"""[P7-18] Lectura de las escenas de `P7_18_escenas.json` (banco_P7_18.py) con la posicion de quien regalo en cada tic (de su diario). Para cada tic
en que el que pedia esta a dos casillas o menos del botiquin regalado, UNA razon, la primera que cumpla, en este orden (declarado antes de contar):
  1. ya lleva un botiquin (cogio otro);
  2. el que lo dio esta encima del regalo (la casilla esta ocupada: no se puede entrar ni coger);
  3. esta encima y `coger` no existe porque la casilla esta en SUS cesiones (el mismo solto ahi antes);
  4. esta encima y `coger` esta escondido por el arreglo del seis ("la mochila no cambia");
  5. esta encima y `coger` existe: lo elige / pierde;
  6. a 1 o 2 casillas, casilla libre: solo tiene `noop` (el paso esta en enfriamiento);
  7. … tiene un candidato de ir a por ESE botiquin (`ir_objeto` o `ir_curioso` con ese destino): lo elige, da un paso hacia el, o pierde contra otra cosa;
  8. … no tiene candidato de ir a por el: su mejor objeto es otro (cual), o la casilla esta en sus cesiones, o no le cabe.
-> P7_18_razones.json"""
import collections, glob, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
E = json.load(open(os.path.join(AQUI, "P7_18_escenas.json"))); G = E["regalos"]; H = E["hermanos"]; V = json.load(open(os.path.join(AQUI, "P7_14b_vidas.json")))
DIR = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0), "NE": (1, -1), "NW": (-1, -1), "SE": (1, 1), "SW": (-1, 1)}
_c = {}
def diario(k):
    if k not in _c:
        v = V[k]; T = {}
        for line in open(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P714b_s{v['serie']}_d{v['dia']}_{v['brazo']}_*", f"*agent_{v['slot']}.art.log"))[0]):
            if '"tick"' in line[:16]:
                r = json.loads(line)
                if r.get("k") == "tick" and r.get("phase") == "live": T[r["tick"]] = (tuple(r["pos"]), r.get("action_result"))
        _c[k] = T
    return _c[k]
def razon(t, dio_encima):
    gp = tuple(t["regalo"]); el = str(t["elegido"]); d = t["d"]
    if t["botiquines"] >= 1: return "ya lleva un botiquin"
    if dio_encima: return "el que lo dio esta encima del regalo"
    if t["dist"] == 0:
        if "coger" in d: return "encima: coge" if el == "coger" else "encima: coger existe y pierde"
        if t["regalo_en_mis_cedidos"]: return "encima: la casilla esta en sus propias cesiones (no hay coger)"
        if t["coger_escondido"]: return "encima: coger escondido por el arreglo del seis"
        return "encima: sin coger, otra razon"
    if len(d) == 1: return "a 1-2: solo noop (paso en enfriamiento)"
    hacia = [c[0] for c in t["candidatos_de_candidatos"] if c[0] in ("ir_objeto", "ir_curioso") and c[2] and tuple(c[2]) == gp]
    if hacia:
        if el in hacia: return "a 1-2: va a por el"
        u = DIR.get(el.split("_", 1)[1]) if el.startswith(("move_", "paso_")) else None
        if u and max(abs(t["pos"][0] + u[0] - gp[0]), abs(t["pos"][1] + u[1] - gp[1])) < t["dist"]: return "a 1-2: da un paso hacia el"
        return "a 1-2: tiene candidato de ir a por el y pierde contra " + ("un paso" if el.startswith(("move_", "paso_")) else el)
    if t["regalo_en_mis_cedidos"]: return "a 1-2: sin candidato, la casilla esta en sus propias cesiones"
    if not t["cabe"]: return "a 1-2: sin candidato, no le cabe"
    mo = t["mejor_objeto"]
    if mo and tuple(mo) == tuple(t["pos"]): return "a 1-2: sin candidato, su mejor objeto es su propia casilla (" + str(t["que_es_el_mejor_objeto"]) + " recordado ahi)"
    if mo: return "a 1-2: sin candidato, su mejor objeto es otro (" + str(t["que_es_el_mejor_objeto"]) + ")"
    return "a 1-2: sin candidato, sin mejor objeto"
R = {"por_brazo": {}, "regalos": []}
for g in G:
    Td = diario(g["vida_del_que_dio"]); Th = diario(g["hermano"]); gp = tuple(g["pos"]); c = collections.Counter(); bloq = 0; pasos = 0
    espera = [t for t in range(g["t0"], g["t1"] + 1) if t in Td]; enc = sum(1 for t in espera if Td[t][0] == gp)
    for t in H[g["hermano"]].get("tics", []):
        if not (g["t0"] <= t["t"] <= g["t1"] and t["regalo"] == g["pos"]): continue
        de = (Td.get(t["t"]) or (None,))[0] == gp; c[razon(t, de)] += 1
        el = str(t["elegido"]); u = DIR.get(el.split("_", 1)[1]) if el.startswith(("move_", "paso_")) else None
        if u and (t["pos"][0] + u[0], t["pos"][1] + u[1]) == gp:
            pasos += 1; bloq += (Th.get(t["t"] + 1) or (None, None))[1] == "blocked"
    R["regalos"].append({**g, "tics_de_espera": len(espera), "tics_con_el_que_dio_encima": enc, "tics_del_que_pedia_cerca": sum(c.values()), "razones": dict(c), "razon_principal": (c.most_common(1)[0][0] if c else None),
                         "pasos_hacia_la_casilla_del_regalo": pasos, "de_ellos_bloqueados": bloq})
for b in ("TECHO", "APRENDE", "BORRADO"):
    X = [r for r in R["regalos"] if r["brazo"] == b]; c = collections.Counter()
    for r in X: c.update(r["razones"])
    R["por_brazo"][b] = {"regalos": len(X), "tics_cerca": sum(c.values()), "razones": dict(c.most_common()), "razon_principal_por_regalo": dict(collections.Counter(r["razon_principal"] for r in X).most_common()),
                         "tics_de_espera": sum(r["tics_de_espera"] for r in X), "tics_con_el_que_dio_encima": sum(r["tics_con_el_que_dio_encima"] for r in X), "regalos_con_el_que_dio_encima_mas_del_90": sum(1 for r in X if r["tics_con_el_que_dio_encima"] > 0.9 * r["tics_de_espera"]),
                         "regalos_con_el_que_dio_encima_alguna_vez": sum(1 for r in X if r["tics_con_el_que_dio_encima"] > 0), "pasos_hacia_la_casilla": sum(r["pasos_hacia_la_casilla_del_regalo"] for r in X), "bloqueados": sum(r["de_ellos_bloqueados"] for r in X)}
    print(b, json.dumps(R["por_brazo"][b], ensure_ascii=False)[:1500])
json.dump(R, open(os.path.join(AQUI, "P7_18_razones.json"), "w"), ensure_ascii=False, indent=1)
