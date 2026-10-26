"""[P7-11] POR QUE EL QUE APRENDE ACABA PEOR, Y QUE ES EL SUELO. Lectura de los 320 diarios de P7-10 (paintball/runs/P710_s<S>_d<D>_<BRAZO>_<semilla>/,
fuera de git), posterior al sello y declarada asi. Coste cero: ni partidas, ni llamadas, ni replay (solo se leen los diarios crudos; el cuerpo
no se ejecuta). Los identificadores del mundo se leen de cada diario (`mundo_leido.id_botiquin`, `player_config.team`, `catalogo`), no se cablean.
  python3 analiza_P7_11.py            -> P7_11_vidas.json (una entrada por vida) y P7_11_dia1.json (APRENDE contra BORRADO el dia 1, tic a tic)
Definiciones (iguales para los cuatro brazos):
  - COGER / REGALAR / USAR: como en `campo_P7_10.py` (sube o baja el n de botiquines tras `pickup` / `drop` con `soltar_<botiquin>` elegido; ventana del canal).
  - EL CANDIDATO EN CURSO de un tic: el cuerpo decide moverse cada ~11 tics (el enfriamiento del paso) y entre medias elige `noop`; por eso a cada
    tic se le pone la categoria del ultimo elegido distinto de `noop` en los 12 tics anteriores (medio segundo), y "quieto" si no lo hay.
  - IR A POR UN BOTIQUIN: `ir_curioso`, mas las rachas de `ir_objeto` (elegidos seguidos con huecos <= 24 tics) que acaban cogiendo un botiquin en
    los 24 tics siguientes. Las rachas de `ir_objeto` que acaban cogiendo otra cosa o nada van aparte (el diario no dice a donde iba).
  - RIVAL A LA VISTA: algun agente de `ve_agentes` de otro equipo en ese tic.
  - DESTINO DE UN REGALO: la primera recogida en esa casilla despues de soltarlo (el hermano o el mismo); si no la hay: "desaparece" si un hermano
    esta a distancia <= 1 de la casilla y el botiquin ya no esta a la vista en ella (con o sin un rival visto encima entre medias); "en el suelo"
    si la ultima vez que se vio la casilla el botiquin seguia; "no se volvio a ver" si ninguno de los dos volvio a verla.
  - LA FILA QUE PAGA una decision: entre el candidato elegido y `noop` (o, si no hay `noop`, el segundo por d), la fila cuya M mas mejora
    (baja si su signo es "-", sube si es "+", segun `ahora.filas`; sin signo en `ahora` se toma "-").
  - ULTIMOS 10 SEGUNDOS: los tics con numero >= ultimo tic - 10 x tick_rate (24 por segundo, de `player_config`)."""
import collections, glob, json, math, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
OBS = ("pos", "hp", "hand", "body", "pack", "effects", "damage_taken", "zona", "ve_agentes", "ve_items", "ve_bushes", "ve_proyectiles", "eventos", "chat")

def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
def categoria(el, kit):
    if el == "ir_curioso": return "ir a por un botiquin"
    if el == "ir_objeto": return "ir a por un objeto"
    if el in ("ir_botin", "coger"): return "botin o coger"
    if el.startswith("soltar_"): return "regalar o soltar"
    if el.startswith("hacer_sitio_"): return "hacer sitio"
    if el.startswith("atacar_") or el.startswith("empunar_") or el.startswith("disparar") or el.startswith("lanzar"): return "pelear"
    if el.startswith("usar_"): return "usar un consumible"
    if el.startswith("move_") or el.startswith("paso_"): return "moverse paso a paso"
    if el == "ir_pareja": return "ir al hermano"
    if el == "ir_centro": return "ir al centro"
    if el == "noop": return "quieto"
    return "otro: " + el

def lee(f):
    M = {"huellas": [], "usos_P7": [], "cuad": {}, "final": None, "team": None, "slot": None, "kit": "first_aid", "cat": None, "rate": 24, "arranque": None, "signos": {}}; T = []
    for line in open(f):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "tick":
            if r.get("phase") != "live": continue
            kit = M["kit"]; R = r.get("RADIOGRAFIA") or {}; el = str(R.get("elegido") or ""); pos = tuple(r["pos"])
            pack = collections.Counter()
            for s in r.get("pack") or []:
                if s: pack[s.get("id")] += int(s.get("n") or 1)
            z = r.get("zona") or {}; c = z.get("center"); rad = z.get("radius")
            t = {"t": r["tick"], "pos": pos, "hp": float(r.get("hp") or 0), "el": el, "do": (r.get("intencion") or {}).get("do"), "kits": pack.get(kit, 0), "pack": dict(pack),
                 "canal": any(e.get("id") == "channeling" and e.get("item") == kit for e in (r.get("effects") or [])),
                 "dentro": (math.dist(pos, c) <= rad) if (c is not None and rad is not None) else None,
                 "kitpos": frozenset(tuple(it["pos"]) for it in (r.get("ve_items") or []) if it.get("id") == kit and it.get("pos")),
                 "riv": [tuple(a["pos"]) for a in (r.get("ve_agentes") or []) if a.get("team") != M["team"] and a.get("pos")],
                 "herm": any(a.get("team") == M["team"] and a.get("slot") != M["slot"] for a in (r.get("ve_agentes") or [])),
                 "dmg": [(str(d.get("source") or ""), float(d.get("amount") or 0)) for d in (r.get("damage_taken") or [])],
                 "banda": (r.get("social") or {}).get("pareja_banda"), "dist_pareja": (r.get("social") or {}).get("dist_pareja")}
            if el == "usar_botiquin" or el.startswith("soltar_" + kit):
                C = {n_: (v_ if isinstance(v_, dict) else {"d": v_}) for n_, v_ in (R.get("candidatos") or {}).items()}; otros = sorted((x for x in C if x != el), key=lambda x: C[x].get("d", 9e9))
                alt = "noop" if "noop" in C else (otros[0] if otros else None)
                t["det"] = {"el": C.get(el), "alt_nombre": alt, "alt": C.get(alt) if alt else None, "signos": {n_: v.get("signo") for n_, v in ((R.get("ahora") or {}).get("filas") or {}).items() if isinstance(v, dict)}, "n_cand": len(C)}
            for n_, v_ in ((R.get("ahora") or {}).get("filas") or {}).items():
                if isinstance(v_, dict) and v_.get("signo"): M["signos"][n_] = v_["signo"]
            T.append(t)
        elif k == "player_config": M["team"] = r.get("team"); M["slot"] = r.get("slot"); M["rate"] = int(r.get("tick_rate") or 24)
        elif k == "mundo_leido": M["kit"] = r.get("id_botiquin") or "first_aid"
        elif k == "catalogo" and M["cat"] is None: M["cat"] = {it["id"]: it for it in r.get("items") or []}
        elif k == "P7_arranque": M["arranque"] = (r.get("entorno_P7") or {})
        elif k == "P7_cuaderno": M["cuad"][r.get("momento")] = r
        elif k == "P7_uso": M["usos_P7"].append(r)
        elif k == "P7_huella": M["huellas"].append(r)
        elif k == "final": M["final"] = r
    return M, T

def fila_que_paga(det):
    if not det or not det.get("el") or not det.get("alt"): return None
    fe, fa = det["el"].get("filas") or {}, det["alt"].get("filas") or {}; sig = det.get("signos") or {}; mejor = None
    for fila in set(fe) | set(fa):
        a, b = float(fa.get(fila) or 0.0), float(fe.get(fila) or 0.0)
        gana = (a - b) if sig.get(fila, "-") == "-" else (b - a)
        if mejor is None or gana > mejor[1]: mejor = (fila, round(gana, 5))
    return {"fila": mejor[0] if mejor else None, "mejora_M": mejor[1] if mejor else None, "alternativa": det.get("alt_nombre"), "d_elegido": det["el"].get("d"), "d_alternativa": det["alt"].get("d"),
            "hp_prevista_elegido": det["el"].get("hp_prevista"), "hp_prevista_alternativa": det["alt"].get("hp_prevista")}

def eventos(M, T):
    """recogidas (por clase), regalos de botiquin, botiquines soltados al hacer sitio"""
    kit = M["kit"]; coge = []; regala = []; sitio_kit = []
    for a, b in zip(T, T[1:]):
        if a["do"] == "pickup":
            sube = [i for i in b["pack"] if b["pack"][i] > a["pack"].get(i, 0)]
            if sube: coge.append({"t": b["t"], "pos": a["pos"], "clases": sube, "kit": kit in sube})
        if a["do"] == "drop" and b["kits"] < a["kits"]:
            if a["el"].startswith("soltar_" + kit): regala.append({"t": b["t"], "t_dec": a["t"], "pos": a["pos"], "n": a["kits"] - b["kits"], "hp": a["hp"], "dentro": a["dentro"], "rival_a_la_vista": bool(a["riv"]), "hermano_a_la_vista": a["herm"], "banda_hermano": a["banda"], "dist_hermano": a["dist_pareja"], "en_canal": a["canal"], "paga": fila_que_paga(a.get("det"))})
            elif a["el"].startswith("hacer_sitio_" + kit): sitio_kit.append({"t": b["t"], "pos": a["pos"]})
    return coge, regala, sitio_kit

def una_vida(M, T, Mh, Th, campo):
    kit = M["kit"]; cura = float((M["cat"] or {}).get(kit, {}).get("heal") or 0) or None; rate = M["rate"]
    coge, regala, sitio_kit = eventos(M, T); coge_h = eventos(Mh, Th)[0] if Th else []
    # la creencia del cuaderno en cada momento (APRENDE y BORRADO): la de arranque, y tras cada huella apuntada la de su situacion
    cre = {}; c0 = ((((M["cuad"].get("arranque") or {}).get("contenido") or {}).get("creencias") or {}).get(kit) or {})
    for sit, v in c0.items():
        if isinstance(v, dict) and v.get("cuerpo") is not None: cre[sit] = float(v["cuerpo"])
    hs = sorted((h for h in M["huellas"] if h.get("apuntado")), key=lambda h: h["t_fin"]); ih = 0
    def creencia_en(t):
        nonlocal ih
        while ih < len(hs) and hs[ih]["t_fin"] <= t:
            cd = hs[ih].get("creencia_despues") or {}
            if cd.get("cuerpo") is not None: cre[hs[ih]["situacion"]] = float(cd["cuerpo"])
            ih += 1
        return max(cre.values()) if cre else None
    # rachas de ir_objeto y lo que acaban cogiendo
    idx = [i for i, t in enumerate(T) if t["el"] == "ir_objeto"]; rachas = []
    for i in idx:
        if rachas and T[i]["t"] - T[rachas[-1][-1]]["t"] <= 24: rachas[-1].append(i)
        else: rachas.append([i])
    a_kit = set(); a_otro = set(); a_nada = set()
    for r in rachas:
        fin = T[r[-1]]["t"]; cg = [c for c in coge if fin < c["t"] <= fin + 24 + 1]
        (a_kit if any(c["kit"] for c in cg) else a_otro if cg else a_nada).update(r)
    cont = collections.Counter(); cats = []; ult = None
    for i, t in enumerate(T):
        c = categoria(t["el"], kit)
        if c == "ir a por un objeto": c = "ir a por un botiquin" if i in a_kit else "ir a por otro objeto" if i in a_otro else "ir a por un objeto sin cogerlo"
        cont["elegido " + c] += 1
        if c != "quieto": ult = (t["t"], c)
        elif ult and t["t"] - ult[0] <= 12: c = ult[1]
        cats.append(c); rv = bool(t["riv"])
        cont["tics"] += 1; cont["tics con rival a la vista"] += rv
        cont["tics " + c] += 1; cont["tics " + c + " con rival a la vista"] += rv
        if t["el"] == "ir_curioso": cont["tics ir_curioso"] += 1
        if t["canal"]: cont["tics en canal"] += 1; cont["tics en canal con rival a la vista"] += rv
        if t["kits"] >= 1: cont["tics con botiquin a bordo"] += 1
        if t["el"].startswith("soltar_" + kit): cont["tics soltar botiquin"] += 1; cont["tics soltar botiquin con rival a la vista"] += rv
    # usos: ventana del canal, y la decision de usar que la abre
    usos = []; v = None
    for i, t in enumerate(T):
        if v is not None and t["el"].startswith("soltar_" + kit): v["regalado"] = True
        if v is None and t["canal"]:
            dec = next((T[j] for j in range(i, max(-1, i - 4), -1) if T[j]["el"] == "usar_botiquin"), None); pg = fila_que_paga(dec.get("det")) if dec else None
            v = {"t0": t["t"], "hp0": t["hp"], "kits0": t["kits"], "dentro": t["dentro"], "regalado": t["el"].startswith("soltar_" + kit), "rival_a_la_vista": bool(t["riv"]),
                 "decision": ({"t": dec["t"], "hp": dec["hp"], **(pg or {}), "cura_imaginada": (round(pg["hp_prevista_elegido"] - pg["hp_prevista_alternativa"], 3) if pg and pg.get("hp_prevista_elegido") is not None and pg.get("hp_prevista_alternativa") is not None else None), "n_cand": dec["det"]["n_cand"]} if dec else None)}
        elif v is not None and not t["canal"]:
            v["gastado"] = t["kits"] < v["kits0"] and not v["regalado"]; v["t_fin"] = t["t"]; v["hp_fin"] = t["hp"]; usos.append(v); v = None
    for u in usos:
        pu = next((x for x in M["usos_P7"] if x.get("tick") == u["t0"]), None)
        if pu: u["P7_uso"] = {k_: pu.get(k_) for k_ in ("heal_imaginado", "creencia_cuerpo", "ignorancia", "esperanza", "k_ganas")}
    # regalos: creencia de quien regala, y destino
    todos = {"yo": T, "hermano": Th or []}
    for g in regala:
        cm = creencia_en(g["t_dec"]) if M["cuad"].get("arranque") else None
        g["creencia_max"] = cm; g["k_creencia"] = (round(cm / cura, 4) if (cm is not None and cura) else None)
        p = g["pos"]; rec = [("el hermano", c["t"]) for c in coge_h if c["kit"] and c["pos"] == p and c["t"] > g["t"]] + [("el mismo", c["t"]) for c in coge if c["kit"] and c["pos"] == p and c["t"] > g["t"]]
        if rec:
            q = min(rec, key=lambda x: x[1]); g["destino"] = "lo recoge " + q[0]; g["tics_hasta_recogerlo"] = q[1] - g["t"]; continue
        visto = None; falta = None; rival_encima = False
        for quien, TT in todos.items():
            for t in TT:
                if t["t"] <= g["t"]: continue
                if p in t["kitpos"]: visto = max(visto or 0, t["t"])
                elif cheb(t["pos"], p) <= 1 and (falta is None or t["t"] < falta): falta = t["t"]
        if falta is not None:
            for TT in todos.values():
                for t in TT:
                    if g["t"] < t["t"] <= falta and p in t["riv"]: rival_encima = True
            g["destino"] = "desaparece (rival visto encima)" if rival_encima else "desaparece (nadie visto)"; g["t_falta"] = falta
        elif visto is not None: g["destino"] = "en el suelo la ultima vez que se vio"; g["t_visto"] = visto
        else: g["destino"] = "no se volvio a ver"
        g["tics_de_vida_despues"] = T[-1]["t"] - g["t"]
    # la muerte: los ultimos 10 segundos
    ult = T[-1]; W = [(t, c) for t, c in zip(T, cats) if t["t"] >= ult["t"] - 10 * rate]
    en_ventana = collections.Counter(c for _, c in W); vistos = set().union(*[t["kitpos"] for t, _ in W]) if W else set()
    muerte = {"categorias": dict(en_ventana), "moda": en_ventana.most_common(1)[0][0], "ultimo_elegido": ult["el"], "dentro": ult["dentro"], "hp_al_empezar_la_ventana": W[0][0]["hp"], "botiquines_a_bordo": ult["kits"],
              "dist_botiquin_a_la_vista": (round(min(math.dist(ult["pos"], p) for p in ult["kitpos"]), 2) if ult["kitpos"] else None),
              "dist_botiquin_visto_en_la_ventana": (round(min(math.dist(ult["pos"], p) for p in vistos), 2) if vistos else None),
              "rivales_a_la_vista": len(ult["riv"]), "tics_en_canal": sum(1 for t, _ in W if t["canal"]), "tics_con_rival_a_la_vista": sum(1 for t, _ in W if t["riv"]),
              "dano_rival": round(sum(a for t, _ in W for s, a in t["dmg"] if s.startswith("P")), 1), "dano_anillo": round(sum(a for t, _ in W for s, a in t["dmg"] if s == "zone"), 1),
              "regalos_en_la_ventana": sum(1 for g in regala if g["t"] >= W[0][0]["t"]), "cogidas_de_botiquin_en_la_ventana": sum(1 for c in coge if c["kit"] and c["t"] >= W[0][0]["t"])}
    pos_h = {(c["pos"], c["t"]) for c in coge_h}
    return {"brazo_del_diario": (M["arranque"] or {}).get("brazo"), "efectivo": (M["arranque"] or {}).get("efectivo"), "cura_catalogo": cura, "huella_con_regalado": (("regalado" in M["huellas"][0]) if M["huellas"] else None),
            "ventanas_con_regalo_apuntadas": sum(1 for h in M["huellas"] if h.get("apuntado") and any(g["t_dec"] >= h["t0"] and g["t_dec"] <= h["t_fin"] for g in regala)),
            "contadores": dict(cont), "coge_botiquines": sum(1 for c in coge if c["kit"]), "coge_botiquines_que_solto_el_hermano": None, "coge_otros": sum(1 for c in coge if not c["kit"]),
            "regala": regala, "regala_n": len(regala), "regala_unidades": sum(g["n"] for g in regala), "botiquines_soltados_al_hacer_sitio": len(sitio_kit),
            "usos": usos, "muerte": muerte, "motivo": (M["final"] or {}).get("reason"), "puesto": (M["final"] or {}).get("placement"), "hp_final": ult["hp"], "ultimo_tick": ult["t"],
            "causa_muerte": (campo or {}).get("causa_muerte"), "signos": M["signos"], "elegidos": dict(collections.Counter(t["el"] if not t["el"].startswith("hacer_sitio_") else "hacer_sitio_*" for t in T))}

def un_partido(carp):
    b = os.path.basename(carp); _, s_, d_, brazo, sem = b.split("_"); serie = int(s_[1:]); dia = int(d_[1:]); out = {}
    campo = json.load(open(os.path.join(AQUI, "P7_10_campo.json")))
    L = {}
    for slot in (10, 11):
        f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log")); L[slot] = lee(f[0]) if f else (None, [])
    for slot in (10, 11):
        M, T = L[slot]; Mh, Th = L[21 - slot] if False else L[10 if slot == 11 else 11]
        if not T: continue
        k = f"s{serie}_d{dia}_{brazo}_{slot}"; v = una_vida(M, T, Mh, Th, campo.get(k))
        # botiquines que coge y que habia soltado el hermano (misma casilla, despues)
        if Th:
            reg_h = eventos(Mh, Th)[1]; mis = [c for c in eventos(M, T)[0] if c["kit"]]
            v["coge_botiquines_que_solto_el_hermano"] = sum(1 for c in mis if any(g["pos"] == c["pos"] and g["t"] < c["t"] for g in reg_h))
        out[k] = {"serie": serie, "dia": dia, "brazo": brazo, "slot": slot, "semilla": int(sem), **v}
    return out

def dia1(serie, slot, a="APRENDE", b="BORRADO"):
    """Dos diarios del mismo dia, semilla y asiento, tic a tic: el primer tic en que difiere lo que ven (y que campo), el primero en que difiere
    lo elegido, y si antes de la primera diferencia de lo visto las decisiones (elegido y la d de cada candidato) son identicas."""
    fa = glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P710_s{serie}_d1_{a}_*", f"*policy_agent_{slot}.art.log"))[0]
    fb = glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P710_s{serie}_d1_{b}_*", f"*policy_agent_{slot}.art.log"))[0]
    def ticks(f):
        for line in open(f):
            if '"tick"' not in line[:16]: continue
            r = json.loads(line)
            if r.get("k") == "tick" and r.get("phase") == "live": yield r
    R = {"serie": serie, "slot": slot, "a": a, "b": b, "tics_comparados": 0, "primer_tic_vista_distinta": None, "campos_distintos": None, "detalle": None, "primer_tic_elegido_distinto": None, "elegidos_en_ese_tic": None,
         "tics_iguales_antes": 0, "decisiones_identicas_antes_de_la_vista_distinta": None, "d_identicas_antes": None, "primer_tic": None}
    iguales_el = True; iguales_d = True
    for x, y in zip(ticks(fa), ticks(fb)):
        if R["primer_tic"] is None: R["primer_tic"] = (x["tick"], y["tick"])
        if x["tick"] != y["tick"]: R["detalle"] = f"los tics se desalinean: {x['tick']} y {y['tick']}"; break
        R["tics_comparados"] += 1
        ex, ey = (x.get("RADIOGRAFIA") or {}).get("elegido"), (y.get("RADIOGRAFIA") or {}).get("elegido")
        if R["primer_tic_vista_distinta"] is None:
            dif = [c for c in OBS if x.get(c) != y.get(c)]
            if dif:
                R["primer_tic_vista_distinta"] = x["tick"]; R["campos_distintos"] = dif; c0 = dif[0]
                R["detalle"] = {c0: [json.dumps(x.get(c0), ensure_ascii=False)[:300], json.dumps(y.get(c0), ensure_ascii=False)[:300]]}
                if "ve_agentes" in dif:
                    ax = {a_["slot"]: a_ for a_ in x.get("ve_agentes") or []}; ay = {a_["slot"]: a_ for a_ in y.get("ve_agentes") or []}
                    R["agentes_distintos"] = sorted(s for s in set(ax) | set(ay) if ax.get(s) != ay.get(s))
                R["decisiones_identicas_antes_de_la_vista_distinta"] = iguales_el; R["d_identicas_antes"] = iguales_d
            else:
                R["tics_iguales_antes"] += 1
                if ex != ey: iguales_el = False
                dx = {k_: (v_.get("d") if isinstance(v_, dict) else v_) for k_, v_ in ((x.get("RADIOGRAFIA") or {}).get("candidatos") or {}).items()}; dy = {k_: (v_.get("d") if isinstance(v_, dict) else v_) for k_, v_ in ((y.get("RADIOGRAFIA") or {}).get("candidatos") or {}).items()}
                if dx != dy: iguales_d = False
        if R["primer_tic_elegido_distinto"] is None and ex != ey: R["primer_tic_elegido_distinto"] = x["tick"]; R["elegidos_en_ese_tic"] = [ex, ey]
        if R["primer_tic_vista_distinta"] is not None and R["primer_tic_elegido_distinto"] is not None: break
    if R["primer_tic_vista_distinta"] is None: R["decisiones_identicas_antes_de_la_vista_distinta"] = iguales_el; R["d_identicas_antes"] = iguales_d
    return R

if __name__ == "__main__":
    carps = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P710_s*_d*_*_*")))
    with Pool(8) as P:
        OUT = {}
        for o in P.imap_unordered(un_partido, carps): OUT.update(o)
        D1 = P.starmap(dia1, [(s, sl, a, b) for s in (1, 2) for sl in (10, 11) for a, b in (("APRENDE", "BORRADO"), ("SUELO", "TECHO"), ("BORRADO", "SUELO"))])
    json.dump(dict(sorted(OUT.items())), open(os.path.join(AQUI, "P7_11_vidas.json"), "w"), ensure_ascii=False, indent=0)
    json.dump(D1, open(os.path.join(AQUI, "P7_11_dia1.json"), "w"), ensure_ascii=False, indent=1)
    print("vidas", len(OUT), "· dia 1:", len(D1))
