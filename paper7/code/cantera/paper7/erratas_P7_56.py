"""[P7-56 erratas] R2 de P7-56 con la tabla del mundo del sello (SELLO_P7_56.md:18-30) al pie de la letra, sobre los mismos datos. No toca analiza_P7_56.py ni P7_56_sello.json.
  La funcion verdad original se lee del fuente de analiza_P7_56.py (como en compara_P7_59.py); los diarios se leen de los .zip de cada vida, en memoria (los .art.log ya no estan).
  Puerta: con la verdad original, esta lectura debe reproducir exactamente el R2 de P7_56_sello.json (las dos cuentas). Si no, para.
  verdad_sello (interpretacion declarada en informe_P7_56_erratas.md):
    - "situacion prometida" = los campos de la invitacion (anillo, calma); "rival cerca" = rival a <= 4 casillas, la unica definicion de rival del menu (CALMA = sin rival a 4 casillas,
      sin fuego, vida >= 30). La invitacion no tiene campo de rival: "DENTRO del anillo sin rival cerca" solo puede prometerse con calma = CALMA.
    - USAR_RACION: "se corta igual que el botiquin si hay golpe" -> la misma condicion que el botiquin.
    - COGER con promesa de cuerpo 0 -> VERDAD; > 0 -> el primer uso posterior del mismo objeto en la misma vida, desde la aceptacion: VERDAD si no se corta y cura (efecto cuerpo > 0);
      sin uso posterior -> FALSA; < 0 -> FALSA.
    - QUEDARSE_QUIETA con anillo CUALQUIERA: el sello no lo dice; se mantiene la regla original (VERDAD si promete <= 0) y se cuenta aparte.
  Variantes NO selladas (solo para ver de donde sale el cambio): COGER con "cualquier uso posterior que cure"; USAR_RACION sin la condicion de golpes (regla del mundo de P7-62).
  python3 erratas_P7_56.py -> P7_56_erratas.json"""
import glob, json, os, sys, zipfile, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs")
src = open(os.path.join(AQUI, "analiza_P7_56.py")).read(); ns = {"os": os, "AQUI": AQUI}
exec(src[src.index("def verdad"):src.index("\n\n\ndef vida")], ns); verdad_original = ns["verdad"]
exec("import os\n" + src[src.index("def invitaciones"):src.index("\n\n\nV = {}")], ns); invitaciones = ns["invitaciones"]
E = json.load(open(os.path.join(AQUI, "P7_56_estado.json"))); SERIES = sorted({p["serie"] for p in E["peticiones"]}); BRAZOS = ("CON_RAZON", "SIN_RAZON")
SELLO = json.load(open(os.path.join(AQUI, "P7_56_sello.json")))
ee = lambda xs: (st.stdev(xs) / len(xs) ** 0.5 if len(xs) > 1 else None)
OBJ = {"COGER_BOTIQUIN": "first_aid", "COGER_RACION": "rations"}


def lee(S, d, b, sl, p):
    fs = glob.glob(os.path.join(RUNS, f"P756_s{S}_d{d}_{b}_{p['semilla']}", f"*policy_agent_{sl}.zip"))
    if not fs: return None
    z = zipfile.ZipFile(fs[0]); n = [x for x in z.namelist() if x.endswith(".log")][0]; H = []; AC = []; EV = []
    for line in z.open(n):
        if not line.startswith(b'{"k":"P7_'): continue
        if line.startswith(b'{"k":"P7_huella"'): H.append(json.loads(line))
        elif line.startswith(b'{"k":"P7_54_aceptada"'): AC.append(json.loads(line))
        elif line.startswith(b'{"k":"P7_54_evaluada"'): EV.append(json.loads(line))
    return {"H": H, "AC": AC, "EV": EV, "marcada": not ((p.get("latencia") or {}).get(str(sl)) or {}).get("pasa", True)}


def sin_golpes(sit): return sit.get("calma") == "CALMA"          # CALMA, o DENTRO sin rival cerca: sin campo de rival, solo CALMA lo promete


def uso_posterior(v, e, accion, cualquiera=False):
    t_ac = max([a["tick"] for a in v["AC"] if a["n"] == e["n"] and a["tick"] <= e["tick"]] or [None]) if any(a["n"] == e["n"] for a in v["AC"]) else None
    if t_ac is None: return None, "sin aceptacion"
    us = sorted([h for h in v["H"] if (h.get("objeto") or "first_aid") == OBJ[accion] and int(h["t0"]) >= t_ac], key=lambda h: int(h["t0"]))
    cura = lambda h: (not h.get("corte")) and float((h.get("efecto") or {}).get("cuerpo") or 0) > 0
    if not us: return False, "sin uso posterior"
    if cualquiera: return any(cura(h) for h in us), ("cura" if any(cura(h) for h in us) else "usa y no cura")
    return cura(us[0]), ("cura" if cura(us[0]) else ("cortado" if us[0].get("corte") else "usa y no cura"))


def verdad_sello(accion, sit, prom, v, e, coger_cualquiera=False, racion_sin_golpes=True):
    a = accion; p = float(prom or 0.0)
    if a == "USAR_BOTIQUIN": return p > 0 and sin_golpes(sit), None
    if a == "USAR_RACION": return (0 < p <= 20) and (sin_golpes(sit) if racion_sin_golpes else True), None
    if a in OBJ:
        if p == 0: return True, "promete 0"
        if p < 0: return False, "promete < 0"
        return uso_posterior(v, e, a, coger_cualquiera)
    if a in ("COGER_RED", "EMPUNAR_RED", "COGER_CAMUFLAJE", "PONERSE_CAMUFLAJE"): return p == 0, None
    if a == "DAR_BOTIQUIN_HERMANA": return p <= 0, None
    if a == "ACERCARSE_HERMANA": return p == 0, None
    if a == "QUEDARSE_QUIETA":
        an = sit.get("anillo")
        if an == "DENTRO": return p <= 0, None
        if an == "FUERA": return p < 0, None
        return p <= 0, "anillo CUALQUIERA (fuera del sello)"
    return False, None


V = {}
for p in E["peticiones"]:
    if p["estado"] != "completed": continue
    for sl in (10, 11):
        v = lee(p["serie"], p["dia"], p["brazo"], sl, p)
        if v: V[(p["serie"], p["dia"], p["brazo"], sl)] = v


def dias_validos(S, fuera_marcadas):
    ds = set(range(1, 21))
    for b in BRAZOS:
        ds &= {d for (s_, d, b_, sl) in V if s_ == S and b_ == b}
        if fuera_marcadas: ds -= {d for (s_, d, b_, sl), v in V.items() if s_ == S and b_ == b and v["marcada"]}
    return ds


def filas(fuera_marcadas):
    out = []
    for S in SERIES:
        ds = dias_validos(S, fuera_marcadas)
        for (s_, d, b_, sl), v in V.items():
            if not (s_ == S and b_ == "CON_RAZON" and d in ds): continue
            inv = invitaciones(S, d, sl) or []
            for e in v["EV"]:
                i = inv[e["n"]] if e["n"] < len(inv) else None
                if not i: continue
                sit = {"anillo": i.get("anillo"), "calma": i.get("calma")}; prom = (e.get("prometido") or {}).get("cuerpo")
                o = verdad_original(e["accion"], sit, prom)
                n, motivo = verdad_sello(e["accion"], sit, prom, v, e)
                n_cq, _ = verdad_sello(e["accion"], sit, prom, v, e, coger_cualquiera=True)
                n_rs, _ = verdad_sello(e["accion"], sit, prom, v, e, racion_sin_golpes=False)
                out.append({"S": S, "d": d, "sl": sl, "accion": e["accion"], "anillo": sit["anillo"], "calma": sit["calma"], "prom": float(prom or 0.0), "conf": float((e.get("confianza_despues") or {}).get("cuerpo") or 0.0),
                            "original": bool(o), "sello": bool(n), "motivo": motivo, "v_coger_cualquiera": bool(n_cq), "v_racion_sin_golpes": bool(n_rs)})
    return out


def r2(F, clave):
    VE = [f["conf"] for f in F if f[clave]]; FA = [f["conf"] for f in F if not f[clave]]
    r = {"n_verdad": len(VE), "n_falsa": len(FA), "media_verdad": round(st.mean(VE), 3) if VE else None, "media_falsa": round(st.mean(FA), 3) if FA else None}
    if VE and FA:
        d = st.mean(VE) - st.mean(FA); e = ((ee(VE) or 0) ** 2 + (ee(FA) or 0) ** 2) ** 0.5
        r.update({"dif": round(d, 3), "ee": round(e, 3), "ee_veces": round(d / e, 1) if e else None, "tres_veces": bool(e and abs(d) >= 3 * e), "pasa": bool(e and d > 0 and d >= 3 * e),
                  "media_verdad_4": round(st.mean(VE), 4), "media_falsa_4": round(st.mean(FA), 4), "dif_4": round(d, 4), "ee_4": round(e, 4)})
    else: r.update({"dif": None, "pasa": False})
    return r


R = {"puerta": {}, "cuentas": {}, "cambios": {}}
for nombre, fm in (("con_todas", False), ("sin_marcadas", True)):
    F = filas(fm)
    orig = r2(F, "original"); sel = SELLO[nombre]["R2"]
    ok = all(orig[k] == sel[k] for k in ("n_verdad", "n_falsa", "media_verdad", "media_falsa", "dif", "ee", "pasa"))
    R["puerta"][nombre] = {"reproduce_P7_56_sello": ok, "sello_json": sel, "esta_lectura": orig}
    if not ok: json.dump(R, open(os.path.join(AQUI, "P7_56_erratas.json"), "w"), ensure_ascii=False, indent=1); sys.exit(f"PUERTA: {nombre} no reproduce el R2 original; paro")
    R["cuentas"][nombre] = {"original": orig, "corregida": r2(F, "sello"), "variante_coger_cualquier_uso": r2(F, "v_coger_cualquiera"), "variante_racion_sin_condicion_de_golpes": r2(F, "v_racion_sin_golpes")}
    C = {}
    for f in F:
        k = f"{f['accion']} · {'V' if f['original'] else 'F'}→{'V' if f['sello'] else 'F'}"; C[k] = C.get(k, 0) + 1
    mot = {}
    for f in F:
        if f["motivo"] and f["accion"] in OBJ or (f["motivo"] or "").startswith("anillo"): kk = f"{f['accion']} · {f['motivo']}"; mot[kk] = mot.get(kk, 0) + 1
    usar = {}
    for f in F:
        if f["accion"] in ("USAR_BOTIQUIN", "USAR_RACION"): kk = f"{f['accion']} · calma {f['calma']} · anillo {f['anillo']} · promesa {'>0' if f['prom'] > 0 else '<=0'}"; usar[kk] = usar.get(kk, 0) + 1
    R["cambios"][nombre] = {"por_accion_original_a_corregida": dict(sorted(C.items())), "motivos_coger_y_quieta": dict(sorted(mot.items())), "usar_por_situacion": dict(sorted(usar.items())), "evaluaciones": len(F)}
R["otras_predicciones"] = {"R1": "no usa la funcion verdad (huellas del botiquin cortadas por un golpe)", "vigilancia": "no usa la funcion verdad"}
json.dump(R, open(os.path.join(AQUI, "P7_56_erratas.json"), "w"), ensure_ascii=False, indent=1)
for nombre in R["cuentas"]:
    print(nombre, "puerta", R["puerta"][nombre]["reproduce_P7_56_sello"])
    for k, x in R["cuentas"][nombre].items(): print("  ", k, x)
    print("   cambios", R["cambios"][nombre])
