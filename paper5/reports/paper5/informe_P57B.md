# P5-7B — La curiosidad y el vínculo con los otros, en seco

En seco, **coste cero**, nada a la plataforma. Motor, decisor y tabla intocados.

---

## El titular

**No morimos por lo que no nos había pasado: morimos a manos de quien mejor
conocíamos.** En 418 muertes de los 434 diarios, **ninguna** vino de un asiento
con conocimiento cero; la mediana del conocimiento del matador es **0,94**.
O4 falla, y falla en la dirección contraria a la sellada.

**El vínculo positivo es raro, como se selló** (O1 cumple en sus tres cláusulas),
**pero además es inerte**: la fila que lo persigue cambia el 0,04 % de las
decisiones. No hay a quién ir.

**Y el vínculo rompe el veto vital.** Es un defecto de diseño, no de
implementación: tal como el encargo la define, `S-VINCULO-EXTRAÑO` **no lleva el
factor `(1 − amenaza)`**, así que no tiene balanza — y cambia decisiones con un
armado a tiro. La curiosidad por los otros, que sí la lleva, no lo hace **ni una
vez**.

---

## La puerta

```
PUERTA (los dos renglones apagados, proxy instalado): 5.555/5.555 = 100,00 %
```

Los dos renglones se instalan **fuera**, con el mismo patrón del piso de P5-3E y
de `curiosidad.py`: se repite el reparto de `A.REPARTO` / `A.APETITIVAS` y se
rehace el `State`. `D.A` pasa a ser un proxy que delega todo en v42.

---

## Lo que el mundo publica, y lo que no

Esto manda sobre lo que B1 puede medir, y va primero:

| | |
|---|---|
| **quién nos pegó** | `damage_taken[].source = "P<slot>"`. **Certeza total.** |
| **quién disparó** | `ve_proyectiles[].shooter` — «el **único autor cierto** de todo el protocolo» (acta del 40, `policy_cortex.py:795-800`). **Solo lo que vuela.** |
| **el cuerpo a cuerpo ajeno** | **no se publica.** Ningún evento de golpe entre terceros: `eventos` son ignición, boom, muertes, regalos y avisos del anillo. |
| quién murió | `death_fireworks.slot` — el **muerto**, no el matador. |

Así que **«pegó a otro a la vista» es cierto para proyectiles y ciego para el
melee**, y el signo negativo está por tanto **subestimado**: un asiento que solo
apalea a otros de cerca nos parece neutro.

**Ninguna etiqueta se usa.** `E3_participantes.json` mapea slot → política y
existe en el repo; **no se abre en ningún punto de este trabajo**.

---

## B1 · La memoria por asiento

Por asiento visto: apariciones, tics a la vista, armas vistas, golpes recibidos
(impactos y daño), disparos a otros, tics a tiro sin pegarnos, y si se acercó o
se alejó.

### (i) El conocimiento, declarado

```
c = 0,50 · min(1, tics_vista / 200)
  + 0,25 · (le he visto un arma)
  + 0,25 · (le he visto CONDUCTA)
```
«Conducta» = me pegó, o disparó a otro, o estuvo a tiro sin pegarme. Los tres
pesos suman 1 y van declarados como `[impl]`: el encargo pide «una fórmula
simple», no una calibrada.

### (ii) El signo, y su reparto

| corpus | asientos vistos | **negativos** | **neutros** | **positivos** | sale de neutro (mediana) |
|---|---|---|---|---|---|
| **lento** (sin cazadores), N=100 | 55 | 14,5 % | **80,0 %** | **5,5 %** | 262 tics (n=11) |
| lento, N=250 | 55 | 14,5 % | 80,0 % | 5,5 % | 328 tics |
| **los 434** (con cazadores), N=100 | 4.261 | **30,9 %** | 63,9 % | 5,3 % | **177 tics** (n=1.540) |
| los 434, N=250 | 4.261 | 30,9 % | 65,7 % | 3,4 % | 197 tics |

**Subir N de 100 a 250 no mueve nada en el lento y casi nada en los 434** (los
positivos bajan del 5,3 % al 3,4 %): quien está a tiro cien tics sin pegar
suele estarlo también doscientos cincuenta.

**Conocimiento mediano: 0,500 en el lento, 0,570 en los 434.**

### Un hallazgo lateral

**392 de los 4.261 asientos nos pegan sin que jamás les hayamos visto un arma en
la mano** — el 9,2 %. En el lento, **ninguno**. Nos golpean desde fuera de
nuestra vista, o con las manos. Es una parte del mundo que la memoria por
asiento no puede anticipar.

---

## B2 · Las dos filas

Las dos son **dolor**, instaladas fuera.

**`R-CURIOSIDAD-OTROS`** (dominio R, reparto (0,1/0,8/0,1) como el terreno):
```
k_o × (1 − conocimiento) × (1 − amenaza) × (1 − g(d))
```
con `g` la caída de `R-LLAMADA` (`:1085`, constantes `:134`/`:135`,
**importadas**). Cero si ese asiento tiene signo negativo o enseña un arma:
**pasa a miedo**, y de eso ya se ocupa `S-7-AGRESOR`.

**`S-VINCULO-EXTRAÑO`** (reparto de `S-COMPANIA`, **importado** de `:437`), con
la forma de la compañía del hermano:
```
S-COMPANIA (appraisal_zs_v42_exp.py:1003-1038): lineal con zona muerta
   M = 0,22 · min(1, (d − 2,0) / 6,0)   si d > 2,0, si no 0
```
**Declarado: la fila que se imita está APAGADA en v42** — `COMPANIA_ON = False`,
línea 314, candado del 62. Se reutiliza su **forma** importando
`COMPANIA_D0`, `COMPANIA_RANGO` y `COMPANIA_TECHO`; **no se enciende la fila**.

---

## B3 · En seco

Cada fila **sola** con sus k, para poder atribuir los cambios, más una conjunta.
Muestreo: se decide cada 50 tics desde el 300 (las constantes del arnés de
P5-2). **Las fracciones son estimaciones de muestra.**

### S-2 · 40 asientos · 2.230 decisiones muestreadas

| configuración | cambian | en seguro | en inseguro | **veto: armado a tiro** | derroche | voz propia |
|---|---|---|---|---|---|---|
| otros k=0,05 | 4 = 0,18 % | 0,29 % | 0,00 % | **0** | 1/4 | 0,15 % |
| **otros k=0,1** | 8 = 0,36 % | **0,71 %** | 0,08 % | **0** | 2/8 | **0,34 %** |
| otros k=0,2 | 31 = 1,39 % | 2,71 % | 0,32 % | **0** | 3/31 | 1,45 % |
| vinc k=0,1 | 1 = 0,04 % | 0,00 % | 0,08 % | **1** ⚠ | 0/1 | 0,05 % |
| vinc k=0,2 | 2 = 0,09 % | 0,00 % | 0,16 % | **2** ⚠ | 0/2 | 0,10 % |
| juntas 0,1/0,1 | 9 = 0,40 % | 0,71 % | 0,16 % | **1** ⚠ | 2/9 | 0,39 % |

### Mundo lento · 6 asientos · 756 decisiones

La curiosidad por los otros cambia **una sola decisión**, la misma con los tres
k (0,13 %); el vínculo, una (0,13 %) **y con un armado a tiro**.

### El veto, y por qué el vínculo lo rompe

**`R-CURIOSIDAD-OTROS`: cero cambios con un armado a tiro, en las seis
configuraciones y los dos mundos.** La balanza `(1 − amenaza)` funciona.

**`S-VINCULO-EXTRAÑO`: 1 y 2 cambios con un armado a tiro.** No es un fallo de
código: **la fórmula que el encargo define para esta fila no lleva el factor de
amenaza**. Sin balanza no hay veto. Se reporta, no se arregla: cambiar la
fórmula sería decidir por la mesa. **Si se quiere veto, hay que meterle
`(1 − amenaza)`, y es una línea.**

---

## Cotejo de las predicciones selladas (mesa, 23-sep-2026)

| | sello | contador | veredicto |
|---|---|---|---|
| **O1** | lento >50 % neutros y <15 % positivos; S-2 >30 % negativos | **80,0 %** · **5,5 %** · **30,9 %** | **CUMPLE (las tres)** |
| **O2** | k_o=0,1 cambia 0,5-3 % en seguro y ninguna con armado a tiro | S-2 **0,71 %**, veto **0** ✔ · lento **0,27 %** ✘ | **CUMPLE en S-2 · FALLA en el lento** |
| **O3** | derroche 2-15 %, y k_o=0,2 más que 0,05 | S-2: **1/4, 2/8, 3/31** (25 %, 25 %, 9,7 %) · lento 0/0/0 | **FALLA** |
| **O4** | >⅓ de las muertes de S-2 por un asiento con conocimiento cero | **0 de 38 en S-2 · 0 de 418 en los 434** | **FALLA** |
| **O5** | el vínculo cambia <1 % | S-2 **0,04 %** · lento 0,13 % | **CUMPLE** |
| **O6** | voz propia >0,3 % | S-2 **0,34 %** ✔ · lento 0,13 % ✘ | **CUMPLE en S-2 · FALLA en el lento** |

### O3 falla, y hay que decir por qué no se puede leer

Las fracciones salen de **cuatro, ocho y treinta y una** decisiones cambiadas.
«25 %» es **un caso de cuatro**. Con esa n, la cláusula de la dirección
(k=0,2 > k=0,05) no es comprobable: sale al revés (9,7 % contra 25 %) porque el
denominador crece más deprisa que el numerador. **El derroche existe —hay 3
casos reales con k=0,2— pero la serie no tiene datos para tasarlo.**

### O4 falla en la dirección contraria, y es el hallazgo

| corpus | muertes | con matador identificado | **conocimiento cero** | **mediana del matador** |
|---|---|---|---|---|
| S-2 (40) | 38 | 21 | **0 = 0,0 %** | **0,88** |
| lento (6) | 6 | 2 | **0 = 0,0 %** | 1,00 |
| los 434 | 418 | 315 | **0 = 0,0 %** | **0,94** |

**Ninguna muerte, en ningún corpus, vino de un desconocido.** El conocimiento se
mide **en el instante del golpe** y descontando lo que ese mismo golpe aporta,
para no premiar al matador por matarnos.

La lectura es incómoda para la idea que motivaba la fila: **la curiosidad por los
otros no habría salvado ninguna de estas vidas**, porque el peligro no venía de
lo desconocido. Venía de los cazadores, que se conocen enseguida y muy bien.

---

## B4 · La figura

`cantera/paper5/figH/B4_P5_C2_a10.png` — trece asientos vistos en una vida de
13.440 tics, con su conocimiento y su signo (color) y los tics en que cada fila
cambió la decisión.

**Lo que enseña: el conocimiento se forma en los primeros dos mil tics y luego se
congela.** Doce mil tics después no se aprende nada nuevo de nadie: las curvas
son escalones tempranos y después líneas planas. Un asiento pasa de 0,78 a 1,00
en el tic 9.500 —un golpe tardío— y nada más se mueve.

Eso explica O2 y O6 en el lento mejor que cualquier tabla: **si a los dos mil
tics ya conoces a todos los que vas a ver, `(1 − conocimiento)` es casi cero el
resto de la partida, y la fila no tiene de qué tirar.**

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

| fichero | |
|---|---|
| `cantera/paper5/otros.py` | nuevo: la memoria, las dos filas, el proxy |
| `cantera/paper5/mide_P57B.py` | B1 y B3 |
| `cantera/paper5/analiza_P57B.py` | el cotejo |
| `cantera/paper5/fig_P57B.py` | B4 |

Datos: `P57B_b1_{s2,lento,434}.json`, `P57B_b3_{s2,lento}.json`,
`P57B_progreso.log`. Figura: `figH/B4_P5_C2_a10.png`.
Corpus de los 434: las **mismas nueve carpetas** que usó E3
(`E3_golpes.py:16`), 434 asientos-partida leídos de uno en uno.

**PARO AQUÍ.**
