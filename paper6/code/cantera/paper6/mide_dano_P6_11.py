"""[P6-11 · 1] CUANTO HACE DE VERDAD UN GOLPE, segun lo que lleva en la mano el que
pega. SOLO LECTURA. Por golpe recibido (`damage_taken` con fuente `P<slot>`): la
mano del atacante en ese tic si esta a la vista (`ve_agentes[].hand`), y la
cantidad. Se compara con el dano del catalogo.
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5")):
    sys.path.insert(0, p)
import serie_util as U
G = collections.defaultdict(list); cat = {}
for pat in sys.argv[1:]:
    for f in sorted(glob.glob(os.path.join(RAIZ, pat, "*policy_agent_1*.art.log"))):
        for r in U.lee(f):
            if r.get("k") == "catalogo":
                for it in r["items"]:
                    cat[it["id"]] = (it.get("kind"), it.get("damage"), it.get("range"))
            if r.get("k") != "tick" or r.get("phase") != "live":
                continue
            ve = {a.get("slot"): a for a in (r.get("ve_agentes") or [])}
            for g in (r.get("damage_taken") or []):
                s = str(g.get("source"))
                if not s.startswith("P"):
                    continue
                a = ve.get(int(s[1:]))
                h = ("NO VISTO" if a is None else (a.get("hand") or "none"))
                G[h].append(float(g.get("amount") or 0))
print(f"{'mano del que pega':16s} {'golpes':>7s} {'dano mediana':>13s} {'min':>6s} {'max':>6s} {'catalogo (kind, dano, alcance)'}")
for h, xs in sorted(G.items(), key=lambda kv: -len(kv[1])):
    print(f"{h:16s} {len(xs):7d} {st.median(xs):13.2f} {min(xs):6.2f} {max(xs):6.2f} {cat.get(h)}")
json.dump({h: {"n": len(xs), "mediana": st.median(xs), "min": min(xs), "max": max(xs), "valores": dict(collections.Counter(xs))} for h, xs in G.items()},
          open(os.path.join(AQUI, "P6_11_dano.json"), "w"), ensure_ascii=False, indent=1)
print("catalogo de armas:", {k: v for k, v in cat.items() if (v[1] or 0) > 0})
