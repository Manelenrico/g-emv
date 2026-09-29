"""DECISOR ZERO-SUM — el ciclo real: appraisal -> candidatos -> motor -> intencion.

QUE SE TRANSPLANTA DE LA ARCILLA DEL REPO (y que no):
  SI  motor/model.py            : opponent_distance + DEFAULT_CONFIG (importados)
  SI  planificador_v1.select_tiebreak : el desempate jerarquico firmado de la casa
  NO  planificador_v1.plan_terminal   : su rollout necesita las primitivas de
      machina (shift_tokens / dest_is_blocked / parse_tokens / modelo de
      transicion) sobre la rejilla egocentrica de tokens. zero-sum es otro
      sustrato (JSON con pos/hp/pack/visible): transplantarlo seria escribir un
      simulador de zero-sum. Se usa el EVALUADOR MINIMO EQUIVALENTE que autoriza
      el prompt, declarado abajo.
  NO  cortex, censo, pregonero de machina. Nada de eso entra.

EVALUADOR MINIMO EQUIVALENTE (declarado):
  Para cada candidato se construye la observacion PREVISTA a tick+H_MIRADA y se
  valora con la MISMA cadena que machina: appraisal -> State -> opponent_distance
  -> argmin -> select_tiebreak. Es el ciclo de machina con horizonte 1 sobre un
  paso COMPROMETIDO de H_MIRADA tics (en machina, H=1 colapsa al greedy
  bit-a-bit: planificador_v1.py:365).

  Lo que se prevé y por que:
    - mi posicion            : CIERTA (enfriamiento 16-SPD, solidos del mapa)
    - anillo en tick+H       : CIERTO (calendario sellado del player_config)
    - hp tras usar consumible: CIERTO (heal del catalogo)
    - zurron tras coger/usar : CIERTO
    - agentes y objetos ajenos: SE CONGELAN donde se vieron. NO es cierto; es la
      hipotesis minima del evaluador, y se declara. (R1 gobierna la TABLA, que
      solo anticipa el calendario; esta congelacion es del evaluador.)
    - efecto de atacar       : NO se prevé (esquiva, no es cierto). Consecuencia
      declarada en el acta: con la tabla v1 el motor NO tiene apetito de atacar.
"""
from __future__ import annotations

import math

from motor.model import DEFAULT_CONFIG, opponent_distance
from planificador.planificador_v1 import select_tiebreak

from alma import appraisal_zs as A

# MIRADA: cuantos tics de compromiso se preven. NO es libre: F-ANTICIPACION es
# BINARIA (dentro/fuera al cerrar el anillo), asi que solo da gradiente si el
# candidato ALCANZA a cruzar el borde dentro de la mirada. Con una mirada corta
# la fila es plana y el agente no migra (medido: episodio ep_alma_solo, 50 % de
# los tics fuera del anillo). Se mira hasta el PLAZO del anillo, acotado por el
# HORIZONTE de 20 s que la tabla sella.
H_MIRADA_MIN = 48                       # [impl] suelo: ~2 s, para que los
                                        # candidatos cortos no se confundan
_ROUND = 5             # misma precision que el planificador de la casa

DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1),
        "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}


class Bloqueos:
    """ARREGLO A (PROMPT_06): un candidato cuyo enfriamiento no ha expirado queda
    FUERA del set de candidatos.

    Los plazos se LEEN, no se cablean:
      - mover / ir-hacia : `you.move_ready_in` de la observacion
      - atacar           : `you.attack_ready_in` de la observacion
      - usar             : `use_ticks` del CATALOGO del player_config, arrancado
                           por el feedback del mundo (`action_result` == "ok"
                           justo despues de emitir `use` = canal iniciado).

    Motivo medido (tanda v2): el agente reemitia `use` durante todo el canal de
    24 tics con `move_ready_in == 0` -- moverse era legal y no lo hacia. 149
    tics perdidos en 7 episodios, ~21 por episodio afectado.
    """

    def __init__(self):
        self.canal_hasta = -1
        self.tics_cooldown = 0          # feedback "cooldown" recibido
        self.tics_congelado = 0         # ... teniendo movimiento disponible

    def actualiza(self, obs, mundo, ultima_accion, tick):
        you = obs.get("you") or {}
        res = you.get("action_result")
        if res == "cooldown":
            self.tics_cooldown += 1
            if (you.get("move_ready_in") or 0) == 0:
                self.tics_congelado += 1
        if ultima_accion and ultima_accion.get("do") == "use":
            idx = ultima_accion.get("slot")
            pack = you.get("pack") or []
            it = None
            if isinstance(idx, int) and 0 <= idx < len(pack) and pack[idx]:
                it = mundo.items.get(pack[idx].get("id"))
            ut = max(1, it.use_ticks if it else 1)
            if res in ("ok", "cooldown"):
                # "ok" tras un use = canal ARRANCADO en este tick.
                # "cooldown" = ya estabamos canalizando: cota superior segura.
                self.canal_hasta = max(self.canal_hasta, tick + ut)

    def veta(self, nombre, obs, tick) -> bool:
        you = obs.get("you") or {}
        if nombre.startswith(("move_", "paso_", "ir_")):
            return (you.get("move_ready_in") or 0) > 0
        if nombre.startswith("atacar_"):
            return (you.get("attack_ready_in") or 0) > 0
        if nombre.startswith(("usar_", "empunar_", "ponerse_")):   # todos son `use`
            return tick < self.canal_hasta
        return False


def _dir_hacia(p, q):
    dx = (q[0] > p[0]) - (q[0] < p[0])
    dy = (q[1] > p[1]) - (q[1] < p[1])
    for d, v in DIRS.items():
        if v == (dx, dy):
            return d
    return None


def _primero_en_linea(pos, objetivo_slot, obs, mundo):
    """EL FUEGO AMIGO (PROMPT_65): ¿quien recibe DE VERDAD mi proyectil?

    El mundo lo tiene certificado (fisica del 41): el proyectil viaja y pega
    al PRIMER cuerpo de la linea que no sea el tirador. Si entre yo y el
    objetivo hay otro cuerpo —mi hermana, por ejemplo— es ESE quien lo recibe.
    Devuelve el slot del interpuesto, o None si la linea esta limpia (y
    entonces la foto queda como estaba: al objetivo).
    """
    vis = (obs.get("visible") or {})
    agentes = vis.get("agents") or []
    destino = None
    cuerpos = {}
    for a in agentes:
        q = tuple(a.get("pos") or ())
        if not q:
            continue
        cuerpos[q] = a.get("slot")
        if a.get("slot") == objetivo_slot:
            destino = q
    if destino is None or destino == tuple(pos):
        return None
    dx = (destino[0] > pos[0]) - (destino[0] < pos[0])
    dy = (destino[1] > pos[1]) - (destino[1] < pos[1])
    pasos = max(abs(destino[0] - pos[0]), abs(destino[1] - pos[1]))
    for i in range(1, pasos):                 # sin incluir la casilla destino
        c = (pos[0] + dx * i, pos[1] + dy * i)
        sl = cuerpos.get(c)
        if sl is not None:
            return sl                          # el primer cuerpo se lo lleva
    return None


def campo_geodesico(mundo, destino):
    """GEODESICA — BFS desde el DESTINO sobre el mapa conocido, bloqueando
    solidos. Devuelve {(x,y): pasos hasta el destino}; inalcanzable => ausente.

    TRANSPLANTE de `coworld_adapter.gemv_policy._geodesic_field_global`
    (gemv_policy.py:661): misma idea —BFS desde el objetivo, los solidos
    conocidos bloquean, lo nunca visto es caminable, y el consumidor cae a la
    linea recta para las celdas ausentes—. ADAPTACIONES, minimas y declaradas:

      1. Rejilla ABSOLUTA 48x48 del `static_map` en vez de la ventana
         egocentrica 13x16 de machina. zero-sum publica el mapa entero en el
         `player_config`, asi que no hace falta ni la proyeccion a la frontera
         ni el atlas de fijos: el mapa es conocido y fijo.
      2. OCHO vecinos en vez de cuatro. machina se mueve en cruz; zero-sum se
         mueve en 8 direcciones y las diagonales cuestan igual
         (`protocol_player.md:117`). Con 4 vecinos la geodesica mentiria sobre
         la longitud del camino.
      3. Los solidos salen de `mundo.solido()` (muros, rocas y fortaleza leidos
         del `static_map`), no de tags de machina.

    El campo es CONSTANTE durante el episodio (el mapa no cambia), asi que se
    cachea por destino.
    """
    from collections import deque
    cache = getattr(mundo, "_campos_geo", None)
    if cache is None:
        cache = {}
        mundo._campos_geo = cache
    key = (int(destino[0]), int(destino[1]))
    if key in cache:
        return cache[key]
    campo = {}
    if mundo.solido(*key):
        cache[key] = campo
        return campo
    q = deque([(key[0], key[1], 0)])
    campo[key] = 0
    while q:
        x, y, d = q.popleft()
        for dx, dy in DIRS.values():
            nx, ny = x + dx, y + dy
            if (nx, ny) in campo or mundo.solido(nx, ny):
                continue
            campo[(nx, ny)] = d + 1
            q.append((nx, ny, d + 1))
    cache[key] = campo
    return campo


def _paso_geodesico(pos, campo, destino, ocupadas=()):
    """Direccion que BAJA la geodesica. None si no hay (o ya se llego).

    CUERPOS (PROMPT_15). El campo es el MAPA: muros, fijo, cacheado. Los
    cuerpos NO entran en el campo porque no son muros: se mueven, y un campo
    con gente dentro caducaria cada tic y habria que rehacerlo 16 veces por
    segundo. Entran aqui, en el PASO, que es lo unico que se emite y lo unico
    que el mundo puede rechazar. Regla, en tres escalones:

      1. la mejor vecina que BAJA y esta LIBRE;
      2. si todas las que bajan tienen a alguien encima, una vecina LIBRE que
         no aleje (mismo valor de campo): rodear pegado, no empujar;
      3. si tampoco hay, None — este tic no se camina. Mejor quieto que
         estampado: el mundo devolvia `blocked` en el 84,9 % de las ordenes
         `ir_*` (4210 emitidas, 3574 rechazadas; medido en el 14).

    La ocupacion es un hecho PRESENTE y cierto. Que el otro siga ahi el tic
    que viene NO se profetiza: por eso solo gobierna el PRIMER paso (ver
    `_camina_geodesica`), y se refresca en cada decision.

    ADAPTACION 4, declarada: entre las vecinas que bajan lo mismo, se elige la
    mas cercana al destino en linea recta. Con 8 vecinos la geodesica es la
    distancia de Chebyshev, asi que en campo abierto EMPATAN muchas casillas
    (ir al oeste y al suroeste bajan igual). Desempatando por el orden de las
    direcciones —como hace machina, que solo tiene 4 vecinos y casi no empata—
    el caminante se iba 8 casillas al sur antes de volver: mismo numero de
    pasos, pero un rodeo enorme en el espacio. Con este desempate el camino es
    recto cuando el mapa esta abierto y solo rodea cuando hay que rodear.
    """
    base = campo.get((pos[0], pos[1]))
    if not base:                       # ausente o ya en el destino
        return None
    ocup = set(ocupadas)
    mejor = None                       # escalon 1: baja y esta libre
    lado = None                        # escalon 2: no aleja y esta libre
    for d, (dx, dy) in DIRS.items():   # orden de DIRS: desempate final estable
        nx, ny = pos[0] + dx, pos[1] + dy
        v = campo.get((nx, ny))
        if v is None:
            continue
        libre = (nx, ny) not in ocup
        clave = (v, (nx - destino[0]) ** 2 + (ny - destino[1]) ** 2)
        if v < base:
            if libre and (mejor is None or clave < mejor[0]):
                mejor = (clave, d)
        elif v == base and libre and (lado is None or clave < lado[0]):
            lado = (clave, d)
    if mejor:
        return mejor[1]
    return lado[1] if lado else None


def _camina_geodesica(pos, campo, mundo, speed, ticks, destino, ocupadas=()):
    """Posicion tras `ticks` tics BAJANDO la geodesica. Rodea los obstaculos.

    Los cuerpos gobiernan SOLO el primer paso: donde hay gente AHORA es un
    hecho; donde la habra dentro de 11 tics no lo es. La imaginacion camina
    con la misma regla que las piernas en el paso que de verdad se emite, y
    con el mapa a secas en los siguientes. Declarado.
    """
    x, y = pos
    for i in range(ticks // mundo.coste_movimiento(speed)):
        d = _paso_geodesico((x, y), campo, destino, ocupadas if i == 0 else ())
        if d is None:
            break
        dx, dy = DIRS[d]
        x, y = x + dx, y + dy
    return (x, y)


def _simula_camino(pos, destino_o_dir, mundo, speed, ticks, hacia_punto):
    """Posicion tras `ticks` tics caminando. Enfriamiento y solidos: CIERTOS.

    Para los `move_*` (rumbo fijo) sigue siendo el caminante recto: es lo que
    esos candidatos significan. Los `ir_*` ya no pasan por aqui: usan la
    geodesica (ver `_camina_geodesica`).

    LA ZANCADA HONESTA (PROMPT_28). Antes, al toparse con un solido, esta
    funcion DESLIZABA por un eje — y el comentario de entonces lo confesaba:
    "como el mundo, que simplemente bloquea; aqui solo evita quedarse clavado".
    Es decir: la foto decia que avanzabas y la orden emitida iba de frente
    contra el muro. CERTIFICADO en la fuente (`sim.nim:622-624`,
    `resolveMovement`):

        if not inBounds(target) or blocksMovement(s.arena.tile(target)):
          s.lastActionResult[i] = "blocked"
          continue

    El mundo NO desliza: rechaza el movimiento entero. La foto ahora dice eso.
    Coste medido de la mentira (PROMPT_27 C): 2571 de 3223 bloqueos eran
    solidos, y el 45,9 % de TODAS las ventanas de movimiento se quemaban en
    ordenes que el mundo rechazaba."""
    x, y = pos
    coste = mundo.coste_movimiento(speed)
    pasos = ticks // coste
    for _ in range(pasos):
        if hacia_punto:
            d = _dir_hacia((x, y), destino_o_dir)
            if d is None:
                break
        else:
            d = destino_o_dir
        dx, dy = DIRS[d]
        if mundo.solido(x + dx, y + dy):
            break                      # el mundo bloquea y no desliza: aqui igual
        x += dx
        y += dy
    return (x, y)


def _obs_prevista(obs, mundo, mem, tick_eval, pos, hp, pack, hand, ver_pareja,
                  golpe=None, suelta=None, body=False):
    """Copia de la observacion con lo previsto sustituido."""
    you = dict(obs.get("you") or {})
    you["pos"] = list(pos)
    you["hp"] = hp
    you["pack"] = pack
    you["hand"] = hand
    if body is not False:          # False = "no se toca"; None = cuerpo vacio
        you["body"] = body
    vis = dict(obs.get("visible") or {})
    if ver_pareja and mem.pareja_pos:
        agentes = list(vis.get("agents") or [])
        if not any(a.get("slot") == mundo.teammate_slot for a in agentes):
            agentes = agentes + [{"slot": mundo.teammate_slot, "team": mundo.team,
                                  "pos": list(mem.pareja_pos),
                                  "hp_band": mem.pareja_banda or "healthy"}]
        vis = dict(vis, agents=agentes)
    # Se valora al tick REAL: lo unico del futuro que entra es el anillo, y entra
    # por ant_ctx. Asi la memoria temporal (voz, soledad) no se descuadra.
    if suelta is not None:
        # el objeto soltado aparece en el suelo, en MI casilla: es lo que la
        # fila de la medicina mira (distancia <=2 a la pareja herida).
        vis = dict(vis, items=list(vis.get("items") or [])
                   + [{"id": suelta[0], "n": 1, "pos": list(suelta[1])}])
    if golpe is not None:
        sl_obj, dmg = golpe
        ags = []
        for a in (vis.get("agents") or []):
            if a.get("slot") == sl_obj:
                base = a.get("_hp_est")
                if base is None:
                    # PROMPT_53: si el golpeado es la PAREJA, la base es el
                    # modelo del hermano (parte fresco -> hp exacto; sin el,
                    # la banda — v27 bit a bit). MISMA base que leen las
                    # filas S de pareja: los margenes entre candidatos no
                    # dependen de la base (solo del dano) y P5 se conserva.
                    if sl_obj == mundo.teammate_slot:
                        base = mem.pareja_hp_est(tick_eval, mem.hp_max or 100.0)
                    else:
                        base = A.BANDA_EST.get(a.get("hp_band"), 100.0)
                a = dict(a, _hp_est=max(0.0, base - dmg))
                # PROMPT_54: si el golpeado es la PAREJA, la foto lleva el
                # dano previsto en crudo — S-VINCULO decide "mata seguro"
                # contra el hp CIERTO (parte o limite de banda), no contra
                # la estimacion por punto medio.
                if sl_obj == mundo.teammate_slot:
                    a["_golpe_pareja"] = dmg
            ags.append(a)
        vis = dict(vis, agents=ags)
    centro, radio, dps = mundo.anillo_en(tick_eval)
    return {"tick": tick_eval, "phase": obs.get("phase"), "you": you,
            "visible": vis, "events": [], "chat": obs.get("chat") or [],
            "zone": {"center": list(centro), "radius": radio, "damage_per_s": dps}}


def _pack_sin(pack, idx):
    out = []
    for i, s in enumerate(pack):
        if i == idx and s:
            n = int(s.get("n") or 1) - 1
            out.append({**s, "n": n} if n > 0 else None)
        else:
            out.append(s)
    return out


def _pack_con(pack, item_id, n, mundo):
    out = list(pack)
    for i, s in enumerate(out):
        if s and s.get("id") == item_id:
            out[i] = {**s, "n": int(s.get("n") or 0) + n}
            return out
    for i, s in enumerate(out):
        if not s:
            out[i] = {"id": item_id, "n": n}
            return out
    return out          # zurron lleno: coger no cambia nada


def candidatos(obs, mundo, mem, tick, bloqueos=None):
    """Los candidatos DECLARADOS del prompt. Lista de (nombre, receta)."""
    you = obs.get("you") or {}
    vis = obs.get("visible") or {}
    pos = tuple(you.get("pos") or (0, 0))
    pack = list(you.get("pack") or [])
    hand = you.get("hand")
    cuerpo = you.get("body")
    id_cuerpo = cuerpo.get("id") if isinstance(cuerpo, dict) else cuerpo
    stats = you.get("stats") or {}
    hp = float(you.get("hp") or 0.0)
    hp_max = mem.hp_max or hp or 1.0
    speed = int(stats.get("speed") or 5)

    # el quieto se llama "noop": es el nombre que select_tiebreak excluye
    # de los empates (N2a "quieto no gana empates"). Con otro nombre, la
    # exclusion no se aplica y el agente se queda clavado en los empates.
    cands = [("noop", {"tipo": "quieto"})]

    # 1. mover en los 8 rumbos — ZANCADA: la mirada los proyecta hasta donde el
    #    enfriamiento deje llegar dentro de H (hoy, 4 casillas).
    #    PROMPT_28: no se ofrece la zancada cuya PRIMERA casilla es solida. El
    #    mundo la rechaza entera (`sim.nim:622-624`) y emitirla es quemar la
    #    ventana de movimiento. Es el precedente del `paso_*` (PROMPT_14)
    #    aplicado al unico verbo que no lo tenia. Solo se mira el PRIMER paso:
    #    es lo unico cierto ahora; lo que haya cuatro casillas mas alla es
    #    hipotesis, y de eso ya se encarga la foto (que ya no desliza).
    for d, (dx, dy) in DIRS.items():
        if mundo.solido(pos[0] + dx, pos[1] + dy):
            continue
        cands.append((f"move_{d}", {"tipo": "mover", "dir": d}))

    # 1b. PASO CORTO (PROMPT_14): los mismos 8 rumbos, pero de UNA casilla, y la
    #     mirada los proyecta a su medida real. Motivo medido en el 13 (s110):
    #     apartarse un paso partia por la mitad S-DANO-PAREJA (0,330 -> 0,165),
    #     pero el unico candidato de movimiento disponible era una zancada de 4
    #     casillas que salia del centro de la finale y encendia F-ANTICIPACION
    #     en su techo. El gesto media una casilla; el vocabulario solo sabia
    #     hablar de cuatro. Tambien lo piden la posicion fina en combate y el
    #     escondite. Solo se ofrecen los pasos a casilla PISABLE.
    #
    #     PISABLE son DOS hechos, los dos presentes y ciertos:
    #       - no es solido (`static_map`, leido del player_config), y
    #       - NO HAY NADIE ENCIMA. Es la misma regla que el mundo aplica y que
    #         el 13 nos enseno por las malas: en s110 el hermano intento entrar
    #         quince veces en la casilla del que le daba el regalo y el mundo
    #         devolvio `blocked` quince veces. Un cuerpo tapa la casilla igual
    #         que un muro. Ofrecer un paso hacia un cuerpo es ofrecer un
    #         `blocked`. (Declarado: la ocupacion es cierta AHORA; que el otro
    #         siga ahi el tic que viene es hipotesis, del lado prudente.)
    ocupadas = {tuple(a.get("pos") or ()) for a in (vis.get("agents") or [])}
    for d, (dx, dy) in DIRS.items():
        q = (pos[0] + dx, pos[1] + dy)
        if not mundo.solido(q[0], q[1]) and q not in ocupadas:
            cands.append((f"paso_{d}", {"tipo": "paso", "dir": d}))

    # 2. ir-hacia (botin conocido mejor valorado)
    # ocupacion VISIBLE ahora mismo: viaja con la receta para que la
    # imaginacion y las piernas usen exactamente el mismo hecho (PROMPT_15).
    cuerpos = frozenset(tuple(a.get("pos") or ()) for a in (vis.get("agents") or [])
                        if a.get("pos"))
    objetivo = _mejor_botin(pos, mundo, mem)
    if objetivo and objetivo != pos:
        cands.append(("ir_botin", {"tipo": "ir", "destino": objetivo,
                                   "cuerpos": cuerpos}))

    # 2b. ir-hacia (OBJETO CONCRETO mas valioso por valor/(1+dist)) — PROMPT_07 B.
    #     Medido en la tanda v3: en el 54,7 % de las decisiones con un objeto a
    #     <=3 casillas, el UNICO candidato de saqueo (`ir_botin`, argmax global)
    #     apuntaba a otro sitio, casi siempre a la camara. No existia ninguna
    #     opcion de ir a por lo que tenia al lado. Este candidato la crea.
    obj_cerca = _mejor_objeto(pos, mundo, mem, obs, tick)
    if obj_cerca and obj_cerca != pos:
        cands.append(("ir_objeto", {"tipo": "ir", "destino": obj_cerca,
                                    "cuerpos": cuerpos,
                                    "recoger": mem.objetos_vistos.get(obj_cerca)}))

    # 3. ir-hacia (centro de zona segura)
    centro, _r, _d = mundo.anillo_en(tick)
    if tuple(centro) != pos:
        cands.append(("ir_centro", {"tipo": "ir", "destino": tuple(centro),
                                    "cuerpos": cuerpos}))

    # 4. ir-hacia (pareja)
    if mem.pareja_pos and tuple(mem.pareja_pos) != pos and not mem.pareja_muerta:
        cands.append(("ir_pareja", {"tipo": "ir", "destino": tuple(mem.pareja_pos),
                                    "cuerpos": cuerpos}))

    # 5. coger (si hay objeto en la casilla)
    # A.1 CESION (PROMPT_13): lo que solte para la pareja herida ya no es mio;
    # mientras la cesion viva, `coger` no lo ve. Esto corta la oscilacion de
    # s107 (dar y recuperar 23 veces).
    aqui = [it for it in (vis.get("items") or [])
            if tuple(it.get("pos") or ()) == pos and pos not in mem.cedidos]
    if aqui:
        cands.append(("coger", {"tipo": "coger", "item": aqui[0]}))

    # 6. usar racion / botiquin (si procede: solo si hay dano que curar)
    if hp < hp_max:
        for i, s in enumerate(pack):
            if not s:
                continue
            it = mundo.items.get(s.get("id"))
            if it and it.kind == "ikConsumable" and it.heal > 0:
                nombre = "usar_botiquin" if s["id"] == mundo.id_botiquin else "usar_racion"
                if nombre not in [c[0] for c in cands]:
                    cands.append((nombre, {"tipo": "usar", "idx": i, "heal": it.heal}))

    # 6b. SOLTAR una cura junto a la pareja HERIDA (PROMPT_12). Disponible SOLO
    #     con pareja herida a la vista y objeto de cura en la mochila. Su valor
    #     NO esta escrito en ningun sitio: emerge de la atenuacion de
    #     S-DANO-PAREJA (la medicina junto a la cama) menos la perdida de W.
    #     Si no gana nunca, se reporta; no se fuerza.
    # PROMPT_59: el gesto tambien se abre en CALMA-PROVISION —hermana con b=0
    # por parte, yo con >=2 vendas, sin caza— para DAR ANTES. No es un
    # candidato nuevo (mismo `soltar`): es su disponibilidad ampliada, la cara
    # de actuacion de S-PROVISION. Detras de A.PROVISION_ON (v30 intacta).
    pareja = next((a for a in (vis.get("agents") or [])
                   if a.get("slot") == mundo.teammate_slot), None)
    _bot_real59 = sum(int(s.get("n") or 1) for s in pack
                      if s and s.get("id") == mundo.id_botiquin)   # UNIDADES (60)
    _prov59 = (A.PROVISION_ON and _bot_real59 >= A.PROVISION_B_MIN
               and A._hermana_b0(mem, tick)
               and A._provision_calma(obs.get("you") or {}, mundo, mem, tick))
    _herida59 = pareja is not None and \
        (pareja.get("hp_band") or "healthy") != "healthy"
    if _herida59 or _prov59:
        for i, sl in enumerate(pack):
            if not sl:
                continue
            it = mundo.items.get(sl.get("id"))
            if it and it.kind == "ikConsumable" and it.heal > 0:
                cands.append((f"soltar_{sl['id']}",
                              {"tipo": "soltar", "idx": i, "item": sl["id"],
                               "n": int(sl.get("n") or 1)}))
                break

    # 6c. EMPUNAR (PROMPT_13 B). Certificado en la fuente del mundo: el ataque
    #     usa `a.hand` y solo eso (sim.nim:902), y sin arma en mano cae en
    #     `else: discard` — no existe el punetazo. Empunar es automatico SOLO al
    #     coger con la mano vacia (sim.nim:713); si la mano ya lleva algo (una
    #     RED, dano 0), el arma buena se va al zurron y ahi se queda. Sacarla es
    #     un acto aparte: `use` sobre la ranura, que intercambia mano<->zurron
    #     (sim.nim:792). Su valor sale de R-2 (estar armado = arma EN LA MANO).
    d_mano = 0.0
    if hand:
        _im = mundo.items.get(hand.get("id"))
        d_mano = float(_im.damage) if _im else 0.0
    _mej_i, _mej_d, _mej_id = None, d_mano, None
    for i, sl in enumerate(pack):
        if not sl:
            continue
        it = mundo.items.get(sl.get("id"))
        if it and it.damage > _mej_d:
            _mej_i, _mej_d, _mej_id = i, float(it.damage), sl["id"]
    if _mej_i is not None:
        cands.append((f"empunar_{_mej_id}",
                      {"tipo": "empunar", "idx": _mej_i, "item": _mej_id}))

    # 6d. PONERSE una prenda (PROMPT_17 B). Certificado en la fuente:
    #     `resolvePickup` para `ikGear` equipa al cuerpo SOLO si el cuerpo esta
    #     vacio (`sim.nim:735: if a.body == iNone: a.body = g.item`); si ya
    #     llevas algo, la prenda se va al zurron y ahi se queda. Sacarla de ahi
    #     es un acto aparte: `use` sobre la ranura, que en `ikGear` viste el
    #     cuerpo EN EL ACTO, sin canal (`sim.nim:805-809`), y tira al suelo lo
    #     que llevaras puesto (`unequipBodyToGround`) — y, si era mochila,
    #     tambien lo que hubiera en las ranuras 2-3.
    #     Esto RESUELVE la contradiccion aparente: en s112 (tanda v4) parecio
    #     automatico porque el cuerpo estaba vacio; en la tanda larga del 16
    #     no hubo ni un tic camuflado porque nunca llego una prenda al zurron.
    #     NO SE LEGISLA NADA: su valor sale de filas que ya existen — S-8, que
    #     el camuflaje apaga, y el granero de W, que la mochila agranda.
    for i, sl in enumerate(pack):
        if not sl:
            continue
        it = mundo.items.get(sl.get("id"))
        if it is None or it.kind != "ikGear":
            continue
        if id_cuerpo == sl["id"]:
            continue                       # ya la llevo puesta
        cands.append((f"ponerse_{sl['id']}",
                      {"tipo": "ponerse", "idx": i, "item": sl["id"],
                       "cuerpo_previo": id_cuerpo}))

    # 7. LEGITIMA DEFENSA (S-7, PROMPT_09): responder SOLO a un AGRESOR ACTIVO
    #    que este a alcance del arma en mano. Nunca se inicia: si el otro no me
    #    ha danado dentro de la ventana, el candidato NI SIQUIERA EXISTE.
    #    Sin excepcion para la pareja: si te dana, es agresor (las filas S de
    #    pareja pesan en contra por si solas; aqui no se escribe nada especial).
    #    LA MANADA (PROMPT_63): tambien es agresor activo el CERTIFICADO de mi
    #    hermana (su parte fresco a=1 con ax,ay + enemigo visible ahi, tol 1).
    #    No es un candidato nuevo: es el mismo `responder` con un motivo mas.
    #    Jamas contra ella (C1) ni contra quien no ha agredido a ninguna (C2).
    arma = mundo.items.get((hand or {}).get("id")) if hand else None
    _agr_herm = A.agresor_de_la_hermana(obs, mundo, mem, tick)
    if arma is not None and arma.damage > 0:
        for a in vis.get("agents") or []:
            sl = a.get("slot")
            if sl == mundo.slot:
                continue
            e = mem.agresores.get(sl)
            _mio = bool(e) and (tick - e["ultimo"]) <= A.AGRESOR_VENTANA_S * mundo.tick_rate
            _suyo = (sl == _agr_herm)
            if not _mio and not _suyo:
                continue                       # no es agresor activo -> sin candidato
            q = tuple(a.get("pos") or ())
            if not q:
                continue
            dx, dy = q[0] - pos[0], q[1] - pos[1]
            alineado = (dx == 0 or dy == 0 or abs(dx) == abs(dy))
            if alineado and max(abs(dx), abs(dy)) <= arma.range:
                d = _dir_hacia(pos, q)
                if d and f"atacar_{d}" not in [c[0] for c in cands]:
                    cands.append((f"atacar_{d}", {"tipo": "atacar", "dir": d,
                                                  "objetivo": sl, "arma": arma}))
    if bloqueos is not None:
        # ARREGLO A: fuera los que no pueden ejecutarse todavia. `noop` nunca se
        # veta: siempre tiene que quedar algo que emitir.
        cands = [c for c in cands
                 if c[0] == "noop" or not bloqueos.veta(c[0], obs, tick)]
    return cands


def mirada(mundo, tick) -> int:
    """Tics que se preven. Hasta el PLAZO del anillo, acotado por el horizonte
    de 20 s que la tabla sella (ANT_HORIZONTE_S) y con suelo H_MIRADA_MIN."""
    tope = int(A.ANT_HORIZONTE_S * mundo.tick_rate)
    prox = A._proximo_encogimiento(mundo, tick)
    if prox is None:
        return H_MIRADA_MIN
    return max(H_MIRADA_MIN, min(tope, prox[0] - tick))


def _promesa(obs, mundo, mem, tick, item_id):
    """LA PROMESA DEL OBJETO [Manel, sellada — PROMPT_18].

    Alivio PROSPECTIVO de la fila que este objeto apaga, medido por PREVISION
    con la misma cadena de siempre: se construye la observacion con el objeto
    ya en su sitio y se resta la M de la fila. NO hay ninguna constante nueva:
    el numero sale de una fila que ya existe.

      - camuflaje -> S-8 EXPOSICION. Si S-8 duele 0, la promesa es 0: la
        prenda no llama. "Es alivio, no fetiche."
      - mochila   -> el granero de W (R-CARENCIA). Su promesa es cuanto sube W.

    La letra pequena del 17 va dentro: con el CUERPO VACIO, recoger ES vestir
    (`resolvePickup`, rama ikGear); con el cuerpo ocupado la prenda cae al
    zurron y el alivio queda a un acto de distancia (`ponerse_`, PROMPT_17) —
    en ese caso la promesa se cuenta igual, porque el acto existe y es gratis
    salvo el canal. Declarado.

    Devuelve 0.0 para todo lo que no tenga fila conocida: fuera de su caso el
    cambio es inerte.
    """
    it = mundo.items.get(item_id)
    # PROMPT_46: el BOTIQUIN apaga R-ACOPIO. Mismo patron sellado del 18 (la
    # prevision con el objeto ya en su sitio; el numero sale de la fila).
    if item_id == mundo.id_botiquin:
        you = obs.get("you") or {}
        pack = list(you.get("pack") or [])
        if any(s2 and s2.get("id") == mundo.id_botiquin for s2 in pack):
            return 0.0                  # servido: la promesa calla
        try:
            hueco = pack.index(None)
        except ValueError:
            return 0.0                  # zurron lleno: no es adquirible
        y2 = dict(you); p2 = list(pack); p2[hueco] = {"id": item_id, "n": 1}
        y2["pack"] = p2
        ob2 = dict(obs); ob2["you"] = y2
        F0 = A.filas(obs, mundo, mem, tick)
        F1 = A.filas(ob2, mundo, mem, tick)
        return max(0.0, (F0.get("R-ACOPIO") or 0.0) - (F1.get("R-ACOPIO") or 0.0))
    if it is None or it.kind != "ikGear":
        return 0.0
    you = obs.get("you") or {}
    cuerpo = you.get("body")
    id_cuerpo = cuerpo.get("id") if isinstance(cuerpo, dict) else cuerpo
    if id_cuerpo == item_id:
        return 0.0                      # ya la llevo puesta
    ob2 = dict(obs)
    y2 = dict(you)
    # el mundo publica `body` como CADENA (medido en los logs: 'backpack'),
    # y `riqueza_W` lo compara como cadena. La prevision usa ese mismo formato.
    y2["body"] = item_id
    ob2["you"] = y2
    if item_id == mundo.id_camuflaje:
        F0 = A.filas(obs, mundo, mem, tick)
        F1 = A.filas(ob2, mundo, mem, tick)
        return max(0.0, (F0.get("S-8-EXPOSICION") or 0.0)
                   - (F1.get("S-8-EXPOSICION") or 0.0))
    if item_id == mundo.id_mochila:
        W0, _ = A.riqueza_W(you, mundo)
        W1, _ = A.riqueza_W(y2, mundo)
        return max(0.0, W1 - W0)
    return 0.0


def _mejor_objeto(pos, mundo, mem, obs=None, tick=0):
    """Objeto CONCRETO y recogible mas valioso, por valor/(1+dist) (PROMPT_07 B).

    Solo cuenta lo que `coger` puede tomar: objetos del suelo vistos o
    recordados. La camara y las bocas NO entran aqui: son sitios, no botin que
    se pueda meter en el zurron. El criterio valor/(1+dist) es el del encargo.

    PROMPT_18: al nivel de la casilla se le suma LA PROMESA del objeto (ver
    `_promesa`). `VALOR_NIVEL` se queda para el botin generico.
    """
    mejor, p_mejor = 0.0, None
    for p, (_id, _n, niv) in mem.objetos_vistos.items():
        if p in mem.cedidos:          # A.1: un regalo no es un objetivo mio
            continue
        val = niv
        if obs is not None:
            val += _promesa(obs, mundo, mem, tick, _id)
        v = val / (1.0 + math.dist(pos, p))
        if v > mejor:
            mejor, p_mejor = v, p
    return p_mejor


def _mejor_botin(pos, mundo, mem):
    """Objetivo de la llamada del botin: el MEJOR VALORADO por la tabla.

    El tope sellado (CAP 0.25) se aplica a la MAGNITUD de la fila, no al ORDEN
    de los objetivos: se ordena por el valor SIN topar. Lectura literal de la
    tabla ("M = valor_nivel x (1 - dist/24), CAP GLOBAL = 0.25": el cap va sobre
    M). Efecto: manda la camara de la Fortaleza (valor_nivel 1.0), que ESTA en
    el centro, asi que codicia y anillo tiran del mismo lado.

    NOTA DE HONESTIDAD: se probo tambien ordenar por el valor TOPADO con empates
    resueltos por cercania. NO se puede atribuir la diferencia de conducta entre
    ambas variantes a partir de un episodio por variante: el agente NO es
    reproducible corrida a corrida (ver acta, seccion de la carrera repetidor/tick).
    """
    mejor, p_mejor = 0.0, None
    for p, niv in mem.fuentes():
        v = niv * max(0.0, 1.0 - math.dist(pos, p) / A.BOTIN_DIST_REF)
        if v > mejor:
            mejor, p_mejor = v, p
    return p_mejor


def decide(obs, mundo, mem, tick, bloqueos=None):
    """El ciclo completo. Devuelve (accion_json, radiografia_de_la_decision)."""
    you = obs.get("you") or {}
    pos = tuple(you.get("pos") or (0, 0))
    hp = float(you.get("hp") or 0.0)
    hp_max = mem.hp_max or hp or 1.0
    pack = list(you.get("pack") or [])
    hand = you.get("hand")
    cuerpo = you.get("body")
    id_cuerpo = cuerpo.get("id") if isinstance(cuerpo, dict) else cuerpo
    stats = you.get("stats") or {}
    speed = int(stats.get("speed") or 5)
    radio_vis = mundo.radio_vision(stats.get("intelligence", 5))
    H = mirada(mundo, tick)

    cands = candidatos(obs, mundo, mem, tick, bloqueos)
    terminal, meta, detalle = {}, {}, {}
    nombres = [c[0] for c in cands]

    # PROMPT_47: ¿hay AHORA un agresor activo visible a bocajarro (< D0)?
    # Se decide sobre la obs REAL y viaja a todas las fotos: con el agresor
    # lejos, ninguna foto enciende el muro (P2 por construccion).
    _muro_on = False
    for _a in (obs.get("visible") or {}).get("agents") or []:
        _e = mem.agresores.get(_a.get("slot"))
        if not _e or (tick - _e["ultimo"]) > A.AGRESOR_VENTANA_S * mundo.tick_rate:
            continue
        if _a.get("pos") and math.dist(pos, tuple(_a["pos"])) < A.MURO_D0:
            _muro_on = True
            break

    # PROMPT_59: las vendas REALES a bordo, para S-PROVISION/R-ACOPIO-por-dos.
    # Se cuenta sobre la obs REAL y viaja a todas las fotos: asi la foto del
    # soltar (que baja el pack) no borra el malestar por si sola — solo lo
    # alivia una entrega servible (patron de _muro_on).
    # UNIDADES, no slots (PROMPT_60): el botiquin se APILA (n>=2 en un slot).
    # Contar slots daba _bot_real=1 con una pila de 2 -> S-PROVISION muda en el
    # campo. Bug de banco (el 59 uso dos slots n=1); el campo lo destapo.
    _bot_real = sum(int(_s.get("n") or 1)
                    for _s in (obs.get("you") or {}).get("pack") or []
                    if _s and _s.get("id") == mundo.id_botiquin)
    # PROMPT_61: el hp REAL, para distinguir en la foto quien REGALO la venda
    # (hp sin cambiar) de quien la USO (hp sanado). Solo el que regala herido
    # paga la cuesta.
    _hp_real = float((obs.get("you") or {}).get("hp") or 0.0)

    for nombre, receta in cands:
        t = receta["tipo"]
        p2, hp2, pack2, hand2 = pos, hp, pack, hand
        body2 = False                      # False = el cuerpo no cambia
        n_moves = 0
        # PROMPT_54: `suelta` se inicializa AQUI. Antes se reseteaba a None
        # despues del despacho (bug: la foto de `soltar` nunca llevaba el
        # objeto al suelo). Era INERTE hasta hoy — la medicina lo habria
        # rechazado igual (A.2: mi casilla, ocupada) — pero el alivio de
        # S-HERIDO lee la cesion en la foto y lo necesita puesto.
        suelta = None
        if t == "mover":
            p2 = _simula_camino(pos, receta["dir"], mundo, speed, H, False)
            n_moves = int(math.dist(pos, p2))
        elif t == "paso":
            # a su medida real: UNA casilla. La casilla ya se comprobo pisable
            # al construir el candidato (solidos: ciertos).
            dx, dy = DIRS[receta["dir"]]
            p2 = (pos[0] + dx, pos[1] + dy)
            n_moves = 1
        elif t == "ir":
            campo = campo_geodesico(mundo, receta["destino"])
            receta["campo"] = campo
            p2 = (_camina_geodesica(pos, campo, mundo, speed, H, receta["destino"],
                                    receta.get("cuerpos") or ())
                  if campo
                  else _simula_camino(pos, receta["destino"], mundo, speed, H, True))
            n_moves = int(math.dist(pos, p2))
            # PROMPT_07 B: si el candidato LLEGA al objeto, se prevé tambien que
            # lo recoge. Sin esto el candidato solo vale por la casilla, y la
            # casilla de un cajon no vale nada: lo que vale es el objeto. NO es
            # cierto (otro puede llevarselo antes); es la misma hipotesis
            # declarada de congelacion que ya usa el evaluador. Declarado.
            rec = receta.get("recoger")
            if rec and p2 == receta["destino"]:
                _it = mundo.items.get(rec[0])
                if _it is not None and _it.kind == "ikGear" and not id_cuerpo:
                    # PROMPT_17/18: con el cuerpo vacio, coger ES vestir
                    # (`sim.nim`, resolvePickup rama ikGear). CIERTO.
                    body2 = rec[0]          # cadena: formato del mundo
                else:
                    pack2 = _pack_con(pack, rec[0], rec[1], mundo)
        elif t == "coger":
            it = receta["item"]
            pack2 = _pack_con(pack, it.get("id"), int(it.get("n") or 1), mundo)
        elif t == "soltar":
            pack2 = _pack_sin(pack, receta["idx"])
            suelta = (receta["item"], pos)     # cae en MI casilla
        elif t == "usar":
            hp2 = min(hp_max, hp + receta["heal"])
            pack2 = _pack_sin(pack, receta["idx"])
            # PROMPT_46: gastar el BOTIQUIN para curarse no es pobreza — la
            # foto lo marca y R-ACOPIO calla (patron de `_hp_est`, 23).
            _sl = pack[receta["idx"]] if receta["idx"] < len(pack) else None
            if _sl and _sl.get("id") == mundo.id_botiquin:
                receta["_cura"] = True
        elif t == "ponerse":
            # CIERTO (sim.nim:805-809): la prenda pasa al cuerpo, la ranura
            # queda vacia, y lo que llevara puesto cae al suelo. Si lo que
            # llevaba era mochila, ademas se pierden las ranuras 2-3: eso lo
            # descuenta el propio zurron previsto.
            pack2 = list(pack)
            pack2[receta["idx"]] = None
            if receta.get("cuerpo_previo") == mundo.id_mochila:
                pack2 = (pack2 + [None, None, None, None])[:2]
            body2 = receta["item"]          # cadena: formato del mundo
        elif t == "empunar":
            # el mundo intercambia mano y ranura (sim.nim:792-795): CIERTO.
            pack2 = list(pack)
            sl = pack2[receta["idx"]]
            pack2[receta["idx"]] = dict(hand) if hand else None
            hand2 = dict(sl)
        # ATACAR: el estado PROPIO no cambia; lo que cambia es el hp previsto del
        # agresor, y por ahi baja S-7. El dano propio es CIERTO (catalogo del
        # mundo + multiplicador de fuerza del README: melee x(5+STR)/10). La
        # ESQUIVA AJENA NO SE PREDICE: hipotesis declarada, del lado optimista.
        golpe = None
        if t == "atacar":
            arma = receta["arma"]
            dmg = arma.damage * ((5 + int(stats.get("strength") or 1)) / 10.0) \
                if arma.kind == "ikMelee" else float(arma.damage)
            _obj = receta["objetivo"]
            # EL FUEGO AMIGO (PROMPT_65): cuando el golpe ATRAVIESA casillas
            # (alcance > 1), el mundo pega al PRIMER cuerpo de la linea, no al
            # que yo apunto. El campo del 64 lo cobro: 3 de los 4 golpes entre
            # hermanas salieron de una defensa que encontro antes a la
            # defendida — y la foto REAL medida (`ereq_feafe3ac` t534) fue con
            # LANZA (melee de rango 2), no con proyectil: por eso la condicion
            # es el ALCANCE, no el tipo de arma. La FOTO tiene que decir esa
            # verdad; entonces S-DANO-PAREJA y S-VINCULO —que ya existen—
            # pesan contra ese golpe solas. Sin regla nueva (R2).
            if A.FUEGO_AMIGO_ON and arma.range > 1:
                _v = _primero_en_linea(pos, _obj, obs, mundo)
                if _v is not None:
                    _obj = _v
            golpe = (_obj, dmg)
        # "quieto": el estado propio previsto no cambia (declarado)

        ver_pareja = bool(mem.pareja_pos) and not mem.pareja_muerta and \
            math.dist(p2, mem.pareja_pos) <= radio_vis
        ob2 = _obs_prevista(obs, mundo, mem, tick, p2, hp2, pack2, hand2, ver_pareja,
                            golpe, suelta, body2)
        if receta.pop("_cura", None):
            ob2["you"]["_cura_en_curso"] = True     # PROMPT_46, solo en la foto
        ob2["you"]["_muro_on"] = _muro_on           # PROMPT_47: bocajarro REAL
        ob2["you"]["_bot_real"] = _bot_real         # PROMPT_59: vendas reales
        ob2["you"]["_hp_real"] = _hp_real           # PROMPT_61: hp real
        st, radio = A.appraise(ob2, mundo, mem, tick)
        d = round(opponent_distance(st, DEFAULT_CONFIG), _ROUND)
        terminal[nombre] = d
        meta[nombre] = (n_moves, 0)
        detalle[nombre] = {"d": d, "pos_prevista": list(p2), "hp_prevista": hp2,
                           "movs": n_moves,
                           "filas": {k: v["M"] for k, v in radio["filas"].items()
                                     if v.get("M")}}

    # desempate: la jerarquia firmada de la casa (planificador_v1.select_tiebreak).
    # preds = terminal: con tie_unified=True la rama que usa la d-de-1-paso no se
    # ejecuta salvo en el fallback del paisaje degenerado, donde queda inerte.
    preds = {a: {"d": terminal[a]} for a in nombres}
    elegido = select_tiebreak(nombres, preds, terminal, meta,
                              attractor=None, action_deltas=None,
                              exclude_noop=True, tie_unified=True)

    receta = dict(cands)[elegido]
    # A.1: al soltar bajo la condicion de medicina el objeto queda CEDIDO.
    # (el candidato `soltar` SOLO existe con pareja viva y herida a la vista,
    #  asi que soltar == ceder por construccion; ver candidatos() 6b.)
    if receta["tipo"] == "soltar":
        mem.cedidos[pos] = {"item": receta["item"], "tick": tick}
    elif receta["tipo"] == "atacar":
        # PROMPT_16: atacar delata al camuflado. Se apunta aqui, que es donde
        # se sabe de cierto que se ataca.
        mem.ultimo_ataque = tick
    accion = _a_json(elegido, receta, pos, mundo, mem, tick)
    honor = None
    if receta["tipo"] == "atacar":
        sl = receta["objetivo"]
        e = mem.agresores.get(sl)
        _mio_h = bool(e) and (tick - e["ultimo"]) <= A.AGRESOR_VENTANA_S * mundo.tick_rate
        # PROMPT_63: el motivo queda DECLARADO en la radiografia — defenderme
        # (era_agresor) o defenderla (defensa_pareja). Las dos metricas de
        # honor del campo se cuentan de aqui: iniciacion-estricta = ninguno
        # de los dos motivos (jamas debe ocurrir, C2).
        honor = {"objetivo": sl,
                 "era_agresor": _mio_h,
                 "defensa_pareja": (sl == A.agresor_de_la_hermana(obs, mundo,
                                                                  mem, tick)),
                 "dano_recibido_de_el": round(e["dano"], 1) if e else 0.0,
                 "es_la_pareja": sl == mundo.teammate_slot}
    spread = max(terminal.values()) - min(terminal.values())
    return accion, {"elegido": elegido, "accion": accion, "mirada_ticks": H,
                    "n_cand": len(cands), "honor": honor,
                    "spread": round(spread, 5), "candidatos": detalle}


def _a_json(nombre, receta, pos, mundo, mem, tick):
    t = receta["tipo"]
    if t == "quieto":
        return {"type": "action", "do": "none"}
    if t in ("mover", "paso"):
        return {"type": "action", "do": "move", "dir": receta["dir"]}
    if t == "ir":
        # el paso emitido SIGUE la geodesica: si la imaginacion rodea el muro,
        # las piernas tienen que rodearlo tambien.
        campo = receta.get("campo") or campo_geodesico(mundo, receta["destino"])
        cuerpos = receta.get("cuerpos") or ()
        d = _paso_geodesico(pos, campo, receta["destino"], cuerpos) if campo else None
        if d is None and not campo:
            d = _dir_hacia(pos, receta["destino"])      # degradacion a linea recta
        if d is not None:
            dx, dy = DIRS[d]
            if (pos[0] + dx, pos[1] + dy) in set(cuerpos):
                d = None               # ni la degradacion embiste a nadie
        return ({"type": "action", "do": "move", "dir": d} if d
                else {"type": "action", "do": "none"})
    if t == "coger":
        return {"type": "action", "do": "pickup"}
    if t in ("usar", "empunar", "ponerse"):
        return {"type": "action", "do": "use", "slot": receta["idx"]}
    if t == "soltar":
        return {"type": "action", "do": "drop", "slot": receta["idx"]}
    if t == "atacar":
        return {"type": "action", "do": "attack", "dir": receta["dir"]}
    return {"type": "action", "do": "none"}
