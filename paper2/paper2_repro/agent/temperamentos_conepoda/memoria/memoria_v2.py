"""
Memoria espacial v2 — habituación logarítmica por eje.

Spec: [doc de diseño interna, no en el repo]
Hereda todo de memoria_v1 excepto ghost_forces_for_position.

Cambio único respecto a v1:
  - v1: forces[axis] += Σ c_i  (suma bruta → satura cap con N objetos)
  - v2: forces[axis] = GHOST_HAB_SCALE × log(1 + Σc_i / GHOST_HAB_SCALE)
        (rendimiento decreciente → el campo fantasma nunca satura el cap)

Interruptor (GEMV_USE_MEMORY):
  0 → OFF (Fase 1)
  1 → ON v1 (suma bruta)
  2 → ON v2 (habituación — este módulo)

motor/model.py INTOCABLE. Política greedy 1-paso exacta. Appraisal v3 sin cambios.
"""
from __future__ import annotations

import math

from memoria.memoria_v1 import (
    MemoriaEspacial as _MemoriaV1,
    apply_ghost,           # noqa: F401 — re-exportar para compatibilidad
    GHOST_FACTOR,
    GHOST_DECAY_LAMBDA,
    WINDOW_HALF,
    FORCE_AXIS,
)

GHOST_HAB_SCALE: float = 0.4
"""
Escala de habituación logarítmica.

f(x) = GHOST_HAB_SCALE × log(1 + x / GHOST_HAB_SCALE)

Propiedades con GHOST_HAB_SCALE=0.4:
  - f(0)   = 0
  - f(1.0) = 0.50   (1 tile solar en HAMBRE: 50% de v1)
  - f(16)  = 1.485  (16 tiles solares: margen 0.515 bajo cap pR=2.0)
  - f(15) + direct_pR(dist=3) = 1.460+0.500 = 1.960 < 2.0 (gradiente percepción directa visible)
  - Monotona creciente, nunca negativa; para x << SCALE → f(x) ≈ x
"""


class MemoriaEspacial(_MemoriaV1):
    """
    Memoria espacial v2 con habituación logarítmica.

    Idéntica a v1 en todo salvo ghost_forces_for_position, donde las
    contribuciones individuales por eje se agregan con f(Σc_i) = HAB_SCALE ×
    log(1 + Σc_i / HAB_SCALE) en lugar de la suma bruta de v1.
    """

    def ghost_forces_for_position(
        self, world_row: int, world_col: int, step: int
    ) -> dict[str, float]:
        """
        Fuerzas fantasma habituadas para la posición (world_row, world_col).

        Exclusión: igual que v1 — se omite un objeto solo si está en la ventana
        ACTUAL (self._agent_world). El fix del bug de repulsión se hereda.

        Habituación: las contribuciones brutas se acumulan por eje y al final
        se aplica f(sum) = GHOST_HAB_SCALE × log(1 + sum / GHOST_HAB_SCALE).
        """
        ar, ac = self._agent_world
        raw_sums: dict[str, float] = {}

        for (wr, wc, cls), entry in self._entries.items():
            ego_r_curr = wr - ar
            ego_c_curr = wc - ac
            if abs(ego_r_curr) <= WINDOW_HALF and abs(ego_c_curr) <= WINDOW_HALF:
                continue
            ego_r = wr - world_row
            ego_c = wc - world_col
            dist = math.sqrt(ego_r * ego_r + ego_c * ego_c)
            age = max(0, step - entry.last_seen_step)
            decay = math.exp(-GHOST_DECAY_LAMBDA * age)
            contrib = entry.raw_amplitude * GHOST_FACTOR * decay / (1.0 + dist)
            axis = FORCE_AXIS.get(cls, "pR")
            raw_sums[axis] = raw_sums.get(axis, 0.0) + contrib

        forces: dict[str, float] = {}
        for axis, s in raw_sums.items():
            forces[axis] = GHOST_HAB_SCALE * math.log(1.0 + s / GHOST_HAB_SCALE)
        return forces
