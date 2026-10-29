# Controlli di robustezza del pilota

## 1. Spot vs futures (energia, 5 coppie)

Stessi compiti e protocollo del pilota (contesto 4096 giorni) sui prezzi spot FRED/EIA, che non hanno roll dei contratti. Valori < 1 = meglio del benchmark; media geometrica sulle 5 coppie.

| modello | CRPS/RW h=1 fut | CRPS/RW h=1 spot | CRPS/RW h=5 fut | CRPS/RW h=5 spot | CRPS/RW h=20 fut | CRPS/RW h=20 spot | pinball/SS fut | pinball/SS spot |
|---|---|---|---|---|---|---|---|---|
| Chronos-2 | 1.002 | 0.979 | 0.988 | 0.938 | 0.964 | 0.925 | 0.987 | 0.986 |
| GARCH-t |  |  |  |  |  |  | 0.988 | 0.986 |
| TimesFM-3 | 0.977 | 0.950 | 0.969 | 0.916 | 0.957 | 0.913 | 0.990 | 0.983 |
| Timestral-209M | 0.969 | 0.941 | 0.962 | 0.915 | 0.952 | 0.911 | 0.985 | 0.979 |
| Timestral-28M | 0.972 | 0.949 | 0.961 | 0.912 | 0.954 | 0.908 | 0.986 | 0.978 |

**Asset con differenza significativa (DM + Benjamini-Hochberg al 10%, su 5)**

| compito | h | modello | meglio (BH) fut | meglio (BH) spot | peggio (BH) fut | peggio (BH) spot |
|---|---|---|---|---|---|---|
| prezzo | 1 | ARIMA | 0 | 0 | 0 | 0 |
| prezzo | 1 | Chronos-2 | 0 | 0 | 0 | 0 |
| prezzo | 1 | ETS | 2 | 2 | 0 | 1 |
| prezzo | 1 | TimesFM-3 | 4 | 5 | 0 | 0 |
| prezzo | 1 | Timestral-209M | 5 | 5 | 0 | 0 |
| prezzo | 1 | Timestral-28M | 4 | 4 | 0 | 0 |
| prezzo | 5 | ARIMA | 2 | 1 | 0 | 0 |
| prezzo | 5 | Chronos-2 | 0 | 0 | 0 | 0 |
| prezzo | 5 | ETS | 5 | 2 | 0 | 0 |
| prezzo | 5 | TimesFM-3 | 3 | 5 | 0 | 0 |
| prezzo | 5 | Timestral-209M | 4 | 5 | 0 | 0 |
| prezzo | 5 | Timestral-28M | 4 | 5 | 0 | 0 |
| prezzo | 20 | ARIMA | 1 | 0 | 0 | 0 |
| prezzo | 20 | Chronos-2 | 0 | 0 | 0 | 0 |
| prezzo | 20 | ETS | 0 | 0 | 0 | 0 |
| prezzo | 20 | TimesFM-3 | 1 | 0 | 0 | 0 |
| prezzo | 20 | Timestral-209M | 2 | 0 | 0 | 0 |
| prezzo | 20 | Timestral-28M | 0 | 0 | 0 | 0 |
| rendimento | 1 | Chronos-2 | 4 | 3 | 0 | 0 |
| rendimento | 1 | EGARCH-t | 4 | 4 | 0 | 0 |
| rendimento | 1 | GARCH-t | 4 | 4 | 0 | 0 |
| rendimento | 1 | GJR-GARCH-t | 4 | 4 | 0 | 0 |
| rendimento | 1 | TimesFM-3 | 3 | 1 | 0 | 0 |
| rendimento | 1 | Timestral-209M | 5 | 5 | 0 | 0 |
| rendimento | 1 | Timestral-28M | 4 | 5 | 0 | 0 |

**Dettaglio per coppia**

| coppia | modello | CRPS/RW h=1 fut | CRPS/RW h=1 spot | CRPS/RW h=5 fut | CRPS/RW h=5 spot | CRPS/RW h=20 fut | CRPS/RW h=20 spot | pinball/SS fut | pinball/SS spot |
|---|---|---|---|---|---|---|---|---|---|
| Benzina | Chronos-2 | 1.002 | 1.007 | 0.990 | 1.001 | 0.958 | 0.981 | 0.988 | 0.988 |
| Benzina | GARCH-t |  |  |  |  |  |  | 0.990 | 0.988 |
| Benzina | TimesFM-3 | 0.980 | 0.978 | 0.965 | 0.979 | 0.941 | 0.962 | 0.991 | 0.994 |
| Benzina | Timestral-209M | 0.970 | 0.970 | 0.956 | 0.971 | 0.929 | 0.958 | 0.985 | 0.986 |
| Benzina | Timestral-28M | 0.974 | 0.973 | 0.962 | 0.968 | 0.945 | 0.961 | 0.988 | 0.989 |
| Brent | Chronos-2 | 0.993 | 0.991 | 0.993 | 0.992 | 0.986 | 0.983 | 0.983 | 0.984 |
| Brent | GARCH-t |  |  |  |  |  |  | 0.977 | 0.980 |
| Brent | TimesFM-3 | 0.970 | 0.964 | 0.963 | 0.955 | 0.966 | 0.965 | 0.984 | 0.990 |
| Brent | Timestral-209M | 0.966 | 0.963 | 0.963 | 0.961 | 0.967 | 0.965 | 0.978 | 0.979 |
| Brent | Timestral-28M | 0.965 | 0.959 | 0.961 | 0.956 | 0.972 | 0.967 | 0.980 | 0.982 |
| Gas naturale | Chronos-2 | 1.006 | 0.886 | 0.965 | 0.757 | 0.906 | 0.734 | 0.994 | 0.981 |
| Gas naturale | GARCH-t |  |  |  |  |  |  | 1.010 | 0.988 |
| Gas naturale | TimesFM-3 | 0.989 | 0.860 | 0.976 | 0.749 | 0.939 | 0.749 | 0.999 | 0.947 |
| Gas naturale | Timestral-209M | 0.973 | 0.842 | 0.954 | 0.745 | 0.922 | 0.732 | 0.994 | 0.957 |
| Gas naturale | Timestral-28M | 0.983 | 0.876 | 0.946 | 0.736 | 0.910 | 0.715 | 0.994 | 0.945 |
| Gasolio | Chronos-2 | 1.008 | 1.006 | 1.013 | 0.991 | 0.994 | 0.973 | 0.983 | 0.988 |
| Gasolio | GARCH-t |  |  |  |  |  |  | 0.980 | 0.988 |
| Gasolio | TimesFM-3 | 0.968 | 0.970 | 0.990 | 0.964 | 0.975 | 0.950 | 0.988 | 0.990 |
| Gasolio | Timestral-209M | 0.962 | 0.964 | 0.983 | 0.965 | 0.981 | 0.961 | 0.981 | 0.986 |
| Gasolio | Timestral-28M | 0.970 | 0.969 | 0.987 | 0.970 | 0.987 | 0.968 | 0.984 | 0.987 |
| WTI | Chronos-2 | 1.000 | 1.011 | 0.980 | 0.977 | 0.982 | 0.985 | 0.989 | 0.991 |
| WTI | GARCH-t |  |  |  |  |  |  | 0.984 | 0.985 |
| WTI | TimesFM-3 | 0.977 | 0.983 | 0.952 | 0.956 | 0.965 | 0.961 | 0.991 | 0.993 |
| WTI | Timestral-209M | 0.973 | 0.974 | 0.953 | 0.957 | 0.964 | 0.965 | 0.985 | 0.988 |
| WTI | Timestral-28M | 0.970 | 0.973 | 0.950 | 0.954 | 0.960 | 0.958 | 0.986 | 0.989 |

