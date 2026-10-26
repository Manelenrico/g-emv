"""[P7-67, diagnostico de la parada, punto 4] SIN mirar resultados del sello: en todas las partidas completadas del campo (paintball/runs/P767F_*), por vida, los pasos listos y los
bloqueados sin cuerpo (la misma regla que guarda_latencia_P7_29.mide), y para cada bloqueo sin cuerpo si `ir_sitio` estaba activo: (a) el cuerpo habia elegido `ir_sitio` en la decision
que dio el paso, o (b) habia un intento de ir_sitio abierto (entre P7_66_aceptada y su cierre). Todo junto, sin separar por brazo ni nivel.  -> P7_67F_bloqueos.json"""
import glob, json, os, zipfile
AQUI = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "paintball", "runs")
DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0), "NE": (1, -1), "NW": (-1, -1), "SE": (1, 1), "SW": (-1, 1)}
def lineas(car, sl):
    a = glob.glob(os.path.join(car, f"*policy_agent_{sl}.art.log"))
    if a: yield from open(a[0], errors="replace"); return
    with zipfile.ZipFile(glob.glob(os.path.join(car, f"*policy_agent_{sl}.zip"))[0]) as Z, Z.open(Z.namelist()[0]) as fh:
        for b in fh: yield b.decode(errors="replace")
E = json.load(open(os.path.join(AQUI, "P7_67F_estado.json"))); V = []
for p in E["peticiones"]:
    if p["estado"] != "completed": continue
    car = os.path.join(RUNS, f"P767F_n{p['nivel']}_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}")
    for sl in (10, 11):
        prev = None; abierta = False; listos = bl = 0; con_el = con_ab = 0; dest = {}
        for l in lineas(car, sl):
            if l.startswith('{"k":"P7_66_aceptada"'): abierta = True; continue
            if l.startswith('{"k":"P7_66_llegada"') or l.startswith('{"k":"P7_66_interrumpida"') or l.startswith('{"k":"P7_66_no_llego"'): abierta = False; continue
            if not l.startswith('{"k":"tick"') or '"phase":"live"' not in l: continue
            r = json.loads(l)
            if (r.get("move_ready_in") or 0) == 0:
                listos += 1
                if r.get("action_result") == "blocked" and prev:
                    it = prev.get("intencion") or {}; sin = True
                    if it.get("do") == "move" and it.get("dir") in DIRS:
                        dx, dy = DIRS[it["dir"]]; tgt = (prev["pos"][0] + dx, prev["pos"][1] + dy)
                        sin = not any(tuple(a.get("pos") or ()) == tgt for a in (prev.get("ve_agentes") or []))
                        if sin: dest[str(tgt)] = dest.get(str(tgt), 0) + 1
                    if sin:
                        bl += 1; el = (prev.get("RADIOGRAFIA") or {}).get("elegido"); con_el += el == "ir_sitio"; con_ab += abierta
            prev = r
        top = max(dest.items(), key=lambda kv: kv[1]) if dest else None
        V.append({"partida": f"n{p['nivel']}_s{p['serie']}_d{p['dia']}_{p['brazo']}", "asiento": sl, "pasos_listos": listos, "bloqueados_sin_cuerpo": bl, "fraccion": bl / listos if listos else 0,
                  "con_ir_sitio_elegido": con_el, "con_intento_abierto": con_ab, "casilla_mas_repetida": top})
tot = sum(v["bloqueados_sin_cuerpo"] for v in V)
R = {"vidas": len(V), "pasos_listos": sum(v["pasos_listos"] for v in V), "bloqueados_sin_cuerpo": tot,
     "vidas_por_encima": {u: sum(1 for v in V if v["fraccion"] > u) for u in ("0.01", "0.02", "0.05")} if False else {f"> {int(100 * u)} %": sum(1 for v in V if v["fraccion"] > u) for u in (0.01, 0.02, 0.05)},
     "parte_con_ir_sitio_elegido": sum(v["con_ir_sitio_elegido"] for v in V) / tot if tot else None, "parte_con_intento_abierto": sum(v["con_intento_abierto"] for v in V) / tot if tot else None,
     "bloqueados_con_ir_sitio_elegido": sum(v["con_ir_sitio_elegido"] for v in V), "bloqueados_con_intento_abierto": sum(v["con_intento_abierto"] for v in V),
     "vidas_mas_de_1_por_ciento": sorted([v for v in V if v["fraccion"] > 0.01], key=lambda v: -v["fraccion"]),
     "vidas_con_algun_bloqueo_y_ir_sitio": sorted([v for v in V if v["con_ir_sitio_elegido"] or v["con_intento_abierto"]], key=lambda v: -(v["con_ir_sitio_elegido"] + v["con_intento_abierto"]))[:15],
     "fracciones_ordenadas_top10": sorted([round(v["fraccion"], 4) for v in V], reverse=True)[:10]}
json.dump({"resumen": R, "vidas": V}, open(os.path.join(AQUI, "P7_67F_bloqueos.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k not in ("vidas_mas_de_1_por_ciento", "vidas_con_algun_bloqueo_y_ir_sitio")}, ensure_ascii=False, indent=1))
for v in R["vidas_mas_de_1_por_ciento"]: print("  >1%:", v["partida"], v["asiento"], round(100 * v["fraccion"], 2), "%", v["bloqueados_sin_cuerpo"], "elegido ir_sitio", v["con_ir_sitio_elegido"], "intento abierto", v["con_intento_abierto"], v["casilla_mas_repetida"])
for v in R["vidas_con_algun_bloqueo_y_ir_sitio"]: print("  con ir_sitio:", v["partida"], v["asiento"], v["bloqueados_sin_cuerpo"], "elegido", v["con_ir_sitio_elegido"], "abierto", v["con_intento_abierto"], round(100 * v["fraccion"], 2), "%")
