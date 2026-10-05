"""[P6-8 · B, version b] DOS ARREGLOS DE METODO, DESDE FUERA — CORREGIDA TRAS LA SERIE.

LA VERSION JUGADA (`arreglos_P6_8.py`, md5 f66355ca12b58b075d12f0e7f7ee39d0)
CREABA `ir_pareja` tambien en los tics de ENFRIAMIENTO de las piernas, cuando el
decisor lo habia vetado (`Bloqueos.veta`, decisor_zs.py:95-102): en esos tics
ganaba a `noop` y emitia un `move` que el mundo rechazaba con `cooldown`. Para
el movimiento es inocuo (no se podia mover), pero infla la estadistica de
"ir_pareja elegido" (6.333 creaciones en un solo diario) y no es lo que la
regla decia. Aqui solo se toca `ir_pareja` si el decisor lo ha propuesto (ya
vetado o no), y solo se CREA si las piernas estan listas (`move_ready_in == 0`).
NO se ha jugado con esta version; queda para la siguiente serie.

No toca `model.py`, ni el cinco, ni `policy_pareja.py`, ni `arreglos_P6_6.py`.
Se aplica DESPUES de `arreglos_P6_6.aplica` (el oido y el don), envolviendo
`D.candidatos` una vez mas. Ni una fila nueva: solo cambia QUE candidatos se
proponen y ADONDE apunta uno de ellos.

─── 1 · `ir_pareja` APUNTA AL PARTE cuando no ve al hermano ────────────────
Medido en P6-7: `mem.pareja_pos` solo se escribe al VER al hermano
(`appraisal_zs_v42_exp.py:624`), y `ir_pareja` apunta ahi (`decisor_zs.py:471`).
Con el hermano fuera de la vista (31,1 % de los tics de A1) ese destino esta a
mas de 3 casillas de donde el parte dice que esta el 41,6 % de las veces (p90
13, maximo 31). El parte FRESCO trae su casilla exacta (`mem.parte_fresco`).

REGLA: si el hermano NO esta en `visible.agents` y `mem.parte_fresco(tick)` da
posicion, `ir_pareja` apunta a esa posicion. Si no habia `ir_pareja` (nunca lo
vio), se crea con la misma receta que el decisor (`{"tipo": "ir", "destino",
"cuerpos"}`; `cuerpos` = casillas ocupadas por lo visible, como en `:446`). Si
lo ve, no se toca nada.

─── 2 · NO PROPONE `coger` CON LA MOCHILA LLENA ─────────────────────────────
Medido en P6-7: 18.566 tics (4,44 %) en A1 eligiendo `coger` con el mundo
respondiendo `inventory_full`, racha peor 3.676 tics. La CAUSA esta en el
decisor: `_pack_con` ya sabe que con el zurron lleno "coger no cambia nada"
(`decisor_zs.py:384`), asi que la prevision de `coger` es IGUAL a la de `noop`,
y el desempate del cinco excluye a `noop` (`select_tiebreak(...,
exclude_noop=True)`, `:896`): en un empate, `coger` gana siempre.

REGLA, leida del mundo y de nada mas: se esconde `coger` si
  (a) la prevision del propio decisor no cambia la mochila
      (`D._pack_con(pack, id, n, mundo) == pack`), o
  (b) el ultimo `action_result` que dio el mundo fue `inventory_full` y sigo
      en la misma casilla con el mismo objeto debajo.
Ninguna capacidad cableada: la mochila es la lista `you.pack` tal cual la
manda el mundo, con sus huecos (`None`) y sus pilas.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from alma import decisor_zs as D                          # noqa: E402

PAREJA_ON = (os.environ.get("GEMV_PAREJA_PARTE", "1") or "1") not in ("0", "", "no")
LLENA_ON = (os.environ.get("GEMV_MOCHILA_LLENA", "1") or "1") not in ("0", "", "no")


def entorno():
    return {"crudo": {"GEMV_PAREJA_PARTE": os.environ.get("GEMV_PAREJA_PARTE"),
                      "GEMV_MOCHILA_LLENA": os.environ.get("GEMV_MOCHILA_LLENA")},
            "efectivo": {"PAREJA_PARTE": PAREJA_ON, "MOCHILA_LLENA": LLENA_ON}}


def destino_parte(obs, mundo, mem, tick):
    """La casilla del hermano segun el parte FRESCO, si NO lo veo; si no, None."""
    herm = getattr(mundo, "teammate_slot", None)
    vis = obs.get("visible") or {}
    if any(a.get("slot") == herm for a in (vis.get("agents") or [])):
        return None
    if getattr(mem, "pareja_muerta", False):
        return None
    pf = getattr(mem, "parte_fresco", None)
    p = pf(tick) if callable(pf) else None
    if not p or not p.get("pos"):
        return None
    q = (int(p["pos"][0]), int(p["pos"][1]))
    pos = tuple((obs.get("you") or {}).get("pos") or ())
    return None if q == pos else q


def mochila_llena(obs, mundo, mem, receta):
    """¿`coger` esta receta no cambiaria nada, o el mundo ya dijo que no cabe?"""
    you = obs.get("you") or {}
    it = receta.get("item") or {}
    pack = list(you.get("pack") or [])
    if D._pack_con(pack, it.get("id"), int(it.get("n") or 1), mundo) == pack:
        return "prevision: la mochila no cambia"
    pos = tuple(you.get("pos") or ())
    ult = getattr(mem, "_lleno8", None)
    if you.get("action_result") == "inventory_full":
        try:
            mem._lleno8 = (pos, it.get("id"))
        except Exception:
            pass
        return "el mundo dijo inventory_full"
    if ult and ult == (pos, it.get("id")):
        return "inventory_full en esta casilla con este objeto"
    return None


def aplica(registra=None):
    hecho = {"pareja_parte": PAREJA_ON, "mochila_llena": LLENA_ON}
    _orig = D.candidatos

    def _cands(obs, mundo, mem, tick, bloqueos=None):
        cs = list(_orig(obs, mundo, mem, tick, bloqueos))
        # limpia la marca de "lleno" si me he movido o la mochila cambio
        ult = getattr(mem, "_lleno8", None)
        if ult and tuple((obs.get("you") or {}).get("pos") or ()) != ult[0]:
            try:
                mem._lleno8 = None
            except Exception:
                pass
        if PAREJA_ON:
            q = destino_parte(obs, mundo, mem, tick)
            if q is not None:
                idx = next((i for i, (n, _r) in enumerate(cs) if n == "ir_pareja"), None)
                if idx is not None:
                    r = dict(cs[idx][1]); antes = r.get("destino"); r["destino"] = q
                    cs[idx] = ("ir_pareja", r)
                    if registra is not None and antes != q:
                        registra({"k": "pareja8", "tick": tick, "estado": "destino_del_parte",
                                  "antes": list(antes) if antes else None, "ahora": list(q)})
                elif int((obs.get("you") or {}).get("move_ready_in") or 0) == 0:
                    vis = obs.get("visible") or {}
                    cuerpos = frozenset(tuple(a.get("pos") or ()) for a in (vis.get("agents") or []) if a.get("pos"))
                    cs.append(("ir_pareja", {"tipo": "ir", "destino": q, "cuerpos": cuerpos}))
                    if registra is not None:
                        registra({"k": "pareja8", "tick": tick, "estado": "ir_pareja_creado", "ahora": list(q)})
        if LLENA_ON:
            fuera = [(n, mochila_llena(obs, mundo, mem, r)) for n, r in cs if r.get("tipo") == "coger"]
            fuera = [(n, m) for n, m in fuera if m]
            if fuera:
                cs = [(n, r) for n, r in cs if n not in {x for x, _ in fuera}]
                if registra is not None:
                    registra({"k": "llena8", "tick": tick, "estado": "coger_escondido", "motivo": fuera[0][1]})
        return cs
    D.candidatos = _cands
    return hecho
