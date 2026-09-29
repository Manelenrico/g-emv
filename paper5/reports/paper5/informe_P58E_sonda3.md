# P5-8E — El atasco en el reloj del mundo · TERCERA SONDA

**PARO AQUÍ.** Las cuarenta siguen esperando el sí.

---

## El titular

**El cambio funciona y la asimetría queda explicada, pero el resultado que la
serie busca sigue sin aparecer — y ahora hay dos sondas que dicen lo mismo.**

- **El atasco en pasos hace su trabajo:** ya no mata todo. En el asiento con
  datos, de 53 formas aceptadas **solo 22 han terminado**, y la duración es
  **22 · 34 · 34** (mín·mediana·máx) en vez de 25-25-25.
- **El veto duro disparó por primera vez en el campo**: 1 caída. El mecanismo
  vive, no solo en el humo.
- **Y la asimetría entre asientos tiene explicación**, que es lo que pediste:
  **el asiento rico acepta menos**. W mediana **1,25** en el asiento que aceptó
  **1 de 153**; W **0,667** en el que aceptó **53 de 140**. Las formas
  rechazadas del asiento pobre tienen **el doble de ventaja** (+0,0342 contra
  +0,0166).

**Lo que no aparece, por segunda sonda consecutiva: la exploración.** Casillas
nuevas por cien tics **dentro** de forma **0,41** contra **8,87 fuera** en el
asiento con 1.706 tics de forma. **Dentro de la forma se ve veinte veces
menos.** En P5-8D fue 1,35 contra 8,66. **Dos sondas, el mismo signo.**

---

## Custodia

```
                            al empezar                         al acabar
motor/model.py              1e511978c251130e95169ebf8443efa1   idéntico
paintball/alma/decisor_zs.py
                            8fa03547e3228ef9df4aa94c444f9252   idéntico
paintball/alma/appraisal_zs_v42_exp.py
                            98c13d60167c80cc8334c965be75c640   idéntico
```

### La imagen

| | |
|---|---|
| etiqueta | **`gemv-anima:curforma-e0`** |
| id | `sha256:e6167599fd9bad6db9eb0072400e37fc5fe1e24010561443afce44f500aebb4c` |
| manifiesto | `sha256:0d5f88c855fa707fbf06aad297658cad7725d320285667f77fcc7360fcd45012` |
| config | `sha256:34a1365638f44fbb03777fe501c9e8ce55b31e162864b4f314da5b0f3686522c` |

md5 dentro: `policy_forma.py` `75e1fb3b4ad111431958021c2ea5386d` ·
`curiosidad_forma.py` `5687f0f3129970290b7f82088ab2e3de` · `humo_curforma.py`
`bc44f40571107a4eb3b2b2d0ccd2d604`.
Políticas `gemv-p58e-A:v1` (`ff7fa54c-…`) y `gemv-p58e-K:v1` (`7597a8d0-…`).

---

## El grep de los plazos de 25 tics

**Queda uno, y lo señalo en vez de tocarlo.**

```
paintball/alma/forma_viva.py:22   CADA_REEVALUA = 25
paintball/alma/forma_viva.py:72   return (tick - self.ultima_revision) >= CADA_REEVALUA
```

Gobierna los exámenes **posteriores** al primero. **P5-8D mandaba conservarlo**
(«después, cada 25 tics como siempre») y **P5-8E dice “un solo cambio”**, así
que no lo he movido. Pero tu frase «el plazo de 25 tics constantes desaparece de
la forma de curiosidad en todos los sitios donde quede» también lo alcanza.
**Es una contradicción entre los dos encargos y la resuelvo hacia el mínimo
cambio, declarándola.** En `policy_forma.py` no queda ningún plazo constante de
25 en la ruta de curiosidad.

---

## El humo

```
  (f) atasco: 3 pasos x 11 tics/casilla = plazo 33 tics (antes: 25 constantes)
      (f1) avanzando 1 casilla cada 11 tics: se atasca = False (debe ser False)
      (f2) quieto: se atasca = True al tic 33 (debe ser True, y a los 33)
```
Más los cinco de P5-8D, todos verdes: apagado idéntico 200/200, el cuerpo se
acerca de 5 a 2 casillas, veto duro discrimina, cero muertes por «deja de ganar»
antes de la llegada, y una completada por alivio.

---

## La sonda

### Precio — y no es la cola

| brazo | precio | **cola** | **juego** |
|---|---|---|---|
| **A** | 0,049848 $ | 2,5 min | 9,3 min |
| **K** | **0,100763 $** | **2,5 min** | **9,4 min** |

**K vuelve a salir por encima de 0,08, y la cola queda descartada**: los dos
brazos esperaron lo mismo y jugaron lo mismo. **K cuesta el doble por la misma
cola y el mismo juego.** No sé por qué, y es la tercera vez que el precio de K
se mueve sin patrón (0,1076 · 0,0559 · 0,1008).

### El hilo

| asiento | vivos | **perdidos** | ms mediana | máx |
|---|---|---|---|---|
| A/10 | 8.487 | **0** | 1,261 | 33,881 |
| A/11 | 9.571 | **0** | 0,605 | 14,499 |
| K/10 | 9.219 | **0** | 1,173 | 16,662 |
| K/11 | 7.807 | **0** | 0,525 | 22,631 |

**Cero tics perdidos.** K por debajo de 5 ms.

### Las formas, y la asimetría explicada

| | **K/10** | **K/11** |
|---|---|---|
| nacidas | 153 = 1,66/100 tics | 140 = 1,79/100 tics |
| **aceptadas** | **1** | **53** |
| **W mediana** | **1,250** | **0,667** |
| amenaza mediana | 0,0 | 0,0 |
| **ventaja de las rechazadas** | **+0,0166** (Q1 0,0000 · Q3 +0,0215) | **+0,0342** (Q1 +0,0340 · Q3 +0,0368) |
| terminadas | 1 | 22 |
| completada por alivio | **1** | 0 |
| **atasco** | 0 | **21** |
| **veto duro** | 0 | **1** |
| deja de ganar | **0** | **0** |
| duración (mín·med·máx) | 33·33·33 | **22·34·34** |

**Ésta es la respuesta a por qué un asiento acepta 1 y el otro 53: la riqueza.**
Con W = 1,25 el cuerpo tiene menos carencia, sus propias opciones valen más, y
la forma de curiosidad no le gana por el margen. Con W = 0,667 sí. La amenaza
mediana es **cero en los dos**, así que no es el peligro: **es el bolsillo**.

### Casillas nuevas por cien tics — informado, no sellado

| | dentro de forma | fuera | tics dentro |
|---|---|---|---|
| **K/10** | 112,50 | 6,14 | **32** |
| **K/11** | **0,41** | **8,87** | 1.706 |
| A/10 | — | 6,50 | 0 |
| A/11 | — | 7,42 | 0 |

**El asiento con datos vuelve a decir que dentro de la forma se ve menos**, y
más fuerte que en P5-8D (0,41 contra 1,35). El asiento con 32 tics dice lo
contrario, igual que antes.

---

## Lo que no sé, marcado como tal

**No sé por qué dentro de la forma se ven menos casillas nuevas.** Tengo una
sospecha —la forma lleva al cuerpo hacia una frontera que ya está viendo
mientras camina, de modo que las casillas se descubren **antes** de entrar en
forma, no durante— pero **no la he medido**. Y hay otra posible: que el cuerpo,
al seguir la forma, deje de hacer lo que le hacía descubrir cosas. **Las dos
caben y no las separo con dos asientos.**

**No sé por qué K cuesta el doble con la misma cola y el mismo juego.**
Descarto la cola con datos; lo demás es especulación.

**El asiento K/10 sigue dando n=1.** Todo lo que diga de él es un caso.

**Y no sé si el atasco es el último cuello.** 21 de 22 finales siguen siendo por
atasco, ahora con plazo 33 en vez de 25. **Puede que 33 tampoco baste**, o puede
que el cuerpo simplemente no siga la forma lo suficiente.

---

## Propuesta, no ejecución

**Recomiendo NO lanzar las cuarenta todavía**, y no por un defecto nuevo, sino
porque **la serie mediría K1 —casillas nuevas dentro contra fuera— y dos sondas
seguidas dicen que ese cociente va en contra**, con el asiento de más datos
dando 0,41 contra 8,87. Gastar ~2,4 $ y cuarenta partidas para confirmar un
signo negativo que ya se ve en la sonda es caro.

Lo que yo haría antes, en seco y a coste cero: **medir en los diarios que ya
tengo cuándo se descubren las casillas de una forma — antes de entrar en ella,
durante, o después**. Eso separa mis dos sospechas y decide si el problema es la
forma o la medida.

**No lo he hecho.** Y señalo lo que ya dije en P5-8D: **éste es el tercer cambio
de reloj en tres sondas.** Cada arreglo ha funcionado y ha destapado el
siguiente. Puede que toque parar de afinar plazos y preguntarse si la forma de
curiosidad, en un cuerpo que anda a once tics por casilla, tiene sitio.

**Gasto de la sonda: 0,150611 $.** Cola vacía antes y después.

**PARO AQUÍ.**
