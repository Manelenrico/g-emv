"""
Memoria espacial v1 — campo fantasma para el appraisal G-EMV.

Spec: [doc de diseño interna, no en el repo]
Interruptor: GEMV_USE_MEMORY=0 → OFF (reproduce Fase 1 exactamente)
             GEMV_USE_MEMORY=1 → ON

motor/model.py INTOCABLE. La política greedy no cambia.
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from motor.model import State, DEFAULT_CONFIG
from appraisal.appraisal_v3 import (
    A_F_HUB, A_R_ENERGY, A_R_MAT,
    ALLY_WEIGHT, RIVAL_WEIGHT, JUNCTION_BONUS,
    EGOCENTRIC_COLS, AGENT_ROW, AGENT_COL,
    TAG_TYPE_HUB, TAG_TYPE_AGENT, TAG_TYPE_JUNCTION,
    TAG_TEAM_COGS, TAG_TEAM_CLIPS,
    TAG_NET_COGS, TAG_NET_CLIPS,
    EXTRACTOR_TAGS,
    TAG_TYPE_OXYGEN_EXTRACTOR, TAG_TYPE_CARBON_EXTRACTOR,
    TAG_TYPE_GERMANIUM_EXTRACTOR, TAG_TYPE_SILICON_EXTRACTOR,
    FID_INV_SOLAR,
    social_weight,
)

# ── Constantes declaradas en spec ────────────────────────────────────────────
GHOST_FACTOR:         float = 0.5
GHOST_DECAY_HALFLIFE: int   = 500
GHOST_DECAY_LAMBDA:   float = math.log(2) / GHOST_DECAY_HALFLIFE
MAX_MEMORY_ENTRIES:   int   = 512
WINDOW_HALF:          int   = 6   # ventana 13×13: ±6 celdas
# DEUDA §disco (2026-07-19): la visión REAL es un disco (dr²+dc²≤37, medido; [doc de diseño interna, no en el repo]), pero
# los candados de memoria (_present / exclusión-ghost) usan el CUADRADO como LÍNEA BASE VALIDADA C6 — NO por
# ser correcto (el cuadrado es falso y lo sabemos) sino porque cambiarlo a disco PERTURBA la navegación (medido:
# s0 dejaba de puntuar) → es un eslabón propio con sus gates de conducta, no un fix de paso. Causa sin
# diagnosticar; candidato: persistencia de recuerdos de esquina no re-verificables. El helper queda como gancho.
_DISK_MEM: bool = os.environ.get("GEMV_DISK", "0") in ("1", "on", "ON", "true")
PERCEPTION_R2: int = 37
# Instrumentación forense (OFF≡bit-exact: solo logging, no cambia conducta). GEMV_MEM_EVENT_DBG=1 →
# emite "MEM_EVENT {json}" por altas/borrados de junctions con clase, celda, causa y estado de percepción.
_MEM_EVENT_DBG: bool = bool(os.environ.get("GEMV_MEM_EVENT_DBG"))
def _mev(d: dict) -> None:
    if _MEM_EVENT_DBG:
        import json as _j
        print("MEM_EVENT " + _j.dumps(d), file=sys.stderr, flush=True)
def _in_view_mem(dr: int, dc: int) -> bool:   # NO cableado (los candados de memoria usan el cuadrado; ver deuda)
    return (dr * dr + dc * dc <= PERCEPTION_R2) if _DISK_MEM else (abs(dr) <= WINDOW_HALF and abs(dc) <= WINDOW_HALF)

_F_POS_TARGET: float = DEFAULT_CONFIG.f_pos_target   # 1.0
_R_POS_TARGET: float = DEFAULT_CONFIG.r_pos_target   # 2.0

ACTION_DELTAS: dict[str, tuple[int, int]] = {
    "move_north": (-1,  0),
    "move_south": ( 1,  0),
    "move_west":  ( 0, -1),
    "move_east":  ( 0,  1),
    "noop":       ( 0,  0),
}

_EXTRACTOR_CLS: dict[int, str] = {
    TAG_TYPE_OXYGEN_EXTRACTOR:    "extractor_oxygen",
    TAG_TYPE_CARBON_EXTRACTOR:    "extractor_carbon",
    TAG_TYPE_GERMANIUM_EXTRACTOR: "extractor_germanium",
    TAG_TYPE_SILICON_EXTRACTOR:   "extractor_silicon",
}

FORCE_AXIS: dict[str, str] = {
    "hub":                 "pF",
    "solar":               "pR",
    "extractor_oxygen":    "pR",
    "extractor_carbon":    "pR",
    "extractor_germanium": "pR",
    "extractor_silicon":   "pR",
    "ally":                "pS",
    "rival":               "nS",
    "junction_own":        "pS",
    "junction_rival":      "nS",
}

# Eslabón 4 — type:aligner (gear station), leído del config (_sane_world_ids lo rebindea). Y las clases
# de memoria del marcador que NO contribuyen al ghost (alimentan solo el atractor N3 estado-gateado).
TAG_TYPE_ALIGNER: int = 9
_MARCADOR_MEM_CLS = ("junction_gray", "gear_aligner")
# Fijos ESTRUCTURALES permanentes (OPCIÓN A): nunca se borran por no-percepción (oclusión/FOV ≠ ausencia).
# gear_aligner = la gear station del aligner (mapa fijo, verificado). junction_* son MUTABLES (cambian de
# dueño) → NO van aquí. Solo activo con mem.fixed_persist (GEMV_FIXED_PERSIST); OFF ≡ bit-exact.
_FIXED_PERSIST_CLS = ("gear_aligner",)


@dataclass
class EntradaMemoria:
    object_class: str    # clave en FORCE_AXIS
    raw_amplitude: float # amplitud × (1+dist_percibido); des-normaliza la distancia
    last_seen_step: int


# ─────────────────────────────────────────────────────────────────────────────

class MemoriaEspacial:
    """
    Memoria espacial de episodio con campo fantasma.

    Ámbito de episodio: llamar reset() al inicio de cada partida.
    OFF == Fase 1: si no se llama a observe() ni ghost_forces(), el State de
    appraise() es idéntico al de Fase 1.
    """

    def __init__(self) -> None:
        # (world_row, world_col, object_class) → EntradaMemoria
        self._entries: dict[tuple[int, int, str], EntradaMemoria] = {}
        self._agent_world: tuple[int, int] = (0, 0)
        self._step: int = 0
        # Memoria de muros (GEMV_WALL_MEM): sólidos conocidos en coords ABSOLUTAS, set SEPARADO de _entries
        # (no toca el cap de 512). wall_mem/solid_types los fija gemv_policy. OFF (wall_mem=False) ⇒ nunca se toca.
        self._walls: set[tuple[int, int]] = set()
        self.wall_mem: bool = False
        self.solid_types: frozenset = frozenset()
        # Hub persistente (GEMV_HUB_PERSIST): el hub propio no se olvida por no-percepción (fijo, centro de la
        # economía; alejarse no debe perder de vista la casa). Misma mecánica que _FIXED_PERSIST_CLS. Lo fija gemv_policy.
        self.hub_persist: bool = False
        # Extractor persistente (GEMV_EXTRACTOR_PERSIST): el extractor (fijo) no se olvida por oclusión/FOV;
        # su posición persiste hasta desmentido REAL (re-visto vacío/eliminado). OFF ≡ bit-exact.
        self.extractor_persist: bool = False

    # ── Ciclo de vida ─────────────────────────────────────────────────────────

    def reset(self) -> None:
        """Llamar al inicio de cada episodio. Memoria nace vacía."""
        self._entries.clear()
        self._walls.clear()
        self._agent_world = (0, 0)
        self._step = 0

    def step_tick(self, action: str, blocked: bool = False) -> None:
        """
        Avanzar un tick: actualizar odometría y contador.

        blocked: True si la acción fue predicha como bloqueada → no actualizar posición.
        Supuesto: movimientos no-bloqueados son deterministas.
        """
        self._step += 1
        if not blocked:
            dr, dc = ACTION_DELTAS.get(action, (0, 0))
            ar, ac = self._agent_world
            self._agent_world = (ar + dr, ac + dc)

    # ── Observación ───────────────────────────────────────────────────────────

    def observe(
        self,
        debug: dict,
        scalar_map: dict,
        tag_map: dict,
        team_side: str,
    ) -> None:
        """
        Actualizar memoria con los objetos percibidos en este tick.
        PERCEPCIÓN MANDA: corrige/borra entradas en la ventana actual.
        """
        ar, ac = self._agent_world
        step    = self._step
        w_energy = debug.get("w_energy", 0.0)

        own_team_tag  = TAG_TEAM_COGS  if team_side == "cogs" else TAG_TEAM_CLIPS
        rival_team_tag= TAG_TEAM_CLIPS if team_side == "cogs" else TAG_TEAM_COGS
        own_net_tag   = TAG_NET_COGS   if team_side == "cogs" else TAG_NET_CLIPS
        rival_net_tag = TAG_NET_CLIPS  if team_side == "cogs" else TAG_NET_COGS

        # ── PERCEPCIÓN MANDA: corregir entradas en ventana ────────────────
        # EXCEPCIÓN (fixed_persist, OPCIÓN A): los FIJOS estructurales (gear stations) son PERMANENTES —
        # no se mueven ni desaparecen. Que no se perciban en ventana es OCLUSIÓN/FOV (el hub u otros tapan
        # la línea de vista), NO ausencia. "Percepción manda" borra lo MUTABLE desmentido de verdad; un
        # fijo ocluido no está desmentido. La percepción los CONFIRMA (re-graba), nunca los borra.
        to_delete = []
        for (wr, wc, cls), entry in self._entries.items():
            if getattr(self, "fixed_persist", False) and (cls in _FIXED_PERSIST_CLS
                    or (cls == "hub" and getattr(self, "hub_persist", False))):
                continue                                   # fijo permanente: no borrar por no-percepción (hub incl. si hub_persist)
            ego_r = wr - ar
            ego_c = wc - ac
            # PERSIST_GANABLE ("el árbol no se olvida; lo que se olvida es si tenía fruta"): la junction
            # ganable (gray/rival) solo se REFUTA si es re-vista DE VERDAD (dentro del disco de percepción
            # real L2²≤37, no la esquina del cuadrado) y ya-no-es-de-ese-estado (percepción manda: pasa a
            # own/rival o desaparece → corrige). Fuera del disco su POSICIÓN persiste como un fijo (el árbol);
            # su ESTADO decae por confianza aparte (fungible). OFF (persist_ganable=False) ≡ cuadrado bit-exact.
            # EXTRACTOR_PERSIST (cura del eslabón): espejo de PERSIST_GANABLE para los extractores (fijos).
            # La POSICIÓN persiste fuera del disco (el árbol no se olvida); sólo el desmentido REAL borra:
            # re-visto DENTRO del disco y AUSENTE = minado hasta vaciarse (remove_source_when_empty). El
            # ESTADO (conf) decae aparte en el desempate. OFF (extractor_persist=False) ≡ bit-exact.
            if getattr(self, "extractor_persist", False) and cls.startswith("extractor_"):
                if ego_r * ego_r + ego_c * ego_c <= PERCEPTION_R2:       # re-vista REAL (disco)
                    if not self._present(ego_r, ego_c, cls, scalar_map, tag_map,
                                         own_team_tag, rival_team_tag, own_net_tag, rival_net_tag):
                        to_delete.append((wr, wc, cls))                  # vaciado/eliminado → corrige
                continue                                                 # fuera del disco → la posición persiste
            if getattr(self, "persist_ganable", False) and cls in ("junction_gray", "junction_rival"):
                if ego_r * ego_r + ego_c * ego_c <= PERCEPTION_R2:       # re-vista REAL (disco de percepción)
                    pres = self._present(ego_r, ego_c, cls, scalar_map, tag_map,
                                         own_team_tag, rival_team_tag, own_net_tag, rival_net_tag)
                    if not pres:
                        to_delete.append((wr, wc, cls))                  # desmentido real → corrige
                        if _MEM_EVENT_DBG:
                            _loc = (ego_r + AGENT_ROW) * EGOCENTRIC_COLS + (ego_c + AGENT_COL)
                            _th = tag_map.get(_loc, set())
                            _mev({"step": step, "ev": "del", "cls": cls, "cell": [wr, wc], "ego": [ego_r, ego_c],
                                  "cause": "disk_refute", "in_disk": True, "present": False,
                                  "tagcell_junction": TAG_TYPE_JUNCTION in _th, "tagcell_own": own_net_tag in _th,
                                  "tagcell_rival": rival_net_tag in _th, "tagcell_empty": len(_th) == 0})
                    elif _MEM_EVENT_DBG:
                        _mev({"step": step, "ev": "confirm", "cls": cls, "cell": [wr, wc], "ego": [ego_r, ego_c], "in_disk": True})
                elif _MEM_EVENT_DBG:
                    _mev({"step": step, "ev": "persist", "cls": cls, "cell": [wr, wc], "ego": [ego_r, ego_c], "in_disk": False})
                continue                                                 # fuera del disco → la posición persiste
            if abs(ego_r) <= WINDOW_HALF and abs(ego_c) <= WINDOW_HALF:   # línea base VALIDADA C6 (cuadrado; ver deuda §disco)
                if not self._present(ego_r, ego_c, cls, scalar_map, tag_map,
                                     own_team_tag, rival_team_tag,
                                     own_net_tag, rival_net_tag):
                    to_delete.append((wr, wc, cls))
                    if _MEM_EVENT_DBG and cls in ("junction_gray", "junction_rival", "junction_own"):
                        _loc = (ego_r + AGENT_ROW) * EGOCENTRIC_COLS + (ego_c + AGENT_COL)
                        _th = tag_map.get(_loc, set())
                        _mev({"step": step, "ev": "del", "cls": cls, "cell": [wr, wc], "ego": [ego_r, ego_c],
                              "cause": "square_refute", "in_square": True, "present": False,
                              "tagcell_junction": TAG_TYPE_JUNCTION in _th, "tagcell_own": own_net_tag in _th,
                              "tagcell_rival": rival_net_tag in _th, "tagcell_empty": len(_th) == 0})
        for k in to_delete:
            del self._entries[k]

        # ── Grabar avistamientos de este tick ─────────────────────────────

        # Hubs propios
        for (loc, dist) in debug.get("own_hubs", []):
            wr, wc = _ego_loc_to_world(loc, ar, ac)
            amp = A_F_HUB * (1.0 + dist)
            self._record(wr, wc, "hub", amp, step)

        # Solar tiles
        for (loc, dist) in debug.get("solar_tiles", []):
            wr, wc = _ego_loc_to_world(loc, ar, ac)
            amp = A_R_ENERGY * w_energy * (1.0 + dist)
            if amp > 0.0:
                self._record(wr, wc, "solar", amp, step)

        # Extractores (con tipo inferido desde tag_map)
        # Registro INCONDICIONAL (percepción manda, independiente de demanda viva).
        # El gating por demanda aplica a la proyección virtual (ghost_forces), no al registro.
        for (loc, dist, w_mat) in debug.get("extractors", []):
            tags = tag_map.get(loc, set())
            ext_types = tags & EXTRACTOR_TAGS
            for tag_type in ext_types:
                cls = _EXTRACTOR_CLS.get(tag_type, "extractor_oxygen")
                amp_ghost = A_R_MAT * w_mat * (1.0 + dist)  # para la fuerza fantasma
                wr, wc = _ego_loc_to_world(loc, ar, ac)
                self._record(wr, wc, cls, max(amp_ghost, 1e-4), step)  # siempre registra

        # Agentes (aliados y rivales) — escanear tag_map directamente
        for loc, tags in tag_map.items():
            if TAG_TYPE_AGENT not in tags:
                continue
            loc_r = loc // EGOCENTRIC_COLS - AGENT_ROW
            loc_c = loc % EGOCENTRIC_COLS - AGENT_COL
            wr = ar + loc_r
            wc = ac + loc_c
            sw = social_weight(loc)
            if own_team_tag in tags:
                amp = ALLY_WEIGHT * sw
                self._record(wr, wc, "ally", amp, step)
            elif rival_team_tag in tags:
                amp = RIVAL_WEIGHT * sw
                self._record(wr, wc, "rival", amp, step)

        # Junctions
        for loc, tags in tag_map.items():
            if TAG_TYPE_JUNCTION not in tags:
                continue
            loc_r = loc // EGOCENTRIC_COLS - AGENT_ROW
            loc_c = loc % EGOCENTRIC_COLS - AGENT_COL
            wr = ar + loc_r
            wc = ac + loc_c
            if own_net_tag in tags:
                self._record(wr, wc, "junction_own",   JUNCTION_BONUS, step)
                _mev({"step": step, "ev": "rec", "cls": "junction_own", "cell": [wr, wc], "ego": [loc_r, loc_c]})
            elif rival_net_tag in tags:
                self._record(wr, wc, "junction_rival", JUNCTION_BONUS, step)
                _mev({"step": step, "ev": "rec", "cls": "junction_rival", "cell": [wr, wc], "ego": [loc_r, loc_c]})
            elif getattr(self, "marcador_mem", False):
                # Eslabón 4 (refinamiento 2): junction GRIS (ganable) — espejo del extractor, para el
                # atractor N3 estado-gateado. NO contribuye al ghost (se salta), sí a _entries.
                self._record(wr, wc, "junction_gray", JUNCTION_BONUS, step)
                _mev({"step": step, "ev": "rec", "cls": "junction_gray", "cell": [wr, wc], "ego": [loc_r, loc_c]})

        # Eslabón 4 — gear stations (type:aligner), memorables como los extractores (gateado por marcador).
        if getattr(self, "marcador_mem", False):
            for loc, tags in tag_map.items():
                if TAG_TYPE_ALIGNER not in tags:
                    continue
                wr = ar + (loc // EGOCENTRIC_COLS - AGENT_ROW)
                wc = ac + (loc % EGOCENTRIC_COLS - AGENT_COL)
                self._record(wr, wc, "gear_aligner", JUNCTION_BONUS, step)

        # ── MEMORIA DE MUROS (GEMV_WALL_MEM) — sólidos conocidos en coords ABSOLUTAS, set separado de _entries ──
        if self.wall_mem and self.solid_types:
            st = self.solid_types
            # REGISTRO: sólidos percibidos en la ventana → _walls (permanentes; un muro no se mueve).
            for loc, tags in tag_map.items():
                if st.intersection(tags):
                    er = loc // EGOCENTRIC_COLS - AGENT_ROW
                    ec = loc % EGOCENTRIC_COLS - AGENT_COL
                    self._walls.add((ar + er, ac + ec))
            # DESMENTIDO perceptual: sólido recordado DENTRO del disco de percepción y ya NO percibido → borrar
            # (percepción manda). Barato: sólo las celdas dentro del disco disparan la comprobación.
            _drop = []
            for (wr, wc) in self._walls:
                er = wr - ar; ec = wc - ac
                if er * er + ec * ec <= PERCEPTION_R2:            # dentro del disco real de percepción
                    _loc = (er + AGENT_ROW) * EGOCENTRIC_COLS + (ec + AGENT_COL)
                    if not st.intersection(tag_map.get(_loc, ())):
                        _drop.append((wr, wc))
            for k in _drop:
                self._walls.discard(k)

        self._prune()

    # ── Campo fantasma ────────────────────────────────────────────────────────

    def ghost_forces(self) -> dict[str, float]:
        """Fuerzas fantasma para la posición actual del agente."""
        return self.ghost_forces_for_position(*self._agent_world, self._step)

    def ghost_forces_for_position(
        self, world_row: int, world_col: int, step: int
    ) -> dict[str, float]:
        """
        Fuerzas fantasma si el agente estuviera en (world_row, world_col) en `step`.

        Exclusión: se omite un objeto solo si está dentro de ±WINDOW_HALF desde la
        posición ACTUAL (self._agent_world). Esto garantiza que el objeto ya está en
        los tokens actuales y, por tanto, en los tokens predichos desplazados.

        Si el objeto está fuera de la ventana actual pero entraría en la ventana
        predicha, NO se excluye: la percepción predicha no lo contiene (no fue
        desplazado desde los tokens actuales), así que el ghost sigue siendo la
        única señal para ese objeto en la predicción.
        """
        ar, ac = self._agent_world
        forces: dict[str, float] = {}
        for (wr, wc, cls), entry in self._entries.items():
            # Excluir solo si el objeto está dentro de la ventana ACTUAL.
            # Si está en la ventana actual, está en los tokens observados y se
            # desplazará correctamente a los tokens predichos → percepción manda.
            ego_r_curr = wr - ar
            ego_c_curr = wc - ac
            if abs(ego_r_curr) <= WINDOW_HALF and abs(ego_c_curr) <= WINDOW_HALF:   # línea base VALIDADA C6 (cuadrado; ver deuda §disco)
                continue
            ego_r = wr - world_row
            ego_c = wc - world_col
            dist = math.sqrt(ego_r * ego_r + ego_c * ego_c)
            if cls in _MARCADOR_MEM_CLS:
                continue                       # marcador: memoria para el atractor N3, NO para el ghost
            age  = max(0, step - entry.last_seen_step)
            decay = math.exp(-GHOST_DECAY_LAMBDA * age)
            contrib = entry.raw_amplitude * GHOST_FACTOR * decay / (1.0 + dist)
            axis = FORCE_AXIS.get(cls, "pR")
            forces[axis] = forces.get(axis, 0.0) + contrib
        return forces

    # ── Stats para logging / M4 ───────────────────────────────────────────────

    def stats(self) -> dict:
        """Estadísticas de la memoria para logging y evaluación M4."""
        by_axis: dict[str, list[float]] = {}
        for (_, _, cls), entry in self._entries.items():
            axis = FORCE_AXIS.get(cls, "pR")
            by_axis.setdefault(axis, []).append(entry.raw_amplitude)
        return {
            "n_entries": len(self._entries),
            "agent_world": self._agent_world,
            "step": self._step,
            "mean_amp_by_axis": {ax: sum(v)/len(v) for ax, v in by_axis.items()},
        }

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def agent_world(self) -> tuple[int, int]:
        return self._agent_world

    @property
    def n_entries(self) -> int:
        return len(self._entries)

    # ── Privados ──────────────────────────────────────────────────────────────

    def _record(self, wr: int, wc: int, cls: str, raw_amplitude: float, step: int) -> None:
        """Grabar o actualizar una entrada. Mantiene el máximo raw_amplitude visto."""
        key = (wr, wc, cls)
        existing = self._entries.get(key)
        if existing is None or raw_amplitude > existing.raw_amplitude:
            self._entries[key] = EntradaMemoria(
                object_class=cls,
                raw_amplitude=raw_amplitude,
                last_seen_step=step,
            )
        else:
            # Actualizar timestamp aunque la amplitud sea menor (objeto sigue ahí)
            existing.last_seen_step = step

    def _prune(self) -> None:
        if len(self._entries) <= MAX_MEMORY_ENTRIES:
            return
        by_amp = sorted(self._entries.items(), key=lambda kv: kv[1].raw_amplitude)
        excess = len(self._entries) - MAX_MEMORY_ENTRIES
        for k, _ in by_amp[:excess]:
            del self._entries[k]

    def _present(
        self, ego_r: int, ego_c: int, cls: str,
        scalar_map: dict, tag_map: dict,
        own_team_tag, rival_team_tag, own_net_tag, rival_net_tag,
    ) -> bool:
        """True si el objeto de clase `cls` está en posición egocéntrica (ego_r, ego_c)."""
        loc = (ego_r + AGENT_ROW) * EGOCENTRIC_COLS + (ego_c + AGENT_COL)
        if cls == "hub":
            tags = tag_map.get(loc, set())
            return TAG_TYPE_HUB in tags and own_team_tag in tags
        elif cls == "solar":
            return scalar_map.get((loc, FID_INV_SOLAR), 0) > 0
        elif cls.startswith("extractor"):
            ext_map = {v: k for k, v in _EXTRACTOR_CLS.items()}
            tag_needed = ext_map.get(cls)
            if tag_needed is None:
                return False
            tags = tag_map.get(loc, set())
            return tag_needed in tags
        elif cls == "ally":
            tags = tag_map.get(loc, set())
            return TAG_TYPE_AGENT in tags and own_team_tag in tags
        elif cls == "rival":
            tags = tag_map.get(loc, set())
            return TAG_TYPE_AGENT in tags and rival_team_tag in tags
        elif cls == "junction_own":
            tags = tag_map.get(loc, set())
            return TAG_TYPE_JUNCTION in tags and own_net_tag in tags
        elif cls == "junction_rival":
            tags = tag_map.get(loc, set())
            return TAG_TYPE_JUNCTION in tags and rival_net_tag in tags
        elif cls == "junction_gray":                      # Eslabón 4: gris = junction sin ningún net
            tags = tag_map.get(loc, set())
            return TAG_TYPE_JUNCTION in tags and own_net_tag not in tags and rival_net_tag not in tags
        elif cls == "gear_aligner":
            return TAG_TYPE_ALIGNER in tag_map.get(loc, set())
        return False


# ── Función de aplicación de fuerzas fantasma ────────────────────────────────

def apply_ghost(state: State, ghost: dict[str, float]) -> State:
    """
    Sumar fuerzas fantasma al State, con caps homeostáticos.
    Las fuerzas pS/nS de memoria NO se escalan por s_scale
    (son recuerdo, no percepción directa).
    """
    if not ghost:
        return state
    pF = min(state.pF + ghost.get("pF", 0.0), _F_POS_TARGET)
    nF = max(state.nF + ghost.get("nF", 0.0), 0.0)
    pR = min(state.pR + ghost.get("pR", 0.0), _R_POS_TARGET)
    nR = max(state.nR + ghost.get("nR", 0.0), 0.0)
    pS = max(state.pS + ghost.get("pS", 0.0), 0.0)
    nS = max(state.nS + ghost.get("nS", 0.0), 0.0)
    return State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _ego_loc_to_world(loc: int, agent_row: int, agent_col: int) -> tuple[int, int]:
    """Convertir loc egocéntrico (row*16+col) a coordenadas mundo."""
    r = loc // EGOCENTRIC_COLS - AGENT_ROW
    c = loc % EGOCENTRIC_COLS - AGENT_COL
    return (agent_row + r, agent_col + c)
