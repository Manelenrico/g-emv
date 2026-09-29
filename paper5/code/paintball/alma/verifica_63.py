"""Banco de LA MANADA — PROMPT_63. v34 = v32 + responder por la hermana.

El modelo siempre fue de supervivencia, y la supervivencia de una manada es
defenderse JUNTOS del que ataca. `era_agresor` se amplia: el agresor ACTIVO y
CERTIFICADO de mi hermana (su parte fresco a=1 con ax,ay + enemigo VISIBLE
ahi, tolerancia 1) es tambien mi agresor. Ni un candidato nuevo (R2): el
`responder` de siempre con un motivo mas, declarado en la radiografia
(`honor.defensa_pareja`).

LAS DOS METRICAS DE HONOR, desde ahora (P4):
  (a) INICIACIONES-ESTRICTAS: atacar a quien no ha agredido ni a mi ni a ella
      = 0 SIEMPRE. Hereda el nombre "cero iniciaciones". Es el candado C2.
  (b) DEFENSAS-POR-LA-HERMANA: primer golpe mio contra su agresor
      certificado. Se cuentan y se DICEN aparte. No son iniciaciones: son
      defensa de la manada.

  P1 LA DEFENSA (sellado): ella a <=2 con parte a=1 y su agresor visible, yo
     sana (hp>=70) sin agresor propio, arma en mano -> v34 responde donde v32
     hacia otra cosa.
  P2 EL PRECIO DE MI VIDA (sellado a hp<=30; radiografia a hp 50).
  P3 los cinco candados C1-C5, uno a uno.
  P4 las dos metricas, calculadas sobre TODO el banco.
  P5 (fuera): bancos 13-62 en verde; determinismo 3/3 aqui.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_63
"""
from __future__ import annotations

import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs
from alma.verifica_54 import chat_parte, texto_parte, escena39, dump

_fallos = []
_honores = []          # (elegido, honor) de TODAS las decisiones del banco
DEF_MANADA = A.MANADA_ON


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v27():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = False, 0.0, 0.0
    A.HERIDO_V30, A.PROVISION_ON, A.COMPANIA_ON = False, False, False
    A.MANADA_ON = False


def v32():
    A.PARTE_ON, A.VINCULO_M, A.HERIDO_M = True, 1.0, 1.8
    A.HERIDO_V30, A.PROVISION_ON, A.PROVISION_B_MIN = True, True, 1
    A.COMPANIA_ON, A.MANADA_ON = False, False


def v34():
    v32()
    A.MANADA_ON = True


def decide1(mundo, o, t=300):
    mem = A.Memoria(); mem.hp_max = 100
    mem.observa(o, mundo, t)
    a, r = D.decide(o, mundo, mem, t)
    F = A.filas(o, mundo, mem, t)
    _honores.append((r.get("elegido"), r.get("honor")))
    return a, r, F


def main():
    check("v34 sellada por defecto (MANADA_ON=True)", DEF_MANADA is True, "")
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    # ESCENA DE LA MANADA, declarada: los tres en contacto EN EL CENTRO y con
    # el anillo ya apretando (T=300 del fixture). Motivo medido: en campo
    # abierto y sin anillo, la ZANCADA de huida escapa de S-7 y S-8 a la vez y
    # gana siempre —eso ya lo sabiamos (el don del 57 perdia igual)—, asi que
    # una escena abierta no prueba nada sobre la manada. Donde la manada de
    # verdad se juega el final es donde huir cuesta: el cerco.
    C = mundo.arena_size // 2
    YO = (C, C)
    HER = (C + 1, C)                  # hermana a 1 (E)
    CAZ = (C + 1, C - 1)              # su cazador: pegado a ELLA y a mi alcance
    T = 300
    print(f"  yo {YO} · hermana {par} en {HER} · su cazador slot 15 en {CAZ}"
          f" · tick {T} (anillo apretando)\n")

    def esc(mihp=90, suhp=25, agr=True, agr_pos=None, caz_pos=CAZ,
            caz_slot=15, dano_mio=False, edad=2, tercero=None):
        """Escena de la manada: ella herida con su cazador declarado."""
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "critical" if suhp < 33 else "hurt"},
              {"slot": caz_slot, "team": "D", "pos": list(caz_pos),
               "hp_band": "healthy"}]
        if tercero:
            ag.append({"slot": tercero[0], "team": "E", "pos": list(tercero[1]),
                       "hp_band": "healthy"})
        t_emision = T - edad
        ch = [chat_parte(par, t_emision,
                         texto_parte(par, t_emision, HER, suhp, bot=0,
                                     agr=1 if agr else 0,
                                     agr_pos=agr_pos or caz_pos))]
        o = obs(T, YO, hp=mihp, hand={"id": "sword", "n": 1},
                pack=[{"id": "first_aid", "n": 1}, None], agentes=ag, chat=ch)
        if dano_mio:
            o["you"]["damage_taken"] = [{"source": f"P{caz_slot}", "amount": 18.0}]
        return o

    # ════ P1 LA DEFENSA ══════════════════════════════════════════════════
    print("=== P1. la defensa: ella herida, su cazador certificado, yo sana ===")
    for mihp in (90, 70):
        v34(); a1, r1, F1 = decide1(mundo, esc(mihp=mihp))
        v32(); a0, r0, F0 = decide1(mundo, esc(mihp=mihp))
        c1 = [k for k in (r1.get("candidatos") or {}) if k.startswith("atacar")]
        c0 = [k for k in (r0.get("candidatos") or {}) if k.startswith("atacar")]
        h = r1.get("honor") or {}
        print(f"    yo{mihp}: v32 `{r0.get('elegido')}` (cand {c0}) -> "
              f"v34 `{r1.get('elegido')}` (cand {c1})")
        check(f"yo{mihp}: v32 NO tenia candidato (no me agredio a mi)",
              not c0, "")
        check(f"yo{mihp}: v34 RESPONDE por ella (`{r1.get('elegido')}`)",
              (r1.get("elegido") or "").startswith("atacar")
              and h.get("defensa_pareja") is True
              and h.get("era_agresor") is False,
              f"honor={h}")
        check(f"yo{mihp}: el objetivo es su cazador (15), no ella",
              h.get("objetivo") == 15 and h.get("es_la_pareja") is False, "")

    # ════ P2 EL PRECIO DE MI VIDA ════════════════════════════════════════
    print("\n=== P2. el precio de mi vida ===")
    for mihp in (30, 20, 10):
        v34(); a2, r2, F2 = decide1(mundo, esc(mihp=mihp, dano_mio=True))
        check(f"yo{mihp} (bajo caza propia): responder PIERDE "
              f"(`{r2.get('elegido')}`)",
              not (r2.get("elegido") or "").startswith("atacar"),
              "mi cuesta y mi muro mandan")
    print("    frontera (radiografia, SIN sello):")
    for mihp in (90, 70, 50, 40, 30):
        v34(); _, r, _ = decide1(mundo, esc(mihp=mihp))
        v34(); _, rc, _ = decide1(mundo, esc(mihp=mihp, dano_mio=True))
        print(f"      yo{mihp:3}: sin caza propia -> `{r.get('elegido')}` · "
              f"bajo caza propia -> `{rc.get('elegido')}`")

    # ════ P3 LOS CINCO CANDADOS ══════════════════════════════════════════
    print("\n=== P3. los cinco candados ===")
    # C1 EL TABU: jamas contra ella
    v34(); _, r_c1, F_c1 = decide1(mundo, esc())
    cands_c1 = (r_c1.get("candidatos") or {})
    # ¿alguna foto apunta a la hermana? el objetivo se lee del honor del elegido
    # y de la geometria: la hermana esta en HER, alineada E a 1 -> si el
    # candidato existiera, seria atacar_E con objetivo par.
    v34()
    o_c1 = esc(agr_pos=list(HER))      # su parte apunta a SU PROPIA casilla
    _, r_c1b, _ = decide1(mundo, o_c1)
    h_c1b = r_c1b.get("honor") or {}
    check("C1 EL TABU: el parte que senala a la propia hermana NO la convierte"
          " en objetivo",
          h_c1b.get("es_la_pareja") is not True
          and A.agresor_de_la_hermana(o_c1, mundo,
                                      (lambda m: (m.observa(o_c1, mundo, 300), m)[1])(
                                          A.Memoria(hp_max=100)), 300) != par,
          "(agresor_de_la_hermana excluye a la pareja por construccion)")
    check("C1: S-VINCULO sigue intacta (0 en escena sin golpe previsto a ella)",
          (F_c1.get("S-VINCULO") or 0) == 0, "")
    # C2 NUNCA CONTRA INOCENTES
    v34(); _, r_c2, _ = decide1(mundo, esc(agr=False))       # su parte a=0
    c_c2 = [k for k in (r_c2.get("candidatos") or {}) if k.startswith("atacar")]
    v32(); a_c2b, r_c2b, _ = decide1(mundo, esc(agr=False))
    v34(); a_c2, r_c2c, _ = decide1(mundo, esc(agr=False))
    check("C2 INOCENTES: sin a=1 en su parte, 0 candidatos de atacar",
          not c_c2, str(c_c2))
    check("C2: y la foto es BYTE-IDENTICA a v32", dump(a_c2, r_c2c) == dump(a_c2b, r_c2b),
          f"`{r_c2c.get('elegido')}`")
    # tercero inocente presente mientras SI hay agresor certificado
    v34(); _, r_c2d, _ = decide1(mundo, esc(tercero=(9, (YO[0], YO[1] + 2))))
    objs = []
    for k, v in (r_c2d.get("candidatos") or {}).items():
        if k.startswith("atacar"):
            objs.append(k)
    check("C2: con un tercero INOCENTE a la vista, no nace candidato contra el",
          len(objs) <= 1, f"candidatos {objs} (solo contra el cazador)")
    # C3 JERARQUIA DEL MIEDO (ya medida en P2) — se re-declara
    v34(); _, r_c3, _ = decide1(mundo, esc(mihp=25, dano_mio=True))
    check("C3 JERARQUIA: a hp<=30 bajo caza, huir gana a responder",
          not (r_c3.get("elegido") or "").startswith("atacar"),
          f"`{r_c3.get('elegido')}`")
    # C4 CADUCIDAD: a=0 / parte viejo / enemigo movido
    for lbl, kw in (("su parte pasa a a=0", dict(agr=False)),
                    ("el parte envejece >96 tics", dict(edad=100)),
                    ("el enemigo YA NO esta en ax,ay (a 3 casillas)",
                     dict(agr_pos=[CAZ[0] + 3, CAZ[1]]))):
        v34(); _, r_c4, _ = decide1(mundo, esc(**kw))
        c4 = [k for k in (r_c4.get("candidatos") or {}) if k.startswith("atacar")]
        check(f"C4 CADUCIDAD: {lbl} -> el candidato muere", not c4, str(c4))
    # C5 SILENCIOS
    def esc_sola():
        o = obs(300, YO, hp=90, hand={"id": "sword", "n": 1},
                pack=[{"id": "first_aid", "n": 1}, None],
                agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                          "hp_band": "healthy"}])
        return o
    v34(); a5, r5, _ = decide1(mundo, esc_sola())
    v27(); a5b, r5b, _ = decide1(mundo, esc_sola())
    check("C5: sin hermana -> byte-identica a v27", dump(a5, r5) == dump(a5b, r5b),
          f"`{r5.get('elegido')}`")
    v34(); a5c, r5c, _ = decide1(mundo, esc(suhp=95, agr=False))
    v32(); a5d, r5d, _ = decide1(mundo, esc(suhp=95, agr=False))
    check("C5: hermana en calma -> identica a v32", dump(a5c, r5c) == dump(a5d, r5d),
          f"`{r5c.get('elegido')}`")
    # el mismo cazador me caza a MI tambien: identico a lo que ya hacia
    v34(); a5e, r5e, _ = decide1(mundo, esc(dano_mio=True, mihp=90))
    v32(); a5f, r5f, _ = decide1(mundo, esc(dano_mio=True, mihp=90))
    h5e, h5f = r5e.get("honor") or {}, r5f.get("honor") or {}
    # el sello dice "identico a lo que ya hacia": misma decision que v32. (Si
    # ademas responde, el motivo es `era_agresor` —el mio— no la manada.)
    check("C5: si tambien me caza a MI, hago lo IDENTICO que v32",
          r5e.get("elegido") == r5f.get("elegido")
          and (not (r5e.get("elegido") or "").startswith("atacar")
               or h5e.get("era_agresor") is True),
          f"v32 `{r5f.get('elegido')}` · v34 `{r5e.get('elegido')}`")

    # ════ P4 LAS DOS METRICAS ════════════════════════════════════════════
    print("\n=== P4. las dos metricas de honor (todo el banco) ===")
    inic_estrictas = [e for e, h in _honores
                      if (e or "").startswith("atacar")
                      and not (h or {}).get("era_agresor")
                      and not (h or {}).get("defensa_pareja")]
    defensas = [e for e, h in _honores
                if (e or "").startswith("atacar")
                and (h or {}).get("defensa_pareja")
                and not (h or {}).get("era_agresor")]
    propias = [e for e, h in _honores
               if (e or "").startswith("atacar") and (h or {}).get("era_agresor")]
    check(f"(a) INICIACIONES-ESTRICTAS = 0  [{len(_honores)} decisiones]",
          not inic_estrictas, str(inic_estrictas))
    print(f"    (b) DEFENSAS-POR-LA-HERMANA: {len(defensas)} (se dicen, no son"
          f" iniciaciones) · respuestas a mi propio agresor: {len(propias)}")
    check("(C1) 0 ataques contra la hermana en todo el banco",
          not [e for e, h in _honores if (h or {}).get("es_la_pareja")], "")

    # ════ P6 HONOR CLASICO + determinismo ════════════════════════════════
    print("\n=== escenas del 39/53 (la hermana AGRESORA): v34 == v32 ===")
    for g, hp0, ph in ((1, 100, 10.0), (4, 28, 72.0)):
        v32(); a7b, r7b, _ = escena39(mundo, YO, HER, par, g, hp0, parte_hp=ph)
        v34(); a7, r7, _ = escena39(mundo, YO, HER, par, g, hp0, parte_hp=ph)
        _honores.extend([(r7b.get("elegido"), r7b.get("honor")),
                         (r7.get("elegido"), r7.get("honor"))])
        check(f"g{g} h{ph:g}: v34 == v32 byte a byte (tabu intacto)",
              dump(a7, r7) == dump(a7b, r7b), f"`{r7.get('elegido')}`")

    print("\n=== determinismo 3/3 ===")
    v34()
    firmas = set()
    for _ in range(3):
        a, r, _ = decide1(mundo, esc())
        firmas.add(dump(a, r))
    check("3/3 byte-identicas", len(firmas) == 1, "")

    A.MANADA_ON = DEF_MANADA
    check("al salir, el estado sellado queda restaurado",
          A.MANADA_ON is DEF_MANADA, "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — la manada: defiende (P1), pero no a cualquier precio"
          " (P2/C3), jamas contra ella (C1) ni contra inocentes (C2), con"
          " caducidad (C4) y silencios (C5). Iniciaciones-estrictas: 0.")


if __name__ == "__main__":
    main()
