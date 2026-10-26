"""[P7-7, decision 1] Recalcula el cuaderno del asiento 11 de P7-6 (P7_6_dia3_cuaderno_11.json: un recuerdo, uso del botiquin en el tic
10665 con la vida a 99 de 100, efecto cuerpo +1) con la regla del recuerdo con techo: la huella de ese uso (diario P76_humo_APRENDE_27068301,
asiento 11) acaba con hp_fin 100 = maximo -> "al menos". Se escribe el cuaderno recalculado (P7_7_cuaderno_11_recalculado.json) y se compara,
cifra a cifra, con el de P7-6; y se calcula ademas que pasaria si llegara un recuerdo firme (ilustracion, no dato del campo).
-> P7_7_recalculo.json"""
import glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..")); sys.path.insert(0, AQUI)
from cuaderno_P7 import Cuaderno
viejo = json.load(open(os.path.join(AQUI, "P7_6_dia3_cuaderno_11.json")))
f = glob.glob(os.path.join(RAIZ, "paintball", "runs", "P76_humo_APRENDE_27068301", "*policy_agent_11.art.log"))[0]
huellas = [json.loads(l) for l in open(f) if '"P7_huella"' in l[:40]]
hp_max = None
for l in open(f):
    if '"k":"tick"' in l[:12] or '"k": "tick"' in l[:12]:
        r = json.loads(l); hp_max = max(hp_max or 0, float(r.get("hp") or 0))
c = Cuaderno.lee(None, 11); c.dia = viejo["dia"] - 1          # el dia 3 se esta viviendo: tras escribir queda en 3, como el de P7-6
R = {"fuente": {"cuaderno_P7_6": "P7_6_dia3_cuaderno_11.json", "diario": os.path.relpath(f, RAIZ), "hp_max_visto_en_el_diario": hp_max}, "huellas": []}
for h in huellas:
    techo = float(h["hp_fin"]) >= float(hp_max)
    r = c.apunta("first_aid", h["situacion"], h["efecto"], h["importancia"], tick=h["t0"], al_menos=techo)
    R["huellas"].append({"t0": h["t0"], "situacion": h["situacion"], "hp0": h["hp0"], "hp_fin": h["hp_fin"], "al_menos": techo, "recuerdo": r})
c.escribe(os.path.join(AQUI, "P7_7_cuaderno_11_recalculado.json"))
nuevo = c.volcado()
R["P7_6"] = {"dia": viejo["dia"], "creencias": viejo["creencias"]}
R["P7_7"] = {"dia": nuevo["dia"], "creencias": nuevo["creencias"], "al_menos_marcados": sum(1 for _, _, r in c.recuerdos() if r.get("al_menos"))}
# vista desde el dia siguiente (como la leeria el dia 4), con las dos reglas
R["vista_dia_4"] = {"P7_7": c.creencia("first_aid", "dentro"), "ignorancia": c.ignorancia("first_aid")}
# ilustracion: si llegara un recuerdo FIRME de cura 40 (vida 50 -> 90) en la misma situacion, con y sin la regla del techo
c2 = Cuaderno.lee(os.path.join(AQUI, "P7_7_cuaderno_11_recalculado.json"), 11)
c2.apunta("first_aid", "dentro", {"cuerpo": 40.0, "recursos": -1.0, "vinculo": 0.0}, {"cuerpo": -0.3, "recursos": -0.04, "vinculo": 0.0}, tick=0, al_menos=False)
con_regla = c2.creencia("first_aid", "dentro")
for _, _, r in c2.recuerdos(): r["al_menos"] = False
sin_regla = c2.creencia("first_aid", "dentro")
R["ilustracion_recuerdo_firme_40"] = {"nota": "hipotetico, no es dato del campo: un segundo recuerdo firme de +40 en 'dentro' el dia 4", "con_regla_del_techo": con_regla, "sin_regla_(P7_6)": sin_regla}
json.dump(R, open(os.path.join(AQUI, "P7_7_recalculo.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
