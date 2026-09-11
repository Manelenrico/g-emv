# Hecho — cómo identifica el mundo a los jugadores en ZERO-SUM

Fecha: 2026-09-08 · **Solo lectura**: no se ejecutó nada, no se tocó código.
Fuentes: el protocolo del mundo, el fósil del simulador y del servidor, y
registros reales de la tanda 66.

`md5 motor/model.py` = `1e511978c251130e95169ebf8443efa1` (sin tocar).

---

## 1 · La respuesta corta

**Un número de asiento. Nada más.**

De cada jugador visible, la observación trae **exactamente un identificador: el
`slot`** (0-15). No llega identificador de agente, ni identificador de política,
ni nombre. El asiento es **estable toda la partida** —lo fija la URL de conexión
y está autenticado por un token propio— pero **no significa nada entre
partidas**: el mismo asiento lo ocupa otro cualquiera en la siguiente.

En el registro de daño recibido, al que golpea se le identifica con la cadena
**`"P<slot>"`** — el mismo número, con una letra delante.

Y **los nombres que enseña el visor no son del mundo: son de la plataforma.**

---

## 2 · Lo que llega de cada jugador visible

`~/paintball_recon/docs/zero-sum/protocol_player.md:62-64`, la observación de
cada tic:

```json
"visible": {"agents": [{"slot":7,"team":"D","pos":[15,38],"hp_band":"hurt",
                        "hand":"sword","body":null,"netted":false,
                        "poisoned":true,"channeling":false}]}
```

Ocho campos, y el **único identificador es `slot`**. Los demás son **estado**
(dónde está, cómo de herido, qué empuña, si está enredado, envenenado o
canalizando), no identidad.

**`team` no añade información**: los asientos van de dos en dos y el equipo se
deduce del asiento (0-1 = A, 2-3 = B … 10-11 = **F**, 14-15 = H). Se ve en el
propio fósil, en los comentarios de la lista de nombres (`sim.nim:261-269`), y
lo confirma nuestro registro: asientos 10 y 11 → `"team": "F"`.

Verificado en un registro real del 66 (`ereq_9869b665`, a10, t459):

```json
{"slot": 9, "team": "E", "pos": [24,21], "hp_band": "healthy",
 "hand": "sword", "body": null, "netted": false, "poisoned": false,
 "channeling": false}
```

**No hay un solo campo más.** Ni `agent_id`, ni `policy`, ni `name`.

### 2.1 · Todo lo demás que nombra a un agente usa también el asiento

| dónde | campo | qué es |
|---|---|---|
| `chat` | `"from": 2` | asiento |
| `visible.projectiles` | `"shooter": 9` | asiento |
| `visible.pods` | `"recipient_slot": 4` | asiento |
| `events` (`death_fireworks`, `gift_incoming`…) | `"slot": 9`, `"recipient": 4` | asiento |
| `final` | `"winner_slot": 2` | asiento |
| `you.damage_taken` | `"source": "P9"` | asiento, con prefijo |

**El asiento es la única moneda de identidad de todo el protocolo.**

### 2.2 · Y a veces ni eso

Los camuflados **no aparecen** en `visible.agents` salvo dentro de su tope de
detección o si se delatan atacando (`protocol_player.md:73-75`). Es decir: el
mundo no solo da poca identidad — **a veces no da ninguna**, porque el cuerpo
entero falta de la lista.

---

## 3 · Tu propia identidad (la que solo tú recibes)

`player_config`, una vez al conectar (`protocol_player.md:12-13`):

```json
{"type": "player_config", "protocol": "zero_sum.player.v1",
 "slot": 3, "team": "B", "teammate_slot": 2, "name": "P03", ...}
```

Tres cosas tuyas: **tu asiento**, el de **tu pareja** (`teammate_slot`) y un
**`name`**. Y ese `name` es **`"P03"` para el asiento 3**: es el asiento otra
vez, formateado. **No es una identidad nueva.**

> **Límite declarado**: nuestro registro **no puede confirmar el `name`**,
> porque `policy.py:223-228` guarda del `player_config` solo `slot`, `team`,
> `teammate_slot`, `protocol`, `tick_rate`, `max_ticks`, `ignition_tick` y
> `zone_schedule`, y `mundo.py` **no lee el campo `name` en absoluto**
> (búsqueda de `name` en `mundo.py`: **cero apariciones**). En los 9,1 MB del
> diario de `ereq_9869b665` a10, `"name"` aparece **0 veces**. La forma `P03`
> se certifica con el documento del protocolo, no con nuestra medida.

---

## 4 · ¿Es estable el asiento durante la partida? — **Sí, y está autenticado**

- **Lo fija la URL de conexión**: `ws://<game>:8080/player?slot=<0..15>&token=<token>`
  (`protocol_player.md:3-4`).
- **Con token por asiento**: el servidor guarda `playerTokens` *por asiento* y
  rechaza el upgrade si el token no es el de ese asiento
  (`server.nim:252-266`: `appState.playerTokens[externalSlot] != token` → **401
  "bad slot/token"**). No puedes conectarte a un asiento que no es el tuyo.
- **Reconectar no te mueve**: *"Reconnecting with a valid token replaces your
  previous socket; your agent state is untouched"* (`protocol_player.md:6-7`;
  política de reconexión también en `server.nim:274`).
- El simulador trabaja siempre sobre `for i in 0 .. 15` con `s.agents[i]`: **el
  índice del asiento ES el agente** durante toda la partida.

**Pero la estabilidad se acaba con la partida.** El asiento 9 no es "alguien":
es una silla. En la partida siguiente la ocupa otra política. **No hay ningún
identificador persistente entre partidas en la observación** — ni debería
esperarse: es un battle royale con roster rotatorio.

---

## 5 · El registro de daño recibido: `"P<slot>"`

`you.damage_taken` es una lista por tic de `{"source": ..., "amount": ...}`
(`protocol_player.md:52`). La etiqueta la construye `applyDamage`
(`sim.nim:860-863`):

```nim
v.damageSources.add((
  (if label.len > 0: label
   elif source >= 0: "P" & $source
   else: "environment"), centi))
```

**Tres formas posibles, y solo tres:**

| `source` | cuándo | ejemplo real (tanda 66) |
|---|---|---|
| **`"P<slot>"`** | te golpea un **agente** y no hay etiqueta | `{"source":"P9","amount":19.8}` — `ereq_9869b665` a10 t2192, hp 92 → 72 |
| **etiqueta fija** | daño con nombre propio: `"zone"`, `"flood"`, `"firestorm"`, `"poison"` | `{"source":"poison","amount":2.0}` — `ereq_c6717e24` a11 t3201, hp 2 → 0 |
| `"environment"` | fuente ≥ 0 ausente y sin etiqueta | no observado en el 66 |

**El veneno es el caso interesante**: se etiqueta `"poison"`, así que la víctima
**pierde el asiento del que la envenenó** en su propio registro de daño — aunque
el mundo por dentro sí se lo apunta al tirador (`a.poisonFrom`, y el kill cuenta
para él). Es decir: **hay un tipo de daño en el que el agredido no puede saber
quién se lo hace**. Para nuestra fila del nombre del agresor (PROMPT_68) eso es
un agujero declarado, no un descuido.

---

## 6 · Los nombres del visor: **son de la interfaz, no del mundo**

### 6.1 · El mundo tiene una lista de nombres… que no emite

`sim.nim:261-276` carga dieciséis nombres por defecto, sobreescribibles por la
config de la partida:

```nim
const DefaultNames = [
  "Adino", "Tryphena",       # team A
  "Carpus", "Tazkia",        # team B
  "Luqman", "Sherah",        # team C
  "Karna", "Damaris",        # team D
  "Archippus", "Balqees",    # team E
  "Kaysan", "Urvasi",        # team F
  "Sanjaya", "Tirzah",       # team G
  "Zimri", "Bhishma"]        # team H
...
result.playerNames[i] = p["name"].getStr()
```

**Pero `playerNames` no se lee en ninguna parte del fósil.** Búsqueda en los
tres fuentes disponibles (`sim.nim`, `server.nim`, `presentation_replay.nim`):
**tres apariciones y ninguna es una lectura** — la declaración
(`sim.nim:60`), el relleno por defecto (271) y la sobreescritura (276). **Nunca
sale en un mensaje del protocolo.** En el fósil es un campo muerto.

(Nuestros asientos 10-11 son el equipo F: si esos nombres se usaran en algún
sitio, nuestras gemelas se llamarían **Kaysan** y **Urvasi**.)

### 6.2 · Los nombres que ves en el visor vienen de la plataforma

Están en los metadatos del episodio que devuelve la API de Softmax
(`runs/manada2/episodios.json`, campo `participants`), indexados por
**`position`, que es el asiento**:

```json
{"position": 10, "kind": "policy",
 "policy_version_id": "581d27d6-d3fe-480b-b637-bd9e85b5bdf8",
 "policy_id": "...", "policy_name": "gemv-anima", "version": 12,
 "player_id": "ply_...", "player_name": "Manel Enrico",
 "is_filler": false, "is_seed": false}
```

Del mismo episodio `ereq_9869b665`:

| asiento | `policy_name` | v | `player_name` |
|---|---|---|---|
| 0 | `Zero Sum Baseline` | 1 | David Greis |
| **9** | `ryanschiller-zero-sum-player-v1` | 2 | **Ryan Schiller** |
| **10** | **`gemv-anima`** | **12** | **Manel Enrico** |
| **11** | **`gemv-anima`** | **12** | **Manel Enrico** |
| 13 | `aaron-zs-fable` | 2 | Aaron |

(De paso: el **P9** que mató a nuestra a10 en la escena de las dos vendas era la
política de Ryan Schiller. Nuestra ánima **nunca pudo saberlo**: para ella era
`P9` y punto.)

Y el resultado del mundo, `res_ereq_9869b665….json`, **no tiene ni un nombre**:
sus claves son `scores`, `placements`, `kills`, `damage_dealt`,
`survival_ticks`, `gifts_received`, `winner_slot`, `winner_team`, `match_ticks`,
`seed` — **todo arrays indexados por asiento**.

### 6.3 · La conclusión, que es la que pedía el encargo

**El nombre es cosa de la interfaz.** El mundo habla en asientos de punta a
punta: protocolo, simulador y fichero de resultados. La plataforma que organiza
las partidas es la que sabe qué política y qué persona ocupa cada asiento, y es
ella quien se lo pasa al visor. **El agente que juega no ve nada de eso.**

El asiento es, además, **la única llave que une los dos mundos**: `position` en
los metadatos = `slot` en la observación = índice en los arrays del resultado.

---

## 7 · Qué significa esto para el paper tres

- **La ánima no puede reconocer a nadie.** Su fila del nombre del agresor
  (PROMPT_68, `IDENTIDAD_ON`) opera sobre lo único que existe: un número de
  silla, válido mientras dure la partida. **No es memoria de un individuo: es
  memoria de una posición.** Escribirlo de otra manera sería inflar el hecho.
- **La hermana no es una excepción.** También es un asiento —el
  `teammate_slot`—, dado en el `player_config`. El vínculo no lo sostiene una
  identidad del mundo: lo sostiene **un número que llega una vez al empezar** y
  el parte que las gemelas se mandan por el canal de equipo.
- **Y hay dos agujeros declarados**: el camuflado, que borra al cuerpo de la
  lista, y el veneno, que llega etiquetado `"poison"` y **sin asiento**. En esos
  dos casos ni siquiera hay silla a la que ponerle nombre.

---

## 8 · Lo que NO se puede afirmar

- **No se ha visto el `name` del `player_config` en un registro real**: nuestro
  logger lo descarta y `mundo.py` no lo lee. La forma `"P03"` sale del
  documento del protocolo (§3).
- **El fósil está incompleto y ya lo sabíamos**: falta la tabla `def()` del
  catálogo, y `presentation_replay.nim` (5,3 kB) es demasiado pequeño para ser
  el visor entero. **No se puede descartar que el visor real lea `playerNames`
  por una vía que no está en el Mac.** Lo que sí es cierto: en las tres fuentes
  disponibles, nadie lo lee, y los nombres que aparecen en nuestros registros
  del 66 son los de la plataforma, no los de `DefaultNames`.
- **No se ha abierto ningún `.replay`** para ver qué identificadores lleva
  dentro: los replays se ven por URL y no hay ninguno guardado en local
  (`hecho_liga_publica.md`, §4).
- **`"environment"` no se ha observado** en la tanda 66; se cita del código.

---

## Rutas de las fuentes

| ruta | qué aporta |
|---|---|
| `~/paintball_recon/docs/zero-sum/protocol_player.md` (3-7, 12-13, 52, 62-64, 73-75, 79-82) | la URL con `slot`+`token` y la política de reconexión; el `player_config` con `slot`/`team`/`teammate_slot`/`name`; **los ocho campos de `visible.agents`**; `damage_taken`; los eventos y el chat, todos por asiento; el camuflaje |
| `~/paintball_recon/docs/zero-sum/src/sim.nim` (60, 261-276, 853-863, 956-960) | **`DefaultNames` y `playerNames`, que nunca se leen**; `applyDamage` construyendo **`"P" & $source`**; `poisonFrom` (el mundo sí sabe quién envenenó) |
| `~/paintball_recon/docs/zero-sum/src/server.nim` (42-43, 252-266, 274) | **token por asiento** y rechazo 401 si no cuadra; la reconexión que no mueve de silla |
| `paintball/runs/manada2/ereq_9869b665-…/a10/…log` | **el registro real**: `ve_agentes` con solo `slot`+estado, `damage_taken` con `"P9"`, y `"name"` con **cero apariciones** en 9,1 MB |
| `paintball/runs/manada2/episodios.json` (`eps[].participants`) | **de dónde salen los nombres del visor**: `policy_name`, `version`, `player_name`, `player_id`, indexados por `position` = asiento |
| `paintball/runs/manada2/res_ereq_9869b665-….json` | el resultado del mundo: **arrays por asiento, sin un solo nombre** |
| `paintball/alma/policy.py` (221-228) · `paintball/alma/mundo.py` | qué guardamos del `player_config` (y que `name` no se lee) |
