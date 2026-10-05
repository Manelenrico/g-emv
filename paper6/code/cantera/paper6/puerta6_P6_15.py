"""[P6-15] PUERTA6: VERSION NUEVA DE LA PUERTA, DECLARADA, EN ARCHIVO APARTE.
INSTRUMENTO DE MEDIDA (banco). La puerta del cinco (`policy_forma`, `forma`,
`forma_viva`, `proyeccion`) NO se toca: se importa y se le llama.

Lo que cambia en la puerta6 es SOLO EL COMPARADOR. La regla de juicio es la
misma (`forma.juzga_margen`: vida < 15 en un punto de control -> "vida"; area
<= margen -> "area"; si no "ok"), con el mismo margen de la puerta, los mismos
puntos de control y la misma `d` con piso (`forma._d2` con `pisos_rival`).

  (A) `curva_real`     — «lo que de verdad hice»: la trayectoria REAL del diario
      (posicion por tic, y sus `usar_*`/`coger`), pasada por la MISMA maquinaria
      de imaginacion que el plan (`proyeccion.proyectar` con `camino`, que sigue
      las posiciones reales y cobra el anillo, los enfriamientos y las curas con
      las reglas de la proyeccion; `forma.foto_rapida`; `forma._d2` con los
      mismos pisos). Las dos cosas quedan imaginadas. Es un TECHO: en una
      partida real no se conoce el futuro.
  (B) `rollout`        — el cuerpo imaginado DECIDIENDO PASO A PASO con su propio
      decisor (`decisor_zs.decide`, con los envoltorios del cuerpo del seis tal
      como esten enganchados) sobre fotos proyectadas SIN piso: los rivales
      quedan quietos donde el cuerpo los ve (`foto_rapida` los deja tal cual) y
      el decisor los siente como los sentiria al verlos. Cada tic: foto ->
      decide -> la accion se aplica con `proyeccion.proyectar_rapido` un tic
      (paso si las piernas estan listas, coger, usar; el anillo cobra). La CURVA
      del comparador en los puntos de control se valora despues con las mismas
      reglas que el plan (pisos), para que el juicio sea el mismo.

Declarado: (B) no modela ataques ni golpes recibidos (los rivales no actuan),
ni cambios de mano/cuerpo (`empunar`/`ponerse`); `soltar` y `atacar` cuentan
como esperar. `mem` y `bloqueos` se copian (deepcopy) como hace `_juzga`.
"""
from __future__ import annotations
import copy
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

VERSION = "puerta6 (P6-15): comparador (A) trayectoria real imaginada · (B) cuerpo decidiendo paso a paso"


# ── (A) la trayectoria real, imaginada ──────────────────────────────────────
def curva_real(estado0, obs_w, mundo, mem, suelo, tics, herm_slot, diario_h, pisos,
               pos_real, accion_real):
    """Como `forma.curva_H`, pero el cuerpo no anda hacia un destino: sigue
    `pos_real(t)` (la casilla real del diario en el tic t, o la ultima conocida)
    y hace `accion_real(t)` ("usar_botiquin", "usar_racion", "coger" o None).
    `proyeccion.proyectar(..., camino=...)` es la via prevista para eso (A3)."""
    e = F.copia_estado(estado0)
    e.setdefault("cura", None)
    suelo_act = dict(suelo)
    out = []
    for tic in tics:
        K = tic - e["tick"]
        if K < 0:
            continue
        t0 = e["tick"]
        camino = [pos_real(t0 + 1 + i) for i in range(K)]
        plan = [accion_real(t0 + 1 + i) for i in range(K)]
        e = P.proyectar(e, plan, K, mundo, suelo_act, camino=camino)
        for it in (e.get("_hecho") or {}).get("cogido") or []:
            for q, s in list(suelo_act.items()):
                if s.get("id") == it and tuple(q) == tuple(e["pos"]):
                    suelo_act.pop(q, None)
        o = F.foto_rapida(obs_w, e, mundo, tic, list(suelo_act.values()))
        m = mem
        if diario_h is not None:
            o, m = AL.pon_hermano(o, mem, herm_slot, diario_h.get(tic), tuple(e["pos"]), mundo)
        out.append({"tic": tic, "d": F._d2(o, mundo, m, tic, pisos), "vida": e["hp"],
                    "W": e.get("W"), "pos": tuple(e["pos"])})
    return out


# ── (B) el cuerpo decidiendo paso a paso ───────────────────────────────────
def accion_a_plan(ac, e, mundo):
    """La accion JSON del decisor -> el plan de UN tic para `_proyecta`."""
    do = (ac or {}).get("do")
    pos = tuple(e["pos"])
    if do == "move" and ac.get("dir") in D.DIRS:
        dx, dy = D.DIRS[ac["dir"]]
        q = (pos[0] + dx, pos[1] + dy)
        if mundo.solido(q[0], q[1]):
            return {"destino": None}
        return {"destino": q}
    if do == "pickup":
        return {"destino": pos, "coger": True}
    if do == "use":
        idx = ac.get("slot")
        pack = e.get("pack") or []
        if isinstance(idx, int) and 0 <= idx < len(pack) and pack[idx]:
            return {"destino": None, "usar": pack[idx].get("id")}
    return {"destino": None}


def rollout(obs_w, estado0, t_fin, mundo, mem, bloqueos, suelo, decide=None, cada=1):
    """Imagina al cuerpo decidiendo desde `estado0["tick"]` hasta `t_fin`.
    Devuelve ({tic: estado}, n_decisiones). `decide` por defecto es
    `decisor_zs.decide` TAL COMO ESTE ENGANCHADO en ese momento (los envoltorios
    del cuerpo del seis incluidos). `cada`: decide en todos los tics (1) o solo
    con piernas listas y cada `cada` tics (declarado si se usa)."""
    decide = decide or (lambda *a: D.decide(*a))
    e = F.copia_estado(estado0)
    e.setdefault("cura", None)
    mem2 = copy.deepcopy(mem)
    blo2 = copy.deepcopy(bloqueos)
    suelo_act = dict(suelo)
    ult = None
    t0 = int(e["tick"])
    snaps = {t0: F.copia_estado(e)}
    n_dec = 0
    plan = {"destino": None}
    for t in range(t0, t_fin):
        if cada == 1 or e.get("move_ready_in", 0) == 0 or (t - t0) % cada == 0:
            foto = F.foto_rapida(obs_w, e, mundo, t, list(suelo_act.values()))
            foto["you"]["action_result"] = None
            mem2.observa(foto, mundo, t)
            blo2.actualiza(foto, mundo, ult, t)
            ac, _ra = decide(foto, mundo, mem2, t, blo2)
            n_dec += 1
            plan = accion_a_plan(ac, e, mundo)
            ult = ac
        e = P.proyectar_rapido(e, plan, 1, mundo, suelo_act)
        for it in (e.get("_hecho") or {}).get("cogido") or []:
            suelo_act.pop(tuple(e["pos"]), None)
        if plan.get("coger") or plan.get("usar"):
            plan = {"destino": None}
        snaps[t + 1] = F.copia_estado(e)
    return snaps, n_dec


def curva_de_rollout(snaps, obs_w, mundo, mem, suelo, tics, pisos, herm_slot=None, diario_h=None):
    """La curva del comparador (B) en los puntos de control, valorada con las
    MISMAS reglas que el plan (`_d2` con pisos)."""
    out = []
    for tic in tics:
        e = snaps.get(tic) or snaps[max(snaps)]
        o = F.foto_rapida(obs_w, e, mundo, tic, list(suelo.values()))
        m = mem
        if diario_h is not None:
            o, m = AL.pon_hermano(o, mem, herm_slot, diario_h.get(tic), tuple(e["pos"]), mundo)
        out.append({"tic": tic, "d": F._d2(o, mundo, m, tic, pisos), "vida": e["hp"],
                    "W": e.get("W"), "pos": tuple(e["pos"])})
    return out


def juzga(cf_plan, cs, t0, margen):
    """La MISMA regla de la puerta, con otro comparador."""
    if not cs or any(p["d"] is None for p in cs):
        return "sin comparador", 0.0
    ver, ar, _dt = F.juzga_margen(cf_plan, cs, t0, margen=margen)
    return ver, (ar or 0.0)
