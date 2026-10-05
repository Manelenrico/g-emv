"""[P6-20 · A] EL VETO CON ALERTA Y PRIMER GOLPE, Y LA CUENTA JUSTA DEL ABANDONO.
SOLO LECTURA de las 40 vidas de A6 (P618_t1), de una en una. Los diarios llevan los
planes (`forma_aceptada`), los tics de compromiso6b (`compromiso6`: sujeta / obedece /
enfriamiento / rompe con causa / cumplida) y las caidas (`forma_caida` con motivo).
Los vetos alternativos se cuentan SOBRE LO GRABADO (contrafactual de recuento: en cada
tic en que el veto grabado rompio, que habria hecho cada veto; el cuerpo grabado actuo
bajo V0, asi que las consecuencias son cotas, declaradas).

    python3 mide_veto_P6_20.py            -> P6_20_banco.json

Definiciones (declaradas):
  · plan vivo: de `forma_aceptada` a `forma_caida` / `cumplida` / muerte / siguiente aviso.
    Ambito «fase 5» (el de P6-18: planes nacidos entre el aviso 5 y el 6 en vidas vivas en
    el aviso 5) y ambito «todos» (el de P6-19: los 309 planes / 70 caidas).
  · rivales: vistos (`ve_agentes`) + contados (parte E2 del hermano, edad <= CADUCIDAD_RIVAL,
    regla de `oyente2.inyecta`); arma = `hand` / `arma` del parte; «armado» = alcance del
    catalogo > 0 (la mano vacia NO cuenta: ampliacion de Manel).
  · «ver el arma» = las rupturas grabadas «a) veto vital: armado a tiro» y «e) armado a
    menos de 6 y acercandose»; «e) rival a 2 o menos» (que solo salta cuando a) no salto:
    rival sin alcance) y «d) vida / carencia» NO cambian con V1-V3.
  · desviado = desde un tic con registro `rompe` hasta que el cuerpo vuelve a estar
    dentro (a salvo): incluye el `enfriamiento` que sigue a la ruptura y el `obedece` de
    la vuelta (el fuego de la vuelta es consecuencia de la ruptura); siguiendo = lo demas:
    `sujeta`, libre dentro, y el `obedece`/`enfriamiento` del tramo inicial de ir (el
    cuerpo anda hacia el circulo por el plan: es coste del plan, no desviacion).
    Episodio de desviacion = racha de tics desviados; su causa = la del primer `rompe`.
  · dano esperado dentro = suma de la tabla arma x distancia de P6-19 (`tabla_puerta6g`)
    sobre los rivales del tic, a la casilla del cuerpo; fuego de fuera = dps de la fase / 24.
  · V0 = lo grabado. V1 = en un tic de «ver el arma», rompe solo si esperado > fuego.
    V2 (Manel) = ver el arma no rompe; tras un golpe de rival con el plan vivo, SUSPENSION de
    N = 96 tics (cierre de episodio, P6-9), en la que sale solo si esperado > fuego.
    V3 (ampliacion) = V2 si la vida aguanta el primer golpe esperado del arma peor a tiro
    con margen: hp > golpe tipico (P6-19, dano por golpe por arma) + MARGEN + 15 (suelo de
    la puerta); si no la aguanta, actua al ver (se aparta dentro: NO es ruptura) y sale solo
    si esperado > fuego. MARGEN = mediana del dano de rival recibido en los 96 tics que
    siguen a un primer golpe (primero tras >= 96 tics sin golpe) en las 40 vidas de A6, con
    o sin plan (los primeros golpes con plan vivo son demasiado pocos); declarado, con la
    sensibilidad al p75.
  · un episodio desaparece bajo Vk si su causa es «ver el arma» y Vk no rompe en su tic;
    fuego ahorrado = fuego del anillo recibido en los episodios que desaparecen.
  · «habria seguido» (caidas por «vida real X bajo la proyectada Y menos 10»):
    X + dano que Vk evita (fuego de los episodios que desaparecen antes de la caida) >= Y-10.
    Cuenta justa: X + TODO el dano de los tics desviados (fuego y golpes) >= Y-10; se declara
    como decision de metodo. Las caidas «en la reevaluacion (area)» no dependen del veto:
    se cuentan como «no cambia».
  · primer golpe estando sujeto = primer golpe de rival (o primero tras 96 tics sin golpe)
    con el plan vivo y el cuerpo dentro (distancia al centro <= min(r1, radio del tic)).
"""
import collections, glob, json, math, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U, parte2 as P2, oyente2 as OY
C = (24, 24); N_REANUDA = 96; VIDA_MIN = 15.0; TR = 24; FASE5 = 4
_T = json.load(open(os.path.join(AQUI, "P6_19_tasas.json")))
TASAS = _T["tabla_puerta6g"]; TIPICO = {w: v["media"] for w, v in _T["golpes"]["dano_por_golpe_por_arma"].items()}
BINS = [(1, 1, "1"), (2, 2, "2"), (3, 4, "3-4"), (5, 6, "5-6"), (7, 8, "7-8"), (9, 99, ">8")]
VER_ARMA = ("a) veto vital: armado a tiro", "e) armado a menos de 6 y acercandose")


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def bin_de(d):
    for lo, hi, n in BINS:
        if lo <= d <= hi:
            return n
    return ">8"


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); cat = next(r for r in recs if r["k"] == "catalogo")
    sm = next(r for r in recs if r["k"] == "static_map"); mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    fin = next((r for r in recs if r.get("k") == "final"), None)
    armas = {it["id"]: (float(it.get("damage") or 0), int(it.get("range") or 0)) for it in cat["items"] if float(it.get("damage") or 0) > 0}
    T = {}; L = collections.defaultdict(list); ult = None; herm = pc["teammate_slot"]
    for r in recs:
        k = r.get("k")
        if k in ("forma_aceptada", "forma_caida", "compromiso6"):
            L[k].append(r)
        if k != "tick" or r.get("phase") != "live":
            continue
        for m in (r.get("chat") or []):
            if m.get("channel") == "team" and m.get("from") == herm and (m.get("text") or "").startswith("E2 "):
                pp = P2.parsea(m["text"], mundo)
                if pp:
                    ult = pp
        t = r["tick"]
        vis = {int(a["slot"]): ((int(a["pos"][0]), int(a["pos"][1])), ((a.get("hand") or {}).get("id") if isinstance(a.get("hand"), dict) else a.get("hand")) or "none") for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("slot") is not None}
        if ult and 0 <= t - ult["t"] <= OY.CADUCIDAD_RIVAL:
            for x in ult["rivales"]:
                if x["slot"] not in vis:
                    vis[int(x["slot"])] = (tuple(x["pos"]), (x.get("arma") or "none"))
        ra = r.get("RADIOGRAFIA") or {}
        cs = ra.get("candidatos") if isinstance(ra, dict) else None
        T[t] = {"pos": tuple(int(x) for x in r["pos"]), "hp": float(r.get("hp") if r.get("hp") is not None else 100), "radio": float((r.get("zona") or {}).get("radius") or 48),
                "dt": {str(g.get("source")): float(g.get("amount") or 0) for g in (r.get("damage_taken") or []) if isinstance(g, dict)},
                "riv": {s: v for s, v in vis.items() if s not in (pc["slot"], herm)}, "el": str(ra.get("elegido") or ""),
                "ahora": {kk: vv.get("M", 0.0) for kk, vv in ((ra.get("ahora") or {}).get("filas") or {}).items()} if isinstance(ra, dict) else {},
                "cs": (cs if isinstance(cs, dict) and isinstance(cs.get("noop"), dict) else None)}
    del recs
    return pc, T, fin, armas, [tuple(z) for z in pc.get("zone_schedule") or []], L


def fase_en(fases, t):
    k = None
    for i, f in enumerate(fases):
        if f[0] <= t:
            k = i
    return k


def esperado_dentro(pos, riv):
    s = 0.0
    for q, w in riv.values():
        fila = TASAS.get(w if w in TASAS else "none") or {}
        s += float((fila.get(bin_de(cheb(pos, q))) or {}).get("dano_por_rival_tic") or 0.0)
    return s


def fam(el):
    if not el or el == "noop":
        return "quieto"
    if el.startswith("atacar"):
        return "pega"
    if el == "_FM_quedarse":
        return "sujeto"
    if el.startswith(("move", "paso", "ir_", "_FM_ir")):
        return "se mueve"
    return el.split("_")[0]


PLANES = []; PRIMEROS = []; E2_DESARMADO = collections.Counter(); GOLPES_VIDA = []
for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball/runs/P618_t1_A6_*"))):
    fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
    if len(fs) != 2:
        continue
    sem = int(carp.rsplit("_", 1)[1])
    for sl in (10, 11):
        pc, T, fin, armas, fases, L = carga(fs[sl]); ts = sorted(T); mt = max(T)
        warn5, sig5 = fases[FASE5][0], fases[FASE5 + 1][0]; viva5 = warn5 in T
        ug = None
        for t in ts:
            drv = sum(a for s_, a in T[t]["dt"].items() if s_.startswith("P"))
            if drv > 0:
                if ug is None or t - ug > N_REANUDA:
                    GOLPES_VIDA.append({"tick": t, "dano": drv, "hp": T[t]["hp"], "dano_rival_96": sum(a for u in ts if t < u <= t + N_REANUDA for s_, a in T[u]["dt"].items() if s_.startswith("P")),
                                        "golpes_96": sum(1 for u in ts if t < u <= t + N_REANUDA for s_ in T[u]["dt"] if s_.startswith("P")), "muere_96": (mt <= t + N_REANUDA) and bool(fin and fin.get("reason") == "eliminated")})
                ug = t
        c6 = collections.defaultdict(lambda: collections.defaultdict(list))
        for r in L["compromiso6"]:
            c6[r.get("id")][r["tick"]].append(r)
        caidas = {r.get("id"): r for r in L["forma_caida"]}
        for fa in L["forma_aceptada"]:
            pid = fa["id"]; t_ac = fa["tick"]; ev = c6.get(pid, {}); ca = caidas.get(pid)
            t_cump = next((r["tick"] for tt in sorted(ev) for r in ev[tt] if r.get("estado") == "cumplida"), None)
            fin_plan = min([x for x in (ca["tick"] if ca else None, t_cump, mt) if x is not None])
            i = fase_en(fases, t_ac); sig = fases[i + 1][0] if (i is not None and i + 1 < len(fases)) else mt
            fin_plan = min(fin_plan, sig); dps = fases[i][5] if i is not None else 0; fuego = dps / TR; r1 = fases[i][4] if i is not None else 48
            mo = str((ca or {}).get("motivo") or ""); m = re.search(r"la vida real ([\d.]+) esta por debajo de la proyectada ([\d.]+)", mo)
            p = {"semilla": sem, "slot": sl, "id": pid, "aceptada": t_ac, "fin": fin_plan, "fase": (i + 1 if i is not None else None), "fase5": bool(viva5 and warn5 <= t_ac < sig5), "fuego_tic": fuego,
                 "motivo": (("vida real" if m else ("reevaluacion" if "reevaluacion" in mo else mo[:30])) if ca else ("cumplida" if t_cump is not None else "viva al final")),
                 "X": float(m.group(1)) if m else None, "Y": float(m.group(2)) if m else None, "tics": 0, "estados": collections.Counter(), "rupturas": collections.Counter(),
                 "dano": {"fuego_siguiendo": 0.0, "fuego_desviado": 0.0, "rival_siguiendo_ya_estaba": 0.0, "rival_siguiendo_se_acerco": 0.0, "rival_desviado": 0.0, "rival_en_suspension": 0.0},
                 "vetos": [], "episodios": [], "primeros": []}
            riv0 = set(T[t_ac]["riv"]) if t_ac in T else set()
            ult_golpe = None; ep = None; prev_desviado = False
            for t in ts:
                if t < t_ac or t > fin_plan:
                    continue
                r = T[t]; p["tics"] += 1; pos = r["pos"]; dentro = math.dist(pos, C) <= min(r1, r["radio"])
                dr = {s: a for s, a in r["dt"].items() if s.startswith("P")}; dz = r["dt"].get("zone", 0.0); drv = sum(dr.values())
                recs_t = ev.get(t, []); est = next((x.get("estado") for x in recs_t if x.get("estado") in ("rompe", "enfriamiento", "obedece", "sujeta")), "libre")
                p["estados"][est] += 1; desviado = (est == "rompe") or (prev_desviado and not dentro); prev_desviado = desviado
                causa_t = next((str(x.get("causa")) for x in recs_t if x.get("estado") == "rompe"), None)
                if causa_t:
                    p["rupturas"][causa_t] += 1
                    if causa_t.startswith("e) rival a 2"):
                        det = next((x.get("detalle") or {} for x in recs_t if x.get("estado") == "rompe"), {})
                        w = (r["riv"].get(int(det.get("slot") or -1)) or (None, "?"))[1]
                        E2_DESARMADO["armado" if (w in armas and armas[w][1] > 0) else ("mano vacia" if w in ("none", "?") else w)] += 1
                suspendido = ult_golpe is not None and (t - ult_golpe) <= N_REANUDA
                # episodios de desviacion
                if desviado:
                    if ep is None:
                        ep = {"t0": t, "causa": causa_t, "fuego": 0.0, "rival": 0.0, "tics": 0, "sale": False, "esp": None, "susp": suspendido}
                        p["episodios"].append(ep)
                    ep["tics"] += 1; ep["fuego"] += dz; ep["rival"] += drv; ep["sale"] |= (not dentro)
                    if ep["causa"] is None and causa_t:
                        ep["causa"] = causa_t
                else:
                    ep = None
                # el dano, por donde estaba el plan
                if desviado:
                    p["dano"]["fuego_desviado"] += dz; p["dano"]["rival_desviado"] += drv
                else:
                    p["dano"]["fuego_siguiendo"] += dz
                    for s, a in dr.items():
                        p["dano"]["rival_siguiendo_ya_estaba" if int(s[1:]) in riv0 else "rival_siguiendo_se_acerco"] += a
                if suspendido:
                    p["dano"]["rival_en_suspension"] += drv
                # primer golpe
                if drv > 0:
                    if ult_golpe is None or (t - ult_golpe) > N_REANUDA:
                        s_ag = max(dr, key=dr.get); ag = r["riv"].get(int(s_ag[1:]))
                        w = ag[1] if ag else next((T[u]["riv"][int(s_ag[1:])][1] for u in range(t - 1, max(t_ac, t - 50) - 1, -1) if u in T and int(s_ag[1:]) in T[u]["riv"]), "?")
                        pr = {"semilla": sem, "slot": sl, "id": pid, "tick": t, "dano": drv, "hp": r["hp"], "dentro": dentro, "estado": est, "arma": w, "dist": (cheb(pos, ag[0]) if ag else None),
                              "fase5": p["fase5"], "tipico": TIPICO.get(w if w in TIPICO else "none", 0.0)}
                        vent = [u for u in ts if t < u <= min(t + N_REANUDA, fin_plan)]
                        pr["tics_ventana"] = len(vent); pr["dano_rival_96"] = sum(a for u in vent for s, a in T[u]["dt"].items() if s.startswith("P")); pr["fuego_96"] = sum(T[u]["dt"].get("zone", 0.0) for u in vent)
                        pr["golpes_96"] = sum(1 for u in vent for s in T[u]["dt"] if s.startswith("P"))
                        pr["hizo"] = dict(collections.Counter(fam(T[u]["el"]) for u in vent)); pr["sale_en"] = next((u - t for u in vent if math.dist(T[u]["pos"], C) > T[u]["radio"]), None)
                        pr["muere_en_96"] = (mt <= t + N_REANUDA) and bool(fin and fin.get("reason") == "eliminated")
                        pr["hp_fin_96"] = T[vent[-1]]["hp"] if vent else r["hp"]
                        filas = collections.Counter(); n_f = 0
                        for u in vent:
                            if T[u]["el"] and T[u]["el"] != "noop":
                                n_f += 1
                                for kk, vv in T[u]["ahora"].items():
                                    filas[kk] += vv
                        pr["filas_ahora_media"] = {kk: round(vv / max(1, n_f), 3) for kk, vv in filas.most_common(5)}
                        det = next((u for u in vent[:25] if T[u]["cs"] and T[u]["el"] in T[u]["cs"]), None)
                        if det is not None:
                            cs = T[det]["cs"]; el = T[det]["el"]; fe, fn = cs[el].get("filas") or {}, cs["noop"].get("filas") or {}
                            pr["detalle"] = {"tick": det, "elegido": el, "delta_elegido_menos_noop": {k: round((fe.get(k) or 0) - (fn.get(k) or 0), 4) for k in set(fe) | set(fn) if abs((fe.get(k) or 0) - (fn.get(k) or 0)) > 1e-4}}
                        p["primeros"].append(pr); PRIMEROS.append(pr)
                    ult_golpe = t
                # los vetos, en los tics de «ver el arma»
                if causa_t in VER_ARMA:
                    esp = esperado_dentro(pos, r["riv"])
                    tiro = [(w, armas[w][1]) for _q, w in r["riv"].values() if w in armas and armas[w][1] > 0 and cheb(pos, _q) <= armas[w][1]]
                    vis_arm = [w for _q, w in r["riv"].values() if w in armas and armas[w][1] > 0]
                    peor = max([TIPICO.get(w, 0.0) for w, _rg in tiro] or [TIPICO.get(w, 0.0) for w in vis_arm] or [0.0])
                    v = {"t": t, "causa": causa_t, "esp": esp, "fuego": fuego, "susp": suspendido, "hp": r["hp"], "peor": peor, "V1": esp > fuego, "V2": suspendido and esp > fuego, "ep": (len(p["episodios"]) - 1 if ep is not None else None)}
                    p["vetos"].append(v)
                    if ep is not None and ep["esp"] is None:
                        ep["esp"] = esp; ep["v"] = v
            p["estados"] = dict(p["estados"]); p["rupturas"] = dict(p["rupturas"]); p["dano"] = {k: round(v, 2) for k, v in p["dano"].items()}
            PLANES.append(p)
        print(f"  A6 {sem} s{sl}: planes {len(L['forma_aceptada'])} · rompe {sum(1 for r in L['compromiso6'] if r.get('estado') == 'rompe')}", flush=True)
        del T

# ── el margen de V3, de los datos ─────────────────────────────────────────
suj = [pr for pr in PRIMEROS if pr["dentro"]]
_g = sorted(g["dano_rival_96"] for g in GOLPES_VIDA)
MARGEN = st.median(_g) if _g else 0.0
MARGEN_P75 = _g[int(0.75 * len(_g))] if _g else 0.0
for p in PLANES:
    for v in p["vetos"]:
        v["debil"] = v["hp"] <= v["peor"] + MARGEN + VIDA_MIN
        v["V3"] = (v["susp"] or v["debil"]) and v["esp"] > v["fuego"]
        v["V3_aparta_dentro"] = v["debil"] and not v["V3"]
    for pr in p["primeros"]:
        pr["debil_V3"] = pr["hp"] <= pr["tipico"] + MARGEN + VIDA_MIN


def resumen(S, etiq):
    R = {"ambito": etiq, "planes": len(S), "tics_plan_vivo": sum(p["tics"] for p in S), "estados": dict(sum((collections.Counter(p["estados"]) for p in S), collections.Counter())),
         "rupturas_V0": dict(sum((collections.Counter(p["rupturas"]) for p in S), collections.Counter())), "fines": dict(collections.Counter(p["motivo"] for p in S))}
    R["rupturas_V0_total"] = sum(R["rupturas_V0"].values()); R["veto_a_V0"] = R["rupturas_V0"].get("a) veto vital: armado a tiro", 0)
    V = [v for p in S for v in p["vetos"]]; EP = [e for p in S for e in p["episodios"]]
    R["tics_ver_el_arma"] = len(V); R["esp_en_tics_ver_arma"] = {"media": round(st.mean(v["esp"] for v in V), 4) if V else None, "max": round(max((v["esp"] for v in V), default=0), 4), "fuego_tic_medio": round(st.mean(v["fuego"] for v in V), 3) if V else None,
                                                                "esp_supera_fuego": sum(1 for v in V if v["esp"] > v["fuego"]), "en_suspension": sum(1 for v in V if v["susp"]), "debil": sum(1 for v in V if v["debil"])}
    R["episodios_desviacion"] = {"n": len(EP), "por_causa": dict(collections.Counter(str(e["causa"])[:2] for e in EP)), "tics": sum(e["tics"] for e in EP), "fuego": round(sum(e["fuego"] for e in EP), 1), "rival": round(sum(e["rival"] for e in EP), 1),
                                 "salen_del_circulo": sum(1 for e in EP if e["sale"]), "tics_mediana": st.median(e["tics"] for e in EP) if EP else None}
    R["vetos"] = {}
    for k in ("V0", "V1", "V2", "V3"):
        rompe = (lambda v: True) if k == "V0" else (lambda v, k=k: v[k])
        quitados = [v for v in V if not rompe(v)]
        ep_q = [e for e in EP if e["causa"] in VER_ARMA and e.get("v") is not None and not rompe(e["v"])]
        d = {"tics_ver_arma_que_rompen": sum(1 for v in V if rompe(v)), "tics_veto_que_desaparecen": len(quitados), "rupturas_restantes": R["rupturas_V0_total"] - len(quitados),
             "episodios_que_desaparecen": len(ep_q), "fuego_ahorrado": round(sum(e["fuego"] for e in ep_q), 1), "golpes_rival_en_esos_episodios": round(sum(e["rival"] for e in ep_q), 1),
             "esperado_extra_por_quedarse (suma esp en los tics quitados)": round(sum(v["esp"] for v in quitados), 2), "esperado_extra_cota_alta (esp x tics del episodio)": round(sum(e["esp"] * e["tics"] for e in ep_q if e["esp"] is not None), 2)}
        if k == "V3":
            d["tics_se_aparta_dentro (debil, sin romper)"] = sum(1 for v in V if v["V3_aparta_dentro"])
        seg_vr = 0; n_vr = 0
        for p in S:
            if p["motivo"] != "vida real":
                continue
            n_vr += 1
            ah = sum(e["fuego"] for e in p["episodios"] if e["causa"] in VER_ARMA and e.get("v") is not None and not rompe(e["v"]))
            if p["X"] + ah >= p["Y"] - 10:
                seg_vr += 1
        d["caidas_vida_real_que_habrian_seguido"] = seg_vr; d["de"] = n_vr
        R["vetos"][k] = d
    # cuenta justa
    CA = [p for p in S if p["motivo"] == "vida real"]
    cj = {"caidas_vida_real": len(CA), "caidas_reevaluacion": sum(1 for p in S if p["motivo"] == "reevaluacion"), "caidas_otras": sum(1 for p in S if p["motivo"] not in ("vida real", "reevaluacion", "cumplida", "viva al final")),
          "dano_hasta_la_caida": {k: round(sum(p["dano"][k] for p in CA), 1) for k in CA[0]["dano"]} if CA else {},
          "hueco_X_menos_Y": {"media": round(st.mean(p["X"] - p["Y"] for p in CA), 1) if CA else None, "mediana": st.median(p["X"] - p["Y"] for p in CA) if CA else None},
          "seguirian_con_cuenta_justa (X + dano desviado >= Y-10)": sum(1 for p in CA if p["X"] + p["dano"]["fuego_desviado"] + p["dano"]["rival_desviado"] >= p["Y"] - 10),
          "seguirian_descontando_tambien_golpes_en_suspension": sum(1 for p in CA if p["X"] + p["dano"]["fuego_desviado"] + p["dano"]["rival_desviado"] + p["dano"]["rival_en_suspension"] >= p["Y"] - 10),
          "seguirian_descontando_solo_fuego_desviado": sum(1 for p in CA if p["X"] + p["dano"]["fuego_desviado"] >= p["Y"] - 10),
          "caidas_sin_desviacion_alguna": sum(1 for p in CA if p["dano"]["fuego_desviado"] + p["dano"]["rival_desviado"] == 0),
          "caidas_con_solo_golpes_de_rival": sum(1 for p in CA if p["dano"]["fuego_desviado"] + p["dano"]["fuego_siguiendo"] == 0 and (p["dano"]["rival_siguiendo_ya_estaba"] + p["dano"]["rival_siguiendo_se_acerco"] + p["dano"]["rival_desviado"]) > 0),
          "por_caida": [{"semilla": p["semilla"], "slot": p["slot"], "id": p["id"], "X": p["X"], "Y": p["Y"], "dano": p["dano"], "tics": p["tics"]} for p in CA]}
    R["cuenta_justa"] = cj
    # primeros golpes
    PR = [pr for p in S for pr in p["primeros"]]; PS = [pr for pr in PR if pr["dentro"]]
    R["primeros_golpes"] = {"total_con_plan_vivo": len(PR), "estando_dentro (sujeto)": len(PS), "dano": round(sum(pr["dano"] for pr in PS), 1), "por_arma": dict(collections.Counter(pr["arma"] for pr in PS)),
                            "estado_del_compromiso_en_el_golpe": dict(collections.Counter(pr["estado"] for pr in PS)), "hp_media_en_el_golpe": round(st.mean(pr["hp"] for pr in PS), 1) if PS else None,
                            "dano_rival_96_despues": {"suma": round(sum(pr["dano_rival_96"] for pr in PS), 1), "mediana": st.median(pr["dano_rival_96"] for pr in PS) if PS else None, "con_mas_golpes": sum(1 for pr in PS if pr["golpes_96"] > 0)},
                            "fuego_96_despues": round(sum(pr["fuego_96"] for pr in PS), 1), "salen_del_circulo_en_96": sum(1 for pr in PS if pr["sale_en"] is not None), "sale_en_mediana": st.median([pr["sale_en"] for pr in PS if pr["sale_en"] is not None] or [0]),
                            "mueren_en_96": sum(1 for pr in PS if pr["muere_en_96"]), "debiles_V3": sum(1 for pr in PS if pr["debil_V3"]), "dano_de_los_debiles": round(sum(pr["dano"] for pr in PS if pr["debil_V3"]), 1),
                            "hizo_en_96 (tics por familia, suma)": dict(sum((collections.Counter(pr["hizo"]) for pr in PS), collections.Counter()))}
    F = collections.defaultdict(list); D = collections.defaultdict(list)
    for pr in PS:
        for k, v in pr["filas_ahora_media"].items():
            F[k].append(v)
        for k, v in (pr.get("detalle") or {}).get("delta_elegido_menos_noop", {}).items():
            D[k].append(v)
    R["primeros_golpes"]["filas_ahora_media (media de medias)"] = {k: round(st.mean(v), 3) for k, v in sorted(F.items(), key=lambda kv: -len(kv[1]))[:8]}
    R["primeros_golpes"]["delta_elegido_menos_noop (media, n detalles)"] = {k: [round(st.mean(v), 4), len(v)] for k, v in sorted(D.items(), key=lambda kv: -abs(st.mean(kv[1])))[:8]}
    R["primeros_golpes"]["detalle_elegidos"] = dict(collections.Counter((pr.get("detalle") or {}).get("elegido", "sin detalle") for pr in PS))
    return R


R = {"nota": "P6-20 A. INSTRUMENTO DE MEDIDA sobre las 40 vidas de A6. Contrafactual de recuento, no de conducta.", "N_reanuda": N_REANUDA, "VIDA_MIN": VIDA_MIN,
     "margen_V3": {"mediana_dano_rival_96_tras_primer_golpe (40 vidas, con o sin plan)": MARGEN, "p75": MARGEN_P75, "media": round(st.mean(_g), 2) if _g else None, "n_primeros_golpes": len(_g), "con_mas_golpes_en_96": sum(1 for g in GOLPES_VIDA if g["golpes_96"] > 0),
                   "mueren_en_96": sum(1 for g in GOLPES_VIDA if g["muere_96"]), "primeros_golpes_con_plan_vivo_sujeto": len(suj), "tipico_por_arma": TIPICO},
     "e2_rival_a_2_o_menos_por_arma": dict(E2_DESARMADO)}
for etiq, S in (("fase5", [p for p in PLANES if p["fase5"]]), ("todos", PLANES)):
    R[etiq] = resumen(S, etiq)
R["primeros_golpes_lista"] = [{k: v for k, v in pr.items() if k not in ("filas_ahora_media",)} for pr in PRIMEROS if pr["dentro"]]
R["planes"] = [{k: v for k, v in p.items() if k not in ("vetos", "primeros")} for p in PLANES]
json.dump(R, open(os.path.join(AQUI, "P6_20_banco.json"), "w"), ensure_ascii=False, indent=1, default=str)
for etiq in ("fase5", "todos"):
    x = R[etiq]
    print(f"=== {etiq}: planes {x['planes']} · tics {x['tics_plan_vivo']} · estados {x['estados']} · rupturas {x['rupturas_V0']} · fines {x['fines']}")
    print(f"   ver el arma {x['tics_ver_el_arma']} · esp {x['esp_en_tics_ver_arma']} · episodios {x['episodios_desviacion']}")
    for k, d in x["vetos"].items():
        print(f"   {k}: {d}")
    cj = dict(x["cuenta_justa"]); cj.pop("por_caida"); print(f"   cuenta justa: {cj}")
    print(f"   primeros golpes: {x['primeros_golpes']}")
print(f"margen V3: {R['margen_V3']} · e) rival a 2 por arma: {R['e2_rival_a_2_o_menos_por_arma']}")
print("-> P6_20_banco.json")
