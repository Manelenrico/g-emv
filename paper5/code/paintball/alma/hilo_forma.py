"""[P5-6A · A2] El hermano cuenta su forma por el canal `team`.

El mundo deja 120 ASCII imprimibles por mensaje y uno cada 24 tics
(`game.protocols.player`, «talk is separate and rate-limited to 1 per 24
ticks»). Aqui se codifica la forma ACEPTADA y el estado propio en ese hueco.

Formato, version 1:

    GF1|<tramo>;<tramo>;...|<hp>,<W>,<herido>

  · tramo = `x.y.i.tic`  con la intencion en una letra:
        i = ir · c = coger · u = usar · e = esperar
    y `-.-` en la casilla cuando el tramo es quedarse donde esta.
  · tic = el tic PREVISTO de llegada a ese punto de control.
  · hp entero, W con dos decimales, herido 0 o 1.
  · sin forma viva: `GF1||<hp>,<W>,<herido>`.

Cuatro tramos y el estado caben de sobra: el peor caso medido son 71
caracteres. `cabe()` lo comprueba y NUNCA se emite algo que no quepa.
"""
from __future__ import annotations

VERSION = "GF1"
TOPE = 120
LETRA = {"ir": "i", "coger": "c", "usar": "u", "esperar": "e"}
INTENCION = {v: k for k, v in LETRA.items()}
MAX_TRAMOS = 4


def cabe(s):
    return isinstance(s, str) and len(s) <= TOPE and s.isascii() and s.isprintable()


def codifica(tramos, hp, W, herido, tics=None):
    """(texto, cabe). `tramos` como los del banco; `tics` los previstos."""
    partes = []
    for i, tr in list(enumerate(tramos or []))[:MAX_TRAMOS]:
        d = tr.get("destino")
        x = f"{int(d[0])}.{int(d[1])}" if d else "-.-"
        letra = LETRA.get(tr.get("intencion") or "esperar", "e")
        tic = 0
        if tics is not None and i < len(tics):
            try:
                tic = int(tics[i])
            except Exception:
                tic = 0
        partes.append(f"{x}.{letra}.{tic}")
    try:
        hp_i = int(round(float(hp)))
    except Exception:
        hp_i = 0
    try:
        w_f = float(W or 0.0)
    except Exception:
        w_f = 0.0
    s = f"{VERSION}|{';'.join(partes)}|{hp_i},{w_f:.2f},{1 if herido else 0}"
    return s, cabe(s)


def decodifica(texto):
    """{'tramos': [...], 'tics': [...], 'hp':, 'W':, 'herido':} o None."""
    if not isinstance(texto, str):
        return None
    s = texto.strip()
    if not s.startswith(VERSION + "|"):
        return None
    try:
        _v, cuerpo, estado = s.split("|", 2)
    except ValueError:
        return None
    tramos, tics = [], []
    if cuerpo:
        for p in cuerpo.split(";"):
            trozos = p.split(".")
            if len(trozos) != 4:
                return None
            xa, ya, letra, tic = trozos
            if xa == "-" or ya == "-":
                destino = None
            else:
                try:
                    destino = (int(xa), int(ya))
                except ValueError:
                    return None
            if letra not in INTENCION:
                return None
            try:
                tics.append(int(tic))
            except ValueError:
                return None
            tramos.append({"destino": destino,
                           "intencion": INTENCION[letra], "esperar": 0})
    try:
        hp_s, w_s, h_s = estado.split(",")
        hp = int(hp_s); W = float(w_s); herido = bool(int(h_s))
    except Exception:
        return None
    return {"tramos": tramos, "tics": tics, "hp": hp, "W": W, "herido": herido}


def igual(a, b):
    """Igualdad de ida y vuelta: lo que importa es lo que el cuerpo usa."""
    if a is None or b is None:
        return a is b
    if len(a["tramos"]) != len(b["tramos"]) or a["tics"] != b["tics"]:
        return False
    for x, y in zip(a["tramos"], b["tramos"]):
        if (x.get("destino") != y.get("destino")
                or x.get("intencion") != y.get("intencion")):
            return False
    return (a["hp"], round(a["W"], 2), a["herido"]) == \
           (b["hp"], round(b["W"], 2), b["herido"])
