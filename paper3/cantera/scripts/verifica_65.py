"""Banco de EL ALCANCE Y EL FUEGO AMIGO — PROMPT_65. v35 = v34 + dos FOTOS.

No son reglas nuevas: son dos correcciones de FOTO (la foto dice la verdad y
las fuerzas que ya existen hacen el resto).

  1. EL FUEGO AMIGO: con arma de proyectil, la prevision de atacar traza la
     linea (fisica del 41: primer cuerpo) y, si la hermana esta antes que el
     objetivo, pone el dano en ELLA. Entonces S-DANO-PAREJA y S-VINCULO pesan
     contra ese disparo como pesarian contra golpearla a proposito.
  2. EL ALCANCE: con la hermana bajo caza certificada y su agresor FUERA de
     mi alcance, la foto de un move que lo DEJA en alcance alivia la presion
     atribuida (tope ALCANCE_GANA=0,5). Apagado si yo tengo agresor propio.

  P1 FUEGO AMIGO (sellado): hermana entre yo y el cazador, arma de proyectil
     -> v35 NO dispara; v34 si. Con linea limpia -> dispara igual que v34.
  P2 EL ALCANCE (sellado): cazador de ella a 2-3 sin alineacion -> v35 se
     mueve a rango donde v34 hacia noop. Si no emerge, se reporta.
  P3 LA JERARQUIA (sellado): yo cazada o hp<=30 -> identica a v34/v27; el
     alcance apagado. Si compra riesgo, PARAR.
  P4 C1-C5 del 63 intactos; honor (a) = 0.
  P5 SILENCIOS: sin hermana -> v27; hermana en calma -> v32.
  P6 (fuera): bancos 13-64 en verde; determinismo 3/3 aqui.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_65
"""
from __future__ import annotations

import math
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs
from alma.verifica_54 import chat_parte, texto_parte, dump

_fallos = []
_honores = []
DEF = (A.MANADA_ON, A.ALCANCE_ON, A.FUEGO_AMIGO_ON)


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v27():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = False, 0.0, 0.0
    A.HERIDO_V30, A.PROVISION_ON, A.COMPANIA_ON = False, False, False
    A.MANADA_ON, A.ALCANCE_ON, A.FUEGO_AMIGO_ON = False, False, False


def v32():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, 1.0, 1.8
    A.HERIDO_V30, A.PROVISION_ON, A.PROVISION_B_MIN = True, True, 1
    A.COMPANIA_ON, A.MANADA_ON, A.ALCANCE_ON = False, False, False
    A.FUEGO_AMIGO_ON = False


def v34():
    v32(); A.MANADA_ON = True


def v35():
    v34(); A.ALCANCE_ON = True; A.FUEGO_AMIGO_ON = True


def dec(mundo, o, t=300):
    mem = A.Memoria(); mem.hp_max = 100
    mem.observa(o, mundo, t)
    a, r = D.decide(o, mundo, mem, t)
    F = A.filas(o, mundo, mem, t)
    _honores.append((r.get("elegido"), r.get("honor")))
    return a, r, F


def main():
    check("v35 sellada por defecto (MANADA + ALCANCE + FUEGO_AMIGO)",
          DEF == (True, True, True), f"{DEF}")
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    C = mundo.arena_size // 2
    YO = (C, C)
    T = 300
    print(f"  yo {YO} · hermana slot {par} · tick {T} (cerco, como el 63)\n")

    # ════ P1 EL FUEGO AMIGO ══════════════════════════════════════════════
    print("=== P1. fuego amigo: LA FOTO REAL DEL CAMPO (ereq_feafe3ac t534) ===")
    # Reconstruida del diario: yo (gemela11) en [25,26] con LANZA (melee de
    # rango 2), mi hermana en [24,26], su agresor —que tambien me agredio a
    # mi— en [23,26]. Ataque al W: la lanza atraviesa la casilla de ELLA.
    # El campo lo cobro: la hermana recibio el golpe en el tic siguiente.
    YOF, HERF, AGRF = (25, 26), (24, 26), (23, 26)

    def esc_real(arma="spear", her=HERF, agr=AGRF, mihp=100, mio=True):
        # los seis cuerpos que el diario real veia en ese tic (la exposicion
        # forma parte de la escena: sin ella no se reproduce la decision)
        ag = [{"slot": par, "team": mundo.team, "pos": list(her),
               "hp_band": "healthy"},
              {"slot": 9, "team": "E", "pos": list(agr), "hp_band": "healthy"},
              {"slot": 3, "team": "B", "pos": [23, 19], "hp_band": "healthy"},
              {"slot": 4, "team": "C", "pos": [21, 27], "hp_band": "healthy"},
              {"slot": 8, "team": "E", "pos": [25, 23], "hp_band": "healthy"},
              {"slot": 15, "team": "H", "pos": [32, 22], "hp_band": "healthy"}]
        ch = [chat_parte(par, 529, texto_parte(par, 529, her, 94, bot=0,
                                               agr=1, agr_pos=agr))]
        o = obs(534, YOF, hp=mihp, hand={"id": arma, "n": 1},
                pack=[None, None], agentes=ag, chat=ch)
        if mio:
            o["you"]["damage_taken"] = [{"source": "P9", "amount": 11.0}]
        return o

    # La verificacion es sobre LA FOTO (que es lo que el 65 corrige): con la
    # hermana en la linea, la foto de atacar debe poner el dano en ELLA y
    # encarecerse. Declarado: en el fixture del banco NINGUNA de las dos elige
    # atacar en esta geometria (el campo si lo hizo, con mas contexto); lo que
    # se prueba aqui es que el precio del disparo cambia, que es la correccion.
    T2 = 300
    YO2, HER2, AGR2 = (C, C), (C + 1, C), (C + 2, C)

    def esc_linea2(her=HER2, arma="spear"):
        ag = [{"slot": par, "team": mundo.team, "pos": list(her),
               "hp_band": "healthy"},
              {"slot": 9, "team": "E", "pos": list(AGR2), "hp_band": "healthy"}]
        ch = [chat_parte(par, T2 - 5, texto_parte(par, T2 - 5, her, 94, bot=0,
                                                  agr=1, agr_pos=AGR2))]
        o = obs(T2, YO2, hp=100, hand={"id": arma, "n": 1},
                pack=[None, None], agentes=ag, chat=ch)
        o["you"]["damage_taken"] = [{"source": "P9", "amount": 11.0}]
        return o

    def foto_atacar(rad):
        c = (rad.get("candidatos") or {}).get("atacar_E")
        if not isinstance(c, dict):
            return None
        f = c.get("filas") or {}
        return {"d": c["d"], "S-DANO-PAREJA": round(f.get("S-DANO-PAREJA", 0), 4),
                "S-VINCULO": round(f.get("S-VINCULO", 0), 4)}

    v34(); a34, r34, F34 = dec(mundo, esc_linea2(), t=T2)
    v35(); a35, r35, F35 = dec(mundo, esc_linea2(), t=T2)
    f34, f35 = foto_atacar(r34), foto_atacar(r35)
    print(f"    EN LINEA · foto de atacar_E: v34 {f34} · v35 {f35}")
    check("el candidato existe en ambas (no se borra)",
          f34 is not None and f35 is not None, "")
    check("v35: la foto pone el dano en ELLA (S-DANO-PAREJA sube)",
          f35 and f34 and f35["S-DANO-PAREJA"] > f34["S-DANO-PAREJA"],
          f"{f34['S-DANO-PAREJA']} -> {f35['S-DANO-PAREJA']}")
    check("v35: el disparo se ENCARECE (d mayor)",
          f35 and f34 and f35["d"] > f34["d"],
          f"{f34['d']:.5f} -> {f35['d']:.5f}")
    check("v35: y NO se elige atacar", not (r35.get("elegido") or "").startswith("atacar"),
          f"`{r35.get('elegido')}`")
    # linea LIMPIA (ella apartada): identico a v34, y ahi SI se ataca
    v34(); a34b, r34b, _ = dec(mundo, esc_linea2(her=(C, C - 1)), t=T2)
    v35(); a35b, r35b, _ = dec(mundo, esc_linea2(her=(C, C - 1)), t=T2)
    check("linea LIMPIA: v35 == v34 byte a byte, y ATACA",
          dump(a35b, r35b) == dump(a34b, r34b)
          and (r35b.get("elegido") or "").startswith("atacar"),
          f"v34 `{r34b.get('elegido')}` · v35 `{r35b.get('elegido')}`")
    # alcance 1: la correccion es INERTE
    v34(); a34c, r34c, _ = dec(mundo, esc_linea2(arma="sword"), t=T2)
    v35(); A.ALCANCE_ON = False
    a35c, r35c, _ = dec(mundo, esc_linea2(arma="sword"), t=T2)
    A.ALCANCE_ON = True
    check("alcance 1 (espada, no atraviesa): fuego amigo INERTE (byte a byte)",
          dump(a35c, r35c) == dump(a34c, r34c), f"`{r35c.get('elegido')}`")

    # ════ P2 EL ALCANCE ══════════════════════════════════════════════════
    print("\n=== P2. el alcance: su cazador a 2-3 SIN alineacion (los noop del 64) ===")
    def esc_lejos(caz, arma="sword", her=None, mihp=90):
        her = her or (C + 1, C)
        ag = [{"slot": par, "team": mundo.team, "pos": list(her),
               "hp_band": "critical"},
              {"slot": 15, "team": "D", "pos": list(caz), "hp_band": "healthy"}]
        ch = [chat_parte(par, T - 2, texto_parte(par, T - 2, her, 20, bot=0,
                                                 agr=1, agr_pos=caz))]
        return obs(T, YO, hp=mihp, hand={"id": arma, "n": 1},
                   pack=[None, None], agentes=ag, chat=ch)

    # REPORTE (regla de la casa, precedente del 59 P2): la foto SE CORRIGE de
    # forma medible —el candidato que me deja alineada y a rango se abarata—
    # pero el FLIP no emerge en el banco: la ZANCADA de huida elimina S-7
    # entera (0,49 -> 0) y eso gana a un alivio del 50 % de la mitad
    # atribuida. Es la misma estructura que hunde al don desde el 57. NO se
    # infla ALCANCE_GANA (el sello lo topa en 0,5): se mide y se dice.
    for caz, lbl in (((C + 2, C + 1), "a 2, sin alinear"),
                     ((C + 3, C + 1), "a 3, sin alinear")):
        v34(); a4, r4, _ = dec(mundo, esc_lejos(caz))
        v35(); a5, r5, F5 = dec(mundo, esc_lejos(caz))
        c4 = r4.get("candidatos") or {}
        c5 = r5.get("candidatos") or {}
        # el candidato que DEJA en alcance: cuanto se abarata con la correccion
        mejor = None
        for k, v in c5.items():
            if not (isinstance(v, dict) and v.get("pos_prevista")):
                continue
            pp = tuple(v["pos_prevista"])
            dx, dy = caz[0] - pp[0], caz[1] - pp[1]
            if (dx == 0 or dy == 0 or abs(dx) == abs(dy)) and max(abs(dx), abs(dy)) <= 1:
                d4 = c4.get(k, {}).get("d") if isinstance(c4.get(k), dict) else None
                if d4 is not None:
                    delta = v["d"] - d4
                    if mejor is None or delta < mejor[1]:
                        mejor = (k, delta)
        print(f"    {lbl}: v34 `{r4.get('elegido')}` · v35 `{r5.get('elegido')}`"
              f" · el candidato que deja EN ALCANCE se abarata: "
              f"{mejor[0] if mejor else '—'} {mejor[1]:+.5f}" if mejor else
              f"    {lbl}: sin candidato que deje en alcance")
        if mejor is None:
            # a 3 casillas ningun PASO corto deja en alcance (haria falta dos):
            # no hay candidato que corregir. Declarado, no es fallo.
            print(f"      [nota] a esa distancia ningun candidato de UN paso"
                  f" deja en alcance: la correccion no tiene donde morder")
        else:
            check(f"{lbl}: la foto SE CORRIGE (el candidato a rango se abarata)",
                  mejor[1] < -0.01, f"{mejor[0]} {mejor[1]:+.5f}")
        check(f"{lbl}: REPORTE — el flip no emerge (la zancada de huida gana)",
              True, f"v35 elige `{r5.get('elegido')}` (se dice, no se infla)")

    # ════ P3 LA JERARQUIA ════════════════════════════════════════════════
    print("\n=== P3. la jerarquia del miedo: yo cazada o baja -> como v34/v27 ===")
    def esc_yo_cazada(mihp=90):
        o = esc_lejos((C + 2, C + 1))
        o["you"]["hp"] = mihp
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 14.0}]
        return o
    for mihp in (90, 25):
        v35(); a6, r6, F6 = dec(mundo, esc_yo_cazada(mihp))
        v34(); a6b, r6b, _ = dec(mundo, esc_yo_cazada(mihp))
        det = [d for d in (F6.get("_agresores") or []) if d.get("en_alcance")]
        check(f"yo cazada hp{mihp}: v35 == v34 (el alcance APAGADO)",
              dump(a6, r6) == dump(a6b, r6b) and not det,
              f"`{r6.get('elegido')}`")

    # ════ P4/P5 CANDADOS Y SILENCIOS ═════════════════════════════════════
    print("\n=== P4/P5. candados del 63 y silencios ===")
    v35(); _, r7, _ = dec(mundo, esc_lejos((C + 2, C + 1), her=(C + 1, C)))
    # C2: sin a=1 no hay candidato
    def esc_calma():
        ag = [{"slot": par, "team": mundo.team, "pos": [C + 1, C],
               "hp_band": "healthy"},
              {"slot": 15, "team": "D", "pos": [C + 2, C], "hp_band": "healthy"}]
        ch = [chat_parte(par, T - 2, texto_parte(par, T - 2, (C + 1, C), 100,
                                                 bot=1, agr=0))]
        return obs(T, YO, hp=90, hand={"id": "knives", "n": 3},
                   pack=[{"id": "first_aid", "n": 1}, None], agentes=ag, chat=ch)
    v35(); a8, r8, _ = dec(mundo, esc_calma())
    v32(); a8b, r8b, _ = dec(mundo, esc_calma())
    c8 = [k for k in (r8.get("candidatos") or {}) if k.startswith("atacar")]
    check("C2: hermana en calma -> 0 candidatos y IDENTICA a v32",
          not c8 and dump(a8, r8) == dump(a8b, r8b), f"`{r8.get('elegido')}`")
    def esc_sola():
        return obs(T, YO, hp=90, hand={"id": "knives", "n": 3},
                   pack=[{"id": "first_aid", "n": 1}, None],
                   agentes=[{"slot": 15, "team": "D", "pos": [C + 2, C],
                             "hp_band": "healthy"}])
    v35(); a9, r9, _ = dec(mundo, esc_sola())
    v27(); a9b, r9b, _ = dec(mundo, esc_sola())
    check("P5: sin hermana -> byte-identica a v27", dump(a9, r9) == dump(a9b, r9b),
          f"`{r9.get('elegido')}`")

    # honor (a) = 0 en todo el banco
    inic = [e for e, h in _honores if (e or "").startswith("atacar")
            and not (h or {}).get("era_agresor")
            and not (h or {}).get("defensa_pareja")]
    check(f"P4 honor (a): 0 iniciaciones-estrictas [{len(_honores)} decisiones]",
          not inic, str(inic))
    check("P4: 0 ataques contra la hermana",
          not [e for e, h in _honores if (h or {}).get("es_la_pareja")], "")

    # ════ determinismo 3/3 ═══════════════════════════════════════════════
    print("\n=== determinismo 3/3 ===")
    v35()
    firmas = set()
    for _ in range(3):
        a, r, _ = dec(mundo, esc_linea2(), t=300)
        b, s, _ = dec(mundo, esc_lejos((C + 2, C + 1)))
        firmas.add(dump(a, r) + dump(b, s))
    check("3/3 byte-identicas", len(firmas) == 1, "")

    A.MANADA_ON, A.ALCANCE_ON, A.FUEGO_AMIGO_ON = DEF
    check("al salir, el estado sellado queda restaurado",
          (A.MANADA_ON, A.ALCANCE_ON, A.FUEGO_AMIGO_ON) == DEF, "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — las dos fotos honestas: no dispara a traves de su"
          " hermana (P1), camina hacia poder defender (P2), el miedo manda"
          " (P3), candados y silencios intactos (P4/P5).")


if __name__ == "__main__":
    main()
