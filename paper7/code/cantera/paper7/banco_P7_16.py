"""[P7-16, parte B] EL BANCO DE PEDIR CORREGIDO, sobre las 320 vidas de P7-14b (un subproceso por vida; sin partidas ni llamadas). La replica sigue
el diario: dice que parte habria emitido cada criatura, en la vida que vivio, con el pedido corregido (GEMV_P7_PIDE2=1), y que elige quien regalo.
  Pase 1: cada vida, con su brazo, su cuaderno y el pedido corregido: el parte de cada emision (registro `P7_pido`), comparado con el del campo.
  Pase 2: la vida de quien hizo cada uno de los regalos del campo, oyendo ahora los partes corregidos del hermano: en el tic de cada regalo, si el
          ultimo parte fresco del hermano pedia y que elige la replica.
  python3 banco_P7_16.py -> P7_16_pedir.json"""
import collections, glob, json, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_16_tmp"); _Q = re.compile(r" q[A-Za-z]+$")
def vida(carp, slot, brazo, cuad, partes=None, tics=None):
    import banco_P7_5 as B
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS[brazo].get(k, "0")
    os.environ["GEMV_P7_PIDE"] = "1"; os.environ["GEMV_P7_PIDE2"] = "1"; os.environ["CUADERNO_DIR"] = cuad; os.environ["GEMV_OJOS"] = "0"
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import mide_P6_29 as M
    import descubre_P7 as X
    import pide_P7 as J
    PIDOS = []; HJ = {}; _ap0 = X.aplica
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); HJ.update(J.aplica(clase, lambda r: (PIDOS.append(r) if r.get("k") == "P7_pido" else None, registra(r) if registra else None))); return h
    X.aplica = _aplica; cambiados = [0]
    if partes:
        PT = json.load(open(partes)); _o0 = M.obs_de; herm = 21 - slot
        def _obs(r, sp, it):
            o = _o0(r, sp, it); chat = o.get("chat") or []
            if chat:
                nuevo = []
                for m in chat:
                    tx = m.get("text") or ""; mm = re.match(r"^E1 P(\d+) t(\d+) ", tx); nv = PT.get(mm.group(2)) if mm else None
                    if m.get("from") == herm and m.get("channel") == "team" and nv and nv != tx and _Q.sub("", nv) == _Q.sub("", tx): m = dict(m, text=nv); cambiados[0] += 1
                    nuevo.append(m)
                o = dict(o, chat=nuevo)
            return o
        M.obs_de = _obs
    REG = {}
    if tics:
        TICS = set(json.load(open(tics))); _d0 = M._DEC0
        def _dec(obs, mundo, mem, tick, bloqueos=None):
            ac, ra = _d0(obs, mundo, mem, tick, bloqueos)
            if tick in TICS and tick not in REG:           # solo la decision de verdad (la primera del tic); las preguntas hipoteticas del pedido no
                REG[tick] = {"elegido": ra.get("elegido"), "hermano_pide": J.hermano_pide(mundo, mem, tick)}
            return ac, ra
        M._DEC0 = _dec
    r = B.vida(carp, slot, brazo, cuad)
    return {"carp": carp, "slot": slot, "brazo": brazo, "hecho_J": HJ, "tics": r["tics"], "fidelidad": r["fidelidad"], "errores": len(r["errores"]), "pidos": PIDOS, "partes_cambiados": cambiados[0], "en_tics": {str(t): REG.get(t) for t in sorted(REG)}}
def lanza(carp, slot, brazo, cuad, salida, partes=None, tics=None):
    if os.path.exists(salida): os.remove(salida)
    cmd = [sys.executable, os.path.abspath(__file__), "--vida", carp, str(slot), "--brazo", brazo, "--cuadernos", cuad, "--salida", salida] + (["--partes", partes] if partes else []) + (["--tics", tics] if tics else [])
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    return json.load(open(salida)) if os.path.exists(salida) else {"error": (r.stderr or r.stdout)[-600:]}
def cuaderno_de(nombre, brazo, s, d):
    cu = os.path.join(SAL, "cuad_" + nombre); shutil.rmtree(cu, ignore_errors=True); os.makedirs(cu)
    if brazo == "APRENDE" and d > 1:
        for q in (10, 11): shutil.copy(os.path.join(AQUI, "P7_14b_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}.json"), os.path.join(cu, f"cuaderno_P7_{q}.json"))
    return cu
BZ = {"ESPERANZA": "ESPERANZA", "BORRADO": "BORRADO", "APRENDE": "APRENDE", "TECHO": "TECHO_SITIO"}
if __name__ == "__main__":
    a = sys.argv; os.makedirs(SAL, exist_ok=True)
    if "--vida" in a:
        i = a.index("--vida"); g = lambda k: a[a.index(k) + 1] if k in a else None
        json.dump(vida(a[i + 1], int(a[i + 2]), g("--brazo"), g("--cuadernos"), g("--partes"), g("--tics")), open(g("--salida"), "w"), ensure_ascii=False); sys.exit(0)
    V = json.load(open(os.path.join(AQUI, "P7_14b_vidas.json"))); carp_de = lambda v: os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P714b_s{v['serie']}_d{v['dia']}_{v['brazo']}_*"))[0])
    def p1(k):
        v = V[k]; return k, lanza(carp_de(v), v["slot"], BZ[v["brazo"]], cuaderno_de("p1_" + k, v["brazo"], v["serie"], v["dia"]), os.path.join(SAL, f"p1_{k}.json"))
    with ThreadPoolExecutor(8) as ex: P1 = dict(ex.map(p1, list(V)))
    err = [k for k, r in P1.items() if r.get("error")]
    if err: sys.exit("ERROR pase 1 " + err[0] + " " + P1[err[0]]["error"][-400:])
    print("pase 1:", len(P1), "vidas", flush=True)
    def p2(k):
        v = V[k]; kh = f"s{v['serie']}_d{v['dia']}_{v['brazo']}_{21 - v['slot']}"
        pf = os.path.join(SAL, f"partes_{kh}.json"); json.dump({str(p["tick"]): p["texto"] for p in P1[kh]["pidos"]} if kh in P1 else {}, open(pf, "w"))
        tf = os.path.join(SAL, f"tics_{k}.json"); json.dump(sorted({g["t_dec"] for g in v["regala"]}), open(tf, "w"))
        return k, lanza(carp_de(v), v["slot"], BZ[v["brazo"]], cuaderno_de("p2_" + k, v["brazo"], v["serie"], v["dia"]), os.path.join(SAL, f"p2_{k}.json"), partes=pf, tics=tf)
    with ThreadPoolExecutor(8) as ex: P2 = dict(ex.map(p2, [k for k, v in V.items() if v["regala"]]))
    err = [k for k, r in P2.items() if r.get("error")]
    if err: sys.exit("ERROR pase 2 " + err[0] + " " + P2[err[0]]["error"][-400:])
    def campo_pidos(v):
        f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp_de(v), f"*policy_agent_{v['slot']}.art.log"))[0]; return [json.loads(l) for l in open(f) if '"P7_pido"' in l[:20]]
    OUT = {"por_vida": {}, "regalos": []}; fid1 = collections.Counter(); fid2 = collections.Counter()
    for k, r in P1.items():
        v = V[k]; fid1.update(r["fidelidad"]); cp = {p["tick"]: p for p in campo_pidos(v)}; nv = {p["tick"]: p for p in r["pidos"]}; com = sorted(set(cp) & set(nv))
        OUT["por_vida"][k] = {"brazo": v["brazo"], "partes": len(com), "campo_con_pedido": sum(1 for t in com if cp[t]["pide"]), "nuevo_con_pedido": sum(1 for t in com if nv[t]["pide"]),
                              "pedia_y_ya_no": sum(1 for t in com if cp[t]["pide"] and not nv[t]["pide"]), "no_pedia_y_ahora_si": sum(1 for t in com if not cp[t]["pide"] and nv[t]["pide"]),
                              "campo_abiertos": sum(1 for t in com if cp[t]["abre"]), "nuevo_abiertos": sum(1 for p in r["pidos"] if p["abre"]), "campo_cierres": dict(collections.Counter(cp[t]["cierra"] for t in com if cp[t].get("cierra"))),
                              "nuevo_cierres": dict(collections.Counter(p["cierra"] for p in r["pidos"] if p.get("cierra"))), "nuevo_por_hacer_sitio": sum(1 for p in r["pidos"] if p["pide"] and p.get("haria_sitio")),
                              "campo_pedia_con_la_vida_entera": None, "campo_pedia_sin_hueco": sum(1 for t in com if cp[t]["pide"] and nv[t].get("hueco") is False), "campo_pedia_sin_faltarle_vida": sum(1 for t in com if cp[t]["pide"] and nv[t].get("falta_vida") is False)}
    for k, r in P2.items():
        v = V[k]; fid2.update(r["fidelidad"])
        for g in v["regala"]:
            e = r["en_tics"].get(str(g["t_dec"])) or {}
            OUT["regalos"].append({"vida": k, "brazo": v["brazo"], "t": g["t_dec"], "destino_en_el_campo": g["destino"], "hermano_pide_corregido": e.get("hermano_pide"), "elegido_replica": e.get("elegido"), "sigue_regalando": str(e.get("elegido")).startswith("soltar_first_aid")})
    OUT["fidelidad_pase1"] = dict(fid1); OUT["fidelidad_pase2"] = dict(fid2); OUT["partes_cambiados_pase2"] = sum(r["partes_cambiados"] for r in P2.values())
    json.dump(OUT, open(os.path.join(AQUI, "P7_16_pedir.json"), "w"), ensure_ascii=False, indent=0)
    G = OUT["regalos"]; print("regalos", len(G), "siguen", sum(1 for g in G if g["sigue_regalando"]), "· de los que volvian a quien los dio (APRENDE):", sum(1 for g in G if g["brazo"] == "APRENDE" and g["destino_en_el_campo"] == "lo recoge el mismo"), "siguen", sum(1 for g in G if g["brazo"] == "APRENDE" and g["destino_en_el_campo"] == "lo recoge el mismo" and g["sigue_regalando"]), "· fidelidad", dict(fid1), dict(fid2))
