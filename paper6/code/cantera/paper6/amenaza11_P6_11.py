"""[P6-11] EL RIVAL SIN ARMA COMO AMENAZA MENOR, desde fuera. ARCHIVO NUEVO.

DECISION DE MANEL: un rival sin arma ES una amenaza, pero menor, en proporcion
al dano que hace de verdad; y si te esta pegando, es amenaza plena, tenga arma
o no. Sin filas nuevas.

LO MEDIDO (`mide_dano_P6_11.py`, 987 golpes de rival en A0+A1+A2+A3): con la
mano vacia, **405 golpes, mediana 3,0** (256 de 3,0 y 95 de 4,5: el punetazo del
mundo, base 3 escalada por fuerza); espada 16,2 (catalogo 18), lanza 10,8 (12),
cuchillos 8, arco 14, cerbatana 4. El punetazo es 3/18 = un sexto de la espada.

DONDE DECIDE EL CUERPO QUE ES AMENAZA, y que ve cada sitio (appraisal_zs_v42_exp):
  · S-7-AGRESOR (:638-656): por `damage_taken.source`. NO mira el arma: el que
    me pega ya es amenaza plena. No se toca.
  · F-4-ALCANCE (:1049-1063): todo hostil por su distancia. NO mira el arma.
  · S-8-EXPOSICION (:1391-1416): todo hostil que me ve. NO mira el arma.
  · F-HERMANO-AMENAZA / F-HERMANO-GOLPE (:1584-1591): `E = mundo.items[hand].
    damage`; `if E <= 0: continue  # sin arma no hay amenaza`. AQUI esta la
    ceguera: un rival de mano vacia junto al hermano no enciende nada, ni
    cuando le pega.
  · F-REENCUENTRO (:898-901): `_arma is None or damage <= 0 -> continue`.
    Segunda ceguera: el que me pego con la mano vacia y vuelve no cuenta.
  · La amenaza de S-COMPANIA (filas10) es el max de F-4, S-7, F-HERMANO-*: hereda.
  Todas leen la mano del hostil con `mundo.items.get(hand)`. Ese es el asidero.

QUE SE TOCA (dos cosas, ninguna en el cinco):
  1. `mundo.items` pasa a ser un dict-hijo que responde a DOS ids que no estan
     en el catalogo, sin cambiar su iteracion (el alfabeto del E2 y `dmg_ref`
     no cambian):
       "~manos"          Item(damage=3,  range=1, kind=ikMelee)  el punetazo
       "~manos_pegando"  Item(damage=dmg_ref, range=1, ikMelee)  amenaza plena
  2. En la obs que ve el decisor (una COPIA: la obs cruda que emite el parte y
     se guarda en el diario no se toca), a cada hostil visible o contado con la
     mano vacia se le pone "~manos"; si ese asiento me esta pegando (esta en
     `mem.agresores` dentro de la ventana S-7) o es el agresor que declara el
     parte fresco del hermano, "~manos_pegando".
  Se envuelven `D.candidatos` y `D.decide` para que los dos vean la misma copia.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from alma import appraisal_zs_v42_exp as A                 # noqa: E402
from alma import decisor_zs as D                          # noqa: E402
from alma.mundo import Item                               # noqa: E402

MANOS, PEGANDO = "~manos", "~manos_pegando"
DANO_MANOS = int(os.environ.get("GEMV_MANOS_DANO", "3") or 3)   # medido: mediana 3,0
ON = (os.environ.get("GEMV_MANOS", "1") or "1") not in ("0", "", "no")


def entorno():
    return {"efectivo": {"MANOS": ON, "DANO_MANOS": DANO_MANOS}}


class ItemsConManos(dict):
    """`mundo.items` + dos ids virtuales. Iterar/len/keys: como el catalogo."""

    def __init__(self, base, dmg_ref):
        super().__init__(base)
        self._v = {MANOS: Item(id=MANOS, kind="ikMelee", damage=DANO_MANOS, range=1, cooldown=0,
                               durability=0, stack_max=1, use_ticks=0, heal=0),
                   PEGANDO: Item(id=PEGANDO, kind="ikMelee", damage=int(dmg_ref), range=1, cooldown=0,
                                 durability=0, stack_max=1, use_ticks=0, heal=0)}

    def get(self, k, default=None):
        if k in self._v:
            return self._v[k]
        return super().get(k, default)

    def __getitem__(self, k):
        if k in self._v:
            return self._v[k]
        return super().__getitem__(k)

    def __contains__(self, k):
        return k in self._v or super().__contains__(k)


def instala(mundo):
    if not isinstance(mundo.items, ItemsConManos):
        mundo.items = ItemsConManos(mundo.items, mundo.dmg_ref)
    return mundo


def pegando(mem, mundo, tick, slot):
    e = (getattr(mem, "agresores", None) or {}).get(slot)
    if e and (tick - e["ultimo"]) <= A.AGRESOR_VENTANA_S * mundo.tick_rate:
        return True
    pf = getattr(mem, "parte_fresco", None)
    p = pf(tick) if callable(pf) else None
    return bool(p and p.get("agresor") and p.get("agresor_slot") == slot)


def reescribe(obs, mundo, mem, tick):
    """Una obs NUEVA con la mano de los hostiles sin arma reescrita. No muta."""
    vis = obs.get("visible") or {}
    ags = vis.get("agents") or []
    nuevos, n = [], 0
    for a in ags:
        sl = a.get("slot")
        h = a.get("hand")
        hid = h if isinstance(h, str) else (h or {}).get("id")
        if sl in (mundo.slot, mundo.teammate_slot) or (hid and hid != "none" and hid in mundo.items):
            nuevos.append(a)
            continue
        b = dict(a)
        b["hand"] = PEGANDO if pegando(mem, mundo, tick, sl) else MANOS
        nuevos.append(b); n += 1
    if not n:
        return obs, 0
    o2 = dict(obs); v2 = dict(vis); v2["agents"] = nuevos; o2["visible"] = v2
    return o2, n


def aplica(registra=None):
    if not ON:
        return {"manos": False}
    _oc, _od = D.candidatos, D.decide

    def _cands(obs, mundo, mem, tick, bloqueos=None):
        instala(mundo)
        o2, n = reescribe(obs, mundo, mem, tick)
        return _oc(o2, mundo, mem, tick, bloqueos)

    def _decide(obs, mundo, mem, tick, bloqueos=None):
        instala(mundo)
        o2, n = reescribe(obs, mundo, mem, tick)
        if n and registra is not None:
            registra({"k": "manos11", "tick": tick, "sin_arma": n,
                      "pegando": sum(1 for a in o2["visible"]["agents"] if a.get("hand") == PEGANDO)})
        return _od(o2, mundo, mem, tick, bloqueos)
    D.candidatos, D.decide = _cands, _decide
    return {"manos": True, "dano_manos": DANO_MANOS}
