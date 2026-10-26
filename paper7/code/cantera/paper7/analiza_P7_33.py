"""[P7-33, F3] EL HUMO DE 3 DIAS de la etapa de lo inutil, leido de los diarios (paintball/runs/P733_s1_d<D>_APRENDE_<semilla>/, dos asientos) -> P7_33_humo.json. Coste cero.
Por dia y criatura: que cosas toca y en que orden (primer tic con cada una en el zurron, mano o cuerpo), cuantas prueba (huellas por objeto: firmes, "al menos", cortes;
ventanas de red y camuflaje completas o no), creencia (cuaderno al acabar; sin cortes), ignorancia, ganas (k al acabar, de `P7_33_k`), cuantas veces coge cada cosa (subidas
del zurron), el contexto de cada prueba (calma / peligro: `P7_33_prueba`), el oido y la ley (`P7_33_ley`) y la latencia (`guarda_latencia_P7_29.mide`).
  python3 analiza_P7_33.py"""
import collections, glob, json, os, statistics as st
import guarda_latencia_P7_29 as GL
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
NOM = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}


def una(carp, dia, slot):
    f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log")); v = {"dia": dia, "asiento": slot, "semilla": int(os.path.basename(carp).split("_")[-1])}
    if not f: v["sin_diario"] = True; return v
    T = []; H = []; PR = []; LEY = []; K = []; fin = final = arr = None
    for line in open(f[0], errors="replace"):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "tick" and r.get("phase") == "live":
            n = collections.Counter()
            for s in (r.get("pack") or []):
                if s: n[s.get("id")] += int(s.get("n") or 1)
            h = r.get("hand") or {}
            if h.get("id") not in (None, "none"): n[h["id"]] += int(h.get("n") or 1)
            b = r.get("body"); bid = b.get("id") if isinstance(b, dict) else b
            if bid: n[bid] += 1
            T.append({"t": r["tick"], "hp": r.get("hp"), "n": {o: n.get(o, 0) for o in NOM}, "el": str((r.get("RADIOGRAFIA") or {}).get("elegido") or ""), "listo": (r.get("move_ready_in") or 0) == 0})
        elif k == "P7_huella": H.append(r)
        elif k == "P7_33_prueba" or (isinstance(k, float) and r.get("momento") == "abre" and "peligro" in r): PR.append(r)   # (humo: "k" pisado por las ganas en el registro de apertura del gear; corregido en la pieza)
        elif k == "P7_33_ley": LEY.append(r)
        elif k == "P7_33_k": K.append(r)
        elif isinstance(k, dict) and "red" in k and "camuflaje" in k: K.append({"tick": r.get("tick"), "ganas": k, "ignorancia": r.get("ignorancia"), "tiene": r.get("tiene"), "ley": r.get("ley")})   # (los diarios del humo: el campo "k" pisaba la clave del registro; corregido en la pieza)
        elif k == "P7_cuaderno" and r.get("momento") == "fin": fin = r
        elif k == "P7_cuaderno" and r.get("momento") == "arranque": arr = r
        elif k == "final": final = r
    if not T: v["sin_diario"] = True; return v
    v["tics"] = len(T); v["puesto"] = (final or {}).get("placement"); v["murio"] = (final or {}).get("reason") == "eliminated"; v["cuaderno_leido"] = bool((arr or {}).get("leido"))
    v["contacto"] = {NOM[o]: next((T[i]["t"] for i in range(1, len(T)) if T[i]["n"][o] > T[i - 1]["n"][o]), None) for o in NOM}
    v["orden_de_contacto"] = [NOM[o] for o, t in sorted(((o, t) for o, t in ((o, v["contacto"][NOM[o]]) for o in NOM) if t is not None), key=lambda x: x[1])]
    v["coge"] = {NOM[o]: sum(max(0, T[i]["n"][o] - T[i - 1]["n"][o]) for i in range(1, len(T))) for o in NOM}
    v["pruebas"] = {}
    for o, nom in NOM.items():
        hs = [h for h in H if (h.get("objeto") or "first_aid") == o]
        v["pruebas"][nom] = {"n": len(hs), "firmes": sum(1 for h in hs if h.get("apuntado") and not h.get("corte") and not h.get("al_menos")), "al_menos": sum(1 for h in hs if h.get("al_menos")), "cortes": sum(1 for h in hs if h.get("corte")),
                             "ventanas_completas": sum(1 for h in hs if h.get("completa")), "ventanas_cortas": sum(1 for h in hs if "completa" in h and not h["completa"]), "hp_al_abrir": [h.get("hp0") for h in hs], "efecto_cuerpo": [h["efecto"]["cuerpo"] for h in hs], "t0": [h["t0"] for h in hs]}
    cont = ((fin or {}).get("contenido") or {}); cr = cont.get("creencias") or {}
    v["al_acabar"] = {}
    for o, nom in NOM.items():
        c = cr.get(o) or {}; rec = [r for s_ in ((cont.get("objetos") or {}).get(o) or {}).get("situaciones", {}).values() for r in s_]
        v["al_acabar"][nom] = {"creencia": {s_: x.get("cuerpo") for s_, x in c.items() if isinstance(x, dict)}, "ignorancia": c.get("ignorancia", 1.0), "ignorancia_cuanto": c.get("ignorancia_cuanto"), "sabido_max": c.get("sabido_max"), "recuerdos": len(rec), "cortes": sum(1 for r in rec if r.get("corte")), "firmes": sum(1 for r in rec if not r.get("corte") and not r.get("al_menos")), "al_menos": sum(1 for r in rec if r.get("al_menos"))}
    v["k_al_acabar"] = (K[-1]["ganas"] if K else None); v["k_muestras"] = [{"tick": x["tick"], **x["ganas"]} for x in K[::4]]; v["ignorancia_muestras"] = [{"tick": x["tick"], **(x.get("ignorancia") or {})} for x in K[::4]]
    ab = [p for p in PR if p.get("momento") == "abre"]
    v["contexto_de_las_pruebas"] = {NOM.get(o, o): {"n": sum(1 for p in ab if p["objeto"] == o), "en_calma": sum(1 for p in ab if p["objeto"] == o and (p.get("peligro") or {}).get("calma")), "rival_a_4": sum(1 for p in ab if p["objeto"] == o and (p.get("peligro") or {}).get("rival_a_4")), "vida_menor_30": sum(1 for p in ab if p["objeto"] == o and (p.get("peligro") or {}).get("vida_menor_30")), "fuego": sum(1 for p in ab if p["objeto"] == o and (p.get("peligro") or {}).get("fuego"))} for o in NOM}
    v["ley"] = {"avisos": [l.get("aviso") for l in LEY if l.get("aviso")], "cambios_de_casillas": [(l["tick"], l.get("casillas_no_transitables")) for l in LEY if "casillas_no_transitables" in l]}
    listos = sum(1 for t in T if t["listo"]); v["ir_curioso_con_paso_listo"] = sum(1 for t in T if t["listo"] and t["el"] == "ir_curioso"); v["ir_curioso_fraccion"] = round(v["ir_curioso_con_paso_listo"] / max(1, listos), 4)
    v["elegido_ponerse_empunar"] = {k: n for k, n in collections.Counter(t["el"] for t in T).items() if k.startswith(("ponerse_", "empunar_", "usar_", "soltar_"))}
    v["latencia"] = GL.mide(f[0])
    return v


if __name__ == "__main__":
    V = []
    for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P733_s1_d*_APRENDE_*"))):
        d = int(os.path.basename(c).split("_")[2][1:])
        for sl in (10, 11): V.append(una(c, d, sl))
    json.dump(V, open(os.path.join(AQUI, "P7_33_humo.json"), "w"), ensure_ascii=False, indent=1)
    for v in V:
        if v.get("sin_diario"): print(v, "sin diario"); continue
        print(f"d{v['dia']} a{v['asiento']} tics {v['tics']} puesto {v['puesto']} orden {v['orden_de_contacto']} coge {v['coge']} pruebas {{ {', '.join(f'{o}: {p['n']}' for o, p in v['pruebas'].items())} }} k {v['k_al_acabar']} ign {{ {', '.join(f'{o}: {a['ignorancia']}' for o, a in v['al_acabar'].items())} }} curioso {v['ir_curioso_fraccion']} ms {v['latencia']['ms_mediana']} / {100 * (v['latencia']['sobre_el_tic'] or 0):.2f} % {'pasa' if v['latencia']['pasa'] else 'NO PASA'}")
