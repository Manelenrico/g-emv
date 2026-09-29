# P5-8O — ¿Anduvo el cuerpo las formas del consejero?

Diagnóstico **en seco**, **coste cero**. Sin imagen, sin plataforma. Motor,
decisor y tabla intocados, idénticos al empezar y al acabar. **Sin sellos.**

Cien partidas de P5-6C, brazos F (consejero) y T (azar), más las veinte de A
como referencia.

---

## El titular

**Sí, el cuerpo anduvo las formas del consejero — y las anduvo bastante más de
lo que anda sus propias metas.**

| | **F** (consejero) | **T** (azar) | **A** (sus propios `ir_`) |
|---|---|---|---|
| gana el paso de la forma, con piernas listas | **76,8 %** | **64,7 %** | — |
| movimientos que **acercan** al destino | 55,8 % | **66,3 %** | 55,3 % |
| **«andadas»** (recorre al menos la mitad) | **44,4 %** | **63,4 %** | **27,2 %** |
| **llegan al destino** | **22,2 %** | **51,2 %** | **1,2 %** |

**Y tu hipótesis del punto 3 sale al revés de lo temido.** De las formas que
cumplen la proyección, **las andadas son la inmensa mayoría**: 9 de 12 en F
(75 %) y 16 de 18 en T (89 %). **La proyección no se cumplía sola por quedarse
quieto.**

**Esto separa netamente las formas del consejero de las de curiosidad.** En
P5-8G el paso de la forma de curiosidad ganaba el **54,2 %** de las discusiones
con piernas listas y el cuerpo recorría **una casilla** en toda la vida de la
forma. Aquí gana el **76,8 %** y **una de cada dos formas de T llega**.

**Pero hay un pero grande, y es de tamaño:** todo esto sale de **86 formas**, con
vidas medianas de **25 tics** y destinos a **2 o 3 casillas**. **Son viajes
cortos.** No es lo mismo que el cuerpo ande cuatro casillas que ande la forma.

---

## Custodia

```
motor/model.py                          1e511978c251130e95169ebf8443efa1
paintball/alma/decisor_zs.py            8fa03547e3228ef9df4aa94c444f9252
paintball/alma/appraisal_zs_v42_exp.py  98c13d60167c80cc8334c965be75c640
```
Idénticos al empezar y al acabar. `cantera/paper5/mide_P58O.py` · datos
`P58O.json`. **Gasto: cero.**

---

## 1 · La reconstrucción de las ventanas

**La ventana no hubo que inventarla: estaba en el diario, en registros que
P5-8G no usó.**

| | |
|---|---|
| formas **aceptadas** en F y T (`forma_aceptada`) | **93** |
| con ventana **reconstruible** | **86 = 92,5 %** |
| **no reconstruibles** | **7** |

**Las siete, por la misma razón: ventana de menos de dos tics vivos.** Son formas
aceptadas en los últimos instantes del asiento, o cuyo cierre cae después de la
muerte del cuerpo. No hay nada que medir en ellas.

### Cómo se cerró cada ventana

| | n |
|---|---|
| **«en la reevaluación deja de ganar (area)»** | **67** |
| **sin cierre → llegada proyectada** (el último punto de control de `forma_aceptada.tics`) | **17** |
| «en la reevaluación deja de ganar (vida)» | 1 |
| «la vida real 16 está por debajo de la proyectada» | 1 |

**Cuatro de cada cinco formas mueren en la reevaluación, no por llegar ni por
fallar un punto de control.**

### Lo que P5-8G no tenía

P5-8G usó `forma_tic`, que **solo se escribe cuando hubo inyección**, y por eso
su columna «el candidato no está» salía 3,45 % y 0,00 % por construcción, con 9
formas por brazo. **Aquí la ventana sale de `forma_aceptada` → `forma_caida`,
que son registros de censo**, y las formas pasan de 9 a **86**.

**Las 86 tienen destino.** Ninguna forma aceptada era solo de `esperar`/`usar`;
todas tienen al menos un tramo con destino. *(Reparto de tramos por forma: 3
tramos en 52 formas, 4 en 14, 2 en 17, 1 en 3.)*

---

## 2 · ¿Anduvo el cuerpo?

Sobre las 86, con el destino del **primer tramo que tiene uno**:

| | **F** (45 formas) | **T** (41 formas) |
|---|---|---|
| vida mediana de la forma | 32 tics | 22 tics |
| tics con piernas listas | 280 | 116 |
| **gana el paso de la forma** | **215 = 76,8 %** | **75 = 64,7 %** |
| movimientos | 138 | 86 |
| **que acercan al destino** | **77 = 55,8 %** | **57 = 66,3 %** |
| **distancia al nacer → al cerrar** | **3 → 2** (mínima 1) | **2 → 1** (mínima 0) |
| **llegan al destino del primer tramo** | **10 = 22,2 %** | **21 = 51,2 %** |
| **«andadas»** (recorre ≥ la mitad) | **20 = 44,4 %** | **26 = 63,4 %** |

**T anda mejor que F, y eso es lo primero que llama la atención.** Las formas del
azar se cumplen más, se andan más y llegan más del doble que las del consejero.
**La explicación más simple es la distancia**: T propone destinos a **2** casillas
de mediana y F a **3**. Un destino más cerca se alcanza más.

*(Rango de distancias: F de 1 a 8, T de 1 a 10.)*

---

## 3 · El cruce con «cumple proyección»

### Primero, el control: reproduzco la cifra de P5-6C

P5-6C midió «cumple proyección» **por punto de control**, con el criterio
`d_real ≤ d_proyectada + 0,05` (`analiza_P56C.py:322`).

| | puntos de control | cumplen | **P5-6C publicó** |
|---|---|---|---|
| **F** | 71 | **39,4 %** | 42,3 % |
| **T** | 36 | **61,1 %** | **61,1 %** |

**T sale exacto. F sale 2,9 puntos por debajo**, y la razón es que yo uso solo
las 86 formas reconstruibles y P5-6C usó todos los puntos de control del
conjunto. **El control vale: la cifra de P5-6C es la que creía ser.**

*(El veredicto que el propio diario escribe, `acierto`/`fallo`, coincide punto a
punto con ese criterio: 28/71 y 22/36 en los dos casos.)*

### Y ahora el cruce

**Solo 66 de las 86 formas llegaron a tener algún punto de control evaluado: 20
(el 23 %) murieron antes del primero.**

**F** (37 formas con punto de control)

| | andada | NO andada |
|---|---|---|
| **cumple** | **9** | 3 |
| no cumple | 10 | 15 |

**T** (29 formas con punto de control)

| | andada | NO andada |
|---|---|---|
| **cumple** | **16** | 2 |
| no cumple | 7 | 4 |

| | de las que **cumplen**, ¿cuántas andadas? | de las **andadas**, ¿cuántas cumplen? |
|---|---|---|
| **F** | **9 de 12 = 75 %** | 9 de 19 = 47 % |
| **T** | **16 de 18 = 89 %** | 16 de 23 = 70 % |

**Tu hipótesis era que las que cumplen fueran sobre todo las NO andadas — la
forma diría «quédate» y la proyección se cumpliría sola. Los datos dicen lo
contrario: tres de cada cuatro en F y nueve de cada diez en T de las que cumplen
fueron andadas.**

**Así que la cifra de P5-6C no mide «el cuerpo se quedó quieto».** Mide, sobre
todo, formas que el cuerpo anduvo.

**Lo que sí hay que decir de esa cifra es otra cosa:** se calcula sobre los **107
puntos de control** de las formas que sobrevivieron lo bastante para tener uno,
que son **66 de 93 aceptadas**, que a su vez son **93 de 4.548 evaluadas**. **El
42,3 % y el 61,1 % describen un superviviente muy seleccionado.**

---

## 4 · La referencia del brazo A

**El brazo A de P5-6C no lleva formas**: `consejero_forma` dice «apagado» y
`forma_resumen` da `llamadas: 0` en los veinte asientos. **No hay «formas del
puñado propio» que leer.**

**Lo que sí permite el diario**, y construyo como referencia: las decisiones en
que el cuerpo eligió un `ir_` **cuyo destino se puede leer**:

| candidato | de dónde sale el destino | n |
|---|---|---|
| `ir_centro` | `zona.center` | 2.690 |
| `ir_botin` | `RADIOGRAFIA.ahora.botin.objetivo` | 2.499 |
| `ir_pareja` | `social.pareja_pos` | 1.662 |

**Los demás `ir_` no traen destino en el diario y quedan fuera.** Se mide sobre
la misma ventana que las formas: **25 tics**, la mediana de vida de las 86.

| | **A** (6.620 casos con el cuerpo aún no en el destino) |
|---|---|
| **«anduvo»** (recorre ≥ la mitad) | **27,2 %** |
| **llega** | **1,2 %** |
| movimientos que acercan | 55,3 % |
| distancia al empezar → al acabar | **4 → 3** (mínima 3) |

### La comparación

| | anduvo | llega | movimientos que acercan | distancia al nacer |
|---|---|---|---|---|
| **F** | **44,4 %** | **22,2 %** | 55,8 % | 3 |
| **T** | **63,4 %** | **51,2 %** | **66,3 %** | 2 |
| **A** | 27,2 % | 1,2 % | 55,3 % | **4** |

**Las formas del consejero se andan y se alcanzan más que las metas que el
cuerpo se pone solo.** Pero **la comparación no es limpia y no la voy a vender
como tal**: los destinos de A están más lejos (mediana 4 contra 3 y 2), y dos de
los tres se mueven o son abstractos —el centro de la zona se desplaza con el
anillo, y la pareja anda—. **Que A llegue al 1,2 % dice tanto de la naturaleza de
sus metas como de su empeño.**

**La fracción de movimientos que acercan es lo más comparable de las tres filas,
porque no depende de la distancia: F 55,8 %, A 55,3 %, T 66,3 %.** Por esa vara,
**F y A son indistinguibles y solo T destaca.**

---

## Un error mío, cazado antes de publicarlo

La primera pasada del cruce dio **cero formas que cumplen**, en los dos brazos.
Era mío: busqué `veredicto == "ok"` cuando el diario escribe **`acierto`** y
**`fallo`**. **Un cero por un literal mal escrito.**

Lo encontré porque el cero era incompatible con el 42,3 % que P5-6C había
publicado, y antes de escribirlo fui a mirar de dónde salía aquella cifra — y de
paso descubrí que **se medía por punto de control y no por forma**, que es un
matiz que este informe necesitaba.

**Es el quinto cero mío de la serie que resulta ser un contador mal apuntado.**
Por eso el informe lleva ahora, arriba del cruce, **el control de que reproduzco
la cifra publicada**.

---

## Lo que no sé, marcado como tal

**No sé si 86 formas bastan.** Salen de 4.548 evaluadas en cien partidas: **el
2 % pasó la puerta**. Todo lo de arriba describe ese 2 %.

**No sé por qué T anda mejor que F.** La distancia menor (2 contra 3) lo explica
en parte, pero **no lo he separado**: haría falta comparar F y T a igualdad de
distancia, y con 45 y 41 formas los tramos quedan casi vacíos.

**No sé qué habría pasado con viajes largos.** Las 86 formas tienen destinos a
mediana 2-3 casillas y viven 25 tics. **El resultado de P5-8G —que el cuerpo no
sigue la forma— se midió sobre formas de curiosidad con destinos a 4-8 casillas.
Puede que la diferencia entre los dos diagnósticos sea la distancia y no el
origen de la forma.** Es comprobable en seco y no está en este encargo.

**Y no sé si «andada» es la vara correcta.** «Recorrer al menos la mitad del
camino» la elegí yo; con otro umbral las tablas del punto 3 cambiarían de
tamaño, aunque el signo —las que cumplen son las andadas— aguanta en los dos
brazos y es lo bastante grande (75 % y 89 %) para no depender del corte.

---

## Lo que esto deja

**La pregunta de P5-8G queda contestada y corregida.** Allí, con 9 formas por
brazo y una columna sesgada, quedó la sospecha de que el 42,3 % y el 61,1 %
midieran «la distracción del cuerpo». **Con 86 formas y ventanas de censo, no:
miden formas que el cuerpo anduvo.**

**Y deja una pregunta nueva que me parece la buena:** el cuerpo anda bien las
formas cortas —las del consejero, a dos o tres casillas— y no anda las largas
—las de curiosidad, a cuatro u ocho—. **Si eso es así, el problema de toda la
serie 8 no era de quién propone la forma, sino de cuánto pide andar.**

**No lo afirmo: lo propongo, y es medible en seco sobre lo que ya hay.**

**PARO AQUÍ.**
