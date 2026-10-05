"""[P6-7] EL BUCLE DE LA MOCHILA LLENA: que objeto, con que mochila, y si lo
que tenia bajo los pies se lo habian CONTADO (E2 del hermano, recursos vigentes
segun `oyente2.peso_recurso` >= UMBRAL_REC) en los 300 tics antes de llegar.
SOLO LECTURA. Rachas >= 24 tics de `coger` + `inventory_full`.
"""
import collections, glob, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
import serie_util as U
import parte2 as P2
import oyente2 as OY

for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.Counter(); R = []
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
            if sl not in (10, 11):
                continue
            recs = list(U.lee(f))
            pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map")
            cat = next(r for r in recs if r["k"] == "catalogo")
            mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); herm = pc["teammate_slot"]
            T = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
            del recs
            # recursos contados vigentes por tic
            cont = {}; ult = None
            for r in T:
                for m in (r.get("chat") or []):
                    if m.get("channel") == "team" and m.get("from") == herm and (m.get("text") or "").startswith("E2 "):
                        p = P2.parsea(m["text"], mundo)
                        if p:
                            ult = p
                t = r["tick"]
                cont[t] = {(x["id"], tuple(x["pos"])) for x in ult["recursos"]} \
                    if ult and t - ult["t"] >= 0 and OY.peso_recurso(t - ult["t"]) >= OY.UMBRAL_REC else set()
            cur = None
            for i, r in enumerate(T):
                ll = (r.get("RADIOGRAFIA") or {}).get("elegido") == "coger" and r.get("action_result_obs") == "inventory_full"
                if ll and cur and r["tick"] == cur["fin"] + 1:
                    cur["fin"] = r["tick"]; continue
                if ll:
                    pos = tuple(int(x) for x in r["pos"])
                    it = next((x["id"] for x in (r.get("ve_items") or []) if tuple(x["pos"]) == pos), None)
                    pack = [s["id"] for s in (r.get("pack") or []) if s]
                    contado = any(k[1] == pos for tt in range(r["tick"] - 300, r["tick"] + 1) for k in cont.get(tt, ()))
                    cur = {"carp": os.path.basename(carp), "slot": sl, "ini": r["tick"], "fin": r["tick"], "pos": pos,
                           "item": it, "pack": pack, "body": r.get("body"), "contado_antes": contado}
                    R.append(cur)
                else:
                    cur = None
    R = [x for x in R if x["fin"] - x["ini"] + 1 >= 24]
    print(f"### {etiq}: {len(R)} rachas >= 24 tics · tics {sum(x['fin']-x['ini']+1 for x in R)}")
    print("  objeto bajo los pies:", dict(collections.Counter(x["item"] for x in R)))
    print("  mochila (n objetos) al empezar:", dict(collections.Counter(len(x["pack"]) for x in R)), "· con backpack puesto:", sum(1 for x in R if x["body"]))
    print("  ese objeto/casilla se lo habian CONTADO en los 300 tics antes:", sum(1 for x in R if x["contado_antes"]), "de", len(R))
    for x in sorted(R, key=lambda x: -(x["fin"] - x["ini"]))[:5]:
        print(f"    {x['carp']} s{x['slot']} {x['ini']}-{x['fin']} ({x['fin']-x['ini']+1}) {x['item']} en {x['pos']} mochila {x['pack']} contado_antes {x['contado_antes']}")
    json.dump(R, open(os.path.join(AQUI, f"P6_7_lleno2_{etiq}.json"), "w"), ensure_ascii=False, indent=1)
