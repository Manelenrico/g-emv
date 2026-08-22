"""
planificador_v1 — lookahead corto de N pasos (horizonte rodante, sin aprendizaje).

Spec: [doc de diseño interna, no en el repo]
Motor: motor/model.py INTOCABLE. Reutiliza las primitivas de predicción de gemv_policy
(vía `ctx`) para garantizar que H=1 reproduce la política greedy bit-a-bit.

Valoración de un camino = d TERMINAL (estado tras H pasos), no suma de d intermedias.
Desempate: (1) min d terminal, (2) min d del primer paso, (3) orden de action_names (noop primero).
Mundo estático durante los H pasos. Celdas no vistas = vacías (salvo memoria ON).

Optimización: memoización por estado. Con memoria OFF la d terminal depende solo de los
tokens → estados repetidos (p.ej. N seguido de S) se evalúan una vez. Con memoria ON la clave
incluye (tokens, desplazamiento acumulado, profundidad) porque el ghost depende de la posición.
`use_cache=False` fuerza enumeración pura (test de equivalencia).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

_INF = float("inf")
_ROUND = 5          # misma precisión que preds/d del log greedy
_TOL = 1e-9


@dataclass
class PlanCtx:
    """Primitivas de predicción, inyectadas desde gemv_policy (evita import circular)."""
    shift_tokens: Callable      # (tokens, scalar_map, drow, dcol, energy_cost) -> tokens
    dest_is_blocked: Callable   # (tag_map, action) -> bool
    parse_tokens: Callable      # (tokens) -> (scalar_map, tag_map)
    appraise: Callable          # (tokens, team_side, s_scale) -> State
    apply_ghost: Callable       # (State, ghost) -> State
    opponent_distance: Callable # (State, config) -> float
    config: object
    action_deltas: dict         # action -> (drow, dcol)
    move_energy_cost: int
    padding_loc: int
    # D2 (Lab 1.2b) — previsión de MAPA: territorio del ventana reconstruido (dict (row,col)->terr),
    # usado para fijar territory:here predicho en el terminal según el desplazamiento acumulado.
    terr_map: dict = None
    terr_here_fid: int = 0
    global_loc: int = 254
    # Autopsia (Lab 1.2c): callable(first_action, cdr, cdc, d, state, terr_terminal) para cada terminal.
    autopsy: object = None
    # v6b — fid_p0 de energía del agente (para N2: energía terminal en el desempate). None ⇒ energía=0.
    fid_energy: int = None
    agent_loc: int = 102


def _token_key(tokens) -> tuple:
    return tuple(sorted((int(t[0]), int(t[1]), int(t[2])) for t in tokens))


def _mp_at(tokens, loc, fid_p0) -> int:
    """Valor multipart (p0/p1) del agente en (loc, fid_p0). Para leer inv:aligner/inv:heart
    del terminal (Córtex C2). fid_p0 None ⇒ 0 (inerte)."""
    if fid_p0 is None:
        return 0
    p0 = p1 = 0
    for t in tokens:
        if int(t[0]) == loc and int(t[1]) == fid_p0: p0 = int(t[2])
        elif int(t[0]) == loc and int(t[1]) == fid_p0 + 1: p1 = int(t[2])
    return p0 + 256 * p1


def _energy_of(tks, ctx: PlanCtx) -> int:
    """Energía del agente en los tokens (multipart p0/p1). 0 si no hay fid declarado (N2 inerte)."""
    if ctx.fid_energy is None:
        return 0
    p0 = p1 = 0
    for t in tks:
        if int(t[0]) == ctx.agent_loc and int(t[1]) == ctx.fid_energy: p0 = int(t[2])
        elif int(t[0]) == ctx.agent_loc and int(t[1]) == ctx.fid_energy + 1: p1 = int(t[2])
    return p0 + 256 * p1


def plan_terminal(
    tokens, scalar_map, tag_map, action_names, team_side, mem, H, s_scale, ctx: PlanCtx,
    use_cache: bool = True, trans_ctx=None, world_step: int = 0, virtual_extractors=None,
    track_meta: bool = False, virtual_hub=None, chain=None, gain=None, rollout_discount=None,
    gain_field=None, commit_k=None, gain_solids=None, cone_prune=None, cone_dryrun=None,
):
    """Devuelve (terminal_d: dict[action -> float], stats: dict).

    terminal_d[a] = mínima d terminal alcanzable ejecutando `a` como primer paso y luego
    hasta H-1 pasos más (mundo estático). Redondeada a _ROUND (consistente con el log greedy).

    Si trans_ctx != None (Fase 3b), el modelo de transición reescribe el inventario del
    estado simulado (mecánica del juego) tras cada paso, antes de appraise.

    Córtex C2 (chain != None, GEMV_CHAIN): la imaginación ENCADENA equip→align. chain =
    (credito, had_aligner, fid_aligner, fid_heart). En un terminal donde el agente ha
    completado la transición-medio (aligner NUEVO ⇒ inv:aligner≥1 ∧ not had_aligner) y el
    align es alcanzable (heart≥1), se RESTA `credito` de la d terminal: el Δd del align ya
    modelado (balda territorial R+S), propagado hacia atrás y ya descontado por confianza y
    distancia aguas arriba. Propaga valor existente; no crea valor. Sin chain ⇒ bit-exact.

    GEMV_ROLLOUT_DISCOUNT (rollout_discount = γ, 2026-07-18): el crédito de la transición (equipar,
    que ya empaqueta el Δd del align vía `chain`) se descuenta γ^k según el PASO k del rollout donde
    se ejecutó el equip (aligner 0→1). "Equipar ya" (k=1) vale más que "equipar en 7 pasos" por
    construcción → el compromiso emerge del valor bien descontado, no de reglas de adyacencia. γ es la
    misma CHAIN_GAMMA de C2. rollout_discount=None ⇒ crédito plano en el terminal (bit-exact con antes).
    """
    stats = {"n_terminal": 0, "n_nodes": 0}
    memo: dict = {}
    _apply_trans = None
    _station = None
    _virt_harvest = None
    _virt_deposit = None
    if trans_ctx is not None:
        from planificador.transicion_v1 import apply_transition as _apply_trans
        from planificador.transicion_v1 import station_bump_effect as _station
        from planificador.transicion_v1 import harvest_virtual as _virt_harvest
        from planificador.transicion_v1 import deposit_virtual as _virt_deposit

    # GEMV_ROLLOUT_DISCOUNT — fid del inv:aligner (para detectar el equip 0→1 en un paso del rollout).
    # Solo se consulta con rollout_discount != None (OFF ⇒ nunca se llama ⇒ bit-exact).
    _rd_fid_alig = chain[2] if (rollout_discount is not None and chain is not None) else None

    def _equipped_this_step(tks_before, ntks_after) -> bool:
        """True si el aligner pasó de 0 a ≥1 en este paso (se ejecutó la transición equipar)."""
        if _rd_fid_alig is None:
            return False
        return (_mp_at(tks_before, ctx.agent_loc, _rd_fid_alig) < 1
                and _mp_at(ntks_after, ctx.agent_loc, _rd_fid_alig) >= 1)

    def terminal_d(tks, cdr, cdc, depth, equip_depth=None):
        stats["n_terminal"] += 1
        # D2 — previsión de mapa: fija territory:here predicho (GLOBAL_LOC) según el mapa del
        # ventana en el desplazamiento acumulado (cdr,cdc). El mapa cubre ±6 (D1); fuera, se deja.
        terr_terminal = None
        if ctx.terr_map is not None:
            from planificador.mapa_territorial import AGENT_ROWCOL
            ar, ac = AGENT_ROWCOL
            if (ar + cdr, ac + cdc) in ctx.terr_map:
                terr_terminal = ctx.terr_map[(ar + cdr, ac + cdc)]
                tks = [t for t in tks
                       if not (int(t[0]) == ctx.global_loc and int(t[1]) == ctx.terr_here_fid)]
                tks.append((ctx.global_loc, ctx.terr_here_fid, terr_terminal))
        s = ctx.appraise(tks, team_side, s_scale=s_scale)
        if mem is not None:
            ar, ac = mem.agent_world
            ghost = mem.ghost_forces_for_position(ar + cdr, ac + cdc, mem._step + depth)
            s = ctx.apply_ghost(s, ghost)
        d = ctx.opponent_distance(s, ctx.config)
        # Córtex C2 — crédito de cadena: si en este terminal se equipó (aligner NUEVO) y el align
        # es alcanzable (heart portado), propaga hacia atrás el Δd del align (ya modelado), descontado
        # aguas arriba por confianza·γ^D. El planner VE así el retorno de equipar (fuerza-d territorial).
        if chain is not None:
            credit, had_aligner, fid_alig, fid_heart = chain
            if credit > 0.0 and not had_aligner:
                alig = _mp_at(tks, ctx.agent_loc, fid_alig)
                if alig >= 1 and _mp_at(tks, ctx.agent_loc, fid_heart) >= 1:
                    # ROLLOUT_DISCOUNT: γ^k según el paso del rollout donde se equipó (equip_depth);
                    # si aligner≥1 pero equip_depth es None (equipó al no-rastrear ⇒ solo OFF), crédito plano.
                    if rollout_discount is not None and equip_depth is not None:
                        d -= credit * (rollout_discount ** equip_depth)
                    else:
                        d -= credit
        # Córtex C4 — FUERZA-d de oportunidad: el Δd del align propagado a CADA terminal por proximidad a
        # la gear (γ^L1). El terminal más cercano vale más ⇒ gradiente continuo (fuerza, no susurro N3).
        # Empates N/E se rompen por orden (norte antes que este) ⇒ vertical-primero emerge (arregla la deriva).
        if gain is not None:
            grel, gscal, ggamma = gain
            if gscal > 0.0:
                # GEODESIA (GEMV_GEODESIC): la distancia del terminal a la gear/junction es el CAMINO MÁS CORTO
                # sobre el mapa conocido (muros/estaciones conocidos bloquean; lo no visto se asume caminable),
                # NO la L1 ciega-al-muro. gain_field[(cdr,cdc)] = geodésica precomputada (BFS); fuera de rango →
                # L1 de respaldo. OFF (gain_field None) ≡ L1 bit-exact.
                # FIX FANTASMA DEL MURO (gain_solids != None, GEMV_GEO_WALL_INF): una celda AUSENTE del campo se
                # separa en dos casos — SÓLIDA conocida (muro perc./record., en gain_solids) → 1e9 (excluida,
                # NO recibe la recta); NO explorada → L1 (optimismo epistémico intacto). gain_solids=None ≡ get(cell,L1).
                if gain_field is not None:
                    if (cdr, cdc) in gain_field:
                        dist = gain_field[(cdr, cdc)]
                    elif gain_solids is not None and (cdr, cdc) in gain_solids:
                        dist = 1e9                                     # sólido conocido: fuera de la competición
                    else:
                        dist = abs(grel[0] - cdr) + abs(grel[1] - cdc) # no explorada: L1
                else:
                    dist = abs(grel[0] - cdr) + abs(grel[1] - cdc)   # L1 del terminal a la gear
                d -= gscal * (ggamma ** dist)
        if ctx.autopsy is not None:
            ctx.autopsy(cdr, cdc, d, s, terr_terminal)
        return d

    def step(tks, sm, tm, action, depth, cdr=0, cdc=0):
        """(new_tokens, (ddr,ddc)) tras una acción. Blocked/noop => sin desplazamiento.

        depth = profundidad del estado resultante (1..H); se pasa al modelo de transición
        para la fase día/noche del solar. cdr/cdc = desplazamiento acumulado (para extractor virtual)."""
        delta = ctx.action_deltas.get(action, (0, 0))
        # 1d-bis: EXTRACTOR VIRTUAL (recordado, fuera de ventana). Si el move llega a su celda (desplazamiento
        # destino == posición relativa del recordado), el agente lo BUMPEA: se queda y cosecha (held+), igual
        # que uno percibido. El planner lo prevé donde la percepción lo haría. Alcance = horizonte (no más).
        if virtual_extractors and delta != (0, 0):
            dest = (cdr + delta[0], cdc + delta[1])
            for (vr, vc, inv_fid) in virtual_extractors:
                if (vr, vc) == dest:
                    ntks = [t for t in tks if int(t[0]) != ctx.padding_loc]
                    ntks = _virt_harvest(ntks, inv_fid, trans_ctx)
                    if _apply_trans is not None:
                        ntks = _apply_trans(ntks, action, world_step, depth, trans_ctx)
                    return ntks, (0, 0)
        # Eslabón 2 — HUB VIRTUAL recordado (espejo del extractor virtual): si el move alcanza la celda
        # del hub recordado, el agente bumpea y DEPOSITA (held→0, team+=). Da gradiente de d hacia el hub
        # aunque esté fuera de ventana/horizonte → descongela la vuelta a H=4. Sin carga → deposit_virtual inerte.
        if virtual_hub is not None and _virt_deposit is not None and delta != (0, 0):
            dest = (cdr + delta[0], cdc + delta[1])
            if (virtual_hub[0], virtual_hub[1]) == dest:
                ntks = [t for t in tks if int(t[0]) != ctx.padding_loc]
                nt2 = _virt_deposit(ntks, trans_ctx)
                if nt2 is not ntks:   # hubo depósito (llevaba carga)
                    if _apply_trans is not None:
                        nt2 = _apply_trans(nt2, action, world_step, depth, trans_ctx)
                    return nt2, (0, 0)
        # v2/extract: choque con estación (extractor demandado / hub propio con carbon) ⇒ el agente NO
        # avanza y la transición aplica el efecto (cosecha / depósito). Estructura de búsqueda intacta.
        if _station is not None:
            bumped, _kind = _station(tks, action, trans_ctx)
            if bumped is not None:
                ntks = [t for t in bumped if int(t[0]) != ctx.padding_loc]
                ntks = _apply_trans(ntks, action, world_step, depth, trans_ctx)
                return ntks, (0, 0)
        if delta == (0, 0) or ctx.dest_is_blocked(tm, action):
            ntks = [t for t in tks if int(t[0]) != ctx.padding_loc]
            move = (0, 0)
        else:
            drow, dcol = delta
            ntks = ctx.shift_tokens(tks, sm, drow, dcol, ctx.move_energy_cost)
            move = (drow, dcol)
        if _apply_trans is not None:
            ntks = _apply_trans(ntks, action, world_step, depth, trans_ctx)
        return ntks, move

    def best_from(tks, cdr, cdc, depth, k, equip_depth=None):
        """min d terminal alcanzable con k pasos restantes desde este estado.

        equip_depth (ROLLOUT_DISCOUNT): profundidad del rollout en que se ejecutó el equip aguas arriba
        (None hasta que ocurre). Se propaga a terminal_d para descontar el crédito γ^equip_depth."""
        if k == 0:
            return terminal_d(tks, cdr, cdc, depth, equip_depth)
        stats["n_nodes"] += 1
        key = None
        if use_cache:
            if rollout_discount is not None:
                # el valor depende de CUÁNDO se equipó (equip_depth) además del estado/posición.
                key = (_token_key(tks), cdr, cdc, depth, k, equip_depth)
            elif mem is None and _apply_trans is None and ctx.terr_map is None:
                key = (_token_key(tks), k)
            else:
                # mem ON: ghost depende de posición/paso. transición ON: fase solar depende de depth.
                # map ON (D2): el terminal fija territory:here según (cdr,cdc) ⇒ la clave debe incluir posición.
                key = (_token_key(tks), cdr, cdc, depth, k)
            cached = memo.get(key)
            if cached is not None:
                return cached
        sm, tm = ctx.parse_tokens(tks)
        best = _INF
        for a in action_names:
            ntks, (ddr, ddc) = step(tks, sm, tm, a, depth + 1, cdr, cdc)
            # PODA DEL CONO (GEMV_CONE): si el hijo cae fuera del cono de relevancia, no se expande.
            # cone_prune=None ⇒ bit-exact (el if nunca entra). El callback vive en el adaptador (cierra
            # sobre gain/gfield): conserva ramas hacia el dominante (gfield-descent = dolor SIEMPRE),
            # hacia el 2º deseo, o cercanas; poda el resto. La raíz (primera acción) nunca se poda porque
            # se evalúa en el bucle de plan_terminal, no aquí.
            if cone_dryrun is not None:                              # LECTURA (dry-run v1/v2): retorno ignorado
                cone_dryrun(cdr + ddr, cdc + ddc, cdr, cdc, depth + 1)
            if cone_prune is not None and cone_prune(cdr + ddr, cdc + ddc, cdr, cdc):
                continue
            ed = equip_depth
            if rollout_discount is not None and equip_depth is None and _equipped_this_step(tks, ntks):
                ed = depth + 1
            v = best_from(ntks, cdr + ddr, cdc + ddc, depth + 1, k - 1, ed)
            if v < best:
                best = v
        if use_cache:
            memo[key] = best
        return best

    # v6b — recursión meta (solo si track_meta): (d, moves, energy) del camino min-d más eficiente.
    # No toca best_from ni terminal[] ⇒ el path OFF/sin-meta es bit-exact.
    memo_m: dict = {}
    def best_from_meta(tks, cdr, cdc, depth, k, equip_depth=None):
        if k == 0:
            return (terminal_d(tks, cdr, cdc, depth, equip_depth), 0, _energy_of(tks, ctx))
        key = None
        if use_cache:
            key = ((_token_key(tks), cdr, cdc, depth, k, equip_depth) if rollout_discount is not None
                   else (_token_key(tks), cdr, cdc, depth, k))
            c = memo_m.get(key)
            if c is not None:
                return c
        sm, tm = ctx.parse_tokens(tks)
        best = (_INF, 0, 0)
        for a in action_names:
            ntks, (ddr, ddc) = step(tks, sm, tm, a, depth + 1, cdr, cdc)
            moved = 1 if (ddr, ddc) != (0, 0) else 0
            ed = equip_depth
            if rollout_discount is not None and equip_depth is None and _equipped_this_step(tks, ntks):
                ed = depth + 1
            cd, cm, ce = best_from_meta(ntks, cdr + ddr, cdc + ddc, depth + 1, k - 1, ed)
            cand = (cd, cm + moved, ce)
            # N1 d; entre iguales-d preferir menos moves; a igualdad más energía terminal
            if (cand[0] < best[0] - _TOL or
                (abs(cand[0] - best[0]) <= _TOL and
                 (cand[1] < best[1] or (cand[1] == best[1] and cand[2] > best[2])))):
                best = cand
        if use_cache:
            memo_m[key] = best
        return best

    terminal: dict = {}
    meta: dict = {}
    for a in action_names:
        ntks, (ddr, ddc) = step(tokens, scalar_map, tag_map, a, 1, 0, 0)
        ed0 = 1 if (rollout_discount is not None and _equipped_this_step(tokens, ntks)) else None
        terminal[a] = round(best_from(ntks, ddr, ddc, 1, H - 1, ed0), _ROUND)
        if track_meta:
            moved = 1 if (ddr, ddc) != (0, 0) else 0
            d_m, mv_m, en_m = best_from_meta(ntks, ddr, ddc, 1, H - 1, ed0)
            meta[a] = (mv_m + moved, en_m)
    # ESLABÓN COMMIT (GEMV_COMMIT) — extractor del PLAN de k pasos para la acción ganadora. El plan es el
    # camino DP (sigue el coste-a-ir con horizonte DECRECIENTE: a1 mirando H-1, a2 mirando H-2, …), que NO
    # oscila (la oscilación necesita re-mirar a H COMPLETO cada tick; comprometerse con este camino la rompe).
    # NO re-plan greedy (eso reproduciría el 2-ciclo). Reusa best_from (memoizado). Se llama 1 vez por commit.
    def _extract_plan(first_action, kk):
        plan = [first_action]
        cur, (ddr, ddc) = step(tokens, scalar_map, tag_map, first_action, 1, 0, 0)
        cdr, cdc, depth = ddr, ddc, 1
        ed = 1 if (rollout_discount is not None and _equipped_this_step(tokens, cur)) else None
        for j in range(1, kk):
            rem = H - 1 - j          # horizonte restante del plan en este paso (decreciente)
            if rem < 0:
                break
            sm2, tm2 = ctx.parse_tokens(cur)
            best = _INF; besta = None; bestn = None; bestmove = (0, 0); bested = ed
            for a in action_names:
                ntks2, (dr2, dc2) = step(cur, sm2, tm2, a, depth + 1, cdr, cdc)
                ed2 = ed
                if rollout_discount is not None and ed is None and _equipped_this_step(cur, ntks2):
                    ed2 = depth + 1
                v = (best_from(ntks2, cdr + dr2, cdc + dc2, depth + 1, rem - 1, ed2) if rem - 1 >= 0
                     else terminal_d(ntks2, cdr + dr2, cdc + dc2, depth + 1, ed2))
                if v < best:
                    best = v; besta = a; bestn = ntks2; bestmove = (dr2, dc2); bested = ed2
            plan.append(besta)
            cur = bestn; cdr += bestmove[0]; cdc += bestmove[1]; depth += 1; ed = bested
        return plan
    if commit_k is not None:
        if track_meta:
            return terminal, meta, stats, _extract_plan
        return terminal, stats, _extract_plan
    if track_meta:
        return terminal, meta, stats
    return terminal, stats


def select(action_names, preds, terminal):
    """Desempate: (1) min d terminal, (2) min d primer paso, (3) orden action_names.

    `preds[a]['d']` = d del primer paso (lo que hoy usa el greedy y los evaluadores).
    Con H=1, terminal[a] == preds[a]['d'] → colapsa al orden greedy (noop primero).
    """
    min_term = min(terminal[a] for a in action_names)
    c1 = [a for a in action_names if terminal[a] <= min_term + _TOL]
    if len(c1) == 1:
        return c1[0]
    min_fs = min(preds[a]["d"] for a in c1)
    c2 = [a for a in c1 if preds[a]["d"] <= min_fs + _TOL]
    return min(c2, key=action_names.index)   # orden action_names (noop primero)


TIEBREAK_EPS = 1e-3   # spec: [doc de diseño interna, no en el repo] — escala de la degeneración medida

# C4 — RED FINAL DEL PASO ([doc de diseño interna, no en el repo], 2026-07-29). Cuando queda un EMPATE EXACTO residual (>1
# candidato tras TODA la jerarquía), el fallback histórico `min(cand, key=action_names.index)` es
# IDÉNTICO para todos los clones → todos eligen la misma acción → colisión/2-ciclo simétrico. C4 lo
# rompe por SLOT (identidad del agente): dos clones en la MISMA situación de empate exacto eligen
# acciones DISTINTAS entre las empatadas (misma terminal_d → no toca la constitución, solo elige otra
# indiferente). ÚLTIMO eslabón, solo en empate exacto (|cand|>1). OFF (c4_on=False) ≡ ordered[0] bit-exact.
_C4_DECISIONS = [0]   # contador de instrumentación (honestidad del examen): cuántas veces decide C4
def _c4_break(cand, action_names, slot, c4_on):
    o = sorted(cand, key=action_names.index)             # orden action_names (noop primero), como el fallback histórico
    if c4_on and slot >= 0 and len(o) > 1:
        _C4_DECISIONS[0] += 1
        return o[slot % len(o)]                           # rompe la simetría de clones por slot
    return o[0]                                           # OFF o sin empate: idéntico a min(cand, key=index)


def _hierarchy(cand, meta, attractor, action_deltas, exclude_noop, fresh_attractor, action_names, attr_field=None, slot=-1, c4_on=False):
    """Rompe un EMPATE por la jerarquía FIRMADA: N2 eficiencia (menos moves; a igualdad más energía) ·
    N3 progreso al atractor/miga (L1) · N4 frescura · ORDEN action_names. NUNCA usa la d-de-1-paso:
    ésa solo separa terminales que NO empatan. GEMV_TIE_UNIFIED — el criterio ya firmado, aplicado a
    TODO empate sea cual sea la rama por la que se llegue."""
    cand = list(cand)
    if exclude_noop:                                # N2a — quieto no gana empates
        movers = [a for a in cand if a != "noop"]
        if movers:
            cand = movers
    if meta:                                        # N2b — menos moves; a igualdad más energía
        mm = min(meta[a][0] for a in cand)
        cand = [a for a in cand if meta[a][0] == mm]
        if len(cand) > 1:
            me = max(meta[a][1] for a in cand)
            cand = [a for a in cand if meta[a][1] == me]
    if len(cand) == 1:
        return cand[0]
    # N3 atractor/miga · N4 frescura (mismo mecanismo). GEODESIA (attr_field): el PROGRESO al atractor es por
    # CAMINO MÁS CORTO (el move que baja la geodésica al atractor), no por L1 ciega-al-muro → el desempate RODEA
    # estaciones/muros en vez de empujar contra ellos (cura el atasco de s0). Solo el `attractor` real usa el
    # campo; `fresh_attractor` (explorar) sigue L1. OFF (attr_field None) ≡ L1 bit-exact.
    for atr, afield in ((attractor, attr_field), (fresh_attractor, None)):
        if atr is not None and action_deltas is not None:
            if afield is not None and afield.get((0, 0)) is not None:
                base = afield[(0, 0)]                # geodésica del agente al atractor
                red = [a for a in cand
                       if afield.get(action_deltas.get(a, (0, 0)), 1e9) < base]   # move que BAJA la geodésica
            else:
                ar, ac = atr
                base = abs(ar) + abs(ac)
                red = [a for a in cand
                       if abs(ar - action_deltas.get(a, (0, 0))[0]) + abs(ac - action_deltas.get(a, (0, 0))[1]) < base]
            if red and len(red) < len(cand):
                cand = red
            if len(cand) == 1:
                return cand[0]
    return _c4_break(cand, action_names, slot, c4_on)   # orden action_names (NUNCA la d-de-1-paso) + C4 red final


def select_tiebreak(action_names, preds, terminal, meta, attractor=None, action_deltas=None,
                    eps: float = TIEBREAK_EPS, exclude_noop: bool = False, fresh_attractor=None,
                    tie_unified: bool = False, attr_field=None, slot: int = -1, c4_on: bool = False):
    """Desempate JERÁRQUICO (GEMV_TIEBREAK). Cláusula 3b: la d terminal es el único juez.

    GEMV_TIE_UNIFIED (vía a, 2026-07-18): PRINCIPIO — un empate en terminal_d es indiferencia genuina y
    lo rompe SIEMPRE la jerarquía (N2/N3-miga/N4/orden), NUNCA la d-de-1-paso, sea cual sea la rama. Cierra
    el agujero de aplicación: antes, con spread>eps, `select()` rompía el empate exacto del mínimo por la
    d-de-1-paso (miope, oscilaba) en vez de por la miga. La d-de-1-paso queda donde nunca estorbó: separa
    terminales que NO empatan (|c1|==1). La tolerancia de empate es EXACTA (±_TOL=1e-9, igualdad de los
    terminales redondeados a _ROUND), NO una banda — el eps=1e-3 (degeneración del paisaje) es concepto
    APARTE y no se ensancha (lección e3). OFF (tie_unified=False) ≡ comportamiento previo bit-exact.
    """
    vals = [terminal[a] for a in action_names]
    spread = max(vals) - min(vals)
    if spread > eps:
        if not tie_unified:
            return select(action_names, preds, terminal)   # OFF: paisaje real → select() bit-exact
        # ON: ¿empate EXACTO en el mínimo del terminal? si no, gana el mínimo (gradiente real, sin empate).
        min_term = min(vals)
        c1 = [a for a in action_names if terminal[a] <= min_term + _TOL]
        if len(c1) == 1:
            return c1[0]                                    # NO hay empate → no-interferencia (la 1-step d no toca)
        return _hierarchy(c1, meta, attractor, action_deltas, exclude_noop, fresh_attractor, action_names, attr_field, slot, c4_on)
    # ── paisaje degenerado (spread≤eps): la indiferencia camina ──
    # SIN cambio bajo tie_unified: esta rama YA rompe el empate por la jerarquía (N3/miga corre ANTES que
    # el fallback N5 d-de-1-paso), así que el agujero NO estaba aquí — estaba en el spread>eps (select()).
    cand = list(action_names)
    if exclude_noop:
        movers = [a for a in cand if a != "noop"]
        if movers:
            cand = movers
    if meta:
        min_moves = min(meta[a][0] for a in cand)
        cand = [a for a in cand if meta[a][0] == min_moves]
        if len(cand) > 1:
            max_en = max(meta[a][1] for a in cand)
            cand = [a for a in cand if meta[a][1] == max_en]
    if len(cand) == 1:
        return cand[0]
    if attractor is not None and action_deltas is not None:
        # GEODESIA: el progreso al atractor por CAMINO MÁS CORTO (rodea sólidos), no por L1 ciega-al-muro.
        # Éste es el desempate del paisaje PLANO — el atasco de s0 vive aquí. OFF (attr_field None) ≡ L1 bit-exact.
        if attr_field is not None and attr_field.get((0, 0)) is not None:
            base = attr_field[(0, 0)]
            reducers = [a for a in cand if attr_field.get(action_deltas.get(a, (0, 0)), 1e9) < base]
        else:
            ar, ac = attractor
            base = abs(ar) + abs(ac)
            reducers = [a for a in cand
                        if abs(ar - action_deltas.get(a, (0, 0))[0]) + abs(ac - action_deltas.get(a, (0, 0))[1]) < base]
        if reducers and len(reducers) < len(cand):
            cand = reducers
    if len(cand) == 1:
        return cand[0]
    if fresh_attractor is not None and action_deltas is not None:
        fr, fc = fresh_attractor
        base = abs(fr) + abs(fc)
        reducers = [a for a in cand
                    if abs(fr - action_deltas.get(a, (0, 0))[0]) + abs(fc - action_deltas.get(a, (0, 0))[1]) < base]
        if reducers and len(reducers) < len(cand):
            cand = reducers
    if len(cand) == 1:
        return cand[0]
    min_fs = min(preds[a]["d"] for a in cand)
    c2 = [a for a in cand if preds[a]["d"] <= min_fs + _TOL]
    return _c4_break(c2, action_names, slot, c4_on)   # C4 red final: empate exacto residual → por slot
