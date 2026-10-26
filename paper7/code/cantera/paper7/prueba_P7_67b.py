"""[P7-67, banco con la pieza nueva] PRUEBAS A MANO de invita_P7_67b (decisiones de la mesa del 17-oct, 10:31). Sin plataforma, sin API.
  1. distancia solo al aceptar: sin aceptar, a 7 no empuja; aceptada y abierta, a 7, fuera del tramo de 300 tics o con la hermana a 6, sigue empujando; tras el juicio vuelve la regla.
  2. activa hasta el juicio: aceptada, la invitacion sigue activa sin calma (IN.cumple aplicado de verdad); sin aceptar, sin calma no.
  3. el candidato: aceptada y a 7 del destino, la lista del cuerpo sigue teniendo `ir_sitio` emparejado con su invitacion (D.candidatos aplicado de verdad).
  4. juicio: acierto con un botiquin a 3 del destino; fallo a 4 o sin botiquin; rival activo a 3 -> interrumpida; 480 tics -> no llego.  python3 prueba_P7_67b.py"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "cantera", "paper6"), RAIZ]
for k, v in (("GEMV_P7_54", "1"), ("GEMV_P7_66", "1"), ("GEMV_P7_67", "1"), ("GEMV_P7_67_ACTIVOS", "4"), ("GEMV_P7_67B", "1")): os.environ[k] = v
import invita_P7_54 as IN, invita_P7_66b as I66, invita_P7_67 as I67, invita_P7_67b as B
from alma import decisor_zs as D
OK = []; MAL = []
def caso(n, c, d=""): (OK if c else MAL).append(n); print(("PASA " if c else "FALLA") + " · " + n + (f" · {d}" if d else ""))
class Mundo:
    slot = 10; teammate_slot = 11; id_botiquin = "first_aid"
    def solido(self, x, y): return False
_orig = D.candidatos
D.candidatos = lambda obs_, mundo, mem, tick, bloqueos=None: [("noop", {"tipo": "noop"}), ("ir_pareja", {"tipo": "ir", "destino": (11, 11)})]
class Prueba:
    def decidir(self, obs_): return None, None
IN.aplica(Prueba, None); I66.aplica(Prueba, None); I67.aplica(Prueba, None); h = B.aplica(Prueba, None)
caso("0 aplicada encima de invita_P7_66b", I66.puede_empujar is B.puede_empujar and I66.juicio is B.juicio and h["juzga_a"] == 3, h)
INV = {"_k": 0, "accion": "IR_A_SITIO", "destino": [3, 1], "calma5": "CALMA5", "cuerpo": 0.0, "recursos": 1.0, "vinculo": 0.0, "falsa": True}
A = {"inv": INV, "t0": 300, "destino": (3, 1)}
I66.E["abiertas"] = []
caso("1a sin aceptar, en el tramo, a 12 de ella y 10 de su hermana -> empuja", I66.puede_empujar(INV, 341, 241, (13, 13), (13, 9), set()))
caso("1b sin aceptar, a 7 de ella -> no empuja (como en P7-66b)", not I66.puede_empujar(INV, 341, 241, (10, 5), (13, 13), set()))
I66.E["abiertas"] = [A]
caso("1c aceptada y abierta, a 7 de ella -> sigue empujando", I66.puede_empujar(INV, 341, 241, (10, 5), (13, 13), set()))
caso("1d aceptada y abierta, a 2 de ella y su hermana a 6 -> sigue empujando", I66.puede_empujar(INV, 341, 241, (5, 1), (9, 1), set()))
caso("1e aceptada y abierta, fuera del tramo de 300 tics -> sigue empujando", I66.puede_empujar(INV, 700, 241, (10, 5), None, set()))
I66.E["abiertas"] = []
caso("1f juzgada (ya no abierta), a 7 -> vuelve la regla: no empuja", not I66.puede_empujar(INV, 341, 241, (10, 5), (13, 13), set()))
base = {"anillo": "DENTRO", "calma": "CALMA", "movimiento": "MOVIENDOSE", "hermana": "LEJOS"}
I66.E.update({"tick": 341, "tic0": 241, "pos": (10, 5), "hermana": (13, 13), "llegados": set()})
caso("2a sin aceptar y sin calma -> no activa", IN.cumple(INV, dict(base, calma5="SIN_CALMA5")) is False)
I66.E["abiertas"] = [A]
caso("2b aceptada, sin calma y a 7 -> sigue activa hasta el juicio", IN.cumple(INV, dict(base, calma5="SIN_CALMA5")) is True)
IN.E["activas"] = [INV]
out = D.candidatos({"visible": {"agents": []}}, Mundo(), None, 341); i = len(out) - 1
caso("3a aceptada y a 7 del destino: el ultimo candidato es ir_sitio con su destino", out[-1][0] == "ir_sitio" and out[-1][1]["destino"] == (3, 1), out[-1])
caso("3b emparejado con su invitacion en la lista de invita_P7_54", IN.E["cands"][i] == "ir_sitio" and IN.E["match"].get(i) is INV)
I66.E["abiertas"] = []; out = D.candidatos({"visible": {"agents": []}}, Mundo(), None, 341)
caso("3c sin aceptar y a 7: no hay ir_sitio", all(n != "ir_sitio" for n, _ in out))
D.candidatos = _orig
caso("4a llega con un botiquin a 3 del destino -> acierto 1", B.juicio(A, 400, (4, 1), None, [(6, 3)]) == ("llegada", 1))
caso("4b llega con el botiquin mas cercano a 4 -> 0", B.juicio(A, 400, (4, 1), None, [(7, 1)]) == ("llegada", 0))
caso("4c llega sin botiquin -> 0", B.juicio(A, 400, (3, 2), None, []) == ("llegada", 0))
caso("4d a 2 casillas aun no ha llegado", B.juicio(A, 400, (5, 1), None, [(3, 1)]) is None)
caso("4e rival activo a 3 antes de llegar -> interrumpida", B.juicio(A, 400, (10, 5), 3, []) == ("interrumpida", None))
caso("4f 480 tics sin llegar -> no llego", B.juicio(A, 780, (10, 5), None, []) == ("no_llego", None))
print(f"\n{len(OK)} pasan, {len(MAL)} fallan" + (f": {MAL}" if MAL else ""))
json.dump({"pasan": OK, "fallan": MAL}, open(os.path.join(AQUI, "P7_67b_pruebas.json"), "w"), ensure_ascii=False, indent=1); sys.exit(1 if MAL else 0)
