"""Banco de LA FOTO HONESTA — PROMPT_23 A. Escenas sinteticas.

  1. La escena del 22A: con el golpe al hermano previsto (100 -> 65),
     S-DANO-PAREJA SUBE en esa foto (ya no queda congelada en 0,10224).
  2. La escena real de s228 reconstruida: los cuatro candidatos ya NO empatan;
     atacar al hermano es estrictamente PEOR que atacar a un hostil y que
     quedarse quieto. El sorteo desaparece por GRADIENTE, no por prohibicion.
  3. Un golpe previsto a un HOSTIL no mueve las filas de pareja.
  4. La muerte prevista del hermano (golpe que lo dejaria a 0) carga
     S-MUERTE-PAREJA en la foto.
  5. La defensa contra hostiles sigue intacta (escena 5a del PROMPT_21).

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_23
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
    PAR = mundo.teammate_slot
    YO = (24, 24)

    # ── 1. la escena del 22A ───────────────────────────────────────────────
    print("=== 1. la escena del 22A: golpe previsto al hermano ===")
    o = obs(300, YO, hand={"id": "sword", "durability": 40},
            agentes=[{"slot": PAR, "team": "A", "pos": [25, 24],
                      "hp_band": "healthy"}])
    o["you"]["damage_taken"] = [{"source": f"P{PAR}", "amount": 20.0}]
    m = A.Memoria(); m.hp_max = 100; m.roce_B = 0.6
    m.observa(o, mundo, 300)
    F0 = A.filas(o, mundo, m, 300)
    ob2 = D._obs_prevista(o, mundo, m, 300, YO, 100.0,
                          list(o["you"]["pack"]), o["you"]["hand"], True,
                          golpe=(PAR, 35.0))
    F1 = A.filas(ob2, mundo, m, 300)
    herm = next(a for a in ob2["visible"]["agents"] if a.get("slot") == PAR)
    print(f"     hp previsto del hermano: {herm.get('_hp_est')}")
    print(f"     S-DANO-PAREJA: ahora {F0['S-DANO-PAREJA']:.5f}  ->  "
          f"en la foto {F1['S-DANO-PAREJA']:.5f}")
    check("S-DANO-PAREJA SUBE en la foto del golpe al hermano",
          F1["S-DANO-PAREJA"] > F0["S-DANO-PAREJA"] + 1e-9, "")

    # ── 3. un golpe a un HOSTIL no mueve las filas de pareja ───────────────
    print("\n=== 3. golpe previsto a un HOSTIL ===")
    o3 = obs(300, YO, hand={"id": "sword", "durability": 40},
             agentes=[{"slot": PAR, "team": "A", "pos": [23, 24],
                       "hp_band": "healthy"},
                      {"slot": 9, "team": "D", "pos": [25, 24],
                       "hp_band": "healthy"}])
    o3["you"]["damage_taken"] = [{"source": "P9", "amount": 20.0}]
    m3 = A.Memoria(); m3.hp_max = 100; m3.roce_B = 0.6
    m3.observa(o3, mundo, 300)
    F3a = A.filas(o3, mundo, m3, 300)
    ob3 = D._obs_prevista(o3, mundo, m3, 300, YO, 100.0,
                          list(o3["you"]["pack"]), o3["you"]["hand"], True,
                          golpe=(9, 35.0))
    F3b = A.filas(ob3, mundo, m3, 300)
    check("pegando a un hostil, S-DANO-PAREJA no se mueve",
          abs(F3b["S-DANO-PAREJA"] - F3a["S-DANO-PAREJA"]) < 1e-12,
          f"{F3a['S-DANO-PAREJA']:.5f} -> {F3b['S-DANO-PAREJA']:.5f}")
    check("...y S-MUERTE-PAREJA sigue en 0",
          F3b["S-MUERTE-PAREJA"] == 0.0, "")

    # ── 4. la muerte prevista del hermano ──────────────────────────────────
    print("\n=== 4. el golpe que lo mataria ===")
    o4 = obs(300, YO, hand={"id": "sword", "durability": 40},
             agentes=[{"slot": PAR, "team": "A", "pos": [25, 24],
                       "hp_band": "critical"}])
    o4["you"]["damage_taken"] = [{"source": f"P{PAR}", "amount": 20.0}]
    m4 = A.Memoria(); m4.hp_max = 100; m4.roce_B = 0.6
    m4.observa(o4, mundo, 300)
    F4a = A.filas(o4, mundo, m4, 300)
    ob4 = D._obs_prevista(o4, mundo, m4, 300, YO, 100.0,
                          list(o4["you"]["pack"]), o4["you"]["hand"], True,
                          golpe=(PAR, 999.0))
    F4b = A.filas(ob4, mundo, m4, 300)
    print(f"     hp previsto: {next(a for a in ob4['visible']['agents'] if a['slot']==PAR).get('_hp_est')}")
    print(f"     S-MUERTE-PAREJA: ahora {F4a['S-MUERTE-PAREJA']:.5f}  ->  "
          f"en la foto {F4b['S-MUERTE-PAREJA']:.5f}   duelo={F4b.get('_duelo')}")
    check("la muerte prevista del hermano CARGA S-MUERTE-PAREJA",
          F4b["S-MUERTE-PAREJA"] > 0.0 and F4a["S-MUERTE-PAREJA"] == 0.0, "")
    check("y se marca como muerte PREVISTA, no recordada",
          (F4b.get("_duelo") or {}).get("prevista") is True, "")

    # ── 2. la escena real de s228 ──────────────────────────────────────────
    print("\n=== 2. la escena real de s228 t453: ¿siguen empatando? ===")
    # tres agresores activos, S-7 saturada; hermano en NE, P15 en E, P4 en SW
    # NOTA: la escena real llevaba CERBATANA, pero el fixture sintetico del
    # banco no trae `blowgun` ni `darts` (hueco arrastrado del PROMPT_18). Se
    # usa el ARCO, que si esta en el catalogo y tiene alcance de sobra (8) para
    # los tres agresores: la geometria del tic real se conserva.
    P = (27, 24)
    o2 = obs(300, P, hp=26, hand={"id": "bow", "durability": 40},
             pack=[{"id": "arrows", "n": 12}, None],
             agentes=[{"slot": PAR, "team": "A", "pos": [28, 23],
                       "hp_band": "healthy"},
                      {"slot": 4, "team": "C", "pos": [25, 26],
                       "hp_band": "healthy"},
                      {"slot": 15, "team": "H", "pos": [28, 24],
                       "hp_band": "healthy"}])
    o2["you"]["damage_taken"] = [{"source": f"P{PAR}", "amount": 8.0},
                                 {"source": "P4", "amount": 26.4},
                                 {"source": "P15", "amount": 39.6}]
    m2 = A.Memoria(); m2.hp_max = 100; m2.roce_B = 0.72
    # y el enfriamiento de movimiento del tic real (move_ready_in = 10), que es
    # lo que dejaba la mesa en cuatro candidatos
    o2["you"]["move_ready_in"] = 10
    m2.observa(o2, mundo, 300)
    F2 = A.filas(o2, mundo, m2, 300)
    print(f"     S-7-AGRESOR = {F2['S-7-AGRESOR']:.5f}  (tope {A.AGRESOR_CAP_TOTAL})")
    _a, rad = D.decide(o2, mundo, m2, 300, bloqueos=D.Bloqueos())
    cs = rad.get("candidatos") or {}
    dd = {k: (v["d"] if isinstance(v, dict) else v) for k, v in cs.items()}
    for k in sorted(dd, key=lambda k: dd[k]):
        quien = ""
        if k == "atacar_NE":
            quien = "  <-- EL HERMANO"
        elif k in ("atacar_E", "atacar_SW"):
            quien = "  (hostil)"
        print(f"     {k:12s} d={dd[k]:.5f}{quien}")
    print(f"     ELIGE: {rad['elegido']}")
    herm_k = "atacar_NE"
    hostiles = [k for k in dd if k.startswith("atacar_") and k != herm_k]
    if herm_k in dd and hostiles:
        check("atacar al HERMANO es estrictamente PEOR que atacar a un hostil",
              all(dd[herm_k] > dd[h] + 1e-9 for h in hostiles),
              f"hermano {dd[herm_k]:.5f} vs hostiles "
              f"{ {h: round(dd[h],5) for h in hostiles} }")
        check("...y peor que quedarse quieto",
              dd[herm_k] > dd.get("noop", 0) + 1e-9,
              f"hermano {dd[herm_k]:.5f} vs noop {dd.get('noop'):.5f}")
        check("el elegido NO es el hermano", rad["elegido"] != herm_k, "")
    else:
        check("la escena reproduce los candidatos del 22A",
              False, f"candidatos={sorted(dd)}")

    # ── 5. la defensa contra hostiles sigue intacta ────────────────────────
    print("\n=== 5. la escena 5a del 21: el verdugo sin botin ===")
    abierto = None
    for y in range(10, mundo.arena_size - 14):
        if all(not mundo.solido(x, y) for x in range(y - 8, y + 14)):
            abierto = y
            break
    Z = (abierto, abierto)
    o5 = obs(300, Z, agentes=[{"slot": 15, "team": "D",
                               "pos": [Z[0] + 6, Z[1]], "hp_band": "healthy"}])
    m5 = A.Memoria(); m5.hp_max = 100; m5.observa(o5, mundo, 300)
    _a5, rad5 = D.decide(o5, mundo, m5, 300)
    dd5 = {k: (v["d"] if isinstance(v, dict) else v)
           for k, v in (rad5.get("candidatos") or {}).items()}
    al = min(dd5[k] for k in dd5 if k.split("_")[-1] in ("W", "NW", "SW")
             and k.startswith(("move_", "paso_")))
    print(f"     elegido {rad5['elegido']} · mejor alejarse {al:.5f} · "
          f"quieto {dd5['noop']:.5f}")
    check("la huida del 21 sigue ganando a quedarse", al < dd5["noop"], "")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
