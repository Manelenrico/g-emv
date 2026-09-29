"""Banco del PONERSE — PROMPT_17 B. Escenas sinteticas, sin episodios.

  1. Con el CUERPO VACIO no hace falta candidato: el mundo equipa solo al coger
     (`sim.nim:735`). Con prenda en el ZURRON, el candidato existe.
  2. Se emite como `use` sobre la ranura y comparte el canal.
  3. La prevision es la del mundo: la prenda pasa al cuerpo y la ranura queda
     vacia (`sim.nim:805-809`).
  4. Cambiar de MOCHILA a otra prenda descuenta las ranuras 2-3 en la
     prevision (`unequipBodyToGround`).
  5. EL VALOR NO SE LEGISLA: ponerse el camuflaje BAJA S-8 en la observacion
     prevista, y por ahi gana o pierde. Se comprueba que baja.
  6. La prenda ya puesta no se ofrece otra vez.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_17
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
    CAMO, MOCHILA = mundo.id_camuflaje, mundo.id_mochila

    abierto = None
    for y in range(6, mundo.arena_size - 6):
        if all(not mundo.solido(x, y) for x in range(y - 4, y + 12)):
            abierto = y
            break
    YO = (abierto, abierto)
    LEJOS = (YO[0] + 6, YO[1])       # a 6: fuera de 4, dentro de 7

    def mem_de(o, tick=300):
        m = A.Memoria(); m.hp_max = 100; m.observa(o, mundo, tick)
        return m

    print("=== 1. cuando existe el candidato ===")
    o_vacio = obs(300, YO, pack=[None, None])
    c_vacio = dict(D.candidatos(o_vacio, mundo, mem_de(o_vacio), 300))
    check("sin prenda en el zurron no hay candidato",
          not any(k.startswith("ponerse_") for k in c_vacio), "")

    o_pk = obs(300, YO, pack=[{"id": CAMO, "n": 1}, None])
    m_pk = mem_de(o_pk)
    c_pk = dict(D.candidatos(o_pk, mundo, m_pk, 300))
    check("con el camuflaje en el zurron, aparece `ponerse_camouflage`",
          f"ponerse_{CAMO}" in c_pk,
          f"{sorted(k for k in c_pk if k.startswith('ponerse_'))}")

    o_ya = obs(300, YO, pack=[{"id": CAMO, "n": 1}, None], body={"id": CAMO})
    c_ya = dict(D.candidatos(o_ya, mundo, mem_de(o_ya), 300))
    check("la prenda YA puesta no se vuelve a ofrecer",
          f"ponerse_{CAMO}" not in c_ya,
          f"{sorted(k for k in c_ya if k.startswith('ponerse_'))}")

    print("\n=== 2. emision y canal ===")
    acc = D._a_json(f"ponerse_{CAMO}", c_pk[f"ponerse_{CAMO}"], YO, mundo, m_pk, 300)
    check("se emite como `use` sobre la ranura",
          acc == {"type": "action", "do": "use", "slot": 0}, f"{acc}")
    b = D.Bloqueos(); b.canal_hasta = 400
    check("comparte el veto del canal con `usar_`",
          b.veta(f"ponerse_{CAMO}", o_pk, 300), "")

    print("\n=== 3-4. la prevision es la del mundo ===")
    _a, rad = D.decide(o_pk, mundo, m_pk, 300)
    det = (rad.get("candidatos") or {}).get(f"ponerse_{CAMO}")
    check("hay radiografia del candidato", isinstance(det, dict), f"{type(det)}")

    # mochila puesta + camuflaje en zurron 0, algo en las ranuras 2-3
    o_mo = obs(300, YO, body={"id": MOCHILA},
               pack=[{"id": CAMO, "n": 1}, None,
                     {"id": "rations", "n": 1}, {"id": "arrows", "n": 6}])
    m_mo = mem_de(o_mo)
    c_mo = dict(D.candidatos(o_mo, mundo, m_mo, 300))
    rec = c_mo.get(f"ponerse_{CAMO}")
    check("con mochila puesta, el candidato existe y recuerda el cuerpo previo",
          rec is not None and rec.get("cuerpo_previo") == MOCHILA, f"{rec}")

    print("\n=== 5. el valor NO se legisla: sale de S-8 ===")
    hostil = [{"slot": 9, "team": "D", "pos": list(LEJOS), "hp_band": "healthy"}]
    o_h = obs(300, YO, pack=[{"id": CAMO, "n": 1}, None], agentes=hostil)
    m_h = mem_de(o_h)
    F_antes = A.filas(o_h, mundo, m_h, 300)
    o_puesto = obs(300, YO, pack=[None, None], body={"id": CAMO}, agentes=hostil)
    F_desp = A.filas(o_puesto, mundo, m_h, 300)
    check("ponerse el camuflaje BAJA S-8 (el de 6 casillas deja de verme)",
          F_desp["S-8-EXPOSICION"] < F_antes["S-8-EXPOSICION"]
          and F_desp["S-8-EXPOSICION"] == 0.0,
          f"{F_antes['S-8-EXPOSICION']:.5f} -> {F_desp['S-8-EXPOSICION']:.5f}")

    _a2, rad2 = D.decide(o_h, mundo, m_h, 300)
    cs = rad2.get("candidatos") or {}
    dp = cs.get(f"ponerse_{CAMO}", {}).get("d")
    dn = cs.get("noop", {}).get("d")
    print(f"    d(ponerse)={dp}   d(noop)={dn}   elegido={rad2['elegido']}")
    check("con un hostil que me ve, ponerse GANA a quedarse",
          dp is not None and dn is not None and dp < dn, "")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
