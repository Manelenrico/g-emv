"""[P7-67, campo, brazo CONGELADA] LA CONFIANZA EN LA RAZON NO SE ACTUALIZA (GEMV_P7_67_CONGELA=1; las demas piezas no se tocan). Identico a MIENTE (misma mentira, mismos
destinos, mismo juicio), pero la confianza del cuerpo en la razon se queda en 0,5 en las tres dimensiones (cuerpo, recursos, vinculo) toda la vida: el juicio se calcula y se registra
igual (P7_66_llegada con su acierto y su «confianza_despues» calculada), y justo despues la confianza vuelve a 0,5, antes de que el cuerpo vuelva a decidir.
Puntos donde se fija a 0,5: al arrancar el dia (despues de leer el cuaderno), al final de cada `decidir` (envoltura mas exterior: se aplica despues de todas las piezas, rapido_P7_43
incluido), al volcar el cuaderno y al cerrar el dia. Cada vez que la encuentra distinta deja un registro P7_67_congela (antes, tic). Registro P7_67_congela_arranque."""
import os
import descubre_P7 as X, invita_P7_54 as IN
ON = os.environ.get("GEMV_P7_67_CONGELA", "0") == "1"
FIJA = 0.5
E = {"n": 0, "registra": None, "tick": None}


def fija(donde):
    antes = dict(IN.E["conf"])
    if any(abs(antes.get(d, FIJA) - FIJA) > 1e-12 for d in ("cuerpo", "recursos", "vinculo")) or set(antes) != {"cuerpo", "recursos", "vinculo"}:
        IN.E["conf"] = {"cuerpo": FIJA, "recursos": FIJA, "vinculo": FIJA}; E["n"] += 1
        if E["registra"]: E["registra"]({"k": "P7_67_congela", "donde": donde, "tick": E["tick"], "antes": antes, "despues": dict(IN.E["conf"])})


def aplica(clase, registra=None):
    if not ON: return {"P7_67_congela": False}
    assert IN.ON, "CONGELADA va sobre invita_P7_54"
    E["registra"] = registra
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        c = _oa(criatura, ruta, registra_); fija("arranque")
        if c is not None and hasattr(c, "volcado"):
            _v = c.volcado
            def volcado(_v=_v): fija("volcado"); return _v()
            c.volcado = volcado
        if registra_: registra_({"k": "P7_67_congela_arranque", "slot": int(criatura), "confianza": dict(IN.E["conf"])})
        return c
    X.arranca = arranca
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        E["tick"] = getattr(self, "tick", None); r = _d(self, obs); fija("decidir"); return r
    clase.decidir = decidir
    _ot = X.termina
    def termina(registra_=None):
        fija("cierre")
        if registra_: registra_({"k": "P7_67_congela_cierre", "veces_fijada": E["n"], "confianza": dict(IN.E["conf"])})
        return _ot(registra_)
    X.termina = termina
    return {"P7_67_congela": True, "fija": FIJA}
