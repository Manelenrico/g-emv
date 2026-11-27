"""[P8] Prompt 149 (preparado, NO lanzado): el lanzador del experimento v6, el de la reserva y la voz. Es lanza_experimento_v5.py (prompt 134) con los jugadores,
las semillas y la carpeta nuevos, y los mismos registros. Seis jugadores: el tonto, el recolector, RG68r y RG068r (como en el v5), RG69r (la reserva, prompt 146:
cuerpo_rg69.RG69) y la protagonista RG69r+voz (la reserva y la voz de ir a casa, prompt 147: cuerpo_vr1.RG69V; en las carpetas «RG69rvoz», porque allí el «+»
separa el mundo de los sabores). Cinco mundos con el árbol, semillas 30161-30200, 40 días: 6 × 5 × 40 = 1.200 partidas, en la carpeta oficial valle_experimento_v6.
CÓMO JUEGA (sin código nuevo de criatura): con el lanzador de la medida del prompt 101 (medida_v3/lanza_medida_v3.una, como el v5) y los registros del v5
(lanza_experimento_v5: REG, el balance y las filas de cada turno, el cuaderno de sitios). Lo que la voz necesita del mundo después de cada paso lo pone el
lanzador de la voz del 143 (lanza_vc1, importado: dónde está cada criatura, si duerme, si está muerta; solo se lee). Durante una partida de RG69r o RG69r+voz,
CV.Criatura se cambia por su clase y se vuelve a poner al acabar (como los lanzadores de los talleres 146 y 147).
LOS REGISTROS:
  - en las cuatro clases de criatura, por criatura y turno: balance.jsonl.gz y filas.jsonl.gz (los del v5); al acabar, cuaderno_sitios.json y cuenta_v61.json;
  - en la protagonista, el registro de decisiones con las de ir (decisiones.jsonl.gz, preguntar=True: para M9, la antigua P11). En el v5 era RG68r;
  - en RG69r y RG69r+voz, al acabar, reserva_v69.json (cuántas fotos de comer usaron la reserva, por criatura); en RG69r+voz, voz_vc1.json (las voces, las
    decisiones oyendo y las cuentas, como el 143: para M12).
  P24, P27, P28 y M11 a M13 se miden con lo que ya escriben el mundo y el lanzador (mundo.jsonl.gz, criaturas.jsonl.gz, balance.jsonl.gz, fin.json) más voz_vc1.json.
   python3 lanza_experimento_v6.py puerta    -> salida/puerta_experimento_v6.json: con este código y sin los registros, partidas de 40 días, sequía dura 30121,
        línea a línea (muertes, criaturas al acabar, mundo y criaturas): el tonto, el recolector, RG68r y RG068r frente a las del v5; RG69r con la reserva
        apagada (RG69off) frente a RG68r del v5; RG69r+voz con la voz apagada (RG69voff) frente a RG69r del taller del 146; y, además, RG69r y RG69r+voz
        encendidas frente a las de los talleres del 146 y del 147
   python3 lanza_experimento_v6.py prueba    -> salida/prueba_experimento_v6.json: RG69r+voz (normal, 9101) y RG69r (bestias que crían, 9102), 10 días, con y
        sin apuntar: idénticas, y con los registros escritos
   python3 lanza_experimento_v6.py experimento [procesos=10] -> las 1.200 partidas, en la carpeta oficial valle_experimento_v6"""
import gzip, json, os, sys
MODO = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].isdigit() else "experimento"
os.environ["MEDV3_MODO"] = "prueba"                                            # (como el v5: lanza_medida_v3 lee de aquí su carpeta por defecto, que no se usa)
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import lanza_vc1 as LV                                                          # (importa lanza_experimento_v5 y pone lo que la voz necesita del mundo)
import cuerpo_rg69 as RZ
import cuerpo_vr1 as ZV
L5 = LV.L5; LM = LV.LM; L = LV.L; CV = LV.CV; B7 = LV.B7; T7 = LV.T7
B7.VARS["RG69r"] = dict(B7.VARS["RG68r"], reserva_v69=True); B7.VARS["RG69rvoz"] = dict(B7.VARS["RG68r"], reserva_v69=True, a_casa=True)
B7.VARS["RG69off"] = dict(B7.VARS["RG68r"], reserva_v69=False); B7.VARS["RG69voff"] = dict(B7.VARS["RG68r"], reserva_v69=True, a_casa=False)     # (las de las puertas)
CLASE = {"RG69r": RZ.RG69, "RG69off": RZ.RG69, "RG69rvoz": ZV.RG69V, "RG69voff": ZV.RG69V}
PROTA = "RG69rvoz"; CRIATURAS = ("RG68r", "RG068r", "RG69r", "RG69rvoz"); BASE = ("tonto", "recolector"); MUNDOS = L5.MUNDOS
L5.CRIATURAS = tuple(L5.CRIATURAS) + tuple(v for v in CRIATURAS + tuple(CLASE) if v not in L5.CRIATURAS)
SEMILLAS = range(30161, 30201); DIAS = 40; OFICIAL = os.path.join(T7, "valle_experimento_v6")
V5 = os.path.join(T7, "valle_experimento_v5"); T146 = os.path.join(T7, "valle_rg69_taller"); T147 = os.path.join(T7, "valle_vr1_taller")

def una(arg, apuntar=True):
    """lanza_experimento_v5.una con la clase de cada jugador y el registro de decisiones en la protagonista"""
    v, mu, s, dias, carpeta = arg; d = os.path.join(carpeta, f"{v}_{mu}_s{s}_d{dias}"); R = L5.REG
    if os.path.exists(os.path.join(d, "fin.json")): return {"id": os.path.basename(d), "saltada": True}
    os.makedirs(d, exist_ok=True); cri = v in L5.CRIATURAS or v.startswith("RG"); viejo = CV.Criatura
    if v in CLASE: CV.Criatura = CLASE[v]
    R["si"] = apuntar and cri
    R["fh"] = gzip.open(os.path.join(d, "balance.jsonl.gz"), "wt", encoding="utf-8") if R["si"] else None
    R["ff"] = gzip.open(os.path.join(d, "filas.jsonl.gz"), "wt", encoding="utf-8") if R["si"] else None
    try: r = LM.una(arg, preguntar=(apuntar and v == PROTA))
    finally:
        CV.Criatura = viejo
        for k in ("fh", "ff"):
            if R[k] is not None: R[k].close()
            R[k] = None
        R["si"] = False
    if apuntar and cri and not r.get("saltada"):
        L5.cuaderno_sitios(d)
        json.dump({a: getattr(c, "cuenta_v61", None) for a, c in L.CRI.items()}, open(os.path.join(d, "cuenta_v61.json"), "w"), ensure_ascii=False)
        if any(isinstance(c, RZ.RG69) for c in L.CRI.values()):
            json.dump({a: c.cuenta_v69 for a, c in sorted(L.CRI.items()) if isinstance(c, RZ.RG69)}, open(os.path.join(d, "reserva_v69.json"), "w"))
        if any(isinstance(c, LV.Z.VC1) for c in L.CRI.values()):
            json.dump({a: {"voces": c.vc_voces, "oye": c.vc_oye, "cuenta": c.vc_cuenta} for a, c in sorted(L.CRI.items()) if isinstance(c, LV.Z.VC1)},
                      open(os.path.join(d, "voz_vc1.json"), "w"), ensure_ascii=False)
    return dict(r, id=os.path.basename(d))

def puerta(x):
    v, mu, s, ref, vref = x; carp = os.path.join(T7, "valle_experimento_v6_puerta"); os.makedirs(carp, exist_ok=True); n = f"{v}_{mu}_s{s}_d40"
    una((v, mu, s, 40, carp), apuntar=False); nr = f"{vref}_{mu}_s{s}_d40"
    return dict(L5.iguales(os.path.join(carp, n), os.path.join(ref, nr)), id=n, frente_a=os.path.relpath(os.path.join(ref, nr), T7))

def prueba(x):
    v, mu, s, ap = x; carp = os.path.join(T7, "valle_experimento_v6_prueba_" + ("con" if ap else "sin")); os.makedirs(carp, exist_ok=True)
    return dict(una((v, mu, s, 10, carp), apuntar=ap), carpeta=carp, apunta=ap, v=v, mu=mu, s=s)


if __name__ == "__main__":
    os.makedirs(os.path.join(AQUI, "salida"), exist_ok=True)
    if MODO == "puerta":
        SD, SDs = "sequia_dura", "sequia_dura+sabores"
        P = [("tonto", SD, 30121, V5, "tonto"), ("recolector", SD, 30121, V5, "recolector"), ("RG68r", SDs, 30121, V5, "RG68r"), ("RG068r", SDs, 30121, V5, "RG068r"),
             ("RG69off", SDs, 30121, V5, "RG68r"), ("RG69voff", SDs, 30121, T146, "RG69r"), ("RG69r", SDs, 30121, T146, "RG69r"), ("RG69rvoz", SDs, 30121, T147, "RG69rvoz")]
        with Pool(len(P), maxtasksperchild=1) as p: R = p.map(puerta, P)
        out = {"identicas": sum(r["identica"] for r in R), "de": len(R), "partidas": R}
        json.dump(out, open(os.path.join(AQUI, "salida", "puerta_experimento_v6.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
    elif MODO == "prueba":
        P = [(PROTA, "normal+sabores", 9101), ("RG69r", "bestias_crian+sabores", 9102)]
        with Pool(4, maxtasksperchild=1) as p: R = p.map(prueba, [x + (ap,) for x in P for ap in (True, False)])
        out = []
        for v, mu, s in P:
            con = next(r for r in R if r["v"] == v and r["apunta"]); sin = next(r for r in R if r["v"] == v and not r["apunta"]); n = f"{v}_{mu}_s{s}_d10"
            a = os.path.join(con["carpeta"], n)
            out.append(dict(L5.iguales(a, os.path.join(sin["carpeta"], n)), id=n, **{f: os.path.exists(os.path.join(a, f)) for f in
                            ("decisiones.jsonl.gz", "balance.jsonl.gz", "filas.jsonl.gz", "cuaderno_sitios.json", "cuenta_v61.json", "reserva_v69.json", "voz_vc1.json")}))
        json.dump(out, open(os.path.join(AQUI, "salida", "prueba_experimento_v6.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        npro = int(sys.argv[2]) if len(sys.argv) > 2 else 10; os.makedirs(OFICIAL, exist_ok=True)
        TR = [(v, mu, s, DIAS, OFICIAL) for mu in MUNDOS for v in BASE for s in SEMILLAS]
        TR += [(v, mu + "+sabores", s, DIAS, OFICIAL) for mu in MUNDOS for v in CRIATURAS for s in SEMILLAS]
        with Pool(npro, maxtasksperchild=1) as p:
            for r in p.imap_unordered(una, TR): print(json.dumps({k: r[k] for k in ("id", "saltada", "decisiones") if k in r}, ensure_ascii=False), flush=True)
