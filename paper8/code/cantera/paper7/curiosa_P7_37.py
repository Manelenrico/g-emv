"""[P7-37] LA CURIOSIDAD POR LO QUE PODRIA IMPORTAR (diseno propuesto a Manel, pendiente de su si). SOLO BANCO: no se juega con ella. Se engancha despues de las piezas del
siete (descubre, pedir, nacer, P7-29, P7-33) y solo toca (a) lo que se escribe en el cuaderno al cerrar una ventana y (b) la ignorancia que lee la curiosidad de clase.
  1. IMPORTANCIA DESCONTADA. La importancia de un recuerdo (cuaderno_P7: cambio del malestar por eje entre abrir y cerrar la ventana, mal1 - mal0) se vuelve a medir
     restando el cambio de malestar que viene de causas conocidas, igual que el efecto (descubre_P7._dano_conocido: el anillo estando fuera, los golpes de rivales a la
     vista): al cerrar, se vuelve a tasar la obs de ese tic con la vida que tendria si no hubiera recibido ese dano conocido (hp + conocido, con techo en hp_max;
     A.appraise sobre una copia de la obs y de la memoria) y la importancia descontada es mal1' - mal0 = importancia + (mal1' - mal1). El anillo solo entra como dano
     (las filas de "fuera del circulo" no se descuentan: declarado). Se guarda en el recuerdo (`importancia_original`, `importancia` = la descontada) y la intensidad se
     recalcula como en el campo, 1 + min(1, S/E), ahora con S de la descontada.
  2. CURIOSIDAD = IGNORANCIA x IMPORTANCIA ESPERADA. Importancia esperada de una clase: media ponderada de la importancia (escalar: min(1, S/E), la misma que entra en
     la intensidad) de sus recuerdos sin cortes, con un recuerdo neutro de importancia 1 y peso PESO_NEUTRO que no se apaga (como el neutro de la creencia): los vividos
     se apagan con OLVIDO y, al apagarse, el neutro vuelve a mandar. La ignorancia es la de siempre (neutro / (neutro + pesos)). Se sustituye `cuaderno.ignorancia(o)` en
     la instancia, que es lo que leen la curiosidad de clase (nace_P7_29.curiosidad_M -> R-CURIOSIDAD) y la llamada de clase (nace_P7_33._cands -> ir_curioso); las ganas
     (k) leen `vivida` (creencia por parecido) y no cambian.
  3. VARIANTE C (Manel, 10-oct): la ignorancia es la de ESA cosa en una situacion como la de ahora, por parecido (recuerdo_P7_23.parecido: foto emocional y contexto), no
     la de la clase entera: ignorancia_parecido(o, contexto_ahora, foto_ahora). Combinada con la importancia esperada del punto 2.
  5. VARIANTE C5 (la mirada de cientifico): el parecido incluye COMO se probo: la forma (la ultima accion del recuerdo que toca la cosa: coger = cogerla y llevarla /
     ponerse / empunar / usar) frente a la forma que se considera, y las acciones anteriores (las ultimas 4 de ahora mas esa forma): parecido_acciones = 0,5 x [misma
     forma] + 0,5 x Jaccard(acciones del recuerdo, acciones de ahora + la forma); el parecido total es el de C por ese factor. Las formas de cada cosa: red = coger o
     empunar; camuflaje = coger o ponerse; botiquin y racion = coger o usar. La curiosidad C5 de una cosa en un momento es la MAYOR entre sus formas (la forma nueva
     llama mas). Numeros declarados aqui, no medidos.
Mandos: GEMV_P7_37 = campo | descontada | C | C5. `E["momentos"]`: tics en los que se anota, por clase, la curiosidad bajo las cuatro lecturas, el contexto, la cautela
(nace_P7_23.cautela_de, P7-26) y, para la red y el camuflaje, la forma y la situacion que mas llamarian (C5)."""
import copy, math, os
import descubre_P7 as X, nace_P7_23 as N, nace_P7_29 as N29, nace_P7_33 as N33, recuerdo_P7_23 as RP
from cuaderno_P7 import DOMINIOS, OLVIDO, PESO_NEUTRO, E_INTENSIDAD
from alma import appraisal_zs_v42_exp as A
VARIANTE = os.environ.get("GEMV_P7_37", "campo")
E = {"momentos": set(), "anotado": {}, "descontadas": 0, "obs": None, "radio": None, "variante": VARIANTE}
FORMAS = ("coger", "ponerse", "empunar", "usar")
SITUACIONES = tuple({"dentro": d, "golpeado_48": g} for d in (True, False) for g in (False, True))


# ── 1. la importancia descontada ──
def escalar(imp): return min(1.0, sum(abs(float((imp or {}).get(d) or 0.0)) for d in DOMINIOS) / E_INTENSIDAD)
def descuenta(h, obs, mundo, mem, tick, radio):
    """Para una huella recien cerrada: la importancia descontada y la intensidad nueva; None si no hay dano conocido en la ventana."""
    hp0 = float(h.get("hp0") or 0.0); hp_fin = float(h.get("hp_fin") or 0.0); conocido = float((h.get("efecto") or {}).get("cuerpo") or 0.0) - (hp_fin - hp0)
    if conocido <= 1e-9: return None
    you = obs.get("you") or {}; hp_max = float(getattr(mem, "hp_max", None) or 100.0)
    o2 = copy.deepcopy(obs); o2["you"]["hp"] = min(hp_max, float(you.get("hp") or 0.0) + conocido)
    _, rap = A.appraise(o2, mundo, copy.deepcopy(mem), tick)
    mal1 = X.malestar_ejes(radio); mal1b = X.malestar_ejes({"ahora": rap})
    return {d: float((h.get("importancia") or {}).get(d) or 0.0) + (mal1b.get(d, 0.0) - mal1.get(d, 0.0)) for d in DOMINIOS}


def aplica_descuento(c, huellas_nuevas, obs, mundo, mem, tick, radio):
    for h in huellas_nuevas:
        if h.get("corte"): continue                                   # los cortes no entran ni en la creencia ni en la importancia esperada: se dejan como estan
        obj = h.get("objeto") or X.kit(mundo); rec = [r for r in c.recuerdos_de(obj) if r.get("tick") == h.get("t0")]
        if not rec: continue
        r = rec[-1]; imp2 = descuenta(h, obs, mundo, mem, tick, radio)
        r["importancia_original"] = dict(r["importancia"])
        if imp2 is not None:
            r["importancia"] = {d: round(imp2[d], 4) for d in DOMINIOS}; E["descontadas"] += 1
        r["intensidad"] = round(1.0 + escalar(r["importancia"]), 4); r["descontada"] = imp2 is not None


# ── 2. la importancia esperada y la curiosidad ──
def importancia_esperada(c, objeto, dia=None):
    d_act = c.dia_actual() if dia is None else dia; num = PESO_NEUTRO * 1.0; den = PESO_NEUTRO
    for r in c.recuerdos_de(objeto):
        if r.get("corte"): continue
        w = float(r["intensidad"]) * (OLVIDO ** max(0, d_act - int(r["dia"]))); num += w * escalar(r.get("importancia")); den += w
    return num / den


def formas_de(mundo):
    return {N33.red(mundo): ("coger", "empunar"), N33.camo(mundo): ("coger", "ponerse"), X.kit(mundo): ("coger", "usar"), N.racion(mundo): ("coger", "usar")}


def forma_de(acciones):
    for a in reversed(list(acciones or [])):
        a = str(a)
        for f in ("ponerse", "empunar", "usar", "coger"):
            if a.startswith(f): return f
    return "coger"


def parecido_acciones(acciones_rec, acciones_ahora, forma):
    fa = forma_de(acciones_rec); A_ = set(map(str, acciones_rec or ())); B_ = set(map(str, acciones_ahora or ())) | {forma}
    j = (len(A_ & B_) / len(A_ | B_)) if (A_ | B_) else 1.0
    return 0.5 * (1.0 if fa == forma else 0.0) + 0.5 * j


def suma_parecida(c, objeto, contexto, foto, acciones=None, forma=None, dia=None):
    d_act = c.dia_actual() if dia is None else dia; s = 0.0
    for r in c.recuerdos_de(objeto):
        if r.get("corte"): continue
        w = float(r["intensidad"]) * (OLVIDO ** max(0, d_act - int(r["dia"]))) * RP.parecido(contexto, foto, r)
        if forma is not None: w *= parecido_acciones(r.get("acciones"), acciones, forma)
        s += w
    return s


def ign_C5(c, objeto, contexto, foto, acciones, formas, dia=None):
    """La ignorancia por parecido con acciones, la MAYOR entre las formas de la cosa (y la forma que la da)."""
    v = {f: PESO_NEUTRO / (PESO_NEUTRO + suma_parecida(c, objeto, contexto, foto, acciones, f, dia)) for f in formas}
    f = max(v, key=v.get); return v[f], f


def curiosidades(c, mundo, objeto, contexto, foto, acciones, dia=None):
    """Las cuatro lecturas: campo (ignorancia de clase), descontada (ign x imp. esperada), C (ign por parecido x imp. esperada), C5 (ign por parecido con acciones, la mayor entre formas, x imp. esperada)."""
    ign = float(c.ignorancia(objeto, dia)) if not hasattr(c, "_ignorancia0") else float(c._ignorancia0(objeto, dia)); ie = importancia_esperada(c, objeto, dia)
    ic = PESO_NEUTRO / (PESO_NEUTRO + suma_parecida(c, objeto, contexto, foto, None, None, dia)); ic5, f5 = ign_C5(c, objeto, contexto, foto, acciones, formas_de(mundo).get(objeto, ("coger",)), dia)
    return {"ignorancia": ign, "importancia_esperada": ie, "campo": ign, "descontada": ign * ie, "C": ic * ie, "C5": ic5 * ie, "ign_parecido": ic, "ign_parecido_acciones": ic5, "forma_C5": f5}


def preferida(c, mundo, objeto, foto, acciones, dia=None):
    """(forma, situacion) con mas curiosidad C5 para la siguiente prueba: la ignorancia por parecido con acciones, probando cada forma de la cosa y cada situacion con la foto de ahora."""
    ie = importancia_esperada(c, objeto, dia); out = {}
    for f in formas_de(mundo).get(objeto, ("coger",)):
        for s in SITUACIONES:
            out[f"{f} · {'dentro' if s['dentro'] else 'fuera'} · {'golpeado' if s['golpeado_48'] else 'sin golpe'}"] = round(PESO_NEUTRO / (PESO_NEUTRO + suma_parecida(c, objeto, s, foto, acciones, f, dia)) * ie, 4)
    mejor = max(out, key=out.get); return {"mejor": mejor, "curiosidad": out[mejor], "todas": out}


# ── el enganche ──
def aplica(clase, registra=None):
    if VARIANTE == "campo" and not E["momentos"]: return {"P7_37": "campo"}
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        c = _oa(criatura, ruta, registra_)
        if c is not None and VARIANTE != "campo":
            c._ignorancia0 = c.ignorancia
            def ign_nueva(objeto, dia=None, _c=c):
                ie = importancia_esperada(_c, objeto, dia)
                if VARIANTE == "descontada": return float(_c._ignorancia0(objeto, dia)) * ie
                obs = E["obs"] or {}; you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); mundo = E.get("mundo")
                ctx = N.contexto_ahora(mundo, pos, N.E.get("tick") or 0) if mundo is not None else {"dentro": True, "golpeado_48": False}
                if VARIANTE == "C5" and mundo is not None: return ign_C5(_c, objeto, ctx, N.E.get("foto"), list(N.E["acciones"]), formas_de(mundo).get(objeto, ("coger",)), dia)[0] * ie
                return PESO_NEUTRO / (PESO_NEUTRO + suma_parecida(_c, objeto, ctx, N.E.get("foto"), None, None, dia)) * ie
            c.ignorancia = ign_nueva
        return c
    X.arranca = arranca
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        E["obs"] = obs; E["mundo"] = self.mundo
        n0 = len(X.ESTADO.get("huellas") or [])
        accion, radio = _d(self, obs)
        c = N.cuaderno()
        if radio is not None and c is not None and getattr(self, "phase", None) == "live":
            nuevas = (X.ESTADO.get("huellas") or [])[n0:]
            if nuevas and VARIANTE != "campo": aplica_descuento(c, nuevas, obs, self.mundo, self.mem, self.tick, radio)
            if self.tick in E["momentos"]:
                you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); ctx = N.contexto_ahora(self.mundo, pos, self.tick); foto = RP.foto_de_radio(radio) or N.E.get("foto"); acc = list(N.E["acciones"])
                C = radio.get("candidatos") or {}
                def dd(n_): c_ = C.get(n_); return (c_.get("d") if isinstance(c_, dict) else c_)
                E["anotado"][self.tick] = {"elegido": radio.get("elegido"), "d_coger": dd("coger"), "d_noop": dd("noop"), "peligro": N33.peligro_de(self, obs), "cautela": N.cautela_de(obs, self.mundo, self.tick), "contexto": ctx, "forma_en_curso": forma_de(acc), "acciones": acc[-4:],
                                           "clases": {o: curiosidades(c, self.mundo, o, ctx, foto, acc) for o in N33.cuatro(self.mundo)},
                                           "preferida": {o: preferida(c, self.mundo, o, foto, acc) for o in N33.gear(self.mundo)}}
        return accion, radio
    clase.decidir = decidir
    return {"P7_37": VARIANTE}
