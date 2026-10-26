"""[P7-18] POR QUE NO COGE LO QUE PIDIO. Los regalos de P7-14b que, con la regla de pedir de P7-17, se seguirian haciendo y que en el campo volvieron a
quien los dio (`P7_17_pedir.json`: sigue regalando y destino "lo recoge el mismo"; ahi estan los 23 de TECHO). Para cada uno, la vida del hermano
que pedia se replica TAL COMO SE JUGO (P7-14b: pedir de P7-13, ojos apagados; un subproceso por vida; sin partidas ni llamadas), y en cada tic, entre
el regalo y la recogida, en que esta a dos casillas o menos (Chebyshev) del botiquin regalado, se apunta lo que el cuerpo tenia delante:
  si veia el botiquin en esa casilla; su zurron; los candidatos que `candidatos` le daba (nombre, tipo, destino y lo que iria a recoger) y la d de
  cada uno en `decide`; cual eligio; a que objeto iria `_mejor_objeto` y con que promesa; si la casilla del regalo esta en su memoria de objetos
  vistos; el rival mas cercano. Del diario: si el arreglo del seis escondio `coger` ese tic (registro `llena8`).
  python3 banco_P7_18.py -> P7_18_escenas.json"""
import collections, copy, glob, json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_18_tmp"); BZ = {"ESPERANZA": "ESPERANZA", "BORRADO": "BORRADO", "APRENDE": "APRENDE", "TECHO": "TECHO_SITIO"}
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
def vida(carp, slot, brazo, cuad, ventanas):
    import banco_P7_5 as B
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS[brazo].get(k, "0")
    os.environ["GEMV_P7_PIDE"] = "1"; os.environ["GEMV_P7_PIDE2"] = "0"; os.environ["CUADERNO_DIR"] = cuad; os.environ["GEMV_OJOS"] = "0"
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import mide_P6_29 as M
    import descubre_P7 as X
    import pide_P7 as J
    from alma import decisor_zs as D
    _ap0 = X.aplica
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); J.aplica(clase, registra); return h
    X.aplica = _aplica
    V = [(v["t0"], v["t1"], tuple(v["pos"])) for v in json.load(open(ventanas))]; REG = []; _d0 = M._DEC0; hechos = set()
    def _dec(obs, mundo, mem, tick, bloqueos=None):
        you = obs.get("you") or {}; pos = tuple(you.get("pos") or ()); cerca = [p for t0, t1, p in V if t0 <= tick <= t1 and cheb(pos, p) <= 2]
        pre = None
        if cerca and tick not in hechos:
            hechos.add(tick); kid = X.kit(mundo); gp = cerca[0]; vis = obs.get("visible") or {}
            try: cs = [(n, r.get("tipo"), list(r.get("destino")) if r.get("destino") else None, (r.get("recoger") or [None])[0] if r.get("recoger") else ((r.get("item") or {}).get("id") if isinstance(r.get("item"), dict) else r.get("item"))) for n, r in D.candidatos(copy.deepcopy(obs), mundo, copy.deepcopy(mem), tick, copy.deepcopy(bloqueos))]
            except Exception as ex: cs = [("ERROR", repr(ex)[:80], None, None)]
            try: mo = D._mejor_objeto(pos, mundo, copy.deepcopy(mem), obs, tick)
            except Exception: mo = None
            ov = getattr(mem, "objetos_vistos", None) or {}
            riv = [cheb(pos, tuple(a["pos"])) for a in (vis.get("agents") or []) if a.get("pos") and a.get("slot") not in (mundo.slot, mundo.teammate_slot)]
            pre = {"t": tick, "pos": list(pos), "regalo": list(gp), "dist": cheb(pos, gp), "hp": you.get("hp"), "zurron": [(s or {}).get("id") for s in (you.get("pack") or [])], "botiquines": X.kits_en(you, mundo),
                   "ve_el_botiquin_en_esa_casilla": any(it.get("id") == kid and tuple(it.get("pos") or ()) == gp for it in (vis.get("items") or [])), "otros_botiquines_a_la_vista": sum(1 for it in (vis.get("items") or []) if it.get("id") == kid and tuple(it.get("pos") or ()) != gp),
                   "candidatos_de_candidatos": cs, "mejor_objeto": (list(mo) if mo else None), "mejor_objeto_es_el_regalo": (tuple(mo) == gp if mo else False), "que_es_el_mejor_objeto": ((ov.get(tuple(mo)) or [None])[0] if mo else None),
                   "regalo_en_objetos_vistos": gp in ov, "regalo_en_mis_cedidos": gp in (getattr(mem, "cedidos", None) or {}), "promesa_del_botiquin": round(float(D._promesa(obs, mundo, mem, tick, kid)), 5),
                   "cabe": J.cabe(you, mundo), "rival_mas_cercano": (min(riv) if riv else None), "en_canal": any(e.get("id") == "channeling" for e in (you.get("effects") or [])), "pedia": bool(J.ESTADO.get("pedia"))}
        ac, ra = _d0(obs, mundo, mem, tick, bloqueos)
        if pre is not None:
            C = ra.get("candidatos") or {}; pre["elegido"] = ra.get("elegido"); pre["d"] = {k_: (v_["d"] if isinstance(v_, dict) else v_) for k_, v_ in C.items()}
            el = C.get(ra.get("elegido")); pre["filas_del_elegido"] = (el.get("filas") if isinstance(el, dict) else None)
            pre["filas_de_ir_a_por_el"] = {k_: v_.get("filas") for k_, v_ in C.items() if isinstance(v_, dict) and k_ in ("ir_objeto", "ir_curioso", "coger")}
            REG.append(pre)
        return ac, ra
    M._DEC0 = _dec
    r = B.vida(carp, slot, brazo, cuad)
    return {"carp": carp, "slot": slot, "brazo": brazo, "fidelidad": r["fidelidad"], "errores": len(r["errores"]), "tics": REG}
if __name__ == "__main__":
    a = sys.argv; os.makedirs(SAL, exist_ok=True)
    if "--vida" in a:
        i = a.index("--vida"); g = lambda k: a[a.index(k) + 1]
        json.dump(vida(a[i + 1], int(a[i + 2]), g("--brazo"), g("--cuadernos"), g("--ventanas")), open(g("--salida"), "w"), ensure_ascii=False); sys.exit(0)
    V = json.load(open(os.path.join(AQUI, "P7_14b_vidas.json"))); P = json.load(open(os.path.join(AQUI, "P7_17_pedir.json")))
    sel = {(g["vida"], g["t"]) for g in P["regalos"] if g["sigue_regalando"] and g["destino_en_el_campo"] == "lo recoge el mismo"}
    porh = collections.defaultdict(list); regalos = []
    for k, v in V.items():
        for g in v["regala"]:
            if (k, g["t_dec"]) in sel:
                kh = f"s{v['serie']}_d{v['dia']}_{v['brazo']}_{21 - v['slot']}"; w = {"t0": g["t"], "t1": g["t"] + g["tics_hasta_recogerlo"], "pos": g["pos"], "vida_del_que_dio": k, "brazo": v["brazo"]}
                porh[kh].append(w); regalos.append({**w, "hermano": kh})
    def lanza(kh):
        v = V[kh]; carp = os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P714b_s{v['serie']}_d{v['dia']}_{v['brazo']}_*"))[0])
        cu = os.path.join(SAL, "cuad_" + kh); shutil.rmtree(cu, ignore_errors=True); os.makedirs(cu)
        if v["brazo"] == "APRENDE" and v["dia"] > 1:
            for q in (10, 11): shutil.copy(os.path.join(AQUI, "P7_14b_res", f"cuaderno_s{v['serie']}_d{v['dia'] - 1}_APRENDE_{q}.json"), os.path.join(cu, f"cuaderno_P7_{q}.json"))
        vf = os.path.join(SAL, f"vent_{kh}.json"); json.dump(porh[kh], open(vf, "w")); sal = os.path.join(SAL, f"esc_{kh}.json")
        if os.path.exists(sal): os.remove(sal)
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(v["slot"]), "--brazo", BZ[v["brazo"]], "--cuadernos", cu, "--ventanas", vf, "--salida", sal], capture_output=True, text=True, timeout=3600)
        o = json.load(open(sal)) if os.path.exists(sal) else {"error": (r.stderr or r.stdout)[-500:]}
        # del diario: los tics en que el arreglo del seis escondio `coger`
        f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{v['slot']}.art.log"))[0]; ll = {}
        for line in open(f):
            if '"llena8"' in line[:16]:
                x = json.loads(line); ll[x.get("tick")] = x.get("motivo")
        for t in o.get("tics", []): t["coger_escondido"] = ll.get(t["t"])
        return kh, o
    with ThreadPoolExecutor(8) as ex: R = dict(ex.map(lanza, list(porh)))
    err = [k for k, r in R.items() if r.get("error")]
    if err: print("ERRORES", len(err), err[0], R[err[0]]["error"][-400:])
    fid = collections.Counter()
    for r in R.values():
        for k_, n in (r.get("fidelidad") or {}).items(): fid[k_] += n
    json.dump({"regalos": regalos, "hermanos": R}, open(os.path.join(AQUI, "P7_18_escenas.json"), "w"), ensure_ascii=False, indent=0)
    print("regalos", len(regalos), collections.Counter(g["brazo"] for g in regalos), "· vidas replicadas", len(R), "· fidelidad", dict(fid), "· tics cerca", sum(len(r.get("tics", [])) for r in R.values()))
