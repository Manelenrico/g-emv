"""
Núcleo matemático: modelo de fuerzas oponentes tridimensional.

Cada eje (F físico, R recursos, S social) tiene dos fuerzas:
  f+  — fuerza de aproximación/placer
  f-  — fuerza de evitación/displacer

Relaciones fundamentales:
  posición_a  = f+_a − f-_a   (estado neto observable)
  tensión_a   = f+_a + f-_a   (intensidad/arousal en ese eje)

La emoción emerge cuando el equilibrio de tensiones se rompe.
"""

from __future__ import annotations
import math


# ── Rangos físicos de las variables del agente ──────────────────────────────
HP_EQ: float       = 75.0
HP_SCALE: float    = 25.0
HP_CAP: float      = 100.0

ENERGY_EQ: float   = 10.0
ENERGY_SCALE: float = 5.0
ENERGY_CAP: float  = 20.0

S_MAX: float = 2.0


# ── Targets posicionales (dónde quiere estar el agente) ─────────────────────
F_POS_TARGET: float = 1.0    # hp=100 → F=+1 (máximo alcanzable)
R_POS_TARGET: float = 2.0    # energy=20 → R=+2 (máximo alcanzable)
S_POS_TARGET: float = 0.8    # pertenencia social moderada

# ── Targets de tensión (nivel de implicación deseado — no cero) ─────────────
# Tensión < target → aburrimiento (poca implicación)
# Tensión > target → estrés/arousal excesivo
F_TEN_TARGET: float = 0.30
R_TEN_TARGET: float = 0.30
S_TEN_TARGET: float = 0.15

# ── Pesos: posición vs tensión por eje ──────────────────────────────────────
W_F_POS: float = 1.0;  W_F_TEN: float = 0.40
W_R_POS: float = 1.0;  W_R_TEN: float = 0.40
W_S_POS: float = 0.70; W_S_TEN: float = 0.25

# ── Acoplamiento asimétrico ──────────────────────────────────────────────────
# La tensión negativa física (nF alta = amenaza física) amplifica la urgencia
# en los ejes R y S. Lo físico pesa más.
F_COUPLING: float = 0.50


# ── Descomposición en fuerzas oponentes ─────────────────────────────────────

def opponent_forces(
    hp: float,
    energy: float,
    s: float,
) -> tuple[float, float, float, float, float, float]:
    """Descompone el estado observable en 6 fuerzas oponentes.

    Retorna (pF, nF, pR, nR, pS, nS).
    Cada par satisface: posición = p − n, tensión = p + n.
    Todas son no-negativas.
    """
    pF = max(0.0, (hp      - HP_EQ    ) / HP_SCALE     )
    nF = max(0.0, (HP_EQ   - hp       ) / HP_SCALE     )

    pR = max(0.0, (energy  - ENERGY_EQ) / ENERGY_SCALE )
    nR = max(0.0, (ENERGY_EQ - energy ) / ENERGY_SCALE )

    pS = max(0.0,  s)
    nS = max(0.0, -s)

    return pF, nF, pR, nR, pS, nS


def opponent_distance(
    hp: float,
    energy: float,
    s: float,
) -> float:
    """Distancia homeostática con estructura de fuerzas oponentes.

    Penaliza:
      1. Desviación posicional respecto a los targets.
      2. Tensión demasiado baja (aburrimiento) o demasiado alta (estrés).
      3. Acoplamiento: amenaza física amplifica urgencia material y social.
    """
    pF, nF, pR, nR, pS, nS = opponent_forces(hp, energy, s)

    pos_F, ten_F = pF - nF, pF + nF
    pos_R, ten_R = pR - nR, pR + nR
    pos_S, ten_S = pS - nS, pS + nS

    d_pos = (
        W_F_POS * (pos_F - F_POS_TARGET) ** 2 +
        W_R_POS * (pos_R - R_POS_TARGET) ** 2 +
        W_S_POS * (pos_S - S_POS_TARGET) ** 2
    )

    d_ten = (
        W_F_TEN * (ten_F - F_TEN_TARGET) ** 2 +
        W_R_TEN * (ten_R - R_TEN_TARGET) ** 2 +
        W_S_TEN * (ten_S - S_TEN_TARGET) ** 2
    )

    coupling = F_COUPLING * nF * (
        (pos_R - R_POS_TARGET) ** 2 + (pos_S - S_POS_TARGET) ** 2
    )

    return math.sqrt(d_pos + d_ten + coupling)


def state_summary(hp: float, energy: float, s: float) -> dict:
    """Retorna un diccionario con todas las magnitudes para análisis."""
    pF, nF, pR, nR, pS, nS = opponent_forces(hp, energy, s)
    return {
        "hp": hp, "energy": energy, "s": s,
        "pF": pF, "nF": nF, "pos_F": pF - nF, "ten_F": pF + nF,
        "pR": pR, "nR": nR, "pos_R": pR - nR, "ten_R": pR + nR,
        "pS": pS, "nS": nS, "pos_S": pS - nS, "ten_S": pS + nS,
        "distance": opponent_distance(hp, energy, s),
    }


if __name__ == "__main__":
    scenarios = [
        ("Plena salud, energía, social",    100.0, 20.0,  1.5),
        ("Equilibrio (referencia)",          75.0, 10.0,  0.0),
        ("Bajo en energía",                  75.0,  2.0,  0.5),
        ("Amenaza física",                   20.0, 15.0,  0.0),
        ("Aislado sin recursos",             60.0,  0.0, -1.0),
    ]
    header = f"{'Escenario':<32} {'pos_F':>6} {'pos_R':>6} {'pos_S':>6} " \
             f"{'ten_F':>6} {'ten_R':>6} {'ten_S':>6} {'dist':>7}"
    print(header)
    print("-" * len(header))
    for name, hp, en, s in scenarios:
        r = state_summary(hp, en, s)
        print(
            f"{name:<32} {r['pos_F']:>6.2f} {r['pos_R']:>6.2f} {r['pos_S']:>6.2f} "
            f"{r['ten_F']:>6.2f} {r['ten_R']:>6.2f} {r['ten_S']:>6.2f} {r['distance']:>7.4f}"
        )
