Partidas: 320; semillas 2001–2040 (40). Muestra: 2000 decisiones por clase y mundo. Intervalos del 95 % por bootstrap, 10000 remuestreos, semilla 8.

## Cuánto deciden igual (la opción elegida frente a la que elegiría cada valorador en el mismo estado)

| clase | mundo | n | con el motor | con las sumas | con la posición | sin ambivalencia medida |
|---|---|---|---|---|---|---|
| RG32r | bestia_dia | 2000 | 100.0 % | 85.2 % | 92.0 % | 0 |
| S32 | bestia_dia | 2000 | 79.1 % | 100.0 % | 78.5 % | 0 |
| P32 | bestia_dia | 2000 | 94.7 % | 87.1 % | 100.0 % | 0 |
| RG032r | bestia_dia | 2000 | 100.0 % | 96.8 % | 96.0 % | 0 |
| S032 | bestia_dia | 2000 | 94.5 % | 100.0 % | 90.3 % | 0 |
| RG32r | sequia_dura | 2000 | 100.0 % | 87.2 % | 90.6 % | 0 |
| S32 | sequia_dura | 2000 | 81.7 % | 100.0 % | 82.8 % | 0 |
| P32 | sequia_dura | 2000 | 93.5 % | 86.8 % | 100.0 % | 1 |

Por situación (con la situación / sin ella, % igual con su gemela; n con ella):

| clase (gemela) | mundo | hambre | bestia | hermana | noche |
|---|---|---|---|---|---|
| RG32r (sumas) | bestia_dia | 66.0 / 86.7 (147) | 58.3 / 85.5 (24) | 87.5 / 75.1 (1614) | 87.2 / 83.2 (964) |
| RG32r (posicion) | bestia_dia | 88.4 / 92.3 (147) | 87.5 / 92.1 (24) | 92.8 / 88.9 (1614) | 92.6 / 91.4 (964) |
| S32 (motor) | bestia_dia | 74.3 / 79.4 (113) | 82.6 / 79.1 (23) | 79.2 / 78.9 (1735) | 81.4 / 77.5 (843) |
| P32 (motor) | bestia_dia | 89.9 / 95.1 (159) | 93.8 / 94.7 (16) | 94.3 / 95.9 (1538) | 94.9 / 94.5 (920) |
| RG032r (sumas) | bestia_dia | 100.0 / 96.7 (37) | 100.0 / 96.7 (26) | 97.6 / 94.6 (1424) | 98.5 / 94.9 (1026) |
| S032 (motor) | bestia_dia | 93.0 / 94.5 (43) | 93.1 / 94.5 (29) | 95.2 / 92.1 (1517) | 96.6 / 92.4 (992) |
| RG32r (sumas) | sequia_dura | 76.6 / 88.4 (192) | 100.0 / 87.2 (2) | 89.2 / 83.2 (1350) | 88.9 / 85.8 (933) |
| RG32r (posicion) | sequia_dura | 88.0 / 90.9 (192) | 100.0 / 90.6 (2) | 92.6 / 86.6 (1350) | 90.8 / 90.5 (933) |
| S32 (motor) | sequia_dura | 70.2 / 82.8 (178) | — / 81.7 (0) | 79.2 / 87.7 (1423) | 83.5 / 80.3 (850) |
| P32 (motor) | sequia_dura | 83.9 / 94.7 (223) | 100.0 / 93.4 (1) | 94.0 / 92.3 (1390) | 93.6 / 93.4 (886) |

## Por cuartos de ambivalencia del estado (cuartos dentro de cada clase y mundo; % igual)

| clase (valorador) | mundo | Q1 (menos) | Q2 | Q3 | Q4 (más) | cortes |
|---|---|---|---|---|---|---|
| RG32r (sumas) | bestia_dia | 93.2 | 85.2 | 82.6 | 79.6 | [0.582, 0.673, 0.768] |
| RG32r (posicion) | bestia_dia | 94.6 | 91.2 | 92.2 | 90.0 | [0.582, 0.673, 0.768] |
| S32 (motor) | bestia_dia | 86.6 | 79.8 | 72.8 | 77.4 | [0.581, 0.673, 0.767] |
| P32 (motor) | bestia_dia | 96.0 | 94.8 | 94.8 | 93.2 | [0.581, 0.68, 0.783] |
| RG032r (sumas) | bestia_dia | — | — | — | 96.8 | [0.0, 0.0, 0.0] |
| S032 (motor) | bestia_dia | — | — | — | 94.5 | [0.0, 0.0, 0.0] |
| RG32r (sumas) | sequia_dura | 93.0 | 89.6 | 86.4 | 80.0 | [0.555, 0.67, 0.775] |
| RG32r (posicion) | sequia_dura | 95.6 | 91.4 | 89.8 | 85.8 | [0.555, 0.67, 0.775] |
| S32 (motor) | sequia_dura | 85.6 | 79.8 | 79.6 | 81.6 | [0.568, 0.676, 0.781] |
| P32 (motor) | sequia_dura | 94.0 | 94.0 | 93.2 | 92.6 | [0.555, 0.664, 0.785] |

## Las predicciones

**C1.** En bestia de día, RG32r vive más que S32. Vivas RG32r − S32: +0.30 [-0.05, +0.65] (n=40) → **no se cumple**

**C2.** RG32r pasa menos turnos con el hambre al máximo que S32, en bestia de día. Por 1.000 turnos vivos, RG32r − S32: -1.72 [-2.32, -1.14] (n=40) → **se cumple**

**C3.** Motor y sumas coinciden menos con ganancias que sin ellas (bestia de día). Coincidencia RG32r–S32 menos RG032r–S032: -0.116 [-0.135, -0.097] (n=40) → **se cumple**

**C4.** En bestia de día, RG32r vive más que P32. Vivas RG32r − P32: +0.05 [-0.28, +0.38] (n=40) → **no se cumple**

**C5.** RG32r y S32 coinciden menos en el cuarto más ambivalente que en el menos ambivalente. Q4 − Q1 (estados de RG32r, por partida):
  - bestia_dia: -0.136 [-0.174, -0.097] (n=40) → **se cumple**
  - sequia_dura: -0.130 [-0.168, -0.090] (n=40) → **se cumple**
  - los dos mundos juntos: -0.133 [-0.160, -0.106] (n=80) → **se cumple**

**C6.** RG32r y P32 coinciden menos en el cuarto más ambivalente que en el menos ambivalente. Q4 − Q1 (estados de RG32r, por partida):
  - bestia_dia: -0.046 [-0.076, -0.015] (n=40) → **se cumple**
  - sequia_dura: -0.098 [-0.133, -0.063] (n=40) → **se cumple**
  - los dos mundos juntos: -0.072 [-0.095, -0.048] (n=80) → **se cumple**

**Sequía dura** (sin predicción; se informa). Vivas al final:
  - RG32r: 3.70
  - S32: 3.08
  - P32: 3.50
  - RG32r − S32: +0.62 [+0.15, +1.07] (n=40)
  - RG32r − P32: +0.20 [-0.17, +0.57] (n=40)
  - S32 − P32: -0.42 [-0.78, -0.07] (n=40)

Vivas y hambre al máximo, todas las clases:

| clase | mundo | vivas | hambre al máximo por 1.000 | muertes de hambre / bestia / otras |
|---|---|---|---|---|
| RG32r | bestia_dia | 7.30 | 1.20 | 8 / 19 / 1 |
| S32 | bestia_dia | 7.00 | 2.92 | 21 / 18 / 1 |
| P32 | bestia_dia | 7.25 | 1.72 | 8 / 21 / 1 |
| RG032r | bestia_dia | 7.50 | 0.87 | 8 / 12 / 0 |
| S032 | bestia_dia | 7.42 | 0.85 | 7 / 15 / 1 |
| RG32r | sequia_dura | 3.70 | 14.71 | 158 / 12 / 2 |
| S32 | sequia_dura | 3.08 | 18.07 | 174 / 21 / 2 |
| P32 | sequia_dura | 3.50 | 15.74 | 169 / 8 / 3 |

## Exploración (añadido de Manel, no es predicción): cuántas dimensiones en conflicto a la vez

En conflicto: su ambivalencia por encima de la mediana de esa dimensión en la muestra de la clase y el mundo.

| clase (valorador) | mundo | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|
| RG32r (sumas) | bestia_dia | 91.1 (473) | 85.3 (476) | 82.0 (633) | 83.0 (418) |
| RG32r (posicion) | bestia_dia | 94.5 (473) | 92.0 (476) | 91.9 (633) | 89.2 (418) |
| S32 (motor) | bestia_dia | 91.0 (413) | 78.6 (566) | 73.8 (633) | 76.0 (388) |
| P32 (motor) | bestia_dia | 96.4 (445) | 95.0 (519) | 95.4 (631) | 91.4 (405) |
| RG032r (sumas) | bestia_dia | 96.7 (1953) | 100.0 (44) | 100.0 (3) | — (0) |
| S032 (motor) | bestia_dia | 94.5 (1967) | 93.8 (32) | 100.0 (1) | — (0) |
| RG32r (sumas) | sequia_dura | 92.5 (468) | 88.5 (460) | 85.8 (681) | 82.1 (391) |
| RG32r (posicion) | sequia_dura | 95.1 (468) | 90.7 (460) | 89.1 (681) | 88.0 (391) |
| S32 (motor) | sequia_dura | 91.3 (427) | 80.9 (477) | 77.9 (768) | 79.0 (328) |
| P32 (motor) | sequia_dura | 94.0 (463) | 92.7 (478) | 94.0 (655) | 92.8 (403) |

Con 2 o 3 dimensiones en conflicto, la que prioriza la opción elegida (la dimensión en conflicto que más queda por encima de la media de las opciones). La criatura (lo que eligió) y, en sus mismos estados, lo que elegiría cada valorador; n = estados con 2 o 3 en conflicto:

| clase | mundo | n | quién elige | F | R | S |
|---|---|---|---|---|---|---|
| RG32r | bestia_dia | 1051 | la criatura | 33.1 % | 18.7 % | 48.1 % |
| RG32r | bestia_dia | 1051 | motor | 33.1 % | 18.7 % | 48.1 % |
| RG32r | bestia_dia | 1051 | sumas | 35.3 % | 16.3 % | 48.4 % |
| RG32r | bestia_dia | 1051 | posición | 32.4 % | 21.7 % | 45.9 % |
| S32 | bestia_dia | 1021 | la criatura | 27.5 % | 16.5 % | 56.0 % |
| S32 | bestia_dia | 1021 | motor | 33.7 % | 26.1 % | 40.3 % |
| S32 | bestia_dia | 1021 | sumas | 27.5 % | 16.5 % | 56.0 % |
| S32 | bestia_dia | 1021 | posición | 32.8 % | 27.7 % | 39.5 % |
| P32 | bestia_dia | 1036 | la criatura | 31.4 % | 20.0 % | 48.6 % |
| P32 | bestia_dia | 1036 | motor | 32.5 % | 19.6 % | 47.9 % |
| P32 | bestia_dia | 1036 | sumas | 34.7 % | 16.5 % | 48.7 % |
| P32 | bestia_dia | 1036 | posición | 31.4 % | 20.0 % | 48.6 % |
| RG032r | bestia_dia | 3 | la criatura | 33.3 % | 66.7 % | 0.0 % |
| RG032r | bestia_dia | 3 | motor | 33.3 % | 66.7 % | 0.0 % |
| RG032r | bestia_dia | 3 | sumas | 33.3 % | 66.7 % | 0.0 % |
| RG032r | bestia_dia | 3 | posición | 33.3 % | 66.7 % | 0.0 % |
| S032 | bestia_dia | 1 | la criatura | 0.0 % | 100.0 % | 0.0 % |
| S032 | bestia_dia | 1 | motor | 0.0 % | 100.0 % | 0.0 % |
| S032 | bestia_dia | 1 | sumas | 0.0 % | 100.0 % | 0.0 % |
| S032 | bestia_dia | 1 | posición | 0.0 % | 100.0 % | 0.0 % |
| RG32r | sequia_dura | 1072 | la criatura | 29.4 % | 16.4 % | 54.2 % |
| RG32r | sequia_dura | 1072 | motor | 29.4 % | 16.4 % | 54.2 % |
| RG32r | sequia_dura | 1072 | sumas | 33.0 % | 15.9 % | 51.1 % |
| RG32r | sequia_dura | 1072 | posición | 29.5 % | 20.6 % | 49.9 % |
| S32 | sequia_dura | 1096 | la criatura | 27.6 % | 14.1 % | 58.3 % |
| S32 | sequia_dura | 1096 | motor | 33.7 % | 21.8 % | 44.5 % |
| S32 | sequia_dura | 1096 | sumas | 27.6 % | 14.1 % | 58.3 % |
| S32 | sequia_dura | 1096 | posición | 31.8 % | 24.5 % | 43.7 % |
| P32 | sequia_dura | 1058 | la criatura | 29.4 % | 17.2 % | 53.4 % |
| P32 | sequia_dura | 1058 | motor | 31.5 % | 16.4 % | 52.1 % |
| P32 | sequia_dura | 1058 | sumas | 33.1 % | 15.2 % | 51.7 % |
| P32 | sequia_dura | 1058 | posición | 29.4 % | 17.2 % | 53.4 % |
