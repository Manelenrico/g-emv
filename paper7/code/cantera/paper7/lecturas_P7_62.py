"""[P7-62, punto 5] LECTURAS EXTRA SIN COSTE sobre las series 1-3 de P7-61 (descriptivas, sin sello), con las funciones de analiza_P7_61 (mismas vidas, mismas definiciones).
  (a) puesto medio, muertes y vida perdida media ANTES (dias 1-7) y DESPUES (dias 8-20) de la falsa, por brazo y hermana; lo mismo en CON_RAZON de P7-56 (sin falsa: el corte en el dia 8
      solo parte el campo igual) para ver si la mejora frente a P7-56 empieza con la falsa o ya estaba antes.
  (b) dias 1-7 de P7-61 (razon honesta, menu SIN EMPUNAR_RED) como replica de CON_RAZON de P7-56 (menu con EMPUNAR_RED) en los mismos dias: fraccion de usos del botiquin cortados por un
      golpe y confianza por dimension (cuaderno al cerrar cada dia, media de los dias 1-7, y al dia 7), por brazo y serie.
  python3 lecturas_P7_62.py -> P7_62_lecturas.json"""
import json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI); sys.argv = sys.argv[:1]
import analiza_P7_61 as A
mean = lambda xs: (round(st.mean(xs), 3) if xs else None)


def conf_dims(C, S, d, b, sl):
    f = os.path.join(AQUI, C["res"], f"cuaderno_s{S}_d{d}_{b}_{sl}.json")
    return (json.load(open(f)).get("confianza_razon_P7_54") or {}) if os.path.exists(f) else {}


V = A.carga("P7_57", [1, 2, 3]); V56 = A.carga("P7_56", None); R = {"a": {}, "b": {}}
for nombre, VV, brazos in (("P7_61", V, ("MIENTEN_DOS", "MIENTE_UNA")), ("P7_56", V56, ("CON_RAZON",))):
    for b in brazos:
        for sl, h in ((10, "valiente"), (11, "prudente")):
            for tramo, ds in (("d1-7", range(1, 8)), ("d8-20", range(8, 21))):
                vs = [v for (s, d, bb, ss), v in VV.items() if bb == b and ss == sl and d in ds]
                R["a"][f"{nombre} {b} · {h} · {tramo}"] = {"vidas": len(vs), "puesto_medio": mean([v["puesto"] for v in vs if v["puesto"] is not None]), "muertes": sum(1 for v in vs if v["murio"]),
                                                          "fraccion_muertes": round(sum(1 for v in vs if v["murio"]) / len(vs), 3) if vs else None, "vida_perdida_media": mean([v["vida_perdida"] for v in vs])}
        C = A.CAMPOS[nombre.replace("P7_61", "P7_57")]
        for S in (1, 2, 3):
            vs = [v for (s, d, bb, ss), v in VV.items() if bb == b and s == S and 1 <= d <= 7]; u = sum(v["usos_kit"] for v in vs); c = sum(v["cortados"] for v in vs)
            cf = {dim: [conf_dims(C, S, d, b, sl).get(dim) for d in range(1, 8) for sl in (10, 11)] for dim in ("cuerpo", "recursos", "vinculo")}
            R["b"][f"{nombre} {b} s{S}"] = {"usos_kit": u, "cortados": c, "fraccion_cortada": round(c / u, 3) if u else None,
                                            "confianza_media_d1_7": {k: mean([x for x in xs if x is not None]) for k, xs in cf.items()},
                                            "confianza_d7": {k: mean([conf_dims(C, S, 7, b, sl).get(k) for sl in (10, 11) if conf_dims(C, S, 7, b, sl).get(k) is not None]) for k in ("cuerpo", "recursos", "vinculo")}}
json.dump(R, open(os.path.join(AQUI, "P7_62_lecturas.json"), "w"), ensure_ascii=False, indent=1)
for k, v in R["a"].items(): print(k, v)
for k, v in R["b"].items(): print(k, v)
