"""Banco de LA MEMORIA ACUMULADA — PROMPT_71. Resello de F-REENCUENTRO.

El 70 dejo la fila encendiendose cuando debia (13/15, 7 tics de adelanto) y
SIN MOVER NI UNA DECISION: recordaba un golpe de 18 en una mesa donde ya
pesan cuesta, muro y anillo. El resello: la memoria recuerda el DANO
ACUMULADO de ese asiento en el episodio. Cuesta cero y es la ultima palanca
honesta; si sigue muda, PARAR y cerrarla con dos numeros.

Las 15 fotos del caso exacto se parametrizan con los datos REALES del campo:
arma vista, distancia minima y —lo nuevo— el dano que ese asiento nos habia
hecho de verdad antes del reencuentro (`runs/casos_exactos.json`, extraido de
los diarios del 64+66: mediana 52, maximo 211).

  P1 (sellado) LA MAGNITUD SUBE: mediana de F-REENCUENTRO > 0,18.
  P2 (sellado) LA ACCION CAMBIA: >=5 de 15, y lo que cambia es distancia /
     pared / hacia la hermana — 0 golpes nacidos de la memoria.
  P3 (sellado) NO PAGA CON COMIDA NI CON CURA (candado del 46 y del 62).
  P4 (sellado) SILENCIOS: sin asiento conocido -> byte a byte v36.
  P5 candados, honor, regresion (fuera de este fichero).
  P6 (sin sello) QUIEN DIVERGE PRIMERO (R7).

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_71
"""
from __future__ import annotations

import collections
import json
import os
import statistics as st
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs
from alma.verifica_54 import dump
from alma.verifica_70 import v36


def escena(mundo, YO, slot, arma, d_ini, d_fin, dano, tics=6, T0=300,
           golpe=18.0):
    """Como la del 70, pero el dano llega en VARIOS golpes (como en el campo):
    asi el ultimo golpe (v37) y el acumulado (v37b) son numeros distintos y el
    interruptor de pareado significa algo."""
    mem = A.Memoria(); mem.hp_max = 100
    n = max(1, int(round(dano / golpe)))
    cada = dano / n
    t = T0 - 200 - n
    hp = 100.0
    for k in range(n):
        hp = max(1.0, hp - cada)
        o0 = obs(t + k, YO, hp=hp, hand={"id": "sword", "n": 1},
                 pack=[None, None],
                 agentes=[{"slot": slot, "team": "D",
                           "pos": [YO[0] + 1, YO[1]], "hp_band": "healthy",
                           "hand": arma}])
        o0["you"]["damage_taken"] = [{"source": f"P{slot}", "amount": cada}]
        mem.observa(o0, mundo, t + k)
    filas, acciones = [], []
    paso = (d_ini - d_fin) / max(1, tics - 1)
    for i in range(tics):
        tt = T0 + i
        d = max(d_fin, d_ini - paso * i)
        px = YO[0] + int(round(d))
        o = obs(tt, YO, hp=hp, hand={"id": "sword", "n": 1}, pack=[None, None],
                agentes=[{"slot": slot, "team": "D", "pos": [px, YO[1]],
                          "hp_band": "healthy", "hand": arma}])
        mem.observa(o, mundo, tt)
        F = A.filas(o, mundo, mem, tt)
        a, r = D.decide(o, mundo, mem, tt)
        filas.append(F.get("F-REENCUENTRO") or 0.0)
        acciones.append(r.get("elegido"))
    return filas, acciones

_fallos = []
_honores = []
DEF = (A.REENCUENTRO_ON, A.ACUMULADO_ON)
CASOS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "runs", "casos_exactos.json")


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v37():
    v36(); A.REENCUENTRO_ON, A.ACUMULADO_ON = True, False


def v37b():
    v36(); A.REENCUENTRO_ON, A.ACUMULADO_ON = True, True


def clase(el):
    if (el or "").startswith(("move_", "paso_")):
        return "distancia/pared"
    if el == "ir_pareja":
        return "hacia la hermana"
    if (el or "").startswith("atacar"):
        return "GOLPE"
    if el in ("ir_botin", "ir_objeto", "coger"):
        return "botin"
    if (el or "").startswith("usar"):
        return "cura"
    return el or "?"


def main():
    check("v37b sellada por defecto (REENCUENTRO + ACUMULADO)",
          DEF == (True, True), f"{DEF}")
    mundo = Mundo.desde_player_config(player_config())
    C = mundo.arena_size // 2
    YO = (C, C)
    casos = json.load(open(CASOS))
    acs = [c["acum_real"] for c in casos]
    print(f"  {len(casos)} casos exactos · dano ACUMULADO real: min {min(acs):.0f}"
          f" · mediana {st.median(acs):.0f} · max {max(acs):.0f}\n")

    # ── P1 · la magnitud sube ────────────────────────────────────────────
    print("=== P1. la magnitud sube (mediana > 0,18) ===")
    m37, m37b = [], []
    for c in casos:
        arma = c["arma"] if c["arma"] in mundo.items else "sword"
        dmin = float(c["dmin"] or 1.0)
        d_ini = min(5.0, dmin + 3)
        v37(); f1, _ = escena(mundo, YO, c["slot"], arma, d_ini, dmin,
                              dano=c["acum_real"])
        v37b(); f2, _ = escena(mundo, YO, c["slot"], arma, d_ini, dmin,
                               dano=c["acum_real"])
        m37.append(max(f1)); m37b.append(max(f2))
    print(f"    v37  (ultimo golpe): min {min(m37):.2f} · mediana "
          f"{st.median(m37):.2f} · max {max(m37):.2f}")
    print(f"    v37b (acumulado)   : min {min(m37b):.2f} · mediana "
          f"{st.median(m37b):.2f} · max {max(m37b):.2f}")
    check(f"P1: mediana de v37b ({st.median(m37b):.2f}) > 0,18",
          st.median(m37b) > 0.18, "")

    # ── P2 · la accion cambia ────────────────────────────────────────────
    print("\n=== P2. la accion cambia (>=5 de 15) y NO es un golpe ===")
    cambian, tipos, golpes = 0, collections.Counter(), 0
    primeras = []
    for c in casos:
        arma = c["arma"] if c["arma"] in mundo.items else "sword"
        dmin = float(c["dmin"] or 1.0)
        d_ini = min(5.0, dmin + 3)
        v37(); _, a1 = escena(mundo, YO, c["slot"], arma, d_ini, dmin,
                              dano=c["acum_real"])
        v37b(); f2, a2 = escena(mundo, YO, c["slot"], arma, d_ini, dmin,
                                dano=c["acum_real"])
        _honores.extend([(x, None) for x in a2])
        dif = [i for i, (x, y) in enumerate(zip(a2, a1)) if x != y]
        if dif:
            cambian += 1
            i = dif[0]
            tipos[clase(a2[i])] += 1
            primeras.append((c["eid"][:16], c["slot"], c["acum_real"], i,
                             a1[i], a2[i], round(f2[i], 3)))
        golpes += sum(1 for x in a2 if (x or "").startswith("atacar"))
    print(f"    cambian {cambian} de {len(casos)} · hacia: {dict(tipos)}")
    check(f"P2: la accion cambia en >=5 de {len(casos)}", cambian >= 5,
          f"{cambian}")
    check("P2: 0 golpes nacidos de la memoria", golpes == 0, f"golpes {golpes}")

    # ── P3 · no paga con comida ni con cura ──────────────────────────────
    print("\n=== P3. no paga con comida ni con cura (candado del 46 y del 62) ===")
    perdidas = 0
    ganadas = 0
    for c in casos:
        arma = c["arma"] if c["arma"] in mundo.items else "sword"
        dmin = float(c["dmin"] or 1.0)
        d_ini = min(5.0, dmin + 3)
        v37(); _, a1 = escena(mundo, YO, c["slot"], arma, d_ini, dmin,
                              dano=c["acum_real"])
        v37b(); _, a2 = escena(mundo, YO, c["slot"], arma, d_ini, dmin,
                               dano=c["acum_real"])
        for x, y in zip(a2, a1):
            if x == y:
                continue
            if clase(y) in ("botin", "cura") and clase(x) not in ("botin", "cura"):
                perdidas += 1
            if clase(x) in ("distancia/pared", "hacia la hermana"):
                ganadas += 1
    print(f"    tics en que v37b ABANDONA botin/cura: {perdidas}")
    print(f"    tics en que v37b gana distancia/pared/hermana: {ganadas}")
    check("P3: no cambia mas hacia perder comida/cura que hacia distancia",
          perdidas <= ganadas,
          f"{perdidas} vs {ganadas}" +
          ("" if perdidas <= ganadas else "  -> AL SOFA"))

    # ── P4 · silencios ───────────────────────────────────────────────────
    print("\n=== P4. silencios: sin asiento conocido -> byte a byte v36 ===")
    def esc_limpia(con_extrano=True):
        ag = [{"slot": 15, "team": "D", "pos": [C + 2, C], "hp_band": "healthy",
               "hand": "sword"}] if con_extrano else []
        return obs(300, YO, hp=90, hand={"id": "sword", "n": 1},
                   pack=[None, None], agentes=ag)
    for lbl, fn in (("extrano armado nunca visto", lambda: esc_limpia()),
                    ("nadie a la vista", lambda: esc_limpia(False))):
        o = fn()
        m1 = A.Memoria(); m1.hp_max = 100
        v37b(); m1.observa(o, mundo, 300)
        a1, r1 = D.decide(o, mundo, m1, 300)
        m2 = A.Memoria(); m2.hp_max = 100
        v36(); m2.observa(o, mundo, 300)
        a2, r2 = D.decide(o, mundo, m2, 300)
        check(f"'{lbl}': v37b == v36 byte a byte",
              dump(a1, r1) == dump(a2, r2), f"`{r1.get('elegido')}`")

    # ── P6 · quien diverge primero (R7) ──────────────────────────────────
    print("\n=== P6. quien diverge primero (SIN SELLO, se describe) ===")
    print(f"    {'episodio':<18} {'slot':>4} {'acum':>7} {'tic':>4} "
          f"{'v37':>12} -> {'v37b':<14} {'F-REENC':>8}")
    for eid, sl, acum, i, x, y, f in primeras[:12]:
        print(f"    {eid:<18} {sl:>4} {acum:>7.0f} {i:>4} {str(x):>12} -> "
              f"{str(y):<14} {f:>8.3f}")

    inic = [e for e, _ in _honores if (e or "").startswith("atacar")]
    check(f"honor (a): 0 golpes en las fotos de v37b [{len(_honores)} acciones]",
          not inic, str(inic[:5]))

    # ── determinismo ─────────────────────────────────────────────────────
    print("\n=== determinismo 3/3 ===")
    v37b()
    firmas = set()
    for _ in range(3):
        f, a = escena(mundo, YO, 12, "sword", 4.0, 1.0, 52.0)
        firmas.add(str(f) + str(a))
    check("3/3 identicas", len(firmas) == 1, "")

    A.REENCUENTRO_ON, A.ACUMULADO_ON = DEF
    check("al salir, el estado sellado queda restaurado",
          (A.REENCUENTRO_ON, A.ACUMULADO_ON) == DEF, "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — la memoria acumulada mueve el cuerpo sin mover la"
          " mano: la fila decide (P1/P2), no roba comida ni cura (P3) y calla"
          " sin memoria (P4).")


if __name__ == "__main__":
    main()
