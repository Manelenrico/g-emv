"""[P7-24/27] EL CAMPO DE LA PRIMERA ETAPA, leido de los 240 diarios (paintball/runs/P724_s<S>_d<D>_<BRAZO>_<semilla>/, dos asientos). Coste cero.
  python3 analiza_P7_24.py -> P7_24_vidas.json (una entrada por vida) y P7_24_resumen.json (medidas, exclusiones y el sello E1-E6)
Definiciones: las del sello (SELLO_P7_24.md). Partidas con corte (artefacto ausente; `PARCIAL_agent_<asiento>.json`): el aprendizaje cuenta hasta el corte; la partida
entera sale de puesto, vida al morir y causa; en las emparejadas se quita el par de ese dia y esa semilla en los brazos comparados; E4 y E5 se repiten sin excluir.
"""
import collections, glob, json, os, statistics as st
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); OBJ = {"first_aid": "botiquin", "rations": "racion"}; CURA = {"botiquin": 50.0, "racion": 15.0}


def lee(f):
    T = []; H = []; U = []; P = []; fin = None; final = None
    for line in open(f, errors="replace"):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "tick" and r.get("phase") == "live":
            n = collections.Counter()
            for s in (r.get("pack") or []):
                if s: n[s.get("id")] += int(s.get("n") or 1)
            T.append({"t": r["tick"], "hp": r.get("hp"), "n": {o: n.get(o, 0) for o in OBJ}, "el": str((r.get("RADIOGRAFIA") or {}).get("elegido") or ""), "listo": (r.get("move_ready_in") or 0) == 0})
        elif k == "P7_huella": H.append(r)
        elif k == "P7_nace_uso": U.append(r)
        elif k == "P7_pido": P.append(r)
        elif k == "P7_cuaderno" and r.get("momento") == "fin": fin = r
        elif k == "final": final = r
    return T, H, U, P, fin, final


def una(x):
    carp, brazo, serie, dia, semilla, slot = x
    f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log")); marca = glob.glob(os.path.join(carp, f"PARCIAL_agent_{slot}.json"))
    v = {"campo": "P7-24", "brazo": brazo, "serie": serie, "dia": dia, "semilla": semilla, "slot": slot, "parcial": (json.load(open(marca[0])) if marca else None)}
    if not f: v["sin_diario"] = True; return v
    T, H, U, P, fin, final = lee(f[0]); v["tics"] = len(T); v["ultimo_tick"] = T[-1]["t"] if T else None
    if not T: v["sin_diario"] = True; return v
    v["puesto"] = (final or {}).get("placement"); v["causa"] = (final or {}).get("reason"); v["murio"] = (final or {}).get("reason") == "eliminated"; v["vida_al_morir"] = T[-1]["hp"] if v["murio"] else None
    v["primer_contacto"] = {OBJ[o]: next((T[i]["t"] for i in range(1, len(T)) if T[i]["n"][o] > T[i - 1]["n"][o]), None) for o in OBJ}
    v["coge"] = {OBJ[o]: sum(max(0, T[i]["n"][o] - T[i - 1]["n"][o]) for i in range(1, len(T))) for o in OBJ}
    usos = {"botiquin": [], "racion": []}
    for h in H:
        o = OBJ.get(h.get("objeto") or "first_aid", "botiquin")
        usos[o].append({"t0": h["t0"], "hp0": h["hp0"], "completado": not h.get("corte"), "al_menos": bool(h.get("al_menos")), "firme": bool(not h.get("corte") and not h.get("al_menos") and h.get("apuntado")), "efecto": h["efecto"]["cuerpo"], "situacion": h.get("situacion")})
    v["usos"] = usos
    v["primer_firme"] = {o: next((u["t0"] for u in usos[o] if u["firme"]), None) for o in usos}
    cr = ((fin or {}).get("contenido") or {}).get("creencias") or {}
    v["al_acabar"] = {}
    for o, nom in OBJ.items():
        c = cr.get(o) or {}
        v["al_acabar"][nom] = {"creencia": {s_: (x or {}).get("cuerpo") for s_, x in c.items() if s_ not in ("ignorancia", "pesos_vividos") and x}, "ignorancia": c.get("ignorancia", 1.0 if brazo != "TECHO" else None)}
    rec = (((fin or {}).get("contenido") or {}).get("objetos") or {})
    v["recuerdos_al_acabar"] = {OBJ[o]: {"total": sum(len(s_) for s_ in (rec.get(o) or {}).get("situaciones", {}).values()), "firmes": sum(1 for s_ in (rec.get(o) or {}).get("situaciones", {}).values() for r_ in s_ if not r_.get("corte") and not r_.get("al_menos")), "al_menos": sum(1 for s_ in (rec.get(o) or {}).get("situaciones", {}).values() for r_ in s_ if r_.get("al_menos")), "cortes": sum(1 for s_ in (rec.get(o) or {}).get("situaciones", {}).values() for r_ in s_ if r_.get("corte"))} for o in OBJ}
    e1 = next((u for u in U if (u.get("esperanza") or 0) > 0), None); v["esperanza_aparece"] = ({"tick": e1["tick"], "objeto": OBJ.get(e1["objeto"], e1["objeto"]), "vale": e1["esperanza"]} if e1 else None)
    v["aperturas_botiquin_hp"] = [u["hp"] for u in U if OBJ.get(u.get("objeto"), u.get("objeto")) == "botiquin"]
    v["pedidos_abre"] = sum(1 for p in P if p.get("abre")); v["tics_pidiendo"] = sum(1 for p in P if p.get("pide"))
    el = collections.Counter(t["el"] for t in T); v["regalos"] = {k: n for k, n in el.items() if k.startswith("soltar_")}
    v["ir_curioso_tics"] = el.get("ir_curioso", 0); v["ir_curioso_con_paso_listo"] = sum(1 for t in T if t["listo"] and t["el"] == "ir_curioso"); v["tics_con_paso_listo"] = sum(1 for t in T if t["listo"])
    return v


if __name__ == "__main__":
    tareas = []
    for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P724_s*_d*_*_*"))):
        b = os.path.basename(c).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); brazo = b[3]; semilla = int(b[4])
        for sl in (10, 11): tareas.append((c, brazo, serie, dia, semilla, sl))
    with Pool(4) as P: V = P.map(una, tareas)
    V = {f"s{v['serie']}_d{v['dia']}_{v['brazo']}_{v['slot']}": v for v in V}
    json.dump(V, open(os.path.join(AQUI, "P7_24_vidas.json"), "w"), ensure_ascii=False, indent=0)
    print("vidas", len(V), "· sin diario", sum(1 for v in V.values() if v.get("sin_diario")), "· parciales", sum(1 for v in V.values() if v.get("parcial")))
