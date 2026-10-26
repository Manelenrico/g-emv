"""[P7-30] EL SEGUNDO CAMPO DE LA PRIMERA ETAPA, leido de los 240 diarios (paintball/runs/P730_s<S>_d<D>_<BRAZO>_<semilla>/, dos asientos). Coste cero.
  python3 analiza_P7_30.py -> P7_30_vidas.json (una entrada por vida, las mismas claves que P7_24_vidas.json y las nuevas de P7-30)
Definiciones: las del sello (SELLO_P7_30.md). Lo nuevo frente a analiza_P7_24: firmes, "al menos" y cortes aparte por objeto (huellas y cuaderno); la ignorancia del cuanto y lo mas
alto que sabe al cerrar el dia; en cada apertura del botiquin (`P7_nace_uso`), si le pesaba la curiosidad del cuanto (hp_max - hp > sabido_max en ese momento: el del cuaderno de
arranque mas los usos completados anteriores del dia); la latencia (`guarda_latencia_P7_29.mide`); los cortes con su causa (recuerdos `acto`)."""
import collections, glob, json, os
from multiprocessing import Pool
import analiza_P7_24 as A24, guarda_latencia_P7_29 as GL, analiza_P7_16 as A16, analiza_P7_21 as A21
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); OBJ = A24.OBJ


def lee(f):
    T, H, U, P, fin, final = A24.lee(f); arr = None; cuanto = []
    for line in open(f, errors="replace"):
        if '"P7_cuaderno"' not in line and '"P7_cuanto"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") == "P7_cuaderno" and r.get("momento") == "arranque": arr = r
        elif r.get("k") == "P7_cuanto": cuanto.append(r)
    return T, H, U, P, fin, final, arr, cuanto


def una(x):
    carp, brazo, serie, dia, semilla, slot = x
    f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log")); marca = glob.glob(os.path.join(carp, f"PARCIAL_agent_{slot}.json"))
    v = {"campo": "P7-30", "brazo": brazo, "serie": serie, "dia": dia, "semilla": semilla, "slot": slot, "parcial": (json.load(open(marca[0])) if marca else None)}
    if not f: v["sin_diario"] = True; return v
    T, H, U, P, fin, final, arr, cuanto = lee(f[0]); v["tics"] = len(T); v["ultimo_tick"] = T[-1]["t"] if T else None
    if not T: v["sin_diario"] = True; return v
    v["puesto"] = (final or {}).get("placement"); v["causa"] = (final or {}).get("reason"); v["murio"] = (final or {}).get("reason") == "eliminated"; v["vida_al_morir"] = T[-1]["hp"] if v["murio"] else None
    v["primer_contacto"] = {OBJ[o]: next((T[i]["t"] for i in range(1, len(T)) if T[i]["n"][o] > T[i - 1]["n"][o]), None) for o in OBJ}
    v["coge"] = {OBJ[o]: sum(max(0, T[i]["n"][o] - T[i - 1]["n"][o]) for i in range(1, len(T))) for o in OBJ}
    usos = {"botiquin": [], "racion": []}
    for h in H:
        o = OBJ.get(h.get("objeto") or "first_aid", "botiquin")
        usos[o].append({"t0": h["t0"], "hp0": h["hp0"], "completado": not h.get("corte"), "al_menos": bool(h.get("al_menos")), "firme": bool(not h.get("corte") and not h.get("al_menos") and h.get("apuntado")), "efecto": h["efecto"]["cuerpo"], "situacion": h.get("situacion"), "dano_en_ventana": h.get("dano_total"), "fuentes": h.get("fuentes_conocidas")})
    v["usos"] = usos
    v["primer_firme"] = {o: next((u["t0"] for u in usos[o] if u["firme"]), None) for o in usos}
    v["cuenta_usos"] = {o: {"canales": len(u), "firmes": sum(1 for x in u if x["firme"]), "al_menos": sum(1 for x in u if x["al_menos"]), "cortes": sum(1 for x in u if not x["completado"])} for o, u in usos.items()}
    cr = ((fin or {}).get("contenido") or {}).get("creencias") or {}; rec = (((fin or {}).get("contenido") or {}).get("objetos") or {})
    v["al_acabar"] = {}
    for o, nom in OBJ.items():
        c = cr.get(o) or {}
        v["al_acabar"][nom] = {"creencia": {s_: x.get("cuerpo") for s_, x in c.items() if isinstance(x, dict)}, "ignorancia": c.get("ignorancia", 1.0 if brazo != "TECHO" else None), "ignorancia_cuanto": c.get("ignorancia_cuanto", 1.0 if brazo != "TECHO" else None), "sabido_max": c.get("sabido_max"), "pesos_firmes": c.get("pesos_firmes")}
    v["recuerdos_al_acabar"] = {OBJ[o]: {"total": sum(len(s_) for s_ in (rec.get(o) or {}).get("situaciones", {}).values()), "firmes": sum(1 for s_ in (rec.get(o) or {}).get("situaciones", {}).values() for r_ in s_ if not r_.get("corte") and not r_.get("al_menos")), "al_menos": sum(1 for s_ in (rec.get(o) or {}).get("situaciones", {}).values() for r_ in s_ if r_.get("al_menos")), "cortes": sum(1 for s_ in (rec.get(o) or {}).get("situaciones", {}).values() for r_ in s_ if r_.get("corte"))} for o in OBJ}
    v["causas_de_corte"] = [{"objeto": OBJ.get(o, o), "dia": r_.get("dia"), **(r_.get("causa_corte") or {})} for o in OBJ for s_ in (rec.get(o) or {}).get("situaciones", {}).values() for r_ in s_ if r_.get("corte") and r_.get("dia") == ((fin or {}).get("contenido") or {}).get("dia")]
    # las aperturas del botiquin: vida, y si le pesaba la curiosidad del cuanto (hp_max - hp > sabido_max en ese momento)
    rec0 = (((arr or {}).get("contenido") or {}).get("objetos") or {}).get("first_aid") or {}
    sab0 = [float(r_["efecto"]["cuerpo"]) for s_ in (rec0.get("situaciones") or {}).values() for r_ in s_ if not r_.get("corte")]
    aps = []
    for u in U:
        if OBJ.get(u.get("objeto"), u.get("objeto")) != "botiquin": continue
        sab = sab0 + [x["efecto"] for x in usos["botiquin"] if x["completado"] and x["t0"] < u["tick"]]; s_max = max(sab) if sab else None
        hp = float(u.get("hp") or 0.0); aps.append({"tick": u["tick"], "hp": hp, "sabido_max": s_max, "le_pesa_el_cuanto": bool(s_max is not None and (100.0 - hp) > s_max), "conocido": s_max is not None})
    v["aperturas_botiquin"] = aps; v["aperturas_botiquin_hp"] = [a["hp"] for a in aps]
    e1 = next((u for u in U if (u.get("esperanza") or 0) > 0), None); v["esperanza_aparece"] = ({"tick": e1["tick"], "objeto": OBJ.get(e1["objeto"], e1["objeto"]), "vale": e1["esperanza"]} if e1 else None)
    v["pedidos_abre"] = sum(1 for p in P if p.get("abre")); v["tics_pidiendo"] = sum(1 for p in P if p.get("pide"))
    el = collections.Counter(t["el"] for t in T); v["regalos"] = {k: n for k, n in el.items() if k.startswith("soltar_")}
    v["ir_curioso_tics"] = el.get("ir_curioso", 0); v["ir_curioso_con_paso_listo"] = sum(1 for t in T if t["listo"] and t["el"] == "ir_curioso"); v["tics_con_paso_listo"] = sum(1 for t in T if t["listo"])
    v["cuanto_muestras"] = [{"tick": c["tick"], "M": c.get("M"), "M_curiosidad": c.get("M_curiosidad")} for c in cuanto[::4]]
    v["latencia"] = GL.mide(f[0]); v["cuaderno_leido"] = bool((arr or {}).get("leido"))
    if brazo == "TECHO":          # TECHO no escribe recuerdos: sus usos del botiquin salen de los canales del diario (P7-21), como en P7-24
        M16, T16 = A16.lee(f[0]); C = A21.canales(T16, A21.lee_extra(f[0]), M16) if T16 else []
        v["canales_techo"] = {"canales": len(C), "completados": sum(1 for c in C if c["completado"]), "hp": [c["hp0"] for c in C]}
    return v


if __name__ == "__main__":
    tareas = []
    for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P730_s*_d*_*_*"))):
        b = os.path.basename(c).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); brazo = b[3]; semilla = int(b[4])
        for sl in (10, 11): tareas.append((c, brazo, serie, dia, semilla, sl))
    with Pool(4) as P: V = P.map(una, tareas)
    V = {f"s{v['serie']}_d{v['dia']}_{v['brazo']}_{v['slot']}": v for v in V}
    json.dump(V, open(os.path.join(AQUI, "P7_30_vidas.json"), "w"), ensure_ascii=False, indent=0)
    print("vidas", len(V), "· sin diario", sum(1 for v in V.values() if v.get("sin_diario")), "· parciales", sum(1 for v in V.values() if v.get("parcial")), "· guarda no pasa", sum(1 for v in V.values() if not v.get("sin_diario") and not v["latencia"]["pasa"]))
