"""Banco de la fila S-7 (legitima defensa) — PROMPT_09. Sin mundo, sin episodios.

Comprueba, sobre escenas sinteticas fieles al contrato de zero-sum 0.1.18:
  1. S-7 vale 0 si nadie me ha danado (aunque haya hostiles pegados).
  2. S-7 se enciende con quien me dano y esta a la vista, y CADUCA con la ventana.
  3. El candidato `atacar_*` NO EXISTE contra un no-agresor (prohibicion de iniciar).
  4. El candidato `atacar_*` existe contra el agresor a alcance, y su valor sale
     de bajar el hp previsto del agresor (sin profetizar la esquiva).
  5. Huir tambien alivia: alejarse baja S-7 por el factor de cercania.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_s7
"""
from __future__ import annotations

import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs
from motor.model import DEFAULT_CONFIG, opponent_distance

_fallos = []


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def escena(mundo, tick, pos, agentes, hand=None, hp=70):
    return obs(tick, pos, hp=hp, hand=hand, agentes=agentes)


def main():
    mundo = Mundo.desde_player_config(player_config())
    ESPADA = {"id": "sword", "durability": 40}
    # el agresor, a dos casillas al este, sano
    AGR = {"slot": 7, "team": "D", "pos": [31, 24], "hp_band": "healthy"}   # adyacente: alcance 1
    LEJOS = {"slot": 7, "team": "D", "pos": [38, 24], "hp_band": "healthy"}
    HERIDO = {"slot": 7, "team": "D", "pos": [31, 24], "hp_band": "critical"}

    print("=== 1. sin agresion previa: S-7 = 0 y NO hay candidato de ataque ===")
    m = A.Memoria(); m.hp_max = 100
    o = escena(mundo, 200, (30, 24), [AGR], ESPADA)
    m.observa(o, mundo, 200)
    F = A.filas(o, mundo, m, 200)
    check("S-7 = 0 sin agresion", F["S-7-AGRESOR"] == 0.0, f"M={F['S-7-AGRESOR']}")
    check("S-8-EXPOSICION si se enciende (el hostil me ve)",
          F["S-8-EXPOSICION"] > 0, f"M={F['S-8-EXPOSICION']:.4f}")
    nombres = [c[0] for c in D.candidatos(o, mundo, m, 200)]
    check("NO existe candidato de ataque contra un no-agresor",
          not any(n.startswith("atacar_") for n in nombres), f"cands={nombres}")

    print("\n=== 2. me dana: S-7 se enciende y aparece el candidato ===")
    m2 = A.Memoria(); m2.hp_max = 100
    o_golpe = escena(mundo, 200, (30, 24), [AGR], ESPADA)
    o_golpe["you"]["damage_taken"] = [{"source": "P7", "amount": 25.0}]
    m2.observa(o_golpe, mundo, 200)
    o2 = escena(mundo, 210, (30, 24), [AGR], ESPADA)
    m2.observa(o2, mundo, 210)
    F2 = A.filas(o2, mundo, m2, 210)
    check("S-7 > 0 tras recibir dano", F2["S-7-AGRESOR"] > 0,
          f"M={F2['S-7-AGRESOR']:.4f}  detalle={F2['_agresores']}")
    nom2 = [c[0] for c in D.candidatos(o2, mundo, m2, 210)]
    check("EXISTE candidato de ataque contra el agresor a alcance",
          any(n.startswith("atacar_") for n in nom2), f"cands={nom2}")

    print("\n=== 3. la ventana CADUCA ===")
    o3 = escena(mundo, 200 + int(A.AGRESOR_VENTANA_S * 24) + 5, (30, 24), [AGR], ESPADA)
    m2.observa(o3, mundo, o3["tick"])
    F3 = A.filas(o3, mundo, m2, o3["tick"])
    check("S-7 vuelve a 0 pasada la ventana", F3["S-7-AGRESOR"] == 0.0,
          f"tick={o3['tick']} M={F3['S-7-AGRESOR']}")
    nom3 = [c[0] for c in D.candidatos(o3, mundo, m2, o3["tick"])]
    check("y el candidato de ataque desaparece",
          not any(n.startswith("atacar_") for n in nom3))

    print("\n=== 4. un agresor MAS DEBIL presiona menos; uno LEJOS, tambien ===")
    F_sano = A.filas(escena(mundo, 210, (30, 24), [AGR], ESPADA), mundo, m2, 210) \
        if False else None
    m4 = A.Memoria(); m4.hp_max = 100
    og = escena(mundo, 200, (30, 24), [AGR], ESPADA)
    og["you"]["damage_taken"] = [{"source": "P7", "amount": 25.0}]
    m4.observa(og, mundo, 200)
    def M_con(ag, p=(30, 24)):
        o = escena(mundo, 205, p, [ag], ESPADA)
        return A.filas(o, mundo, m4, 205)["S-7-AGRESOR"]
    m_sano, m_herido, m_lejos = M_con(AGR), M_con(HERIDO), M_con(LEJOS)
    check("agresor debilitado presiona MENOS", m_herido < m_sano,
          f"sano={m_sano:.4f} critico={m_herido:.4f}")
    check("agresor lejano presiona MENOS (huir alivia)", m_lejos < m_sano,
          f"cerca={m_sano:.4f} lejos={m_lejos:.4f}")

    print("\n=== 5. la decision: responder vs huir COMPITEN ===")
    m5 = A.Memoria(); m5.hp_max = 100
    og = escena(mundo, 200, (30, 24), [AGR], ESPADA)
    og["you"]["damage_taken"] = [{"source": "P7", "amount": 40.0}]
    m5.observa(og, mundo, 200)
    o5 = escena(mundo, 205, (30, 24), [AGR], ESPADA, hp=70)
    m5.observa(o5, mundo, 205)
    accion, R = D.decide(o5, mundo, m5, 205)
    orden = sorted(R["candidatos"].items(), key=lambda kv: kv[1]["d"])
    print(f"    filas: " + ", ".join(
        f"{k}={v['M']}" for k, v in A.appraise(o5, mundo, m5, 205)[1]["filas"].items()
        if v.get("M")))
    for k, v in orden[:5]:
        print(f"      {k:12s} d={v['d']:.5f}")
    print(f"    ELIGE {R['elegido']}  honor={R['honor']}")
    atac = [k for k, _ in orden if k.startswith("atacar_")]
    check("el candidato de respuesta esta en la mesa", bool(atac), f"{atac}")
    if R["honor"]:
        check("HONOR: si atacamos, el objetivo era agresor",
              R["honor"]["era_agresor"], str(R["honor"]))

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
