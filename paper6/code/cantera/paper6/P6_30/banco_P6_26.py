# [P6-30] [P6-30] COPIA de cantera/paper6/banco_P6_26.py con tres cambios declarados: RAIZ un nivel mas arriba (la copia vive en paper6/P6_30), cantera/paper6 en sys.path, y un proceso por vida (maxtasksperchild=1) en el pool que replica el cuerpo. Nada mas cambia.
"""[P6-26 · 1] BANCO SIN LENGUAJE, COSTE CERO: ¿existe un plan que pase? En las escenas de P6-25 donde
la puerta6 rechazo la primera propuesta (de Haiku y de Sonnet, por separado), se prueban TODOS los planes
del espacio del oraculo: cada destino alcanzable que sigue a salvo al llegar (`Oraculo.seguras`, la misma
lista de la que el oraculo elige), con el plan de ir y quedarse de A7h (`policy_pareja23.texto_quedarse`,
tramos 50/50/resto, H = lo que queda de fase al llegar) y sus puntos de control, juzgado por la puerta6
real sobre LA MISMA instantanea de la pregunta (`juez_P6_25.juzga_lote`, proceso aparte).
Y en las escenas de pareja donde solo una de las dos puertas acepto: el mismo barrido para los dos
hermanos, para saber si hay un plan que acepten las dos (cada uno el suyo; y una zona comun: destinos
aceptados por los dos a 3 casillas o menos, Chebyshev).

    python3 banco_P6_26.py [--hilos 4]    -> P6_26_banco.json (los juicios, destino a destino, en P6_26_banco_juicios.json)
"""
from __future__ import annotations
import collections, json, math, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI))); sys.path.insert(0, AQUI); sys.path.insert(1, os.path.join(RAIZ, "cantera", "paper6"))  # [P6-30]
import juez_P6_25 as JZ                                         # noqa: E402  (entorno de A7h, puerta6 real, instantaneas)
import policy_pareja23 as P23                                   # noqa: E402
import traductor_forma as TF                                    # noqa: E402
import oraculo_P6_14 as O                                       # noqa: E402
VERSION = "banco_P6_26 (P6-26): todos los destinos seguros del oraculo, plan ir-y-quedarse, puerta6 real sobre la instantanea de P6-25"


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def espacio(snap_path, escena, filas):
    """Los planes del espacio del oraculo en esa instantanea: [(destino, pasos, llegada, H, tramos)]."""
    job = JZ.carga_snap(snap_path); obs = job["obs"]; mundo = job["mundo"]; t = job["tick"]
    sp = int(((obs.get("you") or {}).get("stats") or {}).get("speed") or 5)
    orac = O.Oraculo(mundo, sp); pos = tuple(int(x) for x in (obs.get("you") or {}).get("pos"))
    Dm = orac.bfs(pos); seg = orac.seguras(pos, t, Dm)
    i = orac.fase_activa(t); fin = orac.fases[i + 1][0] if (i is not None and i + 1 < len(orac.fases)) else t + 400
    out = []
    for q, k in sorted(seg, key=lambda x: (x[1], x[0])):
        llegada = t + k * orac.coste; H = max(25, min(400, fin - llegada))
        texto = P23.texto_quedarse(q, H)
        formas, _inf = TF.traduce(texto, escena["escena_traductor"], filas)
        if not formas:
            continue
        out.append({"destino": list(q), "pasos": k, "llegada": llegada, "H": H, "tramos": TF.solo_tramos(formas[0])})
    return out, {"pos": list(pos), "n_seguras": len(seg), "n_alcanzables": len(Dm), "fin_fase": fin, "coste_paso": orac.coste}


def _barre(args):
    snap, esc, filas, etiq = args
    try:
        planes, info = espacio(snap, esc, filas)
        js = JZ.juzga_lote(snap, [{"id": f"{etiq}|{p['destino'][0]},{p['destino'][1]}", "modelo": "espacio", "tramos": p["tramos"], "etiqueta": etiq} for p in planes])
        for p, j in zip(planes, js):
            j["destino_plan"] = p["destino"]; j["pasos"] = p["pasos"]; j["H"] = p["H"]
            j.pop("curva", None); j["contra"] = (j.get("contra") or [])[:3]
        return {"id": etiq, "snap": snap, "info": info, "juicios": js}
    except Exception as ex:
        import traceback
        return {"id": etiq, "snap": snap, "error": repr(ex)[:300], "traza": traceback.format_exc()[-800:], "juicios": []}


if __name__ == "__main__":
    import multiprocessing as mp
    a = sys.argv; hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 4
    E = json.load(open(os.path.join(AQUI, "P6_25_escenas.json"))); esc = {f"{e['carp']}_{e['slot']}_{e['tick']}": e for e in E["escenas"]}
    JP = json.load(open(os.path.join(AQUI, "P6_25_juicios_primera.json")))["juicios"]
    JR = json.load(open(os.path.join(AQUI, "P6_25_juicios_pareja.json")))["juicios"]
    PR = json.load(open(os.path.join(AQUI, "P6_25_planes_pareja.json")))["planes"]
    # las escenas rechazadas (primera propuesta, por modelo): veredicto area / vida (con plan)
    rech = {m: sorted({j["id"] for j in JP if j["modelo"] == m and j.get("veredicto") in ("area", "vida")}) for m in ("haiku", "sonnet")}
    # los pares donde solo una puerta acepto (por modelo)
    ver = {(j["id"], j["modelo"]): j.get("veredicto") for j in JR}
    pares = collections.defaultdict(dict)
    for p in PR:
        pares[(p["par"], p["modelo"])][p["id"]] = ver.get((p["id"], p["modelo"]))
    solo_una = {m: sorted(par for (par, mm), dd in pares.items() if mm == m and len(dd) == 2 and sum(1 for v in dd.values() if v == "ok") == 1) for m in ("haiku", "sonnet")}
    ids_pareja = set()
    for m, ps in solo_una.items():
        for par in ps:
            for k in pares[(par, m)]:
                ids_pareja.add(k)
    ids = sorted(set(rech["haiku"]) | set(rech["sonnet"]) | ids_pareja)
    tareas = [(esc[k]["snap"]["0"], esc[k], E["filas"][esc[k]["carp"]], k) for k in ids]
    print(f"### P6-26 banco: rechazadas haiku {len(rech['haiku'])}, sonnet {len(rech['sonnet'])}; pares con una sola puerta: haiku {len(solo_una['haiku'])}, sonnet {len(solo_una['sonnet'])} · instantaneas a barrer {len(tareas)} · {hilos} procesos", flush=True)
    t0 = time.time(); ctx = mp.get_context("spawn")
    with ctx.Pool(hilos) as pool:
        res = pool.map(_barre, tareas, chunksize=1)
    seg = round(time.time() - t0, 1)
    json.dump({"nota": __doc__.split("\n")[0], "version": VERSION, "segundos": seg, "escenas": res}, open(os.path.join(AQUI, "P6_26_banco_juicios.json"), "w"), ensure_ascii=False)
    # ── las medidas ──
    por = {r["id"]: r for r in res}
    def mejor(k):
        r = por.get(k) or {}; ok = [j for j in r.get("juicios", []) if j.get("veredicto") == "ok"]
        return r, ok, (max(ok, key=lambda j: j["ventaja"]) if ok else None)
    def q(xs, p):
        xs = sorted(xs); return (round(xs[min(len(xs) - 1, int(p * len(xs)))], 4) if xs else None)
    P2 = {(p["id"], p["modelo"]): p for p in (json.load(open(os.path.join(AQUI, "P6_25_planes_bucle2.json")))["planes"] if os.path.exists(os.path.join(AQUI, "P6_25_planes_bucle2.json")) else [])}
    P3 = {(p["id"], p["modelo"]): p for p in (json.load(open(os.path.join(AQUI, "P6_25_planes_bucle3.json")))["planes"] if os.path.exists(os.path.join(AQUI, "P6_25_planes_bucle3.json")) else [])}
    P1 = {(p["id"], p["modelo"]): p for p in json.load(open(os.path.join(AQUI, "P6_25_planes_primera.json")))["planes"]}
    def dest_de(p):
        return next((tuple(t["destino"]) for t in (p or {}).get("tramos") or [] if t.get("destino")), None)
    OUT = {"nota": __doc__.split("\n")[0], "version": VERSION, "segundos": seg, "instantaneas_barridas": len(tareas), "errores": [r["id"] for r in res if r.get("error")],
           "planes_por_instantanea": {"mediana": q([len(r.get("juicios", [])) for r in res], 0.5), "max": max(len(r.get("juicios", [])) for r in res)}, "por_modelo": {}, "pareja": {}}
    for m in ("haiku", "sonnet"):
        ks = rech[m]; con = [k for k in ks if mejor(k)[2] is not None]; mejores = [mejor(k)[2]["ventaja"] for k in con]
        d1 = []; d2 = []; d3 = []; d2b = []; d3b = []
        for k in con:
            b = tuple(mejor(k)[2]["destino_plan"]); ok_dest = [tuple(j["destino_plan"]) for j in mejor(k)[1]]
            for P, dd, ddb in ((P1, d1, None), (P2, d2, d2b), (P3, d3, d3b)):
                p = P.get((k, m)); dst = dest_de(p)
                if dst is not None:
                    dd.append(cheb(dst, b))
                    if ddb is not None:
                        ddb.append(min(cheb(dst, o) for o in ok_dest))
        n_ok = [len(mejor(k)[1]) for k in ks]; n_tot = [len((por.get(k) or {}).get("juicios", [])) for k in ks]
        OUT["por_modelo"][m] = {"escenas_rechazadas": len(ks), "con_algun_plan_que_pasa": {"k": len(con), "n": len(ks), "pct": round(100 * len(con) / max(1, len(ks)), 1)},
                                "planes_que_pasan_por_escena": {"mediana": q(n_ok, 0.5), "sobre_probados_mediana_pct": q([100 * a / b for a, b in zip(n_ok, n_tot) if b], 0.5)},
                                "mejor_ganancia": {"mediana": q(mejores, 0.5), "p90": q(mejores, 0.9), "min": (round(min(mejores), 4) if mejores else None), "max": (round(max(mejores), 4) if mejores else None)},
                                "distancia_al_mejor (casillas, Chebyshev)": {"primera": {"mediana": q(d1, 0.5), "n": len(d1)}, "segunda": {"mediana": q(d2, 0.5), "n": len(d2)}, "tercera": {"mediana": q(d3, 0.5), "n": len(d3)}},
                                "distancia_al_plan_que_pasa_mas_cercano": {"segunda": {"mediana": q(d2b, 0.5), "n": len(d2b), "a_0_casillas": sum(1 for x in d2b if x == 0)}, "tercera": {"mediana": q(d3b, 0.5), "n": len(d3b), "a_0_casillas": sum(1 for x in d3b if x == 0)}}}
        # pareja: pares con una sola puerta
        n = 0; ambos = 0; comun = 0; det = []
        for par in solo_una[m]:
            dd = pares[(par, m)]; ka, kb = sorted(dd); ra, oka, _ = mejor(ka); rb, okb, _ = mejor(kb)
            if not ra or not rb:
                continue
            n += 1; ambos += bool(oka and okb)
            da = [tuple(j["destino_plan"]) for j in oka]; db = [tuple(j["destino_plan"]) for j in okb]
            cz = any(cheb(x, y) <= 3 for x in da for y in db); comun += cz
            det.append({"par": par, "acepta_A": len(oka), "acepta_B": len(okb), "zona_comun": cz})
        OUT["pareja"][m] = {"pares_con_una_sola_puerta": len(solo_una[m]), "barridos": n, "los_dos_tienen_plan_que_pasa": {"k": ambos, "n": n, "pct": round(100 * ambos / max(1, n), 1)}, "zona_comun_aceptada_por_los_dos (Chebyshev <= 3)": {"k": comun, "n": n, "pct": round(100 * comun / max(1, n), 1)}, "detalle": det}
    json.dump(OUT, open(os.path.join(AQUI, "P6_26_banco.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in OUT.items() if k != "pareja"}, ensure_ascii=False)[:3000]); print("pareja:", json.dumps({m: {k: v for k, v in x.items() if k != "detalle"} for m, x in OUT["pareja"].items()}, ensure_ascii=False))
    print(f"-> P6_26_banco.json · {seg} s")
