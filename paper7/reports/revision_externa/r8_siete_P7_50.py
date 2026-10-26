"""8 · Los recuerdos recibidos de P7-50 que contradicen el efecto real, con el criterio de analiza_P7_50.py:37-40 (copiado del analisis sellado
para listarlos uno a uno). Lee escaneo.json, la salida de r5_r8_escanea_P7_50.py."""
import json, collections as C
from comun import sal
E = json.load(open(sal("escaneo.json")))
signo_real = {"first_aid": 1, "rations": 1, "net": 0, "camouflage": 0}
def contradice(o, ef):
    e = float((ef or {}).get("cuerpo") or 0.0); return (e > 1.0) if signo_real.get(o, 0) == 0 else (e <= 0.0)
REC, VIS = E["REC"], E["VIS"]
serie = lambda r: r["_tag"].split("_")[1]; brazo = lambda r: r["_tag"].split("_")[3]
print("recibidos (COMPARTE):", len(REC), "contados +", len(VIS), "vistos =", len(REC) + len(VIS), "| por via", dict(C.Counter(r["via"] for r in REC)))
print("por serie", dict(C.Counter(serie(r) for r in REC + VIS)), "por brazo", dict(C.Counter(brazo(r) for r in REC + VIS)))
mal = [r for r in REC + VIS if contradice(r.get("objeto"), r.get("efecto"))]
print("contradicen:", len(mal), dict(C.Counter(serie(r) for r in mal)))
for r in sorted(mal, key=lambda r: (r["_sl"], r["_tag"])):
    print(" ", r["_tag"], "asiento", r["_sl"], r["k"], r.get("via"), r["objeto"], "cuerpo", r["efecto"]["cuerpo"], "| emisora: asiento", r.get("de"), "dia", r.get("dia_emisora"), "tick", r.get("tick_emisora"))
