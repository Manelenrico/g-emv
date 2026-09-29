# P5-3G — Los otros como alcance, y el hermano que cuenta su forma

En seco, coste cero. Nada a la plataforma. **Ninguna decisión real cambia.**
Mismas 2.230 escenas, semilla **20260919**.

**R13 falla, así que paro.** Con G1+G2 la fracción de O-después que pasa la
regla sube del 4,6 % al **13,99 %** de las construidas, no al 30 % sellado.
Reporto G5 y G6, como manda el encargo, y no construyo nada más.

**Pero la vía del medio funciona y triplica lo que la honesta dejaba pasar.** Y
G5 da la explicación de por qué se queda a medias: **el hermano recupera el
45 % de lo suyo y los rivales recuperan menos que cero**.

---

## G1 · El alcance de los rivales

Un rival visto en el tic de ventana ya no se congela: se le pone en la
**casilla alcanzable más cercana a nuestra posición proyectada** —lo peor que
puede hacer, no lo que hará—. Alcanzable = BFS por el mapa estático (`#`, `F` y
`R` cortan) con **11 tics por paso** (`manual_del_mundo.md` §4: `16 − velocidad`),
más el alcance de su arma del catálogo:

| arma | alcance | | arma | alcance |
|---|---|---|---|---|
| espada | 1 | | cuchillos | 5 |
| lanza | 2 | | cerbatana | 6 |
| red | 3 | | arco | 8 |

**Las cinco filas que miran a rivales**, con su línea en
`appraisal_zs_v42_exp.py`, **y sin piso: el alcance lo sustituye.**

| fila | línea | |
|---|---|---|
| F-4-ALCANCE | :1070 | estás a tiro de alguien |
| S-8-EXPOSICION | :1416 | cuántos hostiles pueden verte |
| S-7-AGRESOR | :1508 | ese te está pegando |
| MIEDO_APRENDIDO | :1553 | *(apagada aquí)* |
| S-VIDA-AJENA | :1663 | *(apagada aquí)* |

### Dos límites declarados

1. **«Rivales recordados y no a la vista» no se puede hacer.** La `Memoria` de
   la tabla **no guarda la posición de los rivales**: guarda `pareja_pos`,
   `pareja_banda` y `pareja_muerta`, del hermano, y nada de los demás
   (`appraisal_zs_v42_exp.py:449-470`). Solo entran los rivales **a la vista en
   el tic de ventana**. No me lo invento.
2. **El catálogo no da velocidades distintas.** Trae `range` y `cooldown` **de
   ataque**, no de andar. Así que el paso es de once tics para todos.

**Y funciona como se quería:** con el alcance, la mejor curva propia vuelve a
moverse el **70,8 %** de las veces (era 50,8 % con el piso de E1). Quitar el
piso y poner el alcance devuelve el movimiento a la competición **sin
regalarlo**.

## G2 · El hermano que cuenta

Las diez filas del hermano se evalúan con su estado **real** en ese tic, leído
de **su** diario —el otro asiento de la misma partida—: posición, vida, banda,
y si lo veríamos desde nuestra posición proyectada. Si murió antes, como muerto.

**Diario del hermano disponible en 40 de los 40 diarios.**

---

## G4 · El embudo y las tasas

Vida entera. Universo: **908** formas por llave; 2.230 para O-ahora.

### Margen 0

| variante | llave | construidas | **pasa la regla** | **aceptada** | **en la mesa** | IC95 |
|---|---|---|---|---|---|---|
| **E1** (piso a todo) | O-después | 908 | 42 (4,63 %) | 36 (3,96 %) | **85,71 %** | 72,2–93,3 |
| | azar | 908 | 19 (2,09 %) | 8 (0,88 %) | 42,11 % | 23,1–63,7 |
| | **diferencia** | | | | **+43,61** | +19,01 a +68,20 |
| **G1** (alcance) | O-después | 908 | **124 (13,66 %)** | 95 (10,46 %) | **76,61 %** | 68,4–83,2 |
| | azar | 908 | 96 (10,57 %) | 51 (5,62 %) | 53,12 % | 43,2–62,8 |
| | **diferencia** | | | | **+23,49** | +11,03 a +35,94 |
| **G1+G2** | O-después | 908 | **127 (13,99 %)** | **98 (10,79 %)** | **77,17 %** | 69,1–83,6 |
| | azar | 908 | 97 (10,68 %) | 50 (5,51 %) | **51,55 %** | 41,7–61,2 |
| | **diferencia** | | | | **+25,62** | **+13,28 a +37,96** |

### Margen 0,02

| variante | llave | **pasa la regla** | **aceptada** | **en la mesa** | diferencia |
|---|---|---|---|---|---|
| E1 | O-después | 35 (3,85 %) | 32 (3,52 %) | 91,43 % | **+58,10** |
| | azar | 6 (0,66 %) | 2 (0,22 %) | 33,33 % | |
| G1 | O-después | 106 (11,67 %) | 83 (9,14 %) | 78,30 % | **+20,67** |
| | azar | 59 (6,50 %) | 34 (3,74 %) | 57,63 % | |
| **G1+G2** | O-después | **111 (12,22 %)** | **87 (9,58 %)** | **78,38 %** | **+19,76** (+4,95 a +34,57) |
| | azar | 58 (6,39 %) | 34 (3,74 %) | **58,62 %** | |

**El alcance triplica lo que pasa la regla.** De 42 a 124 formas de O-después.
**El hermano no añade casi nada**: de 124 a 127. Sube la diferencia de +23,49 a
+25,62 puntos, dentro del ruido de los intervalos.

**Y el azar también triplica**, de 19 a 97. Por eso la diferencia **baja**
respecto a E1 (+43,61 → +25,62): el alcance deja pasar más de los dos.

**O-ahora: 2.230 de 2.230 = 100,00 %** en las tres variantes.

---

## G5 · La descomposición recuperada

De la mejora que la forma **G1+G2 proyecta** para los futuros buenos (274 con
mejora proyectada), y comparada con la **real** medida en F2:

| grupo | proyectado | real (F2) | **recupera** |
|---|---|---|---|
| **hermano** | **+38,390** | 85,335 | **45,0 %** |
| **propias** (inventario, suelo, vida, anillo) | +14,591 | 22,378 | **65,2 %** |
| **rivales** | **−3,039** | 104,568 | **−2,9 %** |

*(El real por grupo sale de las filas que F2 guardó en detalle; es una cota
inferior del total, y se declara.)*

**Reparto de lo proyectado:** hermano **72,46 %**, propias 27,54 %, rivales
**−5,74 %**.

**Las filas que más aporta la forma:** `S-HERIDO` 30,05 · `S-DANO-PAREJA` 7,76 ·
`R-CARENCIA` 7,17 · `S-PROVISION` 5,34 · `R-HERMANO-FALTA` 4,42 · `R-ACOPIO`
4,31 · `F-HERMANO-GOLPE` 3,56 · `F-ANTICIPACION` 2,17.

**Esto es lo que el encargo quería saber, y la respuesta es nítida.**

1. **El hermano se recupera: el 45 % de su aporte real.** Escucharle funciona.
   Y cinco de las ocho filas que más aporta la forma son suyas.
2. **Los rivales no se recuperan: el −2,9 %.** El signo es negativo y no es un
   error: **con el alcance, la forma proyecta que las filas de rivales
   EMPEORAN**. Es la consecuencia lógica de poner a cada rival en su peor
   casilla: cuanto más tiempo pasa, más lejos puede haber llegado, así que la
   amenaza proyectada **crece** con el horizonte. La cota es honesta y es
   pesimista.
3. **Las propias se recuperan bien, el 65,2 %**, que era de esperar: el
   inventario, el suelo y el anillo sí se proyectan.

**Ese −2,9 % explica R13.** El 87 % de la mejora real está en los otros
(P5-3F); de esa parte, el trozo de los rivales —que es el mayor— la forma no
solo no lo recupera, lo cuenta al revés. Por eso pasa el 14 % y no el 30 %.

---

## G6 · Contra qué gana el azar, con G1+G2 y margen 0,02

Gana en **58** escenas, y en **54 de 58 (93,1 %)** en su primer punto de
control.

| fila que le baja | veces | |
|---|---|---|
| **S-8-EXPOSICION** | **39** | **67,2 %** |
| F-REENCUENTRO | 12 | 20,7 % |
| S-7-AGRESOR | 4 | 6,9 % |
| R-LLAMADA | 1 | 1,7 % |
| F-HERMANO-AMENAZA | 1 | 1,7 % |
| S-PROVISION | 1 | 1,7 % |

**La exposición vuelve a ser la causa, y ahora con motivo.** Con el alcance, que
la exposición baje ya **no es un regalo**: significa que la casilla del azar
queda fuera de donde los rivales pueden llegar a verla, y la de la mejor curva
propia no. Es una diferencia real.

Lo que pasa es que **sigue siendo fácil de conseguir por casualidad**: una
casilla cualquiera del mapa, a la misma distancia, cae a menudo fuera del cono
de alcance de dos o tres rivales.

`F-REENCUENTRO`, el 20,7 %, es la otra: memoria del mapa, sin alcance ni piso.

---

## G7 · El tiempo

| variante | mediana | p90 | máximo | **cada 25 tics** |
|---|---|---|---|---|
| E1 (piso) | 4,18 ms | 5,59 | 8,34 | **1,16 ms/tic** |
| **G1 (alcance)** | **81,89 ms** | 160,76 | 373,39 | **4,27 ms/tic** |
| G1+G2 | 80,49 ms | 163,22 | 367,24 | **4,21 ms/tic** |

**El alcance multiplica por veinte el coste.** El BFS se cachea por rival y
partida, pero la **búsqueda de la peor casilla escanea la rejilla entera por
rival y por punto de control**, y eso es lo caro. El máximo de 373 ms es nueve
veces el fotograma de 40,5 ms.

Con evaluación al llegar y cada 25 tics quedan **4,21 ms por tic**: cabe en el
reloj, pero **por encima de los 3 ms** que pedía R17.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **R13** | con G1+G2, O-después pasa la regla en más del 30 % de las construidas | G4 | **13,99 %** (de 4,63 %) | **FALLA** |
| **R14** | con margen 0,02, el azar por debajo del 25 % en la mesa | G4 | **58,62 %** | **FALLA** |
| **R14** | …y por debajo del 5 % sobre construidas | G4 | **3,74 %** | **CUMPLE** |
| **R15** | con margen 0,02, O-después gana al azar por más de 25 puntos, cero fuera | G4 | **+19,76**, IC95 +4,95 a +34,57 | **FALLA** el umbral, **cumple** lo del cero |
| **R16** | el hermano recupera más de la mitad de su aporte real | G5 | **45,0 %** | **FALLA por poco** |
| **R16** | los rivales recuperan menos de la mitad | G5 | **−2,9 %** | **CUMPLE** |
| **R3'''** | O-ahora 100 % en todas las variantes | G4 | **2.230 de 2.230** en las tres | **CUMPLE** |
| **R17** | por debajo de 3 ms por tic al llegar y cada 25 | G7 | **4,21 ms** | **FALLA** |

**Los contadores podían variar, comprobado.** El de R13 ha ido 4,63 → 13,66 →
13,99 % en tres variantes con las mismas escenas. El del azar en la mesa va del
33,3 % con E1 al 58,6 % aquí. El de R16 se reparte entre tres grupos y uno sale
**negativo**, que no es un valor que estuviera forzado. El del tiempo ha ido de
4,18 a 81,89 ms.

---

## Por qué paro, y qué queda dicho

**R13 falla y el encargo mandaba parar.** No construyo nada más.

**Lo que G5 deja establecido, y es la respuesta a la vía del medio:**

1. **Escuchar al hermano funciona.** Recupera el **45 %** de su aporte real, y
   cinco de las ocho filas que más aporta la forma son suyas. Casi cumple R16 y
   es el único grupo que se recupera de verdad entre los otros.
2. **Proyectar a los rivales por su alcance NO recupera nada: recupera −2,9 %.**
   Y no por un fallo: porque la cota del peor caso **crece con el horizonte**.
   Cuanto más lejos miras, más lejos puede haber llegado el rival, así que la
   forma proyecta que la amenaza **empeora** siempre. Es honesto y es inútil
   para cobrar mejora.
3. **Ese es el techo real de la vía del medio.** El 87 % de la mejora está en
   los otros; el trozo del hermano se puede recuperar escuchándole, el de los
   rivales **no se puede recuperar con una cota pesimista**. Haría falta una
   **predicción** de los rivales, no una cota, y eso es justo lo que la ceguera
   declarada evitaba.
4. **Y cuesta veinte veces más.** 81,89 ms de mediana contra 4,18.

**Dos cosas que se podrían probar, propuestas y no hechas:**

- **Una cota menos pesimista**: el rival en su peor casilla **ponderada por
  probabilidad de ir hacia nosotros**, o acotada a los pasos que de verdad daría
  en el horizonte útil, no en los 100 tics enteros.
- **Solo el hermano**: G2 sin G1, es decir, escuchar al hermano y dejar a los
  rivales congelados con piso, como en E1. G5 dice que el hermano es lo único
  que se recupera; convendría ver esa combinación sola antes que nada.

Son propuestas. **Se habla antes de seguir.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`. Ficheros:
`alcance_g.py` (renombrado: había un `paintball/alcance.py` que lo tapaba),
`forma.py` con `curva_G` y `mejor_propia_G`, `banco_forma6.py`, `G5G6.py`,
`P53G_G1_resumen.json`, `P53G_G1G2_resumen.json`, `P53G_G5G6.json`, y los
progresos `P53G_G1_progreso.log`, `P53G_G1G2_progreso.log`,
`P53G_G5G6_progreso.log`.
