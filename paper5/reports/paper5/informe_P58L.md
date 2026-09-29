# P5-8L — Por qué el veto duro mata los viajes largos, y si tenía razón

Diagnóstico **en seco**, **coste cero**. Sin imagen, sin plataforma. Motor,
decisor y tabla intocados, idénticos al empezar y al acabar. **Sin sellos.**

---

## El titular

**Hay un escalón, está entre 7 y 8 casillas, y es vertical.**

| distancia al nacer | n | **veto duro** | completada |
|---|---|---|---|
| 1-3 | 3 | **0 %** | 66,7 % |
| 4-5 | 8 | **12,5 %** | 75,0 % |
| 6-7 | 8 | **25,0 %** | 75,0 % |
| **8-9** | **100** | **100,0 %** | **0,0 %** |

**Las cien formas nacidas a ocho o nueve casillas murieron las cien por veto
duro. Ninguna llegó.**

**Y el veto no salta porque un armado se acerque: salta porque APARECE.** De los
103 vetos, **101 (98,1 %) se disparan en el mismo tic en que el armado se hace
visible por primera vez** desde que nació la forma. Las formas que mueren así
viven **11 tics de mediana — un solo paso del mundo**.

**El mecanismo es geométrico y no tiene nada de misterioso:** la forma nace
legal (ninguna de las 119 nace con el camino ya cubierto: **0 de 119**, el
nacimiento y la muerte son coherentes), el cuerpo da un paso, y al dar ese paso
aparece un armado. Con un camino de ocho o nueve casillas, la probabilidad de
que el nuevo armado cubra **alguna** de ellas es prácticamente uno.

**¿Tenía razón el veto? No hay prueba de que sí.** De los 103 vetos, **uno solo
(0,97 %) fue seguido de daño en los 50 tics siguientes**, contra el **0,35 %**
de la base de A en entorno seguro. Con un suceso observado contra 0,36
esperados, **no se distingue del azar**.

**Y hay una corrección que me debo a mí mismo: K5 no falló.** Medido por forma,
**0 de 109 recibieron daño con la forma viva** y **1 de 109** en los 50 tics
siguientes. El 1,43 % que publiqué ayer salía de contar **el mismo suceso hasta
cincuenta veces**, una por tic.

---

## Custodia y control

```
                            al empezar                         al acabar
motor/model.py              1e511978c251130e95169ebf8443efa1   idéntico
paintball/alma/decisor_zs.py
                            8fa03547e3228ef9df4aa94c444f9252   idéntico
paintball/alma/appraisal_zs_v42_exp.py
                            98c13d60167c80cc8334c965be75c640   idéntico
```

**El control del arnés:** el camino de cada forma se reconstruye con el mismo
`camino_a_frontera` de la imagen y se coteja con el destino registrado en el
diario. **1.286 de 1.286 destinos coinciden.** Sin eso, nada de lo de abajo
valdría.

---

## 1 · El escalón

119 formas aceptadas: 10 de P5-8I (margen 0,062) y 109 de P5-8K (margen 0,02).

| tramo | n | veto duro | completada | atasco | sin fin |
|---|---|---|---|---|---|
| 1-3 | 3 | 0 (0,0 %) | 2 (66,7 %) | 0 | 1 |
| 4-5 | 8 | 1 (12,5 %) | 6 (75,0 %) | 1 (12 %) | 0 |
| 6-7 | 8 | 2 (25,0 %) | 6 (75,0 %) | 0 | 0 |
| **8-9** | **100** | **100 (100,0 %)** | **0 (0,0 %)** | 0 | 0 |
| 10+ | 0 | — | — | — | — |

**El escalón está entre 6-7 y 8-9: 25 % → 100 %.** No es una pendiente, es un
muro.

**Y el mismo cuadro separado por sonda dice que el muro no lo trajo el margen:**

| | 1-3 | 4-5 | 6-7 | 8-9 |
|---|---|---|---|---|
| **P5-8K** (0,02) | 0 % (n=2) | 25 % (n=4) | 33 % (n=3) | **100 % (n=100)** |
| **P5-8I** (0,062) | 0 % (n=1) | 0 % (n=4) | 20 % (n=5) | **— (n=0)** |

En los tramos que comparten, las dos sondas dan tasas parecidas. **Lo que el
margen 0,02 hizo fue abrir el tramo 8-9, que antes estaba vacío**: P5-8I no
aceptó ni una sola forma más allá de 7 casillas (máximo 7, mediana 5,5), y
P5-8K aceptó cien en 8-9 (mediana 8).

**El margen no cambió la física del veto. Cambió qué distancias entran.**

---

## 2 · El armado que dispara el veto

103 vetos con culpable identificado.

| | |
|---|---|
| **es el hermano** | **0 de 103** — la regla lo excluye por construcción (`armados()` filtra `slot == herm`) |
| quién | **slot 3 (equipo B): 59 · slot 2 (equipo B): 41** · slot 9: 2 · slot 12: 1 |
| arma | **lanza 60 · cuchillos 43** |
| alcance | **2,0 en 60 casos · 5,0 en 43** |
| distancia al cuerpo | min 2 · **mediana 8** · max 8 |

**Dos enemigos del mismo equipo hacen cien de los ciento tres vetos**, y con las
dos armas más cortas del mundo: lanza de alcance 2 y cuchillos de alcance 5.
**No es un arquero a distancia: es un tipo con una lanza sentado a ocho casillas
del cuerpo, cuyo alcance de dos casillas toca una del camino.**

### ¿Se acercaba, o estaba quieto?

| | |
|---|---|
| se acercaba en los 5 tics previos | **2 de 103 → no (`False`)** |
| **no era visible en ninguno de los 5 tics previos** | **101 de 103** |

Y con la ventana abierta a toda la vida de la forma:

| | |
|---|---|
| **no se había visto NUNCA desde que la forma nació** | **101 / 103 = 98,1 %** |
| ya era visible en el tic de nacer | 2 / 103 = 1,9 % |
| tics visible antes del veto | **mediana 0** · max 39 |

**El veto duro no es un mecanismo de «el enemigo se acerca». Es un mecanismo de
«el enemigo aparece».** Y como el cuerpo anda a once tics por casilla, aparece
justo cuando el cuerpo asoma la cabeza al dar su primer paso.

### ¿Nacía ya condenada?

**No. 0 de 119.** Ninguna forma aceptada tenía el camino cubierto en el tic de
nacer, medido con **la misma función que luego la mata**
(`abandona_por_peligro`). **La regla de nacimiento y la de muerte son
coherentes**; el problema no es una contradicción interna, es que el mundo se
revela mientras se anda.

### El contrafactual que pediste

**Los vetos con armado quieto que no se acercaba son solo 2**, porque 101 de 103
ni siquiera eran visibles antes. Con n = 2 no hay contrafactual que hacer: **0
de 2 recibieron daño**.

**Así que doy el cuadro entero, que es el que tiene n:**

| | |
|---|---|
| vetos | **103** |
| seguidos de daño **de ese armado** en 50 tics | **1 = 0,97 %** |
| seguidos de daño **de cualquiera** en 50 tics | **1 = 0,97 %** |
| **base de A en entorno seguro** | **171 / 48.253 = 0,35 %** |

**Un suceso contra 0,36 esperados. El veto duro se disparó 103 veces y en 102 no
pasó nada.** Eso no prueba que el veto sea inútil —puede que evitara justamente
el daño que no se ve— pero **con estos datos no hay ninguna evidencia de que
protegiera de algo**, y sí la hay de que cuesta el 100 % de los viajes largos.

---

## 3 · K5, y la corrección de ayer

**Medido por forma, en P5-8K:**

| | |
|---|---|
| formas aceptadas | 109 |
| **con daño mientras la forma seguía VIVA** | **0 = 0,0 %** |
| con daño en los 50 tics después del fin | **1 = 0,9 %** |
| de las 102 muertas por veto duro, con daño después | **0 = 0,0 %** |
| base de A en seguro (esa misma partida) | **26 / 4.656 = 0,56 %** |

**Ayer publiqué que K5 fallaba: 1,43 % contra 0,56 %. Estaba mal, y el error es
de mi métrica, no del mundo.** La medí **por tic**: cada tic dentro de forma
cuenta como un caso, y «hubo daño en los 50 siguientes» marca hasta cincuenta
tics por un solo golpe. Dieciocho de aquellos «casos» eran **un golpe**.

**Por forma, que es la unidad que tiene sentido, no hay daño durante la forma en
absoluto, y el único golpe posterior es uno.** Con 109 formas y un suceso, K5 no
se distingue de la base de A. **Retiro el fallo de K5 que publiqué en
`informe_P58K_sonda.md`.**

---

## 4 · La asimetría entre asientos

Distancia a la frontera **de todas las nacidas**, no solo de las aceptadas.

| asiento | nacidas | acep | % | min | Q1 | **mediana** | Q3 | max | mediana de las **aceptadas** |
|---|---|---|---|---|---|---|---|---|---|
| **K/0916/10** | 136 | 5 | **3,7 %** | 4 | 6 | **7** | 7 | **7** | **4** |
| **K/0916/11** | 120 | 104 | **86,7 %** | 3 | **8** | **8** | **8** | **11** | **8** |

**Sí: un asiento vive rodeado de fronteras lejanas y el otro de cercanas.** El
que acepta el 86,7 % tiene el cuartil inferior **en 8** —tres de cada cuatro de
sus fronteras están en el tramo del muro— y llega hasta **11**. El que acepta el
3,7 % tiene **todas sus fronteras topadas en 7**, y de las cinco que acepta, la
mediana está en **4**.

**Pero la distancia NO explica la aceptación por sí sola**, y hay que decirlo:
en P5-8I hay asientos con mediana 8 (`5645/10`, `9832/11`) que aceptaron
**cero**. Lo que la distancia explica limpiamente es **quién muere**, no quién
entra. **Con dos asientos en P5-8K no puedo separar la distancia de lo demás.**

**Lo que sí queda claro es la consecuencia:** el asiento 11 aceptó 104 formas y
las 104 cayeron en el tramo donde el veto duro mata el 100 %. **Su 86,7 % de
aceptación produjo cero llegadas.**

---

## 5 · El precio por minuto de pod

| sonda | partidas | **$/min** |
|---|---|---|
| **P5-8H** | 2 | **0,00411 · 0,00412** |
| **P5-8I** | 9 | 0,00288 a **0,00998** |
| **P5-8K** | 2 | **0,00940 · 0,00941** |

### Y el patrón es nítido: el $/min es del EPISODIO, no del brazo

| semilla | brazo A | brazo K |
|---|---|---|
| P5-8H …0916 | 0,00411 | 0,00412 |
| P5-8I …0374 | 0,00998 | 0,00997 |
| P5-8I …0916 | 0,00991 | 0,00990 |
| **P5-8I …5103** | **0,00289** | **0,00288** |
| P5-8I …5645 | 0,00996 | 0,00990 |
| **P5-8K …0916** | **0,00940** | **0,00941** |

**Los dos brazos de una semilla coinciden en la quinta cifra decimal, y entre
semillas el precio por minuto varía 3,4 veces** (0,00288 a 0,00998). Ni la cola
ni el tiempo de juego lo explican: los tiempos de juego están todos entre 8,4 y
10,6 minutos.

### Lo que esto dice del umbral

**Corrijo lo que escribí ayer.** En `informe_P58K_sonda.md` dije que «el precio
por minuto es el mismo» comparando P5-8K (0,00941) con una partida de P5-8I
(0,00992). **Es verdad para ese par y falso en general**: dentro de P5-8I el
rango es 0,00288-0,00998.

**Y el corolario incómodo: un umbral por minuto NO habría parado P5-8K.** Su
0,00941 $/min está **dentro de la banda normal** —de hecho por debajo de la moda
(0,0099)—. P5-8K fue cara **solo porque el pod vivió 19 minutos en vez de 11**,
por una cola de 8,8 minutos contra los 0,9 de mediana.

**Los números para que fijes la vara:**

| | |
|---|---|
| $/min observado, mediana de 13 partidas | **0,00941** |
| $/min observado, máximo | **0,00998** |
| tiempo de **juego**, mediana | **10,2 min** (rango 8,4-10,6) |
| **cola**, mediana | **0,9 min** (rango **0,4 a 8,8**) |
| con $/min mediano, una partida toca 0,15 $ cuando la cola pasa de | **5,9 min** |

**Un umbral de, por ejemplo, 0,012 $/min dejaría un 20 % de holgura sobre el
máximo observado y no dispararía por cola.** Pero eso significa aceptar que una
tanda de diez puede costar 2,3 $ si la cola es corta y 3,8 $ si es larga, con el
mismo $/min. **La vara es tuya; yo doy los números.**

---

## Lo que no sé, marcado como tal

**No sé si el veto duro evitó daño que no se ve.** Que 102 de 103 vetos no vayan
seguidos de daño es compatible con «el veto no servía» y con «el veto funcionó y
por eso no hubo daño». **El diario no distingue las dos.** Lo que sí puedo
afirmar es que **el coste es cierto (100 % de los viajes de 8-9) y el beneficio
no está demostrado**.

**No sé por qué el tramo 8-9 da exactamente 100 %.** La explicación geométrica
—camino largo, armado que aparece— es coherente con los 98,1 % de «aparece en el
tic», pero **cien de cien es demasiado limpio para que me quede tranquilo**, y
las cien salen de **un solo asiento de un solo episodio**. Podría ser propiedad
de ese mapa y esos dos enemigos con lanza. **Con una partida no lo separo.**

**No sé dónde está el escalón de verdad.** El salto medido es de 6-7 a 8-9, pero
entre esos tramos hay **ocho formas contra cien**. El tramo 6-7 con n = 8 puede
ser 25 % o puede ser 60 %. **El único número sólido es el 100 % de 8-9.**

**Y no sé por qué el $/min varía 3,4 veces entre episodios** con la misma cola y
el mismo juego. Lo que sé ahora, y ayer no, es que **es del episodio y no del
brazo**, y que **es idéntico para los dos brazos de una misma semilla**.

---

## Lo que queda sobre la mesa — sin decidir

Tres cosas que el diagnóstico deja preparadas y que **no toco**:

1. **Un tope de distancia al nacer.** Los datos dicen que por encima de 7 no
   llega ninguna. Un tope en 7 habría dejado a P5-8K con **9 formas de 109**
   —las que sí completan— en vez de 109 con cero llegadas.
2. **La regla del veto duro.** Hoy mata por un armado que *aparece*, aunque esté
   quieto a ocho casillas con una lanza de alcance dos. Una regla que exigiera
   *acercamiento* habría perdonado 101 de los 103 vetos.
3. **El umbral de parada por minuto.** Con los números de arriba.

**El margen, el tope de distancia y la regla del veto duro los decide Manel.**

---

`cantera/paper5/mide_P58L.py` · datos `P58L.json`, `P58L_b.json` · diarios de K
y A de P5-8I y P5-8K. **Gasto: cero.**

**PARO AQUÍ.**
