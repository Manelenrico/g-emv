"""[P5-3B] LA FORMA Y LA REGLA. Fuera del decisor; no cambia ninguna decision.

UNA FORMA es una lista de TRAMOS. Cada tramo es {destino, intencion, esperar}.
Los PUNTOS DE CONTROL no van a un H fijo: van al tic de LLEGADA de cada tramo,
calculado con el enfriamiento de andar (11 tics por paso, manual §4) mas las
esperas.

En cada punto de control se arma una FOTO PROYECTADA del mundo:
  · NOSOTROS: `proyeccion.proyectar` da pos, vida, mano, cuerpo, mochila y
    efectos (reglas validadas en P5-3A: residuo cero sin dano ajeno);
  · EL ANILLO: en su estado REAL de ese tic (`mundo.anillo_en`), que es
    determinista y es lo unico del futuro que el cuerpo ya anticipaba;
  · EL SUELO: los objetos tal como estaban en `t`, menos los cogidos;
  · LOS RIVALES: CONGELADOS donde estaban en `t`. **DECLARADO: la forma es
    ciega a los otros.** No se proyecta ni su movimiento ni su dano.

Sobre esa foto se llama a la TABLA (`appraisal_zs_v42_exp.appraise`) y al motor
(`opponent_distance`) y se obtiene la `d` del punto. Eso es la CURVA.

LA REGLA (B3). Una forma se acepta si:
  (1) ningun punto de control tiene vida proyectada por debajo de VIDA_MIN;
  (2) el area ponderada de (d_solo - d_forma) sobre los puntos de control es
      mayor que cero, con peso = 0,5 ** (tic_del_punto / 50).
"""
from __future__ import annotations
import copy, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (RAIZ, os.path.join(RAIZ, "paintball"), AQUI):
    if p not in sys.path:
        sys.path.insert(0, p)
from motor.model import DEFAULT_CONFIG, opponent_distance   # noqa: E402
from alma import appraisal_zs_v42_exp as A                  # noqa: E402
import proyeccion as P                                      # noqa: E402

VIDA_MIN = 15.0
MEDIA_VIDA = 50.0          # el peso cae a la mitad cada 50 tics
PASO = P.PASO_TICS


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def tics_de(tramo, pos):
    """Lo que cuesta un tramo: los pasos por su enfriamiento, mas la espera."""
    d = tramo.get("destino")
    n = cheb(tuple(pos), tuple(d)) if d else 0
    return n * PASO + int(tramo.get("esperar") or 0)


def puntos_de_control(estado0, tramos):
    """[(tic, tramo, pos_al_llegar)] — uno por tramo."""
    out, pos, t = [], tuple(estado0["pos"]), estado0["tick"]
    for tr in tramos:
        t += tics_de(tr, pos)
        if tr.get("destino"):
            pos = tuple(tr["destino"])
        out.append((t, tr, pos))
    return out


def foto_proyectada(obs_t, e, mundo, tick, suelo_restante):
    """La observacion que la tabla vera en el punto de control."""
    o = copy.deepcopy(obs_t)
    o["tick"] = tick
    you = o.setdefault("you", {})
    you["pos"] = list(e["pos"])
    you["hp"] = e["hp"]
    you["hand"] = copy.deepcopy(e.get("hand"))
    you["body"] = e.get("body")
    you["pack"] = [copy.deepcopy(s) for s in (e.get("pack") or [])]
    you["effects"] = list(e.get("effects") or [])
    you["move_ready_in"] = e.get("move_ready_in", 0)
    you["attack_ready_in"] = e.get("attack_ready_in", 0)
    vis = dict(o.get("visible") or {})
    vis["items"] = [dict(it) for it in suelo_restante]
    # los rivales, CONGELADOS donde estaban en t (declarado)
    o["visible"] = vis
    c, radio, dps = mundo.anillo_en(tick)
    o["zone"] = {"center": list(c), "radius": radio, "damage_per_s": dps,
                 "next_radius": (o.get("zone") or {}).get("next_radius"),
                 "warn_tick": (o.get("zone") or {}).get("warn_tick"),
                 "shrink_tick": (o.get("zone") or {}).get("shrink_tick")}
    o["events"] = []
    return o


def curva(estado0, obs_t, tramos, mundo, mem, suelo):
    """[(tic, d, vida, W, pos)] de una forma. Usa la memoria de `t`."""
    pcs = puntos_de_control(estado0, tramos)
    out, e, suelo_act = [], copy.deepcopy(estado0), dict(suelo)
    for tic, tr, pos in pcs:
        K = tic - e["tick"]
        if K < 0:
            continue
        plan = {"destino": tr.get("destino"),
                "coger": tr.get("intencion") == "coger",
                "usar": (tr.get("item") if tr.get("intencion") == "usar"
                         else None)}
        e = P.proyectar(e, plan, K, mundo, suelo_act)
        if tr.get("intencion") == "coger":
            suelo_act.pop(tuple(tr.get("destino") or ()), None)
        o = foto_proyectada(obs_t, e, mundo, tic,
                            list(suelo_act.values()))
        try:
            st, _rad = A.appraise(o, mundo, mem, tic)
            d = opponent_distance(st, DEFAULT_CONFIG)
        except Exception:
            d = None
        out.append({"tic": tic, "d": d, "vida": e["hp"], "W": e.get("W"),
                    "pos": tuple(e["pos"])})
    return out


def seguir_solo(estado0, obs_t, destino_cuerpo, horizonte, mundo, mem, suelo,
                tics_control):
    """La curva de comparacion: el paso de siempre y luego esperar.

    Se evalua en LOS MISMOS tics de control que la forma, para que la resta
    punto a punto tenga sentido y los sesgos de la proyeccion se cancelen.
    """
    out, e = [], copy.deepcopy(estado0)
    suelo_act = dict(suelo)
    primero = True
    for tic in tics_control:
        K = tic - e["tick"]
        if K < 0:
            continue
        plan = ({"destino": destino_cuerpo, "coger": False, "usar": None}
                if primero and destino_cuerpo else
                {"destino": None, "coger": False, "usar": None})
        e = P.proyectar(e, plan, K, mundo, suelo_act)
        primero = False
        o = foto_proyectada(obs_t, e, mundo, tic, list(suelo_act.values()))
        try:
            st, _rad = A.appraise(o, mundo, mem, tic)
            d = opponent_distance(st, DEFAULT_CONFIG)
        except Exception:
            d = None
        out.append({"tic": tic, "d": d, "vida": e["hp"], "W": e.get("W"),
                    "pos": tuple(e["pos"])})
    return out


def area(c_forma, c_solo, t0):
    """Area ponderada de (d_solo - d_forma). Peso = 0,5 ** (dt / 50)."""
    s = 0.0
    det = []
    for a, b in zip(c_forma, c_solo):
        if a["d"] is None or b["d"] is None:
            continue
        w = 0.5 ** ((a["tic"] - t0) / MEDIA_VIDA)
        g = (b["d"] - a["d"]) * w
        s += g
        det.append({"tic": a["tic"], "peso": round(w, 5),
                    "d_forma": round(a["d"], 5), "d_solo": round(b["d"], 5),
                    "gana": round(g, 5)})
    return s, det


def juzga_forma(c_forma, c_solo, t0, vida_min=VIDA_MIN):
    """(veredicto, area, detalle). veredicto in {ok, vida, area}."""
    flojo = [p for p in c_forma if p["vida"] is not None
             and p["vida"] < vida_min]
    ar, det = area(c_forma, c_solo, t0)
    if flojo:
        return "vida", ar, {"puntos": det, "punto_flojo": flojo[0]}
    if ar <= 0.0:
        return "area", ar, {"puntos": det}
    return "ok", ar, {"puntos": det}


# ── [P5-3C] EL COMPARADOR JUSTO ────────────────────────────────────────────
def forma_de_candidato(nombre, receta, horizonte_tics, pos):
    """Un candidato propio del cuerpo, como forma de un tramo.

    Llegar (o coger / usar, si procede) y esperar hasta el mismo horizonte que
    la forma con la que se compara.
    """
    d = receta.get("destino") if isinstance(receta, dict) else None
    tipo = (receta or {}).get("tipo")
    if nombre.startswith("coger"):
        inten = "coger"
    elif nombre.startswith(("usar_", "empunar_", "ponerse_")):
        inten = "usar"
    elif d:
        inten = "ir"
    else:
        inten = "esperar"
    pasos = cheb(tuple(pos), tuple(d)) if d else 0
    espera = max(0, horizonte_tics - pasos * PASO)
    item = None
    if inten == "usar":
        it = (receta or {}).get("item")
        item = it.get("id") if isinstance(it, dict) else it
        if item is None:
            item = {"usar_botiquin": "first_aid",
                    "usar_racion": "rations"}.get(nombre)
    return [{"destino": tuple(d) if d else None, "intencion": inten,
             "esperar": espera, "item": item, "_de": nombre, "_tipo": tipo}]


def coste(c, t0):
    """Area ponderada de la `d` de una curva. Mas bajo, mejor."""
    s = 0.0
    for p in c:
        if p["d"] is None:
            continue
        s += p["d"] * (0.5 ** ((p["tic"] - t0) / MEDIA_VIDA))
    return s


def mejor_propia(estado0, obs_t, base, tics_control, mundo, mem, suelo, t0,
                 vida_min=VIDA_MIN):
    """La MEJOR curva del puñado propio, evaluada en los mismos tics.

    Se proyecta CADA candidato del cuerpo como forma de un tramo y se queda la
    de menor `coste` entre las que pasan la vida minima. Si ninguna la pasa, se
    queda la de menor coste igualmente, y se marca.
    """
    if not tics_control:
        return None, None, None
    hor = tics_control[-1] - t0
    mejores, todas = [], []
    for n, rec in base:
        tr = forma_de_candidato(n, rec, hor, estado0["pos"])
        c = curva_en(estado0, obs_t, tr, mundo, mem, suelo, tics_control)
        k = coste(c, t0)
        flojo = any(p["vida"] is not None and p["vida"] < vida_min for p in c)
        todas.append((k, n, c, flojo))
        if not flojo:
            mejores.append((k, n, c))
    if mejores:
        k, n, c = min(mejores, key=lambda x: x[0])
        return c, n, False
    k, n, c, _f = min(todas, key=lambda x: x[0])
    return c, n, True


def curva_en(estado0, obs_t, tramos, mundo, mem, suelo, tics):
    """La curva de una forma evaluada EXACTAMENTE en `tics`."""
    import copy as _c
    out, e, suelo_act = [], _c.deepcopy(estado0), dict(suelo)
    tr = tramos[0]
    plan = {"destino": tr.get("destino"),
            "coger": tr.get("intencion") == "coger",
            "usar": tr.get("item") if tr.get("intencion") == "usar" else None}
    for tic in tics:
        K = tic - e["tick"]
        if K < 0:
            continue
        e = P.proyectar(e, plan, K, mundo, suelo_act)
        plan = {"destino": None, "coger": False, "usar": None}
        o = foto_proyectada(obs_t, e, mundo, tic, list(suelo_act.values()))
        try:
            st, _r = A.appraise(o, mundo, mem, tic)
            d = opponent_distance(st, DEFAULT_CONFIG)
        except Exception:
            d = None
        out.append({"tic": tic, "d": d, "vida": e["hp"], "W": e.get("W"),
                    "pos": tuple(e["pos"])})
    return out


# ── [P5-3D] EXPOSICION CONSERVADORA ────────────────────────────────────────
EXPO = "S-8-EXPOSICION"


def d_de_crudas(F_, expo_piso=None):
    """Rehace el State desde las filas CRUDAS de `A.filas()`, sin redondeo.

    Es literalmente `appraisal_zs_v42_exp.py:1684-1698`, mas el piso de
    exposicion de D2. Comprobado: con `expo_piso=None` da la misma `d` que
    `opponent_distance(appraise(...)[0])` hasta el ultimo bit.
    """
    from motor.model import State as _S
    pF = nF = pR = nR = pS = nS = 0.0
    for nom, (fF, fR, fS) in A.REPARTO.items():
        M = float(F_.get(nom) or 0.0)
        if nom == EXPO and expo_piso is not None:
            M = max(M, float(expo_piso))
        if M <= 0.0:
            continue
        aF, aR, aS = M * fF, M * fR, M * fS
        if nom in A.APETITIVAS:
            pF += aF; pR += aR; pS += aS
        else:
            nF += aF; nR += aR; nS += aS
    return opponent_distance(_S(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS),
                             DEFAULT_CONFIG)


def d_de_filas(filas, expo_piso=None):
    """Rehace el State del motor desde las filas y devuelve su `d`.

    Es literalmente lo que hace `appraisal_zs_v42_exp.py:1684-1698`: cada fila
    reparte su M en los tres ejes segun `REPARTO` y suma en p o en n segun sea
    apetitiva. Aqui se anade UNA cosa: el piso de exposicion de D2, o sea que
    `S-8-EXPOSICION` no puede bajar de lo que valia en `t`.
    """
    from motor.model import State as _S
    pF = nF = pR = nR = pS = nS = 0.0
    for nom, (fF, fR, fS) in A.REPARTO.items():
        v = filas.get(nom)
        M = float((v or {}).get("M") or 0.0) if isinstance(v, dict) else 0.0
        if nom == EXPO and expo_piso is not None:
            M = max(M, float(expo_piso))
        if M <= 0.0:
            continue
        aF, aR, aS = M * fF, M * fR, M * fS
        if nom in A.APETITIVAS:
            pF += aF; pR += aR; pS += aS
        else:
            nF += aF; nR += aR; nS += aS
    return opponent_distance(_S(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS),
                             DEFAULT_CONFIG)


def _d(o, mundo, mem, tic, expo_piso=None):
    try:
        if expo_piso is None:
            st, _rad = A.appraise(o, mundo, mem, tic)
            return opponent_distance(st, DEFAULT_CONFIG)
        return d_de_crudas(A.filas(o, mundo, mem, tic), expo_piso)
    except Exception:
        return None


def curva_en2(estado0, obs_t, tramos, mundo, mem, suelo, tics, expo_piso=None):
    """`curva_en` con el piso de exposicion opcional (D2)."""
    import copy as _c
    out, e, suelo_act = [], _c.deepcopy(estado0), dict(suelo)
    tr = tramos[0]
    plan = {"destino": tr.get("destino"),
            "coger": tr.get("intencion") == "coger",
            "usar": tr.get("item") if tr.get("intencion") == "usar" else None}
    for tic in tics:
        K = tic - e["tick"]
        if K < 0:
            continue
        e = P.proyectar(e, plan, K, mundo, suelo_act)
        plan = {"destino": None, "coger": False, "usar": None}
        o = foto_proyectada(obs_t, e, mundo, tic, list(suelo_act.values()))
        out.append({"tic": tic, "d": _d(o, mundo, mem, tic, expo_piso),
                    "vida": e["hp"], "W": e.get("W"), "pos": tuple(e["pos"])})
    return out


def curva_multi(estado0, obs_t, tramos, mundo, mem, suelo, expo_piso=None):
    """La curva de una forma de VARIOS tramos, con piso de exposicion."""
    import copy as _c
    pcs = puntos_de_control(estado0, tramos)
    out, e, suelo_act = [], _c.deepcopy(estado0), dict(suelo)
    for tic, tr, pos in pcs:
        K = tic - e["tick"]
        if K < 0:
            continue
        plan = {"destino": tr.get("destino"),
                "coger": tr.get("intencion") == "coger",
                "usar": tr.get("item") if tr.get("intencion") == "usar" else None}
        e = P.proyectar(e, plan, K, mundo, suelo_act)
        if tr.get("intencion") == "coger":
            suelo_act.pop(tuple(tr.get("destino") or ()), None)
        o = foto_proyectada(obs_t, e, mundo, tic, list(suelo_act.values()))
        out.append({"tic": tic, "d": _d(o, mundo, mem, tic, expo_piso),
                    "vida": e["hp"], "W": e.get("W"), "pos": tuple(e["pos"])})
    return out


def mejor_propia2(estado0, obs_t, base, tics, mundo, mem, suelo, t0,
                  vida_min=VIDA_MIN, expo_piso=None):
    """`mejor_propia` con piso de exposicion. Devuelve (curva, quien, sin_vida,
    n_candidatos, se_mueve)."""
    if not tics:
        return None, None, None, 0, None
    hor = tics[-1] - t0
    ok, todas = [], []
    for n, rec in base:
        tr = forma_de_candidato(n, rec, hor, estado0["pos"])
        c = curva_en2(estado0, obs_t, tr, mundo, mem, suelo, tics, expo_piso)
        k = coste(c, t0)
        flojo = any(p["vida"] is not None and p["vida"] < vida_min for p in c)
        mueve = bool(tr[0].get("destino"))
        todas.append((k, n, c, flojo, mueve))
        if not flojo:
            ok.append((k, n, c, mueve))
    if ok:
        k, n, c, mv = min(ok, key=lambda x: x[0])
        return c, n, False, len(base), mv
    k, n, c, _f, mv = min(todas, key=lambda x: x[0])
    return c, n, True, len(base), mv


# ── [P5-3E] EL PISO DE TODAS LAS FILAS QUE MIRAN A UN ASIENTO AJENO ────────
# PRINCIPIO DECLARADO: la forma no cobra seguridad por lo que no ve. Como los
# otros van CONGELADOS en la foto proyectada, ninguna fila que dependa de donde
# esten puede BAJAR por el camino; puede subir si el camino se les acerca.
#
# Las filas, con la linea de `appraisal_zs_v42_exp.py` donde toman valor:
# [CORRECCION P5-3F] F-ANTICIPACION **NO** mira a los rivales: mira AL ANILLO
# (`:975` «solo lo CIERTO: calendario del anillo»; `:986` recorre
# `mundo.eventos_arde(pos, tick)`). Es determinista y SI se proyecta, asi que
# ponerle piso, como hice en P5-3E, impedia a la forma cobrar una mejora
# legitima: salir del fuego. Se saca de la lista.
#   RIVALES
#     F-4-ALCANCE         :1070   estas a tiro de alguien
#     S-8-EXPOSICION      :1416   cuantos hostiles pueden verte
#     S-7-AGRESOR         :1508   ese te esta pegando
#     MIEDO_APRENDIDO     :1553   (apagada en esta configuracion)
#     S-VIDA-AJENA        :1663   (apagada en esta configuracion)
#   EL HERMANO, que tambien es un asiento ajeno y tambien va congelado
#     S-COMPANIA          :1035   lo quieres cerca
#     S-SOLEDAD           :1096   llevas rato sin verlo
#     S-DANO-PAREJA       :1171   le estan pegando
#     S-MUERTE-PAREJA     :1124   se te muere
#     S-VINCULO           :1197   el golpe puede romper el vinculo
#     S-HERIDO            :1302   esta peor que tu
#     S-PROVISION         :1362   tu llevas cura y el no
#     F-HERMANO-AMENAZA   :1642   esta a tiro de alguien
#     F-HERMANO-GOLPE     :1643   el golpe que le cae lo notas
#     R-HERMANO-FALTA     :1644   le falta con que curarse
#
# NO llevan piso, porque no miran a nadie: F-DANO (:875, vida propia que
# falta), F-ANTICIPACION (:1000, el anillo), F-REENCUENTRO (:931, memoria del
# mapa), R-ACOPIO (:951-973), R-CARENCIA (:1076) y R-LLAMADA (:1088), que miran
# el propio inventario y el suelo, y el suelo SI se proyecta.
PISO_OTROS = (
    "F-4-ALCANCE", "S-8-EXPOSICION", "S-7-AGRESOR",
    "MIEDO_APRENDIDO", "S-VIDA-AJENA",
    "S-COMPANIA", "S-SOLEDAD", "S-DANO-PAREJA", "S-MUERTE-PAREJA",
    "S-VINCULO", "S-HERIDO", "S-PROVISION",
    "F-HERMANO-AMENAZA", "F-HERMANO-GOLPE", "R-HERMANO-FALTA",
)


def pisos_de(obs, mundo, mem, tick):
    """El valor en `tick` de cada fila que mira a un asiento ajeno."""
    F_ = A.filas(obs, mundo, mem, tick) or {}
    return {k: float(F_.get(k) or 0.0) for k in PISO_OTROS}


def d_con_pisos(F_, pisos=None):
    """`d` del motor desde las filas crudas, con piso por fila.

    Con `pisos=None` es bit a bit `opponent_distance(appraise(...)[0])`.
    """
    from motor.model import State as _S
    pF = nF = pR = nR = pS = nS = 0.0
    for nom, (fF, fR, fS) in A.REPARTO.items():
        M = float(F_.get(nom) or 0.0)
        if pisos and nom in pisos:
            M = max(M, pisos[nom])
        if M <= 0.0:
            continue
        aF, aR, aS = M * fF, M * fR, M * fS
        if nom in A.APETITIVAS:
            pF += aF; pR += aR; pS += aS
        else:
            nF += aF; nR += aR; nS += aS
    return opponent_distance(_S(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS),
                             DEFAULT_CONFIG)


# ── [P5-3E · E5] SIN `deepcopy` ────────────────────────────────────────────
def copia_estado(e):
    """Copia de un estado sin `copy.deepcopy`.

    Solo se copian las piezas que `proyectar` MUTA: la mochila (sus dicts
    cambian de `n` y se anaden), la mano, los efectos y el canal de cura. La
    posicion es una tupla y los numeros son inmutables.
    """
    n = dict(e)
    n["pack"] = [dict(s) for s in (e.get("pack") or [])]
    h = e.get("hand")
    n["hand"] = dict(h) if isinstance(h, dict) else h
    n["effects"] = list(e.get("effects") or [])
    c = e.get("cura")
    n["cura"] = dict(c) if isinstance(c, dict) else c
    return n


def foto_rapida(obs_t, e, mundo, tick, suelo_restante):
    """`foto_proyectada` sin `deepcopy`: se construye el dict de cero y se
    comparten las piezas que nadie muta (`agents`, `bushes`, `projectiles`)."""
    vis0 = obs_t.get("visible") or {}
    z0 = obs_t.get("zone") or {}
    c, radio, dps = mundo.anillo_en(tick)
    return {
        "type": obs_t.get("type"), "tick": tick, "phase": obs_t.get("phase"),
        "you": {"pos": list(e["pos"]), "hp": e["hp"],
                "stats": (obs_t.get("you") or {}).get("stats"),
                "hand": e.get("hand"), "body": e.get("body"),
                "pack": e.get("pack") or [],
                "effects": e.get("effects") or [],
                "damage_taken": [], "kills": (obs_t.get("you") or {}).get("kills", 0),
                "damage_dealt": (obs_t.get("you") or {}).get("damage_dealt", 0),
                "move_ready_in": e.get("move_ready_in", 0),
                "attack_ready_in": e.get("attack_ready_in", 0),
                "action_result": (obs_t.get("you") or {}).get("action_result")},
        "visible": {"agents": vis0.get("agents") or [],
                    "items": suelo_restante,
                    "pods": vis0.get("pods") or [],
                    "bushes": vis0.get("bushes") or [],
                    "projectiles": vis0.get("projectiles") or []},
        "zone": {"center": list(c), "radius": radio, "damage_per_s": dps,
                 "next_radius": z0.get("next_radius"),
                 "warn_tick": z0.get("warn_tick"),
                 "shrink_tick": z0.get("shrink_tick")},
        "events": [], "chat": []}


def _d2(o, mundo, mem, tic, pisos=None):
    try:
        if not pisos:
            st, _r = A.appraise(o, mundo, mem, tic)
            return opponent_distance(st, DEFAULT_CONFIG)
        return d_con_pisos(A.filas(o, mundo, mem, tic), pisos)
    except Exception:
        return None


def curva_rapida(estado0, obs_t, tramos, mundo, mem, suelo, tics=None,
                 pisos=None):
    """Curva de una forma, sin `deepcopy`. Si `tics` es None, usa los puntos
    de control de los tramos (varios tramos); si se da, evalua en esos."""
    e = copia_estado(estado0)
    suelo_act = dict(suelo)
    out = []
    if tics is None:
        pcs = puntos_de_control(estado0, tramos)
        pasos = [(tic, tr) for tic, tr, _p in pcs]
    else:
        pasos = [(tic, (tramos[0] if i == 0 else
                        {"destino": None, "intencion": "esperar"}))
                 for i, tic in enumerate(tics)]
    for tic, tr in pasos:
        K = tic - e["tick"]
        if K < 0:
            continue
        plan = {"destino": tr.get("destino"),
                "coger": tr.get("intencion") == "coger",
                "usar": tr.get("item") if tr.get("intencion") == "usar" else None}
        e = P.proyectar_rapido(e, plan, K, mundo, suelo_act)
        if tr.get("intencion") == "coger":
            suelo_act.pop(tuple(tr.get("destino") or ()), None)
        o = foto_rapida(obs_t, e, mundo, tic, list(suelo_act.values()))
        out.append({"tic": tic, "d": _d2(o, mundo, mem, tic, pisos),
                    "vida": e["hp"], "W": e.get("W"), "pos": tuple(e["pos"])})
    return out


def mejor_propia3(estado0, obs_t, base, tics, mundo, mem, suelo, t0,
                  vida_min=VIDA_MIN, pisos=None):
    if not tics:
        return None, None, None, 0, None
    hor = tics[-1] - t0
    ok, todas = [], []
    for n, rec in base:
        tr = forma_de_candidato(n, rec, hor, estado0["pos"])
        c = curva_rapida(estado0, obs_t, tr, mundo, mem, suelo, tics, pisos)
        k = coste(c, t0)
        flojo = any(p["vida"] is not None and p["vida"] < vida_min for p in c)
        mueve = bool(tr[0].get("destino"))
        todas.append((k, n, c, flojo, mueve))
        if not flojo:
            ok.append((k, n, c, mueve))
    if ok:
        k, n, c, mv = min(ok, key=lambda x: x[0])
        return c, n, False, len(base), mv
    k, n, c, _f, mv = min(todas, key=lambda x: x[0])
    return c, n, True, len(base), mv


def juzga_margen(c_forma, c_solo, t0, vida_min=VIDA_MIN, margen=0.0):
    flojo = [p for p in c_forma if p["vida"] is not None
             and p["vida"] < vida_min]
    ar, det = area(c_forma, c_solo, t0)
    if flojo:
        return "vida", ar, {"puntos": det, "punto_flojo": flojo[0]}
    if ar <= margen:
        return "area", ar, {"puntos": det}
    return "ok", ar, {"puntos": det}


# ── [P5-3G] CURVA CON ALCANCE Y CON HERMANO ────────────────────────────────
def curva_G(estado0, obs_w, tramos, mundo, mem, suelo, tics, filas_mapa,
            herm_slot, diario_h=None, con_hermano=False):
    """Curva con los rivales en su PEOR casilla alcanzable (G1) y, si se pide,
    con el hermano en su estado REAL leido de su diario (G2). Sin pisos."""
    import alcance_g as AL
    e = copia_estado(estado0)
    suelo_act = dict(suelo)
    out, cache = [], {}
    t0 = estado0["tick"]
    for i, tic in enumerate(tics):
        K = tic - e["tick"]
        if K < 0:
            continue
        tr = tramos[i] if i < len(tramos) else {"destino": None,
                                                "intencion": "esperar"}
        plan = {"destino": tr.get("destino"),
                "coger": tr.get("intencion") == "coger",
                "usar": tr.get("item") if tr.get("intencion") == "usar" else None}
        e = P.proyectar_rapido(e, plan, K, mundo, suelo_act)
        if tr.get("intencion") == "coger":
            suelo_act.pop(tuple(tr.get("destino") or ()), None)
        o = foto_rapida(obs_w, e, mundo, tic, list(suelo_act.values()))
        o, _det = AL.obs_con_alcance(o, mundo, filas_mapa, tuple(e["pos"]),
                                     tic - t0, herm_slot, cache)
        m = mem
        if con_hermano and diario_h is not None:
            o, m = AL.pon_hermano(o, mem, herm_slot, diario_h.get(tic),
                                  tuple(e["pos"]), mundo)
        out.append({"tic": tic, "d": _d2(o, mundo, m, tic, None),
                    "vida": e["hp"], "W": e.get("W"), "pos": tuple(e["pos"])})
    return out


def mejor_propia_G(estado0, obs_w, base, tics, mundo, mem, suelo, t0,
                   filas_mapa, herm_slot, diario_h=None, con_hermano=False,
                   vida_min=VIDA_MIN):
    if not tics:
        return None, None, 0, None
    hor = tics[-1] - t0
    ok, todas = [], []
    for n, rec in base:
        tr = forma_de_candidato(n, rec, hor, estado0["pos"])
        c = curva_G(estado0, obs_w, tr, mundo, mem, suelo, tics, filas_mapa,
                    herm_slot, diario_h, con_hermano)
        k = coste(c, t0)
        flojo = any(p["vida"] is not None and p["vida"] < vida_min for p in c)
        mueve = bool(tr[0].get("destino"))
        todas.append((k, n, c, flojo, mueve))
        if not flojo:
            ok.append((k, n, c, mueve))
    if ok:
        k, n, c, mv = min(ok, key=lambda x: x[0])
        return c, n, len(base), mv
    k, n, c, _f, mv = min(todas, key=lambda x: x[0])
    return c, n, len(base), mv


# ── [P5-3H] E1+G2: rivales a PISO, hermano que CUENTA ──────────────────────
PISO_RIVAL = ("F-4-ALCANCE", "S-8-EXPOSICION", "S-7-AGRESOR",
              "MIEDO_APRENDIDO", "S-VIDA-AJENA")


def pisos_rival(obs, mundo, mem, tick):
    F_ = A.filas(obs, mundo, mem, tick) or {}
    return {k: float(F_.get(k) or 0.0) for k in PISO_RIVAL}


def curva_H(estado0, obs_w, tramos, mundo, mem, suelo, tics, herm_slot,
            diario_h, pisos):
    """Rivales a PISO (no mejoran), hermano REAL de su diario, lo demas
    proyectado (incluido el anillo por F-ANTICIPACION)."""
    import alcance_g as AL
    e = copia_estado(estado0)
    suelo_act = dict(suelo)
    out = []
    for i, tic in enumerate(tics):
        K = tic - e["tick"]
        if K < 0:
            continue
        tr = tramos[i] if i < len(tramos) else {"destino": None,
                                                "intencion": "esperar"}
        plan = {"destino": tr.get("destino"),
                "coger": tr.get("intencion") == "coger",
                "usar": tr.get("item") if tr.get("intencion") == "usar" else None}
        e = P.proyectar_rapido(e, plan, K, mundo, suelo_act)
        if tr.get("intencion") == "coger":
            suelo_act.pop(tuple(tr.get("destino") or ()), None)
        o = foto_rapida(obs_w, e, mundo, tic, list(suelo_act.values()))
        m = mem
        if diario_h is not None:
            o, m = AL.pon_hermano(o, mem, herm_slot, diario_h.get(tic),
                                  tuple(e["pos"]), mundo)
        out.append({"tic": tic, "d": _d2(o, mundo, m, tic, pisos),
                    "vida": e["hp"], "W": e.get("W"), "pos": tuple(e["pos"])})
    return out


def mejor_propia_H(estado0, obs_w, base, tics, mundo, mem, suelo, t0,
                   herm_slot, diario_h, pisos, vida_min=VIDA_MIN):
    if not tics:
        return None, None, 0, None
    hor = tics[-1] - t0
    ok, todas = [], []
    for n, rec in base:
        tr = forma_de_candidato(n, rec, hor, estado0["pos"])
        c = curva_H(estado0, obs_w, tr, mundo, mem, suelo, tics, herm_slot,
                    diario_h, pisos)
        k = coste(c, t0)
        flojo = any(p["vida"] is not None and p["vida"] < vida_min for p in c)
        mueve = bool(tr[0].get("destino"))
        todas.append((k, n, c, flojo, mueve))
        if not flojo:
            ok.append((k, n, c, mueve))
    if ok:
        k, n, c, mv = min(ok, key=lambda x: x[0])
        return c, n, len(base), mv
    k, n, c, _f, mv = min(todas, key=lambda x: x[0])
    return c, n, len(base), mv
