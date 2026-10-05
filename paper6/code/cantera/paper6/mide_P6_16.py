"""[P6-16 · 2] LAS MEDIDAS, TRES COLUMNAS (A4, A5v, A5h) EMPAREJADAS POR SEMILLA. SOLO LECTURA.

    python3 mide_P6_16.py 'A4=paintball/runs/P611_t*_A4_*' 'A5v=paintball/runs/P616_t1_A5v_*' 'A5h=paintball/runs/P616_t2_A5h_*'

Definiciones, copiadas de donde nacieron (no reimplementadas a mi manera):
  · vida = ultimo tic vivo (mide_P6_4); superviviente = `final.reason != eliminated`;
    «los dos vivos al final» = ninguno eliminado en la partida;
  · causa de muerte = la de mide_golpes_P6_11 (ultimo golpe de rival en los 48
    tics antes de morir, o anillo si el ultimo dano es de `zone`);
  · muerte por anillo EVITABLE y su clase = las de mide_anillo_P6_13 (fase que
    mata = ultima con warn <= primer golpe de la racha final; evitable = fases 1-6;
    clase por el peso de las filas de miedo / hermano contra `ir_centro` en el
    detalle de la radiografia; BFS a casilla segura);
  · juntos = % de tics con los dos vivos a distancia Chebyshev <= 3 y <= 8
    (mide_pareja_P6_11); escapadas largas = excursiones (distancia > 8 viniendo
    de <= 8, hasta volver o morir) de >= 200 tics (mide_separa/largas_P6_11);
  · comida = tics en que el `pack` sube en rations o first_aid (mide_base2_P6_11);
  · tiempo ardiendo = tics con `damage_taken` de `zone`;
  · planes (A5): `oraculo16 propone` = ofrecidos; `forma_evaluada` = veredicto
    de la puerta; `forma_aceptada`; `compromiso6`: obedece / enfriamiento /
    rompe (causa) / cumplida (por destino o a salvo = ANDADO); `forma_caida`
    (motivo) = ABANDONADO; (c) aceptado por los dos = mismo destino aceptado en
    los dos diarios a <= 50 tics;
  · aceptacion que aleja del hermano = destino mas lejos del hermano (posicion
    real del otro diario en ese tic) que mi casilla; consecuencia = distancia
    al hermano 100 tics despues, y si muere en los 300 tics siguientes y de que.
"""
import collections, glob, json, math, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
MIEDO = ("S-8-EXPOSICION", "F-4-ALCANCE", "S-7-AGRESOR", "F-DANO", "F-REENCUENTRO", "MIEDO_APRENDIDO")
HERMANO = ("S-COMPANIA", "F-HERMANO-AMENAZA", "F-HERMANO-GOLPE", "S-DANO-PAREJA", "S-HERIDO", "S-PROVISION", "R-HERMANO-FALTA", "S-SOLEDAD")
COMIDA = ("rations", "first_aid")
LEJOS, LARGA = 8, 200
FASE_FINAL = 7


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def fam(e):
    for p in ("ir_centro", "ir_pareja", "ir_objeto", "ir_botin", "move_", "paso_", "atacar", "coger", "noop", "usar", "soltar", "_FM_"):
        if e.startswith(p):
            return p.rstrip("_")
    return "otro"


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); fin = next((r for r in recs if r.get("k") == "final"), None)
    dano = {it["id"]: float(it.get("damage") or 0) for it in cat["items"]}
    sp = 5
    for r in recs:
        if r.get("k") == "arranque":
            m = re.search(r'"speed"\s*:\s*(\d+)', json.dumps(r)); sp = int(m.group(1)) if m else 5; break
    T = {}; L = collections.defaultdict(list)
    for r in recs:
        k = r.get("k")
        if k in ("oraculo16", "forma_evaluada", "forma_reevaluada", "forma_aceptada", "forma_caida", "compromiso6", "resumen16", "hilo_forma", "tiempo_tic", "forma_error", "confianza"):
            L[k].append(r)
        if k != "tick" or r.get("phase") != "live":
            continue
        ra = r.get("RADIOGRAFIA") or {}
        T[r["tick"]] = {"pos": tuple(int(x) for x in r["pos"]), "hp": r.get("hp"), "zona": r.get("zona") or {},
                        "zone_hit": any(g.get("source") == "zone" for g in (r.get("damage_taken") or [])),
                        "dt": [g for g in (r.get("damage_taken") or []) if isinstance(g, dict)],
                        "el": str(ra.get("elegido") or ""), "listas": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0) == 0,
                        "cs": ra.get("candidatos") if isinstance((ra.get("candidatos") or {}).get("noop"), dict) else None,
                        "ve": {a.get("slot"): (int(a["pos"][0]), int(a["pos"][1]), a.get("hand")) for a in (r.get("ve_agentes") or []) if a.get("pos")},
                        "pack": {(s or {}).get("id"): int((s or {}).get("n") or 1) for s in (r.get("pack") or []) if s},
                        "ms16": (ra.get("ms16") if isinstance(ra, dict) else None)}
    del recs
    return mundo, pc, T, fin, sp, dano, L


def bfs_seguro(mundo, desde, r1):
    n = mundo.arena_size; c = (n // 2, n // 2)
    def segura(p): return math.dist(p, c) <= r1 and not mundo.solido(p[0], p[1])
    if segura(desde):
        return 0
    vis = {desde}; frente = [desde]; k = 0
    while frente:
        k += 1; nuevo = []
        for (x, y) in frente:
            for dx, dy in DIRS:
                q = (x + dx, y + dy)
                if not (0 <= q[0] < n and 0 <= q[1] < n) or q in vis or mundo.solido(q[0], q[1]):
                    continue
                if segura(q):
                    return k
                vis.add(q); nuevo.append(q)
        frente = nuevo
    return None


def causa_muerte(T, fin, dano):
    """mide_golpes_P6_11, tal cual."""
    if not (fin and fin.get("reason") == "eliminated"):
        return None, None
    tl = sorted(T); mt = int(fin.get("match_ticks") or tl[-1])
    golpes = []
    for t in tl:
        r = T[t]
        for g in r["dt"]:
            s = str(g.get("source"))
            if not s.startswith("P"):
                continue
            slot = int(s[1:]); a = r["ve"].get(slot)
            if a is None:
                k = "rival NO visto"
            else:
                h = a[2]
                k = "rival visto CON arma en mano" if h and h != "none" and dano.get(h, 0) > 0 else "rival visto con hand NONE"
            golpes.append((t, slot, k))
    cerca = [g for g in golpes if mt - 48 <= g[0] <= mt]
    zt = [t for t in tl if mt - 48 <= t <= mt and T[t]["zone_hit"]]
    if cerca and (not zt or cerca[-1][0] >= max(zt)):
        return cerca[-1][2], cerca[-1][1]
    if zt:
        return "anillo", None
    return "no consta", None


def anatomia_anillo(mundo, T, To, sp, fases):
    """mide_anillo_P6_13, tal cual (la clase de la muerte por anillo)."""
    coste = mundo.coste_movimiento(sp); tm = max(T)
    hits_all = [t for t in sorted(T) if T[t]["zone_hit"]]
    th = None
    if hits_all:
        th = hits_all[-1]
        for a, b in zip(reversed(hits_all[:-1]), reversed(hits_all)):
            if b - a <= 48:
                th = a
            else:
                break
    fase = max((f for f in fases if f[0] <= (th if th is not None else tm)), key=lambda f: f[0]); warn = fase[0]; r1 = fase[4]
    d = {"aviso": warn, "primer_golpe": th, "muerte": tm, "fase": fases.index(fase) + 1, "r1": r1, "dps": fase[5],
         "tics_aviso_a_muerte": tm - warn, "tics_golpe_a_muerte": (tm - th) if th else None}
    for nombre, t in (("aviso", warn), ("golpe", th)):
        if t is None or t not in T:
            d[f"pasos_{nombre}"] = None; d[f"instantes_{nombre}"] = None; continue
        k = bfs_seguro(mundo, T[t]["pos"], r1)
        d[f"pasos_{nombre}"] = k; d[f"instantes_{nombre}"] = (k * coste) if k is not None else None
    d["habia_camino"] = d["pasos_aviso"] is not None
    d["llegaba_saliendo_en_el_aviso"] = (d["instantes_aviso"] is not None and d["instantes_aviso"] < d["tics_aviso_a_muerte"])
    d["hermano_vivo_en_muerte"] = tm in To
    t0 = th or warn; w = [t for t in sorted(T) if t0 <= t <= tm]
    d["tics_con_piernas"] = sum(1 for t in w if T[t]["listas"])
    deltas = collections.defaultdict(list); n_det = 0
    for t in w:
        cs = T[t]["cs"]
        if not cs or not T[t]["listas"] or "ir_centro" not in cs:
            continue
        n_det += 1; el = T[t]["el"]
        if el == "ir_centro" or el not in cs:
            continue
        fg, fc = cs[el].get("filas") or {}, cs["ir_centro"].get("filas") or {}
        for k in set(fg) | set(fc):
            deltas[k].append((fg.get(k) or 0.0) - (fc.get(k) or 0.0))
    peso_miedo = -sum(sum(v) / len(v) for k, v in deltas.items() if k in MIEDO and sum(v) < 0)
    peso_herm = -sum(sum(v) / len(v) for k, v in deltas.items() if k in HERMANO and sum(v) < 0)
    d["peso_miedo"] = round(peso_miedo, 4); d["peso_hermano"] = round(peso_herm, 4); d["detalle_n"] = n_det
    if not d["habia_camino"] and d["pasos_golpe"] is None:
        d["clase"] = "iv · no habia salida"
    elif n_det == 0 and d["tics_con_piernas"] == 0:
        d["clase"] = "v · sin piernas listas entre el golpe y la muerte"
    elif peso_miedo > peso_herm and peso_miedo > 0:
        d["clase"] = "ii · lo retuvo el miedo a rivales"
    elif peso_herm > 0:
        d["clase"] = "iii · lo retuvo el hermano"
    elif d["llegaba_saliendo_en_el_aviso"]:
        d["clase"] = "i · llegaba a salvo si salia antes"
    else:
        d["clase"] = "v · otra"
    d["evitable"] = d["fase"] != FASE_FINAL
    return d


def planes_de(L, T, To, fin):
    """Los planes del oraculo en esta vida, con lo que les paso."""
    P = collections.Counter(); ac = []
    for r in L.get("oraculo16", []):
        P["ofrecidos" if r.get("estado") == "propone" else ("no juzgables (propia)" if "propia" in str(r.get("estado")) else "sin plan/otros")] += 1
        if r.get("estado") == "propone":
            P["ofrecidos (c)"] += ("c" in (r.get("criterios") or [])); P["ofrecidos con hermano vivo"] += bool(r.get("hermano_vivo"))
    for r in L.get("forma_evaluada", []):
        P["veredicto " + str(r.get("veredicto"))] += 1
    for r in L.get("forma_reevaluada", []):
        P["reevaluada " + str(r.get("veredicto"))] += 1
    for r in L.get("forma_aceptada", []):
        d = (r.get("tramos") or [{}])[0].get("destino")
        ac.append({"tick": r["tick"], "id": r.get("id"), "destino": d, "ventaja": r.get("ventaja"), "fin": None, "motivo": None, "obedece": 0, "rompe": collections.Counter(), "enfria": 0})
    por_id = {a["id"]: a for a in ac}
    for r in L.get("compromiso6", []):
        a = por_id.get(r.get("id"))
        if a is None:
            continue
        e = r.get("estado")
        if e == "obedece":
            a["obedece"] += 1
        elif e == "enfriamiento":
            a["enfria"] += 1
        elif e == "rompe":
            a["rompe"][str(r.get("causa"))] += 1
        elif e == "cumplida":
            a["fin"] = "andado (" + str(r.get("por")) + ")"; a["fin_tick"] = r["tick"]
    for r in L.get("forma_caida", []):
        a = por_id.get(r.get("id"))
        if a is not None and a["fin"] is None:
            a["fin"] = "abandonado"; a["motivo"] = str(r.get("motivo"))[:70]; a["fin_tick"] = r["tick"]
    muerte = max(T) if (fin and fin.get("reason") == "eliminated") else None
    for a in ac:
        if a["fin"] is None:
            a["fin"] = "muere con el plan vivo" if (muerte is not None and muerte - a["tick"] <= 300) else "sin cierre registrado"
        a["rompe"] = dict(a["rompe"])
        P["aceptados"] += 1; P["fin: " + a["fin"]] += 1
        if a["motivo"]:
            P["abandono: " + a["motivo"][:40]] += 1
        for c, n in a["rompe"].items():
            P["ruptura " + c] += n
        P["obedece"] += a["obedece"]
        # ¿aleja del hermano? consecuencias
        t = a["tick"]; hp_ = To.get(t) or To.get(max((x for x in To if x <= t), default=None), None) if To else None
        if hp_ and a["destino"]:
            me = T[t]["pos"] if t in T else None
            if me:
                d0 = cheb(me, hp_["pos"]); d1 = cheb(tuple(a["destino"]), hp_["pos"])
                a["aleja"] = d1 > d0; a["d_herm_antes"] = d0; a["d_herm_destino"] = d1
                t2 = t + 100
                if t2 in T and t2 in To:
                    a["d_herm_100"] = cheb(T[t2]["pos"], To[t2]["pos"])
                a["muere_en_300"] = (muerte is not None and t < muerte <= t + 300)
                if a["aleja"]:
                    P["aceptados que alejan del hermano"] += 1
                    if a.get("d_herm_100") is not None:
                        P["  ...distancia a +100 (suma)"] += a["d_herm_100"]; P["  ...con distancia a +100"] += 1
                    P["  ...muere en 300 tics"] += bool(a["muere_en_300"])
    return dict(P), ac


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    carps = sorted(glob.glob(os.path.join(RAIZ, pat)))
    R = {"vidas": [], "por_semilla": {}, "planes": collections.Counter(), "aceptados": []}
    for carp in carps:
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            print(f"    {os.path.basename(carp)}: sin los dos diarios"); continue
        semilla = int(carp.rsplit("_", 1)[1])
        D = {sl: carga(fs[sl]) for sl in (10, 11)}
        fases = [tuple(z) for z in D[10][1].get("zone_schedule") or []]
        sem = {"semilla": semilla, "carp": os.path.basename(carp)}
        acept_por_slot = {}
        for sl in (10, 11):
            mundo, pc, T, fin, sp, dano, L = D[sl]; To = D[21 - sl][2]
            mt = max(T) if T else 0
            v = {"semilla": semilla, "slot": sl, "tics": mt, "superviviente": bool(fin and fin.get("reason") != "eliminated"), "razon": (fin or {}).get("reason"),
                 "comida": 0, "tics_ardiendo": sum(1 for t in T if T[t]["zone_hit"]), "golpes_rival": sum(1 for t in T for g in T[t]["dt"] if str(g.get("source")).startswith("P")),
                 "dano_rival": round(sum(float(g.get("amount") or 0) for t in T for g in T[t]["dt"] if str(g.get("source")).startswith("P")), 1)}
            ant = None
            for t in sorted(T):
                pk = T[t]["pack"]
                if ant is not None:
                    for c in COMIDA:
                        if pk.get(c, 0) > ant.get(c, 0):
                            v["comida"] += 1
                ant = pk
            v["causa"], v["matador"] = causa_muerte(T, fin, dano)
            if v["causa"] == "anillo":
                v["anillo"] = anatomia_anillo(mundo, T, To, sp, fases)
            v["planes"], ac = planes_de(L, T, To, fin)
            acept_por_slot[sl] = ac
            r16 = (L.get("resumen16") or [None])[-1]
            ms16 = sorted(x["ms16"] for x in T.values() if x.get("ms16") is not None)
            tt = sorted(float(x.get("ms") or 0) for x in L.get("tiempo_tic", []))
            v["latencia"] = {"ms16_mediana": (ms16[len(ms16) // 2] if ms16 else None), "ms16_p95": (ms16[int(len(ms16) * 0.95)] if ms16 else None), "ms16_max": (ms16[-1] if ms16 else None),
                             "ms16_mas_de_un_tic": sum(1 for x in ms16 if x > 1000 / 24), "n": len(ms16),
                             "tiempo_tic_mediana": (tt[len(tt) // 2] if tt else None), "tiempo_tic_max": (tt[-1] if tt else None), "tiempo_tic_mas_de_un_tic": sum(1 for x in tt if x > 1000 / 24)}
            v["resumen16"] = {k: r16.get(k) for k in ("rollouts", "rollout_ms_mediana", "ms_forma_mediana", "obedece", "cumplidas", "rupturas", "C", "margen")} if r16 else None
            R["vidas"].append(v); R["aceptados"] += [dict(a, semilla=semilla, slot=sl) for a in ac]
            sem[f"s{sl}"] = {"tics": mt, "superviviente": v["superviviente"], "causa": v["causa"], "anillo_evitable": bool(v.get("anillo", {}).get("evitable")), "clase": (v.get("anillo") or {}).get("clase"),
                             "comida": v["comida"], "ardiendo": v["tics_ardiendo"], "aceptados": len(ac), "ofrecidos": v["planes"].get("ofrecidos", 0)}
        # la pareja: juntos y escapadas largas
        Ta, Tb = D[10][2], D[11][2]
        comunes = sorted(set(Ta) & set(Tb)); dist = [cheb(Ta[t]["pos"], Tb[t]["pos"]) for t in comunes]
        sem["juntos_3"] = round(100 * sum(1 for d in dist if d <= 3) / max(1, len(dist)), 1); sem["juntos_8"] = round(100 * sum(1 for d in dist if d <= 8) / max(1, len(dist)), 1)
        sem["dist_mediana"] = (st.median(dist) if dist else None); sem["tics_comunes"] = len(comunes)
        exc = []; ini = None
        for t, d in zip(comunes, dist):
            if ini is None and d > LEJOS:
                ini = t
            elif ini is not None and d <= LEJOS:
                exc.append(t - ini); ini = None
        if ini is not None and comunes:
            exc.append(comunes[-1] - ini)
        sem["escapadas"] = len(exc); sem["escapadas_largas"] = sum(1 for x in exc if x >= LARGA); sem["escapada_max"] = max(exc) if exc else 0
        sem["los_dos_vivos_al_final"] = all(D[sl][3] and D[sl][3].get("reason") != "eliminated" for sl in (10, 11))
        # (c) aceptado por los dos: mismo destino a <= 50 tics
        n_c2 = 0
        for a in acept_por_slot[10]:
            if any(b["destino"] == a["destino"] and abs(b["tick"] - a["tick"]) <= 50 for b in acept_por_slot[11]):
                n_c2 += 1
        sem["c_aceptado_por_los_dos"] = n_c2
        R["por_semilla"][str(semilla)] = sem
        for k, n in v["planes"].items():
            pass
        for sl in (10, 11):
            for k, n in R["vidas"][-2 if sl == 10 else -1]["planes"].items():
                R["planes"][k] += n
        print(f"    {os.path.basename(carp)}: s10 {sem['s10']['tics']} {sem['s10']['causa']} · s11 {sem['s11']['tics']} {sem['s11']['causa']} · juntos3 {sem['juntos_3']} · ofrecidos {sem['s10']['ofrecidos']}+{sem['s11']['ofrecidos']} aceptados {sem['s10']['aceptados']}+{sem['s11']['aceptados']}", flush=True)
    V = R["vidas"]; PS = R["por_semilla"]
    res = {"vidas": len(V), "semillas": len(PS), "vida_media": round(st.mean(v["tics"] for v in V), 1) if V else None,
           "supervivientes": sum(v["superviviente"] for v in V), "los_dos_vivos_al_final": sum(1 for s in PS.values() if s["los_dos_vivos_al_final"]),
           "muertes_anillo": sum(1 for v in V if v["causa"] == "anillo"), "muertes_anillo_evitables": sum(1 for v in V if v.get("anillo", {}).get("evitable")),
           "clases_anillo": dict(collections.Counter((v.get("anillo") or {}).get("clase", "")[:3].strip(" ·") for v in V if v["causa"] == "anillo")),
           "muertes_rival": sum(1 for v in V if v["causa"] and v["causa"] not in ("anillo", "no consta")), "muertes_no_consta": sum(1 for v in V if v["causa"] == "no consta"),
           "golpes_rival_por_vida": round(sum(v["golpes_rival"] for v in V) / max(1, len(V)), 2), "dano_rival_por_vida": round(sum(v["dano_rival"] for v in V) / max(1, len(V)), 1),
           "comida_por_vida": round(sum(v["comida"] for v in V) / max(1, len(V)), 2), "ardiendo_por_vida": round(sum(v["tics_ardiendo"] for v in V) / max(1, len(V)), 1),
           "juntos_3": round(100 * sum(s["juntos_3"] * s["tics_comunes"] / 100 for s in PS.values()) / max(1, sum(s["tics_comunes"] for s in PS.values())), 1) if PS else None,
           "juntos_8": round(100 * sum(s["juntos_8"] * s["tics_comunes"] / 100 for s in PS.values()) / max(1, sum(s["tics_comunes"] for s in PS.values())), 1) if PS else None,
           "juntos_3_media_por_semilla": round(st.mean(s["juntos_3"] for s in PS.values()), 1) if PS else None,
           "escapadas_largas": sum(s["escapadas_largas"] for s in PS.values()), "escapadas": sum(s["escapadas"] for s in PS.values()),
           "c_aceptado_por_los_dos": sum(s["c_aceptado_por_los_dos"] for s in PS.values()), "planes": dict(R["planes"]),
           "latencia": {k: (round(st.median([v["latencia"][k] for v in V if v["latencia"][k] is not None]), 2) if any(v["latencia"][k] is not None for v in V) else None) for k in ("ms16_mediana", "ms16_p95", "ms16_max", "tiempo_tic_mediana", "tiempo_tic_max")},
           "ms16_mas_de_un_tic_total": sum(v["latencia"]["ms16_mas_de_un_tic"] for v in V), "ms16_n_total": sum(v["latencia"]["n"] for v in V)}
    OUT[etiq] = {"resumen": res, "vidas": V, "por_semilla": PS, "aceptados": R["aceptados"]}
    print(f"### {etiq}: " + json.dumps(res, ensure_ascii=False))
# emparejado por semilla
if len(OUT) >= 2:
    base = "A4" if "A4" in OUT else list(OUT)[0]
    OUT["_emparejado"] = {}
    for etiq in OUT:
        if etiq == base or etiq.startswith("_"):
            continue
        E = {}
        for k in ("juntos_3", "escapadas_largas", "los_dos_vivos_al_final"):
            pares = [(OUT[etiq]["por_semilla"][s][k], OUT[base]["por_semilla"][s][k]) for s in OUT[etiq]["por_semilla"] if s in OUT[base]["por_semilla"]]
            E[k] = {"n": len(pares), "media_dif": round(st.mean(float(a) - float(b) for a, b in pares), 3) if pares else None, "gana": sum(1 for a, b in pares if a > b), "pierde": sum(1 for a, b in pares if a < b)}
        for k in ("tics", "comida", "ardiendo"):
            pares = []
            for s in OUT[etiq]["por_semilla"]:
                if s in OUT[base]["por_semilla"]:
                    for sl in ("s10", "s11"):
                        pares.append((OUT[etiq]["por_semilla"][s][sl][k], OUT[base]["por_semilla"][s][sl][k]))
            E[k] = {"n": len(pares), "media_dif": round(st.mean(a - b for a, b in pares), 1) if pares else None, "gana": sum(1 for a, b in pares if a > b), "pierde": sum(1 for a, b in pares if a < b)}
        OUT["_emparejado"][f"{etiq} - {base}"] = E
        print(f"### {etiq} - {base}: " + json.dumps(E, ensure_ascii=False))
json.dump(OUT, open(os.path.join(AQUI, "P6_16_medidas.json"), "w"), ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_16_medidas.json")
