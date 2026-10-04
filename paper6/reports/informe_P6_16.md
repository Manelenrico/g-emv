# P6-16 · El puente en el campo: el consejero de reglas con dos puertas

*27-sep-2026. Coste: **3,0065 USD** de 5 (2 partidas cortas de humo 0,0346 + 40 de
serie 2,9719; todas facturadas, ninguna fallida). `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; los 202
congelados del cinco y los 32 del seis: 0 alterados al principio y al final. La
puerta del cinco no se toca. Nada de MettaScope. Sin propuestas de diseño.*

**Lo nuevo, todo en archivos aparte y declarado:** `compromiso6_P6_16.py`
(versión nueva del compromiso de P5-8H), `policy_pareja16.py` (A5v/A5h),
`humo_red_P6_16.py`, `Dockerfile.pareja16`, `lanza_P6_16.py`, `sello_P6_16.py`
+ `SELLO_P6_16.md`, `humo_campo_P6_16.py`, `mide_P6_16.py`, `gif_P6_16.py`. El
oráculo (`oraculo_P6_14.py`) y la puerta6 (`puerta6_P6_15.py`) son los de P6-14
y P6-15, instrumentos declarados, no parte del cuerpo. Antes de nada: commit
local `4171f39` (P6-13/14/15, ACTA, manifiesto; JSON > 10 MB y GIF fuera).

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**El puente funciona como mecanismo y no salva vidas.** En A5h la puerta6
acepta 129 planes del oráculo (A5v: 3), compromiso6 los anda (682 pasos), 65
llegan a destino o a salvo… y las muertes por anillo evitables son **19, las
mismas que en A4** (A5v: 18). Lo que pasa después de andar: el cuerpo vuelve
al fuego (los mismos destinos se alcanzan tres y cuatro veces), el plan cae
porque «la vida real está por debajo de la proyectada» (32 veces: la puerta6
imagina más vida de la que hay), y el veto vital de las rupturas (armado a
tiro: 353) lo para dentro del anillo, donde están los rivales. Y entrar al
anillo tiene precio: las muertes por rivales pasan de 6 (A4) a 12 (A5h) y el
daño de rival por vida de 42 a 57. La pareja, en cambio, va **más** junta
(80,0 % contra 77,3 %; el criterio (c) es común y 16 planes los aceptan los
dos). El sello: 3 aciertos, 3 fallos, 1 no alcanzada y 1 con salvedad.

---

## 1 · QUÉ SE JUGÓ

Brazos con las 20 semillas de A4, mundo 0.1.19, `roster_lento_v2`, misma liga:

| brazo | cuerpo | puerta | compromiso | política |
|---|---|---|---|---|
| A4 | el cuerpo del seis, congelado | — (GEMV_FORMA=0) | — | `b4e322cf…` (P6-11, no se repite) |
| **A5v** | el mismo + oráculo en el campo | la del cinco, comparador `mejor_propia_H`, margen 0,062 | compromiso6 | `gemv-p6-A5v:v1` = `174f5e38-5117-43b8-ac6b-ad09c558b6b3` |
| **A5h** | el mismo + oráculo en el campo | la del cinco con el comparador de puerta6 (B, el cuerpo decidiendo paso a paso) | compromiso6 | `gemv-p6-A5h:v1` = `231f7434-9adf-46b3-b43d-03b112183d82` |

Una sola imagen (`gemv-anima:pareja16`, `sha256:41b78270…`, custodias del
motor, del decisor, de la tabla, del cinco y del cuerpo del seis dentro; los
diez humos anteriores y los dos nuevos pasan en el build); los dos brazos se
distinguen solo por `GEMV_PUERTA6` (0/1) pasado al subir, como los
interruptores de siempre.

**El oráculo en el campo** (`policy_pareja16.AlmaPareja16._oraculo16`): solo
desde el primer `warn` del calendario; momento (1): la casilla arde o arderá
antes de lo que tardo en salir más 33 tics; piernas listas; un plan a la vez
(ninguna forma viva ni pendiente) y como mucho uno cada 25 tics (declarado);
criterio (c) con el hermano vivo y localizable (visto, parte E2 fresco o la
memoria; mismo destino: la casilla segura que minimiza el máximo de pasos de
los dos), (b5) con uno solo; H 100. El plan se escribe en el idioma de formas,
lo traduce `traductor_forma.traduce` y entra por la vía del consejero
(`cf.entregado` → `_recoge` → `FormaViva(origen="consejero")` → `_juzga` en el
hilo → `_recoge_hilo`). **La puerta juzga en el hilo desde el primer juicio**
(`evalua_en_hilo = True`) y la reevaluación de las formas vivas también va al
hilo («revisa6», copia declarada de `_revisa_vivas` con el juicio encargado y
aplicado a la vuelta; en los dos brazos). Confianza C viva, como en el cinco.

**compromiso6** (`compromiso6_P6_16.py`), copia declarada de `_compromiso`
(P5-8H) con lo que fijó Manel y solo eso: (1) sin la comprobación de origen
(anda las formas del consejero); (2) el fin del plan es **estar a salvo**
(`a_salvo`: dentro del radio del tic y del radio final de la fase) o pisar el
destino, no ver nada —sin esto el tramo `esperar` tendría al cuerpo parado 100
tics—; (3) la ruptura (c) «daño en el tic» no cuenta el fuego del anillo; (4)
la ruptura (b) «cubre el camino» no aplica (usa `k_camino` del brazo K); (5) el
objetivo es el destino del tramo `ir` mientras el plan viva. (a) veto vital,
(d) vida/carencia y (e) rival cerca, el enfriamiento, el coste y `D._a_json`
son la copia literal. Mismo compromiso en A5v y A5h; sin brazo K.

### 1.1 El humo (§0), con partidas reales cortas por la vía real

Dos partidas reales (semilla 20260916, calendario del anillo al 20 %,
`max_ticks` 3.700; 0,0346 USD), una por brazo, antes de la serie. Y antes,
`humo_red_P6_16.py` en el build (200 observaciones reales por el cable,
calendario comprimido derivado por `Mundo.anillo_en`, un tic cada 1/24 s; en
los dos brazos: 5 propuestas, 0 antes del aviso, 5 juicios en el hilo y
vueltos, 0 en línea, mediana de decisión 1,1-1,6 ms, 5 de 200 por encima de un
tic; una forma dada como aceptada la anda compromiso6 con la acción emitida
igual al paso).

| humo de campo | A5v s10 | A5v s11 | A5h s10 | A5h s11 |
|---|---|---|---|---|
| propuestas antes del primer aviso (1.500) | **0** | 0 | **0** | 0 |
| propuestas después | 6 | 0 | 6 | 0 |
| juicios en el hilo / vueltos / en línea | 6 / 5 / **0** | — | 6 / 6 / **0** | — |
| ms por juicio (mediana) | 273 | — | **769** | — |
| decisión: mediana · p95 · máx (ms) | 1,3 · 8,7 · 256 | 1,4 · 8,8 · 26 | 1,3 · 11,3 · 289 | 0,9 · 4,7 · 12 |
| decisiones por encima de un tic (41,7 ms) | 6 de 2.928 | 0 | 11 de 2.546 | 0 |
| aceptadas · obedece · rupturas | 0 · 0 · 0 | — | **1 · 17 · 0** | — |

Los tres puntos del §0 se cumplen: el oráculo no se enciende fuera del
anillo; la puerta6 juzga en el hilo y ninguna evaluación corre en línea; el
plan aceptado se anda con compromiso (17 pasos, 58 esperas de enfriamiento, sin
ruptura por fuego). Lo que sí retrasa, medido: **el tic de la propuesta** (y el
de encargar la reevaluación) cuesta 200-260 ms = 5-6 tics, porque la puerta
del cinco copia en profundidad `mem` y `bloqueos` para el hilo (`_recoge`,
`policy_forma:1210`); 6 y 11 decisiones por vida (0,2-0,4 %). Se declaró y se
siguió con la misma imagen (cambiarla habría invalidado el humo).

### 1.2 El sello, antes de la primera partida

`SELLO_P6_16.md`, md5 **`cd1865a50896214b3e89d7e928ec74f7`**, escrito con
`sello_P6_16.py` desde `P6_15_planes.json` (margen 0,062) con la regla de
propuesta del campo, antes de las partidas de humo (§4, contrastado).

---

## 2 · LAS MEDIDAS, TRES COLUMNAS (20 semillas, 40 vidas por brazo)

Definiciones copiadas de P6-4/P6-7/P6-11/P6-13 (`mide_P6_16.py`; A4 se
recalcula con ellas y reproduce sus cifras: vida 12.839, juntos 77,3 %, 11
supervivientes, comida 2,88, 22 muertes por anillo, 19 evitables, clases ii 12
· i 8 · iii 1 · v 1).

| | **A4** | **A5v** (puerta del cinco) | **A5h** (puerta6) |
|---|---|---|---|
| muertes por anillo · **evitables** (fases 1-6) | 22 · **19** | 21 · **18** | 19 · **19** |
| clases (P6-13) de las de anillo | ii 12 · i 8 · iii 1 · v 1 | ii 15 · i 6 | ii 15 · i 4 |
| muertes por rivales · «no consta» | **6** · 1 | 9 · 4 | **12** · 4 |
| golpes de rival / vida · daño de rival / vida | 6,2 · **42,0** | 5,6 · 40,1 | 7,1 · **56,6** |
| supervivientes (de 40) | **11** | 6 | 5 |
| los dos vivos al final | **3** | 1 | 1 |
| vida media (tics) | 12.839 | **13.184** | 12.812 |
| juntos a ≤ 3 · ≤ 8 (% de tics con los dos vivos) | 77,3 · 98,4 | 75,0 · 98,0 | **80,0** · 98,1 |
| escapadas largas (> 8 casillas, ≥ 200 tics) · excursiones | 0 · 305 | 2 · 264 | 0 · 217 |
| comida por vida | 2,88 | **4,00** | 2,98 |
| tiempo ardiendo (tics con golpe del anillo) / vida | 9,4 | 10,7 | 8,9 |
| planes ofrecidos · **aceptados** | — | 576 · **3** | 335 · **129** |
| veredictos de la puerta (ok · area · vida) | — | 3 · 483 · 71 | 129 · 161 · 31 |
| pasos obedecidos (compromiso6) | — | 0 | **682** |
| andados hasta el destino · hasta estar a salvo | — | 1 · 2 | 28 · 37 |
| abandonados (forma caída), con el motivo | — | 0 | **59**: vida real < proyectada − 10 **32** · reevaluación «area» 19 · reevaluación «vida» 8 |
| otros cierres | — | — | sin cierre (acaba la partida) 4 · muere con el plan vivo 1 |
| rupturas del compromiso (tics) | — | veto vital 5 | **veto vital 353** · vida < 15 64 |
| (c) aceptado por los dos hermanos (mismo destino, ≤ 50 tics) | — | 0 | **16** |
| latencia: decisión mediana · p95 (ms) · tics > 1 tic | — | 1,8 · 7,5 · 631 de 508.159 | 2,0 · — · 531 de 493.258 |
| juicio en el hilo: mediana · p95 (ms) · encargados / vueltos | — | 299 · 1.333 · 576 / 557 | **664 · 2.175** · 335 / 321 (+152 reevaluaciones) |

**Emparejado por semilla** (A5x − A4; gana/pierde = semillas o vidas con más/menos):

| | A5v − A4 | A5h − A4 |
|---|---|---|
| vida (40 vidas) | +345 (15 / 23) | −28 (16 / 24) |
| juntos ≤ 3 (20 semillas) | +0,8 pp (12 / 8) | **+6,2 pp (13 / 7)** |
| los dos vivos al final | −0,1 (1 / 3) | −0,1 (1 / 3) |
| comida (40 vidas) | +1,1 (19 / 11) | +0,1 (19 / 12) |
| tics ardiendo (40 vidas) | +1,4 (20 / 17) | −0,5 (19 / 20) |
| escapadas largas | +0,1 (2 / 0) | 0 (0 / 0) |

Por semilla y asiento, las causas (`P6_16_medidas.json → por_semilla`): en 8
vidas A4 murió por el anillo y A5h no (`20260916` s10, `20260916` s11, `20365645` s10, `20889290` s10, `21098748` s10, `21098748` s11, `21203477` s11, `21831851` s10), pero solo 2 de esas 8 sobreviven (`20889290` s10, `21098748` s11): las
otras mueren por rivales o «no consta» antes. Y en 5 vidas A5h muere por el
anillo donde A4 no (`20365645` s11, `21622393` s10, `21622393` s11, `22146038` s10, `22146038` s11).

### 2.1 Qué pasó con los planes en las 19 muertes por anillo de A5h

En las ventanas de esas 19 muertes hubo **69 planes aceptados**: 30 andados
(15 al destino, 15 a salvo) y **39 abandonados**; 417 pasos obedecidos, 156
tics de veto vital, 59 de vida < 15. Tres cosas, medidas en `aceptados`:

1. **Llegar no basta.** `21203477` s10 llega a (28,23) dos veces (t 12.428 y
   12.594), `21622393` s10 a (23,28) tres veces, `20679832` s11 dos veces a
   (27,24): el plan se cumple, el cuerpo vuelve a su decisión (S-8, botín) y
   sale del radio otra vez; el siguiente plan llega tarde. Es la vuelta al
   fuego que P6-15 predijo (el paso a paso «arde 15 tics más que el real»).
2. **La puerta6 imagina más vida de la que hay.** 32 formas caen por «la vida
   real X está por debajo de la proyectada Y − 10» (regla del cinco,
   `falla_lo_previsto`): 40 contra 55, 26 contra 40, 8 contra 21, 21 contra 34…
   El rollout cobra el anillo por su regla, pero no los golpes ni la
   trayectoria real; cuando el cuerpo real va más lento o recibe golpes, la
   forma cae en el peor momento.
3. **El veto vital dentro del anillo.** 353 tics de «armado a tiro» (156 en las
   ventanas de muerte): dentro del radio están los rivales, y la ruptura (a)
   —la copia literal— para el paso mientras un armado está a su alcance.
   `21831851` s11: 5 aceptados, 0 pasos, 55 vetos, muere por el anillo.

### 2.2 Muertes por rivales: los planes meten al cuerpo en golpes

A5h: 12 muertes por rival (A4 6, A5v 9), 7,1 golpes y **56,6 de daño de rival
por vida** (A4 42,0). El rollout no modela ataques (declarado en P6-15) y el
plan lleva al cuerpo a casillas «seguras» del anillo que son las de los
rivales; el veto vital lo frena a medias (rompe el paso, no deshace el
camino). Con la puerta del cinco (A5v), que casi no acepta, el daño de rival
no sube (40,1).

### 2.3 Las aceptaciones que alejan del hermano, y sus consecuencias

A5h: **43** planes aceptados cuyo destino está más lejos del hermano que la
casilla del cuerpo (posición real del otro diario en ese tic). De ellos, **24
mueren en los 300 tics siguientes** (22 por el anillo, 2 por rival). La
separación que producen es pequeña: destino a 2-5 casillas del hermano (1-3
antes), y a los 100 tics la distancia vuelve a 1-4 en 15 de 15 con los dos
vivos. A5v: 1 aceptación que aleja (1 → 3), sin muerte. La pareja de A5h está
más junta que la de A4 (+6,2 pp emparejado, 13 semillas de 20) porque el
criterio (c) da el mismo destino a los dos: 265 de los 335 planes fueron (c),
y 16 los aceptaron los dos.

### 2.4 Latencia en la serie

La decisión del cuerpo no espera al juicio: mediana 1,8-2,0 ms; **631 de
508.159 tics (0,12 %) en A5v y 531 de 493.258 (0,11 %) en A5h** por encima de
un tic, todos en los tics de propuesta o de encargo de reevaluación (copia de
la memoria para el hilo), máximo 703 ms. El juicio en el hilo: A5v 299 ms
(p95 1,3 s), A5h **664 ms (p95 2,2 s)**: 2× lo medido en el banco (la CPU del
contenedor); 14 juicios de A5h y 19 de A5v no volvieron antes de acabar la
partida. Con 2 s de juicio, el veredicto llega 50 tics después de la propuesta.

---

## 3 · EL GIF

`P6_16_puente.gif` (115 fotogramas, 11.856 → 13.100; md5 en el manifiesto):
semilla `20889290`, A5h, asiento 10 —en A4 murió por el anillo en 13.008,
clase (ii); aquí sobreviven los dos—. Se ven las propuestas del oráculo
(«PROPONE»), los rechazos (aspa gris, «area»), los dos planes aceptados de la
fase 5 (estrellas verdes en (25,27) y (26,26): andados hasta estar a salvo con
6 vetos vitales cada uno), el hermano (naranja) al lado, y los rivales
contados dentro del radio.

---

## 4 · EL SELLO, CONTRASTADO

| predicción (SELLO_P6_16.md, `cd1865a5…`) | lo medido | |
|---|---|---|
| 1a. A5h tendrá MENOS muertes evitables por anillo que A4 y que A5v (techo del banco: 17 de 19 con plan aceptado a tiempo) | A5h **19** = A4 19; A5v 18 | **fallo** |
| 1b. A5v, las mismas que A4 o como mucho 1 menos | 18 contra 19 | acierta |
| 2. planes aceptados: del orden de 1 (A5v) contra 227 (A5h), menos en el campo | **3** contra **129** (43×) | acierta |
| 3a. «juntos ≤ 3» baja en A5h respecto a A4 (77,3) | **sube a 80,0** (+6,2 pp emparejado) | **fallo** |
| 3b. no cambia en A5v | 75,0 (+0,8 pp, 12/8) | acierta |
| 3c. las escapadas largas suben en A5h | 0 (A5v 2) | fallo (no alcanzada en A5h; A5v no predicho) |
| 4a. juicio A5h ~370 ms, A5v ~140 ms | 664 y 299 ms (CPU del contenedor 2×) | no alcanzada |
| 4b. la decisión del cuerpo no espera | 0,11-0,12 % de tics por encima de un tic, en los de propuesta | acierta, con esa salvedad |

Aciertos 3 (1b, 2, 3b), fallos 3 (1a, 3a, 3c), no alcanzada 1 (4a), con salvedad
1 (4b). El banco acertó en lo que la puerta hace (aceptar) y falló en lo que el
cuerpo hace después (volver al fuego, caer por la vida, pararse ante un armado),
que era justo lo que dijo que no podía predecir.

---

## 5 · LO QUE DICE LA MEDIDA (sin proponer nada)

1. El puente está montado y funciona como mecanismo: el oráculo propone solo
   en el anillo (576 y 335 propuestas), la puerta juzga en el hilo, compromiso6
   anda lo aceptado (682 pasos en A5h), y el compromiso de P5-8H sirve para
   una forma que viene de fuera del cuerpo: 65 planes llegaron.
2. **No salva vidas por el anillo**: 19 evitables en A5h, 19 en A4, 18 en A5v.
   Llegar a la casilla segura no es quedarse: el cuerpo vuelve a salir.
3. **La puerta6 imagina de más**: 32 caídas por vida real bajo la proyectada.
4. **El veto vital de las rupturas** (353 tics) es la ruptura que manda dentro
   del anillo; la (c) adaptada (sin fuego) no rompió ni una vez.
5. **Entrar tiene precio**: muertes por rival 6 → 12 y daño 42 → 57 en A5h.
6. **La pareja no se separa** con (c): +6,2 pp más junta, 16 planes aceptados
   por los dos; las 43 aceptaciones que alejan lo hacen 1-3 casillas y se
   deshacen en 100 tics.
7. La puerta del cinco tal cual (A5v) casi no acepta (3 de 576) y la vida sube
   345 tics emparejados (15/23) sin cambiar el anillo: ruido, no efecto.
8. Coste real del hilo: 664 ms por juicio en A5h, 2 s en el p95.

---

## 6 · ARCHIVOS

| archivo | md5 | qué es |
|---|---|---|
| `compromiso6_P6_16.py` | `a5e959b5ad9375636e8f7245441ba411` | compromiso6, versión nueva declarada |
| `policy_pareja16.py` | `10bc8a84a7931f2354478376af69ce6b` | la política A5v/A5h (oráculo, revisa6, compromiso6, puerta6 por `GEMV_PUERTA6`) |
| `humo_red_P6_16.py` | `012dbc9e03e05058bd60119b984d26f0` | humo de red del build |
| `Dockerfile.pareja16` | `2d9f2c389f39046981804b29fc342390` | la imagen (custodias + humos) |
| `lanza_P6_16.py` | `d650aa897b0ff1d0847d670d5e9eadbd` | tandas 0 (humo), 1 (A5v), 2 (A5h) |
| `sello_P6_16.py` · `SELLO_P6_16.md` | `bd182d03…` · **`cd1865a50896214b3e89d7e928ec74f7`** | el sello y su cálculo |
| `humo_campo_P6_16.py` · `P6_16_humo_campo.json` | `72c125c3…` · `e456e136…` | latencia, hilo, oráculo, compromiso por vida |
| `mide_P6_16.py` · `P6_16_medidas.json` | `25eb820a…` · `7d18a4fe…` | las tres columnas, por semilla, y los planes aceptados |
| `gif_P6_16.py` · `P6_16_puente.gif` | `98b0e12a…` · `5d4ac2faa314ea1bb7e0e0ab81164695` | el caso |
| `P6_16_brazos.json` · `P616_t*_peticiones.json` · `P616_t*_A5*_*.json` | — | políticas, peticiones y resultados (42 partidas) |
| diarios `paintball/runs/P616_t{0,1,2}_*` | en `DIARIOS_P6_MANIFIESTO.md` (168 filas) | fuera de git |
