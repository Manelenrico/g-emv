"""[P6-8 · C] EL CAMINO DE VUELTA, sobre TODOS los tics sin ver al hermano.

Por brazo, tics con el hermano vivo y fuera de la vista, con parte fresco:
  · con piernas listas: ¿esta `ir_pareja` entre los candidatos? ¿gana?
  · con detalle de candidatos (cada 24 tics) e `ir_pareja` candidato:
    d(ir_pareja) - d(noop), y M(ir_pareja) - M(noop) de S-8-EXPOSICION — es
    decir, cuanto sigue pesando la exposicion (contados incluidos) en volver.
  · ademas: cuantos rivales CONTADOS hay en la percepcion en esos tics (del E2
    del hermano, edad <= 50, no vistos), para atribuir la exposicion.
SOLO LECTURA.
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
import serie_util as U
import parte2 as P2
import oyente2 as OY

OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.Counter(); dd, s8, s8c, s8n = [], [], [], []
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
            ult = None
            for r in recs:
                if r.get("k") != "tick" or r.get("phase") != "live":
                    continue
                for m in (r.get("chat") or []):
                    if m.get("channel") == "team" and m.get("from") == herm and (m.get("text") or "").startswith("E2 "):
                        p = P2.parsea(m["text"], mundo)
                        if p:
                            ult = p
                t = r["tick"]; so = r.get("social") or {}; ra = r.get("RADIOGRAFIA") or {}
                ah = ra.get("ahora") or {}; pf = ah.get("parte")
                S["tics"] += 1
                if so.get("pareja_vista") or r.get("pareja_muerta") or not (pf and pf.get("pos")):
                    continue
                S["hermano vivo, fuera de vista, parte fresco"] += 1
                vistos = {a.get("slot") for a in (r.get("ve_agentes") or [])}
                ncont = sum(1 for x in ult["rivales"] if x["slot"] not in vistos) if ult and 0 <= t - ult["t"] <= OY.CADUCIDAD_RIVAL else 0
                if ncont:
                    S["  ...con rival contado en la percepcion"] += 1
                cs = ra.get("candidatos") or {}
                if int(r.get("move_ready_in") or 0) == 0:
                    S["  con piernas listas"] += 1
                    if "ir_pareja" in cs:
                        S["    ir_pareja candidato"] += 1
                        if ra.get("elegido") == "ir_pareja":
                            S["    ir_pareja ELEGIDO"] += 1
                if isinstance(cs.get("noop"), dict) and isinstance(cs.get("ir_pareja"), dict):
                    n, p = cs["noop"], cs["ir_pareja"]
                    dd.append(p["d"] - n["d"])
                    x = (p.get("filas") or {}).get("S-8-EXPOSICION", 0.0) - (n.get("filas") or {}).get("S-8-EXPOSICION", 0.0)
                    s8.append(x); (s8c if ncont else s8n).append(x)
            del recs
    n = S["    ir_pareja candidato"] or 1
    res = {"recuento": dict(S),
           "ir_pareja_elegido_pct": 100 * S["    ir_pareja ELEGIDO"] / n,
           "detalle_n": len(dd), "d_dif_mediana": st.median(dd) if dd else None,
           "noop_gana_pct": 100 * sum(x > 0 for x in dd) / (len(dd) or 1),
           "s8_dif_mediana": st.median(s8) if s8 else None, "s8_positiva_pct": 100 * sum(x > 0 for x in s8) / (len(s8) or 1),
           "s8_con_contado_mediana": st.median(s8c) if s8c else None, "s8_con_contado_n": len(s8c),
           "s8_sin_contado_mediana": st.median(s8n) if s8n else None, "s8_sin_contado_n": len(s8n)}
    OUT[etiq] = res
    print(f"### {etiq}")
    for k, v in S.items():
        print(f"  {k:48s} {v}")
    print(f"  ir_pareja elegido / candidato (piernas listas): {res['ir_pareja_elegido_pct']:.2f} %")
    print(f"  detalle: {len(dd)} tics · d(ir_pareja)-d(noop) mediana {res['d_dif_mediana']:+.4f} · noop gana {res['noop_gana_pct']:.1f} %")
    print(f"  S-8 M(ir_pareja)-M(noop): mediana {res['s8_dif_mediana']:+.4f} · positiva {res['s8_positiva_pct']:.1f} % · con contado {res['s8_con_contado_mediana']} (n={len(s8c)}) · sin contado {res['s8_sin_contado_mediana']} (n={len(s8n)})")
json.dump(OUT, open(os.path.join(AQUI, "P6_10_vuelta2.json"), "w"), ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_10_vuelta2.json")
