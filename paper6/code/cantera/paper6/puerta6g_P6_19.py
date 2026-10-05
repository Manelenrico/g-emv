"""[P6-19 · 2] PUERTA6g: VERSION NUEVA, DECLARADA, DE `puerta6_P6_15` CON GOLPES ESPERADOS.
Copia de la puerta6 (comparador B: el cuerpo decidiendo paso a paso) en la que la
imaginacion LLEVA los golpes de los rivales como EXPECTATIVA, no como simulacion:
en cada tic proyectado, a la vida se le resta la suma, sobre los rivales que el
cuerpo ve o le cuentan (los `agents` de la foto, quietos donde estan), del dano
por rival-tic de las TASAS BASE (`P6_19_tasas.json`, tabla arma x distancia,
medidas en los 200 diarios del mundo del seis). Vale tanto para el comparador
(`rollout_g`) como para la curva del plan (`curva_H_g`): las dos cosas se
imaginan con la misma expectativa. La puerta del cinco, `forma`, `forma_viva`
y `proyeccion` NO se tocan: se importan y se les llama; los ganchos se instalan
y se quitan desde fuera (`instala` / `quita`).

Declarado: los rivales no se mueven en la imaginacion (como en puerta6); el
dano esperado no distingue si el rival nos mira; no se modela el dano que
hacemos nosotros (P6-19 §4 lo dice).
"""
from __future__ import annotations
import copy
import json
import os
import sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    if p not in sys.path:
        sys.path.insert(0, p)
import forma as F                                   # noqa: E402
import proyeccion as P                              # noqa: E402
import alcance_g as AL                              # noqa: E402
from alma import decisor_zs as D                    # noqa: E402
import puerta6_P6_15 as P6                          # noqa: E402

VERSION = "puerta6g (P6-19): puerta6 + dano esperado por tic de las tasas base (arma x distancia, o por contexto) en el comparador y en la curva del plan"
_TASAS = None; _CTX = None
MODO = {"v": "arma_dist"}      # "arma_dist" (la literal: por rival visto/contado, arma x distancia) | "contexto" (fase/dentro, declarada como variante)
C = (24, 24)
BINS = [(1, 1, "1"), (2, 2, "2"), (3, 4, "3-4"), (5, 6, "5-6"), (7, 8, "7-8"), (9, 99, ">8")]


def tasas():
    global _TASAS
    if _TASAS is None:
        _TASAS = json.load(open(os.path.join(AQUI, "P6_19_tasas.json")))["tabla_puerta6g"]
    return _TASAS


def bin_de(d):
    for lo, hi, n in BINS:
        if lo <= d <= hi:
            return n
    return ">8"


def tasas_ctx():
    global _CTX
    if _CTX is None:
        _CTX = json.load(open(os.path.join(AQUI, "P6_19_tasas.json")))["por_tic"]
    return _CTX


def _fase_r1(mundo, tick):
    k = None
    for i, f in enumerate(mundo.zone_schedule or []):
        if f[0] <= tick:
            k = i
    return k, (float(mundo.zone_schedule[k][4]) if k is not None else 48.0)


def dano_esperado_ctx(pos, obs_w, mundo, tick):
    """Variante declarada: la tasa por tic del CONTEXTO (fases 1-4 / fases 5-7 dentro / fuera), 0 sin rivales a la vista."""
    n = sum(1 for a in ((obs_w.get("visible") or {}).get("agents") or []) if a.get("slot") not in (mundo.slot, mundo.teammate_slot) and a.get("pos"))
    if n == 0:
        return 0.0
    k, r1 = _fase_r1(mundo, tick)
    ctx = "fases 1-4" if (k is None or k < 4) else ("fases 5-7 dentro" if ((pos[0] - C[0]) ** 2 + (pos[1] - C[1]) ** 2) ** 0.5 <= r1 else "fases 5-7 fuera")
    return float((tasas_ctx().get(ctx) or {}).get("dano_por_tic") or 0.0)


def dano_esperado(pos, obs_w, mundo, tick=None):
    """Suma del dano por rival-tic esperado sobre los rivales de la foto (vistos o contados), quietos."""
    if MODO["v"] == "contexto" and tick is not None:
        return dano_esperado_ctx(pos, obs_w, mundo, tick)
    T = tasas(); s = 0.0
    for a in ((obs_w.get("visible") or {}).get("agents") or []):
        sl = a.get("slot")
        if sl == mundo.slot or sl == mundo.teammate_slot or not a.get("pos"):
            continue
        h = a.get("hand"); w = (h.get("id") if isinstance(h, dict) else h) or "none"
        if w.startswith("~"):
            w = "none"
        d = max(abs(pos[0] - a["pos"][0]), abs(pos[1] - a["pos"][1]))
        fila = T.get(w) or T.get("none") or {}
        s += float((fila.get(bin_de(d)) or {}).get("dano_por_rival_tic") or 0.0)
    return s


# ── la curva del plan, con golpes esperados ─────────────────────────────────
def curva_H_g(estado0, obs_w, tramos, mundo, mem, suelo, tics, herm_slot, diario_h, pisos):
    """Como `forma.curva_H`, proyectando tic a tic y restando el dano esperado."""
    e = F.copia_estado(estado0)
    e.setdefault("cura", None)
    suelo_act = dict(suelo)
    out = []
    for i, tic in enumerate(tics):
        K = tic - e["tick"]
        if K < 0:
            continue
        tr = tramos[i] if i < len(tramos) else {"destino": None, "intencion": "esperar"}
        plan = {"destino": tr.get("destino"), "coger": tr.get("intencion") == "coger", "usar": tr.get("item") if tr.get("intencion") == "usar" else None}
        for _k in range(K):
            e = P.proyectar_rapido(e, plan, 1, mundo, suelo_act)
            e["hp"] = max(0.0, e["hp"] - dano_esperado(tuple(e["pos"]), obs_w, mundo, int(e["tick"])))
            if plan.get("coger") and (e.get("_hecho") or {}).get("cogido"):
                plan = dict(plan, coger=False)
        if tr.get("intencion") == "coger":
            suelo_act.pop(tuple(tr.get("destino") or ()), None)
        o = F.foto_rapida(obs_w, e, mundo, tic, list(suelo_act.values()))
        m = mem
        if diario_h is not None:
            o, m = AL.pon_hermano(o, mem, herm_slot, diario_h.get(tic), tuple(e["pos"]), mundo)
        out.append({"tic": tic, "d": F._d2(o, mundo, m, tic, pisos), "vida": e["hp"], "W": e.get("W"), "pos": tuple(e["pos"])})
    return out


# ── el comparador: el cuerpo decidiendo paso a paso, con golpes esperados ──
def rollout_g(obs_w, estado0, t_fin, mundo, mem, bloqueos, suelo, decide=None, cada=1):
    decide = decide or (lambda *a: D.decide(*a))
    e = F.copia_estado(estado0); e.setdefault("cura", None)
    mem2 = copy.deepcopy(mem); blo2 = copy.deepcopy(bloqueos)
    suelo_act = dict(suelo); ult = None; t0 = int(e["tick"])
    snaps = {t0: F.copia_estado(e)}; n_dec = 0; plan = {"destino": None}
    for t in range(t0, t_fin):
        if cada == 1 or e.get("move_ready_in", 0) == 0 or (t - t0) % cada == 0:
            foto = F.foto_rapida(obs_w, e, mundo, t, list(suelo_act.values()))
            foto["you"]["action_result"] = None
            mem2.observa(foto, mundo, t); blo2.actualiza(foto, mundo, ult, t)
            ac, _ra = decide(foto, mundo, mem2, t, blo2); n_dec += 1
            plan = P6.accion_a_plan(ac, e, mundo); ult = ac
        e = P.proyectar_rapido(e, plan, 1, mundo, suelo_act)
        e["hp"] = max(0.0, e["hp"] - dano_esperado(tuple(e["pos"]), obs_w, mundo, t + 1))
        for it in (e.get("_hecho") or {}).get("cogido") or []:
            suelo_act.pop(tuple(e["pos"]), None)
        if plan.get("coger") or plan.get("usar"):
            plan = {"destino": None}
        snaps[t + 1] = F.copia_estado(e)
    return snaps, n_dec


# ── los ganchos: puerta6g = curva del plan g + comparador g ────────────────
_ORIG = {}
ESTADO = {"blo": None, "ultimo_snaps": None}


def _mph_g(estado0, obs_w, base, tics, mundo, mem, suelo, t0, herm_slot, diario_h, pisos, vida_min=F.VIDA_MIN):
    if not tics:
        return None, None, 0, None
    snaps, n = rollout_g(obs_w, estado0, int(tics[-1]) + 1, mundo, mem, ESTADO["blo"] or D.Bloqueos(), suelo)
    ESTADO["ultimo_snaps"] = snaps
    c = P6.curva_de_rollout(snaps, obs_w, mundo, mem, suelo, tics, pisos, herm_slot, diario_h)
    return c, "rollout_g", len(base), True


def instala(con_curva=True, con_comparador=True):
    """Instala puerta6g en `forma` (desde fuera; se quita con `quita`)."""
    if not _ORIG:
        _ORIG["curva_H"] = F.curva_H; _ORIG["mejor_propia_H"] = F.mejor_propia_H
    if con_curva:
        F.curva_H = curva_H_g
    if con_comparador:
        F.mejor_propia_H = _mph_g


def quita():
    if _ORIG:
        F.curva_H = _ORIG["curva_H"]; F.mejor_propia_H = _ORIG["mejor_propia_H"]
