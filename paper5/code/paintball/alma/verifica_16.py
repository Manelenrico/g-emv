"""Banco de S-8 EXPOSICION — PROMPT_16. Escenas sinteticas, sin episodios.

  1. S-4 APINAMIENTO ya no existe; S-8 EXPOSICION ocupa su sitio.
  2. LA ROCA CORTA: el mismo hostil, a la misma distancia, con un muro de por
     medio, deja de contar.
  3. EL RADIO: un hostil mas alla del radio conservador (leido de `stats.max`)
     no cuenta; dentro, si.
  4. EL CAMUFLAJE ANULA: puesto y quieto, los de mas de 4 casillas dejan de
     verme; los de dentro de 4 siguen contando.
  5. EL CAMUFLAJE EN MOVIMIENTO: el tope sube de 4 a 7 (un candidato que mueve
     se expone mas que el mismo agente quieto).
  6. ATACAR DELATA: dentro de la ventana, el camuflaje no cuenta.
  7. EL EQUILIBRIO DE LA PAZ: camuflado, quieto y sin nadie a <=4 => 0.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_16
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
    CAMO = mundo.id_camuflaje

    # un tramo ABIERTO (sin solidos) para las escenas sin muro
    abierto = None
    for y in range(6, mundo.arena_size - 6):
        libre = all(not mundo.solido(x, y) for x in range(y - 4, y + 12)) \
            if 0 <= y - 4 else False
        if libre:
            abierto = y
            break
    YO = (abierto, abierto)

    def escena(hostiles, body=None, pos=YO, mem=None, tick=300):
        o = obs(tick, pos, agentes=[
            {"slot": 9 + i, "team": "D", "pos": list(q), "hp_band": "healthy"}
            for i, q in enumerate(hostiles)], body=body)
        m = mem or A.Memoria()
        m.hp_max = 100
        m.observa(o, mundo, tick)
        return A.filas(o, mundo, m, tick), m

    print("=== 1. S-4 fuera, S-8 dentro ===")
    F, _ = escena([(YO[0] + 2, YO[1])])
    check("S-APINAMIENTO ya no existe", "S-APINAMIENTO" not in F, "")
    check("S-8-EXPOSICION existe y se enciende con un hostil pegado",
          F.get("S-8-EXPOSICION", 0) > 0, f"M={F.get('S-8-EXPOSICION')}")
    check("el radio hostil se LEE (stats.max), no se cablea",
          F["_radio_hostil"] == mundo.radio_vision_max() == 10.0,
          f"radio={F['_radio_hostil']}")

    print("\n=== 2. la roca corta la linea de vista ===")
    # se busca un muro y se pone un hostil justo detras, a la misma distancia
    muro = None
    for y in range(2, mundo.arena_size - 2):
        for x in range(2, mundo.arena_size - 2):
            if mundo.solido(x, y) and not mundo.solido(x - 1, y) \
                    and not mundo.solido(x + 1, y) and not mundo.solido(x - 2, y):
                muro = (x, y)
                break
        if muro:
            break
    aca = (muro[0] - 1, muro[1])
    detras = (muro[0] + 1, muro[1])
    F_v, _ = escena([(aca[0] - 1, aca[1])], pos=aca)      # a 1, sin muro
    F_t, _ = escena([detras], pos=aca)                    # a 2, con el muro
    check("con muro de por medio, el hostil NO cuenta",
          F_t["_me_ven"] == 0 and F_t["S-8-EXPOSICION"] == 0.0,
          f"muro={muro} yo={aca} el={detras} me_ven={F_t['_me_ven']}")
    check("sin muro, el mismo tipo de hostil SI cuenta",
          F_v["_me_ven"] == 1, f"me_ven={F_v['_me_ven']}")

    print("\n=== 3. el radio conservador ===")
    R = int(mundo.radio_vision_max())
    F_d, _ = escena([(YO[0] + R - 1, YO[1])])
    F_f, _ = escena([(YO[0] + R + 2, YO[1])])
    check("dentro del radio, cuenta", F_d["_me_ven"] == 1, f"a {R-1}")
    check("fuera del radio, no cuenta", F_f["_me_ven"] == 0, f"a {R+2}")

    print("\n=== 4-5. el camuflaje ===")
    lejos = (YO[0] + 6, YO[1])          # a 6: fuera de 4, dentro de 7
    cerca = (YO[0] + 3, YO[1])          # a 3: dentro de 4
    F_sin, _ = escena([lejos])
    F_con, _ = escena([lejos], body={"id": CAMO})
    check("sin camuflaje, el de 6 casillas me ve", F_sin["_me_ven"] == 1, "")
    check("camuflado y QUIETO, el de 6 casillas NO me ve",
          F_con["_me_ven"] == 0 and F_con["_camo"]["tope"] == A.CAMO_QUIETO,
          f"tope={F_con['_camo']['tope']}")
    F_cc, _ = escena([cerca], body={"id": CAMO})
    check("camuflado, el de DENTRO de 4 sigue contando",
          F_cc["_me_ven"] == 1, f"me_ven={F_cc['_me_ven']}")

    # en movimiento: la posicion prevista difiere de la real
    o_mov = obs(300, (YO[0] + 1, YO[1]), body={"id": CAMO}, agentes=[
        {"slot": 9, "team": "D", "pos": list(lejos), "hp_band": "healthy"}])
    m_mov = A.Memoria(); m_mov.hp_max = 100
    m_mov.observa(obs(300, YO, body={"id": CAMO}), mundo, 300)   # mi pos REAL
    F_mov = A.filas(o_mov, mundo, m_mov, 300)
    check("camuflado y EN MOVIMIENTO, el tope sube a 7",
          F_mov["_camo"]["moviendo"] and F_mov["_camo"]["tope"] == A.CAMO_MOVIENDO,
          f"tope={F_mov['_camo']['tope']}  me_ven={F_mov['_me_ven']}")

    print("\n=== 6. atacar delata ===")
    m_at = A.Memoria(); m_at.hp_max = 100
    m_at.ultimo_ataque = 300 - int(A.CAMO_REVELADO_S * mundo.tick_rate / 2)
    F_at, _ = escena([lejos], body={"id": CAMO}, mem=m_at)
    check("recien atacado, el camuflaje no protege",
          F_at["_camo"]["delatado"] and F_at["_me_ven"] == 1,
          f"delatado={F_at['_camo']['delatado']} me_ven={F_at['_me_ven']}")
    m_vj = A.Memoria(); m_vj.hp_max = 100
    m_vj.ultimo_ataque = 300 - int(A.CAMO_REVELADO_S * mundo.tick_rate * 3)
    F_vj, _ = escena([lejos], body={"id": CAMO}, mem=m_vj)
    check("pasada la ventana, vuelve a proteger",
          not F_vj["_camo"]["delatado"] and F_vj["_me_ven"] == 0, "")

    print("\n=== 7. el equilibrio de la paz ===")
    F_paz, _ = escena([lejos, (YO[0] + 9, YO[1] + 3)], body={"id": CAMO})
    check("camuflado, quieto y sin nadie a <=4: EXPOSICION 0",
          F_paz["S-8-EXPOSICION"] == 0.0 and F_paz["_hostiles"] == 2,
          f"M={F_paz['S-8-EXPOSICION']}  hostiles={F_paz['_hostiles']}  "
          f"me_ven={F_paz['_me_ven']}")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
