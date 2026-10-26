"""11 · El umbral de 5 de P7-55 (analiza_P7_55.py:5-6,59-60): que variable mide, que son los 120 y de donde salen el 4,1 y el 4,7.
Ejecuta las funciones del analisis sellado (recuerdos, dedup, creencia) sobre los cuadernos de P7-50 sin su escritura. Solo lectura."""
import json, os
from comun import P7
src = open(os.path.join(P7, "analiza_P7_55.py")).read().replace("os.path.dirname(os.path.abspath(__file__))", repr(P7))
ns = {"__name__": "analiza_P7_55_revision"}; exec(src[:src.index("\nR = {")], ns)
cuaderno, recuerdos, dedup, creencia, OLVIDO, PESO_NEUTRO = ns["cuaderno"], ns["recuerdos"], ns["dedup"], ns["creencia"], ns["OLVIDO"], ns["PESO_NEUTRO"]
D = json.load(open(os.path.join(P7, "P7_55_datos.json")))["por_dia"]
print("hermanas", sorted(D), "| dias por hermana", {h: len(v) for h, v in D.items()}, "| hermana-dias", sum(len(v) for v in D.values()))
print("comprobaciones: red y camuflaje (umbral 5)", 2 * sum(len(v) for v in D.values()), "; botiquin y racion (umbral 0)", 2 * sum(len(v) for v in D.values()))
for o in ("red", "camuflaje"):
    aa = [(x[o]["a_todos_dedup"] or 0) for v in D.values() for x in v]; print(o, "a maxima en los 120", round(max(aa), 2), "| hermana-dias con a > 0", sum(1 for a in aa if a > 0))
for S, sl, d, o, nom in ((1, 10, 16, "camouflage", "camuflaje"), (2, 10, 16, "net", "red")):
    c = cuaderno(S, d, "COMPARTE", sl); recs, _ = dedup(recuerdos(c)); dia = d + 1
    a = creencia(recs, o, dia); b = creencia(recs, o, dia, lambda r: r.get("origen", "vivido") == "vivido")
    print(f"\ns{S} a{sl}, cuaderno del dia {d}, {nom}: a = {a:.2f}  b = {b if b is None else round(b, 2)}  (creencia en puntos de vida, situacion 'dentro')")
    num = 0.0; den = PESO_NEUTRO
    print("   recuerdo neutro: peso 1,00, efecto 0")
    for r in recs:
        if r["_obj"] != o or r["_sit"] != "dentro" or r.get("corte"): continue
        w = float(r["intensidad"]) * (OLVIDO ** max(0, dia - int(r["dia"])))
        print(f"   {r.get('origen', 'vivido'):8s} dia {r['dia']:>2}  efecto cuerpo {float(r['efecto']['cuerpo']):6.2f}  peso {w:.2f}" + ("  (al menos)" if r.get("al_menos") else ""))
        if not r.get("al_menos"): num += w * float(r["efecto"]["cuerpo"]); den += w
    print(f"   media ponderada = {num:.2f} / {den:.2f} = {num / den:.2f}")
