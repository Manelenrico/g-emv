"""[P6-7] LA DISTANCIA ENTRE LOS DOS, y el bucle de la mochila con la fila encendida.

  · distancia Chebyshev entre los dos asientos, tic a tic, mientras los dos
    viven (posiciones REALES de los dos diarios); mediana, % de tics a <= 3 y
    a <= 8 casillas (8 = alcance del arco, leido del catalogo en el otro script).
  · tics con `elegido == coger` y `action_result_obs == inventory_full`,
    partidos por si F-HERMANO-AMENAZA estaba encendida en ese tic.
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
import serie_util as U


def pista(f):
    T = {}
    for r in U.lee(f):
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        ra = r.get("RADIOGRAFIA") or {}
        T[r["tick"]] = (tuple(int(x) for x in r["pos"]),
                        "F-HERMANO-AMENAZA" in (((ra.get("ahora") or {}).get("filas")) or {}),
                        ra.get("elegido") == "coger" and r.get("action_result_obs") == "inventory_full")
    return T


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.Counter(); porsem = {}
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f
              for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if 10 not in fs or 11 not in fs:
            continue
        A, B = pista(fs[10]), pista(fs[11])
        com = sorted(set(A) & set(B))
        d = [max(abs(A[t][0][0] - B[t][0][0]), abs(A[t][0][1] - B[t][0][1])) for t in com]
        sem = re.search(r"_(\d{8})$", carp).group(1)
        porsem[sem] = {"tics_juntos_vivos": len(com), "dist_mediana": st.median(d) if d else None,
                       "pct_le3": 100 * sum(x <= 3 for x in d) / (len(d) or 1),
                       "pct_le8": 100 * sum(x <= 8 for x in d) / (len(d) or 1)}
        S["tics con los dos vivos"] += len(com)
        S["...a <= 3 casillas"] += sum(x <= 3 for x in d)
        S["...a <= 8 casillas"] += sum(x <= 8 for x in d)
        S["...a > 15 casillas"] += sum(x > 15 for x in d)
        for T in (A, B):
            for t, (p, am, ll) in T.items():
                if ll:
                    S["coger con mochila llena"] += 1
                    S["...con F-HERMANO-AMENAZA encendida" if am else "...con la fila apagada"] += 1
    OUT[etiq] = {"recuento": dict(S), "por_semilla": porsem}
    n = S["tics con los dos vivos"] or 1
    print(f"### {etiq}")
    for k, v in S.items():
        print(f"  {k:40s} {v:8d}" + (f"  {100*v/n:6.2f} %" if k.startswith("...a ") else ""))
    print(f"  mediana de las medianas por semilla: {st.median(v['dist_mediana'] for v in porsem.values())}")
json.dump(OUT, open(os.path.join(AQUI, "P6_10_pareja.json"), "w"), ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_10_pareja.json")
