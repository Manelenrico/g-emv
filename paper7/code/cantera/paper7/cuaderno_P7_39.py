"""[P7-39, dia a dia y criterios I1-I3, I5, para B1 y B2] = cuaderno_P7_38 sobre los cuadernos de P7-39 (P7_39_res/cuaderno_<B1|B2>_s<S>_d<D>_<asiento>.json; GEMV_P7_39 lectura B1|B2) -> P7_39_cuadernos_<B>.json; ademas la creencia de la racion por dia frente a P7-37.
[P7-38, dia a dia y criterios I1-I3, I5] Sobre los 80 cuadernos A (P7_38_res/cuaderno_A_s<S>_d<D>_<asiento>.json) y los de P7-37 (P7_37_res/cuaderno_descontada_*):
importancia escalar (min(1, S/E)) por cosa (cuadernos del dia 20: mediana, cuartiles; P7-33 frente a contrafactual; cuantos quedaron sin referencia o con referencia de
cualquier situacion); "no hizo nada" (red y camuflaje con |efecto cuerpo| <= 1) y su importancia; por criatura y dia: ignorancia, importancia esperada, curiosidad A por
cosa; quien manda; el dia en que cada criatura deja de tener lo inutil como lo que mas llama; creencia de lo util frente a P7-37. -> P7_38_cuadernos.json
  python3 cuaderno_P7_38.py"""
import json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
for p in (os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    if p not in sys.path: sys.path.insert(0, p)
for k, v in (("GEMV_P7", "1"), ("GEMV_P7_NACE", "1"), ("GEMV_P7_29", "1"), ("GEMV_P7_33", "1"), ("GEMV_P7_38", "off")): os.environ.setdefault(k, v)
import nace_P7_29 as N29, contrafactual_P7_38 as CF
LECTURA = os.environ.get("P7_39_LECTURA", "B1")
NOM = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camuflaje": "camuflaje", "camouflage": "camuflaje"}; COSAS = ("first_aid", "rations", "net", "camouflage"); CRI = ((1, 10), (1, 11), (2, 10), (2, 11))
N29.E["arreglos"]["corte"] = True
q = lambda xs: ([round(sorted(xs)[len(xs) // 4], 4), round(st.median(xs), 4), round(sorted(xs)[3 * len(xs) // 4], 4)] if xs else None)


def cre(c, o, d):
    x = c.creencia(o, "dentro", dia=d) or c.creencia(o, "fuera", dia=d); return (x or {}).get("cuerpo")


if __name__ == "__main__":
    R = {"criaturas": {}, "importancia": {}, "no_hizo_nada": {}}
    imp = {o: {"P33": [], "A": [], "n": 0, "sin_ref": 0, "cualquiera": 0, "ref": []} for o in COSAS}; nada = {"P33": [], "A": [], "n": 0}
    for s, sl in CRI:
        k = f"s{s} a{sl}"; dias = {}
        for d in range(1, 21):
            fa = os.path.join(AQUI, "P7_39_res", f"cuaderno_{LECTURA}_s{s}_d{d}_{sl}.json"); f37 = os.path.join(AQUI, "P7_37_res", f"cuaderno_descontada_s{s}_d{d}_{sl}.json")
            if not (os.path.exists(fa) and os.path.exists(f37)): continue
            ca = N29.CuadernoP29.lee(fa); c37 = N29.CuadernoP29.lee(f37); x = {}
            for o in COSAS:
                ign = ca.ignorancia(o, d); ie = CF.importancia_esperada(ca, o)
                x[NOM[o]] = {"ignorancia": round(ign, 4), "importancia_esperada": round(ie, 4), "curiosidad_A": round(ign * ie, 4), "creencia_A": cre(ca, o, d), "creencia_P37": cre(c37, o, d), "recuerdos": len(ca.recuerdos_de(o))}
            if d == 20:
                for o in COSAS:
                    for r in ca.recuerdos_de(o):
                        if r.get("corte"): continue
                        a = CF.escalar(r.get("importancia")); p33 = CF.escalar(r.get("importancia_P33") or r.get("importancia")); imp[o]["P33"].append(p33); imp[o]["A"].append(a); imp[o]["n"] += 1
                        imp[o]["sin_ref"] += int(bool(r.get("sin_referencia"))); imp[o]["cualquiera"] += int(bool(r.get("referencia_cualquiera")))
                        if r.get("referencias"): imp[o]["ref"].append(r["referencias"])
                        if o in ("net", "camouflage") and abs(float((r.get("efecto") or {}).get("cuerpo") or 0.0)) <= 1.0: nada["P33"].append(p33); nada["A"].append(a); nada["n"] += 1
            dias[d] = x
        manda = [(d, max(("botiquin", "racion", "red", "camuflaje"), key=lambda o: x[o]["curiosidad_A"])) for d, x in sorted(dias.items())]
        ult = max((d for d, top in manda if top in ("red", "camuflaje")), default=None)
        deja = ("no llega" if (ult == 20) else (ult + 1 if ult is not None else 1))
        R["criaturas"][k] = {"dias": dias, "manda": manda, "deja_de_mandar_lo_inutil_el_dia": deja}
    for o in COSAS:
        R["importancia"][NOM[o]] = {"recuerdos": imp[o]["n"], "sin_referencia": imp[o]["sin_ref"], "referencia_cualquiera": imp[o]["cualquiera"], "referencias_cuartiles": q(imp[o]["ref"]), "P33_cuartiles": q(imp[o]["P33"]), "A_cuartiles": q(imp[o]["A"]), "A_ceros": sum(1 for a in imp[o]["A"] if a == 0.0)}
    R["no_hizo_nada"] = {"recuerdos": nada["n"], "P33_cuartiles": q(nada["P33"]), "A_cuartiles": q(nada["A"]), "A_ceros": sum(1 for a in nada["A"] if a == 0.0)}
    cierres = sum(len(x["manda"]) for x in R["criaturas"].values()); inut = sum(1 for x in R["criaturas"].values() for d, top in x["manda"] if top in ("red", "camuflaje"))
    c15 = sum(1 for x in R["criaturas"].values() for d, top in x["manda"] if d >= 15); i15 = sum(1 for x in R["criaturas"].values() for d, top in x["manda"] if d >= 15 and top in ("red", "camuflaje"))
    dif = max((abs(x[o]["creencia_A"] - x[o]["creencia_P37"]) for cr in R["criaturas"].values() for x in cr["dias"].values() for o in ("botiquin", "racion") if x[o]["creencia_A"] is not None and x[o]["creencia_P37"] is not None), default=None)
    mb = st.median(imp["first_aid"]["A"]) if imp["first_aid"]["A"] else None; mi = st.median(imp["net"]["A"] + imp["camouflage"]["A"]) if (imp["net"]["A"] + imp["camouflage"]["A"]) else None
    R["criterios"] = {"I1": {"inutil_mediana": (round(mi, 4) if mi is not None else None), "botiquin_mediana": (round(mb, 4) if mb is not None else None), "pasa": bool(mi is not None and mb is not None and mi <= 0.3 * mb)},
                      "I2": {"no_hizo_nada_mediana": (round(st.median(nada["A"]), 4) if nada["A"] else None), "pasa": bool(nada["A"] and st.median(nada["A"]) <= 0.02)},
                      "I3": {"cierres": cierres, "lo_inutil_manda": inut, "cierres_15_20": c15, "lo_inutil_manda_15_20": i15, "pasa": bool(inut <= 40 and i15 <= 0.2 * c15)},
                      "I5": {"max_diferencia_creencia_util": (round(dif, 4) if dif is not None else None), "pasa": bool(dif is not None and dif <= 0.10)}}
    R["lectura"] = LECTURA; json.dump(R, open(os.path.join(AQUI, f"P7_39_cuadernos_{LECTURA}.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(R["importancia"], ensure_ascii=False)); print(R["no_hizo_nada"]); print(R["criterios"]); print({k: v["deja_de_mandar_lo_inutil_el_dia"] for k, v in R["criaturas"].items()})
