"""Banco de DAR DE LO QUE TE FALTA — PROMPT_61. v32 = v31 con S-PROVISION a b>=1.

La generosidad no espera excedente: doy mi UNICA venda cuando ella esta peor
que yo, SIN umbral escrito. Lo decide el equilibrio de fuerzas — mi cuesta
(usar_botiquin me sana; F-DANO convexa) contra su peso (S-HERIDO + S-PROVISION)
— y la foto del soltar con b=1 carga con el vacio real: tras soltar, mi venda
a bordo = 0, y R-ACOPIO escala con MI cuesta (PROVISION_SELF x F-DANO) SOLO en
la foto que regala (hp sin cambiar; usar, que sana, queda exento). Esa foto
honesta ES la prudencia.

Brazos (interruptores): v31 = PROVISION_B_MIN=2; v32 = 1.

  P1 DA CUANDO PUEDE (sellado): yo hp>=80 con b=1, ella hp<=30 con b=0, calma,
     <=2 -> soltar GANA; a >2 -> acercarse gana.
  P2 SE LA QUEDA CUANDO NO PUEDE (sellado): yo hp<=30 con b=1, ella hp<=30 ->
     soltar PIERDE (mi cuesta manda). Y yo hp<=30, ella hp>=80 -> nada.
  P3 LA FRONTERA (radiografia, sin gate): barrido (mi hp, su hp); la mesa NO
     sella el cruce.
  P4 JERARQUIA DEL MIEDO (sellado; PARAR si compra riesgo): perseguida ->
     idéntica a v27; S-PROVISION apagada bajo caza.
  P5 SILENCIOS (sellados): ella b>=1 -> idéntica a v31; sin hermana -> v27.
  P6 HONOR (sellado): escenas del 39/53 -> v32 byte-idéntica a v31; tabu.
  P7 (fuera): bancos 13-60 en verde; determinismo 3/3 aqui.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_61
"""
from __future__ import annotations

import json
import math
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs
from alma.verifica_54 import chat_parte, texto_parte, escena39, dump

_fallos = []
_elegidos = []
S = (A.PARTE_ON, A.VINCULO_M, A.HERIDO_M, A.HERIDO_V30, A.PROVISION_ON,
     A.PROVISION_B_MIN)


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v27():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = False, 0.0, 0.0
    A.HERIDO_V30, A.PROVISION_ON = False, False


def v31():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, S[1], S[2]
    A.HERIDO_V30, A.PROVISION_ON, A.PROVISION_B_MIN = True, True, 2


def v32():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, S[1], S[2]
    A.HERIDO_V30, A.PROVISION_ON, A.PROVISION_B_MIN = True, True, 1


def banda_de(hp):
    return "healthy" if hp > 66 else ("hurt" if hp >= 33 else "critical")


def decide1(mundo, o, t=300):
    mem = A.Memoria(); mem.hp_max = 100
    mem.observa(o, mundo, t)
    a, r = D.decide(o, mundo, mem, t)
    F = A.filas(o, mundo, mem, t)
    _elegidos.append(r.get("elegido"))
    return a, r, F


def pos_prev(rad, el):
    c = (rad.get("candidatos") or {}).get(el)
    return tuple(c["pos_prevista"]) if isinstance(c, dict) and c.get("pos_prevista") else None


def main():
    check("v32 sellada por defecto (PROVISION_B_MIN=1)",
          S[5] == 1 and S[4] is True, f"(B_MIN={S[5]})")
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    YO = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            YO = (y, y)
            break
    HER = (YO[0] + 1, YO[1])
    HL = (YO[0] - 6, YO[1])
    print(f"  yo en {YO} · hermana slot {par}\n")

    def esc(mihp, suhp, her=HER, b_mia=1):
        ag = [{"slot": par, "team": mundo.team, "pos": list(her),
               "hp_band": banda_de(suhp)}]
        ch = [chat_parte(par, 298, texto_parte(par, 298, her, suhp, bot=0))]
        return obs(300, YO, hp=mihp, pack=[{"id": "first_aid", "n": b_mia}, None],
                   agentes=ag, chat=ch)

    def clase(el):
        if (el or "").startswith("soltar"):
            return "DAR"
        if el == "usar_botiquin":
            return "USAR"
        return el

    # ════ P1 DA CUANDO PUEDE ═════════════════════════════════════════════
    print("=== P1. da cuando puede: yo>=80 b=1, ella<=30 b=0, calma ===")
    for mihp in (95, 80):
        for suhp in (10, 25):
            v32(); a, r, F = decide1(mundo, esc(mihp, suhp))
            check(f"yo{mihp} ella{suhp} (<=2): soltar GANA (`{clase(r.get('elegido'))}`)",
                  (r.get("elegido") or "").startswith("soltar"),
                  f"S-PROV={F.get('S-PROVISION') or 0:.3f}")
    # a >2: acercarse
    v32(); a, r, F = decide1(mundo, esc(95, 15, her=HL))
    p = pos_prev(r, r.get("elegido"))
    d = math.dist(p, HL) if p else math.dist(YO, HL)
    check(f"yo95 ella15 a >2: se ACERCA (acaba a {d:.2f} de {math.dist(YO,HL):.2f})",
          d < math.dist(YO, HL) - 0.5, "")

    # ════ P2 SE LA QUEDA CUANDO NO PUEDE ═════════════════════════════════
    print("\n=== P2. se la queda cuando no puede: mi cuesta manda ===")
    for suhp in (8, 20, 30):
        v32(); a, r, F = decide1(mundo, esc(25, suhp))
        check(f"yo25 ella{suhp} (ambas<=30): soltar PIERDE (`{clase(r.get('elegido'))}`)",
              not (r.get("elegido") or "").startswith("soltar"), "")
    for suhp in (10, 25):
        v32(); a, r, F = decide1(mundo, esc(10, suhp))
        check(f"yo10 ella{suhp}: soltar PIERDE (`{clase(r.get('elegido'))}`)",
              not (r.get("elegido") or "").startswith("soltar"), "")
    # yo<=30, ella>=80 -> nada (S-HERIDO calla)
    v32(); a, r, F = decide1(mundo, esc(25, 95))
    check(f"yo25 ella95 (sana): NO da (`{clase(r.get('elegido'))}`), S-HERIDO calla",
          not (r.get("elegido") or "").startswith("soltar")
          and (F.get("S-HERIDO") or 0) == 0, "")

    # ════ P3 LA FRONTERA (radiografia, sin gate) ═════════════════════════
    print("\n=== P3. la frontera (radiografia; la mesa NO sella el cruce) ===")
    print("         su_hp:    8    20    40    70    95")
    for mihp in (95, 80, 60, 40, 25, 10):
        row = []
        for suhp in (8, 20, 40, 70, 95):
            v32(); _, r, _ = decide1(mundo, esc(mihp, suhp))
            row.append(clase(r.get("elegido")))
        print(f"    mi_hp {mihp:3}: " + " ".join(f"{c:5}" for c in row))
    print("    (diagonal: sano DA, herido USA — mi cuesta vs su peso)")

    # ════ P4 JERARQUIA DEL MIEDO ═════════════════════════════════════════
    print("\n=== P4. perseguida + hermana sin venda -> huye como v27 ===")
    def esc_caza(prov):
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "healthy"},
              {"slot": 15, "team": "D", "pos": [YO[0] + 1, YO[1] + 1],
               "hp_band": "healthy"}]
        ch = [chat_parte(par, 298, texto_parte(par, 298, HER, 20, bot=0))] if prov else []
        o = obs(300, YO, hp=90, pack=[{"id": "first_aid", "n": 1}, None],
                agentes=ag, chat=ch)
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
        return o
    v32(); a4, r4, F4 = decide1(mundo, esc_caza(True))
    v27(); a4b, r4b, _ = decide1(mundo, esc_caza(False))
    check(f"bajo caza v32 `{r4.get('elegido')}` == v27 `{r4b.get('elegido')}`",
          r4.get("elegido") == r4b.get("elegido"), "PARAR si difiere")
    check("bajo caza S-PROVISION APAGADA", (F4.get("S-PROVISION") or 0) == 0, "")

    # ════ P5 SILENCIOS ═══════════════════════════════════════════════════
    print("\n=== P5. ella b>=1 -> idéntica a v31; sin hermana -> v27 ===")
    def esc_ella_con(mihp):
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "hurt"}]
        ch = [chat_parte(par, 298, texto_parte(par, 298, HER, 40, bot=1))]  # ella lleva 1
        return obs(300, YO, hp=mihp, pack=[{"id": "first_aid", "n": 1}, None],
                   agentes=ag, chat=ch)
    v32(); a5, r5, _ = decide1(mundo, esc_ella_con(95))
    v31(); a5b, r5b, _ = decide1(mundo, esc_ella_con(95))
    check("ella con b=1: v32 == v31 byte a byte", dump(a5, r5) == dump(a5b, r5b),
          f"`{r5.get('elegido')}`")
    def esc_sola(mihp):
        return obs(300, YO, hp=mihp, pack=[{"id": "first_aid", "n": 1}, None])
    v32(); a6, r6, _ = decide1(mundo, esc_sola(25))
    v27(); a6b, r6b, _ = decide1(mundo, esc_sola(25))
    check("sin hermana: v32 == v27 byte a byte", dump(a6, r6) == dump(a6b, r6b),
          f"`{r6.get('elegido')}`")

    # ════ P6 HONOR ═══════════════════════════════════════════════════════
    print("\n=== P6. escenas del 39/53 con parte: v32 == v31 byte a byte ===")
    for g, hp0, ph in ((1, 100, 10.0), (1, 100, 28.0), (4, 28, 10.0), (4, 28, 72.0)):
        v31(); a7b, r7b, _ = escena39(mundo, YO, HER, par, g, hp0, parte_hp=ph)
        v32(); a7, r7, _ = escena39(mundo, YO, HER, par, g, hp0, parte_hp=ph)
        _elegidos.extend([r7b.get("elegido"), r7.get("elegido")])
        check(f"g{g} hp0={hp0} h{ph:g}: v32 == v31 byte a byte (tabu intacto)",
              dump(a7, r7) == dump(a7b, r7b), f"`{r7.get('elegido')}`")

    # ════ determinismo 3/3 ═══════════════════════════════════════════════
    print("\n=== determinismo 3/3 (P1 dar + P2 quedarse) ===")
    v32()
    firmas = set()
    for _ in range(3):
        a1, r1, _ = decide1(mundo, esc(95, 15))
        a2, r2, _ = decide1(mundo, esc(25, 20))
        firmas.add(dump(a1, r1) + dump(a2, r2))
    check("3/3 byte-identicas", len(firmas) == 1, "")

    inic = [e for e in _elegidos if (e or "").startswith("atacar")]
    check(f"0 iniciaciones ({len(_elegidos)} decisiones)", not inic, str(inic))

    (A.PARTE_ON, A.VINCULO_M, A.HERIDO_M, A.HERIDO_V30, A.PROVISION_ON,
     A.PROVISION_B_MIN) = S
    check("al salir, el estado sellado queda restaurado",
          (A.PROVISION_B_MIN, A.PROVISION_ON) == (S[5], S[4]), "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — dar de lo que te falta: da cuando puede (P1), se la"
          " queda cuando no (P2), el miedo manda (P4), silencios (P5), honor"
          " byte a byte (P6).")


if __name__ == "__main__":
    main()
