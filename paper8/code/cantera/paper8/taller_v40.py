"""[P8] Prompt 85: las partidas de RG40r con el mundo de los sabores (objetos.sabores encendido: «sequia+sabores», «normal+sabores»), con taller_v35 (el
lanzador del experimento y el radar al acabar); y la puerta: con los sabores encendidos, el tonto y el recolector hacen lo mismo (su registro, sin la marca
de origen, igual al del mundo sin sabores), y con el mundo sin sabores RG39r sale igual que en el prompt 84.
   python3 taller_v40.py partidas [procesos] | puerta"""
import gzip, json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import lanzador as L
import taller_v35 as T35
_md = L.mundo_de
def mundo_de(nombre):
    if nombre.endswith("+sabores"):
        m = dict(_md(nombre[:-len("+sabores")])); m["objetos"] = {"sabores": {"activo": True}}; return m
    return _md(nombre)
L.mundo_de = mundo_de
def limpia(texto):
    out = []
    for l in texto.splitlines():
        x = json.loads(l)
        for g in x["agentes"].values(): g.pop("origen", None)
        out.append(json.dumps(x, sort_keys=True))
    return out
def puerta(arg):
    v, mu, s = arg; tmp = os.path.join(L.T7, "valle_prueba_v40"); os.makedirs(tmp, exist_ok=True); L.una((v, mu, s, 40, tmp))
    a = gzip.open(os.path.join(tmp, f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz"), "rt", encoding="utf-8").read()
    if mu.endswith("+sabores"):
        b = gzip.open(os.path.join(L.T7, "valle_experimento", f"{v}_{mu[:-8]}_s{s}_d40", "mundo.jsonl.gz"), "rt", encoding="utf-8").read(); return {"clase": v, "mundo": mu, "igual_sin_la_marca": limpia(a) == limpia(b)}
    b = gzip.open(os.path.join(L.T7, "valle_taller_v35", f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz"), "rt", encoding="utf-8").read(); return {"clase": v, "mundo": mu, "registro_identico": a == b}


if __name__ == "__main__":
    if sys.argv[1] == "puerta":
        with Pool(3) as p: out = p.map(puerta, [("tonto", "normal+sabores", 1001), ("recolector", "normal+sabores", 1001), ("RG39r", "normal", 1001)])
        print(json.dumps(out, ensure_ascii=False)); json.dump(out, open(os.path.join(AQUI, "salida", "puerta_v40.json"), "w"), ensure_ascii=False, indent=1)
    else:
        npro = int(sys.argv[2]) if len(sys.argv) > 2 else 7; os.makedirs(T35.CARPETA, exist_ok=True)
        T = [("RG40r", mu, s) for mu in ("sequia+sabores", "normal+sabores") for s in T35.SEM]
        with Pool(npro) as p:
            for r in p.imap_unordered(T35.partida, T): print(json.dumps(r, ensure_ascii=False), flush=True)
