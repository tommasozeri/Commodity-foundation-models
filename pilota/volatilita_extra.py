"""Analisi aggiuntive sulla volatilita': Log-HAR come benchmark e combinazioni con i foundation model.

1. Log-HAR: l'HAR in logaritmi (covariate.loghar_forecast) come secondo benchmark sui 12 asset con OHLC, accanto
   all'HAR in livelli del pilota.
2. Combinazioni a pesi uguali (media delle varianze previste):
   - sui 12 asset: foundation model senza covariate + Log-HAR;
   - sui 5 asset con volatilita' implicita propria (OVX, GVZ): foundation model con l'indice + Log-HAR-X con lo
     stesso indice.

Usa solo previsioni gia' in cache (nessuna GPU). Output in pilota/risultati/volatilita_extra/.

    python pilota/volatilita_extra.py
"""

import numpy as np
import pandas as pd

import covariate as C
import pilota as P
import vol_implicita as V

OUT = P.RIS / "volatilita_extra"
TAG = "2024-01-01_c4096_p1"


def fm_var(q: np.ndarray, model: str, sel: np.ndarray, h: int) -> np.ndarray:
    """Varianza giornaliera media prevista sui prossimi h giorni dai decili della volatilita' (come P.eval_vol)."""
    vq = np.maximum(P.common(q, P.levels_of(model))[sel, :h], 1e-3)
    return np.mean((vq / 100) ** 2 / 252, axis=(1, 2))


def qlike(real: np.ndarray, p: np.ndarray) -> np.ndarray:
    return real / p - np.log(real / p) - 1


def perdite(asset: str) -> dict[int, pd.DataFrame]:
    """QLIKE per origine di benchmark, foundation model e combinazioni, per ogni orizzonte."""
    df, origins, tasks, _ = P.setup_asset(asset, "2024-01-01", P.CONTESTO, 1)
    if "volatilita" not in tasks:
        return {}
    v = df["var_gk"].to_numpy(float)
    iv_name = V.PROPRIA.get(asset)
    ivar = V.serie_indice(iv_name, df.index).astype(float) ** 2 / 252 / 1e4 if iv_name else None
    out = {}
    for h in P.HORIZONS:
        o = origins[origins + h <= len(v)]
        real = np.array([np.nanmean(v[i: i + h]) for i in o])
        ok = np.isfinite(real)
        o, real = o[ok], real[ok]
        sel = np.searchsorted(origins, o)
        pred = {"HAR": P.har_forecast(v, o, h), "Log-HAR": C.loghar_forecast(v, None, o, h)}
        for m in P.FM_MODELS:
            pred[m] = fm_var(np.load(P.CACHE / f"{m}_{asset}_volatilita_{TAG}.npy"), m, sel, h)
            pred[f"{m} + Log-HAR"] = (pred[m] + pred["Log-HAR"]) / 2
        if ivar is not None:
            pred["Log-HAR-X"] = C.loghar_forecast(v, ivar, o, h)
            for m in P.FM_MODELS:
                fx = fm_var(np.load(P.CACHE / f"{m}_{asset}_volatilita_iv-Propria_{TAG}.npy"), m, sel, h)
                pred[f"{m} + IV"] = fx
                pred[f"{m} + IV + Log-HAR-X"] = (fx + pred["Log-HAR-X"]) / 2
        out[h] = pd.DataFrame({k: qlike(real, p) for k, p in pred.items()}, index=df.index[o])
    return out


def confronta(L: dict, coppie: list[tuple[str, str]]) -> pd.DataFrame:
    """Per ogni coppia (modello, riferimento) e orizzonte: media geometrica dei rapporti e asset significativi."""
    rows = []
    for (a, b) in coppie:
        for h in P.HORIZONS:
            r, p, n = [], [], 0
            for asset, Ls in L.items():
                if h in Ls and a in Ls[h] and b in Ls[h]:
                    x, y = Ls[h][a].to_numpy(), Ls[h][b].to_numpy()
                    r.append(x.mean() / y.mean())
                    p.append(P.dm_test(x, y, h)[1])
            if not r:
                continue
            r, p = np.array(r), np.array(p)
            rej = P.bh_reject(p)
            rows.append({"modello": a, "contro": b, "h": h, "asset": len(r), "rapporto": P.geo_mean(pd.Series(r)),
                         "vince su": f"{(r < 1).sum()}/{len(r)}", "meglio (BH)": int((rej & (r < 1)).sum()),
                         "peggio (BH)": int((rej & (r > 1)).sum())})
    return pd.DataFrame(rows)


def mcs_conta(L: dict, nomi: list[str]) -> pd.DataFrame:
    """Quante volte ogni modello e' nel Model Confidence Set al 90% (asset x orizzonti)."""
    cnt, tot = {n: 0 for n in nomi}, 0
    for asset, Ls in L.items():
        for h, D in Ls.items():
            cols = [n for n in nomi if n in D]
            if len(cols) < len(nomi):
                continue
            tot += 1
            for n in P._safe_mcs(D[cols], h):
                cnt[n] += 1
    return pd.DataFrame({"modello": nomi, "in MCS": [f"{cnt[n]}/{tot}" for n in nomi]})


def main() -> None:
    L = {a: perdite(a) for a in P.ASSETS}
    L = {a: x for a, x in L.items() if x}
    iv = {a: L[a] for a in V.PROPRIA if a in L}
    OUT.mkdir(parents=True, exist_ok=True)

    t1 = confronta(L, [("HAR", "Log-HAR"), *[(m, "Log-HAR") for m in P.FM_MODELS],
                       *[(f"{m} + Log-HAR", "Log-HAR") for m in P.FM_MODELS]])
    t2 = confronta(iv, [("Log-HAR-X", "Log-HAR"), *[(f"{m} + IV", "Log-HAR-X") for m in P.FM_MODELS],
                        *[(f"{m} + IV + Log-HAR-X", "Log-HAR-X") for m in P.FM_MODELS]])
    m1 = mcs_conta(L, ["HAR", "Log-HAR", *P.FM_MODELS, *[f"{m} + Log-HAR" for m in P.FM_MODELS]])
    m2 = mcs_conta(iv, ["Log-HAR-X", *[f"{m} + IV" for m in P.FM_MODELS],
                        *[f"{m} + IV + Log-HAR-X" for m in P.FM_MODELS]])
    for name, d in [("log_har", t1), ("combinazioni_iv", t2), ("mcs_log_har", m1), ("mcs_iv", m2)]:
        d.to_csv(OUT / f"{name}.csv", index=False)

    def piv(d):
        x = d.assign(cella=d.apply(lambda r: f"{r['rapporto']:.3f} ({r['meglio (BH)']}/{r['peggio (BH)']})", axis=1))
        return x.pivot_table(index=["modello", "contro"], columns="h", values="cella", aggfunc="first",
                             sort=False).reset_index()

    with open(OUT / "report.md", "w", encoding="utf-8") as f:
        f.write("# Volatilita': Log-HAR e combinazioni\n\nQLIKE del modello / QLIKE del riferimento, media "
                "geometrica sugli asset; tra parentesi asset significativamente migliori/peggiori (DM + BH al 10%). "
                "Combinazioni: media a pesi uguali delle varianze previste.\n\n")
        f.write(f"## 12 asset: contro il Log-HAR\n\n{P.md_table(piv(t1))}\n\n{P.md_table(m1)}\n\n")
        f.write(f"## 5 asset con volatilita' implicita propria: contro il Log-HAR-X\n\n{P.md_table(piv(t2))}\n\n"
                f"{P.md_table(m2)}\n")
    print(open(OUT / "report.md", encoding="utf-8").read())


if __name__ == "__main__":
    main()
