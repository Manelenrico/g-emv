# P5-8H — El compromiso, y la cuarta sonda

**PARO AQUÍ.** Las cuarenta esperan el sí.

---

## El titular

**El compromiso hizo exactamente lo que el diseño prometía — en el único caso en
que llegó a correr.**

La forma que se aceptó en el asiento 10:

| | |
|---|---|
| obedeció el paso de la forma | **5 de 5 tics con piernas listas = 100 %** |
| rupturas | **0** |
| coste del compromiso | **+0,000** — el decisor ya prefería la forma |
| **distancia al destino** | **5 → 1** |
| **lo que prometía ver** | **76 durante · 9 después · 0 nunca** |
| casillas nuevas/100 tics | **110,20 dentro** contra 6,90 fuera |

**Es la primera vez en cuatro sondas que una forma llega, ve lo que prometió, y
no deja nada sin ver.** En P5-8F el 76,9 % del objetivo no se veía nunca; aquí,
**cero**.

**Y el precio se iguala:** A 0,043067 $ · K **0,044335 $**, con cola y juego
idénticos (2,1/2,2 min y 8,4/8,5 min). K deja de costar el doble.

**Pero es una forma.** El otro asiento nació 155 formas y **no aceptó ninguna**,
y en P5-8E ese mismo asiento aceptó 53 de 140. **Ese derrumbe no lo sé
explicar**, y lo pongo en el titular porque manda sobre lo demás.

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
| etiqueta | **`gemv-anima:curforma-h0`** |
| id | `sha256:6afe40f83aeab5e3bad7f7e83ac73382893fabfe3485d79a6c36a5d4e36db599` |
| manifiesto | `sha256:e32f3d04a75009a2b1e87c1873783e611356cde41ecf3d2eb292c64311a0e1b3` |
| config | `sha256:594e5fa0285f4ebef2838392cc86780fdaf772a5a602cfe25822229c4fe2f41a` |

md5 dentro: `policy_forma.py` `891cea92a87d4866155221023e09615b` ·
`curiosidad_forma.py` `4d2ef856a45d1b890b7135036bcd69ef` · `humo_curforma.py`
`68ccb0100459ffa9286c110b4f1f238f`.
Políticas `gemv-p58h-A:v1` (`7f136548-…`) y `gemv-p58h-K:v1` (`c12eab31-…`).

---

## El humo, y la escena que estaba mal

```
  (g) compromiso: 49 registros · obedece 5 · rompe 0 · enfriamiento 44
      (a) obedece con un ganador DISTINTO al paso de la forma: 0/5
          (aviso) en esta escena el decisor ya prefería la forma
      (b) armado CORTO a 5 acercandose (antes 6): ruptura = e) armado a menos de 6 y acercandose
      (c) pacifico sin arma a 4: ruptura = None (debe ser None)
```
Más los de P5-8E, todos verdes.

**El humo encontró un error mío en la propia prueba.** La primera versión de (b)
ponía un **arco** a 5 casillas y salía ruptura **(a) veto vital**, no (e) — y con
razón: **un arco a cinco casillas sí está a tiro**. La escena estaba mal, no el
código. Cambiada a un arma corta, (e) dispara como debe.

**Y un aviso que dejo en el humo**: en esa escena el decisor ya prefería la
forma, así que **(a) no prueba que se imponga a un ganador distinto**. Lo dice
él mismo en vez de callarlo.

---

## La sonda

### Precio, cola y juego

| brazo | precio | cola | juego |
|---|---|---|---|
| **A** | 0,043067 $ | 2,1 min | 8,4 min |
| **K** | **0,044335 $** | 2,2 min | 8,5 min |

**K vuelve al rango y se iguala con A.** Tras tres sondas con K entre 0,056 y
0,108, ésta es la primera en que los dos brazos cuestan lo mismo.

### El hilo

| asiento | vivos | **perdidos** | ms mediana | máx |
|---|---|---|---|---|
| A/10 | 8.035 | **0** | 1,588 | 23,093 |
| A/11 | 10.584 | **0** | 0,348 | 17,242 |
| K/10 | 7.847 | **0** | 1,215 | 24,368 |
| K/11 | 8.295 | **0** | 0,575 | 18,716 |

**Cero tics perdidos**; K por debajo de 5 ms.

### El compromiso, donde corrió

| K/10 | |
|---|---|
| formas nacidas | 85 |
| **aceptadas** | **1** |
| tics con piernas listas | 5 |
| **obedece** | **5 = 100 %** |
| rompe | **0** (ninguna de las siete causas) |
| enfriamiento | 44 |
| **coste** | **+0,000** en 5 tics |
| fin | **completada por alivio**, vive 50 tics |
| distancia | **5 → 1** |
| lo prometido | **76 durante · 9 después · 0 nunca** |
| nuevas/100 tics | **110,20 dentro** · 6,90 fuera |

| K/11 | |
|---|---|
| nacidas | 155 |
| **aceptadas** | **0** |
| el compromiso | **nunca llegó a correr** |

---

## Lo que no sé, marcado como tal

**El derrumbe del asiento 11 es lo que más me preocupa y no lo explico.** En
P5-8E aceptó **53 de 140**; aquí, **0 de 155**. El compromiso no puede ser la
causa directa —sin formas aceptadas nunca se activó—, así que o es variación del
mundo, o el cambio movió la trayectoria del cuerpo lo bastante como para que el
estado en que nacen las formas sea otro. **Con una partida no lo separo.**

**Los números buenos salen de UNA forma.** El 100 % de obediencia, el coste
cero, el 5 → 1, el «cero nunca»: **n = 1**. No son un resultado, son un caso que
por fin se comporta.

**El coste cero no prueba que el compromiso sea barato.** Salió cero porque en
esos cinco tics el decisor ya prefería la forma. **El caso interesante —obedecer
contra el criterio del cuerpo— no ocurrió ni en el humo ni en la sonda.** Es
justo lo que el compromiso existe para hacer, y **sigue sin medirse**.

**Tampoco sé si las siete rupturas funcionan en vivo.** Cero disparos. El humo
prueba que (e) discrimina entre un armado que se acerca y un pacífico; las otras
seis, en campo, **no se han visto nunca**.

---

## Propuesta, no ejecución

**No recomiendo lanzar las cuarenta todavía**, y por una razón distinta a las
veces anteriores: **no porque algo falle, sino porque la sonda no tiene
potencia**. Con una forma útil por sonda, las cuarenta darían quizá veinte o
treinta formas con compromiso — suficiente para K4 y K6, pero **la asimetría
entre asientos (53 → 0) haría que la mitad de los asientos no aportara nada**, y
K1 se mediría sobre un puñado.

**Lo que yo haría antes, y es barato:** una sonda de **cuatro o cinco semillas**
(ocho o diez partidas, ~0,4 $) solo para ver **cuántas formas se aceptan por
asiento y con qué dispersión**. Si la aceptación sigue siendo 0 en la mitad de
los asientos, las cuarenta no van a dar la n que los sellos piden, y conviene
saberlo antes que después.

**No lo he hecho.** Decidir es de la mesa.

**Gasto de la sonda: 0,087402 $.** Cola vacía antes y después.

**PARO AQUÍ.**
