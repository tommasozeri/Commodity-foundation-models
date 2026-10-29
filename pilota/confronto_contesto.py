"""Confronto del pilota principale tra contesto 1024 e 4096 (stessi asset, modelli e origini giornaliere).

Legge i CSV di pilota/risultati/contesto_1024/ e pilota/risultati/ (4096, specificazione principale) e scrive
pilota/risultati/confronto_1024_4096.md.

    python pilota/confronto_contesto.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilota as P  # noqa: E402

A, B = P.RIS / "contesto_1024", P.RIS
FM = ["Timestral-28M", "Timestral-209M", "TimesFM-3"]


def compare(name: str, key: list[str], metric: str, models: list[str]) -> pd.DataFrame:
    """Per modello e orizzonte: media geometrica a 1024 e 4096, rapporto 4096/1024, asset migliorati."""
    a, b = pd.read_csv(A / f"{name}.csv"), pd.read_csv(B / f"{name}.csv")
    m = a.merge(b, on=["asset", "modello"] + key, suffixes=(" 1024", " 4096"))
    m = m[m["modello"].isin(models)]
    g = m.groupby(["modello"] + key)
    out = pd.DataFrame({
        f"{metric} 1024": g[f"{metric} 1024"].apply(P.geo_mean),
        f"{metric} 4096": g[f"{metric} 4096"].apply(P.geo_mean),
        "asset migliorati": g.apply(lambda d: f"{(d[f'{metric} 4096'] < d[f'{metric} 1024']).sum()}/{len(d)}",
                                    include_groups=False),
        "in MCS 1024": g["in MCS 1024"].apply(lambda s: f"{s.sum()}/{len(s)}"),
        "in MCS 4096": g["in MCS 4096"].apply(lambda s: f"{s.sum()}/{len(s)}"),
    }).reset_index()
    out.insert(len(key) + 3, "4096/1024", out[f"{metric} 4096"] / out[f"{metric} 1024"])
    return out


def significance() -> pd.DataFrame:
    a, b = pd.read_csv(A / "significativita.csv"), pd.read_csv(B / "significativita.csv")
    m = a.merge(b, on=["compito", "h", "modello"], suffixes=(" 1024", " 4096"))
    m = m[m["modello"].isin(FM)]
    return m[["compito", "h", "modello", "meglio (BH) 1024", "meglio (BH) 4096", "peggio (BH) 1024",
              "peggio (BH) 4096"]]


def main() -> None:
    prezzo = compare("prezzo", ["h"], "CRPS/RW", FM)
    rend = compare("rendimento_var", ["alpha"], "pinball/SS", FM + ["GARCH-t"])
    rend = rend[rend["alpha"] == 0.10].drop(columns="alpha")  # pinball sui decili: uguale per ogni alpha
    var = pd.read_csv(B / "rendimento_var.csv").merge(pd.read_csv(A / "rendimento_var.csv"),
                                                     on=["asset", "modello", "alpha"], suffixes=(" 4096", " 1024"))
    var = var[var["modello"].isin(FM)].groupby(["modello", "alpha"]).agg(
        **{"violazioni 1024": ("violazioni 1024", "mean"), "violazioni 4096": ("violazioni 4096", "mean"),
           "Kupiec rifiuti 1024": ("Kupiec p 1024", lambda s: f"{(s < 0.05).sum()}/{len(s)}"),
           "Kupiec rifiuti 4096": ("Kupiec p 4096", lambda s: f"{(s < 0.05).sum()}/{len(s)}")}).reset_index()
    vol = compare("volatilita", ["h"], "QLIKE/HAR", FM)
    sig = significance()

    for t in (prezzo, rend, var, vol, sig):
        print(t.round(3).to_string(index=False), "\n")
    text = ("# Pilota: contesto 1024 contro 4096\n\n"
            "Stessi 15 asset, 3 foundation model e origini giornaliere dal 2024 (calcolo a 4096 su GPU A100). "
            "Rapporti < 1 = meglio del benchmark, media geometrica sugli asset. *4096/1024* < 1 = il contesto "
            "lungo migliora. Con 4096 giorni il Brent (dati dal 07/2007) perde le prime 15 origini.\n\n"
            "## Prezzo (CRPS / random walk)\n\n" + P.md_table(prezzo)
            + "\n\n## Rendimento (pinball sui decili / simulazione storica)\n\n" + P.md_table(rend)
            + "\n\n**VaR: violazioni medie e rifiuti di Kupiec (p < 0.05)**\n\n" + P.md_table(var)
            + "\n\n## Volatilita' (QLIKE / HAR)\n\n" + P.md_table(vol)
            + "\n\n## Asset significativamente migliori / peggiori del benchmark (DM + BH al 10%)\n\n"
            + P.md_table(sig) + "\n")
    out = B / "confronto_1024_4096.md"
    out.write_text(text, encoding="utf-8")
    print("Scritto", out)


if __name__ == "__main__":
    main()
