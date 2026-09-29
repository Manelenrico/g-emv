"""Banco de LA PUERTA DEL PROYECTIL — PROMPT_41. Fontaneria + fisica.

A) GATE DE NEUTRALIDAD (sellado). La fontaneria del 41 anade al diario los
   campos que la espec publica y el registro tiraba: hand/body/netted/poisoned/
   channeling de otros y `ve_proyectiles` (con `shooter`). El alma recibe la
   obs CRUDA (policy.decidir pasa `obs` tal cual a mem.observa y D.decide),
   asi que la conducta no puede depender del diario — pero el gate se CORRE,
   no se supone: el mismo guion antes/despues, bit-identico, 3/3.

   "Antes" = el registro VIEJO, congelado aqui verbatim (el filtro de 4 claves
   que vivia en policy.py/policy_repetidor_forense.py hasta el commit del 40).

B) FISICA DE LA INTERCEPTACION, certificada en `sim.nim` (0.1.18) con lineas:
   - 873-878 spawnProjectile: nace en la casilla del TIRADOR, con su `dir` y
     `remaining` = alcance del arma. NO lleva blanco: es una linea en vuelo.
   - 963-996 advanceProjectiles: 2 casillas/tic, en orden de disparo. En cada
     casilla que pisa: si hay un agente y NO es el tirador -> tirada de esquiva
     `rand(100) < 2*ATH` (980); si esquiva, ATRAVIESA y sigue; si no, GOLPEA a
     ESE agente y muere. Muro (`blocksSight`) lo mata; fin de alcance -> cae al
     suelo como objeto cogible.
   - EL PRIMER CUERPO EN LA LINEA SE LLEVA EL GOLPE, hermano o extrano, blanco
     o interpuesto. La interposicion ES fisica real de este mundo.
   - iNet -> reda (NetTicks); iDarts -> dano + veneno (applyPoison, 956-960);
     resto -> dano del arma (projectileDamage, 948-953).
   - la victima recibe `damage_taken` con `source = shooter` (applyDamage):
     el interpuesto SABRIA quien disparo.
   - cadencia: arco `bowDraw = 18 - ATH div 2` (871, 934); lo demas, el
     `cooldown` del catalogo (941).

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_41
"""
from __future__ import annotations

import json
import math
import sys
import types

# policy.py importa websockets (solo para el ws real); aqui no hay red.
if "websockets" not in sys.modules:
    sys.modules["websockets"] = types.ModuleType("websockets")

from alma.mundo import Mundo
from alma import policy as P
from alma import policy_repetidor_forense as PF
from alma.smoke_alma import player_config, obs

_fallos = []


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def registro_viejo(obs_, intent, mem, social):
    """El registro ANTES del 41, congelado verbatim (las claves del diario que
    construian policy.py:157-175 y policy_repetidor_forense.py:120-139)."""
    you = obs_.get("you") or {}
    vis = obs_.get("visible") or {}
    return {"k": "tick", "tick": obs_.get("tick"), "phase": obs_.get("phase"),
            "pos": you.get("pos"), "hp": you.get("hp"),
            "hand": you.get("hand"), "body": you.get("body"),
            "pack": you.get("pack"), "effects": you.get("effects"),
            "action_result": you.get("action_result"),
            "move_ready_in": you.get("move_ready_in"),
            "kills": you.get("kills"), "damage_dealt": you.get("damage_dealt"),
            "damage_taken": you.get("damage_taken"),
            "zona": obs_.get("zone"),
            "ve_agentes": [{"slot": a.get("slot"), "team": a.get("team"),
                            "pos": a.get("pos"), "hp_band": a.get("hp_band")}
                           for a in vis.get("agents") or []],
            "ve_items": vis.get("items", []), "ve_bushes": vis.get("bushes", []),
            "eventos": obs_.get("events", []), "chat": obs_.get("chat", []),
            "intencion": intent,
            "B": round(mem.roce_B, 4),
            "sin_compania_ticks": mem.ticks_sin_compania,
            "pareja_muerta": mem.pareja_muerta,
            "social": social}


def guion(mundo):
    """~30 tics variados: hermano, hostil, botin, dano recibido y PROYECTILES
    en vuelo con shooter — el guion identico para el antes y el despues."""
    par = mundo.teammate_slot
    YO = None
    for y in range(8, mundo.arena_size - 12):
        if all(not mundo.solido(x, y) for x in range(y - 6, y + 12)):
            YO = (y, y)
            break
    outs = []
    for i in range(30):
        t = 300 + i
        ag = [{"slot": par, "team": mundo.team, "pos": [YO[0] + 2, YO[1]],
               "hp_band": "healthy", "hand": "sword", "body": None,
               "netted": False, "poisoned": (i % 7 == 0), "channeling": False}]
        if i >= 10:
            ag.append({"slot": 15, "team": "D", "pos": [YO[0] + 5, YO[1] + 1],
                       "hp_band": "hurt", "hand": "bow", "body": "backpack",
                       "netted": False, "poisoned": False, "channeling": False})
        o = obs(t, YO, hp=100 - i,
                hand={"id": "sword", "n": 1} if i > 5 else None,
                items=[{"id": "rations", "n": 1, "pos": [YO[0] - 3, YO[1]]}],
                agentes=ag)
        if i >= 12:                      # proyectiles en vuelo, con autor
            o["visible"]["projectiles"] = [
                {"pos": [YO[0] + 4 - (i % 3), YO[1] + 1], "dir": "W",
                 "kind": "arrow", "shooter": 15}]
        if i in (8, 9):
            o["you"]["damage_taken"] = [{"source": "P15", "amount": 9.0}]
        outs.append(o)
    return outs


def corre(mundo, obs_seq, mapa):
    """Pasa el guion por el ciclo REAL de policy.Alma. `mapa` = 'viejo' o
    'nuevo' decide que registro de diario se construye. Devuelve (acciones,
    radiografias, recs)."""
    alma = P.Alma()
    alma.mundo = mundo
    capturado = []
    log_orig = P.log
    P.log = lambda rec: capturado.append(rec)
    try:
        acciones, radios = [], []
        for o in obs_seq:
            accion, radio = alma.decidir(o)
            alma.intent = accion
            acciones.append(accion)
            radios.append(radio)
            if mapa == "nuevo":
                alma.registrar(o, radio)
            else:
                capturado.append(registro_viejo(
                    o, alma.intent, alma.mem, alma._social(o)))
    finally:
        P.log = log_orig
    return acciones, radios, capturado


def main():
    mundo = Mundo.desde_player_config(player_config())

    # ── A. el gate de neutralidad ─────────────────────────────────────────
    print("=== A. GATE DE NEUTRALIDAD: mismo guion, antes/despues, 3/3 ===")
    firmas = set()
    ok_schema = ok_p2 = True
    for corrida in range(3):
        g = guion(mundo)
        a_v, r_v, recs_v = corre(mundo, g, "viejo")
        a_n, r_n, recs_n = corre(mundo, g, "nuevo")
        # `ms` es reloj de pared (policy.decidir lo estampa): se excluye de
        # la firma — es el UNICO campo volatil de la radiografia.
        def _limpia(radios):
            out = []
            for r in radios:
                if r is None:
                    out.append(None); continue
                r2 = dict(r); r2.pop("ms", None)
                out.append(r2)
            return out
        ja = json.dumps([a_v, _limpia(r_v)], sort_keys=True)
        jb = json.dumps([a_n, _limpia(r_n)], sort_keys=True)
        check(f"corrida {corrida+1}: DECISIONES bit-identicas antes/despues",
              ja == jb, f"({len(a_v)} acciones)")
        firmas.add(ja)
        # el rec nuevo, proyectado al esquema viejo, == el rec viejo
        for rv, rn in zip(recs_v, recs_n):
            proy = dict(rn)
            proy.pop("ve_proyectiles", None)
            proy["ve_agentes"] = [{k: e.get(k) for k in
                                   ("slot", "team", "pos", "hp_band")}
                                  for e in rn.get("ve_agentes") or []]
            proy.pop("RADIOGRAFIA", None); rv2 = dict(rv); rv2.pop("RADIOGRAFIA", None)
            if json.dumps(proy, sort_keys=True) != json.dumps(rv2, sort_keys=True):
                ok_schema = False
        # P2: los proyectiles del guion, verbatim y con autor correcto
        for o, rn in zip(g, recs_n):
            esperado = (o.get("visible") or {}).get("projectiles", [])
            if rn.get("ve_proyectiles") != esperado:
                ok_p2 = False
            for pr in rn.get("ve_proyectiles") or []:
                if pr.get("shooter") != 15:
                    ok_p2 = False
    check("determinismo 3/3 (misma firma de decisiones)", len(firmas) == 1,
          f"{len(firmas)} firma(s)")
    check("el rec nuevo proyectado al esquema viejo == rec viejo (solo ANADE)",
          ok_schema, "")
    check("P2: ve_proyectiles verbatim, con `shooter` correcto (15)", ok_p2, "")

    # ── B. la fisica, certificada + la aritmetica del cruce ───────────────
    print("\n=== B. LA FISICA DE LA INTERCEPTACION (sim.nim, con lineas) ===")
    print("  CERTIFICADO 963-996: el proyectil avanza 2 casillas/tic y golpea")
    print("  al PRIMER agente en su linea que no sea el tirador (esquiva 2*ATH,")
    print("  980; si esquiva, ATRAVIESA y sigue). No lleva blanco. Un cuerpo")
    print("  interpuesto SE LLEVA EL GOLPE — la interposicion es fisica real.")
    print("  Muro -> muere (blocksSight); fin de alcance -> objeto cogible.")
    print("  La victima recibe damage_taken con source = SHOOTER (applyDamage).")

    print("\n  el catalogo a distancia (del player_config, no cableado):")
    print(f"  {'arma':<10} {'kind':<10} {'dano':>5} {'alcance':>8} {'cadencia':>9}")
    a_dist = []
    for iid, it in sorted(mundo.items.items()):
        if it.kind in ("ikRanged", "ikThrown"):
            a_dist.append(it)
            print(f"  {iid:<10} {it.kind:<10} {it.damage:>5} {it.rng if hasattr(it,'rng') else it.range:>8} "
                  f"{it.cooldown:>9}")
    check("hay armas a distancia en el catalogo", len(a_dist) >= 2,
          f"({len(a_dist)})")
    print("  (cadencia del arco: 18 - ATH div 2 -> con ATH 6 del tirador tipico,"
          " 15 tics; sim.nim:871)")

    print("\n  LA ARITMETICA DEL CRUCE (v19: enfriamiento 11; proyectil 2 cas/tic)")
    print("  latencia nuestra: vemos el disparo en la obs del tic T; nuestra")
    print("  orden resuelve en T+1. Casilla k-esima disponible en T+1+(k-1)*11.")
    alcances = sorted({(it.range if hasattr(it, "range") else it.rng)
                       for it in a_dist})
    print(f"\n  {'distancia del disparo':>22} {'vuelo (tics)':>13} "
          f"{'casillas nuestras a tiempo (v19)':>33} {'(SPD 10)':>9}")
    for D in sorted(set([4, 6, 8, 10, 12] + list(alcances))):
        vuelo = math.ceil(D / 2)
        k19 = 0
        while 1 + k19 * 11 <= vuelo - 1:
            k19 += 1
        k10 = 0
        while 1 + k10 * 6 <= vuelo - 1:
            k10 += 1
        print(f"  {D:>22} {vuelo:>13} {k19:>33} {k10:>9}")
    print("\n  -> con las piernas de la v19, la interposicion solo alcanza la")
    print("     LINEA ADYACENTE (1 casilla), y solo si el disparo nace a >= 4")
    print("     casillas. La segunda casilla exige un vuelo de 12+ tics = un")
    print("     disparo de 24+ casillas: NO EXISTE en el catalogo.")
    maxr = max(alcances) if alcances else 0
    check("ningun arma alcanza las 24 casillas del segundo paso v19",
          maxr < 24, f"alcance maximo del catalogo: {maxr}")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
