"""Banco de LA CESION QUE CADUCA — PROMPT_24 A. Escenas sinteticas.

  1. La escena de s301: botiquin cedido en t; a t+720 sin recogida, vuelve a
     ser mio y `coger` / `ir_objeto` lo valoran otra vez.
  2. ANTES del plazo el veto aguanta ENTERO: ni una recogida propia en
     t..t+719 (la leccion del PROMPT_12: que la caducidad no reabra la
     oscilacion dar-coger).
  3. Si el herido lo recoge dentro del plazo: todo como hoy.
  4. Si el herido muere o se cura antes del plazo: el veto se levanta al
     momento, como hoy.
  5. Lo soltado que NO es cesion no se ve afectado en nada.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_24
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
    CURA = mundo.id_botiquin
    YO = (24, 24)
    PLAZO = int(A.CESION_CADUCA_S * mundo.tick_rate)
    print(f"  plazo sellado: {A.CESION_CADUCA_S} s = {PLAZO} tics\n")

    def escena(tick, banda="hurt", pos=YO, items=True, pareja=(25, 24)):
        return obs(tick, pos,
                   agentes=([{"slot": PAR, "team": "A", "pos": list(pareja),
                              "hp_band": banda}] if pareja else []),
                   items=([{"id": CURA, "pos": list(YO), "n": 1}] if items else []),
                   pack=[{"id": CURA, "n": 1}, None])

    def memoria_con_cesion(t0=300):
        o = escena(t0)
        m = A.Memoria(); m.hp_max = 100; m.roce_B = 0.6
        m.observa(o, mundo, t0)
        m.cedidos[YO] = {"item": CURA, "tick": t0}
        return m

    # ── 1. caduca a los 720 tics ───────────────────────────────────────────
    print("=== 1. la escena de s301: sin recogida, a los 720 tics vuelve a ser mio ===")
    m = memoria_con_cesion(300)
    o_antes = escena(300 + PLAZO - 1)
    m.observa(o_antes, mundo, 300 + PLAZO - 1)
    c_antes = dict(D.candidatos(o_antes, mundo, m, 300 + PLAZO - 1))
    check("a t+719 sigue cedido: `coger` NO esta",
          "coger" not in c_antes and YO in m.cedidos,
          f"cedidos={list(m.cedidos)}")
    o_desp = escena(300 + PLAZO)
    m.observa(o_desp, mundo, 300 + PLAZO)
    c_desp = dict(D.candidatos(o_desp, mundo, m, 300 + PLAZO))
    check("a t+720 CADUCA: vuelve a ser mio",
          not m.cedidos, f"cedidos={list(m.cedidos)}")
    check("...y `coger` vuelve a la mesa", "coger" in c_desp,
          f"cands={sorted(k for k in c_desp if k in ('coger','ir_objeto'))}")
    check("...y vuelve a ser objetivo de `ir_objeto`",
          D._mejor_objeto(YO, mundo, m, o_desp, 300 + PLAZO) == YO,
          f"mejor_objeto={D._mejor_objeto(YO, mundo, m, o_desp, 300 + PLAZO)}")
    # y la cache de fuentes se ha enterado
    check("la cache de fuentes se entera de la caducidad",
          any(p == YO for p, _n in m.fuentes()),
          f"¿esta {YO} en las fuentes? "
          f"{any(p == YO for p, _n in m.fuentes())}")

    # ── 2. antes del plazo el veto aguanta ENTERO ──────────────────────────
    print("\n=== 2. ni una recogida propia en los 719 tics del veto ===")
    m2 = memoria_con_cesion(300)
    recogidas = 0
    for t in range(300, 300 + PLAZO):
        o = escena(t)
        m2.observa(o, mundo, t)
        _a, rad = D.decide(o, mundo, m2, t)
        if rad["elegido"] == "coger":
            recogidas += 1
    check("cero recogidas propias durante el veto (no se reabre la oscilacion)",
          recogidas == 0, f"recogidas={recogidas}")
    check("y al final del veto la cesion sigue viva",
          YO in m2.cedidos, f"cedidos={list(m2.cedidos)}")

    # ── 3. si el herido lo recoge dentro del plazo ─────────────────────────
    print("\n=== 3. el herido lo recoge dentro del plazo ===")
    m3 = memoria_con_cesion(300)
    # el objeto desaparece del suelo (se lo llevo) y el hermano sigue herido
    o3 = escena(300 + 100, items=False)
    m3.observa(o3, mundo, 300 + 100)
    c3 = dict(D.candidatos(o3, mundo, m3, 300 + 100))
    check("sin objeto en el suelo no hay `coger` (nada que recuperar)",
          "coger" not in c3, "")
    check("la cesion sigue anotada mientras no caduque ni cambie su estado",
          YO in m3.cedidos, f"cedidos={list(m3.cedidos)}")

    # ── 4. muerte / curacion levantan el veto al momento ───────────────────
    print("\n=== 4. las salidas de siempre siguen intactas ===")
    m4 = memoria_con_cesion(300)
    o4 = escena(300 + 50, banda="healthy")
    m4.observa(o4, mundo, 300 + 50)
    check("si se CURA del todo, el veto se levanta al momento",
          not m4.cedidos, f"cedidos={list(m4.cedidos)}")
    m5 = memoria_con_cesion(300)
    m5.pareja_muerta = True
    o5 = escena(300 + 50, pareja=None)
    m5.observa(o5, mundo, 300 + 50)
    check("si MUERE, el veto se levanta al momento",
          not m5.cedidos, f"cedidos={list(m5.cedidos)}")

    # ── 5. lo soltado que no es cesion ─────────────────────────────────────
    print("\n=== 5. lo soltado que NO es cesion no se toca ===")
    m6 = A.Memoria(); m6.hp_max = 100
    o6 = obs(300, YO, items=[{"id": "sword", "pos": list(YO), "n": 1}])
    m6.observa(o6, mundo, 300)
    c6 = dict(D.candidatos(o6, mundo, m6, 300))
    check("una espada en el suelo (no cedida) es cogible desde el primer tic",
          "coger" in c6 and not m6.cedidos, f"cedidos={list(m6.cedidos)}")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
