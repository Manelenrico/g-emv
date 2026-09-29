"""Banco de F-4 ALCANCE — PROMPT_21 A. Escenas sinteticas, sin episodios.

  1. Sin hostiles a la vista, F-4 = 0.
  2. Crece monotonamente al acortarse la distancia del peor hostil.
  3. La PAREJA no duele nunca, ni viva ni muerta.
  4. Techo respetado con cuatro hostiles encima.
  5a. La escena del verdugo, SIN botin de por medio: el paso que ALEJA gana al
      quedarse y al que ACERCA. Es lo que la fila tiene que producir.
  5b. La misma escena CON una racion entre el cazador y yo: se DOCUMENTA quien
      gana. El desequilibrio R-CARENCIA/miedo esta APARCADO por Manel en este
      encargo: aqui se mide, no se arregla.
  6. La escena del 19C: ardiendo + hambre + cazador cerca -> ¿sigue ganando
     ir de compras?
  7. Interaccion con el escondite: camuflado y quieto con hostil a 6 -> se
     DOCUMENTA lo que elija el motor, no se legisla.
  8. Cero candidatos nuevos: el repertorio es el mismo que en v15.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_21
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

    abierto = None
    for y in range(10, mundo.arena_size - 14):
        if all(not mundo.solido(x, y) for x in range(y - 8, y + 14)):
            abierto = y
            break
    YO = (abierto, abierto)

    def escena(hostiles, **kw):
        o = obs(300, kw.pop("pos", YO), agentes=[
            {"slot": s, "team": "D", "pos": list(q), "hp_band": "healthy"}
            for s, q in hostiles], **kw)
        m = A.Memoria(); m.hp_max = 100; m.observa(o, mundo, 300)
        return o, m

    print("=== 1. sin hostiles, F-4 = 0 ===")
    o, m = escena([])
    check("F-4 = 0 sin nadie a la vista",
          A.filas(o, mundo, m, 300)["F-4-ALCANCE"] == 0.0, "")

    print("\n=== 2. monotonia ===")
    vals = []
    for d in (14, 10, 8, 6, 4, 3, 2, 1):
        o, m = escena([(9, (YO[0] + d, YO[1]))])
        vals.append((d, A.filas(o, mundo, m, 300)["F-4-ALCANCE"]))
    print("     " + "  ".join(f"d{d}={v:.5f}" for d, v in vals))
    check("crece monotonamente al acercarse",
          all(vals[i][1] <= vals[i + 1][1] for i in range(len(vals) - 1)), "")
    check("el gradiente por casilla es pequeno pero no nulo",
          0 < vals[3][1] - vals[2][1] < 0.02,
          f"de d8 a d6: +{vals[3][1] - vals[2][1]:.5f}")

    print("\n=== 3. la pareja no duele ===")
    PAR = mundo.teammate_slot
    o, m = escena([(PAR, (YO[0] + 1, YO[1]))])
    check("pareja pegada: F-4 = 0",
          A.filas(o, mundo, m, 300)["F-4-ALCANCE"] == 0.0, "")
    m.pareja_muerta = True
    check("pareja muerta: F-4 sigue en 0",
          A.filas(o, mundo, m, 300)["F-4-ALCANCE"] == 0.0, "")

    print("\n=== 4. techo con cuatro encima ===")
    o, m = escena([(9, (YO[0] + 1, YO[1])), (10, (YO[0] - 1, YO[1])),
                   (11, (YO[0], YO[1] + 1)), (12, (YO[0], YO[1] - 1))])
    F = A.filas(o, mundo, m, 300)
    check("techo 0.5 respetado con cuatro hostiles pegados",
          F["F-4-ALCANCE"] == A.ALCANCE_TECHO, f"M={F['F-4-ALCANCE']}")

    CAZ = (YO[0] + 6, YO[1])

    def mesa(o, m, caz=CAZ):
        """ACTUALIZADO EN EL PROMPT_35 — se clasifica por DISTANCIA RESULTANTE,
        no por la letra del rumbo.

        El banco original llamaba "alejarse" a W/NW/SW y "acercarse" a E/NE/SE,
        con el cazador al este. Era una aproximacion valida con el cuerpo
        8/6/5/1: la zancada proyectaba 4 casillas y la letra bastaba. Con la
        constitucion 8/1/10/1 el enfriamiento baja a 6 tics, la zancada proyecta
        OCHO, y la letra MIENTE: con el cazador en (14,8) y nosotros en (8,8),
        `move_SE` acaba en (16,16) — a OCHO casillas de el, mas lejos que varios
        rumbos "de huida".

        Se corrige el INSTRUMENTO, no la conducta: la pregunta del 21 sigue
        siendo "¿prefiere alejarse?", y ahora se mide donde acaba de verdad.
        Mismo precedente que el 28 con el gate del 14, y el 33 con el del 28.
        """
        _a, rad = D.decide(o, mundo, m, 300)
        dd = {k: (v["d"] if isinstance(v, dict) else v)
              for k, v in (rad.get("candidatos") or {}).items()}
        yo = tuple(o["you"]["pos"])
        spd = int((o["you"].get("stats") or {}).get("speed") or 5)

        def destino(k):
            d = k.split("_")[-1]
            if k.startswith("move_"):
                return D._simula_camino(yo, d, mundo, spd, 48, False)
            dx, dy = D.DIRS[d]
            return (yo[0] + dx, yo[1] + dy)

        def cheb(p, q):
            return max(abs(p[0] - q[0]), abs(p[1] - q[1]))

        d0 = cheb(yo, caz)
        pasos = [k for k in dd if k.startswith(("move_", "paso_"))]
        aleja = [k for k in pasos if cheb(destino(k), caz) > d0]
        acerca = [k for k in pasos if cheb(destino(k), caz) < d0]
        return rad, dd, aleja, acerca

    print("\n=== 5a. el verdugo, SIN botin de por medio ===")
    o, m = escena([(15, CAZ)])
    rad, dd, aleja, acerca = mesa(o, m)
    d_al = min(dd[k] for k in aleja)
    d_ac = min(dd[k] for k in acerca)
    print(f"     elegido: {rad['elegido']}")
    print(f"     mejor ALEJARSE {d_al:.5f}  ·  quieto {dd['noop']:.5f}  ·  "
          f"mejor ACERCARSE {d_ac:.5f}")
    check("alejarse gana a quedarse quieto", d_al < dd["noop"],
          f"{d_al:.5f} < {dd['noop']:.5f}")
    check("alejarse gana a acercarse", d_al < d_ac, f"{d_al:.5f} < {d_ac:.5f}")
    check("y el elegido es un paso que ALEJA", rad["elegido"] in aleja,
          f"(gana {rad['elegido']})")

    print("\n=== 5b. la misma escena CON una racion en medio (aparcado: se mide) ===")
    o, m = escena([(15, CAZ)], items=[{"id": "rations",
                                       "pos": [YO[0] + 3, YO[1]], "n": 1}])
    rad, dd, aleja, acerca = mesa(o, m)
    print(f"     elegido: {rad['elegido']}   ·   ir_objeto {dd.get('ir_objeto')}   ·   "
          f"mejor alejarse {min(dd[k] for k in aleja):.5f}   ·   quieto {dd['noop']:.5f}")
    print("     DOCUMENTADO: con la comida entre el cazador y yo, el hambre manda.")
    print("     No es un fallo de F-4: es el desequilibrio que Manel aparco.")

    print("\n=== 6. la escena del 19C: ardiendo, con hambre y con cazador ===")
    zona = {"center": [24, 24], "radius": 5, "next_radius": 3,
            "warn_tick": 0, "shrink_tick": 0, "damage_per_s": 16}
    o = obs(300, YO, hp=40, zona=zona,
            agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                      "hp_band": "healthy"}],
            items=[{"id": "sword", "pos": [YO[0] + 3, YO[1]], "n": 1}])
    m = A.Memoria(); m.hp_max = 100; m.observa(o, mundo, 300)
    _a6, rad6 = D.decide(o, mundo, m, 300)
    cs6 = {k: (v["d"] if isinstance(v, dict) else v)
           for k, v in (rad6.get("candidatos") or {}).items()}
    F6 = A.filas(o, mundo, m, 300)
    print(f"     filas: { {k: round(v,5) for k,v in F6.items() if isinstance(v,float) and v} }")
    print(f"     elegido: {rad6['elegido']}   ir_objeto: {cs6.get('ir_objeto')}")
    check("con cazador cerca ya NO gana ir de compras",
          rad6["elegido"] != "ir_objeto",
          f"(eligio {rad6['elegido']})")

    print("\n=== 7. escondite vs alcance (se DOCUMENTA, no se legisla) ===")
    o7, m7 = escena([(9, (YO[0] + 6, YO[1]))], body=CAMO)
    F7 = A.filas(o7, mundo, m7, 300)
    _a7, rad7 = D.decide(o7, mundo, m7, 300)
    print(f"     camuflado y quieto con hostil a 6:")
    print(f"       S-8 = {F7['S-8-EXPOSICION']:.5f}   F-4 = {F7['F-4-ALCANCE']:.5f}")
    print(f"       elige: {rad7['elegido']}")
    print("     (dato para el acta: es la primera vez que dos filas nuevas se pisan)")

    print("\n=== 8. cero candidatos nuevos ===")
    o8, m8 = escena([(9, (YO[0] + 6, YO[1]))])
    nombres = sorted(k for k, _ in D.candidatos(o8, mundo, m8, 300))
    esperados = {"noop"} | {f"move_{d}" for d in D.DIRS} | {f"paso_{d}" for d in D.DIRS}
    check("el repertorio no gana verbos nuevos",
          set(nombres) <= esperados | {"ir_botin", "ir_objeto", "ir_centro",
                                       "ir_pareja", "coger"},
          f"{[n for n in nombres if n not in esperados]}")
    check("ningun candidato se llama como la fila",
          not any("alcance" in n.lower() for n in nombres), "")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
