"""[P7-5] Correccion 1 de la mesa sobre el calculo en seco de P7-4: lo esperado sin la cosa resta SOLO el dano de causas que el cuerpo
conoce (anillo estando fuera del circulo; golpes de rivales a la vista y en alcance de su arma, mano vacia = 1). Compara, uso a uso, el
efecto del cuerpo con la regla de P7-4 (todo el dano observado) y con esta, y cuenta cuantos cambian. -> P7_5_huella.json"""
import collections, glob, json, math, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..")); VENT = 49
H = json.load(open(os.path.join(AQUI, "P7_4_huella.json")))["usos"]; H = [h for h in H if "descartado" not in h]
por = collections.defaultdict(list)
for h in H: por[h["vida"]].append(h)
OUT = []
for vida, hs in por.items():
    carp, slot = vida.split("/"); f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]
    quiero = {u: h["t"] for h in hs for u in range(h["t"], h["t"] + VENT + 1)}; T = {}; cat = None
    for line in open(f):
        if '"catalogo"' in line[:30]: cat = {c["id"]: c for c in json.loads(line)["items"]}
        if '"tick"' not in line[:60]: continue
        r = json.loads(line)
        if r.get("k") == "tick" and r["tick"] in quiero: T[r["tick"]] = r
    for h in hs:
        t = h["t"]; conocido = 0.0; total = 0.0; desc = collections.Counter()
        for u in range(t + 1, t + VENT + 1):
            r = T.get(u)
            if r is None: continue
            pos = r["pos"]; z = r["zona"]; fuera = math.dist(pos, z["center"]) > z["radius"]
            ag = {a["slot"]: a for a in (r.get("ve_agentes") or []) if a.get("pos")}
            for d in (r.get("damage_taken") or []):
                src = str(d.get("source") or ""); amt = float(d.get("amount") or 0); total += amt
                if src == "zone":
                    if fuera: conocido += amt; desc["anillo fuera"] += amt
                    else: desc["anillo estando dentro (no conocido)"] += amt
                elif src.startswith("P"):
                    a = ag.get(int(src[1:])) if src[1:].isdigit() else None
                    if a is None: desc["rival no visto (no conocido)"] += amt; continue
                    hid = a.get("hand") if isinstance(a.get("hand"), str) else (a.get("hand") or {}).get("id"); it = cat.get(hid) if (cat and hid) else None
                    alc = int(it["range"]) if it else 1
                    if max(abs(a["pos"][0] - pos[0]), abs(a["pos"][1] - pos[1])) <= alc: conocido += amt; desc["rival visto en alcance"] += amt
                    else: desc["rival visto fuera de alcance (no conocido)"] += amt
                else: desc[src + " (no conocido)"] += amt
        bruto = h["cuerpo"]["bruto"]; e4 = h["cuerpo"]["efecto"]; e5 = bruto + conocido
        OUT.append({"vida": vida, "t": t, "resultado": h["resultado"], "dentro": h["dentro"], "bruto": bruto, "dano_total": round(total, 2), "dano_conocido": round(conocido, 2), "efecto_P7_4": e4, "efecto_P7_5": round(e5, 2), "cambia": abs(e5 - e4) > 0.005, "desglose": {k: round(v, 2) for k, v in desc.items()}})
V = OUT; camb = [o for o in V if o["cambia"]]
def q(v, p):
    v = sorted(v); k = (len(v) - 1) * p; i = int(k); return round(v[i] + (v[min(i + 1, len(v) - 1)] - v[i]) * (k - i), 2) if v else None
R = {"usos": len(V), "cambian": len(camb), "por_resultado": {res: {"n": sum(1 for o in V if o["resultado"] == res), "cambian": sum(1 for o in camb if o["resultado"] == res), "efecto_P7_5_mediana": q([o["efecto_P7_5"] for o in V if o["resultado"] == res], .5), "efecto_P7_5_p10": q([o["efecto_P7_5"] for o in V if o["resultado"] == res], .1), "efecto_P7_5_p90": q([o["efecto_P7_5"] for o in V if o["resultado"] == res], .9)} for res in ("completado", "cancelado")},
     "diferencia_en_los_que_cambian": {"mediana": q([o["efecto_P7_5"] - o["efecto_P7_4"] for o in camb], .5), "min": (min(o["efecto_P7_5"] - o["efecto_P7_4"] for o in camb) if camb else None), "max": (max(o["efecto_P7_5"] - o["efecto_P7_4"] for o in camb) if camb else None)},
     "dano_no_conocido_por_causa": dict(sum((collections.Counter({k: v for k, v in o["desglose"].items() if "no conocido" in k}) for o in V), collections.Counter())),
     "dano_conocido_por_causa": dict(sum((collections.Counter({k: v for k, v in o["desglose"].items() if "no conocido" not in k}) for o in V), collections.Counter()))}
json.dump({"resumen": R, "usos": OUT}, open(os.path.join(AQUI, "P7_5_huella.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
