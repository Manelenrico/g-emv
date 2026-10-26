"""[P7-56 erratas, addendum 1] La misma funcion corregida (verdad_sello de erratas_P7_56.py, leida de su fuente) en dos sitios que usaban analiza_P7_56.verdad:
  1. P7-59 (compara_P7_59.py): verdad en el mundo con nombres (P7_54_razon.json) y a ciegas (P7_59_razon.json).
     Son invitaciones de un banco que nunca se jugaron: COGER con promesa de cuerpo > 0 no tiene «uso posterior» que mirar -> NO JUZGABLE; se dan aparte y con sus dos cotas.
  2. P7-65 (analiza_P7_65.py): L4, cuenta principal y sin la partida marcada. L4 cuenta invitaciones CARGADAS (aceptadas o no). Ancla del «uso posterior» de COGER con cuerpo > 0:
     la primera aceptacion de esa invitacion en esa vida; si no se acepto, su primera activacion; si nunca se activo, el principio de la vida (tic 0). Variante no sellada: ancla en la
     primera activacion para todas (si nunca se activo, tic 0).
  Variante no sellada en los dos: USAR_RACION sin la condicion de golpes (regla del mundo de P7-62), como en erratas_P7_56.py.
  Puerta: con la funcion vieja, cada recalculo reproduce primero la cifra publicada (P7_59_compara.json; P7_65_sello.json L4 en las dos cuentas). Si no, para.
  3. P7-56: la lista de las evaluaciones que cambian de clase (todas las partidas), para la cantera.
  No toca compara_P7_59.py, analiza_P7_65.py, ni sus JSON.  python3 erratas_P7_56_b.py -> P7_56_erratas_b.json"""
import glob, json, math, os, sys, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
s56 = open(os.path.join(AQUI, "analiza_P7_56.py")).read(); ns0 = {}; exec(s56[s56.index("def verdad"):s56.index("\n\n\ndef vida")], ns0); verdad_original = ns0["verdad"]
se = open(os.path.join(AQUI, "erratas_P7_56.py")).read(); nsE = {}
exec('OBJ = {"COGER_BOTIQUIN": "first_aid", "COGER_RACION": "rations"}\n' + se[se.index("def sin_golpes"):se.index("\n\n\nV = {}")], nsE); verdad_sello = nsE["verdad_sello"]; OBJ = nsE["OBJ"]
R = {"puerta": {}}


def para(msg): json.dump(R, open(os.path.join(AQUI, "P7_56_erratas_b.json"), "w"), ensure_ascii=False, indent=1); sys.exit("PUERTA: " + msg + "; paro")


# ── 1. P7-59 ──
PUB59 = json.load(open(os.path.join(AQUI, "P7_59_compara.json")))
def p59(fich, clave):
    Rz = json.load(open(os.path.join(AQUI, fich))); inv = [p for r in Rz for p in r["invitaciones"]]
    vo = sum(1 for p in inv if verdad_original(p["accion"], {"anillo": p["anillo"], "calma": p["calma"]}, p["cuerpo"]))
    R["puerta"][f"P7-59 {clave}"] = {"publicado": [PUB59[clave]["verdad"], PUB59[clave]["invitaciones"]], "funcion_vieja": [vo, len(inv)]}
    if (vo, len(inv)) != (PUB59[clave]["verdad"], PUB59[clave]["invitaciones"]): para(f"P7-59 {clave} no reproduce")
    v = f = nj = vr = 0; cambios = {}; nj_acc = {}
    for p in inv:
        sit = {"anillo": p["anillo"], "calma": p["calma"]}; prom = float(p["cuerpo"] or 0)
        if p["accion"] in OBJ and prom > 0: nj += 1; nj_acc[p["accion"]] = nj_acc.get(p["accion"], 0) + 1; continue
        n, _ = verdad_sello(p["accion"], sit, prom, None, None); o = bool(verdad_original(p["accion"], sit, p["cuerpo"]))
        nr, _ = verdad_sello(p["accion"], sit, prom, None, None, racion_sin_golpes=False); vr += bool(nr)
        v += bool(n); f += (not n)
        if o != bool(n): k = f"{p['accion']} · {'V' if o else 'F'}→{'V' if n else 'F'} · calma {p['calma']} · anillo {p['anillo']}"; cambios[k] = cambios.get(k, 0) + 1
    return {"invitaciones": len(inv), "original_verdad": vo, "corregida_verdad": v, "corregida_falsa": f, "no_juzgables": nj, "no_juzgables_por_accion": nj_acc,
            "cota_baja_verdad": v, "cota_alta_verdad": v + nj, "cambios": cambios,
            "variante_racion_sin_condicion_de_golpes_verdad": vr}
R["P7_59"] = {"con_nombres": p59("P7_54_razon.json", "con_nombres"), "a_ciegas": p59("P7_59_razon.json", "a_ciegas")}

# ── 2. P7-65, L4 ──
s65 = open(os.path.join(AQUI, "analiza_P7_65.py")).read(); ns = {"__file__": os.path.join(AQUI, "analiza_P7_65.py"), "__name__": "analiza_P7_65_lectura"}
exec(s65[:s65.index("\n\n\nV = {}")], ns)
PUB65 = json.load(open(os.path.join(AQUI, "P7_65_sello.json")))
V = {}; H = {}
for p in ns["E"]["peticiones"]:
    if p["estado"] != "completed" or p["serie"] not in ns["SERIES"]: continue
    for sl in (10, 11):
        v = ns["vida"](p, sl)
        if not v: continue
        k = (p["serie"], p["dia"], p["brazo"], sl); V[k] = v
        f = glob.glob(os.path.join(ns["RUNS"], f"P765_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}", f"*policy_agent_{sl}.art.log"))[0]
        H[k] = [json.loads(l) for l in open(f, errors="replace") if l.startswith('{"k":"P7_huella"')]
exec(s65[s65.index("def fuera"):s65.index("\n\n\ndef principales")], ns)      # veredicto, como en el original
MARCADA = ns["MARCADA"]; COGER = ns["COGER"]; SERIES = ns["SERIES"]; r4 = ns["r4"]


def juicio(k, v, i, inv, modo):
    if modo == "vieja": return bool(verdad_original(inv["accion"], {"anillo": inv.get("anillo"), "calma": inv.get("calma")}, inv.get("cuerpo")))
    acc = v["acc"].get(i) or []; act = v["act"].get(i)
    t = (min(acc) if acc else (act if act is not None else 0)) if modo == "sello" else (act if act is not None else 0)
    n, _ = verdad_sello(inv["accion"], {"anillo": inv.get("anillo"), "calma": inv.get("calma")}, inv.get("cuerpo"), {"AC": [{"n": i, "tick": t}], "H": H[k]}, {"n": i, "tick": t})
    return bool(n)


def L4(sin_marcada, modo):
    def l4(S, b):
        tot = acc = 0; tv = 0
        for d in range(12, 21):
            k = (S, d, b, 11); v = V.get(k)
            if not v or (sin_marcada and (k[0], k[1], k[2]) == MARCADA): continue
            ac = set(n for n, ts in v["acc"].items() if ts)
            for i, inv in enumerate(v["inv"]):
                if inv.get("falsa") or inv["accion"] not in COGER: continue
                if juicio(k, v, i, inv, modo): tot += 1; acc += (i in ac)
        return (acc / tot if tot else None), tot
    A = [l4(S, "MIENTEN_DOS") for S in SERIES]; B = [l4(S, "MIENTE_UNA") for S in SERIES]
    xa = [x for x, _ in A if x is not None]; xb = [x for x, _ in B if x is not None]
    ea = st.stdev(xa) / math.sqrt(len(xa)); eb = st.stdev(xb) / math.sqrt(len(xb)); dif = st.mean(xa) - st.mean(xb); e = math.sqrt(ea * ea + eb * eb)
    r = {"MIENTEN_DOS_prudente": [r4(x) for x in xa], "cargadas_A": [t for _, t in A], "MIENTE_UNA_prudente": [r4(x) for x in xb], "cargadas_B": [t for _, t in B],
         "media_A": r4(st.mean(xa)), "media_B": r4(st.mean(xb)), "media": r4(dif), "ee": r4(e), "en_ee": r4(abs(dif) / e) if e else None}
    r["veredicto"] = ns["veredicto"](r); return r


R["P7_65_L4"] = {}
for nombre, sm in (("principal", False), ("sin_la_partida_marcada", True)):
    vie = L4(sm, "vieja"); pub = PUB65[nombre]["L4"]
    R["puerta"][f"P7-65 L4 {nombre}"] = {"publicado": {x: pub[x] for x in ("media", "ee", "veredicto")}, "funcion_vieja": {x: vie[x] for x in ("media", "ee", "veredicto")}}
    if any(vie[x] != pub[x] for x in ("MIENTEN_DOS_prudente", "cargadas_A", "MIENTE_UNA_prudente", "cargadas_B", "media", "ee", "veredicto")): para(f"P7-65 L4 {nombre} no reproduce")
    R["P7_65_L4"][nombre] = {"original": vie, "corregida": L4(sm, "sello"), "variante_ancla_activacion": L4(sm, "activacion")}
# cuantas cambian (cargadas de coger, prudente, d12-20, los dos brazos)
cam = {}
for k, v in V.items():
    if k[3] != 11 or not (12 <= k[1] <= 20): continue
    for i, inv in enumerate(v["inv"]):
        if inv.get("falsa") or inv["accion"] not in COGER: continue
        o = juicio(k, v, i, inv, "vieja"); n = juicio(k, v, i, inv, "sello")
        kk = f"{inv['accion']} · {'V' if o else 'F'}→{'V' if n else 'F'}"; cam[kk] = cam.get(kk, 0) + 1
R["P7_65_L4"]["cambios_cargadas"] = dict(sorted(cam.items()))
# ── 3. P7-56: la lista de las que cambian (todas las partidas), con las mismas funciones de erratas_P7_56.py ──
ns56 = {"__file__": os.path.join(AQUI, "erratas_P7_56.py"), "__name__": "erratas_P7_56_lectura"}; exec(se[:se.index("\n\n\nR = {")], ns56)
L = [f for f in ns56["filas"](False) if f["original"] != f["sello"]]
R["P7_56_lista_cambian"] = [{"serie": f["S"], "dia": f["d"], "asiento": f["sl"], "accion": f["accion"], "promesa_cuerpo": f["prom"], "calma": f["calma"], "anillo": f["anillo"],
                             "motivo": f["motivo"], "confianza_despues_cuerpo": round(f["conf"], 4), "original": f["original"], "corregida": f["sello"]} for f in sorted(L, key=lambda f: (f["S"], f["d"], f["sl"], f["accion"]))]
R["P7_56_lista_n"] = len(L)
json.dump(R, open(os.path.join(AQUI, "P7_56_erratas_b.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(R["puerta"], ensure_ascii=False)); print(json.dumps(R["P7_59"], ensure_ascii=False))
for n, x in R["P7_65_L4"].items(): print(n, x if n == "cambios_cargadas" else {kk: {z: x[kk][z] for z in ("cargadas_A", "cargadas_B", "media_A", "media_B", "media", "ee", "en_ee", "veredicto")} for kk in x})
