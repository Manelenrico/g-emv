"""[P7-25, medida 2] CUANTA CURIOSIDAD HARIA FALTA. Replica (molde de banco_P7_23 / banco_P7_15; UN SUBPROCESO POR VIDA; sin partidas ni llamadas) de las 12 vidas de
APRENDE del humo de P7-23 y del freno de P7-24, tal como se jugaron (la pieza de nacer encendida, el cuaderno que leyo ese dia). En cada tic con el PASO LISTO
(`move_ready_in` = 0; los de enfriamiento no cuentan, mesa de P7-25) y que este en una de las dos situaciones de abajo, el cuerpo decide cinco veces sobre la misma
escena y la misma memoria (copias): con la escala de la curiosidad de hoy (la decision del campo, comprobada contra el diario) y con la escala x1,5, x2, x3 y x4
(`nace_P7_23.E["escala_curiosidad"]`: multiplica la M de R-CURIOSIDAD y la promesa de ir a por la cosa; nada mas). Solo se mira la decision de ese tic: no se inventa el resto.
SITUACIONES, fijadas antes de contar:
  (a) EN CALMA, SIN RIVAL A LA VISTA Y CON UN OBJETO DESCONOCIDO A 1 O 2 CASILLAS: calma > 0,5 (1 - max de las filas de la calma de la radiografia del campo), ningun agente
      rival en `visible.agents`, y un botiquin o racion a la vista a distancia Chebyshev <= 2 de una clase de la que el cuaderno aun no tiene ningun recuerdo.
  (a') como (a) pero admitiendo rivales a la vista a mas de 4 casillas (anadida tras la primera pasada: el caso del freno tenia rivales a 5-8 casillas y no entraba en (a) ni en (b)).
  (b) PELIGRO: fuera del circulo (la situacion del cuerpo, `descubre_P7.situacion`), o un rival a la vista a 4 casillas o menos, o vida < 50.
  "Va hacia lo nuevo": elige `ir_curioso`, o `coger`, o `ir_objeto`. "Huir / entrar / curarse" hoy: un paso o `ir_*` que no sea `ir_curioso` estando fuera (entrar al circulo
  o huir), o `usar_botiquin` / `usar_racion` (curarse). La curiosidad "gana" con un factor si con el elige `ir_curioso` y hoy no.
  python3 banco_P7_25.py            -> P7_25_decisiones.json
  python3 banco_P7_25.py --vida CAMPO_D_SLOT (p. ej. P723_1_10)"""
import collections, copy, glob, json, math, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_25_tmp"); FACTORES = (1.5, 2.0, 3.0, 4.0); RES = {"P723": "P7_23_res", "P724": "P7_24_res"}


def una(pref, d, sl):
    os.environ["GEMV_P7_PIDE"] = "1"; os.environ["GEMV_P7_PIDE2"] = "1"; os.environ["GEMV_P7_NACE"] = "1"; os.environ["GEMV_OJOS"] = "0"
    import banco_P7_5 as B
    carp = os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"{pref}_s1_d{d}_APRENDE_*"))[0])
    cuad = os.path.join(SAL, f"cuad_{pref}_d{d}_{sl}"); shutil.rmtree(cuad, ignore_errors=True); os.makedirs(cuad)
    if d > 1:
        for q in (10, 11): shutil.copy(os.path.join(AQUI, RES[pref], f"cuaderno_s1_d{d - 1}_APRENDE_{q}.json"), os.path.join(cuad, f"cuaderno_P7_{q}.json"))
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS["APRENDE"].get(k, "0")
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import mide_P6_29 as M
    from alma import decisor_zs as D
    import descubre_P7 as X, pide_P7 as J, nace_P7_23 as N
    _ap0 = X.aplica
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); J.aplica(clase, registra); N.aplica(clase, registra); return h
    X.aplica = _aplica
    REG = []; CNT = collections.Counter(); _d0 = M._DEC0
    def _dec(obs, mundo, mem, tick, bloqueos=None):
        you = obs.get("you") or {}; listo = (you.get("move_ready_in") or 0) == 0; pos = tuple(you.get("pos") or (0, 0))
        ac, ra = _d0(obs, mundo, mem, tick, bloqueos); el = str(ra.get("elegido") or ""); CNT["tics"] += 1
        if not listo: return ac, ra
        CNT["listos"] += 1
        if os.environ.get("P7_DEBUG_TICK") and str(tick) == os.environ["P7_DEBUG_TICK"]: print(json.dumps({k_: v_ for k_, v_ in ((ra.get("ahora") or {}).get("filas") or {}).items()})[:600], file=sys.stderr); print(json.dumps(((ra.get("ahora") or {}).get("filas") or {}).get("F-4-ALCANCE")), "| claves ahora:", list((ra.get("ahora") or {}).keys()), file=sys.stderr)
        fl = ((ra.get("ahora") or {}).get("filas") or {}); g = lambda k: float((fl.get(k) or {}).get("M", 0.0)) if isinstance(fl.get(k), dict) else float(fl.get(k) or 0.0)
        calma = 1.0 - max([g(k) for k in X.CALMA_FILAS] + [0.0]); vis = obs.get("visible") or {}
        riv = [a for a in (vis.get("agents") or []) if a.get("team") != getattr(mundo, "team", None) and a.get("slot") != mundo.teammate_slot and a.get("pos")]
        d_riv = min((max(abs(a["pos"][0] - pos[0]), abs(a["pos"][1] - pos[1])) for a in riv), default=None)
        c = X.ESTADO["cuaderno"]; desconocidas = {o for o in N.consumibles(mundo) if c is None or not c.recuerdos_de(o)}
        ids_desc = {X.kit(mundo)} if X.kit(mundo) in desconocidas else set(); ids_desc |= set(N.raciones(mundo)) if N.racion(mundo) in desconocidas else set()
        obj_cerca = min((max(abs(it["pos"][0] - pos[0]), abs(it["pos"][1] - pos[1])) for it in (vis.get("items") or []) if it.get("id") in ids_desc and it.get("pos")), default=None)
        fuera = X.situacion(mundo, pos, tick) == "fuera"; hp = float(you.get("hp") or 0.0)
        a_ = calma > 0.5 and not riv and obj_cerca is not None and obj_cerca <= 2; b_ = fuera or (d_riv is not None and d_riv <= 4) or hp < 50.0
        a2_ = calma > 0.5 and (d_riv is None or d_riv > 4) and obj_cerca is not None and obj_cerca <= 2        # (a') como (a) pero admitiendo rivales a la vista a mas de 4 casillas (el caso del freno: rivales a 5-8)
        if not (a_ or a2_ or b_): return ac, ra
        CNT["evaluados"] += 1; alt = {}
        for f in FACTORES:
            N.E["escala_curiosidad"] = f
            try: _, ra2 = _d0(copy.deepcopy(obs), mundo, copy.deepcopy(mem), tick, copy.deepcopy(bloqueos)); alt[str(f)] = str(ra2.get("elegido") or "")
            finally: N.E["escala_curiosidad"] = 1.0
        REG.append({"t": tick, "hoy": el, "alt": alt, "a": a_, "a2": a2_, "b": b_, "calma": round(calma, 3), "rival_a_la_vista": bool(riv), "d_rival": d_riv, "obj_desconocido_a": obj_cerca, "fuera": fuera, "hp": hp,
                    "d_hoy": {k_: (v_["d"] if isinstance(v_, dict) else v_) for k_, v_ in (ra.get("candidatos") or {}).items() if k_ in ("ir_curioso", "ir_centro", "ir_botin", "ir_pareja", "ir_objeto", "coger", "noop", el)}})
        return ac, ra
    M._DEC0 = _dec
    r = B.vida(carp, sl, "APRENDE", cuad)
    return {"campo": pref, "dia": d, "slot": sl, "tics": r["tics"], "fidelidad": r["fidelidad"], "errores": len(r["errores"]), "cuenta": dict(CNT), "registros": REG}


if __name__ == "__main__":
    os.makedirs(SAL, exist_ok=True)
    if "--vida" in sys.argv:
        pref, d, sl = sys.argv[sys.argv.index("--vida") + 1].split("_"); json.dump(una(pref, int(d), int(sl)), open(os.path.join(SAL, f"dec_{pref}_{d}_{sl}.json"), "w"), ensure_ascii=False)
    else:
        claves = [f"{pref}_{d}_{sl}" for pref in ("P723", "P724") for d in (1, 2, 3) for sl in (10, 11)]
        def lanza(k):
            f = os.path.join(SAL, f"dec_{k}.json")
            if os.path.exists(f): os.remove(f)
            r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", k], capture_output=True, text=True, timeout=10800)
            return json.load(open(f)) if os.path.exists(f) else {"clave": k, "error": (r.stderr or r.stdout)[-600:]}
        with ThreadPoolExecutor(4) as ex: R = list(ex.map(lanza, claves))
        err = [r for r in R if r.get("error")]
        if err: print("ERRORES", len(err), err[0]["clave"], err[0]["error"][-400:])
        json.dump([r for r in R if not r.get("error")], open(os.path.join(AQUI, "P7_25_decisiones.json"), "w"), ensure_ascii=False)
        fid = collections.Counter()
        for r in R:
            for k_, n in (r.get("fidelidad") or {}).items(): fid[k_] += n
        print("vidas", len(R) - len(err), "· fidelidad", dict(fid), "· evaluados", sum(r.get("cuenta", {}).get("evaluados", 0) for r in R))
