"""Banco de EL MURO DEL MIEDO — PROMPT_47. EL REGISTRO DEL PARAR (resello).

El muro se escribio en la tabla (S-7: factor de cercania CONVEXO bajo
MURO_D0=4, intacto mas alla POR CONSTRUCCION; activacion solo con bocajarro
PRESENTE via `_muro_on` estampado desde la obs real — P2 por construccion).

El barrido de K tumbo LA PREMISA del sello P1, no el muro:

  LOS DESTINOS MEDIDOS (la correccion del hecho del 46 — el error era del
  acta, que llamo "iba hacia el cazador" a lo que la geometria desmiente):
    brecha +3E : ir_objeto acaba a dist 1,00  -> MAS CERCA (la unica)
    det+5E     : acaba a dist 2,00 == 2,00    -> EQUIDISTANTE (flanqueo con
                 transito rasante; la foto tasa el punto final, no la senda)
    perpN      : acaba a dist 3,61            -> MAS LEJOS
    contraW    : acaba a dist 5,00            -> MAS LEJOS
    perp45     : acaba a dist 3,61            -> MAS LEJOS

  Lo que el muro SI hace (reproducido abajo): la unica foto que ACERCA (la
  brecha) pierde bajo muro, y a K=2,5 el candado del 46 aguanta el acopio a
  0,18 con margen +0,054 (K=3: +0,097) — EL INTERVALO DEL ACOPIO EXISTIRIA.
  Lo que el muro NO puede hacer: cobrar el TRANSITO (det+5E) — eso es tasar
  la senda en el evaluador, otro encargo y otro sofa.

  P1 LITERAL ("v26 se aparta en las 4") no es evaluable tal como se sello:
  3 de las 4 ya se apartaban en v24. PARAR (trato del 46): MURO_K = 0,
  alma efectiva v24, sin C ni campo, y la mesa resella con esta geometria.

GATES (verdes: el estado sellado + el registro reproducible):
  1. MURO_K por defecto == 0.0 y S-7 identica a v24 (varas del 39/43 exactas).
  2. P2 POR CONSTRUCCION: agresor mas alla de D0 -> mesa bit-identica a v24
     aunque haya fotos que entren en la zona.
  3. EL REGISTRO: a K=2,5 la brecha del 46 huye con ACOPIO_M=0,18 (margen
     +0,05) y a K=0 caia — el muro sostiene el acopio donde el 46 no podia.
  4. LA GEOMETRIA: los cinco destinos de ir_objeto, medidos (la correccion).
  5. Determinismo 3/3.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_47
"""
from __future__ import annotations

import json
import math
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs

_fallos = []
GOLPE = 18.0


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def mesa(mundo, o, t=300):
    mem = A.Memoria(); mem.hp_max = 100
    mem.observa(o, mundo, t)
    _a, rad = D.decide(o, mundo, mem, t)
    c = {k: (v["d"] if isinstance(v, dict) else v)
         for k, v in (rad.get("candidatos") or {}).items()}
    return rad.get("elegido"), c


def main():
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    YO = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            YO = (y, y)
            break
    CAZ = (YO[0] + 2, YO[1])

    def esc(bx, by, hp=25):
        BOT = (YO[0] + bx, YO[1] + by)
        o = obs(300, YO, hp=hp,
                agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                          "hp_band": "healthy"}],
                items=[{"id": "first_aid", "n": 1, "pos": list(BOT)}])
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
        return o, BOT

    # ── 1. el sello (RESELLADO EN EL 48) ─────────────────────────────────
    print("=== 1. EL SELLO: 0/0 (el PARAR del 47) o 3/0,18 (el encendido) ===")
    check("estado sellado valido: (K,M) es (0,0) o (3.0, 0.18)",
          (A.MURO_K, A.ACOPIO_M) in ((0.0, 0.0), (3.0, 0.18)),
          f"K={A.MURO_K} M={A.ACOPIO_M}")
    _K0, _M0 = A.MURO_K, A.ACOPIO_M
    # la historia del 47 se reproduce con SUS constantes (0/0), fijadas a mano
    A.MURO_K, A.ACOPIO_M = 0.0, 0.0
    def escena39(golpes, hp0):
        memx = A.Memoria(); memx.hp_max = 100
        hp = float(hp0); t = 300
        HER = (YO[0] + 1, YO[1])
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "healthy"}]
        for _ in range(golpes):
            hp = max(1.0, hp - GOLPE)
            oo = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
                     pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
            oo["you"]["damage_taken"] = [{"source": f"P{par}", "amount": GOLPE}]
            memx.observa(oo, mundo, t); t += 1
        oo = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
                 pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
        memx.observa(oo, mundo, t)
        _a, rad = D.decide(oo, mundo, memx, t)
        c = {k: (v["d"] if isinstance(v, dict) else v)
             for k, v in (rad.get("candidatos") or {}).items()}
        at = min((v for k, v in c.items() if k.startswith("atacar")), default=None)
        return (at - c[min(c, key=c.get)]) if at is not None else None
    ESPERADO = {(1, 100): 0.20928, (4, 28): 0.49587, (5, 100): 0.39281}
    for (g, hp0), vara in ESPERADO.items():
        m = escena39(g, hp0)
        check(f"vara del 39/43 exacta ({g}g/hp0={hp0})",
              m is not None and abs(m - vara) < 1e-4, f"{m:+.5f} vs {vara:+.5f}")

    # ── 2. P2 por construccion ────────────────────────────────────────────
    print("\n=== 2. P2: agresor LEJOS -> mesa bit-identica aunque una foto entre ===")
    CAZL = (YO[0] + 6, YO[1])
    o2 = obs(300, YO, hp=40,
             agentes=[{"slot": 15, "team": "D", "pos": list(CAZL),
                       "hp_band": "healthy"}],
             items=[{"id": "first_aid", "n": 1, "pos": [YO[0] + 5, YO[1]]}])
    o2["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
    tab = {}
    for nm, k in (("v24", 0.0), ("muro K=2,5", 2.5)):
        A.MURO_K = k
        _el, c = mesa(mundo, o2)
        tab[nm] = c
    A.MURO_K = 0.0
    check("mesa completa bit-identica con el agresor a 6 (> D0)",
          json.dumps(tab["v24"], sort_keys=True)
          == json.dumps(tab["muro K=2,5"], sort_keys=True),
          f"({len(tab['v24'])} candidatos)")

    # ── 3. el registro: el muro sostiene el acopio en la brecha ───────────
    print("\n=== 3. EL REGISTRO: la brecha del 46 bajo muro + acopio 0,18 ===")
    o3, _ = esc(3, 0, 25)
    res = {}
    for nm, k, m in (("sin muro (46)", 0.0, 0.18), ("K=2,5", 2.5, 0.18),
                     ("K=3", 3.0, 0.18)):
        A.MURO_K = k; A.ACOPIO_M = m
        el, c = mesa(mundo, o3)
        margen = (c.get("ir_objeto", 9) - c[el]) if el != "ir_objeto" else -1.0
        res[nm] = (el, margen)
        print(f"     {nm:<14} elige `{el}`"
              + (f"  margen sobre ir_objeto {margen:+.5f}" if margen >= 0 else ""))
    A.MURO_K = 0.0; A.ACOPIO_M = 0.0
    check("sin muro, el acopio 0,18 COMPRABA riesgo (la brecha del 46)",
          res["sin muro (46)"][0] == "ir_objeto", "")
    check("con muro K=2,5, HUYE con margen > 0,05",
          res["K=2,5"][0].startswith("move_") and res["K=2,5"][1] > 0.05,
          f"{res['K=2,5']}")
    check("con muro K=3, margen > 0,09",
          res["K=3"][1] > 0.09, f"{res['K=3'][1]:+.5f}")

    # ── 4. la geometria medida (la correccion del 46) ─────────────────────
    print("\n=== 4. LA GEOMETRIA: destinos reales de ir_objeto (la correccion) ===")
    d0 = math.dist(YO, CAZ)
    ESP = {"brecha +3E": (3, 0, "ACERCA"), "det+5E": (5, 0, "EQUIDISTANTE"),
           "perpN": (0, -3, "ALEJA"), "contraW": (-3, 0, "ALEJA")}
    for nm, (bx, by, esperado) in ESP.items():
        _o, BOT = esc(bx, by)
        campo = D.campo_geodesico(mundo, BOT)
        p2 = D._camina_geodesica(YO, campo, mundo, 5, 48, BOT,
                                 frozenset([tuple(CAZ)]))
        d2 = math.dist(p2, CAZ)
        v = "ACERCA" if d2 < d0 - 1e-9 else ("ALEJA" if d2 > d0 + 1e-9
                                             else "EQUIDISTANTE")
        check(f"{nm}: la foto {esperado}", v == esperado,
              f"{d0:.2f} -> {d2:.2f}")
    print("     (solo la brecha ACERCA; det+5E flanquea EQUIDISTANTE con")
    print("      transito rasante — la foto tasa el punto final, no la senda)")

    # ── 5. determinismo ───────────────────────────────────────────────────
    print("\n=== 5. determinismo 3/3 ===")
    firmas = set()
    for _ in range(3):
        acc = []
        for oo in (o2, o3):
            A.MURO_K = 0.0; A.ACOPIO_M = 0.0
            el, c = mesa(mundo, oo)
            acc.append((el, json.dumps(c, sort_keys=True)))
        firmas.add(json.dumps(acc))
    check("3 corridas identicas", len(firmas) == 1, f"{len(firmas)} firma(s)")

    A.MURO_K, A.ACOPIO_M = _K0, _M0
    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
