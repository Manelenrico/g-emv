# Addendum — recuento por EVENTOS de las ocho vendas (tanda 66)

Fecha: **2026-09-10** · **Solo lectura**: no se ejecutó ninguna partida ni se
tocó código. Todo sale de los diarios ya grabados de `runs/manada2/`.

`md5 motor/model.py` = `1e511978c251130e95169ebf8443efa1` (sin tocar).

**Este documento NO sustituye a `forense_dones_venda.md`**, que queda como
está, sin editar, igual en el proyecto vivo y en esta cantera. Lo que hace es
**añadir una comprobación que aquel no hizo** y corregir la lectura de una de
sus frases. El número principal de aquel forense **se confirma**.

---

## 1 · Qué se recontó, y con qué criterio

El forense original contaba una recogida cuando el hermano emitía
`intencion.do == "pickup"` **en la casilla exacta del don** y su mochila ganaba
una venda en el tic siguiente. Es un criterio **por evento**, no por salto de
vida. Se ha vuelto a hacer desde cero, con el mismo criterio, y **da el mismo
resultado**.

Lo que el original **no** comprobó, y este addendum sí: **qué pasó después de
la recogida** — si el canal de la venda llegó a completarse.

## 2 · Las ocho líneas

| # | partida | soltar (tic · vendas) | posición | ¿pickup de ESA venda? | ¿usa venda después? |
|---|---|---|---|---|---|
| 1 | `ereq_18dfbd78` | t376 · 2 | `[24,22]` | **NO** — cero pickups de venda tras el don | **nunca** |
| 2 | `ereq_3f9b199e` | t1134 · 1 | `[22,22]` | **SÍ** · t1145 · pos `[22,22]` · mochila **0 → 1** | `use` t1146 slot 0 · antes `[first_aidx1, -]` · hp 15 · **canal NO completa** |
| 3 | `ereq_62651a32` | t2277 · 1 | `[24,20]` | **NO** | **nunca** |
| 4 | `ereq_736990b4` | t2326 · 1 | `[23,19]` | **NO** | **nunca** |
| 5 | `ereq_9fab619d` | t2333 · 1 | `[23,21]` | **SÍ** · t2410 · pos `[23,21]` · mochila **0 → 1** | `use` t2411 slot 0 · antes `[first_aidx1, -]` · hp 7 · **canal NO completa** |
| 6 | `ereq_a62f7c2d` | t627 · 1 | `[22,21]` | **SÍ** · t2433 · pos `[22,21]` · mochila **0 → 1** | `use` t2448 slot 0 · antes `[first_aidx1, netx1]` · hp 23 · **canal NO completa** |
| 7 | `ereq_b915417a` | t1705 · 1 | `[19,21]` | **NO** — cero pickups | `use` t1711 slot 0 · antes `[first_aidx1, -]` — **la SUYA**, que ya llevaba en t1705 · hp 7 → **completa en t1760: `[-, -]`, hp 57** |
| 8 | `ereq_9869b665` | t461 · 2 | `[23,20]` | **NO** | **nunca** |

**Recogidas: 3 de 8.** El número del forense original **se confirma**, y se
confirma por el mismo camino: eventos de `pickup`, no saltos de vida.

## 3 · El hecho nuevo: **0 de 3 curas completadas**

Los tres hermanos que recogieron la venda emitieron `use` casi de inmediato.
**Ninguno completó el canal de 48 tics.** Los tres murieron con la venda del
hermano en la mochila, sin gastarla.

| caso | recoge | emite `use` | canal abre | qué lo impide | muere |
|---|---|---|---|---|---|
| **2 · `ereq_3f9b199e`** (a11) | t1145, hp 15 | t1146 | t1147 | **t1172: golpe de P14, 13,2 → hp 15 → 2. Canal cortado** a los 25 tics de 48. Vuelve a abrir canal (visible en t1196) | **t1212**, puesto 13 |
| **5 · `ereq_9fab619d`** (a11) | t2410, hp 7 | t2411 | t2412 | **muere con el canal abierto**: habría completado en t2459 y el episodio se le acaba antes. **24 tics de 48** | **t2436**, puesto 16 |
| **6 · `ereq_a62f7c2d`** (a10) | t2433, hp 23 | t2448 | t2449 | **t2477: golpe de P2, 13,2 → hp 23 → 10. Canal cortado** a los 28 tics de 48. Vuelve a abrir canal (visible en t2498) | **t2537**, puesto 13 |

Dos cortados por un golpe —la venda se cancela con **cualquier** daño
(`sim.nim:867-869`)— y uno por falta de tiempo.

**La única cura completada en las ocho escenas es la del caso 7, y es con la
venda PROPIA, no con el don.** El don de ese caso siguió en `[19,21]` sin que
nadie lo recogiera. Detalle completo de esa escena en
`forense_el_que_llega`/`ereq_b915417a` (10-sep-2026, fuera de esta cantera).

## 4 · Qué frase del original queda corregida en su lectura

`forense_dones_venda.md`, §2.6 y su lectura en llano, dice:

> *"Ocho vendas salieron del zurrón, **tres llegaron a la hermana** — y en los
> tres, la recogió estando peor que cuando se la dieron: 15, 7 y 23 de vida."*

**El dato es correcto; la lectura se queda corta.** Las tres recogidas
existieron y las tres cifras de vida (15, 7, 23) son las del tic del `pickup`.
Lo que la frase deja entender —que la venda sirvió— **no ocurrió en ningún
caso**.

**Redacción corregida, para el paper:**

> De ocho vendas dadas, **tres se recogieron y ninguna llegó a curar a nadie**.
> Los tres hermanos que la recogieron emitieron la cura y murieron con el canal
> sin completar: dos cortados por un golpe y uno por falta de tiempo.

En una frase: **llegaron a la mano, no llegaron a la vida.**

## 5 · Una aclaración de identidad, para que no se crucen dos escenas

Hay **dos** episodios distintos en los que el que recibe está a **7 de vida**, y
es fácil confundirlos:

- **`ereq_9fab619d`** — el hermano **SÍ recoge** el don (t2410, a hp 7) y muere
  con el canal abierto. Es el "7" de la lista de tres recogidas.
- **`ereq_b915417a`** — el hermano está a hp 7 con **una venda propia sin usar**
  y **NO recoge** el don. Se cura con la suya (t1711 → t1760, hp 7 → 57). Ya
  figuraba como no recogida en el forense original.

**No hay contradicción entre los dos documentos**: son dos escenas con la misma
cifra de vida.

## 6 · Lo que sigue sin poder afirmarse

- **Quién se llevó las cinco vendas no recogidas.** Solo se sabe hasta cuándo se
  vieron en el suelo desde nuestros dos diarios.
- **Por qué el canal del caso 6 tarda 15 tics en abrirse** tras la recogida
  (pickup t2433, `use` t2448): no se ha desglosado qué eligió el decisor en esos
  quince tics.
- **Nada sobre las 90 raciones**: este recuento es solo de vendas.

---

## Rutas de las fuentes

| ruta | qué aporta |
|---|---|
| `paintball/runs/manada2/ereq_*/a1{0,1}/*.log` | **el recuento**: eventos `pickup` con posición y mochila antes/después, acciones `use` con `slot`, efecto `channeling` tic a tic, `damage_taken` con fuente y cantidad, y el registro `final` de cada hermano |
| `~/paintball_recon/docs/zero-sum/src/sim.nim` (867-869) | cualquier daño cancela el canal de la venda (y el kit no se pierde) |
| `hechos/forense_dones_venda.md` (esta cantera) | el forense original, **sin editar**: las ocho escenas, filas, márgenes y vetos |
| `hechos/forense_dos_vendas.md` (esta cantera) | el octavo don en detalle (`ereq_9869b665`) |
