"""[P8] Prompt 94, punto 4 (solo mirar): lo que quita de verdad a la criatura una noche dormida fuera de casa, en el mundo de ahora, frente a lo que dice la cultura
(1,5 de vida por noche: medido en el prompt 52, RG11, normal, semillas 1-3, peligro medio; cultura_valle.py, BESTIA_NOCHE_MEDIDA) y a lo que cree (−0,75 de nacimiento,
con el recuerdo neutro; −0,2 a −0,4 al acabar en RG47r). De las partidas de cierre (RG46r en valle_taller_v46, RG47r en valle_taller_v48; 21 semillas, 40 días):
por criatura y noche en que durmió fuera al menos la mitad de los turnos de noche (como la apunta la criatura), la vida que le quitó la bestia esa noche (golpes ×
golpe de la bestia) y la comida que le robó; y la media por noche. Y lo mismo con las noches dormidas en casa.
   python3 verdad_noche_v49.py -> por pantalla"""
import gzip, json, os, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
CFG = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8")); GOLPE = CFG["bestia"]["golpe_dano"]; DIA = CFG["dia"]["turnos"]
CASA = set()
for c in CFG["mapa"]["casas"]:
    for dx in range(3):
        for dy in range(3): CASA.add((c["x0"] + dx, c["y0"] + dy))
CARP = {"RG46r": "/Volumes/Mem G-EMV/valle_taller_v46", "RG47r": "/Volumes/Mem G-EMV/valle_taller_v48"}; MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian")

def una(arg):
    v, mu, s = arg; N = defaultdict(lambda: {"noche": 0, "dorm_fuera": 0, "dorm_casa": 0, "golpes": 0, "roba": 0})
    for l in gzip.open(os.path.join(CARP[v], f"{v}_{mu}+sabores_s{s}_d40", "mundo.jsonl.gz"), "rt"):
        x = json.loads(l)
        if x["fase"] != "noche": continue
        d = x["turno"] // DIA
        for a, g in x["agentes"].items():
            if g["cuerpo"]["muerta"]: continue
            r = N[(a, d)]; r["noche"] += 1
            if g["cuerpo"].get("dormida"): r["dorm_casa" if tuple(g["pos"]) in CASA else "dorm_fuera"] += 1
        for e in x["eventos"]:
            if "bestia_pega" in e: N[(e["bestia_pega"], d)]["golpes"] += 1
            if "bestia_roba" in e: N[(e["bestia_roba"], d)]["roba"] += len(e.get("que") or [])
    out = Counter()
    for r in N.values():
        tot = r["dorm_fuera"] + r["dorm_casa"]
        if not tot or tot * 2 < r["noche"]: continue                       # una noche dormida (la mitad o más)
        k = "fuera" if r["dorm_fuera"] >= r["dorm_casa"] else "casa"
        out[k + "_noches"] += 1; out[k + "_vida"] += r["golpes"] * GOLPE; out[k + "_robo"] += r["roba"]; out[k + "_con_golpe"] += r["golpes"] > 0
    return {"v": v, "mu": mu, "C": dict(out)}


if __name__ == "__main__":
    with Pool(8) as p: R = p.map(una, [(v, mu, s) for v in CARP for mu in MUNDOS for s in range(1001, 1022)])
    print("| mundo | clase | noches dormidas fuera | vida que le quita la bestia por noche fuera (media) | noches fuera con algún golpe | comida robada por noche fuera | noches en casa: vida quitada por noche |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in CARP:
            C = sum((Counter(r["C"]) for r in R if r["v"] == v and r["mu"] == mu), Counter()); n = C["fuera_noches"] or 1; nc = C["casa_noches"] or 1
            print(f"| {mu} | {v} | {C['fuera_noches']} | {C['fuera_vida'] / n:.2f} | {100 * C['fuera_con_golpe'] / n:.1f} % | {C['fuera_robo'] / n:.2f} | {C['casa_vida'] / nc:.2f} |")
