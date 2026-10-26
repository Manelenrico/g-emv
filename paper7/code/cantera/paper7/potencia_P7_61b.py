"""[P7-61, addendum 2] POTENCIA de M1b y M2b con el ruido de CON_RAZON de P7-56.
  M1b: diferencia emparejada (confianza cuerpo justo despues − justo antes) en cada evaluacion de una invitacion FALSA (tabla del mundo) de P7-56: media, sd, evaluaciones necesarias para
       que una caida del tamano observado en las falsas de P7-56 sea >= 3 ee, y el efecto minimo con N evaluaciones.
  M2b: por criatura de P7-56 (6) y por un dia de referencia d* = 9..18 (no hay falsa en P7-56): p(aceptar una verdadera con promesa de cuerpo != 0) en las invitaciones de los dias d*+1 y d*+2
       menos la de d*-1 y d*; sd de ese cambio entre criaturas (media sobre d*): es el ruido de la comparacion "misma criatura, misma ventana" en CON_RAZON.  python3 potencia_P7_61b.py"""
import glob, json, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); sys.path.insert(0, AQUI)
E = json.load(open(os.path.join(AQUI, "P7_56_estado.json"))); src = open(os.path.join(AQUI, "analiza_P7_56.py")).read(); ns = {}; exec(src[src.index("def verdad"):src.index("\n\n\ndef vida")], ns); verdad = ns["verdad"]
import razon_P7_54 as RZ
def invit(S, d, sl):
    f = os.path.join(AQUI, "cuadernos_P7_56", f"CON_RAZON_serie{S}", f"razon_s{S}_d{d - 1}_{sl}.txt")
    return [x for x in (RZ.parsea(l) for l in open(f).read().split("\n") if l.strip().startswith("INVITACION")) if x] if os.path.exists(f) else []
def regs(S, d, sl, k):
    p = next((p for p in E["peticiones"] if p["serie"] == S and p["dia"] == d and p["brazo"] == "CON_RAZON"), None)
    fs = glob.glob(os.path.join(RUNS, f"P756_s{S}_d{d}_CON_RAZON_{p['semilla']}", f"*policy_agent_{sl}.art.log")) if p else []
    return [json.loads(l) for l in open(fs[0], errors="replace") if l.startswith('{"k":"' + k + '"')] if fs else []
# M1b
dif = []
for S in (1, 2, 3):
    for d in range(2, 21):
        for sl in (10, 11):
            inv = invit(S, d, sl)
            for e in regs(S, d, sl, "P7_54_evaluada"):
                i = inv[e["n"]] if e["n"] < len(inv) else None
                if i and not verdad(i["accion"], {"anillo": i["anillo"], "calma": i["calma"]}, i["cuerpo"]): dif.append(e["confianza_despues"]["cuerpo"] - e["confianza_antes"]["cuerpo"])
m, s = st.mean(dif), st.stdev(dif)
M1b = {"n_falsas_P7_56": len(dif), "media_diferencia": round(m, 4), "sd": round(s, 4), "evaluaciones_para_3ee": math.ceil(9 * s * s / (m * m)) if m else None, "efecto_min_con_10": round(3 * s / math.sqrt(10), 4), "efecto_min_con_30": round(3 * s / math.sqrt(30), 4)}
# M2b
def p_acc(S, sl, dias):
    tot = 0; acc = 0
    for d in dias:
        if not (2 <= d <= 20): continue
        inv = invit(S, d, sl); ac = {a["n"] for a in regs(S, d, sl, "P7_54_aceptada")}
        for k, i in enumerate(inv):
            if i["cuerpo"] != 0 and verdad(i["accion"], {"anillo": i["anillo"], "calma": i["calma"]}, i["cuerpo"]): tot += 1; acc += (k in ac)
    return acc / tot if tot else None
cambios = {}
for S in (1, 2, 3):
    for sl in (10, 11):
        xs = []
        for ds in range(9, 19):
            a, b = p_acc(S, sl, (ds + 1, ds + 2)), p_acc(S, sl, (ds - 1, ds))
            if a is not None and b is not None: xs.append(a - b)
        cambios[f"s{S} a{sl}"] = round(st.mean(xs), 4) if xs else None
v = [x for x in cambios.values() if x is not None]
todos = []
for S in (1, 2, 3):
    for sl in (10, 11):
        for ds in range(9, 19):
            a, b = p_acc(S, sl, (ds + 1, ds + 2)), p_acc(S, sl, (ds - 1, ds))
            if a is not None and b is not None: todos.append(a - b)
M2b = {"cambio_medio_por_criatura": cambios, "sd_entre_criaturas": round(st.stdev(v), 4) if len(v) > 1 else None, "sd_de_un_cambio": round(st.stdev(todos), 4), "p_base": round(st.mean(p for p in (p_acc(S, sl, range(9, 21)) for S in (1, 2, 3) for sl in (10, 11)) if p is not None), 4),
       "efecto_min_6_criaturas_frente_a_6": round(3 * st.stdev(todos) * math.sqrt(2 / 6), 4), "efecto_min_9_frente_a_6": round(3 * st.stdev(todos) * math.sqrt(1 / 9 + 1 / 6), 4)}
R = {"M1b": M1b, "M2b": M2b}; json.dump(R, open(os.path.join(AQUI, "P7_61_potencia_b.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False))
