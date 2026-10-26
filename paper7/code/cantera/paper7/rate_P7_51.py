"""[P7-51] COMPROBACION SIN COSTE sobre el campo P7-50 (240 vidas validas + las apartadas), con lo que aporta Ari (zero-sum 0.1.19): 1 mensaje por 24 tics POR CRIATURA, comun a
todos los canales; un mensaje demasiado pronto se descarta y la observacion siguiente trae action_result "rate_limited"; bloqueo inicial de ~480 tics en que se puede hablar.
  (a) la guarda (guarda_latencia_P7_29) cuenta como bloqueados SOLO action_result == "blocked" (linea 32): aqui se cuentan los "rate_limited" por vida y brazo y se comprueba
      que no estan dentro de los bloqueados de la guarda (si lo estuvieran, se recalcula la guarda sin ellos).
  (b) mensajes descartados: cada tick con action_result "rate_limited" se atribuye al ultimo `talk` emitido (registro `voz` o `P7_48_mensaje` en los 2 tics anteriores): E2 (parte)
      o M7 (recuerdo); por brazo. Ademas: todos los action_result distintos, por brazo, y los mensajes enviados en el bloqueo inicial (tick < 480).
  python3 rate_P7_51.py -> P7_51_rate.json"""
import collections, glob, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs")
E = json.load(open(os.path.join(AQUI, "P7_50_estado.json")))
R = {"vidas": {}, "por_brazo": {}, "action_results": {}, "guarda": {}}
for pat, grupo in (("P750_s*", "campo"), ("P750r_s*", "apartadas")):
    for c in sorted(glob.glob(os.path.join(RUNS, pat))):
        b = os.path.basename(c).split("_"); S, d, brazo = int(b[1][1:]), int(b[2][1:]), b[3]
        for sl in (10, 11):
            fs = glob.glob(os.path.join(c, f"*policy_agent_{sl}.art.log"))
            if not fs: continue
            ar = collections.Counter(); rl = []; voces = {}; m7 = {}; T = 0; listos = 0; blocked = 0; rl_listos = 0; bloq_inicial = 0
            for line in open(fs[0], errors="replace"):
                if line.startswith('{"k":"tick"'):
                    r = json.loads(line)
                    if r.get("phase") != "live": continue
                    T += 1; a = r.get("action_result"); ar[str(a)] += 1; listo = (r.get("move_ready_in") or 0) == 0
                    if listo: listos += 1
                    if a == "blocked": blocked += 1
                    if a == "rate_limited":
                        rl.append(r["tick"])
                        if listo: rl_listos += 1
                elif line.startswith('{"k":"voz"'): r = json.loads(line); voces[r["tick"]] = r.get("texto", "")[:2]
                elif line.startswith('{"k":"P7_48_mensaje"'): r = json.loads(line); m7[r["tick"]] = True; bloq_inicial += (r["tick"] < 480)
            atrib = collections.Counter()
            for t in rl:
                prev = [t - k for k in (1, 2, 3) if (t - k) in m7 or (t - k) in voces]
                if not prev: atrib["sin talk previo"] += 1
                else:
                    tp = prev[0]; atrib["M7" if tp in m7 else ("E" + voces[tp][1:] if voces[tp].startswith("E") else voces[tp])] += 1
            R["vidas"][f"{grupo} s{S} d{d} {brazo} a{sl}"] = {"grupo": grupo, "brazo": brazo, "asiento": sl, "tics": T, "listos": listos, "blocked": blocked, "rate_limited": len(rl), "rate_limited_en_paso_listo": rl_listos, "atribucion": dict(atrib), "m7_enviados": len(m7), "m7_en_bloqueo_inicial": bloq_inicial, "partes": len(voces), "action_results": dict(ar)}
por = {}
for k, v in R["vidas"].items():
    if v["grupo"] != "campo": continue
    g = por.setdefault(v["brazo"], {"vidas": 0, "tics": 0, "listos": 0, "blocked": 0, "rate_limited": 0, "rate_limited_en_paso_listo": 0, "atribucion": collections.Counter(), "m7_enviados": 0, "partes": 0, "vidas_con_rate_limited": 0, "action_results": collections.Counter()})
    g["vidas"] += 1
    for kk in ("tics", "listos", "blocked", "rate_limited", "rate_limited_en_paso_listo", "m7_enviados", "partes"): g[kk] += v[kk]
    g["atribucion"].update(v["atribucion"]); g["action_results"].update(v["action_results"]); g["vidas_con_rate_limited"] += int(v["rate_limited"] > 0)
R["por_brazo"] = {b: {**{k: v for k, v in g.items() if k not in ("atribucion", "action_results")}, "atribucion": dict(g["atribucion"]), "action_results": dict(g["action_results"].most_common())} for b, g in por.items()}
# (a) la guarda: ¿cuenta rate_limited? Se compara el "bloqueados" de la guarda (estado) con los blocked del diario
comp = []
for p in E["peticiones"]:
    for sl, g in (p.get("latencia") or {}).items():
        k = f"campo s{p['serie']} d{p['dia']} {p['brazo']} a{sl}"; v = R["vidas"].get(k)
        if v: comp.append({"vida": k, "guarda_bloqueados": g.get("bloqueados"), "diario_blocked": v["blocked"], "diario_rate_limited": v["rate_limited"], "igual_a_blocked": g.get("bloqueados") == v["blocked"]})
R["guarda"] = {"vidas_comparadas": len(comp), "guarda_bloqueados_igual_a_blocked_del_diario": sum(1 for x in comp if x["igual_a_blocked"]), "ejemplos_distintos": [x for x in comp if not x["igual_a_blocked"]][:5], "rate_limited_total_campo": sum(v["rate_limited"] for v in R["vidas"].values() if v["grupo"] == "campo")}
json.dump(R, open(os.path.join(AQUI, "P7_51_rate.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(R["por_brazo"], ensure_ascii=False)); print(R["guarda"])
