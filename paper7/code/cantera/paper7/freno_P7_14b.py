"""[P7-14b] = freno_P7_14.py con los nombres de P7-14b (estado, semillas, cuadernos, diarios en paintball/runs/P714b_*). Nada mas cambia.
[cabecera de P7-14] EL FRENO: APRENDE, serie 1, dias 1 a 3. Solo las tres condiciones del sello, nada mas:
(a) el cuaderno viaja y se lee los dias 2 y 3; (b) hay pedidos y ningun regalo sin pedido; (c) en al menos una criatura la creencia del botiquin
sube y la ignorancia baja entre el fin del dia 1 y el del dia 3. -> P7_14b_freno.json"""
import glob, json, os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import campo_P7_14b as CP
OUT = {}
for dia in (1, 2, 3):
    carp = glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P714b_s1_d{dia}_APRENDE_*"))[0]
    for slot in (10, 11):
        f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log"))
        if f: OUT[f"s1_d{dia}_APRENDE_{slot}"] = {"serie": 1, "dia": dia, "brazo": "APRENDE", "slot": slot, **CP.lee_vida(f[0], "APRENDE")}
F = CP.freno(OUT)
b = json.loads(subprocess.run([sys.executable, os.path.join(AQUI, "analiza_P7_14b.py"), "--freno"], capture_output=True, text=True).stdout.strip().split("\n")[-1])
R = {"a_cuaderno_viaja": F["a_cuaderno_viaja"], "a_pasa": F["a_pasa"], "b": b, "b_pasa": b["b_pasa"], "c": F["c_creencia_sube_ignorancia_baja"], "c_pasa": F["c_pasa"], "pasa": bool(F["a_pasa"] and b["b_pasa"] and F["c_pasa"])}
json.dump(R, open(os.path.join(AQUI, "P7_14b_freno.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False))
