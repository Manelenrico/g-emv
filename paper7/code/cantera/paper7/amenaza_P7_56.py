"""[P7-56, para el sello de P7-57; coste cero] Los usos del botiquin de P7-56 (CON_RAZON y SIN_RAZON) en la situacion de AMENAZA tal como la define invita_P7_57 (rival a <= 4
casillas o fuego en la apertura de la prueba, del `peligro` de P7_33_prueba; o golpe recibido en los 48 tics anteriores, de damage_taken de los ticks): cuantos, que fraccion se corto por
un golpe (corte y dano_total > 0), y cuanto curaron de media (efecto cuerpo de la huella: sobre todos los usos con los cortados a 0, y sobre los no cortados). Lo mismo SIN amenaza, para
comparar. Por brazo y serie, y total. La falsa de P7-57 se juzga por lo vivido, siempre (decision de la mesa): esta fraccion es la probabilidad de que la mentira se desmienta al usarla.
  python3 amenaza_P7_56.py -> P7_56_amenaza.json"""
import glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); E = json.load(open(os.path.join(AQUI, "P7_56_estado.json")))
mean = lambda xs: (round(st.mean(xs), 2) if xs else None)


def usos(f):
    golpes = {}; AB = []; H = []
    for line in open(f, errors="replace"):
        if line.startswith('{"k":"tick"'):
            r = json.loads(line)
            if r.get("phase") == "live":
                g = sum(float(x.get("amount") or 0) for x in (r.get("damage_taken") or []))
                if g > 0: golpes[r["tick"]] = g
        elif line.startswith('{"k":"P7_33_prueba"'):
            r = json.loads(line)
            if r.get("momento") == "abre": AB.append(r)
        elif line.startswith('{"k":"P7_huella"'): H.append(json.loads(line))
    out = []
    for h in H:
        if (h.get("objeto") or "first_aid") != "first_aid": continue
        t0 = int(h["t0"]); ab = min(AB, key=lambda a: abs(a["tick"] - t0)) if AB else None; pel = (ab.get("peligro") or {}) if ab and abs(ab["tick"] - t0) <= 24 else {}
        golpe = any(t0 - 48 <= t < t0 for t in golpes)
        amenaza = bool(pel.get("rival_a_4") or pel.get("fuego") or golpe)
        cortado = bool(h.get("corte") and float(h.get("dano_total") or 0) > 0)
        out.append({"amenaza": amenaza, "cortado": cortado, "efecto": float((h.get("efecto") or {}).get("cuerpo") or 0.0) if not h.get("corte") else 0.0, "hp0": h.get("hp0"), "al_menos": bool(h.get("al_menos"))})
    return out


R = {}
for p in E["peticiones"]:
    if p["estado"] != "completed": continue
    for sl in (10, 11):
        for f in glob.glob(os.path.join(RUNS, f"P756_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}", f"*policy_agent_{sl}.art.log")):
            for u in usos(f): R.setdefault((p["brazo"], p["serie"]), []).append(u)
def resumen(L):
    out = {}
    for k, cond in (("amenaza", True), ("sin_amenaza", False)):
        X = [u for u in L if u["amenaza"] == cond]; nc = [u for u in X if not u["cortado"]]
        out[k] = {"usos": len(X), "cortados": sum(1 for u in X if u["cortado"]), "fraccion_cortada": (round(sum(1 for u in X if u["cortado"]) / len(X), 3) if X else None), "cura_media_todos": mean([u["efecto"] for u in X]), "cura_media_no_cortados": mean([u["efecto"] for u in nc]), "al_menos_no_cortados": sum(1 for u in nc if u["al_menos"])}
    return out
S = {f"{b} s{s}": resumen(L) for (b, s), L in sorted(R.items())}
T = {b: resumen([u for (bb, s), L in R.items() if bb == b for u in L]) for b in ("CON_RAZON", "SIN_RAZON")}; T["los dos"] = resumen([u for L in R.values() for u in L])
json.dump({"por_serie": S, "total": T, "series": sorted({s for (b, s) in R})}, open(os.path.join(AQUI, "P7_56_amenaza.json"), "w"), ensure_ascii=False, indent=1)
for k, v in T.items(): print(k, v)
