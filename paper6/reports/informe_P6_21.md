# P6-21 · ¿Entiende el cuerpo «estar dentro» igual que el juego?

*28-sep-2026. Comprobación estrecha, coste cero, sin arreglar nada: solo lectura de los
200 diarios del mundo del seis (§1) y de los 120 de A4, A5h y A6 (§3, §4), más el código
del juego (`sim.nim`, la copia de `~/paintball_recon/docs/zero-sum/src/`). `motor/model.py`
= `1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados del cinco
y los 32 del seis: 0 alterados al principio y al final. Lo nuevo, en archivos aparte y
declarado: `mide_anillo_P6_21.py` → `P6_21_anillo.json`; `mide_choque_P6_21.py` →
`P6_21_choque.json`; `mide_camino_P6_21.py` → `P6_21_camino.json`; `mide_quieto_P6_21.py`
→ `P6_21_quieto.json`; `mide_retraso_P6_21.py` → `P6_21_retraso.json`;
`mide_fantasma_P6_21.py` → `P6_21_fantasma.json`. Ningún número se escribió antes de
calcularlo. Sin propuestas de diseño. Pase lo que pase, lo siguiente son los razonadores.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**Sí, salvo en dos detalles pequeños; y el borde quema por otra razón.** El juego quema la
casilla cuya distancia euclídea desde (x, y) a (24, 24) es **estrictamente mayor** que un
radio **entero** (el de la observación, `zona.radius`, que es el radio lineal redondeado
hacia arriba), una vez cada 24 tics y multiplicado por 0,82 (atletismo 6); con radio 0
quema todo, incluido el centro. Esa regla explica los 1.980 golpes y las 3.031 estancias
seguras de los 200 diarios sin excepción. El cuerpo congelado, el oráculo y la proyección
usan la misma distancia y la misma comparación, pero con el radio **lineal, con decimales**:
en el encogimiento creen que una casilla arde hasta media casilla **antes** de que el juego
la queme (conservador: 1.692 / 1.748 / 2.713 tics en A4 / A5h / A6 desde el aviso 5) y, con
radio 0, creen seguro el centro cuando el juego lo quema (37 / 133 / 353 tics quietos con
`noop`; 1 / 5 / 12 golpes; **ninguna** de las 22 muertes por anillo de A4). Fuera de eso,
**ni un tic** en que el cuerpo dé por segura una casilla que el juego queme. Las 22 muertes
de A4: 21 en casillas que el cuerpo sabía que ardían (vida 0-10, `noop`, mediana 4 tics en la
casilla) y 1 en una casilla que no ardía, con 1 punto de vida tras el golpe anterior. El borde
quema por esto: en A5h y A6, desde el aviso 5, **el 41 % de los pasos enviados con las piernas
listas a una casilla libre no se dan** (A4: 0,5 %), y el juego resuelve pasos que el cuerpo ya
no está enviando (878 / 1.220 «fantasmas», llegados 3 tics tarde de mediana, hasta 21): las
acciones de A5h y A6 llegan tarde al mundo en las fases finales, y el cuerpo «obedece ir» en la
casilla del borde sin que el paso se ejecute. La proyección sí cuenta el fuego del camino
(`proyeccion.py:205-216`), pero imagina el primer paso en el primer tic: imagina 37,6 puntos
de fuego en los 74 planes de A6 y el cuerpo real recibe 610 siguiendo el plan.

---

## 1 · LA REGLA DEL JUEGO, MEDIDA EN LOS HECHOS (`mide_anillo_P6_21.py`)

200 diarios, tics desde el primer aviso. Hechos por tic: casilla, radio de la observación
(`zona.radius`, entero) y `next_radius`, radio lineal del calendario (`mundo.anillo_en`),
golpe del anillo (`damage_taken` con `source` zone).

- **Cadencia y daño.** 1.980 golpes; entre golpes consecutivos 24 tics (1.454 veces; 48, 72…
  cuando el cuerpo entra y sale). Daño por golpe: 6,56 (1.362), 4,92 (263), 13,12 (156),
  3,28 (112), 19,68 (86) = **0,82 × daño/s de la fase** (8, 6, 16, 4, 24). El código lo
  confirma: `sim.nim:1001-1010` (`resolveHazards`: `tick mod 24 == 0`; `hazardScaled` =
  daño × (100 − 3 × atletismo) / 100, `sim.nim:149-151`; atletismo 6 → 0,82).
- **Radio.** `zona.radius` − radio lineal ∈ [0, 1): 0,0 en 614.844 tics (fuera del
  encogimiento) y positivo en el encogimiento. Es el radio de `sim.nim:320-334`:
  `r = rStart − floor((t − shrinkT)·(rStart − rEnd)/(doneT − shrinkT))`, entero, igual al
  radio lineal **redondeado hacia arriba**.
- **Distancia y comparación.** Se probaron 4 distancias × 8 radios × 2 comparaciones contra
  los 1.980 golpes y las 3.031 estancias seguras (≥ 25 tics en la misma casilla sin golpe,
  con radio observado constante). Con distancia euclídea desde (x, y) a (24, 24) y «quema si
  d > radio observado»: **0 estancias seguras que quemaría y 22 golpes sin explicar**; con
  «d ≥ radio»: 0 golpes sin explicar y 27 estancias (todas a d = radio, hasta 198 tics sin
  arder). Los 22 golpes «sin explicar» son **todos en (24, 24) con radio 0** (fase 7,
  19,68 por golpe). Es exactamente `sim.nim:344-353` (`insideZone`): `if r <= 0: return
  false` («sin casilla segura tras la última etapa») y `dx² + dy² ≤ r²` con `dx = x − 24`.
  Chebyshev y Manhattan fallan por centenares. **Casos que no encajan con la regla
  completa: 0.**
- **Radio de qué momento.** El daño del tic T se calcula con el radio de T y se ve en la
  observación de T + 1; `zona.radius` en T + 1 es el radio de T + 1. Con «obs(t)» y con
  «obs(t−1)» el ajuste es el mismo (22 y 22, los del radio 0): no hay golpe en el que
  importe la diferencia.

## 2 · LAS REGLAS NUESTRAS (archivo y línea)

| pieza | regla de «a salvo» | dónde |
|---|---|---|
| cuerpo congelado, F-ANTICIPACIÓN | «arde ahora» si `d > radio_ahora` con `radio_ahora` = radio **lineal** de `anillo_en(tick)`; lo demás son los instantes futuros en que el radio lineal baja de d | `paintball/alma/mundo.py:280-309` (`eventos_arde`), `311-333` (`anillo_en`: `radio = r0 + (r1 − r0)·f`); `appraisal_zs_v42_exp.py:975-1000` (y `appraisal_zs.py:890-915`, idéntico) |
| cuerpo congelado, foto prevista | `zone.radius` = el radio lineal de `anillo_en(tick_eval)` | `paintball/alma/decisor_zs.py:357-360` |
| cuerpo congelado, candidato `ir_centro` | destino = el centro de `anillo_en(tick)`, (24, 24) | `paintball/alma/decisor_zs.py:465-468` |
| oráculo | `a_salvo(q, t)` = no sólida **y** `d ≤ radio lineal(t)` **y** `d ≤ r1` de la fase activa; `arde(pos, t)` = `dps > 0 y d > radio lineal(t)` | `cantera/paper6/oraculo_P6_14.py:123-131`, `69-71`, `53-55`, `65-67` |
| proyección (puerta6, curva del plan, puerta6g) | por tic imaginado: `_c, radio, dps = anillo_en(t)`; si `d > radio`: `hp −= dps / tick_rate` | `cantera/paper5/proyeccion.py:205-216` (`_proyecta` §4), usado por `proyectar_rapido` (`104-114`) y por `forma.curva_H` (`cantera/paper5/forma.py:655-683`) y `puerta6_P6_15.curva_real` (`48-`) |

Todas usan `math.dist((x, y), (24, 24))` y «mayor que»: la geometría y la comparación son
las del juego. La diferencia está en el radio: **lineal con decimales** en las nuestras,
**entero redondeado hacia arriba** en el juego; y en el radio 0: el juego quema todo, las
nuestras dejan «a salvo» d = 0 (`0 > 0` es falso; el oráculo además exige `d ≤ r1 = 0`).

## 3 · EL CHOQUE (`mide_choque_P6_21.py`; tics desde el aviso 5)

| | A4 | A5h | A6 |
|---|---|---|---|
| tics vivos desde el aviso 5 | 60.376 | 48.971 | 70.728 |
| el juego quema (por su regla) · golpes | 8.229 · 318 | 7.497 · 302 | 7.567 · 298 |
| **cuerpo: segura y el juego quema** | **37** | **133** | **353** |
| … de ellos con radio 0 | 37 | 133 | 353 |
| … golpes recibidos así | 1 | 5 | 12 |
| cuerpo: arde y el juego no quema (todos en encogimiento) | 1.692 | 1.748 | 2.713 |
| oráculo: a salvo y el juego quema | 37 | 133 | 353 |
| oráculo: no a salvo y el juego no quema | 24.823 | 22.225 | 28.419 |
| **quieto en casilla que creía segura mientras quemaba** | **37** (`noop` 37) | **133** (`noop` 131) | **353** (`noop` 346) |

El único choque en la dirección peligrosa (segura para el cuerpo, quemada por el juego) es
el **radio 0**: el cuerpo quieto en el centro en la fase 7, con `noop`, mientras el juego lo
quema a 19,68 por golpe. La cifra del oráculo «no a salvo y el juego no quema» no es un
error: `a_salvo` exige además `d ≤ r1` (que la casilla siga a salvo al acabar la fase), por
diseño (P6-14).

**Las 22 muertes por anillo de A4** (definición de P6-16, `P6_18_campo.json`): 21 en
casillas que el juego quemaba **y el cuerpo sabía que ardían** (d > radio lineal), con vida
0-10, elegido `noop` en el último tic, mediana 4 tics en la casilla (1 a 199); fases 5: 13,
6: 5, 7: 3, 4: 1. **1** (semilla 21098748, asiento 10, tic 14143) en (22, 24), d = 2 con radio
3: ni el juego la quemaba ni el cuerpo la creía ardiendo; había recibido 19,68 en (21, 23)
(d = 3,16 > 3, ardiendo para los dos) seis tics antes y le quedaba 1 punto; el golpe mortal no
consta en el diario. **Ninguna muerte con radio 0 ni en el centro.**

### 3a · Por qué arde entonces el borde: los pasos que no se dan

En P6-20 el cuerpo «obedece ir» tic tras tic en (30, 23) (d = 6,08, radio 6) sin moverse.
Traza (A6, semilla 20679832, asiento 10): del tic 12463 al 12502 envía `move SW` 30 veces,
`SE` 6 y `NE` 4, con `move_ready_in` 0, y el juego responde `ok` a todas sin que la casilla
cambie; en 12503 aparece en (29, 24) (el `SW` enviado por última vez en 12492) y en
12504-12512 el juego responde `cooldown` a acciones `none`. El código del juego lo explica:
resuelve **la primera acción que le llega en cada tic** y descarta las demás sin respuesta
(`sim.nim:523-527`, `submitAction`); `ok` es provisional y solo lo cambian los resolutores
(`sim.nim:1339-1340`); un tic sin acción pendiente conserva la respuesta anterior. Un paso
`ok` que no mueve con las piernas listas es un paso que el juego **no tuvo como pendiente**:
llegó tarde, en un tic que ya tenía otra.

Medido en los 120 diarios (`mide_quieto_P6_21.py`, `mide_fantasma_P6_21.py`):

| desde el aviso 5 | A4 | A5h | A6 |
|---|---|---|---|
| pasos enviados con piernas listas a casilla libre (no sólida, sin cuerpo visto) | 4.215 | 5.612 | 7.802 |
| dados en el tic | 4.196 | 3.144 | 4.422 |
| **perdidos** (`ok`, sin moverse, piernas listas) | **0 (0,0 %)** | **2.292 (40,8 %)** | **3.160 (40,5 %)** |
| **fantasmas** (`cooldown`/`blocked` sin paso enviado en t−1) | 0 | 878 | 1.220 |
| retraso mínimo de los fantasmas (mediana · p90 · máx, tics) | — | 2 · 6 · 37 | 3 · 7 · 21 |
| vidas con pasos perdidos (de 40) | 3 | 34 | 37 |
| lo mismo en las fases 1-4: perdidos | 5 (0,0 %) | 434 (1,6 %) | 774 (2,9 %) |

Los pasos «no dados» por otras causas se distinguen porque el juego los nombra: contra el
hermano (`blocked`, 96 % de los intentos, en todas las fases y brazos: el cuerpo empuja al
hermano) o contra un rival visto (`blocked`, 90-97 %). Los perdidos son solo los `ok`.

Lo que dice la medida: el cuerpo congelado (A4) da todos sus pasos en el tic; **A5h y A6
pierden 4 de cada 10 en las fases finales**, cuando funcionan el hilo de evaluación, el
oráculo y el compromiso (lo único que los separa de A4), y casi ninguno antes. Con el paso
perdido, el cuerpo sigue en la casilla del borde que ya había decidido dejar: por eso arde
«obedeciendo». En A6 desde el aviso 5, de los 2.118 tics en que envía un paso estando
ardiendo, en 1.155 (55 %) no se mueve. El reparto exacto del retraso entre hilo, oráculo y
compromiso no se ha medido (no hay reloj de pared en los diarios; `cadencia_ms` del registro
final mide solo el cómputo de cada tic: en el diario de la traza, mediana 1,6 ms, máximo 364).

## 4 · EL FUEGO DEL CAMINO (`mide_camino_P6_21.py`)

La curva proyectada **sí** cuenta el fuego de la casilla actual y del tramo de ir
(`proyeccion.py:205-216`: en cada tic imaginado, si d > radio lineal, resta dps/24). Lo que
imagina y lo que pasa, con la proyección congelada de verdad (`proyectar_rapido` sobre
`estado_de` del tic en que nació cada plan, tramo a tramo como `curva_H`) en los 74 planes
de la fase 5 de A6:

| | valor |
|---|---|
| planes que nacen en casilla ardiendo según la proyección · según el juego | 64 · 49 |
| planes en que la proyección imagina algún fuego | 10 |
| fuego imaginado total · en el primer control | 37,6 · 37,6 |
| fuego real recibido **siguiendo el plan** (sin ruptura abierta) hasta la caída o el último control | **610,1** (56 planes; 47 con 0 imaginado) |
| fuego real desviado | 223,0 |
| la Y de las 47 caídas por «vida real bajo la proyectada» coincide con la curva recalculada | 47 de 47 |
| tics entre nacer y aceptarse (el hilo) · mediana · p90 · máximo | 22,5 · 46 · 69 |

La proyección no se equivoca de regla: imagina que el cuerpo da el primer paso **en el
primer tic** (todos nacen con `move_ready_in` 0) y entra en el círculo en 11 tics, así que
55 de los 64 que nacen ardiendo imaginan 0 fuego. El cuerpo real tarda 22 tics de mediana en
aceptar el plan (el hilo) y luego pierde 4 de cada 10 pasos (§3a): recibe 610 puntos de fuego
«siguiendo» un plan que imaginaba 38. Ese es el hueco de −13/−14 de P6-20 (dos golpes de
6,56): no está en la regla del anillo, está en que el cuerpo imaginado se mueve y el real no.

## 5 · VEREDICTO (sin propuestas de diseño)

**(c) No hay error en la regla de «dentro», y el borde quema por otra razón**, con dos
detalles declarados:

1. **Detalle heredado del cuerpo congelado (y compartido por el oráculo y la proyección),
   sin efecto en las cifras del capítulo:** el radio lineal con decimales contra el entero
   redondeado hacia arriba del juego. Es conservador (cree que arde antes de que queme:
   1.692-2.713 tics por brazo desde el aviso 5; en ninguno el juego quema una casilla que el
   cuerpo dé por segura). Y con radio 0 el cuerpo cree seguro el centro cuando el juego quema
   todo: 37 / 133 / 353 tics quietos, 1 / 5 / 12 golpes, 0 de las 22 muertes por anillo de A4.
   Ninguna cifra de P6-13 a P6-20 cambia: las medidas de «dentro» y «ardiendo» de P6-17 y
   P6-18 se hicieron con el radio observado y con la distancia euclídea, que es la regla del
   juego; un cuerpo a menos de media casilla del radio (por ejemplo (29, 22), d = 5,39 con
   radio 5, donde mueren dos cuerpos de A4) arde para el juego y para el cuerpo.
2. **La razón por la que el borde quema:** en A5h y A6, en las fases finales, el 41 % de los
   pasos listos hacia una casilla libre no se dan y el juego resuelve pasos atrasados 3 tics
   de mediana (hasta 21): las acciones llegan tarde al mundo. En A4 no ocurre (0 de 4.215).
   Lo que los separa es el instrumental del seis (hilo, oráculo, compromiso). El cuerpo
   «obedece ir» en el borde porque su paso no se ejecuta; la curva proyectada, que imagina el
   paso en el primer tic, promete una vida que el cuerpo real no puede cumplir: 610 puntos de
   fuego siguiendo el plan contra 38 imaginados en los 74 planes de A6.

Lo que esto cambia en la lectura del capítulo: las caídas «sin desviación» de P6-20 (24 de
47) y el «llegar no es quedarse» de P6-18 no son de la puerta ni del anillo: son del cuerpo
que no llega a tiempo. Las cifras publicadas no cambian; su explicación sí. Pase lo que
pase, lo siguiente son los razonadores.

## 6 · ARCHIVOS

| archivo | qué es |
|---|---|
| `mide_anillo_P6_21.py` → `P6_21_anillo.json` | la regla del juego en los hechos (200 diarios; 64 reglas candidatas) |
| `mide_choque_P6_21.py` → `P6_21_choque.json` | el choque pieza a pieza desde el aviso 5 (A4, A5h, A6) y las 22 muertes de A4 |
| `mide_camino_P6_21.py` → `P6_21_camino.json` | el fuego del camino con la proyección congelada, 74 planes |
| `mide_quieto_P6_21.py` → `P6_21_quieto.json` | pasos aceptados que no mueven, por respuesta, destino y dirección |
| `mide_retraso_P6_21.py` → `P6_21_retraso.json` | retraso entre el último envío de un paso y el paso dado (subestima: solo distingue cuando cambia la dirección) |
| `mide_fantasma_P6_21.py` → `P6_21_fantasma.json` | acciones fantasma y pasos perdidos: la firma del retraso |
| `informe_P6_21.md` | este informe |

Nada jugado; ninguna imagen nueva; el código del juego se ha leído, no copiado.
