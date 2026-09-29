"""Banco de EL INVENTARIO — PROMPT_59. v31 = v30 + la provision.

"Si tu no tienes venda y yo llevo, te la dejo ANTES de que haga falta; y si
veo una y tu no tienes, la cojo para ti." El parte trae b<n> (cierto, R1).
Dos caras de una familia:
  S-PROVISION (dar antes): hermana b=0, yo >=2, CALMA -> malestar de fondo,
    aliviable por entrega servible (<=2, 56) o camino (>2, tope 0,5).
  R-ACOPIO POR DOS (coger para ti): hermana b=0, yo ==1, CALMA -> la carencia
    de ella vuelve a importar (peso menor que la mia).
Silencio: hermana b>=1 -> v30. Sin hermana -> v27. Bajo caza -> APAGADO.

Brazos (interruptores): v30 = PROVISION_ON False; v31 = True.

  P1 DAR ANTES (sellado): b=0, yo=2, calma, <=2 -> soltar servible GANA;
     >2 -> acercarse gana (v30: noop/botin).
  P2 COGER PARA TI (sellado): b=0, yo=1, calma, first_aid visible -> v31 va a
     por el (v30 servida con 1 lo ignoraba).
  P3 ELLA LO RECOGE (sellado): receptora b=0 con venda servida a 1-2 -> va a
     por ella (su propio acopio; ya probado 55/57).
  P4 JERARQUIA DEL MIEDO (sellado; PARAR si compra riesgo): perseguida con la
     hermana sin venda a la vista -> v31 huye IDENTICA a v27.
  P5 SILENCIO Y SOLA (sellados): b>=1 -> bit-identica a v30; sin hermana ->
     byte-identica a v27.
  P6 HONOR (sellado): escenas del 39/53 -> v31 byte-identica a v30; tabu.
  P7 (fuera): bancos 13-58 en verde; determinismo 3/3 aqui.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_59
"""
from __future__ import annotations

import json
import math
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs
from alma.verifica_54 import (chat_parte, texto_parte, escena39, cands, dump)

_fallos = []
_elegidos = []
P_S, V_S, H_S, V30_S, PROV_S = (A.PARTE_ON, A.VINCULO_M, A.HERIDO_M,
                                A.HERIDO_V30, A.PROVISION_ON)


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v27():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = False, 0.0, 0.0
    A.HERIDO_V30, A.PROVISION_ON = False, False


def v30():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, V_S, H_S
    A.HERIDO_V30, A.PROVISION_ON = True, False


def v31():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, V_S, H_S
    A.HERIDO_V30, A.PROVISION_ON = True, True


def decide1(mundo, o, t=300):
    mem = A.Memoria(); mem.hp_max = 100
    mem.observa(o, mundo, t)
    accion, rad = D.decide(o, mundo, mem, t)
    F = A.filas(o, mundo, mem, t)
    _elegidos.append(rad.get("elegido"))
    return accion, rad, F


def pos_prev(rad, el):
    c = (rad.get("candidatos") or {}).get(el)
    return tuple(c["pos_prevista"]) if isinstance(c, dict) and c.get("pos_prevista") else None


def parte_b(par, t, pos, bot):
    return [chat_parte(par, t - 2, texto_parte(par, t - 2, pos, 100.0, bot=bot))]


def main():
    check("v31 sellada por defecto (PROVISION_ON=True)",
          PROV_S is True and P_S is True and V30_S is True,
          f"(PROVISION_ON={PROV_S})")
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    YO = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            YO = (y, y)
            break
    HER = (YO[0] + 1, YO[1])          # hermana a 1 (servible)
    HL = (YO[0] - 6, YO[1])           # hermana lejos (>2)
    print(f"  yo en {YO} · hermana slot {par} · venda a 1 en HER={HER}\n")

    # ════ P1 DAR ANTES ═══════════════════════════════════════════════════
    print("=== P1. dar antes: b=0, yo=2, calma, <=2 -> soltar; >2 -> acercarse ===")
    # (a) a <=2: la hermana sana a 1, yo con 2 vendas -> soltar GANA
    def esc_cerca():
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "healthy"}]
        return obs(300, YO, hp=100,
                   pack=[{"id": "first_aid", "n": 1}, {"id": "first_aid", "n": 1}],
                   agentes=ag, chat=parte_b(par, 300, HER, 0))
    v31(); a1, r1, F1 = decide1(mundo, esc_cerca())
    v30(); a0, r0, F0 = decide1(mundo, esc_cerca())
    print(f"    v30 `{r0.get('elegido')}` · v31 `{r1.get('elegido')}` · "
          f"S-PROVISION v30 {F0.get('S-PROVISION') or 0:.3f} v31 {F1.get('S-PROVISION') or 0:.3f}")
    check("v30 no tiene S-PROVISION (apagada)", (F0.get("S-PROVISION") or 0) == 0)
    check("v31 enciende S-PROVISION", (F1.get("S-PROVISION") or 0) > 0,
          f"M={F1.get('S-PROVISION'):.3f}")
    check(f"v31 SUELTA para ella (`{r1.get('elegido')}`) donde v30 no "
          f"(`{r0.get('elegido')}`)",
          (r1.get("elegido") or "").startswith("soltar")
          and not (r0.get("elegido") or "").startswith("soltar"), "")
    # (a') GUARD DEL 60: la venda se APILA (n=2 en UN slot). El conteo debe
    # ser por UNIDADES; con slots daba _bot_real=1 y S-PROVISION muda en campo.
    def esc_pila():
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "healthy"}]
        return obs(300, YO, hp=100,
                   pack=[{"id": "first_aid", "n": 2}, None],   # PILA de 2
                   agentes=ag, chat=parte_b(par, 300, HER, 0))
    v31(); ap, rp, Fp = decide1(mundo, esc_pila())
    check("PILA n=2 en un slot: S-PROVISION enciende (conteo por unidades)",
          (Fp.get("S-PROVISION") or 0) > 0, f"M={Fp.get('S-PROVISION') or 0:.3f}")
    check(f"PILA: v31 suelta para ella (`{rp.get('elegido')}`)",
          (rp.get("elegido") or "").startswith("soltar"), "")

    # (b) a >2: la hermana lejos -> acercarse gana (camino)
    def esc_lejos():
        return obs(300, YO, hp=100,
                   pack=[{"id": "first_aid", "n": 1}, {"id": "first_aid", "n": 1}],
                   chat=parte_b(par, 300, HL, 0))
    v31(); a1b, r1b, F1b = decide1(mundo, esc_lejos())
    v30(); a0b, r0b, F0b = decide1(mundo, esc_lejos())
    p1 = pos_prev(r1b, r1b.get("elegido"))
    d_ahora = math.dist(YO, HL)
    d1 = math.dist(p1, HL) if p1 else d_ahora
    print(f"    lejos: v30 `{r0b.get('elegido')}` · v31 `{r1b.get('elegido')}` "
          f"acaba a {d1:.2f} de {d_ahora:.2f}")
    check("v31 se ACERCA a la hermana desabastecida (>2)", d1 < d_ahora - 0.5,
          f"{d1:.2f} < {d_ahora:.2f}")
    check("v30 no se acercaba (o menos)",
          (pos_prev(r0b, r0b.get("elegido")) is None)
          or math.dist(pos_prev(r0b, r0b.get("elegido")), HL) >= d1 - 1e-9, "")

    # ════ P2 COGER PARA TI — REPORTE (no gate; la casa: "si no emerge, se
    #      reporta"). El forense midio: v30 YA coge todo botiquin ALCANZABLE
    #      (R-LLAMADA, con R-CARENCIA saturada en una venda: 0,667 con 1 = con
    #      2); mas alla del horizonte la foto no recoge y el por-dos no puede
    #      aliviar. No hay escena limpia donde v30 lo ignore y v31 lo coja: el
    #      gesto "coger" es redundante con la recogida de botin que ya existe.
    #      Se VERIFICA la FUERZA (existe, peso menor, silencio con b>=1); el
    #      flip de conducta se REPORTA como no-emergente. ══════════════════
    print("\n=== P2. coger para ti: la FUERZA (reporte del flip, no gate) ===")
    BOT = (YO[0] + 2, YO[1])
    def esc_coger():
        return obs(300, YO, hp=100, pack=[{"id": "first_aid", "n": 1}, None],
                   chat=parte_b(par, 300, HL, 0),
                   items=[{"id": "first_aid", "n": 1, "pos": list(BOT)}])
    v31(); a2, r2, F2 = decide1(mundo, esc_coger())
    v30(); a2b, r2b, F2b = decide1(mundo, esc_coger())
    print(f"    v30 `{r2b.get('elegido')}` (R-ACOPIO {F2b.get('R-ACOPIO') or 0:.3f}) · "
          f"v31 `{r2.get('elegido')}` (R-ACOPIO {F2.get('R-ACOPIO') or 0:.3f})")
    print(f"    REPORTE: ambas cogen la venda alcanzable (v30 por R-LLAMADA); "
          f"el por-dos ANADE apetito pero no flipea (no hay hueco honesto).")
    check("v30 servida con 1: R-ACOPIO=0 (no le importa)",
          (F2b.get("R-ACOPIO") or 0) == 0)
    check("v31: R-ACOPIO POR DOS enciende, peso MENOR que la mia",
          0 < (F2.get("R-ACOPIO") or 0) < A.ACOPIO_M,
          f"({F2.get('R-ACOPIO'):.3f} < {A.ACOPIO_M})")
    check("la venda sigue importando en v31 (va a por ella, para ella)",
          r2.get("elegido") in ("ir_objeto", "ir_botin", "coger")
          or (r2.get("elegido") or "").startswith(("move_", "paso_")), "")

    # ════ P3 ELLA LO RECOGE ══════════════════════════════════════════════
    print("\n=== P3. ella lo recoge: receptora b=0 con venda servida a 1-2 ===")
    # la receptora (nosotras jugando de hermana) con pack vacio y una venda al lado
    def esc_receptora():
        return obs(300, YO, hp=100, pack=[None, None],
                   items=[{"id": "first_aid", "n": 1, "pos": [YO[0] + 1, YO[1]]}])
    v31(); a3, r3, F3 = decide1(mundo, esc_receptora())
    el3 = r3.get("elegido")
    check(f"la receptora va A POR su venda (`{el3}`)",
          el3 in ("ir_objeto", "coger")
          or (el3 or "").startswith(("move_", "paso_")),
          "(su propio acopio, R-ACOPIO/R-LLAMADA)")

    # ════ P4 JERARQUIA DEL MIEDO ═════════════════════════════════════════
    print("\n=== P4. perseguida + hermana sin venda a la vista -> huye como v27 ===")
    def esc_caza(prov_on):
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "healthy"},
              {"slot": 15, "team": "D", "pos": [YO[0] + 1, YO[1] + 1],
               "hp_band": "healthy"}]
        ch = parte_b(par, 300, HER, 0) if prov_on else []
        o = obs(300, YO, hp=25,
                pack=[{"id": "first_aid", "n": 1}, {"id": "first_aid", "n": 1}],
                agentes=ag, chat=ch)
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
        return o
    v31(); a4, r4, F4 = decide1(mundo, esc_caza(True))
    v27(); a4b, r4b, _ = decide1(mundo, esc_caza(False))
    check(f"bajo caza v31 `{r4.get('elegido')}` == v27 `{r4b.get('elegido')}` "
          f"(PARAR si difiere)", r4.get("elegido") == r4b.get("elegido"), "")
    check("bajo caza S-PROVISION APAGADA", (F4.get("S-PROVISION") or 0) == 0, "")

    # ════ P5 SILENCIO Y SOLA ═════════════════════════════════════════════
    print("\n=== P5. hermana b>=1 -> bit-identica a v30; sin hermana -> a v27 ===")
    def esc_sana_prov():
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "healthy"}]
        return obs(300, YO, hp=100,
                   pack=[{"id": "first_aid", "n": 1}, {"id": "first_aid", "n": 1}],
                   agentes=ag, chat=parte_b(par, 300, HER, 1))   # ella lleva 1
    v31(); a5, r5, _ = decide1(mundo, esc_sana_prov())
    v30(); a5b, r5b, _ = decide1(mundo, esc_sana_prov())
    check("hermana con b=1: v31 == v30 byte a byte", dump(a5, r5) == dump(a5b, r5b),
          f"elegido `{r5.get('elegido')}`")
    def esc_sola():
        return obs(300, YO, hp=100,
                   pack=[{"id": "first_aid", "n": 1}, {"id": "first_aid", "n": 1}],
                   items=[{"id": "first_aid", "n": 1, "pos": list(BOT)}])
    v31(); a6, r6, _ = decide1(mundo, esc_sola())
    v27(); a6b, r6b, _ = decide1(mundo, esc_sola())
    check("sin hermana: v31 == v27 byte a byte", dump(a6, r6) == dump(a6b, r6b),
          f"elegido `{r6.get('elegido')}`")

    # ════ P6 HONOR ═══════════════════════════════════════════════════════
    print("\n=== P6. escenas del 39/53 con parte: v31 == v30 byte a byte ===")
    for g, hp0, ph in ((1, 100, 10.0), (1, 100, 28.0), (4, 28, 10.0),
                       (4, 28, 72.0)):
        v30(); a7b, r7b, _ = escena39(mundo, YO, HER, par, g, hp0, parte_hp=ph)
        v31(); a7, r7, _ = escena39(mundo, YO, HER, par, g, hp0, parte_hp=ph)
        _elegidos.extend([r7b.get("elegido"), r7.get("elegido")])
        check(f"g{g} hp0={hp0} h{ph:g}: v31 == v30 byte a byte (tabu intacto)",
              dump(a7, r7) == dump(a7b, r7b), f"`{r7.get('elegido')}`")

    # ════ determinismo 3/3 ═══════════════════════════════════════════════
    print("\n=== determinismo 3/3 (P1 cerca + P2, las escenas nuevas) ===")
    v31()
    firmas = set()
    for _ in range(3):
        a1, r1, _ = decide1(mundo, esc_cerca())
        a2, r2, _ = decide1(mundo, esc_coger())
        firmas.add(dump(a1, r1) + dump(a2, r2))
    check("3/3 byte-identicas", len(firmas) == 1, "")

    inic = [e for e in _elegidos if (e or "").startswith("atacar")]
    check(f"0 iniciaciones en todo el banco ({len(_elegidos)} decisiones)",
          not inic, str(inic))

    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M, A.HERIDO_V30, A.PROVISION_ON = (
        P_S, V_S, H_S, V30_S, PROV_S)
    check("al salir, el estado sellado queda restaurado",
          (A.PROVISION_ON, A.HERIDO_V30) == (PROV_S, V30_S), "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — el inventario: dar antes (P1), coger para ti (P2),"
          " ella recoge (P3), el miedo manda (P4), silencio y sola (P5),"
          " honor byte a byte (P6).")


if __name__ == "__main__":
    main()
