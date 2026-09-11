# Acta — LA PAREJA, SEGUNDA TANDA (campo con v30) · P2 FALLA → AUTOPSIA

Fecha: 2026-09-04 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_57_la_pareja_segunda_tanda.md`

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19** (la pareja no se promociona).
- **v30 sin tocar desde el 56**: `appraisal_zs.py eb9f915e…`,
  `decisor_zs.py f4c315a7…` — los del acta del cuidado, intactos.
- **Coste**: imagen `gemv-anima:v9` (v30, custodia del motor dentro del
  build) + tanda `xreq_f3a6cf02-ce14-4017-b730-acd010165a52`, 40 episodios
  privados. **`cost_preview` VOLVIÓ: `estimated_cost_credits = 20,0`** (≤
  tope 30) — en el 55 era `None`; **ya no está vestigial**, declarado.
  Cosecha 40/40 resultados, **80/80 diarios**, 0 fallos.

---

# EL VEREDICTO, PRIMERO

Sellos: **P1 cumple** (0/0), **P3 cumple** (el mecanismo del cuidado llegó
al campo: ≤2 con una en banda **36 %** vs 2 % del 55, sello ≥10 %), **P2
falla** (dones 18 % vs sello ≥50 %), **P4 falla** (top-4 12 % vs 35 %),
**P5 falla** (juntas 8 %). Regla sellada: *"P2 o P3 fallan → autopsia como
en el 55, antes de nada."* P2 falla → **autopsia obligada, ejecutada**
(abajo). No es "EQUIPO" ni "SE CUIDAN Y NO PUNTÚA" (ambas exigen P2). Es:
**el cuidado ya se ACERCA pero el don todavía no PRENDE — y la autopsia dice
por qué, y esta vez la causa es honesta, no un bug.**

---

# LAS ENTREGAS NUEVAS, PARA LOS OJOS (visor hosted, patrón del 38)

**Entrega A** — `ereq_d0bed0cf`: don **t5040** → recoge **t5050** → curada
**t5100** (gemela11):
<https://api.observatory.softmax-research.net/v2/coworlds/replays/static/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/sha256%3Ac96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9/index.html?v=2#replay=https%3A%2F%2Fsoftmax-public.s3.amazonaws.com%2Freplays%2F610355a0-03c1-4ed3-baf7-a7d0ddc4cd34.replay>

**Entrega B** — `ereq_7a799301`: don **t506** → recoge **t537** → curada
**t586** (gemela11):
<https://api.observatory.softmax-research.net/v2/coworlds/replays/static/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/sha256%3Ac96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9/index.html?v=2#replay=https%3A%2F%2Fsoftmax-public.s3.amazonaws.com%2Freplays%2Fe783da2b-07df-4821-ba3e-a81cdce27b04.replay>

---

# VARAS CONTRA SELLOS (pareado v30 / v29 del 55, método idéntico)

**Nota de método** (declarada): la distancia se recalcula con las
**posiciones verdaderas de los dos diarios** (tick a tick, ambas vivas), no
solo cuando una VE a la otra — v30 sabe sin ver. El brazo v29 del 55 se
recomputa con este método (5,4 real / 7,0 en banda; el 55 reportó 3,6/5,1
por "vista", más optimista de la cuenta).

| vara | sello | **v30** | v29 (55, mismo método) | veredicto |
|---|---|---|---|---|
| **P1 V1 honor** | 0 y 0 | 736 ataques · **0 inic** · **0 golpes** · S-VINCULO 0 | 444 · 0 · 0 | **CUMPLE** |
| **P2 V2 dones** | ≥ 50 % | 13 soltares · 17 eps cond · **18 %** con don | 16 % | **FALLA** |
| **P3 V3 distancia** | ≤2 con banda ≥ 10 % | mediana **3,6** · en banda **2,2** · **≤2: 36 %** | 5,4 · 7,0 · 14 % | **CUMPLE** |
| **P4 V4 moneda** | top-4 ≥ 35 % | **12 %** (5/40) · wins 1 · podio 1 | 15 % | **FALLA** |
| **P5 V5 juntas 8** | > 15 % | **8 %** (3/40) | 10 % | FALLA |
| **V6 mecanismo** | — | S-HERIDO **11.335** tics · camino disparó 9 tics/5 eps (don después: 2) | 6.769 · 3/3/1 | — |

**El titular del mecanismo**: la distancia entre hermanas cuando una está en
banda cae de **7,0 a 2,2** — el arreglo C (camino de ayuda) hace lo que el
forense del 56 pedía: **ahora sí se juntan cuando una cae.** Y S-HERIDO se
enciende el **98 %** de esos tics (era 39 % en el 55): el arreglo A (sabe sin
ver) funcionó. El cuidado llegó entero. Lo que no llegó es la puntuación.

# LA AUTOPSIA DEL DON QUE NO PRENDE (`anatomia2.py`)

1.065 tics con la herida en banda y la portadora viva con botiquín (13
episodios):

| sospechosa | medida | veredicto |
|---|---|---|
| ¿ya no se acercan? | distancia en banda **2,2**; a ≤2 el 9 % de estos tics (36 % sobre TODA la banda) | **NO — el camino funciona** |
| ¿la fila calla? | S-HERIDO encendida **98 %**, M mediana 1,08 | **NO — sabe** |
| ¿la herida se cura sola? | lleva su propio botiquín el 18 % de los tics; 12/13 episodios "sigue en banda" (no muere ni se cura: agonía larga) | parcial |
| **¿el soltar GANA?** | candidato presente 422/1.065 tics; **elegido solo 4 veces** | **AQUÍ ESTÁ** |

**La causa, con foto** (`ereq_5fd43f9c t891`): herida a hp 35, su parte
declara **agresor activo en [19,19] pegado a ella** ([19,18]); la portadora
a 4 casillas con botiquín, S-HERIDO alta — y **soltar pierde ante noop por
+0,525**. Es el **ARREGLO B haciendo su trabajo**: soltar la venda no alivia
S-HERIDO porque la casilla no es servible (el cazador está encima de ella),
así que soltar solo cuesta W sin recompensa → pierde, honestamente. **Y ese
es el caso típico**: se entra en banda PRECISAMENTE porque un cazador te
pega; mientras te pega, ninguna casilla junto a ti es servible; el don
honesto espera a que el cazador se despegue, y para entonces la agonía suele
haber acabado (12/13 "sigue en banda" hasta el estrechamiento o la muerte).

**El don prende donde debe** (las dos entregas de arriba): cuando la herida
NO está siendo cazada en el instante del don, la casilla es servible, soltar
gana, ella recoge y se cura. Correcto. Solo que esa ventana es estrecha.

# POR QUÉ LA MONEDA NO SUBE (P4/P5)

A n=40 y con la tabla del 51 delante (R12: 72 % de pares para señal), 12 %
contra 15 % no es una caída real — es ruido. Lo honesto: **v30 no mueve la
moneda**, ni arriba ni abajo, igual que todo el linaje desde el 50. El
cuidado cambió la CONDUCTA (se juntan, se dan) sin cambiar el RESULTADO
(placement) — el precedente exacto de la pila (49/50): mecanismo demostrable,
moneda que empata.

# INCÓGNITAS CON MÉTODO (el sofá)

1. **El don honesto llega tarde por diseño** (arreglo B): mientras la cazan,
   no hay casilla servible; cuando deja de cazarla, ya salió de banda o
   murió. ¿Vale un don que se adelante — soltar en la línea de su HUIDA
   prevista, no junto a ella? Es conducta nueva; decisión de mesa.
2. **La herida lleva su botiquín el 18 % de los tics**: el don sobra ahí. La
   fila no lee el `b<n>` del parte (botiquín a bordo de la hermana). Leerlo
   —callar S-HERIDO si ella puede curarse sola— es del 53, no diseño nuevo.
3. **La agonía larga**: 12/13 episodios de condición "siguen en banda" sin
   morir ni curarse — la banda no es una emergencia breve sino un estado
   crónico bajo el anillo. ¿El don importa si nadie muere de eso? La moneda
   dice que no (P4/P5). Material de sofá.
4. **La distancia 3,6 de fondo** (fuera de banda) sigue > 2,2 de las v19: el
   camino solo tira EN banda; fuera, nada junta (el forense del 56). Si se
   quiere cercanía de fondo, es otra fila (S-SOLEDAD con la hermana), no
   esta. Declarado.

# QUÉ QUEDA EN EL REPO

- `runs/pareja2/` — episodios.json (con `cost_preview` 20,0), 40 res_, 80
  diarios, resumen.json.
- `runs/xp_pareja2_v30.json` — el cuerpo de la tanda.
- `pareja2.py` (V1-V6 pareado v30/v29) · `anatomia2.py` (la autopsia).
- `gemv-anima:v9` subida (imagen v30). Liga v19; v30 de taller intacta.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

El 55 dejó tres piedras; el 56 las quitó en el banco; el 57 fue a ver si el
campo lo notaba, y la respuesta es la más limpia posible: **el cuidado se
nota entero, la moneda no lo nota nada.**

Lo primero es un triunfo de ingeniería que hay que decir con todas las
letras. Las hermanas que en el 55 vivían a siete casillas cuando una caía
ahora viven a dos; la fila del cuidado que se apagaba tres de cada cuatro
veces por no verla ahora se enciende noventa y ocho de cada cien, porque el
parte le dice dónde está aunque no la vea. Los tres arreglos del 56
funcionaron en el mundo real, no solo en el banco. Se juntan. Se buscan. Se
dan el botiquín, y hay dos replays nuevos donde el gesto se completa entero.

Y aun así el don prende dieciocho veces de cada cien donde debería prender
cincuenta, y la autopsia esta vez no encuentra un culpable sino una verdad
incómoda: **el don honesto llega tarde por diseño, y el diseño tiene razón.**
Se entra en banda porque un cazador te está pegando; mientras te pega,
soltar la venda a tu lado es soltarla a los pies de tu cazador, y el arreglo
B —que escribimos nosotros, en el 56, para no mentir— dice correctamente que
eso no es ayuda. El don espera a que el cazador se aparte. Pero para entonces
la agonía ya se resolvió: doce de cada trece heridas no mueren ni se curan,
simplemente arrastran la banda hasta el anillo. La emergencia que el don
querría atender casi nunca es una emergencia.

Así que la moneda no se mueve, y por una vez eso no es una decepción sino una
coherencia: es exactamente lo que dijo la pila en el 50. Podemos cambiar lo
que el animal HACE —y lo hemos cambiado, se cuidan de verdad— sin cambiar
dónde QUEDA. Para que el cuidado puntúe haría falta que la vida del hermano
decidiera partidas, y en este mundo, bajo este anillo, la banda es crónica y
la muerte viene del cerco, no de la herida que un botiquín arregla. El don
es bueno. El mundo, para el don, es indiferente. Las dos cosas son ciertas y
las dos están medidas.

---

## Reproducción

```bash
cd gemv-coworld
python3 paintball/pareja2.py        # V1-V6 pareado v30/v29
python3 paintball/anatomia2.py      # la autopsia del don que no prende
# tanda: xreq_f3a6cf02…, cuerpo en runs/xp_pareja2_v30.json (cost_preview 20 cr)
```
