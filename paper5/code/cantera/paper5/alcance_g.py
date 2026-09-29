"""[P5-3G] Los rivales por ADONDE PUEDEN LLEGAR, y el hermano que cuenta.

G1 · ALCANCE. Un rival visto en el tic de ventana no se congela: se le pone en
la casilla ALCANZABLE MAS CERCANA a nuestra posicion proyectada —lo peor que
puede hacer, no lo que hara—. Alcanzable = por el mapa estatico (muros `#`,
fortaleza `F` y rocas `R` cortan) con el enfriamiento de andar del mundo,
**11 tics por paso** (`manual_del_mundo.md` §4: `16 - velocidad`; el catalogo
no da velocidades por arma, solo `range` y `cooldown` de ataque, asi que el
paso es el mismo para todos y se declara). Su arma suma su `range` del
catalogo: espada 1, lanza 2, red 3, cuchillos 5, cerbatana 6, arco 8.

LAS CINCO FILAS QUE MIRAN A RIVALES, con su linea en
`appraisal_zs_v42_exp.py`:
    F-4-ALCANCE     :1070   estas a tiro de alguien
    S-8-EXPOSICION  :1416   cuantos hostiles pueden verte
    S-7-AGRESOR     :1508   ese te esta pegando
    MIEDO_APRENDIDO :1553   (apagada en esta configuracion)
    S-VIDA-AJENA    :1663   (apagada en esta configuracion)
**Sin piso**: el alcance lo sustituye.

LIMITE DECLARADO. La `Memoria` de la tabla **no guarda la posicion de los
rivales** (solo `pareja_pos`, del hermano: `appraisal_zs_v42_exp.py:449-470`).
Asi que «rivales recordados y no a la vista» no se puede hacer: solo entran los
que estan a la vista en el tic de ventana. Se dice y no se inventa.

G2 · EL HERMANO QUE CUENTA. Las diez filas del hermano se evaluan con su estado
REAL en ese tic, leido de SU diario (el otro asiento de la misma partida), como
si nos hubiera contado su forma.
"""
from __future__ import annotations
import collections, copy, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (RAIZ, os.path.join(RAIZ, "paintball")):
    if p not in sys.path:
        sys.path.insert(0, p)

SOLIDOS = ("#", "F", "R")
PASO_TICS = 11
FILAS_RIVAL = ("F-4-ALCANCE", "S-8-EXPOSICION", "S-7-AGRESOR",
               "MIEDO_APRENDIDO", "S-VIDA-AJENA")
FILAS_HERMANO = ("S-COMPANIA", "S-SOLEDAD", "S-DANO-PAREJA",
                 "S-MUERTE-PAREJA", "S-VINCULO", "S-HERIDO", "S-PROVISION",
                 "F-HERMANO-AMENAZA", "F-HERMANO-GOLPE", "R-HERMANO-FALTA")
_OCHO = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


def bfs(filas, origen):
    """Distancia en PASOS por el mapa estatico desde `origen`. dict pos->pasos."""
    n = len(filas)
    ox, oy = int(origen[0]), int(origen[1])
    if not (0 <= ox < n and 0 <= oy < n):
        return {}
    d = {(ox, oy): 0}
    q = collections.deque([(ox, oy)])
    while q:
        x, y = q.popleft()
        k = d[(x, y)] + 1
        for dx, dy in _OCHO:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < n and 0 <= ny < n):
                continue
            if (nx, ny) in d or filas[ny][nx] in SOLIDOS:
                continue
            d[(nx, ny)] = k
            q.append((nx, ny))
    return d


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def peor_casilla(dist_r, pasos, P):
    """La casilla alcanzable en `pasos` mas cerca (Chebyshev) de `P`."""
    mejor, md = None, None
    for c, k in dist_r.items():
        if k > pasos:
            continue
        s = cheb(c, P)
        if md is None or s < md:
            mejor, md = c, s
            if md == 0:
                break
    return mejor, md


def alcance_arma(mundo, mano):
    it = mundo.items.get((mano or {}).get("id") if isinstance(mano, dict)
                         else mano)
    return int(getattr(it, "range", 0) or 0) if it is not None else 0


def obs_con_alcance(obs_w, mundo, filas_mapa, pos_proy, k_tics, herm_slot,
                    bfs_cache):
    """La observacion del punto de control con los rivales en su PEOR casilla.

    `bfs_cache` es {slot: dict_de_distancias}, para no rehacer el BFS por punto.
    """
    vis = obs_w.get("visible") or {}
    pasos = int(k_tics // PASO_TICS)
    nuevos, detalle = [], []
    for a in (vis.get("agents") or []):
        if a.get("slot") == herm_slot:
            nuevos.append(a)
            continue
        p0 = tuple(a.get("pos") or ())
        if not p0:
            nuevos.append(a)
            continue
        dr = bfs_cache.get(a.get("slot"))
        if dr is None:
            dr = bfs(filas_mapa, p0)
            bfs_cache[a.get("slot")] = dr
        c, md = peor_casilla(dr, pasos, pos_proy)
        if c is None:
            nuevos.append(a)
            continue
        b = dict(a)
        b["pos"] = [c[0], c[1]]
        nuevos.append(b)
        detalle.append({"slot": a.get("slot"), "de": list(p0), "a": list(c),
                        "pasos": pasos, "dist_a_nosotros": md,
                        "alcance_arma": alcance_arma(mundo, a.get("hand"))})
    o = dict(obs_w)
    o["visible"] = dict(vis, agents=nuevos)
    return o, detalle


def pon_hermano(obs, mem, herm_slot, rec_h, pos_proy, mundo):
    """Mete al hermano con su estado REAL de ese tic (G2).

    `rec_h` es su registro de tic, o None si ya habia muerto.
    """
    vis = obs.get("visible") or {}
    agents = [a for a in (vis.get("agents") or []) if a.get("slot") != herm_slot]
    m2 = copy.copy(mem)
    if rec_h is None:
        m2.pareja_muerta = True
        obs2 = dict(obs)
        obs2["visible"] = dict(vis, agents=agents)
        return obs2, m2
    ph = tuple(rec_h.get("pos") or ())
    hp = rec_h.get("hp") or 0
    banda = ("healthy" if hp >= 67 else "hurt" if hp >= 34 else "critical")
    m2.pareja_muerta = False
    m2.pareja_pos = ph
    m2.pareja_banda = banda
    # solo entra en `visible.agents` si lo VERIAMOS desde la posicion proyectada
    try:
        r_vis = mundo.radio_vision_max()
    except Exception:
        r_vis = 8.0
    if ph and cheb(pos_proy, ph) <= r_vis:
        agents = agents + [{"slot": herm_slot, "team": mundo.team,
                            "pos": [ph[0], ph[1]], "hp_band": banda,
                            "hand": (rec_h.get("hand") or {}).get("id")
                            if isinstance(rec_h.get("hand"), dict) else None,
                            "body": rec_h.get("body"), "netted": False,
                            "poisoned": False, "channeling": False}]
    obs2 = dict(obs)
    obs2["visible"] = dict(vis, agents=agents)
    return obs2, m2
