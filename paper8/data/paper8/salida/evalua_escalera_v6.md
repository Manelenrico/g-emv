# La escalera con la reserva (v6): la evaluación (el experimento)

Partidas leídas: RG69r+voz 200, S69+voz 200, P69+voz 200.

## Las predicciones

**E1** (SE CUMPLE). Vivas el día 40, RG69r+voz − S69+voz, los cinco mundos juntos (200 parejas): +0.19 [+0.07, +0.32]. Se cumple si el límite de abajo es > 0.

**E2** (FALLA). Vivas el día 40, RG69r+voz − S69+voz, la sequía (40 parejas): +0.12 [-0.07, +0.33]. Se cumple si el límite de abajo es > 0.

**Cuentan 2; se cumplen 1.**

## Lo declarado, medido igual (sin predicción)

- Vivas el día 40, RG69r+voz − P69+voz, los cinco mundos juntos (200 parejas): +0.10 [-0.03, +0.23].
- Vivas el día 40, RG69r+voz − P69+voz, la sequía (40 parejas): +0.20 [-0.03, +0.42].
- (El efecto del v5, RG68r − S68 en los cinco juntos, sobre la base vieja: +0,41 [+0,27, +0,57], de motor_frente_simple_v5.md.)

## Vivas el día 40 (de 8; media de las semillas)

| mundo | RG69r+voz | S69+voz | P69+voz |
|---|---|---|---|
| abundancia | 8.00 | 8.00 | 7.95 |
| normal | 8.00 | 7.95 | 8.00 |
| sequia | 7.80 | 7.67 | 7.60 |
| sequia_dura | 4.22 | 3.73 | 4.05 |
| bestias_crian | 6.65 | 6.38 | 6.55 |
| los cinco | 6.93 | 6.75 | 6.83 |

## Las medidas sin predicción, por mundo (emparejadas por semilla)

**vivas el día 40**

| mundo | RG69r+voz · S69+voz · P69+voz (medias) | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 8.00 · 8.00 · 7.95 | +0.00 [+0.00, +0.00] | +0.05 [+0.00, +0.15] |
| normal | 8.00 · 7.95 · 8.00 | +0.05 [+0.00, +0.12] | +0.00 [+0.00, +0.00] |
| sequia | 7.80 · 7.67 · 7.60 | +0.12 [-0.07, +0.33] | +0.20 [-0.03, +0.42] |
| sequia_dura | 4.22 · 3.73 · 4.05 | +0.50 [+0.15, +0.85] | +0.17 [-0.23, +0.57] |
| bestias_crian | 6.65 · 6.38 · 6.55 | +0.28 [-0.17, +0.75] | +0.10 [-0.35, +0.53] |

**muertes de hambre por partida**

| mundo | RG69r+voz · S69+voz · P69+voz (medias) | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 0.00 · 0.00 · 0.00 | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] |
| normal | 0.00 · 0.00 · 0.00 | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] |
| sequia | 0.07 · 0.28 · 0.28 | -0.20 [-0.35, -0.05] | -0.20 [-0.40, -0.03] |
| sequia_dura | 3.48 · 4.22 · 3.67 | -0.75 [-1.10, -0.38] | -0.20 [-0.62, +0.23] |
| bestias_crian | 0.25 · 0.42 · 0.57 | -0.17 [-0.47, +0.07] | -0.33 [-0.57, -0.07] |

**turnos al día con hambre > 30 y comida en la bolsa, días 0 a 9**

| mundo | RG69r+voz · S69+voz · P69+voz (medias) | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 1.90 · 1.78 · 2.19 | +0.12 [-0.33, +0.57] | -0.29 [-0.69, +0.15] |
| normal | 3.56 · 2.77 · 3.46 | +0.78 [+0.17, +1.42] | +0.10 [-0.59, +0.78] |
| sequia | 2.04 · 2.17 · 2.59 | -0.14 [-0.68, +0.38] | -0.56 [-1.07, -0.05] |
| sequia_dura | 3.92 · 4.01 · 5.02 | -0.09 [-0.69, +0.50] | -1.10 [-1.79, -0.38] |
| bestias_crian | 4.32 · 3.87 · 4.88 | +0.45 [-0.17, +1.08] | -0.56 [-1.15, +0.02] |

**noches dormidas fuera, días 0 a 9 (parte de las noches, por partida)**

| mundo | RG69r+voz · S69+voz · P69+voz (medias) | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 0.047 · 0.103 · 0.072 | -0.056 [-0.079, -0.036] | -0.025 [-0.040, -0.010] |
| normal | 0.065 · 0.097 · 0.095 | -0.032 [-0.051, -0.014] | -0.030 [-0.045, -0.015] |
| sequia | 0.060 · 0.110 · 0.088 | -0.051 [-0.076, -0.028] | -0.028 [-0.044, -0.013] |
| sequia_dura | 0.081 · 0.108 · 0.112 | -0.027 [-0.051, -0.005] | -0.031 [-0.047, -0.015] |
| bestias_crian | 0.077 · 0.113 · 0.120 | -0.036 [-0.057, -0.018] | -0.044 [-0.061, -0.027] |

**empujones a otra criatura por partida**

| mundo | RG69r+voz · S69+voz · P69+voz (medias) | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 67.08 · 127.38 · 120.78 | -60.30 [-74.45, -46.27] | -53.70 [-63.73, -43.60] |
| normal | 120.12 · 136.62 · 142.72 | -16.50 [-29.82, -3.38] | -22.60 [-32.73, -12.18] |
| sequia | 107.50 · 142.05 · 135.88 | -34.55 [-52.05, -17.95] | -28.38 [-38.40, -19.25] |
| sequia_dura | 72.60 · 98.58 · 92.75 | -25.98 [-40.02, -11.18] | -20.15 [-35.50, -5.20] |
| bestias_crian | 131.22 · 164.65 · 157.05 | -33.42 [-46.98, -19.90] | -25.82 [-36.92, -14.60] |

**felicidad de la aldea**

| mundo | RG69r+voz · S69+voz · P69+voz (medias) | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 0.921 · 0.895 · 0.885 | +0.025 [+0.017, +0.034] | +0.036 [+0.026, +0.046] |
| normal | 0.793 · 0.786 · 0.766 | +0.007 [-0.007, +0.022] | +0.027 [+0.014, +0.041] |
| sequia | 0.717 · 0.679 · 0.675 | +0.038 [+0.020, +0.055] | +0.042 [+0.026, +0.060] |
| sequia_dura | 0.451 · 0.412 · 0.413 | +0.039 [+0.009, +0.068] | +0.038 [+0.007, +0.068] |
| bestias_crian | 0.533 · 0.491 · 0.481 | +0.043 [+0.023, +0.063] | +0.053 [+0.027, +0.079] |

## Muertes por causa (bestia · hambre · terreno), sumadas en las partidas de cada mundo

| mundo | RG69r+voz | S69+voz | P69+voz |
|---|---|---|---|
| abundancia | 0 · 0 · 0 | 0 · 0 · 0 | 2 · 0 · 0 |
| normal | 0 · 0 · 0 | 2 · 0 · 0 | 0 · 0 · 0 |
| sequia | 5 · 3 · 0 | 2 · 11 · 0 | 5 · 11 · 0 |
| sequia_dura | 9 · 139 · 3 | 2 · 169 · 0 | 9 · 147 · 2 |
| bestias_crian | 42 · 10 · 2 | 48 · 17 · 0 | 35 · 23 · 0 |
| los cinco | 56 · 152 · 5 | 54 · 197 · 0 | 51 · 181 · 2 |
