"""[P7-22, R4 y medida 2] LA REPETICION DE DECISIONES CON EL RECUERDO POR PARECIDO (C). Replica (molde de `banco_P7_15.py`, UN SUBPROCESO POR VIDA, sin
partidas ni llamadas) de las vidas de APRENDE de P7-14b de los dias 11 a 20, tal como se jugaron. En cada tic el cuerpo decide dos veces sobre la misma
escena y la misma memoria: con su cuaderno (la decision del campo, comprobada contra el diario) y con la cura imaginada del botiquin recordada por
parecido (C): efecto = (1 - ignorancia_C) x creencia_vivida_C + ignorancia_C x esperanza, con creencia_vivida_C = suma(w e) / suma(w) e
ignorancia_C = 1 / (1 + suma(w)) sobre los recuerdos de los dias anteriores de esa criatura (P7_22_recuerdos.json), con la foto emocional de AHORA
leida del diario en ese tic. Solo cambia la cura imaginada al usar (`heal_imaginado`); las ganas (`k_ganas`) quedan como en el campo (declarado).
Se apunta cada tic en que las dos decisiones difieren y, para cada eleccion de `usar_botiquin` del campo, que elige C en ese tic.
  python3 banco_decide_P7_22.py            -> P7_22_decisiones.json
  python3 banco_decide_P7_22.py --vida S_D_SLOT"""
import collections, copy, glob, json, math, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_22_tmp"); DIAS = range(11, 21)


def una(s, d, sl):
    import banco_P7_5 as B, banco_P7_22 as K, recuerdos_P7_22 as RQ, analiza_P7_16 as A16
    carp = os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P714b_s{s}_d{d}_APRENDE_*"))[0])
    cuad = os.path.join(SAL, f"cuad_s{s}_d{d}_{sl}"); shutil.rmtree(cuad, ignore_errors=True); os.makedirs(cuad)
    for q in (10, 11): shutil.copy(os.path.join(AQUI, "P7_14b_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}.json"), os.path.join(cuad, f"cuaderno_P7_{q}.json"))
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS["APRENDE"].get(k, "0")
    os.environ["GEMV_P7_PIDE"] = "1"; os.environ["CUADERNO_DIR"] = cuad; os.environ["GEMV_OJOS"] = "0"        # como se jugo P7-14b
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import mide_P6_29 as M
    import descubre_P7 as X
    import pide_P7 as J
    _ap0 = X.aplica
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); J.aplica(clase, registra); return h
    X.aplica = _aplica
    # los recuerdos de los dias anteriores de esta criatura, y la foto y el "golpeada" de cada tic del diario
    s_fijo = json.load(open(os.path.join(AQUI, "P7_22_fijado.json")))["s"]
    previos = [r for v in K.V.values() if v["campo"] == "P7-14b" and v["serie"] == s and v["slot"] == sl and v["dia"] < d for r in v["recuerdos"]]
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{sl}.art.log"))[0]
    FOTO = {}
    for line in open(f):
        if '"k": "tick"' not in line and '"k":"tick"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") == "tick" and r.get("phase") == "live": FOTO[r["tick"]] = RQ.foto_de(r)
    _, T = A16.lee(f); GOLPE = {}; ult = None
    for t in T:
        if any(True for _ in t["dmg"]): ult = t["t"]
        GOLPE[t["t"]] = (ult is not None and 0 < t["t"] - ult <= 48) or any(True for _ in t["dmg"])
    USO = {}
    def heal_C(mundo, pos, tick):
        ahora = {"dia": d, "dentro": X.situacion(mundo, pos, tick) == "dentro", "golpeado_48": bool(GOLPE.get(tick)), "foto": FOTO.get(tick)}
        if ahora["foto"] is None or not previos: cre, den = 0.0, 0.0
        else:
            num = 0.0; den = 0.0
            for r in previos:
                w = r["intensidad"] * (K.OLVIDO ** max(0, d - r["dia"])) * math.exp(-K.dist(K.vec(ahora["foto"]), K.vec(r["foto"])) / s_fijo) * (1.0 if r["dentro"] == ahora["dentro"] else K.CTX_DENTRO) * (1.0 if r["golpeado_48"] == ahora["golpeado_48"] else K.CTX_GOLPE)
                num += w * r["efecto"]["cuerpo"]; den += w
            cre = num / den if den > 0 else 0.0
        ign = 1.0 / (1.0 + den); h = (1.0 - ign) * max(0.0, cre) + ign * X.esperanza_cuerpo(mundo)
        USO[tick] = {"creencia_C": round(cre, 2), "ignorancia_C": round(ign, 3), "heal_C": round(h, 2), "dentro": ahora["dentro"], "golpeado_48": ahora["golpeado_48"], "dolor_F": (ahora["foto"] or {}).get("dolor_F")}
        return h
    DIF = []; ELEC = []; CNT = collections.Counter(); _d0 = M._DEC0; _h0 = X.heal_imaginado
    def _dec(obs, mundo, mem, tick, bloqueos=None):
        X.heal_imaginado = heal_C
        try: _, ra2 = _d0(copy.deepcopy(obs), mundo, copy.deepcopy(mem), tick, copy.deepcopy(bloqueos)); el2 = ra2.get("elegido")
        finally: X.heal_imaginado = _h0
        ac, ra = _d0(obs, mundo, mem, tick, bloqueos); el = ra.get("elegido"); CNT["tics"] += 1
        h_campo = (X.ESTADO.get("ultima_heal") or (None, None)); h_campo = h_campo[1] if h_campo[0] == tick else None
        if el2 != el: DIF.append({"t": tick, "campo": el, "C": el2, "hp": (obs.get("you") or {}).get("hp"), **(USO.get(tick) or {}), "heal_campo": h_campo})
        if el == "usar_botiquin": ELEC.append({"t": tick, "C": el2, "hp": (obs.get("you") or {}).get("hp"), **(USO.get(tick) or {}), "heal_campo": h_campo})
        return ac, ra
    M._DEC0 = _dec
    r = B.vida(carp, sl, "APRENDE", cuad)
    return {"serie": s, "dia": d, "slot": sl, "tics": r["tics"], "tics_comparados": CNT["tics"], "fidelidad": r["fidelidad"], "errores": len(r["errores"]), "recuerdos_previos": len(previos), "distintos": DIF, "elecciones_de_usar": ELEC}


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
        if err: print("ERRORES", len(err), err[0]["clave"], err[0]["error"][-400:])
        json.dump([r for r in R if not r.get("error")], open(os.path.join(AQUI, "P7_22_decisiones.json"), "w"), ensure_ascii=False, indent=0)
        fid = collections.Counter()
        for r in R:
            for k_, n in (r.get("fidelidad") or {}).items(): fid[k_] += n
        print("vidas", len(R) - len(err), "· fidelidad del campo", dict(fid), "· tics comparados", sum(r.get("tics_comparados", 0) for r in R), "· distintos", sum(len(r.get("distintos", [])) for r in R), "· elecciones de usar", sum(len(r.get("elecciones_de_usar", [])) for r in R))
