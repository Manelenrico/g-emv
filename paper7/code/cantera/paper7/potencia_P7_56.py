"""[P7-56] POTENCIA DE R1 con P7-50 (COMPARTE, 3 series x 2 hermanas; tambien SOLAS como segunda referencia): usos del botiquin (huellas vividas) y cortados por un golpe (corte y
dano_total > 0), por serie y brazo; fraccion, ruido entre series (sd) y binomial (sqrt(p(1-p)/N)); series por brazo para ver una reduccion del 30 % y del 50 % a 3 ee.
  python3 potencia_P7_56.py -> P7_56_potencia.json"""
import glob, json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); E = json.load(open(os.path.join(AQUI, "P7_50_estado.json")))
R = {}
for b in ("COMPARTE", "SOLAS"):
    series = {}
    for p in E["peticiones"]:
        if p["brazo"] != b or p["estado"] != "completed": continue
        c = glob.glob(os.path.join(RUNS, f"P750_s{p['serie']}_d{p['dia']}_{b}_{p['semilla']}"))
        if not c: continue
        for sl in (10, 11):
            for f in glob.glob(os.path.join(c[0], f"*policy_agent_{sl}.art.log")):
                for line in open(f, errors="replace"):
                    if not line.startswith('{"k":"P7_huella"'): continue
                    h = json.loads(line)
                    if (h.get("objeto") or "first_aid") != "first_aid": continue
                    s = series.setdefault(p["serie"], {"usos": 0, "cortados": 0, "por_hermana": {10: [0, 0], 11: [0, 0]}}); s["usos"] += 1; s["por_hermana"][sl][0] += 1
                    if h.get("corte") and float(h.get("dano_total") or 0) > 0: s["cortados"] += 1; s["por_hermana"][sl][1] += 1
    fr = [s["cortados"] / s["usos"] for s in series.values() if s["usos"]]; mu = st.mean(fr); sd = st.stdev(fr) if len(fr) > 1 else 0.0; N = st.mean(s["usos"] for s in series.values()); binom = math.sqrt(mu * (1 - mu) / N)
    out = {"por_serie": {str(k): {**v, "fraccion": round(v["cortados"] / v["usos"], 3) if v["usos"] else None} for k, v in series.items()}, "usos_3_series": sum(s["usos"] for s in series.values()), "cortados_3_series": sum(s["cortados"] for s in series.values()), "fraccion_media": round(mu, 3), "sd_entre_series": round(sd, 3), "ee_binomial_por_serie": round(binom, 3), "usos_por_serie": round(N, 1)}
    for e in (0.3, 0.5):
        ef = e * mu; out[f"series_{int(100 * e)}_sd"] = math.ceil(18 * sd * sd / (ef * ef)) if ef > 0 and sd > 0 else None; out[f"series_{int(100 * e)}_binomial"] = math.ceil(18 * binom * binom / (ef * ef)) if ef > 0 else None
    out["efecto_min_3_series_pct_sd"] = round(100 * 3 * sd * math.sqrt(2 / 3) / mu, 1) if mu else None; out["efecto_min_3_series_pct_binomial"] = round(100 * 3 * binom * math.sqrt(2 / 3) / mu, 1) if mu else None
    R[b] = out
json.dump(R, open(os.path.join(AQUI, "P7_56_potencia.json"), "w"), ensure_ascii=False, indent=1)
for b, o in R.items(): print(b, {k: v for k, v in o.items() if k != "por_serie"}, {k: (v["usos"], v["cortados"], v["fraccion"]) for k, v in o["por_serie"].items()})
