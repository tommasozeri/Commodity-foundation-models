# Pilota: contesto 1024 contro 4096

Stessi 15 asset, 3 foundation model e origini giornaliere dal 2024 (calcolo a 4096 su GPU A100). Rapporti < 1 = meglio del benchmark, media geometrica sugli asset. *4096/1024* < 1 = il contesto lungo migliora. Con 4096 giorni il Brent (dati dal 07/2007) perde le prime 15 origini.

## Prezzo (CRPS / random walk)

| modello | h | CRPS/RW 1024 | CRPS/RW 4096 | 4096/1024 | asset migliorati | in MCS 1024 | in MCS 4096 |
|---|---|---|---|---|---|---|---|
| TimesFM-3 | 1 | 0.986 | 0.985 | 1.000 | 8/15 | 11/15 | 12/15 |
| TimesFM-3 | 5 | 0.985 | 0.979 | 0.994 | 9/15 | 12/15 | 11/15 |
| TimesFM-3 | 20 | 0.988 | 0.960 | 0.972 | 13/15 | 15/15 | 12/15 |
| Timestral-209M | 1 | 0.979 | 0.978 | 0.999 | 10/15 | 15/15 | 15/15 |
| Timestral-209M | 5 | 0.974 | 0.972 | 0.998 | 9/15 | 15/15 | 15/15 |
| Timestral-209M | 20 | 0.965 | 0.958 | 0.993 | 13/15 | 14/15 | 14/15 |
| Timestral-28M | 1 | 0.981 | 0.981 | 1.000 | 5/15 | 14/15 | 13/15 |
| Timestral-28M | 5 | 0.977 | 0.976 | 0.998 | 9/15 | 15/15 | 11/15 |
| Timestral-28M | 20 | 0.968 | 0.962 | 0.993 | 10/15 | 13/15 | 14/15 |

## Rendimento (pinball sui decili / simulazione storica)

| modello | pinball/SS 1024 | pinball/SS 4096 | 4096/1024 | asset migliorati | in MCS 1024 | in MCS 4096 |
|---|---|---|---|---|---|---|
| GARCH-t | 0.993 | 0.993 | 1.000 | 1/15 | 15/15 | 13/15 |
| TimesFM-3 | 0.996 | 0.993 | 0.997 | 14/15 | 15/15 | 15/15 |
| Timestral-209M | 0.993 | 0.990 | 0.997 | 15/15 | 14/15 | 15/15 |
| Timestral-28M | 0.994 | 0.991 | 0.996 | 15/15 | 14/15 | 14/15 |

**VaR: violazioni medie e rifiuti di Kupiec (p < 0.05)**

| modello | alpha | violazioni 1024 | violazioni 4096 | Kupiec rifiuti 1024 | Kupiec rifiuti 4096 |
|---|---|---|---|---|---|
| TimesFM-3 | 0.100 | 0.095 | 0.095 | 0/15 | 1/15 |
| Timestral-209M | 0.010 | 0.011 | 0.010 | 2/15 | 1/15 |
| Timestral-209M | 0.050 | 0.047 | 0.045 | 2/15 | 2/15 |
| Timestral-209M | 0.100 | 0.097 | 0.094 | 1/15 | 2/15 |
| Timestral-28M | 0.010 | 0.011 | 0.011 | 1/15 | 1/15 |
| Timestral-28M | 0.050 | 0.045 | 0.045 | 2/15 | 2/15 |
| Timestral-28M | 0.100 | 0.090 | 0.092 | 3/15 | 1/15 |

## Volatilita' (QLIKE / HAR)

| modello | h | QLIKE/HAR 1024 | QLIKE/HAR 4096 | 4096/1024 | asset migliorati | in MCS 1024 | in MCS 4096 |
|---|---|---|---|---|---|---|---|
| TimesFM-3 | 1 | 1.025 | 1.004 | 0.979 | 10/12 | 12/12 | 12/12 |
| TimesFM-3 | 5 | 1.071 | 1.024 | 0.956 | 9/12 | 11/12 | 12/12 |
| TimesFM-3 | 20 | 1.152 | 1.060 | 0.920 | 12/12 | 11/12 | 12/12 |
| Timestral-209M | 1 | 1.031 | 1.013 | 0.982 | 10/12 | 12/12 | 11/12 |
| Timestral-209M | 5 | 1.057 | 1.021 | 0.966 | 10/12 | 12/12 | 12/12 |
| Timestral-209M | 20 | 1.125 | 1.050 | 0.933 | 10/12 | 11/12 | 11/12 |
| Timestral-28M | 1 | 1.034 | 1.025 | 0.991 | 6/12 | 11/12 | 11/12 |
| Timestral-28M | 5 | 1.062 | 1.038 | 0.977 | 6/12 | 11/12 | 11/12 |
| Timestral-28M | 20 | 1.129 | 1.043 | 0.924 | 9/12 | 10/12 | 11/12 |

## Asset significativamente migliori / peggiori del benchmark (DM + BH al 10%)

| compito | h | modello | meglio (BH) 1024 | meglio (BH) 4096 | peggio (BH) 1024 | peggio (BH) 4096 |
|---|---|---|---|---|---|---|
| prezzo | 1 | TimesFM-3 | 4 | 7 | 0 | 0 |
| prezzo | 1 | Timestral-209M | 10 | 12 | 0 | 0 |
| prezzo | 1 | Timestral-28M | 8 | 7 | 0 | 0 |
| prezzo | 5 | TimesFM-3 | 0 | 4 | 0 | 0 |
| prezzo | 5 | Timestral-209M | 8 | 8 | 0 | 0 |
| prezzo | 5 | Timestral-28M | 8 | 7 | 0 | 0 |
| prezzo | 20 | TimesFM-3 | 0 | 1 | 0 | 0 |
| prezzo | 20 | Timestral-209M | 0 | 0 | 0 | 0 |
| prezzo | 20 | Timestral-28M | 0 | 0 | 0 | 0 |
| rendimento | 1 | TimesFM-3 | 0 | 3 | 0 | 0 |
| rendimento | 1 | Timestral-209M | 3 | 7 | 0 | 0 |
| rendimento | 1 | Timestral-28M | 1 | 7 | 0 | 0 |
| volatilita | 1 | TimesFM-3 | 1 | 1 | 0 | 0 |
| volatilita | 1 | Timestral-209M | 1 | 0 | 0 | 0 |
| volatilita | 1 | Timestral-28M | 1 | 0 | 0 | 0 |
| volatilita | 5 | TimesFM-3 | 0 | 1 | 0 | 0 |
| volatilita | 5 | Timestral-209M | 0 | 0 | 0 | 0 |
| volatilita | 5 | Timestral-28M | 0 | 0 | 0 | 0 |
| volatilita | 20 | TimesFM-3 | 0 | 0 | 0 | 0 |
| volatilita | 20 | Timestral-209M | 0 | 0 | 0 | 0 |
| volatilita | 20 | Timestral-28M | 0 | 0 | 0 | 0 |
