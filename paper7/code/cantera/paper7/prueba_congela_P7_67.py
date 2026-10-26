"""[P7-67, campo] PRUEBAS A MANO del brazo CONGELADA (congela_P7_67), con el `decidir` real de invita_P7_66b y el cuaderno real de descubre_P7. Sin plataforma, sin API.
  1. control (sin la pieza): una llegada juzgada 0 baja la confianza en recursos de 0,5 a 0,35;
  2. con la pieza: la misma llegada se juzga y se registra igual (acierto 0, confianza_despues 0,35 en el registro), y al acabar el `decidir` la confianza es 0,5 en las tres dimensiones,
     con su registro P7_67_congela;
  3. al arrancar el dia con un cuaderno que trae 0,35, queda en 0,5; el cuaderno que se escribe al cerrar lleva 0,5 en las tres; registro P7_67_congela_cierre.
  python3 prueba_congela_P7_67.py"""
import json, os, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "cantera", "paper6"), RAIZ]
for k, v in (("GEMV_P7", "1"), ("GEMV_P7_CUADERNO", "1"), ("GEMV_P7_54", "1"), ("GEMV_P7_66", "1"), ("GEMV_P7_67", "1"), ("GEMV_P7_67_ACTIVOS", "4"), ("GEMV_P7_67B", "1"), ("GEMV_P7_67_CONGELA", "1")): os.environ[k] = v
import descubre_P7 as X, invita_P7_54 as IN, invita_P7_66b as I66, invita_P7_67 as I67, invita_P7_67b as B, congela_P7_67 as CG, nace_P7_23 as N
OK = []; MAL = []; LOG = []
def caso(n, c, d=""): (OK if c else MAL).append(n); print(("PASA " if c else "FALLA") + " · " + n + (f" · {d}" if d else ""))
class Mundo:
    slot = 10; teammate_slot = 11; id_botiquin = "first_aid"
    def solido(self, x, y): return False
class Prueba:
    def decidir(self, obs_): return {"type": "action", "do": "none"}, {"elegido": "noop"}
I66.aplica(Prueba, LOG.append); I67.aplica(Prueba, LOG.append); B.aplica(Prueba, LOG.append)
alma = Prueba(); alma.mundo = Mundo(); alma.phase = "live"; alma.mem = None; N.E["ultimo_dano"] = None
INV = {"_k": 0, "accion": "IR_A_SITIO", "destino": [3, 1], "calma5": "CALMA5", "falsa": True}
def llega():
    I66.E["abiertas"] = [{"inv": INV, "t0": 500, "destino": (3, 1)}]; I66.E["tic0"] = 481; IN.E["conf"] = {"cuerpo": 0.5, "recursos": 0.5, "vinculo": 0.5}; LOG.clear()
    alma.tick = 560; alma.decidir({"you": {"pos": [4, 1]}, "visible": {"agents": [], "items": [{"id": "first_aid", "pos": [9, 9]}]}})
    return next((r for r in LOG if r["k"] == "P7_66_llegada"), None)
r = llega()
caso("1 control sin la pieza: llegada juzgada 0 -> recursos 0,35", r is not None and r["acierto_recursos"] == 0 and abs(IN.E["conf"]["recursos"] - 0.35) < 1e-9, IN.E["conf"])
h = CG.aplica(Prueba, LOG.append)
r = llega()
caso("2a con la pieza: la llegada se juzga y se registra igual (acierto 0, confianza_despues 0,35)", r is not None and r["acierto_recursos"] == 0 and abs(r["confianza_despues"]["recursos"] - 0.35) < 1e-9, r and r["confianza_despues"])
caso("2b al acabar el decidir la confianza es 0,5 en las tres dimensiones", IN.E["conf"] == {"cuerpo": 0.5, "recursos": 0.5, "vinculo": 0.5}, IN.E["conf"])
caso("2c queda el registro P7_67_congela (antes 0,35)", any(x["k"] == "P7_67_congela" and abs(x["antes"]["recursos"] - 0.35) < 1e-9 for x in LOG))
d = tempfile.mkdtemp(); ruta = os.path.join(d, "cuaderno_P7_10.json"); json.dump({"confianza_razon_P7_54": {"cuerpo": 0.2, "recursos": 0.35, "vinculo": 0.9}}, open(ruta, "w"))
IN.aplica(Prueba, None)            # la carga de la confianza desde el cuaderno es de invita_P7_54: se aplica y despues otra vez la pieza, como en la imagen (la pieza va la ultima)
CG.aplica(Prueba, LOG.append); LOG.clear()
c = X.arranca(10, ruta, LOG.append)
caso("3a0 (control de la prueba) invita_P7_54 si leyo 0,35 del cuaderno antes de fijar", any(x["k"] == "P7_54_arranque" and abs(x["confianza"]["recursos"] - 0.35) < 1e-9 for x in LOG), [x.get("confianza") for x in LOG if x["k"] == "P7_54_arranque"])
caso("3a al arrancar con un cuaderno de 0,2 / 0,35 / 0,9 queda 0,5 en las tres", IN.E["conf"] == {"cuerpo": 0.5, "recursos": 0.5, "vinculo": 0.5}, IN.E["conf"])
IN.E["conf"]["recursos"] = 0.35; X.termina(LOG.append)
esc = json.load(open(ruta)).get("confianza_razon_P7_54")
caso("3b el cuaderno escrito al cerrar lleva 0,5 en las tres", esc == {"cuerpo": 0.5, "recursos": 0.5, "vinculo": 0.5}, esc)
caso("3c registro P7_67_congela_cierre", any(x["k"] == "P7_67_congela_cierre" for x in LOG))
print(f"\n{len(OK)} pasan, {len(MAL)} fallan" + (f": {MAL}" if MAL else ""))
json.dump({"pasan": OK, "fallan": MAL}, open(os.path.join(AQUI, "P7_67_congela_pruebas.json"), "w"), ensure_ascii=False, indent=1); sys.exit(1 if MAL else 0)
