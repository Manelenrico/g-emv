"""Banco de PIERNAS Y VISTA — PROMPT_35 A. La constitucion 8/1/10/1.

  1. El reparto es VALIDO para el mundo: cada stat en [1,10] y suma <= 20
     (`sim.nim:531-552`, `submitAllocation`).
  2. Se declara EXACTAMENTE 8/1/10/1, y el mismo numero en las dos policies.
  3. El enfriamiento propio derivado es 6 tics (`16 - SPD`, sim.nim:147),
     y la zancada proyecta 8 casillas sobre la mirada de 48.
  4. Las filas NO cambian: F-4 y F-ANTICIPACION salen del MUNDO (posiciones,
     calendario del anillo), no de nuestra constitucion. Se comprueba con la
     misma escena bajo los dos cuerpos.
  5. El radio de vision que el alma se atribuye sube a 9 (INT 8 no cambia),
     y el radio hostil conservador tampoco se mueve.
  6. LO QUE EL CUERPO NUEVO SI CAMBIA, declarado y medido aqui: perseguido,
     `ir_centro` gana a los pasos de huida. Con SPD 5 ganaba un paso. Es
     conducta, no instrumento, y el gate 5a del 21 lo marca.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_35
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
SELLADA = {"intelligence": 8, "athleticism": 1, "speed": 10, "strength": 1}


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def main():
    mundo = Mundo.desde_player_config(player_config())

    if CONSTITUCION != SELLADA:
        print(f"  OTRO CUERPO: la constitucion cargada es {CONSTITUCION},")
        print(f"  no la 8/1/10/1 que describe este banco (la v21).")
        print("  El PROMPT_37 monto el repliegue 5/4/10/1 (v22) sobre la misma")
        print("  alma v19. La v21 vive en el commit del 35 y en `gemv-anima:v3`.")
        print("  Lo que este banco verificaba y SIGUE valiendo para cualquier")
        print("  cuerpo esta en `verifica_37`: reparto valido, enfriamiento")
        print("  derivado, vista derivada y filas identicas bajo todos ellos.")
        print("\n  NADA QUE VERIFICAR EN ESTA VARIANTE (no es un fallo).")
        return 0

    # ── 1-2. el reparto que se declara al mundo ───────────────────────────
    print("=== 1-2. la constitucion declarada ===")
    print("     CERTIFICADO (`sim.nim:531-552`, submitAllocation):")
    print("       if v < 1 or v > 10: return arRejectedInvalid")
    print("       if sum > 20:        return arRejectedInvalid")
    print("       primera asignacion valida GANA y queda `statsLocked`")
    check("la constitucion es exactamente 8/1/10/1",
          CONSTITUCION == SELLADA, f"{CONSTITUCION}")
    check("la del repetidor forense es la MISMA",
          CONST_FORENSE == CONSTITUCION, f"{CONST_FORENSE}")
    s = sum(CONSTITUCION.values())
    check("suma <= 20 (el mundo la aceptaria)", s <= 20, f"suma={s}")
    check("cada stat en [1,10]",
          all(1 <= v <= 10 for v in CONSTITUCION.values()), "")

    # ── 3. lo que compran las piernas ─────────────────────────────────────
    print("\n=== 3. el enfriamiento propio y la zancada ===")
    spd = CONSTITUCION["speed"]
    cd = mundo.coste_movimiento(spd)
    check("enfriamiento derivado = 6 tics (16 - SPD)", cd == 6, f"16-{spd}={cd}")
    print("     antes, con SPD 5: 11 tics. Casi la mitad.")
    abierto = None
    for y in range(10, mundo.arena_size - 14):
        if all(not mundo.solido(x, y) for x in range(y - 10, y + 12)):
            abierto = y
            break
    Z = (abierto, abierto)
    p10 = D._simula_camino(Z, "E", mundo, 10, 48, False)
    p5 = D._simula_camino(Z, "E", mundo, 5, 48, False)
    check("la zancada proyecta 8 casillas con SPD 10",
          abs(p10[0] - Z[0]) == 8, f"{Z} -> {p10}")
    check("...y proyectaba 4 con SPD 5", abs(p5[0] - Z[0]) == 4, f"{Z} -> {p5}")
    print("     la MIRADA no se ha tocado: sigue en 48 tics. Lo que cambia es")
    print("     cuantos pasos caben dentro, y eso lo dicta el cuerpo.")

    # ── 4. las filas no dependen de nuestra constitucion ──────────────────
    print("\n=== 4. las filas salen del MUNDO, no de nuestro cuerpo ===")
    CAZ = (Z[0] + 6, Z[1])
    o10 = obs(300, Z, agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                                "hp_band": "healthy"}])
    o5 = obs(300, Z, agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                              "hp_band": "healthy"}])
    o5["you"]["stats"] = dict(o5["you"]["stats"], speed=5, athleticism=6)
    m10 = A.Memoria(); m10.hp_max = 100; m10.observa(o10, mundo, 300)
    m5 = A.Memoria(); m5.hp_max = 100; m5.observa(o5, mundo, 300)
    F10 = A.filas(o10, mundo, m10, 300)
    F5 = A.filas(o5, mundo, m5, 300)
    for fila in ("F-4-ALCANCE", "F-ANTICIPACION", "S-8-EXPOSICION", "R-CARENCIA"):
        check(f"{fila} identica con los dos cuerpos",
              abs(F10.get(fila, 0) - F5.get(fila, 0)) < 1e-9,
              f"{F10.get(fila)} vs {F5.get(fila)}")

    # ── 5. la vista ───────────────────────────────────────────────────────
    print("\n=== 5. la vista, que NO se ha tocado (INT sigue en 8) ===")
    print("     CERTIFICADO `sim.nim:148`: visionRadius = 5 + (INT+1) div 2")
    check("radio de vision propio = 9", F10.get("_radio_vision") == 9.0,
          f"{F10.get('_radio_vision')}")
    check("radio hostil conservador intacto",
          F10.get("_radio_hostil") == F5.get("_radio_hostil"),
          f"{F10.get('_radio_hostil')}")

    # ── 6. lo que el cuerpo nuevo SI cambia ───────────────────────────────
    print("\n=== 6. la conducta que el cuerpo nuevo cambia (declarada) ===")
    _a, r10 = D.decide(o10, mundo, m10, 300)
    _b, r5 = D.decide(o5, mundo, m5, 300)
    print(f"     perseguido a 6 casillas: con SPD 10 elige `{r10['elegido']}`,")
    print(f"                              con SPD  5 elige `{r5['elegido']}`")
    print("     NO es un gate: es el hallazgo. El cuerpo veloz proyecta tambien")
    print("     la geodesica ocho casillas, asi que `ir_centro` entra mas hondo")
    print("     en el anillo y F-ANTICIPACION lo premia mas que a huir. El gate")
    print("     5a de `verifica_21` lo marca como FALLO a proposito: es una")
    print("     conducta sellada que el cuerpo nuevo altera, y se reporta.")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
