"""[P7-40] LA ESPERANZA DE CLASE Y EL MIEDO QUE CALLA EL PROBAR, NO EL MIRAR (diseno decidido por Manel; SELLO_P7_40.md). SOLO BANCO (GEMV_P7_40=1), sobre B1 de P7-39:
el filtro `efecto_P7_39` (GEMV_P7_39=1) y la pieza `contrafactual_P7_38` sin contrafactual (GEMV_P7_38=A, GEMV_P7_38_CONTRA=0) ya puestas; esta se engancha DESPUES y
sustituye (a) la importancia esperada por la de punto de partida de clase (p0 + suma) / (1 + N) y (b) la ignorancia que lee la curiosidad por ignorancia x importancia
esperada x cautela (nace_P7_23.cautela_de). Ademas abre MIRADAS: cosa de las cuatro a la vista, no llevada, cautela < 1 -> ventana de 240 tics; si la coge, se descarta;
al cerrar, apunte {objeto, dia, tick, foto, intensidad = escalar(|delta malestar filtrado|), peligro}; el punto de partida de esa cosa = max(p0 de clase, intensidad de sus
apuntes). Los apuntes viajan en `apuntes_P7_40_<asiento>.json` (carpeta de la cadena). E1: para cada apunte con la cosa sin recuerdos, el primer tic de calma (cautela = 1)
posterior, en esta vida o en la siguiente, con alguna cosa sin recuerdos a la vista: la clase sin recuerdos que mas llama."""
import json, os, statistics as st
import descubre_P7 as X, nace_P7_23 as N, nace_P7_29 as N29, nace_P7_33 as N33, recuerdo_P7_23 as RP, contrafactual_P7_38 as CF
from cuaderno_P7 import E_INTENSIDAD
ON = os.environ.get("GEMV_P7_40", "0") == "1"; MIRADA = 240
MIEDO = os.environ.get("GEMV_P7_40_MIEDO", "prudente")      # [P7-41] la personalidad: prudente = cautela tal cual; valiente = (1 + cautela) / 2 (propuesta, pendiente de Manel)
EN_CUADERNO = os.environ.get("GEMV_P7_40_EN_CUADERNO", "0") == "1"
CACHE_IGN = os.environ.get("GEMV_P7_43_CACHE", "0") == "1"      # [P7-43] cache por tic de la ignorancia y la curiosidad por clase   # [P7-41, campo] los apuntes viajan dentro del cuaderno (campo `apuntes_P7_40`), no en un archivo aparte
E = {"apuntes": [], "pendientes": [], "miradas": {}, "obs": None, "mundo": None, "ruta": None, "momentos": set(), "anotado": {}, "p0_dia": {}, "resueltos": [], "dia": None}


def escalar(imp): return CF.escalar(imp)
def conocida(c, o): return any(not r.get("corte") for r in c.recuerdos_de(o))
def imps(c, o): return [escalar(r.get("importancia")) for r in c.recuerdos_de(o) if not r.get("corte")]


def p0_clase(c, mundo, objeto):
    """Mediana de la importancia de las otras cosas conocidas de su clase; si ninguna, de todo lo conocido; si nada, 1."""
    clase = N33.gear(mundo) if objeto in N33.gear(mundo) else N.consumibles(mundo)
    v = [x for o in clase if o != objeto and conocida(c, o) for x in imps(c, o)]
    if not v: v = [x for o in N33.cuatro(mundo) if o != objeto and conocida(c, o) for x in imps(c, o)]
    return st.median(v) if v else 1.0


def p0(c, mundo, objeto):
    base = p0_clase(c, mundo, objeto); vistas = [a["intensidad"] for a in E["apuntes"] if a["objeto"] == objeto]
    return max([base] + vistas)


def importancia_esperada(c, mundo, objeto):
    k = (N.E.get("tick"), id(c), objeto, len(E["apuntes"]), sum(len(s_) for o_ in c.objetos.values() for s_ in o_["situaciones"].values()))
    h = E.setdefault("_cache", {})
    if h.get("k") != k[:2]: h.clear(); h["k"] = k[:2]
    if k in h: return h[k]
    v = imps(c, objeto); h[k] = (p0(c, mundo, objeto) + sum(v)) / (1.0 + len(v)); return h[k]


def miedo(cautela): return cautela if MIEDO == "prudente" else (1.0 + cautela) / 2.0


def curiosidad(c, mundo, objeto, cautela=1.0):
    ign = float(c._ignorancia0(objeto)) if hasattr(c, "_ignorancia0") else float(c.ignorancia(objeto)); return ign * importancia_esperada(c, mundo, objeto) * cautela


def aplica(clase, registra=None):
    if not ON: return {"P7_40": False}
    assert os.environ.get("GEMV_P7_38_CONTRA", "1") == "0" and os.environ.get("GEMV_P7_39") == "1", "P7-40 va sobre B1 (filtro de P7-39, sin contrafactual)"
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        c = _oa(criatura, ruta, registra_)
        E["ruta"] = os.path.join(os.path.dirname(os.path.abspath(ruta)), f"apuntes_P7_40_{criatura}.json") if (ruta and not EN_CUADERNO) else None
        if EN_CUADERNO and ruta and os.path.exists(ruta) and X.CUADERNO_ON and not X.BORRADO:
            try: d = (json.load(open(ruta)).get("apuntes_P7_40") or {})
            except Exception: d = {}
            E["apuntes"] = d.get("apuntes", []); E["pendientes"] = d.get("pendientes", []); E["resueltos"] = d.get("resueltos", [])
        elif E["ruta"] and os.path.exists(E["ruta"]) and X.CUADERNO_ON and not X.BORRADO:
            d = json.load(open(E["ruta"])); E["apuntes"] = d.get("apuntes", []); E["pendientes"] = d.get("pendientes", []); E["resueltos"] = d.get("resueltos", [])
        if c is not None and EN_CUADERNO:
            _v0 = c.volcado
            def volcado(_c=c, _v0=_v0):
                d = _v0(); d["apuntes_P7_40"] = {"apuntes": E["apuntes"], "pendientes": E["pendientes"], "resueltos": E["resueltos"][-200:]}; return d
            c.volcado = volcado
        if c is not None:
            hoy = c.dia_actual(); queda = []
            for p in E["pendientes"]:                                   # un apunte de hace mas de un dia ya no puede cumplirse: no cumplido
                if p["dia"] < hoy - 1: E["resueltos"].append({**p, "resuelto_dia": hoy, "tick_calma": None, "manda": None, "cumple": False, "nota": "sin tic de calma en su dia ni en el siguiente"})
                else: queda.append(p)
            E["pendientes"] = queda
            if not hasattr(c, "_ignorancia0"): c._ignorancia0 = c.ignorancia
            def ign_nueva(objeto, dia=None, _c=c):
                obs = E["obs"] or {}; mundo = E["mundo"]
                if mundo is None: return float(_c._ignorancia0(objeto, dia))
                if CACHE_IGN:                                    # [P7-43] por tic y objeto: la obs real y el cuaderno no cambian dentro de `decide`; la clave lleva el numero de recuerdos por si acaso
                    k = (N.E.get("tick"), objeto, dia, sum(len(s_) for o_ in _c.objetos.values() for s_ in o_["situaciones"].values()), len(E["apuntes"])); h = E.setdefault("ign_cache", {})
                    if h.get("_tick") != k[0]: h.clear(); h["_tick"] = k[0]
                    if k not in h: h[k] = curiosidad(_c, mundo, objeto, miedo(N.cautela_de(obs, mundo, N.E.get("tick") or 0)))
                    return h[k]
                return curiosidad(_c, mundo, objeto, miedo(N.cautela_de(obs, mundo, N.E.get("tick") or 0)))
            c.ignorancia = ign_nueva
        return c
    X.arranca = arranca
    _ot = X.termina
    def termina(registra_=None):
        if E["ruta"] and X.CUADERNO_ON: json.dump({"apuntes": E["apuntes"], "pendientes": E["pendientes"], "resueltos": E["resueltos"]}, open(E["ruta"], "w"), ensure_ascii=False)
        return _ot(registra_)
    X.termina = termina
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        E["obs"] = obs; E["mundo"] = self.mundo
        accion, radio = _d(self, obs)
        c = N.cuaderno()
        if radio is None or c is None or getattr(self, "phase", None) != "live" or self.mundo is None: return accion, radio
        mundo = self.mundo; you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); tick = self.tick; dia = c.dia_actual(); E["dia"] = dia
        caut = N.cautela_de(obs, mundo, tick); mal = X.malestar_ejes(radio); foto = RP.foto_de_radio(radio) or N.E.get("foto") or {}
        vis = {it.get("id") for it in ((obs.get("visible") or {}).get("items") or []) if it.get("pos")}
        # miradas: cosa a la vista, no llevada, en peligro
        for o in N33.cuatro(mundo):
            lleva = N33.tiene(you, mundo, o) >= 1 if o in N33.gear(mundo) else N.unidades_de(you, mundo, o) >= 1
            m = E["miradas"].get(o)
            if m is None:
                if o in vis and not lleva and caut < 1.0: E["miradas"][o] = {"t0": tick, "mal0": mal, "foto": foto, "peligro": N33.peligro_de(self, obs), "cautela": caut, "conocida": conocida(c, o)}
                continue
            if lleva: E["miradas"][o] = None; continue                      # la coge: la prueba es la que cuenta, la mirada se descarta
            if tick - m["t0"] >= MIRADA:
                imp = {d_: abs(mal.get(d_, 0.0) - m["mal0"].get(d_, 0.0)) for d_ in ("cuerpo", "recursos", "vinculo")}
                a = {"objeto": o, "dia": dia, "tick": m["t0"], "t_fin": tick, "foto": m["foto"], "intensidad": round(escalar(imp), 4), "importancia": {k: round(v, 4) for k, v in imp.items()}, "peligro": m["peligro"], "cautela": round(m["cautela"], 3), "sin_recuerdos": not m["conocida"], "p0_clase": round(p0_clase(c, mundo, o), 4)}
                E["apuntes"].append(a)
                if a["sin_recuerdos"]: E["pendientes"].append({"objeto": o, "dia": dia, "tick": m["t0"]})
                E["miradas"][o] = None
        # E1: el primer tic de calma con alguna cosa sin recuerdos a la vista
        if E["pendientes"] and caut >= 1.0:
            sin = [o for o in N33.cuatro(mundo) if not conocida(c, o)]; sin_vis = [o for o in sin if o in vis]
            if sin_vis:
                cur = {o: curiosidad(c, mundo, o, 1.0) for o in sin}; top = max(cur, key=cur.get); queda = []
                for p in E["pendientes"]:
                    if p["dia"] < dia - 1: continue                           # mas de un dia: no cumplido (se resuelve al cargar el dia siguiente)
                    if not conocida(c, p["objeto"]):
                        mx = max(cur.values()); empate = sum(1 for v in cur.values() if v >= mx - 1e-9) > 1
                        E["resueltos"].append({**p, "resuelto_dia": dia, "tick_calma": tick, "manda": top, "cumple": cur[p["objeto"]] >= mx - 1e-9, "empate": empate, "curiosidades": {k: round(v, 4) for k, v in cur.items()}})
                    else: E["resueltos"].append({**p, "resuelto_dia": dia, "tick_calma": tick, "manda": None, "cumple": None, "nota": "ya probada antes del tic de calma"})
                E["pendientes"] = queda
        # momentos
        if tick in E["momentos"]:
            ctx = N.contexto_ahora(mundo, pos, tick); C = radio.get("candidatos") or {}
            def dd(n_): c_ = C.get(n_); return (c_.get("d") if isinstance(c_, dict) else c_)
            E["anotado"][tick] = {"elegido": radio.get("elegido"), "d_coger": dd("coger"), "d_noop": dd("noop"), "peligro": N33.peligro_de(self, obs), "cautela": caut, "miedo": miedo(caut), "contexto": ctx,
                                  "clases": {o: {"ignorancia": float(c._ignorancia0(o)), "p0": round(p0(c, mundo, o), 4), "importancia_esperada": round(importancia_esperada(c, mundo, o), 4), "A": round(curiosidad(c, mundo, o, 1.0), 4), "con_cautela": round(curiosidad(c, mundo, o, caut), 4)} for o in N33.cuatro(mundo)}}
        return accion, radio
    clase.decidir = decidir
    return {"P7_40": True}


def p0_todos(c, mundo): return {o: {"p0": round(p0(c, mundo, o), 4), "p0_clase": round(p0_clase(c, mundo, o), 4), "apuntes": sum(1 for a in E["apuntes"] if a["objeto"] == o)} for o in N33.cuatro(mundo)}
