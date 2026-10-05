"""[P6-18 · A.2 y A.6] El resumen del banco de «ir y quedarse»: de las salidas por vida a
`P6_18_banco.json`, con el criterio de campo calculado. Instrumento de medida.
  · prefiere quedarse = veredicto «ok» (ventaja > margen 0,062) del plan de quedarse;
  · veto al salir = ruptura (a) de compromiso6 en los 12 primeros tics de la ventana
    (el tic del paso de salida esta en ellos); veto en la ventana = fraccion de tics
    con (a) hasta el final de la fase.
"""
import collections, glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("P618_SCRATCH") or os.path.join(AQUI, "_P6_18_tmp")
vidas = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(OUT, "P61*_s*.json")))]
M = [m for v in vidas for m in v["momentos"]]
print(f"vidas {len(vidas)} · momentos {len(M)} · {collections.Counter(m['brazo'] for m in M)} · repro difiere total {sum(v['repro'].get('difiere', 0) for v in vidas)} de {sum(sum(v['repro'].values()) for v in vidas)}")
R = {"momentos": M, "resumen": {}}
def q(xs):
    xs = sorted(xs); return {"n": len(xs), "p10": round(xs[len(xs) // 10], 4), "mediana": round(xs[len(xs) // 2], 4), "p90": round(xs[int(len(xs) * 0.9)], 4)} if xs else None
for brazo in ("A5h", "A4"):
    S = [m for m in M if m["brazo"] == brazo]
    res = {"n": len(S), "propia_casilla": sum(1 for m in S if m["propia"]), "a_salvo": sum(1 for m in S if m["a_salvo"])}
    for nombre in ("H_fase", "H100"):
        for modo in ("cinco", "puerta6", "real"):
            ps = [m["planes"][nombre][modo] for m in S if nombre in m["planes"] and modo in m["planes"][nombre]]
            vc = collections.Counter(p["veredicto"] for p in ps)
            ok = [p for p in ps if p["veredicto"] == "ok"]
            res[f"{nombre}·{modo}"] = {"veredictos": dict(vc), "prefiere_quedarse": len(ok), "pct": (round(100 * len(ok) / len(ps), 1) if ps else None), "ventaja": q([p["ventaja"] for p in ps]),
                                      "ventaja_ok": q([p["ventaja"] for p in ok])}
            if modo != "real":
                contra = collections.defaultdict(list)
                for p in ps:
                    for k, dk, Mp, Mc in (p.get("contra") or []):
                        contra[k].append(dk)
                res[f"{nombre}·{modo}"]["filas_en_contra"] = {k: {"n": len(v), "media": round(sum(v) / len(v), 5), "total": round(sum(v), 4)} for k, v in sorted(contra.items(), key=lambda kv: -sum(kv[1])) if sum(v) > 0}
                res[f"{nombre}·{modo}"]["filas_a_favor"] = {k: {"n": len(v), "media": round(sum(v) / len(v), 5), "total": round(sum(v), 4)} for k, v in sorted(contra.items(), key=lambda kv: sum(kv[1])) if sum(v) < 0}
    # el veto
    vs = [m.get("ventana_quedarse") or {} for m in S]
    res["veto"] = {"ventanas": len(vs), "veto_a_en_los_12_primeros_tics": sum(1 for v in vs if v.get("primera_a_en") is not None and v["primera_a_en"] <= 11),
                   "ventanas_con_algun_veto_a": sum(1 for v in vs if (v.get("rupturas") or {}).get("a)")),
                   "fraccion_tics_con_a_mediana": (st.median((v.get("rupturas") or {}).get("a)", 0) / max(1, v.get("tics") or 1) for v in vs) if vs else None),
                   "fraccion_tics_con_d_mediana": (st.median((v.get("rupturas") or {}).get("d)", 0) / max(1, v.get("tics") or 1) for v in vs) if vs else None),
                   "rupturas_total": dict(sum((collections.Counter(v.get("rupturas") or {}) for v in vs), collections.Counter())), "tics_total": sum(v.get("tics") or 0 for v in vs)}
    # cruce: prefiere (puerta6, H_fase) x veto al salir
    for nombre in ("H_fase", "H100"):
        cr = collections.Counter()
        for m, v in zip(S, vs):
            p = m["planes"].get(nombre, {}).get("puerta6")
            if not p:
                continue
            ok = p["veredicto"] == "ok"; veto = v.get("primera_a_en") is not None and v["primera_a_en"] <= 11
            cr[f"prefiere {ok} · veto al salir {veto}"] += 1
        res[f"cruce_{nombre}"] = dict(cr)
    R["resumen"][brazo] = res
    print(f"\n### {brazo}: n {res['n']} · propia casilla {res['propia_casilla']} · a salvo {res['a_salvo']}")
    for k, v in res.items():
        if "·" in k:
            print(f"   {k:16s} {v['veredictos']} · prefiere quedarse {v['prefiere_quedarse']} ({v['pct']} %) · ventaja {v['ventaja']} · ok {v['ventaja_ok']}")
            if v.get("filas_en_contra"):
                print(f"      en contra: {dict(list(v['filas_en_contra'].items())[:5])}")
                print(f"      a favor:   {dict(list(v['filas_a_favor'].items())[:5])}")
    print(f"   veto: {res['veto']}")
    print(f"   cruce H_fase: {res['cruce_H_fase']} · H100: {res['cruce_H100']}")
# el criterio
a5 = R["resumen"]["A5h"]
pref = a5["H_fase·puerta6"]["pct"]; veto12 = a5["veto"]["veto_a_en_los_12_primeros_tics"]; n = a5["n"]
R["criterio"] = {"prefiere_quedarse_puerta6_H_fase_pct": pref, "umbral_pct": 33.3, "veto_al_salir": veto12, "de": n, "veto_mayoria": veto12 > n / 2,
                 "pasa": (pref is not None and pref >= 33.3 and not (veto12 > n / 2))}
print(f"\n=== CRITERIO: puerta6 prefiere quedarse en {pref} % de los 63 (umbral 33,3) · veto (a) en los 12 primeros tics en {veto12} de {n} (mayoria: {veto12 > n / 2}) -> {'PASA' if R['criterio']['pasa'] else 'NO PASA'}")
json.dump(R, open(os.path.join(AQUI, "P6_18_banco.json"), "w"), ensure_ascii=False, indent=1)
print("-> P6_18_banco.json")
