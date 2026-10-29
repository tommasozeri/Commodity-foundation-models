"""PILOTA: Timestral (Mistral) vs TimesFM-3 (Google) sulle commodities.

Esperimento pilota del paper: 4 futures (WTI, Brent, oro, rame), dati giornalieri da Yahoo Finance,
test out-of-sample dal --test-start (default 2024-01-01) con previsioni rolling ogni giorno.

Tre compiti, ciascuno con i suoi benchmark classici:
  1. PREZZO      livello del prezzo di chiusura a 1, 5, 20 giorni
                 benchmark: random walk (con bande dagli ultimi 250 giorni)
                 metriche: MAE e CRPS relativi al RW, direzione, copertura 80%, test di Diebold-Mariano
  2. RENDIMENTO  distribuzione del rendimento log a 1 giorno -> Value at Risk
                 benchmark: simulazione storica (250 giorni), GARCH(1,1) con t di Student
                 metriche: violazioni, test di Kupiec e Christoffersen, tick loss, pinball, DM
  3. VOLATILITA' volatilita' Garman-Klass (da OHLC) media nei prossimi 1, 5, 20 giorni
                 benchmark: HAR-RV, media mobile 22 giorni, random walk
                 metriche: QLIKE e MSE relativi a HAR, DM, Model Confidence Set

Tutti i foundation model ricevono lo stesso contesto (ultimi --contesto giorni, default 4096) e usano
le loro impostazioni di inferenza predefinite. I quantili sono confrontati sui 9 comuni (0.1 ... 0.9):
TimesFM-3 non produce quelli estremi, quindi il VaR al 5% e all'1% e' calcolato solo per Timestral.

Uso:
    python pilota/pilota.py                         tutto (previsioni in cache + valutazione)
    python pilota/pilota.py --modelli Timestral-28M  solo alcuni modelli
    python pilota/pilota.py --solo-valuta            rifa' solo metriche, tabelle e grafici

Output in pilota/risultati/ (con un contesto diverso da 4096: risultati/contesto_N/): report.md, tabelle CSV,
grafici PNG. Previsioni grezze in pilota/cache/. Su CPU il contesto 4096 e' lento: conviene una GPU (Pilota_Colab.ipynb).
"""

import argparse
import math
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view
from scipy import stats

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent
DATI, CACHE, RIS = ROOT / "dati", ROOT / "cache", ROOT / "risultati"
CONTESTO = 4096  # specificazione principale; gli altri contesti vanno in risultati/contesto_N
# nome -> (ticker Yahoo Finance, settore). Esclusi per OHLC inutilizzabili su Yahoo: alluminio (ALI=F,
# 81% di giorni con massimo = minimo, dal 2014), platino (PL=F), palladio (PA=F).
UNIVERSE = {
    "WTI": ("CL=F", "Energia"), "Brent": ("BZ=F", "Energia"), "Gasolio": ("HO=F", "Energia"),
    "Benzina": ("RB=F", "Energia"), "Gas naturale": ("NG=F", "Energia"),
    "Oro": ("GC=F", "Metalli preziosi"), "Argento": ("SI=F", "Metalli preziosi"),
    "Rame": ("HG=F", "Metalli industriali"),
    "Grano": ("ZW=F", "Cereali"), "Mais": ("ZC=F", "Cereali"), "Soia": ("ZS=F", "Cereali"),
    "Caffe": ("KC=F", "Soft e bestiame"), "Zucchero": ("SB=F", "Soft e bestiame"),
    "Cacao": ("CC=F", "Soft e bestiame"), "Bestiame": ("LE=F", "Soft e bestiame"),
}
ASSETS = list(UNIVERSE)
# prezzi spot dell'energia (FRED/EIA): senza roll dei contratti, solo chiusura (niente compito volatilita')
SPOT = {
    "WTI spot": ("DCOILWTICO", "Energia spot"), "Brent spot": ("DCOILBRENTEU", "Energia spot"),
    "Gasolio spot": ("DHOILNYH", "Energia spot"), "Benzina spot": ("DGASNYH", "Energia spot"),
    "Gas naturale spot": ("DHHNGSP", "Energia spot"),
}
ALL_ASSETS = {**UNIVERSE, **SPOT}
DATA_END = "2026-10-24"  # fine dei dati (esclusa): fissa, cosi' le previsioni in cache restano valide
MIN_OHLC = 0.90  # quota minima di giorni con OHLC validi nel test per il compito volatilita'
FM_MODELS = ["Timestral-28M", "Timestral-209M", "TimesFM-3", "Chronos-2"]
# 21 quantili di Timestral e Chronos-2; TimesFM-3 produce solo i decili 0.1...0.9
FULL_Q = np.round(np.r_[0.01, 0.05, np.arange(0.1, 0.91, 0.05), 0.95, 0.99], 2)
PRICE_BENCH = ["ARIMA", "ETS"]  # statsforecast su log-prezzo
GARCH_SPECS = {"GARCH-t": dict(vol="GARCH", p=1, o=0, q=1), "GJR-GARCH-t": dict(vol="GARCH", p=1, o=1, q=1),
               "EGARCH-t": dict(vol="EGARCH", p=1, o=1, q=1)}
STAT_WINDOW = 750  # giorni di log-prezzo per ARIMA/ETS (dal 2021 per il test 2024: esclude il WTI negativo)
H_MAX = 20
HORIZONS = (1, 5, 20)
COMMON_Q = np.round(np.arange(0.1, 0.91, 0.1), 2)  # quantili prodotti da entrambi i modelli
I50 = 4  # indice della mediana in COMMON_Q
BATCH = 128  # serie per passata dei foundation model (--batch)
VAR_LEVELS = (0.10, 0.05, 0.01)
GARCH_Q = np.unique(np.r_[COMMON_Q, VAR_LEVELS])  # quantili di simulazione storica e GARCH
WINDOW = 250  # finestra (giorni) di simulazione storica e bande del random walk


# ======================================================================================
# DATI
# ======================================================================================

def scarica(assets: list[str]) -> None:
    """Scarica da Yahoo Finance i futures mancanti (i file gia' presenti non vengono toccati)."""
    import yfinance as yf

    DATI.mkdir(parents=True, exist_ok=True)
    for name in assets:
        path = DATI / f"{name}.csv"
        if path.exists():
            continue
        if name in SPOT:
            s = pd.read_csv(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={SPOT[name][0]}", na_values=".",
                            index_col=0, parse_dates=True).iloc[:, 0].dropna()
            s = s[(s.index >= "2007-01-01") & (s.index < DATA_END)]
            pd.DataFrame({"Close": s}).rename_axis("data").to_csv(path)
            print(f"    scaricato {name} (FRED {SPOT[name][0]}): {len(s)} giorni")
            continue
        df = yf.download(UNIVERSE[name][0], start="2007-01-01", end=DATA_END, auto_adjust=False, progress=False)
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
        df.index.name = "data"
        df.to_csv(path)
        print(f"    scaricato {name} ({UNIVERSE[name][0]}): {len(df)} giorni")


def load_asset(name: str) -> pd.DataFrame:
    """Prezzo, rendimento log (%), varianza e volatilita' Garman-Klass giornaliere."""
    df = pd.read_csv(DATI / f"{name}.csv", index_col=0, parse_dates=True)
    for k in ("Open", "High", "Low"):  # le serie spot hanno solo la chiusura
        if k not in df:
            df[k] = np.nan
    o, h, l, c = (df[k] for k in ("Open", "High", "Low", "Close"))
    prev = c.shift(1)
    ret = pd.Series(np.where((c > 0) & (prev > 0), 100 * np.log(c / prev), np.nan), index=df.index)
    ok = (o > 0) & (h > 0) & (l > 0) & (c > 0) & (h >= l) & (h > l)
    gk = 0.5 * np.log(h / l) ** 2 - (2 * np.log(2) - 1) * np.log(c / o) ** 2
    gk = gk.where(ok & (gk > 0))
    return pd.DataFrame({"prezzo": c, "rendimento": ret, "var_gk": gk, "vol_gk": np.sqrt(gk * 252) * 100})


def model_input(df: pd.DataFrame, task: str) -> np.ndarray:
    """Serie passata ai foundation model (senza buchi, uguale per tutti)."""
    if task == "prezzo":
        return df["prezzo"].ffill().bfill().to_numpy(np.float32)
    if task == "rendimento":
        return df["rendimento"].fillna(0.0).to_numpy(np.float32)
    return df["vol_gk"].ffill().bfill().to_numpy(np.float32)


# ======================================================================================
# FOUNDATION MODEL (previsioni in cache)
# ======================================================================================

_LOADED: dict = {}


def _load(model: str, device: str):
    if model not in _LOADED:
        if model.startswith("Timestral"):
            from timestral import TimestralForecaster

            _LOADED[model] = TimestralForecaster.from_pretrained(f"mistralai/{model}", device=device)
        elif model == "Chronos-2":
            from chronos import Chronos2Pipeline

            _LOADED[model] = Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map=device)
        else:
            from timesfm3 import ModelConfig, TimesFM3Evaluator

            _LOADED[model] = TimesFM3Evaluator(ModelConfig(per_core_batch_size=BATCH, device=device))
    return _LOADED[model]


def fm_forecast(model: str, contexts: np.ndarray, device: str, batch: int | None = None) -> np.ndarray:
    """Quantili `(N, H_MAX, Q)`: 21 livelli (FULL_Q) per Timestral e Chronos-2, 9 (0.1...0.9) per TimesFM-3."""
    m = _load(model, device)
    batch = batch or BATCH
    out = []
    for s in range(0, len(contexts), batch):
        chunk = contexts[s : s + batch]
        if model.startswith("Timestral"):
            out.append(m.forecast(np.ascontiguousarray(chunk), prediction_length=H_MAX).quantiles[:, 0].cpu().numpy())
        elif model == "Chronos-2":
            res = m.predict(np.ascontiguousarray(chunk[:, None]), prediction_length=H_MAX, batch_size=len(chunk))
            out.append(np.stack([r[0].T.float().cpu().numpy() for r in res]))  # (1, Q, H) -> (H, Q)
        else:
            res = m.predict_batch([c for c in chunk], horizon=H_MAX, return_quantiles=True)
            out.append(np.stack([r.quantiles for r in res]))
    return np.concatenate(out).astype(np.float32)


def levels_of(model: str) -> np.ndarray:
    return COMMON_Q if model == "TimesFM-3" else FULL_Q


def common(q: np.ndarray, levels: np.ndarray) -> np.ndarray:
    """Estrae i 9 quantili comuni 0.1...0.9."""
    idx = [int(np.argmin(np.abs(levels - x))) for x in COMMON_Q]
    return q[..., idx]


def get_forecasts(model: str, asset: str, task: str, x: np.ndarray, origins: np.ndarray, ctx: int,
                  device: str, tag: str) -> np.ndarray:
    path = CACHE / f"{model}_{asset}_{task}_{tag}.npy"
    if path.exists():
        return np.load(path)
    # con una previsione ogni k giorni riusa, se c'e', la cache giornaliera (stesse origini, una ogni k)
    base, step = tag.rsplit("_p", 1)
    daily = CACHE / f"{model}_{asset}_{task}_{base}_p1.npy"
    if int(step) > 1 and daily.exists():
        q1 = np.load(daily)
        if len(q1[:: int(step)]) == len(origins):
            return q1[:: int(step)]
    windows = sliding_window_view(x, ctx)
    contexts = windows[origins - ctx]
    t0 = time.perf_counter()
    q = fm_forecast(model, contexts, device)
    print(f"    {model:15} {asset:6} {task:10} {len(origins)} previsioni in {time.perf_counter() - t0:6.1f}s")
    CACHE.mkdir(parents=True, exist_ok=True)
    np.save(path, q)
    return q


# ======================================================================================
# STRUMENTI STATISTICI
# ======================================================================================

def pinball(q: np.ndarray, y: np.ndarray, levels: np.ndarray) -> np.ndarray:
    """Pinball loss media sui quantili: q `(..., Q)`, y `(...)` -> `(...)`."""
    d = y[..., None] - q
    return np.maximum(levels * d, (levels - 1) * d).mean(-1)


def dm_test(loss_a: np.ndarray, loss_b: np.ndarray, h: int) -> tuple[float, float]:
    """Diebold-Mariano con correzione Harvey-Leybourne-Newbold e varianza Newey-West (lag h-1).

    Ritorna (statistica, p-value bilaterale). Statistica < 0: il modello A ha perdita minore.
    """
    d = np.asarray(loss_a - loss_b, dtype=float)
    d = d[np.isfinite(d)]
    t = len(d)
    if t < 10 or np.allclose(d, 0):
        return np.nan, np.nan
    dc = d - d.mean()
    var = dc @ dc / t
    for k in range(1, h):
        var += 2 * (1 - k / h) * (dc[k:] @ dc[:-k]) / t
    if var <= 0:
        return np.nan, np.nan
    stat = d.mean() / math.sqrt(var / t)
    stat *= math.sqrt((t + 1 - 2 * h + h * (h - 1) / t) / t)
    return float(stat), float(2 * stats.t.sf(abs(stat), df=t - 1))


def kupiec(hits: np.ndarray, alpha: float) -> float:
    """p-value del test di copertura incondizionata (proporzione di violazioni = alpha)."""
    t, x = len(hits), int(hits.sum())
    pi = x / t
    ll0 = (t - x) * math.log(1 - alpha) + x * math.log(alpha)
    ll1 = (t - x) * math.log(1 - pi) if pi < 1 else 0.0
    ll1 += x * math.log(pi) if pi > 0 else 0.0
    return float(stats.chi2.sf(-2 * (ll0 - ll1), 1))


def christoffersen(hits: np.ndarray, alpha: float) -> float:
    """p-value del test di copertura condizionata (giusta frequenza + violazioni non a grappolo)."""
    h = hits.astype(int)
    n00 = int(((h[:-1] == 0) & (h[1:] == 0)).sum())
    n01 = int(((h[:-1] == 0) & (h[1:] == 1)).sum())
    n10 = int(((h[:-1] == 1) & (h[1:] == 0)).sum())
    n11 = int(((h[:-1] == 1) & (h[1:] == 1)).sum())

    def ll(p, a, b):  # a successi, b insuccessi
        return (a * math.log(p) if a else 0.0) + (b * math.log(1 - p) if b else 0.0)

    p01 = n01 / max(n00 + n01, 1)
    p11 = n11 / max(n10 + n11, 1)
    p = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)
    lr_ind = -2 * (ll(p, n01 + n11, n00 + n10) - ll(p01, n01, n00) - ll(p11, n11, n10))
    lr_uc = stats.chi2.isf(kupiec(hits, alpha), 1) if kupiec(hits, alpha) > 0 else 1e3
    return float(stats.chi2.sf(lr_uc + max(lr_ind, 0), 2))


def tick(y: np.ndarray, q: np.ndarray, alpha: float) -> np.ndarray:
    return (alpha - (y < q)) * (y - q)


def mcs(losses: pd.DataFrame, block: int) -> list[str]:
    """Modelli nel Model Confidence Set al 90% (Hansen, Lunde e Nason)."""
    from arch.bootstrap import MCS

    m = MCS(losses.dropna(), size=0.10, block_size=max(block, 2), reps=1000, method="R", seed=0)
    m.compute()
    return list(m.included)


def _safe_mcs(losses: pd.DataFrame, block: int) -> list[str]:
    try:
        return mcs(losses, block)
    except Exception:
        return []


# ======================================================================================
# BENCHMARK CLASSICI
# ======================================================================================

def bench_cached(name: str, asset: str, task: str, origins: np.ndarray, tag: str, fn) -> np.ndarray:
    """Previsioni di un benchmark classico, in cache come quelle dei foundation model (non dipendono dal contesto)."""
    path = CACHE / f"bench_{name}_{asset}_{task}_{tag}_o{origins[0]}-{len(origins)}.npy"
    if path.exists():
        return np.load(path)
    t0 = time.perf_counter()
    q = fn()
    print(f"    {name:15} {asset:6} {task:10} {len(origins)} previsioni in {time.perf_counter() - t0:6.1f}s")
    CACHE.mkdir(parents=True, exist_ok=True)
    np.save(path, q)
    return q


def stat_quantiles(kind: str, p: np.ndarray, origins: np.ndarray, refit: int = 20) -> np.ndarray:
    """Decili del prezzo a 1...H_MAX giorni da AutoARIMA o AutoETS (statsforecast) sul log-prezzo degli ultimi
    STAT_WINDOW giorni. Il modello e' riselezionato e stimato ogni `refit` origini; in mezzo e' riapplicato ai
    dati nuovi con i parametri fissi. Intervalli gaussiani sul log, riportati in prezzo con exp."""
    from statsforecast.models import AutoARIMA, AutoETS

    lv = [20, 40, 60, 80]
    cols = [f"lo-{x}" for x in lv[::-1]] + ["mean"] + [f"hi-{x}" for x in lv]  # quantili 0.1 ... 0.9
    logp = np.log(np.maximum(p, np.min(p[p > 0])))
    out = np.full((len(origins), H_MAX, len(COMMON_Q)), np.nan)
    model = None
    for i, o in enumerate(origins):
        y = logp[max(0, o - STAT_WINDOW) : o]
        if model is None or i % refit == 0:
            model = AutoARIMA(season_length=1) if kind == "ARIMA" else AutoETS(season_length=1, model="ZZN")
            model.fit(y)
        f = model.forward(y=y, h=H_MAX, level=lv)
        out[i] = np.exp(np.stack([f[c] for c in cols], -1))
    return out


def garch_quantiles(r: np.ndarray, origins: np.ndarray, levels: np.ndarray, refit: int = 20,
                    spec: str = "GARCH-t") -> np.ndarray:
    """Quantili a 1 giorno da un modello GARCH con t di Student (GARCH_SPECS), riscalato ogni `refit` origini."""
    from arch import arch_model

    out = np.full((len(origins), len(levels)), np.nan)
    params = None
    for i, o in enumerate(origins):
        hist = r[max(0, o - 2500) : o]
        hist = hist[np.isfinite(hist)]
        am = arch_model(hist, mean="Constant", dist="t", **GARCH_SPECS[spec])
        if params is None or i % refit == 0:
            params = am.fit(disp="off", show_warning=False).params
        f = am.fix(params).forecast(horizon=1, reindex=False)
        mu, s2 = float(f.mean.values[-1, 0]), float(f.variance.values[-1, 0])
        nu = float(params["nu"])
        out[i] = mu + math.sqrt(s2) * stats.t.ppf(levels, nu) * math.sqrt((nu - 2) / nu)
    return out


def har_forecast(v: np.ndarray, origins: np.ndarray, h: int, refit: int = 20) -> np.ndarray:
    """HAR-RV diretto: media della varianza nei prossimi h giorni ~ var. ieri, media 5 e 22 giorni."""
    vf = pd.Series(v).ffill().bfill().to_numpy()
    cs = np.r_[0, np.cumsum(vf)]
    t_all = np.arange(22, len(vf))
    x_d = vf[t_all - 1]
    x_w = (cs[t_all] - cs[t_all - 5]) / 5
    x_m = (cs[t_all] - cs[t_all - 22]) / 22
    y_all = np.array([np.nanmean(v[t : t + h]) if t + h <= len(v) else np.nan for t in t_all])
    out = np.full(len(origins), np.nan)
    beta = None
    for i, o in enumerate(origins):
        if beta is None or i % refit == 0:
            sel = (t_all + h <= o) & np.isfinite(y_all)
            xmat = np.c_[np.ones(sel.sum()), x_d[sel], x_w[sel], x_m[sel]]
            beta = np.linalg.lstsq(xmat, y_all[sel], rcond=None)[0]
        j = o - 22
        out[i] = beta @ np.r_[1, x_d[j], x_w[j], x_m[j]]
    floor = np.nanpercentile(v, 1)
    return np.maximum(out, floor)


# ======================================================================================
# VALUTAZIONE
# ======================================================================================

def eval_prezzo(asset, df, origins, fc) -> tuple[list[dict], dict]:
    p = df["prezzo"].ffill().to_numpy(float)
    rows, losses = [], {}
    for h in HORIZONS:
        ok = origins + h - 1 < len(p)
        o = origins[ok]
        y, last = p[o + h - 1], p[o - 1]
        # random walk probabilistico: ultimo prezzo + quantili delle variazioni a h giorni recenti
        rw_q = np.empty((len(o), len(COMMON_Q)))
        for i, oi in enumerate(o):
            ts = np.arange(max(1, oi - WINDOW), oi - h + 1)
            rw_q[i] = last[i] + np.quantile(p[ts + h - 1] - p[ts - 1], COMMON_Q)
        base_ae, base_ql = np.abs(last - y), pinball(rw_q, y, COMMON_Q)
        losses[("prezzo", h)] = pd.DataFrame({"Random walk": base_ql}, index=df.index[o])
        for m, q in fc.items():
            qm = q[ok, h - 1]
            ae, ql = np.abs(qm[:, I50] - y), pinball(qm, y, COMMON_Q)
            losses[("prezzo", h)][m] = ql
            mask = y != last
            rows.append({
                "asset": asset, "h": h, "modello": m, "n": len(o),
                "MAE/RW": ae.mean() / base_ae.mean(), "CRPS/RW": ql.mean() / base_ql.mean(),
                "DM p (CRPS)": dm_test(ql, base_ql, h)[1], "DM stat": dm_test(ql, base_ql, h)[0],
                "direzione": float(np.mean(np.sign(qm[mask, I50] - last[mask]) == np.sign(y[mask] - last[mask]))),
                "cop80": float(np.mean((y >= qm[:, 0]) & (y <= qm[:, -1]))),
                "cop80 RW": float(np.mean((y >= rw_q[:, 0]) & (y <= rw_q[:, -1]))),
            })
        included = _safe_mcs(losses[("prezzo", h)], h)
        for row in rows:
            if row["h"] == h:
                row["in MCS"] = row["modello"] in included
        rows.append({"asset": asset, "h": h, "modello": "Random walk", "n": len(o), "MAE/RW": 1.0, "CRPS/RW": 1.0,
                     "cop80": float(np.mean((y >= rw_q[:, 0]) & (y <= rw_q[:, -1]))),
                     "in MCS": "Random walk" in included})
    return rows, losses


def eval_rendimento(asset, df, origins, fc_full, levels_full, garch) -> tuple[list[dict], dict, dict]:
    r = df["rendimento"].to_numpy(float)
    y = r[origins]
    ok = np.isfinite(y)
    y = y[ok]
    o = origins[ok]
    hs = np.array([np.nanquantile(r[max(0, oi - WINDOW) : oi], GARCH_Q) for oi in o])
    preds = {"Simulazione storica": (hs, GARCH_Q), **{k: (q[ok], GARCH_Q) for k, q in garch.items()}}
    for m, q in fc_full.items():
        preds[m] = (q[ok, 0], levels_full[m])
    rows, losses, var_paths = [], {}, {}
    ticks = {a: {} for a in VAR_LEVELS}  # tick loss per livello di VaR, per il Model Confidence Set
    base_ql = pinball(common(hs, GARCH_Q), y, COMMON_Q)
    losses[("rendimento", 1)] = pd.DataFrame({"Simulazione storica": base_ql}, index=df.index[o])
    for m, (q, lv) in preds.items():
        ql = pinball(common(q, lv), y, COMMON_Q)
        if m != "Simulazione storica":
            losses[("rendimento", 1)][m] = ql
        for a in VAR_LEVELS:
            if np.min(np.abs(lv - a)) > 1e-6:
                continue  # TimesFM-3 non ha i quantili 0.05 e 0.01
            var = q[:, int(np.argmin(np.abs(lv - a)))]
            hits = y < var
            hs_var = hs[:, int(np.argmin(np.abs(GARCH_Q - a)))]
            ticks[a][m] = tick(y, var, a)
            rows.append({
                "asset": asset, "alpha": a, "modello": m, "n": len(y),
                "violazioni": float(hits.mean()), "Kupiec p": kupiec(hits, a), "Christoffersen p": christoffersen(hits, a),
                "tick/SS": tick(y, var, a).mean() / tick(y, hs_var, a).mean(),
                "pinball/SS": ql.mean() / base_ql.mean(), "DM p (pinball)": dm_test(ql, base_ql, 1)[1],
            })
            if a == 0.10:
                var_paths[m] = var
    # MCS sulla tick loss di ciascun livello di VaR (al 5% e 1% senza TimesFM-3, che non ha quei quantili)
    for a, tk in ticks.items():
        included = _safe_mcs(pd.DataFrame(tk), 1)
        for row in rows:
            if row["alpha"] == a:
                row["in MCS"] = row["modello"] in included
    var_paths["_y"], var_paths["_date"] = y, df.index[o]
    return rows, losses, var_paths


def eval_vol(asset, df, origins, fc) -> tuple[list[dict], dict, dict]:
    v = df["var_gk"].to_numpy(float)
    vf = pd.Series(v).ffill().bfill().to_numpy()
    rows, losses, paths = [], {}, {}
    for h in HORIZONS:
        ok = origins + h <= len(v)
        o = origins[ok]
        real = np.array([np.nanmean(v[oi : oi + h]) for oi in o])
        good = np.isfinite(real)
        o, real = o[good], real[good]
        preds = {
            "HAR": har_forecast(v, o, h),
            "Media 22g": np.array([np.nanmean(v[oi - 22 : oi]) for oi in o]),
            "Random walk": vf[o - 1],
        }
        sel = np.flatnonzero(ok)[good]
        for m, q in fc.items():
            # QLIKE premia la media della varianza: la stimo dai 9 quantili (decili) della volatilita'
            # prevista; la mediana al quadrato la sottostimerebbe (distribuzione asimmetrica)
            vq = np.maximum(q[sel, :h], 1e-3)
            preds[m] = np.mean((vq / 100) ** 2 / 252, axis=(1, 2))
        qlike = {m: real / p - np.log(real / p) - 1 for m, p in preds.items()}
        mse = {m: (np.sqrt(252 * real) * 100 - np.sqrt(252 * p) * 100) ** 2 for m, p in preds.items()}
        L = pd.DataFrame(qlike, index=df.index[o])
        losses[("volatilita", h)] = L
        included = _safe_mcs(L, h)
        for m in preds:
            if m == "HAR":
                continue
            rows.append({
                "asset": asset, "h": h, "modello": m, "n": len(o),
                "QLIKE/HAR": qlike[m].mean() / qlike["HAR"].mean(), "MSE/HAR": mse[m].mean() / mse["HAR"].mean(),
                "DM p (QLIKE)": dm_test(qlike[m], qlike["HAR"], h)[1], "in MCS": m in included,
            })
        rows.append({"asset": asset, "h": h, "modello": "HAR", "n": len(o), "QLIKE/HAR": 1.0, "MSE/HAR": 1.0,
                     "DM p (QLIKE)": np.nan, "in MCS": "HAR" in included})
        if h == 5:
            paths = {m: np.sqrt(252 * p) * 100 for m, p in preds.items()}
            paths["_real"], paths["_date"] = np.sqrt(252 * real) * 100, df.index[o]
    return rows, losses, paths


# ======================================================================================
# OUTPUT
# ======================================================================================

def md_table(df: pd.DataFrame, floatfmt: str = ".3f") -> str:
    cols = list(df.columns)
    fmt = lambda x: (f"{x:{floatfmt}}" if isinstance(x, (float, np.floating)) and np.isfinite(x)
                     else "" if isinstance(x, float) else str(x))
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(lines)


def geo_mean(s: pd.Series) -> float:
    s = s.dropna()
    return float(np.exp(np.log(s).mean())) if len(s) else np.nan


COLORS = {"Timestral-28M": "#7fb3d5", "Timestral-209M": "#1f618d", "TimesFM-3": "#d35400", "Chronos-2": "#c0392b",
          "ARIMA": "#a3a3a3", "ETS": "#6e6e6e", "GARCH-t": "#7d3c98", "GJR-GARCH-t": "#a569bd", "EGARCH-t": "#d2b4de",
          "Simulazione storica": "#999999", "HAR": "#27ae60", "Media 22g": "#d4ac0d", "Random walk": "#555555"}
BENCH_SHOWN = [*PRICE_BENCH, *GARCH_SPECS, "Media 22g"]  # benchmark mostrati accanto ai modelli nei grafici


def plots(prezzo: pd.DataFrame, rend: pd.DataFrame, vol: pd.DataFrame, var_paths: dict, vol_paths: dict,
          models: list[str]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = COLORS

    # 1. punteggi relativi (media geometrica sugli asset, punti = singoli asset)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    panels = [(prezzo, "CRPS/RW", "h", "Prezzo: CRPS / random walk"),
              (rend[rend["alpha"] == 0.10], "pinball/SS", None, "Rendimento: pinball / sim. storica"),
              (vol, "QLIKE/HAR", "h", "Volatilita': QLIKE / HAR")]
    for ax, (d, col, hcol, title) in zip(axes, panels):
        # il random walk sulla volatilita' e' fuori scala (fino a ~100x HAR): resta nelle tabelle
        ms = [m for m in d["modello"].unique() if m not in ("HAR", "Simulazione storica", "Random walk")]
        groups = sorted(d[hcol].unique()) if hcol else [1]
        w = 0.8 / len(ms)
        for j, m in enumerate(ms):
            for k, g in enumerate(groups):
                sub = d[(d["modello"] == m) & ((d[hcol] == g) if hcol else True)]
                x = k + (j - (len(ms) - 1) / 2) * w
                # barre come scostamento dal benchmark (= 1), per vedere differenze di pochi punti
                ax.bar(x, geo_mean(sub[col]) - 1, w * 0.9, bottom=1, color=colors.get(m, "C0"),
                       label=m if k == 0 else None)
                ax.scatter([x] * len(sub), sub[col], s=10, color="k", zorder=3)
        ax.axhline(1, color="k", lw=0.8, ls="--")
        ax.set_xticks(range(len(groups)), [f"h={g}" for g in groups] if hcol else ["h=1"])
        ax.set_title(title, fontsize=10)
        ax.set_ylabel("< 1 = meglio del benchmark")
    handles, labels = [], []
    for ax in axes:
        for hd, lb in zip(*ax.get_legend_handles_labels()):
            if lb not in labels:
                handles.append(hd), labels.append(lb)
    fig.legend(handles, labels, loc="upper center", ncol=len(labels), frameon=False, fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(RIS / "punteggi_relativi.png", dpi=130)
    plt.close(fig)

    # 2. VaR al 10% sul WTI
    if "WTI" in var_paths:
        vp = var_paths["WTI"]
        fig, ax = plt.subplots(figsize=(13, 4.5))
        ax.plot(vp["_date"], vp["_y"], color="0.6", lw=0.7, label="rendimento giornaliero (%)")
        for m in ["Simulazione storica", "GARCH-t", *models]:
            if m in vp:
                ax.plot(vp["_date"], vp[m], lw=1.1, color=colors.get(m), label=f"VaR 10% {m}")
        for m in models:
            if m in vp:
                hit = vp["_y"] < vp[m]
                ax.scatter(vp["_date"][hit], vp["_y"][hit], s=8, color=colors.get(m), zorder=3)
        ax.set_title("WTI: VaR al 10% a 1 giorno e violazioni (punti)")
        ax.legend(fontsize=8, ncol=3)
        fig.tight_layout()
        fig.savefig(RIS / "var_wti.png", dpi=130)
        plt.close(fig)

    # 3. volatilita' a 5 giorni sul WTI
    if "WTI" in vol_paths:
        vp = vol_paths["WTI"]
        fig, ax = plt.subplots(figsize=(13, 4.5))
        ax.plot(vp["_date"], vp["_real"], color="k", lw=0.9, label="realizzata (media 5g, Garman-Klass)")
        for m in ["HAR", *models]:
            if m in vp:
                ax.plot(vp["_date"], vp[m], lw=1.1, color=colors.get(m), label=f"prevista {m}")
        ax.set_ylabel("volatilita' annualizzata (%)")
        ax.set_title("WTI: volatilita' media nei 5 giorni successivi, prevista vs realizzata")
        ax.legend(fontsize=8, ncol=3)
        fig.tight_layout()
        fig.savefig(RIS / "vol_wti.png", dpi=130)
        plt.close(fig)


# ======================================================================================
# MAIN
# ======================================================================================

# ======================================================================================
# SOTTO-PERIODI, REGIMI, SETTORI, TEST MULTIPLI
# ======================================================================================

BENCH = {"prezzo": "Random walk", "rendimento": "Simulazione storica", "volatilita": "HAR"}
FOCUS = [("prezzo", 5, "Prezzo h=5: CRPS / random walk"), ("rendimento", 1, "Rendimento: pinball / sim. storica"),
         ("volatilita", 5, "Volatilita' h=5: QLIKE / HAR")]


def long_losses(all_losses: dict, regimes: dict) -> pd.DataFrame:
    """Una riga per previsione: perdita del modello e del benchmark del suo compito, con anno e regime."""
    parts = []
    for (asset, task, h), L in all_losses.items():
        base = L[BENCH[task]].to_numpy()
        for m in L.columns:
            if m == BENCH[task] or (task == "volatilita" and m == "Random walk"):
                continue
            parts.append(pd.DataFrame({"data": L.index, "asset": asset, "settore": ALL_ASSETS[asset][1],
                                       "compito": task, "h": h, "modello": m, "loss": L[m].to_numpy(),
                                       "base": base}))
    long = pd.concat(parts, ignore_index=True)
    long["anno"] = long["data"].dt.year.astype(str)
    long["regime"] = [regimes[a].get(d, np.nan) for a, d in zip(long["asset"], long["data"])]
    return long.dropna(subset=["loss", "base"])


def rel_by(long: pd.DataFrame, by: str) -> pd.DataFrame:
    """Rapporto perdita modello / benchmark per asset e gruppo, poi media geometrica sugli asset."""
    g = long.groupby(["compito", "h", "modello", by, "asset"])[["loss", "base"]].sum()
    g["rel"] = g["loss"] / g["base"]
    out = g.groupby(["compito", "h", "modello", by])["rel"].agg(
        rel=geo_mean, vince=lambda s: f"{int((s < 1).sum())}/{len(s)}")
    return out.reset_index()


def bh_reject(p: np.ndarray, q: float = 0.10) -> np.ndarray:
    """Benjamini-Hochberg: quali p-value restano significativi controllando il false discovery rate a q."""
    p = np.asarray(p, float)
    ok = np.isfinite(p)
    rej = np.zeros(len(p), bool)
    if ok.sum() == 0:
        return rej
    ps = p[ok]
    order = np.argsort(ps)
    thr = q * np.arange(1, len(ps) + 1) / len(ps)
    passed = ps[order] <= thr
    k = np.max(np.flatnonzero(passed)) + 1 if passed.any() else 0
    r = np.zeros(len(ps), bool)
    r[order[:k]] = True
    rej[ok] = r
    return rej


def significance(prezzo: pd.DataFrame, rend: pd.DataFrame, vol: pd.DataFrame) -> pd.DataFrame:
    """Quanti asset hanno una differenza significativa (DM, BH al 10% sugli asset) a favore o contro."""
    specs = [(prezzo, "prezzo", "h", "CRPS/RW", "DM p (CRPS)"),
             (rend[rend["alpha"] == 0.10].assign(h=1), "rendimento", "h", "pinball/SS", "DM p (pinball)")]
    if len(vol):  # le serie spot non hanno il compito volatilita'
        specs.append((vol[vol["modello"] != "HAR"], "volatilita", "h", "QLIKE/HAR", "DM p (QLIKE)"))
    rows = []
    for d, task, hcol, rel, pcol in specs:
        for (h, m), g in d.groupby([hcol, "modello"]):
            if m in ("Simulazione storica", "Random walk") and task != "volatilita":
                continue
            rej = bh_reject(g[pcol].to_numpy())
            better = rej & (g[rel].to_numpy() < 1)
            worse = rej & (g[rel].to_numpy() > 1)
            raw = (g[pcol] < 0.05).to_numpy()
            rows.append({"compito": task, "h": h, "modello": m, "asset": len(g),
                         "meglio (BH)": int(better.sum()), "peggio (BH)": int(worse.sum()),
                         "p<0.05 senza correzione": int(raw.sum())})
    return pd.DataFrame(rows)


VS_CLASSIC = [("prezzo", "ARIMA"), ("prezzo", "ETS"), ("rendimento", "GARCH-t"), ("rendimento", "GJR-GARCH-t"),
              ("rendimento", "EGARCH-t")]


def significance_vs(all_losses: dict, models: list[str]) -> pd.DataFrame:
    """Ogni foundation model contro ciascun benchmark classico sulla stessa perdita: rapporto (media geometrica
    sugli asset) e asset con differenza significativa (DM, BH al 10%)."""
    rows = []
    for task, b in VS_CLASSIC:
        for h in sorted({k[2] for k in all_losses if k[1] == task}):
            tabs = [L for (_, t, hh), L in all_losses.items() if t == task and hh == h and b in L]
            for m in models:
                res = [(L[m].mean() / L[b].mean(), dm_test(L[m].to_numpy(), L[b].to_numpy(), h)[1])
                       for L in tabs if m in L]
                if not res:
                    continue
                rel, p = map(np.array, zip(*res))
                rej = bh_reject(p)
                rows.append({"compito": task, "h": h, "modello": m, "contro": b, "rapporto": geo_mean(pd.Series(rel)),
                             "batte su": f"{int((rel < 1).sum())}/{len(rel)}", "meglio (BH)": int((rej & (rel < 1)).sum()),
                             "peggio (BH)": int((rej & (rel > 1)).sum())})
    return pd.DataFrame(rows)


def plot_groups(sub: pd.DataFrame, path: Path, models: list[str], title: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = COLORS
    fig, axes = plt.subplots(1, len(FOCUS), figsize=(16, 4.6))
    for ax, (task, h, ttl) in zip(axes, FOCUS):
        d = sub[(sub["compito"] == task) & (sub["h"] == h)]
        groups = list(dict.fromkeys(d["gruppo"]))
        ms = [m for m in [*models, *BENCH_SHOWN] if m in set(d["modello"])]
        w = 0.8 / max(len(ms), 1)
        for j, m in enumerate(ms):
            for k, g in enumerate(groups):
                v = d[(d["modello"] == m) & (d["gruppo"] == g)]["rel"]
                if len(v):
                    x = k + (j - (len(ms) - 1) / 2) * w
                    ax.bar(x, float(v.iloc[0]) - 1, w * 0.9, bottom=1, color=colors.get(m, "C0"),
                           label=m if k == 0 else None)
        ax.axhline(1, color="k", lw=0.8, ls="--")
        ax.set_xticks(range(len(groups)), groups, fontsize=8)
        ax.set_title(ttl, fontsize=10)
        ax.set_ylabel("< 1 = meglio del benchmark")
    handles, labels = [], []
    for ax in axes:
        for hd, lb in zip(*ax.get_legend_handles_labels()):
            if lb not in labels:
                handles.append(hd), labels.append(lb)
    fig.legend(handles, labels, loc="upper center", ncol=len(labels), frameon=False, fontsize=9)
    fig.suptitle(title, y=0.995, fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_heatmap(prezzo: pd.DataFrame, rend: pd.DataFrame, vol: pd.DataFrame, models: list[str]) -> None:
    """Asset x modello: punteggio relativo nei tre compiti (blu = meglio del benchmark, rosso = peggio)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import TwoSlopeNorm

    tabs = [(prezzo[prezzo["h"] == 5], "CRPS/RW", "Prezzo h=5: CRPS / RW", [*models, *PRICE_BENCH]),
            (rend[rend["alpha"] == 0.10], "pinball/SS", "Rendimento: pinball / SS", [*models, *GARCH_SPECS]),
            (vol[vol["h"] == 5], "QLIKE/HAR", "Volatilita' h=5: QLIKE / HAR", [*models, "Media 22g"])]
    fig, axes = plt.subplots(1, 3, figsize=(17, 0.42 * len(ASSETS) + 2))
    for ax, (d, col, ttl, ms) in zip(axes, tabs):
        piv = d.pivot_table(index="asset", columns="modello", values=col).reindex(
            index=[a for a in ASSETS if a in set(d["asset"])], columns=[m for m in ms if m in set(d["modello"])])
        lo, hi = np.nanmin(piv.values), np.nanmax(piv.values)
        span = max(1 - lo, hi - 1, 0.02)
        im = ax.imshow(piv.values, cmap="RdBu_r", norm=TwoSlopeNorm(1.0, 1 - span, 1 + span), aspect="auto")
        ax.set_xticks(range(piv.shape[1]), piv.columns, rotation=20, fontsize=8)
        ax.set_yticks(range(piv.shape[0]), [f"{a} ({ALL_ASSETS[a][1]})" for a in piv.index], fontsize=8)
        for i in range(piv.shape[0]):
            for j in range(piv.shape[1]):
                v = piv.values[i, j]
                if np.isfinite(v):
                    ax.text(j, i, f"{v:.3f}", ha="center", va="center", fontsize=7)
        ax.set_title(ttl, fontsize=10)
        fig.colorbar(im, ax=ax, fraction=0.04)
    fig.tight_layout()
    fig.savefig(RIS / "heatmap_asset.png", dpi=130)
    plt.close(fig)


# ======================================================================================
# MAIN
# ======================================================================================

def setup_asset(asset: str, test_start: str, contesto: int, passo: int) -> tuple:
    """Dati, origini di previsione e compiti di un asset (la volatilita' solo con OHLC affidabili)."""
    df = load_asset(asset)
    o0 = int(np.searchsorted(df.index, pd.Timestamp(test_start)))
    origins = np.arange(max(o0, contesto), len(df), passo)
    ohlc_ok = float(np.isfinite(df["var_gk"].to_numpy()[origins]).mean())
    tasks = ["prezzo", "rendimento"] + (["volatilita"] if ohlc_ok >= MIN_OHLC else [])
    return df, origins, tasks, ohlc_ok


def solo_previsioni(assets: list[str], modelli: list[str], test_start: str, contesto: int, passo: int,
                    device: str) -> None:
    """Calcola soltanto le previsioni dei foundation model (in cache), senza benchmark ne' valutazione: e' la
    parte che serve la GPU (Colab); la valutazione si fa poi sul PC con --solo-valuta."""
    scarica(assets)
    tag = f"{test_start}_c{contesto}_p{passo}"
    for asset in assets:
        df, origins, tasks, _ = setup_asset(asset, test_start, contesto, passo)
        print(f"\n## {asset}: {len(origins)} origini, compiti {', '.join(tasks)}")
        for task in tasks:
            x = model_input(df, task)
            for m in modelli:
                get_forecasts(m, asset, task, x, origins, contesto, device, tag)


def run_experiment(assets: list[str], modelli: list[str], test_start: str = "2024-01-01", contesto: int = CONTESTO,
                   passo: int = 1, device: str = "cpu", solo_valuta: bool = False) -> dict:
    """Previsioni (in cache) e valutazione di tutti i compiti; ritorna tabelle e perdite per previsione."""
    scarica(assets)
    tag = f"{test_start}_c{contesto}_p{passo}"
    btag = f"{test_start}_p{passo}"  # i benchmark classici non dipendono dal contesto

    rows_p, rows_r, rows_v, var_paths, vol_paths, all_losses, regimes = [], [], [], {}, {}, {}, {}
    models: list[str] = []
    for asset in assets:
        df, origins, tasks, ohlc_ok = setup_asset(asset, test_start, contesto, passo)
        print(f"\n## {asset} ({ALL_ASSETS[asset][1]}): {len(df)} giorni, test dal {df.index[origins[0]]:%Y-%m-%d} "
              f"al {df.index[-1]:%Y-%m-%d}, {len(origins)} origini"
              + ("" if "volatilita" in tasks else f"; volatilita' esclusa (OHLC validi solo {ohlc_ok:.0%})"))
        # regime: volatilita' dei rendimenti negli ultimi 22 giorni prima dell'origine, sopra/sotto la mediana del test
        trail = df["rendimento"].rolling(22, min_periods=15).std().shift(1).iloc[origins]
        regimes[asset] = pd.Series(np.where(trail > trail.median(), "vol alta", "vol bassa"), index=trail.index)
        fc = {}
        for task in tasks:
            x = model_input(df, task)
            for m in modelli:
                path = CACHE / f"{m}_{asset}_{task}_{tag}.npy"
                if solo_valuta and not path.exists():
                    continue
                fc[(m, task)] = get_forecasts(m, asset, task, x, origins, contesto, device, tag)
        ms = sorted({m for m, _ in fc}, key=FM_MODELS.index)
        models = sorted(set(models) | set(ms), key=FM_MODELS.index)
        p = df["prezzo"].ffill().to_numpy(float)
        bench_p = {b: bench_cached(b, asset, "prezzo", origins, btag, lambda b=b: stat_quantiles(b, p, origins))
                   for b in PRICE_BENCH}
        fc_p = {**{m: common(fc[(m, "prezzo")], levels_of(m)) for m in ms}, **bench_p}
        r, l = eval_prezzo(asset, df, origins, fc_p)
        rows_p += r
        all_losses.update({(asset, *k): v for k, v in l.items()})
        ret = df["rendimento"].to_numpy(float)
        garch = {g: bench_cached(g, asset, "rendimento", origins, btag,
                                 lambda g=g: garch_quantiles(ret, origins, GARCH_Q, spec=g)) for g in GARCH_SPECS}
        r, l, vp = eval_rendimento(asset, df, origins, {m: fc[(m, "rendimento")] for m in ms},
                                   {m: levels_of(m) for m in ms}, garch)
        rows_r += r
        var_paths[asset] = vp
        all_losses.update({(asset, *k): v for k, v in l.items()})
        if "volatilita" in tasks:
            r, l, pp = eval_vol(asset, df, origins, {m: common(fc[(m, "volatilita")], levels_of(m)) for m in ms})
            rows_v += r
            vol_paths[asset] = pp
            all_losses.update({(asset, *k): v for k, v in l.items()})

    prezzo, rend, vol = pd.DataFrame(rows_p), pd.DataFrame(rows_r), pd.DataFrame(rows_v)
    for d in (prezzo, rend, vol):
        if len(d):
            d.insert(1, "settore", d["asset"].map(lambda x: ALL_ASSETS[x][1]))
    return {"prezzo": prezzo, "rend": rend, "vol": vol, "all_losses": all_losses, "regimes": regimes,
            "models": models, "var_paths": var_paths, "vol_paths": vol_paths}


def summarize(prezzo: pd.DataFrame, rend: pd.DataFrame, vol: pd.DataFrame) -> tuple:
    """Riepiloghi: media geometrica dei punteggi relativi sugli asset e quante volte nel MCS."""
    s_p = prezzo.pivot_table(index="modello", columns="h", values="CRPS/RW", aggfunc=geo_mean)
    s_p.columns = [f"CRPS/RW h={c}" for c in s_p.columns]
    s_p["MAE/RW h=1"] = prezzo[prezzo["h"] == 1].groupby("modello")["MAE/RW"].apply(geo_mean)
    s_p["direzione h=1"] = prezzo[prezzo["h"] == 1].groupby("modello")["direzione"].mean()
    s_p["cop80"] = prezzo.groupby("modello")["cop80"].mean()
    s_p["cop80 RW"] = prezzo.groupby("modello")["cop80 RW"].mean()
    s_v = vol.pivot_table(index="modello", columns="h", values="QLIKE/HAR", aggfunc=geo_mean)
    s_v.columns = [f"QLIKE/HAR h={c}" for c in s_v.columns]
    s_v["volte in MCS"] = vol.groupby("modello")["in MCS"].apply(lambda s: f"{int(s.sum())}/{len(s)}")
    s_r = rend.groupby(["modello", "alpha"]).agg(
        violazioni=("violazioni", "mean"), kupiec_rifiuti=("Kupiec p", lambda s: f"{int((s < 0.05).sum())}/{len(s)}"),
        christoffersen_rifiuti=("Christoffersen p", lambda s: f"{int((s < 0.05).sum())}/{len(s)}"),
        pinball_SS=("pinball/SS", geo_mean)).reset_index().sort_values(["alpha", "modello"], ascending=[False, True])
    mcs_count = lambda s: f"{int(s.fillna(False).astype(bool).sum())}/{len(s)}"
    s_p["volte in MCS"] = prezzo.groupby("modello")["in MCS"].apply(mcs_count)
    s_r = s_r.merge(rend.groupby(["modello", "alpha"])["in MCS"].apply(mcs_count).rename("volte in MCS").reset_index(), on=["modello", "alpha"])
    return s_p, s_r, s_v


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modelli", nargs="*", default=FM_MODELS, choices=FM_MODELS)
    ap.add_argument("--asset", nargs="*", default=ASSETS, choices=list(ALL_ASSETS),
                    help="default: i 15 futures; le serie spot (es. 'WTI spot') vanno indicate esplicitamente")
    ap.add_argument("--test-start", default="2024-01-01")
    ap.add_argument("--contesto", type=int, default=CONTESTO, help="giorni di storico dati ai modelli")
    ap.add_argument("--passo", type=int, default=1, help="giorni tra due previsioni")
    ap.add_argument("--device", default=None)
    ap.add_argument("--batch", type=int, default=128, help="serie per passata del modello (su GPU grandi: 512-1024)")
    ap.add_argument("--solo-valuta", action="store_true", help="usa solo le previsioni gia' in cache")
    ap.add_argument("--solo-previsioni", action="store_true",
                    help="calcola solo le previsioni dei foundation model (per la GPU), senza valutazione")
    ap.add_argument("--cartella", help="sottocartella di risultati/ per l'output (default: contesto_N se N != 4096)")
    a = ap.parse_args()

    import torch

    global RIS, BATCH
    BATCH = a.batch
    sub = a.cartella or (f"contesto_{a.contesto}" if a.contesto != CONTESTO else None)
    if sub:
        RIS = RIS / sub
    device = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    if a.solo_previsioni:
        solo_previsioni(a.asset, a.modelli, a.test_start, a.contesto, a.passo, device)
        return
    RIS.mkdir(parents=True, exist_ok=True)
    res = run_experiment(a.asset, a.modelli, a.test_start, a.contesto, a.passo, device, a.solo_valuta)
    prezzo, rend, vol, models = res["prezzo"], res["rend"], res["vol"], res["models"]
    all_losses, regimes, var_paths, vol_paths = res["all_losses"], res["regimes"], res["var_paths"], res["vol_paths"]
    prezzo.to_csv(RIS / "prezzo.csv", index=False, float_format="%.4f")
    rend.to_csv(RIS / "rendimento_var.csv", index=False, float_format="%.4f")
    vol.to_csv(RIS / "volatilita.csv", index=False, float_format="%.4f")
    plots(prezzo, rend, vol, var_paths, vol_paths, models)
    plot_heatmap(prezzo, rend, vol, models)

    # riepiloghi: media geometrica dei punteggi relativi sugli asset
    s_p, s_r, s_v = summarize(prezzo, rend, vol)

    # sotto-periodi (anni), regimi di volatilita', settori
    long = long_losses(all_losses, regimes)
    by_year, by_regime, by_sector = rel_by(long, "anno"), rel_by(long, "regime"), rel_by(long, "settore")
    for d in (by_year, by_regime, by_sector):
        d.rename(columns={d.columns[3]: "gruppo"}, inplace=True)
    sub = pd.concat([by_year, by_regime], ignore_index=True)
    sub.to_csv(RIS / "sottoperiodi_regimi.csv", index=False, float_format="%.4f")
    by_sector.to_csv(RIS / "settori.csv", index=False, float_format="%.4f")
    plot_groups(sub, RIS / "sottoperiodi.png", models, "Per anno e per regime di volatilita' (media geometrica sugli asset)")
    plot_groups(by_sector, RIS / "settori.png", models, "Per settore (media geometrica sugli asset del settore)")
    sig = significance(prezzo, rend, vol)
    sig.to_csv(RIS / "significativita.csv", index=False)
    vs = significance_vs(all_losses, models)
    vs.to_csv(RIS / "contro_benchmark_classici.csv", index=False, float_format="%.4f")

    def focus_table(d: pd.DataFrame) -> str:
        out = []
        for task, h, ttl in FOCUS:
            x = d[(d["compito"] == task) & (d["h"] == h)]
            piv = x.pivot_table(index="modello", columns="gruppo", values="rel", aggfunc="first")
            wins = x.pivot_table(index="modello", columns="gruppo", values="vince", aggfunc="first")
            cols = list(dict.fromkeys(x["gruppo"]))
            t = pd.DataFrame({c: [f"{piv.loc[m, c]:.3f} ({wins.loc[m, c]})" for m in piv.index] for c in cols},
                             index=piv.index).reset_index()
            out.append(f"**{ttl}**\n\n" + md_table(t))
        return "\n\n".join(out)

    with open(RIS / "report.md", "w", encoding="utf-8") as f:
        f.write(f"# Pilota: foundation model contro benchmark classici sulle commodities\n\n"
                f"{len(a.asset)} commodities: {', '.join(a.asset)}. Test dal {a.test_start}, una previsione ogni "
                f"{a.passo} giorni, contesto {a.contesto} giorni. Valori < 1 = meglio del benchmark (media geometrica "
                f"sugli asset). Tra parentesi: su quanti asset il modello batte il benchmark.\n\n")
        f.write("## Prezzo (benchmark: random walk)\n\n" + md_table(s_p.reset_index()) + "\n\n")
        f.write("## Rendimento: VaR e distribuzione (benchmark: simulazione storica)\n\n" + md_table(s_r) + "\n\n")
        f.write("## Volatilita' (benchmark: HAR-RV)\n\n" + md_table(s_v.reset_index()) + "\n\n")
        f.write("## Significativita' (Diebold-Mariano, Benjamini-Hochberg al 10% sugli asset)\n\n"
                + md_table(sig) + "\n\n")
        f.write("## Foundation model contro i benchmark classici\n\nRapporto tra le perdite (CRPS sul prezzo, pinball "
                "sul rendimento; < 1 = meglio il foundation model), media geometrica sugli asset; asset con differenza "
                "significativa secondo Diebold-Mariano con Benjamini-Hochberg al 10%.\n\n" + md_table(vs) + "\n\n")
        f.write("## Per anno e regime di volatilita'\n\n" + focus_table(sub) + "\n\n")
        f.write("## Per settore\n\n" + focus_table(by_sector) + "\n\n")
        f.write("## Dettaglio per asset\n\n### Prezzo\n\n" + md_table(prezzo) + "\n\n### VaR\n\n" + md_table(rend)
                + "\n\n### Volatilita'\n\n" + md_table(vol) + "\n")
    pd.set_option("display.width", 220)
    pd.set_option("display.max_columns", 30)
    print("\n=== PREZZO ===\n", s_p.round(3).to_string())
    print("\n=== RENDIMENTO / VaR ===\n", s_r.round(3).to_string(index=False))
    print("\n=== VOLATILITA' (QLIKE / HAR) ===\n", s_v.round(3).to_string())
    print("\n=== SIGNIFICATIVITA' ===\n", sig.to_string(index=False))
    print("\n=== CONTRO I BENCHMARK CLASSICI ===\n", vs.round(3).to_string(index=False))
    print("\n=== PER ANNO E REGIME (focus) ===\n" + focus_table(sub))
    print("\n=== PER SETTORE (focus) ===\n" + focus_table(by_sector))
    print(f"\nReport: {RIS / 'report.md'}")


if __name__ == "__main__":
    main()
