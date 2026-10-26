"""12 · La moneda de P7-46: reejecuta analiza_P7_46.py sin su escritura (P7_46_resumen.json) e imprime las forzadas (seccion 1) y R1 contado de nuevo
(seccion 5), comparandolos con el resumen sellado. Solo lectura."""
import json, os
from comun import P7
src = open(os.path.join(P7, "analiza_P7_46.py")).read().replace("os.path.dirname(os.path.abspath(__file__))", repr(P7))
ns = {"__name__": "analiza_P7_46_revision"}; exec(src[:src.index('\njson.dump(R, open(os.path.join(AQUI, "P7_46_resumen.json")')], ns)
R = ns["R"]; S = json.load(open(os.path.join(P7, "P7_46_resumen.json")))
fz = R["forzadas_SIN"]; print("forzadas", fz["n"], "acaban", fz["acaban"], "caducan", fz["caducan"], "sin fin", fz["sin_fin"], "| vidas SIN", len(ns["vidas"]("SIN")))
print("por tipo y fin", fz.get("por_tipo_fin"))
r1 = R["R1"]
for k in ("pruebas_botiquin_por_vida", "factor", "k_estrella", "rapidez_real", "rapidez_real_media", "SIN_real_media"): print(k, r1[k])
for fuente, fila in r1["contada"].items(): print("curva de", fuente, json.dumps(fila, ensure_ascii=False))
print("\nigual que P7_46_resumen.json:", {k: json.loads(json.dumps(R[k], ensure_ascii=False)) == S[k] for k in ("forzadas_SIN", "R1")})
a = json.loads(json.dumps(R["forzadas_SIN"], ensure_ascii=False)); b = S["forzadas_SIN"]
print("campos de las forzadas que difieren del resumen:", {k: (a.get(k), b.get(k)) for k in set(a) | set(b) if a.get(k) != b.get(k)})
