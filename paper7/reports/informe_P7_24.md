# P7-24 · El campo de la primera etapa: nacer sin saber qué curan el botiquín ni la ración

*8-oct-2026 (jugado del 7 al 8 de octubre; P7-24 sellado el 7, freno corregido en P7-27). Coste: plataforma 11,8449 USD (las 120 partidas, freno incluido); consola 0.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar. Sello: `SELLO_P7_24.md` (con sus dos añadidos posteriores, declarados).
Diarios en `paintball/runs/P724_*` (fuera de git); `analiza_P7_24.py` → `P7_24_vidas.json`; `sello_P7_24.py` → `P7_24_resumen.json`; este informe lo escribe `escribe_informe_P7_24.py`.
El sello se ha evaluado una sola vez, al final.*

## El sello

| | regla | resultado | |
|---|---|---|---|
| E1 | descubre: firmes de los dos al día 5 en las 4; ignorancia < 0,3 al día 10 en ≥ 3 | firmes de los dos al día 5: **1 de 4**; ignorancia < 0,3 al día 10: 4 de 4 | **no pasa** |
| E2 | aprende a aprender: el segundo objeto tarda menos en ≥ 3 | 1 de 4 | **no pasa** |
| E3 | qué aprende antes: la ración llega al 80 % antes que el botiquín en ≥ 3 | 3 de 4 | **pasa** |
| E4 | pierde y recupera: APRENDE − TECHO > 2 ee en 1-5; ≤ la mitad en 16-20 | 1-5: 1,80 ± 1,29 (n 20); 16-20: 6,50 ± 1,45 (n 12) | **no pasa** |
| E5 | sin memoria no recupera: BORRADO − TECHO en 16-20 ≥ la mitad de 1-5 | 1-5: 1,06 ± 1,33 (n 18); 16-20: 3,56 ± 1,02 (n 18) | **pasa** |
| E6 | lo aprendido cambia la conducta: vida al abrir el botiquín (11-20), APRENDE < BORRADO | medianas 75 (34 aperturas) frente a 77 (87) | **pasa** |

**Pasan E3, E5 y E6; no pasan E1, E2 y E4.** Y lo que no estaba previsto: **la que recuerda acaba peor, y cada vez peor.** APRENDE − TECHO pasa de 1,8 puestos en los días 1-5 a
6,5 en los días 16-20; APRENDE − BORRADO, de 0,9 a 4,0. Sin excluir las partidas con corte sale lo mismo (E4: 1,80 ± 1,29 (n 20) y 6,53 ± 1,22 (n 15)).

## Sección 1 · El campo tal como se jugó

- 3 brazos × 20 días × 2 series = 120 partidas, la misma semilla para los tres brazos cada día (`semillas_P7_24.json`: k = 155-174; serie 2 en orden inverso). 240 vidas.
- **Partidas con corte de la plataforma: 8** (serie 1 día 3 BORRADO, serie 1 día 10 BORRADO, serie 1 día 12 APRENDE, serie 1 día 18 TECHO, serie 1 día 20 APRENDE, serie 2 día 7 TECHO, serie 2 día 18 APRENDE, serie 2 día 20 APRENDE): en 4 de ellas un asiento de BORRADO o TECHO no tiene ni artefacto ni registro de salida (de ese asiento no queda nada);
  en las 4 de APRENDE, un asiento (o los dos en s2 d18) se cortó a media partida y su diario se rescató del registro de salida hasta el tic del corte, con el cuaderno de fin.
  Según la decisión de la mesa, el aprendizaje de esas vidas cuenta hasta el corte y las 8 partidas enteras (16 vidas) salen de puesto, vida al morir y causa; en las emparejadas se quita el par.
- El freno (días 1-3 de APRENDE, serie 1) se corrigió en P7-27 ((b'): tocan 4 de 6) y el campo siguió desde el día 4 sin repetir nada.

## Sección 2 · Las medidas, por brazo y bloque de días

| brazo | días | vidas (en puesto) | puesto medio | mueren · vida al morir (mediana) | usos botiquín: n (firmes, «al menos», cortes) · vida al usar | usos ración: n (firmes, cortes) · vida al usar | pedidos · regalos | `ir_curioso` con el paso listo (mediana, %) | vidas con esperanza | vidas que tocan botiquín / ración |
|---|---|---:|---:|---|---|---|---|---:|---:|---|
| TECHO | 1-5 | 20 (20) | 6,80 | 15 · 3 | 0 (0, 0, 0) · — | 0 (0, 0) · — | 25 · 31 | 0,0 | 0 | 17 / 11 |
| TECHO | 6-10 | 19 (18) | 5,94 | 15 · 2 | 0 (0, 0, 0) · — | 0 (0, 0) · — | 26 · 19 | 0,0 | 0 | 16 / 14 |
| TECHO | 11-15 | 20 (20) | 6,00 | 12 · 6 | 0 (0, 0, 0) · — | 0 (0, 0) · — | 24 · 8 | 0,0 | 0 | 17 / 15 |
| TECHO | 16-20 | 19 (18) | 4,39 | 13 · 4 | 0 (0, 0, 0) · — | 0 (0, 0) · — | 29 · 48 | 0,0 | 0 | 17 / 11 |
| BORRADO | 1-5 | 19 (18) | 8,44 | 16 · 3 | 39 (1, 17, 19) · 86 | 15 (10, 0) · 78 | 11 · 7 | 3,6 | 8 | 14 / 9 |
| BORRADO | 6-10 | 19 (18) | 4,67 | 14 · 4 | 26 (2, 15, 9) · 83 | 20 (5, 1) · 86 | 7 · 7 | 0,6 | 10 | 15 / 10 |
| BORRADO | 11-15 | 20 (20) | 5,20 | 16 · 4 | 26 (3, 14, 9) · 84 | 13 (8, 0) · 86 | 11 · 8 | 0,9 | 9 | 16 / 13 |
| BORRADO | 16-20 | 20 (20) | 7,35 | 17 · 3 | 58 (2, 15, 41) · 76 | 11 (6, 0) · 79 | 7 · 4 | 1,2 | 6 | 16 / 6 |
| APRENDE | 1-5 | 20 (20) | 8,60 | 15 · 4 | 27 (2, 5, 20) · 60 | 25 (10, 3) · 86 | 18 · 19 | 8,2 | 12 | 11 / 15 |
| APRENDE | 6-10 | 20 (20) | 8,90 | 19 · 5 | 36 (4, 7, 25) · 52 | 26 (10, 0) · 92 | 28 · 19 | 7,8 | 15 | 17 / 18 |
| APRENDE | 11-15 | 20 (18) | 7,44 | 18 · 5 | 27 (1, 11, 15) · 75 | 26 (11, 0) · 86 | 25 · 46 | 10,4 | 18 | 14 / 17 |
| APRENDE | 16-20 | 20 (14) | 11,86 | 14 · 6 | 5 (0, 3, 2) · 80 | 10 (5, 0) · 73 | 16 · 15 | 38,8 | 8 | 9 / 12 |

TECHO sabe y no escribe recuerdos (las piezas del siete no están en ese brazo), así que sus usos salen de los canales del diario (`P7_24_techo_canales.json`, con las definiciones
de P7-21): canales del botiquín días 1-5: 55 (18 completados) · vida al abrir 55; días 6-10: 54 (16 completados) · vida al abrir 58; días 11-15: 37 (15 completados) · vida al abrir 60; días 16-20: 73 (19 completados) · vida al abrir 55. Y en APRENDE, en los días 16-20, la mediana de `ir_curioso` con el paso listo sube al 38,8 % y los usos caen
a 5 de botiquín y 10 de ración en 20 vidas: la que recuerda, con la ignorancia ya baja, se pasa el final del campo yendo a por cosas.

Causa de muerte: en todas las vidas que mueren, `final.reason` = `eliminated` (el diario no distingue anillo de rival en el final; P7-21 lo midió por el daño).

## Sección 3 · E1, E2 y E3 de cerca (las 4 criaturas de APRENDE)

**E1.** | criatura | recuerdos firmes al acabar el día 5: botiquín / ración | ignorancia al acabar el día 10: botiquín / ración |
|---|---|---|
| s1_10 | 1 / 0 | 0,050 / 0,081 |
| s1_11 | 0 / 2 | 0,059 / 0,062 |
| s2_10 | 1 / 5 | 0,068 / 0,071 |
| s2_11 | 0 / 3 | 0,085 / 0,196 |

**E2.** | criatura | primer contacto (tics de vida acumulados): botiquín / ración | primer recuerdo firme: botiquín / ración | tarda desde el contacto: botiquín / ración | orden | el segundo tarda menos |
|---|---|---|---|---|---|
| s1_10 | 12.135 / 13.737 | 12.397 / 68.112 | 262 / 54.375 | botiquin → racion | no |
| s1_11 | 659 / 10.300 | 105.360 / 12.923 | 104.701 / 2.623 | racion → botiquin | no |
| s2_10 | 494 / 2.302 | 13.043 / 13.092 | 12.549 / 10.790 | botiquin → racion | sí |
| s2_11 | 8.018 / 13.115 | 71.518 / 46.581 | 63.500 / 33.466 | racion → botiquin | no |

**E3.** | criatura | día en que la ración llega a 12 | día en que el botiquín (dentro) llega a 40 | la ración antes |
|---|---:|---:|---|
| s1_10 | 17 | nunca | sí |
| s1_11 | 6 | nunca | sí |
| s2_10 | nunca | nunca | no |
| s2_11 | 13 | nunca | sí |

Lo que se ve: las cuatro bajan la ignorancia por debajo de 0,3 (a 0,05-0,10 al final), pero los recuerdos **firmes** son pocos: el cuerpo usa casi siempre entero y aprende «al menos».
La creencia de la ración llega a 12-15 (su cura es 15) en 3 de 4; la del botiquín dentro del círculo se queda en 9-30 (su cura es 50) y nunca llega a 40. El segundo objeto no tarda
menos que el primero (1 de 4).

## Sección 4 · El puesto (E4, E5, sin predicción)

| comparación | días 1-5 (media ± error estándar) | días 16-20 |
|---|---|---|
| APRENDE - TECHO · excluyendo las partidas con corte | 1,80 ± 1,29 (n 20) | 6,50 ± 1,45 (n 12) |
| APRENDE - TECHO · sin excluir nada | 1,80 ± 1,29 (n 20) | 6,53 ± 1,22 (n 15) |
| BORRADO - TECHO · excluyendo las partidas con corte | 1,06 ± 1,33 (n 18) | 3,56 ± 1,02 (n 18) |
| BORRADO - TECHO · sin excluir nada | 1,53 ± 1,34 (n 19) | 2,84 ± 1,20 (n 19) |
| APRENDE − BORRADO (sin predicción; partidas con corte fuera) | 0,94 ± 1,39 (n 18) | 4,00 ± 1,45 (n 14); todos los días 2,84 ± 0,69 (n 68) |

Lectura: en los días 1-5 los tres brazos están cerca (APRENDE y BORRADO entre 1 y 2 puestos peor que TECHO, dentro del error); en los días 16-20 APRENDE está 6,5 puestos
peor que TECHO y 4,0 peor que BORRADO. No es que no recupere: empeora con lo que aprende. Figuras: `P7_24_fig_puesto.png` (el puesto por día) y
`P7_24_fig_creencias.png` (creencia e ignorancia por día de cada criatura, APRENDE y BORRADO).

## Sección 5 · Lo aprendido y la conducta (E6)

Vida al abrir el botiquín en los días 11-20: APRENDE mediana 75 en 34 aperturas; BORRADO 77 en 87. Pasa por 2 puntos y con
menos de la mitad de aperturas: la que recuerda usa el botiquín menos veces.

## Sección 6 · GIF de los datos

`P7_24_primer_firme_botiquin.gif` (serie 1, día 2, asiento 10, tic 901: el primer recuerdo firme del botiquín), `P7_24_primer_firme_racion.gif` (serie 1, día 8, asiento 10, tic 2.436)
y `P7_24_uso_dia15.gif` (serie 1, día 15, asiento 10, tic 12.636: un uso del botiquín con el cuaderno de 14 días). Fuera de git, como los otros GIF.

## Sección 7 · Créditos

Plataforma: 11,8449 USD en 120 partidas (0,0987 por partida); de ellos, 0,2756 del freno (P7-24). Consola: 0.
Acumulado del siete en la plataforma: 30,3324 (hasta P7-26, que ya incluía el freno) + 11,5693 = 41,9017 USD. Saldos no consultados.

## Lo que esto dice, y lo que queda para la mesa

1. El cuerpo que nace sin saber **descubre** las dos cosas (ignorancia a 0,05-0,10 en veinte días) pero aprende **poco y flojo**: casi todo «al menos», y el botiquín se queda en una
   creencia de 9-30 sobre 50. La ración, más barata y usada más veces, sí llega a su cura.
2. **Recordar empeora el puesto**, y más cuanto más se recuerda: el mismo rastro que en los dos campos anteriores (APRENDE un puesto peor que BORRADO), aquí más grande
   (2,8 ± 0,7 sobre todos los días). Dónde se pierde es la pregunta siguiente; lo que este campo da son los diarios para mirarlo.
3. Los 8 cortes de la plataforma están declarados y excluidos; las conclusiones no cambian sin excluirlos.
