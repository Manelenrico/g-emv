"""[P7-28, punto 1] LA CURIOSIDAD QUE NO SE APAGA: replica (molde de banco_P7_25; UN SUBPROCESO POR VIDA; sin partidas ni llamadas) de las vidas de APRENDE de los dias 16-20
de P7-24, tal como se jugaron (pieza de nacer encendida, el cuaderno que leyo ese dia). En cada tic con el paso listo en que el cuerpo elige `ir_curioso`, se apunta lo que el
cuerpo usa al decidir: la ignorancia de cada clase (`cuaderno.ignorancia`, la del cuaderno vivo de ese momento), el alivio de cada clase, la M de R-CURIOSIDAD, la clase que mas
llama, el destino (casilla, clase, distancia, dentro o fuera del circulo), k del botiquin y de la racion (lo que vale tenerlos), y las d de los candidatos que compiten
(`ir_curioso`, `ir_objeto`, `ir_centro`, `ir_botin`, `noop`). Despues, del diario: si llega a esa casilla, si coge y si usa en los 240 tics siguientes.
  python3 banco_P7_28.py            -> P7_28_curiosidad.json
  python3 banco_P7_28.py --vida S_D_SLOT"""
import collections, copy, glob, json, math, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_28_tmp"); DIAS = range(16, 21)


def una(s, d, sl):
    os.environ["GEMV_P7_PIDE"] = "1"; os.environ["GEMV_P7_PIDE2"] = "1"; os.environ["GEMV_P7_NACE"] = "1"; os.environ["GEMV_OJOS"] = "0"
    import banco_P7_5 as B
    carp = os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P724_s{s}_d{d}_APRENDE_*"))[0])
    cuad = os.path.join(SAL, f"cuad_s{s}_d{d}_{sl}"); shutil.rmtree(cuad, ignore_errors=True); os.makedirs(cuad)
    for q in (10, 11): shutil.copy(os.path.join(AQUI, "P7_24_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}.json"), os.path.join(cuad, f"cuaderno_P7_{q}.json"))
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS["APRENDE"].get(k, "0")
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import mide_P6_29 as M
    from alma import decisor_zs as D
    import descubre_P7 as X, pide_P7 as J, nace_P7_23 as N
    _ap0 = X.aplica; ULT = {}
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); J.aplica(clase, registra); N.aplica(clase, registra)
        # la captura de los candidatos va DESPUES de los enganches de nacer: `nace_P7_23.aplica` envuelve D.candidatos y es quien pone `ir_curioso`
        _oc = D.candidatos
        def _cands(obs, mundo, mem, tick, bloqueos=None):
            out = _oc(obs, mundo, mem, tick, bloqueos); ULT[tick] = {n_: r_ for n_, r_ in out if n_ in ("ir_curioso", "ir_objeto")}; return out
        D.candidatos = _cands
        return h
    X.aplica = _aplica
    # el diario, para el seguimiento: posicion y zurron por tic
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{sl}.art.log"))[0]; DIA = {}
    for line in open(f, errors="replace"):
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") == "tick" and r.get("phase") == "live":
            n = collections.Counter()
            for s_ in (r.get("pack") or []):
                if s_: n[s_.get("id")] += int(s_.get("n") or 1)
            DIA[r["tick"]] = {"pos": tuple(r["pos"]), "n": {"first_aid": n.get("first_aid", 0), "rations": n.get("rations", 0)}, "canal": any(e.get("id") == "channeling" for e in (r.get("effects") or []))}
    REG = []; CNT = collections.Counter(); _d0 = M._DEC0
    def _dec(obs, mundo, mem, tick, bloqueos=None):
        ac, ra = _d0(obs, mundo, mem, tick, bloqueos); el = str(ra.get("elegido") or ""); you = obs.get("you") or {}; CNT["tics"] += 1
        if (you.get("move_ready_in") or 0) != 0: return ac, ra
        CNT["listos"] += 1
        if el != "ir_curioso": return ac, ra
        CNT["ir_curioso_listo"] += 1; pos = tuple(you.get("pos") or (0, 0)); c = X.ESTADO["cuaderno"]
        ign = {o: (float(c.ignorancia(o)) if c is not None else 1.0) for o in N.consumibles(mundo)}; ali = {o: N.alivio_clase(obs, mundo, o) for o in N.consumibles(mundo)}
        rec = ULT.get(tick, {}).get("ir_curioso") or {}; dest = tuple(rec.get("destino") or ()); clase = (rec.get("recoger") or [None])[0]
        fl = ((ra.get("ahora") or {}).get("filas") or {}); mc = fl.get("R-CURIOSIDAD"); Mc = (mc.get("M") if isinstance(mc, dict) else mc)
        if Mc is None:
            t_, F_ = X.ESTADO.get("calma_cache", (None, None))
            if t_ != tick: F_ = N.A.filas(obs, mundo, mem, tick)
            Mc = N.curiosidad_M(obs, mundo, F_)[0]
        # la casilla del destino sigue teniendo la cosa ahora? (a la vista) o es solo recuerdo (`mem.objetos_vistos`)
        vis_ = {tuple(it.get("pos") or ()) for it in ((obs.get("visible") or {}).get("items") or []) if it.get("pos")}
        REG.append({"t": tick, "pos": list(pos), "destino": list(dest), "clase": clase, "destino_a_la_vista": (dest in vis_) if dest else None, "dist": (max(abs(dest[0] - pos[0]), abs(dest[1] - pos[1])) if dest else None), "dentro": X.situacion(mundo, pos, tick) == "dentro",
                    "ignorancia": ign, "alivio": ali, "M_curiosidad": Mc, "k_botiquin": round(X.k_ganas(mundo), 4), "k_racion": round(N.k_de(mundo, N.racion(mundo), pos, tick), 4), "zurron": {o: N.unidades_de(you, mundo, o) for o in N.consumibles(mundo)}, "hp": you.get("hp"),
                    "recuerdos": {o: len(c.recuerdos_de(o)) for o in N.consumibles(mundo)} if c is not None else None, "d": {k_: (v_["d"] if isinstance(v_, dict) else v_) for k_, v_ in (ra.get("candidatos") or {}).items() if k_ in ("ir_curioso", "ir_objeto", "ir_centro", "ir_botin", "ir_pareja", "noop", "coger")},
                    "ir_objeto_destino": list((ULT.get(tick, {}).get("ir_objeto") or {}).get("destino") or ())})
        return ac, ra
    M._DEC0 = _dec
    r = B.vida(carp, sl, "APRENDE", cuad)
    # seguimiento en el diario: llega a la casilla / coge / usa en los 240 tics siguientes
    ticks = sorted(DIA)
    for x in REG:
        sig = [t for t in ticks if x["t"] < t <= x["t"] + 240]; d0 = DIA[x["t"]]; dest = tuple(x["destino"])
        x["llega"] = any(DIA[t]["pos"] == dest for t in sig) if dest else None
        x["coge"] = any(DIA[t]["n"][o] > d0["n"][o] for t in sig for o in ("first_aid", "rations"))
        x["usa"] = any(DIA[t]["canal"] for t in sig)
    return {"serie": s, "dia": d, "slot": sl, "tics": r["tics"], "fidelidad": r["fidelidad"], "cuenta": dict(CNT), "registros": REG}


if __name__ == "__main__":
    os.makedirs(SAL, exist_ok=True)
    if "--vida" in sys.argv:
        s, d, sl = (int(x) for x in sys.argv[sys.argv.index("--vida") + 1].split("_")); json.dump(una(s, d, sl), open(os.path.join(SAL, f"dec_{s}_{d}_{sl}.json"), "w"), ensure_ascii=False)
    else:
        claves = [f"{s}_{d}_{sl}" for s in (1, 2) for d in DIAS for sl in (10, 11)]
        def lanza(k):
            f = os.path.join(SAL, f"dec_{k}.json")
            if os.path.exists(f): os.remove(f)
            r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", k], capture_output=True, text=True, timeout=7200)
            return json.load(open(f)) if os.path.exists(f) else {"clave": k, "error": (r.stderr or r.stdout)[-600:]}
        with ThreadPoolExecutor(4) as ex: R = list(ex.map(lanza, claves))
        err = [r for r in R if r.get("error")]
        if err: print("ERRORES", len(err), [e["clave"] for e in err], err[0]["error"][-300:])
        json.dump([r for r in R if not r.get("error")], open(os.path.join(AQUI, "P7_28_curiosidad.json"), "w"), ensure_ascii=False)
        fid = collections.Counter()
        for r in R:
            for k_, n in (r.get("fidelidad") or {}).items(): fid[k_] += n
        print("vidas", len(R) - len(err), "· fidelidad", dict(fid), "· ir_curioso con el paso listo", sum(len(r.get("registros", [])) for r in R))
