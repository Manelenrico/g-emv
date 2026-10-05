"""PAPER CUATRO · PASO 2 · B3/B5/B6 — v37 y v38_exp deciden sobre escenas grabadas.

No juega nada: reconstruye el estado del agente en tics YA OCURRIDOS y hace
decidir a las dos versiones sobre el MISMO estado.

FIDELIDAD (B6). El diario NO guarda ni el mapa ni el catálogo de objetos: el
`player_config` que registra `policy.py:223` es un resumen (slot, team,
teammate_slot, tick_rate, max_ticks, ignition_tick, zone_schedule). El mapa y el
catálogo se toman de `alma/smoke_alma.py`, que es el constructor que el propio
proyecto usa para decidir sin mundo, con la arena real y la tabla de armas
certificada; se le añaden `blowgun` y `darts`, que le faltaban, con los números
de `paintball/hecho_dano_armas.md`. Lo real del diario (slot, equipo, hermano,
calendario del anillo, cadencia) se inyecta encima.

Un diario TRUNCADO por la cabeza no tiene `arranque`/`player_config` y su
memoria de episodio no se puede reconstruir (empezaría a mitad de partida sin
historia). Esos tics se cuentan aparte y NO entran en las cifras.

Uso:  python3 cantera/paper4/decide_otra_vez.py
"""
from __future__ import annotations

import copy
import json
import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
sys.path.insert(0, RAIZ)
sys.path.insert(0, AQUI)
import regla_en_seco as RE                                # noqa: E402
from alma import smoke_alma as SM                         # noqa: E402
from alma.mundo import Mundo                              # noqa: E402
from alma import decisor_zs as D                          # noqa: E402
from alma import appraisal_zs as V37                      # noqa: E402
from alma import appraisal_zs_v38_exp as V38              # noqa: E402

EXTRA = [
    {"id": "blowgun", "kind": "ikRanged", "damage": 4, "range": 6, "cooldown": 20,
     "durability": 0, "stack_max": 1, "use_ticks": 0, "heal": 0},
    {"id": "darts", "kind": "ikAmmo", "damage": 0, "range": 0, "cooldown": 0,
     "durability": 0, "stack_max": 8, "use_ticks": 0, "heal": 0},
]
CONST = {"intelligence": 8, "athleticism": 6, "speed": 5, "strength": 1}


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def monta_mundo(pc):
    cfg = SM.player_config(slot=pc["slot"])
    cfg["items"] = cfg["items"] + EXTRA
    for k in ("slot", "team", "teammate_slot", "tick_rate", "max_ticks",
              "ignition_tick", "zone_schedule"):
        if pc.get(k) is not None:
            cfg[k] = pc[k]
    return Mundo.desde_player_config(cfg)


def a_obs(r):
    """Registro de tic -> observación con la forma del contrato del mundo."""
    return {"type": "observation", "tick": r["tick"], "phase": r.get("phase"),
            "you": {"pos": list(r.get("pos") or [0, 0]), "hp": r.get("hp") or 0,
                    "stats": dict(CONST), "hand": r.get("hand"),
                    "body": r.get("body"), "pack": list(r.get("pack") or [None, None]),
                    "effects": list(r.get("effects") or []),
                    "damage_taken": list(r.get("damage_taken") or []),
                    "kills": r.get("kills") or 0,
                    "damage_dealt": r.get("damage_dealt") or 0,
                    "move_ready_in": r.get("move_ready_in") or 0,
                    "attack_ready_in": 0,          # NO está en el diario (B6)
                    "action_result": r.get("action_result")},
            "visible": {"agents": list(r.get("ve_agentes") or []),
                        "items": list(r.get("ve_items") or []),
                        "pods": [], "bushes": list(r.get("ve_bushes") or []),
                        "projectiles": list(r.get("ve_proyectiles") or [])},
            "zone": r.get("zona") or {},
            "events": list(r.get("eventos") or []), "chat": list(r.get("chat") or [])}


def clase(nombre, pos, obs_prev, amenazas):
    if nombre.startswith("atacar"):
        return "golpe"
    if nombre.split("_")[0] in ("usar", "empunar", "ponerse"):
        return "curarse/usar"
    if nombre.startswith("soltar"):
        return "soltar"
    if nombre.startswith("coger"):
        return "coger"
    if nombre == "noop":
        return "quedarse"
    q = obs_prev
    if q and tuple(q) != tuple(pos):
        a0 = min((cheb(pos, x) for x in amenazas), default=99)
        a1 = min((cheb(q, x) for x in amenazas), default=99)
        return "ganar distancia" if a1 > a0 else "acercarse/otra"
    return "otra"


def main():
    MEM = json.load(open(os.path.join(AQUI, "memoria_aprendida_p95.json")))
    orden = RE.orden_de_juego()
    C = defaultdict(int)
    clases = defaultdict(int)
    cura = defaultdict(int)
    escenas = []

    for ji, eid in orden:
        prev = MEM["antes_de"][str(ji)]
        if not prev:
            continue                              # partida 0: memoria vacía
        for s in RE.SLOTS:
            recs = RE.diario(eid, s)
            if not recs:
                continue
            pc = next((r for r in recs if r.get("k") == "player_config"), None)
            tk = [r for r in recs if r.get("k") == "tick"]
            if pc is None or not any(r.get("k") == "arranque" for r in recs):
                C["tics_en_diarios_truncados"] += sum(
                    1 for r in tk if r.get("phase") == "live")
                C["diarios_truncados"] += 1
                continue
            C["diarios_usables"] += 1
            mundo = monta_mundo(pc)
            mem = V37.Memoria()
            herm = pc.get("teammate_slot")
            for r in tk:
                o = a_obs(r)
                try:
                    mem.observa(o, mundo, r["tick"])
                except Exception:
                    C["observa_falla"] += 1
                    continue
                if r.get("phase") != "live":
                    continue
                pos, hp = r.get("pos"), r.get("hp")
                if not pos or hp is None:
                    continue
                # ¿enciende la fila con la memoria p95 de las partidas anteriores?
                letales = []
                for a in (r.get("ve_agentes") or []):
                    w = a.get("hand") or "none"
                    sl = a.get("slot")
                    if sl is None or sl == herm or not a.get("pos") or w == "net":
                        continue
                    m = prev.get(w)
                    if not m or m.get("R") is None:
                        continue
                    dx, dy = a["pos"][0] - pos[0], a["pos"][1] - pos[1]
                    if max(abs(dx), abs(dy)) > m["R"]:
                        continue
                    if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
                        C["descartados_por_alineacion"] += 1
                        continue
                    # FORMA 2: la fila vale >0 mientras hp < 2*E (u > 0).
                    if hp < 2.0 * m["E"]:
                        letales.append((a, w, m))
                    if hp <= m["E"]:
                        C["_crit_forma1_hp_le_E"] += 1
                if not letales:
                    continue
                C["tics_encendidos"] += 1
                amenazas = [tuple(a["pos"]) for a, _w, _m in letales]

                # ── decidir dos veces sobre el MISMO estado ──────────────
                D.A = V37
                V38.MEMORIA_APRENDIDA = {}
                m1 = copy.deepcopy(mem)
                try:
                    _a1, det1 = D.decide(o, mundo, m1, r["tick"])
                except Exception:
                    C["decide_falla"] += 1
                    continue
                D.A = V38
                V38.MEMORIA_APRENDIDA = {w: {"E": v["E"], "R": v["R"]}
                                         for w, v in prev.items() if v.get("R") is not None}
                m2 = copy.deepcopy(mem)
                try:
                    _a2, det2 = D.decide(o, mundo, m2, r["tick"])
                except Exception:
                    C["decide_falla"] += 1
                    D.A = V37
                    continue
                D.A = V37
                C["decisiones_evaluadas"] += 1
                e1, e2 = det1["elegido"], det2["elegido"]
                if e1 != e2:
                    C["cambian"] += 1
                    C[f"par::{e1.split('_')[0]}->{e2.split('_')[0]}"] += 1
                    cand2 = det2["candidatos"].get(e2)
                    pv = cand2.get("pos_prevista") if isinstance(cand2, dict) else None
                    cl = clase(e2, tuple(pos), pv, amenazas)
                    clases[cl] += 1
                    if e2.startswith("atacar"):
                        C["nuevas_que_son_golpe"] += 1
                # ¿había futuro de curarse con hp_prevista > E de la amenaza?
                Emax = max(m["E"] for _a, _w, m in letales)
                curas = [k for k, v in det2["candidatos"].items()
                         if k.split("_")[0] in ("usar", "empunar")
                         and isinstance(v, dict)
                         and (v.get("hp_prevista") or 0) > Emax]
                # S2b: curas que dejan hp_prevista >= 2*E (la fila se apaga)
                seguras = [k for k, v in det2["candidatos"].items()
                           if k.split("_")[0] in ("usar", "empunar")
                           and isinstance(v, dict)
                           and (v.get("hp_prevista") or 0) >= 2.0 * Emax]
                if seguras:
                    cura["tics_con_cura_SEGURA"] += 1
                    if e1 in seguras and e2 not in seguras:
                        cura["S2b_cura_segura_PERDIDA"] += 1
                        if e2.startswith(("move_", "paso_", "ir_")):
                            cura["S2b_perdida_por_huir"] += 1
                if curas:
                    cura["tics_con_cura_suficiente"] += 1
                    if e2.split("_")[0] in ("usar", "empunar"):
                        cura["v38_elige_curarse"] += 1
                    elif e2 == "noop":
                        cura["v38_elige_quedarse"] += 1
                    else:
                        cura["v38_elige_otra"] += 1
                    if e1.split("_")[0] in ("usar", "empunar"):
                        cura["v37_elegia_curarse"] += 1
                a0, w0, m0 = max(letales, key=lambda L: L[2]["E"] - hp)
                escenas.append({"margen": m0["E"] - hp, "ji": ji, "eid": eid,
                                "slot": s, "tick": r["tick"], "hp": hp,
                                "quien": a0.get("slot"), "arma": w0,
                                "dist": cheb(tuple(pos), tuple(a0["pos"])),
                                "E": m0["E"], "v37": e1, "v38": e2,
                                "cambia": e1 != e2, "cura": bool(curas)})

    print("=== B6 · FIDELIDAD ===")
    print(f"    diarios usables (cabecera completa):  {C['diarios_usables']}")
    print(f"    diarios truncados, DESCARTADOS:       {C['diarios_truncados']}")
    print(f"    tics live de diarios truncados, fuera de las cifras: "
          f"{C['tics_en_diarios_truncados']}")
    print(f"    fallos de mem.observa: {C['observa_falla']} · de decide: {C['decide_falla']}")
    print(f"    NOTA: `attack_ready_in` no está en el diario; se pone a 0.")

    print("\n=== B3 · DECIDIR OTRA VEZ ===")
    print(f"    tics encendidos FORMA 2 (hp < 2E): {C['tics_encendidos']}")
    print(f"    (amenazas que cumplian el criterio FORMA 1, hp <= E: "
          f"{C['_crit_forma1_hp_le_E']})")
    print(f"    amenazas descartadas por DESALINEACIÓN: {C['descartados_por_alineacion']}")
    print(f"    decisiones evaluadas: {C['decisiones_evaluadas']}")
    print(f"    CAMBIAN: {C['cambian']} "
          f"({100*C['cambian']/max(1,C['decisiones_evaluadas']):.1f} %)")
    print(f"    nuevas que son GOLPE: {C['nuevas_que_son_golpe']}")
    print("    tabla acción v37 -> acción v38_exp:")
    for k, v in sorted(((k, v) for k, v in C.items() if k.startswith("par::")),
                       key=lambda x: -x[1]):
        print(f"      {k[5:]:<24} {v}")
    tot = sum(clases.values())
    for k, v in sorted(clases.items(), key=lambda x: -x[1]):
        print(f"      {k:<18} {v:>5}  ({100*v/max(1,tot):.1f} % de las que cambian)")

    print("\n=== B3b · CUANDO HABÍA CURA SUFICIENTE (hp_prevista > E de la amenaza) ===")
    n = cura["tics_con_cura_suficiente"]
    print(f"    tics con ese futuro disponible: {n}")
    if n:
        for k in ("v38_elige_curarse", "v38_elige_quedarse", "v38_elige_otra",
                  "v37_elegia_curarse"):
            print(f"      {k:<22} {cura[k]:>5}  ({100*cura[k]/n:.1f} %)")
    print(f"\n    S2b · tics con cura que deja hp_prevista >= 2*E: "
          f"{cura['tics_con_cura_SEGURA']}")
    print(f"      v37 la elegia y v38 NO: {cura['S2b_cura_segura_PERDIDA']}"
          f" · de ellas por huir: {cura['S2b_perdida_por_huir']}")

    json.dump({"C": dict(C), "clases": dict(clases), "cura": dict(cura),
               "escenas": escenas}, open(os.path.join(AQUI, "b3_resultado.json"), "w"))
    print(f"\n  escenas -> {os.path.join(AQUI, 'b3_resultado.json')}")


if __name__ == "__main__":
    main()
