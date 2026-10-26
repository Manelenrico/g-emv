"""[P7-37, puntos 1 y 2, dia a dia] Sobre los 80 cuadernos encadenados con la importancia descontada (P7_37_res/cuaderno_descontada_s<S>_d<D>_<asiento>.json, banco_P7_37
--cadena) y los 80 del campo (P7_34_res/): para cada criatura, dia y cosa: importancia original y descontada (mediana del escalar min(1, S/E) de los recuerdos sin
cortes), importancia esperada (curiosa_P7_37.importancia_esperada: media ponderada con el neutro de importancia 1), ignorancia (la de siempre), curiosidad de clase del campo
(= ignorancia) y nueva (ignorancia x importancia esperada), creencia dentro (cuerpo, sin cortes) con el cuaderno del campo y con el descontado; que clase manda cada dia
(la de mas curiosidad), la curiosidad de lo inutil frente a lo util, y cuando vuelve a mandar lo inutil tras cada prueba y con que fuerza. -> P7_37_cuadernos.json
  python3 cuaderno_P7_37.py"""
import json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
for p in (os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    if p not in sys.path: sys.path.insert(0, p)
for k, v in (("GEMV_P7", "1"), ("GEMV_P7_NACE", "1"), ("GEMV_P7_29", "1"), ("GEMV_P7_33", "1"), ("GEMV_P7_37", "campo")): os.environ.setdefault(k, v)
import nace_P7_29 as N29, curiosa_P7_37 as CU
NOM = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}; COSAS = tuple(NOM); UT = ("first_aid", "rations"); IN = ("net", "camouflage")
N29.E["arreglos"]["corte"] = True


def lee(f): return N29.CuadernoP29.lee(f)
def cre(c, o, d):
    x = c.creencia(o, "dentro", dia=d) or c.creencia(o, "fuera", dia=d); return (x or {}).get("cuerpo")


if __name__ == "__main__":
    D34 = {(v["serie"], v["asiento"], v["dia"]): v for v in json.load(open(os.path.join(AQUI, "P7_34_datos.json"))) if not v.get("sin_diario") and v["brazo"] == "APRENDE"}
    R = {"criaturas": {}, "importancia": {}}
    imp_orig = {o: [] for o in COSAS}; imp_desc = {o: [] for o in COSAS}; desc_n = {o: [0, 0] for o in COSAS}
    for s in (1, 2):
        for sl in (10, 11):
            k = f"s{s} a{sl}"; dias = {}
            for d in range(1, 21):
                fd = os.path.join(AQUI, "P7_37_res", f"cuaderno_descontada_s{s}_d{d}_{sl}.json"); fc = os.path.join(AQUI, "P7_34_res", f"cuaderno_s{s}_d{d}_APRENDE_{sl}.json")
                if not (os.path.exists(fd) and os.path.exists(fc)): continue
                cd = lee(fd); cc = lee(fc); v = D34.get((s, sl, d)) or {}; x = {}
                for o in COSAS:
                    ign = cd.ignorancia(o, d); ie = CU.importancia_esperada(cd, o, d)
                    x[NOM[o]] = {"ignorancia": round(ign, 4), "ignorancia_campo": round(cc.ignorancia(o, d), 4), "importancia_esperada": round(ie, 4), "curiosidad_campo": round(cc.ignorancia(o, d), 4), "curiosidad_nueva": round(ign * ie, 4),
                                 "creencia_campo": cre(cc, o, d), "creencia_descontada": cre(cd, o, d), "recuerdos": len(cd.recuerdos_de(o)), "pruebas_del_dia": ((v.get("pruebas") or {}).get(NOM[o], {}) or {}).get("n")}
                if d == 20:
                    for o in COSAS:
                        for r in cd.recuerdos_de(o):
                            if r.get("corte"): continue
                            imp_desc[o].append(CU.escalar(r.get("importancia"))); imp_orig[o].append(CU.escalar(r.get("importancia_original") or r.get("importancia"))); desc_n[o][0] += 1; desc_n[o][1] += int(bool(r.get("descontada")))
                dias[d] = x
            # quien manda cada dia
            manda = {"campo": [], "nueva": []}
            for d, x in dias.items():
                for regla in ("campo", "nueva"):
                    cu_ = {o: x[o][f"curiosidad_{regla}"] for o in NOM.values()}; manda[regla].append((d, max(cu_, key=cu_.get)))
            # despertar: tras cada prueba de red/camuflaje, primer dia en que su curiosidad nueva supera la mayor de lo util, y su valor
            desp = {}
            for o in ("red", "camuflaje"):
                pruebas = [d for d, x in dias.items() if (x[o]["pruebas_del_dia"] or 0) > 0]; out = []
                for dp in pruebas:
                    sig = next((d for d in sorted(dias) if d > dp and dias[d][o]["curiosidad_nueva"] >= max(dias[d]["botiquin"]["curiosidad_nueva"], dias[d]["racion"]["curiosidad_nueva"]) - 1e-9), None)
                    out.append({"prueba_dia": dp, "vuelve_a_mandar_dia": sig, "curiosidad_entonces": (dias[sig][o]["curiosidad_nueva"] if sig else None), "curiosidad_util_entonces": (max(dias[sig]["botiquin"]["curiosidad_nueva"], dias[sig]["racion"]["curiosidad_nueva"]) if sig else None), "curiosidad_el_dia_de_la_prueba": dias[dp][o]["curiosidad_nueva"]})
                desp[o] = out
            R["criaturas"][k] = {"dias": dias, "manda": manda, "despierta": desp}
    for o in COSAS:
        R["importancia"][NOM[o]] = {"recuerdos": desc_n[o][0], "descontados": desc_n[o][1], "original_mediana": (round(st.median(imp_orig[o]), 4) if imp_orig[o] else None), "descontada_mediana": (round(st.median(imp_desc[o]), 4) if imp_desc[o] else None),
                                   "original_cuartiles": ([round(sorted(imp_orig[o])[len(imp_orig[o]) // 4], 4), round(sorted(imp_orig[o])[3 * len(imp_orig[o]) // 4], 4)] if imp_orig[o] else None), "descontada_cuartiles": ([round(sorted(imp_desc[o])[len(imp_desc[o]) // 4], 4), round(sorted(imp_desc[o])[3 * len(imp_desc[o]) // 4], 4)] if imp_desc[o] else None)}
    tot = {"campo": [0, 0], "nueva": [0, 0]}
    for k, x in R["criaturas"].items():
        for regla in ("campo", "nueva"):
            for d, top in x["manda"][regla]: tot[regla][0] += 1; tot[regla][1] += int(top in ("red", "camuflaje"))
    R["manda_lo_inutil"] = {regla: {"cierres": t[0], "lo_inutil_manda": t[1]} for regla, t in tot.items()}
    json.dump(R, open(os.path.join(AQUI, "P7_37_cuadernos.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(R["importancia"], ensure_ascii=False)); print(R["manda_lo_inutil"])
    for k, x in R["criaturas"].items():
        for d in (5, 10, 15, 20):
            if d in x["dias"]: print(k, d, {o: (y["curiosidad_campo"], y["curiosidad_nueva"], y["importancia_esperada"], y["creencia_campo"], y["creencia_descontada"]) for o, y in x["dias"][d].items()})
        print(k, x["despierta"])
