"""Estensione dell'esperimento con covariate: volatilita' implicita come covariata su piu' commodities.

Sul WTI (covariate.py) l'unica covariata utile e' l'OVX, e solo per la volatilita'. Qui si controlla se il
risultato si generalizza: i foundation model ricevono come past covariate un indice di volatilita' implicita
CBOE, sui compiti rendimento (VaR) e volatilita' del pilota. Configurazioni:

    VIX      volatilita' implicita dell'S&P 500 (^VIX), su tutte le 15 commodities
    Propria  volatilita' implicita della commodity: OVX (^OVX) per WTI, Brent, Gasolio, Benzina;
             GVZ (^GVZ) per Oro e Argento (gli indici CBOE di argento, mais, soia ecc. non sono piu' pubblicati)

Il benchmark classico con la stessa informazione e' l'HAR-X con la varianza implicita dell'indice.

    python pilota/vol_implicita.py --solo-previsioni --device cuda   previsioni (GPU, Colab)
    python pilota/vol_implicita.py --solo-valuta                     valutazione e report (PC)
    python pilota/vol_implicita.py --prova                           prova veloce su CPU

Output in pilota/risultati/vol_implicita/.
"""

import argparse
import time

import numpy as np
import pandas as pd
import torch
from numpy.lib.stride_tricks import sliding_window_view

import covariate as C
import pilota as P

OUT = P.RIS / "vol_implicita"
INDICI = {"VIX": "^VIX", "OVX": "^OVX", "GVZ": "^GVZ"}
PROPRIA = {"WTI": "OVX", "Brent": "OVX", "Gasolio": "OVX", "Benzina": "OVX", "Oro": "GVZ", "Argento": "GVZ"}
CONFIG = ["VIX", "Propria"]
TASKS = ["rendimento", "volatilita"]


def scarica_indici() -> None:
    import yfinance as yf

    for name, ticker in INDICI.items():
        path = P.DATI / f"{name}.csv"
        if path.exists():
            continue
        df = yf.download(ticker, start="2007-01-01", end=P.DATA_END, auto_adjust=False, progress=False)
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        df[["Close"]].dropna().rename_axis("data").to_csv(path)
        print(f"    scaricato {name} ({ticker}): {len(df)} giorni")


def indice(asset: str, cfg: str) -> str | None:
    return "VIX" if cfg == "VIX" else PROPRIA.get(asset)


def serie_indice(name: str, index: pd.DatetimeIndex) -> np.ndarray:
    """Livello dell'indice sul calendario dell'asset (ultimo valore disponibile; prima dell'inizio, il primo)."""
    s = pd.read_csv(P.DATI / f"{name}.csv", index_col=0, parse_dates=True)["Close"]
    return C.allinea(s, index).ffill().bfill().to_numpy(np.float32)


def lavori(assets: list[str], configs: list[str]) -> list[tuple[str, str, str]]:
    """(asset, compito, configurazione) da calcolare: la volatilita' solo dove il pilota ha OHLC affidabili."""
    out = []
    for a in assets:
        _, _, tasks, _ = P.setup_asset(a, "2024-01-01", P.CONTESTO, 1)
        for t in TASKS:
            if t in tasks:
                out += [(a, t, c) for c in configs if indice(a, c)]
    return out


def cache_path(m: str, asset: str, task: str, cfg: str, tag: str):
    return P.CACHE / f"{m}_{asset}_{task}_iv-{cfg}_{tag}.npy"


def previsioni(assets, modelli, configs, contesto, device, batch, prova=False) -> None:
    tag = f"2024-01-01_c{contesto}_p1"
    for asset, task, cfg in lavori(assets, configs):
        df, origins, _, _ = P.setup_asset(asset, "2024-01-01", contesto, 1)
        if prova:
            origins = origins[::60][:12]
        x = P.model_input(df, task)
        cov = serie_indice(indice(asset, cfg), df.index)
        starts = origins - contesto
        ctx, covs = sliding_window_view(x, contesto)[starts], sliding_window_view(cov, contesto)[starts][:, None]
        for m in modelli:
            path = cache_path(m, asset, task, cfg, tag)
            if path.exists() and not prova:
                continue
            t0 = time.perf_counter()
            q = C.fm_forecast_cov(m, ctx, covs, device, batch)
            print(f"    {m:15} {asset:8} {task:10} +{cfg:7} {len(origins)} previsioni in {time.perf_counter() - t0:6.1f}s"
                  + (f"  forma {q.shape}, finiti {np.isfinite(q).all()}" if prova else ""))
            if not prova:
                P.CACHE.mkdir(parents=True, exist_ok=True)
                np.save(path, q)


# ======================================================================================
# VALUTAZIONE
# ======================================================================================

def valuta(assets, modelli, configs, contesto) -> None:
    tag, btag = f"2024-01-01_c{contesto}_p1", "2024-01-01_p1"
    rel, absr = [], []  # con/senza per asset; punteggi rispetto ai benchmark per asset
    for asset in assets:
        df, origins, tasks, _ = P.setup_asset(asset, "2024-01-01", contesto, 1)
        for task in [t for t in TASKS if t in tasks]:
            fc = {}
            for m in modelli:
                base = P.CACHE / f"{m}_{asset}_{task}_{tag}.npy"
                if not base.exists():
                    continue
                fc[m] = np.load(base)
                for cfg in configs:
                    path = cache_path(m, asset, task, cfg, tag)
                    if indice(asset, cfg) and path.exists():
                        fc[f"{m} + {cfg}"] = np.load(path)
            if not any(" + " in k for k in fc):
                continue  # nessuna previsione con covariata per questo asset e compito
            lv = {k: P.levels_of(k.split(" + ")[0]) for k in fc}
            if task == "rendimento":
                ret = df["rendimento"].to_numpy(float)
                garch = {g: P.bench_cached(g, asset, "rendimento", origins, btag,
                                           lambda g=g: P.garch_quantiles(ret, origins, P.GARCH_Q, spec=g))
                         for g in P.GARCH_SPECS}
                rows, losses, _ = P.eval_rendimento(asset, df, origins, fc, lv, garch)
                absr += [{"asset": asset, "compito": f"VaR {r['alpha']:.0%}", "h": 1, "modello": r["modello"],
                          "valore": r["tick/SS"]} for r in rows]
                Ls = {1: losses[("rendimento", 1)]}
            else:
                rows, losses, _ = P.eval_vol(asset, df, origins, {k: P.common(q, lv[k]) for k, q in fc.items()})
                v = df["var_gk"].to_numpy(float)
                Ls = {}
                for h in P.HORIZONS:
                    L = losses[("volatilita", h)]
                    o = df.index.get_indexer(L.index)
                    real = np.array([np.nanmean(v[oi : oi + h]) for oi in o])

                    def qlike(p):
                        return real / p - np.log(real / p) - 1

                    L["Log-HAR"] = qlike(C.loghar_forecast(v, None, o, h))
                    for cfg in configs:
                        name = indice(asset, cfg)
                        if name:
                            ivar = serie_indice(name, df.index).astype(float) ** 2 / 252 / 1e4
                            L[f"HAR-X + {cfg}"] = qlike(C.harx_forecast(v, ivar, o, h))
                            L[f"Log-HAR-X + {cfg}"] = qlike(C.loghar_forecast(v, ivar, o, h))
                    Ls[h] = L
                    absr += [{"asset": asset, "compito": "volatilita", "h": h, "modello": k,
                              "valore": L[k].mean() / L["HAR"].mean()} for k in L.columns if k != "HAR"]
            for h, L in Ls.items():
                for k in L.columns:
                    if " + " not in k:
                        continue
                    m, cfg = k.split(" + ")
                    ref = {"HAR-X": "HAR", "Log-HAR-X": "Log-HAR"}.get(m, m)
                    stat, p = P.dm_test(L[k].to_numpy(), L[ref].to_numpy(), h)
                    rel.append({"asset": asset, "settore": P.ALL_ASSETS[asset][1], "compito": task, "h": h,
                                "modello": m, "covariata": cfg, "indice": indice(asset, cfg),
                                "rapporto": L[k].mean() / L[ref].mean(), "DM p": p})
    R, A = pd.DataFrame(rel), pd.DataFrame(absr)
    OUT.mkdir(parents=True, exist_ok=True)
    R.to_csv(OUT / "con_contro_senza.csv", index=False)
    A.to_csv(OUT / "punteggi_assoluti.csv", index=False)
    report(R, A, modelli, configs, contesto)


def riassumi(R: pd.DataFrame) -> pd.DataFrame:
    """Per modello, covariata, compito e orizzonte: media geometrica sugli asset e asset significativi (BH)."""
    rows = []
    for (task, h, m, cfg), g in R.groupby(["compito", "h", "modello", "covariata"]):
        rej = P.bh_reject(g["DM p"].to_numpy())
        rows.append({"compito": task, "h": h, "modello": m, "covariata": cfg, "asset": len(g),
                     "rapporto": P.geo_mean(g["rapporto"]), "migliora su": f"{(g['rapporto'] < 1).sum()}/{len(g)}",
                     "meglio (BH)": int((rej & (g["rapporto"] < 1).to_numpy()).sum()),
                     "peggio (BH)": int((rej & (g["rapporto"] > 1).to_numpy()).sum())})
    return pd.DataFrame(rows)


def report(R, A, modelli, configs, contesto) -> None:
    S = riassumi(R)
    order = {m: i for i, m in enumerate([*modelli, "HAR-X", "Log-HAR-X"])}
    S = S.sort_values(["compito", "h", "covariata", "modello"], key=lambda s: s.map(order) if s.name == "modello" else s)
    S.to_csv(OUT / "riepilogo.csv", index=False)
    # punteggi rispetto ai benchmark: media geometrica sugli asset che hanno la covariata
    A = A.copy()
    rows = []
    for cfg in configs:
        assets = set(R.loc[R["covariata"] == cfg, "asset"])
        d = A[A["asset"].isin(assets)]
        names = [*modelli, *[f"{m} + {cfg}" for m in modelli], f"HAR-X + {cfg}", "Log-HAR", f"Log-HAR-X + {cfg}",
                 "GARCH-t", "EGARCH-t"]
        for (task, h), g in d.groupby(["compito", "h"]):
            for k in names:
                s = g.loc[g["modello"] == k, "valore"]
                if len(s):
                    rows.append({"asset con la covariata": cfg, "modello": k, "colonna": f"{task} h={h}"
                                 if task == "volatilita" else task, "valore": P.geo_mean(s)})
    rank = {k: i for i, k in enumerate([*[x for m in modelli for x in (m, *[f"{m} + {c}" for c in configs])],
                                        *[f"HAR-X + {c}" for c in configs], "Log-HAR",
                                        *[f"Log-HAR-X + {c}" for c in configs], "GARCH-t", "EGARCH-t"])}
    B = (pd.DataFrame(rows).pivot_table(index=["asset con la covariata", "modello"], columns="colonna",
                                        values="valore", sort=False).reset_index()
         .sort_values(["asset con la covariata", "modello"], key=lambda s: s.map(rank) if s.name == "modello"
                      else s.map({c: i for i, c in enumerate(configs)})))
    cols = [c for c in ["VaR 10%", "VaR 1%", "volatilita h=1", "volatilita h=5", "volatilita h=20"] if c in B]
    B = B[["asset con la covariata", "modello", *cols]]

    def tab(task, h):
        d = S[(S["compito"] == task) & (S["h"] == h)].drop(columns=["compito", "h"])
        return P.md_table(d)

    with open(OUT / "report_vol_implicita.md", "w", encoding="utf-8") as f:
        f.write("# Volatilita' implicita come covariata\n\n")
        f.write(f"Stessi compiti, origini (dal 2024) e contesto ({contesto} giorni) del pilota. Ogni foundation model "
                "riceve come past covariate un indice CBOE di volatilita' implicita, allineato al calendario della "
                "commodity. VIX su tutte le commodities; volatilita' implicita propria (OVX per WTI, Brent, Gasolio, "
                "Benzina; GVZ per Oro e Argento) dove esiste. HAR-X: l'HAR con la varianza implicita dell'indice "
                "come regressore, confrontato con l'HAR. Log-HAR-X: la stessa regressione in logaritmi (previsione "
                "exp(fit + s2/2)), confrontata con il Log-HAR senza indice.\n\n"
                "Rapporto = perdita con la covariata / perdita dello stesso modello senza (pinball sul rendimento, "
                "QLIKE sulla volatilita'); media geometrica sugli asset. Significativita': Diebold-Mariano con "
                "Benjamini-Hochberg al 10% sugli asset.\n\n")
        f.write("## Volatilita'\n\n")
        for h in P.HORIZONS:
            f.write(f"**h = {h}**\n\n{tab('volatilita', h)}\n\n")
        f.write("## Rendimento (pinball sui decili)\n\n" + tab("rendimento", 1) + "\n\n")
        f.write("## Punteggi rispetto ai benchmark del pilota\n\n"
                "Tick loss / simulazione storica per il VaR, QLIKE / HAR per la volatilita'; media geometrica sugli "
                "asset che hanno la covariata.\n\n" + P.md_table(B) + "\n\n")
        f.write("## Dettaglio per asset (volatilita' h=1)\n\n")
        d = R[(R["compito"] == "volatilita") & (R["h"] == 1)]
        piv = d.pivot_table(index=["asset", "indice"], columns="modello", values="rapporto", sort=False)
        f.write(P.md_table(piv.reset_index()) + "\n")
    print("Report:", OUT / "report_vol_implicita.md")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--asset", nargs="*", default=P.ASSETS, choices=P.ASSETS)
    ap.add_argument("--modelli", nargs="*", default=P.FM_MODELS, choices=P.FM_MODELS)
    ap.add_argument("--config", nargs="*", default=CONFIG, choices=CONFIG)
    ap.add_argument("--contesto", type=int, default=P.CONTESTO)
    ap.add_argument("--batch", type=int, default=128)
    ap.add_argument("--device", default=None)
    ap.add_argument("--solo-previsioni", action="store_true")
    ap.add_argument("--solo-valuta", action="store_true")
    ap.add_argument("--prova", action="store_true", help="contesto 512, 12 origini, niente cache")
    a = ap.parse_args()
    device = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    P.BATCH = a.batch
    P.scarica(a.asset)
    scarica_indici()
    if a.prova:
        previsioni(a.asset, a.modelli, a.config, 512, device, a.batch, prova=True)
        return
    if not a.solo_valuta:
        previsioni(a.asset, a.modelli, a.config, a.contesto, device, a.batch)
    if not a.solo_previsioni:
        valuta(a.asset, a.modelli, a.config, a.contesto)


if __name__ == "__main__":
    main()
