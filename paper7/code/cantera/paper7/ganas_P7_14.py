"""[P7-14, paso 1] COMPROBACION DEL ARREGLO con el cuaderno DE VERDAD (`cuaderno_P7.Cuaderno`): recuerdos firmes con efecto igual a la cura del
catalogo; k de las ganas, W_TARGET y R-ACOPIO de APRENDE con su ignorancia real y con la ignorancia puesta a 0, contra TECHO. -> P7_14_ganas.json"""
import glob, json, os, sys, types
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "paintball"), RAIZ): sys.path.insert(0, p)
for k, v in {"GEMV_P7": "1", "GEMV_P7_CUADERNO": "1", "GEMV_P7_NOVEDAD": "1", "GEMV_P7_SITIO": "1", "GEMV_P7_SABE": "0", "GEMV_P7_BORRADO": "0"}.items(): os.environ[k] = v
import descubre_P7 as X
from cuaderno_P7 import Cuaderno
f = glob.glob(os.path.join(RAIZ, "paintball", "runs", "P710_s1_d1_APRENDE_*", "*agent_10.art.log"))[0]
for line in open(f):
    r = json.loads(line)
    if r.get("k") == "catalogo": cat = r["items"]
    if r.get("k") == "mundo_leido": kid = r["id_botiquin"]; break
mundo = types.SimpleNamespace(id_botiquin=kid, items={i["id"]: types.SimpleNamespace(**i) for i in cat}); cura = X.cura_catalogo(mundo); OUT = {"TECHO": {"k": 1.0, "ACOPIO_M": X.ACOPIO_M0, "ACOPIO_POR_DOS": X.ACOPIO_POR_DOS0, "W_TARGET": X.W_TARGET0}, "APRENDE": []}
for n_rec in (1, 3, 10, 30):
    c = Cuaderno(10)
    for i in range(n_rec): c.apunta(kid, "dentro", {"cuerpo": cura, "recursos": -1, "vinculo": 0}, {"cuerpo": 0, "recursos": 0, "vinculo": 0}, tick=i)
    X.ESTADO["cuaderno"] = c
    fila = {"recuerdos": n_rec, "ignorancia": round(c.ignorancia(kid), 5), "creencia_con_neutro": c.creencia_cuerpo(kid, "dentro"), "creencia_vivida": c.creencia_vivida_cuerpo(kid, "dentro"), "k": round(X.k_ganas(mundo), 6), "W_TARGET": round(2.0 + X.k_ganas(mundo), 6), "ACOPIO_M": round(X.ACOPIO_M0 * X.k_ganas(mundo), 6), "k_del_regalo": round(X.k_creencia(mundo), 6)}
    _ig = c.ignorancia; c.ignorancia = lambda o, dia=None: 0.0
    k0 = X.k_ganas(mundo); fila["con_ignorancia_0"] = {"k": k0, "W_TARGET": 2.0 + k0, "ACOPIO_M": X.ACOPIO_M0 * k0, "ACOPIO_POR_DOS": X.ACOPIO_POR_DOS0 * k0, "cura_imaginada": X.mezcla(mundo, c.creencia_vivida_cuerpo(kid, "dentro")),
                                        "igual_a_TECHO": (k0 == 1.0 and 2.0 + k0 == X.W_TARGET0 and X.ACOPIO_M0 * k0 == X.ACOPIO_M0 and X.ACOPIO_POR_DOS0 * k0 == X.ACOPIO_POR_DOS0)}
    c.ignorancia = _ig; OUT["APRENDE"].append(fila); print(fila)
X.ESTADO["cuaderno"] = Cuaderno(10); OUT["sin_recuerdos"] = {"k": X.k_ganas(mundo), "cura_imaginada": X.mezcla(mundo, None)}; print("sin recuerdos:", OUT["sin_recuerdos"])
json.dump(OUT, open(os.path.join(AQUI, "P7_14_ganas.json"), "w"), ensure_ascii=False, indent=1)
