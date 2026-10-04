# P6-26 · Dos piezas pequeñas: ¿existe un plan que pase?, y el humo de campo de A8

*28-sep-2026. Ninguna serie. Gasto de lenguaje: **0,0467 USD** en el campo (cabecera del sidecar, 8
llamadas) más el humo nativo con la clave (2 llamadas, tope propio 0,05 USD, no guardado aparte) de un
tope de 3; plataforma 0,1120 USD (una partida; la otra volvió sin coste declarado). `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados del cinco y los 32 del seis:
0 alterados al principio y al final. La clave, solo desde `cantera/paper5/.env` en el humo nativo, ni
impresa ni escrita; en el campo, por el sidecar de Bedrock, sin clave en la imagen. Lo nuevo, en archivos
aparte y declarado: `banco_P6_26.py` → `P6_26_banco.json`, `P6_26_banco_juicios.json`; `sello_P6_26_banco.py`
→ `SELLO_P6_26_banco.md` (md5 `6f2c4b959604174985993fb7490899df`, cerrado antes del banco); el brazo A8:
`texto_escena_P6_26.py`, `puerta_proceso_P6_26.py`, `policy_pareja26.py`, `humo_red_P6_26.py`,
`Dockerfile.pareja26`, `lanza_P6_26.py`, `P6_26_brazos.json`; `mide_P6_26.py` → `P6_26_humo.json`,
`P6_26_pasos_humo.json`, `P6_26_pasos_atribucion.json`; `sello_P6_26_serie.py` → `SELLO_P6_26_serie_borrador.md`
(md5 `15b2d6b9c73bfdeb91a1441a5f81cbc6`) y `P6_26_sello_serie_borrador.json`. Ningún número se escribió
antes de calcularlo. Sin propuestas de diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**(1) En las escenas donde la puerta6 rechazó al razonador, casi nunca hay un plan de «ir y quedarse»
que pase: existe alguno en el 22,6 % (Haiku) y el 15,7 % (Sonnet) de esas escenas, y cuando existe,
pasan casi todos los destinos (41 de 49 de mediana): la puerta juzga la escena, no la casilla. (2) El
humo de campo de A8 (dos razonadores Haiku, uno por hermano, 2 semillas del puente) cierra la cadena
entera: 8 llamadas, 0,047 USD, retraso de 113 tics de mediana (4,7 s), 8 planes traducidos, 2 aceptados
con la instantánea de llegada, 2 respuestas que llegan donde la puerta ya rechaza, 2 mensajes de plan
en lugar de un E2, 1 recibido por el hermano, 2 registros de malestar. Pero pierde el 1,2 % de los
pasos en las fases 5-7 (3 de 249; tres en tics de encargo del razonador): pasa del 1 %, así que PARO y
lo digo. La serie de 40 semillas costaría 5,4 USD (6,8 con margen) y no se lanza.**

## 1 · BANCO SIN LENGUAJE: ¿EXISTE UN PLAN QUE PASE? (`banco_P6_26.py`)

En las escenas de P6-25 donde puerta6 rechazó la primera propuesta (Haiku 93, Sonnet 83) y en los 20 +
20 pares de pareja donde solo una puerta aceptó, se probaron TODOS los planes del espacio del oráculo:
cada destino alcanzable que sigue a salvo al llegar (`Oraculo.seguras`, la lista de la que el oráculo
elige; 49 destinos por instantánea de mediana, 61 como máximo) con el plan de ir y quedarse de A7h y sus
puntos de control, juzgado por la puerta6 real en proceso aparte sobre la misma instantánea de la
pregunta. 150 instantáneas, 6.379 juicios, 805 s, 0 errores.

| | Haiku | Sonnet |
|---|---|---|
| escenas rechazadas | 93 | 83 |
| **(a) con al menos un plan que pasa** | **21 = 22,6 %** | **13 = 15,7 %** |
| en ellas, planes que pasan (mediana de 49 probados) | 41,5 (todas las escenas: 0) | |
| el único plan del oráculo pasaba en… | 12 (las 12 están entre las 21) | 7 (las 7 entre las 13) |
| **(b) mejor ganancia disponible**, mediana · p90 · máx. | **0,171** · 0,309 · 0,340 | **0,253** · 1,119 · 1,448 |
| (c) distancia al mejor plan (Chebyshev), 1ª · 2ª · 3ª propuesta | 3 (n 21) · 3 (n 7) · 4 (n 4) | 3 (n 13) · 6 (n 3) · 6 (n 2) |
| (c) distancia al plan que pasa más cercano, 2ª · 3ª | 1 (3 de 7 a 0 casillas) · 2 (0 de 4) | 4 (0 de 3) · 4 (1 de 2 a 0) |
| **(d) pares con una sola puerta: los dos tienen un plan que pasa** | **4 / 20 = 20 %** | **5 / 20 = 25 %** |
| (d) zona común aceptada por los dos (≤ 3 casillas) | 4 / 20 = 20 % | 5 / 20 = 25 % |

**Lo que dicen.** (1) El rechazo es de la escena: en 60 de las 150 instantáneas pasa algún plan y en
ellas pasan casi todos los destinos; en las otras 90 no pasa ninguno de los ~49. El comparador puerta6
(el cuerpo imaginado decidiendo paso a paso) gana o pierde contra «quedarse» como bloque, no casilla a
casilla. (2) Donde existe un plan que pasa, el del oráculo ya era uno (12 de 12 y 7 de 7): el barrido no
encuentra escenas que el oráculo perdiera. (3) El bucle de Manel (P6-25) no acerca: en 3 de 7 segundas
propuestas de Haiku el destino ya coincidía con uno que pasa y aun así no pasó (el destino no es lo que
decide). (4) En la pareja, donde una puerta aceptó y la otra no, hay plan para los dos en uno de cada
cuatro o cinco pares, y cuando lo hay la zona es común.

**Sello del banco** (`SELLO_P6_26_banco.md`): (a) predicho 40-70 %, falla si < 25 %: **falla** en los
dos (22,6 y 15,7 %); (b) mediana entre 0,15 y 0,40 y p90 > 0,40: Sonnet acierta (0,253; 1,119), Haiku
no alcanzada (mediana 0,171 dentro, p90 0,309 fuera); (c) no se acercan: **acierta** (con n de 7/4 y
3/2, declarado); (d) los dos con plan en la mitad o más, falla si < 25 %: Haiku **falla** (20 %), Sonnet
no alcanzada (25 %). 1 acierto, 2 no alcanzadas, 3 fallos: había puesto demasiado en el espacio de
destinos, y el espacio no es el que manda.

## 2 · HUMO DE CAMPO: DOS RAZONADORES HAIKU, UNO POR HERMANO (A8)

**Qué es A8** (`policy_pareja26.py`): A7h tal cual (puerta6 en proceso aparte, ir y quedarse, compromiso6b
con el veto V2 y la cuenta justa) con el razonador Haiku 4.5 en el sitio del oráculo, y solo esto:

- Cada hermano tiene su razonador con la escena del seis en lenguaje llano (`texto_escena_P6_26.py`, los
  mismos bloques de P6-25 más «El plan de tu hermano»). El disparo es el mismo del oráculo (arde o holgura
  ≤ 33), calculado en el proceso.
- **La llamada no toca el hilo principal**: va en un hilo del proceso juez (`puerta_proceso_P6_26._juez26`,
  `hilo_llamada`), por el sidecar de Bedrock (`--use-bedrock`, `BEDROCK_MODEL` = Haiku 4.5), con el gasto
  leído de `X-Coworld-Spend-Usd` y un tope propio de 0,6 USD por vida. Los juicios de la puerta se siguen
  sirviendo mientras el modelo piensa.
- **La puerta juzga con la instantánea del momento en que LLEGA la respuesta.** Dónde: `policy_pareja26.
  AlmaPareja26._aplica_razonador` deja la propuesta en `cf.entregado` en el tic de llegada (`self.tick`), y
  en ese mismo tic `_recoge(obs)` (heredado de P6-23, `policy_pareja23.py`) hace `self.hilo.encarga_juicio(
  fv.id, fv, self, obs)` con el `obs` y la memoria de ese tic. En el diario: `razonador26` con `tick_pregunta`,
  `tick` (llegada), `tics_de_vuelta` y `juzgada_con`, y la `forma_evaluada` con tick ≥ llegada. Además el
  proceso juzga la misma propuesta con la instantánea de la pregunta (`juicio_pregunta`), solo para medir.
- El plan aceptado viaja al hermano por el canal en lugar de un E2: `texto_escena_P6_26.mensaje_plan`
  («`P6 P11 t12772 D24,24 H50 F12996`», 31 caracteres), emitido por la voz del cuerpo (`envuelve_voz`, una
  vez, y vuelve al E2); el hermano lo parsea (`plan26: plan del hermano recibido`) y su razonador lo lee en
  la escena siguiente.
- El diario del siete: al cerrarse cada plan aceptado, `malestar26` con tres columnas por tramo:
  propuesto (la mitad emocional dicha), imaginado (signos proyectados y curva de necesidades de la puerta),
  pasado (signos y necesidades sentidas en los puntos de control).

**Humos**: en nativo, mock (cadena entera), Haiku real (1 llamada, 5,4 s, plan aceptado a la llegada,
mensaje por el cable) y reloj (450 observaciones a 41,67 ms: 0 decisiones tarde); dentro de la imagen,
mock a ritmo de reloj (`OK humo A8 mock`), custodias y «ninguna clave en la imagen» OK.

**Las dos partidas** (`lanza_P6_26.py`, semillas 20260916 y 20365645, mundo 0.1.19, roster_lento_v2,
política `gemv-p6-A8:v1` = `35d839c1-…`):

| por vida | 20260916 s10 | 20260916 s11 | 20365645 s10 | 20365645 s11 | **partida 1** | **partida 2** | **total** |
|---|---|---|---|---|---|---|---|
| tics vividos · final | 13.560 · anillo | 12.528 · elim. | 11.096 · elim. | 11.784 · elim. | | | |
| encargos al proceso · «no dispara» | 224 · 220 | 202 · 199 | 142 · 142 | 158 · 154 | | | 726 · 715 |
| **llamadas** | 3 | 2 | 0 | 3 | 5 | 3 | **8** |
| **coste (sidecar)** | 0,0137 | 0,0080 | 0 | 0,0249 | 0,0218 | 0,0249 | **0,0467 USD** (0,0058 por llamada) |
| **retraso en tics**, mediana · p95 (máx.) | 132 · 146 (146) | 113 · 113 | — | 80 · 131 (131) | | | **113 · 146** (3,3-6,1 s) |
| ms por llamada, mediana | 4.943 | 4.268 | — | 2.996 | | | |
| planes traducidos · intraducibles · calla · errores | 3 · 0 · 0 · 0 | 2 · 0 · 0 · 0 | 0 | 3 · 0 · 0 · 0 | | | 8 · **0** · 0 · 0 |
| pasan en la pregunta · en la llegada | 2 · 0 | 0 · 1 | — | 1 · 1 | | | 3 · 2 |
| **llegan donde la puerta ya rechaza** | **2** | 0 | — | 0 | 2 | 0 | **2 de 3** que pasaban |
| aceptados (a la llegada) | 0 | 1 | 0 | 1 | 1 | 1 | **2** |
| **E2 sustituidos** | 0 | 1 | 0 | 1 | 1 | 1 | **2** (uno por plan aceptado) |
| **el hermano recibe un plan** | 1 | 0 | 0 | 0 | 1 | 0 | **1** |
| malestar26 (planes cerrados) | 0 | 1 (cumplida) | 0 | 1 (caída) | | | 2 |
| lat. máx. del tic (ms) | 59,5 | 24,7 | 21,5 | 24,6 | | | |

Los dos mensajes: `P6 P11 t12772 D24,24 H50 F12996` y `P6 P11 t12077 D24,24 H122 F12996`; el primero lo
recibió el hermano (asiento 10 de 20260916, en su tic 12772+), el segundo llegó con el hermano ya muerto.

**Malestar imaginado y vivido** (`P6_26_humo.json`, 2 planes, 4 tramos; signo de la vida: `+` = la
necesidad baja):

| plan | tramo | propuesto (dicho, por) | imaginado (signo, necesidades F/R/S al final) | pasado |
|---|---|---|---|---|
| 20260916 s11, cumplida | 1 ir | `+`, F-ANTICIPACION | `+`, 1,24 / 0,81 / 0,56 | `−`, 1,33 / 0,87 / 0,70 |
| | 2 esperar 50 | `+`, F-DANO | `−`, 1,27 / 0,86 / 0,68 | `−`, 1,35 / 1,00 / 1,01 |
| 20365645 s11, caída (área) | 1 ir | `−`, F-ANTICIPACION | `−`, 1,30 / 1,00 / 1,13 | (cayó antes del punto) |
| | 2 esperar 50 | `−`, F-DANO | `+`, 1,29 / 1,00 / 1,11 | (cayó antes) |

En el único plan que llegó a sus puntos de control, lo vivido fue peor que lo imaginado en los dos
tramos (la necesidad de vida subió de 1,24 a 1,33 y de 1,27 a 1,35 en vez de bajar): una aceptación
falsa, la primera contada con las tres columnas.

**Pasos perdidos** (P6-21, `P6_26_pasos_humo.json`): antes del aviso 0 de 1.652; fases 1-4 1 de 760
(0,13 %); **fases 5-7 3 de 249 = 1,2 %**, retraso de los pasos dados 0. Los cuatro, uno a uno
(`P6_26_pasos_atribucion.json`): tres en el tic en que el hilo principal encarga al razonador (tic del
cuerpo 44, 48 y 52 ms) y uno en un tic de encargo de juicio (59 ms, el caso conocido de P6-23). La causa
está a la vista en la tabla: A8 encarga al razonador 726 veces en 4 vidas (cada 25 tics, con la
instantánea entera, ~1 MB) y solo 11 disparan; el oráculo de A7h mandaba un encargo ligero (P6-23,
0,14 ms) y calculaba el disparo en el proceso. **Pasa del 1 %: paro.** La serie no se lanza; el sello de
la serie queda en borrador con esta condición previa escrita.

## 3 · COSTE ESTIMADO DE LA SERIE (40 semillas, A7h contra A8 con Haiku) Y PARADA

| | |
|---|---|
| plataforma, 40 partidas de A8 (0,112 USD por partida, la única con coste declarado) | 4,48 USD |
| lenguaje, 80 vidas × 2,0 llamadas por vida × 0,0058 USD (humo, por el sidecar) | 0,93 USD |
| A7h en las mismas 40 semillas | 0 (ya jugadas: P6-23 + P6-24) |
| **total estimado** | **5,42 USD** (6,82 con margen a 5 llamadas por vida) |

La serie NO se lanza. Antes hace falta que el encargo al razonador deje de costar un tic (infraestructura,
como en P6-22 y P6-23: el disparo con un encargo ligero y la instantánea solo cuando dispara) y un humo
nuevo con 0 pasos perdidos; entonces se rehace el sello con los md5 nuevos. El borrador
(`SELLO_P6_26_serie_borrador.md`) lleva la medida principal (tics ardiendo en las fases 5-7, A8 − A7h,
emparejado), las secundarias, el gasto y los md5 de todo lo que jugaría y mediría.

## 4 · DECLARACIONES Y ARCHIVOS

- El humo de campo se hizo con la política subida (`--use-bedrock --bedrock-model us.anthropic.claude-haiku-
  4-5-20251001-v1:0`, `--secret-env GEMV_PUERTA6=1 GEMV_RZ_TOPE_USD=0.6`); el gasto de lenguaje del campo es
  el de la cabecera del sidecar (estimación de la plataforma, no factura). El de las dos llamadas del humo
  nativo con la clave no se guardó en archivo (tope propio 0,05 USD): queda declarado.
- Las instantáneas del banco son las de P6-25 (borrador de la sesión, fuera de git); los 8 diarios y zips
  de A8 (153 MB) están en el manifiesto con su md5, fuera de git; las respuestas crudas del razonador van
  dentro de los diarios (`razonador26.texto`).
- Un humo nativo con llamada real reveló dos defectos míos del arnés (el cable no esperaba al proceso juez
  ni iba a ritmo de reloj), corregidos antes de la imagen; la primera construcción falló por eso y se
  repitió.

| archivo | qué es |
|---|---|
| `sello_P6_26_banco.py` → `SELLO_P6_26_banco.md`, `P6_26_sello_banco.json` | el sello del banco, antes de correrlo |
| `banco_P6_26.py` → `P6_26_banco.json`, `P6_26_banco_juicios.json` | el barrido de todos los destinos y sus juicios |
| `texto_escena_P6_26.py`, `puerta_proceso_P6_26.py`, `policy_pareja26.py` | el brazo A8 |
| `humo_red_P6_26.py`, `Dockerfile.pareja26`, `lanza_P6_26.py`, `P6_26_brazos.json`, `P626_t1_*.json` | su humo, su imagen, el lanzador, la política subida, las dos partidas |
| `mide_P6_26.py` → `P6_26_humo.json`; `mide_pasos_P6_22.py` → `P6_26_pasos_humo.json`; `P6_26_pasos_atribucion.json` | las medidas del humo, los pasos perdidos y su atribución |
| `sello_P6_26_serie.py` → `SELLO_P6_26_serie_borrador.md`, `P6_26_sello_serie_borrador.json` | el borrador del sello de la serie, con el coste estimado y los md5 |
