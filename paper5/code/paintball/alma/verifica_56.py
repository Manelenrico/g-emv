"""Banco de EL CUIDADO A DISTANCIA — PROMPT_56. v30 = v29 con S-HERIDO corregida.

La autopsia del 55 dejo tres piezas; los tres arreglos son de la
especificacion del 54, no diseno nuevo:
  A) la fila se alimenta del PARTE (hp y posicion) este visible o no;
  B) la ayuda "servida" cuenta solo si ELLA puede cogerla (mas cerca de
     ella que de su agresor del parte, y no adyacente a el);
  C) el camino de ayuda: en banda y fuera de alcance, la foto que ACERCA
     alivia parcialmente — con la jerarquia del miedo por encima (bajo
     caza, apagado entero).

Brazos (interruptores, patron de la casa):
  v27: PARTE_ON=False, VINCULO_M=HERIDO_M=0
  v29: PARTE_ON=True, constantes selladas, HERIDO_V30=False
  v30: idem con HERIDO_V30=True

  P1 LA HERMANA INVISIBLE (sellado, el que falto en el 54): fuera de vista,
     parte fresco h20 con posicion, calma y botiquin -> v30 se ACERCA donde
     v29 la ignoraba.
  P2 EL DON SERVIBLE (sellado): la foto del 55 (venda a 1 de la herida,
     pegada a su cazador) -> v30 NO se da por aliviada (v29 si: el bug);
     soltar desde casilla no servible PIERDE; desde casilla servible GANA.
  P3 LA JERARQUIA DEL MIEDO (sellado; si compra riesgo, PARAR): perseguida,
     hermana en banda a distancia -> v30 huye identica a v27.
  P4 SILENCIO DEL SANO Y SOLO INTACTO (sellados): hermana >=60 -> byte-
     identica a v29; sin hermana -> byte-identica a v27.
  P5 HONOR (sellado): las escenas del 39/53 con parte -> v30 BYTE-identica a
     v29 (margenes de atacar identicos; el tabu intacto).
  P6 (fuera de este fichero): bancos 13-55 en verde; determinismo 3/3 aqui.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_56
"""
from __future__ import annotations

import json
import math
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs
from alma.verifica_54 import (chat_parte, texto_parte, banda_de, escena39,
                              cands, dump)

_fallos = []
_elegidos = []
P_SELL, V_SELL, H_SELL, V30_SELL = (A.PARTE_ON, A.VINCULO_M, A.HERIDO_M,
                                    A.HERIDO_V30)


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v27():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = False, 0.0, 0.0
    A.HERIDO_V30 = False


def v29():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, V_SELL, H_SELL
    A.HERIDO_V30 = False


def v30():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, V_SELL, H_SELL
    A.HERIDO_V30 = True


def decide1(mundo, o, t=300):
    mem = A.Memoria(); mem.hp_max = 100
    mem.observa(o, mundo, t)
    accion, rad = D.decide(o, mundo, mem, t)
    F = A.filas(o, mundo, mem, t)
    _elegidos.append(rad.get("elegido"))
    return accion, rad, F


def pos_prevista(rad, elegido):
    c = (rad.get("candidatos") or {}).get(elegido)
    if isinstance(c, dict) and c.get("pos_prevista"):
        return tuple(c["pos_prevista"])
    return None


def main():
    check("v30 sellada encendida por defecto",
          P_SELL is True and V30_SELL is True and V_SELL > 0 and H_SELL > 0,
          f"(PARTE_ON={P_SELL}, HERIDO_V30={V30_SELL}, "
          f"VINCULO={V_SELL}, HERIDO={H_SELL})")
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    YO = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            YO = (y, y)
            break
    HER = (YO[0] + 1, YO[1])
    print(f"  yo en {YO} · hermana slot {par}\n")

    # ════ P1 LA HERMANA INVISIBLE ════════════════════════════════════════
    print("=== P1. la hermana invisible: parte h20 con posicion, calma, botiquin ===")
    HL = (YO[0] - 6, YO[1])          # lejos, opuesta a la Fortaleza
    check("geometria: su casilla es pisable y esta lejos (>2)",
          not mundo.solido(*HL) and math.dist(YO, HL) > 2,
          f"HL={HL} dist={math.dist(YO, HL):.1f}")

    def esc_invisible():
        ch = [chat_parte(par, 298, texto_parte(par, 298, HL, 20.0))]
        return obs(300, YO, hp=100, pack=[{"id": "first_aid", "n": 1}, None],
                   chat=ch)

    v29(); a9, r9, F9 = decide1(mundo, esc_invisible())
    v30(); a0, r0, F0 = decide1(mundo, esc_invisible())
    d_ahora = math.dist(YO, HL)
    p9 = pos_prevista(r9, r9.get("elegido"))
    p0 = pos_prevista(r0, r0.get("elegido"))
    d9 = math.dist(p9, HL) if p9 else d_ahora
    d0 = math.dist(p0, HL) if p0 else d_ahora
    print(f"    v29 `{r9.get('elegido')}` acaba a {d9:.2f} de ella · "
          f"v30 `{r0.get('elegido')}` acaba a {d0:.2f} (ahora {d_ahora:.2f})")
    check("v29 la IGNORABA (S-HERIDO=0 sin vista)",
          (F9.get("S-HERIDO") or 0) == 0, "")
    check("v30 la SABE (S-HERIDO > 0 por el parte)",
          (F0.get("S-HERIDO") or 0) > 0,
          f"M={F0.get('S-HERIDO'):.3f}")
    check(f"v30 se ACERCA (elegido acaba a {d0:.2f} < {d_ahora:.2f})",
          d0 < d_ahora - 0.5, "")
    check("v29 no se acercaba (o menos que v30)", d9 >= d0 - 1e-9,
          f"v29 {d9:.2f} vs v30 {d0:.2f}")

    # ════ P2 EL DON SERVIBLE ═════════════════════════════════════════════
    print("\n=== P2. el don servible: la foto del 55 (venda pegada al cazador) ===")
    H2 = (YO[0] + 1, YO[1])          # la herida
    CZ = (YO[0] + 2, YO[1])          # su cazador, pegado a ella
    VB = (YO[0] + 3, YO[1])          # la venda del 55: a 2 de ella, a 1 de el

    def esc_55(mi_pos):
        ag = [{"slot": par, "team": mundo.team, "pos": list(H2),
               "hp_band": "critical"},
              {"slot": 15, "team": "D", "pos": list(CZ), "hp_band": "healthy"}]
        ch = [chat_parte(par, 298, texto_parte(par, 298, H2, 20.0,
                                               agr=1, agr_pos=CZ))]
        return obs(300, mi_pos, hp=100,
                   pack=[{"id": "first_aid", "n": 1}, None],
                   agentes=ag, chat=ch,
                   items=[{"id": "first_aid", "n": 1, "pos": list(VB)}])

    # (i) el estado: v29 se daba por aliviada; v30 no
    v29(); _, r9b, F9b = decide1(mundo, esc_55(YO))
    v30(); _, r0b, F0b = decide1(mundo, esc_55(YO))
    m29, m30 = F9b.get("S-HERIDO") or 0, F0b.get("S-HERIDO") or 0
    check(f"v29 se daba por aliviada (M {m29:.3f} = atenuada)",
          0 < m29 < 0.5 * H_SELL, "")
    check(f"v30 NO se da por aliviada (M {m30:.3f}, sin atenuar)",
          m30 > 0.5 * H_SELL and m30 > 2 * m29,
          "(la venda pegada al cazador no es ayuda)")
    # (ii) soltar desde MI casilla SERVIBLE (yo en YO: a 1 de ella, a 2 de
    # el, no adyacente a el) GANA en v30
    check("geometria servible: mi casilla a 1 de ella, no adyacente a el",
          max(abs(YO[0] - CZ[0]), abs(YO[1] - CZ[1])) > 1
          and math.dist(YO, H2) <= 2, "")
    check(f"v30: soltar GANA desde casilla servible (`{r0b.get('elegido')}`)",
          (r0b.get("elegido") or "").startswith("soltar"), "")
    check(f"v29 (el bug): soltar NO ganaba (`{r9b.get('elegido')}`)",
          not (r9b.get("elegido") or "").startswith("soltar"), "")
    # (iii) soltar desde casilla NO servible (pegada al cazador) PIERDE
    YO_MAL = (YO[0] + 2, YO[1] - 1)   # adyacente al cazador, a <=2 de ella
    check("geometria no servible: pegado al cazador, a <=2 de ella",
          max(abs(YO_MAL[0] - CZ[0]), abs(YO_MAL[1] - CZ[1])) <= 1
          and math.dist(YO_MAL, H2) <= 2
          and not mundo.solido(*YO_MAL), f"YO_MAL={YO_MAL}")
    v30(); _, r0c, F0c = decide1(mundo, esc_55(YO_MAL))
    c0c = cands(r0c)
    d_sol = c0c.get("soltar_first_aid")
    d_el = c0c.get(r0c.get("elegido"))
    check(f"v30: soltar ahi PIERDE (`{r0c.get('elegido')}`, margen "
          f"{(d_sol - d_el) if (d_sol and d_el) else float('nan'):+.3f})",
          not (r0c.get("elegido") or "").startswith("soltar")
          and d_sol is not None and d_el is not None and d_sol > d_el, "")

    # ════ P3 LA JERARQUIA DEL MIEDO ══════════════════════════════════════
    print("\n=== P3. perseguida + hermana en banda a distancia: huye identica a v27 ===")

    def esc_caza(parte_on):
        HW = (YO[0] - 6, YO[1])
        ag = [{"slot": 15, "team": "D", "pos": [YO[0] + 1, YO[1]],
               "hp_band": "healthy"}]
        ch = ([chat_parte(par, 298, texto_parte(par, 298, HW, 25.0))]
              if parte_on else [])
        o = obs(300, YO, hp=30, agentes=ag, chat=ch,
                pack=[{"id": "first_aid", "n": 1}, None])
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 14.0}]
        return o

    v30(); a0d, r0d, F0d = decide1(mundo, esc_caza(True))
    v27(); a7d, r7d, _ = decide1(mundo, esc_caza(False))
    check(f"bajo caza v30 elige `{r0d.get('elegido')}` == v27 "
          f"`{r7d.get('elegido')}` (PARAR si difiere)",
          r0d.get("elegido") == r7d.get("elegido"), "")
    check("bajo caza el camino esta APAGADO (sin `_herido_camino`)",
          F0d.get("_herido_camino") is None, "")

    # ════ P4 SILENCIO DEL SANO Y SOLO INTACTO ════════════════════════════
    print("\n=== P4. sana >=60 -> byte-identica a v29; sin hermana -> byte-identica a v27 ===")
    for ph in (75.0, 60.0):
        v29(); a9e, r9e, _ = escena39(mundo, YO, HER, par, 1, 100, parte_hp=ph)
        v30(); a0e, r0e, _ = escena39(mundo, YO, HER, par, 1, 100, parte_hp=ph)
        _elegidos.extend([r9e.get("elegido"), r0e.get("elegido")])
        check(f"h{ph:g}: v30 == v29 byte a byte",
              dump(a0e, r0e) == dump(a9e, r9e),
              f"elegido `{r0e.get('elegido')}`")
    def esc_caza_sola():
        o = obs(300, YO, hp=25,
                agentes=[{"slot": 15, "team": "D",
                          "pos": [YO[0] + 2, YO[1]], "hp_band": "healthy"}])
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
        return o

    for nombre, o_fn in (("caza sin hermana", esc_caza_sola),
                         ("paseo", lambda: obs(300, YO, hp=100))):
        v30(); a0f, r0f, _ = decide1(mundo, o_fn())
        v27(); a7f, r7f, _ = decide1(mundo, o_fn())
        check(f"'{nombre}': v30 == v27 byte a byte",
              dump(a0f, r0f) == dump(a7f, r7f),
              f"elegido `{r0f.get('elegido')}`")

    # ════ P5 HONOR ═══════════════════════════════════════════════════════
    print("\n=== P5. honor: las escenas del 39/53 con parte, v30 == v29 byte a byte ===")
    for golpes, hp0, ph in ((1, 100, 10.0), (1, 100, 28.0), (1, 100, 72.0),
                            (4, 28, 10.0), (4, 28, 28.0)):
        v29(); a9g, r9g, F9g = escena39(mundo, YO, HER, par, golpes, hp0,
                                        parte_hp=ph)
        v30(); a0g, r0g, F0g = escena39(mundo, YO, HER, par, golpes, hp0,
                                        parte_hp=ph)
        _elegidos.extend([r9g.get("elegido"), r0g.get("elegido")])
        check(f"g{golpes} hp0={hp0} h{ph:g}: v30 == v29 byte a byte "
              f"(margenes y tabu intactos)",
              dump(a0g, r0g) == dump(a9g, r9g),
              f"elegido `{r0g.get('elegido')}`")

    # ════ determinismo 3/3 ═══════════════════════════════════════════════
    print("\n=== determinismo 3/3 (P1 + P2, las escenas nuevas) ===")
    v30()
    firmas = set()
    for _ in range(3):
        a1, r1, _ = decide1(mundo, esc_invisible())
        a2, r2, _ = decide1(mundo, esc_55(YO))
        firmas.add(dump(a1, r1) + dump(a2, r2))
    check("3/3 byte-identicas", len(firmas) == 1, "")

    inic = [e for e in _elegidos if (e or "").startswith("atacar")]
    check(f"0 iniciaciones en todo el banco ({len(_elegidos)} decisiones)",
          not inic, str(inic))

    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M, A.HERIDO_V30 = (P_SELL, V_SELL,
                                                         H_SELL, V30_SELL)
    check("al salir, el estado sellado queda restaurado",
          (A.PARTE_ON, A.VINCULO_M, A.HERIDO_M, A.HERIDO_V30)
          == (P_SELL, V_SELL, H_SELL, V30_SELL), "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — el cuidado a distancia: sabe sin ver (P1), sirve"
          " de verdad (P2), el miedo manda (P3), sano y solo intactos (P4),"
          " honor byte a byte (P5).")


if __name__ == "__main__":
    main()
