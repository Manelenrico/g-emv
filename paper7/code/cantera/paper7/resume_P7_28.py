"""[P7-28, puntos 2, 3 y 4] Las medidas del informe, desde P7_28_vidas.json (esta lectura), P7_24_vidas.json y P7_24_resumen.json (el campo sellado) y, si existe,
P7_28_curiosidad.json (punto 1, banco_P7_28.py) -> P7_28_resumen.json. Coste cero.
  python3 resume_P7_28.py
Exclusiones: las mismas del sello (las 8 partidas con corte de P7-27 salen de puesto, muerte y pares). Bloques: dias 1-5 y 16-20; los pares, por semilla, dia y asiento."""
import collections, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__))
V28 = json.load(open(os.path.join(AQUI, "P7_28_vidas.json"))); V24 = json.load(open(os.path.join(AQUI, "P7_24_vidas.json"))); R24 = json.load(open(os.path.join(AQUI, "P7_24_resumen.json")))
CORTE = {tuple(x) for x in R24["partidas_con_corte"]}
L = {k: v for k, v in V28.items() if not v.get("sin_diario")}
def corte(v): return (v["serie"], v["dia"], v["brazo"]) in CORTE
def media(x): return round(st.mean(x), 3) if x else None
def resumen(x):
    if len(x) < 2: return {"n": len(x), "media": (x[0] if x else None), "ee": None}
    return {"n": len(x), "media": round(st.mean(x), 3), "ee": round(st.stdev(x) / len(x) ** 0.5, 3)}
def mediana(x): return (st.median(x) if x else None)
BLOQUES = {"dias 1-5": range(1, 6), "dias 6-10": range(6, 11), "dias 11-15": range(11, 16), "dias 16-20": range(16, 21)}
R = {"vidas_leidas": len(L), "sin_diario": [k for k, v in V28.items() if v.get("sin_diario")], "partidas_con_corte": sorted(list(x) for x in CORTE)}

# ── punto 2: la creencia y el uso, por criatura de APRENDE y dia ──
p2 = []
for k, v in sorted(L.items(), key=lambda kv: (kv[1]["serie"], kv[1]["slot"], kv[1]["dia"])):
    if v["brazo"] != "APRENDE": continue
    w = V24.get(k) or {}; cr = ((w.get("al_acabar") or {}).get("botiquin") or {}).get("creencia") or {}; ig = ((w.get("al_acabar") or {}).get("botiquin") or {}).get("ignorancia")
    p2.append({"serie": v["serie"], "asiento": v["slot"], "dia": v["dia"], "parcial": v.get("parcial"), "creencia_dentro": cr.get("dentro"), "creencia_fuera": cr.get("fuera"), "ignorancia": ig,
               "botiquines_llevados_media": round(v["botiquines_media"], 2), "tics_con_botiquin": round(v["tics_con_botiquin"], 2), "cogidos": v["botiquines_cogidos"], "canales": v["canales_botiquin"], "completados": v["canales_completados"],
               "hp_al_abrir": v["vida_al_abrir"], "usos_heridos": v["usos_heridos"], "firmes": v["huellas_botiquin"]["firmes"], "al_menos": v["huellas_botiquin"]["al_menos"], "cortes": v["huellas_botiquin"]["cortes"], "puesto": v["puesto"], "murio": v["murio"]})
R["punto2_aprende_por_dia"] = p2
def bloque(brazo, ds):
    vs = [v for v in L.values() if v["brazo"] == brazo and v["dia"] in ds]; hp = [h for v in vs for h in v["vida_al_abrir"]]
    return {"vidas": len(vs), "botiquines_llevados_media": media([v["botiquines_media"] for v in vs]), "tics_con_botiquin": media([v["tics_con_botiquin"] for v in vs]), "raciones_llevadas_media": media([v["raciones_media"] for v in vs if v["raciones_media"] is not None]),
            "cogidos": sum(v["botiquines_cogidos"] for v in vs), "canales": sum(v["canales_botiquin"] for v in vs), "completados": sum(v["canales_completados"] for v in vs), "usos_heridos": sum(v["usos_heridos"] for v in vs), "hp_al_abrir_mediana": mediana(hp),
            "huellas": {kk: sum(v["huellas_botiquin"][kk] for v in vs) for kk in ("n", "firmes", "al_menos", "cortes")}, "vidas_con_algun_uso_herido": sum(1 for v in vs if v["usos_heridos"] > 0)}
R["punto2_bloques"] = {b: {nb: bloque(b, ds) for nb, ds in BLOQUES.items()} for b in ("APRENDE", "BORRADO", "TECHO")}
R["punto2_aprende_dias_con_uso_herido"] = [(x["serie"], x["asiento"], x["dia"]) for x in p2 if x["usos_heridos"] > 0]

# ── punto 3: donde se pierde el puesto (pares por semilla, dia y asiento; se excluyen los pares con corte) ──
def par(a, b, ds):
    out = []
    for s in (1, 2):
        for d in ds:
            if (s, d, a) in CORTE or (s, d, b) in CORTE: continue
            for sl in (10, 11):
                x = L.get(f"s{s}_d{d}_{a}_{sl}"); y = L.get(f"s{s}_d{d}_{b}_{sl}")
                if x and y and x.get("puesto") is not None and y.get("puesto") is not None: out.append((s, d, sl, x, y))
    return out
def muertes(brazo, ds, excluye=True):
    vs = [v for v in L.values() if v["brazo"] == brazo and v["dia"] in ds and not (excluye and corte(v))]; mu = [v for v in vs if v["murio"]]
    g = [v["muerte"]["primer_golpe"] for v in mu if v["muerte"]["primer_golpe"]]
    return {"vidas": len(vs), "muertos": len(mu), "causa": dict(collections.Counter(v["muerte"]["causa"] for v in mu)), "tic_de_muerte_mediana": mediana([v["muerte"]["tic"] for v in mu]), "tic_de_muerte_media": media([v["muerte"]["tic"] for v in mu]),
            "peleas_finales_con_golpe": len(g), "hp_en_el_primer_golpe_mediana": mediana([x["vida"] for x in g]), "hp_en_el_primer_golpe": sorted(x["vida"] for x in g), "llevaba_botiquin_en_el_primer_golpe": sum(1 for x in g if x["llevaba_botiquin"]), "lo_uso_despues": sum(1 for x in g if x["uso_despues"]),
            "llevaba_botiquin_al_morir": sum(1 for v in mu if v["muerte"]["llevaba_botiquin_al_morir"]), "puesto_medio": media([v["puesto"] for v in vs]), "sobreviven": len(vs) - len(mu)}
R["punto3_muertes"] = {b: {nb: muertes(b, ds) for nb, ds in (("dias 1-5", range(1, 6)), ("dias 16-20", range(16, 21)))} for b in ("APRENDE", "BORRADO", "TECHO")}
# emparejado: diferencia de puesto, de tic de muerte (cuando mueren los dos) y causa cruzada
p3 = {}
for a, b in (("APRENDE", "TECHO"), ("APRENDE", "BORRADO"), ("BORRADO", "TECHO")):
    for nb, ds in (("dias 1-5", range(1, 6)), ("dias 16-20", range(16, 21))):
        P = par(a, b, ds); dp = [x["puesto"] - y["puesto"] for _, _, _, x, y in P]; dt = [x["muerte"]["tic"] - y["muerte"]["tic"] for _, _, _, x, y in P if x["murio"] and y["murio"]]
        cruz = collections.Counter((x["muerte"]["causa"] if x["murio"] else "vive", y["muerte"]["causa"] if y["murio"] else "vive") for _, _, _, x, y in P)
        p3[f"{a} - {b} · {nb}"] = {"pares": len(P), "puesto": resumen(dp), "pares_peor_igual_mejor": [sum(1 for d in dp if d > 0), sum(1 for d in dp if d == 0), sum(1 for d in dp if d < 0)], "tic_de_muerte": resumen(dt), "causa_cruzada": {f"{k[0]}/{k[1]}": n for k, n in sorted(cruz.items())}}
R["punto3_pares"] = p3
# ¿mueren mas las que no llevan botiquin? (todas las vidas, por brazo): muertos entre las que llevaban botiquin en el primer golpe de la pelea final vs no
sin = {}
for b in ("APRENDE", "BORRADO", "TECHO"):
    mu = [v for v in L.values() if v["brazo"] == b and v["murio"] and v["muerte"]["primer_golpe"] and not corte(v)]
    con = [v for v in mu if v["muerte"]["primer_golpe"]["llevaba_botiquin"]]; sin_ = [v for v in mu if not v["muerte"]["primer_golpe"]["llevaba_botiquin"]]
    sin[b] = {"muertes_en_pelea_con_golpe": len(mu), "llevaban_botiquin": len(con), "no_llevaban": len(sin_), "hp_golpe_con": mediana([v["muerte"]["primer_golpe"]["vida"] for v in con]), "hp_golpe_sin": mediana([v["muerte"]["primer_golpe"]["vida"] for v in sin_]), "usaron_con": sum(1 for v in con if v["muerte"]["primer_golpe"]["uso_despues"])}
    # y entre todas las vidas: fraccion de tics con botiquin, muertos vs vivos
    vs = [v for v in L.values() if v["brazo"] == b and not corte(v)]
    sin[b]["tics_con_botiquin_muertos"] = media([v["tics_con_botiquin"] for v in vs if v["murio"]]); sin[b]["tics_con_botiquin_vivos"] = media([v["tics_con_botiquin"] for v in vs if not v["murio"]])
R["punto3_botiquin_y_muerte"] = sin

# lo que elige cada brazo (todas las elecciones del diario, incluidos los tics de enfriamiento), la distancia al centro y lo que hacia antes de la pelea final
R["elegido_bloques"] = {}; R["dist_centro"] = {}; R["antes_del_golpe"] = {}; R["ataca"] = {}
for b in ("APRENDE", "BORRADO", "TECHO"):
    R["elegido_bloques"][b] = {}; R["dist_centro"][b] = {}; R["antes_del_golpe"][b] = {}; R["ataca"][b] = {}
    for nb, ds in (("dias 1-5", range(1, 6)), ("dias 16-20", range(16, 21))):
        vs = [v for v in L.values() if v["brazo"] == b and v["dia"] in ds and not corte(v)]; el = collections.Counter(); tot = 0
        for v in vs:
            for k, c in v["elegido"].items(): el[k] += c; tot += c
        R["elegido_bloques"][b][nb] = {k: round(c / tot, 4) for k, c in el.most_common(5)}
        R["dist_centro"][b][nb] = media([v["dist_al_centro_media"] for v in vs])
        g = [v["muerte"]["primer_golpe"] for v in vs if v["murio"] and v["muerte"]["primer_golpe"]]; an = collections.Counter(); ta = 0
        for x in g:
            for k, c in x["elegido_240_antes"].items(): an[k] += c; ta += c
        R["antes_del_golpe"][b][nb] = {k: round(c / ta, 4) for k, c in an.most_common(4)} if ta else {}
        R["ataca"][b][nb] = sum(1 for v in vs if any(k.startswith("atacar_") for k in v["elegido"]))
        R["ataca"][b][nb + " · antes del golpe"] = sum(sum(c for k, c in x["elegido_240_antes"].items() if k.startswith("atacar_")) for x in g)

# muertes tempranas (antes del tic 4.000) y los pasos bloqueados (P7_28_bloqueos*.json, contados del diario: `action_result` = blocked con el paso listo)
R["muertes_tempranas"] = {b: {nb: sum(1 for v in L.values() if v["brazo"] == b and v["dia"] in ds and not corte(v) and v["murio"] and v["muerte"]["tic"] < 4000) for nb, ds in (("dias 1-5", range(1, 6)), ("dias 16-20", range(16, 21)))} for b in ("APRENDE", "BORRADO", "TECHO")}
R["muertes_medias"] = {b: {nb: sum(1 for v in L.values() if v["brazo"] == b and v["dia"] in ds and not corte(v) and v["murio"] and 4000 <= v["muerte"]["tic"] < 10000) for nb, ds in (("dias 1-5", range(1, 6)), ("dias 16-20", range(16, 21)))} for b in ("APRENDE", "BORRADO", "TECHO")}
R["muertes_tardias"] = {b: {nb: sum(1 for v in L.values() if v["brazo"] == b and v["dia"] in ds and not corte(v) and v["murio"] and v["muerte"]["tic"] >= 10000) for nb, ds in (("dias 1-5", range(1, 6)), ("dias 16-20", range(16, 21)))} for b in ("APRENDE", "BORRADO", "TECHO")}
R["tempranas_aprende"] = sorted(({"serie": v["serie"], "dia": v["dia"], "slot": v["slot"], "muerte": v["muerte"]} for v in L.values() if v["brazo"] == "APRENDE" and v["dia"] >= 16 and not corte(v) and v["murio"] and v["muerte"]["tic"] < 4000), key=lambda x: (x["dia"], x["serie"], x["slot"]))
for f_, k_ in (("P7_28_bloqueos_brazos.json", "bloqueos_brazos"), ("P7_28_bloqueos.json", "bloqueos_aprende_16_20")):
    if os.path.exists(os.path.join(AQUI, f_)): R[k_] = json.load(open(os.path.join(AQUI, f_)))

# ── punto 4: las series por separado ──
p4 = {}
for a, b in (("BORRADO", "TECHO"), ("APRENDE", "TECHO"), ("APRENDE", "BORRADO")):
    for s in (1, 2):
        fila = {}
        for nb, ds in (("dias 1-5", range(1, 6)), ("dias 16-20", range(16, 21))):
            P = [p for p in par(a, b, ds) if p[0] == s]; fila[nb] = resumen([x["puesto"] - y["puesto"] for _, _, _, x, y in P])
        fila["crece"] = (round(fila["dias 16-20"]["media"] - fila["dias 1-5"]["media"], 3) if fila["dias 1-5"]["media"] is not None and fila["dias 16-20"]["media"] is not None else None)
        p4[f"{a} - {b} · serie {s}"] = fila
    # y el puesto absoluto por brazo y serie
for b in ("APRENDE", "BORRADO", "TECHO"):
    for s in (1, 2):
        p4[f"{b} · serie {s} · puesto"] = {nb: resumen([v["puesto"] for v in L.values() if v["brazo"] == b and v["serie"] == s and v["dia"] in ds and not corte(v) and v.get("puesto") is not None]) for nb, ds in (("dias 1-5", range(1, 6)), ("dias 16-20", range(16, 21)))}
R["punto4_series"] = p4

# ── punto 1 (si el banco acabo) ──
f1 = os.path.join(AQUI, "P7_28_curiosidad.json")
if os.path.exists(f1):
    C = json.load(open(f1)); fid = collections.Counter(); reg = []
    for r in C:
        for k_, n in (r.get("fidelidad") or {}).items(): fid[k_] += n
        for x in r["registros"]: reg.append(dict(x, serie=r["serie"], dia=r["dia"], slot=r["slot"]))
    ign_fin = {}
    for r in C:
        w = V24.get(f"s{r['serie']}_d{r['dia']}_APRENDE_{r['slot']}") or {}
        ign_fin[(r["serie"], r["dia"], r["slot"])] = {o: ((w.get("al_acabar") or {}).get(o) or {}).get("ignorancia") for o in ("botiquin", "racion")}
    OBJ = {"first_aid": "botiquin", "rations": "racion"}
    def ign_de(x, o): return x["ignorancia"].get(o) if o in x["ignorancia"] else x["ignorancia"].get({"botiquin": "first_aid", "racion": "rations"}[o])
    por_vida = []
    for r in C:
        xs = r["registros"]; k = (r["serie"], r["dia"], r["slot"])
        por_vida.append({"serie": r["serie"], "dia": r["dia"], "asiento": r["slot"], "tics": r["tics"], "fidelidad": r["fidelidad"], "paso_listo": r["cuenta"].get("listos", 0), "ir_curioso_listo": len(xs),
                         "ignorancia_al_decidir": {o: {"min": (min(ign_de(x, o) for x in xs) if xs else None), "max": (max(ign_de(x, o) for x in xs) if xs else None), "media": (media([ign_de(x, o) for x in xs]) if xs else None)} for o in ("botiquin", "racion")},
                         "ignorancia_al_acabar": ign_fin[k], "clase": dict(collections.Counter(str(x["clase"]) for x in xs)), "dentro": sum(1 for x in xs if x["dentro"]), "fuera": sum(1 for x in xs if not x["dentro"]), "dist_mediana": mediana([x["dist"] for x in xs if x["dist"] is not None]),
                         "llega": sum(1 for x in xs if x["llega"]), "coge": sum(1 for x in xs if x["coge"]), "usa": sum(1 for x in xs if x["usa"]), "M_curiosidad_mediana": mediana([x["M_curiosidad"] for x in xs if x["M_curiosidad"] is not None]),
                         "d_mediana": {c: mediana([x["d"][c] for x in xs if c in x["d"] and x["d"][c] is not None]) for c in ("ir_curioso", "ir_objeto", "ir_centro", "ir_botin", "noop")}, "k_botiquin_mediana": mediana([x["k_botiquin"] for x in xs]), "k_racion_mediana": mediana([x["k_racion"] for x in xs]),
                         "zurron_con_botiquin": sum(1 for x in xs if (x["zurron"].get("first_aid") or x["zurron"].get("botiquin") or 0) >= 1), "zurron_con_racion": sum(1 for x in xs if (x["zurron"].get("rations") or x["zurron"].get("racion") or 0) >= 1)})
    # destinos distintos y "episodios" (rachas de tics seguidos hacia el mismo destino)
    episodios = []
    for r in C:
        xs = r["registros"]; cur = None
        for x in xs:
            if cur and tuple(x["destino"]) == cur["destino"] and x["t"] - cur["t_fin"] <= 40: cur["t_fin"] = x["t"]; cur["n"] += 1
            else:
                cur = {"serie": r["serie"], "dia": r["dia"], "slot": r["slot"], "destino": tuple(x["destino"]), "clase": x["clase"], "t0": x["t"], "t_fin": x["t"], "n": 1, "dist0": x["dist"], "dentro": x["dentro"], "a_la_vista": x.get("destino_a_la_vista"), "hp": x["hp"], "d": x["d"], "llega": x["llega"], "coge": x["coge"], "usa": x["usa"], "ign_bot": ign_de(x, "botiquin"), "ign_rac": ign_de(x, "racion"), "zurron": x["zurron"]}; episodios.append(cur)
    R["punto1"] = {"vidas": len(C), "fidelidad": dict(fid), "registros": len(reg), "por_vida": por_vida, "episodios": len(episodios), "episodios_clase": dict(collections.Counter(str(e["clase"]) for e in episodios)), "episodios_dentro": sum(1 for e in episodios if e["dentro"]),
                   "episodios_llega": sum(1 for e in episodios if e["llega"]), "episodios_coge": sum(1 for e in episodios if e["coge"]), "episodios_usa": sum(1 for e in episodios if e["usa"]), "episodios_dist0_mediana": mediana([e["dist0"] for e in episodios if e["dist0"] is not None]),
                   "episodios_con_botiquin_en_zurron": sum(1 for e in episodios if (e["zurron"].get("first_aid") or e["zurron"].get("botiquin") or 0) >= 1), "episodios_destino_a_la_vista": sum(1 for e in episodios if e["a_la_vista"]),
                   "episodios_llega_o_coge": sum(1 for e in episodios if e["llega"] or e["coge"]), "registros_destino_a_la_vista": sum(1 for x in reg if x.get("destino_a_la_vista")), "registros_dentro": sum(1 for x in reg if x["dentro"]), "registros_dist_mediana": mediana([x["dist"] for x in reg if x["dist"] is not None]),
                   "registros_clase": dict(collections.Counter(str(x["clase"]) for x in reg)), "registros_llega": sum(1 for x in reg if x["llega"]), "registros_coge": sum(1 for x in reg if x["coge"]), "registros_usa": sum(1 for x in reg if x["usa"]),
                   "registros_con_botiquin_en_zurron": sum(1 for x in reg if (x["zurron"].get("first_aid") or 0) >= 1), "registros_con_racion_en_zurron": sum(1 for x in reg if (x["zurron"].get("rations") or 0) >= 1), "ir_curioso_gana_a_ir_objeto_por": mediana([x["d"]["ir_objeto"] - x["d"]["ir_curioso"] for x in reg if x["d"].get("ir_objeto") is not None and x["d"].get("ir_curioso") is not None]),
                   "ir_curioso_gana_a_noop_por": mediana([x["d"]["noop"] - x["d"]["ir_curioso"] for x in reg if x["d"].get("noop") is not None and x["d"].get("ir_curioso") is not None]), "alivio_curiosidad_imaginado_mediana": mediana([x["M_curiosidad"] * 0.5 for x in reg if x["M_curiosidad"] is not None]),
                   "k_botiquin_mediana": mediana([x["k_botiquin"] for x in reg]), "k_racion_mediana": mediana([x["k_racion"] for x in reg]), "episodios_lista": [dict(e, destino=list(e["destino"])) for e in episodios],
                   "d_mediana_global": {c: mediana([x["d"][c] for x in reg if c in x["d"] and x["d"][c] is not None]) for c in ("ir_curioso", "ir_objeto", "ir_centro", "ir_botin", "noop")}, "M_curiosidad_mediana_global": mediana([x["M_curiosidad"] for x in reg if x["M_curiosidad"] is not None]),
                   "ignorancia_al_decidir_global": {o: {"mediana": mediana([ign_de(x, o) for x in reg]), "min": (min(ign_de(x, o) for x in reg) if reg else None), "max": (max(ign_de(x, o) for x in reg) if reg else None)} for o in ("botiquin", "racion")}}
json.dump(R, open(os.path.join(AQUI, "P7_28_resumen.json"), "w"), ensure_ascii=False, indent=1)
for k in ("punto2_bloques", "punto3_muertes", "punto3_pares", "punto3_botiquin_y_muerte", "punto4_series"): print(k, json.dumps(R[k], ensure_ascii=False)[:1500])
if "punto1" in R: print("punto1", {k: v for k, v in R["punto1"].items() if k not in ("por_vida", "episodios_lista")})
