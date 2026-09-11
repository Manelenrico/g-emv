"""Banco de EL NOMBRE DEL AGRESOR — PROMPT_68. v36 = v35 + parte v2 + identidad.

"Cuando alguien nos dice que le hacen dano, preguntamos QUIEN." El parte v2
lleva el ASIENTO del agresor —que la hermana conoce con certeza total: se lo
dice su propio `damage_taken.source`— y la certificacion pasa de la POSICION
(caducable: el 67 midio partes de 28-38 tics con el mundo ya movido) a la
IDENTIDAD. El nombre IDENTIFICA; no persigue: sin verlo, no hay candidato.

  P1 LAS SEIS (sellado): las 6 fotos sin defensa del 66 — donde el agresor
     era visible y en alcance, v36 tiene candidato; donde no lo veia o estaba
     a 2 con espada, sigue sin candidato (no se inventa nada).
  P2 NO PERSIGUE (sellado): nombre certificado pero fuera de vista o de
     alcance -> 0 candidatos, identica a v35.
  P3 C1-C5 del 63 + honor en dos numeros + fuego amigo del 65 intactos.
  P4 SILENCIOS: sin hermana -> v27; en calma -> v32.
  P5 (fuera): bancos 13-67 en verde; determinismo 3/3 aqui.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_68
"""
from __future__ import annotations

import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma import parte as PARTE
from alma.smoke_alma import player_config, obs
from alma.verifica_54 import chat_parte, dump

_fallos = []
_honores = []
DEF = (A.MANADA_ON, A.IDENTIDAD_ON, A.FUEGO_AMIGO_ON)


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v27():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = False, 0.0, 0.0
    A.HERIDO_V30, A.PROVISION_ON, A.COMPANIA_ON = False, False, False
    A.MANADA_ON, A.ALCANCE_ON, A.FUEGO_AMIGO_ON = False, False, False
    A.IDENTIDAD_ON = False


def v32():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, 1.0, 1.8
    A.HERIDO_V30, A.PROVISION_ON, A.PROVISION_B_MIN = True, True, 1
    A.COMPANIA_ON, A.MANADA_ON, A.ALCANCE_ON = False, False, False
    A.FUEGO_AMIGO_ON, A.IDENTIDAD_ON = False, False


def v35():
    v32()
    A.MANADA_ON, A.ALCANCE_ON, A.FUEGO_AMIGO_ON = True, True, True
    A.IDENTIDAD_ON = False


def v36():
    v35(); A.IDENTIDAD_ON = True


def texto2(par, t, pos, hp, bot=0, agr=0, agr_slot=None, agr_pos=None):
    """Parte v2: `... a1 s<asiento>[ ax,ay]` (v1 si agr_slot es None)."""
    s = f"E1 P{par} t{t} {pos[0]},{pos[1]} h{hp:g} v0 b{bot} a{agr}"
    if agr and agr_slot is not None:
        s += f" s{agr_slot}"
    if agr and agr_pos:
        s += f" {agr_pos[0]},{agr_pos[1]}"
    return s


def dec(mundo, o, t=300):
    mem = A.Memoria(); mem.hp_max = 100
    mem.observa(o, mundo, t)
    a, r = D.decide(o, mundo, mem, t)
    _honores.append((r.get("elegido"), r.get("honor")))
    cands = [k for k in (r.get("candidatos") or {}) if k.startswith("atacar")]
    return a, r, cands


def main():
    check("v36 sellada por defecto (MANADA + IDENTIDAD + FUEGO_AMIGO)",
          DEF == (True, True, True), f"{DEF}")
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    C = mundo.arena_size // 2
    YO, T = (C, C), 300
    print(f"  yo {YO} · hermana slot {par} · tick {T}\n")

    # ── A · el formato v2 ────────────────────────────────────────────────
    print("=== A. el parte v2: formato, limpieza y compatibilidad ===")
    t2 = texto2(par, 298, (C + 1, C), 25, agr=1, agr_slot=12,
                agr_pos=(C + 2, C))
    t1 = texto2(par, 298, (C + 1, C), 25, agr=1, agr_pos=(C + 2, C))
    p2, p1 = PARTE.parsea(t2), PARTE.parsea(t1)
    check(f"v2 limpio y <=120 ({len(t2)} chars)", PARTE.ascii_limpio(t2), t2)
    check("v2 parsea con asiento", p2 and p2["agresor_slot"] == 12, str(p2))
    check("v1 sigue parseando (compatibilidad), sin asiento",
          p1 and p1["agresor_slot"] is None and p1["agresor_pos"] is not None, "")
    check("basura con marca valida se rechaza",
          PARTE.parsea("E1 P1 t1 1,1 h1 v0 b0 a1 s12 x") is None, "")
    check("cadencia 48 >= 24 (jamas rate_limited)", PARTE.CADA >= 24, "")

    # ── P1 · LAS SEIS del 66 ─────────────────────────────────────────────
    print("\n=== P1. las seis fotos sin defensa del 66 (geometrias del 67) ===")
    # Del acta 67: (1) no veia al cazador (arco, parte viejo); (2,3,4) lo veia
    # a 1 pero la certificacion por POSICION no encontraba objetivo distinto de
    # la hermana; (5,6) el cazador estaba de verdad a 2, con espada.
    SEIS = [
        ("1 · no lo veia (arco)", dict(ve=False, dist=5, arma="bow")),
        ("2 · a 1, lo veia (espada)", dict(ve=True, dist=1, arma="sword")),
        ("3 · a 1, lo veia (espada)", dict(ve=True, dist=1, arma="sword")),
        ("4 · a 1, lo veia (espada)", dict(ve=True, dist=1, arma="sword")),
        ("5 · a 2 real, espada", dict(ve=True, dist=2, arma="sword")),
        ("6 · a 2 real, espada", dict(ve=True, dist=2, arma="sword")),
    ]

    def esc_seis(ve, dist, arma, v2=True):
        HER = (C + 1, C)
        CAZ = (C + dist, C)                     # DONDE ESTA AHORA (alineado E)
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "critical"}]
        if ve:
            ag.append({"slot": 12, "team": "D", "pos": list(CAZ),
                       "hp_band": "healthy"})
        # EL FALLO QUE EL 67 MIDIO, reproducido: el parte lleva la posicion
        # VIEJA del cazador (el mundo se movio: partes de 28-38 tics). La
        # certificacion por POSICION no encuentra a nadie ahi; la de IDENTIDAD
        # solo necesita el asiento y verlo, este donde este.
        VIEJA = (C + 5, C + 3)
        txt = texto2(par, T - 30, HER, 20, agr=1,
                     agr_slot=12 if v2 else None, agr_pos=VIEJA)
        o = obs(T, YO, hp=90, hand={"id": arma, "n": 1},
                pack=[None, None], agentes=ag, chat=[chat_parte(par, T - 30, txt)])
        return o

    cambian = 0
    for lbl, kw in SEIS:
        v35(); _, r5, c5 = dec(mundo, esc_seis(**kw, v2=False))
        v36(); _, r6, c6 = dec(mundo, esc_seis(**kw, v2=True))
        gano = bool(c6) and not c5
        cambian += 1 if gano else 0
        print(f"    {lbl}: v35 cand {c5} · v36 cand {c6}"
              f" {'** CAMBIA **' if gano else ''}")
        if kw["ve"] and kw["dist"] <= (1 if kw["arma"] == "sword" else 8):
            check(f"{lbl}: v36 TIENE candidato (lo ve y lo alcanza)", bool(c6), "")
        else:
            check(f"{lbl}: v36 sigue SIN candidato (no lo ve o no lo alcanza)",
                  not c6, "no se inventa nada")
    print(f"\n    CAMBIAN {cambian} de 6")
    check("las tres del 'lo veia a 1' cambian", cambian == 3, f"cambian {cambian}")

    # ── P2 · NO PERSIGUE ─────────────────────────────────────────────────
    print("\n=== P2. no persigue: nombre certificado pero sin verlo / sin alcance ===")
    for lbl, kw in (("fuera de VISTA", dict(ve=False, dist=1, arma="sword")),
                    ("visible pero LEJOS (6, espada)",
                     dict(ve=True, dist=6, arma="sword"))):
        v35(); a5, r5, c5 = dec(mundo, esc_seis(**kw, v2=False))
        v36(); a6, r6, c6 = dec(mundo, esc_seis(**kw, v2=True))
        check(f"{lbl}: 0 candidatos en v36", not c6, str(c6))
        check(f"{lbl}: y la decision es la de v35 (no va a buscarlo)",
              r6.get("elegido") == r5.get("elegido"),
              f"v35 `{r5.get('elegido')}` · v36 `{r6.get('elegido')}`")

    # ── P3 · candados y honor ────────────────────────────────────────────
    print("\n=== P3. candados del 63 + honor + fuego amigo del 65 ===")
    # C1: el parte que nombra a la PROPIA hermana no la convierte en objetivo
    def esc_c1():
        HER = (C + 1, C)
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "critical"}]
        txt = texto2(par, T - 5, HER, 20, agr=1, agr_slot=par, agr_pos=HER)
        return obs(T, YO, hp=90, hand={"id": "sword", "n": 1},
                   pack=[None, None], agentes=ag,
                   chat=[chat_parte(par, T - 5, txt)])
    v36(); _, rc1, cc1 = dec(mundo, esc_c1())
    check("C1: el parte que nombra a la hermana -> 0 candidatos", not cc1, str(cc1))
    # C2: a=0 -> 0 candidatos y byte-identica a v35
    def esc_c2():
        HER = (C + 1, C)
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "healthy"},
              {"slot": 12, "team": "D", "pos": [C + 2, C], "hp_band": "healthy"}]
        txt = texto2(par, T - 5, HER, 100, bot=1, agr=0)
        return obs(T, YO, hp=90, hand={"id": "sword", "n": 1},
                   pack=[None, None], agentes=ag,
                   chat=[chat_parte(par, T - 5, txt)])
    v36(); a2, r2, c2 = dec(mundo, esc_c2())
    v35(); a2b, r2b, _ = dec(mundo, esc_c2())
    check("C2: sin a=1 -> 0 candidatos y byte-identica a v35",
          not c2 and dump(a2, r2) == dump(a2b, r2b), f"`{r2.get('elegido')}`")
    # C4: caducidad — parte v2 viejo (>96 tics)
    def esc_c4():
        HER = (C + 1, C)
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "critical"},
              {"slot": 12, "team": "D", "pos": [C + 1, C - 1],
               "hp_band": "healthy"}]
        txt = texto2(par, T - 150, HER, 20, agr=1, agr_slot=12)
        return obs(T, YO, hp=90, hand={"id": "sword", "n": 1},
                   pack=[None, None], agentes=ag,
                   chat=[chat_parte(par, T - 150, txt)])
    v36(); _, r4, c4 = dec(mundo, esc_c4())
    check("C4: parte v2 caducado (>96 tics) -> 0 candidatos", not c4, str(c4))
    # fuego amigo del 65 intacto: con la hermana en la linea, no dispara
    def esc_ff():
        HER = (C + 1, C)
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "healthy"},
              {"slot": 12, "team": "D", "pos": [C + 2, C], "hp_band": "healthy"}]
        txt = texto2(par, T - 5, HER, 94, agr=1, agr_slot=12)
        o = obs(T, YO, hp=100, hand={"id": "spear", "n": 1},
                pack=[None, None], agentes=ag,
                chat=[chat_parte(par, T - 5, txt)])
        o["you"]["damage_taken"] = [{"source": "P12", "amount": 11.0}]
        return o
    v36(); a7, r7, c7 = dec(mundo, esc_ff())
    check("fuego amigo del 65 intacto: con ella en la linea NO dispara",
          bool(c7) and not (r7.get("elegido") or "").startswith("atacar"),
          f"cand {c7} · elige `{r7.get('elegido')}`")

    # ── P4 · silencios ───────────────────────────────────────────────────
    print("\n=== P4. silencios ===")
    def esc_sola():
        return obs(T, YO, hp=90, hand={"id": "sword", "n": 1}, pack=[None, None],
                   agentes=[{"slot": 12, "team": "D", "pos": [C + 2, C],
                             "hp_band": "healthy"}])
    v36(); a8, r8, _ = dec(mundo, esc_sola())
    v27(); a8b, r8b, _ = dec(mundo, esc_sola())
    check("sin hermana: v36 == v27 byte a byte", dump(a8, r8) == dump(a8b, r8b),
          f"`{r8.get('elegido')}`")
    v36(); a9, r9, _ = dec(mundo, esc_c2())
    v32(); a9b, r9b, _ = dec(mundo, esc_c2())
    check("hermana en calma: v36 == v32 byte a byte",
          dump(a9, r9) == dump(a9b, r9b), f"`{r9.get('elegido')}`")

    # honor en dos numeros
    inic = [e for e, h in _honores if (e or "").startswith("atacar")
            and not (h or {}).get("era_agresor")
            and not (h or {}).get("defensa_pareja")]
    check(f"honor (a): 0 iniciaciones-estrictas [{len(_honores)} decisiones]",
          not inic, str(inic))
    check("0 ataques contra la hermana",
          not [e for e, h in _honores if (h or {}).get("es_la_pareja")], "")

    # ── determinismo ─────────────────────────────────────────────────────
    print("\n=== determinismo 3/3 ===")
    v36()
    firmas = set()
    for _ in range(3):
        a, r, _ = dec(mundo, esc_seis(True, 1, "sword"))
        firmas.add(dump(a, r))
    check("3/3 byte-identicas", len(firmas) == 1, "")

    A.MANADA_ON, A.IDENTIDAD_ON, A.FUEGO_AMIGO_ON = DEF
    check("al salir, el estado sellado queda restaurado",
          (A.MANADA_ON, A.IDENTIDAD_ON, A.FUEGO_AMIGO_ON) == DEF, "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — el nombre identifica y no persigue: 3 de 6 fotos"
          " recuperan el gesto (P1), sin verlo no hay candidato (P2),"
          " candados y honor intactos (P3/P4).")


if __name__ == "__main__":
    main()
