"""[P8] Prompt 89: echar y matar separadas y encendidas en todos los mundos (config), la foto de RG44r con sus hechos, y el mundo de estrés «bestias_crian»
(la bestia de día más una cría cada 20 días, hasta dos; en el lanzador), con el lanzador del experimento.
   python3 taller_v44.py puerta                                   -> salida/puerta_v44.json
       el tonto y el recolector salen como en el experimento (sin la lista «bestias» del registro, que es nueva); RG43r, como en el prompt 88 (normal+sabores con
       echar y matar, 1001: aquella partida no tuvo ni empujones ni golpes a la bestia, así que separar las ruedas no la cambia)
   python3 taller_v44.py partidas <clases> <mundos> [semillas=1001-1021] [procesos=7]   -> /Volumes/Mem G-EMV/valle_taller_v44/"""
import gzip, json, os, sys
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":               # que el Mac no se duerma mientras juega (como el lanzador)
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import lanzador as L
import taller_v40                                                        # el mundo «+sabores»
import taller_v43 as T43                                                 # pieza_g.json al acabar
CARPETA = os.path.join(L.T7, "valle_taller_v44")

def lineas(ruta, quita=("bestias",)):
    out = []
    for l in gzip.open(ruta, "rt", encoding="utf-8"):
        x = json.loads(l)
        for k in quita: x.pop(k, None)
        out.append(x)
    return out

def puerta(arg):
    v, mu, s, origen, mu0 = arg; tmp = os.path.join(L.T7, "valle_prueba_v44"); os.makedirs(tmp, exist_ok=True); L.una((v, mu, s, 40, tmp))
    a = lineas(os.path.join(tmp, f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz")); b = lineas(os.path.join(L.T7, origen, f"{v}_{mu0}_s{s}_d40", "mundo.jsonl.gz"))
    return {"clase": v, "mundo": mu, "frente_a": f"{origen}/{v}_{mu0}", "semilla": s, "registro_identico_sin_bestias": a == b}


if __name__ == "__main__":
    if sys.argv[1] == "puerta":
        G_ = [("tonto", "normal", 1001, "valle_experimento", "normal"), ("recolector", "sequia", 1001, "valle_experimento", "sequia"),
              ("RG43r", "normal+sabores", 1001, "valle_taller_v43", "normal+sabores+G=echar.matar")]
        with Pool(3) as p: out = p.map(puerta, G_)
        print(json.dumps(out, ensure_ascii=False)); json.dump(out, open(os.path.join(AQUI, "salida", "puerta_v44.json"), "w"), ensure_ascii=False, indent=1)
    elif sys.argv[1] == "partidas":
        VS = sys.argv[2].split(","); MS = sys.argv[3].split(","); a_, b_ = (sys.argv[4] if len(sys.argv) > 4 else "1001-1021").split("-"); npro = int(sys.argv[5]) if len(sys.argv) > 5 else 7
        os.makedirs(CARPETA, exist_ok=True)
        T = [(v, mu, s, 40, CARPETA) for mu in MS for v in VS for s in range(int(a_), int(b_) + 1)]
        with Pool(npro) as p:
            for r in p.imap_unordered(T43.una, T): print(json.dumps({k: r[k] for k in ("id", "saltada") if k in r}, ensure_ascii=False), flush=True)
