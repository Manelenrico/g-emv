"""[P7-62] RESUMEN para el informe (ninguna cifra a mano): pruebas (P7_62_pruebas.json), comprobacion local en lazo cerrado (P7_62_local.json y sus diarios) y COSTE ESTIMADO de un
campo de 2 brazos (MIENTEN_DOS, MIENTE_UNA) x 3 series, medido sobre P7-61 (P7_57_estado.json: partidas, llamadas a la razon y su coste, horas por serie).
  python3 resumen_P7_62.py -> P7_62_resumen.json"""
import datetime as dt, glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); L = json.load(open(os.path.join(AQUI, "P7_62_local.json"))); E = json.load(open(os.path.join(AQUI, "P7_57_estado.json")))
R = {"pruebas": json.load(open(os.path.join(AQUI, "P7_62_pruebas.json"))), "local": {}}
for d in ("d1", "d2", "d3"):
    for sl, v in L[d]["vidas"].items():
        if sl not in ("10", "11", "12", "13"): continue
        g = v["P7_57"]; f = os.path.join(AQUI, "_P7_62_local", d, "logs", f"policy_agent_{sl}.log"); txt = open(f, errors="replace").read().split("\n") if os.path.exists(f) else []
        R["local"][f"{d} a{sl}"] = {"ms_p95": v.get("ms_p95"), "invitaciones": (g.get("arranque") or {}).get("invitaciones"), "falsas": (g.get("arranque") or {}).get("falsas"),
            "evaluadas_62": [{"accion": e["accion"], "falsa": e["falsa"], "fuente": e["fuente"], "hueco": e.get("hueco"), "hp0": e.get("hp0"), "vivido": e["vivido"]["cuerpo"], "acierto": e["acierto"]["cuerpo"]} for e in g.get("evaluadas62", [])],
            "contrastes_62": len(g.get("contrastes62", [])), "contrastes_falsa": sum(1 for c in g.get("contrastes62", []) if c["falsa"]), "amenaza_de_los_recuerdos": [c["amenaza_recuerdo"] for c in g.get("contrastes62", [])],
            "fuera_de_situacion": ((g.get("cierre62") or {}).get("n") or {}).get("fuera_de_situacion"), "curas_juzgadas_por_P7_54": sum(1 for l in txt if l.startswith('{"k":"P7_54_evaluada"') and '"accion":"USAR_' in l),
            "mensajes_malos": sum(1 for l in txt if l.startswith('{"k":"P7_48_mensaje_malo"')), "mensajes_con_amenaza": sum(1 for l in txt if l.startswith('{"k":"P7_48_mensaje"') and any(f" {o}{s}{k} " in l for o in "brnc" for s in "df" for k in "23"))}
R["local_razon"] = {"llamadas": len(L.get("razon", [])), "usd": round(sum(r["usd_supuesto"] for r in L.get("razon", [])), 4)}
# coste estimado: lo medido en P7-61
raz = E.get("razon", []); usd_llamada = sum(r["usd_supuesto"] for r in raz) / len(raz)
horas = []
for S in (1, 2, 3):
    P = [p for p in E["peticiones"] if p["serie"] == S]
    t0 = min(dt.datetime.fromisoformat(p["pedida_a_las"].replace("Z", "+00:00")) for p in P); t1 = max(dt.datetime.fromisoformat(p["completada_a_las"].replace("Z", "+00:00")) for p in P if p.get("completada_a_las"))
    horas.append((t1 - t0).total_seconds() / 3600)
partidas = 2 * 3 * 20; humo = 3; reint = len(E.get("reintentos", [])); llamadas = 2 * 3 * 19 * 2
R["coste_estimado"] = {"partidas_campo": partidas, "humo": humo, "reintentos_previstos_como_P7_61": reint, "creditos_plataforma": partidas + humo + reint,
                       "llamadas_razon": llamadas + 2 * 2, "usd_por_llamada_P7_61": round(usd_llamada, 4), "usd_consola": round((llamadas + 4) * usd_llamada, 2),
                       "horas_por_serie_P7_61": [round(h, 1) for h in horas], "horas_campo": round(sum(horas), 1), "recarga_diaria": 71,
                       "nota": "1 credito por partida (alguna cuenta 0); llamadas = 2 brazos x 3 series x 19 noches x 2 hermanas (en MIENTE_UNA la honesta tambien llama) + 4 del humo"}
json.dump(R, open(os.path.join(AQUI, "P7_62_resumen.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(R["coste_estimado"]), R["local_razon"])
