"""Banco de LA PROMESA DEL OBJETO — PROMPT_18 A. Escenas sinteticas.

  1. Con S-8 > 0 y un camuflaje a la vista, `ir_objeto` apunta al camuflaje y
     GANA a lo que ganaba en esa misma escena sin la promesa.
  2. Con S-8 = 0, la promesa del camuflaje es 0: vuelve a valer su casilla.
     (La promesa es alivio, no fetiche.)
  3. Con el CUERPO VACIO, la prevision de llegar al camuflaje deja el estado
     previsto CON LA PRENDA PUESTA, no en el zurron.
  4. Un objeto sin fila conocida (una racion) se valora igual que antes: el
     cambio es inerte fuera de su caso.
  5. La mochila promete por el granero de W, no por S-8.
  6. La prenda ya puesta no promete nada.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_18
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
    for y in range(8, mundo.arena_size - 10):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            abierto = y
            break
    YO = (abierto, abierto)
    # el camuflaje AL OESTE y el hostil AL ESTE: ir a por la prenda ALEJA.
    # (Si la prenda estuviera hacia el hostil, ir a por ella expondria mas y
    #  la prevision lo diria; eso NO es un fallo de la promesa, es geometria.)
    CAMO_POS = (YO[0] - 3, YO[1])
    HOSTIL = (YO[0] + 6, YO[1])            # a 6: me ve (fuera del tope 4)

    def escena(hostiles, items, body=None, tick=300):
        o = obs(tick, YO, body=body,
                agentes=[{"slot": 9 + i, "team": "D", "pos": list(q),
                          "hp_band": "healthy"} for i, q in enumerate(hostiles)],
                items=[{"id": i, "pos": list(q), "n": 1} for i, q in items])
        m = A.Memoria(); m.hp_max = 100; m.observa(o, mundo, tick)
        return o, m

    print("=== 1. con S-8 encendida, el camuflaje llama ===")
    o, m = escena([HOSTIL], [(CAMO, CAMO_POS)])
    F = A.filas(o, mundo, m, 300)
    s8 = F["S-8-EXPOSICION"]
    prom = D._promesa(o, mundo, m, 300, CAMO)
    check("S-8 esta encendida en la escena", s8 > 0, f"S-8={s8:.5f}")
    check("la promesa del camuflaje es el alivio de S-8",
          abs(prom - s8) < 1e-9, f"promesa={prom:.5f}  S-8={s8:.5f}")
    sin = D._mejor_objeto(YO, mundo, m)                       # como en v14
    con = D._mejor_objeto(YO, mundo, m, o, 300)               # con promesa
    check("`_mejor_objeto` apunta al camuflaje con la promesa",
          con == CAMO_POS, f"sin promesa -> {sin} · con promesa -> {con}")
    cands = dict(D.candidatos(o, mundo, m, 300))
    check("`ir_objeto` existe y va al camuflaje",
          cands.get("ir_objeto", {}).get("destino") == CAMO_POS,
          f"{cands.get('ir_objeto')}")
    _a, rad = D.decide(o, mundo, m, 300)
    cs = rad.get("candidatos") or {}
    print(f"    elegido={rad['elegido']}   d(ir_objeto)={cs.get('ir_objeto', {}).get('d')}"
          f"   d(noop)={cs.get('noop', {}).get('d')}")
    check("con un hostil que me ve, ir_objeto gana a quedarse",
          cs.get("ir_objeto", {}).get("d") is not None
          and cs["ir_objeto"]["d"] < cs["noop"]["d"], "")

    print("\n=== 2. sin nadie que me vea, la promesa se apaga ===")
    o0, m0 = escena([], [(CAMO, CAMO_POS)])
    F0 = A.filas(o0, mundo, m0, 300)
    p0 = D._promesa(o0, mundo, m0, 300, CAMO)
    check("S-8 = 0 y la promesa del camuflaje = 0",
          F0["S-8-EXPOSICION"] == 0.0 and p0 == 0.0,
          f"S-8={F0['S-8-EXPOSICION']}  promesa={p0}")

    print("\n=== 3. cuerpo vacio: llegar al camuflaje es vestirlo ===")
    _a3, rad3 = D.decide(o, mundo, m, 300)
    det = (rad3.get("candidatos") or {}).get("ir_objeto") or {}
    # la M de S-8 prevista para ir_objeto tiene que ser MENOR que la de quieto
    f_ir = (det.get("filas") or {}).get("S-8-EXPOSICION", 0.0)
    f_no = (((rad3.get("candidatos") or {}).get("noop") or {})
            .get("filas") or {}).get("S-8-EXPOSICION", 0.0)
    check("la prevision de ir_objeto trae S-8 mas baja (prenda puesta)",
          f_ir < f_no, f"S-8 prevista: ir_objeto {f_ir} vs noop {f_no}")

    print("\n=== 4. inerte fuera de su caso ===")
    o4, m4 = escena([HOSTIL], [("rations", CAMO_POS)])
    check("una racion no promete nada",
          D._promesa(o4, mundo, m4, 300, "rations") == 0.0, "")
    check("con solo raciones, `_mejor_objeto` da lo mismo con y sin promesa",
          D._mejor_objeto(YO, mundo, m4) == D._mejor_objeto(YO, mundo, m4, o4, 300),
          f"{D._mejor_objeto(YO, mundo, m4)}")

    print("\n=== 5. la mochila promete por el granero ===")
    o5, m5 = escena([], [(MOCHILA, CAMO_POS)])
    p5 = D._promesa(o5, mundo, m5, 300, MOCHILA)
    W0, _ = A.riqueza_W(o5["you"], mundo)
    y1 = dict(o5["you"]); y1["body"] = MOCHILA      # cadena: formato del mundo
    W1, _ = A.riqueza_W(y1, mundo)
    check("la promesa de la mochila es exactamente lo que sube W",
          abs(p5 - max(0.0, W1 - W0)) < 1e-9, f"promesa={p5:.5f}  W {W0:.3f}->{W1:.3f}")
    # con el zurron LLENO, el granero si vale: la promesa se enciende
    o5b = dict(o5); y5b = dict(o5["you"])
    y5b["pack"] = [{"id": "rations", "n": 1}, {"id": "rations", "n": 1}]
    o5b["you"] = y5b
    p5b = D._promesa(o5b, mundo, m5, 300, MOCHILA)
    check("con el zurron lleno de raciones, la mochila promete MAS",
          p5b > p5 > 0.0, f"vacio={p5:.5f}  con 2 raciones={p5b:.5f}")

    print("\n=== 6. lo ya puesto no promete ===")
    o6, m6 = escena([HOSTIL], [(CAMO, CAMO_POS)], body=CAMO)
    check("con el camuflaje puesto, su promesa es 0",
          D._promesa(o6, mundo, m6, 300, CAMO) == 0.0, "")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
