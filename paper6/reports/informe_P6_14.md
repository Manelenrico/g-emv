# P6-14 · El consejero perfecto de reglas: ¿acepta la puerta los mejores planes para salir del anillo?

*27-sep-2026. Coste cero: ninguna partida nueva, ninguna llamada de pago. Solo
banco sobre los 40 diarios de A4 (P6-11) y el código congelado.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final;
los 202 congelados del cinco (`cantera/paper5/CONGELADO.md`) y los 32 del seis
(`CONGELADO_P6.md`, etiqueta `cuerpo6-congelado`): 0 alterados al principio y
al final. Nada de MettaScope. Sin propuestas de diseño.*

**EL ORÁCULO ES UN INSTRUMENTO DE MEDIDA.** Así se llama en todos los archivos
(`oraculo_P6_14.py`, `banco_P6_14.py`, `corre_P6_14.py`, `resume_P6_14.py`,
`gif_P6_14.py`, `P6_14_planes.json`, `P6_14_resumen.json`, `P6_14_plan.gif`).
No juega, no decide, no entra en ninguna política ni imagen: propone planes en
seco y la puerta real del cuerpo congelado los juzga en seco.

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**De las 19 muertes evitables por anillo, la puerta del cuerpo congelado acepta
a tiempo algún plan del oráculo en 3** (las tres de clase (ii) «miedo»; 0 de 6
de clase (i) «salir tarde»; 0 de 1 de clase (iii)). Acepta **27 de 3.849 planes
juzgables (0,7 %)**. Con el margen mínimo de la puerta (0,02, el que el cuerpo se
aplica a sí mismo) serían 7 de 19; con 0,08, 2 de 19. **Lo que la rechaza no es
el miedo**: es que **el comparador de la puerta es el mejor candidato PROPIO en
proyección** (`ir_botin`, `ir_centro`, `ir_pareja` en 2.912 de 3.064 planes de
la ventana de muerte), y ese candidato, proyectado, ya sale del anillo: la
ventaja del plan es ≤ 0 en 2.286 de las 2.536 rechazadas por área. La puerta
compara con lo que el cuerpo *podría* imaginar, no con lo que *eligió*.

---

## 1 · MÉTODO

### 1.1 El oráculo (`oraculo_P6_14.py`)

Generador de planes por reglas con lo que el mundo publica desde el tic 0:
`zone_schedule` (7 fases `[warn, shrink, done, r0, r1, dps]`), centro (24,24),
mapa (`mundo.solido`), y los rivales **contados** en la percepción que ve el
decisor (vistos + dichos por el hermano, con los ojos inyectados).

- **Casilla segura** = alcanzable (BFS a 8 vecinos por casillas no sólidas) y
  que *siga a salvo cuando llegue*: distancia al centro ≤ radio en el tic de
  llegada **y** ≤ r1 de la fase activa en ese tic (así no arde en lo que queda
  de fase). Llegada = tic + pasos × `coste_movimiento(speed)` (11 tics con
  SPD 5, el mismo reloj que `proyeccion.PASO_TICS`).
- **Criterios de destino:** (a) la más cercana (pasos reales); (b) la de menos
  rivales contados a ≤ R casillas (Chebyshev), desempate por cercanía; (c) la
  misma para los dos hermanos: la que minimiza el máximo de los pasos de ambos
  (posición del hermano de su diario en ese tic; sin (c) si ha muerto).
- **Momentos:** (1) *ahora*: cada decisión con piernas listas en que mi
  casilla arde, o arderá antes de lo que tardo en salir más un margen;
  (2) *al primer aviso de la fase*: la primera decisión con piernas listas
  ≥ `warn` de cada fase, arda o no.
- **Idioma de formas:** el JSON que escribiría un consejero (`{"formas":
  [{"tramos": [{"destino": [x,y], "intencion": "ir", …}, {"intencion":
  "esperar", "esperar": H, …}]}]}`), traducido por el traductor real
  (`traductor_forma.traduce` → `solo_tramos`), no por el oráculo.
- **Umbrales elegidos por el instrumento** (cada uno cruzado con otros dos
  valores en §4): margen de disparo **33 tics** (3 pasos; alternativas 0 y
  110), R de «cerca» **5** (3 y 8), espera H **100** (50 y 200).

### 1.2 El juicio (`banco_P6_14.py`)

Una vida por proceso, por la vía real: el alma real de la pareja
(`policy_pareja.AlmaPareja` con `arreglos_P6_6` + `arreglos_P6_8b` +
`filas10_P6_10` + `amenaza11_P6_11` + `_envuelve`, en el orden de
`policy_pareja11.run`), alimentada por `policy_cortex.decisor` con un WS falso
que sirve el `player_config` y las observaciones del diario tal cual (con su
`chat`: los E2 del hermano entran por el cable). Empatía cableada como fija
`policy_cortex.py:93-96` (se comprueba con `assert`, no se supone); entorno de
la imagen (`GEMV_OJOS=1`, `GEMV_COMPANIA_TECHO=0.32`, `GEMV_CORTEX=0`,
`GEMV_FORMA=0`, …).

**La puerta:** `AlmaForma._acepta_o_no(fv, obs)` (`policy_forma:716`) →
`_juzga` → `forma_viva.evalua` → `forma.curva_H` (plan) contra
`forma.mejor_propia_H` (los candidatos propios del cuerpo vía `D.candidatos`,
alargados al mismo horizonte) → `forma.juzga_margen` (vida < 15 en algún
punto de control → «vida»; área ≤ margen → «area»; si no, «ok») con el margen
de `confianza_viva` (C0 0,30 → **0,062**). Es exactamente la función que
`_decidir_forma` llamaría con `GEMV_FORMA=1`; aquí la llama el instrumento
desde fuera en cada decisión del oráculo, con la percepción que el cuerpo
acaba de decidir (`alma.ultima_obs`, con ojos, como la recibe
`_decidir_forma`). **`GEMV_FORMA` queda en 0** porque con 1 el cuerpo
obedecería a lo aceptado y la repetición dejaría de seguir el diario; el
código de la puerta es el mismo. **`_compromiso` (`:1624`) queda tal cual**:
en la configuración congelada (`GEMV_CURIOSIDAD_FORMA=0`) no interviene. Lo
aceptado se anota y se retira de `alma.vivas` al instante.

**Captura sin tocar la regla:** se envuelven `forma.d_con_pisos` (las filas
con piso que la puerta valora en cada foto) y `forma.mejor_propia_H` (el
comparador) desde el banco; con eso se identifica el comparador y se calcula
**cuánto pesa cada fila en contra**: área sin la fila menos área con la fila
(en las unidades del margen), sobre las mismas fotos con piso. Alineación de
fotos: 19.911 de 19.911 planes.

**Fidelidad del replay:** el `elegido` del replay contra el del diario en
cada tic: **494.368 de 494.370 iguales**. Los 2 que difieren son de
`21622393` asiento 10, que murió en el tic ~2.000 (antes del primer aviso):
dos desempates de `move` y 0 decisiones del oráculo. Las 39 vidas restantes,
al bit.

**Coste:** 40 procesos, 8 a la vez, **718 s de reloj** (3.745 s de CPU);
19.911 llamadas a la puerta, mediana **141 ms**, p95 211 ms.

### 1.3 Definiciones (declaradas)

- **Muerte por anillo** = las 22 de P6-11/P6-13; **evitable** = de las fases
  1-6 (**19**; las 3 de la fase final, radio 3 → 0, no lo son, informe_P6_13
  §2); **clase** = la de P6-13 (i 6, ii 12, iii 1 entre las evitables).
- **Ventana** de una muerte = [aviso de la fase que mata, muerte).
- **A tiempo** = plan aceptado en una decisión de la ventana con llegada
  (tic + pasos × 11) anterior a la muerte.
- **Falsa aceptación** (vidas sin muerte por anillo) = plan aceptado cuya foto
  prevista dice que algo empeora: (α) en algún punto de control la `d` del
  plan es peor que la del comparador; (β) la vida prevista al final es menor
  que la del comparador; (γ) el destino aleja del hermano (Chebyshev al
  hermano de su diario ese tic) más de lo que está ahora.
- **No juzgable** = destino = la propia casilla (el tramo `ir` tiene 0 pasos).
  Se cuentan aparte (§3.6), no se tiran.

---

## 2 · LO QUE HUBO

| | |
|---|---|
| vidas | 40 (22 con muerte por anillo, 19 evitables) |
| tics repetidos | 494.370 |
| decisiones del oráculo (con margen 110, el mayor) | 2.641 · con el margen elegido (33): **2.049**, de ellas 219 de momento (2) |
| planes generados (3 H × hasta 5 destinos) | 19.911 |
| planes con umbrales principales (H 100, R 5, margen 33) | 4.004 = **3.849 juzgables + 155 de propia casilla** |
| veredictos de los 3.849 | **area 3.318 · vida 504 · ok 27** |

Los 40 diarios traen de media 51 decisiones por vida; las vidas que más
tiempo pasan ardiendo son las que más planes generan (`22250767` s11: 299
decisiones, 2.628 planes; `20889290` s10: 203).

---

## 3 · LO QUE HAY QUE CONTAR (§3 de la orden)

### 3.1 En las 19 muertes evitables

**3 de 19 tuvieron al menos un plan aceptado a tiempo**: clase (ii) **3 de
12**, clase (i) **0 de 6**, clase (iii) 0 de 1.

| vida | clase | fase | aviso · golpe · muerte | decisiones · planes | area · vida · ok | aceptados a tiempo (primero) | mejor ventaja (veredicto, comparador) |
|---|---|---|---|---|---|---|---|
| 20260916 s11 | i | 6 | 12.996 · 13.561 · 13.632 | 11 · 11 | 9 · 2 · 0 | 0 | +0,0017 (vida, ir_centro) |
| 20679832 s11 | i | 5 | 11.856 · 12.673 · 12.888 | 34 · 54 | 47 · 7 · 0 | 0 | +0,0000 (area, ir_botin) |
| 20784561 s11 | i | 5 | 11.856 · 12.649 · 12.840 | 34 · 84 | 63 · 21 · 0 | 0 | +0,0519 (area, ir_botin) |
| 21098748 s11 | i | 5 | 11.856 · 12.649 · 13.008 | 44 · 93 | 86 · 7 · 0 | 0 | +0,0286 (area, ir_botin) |
| 21203477 s11 | i | 5 | 11.856 · 12.001 · 12.024 | 5 · 10 | 4 · 6 · 0 | 0 | −0,0076 (vida, ir_centro) |
| 21936580 s11 | i | 6 | 12.996 · 13.921 · 13.968 | 13 · 13 | 12 · 1 · 0 | 0 | +0,0039 (area, ir_centro) |
| 20260916 s10 | ii | 5 | 11.856 · 12.289 · 12.648 | 33 · 67 | 55 · 12 · 0 | 0 | +0,0240 (vida, ir_botin) |
| 20365645 s10 | ii | 3 | 9.576 · 10.273 · 10.920 | 72 · 153 | 138 · 13 · 2 | **2 (t 10.120)** | +0,0873 (ok, ir_botin) |
| 20575103 s10 | ii | 5 | 11.856 · 12.289 · 12.600 | 33 · 61 | 49 · 12 · 0 | 0 | +0,0173 (area, ir_centro) |
| 20575103 s11 | ii | 5 | 11.856 · 12.601 · 12.816 | 22 · 36 | 24 · 12 · 0 | 0 | +0,0066 (area, ir_botin) |
| 20889290 s10 | ii | 5 | 11.856 · 12.745 · 13.008 | 203 · 349 | 345 · 4 · 0 | 0 | +0,0047 (area, ir_centro) |
| 21308206 s10 | ii | 5 | 11.856 · 12.721 · 13.056 | 72 · 103 | 100 · 3 · 0 | 0 | +0,0566 (area, ir_centro) |
| 21727122 s11 | ii | 5 | 11.856 · 12.313 · 12.672 | 37 · 70 | 48 · 22 · 0 | 0 | +0,0275 (vida, ir_botin) |
| 21831851 s10 | ii | 5 | 11.856 · 12.673 · 12.960 | 26 · 46 | 32 · 13 · 1 | **1 (t 12.824)** | +0,0894 (ok, ir_botin) |
| 21831851 s11 | ii | 5 | 11.856 · 12.625 · 12.840 | 38 · 72 | 60 · 12 · 0 | 0 | +0,0000 (area, ir_botin) |
| 21936580 s10 | ii | 5 | 11.856 · 12.505 · 12.888 | 135 · 275 | 242 · 29 · 4 | **4 (t 12.594)** | +0,0741 (ok, ir_botin) |
| 22041309 s11 | ii | 5 | 11.856 · 12.361 · 12.720 | 46 · 103 | 83 · 20 · 0 | 0 | +0,0490 (area, ir_centro) |
| 22250767 s11 | ii | 5 | 11.856 · 12.649 · 12.912 | 289 · 752 | 515 · 237 · 0 | 0 | +0,0038 (vida, ir_botin) |
| 21727122 s10 | iii | 5 | 11.856 · 12.385 · 12.744 | 38 · 70 | 51 · 19 · 0 | 0 | +0,0162 (area, ir_centro) |

(Umbrales principales: H 100, R 5, disparo 33, margen 0,062; planes de la
ventana. Los planes que solo llevan (b) con R 3 u 8 están en las variantes de
§4: con R 3, `21098748` s11 —clase (i)— sí tiene 3 aceptados a tiempo, y la
cuenta pasa a (i) 1 de 6, (ii) 2 de 12, mismo total 3 de 19.)

En 13 de las 19 el mejor plan de toda la ventana queda por debajo de 0,03 de
ventaja; en 5, el mejor plan ni siquiera pasa de «vida» (el cuerpo ya está a
0-21 hp cuando el oráculo puede proponer).

### 3.2 Qué criterio y qué momento aceptan más

| criterio | aceptados / juzgados | |
|---|---|---|
| (b) menos rivales a 5 | **15 / 2.003** | 0,75 % |
| (c) la misma para los dos | 13 / 1.789 | 0,73 % |
| (a) la más cercana | 12 / 1.894 | 0,63 % |

(Un plan puede llevar varios criterios si coinciden en destino.)

| momento | aceptados / juzgados |
|---|---|
| (1) ahora | **27 / 3.542** |
| (2) al primer aviso de la fase | **0 / 321** (+155 de propia casilla) |

Al aviso, la puerta no acepta nada: en 366 de los 504 planes de momento (2)
(tres H) el comparador es `noop`, y en la proyección a 100 tics la casilla
propia aún no arde: área mediana −0,031, ≤ 0 en 489 de 500.

### 3.3 Clase (ii): ¿alguna casilla segura con pocos rivales que la puerta acepte?

Sí, pero casi nunca. En la ventana de las 12 muertes de clase (ii), H 100,
todos los destinos propuestos (a, b3, b5, b8, c):

| rivales contados a ≤ 5 del destino | planes | aceptados | rechazados (area) | rechazados (vida) |
|---|---|---|---|---|
| 0 | 407 | **4** | 344 | 59 |
| 1 | 762 | 2 | 696 | 64 |
| 2 | 769 | 1 | 633 | 135 |
| 3 | 986 | 0 | 830 | 156 |
| ≥ 4 | 239 | 0 | 225 | 14 |

El oráculo **encuentra** casillas seguras sin ningún rival contado cerca (407
planes) y la puerta rechaza 403 de ellas. Lo que pesa en contra en los
rechazos por área de la clase (ii) (media por plan, en área):

| fila | planes en que pesa | peso medio | total |
|---|---|---|---|
| F-DANO | 1.649 | +0,019 | +31,6 |
| R-LLAMADA | 1.769 | +0,015 | +26,6 |
| F-ANTICIPACION | 749 | +0,024 | +18,0 |
| S-8-EXPOSICION | 1.696 | **+0,005** | +7,8 |
| S-PROVISION | 227 | +0,028 | +6,3 |
| S-7-AGRESOR | 147 | +0,029 | +4,3 |

**El miedo no lo tapa**: S-8 pesa +0,005 de media contra los planes de la
clase (ii), porque en la proyección de la puerta los rivales van **a piso**
(`pisos_rival`: F-4-ALCANCE, S-8, S-7, MIEDO_APRENDIDO, S-VIDA-AJENA no bajan
del valor actual, ni para el plan ni para el comparador), así que el miedo se
cancela en la resta salvo cuando el plan se acerca a rivales. Lo que decide es
que el comparador (`ir_botin`, `ir_centro`) **también sale del anillo en
proyección**: la ventaja mediana de los rechazos por área en la ventana es
**−0,018** (cuantiles 10/90: −0,126 / 0,000); ≤ 0 en 2.286 de 2.536; entre 0 y
0,062 (perdidas por margen) 250.

### 3.4 Vidas sin muerte por anillo: falsas aceptaciones

18 vidas, 1.063 planes juzgables (H 100). Aceptados **11** en 5 vidas
(comparador: `ir_botin` 6, `ir_centro` 3, `ir_pareja` 1, `noop` 1). Con lo que
la foto prevista dice del después: **8 falsas** (γ aleja del hermano **7**; β
menos vida al final 2; α algún punto peor 1) en 4 vidas. Ejemplo: `22041309`
s10, t 12.440, hp 100, plan (b) (21,29) → (24,29) aceptado con ventaja +0,076
contra `ir_botin`: el hermano pasa de 3 a 6 casillas; `20365645` s11, t 10.605,
plan (b) a (30,15): vida final prevista 60,3 contra 62,0 y el hermano de 1 a 3.
Los 3 aceptados sin ninguna falsa son `20470374` s10 t 13.899 (a la casilla
(24,27), a 2 del hermano, contra `ir_centro`) y `21308206` s11 t 12.591 y
12.602 (a (23,28), contra `ir_centro`, el hermano a 4).

### 3.5 Qué filas pesan en contra, en general (3.849 juzgables, H 100)

| en contra | planes | peso medio | total | | a favor | planes | peso medio | total |
|---|---|---|---|---|---|---|---|---|
| S-8-EXPOSICION | 2.931 | +0,067 | +196,3 | | F-ANTICIPACION | 1.340 | −0,087 | −117,1 |
| R-LLAMADA | 4.394 | +0,017 | +72,5 | | S-8-EXPOSICION | 2.246 | −0,013 | −29,0 |
| F-DANO | 2.368 | +0,028 | +67,1 | | F-DANO | 2.250 | −0,010 | −22,2 |
| F-REENCUENTRO | 111 | **+0,585** | +64,9 | | R-LLAMADA | 1.002 | −0,013 | −12,8 |
| F-ANTICIPACION | 1.306 | +0,038 | +49,3 | | F-4-ALCANCE | 2.895 | −0,004 | −10,7 |
| S-HERIDO | 408 | +0,059 | +24,3 | | F-REENCUENTRO | 37 | −0,102 | −3,8 |

S-8 pesa en contra cuando el destino está más cerca de rivales que el del
comparador (sobre todo en el momento (2) y en las vidas sin anillo, con
`ir_centro`/`ir_pareja` de comparador); F-ANTICIPACION es la fila que más
favorece a los planes y aun así también pesa en contra en 1.306 (cuando el
comparador llega más adentro del radio que el destino del oráculo).
F-REENCUENTRO, rara (111 planes), es la más pesada por plan: +0,585.

### 3.6 Lo que la puerta no puede juzgar

**155 planes con destino = la propia casilla**, todos de momento (2) (al aviso
el cuerpo suele estar ya en casilla segura; (a) y (b3) la eligen). La puerta
los juzga formalmente («area», ventaja 0,000 en los 155: «esperar aquí H
tics» contra `noop` alargado son la misma curva). Se cuentan aparte y no en
los 3.849. Intraducibles: 0. «Sin comparador» / «revienta»: 0. Fotos no
alineadas: 0.

### 3.7 El criterio (c), juzgado por cada puerta

13 planes (c) aceptados. En 64 ocasiones los dos hermanos juzgaron el **mismo
destino en el mismo tic**; en **0** lo aceptaron los dos. Nunca hubo un plan
común aceptado por las dos puertas.

---

## 4 · LOS UMBRALES, CRUZADOS

81 combinaciones (H × margen de la puerta × margen de disparo × R) están en
`P6_14_resumen.json → variantes`. Lo que cambia y lo que no:

| umbral | valores | evitables con plan aceptado a tiempo | planes aceptados | falsas / aceptados sin anillo |
|---|---|---|---|---|
| **margen de la puerta** (H 100, disparo 33, R 5) | **0,062** · 0,02 · 0,08 | **3** · 7 · 2 | **27** · 155 · 10 | **8/11** · 26/38 · 2/3 |
| **H** (0,062, 33, 5) | 50 · **100** · 200 | 5 · **3** · 3 | 63 · **27** · 24 | 9/16 · **8/11** · 7/10 |
| **margen de disparo** (H 100, 0,062, R 5) | 0 · **33** · 110 | 3 · **3** · 4 | 25 · **27** · 30 | 7/10 · **8/11** · 8/12 |
| **R de «cerca»** (H 100, 0,062, 33) | 3 · **5** · 8 | 3 · **3** · 2 | 32 · **27** · 20 | 14/18 · **8/11** · 3/7 |

Por todo el cruce: evitables a tiempo entre **1 y 10** de 19; con el margen
real de la puerta (0,062) entre **2 y 6**; los 10 solo con margen 0,02 + H 50 +
disparo 110, y entonces 68 falsas de 83 aceptados sin anillo. El margen de
la puerta es el umbral que más mueve la cuenta; R apenas; el disparo,
nada (los planes de momento (1) con más holgura ya pierden por área).

---

## 5 · EL CASO EN GIF

`P6_14_plan.gif` (88 fotogramas, cada 12 tics, del aviso 11.856 a la muerte
12.888): **`21936580` asiento 10, clase (ii)**, con el plan del oráculo
**aceptado** en el tic **12.594**: (b) casilla segura con 0 rivales contados a
5, (19,20) → (19,24), 4 pasos, llegada 12.638, ventaja **+0,0659** contra
`ir_botin`. En el título de cada fotograma: hp, lo que elige el cuerpo, S-8 y
F-ANTICIPACION; en el tic del juicio, «AQUÍ JUZGA LA PUERTA». El cuerpo, que
no vio el plan, elige `move_S`, `ir_objeto`… y muere en 12.888 con el hermano
a 6 casillas. (Se reutiliza el molde de `gif_P6_13.py`; matplotlib sobre los
diarios crudos.)

---

## 6 · LO QUE DICE LA MEDIDA (sin proponer nada)

1. **El techo de un consejero perfecto de reglas, con esta puerta tal cual, es
   3 de 19** muertes evitables (2-6 en cualquier margen real de la puerta).
2. La puerta **no rechaza por miedo**: los rivales van a piso en la
   proyección y S-8 pesa +0,005 de media contra los planes de la clase (ii).
3. La puerta rechaza porque **compara con el mejor candidato propio en
   proyección**, y ese candidato (`ir_botin`, `ir_centro`) ya sale del anillo:
   2.286 de 2.536 rechazos por área tienen ventaja ≤ 0. Es decir: la puerta
   mide si el plan imagina mejor que el cuerpo, y **el cuerpo ya imagina bien
   el anillo** (P6-13). Lo que P6-13 midió como déficit —el cuerpo elige por
   la `d` de ahora, donde S-8 gana a F-ANTICIPACION— **no es lo que la puerta
   mide**.
4. **Al aviso (momento 2) nada pasa**: 0 de 321; a 100 tics vista la casilla
   aún no arde y el comparador es `noop`.
5. Cuando el oráculo puede proponer con la casilla ya ardiendo, en 5 de 19
   vidas el cuerpo está a 0-21 hp y todo cae por «vida» (518 planes en las
   ventanas: hp mediana 9 al decidir).
6. Las aceptaciones fuera del anillo (11 en 18 vidas) son en su mayoría
   **falsas** (8: 7 alejan del hermano).

---

## 7 · ARCHIVOS

| archivo | md5 | qué es |
|---|---|---|
| `oraculo_P6_14.py` | `a791ddc0cca9940b9c80920dc66a623d` | el oráculo (instrumento) |
| `banco_P6_14.py` | `8808fe82ba895996c28a1f15afe7fd51` | una vida por la vía real + la puerta real |
| `corre_P6_14.py` | `8a6e41f550afc094653c1005c316e17a` | las 40 vidas, 8 procesos |
| `resume_P6_14.py` | `601073de2c3dbf0ef7301b3b6cc5aadd` | las cuentas y el cruce de umbrales |
| `gif_P6_14.py` | `c891db7d2e2482838c8723c9739d7812` | el GIF |
| `P6_14_planes.json` | `35d31019ed44da9934ab800d28871835` | los 19.911 planes con veredicto, ventaja, comparador, curvas y filas en contra (23 MB) |
| `P6_14_resumen.json` | `8d3ccbb0f5971d7b170055724f6e9ddb` | totales, cuentas principales, 81 variantes, clase (ii), filas, mejor plan por vida |
| `P6_14_plan.gif` | `fc3fa6df0d153e1bd29f677cc6675834` | el caso |

Las 40 salidas por vida (con las curvas completas) están en el scratch de la
sesión, no en el repo; se regeneran con `corre_P6_14.py` (12 min).

---

## NOTA POSTERIOR (P6-15, 27-sep-2026)

La explicación de §3.3 y §6.2 («el miedo se cancela porque los rivales van a
piso») queda **corregida** por la medida de P6-15 §1.2: el piso cambia la
diferencia de S-8 en 0,004; S-8 se cancela en la puerta porque **el plan del
oráculo entra en el anillo tan expuesto como el comparador** (+0,210 contra
+0,208 sobre quedarse). Los números de este informe no cambian; la causa
atribuida, sí. Ver `informe_P6_15.md`.
