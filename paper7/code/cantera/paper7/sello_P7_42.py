"""[P7-42] EL SELLO Y LAS MEDIDAS, de una vez al acabar el campo, con las palabras de SELLO_P7_42.md: por variante (y personalidad), rapidez (primer dia al 50 % del efecto
real: botiquin 25, racion 7,5; por criatura en APRENDE y SIN, por vida en BORRADO; no llega = 21), sabiduria (dias 11-20), cuando (usos del botiquin con hp < 50, racion con
hp < 100), puesto medio, pruebas por dia; R1 y C1 con sus errores tipicos (3 errores tipicos de la diferencia = "3 veces el ruido"); dos cuentas (todas / sin marcadas).
Lee P7_42_datos.json (analiza_P7_42) -> P7_42_sello.json.  python3 sello_P7_42.py"""
import json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__))
L = [v for v in json.load(open(os.path.join(AQUI, "P7_42_datos.json"))) if not v.get("sin_diario")]
VAR = ("TECHO", "BORRADO_v", "BORRADO_p", "APRENDE_v", "APRENDE_p", "SIN"); REAL = {"botiquin": 50.0, "racion": 15.0}
partidas_corte = sorted({(v["serie"], v["dia"], v["variante"]) for v in L if v.get("parcial")}); MARC = sorted({(v["serie"], v["dia"], v["variante"]) for v in L if not v["latencia"]["pasa"]})
ee = lambda xs: (st.stdev(xs) / len(xs) ** 0.5 if len(xs) > 1 else None)
med = lambda xs: (st.mean(xs) if xs else None)


def vidas(var, fuera=(), dias=None): return [v for v in L if v["variante"] == var and (v["serie"], v["dia"], v["variante"]) not in fuera and (dias is None or v["dia"] in dias)]


def rapidez(var, fuera):
    """Por criatura (serie x asiento) en APRENDE y SIN; por vida en BORRADO (cada dia desde cero: el primer dia cuya vida llega). Lista de dias (21 = no llega)."""
    out = {"botiquin": [], "racion": []}
    if var.startswith("BORRADO") or var == "TECHO":
        for o in out:
            for s in (1, 2, 3):
                for sl in (10, 11):
                    vs = sorted(vidas(var, fuera), key=lambda v: v["dia"]); vs = [v for v in vs if v["serie"] == s and v["asiento"] == sl]
                    if vs: out[o].append(next((v["dia"] for v in vs if (v["al_acabar"][o]["creencia"] or -1) >= 0.5 * REAL[o]), 21))
        return out
    for o in out:
        for s in (1, 2, 3):
            for sl in (10, 11):
                vs = sorted([v for v in vidas(var, fuera) if v["serie"] == s and v["asiento"] == sl], key=lambda v: v["dia"])
                if vs: out[o].append(next((v["dia"] for v in vs if (v["al_acabar"][o]["creencia"] or -1) >= 0.5 * REAL[o]), 21))
    return out


def medidas(var, fuera):
    vs = vidas(var, fuera); v11 = vidas(var, fuera, range(11, 21)); vp = [v for v in vs if (v["serie"], v["dia"], v["variante"]) not in set(partidas_corte) and v["puesto"] is not None]
    ub = sum(v["cuando"]["usos_botiquin"] for v in vs); ub50 = sum(v["cuando"]["usos_botiquin_hp_menor_50"] for v in vs); ur = sum(v["cuando"]["usos_racion"] for v in vs); ur100 = sum(v["cuando"]["usos_racion_hp_menor_100"] for v in vs)
    rp = rapidez(var, fuera); seg = [v["sabiduria"]["segundos_gear"] for v in v11]; vida = [v["sabiduria"]["vida_perdida_gear"] for v in v11]
    pr_dia = {d: med([v["pruebas_dia"] for v in vs if v["dia"] == d]) for d in range(1, 21)}
    return {"vidas": len(vs), "en_puesto": len(vp), "puesto": med([v["puesto"] for v in vp]), "puesto_ee": ee([v["puesto"] for v in vp]) if len(vp) > 1 else None,
            "rapidez_botiquin": rp["botiquin"], "rapidez_botiquin_media": med(rp["botiquin"]), "rapidez_botiquin_ee": ee(rp["botiquin"]), "rapidez_racion": rp["racion"], "rapidez_racion_media": med(rp["racion"]), "rapidez_racion_ee": ee(rp["racion"]),
            "sabiduria_segundos_media": med(seg), "sabiduria_segundos_ee": ee(seg), "sabiduria_vida_media": med(vida), "sabiduria_vida_ee": ee(vida), "sabiduria_tics": {k: sum(v["sabiduria"][k] for v in v11) for k in ("tics_ventana", "tics_llevando", "tics_yendo")},
            "usos_botiquin": ub, "usos_botiquin_hp_menor_50": ub50, "cuando_botiquin": (ub50 / ub if ub else None), "cuando_botiquin_ee": ((ub50 / ub * (1 - ub50 / ub) / ub) ** 0.5 if ub else None), "usos_racion": ur, "usos_racion_hp_menor_100": ur100, "cuando_racion": (ur100 / ur if ur else None),
            "pruebas_total": sum(v["pruebas_dia"] for v in vs), "pruebas_por_dia": pr_dia, "pruebas_por_cosa": {o: sum(v["pruebas_por_cosa"][o] for v in vs) for o in ("botiquin", "racion", "red", "camuflaje")}, "forzadas": sum(v.get("azar", {}).get("forzadas", 0) for v in vs),
            "mueren": sum(1 for v in vs if v["murio"]), "marcadas": sum(1 for v in vs if not v["latencia"]["pasa"]), "ms_mediana": med([v["latencia"]["ms_mediana"] for v in vs if v["latencia"]["ms_mediana"] is not None])}


def compara(a, b, ka, kee, menor=True):
    """diferencia a - b con su error tipico (raiz de la suma de cuadrados) y si es '3 veces el ruido'."""
    if a[ka] is None or b[ka] is None: return {"dif": None}
    d = a[ka] - b[ka]; e = ((a[kee] or 0) ** 2 + (b[kee] or 0) ** 2) ** 0.5
    return {"dif": round(d, 3), "ee": round(e, 3), "tres_veces": bool(e and abs(d) >= 3 * e), "cumple": (d < 0) if menor else (d > 0)}


def evalua(fuera):
    M = {var: medidas(var, fuera) for var in VAR}
    R1 = {k: compara(M[k], M["SIN"], "rapidez_botiquin_media", "rapidez_botiquin_ee", menor=True) for k in ("APRENDE_p", "APRENDE_v")}
    C1 = {k: compara(M[k], M["SIN"], "cuando_botiquin", "cuando_botiquin_ee", menor=False) for k in ("APRENDE_p", "APRENDE_v")}
    return {"medidas": M, "R1": {**R1, "pasa": all(x.get("cumple") for x in R1.values())}, "C1": {**C1, "pasa": all(x.get("cumple") for x in C1.values())},
            "S1": {k: {"segundos": M[k]["sabiduria_segundos_media"], "vida": M[k]["sabiduria_vida_media"]} for k in VAR},
            "caracter": {b: compara(M[f"{b}_v"], M[f"{b}_p"], "puesto", "puesto_ee", menor=True) for b in ("APRENDE", "BORRADO")}}


R = {"vidas": len(L), "partidas_con_corte": [list(x) for x in partidas_corte], "partidas_marcadas": [list(x) for x in MARC], "con_todas": evalua(set(partidas_corte)), "sin_marcadas": evalua(set(partidas_corte) | set(MARC))}
json.dump(R, open(os.path.join(AQUI, "P7_42_sello.json"), "w"), ensure_ascii=False, indent=1)
for cuenta in ("con_todas", "sin_marcadas"):
    E = R[cuenta]; print(cuenta, "R1", E["R1"]["pasa"], {k: v for k, v in E["R1"].items() if k != "pasa"}, "C1", E["C1"]["pasa"], {k: v for k, v in E["C1"].items() if k != "pasa"})
    for var in VAR: m = E["medidas"][var]; print("  ", var, "vidas", m["vidas"], "puesto", m["puesto"] and round(m["puesto"], 2), "rapidez b", m["rapidez_botiquin"], "cuando b", m["cuando_botiquin"] and round(m["cuando_botiquin"], 3), "gear s", m["sabiduria_segundos_media"] and round(m["sabiduria_segundos_media"], 1), "pruebas", m["pruebas_total"], "forzadas", m["forzadas"])
