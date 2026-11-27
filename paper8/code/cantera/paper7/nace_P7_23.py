"""[P7-23] NACER SIN SABER QUE CURAN EL BOTIQUIN NI LA RACION (direccion de Manel, 7-oct). Pieza enganchada DESDE FUERA, despues de
`descubre_P7.aplica` y `pide_P7.aplica`, sobre el cuerpo congelado del seis. Interruptor GEMV_P7_NACE=1 (apagado por defecto); no hace nada
con GEMV_P7_SABE=1 (TECHO) ni con GEMV_P7=0.

LO QUE SE BORRA (los dos consumibles, botiquin `id_botiquin` y racion `id_raciones`; inventario de P7-0, seccion 2, y las piezas del siete):
  1. El efecto en la imaginacion: `receta["heal"]` de `usar_botiquin` y `usar_racion` (decisor_zs.py:484-493, la previsión :823-825) pasa a ser lo
     recordado por parecido, y "no se" -> 0 (ya lo hacia P7-5 para el botiquin: `descubre_P7.heal_imaginado`; aqui tambien la racion).
  2. Las ganas de tenerlos: R-ACOPIO entera (appraisal:935-973, ya escalada por P7-5 con k) y el termino del botiquin en W (:749, idem); el termino
     de la racion en W (:751-759, RACION_2A :411) se escala por k_racion; el objetivo W_TARGET (:126) pasa de 2 + k a 1 + k_botiquin + k_racion.
  3. Las filas que regalan y las que leen el hecho: S-PROVISION (:1304-1362, llevar botiquin con la hermana sin venda) y R-HERMANO-FALTA (:1632-1641,
     su parte dice que no lleva cura) se escalan por k_botiquin; la medicina junto al hermano (S-DANO-PAREJA :1143-1174, S-HERIDO :1237-1278) ya se
     pesaba por lo aprendido del botiquin (P7-8, `regalo_aprendido`); aqui tambien la racion en el suelo (las tres filas miran "cualquier consumible
     con heal > 0", :1160, :1258, :1338), con k_racion.
  4. El pedido (pide_P7, P7-17): se abre solo por lo aprendido (k_botiquin > 0), no por la curiosidad.
  5. La esperanza (P7-9) ya no sale del catalogo: esperanza(objeto) = la creencia vivida del otro consumible que el cuerpo ya conoce (por parecido,
     en la situacion de ahora); sin nada conocido de la clase, 0. La mezcla por ignorancia es la de siempre: (1 - ign) x creencia + ign x esperanza,
     con la ignorancia del objeto por parecido (1 / (1 + suma de pesos parecidos)).
LO QUE QUEDA DE NACIMIENTO: la curiosidad (P7-6/7), extendida a las dos clases: M = ACOPIO_M x calma x media de (ignorancia x alivio) de las dos; `ir_curioso`
  va al objeto mas cercano de la clase con mayor ignorancia x alivio (la extension a dos clases es de esta pieza, no de la mesa; declarada).
EL RECUERDO (`recuerdo_P7_23.CuadernoP23`): cada uso de botiquin o racion, completado o cortado, con contexto, foto emocional, acciones, efecto con el
  "al menos", importancia e intensidad (la formula del cuaderno); el corte: efecto 0 en cuerpo y recursos. Una ventana por canal, como P7-5.
"""
from __future__ import annotations
import collections, math, os
from alma import decisor_zs as D
from alma import appraisal_zs_v42_exp as A
import descubre_P7 as X
import pide_P7 as J
from recuerdo_P7_23 import CuadernoP23, foto_de_radio
from cuaderno_P7 import DOMINIOS

NACE = X._on("GEMV_P7_NACE")
E = {"foto": None, "ultimo_dano": None, "acciones": collections.deque(maxlen=4), "ventana": None, "registra": None, "tick": None, "curioso_sin_camino": 0}


# ── las dos clases ──
def raciones(mundo): return tuple(getattr(mundo, "id_raciones", None) or ("rations",))
def racion(mundo): return raciones(mundo)[0]
def consumibles(mundo): return (X.kit(mundo), racion(mundo))
def cura_cat(mundo, obj):
    it = mundo.items.get(obj) if getattr(mundo, "items", None) else None
    return float(getattr(it, "heal", 0) or 0.0) or (50.0 if obj == X.kit(mundo) else 15.0)
def unidades_de(you, mundo, obj):
    ids = raciones(mundo) if obj != X.kit(mundo) else (obj,)
    return sum(int(s.get("n") or 1) for s in (you.get("pack") or []) if s and s.get("id") in ids)
def contexto_ahora(mundo, pos, tick):
    u = E["ultimo_dano"]; return {"dentro": X.situacion(mundo, pos, tick) == "dentro", "golpeado_48": bool(u is not None and 0 <= tick - u <= 48)}


# ── lo que el cuerpo recuerda de cada cosa ──
def cuaderno():
    c = X.ESTADO["cuaderno"]
    if c is not None and not isinstance(c, CuadernoP23): CuadernoP23.desde(c)
    return c
def vivida(mundo, obj, pos, tick):
    """(creencia vivida del cuerpo por parecido, ignorancia por parecido) del objeto en la situacion de ahora; (None, 1) si no sabe nada."""
    c = cuaderno()
    if c is None or not X.CUADERNO_ON: return None, 1.0
    cre, suma = c.creencia_parecido(obj, contexto_ahora(mundo, pos, tick), E["foto"])
    return (None if cre is None else float(cre["cuerpo"])), 1.0 / (1.0 + suma)
def esperanza(mundo, obj, pos, tick):
    """Lo que el cuerpo sabe de los otros consumibles de la clase: media de sus creencias vividas; nada conocido -> 0."""
    vals = [v for o in consumibles(mundo) if o != obj for v, _ in [vivida(mundo, o, pos, tick)] if v is not None]
    return (sum(max(0.0, v) for v in vals) / len(vals)) if vals else 0.0
def heal_de(mundo, obj, pos, tick):
    v, ign = vivida(mundo, obj, pos, tick); cre = 0.0 if v is None else max(0.0, v)
    return (1.0 - ign) * cre + ign * esperanza(mundo, obj, pos, tick) if X.ESPERANZA_ON else cre
def k_de(mundo, obj, pos, tick): return max(0.0, heal_de(mundo, obj, pos, tick) / cura_cat(mundo, obj))
def k_aprendido(mundo, obj, pos, tick):
    v, _ = vivida(mundo, obj, pos, tick); return 0.0 if v is None else max(0.0, v / cura_cat(mundo, obj))
def pos_tick(obs):
    you = obs.get("you") or {}; return tuple(you.get("pos") or (0, 0)), (E["tick"] or 0)


# ── la ventana de la experiencia, para las dos cosas ──
def _canal_de(you, mundo):
    for e in (you.get("effects") or []):
        if e.get("id") == "channeling" and e.get("item") in consumibles(mundo) + raciones(mundo): return e.get("item") if e.get("item") == X.kit(mundo) else racion(mundo)
    return None
def ventana(self, obs, radio):
    mundo, mem, tick = self.mundo, self.mem, self.tick; you = obs.get("you") or {}; c = cuaderno(); v = E["ventana"]
    if c is None or mundo is None: return
    obj_canal = _canal_de(you, mundo)
    if str((radio or {}).get("elegido") or "").startswith("soltar_") and (v is not None or obj_canal): X.ESTADO["regalo_en_ventana"] = tick
    if v is None:
        if obj_canal:
            d0, como0 = X.dist_hermano(obs, mundo, mem); pos = tuple(you.get("pos") or (0, 0))
            uh = X.ESTADO.get("ultima_heal"); heal_us = uh[1] if (uh and uh[0] == tick - 1) else None
            E["ventana"] = {"objeto": obj_canal, "t0": tick, "contexto": contexto_ahora(mundo, pos, tick), "foto": foto_de_radio(radio) or E["foto"], "acciones": list(E["acciones"]),
                            "hp0": float(you.get("hp") or 0.0), "unidades0": X.unidades(you), "n0": unidades_de(you, mundo, obj_canal), "dist0": d0, "como0": como0, "mal0": X.malestar_ejes(radio),
                            "conocido": 0.0, "fuentes": [], "total": 0.0, "hp_max": float(getattr(mem, "hp_max", None) or 100.0), "techo": False, "heal_imaginado": heal_us}
            if E["registra"]: E["registra"]({"k": "P7_nace_uso", "tick": tick, "objeto": obj_canal, "contexto": E["ventana"]["contexto"], "foto": E["ventana"]["foto"], "hp": you.get("hp"), "heal_imaginado": heal_us,
                                              "creencia_vivida": vivida(mundo, obj_canal, pos, tick)[0], "ignorancia": round(vivida(mundo, obj_canal, pos, tick)[1], 4), "esperanza": round(esperanza(mundo, obj_canal, pos, tick), 3), "acciones": list(E["acciones"])})
        return
    if tick > v["t0"]:
        con, fu = X._dano_conocido(obs, mundo, tick); v["conocido"] += con; v["fuentes"] += fu
        v["total"] += sum(float(d.get("amount") or 0.0) for d in (you.get("damage_taken") or []))
        if float(you.get("hp") or 0.0) >= v["hp_max"]: v["techo"] = True
    if obj_canal == v["objeto"]: return
    obj = v["objeto"]; d1, como1 = X.dist_hermano(obs, mundo, mem); mal1 = X.malestar_ejes(radio)
    rg = X.ESTADO.get("regalo_en_ventana"); regalado = rg is not None and v["t0"] <= rg <= tick; X.ESTADO["regalo_en_ventana"] = None
    completado = unidades_de(you, mundo, obj) < v["n0"]
    efecto = {"cuerpo": (float(you.get("hp") or 0.0) - v["hp0"]) + v["conocido"], "recursos": X.unidades(you) - v["unidades0"], "vinculo": ((d1 - v["dist0"]) if (d1 is not None and v["dist0"] is not None) else 0.0)}
    if not completado: efecto["cuerpo"] = 0.0; efecto["recursos"] = 0.0          # el corte: efecto 0 en cuerpo y en recursos (el dano que lo corta va a su causa)
    importancia = {dom: (mal1.get(dom, 0.0) - v["mal0"].get(dom, 0.0)) for dom in DOMINIOS}
    r = c.apunta_P23(obj, v["contexto"], v["foto"], v["acciones"], efecto, importancia, tick=v["t0"], al_menos=(v["techo"] and completado), corte=not completado) if (X.CUADERNO_ON and not regalado) else None
    h = {"k": "P7_huella", "objeto": obj, "t0": v["t0"], "t_fin": tick, "situacion": "dentro" if v["contexto"]["dentro"] else "fuera", "contexto": v["contexto"], "foto": v["foto"], "hp0": v["hp0"], "hp_fin": you.get("hp"), "hp_max": v["hp_max"],
         "al_menos": bool(v["techo"] and completado), "corte": not completado, "interrumpido": not completado, "regalado": regalado, "dano_total": round(v["total"], 3), "fuentes_conocidas": v["fuentes"],
         "efecto": {k: round(x, 4) for k, x in efecto.items()}, "importancia": {k: round(x, 4) for k, x in importancia.items()}, "intensidad": (r or {}).get("intensidad"), "apuntado": bool(r),
         "creencia_despues": (c.creencia(obj, "dentro" if v["contexto"]["dentro"] else "fuera") if X.CUADERNO_ON else None), "ignorancia_despues": round(c.ignorancia(obj), 4)}
    X.ESTADO["huellas"].append(h)
    if E["registra"]: E["registra"](h)
    E["ventana"] = None


# ── las filas que regalan, para las dos cosas ──
def regalo_nace(obs, mundo, mem, tick, F, filas0):
    vis = obs.get("visible") or {}; items = vis.get("items") or []; pos, _ = pos_tick(obs)
    if not any(a.get("slot") == mundo.teammate_slot for a in (vis.get("agents") or [])): return F
    clases = {X.kit(mundo): X.kit(mundo), **{r: racion(mundo) for r in raciones(mundo)}}
    presentes = {clases[it.get("id")] for it in items if it.get("id") in clases}
    if not presentes: return F
    ks = {o: k_aprendido(mundo, o, pos, tick) for o in presentes}        # el regalo mira LO APRENDIDO (P7-8), sin esperanza
    k = max(ks.values())
    if k >= 1.0: return F
    ob2 = dict(obs); ob2["visible"] = dict(vis, items=[it for it in items if it.get("id") not in clases])
    F_sin = filas0(ob2, mundo, mem, tick); cambio = {}
    for fila in set(F) | set(F_sin):
        if fila.startswith("_") or not isinstance(F.get(fila, 0.0), (int, float)) or not isinstance(F_sin.get(fila, 0.0), (int, float)): continue
        a, b = float(F.get(fila) or 0.0), float(F_sin.get(fila) or 0.0)
        if a != b: F[fila] = b + (a - b) * k; cambio[fila] = (round(a, 5), round(b, 5), round(F[fila], 5))
    if cambio: F["_regalo_aprendido"] = {"k": round(k, 4), "clases": sorted(presentes), "filas": cambio}
    return F


# ── la curiosidad, para las dos cosas ──
def alivio_clase(obs, mundo, obj):
    you = obs.get("you") or {}
    if obj == X.kit(mundo) and you.get("_cura_en_curso"): return 0.0
    return X.ALIVIO_ZURRON if unidades_de(you, mundo, obj) >= 1 else 1.0
def cautela_de(obs, mundo, tick):
    """[P7-26, variante de banco] La cautela por distancias (propuesta de la mesa para medir): 1 sin rivales a 8 casillas o menos; baja linealmente hasta 0 con un
    rival a 2; 0 fuera del circulo o con la vida por debajo de 30. Solo entra si E["cautela"] es verdadero (banco); en el campo la curiosidad sigue con la calma."""
    you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0))
    if float(you.get("hp") or 0.0) < 30.0 or X.situacion(mundo, pos, tick or 0) == "fuera": return 0.0
    riv = [a for a in ((obs.get("visible") or {}).get("agents") or []) if a.get("team") != getattr(mundo, "team", None) and a.get("slot") != mundo.teammate_slot and a.get("pos")]
    d = min((max(abs(a["pos"][0] - pos[0]), abs(a["pos"][1] - pos[1])) for a in riv), default=None)
    if d is None or d > 8: return 1.0
    return max(0.0, min(1.0, (d - 2) / 6.0))
def curiosidad_M(obs, mundo, F):
    calma = cautela_de(obs, mundo, E.get("tick")) if E.get("cautela") else X.calma_de(F); c = cuaderno(); partes = []
    for o in consumibles(mundo):
        ign = 1.0 if (c is None or not X.CUADERNO_ON) else float(c.ignorancia(o)); partes.append(ign * alivio_clase(obs, mundo, o))
    m = sum(partes) / len(partes); ign_m = m
    return X.ACOPIO_M0 * float(E.get("escala_curiosidad") or 1.0) * calma * m, calma, ign_m, 1.0    # escala_curiosidad: 1 en el campo; solo el banco de P7-25 la cambia
def clase_curiosa(obs, mundo):
    """La clase con mayor ignorancia x alivio (la que mas llama), y ese valor."""
    c = cuaderno(); mejor = None
    for o in consumibles(mundo):
        ign = 1.0 if (c is None or not X.CUADERNO_ON) else float(c.ignorancia(o)); v = ign * alivio_clase(obs, mundo, o)
        if mejor is None or v > mejor[1]: mejor = (o, v)
    return mejor


# ── el pedido, solo por lo aprendido ──
def pide_nace(obs, mundo, mem, tick):
    you = obs.get("you") or {}; kid = X.kit(mundo); a_bordo = X.kits_en(you, mundo); pos = tuple(you.get("pos") or (0, 0))
    a_la_vista = any(it.get("id") == kid for it in ((obs.get("visible") or {}).get("items") or []))
    hueco = J.cabe(you, mundo); k = k_de(mundo, kid, pos, tick) if (a_bordo == 0 and hueco) else 0.0
    sitio = bool(a_bordo == 0 and not J.ESTADO["pedia"] and not a_la_vista and not hueco and k_de(mundo, kid, pos, tick) > 0.0 and J.haria_sitio(obs, mundo, mem, tick))
    podria = (hueco and k > 0.0) or sitio
    si = a_bordo == 0 and (J.ESTADO["pedia"] or (podria and not a_la_vista))
    return si, {"a_bordo": a_bordo, "a_la_vista": a_la_vista, "promesa": round(k * cura_cat(mundo, kid), 5), "k_aprendido": round(k, 4), "hueco": hueco, "haria_sitio": sitio}


# ── los enganches ──
def aplica(clase, registra=None):
    E["registra"] = registra
    if not (NACE and X.ON and not X.SABE): return {"NACE": False}
    _arr = X.arranca
    def arranca(criatura, ruta, registra_=None):
        c = _arr(criatura, ruta, registra_); return cuaderno()
    X.arranca = arranca
    def heal_kit(mundo, pos, tick):
        h = heal_de(mundo, X.kit(mundo), pos, tick); return h
    X.heal_imaginado = heal_kit
    X.k_ganas = lambda mundo: k_de(mundo, X.kit(mundo), *E.get("pos_tick", ((0, 0), 0)))
    X.k_creencia = lambda mundo: k_aprendido(mundo, X.kit(mundo), *E.get("pos_tick", ((0, 0), 0)))
    X.w_target = lambda k, mundo: 1.0 + k + k_de(mundo, racion(mundo), *E.get("pos_tick", ((0, 0), 0)))
    X.regalo_aprendido = regalo_nace
    X.curiosidad_M = curiosidad_M
    X.ventana = ventana
    J.pide2 = pide_nace
    _oc = D.candidatos; _ow = A.riqueza_W; _of = A.filas; _op = D._promesa; _od = clase.decidir
    def _cands(obs, mundo, mem, tick, bloqueos=None):
        you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); E["pos_tick"] = (pos, tick)
        out = []; hay_curioso = None
        for n, r in _oc(obs, mundo, mem, tick, bloqueos):
            if n == "usar_racion": r = dict(r, heal=heal_de(mundo, racion(mundo), pos, tick))
            if n == "ir_curioso": hay_curioso = r
            out.append((n, r))
        # la curiosidad abre camino hacia la clase que mas llama (botiquin o racion); la de P7-7 solo iba al botiquin.
        # [P7-24, paso 0: arreglo mas pequeno] (1) NO VA A LO INALCANZABLE: el destino tiene que tener camino segun la geodesica del propio cuerpo
        # (`D.campo_geodesico`; si no lo hay, el cuerpo cae a la linea recta y se queda contra un muro: dia 1 del humo, asiento 11, 4.931 tics); (2) en empate
        # entre clases (las dos igual de desconocidas) va al objeto mas cercano POR CAMINO, no al botiquin por defecto.
        if X.NOVEDAD_ON:
            c = cuaderno(); llamadas = {}
            for o in consumibles(mundo):
                ign = 1.0 if (c is None or not X.CUADERNO_ON) else float(c.ignorancia(o)); llamadas[o] = ign * alivio_clase(obs, mundo, o)
            top = max(llamadas.values()) if llamadas else 0.0
            clases = [o for o, v in llamadas.items() if v >= top - 1e-9 and v > 0 and unidades_de(you, mundo, o) == 0 and D._pack_con(list(you.get("pack") or []), o, 1, mundo) != list(you.get("pack") or [])]
            out = [(n, r) for n, r in out if n != "ir_curioso"]
            if clases:
                ids = {X.kit(mundo)} | set(raciones(mundo)); ids = {i for i in ids if (X.kit(mundo) if i == X.kit(mundo) else racion(mundo)) in clases}
                ced = getattr(mem, "cedidos", {}); vis = obs.get("visible") or {}
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
                    if not any(n == "ir_objeto" and tuple(r.get("destino") or ()) == dest for n, r in out):
                        cuerpos = frozenset(tuple(a.get("pos") or ()) for a in (vis.get("agents") or []) if a.get("pos"))
                        out.append(("ir_curioso", {"tipo": "ir", "destino": dest, "cuerpos": cuerpos, "recoger": sitios[dest]}))
                E["curioso_sin_camino"] = len(sitios) - len(pasos)
        return out
    def _riqueza(you, mundo):
        W, d = _ow(you, mundo); d2 = dict(d); pos, tick = E.get("pos_tick", ((0, 0), 0))
        d2["raciones"] = float(d.get("raciones") or 0.0) * k_de(mundo, racion(mundo), pos, tick)
        return sum(d2.values()), d2
    def _filas(obs, mundo, mem, tick):
        F = _of(obs, mundo, mem, tick); pos = tuple((obs.get("you") or {}).get("pos") or (0, 0)); k = k_de(mundo, X.kit(mundo), pos, tick)
        for fila in ("S-PROVISION", "R-HERMANO-FALTA"):
            if isinstance(F.get(fila), (int, float)) and F[fila]: F[fila] = float(F[fila]) * k
        F["_nace"] = {"k_botiquin": round(k, 4), "k_racion": round(k_de(mundo, racion(mundo), pos, tick), 4)}
        return F
    def _promesa(obs, mundo, mem, tick, item_id):
        base = _op(obs, mundo, mem, tick, item_id)
        if not X.NOVEDAD_ON or item_id not in raciones(mundo): return base
        you = obs.get("you") or {}
        if unidades_de(you, mundo, racion(mundo)) >= 1 or D._pack_con(list(you.get("pack") or []), item_id, 1, mundo) == list(you.get("pack") or []): return base
        cc = clase_curiosa(obs, mundo)
        if not cc or cc[0] != racion(mundo): return base
        t, F = X.ESTADO["calma_cache"]
        if t != tick: F = A.filas(obs, mundo, mem, tick); X.ESTADO["calma_cache"] = (tick, F)
        M, _, _, _ = curiosidad_M(obs, mundo, F); return base + M * (1.0 - X.ALIVIO_ZURRON)
    def decidir(self, obs, _d=_od):
        you = obs.get("you") or {}; E["tick"] = getattr(self, "tick", None); E["pos_tick"] = (tuple(you.get("pos") or (0, 0)), E["tick"] or 0)
        if any(float(d.get("amount") or 0) > 0 for d in (you.get("damage_taken") or [])): E["ultimo_dano"] = self.tick
        accion, radio = _d(self, obs)
        if radio is not None:
            E["acciones"].append(str(radio.get("elegido") or "")); f = foto_de_radio(radio)
            if f: E["foto"] = f
        return accion, radio
    D.candidatos, A.riqueza_W, A.filas, D._promesa, clase.decidir = _cands, _riqueza, _filas, _promesa, decidir
    return {"NACE": True, "borra": ["heal usar_botiquin", "heal usar_racion", "R-ACOPIO (k)", "W botiquin (k)", "W raciones (k)", "W_TARGET 1+k+k", "S-PROVISION (k)", "R-HERMANO-FALTA (k)", "medicina en el suelo: botiquin y racion (k aprendido)", "pedido por lo aprendido", "esperanza desde lo aprendido de la clase"]}
