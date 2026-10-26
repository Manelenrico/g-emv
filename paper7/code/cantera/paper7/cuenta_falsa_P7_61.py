"""[P7-61, addendum 4] CUENTA de las evaluaciones de la invitacion FALSA (solo el numero, para la regla de tamano de muestra; sin mirar resultados). La falsa se identifica
exactamente: en una vida del asiento que miente (mentira_P7_57.miente) del dia d, su indice es la posicion de mentira_P7_57.anade = Random(1000 S + 10 (d - 1) + asiento).randint(0, n
honestas), con n honestas = invitaciones del arranque - 1. Cuenta = registros P7_54_evaluada con ese indice. Intentos parados (P757r_*) fuera.  python3 cuenta_falsa_P7_61.py"""
import glob, json, os, random, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "paintball", "runs"); sys.path.insert(0, AQUI)
import mentira_P7_57 as MT
n = {}
for f in glob.glob(os.path.join(RUNS, "P757_s*_d*_*", "*policy_agent_1[01].art.log")):
    m = re.search(r"P757_s(\d+)_d(\d+)_(MIENTEN_DOS|MIENTE_UNA)_.*agent_(\d+)\.art", f); S, d, b, sl = int(m[1]), int(m[2]), m[3], int(m[4])
    if not MT.miente(b, sl, d): continue
    ninv = None; ev = []
    for l in open(f, errors="replace"):
        if l.startswith('{"k":"P7_57_arranque"'): ninv = json.loads(l)["invitaciones"]
        elif l.startswith('{"k":"P7_54_evaluada"'): ev.append(json.loads(l))
    if not ninv: continue
    pos = random.Random(1000 * S + 10 * (d - 1) + sl).randint(0, ninv - 1)
    k = (S, b, sl); n[k] = n.get(k, 0) + sum(1 for e in ev if e["n"] == pos and e["accion"] == "USAR_BOTIQUIN")
for S in sorted({k[0] for k in n}): print(f"serie {S}:", {f"{k[1]} a{k[2]}": v for k, v in sorted(n.items()) if k[0] == S}, "total", sum(v for k, v in n.items() if k[0] == S))
print("TOTAL", sum(n.values()))
