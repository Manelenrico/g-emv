"""[P6-21 · 3, apoyo] EL RETRASO ENTRE EL PASO ENVIADO Y EL PASO DADO. SOLO LECTURA de los
120 diarios de A4, A5h y A6, de uno en uno.

El juego ejecuta, en cada tic, la primera accion que le llega de cada cuerpo (sim.nim,
`submitAction`: si ya hay una pendiente, la nueva se ignora sin respuesta; `action_result`
conserva el «ok» anterior). Si el cuerpo va con retraso respecto al reloj del mundo, sus
pasos llegan tarde y en rachas: uno se ejecuta tics despues de enviado y los demas se
pierden. Aqui se mide, para cada paso DADO (la casilla cambia de t a t+1 en una de las ocho
direcciones), cuantos tics antes se envio por ultima vez un `intencion` move con esa misma
direccion desde esa casilla: retraso 0 = el paso enviado en t se dio en t; retraso k > 0 =
el paso que se dio es uno enviado k tics antes. Se da por brazo y por fase (antes / desde
el aviso 5), con mediana, p90 y la fraccion con retraso >= 3.
"""
import collections, glob, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
BRAZOS = {"A4": "paintball/runs/P611_t*_A4_*", "A5h": "paintball/runs/P616_t2_A5h_*", "A6": "paintball/runs/P618_t1_A6_*"}
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}
INV = {v: k for k, v in DIRS.items()}
RET = collections.defaultdict(list); ENV = collections.Counter(); DADOS = collections.Counter()
for brazo, pat in BRAZOS.items():
    for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            continue
        sem = int(carp.rsplit("_", 1)[1])
        for sl in (10, 11):
            T = {}; warn5 = None
            for r in U.lee(fs[sl]):
                if r.get("k") == "player_config":
                    warn5 = r["zone_schedule"][4][0]
                elif r.get("k") == "tick" and r.get("phase") == "live":
                    T[r["tick"]] = ((int(r["pos"][0]), int(r["pos"][1])), (r.get("intencion") or {}))
            ts = sorted(T)
            for i, t in enumerate(ts[:-1]):
                if ts[i + 1] != t + 1:
                    continue
                p0, inte = T[t]; p1 = T[t + 1][0]
                fase = "fase5+" if t >= warn5 else "fases1-4"
                if inte.get("do") == "move" and inte.get("dir") in DIRS:
                    ENV[(brazo, fase)] += 1
                if p1 == p0:
                    continue
                d = (p1[0] - p0[0], p1[1] - p0[1])
                if d not in INV:
                    continue
                DADOS[(brazo, fase)] += 1
                dr = INV[d]; k = None
                for u in range(t, max(ts[0], t - 120) - 1, -1):
                    if u in T and T[u][0] == p0 and T[u][1].get("do") == "move" and T[u][1].get("dir") == dr:
                        k = t - u; break
                RET[(brazo, fase)].append(k if k is not None else -1)
        print(f"  {brazo} {sem}", flush=True)


def q(xs):
    v = sorted(x for x in xs if x >= 0); n = len(v)
    return {"n": n, "sin envio previo en 120 tics": sum(1 for x in xs if x < 0), "retraso 0": sum(1 for x in v if x == 0), "retraso 1-2": sum(1 for x in v if 1 <= x <= 2), "retraso >= 3": sum(1 for x in v if x >= 3), "retraso >= 10": sum(1 for x in v if x >= 10),
            "mediana": (v[n // 2] if n else None), "p90": (v[int(0.9 * n)] if n else None), "max": (v[-1] if n else None), "pct >= 3": round(100 * sum(1 for x in v if x >= 3) / max(1, n), 1)}


R = {"nota": "P6-21 §3 apoyo. Retraso (tics) entre el ultimo envio de un paso en esa direccion desde esa casilla y el paso dado.", "por_brazo_fase": {f"{b} | {f}": dict(q(v), pasos_enviados=ENV[(b, f)], pasos_dados=DADOS[(b, f)]) for (b, f), v in sorted(RET.items())}}
json.dump(R, open(os.path.join(AQUI, "P6_21_retraso.json"), "w"), ensure_ascii=False, indent=1)
for k, v in R["por_brazo_fase"].items():
    print("  ", k, v)
print("-> P6_21_retraso.json")
