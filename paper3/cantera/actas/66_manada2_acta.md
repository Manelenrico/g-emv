# Acta — LA MANADA, SEGUNDA TANDA (v35) · **"LA MANADA, LIMPIA"**

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_66_la_manada_segunda_tanda.md`

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **v35 sin tocar desde el 65**: `appraisal_zs.py 9f679bdc…`, `decisor_zs.py
  d9c8baab…` — verificados antes del build.
- **Coste**: imagen `gemv-anima:v12` + tanda `xreq_c2d94f73-…`, 40 episodios
  privados, **`cost_preview` = 20 cr** (≤ tope 30). Cosecha **40/40, 80/80
  diarios**, 0 fallos.

## El roster, verificado (el cambio del encargo)

En el 64 nuestra propia campeona de liga (`gemv-anima:v1`) entraba por
`top_n` y las gemelas se enfrentaban a sí mismas. **Cómo se excluye**: se
abandona `top_n` y se arma un **roster explícito** con los **10 rivales
reales** censados en el 64 (`policy_ref` por UUID de versión: scavenger:12,
relh:52, courier:3, belobog:2, ryanschiller:2, zs-patient:3, aaron-zs-fable:2,
zero-sum-example:1, skourehjan:1, Zero Sum Baseline:1), repitiendo cuatro
para llenar los 14 asientos. **Verificación en el roster resultante: en los
40 episodios, participantes nuestros fuera de los asientos 10/11 = 0.**

---

# EL VEREDICTO, APLICADO TAL COMO QUEDÓ SELLADO

**P1 ∧ P2 ∧ P3 → "LA MANADA, LIMPIA"**: defiende cuando puede y **no hiere a
quien salva**. P4 no acompaña (la protección no es comparable: se dice, no se
sella), así que **no** es "y protege".

| sello | medida | veredicto |
|---|---|---|
| **P1 = V1(a)** iniciaciones-estrictas 0 · ataques a la hermana 0 | **0 y 0** (en 918 respuestas y 104 defensas) | **CUMPLE** (gate absoluto) |
| **P2 = V3** ≥50 % de las ocasiones (con alcance) | **6/12 = 50 %** | **CUMPLE** (justo en el umbral) |
| **P3 = V4** fuego amigo de la defensa = 0 | **0** (baseline 3) | **CUMPLE** |
| **P4 = V5** menos daño a la cazada tras defender | dirección **contraria** y ventanas **no comparables** | **no se sella** (abajo) |
| **P5 = V9** sin degradación | cooldown 0 · congelado 0 | **CUMPLE** |

---

# LAS VARAS (v35 del 66 contra v34 del 64)

| vara | **v35 (66, sin campeona)** | v34 (64) |
|---|---|---|
| V1(a) iniciaciones-estrictas | **0** | 0 |
| V1(b) **defensas por la hermana** | **104** | 12 |
| respuestas a mi propio agresor | **918** | 327 |
| ataques contra la hermana | **0** | 0 |
| V2 ocasiones (con alcance) | 12 | 8 |
| **V3 la defensa llega** | **6/12 = 50 %** | 5/8 = 62 % |
| **V4 fuego amigo** | **0** | 3 |
| V5 protección (golpes 120 t, media) | 0,33 con · **0,00** sin | 0,40 con · 0,93 sin |
| V5 hp de la cazada al cerrar | **40** con · 74 sin | 75 con · 9 sin |
| V6 precio | 9 defensas · **0 caídas** · **0 ambas** · Δhp **−20** | 5 · 0 · 0 · −20 |
| V7 juntas a 8 | **6/40 = 15 %** | 5/40 = 12 % |
| V8 moneda | top-4 5 (12 %) · wins 0 · podio 0 | 8 (20 %) · 1 · 0 |
| V9 estabilidad | 0 · 0 | 0 · 0 |

**El titular**: **104 defensas y ni un solo golpe entre hermanas.** En el 64,
con doce defensas, tres acabaron hiriendo a la defendida; en el 66, con casi
nueve veces más defensas, **cero**. La corrección del fuego amigo del 65
—que la foto diga a quién le da de verdad un golpe que atraviesa— funcionó en
el campo tal como el banco predijo.

## Las escenas, para los ojos

**Defensa repetida contra el mismo cazador** — `ereq_a62f7c2d`: gemela11
defiende en **t435, t628 y t643** (→ slot 9):
<https://api.observatory.softmax-research.net/v2/coworlds/replays/static/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/sha256%3Ac96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9/index.html?v=2#replay=https%3A%2F%2Fsoftmax-public.s3.amazonaws.com%2Freplays%2F9b98dc83-545b-49f4-bc74-a7d94e608ac4.replay>

**La defensa sostenida** — `ereq_4b24cc53`: gemela10 defiende siete tics
seguidos (**t2549-t2555** → slot 13) y vuelve a hacerlo en **t3008-t3011**
(→ slot 7):
<https://api.observatory.softmax-research.net/v2/coworlds/replays/static/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/sha256%3Ac96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9/index.html?v=2#replay=https%3A%2F%2Fsoftmax-public.s3.amazonaws.com%2Freplays%2F3e5751db-f57f-46f1-95b7-3e0f95208d93.replay>

# P4 · LA PROTECCIÓN: por qué NO se sella (la cautela declarada)

La dirección sale **contraria** al 64 (0,33 golpes con defensa vs 0,00 sin),
pero la comparabilidad lo explica y lo invalida: **la cazada está mucho más
herida en las ventanas defendidas** (hp 40 al cerrar) que en las no defendidas
(hp 74) — exactamente al revés que en el 64 (75 vs 9). Es decir: **en cada
tanda, la defensa ocurre en un tipo distinto de ventana**, así que la
comparación con-sin mide el estado de partida, no el efecto de defender. Con
n=12 y ventanas incomparables, **la vara sigue sin poder sellar dirección**.
El sello lo preveía ("si las ventanas no son comparables, se dice y no se
sella"): se dice.

# EL PRECIO, otra vez entero

- **0 defensoras caídas** en los 240 tics siguientes y **0 casos de "ambas
  caen"** — el riesgo "juntas se cazan juntas" sigue sin aparecer en 80
  episodios de campo.
- **Δhp −20** de mediana tras defender: el mismo precio que el 64. Defender
  duele, no mata.
- **0 fuego amigo** (era 3): el precio que sí se pudo quitar, se quitó.

# LO QUE EL CAMBIO DE ROSTER ENSEÑÓ (declarado)

Quitar a nuestra campeona cambió el mundo más de lo previsto: **918
respuestas a agresor propio** frente a 327, y **104 defensas** frente a 12.
Contra rivales ajenos las gemelas son atacadas mucho más — y por eso la
manada tiene ocho veces más ocasiones de aparecer. La moneda baja (top-4
12 % vs 20 %) pero con R12 delante eso **no es señal** a n=40; lo honesto es
decir que **la tanda del 66 es más dura**, no que v35 sea peor: los rosters
no son comparables (es el mismo aviso del 34, al revés).

# INCÓGNITAS CON MÉTODO

1. **La vara de protección necesita pareo por estado**: comparar ventanas con
   la cazada en el mismo rango de hp (p.ej. bandas de 20 hp). Con 12+20
   ventanas acumuladas entre 64 y 66 quizá ya dé; recomputable sin gastar.
2. **P2 justo en el umbral** (50 %): las 6 ocasiones sin defensa merecen
   autopsia fina — ¿huida, o el candidato vetado por enfriamiento? El 65 dejó
   el instrumento.
3. **El alcance sigue sin flipear**: 104 defensas ocurren donde ya había
   alcance; la corrección del 65 no creó ocasiones nuevas (12 vs 8, dentro
   del ruido). Su efecto real sigue sin demostrarse.

# QUÉ QUEDA EN EL REPO

- `runs/manada2/` — episodios.json (cost_preview 20), 40 res_, 80 diarios ·
  `runs/xp_manada2_v35.json` (el roster explícito, reproducible).
- Análisis: `manada_campo.py`, `proteccion.py` (reutilizados sin tocar).
- **v35 intacta**; liga v19; `gemv-anima:v12` subida.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

Ciento cuatro veces una gemela vio a su hermana atacada y respondió, y ni una
sola vez le dio a ella. Ese es el resultado del encargo y conviene medir lo
que significa: en la tanda anterior, con doce defensas, tres terminaron
hiriendo a la persona que se quería salvar — una de cada cuatro. Escribimos
entonces una corrección de una sola idea, que la foto dijera a quién le da de
verdad un golpe que atraviesa una casilla, y el campo la ha devuelto perfecta:
cero de ciento cuatro.

El honor aguanta en su forma estricta por sexta tanda consecutiva. Y aguanta
en el mundo más duro que hemos jugado: al quitar del roster a nuestra propia
campeona —que hasta ahora nos hacía de rival amable— las gemelas pasaron de
327 a 918 respuestas a agresores propios. Es un mundo que las golpea el
triple, y siguen sin pegar primero.

La protección sigue sin dejarse medir, y esta vez el motivo es elegante: en
el 64 la defensa ocurría con la hermana sana y en el 66 con la hermana ya
herida, así que comparar "con defensa" contra "sin defensa" mide en qué
momento aparece la defensa, no lo que la defensa consigue. Hace falta parear
por estado, y para eso ya hay treinta y dos ventanas guardadas entre las dos
tandas: se puede hacer sin gastar un crédito.

Queda dicho también lo que no sabemos: la moneda bajó, pero el roster cambió
a la vez, y con nuestra regla de siempre eso no es una señal sino dos cambios
a la vez. Lo que sí es señal, porque tiene baseline y tamaño, es que la
manada existe, defiende y ya no hiere a quien salva.

---

## Reproducción

```bash
cd gemv-coworld
python3 paintball/manada_campo.py     # varas base (v34/v30)
python3 paintball/proteccion.py       # P2' y la vara de proteccion
# tanda: xreq_c2d94f73…, roster explicito en runs/xp_manada2_v35.json
```
