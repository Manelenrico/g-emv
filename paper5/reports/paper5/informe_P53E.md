# P5-3E — Piso a todas las filas de los otros, y margen mínimo

En seco, coste cero. Nada a la plataforma. **Ninguna decisión real cambia.**
Mismas 2.230 escenas, semilla **20260919**.

**R6c falla, así que paro y no toco la regla.** Con E1 y margen 0, el azar sigue
aceptándose el **42,11 %** de las veces que llega a la mesa, contra el 20 %
sellado. Sobre las 908 formas construidas baja al **0,88 %**, pero entonces
O-después cae al **4,07 %** y no llega al 40 % que la predicción le pedía. Falla
con los dos denominadores, en cláusulas distintas.

**Y sin embargo los dos cambios hacen lo que tenían que hacer.** El piso general
tumba **el 92,3 %** de las formas de azar en la regla (859 de 908) contra el
88,0 % de D2, y la diferencia entre el consejo bueno y el azar sube a **+41,99
puntos**. Quitar el `deepcopy` baja el coste de 6,53 a **4,22 ms** con la `d`
idéntica al bit.

---

## E1 · El principio, y las dieciséis filas

**Declarado en `forma.py`: la forma no cobra seguridad por lo que no ve.** Como
los otros van **congelados** en la foto proyectada, ninguna fila que dependa de
dónde estén puede **bajar** por el camino; puede subir si el camino se les
acerca.

**Las filas que miran a un asiento ajeno**, con la línea de
`appraisal_zs_v42_exp.py` donde toman valor:

| fila | línea | qué mira |
|---|---|---|
| **F-ANTICIPACION** | :1000 | ves venir el golpe de un rival |
| **F-4-ALCANCE** | :1070 | estás a tiro de alguien |
| **S-8-EXPOSICION** | :1416 | cuántos hostiles pueden verte |
| **S-7-AGRESOR** | :1508 | ese te está pegando |
| MIEDO_APRENDIDO | :1553 | *(apagada en esta configuración)* |
| S-VIDA-AJENA | :1663 | *(apagada en esta configuración)* |
| **S-COMPANIA** | :1035 | quieres al hermano cerca |
| **S-SOLEDAD** | :1096 | llevas rato sin verlo |
| **S-DANO-PAREJA** | :1171 | le están pegando |
| **S-MUERTE-PAREJA** | :1124 | se te muere |
| **S-VINCULO** | :1197 | el golpe puede romper el vínculo |
| **S-HERIDO** | :1302 | está peor que tú |
| **S-PROVISION** | :1362 | tú llevas cura y él no |
| **F-HERMANO-AMENAZA** | :1642 | está a tiro de alguien |
| **F-HERMANO-GOLPE** | :1643 | el golpe que le cae lo notas |
| **R-HERMANO-FALTA** | :1644 | le falta con qué curarse |

**Son dieciséis, no tres.** Diez de ellas miran al **hermano**, que también es un
asiento ajeno y también va congelado en la foto.

**Las cinco que NO llevan piso, y por qué:** `F-DANO` (:875, vida propia que
falta), `F-REENCUENTRO` (:931, memoria del mapa), `R-ACOPIO` (:951-973),
`R-CARENCIA` (:1076) y `R-LLAMADA` (:1088). Miran el propio inventario y el
suelo, **y el suelo sí se proyecta**.

**Método, el mismo de D2 y validado igual:** `A.filas()` sobre la foto
proyectada, piso por fila, y el `State` rehecho repartiendo cada fila en sus
tres ejes con `REPARTO`, que es literalmente
`appraisal_zs_v42_exp.py:1684-1698`.

```
E5 · d IDENTICA al bit sin deepcopy: 275/275 = 100.00 %
E1 · con el piso de todas las filas ajenas la d SUBE en 225/275 tics = 81.8 %
```

Con el piso desactivado da la misma `d` que `opponent_distance(appraise(...))`
**en 275 de 275 tics**; con el piso puesto sube en el 81,8 %, o sea que muerde.

### Lo que el piso le hace al comparador

| | D1 (sin piso) | D1+D2 (piso a exposición) | **E1 (piso a las 16)** |
|---|---|---|---|
| la mejor curva propia **se mueve** | 70,1 % | 66,7 % | **49,9 %** |
| quién es la mejor propia | `noop` 270 | — | **`noop` 453** · `ir_botin` 293 · `ir_centro` 80 |

**Quitar el regalo devuelve a «quedarse quieto» a la competición.** Con el piso,
la mejor curva propia vuelve a ser `noop` la mitad de las veces.

### Y lo que le hace a la regla

| llave | D1: pasan | D1+D2: pasan | **E1: pasan** | E1: rechazo por área |
|---|---|---|---|---|
| O-después | 181 de 908 | 79 | **44 (4,8 %)** | 838 |
| azar emparejado | 148 de 908 | 79 | **19 (2,1 %)** | 859 |

La regla con el piso general **deja pasar una de cada veinte** formas del
consejo bueno y **una de cada cincuenta** del azar.

---

## E2 y E3 · Las columnas, con los cuatro márgenes

Criterio de **vida entera**. Universo: 908 formas por llave, 2.230 para O-ahora.

### Sobre las formas que llegan a la mesa

| puerta | O-después | IC95 | azar emparejado | IC95 | **diferencia** | IC95 |
|---|---|---|---|---|---|---|
| **hoy** (P52c) | 8,52 % (72/845) | — | 7,22 % (61/845) | — | **+1,30** | −1,27 a +3,87 |
| **ancha D1+D2** | 67,90 % (55/81) | 57,1–77,1 | 35,44 % (28/79) | 25,8–46,4 | **+32,46** | +17,81 a +47,11 |
| **E1, margen 0** | **84,09 %** (37/44) | 70,6–92,1 | **42,11 %** (8/19) | 23,1–63,7 | **+41,99** | **+17,29 a +66,68** |
| E1, margen 0,02 | 88,89 % (32/36) | 74,7–95,6 | 33,33 % (2/6) | 9,7–70,0 | **+55,56** | +16,46 a +94,65 |
| E1, margen 0,05 | 90,00 % (27/30) | 74,4–96,5 | 50,00 % (2/4) | 15,0–85,0 | +40,00 | **−10,16 a +90,16** |
| E1, margen 0,10 | 89,29 % (25/28) | 72,8–96,3 | 50,00 % (2/4) | 15,0–85,0 | +39,29 | **−11,04 a +89,61** |

### Sobre las 908 formas construidas

| puerta | O-después | azar emparejado | **diferencia** | IC95 |
|---|---|---|---|---|
| ancha D1+D2 | 6,06 % | 3,08 % | +2,97 | +1,06 a +4,89 |
| **E1, margen 0** | **4,07 %** | **0,88 %** | **+3,19** | **+1,77 a +4,62** |
| E1, margen 0,02 | 3,52 % | 0,22 % | +3,30 | +2,07 a +4,54 |
| E1, margen 0,05 | 2,97 % | 0,22 % | +2,75 | +1,61 a +3,90 |
| E1, margen 0,10 | 2,75 % | 0,22 % | +2,53 | +1,43 a +3,64 |

**El margen funciona, y a partir de 0,02 se queda sin datos.** Con margen 0,02
el azar cae de 8 formas a 2, y con 0,05 a 4 en la mesa: los intervalos se abren
tanto que **el cero vuelve a entrar** en la diferencia. El margen que más separa
es **0,02**, con +55,56 puntos y el cero fuera.

**O-ahora: 2.230 de 2.230 = 100,00 %** de coincide, en los tres criterios y en
los cuatro márgenes. La regla del empate de siempre.

---

## E4 · Contra qué sigue ganando el azar, con E1 y margen 0

De las **19** formas de azar que pasan la regla, **las 19 ganan en su primer
punto de control**. La fila que más le baja respecto a la mejor curva propia, ya
**con el piso aplicado**:

| fila | veces | | ¿lleva piso? |
|---|---|---|---|
| **R-LLAMADA** | **8** | **42,1 %** | **no** (el suelo sí se proyecta) |
| F-4-ALCANCE | 6 | 31,6 % | sí |
| F-REENCUENTRO | 4 | 21,1 % | **no** (memoria del mapa) |
| S-8-EXPOSICION | 1 | 5,3 % | sí |

**Dos causas distintas, y solo una es un agujero.**

1. **`R-LLAMADA`, el 42,1 %, es la causa principal y es legítima… a medias.** La
   llamada del botín baja cuando el camino acerca a un objeto del suelo. El
   suelo **sí** se proyecta, así que no hay regalo. Pero la casilla del azar se
   sortea del mapa, y **a veces cae cerca de un objeto por pura suerte**. No es
   que el azar sepa nada: es que el mapa tiene botín repartido y una casilla
   cualquiera está, de media, más cerca de algo que la casilla en la que estás.
2. **`F-4-ALCANCE` y `S-8-EXPOSICION`, el 36,9 %, ya no son un regalo.** Con el
   piso, esas filas **no pueden bajar** por alejarse. Que salgan como «baja»
   significa lo contrario de antes: **la mejor curva propia se acerca a un rival
   congelado y sube su alcance**, mientras la del azar se queda en el piso. Es
   una diferencia real, no una ganancia inventada.
3. **`F-REENCUENTRO`, el 21,1 %**, es memoria del mapa: sitios donde ya te
   hicieron daño. Tampoco lleva piso, y tampoco es un regalo: el mapa es el
   mismo para las dos curvas.

**Las áreas ganadoras siguen siendo diminutas:** 0,0038, 0,0050, 0,0057, 0,0210
en los cuatro ejemplos guardados. Por eso un margen de 0,02 se lleva por delante
a seis de los ocho.

**Un arreglo de método, declarado.** La primera versión de este diagnóstico leía
las filas **crudas**, sin el piso, y me daba exposición y alcance como causantes
principales. Eso engañaba: con E1 esas filas no pueden bajar. Corregido, la
causa principal pasa a ser `R-LLAMADA`.

---

## E5 · Sin `deepcopy`

El perfil de P5-3D señalaba a `copy.deepcopy` como el **58,7 %** del tiempo. Se
ha sustituido por copia explícita de lo único que el bucle muta —la mochila, la
mano, los efectos y el canal de cura— y por construir la foto proyectada de cero
compartiendo lo que nadie toca.

| | con `deepcopy` (D1+D2) | **sin `deepcopy` (E1)** | |
|---|---|---|---|
| mediana | 6,53 ms | **4,22 ms** | **−35 %** |
| p90 | 9,71 ms | **5,64 ms** | −42 % |
| máximo | 13,75 ms | **8,14 ms** | −41 % |
| candidatos del puñado | 18 | 18 | — |

**Y la `d` sale idéntica al bit: 275 de 275** tics de control, la misma
validación que D2.

Con el primer tramo compitiendo cada tic como candidato normal (0,99 ms) y la
forma evaluada cada 25 tics: **0,99 + 4,22/25 = 1,16 ms por tic**, contra los
40,5 ms del reloj del mundo.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **R6c** | con E1 y margen 0, el azar baja del 20 % | E3 | **42,11 %** en la mesa · 0,88 % sobre las 908 | **FALLA** en la mesa |
| **R6c** | O-después por encima del 40 % | E3 | **84,09 %** en la mesa · 4,07 % sobre las 908 | **FALLA** sobre las 908 |
| **R6c** | diferencia mayor de 20 puntos, cero fuera | E3 | **+41,99**, IC95 +17,29 a +66,68 | **CUMPLE** |
| **R6d** | con margen 0,05 el azar baja del 10 % | E3 | **50,00 %** en la mesa (2 de 4) · 0,22 % sobre las 908 | **FALLA** en la mesa |
| **R6d** | O-después por encima del 30 % | E3 | **90,00 %** en la mesa · 2,97 % sobre las 908 | **FALLA** sobre las 908 |
| **R3''** | O-ahora 100 % en todos los casos | E3 | **2.230 de 2.230** en los tres criterios y los cuatro márgenes | **CUMPLE** |
| **R9** | sin `deepcopy`, por debajo de 3 ms | E5 | **4,22 ms** (de 6,53) | **FALLA** |
| **R9** | con la `d` idéntica al bit | E5 | **275 de 275** | **CUMPLE** |

**Los contadores podían variar, comprobado.** El del azar en la mesa va del
7,22 % con la puerta de hoy al 55,41 % con D1, pasando por 35,44 % con D1+D2 y
42,11 % aquí: cuatro valores muy distintos con las mismas escenas. El de la
diferencia va de +1,30 a +55,56 según la variante. El del coste ha bajado tres
veces seguidas: 52,56 → 6,88 → 6,53 → 4,22 ms. El de O-ahora valió **0 %** en mi
primera corrida de P5-3B, con el fallo de orden.

---

## Por qué paro, y qué dejo dicho

**R6c falla y el encargo mandaba parar.** No he tocado la regla.

**Pero el diagnóstico ha cambiado de sitio, y eso es lo importante.** En P5-3D el
azar ganaba **huyendo**: `F-4-ALCANCE` y `S-7-AGRESOR`, filas de distancia a
rivales congelados, le regalaban seguridad. **Ese agujero está tapado.** Ahora
gana por `R-LLAMADA`, la llamada del botín, que es una fila **sin piso y con
motivo**: el suelo sí se proyecta.

**Lo que queda no es un agujero de la regla: es un problema del control.** La
casilla del azar se sortea del mapa, y el mapa tiene botín repartido; una
casilla cualquiera está, de media, más cerca de algún objeto que la casilla en
la que estás parado. El azar no sabe nada, pero el mapa juega a su favor.

**Tres cosas que se podrían mirar, propuestas y no hechas:**

1. **Un control de azar que no toque botín**: sortear entre casillas a la misma
   distancia **y con la misma llamada del botín** que el destino de O-después.
   Así `R-LLAMADA` dejaría de ser la causa y veríamos qué queda.
2. **Margen 0,02**, que es el que más separa: +55,56 puntos con el cero fuera, y
   deja al azar en 2 formas de 908. Por encima de eso los intervalos se abren y
   el cero vuelve a entrar.
3. **Bajar de 4,22 ms** si hiciera falta: el perfil de P5-3D decía que la tabla
   se lleva el 28,7 %, así que lo que queda por recortar ya es la tabla misma, y
   eso sería tocar código que no se toca.

Son propuestas. **Se habla antes de tocar la regla.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`. Ficheros
nuevos o tocados: `forma.py` (con `PISO_OTROS`, `pisos_de`, `d_con_pisos`,
`copia_estado`, `foto_rapida`, `curva_rapida`, `mejor_propia3`,
`juzga_margen`), `proyeccion.py` (con `proyectar_rapido` y `_proyecta`),
`banco_forma5.py`, `porque_gana_azar_E1.py`, `P53E_resumen.json`,
`P53E_porque_azar2.json`, `P53E_progreso.log`, `P53E_corrida.log`,
`P53E_azar2.log`.
