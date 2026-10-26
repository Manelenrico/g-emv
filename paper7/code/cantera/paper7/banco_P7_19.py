"""[P7-19] EL BANCO DE "lo dado no esta entregado mientras quien lo dio lo pisa" (un subproceso por vida; sin partidas ni llamadas). Sobre P7-14b,
con el pedido de P7-17 (GEMV_P7_PIDE2=1) y el arreglo; cada criatura oye los partes que su hermano habria emitido con esa regla (los del banco de
P7-17, `_P7_16_tmp/p1_*.json`). La replica sigue el diario: describe el primer tic en que la decision cambia, no lo que habria pasado despues.
  --todo    las 320 vidas. F2: tras cada regalo de la replica, que elige quien regalo en los tics siguientes, hasta el primero en que elige irse
            (o 720 tics, o deja la casilla en el diario). F4: en cada tic con alguna marca de regalo viva, se decide tambien con el arreglo
            apagado (sobre copias) y se apunta si la eleccion difiere, y si la criatura esta o no sobre su regalo. -> P7_19_todo.json
  --f3      las 40 escenas de P7-18: la vida del que pedia; desde el tic siguiente a aquel en que quien regalo se apartaria (de --todo), con ese
            hermano puesto en la casilla a la que iria, lo que elige el que pedia en el primer tic en que tiene mas que `noop`. -> P7_19_f3.json"""
import collections, copy, glob, json, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_19_tmp"); P1 = os.path.join(AQUI, "_P7_16_tmp"); _Q = re.compile(r" q[A-Za-z]+$")
BZ = {"ESPERANZA": "ESPERANZA", "BORRADO": "BORRADO", "APRENDE": "APRENDE", "TECHO": "TECHO_SITIO"}
DIR = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0), "NE": (1, -1), "NW": (-1, -1), "SE": (1, 1), "SW": (-1, 1)}
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
def vida(carp, slot, brazo, cuad, partes, f3=None):
    import banco_P7_5 as B
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS[brazo].get(k, "0")
    os.environ["GEMV_P7_PIDE"] = "1"; os.environ["GEMV_P7_PIDE2"] = "1"; os.environ["GEMV_P7_PISO"] = "1"; os.environ["CUADERNO_DIR"] = cuad; os.environ["GEMV_OJOS"] = "0"
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import mide_P6_29 as M
    import descubre_P7 as X
    import pide_P7 as J
    from alma import decisor_zs as D
    HJ = {}; _ap0 = X.aplica
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); HJ.update(J.aplica(clase, registra)); return h
    X.aplica = _aplica
    PT = json.load(open(partes)) if partes and os.path.exists(partes) else {}; _o0 = M.obs_de; herm = 21 - slot
    def _obs(r, sp, it):
        o = _o0(r, sp, it); chat = o.get("chat") or []
        if chat and PT:
            nuevo = []
            for m in chat:
                tx = m.get("text") or ""; mm = re.match(r"^E1 P(\d+) t(\d+) ", tx); nv = PT.get(mm.group(2)) if mm else None
                if m.get("from") == herm and m.get("channel") == "team" and nv and nv != tx and _Q.sub("", nv) == _Q.sub("", tx): m = dict(m, text=nv)
                nuevo.append(m)
            o = dict(o, chat=nuevo)
        return o
    M.obs_de = _obs
    CNT = collections.Counter(); DIF = []; SEG = []; abiertos = []; F3 = []; hechos = set(); _d0 = M._DEC0
    pend = [dict(x, hecho=False) for x in (json.load(open(f3)) if f3 else [])]
    def _dec(obs, mundo, mem, tick, bloqueos=None):
        if tick in hechos: return _d0(obs, mundo, mem, tick, bloqueos)          # preguntas hipoteticas del propio pedido (hacer sitio): no se cuentan
        hechos.add(tick); you = obs.get("you") or {}; pos = tuple(you.get("pos") or ()); kid = X.kit(mundo); el2 = None
        marcas = set(J.ESTADO.get("mis_regalos") or ())
        if marcas:
            CNT["tics_con_marca"] += 1; J.ESTADO["piso_apagado"] = True
            try: el2 = _d0(copy.deepcopy(obs), mundo, copy.deepcopy(mem), tick, copy.deepcopy(bloqueos))[1].get("elegido")
            finally: J.ESTADO["piso_apagado"] = False
        for x in pend:                                                              # F3: el que pedia, con el hermano ya apartado
            if x["hecho"] or tick < x["desde"] or tick > x["hasta"]: continue
            gp = tuple(x["regalo"]); q = tuple(x["a_donde"]); ob2 = copy.deepcopy(obs); mem2 = copy.deepcopy(mem); movido = False
            for a_ in ((ob2.get("visible") or {}).get("agents") or []):
                if a_.get("slot") == mundo.teammate_slot and tuple(a_.get("pos") or ()) == gp: a_["pos"] = list(q); movido = True
            if getattr(mem2, "pareja_pos", None) is not None and tuple(mem2.pareja_pos) == gp: mem2.pareja_pos = q
            ac_h, ra_h = _d0(ob2, mundo, mem2, tick, copy.deepcopy(bloqueos)); C = ra_h.get("candidatos") or {}
            if len(C) <= 1 and tick < x["hasta"]: continue                          # solo `noop` (paso en enfriamiento): se mira el tic siguiente
            cs = [(n_, r_.get("tipo"), list(r_.get("destino")) if r_.get("destino") else None) for n_, r_ in D.candidatos(copy.deepcopy(ob2), mundo, copy.deepcopy(mem2), tick, copy.deepcopy(bloqueos))]
            el = str(ra_h.get("elegido") or ""); dd = {k_: (v_["d"] if isinstance(v_, dict) else v_) for k_, v_ in C.items()}; hacia = [n_ for n_, tp, de in cs if tp == "ir" and de and tuple(de) == gp and n_ in ("ir_objeto", "ir_curioso")]
            u = DIR.get((ac_h or {}).get("dir") or "") if (ac_h or {}).get("do") == "move" else None; np_ = (pos[0] + u[0], pos[1] + u[1]) if u else pos
            vis_k = any(it.get("id") == kid and tuple(it.get("pos") or ()) == gp for it in ((obs.get("visible") or {}).get("items") or []))
            F3.append({"vida_del_que_dio": x["vida_del_que_dio"], "t_regalo": x["t_regalo"], "t": tick, "regalo": list(gp), "pos": list(pos), "dist": cheb(pos, gp), "hermano_movido": movido, "ve_el_botiquin": vis_k, "botiquines": X.kits_en(you, mundo), "cabe": J.cabe(you, mundo),
                       "n_cand": len(C), "elegido": el, "accion": ac_h, "hay_coger": "coger" in C, "candidatos_hacia_el_regalo": hacia, "elige_ir_a_por_el": el in hacia or el == "coger", "el_paso_va_hacia_el": bool(u and cheb(np_, gp) < cheb(pos, gp)),
                       "el_paso_entra_en_la_casilla": bool(u and np_ == gp), "d_elegido": dd.get(el), "d_del_mejor_hacia_el": (min(dd[h] for h in hacia if h in dd) if any(h in dd for h in hacia) else None), "pedia": bool(J.ESTADO.get("pedia"))})
            x["hecho"] = True
        ac, ra = _d0(obs, mundo, mem, tick, bloqueos); el = str(ra.get("elegido") or ""); C = ra.get("candidatos") or {}
        if marcas and el2 != el:
            DIF.append({"t": tick, "con_el_arreglo": el, "sin_el_arreglo": el2, "sobre_su_regalo": pos in marcas, "botiquin_en_su_casilla": any(it.get("id") == kid and tuple(it.get("pos") or ()) == pos for it in ((obs.get("visible") or {}).get("items") or [])), "n_cand": len(C)})
        for sg in list(abiertos):                                                   # F2: tras el regalo, hasta que elige irse
            if pos != tuple(sg["pos"]): sg["fin"] = "en el diario ya no esta en la casilla"; abiertos.remove(sg); continue
            dd = {k_: (v_["d"] if isinstance(v_, dict) else v_) for k_, v_ in C.items()}
            if len(C) <= 1: sg["tics_solo_noop"] += 1
            elif el == "noop" or el.startswith("soltar_"):
                sg["tics_quieto_pudiendo"] += 1
                if len(sg["quieto_ejemplos"]) < 3: sg["quieto_ejemplos"].append({"t": tick, "elegido": el, "d": dict(sorted(dd.items(), key=lambda kv: kv[1])[:4])})
            else:
                u = DIR.get((ac or {}).get("dir") or "") if (ac or {}).get("do") == "move" else None
                sg.update({"se_aparta_en": tick, "tics_hasta_apartarse": tick - sg["t"], "elige": el, "accion": ac, "a_donde": ([pos[0] + u[0], pos[1] + u[1]] if u else None), "d_elegido": dd.get(el), "d_noop": dd.get("noop"), "elegia_sin_el_arreglo": el2, "fin": "se aparta"}); abiertos.remove(sg); continue
            if tick - sg["t"] >= 720: sg["fin"] = "720 tics sin apartarse"; abiertos.remove(sg)
        if el.startswith("soltar_" + kid):
            sg = {"t": tick, "pos": list(pos), "hermano_pide": J.hermano_pide(mundo, mem, tick), "tics_solo_noop": 0, "tics_quieto_pudiendo": 0, "quieto_ejemplos": [], "fin": None}; SEG.append(sg); abiertos.append(sg)
        CNT["tics"] += 1
        return ac, ra
    M._DEC0 = _dec
    r = B.vida(carp, slot, brazo, cuad)
    return {"carp": carp, "slot": slot, "brazo": brazo, "hecho_J": HJ, "fidelidad": r["fidelidad"], "errores": len(r["errores"]), "cuenta": dict(CNT), "distintos": DIF, "seguimientos": SEG, "f3": F3}
def cuaderno_de(nombre, v):
    cu = os.path.join(SAL, "cuad_" + nombre); shutil.rmtree(cu, ignore_errors=True); os.makedirs(cu)
    if v["brazo"] == "APRENDE" and v["dia"] > 1:
        for q in (10, 11): shutil.copy(os.path.join(AQUI, "P7_14b_res", f"cuaderno_s{v['serie']}_d{v['dia'] - 1}_APRENDE_{q}.json"), os.path.join(cu, f"cuaderno_P7_{q}.json"))
    return cu
def lanza(V, k, pref, f3=None):
    v = V[k]; kh = f"s{v['serie']}_d{v['dia']}_{v['brazo']}_{21 - v['slot']}"; carp = os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P714b_s{v['serie']}_d{v['dia']}_{v['brazo']}_*"))[0])
    pf = os.path.join(SAL, f"partes_{kh}.json"); src = os.path.join(P1, f"p1_{kh}.json")
    json.dump({str(p["tick"]): p["texto"] for p in json.load(open(src))["pidos"]} if os.path.exists(src) else {}, open(pf, "w"))
    sal = os.path.join(SAL, f"{pref}_{k}.json")
    if os.path.exists(sal): os.remove(sal)
    cmd = [sys.executable, os.path.abspath(__file__), "--vida", carp, str(v["slot"]), "--brazo", BZ[v["brazo"]], "--cuadernos", cuaderno_de(pref + "_" + k, v), "--partes", pf, "--salida", sal] + (["--f3", f3] if f3 else [])
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    return k, (json.load(open(sal)) if os.path.exists(sal) else {"error": (r.stderr or r.stdout)[-600:]})
if __name__ == "__main__":
    a = sys.argv; os.makedirs(SAL, exist_ok=True)
    if "--vida" in a:
        i = a.index("--vida"); g = lambda k: a[a.index(k) + 1] if k in a else None
        json.dump(vida(a[i + 1], int(a[i + 2]), g("--brazo"), g("--cuadernos"), g("--partes"), g("--f3")), open(g("--salida"), "w"), ensure_ascii=False); sys.exit(0)
    V = json.load(open(os.path.join(AQUI, "P7_14b_vidas.json")))
    if "--todo" in a:
        with ThreadPoolExecutor(8) as ex: R = dict(ex.map(lambda k: lanza(V, k, "todo"), list(V)))
        err = [k for k, r in R.items() if r.get("error")]
        if err: print("ERRORES", len(err), err[0], R[err[0]]["error"][-500:])
        json.dump({k: dict(r, brazo_campo=V[k]["brazo"]) for k, r in R.items() if not r.get("error")}, open(os.path.join(AQUI, "P7_19_todo.json"), "w"), ensure_ascii=False, indent=0)
        ok = [r for r in R.values() if not r.get("error")]; fid = collections.Counter()
        for r in ok: fid.update(r["fidelidad"])
        print("vidas", len(ok), "· fidelidad", dict(fid), "· tics", sum(r["cuenta"].get("tics", 0) for r in ok), "· con marca", sum(r["cuenta"].get("tics_con_marca", 0) for r in ok), "· distintos", sum(len(r["distintos"]) for r in ok), "· regalos de la replica", sum(len(r["seguimientos"]) for r in ok), dict(collections.Counter(s_["fin"] for r in ok for s_ in r["seguimientos"])))
    elif "--f3" in a:
        T = json.load(open(os.path.join(AQUI, "P7_19_todo.json"))); E = json.load(open(os.path.join(AQUI, "P7_18_escenas.json")))["regalos"]; porh = collections.defaultdict(list); sin = []
        for g in E:
            sg = next((s_ for s_ in T[g["vida_del_que_dio"]]["seguimientos"] if abs(s_["t"] - (g["t0"] - 1)) <= 1 and s_["pos"] == g["pos"]), None)
            if not sg or sg.get("fin") != "se aparta" or not sg.get("a_donde"): sin.append({"vida_del_que_dio": g["vida_del_que_dio"], "t0": g["t0"], "por_que": ("no elige un paso sino `" + str(sg.get("elige")) + "`" if (sg and sg.get("fin") == "se aparta") else (sg or {}).get("fin") or "la replica no regala en ese tic")}); continue
            porh[g["hermano"]].append({"vida_del_que_dio": g["vida_del_que_dio"], "t_regalo": sg["t"], "regalo": g["pos"], "a_donde": sg["a_donde"], "desde": sg["se_aparta_en"] + 1, "hasta": sg["se_aparta_en"] + 1 + 240})
        def uno(kh):
            f = os.path.join(SAL, f"f3_in_{kh}.json"); json.dump(porh[kh], open(f, "w")); return lanza(V, kh, "f3", f3=f)
        with ThreadPoolExecutor(8) as ex: R = dict(ex.map(uno, list(porh)))
        err = [k for k, r in R.items() if r.get("error")]
        if err: print("ERRORES", len(err), err[0], R[err[0]]["error"][-500:])
        F3 = [x for r in R.values() for x in r.get("f3", [])]
        json.dump({"escenas": len(E), "sin_apartarse_en_F2": sin, "pedidas": sum(len(v) for v in porh.values()), "f3": F3}, open(os.path.join(AQUI, "P7_19_f3.json"), "w"), ensure_ascii=False, indent=1)
        print("escenas", len(E), "· sin apartarse en F2", len(sin), "· evaluadas", len(F3), dict(collections.Counter((x["elige_ir_a_por_el"], x["el_paso_va_hacia_el"]) for x in F3)))
