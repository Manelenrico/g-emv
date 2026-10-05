"""[P6-7] LAS EXCURSIONES LARGAS DE A1 (>= 200 tics) y de que estan hechas.

Para cada excursion larga de `P6_8_separa.json`: quien se aleja, cuanto dura, y
en los tics del que se aleja: cuantos son `coger` con `inventory_full`, cuantos
`move_*` (apartarse) — y de esos, cuantos SIN rival armado a la vista pero CON
rival contado (huida de un contado) —, cuantos `ir_pareja`, y como acaba (se
reunen, o muere uno). Todo leido, nada estimado.
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

MIN = int(os.environ.get("MIN", "200"))


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map")
    cat = next(r for r in recs if r["k"] == "catalogo")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); herm = pc.get("teammate_slot")
    fin = next((r for r in recs if r.get("k") == "final"), None)
    T = {}; ult = None
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        for m in (r.get("chat") or []):
            if m.get("channel") == "team" and m.get("from") == herm and (m.get("text") or "").startswith("E2 "):
                p = P2.parsea(m["text"], mundo)
                if p:
                    ult = p
        t = r["tick"]; ve = r.get("ve_agentes") or []
        vistos = {a.get("slot") for a in ve}
        riv = [x for x in ult["rivales"] if x["slot"] not in vistos] if ult and 0 <= t - ult["t"] <= OY.CADUCIDAD_RIVAL else []
        armado_visto = any(a.get("slot") not in (pc["slot"], herm) and mundo.items.get(a.get("hand") or "") is not None
                           and float(getattr(mundo.items.get(a.get("hand")), "damage", 0) or 0) > 0 for a in ve)
        ra = r.get("RADIOGRAFIA") or {}
        T[t] = {"pos": tuple(int(x) for x in r["pos"]), "el": str(ra.get("elegido") or ""),
                "lleno": ra.get("elegido") == "coger" and r.get("action_result_obs") == "inventory_full",
                "riv_cont": len(riv), "armado_visto": armado_visto, "listas": int(r.get("move_ready_in") or 0) == 0}
    del recs
    return T, fin


S = json.load(open(os.path.join(AQUI, "P6_8_separa.json")))
for brazo in sys.argv[1:]:
    EX = [e for e in S[brazo]["excursiones"] if e[2] - e[1] >= MIN]
    print(f"### {brazo}: {len(EX)} excursiones >= {MIN} tics")
    tot = collections.Counter(); filas = []
    cache = {}
    for carp, t0, t1 in sorted(EX, key=lambda e: -(e[2] - e[1])):
        if carp not in cache:
            fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f
                  for f in glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, "*policy_agent_1*.art.log"))}
            cache[carp] = {sl: carga(fs[sl]) for sl in (10, 11)}
        A, B = cache[carp][10][0], cache[carp][11][0]
        v = [t for t in range(t0, min(t0 + 60, t1)) if t in A and t in B]
        mA = max(abs(A[v[-1]]["pos"][0] - A[v[0]]["pos"][0]), abs(A[v[-1]]["pos"][1] - A[v[0]]["pos"][1]))
        mB = max(abs(B[v[-1]]["pos"][0] - B[v[0]]["pos"][0]), abs(B[v[-1]]["pos"][1] - B[v[0]]["pos"][1]))
        quien, T = (10, A) if mA >= mB else (11, B)
        w = [t for t in range(t0, t1 + 1) if t in T]
        c = collections.Counter()
        for t in w:
            r = T[t]
            if r["lleno"]:
                c["coger lleno"] += 1
            elif r["el"].startswith("move_"):
                c["move (apartarse)"] += 1
                if not r["armado_visto"] and r["riv_cont"]:
                    c["move sin armado visto y CON contado"] += 1
            elif r["el"].startswith("ir_pareja"):
                c["ir_pareja"] += 1
            elif r["el"].startswith("ir_objeto"):
                c["ir_objeto"] += 1
            elif r["el"] == "noop":
                c["noop"] += 1
            else:
                c["otro"] += 1
            if r["listas"]:
                c["piernas listas"] += 1
        fin10, fin11 = cache[carp][10][1], cache[carp][11][1]
        muere = [sl for sl, f in ((10, fin10), (11, fin11)) if f and f.get("reason") == "eliminated" and abs(int(f.get("match_ticks") or 0) - t1) <= 2]
        fila = {"carp": carp, "t0": t0, "t1": t1, "dur": t1 - t0, "se_aleja": quien, "acaba": f"muere {muere}" if muere else "se reunen", **dict(c)}
        filas.append(fila); tot.update(c); tot["dur"] += t1 - t0
        print(f"  {carp} {t0:5d}-{t1:5d} ({t1-t0:4d}) se aleja s{quien} · {fila['acaba']:14s} · lleno {c['coger lleno']:4d} · move {c['move (apartarse)']:3d} (sin visto+contado {c['move sin armado visto y CON contado']:3d}) · ir_pareja {c['ir_pareja']:3d} · ir_objeto {c['ir_objeto']:3d} · noop {c['noop']:4d}")
    print("  SUMA:", dict(tot))
    json.dump(filas, open(os.path.join(AQUI, f"P6_8_largas_{brazo}.json"), "w"), ensure_ascii=False, indent=1)
