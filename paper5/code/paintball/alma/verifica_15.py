"""Banco de las PIERNAS QUE VEN A LA GENTE — PROMPT_15.

  1. El CAMPO sigue siendo el mapa: mismo campo con y sin gente delante
     (los cuerpos no se cachean; si entraran, el campo caducaria cada tic).
  2. ESCALON 1: si la vecina que baja esta libre, se va por ella.
  3. ESCALON 2: si la unica que baja tiene a alguien encima, se rodea por una
     libre que no aleje — no se empuja.
  4. ESCALON 3: si no hay salida libre, None: este tic no se camina.
  5. La EMISION de `ir_*` nunca sale hacia una casilla ocupada, ni siquiera
     por la degradacion a linea recta.
  6. La IMAGINACION usa la misma regla en el PRIMER paso y el mapa a secas en
     los siguientes (los cuerpos de ahora no se profetizan a 11 tics vista).

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_15
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

    # un tramo abierto: se busca una casilla sin solidos alrededor
    origen = None
    for y in range(4, mundo.arena_size - 4):
        for x in range(4, mundo.arena_size - 4):
            if all(not mundo.solido(x + dx, y + dy)
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                origen = (x, y)
                break
        if origen:
            break
    destino = (origen[0] + 6, origen[1])
    campo = D.campo_geodesico(mundo, destino)

    print("=== 1. el campo es el MAPA, no la gente ===")
    campo2 = D.campo_geodesico(mundo, destino)
    check("el campo se cachea y no depende de los cuerpos",
          campo is campo2 and campo.get(origen) == 6,
          f"pasos hasta el destino desde {origen}: {campo.get(origen)}")

    print("\n=== 2-4. los tres escalones del paso ===")
    libre = D._paso_geodesico(origen, campo, destino, ())
    check("escalon 1: sin nadie delante, baja la geodesica", libre == "E", f"{libre}")

    delante = (origen[0] + 1, origen[1])
    rodeo = D._paso_geodesico(origen, campo, destino, {delante})
    dx, dy = D.DIRS.get(rodeo, (0, 0))
    v_rodeo = campo.get((origen[0] + dx, origen[1] + dy))
    check("escalon 1 bis: con uno delante se elige otra que TAMBIEN baja",
          rodeo is not None and v_rodeo is not None and v_rodeo < campo[origen],
          f"{rodeo} -> valor {v_rodeo} (base {campo[origen]})")

    # tapiar TODAS las que bajan: solo queda rodear de lado
    bajan = set()
    for d, (ax, ay) in D.DIRS.items():
        q = (origen[0] + ax, origen[1] + ay)
        v = campo.get(q)
        if v is not None and v < campo[origen]:
            bajan.add(q)
    lado = D._paso_geodesico(origen, campo, destino, bajan)
    dx, dy = D.DIRS.get(lado, (0, 0))
    v_lado = campo.get((origen[0] + dx, origen[1] + dy))
    check("escalon 2: tapadas las que bajan, se rodea sin alejarse",
          lado is not None and v_lado == campo[origen],
          f"{lado} -> valor {v_lado} (base {campo[origen]}); tapadas {sorted(bajan)}")

    todas = {(origen[0] + ax, origen[1] + ay) for ax, ay in D.DIRS.values()}
    check("escalon 3: rodeado del todo, NO se camina (None)",
          D._paso_geodesico(origen, campo, destino, todas) is None, "")

    print("\n=== 5. la emision nunca embiste ===")
    cuerpos = [{"slot": 9 + i, "team": "D", "pos": list(q), "hp_band": "healthy"}
               for i, q in enumerate(sorted(todas))]
    o = obs(300, origen, agentes=cuerpos)
    m = A.Memoria(); m.hp_max = 100; m.observa(o, mundo, 300)
    cands = dict(D.candidatos(o, mundo, m, 300))
    ires = [k for k in cands if k.startswith("ir_")]
    malas = []
    for k in ires:
        acc = D._a_json(k, cands[k], origen, mundo, m, 300)
        if acc.get("do") == "move":
            ax, ay = D.DIRS[acc["dir"]]
            if (origen[0] + ax, origen[1] + ay) in todas:
                malas.append((k, acc["dir"]))
    check("ningun `ir_*` se emite contra un cuerpo", not malas,
          f"candidatos ir_*: {sorted(ires)}  embestidas: {malas}")
    check("tampoco hay `paso_*` con todo ocupado",
          not any(k.startswith("paso_") for k in cands), "")

    print("\n=== 6. la imaginacion: cuerpos en el primer paso, mapa despues ===")
    H = 48
    sin = D._camina_geodesica(origen, campo, mundo, 5, H, destino, ())
    con = D._camina_geodesica(origen, campo, mundo, 5, H, destino, {delante})
    tapado = D._camina_geodesica(origen, campo, mundo, 5, H, destino, todas)
    check("con el camino libre, la imaginacion avanza",
          sin != origen, f"{origen} -> {sin}")
    check("con uno delante, avanza igual (rodea, no se para)",
          con != origen, f"{origen} -> {con}")
    check("rodeado del todo, la imaginacion NO avanza",
          tapado == origen, f"{origen} -> {tapado}")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
