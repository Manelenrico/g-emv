"""[P7-43b] EQUIDAD DE LA LENTITUD (mesa): por brazo y personalidad y por dia, % de decisiones por encima del tic y % de pasos listos bloqueados sin cuerpo (la guarda de
cada asiento, `latencia` en P7_50_estado.json). Si entre brazos el % sobre el tic difiere en mas de 2 puntos (media de la serie), se marca como DUDOSO en el informe (no para
el campo, salvo la guarda). Tambien: paradas, marcadas, creditos gastados. -> P7_50_equidad.json
  python3 equidad_P7_43.py [--serie S]"""
import json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(AQUI, "P7_50_estado.json"))); VAR = ("COMPARTE", "SOLAS")
S = int(sys.argv[sys.argv.index("--serie") + 1]) if "--serie" in sys.argv else None
P = [p for p in E["peticiones"] if p["brazo"] in VAR and p["estado"] == "completed" and (S is None or p["serie"] == S)]
R = {"serie": S, "partidas": len(P), "creditos": len(P), "por_brazo": {}, "por_dia": {}, "marcadas": [], "paradas": [(p["serie"], p["dia"], p["brazo"], sl, g.get("motivo")) for p in P for sl, g in (p.get("latencia") or {}).items() if g.get("para")]}
for v in VAR:
    gs = [(p["dia"], sl, g) for p in P if p["brazo"] == v for sl, g in (p.get("latencia") or {}).items() if g.get("ms_mediana") is not None]
    sobre = [g.get("sobre_el_tic") or 0 for _, _, g in gs]; bloq = [g.get("fraccion_sin_cuerpo") or 0 for _, _, g in gs]
    R["por_brazo"][v] = {"vidas": len(gs), "sobre_el_tic_media_pct": (round(100 * st.mean(sobre), 2) if sobre else None), "bloqueados_media_pct": (round(100 * st.mean(bloq), 2) if bloq else None), "ms_mediana": (round(st.median(g["ms_mediana"] for _, _, g in gs), 2) if gs else None), "ms_p95_max": (round(max(g.get("ms_p95") or 0 for _, _, g in gs), 1) if gs else None),
                        "marcadas": sum(1 for _, _, g in gs if not g.get("pasa")), "paradas": sum(1 for _, _, g in gs if g.get("para")),
                        "por_dia": {d: {"sobre_pct": round(100 * st.mean([g.get("sobre_el_tic") or 0 for dd, _, g in gs if dd == d]), 2), "bloq_pct": round(100 * st.mean([g.get("fraccion_sin_cuerpo") or 0 for dd, _, g in gs if dd == d]), 2)} for d in sorted({dd for dd, _, _ in gs})}}
    R["marcadas"] += [(p["serie"], p["dia"], v, sl) for p in P if p["brazo"] == v for sl, g in (p.get("latencia") or {}).items() if not g.get("pasa")]
vals = {v: x["sobre_el_tic_media_pct"] for v, x in R["por_brazo"].items() if x["sobre_el_tic_media_pct"] is not None}
R["equidad"] = {"max_diferencia_sobre_el_tic_puntos": (round(max(vals.values()) - min(vals.values()), 2) if vals else None), "dudoso": bool(vals) and (max(vals.values()) - min(vals.values())) > 2.0, "extremos": ((max(vals, key=vals.get), min(vals, key=vals.get)) if vals else None)}
json.dump(R, open(os.path.join(AQUI, f"P7_50_equidad{'_s' + str(S) if S else ''}.json"), "w"), ensure_ascii=False, indent=1)
print(f"serie {S}: {len(P)} partidas; equidad {R['equidad']}; paradas {R['paradas']}; marcadas {len(R['marcadas'])}")
for v, x in R["por_brazo"].items(): print(f"  {v}: vidas {x['vidas']} sobre el tic {x['sobre_el_tic_media_pct']} % bloqueados {x['bloqueados_media_pct']} % ms {x['ms_mediana']} p95 max {x['ms_p95_max']} marcadas {x['marcadas']}")
