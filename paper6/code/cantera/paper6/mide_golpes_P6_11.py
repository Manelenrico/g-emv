"""[P6-7 · 3] DE QUE MUEREN, con lupa: cada golpe recibido de un rival, y si en
ese tic el cuerpo lo VEIA y con que llevaba en la mano. Y la MAGNITUD de
F-HERMANO-AMENAZA en los 200 tics antes de morir (no solo si estaba en la
tabla: `M`).  SOLO LECTURA.
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
import serie_util as U

OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.Counter(); vidas = []
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
            if sl not in (10, 11):
                continue
            recs = list(U.lee(f))
            cat = next(r for r in recs if r["k"] == "catalogo")
            dano = {it["id"]: float(it.get("damage") or 0) for it in cat["items"]}
            fin = next((r for r in recs if r.get("k") == "final"), None)
            T = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
            del recs
            golpes = []; ult = None
            for r in T:
                ve = {a.get("slot"): a for a in (r.get("ve_agentes") or [])}
                for g in (r.get("damage_taken") or []):
                    s = str(g.get("source"))
                    if not s.startswith("P"):
                        S[f"golpes de {s}"] += 1; continue
                    slot = int(s[1:]); a = ve.get(slot)
                    if a is None:
                        k = "rival NO visto"
                    else:
                        h = a.get("hand")
                        k = "rival visto CON arma en mano" if h and h != "none" and dano.get(h, 0) > 0 else "rival visto con hand NONE"
                    S[f"golpes de {k}"] += 1
                    golpes.append((r["tick"], slot, k, g.get("amount")))
            d = {"carp": os.path.basename(carp), "slot": sl}
            if fin and fin.get("reason") == "eliminated":
                mt = int(fin.get("match_ticks") or T[-1]["tick"])
                cerca = [g for g in golpes if mt - 48 <= g[0] <= mt]
                zona = any(x.get("source") == "zone" for r in T if mt - 48 <= r["tick"] <= mt for x in (r.get("damage_taken") or []))
                if cerca and (not zona or cerca[-1][0] >= max(r["tick"] for r in T if mt - 48 <= r["tick"] <= mt and any(x.get("source") == "zone" for x in (r.get("damage_taken") or [])))):
                    d["causa"] = cerca[-1][2]; d["matador"] = cerca[-1][1]
                elif zona:
                    d["causa"] = "anillo"
                else:
                    d["causa"] = "no consta"
                S[f"muere por {d['causa']}"] += 1
                # magnitud de F-HERMANO-AMENAZA en los 200 ultimos tics
                ms = [(((r.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("filas") or {}).get("F-HERMANO-AMENAZA", {}).get("M", 0.0)
                      for r in T if r["tick"] > T[-1]["tick"] - 200]
                d["amenaza_M_max"] = max(ms) if ms else 0; d["amenaza_M_media"] = st.mean(ms) if ms else 0
                d["golpes_ult200"] = collections.Counter(g[2] for g in golpes if g[0] > T[-1]["tick"] - 200)
                d["golpes_ult200"] = dict(d["golpes_ult200"]); d["tic"] = mt
            vidas.append(d)
    OUT[etiq] = {"recuento": dict(S), "vidas": vidas}
    print(f"### {etiq}")
    for k, v in sorted(S.items()):
        print(f"  {k:36s} {v}")
    print("  muertes por rival, con la M maxima de F-HERMANO-AMENAZA en los 200 ultimos tics:")
    for d in vidas:
        if d.get("causa") and d["causa"] != "anillo" and d["causa"] != "no consta":
            print(f"    {d['carp']} s{d['slot']} t{d['tic']} {d['causa']:28s} matador P{d['matador']} · amenaza M max {d['amenaza_M_max']:.3f} media {d['amenaza_M_media']:.3f} · golpes ult200 {d['golpes_ult200']}")
    am = [d for d in vidas if d.get("causa") and d["amenaza_M_max"] >= 0.1]
    print(f"  muertes con F-HERMANO-AMENAZA M >= 0,1 en los ultimos 200 tics: {len(am)} -> " + "; ".join(f"{d['carp']} s{d['slot']} {d['causa']} Mmax {d['amenaza_M_max']:.2f}" for d in am))
json.dump(OUT, open(os.path.join(AQUI, "P6_11_golpes.json"), "w"), ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_11_golpes.json")
