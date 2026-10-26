"""[P7-5] EL BANCO DEL CUERPO QUE DESCUBRE: una vida por PROCESO (subproceso), con el molde de replica de P6-29 / P7-2 (obs del diario por un
cable falso) y la politica del siete enganchada (`descubre_P7.aplica`) con los interruptores que diga el brazo.
  --vida CARP SLOT --brazo {apagado,TECHO,SUELO,BORRADO,APRENDE} [--cuadernos DIR]   (un proceso: replica una vida y escribe un JSON)
  --f1 [--hilos N]      F1: los 80 diarios de A4 con `apagado` y con `TECHO`: la eleccion de la replica contra RADIOGRAFIA.elegido, tic a tic
  --f2 ...              F2: ver mas abajo
Salida de cada vida: {fidelidad, desacuerdos, usos: [{t, heal_imaginado, R-ACOPIO, W_botiquin, R-NOVEDAD}], huellas, cuaderno_fin}.
"""
from __future__ import annotations
import collections, glob, json, os, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
BRAZOS = {"apagado": {}, "TECHO": {"GEMV_P7": "1", "GEMV_P7_SABE": "1"},                       # F1: hacer sitio apagado
          "ESPERANZA": {"GEMV_P7": "1", "GEMV_P7_SITIO": "1"},      # [P7-13] el brazo que fue SUELO; "SUELO" queda como nombre viejo para los diarios de P7-10
          "SUELO": {"GEMV_P7": "1", "GEMV_P7_SITIO": "1"}, "TECHO_SITIO": {"GEMV_P7": "1", "GEMV_P7_SABE": "1", "GEMV_P7_SITIO": "1"},
          "BORRADO": {"GEMV_P7": "1", "GEMV_P7_CUADERNO": "1", "GEMV_P7_BORRADO": "1", "GEMV_P7_NOVEDAD": "1", "GEMV_P7_SITIO": "1"},
          "APRENDE": {"GEMV_P7": "1", "GEMV_P7_CUADERNO": "1", "GEMV_P7_NOVEDAD": "1", "GEMV_P7_SITIO": "1"}}

def vida(carp, slot, brazo, cuadernos):
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = BRAZOS[brazo].get(k, "0")
    os.environ["CUADERNO_DIR"] = cuadernos
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import mide_P6_29 as M                      # el entorno de A4 y el molde (obs_de, config_de, WS); instala su gancho, que se deshace
    from alma import policy_cortex as PC
    from alma import policy_forma as PF
    from alma import decisor_zs as D
    import policy_pareja as PP, serie_util as U, descubre_P7 as X, asyncio, re
    D.decide = M._DEC0
    registros = []
    hecho = X.aplica(PP.AlmaPareja, registros.append)
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]
    tics = []; pc = sm = cat = fin = None; sp = it = 5; EL = {}; USOS = {}
    for r in U.lee(f):
        k = r.get("k")
        if k == "player_config": pc = r
        elif k == "static_map": sm = r
        elif k == "catalogo": cat = r
        elif k == "arranque":
            s = json.dumps(r); m = re.search(r'"speed"\s*:\s*(\d+)', s); sp = int(m.group(1)) if m else 5; m = re.search(r'"intelligence"\s*:\s*(\d+)', s); it = int(m.group(1)) if m else 5
        elif k == "tick" and r.get("phase") == "live":
            tics.append(r); EL[r["tick"]] = (r.get("RADIOGRAFIA") or {}).get("elegido")
            if (r.get("intencion") or {}).get("do") == "use":
                s_ = r["intencion"].get("slot"); pk = r.get("pack") or []
                if s_ is not None and s_ < len(pk) and pk[s_] and pk[s_]["id"] == "first_aid": USOS[r["tick"]] = {"hp": r["hp"]}
        elif k == "final": fin = r
    extra = os.environ.get("P7_REGISTRA_TICKS")
    if extra:
        for t_ in json.load(open(extra)): USOS.setdefault(int(t_), {"extra": True})
    # el gancho de lectura: en cada tic, la eleccion; en los tics de uso, lo que imagino y las filas de las ganas y la novedad
    REG = {}; _dec = D.decide
    def _dec5(obs, mundo, mem, tick, bloqueos=None):
        ac, ra = _dec(obs, mundo, mem, tick, bloqueos)
        rec = {"el": ra.get("elegido")}
        if not REG:                                     # el primer tic vivo: las ganas sin botiquin a bordo
            ah = ra.get("ahora") or {}; fl = ah.get("filas") or {}
            REG["inicio"] = {"t": tick, "R-ACOPIO": (fl.get("R-ACOPIO") or {}).get("M", 0.0), "R-CARENCIA": (fl.get("R-CARENCIA") or {}).get("M", 0.0), "W": ah.get("W"), "k": X.k_ganas(mundo), "R-NOVEDAD": fl.get("R-NOVEDAD")}
        if tick in USOS:
            ah = ra.get("ahora") or {}; fl = ah.get("filas") or {}
            uh = X.ESTADO.get("ultima_heal"); fresco = bool(uh and uh[0] == tick)
            rec.update({"heal": (uh[1] if fresco else None), "candidato_usar_en_la_replica": fresco, "elegido_replica_aqui": ra.get("elegido"), "R-ACOPIO": (fl.get("R-ACOPIO") or {}).get("M"), "R-CARENCIA": (fl.get("R-CARENCIA") or {}).get("M"), "W": ah.get("W"),
                        "W_botiquin": (ah.get("W_desglose") or {}).get("botiquin"), "R-NOVEDAD": (fl.get("R-NOVEDAD") or {}), "k": X.k_ganas(mundo), "W_TARGET_usado": (2.0 + X.k_ganas(mundo)) if (X.ON and not X.SABE) else X.W_TARGET0,
                        "d": {k2: (v["d"] if isinstance(v, dict) else v) for k2, v in (ra.get("candidatos") or {}).items()}})
        REG[tick] = rec; return ac, ra
    D.decide = _dec5
    AH = {}; _dd = PP.AlmaPareja.decidir
    def _decidir(self, obs, _d=_dd):
        ac, ra = _d(self, obs)
        if ra is not None and getattr(self, "phase", None) == "live":
            t = self.tick; ah = ra.get("ahora") or {}; fl = ah.get("filas") or {}
            if "inicio" not in AH or t in USOS:
                AH["inicio" if "inicio" not in AH else t] = {"t": t, "R-ACOPIO": (fl.get("R-ACOPIO") or {}).get("M", 0.0), "R-CARENCIA": (fl.get("R-CARENCIA") or {}).get("M", 0.0), "W": ah.get("W"), "W_botiquin": (ah.get("W_desglose") or {}).get("botiquin"), "R-NOVEDAD": fl.get("R-NOVEDAD"), "k": X.k_ganas(self.mundo)}
        return ac, ra
    PP.AlmaPareja.decidir = _decidir
    cfg = M.config_de(pc, sm, cat); alma = PP.AlmaPareja(); alma.artefacto_subido = True; PP._envuelve(alma)
    mudo = lambda rec: None; _logs = (PC.log, PF.log, PP.log); PC.log = mudo; PF.log = mudo; PP.log = mudo
    msgs = [json.dumps(cfg)] + [json.dumps(M.obs_de(r, sp, it)) for r in tics] + [json.dumps({"type": "final", "placement": (fin or {}).get("placement"), "kills": 0, "score": 0.0, "reason": (fin or {}).get("reason"), "match_ticks": (fin or {}).get("match_ticks")})]
    n_tics = len(tics); del tics; ws = M.WS(msgs); out_real = sys.stdout
    try:
        sys.stdout = open(os.devnull, "w"); asyncio.run(PC.decisor(ws, alma))
    finally:
        sys.stdout = out_real; PC.log, PF.log, PP.log = _logs; PC._DIARIO.clear()
    X.termina(registros.append)
    fid = collections.Counter(); des = []
    for t, el in EL.items():
        r = REG.get(t)
        if r is None: fid["sin replica"] += 1
        elif r["el"] == el: fid["igual"] += 1
        else: fid["difiere"] += 1; des.append({"t": t, "diario": el, "replica": r["el"]})
    usos = [{"t": t, **{k: v for k, v in REG.get(t, {}).items() if k != "el"}, "ahora": AH.get(t), "elegido_diario": EL.get(t), "elegido_replica": REG.get(t, {}).get("el")} for t in sorted(USOS)]
    cuad = X.ESTADO["cuaderno"].volcado() if X.ESTADO["cuaderno"] is not None else None
    return {"carp": carp, "slot": slot, "brazo": brazo, "hecho": hecho, "tics": n_tics, "fidelidad": dict(fid), "desacuerdos": des, "usos": usos, "inicio": AH.get("inicio"),
            "huellas": [r for r in registros if r.get("k") == "P7_huella"], "P7_usos": [r for r in registros if r.get("k") == "P7_uso"], "errores": [r for r in registros if r.get("k") == "P7_error"], "cuaderno_fin": cuad}

def lanza_vida(carp, slot, brazo, cuadernos, salida):
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(slot), "--brazo", brazo, "--cuadernos", cuadernos, "--salida", salida], capture_output=True, text=True, timeout=1800)
    if r.returncode or not os.path.exists(salida): return {"carp": carp, "slot": slot, "brazo": brazo, "error": (r.stderr or r.stdout)[-600:]}
    return json.load(open(salida))

def f1(hilos):
    from concurrent.futures import ThreadPoolExecutor
    vidas = [(os.path.basename(c), s) for pat in ("P611_t1_A4_*", "P611_t2_A4_*", "P624_t1_A4_*") for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))) for s in (10, 11) if glob.glob(os.path.join(c, f"*policy_agent_{s}.art.log"))]
    sal = os.path.join(AQUI, "_P7_5_tmp"); os.makedirs(sal, exist_ok=True); R = {}
    for brazo in ("apagado", "TECHO"):
        t0 = time.time()
        with ThreadPoolExecutor(hilos) as ex:
            res = list(ex.map(lambda v: lanza_vida(v[0], v[1], brazo, os.path.join(sal, "cuad_" + brazo), os.path.join(sal, f"{brazo}_{v[0]}_{v[1]}.json")), vidas))
        fid = collections.Counter(); des = []
        for r in res:
            if r.get("error"): fid["error"] += 1; print("  ERROR", r["carp"], r["slot"], r["error"][-200:], flush=True); continue
            fid.update(r["fidelidad"]); des += [{"vida": f"{r['carp']}/{r['slot']}", **d} for d in r["desacuerdos"]]
        R[brazo] = {"vidas": len(vidas), "fidelidad": dict(fid), "desacuerdos": des, "segundos": round(time.time() - t0, 1), "hecho": next((r.get("hecho") for r in res if not r.get("error")), None)}
        print(f"F1 {brazo}: {dict(fid)} · {len(des)} desacuerdos · {R[brazo]['segundos']} s", flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_5_F1.json"), "w"), ensure_ascii=False, indent=1)

def cuaderno_de_P7_1(slot, dias_hasta, destino):
    """F2: el cuaderno cargado A MANO con los recuerdos del diario de P7-1 (efectos de P7_5_huella.json con la regla de causas conocidas;
    recursos, vinculo e importancias de P7_4_huella.json; la importancia va sin signo: aqui solo decide el peso) para un asiento, con las
    semillas en orden creciente como dias 1..dias_hasta. Escribe destino/cuaderno_P7_<slot>.json y devuelve el Cuaderno."""
    sys.path.insert(0, AQUI); from cuaderno_P7 import Cuaderno
    H5 = {(h["vida"], h["t"]): h for h in json.load(open(os.path.join(AQUI, "P7_5_huella.json")))["usos"]}
    H4 = [h for h in json.load(open(os.path.join(AQUI, "P7_4_huella.json")))["usos"] if "descartado" not in h]
    semillas = sorted({int(L["carpeta"].rsplit("_", 1)[1]) for L in json.load(open(os.path.join(AQUI, "P7_1_medidas.json")))["vidas"]})
    dia = {s_: i + 1 for i, s_ in enumerate(semillas)}
    c = Cuaderno(slot); filas = []
    for h in sorted(H4, key=lambda h: (dia[int(h["vida"].split("/")[0].rsplit("_", 1)[1])], h["t"])):
        carp, sl = h["vida"].split("/")
        if int(sl) != slot: continue
        d = dia[int(carp.rsplit("_", 1)[1])]
        if d > dias_hasta: continue
        c.dia = d - 1                                  # el dia que se vive es d
        e5 = H5.get((h["vida"], h["t"]), {}).get("efecto_P7_5", h["cuerpo"]["efecto"])
        r = c.apunta("first_aid", "dentro" if h["dentro"] else "fuera", {"cuerpo": e5, "recursos": h["recursos"]["efecto"], "vinculo": (h["vinculo"]["efecto"] or 0.0)},
                     {k: (h["importancia"].get(e) or 0.0) for k, e in (("cuerpo", "F"), ("recursos", "R"), ("vinculo", "S"))}, tick=h["t"])
        c.cuenta_uso("first_aid"); filas.append({"dia": d, "t": h["t"], "situacion": "dentro" if h["dentro"] else "fuera", "efecto": r["efecto"], "intensidad": r["intensidad"]})
    c.dia = dias_hasta                                  # ya se han vivido dias_hasta dias
    os.makedirs(destino, exist_ok=True); ruta = os.path.join(destino, f"cuaderno_P7_{slot}.json")
    json.dump(c.volcado(), open(ruta, "w"), ensure_ascii=False, indent=1)
    return c, ruta, filas

def f2():
    """F2: con el cuaderno cargado a mano (dias 1-20), replica vidas de los dias 21-40 con APRENDE y comprueba que la imaginacion del
    botiquin (heal de la receta) da la creencia del cuaderno en su situacion, y que las ganas salen con la escala acordada
    (R-ACOPIO = 0,18 x k, el termino del botiquin en W = k, W_TARGET = 2 + k, con k = creencia_max / 50)."""
    sys.path.insert(0, AQUI); from cuaderno_P7 import Cuaderno
    semillas = sorted({int(L["carpeta"].rsplit("_", 1)[1]) for L in json.load(open(os.path.join(AQUI, "P7_1_medidas.json")))["vidas"]})
    carpetas = {int(os.path.basename(c).rsplit("_", 1)[1]): os.path.basename(c) for pat in ("P611_t1_A4_*", "P611_t2_A4_*", "P624_t1_A4_*") for c in glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))}
    sal = os.path.join(AQUI, "_P7_5_tmp", "F2"); os.makedirs(sal, exist_ok=True); R = {"vidas": [], "cuadernos": {}}
    usos_por_vida = collections.Counter(f["vida"] for f in json.load(open(os.path.join(AQUI, "P7_1_diario.json")))["botiquin"])
    for slot in (10, 11):
        cuad_dir = os.path.join(sal, f"cuad_{slot}"); c, ruta, filas = cuaderno_de_P7_1(slot, 20, cuad_dir)
        R["cuadernos"][slot] = {"ruta": ruta, "recuerdos": len(filas), "creencias": c.creencias(), "usos": c.usos("first_aid")}
        # tres vidas de los dias 21-40 de ese asiento con usos de botiquin, en orden; cada una lee lo que dejo la anterior
        cand = [(d, carpetas[s_]) for d, s_ in enumerate(semillas, 1) if d > 20 and usos_por_vida.get(f"{carpetas[s_]}/{slot}", 0) > 0][:3]
        for d, carp in cand:
            antes = Cuaderno.lee(ruta, slot); esperado = {s_: antes.creencia_cuerpo("first_aid", s_) for s_ in ("dentro", "fuera")}; k_esp = (antes.creencia_max_cuerpo("first_aid") or 0.0) / 50.0
            r = lanza_vida(carp, slot, "APRENDE", cuad_dir, os.path.join(sal, f"APRENDE_{carp}_{slot}.json"))
            if r.get("error"): R["vidas"].append({"dia": d, "vida": f"{carp}/{slot}", "error": r["error"]}); print("  ERROR", carp, slot, r["error"][-300:]); continue
            u0 = r["usos"][0] if r["usos"] else {}
            sit0 = next((x["situacion"] for x in r["P7_usos"] if x["tick"] == u0.get("t", -1) + 1), None)
            chk = {"dia": d, "vida": f"{carp}/{slot}", "fidelidad": r["fidelidad"], "primer_uso": {"t": u0.get("t"), "situacion": sit0, "heal_imaginado": u0.get("heal"), "esperado": (esperado.get(sit0) if sit0 else None),
                   "R-ACOPIO_en_el_uso": u0.get("R-ACOPIO"), "W_botiquin": u0.get("W_botiquin"), "k": u0.get("k"), "k_esperado": round(k_esp, 4), "W_TARGET_usado": u0.get("W_TARGET_usado"), "R-NOVEDAD": u0.get("R-NOVEDAD")},
                   "huellas": len(r["huellas"]), "cuaderno_fin": {"dia": (r["cuaderno_fin"] or {}).get("dia"), "usos": ((r["cuaderno_fin"] or {}).get("objetos") or {}).get("first_aid", {}).get("usos"), "creencias": (r["cuaderno_fin"] or {}).get("creencias")}}
            # TODOS los usos (los del diario, que el mundo replica) con candidato fresco en la replica: el heal imaginado contra la
            # creencia vigente en ese momento (la precargada, o la que dejo la huella anterior en esa situacion dentro de la vida)
            vig = dict(esperado); comp = []; hu = sorted(r["huellas"], key=lambda h: h["t0"])
            for pu in r["P7_usos"]:
                sit = pu["situacion"]; esp = vig.get(sit); h = pu.get("heal_imaginado")
                if h is not None:
                    ok = (esp is not None and abs(h - max(0.0, esp)) < 1e-6) or (h == 0.0 and esp is None); comp.append({"t": pu["tick"] - 1, "situacion": sit, "heal": h, "esperado": esp, "ok": ok})
                for hh in hu:
                    if hh["t0"] == pu["tick"] and hh.get("creencia_despues"): vig[sit] = hh["creencia_despues"]["cuerpo"]
            chk["usos_comparados"] = comp; chk["primer_uso"].update({"n_comparados": len(comp), "todos_coinciden": all(c["ok"] for c in comp) if comp else None, "primero": comp[0] if comp else None})
            chk["primer_uso"]["coincide_heal"] = chk["primer_uso"]["todos_coinciden"]
            chk["primer_uso"]["coincide_k"] = (u0.get("k") is not None and abs(u0["k"] - k_esp) < 1e-6)
            ini = r.get("inicio") or {}; chk["inicio"] = dict(ini, R_ACOPIO_esperado=round(0.18 * k_esp, 6), coincide_acopio=(ini.get("R-ACOPIO") is not None and abs(ini["R-ACOPIO"] - 0.18 * k_esp) < 1e-4))
            R["vidas"].append(chk); print(json.dumps(chk, ensure_ascii=False)[:700], flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_5_F2.json"), "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    a = sys.argv
    if "--vida" in a:
        i = a.index("--vida"); carp, slot = a[i + 1], int(a[i + 2]); brazo = a[a.index("--brazo") + 1]; cuad = a[a.index("--cuadernos") + 1] if "--cuadernos" in a else os.path.join(AQUI, "_P7_5_tmp", "cuad")
        r = vida(carp, slot, brazo, cuad)
        if "--salida" in a: json.dump(r, open(a[a.index("--salida") + 1], "w"), ensure_ascii=False)
        else: print(json.dumps({k: v for k, v in r.items() if k not in ("usos", "huellas")}, ensure_ascii=False)[:1500])
    elif "--f1" in a:
        f1(int(a[a.index("--hilos") + 1]) if "--hilos" in a else 4)
    elif "--f2" in a:
        f2()
