# Hecho — la ración y la venda en ZERO-SUM

Fecha: 2026-09-06 · **Solo lectura**: no se ejecutó ninguna partida ni se tocó
código. Todo sale de la documentación del mundo, del fósil del simulador y de
registros crudos de partidas ya jugadas.

---

## 1 · Qué hace cada una (certificado)

| | **venda** (`first_aid`) | **ración** (`rations`) |
|---|---|---|
| vida que devuelve | **50 HP** | **15 HP** |
| ¿tarda? | **sí — canal de 2 s** (48 tics a 24 tps) | **sí — canal de ~24 tics** (1 s) |
| ¿la cancela el daño? | **SÍ: cualquier daño lo cancela** (el kit **no** se pierde) | **NO** — medido en partida (§3) |
| ¿la bloquea el veneno? | **sí** (el dardo del blowgun "blocks first-aid") | no documentado |
| cómo se obtiene | botín (cofres, pods de patrocinador) | **los arbustos la dan** (forrajeo) + botín |
| precio de patrocinador | — | **20 softcoin** (`sword` = 120) |

**Fuente primaria** — `~/paintball_recon/docs/zero-sum/README.md`, sección
*Items*, líneas 49-53:

> *"blowgun+darts (4 dmg + poison: 2 HP per second pulse, INT-scaled duration,
> **blocks first-aid**), … **first-aid kit (50 HP, 2 s channel, cancelled by
> any damage), rations (15 HP)**."*

y línea 46: *"bushes yield rations"*; catálogo de patrocinador en
`protocol_player.md:32` (`"rations": 20`).

## 2 · La mecánica exacta, del simulador

`~/paintball_recon/docs/zero-sum/src/sim.nim`:

- **La cura llega de golpe al COMPLETAR el canal**, no gradualmente, y va
  topada al máximo de vida (línea 832, en `resolveChannels`):

  ```nim
  a.hpCenti = min(MaxHpCenti, a.hpCenti + def(a.channeling.item).heal * 100)
  ```

  (el mundo lleva la vida en centésimas: `hpCenti`, de ahí el `heal * 100`).
  Si el canal no llega a su `doneTick`, **no cura nada**.

- **El canal se abre al usar** y su duración sale del catálogo (línea 809-810):

  ```nim
  a.channeling = Channeling(kind: chConsume, item: slotItem, packIdx: invSlot,
                            doneTick: s.tick + d.useTicks)
  ```

- **La cancelación por daño es SOLO para la venda** (líneas 867-869, dentro de
  la resolución de daño):

  ```nim
  # ANY damage cancels a first-aid channel (kit kept — DESIGN §3.2)
  if v.channeling.kind == chConsume and v.channeling.item == iFirstAid:
    v.channeling = Channeling()
  ```

  El `item == iFirstAid` es explícito: **el canal de la ración sobrevive al
  daño**. Es la diferencia mecánica de fondo entre las dos.

> **Límite declarado de esta fuente**: el fósil `sim.nim` del repositorio **no
> incluye la tabla `def()` del catálogo** (viene de un módulo ausente), así
> que los enteros 50/15 y las duraciones no se leen ahí. Se certifican con el
> README (arriba) y con la medida en partida (§3). Es el mismo fósil
> incompleto que ya declaramos en el encargo 52 (no conoce el canal `team`).

## 3 · Medida en partida real (registro crudo)

Tres usos de ración en diarios de la tanda 66 (`paintball/runs/manada2/`),
leyendo el hp tick a tick alrededor del `usar_racion`:

| episodio · agente | tic del uso | hp al usar | daño recibido durante el canal | hp tras completarse | **subida** | tics hasta la subida |
|---|---|---|---|---|---|---|
| `ereq_4b24cc53` a10 | t588 | 88 | sí (→76) | **91** | **+15** | ~25 |
| `ereq_a62f7c2d` a10 | t374 | 92 | sí (→84→76) | **91** | **+15** | ~27 |
| `ereq_a4afa48e` a11 | t1162 | 80 | sí (→60) | **75** | **+15** | ~27 |

**Lo que esto certifica**: (a) la ración devuelve **exactamente 15 HP**;
(b) tarda **~24 tics** (un segundo) más el retardo de registro del diario;
(c) **el daño no la cancela** — en los tres casos el agente fue golpeado
durante el canal y la cura llegó igual, tal como dice el código.

## 4 · ¿Alimenta la ración alguna otra estadística (hambre, energía)?

**No. En zero-sum no existe hambre, energía, estamina, sed ni fatiga.**
Búsqueda de `hunger|starv|energy|stamina|thirst|fatigue` en `README.md`,
`protocol_player.md`, `protocol_global.md` y todo `src/*.nim`: **sin
resultados**. El estado del jugador que el mundo publica
(`protocol_player.md:50`) es `pos`, `hp`, `stats`, `hand`, `body`, `pack`,
`effects`, `damage_taken`, `kills`, `damage_dealt`, `move_ready_in`,
`attack_ready_in`, `action_result` — **no hay ningún contador de nutrición**.

**La ración es, exactamente, una venda pequeña y rápida que no se interrumpe.**
Su nombre es temático; su función es curar 15 HP.

---

## 5 · Cómo lo trata nuestra tabla (v37) — la pregunta añadida

### 5.1 · ¿Qué distingue nuestra ánima entre venda y ración?

`paintball/alma/mundo.py:128-134` — la distinción **no está cableada, se
deriva del catálogo del mundo**:

```python
cons = [i for i in self.items.values() if i.kind == "ikConsumable"]
cons.sort(key=lambda i: i.heal, reverse=True)
# botiquin = el consumible que MAS cura; el resto, raciones. [impl]
self.id_botiquin = cons[0].id
self.id_raciones = tuple(i.id for i in cons[1:]) or (cons[0].id,)
```

Es decir: **"venda" = el consumible que más cura** (first_aid, 50) y
**"ración" = todos los demás** (rations, 15).

### 5.2 · S-PROVISION: ¿valora solo las vendas o también las raciones?

**Las dos cosas, y de forma asimétrica** (`alma/appraisal_zs.py`):

- **Para que la fila NAZCA se cuentan SOLO VENDAS.** El "cuánto llevo yo"
  (`_botR`) y el "cuánto lleva ella" (`b<n>` del parte v2) filtran por
  `id == mundo.id_botiquin`. Con dos raciones y ninguna venda, **S-PROVISION
  no se enciende**.
- **Para ALIVIARLA vale cualquier consumible que cure.** El bucle del alivio
  acepta todo ítem con `kind == "ikConsumable" and heal > 0` a ≤2 casillas de
  ella — **incluidas las raciones**.
- **El candidato `soltar` del decisor abre cualquier consumible que cure**
  (`decisor_zs.py`, bloque 6b: `if it and it.kind == "ikConsumable" and
  it.heal > 0`), recorriendo el pack **en orden de ranura** y quedándose con
  el primero (`break`). No prefiere la venda: suelta **lo primero que
  encuentre**.

**Consecuencia declarada**: la fila se justifica con vendas pero **el gesto
que se ejecuta puede ser una ración**. Esa asimetría no está sellada por
ninguna mesa; es un efecto de dos criterios distintos (uno estricto para
contar, otro amplio para aliviar) que conviene decir en el paper.

### 5.3 · Los dones, por tipo de objeto

Contados con el mismo criterio en las dos tandas (tic en que se elige
`soltar_*` con la hermana viva a ≤2 casillas):

| tanda | total | **vendas** (`first_aid`) | **raciones** (`rations`) |
|---|---|---|---|
| **66** (v35, social ON) | **98** en 13 eps | **8** (8 %) | **90 (92 %)** |
| **72** (v27-pareja, ablación) | **1** en 1 ep | **0** | **1 (100 %)** |

**Los "98 dones" del 66 son, en su enorme mayoría, raciones**: noventa de
noventa y ocho. Sólo ocho fueron el botiquín de 50 HP. Y el don único de la
ablación —el que movió S-DANO-PAREJA, fila de v19/v27— también fue una
ración.

**Qué significa para el paper**: el gesto de dar existe y está medido, pero
**lo que se da es mayoritariamente el consumible barato** (15 HP, 1 s de
canal, imposible de interrumpir) y no el caro (50 HP, 2 s, cancelable por
cualquier golpe). Dos lecturas posibles, ninguna sellada: puede ser que las
raciones simplemente **abunden más** (los arbustos las producen; las vendas
son botín escaso), o que la ánima **suelte lo primero que encuentra en el
zurrón** por el `break` del bloque 6b. Distinguirlas exige contar qué había
en el pack en cada don, y **eso no se ha medido**.

---

## Rutas de las fuentes

| ruta | qué aporta |
|---|---|
| `~/paintball_recon/docs/zero-sum/README.md` (líneas 44-53) | **fuente primaria**: 50 HP / 2 s / cancelable; 15 HP; arbustos dan raciones; veneno bloquea first-aid |
| `~/paintball_recon/docs/zero-sum/protocol_player.md` (28, 32, 50) | campos `heal`/`use_ticks` del catálogo; precio de patrocinador (`rations`: 20); estado del jugador (sin hambre) |
| `~/paintball_recon/docs/zero-sum/src/sim.nim` (809-810, 823-841, 867-869) | mecánica: canal `doneTick`, cura al completar topada al máximo, **cancelación solo de `iFirstAid`** |
| `~/paintball_recon/docs/zero-sum/src/*.nim`, `README.md`, `protocol_*.md` | **sin resultados** para hambre/energía/estamina |
| `paintball/runs/manada2/ereq_4b24cc53…/a10`, `…a62f7c2d…/a10`, `…a4afa48e…/a11` | los tres usos de ración medidos (+15 HP, ~24 tics, no cancelada por daño) |
| `paintball/alma/mundo.py` (128-134) | cómo se deriva venda-vs-ración del catálogo |
| `paintball/alma/appraisal_zs.py` (bloque S-PROVISION, PROMPT_59/61) | conteo por `id_botiquin`; alivio por cualquier `ikConsumable` con `heal>0` |
| `paintball/alma/decisor_zs.py` (bloque 6b) | el candidato `soltar` abre cualquier consumible que cure, primero del pack |
| `paintball/runs/manada2/`, `paintball/runs/ablacion/` | el conteo de dones por tipo (98 → 8/90; 1 → 0/1) |
