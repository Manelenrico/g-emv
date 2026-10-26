"""6 · Desglose de las partidas de P7-67 campo desde P7_67F_estado.json y las carpetas de paintball/runs."""
import collections as C, glob, json, os
from comun import P7, RUNS
E = json.load(open(os.path.join(P7, "P7_67F_estado.json")))
P = E["peticiones"]; print("peticiones", len(P), C.Counter(p["estado"] for p in P))
k = [(p["nivel"], p["brazo"], p["serie"], p["dia"]) for p in P]; print("duplicados", len(k) - len(set(k)))
for niv in sorted({p["nivel"] for p in P}, key=int):
    q = [p for p in P if p["nivel"] == niv]
    print("nivel", niv, "partidas", len(q), "brazos", dict(C.Counter(p["brazo"] for p in q)), "series", len({p["serie"] for p in q}), "dias", min(p["dia"] for p in q), "-", max(p["dia"] for p in q))
print("cadenas", len({(p["nivel"], p["brazo"], p["serie"]) for p in P}))
car = [os.path.basename(d) for d in glob.glob(os.path.join(RUNS, "P767F_*"))]
print("carpetas", len(car), "apartadas", sorted(c for c in car if "apartada" in c))
