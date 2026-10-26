"""[P7-67, campo, EXPLORATORIO, NO SELLADO] dos preguntas descriptivas de Manel (20-oct), leyendo los diarios del campo (art.log o zip), sin tocar nada sellado -> P7_67_explora.json
  1. MIENTE y CONGELADA, nivel 1, días 16-20: criatura-días sin oportunidad. Para cada uno: si la invitación se cargó (P7_66_arranque) y, en los 300 primeros tics vivos (el tramo), en cuántos se
     cumplía cada condición de invita_P7_66b para ofrecer `ir_sitio`: destino a 8-15 de ella; destino a 8-15 de su hermana (posición de su propio diario en ese tic); calma (ningún rival activo
     a <= 5 visible y ningún golpe en 48 tics); destino transitable en el mapa fijo (`static_map`); viva.
  2. HONESTA, nivel 1, días 11-20: en cada llegada, los botiquines que ve la criatura (el diario solo trae lo visible; los del mapa entero no constan) y el más cercano al destino; y si el destino
     estaba dentro de la zona segura (centro y radio de la zona en el tic de la llegada, distancia euclídea al centro <= radio).
  python3 explora_P7_67_campo.py"""
import glob, json, math, os, zipfile, collections
AQUI = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "paintball", "runs")
E = json.load(open(os.path.join(AQUI, "P7_67F_estado.json"))); D = json.load(open(os.path.join(AQUI, "P7_67F_diseno.json"))); R = json.load(open(os.path.join(AQUI, "P7_67_analisis.json")))
ACT = set(D["activos"]["1"]); EMPUJE = 300
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
def lineas(car, sl):
    a = glob.glob(os.path.join(car, f"*policy_agent_{sl}.art.log"))
    if a: yield from open(a[0], errors="replace"); return
    with zipfile.ZipFile(glob.glob(os.path.join(car, f"*policy_agent_{sl}.zip"))[0]) as Z, Z.open(Z.namelist()[0]) as fh:
        for b in fh: yield b.decode(errors="replace")
SEM = {(p["nivel"], p["serie"], p["dia"], p["brazo"]): p["semilla"] for p in E["peticiones"] if p["estado"] == "completed"}
def car(s, d, b): return os.path.join(RUNS, f"P767F_n1_s{s}_d{d}_{b}_{SEM[('1', s, d, b)]}")
def posiciones(c, sl, hasta):
    """tic relativo -> (pos, obs) de los primeros `hasta` tics vivos, más el mapa y la invitación"""
    T = {}; tic0 = None; mapa = None; inv = None; golpe = -10 ** 9
    for l in lineas(c, sl):
        if l.startswith('{"k":"static_map"') and mapa is None: mapa = json.loads(l)
        elif l.startswith('{"k":"P7_66_arranque"'): inv = json.loads(l).get("invitaciones_sitio")
        elif l.startswith('{"k":"tick"') and '"phase":"live"' in l:
            r = json.loads(l); t = r["tick"]; tic0 = t if tic0 is None else tic0
            if t - tic0 >= hasta: break
            if any(float(x.get("amount") or 0) > 0 for x in (r.get("damage_taken") or [])): golpe = t
            riv = [cheb(tuple(r["pos"]), tuple(a["pos"])) for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("slot") in ACT]
            Rg = r.get("RADIOGRAFIA") or {}
            T[t - tic0] = {"pos": tuple(r["pos"]), "calma": not (riv and min(riv) <= 5) and t - golpe > 48, "n_cand": int(Rg.get("n_cand") or 0), "ir_sitio": "ir_sitio" in (Rg.get("candidatos") or {})}
    return T, mapa, inv

# 1 ── días 16-20 sin oportunidad
P1 = []
for c in R["criatura_dias_detalle"]:
    if c["nivel"] != "1" or c["brazo"] not in ("MIENTE", "CONGELADA") or c["dia"] < 16 or c["oportunidad"]: continue
    s, d, b, sl = c["serie"], c["dia"], c["brazo"], c["slot"]; dest = tuple(D["destinos"][b][str(d)]); cc = car(s, d, b)
    A, mapa, inv = posiciones(cc, sl, EMPUJE); H, _, _ = posiciones(cc, sl ^ 1, EMPUJE)
    ch = mapa["filas"][dest[1]][dest[0]]; legend = mapa["legend"].get(ch, ch)
    n = len(A); ella = sum(8 <= cheb(v["pos"], dest) <= 15 for v in A.values()); herm = sum(1 for t, v in A.items() if t in H and 8 <= cheb(H[t]["pos"], dest) <= 15)
    ambas = sum(1 for t, v in A.items() if 8 <= cheb(v["pos"], dest) <= 15 and (t not in H or 8 <= cheb(H[t]["pos"], dest) <= 15))
    todo = sum(1 for t, v in A.items() if v["calma"] and 8 <= cheb(v["pos"], dest) <= 15 and (t not in H or 8 <= cheb(H[t]["pos"], dest) <= 15))
    # [tic a tic] solo cuentan los tics con más de un candidato (con uno solo, `noop`, el cuerpo no ofrece ningún movimiento: ARREGLO A del decisor)
    eleg = [t for t, v in A.items() if v["n_cand"] > 1]
    todo_eleg = sum(1 for t in eleg if A[t]["calma"] and 8 <= cheb(A[t]["pos"], dest) <= 15 and (t not in H or 8 <= cheb(H[t]["pos"], dest) <= 15))
    falla_h = sum(1 for t in eleg if t in H and not (8 <= cheb(H[t]["pos"], dest) <= 15)); falla_e = sum(1 for t in eleg if not (8 <= cheb(A[t]["pos"], dest) <= 15)); falla_c = sum(1 for t in eleg if not A[t]["calma"])
    primer_paso_hermana = next((cheb(H[t]["pos"], dest) for t in sorted(H) if H[t]["pos"] != H[min(H)]["pos"]), None) if H else None
    d0e = cheb(A[min(A)]["pos"], dest) if A else None; d0h = cheb(H[min(H)]["pos"], dest) if H else None
    P1.append({"serie": s, "dia": d, "brazo": b, "asiento": sl, "destino": list(dest), "casilla": legend, "invitacion_cargada": bool(inv), "tics_vivos_en_el_tramo": n,
               "tics_ella_8_15": ella, "tics_hermana_8_15": herm, "tics_las_dos_8_15": ambas, "tics_en_calma": sum(v["calma"] for v in A.values()), "tics_todo_a_la_vez": todo,
               "distancia_al_empezar_ella": d0e, "distancia_al_empezar_hermana": d0h, "tics_con_eleccion": len(eleg), "tics_con_eleccion_y_todo": todo_eleg,
               "tics_con_eleccion_hermana_fuera_8_15": falla_h, "tics_con_eleccion_ella_fuera_8_15": falla_e, "tics_con_eleccion_sin_calma": falla_c,
               "distancia_hermana_tras_su_primer_paso": primer_paso_hermana, "ir_sitio_ofrecido_algun_tic": any(v["ir_sitio"] for v in A.values())})
# los dos criatura-días del día 19 que sí tuvieron oportunidad, para comparar
CON = [{"serie": c["serie"], "brazo": c["brazo"], "asiento": c["slot"], "tic_oportunidad": c["tic_oportunidad"]} for c in R["criatura_dias_detalle"] if c["nivel"] == "1" and c["brazo"] in ("MIENTE", "CONGELADA") and c["dia"] == 19 and c["oportunidad"]]

# 2 ── HONESTA, llegadas de los días 11-20
P2 = []
for c in R["criatura_dias_detalle"]:
    if c["nivel"] != "1" or c["brazo"] != "HONESTA" or c["dia"] < 11 or not c["llegadas"]: continue
    s, d, sl = c["serie"], c["dia"], c["slot"]; cc = car(s, d, "HONESTA"); lle = None; prox = None
    for l in lineas(cc, sl):
        if l.startswith('{"k":"P7_66_llegada"') and lle is None: lle = json.loads(l)
        elif lle is not None and l.startswith('{"k":"tick"') and '"phase":"live"' in l:
            r = json.loads(l)
            if r["tick"] >= lle["tick"] + 1: prox = r; break
    dest = tuple(lle["destino"]); kits = [tuple(k) for k in lle["botiquines_vistos"]]
    z = (prox or {}).get("zona") or {}; cen = z.get("center"); rad = z.get("radius")
    P2.append({"serie": s, "dia": d, "asiento": sl, "destino": list(dest), "tic": lle["tick"], "acierto": lle["acierto_recursos"], "botiquines_vistos": len(kits),
               "mas_cercano_al_destino": (min(cheb(k, dest) for k in kits) if kits else None), "zona_centro": cen, "zona_radio": rad,
               "destino_dentro_de_la_zona": (math.dist(dest, cen) <= rad) if cen and rad is not None else None})
def por_dia(rows):
    out = {}
    for d in sorted({r["dia"] for r in rows}):
        rs = [r for r in rows if r["dia"] == d]; vis = [r["botiquines_vistos"] for r in rs]; mc = [r["mas_cercano_al_destino"] for r in rs if r["mas_cercano_al_destino"] is not None]
        out[d] = {"destino": rs[0]["destino"], "llegadas": len(rs), "aciertos": sum(r["acierto"] for r in rs), "sin_botiquin_a_la_vista": sum(1 for v in vis if v == 0),
                  "botiquines_vistos_mediana": sorted(vis)[len(vis) // 2], "mas_cercano_mediana": (sorted(mc)[len(mc) // 2] if mc else None),
                  "destino_dentro_de_la_zona": sum(1 for r in rs if r["destino_dentro_de_la_zona"]), "tic_llegada_mediana": sorted(r["tic"] for r in rs)[len(rs) // 2],
                  "radio_zona": sorted({r["zona_radio"] for r in rs if r["zona_radio"] is not None})}
    return out
TIC_OP = collections.Counter(c["tic_oportunidad"] for c in R["criatura_dias_detalle"] if c["oportunidad"])
POR_DEST = {}
for c in R["criatura_dias_detalle"]:
    if c["nivel"] == "1" and c["brazo"] == "HONESTA" and c["llegadas"]:
        k = str(tuple(D["destinos"]["HONESTA"][str(c["dia"])])); x = POR_DEST.setdefault(k, {"dias": set(), "llegadas": 0, "aciertos": 0}); x["dias"].add(c["dia"]); x["llegadas"] += c["llegadas"]; x["aciertos"] += c["aciertos"]
POR_DEST = {k: {"dias": sorted(v["dias"]), "llegadas": v["llegadas"], "aciertos": v["aciertos"]} for k, v in POR_DEST.items()}
RES = {"nota": "EXPLORATORIO, NO SELLADO", "tic_de_la_primera_oferta_en_todo_el_campo": {"minimo": min(TIC_OP), "en_el_tic_0": TIC_OP.get(0, 0), "criatura_dias_con_oferta": sum(TIC_OP.values())},
       "honesta_aciertos_por_destino_dias_1_20": POR_DEST, "pregunta_1": {"sin_oportunidad": P1, "con_oportunidad_dia_19": CON,
       "resumen": {"criatura_dias_con_0_tics_" + k: sum(1 for r in P1 if r[k] == 0) for k in ("tics_ella_8_15", "tics_hermana_8_15", "tics_las_dos_8_15", "tics_en_calma", "tics_todo_a_la_vez", "tics_con_eleccion_y_todo")} | {"total": len(P1),
                   "ir_sitio_ofrecido_algun_tic": sum(r["ir_sitio_ofrecido_algun_tic"] for r in P1), "tics_con_eleccion": sum(r["tics_con_eleccion"] for r in P1),
                   "de_ellos_hermana_fuera_8_15": sum(r["tics_con_eleccion_hermana_fuera_8_15"] for r in P1), "de_ellos_ella_fuera_8_15": sum(r["tics_con_eleccion_ella_fuera_8_15"] for r in P1),
                   "de_ellos_sin_calma": sum(r["tics_con_eleccion_sin_calma"] for r in P1),
                   "distancia_hermana_tras_su_primer_paso": dict(collections.Counter(r["distancia_hermana_tras_su_primer_paso"] for r in P1)),
                   "casillas": dict(collections.Counter(r["casilla"] for r in P1)), "invitacion_cargada": sum(r["invitacion_cargada"] for r in P1),
                   "distancia_al_empezar_ella": dict(collections.Counter(r["distancia_al_empezar_ella"] for r in P1)), "distancia_al_empezar_hermana": dict(collections.Counter(r["distancia_al_empezar_hermana"] for r in P1))}},
       "pregunta_2": {"por_dia": por_dia(P2), "llegadas": P2}}
json.dump(RES, open(os.path.join(AQUI, "P7_67_explora.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(RES["pregunta_1"]["resumen"], ensure_ascii=False)); print("con oportunidad d19:", CON)
for d, v in RES["pregunta_2"]["por_dia"].items(): print(d, v)
