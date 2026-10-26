"""[P7-46] LECTURA POR PRUEBA (exploratorio, sin sello) sobre P7_46_datos.json (banco_P7_46) -> P7_46_resumen.json. Por variante (BORRADO solo como referencia):
  1. SIN: forzadas que acaban (cogida / usada) frente a las que caducan, por tipo y objeto; por que caducan (diagnostico de la ventana de 240 tics, en este orden excluyente):
     ir: llega al destino y el zurron esta lleno (el cuerpo ofrece `hacer_sitio_*`, la forzada solo sabe `coger`) / llega y el cuerpo no ofrece `coger` / no llega y el objeto ya no esta
     a la vista / no llega, bloqueada (>= 24 pasos bloqueados) / no llega, la elegida no fue la forzada en la mitad o mas de los tics / no llega (lejos). usar: el cuerpo nunca ofrecio
     `usar_*` (y % de tics con hp a 100) / ofrecido y no elegido / otro.
  2. Aprendizaje por prueba (una prueba cortada, sin efecto medido, deja la creencia como estaba: se arrastra): creencia del cuerpo tras la 1.a, 3.a y 5.a prueba del botiquin y de la racion (mediana y media +- ee entre criaturas; APRENDE y SIN por criatura = serie x
     asiento a lo largo de los 20 dias; BORRADO por vida); cambio medio por prueba (k = 1..5; la creencia antes de la 1.a es 0).
  3. Eleccion: fraccion de pruebas (huellas) a red + camuflaje y a botiquin + racion por tramo de dias (1-5, 6-10, 11-15, 16-20); en SIN, ademas, el objeto de las forzadas.
  4. Cuando se prueba: fraccion de pruebas en calma (apertura P7-33 `calma`) frente a en peligro; y con hp0 < 50.
  5. R1 contado de nuevo: si SIN hubiera probado el botiquin tantas veces por vida como APRENDE (factor f = pruebas de botiquin por vida APRENDE / SIN), con su propia curva
     de aprendizaje (k* = primera prueba en la que la mediana de la creencia de SIN llega a 25; si no llega, la curva de APRENDE) y su propio calendario de pruebas escalado
     (c'(d) = f x pruebas acumuladas al dia d): dia* = primer dia con c'(d) >= k*, 21 si no. Solo cuenta; no simula partidas.
  python3 analiza_P7_46.py"""
import collections, json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__))
V = [v for v in json.load(open(os.path.join(AQUI, "P7_46_datos.json"))) if not v.get("sin_diario")]
VAR = ("TECHO", "BORRADO_v", "BORRADO_p", "APRENDE_v", "APRENDE_p", "SIN"); CAD = ("APRENDE_v", "APRENDE_p", "SIN"); TRAMOS = ((1, 5), (6, 10), (11, 15), (16, 20))
med = lambda xs: (st.median(xs) if xs else None); mean = lambda xs: (st.mean(xs) if xs else None); ee = lambda xs: (st.stdev(xs) / len(xs) ** 0.5 if len(xs) > 1 else None)
r3 = lambda x: (None if x is None else round(x, 3))


def vidas(var): return [v for v in V if v["variante"] == var]


# 1. SIN: forzadas
def diag(f):
    if f["fin"] != "caduca": return f["fin"]
    if f["tipo"] == "ir":
        if (f.get("tics_en_destino") or 0) > 0 and f.get("tics_hacer_sitio", 0) > 0: return "llega: zurrón lleno (hacer_sitio, sin coger)"
        if (f.get("tics_en_destino") or 0) > 0 and f.get("tics_coger_cand", 0) == 0: return "llega: el cuerpo no ofrece coger"
        if (f.get("tics_en_destino") or 0) > 0: return "llega: coger ofrecido y no cogido"
        if f.get("objeto_a_la_vista_al_fin") is False: return "no llega: el objeto ya no está a la vista"
        if f.get("tics_bloq", 0) >= 24: return "no llega: bloqueada (≥ 24 pasos)"
        if f.get("tics_elegida", 0) < 0.5 * f.get("tics", 1): return "no llega: la elegida no fue la forzada (≥ mitad de los tics)"
        return "no llega (lejos)"
    if f.get("tics_usar_cand", 0) == 0: return "usar nunca ofrecido por el cuerpo"
    if f.get("tics_elegida", 0) == 0: return "usar ofrecido y no elegido"
    return "usar elegido y no consumido"


FZ = [dict(f, serie=v["serie"], dia=v["dia"], asiento=v["asiento"]) for v in vidas("SIN") for f in v["forzadas"]]
# el "llega y el cuerpo no ofrece coger": ¿lo escondio la regla congelada del seis (`llena8`, arreglos_P6_8b: coger se esconde si la prevision dice que la mochila no cambia)?
# se leen solo esas ventanas en sus diarios (registro `llena8` entre t0 y t_fin)
import glob
RUNS = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "paintball", "runs")
def llena8_en_ventana(v, f):
    c = glob.glob(os.path.join(RUNS, f"P741_s{v['serie']}_d{v['dia']}_SIN_*", f"*policy_agent_{v['asiento']}.art.log"))
    if not c: return None
    n = 0; motivos = collections.Counter()
    for line in open(c[0], errors="replace"):
        if line.startswith('{"k":"llena8"'):
            r = json.loads(line)
            if f["t0"] <= r.get("tick", -1) <= f.get("t_fin", f["t0"]): n += 1; motivos[r.get("motivo") or r.get("estado")] += 1
    return n, dict(motivos)
LL = collections.Counter(); LLm = collections.Counter()
for v in vidas("SIN"):
    for f in v["forzadas"]:
        if f["tipo"] == "ir" and diag(f) == "llega: el cuerpo no ofrece coger":
            r = llena8_en_ventana(v, f); LL["con llena8" if r and r[0] else "sin llena8"] += 1
            if r: LLm.update(r[1])
forz = {"n": len(FZ), "por_vida": len(FZ) / max(1, len(vidas("SIN"))), "por_tipo_fin": {t: dict(collections.Counter(f["fin"] for f in FZ if f["tipo"] == t)) for t in ("ir", "usar")},
        "por_objeto_fin": {o: dict(collections.Counter(f["fin"] for f in FZ if f["objeto"] == o)) for o in ("botiquin", "racion", "red", "camuflaje")},
        "acaban": sum(1 for f in FZ if f["fin"] in ("cogida", "usada")), "caducan": sum(1 for f in FZ if f["fin"] == "caduca"), "sin_fin": sum(1 for f in FZ if f["fin"].startswith("sin fin")),
        "duracion_media_acaban": mean([f["duracion"] for f in FZ if f["fin"] in ("cogida", "usada") and f.get("duracion") is not None]),
        "por_que_caducan": {t: dict(collections.Counter(diag(f) for f in FZ if f["tipo"] == t and f["fin"] == "caduca").most_common()) for t in ("ir", "usar")},
        "usar_caduca_hp_100_pct_tics": mean([100 * f["tics_hp_100"] / f["tics"] for f in FZ if f["tipo"] == "usar" and f["fin"] == "caduca" and f.get("tics")]),
        "usar_acaba_hp0_media": mean([f["hp0"] for f in FZ if f["tipo"] == "usar" and f["fin"] == "usada" and f.get("hp0") is not None]), "usar_caduca_hp0_media": mean([f["hp0"] for f in FZ if f["tipo"] == "usar" and f["fin"] == "caduca" and f.get("hp0") is not None]),
        "ir_caduca_d0_media": mean([f["d0"] for f in FZ if f["tipo"] == "ir" and f["fin"] == "caduca" and f.get("d0") is not None]), "ir_cogida_d0_media": mean([f["d0"] for f in FZ if f["tipo"] == "ir" and f["fin"] == "cogida" and f.get("d0") is not None]),
        "forzadas_con_huella_mismo_objeto_240": None, "llega_sin_coger_llena8": dict(LL), "llega_sin_coger_llena8_motivos": dict(LLm)}
# forzadas que acaban y dejan huella del mismo objeto dentro de la ventana (la prueba de verdad)
def con_huella(v, f): return any(h["objeto"] == f["objeto"] and f["t0"] <= h["t0"] <= f.get("t_fin", f["t0"]) + 240 for h in v["huellas"])
ac = [(v, f) for v in vidas("SIN") for f in v["forzadas"] if f["fin"] in ("cogida", "usada")]
forz["forzadas_con_huella_mismo_objeto_240"] = {"acaban": len(ac), "con_huella": sum(1 for v, f in ac if con_huella(v, f)), "por_tipo": {t: (sum(1 for v, f in ac if f["tipo"] == t and con_huella(v, f)), sum(1 for v, f in ac if f["tipo"] == t)) for t in ("ir", "usar")}}


# 2. aprendizaje por prueba
def rellena(cs):
    """una prueba cortada (sin efecto medido) deja la creencia como estaba: se arrastra la ultima conocida (0 antes de la primera)."""
    out = []; ult = 0.0
    for c in cs:
        if c is not None: ult = c
        out.append(ult)
    return out


def secuencias(var, objeto):
    """lista de secuencias de creencia tras cada prueba por criatura (APRENDE/SIN: serie x asiento, 20 dias en orden; BORRADO y TECHO: por vida); las cortadas arrastran la anterior."""
    out = []
    if var in CAD:
        for S in (1, 2, 3):
            for sl in (10, 11):
                vs = sorted([v for v in vidas(var) if v["serie"] == S and v["asiento"] == sl], key=lambda v: v["dia"])
                hs = [h for v in vs for h in sorted(v["huellas"], key=lambda h: h["t0"]) if h["objeto"] == objeto]
                out.append({"criatura": f"s{S}a{sl}", "dias": [(v["dia"], sum(1 for h in v["huellas"] if h["objeto"] == objeto)) for v in vs], "creencias": rellena([h["creencia_despues"] for h in hs]), "sin_efecto": sum(1 for h in hs if h["creencia_despues"] is None), "cortes": sum(1 for h in hs if h["corte"])})
    else:
        for v in vidas(var):
            hs = [h for h in sorted(v["huellas"], key=lambda h: h["t0"]) if h["objeto"] == objeto]
            if hs: out.append({"criatura": f"s{v['serie']}d{v['dia']}a{v['asiento']}", "creencias": rellena([h["creencia_despues"] for h in hs]), "sin_efecto": sum(1 for h in hs if h["creencia_despues"] is None), "cortes": sum(1 for h in hs if h["corte"])})
    return out


def aprendizaje(var, objeto):
    seqs = secuencias(var, objeto); R = {"criaturas": len(seqs), "tras": {}, "cambio_por_prueba": {}}
    for k in (1, 2, 3, 4, 5):
        xs = [s["creencias"][k - 1] for s in seqs if len(s["creencias"]) >= k and s["creencias"][k - 1] is not None]
        R["tras"][k] = {"n": len(xs), "mediana": r3(med(xs)), "media": r3(mean(xs)), "ee": r3(ee(xs))}
        dx = [(s["creencias"][k - 1] or 0) - ((s["creencias"][k - 2] or 0) if k > 1 else 0) for s in seqs if len(s["creencias"]) >= k and s["creencias"][k - 1] is not None]
        R["cambio_por_prueba"][k] = {"n": len(dx), "media": r3(mean(dx)), "ee": r3(ee(dx))}
    todos = [(s["creencias"][i] or 0) - ((s["creencias"][i - 1] or 0) if i else 0) for s in seqs for i in range(len(s["creencias"])) if s["creencias"][i] is not None]
    R["cambio_medio_todas"] = {"n": len(todos), "media": r3(mean(todos)), "ee": r3(ee(todos))}
    R["pruebas_por_criatura"] = r3(mean([len(s["creencias"]) for s in seqs])) if seqs else None
    R["pruebas_sin_efecto_pct"] = r3(100 * sum(s["sin_efecto"] for s in seqs) / max(1, sum(len(s["creencias"]) for s in seqs)))
    R["primera_k_a_25"] = [next((i + 1 for i, c in enumerate(s["creencias"]) if c is not None and c >= (25.0 if objeto == "botiquin" else 7.5)), None) for s in seqs]
    return R


APR = {var: {o: aprendizaje(var, o) for o in ("botiquin", "racion")} for var in VAR if var != "TECHO"}

# 3. eleccion por tramo
def eleccion(var):
    R = {}
    for a, b in TRAMOS:
        hs = [h for v in vidas(var) if a <= v["dia"] <= b for h in v["huellas"]]; n = len(hs)
        R[f"d{a}-{b}"] = {"n": n, "red_camuflaje": r3(sum(1 for h in hs if h["objeto"] in ("red", "camuflaje")) / n) if n else None, "botiquin_racion": r3(sum(1 for h in hs if h["objeto"] in ("botiquin", "racion")) / n) if n else None,
                         "por_objeto": {o: sum(1 for h in hs if h["objeto"] == o) for o in ("botiquin", "racion", "red", "camuflaje")}, "vidas": sum(1 for v in vidas(var) if a <= v["dia"] <= b)}
    hs = [h for v in vidas(var) for h in v["huellas"]]; n = len(hs)
    R["todos"] = {"n": n, "red_camuflaje": r3(sum(1 for h in hs if h["objeto"] in ("red", "camuflaje")) / n) if n else None, "botiquin_racion": r3(sum(1 for h in hs if h["objeto"] in ("botiquin", "racion")) / n) if n else None, "por_objeto": {o: sum(1 for h in hs if h["objeto"] == o) for o in ("botiquin", "racion", "red", "camuflaje")}, "vidas": len(vidas(var))}
    return R
ELE = {var: eleccion(var) for var in VAR}
ELE["SIN_forzadas_por_objeto"] = {o: sum(1 for f in FZ if f["objeto"] == o) for o in ("botiquin", "racion", "red", "camuflaje")}
ELE["SIN_forzadas_por_tramo"] = {f"d{a}-{b}": {"n": sum(1 for f in FZ if a <= f["dia"] <= b), "red_camuflaje": r3(sum(1 for f in FZ if a <= f["dia"] <= b and f["objeto"] in ("red", "camuflaje")) / max(1, sum(1 for f in FZ if a <= f["dia"] <= b)))} for a, b in TRAMOS}

# 4. cuando
def cuando(var):
    hs = [h for v in vidas(var) for h in v["huellas"]]; con = [h for h in hs if h["calma"] is not None]
    R = {"pruebas": len(hs), "con_apertura": len(con), "calma": r3(sum(1 for h in con if h["calma"]) / len(con)) if con else None, "peligro": r3(sum(1 for h in con if not h["calma"]) / len(con)) if con else None,
         "rival_a_4": r3(sum(1 for h in con if (h["peligro"] or {}).get("rival_a_4")) / len(con)) if con else None, "fuego": r3(sum(1 for h in con if (h["peligro"] or {}).get("fuego")) / len(con)) if con else None, "vida_menor_30": r3(sum(1 for h in con if (h["peligro"] or {}).get("vida_menor_30")) / len(con)) if con else None,
         "hp0_menor_50": r3(sum(1 for h in hs if h["hp0"] is not None and h["hp0"] < 50) / len(hs)) if hs else None,
         "por_objeto_calma": {o: (r3(sum(1 for h in con if h["objeto"] == o and h["calma"]) / max(1, sum(1 for h in con if h["objeto"] == o))) if any(h["objeto"] == o for h in con) else None) for o in ("botiquin", "racion", "red", "camuflaje")}}
    return R
CUA = {var: cuando(var) for var in VAR}

# 5. R1 contado de nuevo
def pruebas_botiquin_por_vida(var): return sum(1 for v in vidas(var) for h in v["huellas"] if h["objeto"] == "botiquin") / max(1, len(vidas(var)))
pb = {var: pruebas_botiquin_por_vida(var) for var in CAD}
def curva(var):
    seqs = secuencias(var, "botiquin"); out = {}
    for k in range(1, 40):
        xs = [s["creencias"][k - 1] for s in seqs if len(s["creencias"]) >= k and s["creencias"][k - 1] is not None]
        if len(xs) < 3: break
        out[k] = (med(xs), len(xs))
    return out
CUR = {var: curva(var) for var in CAD}
def k_estrella(var): return next((k for k, (m, n_) in CUR[var].items() if m is not None and m >= 25.0), None)
def rapidez_real(var):
    out = []
    for S in (1, 2, 3):
        for sl in (10, 11):
            vs = sorted([v for v in vidas(var) if v["serie"] == S and v["asiento"] == sl], key=lambda v: v["dia"])
            out.append(next((v["dia"] for v in vs if (v["al_cerrar"]["botiquin"] or -1) >= 25.0), 21))
    return out
def rapidez_contada(var, f, kstar):
    out = []
    for s in secuencias(var, "botiquin"):
        acum = 0; dia = 21
        for d, n_ in s["dias"]:
            acum += n_
            if f * acum >= kstar: dia = d; break
        out.append(dia)
    return out
R1 = {"pruebas_botiquin_por_vida": {v: r3(pb[v]) for v in CAD}, "factor": {v: r3(pb[v] / pb["SIN"]) for v in ("APRENDE_p", "APRENDE_v")}, "k_estrella": {v: k_estrella(v) for v in CAD}, "curva_mediana": {v: {k: (r3(m), n_) for k, (m, n_) in CUR[v].items()} for v in CAD},
      "rapidez_real": {v: rapidez_real(v) for v in CAD}, "rapidez_real_media": {v: r3(mean(rapidez_real(v))) for v in CAD}}
# la cuenta con cada k* (la curva de cada cadena da un k* distinto: se dan los tres, y para cada uno la comprobacion con f = 1 sobre SIN y sobre la cadena que presta la curva)
R1["contada"] = {}
for fuente in CAD:
    kS = R1["k_estrella"][fuente]
    if not kS: R1["contada"][fuente] = None; continue
    fila = {"k": kS, "SIN_f1_dias": rapidez_contada("SIN", 1.0, kS), "propia_f1_dias": rapidez_contada(fuente, 1.0, kS), "propia_real_media": r3(mean(rapidez_real(fuente)))}
    fila["SIN_f1_media"] = r3(mean(fila["SIN_f1_dias"])); fila["propia_f1_media"] = r3(mean(fila["propia_f1_dias"]))
    for v in ("APRENDE_p", "APRENDE_v"):
        f = pb[v] / pb["SIN"]; sin_c = rapidez_contada("SIN", f, kS)
        fila[v] = {"f": r3(f), "SIN_contada_dias": sin_c, "SIN_contada_media": r3(mean(sin_c)), "R1_real": r3(mean(rapidez_real(v)) - mean(rapidez_real("SIN"))), "R1_contada": r3(mean(rapidez_real(v)) - mean(sin_c)), "ee_contada": r3(((ee(rapidez_real(v)) or 0) ** 2 + (ee(sin_c) or 0) ** 2) ** 0.5)}
    R1["contada"][fuente] = fila
R1["SIN_real_media"] = r3(mean(rapidez_real("SIN")))

R = {"vidas": len(V), "forzadas_SIN": forz, "aprendizaje": APR, "eleccion": ELE, "cuando": CUA, "R1": R1}
json.dump(R, open(os.path.join(AQUI, "P7_46_resumen.json"), "w"), ensure_ascii=False, indent=1)
print("forzadas", {k: v for k, v in forz.items() if k in ("n", "acaban", "caducan", "sin_fin", "por_tipo_fin")}); print("por que caducan", forz["por_que_caducan"]); print("huella tras forzada", forz["forzadas_con_huella_mismo_objeto_240"])
for var in APR: print(var, "botiquin tras 1/3/5", [APR[var]["botiquin"]["tras"][k]["mediana"] for k in (1, 3, 5)], "n", [APR[var]["botiquin"]["tras"][k]["n"] for k in (1, 3, 5)], "cambio medio", APR[var]["botiquin"]["cambio_medio_todas"])
for var in VAR: print(var, "eleccion", {t: (x["n"], x["red_camuflaje"]) for t, x in ELE[var].items()}, "calma", CUA[var]["calma"], CUA[var]["con_apertura"])
print("R1", {k: v for k, v in R1.items() if k not in ("curva_mediana", "rapidez_real")})
