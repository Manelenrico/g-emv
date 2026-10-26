"""[P7-44] ¿EL CAMUFLAJE PROTEGE? Con los diarios que ya existen: P7-34 (P734_*, 240 vidas), el piloto 1 (P741p_*, 190 vidas) y el piloto 2 (P741q_*, 24 vidas); TECHO incluido.
Por tic vivo de cada criatura: puesto = el cuerpo lleva el camuflaje (`body` = camouflage); delatado = efecto `camo_revealed` en `effects` (tras atacar); situacion =
dentro/fuera del anillo (`zona`: distancia al centro <= radio) x rival a 8 casillas o menos a la vista (ve_agentes de otro equipo).
Medidas por estado (puesto sin delatar / puesto delatado / sin camuflaje) y situacion: golpes de rivales por minuto (`damage_taken` con fuente P<slot> de otro equipo; 1.440
tics = 1 min), vida perdida por minuto por esos golpes, rivales a 4 o menos por tic (media), y "nos persiguen": rivales a 6 o menos cuya distancia a nosotros ha bajado
respecto a 24 tics antes, por tic. MISMA CRIATURA: solo vidas con >= 240 tics en cada estado (puesto sin delatar y sin camuflaje), diferencia emparejada por vida y situacion.
  python3 analiza_P7_44.py -> P7_44_datos.json"""
import collections, glob, json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); MIN = 1440.0
CAMPOS = (("P734_*", "P7-34"), ("P741p_*", "piloto 1"), ("P741q_*", "piloto 2"))


def vida(f):
    T = []; team = None
    for line in open(f, errors="replace"):
        if '"k":"tick"' not in line[:12]: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("phase") != "live": continue
        if team is None: team = r.get("team")
        pos = tuple(r.get("pos") or (0, 0)); z = r.get("zona") or {}; c = z.get("center") or (24, 24); dentro = math.dist(pos, c) <= float(z.get("radius") or 99)
        b = r.get("body"); bid = b.get("id") if isinstance(b, dict) else b; puesto = (bid == "camouflage")
        delatado = any((e.get("id") == "camo_revealed") for e in (r.get("effects") or []) if isinstance(e, dict))
        riv = [(a.get("slot"), tuple(a["pos"])) for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("team") != team]
        d = [max(abs(q[0] - pos[0]), abs(q[1] - pos[1])) for _, q in riv]
        golpes = [float(x.get("amount") or 0) for x in (r.get("damage_taken") or []) if str(x.get("source") or "").startswith("P")]
        T.append({"t": r["tick"], "pos": pos, "dentro": dentro, "puesto": puesto, "delatado": delatado, "riv": dict(riv), "r8": any(x <= 8 for x in d), "r4": sum(1 for x in d if x <= 4), "golpes": len(golpes), "dano": sum(golpes)})
    # nos persiguen: rival a <= 6 cuya distancia bajo respecto a 24 tics antes
    for i, t in enumerate(T):
        n = 0
        if i >= 24:
            for sl, q in t["riv"].items():
                d_now = max(abs(q[0] - t["pos"][0]), abs(q[1] - t["pos"][1])); q0 = T[i - 24]["riv"].get(sl)
                if q0 is not None and d_now <= 6 and d_now < max(abs(q0[0] - T[i - 24]["pos"][0]), abs(q0[1] - T[i - 24]["pos"][1])): n += 1
        t["persiguen"] = n
    return T


def acum(T):
    A = collections.defaultdict(lambda: {"tics": 0, "golpes": 0, "dano": 0.0, "r4": 0, "persiguen": 0})
    for t in T:
        est = ("puesto delatado" if (t["puesto"] and t["delatado"]) else ("puesto" if t["puesto"] else "sin camuflaje")); sit = ("dentro" if t["dentro"] else "fuera") + (" · rival≤8" if t["r8"] else " · sin rival≤8")
        fase = "fase " + str(min(4, t["t"] // 3000))          # tramo de la vida (3.000 tics): el camuflaje se lleva mas tarde, cuando el anillo aprieta
        for k in ((est, sit), (est, "todas"), (est, f"{fase} · {sit}")):
            a = A[k]; a["tics"] += 1; a["golpes"] += t["golpes"]; a["dano"] += t["dano"]; a["r4"] += t["r4"]; a["persiguen"] += t["persiguen"]
    return A


def tasas(a): return {"tics": a["tics"], "min": round(a["tics"] / MIN, 2), "golpes_min": (a["golpes"] / a["tics"] * MIN if a["tics"] else None), "dano_min": (a["dano"] / a["tics"] * MIN if a["tics"] else None), "r4_tic": (a["r4"] / a["tics"] if a["tics"] else None), "persiguen_tic": (a["persiguen"] / a["tics"] if a["tics"] else None)}


if __name__ == "__main__":
    TOT = collections.defaultdict(lambda: {"tics": 0, "golpes": 0, "dano": 0.0, "r4": 0, "persiguen": 0}); POR_CAMPO = {}; PARES = collections.defaultdict(list); vidas = 0; con_camo = 0; por_brazo = collections.defaultdict(lambda: {"tics": 0, "puesto": 0})
    for pat, et in CAMPOS:
        TC = collections.defaultdict(lambda: {"tics": 0, "golpes": 0, "dano": 0.0, "r4": 0, "persiguen": 0})
        for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))):
            brazo = os.path.basename(c).split("_")[3]
            for sl in (10, 11):
                fs = glob.glob(os.path.join(c, f"*policy_agent_{sl}.art.log"))
                if not fs or os.path.getsize(fs[0]) < 1000: continue
                T = vida(fs[0]); vidas += 1
                if not T: continue
                por_brazo[brazo]["tics"] += len(T); por_brazo[brazo]["puesto"] += sum(1 for t in T if t["puesto"])
                A = acum(T)
                for k, a in A.items():
                    for kk in ("tics", "golpes", "dano", "r4", "persiguen"): TOT[k][kk] += a[kk]; TC[k][kk] += a[kk]
                # misma criatura: pares por vida y situacion, con >= 240 tics en los dos estados
                if any(k[0] == "puesto" for k in A):
                    con_camo += 1
                    sits = ["todas", "dentro · rival≤8", "dentro · sin rival≤8", "fuera · rival≤8", "fuera · sin rival≤8"] + [f"fase {i} · {q}" for i in range(5) for q in ("dentro · rival≤8", "dentro · sin rival≤8", "fuera · rival≤8", "fuera · sin rival≤8")]
                    for sit in sits:
                        p, s = A.get(("puesto", sit)), A.get(("sin camuflaje", sit))
                        if p and s and p["tics"] >= 240 and s["tics"] >= 240:
                            tp, ts = tasas(p), tasas(s); PARES[sit].append({"vida": os.path.basename(c) + f"/{sl}", "golpes_min": tp["golpes_min"] - ts["golpes_min"], "dano_min": tp["dano_min"] - ts["dano_min"], "r4": tp["r4_tic"] - ts["r4_tic"], "persiguen": tp["persiguen_tic"] - ts["persiguen_tic"], "tics_puesto": p["tics"], "tics_sin": s["tics"]})
        POR_CAMPO[et] = {f"{k[0]} | {k[1]}": tasas(a) for k, a in TC.items()}
        print(et, "vidas acumuladas", vidas, flush=True)
    # misma criatura, mismo tramo de la vida y misma situacion: todos los pares (vida x tramo x situacion) juntos
    L = [x for sit, Ls in PARES.items() if sit.startswith("fase ") for x in Ls]
    PARES["misma fase y situación (todos los tramos)"] = L
    R = {"vidas": vidas, "vidas_con_camuflaje_puesto": con_camo, "por_brazo_fraccion_puesto": {b: round(x["puesto"] / x["tics"], 4) for b, x in por_brazo.items() if x["tics"]}, "todo": {f"{k[0]} | {k[1]}": tasas(a) for k, a in TOT.items()}, "por_campo": POR_CAMPO,
         "misma_criatura": {sit: {"n_vidas": len(L), **{m: {"media": round(st.mean(x[m] for x in L), 4), "ee": (round(st.stdev(x[m] for x in L) / len(L) ** 0.5, 4) if len(L) > 1 else None)} for m in ("golpes_min", "dano_min", "r4", "persiguen")}} for sit, L in PARES.items()}}
    json.dump(R, open(os.path.join(AQUI, "P7_44_datos.json"), "w"), ensure_ascii=False, indent=1)
    for k, v in sorted(R["todo"].items()): print(k, {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in v.items()})
    print(json.dumps(R["misma_criatura"], ensure_ascii=False)[:1500]); print(R["por_brazo_fraccion_puesto"])
