"""[P7-67] PRUEBAS A MANO de invita_P7_67 (antes del banco). Sin plataforma, sin API. Activo = asiento 4; pasivas = el resto que no son 10 ni 11.
  1. calma: activo a 6 -> calma; activo a 5 -> no; pasiva a 1 -> calma (la regla la ignora); la hermana a 1 no cuenta; golpe hace 40 tics -> no.
  2. interrupcion: con el rival de lee_obs, una pasiva a 2 no interrumpe; el activo a 3 si.
  3. enganche: tras aplica, invita_P7_66b.lee_obs es el de P7-67; sin asientos activos, aplica se niega.  python3 prueba_P7_67.py"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "cantera", "paper6"), RAIZ]
for k, v in (("GEMV_P7_54", "1"), ("GEMV_P7_66", "1"), ("GEMV_P7_67", "1"), ("GEMV_P7_67_ACTIVOS", "4")): os.environ[k] = v
import invita_P7_66b as I66, invita_P7_67 as J, nace_P7_23 as N
OK = []; MAL = []
def caso(nombre, cond, detalle=""):
    (OK if cond else MAL).append(nombre); print(("PASA " if cond else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))
class Mundo:
    slot = 10; teammate_slot = 11; id_botiquin = "first_aid"
def obs(pos, agentes): return {"you": {"pos": list(pos)}, "visible": {"agents": [{"slot": s, "pos": list(p)} for s, p in agentes], "items": []}}
N.E["ultimo_dano"] = None
_, r, _, c = J.lee_obs(obs((10, 10), [(4, (16, 10))]), Mundo(), 500, None); caso("1a activo a 6 -> calma", c is True and r == 6)
_, r, _, c = J.lee_obs(obs((10, 10), [(4, (15, 10))]), Mundo(), 500, None); caso("1b activo a 5 -> no hay calma", c is False and r == 5)
_, r, _, c = J.lee_obs(obs((10, 10), [(7, (11, 10)), (0, (10, 11))]), Mundo(), 500, None); caso("1c dos pasivas a 1 -> calma (la regla las ignora)", c is True and r is None)
_, r, _, c = J.lee_obs(obs((10, 10), [(11, (11, 10))]), Mundo(), 500, None); caso("1d la hermana a 1 no cuenta", c is True and r is None)
_, r, _, c = J.lee_obs(obs((10, 10), [(7, (11, 10)), (4, (18, 10))]), Mundo(), 500, None); caso("1e pasiva a 1 y activo a 8: el rival es el activo", c is True and r == 8)
N.E["ultimo_dano"] = 460; _, r, _, c = J.lee_obs(obs((10, 10), []), Mundo(), 500, None); caso("1f golpe hace 40 tics -> no hay calma", c is False); N.E["ultimo_dano"] = None
a = {"inv": {"_k": 0}, "t0": 400, "destino": (3, 10)}
_, r, k, _ = J.lee_obs(obs((10, 10), [(5, (12, 10))]), Mundo(), 500, None); caso("2a pasiva a 2 no interrumpe", I66.juicio(a, 500, (10, 10), r, k) is None)
_, r, k, _ = J.lee_obs(obs((10, 10), [(4, (13, 10))]), Mundo(), 500, None); caso("2b activo a 3 interrumpe", I66.juicio(a, 500, (10, 10), r, k) == ("interrumpida", None))
h = J.aplica(None, None); caso("3a tras aplica, invita_P7_66b usa el lee_obs de P7-67", I66.lee_obs is J.lee_obs and h["activos"] == [4], h)
J.ACTIVOS = frozenset()
try: J.aplica(None, None); caso("3b sin asientos activos, aplica se niega", False)
except AssertionError: caso("3b sin asientos activos, aplica se niega", True)
print(f"\n{len(OK)} pasan, {len(MAL)} fallan" + (f": {MAL}" if MAL else ""))
json.dump({"pasan": OK, "fallan": MAL}, open(os.path.join(AQUI, "P7_67_pruebas.json"), "w"), ensure_ascii=False, indent=1)
sys.exit(1 if MAL else 0)
