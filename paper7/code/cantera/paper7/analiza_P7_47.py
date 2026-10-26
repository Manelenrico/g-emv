"""[P7-47] EL SELLO, de una vez, sobre P7_47_cadena.json y los cuadernos de la cadena (P7_47_res/) -> P7_47_sello.json (SELLO_P7_47.md, definiciones y criterios):
  H1 lo inutil manda en los cierres (<= 50 % de los 240; <= 20 % de los 72 de d15-20);  H2 coger lo inutil gana en los momentos (<= 1/3);
  H3 mediana de pruebas del botiquin para llegar a creencia 25 (<= 12), con el mismo calculo sobre los cuadernos reales del campo (P7_41_res, intensidades de P7-40);
  H4 recuperacion (h <= 0,5 en un cierre, >= 5 dias sin recuerdo nuevo de esa cosa, y vuelve a mandar en un cierre posterior) en >= 2 criaturas.
Creencia tras la k-esima prueba = nace_P7_29.CuadernoP29.creencia (dentro, cuerpo, con el neutro; los cortes no entran) con los k primeros recuerdos sin corte del
botiquin (orden dia, tick), vista desde el dia del k-esimo.  python3 analiza_P7_47.py"""
import glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(AQUI, "P7_47_res"); REAL = os.path.join(AQUI, "P7_41_res")
OLVIDO = 0.95; PESO_NEUTRO = 1.0; INUTIL = ("net", "camouflage"); VAR = ("APRENDE_v", "APRENDE_p")
C = json.load(open(os.path.join(AQUI, "P7_47_cadena.json")))["criaturas"]


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
ks = [cr["k_estrella"] for cr in R["criaturas"].values()]; ks_r = [cr["k_estrella_real"] for cr in R["criaturas"].values()]
def mediana_inf(xs):
    v = sorted((float("inf") if x is None else x) for x in xs); n = len(v)
    return None if not n else (v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2)
med = mediana_inf(ks); med_r = mediana_inf(ks_r)
R["H3"] = {"k_estrella": {k: v for k, v in zip(R["criaturas"], ks)}, "mediana": (None if med in (None, float("inf")) else med), "llegan": sum(1 for k in ks if k), "pasa": bool(med is not None and med != float("inf") and med <= 12),
           "real": {"k_estrella": {k: v for k, v in zip(R["criaturas"], ks_r)}, "mediana": (None if med_r in (None, float("inf")) else med_r), "llegan": sum(1 for k in ks_r if k)}, "pruebas_botiquin": {k: cr["pruebas_botiquin"] for k, cr in R["criaturas"].items()},
           "por_variante": {v: {"mediana": (lambda m: None if m in (None, float("inf")) else m)(mediana_inf([cr["k_estrella"] for cr in R["criaturas"].values() if cr["variante"] == v])), "real": (lambda m: None if m in (None, float("inf")) else m)(mediana_inf([cr["k_estrella_real"] for cr in R["criaturas"].values() if cr["variante"] == v]))} for v in VAR}}
rec_cr = [k for k, cr in R["criaturas"].items() if cr["recuperaciones"]]
R["H4"] = {"criaturas_con_recuperacion": rec_cr, "n": len(rec_cr), "pasa": len(rec_cr) >= 2, "detalle": {k: cr["recuperaciones"][:5] for k, cr in R["criaturas"].items() if cr["recuperaciones"]},
           "habituadas_alguna_vez": {k: sorted({o for d, m, h in cr["cierres"] for o, hv in h.items() if hv is not None and hv <= 0.5}) for k, cr in R["criaturas"].items()}}
R["fidelidad"] = {"igual": fid_i, "difiere": fid_d}; R["habituaciones"] = n_hab; R["pruebas_con_efecto"] = n_efe; R["errores"] = errores
R["pasa_sello"] = bool(R["H1"]["pasa"] and R["H2"]["pasa"] and R["H3"]["pasa"])
json.dump(R, open(os.path.join(AQUI, "P7_47_sello.json"), "w"), ensure_ascii=False, indent=1)
print("H1", {k: v for k, v in R["H1"].items() if k not in ("por_dia_inutil",)}); print("H2", {k: v for k, v in R["H2"].items() if k != "elegidos"}, R["H2"]["elegidos"]); print("H3", {k: v for k, v in R["H3"].items() if k not in ("pruebas_botiquin",)}); print("H4", R["H4"]["n"], R["H4"]["criaturas_con_recuperacion"], R["H4"]["habituadas_alguna_vez"])
print("fidelidad", R["fidelidad"], "habituaciones", n_hab, "con efecto", n_efe, "errores", errores, "PASA", R["pasa_sello"])
