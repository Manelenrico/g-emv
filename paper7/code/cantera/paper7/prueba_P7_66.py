"""[P7-66] PRUEBAS A MANO de invita_P7_66 (antes del banco). Sin plataforma, sin API.
  1. juicio: llega con botiquin -> acierto 1; llega sin botiquin -> 0 (la mentira falla en el acto); rival a <= 5 antes de llegar -> interrumpida; 480 tics sin llegar -> no_llego;
     llegar gana a la interrupcion en el mismo tic; a 2 casillas aun no ha llegado.
  2. calma: rival a 6 -> calma; a 5 -> no; golpe hace 40 tics -> no; la hermana a 1 casilla no cuenta. La invitacion con calma5 solo se activa en calma (IN.cumple aplicado de verdad).
  3. candidato: con la invitacion activa, la lista del cuerpo gana `ir_sitio` (receta «ir» con su destino) y queda emparejado con la invitacion en E["match"] de invita_P7_54, al final;
     sin invitacion activa, o ya a <= 1 casilla, no se anade.
  4. solo recursos: la regla de la confianza que aplica la pieza toca solo recursos.  python3 prueba_P7_66.py"""
import inspect, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "cantera", "paper6"), RAIZ]
for k in ("GEMV_P7_54", "GEMV_P7_66"): os.environ[k] = "1"
import invita_P7_54 as IN, invita_P7_66 as J, nace_P7_23 as N
from alma import decisor_zs as D
OK = []; MAL = []
def caso(nombre, cond, detalle=""):
    (OK if cond else MAL).append(nombre); print(("PASA " if cond else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))
INV = {"_k": 0, "accion": "IR_A_SITIO", "destino": [8, 24], "calma5": "CALMA5", "cuerpo": 0.0, "recursos": 1.0, "vinculo": 0.0, "falsa": True}
a = {"inv": INV, "t0": 1000, "destino": (8, 24)}
caso("1a llega (a 1 casilla) y hay un botiquin junto al destino -> acierto 1", J.juicio(a, 1100, (9, 24), None, [(8, 25)]) == ("llegada", 1))
caso("1b llega y no hay botiquin -> 0 (falla en el acto)", J.juicio(a, 1100, (8, 24), None, [(20, 20)]) == ("llegada", 0))
caso("1c rival a 5 antes de llegar -> interrumpida", J.juicio(a, 1100, (15, 24), 5, []) == ("interrumpida", None))
caso("1d rival a 6 -> sigue abierta", J.juicio(a, 1100, (15, 24), 6, []) is None)
caso("1e 480 tics sin llegar ni rival -> no_llego", J.juicio(a, 1480, (15, 24), None, []) == ("no_llego", None))
caso("1f a 2 casillas aun no ha llegado", J.juicio(a, 1100, (10, 24), None, [(8, 24)]) is None)
caso("1g llega con un rival a 3: cuenta la llegada (el juicio de llegar va primero)", J.juicio(a, 1100, (8, 25), 3, []) == ("llegada", 0))
class Mundo:
    slot = 10; teammate_slot = 11; id_botiquin = "first_aid"
    def solido(self, x, y): return False
def obs(pos, agentes, items=()): return {"you": {"pos": list(pos)}, "visible": {"agents": [{"slot": s, "pos": list(p)} for s, p in agentes], "items": [{"id": i, "pos": list(p)} for i, p in items]}}
N.E["ultimo_dano"] = None
_, r, k, c = J.lee_obs(obs((10, 10), [(3, (16, 10))], [("first_aid", (12, 12))]), Mundo(), 500, None); caso("2a rival a 6 -> calma; botiquin leido", c is True and r == 6 and k == [(12, 12)])
_, r, k, c = J.lee_obs(obs((10, 10), [(3, (15, 10))]), Mundo(), 500, None); caso("2b rival a 5 -> no hay calma", c is False)
_, r, k, c = J.lee_obs(obs((10, 10), [(11, (11, 10))]), Mundo(), 500, None); caso("2c la hermana a 1 casilla no cuenta como rival", c is True and r is None)
N.E["ultimo_dano"] = 460; _, r, k, c = J.lee_obs(obs((10, 10), []), Mundo(), 500, None); caso("2d golpe hace 40 tics -> no hay calma", c is False)
N.E["ultimo_dano"] = 440; _, r, k, c = J.lee_obs(obs((10, 10), []), Mundo(), 500, None); caso("2e golpe hace 60 tics -> calma", c is True)
# las piezas aplicadas de verdad sobre una clase de prueba, con una lista de candidatos de juguete
_orig = D.candidatos
D.candidatos = lambda obs_, mundo, mem, tick, bloqueos=None: [("noop", {"tipo": "noop"}), ("ir_pareja", {"tipo": "ir", "destino": (11, 11)})]
class Prueba:
    def decidir(self, obs_): return None, None
IN.aplica(Prueba, None); J.aplica(Prueba, None)
base = {"anillo": "DENTRO", "calma": "CALMA", "movimiento": "MOVIENDOSE", "hermana": "LEJOS"}
caso("2f la invitacion se activa en calma", IN.cumple(INV, dict(base, calma5="CALMA5")) is True)
caso("2g y no se activa sin calma", IN.cumple(INV, dict(base, calma5="SIN_CALMA5")) is False)
IN.E["activas"] = [INV]; J.E["pos"] = (20, 20)
out = D.candidatos({"visible": {"agents": []}}, Mundo(), None, 500)
ult = out[-1]; i = len(out) - 1
caso("3a con la invitacion activa: el ultimo candidato es ir_sitio, receta «ir» con su destino", ult[0] == "ir_sitio" and ult[1]["tipo"] == "ir" and ult[1]["destino"] == (8, 24), ult)
caso("3b emparejado con su invitacion en la lista de invita_P7_54 (mismo indice)", IN.E["cands"][i] == "ir_sitio" and IN.E["match"].get(i) is INV and len(IN.E["cands"]) == len(out))
IN.E["activas"] = []; out = D.candidatos({"visible": {"agents": []}}, Mundo(), None, 500)
caso("3c sin invitacion activa no hay ir_sitio", all(n != "ir_sitio" for n, _ in out))
IN.E["activas"] = [INV]; J.E["pos"] = (9, 24); out = D.candidatos({"visible": {"agents": []}}, Mundo(), None, 500)
caso("3d ya a <= 1 casilla del destino: no se anade", all(n != "ir_sitio" for n, _ in out))
D.candidatos = _orig
src = inspect.getsource(J.aplica)
caso("4a la regla de confianza de la pieza solo toca recursos", 'IN.E["conf"]["recursos"] = (1 - IN.ETA) * IN.E["conf"]["recursos"] + IN.ETA * ac' in src and 'IN.E["conf"]["cuerpo"]' not in src and 'IN.E["conf"]["vinculo"]' not in src)
caso("4b la sombra no la juzga invita_P7_54 (objeto que no existe, t0 en el futuro) ni la mueve juicio_P7_62", J.sombra(a)["objeto"] == "__invita_P7_66__" and J.sombra(a)["t0"] > 10 ** 8)
print(f"\n{len(OK)} pasan, {len(MAL)} fallan" + (f": {MAL}" if MAL else ""))
json.dump({"pasan": OK, "fallan": MAL}, open(os.path.join(AQUI, "P7_66_pruebas.json"), "w"), ensure_ascii=False, indent=1)
sys.exit(1 if MAL else 0)
