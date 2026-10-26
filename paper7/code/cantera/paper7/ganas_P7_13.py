"""[P7-13, punto 5] ¿LAS GANAS DE APRENDE SON LAS DE TECHO CON LA MISMA CREENCIA? Sin cambiar nada: se llama a `descubre_P7.k_ganas` y a
`descubre_P7.heal_imaginado` con un cuaderno de pega cuya creencia es la cura del catalogo y cuya ignorancia se barre, y se apuntan los tres
numeros que `descubre_P7._filas` pone en el cuerpo (:332): ACOPIO_M, ACOPIO_POR_DOS y W_TARGET. Constantes leidas de los modulos.
  python3 ganas_P7_13.py -> P7_13_ganas.json"""
import glob, json, os, sys, types
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "paintball"), RAIZ): sys.path.insert(0, p)
OUT = {}
def brazo(nombre, env, ignorancias):
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = env.get(k, "0")
    for m in ("descubre_P7",): sys.modules.pop(m, None)
    import descubre_P7 as X
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", "P710_s1_d1_APRENDE_*", "*agent_10.art.log"))[0]; cat = None; kid = None
    for line in open(f):
        r = json.loads(line)
        if r.get("k") == "catalogo": cat = r["items"]
        if r.get("k") == "mundo_leido": kid = r["id_botiquin"]; break
    mundo = types.SimpleNamespace(id_botiquin=kid, items={i["id"]: types.SimpleNamespace(**i) for i in cat})
    cura = X.cura_catalogo(mundo); filas = []
    for ign in ignorancias:
        X.ESTADO["cuaderno"] = types.SimpleNamespace(creencia_max_cuerpo=lambda o: cura, creencia_cuerpo=lambda o, s: cura, ignorancia=lambda o, _i=ign: _i)
        k = X.k_ganas(mundo)
        filas.append({"ignorancia": ign, "creencia": cura, "k_ganas": round(k, 5), "ACOPIO_M": round(X.ACOPIO_M0 * k, 5), "ACOPIO_POR_DOS": round(X.ACOPIO_POR_DOS0 * k, 5), "W_TARGET": round(X.W_TARGET0 if X.SABE else 2.0 + k, 5),
                      "peso_del_botiquin_en_W": round(1.0 if X.SABE else k, 5), "cura_imaginada_al_usar": (cura if X.SABE else round(X.heal_imaginado(mundo, (0, 0), 0) if False else X.mezcla(mundo, cura), 4)), "k_del_regalo": round(X.k_creencia(mundo), 5)})
    OUT[nombre] = {"cura_catalogo": cura, "esperanza": X.esperanza_cuerpo(mundo), "ACOPIO_M0": X.ACOPIO_M0, "ACOPIO_POR_DOS0": X.ACOPIO_POR_DOS0, "W_TARGET0": X.W_TARGET0, "filas": filas}
brazo("TECHO", {"GEMV_P7": "1", "GEMV_P7_SABE": "1", "GEMV_P7_SITIO": "1"}, [0.0])
brazo("APRENDE", {"GEMV_P7": "1", "GEMV_P7_CUADERNO": "1", "GEMV_P7_NOVEDAD": "1", "GEMV_P7_SITIO": "1"}, [0.0, 0.05, 0.1, 0.2, 0.5, 1.0])
json.dump(OUT, open(os.path.join(AQUI, "P7_13_ganas.json"), "w"), ensure_ascii=False, indent=1)
for n, d in OUT.items():
    for f in d["filas"]: print(n, f)
