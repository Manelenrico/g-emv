"""[P8] Prompt 117: el lanzador del experimento de la base del ocho, tercera versión (congelado v4: RG61r). Es lanza_experimento_v3.py (prompt 113) con las
clases, las semillas y la carpeta nuevas, y dos registros más: las filas de duelo, soledad y compañía (filas.jsonl.gz, para no tener que volver a jugar) y, al
acabar cada partida de criatura, las cuentas de la v61 (cuenta_v61.json). Juega con el lanzador de la medida del prompt 101
(medida_v3/lanza_medida_v3.una: el árbol encendido en los cinco mundos, arbol.json al acabar, reanudable: se salta las partidas que ya tienen fin.json) y apunta:
  - en las cinco clases de criatura, por criatura y turno (filas.jsonl.gz), de la foto de ahora que el lanzador ya calcula (la de las seis), las filas
    S-DUELO-CUERPO, S-DUELO-RECURSOS, S-DUELO-VINCULO, S-SOLEDAD y S-COMPANIA (0 si no está). Una línea por turno: {"t": turno, "c": {criatura: [las cinco]}};
  - en RG61r, el registro de decisiones con las de ir (preguntar a los tres valoradores en cada decisión: decisiones.jsonl.gz, con la columna 15 de lanza_medida_v3);
  - en las cinco clases de criatura, para las medidas sin predicción, por criatura y turno (balance.jsonl.gz, comprimido): el balance de cada dimensión (cuerpo,
    recursos, vínculo: la fuerza de ganancia menos la de pérdida, de las seis que el lanzador ya calcula para criaturas.jsonl.gz, sin volver a calcularlas), la
    casilla, el sitio (C su casa · O otra casa · P una puerta · o el nombre del terreno), si está dormida y si ve la bestia. Una línea por turno:
       {"t": turno, "c": {criatura: [b_cuerpo, b_recursos, b_vinculo, x, y, sitio, dormida, bestia_vista]}}
  - al acabar cada partida de criatura, los recuerdos de sitios de su cuaderno (cuaderno_sitios.json: por criatura, «sitio:<terreno>» y su situación, cada recuerdo
    con su efecto, importancia, intensidad y origen; se lee cuando la partida ya ha acabado).
   python3 lanza_experimento_v4.py puerta            -> RG61r (bestias que crían, 1004, frente a valle_arreglos_v8b, la de referencia del congelado v4) y el
        tonto (normal, 30001, frente a valle_experimento_v2), sin los registros nuevos, idénticas (muertes, criaturas, mundo y criaturas línea a línea)
   python3 lanza_experimento_v4.py prueba            -> RG61r (normal, 9101) y RG061r (bestias que crían, 9102), 10 días, con y sin apuntar: idénticas
   python3 lanza_experimento_v4.py experimento [procesos=10] -> las 1.400 partidas (7 jugadores × 5 mundos con el árbol × semillas 30081-30120, 40 días),
        en la carpeta oficial valle_experimento_v4"""
FILAS = ("S-DUELO-CUERPO", "S-DUELO-RECURSOS", "S-DUELO-VINCULO", "S-SOLEDAD", "S-COMPANIA")
import gzip, json, os, sys
MODO = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].isdigit() else "experimento"
os.environ["MEDV3_MODO"] = "prueba"                                            # (lanza_medida_v3 lee su modo de sys.argv o de aquí; solo fija su carpeta por defecto, que no se usa)
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI); sys.path.insert(0, os.path.join(AQUI, "medida_v3"))
import lanza_medida_v3 as LM                                                    # (el árbol como en el experimento; preguntar, solo si se pide)
L = LM.L; CV = LM.CV; T7 = L.T7
CRIATURAS = ("RG61r", "RG061r", "S61", "S061", "P61"); BASE = ("tonto", "recolector"); MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian")
SEMILLAS = range(30081, 30121); DIAS = 40; OFICIAL = os.path.join(T7, "valle_experimento_v4")
REG = {"si": False, "fh": None, "ff": None}

# las seis de ahora y las filas de la foto de ahora, recordadas por criatura y turno (el lanzador las calcula para criaturas.jsonl.gz; aquí no se vuelven a calcular)
_sa0 = L._sa
def _sa(c):
    r = _sa0(c); c._seis_v3 = (c.obs["turno"], r[0]); c._filas_v4 = (c.obs["turno"], r[1]); return r
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
        fl = {}                                                                 # (prompt 117) las filas de duelo, soledad y compañía
        for a, c in L.CRI.items():
            q = getattr(c, "_filas_v4", None)
            if self.cuerpo[a]["muerta"] or q is None or q[0] != t: continue
            fl[a] = [round(float(q[1].get(k, 0.0) or 0.0), 5) for k in FILAS]
        REG["ff"].write(json.dumps({"t": t, "c": fl}, separators=(",", ":")) + "\n")
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
    REG["ff"] = gzip.open(os.path.join(d, "filas.jsonl.gz"), "wt", encoding="utf-8") if REG["si"] else None
    try: r = LM.una(arg, preguntar=(apuntar and v == "RG61r"))
    finally:
        for k in ("fh", "ff"):
            if REG[k] is not None: REG[k].close()
            REG[k] = None
        REG["si"] = False
    if apuntar and cri and not r.get("saltada"):
        cuaderno_sitios(d)
        json.dump({a: getattr(c, "cuenta_v61", None) for a, c in L.CRI.items()}, open(os.path.join(d, "cuenta_v61.json"), "w"), ensure_ascii=False)     # (solo medir)
    return dict(r, id=os.path.basename(d))

def iguales(a, b, fotos=False):
    fa, fb = json.load(open(os.path.join(a, "fin.json"))), json.load(open(os.path.join(b, "fin.json")))
    c = {"muertes": fa["muertes"] == fb["muertes"], "criaturas_fin": fa["criaturas"] == fb["criaturas"],
         "mundo": LM.lee_gz(os.path.join(a, "mundo.jsonl.gz")) == LM.lee_gz(os.path.join(b, "mundo.jsonl.gz")),
         "criaturas": LM.lee_gz(os.path.join(a, "criaturas.jsonl.gz")) == LM.lee_gz(os.path.join(b, "criaturas.jsonl.gz"))}
    return dict(c, identica=all(c.values()))

def puerta(x):
    v, mu, s, ref = x; carp = os.path.join(T7, "valle_experimento_v4_puerta"); os.makedirs(carp, exist_ok=True); n = f"{v}_{mu}_s{s}_d40"
    una((v, mu, s, 40, carp), apuntar=False); return dict(iguales(os.path.join(carp, n), os.path.join(T7, ref, n)), id=n, frente_a=ref)

def prueba(x):
    v, mu, s, ap = x; carp = os.path.join(T7, "valle_experimento_v4_prueba_" + ("con" if ap else "sin")); os.makedirs(carp, exist_ok=True)
    return dict(una((v, mu, s, 10, carp), apuntar=ap), carpeta=carp, apunta=ap, v=v, mu=mu, s=s)


if __name__ == "__main__":
    if MODO == "puerta":
        with Pool(2) as p: R = p.map(puerta, [("RG61r", "bestias_crian+sabores", 1004, "valle_arreglos_v8b"), ("tonto", "normal", 30001, "valle_experimento_v2")])
        out = {"identicas": sum(r["identica"] for r in R), "de": len(R), "partidas": R}
        json.dump(out, open(os.path.join(AQUI, "salida", "puerta_experimento_v4.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False))
    elif MODO == "prueba":
        P = [("RG61r", "normal+sabores", 9101), ("RG061r", "bestias_crian+sabores", 9102)]
        with Pool(4) as p: R = p.map(prueba, [x + (ap,) for x in P for ap in (True, False)])
        out = []
        for v, mu, s in P:
            con = next(r for r in R if r["v"] == v and r["apunta"]); sin = next(r for r in R if r["v"] == v and not r["apunta"]); n = f"{v}_{mu}_s{s}_d10"
            a = os.path.join(con["carpeta"], n); out.append(dict(iguales(a, os.path.join(sin["carpeta"], n)), id=n, decisiones=os.path.exists(os.path.join(a, "decisiones.jsonl.gz")),
                                                                 balance=os.path.exists(os.path.join(a, "balance.jsonl.gz")), cuaderno_sitios=os.path.exists(os.path.join(a, "cuaderno_sitios.json")),
                                                                 filas=os.path.exists(os.path.join(a, "filas.jsonl.gz")), cuenta_v61=os.path.exists(os.path.join(a, "cuenta_v61.json"))))
        json.dump(out, open(os.path.join(AQUI, "salida", "prueba_experimento_v4.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False))
    else:
        npro = int(sys.argv[2]) if len(sys.argv) > 2 else 10; os.makedirs(OFICIAL, exist_ok=True)
        TR = [(v, mu, s, DIAS, OFICIAL) for mu in MUNDOS for v in BASE for s in SEMILLAS]
        TR += [(v, mu + "+sabores", s, DIAS, OFICIAL) for mu in MUNDOS for v in CRIATURAS for s in SEMILLAS]
        with Pool(npro) as p:
            for r in p.imap_unordered(una, TR): print(json.dumps({k: r[k] for k in ("id", "saltada", "decisiones") if k in r}, ensure_ascii=False), flush=True)
