"""[P7-65] SIN CONTRASTE PARA «COGER» (decision de Manel, 15-oct; GEMV_P7_65=1), enganchada DESPUES de juicio_P7_62 (que no se toca) y antes de rapido_P7_43.
En el cuaderno no hay recuerdos de COGER una cosa, solo de USARLA: comparar lo contado por la hermana (usos) con una promesa sobre coger mezclaria dos actos. Por eso las invitaciones
de COGER (COGER_BOTIQUIN, COGER_RACION, COGER_RED, COGER_CAMUFLAJE; la falsa de P7-65 es COGER_BOTIQUIN en amenaza, +30) no entran en el contraste con lo contado: solo las juzga lo
vivido (invita_P7_54, sin cambio: el siguiente uso de esa cosa en 480 tics o, si no lo hay, el cambio de vida en 480 tics). Declarado: vale para toda invitacion de coger (el cuerpo no
sabe cual es la falsa); las demas se contrastan como en P7-62 (juicio_P7_62.contrasta, en su situacion).
Registros: P7_65_arranque, P7_65_cierre (contrastes en los que se aparto alguna invitacion de coger)."""
import os
import descubre_P7 as X, invita_P7_54 as IN, invita_P7_57 as IC, juicio_P7_62 as J62
ON = os.environ.get("GEMV_P7_65", "0") == "1"
E = {"apartadas": 0}


def sin_coger(inv): return [i for i in inv if not str(i.get("accion", "")).startswith("COGER_")]


def contrasta(c, mundo, tick, registra):
    """= juicio_P7_62.contrasta sobre las invitaciones cargadas SIN las de coger"""
    todas = IN.E["inv"]
    try:
        IN.E["inv"] = sin_coger(todas); E["apartadas"] += len(todas) - len(IN.E["inv"]) if IN.E["inv"] != todas else 0
        if IN.E["inv"]: J62.contrasta(c, mundo, tick, registra)
    finally:
        IN.E["inv"] = todas


def aplica(clase, registra=None):
    if not ON: return {"P7_65": False}
    assert J62.ON and IN.ON and IC.ON, "P7-65 va sobre juicio_P7_62 (y P7-54, P7-57)"
    IC.contrasta = contrasta
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        c = _oa(criatura, ruta, registra_)
        if registra_: registra_({"k": "P7_65_arranque", "slot": int(criatura), "invitaciones": len(IN.E["inv"]), "de_coger_sin_contraste": len(IN.E["inv"]) - len(sin_coger(IN.E["inv"])), "falsas": sum(1 for i in IN.E["inv"] if i.get("falsa"))})
        return c
    X.arranca = arranca
    _ot = X.termina
    def termina(registra_=None):
        if registra_: registra_({"k": "P7_65_cierre", "confianza": dict(IN.E["conf"])})
        return _ot(registra_)
    X.termina = termina
    return {"P7_65": True}
