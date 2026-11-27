"""[P8] Prompt 97: la tabla de cierre definitiva, con el árbol de fruta dulce encendido en todos los mundos (la bestia pasa por él al atardecer y de noche
sigue a la aldea; el recolector coge su fruta). Las partidas se guardan con los nombres de siempre (sin «+arbol»), en carpetas propias, para que los análisis del
cierre (cierre_v46, diag_v47, diag_robos_v47, verdad_noche_v49, analiza_arbol_v50) sirvan cambiando solo la carpeta. Al acabar cada partida, arbol.json.
   python3 taller_v52.py puerta    -> con el árbol apagado, el tonto y el recolector salen idénticos a los de siempre (salida/puerta_v52.json)
   python3 taller_v52.py pruebas   -> valle_prueba_v52: el tonto, el recolector (normal, 9001-9003) y RG50r (normal, 9001-9002), 40 días, con el árbol
   python3 taller_v52.py cierre    -> valle_taller_v52: RG50r, RG050r (con los sabores), el tonto y el recolector; los cinco mundos; 1001-1021; 40 días"""
import json, os, sys
MODO = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TALLER52_MODO", "cierre")
os.environ["TALLER52_MODO"] = MODO
os.environ["TALLER45_CARPETA"] = {"pruebas": "valle_prueba_v52", "cierre": "valle_taller_v52"}.get(MODO, "valle_prueba_v52")
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import lanzador as L
import taller_v40
import taller_v45 as T
import taller_v44 as T44
_md = taller_v40.mundo_de
def mundo_de(nombre):
    m = dict(_md(nombre))
    if os.environ.get("TALLER52_MODO") in ("pruebas", "cierre"): m["arbol_dulce"] = {"activo": True}      # el árbol, encendido en todos los mundos
    return m
L.mundo_de = mundo_de; taller_v40.mundo_de = mundo_de
MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian")

def una(arg):
    r = T.una(arg); v, mu, s, dias, carpeta = arg; e = L.LOG.get("e")
    if not r.get("saltada") and e is not None and getattr(e, "stats_arbol", None): json.dump(e.stats_arbol, open(os.path.join(carpeta, f"{v}_{mu}_s{s}_d{dias}", "arbol.json"), "w"), ensure_ascii=False)
    return r

def puerta(arg):
    v, mu, s = arg; tmp = os.path.join(L.T7, "valle_prueba_v52_puerta"); os.makedirs(tmp, exist_ok=True); L.una((v, mu, s, 40, tmp))
    a = T44.lineas(os.path.join(tmp, f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz")); b = T44.lineas(os.path.join(L.T7, "valle_experimento", f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz"))
    return {"clase": v, "mundo": mu, "semilla": s, "identico_sin_bestias": a == b}


if __name__ == "__main__":
    if MODO == "puerta":
        with Pool(2) as p: out = p.map(puerta, [("tonto", "normal", 1001), ("recolector", "sequia", 1001)])
        print(json.dumps(out, ensure_ascii=False)); json.dump(out, open(os.path.join(AQUI, "salida", "puerta_v52.json"), "w"), ensure_ascii=False, indent=1)
    else:
        os.makedirs(T.CARPETA, exist_ok=True)
        if MODO == "pruebas":
            TR = [(v, "normal", s, 40, T.CARPETA) for v in ("tonto", "recolector") for s in (9001, 9002, 9003)] + [("RG50r", "normal+sabores", s, 40, T.CARPETA) for s in (9001, 9002)]
        else:
            TR = [(v, mu, s, 40, T.CARPETA) for v in ("tonto", "recolector") for mu in MUNDOS for s in range(1001, 1022)]
            TR += [(v, mu + "+sabores", s, 40, T.CARPETA) for mu in MUNDOS for v in ("RG50r", "RG050r") for s in range(1001, 1022)]
        with Pool(7) as p:
            for r in p.imap_unordered(una, TR): print(json.dumps({k: r[k] for k in ("id", "saltada") if k in r}, ensure_ascii=False), flush=True)
