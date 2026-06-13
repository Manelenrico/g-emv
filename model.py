"""
Núcleo matemático: modelo de fuerzas oponentes tridimensional.
"""

from __future__ import annotations
import math
from dataclasses import dataclass


# ════════════════════════════════════════════════════════════════════════════
# PRINCIPIOS  (estructura matemática — no negociable sin cambiar la teoría)
# ════════════════════════════════════════════════════════════════════════════
#
#  Por cada eje  a ∈ {F (físico), R (recursos), S (social)}:
#    f⁺_a ≥ 0  fuerza de aproximación / placer
#    f⁻_a ≥ 0  fuerza de evitación   / displacer
#
#  POSICIÓN  pos_a = f⁺_a − f⁻_a        (estado neto observable)
#  TENSIÓN   ten_a = f⁺_a + f⁻_a        (intensidad / arousal del eje)
#
#  La distancia homeostática penaliza dos cosas independientes:
#    1. Desviación posicional respecto al estado ideal.
#    2. Desviación de tensión respecto al target de tensión (no cero).
#       ten < target  →  understimulation  (señal geométrica de aburrimiento)
#       ten > target  →  overstimulation   (señal de estrés/saturación)
#
#  ACOPLAMIENTO ASIMÉTRICO (principio, no calibración):
#    La amenaza física (nF > 0) amplifica la urgencia en R y S.
#    Forma: coupling = F_COUPLING · nF · [(pos_R − tgt_R)² + (pos_S − tgt_S)²]
#
#  LIMITACIÓN ESTRUCTURAL (honestidad):
#    Con la descomposición max(0,·), f⁺ y f⁻ nunca son ambas positivas a la
#    vez: ten_a = |pos_a|. Esto implica que posición y tensión son redundantes
#    en el eje. Para capturar ambas como grados de libertad independientes
#    se requeriría una descomposición con línea base (p.ej. cosh/sinh) o
#    variables dinámicas separadas para f⁺ y f⁻.
#
# ════════════════════════════════════════════════════════════════════════════


# ════════════════════════════════════════════════════════════════════════════
# CONSTANTES DE DOMINIO  (del agente y su entorno)
# No son parámetros libres de la teoría, sino del contexto empírico.
# ════════════════════════════════════════════════════════════════════════════

HP_EQ: float        = 75.0   # salud de equilibrio
HP_SCALE: float     = 25.0   # escala de normalización del eje F
HP_CAP: float       = 100.0  # salud máxima alcanzable

ENERGY_EQ: float    = 10.0   # energía de equilibrio
ENERGY_SCALE: float = 5.0    # escala de normalización del eje R
ENERGY_CAP: float   = 20.0   # energía máxima alcanzable

S_MAX: float        = 2.0    # amplitud del eje social (−S_MAX a +S_MAX)


# ════════════════════════════════════════════════════════════════════════════
# CALIBRACIONES LIBRES  (parámetros ajustables sin cambiar la teoría)
# Son la sintonización del modelo en este dominio.
# Todos los experimentos varían solo un subconjunto de estos.
# ════════════════════════════════════════════════════════════════════════════

@dataclass
class ModelConfig:
    # Targets posicionales: dónde quiere estar el agente
    f_pos_target: float = 1.0   # HP_CAP → pos_F = 1.0
    r_pos_target: float = 2.0   # ENERGY_CAP → pos_R = 2.0
    s_pos_target: float = 0.8   # pertenencia social moderada-alta

    # Targets de tensión: nivel óptimo de arousal en cada eje (nunca cero)
    # CLAVE DE FENOTIPO — el Experimento 1 varía solo r_ten_target:
    #   Explorador → valor alto (quiere más arousal/estimulación)
    #   Apático    → valor bajo  (se satisface con poco)
    f_ten_target: float = 0.30
    r_ten_target: float = 0.30
    s_ten_target: float = 0.15

    # Pesos relativos entre posición y tensión, por eje
    w_f_pos: float = 1.0
    w_f_ten: float = 0.40
    w_r_pos: float = 1.0
    w_r_ten: float = 0.40
    w_s_pos: float = 0.70
    w_s_ten: float = 0.25

    # Coeficiente de acoplamiento asimétrico F → R, S
    # Un valor mayor hace que la amenaza física domine toda la agenda
    f_coupling: float = 0.50


DEFAULT_CONFIG = ModelConfig()


# ════════════════════════════════════════════════════════════════════════════
# FUNCIONES PRINCIPALES
# ════════════════════════════════════════════════════════════════════════════

def opponent_forces(
    hp: float, energy: float, s: float,
) -> tuple[float, float, float, float, float, float]:
    """Descompone el estado en las 6 fuerzas oponentes (pF, nF, pR, nR, pS, nS).

    Garantía: pos_a = p_a − n_a,  ten_a = p_a + n_a,  p_a ≥ 0,  n_a ≥ 0.
    """
    pF = max(0.0, (hp        - HP_EQ    ) / HP_SCALE    )
    nF = max(0.0, (HP_EQ     - hp       ) / HP_SCALE    )
    pR = max(0.0, (energy    - ENERGY_EQ) / ENERGY_SCALE)
    nR = max(0.0, (ENERGY_EQ - energy   ) / ENERGY_SCALE)
    pS = max(0.0,  s)
    nS = max(0.0, -s)
    return pF, nF, pR, nR, pS, nS


def opponent_distance(
    hp: float, energy: float, s: float,
    cfg: ModelConfig = DEFAULT_CONFIG,
) -> float:
    """Distancia homeostática al estado ideal.

    Componentes:
      d_pos  — desviación posicional (apunta hacia el estado ideal)
      d_ten  — desviación de tensión (penaliza under- y over-activation)
      coupling — amenaza física amplifica urgencia material y social
    """
    pF, nF, pR, nR, pS, nS = opponent_forces(hp, energy, s)

    pos_F, ten_F = pF - nF, pF + nF
    pos_R, ten_R = pR - nR, pR + nR
    pos_S, ten_S = pS - nS, pS + nS

    d_pos = (
        cfg.w_f_pos * (pos_F - cfg.f_pos_target) ** 2 +
        cfg.w_r_pos * (pos_R - cfg.r_pos_target) ** 2 +
        cfg.w_s_pos * (pos_S - cfg.s_pos_target) ** 2
    )
    d_ten = (
        cfg.w_f_ten * (ten_F - cfg.f_ten_target) ** 2 +
        cfg.w_r_ten * (ten_R - cfg.r_ten_target) ** 2 +
        cfg.w_s_ten * (ten_S - cfg.s_ten_target) ** 2
    )
    coupling = cfg.f_coupling * nF * (
        (pos_R - cfg.r_pos_target) ** 2 +
        (pos_S - cfg.s_pos_target) ** 2
    )
    return math.sqrt(d_pos + d_ten + coupling)


def state_summary(
    hp: float, energy: float, s: float,
    cfg: ModelConfig = DEFAULT_CONFIG,
) -> dict:
    """Todas las magnitudes del estado para análisis o depuración."""
    pF, nF, pR, nR, pS, nS = opponent_forces(hp, energy, s)
    return {
        "hp": hp, "energy": energy, "s": s,
        "pF": pF, "nF": nF, "pos_F": pF - nF, "ten_F": pF + nF,
        "pR": pR, "nR": nR, "pos_R": pR - nR, "ten_R": pR + nR,
        "pS": pS, "nS": nS, "pos_S": pS - nS, "ten_S": pS + nS,
        "distance": opponent_distance(hp, energy, s, cfg),
    }


if __name__ == "__main__":
    scenarios = [
        ("Plena salud, energía, social",    100.0, 20.0,  1.5),
        ("Equilibrio (referencia)",          75.0, 10.0,  0.0),
        ("Bajo en energía",                  75.0,  2.0,  0.5),
        ("Amenaza física",                   20.0, 15.0,  0.0),
        ("Aislado sin recursos",             60.0,  0.0, -1.0),
    ]
    hdr = (f"{'Escenario':<32} {'pos_F':>6} {'pos_R':>6} {'pos_S':>6} "
           f"{'ten_F':>6} {'ten_R':>6} {'ten_S':>6} {'dist':>7}")
    print(hdr); print("-" * len(hdr))
    for name, hp, en, s in scenarios:
        r = state_summary(hp, en, s)
        print(f"{name:<32} {r['pos_F']:>6.2f} {r['pos_R']:>6.2f} {r['pos_S']:>6.2f} "
              f"{r['ten_F']:>6.2f} {r['ten_R']:>6.2f} {r['ten_S']:>6.2f} {r['distance']:>7.4f}")
