"""[P5-7A] Las medidas A1 a A6, en seco, sobre S-2 y el mundo lento.

  python3 cantera/paper5/mide_P57A.py s2     > P57A_s2.txt
  python3 cantera/paper5/mide_P57A.py lento  > P57A_lento.txt

Los dos mundos se reportan APARTE, como pide el encargo.

MUESTREO, declarado: el ojo mira en CADA tic vivo (es barato y la ignorancia
tiene que acumularse bien), pero se DECIDE cada `CADA` tics desde `DESDE`, que
son las constantes del arnes de P5-2 (`banco_llaves.CADA=50`, `DESDE=300`).
Decidir en los 200.000 tics vivos por cada una de las cinco configuraciones
serian horas; con el muestreo son minutos y la fraccion es una estimacion de
muestra, no un censo. Se dice asi.

Diarios de uno en uno: `list()` sobre los ochenta se come 3 GB (acta P5-2b).
"""
from __future__ import annotations
import copy, glob, json, os, random, statistics as st, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)

import serie_util as U                                    # noqa: E402
from serie_util import D, DOV                             # noqa: E402
from alma import appraisal_zs_v42_exp as V42              # noqa: E402
import banco_llaves as B                                  # noqa: E402
import curiosidad as C                                    # noqa: E402

PROG = open(os.path.join(AQUI, "P57A_progreso.log"), "w", buffering=1)


def avisa(t):
    print(t, flush=True)
    PROG.write(t + "\n")


# las configuraciones: las cuatro del renglon LOCAL (A3) y las cuatro de la
# variante FRONTERA (el anadido), cada una con su A5 sin balanza.
CONFIGS = [("local_k0.1", 0.1, True, "local"),
           ("local_k0.2", 0.2, True, "local"),
           ("local_k0.4", 0.4, True, "local"),
           ("local_k0.2_sin_balanza", 0.2, False, "local"),      # <- A5
           ("front_k0.1", 0.1, True, "frontera"),
           ("front_k0.2", 0.2, True, "frontera"),
           ("front_k0.4", 0.4, True, "frontera"),
           ("front_k0.2_sin_balanza", 0.2, False, "frontera")]   # <- A5
TRAMOS = 4          # tramos de vida para el reparto


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def seats(cual):
    """(nombre, fichero) de uno en uno. Nunca una lista de diarios."""
    if cual == "lento":
        for c in ("P5_B1", "P5_C2", "P5_C3"):
            for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs",
                                                   c, "*.art.log"))):
                yield (c + "/" + os.path.basename(f).split("policy_agent_")[1][:2]
                       .strip("."), f)
    else:
        fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                           "*-policy_agent_1*.art.log")))
        idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)),
                                                     min(B.N_DIARIOS, len(fs))))
        for i in idx:
            yield (os.path.basename(fs[i])[:12] + "/"
                   + os.path.basename(fs[i]).split("policy_agent_")[1][:2]
                   .strip("."), fs[i])


def dano_de(r):
    return sum(float(x.get("amount") or 0) if isinstance(x, dict)
               else float(x or 0) for x in (r.get("damage_taken") or []))


def un_asiento(nombre, fichero):
    """Todas las medidas de UN asiento-partida. Devuelve un dict."""
    recs = list(U.lee(fichero))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    arr = next((r for r in recs if r.get("k") == "arranque"), None)
    if not (pc and sm and cat):
        return None
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    INT = ((arr or {}).get("constitucion") or {}).get("intelligence", 8)
    herm = pc.get("teammate_slot")
    ojo = C.Ojo(mundo, INT)
    C.CUR.ojo = ojo
    mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
    tks = [x for x in recs if x.get("k") == "tick"]
    vivos = [x for x in tks if x.get("phase") == "live"]
    if not vivos:
        return None
    t0, t1 = vivos[0]["tick"], vivos[-1]["tick"]
    dur = max(1, t1 - t0)
    dano_hist = []
    O = {"nombre": nombre, "tics_vivos": len(vivos), "t0": t0, "t1": t1,
         "A1": {"global": [], "local": [], "novedad": [],
                "por_tramo": [[] for _ in range(TRAMOS)]},
         "A2": {"grados": {"seguro": 0, "neutro": 0, "inseguro": 0},
                "valores": [], "desglose": {"armados": 0, "dano": 0,
                                            "anillo": 0}},
         "decididos": 0, "ms": {"base": [], "con": [], "front": [],
                                "bfs": []},
         "cfg": {c[0]: {"cambios": 0, "por_grado": {}, "por_tramo": [0] * TRAMOS,
                        "n_grado": {}, "veto_arma": 0, "veto_vida": 0,
                        "derroche_arma": 0, "derroche_anillo": 0,
                        "voz_carencia": [0, 0], "voz_W": [0, 0],
                        "revela_real": [], "revela_proy": [],
                        "tics_con_M": 0, "cands_con_M": 0, "cands": 0,
                        "max_M": 0.0}
                 for c in CONFIGS}}
    pend = []          # (tick, cfg, vistas_en_t) para el «100 tics despues»
    for r in tks:
        t = r["tick"]
        o = DOV.a_obs(r)
        o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
        mem.observa(o, mundo, t)
        blo.actualiza(o, mundo, ult, t)
        ult = r.get("intencion")
        dano_hist.append((t, dano_de(r)))
        if r.get("phase") != "live":
            continue
        pos = tuple(r.get("pos") or ())
        if pos:
            ojo.mira(pos, t)
        pre = copy.deepcopy(mem)
        _in = (r.get("intencion") or {}).get("do")
        _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
        if _in == "attack" or _el.startswith("atacar"):
            mem.ultimo_ataque = t
        elif _el.startswith("soltar_"):
            mem.cedidos[tuple(r.get("pos") or ())] = {
                "item": {"id": _el[len("soltar_"):], "n": 1}, "tick": t}
        if not pos:
            continue
        # ── A1 · la ignorancia, en cada tic vivo ─────────────────────────
        ig, il = ojo.ignorancia_global(), ojo.ignorancia_local(pos)
        nv = ojo.novedad(t)
        O["A1"]["global"].append(ig); O["A1"]["local"].append(il)
        O["A1"]["novedad"].append(nv)
        tr = min(TRAMOS - 1, int(TRAMOS * (t - t0) / dur))
        O["A1"]["por_tramo"][tr].append((ig, il, nv))
        # ── A2 · la amenaza, en cada tic vivo ────────────────────────────
        d100 = sum(v for (tt, v) in dano_hist if t - tt < C.VENTANA_DANO)
        am, des = C.amenaza(r, mundo, herm, d100, t)
        gr = C.grado(am)
        O["A2"]["grados"][gr] += 1
        O["A2"]["valores"].append(am)
        for kk in ("armados", "dano", "anillo"):
            if des[kk] > 0:
                O["A2"]["desglose"][kk] += 1
        # ── A4 · solo en los tics muestreados ────────────────────────────
        if t < B.DESDE or (t - B.DESDE) % B.CADA:
            continue
        ctx = {"o": o, "mundo": mundo, "mem": pre, "blo": blo, "tick": t,
               "r": r}
        C.CUR.on = False
        _a = time.perf_counter()
        base = B.decide_v42(ctx)
        O["ms"]["base"].append((time.perf_counter() - _a) * 1000.0)
        O["decididos"] += 1
        # UN SOLO BFS por tic muestreado sirve para todos los candidatos de
        # las cuatro configuraciones de frontera. Se cronometra aparte.
        _a = time.perf_counter()
        C.CUR.dist_frontera = C.dist_a_frontera(ojo, mundo)
        C.CUR.ign_global = ig
        O["ms"]["bfs"].append((time.perf_counter() - _a) * 1000.0)
        bfilas = ((r.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("filas") or {}
        carencia = float((bfilas.get("R-CARENCIA") or {}).get("M") or 0.0)
        W = float(((r.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("W") or 0.0)
        pb = base["candidatos"][base["elegido"]]
        p_base = tuple(pb["pos_prevista"]) if isinstance(pb, dict) and pb.get(
            "pos_prevista") else pos
        armados = [tuple(a["pos"]) for a in (r.get("ve_agentes") or [])
                   if a.get("slot") != herm and a.get("pos")
                   and C._alcance(mundo, a.get("hand")) > 0]
        a_tiro = any(cheb(pos, q) <= C._alcance(
            mundo, a.get("hand")) for a, q in
            [(a, tuple(a["pos"])) for a in (r.get("ve_agentes") or [])
             if a.get("slot") != herm and a.get("pos")
             and C._alcance(mundo, a.get("hand")) > 0])
        hp = float(r.get("hp") or 100)
        for etq, k, bal, modo in CONFIGS:
            c = O["cfg"][etq]
            C.CUR.on, C.CUR.k, C.CUR.balanza = True, k, bal
            C.CUR.modo = modo
            C.CUR.amenaza_ahora = am
            C.CUR.reinicia_cuentas()
            _a = time.perf_counter()
            nue = B.decide_v42(ctx)
            if etq == "local_k0.2":
                O["ms"]["con"].append((time.perf_counter() - _a) * 1000.0)
            elif etq == "front_k0.2":
                O["ms"]["front"].append((time.perf_counter() - _a) * 1000.0)
            # diagnostico: ¿se ENCENDIO el renglon, aunque no voltease nada?
            c["cands"] += C.CUR.n_valor
            c["cands_con_M"] += C.CUR.n_valor_pos
            c["tics_con_M"] += (C.CUR.n_valor_pos > 0)
            c["max_M"] = max(c["max_M"], C.CUR.max_M)
            c["n_grado"][gr] = c["n_grado"].get(gr, 0) + 1
            if carencia >= 0.25:
                c["voz_carencia"][1] += 1
            if W < 2.0:
                c["voz_W"][1] += 1
            if nue["elegido"] == base["elegido"]:
                continue
            # ── (a) cambia ───────────────────────────────────────────────
            c["cambios"] += 1
            c["por_grado"][gr] = c["por_grado"].get(gr, 0) + 1
            c["por_tramo"][tr] += 1
            if carencia >= 0.25:
                c["voz_carencia"][0] += 1
            if W < 2.0:
                c["voz_W"][0] += 1
            # ── (d) veto vital ───────────────────────────────────────────
            if a_tiro:
                c["veto_arma"] += 1
            if hp < 30:
                c["veto_vida"] += 1
            pn = nue["candidatos"][nue["elegido"]]
            p_new = tuple(pn["pos_prevista"]) if isinstance(pn, dict) and pn.get(
                "pos_prevista") else pos
            # ── (e) derroche ─────────────────────────────────────────────
            if armados:
                if min(cheb(p_new, q) for q in armados) < \
                   min(cheb(p_base, q) for q in armados):
                    c["derroche_arma"] += 1
            ev_n = [tb for tb, dp in mundo.eventos_arde(p_new, t) if dp > 0]
            ev_b = [tb for tb, dp in mundo.eventos_arde(p_base, t) if dp > 0]
            if ev_n and (not ev_b or min(ev_n) < min(ev_b)):
                c["derroche_anillo"] += 1
            # ── (b) lo que revelaria, proyectado ─────────────────────────
            ya = set(ojo.primera_vez)
            c["revela_proy"].append(len(ojo.vistas_desde(p_new) - ya))
            pend.append((t, etq))
        C.CUR.on = False
    # ── (b) lo que revelo de verdad el diario, 100 tics despues ──────────
    for t, etq in pend:
        O["cfg"][etq]["revela_real"].append(
            sum(1 for v in ojo.primera_vez.values() if t < v <= t + 100))
    O["vistas"] = len(ojo.primera_vez)
    O["n_arena"] = ojo.n_arena
    return O


def main():
    cual = sys.argv[1] if len(sys.argv) > 1 else "s2"
    # EL PROXY, PUESTO. Sin esto `D.A` sigue siendo v42 y el renglon no entra
    # en la decision: la primera pasada dio 0 cambios por esto, no por el
    # renglon. `pon_v42` no toca `D.A`, asi que basta instalarlo una vez.
    U.pon(False)
    C.instala()
    assert D.A is C.CUR, "el proxy no quedo instalado"
    avisa(f"=== P5-7A · {cual} · proxy instalado ===")
    todo = []
    for n, (nombre, f) in enumerate(seats(cual), 1):
        t0 = time.time()
        o = un_asiento(nombre, f)
        if o is None:
            avisa(f"  [{n}] {nombre}: sin datos"); continue
        todo.append(o)
        avisa(f"  [{n}] {nombre}: {o['tics_vivos']:,} vivos · "
              f"{o['decididos']} decididos · vistas {o['vistas']}/{o['n_arena']}"
              f" · {time.time() - t0:.0f}s")
    json.dump(todo, open(os.path.join(AQUI, f"P57A_{cual}.json"), "w"))
    avisa(f"\nguardado en P57A_{cual}.json ({len(todo)} asientos)")


if __name__ == "__main__":
    main()
