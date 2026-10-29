"""Controlli di robustezza del pilota.

1. SPOT vs FUTURES  ripete prezzo e VaR sui prezzi spot dell'energia (FRED/EIA: WTI Cushing, Brent Europa,
                    gasolio e benzina NY Harbor, gas Henry Hub), che non hanno salti da roll dei contratti,
                    e li confronta con i futures continui di Yahoo. Niente volatilita' (le spot hanno solo
                    la chiusura).
2. CONTESTO         stessi compiti sui 15 futures con contesto di 256, 512, 1024 e 4096 giorni, una
                    previsione ogni --passo giorni (default 5; il contesto 1024 riusa la cache giornaliera).
                    Modelli: Timestral-28M e TimesFM-3 (il 209M rende come il 28M nel pilota e costa 6x).

    python pilota/robustezza.py                   entrambi
    python pilota/robustezza.py --solo spot       solo il controllo spot (contesto 4096; --contesto per cambiarlo)
    python pilota/robustezza.py --solo contesto   solo la sensibilita' al contesto

Output in pilota/risultati/robustezza/: report_robustezza.md, CSV, contesto.png.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilota as P  # noqa: E402

OUT = P.RIS / "robustezza"
PAIRS = {"WTI": "WTI spot", "Brent": "Brent spot", "Gasolio": "Gasolio spot", "Benzina": "Benzina spot",
         "Gas naturale": "Gas naturale spot"}
CONTEXTS = (256, 512, 1024, 4096)


def key_metrics(prezzo: pd.DataFrame, rend: pd.DataFrame, vol: pd.DataFrame | None) -> pd.DataFrame:
    """Per asset e modello: CRPS/RW (h=1,5,20), pinball/SS, violazioni VaR 10%, QLIKE/HAR (h=1,5,20)."""
    p = prezzo[prezzo["modello"] != "Random walk"].pivot_table(index=["asset", "modello"], columns="h",
                                                              values="CRPS/RW")
    p.columns = [f"CRPS/RW h={h}" for h in p.columns]
    r = rend[rend["alpha"] == 0.10].set_index(["asset", "modello"])[["pinball/SS", "violazioni"]]
    r.columns = ["pinball/SS", "violazioni VaR10"]
    out = p.join(r, how="outer")
    if vol is not None and len(vol):
        v = vol.pivot_table(index=["asset", "modello"], columns="h", values="QLIKE/HAR")
        v.columns = [f"QLIKE/HAR h={h}" for h in v.columns]
        out = out.join(v, how="left")
    return out.reset_index()


def spot_vs_futures(device: str, contesto: int) -> str:
    print("\n########## SPOT vs FUTURES (energia) ##########")
    spot = P.run_experiment(list(PAIRS.values()), P.FM_MODELS, contesto=contesto, passo=1, device=device)
    fut = P.run_experiment(list(PAIRS), P.FM_MODELS, contesto=contesto, passo=1, device=device,
                           solo_valuta=True)
    ks = key_metrics(spot["prezzo"], spot["rend"], None)
    kf = key_metrics(fut["prezzo"], fut["rend"], None)
    kf["coppia"], ks["coppia"] = kf["asset"], ks["asset"].map({v: k for k, v in PAIRS.items()})
    cols = ["CRPS/RW h=1", "CRPS/RW h=5", "CRPS/RW h=20", "pinball/SS"]
    m = kf.merge(ks, on=["coppia", "modello"], suffixes=(" fut", " spot"))
    m = m[m["modello"].isin(P.FM_MODELS + ["GARCH-t"])]
    m.to_csv(OUT / "spot_vs_futures.csv", index=False, float_format="%.4f")

    # media geometrica sulle 5 coppie
    agg = pd.DataFrame({f"{c} {s}": m.groupby("modello")[f"{c} {s}"].apply(P.geo_mean)
                        for c in cols for s in ("fut", "spot")}).reset_index()
    sig_s = P.significance(spot["prezzo"], spot["rend"], spot["vol"])
    sig_f = P.significance(fut["prezzo"], fut["rend"], fut["vol"])
    sig = sig_f.merge(sig_s, on=["compito", "h", "modello"], suffixes=(" fut", " spot"))
    sig = sig[["compito", "h", "modello", "meglio (BH) fut", "meglio (BH) spot", "peggio (BH) fut", "peggio (BH) spot"]]
    det = m[["coppia", "modello"] + [f"{c} {s}" for c in cols for s in ("fut", "spot")]]
    print(agg.round(3).to_string(index=False))
    return ("## 1. Spot vs futures (energia, 5 coppie)\n\n"
            f"Stessi compiti e protocollo del pilota (contesto {contesto} giorni) sui prezzi spot FRED/EIA, che non "
            "hanno roll dei contratti. "
            "Valori < 1 = meglio del benchmark; media geometrica sulle 5 coppie.\n\n"
            + P.md_table(agg) + "\n\n**Asset con differenza significativa (DM + Benjamini-Hochberg al 10%, su 5)**\n\n"
            + P.md_table(sig) + "\n\n**Dettaglio per coppia**\n\n" + P.md_table(det) + "\n\n")


def context_sensitivity(device: str, passo: int) -> str:
    print("\n########## SENSIBILITA' AL CONTESTO ##########")
    models = ["Timestral-28M", "TimesFM-3"]
    rows = []
    for ctx in CONTEXTS:
        print(f"\n=== contesto {ctx} ===")
        res = P.run_experiment(P.ASSETS, models, contesto=ctx, passo=passo, device=device)
        k = key_metrics(res["prezzo"], res["rend"], res["vol"])
        k["contesto"] = ctx
        k["origini"] = res["prezzo"].groupby("asset")["n"].max().reindex(k["asset"]).to_numpy()
        rows.append(k)
    allk = pd.concat(rows, ignore_index=True)
    allk.to_csv(OUT / "contesto.csv", index=False, float_format="%.4f")
    metrics = ["CRPS/RW h=1", "CRPS/RW h=5", "CRPS/RW h=20", "pinball/SS", "QLIKE/HAR h=1", "QLIKE/HAR h=5",
               "QLIKE/HAR h=20"]
    keep = allk[allk["modello"].isin(models + ["GARCH-t", "Media 22g"])]
    agg = keep.groupby(["modello", "contesto"])[metrics].agg(P.geo_mean).reset_index()
    agg = agg[agg["modello"].isin(models)]
    print(agg.round(3).to_string(index=False))
    plot_context(agg, metrics)
    return ("## 2. Sensibilita' alla lunghezza del contesto (15 futures)\n\n"
            f"Contesto di 256, 512, 1024 e 4096 giorni, una previsione ogni {passo} giorni dal 2024. Valori < 1 = "
            "meglio del benchmark (media geometrica sugli asset). Con 4096 giorni il Brent (dati dal 07/2007) perde "
            "le prime ~15 origini del test.\n\n" + P.md_table(agg) + "\n\n![contesto](contesto.png)\n\n")


def plot_context(agg: pd.DataFrame, metrics: list[str]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = {"Timestral-28M": "#1f618d", "TimesFM-3": "#d35400"}
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.3))
    groups = [("Prezzo: CRPS / random walk", [m for m in metrics if m.startswith("CRPS")]),
              ("Rendimento: pinball / sim. storica", ["pinball/SS"]),
              ("Volatilita': QLIKE / HAR", [m for m in metrics if m.startswith("QLIKE")])]
    styles = ["-", "--", ":"]
    for ax, (title, ms) in zip(axes, groups):
        for model, d in agg.groupby("modello"):
            for st, metric in zip(styles, ms):
                ax.plot(d["contesto"], d[metric], marker="o", ls=st, color=colors.get(model),
                        label=f"{model} {metric.split(' ')[-1] if '=' in metric else ''}".strip())
        ax.axhline(1, color="k", lw=0.8)
        ax.set_xscale("log", base=2)
        ax.set_xticks(CONTEXTS, [str(c) for c in CONTEXTS])
        ax.set_xlabel("contesto (giorni)")
        ax.set_title(title, fontsize=10)
        ax.legend(fontsize=7)
    axes[0].set_ylabel("< 1 = meglio del benchmark")
    fig.tight_layout()
    fig.savefig(OUT / "contesto.png", dpi=130)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--solo", choices=["spot", "contesto"])
    ap.add_argument("--passo", type=int, default=5, help="giorni tra due previsioni nella sensibilita' al contesto")
    ap.add_argument("--device", default=None)
    ap.add_argument("--contesto", type=int, default=P.CONTESTO, help="contesto del controllo spot")
    a = ap.parse_args()
    import torch

    device = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    OUT.mkdir(parents=True, exist_ok=True)
    parts = ["# Controlli di robustezza del pilota\n\n"]
    if a.solo in (None, "spot"):
        parts.append(spot_vs_futures(device, a.contesto))
    if a.solo in (None, "contesto"):
        parts.append(context_sensitivity(device, a.passo))
    name = "report_robustezza.md" if a.solo is None else f"report_robustezza_{a.solo}.md"
    (OUT / name).write_text("".join(parts), encoding="utf-8")
    print(f"\nReport: {OUT / name}")


if __name__ == "__main__":
    main()
