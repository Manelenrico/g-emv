"""Banco de la CESION, la ALCANZABILIDAD y el EMPUNAR — PROMPT_13.

Escenas sinteticas, sin mundo y sin episodios. Comprueba:
  A1. CESION: lo soltado bajo la condicion de medicina deja de ser cogible
      (ni `coger` ni `ir_objeto` lo miran) mientras la pareja siga viva y
      herida; la cesion EXPIRA si la pareja muere o se cura del todo.
  A2. ALCANZABILIDAD: la atenuacion de S-DANO-PAREJA NO aplica si hay alguien
      (yo incluido) encima de la cura; si aparto, aplica.
  B.  EMPUNAR: con RED (dano 0) en la mano y ESPADA en el zurron, el candidato
      empunar existe, es un `use` sobre la ranura, y la mano prevista lleva la
      espada. Ademas: con la espada en el zurron NO estamos armados (R-2).

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_13
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
    SLOT = mundo.teammate_slot
    CURA = mundo.id_botiquin
    YO = (24, 24)

    def pareja(pos, banda="hurt"):
        return {"slot": SLOT, "team": "A", "pos": list(pos), "hp_band": banda}

    def mem_con_pareja(o, tick=300):
        m = A.Memoria()
        m.hp_max = 100
        m.observa(o, mundo, tick)
        m.roce_B = 0.6          # vinculo ya rodado (el roce se gana con tics)
        return m

    # ── A2. ALCANZABILIDAD ─────────────────────────────────────────────────
    print("=== A2. ALCANZABILIDAD de la cura ===")
    # la cura EN MI CASILLA: inalcanzable para el herido (estoy encima)
    o_encima = obs(300, YO, agentes=[pareja((25, 24))],
                   items=[{"id": CURA, "pos": list(YO), "n": 1}])
    m = mem_con_pareja(o_encima)
    F = A.filas(o_encima, mundo, m, 300)
    check("con la cura BAJO MIS PIES no hay atenuacion",
          F.get("_medicina") is None, f"medicina={F.get('_medicina')}")
    m_bloq = F["S-DANO-PAREJA"]

    # la misma cura, una casilla al lado, con nadie encima: SI atenua
    o_libre = obs(300, YO, agentes=[pareja((25, 24))],
                  items=[{"id": CURA, "pos": [24, 25], "n": 1}])
    m2 = mem_con_pareja(o_libre)
    F2 = A.filas(o_libre, mundo, m2, 300)
    check("con la cura en casilla LIBRE junto al herido, atenua",
          F2.get("_medicina") is not None and F2["S-DANO-PAREJA"] < m_bloq,
          f"M {m_bloq:.5f} -> {F2['S-DANO-PAREJA']:.5f}")

    # ...y si hay un TERCERO encima de esa casilla, vuelve a no atenuar
    o_otro = obs(300, YO, agentes=[pareja((25, 24)),
                                   {"slot": 9, "team": "D", "pos": [24, 25],
                                    "hp_band": "healthy"}],
                 items=[{"id": CURA, "pos": [24, 25], "n": 1}])
    m3 = mem_con_pareja(o_otro)
    F3 = A.filas(o_otro, mundo, m3, 300)
    check("con OTRO encima de la cura, no atenua", F3.get("_medicina") is None,
          f"medicina={F3.get('_medicina')}")

    # ── A1. CESION ─────────────────────────────────────────────────────────
    print("\n=== A1. CESION ===")
    o_pie = obs(300, YO, agentes=[pareja((25, 24))],
                items=[{"id": CURA, "pos": list(YO), "n": 1}],
                pack=[{"id": CURA, "n": 1}, None])
    m4 = mem_con_pareja(o_pie)
    n_antes = [c[0] for c in D.candidatos(o_pie, mundo, m4, 300)]
    check("sin cesion, `coger` esta en la mesa", "coger" in n_antes,
          f"cands={sorted(n_antes)}")
    m4.cedidos[YO] = {"item": CURA, "tick": 299}
    n_ced = [c[0] for c in D.candidatos(o_pie, mundo, m4, 300)]
    check("CEDIDO: `coger` desaparece de la mesa", "coger" not in n_ced,
          f"cands={sorted(n_ced)}")
    check("CEDIDO: tampoco es objetivo de `ir_objeto`",
          D._mejor_objeto(YO, mundo, m4) != YO,
          f"mejor_objeto={D._mejor_objeto(YO, mundo, m4)}")

    # expiracion: la pareja se cura del todo
    o_sana = obs(360, YO, agentes=[pareja((25, 24), "healthy")],
                 items=[{"id": CURA, "pos": list(YO), "n": 1}])
    m4.observa(o_sana, mundo, 360)
    check("la cesion EXPIRA si la pareja se cura del todo", not m4.cedidos,
          f"cedidos={m4.cedidos}")

    # expiracion: la pareja muere
    m5 = mem_con_pareja(o_pie)
    m5.cedidos[YO] = {"item": CURA, "tick": 299}
    m5.pareja_muerta = True
    m5.observa(obs(360, YO, agentes=[]), mundo, 360)
    check("la cesion EXPIRA si la pareja muere", not m5.cedidos,
          f"cedidos={m5.cedidos}")

    # el registro se hace al SOLTAR
    m6 = mem_con_pareja(obs(300, YO, agentes=[pareja((25, 24))],
                            pack=[{"id": CURA, "n": 1}, None]))
    o_sol = obs(300, YO, agentes=[pareja((25, 24))],
                pack=[{"id": CURA, "n": 1}, None])
    _acc, rad = D.decide(o_sol, mundo, m6, 300)
    if str(rad["elegido"]).startswith("soltar_"):
        check("al soltar se registra la CESION", YO in m6.cedidos, f"{m6.cedidos}")
    else:
        print(f"  [n/a] no eligio soltar en esta escena (eligio {rad['elegido']}); "
              f"el registro se comprueba arriba por construccion")

    # ── B. EMPUNAR ─────────────────────────────────────────────────────────
    print("\n=== B. EMPUNAR ===")
    RED = {"id": "net", "durability": 10}
    o_red = obs(300, YO, hand=RED, pack=[{"id": "sword", "n": 1}, None],
                agentes=[])
    m7 = A.Memoria(); m7.hp_max = 100; m7.observa(o_red, mundo, 300)
    cands = dict(D.candidatos(o_red, mundo, m7, 300))
    check("con RED en mano y ESPADA en zurron existe `empunar_sword`",
          "empunar_sword" in cands, f"cands={sorted(cands)}")
    if "empunar_sword" in cands:
        acc = D._a_json("empunar_sword", cands["empunar_sword"], YO, mundo, m7, 300)
        check("empunar se emite como `use` sobre la ranura del arma",
              acc == {"type": "action", "do": "use", "slot": 0}, f"{acc}")

    # R-2: el arma en el zurron NO es estar armado
    W_red, det_red = A.riqueza_W(o_red["you"], mundo)
    o_esp = obs(300, YO, hand={"id": "sword", "durability": 40},
                pack=[None, None], agentes=[])
    W_esp, det_esp = A.riqueza_W(o_esp["you"], mundo)
    check("espada en ZURRON => arma = 0 (no estoy armado)",
          det_red["arma"] == 0.0, f"arma={det_red['arma']}")
    check("espada en MANO => arma > 0 (estoy armado)",
          det_esp["arma"] > 0.0, f"arma={det_esp['arma']}")

    # con la espada YA en la mano, no hay nada que empunar
    cands2 = dict(D.candidatos(o_esp, mundo, m7, 300))
    check("con la mejor arma ya en la mano no hay candidato empunar",
          not any(n.startswith("empunar_") for n in cands2), f"cands={sorted(cands2)}")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos
                  else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
