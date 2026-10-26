"""[P7-56, Manel 13-oct] INCIDENCIAS Y LENTITUD POR BRAZO: tabla de reintentos y apartadas (brazo, dia, asiento, motivo, hora de la peticion), % de decisiones sobre el tic por brazo y
dia (media de los dos asientos; y el maximo), medianas de ms por brazo; y lo que distingue a los dos brazos: la razon entre dias (segundos por noche), el tamano del archivo de
invitaciones horneado, los segundos de horneado por imagen, la hora a la que caen las peticiones y cuantas partidas habia en vuelo al pedir cada una.  python3 incidencias_P7_56.py -> P7_56_incidencias.json"""
import datetime as dt, glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); E = json.load(open(os.path.join(AQUI, "P7_56_estado.json"))); BR = ("CON_RAZON", "SIN_RAZON")
def hora(s): return s[11:16] if s else "—"
# 1. incidencias
INC = []
for r in E.get("reintentos", []): INC.append({"tipo": "reintento", "serie": r["serie"], "dia": r["dia"], "brazo": r["brazo"], "pedida": hora(r.get("pedida_a_las")), "apartada": r.get("apartado_a_las", "")[11:16], "motivo": r["motivo"][:90], "latencia": {sl: {k: g.get(k) for k in ("ms_mediana", "sobre_el_tic", "fraccion_sin_cuerpo", "pasa")} for sl, g in (r.get("latencia") or {}).items()}})
for r in E.get("apartadas", []): INC.append({"tipo": "apartada", "serie": r["serie"], "dia": r["dia"], "brazo": r["brazo"], "pedida": hora(r.get("pedida_a_las")), "motivo": r["motivo"][:90]})
por_brazo = {b: {"reintentos": sum(1 for x in INC if x["tipo"] == "reintento" and x["brazo"] == b), "apartadas": sum(1 for x in INC if x["tipo"] == "apartada" and x["brazo"] == b), "marcadas": sum(1 for p in E["peticiones"] if p["brazo"] == b for g in (p.get("latencia") or {}).values() if not g.get("pasa"))} for b in BR}
# 2. % sobre el tic por brazo y dia
P = [p for p in E["peticiones"] if p["estado"] == "completed"]
sobre = {b: {} for b in BR}; med = {b: [] for b in BR}; p95 = {b: [] for b in BR}
for p in P:
    gs = [g for g in (p.get("latencia") or {}).values() if g.get("ms_mediana") is not None]
    if not gs: continue
    sobre[p["brazo"]].setdefault(p["dia"], []).append(100 * st.mean(g.get("sobre_el_tic") or 0 for g in gs)); med[p["brazo"]] += [g["ms_mediana"] for g in gs]; p95[p["brazo"]] += [g.get("ms_p95") or 0 for g in gs]
tabla_dia = {b: {d: round(st.mean(v), 2) for d, v in sorted(sobre[b].items())} for b in BR}
resumen = {b: {"vidas": len(med[b]), "mediana_ms_media": round(st.mean(med[b]), 2), "mediana_ms_max": round(max(med[b]), 2), "p95_max": round(max(p95[b]), 1), "sobre_tic_media_pct": round(st.mean(x for v in sobre[b].values() for x in v), 3), "vidas_lentas_mediana_mayor_8ms": sum(1 for m in med[b] if m > 8.0)} for b in BR}
# 3. lo que distingue a los brazos
IM = E["imagenes"]; horneado = {b: [IM[k]["segundos"] for k in IM if k.startswith(b)] for b in BR}
inv_bytes = [os.path.getsize(f) for f in glob.glob(os.path.join(AQUI, "cuadernos_P7_56", "CON_RAZON_serie*", "invitaciones_P7_*.json"))]; cuad_bytes = [os.path.getsize(f) for f in glob.glob(os.path.join(AQUI, "cuadernos_P7_56", "*", "cuaderno_P7_*.json"))]
razon_seg = [r.get("segundos") for r in E.get("razon", []) if r.get("segundos")]
# hora de peticion y partidas en vuelo al pedir (contadas con pedida/completada del estado)
def en_vuelo(t):
    return sum(1 for q in E["peticiones"] + E.get("reintentos", []) if q.get("pedida_a_las") and q["pedida_a_las"] <= t and (q.get("completada_a_las") or "9") > t)
vuelo = {b: [en_vuelo(p["pedida_a_las"]) for p in P if p["brazo"] == b and p.get("pedida_a_las")] for b in BR}
horas = {b: sorted(hora(p.get("pedida_a_las")) for p in P if p["brazo"] == b)[::max(1, len(P) // 20)] for b in BR}
lentas = [(p["brazo"], p["serie"], p["dia"], hora(p.get("pedida_a_las")), round(g["ms_mediana"], 1), round(100 * (g.get("sobre_el_tic") or 0), 2)) for p in P for sl, g in (p.get("latencia") or {}).items() if g.get("ms_mediana") and g["ms_mediana"] > 8.0]
lentas_inc = [(x["brazo"], x["serie"], x["dia"], x["pedida"]) for x in INC if x["tipo"] == "reintento"]
R = {"incidencias": INC, "por_brazo": por_brazo, "sobre_tic_por_dia": tabla_dia, "resumen": resumen, "horneado_segundos": {b: (round(st.mean(v), 1), round(max(v), 1)) if v else None for b, v in horneado.items()}, "invitaciones_bytes": (min(inv_bytes), max(inv_bytes)) if inv_bytes else None, "cuaderno_bytes": (min(cuad_bytes), max(cuad_bytes)) if cuad_bytes else None,
     "razon_segundos": (round(st.mean(razon_seg), 1), round(max(razon_seg), 1)) if razon_seg else None, "en_vuelo_al_pedir": {b: round(st.mean(v), 2) for b, v in vuelo.items() if v}, "vidas_lentas": lentas, "horas_muestra": horas}
json.dump(R, open(os.path.join(AQUI, "P7_56_incidencias.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k not in ("incidencias", "sobre_tic_por_dia", "horas_muestra")}, ensure_ascii=False)[:1500]); print("incidencias", [(x["tipo"], x["brazo"], x["serie"], x["dia"], x["pedida"], x["motivo"][:40]) for x in INC])
