"""Memoria episódica v1.1 — el CLIP como unidad (diseño de Manel; enmienda de v1).

Spec: [doc de diseño interna, no en el repo] (§ENMIENDA v1.1). Extiende memoria_v2 (odometría, decaimiento,
percepción-manda, campo fantasma vía ghost_forces_for_position + apply_ghost). Motor/amplitudes/mundo
INTOCADOS. GEMV_EPISODIC ∈ {off, terr}: off ≡ conducta actual.

INVARIANTE DE CONDUCTA (G4): el índice de proyección `_terr` (celda-mundo→territorio, percepción-manda) se
mantiene por-tick IDÉNTICO a v1, y `ghost_forces_for_position` lo lee igual. Los CLIPS son una capa de
registro/consulta alimentada por las MISMAS observaciones: no tocan la proyección. Por eso T2 no se mueve.
"""
from __future__ import annotations

import math
import sys
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from memoria.memoria_v1 import (
    GHOST_FACTOR, GHOST_DECAY_LAMBDA, WINDOW_HALF, MAX_MEMORY_ENTRIES,
    ACTION_DELTAS, apply_ghost,
)
from appraisal.appraisal_v3 import (
    EGOCENTRIC_COLS, AGENT_ROW, AGENT_COL,
    TAG_TYPE_AGENT, TAG_TYPE_HUB, TAG_TEAM_COGS, TAG_TEAM_CLIPS,
    TERR_OWN, TERR_RIVAL, TERR_OWN_BONUS, TERR_RIVAL_PENALTY,
)

# ── TEMPERAMENTO de la memoria (Manel; valores iniciales declarados; NO calibrar vs veredictos) ──
BUFFER_B: int = 5        # buffer rodante: últimos B ticks retenidos (el "antes" del evento)
THETA_OPEN: float = 0.3  # |Δd| que dispara la apertura de un clip
THETA_CLOSE: float = 0.1 # |Δd| por debajo del cual el paisaje se considera calmo
CALM_C: int = 3          # ticks calmos consecutivos para cerrar un clip


@dataclass
class Fotograma:
    """Un fotograma del clip: las 3 partes de Manel + enlace temporal (tick + acción)."""
    step: int
    position: tuple[int, int]        # 1. POSICIÓN (odometría mundo)
    context: dict                    # 2. CONTEXTO (suelo + entidades)
    landscape: dict                  # 3. PAISAJE (6 fuerzas + d)
    action: str | None = None        # enlace: acción tomada DESDE este fotograma


@dataclass
class Clip:
    """Un pequeño evento (Live Photo): apertura, fotogramas, huella espacial, cierre."""
    open_step: int
    open_salience: float
    frames: list = field(default_factory=list)
    footprint: set = field(default_factory=set)   # posiciones-mundo de los fotogramas
    closed_step: int | None = None


@dataclass
class _TerrCell:
    territory: int
    amplitude: float
    last_seen_step: int


class EpisodicaMemoriaV1:
    """Registro por CLIPS; SOLO el canal territorial proyecta (índice `_terr`, invariante de conducta)."""

    def __init__(self) -> None:
        self._agent_world: tuple[int, int] = (0, 0)
        self._step: int = 0
        # Proyección (IDÉNTICA a v1) — no la tocan los clips.
        self._terr: dict[tuple[int, int], _TerrCell] = {}
        # Registro de EXTRACTORES percibidos (competidor 1d-bis): {(wr,wc): (inv_fid, last_seen_step)}.
        # Dato inerte para la conducta OFF (no lo leen ghost/terr/appraise); lo usa el planner si el
        # interruptor GEMV_VIRTUAL_EXTRACT está ON (extractor recordado = cosechable virtual fuera de ventana).
        self._extractors: dict[tuple[int, int], tuple[int, int]] = {}
        # Registro por clips.
        self._buffer: deque = deque(maxlen=BUFFER_B)
        self._clips: list[Clip] = []
        self._open: Clip | None = None
        self._calm: int = 0
        self._last_mag: float | None = None
        self._last_frame: Fotograma | None = None

    def reset(self) -> None:
        self._agent_world = (0, 0)
        self._step = 0
        self._terr.clear()
        self._extractors.clear()
        self._buffer.clear()
        self._clips.clear()
        self._open = None
        self._calm = 0
        self._last_mag = None
        self._last_frame = None

    def step_tick(self, action: str, blocked: bool = False) -> None:
        # Enlace temporal: el fotograma de este tick guarda la acción tomada desde él.
        if self._last_frame is not None:
            self._last_frame.action = action
        # Odometría (IDÉNTICA a v1).
        self._step += 1
        if not blocked:
            dr, dc = ACTION_DELTAS.get(action, (0, 0))
            ar, ac = self._agent_world
            self._agent_world = (ar + dr, ac + dc)

    # ── Grabación por clips + proyección (índice territorial invariante) ────────
    def observe(self, debug: dict, scalar_map: dict, tag_map: dict, team_side: str) -> None:
        ar, ac = self._agent_world
        step = self._step
        terr = debug.get("territory")

        s_scale = debug.get("s_scale", 1.0)
        landscape = {
            "pF": debug.get("pF_v3", 0.0), "nF": debug.get("raw_nF", 0.0),
            "pR": debug.get("pR_v3", 0.0), "nR": debug.get("raw_nR", 0.0),
            "pS": debug.get("pS_raw", 0.0) * s_scale, "nS": debug.get("nS_raw", 0.0) * s_scale,
            "d": debug.get("d", None),
        }
        own_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
        rival_tag = TAG_TEAM_CLIPS if team_side == "cogs" else TAG_TEAM_COGS
        n_ally = n_rival = n_hub = 0
        for loc, tags in tag_map.items():
            if TAG_TYPE_AGENT in tags:
                if own_tag in tags: n_ally += 1
                elif rival_tag in tags: n_rival += 1
            if TAG_TYPE_HUB in tags: n_hub += 1
        context = {"territory": terr, "n_ally": n_ally, "n_rival": n_rival, "n_hub": n_hub}

        frame = Fotograma(step=step, position=(ar, ac), context=context, landscape=landscape)
        self._last_frame = frame

        # ── Máquina de clips (registro): saliencia = |Δd| (magnitud del paisaje) ──
        mag = landscape["d"] if landscape["d"] is not None else 0.0
        salience = abs(mag - self._last_mag) if self._last_mag is not None else 0.0
        self._last_mag = mag
        self._buffer.append(frame)
        if self._open is None:
            if salience > THETA_OPEN:
                # APERTURA: rescatar el buffer (el "antes") y empezar el clip.
                self._open = Clip(open_step=step, open_salience=salience,
                                  frames=list(self._buffer))
                for f in self._open.frames:
                    self._open.footprint.add(f.position)
                self._calm = 0
        else:
            self._open.frames.append(frame)
            self._open.footprint.add(frame.position)
            if salience < THETA_CLOSE:
                self._calm += 1
                if self._calm >= CALM_C:
                    self._open.closed_step = step
                    self._clips.append(self._open)
                    self._open = None
                    if len(self._clips) > MAX_MEMORY_ENTRIES:
                        self._clips = self._clips[-MAX_MEMORY_ENTRIES:]
            else:
                self._calm = 0

        # ── Proyección territorial: índice `_terr` (IDÉNTICO a v1; percepción manda) ──
        if terr == TERR_OWN:
            self._terr[(ar, ac)] = _TerrCell(TERR_OWN, TERR_OWN_BONUS, step)
        elif terr == TERR_RIVAL:
            self._terr[(ar, ac)] = _TerrCell(TERR_RIVAL, TERR_RIVAL_PENALTY, step)
        elif (ar, ac) in self._terr:
            del self._terr[(ar, ac)]

        # ── Registro de EXTRACTORES percibidos (posición mundo + inv_fid del elemento) ──
        # Dato inerte para OFF; simetría por canal: el extractor opera en el PLANNER (previsión), no aquí.
        import appraisal.appraisal_v3 as _av3
        ext_by_tag = getattr(_av3, "EXTRACTOR_TYPE_INFO", None)
        if ext_by_tag:
            for loc, tags in tag_map.items():
                for t in tags:
                    if t in ext_by_tag:
                        row, col = divmod(loc, EGOCENTRIC_COLS)
                        wr, wc = ar + (row - AGENT_ROW), ac + (col - AGENT_COL)
                        self._extractors[(wr, wc)] = (ext_by_tag[t][0], step)   # inv_fid p0 + last_seen
                        break

    # ── Extractores VIRTUALES para el planner (competidor 1d-bis) ────────────────
    def virtual_extractors_rel(self, demanded_inv_fids, max_age: int | None = None) -> list:
        """Extractores recordados del elemento DEMANDADO, FUERA de ventana (percepción manda dentro),
        como (rel_row, rel_col, inv_fid) relativos a la posición ACTUAL del agente. Con edad > max_age
        se descartan (decaimiento/staleness). Gateado por demanda viva vía `demanded_inv_fids`."""
        ar, ac = self._agent_world
        out = []
        for (wr, wc), (inv_fid, last_seen) in self._extractors.items():
            if inv_fid not in demanded_inv_fids:
                continue
            rr, rc = wr - ar, wc - ac
            if abs(rr) <= WINDOW_HALF and abs(rc) <= WINDOW_HALF:
                continue   # en ventana: la percepción directa (tokens reales) manda; no duplicar
            if max_age is not None and (self._step - last_seen) > max_age:
                continue
            out.append((rr, rc, inv_fid))
        return out

    # ── Campo fantasma territorial (IDÉNTICO a v1) ──────────────────────────────
    def ghost_forces(self) -> dict[str, float]:
        return self.ghost_forces_for_position(*self._agent_world, self._step)

    def ghost_forces_for_position(self, world_row: int, world_col: int, step: int) -> dict[str, float]:
        ar, ac = self._agent_world
        forces: dict[str, float] = {}
        for (wr, wc), cell in self._terr.items():
            if abs(wr - ar) <= WINDOW_HALF and abs(wc - ac) <= WINDOW_HALF:
                continue
            dr = wr - world_row; dc = wc - world_col
            dist = math.sqrt(dr * dr + dc * dc)
            age = max(0, step - cell.last_seen_step)
            decay = math.exp(-GHOST_DECAY_LAMBDA * age)
            contrib = cell.amplitude * GHOST_FACTOR * decay / (1.0 + dist)
            axis = "pF" if cell.territory == TERR_OWN else "nF"
            forces[axis] = forces.get(axis, 0.0) + contrib
        return forces

    # ── Consulta por proximidad (anclaje geométrico; sin cliente nuevo) ─────────
    def clips_near(self, position: tuple[int, int], radius: float) -> list[Clip]:
        pr, pc = position
        out = []
        for clip in self._clips + ([self._open] if self._open else []):
            if any((wr - pr) ** 2 + (wc - pc) ** 2 <= radius * radius for (wr, wc) in clip.footprint):
                out.append(clip)
        return out

    # ── Introspección / dump ────────────────────────────────────────────────────
    def stats(self) -> dict:
        n_own = sum(1 for c in self._terr.values() if c.territory == TERR_OWN)
        n_riv = sum(1 for c in self._terr.values() if c.territory == TERR_RIVAL)
        n_frames = sum(len(c.frames) for c in self._clips) + (len(self._open.frames) if self._open else 0)
        return {
            "n_clips": len(self._clips), "n_open": 1 if self._open else 0, "n_frames": n_frames,
            "n_terr_own": n_own, "n_terr_rival": n_riv,
            "agent_world": self._agent_world, "step": self._step,
            "n_entries": n_frames, "mean_amp_by_axis": {},  # compat log
        }

    def dump_movie(self, k_clips: int = 4) -> list[dict]:
        """La internación como PELÍCULA: k clips con apertura, fotogramas (3 partes + acción) y cierre."""
        clips = self._clips + ([self._open] if self._open else [])
        out = []
        for clip in clips[:k_clips]:
            out.append({
                "open_step": clip.open_step, "open_salience": round(clip.open_salience, 3),
                "closed_step": clip.closed_step, "n_frames": len(clip.frames),
                "footprint_size": len(clip.footprint),
                "frames": [{
                    "step": f.step, "pos": f.position, "action": f.action,
                    "terr": f.context["territory"], "allies": f.context["n_ally"], "rivals": f.context["n_rival"],
                    "pF": round(f.landscape["pF"], 2), "nF": round(f.landscape["nF"], 2),
                    "d": round(f.landscape["d"], 2) if f.landscape["d"] is not None else None,
                } for f in clip.frames],
            })
        return out

    @property
    def agent_world(self) -> tuple[int, int]:
        return self._agent_world

    @property
    def n_entries(self) -> int:
        return sum(len(c.frames) for c in self._clips) + (len(self._open.frames) if self._open else 0)
