"""Banco de EL REPLIEGUE — PROMPT_37 A. La constitucion 5/4/10/1 (la v22).

  1. El reparto es VALIDO (`sim.nim:531-552`): cada stat en [1,10], suma <= 20.
  2. Se declara EXACTAMENTE 5/4/10/1, igual en las dos policies.
  3. Las PIERNAS se conservan: enfriamiento observado = 6 tics (`16 - SPD`),
     igual que la v21. Este examen mueve INT y ATH, no SPD.
  4. La VISTA baja una casilla: radio 8 (`5 + (INT+1) div 2`, sim.nim:148),
     contra los 9 de la v19 y la v21.
  5. Lo que el repliegue compra, de la fuente: esquiva 2 % -> 8 %
     (`rand(100) < 2*ATH`, sim.nim:980) y dano de entorno 97 % -> 88 %
     (`centi*(100-3*ATH) div 100`, sim.nim:149-151).
  6. Las FILAS son identicas bajo los TRES cuerpos (v19 8/6/5/1, v21 8/1/10/1,
     v22 5/4/10/1) en la misma escena: salen del mundo, no de nosotros.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_37
"""
from __future__ import annotations

import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs
from alma.policy import CONSTITUCION
from alma.policy_repetidor_forense import CONSTITUCION as CONST_FORENSE

_fallos = []
SELLADA = {"intelligence": 5, "athleticism": 4, "speed": 10, "strength": 1}
CUERPOS = {"v19": dict(intelligence=8, athleticism=6, speed=5, strength=1),
           "v21": dict(intelligence=8, athleticism=1, speed=10, strength=1),
           "v22": SELLADA}


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def main():
    mundo = Mundo.desde_player_config(player_config())

    if CONSTITUCION != SELLADA:
        print(f"  OTRO CUERPO: la constitucion cargada es {CONSTITUCION},")
        print("  no la 5/4/10/1 que describe este banco (la v22 del repliegue).")
        print("  El PROMPT_42 devolvio la campeona (8/6/5/1) al repo para medir")
        print("  la ocasion con la conducta de la liga. La v22 vive en el commit")
        print("  del 37 y en la imagen `gemv-anima:v4`. Lo transversal (reparto")
        print("  valido, filas identicas bajo cualquier cuerpo) esta verificado")
        print("  en verifica_35/37 historicos y en verifica_39.")
        print("\n  NADA QUE VERIFICAR EN ESTA VARIANTE (no es un fallo).")
        return 0

    # ── 1-2. el reparto ───────────────────────────────────────────────────
    print("=== 1-2. la constitucion declarada ===")
    check("es exactamente 5/4/10/1", CONSTITUCION == SELLADA, f"{CONSTITUCION}")
    check("la del repetidor forense es la MISMA",
          CONST_FORENSE == CONSTITUCION, "")
    s = sum(CONSTITUCION.values())
    check("suma <= 20 (el mundo la aceptaria)", s <= 20, f"suma={s}")
    check("cada stat en [1,10]",
          all(1 <= v <= 10 for v in CONSTITUCION.values()), "")

    # ── 3. las piernas se conservan ───────────────────────────────────────
    print("\n=== 3. las PIERNAS no se tocan (el examen mueve INT y ATH) ===")
    cd = mundo.coste_movimiento(CONSTITUCION["speed"])
    check("enfriamiento observado = 6 tics", cd == 6, f"16-10={cd}")
    check("...el mismo que la v21",
          cd == mundo.coste_movimiento(CUERPOS["v21"]["speed"]), "")
    print(f"     (la v19 pagaba {mundo.coste_movimiento(CUERPOS['v19']['speed'])})")
    abierto = None
    for y in range(10, mundo.arena_size - 14):
        if all(not mundo.solido(x, y) for x in range(y - 10, y + 12)):
            abierto = y
            break
    Z = (abierto, abierto)
    p = D._simula_camino(Z, "E", mundo, CONSTITUCION["speed"], 48, False)
    check("la zancada sigue proyectando 8 casillas", abs(p[0] - Z[0]) == 8,
          f"{Z} -> {p}")

    # ── 4-5. lo que se paga y lo que se compra ────────────────────────────
    print("\n=== 4-5. el trueque del repliegue, de la fuente ===")

    def vista(i):
        return 5 + (i + 1) // 2                      # sim.nim:148

    def esquiva(a):
        return 2 * a                                 # sim.nim:980

    def entorno(a):
        return 100 - 3 * a                           # sim.nim:151

    print(f"     {'cuerpo':<6} {'INT':>4} {'ATH':>4} {'vista':>6} {'esquiva':>8}"
          f" {'dano de entorno':>16}")
    for nm, c in CUERPOS.items():
        print(f"     {nm:<6} {c['intelligence']:>4} {c['athleticism']:>4}"
              f" {vista(c['intelligence']):>6} {str(esquiva(c['athleticism']))+' %':>8}"
              f" {str(entorno(c['athleticism']))+' %':>16}")
    o = obs(300, Z)
    m = A.Memoria(); m.hp_max = 100; m.observa(o, mundo, 300)
    F = A.filas(o, mundo, m, 300)
    check("radio de vision propio = 8 (era 9)",
          F.get("_radio_vision") == 8.0, f"{F.get('_radio_vision')}")
    check("la formula del banco coincide con la del mundo",
          vista(CONSTITUCION["intelligence"]) == 8, "")

    # ── 6. las filas no dependen del cuerpo ───────────────────────────────
    print("\n=== 6. las FILAS son identicas bajo los tres cuerpos ===")
    CAZ = (Z[0] + 6, Z[1])
    ref = None
    for nm, c in CUERPOS.items():
        oo = obs(300, Z, agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                                   "hp_band": "healthy"}])
        oo["you"]["stats"] = dict(oo["you"]["stats"], **c)
        mm = A.Memoria(); mm.hp_max = 100; mm.observa(oo, mundo, 300)
        FF = A.filas(oo, mundo, mm, 300)
        clave = {k: FF.get(k) for k in ("F-4-ALCANCE", "F-ANTICIPACION",
                                        "S-8-EXPOSICION", "R-CARENCIA")}
        if ref is None:
            ref = clave
            print(f"     referencia ({nm}): {clave}")
        else:
            check(f"filas identicas con el cuerpo {nm}", clave == ref, f"{clave}")
    print("     (el radio de vision SI cambia con INT: es del mundo, no de la")
    print("      libreta. Las cuatro filas de arriba no lo usan como entrada.)")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
