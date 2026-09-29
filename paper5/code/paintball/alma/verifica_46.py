"""Banco de EL ACOPIO — PROMPT_46. EL REGISTRO DEL PARAR.

La fila R-ACOPIO se escribio (malestar R de fondo con la mochila sin botiquin;
alivio solo por adquisicion prevista — la foto de coger/ir_objeto-llegando ya
mete el objeto en el zurron, 07 B; la foto de usar el botiquin marca
`_cura_en_curso` y la fila calla). La calibracion la tumbo el CANDADO P2:

  EL INTERVALO IMPOSIBLE (medido aqui, reproducible abajo):
    - para que el botiquin LLAME en calma con competencia (P1 de verdad:
      racion cerca, botiquin lejos) hace falta  M >= 0,18
    - el muro del miedo a bocajarro (cazador a 2, hp 25) mide  0,02512
      -> cualquier M > ~0,03 lo salta: v24 huia (move_SW) y v25 caminaba
         hacia el botiquin DETRAS del cazador (ir_objeto). COMPRA RIESGO.
  No hay M util. La causa no es el acopio: es el muro fino — el APARCADO DEL
  21 (hambre vs miedo: "con la comida en medio, el hambre manda", [Manel]).

  PARAR ejecutado: ACOPIO_M = 0.0 (sellada). El alma efectiva es la v24 —
  la fila existe en el codigo y es identicamente nula.

GATES (verdes: verifican el estado sellado y guardan la brecha reproducible):
  1. ACOPIO_M por defecto == 0.0 y la fila da 0 en toda escena.
  2. Con la fila a 0, las fotos del 39/43 dan margenes IDENTICOS (v24).
  3. LA BRECHA, reproducida a M=0,18 (documento, no conducta): en la escena
     del candado v24 huye y v25 va al botiquin tras el cazador.
  4. El intervalo: a M=0,02 el muro aguanta; a M=0,03 cae. En P1-con-
     competencia, el botiquin no llama hasta M=0,18.
  5. Determinismo 3/3.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_46
"""
from __future__ import annotations

import json
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


def mesa(mundo, o, tick=300):
    mem = A.Memoria(); mem.hp_max = 100
    mem.observa(o, mundo, tick)
    _a, rad = D.decide(o, mundo, mem, tick)
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

    # ── 1. el sello (RESELLADO EN EL 48) ─────────────────────────────────
    print("=== 1. EL SELLO: 0 (el PARAR del 46) o 0,18 con muro (el 48) ===")
    check("estado sellado valido: (M,K) es (0,0) o (0.18, 3.0)",
          (A.ACOPIO_M, A.MURO_K) in ((0.0, 0.0), (0.18, 3.0)),
          f"M={A.ACOPIO_M} K={A.MURO_K}")
    # la historia del 46 se reproduce con SUS constantes, fijadas a mano
    _M0, _K0 = A.ACOPIO_M, A.MURO_K
    A.ACOPIO_M, A.MURO_K = 0.0, 0.0
    o = obs(300, YO, hp=100)
    mem = A.Memoria(); mem.hp_max = 100; mem.observa(o, mundo, 300)
    F = A.filas(o, mundo, mem, 300)
    check("con M=0 la fila es nula (el mundo del 46)",
          (F.get("R-ACOPIO") or 0.0) == 0.0, "")

    # ── 2. el alma efectiva es la v24 ─────────────────────────────────────
    print("\n=== 2. FOTOS DEL 39/43: margenes identicos con la fila a 0 ===")
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
        return (at - c[min(c, key=c.get)]) if at is not None else None, \
            min(c, key=c.get)
    # las varas del 43 bajo el cuerpo campeon (el mismo banco las midio)
    ESPERADO = {(1, 100): 0.20928, (3, 28): 0.49570,
                (4, 28): 0.49587, (5, 100): 0.39281}
    for (g, hp0), vara in ESPERADO.items():
        m, el = escena39(g, hp0)
        check(f"{g}g/hp0={hp0}: margen == vara v24 ({vara:+.5f})",
              m is not None and abs(m - vara) < 1e-4, f"{m:+.5f} · elige {el}")

    # ── 3. LA BRECHA, guardada reproducible (M=0,18; documento) ──────────
    print("\n=== 3. LA BRECHA DEL CANDADO, reproducida a M=0,18 ===")
    CAZ = (YO[0] + 2, YO[1]); BOT = (YO[0] + 3, YO[1])
    o3 = obs(300, YO, hp=25,
             agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                       "hp_band": "healthy"}],
             items=[{"id": "first_aid", "n": 1, "pos": list(BOT)}])
    o3["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
    res = {}
    A.MURO_K = 0.0                       # el 46 no tenia muro
    for nm, m in (("v24 (M=0)", 0.0), ("v25 (M=0,18)", 0.18)):
        A.ACOPIO_M = m
        el, c = mesa(mundo, o3)
        res[nm] = el
        orden = sorted(c.items(), key=lambda kv: kv[1])[:3]
        print(f"     {nm}: elige `{el}`  "
              + "  ".join(f"{k}={v:.5f}" for k, v in orden))
    A.ACOPIO_M = 0.0
    check("v24 HUYE (move_SW/NW)", str(res["v24 (M=0)"]).startswith("move_"),
          res["v24 (M=0)"])
    check("v25 a M=0,18 COMPRABA RIESGO (ir_objeto tras el cazador) — la brecha",
          res["v25 (M=0,18)"] == "ir_objeto", res["v25 (M=0,18)"])

    # ── 4. el intervalo imposible ─────────────────────────────────────────
    print("\n=== 4. EL INTERVALO IMPOSIBLE ===")
    o4 = obs(300, YO, hp=100,
             items=[{"id": "rations", "n": 1, "pos": [YO[0] - 2, YO[1]]},
                    {"id": "first_aid", "n": 1, "pos": [YO[0] - 5, YO[1] - 1]}])
    def destino_p1():
        memx = A.Memoria(); memx.hp_max = 100; memx.observa(o4, mundo, 300)
        return D._mejor_objeto(YO, mundo, memx, o4, 300)
    A.ACOPIO_M = 0.02
    el_muro, _ = mesa(mundo, o3)
    A.ACOPIO_M = 0.03
    el_cae, _ = mesa(mundo, o3)
    A.ACOPIO_M = 0.12
    d12 = destino_p1()
    A.ACOPIO_M = 0.18
    d18 = destino_p1()
    A.ACOPIO_M = 0.0
    check("a M=0,02 el muro AGUANTA (huye)", str(el_muro).startswith("move_"),
          el_muro)
    check("a M=0,03 el muro CAE (el limite es ~0,025)", el_cae == "ir_objeto",
          el_cae)
    check("en calma con competencia, a M=0,12 el botiquin AUN no llama",
          d12 == (YO[0] - 2, YO[1]), f"destino {d12}")
    check("...y a M=0,18 por fin llama — el intervalo [0,03..0,18) esta vacio",
          d18 == (YO[0] - 5, YO[1] - 1), f"destino {d18}")

    # restaurar el estado sellado vigente antes del determinismo
    A.ACOPIO_M, A.MURO_K = _M0, _K0

    # ── 5. determinismo ───────────────────────────────────────────────────
    print("\n=== 5. determinismo 3/3 ===")
    firmas = set()
    for _ in range(3):
        acc = []
        for oo in (o3, o4):
            A.ACOPIO_M, A.MURO_K = _M0, _K0
            el, c = mesa(mundo, oo)
            acc.append((el, json.dumps(c, sort_keys=True)))
        firmas.add(json.dumps(acc))
    check("3 corridas identicas", len(firmas) == 1, f"{len(firmas)} firma(s)")

    A.ACOPIO_M, A.MURO_K = _M0, _K0
    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
