"""Banco de LA ZANCADA HONESTA — PROMPT_28 A. Escenas sinteticas.

  1. `move_*` contra muro: NO se ofrece, y la foto ya no desliza.
  2. La escena del cazador del 21 (gate 5a) con un muro a la espalda: el paso
     elegido SALE de verdad.
  3. Los otros dos casos de bloqueo, contra la mecanica certificada:
     cuerpo visible y "ni solido ni cuerpo".
  4. `paso_*` e `ir_*` intactos.

MECANICA CERTIFICADA (`sim.nim:612-676`, `resolveMovement`):
  - solido / fuera del tablero  -> "blocked", SIN deslizar (linea 622-624)
  - casilla inundada            -> "blocked" (625-627)
  - intercambio de frente (i->j y j->i) -> los dos se cancelan (630-636)
  - varios aspirantes a la misma casilla -> gana uno AL AZAR, el resto
    "blocked" (638-655)
  - casilla ocupada por alguien que NO se mueve -> "blocked" (657-666)
  - en cualquier otro caso, el movimiento ocurre (668-676)

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_28
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


def main():
    mundo = Mundo.desde_player_config(player_config())

    # una casilla libre con un SOLIDO al este
    muro = None
    for y in range(2, mundo.arena_size - 2):
        for x in range(2, mundo.arena_size - 2):
            if (not mundo.solido(x, y) and mundo.solido(x + 1, y)
                    and not mundo.solido(x - 1, y) and not mundo.solido(x, y - 1)):
                muro = (x, y)
                break
        if muro:
            break
    YO = muro
    print(f"  escena: yo en {YO}, SOLIDO al este en {(YO[0]+1, YO[1])}\n")

    # ── 1. el menu y la foto ───────────────────────────────────────────────
    print("=== 1. move_* contra muro: fuera del menu, y la foto no desliza ===")
    o = obs(300, YO)
    m = A.Memoria(); m.hp_max = 100; m.observa(o, mundo, 300)
    cands = dict(D.candidatos(o, mundo, m, 300))
    check("`move_E` (contra el muro) NO se ofrece",
          "move_E" not in cands,
          f"zancadas: {sorted(k for k in cands if k.startswith('move_'))}")
    check("`move_W` (libre) sigue ofreciendose", "move_W" in cands, "")
    check("`paso_E` tampoco se ofrece (precedente del 14)",
          "paso_E" not in cands, "")

    # la foto: ya no desliza
    p_desliz = D._simula_camino(YO, "E", mundo, 5, 48, False)
    check("la foto de ir al este NO avanza (el mundo bloquea, no desliza)",
          p_desliz == YO, f"{YO} -> {p_desliz}")
    p_libre = D._simula_camino(YO, "W", mundo, 5, 48, False)
    check("la foto de ir al oeste SI avanza", p_libre != YO, f"{YO} -> {p_libre}")

    # ── 2. el cazador con un muro a la espalda ─────────────────────────────
    print("\n=== 2. el verdugo del 21, con el muro a la espalda ===")
    # el cazador al OESTE: huir "hacia atras" seria al ESTE, que es el muro
    CAZ = (YO[0] - 6, YO[1])
    o2 = obs(300, YO, agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                                "hp_band": "healthy"}])
    m2 = A.Memoria(); m2.hp_max = 100; m2.observa(o2, mundo, 300)
    _a, rad = D.decide(o2, mundo, m2, 300)
    dd = {k: (v["d"] if isinstance(v, dict) else v)
          for k, v in (rad.get("candidatos") or {}).items()}
    el = rad["elegido"]
    print(f"     elegido: {el}")
    print(f"     mesa: { {k: round(v,5) for k,v in sorted(dd.items(), key=lambda kv: kv[1])[:5]} }")
    if el.startswith(("move_", "paso_")):
        d = el.split("_")[-1]
        dx, dy = D.DIRS[d]
        q = (YO[0] + dx, YO[1] + dy)
        check("el paso elegido SALE de verdad (casilla no solida)",
              not mundo.solido(*q), f"{el} -> {q}")
    else:
        check("el elegido no es una zancada contra el muro",
              not el.startswith("move_E"), f"eligio {el}")

    # ── 3. los otros dos casos, contra la mecanica certificada ─────────────
    print("\n=== 3. cuerpo visible y 'ni solido ni cuerpo' ===")
    print("     CERTIFICADO (sim.nim:657-666): casilla ocupada por alguien que")
    print("     NO se mueve -> 'blocked'; si el ocupante se mueve, el paso SI")
    print("     ocurre. El bloqueo por cuerpo es CONDICIONAL, no cierto.")
    print("     CERTIFICADO (sim.nim:638-655): varios aspirantes a la misma")
    print("     casilla -> gana uno AL AZAR. No es predecible ni por nosotros")
    print("     ni por nadie: es `s.rng.rand`.")
    libre = (YO[0] - 1, YO[1])
    o3 = obs(300, YO, agentes=[{"slot": 9, "team": "D", "pos": list(libre),
                                "hp_band": "healthy"}])
    m3 = A.Memoria(); m3.hp_max = 100; m3.observa(o3, mundo, 300)
    c3 = dict(D.candidatos(o3, mundo, m3, 300))
    check("con un CUERPO al oeste, `move_W` SIGUE ofreciendose "
          "(el bloqueo es condicional, no cierto)",
          "move_W" in c3, "")
    check("...pero `paso_W` no (el paso corto es conservador desde el 15)",
          "paso_W" not in c3, "")
    print("     -> declarado: la zancada solo filtra lo CIERTO (solidos). Los")
    print("        cuerpos y el sorteo de casilla no son ciertos, y no se")
    print("        fingen. Es la misma disciplina de R1.")

    # ── 4. paso_ e ir_ intactos ────────────────────────────────────────────
    print("\n=== 4. paso_* e ir_* intactos ===")
    abierto = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            abierto = y
            break
    Z = (abierto, abierto)
    o4 = obs(300, Z)
    m4 = A.Memoria(); m4.hp_max = 100; m4.observa(o4, mundo, 300)
    c4 = dict(D.candidatos(o4, mundo, m4, 300))
    check("en campo abierto estan los 8 pasos",
          len([k for k in c4 if k.startswith("paso_")]) == 8, "")
    check("y las 8 zancadas", len([k for k in c4 if k.startswith("move_")]) == 8, "")
    campo = D.campo_geodesico(mundo, (Z[0] + 6, Z[1]))
    check("la geodesica sigue dando el mismo paso",
          D._paso_geodesico(Z, campo, (Z[0] + 6, Z[1])) == "E", "")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
