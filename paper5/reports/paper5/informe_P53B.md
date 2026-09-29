# P5-3B — La forma y la regla, en banco

En seco, coste cero. Nada a la plataforma. **Ninguna decisión real cambia**: la
forma vive en `cantera/paper5/forma.py`, fuera del decisor.

Mismos 40 diarios, misma semilla **20260919**, **las mismas 2.230 escenas** de
P5-2, para que todo se compare una a una con P52c.

**R2 se cumple, y por mucho.** Con el criterio de vida entera, la forma del
futuro bueno gana **70,88 %** contra el **46,79 %** del azar emparejado: **24,08
puntos**, con el cero muy fuera del intervalo. La puerta ancha **sí ve el
después**, donde la de hoy no veía nada (8,5 contra 7,2 en P5-2c).

**Pero R6 falla, y falla fuerte.** Una curva al azar también gana a seguir solo
el **46,79 %** de las veces, contra el 10 % sellado. La puerta ancha ve el
después **y deja pasar mucho ruido**.

---

## El arnés, con la forma apagada

```
REPRODUCCION CON LA PROYECCION IMPORTADA: 11,804/11,804 = 100.00 %
```

Con `proyeccion.py` y `forma.py` importados, el arnés sigue reproduciendo el
**100,00 %** de las decisiones. La corrida completa de los 40 diarios ya quedó
en 100,00 % sobre 112.865 tics en P5-2c.

---

## B0 · Cuánto se desvía de sí mismo el cuerpo de hoy

| | |
|---|---|
| escenas | 2.230 |
| escenas en que el ganador del cuerpo **tenía destino** | **89** (4,0 %) |
| de esas, **llegó al destino que quería** en 100 tics | **35 = 39,3 %** |
| tic mediano de llegada | **1** |

**Dos lecturas, y las dos importan.** La primera: en el 96 % de las escenas el
cuerpo **no quiere ir a ninguna parte** —su ganador es `noop`, `usar` o
`atacar`— así que no hay destino del que desviarse. La segunda: cuando sí quiere
ir, **se desvía seis de cada diez veces**. El tic mediano de llegada es 1 porque
la mayoría de esos destinos son la casilla de al lado.

Esto es el contexto de todo lo que sigue: el cuerpo de hoy no persigue planes,
porque casi nunca tiene uno.

---

## B1 · La forma, con un ejemplo entero

Una forma es una lista de **tramos**; cada tramo es un destino más una intención
(`ir` / `coger` / `usar` / `esperar N`). **Los puntos de control no van a un H
fijo:** van al tic de llegada de cada tramo, con los **11 tics por paso** del
manual §4 más las esperas.

En cada punto se arma una **foto proyectada**:

| pieza | de dónde sale |
|---|---|
| nosotros | `proyectar()` de P5-3A: pos, vida, mano, cuerpo, mochila, efectos |
| **el anillo** | su estado **real** en ese tic, `mundo.anillo_en(tick)`, determinista |
| **el suelo** | los objetos tal como estaban en `t`, menos los cogidos |
| **los rivales** | **congelados donde estaban en `t`** |

**Declarado: la forma es ciega a los otros.** No proyecta ni su movimiento ni su
daño. Es la misma ceguera que P5-3A midió como techo.

Sobre esa foto se llama a la **tabla** (`appraise`) y al **motor**
(`opponent_distance`) y sale la `d` del punto. Eso es la curva.

### El ejemplo: diario `ereq_051a3cdd-…-a10`, tic 300

**Los tramos**, sacados del camino que el cuerpo hizo de verdad:

| # | destino | intención |
|---|---|---|
| 1 | (20, 23) | ir |
| 2 | (21, 23) | **usar** |
| 3 | (24, 23) | ir |

**Los puntos de control y sus fotos proyectadas:**

| punto | tic | pos | vida | W | **d de la forma** | **d de seguir solo** |
|---|---|---|---|---|---|---|
| 1 | **344** | (20, 23) | 89,0 | 1,0 | **3,28618** | 3,72554 |
| 2 | **355** | (21, 23) | 89,0 | 1,0 | **3,19465** | 3,72554 |
| 3 | **388** | (24, 23) | 89,0 | 1,0 | **3,21742** | 3,78367 |

Los tics salen de la aritmética del mundo: cuatro pasos desde (24,24) a (20,23)
son 44 tics (300 + 44 = 344); un paso más, 11 (355); tres pasos más, 33 (388).

**El área ponderada:**

| punto | tic | peso `0,5^(dt/50)` | d_solo − d_forma | aporta |
|---|---|---|---|---|
| 1 | 344 | 0,54337 | 0,43936 | **+0,23873** |
| 2 | 355 | 0,46652 | 0,53089 | **+0,24767** |
| 3 | 388 | 0,29525 | 0,56625 | **+0,16719** |
| | | | **área** | **+0,65358** |

Ningún punto baja de `VIDA_MIN = 15`, y el área es positiva: **aceptada**.

---

## B2 · Seguir solo

La curva de comparación es la del **candidato ganador del cuerpo en `t`** —su
paso de siempre— seguido de esperar, y se evalúa **en los mismos tics de
control** que la forma. Así la resta punto a punto tiene sentido y los sesgos de
la proyección, que P5-3A midió, se cancelan entre las dos curvas.

## B3 · La regla

Una forma se acepta si **(1)** ningún punto de control tiene vida proyectada por
debajo de `VIDA_MIN` y **(2)** el área ponderada es mayor que cero, con
peso `0,5 ^ (tic del punto / 50)`.

**Un arreglo declarado, y era mío.** En la primera corrida aplicaba la regla
**antes** de mirar si la forma coincide con el cuerpo. O-ahora propone
exactamente lo que el cuerpo iba a hacer, así que su curva y la de «seguir
solo» son **idénticas** y el área vale **cero exacto**; con «área > 0» las
tumbaba todas y R3 salía 0 %. El B3 del encargo dice que coincide es «si su
primer tramo es el mismo que el ganador del cuerpo», así que eso se decide
**antes**. Corregido y relanzado.

### Qué dice la regla, por llave

| llave | coincide | **acepta (ok)** | rechaza por **vida** | rechaza por **área** | total |
|---|---|---|---|---|---|
| **O-ahora** | **2.230** | — | — | — | 2.230 |
| **O-después** | 2 | **568** | **22** | **316** | 908 |
| **azar emparejado** | — | **421** | **29** | **458** | 908 |
| **QUÉDATE** | **125** | — | — | — | 125 |

### `VIDA_MIN` a 10 y a 20

| llave | vida_min = 10 | **= 15** | = 20 |
|---|---|---|---|
| O-después | ok 571 · vida **14** · área 321 | ok 568 · vida **22** · área 316 | ok 567 · vida **24** · área 315 |
| azar emparejado | ok 424 · vida **19** · área 465 | ok 421 · vida **29** · área 458 | ok 420 · vida **30** · área 458 |

**El umbral casi no manda.** Moverlo de 10 a 20 cambia **8 formas de 908** en
O-después y 11 en el azar. Quien decide es el área, no la vida mínima.

---

## B4 y B5 · Las llaves, y las medidas

| criterio | llave | aceptada | coincide | rechazada | rech. vida | rech. área | vetada | **acept+coin / en la mesa** |
|---|---|---|---|---|---|---|---|---|
| **estricto** | O-ahora | 0 | **2.230** | 0 | 0 | 0 | 0 | **100,00 %** |
| | O-después | 15 | 2 | 6 | 22 | 316 | **547** | 73,91 % (n=23) |
| | azar empar. | 8 | 0 | 20 | 29 | 458 | 393 | 28,57 % (n=28) |
| | QUÉDATE | 0 | **125** | 0 | 0 | 0 | 0 | **100,00 %** |
| **ventana** | O-ahora | 0 | **2.230** | 0 | 0 | 0 | 0 | **100,00 %** |
| | O-después | 339 | 2 | 229 | 22 | 316 | 0 | 59,82 % (n=570) |
| | azar empar. | 122 | 0 | 299 | 29 | 458 | 0 | 28,98 % (n=421) |
| | QUÉDATE | 0 | **125** | 0 | 0 | 0 | 0 | **100,00 %** |
| **vida entera** | O-ahora | 0 | **2.230** | 0 | 0 | 0 | 0 | **100,00 %** |
| | **O-después** | **402** | 2 | 166 | 22 | 316 | 0 | **70,88 %** (n=570) |
| | **azar empar.** | **197** | 0 | 224 | 29 | 458 | 0 | **46,79 %** (n=421) |
| | QUÉDATE | 0 | **125** | 0 | 0 | 0 | 0 | **100,00 %** |

### La diferencia central

| denominador | O-después | azar emparejado | **diferencia** | IC95 |
|---|---|---|---|---|
| las que llegan a la mesa | **70,88 %** (404/570) | **46,79 %** (197/421) | **+24,08 pts** | **+18,03 a +30,14** |
| **todas** las formas construidas | 44,49 % (404/908) | 21,70 % (197/908) | **+22,80 pts** | **+18,60 a +27,00** |

**Con los dos denominadores la diferencia pasa de 22 puntos y el cero queda muy
fuera.**

### Dónde pierde la forma

**En el rechazo por área, casi siempre en el PRIMER punto de control:**

| llave | punto 1 | punto 2 | punto 3 | punto 4 |
|---|---|---|---|---|
| O-después | **244 de 316** (77,2 %) | 35 | 16 | 21 |
| azar emparejado | **434 de 458** (94,8 %) | 24 | — | — |

**En el rechazo en la mesa**, la fila que más pesa (n muy pequeña, porque casi
todo se decide antes, en la regla):

| llave | exposición | carencia | anticipación | n |
|---|---|---|---|---|
| O-después | 4 | 2 | — | **6** |
| azar emparejado | 17 | 2 | 1 | **20** |

### La tabla comparativa con P5-2c: puerta de hoy contra puerta ancha

Mismas escenas, mismo criterio de vida entera:

| | **puerta de hoy** (P5-2c) | **puerta ancha** (aquí) |
|---|---|---|
| O-después | **8,52 %** (72/845) | **70,88 %** (404/570) |
| azar emparejado | **7,22 %** (61/845) | **46,79 %** (197/421) |
| **diferencia** | **+1,30 pts** · IC95 **−1,27 a +3,87** | **+24,08 pts** · IC95 **+18,03 a +30,14** |
| ¿distingue? | **no** (el cero dentro) | **sí** (el cero muy fuera) |

---

## B6 · La figura

`cantera/paper5/figB/B6_formas.png`. Tres escenas, una por veredicto, con la
curva de la forma y la de seguir solo superpuestas y los puntos de control
marcados; la aspa marca vida por debajo de 15.

**Lo que enseña el tercer panel** es lo que no esperaba: el rechazo por área del
tic 1.600 tiene **área exactamente +0,000** y las dos curvas se **superponen
punto por punto**. No es que la forma sea peor: es que es **igual**, y la regla
pide «mayor que cero». Una parte de los 316 rechazos por área de O-después son
empates exactos, no derrotas.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **R2** | con vida entera, O-después gana al azar por más de 10 puntos, cero fuera del intervalo | B5 | **+24,08 pts**, IC95 **+18,03 a +30,14** | **CUMPLE** |
| **R3** | O-ahora: 100 % aceptada+coincide en los tres criterios | B5 | **2.230 de 2.230 = 100,00 %** en los tres | **CUMPLE** |
| **R4** | la vida mínima firma más del 5 % de los rechazos de O-después | B5 | 22 de 504 = **4,37 %** (todos los rechazos) · 22 de 338 = **6,51 %** (solo los de la regla) | **FALLA** con el denominador ancho, cumple con el estrecho |
| **R4** | la exposición deja de firmar más de la mitad | B5 | **4 de 6 = 66,7 %** de los rechazos en la mesa | **FALLA**, pero sobre n = 6 |
| **R5** | QUÉDATE entra a competir en más del 90 % de sus 125 escenas y gana en más de la mitad | B5 | **0 compiten**; las **125 COINCIDEN** | **FALLA**, y por un motivo que es noticia |
| **R6** | el azar como forma se acepta por debajo del 10 % con vida entera | B5 | **46,79 %** | **FALLA**, y por mucho |

**Los contadores podían variar, comprobado.** El de R2 varía entre 28,6 % y
70,9 % según el criterio, y la diferencia entre +1,3 y +24,1 según la puerta. El
de R3 valía **0 %** en mi primera corrida, con el fallo de orden. El de R4 se
reparte entre tres causas distintas y tres filas. El de R5 podía dar cualquier
cosa entre 0 y 125. El de R6 va de 28,6 % a 46,8 % según el criterio.

### R5, que falla por una razón que vale más que la predicción

Las 125 escenas de QUÉDATE son aquellas en que la mejora real llegó **sin que el
cuerpo se moviera**. La predicción daba por hecho que hoy no compiten —y en
P5-2c, en efecto, eran las 125 dormidas— y que con la forma entrarían y ganarían.

Lo que pasa es otra cosa: **en las 125, el ganador del cuerpo no tenía destino**.
Es decir, **el cuerpo ya se estaba quedando quieto**. La forma «quédate»
coincide con él en el 100 % de los casos.

Eso corrige la lectura que di en P5-2c. Allí escribí que «el canal no puede
transmitir *quédate donde estás*, y en el 13,77 % de las escenas con futuro
mejor el consejo correcto es inexpresable». Sigue siendo cierto que no se puede
decir. **Pero no hace falta decirlo: el cuerpo ya lo estaba haciendo solo.**

### R6, que es el aviso serio

Una curva **al azar** —una casilla del mapa a la misma distancia, y luego
esperar— **le gana a seguir solo el 46,79 % de las veces**. Eso no puede ser un
mérito del azar: es que **seguir solo es un rival flojo**. La razón está en B0:
el cuerpo casi nunca tiene un plan, así que «seguir solo» es casi siempre
«quedarse quieto», y casi cualquier movimiento proyectado baja la `d` frente a
quedarse.

**La regla, tal como está, mide sobre todo «moverse contra no moverse».** Que
O-después saque 24 puntos al azar dice que además **hay señal de calidad**; que
el azar saque 46,79 % dice que **la mayor parte de lo que la regla premia no es
calidad**.

---

## Lo que esto deja dicho

1. **R2 se cumple: la puerta ancha ve el después.** De 1,30 puntos con el cero
   dentro a **24,08 con el cero muy fuera**, sobre las mismas escenas. El cambio
   no está en el consejo, está en cómo se juzga.
2. **Ensanchar la puerta no rompe lo que funcionaba.** O-ahora sigue al 100 % en
   los tres criterios.
3. **Quien decide es el área, no la vida mínima.** Mover el umbral de 10 a 20
   cambia 8 formas de 908.
4. **La forma pierde en el primer punto de control**, tres de cada cuatro veces.
   Lo que la tumba no es el final del plan: es el primer paso.
5. **El azar acepta demasiado.** Con el 46,79 % de R6, la regla necesita un
   control más duro antes de encenderla en ninguna decisión: comparar contra el
   **mejor** candidato del cuerpo proyectado, no contra «su paso y luego
   esperar».
6. **Parte de los rechazos por área son empates exactos**, no derrotas. La regla
   «> 0» los cuenta como fallo.

**PARO AQUÍ.** La forma no se ha encendido dentro de ninguna decisión.

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`. Ficheros:
`forma.py`, `banco_forma.py`, `fig_P53B.py`, `P53B_resumen.json`,
`P53B_resumen_v1.json` (la corrida con el fallo de orden, guardada),
`P53B_progreso.log`, `P53B_corrida.log`, `figB/B6_formas.png`.
