# P5-3C — El comparador justo

En seco, coste cero. Nada a la plataforma. **Ninguna decisión real cambia.**
Mismas 2.230 escenas, semilla **20260919**, mismas llaves, mismos tres
criterios, `VIDA_MIN = 15`, pesos `0,5 ^ (tic / 50)`. QUÉDATE retirada.

**Dos resultados, y el segundo es el que manda.**

**Primero: el comparador justo no cambia casi nada.** O-después pasa de 70,88 %
a **70,89 %** y el azar de 46,79 % a **46,90 %**. R2' se cumple otra vez
(+23,99 puntos) y **R6' vuelve a fallar** (46,90 % contra el 15 % sellado). La
razón por la que no cambia nada es el hallazgo: **en el 96 % de las escenas el
puñado del cuerpo tiene un solo candidato, `noop`**, porque en el tic de la
escena las piernas están enfriando. El «comparador justo» resulta ser, en la
práctica, el mismo comparador flojo.

**Segundo, y es un techo duro: no cabe en el reloj del mundo.** Proyectar el
puñado entero como formas cuesta **52,6 ms de mediana** y **129,8 ms como
máximo**, contra los **0,99 ms** que cuesta hoy una decisión. El reloj del mundo
son **40,5 ms por tic**. **La mediana ya se lo come entero.**

---

## El arnés, con la forma apagada

```
REPRODUCCION CON LA PROYECCION IMPORTADA: 11,804/11,804 = 100.00 %
```

Sigue al 100,00 % con `proyeccion.py` y `forma.py` importados.

---

## El cambio, y cómo se ha implementado

«Seguir solo» deja de ser «el paso ganador y luego quedarse». Ahora **cada
candidato propio de `t`** se convierte en una forma de un tramo —llegar, coger o
usar si procede, y esperar hasta el mismo horizonte— y se proyecta con las
mismas reglas y la misma foto del mundo, **en los mismos tics de control**.

**Dos decisiones declaradas, porque el encargo no las fijaba:**

1. **Cómo se elige «la mejor».** A cada curva propia se le calcula el **coste
   ponderado** de su `d`, con los mismos pesos de la regla. La mejor es la de
   menor coste **entre las que pasan la vida mínima**; si ninguna la pasa, se
   coge la de menor coste igualmente y queda marcado.
2. **La regla no cambia**: la forma se acepta si su área ponderada contra esa
   mejor curva propia es positiva y ningún punto suyo baja de 15.

## Quién resulta ser «la mejor propia»

| llave | `noop` | `ir_pareja` | `ir_centro` | `ir_botin` | `ir_objeto` | `usar_*` |
|---|---|---|---|---|---|---|
| O-después | **872** | 13 | 10 | 7 | 1 | 3 |
| azar emparejado | **854** | 15 | 11 | 13 | 14 | 1 |

**La mediana del tamaño del puñado es 1.** En el 96 % de las escenas el único
candidato vivo es `noop`, y por tanto la mejor curva propia es **quedarse
quieto**.

**La causa está medida desde P5-2b:** el cuerpo pasa el **75,69 %** de los
instantes con las piernas enfriando, y `D.candidatos` filtra por el veto antes
de devolver la lista (`decisor_zs.py:605`). En el tic suelto de la escena, casi
nunca hay nada más que elegir.

**Consecuencia honesta:** el comparador que el encargo pedía para ser más duro
**no lo es**, no por cómo lo he escrito sino porque en ese instante el cuerpo no
tiene puñado. Para que lo fuera habría que construirlo en el **tic de ventana**,
cuando las piernas ya están listas, no en el de la escena.

---

## C1 · Las tres puertas, mismas escenas, criterio de vida entera

| | **puerta de hoy** (P52c) | **ancha, comparador flojo** (P53B) | **ancha, comparador justo** (P53C) |
|---|---|---|---|
| **O-después** | **8,52 %** (72/845) | **70,88 %** (404/570) | **70,89 %** (397/560) |
| **azar emparejado** | **7,22 %** (61/845) | **46,79 %** (197/421) | **46,90 %** (189/403) |
| **diferencia** | **+1,30 pts** | **+24,08 pts** | **+23,99 pts** |
| IC95 de la diferencia | **−1,27 a +3,87** | +18,03 a +30,14 | **+17,84 a +30,15** |
| ¿distingue? | **no** | sí | **sí** |

Sobre **todas** las formas construidas (908 en cada brazo), en vez de sobre las
que llegan a la mesa:

| | P53B | P53C |
|---|---|---|
| O-después | 44,49 % | **43,72 %** |
| azar emparejado | 21,70 % | **20,81 %** |

### Las cajas enteras

| criterio | llave | aceptada | coincide | rechazada | rech. vida | rech. área | vetada |
|---|---|---|---|---|---|---|---|
| estricto | O-ahora | 0 | **2.230** | 0 | 0 | 0 | 0 |
| | O-después | 7 | 2 | 4 | 22 | 326 | 547 |
| | azar empar. | 5 | 0 | 5 | 29 | 476 | 393 |
| ventana | O-ahora | 0 | **2.230** | 0 | 0 | 0 | 0 |
| | O-después | 331 | 2 | 227 | 22 | 326 | 0 |
| | azar empar. | 119 | 0 | 284 | 29 | 476 | 0 |
| **vida entera** | O-ahora | 0 | **2.230** | 0 | 0 | 0 | 0 |
| | **O-después** | **395** | 2 | 163 | 22 | **326** | 0 |
| | **azar empar.** | **189** | 0 | 214 | 29 | **476** | 0 |

El comparador justo endurece la **regla**, no la mesa: los rechazos por área
suben de 316 a **326** en O-después y de 458 a **476** en el azar. Diez y
dieciocho formas más. Es todo lo que mueve.

---

## C2 · Contra qué gana el azar

**En qué punto de control gana cada forma aceptada:**

| llave | punto 1 | punto 2 | punto 3 | punto 4 |
|---|---|---|---|---|
| O-después | **378 de 558** (67,7 %) | 89 | 6 | 48 |
| **azar emparejado** | **396 de 403 (98,3 %)** | 7 | — | — |

**El azar gana en el primer punto de control, casi siempre.** Su forma tiene dos
puntos: llegar a la casilla sorteada, y esperar. Gana en el de llegar.

**Y contra qué gana**: contra `noop`, en el 98 % de los casos, porque la mejor
curva propia **es** `noop`. La curva del azar baja la `d` sencillamente porque
**moverse a cualquier sitio baja la `d` frente a quedarse quieto**, y la tabla lo
premia por la vía de la exposición y del botín: al moverse cambia la casilla
prevista, y con ella `S-8-EXPOSICION` y `R-LLAMADA`.

**En la mesa**, cuando llegan a competir de verdad, la fila que las tumba sigue
siendo la misma en las dos:

| llave | exposición | otras | n |
|---|---|---|---|
| O-después | 3 | reencuentro 1 | **4** |
| azar emparejado | **5** | — | **5** |

Con n de cuatro y cinco: casi todo se decide ya en la regla.

---

## C3 · El coste de cómputo

| | valor |
|---|---|
| decisiones medidas | 1.814 |
| **mediana** | **52,56 ms** |
| p90 | 96,67 ms |
| **máximo** | **129,76 ms** |
| tamaño mediano del puñado | **1 candidato** |
| decisión de hoy, mediana sobre 40 diarios | **0,99 ms** |
| decisión de hoy, p95 | 3,92 ms |
| decisión de hoy, máximo | 31,01 ms |
| **el reloj del mundo** | **40,5 ms por tic** (24 tics/s) |

**No cabe, y no cabe por poco: no cabe por mucho.** La mediana de 52,6 ms ya se
come el fotograma entero de 40,5 ms, y el p90 lo duplica. Es **53 veces** lo que
cuesta una decisión hoy.

**Y el dato es optimista**, porque el puñado mediano es de **un** candidato. Los
casos con las piernas libres, que son los que de verdad tendrían que compararse,
son los del p90 y el máximo.

**Lo que esto significa:** proyectar el puñado entero como formas **no se puede
hacer dentro del tic**. Si esta vía sigue, tiene que ser fuera del bucle —en un
hilo aparte, como el consejero, con su propia latencia y su propia caducidad— o
con muchos menos puntos de control.

---

## C4 · La figura

`cantera/paper5/figB/C4_formas.png`: las mismas tres escenas de B6 —una
aceptada, una rechazada por vida mínima, una rechazada por área— pero con **la
mejor curva del puñado propio** en vez de la de quedarse, y con el nombre de esa
mejor propia en el título de cada panel.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **R2'** | O-después gana al azar por más de 10 puntos, cero fuera (vida entera) | C1 | **+23,99 pts**, IC95 **+17,84 a +30,15** | **CUMPLE** |
| **R3'** | O-ahora 100 % en los tres criterios | C1 | **2.230 de 2.230** en los tres | **CUMPLE** |
| **R6'** | el azar baja por debajo del 15 % con vida entera | C1 | **46,90 %** (20,81 % sobre todas las formas) | **FALLA** |
| **R7** | O-después baja respecto a P53B pero se queda por encima del 40 % | C1 | **70,89 %** contra 70,88 %: **no baja** · sobre todas las formas, 43,72 % contra 44,49 %: baja 0,77 pts | **medio**: no baja en la mesa, baja una pizca sobre todas; **por encima del 40 % en los dos casos** |

**Los contadores podían variar, comprobado.** El de R2' va de +1,30 a +24,08
según la puerta. El de R3' valió **0 %** en mi primera corrida de P5-3B, con el
fallo de orden. El de R6' va del 7,22 % con la puerta de hoy al 46,90 % con la
ancha. El de R7 podía bajar: la regla se endureció de verdad, y diez formas de
O-después y dieciocho del azar cambiaron de caja por ello. Lo que pasa es que
diez de 908 no mueven una tasa.

---

## R6' falla: la regla premia moverse, y hay que revisarla

La predicción lo decía: **«si no baja, la regla premia moverse y hay que
revisarla antes de seguir»**. No baja: **46,90 %**.

**La cadena, con las cifras de este informe y de los anteriores:**

1. El cuerpo pasa el **75,69 %** de los instantes con las piernas enfriando
   (P5-2b).
2. `D.candidatos` filtra los vetados, así que en el tic de la escena el puñado
   es **un solo candidato, `noop`**, en el 96 % de los casos.
3. La mejor curva propia es, por tanto, **quedarse quieto**.
4. Cualquier forma que se mueva cambia la casilla prevista y con ella la
   exposición y la llamada del botín, y **baja la `d`**.
5. El área sale positiva y la regla acepta. **Da igual adónde vaya.**

**No he construido nada más.** El encargo mandaba parar aquí si R6' fallaba, y
ha fallado.

### Lo que propongo mirar, sin haberlo hecho

- **Construir el comparador en el tic de ventana**, no en el de la escena: con
  las piernas listas el puñado tiene candidatos de verdad y la comparación sería
  la que el encargo buscaba.
- **Normalizar el área por el movimiento**: comparar contra la mejor forma
  propia **que también se mueva**, para que «moverse» deje de ser la ventaja.
- **Revisar el peso de la exposición en la `d` del futuro proyectado**: es la
  fila que firma casi todos los rechazos en la mesa y, por el otro lado, la que
  regala la ventaja al que se mueve.

Son propuestas, no decisiones.

## Una corrección sobre mi estimación de tiempo

Dije que esta corrida acabaría hacia las **12:56** y acabó a las **13:09**: 52
minutos reales contra 41 estimados, un **25 % por encima**. El ritmo de los
siete primeros diarios no valía para extrapolar, porque los diarios que quedaban
eran más largos y con más escenas por diario.

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`. Ficheros:
`forma.py` (con `mejor_propia`, `curva_en`, `coste`, `forma_de_candidato`),
`banco_forma3.py`, `fig_P53B.py`, `P53C_resumen.json`, `P53C_progreso.log`,
`P53C_corrida.log`, `figB/C4_formas.png`.
