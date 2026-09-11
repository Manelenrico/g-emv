# Ficha de las figuras — paper tres

Fecha: 2026-09-11 · Guion: `paintball/figuras_paper3.py` (nuevo), que **reutiliza
la misma herramienta y los mismos datos que los GIF**: importa `diarios`,
`survival`, `vistos` y `OLVIDO` de `paintball/gif_manada.py`, que a su vez lee
los diarios con `pareja.lee`. **No se usó MettaScope.** No se tocó la cantera,
el motor, `gif_manada.py` ni los dos GIF, que siguen como material
suplementario aparte.

**Formato**: PNG a **300 ppp**, fondo blanco, ancho **5,90 in** — el ancho de
columna del PDF del paper dos (`G-EMV_the_Hive_EN.pdf`, A4 a una columna: caja
de texto de 424,8 pt).

**Legibilidad en gris**: los papeles se separan por **forma** además de por
color, y todo lleva borde negro — círculo grande naranja = la pareja ·
triángulo rojo = el agresor · círculo pequeño gris = los demás · cruz verde =
la venda. Relleno hueco = posición **recordada**, no vista ahora (misma regla
de olvido que los GIF: 48 tics como máximo).

---

## `fig2_arena.png` — figura 2 del paper (para §3.1)

| | |
|---|---|
| partida | **`ereq_292ee72d-e320-474b-a8df-34c73d7c532e`** (serie 66, `runs/manada2`) |
| **tic** | **3029** |
| guion | `python3 paintball/figuras_paper3.py fig1 --out paper3/figuras/fig2_arena.png` |
| parámetros | rejilla entera 0-48, línea cada 4 · anillo de `zona` del diario · 5,90 × 5,90 in a 300 ppp = 1770 × 1770 px |
| tamaño | 41 kB |
| md5 | `75d0b626ba768c151a668ede26f16008` |

**Por qué este tic.** En t3029 se cumplen las dos condiciones del encargo y la
tercera que hace útil la figura:

- **el anillo ya está visiblemente cerrado**: radio **15** sobre 24 iniciales
  (el mundo lo bajó de 24→19 en t2064 y de 19→15 en t2976);
- **quedan 9 jugadores vivos**, dentro del 8-12 pedido;
- es el tic con **más asientos a la vista a la vez** de todos los que cumplen
  lo anterior: **6 vistos en ese instante** más uno recordado, más los dos
  hermanos — **9 puntos para 9 vivos**, es decir, la figura enseña a todos los
  que quedan.

En términos de la partida completa (`match_ticks` 5667) t3029 es el **53 %**:
media partida. En términos de la pareja, que muere en t3408 y t3388, es el
89 % de su vida.

**Lo que la figura declara sin decirlo**: los catorce asientos ajenos se pintan
solo porque **la pareja los ve**. El punto hueco (asiento 1) es una posición
recordada de hace menos de 48 tics. No hay ninguna posición inventada.

---

## `fig3_el_que_llega.png` — figura 3 del paper (para §4.2)

| | |
|---|---|
| partida | **`ereq_b915417a-df92-…`** (serie 66, `runs/manada2`) |
| **tics** | **1704 · 1706 · 1760** |
| guion | `python3 paintball/figuras_paper3.py fig2 --out paper3/figuras/fig3_el_que_llega.png` |
| parámetros | tres paneles en fila, **misma escala y mismo recorte**: `x[16,25] y[15,24]` (caja de los asientos 10, 11, 12 y la casilla de la venda en los tres tics, con 3 de margen) · 5,90 × 2,39 in a 300 ppp = 1770 × 716 px · el tic va debajo de cada panel |
| tamaño | 27 kB |
| md5 | `9d7c2ab9ee80d3e82b73f138eb70e7af` |

**Los tres tics, uno a uno:**

- **(a) t1704** — el primero ya ha llegado: el asiento **10 está a una casilla**
  del **11**, que lleva **7 de vida**. (Llegó a distancia 1 en **t1694** y ahí
  sigue.) El agresor **12**, con lanza, está pegado a los dos.
- **(b) t1706** — **el primer tic en que la venda está en el suelo**. El 10 la
  soltó en **t1705** en `[19,21]`, que es **su propia casilla**: por eso la cruz
  verde se dibuja *encima* del punto naranja. Está a **2 casillas** del 11.
- **(c) t1760** — **el tic exacto en que la cura entra**: el 11 pasa de **7 a
  57**. La venda del suelo sigue en `[19,21]`, a **3 casillas** de él.

**Dos precisiones sobre (c)**, medidas y no interpretadas:

1. La distancia **3** es geométrica: Chebyshev del 11, en `[22,19]`, a la
   venda en `[19,21]`.
2. **En t1760 ningún diario está viendo la venda**: el 11 dejó de verla en
   **t1743** y el 10 vuelve a verla más tarde. Por eso se dibuja **hueca**, como
   posición recordada — 17 tics de antigüedad, dentro de la ventana de olvido de
   48 que usan los GIF. Los únicos tics con el 11 a 57 **y** la venda vista de
   verdad son t1815-1817, y ahí la distancia ya es **5**, no 3. Se ha preferido
   el tic de la cura con la marca hueca antes que mover la escena 55 tics para
   que cuadrase la visibilidad.

Y lo que la figura muestra sin necesidad de pie: el 11 se cura **con la venda
que ya llevaba** (`use slot 0` en t1711), no con la del suelo — que sigue ahí,
sin recoger, en el tercer panel.

---

## `fig1_visor_2x2.png` — cuadrícula del visor (§3.1, a página completa)

| | |
|---|---|
| partida | **`ereq_292ee72d-e320-474b-a8df-34c73d7c532e`** (serie 66, `runs/manada2`) |
| **tiempos** | **0:00 · 1:11 · 2:06 · 3:54** (de 3:56 de partida) |
| **tic** | **1 · 1704 · 3024 · 5616** |
| guion | `python3 paintball/tira_visor.py --rejilla --out paper3/figuras/fig1_visor_2x2.png` |
| parámetros | **2 × 2** — 0:00 arriba izq · 1:11 arriba der · 2:06 abajo izq · 3:54 abajo der · 5,90 in a 300 ppp = **1770 × 1878 px** · paneles cuadrados iguales con margen fino · el tiempo debajo de cada panel |
| tamaño | 3517 kB |
| md5 | `cdfcd19575a3e33fd7a7f31395780d89` |

**La tira en fila queda DESCARTADA.** `fig1_visor_tira.png` (mismos recortes,
mismas marcas, montaje 1×4) **no se ha borrado**: sigue en la carpeta por si
hiciera falta una versión de una columna, pero **no es la figura del paper**.
La del paper es esta 2×2. Si prefieres la carpeta limpia, se borra en un
comando.

**Los círculos, a este tamaño.** Comprobado: con los paneles a 870 px de lado
se ven a simple vista. El trazo pasó de **1,1 a 2,4 pt** — se engordó el
**trazo**, no el radio, que sigue siendo `1,15 × px_por_casilla` como en la
tira. Nada más cambió: mismos recortes, misma calibración y **las mismas seis
posiciones** (t1 `[13,13]`/`[18,9]` · t1704 `[30,17]`/`[27,22]` · t3024
`[29,20]`/`[25,21]`).

**Qué es, y qué NO es.** Es una **captura de pantalla del visor de la
plataforma** (Softmax/MettaScope), hecha por Manel. **De ella no se lee ningún
dato de este trabajo**: todas las cifras del paper salen de los diarios y de los
`res_*.json`, nunca de una imagen. La tira está aquí para enseñar el mundo y el
cierre del anillo, no para medir.

**Correspondencia tiempo → tic.** A 24 tics/s: 0:00 → **1** (primer tic con
diario), 1:11 → **1704**, 2:06 → **3024**, 3:54 → **5616**. Los dos intermedios
quedan confirmados por el propio visor, que dibuja nuestros partes: en 1:11 se
lee `MANEL EN E1 P10 T1681 30 17 H78`, y el diario de a10 da `[30,17] hp 78`;
en 2:06 se lee `MANEL E2 E1 P11 T3025 25 21 H48`, y el diario de a11 da
`[25,21] hp 48`. (El `T` del parte es el tic en que se emitió, unos tics antes
del de la captura.)

**Recorte aplicado.** De cada captura se toma el panel de juego —fuera el borde
negro, el marcador y la lista de bajas del top-izquierda, la línea de monedas
del pie y la barra de reproducción— y de ahí el cuadrado centrado:

| captura | original | recorte (x0,x1,y0,y1) | cuadrado |
|---|---|---|---|
| `visor_0m00.png` | 2958 × 2576 | 198, 2774, 60, 2440 | 2380² |
| `visor_1m11.png` | 3310 × 2576 | 915, 3202, 380, 2340 | 1960² |
| `visor_2m06.png` | 3222 × 2560 | 876, 3163, 380, 2330 | 1950² |
| `visor_3m54.png` | 3478 × 2570 | 726, 3302, 380, 2440 | 2060² |

**Límite declarado**: las cuatro capturas se tomaron con **zoom distinto**, así
que los paneles comparten formato y tamaño pero **no la misma escala del
mundo**. Se recortan al panel de juego, no a una ventana idéntica del mapa.

**Las marcas.** Círculo fino naranja sobre **MANEL EN (asiento 10)** y
**MANEL E2 (asiento 11)** en los tres paneles donde están vivos. En **3:54 no
hay marca**: habían caído en **t3408** y **t3388** (`survival_ticks`), o sea en
2:22 y 2:21.

No se ponen a ojo. La **fortaleza** central sirve de patrón: su muro va de la
casilla 20 a la 28 —nueve de lado, interior 7×7 = 49 celdas, como declara
`mundo_leido.camara_celdas`— y está centrada en (24,24); de su caja en píxeles
salen el centro y los píxeles por casilla, y la posición de cada hermano sale de
**su diario** en ese tic: t1 `[13,13]` y `[18,9]` · t1704 `[30,17]` y `[27,22]`
· t3024 `[29,20]` y `[25,21]`.

**Capturas originales (no modificadas):**

| fichero | md5 |
|---|---|
| `figuras/visor/visor_0m00.png` | `4c6818eedfb47a60e02b3cef6d43a369` |
| `figuras/visor/visor_1m11.png` | `a1be7b6c561922aab516b5cd25349017` |
| `figuras/visor/visor_2m06.png` | `d9a4f0ef8a922e0ee450da25c025b986` |
| `figuras/visor/visor_3m54.png` | `babcddf66072be36ece88f53ca891b23` |

---

## Custodia

| fichero | md5 |
|---|---|
| `figuras/fig2_arena.png` | `75d0b626ba768c151a668ede26f16008` |
| `figuras/fig3_el_que_llega.png` | `9d7c2ab9ee80d3e82b73f138eb70e7af` |
| `figuras/fig1_visor_2x2.png` | `cdfcd19575a3e33fd7a7f31395780d89` |
| `figuras/fig1_visor_2x2.jpg` (ligera para el PDF, 790 kB, 200 ppp) | `437efeb0f7c6bcdc7688e79eadfce1d5` |
| `fig1_visor_tira.png` *(descartada, NO incluida aquí)* | `99409a71adc2a8bcae5402f1aa0fb370` |
| `paintball/tira_visor.py` *(repo privado)* | `c95badc9b56747a7be11b2c9fc84829e` |
| `paintball/figuras_paper3.py` *(repo privado)* | `d3426a5ed269676db1042809ff0324d8` |
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` (intacto) |

---

## Nota de actualización — 2026-09-12

Esta ficha se escribió el 11-sep-2026 para los ficheros tal como se llamaban
entonces en el repositorio de trabajo. Al montar `paper3/` para publicación, **dos
figuras se renombraron y se regeneraron**, así que sus md5 cambiaron. Se han
corregido aquí contra el fichero real de esta carpeta; **ninguna imagen se ha
vuelto a generar para hacer este cotejo**.

| antes | ahora | md5 de la ficha (viejo) | md5 real (corregido) |
|---|---|---|---|
| `fig1_arena.png` | **`fig2_arena.png`** | `f3af8a9f05ac0c2f50c4d54dbd598e8d` | `75d0b626ba768c151a668ede26f16008` |
| `fig2_el_que_llega.png` | **`fig3_el_que_llega.png`** | `8d506b7c83daad7aee99297fc1afdeb1` | `9d7c2ab9ee80d3e82b73f138eb70e7af` |

Las dos conservan tamaño (1770×1770 y 1770×716 px) y resolución (300 ppp); solo
cambian los bytes, por haberse vuelto a dibujar con el nombre nuevo.

**Sin cambios**: `fig1_visor_2x2.png` y las cuatro capturas de `visor/` coinciden
con lo que decía la ficha. **Añadido**: la fila de `fig1_visor_2x2.jpg`, que no
estaba. **Declarado**: `fig1_visor_tira.png` (descartada) y los dos guiones de
`paintball/` no están en esta carpeta; viven en el repositorio privado de trabajo.
