"""Humo del alma SIN mundo: construye un player_config y observaciones
sinteticas fieles al contrato de zero-sum 0.1.18 y ejercita
Mundo -> appraisal (tabla) -> candidatos -> motor -> desempate.

Sirve para depurar sin gastar episodios y para medir la cadencia de decision.
Uso (desde la raiz del repo):  PYTHONPATH=paintball python3 -m alma.smoke_alma
"""
from __future__ import annotations

import json
import statistics
import sys
import time

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from motor.model import DEFAULT_CONFIG, opponent_distance

N = 48
LEGEND = {".": "ground", "#": "wall", "R": "rock", "F": "fortress_wall",
          "P": "pedestal", "B": "berry_bush"}
PEDESTALS = [[40, 24], [39, 30], [35, 35], [30, 39], [24, 40], [18, 39],
             [13, 35], [9, 30], [8, 24], [9, 18], [13, 13], [18, 9],
             [24, 8], [30, 9], [35, 13], [39, 18]]
BUSHES = [[44, 21], [42, 26], [6, 24], [24, 44]]


def construye_mapa():
    g = [["." for _ in range(N)] for _ in range(N)]
    for i in range(N):
        g[0][i] = g[N - 1][i] = "#"
        g[i][0] = g[i][N - 1] = "#"
    # Fortaleza 9x9 centrada en (24,24): anillo 20..28
    for x in range(20, 29):
        for y in (20, 28):
            g[y][x] = "F"
    for y in range(20, 29):
        for x in (20, 28):
            g[y][x] = "F"
    # cuatro bocas de 2 casillas (norte, sur, este, oeste)
    for x in (23, 24):
        g[20][x] = "."; g[28][x] = "."
    for y in (23, 24):
        g[y][20] = "."; g[y][28] = "."
    for (x, y) in PEDESTALS:
        g[y][x] = "P"
    for (x, y) in BUSHES:
        g[y][x] = "B"
    g[30][30] = "R"; g[31][30] = "R"
    return ["".join(f) for f in g]


def player_config(slot=0):
    return {
        "type": "player_config", "protocol": "zero_sum.player.v1",
        "slot": slot, "team": "A", "teammate_slot": 1, "name": f"P{slot:02d}",
        "arena": {"size": N, "static_map": construye_mapa(), "legend": LEGEND,
                  "pedestals": PEDESTALS},
        "freeze": {"ends_tick": 48, "alloc_deadline_tick": 24,
                   "pedestal_mine_rule": "…"},
        "stats": {"budget": 20, "min": 1, "max": 10, "default": [5, 5, 5, 5]},
        "items": [
            {"id": "sword", "kind": "ikMelee", "damage": 18, "range": 1,
             "cooldown": 18, "durability": 40, "stack_max": 1, "use_ticks": 0, "heal": 0},
            {"id": "spear", "kind": "ikMelee", "damage": 12, "range": 2,
             "cooldown": 20, "durability": 40, "stack_max": 1, "use_ticks": 0, "heal": 0},
            {"id": "bow", "kind": "ikRanged", "damage": 14, "range": 8,
             "cooldown": 18, "durability": 0, "stack_max": 1, "use_ticks": 0, "heal": 0},
            {"id": "knives", "kind": "ikThrown", "damage": 8, "range": 5,
             "cooldown": 10, "durability": 0, "stack_max": 8, "use_ticks": 0, "heal": 0},
            {"id": "net", "kind": "ikThrown", "damage": 0, "range": 3,
             "cooldown": 30, "durability": 0, "stack_max": 2, "use_ticks": 0, "heal": 0},
            {"id": "first_aid", "kind": "ikConsumable", "damage": 0, "range": 0,
             "cooldown": 0, "durability": 0, "stack_max": 2, "use_ticks": 48, "heal": 50},
            {"id": "rations", "kind": "ikConsumable", "damage": 0, "range": 0,
             "cooldown": 0, "durability": 0, "stack_max": 5, "use_ticks": 24, "heal": 15},
            {"id": "backpack", "kind": "ikGear", "damage": 0, "range": 0,
             "cooldown": 0, "durability": 0, "stack_max": 1, "use_ticks": 0, "heal": 0},
            {"id": "camouflage", "kind": "ikGear", "damage": 0, "range": 0,
             "cooldown": 0, "durability": 0, "stack_max": 1, "use_ticks": 0, "heal": 0},
            {"id": "arrows", "kind": "ikAmmo", "damage": 0, "range": 0,
             "cooldown": 0, "durability": 0, "stack_max": 12, "use_ticks": 0, "heal": 0},
        ],
        "zone_schedule": [[96, 120, 288, 24, 12, 4], [336, 360, 384, 12, 0, 40]],
        "tick_rate": 24, "max_ticks": 480, "ignition_tick": 48,
    }


def obs(tick, pos, hp=100, pack=None, hand=None, body=None, agentes=(),
        items=(), bushes=(), efectos=(), chat=(), eventos=(), zona=None):
    return {"type": "observation", "tick": tick, "phase": "live",
            "you": {"pos": list(pos), "hp": hp,
                    "stats": {"speed": 5, "strength": 1, "intelligence": 8,
                              "athleticism": 6},
                    "hand": hand, "body": body, "pack": list(pack or [None, None]),
                    "effects": list(efectos), "damage_taken": [], "kills": 0,
                    "damage_dealt": 0, "move_ready_in": 0, "attack_ready_in": 0,
                    "action_result": "ok"},
            "visible": {"agents": list(agentes), "items": list(items),
                        "pods": [], "bushes": list(bushes), "projectiles": []},
            "zone": zona or {"center": [24, 24], "radius": 24, "next_radius": 12,
                             "damage_per_s": 0},
            "events": list(eventos), "chat": list(chat)}


def escena(nombre, mundo, mem, o, tick):
    mem.observa(o, mundo, tick)
    st, radio = A.appraise(o, mundo, mem, tick)
    d = opponent_distance(st, DEFAULT_CONFIG)
    t0 = time.perf_counter()
    accion, det = D.decide(o, mundo, mem, tick)
    ms = (time.perf_counter() - t0) * 1000
    print(f"\n=== {nombre} ===  tick {tick} pos {o['you']['pos']} hp {o['you']['hp']}")
    print("  filas con M>0:", {k: v["M"] for k, v in radio["filas"].items() if v["M"]})
    print("  W:", round(radio["W"], 3), radio["W_desglose"], " B:", round(radio["B"], 3))
    print("  fuerzas State:", radio["fuerzas_state"], " d =", round(d, 5))
    orden = sorted(det["candidatos"].items(), key=lambda kv: kv[1]["d"])
    print("  mejores candidatos:", [(k, v["d"]) for k, v in orden[:4]])
    print("  ELIGE:", det["elegido"], "->", accion, f" ({ms:.2f} ms, "
          f"{len(det['candidatos'])} candidatos)")
    return ms


def main():
    cfg = player_config()
    mundo = Mundo.desde_player_config(cfg)
    print("== MUNDO LEIDO ==")
    for a in mundo.avisos:
        print("  ", a)
    print("   botiquin:", mundo.id_botiquin, "| raciones:", mundo.id_raciones,
          "| mochila:", mundo.id_mochila, "| camuflaje:", mundo.id_camuflaje,
          "| red:", mundo.id_red)
    print("   dmg_ref:", mundo.dmg_ref, "| ammo:", mundo.ammo_ids)
    print("   camara:", len(mundo.camara), "celdas | bocas:", sorted(mundo.bocas))
    print("   anillo en t=0/200/400:", [mundo.anillo_en(t) for t in (0, 200, 400)])

    tiempos = []
    mem = A.Memoria()
    # 1. tranquilo en el pedestal, sano, nada a la vista
    tiempos.append(escena("tranquilo, sano, pedestal", mundo, mem,
                          obs(60, (40, 24), bushes=[{"pos": [42, 26], "charges": 1}]), 60))
    # 2. el anillo va a encoger y estamos fuera
    mem2 = A.Memoria()
    tiempos.append(escena("anillo encogiendo, estamos fuera", mundo, mem2,
                          obs(300, (40, 24), hp=100,
                              zona={"center": [24, 24], "radius": 12,
                                    "next_radius": 0, "damage_per_s": 40}), 300))
    # 3. herido con botiquin en el zurron
    mem3 = A.Memoria(); mem3.hp_max = 100
    tiempos.append(escena("herido con botiquin", mundo, mem3,
                          obs(200, (30, 24), hp=35,
                              pack=[{"id": "first_aid", "n": 1}, None]), 200))
    # 4. objeto en la casilla
    mem4 = A.Memoria(); mem4.hp_max = 100
    tiempos.append(escena("objeto bajo los pies", mundo, mem4,
                          obs(150, (33, 24),
                              items=[{"id": "sword", "n": 1, "pos": [33, 24]}]), 150))
    # 5. hostiles cerca + arma en mano
    mem5 = A.Memoria(); mem5.hp_max = 100
    tiempos.append(escena("hostiles cerca, espada en mano", mundo, mem5,
                          obs(220, (30, 24), hand={"id": "sword", "durability": 40},
                              agentes=[{"slot": 7, "team": "D", "pos": [31, 24],
                                        "hp_band": "healthy"},
                                       {"slot": 9, "team": "E", "pos": [33, 26],
                                        "hp_band": "hurt"}]), 220))
    # 6. la pareja a la vista (roce sube)
    mem6 = A.Memoria(); mem6.hp_max = 100
    for t in range(100, 400, 12):
        mem6.observa(obs(t, (30, 24), agentes=[{"slot": 1, "team": "A",
                                                "pos": [32, 25], "hp_band": "healthy"}]),
                     mundo, t)
    tiempos.append(escena("con la pareja a la vista (B alto)", mundo, mem6,
                          obs(400, (30, 24), agentes=[{"slot": 1, "team": "A",
                                                       "pos": [32, 25],
                                                       "hp_band": "hurt"}]), 400))
    # 7. sin compania mucho rato
    mem7 = A.Memoria(); mem7.hp_max = 100; mem7.ticks_sin_compania = 24 * 40
    tiempos.append(escena("solo hace rato", mundo, mem7, obs(400, (30, 24)), 400))

    print("\n== CADENCIA DE DECISION (humo, nativo arm64) ==")
    print(f"   n={len(tiempos)} mediana={statistics.median(tiempos):.2f} ms "
          f"max={max(tiempos):.2f} ms   (objetivo <= 400 ms)")


if __name__ == "__main__":
    sys.exit(main())
