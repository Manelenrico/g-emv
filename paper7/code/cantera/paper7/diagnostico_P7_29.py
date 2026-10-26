"""[P7-29, seccion 0: antes de arreglar] POR QUE EL MAPA DEL CUERPO "NO TENIA" LOS MUROS DE LAS RACHAS BLOQUEADAS DE P7-24 (pregunta de Manel, 8-oct). Coste cero.
Lee los 240 diarios del campo y escribe P7_29_diagnostico.json:
  1. rachas: cada racha de 3 o mas pasos seguidos `blocked` desde la misma casilla y en la misma direccion (la regla del arreglo 2): que hay en la casilla destino
     segun el `static_map` del propio diario ('.', '#', 'R', 'F', 'B'), si hay un agente a la vista encima, y lo elegido por el cuerpo al empezar la racha;
     ademas, las ocho orientaciones del mapa (identidad, transpuesta, volteos, giros) por si el cuerpo lo leyera girado.
  2. latencia: por vida, el tiempo de decision por tic (`RADIOGRAFIA.ms`), la fraccion de tics por encima del tic (41,67 ms), la fraccion de desplazamientos
     que siguen la propia intencion del tic anterior (`intencion.dir` -> pos(t) - pos(t-1)), y la fraccion de pasos listos bloqueados.
  3. mapa: cuantos mapas distintos hay en el campo y si los tres brazos de una misma semilla reciben el mismo.
  python3 diagnostico_P7_29.py"""
import collections, glob, hashlib, json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); TIC_MS = 1000.0 / 24
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}
GIROS = {"identidad": lambda x, y: (x, y), "transpuesta": lambda x, y: (y, x), "volteo_x": lambda x, y: (47 - x, y), "volteo_y": lambda x, y: (x, 47 - y), "giro_180": lambda x, y: (47 - x, 47 - y), "transpuesta_volteo_x": lambda x, y: (47 - y, x), "transpuesta_volteo_y": lambda x, y: (y, 47 - x), "antitranspuesta": lambda x, y: (47 - y, 47 - x)}


def lee(f):
    sm = None; T = []
    for line in open(f, errors="replace"):
        if '"tick"' not in line and '"static_map"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "static_map" and sm is None: sm = r["filas"]
        elif k == "tick" and r.get("phase") == "live":
            R = r.get("RADIOGRAFIA") or {}
            T.append({"t": r["tick"], "pos": tuple(r["pos"]), "res": r.get("action_result"), "listo": (r.get("move_ready_in") or 0) == 0, "int": (r.get("intencion") or {}), "el": str(R.get("elegido") or ""), "ms": R.get("ms"),
                      "agentes": [tuple(a.get("pos") or ()) for a in (r.get("ve_agentes") or []) if a.get("pos")], "zc": ((r.get("zona") or {}).get("center")), "zr": ((r.get("zona") or {}).get("radius"))})
    return sm, T


if __name__ == "__main__":
    rachas = []; lat = []; mapas = collections.defaultdict(set)
    for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P724_s*_d*_*", "*agent_1[01].art.log"))):
        b = os.path.basename(os.path.dirname(f)).split("_"); vida = {"serie": int(b[1][1:]), "dia": int(b[2][1:]), "brazo": b[3], "asiento": int(f[-10:-8])}
        sm, T = lee(f)
        if len(T) < 100: continue
        if sm: mapas[(vida["serie"], vida["dia"])].add(hashlib.md5(json.dumps(sm).encode()).hexdigest()[:8])
        # 1. rachas
        racha = None
        for i in range(1, len(T)):
            p, q = T[i - 1], T[i]
            if q["res"] == "blocked" and p["int"].get("do") == "move" and q["listo"]:
                d = p["int"].get("dir"); dx, dy = DIRS.get(d, (0, 0)); tgt = (p["pos"][0] + dx, p["pos"][1] + dy); clave = (p["pos"], d)
                if racha and racha["clave"] == clave: racha["n"] += 1
                else:
                    if racha and racha["n"] >= 3: rachas.append(racha)
                    ch = {g: (sm[gy][gx] if (sm and 0 <= gx < 48 and 0 <= gy < 48) else "fuera") for g, fn in GIROS.items() for gx, gy in [fn(*tgt)]} if sm else {}
                    racha = {"clave": clave, **vida, "t": p["t"], "pos": list(p["pos"]), "dir": d, "casilla": list(tgt), "casilla_char": ch.get("identidad", "?"), "giros": ch, "agente_a_la_vista": tgt in p["agentes"], "elegido": p["el"], "n": 1,
                             "dist_centro": (round(math.dist(p["pos"], p["zc"]), 1) if p["zc"] else None), "radio": p["zr"]}
            elif q["res"] != "blocked":
                if racha and racha["n"] >= 3: rachas.append(racha)
                racha = None
        if racha and racha["n"] >= 3: rachas.append(racha)
        # 2. latencia y desplazamientos propios
        ms = [float(t["ms"]) for t in T if t["ms"] is not None]; n = ok = 0
        for i in range(1, len(T)):
            dp = (T[i]["pos"][0] - T[i - 1]["pos"][0], T[i]["pos"][1] - T[i - 1]["pos"][1])
            if dp == (0, 0): continue
            n += 1; it = T[i - 1]["int"]
            if it.get("do") == "move" and DIRS.get(it.get("dir")) == dp: ok += 1
        listos = sum(1 for t in T if t["listo"]); bl = sum(1 for t in T if t["listo"] and t["res"] == "blocked")
        lat.append({**vida, "tics": len(T), "ms_mediana": (round(st.median(ms), 2) if ms else None), "ms_p90": (round(sorted(ms)[int(0.9 * len(ms))], 2) if ms else None), "ms_max": (round(max(ms), 2) if ms else None), "sobre_el_tic": (round(sum(1 for m in ms if m > TIC_MS) / len(ms), 4) if ms else None),
                    "desplazamientos": n, "propios": (round(ok / n, 4) if n else None), "paso_listo": listos, "bloqueados": bl, "bloqueo": round(bl / max(1, listos), 4)})
    for r in rachas: r.pop("clave", None)
    R3 = rachas
    res = {"rachas": {"n": len(R3), "tics": sum(r["n"] for r in R3), "casilla_destino": dict(collections.Counter(f"{r['casilla_char']} · {'agente a la vista' if r['agente_a_la_vista'] else 'nadie a la vista'}" for r in R3)),
                      "tics_por_casilla_destino": dict(collections.Counter(f"{r['casilla_char']} · {'agente a la vista' if r['agente_a_la_vista'] else 'nadie a la vista'}" for r in R3 for _ in range(r["n"]))),
                      "por_brazo": {b: {"rachas": sum(1 for r in R3 if r["brazo"] == b), "tics": sum(r["n"] for r in R3 if r["brazo"] == b)} for b in ("APRENDE", "BORRADO", "TECHO")},
                      "elegido_con_agente_tics": dict(collections.Counter(r["elegido"] for r in R3 if r["agente_a_la_vista"] for _ in range(r["n"])).most_common(8)), "elegido_sin_agente_tics": dict(collections.Counter(r["elegido"] for r in R3 if not r["agente_a_la_vista"] for _ in range(r["n"])).most_common(8)),
                      "giros_sin_agente_tics": {g: dict(collections.Counter(r["giros"].get(g, "?") for r in R3 if not r["agente_a_la_vista"] for _ in range(r["n"]))) for g in GIROS},
                      "mas_largas": sorted(R3, key=lambda r: -r["n"])[:12]},
           "latencia": {"por_vida": lat, "por_brazo_y_bloque": {}},
           "mapa": {"semillas": len(mapas), "semillas_con_un_solo_mapa_entre_brazos": sum(1 for v in mapas.values() if len(v) == 1), "mapas_distintos": len({x for v in mapas.values() for x in v})}}
    for b in ("APRENDE", "BORRADO", "TECHO"):
        for nb, ds in (("dias 1-5", range(1, 6)), ("dias 6-10", range(6, 11)), ("dias 11-15", range(11, 16)), ("dias 16-20", range(16, 21))):
            vs = [x for x in lat if x["brazo"] == b and x["dia"] in ds]
            res["latencia"]["por_brazo_y_bloque"][f"{b} · {nb}"] = {"vidas": len(vs), "ms_mediana_media": round(st.mean(x["ms_mediana"] for x in vs), 2), "sobre_el_tic_media": round(st.mean(x["sobre_el_tic"] for x in vs), 4), "propios_media": round(st.mean(x["propios"] for x in vs if x["propios"] is not None), 4), "bloqueo_media": round(st.mean(x["bloqueo"] for x in vs), 4),
                                                                   "vidas_con_mas_del_20_por_ciento_sobre_el_tic": sum(1 for x in vs if x["sobre_el_tic"] > 0.2)}
    # correlacion de rangos entre "sobre el tic" y "bloqueo" en APRENDE
    ap = [x for x in lat if x["brazo"] == "APRENDE"]
    def rangos(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
        for k, i in enumerate(o): r[i] = k
        return r
    a_ = rangos([x["sobre_el_tic"] for x in ap]); b_ = rangos([x["bloqueo"] for x in ap]); n_ = len(ap)
    res["latencia"]["spearman_APRENDE_sobre_el_tic_vs_bloqueo"] = round(1 - 6 * sum((i - j) ** 2 for i, j in zip(a_, b_)) / (n_ * (n_ ** 2 - 1)), 3) if n_ > 2 else None
    json.dump(res, open(os.path.join(AQUI, "P7_29_diagnostico.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in res["rachas"].items() if k != "mas_largas"}, ensure_ascii=False)[:1500]); print(json.dumps(res["latencia"]["por_brazo_y_bloque"], ensure_ascii=False)[:1500]); print(res["mapa"], "spearman", res["latencia"]["spearman_APRENDE_sobre_el_tic_vs_bloqueo"])
