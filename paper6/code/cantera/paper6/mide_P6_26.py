"""[P6-26 · 2] LAS MEDIDAS DEL HUMO DE CAMPO DE A8, por vida y por partida, de los diarios (`razonador26`,
`plan26`, `malestar26`, `forma_*`, `resumen26`) y los pasos perdidos (P6-21, `mide_pasos_P6_22`):
llamadas; coste en dolares (cabecera del sidecar, acumulada por pod); retraso en tics (mediana y p95);
respuestas que llegan a una escena donde la puerta ya rechaza (pasaban con la instantanea de la pregunta y
no con la de la llegada); intraducibles; pasos perdidos; E2 sustituidos; veces que el hermano recibe un plan;
y las tres columnas del malestar de cada plan aceptado (propuesto / imaginado / pasado). Con eso, el coste
estimado de una serie de 40 semillas. SOLO LECTURA, diarios de uno en uno.
    python3 mide_P6_26.py 'A8=paintball/runs/P626_t1_A8_*'   -> P6_26_humo.json
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U


def q(xs, p):
    xs = sorted(x for x in xs if x is not None)
    return (xs[min(len(xs) - 1, int(p * len(xs)))] if xs else None)


def vida(f):
    rz = []; pl = []; ma = []; ev = []; ac = []; res = None; fin = None; zs = None; arr = None; n_tics = 0; e2 = 0
    for r in U.lee(f):
        k = r.get("k")
        if k == "razonador26": rz.append(r)
        elif k == "plan26": pl.append(r)
        elif k == "malestar26": ma.append(r)
        elif k == "forma_evaluada": ev.append(r)
        elif k == "forma_aceptada": ac.append(r)
        elif k in ("resumen26", "resumen27"): res = r
        elif k == "final": fin = r
        elif k == "player_config": zs = r.get("zone_schedule")
        elif k == "arranque": arr = r
        elif k == "ojos" and r.get("estado") == "dicho": e2 += 1
        elif k == "tick" and r.get("phase") == "live": n_tics += 1
    llam = [r for r in rz if r.get("estado") in ("propone", "intraducible", "calla", "error")]
    retr = [r["tics_de_vuelta"] for r in llam if r.get("tics_de_vuelta") is not None]
    preg = {r["tick_pregunta"]: r for r in rz if r.get("estado") == "juicio con la instantanea de la pregunta"}
    # la llegada: el veredicto de la puerta a la propuesta vuelta en ese tic (forma_evaluada con tick >= tick de vuelta, la primera)
    ya_rechaza = 0; pasan_pregunta = 0; pasan_llegada = 0; pares = []
    for r in [x for x in rz if x.get("estado") == "propone"]:
        e = next((x for x in ev if x.get("tick", -1) >= r["tick"] and x.get("origen") == "consejero"), None)
        vp = (preg.get(r["tick_pregunta"]) or {}).get("veredicto_pregunta"); vl = e.get("veredicto") if e else None
        pares.append({"tick_pregunta": r["tick_pregunta"], "tick_llegada": r["tick"], "retraso": r["tics_de_vuelta"], "pregunta": vp, "llegada": vl, "tick_veredicto": (e.get("tick") if e else None)})
        pasan_pregunta += (vp == "ok"); pasan_llegada += (vl == "ok"); ya_rechaza += (vp == "ok" and vl != "ok")
    usd = max([r.get("usd_acumulado") or 0.0 for r in rz] + [0.0])
    return {"tics": n_tics, "final": {k: (fin or {}).get(k) for k in ("reason", "placement")}, "resumen26": ({k: res.get(k) for k in ("llamadas", "usd_visto", "no_dispara", "propuestas", "intraducibles", "calla", "errores", "retraso_tics", "aceptadas", "pregunta_ok", "llegan_donde_la_puerta_ya_rechaza", "e2_sustituidos", "planes_del_hermano_recibidos", "malestar_registros", "errores_juez", "lat_tic_max", "lat_tic_mas_de_un_tic")} if res else None),
            "entorno_razonador": ((arr or {}).get("entorno23") or {}).get("razonador"),
            "encargos": sum(1 for r in rz if r.get("estado") == "encargado al proceso"), "no_dispara": sum(1 for r in rz if r.get("estado") == "no dispara"), "llamadas": len(llam), "usd": round(usd, 6),
            "propone": sum(1 for r in llam if r["estado"] == "propone"), "intraducibles": sum(1 for r in llam if r["estado"] == "intraducible"), "calla": sum(1 for r in llam if r["estado"] == "calla"), "errores": [r.get("error") for r in llam if r["estado"] == "error"],
            "retraso_tics": {"n": len(retr), "mediana": q(retr, 0.5), "p95": q(retr, 0.95), "max": (max(retr) if retr else None)}, "ms_llamada_mediana": q([r.get("ms_llamada") for r in llam], 0.5),
            "escena_largo_mediana": q([r.get("escena_largo") for r in rz if r.get("escena_largo")], 0.5),
            "pasan_pregunta": pasan_pregunta, "pasan_llegada": pasan_llegada, "llegan_donde_la_puerta_ya_rechaza": ya_rechaza, "pares_pregunta_llegada": pares,
            "aceptadas": len(ac), "evaluadas": dict(collections.Counter(e.get("veredicto") for e in ev)), "e2_dichos": e2, "e2_sustituidos": sum(1 for r in pl if r.get("estado", "").startswith("mensaje del plan dicho")),
            "planes_del_hermano_recibidos": sum(1 for r in pl if r.get("estado") == "plan del hermano recibido"), "mensajes_plan": [r.get("texto") for r in pl if r.get("estado", "").startswith("mensaje del plan dicho")],
            "malestar": [{"id": m["id"], "estado": m["estado"], "motivo": m.get("motivo"), "tramos": m["tramos"]} for m in ma]}


if __name__ == "__main__":
    OUT = {"nota": __doc__.split("\n")[0], "brazos": {}}
    for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
        V = []
        for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
            for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
                sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)); v = vida(f); v["carp"] = os.path.basename(carp); v["slot"] = sl; V.append(v)
                print(f"  {v['carp']} s{sl}: tics {v['tics']} · llamadas {v['llamadas']} · usd {v['usd']} · retraso {v['retraso_tics']} · propone {v['propone']} intr {v['intraducibles']} · aceptadas {v['aceptadas']} · ya rechaza {v['llegan_donde_la_puerta_ya_rechaza']} · e2 sust {v['e2_sustituidos']} · plan hermano {v['planes_del_hermano_recibidos']} · malestar {len(v['malestar'])}", flush=True)
        # por partida
        por_partida = {}
        for v in V:
            p = por_partida.setdefault(v["carp"], {"llamadas": 0, "usd": 0.0, "propone": 0, "intraducibles": 0, "aceptadas": 0, "ya_rechaza": 0, "e2_sustituidos": 0, "planes_hermano": 0, "retrasos": []})
            p["llamadas"] += v["llamadas"]; p["usd"] += v["usd"]; p["propone"] += v["propone"]; p["intraducibles"] += v["intraducibles"]; p["aceptadas"] += v["aceptadas"]; p["ya_rechaza"] += v["llegan_donde_la_puerta_ya_rechaza"]; p["e2_sustituidos"] += v["e2_sustituidos"]; p["planes_hermano"] += v["planes_del_hermano_recibidos"]
        retr = [x for v in V for x in [r["retraso"] for r in v["pares_pregunta_llegada"]]]
        tot = {"vidas": len(V), "partidas": len(por_partida), "llamadas": sum(v["llamadas"] for v in V), "usd": round(sum(v["usd"] for v in V), 6), "usd_por_llamada": (round(sum(v["usd"] for v in V) / max(1, sum(v["llamadas"] for v in V)), 5)),
               "llamadas_por_vida": round(st.mean(v["llamadas"] for v in V), 1) if V else None, "retraso_tics": {"n": len(retr), "mediana": q(retr, 0.5), "p95": q(retr, 0.95)}, "propone": sum(v["propone"] for v in V), "intraducibles": sum(v["intraducibles"] for v in V), "calla": sum(v["calla"] for v in V),
               "errores": [e for v in V for e in v["errores"]][:5], "pasan_pregunta": sum(v["pasan_pregunta"] for v in V), "pasan_llegada": sum(v["pasan_llegada"] for v in V), "llegan_donde_la_puerta_ya_rechaza": sum(v["llegan_donde_la_puerta_ya_rechaza"] for v in V),
               "aceptadas": sum(v["aceptadas"] for v in V), "e2_sustituidos": sum(v["e2_sustituidos"] for v in V), "planes_del_hermano_recibidos": sum(v["planes_del_hermano_recibidos"] for v in V), "malestar_registros": sum(len(v["malestar"]) for v in V)}
        OUT["brazos"][etiq] = {"total": tot, "por_partida": por_partida, "vidas": V}
        print(f"### {etiq}: {json.dumps(tot, ensure_ascii=False)}")
    json.dump(OUT, open(os.path.join(AQUI, "P6_26_humo.json"), "w"), ensure_ascii=False, indent=1)
    print("-> P6_26_humo.json")
