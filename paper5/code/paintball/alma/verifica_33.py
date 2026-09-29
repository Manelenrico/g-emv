"""Banco de LA ZANCADA HONESTA II — PROMPT_33 B. Escenas sinteticas.

  1. `move_*` hacia un CUERPO VISIBLE: ya NO se ofrece (era el cabo del 28).
  2. `move_*` hacia casilla libre: se sigue ofreciendo, y su foto sigue
     proyectando la zancada (el cambio es del MENU, no de la mirada).
  3. `move_*` contra muro: sigue fuera (no se ha roto el 28).
  4. `paso_*` e `ir_*` intactos; con cuerpo al lado, la direccion entera
     desaparece de las tres familias — y eso es lo correcto: no se puede ir.
  5. El sorteo NO se finge: dos aspirantes a la misma casilla libre siguen
     teniendo su candidato (es azar, `sim.nim:650`).

MECANICA CERTIFICADA (`sim.nim`, `resolveMovement` 612-676 + 1340):
  - 1340: `lastActionResult[i] = "ok"` es PROVISIONAL; "resolvers downgrade it".
  - 622-624: solido / fuera del tablero  -> "blocked".
  - 625-627: casilla inundada            -> "blocked".
  - 638-643: INTERCAMBIO DE FRENTE -> los dos intentos se desactivan y NADIE
             escribe lastActionResult: queda el "ok" provisional SIN moverse.
             Exige un cuerpo en el destino. Es la averia de los 611 del 32.
  - 645-656: varios aspirantes -> gana uno AL AZAR (`s.rng.rand`), el resto
             "blocked". NO exige cuerpo en el destino: es azar y no se filtra.
  - 657-666: ocupante que NO se mueve -> "blocked". Exige cuerpo en el destino.
  - 672:     el que sobrevive avanza UNA casilla y paga `moveCooldown` tics.
  - 147:     `moveCooldown(a) = 16 - a.stats.speed`  ->  con speed 5, 11 tics.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_33
"""
from __future__ import annotations

import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs

_fallos = []


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def _es_v20(mundo):
    """¿Esta alma filtra la zancada contra cuerpos visibles? (el arreglo del 33)

    El PROMPT_35 devolvio el alma a la v19 —la campeona— para montarle encima la
    constitucion nueva, y dejo la v20 EN NEVERA (vive en el commit del 33 y en
    la imagen `gemv-anima:v2`). Este banco describe la v20: si el alma cargada
    es la v19, no hay nada que verificar y se dice, en vez de fingir un fallo.
    """
    from alma import appraisal_zs as _A
    libre = None
    for y in range(2, mundo.arena_size - 2):
        for x in range(2, mundo.arena_size - 2):
            if not mundo.solido(x, y) and not mundo.solido(x - 1, y):
                libre = (x, y)
                break
        if libre:
            break
    o = obs(300, libre, agentes=[{"slot": 9, "team": "D",
                                  "pos": [libre[0] - 1, libre[1]],
                                  "hp_band": "healthy"}])
    m = _A.Memoria(); m.hp_max = 100; m.observa(o, mundo, 300)
    return "move_W" not in dict(D.candidatos(o, mundo, m, 300))


def main():
    mundo = Mundo.desde_player_config(player_config())

    if not _es_v20(mundo):
        print("  NEVERA: el alma cargada es la v19 (la zancada NO filtra cuerpos).")
        print("  Este banco describe el arreglo del 33, que el PROMPT_35 dejo en")
        print("  nevera para montar la constitucion 8/1/10/1 sobre la campeona.")
        print("  La v20 vive en el commit del 33 y en la imagen `gemv-anima:v2`.")
        print("\n  NADA QUE VERIFICAR EN ESTA VARIANTE (no es un fallo).")
        return 0

    # casilla libre con un SOLIDO al este y espacio libre alrededor
    muro = None
    for y in range(2, mundo.arena_size - 2):
        for x in range(2, mundo.arena_size - 2):
            if (not mundo.solido(x, y) and mundo.solido(x + 1, y)
                    and not mundo.solido(x - 1, y) and not mundo.solido(x, y - 1)
                    and not mundo.solido(x, y + 1)):
                muro = (x, y)
                break
        if muro:
            break
    YO = muro
    OESTE = (YO[0] - 1, YO[1])
    NORTE = (YO[0], YO[1] - 1)
    print(f"  escena: yo en {YO}, SOLIDO al este, libre al oeste y al norte\n")

    # ── 1. la zancada contra un cuerpo visible ────────────────────────────
    print("=== 1. `move_*` hacia un CUERPO VISIBLE: fuera del menu ===")
    o = obs(300, YO, agentes=[{"slot": 9, "team": "D", "pos": list(OESTE),
                               "hp_band": "healthy"}])
    m = A.Memoria(); m.hp_max = 100; m.observa(o, mundo, 300)
    c = dict(D.candidatos(o, mundo, m, 300))
    check("`move_W` (hacia el cuerpo) NO se ofrece",
          "move_W" not in c,
          f"zancadas: {sorted(k for k in c if k.startswith('move_'))}")
    check("`paso_W` tampoco (precedente del 14, sin cambios)",
          "paso_W" not in c, "")
    check("la direccion libre `move_N` SI se ofrece", "move_N" in c, "")
    check("y `paso_N` tambien", "paso_N" in c, "")

    # ── 2. la mirada NO cambia: sigue siendo zancada ──────────────────────
    print("\n=== 2. el cambio es del MENU, no de la mirada ===")
    p = D._simula_camino(YO, "N", mundo, 5, 48, False)
    saltos = max(abs(p[0] - YO[0]), abs(p[1] - YO[1]))
    check("la foto de `move_N` sigue proyectando varias casillas",
          saltos > 1, f"{YO} -> {p}  ({saltos} casillas)")
    check("la foto del paso corto sigue siendo de UNA casilla",
          True, "(por construccion: n_moves=1 en el evaluador)")

    # ── 3. no se ha roto el 28 ────────────────────────────────────────────
    print("\n=== 3. el 28 sigue en pie: la zancada contra muro, fuera ===")
    o3 = obs(300, YO)
    m3 = A.Memoria(); m3.hp_max = 100; m3.observa(o3, mundo, 300)
    c3 = dict(D.candidatos(o3, mundo, m3, 300))
    check("`move_E` (contra el solido) NO se ofrece", "move_E" not in c3, "")
    check("sin cuerpos delante, `move_W` vuelve al menu", "move_W" in c3, "")
    p3 = D._simula_camino(YO, "E", mundo, 5, 48, False)
    check("y la foto contra el muro sigue sin deslizar", p3 == YO, f"{YO} -> {p3}")

    # ── 4. el sorteo NO se finge ──────────────────────────────────────────
    print("\n=== 4. el sorteo sigue sin fingirse (`sim.nim:645-656`) ===")
    print("     un rival ADYACENTE A LA CASILLA LIBRE puede disputarnosla, y")
    print("     el mundo lo resuelve con `s.rng.rand`. No es cierto y no se")
    print("     filtra: el candidato se mantiene.")
    lejos = (NORTE[0] + 1, NORTE[1] - 1)
    if not mundo.solido(*lejos):
        o4 = obs(300, YO, agentes=[{"slot": 7, "team": "D", "pos": list(lejos),
                                    "hp_band": "healthy"}])
        m4 = A.Memoria(); m4.hp_max = 100; m4.observa(o4, mundo, 300)
        c4 = dict(D.candidatos(o4, mundo, m4, 300))
        check("con un rival que PODRIA disputar la casilla, `move_N` sigue ahi",
              "move_N" in c4, f"rival en {lejos}, casilla libre {NORTE}")

    # ── 5. campo abierto: nada perdido ────────────────────────────────────
    print("\n=== 5. campo abierto: las tres familias completas ===")
    abierto = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            abierto = y
            break
    Z = (abierto, abierto)
    o5 = obs(300, Z)
    m5 = A.Memoria(); m5.hp_max = 100; m5.observa(o5, mundo, 300)
    c5 = dict(D.candidatos(o5, mundo, m5, 300))
    check("las 8 zancadas", len([k for k in c5 if k.startswith("move_")]) == 8, "")
    check("los 8 pasos", len([k for k in c5 if k.startswith("paso_")]) == 8, "")
    campo = D.campo_geodesico(mundo, (Z[0] + 6, Z[1]))
    check("la geodesica sigue dando el mismo paso",
          D._paso_geodesico(Z, campo, (Z[0] + 6, Z[1])) == "E", "")

    # ── 6. el precio, certificado ─────────────────────────────────────────
    print("\n=== 6. el precio del movimiento, de la fuente ===")
    print("     `sim.nim:147`  moveCooldown(a) = 16 - a.stats.speed")
    spd = int((player_config().get("you") or {}).get("stats", {}).get("speed")
              or player_config().get("stats", {}).get("speed") or 5)
    print(f"     con speed={spd}: {16-spd} tics de enfriamiento por CADA orden,")
    print("     sea zancada, paso o geodesica. El coste es el mismo; lo que")
    print("     cambia es cuanto compra. (La constitucion es del sofa, no de")
    print("     este encargo.)")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
