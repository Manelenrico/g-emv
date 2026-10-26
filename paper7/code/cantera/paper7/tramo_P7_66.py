"""[P7-66, segundo banco] ¿HASTA QUE TIC HAY CALMA LEJOS DEL CENTRO? (coste cero) Diarios de P7-65 (240 vidas): por tramos de 100 tics desde el inicio, fraccion de vidas vivas que estan
a mas de 6 casillas del centro (24, 24) y en calma (ningun rival a <= 5 casillas ni golpe en 48 tics), y su distancia media al centro. python3 tramo_P7_66.py -> P7_66_tramo.json"""
import collections, glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "paintball", "runs")
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
viv = collections.Counter(); lejos = collections.Counter(); lejos_calma = collections.Counter(); dist = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(RUNS, "P765_s*_d*_*", "*policy_agent_1[01].art.log"))):
    sl = int(f.split("agent_")[1].split(".")[0]); golpe = -999
    for l in open(f, errors="replace"):
        if not l.startswith('{"k":"tick"'): continue
        r = json.loads(l)
        if r.get("phase") != "live": continue
        t = r["tick"]
        if t > 3000: break
        pos = tuple(r.get("pos") or (0, 0))
        if any(float(x.get("amount") or 0) > 0 for x in (r.get("damage_taken") or [])): golpe = t
        riv = [cheb(pos, tuple(a["pos"])) for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("slot") not in (sl, sl ^ 1)]
        c = not (riv and min(riv) <= 5) and t - golpe > 48; b = t // 100; d = cheb(pos, (24, 24))
        viv[b] += 1; dist[b].append(d)
        if d > 6: lejos[b] += 1; lejos_calma[b] += c
R = {f"{b * 100}-{b * 100 + 99}": {"lejos_del_centro": round(lejos[b] / viv[b], 3), "lejos_y_en_calma": round(lejos_calma[b] / viv[b], 3), "distancia_media_al_centro": round(st.mean(dist[b]), 1)} for b in sorted(viv)}
json.dump(R, open(os.path.join(AQUI, "P7_66_tramo.json"), "w"), ensure_ascii=False, indent=1)
for k, v in R.items(): print(k, v)
