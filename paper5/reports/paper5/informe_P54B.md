# P5-4B — La confianza se paga por lo nuevo

En seco, coste cero. Nada a la plataforma. **Ninguna decisión real cambia.**
Mismas 2.225 escenas, semilla **20260919**, misma regla (E1+G2, margen 0,02,
comparador en ventana), mismos tres consejeros.

**T6 CUMPLE, y es el resultado del encargo: la moneda de lo nuevo separa por
identidad.** «Nadie se mueve» hace **cero** afirmaciones no triviales, así que
su confianza **nunca sale de 0** en las 40 vidas. El mentiroso acaba por debajo
de 0,2 en **39 de 40**. El oráculo acaba en **1,000 de mediana**.

**Pero T7 y T8 FALLAN, y fallan por la misma razón, que es el hallazgo de
verdad: lo nuevo que el oráculo sabe es, casi todo, una ausencia.** De sus 2.290
afirmaciones no triviales, **2.035 (88,9 %) son «no está»** y solo 255 son una
posición lejos de donde estaba. Y creer una ausencia es buena noticia para
cualquier forma, no solo para la buena: **el azar pasa del 0,77 % al 7,16 %** de
las construidas al mismo tiempo que O-después pasa del 4,52 % al 10,57 %.

**Y hay un precio que conviene decir en voz alta: la moneda de lo nuevo apaga al
consejero que más recuperaba.** En P5-4A «nadie se mueve» recuperaba el 16,5 %
del aporte real de los rivales, más que el oráculo. Aquí no puede: no dice nada
nuevo, no cobra confianza, y se queda en el suelo.

---

## B1 · La ausencia como afirmación

`confianza.py:118-144` (`dice2`). Lo dicho de cada rival es una posición **o**
`AUSENTE`:

| consejero | cuándo dice ausencia |
|---|---|
| **oráculo** | cuando **ningún hermano** vio a ese rival en el tic k (verdad parcial de A0) |
| **mentiroso** | con la **misma frecuencia** que el oráculo, `P_AUS = 0,2173`, **medida** (1.231 de 5.665 sobre 12 diarios); el sorteo es independiente de la verdad, así que no filtra nada |
| **nadie se mueve** | nunca |

**Un cambio de alcance que hay que declarar.** En P5-4A el oráculo solo hablaba
de los rivales que alguien había visto: **12.604 dichos**. Ahora habla de
**exactamente los mismos cinco rivales que los otros dos** —los del juego de
filas del cuerpo— y dice «no está» de los que no ve: **9.974 dichos**, igual que
los otros. Los tres consejeros son por fin comparables afirmación a afirmación.

**Qué le pasa a las filas con una ausencia creída** (`confianza.py:147`,
`obs_con_dicho2`): el rival **sale de `visible.agents`**. Como la `Memoria` de
la tabla **no guarda posiciones de rivales** (`appraisal_zs_v42_exp.py:449-470`,
ya establecido en P5-3G), quitarlo de `visible` lo quita **del todo** de las
cinco filas de rivales. **Las filas que leen memoria siguen leyéndola**: el
agresor de la hermana, por la vía de `mem`, sigue ahí. **La ausencia no borra
recuerdos**, solo quita al rival de la vista y del alcance.

Y entra por la misma puerta de siempre (`mezcla`, `confianza.py:87-93`): una
ausencia **mejora** las filas del rival, así que es buena noticia y **entra
multiplicada por C**. Lo malo se sigue creyendo entero, con C o sin ella.

---

## B2 · La moneda de lo nuevo

C empieza en **0** en cada diario. Solo cuentan las afirmaciones **no
triviales**: posición a **más de 3 casillas** de donde estaba el rival, o
ausencia. Acierto **+0,10**, fallo **−0,20**, acotada en 0 y 1. Lo trivial no
mueve nada, ni arriba ni abajo.

| consejero | dichos | **no triviales** | de ellas, ausencias | **comprobadas** | aciertos | tasa |
|---|---|---|---|---|---|---|
| **oráculo** | 9.974 | **2.290 (22,96 %)** | **2.035 (88,9 %)** | **2.290 (100 %)** | 2.290 | **100,00 %** |
| **nadie se mueve** | 9.974 | **0** | 0 | **0** | 0 | — |
| **mentiroso** | 9.974 | **9.805 (98,3 %)** | 2.239 (22,8 %) | 8.259 (84,2 %) | 460 | **5,57 %** |

**Las tres líneas dicen tres cosas distintas y todas importan.**

1. **«Nadie se mueve» no hace ni una afirmación no trivial.** No es que falle la
   comprobación: es que **por construcción su afirmación es la definición misma
   de trivial**. La moneda funciona exactamente como se diseñó.
2. **El oráculo dice poco nuevo —el 23 %— pero todo lo nuevo que dice se
   comprueba y todo acierta.** Que el 100 % se compruebe no es casualidad: una
   ausencia siempre es comprobable (acierto si nadie lo vio en su alcance) y sus
   posiciones no triviales son, por construcción, de rivales vistos.
3. **El mentiroso dice novedad casi siempre —98,3 %— y acierta el 5,57 %.** Se
   comprueba el 84,2 %; de sus posiciones no triviales se comprueba el 79,6 %,
   la misma cifra de P5-4A. Nada se rompió.

**Trayectoria de C y reparto por vidas:**

| consejero | 0-500 | 500-1500 | >1500 | **C final (mediana)** | media | **>0,8** | **<0,2** |
|---|---|---|---|---|---|---|---|
| **oráculo** | 0,600 | **1,000** | **1,000** | **1,000** | 0,778 | **27/40** | 6/40 |
| **nadie se mueve** | 0,000 | 0,000 | 0,000 | **0,000** | 0,000 | 0/40 | **40/40** |
| **mentiroso** | 0,000 | 0,000 | 0,000 | **0,000** | 0,010 | 0/40 | **39/40** |

Contra P5-4A, donde los tres acababan con mediana 1,000, 1,000 y 0,000: **la
única fila que cambia es la de «nadie se mueve», y cambia entera**, de 1,000 a
0,000. Eso es lo que la moneda de lo nuevo vino a hacer.

---

## B3-B4 · La tabla

Universo **908** formas construidas por llave. «En la mesa» = aceptada sobre las
que pasan la regla; el denominador es pequeño y por eso va con intervalo. Las
tasas de la mesa son las del banco de la confianza, que incluye el paso de la
mesa (`compite`); no son las de P5-3H, medidas de otro modo.

**Con «nadie se mueve» y con el mentiroso, C = 0 en todas las vidas, así que los
seis modos de B3 dan la misma fila.** Se escribe una vez y se dice.

| consejero · modo | **O-después pasa** | acepta | **mesa** (IC95) | **azar pasa** | acepta | mesa (IC95) | **diferencia** (IC95) | O-ahora |
|---|---|---|---|---|---|---|---|---|
| **oráculo · lineal** | 92 (10,13 %) | 51 | **55,43 %** (45,3-65,2) | 69 (7,60 %) | 23 | 33,33 % (23,4-45,1) | **+22,10** (+6,57, +36,05) | 100,00 % |
| **oráculo · umbral 0,7** | **96 (10,57 %)** | 50 | 52,08 % (42,2-61,8) | 65 (7,16 %) | 23 | 35,38 % (24,9-47,5) | **+16,70** (+1,05, +31,01) | 100,00 % |
| **nadie · los seis** | 41 (4,52 %) | 24 | **58,54 %** (43,4-72,2) | **7 (0,77 %)** | 2 | 28,57 % (8,2-64,1) | **+29,97** (−8,67, +54,50) | 100,00 % |
| **mentiroso · los seis** | 35 (3,85 %) | 23 | **65,71 %** (49,2-79,2) | **0 (0,00 %)** | **0** | — | **+65,71** (+49,15, +79,17) | 100,00 % |

Sobre las **construidas**, que es el denominador honesto:

| consejero · modo | O-después acepta | azar acepta | diferencia (IC95) |
|---|---|---|---|
| oráculo · lineal | 5,62 % | 2,53 % | **+3,08** (+1,27, +4,97) |
| oráculo · umbral 0,7 | 5,51 % | 2,53 % | **+2,97** (+1,17, +4,85) |
| nadie · los seis | 2,64 % | 0,22 % | **+2,42** (+1,39, +3,69) |
| mentiroso · los seis | 2,53 % | **0,00 %** | **+2,53** (+1,59, +3,77) |

**Lineal contra umbral, en el oráculo: casi lo mismo, y el umbral algo peor.**
El umbral deja pasar cuatro formas más de O-después (96 contra 92) y cuatro
menos de azar (65 contra 69), pero acepta una menos en la mesa, y la diferencia
baja de +22,10 a +16,70. **Con C que acaba en 1,000 en la mayoría de las vidas,
el umbral y el lineal convergen**: la diferencia está solo en los primeros
quinientos instantes, donde el lineal deja entrar un poco y el umbral nada.

### La recuperación del aporte real de los rivales

Medida con C = 1 fija sobre las formas **aceptadas** en el modo umbral 0,7,
contra los totales reales de F2 (rivales 104,568 · hermano 85,335 · propias
22,378). **Es una suma sobre las aceptadas, así que escala con cuántas se
aceptan**: la cifra total y la cifra por forma dicen cosas distintas y van las
dos.

| consejero | aceptadas | **rivales** | **% del real** | **por forma** | hermano | propias |
|---|---|---|---|---|---|---|
| **oráculo** | 50 | +15,489 | **14,81 %** | **0,310** | +6,688 = 7,84 % | +2,208 = 9,87 % |
| **nadie se mueve** | 24 | +3,654 | **3,49 %** | 0,152 | +3,216 = 3,77 % | +0,205 = 0,91 % |
| **mentiroso** | 23 | +0,307 | **0,29 %** | 0,013 | +2,705 = 3,17 % | +0,376 = 1,68 % |

**Comparado con P5-4A (C = 1, sin ausencias):**

| consejero | A: total | A: por forma | **B: total** | **B: por forma** |
|---|---|---|---|---|
| oráculo | 14,0 % (93 formas) | 0,157 | **14,81 %** (50) | **0,310** |
| nadie se mueve | **16,5 %** (96 formas) | 0,180 | 3,49 % (24) | 0,152 |
| mentiroso | 0,8 % (30 formas) | 0,028 | 0,29 % (23) | 0,013 |

**Aquí está el resultado más interesante del encargo, y no lo predecía ningún
sello.** En total, el oráculo apenas se mueve: 14,0 → 14,8 %. **Pero por forma
aceptada casi dobla: 0,157 → 0,310.** Las ausencias son informaciones grandes:
quitar un rival de la vista vale mucho más que corregir su posición tres
casillas. **Y por primera vez el oráculo gana a «nadie se mueve»** (0,310 contra
0,152), que era exactamente lo que T1 no consiguió en P5-4A.

Lo que pasa es que la recuperación total no sube, porque **la regla acepta la
mitad de formas que antes** (50 contra 93). Se gana en calidad por forma y se
pierde en cantidad.

### El coste

| consejero | mediana | máximo |
|---|---|---|
| nadie | 12,61 ms | 47,97 |
| **oráculo** | **13,12 ms** | 68,98 |
| mentiroso | 12,38 ms | 55,11 |

Igual que en P5-4A (12,1-12,3 ms) y el triple que E1+G2 (4,39 ms). **La ausencia
no cuesta nada**: es un borrado en el diccionario de visibles.

---

## B5 · Sensibilidad

Umbral 0,5 y 0,9, y la pareja de premios de A4 (subida 0,05 / bajada 0,10).
**Solo el oráculo tiene filas distintas**: con C = 0 en las 40 vidas, «nadie se
mueve» y el mentiroso dan la misma fila en las seis combinaciones.

| consejero | modo | premio/castigo | O-después pasa | acepta | mesa | azar pasa | acepta | **diferencia** |
|---|---|---|---|---|---|---|---|---|
| **oráculo** | lineal | 0,10 / 0,20 | 92 (10,13 %) | 51 | 55,43 % | 69 | 23 | **+22,10** |
| **oráculo** | umbral **0,5** | 0,10 / 0,20 | **101 (11,12 %)** | **54** | 53,47 % | 72 | 24 | **+20,13** |
| **oráculo** | umbral 0,7 | 0,10 / 0,20 | 96 (10,57 %) | 50 | 52,08 % | 65 | 23 | +16,70 |
| **oráculo** | umbral **0,9** | 0,10 / 0,20 | 80 (8,81 %) | 46 | **57,50 %** | 57 | 21 | **+20,66** |
| **oráculo** | lineal | **0,05 / 0,10** | 86 (9,47 %) | 46 | 53,49 % | 57 | 21 | +16,65 |
| **oráculo** | umbral 0,7 | **0,05 / 0,10** | 77 (8,48 %) | 45 | **58,44 %** | 50 | 20 | +18,44 |
| nadie | los seis | ambas | 41 (4,52 %) | 24 | 58,54 % | 7 | 2 | +29,97 |
| mentiroso | los seis | ambas | 35 (3,85 %) | 23 | 65,71 % | **0** | **0** | +65,71 |

**Nada depende del umbral.** De 0,5 a 0,9 lo que pasa la regla va del 11,12 % al
8,81 % y la diferencia en la mesa se mueve entre +16,70 y +20,66, con intervalos
que se solapan enteros. **Y la moneda más lenta (0,05/0,10) hace lo mismo, un
poco más despacio**: 8,48 % contra 10,57 %, diferencia +18,44 contra +16,70.
Todas las filas del oráculo caben en la misma franja. **La decisión de dónde
poner el umbral no es una decisión importante; la de qué cuenta como novedad,
sí.**

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **T6** | «nadie se mueve» por debajo de 0,2 en más del 80 % de las vidas (hoy 1,0) | B2 | **40/40 = 100 %**, C = 0,000 siempre | **CUMPLE** |
| **T6** | el oráculo acaba por encima de 0,8 | B2 | mediana **1,000**; por vidas, **27/40 = 67,5 %** | **a medias** |
| **T6** | el mentiroso por debajo de 0,2 en más del 80 % | B2 | **39/40 = 97,5 %** | **CUMPLE** |
| **T7** | con ausencias y umbral, el oráculo recupera más del 30 % del aporte de los rivales (hoy 14 %) | B4 | **14,81 %** | **FALLA** |
| **T7** | …y O-después pasa la regla en más del 12 % de las construidas (hoy 4,5 %) | B4 | **10,57 %** (11,12 % con umbral 0,5) | **FALLA** |
| **T8** | con umbral, la diferencia en la mesa por encima de 30 puntos para el oráculo | B4 | **+16,70** | **FALLA** |
| **T8** | …y con lineal, baja | B4 | **+22,10**, o sea **sube** | **FALLA** |
| **T9** | el mentiroso, con B2 y umbral, no cuela ninguna forma de azar | B4 | **0 de 908**, y ni una llega siquiera a la mesa | **CUMPLE** |
| **T10** | O-ahora 100 % en todo | B4 | **2.225 de 2.225** en los tres consejeros y los seis modos | **CUMPLE** |

**Los contadores podían variar, comprobado.** El de T6 va de 0/40 a 40/40 según
consejero, y la fila de «nadie se mueve» se movió entera respecto a P5-4A
(0/40 → 40/40). El de T7 va del 0,29 % al 14,81 % según consejero, y lo que pasa
la regla va del 3,85 % al 11,12 % según consejero y modo. El de T8 va de +16,65
a +65,71. El de T9 va de 0 a 24 formas de azar aceptadas en la misma tabla.

### Por qué T7 y T8 fallan, con el número delante

**T7 y T8 se sellaron esperando que creer ausencias fuera una ventaja del que
sabe.** No lo es, porque **la ausencia es buena noticia para las dos curvas**.
Por la regla de la mezcla, lo bueno entra multiplicado por C, y cuando C llega a
1 el oráculo se cree **todas** sus ausencias —el 88,9 % de su novedad—, lo cual
aligera las filas de rivales tanto en la forma buena como en la de azar. El
resultado se lee en una línea de la tabla: **de «nadie» al oráculo con umbral, el
azar que pasa la regla se multiplica por nueve (7 → 65) mientras O-después se
multiplica por 2,3 (41 → 96)**. La diferencia en la mesa cae de +29,97 a +16,70
por eso, no por un defecto del umbral.

**Es el mismo muro de P5-3F, visto desde otro lado.** El 87 % de la mejora real
está en dónde acaban los otros; una ausencia dice dónde **no** está uno, que es
mucho menos de lo que hace falta.

---

## Lo que P5-4B deja dicho

1. **La moneda de lo nuevo hace su trabajo: separa por identidad.** El que no
   dice nada nuevo se queda en cero (0 afirmaciones no triviales de 9.974), el
   que miente se queda en cero (5,57 % de acierto), el que sabe llega a 1,000 con
   el 100 % de aciertos. **Eso lo arregla P5-4A**, donde el trivial empataba con
   el oráculo en mediana.
2. **Y tiene un precio, que es el hallazgo negativo del encargo: apaga al que más
   recuperaba.** «Nadie se mueve» recuperaba el 16,5 % del aporte de los rivales
   en P5-4A **precisamente por ser trivial** —en el horizonte de una forma los
   rivales casi no se mueven, así que suponer que se quedan quietos es una
   suposición buena—. Castigar la trivialidad tira esa suposición buena junto con
   la inútil. **Premiar la novedad y premiar la utilidad no son lo mismo en este
   mundo.**
3. **Por forma, la verdad ahora sí gana.** 0,310 contra 0,152 de recuperación por
   forma aceptada: **el oráculo dobla su rendimiento por forma gracias a las
   ausencias** y adelanta por primera vez al trivial. Lo que no consigue es
   aceptar más formas.
4. **El umbral no es un parámetro que importe.** De 0,5 a 0,9, y con las dos
   monedas, todo cabe entre +16,65 y +20,66 con intervalos solapados.
5. **El mentiroso queda mejor apagado que en P5-4A:** cero formas de azar y ni
   una que llegue a la mesa. Sigue en pie el artefacto declarado en T2: miente
   **también sobre las formas propias**, así que parte de su inocuidad es del
   diseño, no de la confianza.
6. **Y O-ahora sigue en 100,00 % en los dieciocho casos.** Ensanchar la puerta no
   ha roto nunca lo que ya funcionaba, en ningún banco de esta sección.

**Lo que esto sugiere y NO he ejecutado** (propuesta, no decisión): si lo que
queremos premiar es **informar**, la moneda tendría que pagar por **reducir la
incertidumbre del cuerpo** —cuánto cambia la forma al creer lo dicho— y no por
ser distinto de lo de antes. Un consejero que diga la verdad trivial sería
premiado por lo que vale, y uno que diga novedades inútiles no. Eso es un
mecanismo nuevo y lo dejo sobre la mesa.

**PARO AQUÍ.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`: **ninguno de
los dos se ha tocado.** Ficheros de este encargo: `confianza.py`
(`72018777fcb18c8e7f18e7720c913020`, con el bloque P5-4B: `AUSENTE`, `dice2`,
`obs_con_dicho2`, `no_trivial`, `actualiza_C2`), `banco_confianza2.py`
(`5902fbb8a57a98961c5fde45fdf9c61c`), `P54B_nadie.json`, `P54B_oraculo.json`,
`P54B_mentiroso.json`, y los seis logs `P54B_*_corrida.log` /
`P54B_*_progreso.log`.

Las tres corridas: **2 min 22 s en total** (17:34:58 → 17:37:20).
