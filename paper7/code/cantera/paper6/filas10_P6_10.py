"""[P6-10] LAS DOS FILAS DE LA DISTANCIA, desde fuera. ARCHIVO NUEVO.

No toca `model.py` ni el cinco. Envuelve `appraisal_zs_v42_exp.appraise` EN
MEMORIA: llama al original, quita la S-SOLEDAD del cinco (la que cuenta la voz
como presencia) y mete la suya, y anade S-COMPANIA reconfigurada. Las dos filas
YA EXISTEN en la tabla y en `REPARTO` (las dos (0,1 · 0,1 · 0,8)); no hay fila
nueva: cambia como se calculan.

DECISIONES DE MANEL (P6-10): estar lejos del hermano es un peligro para los
dos, a mas distancia mas dolor, con escapadas largas solo en mucha calma; la
voz del hermano dice donde esta pero NO quita la soledad.

─── S-COMPANIA ───────────────────────────────────────────────────────────────
  d        distancia de CAMINO (`decisor_zs.campo_geodesico`, no euclidea) desde
           mi casilla prevista a la del hermano: la vista si lo veo, la del parte
           fresco si no (`mem.parte_fresco`). Sin ninguna de las dos: muda.
  D0 = 7   RADIO DE RESCATE, medido en P6-9: un rival armado mata en 154 tics
           (mediana de las 29 muertes de A0+A1+A2); la mitad son 77 tics; entre
           los 11 tics por casilla del mundo, 7,00 casillas. Dentro de D0: cero.
  amenaza  = max(F-4-ALCANCE, S-7-AGRESOR, F-HERMANO-AMENAZA, F-HERMANO-GOLPE)
           las cuatro filas de miedo que el cuerpo ya calcula: hostil a mi
           alcance, yo cazado, el hermano amenazado o golpeado. Se dejan fuera
           F-DANO (es herida, no amenaza) y S-8 (exposicion, que con los ojos
           cuenta contados y ya pesa por su lado). calma = 1 - amenaza.
  rango    = D0 x (1 + CALMA_K x calma): con amenaza plena la fila llega a su
           techo a 2·D0 = 14 casillas; en calma total, a (2+CALMA_K)·D0 = 28.
           "Mas despacio cuanta mas calma": la pendiente es techo/rango.
  M        = TECHO x min(1, (d - D0) / rango)   si d > D0, si no 0.
  TECHO    el peso: lo fija el banco (P6-10 § 3b). Activa SIEMPRE (tambien fuera
           de la calma); el veto de `Bloqueos` sigue mandando sobre los candidatos.

─── S-SOLEDAD ────────────────────────────────────────────────────────────────
  DECISION DE MANEL (cambio antes de jugar): la lejania graduada la lleva
  S-COMPANIA; para no contar dos veces la misma distancia, S-SOLEDAD NO se
  enciende por distancia: queda solo para cuando el hermano ha MUERTO, como en
  el cinco, y la voz sigue sin contar como presencia. Con el hermano vivo la
  S-SOLEDAD del cinco vale 0 en todos los diarios de P6-6 y P6-8 (P6-9 § 4:
  el parte llega cada 25/48 tics y cuenta como compania), asi que "solo muerto"
  se cumple por construccion y ESTE ENVOLTORIO NO TOCA S-SOLEDAD. (Una version
  anterior de este archivo, no jugada, la encendia por distancia; retirada.)

─── LA POSICION DEL HERMANO ──────────────────────────────────────────────────
  La obs PREVISTA de cada candidato (`decisor_zs._obs_prevista`) mete al
  hermano como visible en su ULTIMA POSICION VISTA (`mem.pareja_pos`, que puede
  ser rancia) cuando la casilla prevista lo tendria a la vista. Por eso la
  distancia de S-COMPANIA NO se lee de la obs prevista: se toma la posicion REAL
  de ese tic (vista, o la del parte fresco), guardada una vez por tic en
  `D.candidatos` con la obs real (`mem._herm10`).
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from alma import appraisal_zs_v42_exp as A                 # noqa: E402
from alma import decisor_zs as D                          # noqa: E402

D0 = 7                                   # casillas de camino (P6-9, medido)
CALMA_K = 2.0
TECHO = float(os.environ.get("GEMV_COMPANIA_TECHO", "0") or 0)   # lo fija el banco
FILAS_ON = (os.environ.get("GEMV_FILAS10", "1") or "1") not in ("0", "", "no")
AMENAZA_FILAS = ("F-4-ALCANCE", "S-7-AGRESOR", "F-HERMANO-AMENAZA", "F-HERMANO-GOLPE")

_CAMPOS = {}


def entorno():
    return {"efectivo": {"FILAS10": FILAS_ON, "D0": D0, "CALMA_K": CALMA_K, "TECHO": TECHO,
                         "SOLEDAD_TECHO": A.SOLEDAD_TECHO, "SOLEDAD_RAMPA_S": A.SOLEDAD_RAMPA_S}}


def d_camino(mundo, desde, hasta):
    """Pasos de camino de `desde` a `hasta`; None si no hay camino."""
    k = (id(mundo), tuple(hasta))
    campo = _CAMPOS.get(k)
    if campo is None:
        campo = D.campo_geodesico(mundo, tuple(hasta)) or {}
        if len(_CAMPOS) > 64:
            _CAMPOS.clear()
        _CAMPOS[k] = campo
    v = campo.get(tuple(desde))
    return int(v) if v is not None else None


def amenaza_de(F):
    return max(0.0, min(1.0, max(float(F.get(n) or 0.0) for n in AMENAZA_FILAS)))


def compania_M(d, amenaza, techo=None):
    """M de S-COMPANIA. d None = sin camino: se trata como lejos del todo."""
    t = TECHO if techo is None else techo
    if t <= 0.0:
        return 0.0
    if d is None:
        return t
    if d <= D0:
        return 0.0
    rango = D0 * (1.0 + CALMA_K * (1.0 - amenaza))
    return t * min(1.0, (d - D0) / rango)


def pos_hermano(obs, mundo, mem, tick):
    """(pos, visto) del hermano: la vista, o la del parte fresco; (None, False)."""
    herm = getattr(mundo, "teammate_slot", None)
    for a in ((obs.get("visible") or {}).get("agents") or []):
        if a.get("slot") == herm and a.get("pos"):
            return (int(a["pos"][0]), int(a["pos"][1])), True
    pf = getattr(mem, "parte_fresco", None)
    p = pf(tick) if callable(pf) else None
    if p and p.get("pos"):
        return (int(p["pos"][0]), int(p["pos"][1])), False
    return None, False


def aplica(registra=None):
    """Engancha las dos filas. Devuelve lo enganchado."""
    if not FILAS_ON:
        return {"filas10": False}
    _orig_appraise = A.appraise
    _orig_cands = D.candidatos
    fF_c, fR_c, fS_c = A.REPARTO["S-COMPANIA"]

    def _cands(obs, mundo, mem, tick, bloqueos=None):
        # una vez por tic, con la obs REAL: donde esta el hermano (vista o parte)
        try:
            mem._herm10 = (tick,) + pos_hermano(obs, mundo, mem, tick)
        except Exception:
            pass
        return _orig_cands(obs, mundo, mem, tick, bloqueos)

    def _appraise(obs, mundo, mem, tick):
        st, radio = _orig_appraise(obs, mundo, mem, tick)
        if getattr(mem, "pareja_muerta", False):
            return st, radio
        pos = tuple((obs.get("you") or {}).get("pos") or ())
        h = getattr(mem, "_herm10", None)
        ph = h[1] if h and h[0] == tick else None
        if not pos or ph is None:
            return st, radio
        d = d_camino(mundo, pos, ph)
        F = {k: v.get("M", 0.0) for k, v in (radio.get("filas") or {}).items()}
        m_c = compania_M(d, amenaza_de(F))
        if os.environ.get("GEMV_FILAS10_DEBUG") and tick == int(os.environ["GEMV_FILAS10_DEBUG"]):
            print("   FILAS10", tick, "pos", pos, "ph", ph, "d", d, "amenaza", round(amenaza_de(F), 3), "m_c", round(m_c, 4))
        if m_c <= 0.0:
            return st, radio
        # se parte de las fuerzas CRUDAS (antes del __post_init__ de State)
        cr = radio.get("fuerzas_crudas") or {}
        st2 = A.State(pF=cr.get("pF", st.pF), nF=cr.get("nF", st.nF) + m_c * fF_c,
                      pR=cr.get("pR", st.pR), nR=cr.get("nR", st.nR) + m_c * fR_c,
                      pS=cr.get("pS", st.pS), nS=cr.get("nS", st.nS) + m_c * fS_c)
        radio.setdefault("filas", {})["S-COMPANIA"] = {"M": round(m_c, 5), "signo": "-", "F": round(m_c * fF_c, 5),
                                                       "R": round(m_c * fR_c, 5), "S": round(m_c * fS_c, 5)}
        radio["fuerzas_state"] = {"pF": round(st2.pF, 5), "nF": round(st2.nF, 5), "pR": round(st2.pR, 5),
                                  "nR": round(st2.nR, 5), "pS": round(st2.pS, 5), "nS": round(st2.nS, 5)}
        return st2, radio

    A.appraise = _appraise
    D.candidatos = _cands
    return {"filas10": True, "D0": D0, "CALMA_K": CALMA_K, "TECHO": TECHO}
