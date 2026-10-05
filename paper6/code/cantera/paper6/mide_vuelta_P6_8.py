"""[P6-7] POR QUE NO VUELVE: `noop` contra `ir_pareja` en las excursiones largas.

En los tics con detalle de candidatos (cada 24) dentro de cada excursion larga,
para el asiento que se alejo: d(ir_pareja) - d(noop) (positivo = noop gana),
y que filas difieren entre las dos previsiones (media de la diferencia de M
por fila, ir_pareja - noop). Solo tics en que `ir_pareja` era candidato.
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
import serie_util as U

for brazo in sys.argv[1:]:
    L = json.load(open(os.path.join(AQUI, f"P6_8_largas_{brazo}.json")))
    porcarp = collections.defaultdict(list)
    for e in L:
        porcarp[e["carp"]].append(e)
    dd, filas, gana, n_sin = [], collections.defaultdict(list), collections.Counter(), 0
    for carp, exs in porcarp.items():
        for sl in {e["se_aleja"] for e in exs}:
            f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{sl}.art.log"))[0]
            vent = [(e["t0"], e["t1"]) for e in exs if e["se_aleja"] == sl]
            for r in U.lee(f):
                if r.get("k") != "tick" or r.get("phase") != "live":
                    continue
                t = r["tick"]
                if not any(a <= t <= b for a, b in vent):
                    continue
                c = (r.get("RADIOGRAFIA") or {}).get("candidatos") or {}
                if not isinstance(c.get("noop"), dict):
                    continue
                if "ir_pareja" not in c:
                    n_sin += 1; continue
                n, p = c["noop"], c["ir_pareja"]
                dd.append(p["d"] - n["d"])
                gana[(r.get("RADIOGRAFIA") or {}).get("elegido")] += 1
                fn, fp = n.get("filas") or {}, p.get("filas") or {}
                for k in set(fn) | set(fp):
                    filas[k].append(fp.get(k, 0.0) - fn.get(k, 0.0))
    print(f"### {brazo}: {len(dd)} tics con detalle e ir_pareja candidato · {n_sin} con detalle y SIN ir_pareja")
    if dd:
        print(f"  d(ir_pareja) - d(noop): mediana {st.median(dd):+.4f} · ir_pareja mejor (negativo) en {sum(x<0 for x in dd)} · noop mejor en {sum(x>0 for x in dd)} · empate {sum(x==0 for x in dd)}")
        print("  elegido en esos tics:", dict(gana.most_common(6)))
        print("  filas: media de M(ir_pareja) - M(noop), y en cuantos tics difiere:")
        for k, v in sorted(filas.items(), key=lambda kv: -abs(st.mean(kv[1]))):
            nz = sum(1 for x in v if abs(x) > 1e-9)
            if nz:
                print(f"    {k:20s} {st.mean(v):+.4f}  (difiere en {nz}/{len(dd)})")
