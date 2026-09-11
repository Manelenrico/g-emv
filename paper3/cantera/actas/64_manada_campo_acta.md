# Acta — LA MANADA EN EL CAMPO (v34) · P1 CUMPLIDO · P2 falla literal → AUTOPSIA

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_64_la_manada_en_el_campo.md`

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **v34 sin tocar desde el 63**: `appraisal_zs.py 11b7cea0…`, `decisor_zs.py
  136eb577…` — verificados antes del build.
- **Coste**: imagen `gemv-anima:v11` + tanda `xreq_7066af5f-…`, 40 episodios
  privados, **`cost_preview` = 20 cr** (≤ tope 30). Cosecha **40/40
  resultados, 80/80 diarios**, 0 fallos.

---

# EL VEREDICTO, PRIMERO

**P1 (gate absoluto) CUMPLIDO**: **0 iniciaciones-estrictas** y **0 ataques
elegidos contra la hermana** en 40 episodios. La promesa de la casa aguanta
con el honor partido en dos: el animal jamás pegó a quien no había agredido a
ninguna de las dos.

**P2 falla en su forma literal** (5/20 = 25 % < 50 %) → **autopsia obligada,
ejecutada**. Y la autopsia da una respuesta limpia: **de las 20 ventanas de
ocasión, en 12 el golpe era FÍSICAMENTE IMPOSIBLE** (el cazador no alineado o
fuera del alcance del arma). **Donde el golpe era posible, la defensa llegó el
62 % de las veces (5/8).** La definición sellada de "ocasión" no exigía que el
cazador estuviera al alcance; con esa condición añadida, P2 se cumpliría. **La
mesa decide si resella** — el banco no se auto-otorga el hito.

**P4 (V8) sin degradación.** P3 no discrimina con el instrumento usado
(declarado abajo).

---

# LAS ESCENAS, PARA LOS OJOS

**La manada, dos veces en el mismo episodio** — `ereq_feafe3ac`: gemela11
defiende en **t534** (`atacar_W` → slot 9), gemela10 defiende en **t573** y
**t583** (`atacar_SE` → slot 9). Las dos responden al mismo cazador, por
turnos, después de que él golpeara:
<https://api.observatory.softmax-research.net/v2/coworlds/replays/static/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/sha256%3Ac96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9/index.html?v=2#replay=https%3A%2F%2Fsoftmax-public.s3.amazonaws.com%2Freplays%2Fb481c43e-d49f-4e2b-a0b6-a73898506aea.replay>

**Defensa limpia** — `ereq_8a674d69`: gemela11 defiende en **t483** (→ slot 12):
<https://api.observatory.softmax-research.net/v2/coworlds/replays/static/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/sha256%3Ac96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9/index.html?v=2#replay=https%3A%2F%2Fsoftmax-public.s3.amazonaws.com%2Freplays%2Ffc91ff56-cb39-4375-97e8-8f2b9e13a650.replay>

# LAS VARAS (v34 contra v30 del 57, método idéntico)

| vara | **v34** | v30 (57) |
|---|---|---|
| **V1(a) iniciaciones-estrictas** | **0** | 0 |
| **V1(b) DEFENSAS por la hermana** | **12** (en 7 episodios) | **0** (por construcción) |
| respuestas a mi propio agresor | 327 | 736 |
| ataques elegidos contra la hermana | **0** | 0 |
| **V2 la ocasión** | **20 ventanas / 6 eps** | 25 / 9 |
| **V3 la defensa llega** | **5/20 = 25 %** · **5/8 = 62 % donde era posible** | 0/25 |
| **V4 ¿protege?** | 5/5 sobreviven con defensa · 15/15 sin | 25/25 |
| **V5 el precio** | 5 defensas medidas: **0 defensoras caídas** en 240 tics, **0 "ambas caen"**, Δhp mediano **−20** | — |
| V6 juntas a 8 | 5/40 (12 %) | 3/40 (8 %) |
| V7 moneda | top-4 8 (**20 %**) · wins 1 · podio 0 | 5 (12 %) · 1 · 1 |
| **V8 estabilidad** | cooldown 0 · congelado 0 | 0 · 0 |

# LA AUTOPSIA DE P2 (`autopsia_manada.py`)

411 tics de ocasión, dentro de 20 ventanas:

| sospechosa | medida | veredicto |
|---|---|---|
| ¿la ocasión no ocurre? | 20 ventanas en 6 episodios | **NO — ocurre** |
| ¿la certificación no cierra? | el parte con `a=1` y posición está en el 100 % de los tics de ocasión (es la definición) | **NO** |
| **¿el golpe es posible?** | **solo el 37 % de los tics** (151/411). Falla por **no alineado** (228 tics) o **fuera de alcance** (32: espada rango 1, lanza 2) | **SÍ — la causa** |
| ¿la huida gana? | en la ocasión elige `noop` 346 veces; solo 21+8+5 son movimientos | **NO: no huye, es que no alcanza** |

**Por ventana**: 8 de 20 tuvieron geometría posible alguna vez; **en 5 de esas
8 defendió (62 %)**. Las 12 restantes son ventanas donde el cazador estaba a
dos o tres casillas sin alineación — el animal ve a su hermana atacada, tiene
el arma y la certeza, y **no llega**.

# EL PRECIO, DICHO ENTERO (V5 + el hallazgo)

- **La defensora no muere por defender**: 0 caídas en los 240 tics siguientes,
  0 casos de "ambas caen". El riesgo "juntas se cazan juntas" **no aparece**
  en esta tanda.
- **Pero cuesta vida**: Δhp mediano **−20** en la ventana siguiente a defender.
  Defender duele; no mata.
- **FUEGO AMIGO — el hallazgo que no estaba previsto**: hubo **4 golpes entre
  hermanas**, y **3 de ellos son daño colateral de defensas**: la gemela ataca
  al cazador (slot 9, `defensa_pareja=True`) y el proyectil alcanza a **la
  hermana que defendía** en la línea de tiro (la interposición certificada en
  el 40). Ninguno es conducta: en los cuatro, el ataque iba a un extraño.
  **Defender a tu hermana puede golpear a tu hermana**, y hoy la tabla no lo
  prevé.

# LO QUE NO SE PUDO MEDIR (honesto)

**P3 (¿protege?) no discrimina con este instrumento**: sobreviven a la ventana
5/5 con defensa y 15/15 sin ella. La vara "sigue viva 240 tics después"
satura al 100 % en ambos brazos —igual que el proxy de exposición del 51—
porque la muerte en este mundo llega mucho después del acoso. **No hay
evidencia de que proteja, ni de que no**; hace falta otra vara (¿daño recibido
por la cazada durante la ventana? ¿tics hasta salir de banda?), medible sobre
estos mismos diarios sin gastar. Declarado.

# INCÓGNITAS CON MÉTODO

1. **Resellar P2 con la geometría dentro** (la mesa): "ocasión" debería exigir
   cazador **alineado y en alcance**; con esa definición la defensa llega el
   62 %. Sin gastar: recomputable de estos diarios.
2. **El alcance es el cuello**: con espada (rango 1) el 63 % de los tics de
   ocasión son inalcanzables. Un arma de rango (lanza 2, arco 8) cambiaría la
   cifra sin tocar la tabla — pero el arma no se elige, se encuentra.
3. **El fuego amigo de la defensa**: la tabla podría descontar el riesgo de
   que la hermana esté en la línea (el 40 certificó la física; nunca la
   modelamos). Es diseño nuevo, no se hizo aquí.
4. **La vara de protección** (arriba): recomputable ya.

# QUÉ QUEDA EN EL REPO

- `runs/manada/` — episodios.json (cost_preview 20), 40 res_, 80 diarios,
  resumen.json, autopsia.json · `runs/xp_manada_v34.json`.
- `manada_campo.py` (V1-V8) · `autopsia_manada.py` (la autopsia de P2).
- `gemv-anima:v11` subida. **v34 intacta**; liga v19.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

La manada existe y se le ve la cara: doce veces en cuarenta partidas, una
gemela vio a su hermana golpeada, supo por radio quién la golpeaba, comprobó
que ese cuerpo estaba de verdad donde ella decía, y respondió. Y en un
episodio lo hicieron por turnos, las dos contra el mismo cazador, con
cuarenta tics de diferencia. Eso no estaba escrito en ninguna línea de
conducta: sale de pesar la vida de la hermana contra la propia.

Y lo primero que hay que decir del honor: aguanta. Cero iniciaciones
estrictas, cero ataques elegidos contra la hermana, en cuarenta partidas más.
Ampliar por quién se pelea no amplió a quién se pega.

El sello de la defensa falla en su letra —cinco de veinte— y la autopsia
explica por qué de una forma que no admite consuelo pero tampoco culpa: en
doce de esas veinte ventanas **el golpe era imposible**. El cazador estaba a
dos casillas en diagonal rota, o a tres, y la espada llega a una. El animal
veía a su hermana atacada, tenía la certeza y el arma en la mano, y se quedaba
quieto porque no alcanzaba. Donde sí alcanzaba, defendió cinco de ocho veces.
La mesa dirá si eso es la manada o si el sello se resella con el alcance
dentro; el banco no se pone la medalla solo.

Y la factura, que es lo que hace creíble todo lo demás. Defender cuesta veinte
puntos de vida y no mató a nadie: ninguna defensora cayó, ninguna pareja cayó
junta. Pero apareció un precio que no habíamos previsto y que hay que decir
alto: **tres de los cuatro golpes entre hermanas de esta tanda salieron de una
defensa**. La gemela dispara al cazador y el proyectil encuentra primero a la
hermana que iba a salvar. La física ya la certificamos hace veinticuatro
encargos; lo que no hicimos nunca fue enseñarle a mirar quién está en la línea
antes de defender. Hoy sabemos que hace falta.

---

## Reproducción

```bash
cd gemv-coworld
python3 paintball/manada_campo.py     # V1-V8 pareado v34/v30
python3 paintball/autopsia_manada.py  # la autopsia de P2 (la geometria)
# tanda: xreq_7066af5f…, cuerpo en runs/xp_manada_v34.json (cost_preview 20)
```
