# P5-2b — Reanálisis: la ventana, los empates y las piernas

Coste cero. Nada se ha lanzado a la plataforma.

**El titular.** Las tres preguntas del añadido tienen la misma respuesta de
fondo: **lo que el banco estricto medía como «la puerta rechaza» era casi todo
«el cuerpo tenía las piernas frías»**. El cuerpo pasa **tres de cada cuatro
instantes enfriando**, y nueve de cada diez veces que se queda quieto es porque
no puede moverse, no porque lo elija. Con la ventana del campo, los 730 vetos de
O-después desaparecen y la llave pasa de 53 escenas competidas a **783**.

---

## Cómo se ha hecho, y una validación que sale gratis

El banco nuevo es `cantera/paper5/banco_llaves2.py`. Dos cambios, declarados:

1. **No rehace la comprobación de reproducción del arnés.** Quedó cerrada en
   **112.865 / 112.865 = 100,00 %**. Aquí solo se decide en los tics que hacen
   falta: el de la escena y el de su ventana. Eso baja la corrida de **4 h 10 min
   a unos 20 minutos**.
2. **Carga los diarios de uno en uno.** `banco_llaves.py` hacía
   `list(diarios_planos(...))`, que mantiene los ochenta en memoria a la vez; la
   primera versión de hoy llegó a **3.172 MB** en cuarenta segundos. Ahora corre
   en **191 MB**. Ese era también el motivo de que el entorno matara los vigías
   toda la tarde.

La selección es la misma: los mismos índices, la misma semilla **20260919**, los
mismos **40 diarios** y las mismas **2.230 escenas**.

**Y la validación gratis:** la columna estricta de este banco reproduce **cifra a
cifra** la del banco anterior —3 / 2.110 / 90 / 27, 4 / 49 / 730 / 125, 10 / 539—
aunque el camino de cálculo es distinto. El abaratamiento no cambió nada.

Salida sin buffer y una línea por diario en `cantera/paper5/P52b_progreso.log`,
como pedías.

---

## (3) Las piernas: el cuerpo está quieto porque enfría

Sobre los **112.865** tics vivos de los 40 diarios:

| medida | veces | fracción |
|---|---|---|
| tics con `move_ready_in > 0` (enfriando) | **85.425** | **75,69 %** |
| decisiones `noop` | 93.445 | 82,79 % de los tics vivos |
| **`noop` con las piernas frías** | **84.458** | **90,38 % de los noop** |
| `noop` con las piernas libres | 8.987 | 9,62 % de los noop |

**Nueve de cada diez veces que el cuerpo se queda quieto, no podía moverse.** El
«noop por encima del 70 %» que el paper cuatro y la fase C de P5-1 leían como
quietud elegida es, en su inmensa mayoría, quietud forzada. Solo **8.987 de
112.865 instantes**, el **7,96 %**, son quietud de verdad elegida con las piernas
libres.

Esto cambia la lectura de la calma de P5-1 C2 y hay que decirlo: cuando allí
escribí «en calma el cuerpo sigue quieto, noop por encima del 70 %», la cifra era
correcta pero la interpretación se queda corta.

## La ventana, medida

| | |
|---|---|
| escenas | 2.230 |
| **sin ventana** (piernas frías los 100 tics enteros) | **5** |
| espera media hasta la ventana | **4,12 tics** |

Solo cinco escenas de 2.230 no encuentran hueco en cien instantes, y la espera
típica es de cuatro tics, o sea **una sexta parte de segundo**. La ventana no es
una concesión generosa: es lo que el campo hace de todos modos, porque la
propuesta vive cien tics y se reintenta cada uno.

---

## M1 · Las cajas, en las dos columnas

### Criterio estricto (solo el tic t) — lo ya reportado

| llave | n | aceptada | coincide | rechazada | vetada | intraducible | dormida | **compiten** | **aceptada** | IC95 |
|---|---|---|---|---|---|---|---|---|---|---|
| O-ahora | 2.230 | 3 | 2.110 | 90 | 0 | 27 | 0 | 2.203 | 0,14 % | 0,05 – 0,40 |
| O-después | 908 | 4 | 0 | 49 | **730** | 0 | 125 | **53** | **7,55 %** | 2,97 – 17,86 |
| O-azar | 549 | 10 | 0 | 539 | 0 | 0 | 0 | 549 | 1,82 % | 0,99 – 3,32 |

### Criterio de ventana

| llave | n | aceptada | coincide | rechazada | caducada | **compiten** | **aceptada** | IC95 |
|---|---|---|---|---|---|---|---|---|
| O-ahora | 2.230 | 3 | 2.101 | 90 | 36 | 2.194 | 0,14 % | 0,05 – 0,40 |
| **O-después** | 908 | **40** | 0 | 743 | 125 | **783** | **5,11 %** | **3,77 – 6,88** |
| O-azar | 549 | 10 | 0 | 539 | 0 | 549 | 1,82 % | 0,99 – 3,32 |

**Lo que cambia.** Los **730 vetos de O-después se convierten en competencia
real**: 40 aceptadas y 743 rechazos. La tasa baja del 7,55 % al **5,11 %**, pero
sobre un denominador **quince veces mayor** y con un intervalo quince veces más
estrecho. La cifra del banco estricto no era falsa; era ruido.

**O-azar no cambia**, y tiene explicación: el azar solo se construye cuando hay
candidatos de movimiento vivos, lo que ya exige las piernas libres, así que su
ventana es siempre el propio tic t.

**O-ahora tampoco se mueve**: sus 27 intraducibles pasan a caducadas y se le
suman 9 más que dejan de poder atarse en el tic de la ventana.

---

## M2 · Traductor contra puerta, con y sin la regla del gemelo

### Sin la regla (lo reportado)

| | estricto |
|---|---|
| la propuesta vuelve al candidato que el cuerpo eligió | **2.108 de 2.230 = 94,53 %** |
| fallos (rechazada + intraducible) | 117 |
| **del traductor** | **117 = 100,00 %** |
| **de la puerta** | **0 = 0,00 %** |
| rechazos cuya propuesta tiene un **gemelo** (mismo destino, otro nombre) | **90 de 90 = 100,00 %** |

**La puerta sigue sin rechazar ni una vez** un consejo que es lo que el cuerpo
iba a hacer. Y los 90 rechazos son **todos** gemelos: el mismo destino con otro
nombre.

**Aviso sobre la columna de ventana para M2.** Ahí el texto describe lo que el
cuerpo eligió en **t**, pero se juzga en **w**, donde el cuerpo ya puede querer
otra cosa. Por eso el «vuelve al candidato original» cae al 21,66 %, y **eso no
es un fallo del traductor**: es que la pregunta de M2 solo tiene sentido en el
mismo tic. La medida buena de M2 es la columna estricta.

### Con la regla del gemelo

Si un candidato traducido cuyo destino es idéntico al de un candidato propio
cuenta como `coincide`:

| criterio | cajas que cambian | total |
|---|---|---|
| estricto | O-ahora 90 · O-después 10 · O-azar 539 | **639** |
| ventana | O-ahora 90 · O-después 155 · O-azar 539 | **784** |

| llave | criterio | aceptada+coincide sin la regla | con la regla |
|---|---|---|---|
| O-ahora | estricto | 95,91 % | **100,00 %** |
| O-después | estricto | 7,55 % | **26,42 %** |
| O-azar | estricto | 1,82 % | **100,00 %** |
| O-ahora | ventana | 95,90 % | **100,00 %** |
| O-después | ventana | 5,11 % | **24,90 %** |
| O-azar | ventana | 1,82 % | **100,00 %** |

**Y aquí hay que parar, porque la regla rompe el control.** O-azar salta al
**100,00 %**, y no por mérito: el azar se sortea **entre los destinos de los
propios candidatos de movimiento del cuerpo**, así que **todo destino al azar
tiene gemelo por construcción**. Con la regla tal como está escrita, el control
de ruido deja de ser un control.

La lectura que sí se sostiene: la regla es **correcta para O-ahora**, donde
arregla exactamente la pérdida de contabilidad que M2 identificó y lleva la
llave al 100,00 %. Para las llaves que proponen un destino nuevo, «mismo
destino» no puede significar «coincide», porque entonces cualquier propuesta
alcanzable coincide con algo.

---

## M3 · Qué fila tumba a O-después

| criterio | rechazos | la fila que más tumba | | |
|---|---|---|---|---|
| estricto | 49 | **S-8-EXPOSICION 61,22 %** | R-CARENCIA 12,24 % | F-4-ALCANCE 10,20 % |
| **ventana** | **743** | **S-8-EXPOSICION 40,51 %** | R-CARENCIA 14,94 % | F-4-ALCANCE 9,02 % |

Distancia del destino en los rechazos: mediana **2** en estricto, **1** en
ventana, máximo 9.

**El orden aguanta con quince veces más datos.** La exposición sigue firmando la
plaza más grande con diferencia, la carencia sigue segunda y el alcance sigue
tercero. Con la ventana la exposición baja del 61 % al 41 %, y sube el grupo
«sin detalle» al 19,38 %, que son rechazos donde el detalle por filas no venía en
la decisión.

## M4 · O-después por distancia

| distancia | criterio | escenas | vetadas | compiten | aceptadas | tasa | IC95 |
|---|---|---|---|---|---|---|---|
| **1 paso** | estricto | 510 | 486 | 24 | 0 | **0,00 %** | 0,00 – 13,80 |
| **1 paso** | **ventana** | 510 | **0** | **510** | 5 | **0,98 %** | 0,42 – 2,27 |
| 2 pasos | estricto | 77 | 63 | 14 | 1 | 7,14 % | 1,27 – 31,47 |
| 2 pasos | **ventana** | 77 | 0 | 77 | 6 | **7,79 %** | 3,62 – 15,98 |
| 3 pasos | estricto | 70 | 67 | 3 | 1 | 33,33 % | 6,15 – 79,23 |
| 3 pasos | **ventana** | 70 | 0 | 70 | 12 | **17,14 %** | 10,09 – 27,62 |

**La predicción Q5 decía que a un paso subiría del 40 %. Con ventana y 510
escenas competidas, a un paso da 0,98 %, y la tasa SUBE con la distancia:** 0,98,
7,79 y 17,14 por ciento a uno, dos y tres pasos, con intervalos que no se solapan
entre el primero y el tercero. Es lo contrario de lo que se selló. Tiene sentido
a posteriori: un destino a un paso es casi siempre un candidato que el cuerpo ya
tiene, y entonces la propuesta no aporta nada y pierde el empate; un destino a
tres pasos es algo que el cuerpo no había imaginado.

## M5 · La mejora real

Sin cambios respecto al informe anterior, porque no depende del criterio:

| n | mediana | media |
|---|---|---|
| 908 | **−0,11389** | −0,24013 |

---

## (4) O-después contra O-azar, y cuántas escenas hacen falta

| criterio | O-después | O-azar | diferencia | IC95 de la diferencia |
|---|---|---|---|---|
| estricto | 7,55 % (n = 53) | 1,82 % (n = 549) | **+5,73 pts** | **−1,47 a +12,92** |
| **ventana** | **5,11 %** (n = 783) | 1,82 % (n = 549) | **+3,29 pts** | **+1,38 a +5,19** |

**Con la ventana, la pregunta central del encargo se puede responder.** El
intervalo ya **no incluye el cero**: O-después es mejor que el azar, de verdad.
Y la diferencia es de **3,3 puntos**, por debajo de los 5 del umbral, con el
intervalo casi entero por debajo de 5.

O sea: **la puerta distingue algo, pero muy poco**. Un futuro demostrablemente
mejor gana el tic 5,1 veces de cada cien; una casilla al azar, 1,8. Las dos están
lejísimos de las 95,9 de cien con que la puerta reconoce lo que el cuerpo ya
quería.

### Cuántas escenas harían falta

Para distinguir **5 puntos** alrededor del 5,11 % medido, con 95 % de confianza y
80 % de potencia:

| | |
|---|---|
| escenas competidas necesarias **por brazo** | **159** |
| las que hay hoy, con ventana | **783** |
| **¿bastan los 40 diarios?** | **sí, sobran: hay 4,9 veces las necesarias** |
| diarios que habrían bastado | **9 de los 80** |

Con el criterio estricto no bastaban ni los 80: 53 escenas competidas de 40
diarios dan unas 106 de los 80, por debajo de las 159. **La ventana, no más
diarios, es lo que hacía falta.**

---

## Cómo queda el cotejo de Q1 a Q5

| | predicción | estricto | ventana | veredicto final |
|---|---|---|---|---|
| **Q1** | O-ahora > 80 % | 95,91 % | 95,90 % | **CUMPLE** (y 100,00 % con la regla del gemelo) |
| **Q2** | O-después < 20 % | 7,55 % | **5,11 %** | **CUMPLE** |
| **Q2** | …en la banda 8,8 – 10,8 % | solapaba | **5,11 %, IC 3,77 – 6,88: NO solapa** | **FALLA**: queda por debajo del consejero del cuatro |
| **Q3** | azar a menos de 5 puntos | +5,73 (falla) | **+3,29, IC +1,38 a +5,19** | **CUMPLE** con ventana |
| **Q4** | tumba la exposición o la carencia, no el alcance | exposición 61,22 % | **exposición 40,51 %**, alcance 9,02 % | **CUMPLE** |
| **Q5** | a un paso, > 40 % | 0,00 % | **0,98 %** | **FALLA**, y al revés: la tasa sube con la distancia |

El cambio de criterio **da la vuelta a Q3** y **vuelve concluyente a Q2**: con
ventana, O-después no está en la banda del consejero, está **por debajo**.

---

## Lo que este reanálisis deja dicho

1. **El veto no era de la puerta: era de las piernas.** Tres de cada cuatro
   instantes el cuerpo está enfriando, y con la ventana del campo los 730 vetos
   desaparecen. Medir una propuesta en un tic suelto mide sobre todo el
   enfriamiento.
2. **La quietud del cuerpo es forzada, no elegida**, en el 90,38 % de los casos.
   Eso obliga a matizar la lectura de la calma de P5-1 C2.
3. **La puerta sí distingue un futuro bueno del azar, y por poco**: 5,11 % contra
   1,82 %, diferencia de 3,3 puntos con el cero excluido. Es una respuesta a la
   pregunta central, y es una respuesta modesta.
4. **La regla del gemelo arregla O-ahora y rompe el control del azar.** Con ella
   O-ahora llega al 100,00 %, que es lo correcto; pero O-azar también, y eso es
   un artefacto de cómo se sortea el azar, no un mérito.
5. **Lo que queda por hacer**, si se quiere cerrar esto: sortear el azar entre
   casillas del mapa a la misma distancia que el destino de O-después, en vez de
   entre los candidatos del propio cuerpo. Así el control deja de tener gemelo
   garantizado y las dos llaves se comparan de verdad.

## Custodia

```
$ md5 -q motor/model.py paintball/alma/decisor_zs.py \
        paintball/alma/appraisal_zs_v42_exp.py
1e511978c251130e95169ebf8443efa1
8fa03547e3228ef9df4aa94c444f9252
98c13d60167c80cc8334c965be75c640

$ md5 cantera/paper5/banco_llaves2.py cantera/paper5/tablas_P52b.py
MD5 (cantera/paper5/banco_llaves2.py) = 73c042178ec3e5d03cdafcffdc26b3ee
MD5 (cantera/paper5/tablas_P52b.py)   = 70e9c1d13ec1057dfff6f10dd6f5bc9c
```

Los dos ficheros intocables siguen con su md5 de origen. La inyección envuelve
`D.candidatos` desde fuera y los interruptores se fijan como atributos de
módulo. Ficheros de salida: `P52b_resumen.json`, `P52b_detalle.json`,
`P52b_progreso.log`, `P52b_corrida.log`.
