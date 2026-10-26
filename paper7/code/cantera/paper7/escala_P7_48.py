"""[P7-48] LA INTENSIDAD EN SU ESCALA, sola (= la parte 2 de habitua_P7_47, SIN la habituacion: no se dispara, fuera hasta saber medir "nada"; Manel, 12-oct).
Al cerrar cada ventana: intensidad = 1 + importancia / mediana(importancia de todo lo vivido hasta ese momento, este incluido), tope 4; importancia = suma de
|importancia| en los tres dominios (B1, tras P7-39). Mediana 0: 4 si la importancia es > 0, 1 si es 0. La de P7-40 queda en `intensidad_P7_40`. Marca `origen` = "vivido"
en cada recuerdo nuevo (P7-48). GEMV_P7_48_ESCALA=1, enganchada DESPUES de filo_P7_40."""
import os, statistics as st
import descubre_P7 as X, nace_P7_23 as N
from cuaderno_P7 import DOMINIOS
ON = os.environ.get("GEMV_P7_48_ESCALA", "0") == "1"; TOPE = 4.0
E = {"n_intensidad": 0, "registra": None}


def importancia_escalar(r): return sum(abs(float((r.get("importancia") or {}).get(d) or 0.0)) for d in DOMINIOS)


def escala(c, s, excluye=None):
    """1 + s / mediana de las importancias de todos los recuerdos sin corte del cuaderno (este incluido), tope 4."""
    vividos = [importancia_escalar(q) for o_, s_, q in c.recuerdos() if not q.get("corte") and q is not excluye] + [s]
    med = st.median(vividos)
    return (min(TOPE, 1.0 + s / med) if med > 0 else (TOPE if s > 0 else 1.0)), med, len(vividos)


def aplica(clase, registra=None):
    if not ON: return {"P7_48_escala": False}
    assert os.environ.get("GEMV_P7_40") == "1", "la escala va sobre P7-40"
    E["registra"] = registra
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        n0 = len(X.ESTADO.get("huellas") or [])
        accion, radio = _d(self, obs)
        c = N.cuaderno()
        if c is None or getattr(self, "phase", None) != "live" or self.mundo is None: return accion, radio
        for h in (X.ESTADO.get("huellas") or [])[n0:]:
            obj = h.get("objeto") or X.kit(self.mundo); rec = [r for r in c.recuerdos_de(obj) if r.get("tick") == h.get("t0")]
            if not rec: continue
            r = rec[-1]; r.setdefault("origen", "vivido")
            if h.get("corte") or r.get("intensidad_P7_48"): continue
            s = importancia_escalar(r); inten, med, nv = escala(c, s, excluye=r)
            r["intensidad_P7_40"] = r.get("intensidad"); r["intensidad"] = round(inten, 4); r["intensidad_P7_48"] = True; r["mediana_vivida"] = round(med, 4); E["n_intensidad"] += 1
            if registra: registra({"k": "P7_48_intensidad", "tick": self.tick, "objeto": obj, "importancia": round(s, 4), "mediana_vivida": round(med, 4), "n_vividos": nv, "intensidad": r["intensidad"], "intensidad_P7_40": r["intensidad_P7_40"]})
        return accion, radio
    clase.decidir = decidir
    return {"P7_48_escala": True, "tope": TOPE}
