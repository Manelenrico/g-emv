"""[P5-8C] Por que muere la forma de curiosidad al primer examen. En seco.

Para cada forma ACEPTADA (la puerta de P5-8A con el mecanismo de P5-8B bis),
se vuelve a juzgar en tres instantes —tic 0, tic 25 y el tic de LLEGADA
proyectada— y se mira quien la mata bajo cuatro reglas.

  R0 la actual: margen 0,062 (C=0,30), examen a los 25.
  R1 margen base 0,02, sin C, por ser forma propia del cuerpo.
  R2 horizonte: el examen no cae antes de la llegada proyectada.
  R3 decaimiento con exponente 1 en vez de 3 (SOLO para separar causas).
"""
from __future__ import annotations
import collections, copy, glob, json, os, random, statistics as st, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U
from serie_util import D, DOV
from alma import appraisal_zs_v42_exp as V42
import banco_llaves as B
import curiosidad as C, curiosidad_forma as CFM
import forma as F, proyeccion as P

MARGEN_R0, MARGEN_R1 = 0.062, 0.02
EXAMEN = 25


def seats(cual):
    if cual == "lento":
        for d in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs",
                                               "P57C_t*_A_*"))):
            for f in sorted(glob.glob(os.path.join(d, "*.art.log"))):
                yield (os.path.basename(d), f)
    else:
        fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                           "*-policy_agent_1*.art.log")))
        for i in sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40)):
            yield (os.path.basename(fs[i])[:12], fs[i])


def _juzga_en(r, mundo, mem, blo, ojo, cam, dest, t, am, exp=None):
    """(ventaja, veredicto) de la forma desde el estado REAL en el tic `t`."""
    o = DOV.a_obs(r)
    o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
    e0 = P.estado_de(r)
    suelo = {tuple(it["pos"]): it for it in (r.get("ve_items") or [])
             if it.get("pos")}
    tramos = [{"destino": list(dest), "intencion": "ver", "esperar": 0}]
    tics = [x[0] for x in F.puntos_de_control(e0, tramos)]
    if not tics:
        return None, None
    pisos = F.pisos_rival(o, mundo, mem, t)
    base = list(D.candidatos(o, mundo, copy.deepcopy(mem), t,
                             copy.deepcopy(blo)))
    _e = None
    if exp is not None:
        _e = V42.BOTIN_EXP
        V42.BOTIN_EXP = exp          # R3: solo para separar causas
    _orig, _p = CFM.con_renglon(ojo, mundo, cam, tics, t, am)
    try:
        cf = F.curva_H(e0, o, tramos, mundo, mem, suelo, tics, None, None,
                       pisos)
        cs, _q, _n, _m = F.mejor_propia_H(e0, o, base, tics, mundo, mem,
                                          suelo, t, None, None, pisos)
    finally:
        CFM.restaura(_orig)
        if _e is not None:
            V42.BOTIN_EXP = _e
    if cs is None:
        return None, None
    ver, ar, _d = F.juzga_margen(cf, cs, t, margen=0.0)
    return ar, ver


def un_asiento(nombre, f, tope=12):
    recs = list(U.lee(f))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    if not (pc and sm and cat):
        return []
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    herm = pc.get("teammate_slot")
    paso = mundo.coste_movimiento(5)        # tics por casilla, del mundo
    ojo = C.Ojo(mundo, 8)
    mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
    tks = [x for x in recs if x.get("k") == "tick"]
    vivos = [x for x in tks if x.get("phase") == "live"]
    por_tic = {r["tick"]: r for r in vivos}
    dano, out = [], []
    for r in tks:
        t = r["tick"]
        o = DOV.a_obs(r)
        o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
        mem.observa(o, mundo, t); blo.actualiza(o, mundo, ult, t)
        ult = r.get("intencion")
        dano.append((t, sum(float(x.get("amount") or 0)
                            if isinstance(x, dict) else 0.0
                            for x in (r.get("damage_taken") or []))))
        if r.get("phase") != "live":
            continue
        pos = tuple(r.get("pos") or ())
        if pos:
            ojo.mira(pos, t)
        if len(out) >= tope:
            continue
        if t < B.DESDE or (t - B.DESDE) % 200:
            continue
        if not pos:
            continue
        d100 = sum(v for (tt, v) in dano if t - tt < C.VENTANA_DANO)
        am, _ = C.amenaza(r, mundo, herm, d100, t)
        if am >= CFM.UMBRAL_SEGURO or ojo.ignorancia_global() <= 0.5:
            continue
        arms = CFM.armados(r, mundo, herm)
        cam, dist, dest = CFM.camino_a_frontera(ojo, mundo, pos, arms)
        if dest is None:
            continue
        pre = copy.deepcopy(mem)
        ar0, ver0 = _juzga_en(r, mundo, pre, blo, ojo, cam, dest, t, am)
        if ar0 is None or ar0 <= MARGEN_R0:
            continue                      # no la aceptaria R0: no es «aceptada»
        llegada = dist * paso
        fila = {"nombre": nombre, "tick": t, "dist": dist, "paso": paso,
                "llegada": llegada, "ar0": ar0, "ign0": ojo.ignorancia_global()}
        for etq, dt, exp in (("25", EXAMEN, None), ("llegada", llegada, None),
                             ("25_exp1", EXAMEN, 1),
                             ("llegada_exp1", llegada, 1)):
            rr = por_tic.get(t + dt)
            if rr is None:
                fila["ar_" + etq] = None
                continue
            a, v = _juzga_en(rr, mundo, copy.deepcopy(mem), blo, ojo, cam,
                             dest, t + dt, am, exp=exp)
            fila["ar_" + etq] = a
        # ¿la ignorancia proyectada baja de verdad al llegar?
        vistas = set(ojo.primera_vez)
        for q in cam:
            vistas |= ojo.vistas_desde(q)
        fila["ign_llegada"] = 1.0 - len(vistas) / float(ojo.n_arena)
        out.append(fila)
    return out


def main():
    cual = sys.argv[1] if len(sys.argv) > 1 else "lento"
    todo = []
    for n, (nombre, f) in enumerate(seats(cual), 1):
        todo += un_asiento(nombre, f)
        print(f"  [{n}] {nombre}: {len(todo)} formas acumuladas", flush=True)
    json.dump(todo, open(os.path.join(AQUI, f"P58C_{cual}.json"), "w"))
    print(f"guardado en P58C_{cual}.json ({len(todo)} formas)")


if __name__ == "__main__":
    main()
