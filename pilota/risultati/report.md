# Pilota: foundation model contro benchmark classici sulle commodities

15 commodities: WTI, Brent, Gasolio, Benzina, Gas naturale, Oro, Argento, Rame, Grano, Mais, Soia, Caffe, Zucchero, Cacao, Bestiame. Test dal 2024-01-01, una previsione ogni 1 giorni, contesto 4096 giorni. Valori < 1 = meglio del benchmark (media geometrica sugli asset). Tra parentesi: su quanti asset il modello batte il benchmark.

## Prezzo (benchmark: random walk)

| modello | CRPS/RW h=1 | CRPS/RW h=5 | CRPS/RW h=20 | MAE/RW h=1 | direzione h=1 | cop80 | cop80 RW | volte in MCS |
|---|---|---|---|---|---|---|---|---|
| ARIMA | 1.000 | 0.991 | 0.988 | 1.004 | 0.416 | 0.811 | 0.749 | 27/45 |
| Chronos-2 | 1.088 | 1.015 | 0.990 | 1.126 | 0.487 | 0.763 | 0.749 | 21/45 |
| ETS | 0.992 | 0.987 | 0.973 | 1.000 | 0.514 | 0.817 | 0.749 | 31/45 |
| Random walk | 1.000 | 1.000 | 1.000 | 1.000 |  | 0.749 |  | 24/45 |
| TimesFM-3 | 0.985 | 0.979 | 0.960 | 1.009 | 0.494 | 0.809 | 0.749 | 39/45 |
| Timestral-209M | 0.978 | 0.972 | 0.958 | 1.003 | 0.503 | 0.792 | 0.749 | 44/45 |
| Timestral-28M | 0.981 | 0.976 | 0.962 | 1.005 | 0.505 | 0.790 | 0.749 | 41/45 |

## Rendimento: VaR e distribuzione (benchmark: simulazione storica)

| modello | alpha | violazioni | kupiec_rifiuti | christoffersen_rifiuti | pinball_SS | volte in MCS |
|---|---|---|---|---|---|---|
| Chronos-2 | 0.100 | 0.096 | 1/15 | 0/15 | 0.992 | 13/15 |
| EGARCH-t | 0.100 | 0.097 | 1/15 | 0/15 | 0.991 | 14/15 |
| GARCH-t | 0.100 | 0.099 | 1/15 | 1/15 | 0.993 | 14/15 |
| GJR-GARCH-t | 0.100 | 0.100 | 1/15 | 0/15 | 0.993 | 14/15 |
| Simulazione storica | 0.100 | 0.107 | 1/15 | 0/15 | 1.000 | 13/15 |
| TimesFM-3 | 0.100 | 0.095 | 1/15 | 0/15 | 0.993 | 15/15 |
| Timestral-209M | 0.100 | 0.094 | 2/15 | 0/15 | 0.990 | 15/15 |
| Timestral-28M | 0.100 | 0.092 | 1/15 | 0/15 | 0.991 | 15/15 |
| Chronos-2 | 0.050 | 0.046 | 3/15 | 3/15 | 0.992 | 13/15 |
| EGARCH-t | 0.050 | 0.049 | 2/15 | 2/15 | 0.991 | 12/15 |
| GARCH-t | 0.050 | 0.050 | 1/15 | 1/15 | 0.993 | 12/15 |
| GJR-GARCH-t | 0.050 | 0.050 | 1/15 | 1/15 | 0.993 | 12/15 |
| Simulazione storica | 0.050 | 0.056 | 1/15 | 1/15 | 1.000 | 12/15 |
| Timestral-209M | 0.050 | 0.045 | 2/15 | 2/15 | 0.990 | 14/15 |
| Timestral-28M | 0.050 | 0.045 | 2/15 | 2/15 | 0.991 | 15/15 |
| Chronos-2 | 0.010 | 0.010 | 1/15 | 3/15 | 0.992 | 13/15 |
| EGARCH-t | 0.010 | 0.012 | 3/15 | 3/15 | 0.991 | 13/15 |
| GARCH-t | 0.010 | 0.011 | 1/15 | 2/15 | 0.993 | 12/15 |
| GJR-GARCH-t | 0.010 | 0.012 | 2/15 | 2/15 | 0.993 | 13/15 |
| Simulazione storica | 0.010 | 0.016 | 4/15 | 4/15 | 1.000 | 10/15 |
| Timestral-209M | 0.010 | 0.010 | 1/15 | 3/15 | 0.990 | 14/15 |
| Timestral-28M | 0.010 | 0.011 | 1/15 | 2/15 | 0.991 | 15/15 |

## Volatilita' (benchmark: HAR-RV)

| modello | QLIKE/HAR h=1 | QLIKE/HAR h=5 | QLIKE/HAR h=20 | volte in MCS |
|---|---|---|---|---|
| Chronos-2 | 1.029 | 1.069 | 1.085 | 27/36 |
| HAR | 1.000 | 1.000 | 1.000 | 34/36 |
| Media 22g | 1.171 | 1.192 | 1.188 | 23/36 |
| Random walk | 3.075 | 5.332 | 10.228 | 6/36 |
| TimesFM-3 | 1.004 | 1.024 | 1.060 | 36/36 |
| Timestral-209M | 1.013 | 1.021 | 1.050 | 35/36 |
| Timestral-28M | 1.025 | 1.038 | 1.043 | 34/36 |

## Significativita' (Diebold-Mariano, Benjamini-Hochberg al 10% sugli asset)

| compito | h | modello | asset | meglio (BH) | peggio (BH) | p<0.05 senza correzione |
|---|---|---|---|---|---|---|
| prezzo | 1 | ARIMA | 15 | 2 | 2 | 5 |
| prezzo | 1 | Chronos-2 | 15 | 0 | 10 | 10 |
| prezzo | 1 | ETS | 15 | 6 | 2 | 8 |
| prezzo | 1 | TimesFM-3 | 15 | 7 | 0 | 7 |
| prezzo | 1 | Timestral-209M | 15 | 12 | 0 | 12 |
| prezzo | 1 | Timestral-28M | 15 | 7 | 0 | 7 |
| prezzo | 5 | ARIMA | 15 | 0 | 0 | 3 |
| prezzo | 5 | Chronos-2 | 15 | 0 | 1 | 1 |
| prezzo | 5 | ETS | 15 | 2 | 0 | 3 |
| prezzo | 5 | TimesFM-3 | 15 | 4 | 0 | 5 |
| prezzo | 5 | Timestral-209M | 15 | 8 | 0 | 8 |
| prezzo | 5 | Timestral-28M | 15 | 7 | 0 | 7 |
| prezzo | 20 | ARIMA | 15 | 0 | 0 | 1 |
| prezzo | 20 | Chronos-2 | 15 | 0 | 0 | 2 |
| prezzo | 20 | ETS | 15 | 0 | 0 | 0 |
| prezzo | 20 | TimesFM-3 | 15 | 1 | 0 | 3 |
| prezzo | 20 | Timestral-209M | 15 | 0 | 0 | 3 |
| prezzo | 20 | Timestral-28M | 15 | 0 | 0 | 1 |
| rendimento | 1 | Chronos-2 | 15 | 7 | 0 | 7 |
| rendimento | 1 | EGARCH-t | 15 | 6 | 0 | 6 |
| rendimento | 1 | GARCH-t | 15 | 6 | 0 | 6 |
| rendimento | 1 | GJR-GARCH-t | 15 | 5 | 0 | 6 |
| rendimento | 1 | TimesFM-3 | 15 | 3 | 0 | 5 |
| rendimento | 1 | Timestral-209M | 15 | 7 | 0 | 7 |
| rendimento | 1 | Timestral-28M | 15 | 7 | 0 | 7 |
| volatilita | 1 | Chronos-2 | 12 | 0 | 0 | 1 |
| volatilita | 1 | Media 22g | 12 | 0 | 10 | 6 |
| volatilita | 1 | Random walk | 12 | 0 | 12 | 10 |
| volatilita | 1 | TimesFM-3 | 12 | 1 | 0 | 1 |
| volatilita | 1 | Timestral-209M | 12 | 0 | 0 | 1 |
| volatilita | 1 | Timestral-28M | 12 | 0 | 0 | 1 |
| volatilita | 5 | Chronos-2 | 12 | 0 | 0 | 0 |
| volatilita | 5 | Media 22g | 12 | 0 | 4 | 4 |
| volatilita | 5 | Random walk | 12 | 0 | 11 | 11 |
| volatilita | 5 | TimesFM-3 | 12 | 1 | 0 | 1 |
| volatilita | 5 | Timestral-209M | 12 | 0 | 0 | 1 |
| volatilita | 5 | Timestral-28M | 12 | 0 | 0 | 1 |
| volatilita | 20 | Chronos-2 | 12 | 0 | 0 | 0 |
| volatilita | 20 | Media 22g | 12 | 0 | 1 | 2 |
| volatilita | 20 | Random walk | 12 | 0 | 11 | 10 |
| volatilita | 20 | TimesFM-3 | 12 | 0 | 0 | 1 |
| volatilita | 20 | Timestral-209M | 12 | 0 | 0 | 1 |
| volatilita | 20 | Timestral-28M | 12 | 0 | 0 | 2 |

## Foundation model contro i benchmark classici

Rapporto tra le perdite (CRPS sul prezzo, pinball sul rendimento; < 1 = meglio il foundation model), media geometrica sugli asset; asset con differenza significativa secondo Diebold-Mariano con Benjamini-Hochberg al 10%.

| compito | h | modello | contro | rapporto | batte su | meglio (BH) | peggio (BH) |
|---|---|---|---|---|---|---|---|
| prezzo | 1 | Timestral-28M | ARIMA | 0.981 | 14/15 | 9 | 0 |
| prezzo | 1 | Timestral-209M | ARIMA | 0.978 | 15/15 | 11 | 0 |
| prezzo | 1 | TimesFM-3 | ARIMA | 0.986 | 12/15 | 5 | 0 |
| prezzo | 1 | Chronos-2 | ARIMA | 1.089 | 2/15 | 0 | 8 |
| prezzo | 5 | Timestral-28M | ARIMA | 0.984 | 12/15 | 5 | 0 |
| prezzo | 5 | Timestral-209M | ARIMA | 0.981 | 14/15 | 5 | 0 |
| prezzo | 5 | TimesFM-3 | ARIMA | 0.987 | 13/15 | 2 | 0 |
| prezzo | 5 | Chronos-2 | ARIMA | 1.023 | 4/15 | 0 | 2 |
| prezzo | 20 | Timestral-28M | ARIMA | 0.974 | 14/15 | 0 | 0 |
| prezzo | 20 | Timestral-209M | ARIMA | 0.970 | 13/15 | 2 | 0 |
| prezzo | 20 | TimesFM-3 | ARIMA | 0.972 | 12/15 | 1 | 0 |
| prezzo | 20 | Chronos-2 | ARIMA | 1.002 | 7/15 | 0 | 0 |
| prezzo | 1 | Timestral-28M | ETS | 0.989 | 13/15 | 6 | 0 |
| prezzo | 1 | Timestral-209M | ETS | 0.986 | 13/15 | 8 | 0 |
| prezzo | 1 | TimesFM-3 | ETS | 0.994 | 10/15 | 3 | 0 |
| prezzo | 1 | Chronos-2 | ETS | 1.098 | 1/15 | 0 | 9 |
| prezzo | 5 | Timestral-28M | ETS | 0.989 | 10/15 | 5 | 0 |
| prezzo | 5 | Timestral-209M | ETS | 0.985 | 12/15 | 5 | 0 |
| prezzo | 5 | TimesFM-3 | ETS | 0.992 | 10/15 | 2 | 0 |
| prezzo | 5 | Chronos-2 | ETS | 1.028 | 3/15 | 0 | 4 |
| prezzo | 20 | Timestral-28M | ETS | 0.989 | 10/15 | 0 | 0 |
| prezzo | 20 | Timestral-209M | ETS | 0.985 | 12/15 | 0 | 0 |
| prezzo | 20 | TimesFM-3 | ETS | 0.987 | 9/15 | 1 | 0 |
| prezzo | 20 | Chronos-2 | ETS | 1.017 | 5/15 | 1 | 1 |
| rendimento | 1 | Timestral-28M | GARCH-t | 0.998 | 9/15 | 2 | 0 |
| rendimento | 1 | Timestral-209M | GARCH-t | 0.997 | 11/15 | 3 | 0 |
| rendimento | 1 | TimesFM-3 | GARCH-t | 1.000 | 5/15 | 0 | 0 |
| rendimento | 1 | Chronos-2 | GARCH-t | 0.999 | 8/15 | 2 | 1 |
| rendimento | 1 | Timestral-28M | GJR-GARCH-t | 0.998 | 10/15 | 2 | 0 |
| rendimento | 1 | Timestral-209M | GJR-GARCH-t | 0.997 | 12/15 | 3 | 0 |
| rendimento | 1 | TimesFM-3 | GJR-GARCH-t | 1.000 | 5/15 | 0 | 0 |
| rendimento | 1 | Chronos-2 | GJR-GARCH-t | 0.999 | 6/15 | 2 | 0 |
| rendimento | 1 | Timestral-28M | EGARCH-t | 1.000 | 10/15 | 0 | 0 |
| rendimento | 1 | Timestral-209M | EGARCH-t | 0.999 | 13/15 | 0 | 0 |
| rendimento | 1 | TimesFM-3 | EGARCH-t | 1.002 | 2/15 | 0 | 0 |
| rendimento | 1 | Chronos-2 | EGARCH-t | 1.001 | 6/15 | 0 | 0 |

## Per anno e regime di volatilita'

**Prezzo h=5: CRPS / random walk**

| modello | 2024 | 2025 | 2026 | vol alta | vol bassa |
|---|---|---|---|---|---|
| ARIMA | 1.012 (6/15) | 0.994 (10/15) | 0.979 (11/15) | 0.987 (12/15) | 1.005 (7/15) |
| Chronos-2 | 1.023 (2/15) | 1.033 (5/15) | 0.993 (8/15) | 1.011 (6/15) | 1.026 (6/15) |
| ETS | 1.007 (5/15) | 0.992 (11/15) | 0.972 (13/15) | 0.980 (13/15) | 1.002 (7/15) |
| TimesFM-3 | 0.997 (8/15) | 0.999 (7/15) | 0.960 (12/15) | 0.972 (14/15) | 0.994 (12/15) |
| Timestral-209M | 0.989 (11/15) | 0.991 (12/15) | 0.953 (15/15) | 0.964 (14/15) | 0.991 (11/15) |
| Timestral-28M | 0.991 (12/15) | 0.993 (12/15) | 0.957 (15/15) | 0.968 (14/15) | 0.992 (10/15) |

**Rendimento: pinball / sim. storica**

| modello | 2024 | 2025 | 2026 | vol alta | vol bassa |
|---|---|---|---|---|---|
| Chronos-2 | 0.996 (10/15) | 0.999 (7/15) | 0.984 (13/15) | 0.989 (12/15) | 0.997 (12/15) |
| EGARCH-t | 0.994 (12/15) | 0.999 (9/15) | 0.983 (14/15) | 0.988 (13/15) | 0.997 (14/15) |
| GARCH-t | 0.996 (10/15) | 1.001 (8/15) | 0.986 (13/15) | 0.991 (11/15) | 0.997 (12/15) |
| GJR-GARCH-t | 0.996 (9/15) | 1.000 (9/15) | 0.986 (13/15) | 0.991 (10/15) | 0.997 (12/15) |
| TimesFM-3 | 0.996 (9/15) | 0.998 (10/15) | 0.988 (12/15) | 0.992 (11/15) | 0.996 (13/15) |
| Timestral-209M | 0.994 (11/15) | 0.996 (12/15) | 0.983 (14/15) | 0.986 (13/15) | 0.996 (13/15) |
| Timestral-28M | 0.994 (13/15) | 0.996 (14/15) | 0.984 (13/15) | 0.988 (14/15) | 0.995 (13/15) |

**Volatilita' h=5: QLIKE / HAR**

| modello | 2024 | 2025 | 2026 | vol alta | vol bassa |
|---|---|---|---|---|---|
| Chronos-2 | 0.871 (9/12) | 1.072 (3/12) | 1.182 (1/12) | 1.036 (6/12) | 1.083 (2/12) |
| Media 22g | 1.043 (5/12) | 1.156 (2/12) | 1.306 (0/12) | 1.199 (2/12) | 1.154 (1/12) |
| TimesFM-3 | 0.845 (9/12) | 1.025 (4/12) | 1.130 (3/12) | 0.993 (7/12) | 1.032 (3/12) |
| Timestral-209M | 0.830 (9/12) | 1.028 (4/12) | 1.123 (3/12) | 0.983 (7/12) | 1.038 (3/12) |
| Timestral-28M | 0.843 (9/12) | 1.043 (3/12) | 1.147 (2/12) | 1.009 (7/12) | 1.050 (3/12) |

## Per settore

**Prezzo h=5: CRPS / random walk**

| modello | Cereali | Energia | Metalli industriali | Metalli preziosi | Soft e bestiame |
|---|---|---|---|---|---|
| ARIMA | 1.008 (0/3) | 0.987 (4/5) | 0.998 (1/1) | 0.969 (2/2) | 0.995 (3/4) |
| Chronos-2 | 1.005 (1/3) | 0.988 (4/5) | 1.018 (0/1) | 1.107 (0/2) | 1.011 (1/4) |
| ETS | 1.001 (1/3) | 0.981 (5/5) | 1.005 (0/1) | 0.967 (2/2) | 0.989 (4/4) |
| TimesFM-3 | 0.983 (3/3) | 0.969 (5/5) | 1.009 (0/1) | 0.964 (2/2) | 0.988 (4/4) |
| Timestral-209M | 0.978 (3/3) | 0.962 (5/5) | 0.997 (1/1) | 0.956 (2/2) | 0.984 (3/4) |
| Timestral-28M | 0.979 (3/3) | 0.961 (5/5) | 1.006 (0/1) | 0.968 (2/2) | 0.987 (3/4) |

**Rendimento: pinball / sim. storica**

| modello | Cereali | Energia | Metalli industriali | Metalli preziosi | Soft e bestiame |
|---|---|---|---|---|---|
| Chronos-2 | 0.997 (2/3) | 0.987 (5/5) | 0.996 (1/1) | 0.986 (2/2) | 0.997 (2/4) |
| EGARCH-t | 0.997 (3/3) | 0.987 (5/5) | 0.997 (1/1) | 0.983 (2/2) | 0.995 (4/4) |
| GARCH-t | 0.997 (3/3) | 0.988 (4/5) | 1.008 (0/1) | 0.986 (2/2) | 0.996 (4/4) |
| GJR-GARCH-t | 0.997 (2/3) | 0.989 (4/5) | 1.007 (0/1) | 0.984 (2/2) | 0.996 (3/4) |
| TimesFM-3 | 0.996 (2/3) | 0.990 (5/5) | 0.998 (1/1) | 0.987 (2/2) | 0.997 (3/4) |
| Timestral-209M | 0.995 (3/3) | 0.985 (5/5) | 0.995 (1/1) | 0.982 (2/2) | 0.995 (4/4) |
| Timestral-28M | 0.996 (3/3) | 0.986 (5/5) | 0.993 (1/1) | 0.980 (2/2) | 0.996 (4/4) |

**Volatilita' h=5: QLIKE / HAR**

| modello | Cereali | Energia | Metalli industriali | Metalli preziosi | Soft e bestiame |
|---|---|---|---|---|---|
| Chronos-2 | 0.944 (1/3) | 1.113 (1/5) | 1.294 (0/1) | 1.064 (0/1) | 1.061 (0/2) |
| Media 22g | 1.096 (0/3) | 1.306 (0/5) | 1.085 (0/1) | 1.101 (0/1) | 1.175 (0/2) |
| TimesFM-3 | 0.896 (1/3) | 1.090 (1/5) | 1.166 (0/1) | 1.003 (0/1) | 1.013 (0/2) |
| Timestral-209M | 0.873 (2/3) | 1.085 (1/5) | 1.226 (0/1) | 0.990 (1/1) | 1.031 (0/2) |
| Timestral-28M | 0.900 (1/3) | 1.094 (1/5) | 1.201 (0/1) | 1.030 (0/1) | 1.052 (0/2) |

## Dettaglio per asset

### Prezzo

| asset | settore | h | modello | n | MAE/RW | CRPS/RW | DM p (CRPS) | DM stat | direzione | cop80 | cop80 RW | in MCS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WTI | Energia | 1 | Timestral-28M | 708 | 1.001 | 0.970 | 0.000 | -3.605 | 0.535 | 0.795 | 0.771 | True |
| WTI | Energia | 1 | Timestral-209M | 708 | 1.005 | 0.973 | 0.001 | -3.345 | 0.467 | 0.788 | 0.771 | True |
| WTI | Energia | 1 | TimesFM-3 | 708 | 1.007 | 0.977 | 0.022 | -2.296 | 0.502 | 0.802 | 0.771 | True |
| WTI | Energia | 1 | Chronos-2 | 708 | 1.031 | 1.000 | 0.989 | 0.013 | 0.488 | 0.804 | 0.771 | False |
| WTI | Energia | 1 | ARIMA | 708 | 1.000 | 0.991 | 0.077 | -1.769 | 0.436 | 0.826 | 0.771 | False |
| WTI | Energia | 1 | ETS | 708 | 1.000 | 0.988 | 0.006 | -2.775 | 0.513 | 0.825 | 0.771 | False |
| WTI | Energia | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.771 |  | False |
| WTI | Energia | 5 | Timestral-28M | 704 | 0.998 | 0.950 | 0.001 | -3.358 | 0.545 | 0.795 | 0.754 | True |
| WTI | Energia | 5 | Timestral-209M | 704 | 1.000 | 0.953 | 0.000 | -3.499 | 0.496 | 0.807 | 0.754 | True |
| WTI | Energia | 5 | TimesFM-3 | 704 | 0.999 | 0.952 | 0.002 | -3.041 | 0.479 | 0.808 | 0.754 | True |
| WTI | Energia | 5 | Chronos-2 | 704 | 1.028 | 0.980 | 0.178 | -1.348 | 0.486 | 0.754 | 0.754 | False |
| WTI | Energia | 5 | ARIMA | 704 | 1.000 | 0.981 | 0.020 | -2.338 | 0.452 | 0.800 | 0.754 | False |
| WTI | Energia | 5 | ETS | 704 | 1.000 | 0.978 | 0.008 | -2.677 | 0.487 | 0.793 | 0.754 | False |
| WTI | Energia | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.754 |  | False |
| WTI | Energia | 20 | Timestral-28M | 689 | 1.007 | 0.960 | 0.327 | -0.981 | 0.463 | 0.852 | 0.791 | True |
| WTI | Energia | 20 | Timestral-209M | 689 | 1.006 | 0.964 | 0.288 | -1.064 | 0.457 | 0.849 | 0.791 | True |
| WTI | Energia | 20 | TimesFM-3 | 689 | 1.006 | 0.965 | 0.296 | -1.045 | 0.480 | 0.852 | 0.791 | True |
| WTI | Energia | 20 | Chronos-2 | 689 | 1.036 | 0.982 | 0.567 | -0.572 | 0.467 | 0.835 | 0.791 | True |
| WTI | Energia | 20 | ARIMA | 689 | 0.998 | 0.973 | 0.332 | -0.972 | 0.459 | 0.865 | 0.791 | True |
| WTI | Energia | 20 | ETS | 689 | 1.000 | 0.974 | 0.339 | -0.957 | 0.521 | 0.878 | 0.791 | True |
| WTI | Energia | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.791 |  | True |
| Brent | Energia | 1 | Timestral-28M | 693 | 1.004 | 0.965 | 0.000 | -3.661 | 0.504 | 0.811 | 0.762 | True |
| Brent | Energia | 1 | Timestral-209M | 693 | 1.004 | 0.966 | 0.000 | -3.940 | 0.492 | 0.807 | 0.762 | True |
| Brent | Energia | 1 | TimesFM-3 | 693 | 1.006 | 0.970 | 0.012 | -2.528 | 0.499 | 0.799 | 0.762 | True |
| Brent | Energia | 1 | Chronos-2 | 693 | 1.035 | 0.993 | 0.551 | -0.596 | 0.498 | 0.776 | 0.762 | False |
| Brent | Energia | 1 | ARIMA | 693 | 1.004 | 1.001 | 0.773 | 0.288 | 0.428 | 0.820 | 0.762 | False |
| Brent | Energia | 1 | ETS | 693 | 1.002 | 0.995 | 0.302 | -1.032 | 0.514 | 0.817 | 0.762 | False |
| Brent | Energia | 1 | Random walk | 693 | 1.000 | 1.000 |  |  |  | 0.762 |  | False |
| Brent | Energia | 5 | Timestral-28M | 689 | 1.003 | 0.961 | 0.007 | -2.689 | 0.494 | 0.795 | 0.752 | True |
| Brent | Energia | 5 | Timestral-209M | 689 | 1.003 | 0.963 | 0.003 | -2.953 | 0.466 | 0.795 | 0.752 | True |
| Brent | Energia | 5 | TimesFM-3 | 689 | 1.009 | 0.963 | 0.013 | -2.479 | 0.458 | 0.811 | 0.752 | True |
| Brent | Energia | 5 | Chronos-2 | 689 | 1.030 | 0.993 | 0.630 | -0.482 | 0.474 | 0.733 | 0.752 | False |
| Brent | Energia | 5 | ARIMA | 689 | 0.997 | 0.985 | 0.081 | -1.746 | 0.440 | 0.808 | 0.752 | False |
| Brent | Energia | 5 | ETS | 689 | 1.001 | 0.987 | 0.094 | -1.678 | 0.490 | 0.806 | 0.752 | False |
| Brent | Energia | 5 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.752 |  | False |
| Brent | Energia | 20 | Timestral-28M | 674 | 1.015 | 0.972 | 0.517 | -0.648 | 0.439 | 0.832 | 0.746 | True |
| Brent | Energia | 20 | Timestral-209M | 674 | 1.004 | 0.967 | 0.338 | -0.958 | 0.440 | 0.820 | 0.746 | True |
| Brent | Energia | 20 | TimesFM-3 | 674 | 1.004 | 0.966 | 0.348 | -0.940 | 0.478 | 0.841 | 0.746 | True |
| Brent | Energia | 20 | Chronos-2 | 674 | 1.029 | 0.986 | 0.690 | -0.399 | 0.463 | 0.794 | 0.746 | True |
| Brent | Energia | 20 | ARIMA | 674 | 0.999 | 0.974 | 0.334 | -0.966 | 0.408 | 0.856 | 0.746 | True |
| Brent | Energia | 20 | ETS | 674 | 1.000 | 0.979 | 0.464 | -0.733 | 0.524 | 0.861 | 0.746 | True |
| Brent | Energia | 20 | Random walk | 674 | 1.000 | 1.000 |  |  |  | 0.746 |  | True |
| Gasolio | Energia | 1 | Timestral-28M | 708 | 1.016 | 0.970 | 0.006 | -2.783 | 0.475 | 0.804 | 0.753 | True |
| Gasolio | Energia | 1 | Timestral-209M | 708 | 1.007 | 0.962 | 0.000 | -4.046 | 0.473 | 0.802 | 0.753 | True |
| Gasolio | Energia | 1 | TimesFM-3 | 708 | 1.004 | 0.968 | 0.001 | -3.298 | 0.480 | 0.799 | 0.753 | True |
| Gasolio | Energia | 1 | Chronos-2 | 708 | 1.052 | 1.008 | 0.555 | 0.590 | 0.473 | 0.753 | 0.753 | False |
| Gasolio | Energia | 1 | ARIMA | 708 | 1.010 | 1.004 | 0.426 | 0.797 | 0.373 | 0.828 | 0.753 | False |
| Gasolio | Energia | 1 | ETS | 708 | 1.000 | 0.971 | 0.000 | -3.713 | 0.483 | 0.819 | 0.753 | True |
| Gasolio | Energia | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.753 |  | False |
| Gasolio | Energia | 5 | Timestral-28M | 704 | 1.019 | 0.987 | 0.497 | -0.680 | 0.477 | 0.791 | 0.749 | True |
| Gasolio | Energia | 5 | Timestral-209M | 704 | 1.012 | 0.983 | 0.258 | -1.132 | 0.464 | 0.800 | 0.749 | True |
| Gasolio | Energia | 5 | TimesFM-3 | 704 | 1.020 | 0.990 | 0.580 | -0.553 | 0.470 | 0.800 | 0.749 | True |
| Gasolio | Energia | 5 | Chronos-2 | 704 | 1.040 | 1.013 | 0.447 | 0.761 | 0.493 | 0.719 | 0.749 | True |
| Gasolio | Energia | 5 | ARIMA | 704 | 1.003 | 1.003 | 0.756 | 0.311 | 0.416 | 0.828 | 0.749 | False |
| Gasolio | Energia | 5 | ETS | 704 | 0.998 | 0.976 | 0.041 | -2.045 | 0.509 | 0.824 | 0.749 | True |
| Gasolio | Energia | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.749 |  | True |
| Gasolio | Energia | 20 | Timestral-28M | 689 | 1.017 | 0.987 | 0.727 | -0.350 | 0.533 | 0.811 | 0.729 | True |
| Gasolio | Energia | 20 | Timestral-209M | 689 | 1.009 | 0.981 | 0.493 | -0.686 | 0.457 | 0.813 | 0.729 | True |
| Gasolio | Energia | 20 | TimesFM-3 | 689 | 1.010 | 0.975 | 0.509 | -0.660 | 0.569 | 0.816 | 0.729 | True |
| Gasolio | Energia | 20 | Chronos-2 | 689 | 1.038 | 0.994 | 0.849 | -0.190 | 0.399 | 0.772 | 0.729 | True |
| Gasolio | Energia | 20 | ARIMA | 689 | 1.015 | 1.001 | 0.975 | 0.032 | 0.424 | 0.848 | 0.729 | True |
| Gasolio | Energia | 20 | ETS | 689 | 0.994 | 0.976 | 0.353 | -0.930 | 0.509 | 0.829 | 0.729 | True |
| Gasolio | Energia | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.729 |  | True |
| Benzina | Energia | 1 | Timestral-28M | 708 | 1.004 | 0.974 | 0.001 | -3.456 | 0.511 | 0.831 | 0.767 | True |
| Benzina | Energia | 1 | Timestral-209M | 708 | 0.999 | 0.970 | 0.000 | -4.620 | 0.529 | 0.825 | 0.767 | True |
| Benzina | Energia | 1 | TimesFM-3 | 708 | 1.012 | 0.980 | 0.022 | -2.295 | 0.477 | 0.790 | 0.767 | True |
| Benzina | Energia | 1 | Chronos-2 | 708 | 1.031 | 1.002 | 0.823 | 0.224 | 0.516 | 0.811 | 0.767 | False |
| Benzina | Energia | 1 | ARIMA | 708 | 1.002 | 0.999 | 0.793 | -0.262 | 0.085 | 0.860 | 0.767 | False |
| Benzina | Energia | 1 | ETS | 708 | 1.000 | 0.988 | 0.130 | -1.517 | 0.505 | 0.869 | 0.767 | False |
| Benzina | Energia | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.767 |  | False |
| Benzina | Energia | 5 | Timestral-28M | 704 | 1.002 | 0.962 | 0.002 | -3.105 | 0.513 | 0.828 | 0.774 | True |
| Benzina | Energia | 5 | Timestral-209M | 704 | 0.995 | 0.956 | 0.000 | -3.867 | 0.499 | 0.820 | 0.774 | True |
| Benzina | Energia | 5 | TimesFM-3 | 704 | 1.007 | 0.965 | 0.013 | -2.498 | 0.501 | 0.828 | 0.774 | True |
| Benzina | Energia | 5 | Chronos-2 | 704 | 1.032 | 0.990 | 0.452 | -0.752 | 0.477 | 0.749 | 0.774 | False |
| Benzina | Energia | 5 | ARIMA | 704 | 1.000 | 0.983 | 0.077 | -1.769 | 0.077 | 0.865 | 0.774 | False |
| Benzina | Energia | 5 | ETS | 704 | 1.000 | 0.976 | 0.067 | -1.837 | 0.497 | 0.858 | 0.774 | False |
| Benzina | Energia | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.774 |  | False |
| Benzina | Energia | 20 | Timestral-28M | 689 | 1.000 | 0.945 | 0.096 | -1.669 | 0.544 | 0.853 | 0.727 | True |
| Benzina | Energia | 20 | Timestral-209M | 689 | 0.988 | 0.929 | 0.016 | -2.417 | 0.524 | 0.855 | 0.727 | True |
| Benzina | Energia | 20 | TimesFM-3 | 689 | 0.989 | 0.941 | 0.051 | -1.956 | 0.559 | 0.869 | 0.727 | True |
| Benzina | Energia | 20 | Chronos-2 | 689 | 1.012 | 0.958 | 0.037 | -2.092 | 0.493 | 0.790 | 0.727 | True |
| Benzina | Energia | 20 | ARIMA | 689 | 1.001 | 0.965 | 0.157 | -1.416 | 0.083 | 0.865 | 0.727 | False |
| Benzina | Energia | 20 | ETS | 689 | 0.999 | 0.952 | 0.096 | -1.665 | 0.538 | 0.888 | 0.727 | True |
| Benzina | Energia | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.727 |  | True |
| Gas naturale | Energia | 1 | Timestral-28M | 708 | 1.018 | 0.983 | 0.187 | -1.321 | 0.516 | 0.806 | 0.798 | True |
| Gas naturale | Energia | 1 | Timestral-209M | 708 | 1.002 | 0.973 | 0.001 | -3.207 | 0.518 | 0.802 | 0.798 | True |
| Gas naturale | Energia | 1 | TimesFM-3 | 708 | 1.016 | 0.989 | 0.215 | -1.242 | 0.500 | 0.808 | 0.798 | False |
| Gas naturale | Energia | 1 | Chronos-2 | 708 | 1.032 | 1.006 | 0.603 | 0.520 | 0.504 | 0.770 | 0.798 | False |
| Gas naturale | Energia | 1 | ARIMA | 708 | 1.002 | 0.994 | 0.428 | -0.793 | 0.528 | 0.884 | 0.798 | False |
| Gas naturale | Energia | 1 | ETS | 708 | 1.001 | 0.996 | 0.543 | -0.608 | 0.521 | 0.888 | 0.798 | False |
| Gas naturale | Energia | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.798 |  | False |
| Gas naturale | Energia | 5 | Timestral-28M | 704 | 0.992 | 0.946 | 0.074 | -1.791 | 0.511 | 0.771 | 0.777 | True |
| Gas naturale | Energia | 5 | Timestral-209M | 704 | 0.999 | 0.954 | 0.022 | -2.289 | 0.477 | 0.781 | 0.777 | True |
| Gas naturale | Energia | 5 | TimesFM-3 | 704 | 1.021 | 0.976 | 0.159 | -1.410 | 0.444 | 0.786 | 0.777 | False |
| Gas naturale | Energia | 5 | Chronos-2 | 704 | 1.000 | 0.965 | 0.073 | -1.797 | 0.513 | 0.727 | 0.777 | True |
| Gas naturale | Energia | 5 | ARIMA | 704 | 1.003 | 0.984 | 0.025 | -2.248 | 0.476 | 0.847 | 0.777 | True |
| Gas naturale | Energia | 5 | ETS | 704 | 1.003 | 0.987 | 0.070 | -1.816 | 0.519 | 0.842 | 0.777 | True |
| Gas naturale | Energia | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.777 |  | True |
| Gas naturale | Energia | 20 | Timestral-28M | 689 | 0.975 | 0.910 | 0.030 | -2.178 | 0.609 | 0.779 | 0.772 | True |
| Gas naturale | Energia | 20 | Timestral-209M | 689 | 0.986 | 0.922 | 0.011 | -2.536 | 0.529 | 0.788 | 0.772 | True |
| Gas naturale | Energia | 20 | TimesFM-3 | 689 | 1.006 | 0.939 | 0.015 | -2.434 | 0.523 | 0.817 | 0.772 | True |
| Gas naturale | Energia | 20 | Chronos-2 | 689 | 0.971 | 0.906 | 0.052 | -1.946 | 0.500 | 0.768 | 0.772 | True |
| Gas naturale | Energia | 20 | ARIMA | 689 | 1.005 | 0.949 | 0.020 | -2.339 | 0.497 | 0.855 | 0.772 | True |
| Gas naturale | Energia | 20 | ETS | 689 | 1.009 | 0.964 | 0.117 | -1.568 | 0.488 | 0.848 | 0.772 | True |
| Gas naturale | Energia | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.772 |  | False |
| Oro | Metalli preziosi | 1 | Timestral-28M | 708 | 1.007 | 0.990 | 0.196 | -1.294 | 0.513 | 0.785 | 0.686 | True |
| Oro | Metalli preziosi | 1 | Timestral-209M | 708 | 1.005 | 0.987 | 0.107 | -1.614 | 0.500 | 0.775 | 0.686 | True |
| Oro | Metalli preziosi | 1 | TimesFM-3 | 708 | 1.018 | 1.002 | 0.862 | 0.173 | 0.479 | 0.833 | 0.686 | True |
| Oro | Metalli preziosi | 1 | Chronos-2 | 708 | 1.824 | 1.630 | 0.000 | 13.423 | 0.435 | 0.853 | 0.686 | False |
| Oro | Metalli preziosi | 1 | ARIMA | 708 | 1.006 | 0.995 | 0.272 | -1.099 | 0.518 | 0.742 | 0.686 | True |
| Oro | Metalli preziosi | 1 | ETS | 708 | 0.999 | 0.987 | 0.003 | -3.016 | 0.545 | 0.767 | 0.686 | True |
| Oro | Metalli preziosi | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.686 |  | False |
| Oro | Metalli preziosi | 5 | Timestral-28M | 704 | 1.003 | 0.998 | 0.919 | -0.102 | 0.484 | 0.712 | 0.670 | True |
| Oro | Metalli preziosi | 5 | Timestral-209M | 704 | 0.997 | 0.986 | 0.488 | -0.693 | 0.497 | 0.766 | 0.670 | True |
| Oro | Metalli preziosi | 5 | TimesFM-3 | 704 | 1.003 | 0.995 | 0.815 | -0.234 | 0.489 | 0.805 | 0.670 | True |
| Oro | Metalli preziosi | 5 | Chronos-2 | 704 | 1.209 | 1.216 | 0.000 | 3.510 | 0.391 | 0.625 | 0.670 | False |
| Oro | Metalli preziosi | 5 | ARIMA | 704 | 0.993 | 0.997 | 0.695 | -0.393 | 0.567 | 0.722 | 0.670 | True |
| Oro | Metalli preziosi | 5 | ETS | 704 | 0.992 | 0.988 | 0.100 | -1.646 | 0.547 | 0.740 | 0.670 | True |
| Oro | Metalli preziosi | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.670 |  | True |
| Oro | Metalli preziosi | 20 | Timestral-28M | 689 | 0.987 | 1.013 | 0.825 | 0.222 | 0.662 | 0.660 | 0.615 | True |
| Oro | Metalli preziosi | 20 | Timestral-209M | 689 | 0.995 | 1.014 | 0.837 | 0.206 | 0.570 | 0.701 | 0.615 | True |
| Oro | Metalli preziosi | 20 | TimesFM-3 | 689 | 0.990 | 1.009 | 0.900 | 0.126 | 0.469 | 0.803 | 0.615 | True |
| Oro | Metalli preziosi | 20 | Chronos-2 | 689 | 1.126 | 1.174 | 0.123 | 1.546 | 0.334 | 0.562 | 0.615 | False |
| Oro | Metalli preziosi | 20 | ARIMA | 689 | 1.003 | 1.016 | 0.416 | 0.813 | 0.594 | 0.678 | 0.615 | True |
| Oro | Metalli preziosi | 20 | ETS | 689 | 0.996 | 0.998 | 0.946 | -0.068 | 0.576 | 0.695 | 0.615 | True |
| Oro | Metalli preziosi | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.615 |  | True |
| Argento | Metalli preziosi | 1 | Timestral-28M | 708 | 1.014 | 0.940 | 0.000 | -4.301 | 0.470 | 0.795 | 0.720 | True |
| Argento | Metalli preziosi | 1 | Timestral-209M | 708 | 1.008 | 0.940 | 0.000 | -4.424 | 0.493 | 0.794 | 0.720 | True |
| Argento | Metalli preziosi | 1 | TimesFM-3 | 708 | 1.017 | 0.939 | 0.003 | -3.021 | 0.490 | 0.836 | 0.720 | True |
| Argento | Metalli preziosi | 1 | Chronos-2 | 708 | 1.270 | 1.135 | 0.002 | 3.074 | 0.496 | 0.840 | 0.720 | False |
| Argento | Metalli preziosi | 1 | ARIMA | 708 | 1.004 | 0.967 | 0.000 | -4.171 | 0.452 | 0.757 | 0.720 | False |
| Argento | Metalli preziosi | 1 | ETS | 708 | 1.002 | 0.951 | 0.000 | -6.091 | 0.532 | 0.774 | 0.720 | True |
| Argento | Metalli preziosi | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.720 |  | False |
| Argento | Metalli preziosi | 5 | Timestral-28M | 704 | 1.015 | 0.939 | 0.017 | -2.403 | 0.449 | 0.770 | 0.709 | True |
| Argento | Metalli preziosi | 5 | Timestral-209M | 704 | 1.003 | 0.927 | 0.005 | -2.821 | 0.493 | 0.786 | 0.709 | True |
| Argento | Metalli preziosi | 5 | TimesFM-3 | 704 | 1.013 | 0.934 | 0.038 | -2.081 | 0.476 | 0.831 | 0.709 | True |
| Argento | Metalli preziosi | 5 | Chronos-2 | 704 | 1.077 | 1.007 | 0.895 | 0.132 | 0.504 | 0.722 | 0.709 | True |
| Argento | Metalli preziosi | 5 | ARIMA | 704 | 0.997 | 0.942 | 0.017 | -2.393 | 0.447 | 0.770 | 0.709 | True |
| Argento | Metalli preziosi | 5 | ETS | 704 | 1.010 | 0.947 | 0.000 | -3.656 | 0.469 | 0.787 | 0.709 | True |
| Argento | Metalli preziosi | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.709 |  | False |
| Argento | Metalli preziosi | 20 | Timestral-28M | 689 | 1.014 | 0.944 | 0.200 | -1.283 | 0.440 | 0.742 | 0.647 | True |
| Argento | Metalli preziosi | 20 | Timestral-209M | 689 | 0.996 | 0.927 | 0.147 | -1.452 | 0.454 | 0.763 | 0.647 | True |
| Argento | Metalli preziosi | 20 | TimesFM-3 | 689 | 0.983 | 0.916 | 0.115 | -1.579 | 0.492 | 0.813 | 0.647 | True |
| Argento | Metalli preziosi | 20 | Chronos-2 | 689 | 1.111 | 1.031 | 0.726 | 0.351 | 0.565 | 0.697 | 0.647 | True |
| Argento | Metalli preziosi | 20 | ARIMA | 689 | 1.108 | 1.041 | 0.616 | 0.501 | 0.441 | 0.740 | 0.647 | True |
| Argento | Metalli preziosi | 20 | ETS | 689 | 1.024 | 0.946 | 0.134 | -1.502 | 0.472 | 0.761 | 0.647 | True |
| Argento | Metalli preziosi | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.647 |  | True |
| Rame | Metalli industriali | 1 | Timestral-28M | 708 | 1.003 | 0.991 | 0.121 | -1.553 | 0.486 | 0.806 | 0.749 | False |
| Rame | Metalli industriali | 1 | Timestral-209M | 708 | 0.997 | 0.986 | 0.008 | -2.671 | 0.544 | 0.794 | 0.749 | True |
| Rame | Metalli industriali | 1 | TimesFM-3 | 708 | 1.009 | 1.000 | 0.977 | -0.029 | 0.459 | 0.845 | 0.749 | False |
| Rame | Metalli industriali | 1 | Chronos-2 | 708 | 1.052 | 1.052 | 0.001 | 3.267 | 0.501 | 0.893 | 0.749 | False |
| Rame | Metalli industriali | 1 | ARIMA | 708 | 1.002 | 1.002 | 0.704 | 0.381 | 0.249 | 0.825 | 0.749 | False |
| Rame | Metalli industriali | 1 | ETS | 708 | 0.998 | 1.006 | 0.390 | 0.861 | 0.550 | 0.855 | 0.749 | False |
| Rame | Metalli industriali | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.749 |  | False |
| Rame | Metalli industriali | 5 | Timestral-28M | 704 | 1.001 | 1.006 | 0.673 | 0.423 | 0.497 | 0.754 | 0.717 | False |
| Rame | Metalli industriali | 5 | Timestral-209M | 704 | 0.994 | 0.997 | 0.790 | -0.267 | 0.572 | 0.764 | 0.717 | True |
| Rame | Metalli industriali | 5 | TimesFM-3 | 704 | 1.005 | 1.009 | 0.547 | 0.602 | 0.501 | 0.795 | 0.717 | True |
| Rame | Metalli industriali | 5 | Chronos-2 | 704 | 1.019 | 1.018 | 0.325 | 0.985 | 0.517 | 0.720 | 0.717 | True |
| Rame | Metalli industriali | 5 | ARIMA | 704 | 0.999 | 0.998 | 0.891 | -0.138 | 0.241 | 0.820 | 0.717 | True |
| Rame | Metalli industriali | 5 | ETS | 704 | 0.998 | 1.005 | 0.717 | 0.362 | 0.514 | 0.857 | 0.717 | True |
| Rame | Metalli industriali | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.717 |  | True |
| Rame | Metalli industriali | 20 | Timestral-28M | 689 | 0.999 | 0.994 | 0.895 | -0.132 | 0.432 | 0.747 | 0.723 | True |
| Rame | Metalli industriali | 20 | Timestral-209M | 689 | 0.993 | 0.993 | 0.867 | -0.168 | 0.535 | 0.745 | 0.723 | True |
| Rame | Metalli industriali | 20 | TimesFM-3 | 689 | 1.009 | 1.006 | 0.875 | 0.157 | 0.453 | 0.787 | 0.723 | True |
| Rame | Metalli industriali | 20 | Chronos-2 | 689 | 1.004 | 0.990 | 0.769 | -0.294 | 0.513 | 0.676 | 0.723 | True |
| Rame | Metalli industriali | 20 | ARIMA | 689 | 0.999 | 0.989 | 0.760 | -0.305 | 0.257 | 0.817 | 0.723 | True |
| Rame | Metalli industriali | 20 | ETS | 689 | 1.001 | 0.997 | 0.928 | -0.090 | 0.513 | 0.836 | 0.723 | True |
| Rame | Metalli industriali | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.723 |  | True |
| Grano | Cereali | 1 | Timestral-28M | 707 | 0.994 | 0.984 | 0.007 | -2.728 | 0.551 | 0.839 | 0.805 | True |
| Grano | Cereali | 1 | Timestral-209M | 707 | 0.996 | 0.982 | 0.001 | -3.456 | 0.539 | 0.829 | 0.805 | True |
| Grano | Cereali | 1 | TimesFM-3 | 707 | 0.996 | 0.982 | 0.001 | -3.260 | 0.532 | 0.842 | 0.805 | True |
| Grano | Cereali | 1 | Chronos-2 | 707 | 1.031 | 1.017 | 0.048 | 1.983 | 0.488 | 0.833 | 0.805 | False |
| Grano | Cereali | 1 | ARIMA | 707 | 1.017 | 1.021 | 0.004 | 2.887 | 0.464 | 0.895 | 0.805 | False |
| Grano | Cereali | 1 | ETS | 707 | 1.000 | 1.007 | 0.142 | 1.471 | 0.496 | 0.888 | 0.805 | False |
| Grano | Cereali | 1 | Random walk | 707 | 1.000 | 1.000 |  |  |  | 0.805 |  | False |
| Grano | Cereali | 5 | Timestral-28M | 703 | 0.991 | 0.966 | 0.020 | -2.334 | 0.541 | 0.853 | 0.778 | True |
| Grano | Cereali | 5 | Timestral-209M | 703 | 0.995 | 0.967 | 0.004 | -2.869 | 0.538 | 0.849 | 0.778 | True |
| Grano | Cereali | 5 | TimesFM-3 | 703 | 0.997 | 0.968 | 0.001 | -3.421 | 0.539 | 0.821 | 0.778 | True |
| Grano | Cereali | 5 | Chronos-2 | 703 | 1.013 | 0.985 | 0.123 | -1.543 | 0.489 | 0.822 | 0.778 | False |
| Grano | Cereali | 5 | ARIMA | 703 | 0.997 | 1.012 | 0.389 | 0.863 | 0.514 | 0.902 | 0.778 | False |
| Grano | Cereali | 5 | ETS | 703 | 1.000 | 0.999 | 0.928 | -0.091 | 0.519 | 0.899 | 0.778 | False |
| Grano | Cereali | 5 | Random walk | 703 | 1.000 | 1.000 |  |  |  | 0.778 |  | False |
| Grano | Cereali | 20 | Timestral-28M | 688 | 0.967 | 0.923 | 0.079 | -1.757 | 0.581 | 0.833 | 0.744 | True |
| Grano | Cereali | 20 | Timestral-209M | 688 | 0.987 | 0.931 | 0.034 | -2.122 | 0.547 | 0.839 | 0.744 | False |
| Grano | Cereali | 20 | TimesFM-3 | 688 | 0.965 | 0.908 | 0.002 | -3.115 | 0.688 | 0.846 | 0.744 | True |
| Grano | Cereali | 20 | Chronos-2 | 688 | 0.981 | 0.926 | 0.037 | -2.094 | 0.534 | 0.846 | 0.744 | True |
| Grano | Cereali | 20 | ARIMA | 688 | 1.018 | 0.987 | 0.720 | -0.358 | 0.455 | 0.869 | 0.744 | False |
| Grano | Cereali | 20 | ETS | 688 | 1.000 | 0.966 | 0.306 | -1.025 | 0.496 | 0.901 | 0.744 | False |
| Grano | Cereali | 20 | Random walk | 688 | 1.000 | 1.000 |  |  |  | 0.744 |  | False |
| Mais | Cereali | 1 | Timestral-28M | 707 | 1.003 | 0.995 | 0.298 | -1.041 | 0.486 | 0.819 | 0.820 | False |
| Mais | Cereali | 1 | Timestral-209M | 707 | 1.004 | 0.991 | 0.036 | -2.101 | 0.468 | 0.833 | 0.820 | True |
| Mais | Cereali | 1 | TimesFM-3 | 707 | 1.003 | 1.001 | 0.876 | 0.156 | 0.501 | 0.826 | 0.820 | False |
| Mais | Cereali | 1 | Chronos-2 | 707 | 1.049 | 1.035 | 0.002 | 3.174 | 0.486 | 0.843 | 0.820 | False |
| Mais | Cereali | 1 | ARIMA | 707 | 1.001 | 1.029 | 0.000 | 4.160 | 0.481 | 0.917 | 0.820 | False |
| Mais | Cereali | 1 | ETS | 707 | 1.003 | 1.021 | 0.000 | 3.953 | 0.485 | 0.915 | 0.820 | False |
| Mais | Cereali | 1 | Random walk | 707 | 1.000 | 1.000 |  |  |  | 0.820 |  | False |
| Mais | Cereali | 5 | Timestral-28M | 703 | 1.001 | 0.979 | 0.009 | -2.626 | 0.484 | 0.808 | 0.755 | False |
| Mais | Cereali | 5 | Timestral-209M | 703 | 1.000 | 0.973 | 0.001 | -3.425 | 0.511 | 0.815 | 0.755 | True |
| Mais | Cereali | 5 | TimesFM-3 | 703 | 1.018 | 0.989 | 0.246 | -1.161 | 0.441 | 0.812 | 0.755 | False |
| Mais | Cereali | 5 | Chronos-2 | 703 | 1.039 | 1.015 | 0.201 | 1.279 | 0.443 | 0.716 | 0.755 | False |
| Mais | Cereali | 5 | ARIMA | 703 | 1.003 | 1.009 | 0.412 | 0.821 | 0.476 | 0.883 | 0.755 | False |
| Mais | Cereali | 5 | ETS | 703 | 1.005 | 1.005 | 0.626 | 0.488 | 0.477 | 0.878 | 0.755 | False |
| Mais | Cereali | 5 | Random walk | 703 | 1.000 | 1.000 |  |  |  | 0.755 |  | False |
| Mais | Cereali | 20 | Timestral-28M | 688 | 1.002 | 0.944 | 0.111 | -1.598 | 0.521 | 0.763 | 0.765 | True |
| Mais | Cereali | 20 | Timestral-209M | 688 | 0.998 | 0.937 | 0.075 | -1.785 | 0.496 | 0.767 | 0.765 | True |
| Mais | Cereali | 20 | TimesFM-3 | 688 | 1.013 | 0.960 | 0.197 | -1.292 | 0.473 | 0.785 | 0.765 | False |
| Mais | Cereali | 20 | Chronos-2 | 688 | 1.020 | 0.969 | 0.466 | -0.729 | 0.498 | 0.727 | 0.765 | True |
| Mais | Cereali | 20 | ARIMA | 688 | 1.001 | 0.953 | 0.166 | -1.388 | 0.480 | 0.863 | 0.765 | True |
| Mais | Cereali | 20 | ETS | 688 | 1.007 | 0.953 | 0.163 | -1.398 | 0.486 | 0.844 | 0.765 | True |
| Mais | Cereali | 20 | Random walk | 688 | 1.000 | 1.000 |  |  |  | 0.765 |  | True |
| Soia | Cereali | 1 | Timestral-28M | 707 | 1.005 | 1.002 | 0.584 | 0.547 | 0.476 | 0.827 | 0.832 | True |
| Soia | Cereali | 1 | Timestral-209M | 707 | 1.003 | 0.999 | 0.866 | -0.169 | 0.504 | 0.847 | 0.832 | True |
| Soia | Cereali | 1 | TimesFM-3 | 707 | 1.004 | 1.003 | 0.472 | 0.720 | 0.515 | 0.827 | 0.832 | True |
| Soia | Cereali | 1 | Chronos-2 | 707 | 1.046 | 1.043 | 0.000 | 3.940 | 0.479 | 0.857 | 0.832 | False |
| Soia | Cereali | 1 | ARIMA | 707 | 0.995 | 1.009 | 0.037 | 2.090 | 0.411 | 0.894 | 0.832 | True |
| Soia | Cereali | 1 | ETS | 707 | 1.000 | 1.010 | 0.020 | 2.333 | 0.514 | 0.890 | 0.832 | False |
| Soia | Cereali | 1 | Random walk | 707 | 1.000 | 1.000 |  |  |  | 0.832 |  | True |
| Soia | Cereali | 5 | Timestral-28M | 703 | 1.003 | 0.994 | 0.562 | -0.581 | 0.470 | 0.826 | 0.804 | True |
| Soia | Cereali | 5 | Timestral-209M | 703 | 1.001 | 0.992 | 0.476 | -0.714 | 0.510 | 0.824 | 0.804 | True |
| Soia | Cereali | 5 | TimesFM-3 | 703 | 1.000 | 0.992 | 0.446 | -0.762 | 0.544 | 0.839 | 0.804 | True |
| Soia | Cereali | 5 | Chronos-2 | 703 | 1.021 | 1.015 | 0.244 | 1.166 | 0.483 | 0.771 | 0.804 | True |
| Soia | Cereali | 5 | ARIMA | 703 | 0.999 | 1.001 | 0.910 | 0.114 | 0.416 | 0.879 | 0.804 | True |
| Soia | Cereali | 5 | ETS | 703 | 1.000 | 1.000 | 0.993 | 0.008 | 0.496 | 0.871 | 0.804 | True |
| Soia | Cereali | 5 | Random walk | 703 | 1.000 | 1.000 |  |  |  | 0.804 |  | True |
| Soia | Cereali | 20 | Timestral-28M | 688 | 1.003 | 0.968 | 0.459 | -0.741 | 0.436 | 0.805 | 0.769 | True |
| Soia | Cereali | 20 | Timestral-209M | 688 | 1.000 | 0.966 | 0.425 | -0.798 | 0.515 | 0.802 | 0.769 | True |
| Soia | Cereali | 20 | TimesFM-3 | 688 | 1.022 | 0.987 | 0.728 | -0.347 | 0.462 | 0.791 | 0.769 | True |
| Soia | Cereali | 20 | Chronos-2 | 688 | 1.042 | 1.004 | 0.937 | 0.079 | 0.490 | 0.766 | 0.769 | True |
| Soia | Cereali | 20 | ARIMA | 688 | 1.005 | 0.974 | 0.546 | -0.603 | 0.384 | 0.843 | 0.769 | True |
| Soia | Cereali | 20 | ETS | 688 | 1.000 | 0.974 | 0.540 | -0.613 | 0.481 | 0.830 | 0.769 | True |
| Soia | Cereali | 20 | Random walk | 688 | 1.000 | 1.000 |  |  |  | 0.769 |  | True |
| Caffe | Soft e bestiame | 1 | Timestral-28M | 708 | 1.002 | 0.989 | 0.067 | -1.837 | 0.507 | 0.790 | 0.749 | True |
| Caffe | Soft e bestiame | 1 | Timestral-209M | 708 | 0.998 | 0.986 | 0.008 | -2.674 | 0.513 | 0.782 | 0.749 | True |
| Caffe | Soft e bestiame | 1 | TimesFM-3 | 708 | 1.007 | 0.993 | 0.268 | -1.108 | 0.506 | 0.822 | 0.749 | True |
| Caffe | Soft e bestiame | 1 | Chronos-2 | 708 | 1.051 | 1.055 | 0.001 | 3.323 | 0.503 | 0.880 | 0.749 | False |
| Caffe | Soft e bestiame | 1 | ARIMA | 708 | 1.009 | 0.995 | 0.413 | -0.819 | 0.466 | 0.792 | 0.749 | True |
| Caffe | Soft e bestiame | 1 | ETS | 708 | 1.003 | 0.992 | 0.113 | -1.586 | 0.514 | 0.811 | 0.749 | True |
| Caffe | Soft e bestiame | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.749 |  | False |
| Caffe | Soft e bestiame | 5 | Timestral-28M | 704 | 1.002 | 0.989 | 0.446 | -0.763 | 0.469 | 0.741 | 0.717 | True |
| Caffe | Soft e bestiame | 5 | Timestral-209M | 704 | 1.000 | 0.985 | 0.192 | -1.307 | 0.489 | 0.751 | 0.717 | True |
| Caffe | Soft e bestiame | 5 | TimesFM-3 | 704 | 0.999 | 0.982 | 0.102 | -1.640 | 0.540 | 0.797 | 0.717 | True |
| Caffe | Soft e bestiame | 5 | Chronos-2 | 704 | 0.993 | 0.974 | 0.131 | -1.513 | 0.553 | 0.743 | 0.717 | True |
| Caffe | Soft e bestiame | 5 | ARIMA | 704 | 1.014 | 0.991 | 0.287 | -1.066 | 0.429 | 0.773 | 0.717 | True |
| Caffe | Soft e bestiame | 5 | ETS | 704 | 1.009 | 0.990 | 0.305 | -1.027 | 0.487 | 0.780 | 0.717 | True |
| Caffe | Soft e bestiame | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.717 |  | True |
| Caffe | Soft e bestiame | 20 | Timestral-28M | 689 | 1.017 | 0.985 | 0.704 | -0.381 | 0.430 | 0.714 | 0.663 | True |
| Caffe | Soft e bestiame | 20 | Timestral-209M | 689 | 1.000 | 0.975 | 0.461 | -0.737 | 0.459 | 0.723 | 0.663 | True |
| Caffe | Soft e bestiame | 20 | TimesFM-3 | 689 | 1.017 | 0.994 | 0.839 | -0.203 | 0.403 | 0.769 | 0.663 | True |
| Caffe | Soft e bestiame | 20 | Chronos-2 | 689 | 0.984 | 0.961 | 0.322 | -0.992 | 0.573 | 0.705 | 0.663 | True |
| Caffe | Soft e bestiame | 20 | ARIMA | 689 | 1.039 | 1.002 | 0.959 | 0.051 | 0.402 | 0.723 | 0.663 | True |
| Caffe | Soft e bestiame | 20 | ETS | 689 | 1.017 | 0.985 | 0.650 | -0.454 | 0.470 | 0.742 | 0.663 | True |
| Caffe | Soft e bestiame | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.663 |  | True |
| Zucchero | Soft e bestiame | 1 | Timestral-28M | 708 | 1.002 | 0.995 | 0.212 | -1.249 | 0.485 | 0.822 | 0.831 | True |
| Zucchero | Soft e bestiame | 1 | Timestral-209M | 708 | 1.000 | 0.992 | 0.049 | -1.972 | 0.514 | 0.795 | 0.831 | True |
| Zucchero | Soft e bestiame | 1 | TimesFM-3 | 708 | 1.006 | 1.000 | 0.974 | -0.032 | 0.506 | 0.814 | 0.831 | True |
| Zucchero | Soft e bestiame | 1 | Chronos-2 | 708 | 1.041 | 1.027 | 0.002 | 3.162 | 0.464 | 0.815 | 0.831 | False |
| Zucchero | Soft e bestiame | 1 | ARIMA | 708 | 1.002 | 0.995 | 0.176 | -1.353 | 0.342 | 0.818 | 0.831 | True |
| Zucchero | Soft e bestiame | 1 | ETS | 708 | 1.000 | 0.992 | 0.018 | -2.374 | 0.492 | 0.795 | 0.831 | True |
| Zucchero | Soft e bestiame | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.831 |  | False |
| Zucchero | Soft e bestiame | 5 | Timestral-28M | 704 | 0.998 | 0.990 | 0.199 | -1.285 | 0.545 | 0.788 | 0.810 | True |
| Zucchero | Soft e bestiame | 5 | Timestral-209M | 704 | 1.000 | 0.991 | 0.281 | -1.079 | 0.517 | 0.784 | 0.810 | True |
| Zucchero | Soft e bestiame | 5 | TimesFM-3 | 704 | 1.005 | 0.999 | 0.947 | -0.066 | 0.517 | 0.788 | 0.810 | True |
| Zucchero | Soft e bestiame | 5 | Chronos-2 | 704 | 1.018 | 1.011 | 0.315 | 1.005 | 0.454 | 0.737 | 0.810 | False |
| Zucchero | Soft e bestiame | 5 | ARIMA | 704 | 1.002 | 0.990 | 0.250 | -1.151 | 0.361 | 0.797 | 0.810 | True |
| Zucchero | Soft e bestiame | 5 | ETS | 704 | 1.000 | 0.988 | 0.146 | -1.456 | 0.511 | 0.771 | 0.810 | True |
| Zucchero | Soft e bestiame | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.810 |  | True |
| Zucchero | Soft e bestiame | 20 | Timestral-28M | 689 | 1.000 | 0.967 | 0.266 | -1.114 | 0.553 | 0.806 | 0.771 | True |
| Zucchero | Soft e bestiame | 20 | Timestral-209M | 689 | 0.997 | 0.962 | 0.209 | -1.259 | 0.531 | 0.787 | 0.771 | True |
| Zucchero | Soft e bestiame | 20 | TimesFM-3 | 689 | 1.007 | 0.971 | 0.340 | -0.954 | 0.505 | 0.800 | 0.771 | True |
| Zucchero | Soft e bestiame | 20 | Chronos-2 | 689 | 1.030 | 0.992 | 0.820 | -0.228 | 0.372 | 0.739 | 0.771 | False |
| Zucchero | Soft e bestiame | 20 | ARIMA | 689 | 1.005 | 0.971 | 0.388 | -0.863 | 0.340 | 0.787 | 0.771 | True |
| Zucchero | Soft e bestiame | 20 | ETS | 689 | 1.000 | 0.963 | 0.243 | -1.169 | 0.498 | 0.772 | 0.771 | True |
| Zucchero | Soft e bestiame | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.771 |  | True |
| Cacao | Soft e bestiame | 1 | Timestral-28M | 708 | 1.010 | 0.967 | 0.000 | -3.831 | 0.505 | 0.795 | 0.749 | True |
| Cacao | Soft e bestiame | 1 | Timestral-209M | 708 | 1.010 | 0.961 | 0.000 | -3.866 | 0.491 | 0.788 | 0.749 | True |
| Cacao | Soft e bestiame | 1 | TimesFM-3 | 708 | 1.014 | 0.971 | 0.003 | -2.934 | 0.491 | 0.781 | 0.749 | True |
| Cacao | Soft e bestiame | 1 | Chronos-2 | 708 | 1.284 | 1.205 | 0.000 | 5.705 | 0.501 | 0.757 | 0.749 | False |
| Cacao | Soft e bestiame | 1 | ARIMA | 708 | 1.013 | 0.985 | 0.023 | -2.277 | 0.471 | 0.708 | 0.749 | False |
| Cacao | Soft e bestiame | 1 | ETS | 708 | 1.001 | 0.971 | 0.000 | -5.226 | 0.529 | 0.716 | 0.749 | True |
| Cacao | Soft e bestiame | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.749 |  | False |
| Cacao | Soft e bestiame | 5 | Timestral-28M | 704 | 1.018 | 0.969 | 0.045 | -2.005 | 0.455 | 0.759 | 0.751 | True |
| Cacao | Soft e bestiame | 5 | Timestral-209M | 704 | 1.005 | 0.955 | 0.016 | -2.421 | 0.469 | 0.761 | 0.751 | True |
| Cacao | Soft e bestiame | 5 | TimesFM-3 | 704 | 1.024 | 0.974 | 0.162 | -1.399 | 0.482 | 0.768 | 0.751 | True |
| Cacao | Soft e bestiame | 5 | Chronos-2 | 704 | 1.058 | 1.004 | 0.928 | 0.090 | 0.528 | 0.683 | 0.751 | True |
| Cacao | Soft e bestiame | 5 | ARIMA | 704 | 1.016 | 0.988 | 0.418 | -0.811 | 0.479 | 0.678 | 0.751 | True |
| Cacao | Soft e bestiame | 5 | ETS | 704 | 1.013 | 0.982 | 0.219 | -1.230 | 0.501 | 0.673 | 0.751 | True |
| Cacao | Soft e bestiame | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.751 |  | True |
| Cacao | Soft e bestiame | 20 | Timestral-28M | 689 | 1.035 | 0.947 | 0.197 | -1.291 | 0.435 | 0.726 | 0.694 | True |
| Cacao | Soft e bestiame | 20 | Timestral-209M | 689 | 1.007 | 0.924 | 0.103 | -1.634 | 0.422 | 0.700 | 0.694 | True |
| Cacao | Soft e bestiame | 20 | TimesFM-3 | 689 | 0.988 | 0.910 | 0.048 | -1.984 | 0.560 | 0.763 | 0.694 | True |
| Cacao | Soft e bestiame | 20 | Chronos-2 | 689 | 1.065 | 0.994 | 0.950 | -0.063 | 0.547 | 0.666 | 0.694 | True |
| Cacao | Soft e bestiame | 20 | ARIMA | 689 | 1.126 | 1.050 | 0.440 | 0.773 | 0.418 | 0.591 | 0.694 | True |
| Cacao | Soft e bestiame | 20 | ETS | 689 | 1.060 | 0.999 | 0.985 | -0.018 | 0.498 | 0.608 | 0.694 | True |
| Cacao | Soft e bestiame | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.694 |  | True |
| Bestiame | Soft e bestiame | 1 | Timestral-28M | 707 | 1.000 | 0.998 | 0.738 | -0.335 | 0.558 | 0.785 | 0.771 | True |
| Bestiame | Soft e bestiame | 1 | Timestral-209M | 707 | 1.004 | 1.004 | 0.536 | 0.620 | 0.505 | 0.750 | 0.771 | True |
| Bestiame | Soft e bestiame | 1 | TimesFM-3 | 707 | 1.016 | 1.011 | 0.158 | 1.412 | 0.474 | 0.785 | 0.771 | True |
| Bestiame | Soft e bestiame | 1 | Chronos-2 | 707 | 1.276 | 1.265 | 0.000 | 8.869 | 0.468 | 0.902 | 0.771 | False |
| Bestiame | Soft e bestiame | 1 | ARIMA | 707 | 1.000 | 1.007 | 0.200 | 1.282 | 0.535 | 0.832 | 0.771 | True |
| Bestiame | Soft e bestiame | 1 | ETS | 707 | 0.994 | 1.003 | 0.619 | 0.498 | 0.518 | 0.843 | 0.771 | True |
| Bestiame | Soft e bestiame | 1 | Random walk | 707 | 1.000 | 1.000 |  |  |  | 0.771 |  | True |
| Bestiame | Soft e bestiame | 5 | Timestral-28M | 703 | 0.990 | 1.001 | 0.911 | 0.111 | 0.596 | 0.730 | 0.747 | True |
| Bestiame | Soft e bestiame | 5 | Timestral-209M | 703 | 0.996 | 1.004 | 0.695 | 0.392 | 0.562 | 0.734 | 0.747 | True |
| Bestiame | Soft e bestiame | 5 | TimesFM-3 | 703 | 0.987 | 0.996 | 0.816 | -0.232 | 0.568 | 0.772 | 0.747 | True |
| Bestiame | Soft e bestiame | 5 | Chronos-2 | 703 | 1.050 | 1.057 | 0.067 | 1.835 | 0.465 | 0.688 | 0.747 | True |
| Bestiame | Soft e bestiame | 5 | ARIMA | 703 | 1.001 | 1.009 | 0.396 | 0.849 | 0.582 | 0.765 | 0.747 | True |
| Bestiame | Soft e bestiame | 5 | ETS | 703 | 0.996 | 0.996 | 0.693 | -0.395 | 0.488 | 0.787 | 0.747 | True |
| Bestiame | Soft e bestiame | 5 | Random walk | 703 | 1.000 | 1.000 |  |  |  | 0.747 |  | True |
| Bestiame | Soft e bestiame | 20 | Timestral-28M | 688 | 0.978 | 0.976 | 0.383 | -0.872 | 0.596 | 0.773 | 0.740 | True |
| Bestiame | Soft e bestiame | 20 | Timestral-209M | 688 | 0.992 | 0.987 | 0.663 | -0.436 | 0.574 | 0.818 | 0.740 | True |
| Bestiame | Soft e bestiame | 20 | TimesFM-3 | 688 | 0.967 | 0.963 | 0.317 | -1.001 | 0.562 | 0.788 | 0.740 | True |
| Bestiame | Soft e bestiame | 20 | Chronos-2 | 688 | 1.012 | 1.004 | 0.938 | 0.077 | 0.499 | 0.682 | 0.740 | True |
| Bestiame | Soft e bestiame | 20 | ARIMA | 688 | 0.983 | 0.976 | 0.254 | -1.141 | 0.567 | 0.779 | 0.740 | True |
| Bestiame | Soft e bestiame | 20 | ETS | 688 | 0.982 | 0.972 | 0.448 | -0.759 | 0.551 | 0.821 | 0.740 | True |
| Bestiame | Soft e bestiame | 20 | Random walk | 688 | 1.000 | 1.000 |  |  |  | 0.740 |  | True |

### VaR

| asset | settore | alpha | modello | n | violazioni | Kupiec p | Christoffersen p | tick/SS | pinball/SS | DM p (pinball) | in MCS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WTI | Energia | 0.100 | Simulazione storica | 708 | 0.112 | 0.312 | 0.110 | 1.000 | 1.000 |  | True |
| WTI | Energia | 0.050 | Simulazione storica | 708 | 0.052 | 0.784 | 0.135 | 1.000 | 1.000 |  | False |
| WTI | Energia | 0.010 | Simulazione storica | 708 | 0.016 | 0.171 | 0.144 | 1.000 | 1.000 |  | False |
| WTI | Energia | 0.100 | GARCH-t | 708 | 0.102 | 0.881 | 0.953 | 0.942 | 0.984 | 0.002 | True |
| WTI | Energia | 0.050 | GARCH-t | 708 | 0.056 | 0.437 | 0.653 | 0.883 | 0.984 | 0.002 | True |
| WTI | Energia | 0.010 | GARCH-t | 708 | 0.011 | 0.734 | 0.190 | 0.723 | 0.984 | 0.002 | True |
| WTI | Energia | 0.100 | GJR-GARCH-t | 708 | 0.100 | 0.980 | 0.938 | 0.949 | 0.986 | 0.006 | True |
| WTI | Energia | 0.050 | GJR-GARCH-t | 708 | 0.054 | 0.658 | 0.726 | 0.902 | 0.986 | 0.006 | True |
| WTI | Energia | 0.010 | GJR-GARCH-t | 708 | 0.016 | 0.171 | 0.144 | 0.796 | 0.986 | 0.006 | True |
| WTI | Energia | 0.100 | EGARCH-t | 708 | 0.099 | 0.920 | 0.995 | 0.954 | 0.986 | 0.002 | True |
| WTI | Energia | 0.050 | EGARCH-t | 708 | 0.049 | 0.945 | 0.976 | 0.919 | 0.986 | 0.002 | True |
| WTI | Energia | 0.010 | EGARCH-t | 708 | 0.013 | 0.486 | 0.199 | 0.866 | 0.986 | 0.002 | True |
| WTI | Energia | 0.100 | Timestral-28M | 708 | 0.092 | 0.462 | 0.689 | 0.949 | 0.986 | 0.011 | True |
| WTI | Energia | 0.050 | Timestral-28M | 708 | 0.047 | 0.676 | 0.855 | 0.887 | 0.986 | 0.011 | True |
| WTI | Energia | 0.010 | Timestral-28M | 708 | 0.011 | 0.734 | 0.190 | 0.729 | 0.986 | 0.011 | True |
| WTI | Energia | 0.100 | Timestral-209M | 708 | 0.095 | 0.631 | 0.697 | 0.949 | 0.985 | 0.007 | True |
| WTI | Energia | 0.050 | Timestral-209M | 708 | 0.042 | 0.339 | 0.612 | 0.886 | 0.985 | 0.007 | True |
| WTI | Energia | 0.010 | Timestral-209M | 708 | 0.010 | 0.976 | 0.932 | 0.720 | 0.985 | 0.007 | True |
| WTI | Energia | 0.100 | TimesFM-3 | 708 | 0.090 | 0.387 | 0.596 | 0.955 | 0.991 | 0.103 | True |
| WTI | Energia | 0.100 | Chronos-2 | 708 | 0.113 | 0.258 | 0.496 | 0.976 | 0.989 | 0.031 | False |
| WTI | Energia | 0.050 | Chronos-2 | 708 | 0.055 | 0.541 | 0.700 | 0.921 | 0.989 | 0.031 | True |
| WTI | Energia | 0.010 | Chronos-2 | 708 | 0.011 | 0.734 | 0.190 | 0.746 | 0.989 | 0.031 | True |
| Brent | Energia | 0.100 | Simulazione storica | 693 | 0.120 | 0.091 | 0.091 | 1.000 | 1.000 |  | False |
| Brent | Energia | 0.050 | Simulazione storica | 693 | 0.061 | 0.214 | 0.062 | 1.000 | 1.000 |  | False |
| Brent | Energia | 0.010 | Simulazione storica | 693 | 0.014 | 0.272 | 0.172 | 1.000 | 1.000 |  | False |
| Brent | Energia | 0.100 | GARCH-t | 693 | 0.105 | 0.642 | 0.602 | 0.922 | 0.977 | 0.000 | True |
| Brent | Energia | 0.050 | GARCH-t | 693 | 0.056 | 0.457 | 0.653 | 0.877 | 0.977 | 0.000 | True |
| Brent | Energia | 0.010 | GARCH-t | 693 | 0.016 | 0.152 | 0.134 | 0.715 | 0.977 | 0.000 | True |
| Brent | Energia | 0.100 | GJR-GARCH-t | 693 | 0.101 | 0.929 | 0.737 | 0.929 | 0.979 | 0.000 | True |
| Brent | Energia | 0.050 | GJR-GARCH-t | 693 | 0.053 | 0.685 | 0.711 | 0.890 | 0.979 | 0.000 | True |
| Brent | Energia | 0.010 | GJR-GARCH-t | 693 | 0.014 | 0.272 | 0.472 | 0.774 | 0.979 | 0.000 | True |
| Brent | Energia | 0.100 | EGARCH-t | 693 | 0.097 | 0.770 | 0.935 | 0.931 | 0.980 | 0.000 | True |
| Brent | Energia | 0.050 | EGARCH-t | 693 | 0.048 | 0.772 | 0.904 | 0.908 | 0.980 | 0.000 | True |
| Brent | Energia | 0.010 | EGARCH-t | 693 | 0.017 | 0.080 | 0.093 | 0.842 | 0.980 | 0.000 | True |
| Brent | Energia | 0.100 | Timestral-28M | 693 | 0.085 | 0.182 | 0.359 | 0.925 | 0.980 | 0.003 | True |
| Brent | Energia | 0.050 | Timestral-28M | 693 | 0.043 | 0.407 | 0.593 | 0.865 | 0.980 | 0.003 | True |
| Brent | Energia | 0.010 | Timestral-28M | 693 | 0.012 | 0.690 | 0.190 | 0.695 | 0.980 | 0.003 | True |
| Brent | Energia | 0.100 | Timestral-209M | 693 | 0.091 | 0.419 | 0.680 | 0.926 | 0.978 | 0.001 | True |
| Brent | Energia | 0.050 | Timestral-209M | 693 | 0.042 | 0.312 | 0.474 | 0.871 | 0.978 | 0.001 | True |
| Brent | Energia | 0.010 | Timestral-209M | 693 | 0.012 | 0.690 | 0.841 | 0.706 | 0.978 | 0.001 | True |
| Brent | Energia | 0.100 | TimesFM-3 | 693 | 0.085 | 0.182 | 0.359 | 0.934 | 0.984 | 0.009 | True |
| Brent | Energia | 0.100 | Chronos-2 | 693 | 0.114 | 0.229 | 0.453 | 0.940 | 0.983 | 0.006 | True |
| Brent | Energia | 0.050 | Chronos-2 | 693 | 0.051 | 0.951 | 0.982 | 0.891 | 0.983 | 0.006 | True |
| Brent | Energia | 0.010 | Chronos-2 | 693 | 0.012 | 0.690 | 0.190 | 0.695 | 0.983 | 0.006 | True |
| Gasolio | Energia | 0.100 | Simulazione storica | 708 | 0.116 | 0.170 | 0.263 | 1.000 | 1.000 |  | True |
| Gasolio | Energia | 0.050 | Simulazione storica | 708 | 0.056 | 0.437 | 0.396 | 1.000 | 1.000 |  | True |
| Gasolio | Energia | 0.010 | Simulazione storica | 708 | 0.016 | 0.171 | 0.144 | 1.000 | 1.000 |  | False |
| Gasolio | Energia | 0.100 | GARCH-t | 708 | 0.103 | 0.784 | 0.783 | 0.950 | 0.980 | 0.000 | True |
| Gasolio | Energia | 0.050 | GARCH-t | 708 | 0.045 | 0.551 | 0.770 | 0.906 | 0.980 | 0.000 | True |
| Gasolio | Energia | 0.010 | GARCH-t | 708 | 0.008 | 0.675 | 0.870 | 0.720 | 0.980 | 0.000 | True |
| Gasolio | Energia | 0.100 | GJR-GARCH-t | 708 | 0.105 | 0.690 | 0.711 | 0.953 | 0.981 | 0.000 | True |
| Gasolio | Energia | 0.050 | GJR-GARCH-t | 708 | 0.047 | 0.676 | 0.814 | 0.911 | 0.981 | 0.000 | True |
| Gasolio | Energia | 0.010 | GJR-GARCH-t | 708 | 0.008 | 0.675 | 0.870 | 0.738 | 0.981 | 0.000 | True |
| Gasolio | Energia | 0.100 | EGARCH-t | 708 | 0.099 | 0.920 | 0.919 | 0.954 | 0.981 | 0.000 | True |
| Gasolio | Energia | 0.050 | EGARCH-t | 708 | 0.049 | 0.945 | 0.976 | 0.918 | 0.981 | 0.000 | True |
| Gasolio | Energia | 0.010 | EGARCH-t | 708 | 0.008 | 0.675 | 0.870 | 0.746 | 0.981 | 0.000 | True |
| Gasolio | Energia | 0.100 | Timestral-28M | 708 | 0.092 | 0.462 | 0.763 | 0.965 | 0.984 | 0.002 | True |
| Gasolio | Energia | 0.050 | Timestral-28M | 708 | 0.042 | 0.339 | 0.612 | 0.918 | 0.984 | 0.002 | True |
| Gasolio | Energia | 0.010 | Timestral-28M | 708 | 0.008 | 0.675 | 0.870 | 0.710 | 0.984 | 0.002 | True |
| Gasolio | Energia | 0.100 | Timestral-209M | 708 | 0.095 | 0.631 | 0.881 | 0.960 | 0.981 | 0.000 | True |
| Gasolio | Energia | 0.050 | Timestral-209M | 708 | 0.044 | 0.439 | 0.700 | 0.917 | 0.981 | 0.000 | True |
| Gasolio | Energia | 0.010 | Timestral-209M | 708 | 0.007 | 0.407 | 0.684 | 0.707 | 0.981 | 0.000 | True |
| Gasolio | Energia | 0.100 | TimesFM-3 | 708 | 0.089 | 0.320 | 0.601 | 0.965 | 0.988 | 0.030 | True |
| Gasolio | Energia | 0.100 | Chronos-2 | 708 | 0.100 | 0.980 | 0.752 | 0.968 | 0.983 | 0.001 | True |
| Gasolio | Energia | 0.050 | Chronos-2 | 708 | 0.052 | 0.784 | 0.962 | 0.920 | 0.983 | 0.001 | True |
| Gasolio | Energia | 0.010 | Chronos-2 | 708 | 0.008 | 0.675 | 0.103 | 0.711 | 0.983 | 0.001 | True |
| Benzina | Energia | 0.100 | Simulazione storica | 708 | 0.102 | 0.881 | 0.953 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 0.050 | Simulazione storica | 708 | 0.052 | 0.784 | 0.962 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 0.010 | Simulazione storica | 708 | 0.017 | 0.091 | 0.195 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 0.100 | GARCH-t | 708 | 0.095 | 0.631 | 0.740 | 0.980 | 0.990 | 0.011 | True |
| Benzina | Energia | 0.050 | GARCH-t | 708 | 0.052 | 0.784 | 0.962 | 0.961 | 0.990 | 0.011 | True |
| Benzina | Energia | 0.010 | GARCH-t | 708 | 0.010 | 0.976 | 0.932 | 0.933 | 0.990 | 0.011 | True |
| Benzina | Energia | 0.100 | GJR-GARCH-t | 708 | 0.095 | 0.631 | 0.740 | 0.986 | 0.991 | 0.010 | True |
| Benzina | Energia | 0.050 | GJR-GARCH-t | 708 | 0.054 | 0.658 | 0.906 | 0.972 | 0.991 | 0.010 | True |
| Benzina | Energia | 0.010 | GJR-GARCH-t | 708 | 0.013 | 0.486 | 0.699 | 0.949 | 0.991 | 0.010 | True |
| Benzina | Energia | 0.100 | EGARCH-t | 708 | 0.092 | 0.462 | 0.689 | 0.981 | 0.989 | 0.003 | True |
| Benzina | Energia | 0.050 | EGARCH-t | 708 | 0.055 | 0.541 | 0.700 | 0.965 | 0.989 | 0.003 | True |
| Benzina | Energia | 0.010 | EGARCH-t | 708 | 0.013 | 0.486 | 0.199 | 0.931 | 0.989 | 0.003 | True |
| Benzina | Energia | 0.100 | Timestral-28M | 708 | 0.085 | 0.166 | 0.330 | 0.976 | 0.988 | 0.004 | True |
| Benzina | Energia | 0.050 | Timestral-28M | 708 | 0.048 | 0.808 | 0.931 | 0.955 | 0.988 | 0.004 | True |
| Benzina | Energia | 0.010 | Timestral-28M | 708 | 0.013 | 0.486 | 0.199 | 0.912 | 0.988 | 0.004 | True |
| Benzina | Energia | 0.100 | Timestral-209M | 708 | 0.086 | 0.210 | 0.375 | 0.970 | 0.985 | 0.001 | True |
| Benzina | Energia | 0.050 | Timestral-209M | 708 | 0.048 | 0.808 | 0.931 | 0.944 | 0.985 | 0.001 | True |
| Benzina | Energia | 0.010 | Timestral-209M | 708 | 0.010 | 0.976 | 0.932 | 0.915 | 0.985 | 0.001 | True |
| Benzina | Energia | 0.100 | TimesFM-3 | 708 | 0.082 | 0.099 | 0.238 | 0.981 | 0.991 | 0.046 | True |
| Benzina | Energia | 0.100 | Chronos-2 | 708 | 0.097 | 0.821 | 0.927 | 0.987 | 0.988 | 0.008 | True |
| Benzina | Energia | 0.050 | Chronos-2 | 708 | 0.052 | 0.784 | 0.726 | 0.976 | 0.988 | 0.008 | True |
| Benzina | Energia | 0.010 | Chronos-2 | 708 | 0.013 | 0.486 | 0.199 | 0.929 | 0.988 | 0.008 | True |
| Gas naturale | Energia | 0.100 | Simulazione storica | 708 | 0.097 | 0.821 | 0.963 | 1.000 | 1.000 |  | True |
| Gas naturale | Energia | 0.050 | Simulazione storica | 708 | 0.052 | 0.784 | 0.726 | 1.000 | 1.000 |  | True |
| Gas naturale | Energia | 0.010 | Simulazione storica | 708 | 0.013 | 0.486 | 0.699 | 1.000 | 1.000 |  | True |
| Gas naturale | Energia | 0.100 | GARCH-t | 708 | 0.105 | 0.690 | 0.732 | 0.995 | 1.010 | 0.148 | False |
| Gas naturale | Energia | 0.050 | GARCH-t | 708 | 0.037 | 0.090 | 0.140 | 0.967 | 1.010 | 0.148 | False |
| Gas naturale | Energia | 0.010 | GARCH-t | 708 | 0.010 | 0.976 | 0.932 | 0.760 | 1.010 | 0.148 | True |
| Gas naturale | Energia | 0.100 | GJR-GARCH-t | 708 | 0.105 | 0.690 | 0.893 | 0.994 | 1.009 | 0.188 | False |
| Gas naturale | Energia | 0.050 | GJR-GARCH-t | 708 | 0.041 | 0.255 | 0.164 | 0.964 | 1.009 | 0.188 | False |
| Gas naturale | Energia | 0.010 | GJR-GARCH-t | 708 | 0.010 | 0.976 | 0.932 | 0.754 | 1.009 | 0.188 | True |
| Gas naturale | Energia | 0.100 | EGARCH-t | 708 | 0.106 | 0.602 | 0.871 | 0.971 | 0.997 | 0.459 | False |
| Gas naturale | Energia | 0.050 | EGARCH-t | 708 | 0.040 | 0.186 | 0.292 | 0.940 | 0.997 | 0.459 | True |
| Gas naturale | Energia | 0.010 | EGARCH-t | 708 | 0.010 | 0.976 | 0.932 | 0.738 | 0.997 | 0.459 | True |
| Gas naturale | Energia | 0.100 | Timestral-28M | 708 | 0.097 | 0.821 | 0.938 | 0.951 | 0.994 | 0.168 | True |
| Gas naturale | Energia | 0.050 | Timestral-28M | 708 | 0.044 | 0.439 | 0.708 | 0.921 | 0.994 | 0.168 | True |
| Gas naturale | Energia | 0.010 | Timestral-28M | 708 | 0.010 | 0.976 | 0.932 | 0.732 | 0.994 | 0.168 | True |
| Gas naturale | Energia | 0.100 | Timestral-209M | 708 | 0.110 | 0.374 | 0.241 | 0.955 | 0.994 | 0.093 | True |
| Gas naturale | Energia | 0.050 | Timestral-209M | 708 | 0.044 | 0.439 | 0.625 | 0.917 | 0.994 | 0.093 | True |
| Gas naturale | Energia | 0.010 | Timestral-209M | 708 | 0.011 | 0.734 | 0.861 | 0.744 | 0.994 | 0.093 | True |
| Gas naturale | Energia | 0.100 | TimesFM-3 | 708 | 0.112 | 0.312 | 0.334 | 0.961 | 0.999 | 0.864 | True |
| Gas naturale | Energia | 0.100 | Chronos-2 | 708 | 0.112 | 0.312 | 0.578 | 0.962 | 0.994 | 0.142 | True |
| Gas naturale | Energia | 0.050 | Chronos-2 | 708 | 0.052 | 0.784 | 0.713 | 0.918 | 0.994 | 0.142 | True |
| Gas naturale | Energia | 0.010 | Chronos-2 | 708 | 0.011 | 0.734 | 0.861 | 0.754 | 0.994 | 0.142 | True |
| Oro | Metalli preziosi | 0.100 | Simulazione storica | 708 | 0.119 | 0.107 | 0.256 | 1.000 | 1.000 |  | True |
| Oro | Metalli preziosi | 0.050 | Simulazione storica | 708 | 0.066 | 0.056 | 0.124 | 1.000 | 1.000 |  | True |
| Oro | Metalli preziosi | 0.010 | Simulazione storica | 708 | 0.023 | 0.004 | 0.011 | 1.000 | 1.000 |  | False |
| Oro | Metalli preziosi | 0.100 | GARCH-t | 708 | 0.116 | 0.170 | 0.386 | 0.966 | 0.995 | 0.329 | True |
| Oro | Metalli preziosi | 0.050 | GARCH-t | 708 | 0.066 | 0.056 | 0.124 | 0.969 | 0.995 | 0.329 | True |
| Oro | Metalli preziosi | 0.010 | GARCH-t | 708 | 0.017 | 0.091 | 0.195 | 0.899 | 0.995 | 0.329 | True |
| Oro | Metalli preziosi | 0.100 | GJR-GARCH-t | 708 | 0.119 | 0.107 | 0.260 | 0.966 | 0.995 | 0.289 | True |
| Oro | Metalli preziosi | 0.050 | GJR-GARCH-t | 708 | 0.066 | 0.056 | 0.124 | 0.964 | 0.995 | 0.289 | True |
| Oro | Metalli preziosi | 0.010 | GJR-GARCH-t | 708 | 0.017 | 0.091 | 0.195 | 0.870 | 0.995 | 0.289 | True |
| Oro | Metalli preziosi | 0.100 | EGARCH-t | 708 | 0.114 | 0.211 | 0.456 | 0.964 | 0.995 | 0.239 | True |
| Oro | Metalli preziosi | 0.050 | EGARCH-t | 708 | 0.062 | 0.152 | 0.160 | 0.961 | 0.995 | 0.239 | True |
| Oro | Metalli preziosi | 0.010 | EGARCH-t | 708 | 0.016 | 0.171 | 0.329 | 0.858 | 0.995 | 0.239 | True |
| Oro | Metalli preziosi | 0.100 | Timestral-28M | 708 | 0.106 | 0.602 | 0.632 | 0.967 | 0.991 | 0.028 | True |
| Oro | Metalli preziosi | 0.050 | Timestral-28M | 708 | 0.055 | 0.541 | 0.544 | 0.957 | 0.991 | 0.028 | True |
| Oro | Metalli preziosi | 0.010 | Timestral-28M | 708 | 0.013 | 0.486 | 0.699 | 0.856 | 0.991 | 0.028 | True |
| Oro | Metalli preziosi | 0.100 | Timestral-209M | 708 | 0.105 | 0.690 | 0.711 | 0.964 | 0.993 | 0.105 | True |
| Oro | Metalli preziosi | 0.050 | Timestral-209M | 708 | 0.051 | 0.918 | 0.776 | 0.945 | 0.993 | 0.105 | True |
| Oro | Metalli preziosi | 0.010 | Timestral-209M | 708 | 0.013 | 0.486 | 0.699 | 0.834 | 0.993 | 0.105 | True |
| Oro | Metalli preziosi | 0.100 | TimesFM-3 | 708 | 0.107 | 0.519 | 0.550 | 0.980 | 0.996 | 0.389 | True |
| Oro | Metalli preziosi | 0.100 | Chronos-2 | 708 | 0.116 | 0.170 | 0.332 | 0.968 | 0.995 | 0.209 | True |
| Oro | Metalli preziosi | 0.050 | Chronos-2 | 708 | 0.059 | 0.268 | 0.511 | 0.968 | 0.995 | 0.209 | True |
| Oro | Metalli preziosi | 0.010 | Chronos-2 | 708 | 0.017 | 0.091 | 0.195 | 0.890 | 0.995 | 0.209 | True |
| Argento | Metalli preziosi | 0.100 | Simulazione storica | 708 | 0.127 | 0.020 | 0.060 | 1.000 | 1.000 |  | False |
| Argento | Metalli preziosi | 0.050 | Simulazione storica | 708 | 0.072 | 0.011 | 0.040 | 1.000 | 1.000 |  | True |
| Argento | Metalli preziosi | 0.010 | Simulazione storica | 708 | 0.021 | 0.009 | 0.021 | 1.000 | 1.000 |  | True |
| Argento | Metalli preziosi | 0.100 | GARCH-t | 708 | 0.109 | 0.443 | 0.281 | 0.915 | 0.977 | 0.001 | True |
| Argento | Metalli preziosi | 0.050 | GARCH-t | 708 | 0.065 | 0.080 | 0.175 | 0.896 | 0.977 | 0.001 | True |
| Argento | Metalli preziosi | 0.010 | GARCH-t | 708 | 0.011 | 0.734 | 0.190 | 0.895 | 0.977 | 0.001 | False |
| Argento | Metalli preziosi | 0.100 | GJR-GARCH-t | 708 | 0.109 | 0.443 | 0.281 | 0.905 | 0.972 | 0.000 | True |
| Argento | Metalli preziosi | 0.050 | GJR-GARCH-t | 708 | 0.064 | 0.111 | 0.239 | 0.872 | 0.972 | 0.000 | True |
| Argento | Metalli preziosi | 0.010 | GJR-GARCH-t | 708 | 0.008 | 0.675 | 0.103 | 0.847 | 0.972 | 0.000 | True |
| Argento | Metalli preziosi | 0.100 | EGARCH-t | 708 | 0.107 | 0.519 | 0.341 | 0.908 | 0.972 | 0.000 | True |
| Argento | Metalli preziosi | 0.050 | EGARCH-t | 708 | 0.059 | 0.268 | 0.511 | 0.876 | 0.972 | 0.000 | True |
| Argento | Metalli preziosi | 0.010 | EGARCH-t | 708 | 0.008 | 0.675 | 0.103 | 0.840 | 0.972 | 0.000 | True |
| Argento | Metalli preziosi | 0.100 | Timestral-28M | 708 | 0.096 | 0.724 | 0.475 | 0.898 | 0.970 | 0.000 | True |
| Argento | Metalli preziosi | 0.050 | Timestral-28M | 708 | 0.055 | 0.541 | 0.825 | 0.874 | 0.970 | 0.000 | True |
| Argento | Metalli preziosi | 0.010 | Timestral-28M | 708 | 0.007 | 0.407 | 0.054 | 0.835 | 0.970 | 0.000 | True |
| Argento | Metalli preziosi | 0.100 | Timestral-209M | 708 | 0.096 | 0.724 | 0.741 | 0.902 | 0.972 | 0.001 | True |
| Argento | Metalli preziosi | 0.050 | Timestral-209M | 708 | 0.055 | 0.541 | 0.825 | 0.875 | 0.972 | 0.001 | True |
| Argento | Metalli preziosi | 0.010 | Timestral-209M | 708 | 0.006 | 0.205 | 0.021 | 0.842 | 0.972 | 0.001 | True |
| Argento | Metalli preziosi | 0.100 | TimesFM-3 | 708 | 0.102 | 0.881 | 0.596 | 0.922 | 0.977 | 0.001 | True |
| Argento | Metalli preziosi | 0.100 | Chronos-2 | 708 | 0.092 | 0.462 | 0.263 | 0.910 | 0.976 | 0.000 | True |
| Argento | Metalli preziosi | 0.050 | Chronos-2 | 708 | 0.049 | 0.945 | 0.817 | 0.875 | 0.976 | 0.000 | True |
| Argento | Metalli preziosi | 0.010 | Chronos-2 | 708 | 0.006 | 0.205 | 0.021 | 0.923 | 0.976 | 0.000 | False |
| Rame | Metalli industriali | 0.100 | Simulazione storica | 708 | 0.106 | 0.602 | 0.803 | 1.000 | 1.000 |  | True |
| Rame | Metalli industriali | 0.050 | Simulazione storica | 708 | 0.064 | 0.111 | 0.281 | 1.000 | 1.000 |  | False |
| Rame | Metalli industriali | 0.010 | Simulazione storica | 708 | 0.020 | 0.021 | 0.006 | 1.000 | 1.000 |  | True |
| Rame | Metalli industriali | 0.100 | GARCH-t | 708 | 0.114 | 0.211 | 0.107 | 0.992 | 1.008 | 0.077 | True |
| Rame | Metalli industriali | 0.050 | GARCH-t | 708 | 0.059 | 0.268 | 0.513 | 0.962 | 1.008 | 0.077 | True |
| Rame | Metalli industriali | 0.010 | GARCH-t | 708 | 0.016 | 0.171 | 0.144 | 0.963 | 1.008 | 0.077 | True |
| Rame | Metalli industriali | 0.100 | GJR-GARCH-t | 708 | 0.114 | 0.211 | 0.107 | 0.990 | 1.007 | 0.083 | True |
| Rame | Metalli industriali | 0.050 | GJR-GARCH-t | 708 | 0.058 | 0.346 | 0.588 | 0.959 | 1.007 | 0.083 | True |
| Rame | Metalli industriali | 0.010 | GJR-GARCH-t | 708 | 0.013 | 0.486 | 0.199 | 0.961 | 1.007 | 0.083 | True |
| Rame | Metalli industriali | 0.100 | EGARCH-t | 708 | 0.103 | 0.784 | 0.290 | 0.975 | 0.997 | 0.340 | True |
| Rame | Metalli industriali | 0.050 | EGARCH-t | 708 | 0.054 | 0.658 | 0.726 | 0.946 | 0.997 | 0.340 | True |
| Rame | Metalli industriali | 0.010 | EGARCH-t | 708 | 0.014 | 0.299 | 0.180 | 0.985 | 0.997 | 0.340 | True |
| Rame | Metalli industriali | 0.100 | Timestral-28M | 708 | 0.089 | 0.320 | 0.450 | 0.957 | 0.993 | 0.120 | True |
| Rame | Metalli industriali | 0.050 | Timestral-28M | 708 | 0.038 | 0.131 | 0.216 | 0.933 | 0.993 | 0.120 | True |
| Rame | Metalli industriali | 0.010 | Timestral-28M | 708 | 0.013 | 0.486 | 0.199 | 0.983 | 0.993 | 0.120 | True |
| Rame | Metalli industriali | 0.100 | Timestral-209M | 708 | 0.089 | 0.320 | 0.259 | 0.960 | 0.995 | 0.158 | True |
| Rame | Metalli industriali | 0.050 | Timestral-209M | 708 | 0.041 | 0.255 | 0.406 | 0.941 | 0.995 | 0.158 | False |
| Rame | Metalli industriali | 0.010 | Timestral-209M | 708 | 0.013 | 0.486 | 0.199 | 0.984 | 0.995 | 0.158 | True |
| Rame | Metalli industriali | 0.100 | TimesFM-3 | 708 | 0.106 | 0.602 | 0.205 | 0.966 | 0.998 | 0.592 | True |
| Rame | Metalli industriali | 0.100 | Chronos-2 | 708 | 0.092 | 0.462 | 0.263 | 0.978 | 0.996 | 0.297 | True |
| Rame | Metalli industriali | 0.050 | Chronos-2 | 708 | 0.035 | 0.059 | 0.095 | 0.959 | 0.996 | 0.297 | False |
| Rame | Metalli industriali | 0.010 | Chronos-2 | 708 | 0.011 | 0.734 | 0.190 | 0.977 | 0.996 | 0.297 | True |
| Grano | Cereali | 0.100 | Simulazione storica | 707 | 0.099 | 0.930 | 0.444 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 0.050 | Simulazione storica | 707 | 0.044 | 0.444 | 0.099 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 0.010 | Simulazione storica | 707 | 0.010 | 0.979 | 0.932 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 0.100 | GARCH-t | 707 | 0.072 | 0.010 | 0.027 | 0.989 | 0.994 | 0.077 | True |
| Grano | Cereali | 0.050 | GARCH-t | 707 | 0.027 | 0.002 | 0.007 | 1.009 | 0.994 | 0.077 | False |
| Grano | Cereali | 0.010 | GARCH-t | 707 | 0.000 | 0.000 | 0.001 | 1.085 | 0.994 | 0.077 | False |
| Grano | Cereali | 0.100 | GJR-GARCH-t | 707 | 0.075 | 0.021 | 0.058 | 0.990 | 0.994 | 0.083 | True |
| Grano | Cereali | 0.050 | GJR-GARCH-t | 707 | 0.027 | 0.002 | 0.007 | 1.009 | 0.994 | 0.083 | False |
| Grano | Cereali | 0.010 | GJR-GARCH-t | 707 | 0.000 | 0.000 | 0.001 | 1.083 | 0.994 | 0.083 | False |
| Grano | Cereali | 0.100 | EGARCH-t | 707 | 0.076 | 0.030 | 0.058 | 0.989 | 0.994 | 0.089 | True |
| Grano | Cereali | 0.050 | EGARCH-t | 707 | 0.025 | 0.001 | 0.003 | 1.012 | 0.994 | 0.089 | False |
| Grano | Cereali | 0.010 | EGARCH-t | 707 | 0.000 | 0.000 | 0.001 | 1.089 | 0.994 | 0.089 | False |
| Grano | Cereali | 0.100 | Timestral-28M | 707 | 0.078 | 0.041 | 0.083 | 0.987 | 0.993 | 0.025 | True |
| Grano | Cereali | 0.050 | Timestral-28M | 707 | 0.028 | 0.004 | 0.014 | 0.990 | 0.993 | 0.025 | True |
| Grano | Cereali | 0.010 | Timestral-28M | 707 | 0.001 | 0.004 | 0.016 | 0.997 | 0.993 | 0.025 | True |
| Grano | Cereali | 0.100 | Timestral-209M | 707 | 0.078 | 0.041 | 0.083 | 0.984 | 0.992 | 0.018 | True |
| Grano | Cereali | 0.050 | Timestral-209M | 707 | 0.027 | 0.002 | 0.007 | 0.992 | 0.992 | 0.018 | True |
| Grano | Cereali | 0.010 | Timestral-209M | 707 | 0.000 | 0.000 | 0.001 | 1.025 | 0.992 | 0.018 | False |
| Grano | Cereali | 0.100 | TimesFM-3 | 707 | 0.075 | 0.021 | 0.058 | 0.975 | 0.989 | 0.019 | True |
| Grano | Cereali | 0.100 | Chronos-2 | 707 | 0.083 | 0.132 | 0.193 | 0.997 | 0.993 | 0.028 | True |
| Grano | Cereali | 0.050 | Chronos-2 | 707 | 0.030 | 0.008 | 0.025 | 1.000 | 0.993 | 0.028 | True |
| Grano | Cereali | 0.010 | Chronos-2 | 707 | 0.001 | 0.004 | 0.016 | 1.051 | 0.993 | 0.028 | True |
| Mais | Cereali | 0.100 | Simulazione storica | 707 | 0.095 | 0.640 | 0.488 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 0.050 | Simulazione storica | 707 | 0.051 | 0.911 | 0.700 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 0.010 | Simulazione storica | 707 | 0.017 | 0.090 | 0.193 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 0.100 | GARCH-t | 707 | 0.083 | 0.132 | 0.322 | 0.997 | 0.998 | 0.544 | True |
| Mais | Cereali | 0.050 | GARCH-t | 707 | 0.041 | 0.259 | 0.179 | 1.006 | 0.998 | 0.544 | True |
| Mais | Cereali | 0.010 | GARCH-t | 707 | 0.008 | 0.678 | 0.871 | 0.959 | 0.998 | 0.544 | True |
| Mais | Cereali | 0.100 | GJR-GARCH-t | 707 | 0.086 | 0.214 | 0.458 | 0.997 | 0.998 | 0.565 | True |
| Mais | Cereali | 0.050 | GJR-GARCH-t | 707 | 0.042 | 0.344 | 0.247 | 1.005 | 0.998 | 0.565 | True |
| Mais | Cereali | 0.010 | GJR-GARCH-t | 707 | 0.008 | 0.678 | 0.871 | 0.961 | 0.998 | 0.565 | True |
| Mais | Cereali | 0.100 | EGARCH-t | 707 | 0.079 | 0.057 | 0.156 | 1.001 | 0.996 | 0.318 | True |
| Mais | Cereali | 0.050 | EGARCH-t | 707 | 0.041 | 0.259 | 0.179 | 1.007 | 0.996 | 0.318 | True |
| Mais | Cereali | 0.010 | EGARCH-t | 707 | 0.008 | 0.678 | 0.871 | 0.960 | 0.996 | 0.318 | True |
| Mais | Cereali | 0.100 | Timestral-28M | 707 | 0.079 | 0.057 | 0.154 | 0.994 | 0.995 | 0.216 | True |
| Mais | Cereali | 0.050 | Timestral-28M | 707 | 0.040 | 0.189 | 0.123 | 0.993 | 0.995 | 0.216 | True |
| Mais | Cereali | 0.010 | Timestral-28M | 707 | 0.008 | 0.678 | 0.871 | 0.962 | 0.995 | 0.216 | True |
| Mais | Cereali | 0.100 | Timestral-209M | 707 | 0.075 | 0.021 | 0.058 | 0.996 | 0.995 | 0.158 | True |
| Mais | Cereali | 0.050 | Timestral-209M | 707 | 0.038 | 0.133 | 0.111 | 0.993 | 0.995 | 0.158 | True |
| Mais | Cereali | 0.010 | Timestral-209M | 707 | 0.007 | 0.409 | 0.686 | 0.975 | 0.995 | 0.158 | True |
| Mais | Cereali | 0.100 | TimesFM-3 | 707 | 0.091 | 0.394 | 0.658 | 0.996 | 0.998 | 0.698 | True |
| Mais | Cereali | 0.100 | Chronos-2 | 707 | 0.081 | 0.076 | 0.160 | 0.983 | 0.995 | 0.221 | True |
| Mais | Cereali | 0.050 | Chronos-2 | 707 | 0.031 | 0.014 | 0.023 | 0.983 | 0.995 | 0.221 | True |
| Mais | Cereali | 0.010 | Chronos-2 | 707 | 0.007 | 0.409 | 0.686 | 1.024 | 0.995 | 0.221 | False |
| Soia | Cereali | 0.100 | Simulazione storica | 707 | 0.091 | 0.394 | 0.589 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 0.050 | Simulazione storica | 707 | 0.047 | 0.682 | 0.858 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 0.010 | Simulazione storica | 707 | 0.011 | 0.731 | 0.860 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 0.100 | GARCH-t | 707 | 0.089 | 0.326 | 0.598 | 1.003 | 1.000 | 0.929 | True |
| Soia | Cereali | 0.050 | GARCH-t | 707 | 0.035 | 0.060 | 0.169 | 0.982 | 1.000 | 0.929 | True |
| Soia | Cereali | 0.010 | GARCH-t | 707 | 0.010 | 0.979 | 0.932 | 0.957 | 1.000 | 0.929 | True |
| Soia | Cereali | 0.100 | GJR-GARCH-t | 707 | 0.091 | 0.394 | 0.658 | 1.004 | 1.000 | 0.945 | True |
| Soia | Cereali | 0.050 | GJR-GARCH-t | 707 | 0.040 | 0.189 | 0.419 | 0.987 | 1.000 | 0.945 | True |
| Soia | Cereali | 0.010 | GJR-GARCH-t | 707 | 0.010 | 0.979 | 0.932 | 0.962 | 1.000 | 0.945 | True |
| Soia | Cereali | 0.100 | EGARCH-t | 707 | 0.088 | 0.266 | 0.515 | 0.998 | 0.999 | 0.851 | True |
| Soia | Cereali | 0.050 | EGARCH-t | 707 | 0.031 | 0.014 | 0.044 | 0.989 | 0.999 | 0.851 | True |
| Soia | Cereali | 0.010 | EGARCH-t | 707 | 0.010 | 0.979 | 0.932 | 0.965 | 0.999 | 0.851 | True |
| Soia | Cereali | 0.100 | Timestral-28M | 707 | 0.088 | 0.266 | 0.431 | 0.999 | 0.999 | 0.866 | True |
| Soia | Cereali | 0.050 | Timestral-28M | 707 | 0.031 | 0.014 | 0.044 | 0.982 | 0.999 | 0.866 | True |
| Soia | Cereali | 0.010 | Timestral-28M | 707 | 0.010 | 0.979 | 0.932 | 0.953 | 0.999 | 0.866 | True |
| Soia | Cereali | 0.100 | Timestral-209M | 707 | 0.085 | 0.170 | 0.342 | 0.999 | 0.999 | 0.782 | True |
| Soia | Cereali | 0.050 | Timestral-209M | 707 | 0.028 | 0.004 | 0.009 | 0.992 | 0.999 | 0.782 | True |
| Soia | Cereali | 0.010 | Timestral-209M | 707 | 0.010 | 0.979 | 0.932 | 0.967 | 0.999 | 0.782 | True |
| Soia | Cereali | 0.100 | TimesFM-3 | 707 | 0.093 | 0.552 | 0.519 | 1.000 | 1.001 | 0.870 | True |
| Soia | Cereali | 0.100 | Chronos-2 | 707 | 0.075 | 0.021 | 0.069 | 1.026 | 1.004 | 0.299 | False |
| Soia | Cereali | 0.050 | Chronos-2 | 707 | 0.033 | 0.023 | 0.035 | 1.029 | 1.004 | 0.299 | False |
| Soia | Cereali | 0.010 | Chronos-2 | 707 | 0.008 | 0.678 | 0.871 | 0.996 | 1.004 | 0.299 | True |
| Caffe | Soft e bestiame | 0.100 | Simulazione storica | 708 | 0.106 | 0.602 | 0.205 | 1.000 | 1.000 |  | True |
| Caffe | Soft e bestiame | 0.050 | Simulazione storica | 708 | 0.058 | 0.346 | 0.366 | 1.000 | 1.000 |  | True |
| Caffe | Soft e bestiame | 0.010 | Simulazione storica | 708 | 0.014 | 0.299 | 0.505 | 1.000 | 1.000 |  | True |
| Caffe | Soft e bestiame | 0.100 | GARCH-t | 708 | 0.097 | 0.821 | 0.209 | 0.987 | 0.998 | 0.582 | True |
| Caffe | Soft e bestiame | 0.050 | GARCH-t | 708 | 0.056 | 0.437 | 0.453 | 0.999 | 0.998 | 0.582 | True |
| Caffe | Soft e bestiame | 0.010 | GARCH-t | 708 | 0.008 | 0.675 | 0.870 | 0.932 | 0.998 | 0.582 | True |
| Caffe | Soft e bestiame | 0.100 | GJR-GARCH-t | 708 | 0.110 | 0.374 | 0.552 | 0.986 | 0.997 | 0.383 | True |
| Caffe | Soft e bestiame | 0.050 | GJR-GARCH-t | 708 | 0.058 | 0.346 | 0.366 | 1.001 | 0.997 | 0.383 | True |
| Caffe | Soft e bestiame | 0.010 | GJR-GARCH-t | 708 | 0.014 | 0.299 | 0.180 | 0.927 | 0.997 | 0.383 | True |
| Caffe | Soft e bestiame | 0.100 | EGARCH-t | 708 | 0.114 | 0.211 | 0.406 | 0.983 | 0.996 | 0.231 | True |
| Caffe | Soft e bestiame | 0.050 | EGARCH-t | 708 | 0.058 | 0.346 | 0.366 | 0.994 | 0.996 | 0.231 | True |
| Caffe | Soft e bestiame | 0.010 | EGARCH-t | 708 | 0.014 | 0.299 | 0.180 | 0.941 | 0.996 | 0.231 | True |
| Caffe | Soft e bestiame | 0.100 | Timestral-28M | 708 | 0.103 | 0.784 | 0.290 | 0.985 | 1.000 | 0.921 | True |
| Caffe | Soft e bestiame | 0.050 | Timestral-28M | 708 | 0.061 | 0.204 | 0.217 | 0.984 | 1.000 | 0.921 | True |
| Caffe | Soft e bestiame | 0.010 | Timestral-28M | 708 | 0.017 | 0.091 | 0.102 | 0.919 | 1.000 | 0.921 | True |
| Caffe | Soft e bestiame | 0.100 | Timestral-209M | 708 | 0.105 | 0.690 | 0.246 | 0.985 | 0.998 | 0.566 | True |
| Caffe | Soft e bestiame | 0.050 | Timestral-209M | 708 | 0.064 | 0.111 | 0.115 | 0.982 | 0.998 | 0.566 | True |
| Caffe | Soft e bestiame | 0.010 | Timestral-209M | 708 | 0.011 | 0.734 | 0.190 | 0.897 | 0.998 | 0.566 | True |
| Caffe | Soft e bestiame | 0.100 | TimesFM-3 | 708 | 0.103 | 0.784 | 0.290 | 0.989 | 1.001 | 0.816 | True |
| Caffe | Soft e bestiame | 0.100 | Chronos-2 | 708 | 0.092 | 0.462 | 0.263 | 0.999 | 1.001 | 0.860 | True |
| Caffe | Soft e bestiame | 0.050 | Chronos-2 | 708 | 0.052 | 0.784 | 0.713 | 1.015 | 1.001 | 0.860 | True |
| Caffe | Soft e bestiame | 0.010 | Chronos-2 | 708 | 0.007 | 0.407 | 0.684 | 0.931 | 1.001 | 0.860 | True |
| Zucchero | Soft e bestiame | 0.100 | Simulazione storica | 708 | 0.090 | 0.387 | 0.596 | 1.000 | 1.000 |  | True |
| Zucchero | Soft e bestiame | 0.050 | Simulazione storica | 708 | 0.048 | 0.808 | 0.580 | 1.000 | 1.000 |  | True |
| Zucchero | Soft e bestiame | 0.010 | Simulazione storica | 708 | 0.010 | 0.976 | 0.154 | 1.000 | 1.000 |  | False |
| Zucchero | Soft e bestiame | 0.100 | GARCH-t | 708 | 0.086 | 0.210 | 0.375 | 1.000 | 0.997 | 0.330 | True |
| Zucchero | Soft e bestiame | 0.050 | GARCH-t | 708 | 0.041 | 0.255 | 0.406 | 0.999 | 0.997 | 0.330 | True |
| Zucchero | Soft e bestiame | 0.010 | GARCH-t | 708 | 0.006 | 0.205 | 0.021 | 0.945 | 0.997 | 0.330 | False |
| Zucchero | Soft e bestiame | 0.100 | GJR-GARCH-t | 708 | 0.089 | 0.320 | 0.585 | 1.003 | 0.998 | 0.404 | True |
| Zucchero | Soft e bestiame | 0.050 | GJR-GARCH-t | 708 | 0.041 | 0.255 | 0.406 | 1.013 | 0.998 | 0.404 | True |
| Zucchero | Soft e bestiame | 0.010 | GJR-GARCH-t | 708 | 0.006 | 0.205 | 0.021 | 0.956 | 0.998 | 0.404 | False |
| Zucchero | Soft e bestiame | 0.100 | EGARCH-t | 708 | 0.083 | 0.129 | 0.316 | 1.002 | 0.998 | 0.509 | True |
| Zucchero | Soft e bestiame | 0.050 | EGARCH-t | 708 | 0.038 | 0.131 | 0.216 | 1.016 | 0.998 | 0.509 | False |
| Zucchero | Soft e bestiame | 0.010 | EGARCH-t | 708 | 0.006 | 0.205 | 0.021 | 0.971 | 0.998 | 0.509 | False |
| Zucchero | Soft e bestiame | 0.100 | Timestral-28M | 708 | 0.093 | 0.543 | 0.829 | 1.000 | 0.998 | 0.379 | True |
| Zucchero | Soft e bestiame | 0.050 | Timestral-28M | 708 | 0.045 | 0.551 | 0.755 | 0.999 | 0.998 | 0.379 | True |
| Zucchero | Soft e bestiame | 0.010 | Timestral-28M | 708 | 0.008 | 0.675 | 0.002 | 0.906 | 0.998 | 0.379 | True |
| Zucchero | Soft e bestiame | 0.100 | Timestral-209M | 708 | 0.090 | 0.387 | 0.685 | 1.000 | 0.998 | 0.367 | True |
| Zucchero | Soft e bestiame | 0.050 | Timestral-209M | 708 | 0.044 | 0.439 | 0.640 | 1.001 | 0.998 | 0.367 | True |
| Zucchero | Soft e bestiame | 0.010 | Timestral-209M | 708 | 0.006 | 0.205 | 0.021 | 0.906 | 0.998 | 0.367 | True |
| Zucchero | Soft e bestiame | 0.100 | TimesFM-3 | 708 | 0.096 | 0.724 | 0.741 | 0.997 | 0.997 | 0.355 | True |
| Zucchero | Soft e bestiame | 0.100 | Chronos-2 | 708 | 0.086 | 0.210 | 0.452 | 1.010 | 0.999 | 0.704 | True |
| Zucchero | Soft e bestiame | 0.050 | Chronos-2 | 708 | 0.040 | 0.186 | 0.303 | 1.005 | 0.999 | 0.704 | True |
| Zucchero | Soft e bestiame | 0.010 | Chronos-2 | 708 | 0.006 | 0.205 | 0.021 | 0.916 | 0.999 | 0.704 | True |
| Cacao | Soft e bestiame | 0.100 | Simulazione storica | 708 | 0.121 | 0.065 | 0.057 | 1.000 | 1.000 |  | True |
| Cacao | Soft e bestiame | 0.050 | Simulazione storica | 708 | 0.065 | 0.080 | 0.054 | 1.000 | 1.000 |  | True |
| Cacao | Soft e bestiame | 0.010 | Simulazione storica | 708 | 0.023 | 0.004 | 0.010 | 1.000 | 1.000 |  | True |
| Cacao | Soft e bestiame | 0.100 | GARCH-t | 708 | 0.105 | 0.690 | 0.253 | 0.955 | 0.988 | 0.038 | True |
| Cacao | Soft e bestiame | 0.050 | GARCH-t | 708 | 0.061 | 0.204 | 0.433 | 0.936 | 0.988 | 0.038 | True |
| Cacao | Soft e bestiame | 0.010 | GARCH-t | 708 | 0.017 | 0.091 | 0.195 | 0.850 | 0.988 | 0.038 | True |
| Cacao | Soft e bestiame | 0.100 | GJR-GARCH-t | 708 | 0.100 | 0.980 | 0.316 | 0.958 | 0.988 | 0.040 | True |
| Cacao | Soft e bestiame | 0.050 | GJR-GARCH-t | 708 | 0.058 | 0.346 | 0.588 | 0.944 | 0.988 | 0.040 | True |
| Cacao | Soft e bestiame | 0.010 | GJR-GARCH-t | 708 | 0.020 | 0.021 | 0.053 | 0.857 | 0.988 | 0.040 | True |
| Cacao | Soft e bestiame | 0.100 | EGARCH-t | 708 | 0.105 | 0.690 | 0.253 | 0.959 | 0.988 | 0.024 | True |
| Cacao | Soft e bestiame | 0.050 | EGARCH-t | 708 | 0.062 | 0.152 | 0.268 | 0.949 | 0.988 | 0.024 | True |
| Cacao | Soft e bestiame | 0.010 | EGARCH-t | 708 | 0.021 | 0.009 | 0.024 | 0.884 | 0.988 | 0.024 | True |
| Cacao | Soft e bestiame | 0.100 | Timestral-28M | 708 | 0.100 | 0.980 | 0.752 | 0.957 | 0.992 | 0.151 | True |
| Cacao | Soft e bestiame | 0.050 | Timestral-28M | 708 | 0.051 | 0.918 | 0.987 | 0.937 | 0.992 | 0.151 | True |
| Cacao | Soft e bestiame | 0.010 | Timestral-28M | 708 | 0.011 | 0.734 | 0.861 | 0.809 | 0.992 | 0.151 | True |
| Cacao | Soft e bestiame | 0.100 | Timestral-209M | 708 | 0.113 | 0.258 | 0.409 | 0.958 | 0.988 | 0.017 | True |
| Cacao | Soft e bestiame | 0.050 | Timestral-209M | 708 | 0.055 | 0.541 | 0.825 | 0.931 | 0.988 | 0.017 | True |
| Cacao | Soft e bestiame | 0.010 | Timestral-209M | 708 | 0.011 | 0.734 | 0.861 | 0.824 | 0.988 | 0.017 | True |
| Cacao | Soft e bestiame | 0.100 | TimesFM-3 | 708 | 0.100 | 0.980 | 0.890 | 0.956 | 0.992 | 0.159 | True |
| Cacao | Soft e bestiame | 0.100 | Chronos-2 | 708 | 0.095 | 0.631 | 0.483 | 0.963 | 0.986 | 0.004 | True |
| Cacao | Soft e bestiame | 0.050 | Chronos-2 | 708 | 0.051 | 0.918 | 0.699 | 0.947 | 0.986 | 0.004 | True |
| Cacao | Soft e bestiame | 0.010 | Chronos-2 | 708 | 0.017 | 0.091 | 0.195 | 0.837 | 0.986 | 0.004 | True |
| Bestiame | Soft e bestiame | 0.100 | Simulazione storica | 707 | 0.106 | 0.593 | 0.616 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 0.050 | Simulazione storica | 707 | 0.054 | 0.651 | 0.390 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 0.010 | Simulazione storica | 707 | 0.014 | 0.297 | 0.503 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 0.100 | GARCH-t | 707 | 0.098 | 0.831 | 0.214 | 0.998 | 0.999 | 0.725 | True |
| Bestiame | Soft e bestiame | 0.050 | GARCH-t | 707 | 0.054 | 0.651 | 0.629 | 1.004 | 0.999 | 0.725 | False |
| Bestiame | Soft e bestiame | 0.010 | GARCH-t | 707 | 0.017 | 0.090 | 0.193 | 1.052 | 0.999 | 0.725 | True |
| Bestiame | Soft e bestiame | 0.100 | GJR-GARCH-t | 707 | 0.098 | 0.831 | 0.387 | 1.007 | 1.001 | 0.860 | True |
| Bestiame | Soft e bestiame | 0.050 | GJR-GARCH-t | 707 | 0.054 | 0.651 | 0.724 | 1.015 | 1.001 | 0.860 | False |
| Bestiame | Soft e bestiame | 0.010 | GJR-GARCH-t | 707 | 0.016 | 0.170 | 0.327 | 1.068 | 1.001 | 0.860 | True |
| Bestiame | Soft e bestiame | 0.100 | EGARCH-t | 707 | 0.096 | 0.734 | 0.564 | 0.995 | 0.996 | 0.276 | True |
| Bestiame | Soft e bestiame | 0.050 | EGARCH-t | 707 | 0.059 | 0.264 | 0.173 | 1.002 | 0.996 | 0.276 | False |
| Bestiame | Soft e bestiame | 0.010 | EGARCH-t | 707 | 0.018 | 0.045 | 0.105 | 1.060 | 0.996 | 0.276 | True |
| Bestiame | Soft e bestiame | 0.100 | Timestral-28M | 707 | 0.103 | 0.774 | 0.580 | 0.987 | 0.996 | 0.137 | True |
| Bestiame | Soft e bestiame | 0.050 | Timestral-28M | 707 | 0.052 | 0.777 | 0.960 | 0.971 | 0.996 | 0.137 | True |
| Bestiame | Soft e bestiame | 0.010 | Timestral-28M | 707 | 0.017 | 0.090 | 0.193 | 1.044 | 0.996 | 0.137 | True |
| Bestiame | Soft e bestiame | 0.100 | Timestral-209M | 707 | 0.102 | 0.871 | 0.544 | 0.989 | 0.996 | 0.288 | True |
| Bestiame | Soft e bestiame | 0.050 | Timestral-209M | 707 | 0.054 | 0.651 | 0.902 | 0.971 | 0.996 | 0.288 | True |
| Bestiame | Soft e bestiame | 0.010 | Timestral-209M | 707 | 0.017 | 0.090 | 0.193 | 1.056 | 0.996 | 0.288 | True |
| Bestiame | Soft e bestiame | 0.100 | TimesFM-3 | 707 | 0.096 | 0.734 | 0.351 | 0.991 | 0.998 | 0.645 | True |
| Bestiame | Soft e bestiame | 0.100 | Chronos-2 | 707 | 0.099 | 0.930 | 0.275 | 0.989 | 1.001 | 0.893 | True |
| Bestiame | Soft e bestiame | 0.050 | Chronos-2 | 707 | 0.052 | 0.777 | 0.960 | 0.965 | 1.001 | 0.893 | True |
| Bestiame | Soft e bestiame | 0.010 | Chronos-2 | 707 | 0.016 | 0.170 | 0.327 | 0.984 | 1.001 | 0.893 | True |

### Volatilita'

| asset | settore | h | modello | n | QLIKE/HAR | MSE/HAR | DM p (QLIKE) | in MCS |
|---|---|---|---|---|---|---|---|---|
| WTI | Energia | 1 | Media 22g | 708 | 1.417 | 1.219 | 0.056 | True |
| WTI | Energia | 1 | Random walk | 708 | 1.658 | 1.291 | 0.000 | False |
| WTI | Energia | 1 | Timestral-28M | 708 | 1.048 | 0.918 | 0.266 | True |
| WTI | Energia | 1 | Timestral-209M | 708 | 1.024 | 0.941 | 0.482 | True |
| WTI | Energia | 1 | TimesFM-3 | 708 | 0.997 | 0.905 | 0.942 | True |
| WTI | Energia | 1 | Chronos-2 | 708 | 1.032 | 0.922 | 0.450 | False |
| WTI | Energia | 1 | HAR | 708 | 1.000 | 1.000 |  | True |
| WTI | Energia | 5 | Media 22g | 704 | 1.459 | 1.181 | 0.069 | True |
| WTI | Energia | 5 | Random walk | 704 | 1.731 | 1.536 | 0.000 | False |
| WTI | Energia | 5 | Timestral-28M | 704 | 1.155 | 0.923 | 0.225 | True |
| WTI | Energia | 5 | Timestral-209M | 704 | 1.110 | 0.965 | 0.287 | True |
| WTI | Energia | 5 | TimesFM-3 | 704 | 1.127 | 0.939 | 0.284 | True |
| WTI | Energia | 5 | Chronos-2 | 704 | 1.155 | 0.957 | 0.193 | True |
| WTI | Energia | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| WTI | Energia | 20 | Media 22g | 689 | 1.207 | 1.228 | 0.110 | True |
| WTI | Energia | 20 | Random walk | 689 | 2.417 | 1.954 | 0.013 | False |
| WTI | Energia | 20 | Timestral-28M | 689 | 1.278 | 0.998 | 0.265 | True |
| WTI | Energia | 20 | Timestral-209M | 689 | 1.269 | 1.010 | 0.261 | True |
| WTI | Energia | 20 | TimesFM-3 | 689 | 1.282 | 1.001 | 0.274 | True |
| WTI | Energia | 20 | Chronos-2 | 689 | 1.259 | 1.003 | 0.246 | True |
| WTI | Energia | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Brent | Energia | 1 | Media 22g | 693 | 1.356 | 1.238 | 0.069 | True |
| Brent | Energia | 1 | Random walk | 693 | 1.929 | 1.315 | 0.000 | False |
| Brent | Energia | 1 | Timestral-28M | 693 | 1.067 | 0.953 | 0.308 | True |
| Brent | Energia | 1 | Timestral-209M | 693 | 1.043 | 0.967 | 0.446 | True |
| Brent | Energia | 1 | TimesFM-3 | 693 | 1.016 | 0.947 | 0.679 | True |
| Brent | Energia | 1 | Chronos-2 | 693 | 1.048 | 0.949 | 0.272 | True |
| Brent | Energia | 1 | HAR | 693 | 1.000 | 1.000 |  | True |
| Brent | Energia | 5 | Media 22g | 689 | 1.325 | 1.218 | 0.032 | True |
| Brent | Energia | 5 | Random walk | 689 | 2.010 | 1.647 | 0.000 | False |
| Brent | Energia | 5 | Timestral-28M | 689 | 1.176 | 0.986 | 0.178 | True |
| Brent | Energia | 5 | Timestral-209M | 689 | 1.144 | 1.007 | 0.233 | True |
| Brent | Energia | 5 | TimesFM-3 | 689 | 1.137 | 1.005 | 0.223 | True |
| Brent | Energia | 5 | Chronos-2 | 689 | 1.166 | 1.010 | 0.148 | True |
| Brent | Energia | 5 | HAR | 689 | 1.000 | 1.000 |  | True |
| Brent | Energia | 20 | Media 22g | 674 | 1.153 | 1.263 | 0.072 | True |
| Brent | Energia | 20 | Random walk | 674 | 2.577 | 2.036 | 0.001 | False |
| Brent | Energia | 20 | Timestral-28M | 674 | 1.280 | 1.044 | 0.163 | True |
| Brent | Energia | 20 | Timestral-209M | 674 | 1.253 | 1.036 | 0.178 | True |
| Brent | Energia | 20 | TimesFM-3 | 674 | 1.265 | 1.052 | 0.175 | True |
| Brent | Energia | 20 | Chronos-2 | 674 | 1.240 | 1.046 | 0.155 | True |
| Brent | Energia | 20 | HAR | 674 | 1.000 | 1.000 |  | True |
| Gasolio | Energia | 1 | Media 22g | 708 | 1.345 | 1.273 | 0.001 | False |
| Gasolio | Energia | 1 | Random walk | 708 | 1.652 | 1.354 | 0.000 | False |
| Gasolio | Energia | 1 | Timestral-28M | 708 | 1.048 | 0.967 | 0.105 | True |
| Gasolio | Energia | 1 | Timestral-209M | 708 | 1.024 | 0.959 | 0.380 | True |
| Gasolio | Energia | 1 | TimesFM-3 | 708 | 1.022 | 1.001 | 0.420 | True |
| Gasolio | Energia | 1 | Chronos-2 | 708 | 1.046 | 0.961 | 0.218 | True |
| Gasolio | Energia | 1 | HAR | 708 | 1.000 | 1.000 |  | True |
| Gasolio | Energia | 5 | Media 22g | 704 | 1.382 | 1.264 | 0.008 | False |
| Gasolio | Energia | 5 | Random walk | 704 | 1.904 | 1.595 | 0.000 | False |
| Gasolio | Energia | 5 | Timestral-28M | 704 | 1.139 | 1.004 | 0.109 | True |
| Gasolio | Energia | 5 | Timestral-209M | 704 | 1.095 | 0.990 | 0.232 | True |
| Gasolio | Energia | 5 | TimesFM-3 | 704 | 1.108 | 1.029 | 0.174 | True |
| Gasolio | Energia | 5 | Chronos-2 | 704 | 1.163 | 1.011 | 0.112 | True |
| Gasolio | Energia | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Gasolio | Energia | 20 | Media 22g | 689 | 1.085 | 1.212 | 0.410 | True |
| Gasolio | Energia | 20 | Random walk | 689 | 2.264 | 1.914 | 0.000 | False |
| Gasolio | Energia | 20 | Timestral-28M | 689 | 1.222 | 1.039 | 0.124 | True |
| Gasolio | Energia | 20 | Timestral-209M | 689 | 1.184 | 1.013 | 0.138 | True |
| Gasolio | Energia | 20 | TimesFM-3 | 689 | 1.232 | 1.046 | 0.146 | True |
| Gasolio | Energia | 20 | Chronos-2 | 689 | 1.199 | 1.030 | 0.079 | True |
| Gasolio | Energia | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 1 | Media 22g | 708 | 1.320 | 1.101 | 0.064 | False |
| Benzina | Energia | 1 | Random walk | 708 | 1.679 | 1.318 | 0.000 | False |
| Benzina | Energia | 1 | Timestral-28M | 708 | 1.060 | 0.908 | 0.325 | True |
| Benzina | Energia | 1 | Timestral-209M | 708 | 1.048 | 0.927 | 0.348 | True |
| Benzina | Energia | 1 | TimesFM-3 | 708 | 1.054 | 0.934 | 0.273 | True |
| Benzina | Energia | 1 | Chronos-2 | 708 | 1.039 | 0.919 | 0.315 | True |
| Benzina | Energia | 1 | HAR | 708 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 5 | Media 22g | 704 | 1.320 | 1.037 | 0.119 | True |
| Benzina | Energia | 5 | Random walk | 704 | 2.304 | 1.670 | 0.000 | False |
| Benzina | Energia | 5 | Timestral-28M | 704 | 1.196 | 0.897 | 0.195 | True |
| Benzina | Energia | 5 | Timestral-209M | 704 | 1.211 | 0.948 | 0.177 | True |
| Benzina | Energia | 5 | TimesFM-3 | 704 | 1.247 | 0.943 | 0.163 | True |
| Benzina | Energia | 5 | Chronos-2 | 704 | 1.244 | 0.939 | 0.152 | True |
| Benzina | Energia | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 20 | Media 22g | 689 | 1.207 | 1.080 | 0.294 | True |
| Benzina | Energia | 20 | Random walk | 689 | 3.184 | 2.090 | 0.003 | False |
| Benzina | Energia | 20 | Timestral-28M | 689 | 1.219 | 0.877 | 0.444 | True |
| Benzina | Energia | 20 | Timestral-209M | 689 | 1.234 | 0.901 | 0.431 | True |
| Benzina | Energia | 20 | TimesFM-3 | 689 | 1.261 | 0.900 | 0.404 | True |
| Benzina | Energia | 20 | Chronos-2 | 689 | 1.221 | 0.885 | 0.427 | True |
| Benzina | Energia | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Gas naturale | Energia | 1 | Media 22g | 708 | 1.145 | 1.317 | 0.000 | False |
| Gas naturale | Energia | 1 | Random walk | 708 | 1.648 | 1.196 | 0.000 | False |
| Gas naturale | Energia | 1 | Timestral-28M | 708 | 0.944 | 0.886 | 0.023 | True |
| Gas naturale | Energia | 1 | Timestral-209M | 708 | 0.947 | 0.890 | 0.023 | False |
| Gas naturale | Energia | 1 | TimesFM-3 | 708 | 0.926 | 0.887 | 0.002 | True |
| Gas naturale | Energia | 1 | Chronos-2 | 708 | 0.943 | 0.865 | 0.037 | True |
| Gas naturale | Energia | 1 | HAR | 708 | 1.000 | 1.000 |  | False |
| Gas naturale | Energia | 5 | Media 22g | 704 | 1.078 | 1.274 | 0.088 | True |
| Gas naturale | Energia | 5 | Random walk | 704 | 2.074 | 1.371 | 0.000 | False |
| Gas naturale | Energia | 5 | Timestral-28M | 704 | 0.848 | 0.775 | 0.071 | True |
| Gas naturale | Energia | 5 | Timestral-209M | 704 | 0.892 | 0.815 | 0.101 | True |
| Gas naturale | Energia | 5 | TimesFM-3 | 704 | 0.869 | 0.801 | 0.059 | True |
| Gas naturale | Energia | 5 | Chronos-2 | 704 | 0.877 | 0.797 | 0.141 | True |
| Gas naturale | Energia | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Gas naturale | Energia | 20 | Media 22g | 689 | 0.997 | 1.289 | 0.980 | True |
| Gas naturale | Energia | 20 | Random walk | 689 | 2.668 | 2.167 | 0.000 | False |
| Gas naturale | Energia | 20 | Timestral-28M | 689 | 0.715 | 0.730 | 0.119 | True |
| Gas naturale | Energia | 20 | Timestral-209M | 689 | 0.822 | 0.805 | 0.096 | True |
| Gas naturale | Energia | 20 | TimesFM-3 | 689 | 0.850 | 0.843 | 0.122 | True |
| Gas naturale | Energia | 20 | Chronos-2 | 689 | 0.865 | 0.859 | 0.176 | False |
| Gas naturale | Energia | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Oro | Metalli preziosi | 1 | Media 22g | 708 | 1.215 | 1.379 | 0.000 | False |
| Oro | Metalli preziosi | 1 | Random walk | 708 | 1.605 | 1.145 | 0.000 | False |
| Oro | Metalli preziosi | 1 | Timestral-28M | 708 | 1.007 | 0.958 | 0.807 | False |
| Oro | Metalli preziosi | 1 | Timestral-209M | 708 | 0.977 | 0.921 | 0.459 | True |
| Oro | Metalli preziosi | 1 | TimesFM-3 | 708 | 0.965 | 0.887 | 0.289 | True |
| Oro | Metalli preziosi | 1 | Chronos-2 | 708 | 1.009 | 0.939 | 0.779 | False |
| Oro | Metalli preziosi | 1 | HAR | 708 | 1.000 | 1.000 |  | True |
| Oro | Metalli preziosi | 5 | Media 22g | 704 | 1.101 | 1.249 | 0.055 | True |
| Oro | Metalli preziosi | 5 | Random walk | 704 | 1.995 | 1.442 | 0.000 | False |
| Oro | Metalli preziosi | 5 | Timestral-28M | 704 | 1.030 | 0.963 | 0.474 | True |
| Oro | Metalli preziosi | 5 | Timestral-209M | 704 | 0.990 | 0.948 | 0.846 | True |
| Oro | Metalli preziosi | 5 | TimesFM-3 | 704 | 1.003 | 0.932 | 0.966 | True |
| Oro | Metalli preziosi | 5 | Chronos-2 | 704 | 1.064 | 0.968 | 0.310 | False |
| Oro | Metalli preziosi | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Oro | Metalli preziosi | 20 | Media 22g | 689 | 1.033 | 1.231 | 0.783 | True |
| Oro | Metalli preziosi | 20 | Random walk | 689 | 2.316 | 2.087 | 0.000 | False |
| Oro | Metalli preziosi | 20 | Timestral-28M | 689 | 1.159 | 1.081 | 0.038 | True |
| Oro | Metalli preziosi | 20 | Timestral-209M | 689 | 1.126 | 1.089 | 0.078 | True |
| Oro | Metalli preziosi | 20 | TimesFM-3 | 689 | 1.134 | 1.095 | 0.169 | True |
| Oro | Metalli preziosi | 20 | Chronos-2 | 689 | 1.185 | 1.102 | 0.056 | False |
| Oro | Metalli preziosi | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Rame | Metalli industriali | 1 | Media 22g | 691 | 1.025 | 1.081 | 0.669 | True |
| Rame | Metalli industriali | 1 | Random walk | 691 | 20.640 | 1.206 | 0.000 | False |
| Rame | Metalli industriali | 1 | Timestral-28M | 691 | 1.138 | 0.711 | 0.394 | True |
| Rame | Metalli industriali | 1 | Timestral-209M | 691 | 1.114 | 0.699 | 0.457 | True |
| Rame | Metalli industriali | 1 | TimesFM-3 | 691 | 1.109 | 0.717 | 0.478 | True |
| Rame | Metalli industriali | 1 | Chronos-2 | 691 | 1.189 | 0.706 | 0.243 | False |
| Rame | Metalli industriali | 1 | HAR | 691 | 1.000 | 1.000 |  | True |
| Rame | Metalli industriali | 5 | Media 22g | 704 | 1.085 | 1.140 | 0.285 | True |
| Rame | Metalli industriali | 5 | Random walk | 704 | 45.463 | 1.495 | 0.000 | False |
| Rame | Metalli industriali | 5 | Timestral-28M | 704 | 1.201 | 0.678 | 0.417 | True |
| Rame | Metalli industriali | 5 | Timestral-209M | 704 | 1.226 | 0.675 | 0.436 | True |
| Rame | Metalli industriali | 5 | TimesFM-3 | 704 | 1.166 | 0.678 | 0.495 | True |
| Rame | Metalli industriali | 5 | Chronos-2 | 704 | 1.294 | 0.679 | 0.285 | False |
| Rame | Metalli industriali | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Rame | Metalli industriali | 20 | Media 22g | 689 | 1.361 | 1.305 | 0.019 | False |
| Rame | Metalli industriali | 20 | Random walk | 689 | 96.077 | 2.171 | 0.000 | False |
| Rame | Metalli industriali | 20 | Timestral-28M | 689 | 1.504 | 0.739 | 0.162 | True |
| Rame | Metalli industriali | 20 | Timestral-209M | 689 | 1.597 | 0.752 | 0.178 | True |
| Rame | Metalli industriali | 20 | TimesFM-3 | 689 | 1.583 | 0.765 | 0.152 | True |
| Rame | Metalli industriali | 20 | Chronos-2 | 689 | 1.703 | 0.766 | 0.134 | False |
| Rame | Metalli industriali | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 1 | Media 22g | 680 | 1.053 | 1.050 | 0.012 | False |
| Grano | Cereali | 1 | Random walk | 680 | 15.982 | 1.219 | 0.091 | True |
| Grano | Cereali | 1 | Timestral-28M | 680 | 0.933 | 0.712 | 0.453 | True |
| Grano | Cereali | 1 | Timestral-209M | 680 | 0.941 | 0.707 | 0.523 | True |
| Grano | Cereali | 1 | TimesFM-3 | 680 | 0.900 | 0.725 | 0.135 | True |
| Grano | Cereali | 1 | Chronos-2 | 680 | 0.949 | 0.728 | 0.522 | True |
| Grano | Cereali | 1 | HAR | 680 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 5 | Media 22g | 703 | 1.045 | 1.007 | 0.346 | False |
| Grano | Cereali | 5 | Random walk | 703 | 58.475 | 1.853 | 0.031 | True |
| Grano | Cereali | 5 | Timestral-28M | 703 | 0.692 | 0.479 | 0.015 | True |
| Grano | Cereali | 5 | Timestral-209M | 703 | 0.669 | 0.460 | 0.012 | True |
| Grano | Cereali | 5 | TimesFM-3 | 703 | 0.669 | 0.500 | 0.002 | True |
| Grano | Cereali | 5 | Chronos-2 | 703 | 0.754 | 0.517 | 0.050 | True |
| Grano | Cereali | 5 | HAR | 703 | 1.000 | 1.000 |  | False |
| Grano | Cereali | 20 | Media 22g | 688 | 1.005 | 0.855 | 0.978 | False |
| Grano | Cereali | 20 | Random walk | 688 | 301.755 | 3.573 | 0.063 | True |
| Grano | Cereali | 20 | Timestral-28M | 688 | 0.554 | 0.437 | 0.038 | True |
| Grano | Cereali | 20 | Timestral-209M | 688 | 0.540 | 0.415 | 0.039 | True |
| Grano | Cereali | 20 | TimesFM-3 | 688 | 0.540 | 0.432 | 0.029 | True |
| Grano | Cereali | 20 | Chronos-2 | 688 | 0.576 | 0.437 | 0.060 | True |
| Grano | Cereali | 20 | HAR | 688 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 1 | Media 22g | 707 | 1.061 | 0.956 | 0.165 | True |
| Mais | Cereali | 1 | Random walk | 707 | 2.355 | 1.456 | 0.000 | False |
| Mais | Cereali | 1 | Timestral-28M | 707 | 1.029 | 0.880 | 0.632 | True |
| Mais | Cereali | 1 | Timestral-209M | 707 | 1.038 | 0.881 | 0.521 | True |
| Mais | Cereali | 1 | TimesFM-3 | 707 | 1.043 | 0.883 | 0.505 | True |
| Mais | Cereali | 1 | Chronos-2 | 707 | 1.039 | 0.879 | 0.512 | True |
| Mais | Cereali | 1 | HAR | 707 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 5 | Media 22g | 703 | 1.125 | 0.937 | 0.199 | True |
| Mais | Cereali | 5 | Random walk | 703 | 4.326 | 2.449 | 0.000 | False |
| Mais | Cereali | 5 | Timestral-28M | 703 | 1.022 | 0.845 | 0.825 | True |
| Mais | Cereali | 5 | Timestral-209M | 703 | 1.044 | 0.854 | 0.661 | True |
| Mais | Cereali | 5 | TimesFM-3 | 703 | 1.036 | 0.850 | 0.724 | True |
| Mais | Cereali | 5 | Chronos-2 | 703 | 1.071 | 0.856 | 0.518 | True |
| Mais | Cereali | 5 | HAR | 703 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 20 | Media 22g | 688 | 1.174 | 0.850 | 0.529 | True |
| Mais | Cereali | 20 | Random walk | 688 | 8.577 | 3.717 | 0.000 | False |
| Mais | Cereali | 20 | Timestral-28M | 688 | 0.852 | 0.667 | 0.442 | True |
| Mais | Cereali | 20 | Timestral-209M | 688 | 0.885 | 0.687 | 0.578 | True |
| Mais | Cereali | 20 | TimesFM-3 | 688 | 0.895 | 0.690 | 0.602 | True |
| Mais | Cereali | 20 | Chronos-2 | 688 | 0.953 | 0.697 | 0.834 | True |
| Mais | Cereali | 20 | HAR | 688 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 1 | Media 22g | 696 | 1.070 | 1.009 | 0.011 | True |
| Soia | Cereali | 1 | Random walk | 696 | 7.377 | 1.389 | 0.067 | True |
| Soia | Cereali | 1 | Timestral-28M | 696 | 1.035 | 0.893 | 0.281 | True |
| Soia | Cereali | 1 | Timestral-209M | 696 | 1.020 | 0.873 | 0.597 | True |
| Soia | Cereali | 1 | TimesFM-3 | 696 | 1.046 | 0.890 | 0.241 | True |
| Soia | Cereali | 1 | Chronos-2 | 696 | 1.060 | 0.893 | 0.164 | True |
| Soia | Cereali | 1 | HAR | 696 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 5 | Media 22g | 703 | 1.120 | 0.977 | 0.137 | True |
| Soia | Cereali | 5 | Random walk | 703 | 41.915 | 2.356 | 0.189 | True |
| Soia | Cereali | 5 | Timestral-28M | 703 | 1.029 | 0.857 | 0.690 | True |
| Soia | Cereali | 5 | Timestral-209M | 703 | 0.952 | 0.801 | 0.536 | True |
| Soia | Cereali | 5 | TimesFM-3 | 703 | 1.037 | 0.859 | 0.594 | True |
| Soia | Cereali | 5 | Chronos-2 | 703 | 1.041 | 0.840 | 0.636 | True |
| Soia | Cereali | 5 | HAR | 703 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 20 | Media 22g | 688 | 1.344 | 1.001 | 0.270 | True |
| Soia | Cereali | 20 | Random walk | 688 | 402.777 | 4.247 | 0.291 | True |
| Soia | Cereali | 20 | Timestral-28M | 688 | 0.892 | 0.671 | 0.528 | True |
| Soia | Cereali | 20 | Timestral-209M | 688 | 0.851 | 0.638 | 0.416 | True |
| Soia | Cereali | 20 | TimesFM-3 | 688 | 0.963 | 0.707 | 0.846 | True |
| Soia | Cereali | 20 | Chronos-2 | 688 | 0.870 | 0.652 | 0.458 | True |
| Soia | Cereali | 20 | HAR | 688 | 1.000 | 1.000 |  | True |
| Zucchero | Soft e bestiame | 1 | Media 22g | 707 | 1.086 | 1.071 | 0.002 | False |
| Zucchero | Soft e bestiame | 1 | Random walk | 707 | 2.010 | 1.590 | 0.000 | False |
| Zucchero | Soft e bestiame | 1 | Timestral-28M | 707 | 1.020 | 0.944 | 0.365 | True |
| Zucchero | Soft e bestiame | 1 | Timestral-209M | 707 | 1.014 | 0.943 | 0.493 | True |
| Zucchero | Soft e bestiame | 1 | TimesFM-3 | 707 | 1.013 | 0.949 | 0.505 | True |
| Zucchero | Soft e bestiame | 1 | Chronos-2 | 707 | 1.033 | 0.952 | 0.178 | True |
| Zucchero | Soft e bestiame | 1 | HAR | 707 | 1.000 | 1.000 |  | True |
| Zucchero | Soft e bestiame | 5 | Media 22g | 704 | 1.169 | 1.153 | 0.016 | False |
| Zucchero | Soft e bestiame | 5 | Random walk | 704 | 3.354 | 2.450 | 0.000 | False |
| Zucchero | Soft e bestiame | 5 | Timestral-28M | 704 | 1.039 | 0.928 | 0.552 | False |
| Zucchero | Soft e bestiame | 5 | Timestral-209M | 704 | 1.021 | 0.912 | 0.730 | True |
| Zucchero | Soft e bestiame | 5 | TimesFM-3 | 704 | 1.004 | 0.911 | 0.943 | True |
| Zucchero | Soft e bestiame | 5 | Chronos-2 | 704 | 1.061 | 0.941 | 0.387 | False |
| Zucchero | Soft e bestiame | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Zucchero | Soft e bestiame | 20 | Media 22g | 689 | 1.299 | 1.206 | 0.057 | True |
| Zucchero | Soft e bestiame | 20 | Random walk | 689 | 5.048 | 3.439 | 0.000 | False |
| Zucchero | Soft e bestiame | 20 | Timestral-28M | 689 | 1.098 | 0.899 | 0.596 | True |
| Zucchero | Soft e bestiame | 20 | Timestral-209M | 689 | 1.084 | 0.885 | 0.641 | True |
| Zucchero | Soft e bestiame | 20 | TimesFM-3 | 689 | 1.026 | 0.861 | 0.870 | True |
| Zucchero | Soft e bestiame | 20 | Chronos-2 | 689 | 1.125 | 0.911 | 0.519 | True |
| Zucchero | Soft e bestiame | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 1 | Media 22g | 707 | 1.049 | 1.024 | 0.062 | True |
| Bestiame | Soft e bestiame | 1 | Random walk | 707 | 2.641 | 1.378 | 0.001 | False |
| Bestiame | Soft e bestiame | 1 | Timestral-28M | 707 | 0.983 | 0.865 | 0.580 | True |
| Bestiame | Soft e bestiame | 1 | Timestral-209M | 707 | 0.978 | 0.866 | 0.553 | True |
| Bestiame | Soft e bestiame | 1 | TimesFM-3 | 707 | 0.972 | 0.868 | 0.375 | True |
| Bestiame | Soft e bestiame | 1 | Chronos-2 | 707 | 0.982 | 0.869 | 0.599 | True |
| Bestiame | Soft e bestiame | 1 | HAR | 707 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 5 | Media 22g | 703 | 1.180 | 1.121 | 0.017 | False |
| Bestiame | Soft e bestiame | 5 | Random walk | 703 | 5.165 | 2.273 | 0.000 | False |
| Bestiame | Soft e bestiame | 5 | Timestral-28M | 703 | 1.065 | 0.901 | 0.333 | True |
| Bestiame | Soft e bestiame | 5 | Timestral-209M | 703 | 1.042 | 0.889 | 0.572 | True |
| Bestiame | Soft e bestiame | 5 | TimesFM-3 | 703 | 1.023 | 0.877 | 0.737 | True |
| Bestiame | Soft e bestiame | 5 | Chronos-2 | 703 | 1.061 | 0.908 | 0.400 | True |
| Bestiame | Soft e bestiame | 5 | HAR | 703 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 20 | Media 22g | 688 | 1.501 | 1.354 | 0.002 | False |
| Bestiame | Soft e bestiame | 20 | Random walk | 688 | 9.344 | 3.858 | 0.000 | False |
| Bestiame | Soft e bestiame | 20 | Timestral-28M | 688 | 1.178 | 0.958 | 0.270 | True |
| Bestiame | Soft e bestiame | 20 | Timestral-209M | 688 | 1.189 | 0.964 | 0.269 | True |
| Bestiame | Soft e bestiame | 20 | TimesFM-3 | 688 | 1.090 | 0.874 | 0.587 | True |
| Bestiame | Soft e bestiame | 20 | Chronos-2 | 688 | 1.239 | 1.081 | 0.181 | True |
| Bestiame | Soft e bestiame | 20 | HAR | 688 | 1.000 | 1.000 |  | True |
