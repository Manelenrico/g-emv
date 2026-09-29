# P5-3D — Comparador en ventana, exposición conservadora y perfil

En seco, coste cero. Nada a la plataforma. **Ninguna decisión real cambia.**
Mismas 2.230 escenas, semilla **20260919**.

**R6b falla, así que paro.** Con D1 más D2 el azar sigue aceptándose el
**35,44 %** de las veces que llega a la mesa, contra el 20 % sellado. Reporto por
qué renglón gana y no toco la regla.

**Pero los dos cambios funcionan, y mucho.** El comparador en ventana pasa el
puñado de **1 candidato a 18** y hace que la mejor curva propia **se mueva el
70 %** de las veces. La exposición conservadora recorta la ventaja del azar a la
mitad. Y el coste baja de **52,6 ms a 6,9 ms**.

---

## D1 · El comparador en el tic de ventana

| | en el tic de la escena (P53C) | **en el tic de ventana (D1)** |
|---|---|---|
| candidatos del puñado, mediana | **1** | **18** |
| la mejor curva propia **se mueve** | 3,5 % | **70,1 %** (635 de 906) |
| quién es la mejor propia | `noop` 872 | `noop` 270 · `ir_botin` 206 · `ir_centro` 193 · `ir_pareja` 126 · `ir_objeto` 110 |
| coste por decisión, mediana | 52,56 ms | **6,88 ms** |

**El comparador ahora es un rival de verdad.** En el tic de la escena las
piernas estaban enfriando y `D.candidatos` devolvía solo `noop`; en el tic de
ventana devuelve la lista entera.

**Lo que esto le hace a la regla:** los rechazos por área de O-después suben de
**326 a 701**, y los del azar de **476 a 730**. De 908 formas, solo **181**
pasan la regla (antes 558).

## D2 · La exposición conservadora

En las fotos proyectadas de **todas** las formas —propias, O-después y azar— el
renglón `S-8-EXPOSICION` no puede bajar de lo que valía en el tic de partida.
Moverse no esconde de quien no se sabe dónde estará.

**Cómo se ha hecho sin tocar la tabla.** Se llama a `A.filas()` sobre la foto
proyectada, se aplica el piso a esa fila, y se rehace el `State` repartiendo
cada fila en sus tres ejes con `REPARTO`, que es literalmente
`appraisal_zs_v42_exp.py:1684-1698`. Comprobado: **con el piso desactivado da la
misma `d` que `opponent_distance(appraise(...))` en 275 de 275 tics**, al bit. Y
con un piso de +0,2 la `d` sube en los 275, o sea que el piso muerde.

Efecto sobre la regla: las formas que pasan bajan de **181 a 79** en O-después
y de **148 a 79** en el azar.

---

## D3 · Las cuatro puertas, criterio de vida entera

**Sobre las formas que llegan a la mesa:**

| | O-después | azar emparejado | **diferencia** | IC95 |
|---|---|---|---|---|
| **puerta de hoy** (P52c) | 8,52 % (72/845) | 7,22 % (61/845) | **+1,30** | −1,27 a +3,87 |
| **ancha, P53C** | 70,89 % (397/560) | 46,90 % (189/403) | **+23,99** | +17,84 a +30,15 |
| **ancha, D1** | 67,21 % (123/183) | **55,41 %** (82/148) | **+11,81** | +1,30 a +22,31 |
| **ancha, D1+D2** | 67,90 % (55/81) | **35,44 %** (28/79) | **+32,46** | +17,81 a +47,11 |

**Sobre todas las formas construidas (908 en cada brazo):**

| | O-después | azar emparejado | **diferencia** | IC95 |
|---|---|---|---|---|
| ancha, P53C | 43,72 % | 20,81 % | **+22,91** | +18,74 a +27,08 |
| ancha, D1 | 13,55 % | 9,03 % | **+4,52** | +1,61 a +7,42 |
| **ancha, D1+D2** | **6,06 %** | **3,08 %** | **+2,97** | +1,06 a +4,89 |

**Los dos denominadores cuentan historias distintas y las dos son verdad.** La
regla nueva **rechaza mucho más**: de 908 formas de O-después, con D1+D2 solo
79 llegan a la mesa. De las que llegan, dos tercios ganan. Del total, ganan seis
de cada cien.

**O-ahora sigue al 100,00 %** (2.230 de 2.230) en los tres criterios y en las
tres variantes.

---

## D4 · Por qué sigue ganando el azar

De las **79** formas de azar aceptadas con D1+D2:

| dónde gana | veces |
|---|---|
| **en su primer punto de control** | **78 de 79 = 98,7 %** |
| en el segundo | 1 |

**Y qué renglón le baja respecto a la mejor curva propia, en ese punto:**

| fila | veces | |
|---|---|---|
| **F-4-ALCANCE** | **33** | **42,3 %** |
| S-8-EXPOSICION | 27 | 34,6 % |
| S-7-AGRESOR | 13 | 16,7 % |
| F-REENCUENTRO | 3 | 3,8 % |
| otras | 2 | 2,6 % |

**El azar gana huyendo.** `F-4-ALCANCE` —«estás dentro del alcance de alguien
que puede pegarte»— es la que más le baja, y `S-7-AGRESOR` —«ese te está pegando
y aún no le has respondido»— es la tercera. Las dos miden **distancia a los
rivales**, y los rivales están **congelados donde estaban en `t`**: la forma es
ciega a los otros por construcción (declarado en `forma.py`).

**Ahí está el agujero.** Con los rivales congelados, **alejarse de ellos es
gratis y seguro**, y cualquier casilla lejana baja el alcance. La exposición
conservadora tapó una vía —por eso el azar cae del 55,4 % al 35,4 %— pero dejó
abierta la otra, que es la misma idea con otro nombre.

Los ejemplos lo enseñan con cifras pequeñas y consistentes:

```
tic 1450 · área +0,0050 · baja F-4-ALCANCE −0,0062
tic 2300 · área +0,0257 · baja S-8-EXPOSICION −0,0263, F-4-ALCANCE −0,0055
tic 2350 · área +0,0201 · baja S-8-EXPOSICION −0,2051, R-LLAMADA −0,0408
tic  550 · área +0,0084 · baja S-7-AGRESOR −0,0106, S-8-EXPOSICION −0,0105
```

Las áreas ganadoras son **diminutas**: de 0,005 a 0,026. El azar no gana por
mérito, gana por un pelo, y por filas que dependen de dónde estén los otros.

**Nota:** `F-4-ALCANCE` es también la fila que más **sube** contra el azar, 65
veces. O sea que el mismo renglón le da y le quita. Es el que manda en este
juego.

---

## D5 · Dónde se van los milisegundos

`cProfile` sobre **200 decisiones** de la configuración D1 (curva de la forma +
puñado propio + `D.candidatos`).

| | tiempo acumulado | % del total |
|---|---|---|
| **total** | 3,596 s / 200 = **17,98 ms por decisión** | 100 % |
| `mejor_propia2` (el puñado entero) | 3,080 s | **85,6 %** |
| **`copy.deepcopy`** | **2,111 s** | **58,7 %** |
| `foto_proyectada` | 1,534 s | 42,7 % |
| **la tabla (`appraise` + `filas`)** | **1,032 s** | **28,7 %** |
| `proyectar` | 0,527 s | 14,7 % |
| `D.candidatos` | 0,097 s | 2,7 % |

*(Son tiempos **acumulados**, así que se solapan: el `deepcopy` vive dentro de
`foto_proyectada` y de `proyectar`.)*

**Por pieza, milisegundos por llamada suelta:**

| pieza | ms |
|---|---|
| proyectar 25 tics | **0,030** |
| construir la foto | **0,039** |
| llamar a la tabla | **0,046** |
| `D.candidatos` | **0,486** |

Por decisión salen **2,55 puntos de control** y **16,1 candidatos**.

**El cuello de botella no es la tabla: es copiar.** El 58,7 % del tiempo se va
en `deepcopy` del estado y de la observación, y solo el 28,7 % en la tabla. Las
piezas sueltas cuestan centésimas de milisegundo; lo que las hace caras es
llamarlas cuarenta veces con una copia profunda cada vez.

### Si se evalúa al llegar y cada 25 tics

Con el primer tramo compitiendo cada tic como candidato normal (0,99 ms, la
decisión de hoy medida sobre los 40 diarios) y la forma evaluada una vez cada 25
tics:

| con el coste de | por tic |
|---|---|
| el banco D1 (6,88 ms) | 0,99 + 6,88/25 = **1,27 ms** |
| el perfil (17,98 ms) | 0,99 + 17,98/25 = **1,71 ms** |

**Las dos por debajo de 2 ms**, y muy por debajo de los 40,5 ms del reloj del
mundo. La vía cabe; lo que no cabe es evaluarla cada tic.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **R6a** | con D1 el azar baja del 46,9 % pero se queda por encima del 25 % | D3 | **55,41 %** en la mesa (**sube**) · **9,03 %** sobre todas (baja por debajo de 25) | **FALLA** con los dos denominadores, y en sentidos opuestos |
| **R6b** | con D1+D2 el azar baja del 20 % | D3 | **35,44 %** en la mesa · 3,08 % sobre todas | **FALLA** en la mesa |
| **R6b** | O-después por encima del 40 % | D3 | **67,90 %** en la mesa · 6,06 % sobre todas | **CUMPLE** en la mesa |
| **R6b** | diferencia mayor de 15 puntos, cero fuera | D3 | **+32,46 pts**, IC95 **+17,81 a +47,11** | **CUMPLE** |
| **R8** | más de la mitad del tiempo en la tabla | D5 | **28,7 %** · el `deepcopy` se lleva el **58,7 %** | **FALLA** |
| **R8** | al llegar y cada 25 tics, por debajo de 2 ms por tic | D5 | **1,27 ms** (banco) y **1,71 ms** (perfil) | **CUMPLE** |

**Los contadores podían variar, comprobado.** El del azar va del 7,22 % con la
puerta de hoy al 55,41 % con D1, pasando por 35,44 % con D1+D2: tres valores
muy distintos con las mismas escenas. El de la diferencia va de +1,30 a +32,46.
El del reparto del perfil podía haber dado cualquier cosa: la tabla se lleva el
28,7 %, el copiado el 58,7 %.

---

## Por qué paro, y qué propongo mirar

**R6b falla y el encargo mandaba parar.** No he tocado la regla.

**La causa, medida:** el azar gana por `F-4-ALCANCE` (42,3 %) y `S-7-AGRESOR`
(16,7 %), que son filas de **distancia a los rivales**, y la forma tiene a los
rivales **congelados donde estaban**. Alejarse de un rival que no se mueve es una
mejora gratuita y garantizada. D2 tapó la exposición; queda el alcance.

**Tres cosas que se podrían probar, propuestas y no hechas:**

1. **Extender el criterio conservador de D2 a las filas de alcance y agresor**:
   que tampoco puedan bajar de su valor en `t`. Es el mismo argumento —no se
   sabe dónde estarán— aplicado a las dos filas que quedan abiertas.
2. **Proyectar a los rivales**, aunque sea con la hipótesis más tonta (siguen su
   último rumbo). Eso quitaría el regalo, pero rompe la ceguera declarada y
   añade una fuente de error que P5-3A midió como el techo.
3. **Exigir un área mínima**, no «mayor que cero». Las áreas ganadoras del azar
   van de 0,005 a 0,026; un suelo de una décima las dejaría fuera sin tocar
   ninguna fila.

Son propuestas. **Se habla antes de tocar la regla.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`. Ficheros:
`forma.py` (con `d_de_crudas`, `curva_en2`, `curva_multi`, `mejor_propia2`),
`banco_forma4.py`, `perfil_P53D.py`, `porque_gana_azar.py`,
`P53D_D1_resumen.json`, `P53D_D1D2_resumen.json`, `P53D_porque_azar.json`,
`P53D_perfil.log`, y los progresos `P53D_D1_progreso.log` y
`P53D_D1D2_progreso.log`.
