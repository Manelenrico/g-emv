# HECHOS DE PERCEPCIÓN — QUÉ VE UN AGENTE DE OTRO (The Pack, peldaño 1, verificación previa)
**Solo lectura. 2026-08-27. Certifica: el vigilante, a petición de la mesa. Nada implementado.**
**Fuentes:** (a) MOTOR empírico — instrumentación directa del env de mettagrid (imagen
`cvc-game-wait-natural:latest`, `Simulation._c_sim.observations()`), la verdad de terreno de lo que el
encoder C++ emite; (b) player_config `mudanza/player_config_ref.json`; (c) NUESTRO código (repo local).
El encoder de observación vive en C++ (`mettagrid_c` compilado), NO certificable desde fuente Python;
se certifica EMPÍRICAMENTE (probe: dos agentes en ventana, se leen los tokens de la celda del otro).

## Cuadro empírico (probe: agente 0 observa al agente 1 cargado — heart3, oxy2, aligner1, vibe=heart)
El motor emite, en la celda de CADA agente observado (propio Y ajeno), este set de tokens `(loc, fid, val)`:

| feature (id) | ¿emitido del OTRO? | valor observado |
|---|---|---|
| `agent_id` (11) | **SÍ** | 1 (la IDENTIDAD individual 0..7) |
| `agent:group` (0) | SÍ | 0 (equipo/grupo) |
| `tag` (6) | SÍ | 7 (team:cogs) **y** 8 (type:agent) — multivaluado |
| `vibe` (5) | **SÍ** | 1 (el modo/intención declarado; change_vibe_*) |
| `inv:hp` (20) | SÍ | 100 |
| `inv:heart` (22) | **SÍ** | 3 (¡hearts PORTADOS del otro!) |
| `inv:oxygen` (12) | **SÍ** | 2 (¡CARGA del otro!) |
| `inv:aligner` (26) | **SÍ** | 1 (¡GEAR del otro!) |
| `inv:energy` (24) | SÍ | 20 |
| `inv:solar` (34) | SÍ | 3 |
| `last_action` (2) | **NO** | ausente (ni del otro ni del self) |
| `last_action_move` (68) | **NO** | ausente |

## Respuestas a las cinco preguntas de la mesa

**1. ¿Identidad del otro?** **SÍ.** El motor emite `agent_id` (id 11) = 0..7 en la celda de cada agente
observado. La identidad individual (ag0..ag7) es OBSERVABLE. (Probe: los 7 agentes ajenos aparecen con
agent_id 1..7 distintos; el propio, id 0, en el centro loc 102.)

**2. ¿A qué distancia? ¿Mismo disco?** **Mismo disco que el resto de objetos.** Ventana egocéntrica 13×13
(radio L2 ~6; el 16 es stride del byte, no columna — ver [[vara-real-ws140-numeros-canonicos]]). En el
spawn nativo (agentes agrupados junto al hub) los 7 ajenos caben en la ventana a t0 (locs r6-r12, c3-c9).
Un agente fuera del radio ~6 no aparece, igual que cualquier objeto.

**3. ¿Atributos visibles?** **Casi TODO su estado escalar:** identidad (`agent_id`), equipo (`agent:group`
+ tags team/type), **hearts portados** (`inv:heart`), **carga** (`inv:oxygen/carbon/germanium/silicon`),
**gear** (`inv:aligner/miner/scout/scrambler`), hp, energía, solar, y la **`vibe`** (modo/intención). Todo
por-agente, en su celda. (Confirmado emitiendo valores no-cero en el agente 1 y leyéndolos en la obs del 0.)

**4. ¿Acción en curso del otro?** **NO directamente.** `last_action`/`last_action_move` NO se emiten en la
observación (ausentes para el propio y para los ajenos). La única señal de "intención" es la **`vibe`**
(un modo que el agente FIJA con change_vibe_*, no la acción momentánea). Minar/depositar solo es INFERIBLE
por coincidencia (agente junto a la mina + el `team:{material}` del hub sube; o una junction cambia de
dueño al re-observarla) — nunca atribuible a un agente concreto desde la observación.

**5. ¿Guarda algo POR-AGENTE nuestra memoria/DESMENTIDO que el censo herede?** **NADA por identidad.**
- NUESTRA política solo lee a los otros como CONTEO POR TAG DE EQUIPO: `allies`/`rivals` cardinales
  (`bronce/gemv_policy_bronce.py:3545-3557`; social ponderada en `appraisal/appraisal_v3.py:187-203`). El
  `agent_id`, la `vibe` y el inventario del otro se parsean al `scalar_map` pero **jamás se leen**. El
  inventario que sí leemos es siempre el PROPIO, en `AGENT_LOC` (=102).
- La MEMORIA (`memoria/memoria_v1.py:117-119`) indexa por `(world_row, world_col, object_class)`; a los
  otros los guarda como clase genérica `"ally"`/`"rival"` en su celda, sin id, sin inventario
  (`memoria_v1.py:265-279`). El DESMENTIDO (`bronce/gemv_policy_bronce.py:2635-2662`) recuerda CELDAS de
  rechazo por coordenada+TTL, no agentes; el "último move/pos" que guarda es el NUESTRO.
- **Conclusión:** un censo por-agente (clave ag0..ag7) **no tiene nada que heredar** de la memoria actual
  (cell+class, anónima). Pero el SUSTRATO OBSERVABLE es rico: identidad + hearts + carga + gear + vibe por
  agente y por tick, hoy ignorado. Las columnas del censo se pueden diseñar sobre eso REAL, no sobre supuestos.

## Nota de método
Probes: `scratchpad/probe_obs{,2,3}.py` (efímeros). Ids de feature del player_config: `agent:group`=0,
`last_action`=2, `vibe`=5, `tag`=6, `agent_id`=11, `inv:heart`=22, cargos 12/14/16/18, gear 26/28/30/32,
`team:*`=60-67 (stock del hub), `protocol_*`=48-59 (canal del pregonero). model.py `1e511978` intocado.
