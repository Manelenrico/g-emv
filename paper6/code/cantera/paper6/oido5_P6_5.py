"""[P6-5 · 5c] EL OIDO DEL CINCO — devolverle el parte que dejo de entender.

ARCHIVO NUEVO. No toca `model.py`, ni el paper cinco, ni `policy_pareja.py`.
NO esta enganchado a nada: es el remiendo listo, para que lo decida Manel.

EL FALLO (medido en P6-5, `mide_sordera_P6_5.py`). El cuerpo del cinco lee el
parte del hermano en UN solo sitio y con un parser ESTRICTO de marca:

    appraisal_zs_v42_exp.py:578     p = PARTE.parsea(m.get("text") or "")
    parte.py:48                     r"^E1 P(\\d+) t(\\d+) ..."

`policy_pareja` cambio la emision a E2. `AlmaPareja._oye_e2` parsea el E2 para
lo suyo (inyectar rivales y recursos), pero nadie devuelve la CABEZA al sitio
donde el cinco la busca. En el brazo A1 de P6-4 llegaron 18.315 partes del
hermano y el cinco no entendio NI UNO.

EL REMIENDO, y por que asi. No se escribe en `mem.parte` a mano: eso volveria a
ser mi forma, no la del mundo (el fallo de P6-4 con `hand`). Lo que se hace es
poner en el chat un MENSAJE GEMELO con la cabeza traducida a E1, al lado del E2,
con el mismo `from`, `channel` y `tick`. Asi el parte entra por la misma puerta
de siempre (`Memoria.observa`) y hace todo lo que hacia en el cinco: fija
`mem.parte`, estima el hp, certifica el agresor. Cero codigo nuevo en la ruta de
decision.

La traduccion es la cabeza tal cual con la marca cambiada, y se VALIDA con el
parser del cinco: si `PARTE.parsea` no la acepta, se devuelve None y no se
inyecta nada. El parser es el juez, no yo.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from alma import parte as PARTE          # noqa: E402  el parser del cinco

MARCA_E1 = PARTE.MARCA                   # leida, no cableada


def a_E1(texto: str):
    """La cabeza de un E2 como linea E1, o None si el parser del cinco no la da.

    Los bloques de los ojos (` R...`, ` I...`) se cortan: ningun campo de la
    cabeza empieza por R ni por I (marca, P<slot>, t<tick>, x,y, h, v, b, a,
    s<slot>, ax,ay), asi que el corte es exacto y no hace falta otra regla.
    """
    if not isinstance(texto, str) or not texto:
        return None
    trozos = texto.split(" ")
    cabeza = []
    for z in trozos:
        if z[:1] in ("R", "I"):
            break
        cabeza.append(z)
    if not cabeza:
        return None
    cabeza[0] = MARCA_E1                 # E2 -> E1; lo demas, palabra por palabra
    linea = " ".join(cabeza)
    return linea if PARTE.parsea(linea) is not None else None


def gemelo(obs: dict, herm_slot):
    """`obs` con un mensaje E1 GEMELO por cada E2 del hermano. No muta la obs.

    Devuelve (obs2, n_gemelos). Si no hay nada que traducir, devuelve la misma
    obs y 0 — sin copiar nada, para no cambiar la conducta cuando no toca.
    """
    chat = obs.get("chat") or []
    nuevos = []
    for m in chat:
        if m.get("channel") != "team" or m.get("from") != herm_slot:
            continue
        linea = a_E1(m.get("text") or "")
        if linea is None or linea == (m.get("text") or ""):
            continue
        g = dict(m)
        g["text"] = linea
        g["_gemelo_de_E2"] = True
        nuevos.append(g)
    if not nuevos:
        return obs, 0
    obs2 = dict(obs)
    obs2["chat"] = list(chat) + nuevos
    return obs2, len(nuevos)


def remienda(clase, registra=None):
    """Envuelve `clase.decidir` para meter el gemelo antes de decidir.

    `registra(dict)` es opcional (el `log` de la politica). Devuelve la funcion
    original, para poder deshacerlo.
    """
    orig = clase.decidir

    def decidir(self, obs):
        herm = getattr(getattr(self, "mundo", None), "teammate_slot", None)
        if herm is not None:
            obs, n = gemelo(obs, herm)
            if n and registra is not None:
                registra({"k": "oido5", "tick": getattr(self, "tick", None),
                          "gemelos": n})
        return orig(self, obs)

    clase.decidir = decidir
    return orig
