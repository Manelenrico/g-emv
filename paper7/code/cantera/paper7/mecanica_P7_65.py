"""[P7-65] REVISION DE MECANICA tras las series 1 y 2 (registro del sello, 15-oct 21:20): SOLO comprobaciones de funcionamiento, todo junto; no se calcula ni se escribe nada que
deje ver L1, L2 o L4 (ni confianza por brazo, hermana o dia; ni dias de abandono; ni aceptacion de verdaderas). Criterios de parada fijados antes de mirar (en el sello).
  1. invitaciones falsas dichas por brazo (y en la razon honesta: la prudente de MIENTE_UNA, asiento 11): del estado (`mentiras`) y de lo que cada vida cargo (P7_65_arranque.falsas).
  2. evaluaciones de la falsa (P7_54_evaluada con su indice): total, fallos, aciertos (todo junto); de los aciertos, ejemplos con el tic de la cogida (el botiquin entra en la mochila
     tras aceptar) y la vida antes y despues.
  3. agarre: fraccion de vidas-dia con la falsa activa en que se acepto al menos una vez (todo junto).
  4. confianza en la razon: minimo y maximo de todo el campo (las tres dimensiones; arranque, cierre, evaluaciones, contrastes y cuadernos), valores vacios o no numericos, y si toda
     criatura empieza en 0,5 (arranque del dia 1).
  5. respuestas de la razon: llamadas y respuestas ilegibles (sin ninguna invitacion valida, o la llamada fallo).
  python3 mecanica_P7_65.py -> P7_65_mecanica.json (solo agregados)"""
import glob, json, math, os, random
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs")
E = json.load(open(os.path.join(AQUI, "P7_65_estado.json"))); SERIES = (1, 2)
falsas_estado = {}; falsas_vidas = {}; ev_tot = ev_fallo = ev_acierto = 0; ejemplos = []; op = op_acept = 0; conf = []; malos = 0; arranques_d1 = []
def num(x):
    global malos
    if isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x): conf.append(float(x))
    else: malos += 1
def dims(d):
    if not isinstance(d, dict): num(None); return
    for k in ("cuerpo", "recursos", "vinculo"): num(d.get(k))
for m in E.get("mentiras", []):
    if m["serie"] in SERIES: k = f"{m['brazo']} a{m['slot']}"; falsas_estado[k] = falsas_estado.get(k, 0) + 1
pos = {(m["serie"], m["dia_noche"] + 1, m["brazo"], m["slot"]): m["posicion"] for m in E.get("mentiras", [])}
for p in E["peticiones"]:
    if p["serie"] not in SERIES or p["estado"] != "completed": continue
    for sl in (10, 11):
        fs = glob.glob(os.path.join(RUNS, f"P765_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}", f"*policy_agent_{sl}.art.log"))
        if not fs: continue
        k = (p["serie"], p["dia"], p["brazo"], sl); n = pos.get(k); ticks = {}; act = False; acs = []; evs = []
        for l in open(fs[0], errors="replace"):
            if l.startswith('{"k":"tick"'):
                if n is None: continue
                r = json.loads(l)
                if r.get("phase") == "live": ticks[r["tick"]] = (float(r.get("hp") or 0), sum(int(it.get("n") or 1) for it in (r.get("pack") or []) if isinstance(it, dict) and it.get("id") == "first_aid"))      # la mochila apila: {"id": "first_aid", "n": k}
            elif l.startswith('{"k":"P7_65_arranque"'):
                a = json.loads(l); kk = f"{p['brazo']} a{sl}"; falsas_vidas[kk] = falsas_vidas.get(kk, 0) + int(a.get("falsas") or 0)
            elif l.startswith('{"k":"P7_54_arranque"'):
                a = json.loads(l); dims(a.get("confianza"))
                if p["dia"] == 1: arranques_d1.append(a.get("confianza"))
            elif l.startswith('{"k":"P7_54_cierre"') or l.startswith('{"k":"P7_65_cierre"') or l.startswith('{"k":"P7_57_cierre"'): dims(json.loads(l).get("confianza"))
            elif l.startswith('{"k":"P7_54_evaluada"'):
                e = json.loads(l); dims(e.get("confianza_antes")); dims(e.get("confianza_despues"))
                if n is not None and e["n"] == n: evs.append(e)
            elif l.startswith('{"k":"P7_62_contraste"') or l.startswith('{"k":"P7_57_contraste"'):
                c = json.loads(l); num(c.get("confianza_antes")); num(c.get("confianza_despues"))
            elif n is not None and l.startswith('{"k":"P7_54_activa"'):
                if json.loads(l)["n"] == n: act = True
            elif n is not None and l.startswith('{"k":"P7_54_aceptada"'):
                a = json.loads(l)
                if a["n"] == n: acs.append(a["tick"])
        if n is not None and act:
            op += 1; op_acept += bool(acs)
        for e in evs:
            ev_tot += 1; ac = (e.get("acierto") or {}).get("cuerpo")
            if ac == 1:
                ev_acierto += 1
                t0 = max([t for t in acs if t <= e["tick"]], default=None); ts = sorted(ticks)
                cog = next((t for i_, t in enumerate(ts) if i_ > 0 and t0 is not None and t0 <= t <= e["tick"] and ticks[ts[i_ - 1]][1] < ticks[t][1]), None)
                ejemplos.append({"tic_aceptada": t0, "tic_cogida": cog, "vida_al_aceptar": ticks.get(t0, (None,))[0], "vida_en_la_cogida": ticks.get(cog, (None,))[0] if cog else None,
                                 "tic_juicio": e["tick"], "vida_al_juzgar": ticks.get(e["tick"], (None,))[0], "fuente": e.get("fuente"), "vivido_cuerpo": (e.get("vivido") or {}).get("cuerpo"), "prometido_cuerpo": (e.get("prometido") or {}).get("cuerpo"), "botiquines_al_aceptar": ticks.get(t0, (None, None))[1]})
            else: ev_fallo += 1
        cu = os.path.join(AQUI, "P7_65_res", f"cuaderno_s{p['serie']}_d{p['dia']}_{p['brazo']}_{sl}.json")
        if os.path.exists(cu): dims(json.load(open(cu)).get("confianza_razon_P7_54"))
raz = [r for r in E.get("razon", []) if r["serie"] in SERIES]; fallidas = [x for x in E.get("noches_sin_razon", []) if x["serie"] in SERIES and "0 invitaciones" not in (x.get("motivo") or "")]
ilegibles = sum(1 for r in raz if not r.get("invitaciones")) + len(fallidas); llamadas = len(raz) + len(fallidas)
R = {"series": list(SERIES),
     "1_falsas_dichas": {"segun_el_estado": falsas_estado, "segun_lo_que_cargo_cada_vida": falsas_vidas, "razon_honesta_MIENTE_UNA_a11": falsas_vidas.get("MIENTE_UNA a11", 0) + falsas_estado.get("MIENTE_UNA a11", 0)},
     "2_evaluaciones_de_la_falsa": {"total": ev_tot, "fallo": ev_fallo, "acierto": ev_acierto, "fraccion_fallo": round(ev_fallo / ev_tot, 4) if ev_tot else None, "ejemplos_de_acierto": ([x for x in ejemplos if x["tic_cogida"]][:1] + [x for x in ejemplos if x["fuente"] == "huella" and not x["tic_cogida"]][:1] + [x for x in ejemplos if x["fuente"] != "huella"][:1]), "todos_los_aciertos": ejemplos, "n_aciertos": len(ejemplos), "aciertos_por_fuente": {f_: sum(1 for x in ejemplos if x["fuente"] == f_) for f_ in sorted({x["fuente"] for x in ejemplos})},
                                    "aciertos_con_cogida_entre_aceptar_y_juzgar": sum(1 for x in ejemplos if x["tic_cogida"]), "aciertos_por_uso_de_un_botiquin_que_ya_llevaba": sum(1 for x in ejemplos if x["fuente"] == "huella" and not x["tic_cogida"])},
     "3_agarre": {"vidas_dia_con_la_falsa_activa": op, "con_la_falsa_aceptada": op_acept, "fraccion": round(op_acept / op, 4) if op else None},
     "4_confianza": {"valores": len(conf), "minimo": min(conf) if conf else None, "maximo": max(conf) if conf else None, "vacios_o_no_numericos": malos,
                     "arranques_dia_1": len(arranques_d1), "todos_empiezan_en_0_5": all(isinstance(a, dict) and all(a.get(k) == 0.5 for k in ("cuerpo", "recursos", "vinculo")) for a in arranques_d1)},
     "5_razon": {"llamadas": llamadas, "ilegibles": ilegibles, "fraccion_ilegible": round(ilegibles / llamadas, 4) if llamadas else None, "lineas_invalidas": sum(max(0, (r.get("lineas") or 0) - (r.get("invitaciones") or 0)) for r in raz), "lineas": sum(r.get("lineas") or 0 for r in raz)}}
c = R
R["criterios"] = {"menos_del_85_pct_de_fallos": (c["2_evaluaciones_de_la_falsa"]["fraccion_fallo"] or 0) < 0.85,
                  "falsa_en_la_razon_honesta": c["1_falsas_dichas"]["razon_honesta_MIENTE_UNA_a11"] > 0,
                  "confianza_fuera_de_0_1_vacia_o_arranque_no_0_5": bool(c["4_confianza"]["vacios_o_no_numericos"] or (c["4_confianza"]["minimo"] is not None and c["4_confianza"]["minimo"] < 0) or (c["4_confianza"]["maximo"] is not None and c["4_confianza"]["maximo"] > 1) or not c["4_confianza"]["todos_empiezan_en_0_5"]),
                  "mas_del_5_pct_de_respuestas_ilegibles": (c["5_razon"]["fraccion_ilegible"] or 0) > 0.05}
R["mecanica_correcta"] = not any(R["criterios"].values())
json.dump(R, open(os.path.join(AQUI, "P7_65_mecanica.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
