"""[P8] Prompt 143 (taller): el lanzador de VC1, la voz de ir a casa (cuerpo_vc1.py). Juega con el lanzador del experimento v5 (lanza_experimento_v5: los mismos
registros; aquí su `una` se repite con el registro de decisiones también para VC1, que no cambia ninguna decisión) y añade, solo en ficheros nuevos:
  - LA CLASE: B.partida crea las criaturas con CV.Criatura; durante una partida de VC1 se cambia por cuerpo_vc1.VC1 y se vuelve a poner al acabar.
    VC1 = banco_v7.VARS["RG68r"] con a_casa=True; VC1off, con a_casa=False (la puerta); VC1calla, con a_casa=True y a_casa_calla=True (calcula y no cambia nada).
  - LO DEL MUNDO QUE NECESITA LA VOZ (cuerpo_vc1.ESTADO): después del reset y de cada paso, dónde está cada criatura, si durmió ese turno y si está muerta.
  - GUARDA <partida>/voz_vc1.json: las voces, las decisiones oyendo y las cuentas de cada criatura.
  - Las partidas se juegan con la configuración de 40 días (los sorteos del principio del mundo dependen de cuántos días dura: prompt 141) y la de la puerta y
    la de la comprobación se paran al acabar el día 9 (parada.json, sin fin.json).
   python3 lanza_vc1.py puerta    VC1off y VC1calla, sequía dura 30121, días 0 a 9, frente a la sellada de RG68r del v5 -> salida/puerta_vc1.json
   python3 lanza_vc1.py prueba    VC1, sequía dura 30121, 10 días -> salida/prueba_vc1.json
   python3 lanza_vc1.py taller    VC1, 40 días: sequía dura y sequía 30121-30140; normal y bestias que crían 30121-30130 -> /Volumes/Mem G-EMV/valle_vc1_taller"""
import gzip, json, os, sys, time
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import lanza_experimento_v5 as L5
import cuerpo_vc1 as Z
import banco_v7 as B7
L = L5.L; CV = L5.CV; LM = L5.LM; T7 = L.T7; DIA = Z.DIA
B7.VARS["VC1"] = dict(B7.VARS["RG68r"], a_casa=True); B7.VARS["VC1off"] = dict(B7.VARS["RG68r"], a_casa=False)
B7.VARS["VC1calla"] = dict(B7.VARS["RG68r"], a_casa=True, a_casa_calla=True)
L5.CRIATURAS = tuple(L5.CRIATURAS) + ("VC1", "VC1off", "VC1calla")
EXP = os.path.join(T7, "valle_experimento_v5"); TALLER = os.path.join(T7, "valle_vc1_taller"); OP = {"parar": None}

def estado(e):
    Z.ESTADO.clear(); Z.ESTADO.update({a: (tuple(e.pos[a]), bool(e.cuerpo[a].get("dormida")), bool(e.cuerpo[a]["muerta"])) for a in e.agents if a in e.cuerpo})
_rs = L.MU.Valle.reset
def _reset(self, *a, **k):
    r = _rs(self, *a, **k); Z.nueva_partida(); estado(self); return r
L.MU.Valle.reset = _reset
class Parar(Exception): pass
_stp = L.MU.Valle.step
def _step(self, acciones):
    out = _stp(self, acciones); estado(self)
    if OP["parar"] and self.turno >= OP["parar"] * DIA: raise Parar()
    return out
L.MU.Valle.step = _step

def una_v5(arg):
    """lanza_experimento_v5.una, con el registro de decisiones (preguntar) también para VC1"""
    v, mu, s, dias, carpeta = arg; d = os.path.join(carpeta, f"{v}_{mu}_s{s}_d{dias}"); R = L5.REG
    os.makedirs(d, exist_ok=True)
    R["si"] = True; R["fh"] = gzip.open(os.path.join(d, "balance.jsonl.gz"), "wt", encoding="utf-8"); R["ff"] = gzip.open(os.path.join(d, "filas.jsonl.gz"), "wt", encoding="utf-8")
    try: r = LM.una(arg, preguntar=True)
    finally:
        for k in ("fh", "ff"):
            if R[k] is not None: R[k].close()
            R[k] = None
        R["si"] = False
    if not r.get("saltada"):
        L5.cuaderno_sitios(d); json.dump({a: getattr(c, "cuenta_v61", None) for a, c in L.CRI.items()}, open(os.path.join(d, "cuenta_v61.json"), "w"), ensure_ascii=False)
    return dict(r, id=os.path.basename(d))

def una(x):
    v, mu, s, carp, parar = x; d = os.path.join(carp, f"{v}_{mu}_s{s}_d40")
    if os.path.exists(os.path.join(d, "fin.json")) or os.path.exists(os.path.join(d, "parada.json")): return {"id": os.path.basename(d), "saltada": True}
    os.makedirs(d, exist_ok=True); OP["parar"] = parar; viejo = CV.Criatura; CV.Criatura = Z.VC1; t0 = time.time()
    try: r = una_v5((v, mu, s, 40, carp))
    except Parar:                                                                # (parada al acabar el día parar-1: se cierran los registros; no hay fin.json)
        e = L.LOG.get("e")
        if e is not None and getattr(e, "_f", None) is not None: e._f.close(); e._f = None
        if L.LOG.get("fc") is not None: L.LOG["fc"].close(); L.LOG["fc"] = None
        if LM.PREGUNTA["si"]:                                                   # (el registro de decisiones, que lanza_medida_v3 solo escribe al acabar)
            with gzip.open(os.path.join(d, "decisiones.jsonl.gz"), "wt", encoding="utf-8") as fh:
                for x_ in LM.DEC: fh.write(json.dumps(x_, ensure_ascii=False) + "\n")
        LM.PREGUNTA["si"] = False
        for k in ("fh", "ff"):
            if L5.REG[k] is not None: L5.REG[k].close()
            L5.REG[k] = None
        L5.REG["si"] = False
        r = {"id": os.path.basename(d), "parada_en_el_dia": parar}; json.dump(r, open(os.path.join(d, "parada.json"), "w"))
    finally: CV.Criatura = viejo; OP["parar"] = None
    json.dump({a: {"voces": c.vc_voces, "oye": c.vc_oye, "cuenta": c.vc_cuenta} for a, c in sorted(L.CRI.items()) if isinstance(c, Z.VC1)},
              open(os.path.join(d, "voz_vc1.json"), "w"), ensure_ascii=False)
    return dict(r, segundos=round(time.time() - t0, 1))

def lineas(ruta, hasta):
    out = []
    for l in gzip.open(ruta, "rt", encoding="utf-8"):
        x = json.loads(l)
        if x.get("turno", x.get("t")) >= hasta: break
        out.append(l)
    return out

def igual(a, b, dias):
    """el registro del mundo, el de las criaturas y el de las decisiones de los primeros `dias` días, línea a línea"""
    out = {k: lineas(os.path.join(a, f), dias * DIA) == lineas(os.path.join(b, f), dias * DIA) for k, f in (("mundo", "mundo.jsonl.gz"), ("criaturas", "criaturas.jsonl.gz"))}
    da = [l for l in gzip.open(os.path.join(a, "decisiones.jsonl.gz"), "rt", encoding="utf-8") if json.loads(l)[0] < dias * DIA]
    db = [l for l in gzip.open(os.path.join(b, "decisiones.jsonl.gz"), "rt", encoding="utf-8") if json.loads(l)[0] < dias * DIA]
    return dict(out, decisiones=da == db, lineas_mundo=len(lineas(os.path.join(a, "mundo.jsonl.gz"), dias * DIA)))


if __name__ == "__main__":
    MODO = sys.argv[1]; os.makedirs(os.path.join(AQUI, "salida"), exist_ok=True); MU_ = "sequia_dura+sabores"
    if MODO == "puerta":
        C_ = os.path.join(T7, "valle_vc1_puerta")
        with Pool(2, maxtasksperchild=1) as p: R = p.map(una, [(v, MU_, 30121, C_, 10) for v in ("VC1off", "VC1calla")])
        ref = os.path.join(EXP, f"RG68r_{MU_}_s30121_d40"); out = {}
        for v in ("VC1off", "VC1calla"):
            dv = os.path.join(C_, f"{v}_{MU_}_s30121_d40"); vz = json.load(open(os.path.join(dv, "voz_vc1.json")))
            out[v] = dict(igual(dv, ref, 10), voces=sum(len(x["voces"]) for x in vz.values()), decisiones_oyendo=sum(len(x["oye"]) for x in vz.values()))
        json.dump(out, open(os.path.join(AQUI, "salida", "puerta_vc1.json"), "w"), indent=1); print(json.dumps(out, indent=1))
    elif MODO == "prueba":
        C_ = os.path.join(T7, "valle_vc1_prueba")
        with Pool(1, maxtasksperchild=1) as p: R = p.map(una, [("VC1", MU_, 30121, C_, 10)])
        print(json.dumps(R))
    elif MODO == "taller":
        T_ = [("VC1", mu + "+sabores", s, TALLER, None) for mu in ("sequia_dura", "sequia") for s in range(30121, 30141)] + \
             [("VC1", mu + "+sabores", s, TALLER, None) for mu in ("normal", "bestias_crian") for s in range(30121, 30131)]
        with Pool(6, maxtasksperchild=1) as p:
            for r in p.imap_unordered(una, T_): print(json.dumps({k: r.get(k) for k in ("id", "segundos", "saltada")}), flush=True)
