"""[P5-6A · A5] El brazo T: formas al azar con la forma de las de verdad.

El control tiene que parecerse a lo que controla, o no controla nada. Por eso
el numero de tramos y las distancias se sortean de la **distribucion empirica
medida** en las 334 formas traducidas del brazo FORMAS/Haiku de P5-5B
(`P56A_distribucion_azar.json`), no de una distribucion inventada.

  · tramos por forma: 1 el 14,1 % · 2 el 32,3 % · 3 el 38,0 % · 4 el 15,6 %
  · el 39,7 % de los tramos son «quedarse»
  · las distancias van sobre todo de 1 a 6 casillas

La intencion es `ir`, y `coger` si en la casilla de destino hay un objeto, que
es lo que pide el encargo. El destino tiene que ser **alcanzable**: casilla del
mapa, no solida, y se busca a la distancia sorteada.
"""
from __future__ import annotations
import json, os, random

AQUI = os.path.dirname(os.path.abspath(__file__))
SOLIDOS = ("#", "F", "R")
# copia embebida de la distribucion medida, para que la imagen no dependa de
# un fichero de datos suelto. La fuente es P56A_distribucion_azar.json.
N_TRAMOS = {1: 47, 2: 108, 3: 127, 4: 52}
DISTANCIAS = {1: 125, 2: 105, 3: 69, 4: 78, 5: 38, 6: 47, 7: 19, 8: 14,
              9: 4, 10: 7, 11: 3, 12: 1, 14: 1, 15: 3}
P_QUEDARSE = 0.397


def _carga_si_hay():
    """Si el json de la medida esta al lado, manda el (declarado)."""
    for p in (os.path.join(AQUI, "P56A_distribucion_azar.json"),
              os.path.join(AQUI, "..", "..", "cantera", "paper5",
                           "P56A_distribucion_azar.json")):
        if os.path.exists(p):
            try:
                d = json.load(open(p))
                nt = {int(k): v for k, v in d["n_tramos"].items()}
                di = {int(k): v for k, v in d["distancias"].items()}
                pq = d["quedarse"] / max(1, d["tramos"])
                return nt, di, pq
            except Exception:
                pass
    return N_TRAMOS, DISTANCIAS, P_QUEDARSE


def _sortea(pesos, rnd):
    tot = sum(pesos.values())
    x = rnd.random() * tot
    for k in sorted(pesos):
        x -= pesos[k]
        if x <= 0:
            return k
    return sorted(pesos)[-1]


def casilla_a(filas, pos, pasos, rnd):
    """Una casilla pisable a EXACTAMENTE `pasos` de Chebyshev, o None."""
    n = len(filas)
    ops = [(pos[0] + dx, pos[1] + dy)
           for dy in range(-pasos, pasos + 1)
           for dx in range(-pasos, pasos + 1)
           if max(abs(dx), abs(dy)) == pasos
           and 0 <= pos[0] + dx < n and 0 <= pos[1] + dy < n
           and filas[pos[1] + dy][pos[0] + dx] not in SOLIDOS]
    return rnd.choice(ops) if ops else None


def forma_al_azar(pos, filas, suelo, rnd=None):
    """[tramos] con la pinta de las de verdad. `suelo` = {(x,y): item}."""
    rnd = rnd or random
    nt, di, pq = _carga_si_hay()
    n = _sortea(nt, rnd)
    tramos, p = [], tuple(pos)
    for _ in range(n):
        if rnd.random() < pq:
            tramos.append({"destino": None, "intencion": "esperar",
                           "esperar": 11})
            continue
        for _intento in range(6):
            d = _sortea(di, rnd)
            q = casilla_a(filas, p, d, rnd)
            if q:
                break
        else:
            tramos.append({"destino": None, "intencion": "esperar",
                           "esperar": 11})
            continue
        hay = suelo.get(tuple(q))
        tramos.append({"destino": tuple(q),
                       "intencion": "coger" if hay else "ir", "esperar": 0})
        p = tuple(q)
    if not tramos:
        tramos = [{"destino": None, "intencion": "esperar", "esperar": 11}]
    return tramos
