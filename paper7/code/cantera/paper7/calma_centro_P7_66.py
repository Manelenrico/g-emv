"""[P7-66] ¿CUANTA CALMA HAY CERCA DEL CENTRO? (banco, coste cero) Sobre los diarios de P7-65 (240 vidas): calma = ningun rival visible a <= 5 casillas (ni ella ni su hermana) y ningun
golpe en los 48 tics anteriores (la de invita_P7_66). Por vida: tics vivos, tics en calma, tics en calma a <= 6 casillas del centro (24, 24), y tramos de calma seguidos que pasan por esa
zona. python3 calma_centro_P7_66.py -> P7_66_calma_centro.json"""
import glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "paintball", "runs")
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
V = []
for f in sorted(glob.glob(os.path.join(RUNS, "P765_s*_d*_*", "*policy_agent_1[01].art.log"))):
    sl = int(f.split("agent_")[1].split(".")[0]); viv = calma = cc = cerca = 0; golpe = -999; tramos = 0; en = False
    for l in open(f, errors="replace"):
        if not l.startswith('{"k":"tick"'): continue
        r = json.loads(l)
        if r.get("phase") != "live": continue
        t = r["tick"]; pos = tuple(r.get("pos") or (0, 0)); viv += 1
        if any(float(x.get("amount") or 0) > 0 for x in (r.get("damage_taken") or [])): golpe = t
        riv = [cheb(pos, tuple(a["pos"])) for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("slot") not in (sl, sl ^ 1)]
        c = not (riv and min(riv) <= 5) and t - golpe > 48; z = cheb(pos, (24, 24)) <= 6; cerca += z
        if c: calma += 1
        if c and z:
            cc += 1
            if not en: tramos += 1; en = True
        else: en = False
    V.append({"vivos": viv, "calma": calma, "cerca_del_centro": cerca, "calma_cerca_del_centro": cc, "tramos_calma_cerca": tramos})
R = {"vidas": len(V),
     "fraccion_de_la_vida_cerca_del_centro": round(st.median([v["cerca_del_centro"] / v["vivos"] for v in V if v["vivos"]]), 3),
     "fraccion_de_la_calma_que_es_cerca_del_centro": round(sum(v["calma_cerca_del_centro"] for v in V) / sum(v["calma"] for v in V), 3),
     "fraccion_del_tiempo_cerca_del_centro_que_es_calma": round(sum(v["calma_cerca_del_centro"] for v in V) / max(1, sum(v["cerca_del_centro"] for v in V)), 3),
     "tics_de_calma_cerca_del_centro_por_vida_mediana": st.median([v["calma_cerca_del_centro"] for v in V]),
     "vidas_sin_calma_cerca_del_centro": sum(1 for v in V if v["calma_cerca_del_centro"] == 0),
     "tramos_de_calma_cerca_del_centro_por_vida_mediana": st.median([v["tramos_calma_cerca"] for v in V])}
json.dump(R, open(os.path.join(AQUI, "P7_66_calma_centro.json"), "w"), ensure_ascii=False, indent=1); print(R)
