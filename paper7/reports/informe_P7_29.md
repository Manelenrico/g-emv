# P7-29 · Arreglar lo que hundía a la que recuerda, y la curiosidad del cuánto

*8-oct-2026. Coste: plataforma 0; consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar. Pieza nueva `nace_P7_29.py` (enganchada desde fuera tras descubre, pedir y nacer; GEMV_P7_29, apagada por defecto), política `policy_pareja_P7_29.py`, banco `banco_P7_29.py`, diagnóstico `diagnostico_P7_29.py`, imagen `Dockerfile.pareja_P7_29`, lanzador `lanza_P7_29.py`, lectura `analiza_P7_29.py`. Este informe lo escribe `escribe_informe_P7_29.py` desde los JSON citados en cada sección. Ninguna cifra a mano.*

## En corto

1. **Los muros no existían.** De las 2.232 rachas de 3 o más pasos bloqueados de P7-24 (71.892 tics), ninguna choca con un muro del mapa: la casilla destino es suelo en el `static_map` del propio diario en todas (y en las ocho orientaciones posibles del mapa). El 58 % de esos tics son `move_*` del cuerpo contra la hermana a la vista; el 42 % son suelo vacío en vidas cuya **decisión tardaba más que el tic**: el recuerdo por parecido se calculaba 216 veces por tic, y con 20-30 recuerdos APRENDE pasaba de los 41,7 ms (días 16-20: 31,0 ms de mediana, 32 % de tics por encima; TECHO 1,3 ms). Las observaciones se encolan, las acciones llegan tarde y el mundo contesta `blocked`. Esto corrige P7-28: la que recuerda no se hundía (solo) por el candidato, se hundía por lenta. Sección 0.
2. **Arreglo 0 (caché, sin cambiar decisiones):** las 16 vidas replicables de los días 16-20 se reproducen bit a bit con la caché (126.417 tics iguales, 3 difieren) y la decisión pasa de 6,8 a 1,34 ms de mediana en esta máquina.
3. **F1:** `apagado` reproduce A4 (2 tics distintos de 1.007.276, los mismos dos de P7-23); `TECHO` sin pedir, **con la red de muros encendida, NO** (1.095 tics en 3 vidas, 13 "muros" en casillas de suelo con un cuerpo que el cuerpo no ve); **con la red apagada, sí** (2 tics). La red queda apagada por defecto y el humo no se lanza hasta que la mesa decida (F4).
4. **F2 (arreglo 1, banco):** en 14 de 16 vidas el primer cambio de decisión es dejar `ir_curioso` (11 hacia una ración recordada a más de 2 casillas); la creencia del botiquín sin los cortes acaba el día 20 en s1·10 15,9→31,2 · s1·11 9,5→27,5 · s2·10 17,6→29,7 · s2·11 17,6→31,4 (de 50).
5. **F3 (el cuánto, banco):** la fila funciona como se diseñó (M 0,0555 con solo "al menos" → 0,0302 con un firme → 0,0184 con tres: se apaga; y en la foto de usar se alivia solo cuando le faltan más de lo que sabe que da), pero la vida elegida no sirve para ver el momento: el cuerpo solo ofrece `usar_botiquin` 10 tics (al final, fuera del círculo, cada 49 tics entre canales que el anillo corta) y lo elige las 10 veces con los cuatro cuadernos.

## Sección 0 · Por qué el mapa del cuerpo "no tenía" esos muros (antes de arreglar)

**Cómo se construye el mapa del cuerpo (solo describir).** El juego lo da ENTERO al empezar: el `player_config` trae `arena.static_map` (48 filas de 48 caracteres) con su leyenda y los pedestales; la política lo lee en `policy_cortex.py:889-900` y lo guarda en el diario (`static_map`), y `Mundo.desde_player_config` (`paintball/alma/mundo.py:72-105`) lo convierte en el mapa del cuerpo. Sólido es todo carácter cuya leyenda contiene "wall" o "rock" (`ch_wall`) o "fortress" (`ch_fortress`): `mundo.py:118-128`; `solido(x, y)` (`mundo.py:211-214`) devuelve verdadero para esos y para fuera del tablero. Los arbustos ('B', "berry_bush") no son sólidos. El cuerpo NO dibuja nada con lo que ve ni recuerda: no hay casillas "no vistas", el mapa es completo desde el tic 0 y no cambia en la partida. La geodésica (`decisor_zs.py:148-194`) hace un BFS desde el destino sobre ese mapa; lo no sólido es caminable; los cuerpos a la vista no entran en el mapa sino solo en el primer paso (`_paso_geodesico`, `decisor_zs.py:197-246`, con `cuerpos` de la receta, `decisor_zs.py:446-473`). Cambia de una semilla a otra: en el campo hay 20 mapas distintos para 40 (serie, día), y las 40 parejas de brazos de una misma semilla reciben el mismo (la serie 2 repite las 20 semillas de la serie 1).

**Qué hay en la casilla contra la que choca** (`diagnostico_P7_29.py` -> `P7_29_diagnostico.json`; racha = 3 o más pasos seguidos `blocked` con el paso listo desde la misma casilla y en la misma dirección, la regla del arreglo 2): 2.232 rachas, 71.892 tics. En TODAS la casilla destino es '.' (suelo) en el `static_map` del diario; girando, transponiendo o volteando el mapa tampoco sale un muro (tabla de giros en el JSON: con la identidad 30.210 de 30.210 tics sin nadie a la vista caen en suelo). En 1.363 rachas (41.682 tics) hay un agente A LA VISTA en la casilla: casi siempre la hermana, y lo elegido es un paso largo `move_*` (`move_E` 8.478, `move_S` 7.715, `move_W` 7.639, `move_NE` 6.380): los pasos largos del cuerpo (`mover`, `decisor_zs.py:786-788`, `_simula_camino`) no esquivan cuerpos (solo los `paso_*` y los `ir_*` lo hacen). Es del cuerpo de nacimiento y no se toca. En 869 rachas (30.210 tics) no hay nadie a la vista y lo elegido es `ir_objeto` / `ir_curioso` (`ir_objeto` 11.232, `ir_curioso` 10.687, `move_E` 2.664, `move_N` 2.553).

| racha más larga | brazo | desde · dirección · casilla | casilla en el mapa | agente a la vista encima | elegido | tics |
|---|---|---|---|---|---|---:|
| s1 d10 asiento 11 t4.924 | TECHO | (26, 22) · NE · (27, 21) | '.' (suelo) | sí | `move_NE` | 3.087 |
| s1 d3 asiento 11 t5.080 | TECHO | (27, 26) · S · (27, 27) | '.' (suelo) | sí | `move_S` | 3.047 |
| s2 d3 asiento 11 t2.349 | TECHO | (22, 21) · W · (21, 21) | '.' (suelo) | sí | `move_W` | 2.510 |
| s2 d17 asiento 11 t5.116 | APRENDE | (1, 1) · SE · (2, 2) | '.' (suelo) | no | `ir_objeto` | 2.170 |
| s1 d12 asiento 11 t5.289 | APRENDE | (19, 20) · S · (19, 21) | '.' (suelo) | no | `ir_curioso` | 1.614 |
| s2 d20 asiento 10 t5.048 | APRENDE | (28, 15) · SE · (29, 16) | '.' (suelo) | no | `ir_curioso` | 1.528 |
| s2 d18 asiento 11 t9.526 | APRENDE | (27, 26) · NW · (26, 25) | '.' (suelo) | no | `ir_objeto` | 1.301 |
| s2 d12 asiento 11 t7.140 | BORRADO | (26, 27) · E · (27, 27) | '.' (suelo) | sí | `move_E` | 1.261 |

**Por qué choca contra suelo vacío: la decisión tarda más que el tic.** El diario guarda el tiempo de cada decisión (`RADIOGRAFIA.ms`, `policy_cortex.py:511-618`); el mundo va a 24 tics por segundo (41,7 ms). La política decide una observación detrás de otra, en orden (`policy_cortex.py:881-960`): si tarda más que el tic, las observaciones se encolan y cada acción llega al mundo más tarde que la anterior, pedida desde una casilla en la que la criatura ya no está (los desplazamientos dejan de seguir la propia intención). Por brazo y bloque:

| brazo · bloque | vidas | tiempo de decisión por tic, mediana (media de vidas, ms) | tics por encima del tic (41,7 ms) | vidas con más del 20 % por encima | desplazamientos que siguen la propia intención | pasos listos bloqueados |
|---|---:|---:|---:|---:|---:|---:|
| APRENDE · dias 1-5 | 20 | 7,9 | 1,5 % | 0 | 99,5 % | 7,5 % |
| APRENDE · dias 6-10 | 20 | 9,3 | 6,5 % | 1 | 97,0 % | 8,4 % |
| APRENDE · dias 11-15 | 20 | 16,3 | 14,0 % | 3 | 91,8 % | 13,4 % |
| APRENDE · dias 16-20 | 20 | 31,0 | 32,3 % | 8 | 84,2 % | 32,0 % |
| BORRADO · dias 1-5 | 19 | 4,0 | 0,5 % | 0 | 99,7 % | 5,5 % |
| BORRADO · dias 6-10 | 19 | 3,9 | 0,3 % | 0 | 99,8 % | 4,5 % |
| BORRADO · dias 11-15 | 20 | 3,4 | 0,1 % | 0 | 100,0 % | 9,1 % |
| BORRADO · dias 16-20 | 20 | 4,2 | 0,2 % | 0 | 99,9 % | 5,2 % |
| TECHO · dias 1-5 | 20 | 1,8 | 0,0 % | 0 | 100,0 % | 15,8 % |
| TECHO · dias 6-10 | 19 | 1,8 | 0,0 % | 0 | 100,0 % | 13,4 % |
| TECHO · dias 11-15 | 20 | 1,8 | 0,0 % | 0 | 100,0 % | 10,2 % |
| TECHO · dias 16-20 | 19 | 1,3 | 0,0 % | 0 | 100,0 % | 11,9 % |

Las vidas que más chocan son las que más tardan (APRENDE; correlación de rangos entre la fracción de tics por encima del tic y la fracción de pasos bloqueados: 0,45):

| vida (APRENDE) | tics | ms mediana · p90 · máx | sobre el tic | desplazamientos · propios | pasos listos · bloqueados |
|---|---:|---|---:|---|---|
| s1 d20 asiento 11 | 1.062 | 101,0 · 106,9 · 147,1 | 100 % | 0 · — % | 1.062 · 1.062 (100 %) |
| s2 d18 asiento 10 | 272 | 89,5 · 90,8 · 113,7 | 100 % | 0 · — % | 272 · 270 (99 %) |
| s2 d18 asiento 11 | 2.629 | 79,5 · 98,6 · 171,2 | 100 % | 8 · 38 % | 2.549 · 2.536 (99 %) |
| s2 d20 asiento 10 | 2.558 | 94,6 · 98,0 · 204,1 | 98 % | 21 · 33 % | 2.348 · 2.317 (99 %) |
| s1 d12 asiento 11 | 3.235 | 97,9 · 130,3 · 269,0 | 87 % | 42 · 38 % | 2.815 · 2.750 (98 %) |
| s2 d17 asiento 11 | 7.137 | 59,8 · 82,7 · 217,0 | 74 % | 204 · 20 % | 5.097 · 4.627 (91 %) |
| s1 d11 asiento 11 | 9.096 | 41,6 · 89,0 · 255,7 | 50 % | 566 · 63 % | 3.436 · 2.037 (59 %) |
| s1 d9 asiento 11 | 9.384 | 16,4 · 107,7 · 186,4 | 44 % | 522 · 84 % | 4.164 · 2.624 (63 %) |

Dónde se iba el tiempo (`cProfile` sobre la réplica de s2 d19 asiento 11, 1.920 tics): `nace_P7_23.vivida` (el recuerdo por parecido, `recuerdo_P7_23.creencia_parecido` sobre todos los recuerdos de la cosa) se llamaba 414.759 veces (216 por tic) y sumaba 58,7 de los 61,6 s del decisor: cada candidato imagina sus filas, y cada `filas` pide k del botiquín y de la ración varias veces (`nace_P7_23.py:187-189, 236-241, 232-235`). Con 20-30 recuerdos por cosa, eso es lo que crece con los días. Esto NO es un obstáculo que el cuerpo perciba y el mapa no cuente: es un fallo de ingeniería de la pieza de P7-23. Consecuencia para P7-28: la caída de la que recuerda en los días 16-20 coincide con las vidas lentas (8 de 20 con más del 20 % de tics por encima del tic); el candidato `ir_curioso` que P7-28 señaló existe, pero la lentitud explica los atascos, y lo que explica el puesto habrá que volver a medirlo con la pieza rápida.

**Arreglo 0: la caché** (`nace_P7_29.vivida`): dentro del tic, el recuerdo por parecido se calcula una vez por (cosa, contexto dentro/golpeada, tic, día, número de recuerdos, foto) y se reutiliza. Mismos argumentos, mismo resultado: no cambia ninguna decisión. Comprobado (`banco_P7_29.py --cache`):

| réplica de las 16 vidas (días 16-20) | tics iguales · difieren | ms por decisión, mediana de medianas (esta máquina) |
|---|---|---:|
| sin cache | 126.417 · 3 | 6,75 |
| con cache | 126.417 · 3 | 1,34 |

| vida | tics | sin caché: ms mediana · p90 | con caché: ms mediana · p90 | iguales · difieren (con caché) |
|---|---:|---|---|---|
| s1_d16_ asiento 10 | 2.967 | 5,8 · 17,8 | 1,11 · 3,26 | 2.967 · 0 |
| s1_d16_ asiento 11 | 11.136 | 7,5 · 20,5 | 1,13 · 2,90 | 11.136 · 0 |
| s1_d17_ asiento 10 | 11.568 | 11,9 · 28,1 | 2,09 · 4,81 | 11.568 · 0 |
| s1_d17_ asiento 11 | 11.592 | 4,3 · 27,7 | 0,87 · 4,37 | 11.592 · 0 |
| s1_d18_ asiento 10 | 7.169 | 6,8 · 24,0 | 1,37 · 3,98 | 7.169 · 0 |
| s1_d18_ asiento 11 | 7.390 | 6,7 · 25,0 | 1,45 · 4,27 | 7.390 · 0 |
| s1_d19_ asiento 10 | 961 | 5,8 · 20,5 | 1,17 · 4,04 | 961 · 0 |
| s1_d19_ asiento 11 | 10.920 | 9,7 · 25,6 | 1,34 · 3,86 | 10.920 · 0 |
| s1_d20_ asiento 10 | 11.064 | 4,8 · 26,0 | 0,82 · 4,94 | 11.064 · 0 |
| s2_d16_ asiento 10 | 12.312 | 7,1 · 15,1 | 1,40 · 3,17 | 12.312 · 0 |
| s2_d16_ asiento 11 | 12.648 | 4,7 · 25,1 | 0,80 · 3,76 | 12.648 · 0 |
| s2_d17_ asiento 10 | 5.236 | 13,8 · 43,2 | 1,75 · 6,67 | 5.236 · 0 |
| s2_d17_ asiento 11 | 7.137 | 11,6 · 18,7 | 2,06 · 4,33 | 7.134 · 3 |
| s2_d19_ asiento 10 | 1.720 | 4,1 · 11,5 | 0,83 · 2,33 | 1.720 · 0 |
| s2_d19_ asiento 11 | 1.920 | 10,0 · 23,2 | 1,62 · 4,03 | 1.920 · 0 |
| s2_d20_ asiento 11 | 10.680 | 3,2 · 26,8 | 0,61 · 5,17 | 10.680 · 0 |

**Y el arreglo 2 (apuntar el muro tras tres choques)** queda como red de seguridad para lo que no se ve (Manel, 8-oct), con un añadido declarado: si en la casilla hay un agente a la vista no se apunta nada (un cuerpo no es un muro). Lo que la red encuentra en los diarios de A4 (F1) son casillas de suelo sin nadie a la vista que el mundo bloquea tres tics y luego deja pasar (lo más probable, un cuerpo que el cuerpo no ve: camuflado; no comprobado): no son muros, y marcarlas cambia decisiones. Por eso queda apagada.

## F1 · Con todo apagado y con TECHO sin pedir, se reproducen los diarios de A4

`banco_P7_29.py --f1` sobre los 80 diarios de A4 (P6-11 tandas 1 y 2, P6-24; GEMV_P7_PIDE=0 como en P7-23), con la pieza enganchada (GEMV_P7_29=1) -> `P7_29_F1.json`:

| F1 | arreglos encendidos | tics iguales · difieren | vidas con desacuerdo | muros aprendidos | desacuerdos (primeros) |
|---|---|---|---:|---:|---|
| apagado | cache, curiosidad, muros, corte, cuanto | 1.007.274 · 2 | 1 | 0 | 21622393/10 t1832 move_SW→move_W; 21622393/10 t2041 move_NW→paso_NE |
| TECHO con la red de muros | cache, curiosidad, muros, corte, cuanto | 1.006.181 · 1.095 | 3 | 13 | 21622393/10 t1832 move_SW→move_W; 21622393/10 t2041 move_NW→paso_NE; 21727122/10 t5076 ir_objeto→ir_botin |
| TECHO sin la red de muros | cache, corte, cuanto, curiosidad | 1.007.274 · 2 | 1 | 0 | 21622393/10 t1832 move_SW→move_W; 21622393/10 t2041 move_NW→paso_NE |

Los dos tics de `apagado` son los mismos dos de P7-23 (`P7_23_F1.json`). Con la red de muros, TECHO aprende 13 "muros" en casillas de suelo donde no se ve a nadie (en P611_t2 21727122, tic 5074-5076: la criatura en (15, 26) pide `move W` tres veces y el mundo dice blocked; en (14, 26) no hay muro ni agente a la vista; la hermana está en (17, 26)) y a partir de ahí decide distinto. **F1 pasa sin la red y no pasa con ella.** La red queda apagada por defecto (`nace_P7_29.E["arreglos"]["muros"] = False`); lo que queda de la mesa por decidir: si se quita del todo o si se cambia por otra regla (por ejemplo, una marca que caduque). No se ha seguido con el humo.

## F2 · Los arreglos 1 y 2 sobre las vidas de APRENDE de los días 16-20 (banco)

`banco_P7_29.py --f2`: las 16 vidas replicables (las 4 parciales no traen `player_config`), con la caché y el arreglo 1 (la red de muros aparte, abajo), el PRIMER instante en que la decisión de la réplica se separa del diario, y lo que pasaba en ese instante -> `P7_29_F2.json`:

| vida | tics | primer cambio (tic) | el diario hacía → la réplica hace | en ese tic: destino de `ir_curioso` (clase, distancia) · vida · botiquines · paso bloqueado en el diario | cambios en toda la réplica · desde `ir_curioso` · a qué |
|---|---:|---:|---|---|---|
| s1_d16_ asiento 10 | 2.967 | 481 | ir_curioso → ir_objeto | rations, 7 casillas · 100 · 0 · no | 306 · 302 · noop 180, ir_pareja 64, ir_objeto 18, move_NW 11, ir_botin 7 |
| s1_d16_ asiento 11 | 11.136 | 548 | ir_curioso → ir_botin | rations, 7 casillas · 100 · 0 · no | 2912 · 2912 · coger 1301, noop 1017, ir_botin 282, ir_objeto 203, ir_centro 83 |
| s1_d17_ asiento 10 | 11.568 | 481 | ir_curioso → ir_objeto | rations, 6 casillas · 100 · 0 · no | 6328 · 6323 · noop 3623, coger 1500, ir_centro 910, ir_objeto 136, ir_botin 108 |
| s1_d17_ asiento 11 | 11.592 | 481 | ir_curioso → ir_objeto | rations, 4 casillas · 100 · 0 · no | 490 · 490 · noop 397, move_SE 24, ir_objeto 17, move_S 15, soltar_first_aid 13 |
| s1_d18_ asiento 10 | 7.169 | 896 | ir_curioso → ir_botin | first_aid, 5 casillas · 100 · 0 · no | 2561 · 2560 · coger 2412, noop 109, ir_botin 17, ir_objeto 6, ir_pareja 4 |
| s1_d18_ asiento 11 | 7.390 | 490 | ir_curioso → noop | rations, 2 casillas · 100 · 0 · no | 3507 · 3507 · noop 2766, ir_botin 404, ir_objeto 218, ir_centro 106, coger 12 |
| s1_d19_ asiento 10 | 961 | 481 | ir_curioso → ir_objeto | rations, 3 casillas · 100 · 0 · no | 5 · 5 · ir_botin 4, ir_objeto 1 |
| s1_d19_ asiento 11 | 10.920 | 481 | ir_curioso → ir_objeto | rations, 3 casillas · 100 · 0 · no | 3061 · 3056 · coger 2069, noop 428, move_W 238, move_S 180, move_SW 74 |
| s1_d20_ asiento 10 | 11.064 | ninguno | — | — · — · — · no | 0 · 0 ·  |
| s2_d16_ asiento 10 | 12.312 | 481 | ir_curioso → ir_botin | rations, 5 casillas · 100 · 0 · no | 7504 · 7504 · coger 4061, noop 2829, ir_objeto 499, ir_pareja 26, ir_botin 20 |
| s2_d16_ asiento 11 | 12.648 | 617 | ir_curioso → noop | rations, 9 casillas · 100 · 0 · no | 125 · 125 · noop 72, ir_objeto 18, coger 12, ir_centro 6, move_NW 5 |
| s2_d17_ asiento 10 | 5.236 | 481 | ir_curioso → ir_objeto | rations, 8 casillas · 100 · 0 · no | 1432 · 1431 · noop 1150, ir_objeto 103, coger 88, ir_botin 41, move_NW 32 |
| s2_d17_ asiento 11 | 7.137 | 575 | ir_objeto → ir_botin | — · 100 · 0 · no | 2406 · 2403 · ir_objeto 2123, noop 195, ir_botin 31, move_S 31, ir_centro 16 |
| s2_d19_ asiento 10 | 1.720 | 604 | ir_curioso → ir_objeto | first_aid, 2 casillas · 100 · 0 · no | 219 · 219 · noop 197, coger 6, ir_objeto 4, ir_centro 4, usar_botiquin 3 |
| s2_d19_ asiento 11 | 1.920 | 481 | ir_curioso → ir_objeto | rations, 7 casillas · 100 · 0 · no | 381 · 381 · noop 226, ir_objeto 64, move_E 30, ir_pareja 29, coger 10 |
| s2_d20_ asiento 11 | 10.680 | 2.261 | ir_curioso → noop | rations, 7 casillas · 100 · 0 · no | 78 · 78 · noop 40, coger 25, ir_objeto 8, move_N 2, move_SW 2 |

Lectura. En 14 de 16 vidas, el primer cambio es dejar `ir_curioso`; en 11 de ellas el destino era una ración recordada a más de 2 casillas. (La réplica sigue las observaciones del diario: después del primer cambio, "cambios en toda la réplica" dice cuántas veces el cuerpo habría elegido distinto en las mismas escenas, no lo que habría pasado.) **Cuántos pasos dejarían de chocar:** ninguno por muros, porque no había muros (sección 0): los 30.210 tics bloqueados contra suelo vacío son de la latencia y desaparecen con la caché; los 41.682 contra la hermana son del cuerpo. Con la red de muros encendida en la réplica: s1_d16_/10: 0 muros, primer cambio 481; s1_d16_/11: 0 muros, primer cambio 548; s1_d17_/10: 5 muros, primer cambio 481; s1_d17_/11: 0 muros, primer cambio 481; s1_d18_/10: 0 muros, primer cambio 896; s1_d18_/11: 12 muros, primer cambio 490; s1_d19_/10: 0 muros, primer cambio 481; s1_d19_/11: 0 muros, primer cambio 481; s1_d20_/10: 29 muros, primer cambio 1949; s2_d16_/10: 0 muros, primer cambio 481; s2_d16_/11: 13 muros, primer cambio 617; s2_d17_/10: 4 muros, primer cambio 481; s2_d17_/11: 43 muros, primer cambio 575; s2_d19_/10: 0 muros, primer cambio 604; s2_d19_/11: 0 muros, primer cambio 481; s2_d20_/11: 2 muros, primer cambio 2261.

**Arreglo 3 sobre los cuadernos del campo:** la creencia del botiquín recalculada sin los cortes (`CuadernoP29.creencia`), por criatura y día (`P7_29_F2.json`, `creencia_sin_cortes`; aquí los días 1, 5, 10, 15, 19 y 20):

| serie · asiento | día | recuerdos del botiquín: firmes · al menos · cortes | creencia dentro CON cortes (la del campo) | creencia dentro SIN cortes (arreglo 3) | ignorancia de la clase | ignorancia del cuánto | lo más alto que sabe |
|---|---:|---|---:|---:|---:|---:|---:|
| s1 · 10 | 1 | 0 · 0 · 0 | — | — | 1,000 | 1,000 | — |
| s1 · 10 | 5 | 1 · 0 · 4 | 9,1 | 23,9 | 0,126 | 0,523 | 50,0 |
| s1 · 10 | 10 | 2 · 4 · 12 | 22,3 | 36,9 | 0,050 | 0,323 | 50,0 |
| s1 · 10 | 15 | 2 · 6 · 15 | 17,2 | 34,2 | 0,046 | 0,381 | 50,0 |
| s1 · 10 | 19 | 2 · 7 · 16 | 15,9 | 32,6 | 0,050 | 0,430 | 50,0 |
| s1 · 10 | 20 | 2 · 7 · 16 | 15,9 | 31,2 | 0,053 | 0,443 | 50,0 |
| s1 · 11 | 1 | 0 · 1 · 2 | 8,7 | 17,8 | 0,225 | 1,000 | 33,0 |
| s1 · 11 | 5 | 0 · 1 · 5 | 4,6 | 16,1 | 0,146 | 1,000 | 33,0 |
| s1 · 11 | 10 | 1 · 3 · 14 | 6,9 | 29,7 | 0,059 | 0,427 | 50,0 |
| s1 · 11 | 15 | 1 · 7 · 15 | 8,3 | 27,1 | 0,053 | 0,491 | 50,0 |
| s1 · 11 | 19 | 1 · 8 · 16 | 9,5 | 27,9 | 0,057 | 0,542 | 50,0 |
| s1 · 11 | 20 | 1 · 8 · 16 | 9,5 | 27,5 | 0,060 | 0,555 | 50,0 |
| s2 · 10 | 1 | 1 · 1 · 8 | 24,1 | 31,3 | 0,081 | 0,398 | 50,0 |
| s2 · 10 | 5 | 1 · 2 · 8 | 22,1 | 29,5 | 0,082 | 0,448 | 50,0 |
| s2 · 10 | 10 | 2 · 3 · 10 | 29,6 | 34,8 | 0,068 | 0,304 | 50,0 |
| s2 · 10 | 15 | 2 · 5 · 13 | 18,3 | 32,3 | 0,061 | 0,360 | 50,0 |
| s2 · 10 | 19 | 2 · 6 · 13 | 17,8 | 30,3 | 0,067 | 0,409 | 50,0 |
| s2 · 10 | 20 | 2 · 6 · 13 | 17,6 | 29,7 | 0,070 | 0,421 | 50,0 |
| s2 · 11 | 1 | 0 · 1 · 0 | — | — | 0,498 | 1,000 | 4,0 |
| s2 · 11 | 5 | 0 · 1 · 3 | — | — | 0,205 | 1,000 | 4,0 |
| s2 · 11 | 10 | 1 · 1 · 9 | 12,0 | 28,4 | 0,085 | 0,432 | 50,0 |
| s2 · 11 | 15 | 2 · 4 · 17 | 18,2 | 34,1 | 0,046 | 0,318 | 50,0 |
| s2 · 11 | 19 | 2 · 5 · 17 | 17,7 | 31,9 | 0,053 | 0,363 | 50,0 |
| s2 · 11 | 20 | 2 · 5 · 17 | 17,6 | 31,4 | 0,056 | 0,376 | 50,0 |

## F3 · La curiosidad del cuánto (banco)

`banco_P7_29.py --f3` sobre la vida s1 d20 asiento 10 de P7-24 (11.064 tics; lleva dos botiquines casi todo el día y no los usa), con cuatro cuadernos del botiquín (el resto del cuaderno, el real del día 19) -> `P7_29_F3.json`. Por tic con botiquín en el zurrón (usar no necesita el paso listo; durante el canal el candidato queda vetado):

| cuaderno del botiquín | tics con botiquín en el zurrón | tics en que el cuerpo ofrece `usar_botiquin` (vida) | elige `usar_botiquin` (vida) | M del cuánto en lo elegido, mediana · máx | M de la curiosidad de clase (mediana) | ignorancia del cuánto · lo más alto que sabe (cuaderno al fin) |
|---|---:|---|---|---|---:|---|
| (a) solo 'al menos' (30, 25, 20) | 11.044 | 10 (95, 85, 75, 65, 55, 45, 36, 26, 16, 6) | 10 (95, 85, 75, 65, 55, 45, 36, 26, 16, 6) | 0,0555 · 0,1035 | 0,0085 | 1,000 · 30,0 |
| (b) (a) + un firme (45) | 11.044 | 10 (95, 85, 75, 65, 55, 45, 36, 26, 16, 6) | 10 (95, 85, 75, 65, 55, 45, 36, 26, 16, 6) | 0,0302 · 0,0562 | 0,0074 | 0,487 · 45,0 |
| (c) (a) + tres firmes (45, 40, 42) | 11.044 | 10 (95, 85, 75, 65, 55, 45, 36, 26, 16, 6) | 10 (95, 85, 75, 65, 55, 45, 36, 26, 16, 6) | 0,0184 · 0,0343 | 0,0061 | 0,240 · 45,0 |
| (d) el real del día 19 (2 firmes, 7 'al menos', 16 cortes) | 11.044 | 10 (95, 85, 75, 65, 55, 45, 36, 26, 16, 6) | 10 (95, 85, 75, 65, 55, 45, 36, 26, 16, 6) | 0,0281 · 0,0522 | 0,0042 | 0,443 · 50,0 |

| cuaderno | fila del cuánto en la foto de `usar_botiquin`, por vida al ofrecerse (de más a menos vida) |
|---|---|
| (a) | vida 95: 0,0512, vida 85: 0,0512, vida 75: 0,0512, vida 65: 0,0512, vida 55: 0,0512, vida 45: 0,0512, vida 36: 0,0512, vida 26: 0,0546, vida 16: 0,0906, vida 6: 0,0906 |
| (b) | vida 95: 0,0296, vida 85: 0,0305, vida 75: 0,0305, vida 65: 0,0305, vida 55: 0,0305, vida 45: 0,0305, vida 36: 0,0492, vida 26: 0,0492, vida 16: 0,0492, vida 6: 0,0492 |
| (c) | vida 95: 0,0181, vida 85: 0,0209, vida 75: 0,0209, vida 65: 0,0209, vida 55: 0,0209, vida 45: 0,0209, vida 36: 0,0300, vida 26: 0,0300, vida 16: 0,0300, vida 6: 0,0300 |
| (d) | vida 95: 0,0276, vida 85: 0,0288, vida 75: 0,0288, vida 65: 0,0288, vida 55: 0,0288, vida 45: 0,0288, vida 36: 0,0457, vida 26: 0,0457, vida 16: 0,0457, vida 6: 0,0457 |

Lectura. Con solo "al menos" (lo más alto que sabe: 30), la ignorancia del cuánto es 1 y la fila vale lo que la curiosidad de clase el día 1 (misma escala, misma calma: M 0,0555 frente a 0,0085 de la clase, ya sabida). En la foto de usar, la fila baja (alivio 0,5 en la clase del botiquín) solo cuando le faltan más de 30 de vida (tabla: con (a) baja desde vida 65; con (b) y (c), sabe 45, desde vida 55; con (d), sabe 50, desde vida 45). Con un recuerdo firme la ignorancia del cuánto baja a 1/(1 + peso) y con tres se apaga como cualquier ignorancia. En esta vida la criatura va a 100 de vida 10.870 de los 11.044 tics con botiquín y solo pierde vida al final, fuera del círculo: el cuerpo ofrece `usar_botiquin` 10 veces (entre canales de 48 tics que el anillo corta) y lo elige las 10 con los cuatro cuadernos: aquí decide el cuerpo (la cura imaginada con la creencia), no el cuánto. El momento en que el cuánto mueve por sí solo (herida media con botiquín y calma) no aparece en esta vida; habrá que verlo en el humo.

## F4 · El humo de 3 días

NO LANZADO. La cadena de pruebas de la mesa dice "si una falla, para y dilo": F1 no pasa con la red de los muros encendida (sección F1). La imagen (`Dockerfile.pareja_P7_29`, con la red apagada por defecto), las semillas (`semillas_P7_29.json`, k 175-177) y el lanzador (`lanza_P7_29.py --cadena-aprende 1 1 3`) están listos; se lanza con el "adelante" de Manel, con la red apagada (recomendación) o como la mesa decida.

## F5 · Créditos del humo

Plataforma: 0 (nada lanzado; acumulado de la séptima sin cambio: 41,9017 USD). Consola de Anthropic: 0.


## Lo que queda para la mesa

1. La red de los muros: apagada (F1 no pasa con ella; no hay muros que aprender, lo que no se ve no es un muro: bloquea unos tics y se va). Quitarla o cambiarla.
2. P7-28 se corrige: la que recuerda se hundía por lenta (sección 0). Habría que volver a jugar los días 16-20 (o un campo corto) con la pieza rápida antes de atribuir el puesto al candidato `ir_curioso`.
3. El humo F4 está listo para lanzar con el "adelante".
