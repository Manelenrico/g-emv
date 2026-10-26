"""8 · Sensibilidad del criterio de P7-55 (analiza_P7_55.py:59-60) al umbral para lo inutil (red, camuflaje), sobre P7_55_datos.json.
Cuenta hermana-dias con a (todo, sin duplicados) > umbral y b (solo vivido) <= umbral; y el maximo de a con b = 0 en los 20 dias."""
import json, os
from comun import P7
D = json.load(open(os.path.join(P7, "P7_55_datos.json")))["por_dia"]
for u in (5, 4, 3, 2, 1):
    hits = [(h, x["dia"], o) for h, dias in D.items() for x in dias for o in ("red", "camuflaje")
            if (x[o]["a_todos_dedup"] or 0) > u and (x[o]["b_vividos"] or 0) <= u]
    print("umbral >", u, "hermana-dias", len(hits), "hermanas", sorted({h for h, _, _ in hits}))
for o in ("red", "camuflaje"):
    best = max(((x[o]["a_todos_dedup"] or 0, h, x["dia"], x[o]["b_vividos"]) for h, dias in D.items() for x in dias if not (x[o]["b_vividos"] or 0)), default=None)
    alto = max(((x[o]["a_todos_dedup"] or 0, h, x["dia"], x[o]["b_vividos"]) for h, dias in D.items() for x in dias), default=None)
    print(o, "max a con b=0:", best, "| max a en todo:", alto)
