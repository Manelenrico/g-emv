# P5-LAG · El cinco frente a los pasos perdidos

*28-sep-2026. Coste cero: solo lectura de los diarios del cinco (P5-6C: A, F, T y la
ampliación F/T; P5-8M: A y K, tandas 0-4; 279 vidas). Nada jugado, nada construido.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; los 202
congelados del cinco y los 32 del seis: 0 alterados al principio y al final. Lo nuevo, en
archivos aparte y declarado: `mide_P5_LAG.py` → `P5_LAG_medidas.json`; `analiza_P5_LAG.py`
→ `P5_LAG_resumen.json`. Ningún número se escribió antes de calcularlo. Sin propuestas de
diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**Las cifras del cinco se reproducen exactas con el mismo criterio sobre todos los tramos
(42,3 y 61,1 %; 28/56 y 20/32; K/A 1,11 y 1,16; obedece 92,5 %), y en los tramos limpios
—sin ningún paso perdido— se mueven poco y en la dirección que refuerza lo que el cinco
concluyó:** los puntos de control cumplidos pasan a **45,1 % (F, n 51) contra 63,0 % (T,
n 27)**, diferencia −17,9 [−38,0, +5,2], el cero dentro como antes; la emparejada, a 48,5
contra 60,0 % (n 33 y 25), −11,5 [−34,6, +13,7]; K1 sube de 1,11 a **1,21** en tics limpios y
el emparejado («16 % más de mundo») de 1,16 a **1,31**; el compromiso obedece **91,9 %** en las
formas limpias (92,5 en todas). El sesgo va contra el brazo que más pasos perdió (F en
P5-6C, K en P5-8M), así que las conclusiones que ya iban contra ese brazo o que decían «sin
diferencia» **se sostienen**, y las que iban a su favor (K1, la mitad que subió un 16 %) salen
**reforzadas**. Lo que **no** se puede restringir así: la vida y el puesto (S6, K2), porque
una vida sin ningún paso perdido es una vida corta (mediana 1.216 tics en F contra 8.194 en
las demás): la restricción selecciona muertes tempranas, no vidas limpias; y K6, que no medía
pasos. Hay que corregir cuatro frases del cinco (§4): «un millón y medio de instantes vividos
sin perder ninguno», «el cuerpo nunca tuvo que esperar» (dos veces) y las dos filas del
apéndice con «0 perdidos» y «cero perdidos»: esas cifras contaban observaciones sin decisión y
decisiones que pasaban de un tic, no pasos que el juego no ejecutó.

---

## 1 · QUÉ SE MIDIÓ Y CÓMO (`mide_P5_LAG.py`, `analiza_P5_LAG.py`)

**Paso perdido** (P6-21, P6-22): paso enviado con las piernas listas hacia una casilla libre
(no sólida, sin cuerpo visto) al que el juego responde `ok` sin que la casilla cambie ni las
piernas dejen de estar listas. **Tic perdido** = el tic en que se envió.

**Tramos limpios**, declarados: **punto de control limpio** = ningún tic perdido entre la
aceptación de la forma y ese punto; **forma limpia** = ninguno entre la aceptación y su fin;
**tic limpio** (para tasas por tic) = a más de 24 tics de cualquier tic perdido; **vida
limpia** = sin ningún tic perdido. Las medidas son las del cinco con su mismo criterio de
cálculo (`d_real ≤ d_proyectada + 0,05` en los registros `confianza`; celdas tramos × banda;
casillas nuevas por cien tics con `curiosidad.Ojo`, como en `mide_P58M.py`; `obedece` /
`rompe` en los registros `compromiso`): la columna «todos» las recalcula y coincide con lo
publicado, y la columna «limpios» las restringe.

Control: pasos perdidos por brazo (todas las fases): P5-6C A 1 de 25.382 (0,0 %); F 1.262 de
20.424 (6,2 %) y la ampliación 1.389 de 25.176 (5,5 %); T 672 de 25.824 (2,6 %) y 559 de
21.830 (2,6 %); P5-8M A 2 de 21.762 (0,0 %); K 2.364 de 22.802 (**10,4 %**). Vidas sin ningún
paso perdido: A 39 de 40 y 38 de 40; F 8 de 80; T 18 de 80; K 6 de 39.

Dónde caen: en F, 0,46 pasos perdidos por cien tics en toda la vida y **1,27 dentro de una
forma** (56.150 tics de forma, 712 perdidos); en T, 0,20 y 0,33; en K, 0,73 y 1,23. Los pasos
se pierden sobre todo **mientras la forma se anda**, que es cuando la puerta reevalúa cada 25
tics y el compromiso empuja: justo los tramos que miden las afirmaciones.

## 2 · LAS AFIRMACIONES, EN TRAMOS LIMPIOS

### 2a · P5-6C · puntos de control cumplidos («La medida principal»)

| | original (todos) | tramos limpios | n limpios / n | puntos sucios: cumplen |
|---|---|---|---|---|
| F | 33/78 = **42,3 %** [32,0-53,4] | 23/51 = **45,1 %** [32,3-58,6] | 51 / 78 | 10/27 = 37,0 % |
| T | 22/36 = **61,1 %** [44,9-75,2] | 17/27 = **63,0 %** [44,2-78,5] | 27 / 36 | 5/9 = 55,6 % |
| diferencia F − T | **−18,80 [−36,30, +0,86]**, cero dentro | **−17,86 [−37,99, +5,24]**, cero dentro | | |

Los puntos sucios cumplen menos que los limpios en los dos brazos (37 contra 45 en F; 56
contra 63 en T): un paso perdido en el camino de la forma la retrasa y el punto llega peor.
Quitados, la brecha F − T apenas cambia (−18,8 → −17,9) y el cero sigue dentro.

### 2b · P5-6C · la comparación emparejada («(a) La emparejada»)

| | original | tramos limpios |
|---|---|---|
| celdas comparables | 6 de 15 | 5 |
| F | 28/56 = **50,0 %** | 16/33 = **48,5 %** [32,5-64,8] |
| T | 20/32 = **62,5 %** | 15/25 = **60,0 %** [40,7-76,6] |
| diferencia | **−12,50 [−31,80, +8,90]** | **−11,52 [−34,56, +13,72]** |

Celdas limpias: 2 tramos · banda 1 (F 3/4, T 2/2); 3 tramos · quedarse (3/5, 0/1); 3 tramos
· banda 1 (3/8, 6/12); 3 tramos · banda 2-3 (1/7, 5/6); 4 tramos · quedarse (6/9, 2/4). La
celda «2 tramos · quedarse» pierde la pareja.

### 2c · P5-6C · S6 y la vida

| | A | F | T |
|---|---|---|---|
| vida mediana, original (40 / 80 / 80 vidas) | 8.348,5 | 8.154,5 | 8.005,0 |
| puesto mediano, original | 12 | 13 | 12 |
| S6 emparejado por asiento (40 parejas con A), vida, mediana [IC bootstrap] | — | F−A −421,5 [−1.858, +254] | T−A −94 [−629, +1.403]; F−T −540 [−2.124, +160] |
| S6 emparejado, puesto | — | F−A +1,5 [−0,5, +2,0] | T−A +0,5 [−0,5, +2,0]; F−T +1,0 [0, +4] |
| **vidas limpias** (sin ningún paso perdido) | 39 · 8.340 | **8** de 80 · 1.216 | **18** de 80 · 1.393 |

**No se puede restringir así, y se dice por qué:** una vida sin ningún paso perdido es, en F
y T, una vida que murió pronto (mediana 1.216 y 1.393 tics contra 8.194 y 8.927 en las
demás): cuanto más vive un cuerpo con la puerta, más veces se encarga un juicio y más seguro
es que pierda algún paso. Restringir a vidas limpias selecciona muertes tempranas, no vidas
limpias. Lo que sí se puede decir: (1) los pasos perdidos son el 0,46 % de los tics de F y el
0,20 % de T; (2) el efecto de perder un paso es quedarse un tic donde se estaba, y las vidas
las decide el anillo y los vecinos (P6-17: nada en vidas sale del ruido con 20 semillas);
(3) las diferencias de vida y puesto ya tenían el cero dentro en las seis comparaciones.
**S6 se sostiene como estaba: sin diferencia que salga del ruido**, con la salvedad de que el
brazo F llevaba un lastre pequeño y medible que la comparación no descontaba.

### 2d · P5-8M · K1 (casillas nuevas por cien tics)

| | original (todos) | tics limpios |
|---|---|---|
| K · A | 8,93 · 8,08 | 9,80 · 8,08 |
| **K/A** | **1,106** | **1,213** |
| dentro / fuera de forma | 46,95 · 8,08 → **5,81×** | 49,70 · 8,90 → **5,58×** |
| tics de K contados | 323.725 (7.135 dentro) | 283.137 (6.231 dentro) |

### 2e · P5-8M · el emparejado de K1 («un 16 % más de mundo»)

| | original | tics limpios |
|---|---|---|
| K · A, en la ventana en que los dos viven (39 parejas) | 11,34 · 9,75 | 12,76 · 9,75 |
| **K/A** | **1,163** | **1,308** |

En tics limpios K descubre más, no menos: los tics que se quitan son los de los encargos,
donde el cuerpo se queda quieto sin quererlo y no descubre nada. **El «16 % más de mundo»
sube a 31 % en tramos limpios.** (El sello K1 pedía ≥ 1,5: sigue sin llegar.)

### 2f · P5-8M · K2 (vida y puesto por semilla)

| | original (39 parejas) | vidas limpias de K (6 parejas) |
|---|---|---|
| vida K − A, mediana [IC] | −216 [−1.907, +2.439] · K mejor 18 / peor 21 · p 0,75 | +2.086 [−941, +6.868] · 4 / 2 · p 0,69 |
| puesto K − A | −1 [−3, +3] | −0,5 [−3, +3] |

Igual que S6: las 6 vidas limpias de K son las cortas. **K2 no se puede restringir así**; se
sostiene como estaba («sin señal»), y el lastre (10,4 % de los pasos de K perdidos) iba en
contra de K, no a favor.

### 2g · P5-8M · el compromiso

| | original | formas limpias | tics limpios |
|---|---|---|---|
| obedece / rompe | 749 / 61 = **92,5 %** | 545 / 48 = **91,9 %** | 572 / 51 = 91,8 % |
| formas | 209 | 168 limpias · 41 con algún paso perdido dentro | |

«Obedecer» es emitir el paso de la forma, no darlo: en los 7.344 tics de forma de K, 90 pasos
emitidos no se ejecutaron (1,23 por cien tics de forma, contra 0,72 fuera de forma). La tasa de
obediencia no cambia porque se mide en lo emitido; lo que cambia es que 41 de 209 formas se
anduvieron con algún paso que el juego no dio.

### 2h · P5-8M · K6

K6 pedía «< 5 ms de mediana y cero tics perdidos». Lo medido era el cómputo de la decisión
por tic (`tiempo_tic.ms`: medianas por asiento 0,48-3,51 ms y un asiento a 5,508) y
«perdidos» = observaciones sin decisión (`elegido` vacío): **0**, que se reproduce. Ninguna de
las dos cosas mide pasos: **no se puede restringir**, y hay que decir lo que sí pasó: 2.364
pasos perdidos de 22.802 (10,4 %) en 33 de los 39 asientos de K.

### 2i · Lo que no se ha repetido

La magnitud (b), las rechazadas por área (c) y las formas del hermano (d) de P5-6C no se
apoyan en pasos andados con la forma viva o comparan ventanas de A (que no perdió pasos):
no cambian. P5-7C (Q 0,1-1,3 %): no se ha repetido; el lastre es diez veces menor que en F y K.

## 3 · EL SESGO, POR COMPARACIÓN

| serie | brazo que más perdió | la medida | ¿perjudicado o favorecido? | la conclusión del cinco |
|---|---|---|---|---|
| P5-6C | F (6,2 %; T 2,6 %; A 0) | puntos de control cumplidos | **perjudicado**: sus puntos sucios cumplen 37 contra 45 % limpios | «F por debajo de T, cero dentro» iba **en contra** del sesgo → **reforzada** |
| P5-6C | F | emparejada | perjudicado, poco (50,0 → 48,5 % limpio) | igual: cero dentro, **reforzada** |
| P5-6C | F | S6, vida y puesto | perjudicado (quedarse un tic donde estaba, 0,46 % de sus tics) | «sin diferencia» → **se sostiene**; F ya salía peor y el lastre lo explica en parte |
| P5-8M | K (10,4 %; A 0) | K1 y el 16 % | **perjudicado**: en tics limpios 1,11 → 1,21 y 1,16 → 1,31 | «K explora más» iba **en contra** del sesgo → **reforzada** (el sello ≥ 1,5 sigue fallando) |
| P5-8M | K | K2 | perjudicado | «sin señal» → **se sostiene** |
| P5-8M | K | compromiso obedece | ninguno (se mide en lo emitido) | **se sostiene**, con la salvedad de que obedecer no es dar el paso |
| P5-8M | K | K6 | — | **queda en duda** como sello: no medía lo que decía medir |

## 4 · FRASES DEL CINCO QUE HAY QUE CORREGIR

Texto de `paper5_borrador_ES_v39.pdf` y `paper5_draft_EN_v7.pdf` (los últimos borradores del
Mac; la sección se cita por su título). **Qué medían de verdad esas cifras:** «0 perdidos» /
«cero perdidos» = observaciones que llegaron y no produjeron decisión (`elegido` vacío en el
diario), 0 de 1.501.210; «sin perder ninguno» = lo mismo; «el cuerpo nunca tuvo que
esperar» = la decisión del cuerpo no esperaba al juicio de la puerta (el juicio corría en un
hilo y la decisión salía en el tic; tics de más de 40,5 ms: A 0,000 %, F 0,215 %, T 0,008 %).
Ninguna cuenta pasos que el juego no ejecutó: en F fueron 2.651 de 45.600 pasos listos (5,8 %),
en T 1.231 de 47.654 (2,6 %), en K 2.364 de 22.802 (10,4 %), y A 0.

| dónde | ES, literal | EN, literal |
|---|---|---|
| §7 «En el campo: el consejero que habla en formas» / «In the field: the advisor that speaks in shapes» | «La máquina no falló. Doscientas vidas con el diario entero, un millón y medio de instantes vividos sin perder ninguno, y más de dos mil consultas al consejero, todas con su parte.» | "The machine did not fail. Two hundred lives with the whole diary, a million and a half instants lived without losing any, and more than two thousand queries to the advisor, all with their report." |
| §7, mismo párrafo | «Imaginar un plan entero tarda más que un instante de este mundo, así que se hace aparte, en paralelo, al llegar el plan y después cada veinticinco instantes, y el cuerpo nunca tuvo que esperar.» | "Imagining a whole plan takes longer than one instant of this world, so it is done separately, in parallel, when the plan arrives and then every twenty-five instants, and the body never had to wait." |
| §10 «Cómo se midió y hasta dónde llega» / «How it was measured and how far it reaches» | «…con los viajes de curiosidad, el primer examen nunca antes de que el cuerpo haya podido llegar; en el campo, el cuerpo nunca tuvo que esperar.» | "…with curiosity trips, the first examination never before the body could have arrived; in the field, the body never had to wait." |
| Apéndice «Los números y de dónde salen», fila 7 | «cien partidas, doscientas vidas, millón y medio de instantes · 200 diarios; 1.501.210 tics vivos; 0 perdidos · informe_P56C» | "one hundred games, two hundred lives, a million and a half instants · 200 diaries; 1,501,210 live ticks; 0 lost · informe_P56C" |
| Apéndice, fila 8 (P5-8M) | «dos predicciones fallidas por cómo se midieron · armado a tiro con viaje activo: 52 tics, 5 con piernas listas (rupturas por veto); coste por tic: un asiento de 39 a 5,51 ms en todos sus tics, cero perdidos · informe_P58M» | "two predictions failed because of how they were measured · armed one within range with an active trip: 52 ticks, 5 with legs ready (breaks by veto); cost per tick: one seat of 39 at 5.51 ms in all its ticks, zero lost · informe_P58M" |

Lo que estas frases afirman y no es cierto: que el cuerpo no perdió nada y que nunca esperó.
Lo cierto: no perdió ninguna observación y su decisión salía en el tic; pero, con la puerta
en marcha, el juego no ejecutó el 5,8 % de los pasos de F, el 2,6 % de T y el 10,4 % de K (0
en A), porque el hilo principal se paraba a copiar la memoria en cada encargo y las acciones
llegaban tarde (P6-22 §3). Las cifras de campo del cinco se reproducen y se sostienen con la
corrección de §2 y §3; lo que hay que decir es esto, en esas cinco frases y en los informes
`informe_P56C.md` («Tiempo», «0 tics perdidos en 1.501.210 tics vivos») e `informe_P58M.md`
(K6).

## 5 · ARCHIVOS

| archivo | qué es |
|---|---|
| `mide_P5_LAG.py` → `P5_LAG_medidas.json` | los diarios del cinco, vida a vida: tics perdidos, formas y sus puntos (limpio o no), casillas nuevas por tic, compromiso, tiempos |
| `analiza_P5_LAG.py` → `P5_LAG_resumen.json` | las afirmaciones repetidas, todos los tramos y tramos limpios |
| `informe_P5_LAG.md` | este informe |
