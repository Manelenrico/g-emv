"""memoria/rastreo.py — Eslabón 3: memoria de RASTREO por zonas (exploración).

D1: cada tick marca las teselas cubiertas por la ventana (verla basta). D2: frescura = 1 −
confianza, con la MISMA curva episódica que toda la memoria del agente (GHOST_DECAY_HALFLIFE=500).
Cero mecanismos nuevos de memoria: se reusa la constante estándar. Spec: [doc de diseño interna, no en el repo].
"""
from __future__ import annotations

import math
from memoria.memoria_v1 import GHOST_DECAY_HALFLIFE   # decaimiento episódico estándar (500)

TILE: int = 6                                   # lado de tesela ≈ radio de ventana (spec §1)
_LAMBDA: float = math.log(2) / GHOST_DECAY_HALFLIFE


class RastreoZonas:
    """Teselas vistas → last_seen_step. Frescura decaída con la curva estándar."""

    def __init__(self, tile: int = TILE) -> None:
        self.tile = tile
        self._seen: dict[tuple[int, int], int] = {}

    def mark_window(self, ar: int, ac: int, radius: int, step: int) -> None:
        """Marca como rastreadas TODAS las teselas que solapan la ventana [ar±radius]×[ac±radius]."""
        t = self.tile
        for tr in range((ar - radius) // t, (ar + radius) // t + 1):
            for tc in range((ac - radius) // t, (ac + radius) // t + 1):
                self._seen[(tr, tc)] = step

    def confidence(self, tr: int, tc: int, step: int) -> float:
        """exp(−λ·edad); 0 si nunca vista (candidata máxima)."""
        ls = self._seen.get((tr, tc))
        if ls is None:
            return 0.0
        return math.exp(-_LAMBDA * max(0, step - ls))

    def fresh_attractor_rel(self, ar: int, ac: int, step: int, ring: int = 2):
        """Dirección relativa (dr,dc en CELDAS) al centro de la tesela MENOS rastreada (más fresca)
        alcanzable dentro de `ring` teselas. Empata por cercanía (L1 en teselas). None si no hay
        candidata mejor que la tesela actual (raro). La tesela actual se excluye (dtr=dtc=0)."""
        t = self.tile
        cur_tr, cur_tc = ar // t, ac // t
        best_key = None   # (frescura, -dist_teselas)
        best_rel = None
        for dtr in range(-ring, ring + 1):
            for dtc in range(-ring, ring + 1):
                if dtr == 0 and dtc == 0:
                    continue
                tr, tc = cur_tr + dtr, cur_tc + dtc
                fresh = 1.0 - self.confidence(tr, tc, step)
                key = (fresh, -(abs(dtr) + abs(dtc)))
                if best_key is None or key > best_key:
                    # centro de la tesela en celdas del mundo, relativo al agente
                    cell_r = tr * t + t // 2 - ar
                    cell_c = tc * t + t // 2 - ac
                    best_key, best_rel = key, (cell_r, cell_c)
        # si la mejor frescura es ~0 (todo recién visto por igual), no hay pull útil
        if best_key is None or best_key[0] <= 1e-9:
            return None
        return best_rel

    def coverage(self) -> int:
        """Nº de teselas distintas rastreadas (para el gate f)."""
        return len(self._seen)

    def frontier_rel(self, ar: int, ac: int, step: int, ring: int = 12, cap: int = 7):
        """ESLABÓN FORRAJEO (F1): dirección GLOBAL hacia la frontera de lo NO rastreado (escala mapa, no
        ring=2). Busca la tesela MÁS fresca (menos rastreada) en ±ring teselas; empata por CERCANÍA (la
        frontera más próxima → progreso sostenido hacia afuera). Devuelve (rel_celdas_capado, frescura):
        la dirección al centro de esa tesela, recortada a `cap` celdas (para que la fuerza-d γ^L1 del canal
        GAIN sea significativa y SOSTENGA la dirección tick a tick); frescura ∈ [0,1] para saturar la fuerza
        (zona ya explorada → frescura 0 → fuerza 0). (None,0) si todo el entorno está recién rastreado."""
        t = self.tile
        cur_tr, cur_tc = ar // t, ac // t
        best = None   # (key=(-fresh, dist), rel, fresh)
        for dtr in range(-ring, ring + 1):
            for dtc in range(-ring, ring + 1):
                if dtr == 0 and dtc == 0:
                    continue
                tr, tc = cur_tr + dtr, cur_tc + dtc
                fresh = 1.0 - self.confidence(tr, tc, step)
                key = (-fresh, abs(dtr) + abs(dtc))     # max frescura, luego min distancia (frontera cercana)
                if best is None or key < best[0]:
                    cr = tr * t + t // 2 - ar
                    cc = tc * t + t // 2 - ac
                    best = (key, (cr, cc), fresh)
        if best is None or best[2] <= 1e-9:
            return None, 0.0
        (cr, cc), fresh = best[1], best[2]
        d = abs(cr) + abs(cc)
        if d > cap and d > 0:                            # recortar a `cap` celdas (waypoint sostenido)
            cr = int(round(cr * cap / d)); cc = int(round(cc * cap / d))
        return (cr, cc), fresh
