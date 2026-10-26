"""[P7-23] EL BANCO DE NACER SIN SABER (molde de banco_P7_5 / banco_P7_13; UNA VIDA POR PROCESO; sin partidas ni llamadas).
  python3 banco_P7_23.py --f1 [--hilos N]   F1: los 80 diarios de A4 con `apagado` y con `TECHO` sin pedir, con las tres piezas enganchadas -> P7_23_F1.json
  python3 banco_P7_23.py --f2 [--hilos N]   F2: vidas de APRENDE de P7-14b (dia 1) replicadas con NACE y el cuaderno vacio, y con un cuaderno cargado a mano
                                            (tres usos de racion) -> P7_23_F2.json
  python3 banco_P7_23.py --vida CARP SLOT --brazo B --cuadernos DIR --salida F [--pide 0|1] [--nace 0|1]
Lo que se lee en cada tic de la replica (gancho sobre `D.candidatos` y `D.decide`, despues de las piezas): la cura imaginada de `usar_botiquin` y
`usar_racion` cuando son candidatos, k del botiquin y de la racion, si pide, lo elegido, S-PROVISION, R-HERMANO-FALTA, R-CURIOSIDAD y el destino de
`ir_curioso`. La replica sigue los pasos del diario: dice que imagina y que elegiria el cuerpo que nace en esas escenas, no lo que habria pasado."""
import collections, glob, json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_23_tmp")


def vida(carp, slot, brazo, cuad, pide, nace):
    os.environ["GEMV_P7_PIDE"] = str(pide); os.environ["GEMV_P7_PIDE2"] = str(pide); os.environ["GEMV_P7_NACE"] = str(nace)
    if not carp.startswith(("P611", "P624")): os.environ["GEMV_OJOS"] = "0"        # los diarios del siete se jugaron con los ojos apagados; los de A4 (F1), con ojos (E2)
    import banco_P7_5 as B
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS[brazo].get(k, "0")
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    from alma import decisor_zs as D
    import descubre_P7 as X, pide_P7 as J, nace_P7_23 as N
    HECHO = {}; LEC = []; CNT = collections.Counter(); EJ = {}
    _ap0 = X.aplica
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); HECHO["J"] = J.aplica(clase, registra); HECHO["N"] = N.aplica(clase, registra)
        _oc = D.candidatos; _od = D.decide
        def _cands(obs, mundo, mem, tick, bloqueos=None):
            out = _oc(obs, mundo, mem, tick, bloqueos)
            h_ = {n: r.get("heal") for n, r in out if n in ("usar_botiquin", "usar_racion")}
            cur = next((r.get("destino") for n, r in out if n == "ir_curioso"), None)
            pasos = None
            if cur:
                try: campo = D.campo_geodesico(mundo, tuple(cur)); pasos = campo.get(tuple((obs.get("you") or {}).get("pos") or (0, 0))) if campo else None
                except Exception: pasos = None
            LEC.append({"t": tick, "heal": h_, "ir_curioso": (list(cur) if cur else None), "curioso_pasos": pasos, "k_botiquin": round(X.k_ganas(mundo), 4), "k_racion": (round(N.k_de(mundo, N.racion(mundo), tuple((obs.get("you") or {}).get("pos") or (0, 0)), tick), 4) if HECHO["N"].get("NACE") else None)})
            return out
        def _dec(obs, mundo, mem, tick, bloqueos=None):
            ac, ra = _od(obs, mundo, mem, tick, bloqueos); fl = ((ra.get("ahora") or {}).get("filas") or {}); el = str(ra.get("elegido") or "")
            CNT["tics"] += 1; CNT["pide"] += int(bool(J.ESTADO.get("pedia")))
            if el.startswith("soltar_"): CNT["elige " + el] += 1
            if el.startswith(("soltar_", "hacer_sitio", "usar_", "ir_curioso", "coger")): EJ.setdefault(el, []).append(tick) if len(EJ.get(el, [])) < 8 else None
            if el.startswith("hacer_sitio"): CNT["elige hacer_sitio"] += 1
            if el in ("usar_botiquin", "usar_racion", "ir_curioso", "ir_objeto", "coger"): CNT["elige " + el] += 1
            if os.environ.get("P7_FILAS_TICK") and str(tick) == os.environ["P7_FILAS_TICK"]: print(json.dumps({n_: {kk: vv for kk, vv in (c_ if isinstance(c_, dict) else {"d": c_}).items() if kk in ("d", "filas", "pos_prevista", "hp_prevista")} for n_, c_ in (ra.get("candidatos") or {}).items()}), file=sys.stderr)
            if LEC and LEC[-1]["t"] == tick: LEC[-1].update({"el": el, "S-PROVISION": (fl.get("S-PROVISION") or {}).get("M"), "R-HERMANO-FALTA": (fl.get("R-HERMANO-FALTA") or {}).get("M"), "R-CURIOSIDAD": (fl.get("R-CURIOSIDAD") or {}).get("M"), "R-ACOPIO": (fl.get("R-ACOPIO") or {}).get("M"), "pide": bool(J.ESTADO.get("pedia"))})
            return ac, ra
        D.candidatos = _cands; D.decide = _dec
        return h
    X.aplica = _aplica
    r = B.vida(carp, slot, brazo, cuad)
    heals = collections.Counter(); kb = collections.Counter(); kr = collections.Counter()
    for l in LEC:
        for n_, h_ in l["heal"].items(): heals[(n_, round(float(h_ or 0), 2))] += 1
        kb[l["k_botiquin"]] += 1
        if l.get("k_racion") is not None: kr[l["k_racion"]] += 1
    t1 = min((h["t0"] for h in r["huellas"]), default=None)
    antes = [l for l in LEC if t1 is None or l["t"] < t1]
    ANTES = {"tics": len(antes), "primer_uso": t1, "heal_max_botiquin": max((float(l["heal"].get("usar_botiquin") or 0) for l in antes if "usar_botiquin" in l["heal"]), default=None), "heal_max_racion": max((float(l["heal"].get("usar_racion") or 0) for l in antes if "usar_racion" in l["heal"]), default=None),
             "candidatos_usar_botiquin": sum(1 for l in antes if "usar_botiquin" in l["heal"]), "candidatos_usar_racion": sum(1 for l in antes if "usar_racion" in l["heal"]), "k_botiquin_max": max((l["k_botiquin"] for l in antes), default=None), "k_racion_max": max((l["k_racion"] or 0 for l in antes), default=None),
             "tics_pidiendo": sum(1 for l in antes if l.get("pide")), "elige_soltar": sum(1 for l in antes if str(l.get("el") or "").startswith("soltar_")), "elige_usar": sum(1 for l in antes if str(l.get("el") or "").startswith("usar_")), "S-PROVISION_max": max((float(l.get("S-PROVISION") or 0) for l in antes), default=None), "R-HERMANO-FALTA_max": max((float(l.get("R-HERMANO-FALTA") or 0) for l in antes), default=None)}
    return {"carp": carp, "slot": slot, "brazo": brazo, "pide": pide, "nace": nace, "antes_del_primer_uso": ANTES, "hecho": r["hecho"], "hecho_J": HECHO.get("J"), "hecho_N": HECHO.get("N"), "tics": r["tics"], "fidelidad": r["fidelidad"], "desacuerdos": r["desacuerdos"][:50], "errores": r["errores"],
            "cuenta": dict(CNT), "heals_imaginadas": {f"{n_} {h_}": k_ for (n_, h_), k_ in heals.most_common()}, "k_botiquin": {str(k_): v_ for k_, v_ in kb.most_common(6)}, "k_racion": {str(k_): v_ for k_, v_ in kr.most_common(6)},
            "ir_curioso": {"tics con candidato": sum(1 for l in LEC if l["ir_curioso"]), "destinos distintos": len({tuple(l["ir_curioso"]) for l in LEC if l["ir_curioso"]}), "sin camino": sum(1 for l in LEC if l["ir_curioso"] and l.get("curioso_pasos") is None), "destinos": {str(k_): v_ for k_, v_ in collections.Counter(tuple(l["ir_curioso"]) for l in LEC if l["ir_curioso"]).most_common(5)}},
            "filas_max": {f_: max((float(l.get(f_) or 0) for l in LEC), default=None) for f_ in ("S-PROVISION", "R-HERMANO-FALTA", "R-CURIOSIDAD", "R-ACOPIO")},
            "ejemplos": EJ, "usos_registrados": r["usos"], "huellas": r["huellas"], "cuaderno_fin": r["cuaderno_fin"]}


def lanza(carp, slot, brazo, cuad, pide, nace, salida):
    if os.path.exists(salida): os.remove(salida)
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(slot), "--brazo", brazo, "--cuadernos", cuad, "--pide", str(pide), "--nace", str(nace), "--salida", salida], capture_output=True, text=True, timeout=3600)
    return json.load(open(salida)) if os.path.exists(salida) else {"carp": carp, "slot": slot, "brazo": brazo, "error": (r.stderr or r.stdout)[-800:]}


def f1(hilos):
    vidas = [(os.path.basename(c), s) for pat in ("P611_t1_A4_*", "P611_t2_A4_*", "P624_t1_A4_*") for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))) for s in (10, 11) if glob.glob(os.path.join(c, f"*policy_agent_{s}.art.log"))]
    R = {}
    for brazo in ("apagado", "TECHO"):
        t0 = time.time(); cu = os.path.join(SAL, "cuad_f1_" + brazo); os.makedirs(cu, exist_ok=True)
        with ThreadPoolExecutor(hilos) as ex: res = list(ex.map(lambda v: lanza(v[0], v[1], brazo, cu, 0, 1, os.path.join(SAL, f"f1_{brazo}_{v[0]}_{v[1]}.json")), vidas))
        fid = collections.Counter(); des = []
        for r in res:
            if r.get("error"): fid["error"] += 1; print("  ERROR", r["carp"], r["slot"], r["error"][-300:], flush=True); continue
            fid.update(r["fidelidad"]); des += [{"vida": f"{r['carp']}/{r['slot']}", **d} for d in r["desacuerdos"]]
        ok = next((r for r in res if not r.get("error")), {})
        R[brazo] = {"vidas": len(vidas), "fidelidad": dict(fid), "desacuerdos": des, "segundos": round(time.time() - t0, 1), "hecho": ok.get("hecho"), "hecho_J": ok.get("hecho_J"), "hecho_N": ok.get("hecho_N")}
        print(f"F1 {brazo}: {dict(fid)} · {len(des)} desacuerdos · {R[brazo]['segundos']} s · nace {ok.get('hecho_N')}", flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_23_F1.json"), "w"), ensure_ascii=False, indent=1)


def cuaderno_a_mano(destino, slot, usos_racion=3):
    """F2 (b): un cuaderno con tres usos de racion completados (efecto cuerpo 15, la cura del catalogo; recursos -1), sin nada del botiquin."""
    sys.path.insert(0, AQUI); from recuerdo_P7_23 import CuadernoP23
    c = CuadernoP23(slot); c.dia = 1
    for i in range(usos_racion):
        c.apunta_P23("rations", {"dentro": True, "golpeado_48": False}, {"dolor_F": 0.8, "dolor_R": 0.5, "dolor_S": 0.4, "positivo": 0.2, "d": 3.5}, ["noop"] * 4, {"cuerpo": 15.0, "recursos": -1.0, "vinculo": 0.0}, {"cuerpo": -0.1, "recursos": 0.05, "vinculo": 0.0}, tick=1000 + i)
    os.makedirs(destino, exist_ok=True); c.escribe(os.path.join(destino, f"cuaderno_P7_{slot}.json")); return c


def f2(hilos):
    carps = [os.path.basename(c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P714b_s*_d1_APRENDE_*")))]
    vidas = [(c, s) for c in carps for s in (10, 11)]
    R = {}
    for etiqueta, carga in (("vacio", False), ("tres_raciones", True)):
        cu = os.path.join(SAL, "cuad_f2_" + etiqueta); shutil.rmtree(cu, ignore_errors=True); os.makedirs(cu)
        if carga:
            for s in (10, 11): cuaderno_a_mano(cu, s)
        t0 = time.time()
        with ThreadPoolExecutor(hilos) as ex: res = list(ex.map(lambda v: lanza(v[0], v[1], "APRENDE", os.path.join(SAL, f"cuad_f2_{etiqueta}_{v[0]}_{v[1]}") if not shutil.copytree(cu, os.path.join(SAL, f"cuad_f2_{etiqueta}_{v[0]}_{v[1]}"), dirs_exist_ok=True) else cu, 1, 1, os.path.join(SAL, f"f2_{etiqueta}_{v[0]}_{v[1]}.json")), vidas))
        R[etiqueta] = {"vidas": [{k_: v_ for k_, v_ in r.items() if k_ not in ("desacuerdos", "huellas", "cuaderno_fin")} | {"huellas": len(r.get("huellas") or []), "recuerdos_al_fin": (sum(len(s_) for o_ in ((r.get("cuaderno_fin") or {}).get("objetos") or {}).values() for s_ in (o_.get("situaciones") or {}).values()) if r.get("cuaderno_fin") else None)} for r in res], "segundos": round(time.time() - t0, 1)}
        print(f"F2 {etiqueta}: {len(res)} vidas · {R[etiqueta]['segundos']} s", flush=True)
        for r in res:
            if r.get("error"): print("  ERROR", r.get("carp"), r.get("slot"), r["error"][-300:], flush=True)
            else: print("  ", r["carp"], r["slot"], "heals", r["heals_imaginadas"], "| k_bot", r["k_botiquin"], "| k_rac", r["k_racion"], "| cuenta", {k_: v_ for k_, v_ in r["cuenta"].items() if k_ != "tics"}, "| filas_max", r["filas_max"], flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_23_F2.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    os.makedirs(SAL, exist_ok=True); a = sys.argv
    hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 6
    if "--vida" in a:
        i = a.index("--vida"); carp, slot = a[i + 1], int(a[i + 2]); brazo = a[a.index("--brazo") + 1]; cuad = a[a.index("--cuadernos") + 1]; salida = a[a.index("--salida") + 1]
        pide = int(a[a.index("--pide") + 1]) if "--pide" in a else 1; nace = int(a[a.index("--nace") + 1]) if "--nace" in a else 1
        json.dump(vida(carp, slot, brazo, cuad, pide, nace), open(salida, "w"), ensure_ascii=False)
    elif "--f1" in a: f1(hilos)
    elif "--f2" in a: f2(hilos)
