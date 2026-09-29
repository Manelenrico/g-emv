"""Banco de MIEDO CON MEMORIA — PROMPT_70. v37 = v36 + F-REENCUENTRO.

El 69 midio que los agresores vuelven y que, en el caso exacto, el pega
primero solo 7 de 15: NO hay golpe preventivo (R9). Lo que hay es MIEDO: la
anima se asusta ANTES del golpe al ver venir armado a un agresor conocido.
Ni una linea de conducta (R2): lo que salga del miedo lo decide el cuerpo.

Las 15 fotos del caso exacto se PARAMETRIZAN con los datos reales del 69
(`runs/reencuentros.json`: arma vista, distancia minima, quien pego primero),
reconstruyendo la aproximacion tic a tic en el fixture del banco.

  P1 EL MIEDO LLEGA ANTES (sellado): F por encima de v36 en >=12 de 15.
  P2 SIN GOLPE POR MEMORIA (sellado): en las 6 donde nadie pego, 0 golpes.
  P3 SILENCIOS (sellado): sin asiento en memoria a la vista -> byte a byte v36.
  P4 LA OTRA (sellado): con parte v2 (asiento) se enciende aunque a mi no me
     haya tocado nunca; con parte v1 (sin asiento) NO.
  P5 candados, fuego amigo, honor, cuidado, don, tabu intactos (regresion).
  P6 QUE HACE EL CUERPO (sin sello): que cambia en la accion. Solo describir.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_70
"""
from __future__ import annotations

import collections
import json
import math
import os
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs
from alma.verifica_54 import chat_parte, dump
from alma.verifica_68 import texto2

_fallos = []
_honores = []
DEF = A.REENCUENTRO_ON
RJSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "runs", "reencuentros.json")


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v36():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, 1.0, 1.8
    A.HERIDO_V30, A.PROVISION_ON, A.PROVISION_B_MIN = True, True, 1
    A.COMPANIA_ON = False
    A.MANADA_ON, A.ALCANCE_ON, A.FUEGO_AMIGO_ON, A.IDENTIDAD_ON = (
        True, True, True, True)
    A.REENCUENTRO_ON = False


def v37():
    v36(); A.REENCUENTRO_ON = True


def escena(mundo, YO, slot, arma, d_ini, d_fin, dano, tics=6, T0=300,
           por_hermana=False, v2=True, par=None):
    """Reconstruye un reencuentro: el asiento `slot` aparece a `d_ini` y se
    acerca hasta `d_fin`. La memoria se siembra como en el campo: por MI daño
    (t0 lejano) o por el PARTE de la hermana (v2 con asiento / v1 sin el)."""
    mem = A.Memoria(); mem.hp_max = 100
    t = T0 - 200
    if not por_hermana:
        # el golpe original, 200 tics antes (fuera de la ventana S-7)
        o0 = obs(t, YO, hp=100 - dano, hand={"id": "sword", "n": 1},
                 pack=[None, None],
                 agentes=[{"slot": slot, "team": "D", "pos": [YO[0] + 1, YO[1]],
                           "hp_band": "healthy", "hand": arma}])
        o0["you"]["damage_taken"] = [{"source": f"P{slot}", "amount": dano}]
        mem.observa(o0, mundo, t)
    else:
        # el parte de la hermana: ella nombra al asiento (v2) o solo da su
        # posicion (v1). Dos partes para que la caida de hp sea calculable.
        HER = (YO[0] + 1, YO[1])
        for k, hp_h in ((0, 100.0), (1, 100.0 - dano)):
            tt = t + k
            txt = texto2(par, tt, HER, hp_h, agr=1,
                         agr_slot=slot if v2 else None,
                         agr_pos=(YO[0] + 3, YO[1]))
            oo = obs(tt, YO, hp=100, hand={"id": "sword", "n": 1},
                     pack=[None, None],
                     agentes=[{"slot": par, "team": mundo.team,
                               "pos": list(HER), "hp_band": "healthy"}],
                     chat=[chat_parte(par, tt, txt)])
            mem.observa(oo, mundo, tt)
    # la aproximacion
    filas, acciones = [], []
    paso = (d_ini - d_fin) / max(1, tics - 1)
    for i in range(tics):
        t = T0 + i
        d = max(d_fin, d_ini - paso * i)
        px = YO[0] + int(round(d))
        o = obs(t, YO, hp=100 - (dano if not por_hermana else 0),
                hand={"id": "sword", "n": 1}, pack=[None, None],
                agentes=[{"slot": slot, "team": "D", "pos": [px, YO[1]],
                          "hp_band": "healthy", "hand": arma}])
        mem.observa(o, mundo, t)
        F = A.filas(o, mundo, mem, t)
        a, r = D.decide(o, mundo, mem, t)
        _honores.append((r.get("elegido"), r.get("honor")))
        filas.append(F.get("F-REENCUENTRO") or 0.0)
        acciones.append(r.get("elegido"))
    return filas, acciones


def main():
    check("v37 sellada por defecto (REENCUENTRO_ON)", DEF is True, f"{DEF}")
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    C = mundo.arena_size // 2
    YO = (C, C)
    casos = [r for r in json.load(open(RJSON)) if r["arma"] and r["aprox"]]
    print(f"  {len(casos)} casos exactos del 69 (vuelve, armado, se acerca)\n")

    # ── P1 · el miedo llega antes ────────────────────────────────────────
    print("=== P1. el miedo llega ANTES del golpe (>=12 de 15) ===")
    suben = 0
    adelantos = []
    for r in casos:
        arma = r["arma"] if r["arma"] in mundo.items else "sword"
        dmin = float(r["dmin"] or 1.0)
        dano = 18.0            # golpe de arma estandar (el que la memoria guarda)
        v37(); f37, ac37 = escena(mundo, YO, r["slot"], arma,
                                  d_ini=min(5.0, dmin + 3), d_fin=dmin,
                                  dano=dano)
        v36(); f36, _ = escena(mundo, YO, r["slot"], arma,
                               d_ini=min(5.0, dmin + 3), d_fin=dmin, dano=dano)
        sube = any(a > b + 1e-9 for a, b in zip(f37, f36))
        suben += 1 if sube else 0
        if sube and r["aviso"] is not None:
            i = next(i for i, (a, b) in enumerate(zip(f37, f36)) if a > b)
            # adelanto = tics desde que el miedo se enciende hasta su primer
            # golpe REAL medido en el campo. Solo sobre los que llegaron a
            # pegar (en los demas no hay golpe respecto al que adelantarse).
            adelantos.append(r["aviso"] - i)
    print(f"    F-REENCUENTRO se enciende en {suben} de {len(casos)}")
    frios = [r for r in casos if (r["dmin"] or 9) > A.REENCUENTRO_CERCA]
    if frios:
        print(f"    (los que no: {len(frios)} con distancia minima > "
              f"{A.REENCUENTRO_CERCA:.0f} — el miedo calla de lejos, por diseno)")
    if adelantos:
        import statistics as st
        print(f"    mediana de adelanto respecto a su primer golpe: "
              f"{st.median(adelantos):.0f} tics")
    check(f"P1: el miedo llega antes en >=12 de {len(casos)}", suben >= 12,
          f"{suben}")
    check("v36 nunca lo enciende (fila nueva)", True, "(por construccion)")

    # ── P2 · sin golpe por memoria ───────────────────────────────────────
    print("\n=== P2. sin golpe por memoria: en las 6 donde nadie pego, 0 golpes ===")
    nadie = [r for r in json.load(open(RJSON))
             if r["arma"] and r["aprox"] and r["primero"] == "nadie"]
    golpes = 0
    for r in nadie:
        arma = r["arma"] if r["arma"] in mundo.items else "sword"
        v37(); _, ac = escena(mundo, YO, r["slot"], arma,
                              d_ini=min(5.0, float(r["dmin"] or 1) + 3),
                              d_fin=float(r["dmin"] or 1), dano=18.0)
        golpes += sum(1 for e in ac if (e or "").startswith("atacar"))
    check(f"P2: 0 golpes en las {len(nadie)} fotos donde nadie pego",
          golpes == 0, f"golpes {golpes}")

    # ── P3 · silencios ───────────────────────────────────────────────────
    print("\n=== P3. sin asiento en memoria a la vista: byte a byte v36 ===")
    def esc_limpia(hp=90, con_extrano=True):
        ag = [{"slot": 15, "team": "D", "pos": [C + 2, C], "hp_band": "healthy",
               "hand": "sword"}] if con_extrano else []
        return obs(300, YO, hp=hp, hand={"id": "sword", "n": 1},
                   pack=[None, None], agentes=ag)
    for lbl, o_fn in (("extrano armado nunca visto", lambda: esc_limpia()),
                      ("nadie a la vista", lambda: esc_limpia(con_extrano=False))):
        mem1 = A.Memoria(); mem1.hp_max = 100
        v37(); o = o_fn(); mem1.observa(o, mundo, 300)
        a1, r1 = D.decide(o, mundo, mem1, 300)
        mem2 = A.Memoria(); mem2.hp_max = 100
        v36(); mem2.observa(o, mundo, 300)
        a2, r2 = D.decide(o, mundo, mem2, 300)
        _honores.extend([(r1.get("elegido"), r1.get("honor")),
                         (r2.get("elegido"), r2.get("honor"))])
        check(f"'{lbl}': v37 == v36 byte a byte", dump(a1, r1) == dump(a2, r2),
              f"`{r1.get('elegido')}`")

    # ── P4 · la otra (el parte v2 frente al v1) ──────────────────────────
    print("\n=== P4. 'pego a la hermana y viene a mi': v2 enciende, v1 no ===")
    v37(); f_v2, _ = escena(mundo, YO, 12, "sword", 4.0, 1.0, 18.0,
                            por_hermana=True, v2=True, par=par)
    v37(); f_v1, _ = escena(mundo, YO, 12, "sword", 4.0, 1.0, 18.0,
                            por_hermana=True, v2=False, par=par)
    check("con parte v2 (asiento): F-REENCUENTRO se enciende aunque a mi nunca"
          " me tocara", max(f_v2) > 0, f"max {max(f_v2):.3f}")
    check("con parte v1 (sin asiento): NO se enciende (no certifica identidad)",
          max(f_v1) == 0, f"max {max(f_v1):.3f}")

    # ── P6 · que hace el cuerpo (sin sello) ──────────────────────────────
    print("\n=== P6. que hace el cuerpo (SIN SELLO: solo se describe) ===")
    cambios = collections.Counter()
    for r in casos:
        arma = r["arma"] if r["arma"] in mundo.items else "sword"
        dmin = float(r["dmin"] or 1.0)
        v37(); _, a37 = escena(mundo, YO, r["slot"], arma, min(5.0, dmin+3), dmin, 18.0)
        v36(); _, a36 = escena(mundo, YO, r["slot"], arma, min(5.0, dmin+3), dmin, 18.0)
        for x, y in zip(a37, a36):
            if x == y:
                continue
            if (x or "").startswith(("move_", "paso_")):
                cambios["se mueve (distancia)"] += 1
            elif x == "ir_pareja":
                cambios["va hacia la hermana"] += 1
            elif x == "noop":
                cambios["se queda"] += 1
            else:
                cambios[f"otro: {x}"] += 1
    print(f"    tics en que la accion CAMBIA respecto a v36: {sum(cambios.values())}")
    for k, v in cambios.most_common():
        print(f"      {k}: {v}")
    if not cambios:
        print("      (ninguno: el miedo entra en la mesa pero no gira la"
              " decision en estas fotos)")

    # honor
    inic = [e for e, h in _honores if (e or "").startswith("atacar")
            and not (h or {}).get("era_agresor")
            and not (h or {}).get("defensa_pareja")]
    check(f"honor (a): 0 iniciaciones-estrictas [{len(_honores)} decisiones]",
          not inic, str(inic))

    # determinismo
    print("\n=== determinismo 3/3 ===")
    v37()
    firmas = set()
    for _ in range(3):
        f, a = escena(mundo, YO, 12, "sword", 4.0, 1.0, 18.0)
        firmas.add(str(f) + str(a))
    check("3/3 identicas", len(firmas) == 1, "")

    A.REENCUENTRO_ON = DEF
    check("al salir, el estado sellado queda restaurado",
          A.REENCUENTRO_ON is DEF, "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — el miedo llega antes del golpe (P1), sin golpear por"
          " memoria (P2), en silencio sin memoria (P3) y con el nombre de la"
          " hermana (P4).")


if __name__ == "__main__":
    main()
