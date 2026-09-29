# P5-7C — La frontera en el campo

## C0 · La imagen, construida y con sus humos dentro

**Nada lanzado.** La serie C1 espera el sí.

---

### El titular de C0

**La curiosidad cabe en el bucle del juego.** Con el interruptor apagado la
política es **idéntica decisión a decisión** en los 200 tics de la escena
grabada; encendida, el renglón entra en la foto de **todos** los candidatos y
vuelve el tic entero en **3,321 ms de mediana dentro de la imagen**, por debajo
de los 5 ms que pide Q5, con **cero tics sin decisión**.

---

### La imagen

| | |
|---|---|
| etiqueta | **`gemv-anima:curiosidad-c0`** |
| id (lista de manifiestos) | `sha256:57bd6f366d3129f965091b57f277ae29ec1508f179451cd98839e6267722efe4` |
| manifiesto | `sha256:3192da17910b88874c4764a664a49406ff72117a25fb80f0ef18afa7f7e23405` |
| config | `sha256:1bc32e166b6c75bfd8326b6191f3ebae575e9e418264d1c65ea5f80a5b72b5e0` |

**Nombre nuevo para contenido nuevo**, como quedó fijado en P5-6C C0: una
etiqueta por build, nunca reutilizada.

#### md5 de contenido, leídos **dentro** de la imagen

```
motor/model.py                       1e511978c251130e95169ebf8443efa1   (INTOCABLE)
alma/decisor_zs.py                   8fa03547e3228ef9df4aa94c444f9252   (sin tocar)
alma/appraisal_zs_v42_exp.py         98c13d60167c80cc8334c965be75c640   (sin tocar)
alma/policy_forma.py                 2d58ff330a1d377113d8b625d6b728ac   (+ interruptor)
alma/curiosidad.py                   f803f47c8ed0a8eaf3855d7e1dc7d457   (nuevo)
alma/humo_curiosidad.py              7b38d5a64f8562e3d092b4bf72c681eb   (nuevo)
alma/forma.py                        b801876afda071403c5af54a28feff85
alma/proyeccion.py                   bbc42daeaa769c783844997067ef148d
```

El build **verifica los tres primeros y se cae si cambian**. El decisor y la
tabla siguen byte a byte los de la serie de las cien.

---

### El interruptor

```
GEMV_CURIOSIDAD=frontera     instala R-CURIOSIDAD-FRONTERA
GEMV_CURIOSIDAD_K=0.2        la ganancia
GEMV_CURIOSIDAD_BALANZA=1    el factor (1 − amenaza)
```

**La imagen viene apagada** (`GEMV_CURIOSIDAD=` vacío), y el humo (e) lo
comprueba. Vacío o `0` deja la política **exactamente** como estaba: el
despachador llama directo a la de siempre y no registra nada.

`curiosidad.py` es **el mismo fichero que usó el banco de P5-7A**, copiado a la
imagen desde `cantera/paper5/`: **no hay copia divergente en el repo**. Para que
pudiera viajar hubo que quitarle la dependencia de `serie_util`, que vive en
`cantera/paper4` y no entra en la imagen; el banco se volvió a correr entero
después del cambio y sigue dando lo mismo.

**Dónde se instala:** `D.A` pasa a ser el proxy que delega todo en v42 y solo
reimplanta el montaje del `State`, igual que en el banco. El renglón queda
**fuera** del appraisal; el decisor y la tabla no se tocan.

---

### El registro nuevo, por tic

```json
{"k":"curiosidad_tic","tick":...,
 "ign_global":0.8902,"dist_frontera":3,"amenaza":0.0,"grado":"seguro",
 "amenaza_desglose":{"armados":0.0,"n_armados":0,"dano":0.0,"anillo":0.0},
 "encendio":true,"decidio":false,
 "cands_con_M":17,"cands":17,"max_M":0.11476,"vistas":470,
 "ms_bfs":2.495,"ms_contrafactual":0.330,"ms_total":3.321}
```

**`decidio`** se mide con un **contrafactual**: cuando el renglón se enciende, se
vuelve a decidir con él apagado y se comparan los ganadores. Solo se paga cuando
hay algo que comparar; con el renglón a cero la decisión es la de siempre.

---

### Los humos, corridos **dentro** de la imagen

```
== HUMOS DE LA CURIOSIDAD (P5-7C · C0) ==
  (a) APAGADA identica: 200/200 decisiones, mismo `elegido` y misma `d_ahora`;
      0 registros de curiosidad
  (b) ENCENDIDA: 200 registros · el renglon ENTRA en 200 tics (100.0 %) ·
      M maximo 0.11476 · DECIDE en 5 tics
      ignorancia global 0.8902 -> 0.7960 · vistas 470 casillas
  (c) TIEMPO DEL TIC ENTERO: mediana 3.321 ms · maximo 16.870 ms
      desglose: decisor 0.352 · BFS 2.495 · contrafactual 0.330 ms (medianas)
      tics sin decision: 0
  (e) ENTORNO: crudo y efectivo en el diario · la imagen viene APAGADA ·
      k=0.2 balanza=True

TODOS LOS HUMOS DE LA CURIOSIDAD OK (200 decisiones por pasada)
```

**Los cuatro corren en el build y lo tumban si fallan**, junto a los dieciséis
del cuatro y los doce de las formas.

**(b) es el humo que P5-7A me enseñó a escribir.** Allí publiqué un cero que
parecía un resultado y era un interruptor muerto. Aquí el humo **exige** que el
renglón se encienda: si `M > 0` no ocurre en ningún tic, el build se cae.

**El tiempo, con su desglose honesto.** La primera versión del humo midió el
`ms` de la radiografía —0,194 ms— y habría dado una cifra bonita y falsa, porque
ese número **es solo el decisor** y deja fuera justo lo que la curiosidad añade.
Se cambió por `ms_total`, que cuenta preparación, BFS, decisión y contrafactual.
**El BFS es el 75 % del coste**; el renglón en sí es gratis.

*(Las medianas de la imagen —3,321 ms— son más altas que en la máquina —1,904
ms— porque la imagen es `linux/amd64` emulada sobre `arm64`. En el campo correrá
en amd64 nativo, así que la cifra de la imagen es la conservadora.)*

---

### Frenos

Los de siempre, intactos: el vigía del tic, el tope de llamadas y el de gasto.
**La curiosidad no llama a nadie** —no hay consejero en este brazo—, así que los
dos frenos de gasto quedan inertes por construcción.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

| fichero | md5 |
|---|---|
| `cantera/paper5/curiosidad.py` | `f803f47c8ed0a8eaf3855d7e1dc7d457` |
| `paintball/alma/policy_forma.py` | `2d58ff330a1d377113d8b625d6b728ac` |
| `paintball/alma/humo_curiosidad.py` | `7b38d5a64f8562e3d092b4bf72c681eb` |
| `paintball/alma/Dockerfile.forma` | `15538ebfd382fc3b60201422b0901469` |

---

# C1 y C2 · LAS CUARENTA PARTIDAS

Cuatro tandas de cinco semillas por dos brazos, `lento_v0`, `roster_lento_v1`,
la misma semilla en A y en Q, una petición por episodio, cola vacía antes de
cada tanda. **Misma imagen en las cuatro.**

## El titular

**La curiosidad cabe en el juego y no hace daño, pero tampoco hace lo que se le
pidió.** Cuarenta diarios enteros, **cero frenos, cero tics perdidos, cero
disparos del vigía**, y el veto vital **perfecto: cero decisiones con un armado
a tiro en 27.519**. Pero Q ve un **1,086×** de lo que ve A, cuando Q1 pedía
1,30×.

**Y hay un defecto de diseño medido, no supuesto:** la balanza recorta *cuántas*
veces actúa el renglón en peligro —del 5,62 % en seguro al 1,58 % en inseguro—
**pero no corrige hacia dónde apunta cuando actúa**.

## C2 · Lo que ve

| | vista al final (mediana) | min-max | ignorancia por tramo | nuevas/100 tics |
|---|---|---|---|---|
| **A** | **0,2737** | 0,2057 – 0,3537 | 0,779 → 0,739 | 14,5 |
| **Q** | **0,2971** | 0,2378 – 0,4219 | 0,758 → 0,725 | 14,5 |

**Q − A = +0,0234 [−0,0182, +0,0571] · Q/A = 1,086×.** El cero dentro.

**Las casillas nuevas por cien tics son idénticas (14,5).** Q no explora más
deprisa: acaba viendo algo más porque vive algo más, no porque busque.

## C2 · El renglón, sobre 357.982 tics

**Se enciende en el 87,51 % y decide en el 7,69 %.**

| entorno | % de tics | **decide** |
|---|---|---|
| seguro | 51,72 % | 5,62 % |
| **neutro** | 25,42 % | **17,39 %** |
| inseguro | 22,86 % | **1,58 %** |

La balanza se ve trabajar en la última columna: de 5,62 % a 1,58 % al pasar de
seguro a inseguro.

## El veto, y el desglose por entorno

| entorno | decisiones | **armado a tiro** | acerca al armado | daño en 50 tics |
|---|---|---|---|---|
| seguro | 10.404 | **0 = 0,00 %** | 16/731 = 2,19 % | 0,41 % |
| **inseguro** | 1.292 | **0 = 0,00 %** | **163/1.235 = 13,20 %** | 1,01 % |
| neutro | 15.823 | **0 = 0,00 %** | 285/15.714 = 1,81 % | 0,13 % |

**El veto vital es perfecto: cero, en 27.519 decisiones.**

## La referencia de A, sobre las veinte semillas

En A no existen «decisiones de curiosidad», así que el conjunto comparable es la
**vida entera**; se mide también en Q, para separar la geometría del mundo de lo
que hace el renglón.

### «Acerca al armado más cercano»

| | seguro | neutro | **inseguro** |
|---|---|---|---|
| **A**, todos sus tics | 1,80 % | 1,92 % | **2,23 %** |
| **Q**, todos sus tics | 0,75 % | 2,04 % | **2,09 %** |
| **Q, solo curiosidad** | 2,19 % | 1,81 % | **13,20 %** |

**No es geometría.** La tasa base del cuerpo en peligro es del 2,23 %, y Q en
conjunto va por debajo (2,09 %). **Pero cuando el renglón voltea una decisión en
entorno inseguro, acerca al armado seis veces más que la tasa base.**

En la tanda 1 puse un freno a esta lectura por si era el anillo empujando a
todos al centro. **La referencia lo descarta: el efecto es del renglón.**

### El daño en los 50 tics siguientes, con la hipótesis declarada

| | seguro | neutro | **inseguro** |
|---|---|---|---|
| **A**, todos sus tics | 0,82 % | 1,26 % | **6,63 %** |
| **Q**, todos sus tics | 0,59 % | 0,80 % | **8,87 %** |
| **Q, solo curiosidad** | 0,41 % | 0,13 % | **1,01 %** |

Dos cosas a la vez, y las dos hay que decirlas: **Q recibe daño en entorno
inseguro más a menudo que A** (8,87 % contra 6,63 %), **y sus decisiones de
curiosidad van seguidas de daño seis veces menos que su propia tasa base**
(1,01 % contra 8,87 %).

**La hipótesis, declarada como hipótesis:** Q pasa **77.414 tics** en inseguro y
A **110.593**. Si Q entra en «inseguro» menos veces pero en situaciones más
agudas, su tasa por tic sube sin que su conducta sea peor. Y las decisiones de
curiosidad se concentran en los momentos **menos** agudos dentro de inseguro
—los que la balanza deja pasar—, lo que explicaría el 1,01 %. **No lo he
probado.** Probarlo pide una medida que no está en el encargo: el daño por tic
condicionado a la amenaza continua, no al grado.

## C2 · Vida, puesto, tiempo, frenos

| | vida mediana | puesto mediano | tics perdidos | frenos | vigía |
|---|---|---|---|---|---|
| A | 8.999,5 | 12,0 | **0** | **0** | **0** |
| Q | 9.320,5 | 12,0 | **0** | **0** | **0** |

**Q − A: vida +321 [−1.835, +996] · puesto +0,0 [−2,5, +4,0].** Los dos con el
cero dentro.

**Muertes:** A 39 eliminado y 1 `winner`; Q 38 eliminado, 1 `match_over` y
**1 `winner`**.

## Cotejo de las predicciones selladas (mesa, 23-sep-2026)

| | sello | contador | veredicto |
|---|---|---|---|
| **Q1** | Q ve >30 % más arena que A | **1,086×** · +0,0234 [−0,0182, +0,0571] | **FALLA** |
| **Q2** | decide >3 % en seguro y <0,3 % en inseguro | seguro **5,62 %** ✔ · inseguro **1,58 %** ✘ | **FALLA (por el inseguro)** |
| **Q3** | vida y puesto de Q no peores más allá del ruido | vida +321 [−1.835, +996] · puesto +0,0 [−2,5, +4,0] | **CUMPLE** |
| **Q4** | <15 % de las muertes con curiosidad en los 100 tics previos | **3/38 = 7,89 %** | **CUMPLE** |
| **Q5** | <5 ms de mediana y cero tics perdidos | **5,932 ms** ✘ · **0 perdidos** ✔ | **FALLA (por el tiempo)** |
| **Q6** | gasto <4 $ de plataforma | **2,672766 $** | **CUMPLE** |

### Q2 falla por su segunda cláusula, y es lo mismo que enseña el desglose

Decide el 5,62 % en seguro (pedía >3 ✔) pero el **1,58 % en inseguro**, cinco
veces el 0,3 % pedido. **La balanza atenúa, no veta.** El veto absoluto existe
solo para el caso extremo —armado a tiro, cero en 27.519— pero entre «a tiro» y
«seguro» el renglón sigue actuando.

### Q5 falla, y estable

**5,932 ms de mediana** (5,712 · 6,194 · 6,004 · 5,932 en las cuatro tandas), con
máximo 93,545. El humo dentro de la imagen daba 3,321 ms sobre 200 tics de una
escena; el campo, con 357.982 tics y BFS sobre mapas más abiertos, cuesta el
doble. **No perdió ni un tic**, así que el freno no mordió, pero el sello está
incumplido.

## Gasto

| brazo | episodios | mediana | máximo | suma |
|---|---|---|---|---|
| A | 19 | 0,052835 | 0,124174 | 1,289043 |
| Q | 20 | 0,056376 | 0,129274 | 1,383723 |
| | **40** (1 sin facturar) | | | **2,672766 $** |

**Sin consejero: cero gasto de modelo.** La curiosidad no llama a nadie.
**Q sale tan barato como A**, y el total queda por debajo del tope de 4 $ (Q6).

**Un episodio sin facturar: `A/20889290`** (`cost_usd: null`, diario entero).
Quinto caso de la plataforma en este trabajo, y el primero fuera del brazo F de
P5-6C.

## Las figuras

`cantera/paper5/figI/`:

- **`F1_arena_vista.png`** — la arena vista, asiento a asiento, con la mediana
  de cada brazo y el cociente 1,086× anotado.
- **`F2_una_vida_Q.png`** — una vida de Q con la ignorancia global, la amenaza
  graduada y la **densidad** de decisiones de curiosidad, **todo leído del
  diario**, no reconstruido. Se eligió la vida con la **mediana** de decisiones:
  la del máximo tenía 6.207 y las líneas tapaban la figura entera.

**Enseña lo mismo que la figura de P5-7A:** la ignorancia global se congela en
0,78 durante siete mil tics, y en ese tramo la curiosidad apenas decide.

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

| fichero | md5 |
|---|---|
| `cantera/paper5/curiosidad.py` | `f803f47c8ed0a8eaf3855d7e1dc7d457` |
| `paintball/alma/policy_forma.py` | `2d58ff330a1d377113d8b625d6b728ac` |
| `paintball/alma/humo_curiosidad.py` | `7b38d5a64f8562e3d092b4bf72c681eb` |
| `paintball/alma/Dockerfile.forma` | `15538ebfd382fc3b60201422b0901469` |
| `cantera/paper5/lanza_P57C.py` | `656fc145d06321496f4e81ad9e9d5f6d` |
| `cantera/paper5/baja_P57C.py` | `6baac1f41ac88aa214290962ad67c867` |
| `cantera/paper5/analiza_P57C.py` | `c2c67882a31024d23c16670e5e081d8e` |
| `cantera/paper5/fig_P57C.py` | `816488410e253fcff2ed67f07a7d291c` |

Imagen `gemv-anima:curiosidad-c0`
(`sha256:57bd6f366d3129f965091b57f277ae29ec1508f179451cd98839e6267722efe4`).
Políticas `gemv-p57c-A:v1` (`2bc0809a-…`) y `gemv-p57c-Q:v1` (`af1e34c9-…`).
Roster `roster_lento_v1.json` md5 `a2293bd16ee94e6d4c2f4683b57c2a09`.

**PARO AQUÍ.**
