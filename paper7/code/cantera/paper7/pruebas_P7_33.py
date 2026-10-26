"""[P7-33] LAS PRUEBAS F1 Y F2 (banco, coste cero), sobre banco_P7_33.vida (una vida por proceso).
  python3 pruebas_P7_33.py --f1 [--hilos N]   F1a: los 80 diarios de A4 con `apagado` (GEMV_P7=0): se reproducen. F1b: los mismos 80 con TECHO sin pedir y el oido y la ley
                                           encendidos (GEMV_P7_33=1): cuantas decisiones cambian y en que vidas; y las vidas de TECHO de las semillas k = 184 (P7-30 s1 d7,
                                           s2 d14) y k = 159 (P7-24 s1 d5, s2 d16) replicadas con la ley: en que tics cambian las decisiones frente a la ventana de la inundacion
                                           que anuncia el propio diario. -> P7_33_F1.json
  python3 pruebas_P7_33.py --f2 [--hilos N]   F2: las 6 vidas de APRENDE del dia 1 de P7-30 (cuaderno vacio) con la pieza: efecto imaginado y ganas (k) de las cuatro cosas
                                           en todos los tics; y las mismas vidas con un cuaderno cargado a mano con tres pruebas de red sin efecto: creencia de la red,
                                           ignorancia, y si `ir_curioso` sigue yendo a por redes. -> P7_33_F2.json"""
import collections, glob, json, os, shutil, sys, time
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import banco_P7_33 as B
SAL = B.SAL


def lanza(carp, slot, brazo, cuad, salida, p33=1, pide=1):
    if os.path.exists(salida): os.remove(salida)
    env = dict(os.environ, P7_33=str(p33))
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(AQUI, "banco_P7_33.py"), "--vida", carp, str(slot), "--brazo", brazo, "--cuadernos", cuad, "--arreglos", ",".join(B.TODOS), "--p29", "1", "--pide", str(pide), "--salida", salida], capture_output=True, text=True, timeout=7200, env=env)
    return json.load(open(salida)) if os.path.exists(salida) else {"carp": carp, "slot": slot, "brazo": brazo, "error": (r.stderr or r.stdout)[-800:]}


def avisos_de(carp, slot):
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]; out = []
    for line in open(f, errors="replace"):
        if '"event_warning"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        for e in r.get("eventos") or []:
            if e.get("type") == "event_warning": out.append(e)
    return out


def f1(hilos):
    vidas = [(os.path.basename(c), s) for pat in ("P611_t1_A4_*", "P611_t2_A4_*", "P624_t1_A4_*") for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))) for s in (10, 11) if glob.glob(os.path.join(c, f"*policy_agent_{s}.art.log"))]
    R = json.load(open(os.path.join(AQUI, "P7_33_F1.json"))) if os.path.exists(os.path.join(AQUI, "P7_33_F1.json")) else {}
    for et, brazo, p33 in (("apagado", "apagado", 1), ("TECHO con oido y ley", "TECHO", 1)):
        if "--solo-techo" in sys.argv and brazo == "apagado" and "apagado" in R: continue
        t0 = time.time(); cu = os.path.join(SAL, "cuad_f1_33_" + brazo); os.makedirs(cu, exist_ok=True)
        with ThreadPoolExecutor(hilos) as ex: res = list(ex.map(lambda v: lanza(v[0], v[1], brazo, cu, os.path.join(SAL, f"f1_33_{brazo}_{v[0]}_{v[1]}.json"), p33, 0), vidas))
        fid = collections.Counter(); porvida = []
        for r in res:
            if r.get("error"): fid["error"] += 1; print("  ERROR", r["carp"], r["slot"], r["error"][-300:], flush=True); continue
            fid.update(r["fidelidad"])
            if r["desacuerdos"]: porvida.append({"vida": f"{r['carp']}/{r['slot']}", "cambios": len(r["desacuerdos"]), "primero": r["desacuerdos"][0], "ultimo": r["desacuerdos"][-1], "avisos": avisos_de(r["carp"], r["slot"]), "ley": r.get("P7_33", {}).get("ley")})
        R[et] = {"vidas": len(vidas), "fidelidad": dict(fid), "vidas_con_cambios": porvida, "segundos": round(time.time() - t0, 1), "hecho_33": next((r.get("hecho_33") for r in res if not r.get("error")), None)}
        print(f"F1 {et}: {dict(fid)} · vidas con cambios {len(porvida)} · {R[et]['segundos']} s", flush=True)
    # las vidas de las inundaciones: TECHO de k = 184 (P730 s1 d7, s2 d14) y k = 159 (P724 s1 d5, s2 d16)
    inund = []
    for pref in ("P730_s1_d7_TECHO", "P730_s2_d14_TECHO", "P724_s1_d5_TECHO", "P724_s2_d16_TECHO"):
        cs = glob.glob(os.path.join(RAIZ, "paintball", "runs", pref + "_*"))
        if not cs: continue
        for s in (10, 11):
            if not glob.glob(os.path.join(cs[0], f"*policy_agent_{s}.art.log")): inund.append({"vida": f"{os.path.basename(cs[0])}/{s}", "error": "sin diario (archivado en el T7; rehidratar)"}); continue
            cu = os.path.join(SAL, "cuad_f1_33_inund"); os.makedirs(cu, exist_ok=True)
            r = lanza(os.path.basename(cs[0]), s, "TECHO", cu, os.path.join(SAL, f"f1_33_inund_{pref}_{s}.json"), 1, 1)
            if r.get("error"): inund.append({"vida": f"{os.path.basename(cs[0])}/{s}", "error": r["error"][-300:]}); continue
            av = avisos_de(os.path.basename(cs[0]), s); des = r["desacuerdos"]
            def en_evento(t): return any(int(e.get("from_tick") or 0) - 120 <= t < int(e.get("from_tick") or 0) + int(e.get("duration") or 0) + 60 for e in av)
            inund.append({"vida": f"{os.path.basename(cs[0])}/{s}", "tics": r["tics"], "fidelidad": r["fidelidad"], "avisos": av, "cambios": len(des), "cambios_en_ventana_de_evento": sum(1 for d in des if en_evento(d["t"])), "primero": (des[0] if des else None), "ultimo": (des[-1] if des else None), "ley": r.get("P7_33", {}).get("ley")})
            print("  inundacion", inund[-1]["vida"], inund[-1]["fidelidad"], "cambios", inund[-1]["cambios"], "en ventana", inund[-1]["cambios_en_ventana_de_evento"], flush=True)
    R["inundaciones"] = inund
    json.dump(R, open(os.path.join(AQUI, "P7_33_F1.json"), "w"), ensure_ascii=False, indent=1)


def cuaderno_red(destino, slot):
    """Un cuaderno con tres pruebas de red SIN EFECTO (efecto 0 en los tres dominios), completas, y nada mas."""
    from recuerdo_P7_23 import CuadernoP23
    c = CuadernoP23(slot); c.dia = 1
    for i in range(3):
        r = c.apunta_P23("net", {"dentro": True, "golpeado_48": False}, {"dolor_F": 0.3, "dolor_R": 0.4, "dolor_S": 0.3, "positivo": 0.2, "d": 3.0}, ["noop"] * 4, {"cuerpo": 0.0, "recursos": 0.0, "vinculo": 0.0}, {"cuerpo": 0.0, "recursos": 0.0, "vinculo": 0.0}, tick=100 + i, al_menos=False, corte=False)
        r["prueba"] = {"duracion": 240, "completa": True}
    os.makedirs(destino, exist_ok=True); c.escribe(os.path.join(destino, f"cuaderno_P7_{slot}.json")); return c


def f2(hilos):
    vidas = [(os.path.basename(c), s) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P730_s*_d1_APRENDE_*"))) for s in (10, 11)]
    R = {}
    for et, carga in (("vacio", False), ("tres_redes_sin_efecto", True)):
        def una(v):
            cu = os.path.join(SAL, f"cuad_f2_33_{et}_{v[0]}_{v[1]}"); shutil.rmtree(cu, ignore_errors=True); os.makedirs(cu)
            if carga:
                for s in (10, 11): cuaderno_red(cu, s)
            return lanza(v[0], v[1], "APRENDE", cu, os.path.join(SAL, f"f2_33_{et}_{v[0]}_{v[1]}.json"))
        t0 = time.time()
        with ThreadPoolExecutor(hilos) as ex: res = list(ex.map(una, vidas))
        out = []
        for r in res:
            if r.get("error"): out.append({"carp": r["carp"], "slot": r["slot"], "error": r["error"][-300:]}); print("  ERROR", r["carp"], r["slot"], r["error"][-200:], flush=True); continue
            X_ = [x for x in r["registros"] if x.get("el")]
            t1 = min((h["t0"] for h in r["huellas"]), default=None); antes = [x for x in X_ if t1 is None or x["t"] < t1]
            kmax = {o: max((x["k33"][o] for x in antes), default=None) for o in ("botiquin", "racion", "red", "camuflaje")}; hmax = {o: max((x["heal33"][o] for x in antes), default=None) for o in ("botiquin", "racion")}
            cur = collections.Counter((x["ir_curioso"] or {}).get("clase") for x in X_ if x["el"] == "ir_curioso")
            cf = ((r.get("cuaderno_fin") or {}).get("creencias") or {})
            out.append({"carp": r["carp"][5:12], "slot": r["slot"], "tics": r["tics"], "primera_huella": t1, "k_max_antes_de_la_primera_prueba": kmax, "heal_imaginado_max_antes": hmax, "k_red_max_toda_la_vida": max((x["k33"]["red"] for x in X_), default=None), "k_camo_max_toda_la_vida": max((x["k33"]["camuflaje"] for x in X_), default=None),
                        "ir_curioso_por_clase": dict(cur), "pruebas": {o: sum(1 for h in r["huellas"] if h["objeto"] == o) for o in ("net", "camouflage", "first_aid", "rations")}, "cuaderno_fin": {o: {"ignorancia": v.get("ignorancia"), "creencia_dentro": ((v.get("dentro") or {}) or {}).get("cuerpo"), "sabido_max": v.get("sabido_max")} for o, v in cf.items()}, "ms": r["ms_replica"]})
        R[et] = {"vidas": out, "segundos": round(time.time() - t0)}
        print(f"F2 {et}: {len(out)} vidas · {R[et]['segundos']} s", flush=True)
        for o in out:
            if not o.get("error"): print("  ", o["carp"], o["slot"], "k max antes", o["k_max_antes_de_la_primera_prueba"], "heal antes", o["heal_imaginado_max_antes"], "| k red/camo vida", o["k_red_max_toda_la_vida"], o["k_camo_max_toda_la_vida"], "| ir_curioso", o["ir_curioso_por_clase"], "| cuaderno red", o["cuaderno_fin"].get("net"), flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_33_F2.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    os.makedirs(SAL, exist_ok=True); a = sys.argv; hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 6
    if "--f1" in a: f1(hilos)
    elif "--f2" in a: f2(hilos)
