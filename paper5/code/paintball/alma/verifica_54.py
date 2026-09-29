"""Banco de EL PESO DEL HERMANO — PROMPT_54. v29 = v28 + S-VINCULO + S-HERIDO.

Sofa T2b sellado [Manel]: la tabla nunca aprendio que la vida del hermano
vale mas que la de un extrano. Dos filas nuevas sobre el hecho cierto del
parte (R1: parte fresco -> exacto; banda -> solo lo que garantiza; R2:
fuerzas, no conductas — ni un candidato nuevo):

  S-VINCULO — el tabu: mi golpe previsto mata SEGURO al hermano -> acantilado
     plano (VINCULO_M), sin B.
  S-HERIDO — el cuidado: deficit del hermano bajo 60, espejo de la cuesta
     del 43 (mismos numeros sellados), aliviable SOLO por ayuda prevista
     cierta (cura en el suelo a <=2 de el — la lectura de la cesion);
     transito sin tasar (47) => constante entre fotos de huida.

Brazos del pareado (constantes, patron del 48):
  v27 / v28-candado : PARTE_ON=False, VINCULO_M=HERIDO_M=0  (identicos)
  v28-taller        : PARTE_ON=True,  VINCULO_M=HERIDO_M=0
  v29               : PARTE_ON=True,  constantes selladas

  P1 EL CANDADO RESELLADO MAS FUERTE (sellado; si no, PARAR): fotos del
     39/53 con hermano-agresor a h10/h28/h72 — margen de atacar >= vara del
     39 (+0,374) en TODAS y CRECIENTE a hp bajo; 0 iniciaciones; jamas
     elegido.
  P2 EL DON DESPIERTA (sellado, con su valvula): hermano a hp<=30 por parte,
     botiquin a bordo, sin agresor cerca -> dar/ceder GANA donde v28
     ignoraba. Si no emerge, NO se guioniza: se reporta.
  P3 LA JERARQUIA DEL MIEDO (sellado; si no, PARAR): perseguido con hermano
     herido a la vista, v29 huye IGUAL que v27.
  P4 EL SILENCIO DEL SANO (sellado): hermano >= 60 -> decisiones identicas a
     v28-candado.
  P5 EL SOLO INTACTO (sellado): sin hermano / texto ajeno -> BIT-identico a
     v27.
  P6 HONOR GENERAL (sellado): margenes contra extranos identicos (byte) sin
     hermano en juego; en escena mixta, deltas declarados; determinismo 3/3.
     (bancos 13-53: fuera de este fichero)

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_54
"""
from __future__ import annotations

import json
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma import parte as PARTE
from alma.smoke_alma import player_config, obs

_fallos = []
_elegidos = []
GOLPE = 18.0
V_SELL, H_SELL = A.VINCULO_M, A.HERIDO_M
P_SELL = A.PARTE_ON
VARA_39 = 0.374          # la vara del encargo (la menor de las dos del 39)


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v27():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = False, 0.0, 0.0


v28c = v27                # v28-candado ES v27 en decisiones (53)


def v28t():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, 0.0, 0.0


def v29():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, V_SELL, H_SELL


def dump(accion, rad):
    return json.dumps((accion, rad), sort_keys=True, default=str)


def cands(rad):
    return {k: (v["d"] if isinstance(v, dict) else v)
            for k, v in (rad.get("candidatos") or {}).items()}


def margen_atacar(rad):
    c = cands(rad)
    at = {k: v for k, v in c.items() if k.startswith("atacar")}
    el = rad.get("elegido")
    _elegidos.append(el)
    if not at or c.get(el) is None:
        return None, el, c
    return min(at.values()) - c[el], el, c


def chat_parte(par, t_emision, texto):
    return {"tick": t_emision + 2, "from": par, "channel": "team",
            "to": None, "text": texto}


def texto_parte(par, t, pos, hp, ven=0, bot=0, agr=0, agr_pos=None):
    s = f"E1 P{par} t{t} {pos[0]},{pos[1]} h{hp:g} v{ven} b{bot} a{agr}"
    if agr and agr_pos:
        s += f" {agr_pos[0]},{agr_pos[1]}"
    return s


def banda_de(hp):
    return "healthy" if hp > 66 else ("hurt" if hp >= 33 else "critical")


def escena39(mundo, YO, HER, par, golpes, hp0, parte_hp=None, tick0=300):
    """La tentacion del 39: el hermano me pega armado. Banda CONSISTENTE con
    su parte (el mundo no miente dos veces)."""
    mem = A.Memoria(); mem.hp_max = 100
    hp = float(hp0)
    t = tick0
    banda = banda_de(parte_hp) if parte_hp is not None else "healthy"
    ag = [{"slot": par, "team": mundo.team, "pos": list(HER), "hp_band": banda}]
    for _ in range(golpes):
        hp = max(1.0, hp - GOLPE)
        o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
                pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
        o["you"]["damage_taken"] = [{"source": f"P{par}", "amount": GOLPE}]
        mem.observa(o, mundo, t)
        t += 1
    ch = []
    if parte_hp is not None:
        ch = [chat_parte(par, t - 2, texto_parte(par, t - 2, HER, parte_hp))]
    o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
            pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag), chat=ch)
    mem.observa(o, mundo, t)
    accion, rad = D.decide(o, mundo, mem, t)
    F = A.filas(o, mundo, mem, t)
    return accion, rad, F


def lealtad54(mundo, YO, HER, par, parte_hp, tick0=300):
    """El don del 54: yo sano con botiquin, hermano ADYACENTE muy herido
    (banda consistente), SIN agresor cerca. Parte fresco con su hp exacto."""
    mem = A.Memoria(); mem.hp_max = 100
    banda = banda_de(parte_hp)
    ag = [{"slot": par, "team": mundo.team, "pos": list(HER), "hp_band": banda}]
    ch = [chat_parte(par, tick0 - 2,
                     texto_parte(par, tick0 - 2, HER, parte_hp))]
    o = obs(tick0, YO, hp=100, pack=[{"id": "first_aid", "n": 1}, None],
            agentes=list(ag), chat=ch)
    mem.observa(o, mundo, tick0)
    accion, rad = D.decide(o, mundo, mem, tick0)
    F = A.filas(o, mundo, mem, tick0)
    return accion, rad, F


def main():
    check("constantes selladas encendidas por defecto",
          P_SELL is True and V_SELL > 0 and H_SELL > 0,
          f"(PARTE_ON={P_SELL}, VINCULO_M={V_SELL}, HERIDO_M={H_SELL})")
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    YO = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            YO = (y, y)
            break
    HER = (YO[0] + 1, YO[1])
    CAZ = (YO[0] + 2, YO[1])
    print(f"  yo en {YO} · hermano slot {par} en {HER} · extrano slot 15 en {CAZ}")
    print(f"  VINCULO_M={V_SELL} · HERIDO_M={H_SELL} · umbral silencio "
          f"{A.HERIDO_UMBRAL} · alivio x{A.HERIDO_ATEN}\n")

    # ════ P1 EL CANDADO RESELLADO MAS FUERTE ═════════════════════════════
    print("=== P1. margen de atacar al hermano-agresor: >= vara y CRECIENTE a hp bajo ===")
    for golpes, hp0 in ((1, 100), (4, 28)):
        margenes = {}
        for ph in (72.0, 28.0, 10.0):
            v29(); _, r9, F9 = escena39(mundo, YO, HER, par, golpes, hp0,
                                        parte_hp=ph)
            m9, e9, _ = margen_atacar(r9)
            v28t(); _, r8, _ = escena39(mundo, YO, HER, par, golpes, hp0,
                                        parte_hp=ph)
            m8, _, _ = margen_atacar(r8)
            margenes[ph] = m9
            filas = {k: round(F9.get(k) or 0.0, 4)
                     for k in ("S-VINCULO", "S-HERIDO")}
            print(f"    g{golpes} hp0={hp0} h{ph:<4g} margen v28 {m8:+.5f} -> "
                  f"v29 {m9:+.5f}   filas del AHORA {filas}")
            check(f"g{golpes} hp0={hp0} h{ph:g}: margen {m9:+.5f} >= vara "
                  f"{VARA_39:+.3f}", m9 is not None and m9 >= VARA_39, "")
            check(f"g{golpes} hp0={hp0} h{ph:g}: no ataca (`{e9}`)",
                  not (e9 or "").startswith("atacar"), "")
        check(f"g{golpes} hp0={hp0}: MAS LEJOS cuanto mas bajo "
              f"(h10 {margenes[10.0]:+.4f} > h28 {margenes[28.0]:+.4f} > "
              f"h72 {margenes[72.0]:+.4f})",
              margenes[10.0] > margenes[28.0] > margenes[72.0], "")

    # ════ P2 EL DON DESPIERTA ════════════════════════════════════════════
    print("\n=== P2. hermano a hp<=30 por parte, botiquin a bordo, sin agresor: ¿gana el don? ===")
    despierta = True
    for ph in (30.0, 25.0, 15.0, 8.0):
        v29(); a9, r9, F9 = lealtad54(mundo, YO, HER, par, ph)
        v28c(); a8, r8, _ = lealtad54(mundo, YO, HER, par, ph)
        _elegidos.extend([r9.get("elegido"), r8.get("elegido")])
        c9 = cands(r9)
        d_soltar = c9.get("soltar_first_aid")
        gana = (r9.get("elegido") or "").startswith("soltar")
        despierta = despierta and gana
        print(f"    h{ph:<4g} v28 `{r8.get('elegido')}` -> v29 "
              f"`{r9.get('elegido')}`  · d(soltar)="
              f"{d_soltar if d_soltar is None else round(d_soltar, 4)}"
              f" · S-HERIDO ahora {round(F9.get('S-HERIDO') or 0, 4)}")
        check(f"h{ph:g}: el don GANA en v29 (v28 ignoraba: `{r8.get('elegido')}`)",
              gana, f"elegido `{r9.get('elegido')}`")

    # ════ P3 LA JERARQUIA DEL MIEDO ══════════════════════════════════════
    print("\n=== P3. perseguido + hermano herido a la vista: v29 huye IGUAL que v27 ===")

    def persecucion(parte_on):
        mem = A.Memoria(); mem.hp_max = 100
        HERW = (YO[0] - 1, YO[1])            # el hermano al oeste, herido
        ag = [{"slot": par, "team": mundo.team, "pos": list(HERW),
               "hp_band": "critical"},
              {"slot": 15, "team": "D", "pos": list(CAZ), "hp_band": "healthy"}]
        ch = ([chat_parte(par, 298, texto_parte(par, 298, HERW, 25.0))]
              if parte_on else [])
        o = obs(300, YO, hp=30, agentes=ag, chat=ch,
                pack=[{"id": "first_aid", "n": 1}, None])
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 14.0}]
        mem.observa(o, mundo, 300)
        accion, rad = D.decide(o, mundo, mem, 300)
        return accion, rad

    v29(); a9, r9 = persecucion(True)
    v27(); a7, r7 = persecucion(False)
    _elegidos.extend([r9.get("elegido"), r7.get("elegido")])
    check(f"bajo caza, v29 elige `{r9.get('elegido')}` == v27 "
          f"`{r7.get('elegido')}` (el cuidado no compra riesgo)",
          r9.get("elegido") == r7.get("elegido"),
          "PARAR si difiere (trato del 46)")

    # ════ P4 EL SILENCIO DEL SANO ════════════════════════════════════════
    print("\n=== P4. hermano >= 60: decisiones identicas a v28-candado ===")
    for golpes, hp0, ph in ((1, 100, 100.0), (1, 100, 75.0), (1, 100, 60.0),
                            (3, 100, 80.0)):
        v29(); a9, r9, F9 = escena39(mundo, YO, HER, par, golpes, hp0,
                                     parte_hp=ph)
        v28c(); a8, r8, _ = escena39(mundo, YO, HER, par, golpes, hp0,
                                     parte_hp=ph)
        _elegidos.extend([r9.get("elegido"), r8.get("elegido")])
        check(f"h{ph:g} (g{golpes}): elegido v29 `{r9.get('elegido')}` == "
              f"v28-candado `{r8.get('elegido')}` y las filas callan",
              (r9.get("elegido") == r8.get("elegido")
               and json.dumps(a9, sort_keys=True) == json.dumps(a8, sort_keys=True)
               and (F9.get("S-VINCULO") or 0) == 0
               and (F9.get("S-HERIDO") or 0) == 0), "")

    # ════ P5 EL SOLO INTACTO ═════════════════════════════════════════════
    print("\n=== P5. sin hermano / texto ajeno: v29 BIT-identica a v27 ===")
    BOT = (YO[0] + 3, YO[1])

    def esc_caza():
        o = obs(300, YO, hp=25,
                agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                          "hp_band": "healthy"}],
                items=[{"id": "first_aid", "n": 1, "pos": list(BOT)}])
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
        return o

    def esc_paseo():
        return obs(300, YO, hp=100)

    def esc_ajeno():
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "hurt"}]
        ch = [chat_parte(par, 298, t) for t in
              (f"P{par} 10,10 healthy", "hola que tal",
               "E1 P99 t300 10,10 h50 v0 b0 a0")]
        return obs(300, YO, hp=25, agentes=ag, chat=ch,
                   items=[{"id": "first_aid", "n": 1, "pos": list(BOT)}])

    for nombre, esc in (("caza+botiquin", esc_caza), ("paseo", esc_paseo),
                        ("gemelo con texto ajeno", esc_ajeno)):
        def corre1():
            mem = A.Memoria(); mem.hp_max = 100
            o = esc()
            mem.observa(o, mundo, 300)
            accion, rad = D.decide(o, mundo, mem, 300)
            return accion, rad
        v29(); a9, r9 = corre1()
        v27(); a7, r7 = corre1()
        _elegidos.extend([r9.get("elegido"), r7.get("elegido")])
        check(f"'{nombre}': v29 == v27 byte a byte",
              dump(a9, r9) == dump(a7, r7), f"elegido `{r9.get('elegido')}`")

    # ════ P6 HONOR GENERAL ═══════════════════════════════════════════════
    print("\n=== P6. margenes contra EXTRANOS ===")
    # sin hermano en juego: byte-identico (P5 lo cubre); aqui la escena MIXTA
    # (extrano agresor + hermano critico con parte): deltas DECLARADOS.
    def mixta(parte_on):
        mem = A.Memoria(); mem.hp_max = 100
        HERW = (YO[0] - 1, YO[1])
        CAZ1 = (YO[0] + 1, YO[1])          # adyacente: el atacar existe (espada)
        ag = [{"slot": par, "team": mundo.team, "pos": list(HERW),
               "hp_band": "critical"},
              {"slot": 15, "team": "D", "pos": list(CAZ1), "hp_band": "healthy"}]
        ch = ([chat_parte(par, 298, texto_parte(par, 298, HERW, 25.0))]
              if parte_on else [])
        o = obs(300, YO, hp=70, hand={"id": "sword", "n": 1}, agentes=ag,
                chat=ch)
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 14.0}]
        mem.observa(o, mundo, 300)
        accion, rad = D.decide(o, mundo, mem, 300)
        return accion, rad

    v29(); _, r9 = mixta(True)
    v27(); _, r7 = mixta(False)
    m9, e9, c9 = margen_atacar(r9)
    m7, e7, c7 = margen_atacar(r7)
    at9 = sorted(k for k in c9 if k.startswith("atacar"))
    at7 = sorted(k for k in c7 if k.startswith("atacar"))
    check("mixta: solo candidatos de atacar al EXTRANO, y los mismos",
          at9 == at7 and bool(at9), f"{at9}")
    check("mixta: hay margen medible en ambos brazos",
          m9 is not None and m7 is not None, f"m27={m7} m29={m9}")
    if m9 is not None and m7 is not None:
        print(f"    margen de atacar al extrano: v27 {m7:+.5f} -> v29 "
              f"{m9:+.5f}  (delta {m9 - m7:+.5f}, DECLARADO: residuo no"
              " lineal de d + nivel de S-HERIDO)")
        check("mixta: el extrano no se vuelve mas atacable de forma material "
              f"(delta {m9 - m7:+.5f} > -0.05)", m9 - m7 > -0.05, "")
    check(f"mixta: elegido v29 `{r9.get('elegido')}` no es atacar",
          not (r9.get("elegido") or "").startswith("atacar"), "")

    # ════ determinismo 3/3 ═══════════════════════════════════════════════
    print("\n=== determinismo 3/3 (P1 h10 + P2 h8, las escenas cargadas) ===")
    v29()
    firmas = set()
    for _ in range(3):
        a, r, _ = escena39(mundo, YO, HER, par, 1, 100, parte_hp=10.0)
        b, s, _ = lealtad54(mundo, YO, HER, par, 8.0)
        firmas.add(dump(a, r) + dump(b, s))
    check("3/3 byte-identicas", len(firmas) == 1, "")

    inic = [e for e in _elegidos if (e or "").startswith("atacar")]
    check(f"0 iniciaciones en todo el banco ({len(_elegidos)} decisiones)",
          not inic, str(inic))

    # estado sellado restaurado
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = P_SELL, V_SELL, H_SELL
    check("al salir, el estado sellado queda restaurado",
          (A.PARTE_ON, A.VINCULO_M, A.HERIDO_M) == (P_SELL, V_SELL, H_SELL), "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — el peso del hermano esta puesto: tabu (P1),"
          " cuidado (P2), miedo intacto (P3), silencio del sano (P4),"
          " el solo intacto (P5), honor (P6).")


if __name__ == "__main__":
    main()
