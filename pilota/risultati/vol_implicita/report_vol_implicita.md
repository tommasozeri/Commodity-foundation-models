# Volatilita' implicita come covariata

Stessi compiti, origini (dal 2024) e contesto (4096 giorni) del pilota. Ogni foundation model riceve come past covariate un indice CBOE di volatilita' implicita, allineato al calendario della commodity. VIX su tutte le commodities; volatilita' implicita propria (OVX per WTI, Brent, Gasolio, Benzina; GVZ per Oro e Argento) dove esiste. HAR-X: l'HAR con la varianza implicita dell'indice come regressore, confrontato con l'HAR. Log-HAR-X: la stessa regressione in logaritmi (previsione exp(fit + s2/2)), confrontata con il Log-HAR senza indice.

Rapporto = perdita con la covariata / perdita dello stesso modello senza (pinball sul rendimento, QLIKE sulla volatilita'); media geometrica sugli asset. Significativita': Diebold-Mariano con Benjamini-Hochberg al 10% sugli asset.

## Volatilita'

**h = 1**

| modello | covariata | asset | rapporto | migliora su | meglio (BH) | peggio (BH) |
|---|---|---|---|---|---|---|
| Timestral-28M | Propria | 5 | 0.863 | 5/5 | 5 | 0 |
| Timestral-209M | Propria | 5 | 0.885 | 5/5 | 5 | 0 |
| TimesFM-3 | Propria | 5 | 0.926 | 5/5 | 5 | 0 |
| Chronos-2 | Propria | 5 | 0.941 | 5/5 | 5 | 0 |
| HAR-X | Propria | 5 | 1.145 | 1/5 | 1 | 4 |
| Log-HAR-X | Propria | 5 | 0.907 | 5/5 | 4 | 0 |
| Timestral-28M | VIX | 12 | 0.983 | 10/12 | 0 | 0 |
| Timestral-209M | VIX | 12 | 0.984 | 10/12 | 0 | 0 |
| TimesFM-3 | VIX | 12 | 0.991 | 10/12 | 2 | 0 |
| Chronos-2 | VIX | 12 | 1.013 | 3/12 | 0 | 2 |
| HAR-X | VIX | 12 | 1.020 | 5/12 | 0 | 0 |
| Log-HAR-X | VIX | 12 | 0.988 | 9/12 | 2 | 0 |

**h = 5**

| modello | covariata | asset | rapporto | migliora su | meglio (BH) | peggio (BH) |
|---|---|---|---|---|---|---|
| Timestral-28M | Propria | 5 | 0.750 | 5/5 | 5 | 0 |
| Timestral-209M | Propria | 5 | 0.785 | 5/5 | 5 | 0 |
| TimesFM-3 | Propria | 5 | 0.844 | 5/5 | 2 | 0 |
| Chronos-2 | Propria | 5 | 0.902 | 5/5 | 5 | 0 |
| HAR-X | Propria | 5 | 0.950 | 4/5 | 0 | 0 |
| Log-HAR-X | Propria | 5 | 0.840 | 5/5 | 3 | 0 |
| Timestral-28M | VIX | 12 | 0.995 | 8/12 | 0 | 0 |
| Timestral-209M | VIX | 12 | 0.997 | 7/12 | 0 | 0 |
| TimesFM-3 | VIX | 12 | 0.988 | 10/12 | 0 | 0 |
| Chronos-2 | VIX | 12 | 1.053 | 0/12 | 0 | 5 |
| HAR-X | VIX | 12 | 1.041 | 3/12 | 0 | 0 |
| Log-HAR-X | VIX | 12 | 1.010 | 7/12 | 0 | 0 |

**h = 20**

| modello | covariata | asset | rapporto | migliora su | meglio (BH) | peggio (BH) |
|---|---|---|---|---|---|---|
| Timestral-28M | Propria | 5 | 0.803 | 5/5 | 0 | 0 |
| Timestral-209M | Propria | 5 | 0.791 | 5/5 | 0 | 0 |
| TimesFM-3 | Propria | 5 | 0.867 | 5/5 | 0 | 0 |
| Chronos-2 | Propria | 5 | 0.909 | 5/5 | 0 | 0 |
| HAR-X | Propria | 5 | 0.864 | 4/5 | 0 | 0 |
| Log-HAR-X | Propria | 5 | 0.857 | 4/5 | 0 | 0 |
| Timestral-28M | VIX | 12 | 1.008 | 7/12 | 0 | 0 |
| Timestral-209M | VIX | 12 | 0.996 | 7/12 | 0 | 0 |
| TimesFM-3 | VIX | 12 | 0.988 | 8/12 | 0 | 0 |
| Chronos-2 | VIX | 12 | 1.058 | 2/12 | 0 | 4 |
| HAR-X | VIX | 12 | 1.034 | 3/12 | 0 | 0 |
| Log-HAR-X | VIX | 12 | 1.032 | 6/12 | 0 | 0 |

## Rendimento (pinball sui decili)

| modello | covariata | asset | rapporto | migliora su | meglio (BH) | peggio (BH) |
|---|---|---|---|---|---|---|
| Timestral-28M | Propria | 6 | 0.998 | 5/6 | 0 | 1 |
| Timestral-209M | Propria | 6 | 0.998 | 5/6 | 0 | 0 |
| TimesFM-3 | Propria | 6 | 0.997 | 5/6 | 0 | 0 |
| Chronos-2 | Propria | 6 | 0.997 | 6/6 | 0 | 0 |
| Timestral-28M | VIX | 15 | 1.000 | 9/15 | 0 | 0 |
| Timestral-209M | VIX | 15 | 1.000 | 10/15 | 0 | 0 |
| TimesFM-3 | VIX | 15 | 1.000 | 9/15 | 0 | 0 |
| Chronos-2 | VIX | 15 | 1.000 | 9/15 | 0 | 0 |

## Punteggi rispetto ai benchmark del pilota

Tick loss / simulazione storica per il VaR, QLIKE / HAR per la volatilita'; media geometrica sugli asset che hanno la covariata.

| asset con la covariata | modello | VaR 10% | VaR 1% | volatilita h=1 | volatilita h=5 | volatilita h=20 |
|---|---|---|---|---|---|---|
| VIX | Timestral-28M | 0.966 | 0.862 | 1.025 | 1.038 | 1.043 |
| VIX | Timestral-28M + VIX | 0.965 | 0.858 | 1.007 | 1.032 | 1.051 |
| VIX | Timestral-209M | 0.966 | 0.866 | 1.013 | 1.021 | 1.050 |
| VIX | Timestral-209M + VIX | 0.965 | 0.860 | 0.997 | 1.018 | 1.046 |
| VIX | TimesFM-3 | 0.971 |  | 1.004 | 1.024 | 1.060 |
| VIX | TimesFM-3 + VIX | 0.968 |  | 0.995 | 1.011 | 1.047 |
| VIX | Chronos-2 | 0.977 | 0.884 | 1.029 | 1.069 | 1.085 |
| VIX | Chronos-2 + VIX | 0.974 | 0.881 | 1.042 | 1.126 | 1.148 |
| VIX | HAR-X + VIX |  |  | 1.020 | 1.041 | 1.034 |
| VIX | Log-HAR |  |  | 1.022 | 0.998 | 0.988 |
| VIX | Log-HAR-X + VIX |  |  | 1.010 | 1.008 | 1.020 |
| VIX | GARCH-t | 0.972 | 0.885 |  |  |  |
| VIX | EGARCH-t | 0.971 | 0.906 |  |  |  |
| Propria | Timestral-28M | 0.946 | 0.785 | 1.046 | 1.138 | 1.231 |
| Propria | Timestral-28M + Propria | 0.940 | 0.730 | 0.903 | 0.853 | 0.988 |
| Propria | Timestral-209M | 0.945 | 0.783 | 1.023 | 1.108 | 1.212 |
| Propria | Timestral-209M + Propria | 0.938 | 0.739 | 0.905 | 0.870 | 0.959 |
| Propria | TimesFM-3 | 0.956 |  | 1.010 | 1.121 | 1.234 |
| Propria | TimesFM-3 + Propria | 0.947 |  | 0.935 | 0.947 | 1.069 |
| Propria | Chronos-2 | 0.958 | 0.810 | 1.034 | 1.157 | 1.221 |
| Propria | Chronos-2 + Propria | 0.952 | 0.770 | 0.973 | 1.044 | 1.110 |
| Propria | HAR-X + Propria |  |  | 1.145 | 0.950 | 0.864 |
| Propria | Log-HAR |  |  | 1.059 | 1.006 | 0.983 |
| Propria | Log-HAR-X + Propria |  |  | 0.961 | 0.846 | 0.842 |
| Propria | GARCH-t | 0.946 | 0.809 |  |  |  |
| Propria | EGARCH-t | 0.948 | 0.845 |  |  |  |

## Dettaglio per asset (volatilita' h=1)

| asset | indice | Timestral-28M | Timestral-209M | TimesFM-3 | Chronos-2 | HAR-X | Log-HAR-X |
|---|---|---|---|---|---|---|---|
| WTI | VIX | 0.944 | 0.961 | 0.985 | 1.010 | 1.027 | 0.989 |
| WTI | OVX | 0.849 | 0.879 | 0.934 | 0.951 | 1.299 | 0.862 |
| Brent | VIX | 0.937 | 0.948 | 0.978 | 1.011 | 1.027 | 0.984 |
| Brent | OVX | 0.836 | 0.851 | 0.914 | 0.942 | 1.273 | 0.932 |
| Gasolio | VIX | 0.956 | 0.969 | 0.984 | 0.988 | 0.998 | 1.000 |
| Gasolio | OVX | 0.888 | 0.911 | 0.937 | 0.940 | 0.953 | 0.924 |
| Benzina | VIX | 0.967 | 0.977 | 0.988 | 1.014 | 1.082 | 0.975 |
| Benzina | OVX | 0.860 | 0.878 | 0.906 | 0.959 | 1.177 | 0.909 |
| Gas naturale | VIX | 0.986 | 0.999 | 1.006 | 1.034 | 1.003 | 1.009 |
| Oro | VIX | 0.995 | 1.007 | 0.990 | 0.999 | 1.044 | 0.907 |
| Oro | GVZ | 0.885 | 0.905 | 0.937 | 0.912 | 1.059 | 0.909 |
| Rame | VIX | 1.039 | 0.980 | 0.987 | 1.034 | 1.065 | 1.006 |
| Grano | VIX | 0.991 | 0.989 | 0.998 | 1.001 | 0.999 | 0.997 |
| Mais | VIX | 0.998 | 0.992 | 0.990 | 1.039 | 1.007 | 1.001 |
| Soia | VIX | 0.992 | 0.993 | 0.992 | 0.994 | 0.999 | 0.999 |
| Zucchero | VIX | 1.001 | 1.002 | 0.998 | 1.016 | 0.999 | 0.998 |
| Bestiame | VIX | 0.996 | 0.994 | 1.001 | 1.016 | 0.999 | 0.999 |
