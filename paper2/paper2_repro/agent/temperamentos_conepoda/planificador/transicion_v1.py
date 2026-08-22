"""
transicion_v1 — modelo de transición para el simulador del planificador.

Spec: [doc de diseño interna, no en el repo]
Enseña al paso de simulación las consecuencias de las acciones PROPIAS sobre el inventario
predicho (energía, HP, materiales), según la mecánica PÚBLICA del juego (magnitudes citadas
en la spec desde src/cogsguard/game/…). NO aprendido, NO inventado, NO calibrado.

Se aplica DENTRO del paso del planificador, tras _shift_tokens (que ya restó el coste de move),
antes de appraise. Ablacionable: si no se llama (GEMV_TRANSITION=0) el planificador es idéntico a v1.

Mecánica modelada (ver spec §2 para fuentes):
  - Regen solar global: +solar/tick (día=3 / noche=1, day_length=200).      [days.py, solar.py]
  - Curación en territorio propio: energía→cap(20), HP→cap(100).            [heal_team.py]
  - Daño en territorio rival: HP −1/tick.                                   [damage_strangers.py]
  - Cosecha por bump de extractor: +1 recurso (sin gear).                   [extractors.py]
  - Coste de move (−4) ya lo aplica _shift_tokens; aquí NO se re-resta.     [energy.py]
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable

# FONTANERÍA ETAPA 2 (GEMV_SPARSE): reusar el scalar_map YA parseado para lecturas O(1) en vez del scan
# O(n). Empieza por las funciones que YA llaman parse_tokens y DESCARTAN el scalar_map (coste cero: el
# parse ya ocurre). Bit-exact por construcción (dict.get == scan). OFF ≡ scan de siempre.
_SPARSE: bool = os.environ.get("GEMV_SPARSE", "0") in ("1", "on", "ON", "true")

def _gm_sm(sm, loc, fid_p0):
    """get_multipart O(1) sobre el scalar_map ya parseado (mismo resultado que el scan _get_multipart)."""
    return sm.get((loc, fid_p0), 0) + 256 * sm.get((loc, fid_p0 + 1), 0)

# Magnitudes citadas (spec §2)
ENERGY_CAP = 20      # energy.py limit
HP_CAP = 100         # damage.py limit
DAY_SOLAR = 3        # days.py
NIGHT_SOLAR = 1      # days.py
DAY_LENGTH = 200     # days.py
TERR_DAMAGE = -1     # damage_strangers.py
EXTRACT_AMOUNT = 1   # extractors.py small_amount (sin gear miner)


@dataclass
class TransCtx:
    parse_tokens: Callable
    agent_loc: int
    fid_energy_p0: int      # 24
    fid_hp_p0: int          # 20
    egocentric_cols: int    # 16
    agent_row: int
    agent_col: int
    tag_type_hub: int
    own_team_tag: int
    extractor_tags: frozenset
    action_deltas: dict
    # Cobertura de la transición (interruptores propios; OFF ≡ conducta v1 bit-exact):
    model_energy: bool = True          # energía/HP (Fase 3b). GEMV_TRANSITION.
    model_extract: bool = False        # bump→cosecha (completa la cobertura). GEMV_TRANSITION_EXTRACT.
    extractor_inv_fid: dict = None     # tag_type de extractor → fid_p0 del inventario del material
    # Cobertura v2 (depósito como ACTO): el bump al hub propio con carbon deposita (held→0) e incrementa
    # el token acts_done (el crédito A lo aplica appraise). Sólo activo con GEMV_COVERAGE=v2_hybrid.
    model_deposit: bool = False
    fid_carbon: int = None             # fid_p0 del inventario carbon del agente (compat)
    element_inv_fids: tuple = None     # fid_p0 de TODOS los elementos (depósito generalizado; competidor 1b)
    fid_acts_done: int = 250           # token acts_done (AGENT_LOC, fid_acts_done, n)
    # v6 D2 — cargo-cap: límite COMBINADO de carga (CargoLimitVariant.limit=4, cargo.py). None=sin cap (v5).
    cargo_cap: int = None
    # v6 D1 — el depósito sube team_held: loc global + mapa inv_fid_p0 → team_fid_p0. None=no sube (v5).
    team_loc: int = None
    inv_to_team: dict = None
    # Eslabón 1 (GEMV_HEARTS) — transición make_and_get_heart (hub.py:121). OFF ≡ v6 bit-exact.
    model_hearts: bool = False
    fid_inv_heart: int = None     # inv:heart p0 del agente (22, leído del player_config)
    heart_recipe: int = 7         # heart.cost = {elemento: 7} (machina_1.py:132)
    heart_cap: int = 10           # heart.py:25 limit=10 por agente
    hub_get_ok: bool = False       # Eslabón 4 V-A: modelar get OPTIMISTA (retirar heart del hub) cuando
                                   # pantry<7 (make no casa). True solo si marcador ∧ hub no ha fallado
                                   # recientemente (candado). Default False ⇒ eslabón 1-3 bit-exact.
    # Eslabón 4 (GEMV_MARCADOR) — equipar aligner + alinear junction. OFF ≡ e3 bit-exact.
    model_marcador: bool = False
    fid_inv_aligner: int = None           # inv:aligner p0 (26)
    tag_type_aligner_station: int = None  # type:aligner (9) = gear station del aligner
    tag_type_junction: int = None         # type:junction (13)
    tag_net_own: int = None               # net:cogs (5) del propio equipo
    aligner_cost: dict = None             # {team_fid: coste} del aligner (C3,O1,G1,Si1) del hub
    fid_tag: int = None                   # fid del token 'tag' (6), para leer/escribir tags de celda
    equip_gated: bool = False             # GEMV_EQUIP_GATED: el equip imaginado exige fondos CONOCIDOS del hub


def _get_multipart(tokens, loc, fid_p0, sm=None):
    if _SPARSE and sm is not None:               # ETAPA 2: lectura O(1) sobre el scalar_map reusado
        return sm.get((loc, fid_p0), 0) + 256 * sm.get((loc, fid_p0 + 1), 0)
    p0 = p1 = 0
    for t in tokens:
        if int(t[0]) == loc and int(t[1]) == fid_p0: p0 = int(t[2])
        elif int(t[0]) == loc and int(t[1]) == fid_p0 + 1: p1 = int(t[2])
    return p0 + 256 * p1


def _set_multipart(tokens, loc, fid_p0, value):
    """Devuelve tokens con el valor multipart (p0,p1) puesto en (loc,fid_p0/fid_p0+1)."""
    value = max(0, int(round(value)))
    lo, hi = value % 256, value // 256
    out, seen_lo, seen_hi = [], False, False
    for t in tokens:
        loc_t, fid_t = int(t[0]), int(t[1])
        if loc_t == loc and fid_t == fid_p0:
            out.append((loc, fid_p0, lo)); seen_lo = True
        elif loc_t == loc and fid_t == fid_p0 + 1:
            out.append((loc, fid_p0 + 1, hi)); seen_hi = True
        else:
            out.append((t[0], t[1], t[2]))
    if not seen_lo: out.append((loc, fid_p0, lo))
    if hi and not seen_hi: out.append((loc, fid_p0 + 1, hi))
    return out


def _in_own_territory(tokens, tag_map, ctx: TransCtx) -> bool:
    """En territorio propio si hay un hub propio en la ventana (radio ventana 6 < radio territorio 20;
    empíricamente el hub propio está a dist ≤6 en ~100% de los ticks → siempre en territorio)."""
    for loc, tags in tag_map.items():
        if ctx.tag_type_hub in tags and ctx.own_team_tag in tags:
            return True
    return False


def solar_at(step: int) -> int:
    """Valor solar del tick según fase día/noche (days.py). Día la primera mitad del periodo."""
    return DAY_SOLAR if (step % DAY_LENGTH) < (DAY_LENGTH // 2) else NIGHT_SOLAR


def _cargo_total(tokens, ctx: TransCtx) -> int:
    """Carga combinada del agente entre todos los elementos (para el cargo-cap D2)."""
    fids = ctx.element_inv_fids or ((ctx.fid_carbon,) if ctx.fid_carbon else ())
    return sum(_get_multipart(tokens, ctx.agent_loc, f) for f in fids)


def _cargo_full(tokens, ctx: TransCtx) -> bool:
    """True si la carga combinada ya alcanzó el cargo-cap (D2). Sin cap ⇒ nunca lleno."""
    return ctx.cargo_cap is not None and _cargo_total(tokens, ctx) >= ctx.cargo_cap


def harvest_bump(tokens, ext_tag: int, ctx: TransCtx):
    """Bump→cosecha (extractors.py, small_amount=1): el agente NO se mueve (la estación bloquea)
    y suma +EXTRACT_AMOUNT del material del extractor a su inventario predicho. Ese held+ propaga
    a `appraise` (w_mat = max(0,demand−held)/100 baja; cobertura β del canal social sube) ⇒ `d`
    baja SOLA al bumpear. No hay términos de valor nuevos: es mecánica pública del juego."""
    if not ctx.model_extract or not ctx.extractor_inv_fid:
        return tokens
    inv_fid = ctx.extractor_inv_fid.get(int(ext_tag))
    if inv_fid is None:
        return tokens
    if _cargo_full(tokens, ctx):          # D2 — carga llena: el juego no concede más (cargo-cap)
        return tokens
    held = _get_multipart(tokens, ctx.agent_loc, inv_fid)
    return _set_multipart(tokens, ctx.agent_loc, inv_fid, held + EXTRACT_AMOUNT)


def harvest_virtual(tokens, inv_fid: int, ctx: TransCtx):
    """Cosecha de un extractor VIRTUAL (recordado, fuera de ventana): held+EXTRACT_AMOUNT del elemento.
    Idéntico al efecto de una cosecha percibida; el planner lo prevé donde la percepción directa lo haría."""
    if _cargo_full(tokens, ctx):          # D2 — cargo-cap también en cosecha virtual
        return tokens
    held = _get_multipart(tokens, ctx.agent_loc, inv_fid)
    return _set_multipart(tokens, ctx.agent_loc, inv_fid, held + EXTRACT_AMOUNT)


def make_heart_bump(tokens, ctx: TransCtx, sm=None):
    """make_and_get_heart (hub.py:121-128), Eslabón 1: en el firstMatch [deposit, get, make],
    con carga de elementos = 0 (si no, deposit casó antes), pantry ≥ recipe/elem en LOS 4 y
    hearts < cap → inv:heart+1, team_held −recipe/elem. Devuelve tokens o None si no casa.
    get_heart (retirar) NO se modela: los hearts del hub son INobservables (spec §0)."""
    if not ctx.model_hearts or ctx.fid_inv_heart is None:
        return None
    if ctx.team_loc is None or not ctx.inv_to_team:
        return None
    if _cargo_total(tokens, ctx) > 0:          # carga de elementos ≠ 0 ⇒ deposit casa primero
        return None
    team_fids = set(ctx.inv_to_team.values())
    if not team_fids:
        return None
    hearts = _get_multipart(tokens, ctx.agent_loc, ctx.fid_inv_heart, sm=sm)
    if ctx.heart_cap is not None and hearts >= ctx.heart_cap:
        return None
    pantry_ok = all(_get_multipart(tokens, ctx.team_loc, tf, sm=sm) >= ctx.heart_recipe for tf in team_fids)
    if pantry_ok:                              # MAKE: pantry ≥ recipe → craftea, team_held −recipe/elem
        out = tokens
        for tf in team_fids:                   # queryDelta(hq, −recipe/elem)
            cur = _get_multipart(out, ctx.team_loc, tf, sm=sm)   # tf distinto → leído antes de su set
            out = _set_multipart(out, ctx.team_loc, tf, cur - ctx.heart_recipe)
        out = _set_multipart(out, ctx.agent_loc, ctx.fid_inv_heart, hearts + 1)  # updateActor(heart+1)
        return out
    # GET OPTIMISTA (V-A, Eslabón 4): pantry<7 → el make no casa, pero el hub PUEDE tener hearts
    # (INobservable). Se imagina el retiro (heart+1, sin tocar despensa) SI el candado no lo enfría.
    # El firstMatch del juego resuelve de verdad: get si hay, nada si no (→ el candado registra el fallo).
    if ctx.hub_get_ok:
        return _set_multipart(tokens, ctx.agent_loc, ctx.fid_inv_heart, hearts + 1)
    return None


def deposit_virtual(tokens, ctx: TransCtx):
    """Eslabón 2 — DEPÓSITO VIRTUAL en el hub RECORDADO (fuera de ventana), espejo de harvest_virtual.
    held(elementos)→0, team_held += delivered (D1, queryDeposit), acts_done+1. Mecánica real del juego;
    el alcance lo da la memoria del hub (no la ventana). Sin carga de elementos → sin efecto."""
    fids = ctx.element_inv_fids if ctx.element_inv_fids else ((ctx.fid_carbon,) if ctx.fid_carbon else ())
    total = sum(_get_multipart(tokens, ctx.agent_loc, f) for f in fids)
    if total <= 0:
        return tokens
    out = tokens
    for f in fids:
        delivered = _get_multipart(out, ctx.agent_loc, f)
        out = _set_multipart(out, ctx.agent_loc, f, 0)                    # entrega todos los elementos
        if delivered > 0 and ctx.team_loc is not None and ctx.inv_to_team:
            tf = ctx.inv_to_team.get(int(f))
            if tf is not None:
                cur = _get_multipart(out, ctx.team_loc, tf)
                out = _set_multipart(out, ctx.team_loc, tf, cur + delivered)  # sube team_held
    acts = 0
    for t in out:
        if int(t[0]) == ctx.agent_loc and int(t[1]) == ctx.fid_acts_done:
            acts = int(t[2])
    out = [t for t in out if not (int(t[0]) == ctx.agent_loc and int(t[1]) == ctx.fid_acts_done)]
    out.append((ctx.agent_loc, ctx.fid_acts_done, acts + 1))              # registra el acto
    return out


def equip_aligner_bump(tokens, ctx: TransCtx, sm=None):
    """Eslabón 4 — bump gear station del aligner (gear_stations.py): inv:aligner=1, hub paga el coste
    (team_held −aligner_cost por elemento). El heart portado SOBREVIVE (ClearInventory solo 'gear', O3).
    Si ya lleva aligner → None (keep_gear, sin efecto). Sin coste alcanzable en el hub → igual se modela
    (el juego lo gatea; el planner imagina el equipado) — SALVO equip_gated (fix del equip optimista)."""
    if not ctx.model_marcador or ctx.fid_inv_aligner is None:
        return None
    if _get_multipart(tokens, ctx.agent_loc, ctx.fid_inv_aligner, sm=sm) > 0:
        return None  # ya equipado
    # FIX DEL EQUIP OPTIMISTA (GEMV_EQUIP_GATED): el equip imaginado SOLO existe si los fondos CONOCIDOS del
    # hub (team_held en team_loc, percibido/recordado) cubren el coste del gear. Sin fondos conocidos → None
    # (el equip no se imagina; el hambre de despensa, que sí sabe reponer, toma el mando natural).
    if getattr(ctx, "equip_gated", False):
        if ctx.team_loc is None or not ctx.aligner_cost:
            return None
        for tf, c in ctx.aligner_cost.items():
            if _get_multipart(tokens, ctx.team_loc, tf, sm=sm) < c:
                return None
    out = tokens
    if ctx.team_loc is not None and ctx.aligner_cost:
        for tf, c in ctx.aligner_cost.items():
            cur = _get_multipart(out, ctx.team_loc, tf, sm=sm)   # tf distinto por iter → leído antes de su set
            out = _set_multipart(out, ctx.team_loc, tf, max(0, cur - c))   # hub paga
    out = _set_multipart(out, ctx.agent_loc, ctx.fid_inv_aligner, 1)       # aligner equipado
    return out  # el heart (capacidad aparte) NO se toca


def _cell_tags(tokens, loc, ctx: TransCtx):
    return {int(t[2]) for t in tokens if int(t[0]) == loc and int(t[1]) == ctx.fid_tag}


def align_junction_bump(tokens, dest_loc, ctx: TransCtx, sm=None):
    """Eslabón 4 — bump junction gris/enemiga (type:junction sin nuestro net) con aligner+heart
    (junction.py:99-118): la junction gana tags team+net (nuestra), heart −1 del agente. La proximidad
    (≤15 net-node/≤25 hub) se gatea aguas arriba (el planner solo llama esto en junctions alcanzables).
    Devuelve tokens o None si no casa."""
    if not ctx.model_marcador or ctx.fid_tag is None:
        return None
    tags = _cell_tags(tokens, dest_loc, ctx)
    if ctx.tag_type_junction not in tags:
        return None                                   # no es junction
    if ctx.tag_net_own in tags:
        return None                                   # ya es nuestra
    if _get_multipart(tokens, ctx.agent_loc, ctx.fid_inv_aligner or -1, sm=sm) < 1:
        return None                                   # sin aligner
    if _get_multipart(tokens, ctx.agent_loc, ctx.fid_inv_heart or -1, sm=sm) < 1:
        return None                                   # sin heart
    out = [t for t in tokens]
    out.append((dest_loc, ctx.fid_tag, ctx.own_team_tag))   # addTag(team)
    out.append((dest_loc, ctx.fid_tag, ctx.tag_net_own))    # addTag(net)
    hearts = _get_multipart(out, ctx.agent_loc, ctx.fid_inv_heart, sm=sm)   # tags no tocan heart → reuso
    out = _set_multipart(out, ctx.agent_loc, ctx.fid_inv_heart, hearts - 1)  # consume 1 heart
    return out


def _dest_loc(action, ctx: TransCtx):
    d = ctx.action_deltas.get(action, (0, 0))
    return (ctx.agent_row + d[0]) * ctx.egocentric_cols + (ctx.agent_col + d[1])


def station_bump_effect(tokens, action, ctx: TransCtx):
    """Si el move choca con una estación, el agente NO avanza y la transición aplica su efecto.
    Devuelve (tokens_modificados, tipo) o (None, None) si el destino no es estación-bump.

      - extractor demandado (model_extract): COSECHA (held+EXTRACT_AMOUNT).
      - hub propio con carbon (model_deposit): DEPÓSITO (held carbon→0, acts_done token +1). El crédito
        A del acto lo aplica appraise al leer acts_done; aquí sólo se registra el acto en el token.
    """
    if action not in ctx.action_deltas:
        return None, None
    dloc = _dest_loc(action, ctx)
    _sm, tag_map = ctx.parse_tokens(tokens)      # ETAPA 2: reusar el scalar_map (se parsea igual)
    tags = tag_map.get(dloc, set())
    # Eslabón 4 — alinear junction: el destino es una junction gris/enemiga y llevo aligner+heart.
    if ctx.model_marcador and ctx.tag_type_junction in tags:
        aligned = align_junction_bump(tokens, dloc, ctx, sm=_sm)
        if aligned is not None:
            return aligned, "align"
        return tokens, "junction_blocked"   # junction (ya nuestra o sin recursos): bloquea el move
    # Eslabón 4 — equipar aligner: el destino es la gear station del aligner.
    if ctx.model_marcador and ctx.tag_type_aligner_station is not None and ctx.tag_type_aligner_station in tags:
        equipped = equip_aligner_bump(tokens, ctx, sm=_sm)
        if equipped is not None:
            return equipped, "equip_aligner"
        return tokens, "station_blocked"    # ya equipado: bloquea el move
    # depósito: hub propio + llevo ALGÚN elemento (generalizado a todos; el juego deposita actorHasAnyOf).
    if (ctx.model_deposit and ctx.tag_type_hub in tags and ctx.own_team_tag in tags):
        fids = ctx.element_inv_fids if ctx.element_inv_fids else ((ctx.fid_carbon,) if ctx.fid_carbon else ())
        total = sum(_get_multipart(tokens, ctx.agent_loc, f, sm=_sm) for f in fids)   # unmodificado → reuso
        if total > 0:
            out = tokens
            for f in fids:
                delivered = _get_multipart(out, ctx.agent_loc, f, sm=_sm)   # cada f leído antes de su set
                out = _set_multipart(out, ctx.agent_loc, f, 0)               # entrega TODOS los elementos
                # D1 — el depósito SUBE team_held (queryDeposit, hub.py): el hub recibe la carga ⇒ el
                # déficit SHELF derivado (que lee team_held) baja en la imaginación.
                if delivered > 0 and ctx.team_loc is not None and ctx.inv_to_team:
                    tf = ctx.inv_to_team.get(int(f))
                    if tf is not None:
                        cur = _get_multipart(out, ctx.team_loc, tf)   # tf ACUMULA → NO reuso (scan seguro)
                        out = _set_multipart(out, ctx.team_loc, tf, cur + delivered)
            acts = 0
            for t in out:
                if int(t[0]) == ctx.agent_loc and int(t[1]) == ctx.fid_acts_done:
                    acts = int(t[2])
            out = [t for t in out if not (int(t[0]) == ctx.agent_loc and int(t[1]) == ctx.fid_acts_done)]
            out.append((ctx.agent_loc, ctx.fid_acts_done, acts + 1))            # registra el acto (1 evento)
            return out, "deposit"
        # carga de elementos = 0 → firstMatch cae a get_heart/make_and_get_heart (hub.py:163). Eslabón 1:
        made = make_heart_bump(tokens, ctx, sm=_sm)
        if made is not None:
            return made, "make"
        # hub propio sin carga y sin poder fabricar: bloquea el move, el agente no avanza
        return tokens, "hub_blocked"
    # cosecha: extractor demandado
    if ctx.model_extract and ctx.extractor_inv_fid:
        for t in tags:
            if int(t) in ctx.extractor_inv_fid:
                if _cargo_full(tokens, ctx):          # D2 — cargo-cap en la cosecha del planner
                    return tokens, "harvest_full"
                inv_fid = ctx.extractor_inv_fid[int(t)]
                held = _get_multipart(tokens, ctx.agent_loc, inv_fid, sm=_sm)   # unmodificado → reuso
                return _set_multipart(tokens, ctx.agent_loc, inv_fid, held + EXTRACT_AMOUNT), "harvest"
    return None, None


def apply_transition(tokens, action, world_step, sim_depth, ctx: TransCtx):
    """Modifica los tokens de inventario del estado simulado según la mecánica del juego.

    world_step: paso real del episodio. sim_depth: profundidad en el horizonte (1..H).
    """
    if not ctx.model_energy:
        return tokens                      # sub-interruptor energía/HP apagado: no tocar (bit-exact v1)
    if _SPARSE:
        _sm, tag_map = ctx.parse_tokens(tokens)     # ETAPA 2: reusar el scalar_map (ya se parsea igual)
        energy = _gm_sm(_sm, ctx.agent_loc, ctx.fid_energy_p0)
        hp = _gm_sm(_sm, ctx.agent_loc, ctx.fid_hp_p0)
    else:
        _, tag_map = ctx.parse_tokens(tokens)
        energy = _get_multipart(tokens, ctx.agent_loc, ctx.fid_energy_p0)
        hp = _get_multipart(tokens, ctx.agent_loc, ctx.fid_hp_p0)

    if _in_own_territory(tokens, tag_map, ctx):
        # heal_team.py: +100/tick energía y HP → a cap.
        new_energy, new_hp = ENERGY_CAP, HP_CAP
    else:
        # Regen solar global (days.py/solar.py). El coste de move (−4) ya está en `energy`.
        new_energy = min(energy + solar_at(world_step + sim_depth), ENERGY_CAP)
        new_hp = hp  # sin drenaje basal modelado (spec §3); daño rival se omite (raro, all-cogs)

    out = tokens
    if new_energy != energy:
        out = _set_multipart(out, ctx.agent_loc, ctx.fid_energy_p0, new_energy)
    if new_hp != hp:
        out = _set_multipart(out, ctx.agent_loc, ctx.fid_hp_p0, new_hp)
    return out
