"""Banco de EL ENCENDIDO — PROMPT_48. La pila de C completa, con sellos.

v27 (efectiva) = v24 + MURO (K=3, resello P1' de la mesa) + ACOPIO (M=0,18).
Las constantes viven en la tabla y estan ENCENDIDAS por defecto: este banco
verifica el encendido tal como quedo, pareando contra v24 (K=0, M=0) por
monkeypatch — el pareado exacto de la casa.

P1' (RESELLO de la mesa, sustituye al P1 del 47):
  - ninguna foto ELEGIDA acaba mas cerca del cazador que la posicion actual
    (en todas las geometrias del barrido del 46/47);
  - la brecha +3E HUYE con el acopio encendido;
  - el flanqueo det+5E NO EMPEORA (equidistante se acepta; la senda no se
    tasa — limite declarado, a la reserva).

LAS CUATRO DEL 47: lejos identico a v24 (muro por construccion, pareado con
el MISMO acopio); honor (margenes de atacar iguales o mas lejos; el
responder->huir a bocajarro se DECLARA); techo del 09 y reparto intactos.

LAS CINCO DEL 46 sobre v27: calma compra (competencia: el botiquin llama);
jerarquia del miedo (la brecha huye CON el muro debajo); honor servido
(fotos del 39/43 identicas con/sin acopio: la fila servida calla); silencio
del servido (mesa bit-identica v24<->v27 con botiquin a bordo y sin
bocajarro); determinismo 3/3.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_48
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
K_SELLADA, M_SELLADA = 3.0, 0.18


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v27():
    A.MURO_K, A.ACOPIO_M = K_SELLADA, M_SELLADA


def v24():
    A.MURO_K, A.ACOPIO_M = 0.0, 0.0


def mesa(mundo, o, t=300, mem=None):
    if mem is None:
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

    print(f"  constantes encendidas: MURO_K={A.MURO_K}  ACOPIO_M={A.ACOPIO_M}\n")
    check("el encendido es el sellado (K=3, M=0,18)",
          (A.MURO_K, A.ACOPIO_M) == (K_SELLADA, M_SELLADA), "")

    def esc(bx, by, hp=25):
        BOT = (YO[0] + bx, YO[1] + by)
        o = obs(300, YO, hp=hp,
                agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                          "hp_band": "healthy"}],
                items=[{"id": "first_aid", "n": 1, "pos": list(BOT)}])
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
        return o, BOT

    # ── P1' en todas las geometrias del barrido ───────────────────────────
    print("=== P1' (resello): ninguna foto ELEGIDA acaba mas cerca ===")
    d0 = math.dist(YO, CAZ)
    GEOS = [("brecha +3E", 3, 0, 25), ("det+5E", 5, 0, 25),
            ("perpN", 0, -3, 25), ("contraW", -3, 0, 25),
            ("perp45", 0, -3, 45)]
    v27()
    for nm, bx, by, hp in GEOS:
        o, BOT = esc(bx, by, hp)
        el, c = mesa(mundo, o)
        # ¿donde acaba la foto del elegido?
        if el.startswith(("move_", "paso_")):
            dxy = D.DIRS[el.split("_")[-1]]
            if el.startswith("move_"):
                p2 = D._simula_camino(YO, el.split("_")[-1], mundo, 5, 48, False)
            else:
                p2 = (YO[0] + dxy[0], YO[1] + dxy[1])
        elif el == "ir_objeto":
            campo = D.campo_geodesico(mundo, BOT)
            p2 = D._camina_geodesica(YO, campo, mundo, 5, 48, BOT,
                                     frozenset([tuple(CAZ)]))
        elif el == "usar_botiquin":
            p2 = YO
        else:
            p2 = YO
        d2 = math.dist(p2, CAZ)
        check(f"{nm}: elegido `{el}` acaba a {d2:.2f} >= {d0:.2f}",
              d2 >= d0 - 1e-9, "")
    o3, _ = esc(3, 0, 25)
    el, c = mesa(mundo, o3)
    margen = (c.get("ir_objeto", 9) - c[el]) if el != "ir_objeto" else -1
    check("la brecha HUYE con el acopio encendido",
          el.startswith("move_"), f"`{el}`, margen {margen:+.5f}")
    check("...con el margen del sello (> 0,09)", margen > 0.09, "")

    # ── las cuatro del 47 ─────────────────────────────────────────────────
    print("\n=== LAS CUATRO DEL 47 ===")
    # (a) lejos identico: mismo acopio en ambos brazos, muro on/off
    CAZL = (YO[0] + 6, YO[1])
    o2 = obs(300, YO, hp=40,
             agentes=[{"slot": 15, "team": "D", "pos": list(CAZL),
                       "hp_band": "healthy"}],
             items=[{"id": "first_aid", "n": 1, "pos": [YO[0] + 5, YO[1]]}])
    o2["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
    tab = {}
    for nm, k in (("sin muro", 0.0), ("muro K=3", K_SELLADA)):
        A.MURO_K = k; A.ACOPIO_M = M_SELLADA
        _el, cc = mesa(mundo, o2)
        tab[nm] = cc
    v27()
    check("agresor a 6 (> D0): mesa bit-identica (el muro calla lejos)",
          json.dumps(tab["sin muro"], sort_keys=True)
          == json.dumps(tab["muro K=3"], sort_keys=True),
          f"({len(tab['sin muro'])} candidatos)")
    # (b) honor: margenes de atacar en las fotos del 39, pareado v24/v27
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
        el, cc = mesa(mundo, oo, t, memx)
        at = min((v for k, v in cc.items() if k.startswith("atacar")), default=None)
        return el, (at - cc[el]) if at is not None else None
    cambios = []
    for g, hp0 in ((1, 100), (3, 28), (4, 28), (5, 100)):
        v24(); e24, m24 = escena39(g, hp0)
        v27(); e27, m27 = escena39(g, hp0)
        check(f"honor {g}g/hp0={hp0}: margen v27 >= v24",
              m27 is not None and m27 >= m24 - 1e-9,
              f"{m24:+.5f} -> {m27:+.5f}")
        if e27 != e24:
            cambios.append(f"{g}g/hp0={hp0}: {e24} -> {e27}")
    print(f"     cambios de eleccion a bocajarro (DECLARADOS): "
          f"{cambios if cambios else 'ninguno'}")
    # (c) techo del 09 y reparto intactos
    check("techo del 09 intacto (AGRESOR_TECHO=0.5, CAP_TOTAL=0.5)",
          A.AGRESOR_TECHO == 0.5 and A.AGRESOR_CAP_TOTAL == 0.5, "")
    check("reparto de S-7 intacto (0.5/0.1/0.4)",
          A.REPARTO["S-7-AGRESOR"] == (0.5, 0.1, 0.4), "")

    # ── las cinco del 46 sobre v27 ────────────────────────────────────────
    print("\n=== LAS CINCO DEL 46, SOBRE LA PILA ENCENDIDA ===")
    # 1. calma compra (con competencia: la prueba dura)
    v27()
    o4 = obs(300, YO, hp=100,
             items=[{"id": "rations", "n": 1, "pos": [YO[0] - 2, YO[1]]},
                    {"id": "first_aid", "n": 1, "pos": [YO[0] - 5, YO[1] - 1]}])
    memx = A.Memoria(); memx.hp_max = 100; memx.observa(o4, mundo, 300)
    dst = D._mejor_objeto(YO, mundo, memx, o4, 300)
    el4, _c4 = mesa(mundo, o4)
    check("CALMA COMPRA: con racion cerca, el botiquin lejano llama",
          dst == (YO[0] - 5, YO[1] - 1), f"destino {dst}")
    check("...y el elegido es ir_objeto", el4 == "ir_objeto", el4)
    # 2. jerarquia del miedo: la brecha (ya arriba) + perseguido sin botin
    o5 = obs(300, YO, hp=55,
             agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                       "hp_band": "healthy"}])
    o5["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
    el5, _ = mesa(mundo, o5)
    check("perseguido sin botin: huye (el muro debajo)",
          el5.startswith("move_") or el5.startswith("ir_"), el5)
    # 3. honor servido: fotos del 39/43 con/sin acopio identicas
    for g, hp0 in ((4, 28), (1, 100)):
        A.MURO_K = K_SELLADA; A.ACOPIO_M = 0.0
        _eA, mA = escena39(g, hp0)
        v27(); _eB, mB = escena39(g, hp0)
        check(f"servido {g}g/hp0={hp0}: margen identico con/sin acopio",
              mA is not None and abs(mB - mA) < 1e-9, f"{mA:+.5f} vs {mB:+.5f}")
    # 4. silencio del servido: botiquin a bordo, sin bocajarro
    o6 = obs(300, YO, hp=40, pack=[{"id": "first_aid", "n": 1}, None],
             items=[{"id": "rations", "n": 1, "pos": [YO[0] - 2, YO[1]]}],
             agentes=[{"slot": 15, "team": "D", "pos": [YO[0] + 6, YO[1]],
                       "hp_band": "healthy"}])
    tab2 = {}
    for nm, (k, m) in (("v24", (0.0, 0.0)), ("v27", (K_SELLADA, M_SELLADA))):
        A.MURO_K, A.ACOPIO_M = k, m
        _el, cc = mesa(mundo, o6)
        tab2[nm] = cc
    v27()
    check("SILENCIO DEL SERVIDO: mesa bit-identica v24<->v27",
          json.dumps(tab2["v24"], sort_keys=True)
          == json.dumps(tab2["v27"], sort_keys=True),
          f"({len(tab2['v24'])} candidatos)")

    # ── determinismo 3/3 ──────────────────────────────────────────────────
    print("\n=== determinismo 3/3 ===")
    firmas = set()
    for _ in range(3):
        acc = []
        for oo in (o3, o4, o6):
            v27()
            el, cc = mesa(mundo, oo)
            acc.append((el, json.dumps(cc, sort_keys=True)))
        firmas.add(json.dumps(acc))
    check("3 corridas identicas", len(firmas) == 1, f"{len(firmas)} firma(s)")

    v27()
    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
