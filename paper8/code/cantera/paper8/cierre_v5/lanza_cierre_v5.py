"""[P8] Prompt 107: la tabla de cierre v5. RG55r (RG54r sin tope_dar) y RG055r, con los sabores, el árbol encendido en los cinco mundos, semillas 1001-1021, 40 días,
en valle_cierre_v5; RG50r, el tonto y el recolector se reutilizan de la tabla del prompt 97 (valle_taller_v52: las mismas semillas, mundos, días y árbol), tras
comprobar que con el código de ahora salen idénticas. Juega con el lanzador del experimento (lanza_medida_v3.una: el árbol, arbol.json al acabar; preguntar a los
valoradores, solo en RG50r, no cambia nada) y, en RG55r, el registro de la foto de medida_v3/rejuega_fotos.py (fotos.jsonl.gz, destinos.jsonl.gz).
   python3 lanza_cierre_v5.py puerta [procesos] -> RG50r (normal y sequía dura), el tonto (bestias que crían) y el recolector (sequía), semilla 1001, en
        valle_cierre_v5_puerta, frente a valle_taller_v52: muertes y criaturas de fin.json, mundo y criaturas línea a línea, y arbol.json
   python3 lanza_cierre_v5.py cierre [procesos] -> las 210 partidas de RG55r y RG055r"""
import gzip, json, os, sys
MODO = sys.argv[1] if len(sys.argv) > 1 else "cierre"
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); P8 = os.path.dirname(AQUI); sys.path.insert(0, P8); sys.path.insert(0, os.path.join(P8, "medida_v3"))
import rejuega_fotos as RF                                                  # (importa lanza_medida_v3: el árbol como en el experimento)
LM = RF.LM; T7 = LM.L.T7; T52 = os.path.join(T7, "valle_taller_v52")
MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian"); SEM = range(1001, 1022)

def una(arg):
    v, mu, s, dias, carp = arg; d = os.path.join(carp, f"{v}_{mu}_s{s}_d{dias}")
    if os.path.exists(os.path.join(d, "fin.json")): return {"id": os.path.basename(d), "saltada": True}
    if v == "RG55r":
        os.makedirs(d, exist_ok=True)
        RF.FH["f"] = gzip.open(os.path.join(d, "fotos.jsonl.gz"), "wt", encoding="utf-8", compresslevel=6); RF.FH["g"] = gzip.open(os.path.join(d, "destinos.jsonl.gz"), "wt", encoding="utf-8")
    try: r = LM.una(arg)
    finally:
        for k in ("f", "g"):
            if RF.FH.get(k) is not None: RF.FH[k].close()
        RF.FH.clear()
    return {"id": os.path.basename(d), "saltada": r.get("saltada", False), "segundos": r.get("segundos")}

def puerta(arg):
    v, mu, s, dias, carp = arg; una(arg); n = f"{v}_{mu}_s{s}_d{dias}"; a, b = os.path.join(carp, n), os.path.join(T52, n)
    fa, fb = json.load(open(os.path.join(a, "fin.json"))), json.load(open(os.path.join(b, "fin.json")))
    c = {"muertes": fa["muertes"] == fb["muertes"], "criaturas_fin": fa["criaturas"] == fb["criaturas"],
         "mundo": LM.lee_gz(os.path.join(a, "mundo.jsonl.gz")) == LM.lee_gz(os.path.join(b, "mundo.jsonl.gz")),
         "criaturas": LM.lee_gz(os.path.join(a, "criaturas.jsonl.gz")) == LM.lee_gz(os.path.join(b, "criaturas.jsonl.gz")),
         "arbol": json.load(open(os.path.join(a, "arbol.json"))) == json.load(open(os.path.join(b, "arbol.json")))}
    return dict(id=n, **c, identica=all(c.values()))


if __name__ == "__main__":
    npro = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    if MODO == "puerta":
        carp = os.path.join(T7, "valle_cierre_v5_puerta"); os.makedirs(carp, exist_ok=True)
        G = [("RG50r", "normal+sabores", 1001, 40, carp), ("RG50r", "sequia_dura+sabores", 1001, 40, carp), ("tonto", "bestias_crian", 1001, 40, carp), ("recolector", "sequia", 1001, 40, carp)]
        with Pool(npro) as p: R = p.map(puerta, G)
        out = {"identicas": sum(r["identica"] for r in R), "de": len(R), "partidas": R}
        json.dump(out, open(os.path.join(AQUI, "puerta_cierre_v5.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False))
    else:
        carp = os.path.join(T7, "valle_cierre_v5"); os.makedirs(carp, exist_ok=True)
        TR = [(v, mu + "+sabores", s, 40, carp) for mu in MUNDOS for v in ("RG55r", "RG055r") for s in SEM]
        with Pool(npro) as p:
            for r in p.imap_unordered(una, TR): print(json.dumps(r, ensure_ascii=False), flush=True)
