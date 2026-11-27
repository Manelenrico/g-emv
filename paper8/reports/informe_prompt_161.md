# Prompt 161: los días de cosecha, lo que sabe y aprende la criatura, y cuatro figuras del v6

Solo análisis, lectura y figuras. No se juega ninguna partida, no se toca nada sellado y no se usa la clave. Las figuras están en `figuras/` (PNG y PDF): `v6_A_vivas`, `v6_B_costumbres`, `v6_C_duelo_soledad` y `v6_D_un_dia`.

## Parte 1: los días con fruto frente a los días sin fruto

Es análisis hecho después de ver los datos, no una predicción, y no propongo causas. El programa es `dias_cosecha_161.py`. Las tablas completas están más abajo, copiadas de `salida/dias_cosecha_161.md`.

**Cómo se mide.**
- **Las partidas.** Tres jugadores de la escalera, cinco mundos y las semillas 30161-30200: 600 partidas.
- **Los días.** Se comparan los días con fruto (3, 5, …, 39) con los días sin fruto (2, 4, …, 40). El día 1 no entra, como en el 160.
- **Por partida** se saca la media de cada lado. La diferencia (con fruto − sin fruto) se empareja dentro de la partida.
- **El resultado** es la media de las 40 partidas, con su intervalo del 95 %. En todas las filas entran las 40 partidas.
- **Los balances** salen del registro `balance.jsonl.gz`, que apuntó el lanzador: la fuerza de ganancia menos la de pérdida. Se cuentan solo los turnos despierta.
- **Lo demás** sale del registro del mundo, en los turnos viva.
- **«En un huerto o pegada a él»** quiere decir en una de sus 64 casillas o en las de alrededor, también en diagonal: 144 casillas en total.

**Lo que sale, en pocas palabras.**
- **Los balances bajo cero.** Los días con fruto, los tres balances pasan más tiempo bajo cero en casi todos los mundos y jugadores. El que más cae es el de los recursos:
  - **normal:** +3,6 puntos en RG69r+voz, +8,3 en S69+voz y +7,3 en P69+voz;
  - **bestias que crían:** +10,0, +13,1 y +11,9.
- **Las excepciones** son la abundancia, donde las diferencias son de un punto o menos, y algunas celdas sueltas: los recursos de RG69r+voz en la abundancia y el vínculo de S69+voz en la abundancia.
- **El huerto.** Los días con fruto se trabaja menos el huerto (de 4 a 9 turnos menos por criatura) y se pasa mucho menos tiempo en él o pegada a él (de 18 a 56 turnos menos), en todos los mundos.
- **El cansancio** es algo menor los días con fruto, de 0 a 2,6 puntos.
- **El hambre** es algo menor en la abundancia y algo mayor en las sequías y en las bestias que crían, hasta +3 puntos en S69+voz en la sequía dura.
- **Los empujones** son más los días con fruto, entre +0,15 y +1,26 al día en la aldea.
- **La comida cogida** es menor o igual los días con fruto.
- **La comida comida** casi no cambia: menos de 0,15 por criatura y día.

### Qué balance cae más los días con fruto, una frase por mundo

«Cae más» quiere decir el que más sube su parte de turnos despierta bajo cero los días con fruto, en puntos.
- **Abundancia:** casi no cae ninguno. Lo que más cae es el vínculo en RG69r+voz (+0,7 [+0,3, +1,2]) y en P69+voz (+2,4 [+1,9, +2,9]); en S69+voz, los recursos (+0,7 [−0,1, +1,6], el intervalo toca cero).
- **Normal:** el de los recursos, en los tres: +3,6 [+2,7, +4,4] en RG69r+voz, +8,3 [+6,9, +9,6] en S69+voz y +7,3 [+6,3, +8,2] en P69+voz.
- **Sequía:** el de los recursos, en los tres: +6,7 [+5,9, +7,6], +9,8 [+8,5, +10,9] y +8,5 [+7,3, +9,8].
- **Sequía dura:** el de los recursos, en los tres: +6,9 [+5,8, +8,0], +8,7 [+7,2, +10,2] y +8,7 [+7,1, +10,3].
- **Bestias que crían:** el de los recursos, en los tres: +10,0 [+9,1, +11,0], +13,1 [+12,0, +14,2] y +11,9 [+10,6, +13,2].

### Las tablas (de `salida/dias_cosecha_161.md`)

#### balance del cuerpo bajo cero (parte de los turnos despierta, en %)

| mundo | jugador | días con fruto | días sin fruto | con fruto − sin fruto (95 %) | partidas |
|---|---|---|---|---|---|
| abundancia | RG69r+voz | 1.5 | 1.5 | +0.1 [-0.2, +0.4] | 40 |
| abundancia | S69+voz | 1.8 | 1.6 | +0.3 [-0.0, +0.5] | 40 |
| abundancia | P69+voz | 3.6 | 3.0 | +0.6 [+0.3, +0.9] | 40 |
| normal | RG69r+voz | 6.1 | 5.5 | +0.7 [+0.2, +1.1] | 40 |
| normal | S69+voz | 3.9 | 3.2 | +0.8 [+0.4, +1.1] | 40 |
| normal | P69+voz | 7.1 | 5.3 | +1.8 [+1.4, +2.2] | 40 |
| sequía | RG69r+voz | 11.1 | 9.1 | +2.0 [+1.5, +2.5] | 40 |
| sequía | S69+voz | 11.5 | 8.1 | +3.4 [+2.7, +4.2] | 40 |
| sequía | P69+voz | 14.2 | 11.2 | +3.0 [+2.4, +3.5] | 40 |
| sequía dura | RG69r+voz | 47.5 | 44.5 | +3.0 [+2.1, +3.9] | 40 |
| sequía dura | S69+voz | 50.5 | 47.7 | +2.8 [+1.9, +3.6] | 40 |
| sequía dura | P69+voz | 52.0 | 48.9 | +3.0 [+2.1, +4.0] | 40 |
| bestias que crían | RG69r+voz | 30.5 | 27.1 | +3.4 [+1.8, +5.1] | 40 |
| bestias que crían | S69+voz | 32.3 | 27.7 | +4.6 [+2.7, +6.5] | 40 |
| bestias que crían | P69+voz | 34.7 | 30.8 | +4.0 [+2.6, +5.3] | 40 |

#### balance de los recursos bajo cero (%)

| mundo | jugador | días con fruto | días sin fruto | con fruto − sin fruto (95 %) | partidas |
|---|---|---|---|---|---|
| abundancia | RG69r+voz | 3.8 | 4.1 | -0.3 [-0.7, +0.2] | 40 |
| abundancia | S69+voz | 9.2 | 8.5 | +0.7 [-0.1, +1.6] | 40 |
| abundancia | P69+voz | 5.1 | 4.1 | +1.0 [+0.5, +1.5] | 40 |
| normal | RG69r+voz | 13.9 | 10.4 | +3.6 [+2.7, +4.4] | 40 |
| normal | S69+voz | 23.7 | 15.5 | +8.3 [+6.9, +9.6] | 40 |
| normal | P69+voz | 18.2 | 10.9 | +7.3 [+6.3, +8.2] | 40 |
| sequía | RG69r+voz | 23.8 | 17.0 | +6.7 [+5.9, +7.6] | 40 |
| sequía | S69+voz | 34.2 | 24.5 | +9.8 [+8.5, +10.9] | 40 |
| sequía | P69+voz | 27.6 | 19.1 | +8.5 [+7.3, +9.8] | 40 |
| sequía dura | RG69r+voz | 42.4 | 35.4 | +6.9 [+5.8, +8.0] | 40 |
| sequía dura | S69+voz | 49.4 | 40.7 | +8.7 [+7.2, +10.2] | 40 |
| sequía dura | P69+voz | 46.6 | 37.9 | +8.7 [+7.1, +10.3] | 40 |
| bestias que crían | RG69r+voz | 38.0 | 28.0 | +10.0 [+9.1, +11.0] | 40 |
| bestias que crían | S69+voz | 49.1 | 36.0 | +13.1 [+12.0, +14.2] | 40 |
| bestias que crían | P69+voz | 43.7 | 31.8 | +11.9 [+10.6, +13.2] | 40 |

#### balance del vínculo bajo cero (%)

| mundo | jugador | días con fruto | días sin fruto | con fruto − sin fruto (95 %) | partidas |
|---|---|---|---|---|---|
| abundancia | RG69r+voz | 5.0 | 4.3 | +0.7 [+0.3, +1.2] | 40 |
| abundancia | S69+voz | 1.8 | 1.8 | -0.0 [-0.2, +0.2] | 40 |
| abundancia | P69+voz | 8.1 | 5.7 | +2.4 [+1.9, +2.9] | 40 |
| normal | RG69r+voz | 12.7 | 10.6 | +2.1 [+1.5, +2.7] | 40 |
| normal | S69+voz | 4.3 | 3.4 | +0.9 [+0.6, +1.2] | 40 |
| normal | P69+voz | 13.4 | 9.6 | +3.8 [+3.2, +4.3] | 40 |
| sequía | RG69r+voz | 15.5 | 12.7 | +2.8 [+2.2, +3.4] | 40 |
| sequía | S69+voz | 8.3 | 6.2 | +2.1 [+1.7, +2.5] | 40 |
| sequía | P69+voz | 17.2 | 13.2 | +4.0 [+3.4, +4.7] | 40 |
| sequía dura | RG69r+voz | 48.8 | 45.6 | +3.2 [+2.5, +4.0] | 40 |
| sequía dura | S69+voz | 46.8 | 44.7 | +2.2 [+1.4, +3.0] | 40 |
| sequía dura | P69+voz | 49.0 | 45.6 | +3.4 [+2.7, +4.1] | 40 |
| bestias que crían | RG69r+voz | 23.6 | 19.6 | +4.1 [+3.4, +4.8] | 40 |
| bestias que crían | S69+voz | 15.2 | 13.3 | +1.9 [+1.4, +2.4] | 40 |
| bestias que crían | P69+voz | 24.4 | 20.9 | +3.6 [+2.9, +4.3] | 40 |

#### turnos de trabajo en el huerto, por criatura y día

| mundo | jugador | días con fruto | días sin fruto | con fruto − sin fruto (95 %) | partidas |
|---|---|---|---|---|---|
| abundancia | RG69r+voz | 17.50 | 23.12 | -5.61 [-8.12, -3.15] | 40 |
| abundancia | S69+voz | 15.84 | 23.70 | -7.87 [-10.29, -5.45] | 40 |
| abundancia | P69+voz | 18.00 | 22.68 | -4.68 [-6.56, -2.71] | 40 |
| normal | RG69r+voz | 17.29 | 23.37 | -6.08 [-8.56, -3.62] | 40 |
| normal | S69+voz | 15.70 | 24.44 | -8.74 [-11.04, -6.45] | 40 |
| normal | P69+voz | 18.20 | 22.49 | -4.29 [-6.56, -2.08] | 40 |
| sequía | RG69r+voz | 18.03 | 23.07 | -5.04 [-7.44, -2.55] | 40 |
| sequía | S69+voz | 15.87 | 24.57 | -8.70 [-11.17, -6.25] | 40 |
| sequía | P69+voz | 18.88 | 22.65 | -3.78 [-6.05, -1.46] | 40 |
| sequía dura | RG69r+voz | 25.68 | 32.29 | -6.61 [-8.79, -4.40] | 40 |
| sequía dura | S69+voz | 25.36 | 32.39 | -7.03 [-9.43, -4.75] | 40 |
| sequía dura | P69+voz | 26.41 | 31.23 | -4.82 [-7.39, -2.31] | 40 |
| bestias que crían | RG69r+voz | 19.00 | 24.23 | -5.23 [-7.76, -2.66] | 40 |
| bestias que crían | S69+voz | 17.43 | 25.73 | -8.30 [-10.72, -5.81] | 40 |
| bestias que crían | P69+voz | 19.25 | 23.96 | -4.71 [-7.23, -2.20] | 40 |

#### cansancio medio (0 a 100)

| mundo | jugador | días con fruto | días sin fruto | con fruto − sin fruto (95 %) | partidas |
|---|---|---|---|---|---|
| abundancia | RG69r+voz | 8.9 | 11.1 | -2.2 [-3.0, -1.4] | 40 |
| abundancia | S69+voz | 9.1 | 11.7 | -2.6 [-3.5, -1.7] | 40 |
| abundancia | P69+voz | 12.8 | 13.5 | -0.7 [-1.3, +0.0] | 40 |
| normal | RG69r+voz | 14.7 | 15.9 | -1.2 [-2.0, -0.4] | 40 |
| normal | S69+voz | 10.6 | 13.1 | -2.5 [-3.4, -1.6] | 40 |
| normal | P69+voz | 15.7 | 15.7 | -0.1 [-0.8, +0.7] | 40 |
| sequía | RG69r+voz | 16.1 | 16.8 | -0.7 [-1.3, -0.0] | 40 |
| sequía | S69+voz | 13.1 | 14.7 | -1.6 [-2.5, -0.7] | 40 |
| sequía | P69+voz | 17.5 | 17.6 | -0.0 [-0.8, +0.7] | 40 |
| sequía dura | RG69r+voz | 22.3 | 22.6 | -0.4 [-1.0, +0.4] | 40 |
| sequía dura | S69+voz | 19.8 | 21.2 | -1.3 [-2.2, -0.4] | 40 |
| sequía dura | P69+voz | 24.4 | 24.6 | -0.2 [-0.8, +0.5] | 40 |
| bestias que crían | RG69r+voz | 21.6 | 22.2 | -0.6 [-1.4, +0.3] | 40 |
| bestias que crían | S69+voz | 17.7 | 19.3 | -1.5 [-2.4, -0.7] | 40 |
| bestias que crían | P69+voz | 22.3 | 23.1 | -0.8 [-1.7, +0.1] | 40 |

#### hambre media (0 a 100)

| mundo | jugador | días con fruto | días sin fruto | con fruto − sin fruto (95 %) | partidas |
|---|---|---|---|---|---|
| abundancia | RG69r+voz | 4.3 | 4.9 | -0.6 [-0.7, -0.4] | 40 |
| abundancia | S69+voz | 4.8 | 5.1 | -0.3 [-0.5, -0.2] | 40 |
| abundancia | P69+voz | 4.6 | 5.0 | -0.4 [-0.5, -0.3] | 40 |
| normal | RG69r+voz | 5.8 | 6.2 | -0.4 [-0.6, -0.2] | 40 |
| normal | S69+voz | 6.8 | 6.3 | +0.5 [+0.3, +0.7] | 40 |
| normal | P69+voz | 6.5 | 6.3 | +0.2 [+0.0, +0.3] | 40 |
| sequía | RG69r+voz | 8.2 | 7.7 | +0.5 [+0.3, +0.7] | 40 |
| sequía | S69+voz | 10.6 | 8.8 | +1.8 [+1.4, +2.3] | 40 |
| sequía | P69+voz | 9.3 | 8.5 | +0.8 [+0.5, +1.2] | 40 |
| sequía dura | RG69r+voz | 13.9 | 12.3 | +1.6 [+1.1, +2.0] | 40 |
| sequía dura | S69+voz | 17.7 | 14.7 | +3.0 [+2.2, +3.8] | 40 |
| sequía dura | P69+voz | 14.7 | 12.9 | +1.8 [+1.1, +2.5] | 40 |
| bestias que crían | RG69r+voz | 10.3 | 9.4 | +0.8 [+0.5, +1.1] | 40 |
| bestias que crían | S69+voz | 12.8 | 10.4 | +2.5 [+2.0, +3.0] | 40 |
| bestias que crían | P69+voz | 11.9 | 10.2 | +1.7 [+1.3, +2.1] | 40 |

#### empujones de la aldea en el día

| mundo | jugador | días con fruto | días sin fruto | con fruto − sin fruto (95 %) | partidas |
|---|---|---|---|---|---|
| abundancia | RG69r+voz | 1.77 | 1.25 | +0.52 [+0.25, +0.81] | 40 |
| abundancia | S69+voz | 3.30 | 2.61 | +0.69 [+0.25, +1.11] | 40 |
| abundancia | P69+voz | 3.42 | 2.17 | +1.26 [+0.91, +1.61] | 40 |
| normal | RG69r+voz | 3.29 | 2.46 | +0.83 [+0.49, +1.17] | 40 |
| normal | S69+voz | 3.63 | 2.81 | +0.82 [+0.31, +1.32] | 40 |
| normal | P69+voz | 3.90 | 2.74 | +1.17 [+0.85, +1.50] | 40 |
| sequía | RG69r+voz | 2.80 | 2.29 | +0.51 [+0.25, +0.76] | 40 |
| sequía | S69+voz | 3.60 | 3.06 | +0.53 [+0.02, +1.03] | 40 |
| sequía | P69+voz | 3.51 | 2.84 | +0.66 [+0.29, +1.03] | 40 |
| sequía dura | RG69r+voz | 1.72 | 1.57 | +0.15 [-0.08, +0.37] | 40 |
| sequía dura | S69+voz | 2.34 | 2.09 | +0.25 [-0.05, +0.56] | 40 |
| sequía dura | P69+voz | 2.16 | 1.93 | +0.22 [+0.03, +0.42] | 40 |
| bestias que crían | RG69r+voz | 3.41 | 2.84 | +0.57 [+0.27, +0.91] | 40 |
| bestias que crían | S69+voz | 4.01 | 3.80 | +0.21 [-0.21, +0.66] | 40 |
| bestias que crían | P69+voz | 3.94 | 3.39 | +0.55 [+0.25, +0.84] | 40 |

#### turnos en un huerto o pegada a él, por criatura y día

| mundo | jugador | días con fruto | días sin fruto | con fruto − sin fruto (95 %) | partidas |
|---|---|---|---|---|---|
| abundancia | RG69r+voz | 91.2 | 143.2 | -52.0 [-59.5, -44.4] | 40 |
| abundancia | S69+voz | 70.4 | 126.3 | -55.9 [-65.4, -46.6] | 40 |
| abundancia | P69+voz | 90.7 | 136.1 | -45.4 [-52.0, -39.3] | 40 |
| normal | RG69r+voz | 75.9 | 115.5 | -39.6 [-47.0, -32.3] | 40 |
| normal | S69+voz | 65.5 | 112.0 | -46.4 [-55.1, -38.2] | 40 |
| normal | P69+voz | 76.5 | 112.8 | -36.3 [-43.8, -28.9] | 40 |
| sequía | RG69r+voz | 82.3 | 114.3 | -32.0 [-38.4, -25.7] | 40 |
| sequía | S69+voz | 72.7 | 116.4 | -43.8 [-52.1, -35.8] | 40 |
| sequía | P69+voz | 81.6 | 113.1 | -31.6 [-38.3, -24.7] | 40 |
| sequía dura | RG69r+voz | 105.9 | 126.8 | -20.9 [-27.7, -14.3] | 40 |
| sequía dura | S69+voz | 117.9 | 146.2 | -28.3 [-35.5, -21.4] | 40 |
| sequía dura | P69+voz | 104.5 | 123.0 | -18.4 [-24.4, -12.5] | 40 |
| bestias que crían | RG69r+voz | 69.9 | 97.2 | -27.3 [-33.8, -21.0] | 40 |
| bestias que crían | S69+voz | 68.3 | 100.4 | -32.1 [-39.9, -24.4] | 40 |
| bestias que crían | P69+voz | 70.5 | 93.1 | -22.6 [-29.8, -15.5] | 40 |

#### comida cogida, por criatura y día

| mundo | jugador | días con fruto | días sin fruto | con fruto − sin fruto (95 %) | partidas |
|---|---|---|---|---|---|
| abundancia | RG69r+voz | 5.48 | 6.53 | -1.05 [-1.37, -0.74] | 40 |
| abundancia | S69+voz | 5.11 | 6.28 | -1.17 [-1.64, -0.71] | 40 |
| abundancia | P69+voz | 5.76 | 6.29 | -0.53 [-0.88, -0.18] | 40 |
| normal | RG69r+voz | 4.89 | 5.53 | -0.64 [-0.97, -0.32] | 40 |
| normal | S69+voz | 4.26 | 5.33 | -1.07 [-1.42, -0.74] | 40 |
| normal | P69+voz | 4.90 | 5.32 | -0.42 [-0.69, -0.15] | 40 |
| sequía | RG69r+voz | 5.24 | 5.59 | -0.35 [-0.62, -0.07] | 40 |
| sequía | S69+voz | 4.33 | 5.06 | -0.73 [-1.09, -0.38] | 40 |
| sequía | P69+voz | 5.08 | 5.24 | -0.16 [-0.45, +0.13] | 40 |
| sequía dura | RG69r+voz | 4.40 | 4.28 | +0.12 [-0.13, +0.37] | 40 |
| sequía dura | S69+voz | 4.03 | 4.23 | -0.20 [-0.47, +0.06] | 40 |
| sequía dura | P69+voz | 4.35 | 4.21 | +0.14 [-0.07, +0.34] | 40 |
| bestias que crían | RG69r+voz | 5.26 | 5.25 | +0.01 [-0.31, +0.34] | 40 |
| bestias que crían | S69+voz | 4.20 | 4.86 | -0.67 [-0.96, -0.35] | 40 |
| bestias que crían | P69+voz | 4.84 | 5.12 | -0.28 [-0.53, -0.05] | 40 |

#### comida comida, por criatura y día

| mundo | jugador | días con fruto | días sin fruto | con fruto − sin fruto (95 %) | partidas |
|---|---|---|---|---|---|
| abundancia | RG69r+voz | 2.96 | 3.01 | -0.05 [-0.07, -0.03] | 40 |
| abundancia | S69+voz | 2.96 | 3.02 | -0.05 [-0.08, -0.03] | 40 |
| abundancia | P69+voz | 3.00 | 3.03 | -0.03 [-0.05, -0.00] | 40 |
| normal | RG69r+voz | 3.04 | 3.03 | +0.01 [-0.02, +0.03] | 40 |
| normal | S69+voz | 2.97 | 3.04 | -0.07 [-0.11, -0.03] | 40 |
| normal | P69+voz | 3.05 | 3.05 | +0.00 [-0.02, +0.03] | 40 |
| sequía | RG69r+voz | 3.08 | 3.02 | +0.05 [+0.01, +0.09] | 40 |
| sequía | S69+voz | 3.01 | 3.04 | -0.03 [-0.08, +0.02] | 40 |
| sequía | P69+voz | 3.10 | 3.03 | +0.07 [+0.03, +0.12] | 40 |
| sequía dura | RG69r+voz | 3.15 | 3.03 | +0.12 [+0.07, +0.17] | 40 |
| sequía dura | S69+voz | 3.09 | 3.08 | +0.01 [-0.07, +0.08] | 40 |
| sequía dura | P69+voz | 3.18 | 3.04 | +0.14 [+0.08, +0.20] | 40 |
| bestias que crían | RG69r+voz | 3.16 | 3.03 | +0.13 [+0.08, +0.18] | 40 |
| bestias que crían | S69+voz | 3.05 | 3.06 | -0.02 [-0.08, +0.05] | 40 |
| bestias que crían | P69+voz | 3.14 | 3.06 | +0.08 [+0.03, +0.13] | 40 |


## Parte 2: lo que la criatura sabe al nacer y lo que aprende

Esta parte la he leído yo, sin ayudantes, en el código con que se jugó RG69r+voz. Abreviaturas: «cv» es `cuerpo_valle.py`, «cfg» es `config_cuerpo_valle.json`, «cu» es `paper7/cuaderno_P7.py`, «A» es `paintball/alma/appraisal_zs_v42_exp.py`.

**Cómo lo he comprobado.** El programa nuevo `lee_criatura_161.py` hace dos cosas, sin jugar:
- resuelve los interruptores como el lanzador del v6 (`lanza_experimento_v6.py:33`, `lanzador.py:86`);
- prepara el mundo de la semilla 30161 sin dar ni un paso, como `banco_cuerpo_valle.py:36`, hace las dos hermanas de la casa A con la clase de RG69r+voz y vuelca lo que hay en su cuaderno antes de vivir nada.

La salida está en `salida/lee_criatura_161.json`. Lleva 95 interruptores encendidos y 7 apagados, entre ellos `imagina_v45`, `enfado` y `dormir_en_casa`. La clase es `cuerpo_vr1.RG69V`, que encadena la voz (`cuerpo_vc1.VC1`), la reserva (`cuerpo_rg69.RG69`) y la criatura de siempre.

### Lo que sabe al nacer sin haberlo vivido (lo heredado)

**1. El mapa entero.** El mundo le da al nacer el mapa público (`valle/mundo.py:125-134`):
- el terreno de cada casilla;
- las cuatro casas con sus celdas y su puerta;
- el almacén y desde dónde se coge;
- las 16 plantas y a qué huerto pertenece cada una;
- las puertas del valle.

El mapa trae también dónde está cada matorral (`mundo.py:134`), pero la criatura no lo usa. En `cv` no hay ninguna lectura de `M.matorrales`, y los matorrales los aprende viéndolos (`cv:740-752`).

**2. Las reglas públicas del mundo** (`mundo.py:133`, leídas en `cv:223`):

| regla | valor |
|---|---|
| golpe de la bestia | 40 |
| golpe de una criatura | 15 |
| la bestia roba la bolsa | sí |
| la bestia no entra en las casas | sí |
| la bestia cuenta como | 2 criaturas |
| temperatura cómoda | de 15 a 25 |
| harta por debajo de | hambre 15 |
| hambre por grado de frío | 0,05 |
| hambre por una noche fuera | 11,62 |
| llamadas | cuatro tipos; alcance 4, 7 o 10; cansancio 0, 0,15 o 0,3 |
| pasos de la bestia por turno | 1 |
| la medicina | cura 40 |

**3. Treinta y un recuerdos en su cuaderno, todos «heredados».** Cada uno pesa como una sola experiencia, de intensidad 1 (`cv:544`, por `radar_v39`). No se olvidan con los días (`cv:352` y `cu:60-61`, por `cultura_sin_olvido_v22`). Son estos, con su valor:

- **La cultura del valle** (`cultura_matorrales_medio.json`, cargada en `cv:541-552`). Son 11 frases y 17 recuerdos, porque algunas valen para varias situaciones:

| lo que dice | efecto (cuerpo · recursos · vínculo) y datos |
|---|---|
| una comida quita hambre | cuerpo 35 |
| la medicina cura | cuerpo 40 |
| la zona salvaje hiere, pero allí está la medicina (de día y de noche) | −0,05 · 0,5 · 0; da medicina 0,5 |
| en el bosque aparece comida (de día y de noche) | 0 · 0 · 0; da comida 0 |
| el huerto trabajado da fruto en unos dos días | recursos 0,15; cada 20 turnos de trabajo; 800 turnos de espera |
| la comida se conserva (almacén, despensa, bolsa y suelo) | dura: almacén sin límite, despensa 1.600 turnos, bolsa 800, suelo 150 |
| de noche viene la bestia | cuerpo −1,5; empieza en el turno 280 del día |
| la casa es segura de noche | 0 |
| dormida fuera, la bestia te pega | cuerpo −1,5 |
| los matorrales del bosque dan fruto, no dice dónde | recursos 0,5; 2,02 matorrales por cada 100 casillas |
| si llamas, la mitad de las veces viene alguien | viene 0,5 |

- **Los hechos de la bestia y de acompañar** (`cultura_hechos_v40.json`, `cv:572-579`). Son tres, en la situación «acompañada»:
  - la bestia ataca a una sola, a suertes (cuerpo 0,5);
  - un empujón lo gana el bando mayor (recursos 1);
  - empujar a la bestia sale bien con dos pegadas; si no, le pega 40 (cuerpo −40, recursos 1).
- **Echar y matar a la bestia** (`cultura_hechos_v44.json`, `cv:562-570`). Son dos hechos, con sus números guardados aparte en `hechos_g`:
  - echar: exponente 1,5; dos a la vez; 400 turnos lejos; golpe de 40;
  - matar: 150 de vida; se cura 2 por turno; golpe de 15; deja 24 comidas; vuelve otra a los 2.000 turnos.
- **El árbol dulce** (`cultura_hechos_v50.json`, `cv:554-561`). Son dos hechos, que no dicen dónde ni cuándo:
  - «a veces aparece un árbol de fruta dulce lejos»;
  - «al atardecer la bestia pasa por los árboles dulces».
- **Lo que vale cada cosa** (el «radar» al nacer, `cv:1783-1797`). Son siete recuerdos:
  - su hermana, «cerca»: cuerpo 0 y recursos 0 (con `radar_v38`, `cv:1791`);
  - su hermana, «trato»: vínculo 0,5 (cfg:`radar_v34.hermana_vinculo`);
  - las fuentes de comida: el almacén 0,24, las cajas 0,12 y las bayas 0,07 (A:147, `VALOR_NIVEL`);
  - guardar una medicina: recursos 0,18 (A:111, `ACOPIO_M`);
  - dar una medicina: vínculo 0,125 (A:369, `H_PREV` × 0,5);
  - dar una comida: vínculo 0,538, el alivio que imagina en una hermana flaca (`cv:1796`).

**4. Lo que no se aprende** (los números fijos de nacimiento):
- **El temperamento**, valiente o prudente (más abajo).
- **El valor de la otra por ser de su familia** (`cv:2043-2048`, cfg:8): la hermana 0,9864 y una vecina 0,3675.
  - En unidades de la fila del daño, la vida de la hermana vale 1,381 (`cv:2050-2052`).
- **El vínculo con la hermana empieza en 0,5**, el suelo de su escalón (`cv:532`, cfg:`vinculo.escalones.hermana`).
- **A una vecina no la conoce hasta que la ve.** Entonces nace con trato 0,125 (`cv:1799-1806`: 0,25 × 0,5).

### Lo que aprende viviendo

**La regla del cuaderno.** Casi todo lo que aprende va al cuaderno, y todo sigue la misma regla (`cu:1-20`):
- **Lo que cree de una cosa** es la media de lo que le hicieron sus recuerdos, pesada por el peso de cada uno.
- **El peso de un recuerdo vivido** es su intensidad × 0,95 por cada día que pasa (`cu:23` y `59-62`), así que pierde la mitad en unos 13,5 días.
- **La intensidad** va de 1 a 2. Sube con lo que le movió el malestar (`cu:99-104`).
- **Lo heredado pesa 1 y no se olvida.** Además hay un recuerdo «neutro», de efecto 0 y peso 1, que no se apaga (`cu:112-122`).
- **Cuánto tarda en cambiar lo que cree:**
  - una sola experiencia de intensidad 1 ya pesa un tercio de la creencia: neutro 1, heredado 1, vivido 1;
  - dos experiencias pesan la mitad, y diez cinco sextos;
  - al cabo de unos 14 días sin repetirla, lo vivido pesa la mitad y la creencia vuelve hacia lo heredado.
- **Lo que va sin el neutro** (`con_neutro=False`) son el radar, el trato y el sabor (`cv:1808-1811` y `2038-2041`). Allí lo vivido cuenta todavía más deprisa.
- **Los recuerdos de hace más de dos días se juntan en uno** (`cv:639`, `cu:35-57`). La creencia no cambia por eso.

**Lo que aprende, una por una:**

| lo que aprende | cómo lo apunta | dónde |
|---|---|---|
| cuánto le quita el hambre una comida, y cuánto le cura una medicina | al comer: lo que bajó el hambre o subió la vida. Si llegó a cero o al máximo, se apunta «al menos» | `cv:672-683` |
| qué le hace estar en cada sitio (salvaje, bosque, casa…), de día y de noche | la vida que pierde por turno y lo que encuentra allí | `cv:1398-1403` |
| qué le pasa de noche con la bestia | por cada noche fuera: la vida y la comida perdidas | `cv:1432-1436` |
| qué le pasa al dormir en casa o fuera | la vida que pierde dormida en cada sitio | `cv:1437-1440` |
| cuánto fruto da su trabajo en el huerto | los frutos que ve en la planta después, entre los turnos que trabajó; 0 si no salió | `cv:1442-1455` |
| dónde hay matorrales y plantas | cada uno que ve, con si tenía fruto; no se borra nunca | `cv:740-752` |
| si un matorral tiene fruto | por visita (recursos 1 o 0) y por cuánto tiempo hace que lo vio | `cv:744-752` |
| lo que le cuesta al cuerpo cada clase de acción (cansancio, hambre, vida) | media móvil con un peso de 0,2 por turno (cfg:133); nace sin saberlo | `cv:655-667` |
| lo que vale cada una de las otras | cada mirada (44 turnos): la vida que pierde y la comida que gana con ella al lado, frente a sin nadie | `cv:1832-1877` |
| el trato con cada una, que es su vínculo | cada mirada: la parte de la mirada en que la vio, más un cuarto por cada vez que se dieron algo, menos un cuarto por cada robo. Si no vio a la hermana en toda la mirada, se apunta 0 | `cv:1878-1889`; el vínculo es eso: `cv:1949-1952` |
| quién le roba | cada robo que sufre, con lo que perdió | `cv:1840-1846` |
| qué le pasa a la otra cuando le da algo | una mirada después: si se la ve mejor | `cv:1864-1865` y `1896-1905` |
| si guardar la medicina sirvió | cuando la usa | `cv:1923` |
| qué sabe la comida de cada sitio | al comerla | `cv:1918` |
| lo que ve hacer a las otras | los mismos apuntes, marcados como «visto» | `cv:1930` y `1947` |
| lo que siente de bueno (el hambre que quitó, la comida nueva, el alivio al dar) | no va al cuaderno: se queda en su estado y baja a la mitad cada 44 turnos | `cv:2282-2294` |

**De dónde le llega lo que aprende.** Nada de lo que aprende viene de una recompensa ni de una nota de alguien de fuera.
- El mundo no da puntos: la recompensa es siempre 0 (`mundo.py:3` y `720`), y la criatura no lee ninguna.
- Todo lo que apunta sale de:
  - su propio cuerpo: hambre, vida y cansancio;
  - lo que ve: frutos, las otras, la bestia, los empujones;
  - lo que oye de las otras dentro del mundo: las llamadas y la voz de ir a casa.
- **La voz** es de la hermana, que está en el mundo. No enseña nada: mientras dura, solo cambia dónde se imagina a la hermana en la foto, que pasa a estar en casa (`cuerpo_vc1.py:1-21`).
- **Lo único que viene de fuera es lo heredado del punto 3.** Se lo da quien la diseña, al nacer, y después ya no le llega nada más.

### El temperamento

- **Cómo se reparte:**
  - la hermana 1 de cada casa (A1, B1, C1 y D1) es valiente, con 0,5;
  - la hermana 2 (A2, B2, C2 y D2) es prudente, con 1,5;
  - el reparto es por el número del nombre (`cv:222`, cfg:85-88); en las ocho queda cuatro y cuatro.
- **Qué multiplica exactamente.** Multiplica nueve filas del miedo, cuando están en la foto (`cv:1740-1741`, la lista en `paper7/miedo_P7_49.py:16`):
  - F-ANTICIPACION (la regla general la quita después, `cv:2189`, así que no cuenta);
  - F-4-ALCANCE, el peligro de la bestia cerca;
  - F-REENCUENTRO;
  - MIEDO_APRENDIDO;
  - F-HERMANO-AMENAZA, la hermana en peligro;
  - S-8-EXPOSICION;
  - S-7-AGRESOR;
  - R-ACOPIO, no llevar medicina;
  - S-COMPANIA, estar lejos de la hermana.
- **Dónde se aplica.** Se aplica en `_filas_orig` (`cv:1609`), antes de que la regla general añada lo suyo (`cv:2188`). Por eso las ganancias «G-…» de esas mismas filas, que son lo que la foto alivia (`cv:2229-2237`), también llevan el multiplicador.
- **Lo que no toca:** el hambre, el daño, el cansancio, el frío, la carencia de comida, la soledad, el duelo ni el «vivir bien».

### Los dos pesos de familia: de dónde salen 0,9864 y 0,3675

- **Salen de medir otra criatura más antigua, RG32r** (cfg:8, prompt 84, Manel). El programa es `pesos_rg32r.py`; la salida, `salida/pesos_rg32r.json`.
- **Cómo se midieron:**
  - cuatro partidas de 40 días: sequía y normal, semillas 1001 y 1002;
  - al empezar cada día, el vínculo de cada criatura viva con su hermana viva (B) y con cada vecina que conocía.
- **Lo que salió:**
  - la media de B fue 0,98640, con 1.198 muestras y cuartiles 1, 1 y 1;
  - la de las vecinas fue 0,36754, con 7.190 muestras y cuartiles 0,31, 0,39 y 0,43.
- **Para qué sirven.** Son el valor de la otra «por ser familia», que no se aprende (`cv:2043-2048`).
  - Sustituyen a los números de antes (cfg:`radar_v34`): la hermana, la mitad de la propia vida; una vecina, un cuarto de eso.
  - Pesan donde pesaba la familia: el valor de su vida (`cv:2050-2052`) y el peso de la otra al darle algo, que es la familia × lo que vale ahora en su radar frente a lo que valía al nacer (`cv:2058-2060`).

### La curiosidad que queda: lo que le falta saber de dónde hay comida

La fila es R-CURIOSIDAD-FRONTERA. La regla general quita las otras dos curiosidades (`cv:2189`).

- **Qué mide.** Una pérdida que crece cuanto más lejos imagina estar de una casilla que nunca ha visto (`cv:796-800`):
  - 0,2 (cfg:147, `curiosidad_frontera.k`);
  - × (1 − la amenaza);
  - × (1 − g(los pasos hasta lo no visto));
  - × lo que le falta saber.
- **Las piezas de la fórmula:**
  - **g** es la caída cúbica de `paper5/curiosidad.py:167-175`: (1 − pasos/24)³;
  - **lo que le falta saber** es 1 − los matorrales que ya ha visto entre los que la cultura dice que hay en el bosque (`cv:2316-2320` y `2199-2200`);
  - **los que dice la cultura** son 2,02 por 100 casillas × 992 casillas de bosque, unos 20.
- **Un detalle de la cuenta.** «Los que ha visto» cuenta todo lo que tiene en su lista de matorrales: también las 16 plantas del huerto y los matorrales salvajes (`cv:741`).
- **Cuánto pesa.**
  - Vale como mucho 0,2.
  - Al nacer, lo que le falta saber es 1 (lo confirma `lee_criatura_161.py`).
  - Se reparte 0,1 · 0,8 · 0,1, casi todo en recursos (`paper5/curiosidad.py:49`).
  - Es una pérdida, no una ganancia (`cv:36`).
- **Qué la apaga:**
  - haber visto tantos matorrales como la cultura dice que hay, unos 20 contando las plantas;
  - la amenaza: la bestia pegada, o 25 de vida perdidos en los últimos 9 turnos (`cv:782-794`; cfg:147 `ventana_dano_turnos`);
  - no quedar ninguna casilla sin ver a la que se pueda llegar (`cv:797-798`);
  - en la foto, estar ya pegada a lo no visto: con 0 pasos, g = 1 y la fila vale 0.

## Parte 3: las vivas del v6 (figura `figuras/v6_A_vivas`)

Usa la pieza sellada `cierre_v46`, a través de `evalua_experimento_v6.c46`: vivas el día 40 = 8 menos las muertes que apunta `fin.json`. Es la medida sellada de vivas, repetida tal cual. Lo nuevo es solo la figura. Cada valor es la media de 40 semillas, con su intervalo del 95 %.

| mundo | el tonto | el recolector | RG68r | RG068r | RG69r+voz |
|---|---|---|---|---|---|
| abundancia | 8,00 | 7,97 | 8,00 | 7,97 | 8,00 |
| normal | 8,00 | 7,97 | 7,92 | 7,78 | 8,00 |
| sequía | 5,12 [4,88, 5,38] | 7,97 | 7,45 [7,25, 7,65] | 7,67 [7,50, 7,83] | 7,80 [7,67, 7,92] |
| sequía dura | 1,55 [1,27, 1,82] | 3,42 [3,15, 3,67] | 4,03 [3,75, 4,28] | 4,12 [3,83, 4,42] | 4,22 [3,95, 4,50] |
| bestias que crían | 3,50 [2,98, 4,03] | 5,55 [5,08, 6,05] | 6,28 [5,95, 6,60] | 6,50 [6,10, 6,88] | 6,65 [6,35, 6,95] |

Las vivas de RG69r+voz son exactamente las de la figura sellada de la escalera (`salida/figuras_escalera_paper8.json`).

## Parte 4: las dos costumbres (figura `figuras/v6_B_costumbres`)

Hay tres jugadores: la criatura de antes (RG68r), con la reserva (RG69r) y con la reserva y la voz (RG69r+voz). Cada valor es la media de 40 semillas, con su intervalo del 95 %.

**Panel 1: turnos al día con hambre > 30 y comida en la bolsa, días 0 a 9.**
- Es la medida sellada de P24 y P29, sacada con la misma pieza: `evalua_experimento_v6.nuevas`, que llama a `extrae_hg_v1`.
- Repite lo sellado. Con la sequía y la sequía dura juntas sale RG68r 31,97, RG69r 3,75 y RG69r+voz 2,98, los mismos números de `salida/evalua_experimento_v6.md:95` y `105`.

| mundo | RG68r | RG69r | RG69r+voz |
|---|---|---|---|
| abundancia | 14,0 | 2,4 | 1,9 |
| normal | 29,8 | 3,4 | 3,6 |
| sequía | 18,7 | 2,8 | 2,0 |
| sequía dura | 45,3 | 4,7 | 3,9 |
| bestias que crían | 40,6 | 4,1 | 4,3 |

**Panel 2: noches dormidas fuera, días 0 a 9, en %.**
- Es la medida de P28, con la misma pieza (`analiza_vc1`, «noches10»).
- La sellada suma todas las noches de las 80 partidas de las dos sequías. Aquí va por partida (las noches fuera entre las noches de cada partida), para poder dar el intervalo. Lo simple, y lo dejo dicho.
- Con las dos sequías juntas sale RG69r+voz 7,0 % y RG69r 24,2 %, como en lo sellado.

| mundo | RG68r | RG69r | RG69r+voz |
|---|---|---|---|
| abundancia | 20,8 | 22,3 | 4,7 |
| normal | 23,1 | 23,3 | 6,5 |
| sequía | 21,8 | 22,7 | 6,0 |
| sequía dura | 24,6 | 25,6 | 8,1 |
| bestias que crían | 22,7 | 26,8 | 7,7 |

**Panel 3: golpes de la bestia recibidos estando dormida, por partida.**
- Es medida nueva, hecha después. Cuenta los sucesos «bestia_pega» con motivo «dormida» (`valle/mundo.py:1032-1033`), contados en el prompt 160.

| mundo | RG68r | RG69r | RG69r+voz |
|---|---|---|---|
| abundancia | 3,90 [3,10, 4,72] | 4,22 | 0,40 [0,25, 0,57] |
| normal | 3,02 | 3,38 | 0,80 |
| sequía | 2,88 | 3,10 | 1,07 |
| sequía dura | 1,95 | 2,02 | 1,15 |
| bestias que crían | 3,27 | 3,40 | 1,43 |

Los intervalos de todas las celdas están en `salida/figuras_v6_161.json`.

## Parte 5: el duelo y la soledad (figura `figuras/v6_C_duelo_soledad`)

**Las definiciones** son las de la medida sellada A4, importadas de `duelo_soledad_v6.py` (`casos_de`, `her` y las mismas reglas de los controles):
- **duelo** = S-DUELO-CUERPO + S-DUELO-RECURSOS + S-DUELO-VINCULO;
- **soledad** = S-SOLEDAD.

Las dos son la media de los turnos despierta de cada día.

**Los casos que entran:**
- **136 casos**, en 73 partidas: 8 en la sequía, 95 en la sequía dura y 33 en las bestias que crían. En la abundancia y el normal no hay ninguno.
- **378 controles**: las de otra casa de la misma partida que conservan a su hermana, en los mismos días.
- **Comprobación:** son los mismos números que da la salida sellada (`salida/duelo_soledad_v6.json`: 136, 378 y 73).
- **Lo que mira la figura** es nuevo: el trazo día a día, del día −5 al +15. La medida sellada daba resúmenes.
- **Los que quedan con el tiempo.** Hacia el final quedan menos, porque algunas mueren o se acaba la partida. El día +15 quedan 109 casos y 254 controles; la cuenta de cada día está en el JSON.

**Lo que se ve:**
- **El duelo** de la que pierde a su hermana pasa de casi 0 a 1,64 el día después. Baja a la mitad hacia el día +5 y se queda en unos 0,8 hasta el día +15.
- **El duelo de los controles** sube a 0,24 el día después, porque también ha muerto una vecina, y se queda en unos 0,17.
- **La soledad** de la que pierde a su hermana sube de 0,03 a 0,43-0,45 y casi no baja: el día +15 está en 0,39.
- **La soledad de los controles** se queda en 0,01-0,02.

## Parte 6: un día en el valle (figura `figuras/v6_D_un_dia`)

- **La partida:** mundo normal, semilla 30161, RG69r+voz.
- **Los días:** el 5 y el 6, contados desde el 1; son los turnos 1.600 a 2.399. El 5 es día de fruto. No he cambiado ni la partida ni los días.
- **Las filas:** una por criatura, con las hermanas juntas y una raya entre casas.
- **Lo que hace.** Es la acción que apunta el mundo en cada turno, haya salido bien o no. Si está dormida, cuenta como dormir.
  - Hay un color para «otra» (dejar, golpear, llamar, hablar), porque esas acciones también existen. Es lo simple y lo dejo dicho.
- **Dónde está.** Es el terreno de su casilla. He añadido «otro sitio» para el camino, el almacén y las puertas, que no estaban en la lista. También es lo simple.
- **El fondo:** el anochecer, claro, y la noche, oscuro, según la fase del registro.
- **En esos dos días no muere ninguna.**
- **Lo que se ve, sin interpretarlo:**
  - por la noche duermen en casa todas menos B1, que la noche del día 5 duerme en el bosque;
  - en el día 6, sin fruto, hay más trabajo en el huerto por la mañana (A1, A2, B1 y C2);
  - las mañanas empiezan con muchos cambios cortos: coger, comer y algún empujón.

## Parte 7: cierre

**Qué es análisis hecho después y qué repite lo sellado.**
- Las partes 1, 3, 4, 5 y 6 son análisis hecho después de ver los datos. No hay predicciones ni causas.
- Repiten una medida sellada:
  - la parte 3 (las vivas);
  - los paneles 1 y 2 de la parte 4 (P24 y P29, y P28);
  - en la parte 5, la elección de casos y controles y las definiciones de A4.
- Lo demás es nuevo:
  - toda la parte 1;
  - el panel 3 de la parte 4;
  - el trazo día a día de la parte 5;
  - la figura de la parte 6.

**Lo hecho.** Siete partes y cuatro figuras, en PNG y PDF.
- Los programas nuevos, todos de solo lectura:
  - `dias_cosecha_161.py`, para la parte 1;
  - `lee_criatura_161.py`, para la parte 2: prepara el mundo sin dar ni un paso y hace las dos hermanas de la casa A, sin jugar;
  - `figuras_v6_161.py`, para las partes 3 a 6.
- Las salidas:
  - `salida/dias_cosecha_161.md` y `.json`;
  - `salida/lee_criatura_161.json`;
  - `salida/figuras_v6_161.json`.
- No se ha jugado ninguna partida, no se ha tocado nada sellado y no se ha usado la clave.

**Lo que no se ha podido.** Nada de lo pedido ha quedado sin hacer. Hay dos cosas que conviene saber:
- **En la parte 2**, «el valor de una vecina al nacer» no existe hasta que la ve: la criatura no conoce a las vecinas hasta verlas.
- **En la parte 6**, la lista de sitios del prompt no cubría el camino, el almacén ni las puertas, y he añadido «otro sitio».

**Los tropiezos:**
- **Las figuras se colgaron dos veces.** El programa importa `reserva_v1/gif_rg69.py` (para los colores del mapa), y ese importa `reserva_v1/analiza_rg69.py`, que al cargarse cambia la carpeta de RG69r a la del taller (`valle_rg69_taller`, `analiza_rg69.py:26`).
  - Las partidas de RG69r con las semillas del v6 no están en el taller. La pieza paraba con «partida sin acabar», el proceso de trabajo moría sin avisar y el conjunto se quedaba esperando.
  - Lo arreglé sin tocar ese fichero: después de los imports, `figuras_v6_161.py` devuelve las carpetas a las del experimento y lo comprueba con un assert.
  - La pasada mala no escribió ninguna cuenta de RG69r: la pieza para antes de escribir.
  - Sí escribió, en la caché de la escalera (`evalua_escalera_v6/experimento/datos`), cuentas de RG68r y otras sacadas de las partidas selladas, que son las buenas. No he borrado nada.
  - Los resultados finales cuadran con lo sellado (partes 3 a 5).
- **Una ruta personal.** La primera versión de `lee_criatura_161.py` escribía la ruta entera de la cultura en su JSON, y la cambié por una relativa.
- **Comandos sueltos:**
  - cuatro lecturas cortas con `python3 -I` en la terminal, que solo leen ficheros JSON;
  - dos ediciones de mis propios programas con un `python3` en la terminal;
  - un programa de prueba en el scratchpad (`prueba_fig161.py`), que solo lee.

**Las citas que he comprobado yo.** Las de la parte 2 las he leído yo en el código, todas:
- `cv:222`, `352`, `532`, `541-579`, `655-683`, `740-752`, `760-800`, `1398-1455`, `1609`, `1740-1741`, `1783-1811`, `1832-1889`, `1896-1952`, `2038-2066`, `2186-2237` y `2282-2320`;
- `cu` entero;
- `cuerpo_vc1.py`, `cuerpo_rg69.py` y `cuerpo_vr1.py` enteros;
- `paper7/miedo_P7_49.py:16`, `paper5/curiosidad.py:49` y `167-175`;
- en la configuración: cfg:8, 11, 85-88, 133, 147 y 159;
- `pesos_rg32r.py` y su salida;
- `valle/mundo.py:3`, `125-134`, `720` y `1032-1033`.

Los valores de lo heredado están comprobados además haciendo las criaturas de verdad (`lee_criatura_161.py`).

Las citas que no he comprobado:
- las que vienen de informes anteriores, como el ciclo del huerto del 157 y las comprobaciones del 160;
- `A:111`, `147` y `369`: solo he leído esas líneas, no su historia.

**Gasto:** 0 créditos de la plataforma y 0 dólares de la consola de Anthropic. No he leído los saldos.
