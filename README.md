# Time series foundation models for commodity futures: prices, risk and volatility

Code, data and results for the paper by Tommaso Zeri.
Paper: [tommasozeri.github.io/research/foundation-models-commodity-futures](https://tommasozeri.github.io/research/foundation-models-commodity-futures/)

Four time series foundation models (Timestral-28M, Timestral-209M, TimesFM-3, Chronos-2), used zero-shot, are
compared with econometric benchmarks on 15 commodity futures for three tasks: price distributions, one-day
Value-at-Risk and realized volatility, with daily forecasts from January 2024 to October 2026.

This repository contains the code, the downloaded data and the result files. The cached forecasts of the
foundation models and benchmarks (`pilota/cache/*.npy`, about 600 MB) are too large for git: download
`replication_package.zip` from the [Releases](../../releases) page and copy its `pilota/cache/` folder into
`pilota/`. With the cached forecasts, all results can be reproduced **on a CPU in about one hour**, without a
GPU and without downloading any model. Recomputing the foundation-model forecasts from scratch requires a GPU
(see Section 4).

## 1. Contents

```
pilota/
  pilota.py              main evaluation: price, return/VaR and volatility tasks, benchmarks, tests, MCS
  robustezza.py          robustness: spot vs futures, context length (256, 512, 1024, 4096)
  confronto_contesto.py  comparison of the 1024- and 4096-day contexts
  covariate.py           covariate experiment on WTI (Brent, dollar + OVX, inventories, all, placebo)
  vol_implicita.py       implied volatility (VIX, OVX, GVZ) as covariate on all commodities
  volatilita_extra.py    log-HAR benchmark and equal-weight combinations
  analisi_wti.py         two WTI checks cited in the text (Chronos-2 median; calm vs spike regimes)
  dati/                  downloaded data (CSV), see Section 3
  cache/                 cached forecasts (.npy), from the release, see Section 5
  risultati/             result files (CSV and Markdown reports) as produced for the paper
paper/
  figure.py              figures of the paper (`python paper/figure.py en`)
  appendice.py           appendix tables (`python paper/appendice.py en`)
Pilota_Colab.ipynb       notebook used to compute the foundation-model forecasts on a Colab A100 GPU
requirements.txt
```

Code comments, variable names and the names of the result files are in Italian. The mapping to the paper is
given below; the main terms are *prezzo* = price, *rendimento* = return, *volatilita* = volatility,
*contesto* = context length, *origini* = forecast origins, *risultati* = results, *covariate* = covariates,
*solo-valuta* = evaluate only (use cached forecasts), *solo-previsioni* = forecast only.

## 2. Software

Python 3.13 with the packages in `requirements.txt`. The results in the paper were obtained with:

| Package | Version |
|---|---|
| numpy / pandas / scipy | 2.5.4 / 2.3.3 / 1.18.1 |
| torch | 2.14.1 (CPU locally; CUDA on Colab) |
| arch | 8.0.0 |
| statsforecast | 2.1.1 |
| timestral | 1.0.0 (github.com/mistralai/timestral, commit a534bdb) |
| timesfm | 3.0.2 (github.com/google-research/timesfm, commit e51928e) |
| chronos-forecasting | 2.3.2 |
| transformers / huggingface-hub | 5.21.0 / 2.3.0 |

Model weights (Hugging Face revisions used locally):

| Model | Repository | Revision |
|---|---|---|
| Timestral-28M | `mistralai/Timestral-28M` | `49b26409ac87b5935539a5d8ffe7f397b720db47` |
| Timestral-209M | `mistralai/Timestral-209M` | `9874d252ab0aae16f7f7c999f98f98d6ad7d8365` |
| TimesFM-3 | `google/timesfm-3.0-pytorch` | `43046b85ec22d584a13f8098c2ed39c889e129c2` |
| Chronos-2 | `amazon/chronos-2` | `29ec3766d36d6f73f0696f85560a422f50e8498c` |

The TimesFM-3 weights are released under a non-commercial licence.

## 3. Data

All data are public and are included in `pilota/dati/` as downloaded (fixed end date 23 October 2026). If the
files are deleted, the scripts download them again, but values may differ slightly from those used in the paper.

| Files | Source |
|---|---|
| 15 futures (`WTI.csv`, ..., `Bestiame.csv`) | Yahoo Finance, continuous front-month (`CL=F`, `BZ=F`, `HO=F`, `RB=F`, `NG=F`, `GC=F`, `SI=F`, `HG=F`, `ZW=F`, `ZC=F`, `ZS=F`, `KC=F`, `SB=F`, `CC=F`, `LE=F`) |
| 5 spot series (`* spot.csv`) | FRED (EIA): `DCOILWTICO`, `DCOILBRENTEU`, `DHOILNYH`, `DGASNYH`, `DHHNGSP` |
| `DXY.csv`, `OVX.csv`, `GVZ.csv`, `VIX.csv` | Yahoo Finance: `DX-Y.NYB`, `^OVX`, `^GVZ`, `^VIX` |
| `Scorte EIA.csv` | EIA weekly US crude oil stocks excluding SPR (`WCESTUS1`), with the release date used |

Italian file names: Gasolio = heating oil, Benzina = gasoline, Gas naturale = natural gas, Oro = gold,
Argento = silver, Rame = copper, Grano = wheat, Mais = corn, Soia = soybeans, Caffe = coffee, Zucchero = sugar,
Cacao = cocoa, Bestiame = live cattle, Scorte = inventories.

## 4. Reproducing the results

Run all commands from the root of the package, in the order of the table: the figure and appendix scripts read
the result files written by the evaluation scripts. The package already ships these result files in
`pilota/risultati/`, so each script can also be run on its own. Running the evaluation scripts on the cached
forecasts reproduces the shipped result files exactly.

| Paper | Command | Output in `pilota/risultati/` |
|---|---|---|
| Tables 3–5, Figures 5–8 data, DM/BH tests, MCS, by year/regime/sector | `python pilota/pilota.py --solo-valuta` | `report.md`, `prezzo.csv`, `rendimento_var.csv`, `volatilita.csv`, `significativita.csv`, `contro_benchmark_classici.csv`, `sottoperiodi_regimi.csv`, `settori.csv` |
| Context 1024 (robustness) | `python pilota/pilota.py --contesto 1024 --solo-valuta` then `python pilota/confronto_contesto.py` | `contesto_1024/`, `confronto_1024_4096.md` |
| Context 256–4096, Figure 9 | `python pilota/robustezza.py --solo contesto` | `robustezza/` |
| Spot vs futures | `python pilota/robustezza.py --solo spot` | `robustezza/report_robustezza_spot.md` |
| Covariates on WTI | `python pilota/covariate.py --solo-valuta` | `covariate/` |
| Implied volatility, Tables 7–8, Figure 10 | `python pilota/vol_implicita.py --solo-valuta` | `vol_implicita/` |
| Log-HAR and combinations, Table 6 | `python pilota/volatilita_extra.py` | `volatilita_extra/` |
| Chronos-2 median by context (Section 5.1); calm vs spike regimes for WTI (discussion of Figure 11) | `python pilota/analisi_wti.py` | printed to screen |
| Figures | `python paper/figure.py en` | `paper_en/figures/` |
| Appendix tables | `python paper/appendice.py en` | `paper_en/appendix.tex` |

Table and figure numbers refer to the submitted manuscript. The benchmarks (ARIMA, ETS, GARCH family) are also
cached in `pilota/cache/bench_*.npy`; if these files are removed they are re-estimated on the CPU (about one hour).
The Model Confidence Set uses a fixed bootstrap seed.

**Recomputing the foundation-model forecasts.** Delete the corresponding `.npy` files in `pilota/cache/` and run
the scripts without `--solo-valuta`, or with `--solo-previsioni --device cuda` on a GPU. The 4096-day forecasts
in the paper were computed on an NVIDIA A100 with `Pilota_Colab.ipynb` (about 30–60 minutes per experiment).
Forecasts recomputed on a second GPU runtime differed by less than 1e-4 in price units for WTI.

## 5. Cached forecasts

File names follow `{model}_{asset}_{task}[_{experiment}]_{test start}_c{context}_p{step}.npy`, with
`task` in {`prezzo`, `rendimento`, `volatilita`}, `c` the context length and `p` the step between origins
(1 = daily). Experiment tags: `cov-{configuration}` (WTI covariates), `iv-VIX` and `iv-Propria` (implied
volatility: VIX and the commodity's own index). Each array has shape (origins, 20 horizons, quantiles): 21
quantiles (0.01, 0.05, 0.10, ..., 0.95, 0.99) for Timestral and Chronos-2, 9 deciles for TimesFM-3. Benchmark
files are `bench_{model}_{asset}_{task}_..._o{first origin}-{number of origins}.npy`.

## Citation

```bibtex
@report{zeri2026foundation,
  author = {Zeri, Tommaso},
  title  = {Time Series Foundation Models for Commodity Futures: Prices, Risk and Volatility},
  year   = {2026},
  url    = {https://tommasozeri.github.io/research/foundation-models-commodity-futures/}
}
```

## Licence

Code: MIT (see `LICENSE`). Data are redistributed from their public sources (Yahoo Finance, FRED, EIA) and remain
subject to their terms. The TimesFM-3 weights are released by Google under a non-commercial licence.
