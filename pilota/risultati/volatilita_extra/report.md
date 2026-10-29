# Volatilita': Log-HAR e combinazioni

QLIKE del modello / QLIKE del riferimento, media geometrica sugli asset; tra parentesi asset significativamente migliori/peggiori (DM + BH al 10%). Combinazioni: media a pesi uguali delle varianze previste.

## 12 asset: contro il Log-HAR

| modello | contro | 1 | 5 | 20 |
|---|---|---|---|---|
| HAR | Log-HAR | 0.978 (0/0) | 1.002 (0/0) | 1.012 (0/0) |
| Timestral-28M | Log-HAR | 1.002 (0/0) | 1.040 (1/0) | 1.055 (0/0) |
| Timestral-209M | Log-HAR | 0.991 (1/0) | 1.023 (1/0) | 1.063 (0/0) |
| TimesFM-3 | Log-HAR | 0.982 (2/0) | 1.026 (1/0) | 1.072 (0/0) |
| Chronos-2 | Log-HAR | 1.007 (0/0) | 1.071 (0/0) | 1.098 (0/0) |
| Timestral-28M + Log-HAR | Log-HAR | 0.968 (3/0) | 0.973 (1/0) | 0.945 (4/0) |
| Timestral-209M + Log-HAR | Log-HAR | 0.961 (4/0) | 0.961 (2/0) | 0.941 (4/0) |
| TimesFM-3 + Log-HAR | Log-HAR | 0.959 (3/0) | 0.968 (1/0) | 0.956 (3/0) |
| Chronos-2 + Log-HAR | Log-HAR | 0.963 (3/0) | 0.973 (1/0) | 0.947 (3/0) |

| modello | in MCS |
|---|---|
| HAR | 33/36 |
| Log-HAR | 25/36 |
| Timestral-28M | 30/36 |
| Timestral-209M | 33/36 |
| TimesFM-3 | 33/36 |
| Chronos-2 | 26/36 |
| Timestral-28M + Log-HAR | 30/36 |
| Timestral-209M + Log-HAR | 36/36 |
| TimesFM-3 + Log-HAR | 34/36 |
| Chronos-2 + Log-HAR | 33/36 |

## 5 asset con volatilita' implicita propria: contro il Log-HAR-X

| modello | contro | 1 | 5 | 20 |
|---|---|---|---|---|
| Log-HAR-X | Log-HAR | 0.907 (4/0) | 0.840 (3/0) | 0.857 (0/0) |
| Timestral-28M + IV | Log-HAR-X | 0.940 (1/0) | 1.009 (0/0) | 1.173 (0/0) |
| Timestral-209M + IV | Log-HAR-X | 0.942 (1/0) | 1.029 (0/0) | 1.139 (0/0) |
| TimesFM-3 + IV | Log-HAR-X | 0.973 (1/0) | 1.120 (0/0) | 1.270 (0/0) |
| Chronos-2 + IV | Log-HAR-X | 1.013 (1/1) | 1.234 (0/3) | 1.318 (0/0) |
| Timestral-28M + IV + Log-HAR-X | Log-HAR-X | 0.939 (5/0) | 0.972 (0/0) | 1.045 (0/0) |
| Timestral-209M + IV + Log-HAR-X | Log-HAR-X | 0.941 (5/0) | 0.986 (0/0) | 1.035 (0/0) |
| TimesFM-3 + IV + Log-HAR-X | Log-HAR-X | 0.953 (2/0) | 1.016 (0/0) | 1.075 (0/0) |
| Chronos-2 + IV + Log-HAR-X | Log-HAR-X | 0.963 (1/0) | 1.050 (0/0) | 1.083 (0/0) |

| modello | in MCS |
|---|---|
| Log-HAR-X | 12/15 |
| Timestral-28M + IV | 14/15 |
| Timestral-209M + IV | 15/15 |
| TimesFM-3 + IV | 10/15 |
| Chronos-2 + IV | 6/15 |
| Timestral-28M + IV + Log-HAR-X | 14/15 |
| Timestral-209M + IV + Log-HAR-X | 15/15 |
| TimesFM-3 + IV + Log-HAR-X | 14/15 |
| Chronos-2 + IV + Log-HAR-X | 13/15 |
