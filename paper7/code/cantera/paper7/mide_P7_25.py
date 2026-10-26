"""[P7-25, medida 1] LA MEDIDA CORREGIDA, leida de los diarios del humo de P7-23 (P723_s1_d1-3) y del freno de P7-24 (P724_s1_d1-3), los dos asientos. Coste cero.
  python3 mide_P7_25.py -> P7_25_medida.json
Por vida: (1) de los instantes en que el paso esta LISTO (`move_ready_in` = 0, no enfriamiento), en cuantos gana `ir_curioso`; (2) cuantos instantes pasan desde que ve
por primera vez un objeto desconocido (botiquin o racion a la vista cuando aun no tiene ningun recuerdo de esa clase: al nacer, las dos) hasta tocarlo (la primera unidad
de esa clase que entra en el zurron). Tambien: lo elegido con el paso listo, y lo elegido con el paso listo y un consumible desconocido a 1 o 2 casillas."""
import collections, glob, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); OBJ = {"first_aid": "botiquin", "rations": "racion"}


def una(f):
    T = []; H = []
    for line in open(f):
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") == "tick" and r.get("phase") == "live":
            n = collections.Counter()
            for s in (r.get("pack") or []):
                if s: n[s.get("id")] += int(s.get("n") or 1)
            T.append({"t": r["tick"], "pos": tuple(r["pos"]), "listo": (r.get("move_ready_in") or 0) == 0, "el": str((r.get("RADIOGRAFIA") or {}).get("elegido") or ""), "n": {o: n.get(o, 0) for o in OBJ},
                      "vis": {o: min((max(abs(i["pos"][0] - r["pos"][0]), abs(i["pos"][1] - r["pos"][1])) for i in (r.get("ve_items") or []) if i.get("id") == o and i.get("pos")), default=None) for o in OBJ}})
        elif r.get("k") == "P7_huella": H.append(r)
    out = {"tics": len(T), "listos": sum(1 for t in T if t["listo"])}
    L = [t for t in T if t["listo"]]; out["gana_ir_curioso_con_el_paso_listo"] = sum(1 for t in L if t["el"] == "ir_curioso"); out["elegido_con_el_paso_listo"] = dict(collections.Counter(t["el"] for t in L).most_common(8))
    out["ir_curioso_en_total"] = sum(1 for t in T if t["el"] == "ir_curioso")
    # ver por primera vez y tocar, por clase (desconocida hasta su primer recuerdo)
    primer_rec = {}
    for h in H:
        o = h.get("objeto") or "first_aid"
        if h.get("apuntado") and o not in primer_rec: primer_rec[o] = h["t0"]
    out["ver_y_tocar"] = {}
    for o in OBJ:
        ve = next((t["t"] for t in T if t["vis"][o] is not None), None)
        toca = next((T[i]["t"] for i in range(1, len(T)) if T[i]["n"][o] > T[i - 1]["n"][o]), None)
        out["ver_y_tocar"][OBJ[o]] = {"ve_por_primera_vez": ve, "toca": toca, "instantes_de_ver_a_tocar": (toca - ve) if (ve is not None and toca is not None) else None}
    # con el paso listo y un consumible desconocido a 1 o 2 casillas
    cerca = [t for t in L if any(t["vis"][o] is not None and t["vis"][o] <= 2 and (o not in primer_rec or t["t"] < primer_rec[o]) for o in OBJ)]
    out["paso_listo_y_desconocido_a_1_o_2"] = {"tics": len(cerca), "elegido": dict(collections.Counter(t["el"] for t in cerca).most_common(6))}
    return out


if __name__ == "__main__":
    OUT = {}
    for pref, campo in (("P723", "humo P7-23"), ("P724", "freno P7-24")):
        for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"{pref}_s1_d*_APRENDE_*"))):
            d = int(os.path.basename(c).split("_")[2][1:])
            for sl in (10, 11):
                f = glob.glob(os.path.join(c, f"*policy_agent_{sl}.art.log"))
                if f: OUT[f"{campo}|d{d}_{sl}"] = una(f[0])
    json.dump(OUT, open(os.path.join(AQUI, "P7_25_medida.json"), "w"), ensure_ascii=False, indent=1)
    for k, v in OUT.items(): print(k, "| listos", v["listos"], "de", v["tics"], "| ir_curioso con paso listo", v["gana_ir_curioso_con_el_paso_listo"], f"({100*v['gana_ir_curioso_con_el_paso_listo']/max(1,v['listos']):.0f} %)", "| en total", v["ir_curioso_en_total"], "| ver->tocar", {o: x["instantes_de_ver_a_tocar"] for o, x in v["ver_y_tocar"].items()}, "| cerca:", v["paso_listo_y_desconocido_a_1_o_2"])
