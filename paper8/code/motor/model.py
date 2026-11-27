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

    # Sensibilidades del acoplamiento mutuo (cuánto arrastra cada eje a los demás)
    # El arrastre usa ten_a = f⁺_a + f⁻_a: bidireccional, oportunidad y amenaza pesos igual.
    sens_F: float = 0.30   # físico arrastra más (el cuerpo secuestra la atención)
    sens_R: float = 0.15   # recursos: arrastre medio
    sens_S: float = 0.10   # social: arrastre menor


DEFAULT_CONFIG = ModelConfig()

# CALIBRACIÓN LIBRE — tensión mínima por eje (no un principio, un parámetro)
# Un sistema con tensión cero es un sistema "muerto": la esfera nunca se
# desinfla del todo. Valor inicial propuesto: 0.10 (en las escalas del
# modelo, equivale a ~2.5 hp o ~0.5 unidades de energía desde el equilibrio).
# Ajustar empíricamente; no cambia la estructura matemática del modelo.
TEN_BASAL_MIN: float = 0.10

# CALIBRACIÓN LIBRE — techo de tensión total (valla numérica, no fenómeno)
# (ten_F + ten_R + ten_S) ≤ VOL_MAX. El presupuesto total es fijo, pero el
# reparto entre ejes es completamente libre: un eje puede acaparar casi todo
# el volumen (zepelín) mientras los otros quedan en su mínimo basal.
# Mecanismo: solo se escala el EXCEDENTE sobre TEN_BASAL_MIN. El suelo basal
# es intocable; el ajuste recae únicamente sobre quienes tienen excedente.
# Valor: 8.0 — presupuesto disponible sobre el basal = 8.0 - 3×0.10 = 7.70.
# PENDIENTE (capa dinámica futura — junto al aburrimiento):
#   Coste de salud del sobreesfuerzo: desgaste acumulado cuando el sistema
#   opera sostenidamente cerca de VOL_MAX (fenómeno temporal, no instantáneo).
#   Coste temporal: límite de cuánto tiempo puede sostenerse la saturación.
#   Estos son fenómenos de acumulación temporal — no pertenecen al núcleo
#   geométrico instantáneo. Se implementarán en la capa dinámica.
VOL_MAX: float = 8.0


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

    # MÍNIMO BASAL — implementado en __post_init__
    #   ten_a = f⁺_a + f⁻_a ≥ TEN_BASAL_MIN  por eje.
    #   Mecanismo: se añade (déficit/2) a cada fuerza del eje, preservando
    #   la posición exactamente (sumar igual a ambas se cancela en la resta).

    # TECHO ASIMÉTRICO — implementado en __post_init__ (después del mínimo)
    #   (ten_F + ten_R + ten_S) ≤ VOL_MAX.
    #   Solo se escala el excedente sobre TEN_BASAL_MIN: el suelo basal es
    #   intocable. Un eje puede acaparar casi todo el presupuesto (zepelín)
    #   mientras los otros permanecen en su mínimo exacto sin bajar de él.

    pF: float = 0.0  # f⁺_F — aproximación física / placer / vitalidad
    nF: float = 0.0  # f⁻_F — amenaza física / daño / vulnerabilidad
    pR: float = 0.0  # f⁺_R — abundancia de recursos / energía disponible
    nR: float = 0.0  # f⁻_R — escasez / carencia de recursos
    pS: float = 0.0  # f⁺_S — vínculo social / pertenencia
    nS: float = 0.0  # f⁻_S — rechazo / aislamiento / amenaza social

    def __post_init__(self) -> None:
        """Aplica los límites de volumen: mínimo basal y techo asimétrico.

        1. Mínimo basal: si f⁺_a + f⁻_a < TEN_BASAL_MIN, añade (déficit/2)
           a cada fuerza — preserva la posición, sube la tensión.
        2. Techo asimétrico: si (ten_F + ten_R + ten_S) > VOL_MAX, se escala
           solo el excedente sobre TEN_BASAL_MIN. El suelo basal es intocable.
           Los ejes con excedente=0 (en su mínimo exacto) no se modifican.
           La relación f⁺/f⁻ dentro de cada eje se conserva.
        """
        # Step 1: basal minimum
        for p_attr, n_attr in (('pF', 'nF'), ('pR', 'nR'), ('pS', 'nS')):
            fp  = getattr(self, p_attr)
            fn  = getattr(self, n_attr)
            ten = fp + fn
            if ten < TEN_BASAL_MIN:
                add = (TEN_BASAL_MIN - ten) / 2
                setattr(self, p_attr, fp + add)
                setattr(self, n_attr, fn + add)
        # Step 2: asymmetric volume ceiling — scale only surplus above basal
        total = self.ten_F + self.ten_R + self.ten_S
        if total > VOL_MAX:
            allowed_surplus = VOL_MAX - 3.0 * TEN_BASAL_MIN
            exc_F = self.ten_F - TEN_BASAL_MIN
            exc_R = self.ten_R - TEN_BASAL_MIN
            exc_S = self.ten_S - TEN_BASAL_MIN
            exc_total = exc_F + exc_R + exc_S
            if exc_total > 0.0:
                scale = allowed_surplus / exc_total
                for p_attr, n_attr, exc in (
                    ('pF', 'nF', exc_F),
                    ('pR', 'nR', exc_R),
                    ('pS', 'nS', exc_S),
                ):
                    old_ten = getattr(self, p_attr) + getattr(self, n_attr)
                    new_ten = TEN_BASAL_MIN + exc * scale
                    if old_ten > 0.0:
                        r = new_ten / old_ten
                        setattr(self, p_attr, getattr(self, p_attr) * r)
                        setattr(self, n_attr, getattr(self, n_attr) * r)

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
    coupling acoplamiento mutuo: cada eje arrastra a los otros dos.
             El arrastre usa ten_a = f⁺_a + f⁻_a (bidireccional).
             coupling = sens_F·ten_F·[(Δpos_R)²+(Δpos_S)²]
                      + sens_R·ten_R·[(Δpos_F)²+(Δpos_S)²]
                      + sens_S·ten_S·[(Δpos_F)²+(Δpos_R)²]
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
    dF = (state.pos_F - cfg.f_pos_target) ** 2
    dR = (state.pos_R - cfg.r_pos_target) ** 2
    dS = (state.pos_S - cfg.s_pos_target) ** 2
    coupling = (
        cfg.sens_F * state.ten_F * (dR + dS) +
        cfg.sens_R * state.ten_R * (dF + dS) +
        cfg.sens_S * state.ten_S * (dF + dR)
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
        sens_F=0.0, sens_R=0.0, sens_S=0.0,  # acoplamiento apagado
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

    # ── Prueba mínimo basal (§3 Decisiones_nucleo) ────────────────────────
    print("═══ Prueba: mínimo basal de tensión (TEN_BASAL_MIN={:.2f}) ════".format(TEN_BASAL_MIN))

    # Caso A: ambas fuerzas en cero → deben subir a TEN_BASAL_MIN/2 cada una
    s_cero = State(pF=0.0, nF=0.0)
    print(f"  A) State(pF=0, nF=0)     → pF={s_cero.pF:.3f}  nF={s_cero.nF:.3f}"
          f"  pos={s_cero.pos_F:.3f}  ten={s_cero.ten_F:.3f}")
    assert abs(s_cero.ten_F - TEN_BASAL_MIN) < 1e-9, "ten debe ser TEN_BASAL_MIN"
    assert abs(s_cero.pos_F) < 1e-9,                 "pos debe seguir siendo 0"

    # Caso B: una fuerza sola por debajo del mínimo → sube preservando posición
    s_bajo = State(pF=0.06, nF=0.02)   # ten=0.08 < 0.10; pos=0.04
    print(f"  B) State(pF=0.06,nF=0.02)→ pF={s_bajo.pF:.3f}  nF={s_bajo.nF:.3f}"
          f"  pos={s_bajo.pos_F:.3f}  ten={s_bajo.ten_F:.3f}")
    assert abs(s_bajo.ten_F - TEN_BASAL_MIN) < 1e-9, "ten debe ser TEN_BASAL_MIN"
    assert abs(s_bajo.pos_F - 0.04) < 1e-9,          "pos debe conservarse (0.04)"

    # Caso C: tensión ya por encima del mínimo → sin cambio
    s_alto = State(pF=1.0, nF=0.5)    # ten=1.5 > 0.10; pos=0.5
    print(f"  C) State(pF=1.0, nF=0.5) → pF={s_alto.pF:.3f}  nF={s_alto.nF:.3f}"
          f"  pos={s_alto.pos_F:.3f}  ten={s_alto.ten_F:.3f}")
    assert s_alto.pF == 1.0 and s_alto.nF == 0.5,    "sin cambio si ten > mínimo"

    # Caso D: state_from_observables en equilibrio → fuerzas cero → clampeado
    s_eq = state_from_observables(HP_EQ, ENERGY_EQ, 0.0)
    print(f"  D) observables(HP_EQ, EQ, 0) → "
          f"pF={s_eq.pF:.3f} nF={s_eq.nF:.3f} ten_F={s_eq.ten_F:.3f}  "
          f"pR={s_eq.pR:.3f} nR={s_eq.nR:.3f} ten_R={s_eq.ten_R:.3f}")
    assert abs(s_eq.ten_F - TEN_BASAL_MIN) < 1e-9, "equilibrio: ten_F clampeado"
    assert abs(s_eq.ten_R - TEN_BASAL_MIN) < 1e-9, "equilibrio: ten_R clampeado"
    assert abs(s_eq.ten_S - TEN_BASAL_MIN) < 1e-9, "equilibrio: ten_S clampeado"
    assert abs(s_eq.pos_F) < 1e-9,                 "equilibrio: pos_F sigue en 0"

    print()
    print("  ✓  Tensión en cero → sube a TEN_BASAL_MIN (pos. intacta).")
    print("  ✓  Tensión baja → sube a mínimo preservando posición.")
    print("  ✓  Tensión alta → sin cambio.")
    print("  ✓  Equilibrio observable → tensión basal en todos los ejes.")
    print()

    # ── Prueba techo asimétrico (§3 Decisiones_nucleo) ───────────────────
    print("═══ Prueba: techo asimétrico (VOL_MAX={:.1f}  presupuesto_excedente={:.2f}) ════".format(
        VOL_MAX, VOL_MAX - 3 * TEN_BASAL_MIN))

    # Caso A: total bajo el techo — sin cambio
    s_a = State(pF=1.0, nF=0.5, pR=0.8, nR=0.2, pS=0.4, nS=0.1)
    total_a = s_a.ten_F + s_a.ten_R + s_a.ten_S
    print(f"  A) Tensiones (1.5 + 1.0 + 0.5) = {total_a:.2f}  →  sin cambio (bajo techo)")
    assert total_a <= VOL_MAX,               "debe estar bajo el techo"
    assert s_a.pF == 1.0 and s_a.nF == 0.5, "sin modificación si bajo el techo"

    # Caso B — Zepelín: F acapara casi todo; R y S al mínimo basal intactos
    # Pedido: ten_F=8.0, ten_R=ten_S=TEN_BASAL_MIN → total=8.20 > VOL_MAX
    # R y S tienen exc=0 → no se tocan; F se comprime solo en su excedente
    _b = TEN_BASAL_MIN / 2
    s_b = State(pF=4.0, nF=4.0, pR=_b, nR=_b, pS=_b, nS=_b)
    total_b = s_b.ten_F + s_b.ten_R + s_b.ten_S
    print(f"  B) Zepelín (F=8.0, R=S=basal) → total={total_b:.6f}  "
          f"tenF={s_b.ten_F:.4f}  tenR={s_b.ten_R:.4f}  tenS={s_b.ten_S:.4f}")
    assert abs(total_b - VOL_MAX) < 1e-9,             "total = VOL_MAX"
    assert abs(s_b.ten_R - TEN_BASAL_MIN) < 1e-9,    "R intocable (exc=0)"
    assert abs(s_b.ten_S - TEN_BASAL_MIN) < 1e-9,    "S intocable (exc=0)"
    assert s_b.ten_F > VOL_MAX - 2 * TEN_BASAL_MIN - 0.5, "F acapara la mayor parte"
    assert abs(s_b.pos_F) < 1e-9,                    "posición F conservada (pF=nF)"

    # Caso C — Reparto: F alto, R empieza a pedir; S al basal intocable
    # Pedido: ten_F=7.70, ten_R=0.50, ten_S=0.10 → total=8.30 > VOL_MAX
    # S tiene exc=0 → intocable; F y R ceden proporcionalmente en su excedente
    s_c = State(pF=3.85, nF=3.85, pR=0.25, nR=0.25, pS=_b, nS=_b)
    total_c = s_c.ten_F + s_c.ten_R + s_c.ten_S
    print(f"  C) Reparto (F=7.70, R=0.50, S=basal) → total={total_c:.6f}  "
          f"tenF={s_c.ten_F:.4f}  tenR={s_c.ten_R:.4f}  tenS={s_c.ten_S:.4f}")
    assert abs(total_c - VOL_MAX) < 1e-9,             "total = VOL_MAX"
    assert abs(s_c.ten_S - TEN_BASAL_MIN) < 1e-9,    "S intocable (exc=0)"
    assert s_c.ten_R > TEN_BASAL_MIN,                 "R obtuvo algo (no bajó al basal)"
    assert s_c.ten_R < 0.50,                          "R comprimido desde 0.50"
    assert s_c.ten_F < 7.70,                          "F cedió parte de su excedente"
    assert abs(s_c.pos_F) < 1e-9,                    "posición F conservada"
    assert abs(s_c.pos_R) < 1e-9,                    "posición R conservada"

    # Caso D — Tres ejes con excedente: ninguno cae al basal
    # Pedido: ten_F=6.0, ten_R=4.0, ten_S=2.0 → total=12.0 > VOL_MAX
    # Todos comprimen su excedente; ratios f⁺/f⁻ por eje conservados
    s_d = State(pF=4.0, nF=2.0, pR=2.0, nR=2.0, pS=1.0, nS=1.0)
    total_d = s_d.ten_F + s_d.ten_R + s_d.ten_S
    print(f"  D) Tres ejes altos (6+4+2=12) → total={total_d:.6f}  "
          f"tenF={s_d.ten_F:.4f}  tenR={s_d.ten_R:.4f}  tenS={s_d.ten_S:.4f}")
    assert abs(total_d - VOL_MAX) < 1e-9,             "total = VOL_MAX"
    assert s_d.ten_F >= TEN_BASAL_MIN,                "F no baja del basal"
    assert s_d.ten_R >= TEN_BASAL_MIN,                "R no baja del basal"
    assert s_d.ten_S >= TEN_BASAL_MIN,                "S no baja del basal"
    assert abs(s_d.pF / s_d.nF - 2.0) < 1e-9,       "ratio F conservado (pF/nF=2)"

    print()
    print("  ✓  Bajo el techo: sin cambio.")
    print("  ✓  Zepelín: R y S intocables al mínimo; solo F comprimido.")
    print("  ✓  Reparto: S intocable; F y R comparten el ajuste en su excedente.")
    print("  ✓  Tres ejes: ninguno baja del basal; ratios f⁺/f⁻ conservados.")
    print()

    # ── Prueba acoplamiento mutuo ─────────────────────────────────────────
    # Config de aislamiento: d_pos=0 y d_ten=0 (todos los pesos en cero),
    # solo UNA sensibilidad activa. Así d² = coupling exactamente.
    # Para cada test: ten_fuente=2.0, déficit_destino=1.0 → coupling=2.0, d=√2.
    print("═══ Prueba: acoplamiento mutuo ════════════════════════════════════════")
    _BASAL = TEN_BASAL_MIN / 2

    def _iso_cfg(sf=0.0, sr=0.0, ss=0.0):
        return ModelConfig(
            f_pos_target=0.0, r_pos_target=0.0, s_pos_target=0.0,
            f_ten_target=0.0, r_ten_target=0.0, s_ten_target=0.0,
            w_f_pos=0.0, w_r_pos=0.0, w_s_pos=0.0,
            w_f_ten=0.0, w_r_ten=0.0, w_s_ten=0.0,
            sens_F=sf, sens_R=sr, sens_S=ss,
        )

    # Caso A: F arrastra R — ten_F=2, pos_R=1.0, sens_F=1.0
    # coupling = 1.0 · 2.0 · (1.0² + 0²) = 2.0
    st_FA = State(pF=1.0, nF=1.0, pR=1.0, nR=0.0, pS=_BASAL, nS=_BASAL)
    d_FA = opponent_distance(st_FA, _iso_cfg(sf=1.0))
    print(f"  A) F→R  (ten_F=2, pos_R=1): coupling={d_FA**2:.4f}  d={d_FA:.4f}  "
          f"(esperado d²=2.0, d={2.0**0.5:.4f})")
    assert abs(d_FA ** 2 - 2.0) < 1e-9, "F arrastra R: d²=2.0"

    # Caso B: R arrastra F — ten_R=2, pos_F=1.0, sens_R=1.0
    # coupling = 1.0 · 2.0 · (1.0² + 0²) = 2.0
    st_RF = State(pF=1.0, nF=0.0, pR=1.0, nR=1.0, pS=_BASAL, nS=_BASAL)
    d_RF = opponent_distance(st_RF, _iso_cfg(sr=1.0))
    print(f"  B) R→F  (ten_R=2, pos_F=1): coupling={d_RF**2:.4f}  d={d_RF:.4f}  "
          f"(esperado d²=2.0, d={2.0**0.5:.4f})")
    assert abs(d_RF ** 2 - 2.0) < 1e-9, "R arrastra F: d²=2.0"

    # Caso C: S arrastra F — ten_S=2, pos_F=1.0, sens_S=1.0
    # coupling = 1.0 · 2.0 · (1.0² + 0²) = 2.0
    st_SF = State(pF=1.0, nF=0.0, pR=_BASAL, nR=_BASAL, pS=1.0, nS=1.0)
    d_SF = opponent_distance(st_SF, _iso_cfg(ss=1.0))
    print(f"  C) S→F  (ten_S=2, pos_F=1): coupling={d_SF**2:.4f}  d={d_SF:.4f}  "
          f"(esperado d²=2.0, d={2.0**0.5:.4f})")
    assert abs(d_SF ** 2 - 2.0) < 1e-9, "S arrastra F: d²=2.0"

    # Caso D: alta tensión sin déficit → acoplamiento cero
    # ten_F=2, pos_R=0=target, pos_S=0=target → coupling=0 aunque sens_F alto
    st_nodep = State(pF=1.0, nF=1.0, pR=_BASAL, nR=_BASAL, pS=_BASAL, nS=_BASAL)
    d_nodep = opponent_distance(st_nodep, _iso_cfg(sf=1.0))
    print(f"  D) ten_F=2, R y S sin déficit: coupling={d_nodep**2:.6f}  "
          f"(esperado 0 — la tensión sola no genera acoplamiento)")
    assert abs(d_nodep) < 1e-9, "sin déficit: coupling=0"

    print()
    print("  ✓  F arrastra R y S: d²=2.0 cuando ten_F=2 y déficit_R=1.")
    print("  ✓  R arrastra F y S: d²=2.0 cuando ten_R=2 y déficit_F=1.")
    print("  ✓  S arrastra F y R: d²=2.0 cuando ten_S=2 y déficit_F=1.")
    print("  ✓  Tensión alta sin déficit posicional → acoplamiento cero.")
    print()
