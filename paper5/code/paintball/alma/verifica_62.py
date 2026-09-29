"""Banco de LA COMPANIA — PROMPT_62. v33 = v32 + S-COMPANIA · CANDADO.

Estado sellado que este banco verifica (patron del 46/53): LAS DOS ANCLAS DE
LA MESA SON INCOMPATIBLES. El barrido de COMPANIA_TECHO lo cierra:
  - por debajo de 0,22 la fila no cambia NADA (ni junta);
  - de 0,22 en adelante lo unico que cambia es que PIERDE COMIDA (ancla 2).
Y no hace falta: con la hermana HACIA EL CENTRO, el ANILLO YA LAS JUNTA (v32
sin fila acaba a 1-2). La fila queda APAGADA (A.COMPANIA_ON=False) con el
motivo grabado en la tabla.

  P1 SE JUNTAN EN CALMA (sellado): REPRODUCIDO SIN FILA — con la hermana
     hacia el centro, v32 (sin compania) ya acaba a <=3. El sello se cumple
     por el anillo, no por la fila; y en la escena tangencial NINGUN techo
     inferior al hambre acerca (medido).
  P2 NO PASA HAMBRE (sellado): ROTO por la fila a techo >=0,22 — reproducido
     aqui como medida del candado (v32 coge la racion, v33 no).
  P3 JERARQUIA DEL MIEDO (sellado): con el candado echado, v33==v32==v27 bajo
     caza; y con el taller encendido, la fila esta APAGADA bajo caza (gate).
  P4 EL ANILLO MANDA (sellado): con el anillo mordiendo (<5 s para arder), la
     fila no enciende ni con el taller (gate por inminencia, no por valor:
     F-ANTICIPACION vale ~0,2 de FONDO en todo el mapa).
  P5 SILENCIOS (sellados): sin hermana / a <=d0 -> byte-identico a v32.
  P6 HONOR (sellado): escenas del 39/53 -> byte-identicas a v32.
  P7 (fuera): bancos 13-61 en verde; determinismo 3/3 aqui.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_62
"""
from __future__ import annotations

import math
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs
from alma.verifica_54 import chat_parte, texto_parte, escena39, dump

_fallos = []
_elegidos = []
DEF = (A.COMPANIA_ON, A.COMPANIA_TECHO)


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v27():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = False, 0.0, 0.0
    A.HERIDO_V30, A.PROVISION_ON, A.COMPANIA_ON = False, False, False


def v32():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, 1.0, 1.8
    A.HERIDO_V30, A.PROVISION_ON, A.PROVISION_B_MIN = True, True, 1
    A.COMPANIA_ON = False


def v33(techo=0.22):
    v32()
    A.COMPANIA_ON, A.COMPANIA_TECHO = True, techo


def escena(mundo, par, YO, HER, T=100, botin=None, hp=100, caza=False,
           bh=1, pack=None):
    ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
           "hp_band": "healthy"}]
    if caza:
        ag.append({"slot": 15, "team": "D", "pos": [YO[0] + 1, YO[1] + 1],
                   "hp_band": "healthy"})
    ch = [chat_parte(par, T - 2, texto_parte(par, T - 2, HER, 100, bot=bh))]
    items = [{"id": botin[0], "n": 1, "pos": list(botin[1])}] if botin else []
    o = obs(T, YO, hp=hp, pack=pack or [{"id": "first_aid", "n": 1}, None],
            agentes=ag, chat=ch, items=items)
    if caza:
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
    return o


def roll(mundo, par, YO, HER, n=8, T0=100, botin=None):
    """Camina n tics y devuelve (dist final a la hermana, ¿cogio el botin?)."""
    pos = tuple(YO)
    mem = A.Memoria(); mem.hp_max = 100
    cog = False
    for i in range(n):
        t = T0 + i
        o = escena(mundo, par, pos, HER, T=t, botin=None if cog else botin)
        mem.observa(o, mundo, t)
        a, r = D.decide(o, mundo, mem, t)
        e = r.get("elegido")
        _elegidos.append(e)
        c = (r.get("candidatos") or {}).get(e)
        pp = c.get("pos_prevista") if isinstance(c, dict) else None
        if pp:
            pos = tuple(pp)
        if botin and pos == tuple(botin[1]):
            cog = True
    return round(math.dist(pos, HER), 1), cog


def main():
    check("EL CANDADO: la compania esta APAGADA por defecto",
          DEF[0] is False, "(motivo grabado en la tabla — anclas incompatibles)")
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    C = mundo.arena_size // 2
    print(f"  centro {C},{C} · d0={A.COMPANIA_D0} · techo barrido {DEF[1]}\n")

    # ════ P1 SE JUNTAN EN CALMA — reproducido SIN fila ═══════════════════
    print("=== P1. se juntan en calma: el ANILLO ya las junta (sin fila) ===")
    for YO, HER, lbl in (((C, C + 8), (C, C - 2), "d10, ella hacia el centro"),
                         ((C - 8, C), (C - 1, C), "d7, ella hacia el centro"),
                         ((C + 6, C + 6), (C, C + 1), "d~7 diagonal")):
        v32(); d32, _ = roll(mundo, par, YO, HER)
        v33(); d33, _ = roll(mundo, par, YO, HER)
        check(f"{lbl}: v32 (SIN fila) ya acaba a {d32} <= 3",
              d32 <= 3.0, f"(v33 acaba a {d33})")
    # y la escena tangencial: ningun techo por debajo del hambre acerca
    YOt, HERt = (C, C + 6), (C - 10, C + 6)
    v32(); dt32, _ = roll(mundo, par, YOt, HERt)
    filas_t = []
    for techo in (0.05, 0.10, 0.15, 0.22, 0.35, 0.5):
        v33(techo); dt, _ = roll(mundo, par, YOt, HERt)
        filas_t.append((techo, dt))
    print(f"    tangencial (ella NO hacia el centro): v32 {dt32} · v33 por techo: "
          + " ".join(f"{t}->{d}" for t, d in filas_t))
    check("tangencial: NINGUN techo acerca (la fila no junta donde haria falta)",
          all(abs(d - dt32) < 0.05 for _, d in filas_t), "")

    # ════ P2 NO PASA HAMBRE — la medida del candado ══════════════════════
    print("\n=== P2. no pasa hambre: ROTO a techo >= 0,22 (medida del candado) ===")
    YOh, HERh = (C, C + 4), (C, C - 4)
    BOT = ("rations", (C, C + 6))          # a 2, en direccion OPUESTA a ella
    v32(); _, cog32 = roll(mundo, par, YOh, HERh, botin=BOT)
    check(f"v32 (sin fila) COGE la racion a 2", cog32, "")
    rotos = []
    for techo in (0.05, 0.10, 0.15, 0.22, 0.35, 0.5):
        v33(techo); _, cog = roll(mundo, par, YOh, HERh, botin=BOT)
        rotos.append((techo, cog))
    print("    ¿coge la racion? por techo: "
          + " ".join(f"{t}->{'SI' if c else 'NO'}" for t, c in rotos))
    check("CANDADO reproducido: de 0,22 en adelante la fila le hace PERDER la"
          " racion (ancla 2 rota)",
          any(not c for t, c in rotos if t >= 0.22)
          and all(c for t, c in rotos if t < 0.22),
          "(y por debajo de 0,22 la fila es inerte: no junta ni quita)")

    # ════ P3 JERARQUIA DEL MIEDO ═════════════════════════════════════════
    print("\n=== P3. bajo caza: identica a v27; la fila apagada por el gate ===")
    YOc, HERc = (C, C + 4), (C, C - 4)
    v33(0.35)
    o = escena(mundo, par, YOc, HERc, caza=True, hp=40)
    mem = A.Memoria(); mem.hp_max = 100; mem.observa(o, mundo, 100)
    F = A.filas(o, mundo, mem, 100)
    a33, r33 = D.decide(o, mundo, mem, 100)
    v27()
    o2 = escena(mundo, par, YOc, HERc, caza=True, hp=40)
    mem2 = A.Memoria(); mem2.hp_max = 100; mem2.observa(o2, mundo, 100)
    a27, r27 = D.decide(o2, mundo, mem2, 100)
    _elegidos.extend([r33.get("elegido"), r27.get("elegido")])
    check("bajo caza S-COMPANIA APAGADA (gate)", (F.get("S-COMPANIA") or 0) == 0, "")
    check(f"bajo caza v33 `{r33.get('elegido')}` == v27 `{r27.get('elegido')}`",
          r33.get("elegido") == r27.get("elegido"), "PARAR si difiere")

    # ════ P4 EL ANILLO MANDA ═════════════════════════════════════════════
    print("\n=== P4. anillo mordiendo (arde en <5 s): la fila no enciende ===")
    v33(0.35)
    # una casilla del borde en un tick tardio: arde ya o casi
    YOb = (2, C)
    ob = escena(mundo, par, YOb, (C, C), T=300)
    memb = A.Memoria(); memb.hp_max = 100; memb.observa(ob, mundo, 300)
    Fb = A.filas(ob, mundo, memb, 300)
    check(f"anillo mordiendo: S-COMPANIA = 0 (F-ANT {Fb.get('F-ANTICIPACION'):.3f})",
          (Fb.get("S-COMPANIA") or 0) == 0,
          "(gate por INMINENCIA: F-ANT vale ~0,2 de fondo en todo el mapa)")

    # ════ P5 SILENCIOS ═══════════════════════════════════════════════════
    print("\n=== P5. sin hermana -> v27; a <=d0 -> v32 ===")
    v33(0.35)
    o5 = obs(100, (C, C + 4), hp=100, pack=[{"id": "first_aid", "n": 1}, None])
    m5 = A.Memoria(); m5.hp_max = 100; m5.observa(o5, mundo, 100)
    a5, r5 = D.decide(o5, mundo, m5, 100)
    v27()
    m5b = A.Memoria(); m5b.hp_max = 100; m5b.observa(o5, mundo, 100)
    a5b, r5b = D.decide(o5, mundo, m5b, 100)
    _elegidos.extend([r5.get("elegido"), r5b.get("elegido")])
    check("sin hermana: v33 == v27 byte a byte", dump(a5, r5) == dump(a5b, r5b),
          f"`{r5.get('elegido')}`")
    HERd = (C, C + 5)                      # a 1 de mi: dentro de d0
    v33(0.35)
    o6 = escena(mundo, par, (C, C + 4), HERd)
    m6 = A.Memoria(); m6.hp_max = 100; m6.observa(o6, mundo, 100)
    F6 = A.filas(o6, mundo, m6, 100)
    a6, r6 = D.decide(o6, mundo, m6, 100)
    v32()
    m6b = A.Memoria(); m6b.hp_max = 100; m6b.observa(o6, mundo, 100)
    a6b, r6b = D.decide(o6, mundo, m6b, 100)
    _elegidos.extend([r6.get("elegido"), r6b.get("elegido")])
    # el silencio es sobre la SITUACION real (a <=d0 la fila calla). En las
    # FOTOS de candidatos que se ALEJAN la fila si habla —alejarse duele— y
    # eso es el diseno, no un fallo: se declara y se mide aparte.
    check("hermana a <=d0: S-COMPANIA calla en la obs REAL",
          (F6.get("S-COMPANIA") or 0) == 0, "")
    check("hermana a <=d0: misma decision que v32",
          r6.get("elegido") == r6b.get("elegido"),
          f"`{r6.get('elegido')}` (las fotos que se ALEJAN si la encienden: "
          "declarado, es el gradiente)")

    # ════ P6 HONOR ═══════════════════════════════════════════════════════
    print("\n=== P6. escenas del 39/53: v33 == v32 byte a byte ===")
    YOh2 = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            YOh2 = (y, y)
            break
    HERh2 = (YOh2[0] + 1, YOh2[1])
    for g, hp0, ph in ((1, 100, 10.0), (1, 100, 28.0), (4, 28, 72.0)):
        v32(); a7b, r7b, _ = escena39(mundo, YOh2, HERh2, par, g, hp0, parte_hp=ph)
        v33(0.35); a7, r7, _ = escena39(mundo, YOh2, HERh2, par, g, hp0, parte_hp=ph)
        _elegidos.extend([r7b.get("elegido"), r7.get("elegido")])
        check(f"g{g} hp0={hp0} h{ph:g}: v33 == v32 byte a byte (tabu intacto)",
              dump(a7, r7) == dump(a7b, r7b), f"`{r7.get('elegido')}`")

    # ════ determinismo 3/3 ═══════════════════════════════════════════════
    print("\n=== determinismo 3/3 ===")
    firmas = set()
    for _ in range(3):
        v33(0.35)
        firmas.add(str(roll(mundo, par, (C, C + 8), (C, C - 2))))
    check("3/3 identicas", len(firmas) == 1, "")

    inic = [e for e in _elegidos if (e or "").startswith("atacar")]
    check(f"0 iniciaciones ({len(_elegidos)} decisiones)", not inic, str(inic))

    A.COMPANIA_ON, A.COMPANIA_TECHO = DEF
    check("al salir, el candado queda echado", A.COMPANIA_ON is False, "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — la compania en CANDADO: el anillo ya las junta (P1),"
          " la fila solo quitaria comida (P2), gates del miedo y del anillo"
          " correctos (P3/P4), silencios y honor byte a byte (P5/P6).")


if __name__ == "__main__":
    main()
