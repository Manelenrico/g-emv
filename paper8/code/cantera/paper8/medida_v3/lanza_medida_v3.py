"""[P8] Prompt 101: COPIA de lanza_experimento_v2.py (el original no se toca: es el que corrió el experimento) con el registro de decisiones arreglado.
EL ARREGLO (en `pregunta`): el original buscaba lo elegido por identidad (`preds[n]["acc"] is acc`), y cuando lo elegido es un «ir_…» (o trabajar_planta),
Criatura.actua lo cambia por un «mover» (o un «trabajar») antes de devolverlo: no lo encontraba y no apuntaba la decisión. Ahora, si no lo encuentra por
identidad y la acción viene de una decisión nueva de ir (lleva `_ir` y no `_compromiso`), lo busca: el destino recién comprometido (`c.dest`, con t0 = este
turno: una copia de la opción elegida, igual en valor) o, para trabajar_planta, la opción con esa planta. Las filas así encontradas llevan al final un 1
(columna 15; las demás, 0); las 14 primeras columnas son las de siempre. Las que no se puedan casar se cuentan (`sin_casar`).
Modos nuevos:
   python3 lanza_medida_v3.py prueba            -> RG50r (normal+sabores, 9001, 10 días) con y sin preguntar: idénticas, y cuántas decisiones de ir se apuntan
   python3 lanza_medida_v3.py rejuega [procesos=7] -> las 200 partidas de RG50r del experimento en valle_medida_v3_rg50r; al acabar cada una, la compara con la
        oficial (muertes y criaturas de fin.json, mundo.jsonl.gz y criaturas.jsonl.gz línea a línea, y decisiones: las nuevas sin las de ir = las oficiales);
        a la primera que no salga idéntica, PARA
Lo de abajo es el texto del original:
[P8] Prompt 99: el lanzador del experimento de la base del ocho (congelado v2). Juega con el lanzador del experimento (lanzador.una, por taller_v45.una:
reanudable, se salta las partidas que ya tienen fin.json; imagina.json y radar_dia.json al acabar), con el árbol de fruta dulce encendido en los cinco mundos
(como taller_v52), en la carpeta oficial valle_experimento_v2 (nada de pruebas mezcladas). Al acabar cada partida, arbol.json.
En las partidas de RG50r, para P11 (la medida de C5 y C6 del sellado anterior, lanza_confirmacion.py), pregunta en cada decisión qué elegirían los tres
valoradores en ese mismo estado exacto (las mismas fotos y filas de cada candidato, valoradas con el motor, las sumas y la posición), y lo guarda en
<partida>/decisiones.jsonl.gz con la misma fila que entonces:
   [turno, criatura, elige, motor, sumas, posicion, igual_motor, igual_sumas, igual_posicion, hambre > umbral_flaca, bestia vista, hermana a la vista,
    anochecer o noche, mejora]
Lo que cambia frente a lanza_confirmacion (porque RG50r tiene dos reglas de empate más, empate_quedarse_v47 y empate_suertes_v42): «elige» es la opción que
eligió de verdad la criatura (no una copia de su regla); y cada valorador desempata con las reglas de ahora: la de seguir con lo que hacía (empates_sigue_v23),
la de quedarse en un empate exacto, y, si aún empata y la elegida está entre sus empatadas, la elegida (sin tocar los sorteos de la criatura). Preguntar no
cambia ninguna decisión (se comprueba en el modo «prueba»).
   python3 lanza_experimento_v2.py puerta        -> con el árbol apagado, el tonto (normal, 1001) y RG49r (normal+sabores, 9001, 10 días) idénticos a los de antes
   python3 lanza_experimento_v2.py prueba        -> RG50r (normal+sabores con el árbol, 9001, 10 días) con y sin preguntar, idénticas (valle_prueba_v53)
   python3 lanza_experimento_v2.py experimento [procesos=7] -> las 1.400 partidas (7 jugadores × 5 mundos × semillas 30001-30040, 40 días)"""
import gzip, json, os, sys
MODO = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MEDV3_MODO", "rejuega")
os.environ["MEDV3_MODO"] = MODO
os.environ["EXPV2_MODO"] = "experimento"                                   # (el árbol encendido, como en el experimento)
os.environ["TALLER45_CARPETA"] = {"rejuega": "valle_medida_v3_rg50r"}.get(MODO, "valle_prueba_v3_medida")
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); P8 = os.path.dirname(AQUI); sys.path.insert(0, P8)
import lanzador as L
import taller_v40
import taller_v45 as T
import taller_v44 as T44
import cuerpo_valle as CV
CR = L.CFG_M["criaturas"]; SEMILLAS = range(30001, 30041); DIAS = 40
MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian"); CLASES = ("RG50r", "RG050r", "S50", "S050", "P50"); BASE = ("tonto", "recolector")
_md = taller_v40.mundo_de
def mundo_de(nombre):
    m = dict(_md(nombre))
    if os.environ.get("EXPV2_ARBOL", "1") == "1" and os.environ.get("EXPV2_MODO") in ("experimento", "prueba"): m["arbol_dulce"] = {"activo": True}      # el árbol, encendido en todos los mundos
    return m
L.mundo_de = mundo_de; taller_v40.mundo_de = mundo_de

# ── las preguntas a los tres valoradores (solo con PREGUNTA["si"]) ──
PREGUNTA = {"si": False}; CUR = {}; DEC = []; SIN = {"n": 0}
_st = CV.PL.select_tiebreak
def st(nombres, preds, terminal, meta, *a, **k):
    e = _st(nombres, preds, terminal, meta, *a, **k); c = CUR.get("c")
    if PREGUNTA["si"] and c is not None: CUR["ult"] = (list(nombres), preds, meta, c._ult_clave)       # lo que había al decidir (antes de que cambie su clave)
    return e
CV.PL.select_tiebreak = st
_ac = CV.Criatura.actua
def actua(self, obs, info):
    CUR["c"] = self; CUR.pop("ult", None); acc = _ac(self, obs, info)
    if PREGUNTA["si"] and CUR.get("ult") is not None: pregunta(self, acc)
    return acc
CV.Criatura.actua = actua

def desempata(c, nombres, preds, e, ult, elegida):
    """las reglas de empate de ahora, sin tocar los sorteos de la criatura: seguir con lo que hacía; quedarse en un empate exacto; si aún empata y la
    elegida está entre las empatadas, la elegida"""
    if c.empates_sigue_v23 and ult is not None:
        mg_ = 1e-9 if c.empate_margen_v24 is None else c.empate_margen_v24
        tie = [n for n in nombres if abs(preds[n]["d"] - preds[e]["d"]) <= mg_]
        if len(tie) > 1:
            mismo = [n for n in tie if c.clave_accion(preds[n]["acc"]) == ult] or [n for n in tie if preds[n]["acc"]["accion"] == ult[0]]
            if mismo and e not in mismo: e = mismo[0]
    tie = [n for n in nombres if abs(preds[n]["d"] - preds[e]["d"]) <= 1e-9]
    if getattr(c, "empate_quedarse_v47", False):
        tq = [n for n in tie if preds[n]["acc"]["accion"] == "quedarse"]
        if tq and preds[e]["acc"]["accion"] != "quedarse": return tq[0]
    if len(tie) > 1 and elegida in tie: return elegida
    return e

def pregunta(c, acc):
    nombres, preds, meta, ult = CUR["ult"]; f0 = next((n for n in nombres if preds[n]["acc"] is acc), None); casada = 0
    if f0 is None and acc.get("_ir") and not acc.get("_compromiso"):      # (prompt 101, el arreglo) una decisión nueva de ir: actua cambió la opción por un paso
        if acc["_ir"] == "trabajar_planta": f0 = next((n for n in nombres if preds[n]["acc"].get("que") == "trabajar_planta" and preds[n]["acc"].get("planta") == acc.get("planta")), None)
        elif c.dest is not None and c.dest.get("t0") == c.obs["turno"]: f0 = next((n for n in nombres if preds[n]["acc"] == c.dest["acc"]), None)
        if f0 is None: SIN["n"] += 1; return
        casada = 1
    if f0 is None: return                                                  # (lo elegido no salió de las fotos: una llamada en cola o seguir el destino)
    nom = lambda n: preds[n]["acc"].get("que") or preds[n]["acc"]["accion"]; fila = [c.obs["turno"], c.a, nom(f0)]; ig = []; el = [f0]
    VAL = (lambda F: CV.compone(F, c.satura_v8, c.sin_techo_v11), CV.compone_sumas, lambda F: CV.compone_posicion(F, c.satura_v8))
    for val in VAL:
        p2 = {n: dict(preds[n], d=round(val(preds[n]["F"])[1], 9)) for n in nombres}
        f2 = desempata(c, nombres, p2, _st(nombres, p2, {n: p2[n]["d"] for n in nombres}, meta), ult, f0); fila.append(nom(f2)); ig.append(int(f2 == f0)); el.append(f2)
    o = c.obs; pos = {}
    for n in nombres:
        q, _ = CV.compone_sumas(preds[n]["F"]); pos[n] = (q.pF - q.nF, q.pR - q.nR, q.pS - q.nS)
    med = [sum(pos[n][i] for n in nombres) / len(nombres) for i in range(3)]
    mejora = [[round(pos[n][i] - med[i], 4) for i in range(3)] for n in el]
    DEC.append(fila + ig + [int(o["yo"]["hambre"] > CR["umbral_flaca"]), int(c.bestia is not None), int(bool(c.pareja_vista)), int(o["fase"] in ("anochecer", "noche"))] + [mejora] + [casada])

def una(arg, preguntar=None):
    v, mu, s, dias, carpeta = arg; d = os.path.join(carpeta, f"{v}_{mu}_s{s}_d{dias}"); fd = os.path.join(d, "decisiones.jsonl.gz")
    if os.path.exists(os.path.join(d, "fin.json")): return {"id": os.path.basename(d), "saltada": True}
    PREGUNTA["si"] = (v == "RG50r") if preguntar is None else preguntar; DEC.clear(); CUR.clear(); SIN["n"] = 0
    r = T.una(arg); e = L.LOG.get("e")
    if e is not None and getattr(e, "stats_arbol", None): json.dump(e.stats_arbol, open(os.path.join(d, "arbol.json"), "w"), ensure_ascii=False)
    if PREGUNTA["si"]:
        tmp = fd + ".tmp"
        with gzip.open(tmp, "wt", encoding="utf-8") as fh:
            for x in DEC: fh.write(json.dumps(x, ensure_ascii=False) + "\n")
        os.replace(tmp, fd)
    PREGUNTA["si"] = False
    return dict(r, decisiones=len(DEC), de_ir=sum(x[14] for x in DEC), sin_casar=SIN["n"])

OFICIAL = os.path.join(L.T7, "valle_experimento_v2")
def lee_gz(ruta): return gzip.open(ruta, "rt", encoding="utf-8").read().splitlines()

def compara(nombre, carpeta):
    """la partida rejugada frente a la oficial: muertes y criaturas de fin.json; mundo y criaturas línea a línea; decisiones: las nuevas sin las de ir (columna
    15 = 1), y sin esa columna, iguales a las oficiales"""
    a, b = os.path.join(carpeta, nombre), os.path.join(OFICIAL, nombre); fa, fb = json.load(open(os.path.join(a, "fin.json"))), json.load(open(os.path.join(b, "fin.json")))
    out = {"id": nombre, "muertes": fa["muertes"] == fb["muertes"], "criaturas_fin": fa["criaturas"] == fb["criaturas"], "dias": fa["dias"] == fb["dias"],
           "mundo": lee_gz(os.path.join(a, "mundo.jsonl.gz")) == lee_gz(os.path.join(b, "mundo.jsonl.gz")),
           "criaturas": lee_gz(os.path.join(a, "criaturas.jsonl.gz")) == lee_gz(os.path.join(b, "criaturas.jsonl.gz"))}
    nd = [json.loads(l) for l in lee_gz(os.path.join(a, "decisiones.jsonl.gz"))]; od = [json.loads(l) for l in lee_gz(os.path.join(b, "decisiones.jsonl.gz"))]
    out["decisiones_sin_ir_iguales"] = [x[:14] for x in nd if not x[14]] == od; out["decisiones_nuevas"] = len(nd); out["de_ir"] = sum(x[14] for x in nd); out["oficiales"] = len(od)
    out["identica"] = all(out[k] for k in ("muertes", "criaturas_fin", "dias", "mundo", "criaturas", "decisiones_sin_ir_iguales"))
    return out

def prueba(arg):
    preguntar = arg; carp = os.path.join(L.T7, "valle_prueba_v3_medida_" + ("con" if preguntar else "sin")); os.makedirs(carp, exist_ok=True)
    r = una(("RG50r", "normal+sabores", 9001, 10, carp), preguntar=preguntar); return dict(r, preguntar=preguntar, carpeta=carp)

def rejuega(arg):
    r = una(arg); v, mu, s, dias, carpeta = arg; c = compara(f"{v}_{mu}_s{s}_d{dias}", carpeta)
    return dict(c, saltada=r.get("saltada", False), sin_casar=r.get("sin_casar"), segundos=r.get("segundos"))


if __name__ == "__main__":
    if MODO == "prueba":
        with Pool(2) as p: R = p.map(prueba, [True, False])
        n = "RG50r_normal+sabores_s9001_d10"; ca, sa = os.path.join(R[0]["carpeta"], n), os.path.join(R[1]["carpeta"], n)
        out = {"con_preguntas_decisiones": R[0]["decisiones"], "de_ir": R[0]["de_ir"], "sin_casar": R[0]["sin_casar"],
               "mundo_identico_con_y_sin_preguntar": lee_gz(os.path.join(ca, "mundo.jsonl.gz")) == lee_gz(os.path.join(sa, "mundo.jsonl.gz")),
               "criaturas_identico_con_y_sin_preguntar": lee_gz(os.path.join(ca, "criaturas.jsonl.gz")) == lee_gz(os.path.join(sa, "criaturas.jsonl.gz"))}
        v53 = os.path.join(L.T7, "valle_prueba_v53_con", n, "decisiones.jsonl.gz")          # la prueba del prompt 99, con el lanzador original
        if os.path.exists(v53):
            nd = [json.loads(l) for l in lee_gz(os.path.join(ca, "decisiones.jsonl.gz"))]; od = [json.loads(l) for l in lee_gz(v53)]
            out["sin_las_de_ir_iguales_a_las_del_original"] = [x[:14] for x in nd if not x[14]] == od
        print(json.dumps(out, ensure_ascii=False)); json.dump(out, open(os.path.join(AQUI, "prueba_v3.json"), "w"), ensure_ascii=False, indent=1)
    elif MODO == "rejuega":
        npro = int(sys.argv[2]) if len(sys.argv) > 2 else 7; os.makedirs(T.CARPETA, exist_ok=True)
        TR = [("RG50r", mu + "+sabores", s, DIAS, T.CARPETA) for mu in MUNDOS for s in SEMILLAS]; R = []; para = None
        with Pool(npro) as p:
            for r in p.imap_unordered(rejuega, TR):
                R.append(r); print(json.dumps({k: r[k] for k in ("id", "identica", "decisiones_nuevas", "de_ir", "oficiales", "sin_casar", "segundos")}, ensure_ascii=False), flush=True)
                if not r["identica"]: para = r; p.terminate(); break
        out = {"jugadas": len(R), "identicas": sum(r["identica"] for r in R), "para": para, "partidas": R}
        json.dump(out, open(os.path.join(AQUI, "rejuega_v3.json"), "w"), ensure_ascii=False, indent=1)
        print(json.dumps({k: out[k] for k in ("jugadas", "identicas", "para")}, ensure_ascii=False), flush=True)
