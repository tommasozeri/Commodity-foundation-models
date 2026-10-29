# Esperimento con covariate: WTI

Future WTI, test dal 02/01/2024 al 23/10/2026 (708 origini giornaliere), contesto 4096 giorni, stessi compiti e metriche del pilota. I foundation model ricevono solo il passato delle covariate (past covariates), allineato al calendario del WTI con l'ultimo valore disponibile a ogni data.

| configurazione | covariate |
|---|---|
| Brent | future Brent (prezzo, rendimento o volatilita' Garman-Klass, come il compito) |
| Mercato | dollaro DXY (livello, rendimento o rendimento assoluto) e OVX (volatilita' implicita) |
| Scorte | scorte USA di greggio esclusa la SPR (EIA), usate dal 6° giorno dopo la fine della settimana, cioe' dopo la pubblicazione; variazione % per il compito rendimento |
| Tutte | le quattro serie |
| Placebo | rumore sintetico con le statistiche del Brent, indipendente dal WTI |

## Con covariate contro senza

Rapporto tra la perdita con covariate e quella dello stesso modello senza covariate (CRPS sul prezzo, pinball sul rendimento, QLIKE sulla volatilita'); < 1 = le covariate aiutano. ▼/▲ = significativamente meglio/peggio (Diebold-Mariano, Benjamini-Hochberg al 10% su tutte le coppie modello x configurazione dello stesso compito e orizzonte).

| modello | covariate | prezzo h=1 | prezzo h=5 | prezzo h=20 | rendimento h=1 | vol h=1 | vol h=5 | vol h=20 |
|---|---|---|---|---|---|---|---|---|
| Timestral-28M | Brent | 0.998 | 0.996 | 1.004 | 1.000 | 1.011 | 1.014 | 1.005 |
| Timestral-28M | Mercato | 1.002 | 1.006 | 1.013 | 0.997 | 0.849 ▼ | 0.728 | 0.789 |
| Timestral-28M | Scorte | 1.000 | 1.000 | 0.997 | 0.999 | 0.994 | 0.983 | 1.004 |
| Timestral-28M | Tutte | 0.998 | 0.998 | 1.005 | 0.996 | 0.864 ▼ | 0.758 | 0.816 |
| Timestral-28M | Placebo | 1.000 | 1.001 | 0.998 | 1.000 | 0.994 | 0.956 | 0.942 |
| Timestral-209M | Brent | 0.998 | 0.998 | 0.998 | 1.000 | 1.008 | 1.017 | 1.002 |
| Timestral-209M | Mercato | 0.999 | 1.003 | 1.013 | 0.998 | 0.873 ▼ | 0.790 | 0.790 |
| Timestral-209M | Scorte | 1.001 | 1.004 | 1.005 | 1.001 | 0.999 | 0.997 | 1.000 |
| Timestral-209M | Tutte | 1.000 | 1.004 | 1.012 | 0.998 | 0.879 ▼ | 0.799 | 0.821 |
| Timestral-209M | Placebo | 0.998 | 1.001 | 1.002 | 1.000 | 1.008 | 1.000 | 0.975 |
| TimesFM-3 | Brent | 0.999 | 0.996 | 1.002 | 0.999 | 1.001 | 1.000 | 0.987 |
| TimesFM-3 | Mercato | 0.999 | 1.013 | 1.021 | 0.998 | 0.939 ▼ | 0.856 | 0.900 |
| TimesFM-3 | Scorte | 0.998 | 1.003 | 1.003 | 1.001 | 1.009 | 1.009 | 1.004 |
| TimesFM-3 | Tutte | 1.003 | 1.009 | 1.022 | 0.997 | 0.932 ▼ | 0.849 | 0.889 |
| TimesFM-3 | Placebo | 0.998 | 0.997 | 1.003 | 0.998 | 0.997 | 0.969 | 0.952 |
| Chronos-2 | Brent | 0.998 | 0.997 | 0.998 | 1.000 | 1.001 | 1.005 | 0.998 |
| Chronos-2 | Mercato | 1.011 | 0.989 | 1.011 | 0.997 | 0.903 ▼ | 0.796 | 0.866 |
| Chronos-2 | Scorte | 0.997 | 1.000 | 1.002 | 1.003 | 1.023 | 1.066 | 1.062 |
| Chronos-2 | Tutte | 1.011 | 0.992 | 1.017 | 0.998 | 0.918 ▼ | 0.821 | 0.888 |
| Chronos-2 | Placebo | 0.989 | 0.996 | 1.001 | 0.999 | 1.038 | 1.000 | 0.955 |

**Esiti significativi per configurazione** (su tutti i modelli, compiti e orizzonti)

| covariate | meglio | non significativo |
|---|---|---|
| Brent | 0 | 28 |
| Mercato | 4 | 24 |
| Scorte | 0 | 28 |
| Tutte | 4 | 24 |
| Placebo | 0 | 28 |

## Punteggi rispetto ai benchmark del pilota

CRPS/random walk sul prezzo, tick loss/simulazione storica sul VaR, QLIKE/HAR sulla volatilita'. Ogni modello senza covariate e con ciascuna configurazione, accanto ai benchmark classici; HAR-X (OVX) e' l'HAR con la varianza implicita dell'OVX come regressore, cioe' un modello classico con la stessa informazione di mercato (dove la regressione va sotto il pavimento si usa l'HAR).

| modello | prezzo h=1 | prezzo h=5 | prezzo h=20 | VaR 10% | VaR 1% | volatilita h=1 | volatilita h=5 | volatilita h=20 |
|---|---|---|---|---|---|---|---|---|
| Timestral-28M | 0.970 | 0.950 | 0.960 | 0.949 | 0.729 | 1.048 | 1.155 | 1.278 |
| Timestral-28M + Brent | 0.968 | 0.947 | 0.964 | 0.947 | 0.716 | 1.060 | 1.171 | 1.284 |
| Timestral-28M + Mercato | 0.972 | 0.957 | 0.972 | 0.940 | 0.668 | 0.890 | 0.841 | 1.009 |
| Timestral-28M + Scorte | 0.970 | 0.950 | 0.957 | 0.948 | 0.730 | 1.042 | 1.135 | 1.283 |
| Timestral-28M + Tutte | 0.968 | 0.949 | 0.965 | 0.940 | 0.669 | 0.905 | 0.875 | 1.044 |
| Timestral-28M + Placebo | 0.970 | 0.951 | 0.959 | 0.948 | 0.722 | 1.041 | 1.104 | 1.204 |
| Timestral-209M | 0.973 | 0.953 | 0.964 | 0.949 | 0.720 | 1.024 | 1.110 | 1.269 |
| Timestral-209M + Brent | 0.971 | 0.951 | 0.962 | 0.949 | 0.715 | 1.032 | 1.129 | 1.271 |
| Timestral-209M + Mercato | 0.972 | 0.956 | 0.977 | 0.942 | 0.680 | 0.893 | 0.877 | 1.003 |
| Timestral-209M + Scorte | 0.974 | 0.956 | 0.969 | 0.954 | 0.730 | 1.023 | 1.107 | 1.270 |
| Timestral-209M + Tutte | 0.973 | 0.957 | 0.976 | 0.941 | 0.684 | 0.900 | 0.887 | 1.043 |
| Timestral-209M + Placebo | 0.971 | 0.954 | 0.966 | 0.949 | 0.726 | 1.032 | 1.110 | 1.237 |
| TimesFM-3 | 0.977 | 0.952 | 0.965 | 0.955 |  | 0.997 | 1.127 | 1.282 |
| TimesFM-3 + Brent | 0.975 | 0.948 | 0.967 | 0.954 |  | 0.998 | 1.127 | 1.265 |
| TimesFM-3 + Mercato | 0.976 | 0.964 | 0.986 | 0.946 |  | 0.936 | 0.964 | 1.154 |
| TimesFM-3 + Scorte | 0.974 | 0.954 | 0.968 | 0.952 |  | 1.006 | 1.137 | 1.286 |
| TimesFM-3 + Tutte | 0.980 | 0.960 | 0.987 | 0.951 |  | 0.929 | 0.957 | 1.139 |
| TimesFM-3 + Placebo | 0.974 | 0.948 | 0.968 | 0.949 |  | 0.994 | 1.091 | 1.220 |
| Chronos-2 | 1.000 | 0.980 | 0.982 | 0.976 | 0.746 | 1.032 | 1.155 | 1.259 |
| Chronos-2 + Brent | 0.998 | 0.977 | 0.979 | 0.971 | 0.731 | 1.033 | 1.160 | 1.257 |
| Chronos-2 + Mercato | 1.011 | 0.969 | 0.993 | 0.971 | 0.766 | 0.932 | 0.920 | 1.091 |
| Chronos-2 + Scorte | 0.997 | 0.979 | 0.983 | 0.979 | 0.767 | 1.056 | 1.231 | 1.337 |
| Chronos-2 + Tutte | 1.012 | 0.972 | 0.998 | 0.969 | 0.758 | 0.947 | 0.948 | 1.118 |
| Chronos-2 + Placebo | 0.989 | 0.976 | 0.983 | 0.970 | 0.755 | 1.072 | 1.155 | 1.203 |
| ARIMA | 0.991 | 0.981 | 0.973 |  |  |  |  |  |
| ETS | 0.988 | 0.978 | 0.974 |  |  |  |  |  |
| GARCH-t |  |  |  | 0.942 | 0.723 |  |  |  |
| GJR-GARCH-t |  |  |  | 0.949 | 0.796 |  |  |  |
| EGARCH-t |  |  |  | 0.954 | 0.866 |  |  |  |
| HAR-X (OVX) |  |  |  |  |  | 1.299 | 0.970 | 0.697 |
| Media 22g |  |  |  |  |  | 1.417 | 1.459 | 1.207 |
