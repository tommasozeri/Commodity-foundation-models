"""Two WTI checks cited in the paper (Section 5.1 and Section 5.5).

1. Chronos-2 median vs last price for different context lengths (runs Chronos-2 on CPU on 60 origins).
2. Five-day volatility forecasts in a calm period (2024) and during the spring-2026 spike: QLIKE and the ratio
   between the average forecast and the average realized variance, for Timestral-209M with and without the OVX,
   HAR and log-HAR-X.

    python pilota/analisi_wti.py
"""

import numpy as np
import torch

import covariate as C
import pilota as P
import vol_implicita as V

TAG = "2024-01-01_c4096_p1"


def chronos_contesto() -> None:
    from chronos import Chronos2Pipeline

    pipe = Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map="cpu")
    df, orig, _, _ = P.setup_asset("WTI", "2024-01-01", 4096, 1)
    x = P.model_input(df, "prezzo")
    o = orig[::12][:60]
    print("Chronos-2, WTI, 60 origins: mean |median - last price| and MAE of the median vs random walk")
    for ctx in (4096, 2048, 1024, 512, 256):
        X = np.stack([x[i - ctx: i] for i in o])[:, None, :]
        with torch.no_grad():
            r = pipe.predict(X, prediction_length=1, batch_size=len(o))
        med = np.array([t[0, 10, 0].item() for t in r])  # quantile 0.5 is the 11th of 21
        print(f"  context {ctx:5d}: |median-last| {np.abs(med - x[o - 1]).mean():.3f}  "
              f"MAE {np.abs(med - x[o]).mean():.3f}  MAE RW {np.abs(x[o - 1] - x[o]).mean():.3f}")


def regimi_volatilita(h: int = 5) -> None:
    df, orig, _, _ = P.setup_asset("WTI", "2024-01-01", 4096, 1)
    v = df["var_gk"].to_numpy(float)
    o = orig[orig + h <= len(v)]
    real = np.array([np.nanmean(v[i: i + h]) for i in o])
    ok = np.isfinite(real)
    o, real = o[ok], real[ok]
    sel = np.searchsorted(orig, o)

    def fm(path):
        q = P.common(np.load(path), P.levels_of("Timestral-209M"))[sel, :h]
        return np.mean((np.maximum(q, 1e-3) / 100) ** 2 / 252, axis=(1, 2))

    ovx = V.serie_indice("OVX", df.index).astype(float) ** 2 / 252 / 1e4
    pred = {"Timestral-209M": fm(P.CACHE / f"Timestral-209M_WTI_volatilita_{TAG}.npy"),
            "Timestral-209M + OVX": fm(P.CACHE / f"Timestral-209M_WTI_volatilita_iv-Propria_{TAG}.npy"),
            "HAR": P.har_forecast(v, o, h), "log-HAR-X (OVX)": C.loghar_forecast(v, ovx, o, h)}
    d = df.index[o]
    periodi = {"calm (2024)": d < "2025-01-01", "spike (Mar-May 2026)": (d >= "2026-03-01") & (d < "2026-06-01"),
               "whole test period": np.ones(len(d), bool)}
    print(f"\nWTI, h={h}: mean QLIKE and mean forecast / mean realized variance")
    for nome, m in periodi.items():
        print(f"  {nome}")
        for k, p in pred.items():
            ql = real / p - np.log(real / p) - 1
            print(f"    {k:22s} QLIKE {ql[m].mean():.3f}   bias {p[m].mean() / real[m].mean():.2f}")


if __name__ == "__main__":
    regimi_volatilita()
    chronos_contesto()
