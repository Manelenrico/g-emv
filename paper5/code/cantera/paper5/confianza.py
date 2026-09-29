"""[P5-4A] Los tres consejeros de mentira, y la confianza.

A0 · LA VERDAD, declarada. El log del juego (`coworld episode-logs --game`) es
el stdout de los contenedores: arranque, chat y avisos. **No trae posiciones.**
El replay es un binario propietario (`ZERO_SUM_FRAMES`, 30 MB descomprimidos)
que no se puede leer sin su visor. Asi que **NO tenemos la verdad entera**: el
oraculo usa la VERDAD PARCIAL, la posicion real de un rival en el punto de
control cuando **alguno de los dos hermanos lo vio en ese tic**, y piso cuando
no lo vio ninguno.

A2 · COMO ENTRA LO DICHO, en las cinco filas de rivales:
  · si lo dicho hace la fila PEOR que el piso, se toma entero (lo malo siempre
    se cree);
  · si la hace MEJOR, la mejora sobre el piso entra multiplicada por C.
Con C = 0 y el consejero «nadie se mueve» sale exactamente E1+G2.
"""
from __future__ import annotations
import os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import forma as F                                          # noqa: E402
import alcance_g as AL                                     # noqa: E402

FILAS_RIVAL = F.PISO_RIVAL
SOLIDOS = ("#", "F", "R")
# [eleccion de la mesa, declarada] premio y castigo de la confianza
SUBE, BAJA = 0.05, 0.10
SUBE2, BAJA2 = 0.10, 0.20
C0 = 0.5
TOL_ACIERTO = 3          # casillas


def vistos_en(dia, tick):
    """{slot: pos} de lo que ESE diario vio en ese tic."""
    r = (dia or {}).get(tick)
    if r is None:
        return {}
    return {a.get("slot"): tuple(a.get("pos") or ())
            for a in (r.get("ve_agentes") or []) if a.get("pos")}


def verdad_parcial(dia_yo, dia_h, tick, herm):
    """Lo que alguno de los dos hermanos vio en ese tic, sin el hermano."""
    v = dict(vistos_en(dia_h, tick))
    v.update(vistos_en(dia_yo, tick))
    v.pop(herm, None)
    return v


def dice(consejero, rivales_w, tick, dia_yo, dia_h, herm, filas_mapa, rnd):
    """{slot: pos dicha} para los rivales de los que el consejero habla."""
    if consejero == "nadie":
        return dict(rivales_w)
    if consejero == "oraculo":
        return verdad_parcial(dia_yo, dia_h, tick, herm)
    # mentiroso: una casilla pisable al azar, por rival
    n = len(filas_mapa)
    out = {}
    for s in rivales_w:
        for _ in range(20):
            x, y = rnd.randrange(n), rnd.randrange(n)
            if filas_mapa[y][x] not in SOLIDOS:
                out[s] = (x, y)
                break
    return out


def obs_con_dicho(obs, dicho, herm):
    """La observacion con los rivales en la posicion DICHA."""
    vis = obs.get("visible") or {}
    ag = []
    for a in (vis.get("agents") or []):
        s = a.get("slot")
        if s != herm and s in dicho:
            b = dict(a)
            b["pos"] = [dicho[s][0], dicho[s][1]]
            ag.append(b)
        else:
            ag.append(a)
    o = dict(obs)
    o["visible"] = dict(vis, agents=ag)
    return o


def mezcla(F_dicho, pisos, C):
    """Las filas finales: lo malo entero, lo bueno por C."""
    out = dict(F_dicho)
    for k, piso in pisos.items():
        m = float(F_dicho.get(k) or 0.0)
        out[k] = m if m >= piso else piso - C * (piso - m)
    return out


def actualiza_C(C, dicho, dia_yo, dia_h, tick, herm, sube=SUBE, baja=BAJA):
    """(C nueva, aciertos, fallos). Solo cuentan los rivales COMPROBADOS."""
    real = verdad_parcial(dia_yo, dia_h, tick, herm)
    ok = mal = 0
    for s, p in dicho.items():
        q = real.get(s)
        if q is None:
            continue
        if AL.cheb(p, q) <= TOL_ACIERTO:
            ok += 1
        else:
            mal += 1
    C = min(1.0, max(0.0, C + sube * ok - baja * mal))
    return C, ok, mal


# ── [P5-4B] LA AUSENCIA, Y LA MONEDA DE LO NUEVO ───────────────────────────
AUSENTE = "__AUSENTE__"
SUBE_N, BAJA_N = 0.10, 0.20      # la moneda de lo nuevo
TRIVIAL = 3                      # a 3 casillas o menos de donde estaba: trivial


def dice2(consejero, rivales_w, tick, dia_yo, dia_h, herm, filas_mapa, rnd,
          p_aus=0.0):
    """{slot: pos | AUSENTE}. El consejero puede decir una AUSENCIA.

    · oraculo: ausencia cuando NINGUN hermano ve al rival en ese tic;
    · mentiroso: ausencia con la misma FRECUENCIA que el oraculo (`p_aus`,
      medida aparte), y si no, una casilla al azar; el sorteo es independiente
      de la verdad, asi que no filtra informacion;
    · nadie se mueve: nunca dice ausencia.
    """
    if consejero == "nadie":
        return dict(rivales_w)
    if consejero == "oraculo":
        real = verdad_parcial(dia_yo, dia_h, tick, herm)
        return {s: real.get(s, AUSENTE) for s in rivales_w}
    n = len(filas_mapa)
    out = {}
    for s in rivales_w:
        if rnd.random() < p_aus:
            out[s] = AUSENTE
            continue
        for _ in range(20):
            x, y = rnd.randrange(n), rnd.randrange(n)
            if filas_mapa[y][x] not in SOLIDOS:
                out[s] = (x, y)
                break
    return out


def obs_con_dicho2(obs, dicho, herm):
    """Con AUSENCIA, el rival SALE de `visible.agents`.

    DECLARADO: la `Memoria` de la tabla no guarda posiciones de rivales
    (`appraisal_zs_v42_exp.py:449-470`), asi que quitarlo de `visible` lo quita
    del todo de las cinco filas. Las filas que leen memoria (el agresor de la
    hermana, por `mem`) siguen leyendola: la ausencia no borra recuerdos.
    """
    vis = obs.get("visible") or {}
    ag = []
    for a in (vis.get("agents") or []):
        s = a.get("slot")
        if s == herm or s not in dicho:
            ag.append(a)
            continue
        d = dicho[s]
        if d is AUSENTE or d == AUSENTE:
            continue                       # fuera de vista: no esta
        b = dict(a)
        b["pos"] = [d[0], d[1]]
        ag.append(b)
    o = dict(obs)
    o["visible"] = dict(vis, agents=ag)
    return o


def no_trivial(dicho, rivales_w):
    """Las afirmaciones que NO son «sigue donde estaba»."""
    out = {}
    for s, d in dicho.items():
        if d is AUSENTE or d == AUSENTE:
            out[s] = AUSENTE
        elif s not in rivales_w or AL.cheb(d, rivales_w[s]) > TRIVIAL:
            out[s] = d
    return out


def actualiza_C2(C, dicho, rivales_w, dia_yo, dia_h, tick, herm, mundo,
                 sube=SUBE_N, baja=BAJA_N):
    """La moneda de lo nuevo: solo pagan las afirmaciones NO triviales."""
    nt = no_trivial(dicho, rivales_w)
    if not nt:
        return C, 0, 0, 0
    real = verdad_parcial(dia_yo, dia_h, tick, herm)
    ok = mal = comp = 0
    for s, d in nt.items():
        if d is AUSENTE or d == AUSENTE:
            # acierto si NINGUN hermano lo ve en ese tic
            comp += 1
            if s in real:
                mal += 1
            else:
                ok += 1
            continue
        q = real.get(s)
        if q is None:
            continue                      # no comprobable
        comp += 1
        if AL.cheb(d, q) <= TOL_ACIERTO:
            ok += 1
        else:
            mal += 1
    C = min(1.0, max(0.0, C + sube * ok - baja * mal))
    return C, ok, mal, len(nt)
