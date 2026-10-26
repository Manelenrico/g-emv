"""[P7-0] Inventario de las cosas: cuanto se las encuentra el cuerpo A4 del seis y que pasa al usarlas.

Lee los 80 diarios A4 del seis (40 semillas: P611_t1, P611_t2 = las 20 de P6-23; P624_t1 = las 20 nuevas de P6-24;
2 asientos por partida), uno a uno, registro a registro (sin cargar el diario entero). Solo lectura.

Definiciones (declaradas aqui, no en el informe):
  - VER: un objeto se "ve" cuando aparece en `ve_items` (id, n, pos). Se cuentan (a) tics con el objeto a la vista y
    (b) montones distintos = pares (id, pos) distintos a lo largo de la vida. Primer encuentro = primer tic en que
    aparece. Los arbustos van por `ve_bushes` (pos, charges). Las armas/prendas de otros, por `ve_agentes[].hand/body`.
  - COGER: `intencion.do == "pickup"` en el tic t, y en el registro t+1 el inventario (hand, pack, body) tiene algo
    que en t no tenia (id nuevo o n mayor): eso es lo cogido. El diario no apunta que se cogio; se infiere del
    inventario. `action_result` del tic t es el resultado de la accion emitida en t-1 (comprobado: pickup en 592,
    `hand` cambia en 593, `no_target` en 594 para el pickup repetido de 593).
  - USAR: `intencion.do == "use"` con `slot` = indice del `pack` (comprobado: use/s0 con pack[0]=first_aid ->
    efecto channeling first_aid). El objeto usado es pack[slot] en t. Confirmacion por lo que sigue: consumible ->
    aparece `effects[channeling, item]` en t+1; COMPLETADO si en done_tick+1 el n del objeto en el pack ha bajado
    (o el objeto ha desaparecido); CANCELADO si no (el canal se corta con cualquier dano). Arma -> `hand` en t+1 es
    el objeto (use = intercambiar mano<->zurron). Prenda -> `body` en t+1 es el objeto.
  - SOLTAR: `intencion.do == "drop"` con slot; confirmado si pack[slot] cambia en t+1. DAR no existe como accion
    del juego: lo mas parecido es soltar con el hermano a <= 2 casillas (se cuenta aparte, como proxy declarado).
  - ATACAR: `intencion.do == "attack"` con lo que hay en `hand`; golpe confirmado si `damage_dealt` sube en t+1.
  - LO QUE PASA AL USAR (punto 4): para cada uso de consumible, hp en t, hp en t_fin = done_tick + 1, dano recibido
    en (t, t_fin] (`damage_taken[].amount`), delta_neto = hp(t_fin) - hp(t) + dano recibido. Ventana = el canal del
    catalogo (use_ticks: 48 first_aid, 24 rations) + 1 tic. Si la vida acaba antes, se marca.
"""
import glob, hashlib, json, os, statistics, sys
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
SERIES = ("P611_t1", "P611_t2", "P624_t1")
OUT = os.path.join(AQUI, "P7_0_medidas.json")

def diarios():
    for s in SERIES:
        for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"{s}_A4_*"))):
            for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_*.art.log"))):
                yield s, os.path.basename(carp), f

def inv(r):
    """(hand_id, hand_n, pack [(id,n)|None], body_id) de un registro tick."""
    h = r.get("hand") or {}
    hid = h.get("id") if h.get("id") not in (None, "none") else None
    hn = int(h.get("n") or 1) if hid else 0
    pack = [((s.get("id"), int(s.get("n") or 1)) if s else None) for s in (r.get("pack") or [])]
    b = r.get("body"); bid = (b.get("id") if isinstance(b, dict) else b) or None
    return hid, hn, pack, bid

def unidades(r):
    hid, hn, pack, bid = inv(r); c = Counter()
    if hid: c[hid] += hn
    for s in pack:
        if s: c[s[0]] += s[1]
    if bid: c[bid] += 1
    return c

def vida(serie, carp, f):
    cat = None; pc = None; T_prev = None; L = {"serie": serie, "carpeta": carp, "archivo": os.path.relpath(f, RAIZ)}
    ve_tics = Counter(); montones = defaultdict(set); primer_ve = {}; bush_pos = set(); primer_bush = None
    ajenos = defaultdict(set); regalos = Counter(); regalos_mios = Counter()
    coge = []; usa = []; suelta = []; ataca = []; pend_pick = []; pend_use = []; pend_drop = []; pend_att = []
    canales = []  # usos de consumible pendientes de cerrar (done_tick)
    efectos = Counter(); ultimo_tick = 0; hp_por_tic = {}; dmg_por_tic = {}; final = None; fallos_pick = 0
    n_ticks = 0
    puesto = Counter(); en_mano = Counter(); largo_pack = defaultdict(Counter); fuentes = Counter(); dano_fuente = Counter()
    episodios = {"poison": [], "netted": []}; abierto = {}; fallos_causa = Counter(); fallos_arbusto = 0; fallos_con_objeto = 0
    with open(f) as fh:
        for line in fh:
            try: r = json.loads(line)
            except Exception: continue
            k = r.get("k")
            if k == "catalogo": cat = r["items"]; L["catalogo_md5"] = hashlib.md5(json.dumps(cat, sort_keys=True).encode()).hexdigest(); continue
            if k == "player_config": pc = r; continue
            if k == "final": final = r; continue
            if k != "tick": continue
            t = r["tick"]; n_ticks += 1; ultimo_tick = t; hp_por_tic[t] = r.get("hp"); dmg_por_tic[t] = sum(float(d.get("amount") or 0) for d in (r.get("damage_taken") or []))
            for it in r.get("ve_items") or []:
                ve_tics[it["id"]] += 1; montones[it["id"]].add(tuple(it["pos"])); primer_ve.setdefault(it["id"], t)
            for b in r.get("ve_bushes") or []:
                bush_pos.add(tuple(b["pos"])); primer_bush = primer_bush if primer_bush is not None else t
            for a in r.get("ve_agentes") or []:
                if a.get("slot") == (pc or {}).get("slot"): continue
                if a.get("hand") and a["hand"] != "none": ajenos[a["hand"]].add(a["slot"])
                if a.get("body"): ajenos[a["body"]].add(a["slot"])
            for e in r.get("eventos") or []:
                if isinstance(e, dict) and e.get("type") == "gift_landed":
                    regalos[e.get("item")] += 1
                    if e.get("slot") == (pc or {}).get("slot"): regalos_mios[e.get("item")] += 1
            for e in r.get("effects") or []:
                efectos[e.get("id")] += 1
            hid0, hn0, pack0, bid0 = inv(r)
            puesto[bid0 or "nada"] += 1; en_mano[hid0 or "nada"] += 1; largo_pack[bid0 or "nada"][len(pack0)] += 1
            for d in r.get("damage_taken") or []:
                fuentes[d.get("source")] += 1; dano_fuente[d.get("source")] += float(d.get("amount") or 0)
            ids_ef = {e.get("id") for e in (r.get("effects") or [])}
            for nombre in ("poison", "netted"):
                if nombre in ids_ef and nombre not in abierto: abierto[nombre] = {"t0": t, "hp0": r.get("hp")}
                if nombre not in ids_ef and nombre in abierto:
                    ep = abierto.pop(nombre); episodios[nombre].append({"t0": ep["t0"], "t1": t, "largo": t - ep["t0"], "hp0": ep["hp0"], "hp1": r.get("hp")})
            # cierre de lo pendiente del tic anterior (t-1 -> este registro es "t+1" de aquello)
            if T_prev is not None and T_prev["tick"] == t - 1:
                tp = T_prev; up, un = unidades(tp), unidades(r)
                it_p = tp.get("intencion") or {}
                if it_p.get("do") == "pickup":
                    gan = {i: un[i] - up[i] for i in un if un[i] > up[i]}
                    if gan:
                        en_arbusto = tuple(tp["pos"]) in bush_pos
                        for i, n in gan.items(): coge.append({"t": tp["tick"], "id": i, "n": n, "en_arbusto": en_arbusto})
                    else:
                        fallos_pick += 1; fallos_causa[r.get("action_result")] += 1
                        if tuple(tp["pos"]) in bush_pos: fallos_arbusto += 1
                        if any(tuple(i["pos"]) == tuple(tp["pos"]) for i in (tp.get("ve_items") or [])): fallos_con_objeto += 1
                elif it_p.get("do") == "use":
                    s = it_p.get("slot"); hid, hn, pack, bid = inv(tp)
                    obj = pack[s][0] if (s is not None and s < len(pack) and pack[s]) else None
                    kind = next((c["kind"] for c in cat if c["id"] == obj), None) if obj else None
                    u = {"t": tp["tick"], "id": obj, "kind": kind, "slot": s, "hp": tp.get("hp"), "confirmado": False,
                         "elegido": (tp.get("RADIOGRAFIA") or {}).get("elegido"), "fase": tp.get("phase"), "radio_zona": (tp.get("zona") or {}).get("radius")}
                    hid1, hn1, pack1, bid1 = inv(r)
                    if kind == "ikConsumable":
                        ef = next((e for e in (r.get("effects") or []) if e.get("id") == "channeling" and e.get("item") == obj), None)
                        if ef:
                            u["confirmado"] = True; u["done_tick"] = ef.get("done_tick"); u["n_antes"] = up[obj]
                            canales.append(u)
                    elif kind in ("ikMelee", "ikRanged", "ikThrown"):
                        u["confirmado"] = (hid1 == obj)
                    elif kind == "ikGear":
                        u["confirmado"] = (bid1 == obj)
                    usa.append(u)
                elif it_p.get("do") == "drop":
                    s = it_p.get("slot"); hid, hn, pack, bid = inv(tp); hid1, hn1, pack1, bid1 = inv(r)
                    obj = pack[s][0] if (s is not None and s < len(pack) and pack[s]) else None
                    herm = next((a for a in (tp.get("ve_agentes") or []) if a.get("slot") == (pc or {}).get("teammate_slot")), None)
                    dh = max(abs(herm["pos"][0] - tp["pos"][0]), abs(herm["pos"][1] - tp["pos"][1])) if herm and herm.get("pos") else None
                    suelta.append({"t": tp["tick"], "id": obj, "confirmado": (s is not None and s < len(pack) and pack1[s] != pack[s]), "dist_hermano": dh})
                elif it_p.get("do") == "attack":
                    hid, hn, pack, bid = inv(tp)
                    ataca.append({"t": tp["tick"], "arma": hid or "manos", "golpe": (r.get("damage_dealt") or 0) > (tp.get("damage_dealt") or 0), "res": r.get("action_result"),
                                  "municion": sum(n for i, n in up.items() if i in ("arrows", "darts"))})
            # cierre de canales cuyo done_tick+1 es este tic
            for u in [u for u in canales if u.get("done_tick") is not None and t >= u["done_tick"] + 1]:
                u["t_fin"] = t; u["hp_fin"] = r.get("hp"); u["n_despues"] = unidades(r)[u["id"]]
                u["completado"] = u["n_despues"] < u["n_antes"]
                u["dano_ventana"] = sum(v for tt, v in dmg_por_tic.items() if u["t"] < tt <= t)
                u["delta_neto"] = (u["hp_fin"] - u["hp"]) + u["dano_ventana"]
                canales.remove(u)
            T_prev = r
            # poda del historial de dano (ventana maxima 60 tics)
            for tt in [tt for tt in dmg_por_tic if tt < t - 60]: del dmg_por_tic[tt]; hp_por_tic.pop(tt, None)
    for u in canales: u["t_fin"] = None; u["completado"] = None; u["nota"] = "la vida acaba antes de cerrar el canal"
    L.update({"slot": (pc or {}).get("slot"), "ticks": n_ticks, "ultimo_tick": ultimo_tick, "final": {k: (final or {}).get(k) for k in ("placement", "reason", "match_ticks", "kills")},
              "ve_tics": dict(ve_tics), "montones": {i: len(p) for i, p in montones.items()}, "primer_ve": primer_ve,
              "arbustos_vistos": len(bush_pos), "primer_arbusto": primer_bush, "ajenos": {i: len(s) for i, s in ajenos.items()},
              "regalos_vistos": dict(regalos), "regalos_mios": dict(regalos_mios), "efectos": dict(efectos),
              "coge": coge, "fallos_pickup": fallos_pick, "fallos_causa": dict(fallos_causa), "fallos_en_arbusto": fallos_arbusto, "fallos_con_objeto_en_la_casilla": fallos_con_objeto,
              "usa": usa, "suelta": suelta, "ataca": ataca, "tics_puesto": dict(puesto), "tics_en_mano": dict(en_mano),
              "largo_pack_por_prenda": {k: dict(v) for k, v in largo_pack.items()}, "fuentes_dano": dict(fuentes), "dano_por_fuente": {k: round(v, 2) for k, v in dano_fuente.items()},
              "episodios": episodios})
    return L, cat

def q(v, p):
    if not v: return None
    v = sorted(v); k = (len(v) - 1) * p; i = int(k); f = k - i
    return v[i] if i + 1 >= len(v) else v[i] + (v[i + 1] - v[i]) * f

def resumen(vidas, cat):
    ids = [c["id"] for c in cat]; R = {"vidas": len(vidas), "por_objeto": {}}
    for i in ids + ["berry_bush", "manos"]:
        ve = [L["montones"].get(i, 0) for L in vidas] if i != "berry_bush" else [L["arbustos_vistos"] for L in vidas]
        tics = [L["ve_tics"].get(i, 0) for L in vidas]
        coge = [sum(c["n"] for c in L["coge"] if c["id"] == i) for L in vidas]
        usos_conf = [sum(1 for u in L["usa"] if u["id"] == i and u["confirmado"]) for L in vidas]
        usos_int = [sum(1 for u in L["usa"] if u["id"] == i) for L in vidas]
        compl = [sum(1 for u in L["usa"] if u["id"] == i and u.get("completado")) for L in vidas]
        ataques = [sum(1 for a in L["ataca"] if a["arma"] == i) for L in vidas]
        golpes = [sum(1 for a in L["ataca"] if a["arma"] == i and a["golpe"]) for L in vidas]
        suelta = [sum(1 for s in L["suelta"] if s["id"] == i and s["confirmado"]) for L in vidas]
        da = [sum(1 for s in L["suelta"] if s["id"] == i and s["confirmado"] and s["dist_hermano"] is not None and s["dist_hermano"] <= 2) for L in vidas]
        t_ve = [L["primer_ve"][i] for L in vidas if i in L["primer_ve"]] if i != "berry_bush" else [L["primer_arbusto"] for L in vidas if L["primer_arbusto"] is not None]
        t_coge = [min(c["t"] for c in L["coge"] if c["id"] == i) for L in vidas if any(c["id"] == i for c in L["coge"])]
        t_usa = [min(u["t"] for u in L["usa"] if u["id"] == i and u["confirmado"]) for L in vidas if any(u["id"] == i and u["confirmado"] for u in L["usa"])]
        t_ata = [min(a["t"] for a in L["ataca"] if a["arma"] == i) for L in vidas if any(a["arma"] == i for a in L["ataca"])]
        def est(v): return {"mediana": q(v, .5), "p10": q(v, .1), "p90": q(v, .9), "total": sum(v), "vidas_con": sum(1 for x in v if x > 0)}
        R["por_objeto"][i] = {"tics_a_la_vista": est(tics), "montones_vistos": est(ve), "cogidos": est(coge), "usos_intentados": est(usos_int), "usos_confirmados": est(usos_conf),
                              "usos_completados": est(compl), "ataques": est(ataques), "golpes": est(golpes), "sueltos": est(suelta), "sueltos_junto_al_hermano": est(da),
                              "tics_primer_encuentro": {"n": len(t_ve), "mediana": q(t_ve, .5), "p10": q(t_ve, .1), "p90": q(t_ve, .9)},
                              "tics_primera_cogida": {"n": len(t_coge), "mediana": q(t_coge, .5), "p10": q(t_coge, .1), "p90": q(t_coge, .9)},
                              "tics_primer_uso": {"n": len(t_usa), "mediana": q(t_usa, .5), "p10": q(t_usa, .1), "p90": q(t_usa, .9)},
                              "tics_primer_ataque": {"n": len(t_ata), "mediana": q(t_ata, .5), "p10": q(t_ata, .1), "p90": q(t_ata, .9)},
                              "vistos_en_manos_ajenas": sum(L["ajenos"].get(i, 0) for L in vidas), "regalos_vistos": sum(L["regalos_vistos"].get(i, 0) for L in vidas), "regalos_mios": sum(L["regalos_mios"].get(i, 0) for L in vidas)}
    # punto 4: cambios al usar consumibles
    R["usos_consumibles"] = []
    for L in vidas:
        for u in L["usa"]:
            if u["kind"] == "ikConsumable" and u["confirmado"]:
                R["usos_consumibles"].append({"vida": L["carpeta"] + "/" + str(L["slot"]), **u})
    R["efectos_sobre_mi"] = dict(sum((Counter(L["efectos"]) for L in vidas), Counter()))
    R["fallos_pickup_total"] = sum(L["fallos_pickup"] for L in vidas)
    R["cogidas_en_arbusto"] = sum(1 for L in vidas for c in L["coge"] if c["en_arbusto"])
    R["tics_puesto"] = dict(sum((Counter(L["tics_puesto"]) for L in vidas), Counter())); R["tics_en_mano"] = dict(sum((Counter(L["tics_en_mano"]) for L in vidas), Counter()))
    lp = defaultdict(Counter)
    for L in vidas:
        for k, v in L["largo_pack_por_prenda"].items(): lp[k].update({int(a): b for a, b in v.items()})
    R["largo_pack_por_prenda"] = {k: dict(v) for k, v in lp.items()}
    R["fuentes_dano"] = dict(sum((Counter(L["fuentes_dano"]) for L in vidas), Counter())); R["dano_por_fuente"] = dict(sum((Counter(L["dano_por_fuente"]) for L in vidas), Counter()))
    R["fallos_causa"] = dict(sum((Counter(L["fallos_causa"]) for L in vidas), Counter())); R["fallos_en_arbusto"] = sum(L["fallos_en_arbusto"] for L in vidas); R["fallos_con_objeto_en_la_casilla"] = sum(L["fallos_con_objeto_en_la_casilla"] for L in vidas)
    for nombre in ("poison", "netted"):
        eps = [e for L in vidas for e in L["episodios"][nombre]]
        R["episodios_" + nombre] = {"n": len(eps), "vidas_con": sum(1 for L in vidas if L["episodios"][nombre]), "largo_mediana": q([e["largo"] for e in eps], .5), "largo_p10": q([e["largo"] for e in eps], .1), "largo_p90": q([e["largo"] for e in eps], .9),
                                    "hp_perdido_mediana": q([e["hp0"] - e["hp1"] for e in eps if e["hp0"] is not None and e["hp1"] is not None], .5)}
    R["vidas_con_camuflaje_puesto"] = sum(1 for L in vidas if L["tics_puesto"].get("camouflage")); R["vidas_con_mochila_puesta"] = sum(1 for L in vidas if L["tics_puesto"].get("backpack"))
    R["ataques_resultado"] = {}
    for L in vidas:
        for a in L["ataca"]: R["ataques_resultado"].setdefault(a["arma"], Counter())[a["res"]] += 1
    R["ataques_resultado"] = {k: dict(v) for k, v in R["ataques_resultado"].items()}
    R["ataques_sin_municion"] = {w: sum(1 for L in vidas for a in L["ataca"] if a["arma"] == w and a["municion"] == 0) for w in ("bow", "blowgun")}
    R["ids_vistos_fuera_del_catalogo"] = sorted({i for L in vidas for i in L["ve_tics"] if i not in [c["id"] for c in cat]})
    R["duracion_vida"] = {"mediana": q([L["ultimo_tick"] for L in vidas], .5), "p10": q([L["ultimo_tick"] for L in vidas], .1), "p90": q([L["ultimo_tick"] for L in vidas], .9)}
    return R

if __name__ == "__main__":
    vidas = []; cats = set(); cat0 = None
    for n, (s, carp, f) in enumerate(diarios(), 1):
        L, cat = vida(s, carp, f); vidas.append(L); cats.add(L.get("catalogo_md5")); cat0 = cat0 or cat
        print(f"{n:>2} {carp} asiento {L['slot']}: {L['ticks']} tics, coge {len(L['coge'])}, usa {len(L['usa'])}, suelta {len(L['suelta'])}, ataca {len(L['ataca'])}", flush=True)
    R = resumen(vidas, cat0); R["catalogos_distintos"] = len(cats); R["catalogo"] = cat0; R["series"] = SERIES
    json.dump({"resumen": R, "vidas": vidas}, open(OUT, "w"), indent=1, ensure_ascii=False)
    print("vidas:", len(vidas), "catalogos distintos:", len(cats), "->", os.path.relpath(OUT, RAIZ))
