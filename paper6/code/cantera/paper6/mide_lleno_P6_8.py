"""[P6-7] EL BUCLE DE LA MOCHILA LLENA. SOLO LECTURA.

Encontrado al mirar la partida 20260916 de A1: el asiento 11 elige `coger`
3.226 tics seguidos en [1,45] con `action_result: inventory_full`. El cuerpo del
cinco no lee ese resultado (`Bloqueos` solo trata `cooldown`), asi que insiste
mientras el objeto siga en el suelo, aunque tenga 14 candidatos de movimiento.

Se cuenta por brazo: tics con elegido `coger` y `action_result_obs ==
"inventory_full"`, rachas (tics consecutivos), vidas afectadas, la racha mas
larga, cuantos de esos tics caen con el anillo haciendo dano, y si en esos tics
el cuerpo tenia piernas listas (o sea, podia haberse ido).
"""
import collections, glob, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
import serie_util as U

OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.Counter(); peor = None; vidas = []
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
            if sl not in (10, 11):
                continue
            n = 0; ll = 0; anillo = 0; listas = 0; cur = None; rachas = []; mt = None; muere = False
            for r in U.lee(f):
                if r.get("k") == "final":
                    muere = r.get("reason") == "eliminated"; mt = r.get("match_ticks")
                if r.get("k") != "tick" or r.get("phase") != "live":
                    continue
                n += 1
                el = (r.get("RADIOGRAFIA") or {}).get("elegido")
                if el == "coger" and r.get("action_result_obs") == "inventory_full":
                    ll += 1
                    if any(g.get("source") == "zone" for g in (r.get("damage_taken") or [])):
                        anillo += 1
                    if int(r.get("move_ready_in") or 0) == 0:
                        listas += 1
                    t = r["tick"]
                    if cur and t == cur[1] + 1:
                        cur[1] = t
                    else:
                        cur = [t, t, list(r["pos"])]; rachas.append(cur)
            S["vidas"] += 1; S["tics"] += n; S["tics coger con mochila LLENA"] += ll
            S["...con el anillo haciendo dano"] += anillo
            S["...con piernas listas (podia irse)"] += listas
            S["rachas (>= 24 tics)"] += sum(1 for a in rachas if a[1] - a[0] + 1 >= 24)
            if ll:
                S["vidas afectadas"] += 1
                if ll >= 240:
                    S["vidas con >= 240 tics (10 s) asi"] += 1
            for a in rachas:
                d = a[1] - a[0] + 1
                if peor is None or d > peor[0]:
                    peor = (d, os.path.basename(carp), sl, a[2], a[0], a[1], n, muere, mt)
            vidas.append({"carp": os.path.basename(carp), "slot": sl, "tics": n,
                          "lleno": ll, "anillo": anillo, "muere": muere, "mt": mt,
                          "rachas": [(a[0], a[1], a[2]) for a in rachas if a[1] - a[0] + 1 >= 24]})
    OUT[etiq] = {"recuento": dict(S), "peor": peor, "vidas": vidas}
    print(f"### {etiq}")
    for k, v in S.items():
        print(f"  {k:40s} {v}")
    print(f"  % de tics vividos: {100 * S['tics coger con mochila LLENA'] / (S['tics'] or 1):.2f} %")
    if peor:
        print(f"  peor racha: {peor[0]} tics en {peor[1]} s{peor[2]} en {peor[3]}, tics {peor[4]}-{peor[5]} "
              f"({100 * peor[0] / peor[6]:.1f} % de esa vida) · muere {peor[7]} en {peor[8]}")
json.dump(OUT, open(os.path.join(AQUI, "P6_8_lleno.json"), "w"), ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_8_lleno.json")
