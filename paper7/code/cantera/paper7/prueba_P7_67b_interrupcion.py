"""[P7-67, antes del sello] PRUEBA DE PUNTA A PUNTA de la interrupcion con invita_P7_67b: el `decidir` real de invita_P7_66b (con invita_P7_54, P7_67 y P7_67b aplicadas encima de una
clase de prueba) con un intento ya aceptado y abierto. Sin plataforma, sin API.
  1. rival ACTIVO (asiento 4) a 3 antes de llegar -> P7_66_interrumpida, no se juzga (sin P7_66_llegada) y la confianza no cambia;
  2. estatua (asiento 7) a 1 -> sigue abierto;  3. rival activo a 4 -> sigue abierto;  4. activo a 3 en el mismo tic en que llega -> cuenta la llegada (el juicio de llegar va primero).
  python3 prueba_P7_67b_interrupcion.py"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "cantera", "paper6"), RAIZ]
for k, v in (("GEMV_P7_54", "1"), ("GEMV_P7_66", "1"), ("GEMV_P7_67", "1"), ("GEMV_P7_67_ACTIVOS", "4"), ("GEMV_P7_67B", "1")): os.environ[k] = v
import invita_P7_54 as IN, invita_P7_66b as I66, invita_P7_67 as I67, invita_P7_67b as B, nace_P7_23 as N
OK = []; MAL = []; LOG = []
def caso(n, c, d=""): (OK if c else MAL).append(n); print(("PASA " if c else "FALLA") + " · " + n + (f" · {d}" if d else ""))
class Mundo:
    slot = 10; teammate_slot = 11; id_botiquin = "first_aid"
    def solido(self, x, y): return False
class Prueba:
    def decidir(self, obs_): return {"type": "action", "do": "none"}, {"elegido": "noop"}
I66.aplica(Prueba, LOG.append); I67.aplica(Prueba, LOG.append); B.aplica(Prueba, LOG.append)      # solo el decidir de invita_P7_66b envuelve la clase (invita_P7_54 se usa por su estado)
alma = Prueba(); alma.mundo = Mundo(); alma.phase = "live"; alma.mem = None; N.E["ultimo_dano"] = None
INV = {"_k": 0, "accion": "IR_A_SITIO", "destino": [3, 1], "calma5": "CALMA5", "falsa": True}
def abre(): I66.E["abiertas"] = [{"inv": INV, "t0": 500, "destino": (3, 1)}]; I66.E["tic0"] = 481; LOG.clear(); IN.E["conf"]["recursos"] = 0.5
def obs(pos, ag): return {"you": {"pos": list(pos)}, "visible": {"agents": [{"slot": s, "pos": list(p)} for s, p in ag], "items": [{"id": "first_aid", "pos": [3, 2]}]}}
def paso(t, o): alma.tick = t; alma.decidir(o); return [r["k"] for r in LOG if r["k"].startswith("P7_66_")]
abre(); k = paso(560, obs((12, 5), [(4, (15, 5))]))
caso("1 rival ACTIVO a 3 antes de llegar -> interrumpida, sin juicio, confianza igual", k == ["P7_66_interrumpida"] and I66.E["abiertas"] == [] and IN.E["conf"]["recursos"] == 0.5, k)
abre(); k = paso(560, obs((12, 5), [(7, (13, 5))]))
caso("2 estatua a 1 -> sigue abierto", k == [] and len(I66.E["abiertas"]) == 1, k)
abre(); k = paso(560, obs((12, 5), [(4, (16, 5))]))
caso("3 rival activo a 4 -> sigue abierto", k == [] and len(I66.E["abiertas"]) == 1, k)
abre(); k = paso(560, obs((4, 1), [(4, (7, 1))]))
caso("4 llega con el activo a 3 en el mismo tic -> cuenta la llegada (acierto: botiquin a 1)", k == ["P7_66_llegada"] and IN.E["conf"]["recursos"] != 0.5, k)
print(f"\n{len(OK)} pasan, {len(MAL)} fallan" + (f": {MAL}" if MAL else ""))
json.dump({"pasan": OK, "fallan": MAL}, open(os.path.join(AQUI, "P7_67b_interrupcion_pruebas.json"), "w"), ensure_ascii=False, indent=1); sys.exit(1 if MAL else 0)
