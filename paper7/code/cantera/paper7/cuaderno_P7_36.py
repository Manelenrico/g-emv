"""[P7-36, partes 2 y 3] LA REGLA DE LA INTENSIDAD COMO LA QUISO MANEL, recalculada sin jugar sobre los cuadernos de las cuatro criaturas de APRENDE de P7-34
(P7_34_res/cuaderno_s<S>_d<D>_APRENDE_<asiento>.json, los 20 dias):
  regla vieja (cuaderno_P7.apunta):  intensidad = 1 + min(1, S / E),  S = |imp_cuerpo| + |imp_recursos| + |imp_vinculo|, E = 1,5 (tope 2)
  regla nueva (mesa, P7-36):         intensidad = max(0,05, min(1, S / E))   (sin la base de 1; suelo 0,05 para que ningun recuerdo pese exactamente cero; el tope de 1 es el
                                     mismo min(1, S/E) de la regla vieja, declarado)
El peso de un recuerdo visto desde el dia d es intensidad x OLVIDO^(d - dia del recuerdo) (OLVIDO = 0,95, cuaderno_P7). Para cada criatura, dia y cosa: peso total de sus
recuerdos (`pesos_vividos`), creencia dentro del circulo (cuerpo, sin cortes: `CuadernoP29.creencia`) e ignorancia (`ignorancia` = neutro / (neutro + pesos)), con las dos
reglas, vistas al cerrar el dia d (dia = d, como las tablas de P7-34). Parte 3: la llamada de cada clase a la curiosidad es ignorancia x alivio (nace_P7_33._cands: la clase
que mas llama manda `ir_curioso`; alivio = 1 si no la lleva); se da, por criatura y cosa inutil, el primer dia tras cada prueba en que su ignorancia (regla nueva) vuelve a
ser la mayor de las cuatro (la clase que mas llama) y el primer dia en que vuelve a pasar de 0,5; y lo mismo con la regla vieja; frente a las repruebas reales de P7-34
(I4: s1 a11 red dia 11, s2 a11 red dia 18) y las pruebas reales de cada dia (P7_34_datos.json). -> P7_36_cuadernos.json
  python3 cuaderno_P7_36.py"""
import copy, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
for p in (os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    if p not in sys.path: sys.path.insert(0, p)
os.environ.setdefault("GEMV_P7", "1"); os.environ.setdefault("GEMV_P7_NACE", "1"); os.environ.setdefault("GEMV_P7_29", "1")
import cuaderno_P7 as CU, nace_P7_29 as N29
NOM = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camuflaje": "camuflaje", "camouflage": "camuflaje"}; COSAS = ("first_aid", "rations", "net", "camouflage"); SUELO = 0.05
N29.E["arreglos"]["corte"] = True


def intensidad_nueva(r):
    S = sum(abs(float((r.get("importancia") or {}).get(d) or 0.0)) for d in CU.DOMINIOS); return max(SUELO, min(1.0, S / CU.E_INTENSIDAD))


def con_regla(c0, nueva):
    c = N29.CuadernoP29(c0.criatura); c.dia = c0.dia; c.objetos = copy.deepcopy(c0.objetos)
    if nueva:
        for o in c.objetos.values():
            for sit in o["situaciones"].values():
                for r in sit: r["intensidad_vieja"] = r["intensidad"]; r["intensidad"] = round(intensidad_nueva(r), 4)
    return c


def medida(c, o, d):
    cre = c.creencia(o, "dentro", dia=d); cf = c.creencia(o, "fuera", dia=d)
    return {"peso": round(c.pesos_vividos(o, d), 4), "creencia": ((cre or {}).get("cuerpo") if cre is not None else ((cf or {}).get("cuerpo") if cf is not None else None)), "ignorancia": round(c.ignorancia(o, d), 4), "recuerdos": len(c.recuerdos_de(o))}


if __name__ == "__main__":
    D34 = {(v["serie"], v["asiento"], v["dia"]): v for v in json.load(open(os.path.join(AQUI, "P7_34_datos.json"))) if not v.get("sin_diario") and v["brazo"] == "APRENDE"}
    R = {"reglas": {"vieja": "1 + min(1, S/1,5)", "nueva": f"max({SUELO}, min(1, S/1,5))"}, "criaturas": {}}
    for s in (1, 2):
        for sl in (10, 11):
            k = f"s{s} a{sl}"; dias = {}
            for d in range(1, 21):
                f = os.path.join(AQUI, "P7_34_res", f"cuaderno_s{s}_d{d}_APRENDE_{sl}.json")
                if not os.path.exists(f): continue
                c0 = N29.CuadernoP29.lee(f); cv = con_regla(c0, False); cn = con_regla(c0, True)
                v = D34.get((s, sl, d)) or {}
                dias[d] = {NOM[o]: {"vieja": medida(cv, o, d), "nueva": medida(cn, o, d), "pruebas_del_dia": ((v.get("pruebas") or {}).get(NOM[o], {}) or {}).get("n"), "contacto_del_dia": ((v.get("contacto") or {}).get(NOM[o]))} for o in COSAS}
            # parte 3: cuando vuelve a mandar lo inutil (su ignorancia es la mayor de las cuatro) y cuando vuelve a pasar de 0,5, tras cada prueba
            despierta = {}
            for o in ("red", "camuflaje"):
                for regla in ("vieja", "nueva"):
                    pruebas = [d for d, x in dias.items() if (x[o]["pruebas_del_dia"] or 0) > 0]; out = []
                    for dp in pruebas:
                        manda = next((d for d in sorted(dias) if d > dp and dias[d][o][regla]["ignorancia"] >= max(dias[d][q][regla]["ignorancia"] for q in ("botiquin", "racion", "red", "camuflaje") if q != o) - 1e-9), None)
                        medio = next((d for d in sorted(dias) if d > dp and dias[d][o][regla]["ignorancia"] >= 0.5), None)
                        out.append({"prueba_dia": dp, "vuelve_a_mandar_dia": manda, "pasa_de_0_5_dia": medio})
                    despierta[f"{o} {regla}"] = out
            R["criaturas"][k] = {"dias": dias, "despierta": despierta, "pruebas_reales": {o: [d for d, x in dias.items() if (x[o]["pruebas_del_dia"] or 0) > 0] for o in ("red", "camuflaje")}}
    json.dump(R, open(os.path.join(AQUI, "P7_36_cuadernos.json"), "w"), ensure_ascii=False, indent=1)
    for k, x in R["criaturas"].items():
        for d in (5, 10, 15, 20):
            if d in x["dias"]: print(k, d, {o: (y["vieja"]["peso"], y["nueva"]["peso"], y["vieja"]["ignorancia"], y["nueva"]["ignorancia"], y["vieja"]["creencia"], y["nueva"]["creencia"]) for o, y in x["dias"][d].items()})
        print(k, "pruebas reales", x["pruebas_reales"], "despierta", x["despierta"])
