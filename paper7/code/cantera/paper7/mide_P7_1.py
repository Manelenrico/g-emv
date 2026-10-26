"""[P7-1] El botiquin y el arco por dentro, y el diario de tres columnas sobre lo ya vivido (80 diarios A4 del seis). Solo lectura.

Definiciones (todas se calculan; ninguna cifra a mano):
  - DENTRO del circulo: dist euclidea de `pos` al `zona.center` <= `zona.radius` del mismo tic (comprobado contra el dano de zona:
    se cuenta en `R["zona_vs_dano"]` cuantos golpes de zona caen fuera por esta regla).
  - FASE: indice k (1-7) de `zone_schedule` con warn_tick <= t; 0 antes del primer aviso; "encogiendo" si shrink <= t < done.
  - USO DE BOTIQUIN: `use` sobre un slot con first_aid y `effects[channeling first_aid]` en t+1 (como en P7-0). COMPLETADO si el n
    del pack baja en done_tick+1; CANCELADO si no; SIN CERRAR si la vida acaba antes. t_corte = primer tic de (t, done_tick] con
    `damage_taken` no vacio (en los cancelados); sus `source` dicen de donde vino el dano.
  - POSICIONES DURANTE EL CANAL: `pos` en t..t_fin; se cuentan las distintas y las intenciones no-`none` emitidas con su resultado.
  - CASILLA SIN DANO ALCANZABLE (solo cortes por zona): pasos = ceil(dist - radius) (casillas hasta el borde, Chebyshev, sin muros);
    tics necesarios = pasos * coste_movimiento(speed 5) = 11 (mundo.py:216-217, 16 - SPD); alcanzable si tics necesarios <= t_corte - t.
  - TIEMPO INTENTANDO CURARSE EN EL FUEGO: tics por vida dentro de un canal de botiquin (t..t_corte o t_fin) estando FUERA del circulo.
  - MUERTE POR ANILLO: la vida acaba (ultimo tic del diario) y el ultimo dano registrado antes de acabar tiene source "zone".
  - ATAQUE SIN MUNICION: `attack` con arco o cerbatana en mano cuyo `action_result` en t+1 es `no_ammo`. Municion en la mochila =
    unidades de arrows (arco) / darts (cerbatana) en hand+pack en t. A la vista = `ve_items` con ese id en t. Contada por el hermano =
    el ultimo E2 del hermano en `chat` con <= 86 tics (oyente2.py:83-89) lista esa letra en su seccion I (parte2.py:76-81: letras por id
    ordenado: arrows='a', darts='f'). Lo que hacia el rival: `RADIOGRAFIA.honor.objetivo` da el asiento; "me pegaba" si hay
    `damage_taken.source == P<slot>` en los 120 tics anteriores (AGRESOR_VENTANA_S = 5 s); "se acercaba" si su distancia en t es menor
    que en t-24; si no, "nada". Golpe = `damage_dealt` sube en t+1.
  - DIARIO DE TRES COLUMNAS: una fila por uso de botiquin y por ataque con arco/cerbatana. SITUACION = variables que el cuerpo ya
    percibe en t (dentro/fuera, hp, dano recibido en los 24 y 120 tics anteriores, rivales a <= 5 casillas, distancia al mas cercano,
    municion en la mochila). IMAGINADO = lo que su prevision espera (decisor_zs.py:824: hp + heal del catalogo, tope hp_max;
    decisor_zs.py:852-856: dano del arma del catalogo, 14 arco / 4 cerbatana). PASO = exacto: hp en t_fin, n del pack, action_result,
    damage_dealt; inferido: "cura real" = hp(t_fin) - hp(t) + dano recibido en la ventana; "cancelado" = n no baja.
"""
import glob, json, math, os, re
from collections import Counter, defaultdict, deque

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
SERIES = ("P611_t1", "P611_t2", "P624_t1"); OUT = os.path.join(AQUI, "P7_1_medidas.json"); DIARIO = os.path.join(AQUI, "P7_1_diario.json")
COSTE_MOV = 16 - 5; VENT_CORTA = 24; VENT_LARGA = 120; EDAD_PARTE = 86; CERCA = 5
LETRA = {"bow": "a", "blowgun": "f"}; MUNI = {"bow": "arrows", "blowgun": "darts"}; DANO = {"bow": 14, "blowgun": 4}

def diarios():
    for s in SERIES:
        for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"{s}_A4_*"))):
            for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_*.art.log"))): yield s, os.path.basename(carp), f

def unidades(r):
    c = Counter(); h = r.get("hand") or {}
    if h.get("id") not in (None, "none"): c[h["id"]] += int(h.get("n") or 1)
    for s in r.get("pack") or []:
        if s: c[s["id"]] += int(s.get("n") or 1)
    return c

def dentro(r):
    z = r["zona"]; d = math.dist(r["pos"], z["center"]); return d <= z["radius"], d - z["radius"], z["radius"]

def fase(t, sched):
    k = 0; enc = False
    for i, (warn, shrink, done, r0, r1, dps) in enumerate(sched, 1):
        if t >= warn: k = i; enc = shrink <= t < done
    return k, enc

def rivales(r, mio, herm):
    out = []
    for a in r.get("ve_agentes") or []:
        if a.get("slot") in (mio, herm) or not a.get("pos"): continue
        out.append((a["slot"], math.dist(r["pos"], a["pos"]), a))
    return out

def vida(serie, carp, f):
    pc = None; sched = None; cat = None; buf = {}; orden = deque(); final = None; ultimo = None
    usos = []; pend_canal = []; ataques = []; pend_att = None; pend_use = None; fuego = 0; dano_final = None; chats = deque()
    zona_chk = [0, 0]; L = {"serie": serie, "carpeta": carp}
    for line in open(f):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "player_config": pc = r; sched = r["zone_schedule"]; continue
        if k == "catalogo": cat = {c["id"]: c for c in r["items"]}; continue
        if k == "final": final = r; continue
        if k != "tick": continue
        t = r["tick"]; mio = pc["slot"]; herm = pc["teammate_slot"]
        for d in r.get("damage_taken") or []:
            dano_final = (t, d.get("source"))
            if d.get("source") == "zone": zona_chk[0] += 1; zona_chk[1] += (not dentro(r)[0])
        for c in r.get("chat") or []:
            if c.get("from") == herm and c.get("channel") == "team" and str(c.get("text", "")).startswith("E2"): chats.append((c.get("tick", t), c["text"]))
        while chats and chats[0][0] < t - 2 * EDAD_PARTE: chats.popleft()
        # cierre de lo pendiente del tic anterior
        if pend_use and pend_use["t"] == t - 1:
            u = pend_use; pend_use = None
            ef = next((e for e in (r.get("effects") or []) if e.get("id") == "channeling" and e.get("item") == "first_aid"), None)
            if ef:
                u["done_tick"] = ef["done_tick"]; u["confirmado"] = True; pend_canal.append(u); usos.append(u)
        if pend_att and pend_att["t"] == t - 1:
            a = pend_att; pend_att = None
            a["resultado"] = r.get("action_result"); a["golpe"] = (r.get("damage_dealt") or 0) > a["_dd"]; a["dano_hecho"] = round((r.get("damage_dealt") or 0) - a["_dd"], 2); del a["_dd"]
            ataques.append(a)
        # canales abiertos: posiciones, corte, cierre
        for u in list(pend_canal):
            if u.get("t_corte") is None and (r.get("damage_taken") or []):
                u["t_corte"] = t; u["fuentes_corte"] = [d.get("source") for d in r["damage_taken"]]; u["hp_corte"] = r.get("hp"); u["dentro_corte"] = dentro(r)[0]
            # posiciones e intenciones SOLO mientras el canal vive: hasta el corte (cancelados) o hasta done_tick (completados)
            if u.get("t_corte") is None or t <= u["t_corte"]:
                if t <= u["done_tick"]:
                    u["_pos"].add(tuple(r["pos"]))
                    if t > u["t"] and r["intencion"].get("do") != "none": u["_intenciones"].append((r["intencion"].get("do"), r.get("action_result")))
                if not dentro(r)[0]: u["_tics_fuera"] += 1
            if t >= u["done_tick"] + 1:
                u["dentro_fin"] = dentro(r)[0]
                u["t_fin"] = t; u["hp_fin"] = r.get("hp"); u["n_despues"] = unidades(r)["first_aid"]
                # COMPLETADO = el n baja Y no hubo dano antes de done_tick (el dano corta el canal; si el n baja con dano en medio,
                # el botiquin salio del zurron por otra causa: soltado o cogido/soltado; se marca aparte)
                u["n_bajo"] = u["n_despues"] < u["n_antes"]; u["dano_antes_de_done"] = bool(u.get("t_corte") and u["t_corte"] <= u["done_tick"])
                u["completado"] = u["n_bajo"] and not u["dano_antes_de_done"]
                u["dano_ventana"] = round(u["_dano_v"], 2); u["cura_real"] = round((u["hp_fin"] - u["hp"]) + u["_dano_v"], 2)
                u["posiciones_distintas"] = len(u["_pos"]); u["movio"] = len(u["_pos"]) > 1; u["intenciones_en_canal"] = dict(Counter(f"{a}/{b}" for a, b in u["_intenciones"]))
                u["tics_fuera_en_canal"] = u["_tics_fuera"]
                if u.get("t_corte") and "zone" in (u.get("fuentes_corte") or []):
                    pasos = max(0, math.ceil(u["dist_borde"])); u["pasos_hasta_dentro"] = pasos; u["tics_necesarios"] = pasos * COSTE_MOV
                    u["tics_hasta_corte"] = u["t_corte"] - u["t"]; u["casilla_sin_dano_alcanzable"] = (pasos > 0 and pasos * COSTE_MOV <= u["t_corte"] - u["t"])
                for kk in ("_pos", "_intenciones", "_dano_v", "_tics_fuera"): u.pop(kk, None)
                pend_canal.remove(u)
            else:
                u["_dano_v"] += sum(float(d.get("amount") or 0) for d in (r.get("damage_taken") or []))
        # este tic: intencion
        it = r["intencion"] or {}; un = unidades(r)
        if it.get("do") == "use":
            s = it.get("slot"); pk = r.get("pack") or []
            if s is not None and s < len(pk) and pk[s] and pk[s]["id"] == "first_aid":
                den, db, rad = dentro(r); fk, enc = fase(t, sched); rv = rivales(r, mio, herm)
                prev = [buf[u] for u in range(t - VENT_LARGA, t) if u in buf]
                d24 = sum(float(d.get("amount") or 0) for q in prev if q["tick"] >= t - VENT_CORTA for d in (q.get("damage_taken") or []))
                d120 = sum(float(d.get("amount") or 0) for q in prev for d in (q.get("damage_taken") or []))
                f120 = sorted({d.get("source") for q in prev for d in (q.get("damage_taken") or [])})
                pend_use = {"t": t, "hp": r.get("hp"), "dentro": den, "dist_borde": round(db, 2), "radio": rad, "fase": fk, "encogiendo": enc,
                            "rivales_vistos": len(rv), "rival_min_dist": round(min((d for _, d, _ in rv), default=-1), 2), "rivales_a_5": sum(1 for _, d, _ in rv if d <= CERCA),
                            "dano_prev_24": round(d24, 2), "dano_prev_120": round(d120, 2), "fuentes_prev_120": f120, "n_antes": un["first_aid"],
                            "hp_imaginado": min(100, (r.get("hp") or 0) + cat["first_aid"]["heal"]), "_pos": {tuple(r["pos"])}, "_intenciones": [], "_dano_v": 0.0, "_tics_fuera": 0,
                            "pos": r["pos"], "elegido": (r.get("RADIOGRAFIA") or {}).get("elegido")}
        elif it.get("do") == "attack" and (r.get("hand") or {}).get("id") in ("bow", "blowgun"):
            arma = r["hand"]["id"]; den, db, rad = dentro(r); fk, enc = fase(t, sched); rv = rivales(r, mio, herm)
            hon = ((r.get("RADIOGRAFIA") or {}).get("honor") or {}); obj = hon.get("objetivo")
            prev = [buf[u] for u in range(t - VENT_LARGA, t) if u in buf]
            me_pego = any(d.get("source") == f"P{obj}" for q in prev for d in (q.get("damage_taken") or [])) if obj is not None else None
            d_obj = next((d for s_, d, _ in rv if s_ == obj), None)
            q24 = buf.get(t - VENT_CORTA); d_obj_24 = None
            if q24 is not None and obj is not None:
                ag = next((a for a in (q24.get("ve_agentes") or []) if a.get("slot") == obj and a.get("pos")), None)
                d_obj_24 = math.dist(q24["pos"], ag["pos"]) if ag else None
            acerca = (d_obj is not None and d_obj_24 is not None and d_obj < d_obj_24 - 0.5)
            parte = next((txt for tk, txt in reversed(chats) if t - tk <= EDAD_PARTE), None)
            secI = re.search(r"\sI([A-Za-z0-9,]+)", parte) if parte else None
            contada = bool(secI and re.search(LETRA[arma] + r"\d+,\d+", secI.group(1)))
            pend_att = {"t": t, "arma": arma, "hp": r.get("hp"), "dentro": den, "fase": fk, "municion_mochila": un[MUNI[arma]], "municion_a_la_vista": sum(int(i.get("n") or 1) for i in (r.get("ve_items") or []) if i["id"] == MUNI[arma]),
                        "municion_contada_por_el_hermano": contada, "objetivo": obj, "era_agresor": hon.get("era_agresor"), "defensa_pareja": hon.get("defensa_pareja"), "dano_recibido_de_el": hon.get("dano_recibido_de_el"),
                        "rival_me_pego_120": me_pego, "rival_dist": round(d_obj, 2) if d_obj is not None else None, "rival_se_acercaba": acerca,
                        "rival_hacia": ("me pegaba" if me_pego else ("se acercaba" if acerca else "nada")), "rivales_a_5": sum(1 for _, d, _ in rv if d <= CERCA),
                        "dano_prev_24": round(sum(float(d.get("amount") or 0) for q in prev if q["tick"] >= t - VENT_CORTA for d in (q.get("damage_taken") or [])), 2),
                        "dano_imaginado": DANO[arma], "attack_ready_in": r.get("attack_ready_in"), "_dd": (r.get("damage_dealt") or 0), "pack": r.get("pack"), "hand": r.get("hand")}
        buf[t] = r; orden.append(t)
        while orden and orden[0] < t - VENT_LARGA - 2: buf.pop(orden.popleft(), None)
        ultimo = r
    for u in pend_canal:
        u["completado"] = None; u["nota"] = "la vida acaba antes de cerrar el canal"; u["posiciones_distintas"] = len(u["_pos"]); u["tics_fuera_en_canal"] = u["_tics_fuera"]
        for kk in ("_pos", "_intenciones", "_dano_v", "_tics_fuera"): u.pop(kk, None)
        usos.append(u) if u not in usos else None
    # tiempo en el fuego: tics en canal fuera del circulo, hasta el corte si lo hubo
    fuego = 0
    for u in usos:
        if u.get("t_corte"): fuego += min(u.get("tics_fuera_en_canal", 0), u["t_corte"] - u["t"] + 1)
        else: fuego += u.get("tics_fuera_en_canal", 0)
    T_fin = ultimo["tick"] if ultimo else 0
    muerte_anillo = bool(final and final.get("reason") == "eliminated" and dano_final and dano_final[1] == "zone" and T_fin - dano_final[0] <= 30)
    intentos_10s = [u["t"] for u in usos if u["t"] >= T_fin - 240]
    L.update({"slot": pc["slot"], "ticks": T_fin, "final": {k: (final or {}).get(k) for k in ("placement", "reason", "match_ticks")}, "muerte_por_anillo": muerte_anillo, "ultimo_dano": dano_final,
              "usos_botiquin": usos, "tics_curandose_en_el_fuego": fuego, "intentos_botiquin_ultimos_10s": len(intentos_10s),
              "ataques_arco_cerbatana": ataques, "zona_vs_dano": zona_chk})
    return L

def q(v, p):
    if not v: return None
    v = sorted(v); k = (len(v) - 1) * p; i = int(k); f = k - i
    return v[i] if i + 1 >= len(v) else round(v[i] + (v[i + 1] - v[i]) * f, 2)
def tri(v): return {"n": len(v), "mediana": q(v, .5), "p10": q(v, .1), "p90": q(v, .9), "total": sum(v) if v else 0}

if __name__ == "__main__":
    vidas = [vida(*x) for x in diarios()]
    U = [dict(u, vida=L["carpeta"] + "/" + str(L["slot"])) for L in vidas for u in L["usos_botiquin"]]
    A = [dict(a, vida=L["carpeta"] + "/" + str(L["slot"])) for L in vidas for a in L["ataques_arco_cerbatana"]]
    R = {"vidas": len(vidas), "zona_vs_dano": [sum(L["zona_vs_dano"][0] for L in vidas), sum(L["zona_vs_dano"][1] for L in vidas)]}
    # 1 · botiquin
    cer = [u for u in U if u.get("completado") is not None]
    R["botiquin"] = {"usos": len(U), "cerrados": len(cer), "completados": sum(1 for u in cer if u["completado"]), "cancelados": sum(1 for u in cer if not u["completado"]), "sin_cerrar": len(U) - len(cer),
                     "posiciones_distintas": dict(Counter(u.get("posiciones_distintas") for u in U if u.get("completado") is not None)), "movio_por_resultado": {k: dict(Counter(u.get("movio") for u in U if u.get("completado") is (k == "completado"))) for k in ("completado", "cancelado")},
                     "fuentes_corte_por_dentro": {k: dict(Counter(s_ for u in U if u.get("completado") is False and u.get("t_corte") and u["dentro"] is (k == "dentro") for s_ in u["fuentes_corte"])) for k in ("dentro", "fuera")},
                     "completados_fuera_que_acaban_dentro": sum(1 for u in U if u.get("completado") and not u["dentro"] and u.get("dentro_fin")),
                     "cancelados_dentro_por_zona_encogiendo": sum(1 for u in U if u.get("completado") is False and u["dentro"] and "zone" in (u.get("fuentes_corte") or [])), "intenciones_en_canal": dict(sum((Counter(u.get("intenciones_en_canal") or {}) for u in U), Counter())),
                     "por_dentro_fuera": {}, "por_fase": {}, "fuentes_corte": dict(Counter(s for u in U if u.get("completado") is False and u.get("t_corte") for s in u["fuentes_corte"])),
                     "n_bajo_con_dano_en_canal": [{"vida": u["vida"], "t": u["t"], "t_corte_menos_done": u["t_corte"] - u["done_tick"], "fuentes": u["fuentes_corte"], "intenciones": u.get("intenciones_en_canal")} for u in U if u.get("n_bajo") and u.get("dano_antes_de_done")],
                     "cancelados_con_n_bajando": sum(1 for u in U if u.get("completado") is False and u.get("n_bajo")),
                     "corte_por_zona_alcanzable": dict(Counter(("alcanzable" if u.get("casilla_sin_dano_alcanzable") else ("no alcanzable" if u.get("pasos_hasta_dentro") else "estaba dentro (el circulo se movio o dano de otro)")) for u in U if u.get("completado") is False and u.get("t_corte") and "zone" in u["fuentes_corte"])),
                     "tics_hasta_corte": tri([u["t_corte"] - u["t"] for u in U if u.get("completado") is False and u.get("t_corte")]), "pasos_hasta_dentro": tri([u["pasos_hasta_dentro"] for u in U if u.get("pasos_hasta_dentro") is not None]),
                     "tiempo_en_el_fuego_por_vida": tri([L["tics_curandose_en_el_fuego"] for L in vidas]), "vidas_con_fuego": sum(1 for L in vidas if L["tics_curandose_en_el_fuego"] > 0),
                     "muertes_por_anillo": sum(1 for L in vidas if L["muerte_por_anillo"]), "muertes_anillo_con_intento_10s": sum(1 for L in vidas if L["muerte_por_anillo"] and L["intentos_botiquin_ultimos_10s"] > 0),
                     "intentos_10s_en_muertes_anillo": tri([L["intentos_botiquin_ultimos_10s"] for L in vidas if L["muerte_por_anillo"]]), "razones_final": dict(Counter(L["final"]["reason"] for L in vidas)),
                     "rivales_vistos_al_usar": dict(Counter(min(u["rivales_vistos"], 3) for u in U)), "rival_min_dist": tri([u["rival_min_dist"] for u in U if u["rival_min_dist"] >= 0]), "hp_al_usar": tri([u["hp"] for u in U])}
    for nombre, key in (("dentro", lambda u: "dentro" if u["dentro"] else "fuera"), ("fase", lambda u: str(u["fase"]) + ("e" if u["encogiendo"] else ""))):
        g = defaultdict(Counter)
        for u in cer: g[key(u)]["completado" if u["completado"] else "cancelado"] += 1
        R["botiquin"]["por_" + ("dentro_fuera" if nombre == "dentro" else "fase")] = {k: dict(v) for k, v in g.items()}
    # 2 · arco y cerbatana
    R["arco"] = {}
    for arma in ("bow", "blowgun"):
        AA = [a for a in A if a["arma"] == arma]; na = [a for a in AA if a["resultado"] == "no_ammo"]
        R["arco"][arma] = {"ataques": len(AA), "resultados": dict(Counter(a["resultado"] for a in AA)), "golpes": sum(1 for a in AA if a["golpe"]),
                           "no_ammo_con_municion_en_mochila": sum(1 for a in na if a["municion_mochila"] > 0), "no_ammo_sin_municion": sum(1 for a in na if a["municion_mochila"] == 0),
                           "ok_con_municion": sum(1 for a in AA if a["resultado"] == "ok" and a["municion_mochila"] > 0), "ok_sin_municion": sum(1 for a in AA if a["resultado"] == "ok" and a["municion_mochila"] == 0),
                           "no_ammo_municion_a_la_vista": sum(1 for a in na if a["municion_a_la_vista"] > 0), "no_ammo_contada_por_el_hermano": sum(1 for a in na if a["municion_contada_por_el_hermano"]),
                           "no_ammo_rival_hacia": dict(Counter(a["rival_hacia"] for a in na)), "no_ammo_era_agresor": dict(Counter(a["era_agresor"] for a in na)), "no_ammo_defensa_pareja": dict(Counter(a["defensa_pareja"] for a in na)),
                           "no_ammo_rival_dist": tri([a["rival_dist"] for a in na if a["rival_dist"] is not None]), "no_ammo_dentro": dict(Counter(a["dentro"] for a in na)),
                           "tics_no_ammo_por_vida": tri([sum(1 for a in L["ataques_arco_cerbatana"] if a["arma"] == arma and a["resultado"] == "no_ammo") for L in vidas]),
                           "vidas_con_no_ammo": sum(1 for L in vidas if any(a["arma"] == arma and a["resultado"] == "no_ammo" for a in L["ataques_arco_cerbatana"])),
                           "fraccion_vida_no_ammo": tri([sum(1 for a in L["ataques_arco_cerbatana"] if a["arma"] == arma and a["resultado"] == "no_ammo") / L["ticks"] for L in vidas if any(a["arma"] == arma for a in L["ataques_arco_cerbatana"])]),
                           "casos_no_ammo_con_municion": [{k: a[k] for k in ("vida", "t", "hand", "pack", "municion_mochila", "attack_ready_in")} for a in na if a["municion_mochila"] > 0][:10]}
    # 3 · diario de tres columnas
    def fila_bot(u):
        return {"vida": u["vida"], "t": u["t"], "situacion": {"dentro": u["dentro"], "dist_borde": u["dist_borde"], "hp": u["hp"], "dano_prev_24": u["dano_prev_24"], "dano_prev_120": u["dano_prev_120"], "rivales_a_5": u["rivales_a_5"], "rival_min_dist": u["rival_min_dist"], "fase": u["fase"], "encogiendo": u["encogiendo"]},
                "imaginado": {"hp_esperado": u["hp_imaginado"], "cura_esperada": u["hp_imaginado"] - u["hp"], "fuente": "decisor_zs.py:824 (hp + heal del catalogo, tope 100)"},
                "paso": {"resultado": ("completado" if u.get("completado") else ("cancelado" if u.get("completado") is False else "sin cerrar")), "hp_fin": u.get("hp_fin"), "cura_real": u.get("cura_real"), "dano_ventana": u.get("dano_ventana"), "t_corte": u.get("t_corte"), "fuentes_corte": u.get("fuentes_corte"), "movio": u.get("movio"), "dentro_fin": u.get("dentro_fin"), "posiciones_distintas": u.get("posiciones_distintas")},
                "exacto": ["hp", "n del pack", "effects", "damage_taken"], "inferido": ["cura_real = hp_fin - hp + dano en la ventana", "cancelado = hubo dano antes de done_tick, o el n no baja en done_tick+1"]}
    def fila_arco(a):
        return {"vida": a["vida"], "t": a["t"], "arma": a["arma"], "situacion": {"dentro": a["dentro"], "hp": a["hp"], "dano_prev_24": a["dano_prev_24"], "rivales_a_5": a["rivales_a_5"], "rival_dist": a["rival_dist"], "municion_mochila": a["municion_mochila"], "municion_a_la_vista": a["municion_a_la_vista"], "municion_contada_por_el_hermano": a["municion_contada_por_el_hermano"], "rival_hacia": a["rival_hacia"], "fase": a["fase"]},
                "imaginado": {"dano_esperado": a["dano_imaginado"], "fuente": "decisor_zs.py:852-856 (dano del catalogo; a distancia sin multiplicador)"},
                "paso": {"resultado": a["resultado"], "golpe": a["golpe"], "dano_hecho": a["dano_hecho"]}, "exacto": ["action_result", "damage_dealt"], "inferido": ["golpe = damage_dealt sube en t+1 (no dice a quien)"]}
    diario = {"botiquin": [fila_bot(u) for u in U], "arco_cerbatana": [fila_arco(a) for a in A]}
    json.dump(diario, open(DIARIO, "w"), indent=1, ensure_ascii=False)
    # 4 · lo imaginado contra lo que paso, por situacion
    def grupos(filas, claves):
        out = {}
        for nombre, fn in claves.items():
            g = defaultdict(Counter)
            for f in filas: g[str(fn(f))][f["paso"]["resultado"] if "resultado" in f["paso"] else ""] += 1
            out[nombre] = {k: dict(v) for k, v in sorted(g.items())}
        return out
    bot = [f for f in diario["botiquin"] if f["paso"]["resultado"] != "sin cerrar"]
    R["aprender"] = {"botiquin": grupos(bot, {"dentro": lambda f: "dentro" if f["situacion"]["dentro"] else "fuera", "dano_prev_24": lambda f: "con dano 24" if f["situacion"]["dano_prev_24"] > 0 else "sin dano 24",
                                             "dano_prev_120": lambda f: "con dano 120" if f["situacion"]["dano_prev_120"] > 0 else "sin dano 120", "rivales_a_5": lambda f: "rival a 5" if f["situacion"]["rivales_a_5"] > 0 else "sin rival a 5",
                                             "fase": lambda f: f["situacion"]["fase"], "dentro_y_dano24": lambda f: ("dentro" if f["situacion"]["dentro"] else "fuera") + " / " + ("con dano 24" if f["situacion"]["dano_prev_24"] > 0 else "sin dano 24"),
                                             "hp_banda": lambda f: "hp<50" if f["situacion"]["hp"] < 50 else "hp>=50",
                                             "dentro_y_rival5": lambda f: ("dentro" if f["situacion"]["dentro"] else "fuera") + " / " + ("rival a 5" if f["situacion"]["rivales_a_5"] > 0 else "sin rival a 5"),
                                             "fuera_y_movio": lambda f: ("fuera" if not f["situacion"]["dentro"] else "dentro") + " / " + ("se movio" if f["paso"]["movio"] else "quieto"),
                                             "dentro_sin_rival5_sin_dano24": lambda f: "dentro, sin rival a 5, sin dano 24" if (f["situacion"]["dentro"] and f["situacion"]["rivales_a_5"] == 0 and f["situacion"]["dano_prev_24"] == 0) else "resto"}),
                     "botiquin_cura_real": {k: tri([f["paso"]["cura_real"] for f in bot if (f["situacion"]["dentro"] == (k == "dentro"))]) for k in ("dentro", "fuera")},
                     "arco_cerbatana": {arma: grupos([f for f in diario["arco_cerbatana"] if f["arma"] == arma], {"municion": lambda f: "con municion" if f["situacion"]["municion_mochila"] > 0 else "sin municion", "rival_hacia": lambda f: f["situacion"]["rival_hacia"],
                                             "dentro": lambda f: "dentro" if f["situacion"]["dentro"] else "fuera", "rivales_a_5": lambda f: "rival a 5" if f["situacion"]["rivales_a_5"] > 0 else "sin rival a 5", "dano_prev_24": lambda f: "con dano 24" if f["situacion"]["dano_prev_24"] > 0 else "sin dano 24",
                                             "a_la_vista": lambda f: "municion a la vista" if f["situacion"]["municion_a_la_vista"] > 0 else "sin municion a la vista", "contada": lambda f: "contada por el hermano" if f["situacion"]["municion_contada_por_el_hermano"] else "no contada"}) for arma in ("bow", "blowgun")},
                     "arco_dano_hecho_ok": {arma: tri([f["paso"]["dano_hecho"] for f in diario["arco_cerbatana"] if f["arma"] == arma and f["paso"]["resultado"] == "ok"]) for arma in ("bow", "blowgun")}}
    # 5 · filas por vida y situacion
    def por_vida(filas, fn):
        g = defaultdict(lambda: Counter())
        for f in filas: g[str(fn(f))][f["vida"]] += 1
        todas = [L["carpeta"] + "/" + str(L["slot"]) for L in vidas]
        return {k: tri([c.get(v, 0) for v in todas]) for k, c in g.items()} | {"todas": tri([sum(c.get(v, 0) for c in g.values()) for v in todas])}
    R["filas_por_vida"] = {"botiquin": {"dentro_fuera": por_vida(diario["botiquin"], lambda f: "dentro" if f["situacion"]["dentro"] else "fuera"), "dano_prev_24": por_vida(diario["botiquin"], lambda f: "con dano 24" if f["situacion"]["dano_prev_24"] > 0 else "sin dano 24")},
                           "bow": {"municion": por_vida([f for f in diario["arco_cerbatana"] if f["arma"] == "bow"], lambda f: "con municion" if f["situacion"]["municion_mochila"] > 0 else "sin municion")},
                           "blowgun": {"municion": por_vida([f for f in diario["arco_cerbatana"] if f["arma"] == "blowgun"], lambda f: "con municion" if f["situacion"]["municion_mochila"] > 0 else "sin municion")}}
    json.dump({"resumen": R, "vidas": vidas}, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(json.dumps(R, indent=1, ensure_ascii=False)[:12000])
