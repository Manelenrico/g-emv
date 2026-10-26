"""[P7-34] EL CAMPO DE LO INUTIL, leido de los diarios (paintball/runs/P734_s<S>_d<D>_<BRAZO>_<semilla>/, dos asientos) -> P7_34_datos.json. Coste cero.
Por serie, dia, brazo y asiento, para cada una de las cuatro cosas (SELLO_P7_34.md, "Definiciones"): contactos (tics en que suben las unidades), cogidas, sueltas (bajadas
sin uso), usos (aperturas del canal, `P7_nace_uso`), pruebas y su contexto (`P7_huella` + `P7_33_prueba` "abre"), recuerdos al cerrar (firmes, "al menos", cortes, "no hizo nada",
intensidad media), creencia, ignorancia, ganas (ultimo `P7_33_k`); puesto, muerte, latencia (`guarda_latencia_P7_29.mide`) y agua (`P7_33_ley`).
  python3 analiza_P7_34.py [--solo-aprende]"""
import collections, glob, json, os, statistics as st, sys
import guarda_latencia_P7_29 as GL
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
NOM = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}
UTILES = ("botiquin", "racion"); INUTILES = ("red", "camuflaje"); NADA = 1.0     # "no hizo nada": |efecto en el cuerpo| <= 1


def unidades(r):
    n = collections.Counter()
    for s in (r.get("pack") or []):
        if s: n[s.get("id")] += int(s.get("n") or 1)
    h = r.get("hand") or {}
    if h.get("id") not in (None, "none"): n[h["id"]] += int(h.get("n") or 1)
    b = r.get("body"); bid = b.get("id") if isinstance(b, dict) else b
    if bid: n[bid] += 1
    return {o: n.get(o, 0) for o in NOM}


def una(carp, serie, dia, brazo, slot):
    f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log")); v = {"serie": serie, "dia": dia, "brazo": brazo, "asiento": slot, "semilla": int(os.path.basename(carp).split("_")[-1]), "carpeta": os.path.basename(carp)}
    if not f: v["sin_diario"] = True; return v
    T = []; H = []; PR = []; LEY = []; K = []; USO = {}; fin = final = arr = None; errores = 0; parcial = None
    for line in open(f[0], errors="replace"):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "tick" and r.get("phase") == "live":
            T.append({"t": r["tick"], "hp": r.get("hp"), "n": unidades(r), "el": str((r.get("RADIOGRAFIA") or {}).get("elegido") or ""), "listo": (r.get("move_ready_in") or 0) == 0, "bloq": r.get("action_result") == "blocked", "pos": tuple(r.get("pos") or (0, 0))})
        elif k == "P7_huella": H.append(r)
        elif k == "P7_nace_uso": USO[r.get("objeto")] = USO.get(r.get("objeto"), 0) + 1
        elif k == "P7_33_prueba": PR.append(r)
        elif k == "P7_33_ley": LEY.append(r)
        elif k == "P7_33_k": K.append(r)
        elif k == "P7_cuaderno" and r.get("momento") == "fin": fin = r
        elif k == "P7_cuaderno" and r.get("momento") == "arranque": arr = r
        elif k == "final": final = r
        elif k == "P7_error" and "fotos para" in str(r.get("error")): errores += 1
        elif k == "PARCIAL": parcial = r
    if not T: v["sin_diario"] = True; return v
    v["tics"] = len(T); v["ultimo_tic"] = T[-1]["t"]; v["puesto"] = (final or {}).get("placement"); v["murio"] = (final or {}).get("reason") == "eliminated"; v["tic_muerte"] = (T[-1]["t"] if v["murio"] else None)
    v["cuaderno_leido"] = bool((arr or {}).get("leido")); v["errores_fotos"] = errores; v["parcial"] = parcial is not None or final is None
    v["contacto"] = {}; v["coge"] = {}; v["suelta"] = {}; v["usa"] = {}; v["contactos"] = {}
    for o, nom in NOM.items():
        subidas = [T[i]["t"] for i in range(1, len(T)) if T[i]["n"][o] > T[i - 1]["n"][o]]
        v["contactos"][nom] = subidas; v["contacto"][nom] = (subidas[0] if subidas else None)
        v["coge"][nom] = sum(max(0, T[i]["n"][o] - T[i - 1]["n"][o]) for i in range(1, len(T)))
        bajadas = sum(T[i - 1]["n"][o] - T[i]["n"][o] for i in range(1, len(T)) if T[i]["n"][o] < T[i - 1]["n"][o])
        v["usa"][nom] = USO.get(o, 0); v["suelta"][nom] = max(0, bajadas - USO.get(o, 0))      # usos = aperturas del canal (`P7_nace_uso`); sueltas = las demas bajadas (regalos, hacer sitio, muerte)
    v["orden_de_contacto"] = [NOM[o] for o, t in sorted(((o, v["contacto"][NOM[o]]) for o in NOM if v["contacto"][NOM[o]] is not None), key=lambda x: x[1])]
    ab = {}
    for p in PR:
        if p.get("momento") == "abre": ab.setdefault(p["objeto"], []).append(p)
    v["pruebas"] = {}
    for o, nom in NOM.items():
        hs = [h for h in H if (h.get("objeto") or "first_aid") == o]; ap = ab.get(o, [])
        v["pruebas"][nom] = {"n": len(hs), "firmes": sum(1 for h in hs if h.get("apuntado") and not h.get("corte") and not h.get("al_menos")), "al_menos": sum(1 for h in hs if h.get("al_menos")), "cortes": sum(1 for h in hs if h.get("corte")),
                             "ventanas_completas": sum(1 for h in hs if h.get("completa")), "t0": [h["t0"] for h in hs], "hp_al_abrir": [h.get("hp0") for h in hs], "efecto_cuerpo": [((h.get("efecto") or {}).get("cuerpo")) for h in hs],
                             "aperturas": len(ap), "en_calma": sum(1 for p in ap if (p.get("peligro") or {}).get("calma")), "rival_a_4": sum(1 for p in ap if (p.get("peligro") or {}).get("rival_a_4")), "fuego": sum(1 for p in ap if (p.get("peligro") or {}).get("fuego")), "vida_menor_30": sum(1 for p in ap if (p.get("peligro") or {}).get("vida_menor_30")),
                             "contextos": [{"tick": p["tick"], **{k_: (p.get("peligro") or {}).get(k_) for k_ in ("calma", "rival_a_4", "fuego", "vida_menor_30")}} for p in ap]}
    cont = ((fin or {}).get("contenido") or {}); cr = cont.get("creencias") or {}
    v["al_acabar"] = {}
    for o, nom in NOM.items():
        c = cr.get(o) or {}; sits = ((cont.get("objetos") or {}).get(o) or {}).get("situaciones", {}); rec = [r for s_ in sits.values() for r in s_]
        firmes = [r for r in rec if not r.get("corte") and not r.get("al_menos")]
        cre_d = (c.get("dentro") or {}).get("cuerpo") if isinstance(c.get("dentro"), dict) else None; cre_f = (c.get("fuera") or {}).get("cuerpo") if isinstance(c.get("fuera"), dict) else None
        v["al_acabar"][nom] = {"creencia": (cre_d if (cre_d is not None or nom == "botiquin") else cre_f), "creencia_dentro": cre_d, "creencia_fuera": cre_f, "ignorancia": c.get("ignorancia", 1.0), "ignorancia_cuanto": c.get("ignorancia_cuanto"), "sabido_max": c.get("sabido_max"),
                              "recuerdos": len(rec), "firmes": len(firmes), "al_menos": sum(1 for r in rec if r.get("al_menos")), "cortes": sum(1 for r in rec if r.get("corte")),
                              "no_hizo_nada": sum(1 for r in rec if nom in INUTILES and not r.get("corte") and abs(float((r.get("efecto") or {}).get("cuerpo") or 0.0)) <= NADA),
                              "intensidad_media": (round(st.mean(float(r["intensidad"]) for r in rec if not r.get("corte")), 4) if any(not r.get("corte") for r in rec) else None), "intensidades": [round(float(r["intensidad"]), 4) for r in rec if not r.get("corte")]}
    v["k_al_acabar"] = ((K[-1].get("ganas") or K[-1].get("k")) if K else None)
    v["ley"] = {"avisos": [l.get("aviso") for l in LEY if l.get("aviso")], "casillas": [(l["tick"], l.get("casillas_no_transitables")) for l in LEY if "casillas_no_transitables" in l], "bloqueados": sum(1 for t in T if t["bloq"])}
    listos = sum(1 for t in T if t["listo"]); v["ir_curioso_con_paso_listo"] = sum(1 for t in T if t["listo"] and t["el"] == "ir_curioso"); v["ir_curioso_fraccion"] = round(v["ir_curioso_con_paso_listo"] / max(1, listos), 4)
    v["latencia"] = GL.mide(f[0])
    return v


if __name__ == "__main__":
    V = []
    for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P734_s*_d*_*"))):
        b = os.path.basename(c).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); brazo = b[3]
        if "--solo-aprende" in sys.argv and brazo != "APRENDE": continue
        for sl in (10, 11): V.append(una(c, serie, dia, brazo, sl)); print(f"s{serie} d{dia} {brazo} a{sl}", ("sin diario" if V[-1].get("sin_diario") else f"tics {V[-1]['tics']} puesto {V[-1]['puesto']} coge {V[-1]['coge']} pruebas {{ {', '.join(f'{o}: {p['n']}' for o, p in V[-1]['pruebas'].items())} }} errores fotos {V[-1]['errores_fotos']}"), flush=True)
    json.dump(V, open(os.path.join(AQUI, "P7_34_datos.json"), "w"), ensure_ascii=False, indent=1)
    print(len(V), "vidas")
