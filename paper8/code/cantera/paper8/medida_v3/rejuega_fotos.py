"""[P8] Prompt 101, punto 4: el registro de la foto por turno. Vuelve a jugar unas pocas partidas del experimento (valle_experimento_v2: el congelado v2, con
el árbol, 40 días), RG50r, RG050r y S50, semillas 30001-30003, en sequía, sequía dura y abundancia (27 partidas), en una carpeta aparte (valle_fotos_v3), y
apunta en <partida>/fotos.jsonl.gz, en cada decisión nueva (las que salen de las fotos; seguir un destino y las llamadas en cola no deciden), una línea:
   {"t": turno, "a": criatura, "ex": [fuerza, tercio] (la expresión, _expresion, la que mira el compromiso), "e": índice de la elegida (o -1 si no se casa),
    "o": [[nombre, acc sin la dirección, d, filas], ...]}
Las filas: la primera opción, entera (solo las distintas de 0); las demás, solo las filas que difieren de la primera (sin pérdida: una fila que falta = la de
la primera; un 0 explícito = no la tiene). Redondeo a 6 decimales. La elegida se casa como en lanza_medida_v3 (por identidad; si es una decisión nueva de
ir, por el destino recién comprometido o la planta).
Y en <partida>/destinos.jsonl.gz, cada vez que suelta un destino (cuerpo_valle._sigue_destino devuelve None): turno, criatura, adónde iba («que»), turnos desde
que se comprometió, y por qué: «llega» (está en el destino), «emoción» (cambió la expresión: la guardada y la nueva), «sin avanzar» (la misma casilla 3 turnos) o «sin paso» (el camino no da un paso válido este turno).
Al acabar cada partida la compara con la oficial (muertes y criaturas de fin.json; mundo.jsonl.gz y criaturas.jsonl.gz línea a línea): apuntar no debe
cambiar nada. Si una no sale idéntica, o la carpeta pasa de 2 GB, PARA.
   python3 rejuega_fotos.py prueba            -> RG50r, sequía dura, 30001, 2 días (valle_fotos_v3_prueba): cuánto ocupa y cuánto tarda
   python3 rejuega_fotos.py [procesos=7]      -> las 27 partidas"""
import gzip, json, os, subprocess, sys
MODO = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].isdigit() else "todas"
os.environ["EXPV2_MODO"] = "experimento"                                   # el árbol encendido, como en el experimento
os.environ["TALLER45_CARPETA"] = "valle_fotos_v3_prueba" if MODO == "prueba" else "valle_fotos_v3"
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); P8 = os.path.dirname(AQUI); sys.path.insert(0, P8); sys.path.insert(0, AQUI)
import lanza_medida_v3 as LM                                               # el mundo con el árbol (mundo_de) y la comparación con la oficial
import taller_v45 as T
import cuerpo_valle as CV
LM.PREGUNTA["si"] = False
CLASES = ("RG50r", "RG050r", "S50"); MUNDOS = ("sequia", "sequia_dura", "abundancia"); SEMILLAS = (30001, 30002, 30003); DIAS = 40; TOPE = 2 * 1024 ** 3
FH = {}; CUR = {}
CARPETA = os.path.join(LM.L.T7, "valle_fotos_v3_prueba" if MODO == "prueba" else "valle_fotos_v3")      # (la de CARPETA la fija lanza_medida_v3 al importarse)
r6 = lambda x: round(float(x), 6)

_st = CV.PL.select_tiebreak
def st(nombres, preds, terminal, meta, *a, **k):
    e = _st(nombres, preds, terminal, meta, *a, **k)
    if CUR.get("c") is not None: CUR["ult"] = (list(nombres), preds)
    return e
CV.PL.select_tiebreak = st                                                  # (lanza_medida_v3 ya envolvió la suya: esta va encima, y solo mira)

_ac = CV.Criatura.actua
def actua(self, obs, info):
    CUR["c"] = self; CUR.pop("ult", None); acc = _ac(self, obs, info); CUR["c"] = None
    if FH.get("f") is not None and CUR.get("ult") is not None: apunta(self, acc)
    return acc
CV.Criatura.actua = actua

def apunta(c, acc):
    nombres, preds = CUR["ult"]; f0 = next((n for n in nombres if preds[n]["acc"] is acc), None)
    if f0 is None and acc.get("_ir") and not acc.get("_compromiso"):
        if acc["_ir"] == "trabajar_planta": f0 = next((n for n in nombres if preds[n]["acc"].get("que") == "trabajar_planta" and preds[n]["acc"].get("planta") == acc.get("planta")), None)
        elif c.dest is not None and c.dest.get("t0") == c.obs["turno"]: f0 = next((n for n in nombres if preds[n]["acc"] == c.dest["acc"]), None)
    if f0 is None and not acc.get("_ir"): return                           # (no salió de las fotos)
    base = {k: r6(v) for k, v in preds[nombres[0]]["F"].items() if r6(v) != 0.0}; O = []
    for i, n in enumerate(nombres):
        p = preds[n]; F = {k: r6(v) for k, v in p["F"].items()}
        if i == 0: fil = base
        else: fil = {k: v for k, v in F.items() if v != base.get(k, 0.0)}; fil.update({k: 0.0 for k in base if k not in F})
        O.append([p["acc"].get("que") or p["acc"]["accion"], {k: (list(v) if isinstance(v, tuple) else v) for k, v in p["acc"].items() if k != "dir"}, r6(p["d"]), fil])
    FH["f"].write(json.dumps({"t": c.obs["turno"], "a": c.a, "ex": list(c._expresion()), "e": nombres.index(f0) if f0 is not None else -1, "o": O}, ensure_ascii=False, separators=(",", ":")) + "\n")

_sd = CV.Criatura._sigue_destino
def sigue_destino(self, obs, validas):
    D = self.dest; ex0 = D.get("ex") if D else None; r = _sd(self, obs, validas)
    if r is None and D is not None and FH.get("g") is not None:
        pos = tuple(obs["yo"]["pos"]); dst = tuple(D["acc"]["destino"]); ex1 = D.get("ex")
        n_ = CV.CFG["compromiso"]["sin_avanzar_turnos"]; quieta = len(D["hist"]) >= n_ + 1 and len(set(D["hist"])) == 1
        por = "llega" if pos == dst else ("emoción" if (ex0 is not None and ex1 != ex0) else ("sin avanzar" if quieta else "sin paso"))
        FH["g"].write(json.dumps({"t": obs["turno"], "a": self.a, "que": D["acc"].get("que"), "turnos": obs["turno"] - D.get("t0", obs["turno"]), "por": por,
                                  "ex0": list(ex0) if ex0 else None, "ex1": list(ex1) if ex1 else None}, ensure_ascii=False) + "\n")
    return r
CV.Criatura._sigue_destino = sigue_destino

def una(arg):
    v, mu, s, dias, carpeta = arg; d = os.path.join(carpeta, f"{v}_{mu}_s{s}_d{dias}")
    if os.path.exists(os.path.join(d, "fin.json")): return {"id": os.path.basename(d), "saltada": True}
    os.makedirs(d, exist_ok=True)
    FH["f"] = gzip.open(os.path.join(d, "fotos.jsonl.gz"), "wt", encoding="utf-8", compresslevel=6); FH["g"] = gzip.open(os.path.join(d, "destinos.jsonl.gz"), "wt", encoding="utf-8")
    try: r = T.una(arg)
    finally: FH["f"].close(); FH["g"].close(); FH.clear()
    return dict(r, fotos_mb=round(os.path.getsize(os.path.join(d, "fotos.jsonl.gz")) / 1e6, 1))

def una_y_compara(arg):
    r = una(arg); v, mu, s, dias, carpeta = arg; n = f"{v}_{mu}_s{s}_d{dias}"
    a, b = os.path.join(carpeta, n), os.path.join(LM.OFICIAL, n); fa, fb = json.load(open(os.path.join(a, "fin.json"))), json.load(open(os.path.join(b, "fin.json")))
    c = {"muertes": fa["muertes"] == fb["muertes"], "criaturas_fin": fa["criaturas"] == fb["criaturas"],
         "mundo": LM.lee_gz(os.path.join(a, "mundo.jsonl.gz")) == LM.lee_gz(os.path.join(b, "mundo.jsonl.gz")),
         "criaturas": LM.lee_gz(os.path.join(a, "criaturas.jsonl.gz")) == LM.lee_gz(os.path.join(b, "criaturas.jsonl.gz"))}
    return dict(r, id=n, **c, identica=all(c.values()))

def tamano(carpeta): return int(subprocess.run(["du", "-sk", carpeta], capture_output=True, text=True).stdout.split()[0]) * 1024


if __name__ == "__main__":
    if MODO == "prueba":
        os.makedirs(CARPETA, exist_ok=True); r = una(("RG50r", "sequia_dura+sabores", 30001, 2, CARPETA)); print(json.dumps(r, ensure_ascii=False))
    else:
        npro = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7; os.makedirs(CARPETA, exist_ok=True)
        TR = [(v, mu + "+sabores", s, DIAS, CARPETA) for mu in MUNDOS for v in CLASES for s in SEMILLAS]; R = []; para = None
        with Pool(npro) as p:
            for r in p.imap_unordered(una_y_compara, TR):
                R.append(r); tam = tamano(CARPETA); print(json.dumps(dict({k: r.get(k) for k in ("id", "identica", "fotos_mb", "segundos")}, carpeta_gb=round(tam / 1024 ** 3, 2)), ensure_ascii=False), flush=True)
                if not r["identica"]: para = {"por": "no idéntica", **r}; p.terminate(); break
                if tam > TOPE: para = {"por": "pasa de 2 GB", "gb": round(tam / 1024 ** 3, 2)}; p.terminate(); break
        out = {"jugadas": len(R), "identicas": sum(r["identica"] for r in R), "para": para, "partidas": R}
        json.dump(out, open(os.path.join(AQUI, "rejuega_fotos.json"), "w"), ensure_ascii=False, indent=1)
        print(json.dumps({k: out[k] for k in ("jugadas", "identicas", "para")}, ensure_ascii=False), flush=True)
