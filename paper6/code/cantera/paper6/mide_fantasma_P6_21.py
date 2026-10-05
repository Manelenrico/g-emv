"""[P6-21 · 3, apoyo] ACCIONES FANTASMA Y PASOS PERDIDOS: la firma del retraso. SOLO LECTURA
de los 120 diarios de A4, A5h y A6, de uno en uno.

El juego resuelve en cada tic la primera accion que le llega de cada cuerpo (sim.nim,
`submitAction`); la respuesta (`action_result`) de un tic sin accion pendiente conserva la
anterior. Dos firmas de que las acciones llegan tarde:
  · FANTASMA: en el tic t la respuesta es `cooldown` o `blocked` (solo las produce un paso
    resuelto en t-1) y el cuerpo NO envio un paso en t-1 (`intencion` none u otra cosa): el
    juego resolvio un paso que el cuerpo habia enviado antes. Se anota cuantos tics antes
    envio el ultimo paso (retraso minimo).
  · PERDIDO: en t-1 el cuerpo envio un paso con las piernas listas (`move_ready_in` 0) a una
    casilla libre (no solida, sin cuerpo visto), en t la respuesta es `ok`, la casilla no
    cambia y las piernas siguen listas: el juego no tuvo ese paso como pendiente.
Se cuentan por brazo y fase (antes / desde el aviso 5), y por tic con cuerpo vivo.
"""
import collections, glob, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
BRAZOS = {"A4": "paintball/runs/P611_t*_A4_*", "A5h": "paintball/runs/P616_t2_A5h_*", "A6": "paintball/runs/P618_t1_A6_*"}
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}
K = collections.defaultdict(collections.Counter); RETF = collections.defaultdict(list); VIDAS = collections.defaultdict(list)
for brazo, pat in BRAZOS.items():
    for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            continue
        sem = int(carp.rsplit("_", 1)[1])
        for sl in (10, 11):
            recs = list(U.lee(fs[sl]))
            pc = next(r for r in recs if r["k"] == "player_config"); cat = next(r for r in recs if r["k"] == "catalogo"); sm = next(r for r in recs if r["k"] == "static_map")
            mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); warn5 = pc["zone_schedule"][4][0]
            T = {}
            for r in recs:
                if r.get("k") == "tick" and r.get("phase") == "live":
                    T[r["tick"]] = {"pos": (int(r["pos"][0]), int(r["pos"][1])), "int": r.get("intencion") or {}, "mri": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0), "ar": r.get("action_result_obs", r.get("action_result")),
                                    "ve": {tuple(a["pos"]) for a in (r.get("ve_agentes") or []) if a.get("pos")}}
            del recs
            ts = sorted(T); ult_paso = None; v = collections.Counter()
            for t in ts:
                r = T[t]; fase = "fase5+" if t >= warn5 else "fases1-4"; k = K[(brazo, fase)]; k["tics"] += 1
                prev = T.get(t - 1)
                if prev is None:
                    if r["int"].get("do") == "move":
                        ult_paso = t
                    continue
                pm = prev["int"].get("do") == "move" and prev["int"].get("dir") in DIRS
                if r["ar"] in ("cooldown", "blocked") and not pm:
                    k["fantasma"] += 1; v["fantasma"] += 1
                    if ult_paso is not None:
                        RETF[(brazo, fase)].append(t - 1 - ult_paso)
                if pm and prev["mri"] == 0:
                    dx, dy = DIRS[prev["int"]["dir"]]; dest = (prev["pos"][0] + dx, prev["pos"][1] + dy)
                    libre = not mundo.solido(dest[0], dest[1]) and dest not in prev["ve"]
                    k["pasos enviados listos"] += 1
                    if libre:
                        k["pasos a casilla libre"] += 1
                        if r["ar"] == "ok" and r["pos"] == prev["pos"] and r["mri"] == 0:
                            k["perdido"] += 1; v["perdido"] += 1
                        elif r["pos"] == dest:
                            k["dado en el tic"] += 1
                if r["int"].get("do") == "move":
                    ult_paso = t
            VIDAS[brazo].append({"sem": sem, "slot": sl, "fantasma": v["fantasma"], "perdido": v["perdido"], "tics_fase5": sum(1 for t in ts if t >= warn5)})
        print(f"  {brazo} {sem}", flush=True)


def q(xs):
    v = sorted(xs); n = len(v)
    return {"n": n, "mediana": (v[n // 2] if n else None), "p90": (v[int(0.9 * n)] if n else None), "max": (v[-1] if n else None)} if n else {"n": 0}


R = {"nota": "P6-21 §3 apoyo. Firmas del retraso: fantasma (respuesta cooldown/blocked sin paso enviado en t-1) y perdido (paso listo a casilla libre, respuesta ok, sin moverse, piernas listas).",
     "por_brazo_fase": {f"{b} | {f}": dict(k, pct_fantasma=round(100 * k["fantasma"] / max(1, k["tics"]), 2), pct_perdido=round(100 * k["perdido"] / max(1, k["pasos a casilla libre"]), 1), retraso_minimo_fantasma=q(RETF[(b, f)])) for (b, f), k in sorted(K.items())},
     "vidas": {b: {"n": len(v), "con_fantasmas": sum(1 for x in v if x["fantasma"] > 0), "con_perdidos": sum(1 for x in v if x["perdido"] > 0), "lista": v} for b, v in VIDAS.items()}}
json.dump(R, open(os.path.join(AQUI, "P6_21_fantasma.json"), "w"), ensure_ascii=False, indent=1)
for k, v in R["por_brazo_fase"].items():
    print("  ", k, v)
for b, v in R["vidas"].items():
    print("  ", b, {kk: vv for kk, vv in v.items() if kk != "lista"})
print("-> P6_21_fantasma.json")
