"""[P7-58] = analiza_P7_47 adaptado a SELLO_P7_58: H1, H2 iguales; H3 nueva (dias 10-20, cierres donde racion y red tienen >= 3 pruebas: curiosidad racion > red en >= 75 %);
curiosidad por objeto y dia; cuando se apaga la del botiquin (primer dia desde el que queda < 0,5 hasta el d20). Lee P7_58_cadena.json -> P7_58_sello.json.
--- cabecera de analiza_P7_47 ---
[P7-47] EL SELLO, de una vez, sobre P7_47_cadena.json y los cuadernos de la cadena (P7_47_res/) -> P7_47_sello.json (SELLO_P7_47.md, definiciones y criterios):
  H1 lo inutil manda en los cierres (<= 50 % de los 240; <= 20 % de los 72 de d15-20);  H2 coger lo inutil gana en los momentos (<= 1/3);
  H3 mediana de pruebas del botiquin para llegar a creencia 25 (<= 12), con el mismo calculo sobre los cuadernos reales del campo (P7_41_res, intensidades de P7-40);
  H4 recuperacion (h <= 0,5 en un cierre, >= 5 dias sin recuerdo nuevo de esa cosa, y vuelve a mandar en un cierre posterior) en >= 2 criaturas.
Creencia tras la k-esima prueba = nace_P7_29.CuadernoP29.creencia (dentro, cuerpo, con el neutro; los cortes no entran) con los k primeros recuerdos sin corte del
botiquin (orden dia, tick), vista desde el dia del k-esimo.  python3 analiza_P7_47.py"""
import glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(AQUI, "P7_58_res"); REAL = os.path.join(AQUI, "P7_41_res")
OLVIDO = 0.95; PESO_NEUTRO = 1.0; INUTIL = ("net", "camouflage"); VAR = ("APRENDE_v", "APRENDE_p")
C = json.load(open(os.path.join(AQUI, "P7_58_cadena.json")))["criaturas"]


def creencia_dentro(recs, dia):
    """= CuadernoP29.creencia(objeto, 'dentro', dia)['cuerpo'] con esos recuerdos (ya sin cortes), None si ninguno es 'dentro'."""
    rec = [r for r in recs if r.get("_sit") == "dentro"]
    if not rec: return None
    num = 0.0; den = PESO_NEUTRO; techo = []
    for r in rec:
        w = float(r["intensidad"]) * (OLVIDO ** max(0, dia - int(r["dia"])))
        if r.get("al_menos"): techo.append((w, float(r["efecto"]["cuerpo"]))); continue
        num += w * float(r["efecto"]["cuerpo"]); den += w
    if techo:
        base = (num / den) if den > 0 else 0.0
        for w, e in techo:
            if e > base: num += w * e; den += w
    return round(num / den, 4) if den > 0 else None


def k_estrella(cuaderno, objeto="first_aid", umbral=25.0):
    sits = ((cuaderno.get("objetos") or {}).get(objeto) or {}).get("situaciones") or {}
    recs = sorted([dict(r, _sit=s) for s, L in sits.items() for r in L if not r.get("corte")], key=lambda r: (int(r["dia"]), int(r.get("tick") or 0)))
    curva = []
    for k in range(1, len(recs) + 1):
        b = creencia_dentro(recs[:k], int(recs[k - 1]["dia"])); curva.append(b)
        if b is not None and b >= umbral: return k, len(recs), curva
    return None, len(recs), curva


def ultimo_cuaderno(carp, var, s, sl):
    fs = sorted(glob.glob(os.path.join(carp, f"cuaderno_s{s}_d*_{var}_{sl}.json")), key=lambda f: int(os.path.basename(f).split("_d")[1].split("_")[0]))
    return (json.load(open(fs[-1])), int(os.path.basename(fs[-1]).split("_d")[1].split("_")[0])) if fs else (None, 0)


R = {"criaturas": {}, "H1": {}, "H2": {}, "H3": {}, "H4": {}}
cierres = []; momentos = []; fid_i = 0; fid_d = 0; n_hab = 0; n_efe = 0; errores = []
for nombre, vidas in C.items():
    var, s, sl = nombre.split(); s = int(s[1:]); sl = int(sl[1:]); cr = {"variante": var, "serie": s, "asiento": sl, "dias": len(vidas), "cierres": [], "h_por_dia": {}, "recuerdos_nuevos_por_dia": {}}
    prev_rec = None
    for v in vidas:
        if v.get("error"): errores.append((nombre, v["dia"], v["error"][-200:])); break
        f = v.get("fidelidad") or {}; fid_i += f.get("igual", 0); fid_d += f.get("difiere", 0); n_hab += (v.get("habitua") or {}).get("n_habitua", 0); n_efe += (v.get("habitua") or {}).get("n_efecto", 0)
        ci = v.get("cierre") or {}
        if ci: cierres.append({"criatura": nombre, "variante": var, "dia": v["dia"], "manda": ci["manda"], "inutil": ci["inutil_manda"], "A": ci["A"], "h": ci.get("h") or {}}); cr["cierres"].append((v["dia"], ci["manda"], ci.get("h") or {}))
        cr["h_por_dia"][v["dia"]] = ci.get("h") or {}
        rec = (ci.get("recuerdos") or {}); cr["recuerdos_nuevos_por_dia"][v["dia"]] = ({o: rec[o] - (prev_rec or {}).get(o, 0) for o in rec} if rec else {}); prev_rec = rec or prev_rec
        for t, m in (v.get("momentos") or {}).items(): momentos.append({"criatura": nombre, "variante": var, "dia": v["dia"], "tick": int(t), "diario_coger": m.get("diario_coger"), "apertura": m.get("apertura"), "elegido": m.get("elegido")})
    # H3: la cadena y el real
    cu, d_ult = ultimo_cuaderno(RES, var, s, sl); k, n, curva = (k_estrella(cu) if cu else (None, 0, []))
    cu_r, _ = ultimo_cuaderno(REAL, var, s, sl); k_r, n_r, curva_r = (k_estrella(cu_r) if cu_r else (None, 0, []))
    cr.update({"k_estrella": k, "pruebas_botiquin": n, "curva": curva[:40], "dia_ultimo_cuaderno": d_ult, "k_estrella_real": k_r, "pruebas_botiquin_real": n_r, "curva_real": curva_r[:40], "habituacion_final": (cu or {}).get("habituacion_P7_47")})
    # H4: recuperacion
    rec4 = []
    for d, manda, h in cr["cierres"]:
        for o, hv in h.items():
            if hv is None or hv > 0.5: continue
            sin = all(cr["recuerdos_nuevos_por_dia"].get(dd, {}).get(o, 0) == 0 for dd in range(d + 1, d + 6))
            if not sin: continue
            vuelve = [dd for dd, m2, _ in cr["cierres"] if dd >= d + 5 and m2 == o]
            if vuelve: rec4.append({"objeto": o, "dia_habituado": d, "h": hv, "vuelve_a_mandar_dia": vuelve[0]})
    cr["recuperaciones"] = rec4
    R["criaturas"][nombre] = cr

tot = len(cierres); inu = sum(1 for c in cierres if c["inutil"]); c15 = [c for c in cierres if c["dia"] >= 15]; inu15 = sum(1 for c in c15 if c["inutil"])
R["H1"] = {"cierres": tot, "inutil_manda": inu, "pct": round(100 * inu / tot, 1) if tot else None, "d15_20_cierres": len(c15), "d15_20_inutil": inu15, "d15_20_pct": round(100 * inu15 / len(c15), 1) if c15 else None,
           "pasa": bool(tot and inu <= 0.5 * tot and inu15 <= 0.2 * len(c15)), "por_variante": {v: {"cierres": sum(1 for c in cierres if c["variante"] == v), "inutil": sum(1 for c in cierres if c["variante"] == v and c["inutil"]), "d15_20_inutil": sum(1 for c in c15 if c["variante"] == v and c["inutil"]), "d15_20": sum(1 for c in c15 if c["variante"] == v)} for v in VAR},
           "manda_por_clase": {o: sum(1 for c in cierres if c["manda"] == o) for o in ("first_aid", "rations", "net", "camouflage")}, "por_dia_inutil": {d: sum(1 for c in cierres if c["dia"] == d and c["inutil"]) for d in range(1, 21)}}
mm = [m for m in momentos if m["elegido"] is not None]; cog = sum(1 for m in mm if m["elegido"] == "coger"); cur = sum(1 for m in mm if m["elegido"] == "ir_curioso")
R["H2"] = {"momentos": len(mm), "coger": cog, "ir_curioso": cur, "fraccion_coger": round(cog / len(mm), 3) if mm else None, "pasa": bool(mm and cog <= len(mm) / 3), "diario_coger_momentos": sum(1 for m in mm if m["diario_coger"]), "aperturas": sum(1 for m in mm if m["apertura"]),
           "por_variante": {v: {"momentos": sum(1 for m in mm if m["variante"] == v), "coger": sum(1 for m in mm if m["variante"] == v and m["elegido"] == "coger")} for v in VAR}, "elegidos": {}}
for m in mm: R["H2"]["elegidos"][m["elegido"]] = R["H2"]["elegidos"].get(m["elegido"], 0) + 1
# H3 (P7-58): dias 10-20, cierres con racion y red probadas >= 3 veces
h3 = []; curio_dia = {}; apaga = {}
for nombre, vidas in C.items():
    serie_k = []
    for v in vidas:
        ci = v.get("cierre") or {}; det = ci.get("detalle") or {}; A = ci.get("A") or {}
        if not A: continue
        curio_dia.setdefault(v["dia"], []).append(A)
        serie_k.append((v["dia"], A.get("first_aid")))
        if v["dia"] >= 10 and (det.get("rations") or {}).get("pruebas", 0) >= 3 and (det.get("net") or {}).get("pruebas", 0) >= 3: h3.append({"criatura": nombre, "dia": v["dia"], "racion": A.get("rations"), "red": A.get("net"), "mayor": A.get("rations", 0) > A.get("net", 0)})
    ap = None
    for i, (d, k) in enumerate(serie_k):
        if all((kk or 0) < 0.5 for dd, kk in serie_k[i:]): ap = d; break
    apaga[nombre] = ap
R["H3"] = {"cierres": len(h3), "racion_mayor": sum(1 for x in h3 if x["mayor"]), "fraccion": (round(sum(1 for x in h3 if x["mayor"]) / len(h3), 3) if h3 else None), "pasa": bool(h3 and sum(1 for x in h3 if x["mayor"]) >= 0.75 * len(h3)), "detalle": h3}
R["curiosidad_por_dia"] = {d: {o: round(st.mean(A.get(o, 0) for A in L), 3) for o in ("first_aid", "rations", "net", "camouflage")} for d, L in sorted(curio_dia.items())}
R["apaga_botiquin"] = apaga
R["H4"] = {"pasa": None}
R["fidelidad"] = {"igual": fid_i, "difiere": fid_d}; R["habituaciones"] = n_hab; R["pruebas_con_efecto"] = n_efe; R["errores"] = errores
R["pasa_sello"] = bool(R["H1"]["pasa"] and R["H2"]["pasa"] and R["H3"]["pasa"])
json.dump(R, open(os.path.join(AQUI, "P7_58_sello.json"), "w"), ensure_ascii=False, indent=1)
print("H1", {k: v for k, v in R["H1"].items() if k not in ("por_dia_inutil",)}); print("H2", {k: v for k, v in R["H2"].items() if k != "elegidos"}, R["H2"]["elegidos"]); print("H3", {k: v for k, v in R["H3"].items() if k != "detalle"}); print("apaga botiquin", R["apaga_botiquin"]); print("curiosidad d1/d10/d20", {d: R["curiosidad_por_dia"].get(d) for d in (1, 10, 20)})
print("fidelidad", R["fidelidad"], "habituaciones", n_hab, "con efecto", n_efe, "errores", errores, "PASA", R["pasa_sello"])
