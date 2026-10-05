"""[P6-22 · 1, 2, 5] LOS PASOS QUE NO LLEGAN, brazo por brazo y fase por fase. SOLO LECTURA de
diarios, de uno en uno. La medida es la de P6-21 (`mide_fantasma_P6_21.py`), tal cual:

  · PASO PERDIDO: en t-1 el cuerpo envio un paso (`intencion` move) con las piernas listas
    (`move_ready_in` 0) a una casilla libre (no solida en el mapa estatico, sin cuerpo visto);
    en t la respuesta del juego es `ok`, la casilla no cambia y las piernas siguen listas.
    Porcentaje = perdidos / pasos listos a casilla libre.
  · FANTASMA: en t la respuesta es `cooldown` o `blocked` (solo las produce un paso resuelto
    en t-1) y el cuerpo NO envio un paso en t-1: el juego resolvio un paso enviado antes.
    Retraso minimo = t-1 menos el ultimo tic con paso enviado.
  · RETRASO POR TIC (para el humo): para cada paso DADO (la casilla cambia en una direccion),
    tics desde el ultimo envio de esa direccion desde esa casilla (0 = en el tic).
Por brazo y por fase del anillo (antes del primer aviso; fases 1-4; fases 5-7), y por vida.

    python3 mide_pasos_P6_22.py SALIDA.json 'ETIQUETA=paintball/runs/PATRON_*' ...
"""
import collections, glob, json, math, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}
INV = {v: k for k, v in DIRS.items()}


def fase_de(t, zs):
    if not zs or t < zs[0][0]:
        return "antes del aviso 1"
    return "fases 5-7" if t >= zs[4][0] else "fases 1-4"


def mide_vida(f):
    recs = list(U.lee(f))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    if pc is None:
        del recs; return None
    cat = next(r for r in recs if r["k"] == "catalogo"); sm = next(r for r in recs if r["k"] == "static_map")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); zs = pc.get("zone_schedule") or []
    T = {}
    for r in recs:
        if r.get("k") == "tick" and r.get("phase") == "live":
            T[r["tick"]] = {"pos": (int(r["pos"][0]), int(r["pos"][1])), "int": r.get("intencion") or {}, "mri": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0), "ar": r.get("action_result_obs", r.get("action_result")),
                            "ve": {tuple(a["pos"]) for a in (r.get("ve_agentes") or []) if a.get("pos")}}
    del recs
    ts = sorted(T); K = collections.defaultdict(collections.Counter); RETF = collections.defaultdict(list); RETD = collections.defaultdict(list); ult_paso = None
    for t in ts:
        r = T[t]; fase = fase_de(t, zs); k = K[fase]; k["tics"] += 1
        prev = T.get(t - 1)
        if prev is None:
            if r["int"].get("do") == "move":
                ult_paso = t
            continue
        pm = prev["int"].get("do") == "move" and prev["int"].get("dir") in DIRS
        if r["ar"] in ("cooldown", "blocked") and not pm:
            k["fantasma"] += 1
            if ult_paso is not None:
                RETF[fase].append(t - 1 - ult_paso)
        if pm and prev["mri"] == 0:
            dx, dy = DIRS[prev["int"]["dir"]]; dest = (prev["pos"][0] + dx, prev["pos"][1] + dy)
            if not mundo.solido(dest[0], dest[1]) and dest not in prev["ve"]:
                k["pasos a casilla libre"] += 1
                if r["ar"] == "ok" and r["pos"] == prev["pos"] and r["mri"] == 0:
                    k["perdido"] += 1
                elif r["pos"] == dest:
                    k["dado en el tic"] += 1
        # retraso de cada paso dado
        d = (r["pos"][0] - prev["pos"][0], r["pos"][1] - prev["pos"][1])
        if d in INV:
            dr = INV[d]; kk = None
            for u in range(t - 1, max(ts[0], t - 120) - 1, -1):
                if u in T and T[u]["pos"] == prev["pos"] and T[u]["int"].get("do") == "move" and T[u]["int"].get("dir") == dr:
                    kk = t - 1 - u; break
            RETD[fase].append(kk if kk is not None else -1)
        if r["int"].get("do") == "move":
            ult_paso = t
    return {"K": {f: dict(c) for f, c in K.items()}, "RETF": dict(RETF), "RETD": dict(RETD), "tics": len(ts), "mt": (ts[-1] if ts else 0)}


def q(xs):
    v = sorted(x for x in xs if x >= 0); n = len(v)
    if not n:
        return {"n": 0}
    return {"n": n, "mediana": v[n // 2], "p90": v[int(0.9 * n)], "max": v[-1], "0": sum(1 for x in v if x == 0), "1-2": sum(1 for x in v if 1 <= x <= 2), ">=3": sum(1 for x in v if x >= 3), ">=10": sum(1 for x in v if x >= 10)}


salida = sys.argv[1]; R = {"nota": "P6-22. INSTRUMENTO DE MEDIDA (la medida de P6-21). Por brazo y fase.", "brazos": {}}
for arg in sys.argv[2:]:
    etiq, pat = arg.split("=", 1)
    K = collections.defaultdict(collections.Counter); RETF = collections.defaultdict(list); RETD = collections.defaultdict(list); vidas = []
    carps = sorted(glob.glob(os.path.join(RAIZ, pat)))
    for carp in carps:
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            m = re.search(r"policy_agent_(\d+)\.art\.log$", f); sl = int(m.group(1)) if m else -1
            try:
                v = mide_vida(f)
            except Exception as ex:
                print(f"  ERROR {f}: {ex!r}", flush=True); continue
            if v is None:
                continue
            for fase, c in v["K"].items():
                K[fase].update(c)
            for fase, xs in v["RETF"].items():
                RETF[fase].extend(xs)
            for fase, xs in v["RETD"].items():
                RETD[fase].extend(xs)
            vd = {"carpeta": os.path.basename(carp), "slot": sl, "tics": v["tics"]}
            for fase, c in v["K"].items():
                vd[fase] = {"perdido": c.get("perdido", 0), "libre": c.get("pasos a casilla libre", 0), "fantasma": c.get("fantasma", 0)}
            vidas.append(vd)
        print(f"  {etiq} {os.path.basename(carp)}: vidas {len(vidas)}", flush=True)
    res = {"partidas": len(carps), "vidas": len(vidas), "por_fase": {}}
    for fase in ("antes del aviso 1", "fases 1-4", "fases 5-7"):
        c = K.get(fase, collections.Counter())
        res["por_fase"][fase] = {"tics": c.get("tics", 0), "pasos a casilla libre": c.get("pasos a casilla libre", 0), "dado en el tic": c.get("dado en el tic", 0), "perdido": c.get("perdido", 0),
                                 "pct_perdido": round(100 * c.get("perdido", 0) / max(1, c.get("pasos a casilla libre", 0)), 2), "fantasma": c.get("fantasma", 0), "pct_fantasma_por_tic": round(100 * c.get("fantasma", 0) / max(1, c.get("tics", 0)), 3),
                                 "retraso_minimo_fantasma": q(RETF.get(fase, [])), "retraso_pasos_dados": q(RETD.get(fase, []))}
    res["vidas_con_perdidos_fases_5-7"] = sum(1 for v in vidas if v.get("fases 5-7", {}).get("perdido", 0) > 0)
    res["vidas_lista"] = vidas
    R["brazos"][etiq] = res
    print(f"=== {etiq}: partidas {len(carps)} vidas {len(vidas)}")
    for fase, x in res["por_fase"].items():
        print(f"   {fase}: libres {x['pasos a casilla libre']} · perdidos {x['perdido']} ({x['pct_perdido']} %) · fantasmas {x['fantasma']} · retraso pasos dados {x['retraso_pasos_dados']}")
    json.dump(R, open(salida, "w"), ensure_ascii=False, indent=1)
print("->", salida)
