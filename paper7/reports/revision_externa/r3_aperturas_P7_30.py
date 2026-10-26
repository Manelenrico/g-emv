"""3 · Las aperturas del botiquin de APRENDE en P7-30 por la marca de analiza_P7_30.py:54 (le_pesa_el_cuanto / conocido). Lee P7_30_vidas.json."""
import json, os, statistics as st
from comun import P7
V = json.load(open(os.path.join(P7, "P7_30_vidas.json"))); V = V.values() if isinstance(V, dict) else V
G = {"le pesa": [], "conocido, no pesa": [], "sin conocer": []}; SM = {"le pesa": [], "conocido, no pesa": []}
for v in V:
    if v.get("brazo") != "APRENDE": continue
    for a in v.get("aperturas_botiquin") or []:
        g = "le pesa" if a["le_pesa_el_cuanto"] else ("conocido, no pesa" if a["conocido"] else "sin conocer"); G[g].append(a["hp"])
        if g in SM: SM[g].append(a["sabido_max"])
for g, x in G.items(): print(g, "aperturas", len(x), "vida mediana", st.median(x) if x else None, "sabido_max mediano", st.median(SM[g]) if SM.get(g) else None)
print("total", sum(len(x) for x in G.values()))
