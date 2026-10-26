"""[P7-64] BANCO (coste cero): ¿DONDE TIENE AGARRE LA RAZON? Sobre todas las invitaciones de P7-56 (CON_RAZON, 3 series) y de las series 1-3 de P7-61 (MIENTEN_DOS, MIENTE_UNA:
dias 1-7 honestos, dias 8-20 honestas y la falsa aparte), con las funciones de analiza_P7_61 (invitaciones reconstruidas, verdad por la tabla del mundo).
  OPORTUNIDAD = una invitacion cargada en una vida-dia que se activo al menos una vez (P7_54_activa con su indice); ACEPTADA si hay P7_54_aceptada con su indice.
  EL MOMENTO de una oportunidad = su primer tic activa (unico tic que se registra): vida (tramos < 30, 30-60, 60-90, >= 90); AMENAZA = rival a <= 4 casillas (ve_agentes) o golpe en
  los 48 tics anteriores o calma=PELIGRO con vida >= 30 (fuego o rival, de la situacion registrada); PESO DE LA ALTERNATIVA = d(candidato invitado) - d(elegido) en la radiografia de
  ese tic (el cuerpo elige el menor d; 0 = el invitado era el elegido), solo para las acciones con candidato de nombre unico (usar_botiquin, usar_racion, ir_pareja, noop,
  ponerse_camouflage, soltar_first_aid, empunar_net); para COGER_* no se puede saber cual de los ir_objeto/coger es el de la invitacion ("sin medida").
  EVALUACIONES por accion: P7_54_evaluada (+ P7_62_evaluada si las hubiera).  python3 banco_P7_64.py -> P7_64_banco.json"""
import glob, json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); sys.path.insert(0, AQUI); sys.argv = sys.argv[:1]
import analiza_P7_61 as A
NOMBRE = {"USAR_BOTIQUIN": "usar_botiquin", "USAR_RACION": "usar_racion", "ACERCARSE_HERMANA": "ir_pareja", "QUEDARSE_QUIETA": "noop", "PONERSE_CAMUFLAJE": "ponerse_camouflage",
          "DAR_BOTIQUIN_HERMANA": "soltar_first_aid", "EMPUNAR_RED": "empunar_net"}


def tramo_vida(hp): return "<30" if hp < 30 else "30-60" if hp < 60 else "60-90" if hp < 90 else ">=90"
def tramo_peso(m): return "sin medida" if m is None else "0 (elegida)" if m <= 1e-9 else "(0, 0,02]" if m <= 0.02 else "(0,02, 0,1]" if m <= 0.1 else "> 0,1"


def lee(f, slot, ticks_pedidos):
    T = {}; golpes = []; ACT = {}; AC = {}; EV = []
    for l in open(f, errors="replace"):
        if l.startswith('{"k":"tick"'):
            r = json.loads(l)
            if r.get("phase") != "live": continue
            t = r["tick"]
            if any(float(d.get("amount") or 0) > 0 for d in (r.get("damage_taken") or [])): golpes.append(t)
            if True:
                pos = r.get("pos") or (0, 0); riv = [max(abs(a["pos"][0] - pos[0]), abs(a["pos"][1] - pos[1])) for a in (r.get("ve_agentes") or []) if a.get("slot") not in (slot, slot ^ 1) and a.get("pos")]
                R = r.get("RADIOGRAFIA") or {}; C = {k: (v["d"] if isinstance(v, dict) else v) for k, v in (R.get("candidatos") or {}).items()}
                T[t] = {"hp": float(r.get("hp") or 0), "rival": min(riv) if riv else None, "C": C, "el": R.get("elegido")}
        elif l.startswith('{"k":"P7_54_activa"'):
            a = json.loads(l); ACT.setdefault(a["n"], a)
        elif l.startswith('{"k":"P7_54_aceptada"'):
            a = json.loads(l); AC.setdefault(a["n"], []).append(a["tick"])
        elif l.startswith('{"k":"P7_54_evaluada"') or l.startswith('{"k":"P7_62_evaluada"'): EV.append(json.loads(l))
    return T, golpes, ACT, AC, EV


filas = []; cargadas = []
for campo, brazos, series in (("P7_56", ("CON_RAZON",), (1, 2, 3)), ("P7_57", ("MIENTEN_DOS", "MIENTE_UNA"), (1, 2, 3))):
    C = A.CAMPOS[campo]; E = json.load(open(os.path.join(AQUI, C["estado"])))
    for p in E["peticiones"]:
        if p["estado"] != "completed" or p["brazo"] not in brazos or p["serie"] not in series: continue
        for sl in (10, 11):
            fs = glob.glob(os.path.join(RUNS, f"{C['pref']}_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}", f"*policy_agent_{sl}.art.log"))
            if not fs: continue
            inv, pos = A.invitaciones(C, p["serie"], p["dia"], p["brazo"], sl)
            if not inv: continue
            # primera pasada barata: los tics de activacion; luego solo esos tics (y los golpes)
            T, golpes, ACT, AC, EV = lee(fs[0], sl, None)
            nev = {}
            for e in EV: nev[e["n"]] = nev.get(e["n"], 0) + 1
            for k, i in enumerate(inv):
                a = ACT.get(k)
                cargadas.append({"campo": campo, "serie": p["serie"], "dia": p["dia"], "brazo": p["brazo"], "asiento": sl, "accion": i["accion"], "falsa": bool(i.get("falsa")), "calma": i.get("calma"), "anillo": i.get("anillo"), "hermana": i.get("hermana"), "activa": a is not None})
                if a is None: continue
                t = a["tick"]; m = T.get(t) or {}; hp = m.get("hp", 100.0); sit = a.get("situacion") or {}
                amen = bool((m.get("rival") is not None and m["rival"] <= 4) or any(t - 48 <= g <= t for g in golpes) or (sit.get("calma") == "PELIGRO" and hp >= 30))
                nom = NOMBRE.get(i["accion"]); Cd = m.get("C") or {}; el = m.get("el")
                peso = (Cd[nom] - Cd[el]) if (nom and nom in Cd and el in Cd) else None
                falsa = bool(i.get("falsa"))
                periodo = "P7-56" if campo == "P7_56" else ("P7-61 falsa" if falsa else ("P7-61 d1-7" if p["dia"] <= 7 else "P7-61 d8-20"))
                filas.append({"campo": campo, "periodo": periodo, "serie": p["serie"], "dia": p["dia"], "brazo": p["brazo"], "asiento": sl, "accion": i["accion"], "falsa": falsa, "verdad": A.es_verdad(i),
                              "cuerpo": float(i.get("cuerpo") or 0), "anillo": i.get("anillo"), "calma": i.get("calma"), "movimiento": i.get("movimiento"), "hermana": i.get("hermana"),
                              "aceptada": k in AC, "n_aceptaciones": len(AC.get(k, [])), "evaluaciones": nev.get(k, 0), "vida": hp, "tramo_vida": tramo_vida(hp), "amenaza": amen, "peso": peso, "tramo_peso": tramo_peso(peso)})


def frac(L):
    n = len(L); a = sum(1 for x in L if x["aceptada"]); return {"oportunidades": n, "aceptadas": a, "fraccion": round(a / n, 3) if n else None, "evaluaciones": sum(x["evaluaciones"] for x in L)}


R = {"oportunidades": len(filas), "por_accion": {}, "por_vida": {}, "por_amenaza": {}, "por_peso": {}, "por_accion_y_momento": {}, "situaciones_con_agarre": []}
PER = ("P7-56", "P7-61 d1-7", "P7-61 d8-20", "P7-61 falsa")
for per in PER + ("honestas, todo",):
    L = [x for x in filas if (x["periodo"] == per if per != "honestas, todo" else not x["falsa"])]
    R["por_accion"][per] = {ac: frac([x for x in L if x["accion"] == ac]) for ac in sorted({x["accion"] for x in L})}
    R["por_vida"][per] = {t: frac([x for x in L if x["tramo_vida"] == t]) for t in ("<30", "30-60", "60-90", ">=90")}
    R["por_amenaza"][per] = {k: frac([x for x in L if x["amenaza"] == v]) for k, v in (("amenaza", True), ("sin amenaza", False))}
    R["por_peso"][per] = {t: frac([x for x in L if x["tramo_peso"] == t]) for t in ("0 (elegida)", "(0, 0,02]", "(0,02, 0,1]", "> 0,1", "sin medida")}
H = [x for x in filas if not x["falsa"]]
for ac in sorted({x["accion"] for x in H}):
    L = [x for x in H if x["accion"] == ac]
    R["por_accion_y_momento"][ac] = {"vida": {t: frac([x for x in L if x["tramo_vida"] == t]) for t in ("<30", "30-60", "60-90", ">=90")}, "amenaza": {k: frac([x for x in L if x["amenaza"] == v]) for k, v in (("amenaza", True), ("sin amenaza", False))}}
# situaciones con agarre: accion x (calma, anillo, hermana) de la invitacion, con >= 15 oportunidades
grupos = {}
for x in H: grupos.setdefault((x["accion"], x["calma"], x["anillo"], x["hermana"]), []).append(x)
for (ac, ca, an, he), L in grupos.items():
    if len(L) < 15: continue
    f = frac(L); vidas = sorted({(x["campo"], x["serie"], x["dia"], x["brazo"], x["asiento"]) for x in L})
    R["situaciones_con_agarre"].append({"accion": ac, "calma": ca, "anillo": an, "hermana": he, **f, "vida_media_al_activarse": round(st.mean(x["vida"] for x in L), 1), "fraccion_en_amenaza": round(sum(x["amenaza"] for x in L) / len(L), 3),
                                        "activacion_por_carga": None})
R["situaciones_con_agarre"].sort(key=lambda g: -(g["fraccion"] or 0))
# frecuencia por serie de cada accion (oportunidades y evaluaciones por serie y hermana, honestas)
ser = {}
for x in H: ser.setdefault(x["accion"], []).append(x)
nvidas_serie = {}
for x in H: nvidas_serie.setdefault((x["campo"], x["serie"], x["brazo"], x["asiento"]), set()).add(x["dia"])
R["por_serie_y_hermana"] = {ac: {"oportunidades": round(len(L) / len(nvidas_serie), 2), "aceptadas": round(sum(x["aceptada"] for x in L) / len(nvidas_serie), 2), "evaluaciones": round(sum(x["evaluaciones"] for x in L) / len(nvidas_serie), 2)} for ac, L in ser.items()}
R["hermanas_serie"] = len(nvidas_serie)
# activacion por carga (de las invitaciones honestas cargadas, que fraccion se activo) y evaluaciones por oportunidad, por grupo (accion, calma, anillo, hermana)
for g in R["situaciones_con_agarre"]:
    Lc = [c for c in cargadas if not c["falsa"] and (c["accion"], c["calma"], c["anillo"], c["hermana"]) == (g["accion"], g["calma"], g["anillo"], g["hermana"])]
    g["cargadas"] = len(Lc); g["activacion_por_carga"] = round(sum(c["activa"] for c in Lc) / len(Lc), 3) if Lc else None; g["evaluaciones_por_oportunidad"] = round(g["evaluaciones"] / g["oportunidades"], 2)
    g["evaluaciones_por_serie_si_se_carga_cada_noche"] = round(39 * (g["activacion_por_carga"] or 0) * g["evaluaciones_por_oportunidad"], 1)      # 3 hermanas que mienten x 13 dias (8-20)
def candidata(nombre, filtro, filtro_c):
    L = [x for x in H if filtro(x)]; Lc = [c for c in cargadas if not c["falsa"] and filtro_c(c)]
    act = sum(c["activa"] for c in Lc) / len(Lc) if Lc else None; ev_op = sum(x["evaluaciones"] for x in L) / len(L) if L else None; ac = sum(x["aceptada"] for x in L) / len(L) if L else None
    return {"nombre": nombre, "cargadas": len(Lc), "oportunidades": len(L), "activacion_por_carga": round(act, 3) if act is not None else None, "aceptacion_por_oportunidad": round(ac, 3) if ac is not None else None,
            "evaluaciones_por_oportunidad": round(ev_op, 2) if ev_op is not None else None, "evaluaciones_por_serie_si_se_carga_cada_noche": round(39 * act * ev_op, 1) if act is not None and ev_op is not None else None}
R["candidatas"] = [
    candidata("ACERCARSE_HERMANA con peligro (calma=PELIGRO)", lambda x: x["accion"] == "ACERCARSE_HERMANA" and x["calma"] == "PELIGRO", lambda c: c["accion"] == "ACERCARSE_HERMANA" and c["calma"] == "PELIGRO"),
    candidata("QUEDARSE_QUIETA con peligro (calma=PELIGRO)", lambda x: x["accion"] == "QUEDARSE_QUIETA" and x["calma"] == "PELIGRO", lambda c: c["accion"] == "QUEDARSE_QUIETA" and c["calma"] == "PELIGRO"),
    candidata("QUEDARSE_QUIETA (cualquier situacion)", lambda x: x["accion"] == "QUEDARSE_QUIETA", lambda c: c["accion"] == "QUEDARSE_QUIETA"),
    candidata("COGER_BOTIQUIN (cualquier situacion)", lambda x: x["accion"] == "COGER_BOTIQUIN", lambda c: c["accion"] == "COGER_BOTIQUIN"),
    candidata("COGER_BOTIQUIN con peligro (calma=PELIGRO)", lambda x: x["accion"] == "COGER_BOTIQUIN" and x["calma"] == "PELIGRO", lambda c: c["accion"] == "COGER_BOTIQUIN" and c["calma"] == "PELIGRO"),
    candidata("USAR_RACION (referencia: la falsa de P7-63)", lambda x: x["accion"] == "USAR_RACION", lambda c: c["accion"] == "USAR_RACION")]
json.dump(R, open(os.path.join(AQUI, "P7_64_banco.json"), "w"), ensure_ascii=False, indent=1)
json.dump(filas, open(os.path.join(AQUI, "P7_64_filas.json"), "w"), ensure_ascii=False)
print(R["oportunidades"]); [print(per, {k: (v["oportunidades"], v["fraccion"]) for k, v in R["por_accion"][per].items()}) for per in R["por_accion"]]
