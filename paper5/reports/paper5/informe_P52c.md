# P5-2c — El control justo, y lo que se lleva por delante

Coste cero. Nada a la plataforma. Mismos 40 diarios, misma semilla **20260919**,
mismas **2.230 escenas**. Progreso por diario en `P52c_progreso.log`.

**El titular, y corrige lo que escribí ayer.** Con un control de azar **justo**
—una casilla del mapa a la misma distancia, no un destino que el cuerpo ya tenía
en la mano— y con el criterio que más se parece al campo, la diferencia entre un
futuro demostrablemente mejor y una casilla cualquiera es de **1,30 puntos, con
un intervalo de −1,27 a +3,87 que incluye el cero**. En P5-2b concluí que «la
puerta sí distingue, y por poco». Con el control justo, **no se puede afirmar que
distinga nada**.

---

## M1 · Las cajas en los tres criterios

### Estricto (solo el tic t)

| llave | n | aceptada | coincide | rechazada | vetada | intraducible | dormida | **compiten** | **aceptada** | IC95 |
|---|---|---|---|---|---|---|---|---|---|---|
| O-ahora | 2.230 | 0 | 2.203 | 0 | 0 | 27 | 0 | 2.203 | 0,00 % | 0,00 – 0,17 |
| **O-después** | 908 | 4 | 0 | 49 | 730 | 0 | 125 | **53** | **7,55 %** | 2,97 – 17,86 |
| **azar emparejado** | 908 | 1 | 0 | 52 | 730 | 0 | 125 | **53** | **1,89 %** | 0,33 – 9,94 |

### Ventana (el primer tic con las piernas listas)

| llave | n | aceptada | coincide | rechazada | caducada | **compiten** | **aceptada** | IC95 |
|---|---|---|---|---|---|---|---|---|
| O-ahora | 2.230 | 0 | 2.194 | 0 | 36 | 2.194 | 0,00 % | – |
| **O-después** | 908 | 40 | 0 | 743 | 125 | **783** | **5,11 %** | 3,77 – 6,88 |
| **azar emparejado** | 908 | 24 | 0 | 759 | 125 | **783** | **3,07 %** | 2,07 – 4,52 |

### Vida entera (cada tic con las piernas listas, durante los 100)

| llave | n | aceptada | coincide | rechazada | caducada | **compiten** | **aceptada** | IC95 |
|---|---|---|---|---|---|---|---|---|
| O-ahora | 2.230 | 13 | 2.182 | 0 | 35 | 2.195 | 0,59 % | 0,35 – 1,01 |
| **O-después** | 908 | **72** | 0 | 773 | 63 | **845** | **8,52 %** | **6,82 – 10,60** |
| **azar emparejado** | 908 | **61** | 0 | 784 | 63 | **845** | **7,22 %** | **5,66 – 9,16** |

**La cifra que importa está en la última tabla y es que las dos filas se tocan.**
Con el criterio del campo, un futuro que el propio diario certifica como mejor
gana el tic **8,52** veces de cada cien; una casilla del mapa sorteada al azar a
la misma distancia gana **7,22**.

---

## La diferencia, en los tres criterios

| criterio | O-después | azar emparejado | diferencia | IC95 | ¿excluye el cero? |
|---|---|---|---|---|---|
| estricto | 7,55 % (n = 53) | 1,89 % (n = 53) | +5,66 pts | **−2,34 a +13,66** | no |
| ventana | 5,11 % (n = 783) | 3,07 % (n = 783) | +2,04 pts | **+0,08 a +4,00** | por los pelos |
| **vida entera** | **8,52 %** (n = 845) | **7,22 %** (n = 845) | **+1,30 pts** | **−1,27 a +3,87** | **no** |

**Cuanto más se parece el banco al campo, más se parecen las dos llaves.** Con el
criterio estricto la diferencia parecía grande y no era significativa por falta
de datos; con la ventana quedaba justo al borde; con la vida entera hay
denominadores de 845 en los dos brazos y **la diferencia se desvanece**.

## (1) El azar viejo contra el emparejado

| criterio | azar viejo (de los candidatos del cuerpo) | azar emparejado (del mapa, misma distancia) |
|---|---|---|
| estricto | 1,82 % (10 de 549) | **1,89 %** (1 de 53) |
| ventana | 1,82 % (10 de 549) | **3,07 %** (24 de 783) |

**El control viejo era peor de dos maneras.** Sorteaba entre los destinos que el
cuerpo ya tenía en su lista, así que (a) tenía gemelo garantizado y (b) eran
destinos que el cuerpo ya había puntuado y descartado, lo que le daba una ventaja
artificial a O-después. El emparejado sortea casillas **pisables del mapa** a la
misma distancia Chebyshev, con semilla fija, y sale **más fuerte**: 3,07 % contra
1,82 % con ventana.

## (4) Los gemelos

| criterio | llave | con gemelo | |
|---|---|---|---|
| estricto | O-después | 10 de 908 | **1,10 %** |
| estricto | azar emparejado | 4 de 908 | **0,44 %** |
| ventana | O-después | 156 de 908 | 17,18 % |
| ventana | azar emparejado | 52 de 908 | 5,73 % |

**El emparejado ya no tiene gemelo garantizado**, que era el defecto que rompía
el control en P5-2b. Sí lo tiene alguna vez, y la cifra queda dicha.

La regla del empate se aplica **solo a O-ahora**, como pedías. Para O-después y
el azar emparejado se registra el gemelo pero **no se les cambia la caja**.

## M2 · O-ahora, con su regla

| | |
|---|---|
| escenas | 2.230 |
| fallos (todos intraducibles) | **27** |
| **del traductor** | **27** |
| **de la puerta** | **0** |
| aceptada + coincide | **100,00 %** en los tres criterios |

**Con la regla del gemelo, O-ahora llega al 100,00 % de las escenas competidas,
en los tres criterios.** Los 90 rechazos por empate exacto que M2 identificó en
el banco anterior eran, confirmado, el mismo destino con otro nombre. Lo único
que queda fuera son 27 textos que no nombran nada que el mundo ofrezca ese tic.

**La puerta no rechaza ni una vez** un consejo que es lo que el cuerpo iba a
hacer. Eso se sostiene en los tres criterios.

## M3 · Qué fila tumba

| criterio | llave | rechazos | la que más tumba | segunda | tercera |
|---|---|---|---|---|---|
| estricto | O-después | 49 | **exposición 61,22 %** | carencia 12,24 % | — |
| estricto | azar emparejado | 52 | exposición 57,69 % | alcance 15,38 % | carencia 13,46 % |
| ventana | O-después | 743 | **exposición 40,51 %** | carencia 14,94 % | alcance 9,02 % |
| ventana | azar emparejado | 759 | exposición 48,09 % | carencia 25,03 % | alcance 6,19 % |
| **vida** | **O-después** | **773** | **exposición 41,91 %** | carencia 14,75 % | — |
| **vida** | azar emparejado | 784 | exposición 48,21 % | carencia 24,36 % | llamada 5,48 % |

**La exposición manda en los seis casos**, y manda igual para el consejo bueno y
para el azar. Es otra señal de que la puerta no está mirando la calidad del
futuro: está mirando si el camino la deja a la vista.

## M4 y (3) · Q5, por distancia y con vida entera

### O-después

| distancia | escenas | estricto | ventana | **vida entera** | IC95 (vida) |
|---|---|---|---|---|---|
| **1 paso** | 510 | 0,00 % | 0,98 % | **2,35 %** | 1,35 – 4,07 |
| 2 pasos | 77 | 7,14 % | 7,79 % | **12,99 %** | 7,21 – 22,28 |
| **3 o más** | 196 | 20,00 % | 14,80 % | **22,96 %** | 17,62 – 29,33 |

### Azar emparejado, la misma tabla

| distancia | escenas | estricto | ventana | **vida entera** |
|---|---|---|---|---|
| 1 paso | 510 | 0,00 % | 1,57 % | **3,73 %** |
| 2 pasos | 77 | 0,00 % | 1,30 % | **10,39 %** |
| 3 o más | 196 | 6,67 % | 7,65 % | **14,80 %** |

**Q5 vuelve a fallar, y con el mejor criterio posible.** A un paso da **2,35 %**,
no el 40 % sellado, y la tasa **sube con la distancia** hasta el 22,96 % a tres o
más pasos. A un paso, además, **el azar gana más que el consejo bueno** (3,73 %
contra 2,35 %): cuando el destino está pegado, el cuerpo ya tiene ese candidato y
la propuesta solo puede empatar y perder.

### La fila que tumba, por distancia (O-después, vida entera)

| distancia | la que más tumba | segunda |
|---|---|---|
| 1 paso | exposición 40,96 % | carencia 12,05 % |
| 2 pasos | exposición 44,78 % | carencia 22,39 % |
| 3 o más | exposición 41,06 % | carencia 21,19 % |

### La mejora sin moverse

| | |
|---|---|
| escenas de O-después en que el cuerpo **no se movió de su casilla** en 100 tics | **125 de 908 = 13,77 %** |
| de esas 125, cuántas están en los grupos de 1, 2 y 3+ pasos | **ninguna** |

**Y esto tiene una consecuencia que conviene subrayar.** Esas 125 escenas son
exactamente las que el banco marca como **dormidas** en el criterio estricto y
**caducadas** en los otros dos. En ellas el consejo bueno es «quédate donde
estás»: la mejora real llegó sin que el cuerpo se moviera. El traductor las
convierte en «ve a la casilla (x,y)» con (x,y) = la casilla actual, y `CX.ata`
devuelve `None` porque un destino igual a la posición no se puede atar
(`cortex_t5.py:658-660`).

**O sea: el canal no puede transmitir «quédate donde estás» como destino.** En
casi una de cada siete escenas con futuro mejor, el consejo correcto es
inexpresable por construcción. Eso no es que la puerta lo rechace: es que no
llega.

## Vida entera · cuántas veces gana y cuándo

| llave | cuántas ganan | veces que gana (mediana / máx) | edad de la 1ª victoria (mediana / máx) | tics en que compite (mediana) |
|---|---|---|---|---|
| O-ahora | 13 | 3 / 8 | 33 / 99 | 9 |
| **O-después** | **72** | 2 / 9 | **8** / 93 | 9 |
| azar emparejado | 61 | 2 / 21 | **19** / 98 | 9 |

La propuesta compite, típicamente, en **nueve** de sus cien instantes de vida:
el resto lo pasa esperando a que las piernas se enfríen. Cuando O-después gana,
gana **pronto** —mediana de 8 instantes desde que nace— mientras que el azar
tarda 19. Es la única señal, débil, de que la calidad del consejo cuenta para
algo.

## M5 · La mejora real

| n | mediana | media | sin moverse |
|---|---|---|---|
| 908 | **−0,11389** | −0,24013 | 125 = 13,77 % |

Sin cambios: no depende del criterio.

---

## Lo que esto obliga a corregir

1. **La conclusión de P5-2b era optimista por culpa del control.** Con el azar
   viejo salía «+3,29 puntos, el cero excluido». Con el azar justo y el criterio
   del campo sale **+1,30 puntos con el cero dentro**. La respuesta a la pregunta
   central del encargo P5-2 es: **no se puede afirmar que la puerta distinga un
   futuro demostrablemente mejor de una casilla cualquiera a la misma
   distancia.**
2. **La puerta funciona perfectamente para lo que ya sabe.** O-ahora llega al
   **100,00 %** en los tres criterios y la puerta no lo rechaza nunca. El
   instrumento no está roto: está ciego a la novedad, no al reconocimiento.
3. **Lo que decide no es la calidad del futuro, es la exposición.** Cuatro de
   cada diez rechazos los firma `S-8-EXPOSICION`, y los firma **igual** para el
   consejo bueno y para el azar.
4. **Hay un consejo que el canal no puede decir.** «Quédate donde estás» es el
   consejo correcto en el 13,77 % de las escenas con futuro mejor, y el traductor
   no tiene forma de expresarlo: un destino igual a la posición no se ata.
5. **Q5 falla en los tres criterios y falla al revés.** Cuanto más cerca está el
   destino, menos gana la propuesta, porque más probable es que el cuerpo ya lo
   tuviera. A un paso el azar incluso gana más.

**Lo que haría falta para ir más allá**, y no está hecho: dar al canal una forma
de decir «quieto», y separar en la tabla lo que mide la exposición del camino de
lo que mide la exposición del destino. Las dos son propuestas, no decisiones.

## Custodia

```
$ md5 -q motor/model.py paintball/alma/decisor_zs.py \
        paintball/alma/appraisal_zs_v42_exp.py
1e511978c251130e95169ebf8443efa1
8fa03547e3228ef9df4aa94c444f9252
98c13d60167c80cc8334c965be75c640
```

Ficheros: `cantera/paper5/banco_llaves3.py`, `tablas_P52c.py`,
`P52c_resumen.json`, `P52c_detalle.json`, `P52c_progreso.log`,
`P52c_corrida.log`. Ni el decisor ni la tabla se han tocado.
