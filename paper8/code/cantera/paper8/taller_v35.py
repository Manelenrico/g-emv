"""[P8] Prompt 80: las partidas pieza a pieza (sequía y normal, semillas 1001-1021, 40 días; con el lanzador del experimento y, al acabar, el radar de cada
criatura en radar.json, como taller_v34): RG33r (A), RG34r_B (A+B), RG34r_BC (A+B+C), RG34r (A+B+C+D) y las tres con el arreglo de honradez (RG34r_Bh,
RG34r_BCh, RG34rh). Retomable.
   python3 taller_v35.py <clases> [procesos=9] -> /Volumes/Mem G-EMV/valle_taller_v35/"""
import json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import lanzador as L
import taller_v34 as T34
CARPETA = os.path.join(L.T7, "valle_taller_v35"); MUNDOS = tuple((os.environ.get("TALLER_MUNDOS") or "sequia,normal").split(",")); SEM = range(1001, 1022)

def partida(arg):
    v, mu, s = arg; d = os.path.join(CARPETA, f"{v}_{mu}_s{s}_d40")
    if os.path.exists(os.path.join(d, "radar.json")): return {"id": os.path.basename(d), "saltada": True}
    r = L.una((v, mu, s, 40, CARPETA))
    json.dump({a: T34.radar_de(c) for a, c in L.CRI.items()} if all(getattr(c, "_rad", None) for c in L.CRI.values()) else {}, open(os.path.join(d, "radar.json"), "w"), ensure_ascii=False)
    return r


if __name__ == "__main__":
    VS = sys.argv[1].split(","); npro = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    os.makedirs(CARPETA, exist_ok=True)
    T = [(v, mu, s) for v in VS for mu in MUNDOS for s in SEM]
    with Pool(npro) as p:
        for r in p.imap_unordered(partida, T): print(json.dumps(r, ensure_ascii=False), flush=True)
