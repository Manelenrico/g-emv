"""[P7-62] LA REGLA DEL MUNDO FRENTE A LA MARCA DEL CUERPO, sobre las series 1-3 de P7-61 (descriptivo, coste cero): para cada uso del botiquin (huella), cortado por la regla del mundo
(golpe en [t0, t0 + use_ticks del catalogo]) frente a la marca de corte de la huella (corte y dano_total > 0, la que usaba invita_P7_54 y analiza); y las evaluaciones de la falsa de P7-61
rejuzgadas con juicio_P7_62.juicio (los golpes de los tics del diario; las curas de antes, tal cual). python3 cortes_P7_62.py -> P7_62_cortes.json"""
import glob, json, os, random, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path[:0] = [AQUI, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "cantera", "paper6"), RAIZ]
import juicio_P7_62 as J, mentira_P7_57 as MT
E = json.load(open(os.path.join(AQUI, "P7_57_estado.json"))); R = {"usos": 0, "regla_si_marca_si": 0, "regla_si_marca_no": 0, "regla_no_marca_si": 0, "regla_no_marca_no": 0, "falsa": []}
CANAL = None
for p in E["peticiones"]:
    for sl in (10, 11):
        fs = glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P757_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}", f"*policy_agent_{sl}.art.log"))
        if not fs: continue
        golpes = []; H = []; AC = []; EV = []; ninv = None
        for l in open(fs[0], errors="replace"):
            if l.startswith('{"k":"tick"'):
                r = json.loads(l)
                if r.get("phase") == "live" and any(float(d.get("amount") or 0) > 0 for d in (r.get("damage_taken") or [])): golpes.append(r["tick"])
            elif l.startswith('{"k":"P7_huella"'): H.append(json.loads(l))
            elif l.startswith('{"k":"catalogo"') and CANAL is None: CANAL = {it["id"]: int(it.get("use_ticks") or 0) for it in json.loads(l)["items"]}
            elif l.startswith('{"k":"P7_54_aceptada"'): AC.append(json.loads(l))
            elif l.startswith('{"k":"P7_54_evaluada"'): EV.append(json.loads(l))
            elif l.startswith('{"k":"P7_57_arranque"'): ninv = json.loads(l)["invitaciones"]
        for h in H:
            if (h.get("objeto") or "first_aid") != "first_aid": continue
            h = dict(h, objeto="first_aid"); regla = J.cortada(h, golpes, CANAL, {"first_aid"}); marca = bool(h.get("corte")) and float(h.get("dano_total") or 0) > 0
            R["usos"] += 1; R[f"regla_{'si' if regla else 'no'}_marca_{'si' if marca else 'no'}"] += 1
        if MT.miente(p["brazo"], sl, p["dia"]) and ninv:
            pos = random.Random(1000 * p["serie"] + 10 * (p["dia"] - 1) + sl).randint(0, ninv - 1)
            for e in EV:
                if e["n"] != pos: continue
                a = max([x for x in AC if x["n"] == pos and x["tick"] <= e["tick"]], key=lambda x: x["tick"])
                ab = {"inv": dict(MT.FALSA), "t0": a["tick"], "hp0": 0.0, "W0": None, "B0": None, "objeto": "first_aid", "n_huellas0": 0}
                hs = sorted([dict(h, objeto=h.get("objeto") or "first_aid") for h in H], key=lambda h: int(h["t0"]))
                r = J.juicio(ab, hs, a["tick"] + 10 ** 6, 0.0, None, None, golpes, CANAL, {"first_aid"})
                R["falsa"].append({"serie": p["serie"], "dia": p["dia"], "brazo": p["brazo"], "asiento": sl, "antes": e["acierto"]["cuerpo"], "ahora": r[1]["cuerpo"] if r else None, "fuente_ahora": r[2] if r else None})
F = R["falsa"]; R["canal"] = CANAL
R["falsa_resumen"] = {"evaluaciones": len(F), "aciertos_antes": sum(1 for x in F if x["antes"] == 1), "aciertos_ahora": sum(1 for x in F if x["ahora"] == 1), "cortadas_ahora": sum(1 for x in F if x["fuente_ahora"] == "cortada por golpe"),
                      "cambian": sum(1 for x in F if x["antes"] != x["ahora"])}
json.dump(R, open(os.path.join(AQUI, "P7_62_cortes.json"), "w"), ensure_ascii=False, indent=1); print({k: v for k, v in R.items() if k != "falsa"})
