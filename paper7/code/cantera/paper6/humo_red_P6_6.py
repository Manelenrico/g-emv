"""[P6-6] EL HUMO DE RED CON LOS DOS ARREGLOS. Antes de pagar nada.

Molde de `humo_red_P6_4.py`, con tres diferencias que importan:

  1. Aplica `arreglos_P6_6.aplica` (oido + don) como lo hara la politica.
  2. Los partes E2 del hermano NO se escriben a mano: los emite el EMISOR DE
     PRODUCCION (`parte2.emite`) sobre los tics grabados, y entran por el CABLE,
     en `chat`, que es la via real de lectura. (Regla nueva de Manel.)
  3. Comprueba lo que P6-5 descubrio que nadie comprobaba: que al final del
     bucle `alma.mem.parte` NO es None — es decir, que el cuerpo del cinco ha
     entendido de verdad el parte de su hermano por el cable.
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
sys.path.insert(0, RAIZ)
os.environ["GEMV_OJOS"] = os.environ.get("GEMV_OJOS", "1")
os.environ.setdefault("GEMV_CORTEX", "0")

import asyncio
from alma import policy_cortex as PC
from alma.mundo import Mundo
sys.path.insert(0, '/app'); sys.path.insert(0, '/app/alma')
import policy_pareja as PP
import parte2 as P2
import arreglos_P6_6 as R6

_CAND = [os.path.join(AQUI, "humo_200tics.json"),
         os.path.join(RAIZ, "paintball", "alma", "humo_200tics.json"),
         "/app/alma/humo_200tics.json"]
_G = next(x for x in _CAND if os.path.exists(x))
D = json.load(open(_G))


HERM = None          # se fija en cuanto se lee el player_config


def _obs(r):
    o = {"type": "observation", "tick": r["tick"], "phase": r.get("phase", "live")}
    o["you"] = {"pos": r.get("pos"), "hp": r.get("hp"),
                "hand": r.get("hand"), "body": r.get("body"),
                "pack": r.get("pack") or [], "effects": r.get("effects") or [],
                "move_ready_in": r.get("move_ready_in") or 0,
                "attack_ready_in": r.get("attack_ready_in") or 0,
                "action_result": r.get("action_result")}
    o["visible"] = {"agents": r.get("ve_agentes") or [],
                    "items": r.get("ve_items") or [],
                    "bushes": r.get("ve_bushes") or [],
                    "projectiles": r.get("ve_proyectiles") or []}
    o["zone"] = r.get("zona") or {}
    o["events"] = r.get("eventos") or []
    # SE QUITAN los mensajes del hermano que traia el grabado (eran E1, de la
    # serie del cinco). Si se dejaran, `mem.parte` podria venir de ELLOS y la
    # comprobacion del oido no probaria nada: seria el agujero de siempre.
    o["chat"] = [m for m in (r.get("chat") or []) if m.get("from") != HERM]
    o["social"] = r.get("social") or {}
    return o


pc = dict(D["player_config"]); pc["type"] = "player_config"
pc["arena"] = {"size": D["static_map"].get("size") or 48,
               "static_map": list(D["static_map"]["filas"]),
               "legend": dict(D["static_map"].get("legend") or {}),
               "pedestals": D["static_map"].get("pedestals") or []}
pc["items"] = list(D["catalogo"]["items"])
pc["stats"] = {"budget": 20, "min": 1, "max": 10, "default": [5, 5, 5, 5]}
HERM = pc.get("teammate_slot")
MUNDO = Mundo.desde_player_config(dict(pc))


class MemV:
    agresores = {}
    parte = None
    pareja_muerta = False

    def parte_fresco(self, _t):
        return None


# LOS PARTES DEL HERMANO, EMITIDOS POR EL EMISOR DE PRODUCCION sobre los tics
# grabados. Se cambia solo el numero de asiento del emisor (el grabado es de un
# asiento; el hermano es el otro). Ni un campo escrito a mano.
ticks = list(D["ticks"])
_oj = P2.Ojeador()
msgs = [json.dumps(pc)]
n_partes = 0
for r in ticks:
    o = _obs(r)
    t = r["tick"]
    if t % P2.CADA == 0:
        ob = {"you": dict(o["you"]), "visible": dict(o["visible"]), "chat": []}
        ob["you"]["stats"] = {"speed": 5, "intelligence": 5}
        texto = P2.emite(ob, t, MUNDO, MemV(), 120, _oj, None)
        texto = texto.replace(f"P{MUNDO.slot} ", f"P{HERM} ", 1)
        o["chat"] = list(o["chat"]) + [{"tick": t, "from": HERM,
                                        "channel": "team", "to": None,
                                        "text": texto}]
        n_partes += 1
    msgs.append(json.dumps(o))
msgs.append(json.dumps({"type": "final", "placement": 9, "kills": 0,
                        "score": 0.0, "reason": "humo",
                        "match_ticks": ticks[-1]["tick"]}))

enviados = []


class WS:
    def __aiter__(self):
        self._i = 0
        return self

    async def __anext__(self):
        if self._i >= len(msgs):
            raise StopAsyncIteration
        m = msgs[self._i]; self._i += 1
        return m

    async def send(self, s):
        enviados.append(json.loads(s))


alma = PP.AlmaPareja()
d0 = len(PC._DIARIO)
PP._envuelve(alma)
hecho = R6.aplica(PP.AlmaPareja, PC.log)          # los dos arreglos
alma.cf.arranca()
asyncio.run(PC.decisor(WS(), alma))
nuevas = PC._DIARIO[d0:]
claves, errores, ojos, dones = {}, [], {}, {}
for linea in nuevas:
    try:
        r = json.loads(linea)
    except Exception:
        continue
    k = r.get("k")
    claves[k] = claves.get(k, 0) + 1
    if k == "ojos":
        ojos[r.get("estado")] = ojos.get(r.get("estado"), 0) + 1
    if k == "don":
        dones[r.get("estado")] = dones.get(r.get("estado"), 0) + 1
    if k and "error" in k:
        errores.append(r)

acciones = [e for e in enviados if e.get("type") == "action"]
charlas = [e for e in enviados if e.get("type") == "talk"]
n_obs = len(ticks)
print(f"arreglos          : {hecho}")
print(f"partes E2 metidos : {n_partes} (del emisor de produccion, por el cable)")
print(f"acciones emitidas : {len(acciones)} de {n_obs} observaciones")
print(f"mensajes de canal : {len(charlas)}")
print(f"registros ojos    : {ojos}")
print(f"registros don     : {dones}")
print(f"errores           : {len(errores)}")
for e in errores[:3]:
    print("   ", json.dumps(e, ensure_ascii=False)[:400])
print(f"claves            : {json.dumps({k: v for k, v in sorted(claves.items())}, ensure_ascii=False)}")
print(f"mem.parte         : {alma.mem.parte}")

assert hecho["oido"] and hecho["don"], hecho
assert len(acciones) == n_obs, \
    ("UNA EMISION POR OBSERVACION: el bucle se cayo", len(acciones), n_obs)
assert not errores, ("hubo errores en el bucle", errores[:2])
assert charlas, "no salio ni un mensaje por el canal team"
e2 = [t for t in charlas if (t.get("text") or "").startswith("E2 ")]
assert e2, ("el canal team no llevo E2", charlas[:2])
assert all(len(t["text"]) <= 120 for t in e2), "un E2 paso de 120"
assert ojos.get("inyectado"), "no se inyecto nada pese a llegar partes E2"
# EL QUE FALTABA: el cuerpo del cinco ha entendido el parte por el CABLE
# guarda explicita: en lo que se manda por el cable no va ni un E1 del hermano
for i, r in enumerate(ticks):
    for m in json.loads(msgs[1 + i]).get("chat") or []:
        assert not (m.get("from") == HERM
                    and (m.get("text") or "").startswith("E1 ")), \
            ("se colo un E1 del hermano: la prueba del oido seria vacia", m)
assert alma.mem.parte is not None, \
    "EL OIDO NO FUNCIONA POR EL CABLE: mem.parte sigue en None"
assert alma.mem.parte["slot"] == HERM, alma.mem.parte
# y no hay recuperacion del propio regalo
seq = [(e.get("do"), tuple(e.get("pos") or ())) for e in acciones]
print(f"\nOK · {len(e2)} partes E2 (max {max(len(t['text']) for t in e2)} car) · "
      f"inyecciones {ojos.get('inyectado')} · vetados {ojos.get('vetados', 0)} · "
      f"mem.parte t={alma.mem.parte['t']} hp={alma.mem.parte['hp']:g} "
      f"b={alma.mem.parte['botiquin']}")
