# P6-22 · Los pasos que no llegan: el cinco, la causa y el arreglo

*28-sep-2026. Primero medir (coste cero): los diarios de todas las series del cinco, A5v del
seis, el bucle principal tic a tic y la prueba del intérprete. Después el arreglo, como
infraestructura, con banco de invariancia y humo: dos partidas reales cortas, **0,0260 USD**
de un tope de 0,5. Ninguna serie jugada. `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados del cinco y
los 32 del seis: 0 alterados al principio y al final. Lo nuevo, en archivos aparte y
declarado: `mide_pasos_P6_22.py` → `P6_22_pasos_cinco.json`, `P6_22_pasos_seis.json`,
`P6_22_pasos_humo.json`; `mide_gil_P6_22.py` → `P6_22_gil.json`; `mide_bucle_P6_22.py` →
`P6_22_bucle_{A4,A5v,A6,A6p}.json`; el arreglo `puerta_proceso_P6_22.py`;
`banco_fix_P6_22.py` → `P6_22_banco_fix.json`; `policy_pareja22.py`, `humo_red_P6_22.py`,
`Dockerfile.pareja22`, `lanza_P6_22.py`, `P6_22_brazos.json`. Ningún número se escribió antes
de calcularlo. Sin propuestas de diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**El cinco también perdió pasos, menos que el seis y en los brazos con la puerta: F (el
consejero de lenguaje con la puerta en el hilo) 5,5 / 8,0 / 11,1 % de los pasos listos hacia
casilla libre antes del aviso / fases 1-4 / fases 5-7 (la ampliación, 4,1 / 7,5 / 17,3 %); T
(formas de azar con la misma puerta) 2,0 / 3,5 / 5,3 %; K (curiosidad como forma) 9,3 / 11,7 /
8,9 %; Q (curiosidad sin puerta) 0,1 / 1,3 / 1,3 %; A (cuerpo solo) 0,0 % en todo.** Eso toca
las comparaciones de campo entre A, F y T de P5-6C y entre A y K de P5-8M (§1): el cinco no
puede subirse a Zenodo tal cual sin decirlo. **A5v pierde el 37,4 % en las fases 5-7** (A5h
40,8, A6 40,5): la puerta del cinco con su comparador ya bastaba. **La causa no es el bloqueo
del intérprete** (un hilo que calcula dobla la latencia del bucle de 9 a 18 ms y no pasa de
un tic; un proceso aparte no la toca): es lo que el propio hilo principal hace en los tics de
encargo: la copia profunda de la memoria y los bloqueos (12-73 ms) más el tic de propuesta
del oráculo (hasta 27 ms), con el juicio en el hilo (puerta6: 274 ms de mediana) encima.
**El cuerpo tiene 41,7 ms por tic** (1000 / 24). **El arreglo** (`puerta_proceso_P6_22`):
el juicio corre en un proceso aparte y el hilo principal solo hace una instantánea por
serialización (≈ 5 ms de memoria en el Mac, 14-20 en la plataforma). Con él, en el bucle
real con mundo que no espera, A6 pasa de 23,6 % de pasos perdidos a **0,0 %**, con los
mismos veredictos: el banco de P6-15 repetido con la instantánea da **38 vidas, 19.911 planes: 19.911 veredictos y ventajas idénticos (puerta del cinco, comparador real y rollout a 1, 6 y 11), 0 distintos, 0 sin pareja**. En las
dos partidas reales: **0,0 % de pasos perdidos hasta la fase 4 y 3,3 % (7 de 211) en las
fases 5-7**, los siete en el tic de una propuesta del oráculo o el siguiente; retraso de los
pasos dados: 0 tics en los 895. Lo que viene (§6): un razonador de segundos cabe en la misma
infraestructura si nunca toca el hilo principal; lo que no cabe es lo que aún hace el
oráculo en él.

---

## 1 · EL CINCO, ANTES DE NADA (`mide_pasos_P6_22.py`, la medida de P6-21)

Medida de P6-21, tal cual: **paso perdido** = paso enviado con las piernas listas hacia una
casilla libre (no sólida, sin cuerpo visto) al que el juego responde `ok` sin que la casilla
cambie ni las piernas dejen de estar listas; **fantasma** = respuesta `cooldown` o `blocked`
en un tic en que el cuerpo no había enviado un paso. Por brazo y por fase del anillo (antes
del primer aviso; fases 1-4; fases 5-7). Brazos del cinco: **A** cuerpo solo; **F**
consejero de lenguaje con la puerta (juicio en el hilo); **T** formas de azar con la misma
puerta; **Q** curiosidad como renglón (sin puerta); **K** curiosidad como forma con puerta y
compromiso.

| serie · brazo | partidas · vidas | antes del aviso 1 | fases 1-4 | fases 5-7 | fantasmas (5-7) |
|---|---|---|---|---|---|
| P5-6C · A | 20 · 40 | 1 / 18.038 (0,01 %) | 0 / 6.452 (0,0 %) | 0 / 892 (0,0 %) | 0 |
| P5-6C · F | 20 · 40 | 838 / 15.294 (**5,5 %**) | 378 / 4.715 (**8,0 %**) | 46 / 415 (**11,1 %**) | 3 |
| P5-6C · T | 20 · 40 | 355 / 17.476 (2,0 %) | 247 / 7.031 (3,5 %) | 70 / 1.317 (5,3 %) | 3 |
| P5-6C amp · F | 20 · 40 | 746 / 18.341 (4,1 %) | 416 / 5.521 (7,5 %) | 227 / 1.314 (**17,3 %**) | 19 |
| P5-6C amp · T | 20 · 40 | 403 / 16.046 (2,5 %) | 138 / 5.321 (2,6 %) | 18 / 463 (3,9 %) | 1 |
| P5-7C · A | 20 · 40 | 0 (0,0 %) | 0 (0,0 %) | 0 / 1.124 (0,0 %) | 0 |
| P5-7C · Q | 20 · 40 | 16 / 19.273 (0,1 %) | 90 / 7.202 (1,3 %) | 16 / 1.235 (1,3 %) | 8 |
| P5-8 · A (B-M) | 30 · 60 | 5 / 23.885 (0,0 %) | 1 / 8.730 (0,0 %) | 0 / 851 (0,0 %) | 0 |
| P5-8 · K (B-M) | 30 · 59 | 2.610 / 28.176 (**9,3 %**) | 1.228 / 10.463 (**11,7 %**) | 156 / 1.745 (**8,9 %**) | 8 |
| P5-6B (A, F, T, F2, C0F) | 5 · 10 | 239 / 5.030 (4,8 %) | 107 / 1.339 (8,0 %) | — | 0 |

(Los tres episodios B1, C2 y C3 —sondas del cinco, 6 vidas— pierden 0 de 3.355 (0,0 %) de sus pasos; la tanda descartada no se cuenta.) El retraso de
los pasos dados es 0 en la práctica en todos los brazos del cinco (máximo 9 tics en F, 8 en
K; menos del 0,1 % de los pasos con retraso ≥ 3).

**Qué afirmaciones del cinco toca.** Todo lo que compara **conductas en el campo** entre un
brazo que pierde pasos y otro que no, o entre dos que pierden distinto:

- `informe_P56C.md`, «La medida principal»: F 33/78 = 42,3 % contra T 22/36 = 61,1 %,
  diferencia −18,80 [−36,30, +0,86]; y «(a) La emparejada», «(b) La magnitud», «Vida» y
  el cotejo S6 (F−A, T−A, F−T, cero dentro). F perdía el doble de pasos que T y A ninguno:
  las formas de F se andaron con un cuerpo que no llegaba a tiempo. El **acta** de P5-6C
  («0 tics perdidos en 1.501.210 tics vivos»; «tics > 40,5 ms: F 0,215 %») medía otra cosa:
  observaciones sin procesar y decisiones lentas, no pasos que el juego no ejecutó.
- `informe_P58M.md`, K1 (K/A 1,11-1,23 de vida, «dentro/fuera» 5,20×), K2 («K se acerca
  menos a los armados», 6-3-1 semillas), «El compromiso» (obedece 92,6 %: obedecer es
  emitir, no dar el paso) y K6 (5,5 ms por tic sin tics perdidos). K perdía 9-12 % de sus
  pasos en todas las fases.
- `informe_P57C.md`: Q perdía 0,1-1,3 %; Q5 («0 tics perdidos») sigue siendo otra medida.
  El hallazgo de P5-7C (la curiosidad no explora más) no se apoya en pasos.
- Lo que **no** toca: todo lo de banco (seco) del cinco, la puerta como mecanismo de
  aceptación, y las cifras de A.

**Sobre Zenodo:** tal cual, no. Las comparaciones de campo A/F/T y A/K llevan un defecto de
instrumental medible y no declarado. Lo que se declara aquí (esta tabla y la causa de §3)
es lo que habría que añadir; la decisión es de Manel.

## 2 · A5v EN EL SEIS

| brazo | antes del aviso 1 | fases 1-4 | fases 5-7 | fantasmas (5-7) · retraso mínimo mediana |
|---|---|---|---|---|
| A3 | 0,01 % | 0,0 % | 0 / 4.697 (0,0 %) | 0 |
| A4 | 0,01 % | 0,04 % | 0 / 4.215 (0,0 %) | 0 |
| **A5v** (puerta del cinco, comparador del cinco) | 0,02 % | 611 / 11.364 (5,4 %) | **2.299 / 6.144 (37,4 %)** | 1.089 · 2-3 tics |
| A5h (puerta del cinco, comparador puerta6) | 0,01 % | 4,0 % | 2.292 / 5.612 (40,8 %) | 878 |
| A6 (A5h + ir y quedarse) | 0,01 % | 6,6 % | 3.160 / 7.802 (40,5 %) | 1.220 |

A5v pierde casi lo mismo que A5h y A6: **el comparador de puerta6 (274 ms de rollout por
juicio) no es lo que tira los pasos; la puerta del cinco tal como se encarga y el oráculo
bastan**. El corte entre fases 1-4 y 5-7 es el oráculo: solo propone desde el primer aviso
y, desde el aviso 5, cada 25 tics con planes vivos.

## 3 · LA CAUSA (`mide_gil_P6_22.py`, `mide_bucle_P6_22.py`)

**Cuánto tiene el cuerpo por tic: 1000 / 24 = 41,67 ms** (`tick_rate` 24 del
`player_config`). El juego resuelve en cada tic la primera acción que le llega y descarta las
demás sin respuesta (`sim.nim`, `submitAction`; P6-21). Si un tic del bucle tarda más de 41,7
ms, la observación siguiente ya está en la cola, se decide enseguida y su acción cae en el
mismo tic del servidor que la anterior: **una perdida por cada tic que se pasa**.

### 3a · ¿Es el bloqueo del intérprete? (prueba directa, sin partidas)

Bucle principal = `alma.decidir` del cuerpo A4 sobre observaciones reales de A6 (semilla
20679832, asiento 10, desde el aviso 5), a 24 por segundo; latencia desde que toca el tic
hasta que la decisión está (720 tics por condición). Copia profunda de la memoria: 9,3 ms;
ida y vuelta por `pickle`: 1,7 ms (106 KB).

| condición | mediana | p90 | p99 | máx | tics > 41,7 ms |
|---|---|---|---|---|---|
| a) solo | 8,98 ms | 11,2 | 12,9 | 17,5 | 0 |
| b) con un HILO de Python calculando sin parar (copias profundas) | **18,4** | 24,7 | 25,6 | 31,2 | 0 |
| c) con un PROCESO aparte calculando lo mismo | 6,0 | 6,1 | 6,6 | 8,2 | 0 |
| d) el bucle principal copia la memoria cada 25 tics (`_recoge` / `_revisa_vivas`) | 8,9 | 11,2 | 48,4 | 50,3 | **21 (2,9 %)** |

El hilo **dobla** la latencia (el intérprete se reparte) pero no la saca del tic; el proceso
no la toca; lo que sí saca tics del reloj es **lo que el hilo principal hace por sí mismo**.

### 3b · El bucle real, tic a tic, con un mundo que no espera

El bucle real del cliente (`policy_cortex.decisor`) con un WS falso que entrega las
observaciones grabadas de un diario a 1/24 s de reloj de pared **sin esperar al cuerpo** (se
acumulan como en la red) y anota en qué tic de reloj cae cada acción: dos acciones en el
mismo tic = una perdida. Bucle abierto (posiciones grabadas). Diario: A6 20679832 asiento
10, tics 11.400-12.888 (1.489 tics, 62 s), el mismo para los cuatro brazos.

| | A4 | A5v | A6 | **A6p (arreglo)** |
|---|---|---|---|---|
| acciones perdidas | 1 (0,1 %) | 34 (2,3 %) | 122-136 (8,2-9,1 %) | **0** |
| pasos (`move`) perdidos | **0 (0,0 %)** | 26 (9,5 %) | 64-65 (**23,3-23,6 %**) | **0 (0,0 %)** |
| acciones tarde (≥ 1 tic) | 1 | 36 | 133-150 (hasta 9 tics) | 0 |
| espera en cola, p99 · máx (ms) | 1,6 · 74,8 | 48 · 65 | 191-237 · 291-389 | 1,4 · 7,2 |
| `decidir`, mediana · p99 · máx (ms) | 3,7 · 11,6 · 18,5 | 3,9 · 83,7 · 103,2 | 3,8-4,5 · 77-80 · 103-105 | 3,4 · 24,5 · **39,3** |

Las piezas, en el hilo principal (ms por llamada, mediana · máx, y total en los 62 s):

| pieza | A5v | A6 | A6p |
|---|---|---|---|
| copia profunda de `mem` + `bloqueos` (`_recoge`, `_revisa_vivas`) | 38 llamadas · 21,2 · 60,5 · 935 ms | 48 · 12,6 · 72,8 · 1.192 ms | **0** (instantánea: 20 · 10,4 · 17,1 ms; `mem` 271 KB ≈ 5 ms, `mundo` 269 KB ≈ 4 ms una sola vez) |
| oráculo por tic (`_oraculo16`; `seguras` 6 ms por llamada, ~600 llamadas) | 3.700 ms · máx 28,7 | 3.949 ms · máx 27,1 | 3.949 ms · máx 27,1 (sin tocar) |

Y en el hilo (o el proceso): la evaluación entera de la puerta del cinco 37 ms de mediana
(su comparador 5,6 ms); con puerta6, 316 ms (el rollout 274 ms). El hilo está ocupado 8,1 s
de los 62 en A6 y mientras tanto `decidir` no sube (4,3 ms de mediana): lo que se pasa de
tic son los tics de encargo, con el hilo libre (p99 de `decidir` con el hilo libre: 83 ms).

**La causa, en orden:** (1) la copia profunda en el hilo principal en cada encargo y
reevaluación (cada 25 tics con plan vivo), 12-73 ms; (2) el tic de propuesta del oráculo
(BFS + `seguras` + traductor), hasta 27 ms, que coincide con (1); (3) el reparto del
intérprete con el hilo, que dobla lo que dura el resto. En la plataforma, más lenta que el
Mac (las instantáneas tardan allí 14-20 ms de mediana contra 10), lo mismo pesa el doble.

## 4 · EL ARREGLO, COMO INFRAESTRUCTURA (`puerta_proceso_P6_22.py`)

Versión nueva, declarada; no toca el cuerpo congelado ni la puerta del cinco: los importa.
`AlmaPareja22` = `AlmaPareja18` con dos métodos rehechos (`_recoge` del cinco y
`_revisa_vivas` de P6-16) sin la copia profunda: el encargo lleva una **instantánea por
serialización** (`pickle`, en C) de la memoria, los bloqueos, la observación, la forma y el
estado que `_juzga` lee (tic, confianza, lo dicho por el hermano), y va a un **proceso
aparte** («el juez») con un alma espejo: mismo código, mismos arreglos, mismos ganchos
(puerta6), que ejecuta `_juzga` tal cual y devuelve (veredicto, ventaja, curva, tics) por una
cola que el bucle recoge cuando pasa. Misma interfaz que el hilo (`encarga`/`recoge`).

**No cambia ninguna decisión**, comprobado de dos maneras:

1. **El banco de P6-15 repetido con la instantánea en lugar de la copia profunda en todo el
   proceso** (`banco_fix_P6_22.py`: `copy.deepcopy` = `pickle` ida y vuelta, y
   `banco_P6_15.vida` tal cual), comparado plan a plan con `P6_15_planes.json` (veredicto y
   ventaja de la puerta del cinco, del comparador real y del rollout a 1, 6 y 11):
   **38 vidas, 19.911 planes: 19.911 veredictos y ventajas idénticos (puerta del cinco, comparador real y rollout a 1, 6 y 11), 0 distintos, 0 sin pareja**.
2. **El bucle real, A6 contra A6p sobre el mismo diario**: los juicios que caen en el mismo
   tic dan el mismo veredicto y la misma ventaja a cinco decimales (ids 1-7 de la ventana);
   los que caen en tics distintos (porque el veredicto anterior vuelve uno o dos tics antes
   con el proceso y el siguiente encargo se adelanta) dan ventajas distintas por juzgar otra
   observación, no otra regla: 21 registros en A6, 20 en A6p, 9 idénticos, el resto
   desplazados 1-4 tics. Declarado.

## 5 · HUMO: DOS PARTIDAS REALES CORTAS (`lanza_P6_22.py`, 0,0260 USD)

Imagen `gemv-anima:pareja22` (= `Dockerfile.pareja18` + el arreglo, la política
`policy_pareja22.py` y `humo_red_P6_22.py`; custodias del motor, del decisor, de la tabla y
de las piezas del seis dentro; el humo de red corre en el build sin la prueba de reloj, que
bajo emulación amd64 no mide nada). Política `gemv-p6-A6p:v1`
(`543b8e91-c50c-4fa2-9eae-b1b7007e4a46`). Mundo corto de P6-18 (calendario al 20 %,
`max_ticks` 3.700), semillas 20260916 y 20365645, roster lento v2. Las dos llegaron a la
fase 7 (última fase cerrada en el tic 3.380; finales en 3.289-3.481: un `match_over` con
puestos 1 y 2, dos eliminados). El juez en su proceso: 24 encargos (12 juicios y 12 reevaluaciones) y 23 veredictos de vuelta (uno en vuelo al acabar), 0 errores;
propuestas del oráculo 3 / 0 / 6 / 6 por asiento; veredictos `ok` y `area`; `obedece` 9.

| fase | pasos listos a casilla libre | perdidos | fantasmas | retraso de los pasos dados |
|---|---|---|---|---|
| antes del aviso 1 | 359 | **0 (0,0 %)** | 0 | 361 pasos, todos 0 tics |
| fases 1-4 | 312 | **0 (0,0 %)** | 0 | 328, todos 0 |
| fases 5-7 | 211 | **7 (3,3 %)** | 1 | 206, todos 0 |

A4 en el campo: 0,0 %. Antes de la fase 5, al nivel de A4. En las fases 5-7 quedan 7 pasos
perdidos: **los siete en el tic de una propuesta del oráculo con su encargo (ms16 45-80 ms
en la plataforma) o en el tic siguiente**; en los tics sin propuesta, ninguno. La
distribución del retraso por tic, con el arreglo: 0 tics en los 895 pasos dados. `cadencia_ms`
por asiento: mediana 0,65-0,84 ms, p95 2,8-4,4, máximo 12-71.

Lo que queda, pues, no es la puerta: es el tic en que el oráculo propone (BFS de casillas
seguras, traductor, instantánea de 270 KB), que en la plataforma roza o pasa los 41,7 ms.

## 6 · LO QUE VIENE: RAZONADORES DE SEGUNDOS

Un razonador de lenguaje tardará segundos, no milisegundos. Lo que esta infraestructura ya
da: el cuerpo no espera nada que corra fuera de su hilo, sea un juicio de 300 ms o una
respuesta de 5 s; el proceso recibe una instantánea y devuelve por la cola cuando puede.
Lo que **no** da todavía, medido aquí:

- Todo lo que siga corriendo en el hilo principal se paga tic a tic: el oráculo cuesta hoy
  hasta 27 ms (Mac) en su tic de propuesta y es la única fuente de pasos perdidos que queda.
  Un razonador que proponga desde el proceso, no desde el bucle, no añade nada al tic.
- Una instantánea de 270 KB cuesta 5 ms aquí y 14-20 en la plataforma; con varias por
  segundo se notaría. Con segundos de latencia, una por propuesta basta.
- Lo que vuelve tarde vuelve a un mundo que ya cambió: en el bucle real los juicios que
  vuelven uno o dos tics antes o después ya cambian qué observación se juzga (§4.2). Con
  segundos, la respuesta será sobre un mundo de cien tics atrás; el mecanismo del cinco
  (puntos de control, reevaluación cada 25 tics) es el que la contrasta con el presente, y
  no se ha medido con retrasos de esa escala.
- El proceso es uno; dos razonadores (uno por hermano) son dos procesos, uno por cuerpo,
  cada uno con su instantánea; el canal entre ellos ya existe (el parte).

Sin propuestas de diseño.

## 7 · ARCHIVOS

| archivo | qué es |
|---|---|
| `mide_pasos_P6_22.py` → `P6_22_pasos_cinco.json`, `P6_22_pasos_seis.json`, `P6_22_pasos_humo.json` | la medida de P6-21 por brazo y fase: el cinco (11 grupos), el seis (A3, A4, A5v, A5h, A6) y el humo |
| `mide_gil_P6_22.py` → `P6_22_gil.json` | la prueba del bloqueo del intérprete |
| `mide_bucle_P6_22.py` → `P6_22_bucle_{A4,A5v,A6,A6p}.json` | el bucle real con mundo que no espera, por tic y por pieza; veredictos para comparar |
| `puerta_proceso_P6_22.py` | el arreglo: instantánea + proceso juez + `AlmaPareja22` |
| `banco_fix_P6_22.py` → `P6_22_banco_fix.json` | el banco de P6-15 repetido con la instantánea, plan a plan |
| `policy_pareja22.py` · `humo_red_P6_22.py` · `Dockerfile.pareja22` · `lanza_P6_22.py` · `P6_22_brazos.json` · `P622_t0_*.json` | la política A6p, su humo (con la prueba de reloj), la imagen, el lanzador y las dos partidas |
| `DIARIOS_P6_MANIFIESTO.md` | los 4 diarios del humo con su md5 (fuera de git) |
