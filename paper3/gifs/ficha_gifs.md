# Ficha de los GIFs — paper tres

Fecha: 2026-09-11 · Guion: `paintball/gif_manada.py` (nuevo; **no se tocó**
`gemelos_gif.py` ni `replay_gif.py`). Lector de diarios: `pareja.lee`.
**No se usó MettaScope.** Nada se ha subido a ningún sitio.

Los dos GIF se pintan **solo desde los dos diarios de la pareja**: de estas
tandas no hay `.replay` guardado en local. Por eso los otros catorce asientos
aparecen únicamente cuando alguno de los dos los ve (`ve_agentes`), la última
posición vista se mantiene hueca 48 tics como mucho, y **nunca se inventa una
posición**. Los muertos dejan de pintarse desde su `survival_ticks` del
`res_ereq`.

---

## 1 · `gif_manada_anillo.gif`

| | |
|---|---|
| partida | **`ereq_292ee72d-e320-474b-a8df-34c73d7c532e`** (serie 66, `runs/manada2`) |
| tics | **1 → 3408** |
| guion | `python3 paintball/gif_manada.py gif1 --out paper3/gifs/gif_manada_anillo.gif --paso 18 --fig 3.7` |
| parámetros | paso **18** tics/fotograma · 12 fps · 190 fotogramas emitidos (168 en fichero tras fusionar idénticos) · **15,24 s** · 370×370 px · dpi 100 |
| tamaño | **288 kB** |
| md5 | `c6430d3c3adca4d68469996791f9cbde` |

**Cotejo**: `pareja_pos` de a10 contra `pos` de a11 — **909/909 tics
coinciden**.

**Dos correcciones al encargo, medidas:**

1. **La partida no da 5667 tics de diario.** `match_ticks` es 5667, pero los
   dos hermanos mueren en **t3408** y **t3388** (`survival_ticks`), y el diario
   acaba ahí: después no hay observación que pintar. El GIF cubre **1-3408**,
   que es la partida entera **desde la pareja**.
2. **No es la partida más larga con los dos diarios completos desde el tic 1.**
   Es la **cuarta**. Las cinco primeras: `ereq_4467998b` (4416),
   `ereq_f9a19099` (3441), `ereq_4b24cc53` (3437), **`ereq_292ee72d` (3408)**,
   `ereq_62651a32` (3377). Se ha hecho con la partida que el encargo nombra;
   si se prefiere la más larga, es un cambio de una línea en el guion.

**Por qué esta partida y no otra** (lo que sí la justifica): es de las cinco
con **los dos diarios íntegros desde el tic 1** —sin truncado, ver
`paintball/cobertura_diarios_acta.md`—, la pareja sobrevive hasta bien entrada
la fase de anillo (puestos 8 y 9 de 16), y el cotejo entre los dos diarios sale
**perfecto**, 909/909.

**Paso 18 y no 24**: el encargo pedía «15-25 s a 12 fps (paso ≈ 24)», pero
el ≈24 salía de los 5667 tics inexistentes. Con los 3408 reales, el paso 24 da
**11,4 s** —fuera del rango—; el paso 18 da **15,24 s**, dentro, con **más**
fotogramas y por debajo del tope de 400 kB.

**Para Zenodo (EN):**
> A full match of the pair in ZERO-SUM (48×48 grid, 16 seats): the two siblings
> in orange, the shrinking ring in blue, and the other fourteen seats as grey
> dots **only while one of the pair can actually see them** — a hollow dot is a
> position remembered for at most two seconds after sight is lost.
> Everything is drawn from the two agents' own logs, so the map is not the
> world's view but theirs: no position is ever invented.

---

## 2 · `gif_el_que_llega.gif`

| | |
|---|---|
| partida | **`ereq_b915417a-df92-…`** (serie 66, `runs/manada2`) |
| tics | **1560 → 1800** |
| guion | `python3 paintball/gif_manada.py gif2 --out paper3/gifs/gif_el_que_llega.gif` |
| parámetros | paso **2** tics/fotograma · 12 fps · 121 fotogramas emitidos (60 en fichero) · **9,74 s** (velocidad real) · recorte `x[14,29] y[11,26]` (caja de los asientos 10, 11 y 12 con 4 casillas de margen) · 440×440 px · dpi 100 |
| tamaño | **109 kB** |
| md5 | `3269db1c4a606110b5b0fd01b195bfb8` |

**Los tres tics de la escena:**

- **Suelta: t1705**, por el asiento 10 (`intencion = {"do":"drop","slot":0}`,
  `RADIOGRAFIA.elegido = "soltar_first_aid"`), en `[19,21]`.
  **Aviso: `social.solto` es `null`** en todo el episodio — el campo no se
  rellenó; el tic de la suelta sale de la `intencion` y de la radiografía, no
  de él.
- **Recogida: ninguna.** `social.cogio` es `null` en los dos diarios, y no hay
  ningún `pickup` del asiento 11 en la casilla `[19,21]`. La venda sigue en el
  suelo al final de la ventana.
- **Cura propia: t1711**, asiento 11, `{"do":"use","slot":0}` sobre la venda
  que **ya llevaba**; el canal completa en **t1760** y la vida pasa de **7 a
  57**. (El mismo asiento lo había intentado en t1617 y un golpe se lo cortó.)

**Para Zenodo (EN):**
> Ten seconds at real speed, the moment one sibling reaches the other. The pair
> is orange with its exact hit points; the attacker (seat 12, spear) is red;
> green crosses are first-aid kits lying on the ground. One sibling drops a kit
> beside the other at tick 1705 — and the wounded one, at 7 hit points, heals
> at tick 1711 with **the kit it was already carrying**. The gift is never
> picked up.

---

## Custodia

| fichero | md5 |
|---|---|
| `paper3/gifs/gif_manada_anillo.gif` | `c6430d3c3adca4d68469996791f9cbde` |
| `paper3/gifs/gif_el_que_llega.gif` | `3269db1c4a606110b5b0fd01b195bfb8` |
| `paintball/gif_manada.py` | `30da497eb5077859e2f6e58cd787781f` |
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` (intacto) |
