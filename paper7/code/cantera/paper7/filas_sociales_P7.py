"""[P7 filas sociales] SOLO LECTURA: en los diarios de los ocho campos del siete (P7-30, 34, 45, 50, 56, 61, 65, 67), ¿murió alguna vez una hermana y se encendió el duelo en la otra?
Por cada diario (asiento 10 y 11; el .art.log o, si no está, el .zip leído en memoria): el primer tic vivo con `pareja_muerta` = true estando ella viva (hp > 0).
Apunta: el tic, su vida, `RADIOGRAFIA.ahora.duelo`, la fuerza M de S-MUERTE-PAREJA a 0, 1, 5, 10, 20, 30 y 60 s, el último segundo en que la fila aparece, si es la fila más fuerte en ese tic,
y lo elegido (`RADIOGRAFIA.elegido`) en los 10 s antes y los 10 s después (descriptivo: sin grupo de control). No toca ningún otro archivo.
  python3 filas_sociales_P7.py -> P7_filas_sociales.json"""
import collections, glob, json, os, sys, zipfile
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "paintball", "runs")
CAMPOS = {"P7-30": "P730_", "P7-34": "P734_", "P7-45": "P741_", "P7-50": "P750_", "P7-56": "P756_", "P7-61": "P757_", "P7-65": "P765_", "P7-67": "P767F_"}
TPS = 24; VENT = 240; MARCAS = (0, 1, 5, 10, 20, 30, 60)
SOCIALES = ("S-MUERTE-PAREJA", "S-DANO-PAREJA", "S-VINCULO", "S-HERIDO")      # tics vivos en que la fila aparece en RADIOGRAFIA.ahora.filas (la foto de ahora); aparte, las fotos de candidatos que el diario guarda en algunos tics


def lineas(carp, sl):
    a = glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log"))
    if a: return open(a[0], "rb")
    z = glob.glob(os.path.join(carp, f"*policy_agent_{sl}.zip"))
    if not z: return None
    zf = zipfile.ZipFile(z[0]); nm = [x for x in zf.namelist() if x.endswith(".log")]
    return zf.open(nm[0]) if nm else None


def una(arg):
    campo, carp, sl = arg
    f = lineas(carp, sl)
    if f is None: return {"campo": campo, "partida": os.path.basename(carp), "asiento": sl, "sin_diario": True}
    antes = collections.deque(maxlen=VENT); t0 = None; out = None; despues = []; serie_M = {}; ultimo = None; vivos = 0; cuenta = {k: 0 for k in SOCIALES}; cuenta_fotos = {k: 0 for k in SOCIALES}; vinculo = []
    for line in f:
        if not line.startswith(b'{"k":"tick"') or b'"phase":"live"' not in line: continue
        vivos += 1
        ia = line.find(b'"ahora":'); ja = line.find(b'"W":', ia) if ia >= 0 else -1
        ahora_txt = line[ia:ja] if ia >= 0 else b""; fotos_txt = line[:ia] if ia >= 0 else line
        for k in SOCIALES:
            kb = b'"' + k.encode() + b'"'
            if kb in ahora_txt: cuenta[k] += 1
            if kb in fotos_txt: cuenta_fotos[k] += 1
        if b'"S-VINCULO"' in fotos_txt:
            r_ = json.loads(line); ra_ = r_.get("RADIOGRAFIA") or {}
            cands = [c for c, v in ra_.items() if isinstance(v, dict) for c2, v2 in v.items() if isinstance(v2, dict) and "S-VINCULO" in (v2.get("filas") or {}) for c in [c2]]
            vinculo.append({"tic": r_["tick"], "candidatos_con_S_VINCULO": cands, "elegido": ra_.get("elegido"), "pareja_muerta": r_.get("pareja_muerta")})
        if t0 is None and b'"pareja_muerta":true' not in line:
            antes.append(line); continue
        r = json.loads(line); ra = r.get("RADIOGRAFIA") or {}; ah = ra.get("ahora") or {}; filas = ah.get("filas") or {}
        if t0 is None:
            if not r.get("pareja_muerta") or float(r.get("hp") or 0) <= 0: antes.append(line); continue
            t0 = r["tick"]
            mx = max(filas.items(), key=lambda x: float(x[1].get("M") or 0))[0] if filas else None
            el_antes = collections.Counter((json.loads(l).get("RADIOGRAFIA") or {}).get("elegido") for l in antes)
            out = {"campo": campo, "partida": os.path.basename(carp), "asiento": sl, "tic_muerte_vista": t0, "vida": r.get("hp"), "duelo": ah.get("duelo"),
                   "fila_mas_fuerte": mx, "S_MUERTE_PAREJA_en_t0": (filas.get("S-MUERTE-PAREJA") or {}).get("M"), "elegido_antes_10s": dict(el_antes), "tics_antes": len(antes)}
        dt = (r["tick"] - t0) / TPS
        m = (filas.get("S-MUERTE-PAREJA") or {}).get("M")
        if m is not None: ultimo = dt
        for s in MARCAS:
            if s not in serie_M and dt >= s: serie_M[s] = m
        if r["tick"] - t0 < VENT: despues.append(ra.get("elegido"))
        if float(r.get("hp") or 0) <= 0: break
    base = {"tics_vivos": vivos, "tics_con_fila": cuenta, "tics_con_fila_en_fotos_de_candidatos": cuenta_fotos, "S_VINCULO_en_fotos": vinculo}
    if out is None: return dict({"campo": campo, "partida": os.path.basename(carp), "asiento": sl, "duelo_visto": False}, **base)
    out.update(base)
    out.update({"duelo_visto": True, "M_por_segundo": {str(k): v for k, v in serie_M.items()}, "ultimo_segundo_con_fila": ultimo, "elegido_despues_10s": dict(collections.Counter(despues)),
                "tics_despues": len(despues)})
    return out


if __name__ == "__main__":
    tareas = [(c, d, sl) for c, p in CAMPOS.items() for d in sorted(glob.glob(os.path.join(RUNS, p + "*"))) if os.path.isdir(d) and not d.endswith("_apartada1") for sl in (10, 11)]
    with Pool(8) as P: R = P.map(una, tareas, chunksize=8)
    resumen = {}
    for c in CAMPOS:
        xs = [x for x in R if x["campo"] == c]
        resumen[c] = {"diarios": len(xs), "sin_diario": sum(1 for x in xs if x.get("sin_diario")), "con_duelo": sum(1 for x in xs if x.get("duelo_visto")),
                      "tics_vivos": sum(x.get("tics_vivos", 0) for x in xs), "tics_con_fila": {k: sum((x.get("tics_con_fila") or {}).get(k, 0) for x in xs) for k in SOCIALES},
                      "diarios_con_fila": {k: sum(1 for x in xs if (x.get("tics_con_fila") or {}).get(k, 0) > 0) for k in SOCIALES},
                      "tics_con_fila_en_fotos_de_candidatos": {k: sum((x.get("tics_con_fila_en_fotos_de_candidatos") or {}).get(k, 0) for x in xs) for k in SOCIALES}}
    vinc = [dict(v, campo=x["campo"], partida=x["partida"], asiento=x["asiento"]) for x in R for v in (x.get("S_VINCULO_en_fotos") or [])]
    json.dump({"resumen": resumen, "S_VINCULO_en_fotos": vinc, "eventos": [x for x in R if x.get("duelo_visto")], "sin_diario": [x for x in R if x.get("sin_diario")]}, open(os.path.join(AQUI, "P7_filas_sociales.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(resumen, ensure_ascii=False))
