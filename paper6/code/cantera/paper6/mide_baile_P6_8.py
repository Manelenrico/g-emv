"""[P6-8] EL BAILE: el cuerpo alternando entre DOS casillas. SOLO LECTURA.

Visto en A2 (22146038 s10): miles de tics yendo y viniendo entre (24,21) y
(25,22), con `ir_pareja` ganando solo en enfriamiento y `move_NW` / `ir_objeto`
turnandose cuando las piernas estan listas. Se cuenta, por brazo: rachas de
>= 6 movimientos efectivos consecutivos (la posicion cambia) que solo pisan
DOS casillas; tics en esas rachas; vidas afectadas; la racha mas larga.
"""
import collections, glob, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
import serie_util as U

OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.Counter(); peor = None
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
            if sl not in (10, 11):
                continue
            S["vidas"] += 1
            movs = []          # (tick, pos) en cada cambio de posicion
            ult = None; n = 0
            for r in U.lee(f):
                if r.get("k") != "tick" or r.get("phase") != "live":
                    continue
                n += 1; p = tuple(r["pos"])
                if p != ult:
                    movs.append((r["tick"], p)); ult = p
            S["tics"] += n
            # rachas de movimientos que solo pisan dos casillas
            i = 0; afectada = False
            while i < len(movs):
                j = i
                cells = {movs[i][1]}
                while j + 1 < len(movs) and len(cells | {movs[j + 1][1]}) <= 2:
                    j += 1; cells.add(movs[j][1])
                if j - i + 1 >= 6 and len(cells) == 2:
                    d = movs[j][0] - movs[i][0]
                    S["rachas de baile (>= 6 movs, 2 casillas)"] += 1
                    S["tics bailando"] += d; afectada = True
                    if peor is None or d > peor[0]:
                        peor = (d, j - i + 1, os.path.basename(carp), sl, sorted(cells), movs[i][0], movs[j][0], n)
                i = j + 1
            if afectada:
                S["vidas afectadas"] += 1
    OUT[etiq] = {"recuento": dict(S), "peor": peor}
    print(f"### {etiq}: " + " · ".join(f"{k} {v}" for k, v in S.items()) + f" · % {100*S['tics bailando']/(S['tics'] or 1):.2f}")
    if peor:
        print(f"   peor: {peor[0]} tics ({peor[1]} movimientos) {peor[2]} s{peor[3]} entre {peor[4]} tics {peor[5]}-{peor[6]} = {100*peor[0]/peor[7]:.1f} % de esa vida")
json.dump(OUT, open(os.path.join(AQUI, "P6_8_baile.json"), "w"), ensure_ascii=False, indent=1)
