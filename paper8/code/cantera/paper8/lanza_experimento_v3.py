"""[P8] Prompt 113: el lanzador del experimento de la base del ocho, segunda versión (congelado v3: RG58r). Juega con el lanzador de la medida del prompt 101
(medida_v3/lanza_medida_v3.una: el árbol encendido en los cinco mundos, arbol.json al acabar, reanudable: se salta las partidas que ya tienen fin.json) y apunta:
  - en RG58r, el registro de decisiones con las de ir (preguntar a los tres valoradores en cada decisión: decisiones.jsonl.gz, con la columna 15 de lanza_medida_v3);
  - en las cinco clases de criatura, para las medidas sin predicción, por criatura y turno (balance.jsonl.gz, comprimido): el balance de cada dimensión (cuerpo,
    recursos, vínculo: la fuerza de ganancia menos la de pérdida, de las seis que el lanzador ya calcula para criaturas.jsonl.gz, sin volver a calcularlas), la
    casilla, el sitio (C su casa · O otra casa · P una puerta · o el nombre del terreno), si está dormida y si ve la bestia. Una línea por turno:
       {"t": turno, "c": {criatura: [b_cuerpo, b_recursos, b_vinculo, x, y, sitio, dormida, bestia_vista]}}
  - al acabar cada partida de criatura, los recuerdos de sitios de su cuaderno (cuaderno_sitios.json: por criatura, «sitio:<terreno>» y su situación, cada recuerdo
    con su efecto, importancia, intensidad y origen; se lee cuando la partida ya ha acabado).
   python3 lanza_experimento_v3.py puerta            -> RG58r (bestias que crían, 1004, frente a valle_medicina_v1) y el tonto (normal, 30001, frente a
        valle_experimento_v2), sin el registro nuevo, idénticas (muertes, criaturas, mundo y criaturas línea a línea)
   python3 lanza_experimento_v3.py prueba            -> RG58r (normal, 9101) y RG058r (bestias que crían, 9102), 10 días, con y sin apuntar: idénticas
   python3 lanza_experimento_v3.py experimento [procesos=10] -> las 1.400 partidas (7 jugadores × 5 mundos con el árbol × semillas 30041-30080, 40 días),
        en la carpeta oficial valle_experimento_v3"""
import gzip, json, os, sys
MODO = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].isdigit() else "experimento"
os.environ["MEDV3_MODO"] = "prueba"                                            # (lanza_medida_v3 lee su modo de sys.argv o de aquí; solo fija su carpeta por defecto, que no se usa)
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI); sys.path.insert(0, os.path.join(AQUI, "medida_v3"))
import lanza_medida_v3 as LM                                                    # (el árbol como en el experimento; preguntar, solo si se pide)
L = LM.L; CV = LM.CV; T7 = L.T7
CRIATURAS = ("RG58r", "RG058r", "S58", "S058", "P58"); BASE = ("tonto", "recolector"); MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian")
SEMILLAS = range(30041, 30081); DIAS = 40; OFICIAL = os.path.join(T7, "valle_experimento_v3")
REG = {"si": False, "fh": None}

# las seis de ahora, recordadas por criatura y turno (el lanzador las calcula para criaturas.jsonl.gz; aquí no se vuelven a calcular)
_sa0 = L._sa
def _sa(c):
    r = _sa0(c); c._seis_v3 = (c.obs["turno"], r[0]); return r
L._sa = _sa
_st = L.MU.Valle.step
def _step(self, acciones):
    out = _st(self, acciones)
    if REG["si"] and REG["fh"] is not None:
        t = self.turno - 1; cr = {}
        for a, c in L.CRI.items():
            if self.cuerpo[a]["muerta"]: continue
            s_ = getattr(c, "_seis_v3", None)
            if s_ is None or s_[0] != t: continue
            sx = s_[1]; p = tuple(self.pos[a]); k = self.celda_casa.get(p)
            sitio = ("P" if p == self.puerta_casa.get(k) else ("C" if k == self.casa_de[a] else "O")) if k is not None else str(self.terreno(p))
            cr[a] = [round(sx["placer"] - sx["displacer"], 4), round(sx["alegria"] - sx["enfado"], 4), round(sx["amor"] - sx["tristeza"], 4), p[0], p[1], sitio,
                     int(bool(self.cuerpo[a].get("dormida"))), int((c.obs or {}).get("bestia") is not None)]
        REG["fh"].write(json.dumps({"t": t, "c": cr}, separators=(",", ":")) + "\n")
    return out
L.MU.Valle.step = _step

def cuaderno_sitios(d):
    out = {}
    for a, c in L.CRI.items():
        out[a] = {o: {sit: [{k: r.get(k) for k in ("dia", "efecto", "importancia", "intensidad", "origen")} for r in recs] for sit, recs in (w.get("situaciones") or {}).items()}
                  for o, w in c.cuaderno.objetos.items() if o.startswith("sitio:")}
    json.dump(out, open(os.path.join(d, "cuaderno_sitios.json"), "w"), ensure_ascii=False)

def una(arg, apuntar=True):
    v, mu, s, dias, carpeta = arg; d = os.path.join(carpeta, f"{v}_{mu}_s{s}_d{dias}")
    if os.path.exists(os.path.join(d, "fin.json")): return {"id": os.path.basename(d), "saltada": True}
    os.makedirs(d, exist_ok=True); cri = v in CRIATURAS or v.startswith("RG")
    REG["si"] = apuntar and cri; REG["fh"] = gzip.open(os.path.join(d, "balance.jsonl.gz"), "wt", encoding="utf-8") if REG["si"] else None
    try: r = LM.una(arg, preguntar=(apuntar and v == "RG58r"))
    finally:
        if REG["fh"] is not None: REG["fh"].close()
        REG["fh"] = None; REG["si"] = False
    if apuntar and cri and not r.get("saltada"): cuaderno_sitios(d)
    return dict(r, id=os.path.basename(d))

def iguales(a, b, fotos=False):
    fa, fb = json.load(open(os.path.join(a, "fin.json"))), json.load(open(os.path.join(b, "fin.json")))
    c = {"muertes": fa["muertes"] == fb["muertes"], "criaturas_fin": fa["criaturas"] == fb["criaturas"],
         "mundo": LM.lee_gz(os.path.join(a, "mundo.jsonl.gz")) == LM.lee_gz(os.path.join(b, "mundo.jsonl.gz")),
         "criaturas": LM.lee_gz(os.path.join(a, "criaturas.jsonl.gz")) == LM.lee_gz(os.path.join(b, "criaturas.jsonl.gz"))}
    return dict(c, identica=all(c.values()))

def puerta(x):
    v, mu, s, ref = x; carp = os.path.join(T7, "valle_experimento_v3_puerta"); os.makedirs(carp, exist_ok=True); n = f"{v}_{mu}_s{s}_d40"
    una((v, mu, s, 40, carp), apuntar=False); return dict(iguales(os.path.join(carp, n), os.path.join(T7, ref, n)), id=n, frente_a=ref)

def prueba(x):
    v, mu, s, ap = x; carp = os.path.join(T7, "valle_experimento_v3_prueba_" + ("con" if ap else "sin")); os.makedirs(carp, exist_ok=True)
    return dict(una((v, mu, s, 10, carp), apuntar=ap), carpeta=carp, apunta=ap, v=v, mu=mu, s=s)


if __name__ == "__main__":
    if MODO == "puerta":
        with Pool(2) as p: R = p.map(puerta, [("RG58r", "bestias_crian+sabores", 1004, "valle_medicina_v1"), ("tonto", "normal", 30001, "valle_experimento_v2")])
        out = {"identicas": sum(r["identica"] for r in R), "de": len(R), "partidas": R}
        json.dump(out, open(os.path.join(AQUI, "salida", "puerta_experimento_v3.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False))
    elif MODO == "prueba":
        P = [("RG58r", "normal+sabores", 9101), ("RG058r", "bestias_crian+sabores", 9102)]
        with Pool(4) as p: R = p.map(prueba, [x + (ap,) for x in P for ap in (True, False)])
        out = []
        for v, mu, s in P:
            con = next(r for r in R if r["v"] == v and r["apunta"]); sin = next(r for r in R if r["v"] == v and not r["apunta"]); n = f"{v}_{mu}_s{s}_d10"
            a = os.path.join(con["carpeta"], n); out.append(dict(iguales(a, os.path.join(sin["carpeta"], n)), id=n, decisiones=os.path.exists(os.path.join(a, "decisiones.jsonl.gz")),
                                                                 balance=os.path.exists(os.path.join(a, "balance.jsonl.gz")), cuaderno_sitios=os.path.exists(os.path.join(a, "cuaderno_sitios.json"))))
        json.dump(out, open(os.path.join(AQUI, "salida", "prueba_experimento_v3.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False))
    else:
        npro = int(sys.argv[2]) if len(sys.argv) > 2 else 10; os.makedirs(OFICIAL, exist_ok=True)
        TR = [(v, mu, s, DIAS, OFICIAL) for mu in MUNDOS for v in BASE for s in SEMILLAS]
        TR += [(v, mu + "+sabores", s, DIAS, OFICIAL) for mu in MUNDOS for v in CRIATURAS for s in SEMILLAS]
        with Pool(npro) as p:
            for r in p.imap_unordered(una, TR): print(json.dumps({k: r[k] for k in ("id", "saltada", "decisiones") if k in r}, ensure_ascii=False), flush=True)
