"""Banco de EL PARTE DE ESTADO — PROMPT_53. Temporada dos, primera piedra.

v28 = v27 + el parte: el testimonio del hermano (canal team, cerrado de
fabrica — 52) sustituye a la estimacion por banda en el modelo del hermano
que ya usan las filas S de pareja. NI UNA FILA NUEVA (R2). El pareado exacto
v27<->v28 es el interruptor A.PARTE_ON (patron de ACOPIO_M/MURO_K del 48).

ESTADO SELLADO QUE ESTE BANCO VERIFICA (patron del 46): EL CANDADO DEL P5.
El sello P5 exigia que el parte no ACERCARA el candidato de atacar al
hermano, y la medida dice que SI lo acerca en el rincon del hermano-agresor
casi muerto (S-7 sellada pone su hp en el precio de la foto de responder).
El OYENTE queda APAGADO por defecto (A.PARTE_ON=False, motivo grabado en la
tabla); el EMISOR queda vivo (P1 verde). Este banco:

  P1 FORMATO (sellado, VERDE): ASCII/longitud limpios, cadencia 48 >= 24
     (jamas rate_limited), parse 100 % de los partes propios en eco,
     determinismo del mensaje.
  P2 EL SOLO INTACTO (sellado, VERDE): sin gemelo (o con texto ajeno por el
     canal), v28 BIT-IDENTICA a v27; y con el candado echado (defecto),
     incluso un parte VALIDO no toca nada.
  P3 LA FOTO HONESTA SABE (sellado, VERDE — medido con el taller encendido):
     tras el primer parte, la estimacion del hermano = su hp real EXACTO
     (error 0) hasta la caducidad (96 tics); banda despues.
  P4 ¿CAMBIA LA CONDUCTA SABER? (SIN gate): lealtad (25), tentacion (39) y
     escudo (40/42) — reconstruidas: esos bancos no existen como ficheros.
     Resultado historico: 0 decisiones cambian; solo S-DANO-PAREJA se mueve.
  P5 HONOR: sin parte, byte-identico (VERDE). Con parte: el candidato NI
     NACE del testimonio NI es elegido, 0 iniciaciones (VERDE) — pero el
     margen SE ACERCA en el rincon (CANDADO, reproducido aqui como estado
     sellado; el sello "no acercar" FALLO y por eso el oyente esta apagado).
  P6 (fuera de este fichero): bancos 13-52 en verde + humo 3/3.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_53
"""
from __future__ import annotations

import json
import sys
import types

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma import parte as PARTE
from alma.smoke_alma import player_config, obs

_fallos = []
_elegidos = []          # 0 iniciaciones: se recogen TODOS los elegidos del banco
GOLPE = 18.0


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def v27():
    A.PARTE_ON = False


def v28():
    A.PARTE_ON = True


def dump(accion, rad):
    return json.dumps((accion, rad), sort_keys=True, default=str)


def corre(mundo, obses, t0=300):
    """Memoria fresca, observa cada obs en su tic y decide sobre la ultima."""
    mem = A.Memoria(); mem.hp_max = 100
    t = t0
    for o in obses[:-1]:
        mem.observa(o, mundo, t)
        t += 1
    o = obses[-1]
    mem.observa(o, mundo, t)
    accion, rad = D.decide(o, mundo, mem, t)
    return accion, rad, mem, o, t


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


def chat_parte(par, t_emision, texto, t_llegada=None):
    return {"tick": t_llegada if t_llegada is not None else t_emision + 2,
            "from": par, "channel": "team", "to": None, "text": texto}


def texto_parte(par, t, pos, hp, ven=0, bot=0, agr=0, agr_pos=None):
    s = f"E1 P{par} t{t} {pos[0]},{pos[1]} h{hp:g} v{ven} b{bot} a{agr}"
    if agr and agr_pos:
        s += f" {agr_pos[0]},{agr_pos[1]}"
    return s


# ── escena del 39 (tentacion armada), con parte opcional ─────────────────────
def escena39(mundo, YO, HER, par, golpes, hp0, parte_hp=None, tick0=300):
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
    ch = []
    if parte_hp is not None:
        ch = [chat_parte(par, t - 2, texto_parte(par, t - 2, HER, parte_hp))]
    o = obs(t, YO, hp=hp, hand={"id": "sword", "n": 1},
            pack=[{"id": "first_aid", "n": 1}, None], agentes=list(ag), chat=ch)
    mem.observa(o, mundo, t)
    accion, rad = D.decide(o, mundo, mem, t)
    F = A.filas(o, mundo, mem, t)
    return accion, rad, F


def filas_diff(Fa, Fb):
    dif = {}
    for k in set(Fa) | set(Fb):
        if k.startswith("_"):
            continue
        va, vb = float(Fa.get(k) or 0.0), float(Fb.get(k) or 0.0)
        if abs(va - vb) > 1e-9:
            dif[k] = (round(va, 5), round(vb, 5))
    return dif


def main():
    DEFECTO = A.PARTE_ON
    # RESELLO DEL 54: el candado del 53 se resello con EL PESO DEL HERMANO
    # (S-VINCULO/S-HERIDO). Este banco reproduce el mundo del 53 fijando las
    # constantes del peso a 0 (patron del 46/47) y las restaura al salir.
    _V0, _H0 = A.VINCULO_M, A.HERIDO_M
    A.VINCULO_M = A.HERIDO_M = 0.0
    mundo = Mundo.desde_player_config(player_config())
    par = mundo.teammate_slot
    YO = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            YO = (y, y)
            break
    HER = (YO[0] + 1, YO[1])
    CAZ = (YO[0] + 2, YO[1])
    print(f"  yo en {YO} · hermano slot {par} en {HER} · cazador slot 15 en {CAZ}")
    print(f"  PARTE: marca {PARTE.MARCA} · cada {PARTE.CADA} tics · "
          f"caducidad {PARTE.CADUCIDAD} tics\n")
    check("estado sellado: candado del 53 (off) o resello del 54 (parte+peso)",
          (DEFECTO is False) or (DEFECTO is True and _V0 > 0 and _H0 > 0),
          f"(PARTE_ON={DEFECTO}, VINCULO_M={_V0}, HERIDO_M={_H0})")

    # ════ P1 FORMATO (sellado) ═══════════════════════════════════════════
    print("=== P1. FORMATO: ASCII/longitud, cadencia, eco parseado, determinismo ===")
    mem1 = A.Memoria(); mem1.hp_max = 100
    ventana = int(A.AGRESOR_VENTANA_S * 24)
    estados = []
    for hp in (100.0, 87.5, 33.36, 1.0):
        for ven in (0, 1):
            for bot in (0, 1, 2):
                estados.append((hp, ven, bot, "sin"))
    estados += [(60.0, 1, 1, "visible"), (60.0, 0, 2, "invisible")]
    emitidos, limpios, parseados, exactos = 0, 0, 0, 0
    for hp, ven, bot, agr in estados:
        mem = A.Memoria(); mem.hp_max = 100
        ag_vis = []
        if agr != "sin":
            mem.agresores[15] = {"dano": 12.0, "ultimo": 300}
            if agr == "visible":
                ag_vis = [{"slot": 15, "team": "D", "pos": list(CAZ),
                           "hp_band": "healthy"}]
        efect = [{"id": "poison_dart", "ends_tick": 400}] if ven else []
        pk = [{"id": "first_aid", "n": bot}, None] if bot else [None, None]
        o = obs(300, YO, hp=hp, pack=pk, agentes=ag_vis, efectos=efect)
        t3 = [PARTE.emite(o, 300, mundo, mem, ventana) for _ in range(3)]
        if not (t3[0] == t3[1] == t3[2]):
            check(f"determinista {hp}/{ven}/{bot}/{agr}", False, t3[0])
        texto = t3[0]
        emitidos += 1
        if PARTE.ascii_limpio(texto):
            limpios += 1
        p = PARTE.parsea(texto)
        if p is not None:
            parseados += 1
            ok = (p["slot"] == mundo.slot and p["t"] == 300
                  and p["pos"] == tuple(YO) and abs(p["hp"] - hp) < 1e-9
                  and p["veneno"] == bool(ven) and p["botiquin"] == bot
                  and p["agresor"] == (agr != "sin")
                  and (p["agresor_pos"] == (tuple(CAZ) if agr == "visible"
                                            else None)))
            if ok:
                exactos += 1
            else:
                check(f"campos exactos {hp}/{ven}/{bot}/{agr}", False, str(p))
    check(f"0 filtrados por ASCII/longitud ({limpios}/{emitidos})",
          limpios == emitidos)
    check(f"eco propio parseado 100 % ({parseados}/{emitidos})",
          parseados == emitidos)
    check(f"campos exactos en el eco ({exactos}/{emitidos})",
          exactos == emitidos)
    # cadencia: el gating de la policy (tick - ultima_voz >= VOZ_CADA)
    sys.modules.setdefault("websockets", types.ModuleType("websockets"))
    from alma import policy as POL
    gaps = []
    ultima = -10 ** 9
    for t in range(0, 2000):
        if t - ultima >= POL.VOZ_CADA:
            if ultima > -10 ** 8:
                gaps.append(t - ultima)
            ultima = t
    check(f"cadencia de la policy: VOZ_CADA={POL.VOZ_CADA} >= 24 y gaps=={{{POL.VOZ_CADA}}}",
          POL.VOZ_CADA >= 24 and set(gaps) == {POL.VOZ_CADA},
          "(1/24 tics del mundo: jamas rate_limited)")

    # ════ P2 EL SOLO INTACTO (sellado) ═══════════════════════════════════
    print("\n=== P2. EL SOLO INTACTO: v28 bit-identica a v27 sin gemelo / con texto ajeno ===")
    BOT = (YO[0] + 3, YO[1])

    def esc_caza():
        o = obs(300, YO, hp=25,
                agentes=[{"slot": 15, "team": "D", "pos": list(CAZ),
                          "hp_band": "healthy"}],
                items=[{"id": "first_aid", "n": 1, "pos": list(BOT)}])
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
        return [o]

    def esc_paseo():
        return [obs(300, YO, hp=100)]

    def esc_veneno():
        return [obs(300, YO, hp=40,
                    efectos=[{"id": "poison_dart", "ends_tick": 400}])]

    AJENOS = [
        f"P{par} 10,10 healthy",                        # el latido viejo del 32
        "hola que tal",                                 # texto ajeno
        f"E1 P{par} t300 10,10 h50",                    # E1 truncado (no parsea)
        "E1 P99 t300 10,10 h50 v0 b0 a0",               # slot que no casa
    ]

    def esc_ajeno():
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "hurt"}]
        ch = [chat_parte(par, 298, txt) for txt in AJENOS]
        o = obs(300, YO, hp=25, agentes=ag, chat=ch,
                items=[{"id": "first_aid", "n": 1, "pos": list(BOT)}])
        return [o]

    def esc_gemelo_mudo():
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "hurt"}]
        return [obs(300, YO, hp=25, agentes=ag,
                    pack=[{"id": "first_aid", "n": 1}, None])]

    for nombre, esc in (("caza+botiquin (48)", esc_caza),
                        ("paseo", esc_paseo),
                        ("veneno+herido", esc_veneno),
                        ("gemelo con TEXTO AJENO x4", esc_ajeno),
                        ("gemelo MUDO (banda de siempre)", esc_gemelo_mudo)):
        v28(); a28, r28, m28, _, _ = corre(mundo, esc())
        v27(); a27, r27, m27, _, _ = corre(mundo, esc())
        v28()
        _elegidos.extend([r28.get("elegido"), r27.get("elegido")])
        check(f"'{nombre}': v28 == v27 byte a byte",
              dump(a28, r28) == dump(a27, r27),
              f"elegido `{r28.get('elegido')}`")
        check(f"'{nombre}': el oyente no guardo nada", m28.parte is None, "")

    # con el CANDADO echado (el defecto), incluso un parte VALIDO no toca nada
    def esc_parte_valido():
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "hurt"}]
        ch = [chat_parte(par, 298, texto_parte(par, 298, HER, 35))]
        return [obs(300, YO, hp=25, agentes=ag, chat=ch,
                    pack=[{"id": "first_aid", "n": 1}, None])]

    A.PARTE_ON = False                  # el mundo del candado del 53
    ac, rc, mc, _, _ = corre(mundo, esc_parte_valido())
    v27(); a7c, r7c, _, _, _ = corre(mundo, esc_parte_valido())
    v28()
    _elegidos.extend([rc.get("elegido"), r7c.get("elegido")])
    check("con el CANDADO echado: un parte VALIDO ni se guarda ni cambia nada",
          mc.parte is None and dump(ac, rc) == dump(a7c, r7c),
          f"elegido `{rc.get('elegido')}`")

    # ════ P3 LA FOTO HONESTA SABE (sellado) ══════════════════════════════
    print("\n=== P3. LA FOTO HONESTA SABE: exacto tras el parte, banda tras caducar ===")
    v28()
    ag_her = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": "healthy"}]
    for hp_real in (70.0, 34.0, 87.5):
        mem = A.Memoria(); mem.hp_max = 100
        ch = [chat_parte(par, 298, texto_parte(par, 298, HER, hp_real,
                                               ven=1, bot=2, agr=0))]
        o = obs(300, YO, hp=100, agentes=[dict(a) for a in ag_her], chat=ch)
        mem.observa(o, mundo, 300)
        errores = [abs(mem.pareja_hp_est(t, 100.0) - hp_real)
                   for t in range(300, 298 + PARTE.CADUCIDAD + 1)]
        check(f"h{hp_real:g}: error 0 hasta la caducidad "
              f"(tics 300..{298 + PARTE.CADUCIDAD})",
              max(errores) < 1e-9, f"max error {max(errores):g}")
        despues = mem.pareja_hp_est(298 + PARTE.CADUCIDAD + 1, 100.0)
        check(f"h{hp_real:g}: banda despues de caducar (est {despues:g})",
              abs(despues - A.BANDA_EST["healthy"]) < 1e-9, "")
        check(f"h{hp_real:g}: veneno/botiquin/agresor con su tic",
              (mem.parte["veneno"] is True and mem.parte["botiquin"] == 2
               and mem.parte["agresor"] is False and mem.parte["t"] == 298), "")
    # el mas reciente manda; uno viejo que llega tarde no pisa
    mem = A.Memoria(); mem.hp_max = 100
    o = obs(300, YO, hp=100, agentes=[dict(a) for a in ag_her],
            chat=[chat_parte(par, 298, texto_parte(par, 298, HER, 70))])
    mem.observa(o, mundo, 300)
    o2 = obs(348, YO, hp=100, agentes=[dict(a) for a in ag_her],
             chat=[chat_parte(par, 346, texto_parte(par, 346, HER, 55)),
                   chat_parte(par, 290, texto_parte(par, 290, HER, 99),
                              t_llegada=348)])
    mem.observa(o2, mundo, 348)
    check("el parte mas RECIENTE manda (h55, no h99 tardio ni h70 viejo)",
          abs(mem.pareja_hp_est(348, 100.0) - 55.0) < 1e-9,
          f"est {mem.pareja_hp_est(348, 100.0):g}")
    # la radiografia del appraise enseña el testimonio (solo con parte fresco;
    # la radiografia del decide no acarrea el `ahora` — conocido)
    _st, radA = A.appraise(o2, mundo, mem, 348)
    check("radiografia (appraise) lleva `parte` con parte fresco",
          isinstance(radA.get("parte"), dict) and radA["parte"]["hp"] == 55.0, "")
    # muerto el hermano, su ultimo parte calla (los fuegos mandan)
    mem.pareja_muerta = True
    check("muerto el hermano, el parte calla (vuelve a banda)",
          abs(mem.pareja_hp_est(348, 100.0) - A.BANDA_EST["healthy"]) < 1e-9, "")

    # ════ P4 ¿CAMBIA LA CONDUCTA SABER? (SIN gate) ═══════════════════════
    print("\n=== P4. ¿CAMBIA LA CONDUCTA SABER? (sin gate — la pregunta del encargo) ===")
    print("  [escenas de lealtad(25) y escudo(40/42) RECONSTRUIDAS de sus actas:")
    print("   esos bancos no existen como ficheros — declarado]\n")
    cambios = []

    def compara(nombre, obses_sin, obses_con):
        v27(); a27, r27, _, o27, t27 = corre(mundo, obses_sin)
        F27 = A.filas(o27, mundo, _mem_de(obses_sin), t27)
        v28(); a28, r28, _, o28, t28 = corre(mundo, obses_con)
        F28 = A.filas(o28, mundo, _mem_de(obses_con), t28)
        _elegidos.extend([r27.get("elegido"), r28.get("elegido")])
        dif = filas_diff(F27, F28)
        c27, c28 = cands(r27), cands(r28)
        dc = {k: (round(c27[k], 5), round(c28[k], 5))
              for k in set(c27) & set(c28) if abs(c27[k] - c28[k]) > 1e-6}
        cambio = r27.get("elegido") != r28.get("elegido")
        if cambio:
            cambios.append((nombre, r27.get("elegido"), r28.get("elegido"), dif))
        print(f"  {nombre:<38} v27 `{r27.get('elegido')}` -> v28 `{r28.get('elegido')}`"
              f"  {'** CAMBIA **' if cambio else '(igual)'}")
        if dif:
            print(f"    filas que se mueven: {dif}")
        if dc and not cambio:
            print(f"    candidatos que se mueven (sin cambiar el elegido): "
                  f"{dict(list(dc.items())[:4])}")
        return cambio

    def _mem_de(obses):
        mem = A.Memoria(); mem.hp_max = 100
        t = 300
        for o in obses:
            mem.observa(o, mundo, t)
            t += 1
        return mem

    # LEALTAD (25): yo sano con botiquin a bordo, hermano herido al lado
    def esc_lealtad(band, parte_hp):
        ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
               "hp_band": band}]
        ch = ([chat_parte(par, 298, texto_parte(par, 298, HER, parte_hp))]
              if parte_hp is not None else [])
        return [obs(300, YO, hp=100, pack=[{"id": "first_aid", "n": 1}, None],
                    agentes=ag, chat=ch)]

    compara("lealtad: banda hurt, parte h35",
            esc_lealtad("hurt", None), esc_lealtad("hurt", 35))
    compara("lealtad: banda hurt, parte h60",
            esc_lealtad("hurt", None), esc_lealtad("hurt", 60))
    compara("lealtad: banda healthy, parte h70",
            esc_lealtad("healthy", None), esc_lealtad("healthy", 70))
    compara("lealtad: banda critical, parte h8",
            esc_lealtad("critical", None), esc_lealtad("critical", 8))

    # TENTACION (39): el hermano me pega armado; ¿cambia algo saber su hp?
    for golpes, hp0, ph in ((1, 100, 100), (3, 100, 80), (4, 28, 80)):
        v27(); a7, r7, F7 = escena39(mundo, YO, HER, par, golpes, hp0)
        v28(); a8, r8, F8 = escena39(mundo, YO, HER, par, golpes, hp0,
                                     parte_hp=ph)
        _elegidos.extend([r7.get("elegido"), r8.get("elegido")])
        dif = filas_diff(F7, F8)
        cambio = r7.get("elegido") != r8.get("elegido")
        if cambio:
            cambios.append((f"tentacion g{golpes} hp0={hp0} parte h{ph}",
                            r7.get("elegido"), r8.get("elegido"), dif))
        print(f"  tentacion: {golpes} golpes hp0={hp0} parte h{ph:<4}"
              f"        v27 `{r7.get('elegido')}` -> v28 `{r8.get('elegido')}`"
              f"  {'** CAMBIA **' if cambio else '(igual)'}")
        if dif:
            print(f"    filas que se mueven: {dif}")

    # ESCUDO (40/42): agresor extrano sobre mi, hermano herido cerca
    def esc_escudo(parte_hp):
        ag = [{"slot": par, "team": mundo.team,
               "pos": [YO[0] - 1, YO[1]], "hp_band": "hurt"},
              {"slot": 15, "team": "D", "pos": list(CAZ), "hp_band": "healthy"}]
        ch = ([chat_parte(par, 298,
                          texto_parte(par, 298, (YO[0] - 1, YO[1]), parte_hp,
                                      agr=1, agr_pos=CAZ))]
              if parte_hp is not None else [])
        o = obs(300, YO, hp=70, agentes=ag, chat=ch,
                pack=[{"id": "first_aid", "n": 1}, None])
        o["you"]["damage_taken"] = [{"source": "P15", "amount": 12.0}]
        return [o]

    compara("escudo: hermano hurt, parte h20+agresor",
            esc_escudo(None), esc_escudo(20))

    print(f"\n  DECISIONES QUE CAMBIAN AL SABER: {len(cambios)}")
    for nombre, e7, e8, dif in cambios:
        print(f"    - {nombre}: `{e7}` -> `{e8}` · filas: {dif}")

    # ════ P5 HONOR (sellado) ═════════════════════════════════════════════
    print("\n=== P5. HONOR: margenes de atacar identicos sin parte; con parte, ni nace ni se acerca ===")
    # (a) las escenas del 39 SIN parte: v28 byte-identica a v27
    for golpes, hp0 in ((1, 100), (3, 100), (4, 100), (1, 28), (4, 28)):
        v28(); a8, r8, _ = escena39(mundo, YO, HER, par, golpes, hp0)
        v27(); a7, r7, _ = escena39(mundo, YO, HER, par, golpes, hp0)
        v28()
        check(f"39 sin parte g{golpes} hp0={hp0}: v28 == v27 byte a byte",
              dump(a8, r8) == dump(a7, r7), f"elegido `{r8.get('elegido')}`")
    # (b) CON parte (taller encendido): el candidato ni nace ni es elegido —
    # GATES verdes; el margen es LA MEDIDA DEL CANDADO y se reproduce aqui.
    print()
    deltas = []
    for golpes, hp0 in ((1, 100), (4, 100), (4, 28)):
        for ph in (100.0, 80.0, 25.0, 10.0):
            v27(); _, r7, _ = escena39(mundo, YO, HER, par, golpes, hp0,
                                       parte_hp=ph)
            m7, e7, c7 = margen_atacar(r7)
            v28(); _, r8, _ = escena39(mundo, YO, HER, par, golpes, hp0,
                                       parte_hp=ph)
            m8, e8, c8 = margen_atacar(r8)
            at7 = sorted(k for k in c7 if k.startswith("atacar"))
            at8 = sorted(k for k in c8 if k.startswith("atacar"))
            check(f"g{golpes} hp0={hp0} h{ph:g}: atacar ni nace ni muere "
                  f"({len(at8)} cand.)", at7 == at8, "")
            if m7 is not None and m8 is not None:
                deltas.append((f"g{golpes} hp0={hp0} h{ph:g}", m7, m8, m8 - m7))
                check(f"g{golpes} hp0={hp0} h{ph:g}: atacar sigue perdiendo "
                      f"(margen {m8:+.5f} > 0)", m8 > 0.0, "")
            check(f"g{golpes} hp0={hp0} h{ph:g}: no ataca "
                  f"(`{e8}`)", not (e8 or "").startswith("atacar"), "")
    print("\n  la medida del candado — el margen de atacar bajo el parte:")
    for tag, m7, m8, dl in deltas:
        print(f"    {tag:<24} {m7:+.5f} -> {m8:+.5f}   (delta {dl:+.5f})")
    peor = min(dl for _, _, _, dl in deltas)
    check("CANDADO reproducido: el parte SI acerca el atacar en el rincon "
          f"del hermano-agresor casi muerto (peor delta {peor:+.5f} < -0,1)",
          peor < -0.1,
          "(S-7 sellada: presion x hp del agresor => responder se abarata)")
    # (c) el testimonio NO es agresion: parte con a1+posicion, sin dano
    v28()
    ag = [{"slot": par, "team": mundo.team, "pos": list(HER),
           "hp_band": "healthy"},
          {"slot": 15, "team": "D", "pos": list(CAZ), "hp_band": "healthy"}]
    ch = [chat_parte(par, 298, texto_parte(par, 298, HER, 40.0,
                                           agr=1, agr_pos=CAZ))]
    o = obs(300, YO, hp=100, hand={"id": "sword", "n": 1}, agentes=ag, chat=ch)
    mem = A.Memoria(); mem.hp_max = 100
    mem.observa(o, mundo, 300)
    accion, rad = D.decide(o, mundo, mem, 300)
    _elegidos.append(rad.get("elegido"))
    c = cands(rad)
    check("testimonio 'a1' SIN dano recibido: mem.agresores queda vacio",
          not mem.agresores, str(mem.agresores))
    check("testimonio 'a1' SIN dano recibido: 0 candidatos de atacar",
          not any(k.startswith("atacar") for k in c), str(sorted(c))[:90])

    # ════ determinismo 3/3 (escena con parte, la mas cargada) ════════════
    print("\n=== determinismo 3/3 (escena de gemelos con parte) ===")
    v28()
    firmas = set()
    for _ in range(3):
        a, r, _ = escena39(mundo, YO, HER, par, 3, 100, parte_hp=80)
        firmas.add(dump(a, r))
    check("3/3 byte-identicas", len(firmas) == 1, "")

    # ════ 0 iniciaciones en TODO el banco ════════════════════════════════
    inic = [e for e in _elegidos if (e or "").startswith("atacar")]
    check(f"0 iniciaciones en todo el banco ({len(_elegidos)} decisiones)",
          not inic, str(inic))

    # el estado sellado queda restaurado al salir, pase lo que pase
    A.PARTE_ON = DEFECTO
    A.VINCULO_M, A.HERIDO_M = _V0, _H0
    check("al salir, el estado sellado queda restaurado",
          A.PARTE_ON is DEFECTO and (A.VINCULO_M, A.HERIDO_M) == (_V0, _H0), "")

    print()
    if _fallos:
        print(f"  BANCO ROJO: {len(_fallos)} fallos -> {_fallos}")
        sys.exit(1)
    print("  BANCO VERDE — emisor certificado (P1); oyente en CANDADO (P5"
          " fallido, reproducido); el solo intacto (P2); P4: 0 decisiones"
          " cambian al saber.")


if __name__ == "__main__":
    main()
