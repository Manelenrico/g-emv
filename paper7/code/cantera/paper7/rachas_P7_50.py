"""[P7-50, Manel 12-oct] RACHAS >= 72 TICS QUE LA REGLA v3b NO QUITO, por brazo y por hermana: en cada diario del campo (P750_*; los intentos apartados P750r_* aparte), los
empujes bloqueados sin cuerpo en la casilla destino (como la guarda), agrupados en rachas hacia la misma casilla (huecos <= 24 tics); una racha "larga" dura >= 72 tics.
Para cada racha larga: si la casilla fue marcada (`P7_43_muro`) dentro de la racha y cuanto siguio empujando despues de la marca; la accion elegida (ir_pareja, ir_objeto...).
  python3 rachas_P7_50.py -> P7_50_rachas.json"""
import collections, glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs")
DIR = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}


def vida(f):
    T = []; muros = []
    for line in open(f, errors="replace"):
        if line.startswith('{"k":"tick"'):
            r = json.loads(line)
            if r.get("phase") == "live": T.append((r["tick"], tuple(r["pos"]), r.get("action_result"), (r.get("intencion") or {}).get("dir"), (r.get("move_ready_in") or 0) == 0, {tuple(a["pos"]) for a in (r.get("ve_agentes") or []) if a.get("pos")}, str((r.get("RADIOGRAFIA") or {}).get("elegido") or "")))
        elif line.startswith('{"k":"P7_43_muro"'): muros.append(json.loads(line))
    listos = sum(1 for t in T if t[4]); bl = []; prev = None
    for t in T:
        if prev and t[2] == "blocked" and prev[3] in DIR:
            dx, dy = DIR[prev[3]]; hacia = (prev[1][0] + dx, prev[1][1] + dy)
            if hacia not in t[5]: bl.append((t[0], hacia, prev[6]))
        prev = t
    rachas = []; cur = None
    for t, h, el in bl:
        if cur and cur["hacia"] == h and t - cur["t_ult"] <= 24: cur["n"] += 1; cur["t_ult"] = t; cur["el"][el] += 1
        else:
            if cur: rachas.append(cur)
            cur = {"hacia": h, "t0": t, "t_ult": t, "n": 1, "el": collections.Counter({el: 1})}
    if cur: rachas.append(cur)
    largas = []
    for r in rachas:
        dur = r["t_ult"] - r["t0"] + 1
        if dur < 72: continue
        m = next((m for m in muros if tuple(m["casilla"]) == r["hacia"] and r["t0"] <= m["tick"] <= r["t_ult"] + 24), None)
        largas.append({"t0": r["t0"], "dur": dur, "empujes": r["n"], "hacia": list(r["hacia"]), "marcada_en_racha": bool(m), "tic_marca": (m or {}).get("tick"), "empujes_tras_marca": (sum(1 for t, h, el in bl if h == r["hacia"] and m["tick"] < t <= r["t_ult"]) if m else None), "elegido": dict(r["el"].most_common(2))})
    return {"tics": len(T), "listos": listos, "bloqueados_sin_cuerpo": len(bl), "pct": (100 * len(bl) / listos if listos else None), "rachas": len(rachas), "cortas": sum(1 for r in rachas if r["t_ult"] - r["t0"] + 1 < 72), "largas": largas, "muros": len(muros)}


if __name__ == "__main__":
    R = {}
    for pat, et in (("P750_s*", "campo"), ("P750r_s*", "apartadas")):
        for c in sorted(glob.glob(os.path.join(RUNS, pat))):
            b = os.path.basename(c).split("_"); S, d, brazo = int(b[1][1:]), int(b[2][1:]), b[3]
            for sl in (10, 11):
                fs = glob.glob(os.path.join(c, f"*policy_agent_{sl}.art.log"))
                if fs: R[f"{et} s{S} d{d} {brazo} a{sl}"] = {"grupo": et, "serie": S, "dia": d, "brazo": brazo, "asiento": sl, **vida(fs[0])}
    por = {}
    for k, v in R.items():
        if v["grupo"] != "campo": continue
        g = por.setdefault((v["brazo"], "valiente" if v["asiento"] == 10 else "prudente"), {"vidas": 0, "largas": 0, "largas_marcadas": 0, "empujes_largas": 0, "empujes_tras_marca": 0, "cortas": 0, "pct_medio": [], "elegidos": collections.Counter()})
        g["vidas"] += 1; g["largas"] += len(v["largas"]); g["largas_marcadas"] += sum(1 for x in v["largas"] if x["marcada_en_racha"]); g["empujes_largas"] += sum(x["empujes"] for x in v["largas"]); g["empujes_tras_marca"] += sum(x["empujes_tras_marca"] or 0 for x in v["largas"]); g["cortas"] += v["cortas"]; g["pct_medio"].append(v["pct"] or 0)
        for x in v["largas"]: g["elegidos"].update(x["elegido"])
    res = {f"{b} · {h}": {**{k: v for k, v in g.items() if k not in ("pct_medio", "elegidos")}, "pct_medio": round(st.mean(g["pct_medio"]), 2), "elegidos": dict(g["elegidos"].most_common(4))} for (b, h), g in por.items()}
    json.dump({"por_brazo_hermana": res, "vidas": R}, open(os.path.join(AQUI, "P7_50_rachas.json"), "w"), ensure_ascii=False, indent=1)
    for k, v in res.items(): print(k, v)
