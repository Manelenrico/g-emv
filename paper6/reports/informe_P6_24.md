# P6-24 · Réplica del puente con veinte semillas nuevas

*28-sep-2026. Gasto **3,5536 USD** de 5 (humo 0,0479 + A4 1,7099 + A7h 1,7958). `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados del cinco y los
32 del seis: 0 alterados al principio y al final. Nada cambia en los brazos: A4 es la versión
subida en P6-11 (`gemv-p6-A4-manos v1`, `b4e322cf`) y A7h la de P6-23 (`gemv-p6-A7h v1`,
`219ef011`). Lo nuevo, en archivos aparte y declarado: `semillas_P6_24.json`, `lanza_P6_24.py`,
`P6_24_brazos.json`, `mide_campo_P6_24.py` → `P6_24_campo_P623.json` (la medida sobre los
diarios de P6-23, para el sello), `P6_24_campo.json`, `P6_24_campo_40.json`; `sello_P6_24.py`
→ `SELLO_P6_24.md` (md5 `3d8b780b520d405a8d5f939cf3fec5bc`, cerrado antes de las tandas 1 y 2)
y `P6_24_sello.json`; `P6_24_pasos_humo.json`, `P6_24_pasos_serie.json`. Humo por la vía real.
Ningún número se escribió antes de calcularlo. Sin propuestas de diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**Con veinte semillas nunca usadas, el puente vuelve a arder menos: en las fases 5-7, A7h arde
62 tics menos que A4 por vida viva en el aviso 5, emparejado por semilla (n 19, mediana −77,
p unilateral 0,042, IC95 [−126, +3]); P6-23, con esta misma medida, daba −53 (p 0,047).** La
predicción del sello se cumple en dirección, prueba y magnitud. Lo secundario va en la misma
dirección que en P6-23: dentro del círculo 46 % contra 36 %, 19 de 70 planes sostenidos hasta
el final de la fase (P6-23: 6 de 58), pasos perdidos 0,02 % y 0,11 % (humo 0 en todas las
fases), y en vidas, anillo 23 contra 17, rival 7 contra 3, supervivientes 5 contra 17
(emparejado +0,6 por semilla, p 0,049; secundaria y de poca potencia, declarado).

## 1 · SEMILLAS, HUMO Y SERIE

**Las semillas** (`semillas_P6_24.json`): la sucesión de `semillas_S2` (paso 104.729)
continuada desde la última del seis (22.250.767), saltando los 20 valores siguientes, que ya
se habían usado en el cuatro o el cinco; 363 valores usados revisados (todo el seis, el cuatro,
el cinco y `paintball/runs`). Las 20 están escritas en el sello antes de jugar.

**El humo** (tanda 0, 0,0479 USD): una partida corta por brazo (mundo de P6-18 comprimido
hasta la fase 7) con la primera semilla nueva. Pasos perdidos **0 de 114 / 121 / 71** (A4) y
**0 de 114 / 107 / 116** (A7h) antes del aviso / fases 1-4 / fases 5-7, 0 fantasmas, retraso 0.
El diario de A4 arranca con el mismo registro, campo a campo, que el de P6-11; el de A7h con
`policy_pareja23`, puerta6 y el proceso: 8-9 propuestas del oráculo vueltas del proceso, 0
errores del juez, 1 suspensión.

**La serie** (tandas 1 y 2): 20 partidas por brazo, mundo 0.1.19, `roster_lento_v2`, 80
diarios enteros (3,1 GB, fuera de git, md5 en el manifiesto). Vidas vivas en el aviso de la
fase 5: A4 39 de 40, A7h 38 de 40; semillas emparejables: 19.

## 2 · LA MEDIDA PRINCIPAL

Tics ardiendo en las fases 5-7 (del aviso 5 al final de la vida o de la partida; arde =
distancia al centro mayor que el radio del tic), por vida viva en el aviso 5, media por
semilla, A7h − A4, emparejado; permutación exacta por cambio de signo, unilateral; IC95 de la
media por bootstrap (10.000 remuestreos).

| | A4 | A7h | A7h − A4 (emparejado) |
|---|---|---|---|
| tics ardiendo 5-7, media · mediana por vida | 231,7 · 228 | 169,6 · 144 | **−61,6** (mediana −77) |
| vidas con 0 tics ardiendo | 1 | 4 | |
| semillas en que A7h arde menos / más | | | 11 / 8 (n 19) |
| p unilateral (A7h arde menos) · bilateral | | | **0,042** · 0,085 |
| IC95 bootstrap de la media | | | [−125,7, +3,5] |

Las 19 diferencias por semilla: −297, +44,5, +20,5, +134, −208,5, +219, −38, −171, −77, −84,
−179, −170,5, −249, −103, +149,5, +15,5, +20, −242,5, +45,5. El efecto no es uniforme: en 8
semillas A7h arde más, en 11 menos, y las que menos arde son grandes (siete por debajo de
−170).

## 3 · LO SECUNDARIO (declarado, poca potencia)

| | A4 | A7h | A7h − A4 (emparejado, bilateral) |
|---|---|---|---|
| tics ardiendo en la fase 5 (medida de P6-23) | 192,4 | 117,8 | −73,1 · 6/13 · p 0,051 · IC95 [−139, −7] |
| % dentro del círculo, fase 5 | 35,6 | 46,0 | +9,3 · 11/8 · p 0,34 |
| planes de la fase 5: aceptados · sostenidos hasta el fin de fase | 0 · 0 | 70 · **19** | +0,95 sostenidos/semilla · 11/0 · p 0,001 |
| pasos perdidos, fases 5-7 (P6-21) | 1 / 4.282 (0,02 %) | 6 / 5.334 (0,11 %) | +0,25 · p 0,38 |
| pasos perdidos, toda la vida | 1 / 32.479 | 16 / 37.007 | |
| muertes por anillo · por rival · supervivientes | 23 · 7 · 5 | 17 · 3 · 17 | anillo −0,3 (p 0,35) · rival −0,2 (p 0,36) · supervivientes +0,6 · 10/4 · p 0,049 |

Pasos perdidos: retraso 0 tics en todos los pasos dados de los dos brazos; fantasmas 0 en
las fases 5-7. Los seis de A7h caen en 4 vidas.

Comparado con P6-23 (mismos brazos, semillas viejas): dentro 42,4 → 46,0 %; ardiendo fase 5
115,5 → 117,8 (A4 196 → 192); sostenidos 6 de 58 → 19 de 70; supervivientes A4 11 → 5, A7h
13 → 17; anillo A4 22 → 23, A7h 14 → 17. Las vidas siguen siendo lo que P6-17 dijo: ±10 es
lo detectable con 20 semillas; la diferencia de supervivientes (12 vidas, p 0,049 emparejado)
se anota como secundaria, sin sello, y no se convierte en titular.

## 4 · LAS 40 SEMILLAS JUNTAS (P6-23 + P6-24)

Las 20 semillas de P6-23 (A4 de P6-11, A7h de P6-23) y las 20 nuevas, con la misma medida y
la misma prueba (con 37 pares la permutación exacta no cabe: Monte Carlo de 1.000.000 de
cambios de signo, semilla 0, declarado en el JSON; el guion se corrigió para eso después de
que la primera pasada muriera sin traza al llegar a la prueba, y la unión se hace desde los dos
JSON ya medidos, mismas vidas y mismas medidas). Declarado: el md5 de `mide_campo_P6_24.py` en el
sello es `ca897b141002abc095bda58c68a82d3a` (la versión con la que se midieron `P6_24_campo_P623.json` y
`P6_24_campo.json`, permutación exacta, n ≤ 19); la versión final, `3c44463cd7a4a9c914f087eaabffe864`, solo
añade el Monte Carlo para n > 22 y el modo de unión.

| | A4 | A7h | A7h − A4 (emparejado) |
|---|---|---|---|
| vidas · vivas en el aviso 5 | 80 · 74 | 80 · 77 | 37 semillas emparejables |
| **tics ardiendo 5-7**, media · mediana por vida | 232,3 · 233,5 | 174,7 · 146 | **−57,6** (mediana −43) · 13/24 · **p unilateral 0,007** · bilateral 0,014 · IC95 [−100,9, −15,3] |
| tics ardiendo, fase 5 | 194,1 | 116,6 | −76,1 · 12/25 · p 0,005 · IC95 [−123, −28] |
| % dentro, fase 5 | 34,3 | 44,1 | +8,3 · 22/15 · p 0,18 |
| planes de la fase 5: aceptados · sostenidos | 0 · 0 | 128 · 25 | +0,62 sostenidos/semilla · 16/0 · p < 0,001 |
| pasos perdidos, fases 5-7 | 1 / 8.485 (0,01 %) | 26 / 10.860 (0,24 %) | |
| muertes por anillo · por rival · supervivientes | 45 · 13 · 16 | 31 · 15 · 30 | anillo −0,35 (p 0,10) · rival +0,05 (p 0,86) · supervivientes +0,35 · 17/10 · p 0,09 |

Con 40 semillas el intervalo de la medida principal ya no toca el cero: A7h arde entre 15 y
100 tics menos que A4 en las fases finales, 58 de media. Las vidas siguen dentro del ruido
(anillo p 0,10, supervivientes p 0,09), como P6-17 dijo que estarían.

## 5 · EL SELLO, CONTRASTADO (`SELLO_P6_24.md`, md5 `3d8b780b520d405a8d5f939cf3fec5bc`)

| | predicción | medido | veredicto |
|---|---|---|---|
| **principal** · tics ardiendo 5-7, A7h − A4 emparejado | < 0, p unilateral < 0,05, media dentro de [−109,6, +2,5] (IC95 de P6-23 con esta medida) | −61,6; p 0,042; dentro del intervalo | **acierta** |
| gasto | ≤ 5 USD | 3,5536 | **acierta** |
| secundarias (sin sello) · ardiendo fase 5 | A7h < A4 | −73,1 (p 0,051) | en la dirección prevista |
| · % dentro fase 5 | A7h > A4 | +9,3 (p 0,34) | en la dirección prevista |
| · sostenidos A7h | algunos | 19 de 70 | sí |
| · pasos perdidos 5-7 | cerca de 0; se declara si > 0,5 % | 0,02 % y 0,11 % | cerca de 0 |
| · anillo, rival, supervivientes | dentro del ruido | anillo 23/17, rival 7/3, supervivientes 5/17 (p 0,049) | en la dirección de P6-23; supervivientes al borde, sin sello |

Una observación sobre el encargo: la magnitud «−79 tics» de P6-23 era la de la fase 5; con la
medida pedida (fases 5-7) P6-23 da −53,3 (IC95 [−109,6, +2,5]). El sello recoge las dos y
fija el umbral con la de las fases 5-7; se contrasta contra esa.

## 6 · ARCHIVOS

| archivo | qué es |
|---|---|
| `semillas_P6_24.json` | las 20 semillas nuevas, cómo se eligieron y los 20 valores saltados |
| `lanza_P6_24.py` · `P6_24_brazos.json` · `P624_t*_*.json` | el lanzador (humo, A4, A7h), las dos políticas reutilizadas, las 42 partidas |
| `sello_P6_24.py` → `SELLO_P6_24.md`, `P6_24_sello.json` | el sello, con las semillas y los md5 de lo que juega y de lo que mide |
| `mide_campo_P6_24.py` → `P6_24_campo_P623.json`, `P6_24_campo.json`, `P6_24_campo_40.json` | la medida principal y las secundarias: sobre P6-23 (origen del sello), sobre P6-24, y las 40 juntas |
| `mide_pasos_P6_22.py` → `P6_24_pasos_humo.json`, `P6_24_pasos_serie.json` | pasos perdidos, fantasmas y retraso por fase |
| `DIARIOS_P6_MANIFIESTO.md` | los 84 diarios y zips de P6-24 con su md5 (fuera de git) |
