"""Esperimento con covariate sul WTI: i foundation model migliorano se vedono anche altre serie?

Stessi compiti, origini, contesto e valutazione del pilota (pilota.py), sul future WTI. Ogni foundation model
riceve, oltre al passato del WTI, il passato di alcune covariate (solo past covariates: nessun valore futuro,
quindi niente look-ahead). Configurazioni:

    Brent    future Brent (BZ=F)
    Mercato  dollaro (DXY, DX-Y.NYB) e volatilita' implicita del petrolio (OVX, ^OVX)
    Scorte   scorte settimanali USA di greggio esclusa la SPR (EIA WCESTUS1), dalla data di pubblicazione
    Tutte    le quattro serie insieme
    Placebo  rumore sintetico con le statistiche del Brent: controlla che covariate inutili non peggiorino

Il confronto e' con le previsioni senza covariate del pilota principale (stessa cache) e con un benchmark
classico che usa la stessa informazione: HAR-X con la varianza implicita dell'OVX per la volatilita'.

    python pilota/covariate.py --solo-previsioni --device cuda   previsioni (GPU, Colab)
    python pilota/covariate.py --solo-valuta                     valutazione e report (PC)
    python pilota/covariate.py --prova                           prova veloce su CPU (contesto 512, 24 origini)

Output in pilota/risultati/covariate/.
"""

import argparse
import time

import numpy as np
import pandas as pd
import torch
from numpy.lib.stride_tricks import sliding_window_view

import pilota as P

TARGET = "WTI"
OUT = P.RIS / "covariate"
CONFIG = {"Brent": ["brent"], "Mercato": ["dxy", "ovx"], "Scorte": ["scorte"],
          "Tutte": ["brent", "dxy", "ovx", "scorte"], "Placebo": ["placebo"]}
YAHOO = {"DXY": "DX-Y.NYB", "OVX": "^OVX"}
EIA_SCORTE = "https://www.eia.gov/dnav/pet/hist_xls/WCESTUS1w.xls"
# le scorte della settimana che finisce il venerdi' escono il mercoledi' successivo (giovedi' con le festivita'):
# il dato si usa dalla chiusura del giovedi', 6 giorni dopo la fine della settimana
SCORTE_LAG = 6
TASKS = ["prezzo", "rendimento", "volatilita"]


# ======================================================================================
# DATI
# ======================================================================================

def scarica_covariate() -> None:
    """DXY e OVX da Yahoo, scorte EIA settimanali (i file gia' presenti non vengono toccati)."""
    import yfinance as yf

    for name, ticker in YAHOO.items():
        path = P.DATI / f"{name}.csv"
        if path.exists():
            continue
        df = yf.download(ticker, start="2007-01-01", end=P.DATA_END, auto_adjust=False, progress=False)
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        df[["Close"]].dropna().rename_axis("data").to_csv(path)
        print(f"    scaricato {name} ({ticker}): {len(df)} giorni")
    path = P.DATI / "Scorte EIA.csv"
    if not path.exists():
        s = pd.read_excel(EIA_SCORTE, sheet_name="Data 1", skiprows=2, index_col=0).iloc[:, 0].dropna()
        s = s[(s.index >= "2007-01-01") & (s.index < P.DATA_END)] / 1000  # milioni di barili
        out = pd.DataFrame({"scorte": s, "pubblicata": s.index + pd.Timedelta(days=SCORTE_LAG)})
        out.rename_axis("settimana").to_csv(path)
        print(f"    scaricate scorte EIA: {len(s)} settimane")


def allinea(s: pd.Series, index: pd.DatetimeIndex) -> pd.Series:
    """Ultimo valore disponibile a ogni data del calendario del WTI (mai valori successivi alla data)."""
    s = s.sort_index()
    return s.reindex(index.union(s.index)).ffill().reindex(index)


def covariate(df: pd.DataFrame, task: str, seed: int = 0) -> dict[str, np.ndarray]:
    """Covariate sul calendario del WTI, trasformate come il target del compito; senza buchi."""
    idx = df.index
    brent = P.load_asset("Brent")
    b_p = allinea(brent["prezzo"], idx)
    dxy = allinea(pd.read_csv(P.DATI / "DXY.csv", index_col=0, parse_dates=True)["Close"], idx)
    ovx = allinea(pd.read_csv(P.DATI / "OVX.csv", index_col=0, parse_dates=True)["Close"], idx)
    sc = pd.read_csv(P.DATI / "Scorte EIA.csv", parse_dates=["settimana", "pubblicata"])
    scorte = allinea(sc.set_index("pubblicata")["scorte"], idx)
    d_scorte = allinea(sc.set_index("pubblicata")["scorte"].pct_change() * 100, idx)
    rng = np.random.default_rng(seed)
    n = len(idx)
    if task == "prezzo":
        sd = np.log(b_p).diff().std()  # random walk geometrico: positivo come un prezzo
        out = {"brent": b_p, "dxy": dxy, "ovx": ovx, "scorte": scorte,
               "placebo": b_p.mean() * np.exp(np.cumsum(rng.normal(0, sd, n)))}
    elif task == "rendimento":
        b_r = 100 * np.log(b_p).diff()
        out = {"brent": b_r, "dxy": 100 * np.log(dxy).diff(), "ovx": ovx, "scorte": d_scorte,
               "placebo": rng.standard_t(4, n) * b_r.std() / np.sqrt(2)}
    else:
        b_v = allinea(brent["vol_gk"], idx)
        lv = np.log(b_v.dropna())
        ar = np.zeros(n)
        for t in range(1, n):  # AR(1) sul log con la persistenza tipica della volatilita'
            ar[t] = 0.97 * ar[t - 1] + rng.normal(0, lv.std() * np.sqrt(1 - 0.97**2))
        out = {"brent": b_v, "dxy": 100 * np.sqrt(252) * np.log(dxy).diff().abs(), "ovx": ovx, "scorte": scorte,
               "placebo": np.exp(lv.mean() + ar)}
    return {k: pd.Series(np.asarray(v, float), index=idx).ffill().bfill().to_numpy(np.float32)
            for k, v in out.items()}


# ======================================================================================
# PREVISIONI
# ======================================================================================

def fm_forecast_cov(model: str, contexts: np.ndarray, covs: np.ndarray, device: str, batch: int) -> np.ndarray:
    """Come P.fm_forecast, con covariate passate `(N, C, T)` allineate ai contesti `(N, T)`."""
    m = P._load(model, device)
    out = []
    for s in range(0, len(contexts), batch):
        x, c = np.ascontiguousarray(contexts[s : s + batch]), np.ascontiguousarray(covs[s : s + batch])
        if model.startswith("Timestral"):
            out.append(m.forecast(x, prediction_length=P.H_MAX, past_covariates=c).quantiles[:, 0].cpu().numpy())
        elif model == "Chronos-2":
            inputs = [{"target": x[i], "past_covariates": {f"c{j}": c[i, j] for j in range(c.shape[1])}}
                      for i in range(len(x))]
            res = m.predict(inputs, prediction_length=P.H_MAX, batch_size=len(x))
            out.append(np.stack([r[0].T.float().cpu().numpy() for r in res]))
        else:
            res = m.predict_batch(list(x), horizon=P.H_MAX, past_only_covariates=list(c), return_quantiles=True)
            out.append(np.stack([r.quantiles for r in res]))
    return np.concatenate(out).astype(np.float32)


def get_forecasts_cov(model: str, cfg: str, task: str, x: np.ndarray, cov: dict, origins: np.ndarray,
                      ctx: int, device: str, tag: str, batch: int, cache: bool = True) -> np.ndarray:
    path = P.CACHE / f"{model}_{TARGET}_{task}_cov-{cfg}_{tag}.npy"
    if cache and path.exists():
        return np.load(path)
    starts = origins - ctx
    contexts = sliding_window_view(x, ctx)[starts]
    covs = np.stack([sliding_window_view(cov[k], ctx)[starts] for k in CONFIG[cfg]], axis=1)
    t0 = time.perf_counter()
    q = fm_forecast_cov(model, contexts, covs, device, batch)
    print(f"    {model:15} {task:10} +{cfg:8} {len(origins)} previsioni in {time.perf_counter() - t0:6.1f}s")
    if cache:
        P.CACHE.mkdir(parents=True, exist_ok=True)
        np.save(path, q)
    return q


# ======================================================================================
# BENCHMARK CLASSICO CON LA STESSA INFORMAZIONE
# ======================================================================================

def harx_forecast(v: np.ndarray, extra: np.ndarray, origins: np.ndarray, h: int, refit: int = 20) -> np.ndarray:
    """HAR-RV con un regressore in piu' noto all'origine (varianza implicita giornaliera dell'OVX, ieri)."""
    vf = pd.Series(v).ffill().bfill().to_numpy()
    cs = np.r_[0, np.cumsum(vf)]
    t_all = np.arange(22, len(vf))
    xs = np.c_[np.ones(len(t_all)), vf[t_all - 1], (cs[t_all] - cs[t_all - 5]) / 5,
               (cs[t_all] - cs[t_all - 22]) / 22, extra[t_all - 1]]
    y_all = np.array([np.nanmean(v[t : t + h]) if t + h <= len(v) else np.nan for t in t_all])
    out = np.full(len(origins), np.nan)
    beta = None
    for i, o in enumerate(origins):
        if beta is None or i % refit == 0:
            sel = (t_all + h <= o) & np.isfinite(y_all)
            beta = np.linalg.lstsq(xs[sel], y_all[sel], rcond=None)[0]
        out[i] = beta @ xs[o - 22]
    # insanity filter: dove la regressione lineare va sotto il pavimento (a h=1 succede nel ~7% dei giorni)
    # si usa la previsione dell'HAR senza OVX
    floor = np.nanpercentile(v, 1)
    return np.where(out < floor, P.har_forecast(v, origins, h, refit), out)


def loghar_forecast(v: np.ndarray, extra: np.ndarray | None, origins: np.ndarray, h: int,
                    refit: int = 20) -> np.ndarray:
    """HAR-RV in logaritmi (con un regressore in piu' se `extra` non e' None): OLS di log(varianza media nei
    prossimi h giorni) sui log delle componenti giornaliera, settimanale e mensile. La previsione in livelli e'
    exp(fit + s2/2), correzione lognormale con la varianza dei residui della stima. Sempre positiva."""
    vf = pd.Series(v).ffill().bfill().to_numpy()
    cs = np.r_[0, np.cumsum(vf)]
    t_all = np.arange(22, len(vf))
    cols = [np.ones(len(t_all)), np.log(vf[t_all - 1]), np.log((cs[t_all] - cs[t_all - 5]) / 5),
            np.log((cs[t_all] - cs[t_all - 22]) / 22)]
    if extra is not None:
        cols.append(np.log(extra[t_all - 1]))
    xs = np.column_stack(cols)
    y_all = np.log([np.nanmean(v[t : t + h]) if t + h <= len(v) else np.nan for t in t_all])
    out = np.full(len(origins), np.nan)
    beta, s2 = None, 0.0
    for i, o in enumerate(origins):
        if beta is None or i % refit == 0:
            sel = (t_all + h <= o) & np.isfinite(y_all)
            beta = np.linalg.lstsq(xs[sel], y_all[sel], rcond=None)[0]
            s2 = float(np.var(y_all[sel] - xs[sel] @ beta))
        out[i] = np.exp(beta @ xs[o - 22] + s2 / 2)
    return out


# ======================================================================================
# VALUTAZIONE
# ======================================================================================

def label(m: str, cfg: str | None) -> str:
    return m if cfg is None else f"{m} + {cfg}"


def valuta(modelli: list[str], configs: list[str], contesto: int, test_start: str = "2024-01-01") -> None:
    tag = f"{test_start}_c{contesto}_p1"
    df, origins, tasks, _ = P.setup_asset(TARGET, test_start, contesto, 1)
    rows_rel, abs_rows = [], []
    have = {}  # (modello, compito, config o None) -> quantili
    for task in tasks:
        for m in modelli:
            for cfg in [None, *configs]:
                path = P.CACHE / (f"{m}_{TARGET}_{task}_{tag}.npy" if cfg is None
                                  else f"{m}_{TARGET}_{task}_cov-{cfg}_{tag}.npy")
                if path.exists():
                    have[(m, task, cfg)] = np.load(path)
    if not have:
        raise SystemExit("Nessuna previsione con covariate in cache: lancia prima --solo-previsioni (Colab).")

    def keys(task):
        return [(m, cfg) for (m, t, cfg) in have if t == task]

    # prezzo
    btag = f"{test_start}_p1"
    fc = {label(m, c): P.common(have[(m, "prezzo", c)], P.levels_of(m)) for m, c in keys("prezzo")}
    p = df["prezzo"].ffill().to_numpy(float)
    fc.update({b: P.bench_cached(b, TARGET, "prezzo", origins, btag, lambda b=b: P.stat_quantiles(b, p, origins))
               for b in P.PRICE_BENCH})
    rows, losses = P.eval_prezzo(TARGET, df, origins, fc)
    abs_rows += [{**r, "compito": "prezzo", "metrica": "CRPS/RW", "valore": r["CRPS/RW"]} for r in rows]
    rel = {("prezzo", h): losses[("prezzo", h)] for h in P.HORIZONS}
    # rendimento
    ret = df["rendimento"].to_numpy(float)
    garch = {g: P.bench_cached(g, TARGET, "rendimento", origins, btag,
                               lambda g=g: P.garch_quantiles(ret, origins, P.GARCH_Q, spec=g)) for g in P.GARCH_SPECS}
    ks = keys("rendimento")
    rows, losses, _ = P.eval_rendimento(TARGET, df, origins, {label(m, c): have[(m, "rendimento", c)] for m, c in ks},
                                        {label(m, c): P.levels_of(m) for m, c in ks}, garch)
    abs_rows += [{**r, "compito": f"VaR {r['alpha']:.0%}", "metrica": "tick/SS", "valore": r["tick/SS"]}
                 for r in rows]
    rel[("rendimento", 1)] = losses[("rendimento", 1)]
    # volatilita', con HAR-X (OVX) come benchmark classico con la stessa informazione
    if "volatilita" in tasks:
        fc = {label(m, c): P.common(have[(m, "volatilita", c)], P.levels_of(m)) for m, c in keys("volatilita")}
        rows, losses, _ = P.eval_vol(TARGET, df, origins, fc)
        v = df["var_gk"].to_numpy(float)
        ovx_var = covariate(df, "volatilita")["ovx"].astype(float) ** 2 / 252 / 1e4
        for h in P.HORIZONS:
            L = losses[("volatilita", h)]
            o = df.index.get_indexer(L.index)
            real = np.array([np.nanmean(v[oi : oi + h]) for oi in o])
            p = harx_forecast(v, ovx_var, o, h)
            L["HAR-X (OVX)"] = real / p - np.log(real / p) - 1
            rows.append({"asset": TARGET, "h": h, "modello": "HAR-X (OVX)",
                         "QLIKE/HAR": L["HAR-X (OVX)"].mean() / L["HAR"].mean(),
                         "DM p (QLIKE)": P.dm_test(L["HAR-X (OVX)"].to_numpy(), L["HAR"].to_numpy(), h)[1]})
            rel[("volatilita", h)] = L
        abs_rows += [{**r, "compito": "volatilita", "metrica": "QLIKE/HAR", "valore": r["QLIKE/HAR"]} for r in rows]

    # con covariate contro senza, per ogni modello: rapporto delle perdite e Diebold-Mariano
    for (task, h), L in rel.items():
        for m in modelli:
            if m not in L:
                continue
            for cfg in configs:
                k = label(m, cfg)
                if k not in L:
                    continue
                a, b = L[k].to_numpy(), L[m].to_numpy()
                stat, p = P.dm_test(a, b, h)
                rows_rel.append({"compito": task, "h": h, "modello": m, "covariate": cfg,
                                 "rapporto": a.mean() / b.mean(), "DM stat": stat, "DM p": p})
    R = pd.DataFrame(rows_rel)
    # Benjamini-Hochberg su tutte le coppie modello x configurazione dello stesso compito e orizzonte
    R["BH"] = False
    for _, g in R.groupby(["compito", "h"]):
        R.loc[g.index, "BH"] = P.bh_reject(g["DM p"].to_numpy())
    R["esito"] = np.where(~R["BH"], "", np.where(R["rapporto"] < 1, "meglio", "peggio"))
    OUT.mkdir(parents=True, exist_ok=True)
    R.to_csv(OUT / "con_contro_senza.csv", index=False)
    A = pd.DataFrame(abs_rows)
    A.to_csv(OUT / "punteggi_assoluti.csv", index=False)
    report(R, A, df, origins, contesto, modelli, configs)


def report(R: pd.DataFrame, A: pd.DataFrame, df, origins, contesto, modelli, configs) -> None:
    def cella(r):
        mark = {"meglio": " ▼", "peggio": " ▲"}.get(r["esito"], "")
        return f"{r['rapporto']:.3f}{mark}"

    R = R.assign(colonna=R["compito"].str.replace("volatilita", "vol") + " h=" + R["h"].astype(str))
    cols = [c for c in ["prezzo h=1", "prezzo h=5", "prezzo h=20", "rendimento h=1", "vol h=1", "vol h=5", "vol h=20"]
            if c in set(R["colonna"])]
    T = R.assign(v=R.apply(cella, axis=1)).pivot_table(index=["modello", "covariate"], columns="colonna", values="v",
                                                         aggfunc="first")[cols]
    T = T.reindex([(m, c) for m in modelli for c in configs if (m, c) in T.index]).reset_index()
    cnt = (R.assign(esito=R["esito"].replace("", "non significativo")).groupby("covariate")["esito"]
           .value_counts().unstack(fill_value=0).reindex(configs).dropna(how="all"))

    A = A[A["modello"].notna()]
    focus = [("prezzo", "h", 1), ("prezzo", "h", 5), ("prezzo", "h", 20), ("VaR 10%", None, None),
             ("VaR 1%", None, None), ("volatilita", "h", 1), ("volatilita", "h", 5), ("volatilita", "h", 20)]
    ab = []
    for task, hcol, h in focus:
        d = A[A["compito"] == task]
        if hcol:
            d = d[d["h"] == h]
        name = task if h is None else f"{task} h={h}"
        ab.append(d.set_index("modello")["valore"].rename(name))
    ab = pd.concat(ab, axis=1)
    order = [label(m, c) for m in modelli for c in [None, *configs]] + \
            [b for b in ["ARIMA", "ETS", *P.GARCH_SPECS, "HAR-X (OVX)", "Media 22g"] if b in ab.index]
    ab = ab.reindex([o for o in order if o in ab.index]).reset_index().rename(columns={"index": "modello"})

    with open(OUT / "report_covariate.md", "w", encoding="utf-8") as f:
        f.write("# Esperimento con covariate: WTI\n\n")
        f.write(f"Future WTI, test dal {df.index[origins[0]]:%d/%m/%Y} al {df.index[-1]:%d/%m/%Y} ({len(origins)} "
                f"origini giornaliere), contesto {contesto} giorni, stessi compiti e metriche del pilota. "
                "I foundation model ricevono solo il passato delle covariate (past covariates), allineato al "
                "calendario del WTI con l'ultimo valore disponibile a ogni data.\n\n")
        f.write("| configurazione | covariate |\n|---|---|\n"
                "| Brent | future Brent (prezzo, rendimento o volatilita' Garman-Klass, come il compito) |\n"
                "| Mercato | dollaro DXY (livello, rendimento o rendimento assoluto) e OVX (volatilita' implicita) |\n"
                f"| Scorte | scorte USA di greggio esclusa la SPR (EIA), usate dal {SCORTE_LAG}° giorno dopo la "
                "fine della settimana, cioe' dopo la pubblicazione; variazione % per il compito rendimento |\n"
                "| Tutte | le quattro serie |\n"
                "| Placebo | rumore sintetico con le statistiche del Brent, indipendente dal WTI |\n\n")
        f.write("## Con covariate contro senza\n\n"
                "Rapporto tra la perdita con covariate e quella dello stesso modello senza covariate (CRPS sul "
                "prezzo, pinball sul rendimento, QLIKE sulla volatilita'); < 1 = le covariate aiutano. "
                "▼/▲ = significativamente meglio/peggio (Diebold-Mariano, Benjamini-Hochberg al 10% su tutte le "
                "coppie modello x configurazione dello stesso compito e orizzonte).\n\n")
        f.write(P.md_table(T) + "\n\n")
        f.write("**Esiti significativi per configurazione** (su tutti i modelli, compiti e orizzonti)\n\n")
        f.write(P.md_table(cnt.reset_index()) + "\n\n")
        f.write("## Punteggi rispetto ai benchmark del pilota\n\n"
                "CRPS/random walk sul prezzo, tick loss/simulazione storica sul VaR, QLIKE/HAR sulla volatilita'. "
                "Ogni modello senza covariate e con ciascuna configurazione, accanto ai benchmark classici; "
                "HAR-X (OVX) e' l'HAR con la varianza implicita dell'OVX come regressore, cioe' un modello classico "
                "con la stessa informazione di mercato (dove la regressione va sotto il pavimento si usa l'HAR).\n\n")
        f.write(P.md_table(ab) + "\n")
    print("Report:", OUT / "report_covariate.md")


# ======================================================================================
# MAIN
# ======================================================================================

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modelli", nargs="*", default=P.FM_MODELS, choices=P.FM_MODELS)
    ap.add_argument("--config", nargs="*", default=list(CONFIG), choices=list(CONFIG))
    ap.add_argument("--contesto", type=int, default=P.CONTESTO)
    ap.add_argument("--batch", type=int, default=128, help="serie per passata (con covariate servono piu' memoria)")
    ap.add_argument("--device", default=None)
    ap.add_argument("--solo-previsioni", action="store_true", help="calcola solo le previsioni (GPU)")
    ap.add_argument("--solo-valuta", action="store_true", help="usa solo le previsioni gia' in cache")
    ap.add_argument("--prova", action="store_true", help="prova veloce: contesto 512, 24 origini, niente cache")
    a = ap.parse_args()
    device = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    P.BATCH = a.batch
    P.scarica([TARGET, "Brent"])
    scarica_covariate()

    if a.prova:
        df, origins, tasks, _ = P.setup_asset(TARGET, "2024-01-01", 512, 1)
        origins = origins[::30][:24]
        for task in tasks:
            x, cov = P.model_input(df, task), covariate(df, task)
            for m in a.modelli:
                base = P.fm_forecast(m, sliding_window_view(x, 512)[origins - 512], device, a.batch)
                for cfg in a.config:
                    q = get_forecasts_cov(m, cfg, task, x, cov, origins, 512, device, "prova", a.batch, cache=False)
                    lv = P.levels_of(m)
                    i50 = int(np.argmin(np.abs(lv - 0.5)))
                    print(f"      forma {q.shape}, finiti {np.isfinite(q).all()}, |mediana - senza cov| a h=1: "
                          f"{np.abs(q[:, 0, i50] - base[:, 0, i50]).mean():.4f} (scala {np.abs(base[:, 0, i50]).mean():.3f})")
        return

    if not a.solo_valuta:
        df, origins, tasks, _ = P.setup_asset(TARGET, "2024-01-01", a.contesto, 1)
        tag = f"2024-01-01_c{a.contesto}_p1"
        for task in tasks:
            x, cov = P.model_input(df, task), covariate(df, task)
            for m in a.modelli:
                P.get_forecasts(m, TARGET, task, x, origins, a.contesto, device, tag)  # senza covariate (di solito in cache)
                for cfg in a.config:
                    get_forecasts_cov(m, cfg, task, x, cov, origins, a.contesto, device, tag, a.batch)
    if not a.solo_previsioni:
        valuta(a.modelli, a.config, a.contesto)


if __name__ == "__main__":
    main()
