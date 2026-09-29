"""[P5-5A] A1-A4 sobre el juicio ya hecho. En seco, coste cero."""
from __future__ import annotations
import json, os, sys, math, collections, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import clases_consejo as CC                                 # noqa: E402

SUBE, BAJA = 0.10, 0.20        # la moneda de P5-4B


def wilson(k, n, z=1.96):
    if not n:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d * 100, (c + m) / d * 100)


def newc(k1, n1, k2, n2):
    p1 = k1 / n1 * 100 if n1 else 0.0
    p2 = k2 / n2 * 100 if n2 else 0.0
    l1, u1 = wilson(k1, n1); l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return (d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2),
            d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))


def main():
    F = json.load(open(f"{AQUI}/P55A_juicio.json"))
    # texto entero por respuesta, para arreglar «lo nuevo» del hermano
    txt = {}
    for line in open(f"{AQUI}/P55A_respuestas.jsonl", encoding="utf-8"):
        d = json.loads(line)
        if d["ok"]:
            txt[(d["arm"], d["ereq"], d["asiento"], d["tick_foto"])] = \
                " ".join(p["accion"] + " " + p["motivo"] for p in d["props"])
    for f in F:
        t = txt.get((f["arm"], f["ereq"], f["asiento"], f["t0"]), "")
        cambio = bool(CC.clasifica(t, None).get("HERM_CAMBIO"))
        for a in f["afs"]:
            if a["clase"] == "HERMANO":
                a["nuevo"] = cambio

    # ── A1 ────────────────────────────────────────────────────────────────
    print("=" * 74)
    print("A1 · CLASIFICACION, por respuesta")
    n = len(F)
    porarm = collections.defaultdict(collections.Counter)
    tot = collections.Counter()
    for f in F:
        cs = set(f["clases"])
        for c in cs or {"NADA"}:
            tot[c] += 1; porarm[f["arm"]][c] += 1
        if cs & {"LLEGADA", "AUSENCIA", "POSICION", "HERMANO"}:
            tot["ALGO"] += 1; porarm[f["arm"]]["ALGO"] += 1
        if cs & {"LLEGADA", "AUSENCIA", "POSICION"}:
            tot["RIVALES"] += 1; porarm[f["arm"]]["RIVALES"] += 1
        if cs & {"LLEGADA", "AUSENCIA"}:
            tot["LLE_AUS"] += 1; porarm[f["arm"]]["LLE_AUS"] += 1
    nb = sum(1 for f in F if f["arm"] == "S2_B")
    nc = n - nb
    print(f"  respuestas: {n}  (S2_B {nb} · S2_C {nc})")
    for c in ("LLEGADA", "AUSENCIA", "POSICION", "HERMANO", "NADA",
              "ALGO", "RIVALES", "LLE_AUS"):
        b, cc = porarm["S2_B"][c], porarm["S2_C"][c]
        print(f"  {c:9s} {tot[c]:5d} {tot[c]/n*100:6.2f}%   "
              f"B {b:5d} {b/nb*100:6.2f}%   C {cc:5d} {cc/nc*100:6.2f}%")

    # ── A2 ────────────────────────────────────────────────────────────────
    print("=" * 74)
    print("A2 · COMPROBACION, por afirmacion")
    c = collections.defaultdict(collections.Counter)
    for f in F:
        for a in f["afs"]:
            k = a["clase"]; c[k]["n"] += 1; c[k][a["ver"]] += 1
            c[k]["b_" + a["base"]] += 1
    for k in ("LLEGADA", "AUSENCIA", "POSICION", "HERMANO"):
        d = c[k]; comp = d["ok"] + d["mal"]; bc = d["b_ok"] + d["b_mal"]
        lo, hi = wilson(d["ok"], comp); blo, bhi = wilson(d["b_ok"], bc)
        dif, dlo, dhi = newc(d["ok"], comp, d["b_ok"], bc)
        print(f"  {k:9s} n={d['n']:5d} comprobables={comp:5d} "
              f"({comp/d['n']*100:5.1f}%)  acierto={d['ok']/comp*100:6.2f}% "
              f"[{lo:.1f}-{hi:.1f}]  |  BASE {d['b_ok']/bc*100:6.2f}% "
              f"[{blo:.1f}-{bhi:.1f}]  |  dif {dif:+6.2f} [{dlo:+.2f},{dhi:+.2f}]")

    # ── A3 ────────────────────────────────────────────────────────────────
    print("=" * 74)
    print("A3 · LO NUEVO, y la confianza que habria ganado")
    nn = collections.Counter()
    for f in F:
        for a in f["afs"]:
            nn["afs"] += 1
            if a["nuevo"]:
                nn["nuevas"] += 1; nn["n_" + a["ver"]] += 1
            else:
                nn["triv"] += 1; nn["t_" + a["ver"]] += 1
    cn = nn["n_ok"] + nn["n_mal"]; ct = nn["t_ok"] + nn["t_mal"]
    print(f"  afirmaciones {nn['afs']} · NO TRIVIALES {nn['nuevas']} "
          f"({nn['nuevas']/nn['afs']*100:.2f}%) · triviales {nn['triv']}")
    print(f"  no triviales comprobadas {cn} ({cn/max(1,nn['nuevas'])*100:.1f}%) "
          f"acierto {nn['n_ok']/cn*100:.2f}%" if cn else "  sin no triviales")
    print(f"  triviales    comprobadas {ct} acierto {nn['t_ok']/ct*100:.2f}%")
    # confianza por vida
    vidas = collections.defaultdict(list)
    for f in F:
        for a in f["afs"]:
            if a["nuevo"] and a["ver"] in ("ok", "mal"):
                vidas[(f["arm"], f["ereq"], f["asiento"])].append((f["t0"], a["ver"]))
    Cf = {}; tray = collections.defaultdict(list)
    for v, xs in vidas.items():
        C = 0.0
        for t, ver in sorted(xs):
            C = min(1.0, max(0.0, C + (SUBE if ver == "ok" else -BAJA)))
            tr = "0-500" if t < 500 else ("500-1500" if t < 1500 else ">1500")
            tray[tr].append(C)
        Cf[v] = C
    todas = collections.defaultdict(list)
    for line in open(f"{AQUI}/P55A_respuestas.jsonl", encoding="utf-8"):
        d = json.loads(line)
        if d["ok"]:
            todas[(d["arm"], d["ereq"], d["asiento"])].append(1)
    for v in todas:
        Cf.setdefault(v, 0.0)
    vs = sorted(Cf.values())
    print(f"  vidas {len(vs)} (con alguna afirmacion nueva: {len(vidas)})")
    print(f"  C final mediana {st.median(vs):.3f} · media {sum(vs)/len(vs):.3f} "
          f"· >0,5 {sum(1 for x in vs if x > 0.5)}/{len(vs)} "
          f"· >0,8 {sum(1 for x in vs if x > 0.8)}/{len(vs)} "
          f"· <0,2 {sum(1 for x in vs if x < 0.2)}/{len(vs)}")
    print("  trayectoria " + " · ".join(
        f"{k} {st.median(v):.3f}" for k, v in sorted(tray.items())))

    # ── A4 ────────────────────────────────────────────────────────────────
    print("=" * 74)
    print("A4 · ACEPTACION REAL DEL CUATRO")
    for etiq, clases in (("otros (rivales+hermano)",
                          {"LLEGADA", "AUSENCIA", "POSICION", "HERMANO"}),
                         ("solo rivales", {"LLEGADA", "AUSENCIA", "POSICION"})):
        g = {True: collections.Counter(), False: collections.Counter()}
        for f in F:
            cierta = any(a["ver"] == "ok" and a["clase"] in clases
                         for a in f["afs"])
            for p in f["props"]:
                if p["regla"] == "esperar":
                    continue
                gr = g[cierta]; gr["n"] += 1
                if p["cajas"].get("en la mesa"):
                    gr["mesa"] += 1
                if p["gano"]:
                    gr["gano"] += 1
        a, b = g[True], g[False]
        d1, l1, h1 = newc(a["mesa"], a["n"], b["mesa"], b["n"])
        d2, l2, h2 = newc(a["gano"], a["n"], b["gano"], b["n"])
        print(f"  [{etiq}]")
        print(f"    con afirmacion cierta : n={a['n']:5d} "
              f"mesa {a['mesa']/a['n']*100:5.2f}%  gano {a['gano']/a['n']*100:5.3f}%")
        print(f"    sin afirmacion cierta : n={b['n']:5d} "
              f"mesa {b['mesa']/b['n']*100:5.2f}%  gano {b['gano']/b['n']*100:5.3f}%")
        print(f"    diferencia mesa {d1:+6.2f} [{l1:+.2f},{h1:+.2f}] · "
              f"gano {d2:+6.3f} [{l2:+.3f},{h2:+.3f}]")
    json.dump({"C_final": {"|".join(k): v for k, v in Cf.items()}},
              open(f"{AQUI}/P55A_confianza.json", "w"), ensure_ascii=False)


if __name__ == "__main__":
    main()
