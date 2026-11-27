"""[P7-33] LA ETAPA DE LO INUTIL: nacer sin saber nada de CUATRO cosas (botiquin, racion, red y camuflaje), probar la red y el camuflaje con una ventana de tiempo,
y el oido y la ley (los avisos del mundo). Diseno de Manel (9-oct); numeros de la mesa. Pieza enganchada DESDE FUERA, despues de descubre, pedir, nacer (P7-23) y
P7-29, sobre el cuerpo congelado del seis. Interruptor GEMV_P7_33=1 (apagado por defecto: con 0 no toca nada). Con GEMV_P7_SABE=1 (TECHO) solo queda el oido y la ley.

LO QUE SE BORRA DE LA RED Y DEL CAMUFLAJE (lo que el cuerpo sabe de ellos; inventario con archivo y linea, como en P7-23 con el botiquin y la racion):
  1. Su valor en la riqueza W: `gear_menor` = GEAR_MENOR_W (0,25) por el camuflaje puesto y 0,25 por la red en la mano o en el zurron
     (appraisal_zs_v42_exp.py:413, :761-769). Pasa a 0,25 x k_camuflaje y 0,25 x k_red (envoltorio de `A.riqueza_W`).
  2. Los radios del camuflaje: con el puesto, los rivales a mas de CAMO_QUIETO = 4 casillas (quieta) o CAMO_MOVIENDO = 7 (en movimiento) no la ven en S-8 EXPOSICION
     (appraisal_zs_v42_exp.py:405-406, :1393-1411). Pasan a 4 x k_camuflaje y 7 x k_camuflaje mientras se calculan las filas (con k = 0 nadie deja de verla: como
     sin camuflaje).
  3. La promesa del camuflaje en el suelo: el alivio de S-8 que daria llevarlo (decisor_zs.py:672-677): sale de las mismas filas, asi que ya va escalada por 2.
     La red no tiene promesa propia (su dano es 0: `arma` = 0, :731-745) ni candidato `empunar` (:536-544, solo armas con dano).
  4. Ganas: solo R-CARENCIA (el hueco en W, :1076), que ya va por 1. Regalo y pedido: el cuerpo no regala ni pide gear (solo botiquin y raciones, P7-8 y P7-17);
     nada que borrar, declarado.
  k_cosa (red, camuflaje) = (1 - ignorancia) x creencia vivida en el cuerpo + ignorancia x esperanza de la otra cosa de gear, dividido por la vida entera (hp_max,
  100): lo que cree que le da en el cuerpo (vida conservada + dano conocido) por lo que vale la vida; "no se" -> 0. (Numero de esta pieza, declarado: no hay cura
  de catalogo para el gear.)
PROBAR LA RED Y EL CAMUFLAJE (puntos 2, 3 y 7): la prueba tiene un tiempo. Camuflaje: una ventana de VENTANA_S = 10 segundos llevandolo PUESTO (`you.body`), o
  antes si se lo quita. Red: 10 segundos con ella en la mochila o en la mano, o antes si la suelta o la lanza. Una prueba por cada vez que la cosa llega (se pone, entra en el zurron): no se encadenan ventanas mientras la sigue llevando (declarado). La huella, como cualquier recuerdo (P7-23): efecto
  cuerpo = vida al cerrar - vida al abrir + dano conocido en la ventana; recursos = unidades al cerrar - al abrir (el hueco que ocupa, como lo cuenta el cuerpo);
  vinculo = distancia a la hermana; importancia = lo que movio el malestar; foto emocional, contexto y acciones al abrir; mas `duracion`, `completa` (llego a
  los 10 s) y `peligro`. Sin "al menos" (no hay cura que tope) y sin corte (la prueba acaba cuando acaba la ventana o se va la cosa): declarado. Si no cambio nada,
  el recuerdo dice "no hizo nada" (efecto 0).
LA CURIOSIDAD DE LA CLASE (punto 4), para las cuatro: ignorancia x alivio; tenerla alivia la mitad (ALIVIO_ZURRON; la red en zurron o mano, el camuflaje en zurron
  o puesto) y probarla el resto (los recuerdos bajan la ignorancia). `ir_curioso` va a la clase que mas llama de las cuatro (aqui se extiende la de P7-23 a la red
  y el camuflaje). La curiosidad del CUANTO (P7-29) sigue siendo de los consumibles: la red y el camuflaje no se "usan"; declarado. La esperanza del botiquin y de
  la racion sigue saliendo solo de la otra cosa consumible (no del gear).
OIDO Y LEY (punto 5, decision de Manel): el cuerpo lee `event_warning` (inundacion: rectangulo y plazo; tormenta de fuego: centro, radio y plazo) y, mientras dura
  el evento, esas casillas son no transitables en su mapa (`mundo.solido`, envuelto; el campo geodesico cacheado se vacia cuando cambia lo activo). En los tres
  brazos. Nota: `solido` tambien corta la linea de vista (mundo.py:231-247); declarado.
MEDIDA (punto 8, sin construir nada): en cada prueba de cada cosa, el contexto al abrirla: en calma o en peligro (rival a 4 casillas o menos, fuego, vida < 30).
"""
from __future__ import annotations
import collections, math
from alma import decisor_zs as D
from alma import appraisal_zs_v42_exp as A
import descubre_P7 as X
import nace_P7_23 as N
import nace_P7_29 as N29
from cuaderno_P7 import DOMINIOS
from recuerdo_P7_23 import foto_de_radio
_unidades_de0 = N.unidades_de          # la de P7-23, antes de envolverla

ON = X._on("GEMV_P7_33")
VENTANA_S = 10.0                      # numero de la mesa: la ventana de la prueba de la red y del camuflaje
PELIGRO_RIVAL = 4; PELIGRO_VIDA = 30.0   # numeros de la mesa (punto 8)
CAMO_Q0, CAMO_M0, GEAR_W0 = float(A.CAMO_QUIETO), float(A.CAMO_MOVIENDO), float(A.GEAR_MENOR_W)
E = {"registra": None, "ventanas": {}, "presente": {}, "eventos": [], "activos": frozenset(), "mundo_patch": False, "pruebas": 0, "ley": {"avisos": 0, "cambios": 0, "casillas": 0}, "ultimo_k_log": -10 ** 9}


# ── las cuatro cosas ──
def red(mundo): return getattr(mundo, "id_red", "") or "net"
def camo(mundo): return getattr(mundo, "id_camuflaje", "") or "camouflage"
def gear(mundo): return (red(mundo), camo(mundo))
def cuatro(mundo): return (X.kit(mundo), N.racion(mundo)) + gear(mundo)
def tiene(you, mundo, obj):
    """Unidades de la cosa que lleva: la red en zurron o en la mano; el camuflaje en zurron o puesto; botiquin y racion como en P7-23."""
    if obj == red(mundo):
        n = sum(int(s.get("n") or 1) for s in (you.get("pack") or []) if s and s.get("id") == obj); h = you.get("hand") or {}
        return n + (int(h.get("n") or 1) if h.get("id") == obj else 0)
    if obj == camo(mundo):
        c = you.get("body"); cid = c.get("id") if isinstance(c, dict) else c
        return sum(int(s.get("n") or 1) for s in (you.get("pack") or []) if s and s.get("id") == obj) + (1 if cid == obj else 0)
    return _unidades_de0(you, mundo, obj)
def puesto(you, mundo):
    c = you.get("body"); cid = c.get("id") if isinstance(c, dict) else c; return cid == camo(mundo)


# ── lo aprendido de la red y del camuflaje: k ──
def esperanza_gear(mundo, obj, pos, tick):
    vals = [v for o in gear(mundo) if o != obj for v, _ in [N.vivida(mundo, o, pos, tick)] if v is not None]
    return (sum(max(0.0, v) for v in vals) / len(vals)) if vals else 0.0
def k_gear(mundo, obj, pos, tick, mem=None):
    if X.SABE: return 1.0
    v, ign = N.vivida(mundo, obj, pos, tick); cre = 0.0 if v is None else max(0.0, v)
    hp_max = float(getattr(mem, "hp_max", None) or 100.0) if mem is not None else 100.0
    return max(0.0, min(1.0, ((1.0 - ign) * cre + ign * esperanza_gear(mundo, obj, pos, tick)) / hp_max))


# ── el oido y la ley ──
def _oye(self, obs):
    tick = getattr(self, "tick", 0); mundo = self.mundo
    for e in (obs.get("events") or []):
        if e.get("type") == "event_warning" and e not in E["eventos"]:
            E["eventos"].append(e); E["ley"]["avisos"] += 1
            if E["registra"]: E["registra"]({"k": "P7_33_ley", "tick": tick, "aviso": e})
    act = set()
    for e in E["eventos"]:
        t0 = int(e.get("from_tick") or 0); dur = int(e.get("duration") or 0)
        if not (t0 <= tick < t0 + dur): continue
        if e.get("kind") == "flood" and e.get("rect"):
            x0, y0, x1, y1 = e["rect"]; act |= {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
        elif e.get("kind") == "firestorm" and e.get("center"):
            cx, cy = e["center"]; r = int(e.get("radius") or 0); act |= {(x, y) for x in range(cx - r, cx + r + 1) for y in range(cy - r, cy + r + 1) if (x - cx) ** 2 + (y - cy) ** 2 <= r * r}
    act = frozenset(act)
    if not E["mundo_patch"]:
        _s0 = mundo.solido; mundo.solido = lambda x, y, _s0=_s0: ((int(x), int(y)) in E["activos"]) or _s0(x, y); E["mundo_patch"] = True
    if act != E["activos"]:
        E["activos"] = act; mundo._campos_geo = {}; E["ley"]["cambios"] += 1; E["ley"]["casillas"] = len(act)
        if E["registra"]: E["registra"]({"k": "P7_33_ley", "tick": tick, "casillas_no_transitables": len(act), "eventos_activos": sum(1 for e in E["eventos"] if int(e.get("from_tick") or 0) <= tick < int(e.get("from_tick") or 0) + int(e.get("duration") or 0))})


# ── el contexto de cada prueba (punto 8) ──
def peligro_de(self, obs):
    you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); mundo = self.mundo; tick = getattr(self, "tick", 0)
    riv = [a for a in ((obs.get("visible") or {}).get("agents") or []) if a.get("slot") not in (mundo.slot, mundo.teammate_slot) and a.get("pos")]
    d = min((max(abs(a["pos"][0] - pos[0]), abs(a["pos"][1] - pos[1])) for a in riv), default=None)
    fuego = any(e.get("kind") == "firestorm" and e.get("center") and int(e.get("from_tick") or 0) <= tick < int(e.get("from_tick") or 0) + int(e.get("duration") or 0) and (pos[0] - e["center"][0]) ** 2 + (pos[1] - e["center"][1]) ** 2 <= int(e.get("radius") or 0) ** 2 for e in E["eventos"])
    hp = float(you.get("hp") or 0.0)
    p = {"rival_a_4": bool(d is not None and d <= PELIGRO_RIVAL), "d_rival": d, "fuego": bool(fuego), "vida_menor_30": hp < PELIGRO_VIDA, "vida": hp}
    p["calma"] = not (p["rival_a_4"] or p["fuego"] or p["vida_menor_30"]); return p


# ── las ventanas de la red y del camuflaje ──
def ventana_gear(self, obs, radio):
    mundo, mem, tick = self.mundo, self.mem, self.tick; you = obs.get("you") or {}; c = N.cuaderno()
    if c is None or mundo is None: return
    vt = int(VENTANA_S * mundo.tick_rate)
    for obj in gear(mundo):
        presente = (puesto(you, mundo) if obj == camo(mundo) else tiene(you, mundo, obj) >= 1)
        nueva = presente and not E["presente"].get(obj, False); E["presente"][obj] = presente      # una prueba por cada vez que la cosa llega (se pone / entra en el zurron), no una cadena de ventanas
        v = E["ventanas"].get(obj)
        if v is None:
            if nueva:
                d0, como0 = X.dist_hermano(obs, mundo, mem); pos = tuple(you.get("pos") or (0, 0))
                E["ventanas"][obj] = {"objeto": obj, "t0": tick, "contexto": N.contexto_ahora(mundo, pos, tick), "foto": foto_de_radio(radio) or N.E["foto"], "acciones": list(N.E["acciones"]), "hp0": float(you.get("hp") or 0.0), "unidades0": X.unidades(you), "dist0": d0, "como0": como0, "mal0": X.malestar_ejes(radio),
                                     "conocido": 0.0, "fuentes": [], "total": 0.0, "peligro": peligro_de(self, obs)}
                if E["registra"]: E["registra"]({"k": "P7_33_prueba", "momento": "abre", "tick": tick, "objeto": obj, "peligro": E["ventanas"][obj]["peligro"], "hp": you.get("hp"), "ignorancia": round(c.ignorancia(obj), 4), "ganas": round(k_gear(mundo, obj, pos, tick, mem), 4)})
            continue
        if tick > v["t0"]:
            con, fu = X._dano_conocido(obs, mundo, tick); v["conocido"] += con; v["fuentes"] += fu
            v["total"] += sum(float(d.get("amount") or 0.0) for d in (you.get("damage_taken") or []))
        completa = tick - v["t0"] >= vt
        if presente and not completa: continue
        d1, como1 = X.dist_hermano(obs, mundo, mem); mal1 = X.malestar_ejes(radio)
        efecto = {"cuerpo": (float(you.get("hp") or 0.0) - v["hp0"]) + v["conocido"], "recursos": X.unidades(you) - v["unidades0"], "vinculo": ((d1 - v["dist0"]) if (d1 is not None and v["dist0"] is not None) else 0.0)}
        importancia = {dom: (mal1.get(dom, 0.0) - v["mal0"].get(dom, 0.0)) for dom in DOMINIOS}
        r = c.apunta_P23(obj, v["contexto"], v["foto"], v["acciones"], efecto, importancia, tick=v["t0"], al_menos=False, corte=False) if X.CUADERNO_ON else None
        if r is not None: r["prueba"] = {"duracion": tick - v["t0"], "completa": completa, "peligro": v["peligro"]}
        h = {"k": "P7_huella", "objeto": obj, "t0": v["t0"], "t_fin": tick, "situacion": "dentro" if v["contexto"]["dentro"] else "fuera", "contexto": v["contexto"], "foto": v["foto"], "hp0": v["hp0"], "hp_fin": you.get("hp"), "al_menos": False, "corte": False, "completa": completa, "duracion": tick - v["t0"],
             "motivo_cierre": ("ventana" if completa else "se fue la cosa"), "dano_total": round(v["total"], 3), "fuentes_conocidas": v["fuentes"], "efecto": {k_: round(x, 4) for k_, x in efecto.items()}, "importancia": {k_: round(x, 4) for k_, x in importancia.items()}, "intensidad": (r or {}).get("intensidad"), "apuntado": bool(r),
             "peligro": v["peligro"], "creencia_despues": (c.creencia(obj, "dentro" if v["contexto"]["dentro"] else "fuera") if X.CUADERNO_ON else None), "ignorancia_despues": round(c.ignorancia(obj), 4)}
        X.ESTADO["huellas"].append(h); E["pruebas"] += 1
        if E["registra"]: E["registra"](h)
        E["ventanas"][obj] = None


# ── los enganches ──
def aplica(clase, registra=None):
    E["registra"] = registra
    if not (ON and X.ON): return {"P7_33": False}
    _od = clase.decidir
    if X.SABE or not N.NACE:
        def decidir_t(self, obs, _d=_od):
            if getattr(self, "mundo", None) is not None: _oye(self, obs)
            return _d(self, obs)
        clase.decidir = decidir_t
        return {"P7_33": True, "solo": "oido y ley (TECHO o sin nace)", "VENTANA_S": VENTANA_S}
    # las cuatro cosas entran en la curiosidad de la clase; la esperanza y el cuanto siguen siendo de los consumibles
    _cons = N.consumibles; N.consumibles = cuatro; N.unidades_de = tiene
    _esp = N.esperanza
    def esperanza2(mundo, obj, pos, tick):
        N.consumibles = _cons
        try: return _esp(mundo, obj, pos, tick)
        finally: N.consumibles = cuatro
    N.esperanza = esperanza2
    _cu = N29.cuanto_M
    def cuanto2(obs, mundo, mem, F):
        N.consumibles = _cons
        try: return _cu(obs, mundo, mem, F)
        finally: N.consumibles = cuatro
    N29.cuanto_M = cuanto2
    # 1 y 2: W y radios del camuflaje por lo aprendido
    _ow = A.riqueza_W; _of = A.filas; _op = D._promesa; _oc = D.candidatos
    def _riqueza(you, mundo):
        W, d = _ow(you, mundo); d2 = dict(d); pos, tick = N.E.get("pos_tick", ((0, 0), 0))
        g = 0.0
        if mundo.id_camuflaje and puesto(you, mundo): g += GEAR_W0 * k_gear(mundo, camo(mundo), pos, tick)
        if mundo.id_red and tiene(you, mundo, red(mundo)) >= 1: g += GEAR_W0 * k_gear(mundo, red(mundo), pos, tick)
        d2["gear_menor"] = g; return sum(d2.values()), d2
    def _filas(obs, mundo, mem, tick):
        pos = tuple((obs.get("you") or {}).get("pos") or (0, 0)); kc = k_gear(mundo, camo(mundo), pos, tick, mem)
        A.CAMO_QUIETO = CAMO_Q0 * kc; A.CAMO_MOVIENDO = CAMO_M0 * kc
        try: F = _of(obs, mundo, mem, tick)
        finally: A.CAMO_QUIETO = CAMO_Q0; A.CAMO_MOVIENDO = CAMO_M0
        F["_P7_33"] = {"k_camuflaje": round(kc, 4), "k_red": round(k_gear(mundo, red(mundo), pos, tick, mem), 4)}
        return F
    def _promesa(obs, mundo, mem, tick, item_id):
        base = _op(obs, mundo, mem, tick, item_id)
        if not X.NOVEDAD_ON or item_id not in gear(mundo): return base
        you = obs.get("you") or {}
        if tiene(you, mundo, item_id) >= 1: return base
        cc = N.clase_curiosa(obs, mundo)
        if not cc or cc[0] != item_id: return base
        t, F = X.ESTADO["calma_cache"]
        if t != tick: F = A.filas(obs, mundo, mem, tick); X.ESTADO["calma_cache"] = (tick, F)
        M, _, _, _ = N29.curiosidad_M(obs, mundo, F); return base + M * (1.0 - X.ALIVIO_ZURRON)
    def _cands(obs, mundo, mem, tick, bloqueos=None):
        out = _oc(obs, mundo, mem, tick, bloqueos)
        if not X.NOVEDAD_ON: return out
        you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); c = N.cuaderno()
        llamadas = {o: (1.0 if (c is None or not X.CUADERNO_ON) else float(c.ignorancia(o))) * N29.alivio_clase(obs, mundo, o) for o in cuatro(mundo)}
        top = max(llamadas.values()) if llamadas else 0.0
        clases = [o for o, v in llamadas.items() if v >= top - 1e-9 and v > 0 and tiene(you, mundo, o) == 0]
        if not any(o in gear(mundo) for o in clases): return out            # la clase que mas llama es un consumible: lo de P7-23/29 vale
        out = [(n_, r_) for n_, r_ in out if n_ != "ir_curioso"]; N29.E["curioso"] = None
        ced = getattr(mem, "cedidos", {}); vis = obs.get("visible") or {}; ids = {o for o in clases if o in gear(mundo)}
        if any(o not in gear(mundo) for o in clases): ids |= {X.kit(mundo)} | set(N.raciones(mundo))      # empate con un consumible: todos los sitios compiten por camino
        sitios = {tuple(it.get("pos") or ()): (it.get("id"), int(it.get("n") or 1), float(A.VALOR_NIVEL["cajones"])) for it in (vis.get("items") or []) if it.get("id") in ids and it.get("pos")}
        for p_, v_ in (getattr(mem, "objetos_vistos", None) or {}).items():
            if v_ and v_[0] in ids and tuple(p_) not in sitios: sitios[tuple(p_)] = tuple(v_)
        sitios = {p_: v_ for p_, v_ in sitios.items() if p_ not in ced and p_ != pos}
        pasos = {}
        for p_ in sitios:
            try: campo = D.campo_geodesico(mundo, p_)
            except Exception: campo = None
            if campo and pos in campo: pasos[p_] = campo[pos]
        if pasos:
            dest = min(pasos, key=lambda p_: (pasos[p_], math.dist(pos, p_)))
            if not any(n_ == "ir_objeto" and tuple(r_.get("destino") or ()) == dest for n_, r_ in out):
                cuerpos = frozenset(tuple(a.get("pos") or ()) for a in (vis.get("agents") or []) if a.get("pos")); cid = sitios[dest][0]
                clase = X.kit(mundo) if cid == X.kit(mundo) else (N.racion(mundo) if cid in N.raciones(mundo) else cid)
                out.append(("ir_curioso", {"tipo": "ir", "destino": dest, "cuerpos": cuerpos, "curioso": clase})); N29.E["curioso"] = (clase, tuple(dest))
        N29.E["cands"] = [n_ for n_, _ in out]; N29.E["idx"] = 0
        return out
    def decidir(self, obs, _d=_od):
        if getattr(self, "mundo", None) is not None: _oye(self, obs)
        accion, radio = _d(self, obs)
        if radio is not None and getattr(self, "phase", None) == "live":
            try: ventana_gear(self, obs, radio)
            except Exception as ex:
                if E["registra"]: E["registra"]({"k": "P7_error", "tick": getattr(self, "tick", None), "error": "P7-33 ventana: " + repr(ex)[:160]})
            # el contexto de las pruebas de botiquin y racion (punto 8): la ventana de P7-23 acaba de abrirse en este tic
            v = N.E.get("ventana")
            if v is not None and v.get("t0") == self.tick and "peligro" not in v:
                v["peligro"] = peligro_de(self, obs)
                if E["registra"]: E["registra"]({"k": "P7_33_prueba", "momento": "abre", "tick": self.tick, "objeto": v["objeto"], "peligro": v["peligro"], "hp": (obs.get("you") or {}).get("hp")})
            if self.tick - E["ultimo_k_log"] >= 250 and E["registra"]:
                E["ultimo_k_log"] = self.tick; c = N.cuaderno(); mundo = self.mundo; pos = tuple((obs.get("you") or {}).get("pos") or (0, 0))
                E["registra"]({"k": "P7_33_k", "tick": self.tick, "ganas": {"botiquin": round(X.k_ganas(mundo), 4), "racion": round(N.k_de(mundo, N.racion(mundo), pos, self.tick), 4), "red": round(k_gear(mundo, red(mundo), pos, self.tick, self.mem), 4), "camuflaje": round(k_gear(mundo, camo(mundo), pos, self.tick, self.mem), 4)},
                               "ignorancia": ({o: round(c.ignorancia(o), 4) for o in cuatro(mundo)} if c is not None else None), "tiene": {o: tiene(obs.get("you") or {}, mundo, o) for o in cuatro(mundo)}, "ley": dict(E["ley"])})
        return accion, radio
    A.riqueza_W, A.filas, D._promesa, D.candidatos, clase.decidir = _riqueza, _filas, _promesa, _cands, decidir
    return {"P7_33": True, "cuatro": True, "VENTANA_S": VENTANA_S, "PELIGRO_RIVAL": PELIGRO_RIVAL, "PELIGRO_VIDA": PELIGRO_VIDA, "borra": ["W gear_menor (k_red, k_camuflaje)", "radios del camuflaje (x k_camuflaje)", "promesa del camuflaje (via filas)", "curiosidad de las cuatro clases", "ventanas de red y camuflaje (10 s)", "oido y ley"]}
