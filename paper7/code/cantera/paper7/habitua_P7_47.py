"""[P7-47] HABITUACION Y PESO DE LA INTENSIDAD (diseno de Manel; SELLO_P7_47.md). SOLO BANCO (GEMV_P7_47=1), sobre P7-40 tal cual (filo_P7_40 ya enganchada):
  (1) HABITUACION: cada prueba que acaba en "no hizo nada" (importancia escalar 0 en B1; las cortadas no cuentan) multiplica por 0,5 la curiosidad de ese objeto;
      una prueba con efecto no habitua. La habituacion vuelve hacia 1 al ritmo del olvido: h(d) = 1 - (1 - h0) x OLVIDO^(d - d0). Se aplica envolviendo
      `filo_P7_40.curiosidad` (la que leen la ignorancia nueva, E1 y los momentos). El estado viaja en el cuaderno (`habituacion_P7_47`: {objeto: {"h": h0, "dia": d0}}).
  (2) INTENSIDAD EN SU ESCALA: al cerrar cada ventana, intensidad = 1 + importancia / mediana(importancia de todo lo vivido hasta ese momento, este incluido), tope 4;
      importancia = suma de |importancia| en los tres dominios (B1, tras P7-39), sin el techo E. Mediana 0: 4 si la importancia es > 0, 1 si es 0. La de P7-40 se guarda en
      `intensidad_P7_40`. Se hace en `decidir` DESPUES de las piezas de abajo (que ya pusieron la importancia B1 y la intensidad de P7-40 en el recuerdo nuevo).
Registros: `P7_47_intensidad` (por recuerdo) y `P7_47_habitua` (por habituacion)."""
import json, os, statistics as st
import descubre_P7 as X, nace_P7_23 as N, filo_P7_40 as FI
from cuaderno_P7 import DOMINIOS, OLVIDO
ON = os.environ.get("GEMV_P7_47", "0") == "1"; FACTOR = 0.5; TOPE = 4.0
E = {"H": {}, "registra": None, "n_intensidad": 0, "n_habitua": 0, "n_efecto": 0, "mundo": None}


def importancia_escalar(r): return sum(abs(float((r.get("importancia") or {}).get(d) or 0.0)) for d in DOMINIOS)


def h_de(objeto, dia):
    x = E["H"].get(objeto)
    if not x: return 1.0
    return 1.0 - (1.0 - float(x["h"])) * (OLVIDO ** max(0, int(dia) - int(x["dia"])))


def h_todas(dia): return {o: round(h_de(o, dia), 4) for o in E["H"]}


def aplica(clase, registra=None):
    if not ON: return {"P7_47": False}
    assert os.environ.get("GEMV_P7_40") == "1", "P7-47 va sobre P7-40"
    E["registra"] = registra
    # (1) la curiosidad de filo_P7_40, por el factor h del objeto
    _oc = FI.curiosidad
    def curiosidad(c, mundo, objeto, cautela=1.0, _oc=_oc):
        return _oc(c, mundo, objeto, cautela) * h_de(objeto, c.dia_actual())
    FI.curiosidad = curiosidad
    # el estado viaja en el cuaderno
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        c = _oa(criatura, ruta, registra_)
        E["H"] = {}
        if ruta and os.path.exists(ruta) and X.CUADERNO_ON and not X.BORRADO:
            try: E["H"] = dict((json.load(open(ruta)).get("habituacion_P7_47") or {}))
            except Exception: E["H"] = {}
        if c is not None:
            _v0 = c.volcado
            def volcado(_v0=_v0):
                d = _v0(); d["habituacion_P7_47"] = E["H"]; return d
            c.volcado = volcado
        return c
    X.arranca = arranca
    # (2) la intensidad en su escala y (1) la habituacion, al cerrar cada ventana
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        n0 = len(X.ESTADO.get("huellas") or [])
        accion, radio = _d(self, obs)
        c = N.cuaderno(); E["mundo"] = self.mundo
        if c is None or getattr(self, "phase", None) != "live" or self.mundo is None: return accion, radio
        nuevas = (X.ESTADO.get("huellas") or [])[n0:]
        if not nuevas: return accion, radio
        dia = c.dia_actual()
        for h in nuevas:
            if h.get("corte"): continue
            obj = h.get("objeto") or X.kit(self.mundo); rec = [r for r in c.recuerdos_de(obj) if r.get("tick") == h.get("t0")]
            if not rec: continue
            r = rec[-1]
            if r.get("intensidad_P7_47"): continue
            s = importancia_escalar(r)
            vividos = [importancia_escalar(q) for o_, s_, q in c.recuerdos() if not q.get("corte") and q is not r] + [s]
            med = st.median(vividos)
            inten = (min(TOPE, 1.0 + s / med) if med > 0 else (TOPE if s > 0 else 1.0))
            r["intensidad_P7_40"] = r.get("intensidad"); r["intensidad"] = round(inten, 4); r["intensidad_P7_47"] = True; r["mediana_vivida"] = round(med, 4); E["n_intensidad"] += 1
            if registra: registra({"k": "P7_47_intensidad", "tick": self.tick, "objeto": obj, "importancia": round(s, 4), "mediana_vivida": round(med, 4), "n_vividos": len(vividos), "intensidad": r["intensidad"], "intensidad_P7_40": r["intensidad_P7_40"]})
            if s <= 0.0:
                h0 = h_de(obj, dia) * FACTOR; E["H"][obj] = {"h": round(h0, 6), "dia": dia}; E["n_habitua"] += 1
                if registra: registra({"k": "P7_47_habitua", "tick": self.tick, "objeto": obj, "h": round(h0, 4), "dia": dia})
            else: E["n_efecto"] += 1
        return accion, radio
    clase.decidir = decidir
    return {"P7_47": True, "factor": FACTOR, "tope": TOPE}


def estado(): return {"H": E["H"], "n_intensidad": E["n_intensidad"], "n_habitua": E["n_habitua"], "n_efecto": E["n_efecto"]}
