"""[P6-9] EL TIEMPO DE RESCATE Y EL HUECO DE VALOR. SOLO LECTURA.

1 · EPISODIOS DE PELIGRO. Un golpe = una entrada de `damage_taken`. Un episodio
    empieza en un golpe sin golpes en los N tics anteriores, y acaba en la
    muerte (ultimo tic vivo dentro de N tics del ultimo golpe) o en el primer
    tic con N tics sin golpes (la salida se fecha en el ULTIMO golpe). Causa =
    fuente del primer golpe: anillo (`zone`), rival con arma en mano, rival con
    la mano vacia, otro. Se calcula para VARIOS N y se elige mirando los huecos.
2 · ¿HABRIA LLEGADO? Al empezar el episodio, distancia REAL del otro hermano
    (su diario), pasos de CAMINO (`decisor_zs.campo_geodesico` hacia la casilla
    de la victima, evaluado en la casilla del otro) x coste de movimiento
    (`mundo.coste_movimiento(speed)`, leido del mundo), y si esa llegada es
    menor que la duracion. Y lo que hizo de verdad: familias de `elegido` del
    otro durante el episodio, distancia minima que alcanzo, si llego a <= 1.
3 · EL HUECO DE VALOR. Tics con detalle de candidatos, piernas listas, hermano
    vivo, `ir_pareja` candidato y ganador distinto: d(ir_pareja) - d(ganador),
    cuando el hermano esta LEJOS (llegada = pasos x coste > T) para varios T.
    Todo leido de la RADIOGRAFIA; nada recalculado de la tabla.
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
import serie_util as U
from alma import decisor_zs as D

NS = (48, 96, 144, 240)
TS = (100, 200, 300, 500)


def pct(xs, q):
    if not xs:
        return None
    s = sorted(xs); return s[min(len(s) - 1, int(round(q * (len(s) - 1))))]


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map")
    cat = next(r for r in recs if r["k"] == "catalogo")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    fin = next((r for r in recs if r.get("k") == "final"), None)
    sp = 5
    for r in recs:
        if r.get("k") == "arranque":
            m = re.search(r'"speed"\s*:\s*(\d+)', json.dumps(r)); sp = int(m.group(1)) if m else 5; break
    dano = {it["id"]: float(it.get("damage") or 0) for it in cat["items"]}
    T = {}
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        ve = {a.get("slot"): a for a in (r.get("ve_agentes") or [])}
        gol = []
        for g in (r.get("damage_taken") or []):
            s = str(g.get("source"))
            if s == "zone":
                gol.append("anillo")
            elif s.startswith("P"):
                a = ve.get(int(s[1:])); h = a.get("hand") if a else None
                gol.append("rival con arma" if a and h and h != "none" and dano.get(h, 0) > 0 else "rival sin arma (o no visto)")
            else:
                gol.append("otro")
        ra = r.get("RADIOGRAFIA") or {}; cs = ra.get("candidatos") or {}
        T[r["tick"]] = {"pos": tuple(int(x) for x in r["pos"]), "hp": r.get("hp"), "gol": gol,
                        "el": str(ra.get("elegido") or ""), "listas": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0) == 0,
                        "cs": cs if isinstance(cs.get("noop"), dict) else None,
                        "muerta": bool(r.get("pareja_muerta"))}
    del recs
    return mundo, sp, T, fin


def fam(e):
    for p in ("ir_pareja", "ir_objeto", "ir_botin", "ir_centro", "move_", "paso_", "atacar", "coger", "noop", "usar", "soltar"):
        if e.startswith(p):
            return p.rstrip("_")
    return "otro"


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def pasos(mundo, desde, hasta):
    campo = D.campo_geodesico(mundo, hasta)
    if campo and desde in campo:
        return int(campo[desde])
    return None


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    huecos = []; EP = {n: [] for n in NS}; HUECO = {t: [] for t in TS}; S = collections.Counter()
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f
              for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if 10 not in fs or 11 not in fs:
            continue
        L = {sl: carga(fs[sl]) for sl in (10, 11)}
        S["partidas"] += 1
        for sl in (10, 11):
            otro = 21 - sl
            mundo, sp, T, fin = L[sl]; To = L[otro][2]
            coste = mundo.coste_movimiento(sp)
            tics = sorted(T); golpes = [(t, g) for t in tics for g in T[t]["gol"]]
            muere = bool(fin and fin.get("reason") == "eliminated"); tl = tics[-1]
            # huecos entre golpes consecutivos
            for (a, _), (b, _) in zip(golpes, golpes[1:]):
                if b > a:
                    huecos.append(b - a)
            # episodios para cada N
            for N in NS:
                i = 0
                while i < len(golpes):
                    t0, causa = golpes[i]; j = i
                    while j + 1 < len(golpes) and golpes[j + 1][0] - golpes[j][0] <= N:
                        j += 1
                    tu = golpes[j][0]
                    fin_muerte = muere and tl - tu <= N
                    t1 = tl if fin_muerte else tu
                    e = {"carp": os.path.basename(carp), "slot": sl, "t0": t0, "t1": t1, "dur": t1 - t0,
                         "causa": causa, "golpes": j - i + 1, "acaba": "muere" if fin_muerte else "sale"}
                    # el otro hermano
                    if t0 in To:
                        po = To[t0]["pos"]; pv = T[t0]["pos"]
                        e["dist"] = cheb(po, pv); ps = pasos(mundo, po, pv)
                        e["pasos"] = ps; e["llegada"] = ps * coste if ps is not None else None
                        e["llegaria"] = (e["llegada"] < e["dur"]) if e["llegada"] is not None else None
                        w = [t for t in range(t0, t1 + 1) if t in To]
                        e["otro_vivo_al_final"] = t1 in To
                        e["otro_elige"] = dict(collections.Counter(fam(To[t]["el"]) for t in w))
                        dm = min((cheb(To[t]["pos"], T[t]["pos"]) for t in w if t in T), default=None)
                        e["dist_min"] = dm; e["llego"] = (dm is not None and dm <= 1)
                        e["dist_final"] = cheb(To[w[-1]]["pos"], T[w[-1]]["pos"]) if w and w[-1] in T else None
                    else:
                        e["dist"] = None; e["otro_vivo_al_final"] = False
                    EP[N].append(e); i = j + 1
            # hueco de valor
            for t in tics:
                r = T[t]
                if not r["cs"] or not r["listas"] or r["muerta"] or t not in To or "ir_pareja" not in r["cs"]:
                    continue
                el = r["el"]
                if el == "ir_pareja" or el not in r["cs"]:
                    continue
                dp, dg = r["cs"]["ir_pareja"]["d"], r["cs"][el]["d"]
                ps = pasos(mundo, r["pos"], To[t]["pos"])
                if ps is None:
                    continue
                lleg = ps * coste
                for Tt in TS:
                    if lleg > Tt:
                        HUECO[Tt].append((dp - dg, fam(el), cheb(r["pos"], To[t]["pos"])))
        del L
        print(f"    {os.path.basename(carp)}", flush=True)
    res = {"huecos": {"n": len(huecos), "p50": pct(huecos, .5), "p75": pct(huecos, .75), "p90": pct(huecos, .9), "p95": pct(huecos, .95),
                      "hist": {k: sum(1 for h in huecos if lo <= h < hi) for k, (lo, hi) in
                               {"<=24": (0, 25), "25-48": (25, 49), "49-96": (49, 97), "97-144": (97, 145), "145-240": (145, 241), "241-480": (241, 481), ">480": (481, 10**9)}.items()}},
           "episodios": {}, "hueco_valor": {}}
    print(f"### {etiq} · huecos entre golpes: n={len(huecos)} p50={pct(huecos,.5)} p75={pct(huecos,.75)} p90={pct(huecos,.9)} p95={pct(huecos,.95)} · hist {res['huecos']['hist']}")
    for N in NS:
        E = EP[N]; r = {"n": len(E), "por_causa": {}}
        for c in sorted({e["causa"] for e in E}):
            X = [e for e in E if e["causa"] == c]; du = [e["dur"] for e in X]
            X2 = [e for e in X if e.get("dist") is not None]
            r["por_causa"][c] = {"n": len(X), "mueren": sum(e["acaba"] == "muere" for e in X),
                                 "dur_p50": pct(du, .5), "dur_p25": pct(du, .25), "dur_p75": pct(du, .75), "dur_p90": pct(du, .9),
                                 "golpes_p50": pct([e["golpes"] for e in X], .5),
                                 "con_otro_vivo": len(X2), "dist_p50": pct([e["dist"] for e in X2], .5),
                                 "llegada_p50": pct([e["llegada"] for e in X2 if e["llegada"] is not None], .5),
                                 "llegaria": sum(1 for e in X2 if e.get("llegaria")), "llego": sum(1 for e in X2 if e.get("llego")),
                                 "otro_elige": dict(sum((collections.Counter(e["otro_elige"]) for e in X2), collections.Counter()))}
        res["episodios"][N] = {"resumen": r, "lista": E}
        print(f"  N={N}: {len(E)} episodios")
        for c, v in r["por_causa"].items():
            print(f"     {c:28s} n={v['n']:4d} mueren {v['mueren']:3d} · dur p25/50/75/90 {v['dur_p25']}/{v['dur_p50']}/{v['dur_p75']}/{v['dur_p90']} · golpes p50 {v['golpes_p50']} · otro vivo {v['con_otro_vivo']} · dist p50 {v['dist_p50']} · llegada p50 {v['llegada_p50']} · llegaria {v['llegaria']} · llego {v['llego']}")
    for Tt in TS:
        H = HUECO[Tt]; d = [x[0] for x in H]
        res["hueco_valor"][Tt] = {"n": len(H), "p25": pct(d, .25), "p50": pct(d, .5), "p75": pct(d, .75), "p90": pct(d, .9),
                                  "gana": dict(collections.Counter(x[1] for x in H)), "dist_p50": pct([x[2] for x in H], .5)}
        print(f"  hueco de valor, lejos = llegada > {Tt}: n={len(H)} · d(ir_pareja)-d(gana) p25/50/75/90 {pct(d,.25)}/{pct(d,.5)}/{pct(d,.75)}/{pct(d,.9)} · gana {dict(collections.Counter(x[1] for x in H).most_common(5))}")
    OUT[etiq] = res
json.dump(OUT, open(os.path.join(AQUI, "P6_9.json"), "w"), ensure_ascii=False, indent=1, default=str)
print("\n-> cantera/paper6/P6_9.json")
