"""[P7-21, anadido de Manel] EL ESTADO EMOCIONAL DEL CUERPO AL ABRIR CADA CANAL DEL BOTIQUIN. Lectura de los diarios de APRENDE y BORRADO de los dos campos.
Coste cero. Toma los canales de P7_21_vidas.json (tic de apertura) y lee en el diario, en ese tic, `RADIOGRAFIA.ahora.filas` y `d_ahora`.
  python3 emocion_P7_21.py -> P7_21_emocion.json

LO QUE GUARDA EL DIARIO POR INSTANTE (y lo que no): cada fila activa de la tabla con su magnitud `M`, su signo (`-` dolor, `+` lo positivo) y su reparto
en los tres dominios (`F` cuerpo, `R` recursos, `S` vinculo); y la distancia total `d_ahora`. NO distingue, dentro de lo positivo, el alivio de la
atraccion: solo hay un signo. Asi que aqui el "mapa" es: dolor por dominio (suma de las filas con signo -), positivo por dominio (suma de las con +),
y la distancia total.
"""
import collections, glob, json, os
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
V = json.load(open(os.path.join(AQUI, "P7_21_vidas.json")))


def una(k):
    v = V[k]; pref = "P710" if v["campo"] == "P7-10" else "P714b"; brazo = "SUELO" if (v["brazo"] == "ESPERANZA" and pref == "P710") else v["brazo"]
    carp = glob.glob(os.path.join(RAIZ, "paintball", "runs", f"{pref}_s{v['serie']}_d{v['dia']}_{brazo}_*"))[0]; f = glob.glob(os.path.join(carp, f"*policy_agent_{v['slot']}.art.log"))[0]
    quiero = {c["t0"] for c in v["canales"]}; out = {}
    for line in open(f):
        if '"k": "tick"' not in line and '"k":"tick"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") != "tick" or r.get("tick") not in quiero: continue
        a = (r.get("RADIOGRAFIA") or {}).get("ahora") or {}; filas = a.get("filas") or {}
        e = {"dolor": {"F": 0.0, "R": 0.0, "S": 0.0}, "positivo": {"F": 0.0, "R": 0.0, "S": 0.0}, "d": (r.get("RADIOGRAFIA") or {}).get("d_ahora"), "filas": {}}
        for nombre, fila in filas.items():
            lado = "dolor" if fila.get("signo") == "-" else "positivo"
            for dom in ("F", "R", "S"): e[lado][dom] += float(fila.get(dom) or 0.0)
            e["filas"][nombre] = (fila.get("signo"), float(fila.get("M") or 0.0))
        out[r["tick"]] = e
        if len(out) == len(quiero): break
    return k, out


if __name__ == "__main__":
    claves = [k for k, v in V.items() if v["brazo"] in ("APRENDE", "BORRADO") and v["canales"]]
    OUT = {}
    with Pool(4) as P:
        for k, o in P.imap_unordered(una, claves): OUT[k] = o
    json.dump(OUT, open(os.path.join(AQUI, "P7_21_emocion.json"), "w"), ensure_ascii=False)
    print("vidas", len(OUT), "· canales con estado", sum(len(o) for o in OUT.values()), "de", sum(len(V[k]["canales"]) for k in claves))
