# Acta — RECONOCIMIENTO DE BATTLE ROYALE (temporada tres, coste 0)

Fecha: 2026-09-04 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_58_reconocimiento_battle_royale.md` · **Solo lectura**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga zero-sum en **v19**, intacta. La pareja (57) sigue aparte.
- **Ninguna imagen, ningún submit, ningún código tocado.** Se leyó: el
  paquete descargado (`~/paintball_recon/br/…`), el manifiesto, y las docs
  públicas del repo `Metta-AI/coworld-battle-royale`.

---

# EL TITULAR, PRIMERO

Battle Royale **NO es una variante de nuestro zero-sum**: es otro motor.
Zero-sum daba al jugador un **obs JSON estructurado** (`visible.agents[]` con
`hp_band`, `damage_taken[].source`, `teammate_slot`) y aceptaba **acciones
tipadas** (`move_N`, `atacar`, `usar`). BR hereda el motor de **Coworld CTF /
sprite_v1**: el obs es un **stream de sprites + marcadores HUD** (posiciones
en píxeles, sin bandas, sin autor del daño) y la acción es una **máscara de
gamepad** (D-pad mover, botones rotar el aim en *brads*, gatillo disparar,
bit 7 granada). **Toda nuestra tabla se ata al obs y a la acción de
zero-sum; ninguno de los dos existe en BR.** El coste real de "portar" no es
ajustar filas: es reescribir la percepción y la actuación enteras. Detalle y
número abajo.

---

# A · EL MUNDO (con fuentes)

| dato | valor | fuente |
|---|---|---|
| coworld id | `cow_0e13dff3-0f67-4a55-90d0-4929c480e7ef` | `coworld list` / API |
| nombre · versión | **battleroyale 0.1.16**, canónica | manifiesto |
| owner | **treeform@softmax.com** (no Ari; Ari propuso el experimento) | `game.owner` |
| liga pública | **Battle Royale** `league_b88a269b…`, abierta desde **2026-08-20** | `coworld leagues` |
| repo | **github.com/Metta-AI/coworld-battle-royale** (README/RULES/PROTOCOL/VERTICAL_SLICE por URI) | `docs.pages` |
| variantes | **br-12** (12 jugadores) · **br-16** (16) | `variants` |
| modo | `ffa` (battle royale); el motor también hace `ctf` | `config.mode` |
| baseline | bot `baseline` empaquetado (imagen en `coworld_images.json`), 12× en la certificación | `certification.players` |

**El mundo, en una frase** (de la descripción del manifiesto, certificada):
free-for-all, cada asiento su propio equipo/color, **sin aliados**; 2-16
jugadores en anillo de spawn; **20 hit points, UNA vida, sin respawn**; zona
segura que encoge 150 s hasta un **suelo del 3 %**; fuera del anillo cuesta
**1 hp cada 48 ticks**; combate/visión/movimiento heredados de CTF (aim
desacoplado del movimiento con cono de niebla, armas *hitscan* con *windup*
de gatillo, rango fijo, aim con ruido; el disparo no visto se oye como
**anillo de sonido** jitterado); **grito de 10 chars** oído a 1/5 del campo;
en el final (≤3 vivos) los bots baseline cierran sobre el enemigo más
cercano. 24 ticks/s; `maxTicks` de liga **8640 = 6:00**.

XP alojadas: la liga es pública y abierta — nuestro método pareado
(champion-inside por `top_n`) es viable en principio. **No se lanzó nada.**

---

# B · EL DIFF DE PROTOCOLO vs zero-sum 0.1.18

## Observación — **cambio de naturaleza, no de campos**

| lo que la tabla usa (zero-sum) | en BR (sprite_v1) |
|---|---|
| `you.pos` (tile 48×48, Chebyshev) | posición en **píxeles**, mapa 1× (arena "huge") |
| `you.hp` número + `hp_band` ajeno | hp propio número (20); **de los demás no hay banda ni número — son sprites** |
| `visible.agents[]` (lista tipada) | **objetos-sprite** `(x,y,z,layer,sprite_id)`; nada semántico |
| `damage_taken[].source = "P<slot>"` | **NO existe**: sabes que te bajó el hp, no quién (salvo que le vieras disparar) |
| `teammate_slot`, `team` | **desaparecen**: cada asiento es su propio equipo, sin aliados |
| `effects` (poison…) | no aplica; sin veneno en la espec de BR |
| `projectiles[]` (2 tiles/tick) | armas **hitscan** (instantáneas, rango 1300 px); no hay proyectil que interponer |
| cono de visión | **niebla real**: bubble 90 px + cono ±45° del aim; LOS corta |
| — | **anillo de sonido**: disparo no visto se oye jitterado (dirección aproximada) |

El obs de zero-sum era un contrato de datos; el de BR es un **fotograma
renderizado + marcadores HUD** (`own aim <brads>`, máscara de caminabilidad
como sprite). El HUD de sprite_v1 **no publica salud ni equipo ajenos**: hay
que reconstruirlos de los sprites.

## Acciones — **de acción tipada a mando de consola**

| zero-sum | BR (CTF input mask) |
|---|---|
| `{"type":"action","do":"move_N"}` etc. | **D-pad** (bits de dirección) |
| `atacar_*` (melee/alcance, cooldown por arma) | **gatillo** (botón A): *windup* 5 ticks, cooldown 12 ticks |
| — (el aim iba con el cuerpo) | **aim DESACOPLADO**: B rota antihorario, Select horario, **5 brads/tick**; el aim se **bloquea** al apretar gatillo |
| `usar`, `soltar`, `coger`, `empuñar` | recoger/soltar armas del suelo (dropWeaponOnDeath); sin nuestro repertorio de zurrón |
| — | **granada**: mantener bit 7 (valor 128, botón C) carga, soltar lanza |

## El grito (el único canal)

- **10 caracteres** (descripción del manifiesto).
- **Broadcast gated**: llega solo si el receptor está **dentro del radio de
  visión del emisor Y con LOS** (línea de vista) — más estricto que el team
  de zero-sum (que era cerrado por equipo, 0 fugas). Aquí **cualquiera** que
  te vea puede oírte: "diplomacia y traición de proximidad" (palabras del
  owner).
- **Cadencia 1 msg/s** (24 ticks). Coste de acción: la espec de CTF lo trata
  como canal aparte (como en zero-sum), **a certificar en cable**.

## Anillo, botín, armas, score

- **Anillo**: encoge 150 s hasta 3 % del área; fuera, 1 hp/48 ticks;
  `ringRecoveryTicks=2` (la exposición **drena** al reentrar, no resetea).
- **Armas** (FFA): tres bandas ancladas al mapa — **low** (2 dmg) amplia,
  **mid** (3 dmg) intermedia, **heavy** (5 dmg) en el centro; cluster central
  de 12 items. `dropWeaponOnDeath=true` en las variantes: el muerto deja su
  arma de un uso.
- **Score (R11 del mundo nuevo)** — **cambia el incentivo de raíz**:
  `reward = survival (1/seg) + podio (1º 100, 2º 40, 3º 15) + 10 por kill
  (último que dañó) + 4 por asistencia (repartida entre los que dañaron en
  240 ticks)`. En zero-sum se puntuaba por **placement** (sobrevivir bastaba,
  0 kills valía). En BR **matar puntúa 10 y el podio pesa 100/40/15**: el
  animal que jamás inicia (0 iniciaciones en 58 encargos) cobra **solo
  survival + podio**, nunca los +10. Esto es lo que Ari llama "non-aggression
  stops being cheap" — y es honesto: **es el mundo el que cobra, no nosotros
  el que nos endurecemos** (R9).

---

# C · LAS MEDIDAS ANTI-PASIVIDAD, UNA A UNA (con fuente y número)

El motor tiene **tres** sistemas; **solo uno está encendido** en las
variantes de liga (br-12/br-16). Se certifica del `config_schema` (defaults)
y de los `game_config` de cada variante:

| medida | mecanismo · número | estado en br-12/16 | ¿qué fila nuestra lo sentiría? |
|---|---|---|---|
| **ANILLO** | zona encoge en `ringShrinkSec=150` s a `ringFloorAreaPct=3` %; fuera **1 hp / `ringDamageTicks=48`**; drena al reentrar (`ringRecoveryTicks=2`) | **ACTIVO** | F-ANTICIPACIÓN (anillo) — pero su entrada (centro/radio) hoy viene del obs JSON; en BR hay que leerla del HUD/sprite |
| **PRESIÓN POR AISLAMIENTO** | `passivityRadius` > 0 → quien esté lejos de **todo** otro vivo acumula presión; `passivityGraceTicks=480`, daño `passivityDamageTicks=96`, drena `passivityRecoveryTicks=2` | **INERTE** (`passivityRadius=0`, no lo sube ninguna variante) | ninguna hoy: **castiga "estar solo lejos", que nuestra tabla no anticipa** — falta de plato del mundo nuevo si se enciende |
| **BARRAGE (bombardeo final)** | `barrageMaxPerSec` > 0 → lluvia de granadas por el borde desde `barrageStartSec=30` s del final, satura en `barrageSaturateSec=30` s | **INERTE** (`barrageMaxPerSec=0`) | ninguna: castigo espacial temporal que no modelamos |
| **BOTS FINALES** | ≤3 vivos → los baseline cierran sobre el más cercano (respetando anillo y gates de aim/fuego) | ACTIVO (comportamiento del rival, no del mundo) | nos afecta como presión, no como fila |
| **EL SCORE** (arriba) | matar +10, podio 100/40/15, survival 1/s | ACTIVO | **la medida de verdad**: no daña, pero deja de premiar la mera supervivencia |

**Lectura**: "a few anti-passivity measures" son, en la liga real, **el
anillo + el marcador**. Los dos sistemas de castigo directo por no-pegar
(presión por aislamiento, barrage) **existen en el motor pero vienen
apagados** — si Ari los enciende para el experimento, **son platos que
nuestra tabla no ve** (declarado, no se arregla aquí: R9). El anillo sí lo
veríamos si portamos su entrada; el score no se "siente" en una fila, se
paga en el resultado.

---

# D · QUÉ ES DE ZERO-SUM Y QUÉ ES DE LA TABLA (inventario por dependencia)

| fila | depende de | en BR |
|---|---|---|
| **S-DANO/MUERTE-PAREJA, S-VINCULO, S-HERIDO, el PARTE** | `teammate_slot`, canal team | **se apagan solas** (sin equipo no hay hermano) — pero hay que verificar que se apagan LIMPIAMENTE, como el P5 del 54/56: sin `teammate_slot` la rama entera es inerte. **Probable bit-limpio, a certificar en el nuevo obs** |
| **S-7-AGRESOR, el MURO** | `damage_taken[].source` (`era_agresor`) | **SIN ENTRADA**: BR no dice quién te disparó. `era_agresor` no se puede construir de fábrica. El muro (reactivo al agresor) queda ciego |
| **F-4-ALCANCE, F-ANTICIPACIÓN** | posición ajena + anillo | entrada EXISTE pero cambia de forma: posiciones en píxeles/sprites, anillo circular (no cuadrado Chebyshev). **Recalibrar geometría** |
| **R-CARENCIA, R-ACOPIO, R-LLAMADA, R-PROMESA** (botín) | `visible.items[]` tipado | botín EXISTE (bandas low/mid/heavy, cluster central) pero llega como **sprites sin etiqueta de valor**: hay que reconocer el arma por su sprite |
| **CUESTA (F-DANO convexa)** | `you.hp` propio | **pasa tal cual** (hp propio es número, 20 en vez de 100 — reescalar el umbral) |
| **S-8-EXPOSICIÓN** | quién me ve (INT/visión) | concepto vale, pero la visión de BR es **cono + niebla + LOS**, no radio limpio: recalibrar |
| **el HONOR (0 iniciaciones)** | candidato `atacar` con `era_agresor` | sin `source` no hay `era_agresor`; el honor tal como lo definimos **no tiene sobre qué decidir**. Habría que redefinir "iniciar" en un mundo hitscan |

**Resumen del inventario:**
- **Pasan tal cual (reescalando constante)**: CUESTA (hp propio). *Una.*
- **Necesitan re-certificación de entrada** (existe, otra forma): F-4,
  F-ANTICIPACIÓN, R-* (botín), S-8-EXPOSICIÓN.
- **Se apagan solas** (sin equipo): todo el bloque S de pareja + el parte
  (probable bit-limpio, a verificar).
- **Sin entrada en BR** (el mundo no la da): S-7-AGRESOR, el MURO, el HONOR
  como `era_agresor` — todo lo que colgaba de "quién me dañó".

---

# E · LA ESTIMACIÓN HONESTA — "portar y certificar" en "a few days"

**No es un port de tabla; es una capa de percepción y actuación nueva.** El
compromiso de "unos días" es realista **solo si** se acota así:

1. **Puente de percepción** (lo caro): de sprite_v1 (frame + HUD) a un
   pseudo-obs estructurado que la tabla pueda leer — reconstruir posiciones,
   hp propio, armas del suelo por sprite, borde del anillo. **Sin autor del
   daño ni salud ajena**: dos entradas que simplemente no están.
2. **Puente de actuación**: de acción tipada a máscara de gamepad con **aim
   desacoplado en brads** — nuestro decisor elige "a dónde", pero BR exige
   además "hacia dónde apunto y cuándo disparo", un eje de control que **no
   teníamos** (en zero-sum el ataque iba con el cuerpo). Esto es diseño
   nuevo, no traducción.
3. **Qué se puede prometer de verdad en pocos días**: un animal que **se
   mueve, respeta el anillo, recoge un arma y NO inicia** — y medir su score
   (survival+podio, ~0 kills) contra el baseline. Eso ya responde la pregunta
   de Ari ("el mismo agente antes y después de que el mundo cobre por la
   pasividad"): **cuánto pierde por no pegar, en la moneda de BR.** Es el
   método de la casa (medir, no endurecer) y cabe en el plazo.
4. **Lo que NO cabe en pocos días**: un animal que apunte y dispare bien
   (control continuo de aim con windup y niebla) — eso es una policy de
   puntería, otra temporada. Y si Ari enciende la presión por aislamiento o
   el barrage, son platos nuevos que habría que modelar desde cero.

**Recomendación para el sofá**: aceptar el experimento en su versión honesta
—portar el esqueleto (mover + anillo + no iniciar), medir el precio de la
pasividad en la moneda nueva— y declarar por adelantado que la puntería y los
castigos dormidos quedan fuera del primer plazo. Es exactamente lo que R9
pide: no maquillamos al animal para BR; dejamos que el mundo le cobre y
apuntamos la factura.

---

# INCÓGNITAS CON MÉTODO (lo que este reconocimiento no pudo cerrar)

1. **El obs del jugador BR en cable**: la espec dice "sprite_v1 + HUD
   markers" pero no lista los campos exactos que llega por el socket. Método:
   `coworld run-episode` local con el baseline y capturar el primer obs
   (fixture), como hicimos con zero-sum en el debut. **No ejecutado** (el
   encargo era solo leer; queda como primer paso del 59 si la mesa aprueba).
2. **El coste de acción del grito**: la espec de CTF lo separa del input;
   confirmar en cable que no pisa el gate de disparo. Método: fixture.
3. **Salud ajena**: ¿de verdad no hay banda de hp del enemigo en el HUD?
   sprite_v1 no la publica; confirmar que no llega por otro marcador. Método:
   fixture + inspección del frame.
4. **La liga**: `league_b88a269b` es pública; falta ver si admite XP
   privadas pareadas (champion-inside) como zero-sum. Método: un `xp-request`
   de sonda **cuando la mesa lo apruebe** (tiene coste; no se hizo).

# QUÉ QUEDA EN EL REPO

- `paintball/br_reconocimiento_acta.md` — este acta.
- El paquete descargado vive en `~/paintball_recon/br/` (READ-ONLY, fuera
  del repo, como el resto de `paintball_recon`).
- **Nada de código, ninguna imagen, ningún submit.** Liga zero-sum v19
  intacta; `motor/model.py` `1e511978c251130e95169ebf8443efa1` al cierre.

---

# LECTURA FRÍA

Ari propuso el experimento perfecto para nuestro método —el mismo animal
antes y después de que el mundo cobre por la pasividad— y el reconocimiento
dice que el experimento es real y que el mundo es otro. Battle Royale no es
zero-sum con el anillo más apretado: es el motor de CTF, con obs de sprites y
mando de consola, donde el aim vive separado del cuerpo y nadie te dice quién
te disparó. Nuestra tabla, que nació leyendo un JSON honesto y escribiendo
acciones con nombre, se queda sin sus dos orillas a la vez.

Lo que sobrevive es lo que siempre fue nuestro y no del mundo: la filosofía
de medir en vez de maquillar. Podemos poner en BR un esqueleto que se mueva,
respete el anillo y no pegue primero, y leer en la moneda nueva —diez por
kill, cien por el podio, uno por segundo vivo— exactamente cuánto cuesta no
iniciar. Esa es la respuesta a la pregunta de Ari, y cabe en unos días. Lo
que no cabe es enseñarle a apuntar: eso es otra criatura.

Y hay una elegancia en el hallazgo que conviene decir. Durante cincuenta y
ocho encargos construimos un animal que nunca pegó primero porque en
zero-sum sobrevivir bastaba para puntuar. BR quita esa red: aquí la
supervivencia paga uno por segundo y el podio paga cien, pero el que mata se
lleva diez cada vez. Por fin hay un mundo donde el pacifismo tiene precio, y
la factura la pasa el mundo, no nosotros. Medirla sin tocar al animal es,
palabra por palabra, lo que la casa sabe hacer.
