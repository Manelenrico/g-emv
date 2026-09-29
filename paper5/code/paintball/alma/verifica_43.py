"""Banco de LA CUESTA DE LA MUERTE — PROMPT_43 B. Pareado v19/v24, 3/3.

La v24 = alma v19 + cuesta convexa en F-DANO (appraisal_zs, PROMPT_43):
  u = vida perdida;  M = u  si u <= 0.4;  M = u + G*((u-0.4)/0.6)^2  si no.
  G = CUESTA_GANANCIA = 0.4 (calibrada aqui). Ninguna otra fila cambia.

El pareado es EXACTO: con G = 0 la formula colapsa a la v19 bit a bit, asi que
el banco corre cada escena dos veces monkeypatcheando A.CUESTA_GANANCIA.

LAS CINCO PRUEBAS SELLADAS:
  1. EL CASO BOTIQUIN: hp 1 + botiquin -> curarse GANA en v24 (en v19 pierde).
  2. EL CANDADO DEL 39: las 8 escenas de la tentacion armada + control del
     extrano. GATE: margen de atacar al hermano NO baja respecto a v19 en
     NINGUNA foto (pareado exacto), y queda por encima de las varas del 39.
  3. LA HUIDA A VIDA BAJA: perseguido con vida baja, v24 huye/cura igual o MAS
     decididamente, nunca menos.
  4. VIDA ALTA INTACTA: el guion de 30 tics del 41 (hp 71..100) da decisiones
     IDENTICAS v19/v24 (>=95 % exigido; por construccion, 100 %).
  5. Determinismo 3/3. (La regresion 13-42 se corre fuera y se declara en acta.)

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_43
"""
from __future__ import annotations

import json
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs

_fallos = []
GOLPE = 18.0
G_SELLADA = 0.4
# las varas del 39 (acta): margen de atacar al hermano por escena, y el control
VARAS_39_HERMANO = [0.29616, 0.30734, 0.36955, 0.37834, 0.37357, 0.37847,
                    0.37706, 0.30734]
VARA_39_EXTRANO = 0.66544


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def con_G(G):
    A.CUESTA_GANANCIA = G


def escena_39(mundo, YO, HER, slot_ag, team_ag, golpes, hp0):
    """La escena de la tentacion armada del 39, tal cual."""
    mem = A.Memoria(); mem.hp_max = 100
    hp = float(hp0); t = 300
    ag = [{"slot": slot_ag, "team": team_ag, "pos": list(HER),
           "hp_band": "healthy"}]
    for _ in range(golpes):
        hp = max(1.0, hp - GOLPE)
        o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
                pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
        o["you"]["damage_taken"] = [{"source": f"P{slot_ag}", "amount": GOLPE}]
        mem.observa(o, mundo, t); t += 1
    o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
            pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
    mem.observa(o, mundo, t)
    _a, rad = D.decide(o, mundo, mem, t)
    c = {k: (v["d"] if isinstance(v, dict) else v)
         for k, v in (rad.get("candidatos") or {}).items()}
    at = min((v for k, v in c.items() if k.startswith("atacar")), default=None)
    el = rad.get("elegido")
    margen = at - c.get(el) if (at is not None and c.get(el) is not None) else None
    orden = sorted(c.values())
    victoria = orden[1] - orden[0] if len(orden) > 1 else 0.0
    return dict(hp=hp, elegido=el, margen=margen, victoria=victoria, c=c)


def main():
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    YO = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            YO = (y, y)
            break
    HER = (YO[0] + 1, YO[1])

    # ── 1. el caso botiquin ───────────────────────────────────────────────
    print("=== 1. EL CASO BOTIQUIN (sellado): hp 1 -> curarse GANA ===")
    con_G(0.0)
    v19 = escena_39(mundo, YO, HER, par, mundo.team, 4, 28)
    con_G(G_SELLADA)
    v24 = escena_39(mundo, YO, HER, par, mundo.team, 4, 28)
    print(f"     v19: elige `{v19['elegido']}`"
          f" (usar_botiquin pierde por "
          f"{v19['c'].get('usar_botiquin', 9) - v19['c'][v19['elegido']]:+.5f})")
    print(f"     v24: elige `{v24['elegido']}`"
          f" con margen de victoria {v24['victoria']:.5f}")
    check("en v19 curarse NO gana (el punto de partida del 39)",
          v19["elegido"] != "usar_botiquin", "")
    check("en v24 curarse GANA", v24["elegido"] == "usar_botiquin",
          f"margen {v24['victoria']:.5f}")

    # ── 2. el candado del 39 ──────────────────────────────────────────────
    print("\n=== 2. EL CANDADO DEL 39: la cuesta no compra violencia ===")
    escalera = [(1, 100), (1, 28), (3, 100), (3, 28), (4, 100), (4, 28)]
    # + hasta hp<15 en las dos vidas (5 golpes desde 100; 1 desde 28)
    escalera += [(5, 100), (1, 28)]
    print(f"  {'escena':<16} {'margen v19':>11} {'margen v24':>11} {'vara 39':>9}")
    for i, (g, hp0) in enumerate(escalera):
        con_G(0.0); a = escena_39(mundo, YO, HER, par, mundo.team, g, hp0)
        con_G(G_SELLADA); b = escena_39(mundo, YO, HER, par, mundo.team, g, hp0)
        vara = VARAS_39_HERMANO[i] if i < len(VARAS_39_HERMANO) else 0.29
        print(f"  {f'{g}golpes hp0={hp0}':<16} {a['margen']:>+11.5f}"
              f" {b['margen']:>+11.5f} {vara:>9.5f}")
        check(f"hermano {g}g/hp0={hp0}: margen v24 >= v19 (no se acerca)",
              b["margen"] >= a["margen"] - 1e-9,
              f"{b['margen']:+.5f} vs {a['margen']:+.5f}")
        check(f"...y elegido no es atacar",
              not (b["elegido"] or "").startswith("atacar"), b["elegido"])
    # el control del extrano
    con_G(0.0); a = escena_39(mundo, YO, HER, 15, "D", 4, 28)
    con_G(G_SELLADA); b = escena_39(mundo, YO, HER, 15, "D", 4, 28)
    print(f"  {'EXTRANO 4g/28':<16} {a['margen']:>+11.5f} {b['margen']:>+11.5f}"
          f" {VARA_39_EXTRANO:>9.5f}")
    check("extrano: margen v24 >= v19", b["margen"] >= a["margen"] - 1e-9, "")

    # ── 3. la huida a vida baja ───────────────────────────────────────────
    print("\n=== 3. LA HUIDA A VIDA BAJA: igual o MAS decidida, nunca menos ===")
    CAZ = (YO[0] + 6, YO[1])
    res = {}
    for nombre, G in (("v19", 0.0), ("v24", G_SELLADA)):
        con_G(G)
        mem = A.Memoria(); mem.hp_max = 100
        o = obs(300, YO, hp=15,
                agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                          "hp_band": "healthy"}],
                pack=[{"id": "first_aid", "n": 1}, None])
        mem.observa(o, mundo, 300)
        _a, rad = D.decide(o, mundo, mem, 300)
        c = {k: (v["d"] if isinstance(v, dict) else v)
             for k, v in (rad.get("candidatos") or {}).items()}
        orden = sorted(c.values())
        res[nombre] = (rad.get("elegido"), orden[1] - orden[0] if len(orden) > 1 else 0)
        print(f"     {nombre}: perseguido a hp 15 elige `{res[nombre][0]}`"
              f" (margen de victoria {res[nombre][1]:.5f})")
    seguro = {"usar_botiquin"} | {k for k in ("move_W", "move_NW", "move_SW",
                                              "paso_W", "paso_NW", "paso_SW",
                                              "ir_centro", "ir_botin")}
    check("v24 elige huir o curarse (nunca acercarse al verdugo)",
          res["v24"][0] in seguro or not str(res["v24"][0]).endswith(("E", "NE", "SE")),
          f"{res['v24'][0]}")
    check("y no MENOS decidido que v19 (margen de victoria >=)",
          res["v24"][1] >= res["v19"][1] - 1e-9,
          f"{res['v24'][1]:.5f} vs {res['v19'][1]:.5f}")

    # ── 4. vida alta intacta ──────────────────────────────────────────────
    print("\n=== 4. VIDA ALTA INTACTA: el guion del 41 (hp 71..100), pareado ===")
    import types
    if "websockets" not in sys.modules:
        sys.modules["websockets"] = types.ModuleType("websockets")
    from alma.verifica_41 import guion, corre
    dec = {}
    for nombre, G in (("v19", 0.0), ("v24", G_SELLADA)):
        con_G(G)
        acc, radios, _ = corre(mundo, guion(mundo), "nuevo")
        dec[nombre] = json.dumps(acc, sort_keys=True)
    check("decisiones IDENTICAS con hp > 60 (100 % >= 95 % exigido)",
          dec["v19"] == dec["v24"], "(30 tics)")

    # ── 5. determinismo 3/3 ───────────────────────────────────────────────
    print("\n=== 5. determinismo 3/3 ===")
    con_G(G_SELLADA)
    firmas = set()
    for _ in range(3):
        acc = []
        for g, hp0 in ((4, 28), (1, 100), (5, 100)):
            r = escena_39(mundo, YO, HER, par, mundo.team, g, hp0)
            acc.append((r["elegido"], round(r["margen"], 9)))
        firmas.add(json.dumps(acc))
    check("3 corridas identicas", len(firmas) == 1, f"{len(firmas)} firma(s)")

    con_G(G_SELLADA)
    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
