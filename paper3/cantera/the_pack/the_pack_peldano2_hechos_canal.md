# HECHOS DEL CANAL SOCIAL — para el peldaño 2 (el pregonero firmado). Verificación previa, solo lectura.
**2026-08-29. Certifica: el vigilante, a petición de la mesa. Nada implementado.**
**Fuentes:** (a) MOTOR — cogsguard/mettagrid en la imagen `cvc-game-wait-natural` (config Python + empírico);
(b) NUESTRO pregonero — `bronce/gemv_policy_bronce.py` (file:line). model.py INTOCABLE (1e511978).

## HALLAZGO CENTRAL
Nuestro pregonero **NO usa el canal talk/broadcast del MOTOR**: usa un **TABLÓN DE FICHERO**
(`/coworld-artifact/pregonero_<slot>.jsonl`), un bind-mount rw compartido por TODOS los contenedores de
jugador (`.venv-coworld/.../coworld/runner/runner.py:319-320`). Cada agente escribe su fichero y lee los de
los demás. El canal del motor (talk = "sabor de las vibes", `cogsguard/game/talk.py:27`) es OTRA cosa y no lo
usamos. ⇒ **el formato del mensaje lo controlamos nosotros; firmar no depende del motor.**

## Respuestas a las cinco preguntas

**1. ¿Qué transporta HOY un mensaje? ¿Lleva emisor?** El mensaje del tablón es una línea JSON
(`gemv_policy_bronce.py:264`): `{"wr", "wc", "cls", "tick", "slot"}`. **YA lleva el emisor** en el campo
`slot` (y redundante en el nombre `pregonero_<slot>.jsonl`). PERO el consumidor lo **IGNORA**
(`_pregonero_consume`, :288-303 — no lee `fa["slot"]`, no atribuye, no pondera por fuente; la única
discriminación por origen es saltarse el propio fichero por nombre, :282). ⇒ **el emisor viaja pero es
INERTE aguas abajo: el conocimiento entra en memoria SIN FIRMA EFECTIVA.** (El canal del motor, la vibe, sí
lleva emisor implícito —se observa en la celda del hablante con su agent_id— pero es baja capacidad, ~7
categorías, y no es este canal.)

**2. ¿Alcance? ¿Cooldown 50?** El tablón es un mount rw compartido ⇒ **broadcast pleno al equipo, sin radio**
(todos leen a todos; se reescribe entero cada tick, `_pregonero_publish` :254-267). El **cooldown 50** del
player_config es del canal TALK del MOTOR (`TalkConfig.cooldown_steps=50`, mettagrid_config.py:215, "min
resend gap") — **NO aplica a nuestro tablón** (no pasa por el motor; sin cooldown, reescritura por-tick).

**3. ¿Formato/capacidad?** JSON-lines sobre fichero, **sin `max_length` del motor** (el talk del motor sí lo
tiene: 140 chars). Cabe: posición absoluta (`wr`,`wc`) + clase (`cls`: junction_{gray,rival,own} /
extractor_{oxígeno,carbono,germanio,silicio}, `_PREGONERO_CLASSES` :250-251) + frescura (`tick`) + emisor
(`slot`). NO viajan muros, estados internos ni intenciones. Capacidad ampliable a voluntad (dict JSON).

**4. Nuestro pregonero: qué/cuándo/cómo.**
- **Emisor** (`_pregonero_publish` :254-267): cada tick, todo junction/extractor en la ventana percibida se
  registra en `_pregonero_seen` como sighting de PRIMERA MANO (anti-eco: nunca se publica lo oído) y se
  reescribe el tablón (escritura atómica tmp+replace). Sitio de llamada :2785-2809.
- **Receptor** (`_pregonero_consume` :270-306): lee los tablones ajenos, inyecta sus hechos FUERA de mi
  ventana en la memoria con confianza MENOR (`eff = tick − PENALTY`, PENALTY=500 ⇒ conf inicial ~0.5, misma
  curva de decaimiento), vía `mem._record(wr,wc,cls,1.0,eff)` (:302). Candados: (i) PERCEPCIÓN MANDA en mi
  disco ±6 (:296); (ii) FRESCO GANA (:300). El consumidor aguas abajo (ganancia/atractores) solo ve más
  objetos en la memoria.
- **El 85%** (fuente `pregonero_flood.md:28-36`, corrida tanda_p2500_r1, 8 ag × 2500t): fracción SOCIAL de
  las junctions conocidas = del-canal / conoce; ag0 82%, ag4 96%, ag7 80% ⇒ rango 80-96%, media ~85%. El
  animal debe la mayor parte de su mapa a la palabra, no a sus ojos. Matiz honesto: del tablón viajan 76%
  extractores / 24% junctions (`:25-26`); el 85% es sobre junctions-conocidas; y en cosecha "el 85% social
  era flood que la cosecha no necesitaba" (`pregonero_ablacion_b1.md:55`) — robusto como fracción de MAPA,
  matizado como valor de cosecha. Corrobora: `pregonero_ablacion_b2.md:57-58`.

**5. ¿Bits libres para firmar?** **SÍ, ilimitados** — JSON sobre fichero, sin límite de motor. Y de hecho
**el emisor YA está** (`slot`, :264). El peldaño 2 mínimo NO necesita ampliar el formato ni tocar el motor:
el trabajo es (a) que el consumidor USE/VERIFIQUE el emisor (comprobar `slot`-JSON == nombre-de-fichero; hoy
:282-303 no lo hace y el mount rw compartido lo hace falsificable), y (b) nace la columna de FIABILIDAD (¿su
anuncio era verdad? = distancia anuncio-vs-conducta/primera-mano, medida contra el censo LIMPIO que ya
tenemos). El único coste que el forense señala es CPU de parseo (`pregonero_flood.md:46`: 24M parses/corrida),
lineal en nº de entradas — no un límite duro.

## Síntesis para el diseño de la mesa
«Firmar lo que ya se anuncia, sin ampliar lo anunciable» encaja EXACTO: no se añade contenido anunciable; se
hace LOAD-BEARING el emisor que ya viaja (hoy inerte) y se estrena la FIABILIDAD por fuente. Sin motor, sin
bits nuevos, sin radio: solo activar el `slot` y medir su verdad contra lo observable certificado.
model.py `1e511978` intocado.
