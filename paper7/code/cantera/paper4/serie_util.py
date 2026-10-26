"""PAPER CUATRO · SERIES — utilidades comunes del forense. [13-sep-2026]

Arnes validado en S-1: v40_exp (interruptores por variable, aqui se fijan a
mano), catalogo REAL y MAPA DE CADA EPISODIO leidos de su propio diario,
attack_ready_in tomado del propio diario (esta grabado), Bloqueos alimentado
cada tic. Sobre `serie_base` dio acuerdo 99,91 % y verificados 98,18 %.
"""
from __future__ import annotations

import ast
import copy
import glob
import json
import os
import sys

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
sys.path.insert(0, RAIZ)
sys.path.insert(0, AQUI)
import decide_otra_vez as DOV                             # noqa: E402
from alma import smoke_alma as SM                         # noqa: E402
from alma.mundo import Mundo                              # noqa: E402
from alma import decisor_zs as D                          # noqa: E402
from alma import appraisal_zs as V37                      # noqa: E402
from alma import appraisal_zs_v40_exp as V40              # noqa: E402

LEY = {".": "ground", "#": "wall", "R": "rock", "F": "fortress_wall",
       "P": "pedestal", "B": "berry_bush"}
TOL = 1e-4
MEMP = json.load(open(os.path.join(AQUI, "memoria_aprendida_p95.json")))
PREV = {w: {"E": v["E"], "R": v["R"]} for w, v in MEMP["completa"].items()
        if v.get("R") is not None}
N_MEM = {w: v.get("n", 0) for w, v in MEMP["completa"].items()}


def lee(path):
    """pareja.lee tolerante: salta lineas rotas (1 en toda la serie)."""
    s = open(path, encoding="utf-8", errors="replace").read()
    if s.startswith(("b'", 'b"')):
        out = []
        for ln in s.splitlines():
            if not ln.startswith(("b'", 'b"')):
                continue
            try:
                out.append(ast.literal_eval(ln).decode("utf-8", "replace"))
            except Exception:
                pass
        s = "\n".join(out)
    for ln in s.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            yield json.loads(ln)
        except Exception:
            pass


def mundo_de(pc, filas, items):
    cfg = SM.player_config(slot=pc["slot"])
    cfg["items"] = list(items)
    cfg["arena"] = {"size": 48, "static_map": list(filas), "legend": dict(LEY),
                    "pedestals": [[x, y] for y, f in enumerate(filas)
                                  for x, ch in enumerate(f) if ch == "P"]}
    for k in ("slot", "team", "teammate_slot", "tick_rate", "max_ticks",
              "ignition_tick", "zone_schedule"):
        if pc.get(k) is not None:
            cfg[k] = pc[k]
    return Mundo.desde_player_config(cfg)


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def amenazas(r, herm, prev=PREV):
    """Las de la FORMA 2: alineadas, dentro de R, hp < 2E."""
    pos, hp = r.get("pos"), r.get("hp")
    out = []
    if not pos or hp is None:
        return out
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
            continue
        if hp < 2.0 * m["E"]:
            out.append({"slot": sl, "arma": w, "E": m["E"], "R": m["R"],
                        "dist": max(abs(dx), abs(dy)),
                        "u": max(0.0, min(1.0, (2 * m["E"] - hp) / m["E"]))})
    return out


def diarios(tanda):
    """(eid, slot, recs, pc, filas, items) de cada diario CON cabecera."""
    base = os.path.join(RAIZ, "paintball", "runs", tanda)
    for eid in sorted(os.path.basename(p) for p in glob.glob(f"{base}/ereq_*")):
        for s in (10, 11):
            fs = glob.glob(f"{base}/{eid}/a{s}/*.log")
            if not fs:
                continue
            recs = list(lee(sorted(fs)[0]))
            pc = next((r for r in recs if r.get("k") == "player_config"), None)
            sm = next((r for r in recs if r.get("k") == "static_map"), None)
            cat = next((r for r in recs if r.get("k") == "catalogo"), None)
            if pc is None or sm is None or cat is None:
                continue
            yield eid, s, recs, pc, list(sm["filas"]), cat["items"]


def pon(miedo, mem=None):
    V40.MIEDO_ON = bool(miedo)
    V40.VIDA_AJENA_ON = False
    V40.MEMORIA_APRENDIDA = (mem if mem is not None else (PREV if miedo else {}))


def recorre(tanda, miedo_arnes):
    """Genera (ctx, det, verificado) por cada tic live de cada diario usable.

    `det` es la decision del arnes con la fila como `miedo_arnes` indique.
    `verificado` compara la d de TODOS los candidatos contra el diario.
    """
    for eid, s, recs, pc, filas, items in diarios(tanda):
        mundo = mundo_de(pc, filas, items)
        mem = V40.Memoria()
        blo = D.Bloqueos()
        ult = None
        herm = pc.get("teammate_slot")
        tk = [r for r in recs if r.get("k") == "tick"]
        for r in tk:
            t = r["tick"]
            o = DOV.a_obs(r)
            o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
            mem.observa(o, mundo, t)
            blo.actualiza(o, mundo, ult, t)
            ult = r.get("intencion")
            if r.get("phase") != "live":
                continue
            # [v4d] EL ORDEN DEL CAMPO, con las escrituras tomadas del DIARIO.
            # `pre` es la memoria tal como esta AL ENTRAR en el tic: es la que
            # ven los candidatos, porque `decide` los valora ANTES de su
            # epilogo. Justo despues se aplican sobre la memoria VIVA las dos
            # escrituras de decisor_zs.py:903-908, pero con la accion REAL del
            # diario, no con la que elija el arnes; y la foto del presente
            # (policy_serie.py:138) usa ya esa memoria viva.
            pre = copy.deepcopy(mem)
            _in = (r.get("intencion") or {}).get("do")
            _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
            if _in == "attack" or _el.startswith("atacar"):
                mem.ultimo_ataque = t                      # decisor_zs.py:908
            elif _el.startswith("soltar_"):                # decisor_zs.py:904
                mem.cedidos[tuple(r.get("pos") or ())] = {
                    "item": {"id": _el[len("soltar_"):], "n": 1}, "tick": t}
            yield {"eid": eid, "slot": s, "tick": t, "r": r, "herm": herm,
                   "mundo": mundo, "mem": pre, "mem_post": mem,
                   "blo": blo, "o": o}, None, None
            # [ARREGLO v4b] `decide` escribe en `mem` DESPUES de elegir
            # (decisor_zs.py:903-908) y el arnes le pasa una copia, asi que esas
            # dos escrituras se perdian. Se replican aqui desde el diario, con
            # la accion que el agente REALMENTE eligio:
            #   903-904  if receta["tipo"] == "soltar": mem.cedidos[pos] = {...}
            #   905-908  elif receta["tipo"] == "atacar": mem.ultimo_ataque = tick
            # `ultimo_ataque` alimenta `delatado` en S-8-EXPOSICION
            # (appraisal_zs.py:1309-1310): sin el, un agente CAMUFLADO que acaba
            # de atacar se cree invisible y la fila sale 0.24 en vez de 0.30.



def decide_con(ctx, miedo, mem=None, viva=False, como_el_campo=True):
    """`viva=True` = el orden del CAMPO: se pasa la memoria VIVA, como
    `policy.py:105`, para que el epilogo del decisor (decisor_zs.py:903-908)
    escriba donde debe. `viva=False` da una copia, para comparar versiones."""
    pon(miedo, mem)
    # [v4d] EL CABLEADO DEL CAMPO. `policy_serie.py` NO asigna `D.A`; el decisor
    # usa su propia importacion (decisor_zs.py:39 -> appraisal_zs, o sea v37) en
    # la linea 882, que es la que valora los CANDIDATOS. v40 solo entra en la
    # foto del presente (policy_serie.py:138). Con `como_el_campo=True` se
    # reproduce eso; con False se fuerza v40 tambien en los candidatos, que es
    # lo que HABRIA pasado si la fila estuviera cableada a la decision.
    D.A = V37 if como_el_campo else V40
    m = ctx["mem"] if viva else copy.deepcopy(ctx["mem"])   # v4d: ctx["mem"] = `pre`
    b = ctx["blo"] if viva else copy.deepcopy(ctx["blo"])
    _a, det = D.decide(ctx["o"], ctx["mundo"], m, ctx["tick"], b)
    D.A = V37
    return det


def ds(det):
    return {k: (v["d"] if isinstance(v, dict) else v)
            for k, v in det["candidatos"].items()}


def verificado(ctx, det):
    R = ctx["r"].get("RADIOGRAFIA") or {}
    dia = {k: (v["d"] if isinstance(v, dict) else v)
           for k, v in (R.get("candidatos") or {}).items()}
    rec = ds(det)
    return (set(dia) == set(rec)
            and all(abs(dia[k] - rec[k]) <= TOL for k in dia))


def clase(nombre, ctx, det=None):
    r = ctx["r"]
    mri = r.get("move_ready_in") or 0
    if nombre.startswith("atacar_"):
        return "golpe"
    if nombre.split("_")[0] in ("usar", "empunar", "ponerse"):
        return "curarse"
    if nombre.startswith("soltar"):
        return "soltar"
    if nombre.startswith("coger"):
        return "coger"
    if nombre == "ir_pareja":
        return "ir_pareja"
    if nombre == "noop":
        return ("noop con movimiento vetado" if mri > 0
                else "noop con movimiento disponible")
    if nombre.startswith(("move_", "paso_", "ir_")):
        return "apartarse"
    return f"otra ({nombre.split('_')[0]})"
