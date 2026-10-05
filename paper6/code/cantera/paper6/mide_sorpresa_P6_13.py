"""[P6-13 · 4] CUANTO IMAGINA EL CUERPO EL ANILLO. SOLO LECTURA.

La misma medida que P6-4 hizo con S-8 (`mide_P6_4.py:201-218`): en cada tic con
detalle y piernas listas, la fila que el ganador PREVIO en su foto (`candidatos
[elegido].filas`) contra la fila REAL en el siguiente tic con piernas listas
(`ahora.filas`). Aqui, F-ANTICIPACION (la unica fila que lee el anillo), y S-8
al lado para comparar. Se guarda tambien el signo (previsto - real): si el
cuerpo se queda corto o se pasa. Y por fase del anillo.
Ademas: ¿la foto prevista lleva el anillo avanzado? Se comprueba en el decisor
(`_obs_prevista` pone `zone` = `mundo.anillo_en(tick_eval)`, decisor_zs.py:357)
y en los datos: en los tics con detalle, cuantas veces la F-ANTICIPACION prevista
del ganador es > 0 cuando la real siguiente es > 0.
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5")):
    sys.path.insert(0, p)
import serie_util as U
FASES = None
def fase_de(t):
    if not FASES or t < FASES[0][0]: return 0
    return max(i + 1 for i, f in enumerate(FASES) if f[0] <= t)
OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.defaultdict(list); C = collections.Counter()
    for f in sorted(glob.glob(os.path.join(RAIZ, pat, "*policy_agent_1*.art.log"))):
        T = []
        for r in U.lee(f):
            if r.get("k") == "player_config" and FASES is None:
                FASES = [tuple(z) for z in r.get("zone_schedule") or []]
            if r.get("k") != "tick" or r.get("phase") != "live":
                continue
            ra = r.get("RADIOGRAFIA") or {}
            T.append((r["tick"], int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0) == 0, ra.get("candidatos"), ra.get("elegido"),
                      {k: v.get("M") for k, v in ((ra.get("ahora") or {}).get("filas") or {}).items()}))
        listas = [x for x in T if x[1]]
        for (t, _, cand, el, _fl), (t2, _, _c2, _e2, fl2) in zip(listas, listas[1:]):
            if not cand or not isinstance(cand.get(el), dict) or cand[el].get("filas") is None:
                continue
            fp = cand[el]["filas"]; fase = fase_de(t)
            for fila in ("F-ANTICIPACION", "S-8-EXPOSICION"):
                p = float(fp.get(fila) or 0.0); q = float(fl2.get(fila) or 0.0)
                S[(fila, "abs")].append(abs(q - p)); S[(fila, "signo")].append(p - q); S[(fila, "abs", fase)].append(abs(q - p))
                if q > 0: C[(fila, "real>0")] += 1; C[(fila, "real>0 y prevista>0")] += (p > 0)
                if p > 0: C[(fila, "prevista>0")] += 1
            C["pares"] += 1
    res = {}
    for fila in ("F-ANTICIPACION", "S-8-EXPOSICION"):
        a = S[(fila, "abs")]; sg = S[(fila, "signo")]
        res[fila] = {"n": len(a), "sorpresa_mediana": st.median(a) if a else None, "sorpresa_media": st.mean(a) if a else None, "sorpresa_suma": sum(a),
                     "signo_medio (prevista-real)": st.mean(sg) if sg else None, "se_queda_corto (real>prevista) %": 100 * sum(1 for x in sg if x < -1e-9) / (len(sg) or 1),
                     "se_pasa %": 100 * sum(1 for x in sg if x > 1e-9) / (len(sg) or 1),
                     "real>0": C[(fila, "real>0")], "real>0 y prevista>0": C[(fila, "real>0 y prevista>0")], "prevista>0": C[(fila, "prevista>0")],
                     "por_fase": {fz: {"n": len(S[(fila, "abs", fz)]), "mediana": st.median(S[(fila, "abs", fz)]), "media": st.mean(S[(fila, "abs", fz)])} for fz in range(0, 8) if S[(fila, "abs", fz)]}}
    OUT[etiq] = res
    print(f"### {etiq}: {C['pares']} pares de tics con detalle y piernas listas")
    for fila, v in res.items():
        print(f"  {fila}: sorpresa |real-prevista| mediana {v['sorpresa_mediana']:.5f} media {v['sorpresa_media']:.5f} suma {v['sorpresa_suma']:.1f} · signo medio {v['signo_medio (prevista-real)']:+.5f} · se queda corto {v['se_queda_corto (real>prevista) %']:.1f} % · se pasa {v['se_pasa %']:.1f} % · real>0 {v['real>0']} de los cuales prevista>0 {v['real>0 y prevista>0']}")
        print("    por fase:", {fz: f"n={x['n']} med={x['mediana']:.4f} media={x['media']:.4f}" for fz, x in v["por_fase"].items()})
json.dump(OUT, open(os.path.join(AQUI, "P6_13_sorpresa.json"), "w"), ensure_ascii=False, indent=1)
