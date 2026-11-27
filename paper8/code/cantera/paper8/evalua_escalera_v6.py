"""[P8] Prompt 152: la evaluación de la escalera con la reserva. RG69r+voz (la protagonista del v6, leída de valle_experimento_v6 sellado, sin volver a
jugarla) frente a S69+voz y P69+voz (valle_escalera_v6, de lanza_escalera_v6.py): cinco mundos, semillas 30161-30200, 40 días. Solo lee.
LAS PIEZAS, importadas del evaluador sellado del v6 (evalua_experimento_v6, modo «experimento», sin tocarlo), con las carpetas de los jugadores nuevos añadidas:
  - c46 (cierre_v46): las vivas el día 40 (8 menos las muertes de fin.json), las muertes por causa y los empujones a otra criatura (como P16);
  - v5m (evalua_experimento_v5.v5): la felicidad de la aldea (como P26);
  - nuevas: los turnos al día despierta con hambre > 30 y comida en la bolsa, días 0 a 9 (extrae_hg_v1, como P24) y las noches dormidas fuera, días 0 a 9
    (analiza_vc1, como P28; aquí, por partida: las noches fuera entre las noches);
  - boot: bootstrap de 10.000 remuestreos con semilla 8 (evalua_experimento_v5.boot, el mismo que motor_frente_simple_v5.py).
LAS PREDICCIONES (predicciones_selladas_v6_escalera.md):
  E1: vivas el día 40 de RG69r+voz − S69+voz, emparejadas por mundo y semilla, los cinco mundos juntos (las 200 parejas, en el orden de motor_frente_simple_v5:
      mundo y, dentro, semilla): se cumple si el límite de abajo del intervalo del 95 % es > 0.
  E2: lo mismo, solo en la sequía (40 parejas): límite de abajo > 0.
  Sin predicción, medido igual: RG69r+voz − P69+voz (los cinco juntos y la sequía); por mundo, las medidas del punto 5 del prompt 152 frente a S69+voz y a P69+voz;
  y las muertes por causa de los tres.
   python3 evalua_escalera_v6.py           -> salida/evalua_escalera_v6.md y .json
   python3 evalua_escalera_v6.py prueba    -> (antes de sellar, para ver que el programa corre de principio a fin) lo mismo sobre partidas ya selladas del v6,
        RG68r con el nombre S69voz y RG068r con el nombre P69voz (enlaces en evalua_escalera_v6/prueba/enlaces), semillas 30161-30163
        -> salida/evalua_escalera_v6_prueba.md: esos números no son de los jugadores nuevos y no se miran"""
import json, os, sys
from collections import Counter
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
MODO = os.environ.get("ESCALERA_MODO") or ("prueba" if len(sys.argv) > 1 and sys.argv[1] == "prueba" else "experimento"); os.environ["ESCALERA_MODO"] = MODO
sys.argv[1:] = []                                                               # (el modo «experimento» del evaluador del v6)
import evalua_experimento_v6 as E6
T7, MUNDOS, boot, nom0 = E6.T7, E6.MUNDOS, E6.boot, E6.nom
assert tuple(MUNDOS) == ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian")       # (el orden de motor_frente_simple_v5)
PROTA = "RG69rvoz"; NUEVOS = ("S69voz", "P69voz"); JUG = (PROTA,) + NUEVOS
NOM = {"RG69rvoz": "RG69r+voz", "S69voz": "S69+voz", "P69voz": "P69+voz"}; nom = lambda v: NOM.get(v, nom0(v))
CACHE = os.path.join(AQUI, "evalua_escalera_v6", MODO)
for d_ in ("partidas", "noches", "datos"): os.makedirs(os.path.join(CACHE, d_), exist_ok=True)
if MODO == "experimento":
    ESC = os.path.join(T7, "valle_escalera_v6"); SEM = range(30161, 30201); SAL = "evalua_escalera_v6"
else:
    ESC = os.path.join(CACHE, "enlaces"); SEM = range(30161, 30164); SAL = "evalua_escalera_v6_prueba"; os.makedirs(ESC, exist_ok=True)
    for v, de in (("S69voz", "RG68r"), ("P69voz", "RG068r")):
        for mu in MUNDOS:
            for s in SEM:
                n = os.path.join(ESC, f"{v}_{mu}+sabores_s{s}_d40")
                if not os.path.lexists(n): os.symlink(os.path.join(E6.EXP, f"{de}_{mu}+sabores_s{s}_d40"), n)
E6.CARPETA.update({v: ESC for v in NUEVOS}); E6.AN.CARP.update({v: (ESC, v) for v in NUEVOS})
E6.AN.OUT = os.path.join(CACHE, "partidas"); E6.AN.AQUI = CACHE; E6.X.AQUI = CACHE

def una(x):
    v, mu, s = x; c = E6.c46(x); f = E6.v5m(x); n = E6.nuevas(x); nf, nt = n["noches10"]
    return {"v": v, "mu": mu, "s": s, "vivas": c["vivas"], "causas": c["causas"], "hambre": c["causas"].get("hambre", 0), "empujones": c["C"].get("empujar", 0),
            "feliz": f["feliz_aldea"], "h30_bolsa": n["h30_bolsa"], "noches10": nf / nt if nt else None, "noches10_n": [nf, nt]}


if __name__ == "__main__":
    T = [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM]
    falta = [x for x in T if not E6.hecho(*x)]
    if falta: sys.exit(f"faltan {len(falta)} partidas, por ejemplo {falta[:3]}")
    with Pool(10) as p: R = {(r["v"], r["mu"], r["s"]): r for r in p.map(una, T, chunksize=2)}
    f2 = lambda b: f"{b['media']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}]"; f3 = lambda b: f"{b['media']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}]"
    def par(a, b, mus, k):
        return [R[(a, mu, s)][k] - R[(b, mu, s)][k] for mu in mus for s in SEM if R[(a, mu, s)][k] is not None and R[(b, mu, s)][k] is not None]
    OUT = {"modo": MODO, "semillas": [SEM.start, SEM.stop - 1]}; w = [f"# La escalera con la reserva (v6): la evaluación ({'el experimento' if MODO == 'experimento' else 'PRUEBA del programa, con partidas que no son de los jugadores nuevos'})\n",
                                                                     f"Partidas leídas: " + ", ".join(f"{nom(v)} {sum(1 for k in R if k[0] == v)}" for v in JUG) + ".\n"]
    w.append("## Las predicciones\n")
    for k, mus, txt in (("E1", MUNDOS, "los cinco mundos juntos"), ("E2", ("sequia",), "la sequía")):
        b = boot(par(PROTA, "S69voz", mus, "vivas")); ok = b["lo"] > 0; OUT[k] = dict(b, cumple=ok)
        w.append(f"**{k}** ({'SE CUMPLE' if ok else 'FALLA'}). Vivas el día 40, RG69r+voz − S69+voz, {txt} ({b['n']} parejas): {f2(b)}. Se cumple si el límite de abajo es > 0.\n")
    w.append("**Cuentan 2; se cumplen " + str(sum(OUT[k]["cumple"] for k in ("E1", "E2"))) + ".**\n")
    w.append("## Lo declarado, medido igual (sin predicción)\n")
    for k, mus, txt in (("P_cinco", MUNDOS, "los cinco mundos juntos"), ("P_sequia", ("sequia",), "la sequía")):
        b = boot(par(PROTA, "P69voz", mus, "vivas")); OUT[k] = b; w.append(f"- Vivas el día 40, RG69r+voz − P69+voz, {txt} ({b['n']} parejas): {f2(b)}.")
    w.append("- (El efecto del v5, RG68r − S68 en los cinco juntos, sobre la base vieja: +0,41 [+0,27, +0,57], de motor_frente_simple_v5.md.)\n")
    w += ["## Vivas el día 40 (de 8; media de las semillas)\n", "| mundo | " + " | ".join(nom(v) for v in JUG) + " |", "|---|---|---|---|"]
    for mu in MUNDOS + ("los cinco",):
        ms = MUNDOS if mu == "los cinco" else (mu,)
        w.append(f"| {mu} | " + " | ".join(f"{sum(R[(v, m, s)]['vivas'] for m in ms for s in SEM) / (len(ms) * len(SEM)):.2f}" for v in JUG) + " |")
    MED = (("vivas el día 40", "vivas", f2), ("muertes de hambre por partida", "hambre", f2), ("turnos al día con hambre > 30 y comida en la bolsa, días 0 a 9", "h30_bolsa", f2),
           ("noches dormidas fuera, días 0 a 9 (parte de las noches, por partida)", "noches10", f3), ("empujones a otra criatura por partida", "empujones", f2),
           ("felicidad de la aldea", "feliz", f3))
    w.append("\n## Las medidas sin predicción, por mundo (emparejadas por semilla)\n")
    OUT["medidas"] = {}
    for tit, k, ff in MED:
        w += [f"**{tit}**\n", "| mundo | RG69r+voz · S69+voz · P69+voz (medias) | RG69r+voz − S69+voz | RG69r+voz − P69+voz |", "|---|---|---|---|"]
        for mu in MUNDOS:
            mm = lambda v: (lambda L: sum(L) / len(L) if L else float("nan"))([R[(v, mu, s)][k] for s in SEM if R[(v, mu, s)][k] is not None])
            bs, bp = boot(par(PROTA, "S69voz", (mu,), k)), boot(par(PROTA, "P69voz", (mu,), k)); OUT["medidas"][f"{k}|{mu}"] = {"S": bs, "P": bp, "medias": [mm(v) for v in JUG]}
            dec = 3 if ff is f3 else 2
            w.append(f"| {mu} | " + " · ".join(f"{mm(v):.{dec}f}" for v in JUG) + f" | {ff(bs)} | {ff(bp)} |")
        w.append("")
    causas = sorted({c for r in R.values() for c in r["causas"]})
    w += ["## Muertes por causa (" + " · ".join(causas) + "), sumadas en las partidas de cada mundo\n", "| mundo | " + " | ".join(nom(v) for v in JUG) + " |", "|---|---|---|---|"]
    OUT["causas"] = {}
    for mu in MUNDOS + ("los cinco",):
        ms = MUNDOS if mu == "los cinco" else (mu,); cel = []
        for v in JUG:
            c = Counter()
            for m in ms:
                for s in SEM: c.update(R[(v, m, s)]["causas"])
            OUT["causas"][f"{v}|{mu}"] = dict(c); cel.append(" · ".join(str(c.get(x, 0)) for x in causas))
        w.append(f"| {mu} | " + " | ".join(cel) + " |")
    open(os.path.join(AQUI, "salida", SAL + ".md"), "w").write("\n".join(w) + "\n")
    json.dump(OUT, open(os.path.join(AQUI, "salida", SAL + ".json"), "w"), ensure_ascii=False, indent=1)
    print(f"escrito salida/{SAL}.md ({len(R)} partidas)")
