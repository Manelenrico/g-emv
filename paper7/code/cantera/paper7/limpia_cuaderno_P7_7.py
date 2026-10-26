"""[P7-7] Reconstruye el cuaderno de una criatura desde las huellas de su diario con la regla corregida (una ventana que se cierra con el
botiquin aun en el zurron es un canal interrumpido: no es experiencia de la cosa, no se apunta) y la marca "al menos" por hp_max.
  python3 limpia_cuaderno_P7_7.py CARP SLOT DIA_PREVIO ENTRADA_O_VACIO SALIDA
Lee el cuaderno de entrada (el que la criatura leyo al arrancar ese dia; vacio = ninguno), le apunta las huellas no interrumpidas del
diario y escribe la salida (dia = DIA_PREVIO + 1). Imprime las creencias antes y despues."""
import glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..")); sys.path.insert(0, AQUI)
from cuaderno_P7 import Cuaderno
carp, slot, entrada, salida = sys.argv[1], int(sys.argv[2]), sys.argv[4], sys.argv[5]
f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]
H = [json.loads(l) for l in open(f) if '"P7_huella"' in l[:40]]
# [P7-10] los tics en que el cuerpo eligio soltar_first_aid (regalo), para anular las ventanas que los contienen
REGALO_T = []
for l in open(f):
    if '"k":"tick"' in l[:12]:
        r_ = json.loads(l)
        if str((r_.get("RADIOGRAFIA") or {}).get("elegido") or "").startswith("soltar_first_aid"): REGALO_T.append((r_["tick"], r_["tick"]))
c = Cuaderno.lee(entrada if entrada != "vacio" else None, slot)
if entrada == "vacio": c.dia = int(sys.argv[3])
hp_max = max(float(json.loads(l).get("hp") or 0) for l in open(f) if '"k":"tick"' in l[:12])
quitadas = []; puestas = []
for h in H:
    interrumpido = h.get("interrumpido") if h.get("interrumpido") is not None else (h["efecto"]["recursos"] >= 0)
    if h.get("regalado") or (h.get("regalado") is None and REGALO_T and any(t0_ <= h["t0"] <= t1_ or h["t0"] <= t0_ <= h["t_fin"] for t0_, t1_ in REGALO_T)): interrumpido = True   # [P7-10] regalo durante la ventana
    if interrumpido: quitadas.append(h["t0"]); continue
    c.apunta("first_aid", h["situacion"], h["efecto"], h["importancia"], tick=h["t0"], al_menos=(h.get("al_menos") if h.get("al_menos") is not None else float(h["hp_fin"]) >= hp_max)); puestas.append(h["t0"])
c.escribe(salida)
print(json.dumps({"diario": os.path.relpath(f, RAIZ), "hp_max": hp_max, "huellas": len(H), "apuntadas": puestas, "interrumpidas_no_apuntadas": quitadas, "dia": c.dia, "creencias": c.creencias()}, ensure_ascii=False, indent=1))
