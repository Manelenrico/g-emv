"""[P6-4] EL HUMO QUE FALTABA: el bucle de red entero CON LOS OJOS ENCENDIDOS.

P6-3 probo once cosas del mensaje y del oyente por separado, y ninguna probo
`run()` de punta a punta con `GEMV_OJOS=1`. Por eso la tanda 2 de P6-4 se
gasto diez partidas en las que la criatura murio enseguida y la plataforma no
produjo ni un diario. Esto es lo que habria que haber corrido ANTES.

Copia del molde de `humo_forma.py:600` (humo `i`), con la politica de la
pareja en vez de la de formas.
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
sys.path.insert(0, '/app'); sys.path.insert(0, '/app/alma')
import policy_pareja as PP
import parte2 as P2

# el grabado de 200 tics: al lado de este archivo dentro de la imagen
# (/app/alma/), y en paintball/alma/ fuera de ella.
_CAND = [os.path.join(AQUI, "humo_200tics.json"),
         os.path.join(RAIZ, "paintball", "alma", "humo_200tics.json"),
         "/app/alma/humo_200tics.json"]
_G = next(x for x in _CAND if os.path.exists(x))
D = json.load(open(_G))


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
    o["chat"] = r.get("chat") or []
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
# UN PARTE E2 DEL HERMANO EN CADA TIC: es lo que la tanda 2 tenia de verdad y
# los humos de P6-3 nunca metieron por el CABLE.
ticks = list(D["ticks"])
for r in ticks:
    r = r
msgs = [json.dumps(pc)]
for r in ticks:
    o = _obs(r)
    t = r["tick"]
    if t % P2.CADA == 0:
        riv = [x for x in (r.get("ve_agentes") or [])
               if x.get("slot") not in (pc["slot"], HERM) and x.get("pos")][:3]
        cola = ""
        if riv:
            cola = " R" + "".join(
                f"{x['slot']}:{int(x['pos'][0])},{int(x['pos'][1])}-." for x in riv)
        o["chat"] = list(o["chat"]) + [{
            "tick": t, "from": HERM, "channel": "team", "to": None,
            "text": f"E2 P{HERM} t{t} 24,24 h100 v0 b0 a0{cola}"}]
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
alma.cf.arranca()
asyncio.run(PC.decisor(WS(), alma))
nuevas = PC._DIARIO[d0:]
claves, errores, ojos = {}, [], {}
for linea in nuevas:
    try:
        r = json.loads(linea)
    except Exception:
        continue
    k = r.get("k")
    claves[k] = claves.get(k, 0) + 1
    if k == "ojos":
        ojos[r.get("estado")] = ojos.get(r.get("estado"), 0) + 1
    if k and "error" in k:
        errores.append(r)

acciones = [e for e in enviados if e.get("type") == "action"]
charlas = [e for e in enviados if e.get("type") == "talk"]
n_obs = len(ticks)
print(f"acciones emitidas : {len(acciones)} de {n_obs} observaciones")
print(f"mensajes de canal : {len(charlas)}")
print(f"registros ojos    : {ojos}")
print(f"errores           : {len(errores)}")
for e in errores[:3]:
    print("   ", json.dumps(e, ensure_ascii=False)[:400])
print(f"claves            : {json.dumps({k: v for k, v in sorted(claves.items())}, ensure_ascii=False)}")

assert len(acciones) == n_obs, \
    ("UNA EMISION POR OBSERVACION: el bucle se cayo", len(acciones), n_obs)
assert not errores, ("hubo errores en el bucle", errores[:2])
assert charlas, "no salio ni un mensaje por el canal team"
e2 = [t for t in charlas if (t.get("text") or "").startswith("E2 ")]
assert e2, ("el canal team no llevo E2", charlas[:2])
assert all(len(t["text"]) <= 120 for t in e2), "un E2 paso de 120"
assert ojos.get("inyectado"), "no se inyecto nada pese a llegar partes E2"
print(f"\nOK · {len(e2)} partes E2, el mas largo {max(len(t['text']) for t in e2)} car · "
      f"inyecciones {ojos.get('inyectado')} · vetados {ojos.get('vetados', 0)}")
