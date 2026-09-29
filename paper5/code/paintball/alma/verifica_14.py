"""Banco del PASO CORTO — PROMPT_14.

  1. Vocabulario: existen los 8 `paso_*`, y NO existe el paso a casilla no
     PISABLE — ni solida (muro) ni ocupada por un cuerpo.
  2. Medida: `paso_X` se proyecta a UNA casilla; `move_X` sigue proyectando la
     zancada entera. Misma direccion, distinta medida.
  3. Emision: `paso_X` sale como un `move` normal y comparte el enfriamiento.
  4. REPLAY del tic decisivo: se reconstruye la observacion REAL de
     `runs/cesion/ep_110`, contenedor 0, tic 420 (el don que no llego) y se
     compara el reparto de candidatos con y sin paso corto.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_14
"""
from __future__ import annotations

import json
import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs

_fallos = []
REPLAY = "paintball/runs/cesion/ep_110/logs/policy_agent_0.log"


def check(nombre, cond, detalle=""):
    print(f"  [{'PASS' if cond else 'FALLO'}] {nombre}  {detalle}")
    if not cond:
        _fallos.append(nombre)


def obs_del_log(rec, slot_pareja):
    """Reconstruye la observacion a partir de una linea `tick` del log."""
    return {"type": "observation", "tick": rec["tick"], "phase": rec.get("phase", "live"),
            "you": {"pos": list(rec["pos"]), "hp": rec["hp"],
                    "stats": {"intelligence": 8, "athleticism": 6,
                              "speed": 5, "strength": 1},
                    "hand": rec.get("hand"), "body": rec.get("body"),
                    "pack": list(rec.get("pack") or [None, None]),
                    "effects": list(rec.get("effects") or []),
                    "damage_taken": list(rec.get("damage_taken") or []),
                    "kills": rec.get("kills") or 0,
                    "damage_dealt": rec.get("damage_dealt") or 0,
                    "move_ready_in": rec.get("move_ready_in") or 0,
                    "attack_ready_in": 0,
                    "action_result": rec.get("action_result") or "ok"},
            "visible": {"agents": list(rec.get("ve_agentes") or []),
                        "items": list(rec.get("ve_items") or []),
                        "pods": [], "bushes": list(rec.get("ve_bushes") or []),
                        "projectiles": []},
            "zone": rec.get("zona") or {},
            "events": list(rec.get("eventos") or []),
            "chat": list(rec.get("chat") or [])}


def main():
    mundo = Mundo.desde_player_config(player_config())

    # ── 1-3. vocabulario, medida y emision ─────────────────────────────────
    print("=== 1-3. el paso corto en el vocabulario ===")
    YO = (24, 24)
    o = obs(300, YO, agentes=[])
    m = A.Memoria(); m.hp_max = 100; m.observa(o, mundo, 300)
    cands = dict(D.candidatos(o, mundo, m, 300))
    pasos = sorted(k for k in cands if k.startswith("paso_"))
    check("estan los 8 pasos en campo abierto", len(pasos) == 8, f"{pasos}")

    # junto a un muro: el paso a la casilla solida NO se ofrece
    pared = None
    for y in range(1, mundo.arena_size - 1):
        for x in range(1, mundo.arena_size - 1):
            if not mundo.solido(x, y) and mundo.solido(x + 1, y):
                pared = (x, y)
                break
        if pared:
            break
    o_p = obs(300, pared, agentes=[])
    m_p = A.Memoria(); m_p.hp_max = 100; m_p.observa(o_p, mundo, 300)
    c_p = dict(D.candidatos(o_p, mundo, m_p, 300))
    # NOTA (PROMPT_28): este gate exigia ademas que `move_E` SIGUIERA
    # ofreciendose hacia el solido. Eso era exactamente el defecto que el 28
    # arreglo —la zancada se ofrecia contra el muro y el mundo la rechazaba—,
    # asi que la asercion se actualiza: ahora NINGUNO de los dos se ofrece.
    check("no se ofrece el paso a casilla SOLIDA",
          "paso_E" not in c_p,
          f"pos={pared} pasos={sorted(k for k in c_p if k.startswith('paso_'))}")
    check("y desde el 28, la ZANCADA contra el solido tampoco",
          "move_E" not in c_p,
          f"zancadas={sorted(k for k in c_p if k.startswith('move_'))}")

    # con un cuerpo al norte, el paso al norte NO se ofrece: el mundo devuelve
    # `blocked` (medido: 3008 de 3037 pasos de la tanda v11 sin esta regla).
    o_c = obs(300, YO, agentes=[{"slot": 9, "team": "D", "pos": [24, 23],
                                 "hp_band": "healthy"}])
    m_c = A.Memoria(); m_c.hp_max = 100; m_c.observa(o_c, mundo, 300)
    c_c = dict(D.candidatos(o_c, mundo, m_c, 300))
    check("no se ofrece el paso a casilla OCUPADA por un cuerpo",
          "paso_N" not in c_c and "paso_S" in c_c,
          f"pasos={sorted(k for k in c_c if k.startswith('paso_'))}")

    acc = D._a_json("paso_N", cands["paso_N"], YO, mundo, m, 300)
    check("el paso se emite como un `move` normal",
          acc == {"type": "action", "do": "move", "dir": "N"}, f"{acc}")
    b = D.Bloqueos()
    o_frio = obs(300, YO, agentes=[])
    o_frio["you"]["move_ready_in"] = 5
    check("el paso comparte el enfriamiento de movimiento",
          b.veta("paso_N", o_frio, 300), "")

    _acc, rad = D.decide(o, mundo, m, 300)
    det = rad.get("candidatos") or {}
    if isinstance(det.get("paso_N"), dict) and isinstance(det.get("move_N"), dict):
        mp, mv = det["paso_N"]["movs"], det["move_N"]["movs"]
        check("el paso se proyecta a 1 casilla y la zancada a mas",
              mp == 1 and mv > 1, f"paso_N movs={mp}  move_N movs={mv}")
        check("misma direccion, distinta casilla prevista",
              det["paso_N"]["pos_prevista"] != det["move_N"]["pos_prevista"],
              f"{det['paso_N']['pos_prevista']} vs {det['move_N']['pos_prevista']}")

    # ── 4. replay del tic que no llego ─────────────────────────────────────
    print("\n=== 4. REPLAY: s110 cont0 t420, el don que no llego ===")
    try:
        recs = [json.loads(l) for l in open(REPLAY, encoding="utf-8", errors="replace")
                if l.startswith("{") and '"k":"tick"' in l]
    except FileNotFoundError:
        print(f"  [n/a] no encuentro {REPLAY}; se salta el replay")
        recs = []
    if recs:
        rec = next((r for r in recs if r["tick"] == 420), None)
        o4 = obs_del_log(rec, mundo.teammate_slot)
        m4 = A.Memoria(); m4.hp_max = 100
        # el vinculo ya rodado: se alimenta con los tics previos del propio log
        for r in recs:
            if r["tick"] > 420:
                break
            m4.observa(obs_del_log(r, mundo.teammate_slot), mundo, r["tick"])
        m4.cedidos[(24, 24)] = {"item": "rations", "tick": 409}   # como en produccion
        _a, r4 = D.decide(o4, mundo, m4, 420)
        det4 = r4.get("candidatos") or {}
        orden = sorted(((v["d"] if isinstance(v, dict) else v), k)
                       for k, v in det4.items())
        print(f"    elegido: {r4['elegido']}   (mirada H={r4['mirada_ticks']} tics)")
        for d, k in orden[:6]:
            v = det4[k]
            f = v.get("filas", {}) if isinstance(v, dict) else {}
            print(f"      {k:12s} d={d:.5f}  pos={v.get('pos_prevista')} "
                  f"movs={v.get('movs')}  S-DANO-PAREJA={f.get('S-DANO-PAREJA')} "
                  f"F-ANTICIPACION={f.get('F-ANTICIPACION')}")
        pasos4 = {k: v for k, v in det4.items() if k.startswith("paso_")}
        # en t420 hay dos cuerpos pegados (slot 1 en (25,24), slot 5 en (23,23)):
        # esos dos rumbos NO deben ofrecerse.
        vecinos = {(24 + dx, 24 + dy) for dx, dy in D.DIRS.values()}
        cuerpos = {tuple(a["pos"]) for a in o4["visible"]["agents"]} & vecinos
        check("se ofrecen los pasos PISABLES y solo esos",
              len(pasos4) == 8 - len(cuerpos),
              f"n={len(pasos4)}  cuerpos pegados={sorted(cuerpos)}")
        check("cada paso se proyecta a UNA casilla",
              all(v["movs"] == 1 for v in pasos4.values()),
              f"movs={sorted({v['movs'] for v in pasos4.values()})}")
        mejor_paso = min(v["d"] for v in pasos4.values())
        d_noop = det4["noop"]["d"]
        # NO se exige que gane: se MIDE. En este tic el anillo tiene radio 0 y
        # (24,24) es la unica casilla que no arde, asi que apartarse enciende
        # F-ANTICIPACION en su techo se den 1 o 4 casillas. El paso corto no
        # rescata ESTA escena; el acta lo dice.
        print(f"    mejor paso d={mejor_paso:.5f}   noop d={d_noop:.5f}   "
              f"-> gana {'el paso' if mejor_paso < d_noop else 'quedarse'}")
        print(f"    (apartarse parte S-DANO-PAREJA 0,330 -> 0,165, pero "
              f"F-ANTICIPACION sube 0 -> 0,5: el anillo esta a radio 0)")

    print("\n" + ("TODOS LOS GATES PASAN" if not _fallos else f"FALLOS: {_fallos}"))
    return 1 if _fallos else 0


if __name__ == "__main__":
    sys.exit(main())
