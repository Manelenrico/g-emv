"""[P8] Prompt 117: la medida de dormir del experimento v4 (la de P9). Es la copia arreglada del diagnóstico v4 (diagnostico_v4/dormir_v4.py, prompt 114), con la
carpeta como parámetro y la marca de agotada. Solo lee.
LA PRIMERA VEZ QUE SE DUERME CADA NOCHE: por criatura viva y por día, el primer turno de la noche (anochecer o noche, de la config del mundo) en que está
dormida; si ya dormía al empezar el anochecer, cuenta el primer turno del anochecer. Dónde está entonces: dentro de su casa (sin la puerta) · en una puerta ·
en otra casa · fuera; y si estaba agotada (cuerpo.agotada del registro del mundo) ese turno o el anterior.
   una(carpeta_de_la_partida, semilla) -> {"noches", "dentro", "puerta", "puerta_agotada", "puerta_sin_agotar", "otra casa", "fuera", "puertas_sin_agotar": [...]}"""
import gzip, json, os, sys
from collections import Counter
P8 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RAIZ = os.path.dirname(os.path.dirname(P8)); sys.path.insert(0, P8)
MC = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8")); DIA = MC["dia"]["turnos"]; FASES = []
for nom, n in MC["dia"]["fases"]: FASES += [nom] * int(n)
fase = lambda t: FASES[t % DIA]
NOCHE = ("anochecer", "noche")

def una(d, s):
    import lanzador as L
    e = L.MU.Valle(); _, inf = e.reset(seed=s); mp = inf[e.agents[0]]["mapa"]
    casa = {k: {tuple(c) for c in w["celdas"]} for k, w in mp["casas"].items()}; puertas = {tuple(w["puerta"]) for w in mp["casas"].values()}
    donde = lambda a, p: "puerta" if p in puertas else ("dentro" if p in casa[a[0]] else ("otra casa" if any(p in c for c in casa.values()) else "fuera"))
    C = Counter(); visto = set(); ago_prev = {}; malas = []
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l); t = x["turno"]; fa = fase(t)
        for a, g in x["agentes"].items():
            cu = g["cuerpo"]; ago = bool(cu.get("agotada")) or ago_prev.get(a, False)
            if cu.get("dormida") and not cu["muerta"] and fa in NOCHE and (a, t // DIA) not in visto:
                visto.add((a, t // DIA)); k = donde(a, tuple(g["pos"])); C["noches"] += 1; C[k] += 1
                if k == "puerta":
                    C["puerta_agotada" if ago else "puerta_sin_agotar"] += 1
                    if not ago: malas.append({"t": t, "a": a})
            ago_prev[a] = bool(cu.get("agotada"))
    return dict(C, puertas_sin_agotar=malas)
