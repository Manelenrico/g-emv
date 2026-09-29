"""[P5-8B] Los humos del brazo K, donde vive la regla.

  (a) APAGADO: 200 tics de escena grabada, decision a decision IDENTICA.
  (b) EL CUERPO PISA EL CAMINO: con una forma aceptada, las casillas que el
      cuerpo visita salen del camino de la forma.
  (c) EL VETO DURO DISPARA al aparecer un armado que cubre el camino restante.
"""
from __future__ import annotations
import importlib, json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import humo_cortex as HC                                   # noqa: E402
FALLOS = []


def _recarga(**env):
    for k, v in env.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    for m in ("curiosidad", "curiosidad_forma", "alma.policy_forma"):
        sys.modules.pop(m, None)
    import alma
    if hasattr(alma, "policy_forma"):
        delattr(alma, "policy_forma")
    return importlib.import_module("alma.policy_forma")


def _corre(**env):
    import asyncio
    PF = _recarga(**env)
    from alma import policy_cortex as PC
    from alma import humo_forma as HF
    d = json.load(open(os.path.join(AQUI, "humo_200tics.json")))
    pc = dict(d["player_config"]); pc["type"] = "player_config"
    pc["arena"] = {"size": d["static_map"].get("size") or 48,
                   "static_map": list(d["static_map"]["filas"]),
                   "legend": dict(d["static_map"].get("legend") or HC.LEY),
                   "pedestals": d["static_map"].get("pedestals") or []}
    pc["items"] = list(d["catalogo"]["items"])
    pc["stats"] = {"budget": 20, "min": 1, "max": 10, "default": [5, 5, 5, 5]}
    msgs = [json.dumps(pc)] + [json.dumps(HF._obs(r)) for r in d["ticks"]]
    msgs.append(json.dumps({"type": "final", "placement": 9, "kills": 0,
                            "score": 0.0, "reason": "humo",
                            "match_ticks": d["ticks"][-1]["tick"]}))

    class WS:
        def __aiter__(self):
            self._i = 0; return self

        async def __anext__(self):
            if self._i >= len(msgs):
                raise StopAsyncIteration
            m = msgs[self._i]; self._i += 1; return m

        async def send(self, s):
            pass
    alma = PF.AlmaForma()
    i0 = len(PC._DIARIO)
    asyncio.run(PC.decisor(WS(), alma))
    out = []
    for ln in PC._DIARIO[i0:]:
        try:
            out.append(json.loads(ln))
        except Exception:
            pass
    return PF, out, alma


OFF = dict(GEMV_CURIOSIDAD=None, GEMV_CURIOSIDAD_FORMA=None, GEMV_FORMA=None,
           GEMV_HILO_FORMA=None, GEMV_CONSEJERO_FORMA=None,
           GEMV_FORMAS_AZAR=None)
ON = dict(OFF, GEMV_FORMA="1", GEMV_CURIOSIDAD_FORMA="1",
          GEMV_CURIOSIDAD_CONSIGNA="0.5")


def a_apagado_identico():
    _p0, d0, _a0 = _corre(**OFF)
    _p1, d1, _a1 = _corre(**dict(OFF, GEMV_CURIOSIDAD_FORMA="0"))
    t0 = [r for r in d0 if r.get("k") == "tick" and r.get("RADIOGRAFIA")]
    t1 = [r for r in d1 if r.get("k") == "tick" and r.get("RADIOGRAFIA")]
    ig = sum(1 for a, b in zip(t0, t1)
             if a["RADIOGRAFIA"]["elegido"] == b["RADIOGRAFIA"]["elegido"]
             and a["RADIOGRAFIA"].get("d_ahora") == b["RADIOGRAFIA"].get("d_ahora"))
    cur = [r for r in d1 if r.get("k") == "cur_forma_tic"]
    if ig != len(t0) or cur:
        FALLOS.append(f"(a) apagado NO identico: {ig}/{len(t0)}, {len(cur)} registros")
    print(f"  (a) APAGADO identico: {ig}/{len(t0)} decisiones · "
          f"{len(cur)} registros de curiosidad-forma")


def b_y_c_el_cuerpo_pisa_y_el_veto():
    PF, d, alma = _corre(**ON)
    prop = [r for r in d if r.get("k") == "forma_propuesta"
            and r.get("origen") == "curiosidad"]
    acep = [r for r in d if r.get("k") == "forma_aceptada"]
    caid = [r for r in d if r.get("k") == "forma_caida"]
    tic = [r for r in d if r.get("k") == "cur_forma_tic"]
    tks = {r["tick"]: r for r in d if r.get("k") == "tick"}
    print(f"  (b) el brazo K vive: {len(prop)} formas nacidas · "
          f"{len(acep)} aceptadas · {len(caid)} caidas · "
          f"{len(tic)} registros `cur_forma_tic`")
    if not prop:
        FALLOS.append("(b) el brazo K NO genero ni una forma en 200 tics")
        return
    # UN MECANISMO QUE NACE Y NUNCA PASA LA PUERTA ES UN MECANISMO MUERTO.
    # En seco pasaba el 37 %; si aqui pasa CERO, algo esta mal cableado y el
    # humo tiene que caerse (la leccion de P5-7A).
    if not acep:
        FALLOS.append(f"(b) {len(prop)} formas nacidas y CERO aceptadas: "
                      f"en seco pasaba el 37 %")
    if not tic:
        FALLOS.append("(b) no hay registro `cur_forma_tic`: las cuarenta no se leerian")
    # ¿el cuerpo pisa el camino? se comprueba contra el DESTINO: mientras la
    # forma esta activa, la distancia al destino no debe crecer.
    for a in acep:
        fid = a.get("id")
        act = [r for r in tic if r.get("activa") == fid and r.get("destino")]
        if len(act) < 3:
            continue
        dest = tuple(act[0]["destino"])
        ds = []
        for r in act:
            tk = tks.get(r["tick"])
            if tk and tk.get("pos"):
                p = tuple(tk["pos"])
                ds.append(max(abs(p[0] - dest[0]), abs(p[1] - dest[1])))
        if len(ds) >= 3:
            print(f"      forma {fid} -> destino {dest}: distancia "
                  f"{ds[0]} -> {ds[-1]} en {len(ds)} tics")
            if ds[-1] > ds[0]:
                FALLOS.append(f"(b) con la forma {fid} activa el cuerpo se ALEJO "
                              f"del destino ({ds[0]} -> {ds[-1]})")
            break
    # (c) el veto duro: se comprueba la FUNCION donde vive, con una escena
    import curiosidad_forma as CFM
    mundo = alma.mundo
    dest, cam = (24, 20), [(24, 24), (24, 23), (24, 22), (24, 21), (24, 20)]
    r_sin = {"ve_agentes": []}
    r_con = {"ve_agentes": [{"slot": 3, "pos": [24, 21], "hand": "sword",
                             "hp_band": "healthy"}]}
    v0 = CFM.abandona_por_peligro(dest, cam, r_sin, mundo, 11)
    v1 = CFM.abandona_por_peligro(dest, cam, r_con, mundo, 11)
    print(f"  (c) VETO DURO: sin armado {v0} · con un armado sobre el camino {v1}")
    if v0 or not v1:
        FALLOS.append(f"(c) el veto duro no discrimina: sin={v0} con={v1}")


def g_el_compromiso():
    """[P5-8H] (a) obedece con piernas listas · (b)(c) las rupturas."""
    PF, d, alma = _corre(**ON)
    comp = [r for r in d if r.get("k") == "compromiso"]
    ob = [r for r in comp if r.get("estado") == "obedece"]
    ro = [r for r in comp if r.get("estado") == "rompe"]
    en = [r for r in comp if r.get("estado") == "enfriamiento"]
    import collections
    print(f"  (g) compromiso: {len(comp)} registros · obedece {len(ob)} · "
          f"rompe {len(ro)} · enfriamiento {len(en)}")
    if ro:
        print(f"      causas: {dict(collections.Counter(r['causa'][:28] for r in ro))}")
    # (a) al obedecer, la accion tiene que ser la de la forma AUNQUE el
    #     decisor prefiriese otra
    distinto = [r for r in ob if r.get("habria_ganado") != r.get("paso")]
    print(f"      (a) obedece con un ganador DISTINTO al paso de la forma: "
          f"{len(distinto)}/{len(ob)}")
    if ob and not distinto:
        print("          (aviso) en esta escena el decisor ya prefería la forma")
    if not comp:
        FALLOS.append("(g) el compromiso no dejo ni un registro")
    # (b) y (c): la logica de la ruptura (e), sobre escenas construidas
    import curiosidad_forma as CFM
    mundo = alma.mundo
    class _F: id = 99
    alma.k_camino[99] = [(24, 24)]
    alma.vivas = []
    def _obs(agentes, mri=0):
        return {"you": {"pos": [24, 24], "hp": 100, "damage_taken": [],
                        "move_ready_in": mri, "pack": [None, None],
                        "hand": {"id": "none"}, "body": None},
                "visible": {"agents": agentes, "items": []}}
    fv = _F(); fv.origen = "curiosidad"; fv.W_nace = None
    # (b) armado acercandose a 5. OJO: con un ARCO, 5 casillas YA es «a
    # tiro» y dispara (a) — la escena tiene que usar un arma CORTA para
    # aislar (e). Lo cazo el humo la primera vez.
    alma.k_rival_dist = {3: 6}
    c1, _d1 = alma._rupturas(_obs([{"slot": 3, "pos": [24, 19],
                                    "hand": "sword", "hp_band": "healthy"}]), fv)
    print(f"      (b) armado CORTO a 5 acercandose (antes 6): ruptura = {c1}")
    if not c1 or "e)" not in c1:
        FALLOS.append(f"(b) no rompio por (e): {c1}")
    # (c) pacifico SIN arma a 4
    alma.k_rival_dist = {4: 5}
    c2, _d2 = alma._rupturas(_obs([{"slot": 4, "pos": [24, 20],
                                    "hand": "none", "hp_band": "healthy"}]), fv)
    print(f"      (c) pacifico sin arma a 4: ruptura = {c2} (debe ser None)")
    if c2 is not None:
        FALLOS.append(f"(c) rompio con un pacifico a 4: {c2}")


def f_el_atasco_en_pasos():
    """[P5-8E] El atasco se mide en PASOS del mundo, no en tics constantes.

    (f1) un cuerpo que avanza una casilla cada 11 tics NO se atasca.
    (f2) un cuerpo que no se mueve en 33 tics SI se atasca.
    Se prueba la aritmetica del plazo contra el paso leido del mundo.
    """
    PF = _recarga(**ON)
    paso = 11                      # 16 - speed(5), el del mundo
    plazo = PF.CUR_ATASCO_PASOS * paso
    print(f"  (f) atasco: {PF.CUR_ATASCO_PASOS} pasos x {paso} tics/casilla "
          f"= plazo {plazo} tics (antes: 25 constantes)")
    if plazo <= paso:
        FALLOS.append(f"(f) el plazo {plazo} no da ni para un paso")
    # (f1) avanzando una casilla cada paso, el «mejor» se renueva cada 11 tics
    mejor, t_mejor, atasca = 6, 0, False
    for t in range(1, 80):
        d = 6 - (t // paso)        # una casilla por paso
        if d < mejor:
            mejor, t_mejor = d, t
        elif t - t_mejor >= plazo:
            atasca = True
            break
    print(f"      (f1) avanzando 1 casilla cada {paso} tics: "
          f"se atasca = {atasca} (debe ser False)")
    if atasca:
        FALLOS.append("(f1) un cuerpo que avanza se atasca")
    # (f2) quieto
    mejor, t_mejor, atasca = 6, 0, False
    for t in range(1, 80):
        d = 6
        if d < mejor:
            mejor, t_mejor = d, t
        elif t - t_mejor >= plazo:
            atasca = True
            break
    print(f"      (f2) quieto: se atasca = {atasca} al tic {t} "
          f"(debe ser True, y a los {plazo})")
    if not atasca:
        FALLOS.append("(f2) un cuerpo quieto NO se atasca")


def e_el_reloj_y_el_alivio():
    """[P5-8D] (a) el reloj honesto · (b) completada por alivio."""
    PF, d, alma = _corre(**ON)
    from alma import forma_viva as FV
    acep = {r["id"]: r["tick"] for r in d if r.get("k") == "forma_aceptada"}
    fin = [r for r in d if r.get("k") == "forma_caida"]
    import collections
    mot = collections.Counter(str(r.get("motivo") or "")[:26] for r in fin)
    vidas = [(r["tick"] - acep[r["id"]]) for r in fin if r.get("id") in acep]
    print(f"  (e) fin de las formas: {dict(mot)}")
    if vidas:
        print(f"      duracion: min {min(vidas)} · mediana {st.median(vidas)} "
              f"· max {max(vidas)} (CADA_REEVALUA = {FV.CADA_REEVALUA})")
    # (a) EL RELOJ: ninguna puede morir por «deja de ganar» ANTES de su llegada
    prop = {r["id"]: r for r in d if r.get("k") == "forma_propuesta"
            and r.get("origen") == "curiosidad"}
    pronto = []
    for r in fin:
        if "deja de ganar" not in str(r.get("motivo") or ""):
            continue
        p0 = prop.get(r.get("id"))
        if not p0:
            continue
        llega = acep.get(r["id"], 0) + p0.get("dist", 0) * 11
        if r["tick"] < llega:
            pronto.append((r["id"], r["tick"], llega))
    print(f"      (a) muertes por «deja de ganar» ANTES de la llegada "
          f"proyectada: {len(pronto)} (debe ser 0)")
    if pronto:
        FALLOS.append(f"(a) el reloj no se respeta: {pronto[:3]}")
    # (b) alivio
    ali = sum(1 for r in fin if "alivio" in str(r.get("motivo") or ""))
    print(f"      (b) completadas POR ALIVIO: {ali}")
    if vidas and min(vidas) == max(vidas) == FV.CADA_REEVALUA:
        FALLOS.append("(e) TODAS mueren en su primer examen otra vez")


def d_la_reevaluacion():
    """[P5-8B bis] La puerta juzga y RE-JUZGA con la misma regla.

    (d1) alguna forma aceptada tiene que SOBREVIVIR a su primera
         reevaluacion: si TODAS mueren exactamente a `CADA_REEVALUA`, el
         renglon no esta entrando en la reevaluacion y el humo se cae.
    (d2) y tiene que haber formas que SI mueran por «deja de ganar»: una
         puerta que nunca tumba nada tampoco es una puerta.
    """
    PF, d, alma = _corre(**ON)
    from alma import forma_viva as FV
    acep = {r["id"]: r["tick"] for r in d if r.get("k") == "forma_aceptada"}
    caid = {r["id"]: (r["tick"], str(r.get("motivo") or ""))
            for r in d if r.get("k") == "forma_caida"}
    vidas = [(caid[i][0] - acep[i], caid[i][1]) for i in acep if i in caid]
    if not vidas:
        print("  (d) sin formas con caida en 200 tics: no se puede juzgar")
        return
    largos = [v for v, _m in vidas]
    import collections
    mot = collections.Counter(m[:28] for _v, m in vidas)
    print(f"  (d) duracion de las formas: min {min(largos)} · "
          f"mediana {st.median(largos)} · max {max(largos)} "
          f"(CADA_REEVALUA = {FV.CADA_REEVALUA}) · n={len(largos)}")
    print(f"      causas: {dict(mot)}")
    if min(largos) == max(largos) == FV.CADA_REEVALUA:
        FALLOS.append(f"(d) TODAS las formas mueren exactamente a "
                      f"{FV.CADA_REEVALUA} tics: el renglon NO entra en la "
                      f"reevaluacion")
    sobreviven = sum(1 for v in largos if v > FV.CADA_REEVALUA)
    print(f"      sobreviven a la primera reevaluacion: "
          f"{sobreviven}/{len(largos)}")
    if not sobreviven:
        print("      (nota) con R2 el primer examen ya no cae en el tic 25: "
              "lo que manda es (e)")
    if not any("gan" in m for _v, m in vidas):
        print("      AVISO: ninguna murio por «deja de ganar» en esta escena")


def h_el_margen_por_origen():
    """[P5-8K] La puerta cobra 0,02 al cuerpo y su margen de siempre al consejero.

    Se prueba DONDE VIVE LA REGLA: `_margen_de` en la politica, y
    `forma.juzga_margen`, que es quien compara ventaja contra margen.
    """
    PF = _recarga(GEMV_CURIOSIDAD_FORMA="1", GEMV_FORMA="1")
    import forma as F
    from alma import confianza_viva as CV

    class _FV:                       # una forma de mentira, solo el origen
        def __init__(self, o): self.origen = o

    class _Conf:
        C = 0.30
        def margen(self): return CV.MARGEN_BASE + CV.MARGEN_RANGO * (1.0 - self.C)

    alma = PF.AlmaForma.__new__(PF.AlmaForma)      # sin arrancar el mundo
    alma.conf = _Conf()
    m_cur = alma._margen_de(_FV("curiosidad"))
    m_con = alma._margen_de(_FV("consejero"))
    print(f"  (h) margen por origen: curiosidad {m_cur:.4f} · "
          f"consejero (C=0,30) {m_con:.4f}")
    if abs(m_cur - CV.MARGEN_BASE) > 1e-12:
        FALLOS.append(f"(h) el margen de curiosidad no es MARGEN_BASE: {m_cur}")
    if abs(m_con - 0.062) > 1e-9:
        FALLOS.append(f"(h) el margen del consejero CAMBIO: {m_con} != 0,062")
    if m_cur >= m_con:
        FALLOS.append("(h) el margen de curiosidad no es MENOR que el del consejero")

    # ── la puerta de verdad: dos curvas que dan la ventaja pedida ──
    def _curvas(ventaja):
        """(c_forma, c_solo) cuyo `area` vale `ventaja`. El area de `forma.py`
        pondera por 0,5**(dt/MEDIA_VIDA); con un solo punto en dt=0 el peso es
        1 y el area es la diferencia de `d`."""
        t0 = 100
        cf = [{"tic": t0, "d": 1.0 - ventaja, "vida": 100.0}]
        cs = [{"tic": t0, "d": 1.0, "vida": 100.0}]
        return cf, cs, t0

    casos = [("curiosidad", 0.045, "ok"), ("curiosidad", 0.015, "area"),
             ("consejero", 0.045, "area")]
    for origen, ven, espera in casos:
        cf, cs, t0 = _curvas(ven)
        mg = alma._margen_de(_FV(origen))
        ver, ar, _ = F.juzga_margen(cf, cs, t0, margen=mg)
        ok = (ver == espera)
        print(f"      {origen:11s} ventaja {ven:.3f} contra margen {mg:.4f}"
              f" -> {ver!r} (area {ar:+.5f}) {'OK' if ok else 'MAL'}")
        if not ok:
            FALLOS.append(f"(h) {origen} con ventaja {ven}: {ver}, se esperaba {espera}")
        if abs(ar - ven) > 1e-9:
            FALLOS.append(f"(h) el area de la prueba no es la ventaja pedida: {ar} != {ven}")


def i_el_rodeo():
    """[P5-8M] (a) rodea y sigue · (b) sin rodeo · (c) el que se acerca rompe."""
    PF, d, alma = _corre(**ON)
    import curiosidad_forma as CFM
    import forma_viva as FV
    mundo = alma.mundo
    herm = mundo.teammate_slot
    print(f"  (i) rodeo: COLCHON_RODEO={CFM.COLCHON_RODEO} · "
          f"TOPE_RODEO={CFM.TOPE_RODEO} · sombra del nacimiento intacta")

    def escena(lancero_pos, dest, cam, k_rival_dist, hand="spear"):
        """Monta UNA forma viva con su camino y llama a `_abandonos_K`."""
        fv = FV.FormaViva(99, [{"destino": list(dest), "intencion": "ver",
                                "esperar": 0}], alma.tick, origen="curiosidad")
        fv.estado = "aceptada"
        alma.vivas = [fv]
        alma.k_camino = {fv.id: list(cam)}
        alma.k_dist_min = {fv.id: (99, alma.tick)}
        alma.k_rival_dist = dict(k_rival_dist)
        obs = {"you": {"pos": list(cam[0]), "hp": 100, "hand": {"id": "none"},
                       "pack": [], "effects": [], "move_ready_in": 0,
                       "damage_taken": []},
               "visible": {"agents": [{"slot": 3, "team": "B",
                                       "pos": list(lancero_pos),
                                       "hand": hand, "hp_band": "healthy"}],
                           "items": [], "projectiles": []},
               "tick": alma.tick}
        alma._abandonos_K(obs)
        vive = any(x.id == fv.id for x in alma.vivas)
        return fv, vive, list(alma.k_camino.get(fv.id) or [])

    # el alcance de la lanza, LEIDO del mundo
    rg = CFM.C._alcance(mundo, "spear")
    # camino recto de 8 casillas hacia el norte desde (24,24)
    cam = [(24, 24 - k) for k in range(9)]
    dest = cam[-1]
    # (a) LANCERO QUIETO que toca el camino: k_rival_dist con la MISMA
    #     distancia de ahora -> no se acerca
    lanc = (22, 16)          # a OCHO casillas del cuerpo, como pide el encargo
    dq = max(abs(24 - lanc[0]), abs(24 - lanc[1]))
    toca = any(max(abs(c[0]-lanc[0]), abs(c[1]-lanc[1])) <= rg for c in cam)
    fv, vive, cam2 = escena(lanc, dest, cam, {3: dq})
    rod = getattr(fv, "rodeos", 0)
    print(f"      (a) lancero QUIETO en {lanc} (alcance {rg:.0f}, a {dq} del "
          f"cuerpo, toca el camino={toca}): vive={vive} rodeos={rod} "
          f"largo {len(cam)-1} -> {len(cam2)-1} · desvio {getattr(fv,'desvio',None)}")
    if not toca:
        FALLOS.append("(a) la escena esta mal: el lancero NO toca el camino")
    if not vive or rod != 1:
        FALLOS.append(f"(a) con un armado QUIETO la forma deberia RODEAR y seguir: "
                      f"vive={vive} rodeos={rod}")
    if vive and getattr(fv, "desvio", None) is None:
        FALLOS.append("(a) rodea pero no pone `desvio`: el rodeo seria cosmetico")
    if vive and cam2 == list(cam):
        FALLOS.append("(a) rodea pero el camino no ha cambiado")

    # (b) MISMO lancero, pero pegado al destino: no hay vuelta
    lanc2 = (24, 17)
    fv2, vive2, _ = escena(lanc2, dest, cam, {3: 7})
    mot = getattr(fv2, "motivo_caida", None)
    print(f"      (b) lancero pegado al destino {lanc2}: vive={vive2} · "
          f"motivo {mot!r}")
    if vive2 or not str(mot or "").startswith("sin rodeo"):
        FALLOS.append(f"(b) deberia abandonar con «sin rodeo»: vive={vive2} mot={mot!r}")

    # (c) el que SE ACERCA sigue matando la forma (veto duro de siempre)
    fv3, vive3, _ = escena(lanc, dest, cam, {3: dq + 1})     # antes mas lejos
    mot3 = getattr(fv3, "motivo_caida", None)
    print(f"      (c) el MISMO lancero ACERCANDOSE (antes {dq+1}, ahora {dq}): "
          f"vive={vive3} · motivo {mot3!r}")
    if vive3 or not str(mot3 or "").startswith("veto duro"):
        FALLOS.append(f"(c) un armado que se acerca debe romper: vive={vive3} mot={mot3!r}")


if __name__ == "__main__":
    import hashlib
    print("== HUMOS DEL BRAZO K (P5-8B · margen P5-8K · rodeo P5-8M) ==")
    for f in ("curiosidad_forma.py", "policy_forma.py"):
        pth = os.path.join(AQUI, f)
        if os.path.exists(pth):
            print(f"  md5 {f}: "
                  f"{hashlib.md5(open(pth,'rb').read()).hexdigest()}")
    a_apagado_identico()
    b_y_c_el_cuerpo_pisa_y_el_veto()
    d_la_reevaluacion()
    e_el_reloj_y_el_alivio()
    f_el_atasco_en_pasos()
    g_el_compromiso()
    h_el_margen_por_origen()
    i_el_rodeo()
    if FALLOS:
        print("\nFALLOS:")
        for x in FALLOS:
            print("  ·", x)
        sys.exit(1)
    print("\nLOS HUMOS DEL BRAZO K OK")
