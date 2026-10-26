"""[P7-42] EL CAMPO DEL CAPITULO 3, leido de los diarios (paintball/runs/P741_s<S>_d<D>_<variante>_<semilla>/, dos asientos) -> P7_42_datos.json. Coste cero.
= analiza_P7_34.una (contactos, cogidas, pruebas y contexto, cuaderno, puesto, muerte, latencia, agua) + las medidas de SELLO_P7_42.md:
  rapidez (creencia del botiquin y la racion al cerrar; el primer dia se calcula en sello_P7_42), sabiduria (dias 11-20: tics con ventana de red/camuflaje abierta, tics
  llevando red o camuflaje, tics de `ir_curioso`/`ir_azar` que acaban en una cogida de red o camuflaje; y la vida perdida en esos tics), cuando (aperturas de uso del
  botiquin con hp < 50, de la racion con hp < 100: `P7_nace_uso`), pruebas por dia (huellas de las cuatro cosas) y, en SIN, las forzadas (`P7_41_azar`).
  python3 analiza_P7_42.py"""
import collections, glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import analiza_P7_34 as A34
NOM = A34.NOM


def extra(carp, slot):
    f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log"))
    if not f: return {}
    T = []; H = []; USO = []; AZ = []; ARR = None
    for line in open(f[0], errors="replace"):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "tick" and r.get("phase") == "live":
            n = A34.unidades(r); T.append({"t": r["tick"], "hp": float(r.get("hp") or 0.0), "el": str((r.get("RADIOGRAFIA") or {}).get("elegido") or ""), "gear": (n["net"] + n["camouflage"]) > 0, "n": n})
        elif k == "P7_huella": H.append(r)
        elif k == "P7_nace_uso": USO.append(r)
        elif k == "P7_41_azar": AZ.append(r)
        elif k == "P7_41_arranque": ARR = r
    if not T: return {}
    idx = {t["t"]: i for i, t in enumerate(T)}
    # sabiduria: tics con ventana de red/camuflaje abierta
    en_ventana = set(); ven_o = {"net": set(), "camouflage": set()}
    for h in H:
        if (h.get("objeto") or "first_aid") in ("net", "camouflage"):
            for t in range(int(h["t0"]), int(h.get("t_fin") or h["t0"]) + 1): en_ventana.add(t); ven_o[h["objeto"]].add(t)
    llevando = {t["t"] for t in T if t["gear"]}; llev_o = {o: {t["t"] for t in T if t["n"][o] > 0} for o in ("net", "camouflage")}
    # ir hacia: las rachas de ir_curioso / ir_azar que acaban en una cogida de red o camuflaje
    yendo = set()
    for i in range(1, len(T)):
        if (T[i]["n"]["net"] + T[i]["n"]["camouflage"]) > (T[i - 1]["n"]["net"] + T[i - 1]["n"]["camouflage"]):
            j = i - 1
            while j >= 0 and T[j]["el"] in ("ir_curioso", "ir_azar", "coger"): yendo.add(T[j]["t"]); j -= 1
    gear_tics = en_ventana | llevando | yendo
    vida_perdida = sum(max(0.0, T[i - 1]["hp"] - T[i]["hp"]) for i in range(1, len(T)) if T[i]["t"] in gear_tics)
    # [Manel, 11-oct] la sabiduria por separado para red y camuflaje: ventana + llevando (el ir hacia no distingue la cosa hasta cogerla: se reparte segun lo cogido)
    por_cosa = {}
    for o in ("net", "camouflage"):
        yo = set()
        for i in range(1, len(T)):
            if T[i]["n"][o] > T[i - 1]["n"][o]:
                j = i - 1
                while j >= 0 and T[j]["el"] in ("ir_curioso", "ir_azar", "coger"): yo.add(T[j]["t"]); j -= 1
        tics_o = ven_o[o] | llev_o[o] | yo
        por_cosa[NOM[o]] = {"tics": len(tics_o), "segundos": round(len(tics_o) / 24.0, 1), "vida_perdida": round(sum(max(0.0, T[i - 1]["hp"] - T[i]["hp"]) for i in range(1, len(T)) if T[i]["t"] in tics_o), 1)}
    usos_b = [u for u in USO if u.get("objeto") == "first_aid"]; usos_r = [u for u in USO if u.get("objeto") == "rations"]
    forz = [a for a in AZ if a.get("momento") == "forzada"]; fines = [a for a in AZ if a.get("momento") == "fin"]
    return {"sabiduria": {"tics_ventana": len(en_ventana), "tics_llevando": len(llevando), "tics_yendo": len(yendo), "tics_gear": len(gear_tics), "segundos_gear": round(len(gear_tics) / 24.0, 1), "vida_perdida_gear": round(vida_perdida, 1), "por_cosa": por_cosa},
            "cuando": {"usos_botiquin": len(usos_b), "usos_botiquin_hp_menor_50": sum(1 for u in usos_b if float(u.get("hp") or 100) < 50), "usos_racion": len(usos_r), "usos_racion_hp_menor_100": sum(1 for u in usos_r if float(u.get("hp") or 100) < 100), "hp_usos_botiquin": [u.get("hp") for u in usos_b]},
            "pruebas_dia": sum(1 for h in H), "pruebas_por_cosa": {NOM[o]: sum(1 for h in H if (h.get("objeto") or "first_aid") == o) for o in NOM},
            "azar": {"forzadas": len(forz), "forzadas_por_tipo": {t: sum(1 for a in forz if a.get("tipo") == t) for t in ("ir", "usar")}, "forzadas_conocida": sum(1 for a in forz if a.get("conocida")), "fines": {k: sum(1 for a in fines if a.get("fin") == k) for k in ("cogida", "usada", "caduca")}},
            "arranque_41": ({k: v for k, v in ARR.items() if k in ("brazo", "piezas", "miedo")} if ARR else None), "elegidos": dict(collections.Counter(t["el"] for t in T).most_common(12))}


if __name__ == "__main__":
    V = []
    for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P741_s*_d*_*"))):
        b = os.path.basename(c).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); var = "_".join(b[3:-1])
        for sl in (10, 11):
            v = A34.una(c, serie, dia, var, sl); v["variante"] = var; v["base"] = var.split("_")[0]; v["personalidad"] = ({"v": "valiente", "p": "prudente"}.get(var.split("_")[-1], "unica") if "_" in var else "unica")
            if not v.get("sin_diario"): v.update(extra(c, sl))
            V.append(v); print(f"s{serie} d{dia} {var} a{sl}", ("sin diario" if v.get("sin_diario") else f"puesto {v['puesto']} pruebas {v.get('pruebas_dia')} gear {v.get('sabiduria', {}).get('segundos_gear')} s usos b {v.get('cuando', {}).get('usos_botiquin')} forzadas {v.get('azar', {}).get('forzadas')} errores fotos {v['errores_fotos']}"), flush=True)
    json.dump(V, open(os.path.join(AQUI, "P7_42_datos.json"), "w"), ensure_ascii=False, indent=1); print(len(V), "vidas")
