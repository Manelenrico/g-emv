# P5-8D — El reloj honesto, la forma que cumple al cobrar, y la segunda sonda

**PARO AQUÍ. Las cuarenta siguen sin poder lanzarse**, y la razón es nueva.

---

## El titular

**El arreglo funciona: ninguna forma muere ya por «deja de ganar».** Las
duraciones dejan de ser 25-25-25 y pasan a **mín 26 · mediana 36 · máx 51**. El
reloj honesto hizo su trabajo.

**Pero ha salido un segundo defecto de la misma familia, y es mío: el atasco.**
De las 51 formas aceptadas, **50 mueren por atasco** y solo **1 se completa por
alivio**. El atasco exige acercarse al destino en **25 tics**; con **11 tics por
casilla**, en 25 tics el cuerpo avanza **dos casillas como mucho**. Es la misma
trampa de escala que acabo de arreglar en el examen, **repetida en otro
contador que yo mismo puse en P5-8B**.

**Y hay un dato que no me gusta y no voy a maquillar:** en el asiento con datos
(50 formas, 1.708 tics dentro de forma), las casillas nuevas por cien tics
**dentro** de forma son **1,35** y **fuera** son **8,66**. **Dentro de la forma
se ve menos, no más.** En el otro asiento pasa lo contrario (112,50 dentro
contra 6,62 fuera) pero con **32 tics y una sola forma**. Con dos asientos no se
puede decir cuál es la regla.

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
| etiqueta | **`gemv-anima:curforma-d0`** |
| id | `sha256:66e9e0440749f65185e184da84f9017dd5deb63970291918c12eaa1ebe9be440` |
| manifiesto | `sha256:2190107fb25766043138cbe2ee375d9f0c3b7d5721109174b690b859befa59bb` |
| config | `sha256:554de1f62231e78ad2bce5df269cbd4ea153d23ddea17a5fb469fcd531d0ffb6` |

md5 leídos **dentro**: `policy_forma.py` `2369b5ed3ae0f8e11550a1418eeda8f6` ·
`curiosidad_forma.py` `5687f0f3129970290b7f82088ab2e3de` ·
`humo_curforma.py` `d6332507d19a25e0e218fd3b4e9679b7`.

Políticas `gemv-p58d-A:v1` (`a20606e1-…`) y `gemv-p58d-K:v1` (`faa51b82-…`).
**Ninguna llama a ningún modelo.**

---

## Los humos

```
  (a) APAGADO identico: 200/200 decisiones · 0 registros de curiosidad-forma
  (b) el brazo K vive: 3 nacidas · 1 aceptada
      forma 2 -> destino (23, 21): distancia 5 -> 2 en 49 tics
  (c) VETO DURO: sin armado False · con un armado sobre el camino True
  (d) duracion: min 50 · mediana 50 · max 50 (CADA_REEVALUA = 25)
      causas: {'completada por alivio': 1}
  (e) muertes por «deja de ganar» ANTES de la llegada proyectada: 0 (debe ser 0)
      completadas POR ALIVIO: 1
LOS HUMOS DEL BRAZO K OK
```

**Los tres cambios se ven funcionar en el humo**: la forma vive 50 tics en vez
de 25, el cuerpo se acerca de 5 a 2 casillas, y termina **por alivio**.

---

## La sonda

### Precio y cola

| brazo | precio | |
|---|---|---|
| **A** | **0,044500 $** | dentro de 0,04-0,08 |
| **K** | **0,055943 $** | **dentro** |

**K vuelve al rango.** En la sonda 1 salió a 0,107574 $; ahora **la mitad**. No
hizo falta mirar la cola. *(Con n=1 por brazo no afirmo que el cambio lo haya
causado; puede ser variación del pod.)*

### El hilo

| asiento | tics vivos | **perdidos** | ms mediana | ms máx |
|---|---|---|---|---|
| A/10 | 8.117 | **0** | 0,716 | 15,820 |
| A/11 | 9.801 | **0** | 0,825 | 45,767 |
| K/10 | 9.368 | **0** | 1,495 | 18,547 |
| K/11 | 10.893 | **0** | 1,169 | 18,482 |

**Cero tics perdidos.** K sigue por debajo de 5 ms (K6 cumpliría).

### Las formas, con sus causas de fin

| | K/10 | K/11 |
|---|---|---|
| nacidas | 103 = **1,10**/100 tics | 133 = **1,22**/100 tics |
| aceptadas | 1 | 50 |
| **completada por alivio** | **1** | 0 |
| completada por llegada | 0 | 0 |
| deja de ganar | **0** | **0** |
| veto duro | 0 | 0 |
| **atasco** | 0 | **50** |
| duración (mín·mediana·máx) | 33·33·33 | **26·36·51** |

**Cero muertes por «deja de ganar»: el arreglo de P5-8D funciona.**
**Cincuenta de cincuenta por atasco: el arreglo destapó el siguiente cuello.**

### Casillas nuevas por cien tics — informado, no sellado

| | dentro de forma | fuera de forma | tics dentro |
|---|---|---|---|
| **K/10** | **112,50** | 6,62 | **32** |
| **K/11** | **1,35** | 8,66 | 1.708 |
| A/10 | — | 7,15 | 0 |
| A/11 | — | 7,44 | 0 |

**Los dos asientos de K dicen lo contrario.** El que tiene datos dice que dentro
de la forma se ve **menos**; el otro, con 32 tics y una forma, dice que se ve
diecisiete veces más. **No hay conclusión aquí**, y va sin sello como se pidió.

---

## Los sellos, con lo que la sonda anticipa

| | sello | lo que la sonda dice |
|---|---|---|
| **K4** | completadas (llegada + alivio) ≥50 %; veto duro 5-30 % | **1 de 51 = 2 %** y veto duro **0 %** — fallaría |
| **K6** | <5 ms y cero perdidos | **cumple** (1,2-1,5 ms, cero perdidos) |
| **K7** | ≤4 $ | con 0,056 $/partida, **~2,2 $** proyectados |
| K3 | cero con armado a tiro y forma activa | sin decisiones problemáticas en la sonda |

**K4 fallaría, pero ahora por el atasco, no por la puerta.**

---

## Lo que no sé, marcado como tal

**No sé si el atasco de 25 tics es el único cuello que queda.** Lo he
diagnosticado por aritmética —11 tics por casilla contra un plazo de 25— y eso
es sólido; pero ya me equivoqué una vez diagnosticando por aritmética en
P5-8B, así que **no lo afirmo hasta medirlo**.

**No sé por qué los dos asientos de K dan resultados opuestos** en casillas
nuevas dentro de forma. Uno tiene 32 tics dentro y el otro 1.708. **Con dos
asientos no hay con qué.**

**No sé si el precio de K bajó por el cambio o por azar del pod.** n=1.

**Y no sé por qué el asiento 10 aceptó 1 de 103 y el 11 aceptó 50 de 133.** La
misma partida, la misma semilla, los dos asientos del mismo equipo. Esa
diferencia ya apareció en la sonda 1 (1/145 contra 38/162) y **sigue sin
explicación**.

---

## Propuesta, no ejecución

**El atasco debe medirse en el mismo reloj que el resto**: si el cuerpo tarda 11
tics por casilla, exigirle acercarse en 25 tics es exigirle dos casillas. Lo
coherente con R2 sería **darle el mismo plazo que al examen** —la llegada
proyectada— o al menos **un múltiplo del paso**, no una constante en tics.

**No lo he cambiado.** Sería el tercer cambio de reloj en dos días y **prefiero
que la mesa decida si esto es afinar o es perseguir la propia cola**. Los datos
dicen que cada vez que arreglo un plazo aparece otro detrás; puede que el
mensaje sea que **una forma de seis casillas en un cuerpo que anda a 11 tics por
casilla es demasiado lenta para cualquier plazo que la puerta tolere**.

**Gasto de la sonda: 0,100443 $.** Cola vacía antes y después.

**PARO AQUÍ.**
