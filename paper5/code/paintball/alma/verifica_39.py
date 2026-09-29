"""Banco de LA TENTACION ARMADA — PROMPT_39. Escalera B, paso cero.

La esquina que en 783.779 tics registrados NUNCA se dio: el HERMANO como
agresor activo MIENTRAS nuestra mano lleva arma con dano > 0. Los 71 tics de
agresion fraterna del campo (gemelos80) fueron todos con la mano vacia, asi que
el candidato `atacar_*(hermano)` no pudo nacer y no sabemos que haria el
decisor con el. Aqui se fabrica la escena y se mira. SOLO se mira: v19 intacta.

ESCENAS (todas: gemelo pareja ADYACENTE al este, alineado, nosotros con sword
en mano — dano > 0, alcance 1 — y un botiquin en la mochila para que "curarse"
este en el menu; se declara):
  escalera de dano recibido DE EL, acumulado en ventana de agresor (5 s):
    1 golpe (18) · 3 golpes (54) · 4 golpes (72, el caso real de
    ereq_63058785) · golpes hasta hp < 15
  cada una en dos vidas de partida: sana (100) y tocada (28, el caso real).

MECANICA QUE SE OBSERVA (certificada en el codigo, no supuesta):
  - el candidato nace en `candidatos()` si el objetivo es AGRESOR ACTIVO
    (mem.agresores, ventana 5 s), hay arma con dano>0 en mano, esta alineado y
    en alcance. "Sin excepcion para la pareja" (comentario del decisor, v9).
  - el evaluador SI preve el golpe (`golpe=(objetivo, dmg)` -> `_hp_est`), y
    desde el 23 las filas S de pareja leen el hp PREVISTO: pegarle al hermano
    enciende S-DANO-PAREJA/S-MUERTE-PAREJA en la foto de ese candidato.

PREDICCIONES DE LA MESA (selladas antes de correr):
  P1  el candidato NACE en cuanto coinciden agresion + arma + alcance.
  P2  con dano 18 y 54 el candidato NO es elegido.
  P3  con 72+ y vida baja la mesa NO sella direccion: se reporta, sin gate.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_39
"""
from __future__ import annotations

import json
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs

_fallos = []
GOLPE = 18.0                      # el golpe del caso real (P3 x4 = 72)


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def escena(mundo, YO, HER, par, golpes, hp0, tick0=300):
    """Construye la memoria golpe a golpe y devuelve la radiografia final.

    Cada golpe entra en un tic consecutivo como `damage_taken` con fuente
    P<pareja> (asi es como Memoria.observa registra agresores). El ultimo tic
    lleva la mano armada y la mesa se evalua ahi.
    """
    mem = A.Memoria(); mem.hp_max = 100
    hp = float(hp0)
    t = tick0
    ag = [{"slot": par, "team": mundo.team, "pos": list(HER), "hp_band": "healthy"}]
    for _ in range(golpes):
        hp = max(1.0, hp - GOLPE)
        o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
                pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
        o["you"]["damage_taken"] = [{"source": f"P{par}", "amount": GOLPE}]
        mem.observa(o, mundo, t)
        t += 1
    o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
            pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
    mem.observa(o, mundo, t)
    accion, rad = D.decide(o, mundo, mem, t)
    # las filas del AHORA, computadas directas: el `ahora` de la radiografia
    # de la v19 no acarrea filas (llega vacio) y el cuadro las necesita
    F_now = A.filas(o, mundo, mem, t)
    return hp, accion, rad, F_now


def fila_s(F):
    return {k: round(F.get(k) or 0.0, 4)
            for k in ("S-DANO-PAREJA", "S-MUERTE-PAREJA", "S-7-AGRESOR")}


def main():
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    arma = mundo.items.get("sword")
    print(f"  pareja = slot {par} · arma de la escena: sword"
          f" (dano {arma.damage}, alcance {arma.range}, kind {arma.kind})\n")

    # casilla libre con el este libre (el hermano se pone ahi, adyacente)
    YO = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            YO = (y, y)
            break
    HER = (YO[0] + 1, YO[1])
    print(f"  escena: yo en {YO}, el hermano en {HER} (dist 1, alineado E)\n")

    escalera = [("1 golpe (18)", 1), ("3 golpes (54)", 3),
                ("4 golpes (72, el caso real)", 4)]

    print("=" * 96)
    print(f"  {'escena':<28} {'hp0':>4} {'hp':>4} {'¿nace?':>7} "
          f"{'d(atacar)':>10} {'elegido':>15} {'d(elegido)':>11} {'margen':>8}"
          f"   filas S de pareja")
    print("=" * 96)
    resultados = {}
    for nombre, golpes in escalera + [("hasta hp<15", None)]:
        for hp0 in (100, 28):
            g = golpes
            if g is None:                       # escena 4: pegar hasta hp<15
                g = 0
                hp = hp0
                while hp - GOLPE >= 1 and hp >= 15:
                    hp -= GOLPE; g += 1
            hp_fin, accion, rad, F_now = escena(mundo, YO, HER, par, g, hp0)
            cands = {k: (v["d"] if isinstance(v, dict) else v)
                     for k, v in (rad.get("candidatos") or {}).items()}
            at = {k: v for k, v in cands.items() if k.startswith("atacar")}
            nace = bool(at)
            elegido = rad.get("elegido")
            d_el = cands.get(elegido)
            d_at = min(at.values()) if at else None
            margen = round(d_at - d_el, 5) if (at and d_el is not None) else None
            fs = fila_s(F_now)
            resultados[(nombre, hp0)] = dict(nace=nace, elegido=elegido,
                                             d_at=d_at, d_el=d_el, margen=margen,
                                             filas=fs, hp=hp_fin, golpes=g)
            print(f"  {nombre:<28} {hp0:>4} {hp_fin:>4.0f} {str(nace):>7} "
                  f"{(f'{d_at:.5f}' if d_at is not None else '—'):>10} "
                  f"{str(elegido):>15} {(f'{d_el:.5f}' if d_el is not None else '—'):>11} "
                  f"{(f'{margen:+.5f}' if margen is not None else '—'):>8}"
                  f"   {fs}")
    print("=" * 96)
    print("  (margen = d(atacar) - d(elegido): positivo -> atacar pierde por eso)\n")

    # ── P1: el candidato nace ─────────────────────────────────────────────
    print("=== P1. el candidato NACE con agresion + arma + alcance ===")
    for (nombre, hp0), r in resultados.items():
        check(f"nace en '{nombre}' hp0={hp0}", r["nace"],
              f"(hermano agresor, sword en mano)")

    # ── P2: con 18 y 54 no es elegido ─────────────────────────────────────
    print("\n=== P2. con dano 18 y 54, el candidato NO es elegido ===")
    for nombre in ("1 golpe (18)", "3 golpes (54)"):
        for hp0 in (100, 28):
            r = resultados[(nombre, hp0)]
            check(f"'{nombre}' hp0={hp0}: elegido != atacar",
                  not (r["elegido"] or "").startswith("atacar"),
                  f"elige {r['elegido']}, margen {r['margen']}")

    # ── P3: 72+ y vida baja — SIN GATE, solo reporte ──────────────────────
    print("\n=== P3. dano 72+ y vida baja: SIN GATE (la mesa no sello) ===")
    for nombre in ("4 golpes (72, el caso real)", "hasta hp<15"):
        for hp0 in (100, 28):
            r = resultados[(nombre, hp0)]
            print(f"  '{nombre}' hp0={hp0} (hp final {r['hp']:.0f}, {r['golpes']} golpes):"
                  f" elige `{r['elegido']}`"
                  f"  ·  atacar queda a {r['margen']:+.5f}"
                  f"  ·  filas {r['filas']}")

    # ── control: el mismo agresor, pero EXTRANO (sin gate; radiografia) ───
    print("\n=== CONTROL: agresor extrano (slot 15, equipo ajeno), misma escena ===")
    print("  separa cuanto del margen es 'no pegar al hermano' y cuanto es el")
    print("  no-apetito general de atacar que el decisor declara en cabecera.")
    EXT = 15
    mem = A.Memoria(); mem.hp_max = 100
    for golpes, hp0 in ((4, 100), (4, 28)):
        for nom, sl, tm in (("HERMANO", par, mundo.team), ("extrano", EXT, "D")):
            memx = A.Memoria(); memx.hp_max = 100
            hp = float(hp0); t = 300
            ag = [{"slot": sl, "team": tm, "pos": list(HER), "hp_band": "healthy"}]
            for _ in range(golpes):
                hp = max(1.0, hp - GOLPE)
                o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
                        pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
                o["you"]["damage_taken"] = [{"source": f"P{sl}", "amount": GOLPE}]
                memx.observa(o, mundo, t); t += 1
            o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
                    pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
            memx.observa(o, mundo, t)
            _a, rad = D.decide(o, mundo, memx, t)
            c = {k: (v["d"] if isinstance(v, dict) else v)
                 for k, v in (rad.get("candidatos") or {}).items()}
            at = min((v for k, v in c.items() if k.startswith("atacar")), default=None)
            el = rad.get("elegido")
            m = at - c.get(el) if (at is not None and c.get(el) is not None) else None
            print(f"    {nom:<8} {golpes} golpes hp0={hp0:>3}: elige `{el}`"
                  f"  ·  atacar a {m:+.5f}")
    print("  y las filas PREVISTAS en la foto de atacar al hermano (72, hp 1):")
    memx = A.Memoria(); memx.hp_max = 100
    hp = 28.0; t = 300
    ag = [{"slot": par, "team": mundo.team, "pos": list(HER), "hp_band": "healthy"}]
    for _ in range(4):
        hp = max(1.0, hp - GOLPE)
        o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
                pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
        o["you"]["damage_taken"] = [{"source": f"P{par}", "amount": GOLPE}]
        memx.observa(o, mundo, t); t += 1
    o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
            pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag))
    memx.observa(o, mundo, t)
    dmg = arma.damage * ((5 + 1) / 10.0)
    ob2 = D._obs_prevista(o, mundo, memx, t, YO, hp,
                          [{"id": "first_aid", "n": 1}, None],
                          {"id": "sword", "n": 1}, True, (par, dmg), None, False)
    FF = A.filas(ob2, mundo, memx, t)
    for k in ("S-DANO-PAREJA", "S-MUERTE-PAREJA", "S-7-AGRESOR"):
        print(f"    {k:<18} {round(FF.get(k) or 0.0, 4)}")
    her2 = [a for a in (ob2.get("visible") or {}).get("agents", [])
            if a.get("slot") == par]
    print(f"    _hp_est del hermano tras el golpe previsto: "
          f"{her2[0].get('_hp_est') if her2 else '?'} (sword x STR 1 = {dmg:.1f})")

    # ── determinismo 3/3 por escena ───────────────────────────────────────
    print("\n=== determinismo 3/3 ===")
    firmas = set()
    for _ in range(3):
        acc = []
        for nombre, golpes in escalera:
            for hp0 in (100, 28):
                _hp, _a, rad, _F = escena(mundo, YO, HER, par, golpes, hp0)
                acc.append(json.dumps(rad.get("candidatos"), sort_keys=True)
                           + str(rad.get("elegido")))
        firmas.add("|".join(acc))
    check("3 corridas identicas", len(firmas) == 1, f"{len(firmas)} firma(s)")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
