"""[P7-5] Reconstruye el cuaderno de una criatura a partir de su diario (los registros P7_uso y P7_huella, en orden), con la misma regla
(`cuaderno_P7.Cuaderno.apunta`): es exactamente lo que el cuerpo escribio en /app/cuadernos al acabar. Hizo falta el dia 1 del humo,
cuyo registro de fin no viajo en el artefacto (se escribia despues de la subida). Declarado en el informe.
  python3 reconstruye_cuaderno_P7_5.py DIARIO.art.log ASIENTO DIA_PREVIO(cuaderno leido al arrancar, o -) SALIDA.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cuaderno_P7 import Cuaderno
f, slot, previo, salida = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
c = Cuaderno.lee(previo, slot) if previo != "-" else Cuaderno(slot)
usos = 0; n = 0
for line in open(f):
    if '"P7_uso"' in line or '"P7_huella"' in line:
        r = json.loads(line)
        if r.get("k") == "P7_uso": c.cuenta_uso("first_aid"); usos += 1
        elif r.get("k") == "P7_huella" and r.get("apuntado"): c.apunta("first_aid", r["situacion"], r["efecto"], r["importancia"], tick=r["t0"]); n += 1
c.escribe(salida); print(f"-> {salida}: usos {usos}, recuerdos {n}, dia {c.dia}, creencias {json.dumps(c.creencias())[:300]}")
