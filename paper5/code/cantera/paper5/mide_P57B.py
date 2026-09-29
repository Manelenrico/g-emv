"""[P5-7B] B1 (la memoria por asiento) y B3 (en seco, con el arnes).

  python3 cantera/paper5/mide_P57B.py b1 s2      > ...
  python3 cantera/paper5/mide_P57B.py b1 lento
  python3 cantera/paper5/mide_P57B.py b1 434     (solo estadisticas de B1)
  python3 cantera/paper5/mide_P57B.py b3 s2
  python3 cantera/paper5/mide_P57B.py b3 lento

Diarios de UNO EN UNO (la regla de memoria del acta de P5-2b).
Muestreo de B3: se decide cada `banco_llaves.CADA` tics desde `DESDE`, como en
P5-7A; el resto de la vida se recorre igual para que la memoria por asiento se
acumule bien. Las fracciones son estimaciones de muestra, y se dice.
"""
from __future__ import annotations
import collections, copy, glob, json, os, random, statistics as st, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)

import serie_util as U                                    # noqa: E402
from serie_util import D, DOV                             # noqa: E402
from alma import appraisal_zs_v42_exp as V42              # noqa: E402
import banco_llaves as B                                  # noqa: E402
import curiosidad as C                                    # noqa: E402
import otros as O                                         # noqa: E402

PROG = open(os.path.join(AQUI, "P57B_progreso.log"), "w", buffering=1)


def avisa(t):
    print(t, flush=True)
    PROG.write(t + "\n")


# las carpetas de los 434, las MISMAS que uso E3 (`E3_golpes.py:16`)
CARP_434 = ("S2_A", "S2_B", "S2_C", "S2_Aconf",
            "S3_D0", "S3_D100", "S3_T", "S3_humo_D300", "S3_humo2_D300")

# B3: cada fila SOLA, para poder atribuir los cambios, y una conjunta
CONFIGS = [("otros_k0.05", 0.05, 0.0), ("otros_k0.1", 0.1, 0.0),
           ("otros_k0.2", 0.2, 0.0),
           ("vinc_k0.1", 0.0, 0.1), ("vinc_k0.2", 0.0, 0.2),
           ("juntas_0.1_0.1", 0.1, 0.1)]


def seats(cual):
    if cual == "lento":
        for c in ("P5_B1", "P5_C2", "P5_C3"):
            for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs",
                                                   c, "*.art.log"))):
                yield (c + "/" + os.path.basename(f).split("policy_agent_")[1][:2]
                       .strip("."), f)
    elif cual == "434":
        for c in CARP_434:
            d = os.path.join(RAIZ, "paintball", "runs", c)
            if not os.path.isdir(d):
                continue
            for f in sorted(glob.glob(os.path.join(
                    d, "*-policy_agent_1*.art.log"))):
                yield (c + "/" + os.path.basename(f)[:12], f)
    else:
        fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                           "*-policy_agent_1*.art.log")))
        idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)),
                                                     min(B.N_DIARIOS, len(fs))))
        for i in idx:
            yield (os.path.basename(fs[i])[:12] + "/"
                   + os.path.basename(fs[i]).split("policy_agent_")[1][:2]
                   .strip("."), fs[i])


def _cabeceras(recs):
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    return pc, sm, cat


# ══════════════════════════════════════════════════════════════════════════
#  B1 · la memoria por asiento
# ══════════════════════════════════════════════════════════════════════════
def b1_de_uno(nombre, f):
    recs = list(U.lee(f))
    pc, sm, cat = _cabeceras(recs)
    if not (pc and sm and cat):
        return None
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    herm = pc.get("teammate_slot")
    m = O.MemoriaOtros(mundo, herm)
    fin = next((r for r in recs if r.get("k") == "final"), None)
    vivos = 0
    # cuantos tics tarda un asiento en salir de NEUTRO, por cada N
    sale = {n: {} for n in O.N_A_TIRO}
    muertes_con_C0 = 0
    ult_golpes = []
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        t = r["tick"]
        vivos += 1
        antes = {n: {sl: o.signo(n) for sl, o in m.por_slot.items()}
                 for n in O.N_A_TIRO}
        m.observa(r, t)
        for n in O.N_A_TIRO:
            for sl, o in m.por_slot.items():
                if sl in sale[n]:
                    continue
                if antes[n].get(sl, 0) == 0 and o.signo(n) != 0:
                    sale[n][sl] = t - (o.primer_tick or t)
        for g in (r.get("damage_taken") or []):
            sl = O._slot_de(g.get("source"))
            if sl is not None and str(g.get("source")) != "zone":
                # el CONOCIMIENTO de ese asiento EN ESE MOMENTO, no al final:
                # es lo que O4 pregunta («la muerte por lo que no te habia
                # pasado»). `m.observa` ya corrio para este tic, asi que este
                # golpe ya cuenta en su conducta; se descuenta su aporte para
                # no premiar al matador por matarnos.
                _o = m.por_slot.get(sl)
                _c = _o.conocimiento() if _o else 0.0
                if _o is not None and _o.golpes_a_mi == 1 \
                        and not _o.disparos_a_otros and not _o.tics_a_tiro:
                    _c -= O.W_CONDUCTA        # su unica conducta fue pegarnos
                ult_golpes.append((t, sl, max(0.0, _c)))
    # LA MUERTE POR LO QUE NO TE HABIA PASADO: el ultimo golpe antes del final
    con_del_matador = None
    murio = bool(fin and (fin.get("reason") == "eliminated"))
    if murio and ult_golpes:
        mt = fin.get("match_ticks") or 0
        cerca = [(sl, c_) for t, sl, c_ in ult_golpes if mt - 48 <= t <= mt]
        if cerca:
            con_del_matador = cerca[-1][1]
            muertes_con_C0 = 1 if con_del_matador <= 0.0 else 0
    return {"nombre": nombre, "tics_vivos": vivos,
            "reparto": {str(n): m.reparto(n) for n in O.N_A_TIRO},
            "conocimiento": [o.conocimiento() for o in m.por_slot.values()],
            "sale_de_neutro": {str(n): list(sale[n].values())
                               for n in O.N_A_TIRO},
            "sin_arma_pero_pega": sum(1 for o in m.por_slot.values()
                                      if o.golpes_a_mi and not o.armas),
            "muerte_C0": muertes_con_C0, "murio": murio,
            "conocimiento_del_matador": con_del_matador,
            "final": bool(fin)}


def b1(cual):
    avisa(f"=== P5-7B · B1 · {cual} ===")
    todo = []
    for n, (nombre, f) in enumerate(seats(cual), 1):
        o = b1_de_uno(nombre, f)
        if o:
            todo.append(o)
        if n % 25 == 0:
            avisa(f"  ... {n} diarios")
    json.dump(todo, open(os.path.join(AQUI, f"P57B_b1_{cual}.json"), "w"))
    avisa(f"  {len(todo)} asientos · guardado en P57B_b1_{cual}.json")


# ══════════════════════════════════════════════════════════════════════════
#  B3 · en seco, con el arnes
# ══════════════════════════════════════════════════════════════════════════
def b3_de_uno(nombre, f):
    recs = list(U.lee(f))
    pc, sm, cat = _cabeceras(recs)
    if not (pc and sm and cat):
        return None
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    herm = pc.get("teammate_slot")
    mem_o = O.MemoriaOtros(mundo, herm)
    O.SOC.mem = mem_o
    mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
    tks = [x for x in recs if x.get("k") == "tick"]
    vivos = [x for x in tks if x.get("phase") == "live"]
    if not vivos:
        return None
    dano_hist = []
    # quien nos pega en los 200 tics SIGUIENTES, para el derroche
    golpes = collections.defaultdict(list)
    for r in vivos:
        for g in (r.get("damage_taken") or []):
            sl = O._slot_de(g.get("source"))
            if sl is not None and str(g.get("source")) != "zone":
                golpes[sl].append(r["tick"])
    Ocfg = {c[0]: {"cambios": 0, "por_grado": {}, "n_grado": {},
                   "veto_arma": 0, "derroche": 0, "con_desconocido": 0,
                   "voz_carencia": [0, 0], "n_otros": 0, "n_vinc": 0,
                   "max_o": 0.0, "max_s": 0.0}
            for c in CONFIGS}
    Out = {"nombre": nombre, "decididos": 0, "cfg": Ocfg, "ms": []}
    for r in tks:
        t = r["tick"]
        o = DOV.a_obs(r)
        o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
        mem.observa(o, mundo, t)
        blo.actualiza(o, mundo, ult, t)
        ult = r.get("intencion")
        dano_hist.append((t, sum(float(x.get("amount") or 0)
                                 if isinstance(x, dict) else float(x or 0)
                                 for x in (r.get("damage_taken") or []))))
        if r.get("phase") != "live":
            continue
        mem_o.observa(r, t)
        pre = copy.deepcopy(mem)
        _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
        if ((r.get("intencion") or {}).get("do") == "attack"
                or _el.startswith("atacar")):
            mem.ultimo_ataque = t
        elif _el.startswith("soltar_"):
            mem.cedidos[tuple(r.get("pos") or ())] = {
                "item": {"id": _el[len("soltar_"):], "n": 1}, "tick": t}
        if t < B.DESDE or (t - B.DESDE) % B.CADA:
            continue
        pos = tuple(r.get("pos") or ())
        if not pos:
            continue
        d100 = sum(v for (tt, v) in dano_hist if t - tt < C.VENTANA_DANO)
        am, _des = C.amenaza(r, mundo, herm, d100, t)
        gr = C.grado(am)
        a_tiro = any(max(abs(pos[0] - q[0]), abs(pos[1] - q[1]))
                     <= C._alcance(mundo, a.get("hand"))
                     for a in (r.get("ve_agentes") or [])
                     if a.get("slot") != herm and a.get("pos")
                     and C._alcance(mundo, a.get("hand")) > 0
                     for q in [tuple(a["pos"])])
        ctx = {"o": o, "mundo": mundo, "mem": pre, "blo": blo, "tick": t,
               "r": r}
        O.SOC.on = False
        base = B.decide_v42(ctx)
        Out["decididos"] += 1
        bf = ((r.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("filas") or {}
        carencia = float((bf.get("R-CARENCIA") or {}).get("M") or 0.0)
        O.SOC.amenaza_ahora = am
        O.SOC.desconocido = mem_o.desconocido_mas_cerca(r)
        O.SOC.positivos = mem_o.positivos_a_la_vista(r)
        for etq, ko, ks in CONFIGS:
            c = Ocfg[etq]
            O.SOC.on, O.SOC.k_o, O.SOC.k_s = True, ko, ks
            O.SOC.reinicia_cuentas()
            _a = time.perf_counter()
            nue = B.decide_v42(ctx)
            if etq == "otros_k0.1":
                Out["ms"].append((time.perf_counter() - _a) * 1000.0)
            c["n_grado"][gr] = c["n_grado"].get(gr, 0) + 1
            c["n_otros"] += (O.SOC.n_otros > 0)
            c["n_vinc"] += (O.SOC.n_vinculo > 0)
            c["max_o"] = max(c["max_o"], O.SOC.max_o)
            c["max_s"] = max(c["max_s"], O.SOC.max_s)
            if carencia >= 0.25:
                c["voz_carencia"][1] += 1
            if nue["elegido"] == base["elegido"]:
                continue
            c["cambios"] += 1
            c["por_grado"][gr] = c["por_grado"].get(gr, 0) + 1
            if carencia >= 0.25:
                c["voz_carencia"][0] += 1
            if a_tiro:
                c["veto_arma"] += 1
            # DERROCHE: ¿el cambio acerca a un asiento que en 200 tics nos pega?
            if O.SOC.desconocido is not None:
                sl, q, _k, _d = O.SOC.desconocido
                c["con_desconocido"] += 1
                pn = nue["candidatos"][nue["elegido"]]
                pb = base["candidatos"][base["elegido"]]
                p_new = tuple(pn["pos_prevista"]) if isinstance(pn, dict) and \
                    pn.get("pos_prevista") else pos
                p_bas = tuple(pb["pos_prevista"]) if isinstance(pb, dict) and \
                    pb.get("pos_prevista") else pos
                acerca = (max(abs(p_new[0] - q[0]), abs(p_new[1] - q[1]))
                          < max(abs(p_bas[0] - q[0]), abs(p_bas[1] - q[1])))
                if acerca and any(t < g <= t + 200 for g in golpes.get(sl, ())):
                    c["derroche"] += 1
        O.SOC.on = False
    return Out


def b3(cual):
    avisa(f"=== P5-7B · B3 · {cual} · proxy instalado ===")
    U.pon(False)
    O.instala()
    assert D.A is O.SOC, "el proxy no quedo instalado"
    todo = []
    for n, (nombre, f) in enumerate(seats(cual), 1):
        t0 = time.time()
        o = b3_de_uno(nombre, f)
        if o:
            todo.append(o)
            avisa(f"  [{n}] {nombre}: {o['decididos']} decididos · "
                  f"{time.time() - t0:.0f}s")
    json.dump(todo, open(os.path.join(AQUI, f"P57B_b3_{cual}.json"), "w"))
    avisa(f"  guardado en P57B_b3_{cual}.json")


if __name__ == "__main__":
    que = sys.argv[1] if len(sys.argv) > 1 else "b1"
    cual = sys.argv[2] if len(sys.argv) > 2 else "s2"
    (b1 if que == "b1" else b3)(cual)
