"""[P7-38] IMPORTANCIA CONTRA LO QUE HABRIA PASADO SIN LA PRUEBA (metodo decidido por Manel; SELLO_P7_38.md). SOLO BANCO (GEMV_P7_38 = A | off). Se engancha despues de
las piezas del siete y toca (a) la importancia que se escribe en cada recuerdo al cerrar una ventana y (b) la ignorancia que leen la curiosidad y la llamada de clase.
  PISTAS DEL PASADO: por tic vivo, [tick, dentro, golpeado_48, dolor_R, malF, malR, malS, en_prueba]; las de los dias anteriores viajan en la carpeta de la cadena
  (`pistas_P7_38_<asiento>.json`, una lista por dia) y las del dia en curso se van anotando. Ventanas de referencia: tramos [u, u+L] con u multiplo de 12, dentro de una
  vida, sin prueba abierta en ningun tic del tramo; situacion = (dentro, golpeado_48, banda de hambre = tercil del dolor_R en el pasado: bajo/medio/alto, una sola banda
  con menos de 30 tics de pasado). Importancia por dominio = |delta_prueba - media(delta_ref)|, 0 si < 1 desviacion tipica de los delta_ref; < 5 referencias en la situacion
  -> cualquier situacion (marcado `referencia_cualquiera`); < 5 en total -> se deja la de P7-33 (marcado `sin_referencia`). Intensidad = 1 + min(1, S/E) con la contrafactual.
  IMPORTANCIA ESPERADA de una clase = (1 + suma de importancias escalares de sus recuerdos sin cortes) / (1 + N). CURIOSIDAD = ignorancia x importancia esperada."""
import json, math, os, statistics as st
import descubre_P7 as X, nace_P7_23 as N, nace_P7_29 as N29, nace_P7_33 as N33, recuerdo_P7_23 as RP
from cuaderno_P7 import DOMINIOS, E_INTENSIDAD
VARIANTE = os.environ.get("GEMV_P7_38", "off"); PASO = 12; MIN_REF = 5; MIN_PASADO = 30
CONTRA = os.environ.get("GEMV_P7_38_CONTRA", "1") == "1"
PISTAS = os.environ.get("GEMV_P7_38_PISTAS", "1") == "1"      # [P7-41] en el campo (B1, sin contrafactual) no hacen falta las pistas por tic      # [P7-39] B1: la misma pieza sin el contrafactual (la importancia se queda en |delta| del malestar filtrado)
E = {"pistas_pasado": [], "pistas_hoy": [], "momentos": set(), "anotado": {}, "obs": None, "mundo": None, "ruta_pistas": None, "n_contrafactual": 0, "n_cualquiera": 0, "n_sin_ref": 0}
DOM_I = {"cuerpo": 4, "recursos": 5, "vinculo": 6}


def escalar(imp): return min(1.0, sum(abs(float((imp or {}).get(d) or 0.0)) for d in DOMINIOS) / E_INTENSIDAD)


# ── las pistas ──
def banda_de(dolor_R):
    """La banda de hambre: tercil del dolor_R en el pasado (umbrales recalculados cada 240 tics sobre todo el pasado, E["dolor_R"])."""
    u = E.get("umbrales")
    if not u: return 0
    return 0 if dolor_R <= u[0] else (1 if dolor_R <= u[1] else 2)


def recalcula_umbrales():
    vals = sorted(E["dolor_R"]); E["umbrales"] = (vals[len(vals) // 3], vals[2 * len(vals) // 3]) if len(vals) >= MIN_PASADO else None


def _acum(dia):
    k = id(dia); a = E.setdefault("_acum", {}).get(k)
    if a is None or len(a) != len(dia) + 1:
        a = [0]
        for p in dia: a.append(a[-1] + int(bool(p[7])))
        E["_acum"][k] = a
    return a


def referencias(pasado_dias, L, situacion):
    """Los delta de malestar por dominio de las ventanas de referencia de duracion L; (lista de deltas, en_situacion: bool)."""
    todas = []; sit = []
    for dia in pasado_dias:
        if not dia: continue
        idx = {p[0]: i for i, p in enumerate(dia)}; ac = _acum(dia)
        for i, p in enumerate(dia):
            u = p[0]
            if u % PASO: continue
            j = idx.get(u + L)
            if j is None or ac[j + 1] - ac[i] > 0: continue
            d = tuple(dia[j][k] - p[k] for k in (4, 5, 6)); todas.append(d)
            if (p[1], p[2], p[8]) == situacion: sit.append(d)
    return (sit, True) if len(sit) >= MIN_REF else (todas, False)


def contrafactual(r, h, pasado_dias):
    L = int(h.get("t_fin", 0)) - int(h.get("t0", 0)); ctx = h.get("contexto") or {}; t0 = int(h.get("t0", 0))
    banda = next((p[8] for p in pasado_dias[-1] if p[0] == t0), 0) if pasado_dias else 0
    refs, en_sit = referencias(pasado_dias, L, (bool(ctx.get("dentro")), bool(ctx.get("golpeado_48")), banda))
    r["importancia_P33"] = dict(r["importancia"])
    if len(refs) < MIN_REF: r["sin_referencia"] = True; E["n_sin_ref"] += 1; return
    imp = {}
    for d, k in (("cuerpo", 0), ("recursos", 1), ("vinculo", 2)):
        xs = [x[k] for x in refs]; mu = st.mean(xs); sd = st.pstdev(xs) if len(xs) > 1 else 0.0
        v = abs(float(r["importancia_P33"].get(d) or 0.0) - mu); imp[d] = 0.0 if v < sd else round(v, 4)
    r["importancia"] = imp; r["intensidad"] = round(1.0 + escalar(imp), 4); r["referencia_cualquiera"] = not en_sit; r["referencias"] = len(refs); r["duracion_ref"] = L
    E["n_contrafactual"] += 1; E["n_cualquiera"] += int(not en_sit)


# ── la importancia esperada y la curiosidad ──
def importancia_esperada(c, objeto):
    rec = [r for r in c.recuerdos_de(objeto) if not r.get("corte")]
    return (1.0 + sum(escalar(r.get("importancia")) for r in rec)) / (1.0 + len(rec))


def curiosidad_A(c, objeto): return float(c._ignorancia0(objeto) if hasattr(c, "_ignorancia0") else c.ignorancia(objeto)) * importancia_esperada(c, objeto)


# ── la mirada de cientifico (C5 de P7-37), para A+M: entre situaciones sin peligro ──
def preferida(c, mundo, objeto, foto, acciones, solo_sin_peligro):
    import curiosa_P7_37 as C37
    ie = importancia_esperada(c, objeto); out = {}
    for f in C37.formas_de(mundo).get(objeto, ("coger",)):
        for s in C37.SITUACIONES:
            if solo_sin_peligro and not (s["dentro"] and not s["golpeado_48"]): continue
            out[f"{f} · {'dentro' if s['dentro'] else 'fuera'} · {'golpeado' if s['golpeado_48'] else 'sin golpe'}"] = round(1.0 / (1.0 + C37.suma_parecida(c, objeto, s, foto, acciones, f)) * ie, 4)
    mejor = max(out, key=out.get); return {"mejor": mejor, "curiosidad": out[mejor]}


# ── el enganche ──
def aplica(clase, registra=None):
    if VARIANTE == "off" and not E["momentos"]: return {"P7_38": "off"}
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        c = _oa(criatura, ruta, registra_)
        E["ruta_pistas"] = os.path.join(os.path.dirname(os.path.abspath(ruta)), f"pistas_P7_38_{criatura}.json") if ruta else None
        if E["ruta_pistas"] and os.path.exists(E["ruta_pistas"]) and X.CUADERNO_ON and not X.BORRADO: E["pistas_pasado"] = json.load(open(E["ruta_pistas"]))
        E["dolor_R"] = [p[3] for dia in E["pistas_pasado"] for p in dia]; recalcula_umbrales()
        if c is not None and VARIANTE == "A":
            c._ignorancia0 = c.ignorancia; c.ignorancia = (lambda objeto, dia=None, _c=c: float(_c._ignorancia0(objeto, dia)) * importancia_esperada(_c, objeto))
        return c
    X.arranca = arranca
    _ot = X.termina
    def termina(registra_=None):
        if PISTAS and E["ruta_pistas"] and E["pistas_hoy"] and X.CUADERNO_ON:
            json.dump(E["pistas_pasado"] + [E["pistas_hoy"]], open(E["ruta_pistas"], "w"))
        return _ot(registra_)
    X.termina = termina
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        E["obs"] = obs; E["mundo"] = self.mundo; n0 = len(X.ESTADO.get("huellas") or [])
        accion, radio = _d(self, obs)
        c = N.cuaderno()
        if radio is not None and getattr(self, "phase", None) == "live" and self.mundo is not None:
            you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); ctx = N.contexto_ahora(self.mundo, pos, self.tick); foto = RP.foto_de_radio(radio) or N.E.get("foto") or {}
            mal = X.malestar_ejes(radio); en_prueba = bool(N.E.get("ventana")) or any(v for v in (N33.E.get("ventanas") or {}).values())
            dR = float(foto.get("dolor_R") or 0.0)
            if PISTAS: E.setdefault("dolor_R", []).append(dR)
            if PISTAS and (len(E["dolor_R"]) % 240 == 0 or (E.get("umbrales") is None and len(E["dolor_R"]) >= MIN_PASADO)): recalcula_umbrales()
            if PISTAS: E["pistas_hoy"].append([self.tick, bool(ctx["dentro"]), bool(ctx["golpeado_48"]), dR, mal.get("cuerpo", 0.0), mal.get("recursos", 0.0), mal.get("vinculo", 0.0), en_prueba, banda_de(dR)])
            nuevas = (X.ESTADO.get("huellas") or [])[n0:]
            if os.environ.get("P7_38_DEBUG") and nuevas: __import__("sys").stderr.write(f"DEBUG nuevas {self.tick} {[(h.get('objeto'), h.get('t0'), h.get('corte')) for h in nuevas]} c {c is not None} rec {[r.get('tick') for h in nuevas for r in c.recuerdos_de(h.get('objeto') or X.kit(self.mundo))] if c is not None else None}\n")
            if nuevas and c is not None and VARIANTE == "A":
                for h in nuevas:
                    if h.get("corte"): continue
                    obj = h.get("objeto") or X.kit(self.mundo); rec = [r for r in c.recuerdos_de(obj) if r.get("tick") == h.get("t0")]
                    if rec and CONTRA: contrafactual(rec[-1], h, E["pistas_pasado"] + [E["pistas_hoy"]])
                    elif rec: rec[-1]["importancia_P33"] = dict(rec[-1]["importancia"]); rec[-1]["intensidad"] = round(1.0 + escalar(rec[-1]["importancia"]), 4); E["n_contrafactual"] += 1
            if self.tick in E["momentos"] and c is not None:
                acc = list(N.E["acciones"]); C = radio.get("candidatos") or {}
                def dd(n_): c_ = C.get(n_); return (c_.get("d") if isinstance(c_, dict) else c_)
                E["anotado"][self.tick] = {"elegido": radio.get("elegido"), "d_coger": dd("coger"), "d_noop": dd("noop"), "peligro": N33.peligro_de(self, obs), "cautela": N.cautela_de(obs, self.mundo, self.tick), "contexto": ctx,
                                           "clases": {o: {"ignorancia": float(c._ignorancia0(o) if hasattr(c, "_ignorancia0") else c.ignorancia(o)), "importancia_esperada": importancia_esperada(c, o), "A": curiosidad_A(c, o)} for o in N33.cuatro(self.mundo)},
                                           "preferida": {o: {"todas": preferida(c, self.mundo, o, foto, acc, False), "sin_peligro": preferida(c, self.mundo, o, foto, acc, True)} for o in N33.gear(self.mundo)}}
        return accion, radio
    clase.decidir = decidir
    return {"P7_38": VARIANTE}
