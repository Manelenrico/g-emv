"""[P7-13] LECTURA DEL HUMO (3 dias, APRENDE, pedir encendido): de los diarios de paintball/runs/P713_s1_d<D>_APRENDE_<semilla>/ (fuera de git).
Por dia y criatura: partes emitidos y cuantos llevan el pedido; pedidos abiertos y cerrados y por que (registro `P7_pido` del emisor: "lo lleva",
"lo ve", "ya no le alivia"); para los cerrados con "lo lleva" o "lo ve", si el botiquin que coge despues lo habia soltado el hermano; regalos
(`soltar_first_aid` ejecutado) con o sin pedido (ultimo parte del hermano emitido antes de la decision y con edad <= la caducidad del parte,
leida de `alma/parte.py`); su destino; y los tics yendo a por botiquines. Las medidas de regalos, recogidas y tiempo son las de
`analiza_P7_11.py` (mismas definiciones). -> P7_13_humo.json"""
import glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "paintball")): sys.path.insert(0, p)
import analiza_P7_11 as A11
from alma import parte as PARTE
def extras(f):
    P = []; V = []; arr = None; err = 0
    for line in open(f):
        if '"P7_pido"' in line[:20]: P.append(json.loads(line))
        elif '"k":"voz"' in line[:12]: V.append(json.loads(line))
        elif '"P7_arranque"' in line[:22]: arr = json.loads(line)
        elif '"P7_error"' in line[:20]: err += 1
    return P, V, arr, err
OUT = {}
for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P713_s1_d*_APRENDE_*"))):
    vidas = A11.un_partido(carp); X = {sl: extras(glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log"))[0]) for sl in (10, 11)}
    for k, v in vidas.items():
        sl = v["slot"]; P, Vz, arr, err = X[sl]; Ph = X[21 - sl][0]
        M, T = A11.lee(glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log"))[0]); Mh, Th = A11.lee(glob.glob(os.path.join(carp, f"*policy_agent_{21 - sl}.art.log"))[0])
        coge = [c for c in A11.eventos(M, T)[0] if c["kit"]]; reg_h = A11.eventos(Mh, Th)[1]
        cierres = []
        for p in P:
            if not p.get("cierra"): continue
            sig = next((c for c in coge if p["tick"] - PARTE.CADA <= c["t"] <= p["tick"] + PARTE.CADUCIDAD), None)
            cierres.append({"tick": p["tick"], "motivo": p["cierra"], "coge_en": (sig["t"] if sig else None), "lo_habia_soltado_el_hermano": (any(g["pos"] == sig["pos"] and g["t"] < sig["t"] for g in reg_h) if sig else None)})
        for g in v["regala"]:
            ult = [p for p in Ph if p["tick"] < g["t_dec"] and g["t_dec"] - p["tick"] <= PARTE.CADUCIDAD]
            g["con_pedido"] = bool(ult and ult[-1]["pide"]); g["edad_del_parte"] = (g["t_dec"] - ult[-1]["tick"]) if ult else None
        OUT[k] = {"serie": v["serie"], "dia": v["dia"], "slot": sl, "semilla": v["semilla"], "pide_encendido": ((arr or {}).get("pide") or {}).get("PIDE"), "brazo": ((arr or {}).get("entorno_P7") or {}).get("brazo"), "errores_P7": err,
                  "partes": len(P), "partes_con_pedido": sum(1 for p in P if p["pide"]), "partes_voz": len(Vz), "voz_con_campo": sum(1 for x in Vz if " q" in x["texto"]), "largo_max": max((p["largo"] for p in P), default=None),
                  "pedidos_abiertos": sum(1 for p in P if p["abre"]), "pedidos_cerrados": len(cierres), "cierres": cierres, "abierto_al_final": bool(P and P[-1]["pide"]),
                  "sin_botiquin_y_viendo_uno": sum(1 for p in P if p["a_bordo"] == 0 and p["a_la_vista"]), "sin_botiquin_y_promesa_0": sum(1 for p in P if p["a_bordo"] == 0 and not p["a_la_vista"] and p["promesa"] <= 0),
                  "regalos": v["regala"], "regalos_n": v["regala_n"], "regalos_con_pedido": sum(1 for g in v["regala"] if g["con_pedido"]),
                  "coge_botiquines": v["coge_botiquines"], "coge_los_que_solto_el_hermano": v["coge_botiquines_que_solto_el_hermano"], "usos": sum(1 for u in v["usos"] if u.get("gastado")),
                  "tics": v["contadores"]["tics"], "tics_yendo_a_por_botiquin": v["contadores"].get("tics ir a por un botiquin", 0), "puesto": v["puesto"], "hp_final": v["hp_final"], "motivo": v["motivo"], "muerte": v["muerte"]["moda"]}
json.dump(OUT, open(os.path.join(AQUI, "P7_13_humo.json"), "w"), ensure_ascii=False, indent=1)
for k, o in OUT.items():
    print(k, {a: o[a] for a in ("pide_encendido", "brazo", "errores_P7", "partes", "partes_con_pedido", "voz_con_campo", "largo_max", "pedidos_abiertos", "pedidos_cerrados", "regalos_n", "regalos_con_pedido", "coge_botiquines", "coge_los_que_solto_el_hermano", "tics_yendo_a_por_botiquin", "tics", "puesto")}, [(c["motivo"], c["lo_habia_soltado_el_hermano"]) for c in o["cierres"]][:6], [g["destino"] for g in o["regalos"]])

# ── por que no hay regalos: los tics en que el hermano pide y yo llevo botiquines ──
sys.path.insert(0, os.path.join(RAIZ, "paintball")); sys.path.insert(0, RAIZ)
from alma import appraisal_zs_v42_exp as AP
OC = {}
for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P713_s1_d*_APRENDE_*"))):
    b = os.path.basename(carp).split("_"); dia = int(b[2][1:]); F = {sl: glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log"))[0] for sl in (10, 11)}
    for sl in (10, 11):
        Ph = extras(F[21 - sl])[0]; j = 0; ult = None; c = {"tics": 0, "hermano_pide": 0, "hermano_pide_y_llevo_1_o_mas": 0, "hermano_pide_y_llevo_2_o_mas": 0, "con_candidato_de_regalar": 0, "hermano_pide_y_candidato_de_regalar": 0, "elegido_regalar": 0,
                                                          "hermano_pide_y_lo_veo": 0, "hermano_pide_llevo_y_lo_veo": 0, "hermano_b0_y_llevo_minimo": 0}
        dmin = []
        for line in open(F[sl]):
            if '"tick"' not in line[:16]: continue
            r = json.loads(line)
            if r.get("k") != "tick" or r.get("phase") != "live": continue
            t = r["tick"]
            while j < len(Ph) and Ph[j]["tick"] < t: ult = Ph[j]; j += 1
            pide = bool(ult and ult["pide"] and t - ult["tick"] <= PARTE.CADUCIDAD)
            kits = sum(int((s or {}).get("n") or 0) for s in (r.get("pack") or []) if s and s.get("id") == "first_aid")
            R = r.get("RADIOGRAFIA") or {}; C = R.get("candidatos") or {}; cand = any(str(x).startswith("soltar_first_aid") for x in C)
            veo = any(a.get("slot") == 21 - sl for a in (r.get("ve_agentes") or []))
            par = (R.get("ahora") or {}).get("parte") or {}
            c["tics"] += 1; c["hermano_pide"] += pide; c["hermano_pide_y_llevo_1_o_mas"] += (pide and kits >= 1); c["hermano_pide_y_llevo_2_o_mas"] += (pide and kits >= 2)
            c["con_candidato_de_regalar"] += cand; c["hermano_pide_y_candidato_de_regalar"] += (pide and cand); c["elegido_regalar"] += str(R.get("elegido")).startswith("soltar_first_aid")
            c["hermano_pide_y_lo_veo"] += (pide and veo); c["hermano_pide_llevo_y_lo_veo"] += (pide and veo and kits >= 1); c["hermano_b0_y_llevo_minimo"] += (par.get("botiquin") == 0 and kits >= AP.PROVISION_B_MIN)
            if pide and cand:
                dd = {k_: (v_["d"] if isinstance(v_, dict) else v_) for k_, v_ in C.items()}; s_ = min(v_ for k_, v_ in dd.items() if k_.startswith("soltar_first_aid")); o_ = min(v_ for k_, v_ in dd.items() if not k_.startswith("soltar_first_aid"))
                dmin.append(round(s_ - o_, 5))
        c["d_regalar_menos_la_mejor_otra"] = {"n": len(dmin), "min": min(dmin) if dmin else None, "mediana": sorted(dmin)[len(dmin) // 2] if dmin else None, "negativas": sum(1 for x in dmin if x < 0)}
        OC[f"s1_d{dia}_APRENDE_{sl}"] = c
        print(f"s1_d{dia}_{sl}", c)
OUT2 = json.load(open(os.path.join(AQUI, "P7_13_humo.json")))
for k in OUT2: OUT2[k]["ocasiones"] = OC.get(k)
OUT2["_constantes"] = {"PROVISION_B_MIN": AP.PROVISION_B_MIN, "PROVISION_M": AP.PROVISION_M, "CADA": PARTE.CADA, "CADUCIDAD": PARTE.CADUCIDAD}
json.dump(OUT2, open(os.path.join(AQUI, "P7_13_humo.json"), "w"), ensure_ascii=False, indent=1)
