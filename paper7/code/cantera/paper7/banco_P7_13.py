"""[P7-13] EL BANCO DE PEDIR Y DEJAR DE PEDIR. Molde de `banco_P7_5.py` (replica de un diario por un cable falso), UN SUBPROCESO POR VIDA, sin
partidas ni llamadas. La politica replicada es la de P7-13: `descubre_P7.aplica` y despues `pide_P7.aplica`.
  --vida CARP SLOT --brazo B --cuadernos DIR --pide 0|1 --salida F [--partes F] [--tics F]     (un proceso: una vida)
  --f1 [--hilos N]   F1: los 80 diarios de A4 con `apagado` y con `TECHO`, pedir APAGADO: la eleccion de la replica contra el diario -> P7_13_F1.json
  --f2 [--hilos N]   F2: los 171 regalos de APRENDE en P7-10. Pase 1: se replican con pedir encendido las vidas de las partidas con algun regalo
                     (las dos criaturas) y se guarda el parte que cada una habria emitido, con su pedido. Pase 2: se replica otra vez la vida de
                     quien regalo, oyendo ahora los partes del hermano con su pedido, y en cada tic en que el campo regalo se mira si el ultimo
                     parte fresco del hermano pedia y que elige la replica. -> P7_13_F2.json"""
import collections, glob, json, os, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_13_tmp")

def vida(carp, slot, brazo, cuad, pide, partes=None, tics=None):
    import banco_P7_5 as B
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS[brazo].get(k, "0")
    os.environ["GEMV_P7_PIDE"] = str(pide); os.environ["CUADERNO_DIR"] = cuad
    # [P7-13] los diarios del campo del siete (P7-5 a P7-10) se jugaron con GEMV_OJOS=0 (parte E1 cada 48 tics; lo dice su `arranque`), y los
    # de A4 del seis con GEMV_OJOS=1 (parte E2). El molde de replica (`mide_P6_29`) pone 1 por defecto: aqui se pone el del diario.
    if carp.startswith("P7"): os.environ["GEMV_OJOS"] = "0"
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import mide_P6_29 as M
    import descubre_P7 as X
    import pide_P7 as J
    PIDOS = []; HJ = {}; _ap0 = X.aplica
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); HJ.update(J.aplica(clase, lambda r: (PIDOS.append(r) if r.get("k") == "P7_pido" else None, registra(r) if registra else None)))
        return h
    X.aplica = _aplica
    cambiados = [0]
    if partes:                                              # pase 2: el hermano habla con su pedido
        PT = json.load(open(partes)); _o0 = M.obs_de; herm = 21 - slot
        def _obs(r, sp, it):
            o = _o0(r, sp, it); chat = o.get("chat") or []
            if chat:
                nuevo = []
                for m in chat:
                    tx = m.get("text") or ""; mm = re.match(r"^E1 P(\d+) t(\d+) ", tx)
                    if m.get("from") == herm and m.get("channel") == "team" and mm and PT.get(mm.group(2)) and PT[mm.group(2)] != tx and PT[mm.group(2)].startswith(tx):
                        m = dict(m, text=PT[mm.group(2)]); cambiados[0] += 1
                    nuevo.append(m)
                o = dict(o, chat=nuevo)
            return o
        M.obs_de = _obs
    REG = {}
    if tics:
        TICS = set(json.load(open(tics))); _d0 = M._DEC0
        def _dec(obs, mundo, mem, tick, bloqueos=None):
            ac, ra = _d0(obs, mundo, mem, tick, bloqueos)
            if tick in TICS:
                C = ra.get("candidatos") or {}; p = mem.parte_fresco(tick)
                REG[tick] = {"elegido": ra.get("elegido"), "hermano_pide": J.hermano_pide(mundo, mem, tick), "parte_fresco": (p is not None), "parte_b": (p or {}).get("botiquin"), "parte_edad": (tick - p["t"]) if p else None,
                             "d": {k: (v["d"] if isinstance(v, dict) else v) for k, v in C.items()}, "S-PROVISION": {k: (v.get("filas") or {}).get("S-PROVISION") for k, v in C.items() if isinstance(v, dict) and (k == "noop" or k.startswith("soltar_"))}}
            return ac, ra
        M._DEC0 = _dec
    r = B.vida(carp, slot, brazo, cuad)
    return {"carp": carp, "slot": slot, "brazo": brazo, "pide": pide, "hecho": r["hecho"], "hecho_J": HJ, "tics": r["tics"], "fidelidad": r["fidelidad"], "desacuerdos": r["desacuerdos"], "errores": r["errores"],
            "pidos": PIDOS, "partes_cambiados": cambiados[0], "en_tics": {str(t): REG.get(t) for t in sorted(REG)}}

def lanza(carp, slot, brazo, cuad, pide, salida, partes=None, tics=None):
    if os.path.exists(salida): os.remove(salida)
    cmd = [sys.executable, os.path.abspath(__file__), "--vida", carp, str(slot), "--brazo", brazo, "--cuadernos", cuad, "--pide", str(pide), "--salida", salida]
    if partes: cmd += ["--partes", partes]
    if tics: cmd += ["--tics", tics]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=2400)
    return json.load(open(salida)) if os.path.exists(salida) else {"carp": carp, "slot": slot, "brazo": brazo, "error": (r.stderr or r.stdout)[-600:]}

def f1(hilos):
    vidas = [(os.path.basename(c), s) for pat in ("P611_t1_A4_*", "P611_t2_A4_*", "P624_t1_A4_*") for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))) for s in (10, 11) if glob.glob(os.path.join(c, f"*policy_agent_{s}.art.log"))]
    R = {}
    for brazo in ("apagado", "TECHO"):
        t0 = time.time(); cu = os.path.join(SAL, "cuad_f1_" + brazo); os.makedirs(cu, exist_ok=True)
        with ThreadPoolExecutor(hilos) as ex: res = list(ex.map(lambda v: lanza(v[0], v[1], brazo, cu, 0, os.path.join(SAL, f"f1_{brazo}_{v[0]}_{v[1]}.json")), vidas))
        fid = collections.Counter(); des = []
        for r in res:
            if r.get("error"): fid["error"] += 1; print("  ERROR", r["carp"], r["slot"], r["error"][-300:], flush=True); continue
            fid.update(r["fidelidad"]); des += [{"vida": f"{r['carp']}/{r['slot']}", **d} for d in r["desacuerdos"]]
        ok = next((r for r in res if not r.get("error")), {})
        R[brazo] = {"vidas": len(vidas), "fidelidad": dict(fid), "desacuerdos": des, "segundos": round(time.time() - t0, 1), "hecho": ok.get("hecho"), "hecho_J": ok.get("hecho_J")}
        print(f"F1 {brazo}: {dict(fid)} · {len(des)} desacuerdos · {R[brazo]['segundos']} s · pide {ok.get('hecho_J')}", flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_13_F1.json"), "w"), ensure_ascii=False, indent=1)

def cuaderno_de(clave_dir, s, d):
    cuad = os.path.join(SAL, "cuad_" + clave_dir); shutil.rmtree(cuad, ignore_errors=True); os.makedirs(cuad)
    if d > 1:
        for q in (10, 11):
            limpio = os.path.join(AQUI, "P7_10_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}_limpio.json"); normal = os.path.join(AQUI, "P7_10_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}.json")
            shutil.copy(limpio if os.path.exists(limpio) else normal, os.path.join(cuad, f"cuaderno_P7_{q}.json"))
    return cuad

def f2(hilos):
    V = json.load(open(os.path.join(AQUI, "P7_11_vidas.json"))); AP = {k: v for k, v in V.items() if v["brazo"] == "APRENDE"}
    partidas = sorted({(v["serie"], v["dia"]) for v in AP.values() if v["regala"]})
    carp_de = lambda s, d: os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P710_s{s}_d{d}_APRENDE_*"))[0])
    t0 = time.time()
    def pase1(x):
        s, d, sl = x; return x, lanza(carp_de(s, d), sl, "APRENDE", cuaderno_de(f"p1_s{s}_d{d}_{sl}", s, d), 1, os.path.join(SAL, f"f2_p1_s{s}_d{d}_{sl}.json"))
    with ThreadPoolExecutor(hilos) as ex: P1 = dict(ex.map(pase1, [(s, d, sl) for s, d in partidas for sl in (10, 11)]))
    err = [k for k, r in P1.items() if r.get("error")]
    if err: print("ERROR pase 1", err[0], P1[err[0]]["error"][-400:]); return
    print(f"pase 1: {len(P1)} vidas · {round(time.time() - t0)} s", flush=True)
    def pase2(x):
        s, d, sl = x; v = AP[f"s{s}_d{d}_APRENDE_{sl}"]; herm = P1[(s, d, 21 - sl)]
        pf = os.path.join(SAL, f"f2_partes_s{s}_d{d}_{21 - sl}.json"); json.dump({str(p["tick"]): p["texto"] for p in herm["pidos"]}, open(pf, "w"))
        tf = os.path.join(SAL, f"f2_tics_s{s}_d{d}_{sl}.json"); json.dump(sorted({g["t_dec"] for g in v["regala"]}), open(tf, "w"))
        return x, lanza(carp_de(s, d), sl, "APRENDE", cuaderno_de(f"p2_s{s}_d{d}_{sl}", s, d), 1, os.path.join(SAL, f"f2_p2_s{s}_d{d}_{sl}.json"), partes=pf, tics=tf)
    dadores = [(v["serie"], v["dia"], v["slot"]) for v in AP.values() if v["regala"]]
    with ThreadPoolExecutor(hilos) as ex: P2 = dict(ex.map(pase2, dadores))
    err = [k for k, r in P2.items() if r.get("error")]
    if err: print("ERROR pase 2", err[0], P2[err[0]]["error"][-400:]); return
    regalos = []; fid1 = collections.Counter(); fid2 = collections.Counter(); nuevos = 0
    for r in P1.values(): fid1.update(r["fidelidad"])
    for (s, d, sl), r in P2.items():
        fid2.update(r["fidelidad"]); v = AP[f"s{s}_d{d}_APRENDE_{sl}"]; td = {g["t_dec"] for g in v["regala"]}
        nuevos += sum(1 for x in r["desacuerdos"] if str(x["replica"]).startswith("soltar_first_aid") and x["t"] not in td)
        for g in v["regala"]:
            e = r["en_tics"].get(str(g["t_dec"])) or {}
            regalos.append({"vida": f"s{s}_d{d}_{sl}", "t": g["t_dec"], "hermano_pide": e.get("hermano_pide"), "parte_fresco": e.get("parte_fresco"), "parte_b": e.get("parte_b"), "elegido_replica": e.get("elegido"),
                            "sigue_regalando": str(e.get("elegido")).startswith("soltar_first_aid"), "banda_hermano": g["banda_hermano"], "destino_en_el_campo": g["destino"], "d": e.get("d"), "S-PROVISION": e.get("S-PROVISION")})
    pid = {f"s{s}_d{d}_{sl}": {"emisiones": len(r["pidos"]), "pidiendo": sum(1 for p in r["pidos"] if p["pide"]), "abre": sum(1 for p in r["pidos"] if p["abre"]), "cierra": dict(collections.Counter(p["cierra"] for p in r["pidos"] if p["cierra"])), "largo_max": max((p["largo"] for p in r["pidos"]), default=None)} for (s, d, sl), r in P1.items()}
    OUT = {"regalos": regalos, "resumen": {"regalos": len(regalos), "el_hermano_pedia": sum(1 for g in regalos if g["hermano_pide"]), "la_replica_sigue_regalando": sum(1 for g in regalos if g["sigue_regalando"]),
                                           "regalos_nuevos_en_otros_tics": nuevos, "partes_del_hermano_con_pedido_oidos": sum(r["partes_cambiados"] for r in P2.values())},
           "fidelidad_pase1": dict(fid1), "fidelidad_pase2": dict(fid2), "pedidos_por_vida": pid, "segundos": round(time.time() - t0)}
    json.dump(OUT, open(os.path.join(AQUI, "P7_13_F2.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(OUT["resumen"], ensure_ascii=False), "· fidelidad pase 1", dict(fid1), "· pase 2", dict(fid2), "·", OUT["segundos"], "s")

if __name__ == "__main__":
    a = sys.argv; os.makedirs(SAL, exist_ok=True); hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 8
    if "--vida" in a:
        i = a.index("--vida"); g = lambda k: a[a.index(k) + 1] if k in a else None
        r = vida(a[i + 1], int(a[i + 2]), g("--brazo"), g("--cuadernos"), int(g("--pide") or 0), g("--partes"), g("--tics"))
        json.dump(r, open(g("--salida"), "w"), ensure_ascii=False)
    elif "--f1" in a: f1(hilos)
    elif "--f2" in a: f2(hilos)
