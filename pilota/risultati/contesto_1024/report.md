# Pilota: Timestral vs TimesFM-3 sulle commodities

15 commodities: WTI, Brent, Gasolio, Benzina, Gas naturale, Oro, Argento, Rame, Grano, Mais, Soia, Caffe, Zucchero, Cacao, Bestiame. Test dal 2024-01-01, una previsione ogni 1 giorni, contesto 1024 giorni. Valori < 1 = meglio del benchmark (media geometrica sugli asset). Tra parentesi: su quanti asset il modello batte il benchmark.

## Prezzo (benchmark: random walk)

| modello | CRPS/RW h=1 | CRPS/RW h=5 | CRPS/RW h=20 | MAE/RW h=1 | direzione h=1 | cop80 | cop80 RW | volte in MCS |
|---|---|---|---|---|---|---|---|---|
| Random walk | 1.000 | 1.000 | 1.000 | 1.000 |  | 0.750 |  | 25/45 |
| TimesFM-3 | 0.986 | 0.985 | 0.988 | 1.010 | 0.494 | 0.792 | 0.750 | 38/45 |
| Timestral-209M | 0.979 | 0.974 | 0.965 | 1.003 | 0.495 | 0.794 | 0.750 | 44/45 |
| Timestral-28M | 0.981 | 0.977 | 0.968 | 1.005 | 0.504 | 0.804 | 0.750 | 42/45 |

## Rendimento: VaR e distribuzione (benchmark: simulazione storica)

| modello | alpha | violazioni | kupiec_rifiuti | christoffersen_rifiuti | pinball_SS | volte in MCS |
|---|---|---|---|---|---|---|
| GARCH-t | 0.100 | 0.099 | 1/15 | 1/15 | 0.993 | 15/15 |
| Simulazione storica | 0.100 | 0.107 | 1/15 | 0/15 | 1.000 | 12/15 |
| TimesFM-3 | 0.100 | 0.095 | 0/15 | 0/15 | 0.996 | 15/15 |
| Timestral-209M | 0.100 | 0.097 | 1/15 | 1/15 | 0.993 | 14/15 |
| Timestral-28M | 0.100 | 0.090 | 3/15 | 2/15 | 0.994 | 14/15 |
| GARCH-t | 0.050 | 0.050 | 1/15 | 1/15 | 0.993 | 14/15 |
| Simulazione storica | 0.050 | 0.056 | 1/15 | 1/15 | 1.000 | 13/15 |
| Timestral-209M | 0.050 | 0.047 | 2/15 | 2/15 | 0.993 | 15/15 |
| Timestral-28M | 0.050 | 0.045 | 2/15 | 2/15 | 0.994 | 14/15 |
| GARCH-t | 0.010 | 0.011 | 1/15 | 2/15 | 0.993 | 14/15 |
| Simulazione storica | 0.010 | 0.016 | 4/15 | 4/15 | 1.000 | 10/15 |
| Timestral-209M | 0.010 | 0.011 | 2/15 | 2/15 | 0.993 | 14/15 |
| Timestral-28M | 0.010 | 0.011 | 1/15 | 1/15 | 0.994 | 15/15 |

## Volatilita' (benchmark: HAR-RV)

| modello | QLIKE/HAR h=1 | QLIKE/HAR h=5 | QLIKE/HAR h=20 | volte in MCS |
|---|---|---|---|---|
| HAR | 1.000 | 1.000 | 1.000 | 35/36 |
| Media 22g | 1.170 | 1.192 | 1.188 | 23/36 |
| Random walk | 3.076 | 5.336 | 10.229 | 6/36 |
| TimesFM-3 | 1.025 | 1.071 | 1.152 | 34/36 |
| Timestral-209M | 1.031 | 1.057 | 1.125 | 35/36 |
| Timestral-28M | 1.034 | 1.062 | 1.129 | 32/36 |

## Significativita' (Diebold-Mariano, Benjamini-Hochberg al 10% sugli asset)

| compito | h | modello | asset | meglio (BH) | peggio (BH) | p<0.05 senza correzione |
|---|---|---|---|---|---|---|
| prezzo | 1 | TimesFM-3 | 15 | 4 | 0 | 5 |
| prezzo | 1 | Timestral-209M | 15 | 10 | 0 | 10 |
| prezzo | 1 | Timestral-28M | 15 | 8 | 0 | 7 |
| prezzo | 5 | TimesFM-3 | 15 | 0 | 0 | 2 |
| prezzo | 5 | Timestral-209M | 15 | 8 | 0 | 8 |
| prezzo | 5 | Timestral-28M | 15 | 8 | 0 | 7 |
| prezzo | 20 | TimesFM-3 | 15 | 0 | 0 | 1 |
| prezzo | 20 | Timestral-209M | 15 | 0 | 0 | 3 |
| prezzo | 20 | Timestral-28M | 15 | 0 | 0 | 1 |
| rendimento | 1 | GARCH-t | 15 | 6 | 0 | 6 |
| rendimento | 1 | TimesFM-3 | 15 | 0 | 0 | 2 |
| rendimento | 1 | Timestral-209M | 15 | 3 | 0 | 4 |
| rendimento | 1 | Timestral-28M | 15 | 1 | 0 | 2 |
| volatilita | 1 | Media 22g | 12 | 0 | 10 | 6 |
| volatilita | 1 | Random walk | 12 | 0 | 12 | 10 |
| volatilita | 1 | TimesFM-3 | 12 | 1 | 0 | 1 |
| volatilita | 1 | Timestral-209M | 12 | 1 | 0 | 1 |
| volatilita | 1 | Timestral-28M | 12 | 1 | 0 | 1 |
| volatilita | 5 | Media 22g | 12 | 0 | 4 | 4 |
| volatilita | 5 | Random walk | 12 | 0 | 11 | 11 |
| volatilita | 5 | TimesFM-3 | 12 | 0 | 0 | 1 |
| volatilita | 5 | Timestral-209M | 12 | 0 | 0 | 1 |
| volatilita | 5 | Timestral-28M | 12 | 0 | 0 | 1 |
| volatilita | 20 | Media 22g | 12 | 0 | 1 | 2 |
| volatilita | 20 | Random walk | 12 | 0 | 11 | 10 |
| volatilita | 20 | TimesFM-3 | 12 | 0 | 0 | 1 |
| volatilita | 20 | Timestral-209M | 12 | 0 | 0 | 0 |
| volatilita | 20 | Timestral-28M | 12 | 0 | 0 | 0 |

## Per anno e regime di volatilita'

**Prezzo h=5: CRPS / random walk**

| modello | 2024 | 2025 | 2026 | vol alta | vol bassa |
|---|---|---|---|---|---|
| TimesFM-3 | 0.999 (8/15) | 0.999 (8/15) | 0.971 (11/15) | 0.979 (11/15) | 0.999 (10/15) |
| Timestral-209M | 0.988 (12/15) | 0.991 (12/15) | 0.959 (14/15) | 0.965 (14/15) | 0.994 (12/15) |
| Timestral-28M | 0.991 (12/15) | 0.994 (12/15) | 0.962 (14/15) | 0.969 (15/15) | 0.995 (12/15) |

**Rendimento: pinball / sim. storica**

| modello | 2024 | 2025 | 2026 | vol alta | vol bassa |
|---|---|---|---|---|---|
| GARCH-t | 0.996 (10/15) | 1.001 (8/15) | 0.986 (13/15) | 0.991 (11/15) | 0.997 (12/15) |
| TimesFM-3 | 0.999 (9/15) | 0.999 (9/15) | 0.993 (13/15) | 0.996 (10/15) | 0.998 (10/15) |
| Timestral-209M | 0.997 (9/15) | 0.998 (11/15) | 0.988 (12/15) | 0.990 (12/15) | 0.998 (12/15) |
| Timestral-28M | 0.996 (12/15) | 0.999 (8/15) | 0.990 (11/15) | 0.992 (13/15) | 0.998 (12/15) |

**Volatilita' h=5: QLIKE / HAR**

| modello | 2024 | 2025 | 2026 | vol alta | vol bassa |
|---|---|---|---|---|---|
| Media 22g | 1.043 (5/12) | 1.157 (2/12) | 1.306 (0/12) | 1.199 (2/12) | 1.154 (1/12) |
| TimesFM-3 | 0.924 (8/12) | 1.046 (4/12) | 1.183 (2/12) | 1.045 (6/12) | 1.081 (2/12) |
| Timestral-209M | 0.854 (10/12) | 1.037 (4/12) | 1.190 (3/12) | 1.018 (6/12) | 1.072 (2/12) |
| Timestral-28M | 0.874 (9/12) | 1.039 (4/12) | 1.209 (3/12) | 1.032 (6/12) | 1.079 (2/12) |

## Per settore

**Prezzo h=5: CRPS / random walk**

| modello | Cereali | Energia | Metalli industriali | Metalli preziosi | Soft e bestiame |
|---|---|---|---|---|---|
| TimesFM-3 | 0.980 (3/3) | 0.982 (5/5) | 1.008 (0/1) | 0.971 (2/2) | 0.992 (3/4) |
| Timestral-209M | 0.979 (3/3) | 0.964 (5/5) | 0.994 (1/1) | 0.965 (2/2) | 0.984 (4/4) |
| Timestral-28M | 0.982 (3/3) | 0.966 (5/5) | 1.000 (1/1) | 0.971 (2/2) | 0.985 (4/4) |

**Rendimento: pinball / sim. storica**

| modello | Cereali | Energia | Metalli industriali | Metalli preziosi | Soft e bestiame |
|---|---|---|---|---|---|
| GARCH-t | 0.997 (3/3) | 0.988 (4/5) | 1.008 (0/1) | 0.986 (2/2) | 0.996 (4/4) |
| TimesFM-3 | 0.998 (1/3) | 0.995 (4/5) | 1.000 (1/1) | 0.991 (1/2) | 0.998 (4/4) |
| Timestral-209M | 0.998 (2/3) | 0.990 (5/5) | 0.997 (1/1) | 0.986 (2/2) | 0.997 (3/4) |
| Timestral-28M | 0.998 (2/3) | 0.991 (5/5) | 0.997 (1/1) | 0.986 (2/2) | 0.999 (3/4) |

**Volatilita' h=5: QLIKE / HAR**

| modello | Cereali | Energia | Metalli industriali | Metalli preziosi | Soft e bestiame |
|---|---|---|---|---|---|
| Media 22g | 1.096 (0/3) | 1.306 (0/5) | 1.085 (0/1) | 1.101 (0/1) | 1.175 (0/2) |
| TimesFM-3 | 1.000 (1/3) | 1.092 (1/5) | 1.305 (0/1) | 1.022 (0/1) | 1.050 (0/2) |
| Timestral-209M | 0.947 (2/3) | 1.104 (1/5) | 1.267 (0/1) | 1.014 (0/1) | 1.042 (0/2) |
| Timestral-28M | 0.969 (1/3) | 1.121 (1/5) | 1.200 (0/1) | 1.012 (0/1) | 1.028 (0/2) |

## Dettaglio per asset

### Prezzo

| asset | settore | h | modello | n | MAE/RW | CRPS/RW | DM p (CRPS) | DM stat | direzione | cop80 | cop80 RW | in MCS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WTI | Energia | 1 | Timestral-28M | 708 | 0.999 | 0.970 | 0.001 | -3.278 | 0.533 | 0.805 | 0.771 | True |
| WTI | Energia | 1 | Timestral-209M | 708 | 1.002 | 0.971 | 0.001 | -3.352 | 0.511 | 0.805 | 0.771 | True |
| WTI | Energia | 1 | TimesFM-3 | 708 | 1.007 | 0.978 | 0.051 | -1.952 | 0.498 | 0.818 | 0.771 | True |
| WTI | Energia | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.771 |  | False |
| WTI | Energia | 5 | Timestral-28M | 704 | 0.996 | 0.950 | 0.000 | -3.579 | 0.499 | 0.812 | 0.754 | True |
| WTI | Energia | 5 | Timestral-209M | 704 | 0.998 | 0.951 | 0.000 | -3.811 | 0.520 | 0.797 | 0.754 | True |
| WTI | Energia | 5 | TimesFM-3 | 704 | 1.007 | 0.961 | 0.029 | -2.187 | 0.480 | 0.815 | 0.754 | True |
| WTI | Energia | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.754 |  | False |
| WTI | Energia | 20 | Timestral-28M | 689 | 1.015 | 0.971 | 0.451 | -0.755 | 0.389 | 0.871 | 0.791 | True |
| WTI | Energia | 20 | Timestral-209M | 689 | 1.013 | 0.969 | 0.372 | -0.893 | 0.427 | 0.851 | 0.791 | True |
| WTI | Energia | 20 | TimesFM-3 | 689 | 1.053 | 1.000 | 0.996 | 0.005 | 0.424 | 0.833 | 0.791 | True |
| WTI | Energia | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.791 |  | True |
| Brent | Energia | 1 | Timestral-28M | 708 | 1.003 | 0.965 | 0.000 | -3.501 | 0.532 | 0.822 | 0.764 | True |
| Brent | Energia | 1 | Timestral-209M | 708 | 1.006 | 0.968 | 0.001 | -3.459 | 0.502 | 0.815 | 0.764 | True |
| Brent | Energia | 1 | TimesFM-3 | 708 | 1.012 | 0.972 | 0.021 | -2.311 | 0.502 | 0.818 | 0.764 | True |
| Brent | Energia | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.764 |  | False |
| Brent | Energia | 5 | Timestral-28M | 704 | 1.001 | 0.963 | 0.007 | -2.707 | 0.498 | 0.824 | 0.756 | True |
| Brent | Energia | 5 | Timestral-209M | 704 | 1.001 | 0.961 | 0.002 | -3.058 | 0.525 | 0.804 | 0.756 | True |
| Brent | Energia | 5 | TimesFM-3 | 704 | 1.026 | 0.982 | 0.276 | -1.091 | 0.498 | 0.830 | 0.756 | False |
| Brent | Energia | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.756 |  | False |
| Brent | Energia | 20 | Timestral-28M | 689 | 1.015 | 0.975 | 0.567 | -0.572 | 0.440 | 0.856 | 0.752 | True |
| Brent | Energia | 20 | Timestral-209M | 689 | 1.013 | 0.973 | 0.489 | -0.692 | 0.451 | 0.829 | 0.752 | True |
| Brent | Energia | 20 | TimesFM-3 | 689 | 1.082 | 1.020 | 0.687 | 0.403 | 0.412 | 0.814 | 0.752 | True |
| Brent | Energia | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.752 |  | True |
| Gasolio | Energia | 1 | Timestral-28M | 708 | 1.008 | 0.965 | 0.001 | -3.363 | 0.494 | 0.806 | 0.753 | True |
| Gasolio | Energia | 1 | Timestral-209M | 708 | 1.009 | 0.964 | 0.000 | -3.645 | 0.451 | 0.805 | 0.753 | True |
| Gasolio | Energia | 1 | TimesFM-3 | 708 | 1.010 | 0.968 | 0.003 | -3.010 | 0.475 | 0.802 | 0.753 | True |
| Gasolio | Energia | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.753 |  | False |
| Gasolio | Energia | 5 | Timestral-28M | 704 | 1.014 | 0.984 | 0.323 | -0.988 | 0.472 | 0.821 | 0.749 | True |
| Gasolio | Energia | 5 | Timestral-209M | 704 | 1.012 | 0.983 | 0.217 | -1.235 | 0.456 | 0.807 | 0.749 | True |
| Gasolio | Energia | 5 | TimesFM-3 | 704 | 1.034 | 1.000 | 0.985 | -0.019 | 0.447 | 0.795 | 0.749 | False |
| Gasolio | Energia | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.749 |  | True |
| Gasolio | Energia | 20 | Timestral-28M | 689 | 1.007 | 0.983 | 0.519 | -0.645 | 0.514 | 0.829 | 0.729 | True |
| Gasolio | Energia | 20 | Timestral-209M | 689 | 1.013 | 0.984 | 0.547 | -0.602 | 0.533 | 0.807 | 0.729 | True |
| Gasolio | Energia | 20 | TimesFM-3 | 689 | 1.027 | 0.999 | 0.979 | -0.026 | 0.508 | 0.800 | 0.729 | True |
| Gasolio | Energia | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.729 |  | True |
| Benzina | Energia | 1 | Timestral-28M | 708 | 1.002 | 0.973 | 0.001 | -3.393 | 0.485 | 0.836 | 0.767 | True |
| Benzina | Energia | 1 | Timestral-209M | 708 | 1.001 | 0.973 | 0.000 | -4.176 | 0.491 | 0.821 | 0.767 | True |
| Benzina | Energia | 1 | TimesFM-3 | 708 | 1.014 | 0.985 | 0.106 | -1.620 | 0.487 | 0.818 | 0.767 | False |
| Benzina | Energia | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.767 |  | False |
| Benzina | Energia | 5 | Timestral-28M | 704 | 1.004 | 0.966 | 0.003 | -2.960 | 0.474 | 0.839 | 0.774 | True |
| Benzina | Energia | 5 | Timestral-209M | 704 | 1.000 | 0.963 | 0.000 | -3.615 | 0.484 | 0.810 | 0.774 | True |
| Benzina | Energia | 5 | TimesFM-3 | 704 | 1.014 | 0.982 | 0.305 | -1.026 | 0.526 | 0.830 | 0.774 | True |
| Benzina | Energia | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.774 |  | False |
| Benzina | Energia | 20 | Timestral-28M | 689 | 1.009 | 0.957 | 0.076 | -1.775 | 0.511 | 0.859 | 0.727 | True |
| Benzina | Energia | 20 | Timestral-209M | 689 | 1.001 | 0.947 | 0.025 | -2.240 | 0.456 | 0.851 | 0.727 | True |
| Benzina | Energia | 20 | TimesFM-3 | 689 | 1.104 | 1.038 | 0.514 | 0.654 | 0.486 | 0.821 | 0.727 | True |
| Benzina | Energia | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.727 |  | True |
| Gas naturale | Energia | 1 | Timestral-28M | 708 | 1.006 | 0.981 | 0.022 | -2.296 | 0.514 | 0.809 | 0.798 | True |
| Gas naturale | Energia | 1 | Timestral-209M | 708 | 1.004 | 0.976 | 0.000 | -3.615 | 0.466 | 0.828 | 0.798 | True |
| Gas naturale | Energia | 1 | TimesFM-3 | 708 | 1.011 | 0.985 | 0.041 | -2.049 | 0.456 | 0.806 | 0.798 | False |
| Gas naturale | Energia | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.798 |  | False |
| Gas naturale | Energia | 5 | Timestral-28M | 704 | 1.012 | 0.969 | 0.052 | -1.944 | 0.467 | 0.794 | 0.777 | True |
| Gas naturale | Energia | 5 | Timestral-209M | 704 | 1.003 | 0.964 | 0.008 | -2.681 | 0.453 | 0.808 | 0.777 | True |
| Gas naturale | Energia | 5 | TimesFM-3 | 704 | 1.028 | 0.985 | 0.261 | -1.125 | 0.450 | 0.800 | 0.777 | False |
| Gas naturale | Energia | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.777 |  | False |
| Gas naturale | Energia | 20 | Timestral-28M | 689 | 1.011 | 0.946 | 0.068 | -1.825 | 0.544 | 0.846 | 0.772 | True |
| Gas naturale | Energia | 20 | Timestral-209M | 689 | 1.003 | 0.939 | 0.022 | -2.290 | 0.488 | 0.837 | 0.772 | True |
| Gas naturale | Energia | 20 | TimesFM-3 | 689 | 1.022 | 0.962 | 0.092 | -1.686 | 0.506 | 0.842 | 0.772 | True |
| Gas naturale | Energia | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.772 |  | False |
| Oro | Metalli preziosi | 1 | Timestral-28M | 708 | 1.007 | 0.990 | 0.267 | -1.111 | 0.497 | 0.797 | 0.686 | True |
| Oro | Metalli preziosi | 1 | Timestral-209M | 708 | 1.016 | 0.999 | 0.904 | -0.120 | 0.448 | 0.744 | 0.686 | True |
| Oro | Metalli preziosi | 1 | TimesFM-3 | 708 | 1.019 | 1.001 | 0.954 | 0.058 | 0.484 | 0.799 | 0.686 | True |
| Oro | Metalli preziosi | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.686 |  | True |
| Oro | Metalli preziosi | 5 | Timestral-28M | 704 | 1.009 | 0.999 | 0.956 | -0.055 | 0.446 | 0.751 | 0.670 | True |
| Oro | Metalli preziosi | 5 | Timestral-209M | 704 | 1.003 | 0.995 | 0.800 | -0.254 | 0.452 | 0.766 | 0.670 | True |
| Oro | Metalli preziosi | 5 | TimesFM-3 | 704 | 1.005 | 0.995 | 0.747 | -0.323 | 0.483 | 0.801 | 0.670 | True |
| Oro | Metalli preziosi | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.670 |  | True |
| Oro | Metalli preziosi | 20 | Timestral-28M | 689 | 1.020 | 1.039 | 0.455 | 0.747 | 0.470 | 0.673 | 0.615 | True |
| Oro | Metalli preziosi | 20 | Timestral-209M | 689 | 1.007 | 1.022 | 0.711 | 0.371 | 0.566 | 0.695 | 0.615 | True |
| Oro | Metalli preziosi | 20 | TimesFM-3 | 689 | 1.038 | 1.050 | 0.299 | 1.040 | 0.409 | 0.737 | 0.615 | True |
| Oro | Metalli preziosi | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.615 |  | True |
| Argento | Metalli preziosi | 1 | Timestral-28M | 708 | 1.016 | 0.940 | 0.000 | -3.864 | 0.479 | 0.795 | 0.720 | True |
| Argento | Metalli preziosi | 1 | Timestral-209M | 708 | 1.007 | 0.936 | 0.000 | -4.411 | 0.494 | 0.787 | 0.720 | True |
| Argento | Metalli preziosi | 1 | TimesFM-3 | 708 | 1.019 | 0.936 | 0.000 | -3.550 | 0.484 | 0.815 | 0.720 | True |
| Argento | Metalli preziosi | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.720 |  | False |
| Argento | Metalli preziosi | 5 | Timestral-28M | 704 | 1.026 | 0.943 | 0.033 | -2.134 | 0.430 | 0.774 | 0.709 | True |
| Argento | Metalli preziosi | 5 | Timestral-209M | 704 | 1.013 | 0.936 | 0.015 | -2.438 | 0.480 | 0.770 | 0.709 | True |
| Argento | Metalli preziosi | 5 | TimesFM-3 | 704 | 1.031 | 0.948 | 0.077 | -1.773 | 0.456 | 0.812 | 0.709 | True |
| Argento | Metalli preziosi | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.709 |  | False |
| Argento | Metalli preziosi | 20 | Timestral-28M | 689 | 1.015 | 0.953 | 0.332 | -0.971 | 0.447 | 0.742 | 0.647 | False |
| Argento | Metalli preziosi | 20 | Timestral-209M | 689 | 1.007 | 0.941 | 0.242 | -1.171 | 0.499 | 0.736 | 0.647 | True |
| Argento | Metalli preziosi | 20 | TimesFM-3 | 689 | 1.018 | 0.951 | 0.368 | -0.900 | 0.456 | 0.763 | 0.647 | True |
| Argento | Metalli preziosi | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.647 |  | True |
| Rame | Metalli industriali | 1 | Timestral-28M | 708 | 1.004 | 0.991 | 0.233 | -1.194 | 0.492 | 0.835 | 0.749 | True |
| Rame | Metalli industriali | 1 | Timestral-209M | 708 | 0.996 | 0.985 | 0.003 | -2.951 | 0.514 | 0.812 | 0.749 | True |
| Rame | Metalli industriali | 1 | TimesFM-3 | 708 | 1.011 | 0.995 | 0.589 | -0.541 | 0.490 | 0.806 | 0.749 | True |
| Rame | Metalli industriali | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.749 |  | False |
| Rame | Metalli industriali | 5 | Timestral-28M | 704 | 0.996 | 1.000 | 0.989 | -0.014 | 0.517 | 0.781 | 0.717 | True |
| Rame | Metalli industriali | 5 | Timestral-209M | 704 | 0.992 | 0.994 | 0.585 | -0.547 | 0.534 | 0.783 | 0.717 | True |
| Rame | Metalli industriali | 5 | TimesFM-3 | 704 | 1.007 | 1.008 | 0.694 | 0.394 | 0.499 | 0.811 | 0.717 | True |
| Rame | Metalli industriali | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.717 |  | True |
| Rame | Metalli industriali | 20 | Timestral-28M | 689 | 0.990 | 0.987 | 0.757 | -0.310 | 0.477 | 0.771 | 0.723 | True |
| Rame | Metalli industriali | 20 | Timestral-209M | 689 | 0.998 | 0.997 | 0.925 | -0.094 | 0.515 | 0.775 | 0.723 | True |
| Rame | Metalli industriali | 20 | TimesFM-3 | 689 | 1.018 | 1.009 | 0.888 | 0.141 | 0.433 | 0.749 | 0.723 | True |
| Rame | Metalli industriali | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.723 |  | True |
| Grano | Cereali | 1 | Timestral-28M | 707 | 1.000 | 0.990 | 0.101 | -1.644 | 0.533 | 0.833 | 0.805 | False |
| Grano | Cereali | 1 | Timestral-209M | 707 | 0.993 | 0.979 | 0.000 | -3.545 | 0.541 | 0.840 | 0.805 | True |
| Grano | Cereali | 1 | TimesFM-3 | 707 | 1.000 | 0.988 | 0.118 | -1.564 | 0.523 | 0.842 | 0.805 | False |
| Grano | Cereali | 1 | Random walk | 707 | 1.000 | 1.000 |  |  |  | 0.805 |  | False |
| Grano | Cereali | 5 | Timestral-28M | 703 | 0.995 | 0.970 | 0.018 | -2.379 | 0.538 | 0.839 | 0.778 | True |
| Grano | Cereali | 5 | Timestral-209M | 703 | 0.995 | 0.966 | 0.004 | -2.878 | 0.549 | 0.844 | 0.778 | True |
| Grano | Cereali | 5 | TimesFM-3 | 703 | 0.988 | 0.959 | 0.016 | -2.412 | 0.557 | 0.834 | 0.778 | True |
| Grano | Cereali | 5 | Random walk | 703 | 1.000 | 1.000 |  |  |  | 0.778 |  | False |
| Grano | Cereali | 20 | Timestral-28M | 688 | 0.974 | 0.924 | 0.036 | -2.099 | 0.585 | 0.840 | 0.744 | False |
| Grano | Cereali | 20 | Timestral-209M | 688 | 0.981 | 0.925 | 0.022 | -2.301 | 0.585 | 0.828 | 0.744 | False |
| Grano | Cereali | 20 | TimesFM-3 | 688 | 0.946 | 0.898 | 0.025 | -2.250 | 0.569 | 0.818 | 0.744 | True |
| Grano | Cereali | 20 | Random walk | 688 | 1.000 | 1.000 |  |  |  | 0.744 |  | False |
| Mais | Cereali | 1 | Timestral-28M | 707 | 1.006 | 0.999 | 0.818 | -0.230 | 0.486 | 0.844 | 0.820 | True |
| Mais | Cereali | 1 | Timestral-209M | 707 | 1.003 | 0.995 | 0.225 | -1.214 | 0.474 | 0.843 | 0.820 | True |
| Mais | Cereali | 1 | TimesFM-3 | 707 | 1.007 | 1.006 | 0.311 | 1.014 | 0.486 | 0.812 | 0.820 | False |
| Mais | Cereali | 1 | Random walk | 707 | 1.000 | 1.000 |  |  |  | 0.820 |  | True |
| Mais | Cereali | 5 | Timestral-28M | 703 | 1.003 | 0.982 | 0.025 | -2.250 | 0.491 | 0.826 | 0.755 | True |
| Mais | Cereali | 5 | Timestral-209M | 703 | 1.002 | 0.979 | 0.010 | -2.593 | 0.463 | 0.825 | 0.755 | True |
| Mais | Cereali | 5 | TimesFM-3 | 703 | 1.016 | 0.988 | 0.193 | -1.304 | 0.476 | 0.809 | 0.755 | True |
| Mais | Cereali | 5 | Random walk | 703 | 1.000 | 1.000 |  |  |  | 0.755 |  | False |
| Mais | Cereali | 20 | Timestral-28M | 688 | 1.008 | 0.950 | 0.132 | -1.508 | 0.399 | 0.786 | 0.765 | True |
| Mais | Cereali | 20 | Timestral-209M | 688 | 1.008 | 0.948 | 0.137 | -1.487 | 0.378 | 0.779 | 0.765 | True |
| Mais | Cereali | 20 | TimesFM-3 | 688 | 1.013 | 0.962 | 0.214 | -1.244 | 0.454 | 0.765 | 0.765 | True |
| Mais | Cereali | 20 | Random walk | 688 | 1.000 | 1.000 |  |  |  | 0.765 |  | True |
| Soia | Cereali | 1 | Timestral-28M | 707 | 1.009 | 1.007 | 0.141 | 1.474 | 0.469 | 0.832 | 0.832 | True |
| Soia | Cereali | 1 | Timestral-209M | 707 | 1.003 | 1.003 | 0.560 | 0.583 | 0.494 | 0.833 | 0.832 | True |
| Soia | Cereali | 1 | TimesFM-3 | 707 | 1.008 | 1.008 | 0.182 | 1.336 | 0.498 | 0.825 | 0.832 | True |
| Soia | Cereali | 1 | Random walk | 707 | 1.000 | 1.000 |  |  |  | 0.832 |  | True |
| Soia | Cereali | 5 | Timestral-28M | 703 | 1.002 | 0.994 | 0.590 | -0.539 | 0.493 | 0.828 | 0.804 | True |
| Soia | Cereali | 5 | Timestral-209M | 703 | 1.003 | 0.993 | 0.548 | -0.601 | 0.490 | 0.825 | 0.804 | True |
| Soia | Cereali | 5 | TimesFM-3 | 703 | 1.002 | 0.994 | 0.557 | -0.588 | 0.529 | 0.828 | 0.804 | True |
| Soia | Cereali | 5 | Random walk | 703 | 1.000 | 1.000 |  |  |  | 0.804 |  | True |
| Soia | Cereali | 20 | Timestral-28M | 688 | 1.005 | 0.975 | 0.542 | -0.611 | 0.488 | 0.812 | 0.769 | True |
| Soia | Cereali | 20 | Timestral-209M | 688 | 1.005 | 0.974 | 0.540 | -0.613 | 0.472 | 0.785 | 0.769 | True |
| Soia | Cereali | 20 | TimesFM-3 | 688 | 1.035 | 1.004 | 0.921 | 0.100 | 0.483 | 0.772 | 0.769 | True |
| Soia | Cereali | 20 | Random walk | 688 | 1.000 | 1.000 |  |  |  | 0.769 |  | True |
| Caffe | Soft e bestiame | 1 | Timestral-28M | 708 | 1.001 | 0.989 | 0.053 | -1.937 | 0.510 | 0.787 | 0.749 | True |
| Caffe | Soft e bestiame | 1 | Timestral-209M | 708 | 1.000 | 0.989 | 0.029 | -2.185 | 0.513 | 0.785 | 0.749 | True |
| Caffe | Soft e bestiame | 1 | TimesFM-3 | 708 | 1.010 | 0.995 | 0.502 | -0.671 | 0.507 | 0.806 | 0.749 | True |
| Caffe | Soft e bestiame | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.749 |  | False |
| Caffe | Soft e bestiame | 5 | Timestral-28M | 704 | 1.000 | 0.987 | 0.262 | -1.122 | 0.493 | 0.744 | 0.717 | True |
| Caffe | Soft e bestiame | 5 | Timestral-209M | 704 | 1.002 | 0.988 | 0.222 | -1.224 | 0.487 | 0.757 | 0.717 | True |
| Caffe | Soft e bestiame | 5 | TimesFM-3 | 704 | 1.001 | 0.989 | 0.392 | -0.857 | 0.534 | 0.787 | 0.717 | True |
| Caffe | Soft e bestiame | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.717 |  | True |
| Caffe | Soft e bestiame | 20 | Timestral-28M | 689 | 1.006 | 0.979 | 0.571 | -0.566 | 0.480 | 0.730 | 0.663 | True |
| Caffe | Soft e bestiame | 20 | Timestral-209M | 689 | 1.005 | 0.977 | 0.497 | -0.680 | 0.473 | 0.727 | 0.663 | True |
| Caffe | Soft e bestiame | 20 | TimesFM-3 | 689 | 1.005 | 0.991 | 0.833 | -0.211 | 0.457 | 0.765 | 0.663 | True |
| Caffe | Soft e bestiame | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.663 |  | True |
| Zucchero | Soft e bestiame | 1 | Timestral-28M | 708 | 0.999 | 0.994 | 0.135 | -1.495 | 0.488 | 0.825 | 0.831 | True |
| Zucchero | Soft e bestiame | 1 | Timestral-209M | 708 | 1.002 | 0.995 | 0.266 | -1.113 | 0.505 | 0.798 | 0.831 | True |
| Zucchero | Soft e bestiame | 1 | TimesFM-3 | 708 | 1.012 | 1.002 | 0.701 | 0.383 | 0.486 | 0.787 | 0.831 | True |
| Zucchero | Soft e bestiame | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.831 |  | True |
| Zucchero | Soft e bestiame | 5 | Timestral-28M | 704 | 1.003 | 0.995 | 0.531 | -0.627 | 0.483 | 0.791 | 0.810 | True |
| Zucchero | Soft e bestiame | 5 | Timestral-209M | 704 | 1.005 | 0.996 | 0.693 | -0.395 | 0.451 | 0.776 | 0.810 | True |
| Zucchero | Soft e bestiame | 5 | TimesFM-3 | 704 | 1.021 | 1.011 | 0.453 | 0.750 | 0.507 | 0.747 | 0.810 | True |
| Zucchero | Soft e bestiame | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.810 |  | True |
| Zucchero | Soft e bestiame | 20 | Timestral-28M | 689 | 1.019 | 0.981 | 0.582 | -0.551 | 0.414 | 0.807 | 0.771 | True |
| Zucchero | Soft e bestiame | 20 | Timestral-209M | 689 | 1.014 | 0.978 | 0.491 | -0.690 | 0.428 | 0.766 | 0.771 | True |
| Zucchero | Soft e bestiame | 20 | TimesFM-3 | 689 | 1.075 | 1.040 | 0.543 | 0.609 | 0.534 | 0.729 | 0.771 | True |
| Zucchero | Soft e bestiame | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.771 |  | True |
| Cacao | Soft e bestiame | 1 | Timestral-28M | 708 | 1.007 | 0.964 | 0.000 | -3.965 | 0.495 | 0.819 | 0.749 | True |
| Cacao | Soft e bestiame | 1 | Timestral-209M | 708 | 1.011 | 0.963 | 0.000 | -4.329 | 0.468 | 0.773 | 0.749 | True |
| Cacao | Soft e bestiame | 1 | TimesFM-3 | 708 | 1.014 | 0.968 | 0.001 | -3.193 | 0.496 | 0.771 | 0.749 | True |
| Cacao | Soft e bestiame | 1 | Random walk | 708 | 1.000 | 1.000 |  |  |  | 0.749 |  | False |
| Cacao | Soft e bestiame | 5 | Timestral-28M | 704 | 1.010 | 0.964 | 0.014 | -2.466 | 0.467 | 0.776 | 0.751 | True |
| Cacao | Soft e bestiame | 5 | Timestral-209M | 704 | 1.008 | 0.960 | 0.009 | -2.636 | 0.477 | 0.756 | 0.751 | True |
| Cacao | Soft e bestiame | 5 | TimesFM-3 | 704 | 1.024 | 0.973 | 0.185 | -1.327 | 0.489 | 0.743 | 0.751 | True |
| Cacao | Soft e bestiame | 5 | Random walk | 704 | 1.000 | 1.000 |  |  |  | 0.751 |  | False |
| Cacao | Soft e bestiame | 20 | Timestral-28M | 689 | 1.032 | 0.945 | 0.118 | -1.565 | 0.421 | 0.739 | 0.694 | True |
| Cacao | Soft e bestiame | 20 | Timestral-209M | 689 | 1.026 | 0.941 | 0.113 | -1.588 | 0.446 | 0.707 | 0.694 | True |
| Cacao | Soft e bestiame | 20 | TimesFM-3 | 689 | 1.013 | 0.926 | 0.139 | -1.480 | 0.451 | 0.704 | 0.694 | True |
| Cacao | Soft e bestiame | 20 | Random walk | 689 | 1.000 | 1.000 |  |  |  | 0.694 |  | True |
| Bestiame | Soft e bestiame | 1 | Timestral-28M | 707 | 1.001 | 1.001 | 0.859 | 0.178 | 0.545 | 0.806 | 0.771 | True |
| Bestiame | Soft e bestiame | 1 | Timestral-209M | 707 | 0.995 | 0.998 | 0.657 | -0.445 | 0.557 | 0.762 | 0.771 | True |
| Bestiame | Soft e bestiame | 1 | TimesFM-3 | 707 | 0.995 | 1.001 | 0.835 | 0.208 | 0.541 | 0.755 | 0.771 | True |
| Bestiame | Soft e bestiame | 1 | Random walk | 707 | 1.000 | 1.000 |  |  |  | 0.771 |  | True |
| Bestiame | Soft e bestiame | 5 | Timestral-28M | 703 | 0.983 | 0.994 | 0.535 | -0.621 | 0.591 | 0.747 | 0.747 | True |
| Bestiame | Soft e bestiame | 5 | Timestral-209M | 703 | 0.978 | 0.991 | 0.306 | -1.024 | 0.591 | 0.748 | 0.747 | True |
| Bestiame | Soft e bestiame | 5 | TimesFM-3 | 703 | 0.974 | 0.996 | 0.829 | -0.216 | 0.623 | 0.740 | 0.747 | True |
| Bestiame | Soft e bestiame | 5 | Random walk | 703 | 1.000 | 1.000 |  |  |  | 0.747 |  | True |
| Bestiame | Soft e bestiame | 20 | Timestral-28M | 688 | 0.971 | 0.967 | 0.313 | -1.011 | 0.590 | 0.815 | 0.740 | True |
| Bestiame | Soft e bestiame | 20 | Timestral-209M | 688 | 0.971 | 0.964 | 0.185 | -1.327 | 0.589 | 0.828 | 0.740 | True |
| Bestiame | Soft e bestiame | 20 | TimesFM-3 | 688 | 0.968 | 0.982 | 0.769 | -0.294 | 0.606 | 0.673 | 0.740 | True |
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
| WTI | Energia | 0.100 | Timestral-28M | 708 | 0.088 | 0.261 | 0.414 | 0.952 | 0.989 | 0.061 | True |
| WTI | Energia | 0.050 | Timestral-28M | 708 | 0.042 | 0.339 | 0.612 | 0.896 | 0.989 | 0.061 | True |
| WTI | Energia | 0.010 | Timestral-28M | 708 | 0.008 | 0.675 | 0.103 | 0.725 | 0.989 | 0.061 | True |
| WTI | Energia | 0.100 | Timestral-209M | 708 | 0.095 | 0.631 | 0.697 | 0.954 | 0.990 | 0.061 | True |
| WTI | Energia | 0.050 | Timestral-209M | 708 | 0.044 | 0.439 | 0.700 | 0.899 | 0.990 | 0.061 | True |
| WTI | Energia | 0.010 | Timestral-209M | 708 | 0.010 | 0.976 | 0.154 | 0.706 | 0.990 | 0.061 | True |
| WTI | Energia | 0.100 | TimesFM-3 | 708 | 0.099 | 0.920 | 0.919 | 0.962 | 0.996 | 0.569 | True |
| Brent | Energia | 0.100 | Simulazione storica | 708 | 0.119 | 0.107 | 0.105 | 1.000 | 1.000 |  | False |
| Brent | Energia | 0.050 | Simulazione storica | 708 | 0.059 | 0.268 | 0.067 | 1.000 | 1.000 |  | False |
| Brent | Energia | 0.010 | Simulazione storica | 708 | 0.014 | 0.299 | 0.180 | 1.000 | 1.000 |  | False |
| Brent | Energia | 0.100 | GARCH-t | 708 | 0.105 | 0.690 | 0.630 | 0.923 | 0.977 | 0.000 | True |
| Brent | Energia | 0.050 | GARCH-t | 708 | 0.056 | 0.437 | 0.653 | 0.877 | 0.977 | 0.000 | True |
| Brent | Energia | 0.010 | GARCH-t | 708 | 0.016 | 0.171 | 0.144 | 0.719 | 0.977 | 0.000 | True |
| Brent | Energia | 0.100 | Timestral-28M | 708 | 0.085 | 0.166 | 0.330 | 0.932 | 0.986 | 0.043 | True |
| Brent | Energia | 0.050 | Timestral-28M | 708 | 0.041 | 0.255 | 0.406 | 0.890 | 0.986 | 0.043 | False |
| Brent | Energia | 0.010 | Timestral-28M | 708 | 0.011 | 0.734 | 0.190 | 0.723 | 0.986 | 0.043 | True |
| Brent | Energia | 0.100 | Timestral-209M | 708 | 0.095 | 0.631 | 0.740 | 0.929 | 0.983 | 0.011 | True |
| Brent | Energia | 0.050 | Timestral-209M | 708 | 0.042 | 0.339 | 0.521 | 0.875 | 0.983 | 0.011 | True |
| Brent | Energia | 0.010 | Timestral-209M | 708 | 0.011 | 0.734 | 0.190 | 0.699 | 0.983 | 0.011 | True |
| Brent | Energia | 0.100 | TimesFM-3 | 708 | 0.086 | 0.210 | 0.233 | 0.937 | 0.990 | 0.234 | True |
| Gasolio | Energia | 0.100 | Simulazione storica | 708 | 0.116 | 0.170 | 0.263 | 1.000 | 1.000 |  | True |
| Gasolio | Energia | 0.050 | Simulazione storica | 708 | 0.056 | 0.437 | 0.396 | 1.000 | 1.000 |  | True |
| Gasolio | Energia | 0.010 | Simulazione storica | 708 | 0.016 | 0.171 | 0.144 | 1.000 | 1.000 |  | False |
| Gasolio | Energia | 0.100 | GARCH-t | 708 | 0.103 | 0.784 | 0.783 | 0.950 | 0.980 | 0.000 | True |
| Gasolio | Energia | 0.050 | GARCH-t | 708 | 0.045 | 0.551 | 0.770 | 0.906 | 0.980 | 0.000 | True |
| Gasolio | Energia | 0.010 | GARCH-t | 708 | 0.008 | 0.675 | 0.870 | 0.720 | 0.980 | 0.000 | True |
| Gasolio | Energia | 0.100 | Timestral-28M | 708 | 0.079 | 0.055 | 0.153 | 0.969 | 0.989 | 0.073 | True |
| Gasolio | Energia | 0.050 | Timestral-28M | 708 | 0.037 | 0.090 | 0.236 | 0.931 | 0.989 | 0.073 | True |
| Gasolio | Energia | 0.010 | Timestral-28M | 708 | 0.007 | 0.407 | 0.684 | 0.721 | 0.989 | 0.073 | True |
| Gasolio | Energia | 0.100 | Timestral-209M | 708 | 0.092 | 0.462 | 0.763 | 0.967 | 0.987 | 0.014 | True |
| Gasolio | Energia | 0.050 | Timestral-209M | 708 | 0.042 | 0.339 | 0.612 | 0.928 | 0.987 | 0.014 | True |
| Gasolio | Energia | 0.010 | Timestral-209M | 708 | 0.008 | 0.675 | 0.870 | 0.709 | 0.987 | 0.014 | True |
| Gasolio | Energia | 0.100 | TimesFM-3 | 708 | 0.090 | 0.387 | 0.596 | 0.984 | 0.994 | 0.427 | True |
| Benzina | Energia | 0.100 | Simulazione storica | 708 | 0.102 | 0.881 | 0.953 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 0.050 | Simulazione storica | 708 | 0.052 | 0.784 | 0.962 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 0.010 | Simulazione storica | 708 | 0.017 | 0.091 | 0.195 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 0.100 | GARCH-t | 708 | 0.095 | 0.631 | 0.740 | 0.980 | 0.990 | 0.011 | True |
| Benzina | Energia | 0.050 | GARCH-t | 708 | 0.052 | 0.784 | 0.962 | 0.961 | 0.990 | 0.011 | True |
| Benzina | Energia | 0.010 | GARCH-t | 708 | 0.010 | 0.976 | 0.932 | 0.933 | 0.990 | 0.011 | True |
| Benzina | Energia | 0.100 | Timestral-28M | 708 | 0.083 | 0.129 | 0.283 | 0.986 | 0.994 | 0.324 | True |
| Benzina | Energia | 0.050 | Timestral-28M | 708 | 0.048 | 0.808 | 0.931 | 0.976 | 0.994 | 0.324 | True |
| Benzina | Energia | 0.010 | Timestral-28M | 708 | 0.010 | 0.976 | 0.932 | 0.932 | 0.994 | 0.324 | True |
| Benzina | Energia | 0.100 | Timestral-209M | 708 | 0.097 | 0.821 | 0.725 | 0.975 | 0.992 | 0.091 | True |
| Benzina | Energia | 0.050 | Timestral-209M | 708 | 0.047 | 0.676 | 0.855 | 0.957 | 0.992 | 0.091 | True |
| Benzina | Energia | 0.010 | Timestral-209M | 708 | 0.014 | 0.299 | 0.180 | 0.917 | 0.992 | 0.091 | True |
| Benzina | Energia | 0.100 | TimesFM-3 | 708 | 0.090 | 0.387 | 0.476 | 1.003 | 0.996 | 0.428 | True |
| Gas naturale | Energia | 0.100 | Simulazione storica | 708 | 0.097 | 0.821 | 0.963 | 1.000 | 1.000 |  | True |
| Gas naturale | Energia | 0.050 | Simulazione storica | 708 | 0.052 | 0.784 | 0.726 | 1.000 | 1.000 |  | True |
| Gas naturale | Energia | 0.010 | Simulazione storica | 708 | 0.013 | 0.486 | 0.699 | 1.000 | 1.000 |  | True |
| Gas naturale | Energia | 0.100 | GARCH-t | 708 | 0.105 | 0.690 | 0.732 | 0.995 | 1.010 | 0.148 | True |
| Gas naturale | Energia | 0.050 | GARCH-t | 708 | 0.037 | 0.090 | 0.140 | 0.967 | 1.010 | 0.148 | False |
| Gas naturale | Energia | 0.010 | GARCH-t | 708 | 0.010 | 0.976 | 0.932 | 0.760 | 1.010 | 0.148 | True |
| Gas naturale | Energia | 0.100 | Timestral-28M | 708 | 0.093 | 0.543 | 0.737 | 0.974 | 1.000 | 0.912 | True |
| Gas naturale | Energia | 0.050 | Timestral-28M | 708 | 0.038 | 0.131 | 0.207 | 0.945 | 1.000 | 0.912 | True |
| Gas naturale | Energia | 0.010 | Timestral-28M | 708 | 0.010 | 0.976 | 0.932 | 0.797 | 1.000 | 0.912 | True |
| Gas naturale | Energia | 0.100 | Timestral-209M | 708 | 0.093 | 0.543 | 0.517 | 0.960 | 0.997 | 0.435 | True |
| Gas naturale | Energia | 0.050 | Timestral-209M | 708 | 0.038 | 0.131 | 0.207 | 0.927 | 0.997 | 0.435 | True |
| Gas naturale | Energia | 0.010 | Timestral-209M | 708 | 0.010 | 0.976 | 0.932 | 0.761 | 0.997 | 0.435 | True |
| Gas naturale | Energia | 0.100 | TimesFM-3 | 708 | 0.096 | 0.724 | 0.496 | 0.962 | 1.000 | 0.938 | True |
| Oro | Metalli preziosi | 0.100 | Simulazione storica | 708 | 0.119 | 0.107 | 0.256 | 1.000 | 1.000 |  | True |
| Oro | Metalli preziosi | 0.050 | Simulazione storica | 708 | 0.066 | 0.056 | 0.124 | 1.000 | 1.000 |  | True |
| Oro | Metalli preziosi | 0.010 | Simulazione storica | 708 | 0.023 | 0.004 | 0.011 | 1.000 | 1.000 |  | False |
| Oro | Metalli preziosi | 0.100 | GARCH-t | 708 | 0.116 | 0.170 | 0.386 | 0.966 | 0.995 | 0.329 | True |
| Oro | Metalli preziosi | 0.050 | GARCH-t | 708 | 0.066 | 0.056 | 0.124 | 0.969 | 0.995 | 0.329 | True |
| Oro | Metalli preziosi | 0.010 | GARCH-t | 708 | 0.017 | 0.091 | 0.195 | 0.899 | 0.995 | 0.329 | True |
| Oro | Metalli preziosi | 0.100 | Timestral-28M | 708 | 0.117 | 0.136 | 0.192 | 0.979 | 0.994 | 0.080 | True |
| Oro | Metalli preziosi | 0.050 | Timestral-28M | 708 | 0.061 | 0.204 | 0.217 | 0.971 | 0.994 | 0.080 | True |
| Oro | Metalli preziosi | 0.010 | Timestral-28M | 708 | 0.017 | 0.091 | 0.195 | 0.916 | 0.994 | 0.080 | True |
| Oro | Metalli preziosi | 0.100 | Timestral-209M | 708 | 0.117 | 0.136 | 0.192 | 0.981 | 0.996 | 0.170 | True |
| Oro | Metalli preziosi | 0.050 | Timestral-209M | 708 | 0.066 | 0.056 | 0.161 | 0.970 | 0.996 | 0.170 | True |
| Oro | Metalli preziosi | 0.010 | Timestral-209M | 708 | 0.018 | 0.045 | 0.106 | 0.897 | 0.996 | 0.170 | True |
| Oro | Metalli preziosi | 0.100 | TimesFM-3 | 708 | 0.113 | 0.258 | 0.385 | 0.985 | 1.002 | 0.706 | True |
| Argento | Metalli preziosi | 0.100 | Simulazione storica | 708 | 0.127 | 0.020 | 0.060 | 1.000 | 1.000 |  | False |
| Argento | Metalli preziosi | 0.050 | Simulazione storica | 708 | 0.072 | 0.011 | 0.040 | 1.000 | 1.000 |  | True |
| Argento | Metalli preziosi | 0.010 | Simulazione storica | 708 | 0.021 | 0.009 | 0.021 | 1.000 | 1.000 |  | True |
| Argento | Metalli preziosi | 0.100 | GARCH-t | 708 | 0.109 | 0.443 | 0.281 | 0.915 | 0.977 | 0.001 | True |
| Argento | Metalli preziosi | 0.050 | GARCH-t | 708 | 0.065 | 0.080 | 0.175 | 0.896 | 0.977 | 0.001 | True |
| Argento | Metalli preziosi | 0.010 | GARCH-t | 708 | 0.011 | 0.734 | 0.190 | 0.895 | 0.977 | 0.001 | True |
| Argento | Metalli preziosi | 0.100 | Timestral-28M | 708 | 0.102 | 0.881 | 0.596 | 0.920 | 0.977 | 0.002 | True |
| Argento | Metalli preziosi | 0.050 | Timestral-28M | 708 | 0.062 | 0.152 | 0.317 | 0.909 | 0.977 | 0.002 | True |
| Argento | Metalli preziosi | 0.010 | Timestral-28M | 708 | 0.011 | 0.734 | 0.190 | 0.913 | 0.977 | 0.002 | True |
| Argento | Metalli preziosi | 0.100 | Timestral-209M | 708 | 0.102 | 0.881 | 0.596 | 0.920 | 0.976 | 0.001 | True |
| Argento | Metalli preziosi | 0.050 | Timestral-209M | 708 | 0.059 | 0.268 | 0.511 | 0.908 | 0.976 | 0.001 | True |
| Argento | Metalli preziosi | 0.010 | Timestral-209M | 708 | 0.014 | 0.299 | 0.180 | 0.919 | 0.976 | 0.001 | True |
| Argento | Metalli preziosi | 0.100 | TimesFM-3 | 708 | 0.099 | 0.920 | 0.694 | 0.937 | 0.982 | 0.020 | True |
| Rame | Metalli industriali | 0.100 | Simulazione storica | 708 | 0.106 | 0.602 | 0.803 | 1.000 | 1.000 |  | False |
| Rame | Metalli industriali | 0.050 | Simulazione storica | 708 | 0.064 | 0.111 | 0.281 | 1.000 | 1.000 |  | True |
| Rame | Metalli industriali | 0.010 | Simulazione storica | 708 | 0.020 | 0.021 | 0.006 | 1.000 | 1.000 |  | True |
| Rame | Metalli industriali | 0.100 | GARCH-t | 708 | 0.114 | 0.211 | 0.107 | 0.992 | 1.008 | 0.077 | True |
| Rame | Metalli industriali | 0.050 | GARCH-t | 708 | 0.059 | 0.268 | 0.513 | 0.962 | 1.008 | 0.077 | True |
| Rame | Metalli industriali | 0.010 | GARCH-t | 708 | 0.016 | 0.171 | 0.144 | 0.963 | 1.008 | 0.077 | True |
| Rame | Metalli industriali | 0.100 | Timestral-28M | 708 | 0.096 | 0.724 | 0.229 | 0.968 | 0.997 | 0.612 | True |
| Rame | Metalli industriali | 0.050 | Timestral-28M | 708 | 0.049 | 0.945 | 0.976 | 0.950 | 0.997 | 0.612 | True |
| Rame | Metalli industriali | 0.010 | Timestral-28M | 708 | 0.014 | 0.299 | 0.180 | 1.002 | 0.997 | 0.612 | True |
| Rame | Metalli industriali | 0.100 | Timestral-209M | 708 | 0.096 | 0.724 | 0.229 | 0.968 | 0.997 | 0.394 | True |
| Rame | Metalli industriali | 0.050 | Timestral-209M | 708 | 0.048 | 0.808 | 0.931 | 0.941 | 0.997 | 0.394 | True |
| Rame | Metalli industriali | 0.010 | Timestral-209M | 708 | 0.014 | 0.299 | 0.180 | 0.997 | 0.997 | 0.394 | True |
| Rame | Metalli industriali | 0.100 | TimesFM-3 | 708 | 0.102 | 0.881 | 0.333 | 0.964 | 1.000 | 0.901 | True |
| Grano | Cereali | 0.100 | Simulazione storica | 707 | 0.099 | 0.930 | 0.444 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 0.050 | Simulazione storica | 707 | 0.044 | 0.444 | 0.099 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 0.010 | Simulazione storica | 707 | 0.010 | 0.979 | 0.932 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 0.100 | GARCH-t | 707 | 0.072 | 0.010 | 0.027 | 0.989 | 0.994 | 0.077 | True |
| Grano | Cereali | 0.050 | GARCH-t | 707 | 0.027 | 0.002 | 0.007 | 1.009 | 0.994 | 0.077 | True |
| Grano | Cereali | 0.010 | GARCH-t | 707 | 0.000 | 0.000 | 0.001 | 1.085 | 0.994 | 0.077 | False |
| Grano | Cereali | 0.100 | Timestral-28M | 707 | 0.071 | 0.006 | 0.023 | 0.991 | 0.995 | 0.068 | False |
| Grano | Cereali | 0.050 | Timestral-28M | 707 | 0.025 | 0.001 | 0.003 | 0.997 | 0.995 | 0.068 | True |
| Grano | Cereali | 0.010 | Timestral-28M | 707 | 0.001 | 0.004 | 0.016 | 0.993 | 0.995 | 0.068 | True |
| Grano | Cereali | 0.100 | Timestral-209M | 707 | 0.079 | 0.057 | 0.154 | 0.992 | 0.994 | 0.051 | False |
| Grano | Cereali | 0.050 | Timestral-209M | 707 | 0.024 | 0.000 | 0.001 | 0.998 | 0.994 | 0.051 | True |
| Grano | Cereali | 0.010 | Timestral-209M | 707 | 0.001 | 0.004 | 0.016 | 1.021 | 0.994 | 0.051 | False |
| Grano | Cereali | 0.100 | TimesFM-3 | 707 | 0.085 | 0.170 | 0.225 | 0.975 | 0.991 | 0.029 | True |
| Mais | Cereali | 0.100 | Simulazione storica | 707 | 0.095 | 0.640 | 0.488 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 0.050 | Simulazione storica | 707 | 0.051 | 0.911 | 0.700 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 0.010 | Simulazione storica | 707 | 0.017 | 0.090 | 0.193 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 0.100 | GARCH-t | 707 | 0.083 | 0.132 | 0.322 | 0.997 | 0.998 | 0.544 | True |
| Mais | Cereali | 0.050 | GARCH-t | 707 | 0.041 | 0.259 | 0.179 | 1.006 | 0.998 | 0.544 | True |
| Mais | Cereali | 0.010 | GARCH-t | 707 | 0.008 | 0.678 | 0.871 | 0.959 | 0.998 | 0.544 | True |
| Mais | Cereali | 0.100 | Timestral-28M | 707 | 0.074 | 0.014 | 0.025 | 1.008 | 1.000 | 0.900 | True |
| Mais | Cereali | 0.050 | Timestral-28M | 707 | 0.038 | 0.133 | 0.219 | 1.002 | 1.000 | 0.900 | True |
| Mais | Cereali | 0.010 | Timestral-28M | 707 | 0.011 | 0.731 | 0.860 | 0.977 | 1.000 | 0.900 | True |
| Mais | Cereali | 0.100 | Timestral-209M | 707 | 0.074 | 0.014 | 0.040 | 1.003 | 0.997 | 0.428 | True |
| Mais | Cereali | 0.050 | Timestral-209M | 707 | 0.038 | 0.133 | 0.081 | 0.998 | 0.997 | 0.428 | True |
| Mais | Cereali | 0.010 | Timestral-209M | 707 | 0.010 | 0.979 | 0.932 | 0.960 | 0.997 | 0.428 | True |
| Mais | Cereali | 0.100 | TimesFM-3 | 707 | 0.081 | 0.076 | 0.202 | 1.002 | 1.003 | 0.433 | True |
| Soia | Cereali | 0.100 | Simulazione storica | 707 | 0.091 | 0.394 | 0.589 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 0.050 | Simulazione storica | 707 | 0.047 | 0.682 | 0.858 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 0.010 | Simulazione storica | 707 | 0.011 | 0.731 | 0.860 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 0.100 | GARCH-t | 707 | 0.089 | 0.326 | 0.598 | 1.003 | 1.000 | 0.929 | True |
| Soia | Cereali | 0.050 | GARCH-t | 707 | 0.035 | 0.060 | 0.169 | 0.982 | 1.000 | 0.929 | True |
| Soia | Cereali | 0.010 | GARCH-t | 707 | 0.010 | 0.979 | 0.932 | 0.957 | 1.000 | 0.929 | True |
| Soia | Cereali | 0.100 | Timestral-28M | 707 | 0.078 | 0.041 | 0.124 | 1.006 | 1.001 | 0.813 | True |
| Soia | Cereali | 0.050 | Timestral-28M | 707 | 0.025 | 0.001 | 0.003 | 0.996 | 1.001 | 0.813 | True |
| Soia | Cereali | 0.010 | Timestral-28M | 707 | 0.011 | 0.731 | 0.860 | 0.969 | 1.001 | 0.813 | True |
| Soia | Cereali | 0.100 | Timestral-209M | 707 | 0.079 | 0.057 | 0.160 | 1.012 | 1.002 | 0.493 | True |
| Soia | Cereali | 0.050 | Timestral-209M | 707 | 0.030 | 0.008 | 0.015 | 0.997 | 1.002 | 0.493 | True |
| Soia | Cereali | 0.010 | Timestral-209M | 707 | 0.010 | 0.979 | 0.932 | 0.967 | 1.002 | 0.493 | True |
| Soia | Cereali | 0.100 | TimesFM-3 | 707 | 0.088 | 0.266 | 0.431 | 1.002 | 1.002 | 0.506 | True |
| Caffe | Soft e bestiame | 0.100 | Simulazione storica | 708 | 0.106 | 0.602 | 0.205 | 1.000 | 1.000 |  | True |
| Caffe | Soft e bestiame | 0.050 | Simulazione storica | 708 | 0.058 | 0.346 | 0.366 | 1.000 | 1.000 |  | True |
| Caffe | Soft e bestiame | 0.010 | Simulazione storica | 708 | 0.014 | 0.299 | 0.505 | 1.000 | 1.000 |  | True |
| Caffe | Soft e bestiame | 0.100 | GARCH-t | 708 | 0.097 | 0.821 | 0.209 | 0.987 | 0.998 | 0.582 | True |
| Caffe | Soft e bestiame | 0.050 | GARCH-t | 708 | 0.056 | 0.437 | 0.453 | 0.999 | 0.998 | 0.582 | True |
| Caffe | Soft e bestiame | 0.010 | GARCH-t | 708 | 0.008 | 0.675 | 0.870 | 0.932 | 0.998 | 0.582 | True |
| Caffe | Soft e bestiame | 0.100 | Timestral-28M | 708 | 0.100 | 0.980 | 0.376 | 1.003 | 1.006 | 0.412 | True |
| Caffe | Soft e bestiame | 0.050 | Timestral-28M | 708 | 0.062 | 0.152 | 0.160 | 1.007 | 1.006 | 0.412 | True |
| Caffe | Soft e bestiame | 0.010 | Timestral-28M | 708 | 0.013 | 0.486 | 0.199 | 0.901 | 1.006 | 0.412 | True |
| Caffe | Soft e bestiame | 0.100 | Timestral-209M | 708 | 0.103 | 0.784 | 0.290 | 0.999 | 1.002 | 0.649 | True |
| Caffe | Soft e bestiame | 0.050 | Timestral-209M | 708 | 0.062 | 0.152 | 0.160 | 1.009 | 1.002 | 0.649 | True |
| Caffe | Soft e bestiame | 0.010 | Timestral-209M | 708 | 0.011 | 0.734 | 0.861 | 0.913 | 1.002 | 0.649 | True |
| Caffe | Soft e bestiame | 0.100 | TimesFM-3 | 708 | 0.097 | 0.821 | 0.449 | 1.000 | 1.000 | 0.933 | True |
| Zucchero | Soft e bestiame | 0.100 | Simulazione storica | 708 | 0.090 | 0.387 | 0.596 | 1.000 | 1.000 |  | True |
| Zucchero | Soft e bestiame | 0.050 | Simulazione storica | 708 | 0.048 | 0.808 | 0.580 | 1.000 | 1.000 |  | True |
| Zucchero | Soft e bestiame | 0.010 | Simulazione storica | 708 | 0.010 | 0.976 | 0.154 | 1.000 | 1.000 |  | False |
| Zucchero | Soft e bestiame | 0.100 | GARCH-t | 708 | 0.086 | 0.210 | 0.375 | 1.000 | 0.997 | 0.330 | True |
| Zucchero | Soft e bestiame | 0.050 | GARCH-t | 708 | 0.041 | 0.255 | 0.406 | 0.999 | 0.997 | 0.330 | True |
| Zucchero | Soft e bestiame | 0.010 | GARCH-t | 708 | 0.006 | 0.205 | 0.021 | 0.945 | 0.997 | 0.330 | True |
| Zucchero | Soft e bestiame | 0.100 | Timestral-28M | 708 | 0.082 | 0.099 | 0.238 | 1.003 | 0.999 | 0.696 | True |
| Zucchero | Soft e bestiame | 0.050 | Timestral-28M | 708 | 0.044 | 0.439 | 0.640 | 1.000 | 0.999 | 0.696 | True |
| Zucchero | Soft e bestiame | 0.010 | Timestral-28M | 708 | 0.007 | 0.407 | 0.054 | 0.940 | 0.999 | 0.696 | True |
| Zucchero | Soft e bestiame | 0.100 | Timestral-209M | 708 | 0.093 | 0.543 | 0.722 | 1.003 | 0.999 | 0.698 | True |
| Zucchero | Soft e bestiame | 0.050 | Timestral-209M | 708 | 0.045 | 0.551 | 0.755 | 1.000 | 0.999 | 0.698 | True |
| Zucchero | Soft e bestiame | 0.010 | Timestral-209M | 708 | 0.008 | 0.675 | 0.002 | 0.894 | 0.999 | 0.698 | True |
| Zucchero | Soft e bestiame | 0.100 | TimesFM-3 | 708 | 0.081 | 0.075 | 0.200 | 0.999 | 0.997 | 0.376 | True |
| Cacao | Soft e bestiame | 0.100 | Simulazione storica | 708 | 0.121 | 0.065 | 0.057 | 1.000 | 1.000 |  | True |
| Cacao | Soft e bestiame | 0.050 | Simulazione storica | 708 | 0.065 | 0.080 | 0.054 | 1.000 | 1.000 |  | True |
| Cacao | Soft e bestiame | 0.010 | Simulazione storica | 708 | 0.023 | 0.004 | 0.010 | 1.000 | 1.000 |  | True |
| Cacao | Soft e bestiame | 0.100 | GARCH-t | 708 | 0.105 | 0.690 | 0.253 | 0.955 | 0.988 | 0.038 | True |
| Cacao | Soft e bestiame | 0.050 | GARCH-t | 708 | 0.061 | 0.204 | 0.433 | 0.936 | 0.988 | 0.038 | True |
| Cacao | Soft e bestiame | 0.010 | GARCH-t | 708 | 0.017 | 0.091 | 0.195 | 0.850 | 0.988 | 0.038 | True |
| Cacao | Soft e bestiame | 0.100 | Timestral-28M | 708 | 0.103 | 0.784 | 0.606 | 0.959 | 0.994 | 0.306 | True |
| Cacao | Soft e bestiame | 0.050 | Timestral-28M | 708 | 0.047 | 0.676 | 0.855 | 0.945 | 0.994 | 0.306 | True |
| Cacao | Soft e bestiame | 0.010 | Timestral-28M | 708 | 0.011 | 0.734 | 0.861 | 0.819 | 0.994 | 0.306 | True |
| Cacao | Soft e bestiame | 0.100 | Timestral-209M | 708 | 0.120 | 0.084 | 0.185 | 0.967 | 0.990 | 0.028 | True |
| Cacao | Soft e bestiame | 0.050 | Timestral-209M | 708 | 0.061 | 0.204 | 0.409 | 0.941 | 0.990 | 0.028 | True |
| Cacao | Soft e bestiame | 0.010 | Timestral-209M | 708 | 0.014 | 0.299 | 0.505 | 0.826 | 0.990 | 0.028 | True |
| Cacao | Soft e bestiame | 0.100 | TimesFM-3 | 708 | 0.103 | 0.784 | 0.814 | 0.957 | 0.997 | 0.608 | True |
| Bestiame | Soft e bestiame | 0.100 | Simulazione storica | 707 | 0.106 | 0.593 | 0.616 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 0.050 | Simulazione storica | 707 | 0.054 | 0.651 | 0.390 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 0.010 | Simulazione storica | 707 | 0.014 | 0.297 | 0.503 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 0.100 | GARCH-t | 707 | 0.098 | 0.831 | 0.214 | 0.998 | 0.999 | 0.725 | True |
| Bestiame | Soft e bestiame | 0.050 | GARCH-t | 707 | 0.054 | 0.651 | 0.629 | 1.004 | 0.999 | 0.725 | True |
| Bestiame | Soft e bestiame | 0.010 | GARCH-t | 707 | 0.017 | 0.090 | 0.193 | 1.052 | 0.999 | 0.725 | True |
| Bestiame | Soft e bestiame | 0.100 | Timestral-28M | 707 | 0.106 | 0.593 | 0.616 | 0.990 | 0.999 | 0.510 | True |
| Bestiame | Soft e bestiame | 0.050 | Timestral-28M | 707 | 0.052 | 0.777 | 0.960 | 0.975 | 0.999 | 0.510 | True |
| Bestiame | Soft e bestiame | 0.010 | Timestral-28M | 707 | 0.016 | 0.170 | 0.327 | 1.037 | 0.999 | 0.510 | True |
| Bestiame | Soft e bestiame | 0.100 | Timestral-209M | 707 | 0.113 | 0.252 | 0.282 | 0.990 | 0.999 | 0.623 | True |
| Bestiame | Soft e bestiame | 0.050 | Timestral-209M | 707 | 0.061 | 0.201 | 0.404 | 0.979 | 0.999 | 0.623 | True |
| Bestiame | Soft e bestiame | 0.010 | Timestral-209M | 707 | 0.017 | 0.090 | 0.193 | 1.075 | 0.999 | 0.623 | True |
| Bestiame | Soft e bestiame | 0.100 | TimesFM-3 | 707 | 0.110 | 0.367 | 0.568 | 0.995 | 1.000 | 0.901 | True |

### Volatilita'

| asset | settore | h | modello | n | QLIKE/HAR | MSE/HAR | DM p (QLIKE) | in MCS |
|---|---|---|---|---|---|---|---|---|
| WTI | Energia | 1 | Media 22g | 708 | 1.417 | 1.219 | 0.056 | True |
| WTI | Energia | 1 | Random walk | 708 | 1.658 | 1.291 | 0.000 | False |
| WTI | Energia | 1 | Timestral-28M | 708 | 1.043 | 0.930 | 0.292 | True |
| WTI | Energia | 1 | Timestral-209M | 708 | 1.036 | 0.964 | 0.364 | True |
| WTI | Energia | 1 | TimesFM-3 | 708 | 1.006 | 0.908 | 0.881 | True |
| WTI | Energia | 1 | HAR | 708 | 1.000 | 1.000 |  | True |
| WTI | Energia | 5 | Media 22g | 704 | 1.459 | 1.181 | 0.069 | True |
| WTI | Energia | 5 | Random walk | 704 | 1.731 | 1.536 | 0.000 | False |
| WTI | Energia | 5 | Timestral-28M | 704 | 1.158 | 0.946 | 0.195 | True |
| WTI | Energia | 5 | Timestral-209M | 704 | 1.128 | 1.006 | 0.218 | True |
| WTI | Energia | 5 | TimesFM-3 | 704 | 1.114 | 0.937 | 0.296 | True |
| WTI | Energia | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| WTI | Energia | 20 | Media 22g | 689 | 1.207 | 1.228 | 0.110 | True |
| WTI | Energia | 20 | Random walk | 689 | 2.417 | 1.954 | 0.013 | False |
| WTI | Energia | 20 | Timestral-28M | 689 | 1.395 | 1.039 | 0.220 | True |
| WTI | Energia | 20 | Timestral-209M | 689 | 1.347 | 1.055 | 0.230 | True |
| WTI | Energia | 20 | TimesFM-3 | 689 | 1.370 | 1.037 | 0.229 | True |
| WTI | Energia | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Brent | Energia | 1 | Media 22g | 708 | 1.347 | 1.229 | 0.072 | True |
| Brent | Energia | 1 | Random walk | 708 | 1.938 | 1.309 | 0.000 | False |
| Brent | Energia | 1 | Timestral-28M | 708 | 1.062 | 0.973 | 0.319 | True |
| Brent | Energia | 1 | Timestral-209M | 708 | 1.043 | 0.993 | 0.474 | True |
| Brent | Energia | 1 | TimesFM-3 | 708 | 1.020 | 0.943 | 0.625 | True |
| Brent | Energia | 1 | HAR | 708 | 1.000 | 1.000 |  | True |
| Brent | Energia | 5 | Media 22g | 704 | 1.323 | 1.214 | 0.032 | True |
| Brent | Energia | 5 | Random walk | 704 | 2.028 | 1.646 | 0.000 | False |
| Brent | Energia | 5 | Timestral-28M | 704 | 1.168 | 1.010 | 0.205 | True |
| Brent | Energia | 5 | Timestral-209M | 704 | 1.138 | 1.055 | 0.249 | True |
| Brent | Energia | 5 | TimesFM-3 | 704 | 1.151 | 1.017 | 0.177 | True |
| Brent | Energia | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Brent | Energia | 20 | Media 22g | 689 | 1.151 | 1.261 | 0.073 | True |
| Brent | Energia | 20 | Random walk | 689 | 2.579 | 2.038 | 0.001 | False |
| Brent | Energia | 20 | Timestral-28M | 689 | 1.364 | 1.081 | 0.145 | True |
| Brent | Energia | 20 | Timestral-209M | 689 | 1.313 | 1.086 | 0.151 | True |
| Brent | Energia | 20 | TimesFM-3 | 689 | 1.341 | 1.076 | 0.147 | True |
| Brent | Energia | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Gasolio | Energia | 1 | Media 22g | 708 | 1.345 | 1.273 | 0.001 | False |
| Gasolio | Energia | 1 | Random walk | 708 | 1.652 | 1.354 | 0.000 | False |
| Gasolio | Energia | 1 | Timestral-28M | 708 | 1.034 | 0.976 | 0.205 | True |
| Gasolio | Energia | 1 | Timestral-209M | 708 | 1.010 | 0.965 | 0.729 | True |
| Gasolio | Energia | 1 | TimesFM-3 | 708 | 1.013 | 1.004 | 0.697 | True |
| Gasolio | Energia | 1 | HAR | 708 | 1.000 | 1.000 |  | True |
| Gasolio | Energia | 5 | Media 22g | 704 | 1.382 | 1.264 | 0.008 | False |
| Gasolio | Energia | 5 | Random walk | 704 | 1.904 | 1.595 | 0.000 | False |
| Gasolio | Energia | 5 | Timestral-28M | 704 | 1.147 | 1.020 | 0.102 | True |
| Gasolio | Energia | 5 | Timestral-209M | 704 | 1.111 | 1.021 | 0.173 | True |
| Gasolio | Energia | 5 | TimesFM-3 | 704 | 1.097 | 1.035 | 0.218 | True |
| Gasolio | Energia | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Gasolio | Energia | 20 | Media 22g | 689 | 1.085 | 1.212 | 0.410 | True |
| Gasolio | Energia | 20 | Random walk | 689 | 2.264 | 1.914 | 0.000 | False |
| Gasolio | Energia | 20 | Timestral-28M | 689 | 1.266 | 1.061 | 0.107 | True |
| Gasolio | Energia | 20 | Timestral-209M | 689 | 1.250 | 1.064 | 0.118 | True |
| Gasolio | Energia | 20 | TimesFM-3 | 689 | 1.296 | 1.081 | 0.120 | True |
| Gasolio | Energia | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 1 | Media 22g | 708 | 1.320 | 1.101 | 0.064 | False |
| Benzina | Energia | 1 | Random walk | 708 | 1.679 | 1.318 | 0.000 | False |
| Benzina | Energia | 1 | Timestral-28M | 708 | 1.081 | 0.922 | 0.246 | True |
| Benzina | Energia | 1 | Timestral-209M | 708 | 1.066 | 0.938 | 0.261 | True |
| Benzina | Energia | 1 | TimesFM-3 | 708 | 1.069 | 0.930 | 0.197 | True |
| Benzina | Energia | 1 | HAR | 708 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 5 | Media 22g | 704 | 1.320 | 1.037 | 0.119 | True |
| Benzina | Energia | 5 | Random walk | 704 | 2.304 | 1.670 | 0.000 | False |
| Benzina | Energia | 5 | Timestral-28M | 704 | 1.277 | 0.933 | 0.138 | True |
| Benzina | Energia | 5 | Timestral-209M | 704 | 1.282 | 0.967 | 0.130 | True |
| Benzina | Energia | 5 | TimesFM-3 | 704 | 1.275 | 0.953 | 0.134 | True |
| Benzina | Energia | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Benzina | Energia | 20 | Media 22g | 689 | 1.207 | 1.080 | 0.294 | True |
| Benzina | Energia | 20 | Random walk | 689 | 3.184 | 2.090 | 0.003 | False |
| Benzina | Energia | 20 | Timestral-28M | 689 | 1.319 | 0.932 | 0.353 | True |
| Benzina | Energia | 20 | Timestral-209M | 689 | 1.348 | 0.953 | 0.333 | True |
| Benzina | Energia | 20 | TimesFM-3 | 689 | 1.367 | 0.949 | 0.323 | True |
| Benzina | Energia | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Gas naturale | Energia | 1 | Media 22g | 708 | 1.145 | 1.317 | 0.000 | False |
| Gas naturale | Energia | 1 | Random walk | 708 | 1.648 | 1.196 | 0.000 | False |
| Gas naturale | Energia | 1 | Timestral-28M | 708 | 0.949 | 0.920 | 0.006 | False |
| Gas naturale | Energia | 1 | Timestral-209M | 708 | 0.940 | 0.910 | 0.002 | True |
| Gas naturale | Energia | 1 | TimesFM-3 | 708 | 0.924 | 0.888 | 0.002 | True |
| Gas naturale | Energia | 1 | HAR | 708 | 1.000 | 1.000 |  | False |
| Gas naturale | Energia | 5 | Media 22g | 704 | 1.078 | 1.274 | 0.088 | True |
| Gas naturale | Energia | 5 | Random walk | 704 | 2.074 | 1.371 | 0.000 | False |
| Gas naturale | Energia | 5 | Timestral-28M | 704 | 0.895 | 0.842 | 0.026 | True |
| Gas naturale | Energia | 5 | Timestral-209M | 704 | 0.899 | 0.860 | 0.039 | True |
| Gas naturale | Energia | 5 | TimesFM-3 | 704 | 0.865 | 0.800 | 0.033 | True |
| Gas naturale | Energia | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Gas naturale | Energia | 20 | Media 22g | 689 | 0.997 | 1.289 | 0.980 | True |
| Gas naturale | Energia | 20 | Random walk | 689 | 2.668 | 2.167 | 0.000 | False |
| Gas naturale | Energia | 20 | Timestral-28M | 689 | 0.893 | 0.878 | 0.064 | True |
| Gas naturale | Energia | 20 | Timestral-209M | 689 | 0.900 | 0.918 | 0.063 | True |
| Gas naturale | Energia | 20 | TimesFM-3 | 689 | 0.918 | 0.885 | 0.148 | True |
| Gas naturale | Energia | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Oro | Metalli preziosi | 1 | Media 22g | 708 | 1.215 | 1.379 | 0.000 | False |
| Oro | Metalli preziosi | 1 | Random walk | 708 | 1.605 | 1.145 | 0.000 | False |
| Oro | Metalli preziosi | 1 | Timestral-28M | 708 | 1.007 | 0.976 | 0.813 | True |
| Oro | Metalli preziosi | 1 | Timestral-209M | 708 | 0.994 | 0.940 | 0.853 | True |
| Oro | Metalli preziosi | 1 | TimesFM-3 | 708 | 0.981 | 0.883 | 0.613 | True |
| Oro | Metalli preziosi | 1 | HAR | 708 | 1.000 | 1.000 |  | True |
| Oro | Metalli preziosi | 5 | Media 22g | 704 | 1.101 | 1.249 | 0.055 | True |
| Oro | Metalli preziosi | 5 | Random walk | 704 | 1.995 | 1.442 | 0.000 | False |
| Oro | Metalli preziosi | 5 | Timestral-28M | 704 | 1.012 | 0.988 | 0.816 | True |
| Oro | Metalli preziosi | 5 | Timestral-209M | 704 | 1.014 | 0.988 | 0.823 | True |
| Oro | Metalli preziosi | 5 | TimesFM-3 | 704 | 1.022 | 0.932 | 0.735 | True |
| Oro | Metalli preziosi | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Oro | Metalli preziosi | 20 | Media 22g | 689 | 1.033 | 1.231 | 0.783 | True |
| Oro | Metalli preziosi | 20 | Random walk | 689 | 2.316 | 2.087 | 0.000 | False |
| Oro | Metalli preziosi | 20 | Timestral-28M | 689 | 1.114 | 1.098 | 0.101 | True |
| Oro | Metalli preziosi | 20 | Timestral-209M | 689 | 1.150 | 1.155 | 0.064 | True |
| Oro | Metalli preziosi | 20 | TimesFM-3 | 689 | 1.160 | 1.108 | 0.130 | True |
| Oro | Metalli preziosi | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Rame | Metalli industriali | 1 | Media 22g | 691 | 1.025 | 1.081 | 0.669 | True |
| Rame | Metalli industriali | 1 | Random walk | 691 | 20.640 | 1.206 | 0.000 | False |
| Rame | Metalli industriali | 1 | Timestral-28M | 691 | 1.131 | 0.716 | 0.330 | True |
| Rame | Metalli industriali | 1 | Timestral-209M | 691 | 1.134 | 0.698 | 0.409 | True |
| Rame | Metalli industriali | 1 | TimesFM-3 | 691 | 1.185 | 0.742 | 0.252 | True |
| Rame | Metalli industriali | 1 | HAR | 691 | 1.000 | 1.000 |  | True |
| Rame | Metalli industriali | 5 | Media 22g | 704 | 1.085 | 1.140 | 0.285 | True |
| Rame | Metalli industriali | 5 | Random walk | 704 | 45.463 | 1.495 | 0.000 | False |
| Rame | Metalli industriali | 5 | Timestral-28M | 704 | 1.200 | 0.692 | 0.331 | True |
| Rame | Metalli industriali | 5 | Timestral-209M | 704 | 1.267 | 0.673 | 0.381 | True |
| Rame | Metalli industriali | 5 | TimesFM-3 | 704 | 1.305 | 0.720 | 0.139 | True |
| Rame | Metalli industriali | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Rame | Metalli industriali | 20 | Media 22g | 689 | 1.361 | 1.305 | 0.019 | False |
| Rame | Metalli industriali | 20 | Random walk | 689 | 96.077 | 2.171 | 0.000 | False |
| Rame | Metalli industriali | 20 | Timestral-28M | 689 | 1.530 | 0.761 | 0.093 | False |
| Rame | Metalli industriali | 20 | Timestral-209M | 689 | 1.671 | 0.762 | 0.144 | False |
| Rame | Metalli industriali | 20 | TimesFM-3 | 689 | 1.593 | 0.782 | 0.019 | False |
| Rame | Metalli industriali | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 1 | Media 22g | 680 | 1.053 | 1.050 | 0.012 | False |
| Grano | Cereali | 1 | Random walk | 680 | 15.982 | 1.219 | 0.091 | True |
| Grano | Cereali | 1 | Timestral-28M | 680 | 1.025 | 0.763 | 0.828 | True |
| Grano | Cereali | 1 | Timestral-209M | 680 | 1.087 | 0.733 | 0.583 | True |
| Grano | Cereali | 1 | TimesFM-3 | 680 | 1.003 | 0.778 | 0.975 | True |
| Grano | Cereali | 1 | HAR | 680 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 5 | Media 22g | 703 | 1.045 | 1.007 | 0.346 | True |
| Grano | Cereali | 5 | Random walk | 703 | 58.475 | 1.853 | 0.031 | True |
| Grano | Cereali | 5 | Timestral-28M | 703 | 0.836 | 0.567 | 0.301 | True |
| Grano | Cereali | 5 | Timestral-209M | 703 | 0.821 | 0.516 | 0.306 | True |
| Grano | Cereali | 5 | TimesFM-3 | 703 | 0.894 | 0.667 | 0.345 | True |
| Grano | Cereali | 5 | HAR | 703 | 1.000 | 1.000 |  | True |
| Grano | Cereali | 20 | Media 22g | 688 | 1.005 | 0.855 | 0.978 | True |
| Grano | Cereali | 20 | Random walk | 688 | 301.755 | 3.573 | 0.063 | True |
| Grano | Cereali | 20 | Timestral-28M | 688 | 0.793 | 0.539 | 0.500 | False |
| Grano | Cereali | 20 | Timestral-209M | 688 | 0.698 | 0.482 | 0.311 | True |
| Grano | Cereali | 20 | TimesFM-3 | 688 | 0.767 | 0.573 | 0.392 | True |
| Grano | Cereali | 20 | HAR | 688 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 1 | Media 22g | 707 | 1.061 | 0.956 | 0.165 | True |
| Mais | Cereali | 1 | Random walk | 707 | 2.355 | 1.456 | 0.000 | False |
| Mais | Cereali | 1 | Timestral-28M | 707 | 1.047 | 0.885 | 0.440 | True |
| Mais | Cereali | 1 | Timestral-209M | 707 | 1.055 | 0.883 | 0.406 | True |
| Mais | Cereali | 1 | TimesFM-3 | 707 | 1.055 | 0.893 | 0.380 | True |
| Mais | Cereali | 1 | HAR | 707 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 5 | Media 22g | 703 | 1.125 | 0.937 | 0.199 | True |
| Mais | Cereali | 5 | Random walk | 703 | 4.326 | 2.449 | 0.000 | False |
| Mais | Cereali | 5 | Timestral-28M | 703 | 1.072 | 0.871 | 0.478 | True |
| Mais | Cereali | 5 | Timestral-209M | 703 | 1.101 | 0.874 | 0.381 | True |
| Mais | Cereali | 5 | TimesFM-3 | 703 | 1.069 | 0.874 | 0.497 | True |
| Mais | Cereali | 5 | HAR | 703 | 1.000 | 1.000 |  | True |
| Mais | Cereali | 20 | Media 22g | 688 | 1.174 | 0.850 | 0.529 | True |
| Mais | Cereali | 20 | Random walk | 688 | 8.577 | 3.717 | 0.000 | False |
| Mais | Cereali | 20 | Timestral-28M | 688 | 0.985 | 0.740 | 0.944 | True |
| Mais | Cereali | 20 | Timestral-209M | 688 | 1.029 | 0.740 | 0.906 | True |
| Mais | Cereali | 20 | TimesFM-3 | 688 | 0.995 | 0.757 | 0.982 | True |
| Mais | Cereali | 20 | HAR | 688 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 1 | Media 22g | 696 | 1.070 | 1.009 | 0.011 | False |
| Soia | Cereali | 1 | Random walk | 696 | 7.377 | 1.389 | 0.067 | True |
| Soia | Cereali | 1 | Timestral-28M | 696 | 1.050 | 0.895 | 0.173 | True |
| Soia | Cereali | 1 | Timestral-209M | 696 | 1.029 | 0.878 | 0.471 | True |
| Soia | Cereali | 1 | TimesFM-3 | 696 | 1.055 | 0.903 | 0.161 | True |
| Soia | Cereali | 1 | HAR | 696 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 5 | Media 22g | 703 | 1.120 | 0.977 | 0.137 | False |
| Soia | Cereali | 5 | Random walk | 703 | 41.915 | 2.356 | 0.189 | True |
| Soia | Cereali | 5 | Timestral-28M | 703 | 1.015 | 0.850 | 0.824 | False |
| Soia | Cereali | 5 | Timestral-209M | 703 | 0.940 | 0.796 | 0.419 | True |
| Soia | Cereali | 5 | TimesFM-3 | 703 | 1.045 | 0.869 | 0.529 | False |
| Soia | Cereali | 5 | HAR | 703 | 1.000 | 1.000 |  | True |
| Soia | Cereali | 20 | Media 22g | 688 | 1.344 | 1.001 | 0.270 | True |
| Soia | Cereali | 20 | Random walk | 688 | 402.777 | 4.247 | 0.291 | True |
| Soia | Cereali | 20 | Timestral-28M | 688 | 0.883 | 0.670 | 0.489 | True |
| Soia | Cereali | 20 | Timestral-209M | 688 | 0.844 | 0.634 | 0.389 | True |
| Soia | Cereali | 20 | TimesFM-3 | 688 | 0.987 | 0.723 | 0.949 | True |
| Soia | Cereali | 20 | HAR | 688 | 1.000 | 1.000 |  | True |
| Zucchero | Soft e bestiame | 1 | Media 22g | 707 | 1.086 | 1.071 | 0.002 | False |
| Zucchero | Soft e bestiame | 1 | Random walk | 707 | 2.010 | 1.590 | 0.000 | False |
| Zucchero | Soft e bestiame | 1 | Timestral-28M | 707 | 1.022 | 0.946 | 0.347 | True |
| Zucchero | Soft e bestiame | 1 | Timestral-209M | 707 | 1.018 | 0.946 | 0.430 | True |
| Zucchero | Soft e bestiame | 1 | TimesFM-3 | 707 | 1.024 | 0.956 | 0.282 | True |
| Zucchero | Soft e bestiame | 1 | HAR | 707 | 1.000 | 1.000 |  | True |
| Zucchero | Soft e bestiame | 5 | Media 22g | 704 | 1.169 | 1.153 | 0.016 | False |
| Zucchero | Soft e bestiame | 5 | Random walk | 704 | 3.354 | 2.450 | 0.000 | False |
| Zucchero | Soft e bestiame | 5 | Timestral-28M | 704 | 1.036 | 0.926 | 0.592 | True |
| Zucchero | Soft e bestiame | 5 | Timestral-209M | 704 | 1.029 | 0.924 | 0.655 | True |
| Zucchero | Soft e bestiame | 5 | TimesFM-3 | 704 | 1.046 | 0.939 | 0.471 | True |
| Zucchero | Soft e bestiame | 5 | HAR | 704 | 1.000 | 1.000 |  | True |
| Zucchero | Soft e bestiame | 20 | Media 22g | 689 | 1.299 | 1.206 | 0.057 | True |
| Zucchero | Soft e bestiame | 20 | Random walk | 689 | 5.048 | 3.439 | 0.000 | False |
| Zucchero | Soft e bestiame | 20 | Timestral-28M | 689 | 1.069 | 0.890 | 0.694 | True |
| Zucchero | Soft e bestiame | 20 | Timestral-209M | 689 | 1.055 | 0.889 | 0.744 | True |
| Zucchero | Soft e bestiame | 20 | TimesFM-3 | 689 | 1.087 | 0.904 | 0.623 | True |
| Zucchero | Soft e bestiame | 20 | HAR | 689 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 1 | Media 22g | 707 | 1.049 | 1.024 | 0.062 | True |
| Bestiame | Soft e bestiame | 1 | Random walk | 707 | 2.641 | 1.378 | 0.001 | False |
| Bestiame | Soft e bestiame | 1 | Timestral-28M | 707 | 0.968 | 0.862 | 0.387 | True |
| Bestiame | Soft e bestiame | 1 | Timestral-209M | 707 | 0.979 | 0.865 | 0.643 | True |
| Bestiame | Soft e bestiame | 1 | TimesFM-3 | 707 | 0.988 | 0.876 | 0.767 | True |
| Bestiame | Soft e bestiame | 1 | HAR | 707 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 5 | Media 22g | 703 | 1.180 | 1.121 | 0.017 | False |
| Bestiame | Soft e bestiame | 5 | Random walk | 703 | 5.165 | 2.273 | 0.000 | False |
| Bestiame | Soft e bestiame | 5 | Timestral-28M | 703 | 1.020 | 0.885 | 0.761 | True |
| Bestiame | Soft e bestiame | 5 | Timestral-209M | 703 | 1.055 | 0.893 | 0.504 | True |
| Bestiame | Soft e bestiame | 5 | TimesFM-3 | 703 | 1.054 | 0.905 | 0.507 | True |
| Bestiame | Soft e bestiame | 5 | HAR | 703 | 1.000 | 1.000 |  | True |
| Bestiame | Soft e bestiame | 20 | Media 22g | 688 | 1.501 | 1.354 | 0.002 | False |
| Bestiame | Soft e bestiame | 20 | Random walk | 688 | 9.344 | 3.858 | 0.000 | False |
| Bestiame | Soft e bestiame | 20 | Timestral-28M | 688 | 1.198 | 0.952 | 0.268 | True |
| Bestiame | Soft e bestiame | 20 | Timestral-209M | 688 | 1.249 | 0.974 | 0.192 | True |
| Bestiame | Soft e bestiame | 20 | TimesFM-3 | 688 | 1.209 | 0.974 | 0.279 | True |
| Bestiame | Soft e bestiame | 20 | HAR | 688 | 1.000 | 1.000 |  | True |
