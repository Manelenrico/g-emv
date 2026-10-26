"""[P7-67, campo, punto 5] COMPROBACION DEL HUMO (las 9 partidas del dia 1 de la serie 1 de cada brazo y nivel) -> P7_67F_humo.json. Por partida y asiento:
  - guarda de latencia (la de P7-65: pasa / marcada / regla dura);  - diario y cuaderno de fin;  - la imagen arranco con lo que toca: P7_67_arranque con los asientos activos del
    nivel (P7_67F_diseno.json), P7_67b_arranque, y en CONGELADA P7_67_congela_arranque;  - el juicio: registros P7_66_* y, en cada llegada, el acierto recalculado desde el registro
    (botiquin visto a <= 3 del destino) igual al apuntado;  - CONGELADA: la confianza al cerrar el dia es 0,5 en las tres dimensiones;  y al final, que analiza_P7_67.py corre.
  python3 verifica_humo_P7_67F.py"""
import glob, json, os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
D = json.load(open(os.path.join(AQUI, "P7_67F_diseno.json"))); E = json.load(open(os.path.join(AQUI, "P7_67F_estado.json")))
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
R = []; mal = []
for p in sorted(E["peticiones"], key=lambda p: (int(p["nivel"]), p["brazo"])):
    car = os.path.join(RAIZ, "paintball", "runs", f"P767F_n{p['nivel']}_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}")
    for sl in (10, 11):
        g = (p.get("latencia") or {}).get(str(sl)) or {}; f = glob.glob(os.path.join(car, f"*policy_agent_{sl}.art.log"))
        x = {"nivel": p["nivel"], "brazo": p["brazo"], "asiento": sl, "estado": p["estado"], "p95_ms": g.get("ms_p95"), "sobre_el_tic": g.get("sobre_el_tic"), "guarda_pasa": g.get("pasa"), "regla_dura": bool(g.get("para")),
             "diario": bool(f), "cuaderno_fin": False, "activos": None, "P7_67b": False, "congela_arranque": False, "eventos": {}, "aciertos_bien": 0, "aciertos_mal": 0, "conf_cierre": None, "congela_fijadas": 0}
        for l in (open(f[0], errors="replace") if f else []):
            if not l.startswith('{"k":"') or l.startswith('{"k":"tick"'): continue
            k = l[6:l.index('"', 6)]
            if k == "P7_cuaderno" and '"momento":"fin"' in l: x["cuaderno_fin"] = True
            elif k == "P7_67_arranque": x["activos"] = json.loads(l)["activos"]
            elif k == "P7_67b_arranque": x["P7_67b"] = True
            elif k == "P7_67_congela_arranque": x["congela_arranque"] = True
            elif k == "P7_67_congela": x["congela_fijadas"] += 1
            elif k == "P7_54_cierre": x["conf_cierre"] = json.loads(l)["confianza"]
            elif k.startswith("P7_66_") and k not in ("P7_66_arranque", "P7_66_cierre"):
                x["eventos"][k] = x["eventos"].get(k, 0) + 1
                if k == "P7_66_llegada":
                    r = json.loads(l); calc = 1 if any(cheb(tuple(b), tuple(r["destino"])) <= 3 for b in r["botiquines_vistos"]) else 0
                    x["aciertos_bien" if calc == r["acierto_recursos"] else "aciertos_mal"] += 1
        ok = (x["estado"] == "completed" and x["diario"] and x["cuaderno_fin"] and not x["regla_dura"] and x["activos"] == D["activos"][p["nivel"]] and x["P7_67b"] and x["aciertos_mal"] == 0
              and x["congela_arranque"] == (p["brazo"] == "CONGELADA") and (p["brazo"] != "CONGELADA" or x["conf_cierre"] == {"cuerpo": 0.5, "recursos": 0.5, "vinculo": 0.5}))
        x["pasa"] = ok; R.append(x)
        if not ok: mal.append(f"n{p['nivel']} {p['brazo']} {sl}")
an = subprocess.run([sys.executable, os.path.join(AQUI, "analiza_P7_67.py")], capture_output=True, text=True)
out = {"partidas": len(E["peticiones"]), "completadas": sum(1 for p in E["peticiones"] if p["estado"] == "completed"), "reintentos": len(E.get("reintentos", [])), "asientos": R, "no_pasan": mal,
       "guarda_marcadas": [f"n{x['nivel']} {x['brazo']} {x['asiento']}" for x in R if x["guarda_pasa"] is False], "p95_max": max((x["p95_ms"] or 0) for x in R),
       "analisis_corre": an.returncode == 0, "analisis_salida": (an.stdout + an.stderr)[-1500:]}
out["humo_pasa"] = not mal and out["analisis_corre"] and out["completadas"] == 9
json.dump(out, open(os.path.join(AQUI, "P7_67F_humo.json"), "w"), ensure_ascii=False, indent=1)
for x in R: print(x["nivel"], x["brazo"], x["asiento"], "p95", x["p95_ms"], "guarda", x["guarda_pasa"], "fin", x["cuaderno_fin"], "activos", x["activos"], "67b", x["P7_67b"], "congela", x["congela_arranque"], x["congela_fijadas"], "conf", x["conf_cierre"], x["eventos"], "aciertos ok/mal", x["aciertos_bien"], x["aciertos_mal"], "PASA" if x["pasa"] else "NO PASA")
print("analisis:", out["analisis_salida"]); print("HUMO", "PASA" if out["humo_pasa"] else "NO PASA", out["no_pasan"])
