"""1b (P7-65 L1), 1d (confianza final P7-67) y 1e (escala propia - formula antigua) con otras unidades. Lee solo JSON sellados."""
import json, math, os, statistics as st
from comun import P7
def me(xs): return (st.mean(xs), st.stdev(xs) / math.sqrt(len(xs)), len(xs))
# (b) P7-65 L1: 9 criaturas -> 6 cadenas de partidas (serie, brazo) -> 3 series
L = json.load(open(os.path.join(P7, "P7_65_sello.json")))["principal"]["L1"]["criaturas"]
v = {k: x["media"] for k, x in L.items()}
m, e, n = me(list(v.values())); print("b criatura      ", round(m, 4), round(e, 4), n, round(m / e, 1))
par = {}
for k, x in v.items(): s, b, h = k.split(); par.setdefault((s, b), []).append(x)
m, e, n = me([st.mean(x) for x in par.values()]); print("b cadena/partida", round(m, 4), round(e, 4), n, round(m / e, 1))
ser = {}
for k, x in v.items(): ser.setdefault(k.split()[0], []).append(x)
m, e, n = me([st.mean(x) for x in ser.values()]); print("b serie         ", round(m, 4), round(e, 4), n, round(m / e, 1))
# (d) P7-67 campo, nivel 1, dia 20: confianza de arranque (recursos) por serie
A = json.load(open(os.path.join(P7, "P7_67_analisis.json")))
CD = [c for c in A["criatura_dias_detalle"] if c["nivel"] == "1" and c["dia"] == 20 and c["conf_arranque"]]
S = {}
for c in CD: S.setdefault(c["brazo"], {}).setdefault(c["serie"], []).append(float(c["conf_arranque"]["recursos"]))
for b in S: print("d", b, "criaturas", tuple(round(x, 4) for x in me([x for v_ in S[b].values() for x in v_])), "series", tuple(round(x, 4) for x in me([st.mean(v_) for v_ in S[b].values()])))
H = {s: st.mean(v_) for s, v_ in S["HONESTA"].items()}; M = {s: st.mean(v_) for s, v_ in S["MIENTE"].items()}
mh, eh, _ = me(list(H.values())); mm, em, _ = me(list(M.values())); d = mh - mm; e = math.hypot(eh, em)
print("d HONESTA-MIENTE por serie, sin emparejar", round(d, 4), round(e, 4), round(d / e, 1))
m, e, n = me([H[s] - M[s] for s in H if s in M]); print("d emparejado por serie", round(m, 4), round(e, 4), n, round(m / e, 1))
print("d parejas de hermanas con la misma confianza", {b: sum(1 for v_ in S[b].values() if len(set(v_)) == 1) for b in S})
# (e) figuras/informe_P7_figuras.md:176 -> por serie (variante + serie; a10 y a11 de la misma serie se promedian)
PC = json.load(open(os.path.join(P7, "figuras", "figuras_P7_valores.json")))["fig3_1_intensidades_11_17"]["por_criatura"]
m, e, n = me([x["dif_media"] for x in PC.values()]); print("e criatura", round(m, 2), round(e, 2), n, round(m / e, 1))
G = {}
for k, x in PC.items(): G.setdefault(" ".join(k.split()[:2]), []).append(x["dif_media"])
m, e, n = me([st.mean(x) for x in G.values()]); print("e serie", round(m, 2), round(e, 2), n, round(m / e, 1), sorted(G))
