"""[P6-27 · 2-4] LAS MEDIDAS DE A8 (humo y serie) DESDE LOS DIARIOS, ademas de `mide_P6_26.py` (llamadas, coste,
retraso, respuestas que pasaban al pedir y se rechazan al llegar, intraducibles, E2 sustituidos, planes del hermano)
y de `mide_pasos_P6_22.py` (pasos perdidos):
  · aceptadas y CUMPLIDAS hasta el final de la fase (compromiso6 `cumplida` por «fin de fase»);
  · planes enviados y recibidos por el hermano, y aceptados por las dos puertas (los dos hermanos con plan vivo a la vez
    en la misma partida);
  · ACEPTACIONES FALSAS: para cada plan aceptado, lo imaginado contra lo vivido en sus puntos de control:
      (i) con `malestar26` (A8): la necesidad de vida imaginada (curva de la puerta) y la sentida en cada punto;
      (ii) con los registros `confianza` (A8 y A7h, la misma medida): `d_real` contra `d_proyectada` en cada punto de
           control (d = la distancia-malestar del cuerpo, la que la puerta proyecta); fraccion de puntos y de planes con
           lo vivido PEOR que lo imaginado (d_real > d_proyectada) y la diferencia mediana. Esto SI se puede calcular
           para el oraculo en los diarios de A7h, porque `confianza` se escribe en los dos.
  · pasos perdidos en tics de encargo o consulta del razonador (criterio (a) del humo), con `atribuye`.
    python3 mide_P6_27.py SALIDA.json 'A8=paintball/runs/P627_t0_A8_*' ['A7h=paintball/runs/P623_t2_A7h_*;...']
"""
import collections, glob, json, math, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
import mide_P6_26 as M26
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}


def q(xs, p):
    xs = sorted(x for x in xs if x is not None)
    return (xs[min(len(xs) - 1, int(p * len(xs)))] if xs else None)


def vida(f):
    v = M26.vida(f)
    recs = list(U.lee(f)); pc = next(r for r in recs if r.get("k") == "player_config"); zs = pc["zone_schedule"]
    sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo"); mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    ac = [r for r in recs if r.get("k") == "forma_aceptada"]; c6 = [r for r in recs if r.get("k") == "compromiso6"]; conf = [r for r in recs if r.get("k") == "confianza" and r.get("d_real") is not None]
    ids = {r["id"] for r in ac}
    cumpl_fin = {r["id"] for r in c6 if r.get("estado") == "cumplida" and r.get("por") == "fin de fase" and r.get("id") in ids}
    # aceptaciones falsas por `confianza`: por punto y por plan
    por_plan = collections.defaultdict(list)
    for r in conf:
        if r.get("id") in ids:
            por_plan[r["id"]].append((r["punto"], r["d_real"], r["d_proyectada"]))
    puntos = [(dr, dp) for ps in por_plan.values() for _p, dr, dp in ps]
    peor_punto = sum(1 for dr, dp in puntos if dr > dp); planes_peor = sum(1 for ps in por_plan.values() if any(dr > dp for _p, dr, dp in ps))
    planes_peor_1 = sum(1 for ps in por_plan.values() if any(dr > dp for p_, dr, dp in ps if p_ == 0))
    dif = [dr - dp for dr, dp in puntos]
    # malestar26 (A8): necesidad de vida imaginada contra sentida por tramo
    ma = [r for r in recs if r.get("k") == "malestar26"]; m_puntos = []
    for m in ma:
        for t in m.get("tramos") or []:
            ni = ((t.get("imaginado") or {}).get("nec") or [None])[0]; np_ = ((t.get("pasado") or {}).get("nec") or [None])[0]
            if ni is not None and np_ is not None:
                m_puntos.append((np_, ni))
    # pasos perdidos en tics de encargo/consulta del razonador
    T = {}; enc = set(); preg = set(); vuelta = set()
    for r in recs:
        k = r.get("k")
        if k == "tick" and r.get("phase") == "live":
            T[r["tick"]] = {"pos": (int(r["pos"][0]), int(r["pos"][1])), "int": r.get("intencion") or {}, "mri": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0), "ar": r.get("action_result_obs", r.get("action_result")), "ve": {tuple(a["pos"]) for a in (r.get("ve_agentes") or []) if a.get("pos")}, "ms16": (r.get("RADIOGRAFIA") or {}).get("ms16")}
        elif k == "hilo_forma" and "encargada" in (r.get("estado") or ""): enc.add(r["tick"])
        elif k == "razonador26" and r.get("estado") in ("encargado al proceso", "pregunta hecha"): preg.add(r["tick"])
        elif k == "razonador26" and r.get("estado") == "propone": vuelta.add(r["tick"])
    perd = []
    for t in sorted(T):
        prev = T.get(t - 1); r = T[t]
        if prev is None:
            continue
        pm = prev["int"].get("do") == "move" and prev["int"].get("dir") in DIRS
        if pm and prev["mri"] == 0:
            dx, dy = DIRS[prev["int"]["dir"]]; dest = (prev["pos"][0] + dx, prev["pos"][1] + dy)
            if not mundo.solido(*dest) and dest not in prev["ve"] and r["ar"] == "ok" and r["pos"] == prev["pos"] and r["mri"] == 0:
                tp = t - 1
                perd.append({"tick": tp, "fase": ("5-7" if tp >= zs[4][0] else ("1-4" if tp >= zs[0][0] else "antes")), "en_razonador": any(u in preg or u in vuelta for u in (tp - 1, tp)), "en_encargo_juicio": any(u in enc for u in (tp - 1, tp)), "ms16": prev["ms16"]})
    v.update({"aceptadas": len(ac), "cumplidas_fin_fase": len(cumpl_fin), "falsas_confianza": {"planes_con_puntos": len(por_plan), "puntos": len(puntos), "puntos_peor": peor_punto, "planes_peor_algun_punto": planes_peor, "planes_peor_primer_punto": planes_peor_1,
                                                                                                    "dif_mediana (d_real - d_proyectada)": (round(st.median(dif), 5) if dif else None), "dif_p90": q(dif, 0.9)},
              "falsas_malestar26": {"tramos": len(m_puntos), "peor": sum(1 for np_, ni in m_puntos if np_ > ni), "dif_mediana (sentida - imaginada, vida)": (round(st.median([np_ - ni for np_, ni in m_puntos]), 4) if m_puntos else None)},
              "pasos_perdidos": perd, "pasos_perdidos_5_7": sum(1 for p in perd if p["fase"] == "5-7"), "pasos_perdidos_en_razonador": sum(1 for p in perd if p["en_razonador"]), "pasos_perdidos_en_encargo_juicio": sum(1 for p in perd if p["en_encargo_juicio"]),
              "planes_vivos": [(r["tick"], r["id"]) for r in ac], "planes_cerrados": {r["id"]: r["tick"] for r in recs if r.get("k") == "forma_caida" or (r.get("k") == "compromiso6" and r.get("estado") == "cumplida")}})
    return v


def pareja_aceptan_las_dos(vs):
    """En la misma partida, cuantas veces los dos hermanos tienen un plan aceptado VIVO a la vez."""
    por = collections.defaultdict(list)
    for v in vs:
        por[v["carp"]].append(v)
    out = {"partidas": 0, "veces_los_dos_con_plan_vivo": 0, "planes_del_hermano_recibidos": sum(v["planes_del_hermano_recibidos"] for v in vs), "planes_enviados": sum(v["e2_sustituidos"] for v in vs)}
    for carp, dd in por.items():
        if len(dd) != 2:
            continue
        out["partidas"] += 1
        a, b = dd
        def vivos(v):
            return [(t, v["planes_cerrados"].get(i, t + 400)) for t, i in v["planes_vivos"]]
        for ta, fa in vivos(a):
            for tb, fb in vivos(b):
                if ta <= fb and tb <= fa:
                    out["veces_los_dos_con_plan_vivo"] += 1
    return out


if __name__ == "__main__":
    salida = sys.argv[1]; OUT = {"nota": __doc__.split("\n")[0], "brazos": {}}
    for etiq, pats in [x.split("=", 1) for x in sys.argv[2:]]:
        V = []
        for pat in pats.split(";"):
            for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
                for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
                    sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)); v = vida(f); v["carp"] = os.path.basename(carp); v["slot"] = sl; V.append(v)
                    print(f"  {v['carp']} s{sl}: llamadas {v['llamadas']} · usd {v['usd']} · retraso {v['retraso_tics']['mediana']} · aceptadas {v['aceptadas']} cumplidas fin {v['cumplidas_fin_fase']} · ya rechaza {v['llegan_donde_la_puerta_ya_rechaza']} · perdidos 5-7 {v['pasos_perdidos_5_7']} (razonador {v['pasos_perdidos_en_razonador']}, juicio {v['pasos_perdidos_en_encargo_juicio']}) · falsas conf {v['falsas_confianza']['planes_peor_algun_punto']}/{v['falsas_confianza']['planes_con_puntos']}", flush=True)
        retr = [x for v in V for x in [r["retraso"] for r in v["pares_pregunta_llegada"]]]
        dif = []; puntos = 0; peor = 0; planes = 0; planes_peor = 0
        for v in V:
            fc = v["falsas_confianza"]; puntos += fc["puntos"]; peor += fc["puntos_peor"]; planes += fc["planes_con_puntos"]; planes_peor += fc["planes_peor_algun_punto"]
        tot = {"vidas": len(V), "partidas": len({v["carp"] for v in V}), "llamadas": sum(v["llamadas"] for v in V), "usd": round(sum(v["usd"] for v in V), 6), "usd_por_llamada": (round(sum(v["usd"] for v in V) / max(1, sum(v["llamadas"] for v in V)), 5)),
               "llamadas_por_vida": (round(st.mean(v["llamadas"] for v in V), 2) if V else None), "retraso_tics": {"n": len(retr), "mediana": q(retr, 0.5), "p95": q(retr, 0.95)}, "propone": sum(v["propone"] for v in V), "intraducibles": sum(v["intraducibles"] for v in V), "calla": sum(v["calla"] for v in V), "errores": sum(len(v["errores"]) for v in V),
               "pasan_pregunta": sum(v["pasan_pregunta"] for v in V), "pasan_llegada": sum(v["pasan_llegada"] for v in V), "llegan_donde_la_puerta_ya_rechaza": sum(v["llegan_donde_la_puerta_ya_rechaza"] for v in V),
               "aceptadas": sum(v["aceptadas"] for v in V), "cumplidas_fin_fase": sum(v["cumplidas_fin_fase"] for v in V), "e2_sustituidos": sum(v["e2_sustituidos"] for v in V), "planes_del_hermano_recibidos": sum(v["planes_del_hermano_recibidos"] for v in V), "pareja": pareja_aceptan_las_dos(V),
               "falsas_confianza": {"planes_con_puntos": planes, "planes_peor_algun_punto": planes_peor, "pct_planes_peor": (round(100 * planes_peor / planes, 1) if planes else None), "puntos": puntos, "puntos_peor": peor, "pct_puntos_peor": (round(100 * peor / puntos, 1) if puntos else None)},
               "falsas_malestar26": {"tramos": sum(v["falsas_malestar26"]["tramos"] for v in V), "peor": sum(v["falsas_malestar26"]["peor"] for v in V)},
               "pasos_perdidos_5_7": sum(v["pasos_perdidos_5_7"] for v in V), "pasos_perdidos_en_razonador": sum(v["pasos_perdidos_en_razonador"] for v in V), "pasos_perdidos_en_encargo_juicio": sum(v["pasos_perdidos_en_encargo_juicio"] for v in V), "pasos_perdidos_total": sum(len(v["pasos_perdidos"]) for v in V)}
        # la diferencia mediana de las falsas, sobre todos los puntos
        difs = []
        for v in V:
            pass
        OUT["brazos"][etiq] = {"total": tot, "vidas": V}
        print(f"### {etiq}: {json.dumps(tot, ensure_ascii=False)}")
    json.dump(OUT, open(os.path.join(AQUI, salida), "w"), ensure_ascii=False, indent=1)
    print("->", salida)
