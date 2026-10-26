# P7-55 · Banco (coste cero): ¿cuánto aprende cada hermana de la otra? Sobre los cuadernos de P7-50

*13-oct-2026. Sobre los 120 cuadernos por día de COMPARTE y los 120 de SOLAS (P7_50_res). `analiza_P7_55.py` → `P7_55_datos.json`; `escribe_informe_P7_55.py` (este informe; ninguna cifra a mano).
Creencia = la del cuerpo (dentro; sin cortes; neutro de peso 1; «al menos» solo si sube; olvido 0,95 por día), recalculada del cuaderno. `motor/model.py` intacto. Plataforma 0; consola 0 $.*

## 1 · Fusión por evento

En cada cuaderno se quita la segunda copia de los «vistos» que llegaron también contados por la hermana (mismo objeto, mismo día de origen, |tic| ≤ 240): en los cuadernos del día 20 de las
seis hermanas de COMPARTE, 43 vistos quitados (los 43 usos contados dos veces de P7-53, vistos desde cada cuaderno). La creencia (c) sin deduplicar frente a (a) deduplicada mide lo que esa doble cuenta
cambió de verdad en lo que el cuerpo creyó: en la tabla, (c) y (a) al día 20.

## 2 y 3 · Lo que cree cada hermana y cuánto viene de la otra

| serie · hermana | objeto | creencia d20: (a) todos dedup · (b) solo vividos · (c) todos sin dedup | aprendido de la otra (a − b), media d1-20 | fracción de lo creído que viene de la otra | recuerdos al d20: vividos · recibidos | área d1-20: (a) · (b) |
|---|---|---|---:|---:|---|---|
| s1 a10 valiente | botiquin | 40,9 · 24,1 · 40,9 | 7,20 | 19 % | 14 · 11 | 633 · 489 |
| s1 a10 valiente | racion | 14,3 · 13,3 · 14,3 | 1,15 | 9 % | 23 · 25 | 255 · 232 |
| s1 a10 valiente | red | 0,0 · 0,0 · 0,0 | 0,00 | — | 7 · 10 | 0 · 0 |
| s1 a10 valiente | camuflaje | 2,9 · 0,0 · 2,5 | 0,90 | 100 % | 7 · 17 | 18 · 0 |
| s1 a11 prudente | botiquin | 40,9 · 43,2 · 40,9 | 4,00 | 33 % | 11 · 14 | 633 · 553 |
| s1 a11 prudente | racion | 14,3 · 14,4 · 14,3 | 1,17 | 15 % | 25 · 23 | 254 · 230 |
| s1 a11 prudente | red | 0,0 · 0,0 · 0,0 | 0,00 | — | 10 · 7 | 0 · 0 |
| s1 a11 prudente | camuflaje | 2,9 · 3,6 · 2,9 | -0,28 | 31 % | 16 · 7 | 18 · 24 |
| s2 a10 valiente | botiquin | 39,2 · 20,4 · 39,2 | 5,70 | 46 % | 14 · 13 | 664 · 550 |
| s2 a10 valiente | racion | 14,2 · 13,8 · 14,2 | 0,21 | 2 % | 23 · 12 | 270 · 265 |
| s2 a10 valiente | red | 3,1 · 0,0 · 3,1 | 0,95 | 100 % | 10 · 9 | 19 · 0 |
| s2 a10 valiente | camuflaje | 0,5 · 0,0 · 0,5 | 0,37 | 100 % | 2 · 17 | 7 · 0 |
| s2 a11 prudente | botiquin | 39,2 · 34,7 · 39,2 | 7,25 | 27 % | 13 · 14 | 638 · 493 |
| s2 a11 prudente | racion | 14,2 · 13,1 · 14,2 | 5,65 | 44 % | 12 · 23 | 269 · 156 |
| s2 a11 prudente | red | 3,0 · 6,8 · 3,0 | -0,92 | 84 % | 9 · 10 | 23 · 42 |
| s2 a11 prudente | camuflaje | 0,5 · 0,5 · 0,5 | -0,06 | 15 % | 15 · 2 | 7 · 9 |
| s3 a10 valiente | botiquin | 45,8 · 37,3 · 45,8 | 6,49 | 18 % | 14 · 18 | 796 · 666 |
| s3 a10 valiente | racion | 11,4 · 10,0 · 11,4 | 1,76 | 15 % | 29 · 26 | 246 · 211 |
| s3 a10 valiente | red | 0,0 · 0,0 · 0,0 | 0,00 | — | 7 · 9 | 0 · 0 |
| s3 a10 valiente | camuflaje | 0,0 · 0,0 · 0,0 | 0,00 | — | 9 · 8 | 0 · 0 |
| s3 a11 prudente | botiquin | 45,8 · 44,9 · 45,8 | 2,32 | 8 % | 18 · 14 | 822 · 776 |
| s3 a11 prudente | racion | 11,4 · 13,3 · 11,4 | -0,28 | 11 % | 26 · 29 | 247 · 253 |
| s3 a11 prudente | red | 0,0 · 0,0 · 0,0 | 0,00 | — | 9 · 7 | 0 · 0 |
| s3 a11 prudente | camuflaje | 0,0 · 0,0 · 0,0 | 0,00 | — | 7 · 9 | 0 · 0 |

- **Con los mismos recuerdos deduplicados, las dos hermanas creen exactamente lo mismo al d20** (columna (a), misma cifra en 10 y 11): el canal y la noche igualan los cuadernos.
- **Cuánto viene de la otra** (botiquín): valientes 19 %, 46 %, 18 % (media 28 %); prudentes 33 %, 27 %, 8 % (media 22 %). La que más aprende de la otra es la que menos
  vivió por sí misma: la valiente de la serie 2 (b 20,4 → a 39,2). En la ración, 2 %-44 %; en red y camuflaje lo recibido es a veces todo lo que hay (sin vividos propios).
- **¿Alguna vez lo recibido la llevó a creer algo falso?** 0 veces en 120 hermana-días (criterio: red o camuflaje con creencia > 5 cuando lo vivido decía ≤ 5; botiquín o ración ≤ 0 cuando lo vivido decía > 0).
  Lo más alto que lo recibido subió una cosa inútil: red 3,1, camuflaje 2,9 al d20.

## 4 · ¿Compartir cambió también lo que vivían por sí mismas?

| serie · hermana | pruebas vividas: COMPARTE · SOLAS | botiquín, área d1-20 solo vivido: COMPARTE (b) · SOLAS | botiquín al d20: COMPARTE (b) · SOLAS | ración d20: (b) · SOLAS |
|---|---|---|---|---|
| s1 a10 valiente | 72 · 83 | 489 · 558 | 24,1 · 43,5 | 13,3 · 7,5 |
| s1 a11 prudente | 95 · 54 | 553 · 213 | 43,2 · 12,1 | 14,4 · 8,1 |
| s2 a10 valiente | 66 · 75 | 550 · 503 | 20,4 · 34,7 | 13,8 · 14,0 |
| s2 a11 prudente | 74 · 66 | 493 · 643 | 34,7 · 41,5 | 13,1 · 13,7 |
| s3 a10 valiente | 80 · 69 | 666 · 419 | 37,3 · 43,1 | 10,0 · 13,2 |
| s3 a11 prudente | 117 · 93 | 776 · 650 | 44,9 · 39,4 | 13,3 · 13,5 |

Sí: la prudente probó más por sí misma en COMPARTE que en SOLAS en 3 de 3 series (95 frente a 54, 74 frente a 66, 117 frente a 93); en total 4 de 6 hermanas probaron más en COMPARTE, y en 4 de 6 el área del botiquín
con SOLO lo vivido es mayor en COMPARTE que en SOLAS. Compartir no solo da recuerdos: cambia lo que se vive (una hermana que ya «sabe» del botiquín por la otra lo usa, y al usarlo vive).

## Lectura

1. Lo aprendido de la otra es real y acotado: entre 8 % y 46 % de lo que cada una cree del botiquín al d20; nunca falso (0 de 120 hermana-días).
2. Los cuadernos de las dos acaban idénticos: lo que mide «la que menos prueba» en S1 es la pareja (P7-53).
3. Compartir también cambió lo vivido: la prudente probó más en las tres series; para el siguiente campo, la medida «aprendido de la otra» debe ser (a − b) del cuaderno, no el área total.
