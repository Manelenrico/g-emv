"""[P8] Prompt 69: el lanzador del experimento. Juega una lista de partidas (variante × mundo × semilla, de N días) y escribe sus registros en el T7, no en el
disco del Mac. El Mac no se duerme mientras juega (se relanza bajo `caffeinate -ims`). Se puede retomar: una partida está hecha si tiene su `fin.json`
(se escribe el último, con otro nombre y renombrándolo al final); al volver a lanzar, salta las hechas y sigue con las demás.
Por partida, en <T7>/valle_experimento/<id>/:
  - mundo.jsonl.gz: el registro del mundo (una línea por turno: lo que hace cada una, dónde está, su cuerpo, su bolsa, la bestia, los sucesos; cada 4 turnos, los
    objetos del suelo, las plantas y los matorrales);
  - criaturas.jsonl.gz: una línea por turno: por criatura, las seis sumas de su estado de ahora antes del motor (placer, displacer, alegría, enfado, amor, tristeza:
    lo que mide la felicidad con el motor como instrumento), la llamada que hace y el sonido; y del mundo, lo que hay en cada despensa y en el almacén;
  - fin.json: quién muere, de qué y cuándo; por criatura, lo aprendido mirando, lo que cree de lo principal al acabar, lo juntado; la semilla, la config y el
    código con que se jugó (huellas), y lo que tardó.
Los mundos: abundancia, normal, sequia (los de siempre), sequia_dura y bestia_dia (los mandos de estrés, encendidos solo en la partida).
   python3 lanzador.py <variantes> <mundos> <semillas> [dias=40] [procesos=8] [carpeta]
   p. ej.: python3 lanzador.py RG32r,tonto normal 1,2 40
   (las semillas también como intervalo: 1001-1040)"""
import gzip, hashlib, json, os, sys, time
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path[:0] = [AQUI, os.path.join(RAIZ, "valle")]
T7 = "/Volumes/Mem G-EMV"
CARPETA_DEF = os.path.join(T7, "valle_experimento")

if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":               # que el Mac no se duerma mientras juega
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)

import mundo as MU
import banco_cuerpo_valle as B, banco_v7 as B7, banco_base_v5 as BB, pasada_v22 as P, cuerpo_valle as CV
CFG_M = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8"))
_open = open
def _abre(ruta, modo="r", *a, **k):                                         # el registro del mundo, comprimido desde el principio (sin ficheros a medias que borrar)
    if isinstance(ruta, str) and ruta.endswith(".gz"): return gzip.open(ruta, modo.replace("t", "") + ("t" if "b" not in modo else ""), encoding=k.get("encoding", "utf-8"))
    return _open(ruta, modo, *a, **k)
MU.open = _abre

def mundo_de(nombre):
    """los cambios del mundo de cada nombre (sobre la config, que no se toca)"""
    if nombre in ("abundancia", "normal", "sequia"): return {"matorrales": {"epocas": P.MUNDOS[nombre]}} if P.MUNDOS[nombre] else {}
    if nombre == "sequia_dura": return {"estres": {"sequia_dura": dict(CFG_M["estres"]["sequia_dura"], activo=True)}}
    if nombre == "bestia_dia": return {"bestia": {"de_dia": dict(CFG_M["bestia"]["de_dia"], activo=True)}}
    if nombre == "bestias_crian":                                            # (prompt 89, Manel) el mundo de estrés que sustituye a la bestia de día: ella, más una cría cada 20 días, hasta dos
        G = json.loads(json.dumps(CFG_M["bestia"]["pieza_g"])); G["cria"] = dict(G["cria"], **CFG_M["estres"]["bestias_crian"]["cria"])
        return {"bestia": {"de_dia": dict(CFG_M["bestia"]["de_dia"], activo=True), "pieza_g": G}}
    raise ValueError(nombre)

MUNDO_J = {}; CRI = {}; LOG = {}
_vi = MU.Valle.__init__
def _init(self, *a, **k):
    _vi(self, *a, **k); LOG["e"] = self
    for sec, kv in MUNDO_J.items():
        for k_, v_ in kv.items(): self.cfg[sec][k_] = v_
MU.Valle.__init__ = _init
_ac = CV.Criatura.actua
def _actua(self, obs, info):
    CRI[self.a] = self; acc = _ac(self, obs, info); self._log_acc = acc; return acc
CV.Criatura.actua = _actua
_sa = CV.Criatura.seis_ahora
def _seis(self):
    r = _sa(self); self._log_seis = (self.obs["turno"], r[0]); return r
CV.Criatura.seis_ahora = _seis
_st = MU.Valle.step
def _step(self, acciones):
    out = _st(self, acciones); f = LOG.get("fc")
    if f is not None:
        t = self.turno - 1; cr = {}
        for a, c in CRI.items():
            if self.cuerpo[a]["muerta"]: continue
            s_ = getattr(c, "_log_seis", None); acc = getattr(c, "_log_acc", None) or {}
            if s_ is None or s_[0] != t:                                    # sin voz este turno: las seis de ahora, para medir (no cambia nada)
                try: s_ = (t, _sa(c)[0])
                except Exception: s_ = (t, None)
            cr[a] = {"seis": {k: round(v, 4) for k, v in s_[1].items()} if s_[1] else None, "llama": acc.get("llama"), "suena": acc.get("suena")}
        tp = lambda L: {x: sum(1 for o in L if o["tipo"] == x) for x in ("comida", "medicina")}
        f.write(json.dumps({"turno": t, "criaturas": cr, "despensas": {k: tp(v) for k, v in self.despensa.items()}, "almacen": tp(self.almacen)}, ensure_ascii=False) + "\n")
    return out
MU.Valle.step = _step

def huella(ruta): return hashlib.md5(_open(ruta, "rb").read()).hexdigest()

def una(arg):
    v, mu, s, dias, carpeta = arg
    pid = f"{v}_{mu}_s{s}_d{dias}"; d = os.path.join(carpeta, pid); fin = os.path.join(d, "fin.json")
    if os.path.exists(fin): return {"id": pid, "saltada": True}
    os.makedirs(d, exist_ok=True); t0 = time.time(); c0 = time.process_time()
    CRI.clear(); MUNDO_J.clear(); MUNDO_J.update(mundo_de(mu))
    LOG["fc"] = gzip.open(os.path.join(d, "criaturas.jsonl.gz"), "wt", encoding="utf-8")
    reg = os.path.join(d, "mundo.jsonl.gz")
    if v in ("tonto", "recolector"): BB.partida(v, CFG_M["margen_comida"]["activo"], "medio", s, dias=dias, registro=reg, objetos_cada=4)
    else: B.partida("cuerpo", s, registro=reg, dias=dias, objetos_cada=4, cultura=B7.cultura("medio"), mando="medio", mundo=MUNDO_J or None, **B7.VARS[v])
    LOG["fc"].close(); LOG["fc"] = None
    e = LOG["e"]; D = e.dia_turnos
    claves = (("comida", "valle", "cuerpo"), ("medicina", "valle", "cuerpo"), ("bestia", "noche", "cuerpo"), ("matorral", "bosque", "recursos"), ("dormir", "fuera", "cuerpo"))
    out = {"id": pid, "variante": v, "mundo": mu, "semilla": s, "dias": dias, "mundo_cambios": MUNDO_J,
           "muertes": [{"criatura": a, "causa": e.cuerpo[a]["causa"], "turno": e.cuerpo[a]["turno_muerte"], "dia": e.cuerpo[a]["turno_muerte"] // D} for a in e.possible_agents if e.cuerpo[a]["muerta"]],
           "criaturas": {a: {"vistos": list(getattr(c, "vistos_log", [])), "vistos_descartados": dict(getattr(c, "visto_stats", {})), "juntados": getattr(c, "juntados", 0),
                             "cree": {f"{o}|{si}": (lambda x: None if x is None else round(x[dom], 4))(c.cuaderno.creencia(o, si)) for o, si, dom in claves},
                             "miedo": c.miedo, "hermana": c.hermana} for a, c in CRI.items()},
           "huellas": {"config": huella(os.path.join(RAIZ, "valle", "config_valle.json")), "mundo.py": huella(MU.__file__), "cuerpo_valle.py": huella(CV.__file__), "model.py": huella(os.path.join(RAIZ, "motor", "model.py"))},
           "segundos": round(time.time() - t0, 1), "cpu": round(time.process_time() - c0, 1)}
    tmp = fin + ".tmp"
    with _open(tmp, "w", encoding="utf-8") as fh: json.dump(out, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return {"id": pid, "saltada": False, "segundos": out["segundos"]}


if __name__ == "__main__":
    VS = sys.argv[1].split(","); MS = sys.argv[2].split(",")
    SS = [s_ for x in sys.argv[3].split(",") for s_ in (range(int(x.split("-")[0]), int(x.split("-")[1]) + 1) if "-" in x else [int(x)])]
    dias = int(sys.argv[4]) if len(sys.argv) > 4 else 40; npro = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    carpeta = sys.argv[6] if len(sys.argv) > 6 else CARPETA_DEF
    assert os.path.isdir(os.path.dirname(carpeta)), f"no está el disco: {os.path.dirname(carpeta)}"
    os.makedirs(carpeta, exist_ok=True)
    T = [(v, mu, s, dias, carpeta) for mu in MS for v in VS for s in SS]       # (prompt 70) por mundos, en el orden dado; dentro de cada mundo, por clase y semilla
    with Pool(npro) as p:
        for r in p.imap_unordered(una, T): print(json.dumps(r, ensure_ascii=False), flush=True)
