# Acta — EL PRIMER MINUTO Y LA VOZ (cierre de la ànima sola)

Fecha: 2026-09-04 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_52_el_primer_minuto_y_la_voz.md`

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Solo lectura (replays pagados + diarios + fuentes). Liga en
  **v19**. **Coste 0.**

---

# A · ¿LA v27 EVITA EL CONTACTO TEMPRANO? (H1 del 51, 80 pares del 49+50)

Instrumento del 51 (replay, sin recorte de cabeza); 80/80 pares con pista.

| tics 1-1000, pareado | v19 | v27 | pareado | p |
|---|---|---|---|---|
| **pegado (≤1)** | 4,6 % | 8,1 % | v27 menos en **32**, más en 38, igual 10 | **0,55** |
| contacto (≤3) | 22,0 % | 26,1 % | 37-43-0 | 0,58 |

## La predicción sellada — **CONFIRMADA**

> *"La v27 NO reduce el pegado de forma apreciable — el muro es reactivo
> (necesita `era_agresor`, es decir, que ya te hayan pegado); antes del
> primer golpe, v27 y v19 son el mismo animal por construcción."*

Exactamente eso: 32-38-10, p=0,55. **El miedo actual llega tarde por diseño.**

## Causa-o-sorteo: ¿nace ya pegado? — **NO**

| | |
|---|---|
| corr(dist al enemigo más cercano en el tic ≤50, % pegado en 1-1000) | **+0,114** (n=160) |
| nace con enemigo a ≤5 → pegado mediano | 4,6 % (n=76) |
| nace a >5 → pegado mediano | 8,1 % (n=84) |

**El spawn no predice el contacto temprano** — la correlación es débil y va
al revés de la cuna (los pedestales son un anillo simétrico; todos nacen
parecido). El pegado de los primeros mil tics **se fabrica andando**, no
naciendo: es dinámica de la apertura (quién va hacia dónde, quién caza),
no lotería de cuna. Eso deja la H1 del 51 más interesante y más difícil a la
vez: hay conducta implicada, pero la palanca que tenemos (el miedo) es
reactiva por diseño.

## LA LECTURA SELLADA, APLICADA — **EL TOPE, ESCRITO**

> Rama primera del sello: *"Si NO reduce: el miedo actual llega tarde por
> diseño; la única palanca sería un 'distancia con extraños' preventivo —
> indemostrable en puestos a n=40 (hay que ganar el 72 %). **TOPE ESCRITO**
> con el hallazgo del primer minuto."*

**TOPE DE LA ÀNIMA SOLA — escrito y con sus números:**

1. La moneda del mundo empata exacto (50: 17-17-6, p=1,0) tras cuatro
   retadores banked pieza a pieza.
2. Lo que separa buenas de malas es el contacto del primer minuto (51:
   0,0 % vs 20,3 % pegado), y **ese contacto no viene de la cuna** (arriba)
   **ni lo reduce el miedo que tenemos** (arriba) — el muro despierta con el
   primer golpe, que es tarde.
3. La palanca restante (miedo preventivo a extraños) costaría un rediseño de
   fila y su efecto en puestos sería **indemostrable con nuestro presupuesto**
   (72 % de pares a n=40; la tabla del 51 queda de guardia).

**Aquí termina la temporada de la ànima sola.** La v19 queda campeona; la
v27 queda en el taller como conocimiento; y la temporada dos —lo social—
tiene su baseline (la pareja son dos boletos: 21 % ≈ 2×13 %) y su primera
piedra certificada abajo.

---

# B · QUÉ PUEDE LLEVAR LA VOZ (la primera piedra de la temporada dos)

Certificado con la espec, el fósil del simulador y **el cable real medido**
(17.601 mensajes de team, 10.616 totales analizados):

| pregunta | respuesta certificada | fuente |
|---|---|---|
| formato | `{"type":"talk","channel":"broadcast\|team\|dm","to":9,"text":…}` | espec :114 |
| tamaño máximo | **120 chars, ASCII imprimible (0x20-0x7E)**; lo demás se filtra | espec :114 + fósil `sanitizeTalk` (573-579) · campo: máx visto 74, 0 no-ASCII |
| frecuencia | **1 por 24 tics**; pasarse → `rate_limited` | espec :99 + fósil 587-589 |
| ¿consume acción? | **NO** — canal separado del `action`; no pasa por ningún enfriamiento. *(Curiosidad declarada: pasarse del límite PISA `lastActionResult` con `rate_limited`)* | espec :99 + fósil `submitTalk` |
| latencia | **+2 tics medidos** (envío→obs), uniforme en los tres canales (886+171+9559 mensajes, todos a +2) | cable real |
| ¿quién recibe `team`? | **el compañero de asiento (seat^1) y el propio eco. NADIE MÁS: 0 terceros en 17.601.** El gemelo lo recibe (5.342 de compañero en gemelos/ocasion/pila/vara); el aliado de relleno y el campeón-pareja también | cable real |
| ¿puede un extraño hablar por `team`? | **NO** — canal cerrado por equipo, por construcción del mundo. **La confianza del canal es del mundo, no del protocolo social**: lo que llegue por team ES del hermano | cable real (0 fugas) |
| receptor en obs | `chat: [{tick, from, channel, to, text}]` — `from` es slot entero, texto crudo; **parseable con certeza** | espec :70 + 32 |
| el latido del 32 | cada **48 tics exactos** (7.070 latidos, gaps = {48}), canal team, `"P<slot> x,y banda"` (≤74 chars), sin consumir acción | policy.py:262-267 + cable |

## El hallazgo de fuentes, declarado

**El fósil de `sim.nim` no conoce el canal `team`**: su enum es
`{broadcast, dm}` (98-99) y el parser **descarta** cualquier otro canal
(1456: `elif chStr != $tcBroadcast: return`). Pero el cable real lo entrega
—17.601 mensajes— y cerrado por equipo. **El fósil es anterior al mundo
desplegado**; para la voz, la fuente de verdad es el cable, y así queda
certificado (por eso la latencia se midió en vez de fiarse del "next-tick"
del fósil: el cable dice **+2**).

No hay acta parcial: todo lo que la temporada dos necesita del canal es
cierto y está medido.

---

# LECTURA FRÍA

El primer minuto era la última puerta de la ànima sola, y se cerró con las
dos respuestas limpias que un cierre necesita. La v27 no evita el contacto
temprano — no porque el muro falle, sino porque el muro es un reflejo: se
enciende con el primer golpe, y el primer minuto se decide antes. Y ese
contacto no es cuna: los pedestales reparten igual, y el pegado se fabrica
andando en los mil tics siguientes. La única palanca que quedaría es un
miedo preventivo a extraños — otra fila, otro sofá — cuyo efecto en puestos
no podríamos demostrar ni aunque funcionara: setenta y dos por ciento de
pares a nuestro presupuesto. La regla de la mesa era una estrategia más y el
tope: **el tope queda escrito, con sus tres números debajo.**

La temporada de la ànima sola termina como debía: con la campeona invicta en
su moneda, cuatro retadores honestos en el taller, y un animal que en
cincuenta y dos encargos jamás pegó primero.

Y la temporada dos ya tiene su primera piedra puesta, que es mejor de lo que
esperaba: **el canal de equipo es cerrado por construcción del mundo** — cero
fugas en diecisiete mil mensajes. Lo que llegue por team ES del hermano, sin
firma ni protocolo: la confianza viene de fábrica. Ciento veinte caracteres
ASCII, uno cada veinticuatro tics, dos tics de latencia, gratis de acción. El
latido del 32 ya usa ese canal para decir dónde está la gente; lo que la
temporada dos tiene que decidir es qué más vale la pena decir — y qué hace
el que escucha.

---

## Reproducción

```bash
cd gemv-coworld
# A: contacto pareado + causa-o-sorteo (pistas en runs/_replays51, plan _plan52)
# B: espec :99/:114/:70 · fosil sim.nim 98-99, 573-589, 1343-1359, 1452-1457
#    · cable real: los conteos de este acta salen de los diarios de
#    pila/vara/gemelos80/ocasion (scripts inline en el acta del commit)
```
