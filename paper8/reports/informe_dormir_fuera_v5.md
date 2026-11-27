# Valle · prompt 140 · Por qué la criatura se queda a dormir fuera

**Qué es esto:**
- Solo análisis de partidas ya jugadas: las de RG68r y RG068r del experimento v5 en sequía y sequía dura, días 0 a 9, y las seis del piloto del prompt 139 (RZ1 y RG68r).
- **No se ha jugado nada nuevo ni se ha llamado a ningún modelo.**
- **No cambia el congelado v5 ni las predicciones selladas:** no se han tocado.
- Sustituye al prompt 140 anterior.

**Los programas,** en `dormir_fuera_v5/`:
- `noches_v5.py` reconstruye cada noche de cada criatura con los registros. Las reglas están en su cabecera;
- `analiza_dormir_v5.py` hace las tablas (`tablas_dormir_v5.md`) y declara las reglas de los motivos y de la comparación del punto 5;
- `mira_noches_v5.py` es un primer vistazo.

**Lo que guarda cada registro, y lo que no:**
- **El registro de decisiones del v5** (`decisiones.jsonl.gz`, solo de RG68r) guarda, de cada decisión:
  - el turno, la criatura y lo elegido;
  - lo que habrían elegido el valorador de sumas y el de posición;
  - si tenía mucha hambre, si veía la bestia y a su hermana, y si era anochecer o noche;
  - la «mejora» de lo elegido.
- **No guarda** la segunda opción, ni qué candidatos había, ni el malestar de cada uno, ni sus filas. Así que, en las 80 partidas del v5, **no se puede saber si «ir a casa» estaba entre los candidatos ni cuánto le faltó para ganar.**
- **Eso solo se sabe, en parte, en las partidas del piloto,** que llevan el registro del diario:
  - **la segunda opción y su diferencia** (la «duda»). Así, «ir a casa» solo se ve si fue la primera o la segunda;
  - **las filas que más pesan en la foto de ahora,** que es lo que siente en ese momento, no la foto de lo elegido.
- **De la sequía dura no hay ninguna partida con ese detalle.**

**Las noches** (cabecera de `noches_v5.py`):
- **Una noche es «fuera»** si en la fase noche (turnos 280 a 399) está dormida fuera de su casa más de la mitad del tiempo; **«dentro»**, si está dormida dentro más de la mitad.
- **«El sueño»** es el primer turno desde el 240 (el anochecer) en que está dormida.
- **«A cuántos turnos de casa»** son los pasos del camino más corto hasta su puerta, más uno.

## 1 y 2. RG68r en el v5: las noches fuera y las noches dentro (días 0 a 9)

**sequía** (40 partidas): 3194 noches de criatura; **fuera 736 (23%)**, dentro 2370, despierta casi toda la noche 88.

| | noches fuera | noches dentro |
|---|---|---|
| al empezar el anochecer (turno 240), ya en casa | 0% | 24% |
| … si no, a cuántos turnos de casa | 17.5 (mediana 17) | 12.8 (mediana 12) |
| dónde estaba al empezar el anochecer | bosque 54%, huerto 27%, aldea 11%, salvaje 5% | bosque 43%, en casa 24%, aldea 14%, huerto 13% |
| turno del día en que se duerme | 246.7 (mediana 242) | 255.7 (mediana 253) |
| a cuántos turnos de casa se duerme | 14.5 (mediana 14) | 0.1 (mediana 0) |
| dónde se duerme | aldea 41%, bosque 36%, huerto 16%, salvaje 4% | en casa 99%, aldea 1%, bosque 0%, huerto 0% |
| cómo se duerme: eligió dormir | 94% | 94% |
| cómo se duerme: agotada | 3% | 0% |
| decisiones entre el turno 240 y el sueño (media) | 2.3 | 4.6 |
| eligió «ir_casa» alguna vez desde la mitad de la tarde | 77% | 96% |
| … turno de la primera vez | 240.9 (mediana 240) | 228.7 (mediana 236) |
| su hermana a 2 casillas o menos al dormirse | 79% | 79% |
| hambre al dormirse | 1.6 (mediana 2) | 4.8 (mediana 5) |

Lo que eligió desde el turno 200 hasta el sueño (todas las decisiones, de las noches fuera · de las de dentro):

| opción | noches fuera | noches dentro |
|---|---|---|
| quedarse | 20052 (78%) | 61667 (75%) |
| trabajar_planta | 1979 (8%) | 5740 (7%) |
| ir_casa | 400 (2%) | 3763 (5%) |
| dormir | 929 (4%) | 2743 (3%) |
| coger | 414 (2%) | 1529 (2%) |
| mover | 410 (2%) | 1531 (2%) |
| ir_pareja | 383 (1%) | 1506 (2%) |
| comer | 328 (1%) | 994 (1%) |
| ir_objeto | 262 (1%) | 838 (1%) |
| dejar | 4 (0%) | 656 (1%) |
| empujar | 278 (1%) | 325 (0%) |
| ir_botin | 141 (1%) | 435 (1%) |

Lo último que eligió antes de dormirse, en las noches fuera: ir_casa 271, quedarse 270, ir_pareja 60, trabajar_planta 25, comer 22, coger 22, mover 16, empujar 12.

**sequía dura** (40 partidas): 3189 noches de criatura; **fuera 766 (24%)**, dentro 2337, despierta casi toda la noche 86.

| | noches fuera | noches dentro |
|---|---|---|
| al empezar el anochecer (turno 240), ya en casa | 0% | 19% |
| … si no, a cuántos turnos de casa | 18.6 (mediana 19) | 13.7 (mediana 13) |
| dónde estaba al empezar el anochecer | bosque 56%, huerto 22%, aldea 9%, salvaje 7% | bosque 47%, en casa 19%, aldea 16%, huerto 12% |
| turno del día en que se duerme | 248.8 (mediana 242) | 258.3 (mediana 255) |
| a cuántos turnos de casa se duerme | 15.7 (mediana 16) | 0.2 (mediana 0) |
| dónde se duerme | bosque 39%, aldea 33%, huerto 15%, salvaje 5% | en casa 98%, aldea 1%, bosque 0%, en otra casa 0% |
| cómo se duerme: eligió dormir | 90% | 90% |
| cómo se duerme: agotada | 5% | 0% |
| decisiones entre el turno 240 y el sueño (media) | 2.7 | 4.1 |
| eligió «ir_casa» alguna vez desde la mitad de la tarde | 73% | 97% |
| … turno de la primera vez | 241.8 (mediana 240) | 230.3 (mediana 236) |
| su hermana a 2 casillas o menos al dormirse | 69% | 70% |
| hambre al dormirse | 9.0 (mediana 5) | 16.7 (mediana 13) |

Lo que eligió desde el turno 200 hasta el sueño (todas las decisiones, de las noches fuera · de las de dentro):

| opción | noches fuera | noches dentro |
|---|---|---|
| quedarse | 18848 (75%) | 50496 (70%) |
| trabajar_planta | 1923 (8%) | 5005 (7%) |
| ir_casa | 482 (2%) | 4463 (6%) |
| dormir | 1036 (4%) | 2942 (4%) |
| mover | 519 (2%) | 1972 (3%) |
| ir_pareja | 591 (2%) | 1841 (3%) |
| coger | 327 (1%) | 1235 (2%) |
| ir_objeto | 323 (1%) | 1133 (2%) |
| comer | 422 (2%) | 927 (1%) |
| ir_matorral | 161 (1%) | 554 (1%) |
| ir_botin | 185 (1%) | 521 (1%) |
| empujar | 163 (1%) | 300 (0%) |

Lo último que eligió antes de dormirse, en las noches fuera: quedarse 272, ir_casa 230, ir_pareja 89, mover 32, comer 27, trabajar_planta 24, ir_vecina 19, coger 18.

### Con más detalle: RG68r en las tres partidas del piloto (con el registro del diario), días 0 a 9

Solo aquí se sabe la segunda opción de cada decisión y su diferencia (la «duda»: el malestar de la segunda menos el de la elegida), y las filas que más pesan en su foto de ahora. «ir_casa» solo se ve si fue la primera o la segunda; si no, se sabe que perdía por más que la segunda. Las filas son las de la foto de ahora (lo que siente), no las de la foto de lo elegido: esas no se guardan.

| partida | noche | criatura | dónde y a cuántos turnos de casa al dormirse | cómo | en la decisión de dormir: segunda opción (diferencia) | ¿«ir_casa» en las dos primeras de alguna decisión desde el 240? | filas que más pesan (pérdida; ganancia) |
|---|---|---|---|---|---|---|---|
| normal 1001 | 0 | B1 | bosque, 23 | eligió dormir | ir_casa (0.116) | sí: t240 segunda, a 0.116 | R-CARENCIA 0.48, F-CANSANCIO 0.19, F-FRIO 0.15; G-F-HAMBRE 0.05, G-R-CARENCIA 0.01 |
| normal 1001 | 0 | B2 | bosque, 22 | eligió dormir | quedarse (0.148) | no | R-CARENCIA 0.50, F-CANSANCIO 0.43, R-ACOPIO 0.27; G-F-HAMBRE 0.05, G-R-CARENCIA 0.01 |
| normal 1001 | 1 | B2 | huerto, 15 | eligió dormir | ir_casa (0.032) | sí: t240 segunda, a 0.032 | F-CANSANCIO 0.58, R-ACOPIO 0.27, R-CARENCIA 0.24; G-F-HAMBRE 0.14, G-R-CARENCIA 0.12 |
| normal 1001 | 1 | C1 | bosque, 24 | eligió dormir | ir_casa (0.020) | sí: t240 segunda, a 0.020 | F-CANSANCIO 0.35, R-CARENCIA 0.30, F-FRIO 0.15; G-R-CARENCIA 0.08, G-F-HAMBRE 0.06 |
| normal 1001 | 1 | C2 | bosque, 23 | eligió dormir | empujar (0.066) | no | R-CARENCIA 0.42, F-CANSANCIO 0.39, R-ACOPIO 0.27; G-F-HAMBRE 0.05, G-R-CARENCIA 0.01 |
| normal 1001 | 1 | D2 | bosque, 21 | eligió dormir | empujar (0.075) | no | F-CANSANCIO 0.53, R-CARENCIA 0.33, R-ACOPIO 0.27; G-F-HAMBRE 0.06, G-R-CARENCIA 0.05 |
| normal 1001 | 2 | C2 | aldea, 5 | eligió dormir | trabajar_planta (0.077) | no | R-CARENCIA 0.31, R-ACOPIO 0.27, F-FRIO 0.15; G-R-CARENCIA 0.09, G-F-HAMBRE 0.04 |
| normal 1001 | 2 | D2 | bosque, 17 | eligió dormir | ir_casa (0.007) | sí: t240 segunda, a 0.007 | R-CARENCIA 0.34, R-ACOPIO 0.27, F-FRIO 0.15; G-F-HAMBRE 0.15, G-R-CARENCIA 0.07 |
| normal 1001 | 3 | B2 | bosque, 20 | eligió dormir | ir_casa (0.009) | sí: t240 segunda, a 0.009 | R-CARENCIA 0.36, R-ACOPIO 0.27, F-FRIO 0.15; G-F-HAMBRE 0.09, G-R-CARENCIA 0.01 |
| normal 1001 | 3 | C2 | bosque, 13 | eligió dormir | ir_casa (0.034) | sí: t245 segunda, a 0.059, t246 segunda, a 0.058, t252 segunda, a 0.034 | R-CARENCIA 0.62, F-DANO 0.40, S-DANO-PAREJA 0.29; G-F-HAMBRE 0.06, G-R-CARENCIA 0.00 |
| normal 1001 | 4 | C2 | bosque, 29 | eligió dormir | quedarse (0.059) | no | R-CARENCIA 0.88, S-SOLEDAD 0.33, R-ACOPIO 0.27; G-F-HAMBRE 0.06, G-R-CARENCIA 0.02 |
| normal 1001 | 5 | B2 | aldea, 4 | eligió dormir | mover (0.063) | sí: t241 elegida | R-CARENCIA 0.62, R-ACOPIO 0.27, F-FRIO 0.15; G-F-HAMBRE 0.05, G-R-CARENCIA 0.00 |
| normal 1001 | 5 | C2 | aldea, 5 | eligió dormir | quedarse (0.075) | sí: t240 elegida | R-CARENCIA 0.76, R-ACOPIO 0.27, F-FRIO 0.15; G-F-HAMBRE 0.11, G-R-CARENCIA 0.04 |
| normal 1001 | 6 | A2 | bosque, 14 | eligió dormir | empujar (0.055) | no | R-CARENCIA 0.88, F-CANSANCIO 0.49, R-ACOPIO 0.27; G-F-HAMBRE 0.18, G-R-CARENCIA 0.08 |
| normal 1001 | 6 | B2 | aldea, 3 | eligió dormir | empujar (0.076) | sí: t240 elegida | R-CARENCIA 0.76, R-ACOPIO 0.27, F-CANSANCIO 0.16; G-F-HAMBRE 0.03, G-R-CARENCIA 0.02 |
| normal 1001 | 6 | D1 | aldea, 3 | eligió dormir | trabajar_planta (0.022) | sí: t252 elegida | R-CARENCIA 0.50, F-CANSANCIO 0.32, F-FRIO 0.15; G-F-HAMBRE 0.05, G-R-CARENCIA 0.01 |
| normal 1001 | 7 | A2 | bosque, 26 | eligió dormir | quedarse (0.158) | no | R-CARENCIA 0.54, R-ACOPIO 0.27, F-FRIO 0.15; G-F-HAMBRE 0.05, G-R-CARENCIA 0.04 |
| normal 1001 | 9 | A1 | aldea, 3 | eligió dormir | mover (0.077) | no | R-CARENCIA 0.75, F-CANSANCIO 0.16, F-FRIO 0.15; G-F-HAMBRE 0.24, G-R-CARENCIA 0.23 |
| normal 1001 | 9 | B2 | bosque, 14 | eligió dormir | ir_casa (0.035) | sí: t240 segunda, a 0.035 | R-CARENCIA 0.74, F-CANSANCIO 0.42, R-ACOPIO 0.27; G-F-HAMBRE 0.09, G-R-CARENCIA 0.04 |
| sequía 1002 | 0 | A1 | salvaje, 33 | eligió dormir | ir_casa (0.142) | sí: t240 segunda, a 0.142 | R-CARENCIA 0.49, F-CANSANCIO 0.20, F-FRIO 0.15; G-F-HAMBRE 0.05, G-R-CARENCIA 0.01 |
| sequía 1002 | 0 | A2 | salvaje, 34 | eligió dormir | quedarse (0.153) | no | R-CARENCIA 0.49, F-CANSANCIO 0.43, R-ACOPIO 0.27; G-F-HAMBRE 0.06, G-R-CARENCIA 0.01 |
| sequía 1002 | 0 | B1 | huerto, 11 | eligió dormir | quedarse (0.130) | no | R-CARENCIA 0.90, F-CANSANCIO 0.30, F-FRIO 0.15; G-F-HAMBRE 0.07, G-R-CARENCIA 0.06 |
| sequía 1002 | 0 | B2 | bosque, 10 | eligió dormir | ir_casa (0.038) | sí: t240 segunda, a 0.038 | R-CARENCIA 0.38, R-ACOPIO 0.27, F-CANSANCIO 0.27; G-F-HAMBRE 0.05, G-R-CARENCIA 0.04 |
| sequía 1002 | 0 | C1 | huerto, 16 | eligió dormir | ir_casa (0.048) | sí: t240 segunda, a 0.048 | R-CARENCIA 0.39, F-CANSANCIO 0.26, F-FRIO 0.15; G-F-HAMBRE 0.05, G-R-CARENCIA 0.04 |
| sequía 1002 | 0 | C2 | huerto, 15 | eligió dormir | ir_casa (0.118) | sí: t240 segunda, a 0.118 | F-CANSANCIO 0.43, R-CARENCIA 0.40, R-ACOPIO 0.27; G-R-CARENCIA 0.19, G-F-HAMBRE 0.05 |
| sequía 1002 | 0 | D1 | salvaje, 29 | agotada | quedarse (0.186) | no | F-CANSANCIO 1.40, R-CARENCIA 0.26, F-FRIO 0.15; G-F-HAMBRE 0.04, G-R-CARENCIA 0.04 |
| sequía 1002 | 0 | D2 | salvaje, 25 | eligió dormir | ir_botin (0.143) | no | F-CANSANCIO 0.47, R-CARENCIA 0.40, R-ACOPIO 0.27; G-F-HAMBRE 0.05, G-R-CARENCIA 0.04 |
| sequía 1002 | 1 | A2 | bosque, 24 | eligió dormir | ir_casa (0.042) | sí: t241 segunda, a 0.042 | R-CARENCIA 0.78, R-ACOPIO 0.27, F-FRIO 0.15; G-F-HAMBRE 0.05, G-R-CARENCIA 0.00 |
| sequía 1002 | 1 | C2 | bosque, 27 | eligió dormir | empujar (0.074) | no | R-CARENCIA 0.34, R-ACOPIO 0.27, F-FRIO 0.15; G-R-CARENCIA 0.04, G-F-HAMBRE 0.03 |
| sequía 1002 | 3 | A2 | bosque, 15 | eligió dormir | ir_casa (0.015) | sí: t240 segunda, a 0.015 | F-CANSANCIO 0.28, R-ACOPIO 0.27, R-CARENCIA 0.20; G-R-CARENCIA 0.13, G-F-HAMBRE 0.13 |
| sequía 1002 | 3 | C1 | aldea, 5 | eligió dormir | quedarse (0.057) | no | R-CARENCIA 0.49, F-CANSANCIO 0.28, F-FRIO 0.15; G-F-HAMBRE 0.07, G-R-CARENCIA 0.01 |
| sequía 1002 | 4 | B2 | bosque, 23 | eligió dormir | empujar (0.050) | no | R-CARENCIA 0.74, R-ACOPIO 0.27, F-CANSANCIO 0.16; G-F-HAMBRE 0.13, G-R-CARENCIA 0.09 |
| sequía 1002 | 4 | C2 | aldea, 5 | eligió dormir | quedarse (0.060) | no | R-CARENCIA 0.39, R-ACOPIO 0.27, F-FRIO 0.15; G-F-HAMBRE 0.07, G-R-CARENCIA 0.02 |
| sequía 1002 | 5 | B1 | aldea, 5 | eligió dormir | quedarse (0.067) | no | R-CARENCIA 0.24, F-CANSANCIO 0.15, F-FRIO 0.15; G-F-HAMBRE 0.06, G-R-CARENCIA 0.05 |
| sequía 1002 | 5 | D2 | bosque, 23 | eligió dormir | quedarse (0.058) | sí: t242 segunda, a 0.054 | R-CARENCIA 0.33, R-ACOPIO 0.27, F-CANSANCIO 0.19; G-F-HAMBRE 0.11, G-R-CARENCIA 0.04 |
| sequía 1002 | 6 | D2 | aldea, 4 | eligió dormir | quedarse (0.058) | sí: t240 elegida | R-CARENCIA 0.74, R-ACOPIO 0.27, F-FRIO 0.15; G-F-HAMBRE 0.07, G-R-CARENCIA 0.00 |
| sequía 1002 | 7 | C1 | aldea, 5 | eligió dormir | quedarse (0.076) | no | R-CARENCIA 0.31, F-FRIO 0.15, S-DANO-PAREJA 0.15; G-R-CARENCIA 0.09, G-F-HAMBRE 0.04 |
| sequía 1002 | 8 | D2 | aldea, 5 | eligió dormir | quedarse (0.059) | sí: t240 elegida | R-CARENCIA 0.47, R-ACOPIO 0.27, F-CANSANCIO 0.26; G-F-HAMBRE 0.10, G-R-CARENCIA 0.09 |
| sequía 1002 | 9 | C1 | aldea, 3 | eligió dormir | comer (0.044) | no | R-CARENCIA 0.77, F-HAMBRE 0.15, F-FRIO 0.15; G-F-HAMBRE 0.04, G-R-CARENCIA 0.01 |
| bestias que crían 1003 | 0 | A1 | aldea, 5 | eligió dormir | quedarse (0.169) | no | F-CANSANCIO 0.58, R-CARENCIA 0.41, F-FRIO 0.15; G-F-HAMBRE 0.04, G-R-CARENCIA 0.03 |
| bestias que crían 1003 | 1 | A1 | aldea, 3 | eligió dormir | empujar (0.077) | no | R-CARENCIA 0.56, F-FRIO 0.15, S-DANO-PAREJA 0.15; G-F-HAMBRE 0.03, G-R-CARENCIA 0.00 |
| bestias que crían 1003 | 2 | A2 | bosque, 20 | eligió dormir | empujar (0.069) | no | R-CARENCIA 0.47, F-CANSANCIO 0.34, R-ACOPIO 0.27; G-F-HAMBRE 0.17, G-R-CARENCIA 0.13 |
| bestias que crían 1003 | 2 | C2 | aldea, 5 | eligió dormir | trabajar_planta (0.059) | no | R-CARENCIA 0.42, R-ACOPIO 0.27, F-CANSANCIO 0.20; G-R-CARENCIA 0.07, G-F-HAMBRE 0.03 |
| bestias que crían 1003 | 2 | D2 | bosque, 19 | eligió dormir | ir_casa (0.029) | sí: t240 segunda, a 0.029 | R-CARENCIA 0.29, R-ACOPIO 0.27, F-CANSANCIO 0.24; G-R-CARENCIA 0.06, G-F-HAMBRE 0.05 |
| bestias que crían 1003 | 4 | A2 | O, 11 | eligió dormir | quedarse (0.031) | sí: t242 elegida, t243 segunda, a 0.045, t244 segunda, a 0.481 | R-CARENCIA 1.00, F-CANSANCIO 0.76, R-ACOPIO 0.27; G-F-HAMBRE 0.06, G-R-CARENCIA 0.02 |
| bestias que crían 1003 | 4 | B2 | aldea, 5 | eligió dormir | ir_pareja (0.057) | sí: t272 elegida, t280 elegida | R-CARENCIA 0.79, F-CANSANCIO 0.54, F-FRIO 0.45; G-F-HAMBRE 0.23, G-R-CARENCIA 0.09 |
| bestias que crían 1003 | 4 | D1 | aldea, 4 | otro | mover (0.004) | no | R-CARENCIA 0.76, F-CANSANCIO 0.35, S-DANO-PAREJA 0.24; G-F-HAMBRE 0.04, G-R-CARENCIA 0.02 |
| bestias que crían 1003 | 6 | A1 | O, 11 | otro | comer (0.091) | sí: t241 elegida, t245 elegida, t251 segunda, a 0.136 | F-CANSANCIO 1.29, R-CARENCIA 0.54, P-RADAR-CUERPO 0.23; G-F-HAMBRE 0.27, G-R-CARENCIA 0.25 |
| bestias que crían 1003 | 6 | C2 | O, 11 | eligió dormir | quedarse (0.087) | sí: t240 elegida | F-CANSANCIO 0.65, P-RADAR-CUERPO 0.62, S-DANO-PAREJA 0.44; G-R-CARENCIA 0.38, G-F-HAMBRE 0.08 |
| bestias que crían 1003 | 6 | D1 | bosque, 18 | eligió dormir | quedarse (0.017) | sí: t240 segunda, a 0.076, t271 segunda, a 0.104, t301 segunda, a 0.751 | R-CARENCIA 0.89, R-HERMANO-FALTA 0.86, S-SOLEDAD 0.50; G-F-HAMBRE 0.34, G-R-CARENCIA 0.10 |
| bestias que crían 1003 | 8 | A1 | bosque, 14 | otro | ir_casa (0.057) | sí: t240 segunda, a 0.985, t241 segunda, a 0.057 | F-CANSANCIO 0.79, R-CARENCIA 0.76, F-HAMBRE 0.20; G-R-CARENCIA 0.24, G-F-HAMBRE 0.03 |
| bestias que crían 1003 | 8 | A2 | huerto, 16 | otro | empujar (0.114) | no | R-CARENCIA 1.00, F-CANSANCIO 0.52, F-HAMBRE 0.36; G-R-CARENCIA 0.05, G-F-HAMBRE 0.01 |
| bestias que crían 1003 | 8 | B2 | huerto, 16 | eligió dormir | quedarse (0.148) | no | F-FRIO 0.45, F-CANSANCIO 0.44, R-ACOPIO 0.27; G-F-HAMBRE 0.11, G-R-CARENCIA 0.10 |
| bestias que crían 1003 | 8 | D2 | aldea, 7 | eligió dormir | ir_bosque (0.006) | sí: t241 elegida | R-CARENCIA 1.00, F-CANSANCIO 0.90, S-DANO-PAREJA 0.15; G-F-HAMBRE 0.18, G-R-CARENCIA 0.05 |
| bestias que crían 1003 | 9 | A1 | bosque, 34 | eligió dormir | empujar (0.047) | no | R-CARENCIA 0.87, F-CANSANCIO 0.34, F-FRIO 0.15; G-F-HAMBRE 0.16, G-R-CARENCIA 0.05 |
| bestias que crían 1003 | 9 | B2 | aldea, 5 | eligió dormir | quedarse (0.029) | sí: t240 elegida | R-CARENCIA 0.46, R-ACOPIO 0.27, F-FRIO 0.15; G-F-HAMBRE 0.12, G-R-CARENCIA 0.00 |
| bestias que crían 1003 | 9 | D1 | bosque, 28 | eligió dormir | comer (0.070) | no | R-CARENCIA 0.75, F-CANSANCIO 0.20, F-FRIO 0.15; G-F-HAMBRE 0.04, G-R-CARENCIA 0.01 |

57 noches fuera en esas tres partidas, días 0 a 9.

**La última parte de la tarde (turnos 200 a 239), en esas tres partidas:** qué elegía en cada decisión y cuántas veces «ir_casa» fue la segunda opción, y por cuánto perdía; y las ganancias que más pesaban en su foto de ahora.

| noches | decisiones | lo elegido (las cuatro más) | «ir_casa» elegida | «ir_casa» segunda: veces y diferencia (mediana) | la ganancia que más pesa en la foto de ahora (media de la mayor) |
|---|---|---|---|---|---|
| fuera | 2034 | quedarse 90%, trabajar_planta 4%, coger 1%, mover 1% | 1% | 55 (3%), 0.005 | 0.106 |
| dentro | 5721 | quedarse 84%, trabajar_planta 6%, mover 2%, ir_casa 2% | 2% | 61 (1%), 0.034 | 0.117 |

## 3. De las noches fuera de RG68r, qué parte se explica por cada motivo

| motivo | sequía | sequía dura |
|---|---|---|
| seguía trabajando el huerto | 64 (9%) | 68 (9%) |
| iba a por comida que vio | 51 (7%) | 55 (7%) |
| estaba con la hermana o con vecinas | 53 (7%) | 92 (12%) |
| volvía tarde del árbol | 0 (0%) | 4 (1%) |
| se quedó agotada | 19 (3%) | 39 (5%) |
| otro: se durmió donde estaba, sin ir hacia casa | 291 (40%) | 301 (39%) |
| otro: iba hacia casa y se durmió por el camino | 258 (35%) | 207 (27%) |

«Otro», por lo último que eligió y dónde se durmió: ir_casa en aldea 388, quedarse en bosque 311, quedarse en huerto 124, quedarse en aldea 38, quedarse en salvaje 36, mover en O 23.

## 4. La gemela (RG068r), con el registro del mundo (días 0 a 9)

La gemela no guarda decisiones. Del registro del mundo y del de balance se sabe dónde está cada turno, cuándo entra en casa, desde dónde vuelve y cuándo y dónde se duerme.

| | sequía: RG68r · RG068r | sequía dura: RG68r · RG068r |
|---|---|---|
| noches fuera | 23% · 5% | 24% · 6% |
| ya en casa al empezar el anochecer (240) | 18% · 58% | 14% · 55% |
| noches dentro: turno en que entra en casa | 241.0 (mediana 250) · 232.1 (mediana 240) | 245.6 (mediana 252) · 233.5 (mediana 240) |
| noches dentro: turno en que empieza a volver | 206.7 (mediana 208) · 196.9 (mediana 197) | 214.8 (mediana 223) · 199.9 (mediana 200) |
| … desde cuántos turnos de casa | 14.2 (mediana 14) · 15.2 (mediana 14) | 15.3 (mediana 14) · 16.3 (mediana 15) |
| noches fuera: a cuántos turnos de casa al empezar el anochecer | 17.5 (mediana 17) · 12.5 (mediana 12) | 18.6 (mediana 19) · 15.4 (mediana 15) |
| noches fuera: turno en que se duerme | 246.7 (mediana 242) · 249.7 (mediana 248) | 248.8 (mediana 242) · 251.3 (mediana 248) |
| noches fuera: agotada al dormirse | 3% · 10% | 5% · 21% |

## 5. ¿El frío basta? Una comparación dentro de RG68r (no es una prueba)

En cada partida, las criaturas vivas el día 10 partidas en dos mitades por sus noches fuera de los días 0 a 9.

| mundo | partidas | noches fuera (media): más · menos | hambre media el día 10: más · menos | más − menos [95 %] | mueren en la partida: más · menos | más − menos [95 %] |
|---|---|---|---|---|---|---|
| sequía | 40 | 3.5 · 1.1 | 19.4 · 19.1 | +0.3 [-2.7, +3.3] | 8% · 6% | +0.01 [-0.04, +0.06] |
| sequía dura | 40 | 3.6 · 1.1 | 46.2 · 50.6 | -4.4 [-8.3, -0.3] \* | 53% · 58% | -0.05 [-0.14, +0.05] |

## 6. RZ1 en el piloto: las propuestas con «ir a casa» para la segunda mitad de la tarde o el anochecer

| partida | propuestas | esa noche durmió en casa | no | de las que no: el cuerpo tuvo «ir a casa» delante (con filas) en alguna decisión | … y eligió otra cosa |
|---|---|---|---|---|---|
| normal 1001 | 120 | 91 | 29 | 26 | 20 |
| sequía 1002 | 113 | 89 | 24 | 23 | 15 |
| bestias que crían 1003 | 125 | 93 | 32 | 29 | 27 |

En las 1703 decisiones con filas de esas propuestas que no acabaron en casa, el cuerpo eligió: quedarse quieta 573, dormir 382, trabajar el huerto 132, ir con la hermana 78, comer comida 73, ir a coger algo que ve 50, dar un paso 33, ir con una vecina que lo necesita 24 (y «ir a casa» 233). En 47 de ellas las filas cambiaron lo elegido.

Cuánto le faltó a «ir a casa» CON las filas: solo se sabe cuando fue la segunda opción (297 decisiones de 1470 en que eligió otra cosa): diferencia media 0.160, mediana 0.059, la menor 0.000 y la mayor 1.172. En las demás, «ir a casa» quedó tercera o más abajo: perdía por más que la segunda.

Para comparar, la parte de noches dormidas dentro (días 1 a 39; el día 0 no tiene propuestas): normal 1001: RZ1 con esa propuesta 75% de 118, RZ1 sin ella 79% de 194, RG68r (la misma semilla, días 1 a 39) 81%; sequía 1002: RZ1 con esa propuesta 79% de 107, RZ1 sin ella 80% de 205, RG68r (la misma semilla, días 1 a 39) 84%; bestias que crían 1003: RZ1 con esa propuesta 74% de 125, RZ1 sin ella 71% de 154, RG68r (la misma semilla, días 1 a 39) 76%.

SIN las filas, y CON las filas a fuerza entera: los registros no lo permiten. Se guarda, de cada decisión con filas, lo elegido y si sin filas habría ganado otra cosa (el candidato de menor malestar sin ellas), pero no el malestar de «ir a casa» con y sin filas, ni sus filas. Para saberlo habría que guardar el malestar de cada candidato con y sin las filas, o volver a jugar esas decisiones; aquí no se juega nada.


## Cuatro frases

1. **Qué la retiene fuera.** Pocas veces es el trabajo, la comida o la hermana: entre los tres son de 2 a 3 de cada 10 noches fuera (23 % en la sequía, 28 % en la sequía dura), y quedarse agotada, 3-5 de cada 100.
   - **Lo que pasa casi siempre** es que, al final de la tarde, se queda quieta en el bosque o en el huerto: 9 de cada 10 decisiones entre los turnos 200 y 240 son «quedarse». Está a unos 17-19 turnos de casa.
   - **Al empezar el anochecer,** cuando ya se puede dormir, dormir allí gana a ir a casa. Es casi siempre lo primero que elige: en el piloto, «ir a casa» queda segunda por muy poco, de 0,007 a 0,14.
   - **En 3 de cada 10 noches fuera** sí empezó a volver y se durmió por el camino.
   - **La gemela,** en cambio, empieza a volver hacia el turno 197-200 y ya está en casa al anochecer en más de la mitad de las noches. RG68r lo está en una de cada seis.
2. **Si lo que la retiene es una ganancia, los registros no lo dicen.**
   - No se guardan las filas del candidato elegido.
   - En la foto de ahora pesan sobre todo pérdidas: tener poca comida guardada, el cansancio y el frío. Las ganancias son pequeñas: la mayor, unos 0,11.
   - **La única pista es la gemela,** que es igual que RG68r salvo las filas de ganancia y vuelve antes. Apunta a que una ganancia la retiene quieta al final de la tarde, pero no se puede saber cuál.
3. **Si una promesa más fuerte la habría traído a casa, no se puede saber.**
   - Con las promesas que hubo, proponer «ir a casa» para la tarde o el anochecer no la trae más a casa. Duerme dentro el 75 %, 79 % y 74 % de esas noches, frente al 79 %, 80 % y 71 % de las noches sin esa propuesta.
   - **Cuando no vino,** «ir a casa» quedó segunda solo en 297 de 1.470 decisiones, a una diferencia mediana de 0,059. En el resto quedó más abajo. Las filas solo cambiaron lo elegido en 47 de 1.703 decisiones.
   - **Con las filas a fuerza entera:** los registros no guardan el malestar de «ir a casa» con y sin filas. Puede que en las decisiones de diferencia pequeña hubiera ganado, pero no se puede calcular sin volver a jugar.
4. **Qué no se puede saber con estos registros:**
   - las filas de lo elegido y de «ir a casa» en cada decisión;
   - el valor de «ir a casa» cuando no fue ni la primera ni la segunda;
   - qué ganancia la retiene quieta al final de la tarde;
   - de la gemela, cualquier decisión;
   - si dormir fuera por sí solo explica sus muertes de más. La comparación dentro de RG68r (punto 5) no lo apoya: las que más noches durmieron fuera no tenían más hambre el día 10. En la sequía dura tenían algo menos. Ni murieron más. Pero es una comparación, no una prueba: las que duermen fuera no son iguales que las demás en lo otro.

## Deslices de proceso

- **La primera tabla mezclaba la sequía con la sequía dura:** el patrón de búsqueda de «sequia» también recogía los ficheros de «sequia_dura». Lo vi porque salían idénticas. Lo arreglé antes de escribir nada.
- **Cambié la regla del motivo «con la hermana»:** al principio contaba tener a la hermana cerca al dormirse, y eso pasa igual dentro que fuera. Ahora pide haber elegido ir con ella o con una vecina.
- No he usado `python3 -c` ni `python3 -` sueltos, ni he esperado a ningún programa con `pgrep`.

## Gasto

| bolsa | gasto | saldo |
|---|---|---|
| créditos de la plataforma | **0** | no lo he leído |
| dólares de la consola de Anthropic | **0 $** (no se llamó a ningún modelo) | no lo he leído |
