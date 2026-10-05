"""[P6-10] DOS LINEAS BASE PARA EL SELLO. SOLO LECTURA.
  · muertes con el otro hermano vivo: cuantas con el otro a <= D0 (7) casillas de
    CAMINO (`campo_geodesico`) en el ultimo tic vivo, por brazo.
  · recogidas de comida (racion o venda): tics en que el `pack` sube en rations
    o first_aid, por brazo (por vida).
"""
import collections, glob, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
from alma import decisor_zs as D
D0 = 7; COMIDA = ("rations", "first_aid")
OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.Counter()
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if 10 not in fs or 11 not in fs:
            continue
        L = {}
        for sl in (10, 11):
            recs = list(U.lee(fs[sl]))
            pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
            mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); fin = next((r for r in recs if r.get("k") == "final"), None)
            T = {r["tick"]: (tuple(int(x) for x in r["pos"]), {(s or {}).get("id"): int((s or {}).get("n") or 1) for s in (r.get("pack") or []) if s}) for r in recs if r.get("k") == "tick" and r.get("phase") == "live"}
            L[sl] = (mundo, T, fin); del recs
        for sl in (10, 11):
            mundo, T, fin = L[sl]; To = L[21 - sl][1]
            S["vidas"] += 1
            ant = None
            for t in sorted(T):
                pk = T[t][1]
                if ant is not None:
                    for c in COMIDA:
                        if pk.get(c, 0) > ant.get(c, 0):
                            S["recogidas de comida"] += 1; S[f"  {c}"] += 1
                ant = pk
            if fin and fin.get("reason") == "eliminated":
                tl = max(T); S["muertes"] += 1
                if tl in To:
                    S["muertes con el otro vivo"] += 1
                    campo = D.campo_geodesico(mundo, T[tl][0]) or {}
                    dc = campo.get(To[tl][0])
                    if dc is not None and dc <= D0:
                        S["  ...con el otro a <= D0 de camino"] += 1
    OUT[etiq] = dict(S)
    print(f"### {etiq}: " + " · ".join(f"{k} {v}" for k, v in S.items()) + f" · comida por vida {S['recogidas de comida']/(S['vidas'] or 1):.2f}")
json.dump(OUT, open(os.path.join(AQUI, "P6_10_base2.json"), "w"), ensure_ascii=False, indent=1)
