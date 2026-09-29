# P5-2 — Control del consejo bueno, en banco

Coste cero. Nada se ha lanzado a la plataforma. Todo sobre los diarios de S-2
brazo A, el cuerpo a solas, con el arnés que decide otra vez.

**Es validación del instrumento, no del campo.** Nada de lo que sigue se afirma
de una partida.

**El titular.** La puerta no es el problema, y el traductor tampoco. De cada cien
consejos que ya sabemos buenos, **ochenta no llegan siquiera a la mesa**: el
cuerpo los veta antes de puntuarlos porque tiene las piernas enfriando. De los
que sí llegan, el cuerpo distingue muy poco entre un futuro demostrablemente
mejor y una casilla al azar.

---

## El arnés, antes de inyectar nada

```
REPRODUCCION DEL ARNES: 112,865 de 112,865 = 100.00 %
```

**El 100,00 %** de los tics, con el criterio por `d` a 1e-4 sobre **todos** los
candidatos de cada tic, en los 40 diarios elegidos. La puerta del encargo era el
99 %.

**Costó dos correcciones, y las dos son de método, no del banco.** El primer
intento se quedó en **87,43 %**, y no inyecté nada hasta arreglarlo:

1. **El decisor no valora con la tabla v37.** `policy_cortex.py:97` hace
   `D.A = appraisal_zs_v42_exp`, así que en S-2 los **candidatos** se puntúan con
   v42_exp. El arnés del paper cuatro cableaba v37, que era lo correcto para
   `policy_serie.py` pero no para la política del córtex.
2. **La empatía estaba encendida, y yo la había apagado.** Cada diario escribe
   sus propios interruptores en su registro `arranque`:

   ```
   "cuerpo": "v42_exp EMPATIA_ON H_PREV 0.25 H_GOLPE 1.0 MIEDO_ON False VIDA_AJENA_ON False"
   ```

   Suponerlos apagados desplazaba **todas** las distancias unos 0,13 de forma
   casi uniforme: el conjunto de candidatos coincidía siempre y solo bailaban los
   valores, que es exactamente la firma que salió al diagnosticar. Ahora el arnés
   **los lee del diario**, partida por partida, y no los supone.

Los 40 diarios traen el mismo bloque, así que la serie es homogénea.

**Un fallo mío de operación, dicho.** Lancé la corrida redirigiendo la salida sin
desactivar el buffer de Python, así que estuve tres horas y media sin poder ver
el progreso, y mi estimación de duración (2 h 32) se quedó en 4 h 10 reales. No
afecta a ninguna cifra; afecta a que no supe decirte dónde iba.

## Las escenas

| dato | valor |
|---|---|
| semilla de la selección | **20260919** |
| diarios de S2_A disponibles | 80 |
| diarios elegidos al azar | **40** |
| tics vivos recorridos | 112.865 |
| cadencia | múltiplos de 50 desde el tic 300, fuera del pedestal |
| **escenas** | **2.230** |

Y lo que no llegó a escena, por su motivo:

| se salta porque | veces |
|---|---|
| en `t+100` el cuerpo no estaba mejor (o no había `d`) | 1.242 |
| en `t+100` el cuerpo ya estaba muerto | 80 |
| no había ninguna casilla alcanzable para el azar | 1.681 |
| el texto no tenía forma | **0** |

De ahí salen **908 escenas** para O-después y **549** para O-azar.

---

## M1 · Las cajas y la tasa de aceptación

| llave | n | aceptada | coincide | rechazada | vetada | intraducible | dormida | **compiten** | **aceptada / compiten** | **aceptada+coincide / compiten** |
|---|---|---|---|---|---|---|---|---|---|---|
| **O-ahora** | 2.230 | 3 | **2.110** | 90 | 0 | 27 | 0 | **2.203** | 0,14 % | **95,91 %** |
| **O-después** | 908 | 4 | 0 | 49 | **730** | 0 | 125 | **53** | **7,55 %** | 7,55 % |
| **O-azar** | 549 | 10 | 0 | 539 | 0 | 0 | 0 | **549** | **1,82 %** | 1,82 % |

**«Compiten» = las que llegan a puntuarse**: aceptada, coincide o rechazada. Se
excluyen las vetadas, las dormidas y las intraducibles, que es el mismo corte que
usaba el paper cuatro para «las que compiten sin esperar».

**Dos denominadores, y por qué.** O-ahora propone lo que el cuerpo ya eligió, así
que **nunca puede ganarle**: la regla de que los empates son del cuerpo la manda
siempre a «coincide». Para esa llave, «acertar» es acabar siendo lo que el cuerpo
hace, que es la columna de aceptada+coincide. Para O-después y O-azar, que
proponen un destino que el cuerpo no había elegido, «acertar» es ganar el tic, o
sea la columna de aceptada sola. Así se cotejan las predicciones.

**La cifra que manda la tiene O-después, y no es ninguna de las dos anteriores:**

| de las 908 escenas de O-después | | |
|---|---|---|
| **vetadas** antes de puntuarse | **730** | **80,40 %** |
| dormidas (no hubo dónde atarlas ese tic) | 125 | 13,77 % |
| **llegan a competir** | **53** | **5,84 %** |

Ocho de cada diez consejos buenos mueren en el veto. El veto es
`decisor_zs.py:97-98`: cualquier receta de tipo `ir`, `move` o `paso` queda
vetada mientras `move_ready_in > 0`, o sea mientras las piernas enfrían. En el
tic suelto en que la foto se toma, eso es casi siempre.

**Y por eso todas las enes de O-después son pequeñas.** 53 escenas competidas.
Doy los intervalos en el cotejo y no escondo la incertidumbre.

## M2 · O-ahora: el traductor contra la puerta

| | veces | |
|---|---|---|
| escenas | 2.230 | |
| la propuesta **vuelve** al candidato que el cuerpo eligió | **2.108** | **94,53 %** |
| fallos (rechazada + intraducible) | **117** | 5,25 % |
| · **del traductor** (no vuelve al candidato original) | **117** | **100,00 %** |
| · · intraducibles del todo | 27 | |
| · · vuelve como casilla y empata exacto | 90 | |
| · **de la puerta** (vuelve y pierde) | **0** | **0,00 %** |

**La separación sale limpia y sale entera del lado del traductor.** Cuando el
consejo es literalmente lo que el cuerpo iba a hacer, **la puerta no lo rechaza
ni una vez**. Los 117 fallos son todos de traducción, y de dos tipos:

- **27 intraducibles**: el texto no nombra nada que el mundo ofrezca ese tic.
- **90 empates exactos**: el traductor convierte, por ejemplo, `ir_objeto` en
  `_CX_ir_32_14`, que es **el mismo destino con otro nombre**. Puntúa
  idénticamente —`d_prop` y `d_gana` coinciden hasta el quinto decimal— y la
  regla de que los empates son del cuerpo la tumba. No es que el cuerpo prefiera
  otra cosa: es que ya no reconoce que le están proponiendo lo suyo.

La forma del texto en las 2.230 escenas: «espera» 1.833, frase del relator 277,
casilla 93, «coge» 27.

## M3 · O-después: qué fila tumba, y a qué distancia

De los 49 rechazos, la fila en la que la propuesta está **por encima** del
ganador:

| fila | veces | |
|---|---|---|
| **S-8-EXPOSICION** | **30** | **61,22 %** |
| R-CARENCIA | 6 | 12,24 % |
| F-4-ALCANCE | 5 | 10,20 % |
| R-LLAMADA | 2 | 4,08 % |
| F-REENCUENTRO | 1 | 2,04 % |
| sin detalle | 5 | 10,20 % |

**Seis de cada diez rechazos los firma la exposición**: ir a donde el cuerpo
estuvo cien instantes después implicaba, en la foto de ahora, dejarse ver por
más gente.

Distancia del destino, en casillas:

| | mediana | p90 | máx |
|---|---|---|---|
| todas las escenas de O-después | **1** | 4 | 9 |
| solo los rechazos | **2** | — | 7 |

## M4 · Con el destino a un paso

| distancia | escenas | vetadas | compiten | aceptadas | tasa |
|---|---|---|---|---|---|
| **1 paso** | 510 | **486** | 24 | **0** | **0,00 %** (IC95 0 – 13,8) |
| 2 pasos | 77 | — | 14 | 1 | 7,14 % |
| 3 pasos | 70 | — | 3 | 1 | 33,33 % |

**A un paso no sube: se hunde.** Y el motivo es el mismo veto: de las 510
escenas con el destino pegado, **486 se vetan**, porque un destino adyacente
sigue pidiendo una receta de movimiento y las piernas siguen frías. De las 24
que llegan a puntuarse, **ninguna gana**.

## M5 · Cuánto mejor estaba de verdad

La diferencia `d(t+100) − d(t)` en las 908 escenas de O-después, que por
construcción es siempre negativa:

| n | mediana | media | p10 | p90 |
|---|---|---|---|---|
| 908 | **−0,11389** | −0,24013 | −0,61568 | −0,00655 |

El consejo era bueno de verdad, pero **poco**: la mediana de la mejora es de una
décima de `d`. La mitad de las escenas mejoran menos que eso, y el p90 está en
siete milésimas. Es una mejora real y comprobada con el saber del propio diario,
pero pequeña frente a la dispersión de los candidatos del cuerpo.

## O-azar, para comparar

| | escenas | aceptadas | tasa |
|---|---|---|---|
| todas | 549 | 10 | **1,82 %** |
| solo las que también tenían O-después | 117 | 2 | 1,71 % |

Distancia del destino al azar: mediana 2, máximo 14.

**Ninguna escena de O-azar se vetó.** Es una asimetría del método que hay que
declarar: el azar solo existe cuando hay candidatos de movimiento vivos, o sea
cuando las piernas **no** están frías; O-después se construye en toda escena con
futuro mejor, frías o no. Por eso el azar tiene 549 escenas competidas y
O-después 53. La comparación pareada de la última fila es la honesta.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **Q1** | O-ahora aceptada > 80 % de las competidas | M1, aceptada+coincide sobre competidas | **95,91 %** (IC95 95,00 – 96,66) | **CUMPLE** |
| **Q2** | O-después aceptada < 20 % | M1, aceptada sobre competidas | **7,55 %** (IC95 2,97 – 17,86) | **CUMPLE** |
| **Q2** | …y en la banda del consejero del cuatro (8,8 – 10,8 %) | el mismo | 7,55 %, IC95 **solapa** la banda | **compatible, no distinguible** |
| **Q3** | O-azar a menos de 5 puntos de O-después | M1, diferencia de tasas | **5,73 puntos** (IC95 −1,47 a +12,92) | **FALLA por 0,73 puntos** |
| **Q4** | la fila que más tumba es la exposición o la carencia, no el alcance | M3 | **exposición 61,22 %**, carencia 12,24 %, alcance 10,20 % | **CUMPLE** |
| **Q5** | a un paso, O-después sube por encima del 40 % | M4 | **0,00 %** de 24 competidas | **FALLA** |

**Los contadores podían variar, comprobado uno a uno.** Q1 tenía 2.203 escenas
competidas y 117 fallos: podía haber caído a cualquier valor, y de hecho en el
arnés mal cableado el reparto de cajas era otro. Q2 y Q3 comparan dos tasas que
en este mismo banco van del 0 % al 33 % según el subconjunto. Q4 reparte entre
seis filas distintas y ninguna estaba forzada. Q5 tenía 510 escenas a un paso.

### Q3, con el matiz que merece

Falla por 0,73 puntos sobre un umbral de 5, y el intervalo de la diferencia va de
**−1,47 a +12,92 puntos**. Con 53 escenas competidas de un lado y 549 del otro,
**esta serie no puede distinguir a O-después del azar**. El veredicto formal es
«falla»; la lectura honesta es «no se puede afirmar que sean distintos, ni que
sean iguales». Para separarlos haría falta un banco que rescate las propuestas
vetadas, no que las cuente como perdidas.

### Q5, que es la que más enseña

Se selló pensando que, si el futuro cabía en la foto, la puerta lo vería. Lo que
pasa es otra cosa: **a un paso la propuesta ni siquiera se puntúa**. El 95,3 % de
esas escenas mueren en el veto de las piernas. La predicción daba por hecho que
llegar cerca era llegar a la mesa, y no lo es.

---

## Lo que este control deja dicho sobre el instrumento

1. **La puerta funciona cuando reconoce lo que le dan.** Con un consejo que es
   literalmente el candidato del cuerpo, la puerta acierta el 95,91 % y **rechaza
   el 0 %**. El paper cuatro no puede seguir diciendo «el cuerpo no aprovecha el
   consejo» sin distinguir de qué consejo habla.
2. **El traductor pierde poco, pero pierde de una forma concreta y arreglable.**
   Sus 117 fallos son 27 textos que no nombran nada y **90 empates exactos** en
   los que la propuesta es el mismo destino con otro nombre. Ese segundo grupo es
   una pérdida de contabilidad, no de criterio: si la atadura reconociera que
   `_CX_ir_32_14` es el `ir_objeto` del cuerpo, esas 90 pasarían a «coincide».
3. **El cuello de botella no es la puerta ni el traductor: es el veto.** Ocho de
   cada diez consejos buenos no llegan a puntuarse porque el cuerpo tiene las
   piernas frías en ese instante. En el campo la propuesta vive cien tics y puede
   reintentarlo; **en este banco se puntúa un solo tic**, como pedía el encargo.
   Esa es la diferencia principal entre este control y la serie S-2, y explica
   por qué las enes salen tan cortas.
4. **Cuando llega a puntuarse, la exposición manda.** Seis de cada diez rechazos
   de un futuro demostrablemente mejor los firma `S-8-EXPOSICION`: el cuerpo
   prefiere no dejarse ver antes que estar mejor dentro de cien instantes.
5. **Lo que el control NO permite afirmar.** Con 53 escenas competidas no se
   puede decir si la puerta distingue un futuro bueno de uno cualquiera. La
   pregunta central del encargo sigue **sin respuesta concluyente**, y el camino
   para responderla es un banco que deje competir a la propuesta durante su vida
   entera, no en un tic suelto.

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Ficheros: `cantera/paper5/banco_llaves.py`, `tablas_P52.py`,
`P52_resumen.json`, `P52_detalle.json`, `P52_corrida.log`. Ni `decisor_zs.py`
ni `appraisal_zs_v42_exp.py` se han tocado: la inyección envuelve `D.candidatos`
desde fuera y los interruptores se fijan como atributos de módulo, igual que
hace `serie_util.pon`.
