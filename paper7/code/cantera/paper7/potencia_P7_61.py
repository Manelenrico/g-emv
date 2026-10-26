"""[P7-61] POTENCIA de M1-M3 con el ruido de CON_RAZON de P7-56 (SELLO_P7_61.md), y la vigilancia que faltaba de P7-56 (puesto medio, vida perdida y muertes por brazo y hermana).
  M1: confianza en el cuerpo, media de los dias 14-20 (las dos hermanas), por serie.  M2: fraccion de invitaciones verdaderas (tabla del mundo) aceptadas al menos una vez, dias 12-20, por serie.
  M3 (sustituto): aceptaciones por oportunidad de las invitaciones USAR_BOTIQUIN verdaderas de la valiente (asiento 10), dias 10-20, por serie.
  Series por brazo para ver un efecto del 30 % y del 50 % a 3 ee (n >= 18 sd^2 / efecto^2); efecto minimo con 3 series.  python3 potencia_P7_61.py -> P7_61_potencia.json"""
import glob, json, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); sys.path.insert(0, AQUI)
E = json.load(open(os.path.join(AQUI, "P7_56_estado.json"))); src = open(os.path.join(AQUI, "analiza_P7_56.py")).read(); ns = {}; exec(src[src.index("def verdad"):src.index("\n\n\ndef vida")], ns); verdad = ns["verdad"]
import razon_P7_54 as RZ
def conf(S, d, sl):
    f = os.path.join(AQUI, "P7_56_res", f"cuaderno_s{S}_d{d}_CON_RAZON_{sl}.json")
    try: return (json.load(open(f)).get("confianza_razon_P7_54") or {}).get("cuerpo")
    except Exception: return None
def invit(S, d, sl):
    f = os.path.join(AQUI, "cuadernos_P7_56", f"CON_RAZON_serie{S}", f"razon_s{S}_d{d - 1}_{sl}.txt")
    if not os.path.exists(f): return []
    return [x for x in (RZ.parsea(l) for l in open(f).read().split("\n") if l.strip().startswith("INVITACION")) if x]
def registros(S, d, sl, k):
    p = next((p for p in E["peticiones"] if p["serie"] == S and p["dia"] == d and p["brazo"] == "CON_RAZON"), None)
    fs = glob.glob(os.path.join(RUNS, f"P756_s{S}_d{d}_CON_RAZON_{p['semilla']}", f"*policy_agent_{sl}.art.log")) if p else []
    return [json.loads(l) for l in open(fs[0], errors="replace") if l.startswith('{"k":"' + k + '"')] if fs else []
M1 = []; M2 = []; M3 = []
for S in (1, 2, 3):
    c = [conf(S, d, sl) for d in range(14, 21) for sl in (10, 11)]; c = [x for x in c if x is not None]; M1.append(st.mean(c) if c else None)
    ver = 0; acc = 0
    for d in range(12, 21):
        for sl in (10, 11):
            inv = invit(S, d, sl); ac = {a["n"] for a in registros(S, d, sl, "P7_54_aceptada")}
            for k, i in enumerate(inv):
                if verdad(i["accion"], {"anillo": i["anillo"], "calma": i["calma"]}, i["cuerpo"]): ver += 1; acc += (k in ac)
    M2.append(acc / ver if ver else None)
    op = 0; ac3 = 0
    for d in range(10, 21):
        inv = invit(S, d, 10); ks = [k for k, i in enumerate(inv) if i["accion"] == "USAR_BOTIQUIN" and verdad(i["accion"], {"anillo": i["anillo"], "calma": i["calma"]}, i["cuerpo"])]
        if not ks: continue
        act = {a["n"] for a in registros(S, d, 10, "P7_54_activa")}; acs = [a for a in registros(S, d, 10, "P7_54_aceptada") if a["n"] in ks]
        if any(k in act for k in ks): op += 1; ac3 += len(acs)
    M3.append(ac3 / op if op else None)
def pot(xs):
    xs = [x for x in xs if x is not None]; mu = st.mean(xs); sd = st.stdev(xs) if len(xs) > 1 else 0.0; o = {"valores": [round(x, 4) for x in xs], "media": round(mu, 4), "sd": round(sd, 4)}
    for e in (0.3, 0.5): ef = e * mu; o[f"series_{int(100 * e)}"] = (math.ceil(18 * sd * sd / (ef * ef)) if ef and sd else None)
    o["efecto_min_3_series_pct"] = round(100 * 3 * sd * math.sqrt(2 / 3) / mu, 1) if mu else None; return o
# vigilancia que faltaba de P7-56: puesto, vida perdida, muertes por brazo y hermana (sumando las series)
VG = json.load(open(os.path.join(AQUI, "P7_56_sello.json")))["con_todas"]["vigilancia"]; vig = {}
for b in ("CON_RAZON", "SIN_RAZON"):
    for h in ("valiente", "prudente"):
        xs = [VG[f"s{S} {b}"] for S in (1, 2, 3)]
        vig[f"{b} · {h}"] = {"puesto_medio": round(st.mean(x["puesto"][h] for x in xs), 2), "vida_perdida_media": round(st.mean(x["vida_perdida"][h] for x in xs), 1), "muertes": sum(x["muertes"][h] for x in xs), "vidas": 60}
R = {"M1": pot(M1), "M2": pot(M2), "M3_sustituto": pot(M3), "vigilancia_P7_56": vig}
json.dump(R, open(os.path.join(AQUI, "P7_61_potencia.json"), "w"), ensure_ascii=False, indent=1)
for k, v in R.items(): print(k, v)
