"""[P7-31, seccion 3] Cuantas rachas de 3 o mas pasos listos bloqueados sin nadie a la vista caen en una casilla inundada (o en una tormenta de fuego) segun el aviso
`event_warning` del propio diario (rectangulo y ventana de cada inundacion; centro y radio de cada tormenta). Campos: P7-24, P7-30 (lo jugado) y la partida de A4
P611_t2 21727122 (la de los "muros fantasma" de F1 en P7-29). -> P7_31_inundaciones.json
  python3 inundaciones_P7_31.py"""
import collections, glob, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0), "NE": (1, -1), "NW": (-1, -1), "SE": (1, 1), "SW": (-1, 1)}


def analiza(f):
    avisos = []; prev = None; racha = None; R = []
    for line in open(f, errors="replace"):
        if '"tick"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") != "tick" or r.get("phase") != "live": continue
        for e in r.get("eventos") or []:
            if e.get("type") == "event_warning": avisos.append(e)
        bl = r.get("action_result") == "blocked" and (r.get("move_ready_in") or 0) == 0 and prev is not None and (prev.get("intencion") or {}).get("do") == "move"
        if bl:
            d = prev["intencion"]["dir"]; dx, dy = DIRS.get(d, (0, 0)); tgt = (prev["pos"][0] + dx, prev["pos"][1] + dy); visto = any(tuple(a.get("pos") or ()) == tgt for a in prev.get("ve_agentes") or [])
            key = (tuple(prev["pos"]), d)
            if racha and racha["key"] == key: racha["n"] += 1; racha["t1"] = r["tick"]; racha["visto"] += visto
            else:
                if racha and racha["n"] >= 3 and racha["visto"] == 0: R.append(racha)
                racha = {"key": key, "n": 1, "t0": r["tick"], "t1": r["tick"], "visto": int(visto), "tgt": tgt}
        elif r.get("action_result") != "blocked":
            if racha and racha["n"] >= 3 and racha["visto"] == 0: R.append(racha)
            racha = None
        prev = r
    if racha and racha["n"] >= 3 and racha["visto"] == 0: R.append(racha)
    def inundada(t, c): return any(e.get("kind") == "flood" and e["from_tick"] <= t < e["from_tick"] + e["duration"] and e["rect"][0] <= c[0] <= e["rect"][2] and e["rect"][1] <= c[1] <= e["rect"][3] for e in avisos)
    def tormenta(t, c): return any(e.get("kind") == "firestorm" and e["from_tick"] <= t < e["from_tick"] + e["duration"] and (c[0] - e["center"][0]) ** 2 + (c[1] - e["center"][1]) ** 2 <= e["radius"] ** 2 for e in avisos)
    return avisos, [(x, inundada(x["t0"], x["tgt"]), tormenta(x["t0"], x["tgt"])) for x in R]


if __name__ == "__main__":
    tot = collections.Counter(); tics = collections.Counter(); ej = []; avisos_n = collections.Counter()
    for pat in ("P724_s*_d*_*", "P730_s*_d*_*", "P611_t2_A4_21727122"):
        for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", pat, "*agent_1[01].art.log"))):
            av, R = analiza(f); campo = os.path.basename(os.path.dirname(f))[:4]; avisos_n[(campo, "vidas con algun aviso")] += int(bool(av))
            for x, inu, tor in R:
                k = (campo, "inundada" if inu else ("tormenta" if tor else "otra")); tot[k] += 1; tics[k] += x["n"]
                if (inu or tor) and len(ej) < 20: ej.append({"partida": os.path.basename(os.path.dirname(f)), "asiento": f[-10:-8], "t0": x["t0"], "desde": list(x["key"][0]), "dir": x["key"][1], "hacia": list(x["tgt"]), "n": x["n"], "evento": "flood" if inu else "firestorm"})
    out = {"rachas": {f"{k[0]} · {k[1]}": [tot[k], tics[k]] for k in tot}, "vidas_con_aviso": {f"{k[0]}": v for k, v in avisos_n.items()}, "ejemplos": ej}
    json.dump(out, open(os.path.join(AQUI, "P7_31_inundaciones.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out["rachas"], ensure_ascii=False), out["vidas_con_aviso"])
