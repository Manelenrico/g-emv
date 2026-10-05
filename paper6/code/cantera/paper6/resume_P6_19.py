"""[P6-19 · 2 y 3] El resumen del banco de puerta6g. Instrumento de medida.
  fidelidad: error de vida prevista (prevista - real) a +50/+100/+200 de puerta6, puerta6g y
             puerta6g_ctx en las decisiones del oraculo de las 40 vidas de A4 (P6-15); y de que
             es el dano real de esas ventanas (anillo / rivales).
  momentos:  los 85 de P6-18 juzgados con las tres puertas; «promete de mas» = vida prevista de
             la curva del plan menos la real en cada punto de control.
  a6:        los planes propuestos en el campo por A6, juzgados con las tres; y las caidas por
             «vida real por debajo de la proyectada»: cuantas dejarian de caer con la curva g.
"""
import collections, glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("P619_SCRATCH") or os.path.join(AQUI, "_P6_19_tmp")
PUERTAS = ("puerta6", "puerta6g", "puerta6g_ctx")
MP = 0.062
R = {"nota": "P6-19. INSTRUMENTO DE MEDIDA."}


def q(xs):
    xs = sorted(xs); return {"n": len(xs), "media": round(st.mean(xs), 3), "mediana": round(xs[len(xs) // 2], 3), "p10": round(xs[len(xs) // 10], 3), "p90": round(xs[int(len(xs) * 0.9)], 3), "mad": round(st.mean(abs(x) for x in xs), 3)} if xs else None


# ── fidelidad ──
F = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(OUT, "fidelidad_*.json")))]
reg = [r for v in F for r in v["registros"]]
fid = {"vidas": len(F), "decisiones": len(reg)}
for k in (50, 100, 200):
    sel = [r for r in reg if all(f"error_{k}" in r[p] for p in PUERTAS)]
    fid[f"+{k}"] = {"n": len(sel), "dano_real_anillo_media": round(st.mean(r[f"dano_real_anillo_{k}"] for r in sel), 2) if sel else None, "dano_real_rival_media": round(st.mean(r[f"dano_real_rival_{k}"] for r in sel), 2) if sel else None,
                   "con_dano_rival": sum(1 for r in sel if r[f"dano_real_rival_{k}"] > 0)}
    for p in PUERTAS:
        e = [r[p][f"error_{k}"] for r in sel]
        fid[f"+{k}"][p] = {"error": q(e), "promete_de_mas (error > 10)": sum(1 for x in e if x > 10), "promete_de_menos (error < -10)": sum(1 for x in e if x < -10),
                            "vida_prevista_media": round(st.mean(r[p][f"vida_{k}"] for r in sel), 2) if sel else None, "real_media": round(st.mean(r[p][f"real_{k}"] for r in sel), 2) if sel else None}
    # solo las decisiones con dano de rival real en la ventana
    sr = [r for r in sel if r[f"dano_real_rival_{k}"] > 0]
    fid[f"+{k}"]["con_golpes_reales"] = {p: q([r[p][f"error_{k}"] for r in sr]) for p in PUERTAS}
    fid[f"+{k}"]["con_golpes_reales"]["n"] = len(sr)
fid["dano_esperado_ahora"] = q([r["dano_esperado_ahora"] for r in reg])
fid["ms"] = {p: q([r[p]["ms"] for r in reg]) for p in PUERTAS}
R["fidelidad"] = fid
print("=== FIDELIDAD", fid["vidas"], "vidas", fid["decisiones"], "decisiones · dano esperado ahora", fid["dano_esperado_ahora"])
for k in (50, 100, 200):
    x = fid[f"+{k}"]
    print(f"   +{k}: n {x['n']} · dano real anillo {x['dano_real_anillo_media']} rival {x['dano_real_rival_media']} (con rival {x['con_dano_rival']})")
    for p in PUERTAS:
        print(f"      {p:13s} error {x[p]['error']} · de mas {x[p]['promete_de_mas (error > 10)']} de menos {x[p]['promete_de_menos (error < -10)']} · prevista {x[p]['vida_prevista_media']} real {x[p]['real_media']} · con golpes reales {x['con_golpes_reales'][p]}")

# ── momentos ──
M = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(OUT, "momentos_*.json")))]
mom = [r for v in M for r in v["registros"]]
res_m = {}
for brazo in ("A5h", "A4"):
    S = [r for r in mom if r["brazo"] == brazo and all(p in r for p in PUERTAS)]
    d = {"n": len(S)}
    for p in PUERTAS:
        vc = collections.Counter(r[p]["veredicto"] for r in S)
        prom = [c["vida"] - c["vida_real"] for r in S for c in r[p]["curva"][1:] if c["vida"] is not None]
        d[p] = {"veredictos": dict(vc), "prefiere_quedarse": vc.get("ok", 0), "pct": round(100 * vc.get("ok", 0) / max(1, len(S)), 1), "ventaja": q([r[p]["ventaja"] for r in S]),
                "promete_de_mas (vida prevista - real en los puntos de control)": q(prom)}
    d["cambian"] = {"puerta6 ok -> puerta6g no": sum(1 for r in S if r["puerta6"]["veredicto"] == "ok" and r["puerta6g"]["veredicto"] != "ok"), "puerta6 no -> puerta6g ok": sum(1 for r in S if r["puerta6"]["veredicto"] != "ok" and r["puerta6g"]["veredicto"] == "ok"),
                   "puerta6 ok -> ctx no": sum(1 for r in S if r["puerta6"]["veredicto"] == "ok" and r["puerta6g_ctx"]["veredicto"] != "ok"), "puerta6 no -> ctx ok": sum(1 for r in S if r["puerta6"]["veredicto"] != "ok" and r["puerta6g_ctx"]["veredicto"] == "ok")}
    res_m[brazo] = d
    print(f"=== MOMENTOS {brazo}: n {len(S)}")
    for p in PUERTAS:
        print(f"   {p:13s} {d[p]['veredictos']} · prefiere {d[p]['prefiere_quedarse']} ({d[p]['pct']} %) · ventaja {d[p]['ventaja']} · promete de mas {d[p]['promete_de_mas (vida prevista - real en los puntos de control)']}")
    print("   cambian:", d["cambian"])
R["momentos"] = res_m

# ── a6 ──
A6 = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(OUT, "a6_*.json")))]
pl = [r for v in A6 for r in v["registros"] if all(p in r for p in PUERTAS)]
ca = [c for v in A6 for c in v["caidas"]]
a6 = {"vidas": len(A6), "planes_propuestos_juzgados": len(pl), "caidas_vida_real": len(ca)}
for p in PUERTAS:
    vc = collections.Counter(r[p]["veredicto"] for r in pl)
    prom = [c["vida"] - c["vida_real"] for r in pl for c in r[p]["curva"][1:] if c["vida"] is not None]
    a6[p] = {"veredictos": dict(vc), "ok": vc.get("ok", 0), "pct": round(100 * vc.get("ok", 0) / max(1, len(pl)), 1), "ventaja": q([r[p]["ventaja"] for r in pl]), "promete_de_mas": q(prom)}
a6["cambian"] = {"puerta6 ok -> g no": sum(1 for r in pl if r["puerta6"]["veredicto"] == "ok" and r["puerta6g"]["veredicto"] != "ok"), "puerta6 no -> g ok": sum(1 for r in pl if r["puerta6"]["veredicto"] != "ok" and r["puerta6g"]["veredicto"] == "ok"),
                 "puerta6 ok -> ctx no": sum(1 for r in pl if r["puerta6"]["veredicto"] == "ok" and r["puerta6g_ctx"]["veredicto"] != "ok"), "puerta6 no -> ctx ok": sum(1 for r in pl if r["puerta6"]["veredicto"] != "ok" and r["puerta6g_ctx"]["veredicto"] == "ok")}
cj = [c for c in ca if "caeria_con_g" in c]
a6["caidas"] = {"n": len(ca), "juzgadas": len(cj), "seguirian_cayendo_con_g": sum(1 for c in cj if c["caeria_con_g"]), "dejarian_de_caer_con_g": sum(1 for c in cj if not c["caeria_con_g"]),
                "seguirian_cayendo_con_ctx": sum(1 for c in cj if c["caeria_con_ctx"]), "dejarian_de_caer_con_ctx": sum(1 for c in cj if not c["caeria_con_ctx"]),
                "hueco_real_menos_proyectada": q([c["hp_real"] - c["proyectada"] for c in cj if c["hp_real"] is not None]), "proyectada_g_menos_6": q([c["proyectada_g"] - c["proyectada_6"] for c in cj if c["proyectada_g"] is not None]),
                "proyectada_ctx_menos_6": q([c["proyectada_ctx"] - c["proyectada_6"] for c in cj if c.get("proyectada_ctx") is not None]),
                "veredicto_g_de_las_caidas": dict(collections.Counter(c["veredicto_g"] for c in cj)), "veredicto_ctx_de_las_caidas": dict(collections.Counter(c["veredicto_ctx"] for c in cj))}
R["a6"] = a6
print(f"=== A6: {len(A6)} vidas · planes {len(pl)} · caidas {len(ca)}")
for p in PUERTAS:
    print(f"   {p:13s} {a6[p]['veredictos']} · ok {a6[p]['ok']} ({a6[p]['pct']} %) · ventaja {a6[p]['ventaja']} · promete de mas {a6[p]['promete_de_mas']}")
print("   cambian:", a6["cambian"]); print("   caidas:", a6["caidas"])
json.dump(R, open(os.path.join(AQUI, "P6_19_banco.json"), "w"), ensure_ascii=False, indent=1)
print("-> P6_19_banco.json")
