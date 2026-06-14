"""
Núcleo matemático: modelo de fuerzas oponentes tridimensional.

Versión 2 — fuerzas verdaderamente independientes.
Las seis fuerzas (pF, nF, pR, nR, pS, nS) son VARIABLES DE ESTADO
independientes, no derivadas de un único escalar por eje. Posición y tensión
emergen de la suma y la resta y son magnitudes independientes entre sí.
"""

from __future__ import annotations
import math
from dataclasses import dataclass


# ════════════════════════════════════════════════════════════════════════════
# PRINCIPIOS  (estructura matemática — no negociable sin cambiar la teoría)
# ════════════════════════════════════════════════════════════════════════════
#
#  ESTADO: seis fuerzas oponentes independientes
#  ──────────────────────────────────────────────
#  Por cada eje  a ∈ {F (físico), R (recursos), S (social)}:
#    f⁺_a ≥ 0   fuerza de aproximación / placer    (magnitud, nunca negativa)
#    f⁻_a ≥ 0   fuerza de evitación / displacer    (magnitud, nunca negativa)
#
#  Las dos fuerzas de un eje son INDEPENDIENTES: pueden subir o bajar por
#  separado, o ambas simultáneamente. La negatividad la lleva QUÉ fuerza es
#  (f⁻ ya tira hacia lo negativo), no su magnitud.
#
#  MAGNITUDES DERIVADAS por eje (no son variables primarias):
#    posición  pos_a = f⁺_a − f⁻_a   (hacia qué polo está inclinado el eje)
#    tensión   ten_a = f⁺_a + f⁻_a   (carga total / intensidad / arousal)
#
#  CONSECUENCIA CLAVE — calma vs. tensión contenida:
#    (f⁺=1, f⁻=1)  →  pos=0, ten=2   calma en equilibrio
#    (f⁺=3, f⁻=3)  →  pos=0, ten=6   tensión contenida
#    Misma posición, tensión muy distinta. El modelo los distingue.
#    La implementación anterior (v1) no podía hacerlo: con max(0,·) la
#    tensión era siempre |posición| — un solo grado de libertad por eje.
#
#  DISTANCIA HOMEOSTÁTICA
#  ──────────────────────
#    d²  =  d_pos  +  d_ten  +  coupling
#
#    d_pos    penaliza la desviación posicional respecto al descentramiento
#             basal (f_pos_target, r_pos_target, s_pos_target).
#    d_ten    penaliza la desviación de tensión respecto al arousal óptimo
#             (f_ten_target, r_ten_target, s_ten_target).
#             ten < target → understimulation; ten > target → overstimulation.
#    coupling acoplamiento asimétrico: amenaza física (nF > 0) amplifica la
#             urgencia en R y S.
#             coupling = f_coupling · nF · [(pos_R − tgt_R)² + (pos_S − tgt_S)²]
#
# ════════════════════════════════════════════════════════════════════════════


# ════════════════════════════════════════════════════════════════════════════
# CONSTANTES DE DOMINIO  (del agente y su entorno — no libres de la teoría)
# ════════════════════════════════════════════════════════════════════════════

HP_EQ: float        = 75.0   # salud de equilibrio
HP_SCALE: float     = 25.0   # escala de normalización del eje F
HP_CAP: float       = 100.0  # salud máxima alcanzable

ENERGY_EQ: float    = 10.0   # energía de equilibrio
ENERGY_SCALE: float = 5.0    # escala de normalización del eje R
ENERGY_CAP: float   = 20.0   # energía máxima alcanzable

S_MAX: float        = 2.0    # amplitud del eje social


# ════════════════════════════════════════════════════════════════════════════
# CALIBRACIONES LIBRES  (ajustables sin cambiar la teoría)
# ════════════════════════════════════════════════════════════════════════════

@dataclass
class ModelConfig:
    # Descentramiento basal: hacia dónde apunta la posición ideal
    f_pos_target: float = 1.0    # eje F: inclinado al polo positivo (salud)
    r_pos_target: float = 2.0    # eje R: inclinado a la abundancia
    s_pos_target: float = 0.8    # eje S: pertenencia social moderada-alta

    # Arousal óptimo: nivel de tensión saludable por eje (nunca cero)
    f_ten_target: float = 0.30
    r_ten_target: float = 0.30
    s_ten_target: float = 0.15

    # Pesos relativos posición / tensión por eje
    w_f_pos: float = 1.0;  w_f_ten: float = 0.40
    w_r_pos: float = 1.0;  w_r_ten: float = 0.40
    w_s_pos: float = 0.70; w_s_ten: float = 0.25

    # Coeficiente del acoplamiento físico asimétrico
    f_coupling: float = 0.50


DEFAULT_CONFIG = ModelConfig()


# ════════════════════════════════════════════════════════════════════════════
# ESTADO — seis fuerzas oponentes independientes
# ════════════════════════════════════════════════════════════════════════════

@dataclass
class State:
    """Las seis fuerzas oponentes como variables de estado independientes.

    Todas las magnitudes son ≥ 0.  El signo de la experiencia emerge de la
    resta (pos = f⁺ − f⁻); la magnitud nunca es negativa.

    A diferencia de la v1, pF y nF PUEDEN ser ambas positivas a la vez:
    eso representa tensión contenida (f⁺=3, f⁻=3 → pos=0, ten=6).
    Para representar ese estado, construir directamente:
        State(pF=3.0, nF=3.0, ...)
    Para inicializar desde observables físicos, usar state_from_observables().
    """

    # PENDIENTE §3 (Decisiones_nucleo): MÍNIMO BASAL DE TENSIÓN.
    #   La esfera no se desinfla a cero: ten_a = pF + nF ≥ TEN_BASAL_MIN.
    #   Decisión pendiente: ¿cota por eje individual o sobre la suma global?
    #   Implementar cuando se formalice la sección de límites de volumen.

    # PENDIENTE §3 (Decisiones_nucleo): MÁXIMO NORMAL y MÁXIMO DE EMERGENCIA.
    #   Máximo normal:     sum(ten_F + ten_R + ten_S) ≤ VOL_MAX_NORMAL
    #   Techo blando:      bajo demanda extrema el sistema puede superar
    #                      VOL_MAX_NORMAL un porcentaje, con coste energético.
    #   Implementar cuando se formalice la sección de límites de volumen.

    pF: float = 0.0  # f⁺_F — aproximación física / placer / vitalidad
    nF: float = 0.0  # f⁻_F — amenaza física / daño / vulnerabilidad
    pR: float = 0.0  # f⁺_R — abundancia de recursos / energía disponible
    nR: float = 0.0  # f⁻_R — escasez / carencia de recursos
    pS: float = 0.0  # f⁺_S — vínculo social / pertenencia
    nS: float = 0.0  # f⁻_S — rechazo / aislamiento / amenaza social

    # ── Magnitudes derivadas — NO son variables primarias ─────────────────
    # pos_a = f⁺_a − f⁻_a  (posición: signo neto del eje)
    # ten_a = f⁺_a + f⁻_a  (tensión: carga total del eje)

    @property
    def pos_F(self) -> float: return self.pF - self.nF
    @property
    def ten_F(self) -> float: return self.pF + self.nF

    @property
    def pos_R(self) -> float: return self.pR - self.nR
    @property
    def ten_R(self) -> float: return self.pR + self.nR

    @property
    def pos_S(self) -> float: return self.pS - self.nS
    @property
    def ten_S(self) -> float: return self.pS + self.nS


def state_from_observables(hp: float, energy: float, s: float) -> State:
    """Inicializa un State a partir de observables físicos (hp, energy, s).

    Usa la descomposición max(0,·): en el State resultante, exactamente una
    de las dos fuerzas de cada eje es cero — la situación más simple, donde
    el sistema no tiene tensión interna más allá de la posición.

    Para estados con ambas fuerzas > 0 (tensión contenida, ambivalencia),
    construye State(pF=..., nF=...) directamente.
    """
    return State(
        pF=max(0.0, (hp        - HP_EQ    ) / HP_SCALE    ),
        nF=max(0.0, (HP_EQ     - hp       ) / HP_SCALE    ),
        pR=max(0.0, (energy    - ENERGY_EQ) / ENERGY_SCALE),
        nR=max(0.0, (ENERGY_EQ - energy   ) / ENERGY_SCALE),
        pS=max(0.0,  s),
        nS=max(0.0, -s),
    )


# ════════════════════════════════════════════════════════════════════════════
# FUNCIONES PRINCIPALES  (operan sobre State)
# ════════════════════════════════════════════════════════════════════════════

def opponent_distance(state: State, cfg: ModelConfig = DEFAULT_CONFIG) -> float:
    """Distancia homeostática del State al estado ideal definido por cfg.

    d = sqrt(d_pos + d_ten + coupling)

    d_pos    suma ponderada de desviaciones posicionales al cuadrado
    d_ten    suma ponderada de desviaciones de tensión al cuadrado
    coupling acoplamiento físico: nF amplifica la urgencia en R y S
    """
    d_pos = (
        cfg.w_f_pos * (state.pos_F - cfg.f_pos_target) ** 2 +
        cfg.w_r_pos * (state.pos_R - cfg.r_pos_target) ** 2 +
        cfg.w_s_pos * (state.pos_S - cfg.s_pos_target) ** 2
    )
    d_ten = (
        cfg.w_f_ten * (state.ten_F - cfg.f_ten_target) ** 2 +
        cfg.w_r_ten * (state.ten_R - cfg.r_ten_target) ** 2 +
        cfg.w_s_ten * (state.ten_S - cfg.s_ten_target) ** 2
    )
    coupling = cfg.f_coupling * state.nF * (
        (state.pos_R - cfg.r_pos_target) ** 2 +
        (state.pos_S - cfg.s_pos_target) ** 2
    )
    return math.sqrt(d_pos + d_ten + coupling)


def state_summary(state: State, cfg: ModelConfig = DEFAULT_CONFIG) -> dict:
    """Todas las magnitudes del State para análisis o depuración."""
    return {
        "pF": state.pF, "nF": state.nF,
        "pos_F": state.pos_F, "ten_F": state.ten_F,
        "pR": state.pR, "nR": state.nR,
        "pos_R": state.pos_R, "ten_R": state.ten_R,
        "pS": state.pS, "nS": state.nS,
        "pos_S": state.pos_S, "ten_S": state.ten_S,
        "distance": opponent_distance(state, cfg),
    }


# ════════════════════════════════════════════════════════════════════════════
# COMPATIBILIDAD CON EXPERIMENTOS v1
# experiments.py y experiments_decentramiento.py llaman a las funciones con
# (hp, energy, s, cfg). Estos shims mantienen esa API funcionando mientras
# se actualiza cada archivo a la API nueva (State).
# ════════════════════════════════════════════════════════════════════════════

def opponent_forces(
    hp: float, energy: float, s: float,
) -> tuple[float, float, float, float, float, float]:
    """Shim v1 → v2: devuelve (pF, nF, pR, nR, pS, nS) desde observables."""
    st = state_from_observables(hp, energy, s)
    return st.pF, st.nF, st.pR, st.nR, st.pS, st.nS


def opponent_distance_obs(
    hp: float, energy: float, s: float,
    cfg: ModelConfig = DEFAULT_CONFIG,
) -> float:
    """Shim v1 → v2: distancia desde observables físicos (hp, energy, s)."""
    return opponent_distance(state_from_observables(hp, energy, s), cfg)


def state_summary_obs(
    hp: float, energy: float, s: float,
    cfg: ModelConfig = DEFAULT_CONFIG,
) -> dict:
    """Shim v1 → v2: resumen desde observables físicos."""
    return state_summary(state_from_observables(hp, energy, s), cfg)


# ════════════════════════════════════════════════════════════════════════════
# VERIFICACIÓN  (prueba del documento: calma vs. tensión contenida)
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # ── Prueba clave del documento (§1 Decisiones_nucleo) ─────────────────
    # Dos estados con la MISMA posición (pos_F=0) pero distinta tensión.
    # El modelo v2 debe distinguirlos. El v1 no podía.

    calma    = State(pF=1.0, nF=1.0)   # pos_F = 0, ten_F = 2  — calma
    cargado  = State(pF=3.0, nF=3.0)   # pos_F = 0, ten_F = 6  — tensión contenida

    cfg_test = ModelConfig(
        f_pos_target=0.0, f_ten_target=0.0,   # target neutro: eje F en cero
        r_pos_target=0.0, r_ten_target=0.0,
        s_pos_target=0.0, s_ten_target=0.0,
        f_coupling=0.0,
        w_f_pos=1.0, w_f_ten=1.0,
        w_r_pos=0.0, w_r_ten=0.0,
        w_s_pos=0.0, w_s_ten=0.0,
    )

    d_calma   = opponent_distance(calma,   cfg_test)
    d_cargado = opponent_distance(cargado, cfg_test)

    print("═══ Prueba: calma vs. tensión contenida (§1 Decisiones_nucleo) ════")
    print(f"  calma    (pF=1, nF=1):  pos_F={calma.pos_F:.1f}  ten_F={calma.ten_F:.1f}"
          f"  →  distancia={d_calma:.4f}")
    print(f"  cargado  (pF=3, nF=3):  pos_F={cargado.pos_F:.1f}  ten_F={cargado.ten_F:.1f}"
          f"  →  distancia={d_cargado:.4f}")
    print()

    assert calma.pos_F   == cargado.pos_F   == 0.0,  "posición debe ser igual"
    assert calma.ten_F   == 2.0,                     "tensión calma debe ser 2"
    assert cargado.ten_F == 6.0,                     "tensión cargado debe ser 6"
    assert d_calma != d_cargado,                     "distancias deben ser distintas"
    assert d_cargado > d_calma,                      "cargado más lejos del target neutro"

    print("  ✓  Misma posición (0.0), tensión distinta (2 vs 6).")
    print("  ✓  Distancias diferentes: el modelo los distingue.")
    print()

    # ── Sanidad: state_from_observables sigue funcionando ─────────────────
    print("═══ Sanidad: inicialización desde observables ═══════════════════")
    scenarios = [
        ("Equilibrio",        HP_EQ,  ENERGY_EQ, 0.0),
        ("Plena salud",       100.0,  20.0,       1.5),
        ("Bajo en energía",   HP_EQ,   2.0,       0.5),
        ("Amenaza física",     20.0,  15.0,       0.0),
    ]
    hdr = f"  {'Escenario':<22} {'pos_F':>6} {'ten_F':>6} {'pos_R':>6} {'ten_R':>6} {'dist':>8}"
    print(hdr); print("  " + "─" * (len(hdr) - 2))
    for name, hp, en, s in scenarios:
        st = state_from_observables(hp, en, s)
        d  = opponent_distance(st)
        print(f"  {name:<22} {st.pos_F:>6.2f} {st.ten_F:>6.2f} "
              f"{st.pos_R:>6.2f} {st.ten_R:>6.2f} {d:>8.4f}")
        # Verificar que en v2, con max(0,·), ten sigue siendo |pos| (caso especial)
        assert abs(st.ten_F - abs(st.pos_F)) < 1e-9, "sanidad: ten=|pos| para observables simples"
    print()
    print("  ✓  Observables inicializan correctamente.")
    print("  ✓  Para estos estados simples, ten = |pos| (solo una fuerza activa por eje).")
    print("     Para tensión contenida, construir State directamente.")
