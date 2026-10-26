"""[P7 figuras] Las figuras 3.1, 5.2 y 5.3 del paper siete, en español y en inglés, solo desde datos que ya existen (no juega partidas, no toca el cuerpo ni el motor,
no modifica ningún guion de los experimentos). Escribe fig3_1_*, fig5_2_*, fig5_3_* (PNG a 300 ppp y PDF), figuras_P7_valores.json e informe_P7_figuras.md en esta carpeta.
Cada figura pasa antes su comprobación obligatoria; si una no pasa, el programa para sin dibujar y lo dice.
  Fig. 5.2: P7_67_analisis.json (analiza_P7_67.py, sellado) -> criatura_dias_detalle, nivel 1, MIENTE y CONGELADA, llegadas sumadas por tramos de 5 días (como escribe_informe_P7_67_campo.py:28-33).
  Fig. 5.3: el mismo detalle, conf_arranque.recursos, media por criatura-día de las 32 criaturas de cada día (como analiza_P7_67.py:170-174); banda ± 1 ee con la serie como unidad.
  Fig. 3.1: fórmula antigua = P7_46_resumen.json R1.curva_mediana (analiza_P7_46.py:146-153,171); escala propia = la misma curva mediana sobre los cuadernos guardados de la cadena
            de P7-47 (P7_47_res), con creencia_dentro de analiza_P7_47.py:13 sin cortar en el cruce (analiza_P7_47.py:29-36 corta en el cruce). No se vuelve a ejecutar ninguna réplica.
  Repetible: mismos datos -> mismos bytes (metadatos de fecha anulados).   python3 hace_figuras_P7.py"""
import hashlib, json, os, statistics as st, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__)); P7 = os.path.dirname(AQUI)
ACENTO = "#1f6f78"; GRIS = "#7a7a7a"; NEGRO = "#000000"
CM = 1 / 2.54; TAM = (16 * CM, 9 * CM)
matplotlib.rcParams.update({"font.size": 11, "axes.labelsize": 11, "xtick.labelsize": 11, "ytick.labelsize": 11, "font.family": "DejaVu Sans", "pdf.fonttype": 42,
                            "svg.hashsalt": "P7", "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False, "figure.facecolor": "white", "axes.facecolor": "white"})
T = {"es": {"MIENTE": "razón que miente", "CONGELADA": "confianza congelada", "HONESTA": "razón honesta", "dias": "días", "llegadas": "llegadas al sitio de la mentira",
            "confianza": "confianza en lo que la razón dice de los recursos", "pruebas": "pruebas del botiquín", "cree": "lo que cree que cura (fracción de lo que cura)",
            "antigua": "fórmula antigua", "propia": "escala propia", "prudente": "prudente", "valiente": "valiente"},
     "en": {"MIENTE": "lying reason", "CONGELADA": "frozen trust", "HONESTA": "honest reason", "dias": "days", "llegadas": "arrivals at the lie's destination",
            "confianza": "trust in what the reason says about resources", "pruebas": "medkit trials", "cree": "what it believes it cures (fraction of the true cure)",
            "antigua": "old formula", "propia": "own scale", "prudente": "cautious", "valiente": "brave"}}
CURA = 50.0          # lo que cura el botiquín (regla del mundo, informe_P7_62.md:17); la mitad, 25, es el umbral de P7-46 y P7-47
BLOQUES = ((1, 5), (6, 10), (11, 15), (16, 20))


def para(msg): sys.exit("COMPROBACIÓN OBLIGATORIA NO PASA: " + msg + ". No se dibuja nada.")


# ── datos de P7-67 ──
A = json.load(open(os.path.join(P7, "P7_67_analisis.json")))
CD = [c for c in A["criatura_dias_detalle"] if c["nivel"] == "1"]
F52 = {}; OFR = {}
for b in ("MIENTE", "CONGELADA", "HONESTA"):
    for lo, hi in BLOQUES:
        cs = [c for c in CD if c["brazo"] == b and lo <= c["dia"] <= hi]
        F52[(b, lo)] = sum(c["llegadas"] for c in cs)
        OFR[(b, lo)] = {"criatura_dias": len(cs), "con_oferta": sum(1 for c in cs if c["oportunidad"]), "aceptaciones": sum(c["aceptadas"] for c in cs), "llegadas": F52[(b, lo)],
                        "dias_sin_oferta": sorted({c["dia"] for c in cs if not c["oportunidad"]})}
ESPERA52 = {"MIENTE": [73, 16, 15, 2], "CONGELADA": [112, 143, 153, 113]}
SALE52 = {b: [F52[(b, lo)] for lo, _ in BLOQUES] for b in ESPERA52}
if SALE52 != ESPERA52: para(f"figura 5.2: sale {SALE52}, se esperaba {ESPERA52}")

F53 = {}
for b in ("MIENTE", "CONGELADA", "HONESTA"):
    for d in range(1, 21):
        cs = [c for c in CD if c["brazo"] == b and c["dia"] == d and c["conf_arranque"]]
        xs = [float(c["conf_arranque"]["recursos"]) for c in cs]
        por_serie = {}
        for c in cs: por_serie.setdefault(c["serie"], []).append(float(c["conf_arranque"]["recursos"]))
        ms = [st.mean(v) for _, v in sorted(por_serie.items())]
        F53[(b, d)] = {"media": st.mean(xs), "n_criaturas": len(xs), "n_series": len(ms), "ee_serie": (st.stdev(ms) / len(ms) ** 0.5) if len(ms) > 1 else 0.0}
c53 = {"MIENTE": round(F53[("MIENTE", 20)]["media"], 3), "HONESTA": round(F53[("HONESTA", 20)]["media"], 3)}
plana = all(abs(F53[("CONGELADA", d)]["media"] - 0.5) < 1e-12 for d in range(1, 21))
ref = A["confianza_dia_a_dia"]
igual_informe = all(round(F53[(b, d)]["media"], 4) == ref[b]["recursos"][str(d)] for b in ("MIENTE", "CONGELADA", "HONESTA") for d in range(1, 21))
if c53 != {"MIENTE": 0.157, "HONESTA": 0.838} or not plana or not igual_informe: para(f"figura 5.3: día 20 {c53}, CONGELADA plana {plana}, igual a P7_67_analisis {igual_informe}")

# ── datos de P7-46 (fórmula antigua) y P7-47 (escala propia) ──
R46 = json.load(open(os.path.join(P7, "P7_46_resumen.json")))["R1"]
VIEJA = {v: [(int(k), m, n) for k, (m, n) in sorted(R46["curva_mediana"][v].items(), key=lambda x: int(x[0]))] for v in ("APRENDE_p", "APRENDE_v")}
src = open(os.path.join(P7, "analiza_P7_47.py")).read(); ns = {"__file__": os.path.join(P7, "analiza_P7_47.py"), "__name__": "analiza_P7_47_lectura"}
exec(src[:src.index("\n\nR = {")], ns)
CURV = {}
for var in ("APRENDE_v", "APRENDE_p"):
    for s in (1, 2, 3):
        for sl in (10, 11):
            cu, _ = ns["ultimo_cuaderno"](ns["RES"], var, s, sl)
            sits = ((cu.get("objetos") or {}).get("first_aid") or {}).get("situaciones") or {}
            recs = sorted([dict(r, _sit=k) for k, L in sits.items() for r in L if not r.get("corte")], key=lambda r: (int(r["dia"]), int(r.get("tick") or 0)))
            CURV[(var, s, sl)] = [ns["creencia_dentro"](recs[:k], int(recs[k - 1]["dia"])) for k in range(1, len(recs) + 1)]
S47 = json.load(open(os.path.join(P7, "P7_47_sello.json")))["criaturas"]
for (var, s, sl), c in CURV.items():
    g = S47[f"{var} s{s} a{sl}"]["curva"]
    if c[:len(g)] != g: para(f"figura 3.1: la creencia recalculada de {var} s{s} a{sl} no coincide con la curva guardada en P7_47_sello.json")


def mediana(claves):
    out = []
    for k in range(1, 100):
        xs = [CURV[c][k - 1] for c in claves if len(CURV[c]) >= k and CURV[c][k - 1] is not None]
        if len(xs) < 3: break          # como analiza_P7_46.py:150 (al menos 3 criaturas)
        out.append((k, st.median(xs), len(xs)))
    return out


PROPIA = mediana(sorted(CURV)); PROPIA_v = mediana(sorted(c for c in CURV if c[0] == "APRENDE_v")); PROPIA_p = mediana(sorted(c for c in CURV if c[0] == "APRENDE_p"))
cruce = lambda cur: next((k for k, m, _ in cur if m is not None and m >= CURA / 2), None)
c31 = {"antigua_prudente": cruce(VIEJA["APRENDE_p"]), "antigua_valiente": cruce(VIEJA["APRENDE_v"]), "propia": cruce(PROPIA)}
if c31["antigua_prudente"] != 17 or c31["antigua_valiente"] != 30 or c31["propia"] not in (8, 9): para(f"figura 3.1: cruces {c31}")

# ── 3.1, revisión: la fórmula antigua contada como la escala propia (solo pruebas no cortadas) ──
D46 = [v for v in json.load(open(os.path.join(P7, "P7_46_datos.json"))) if not v.get("sin_diario")]
s46 = open(os.path.join(P7, "analiza_P7_46.py")).read(); ns46 = {}; exec(s46[s46.index("def rellena"):s46.index("\n\n\ndef secuencias")], ns46); rellena = ns46["rellena"]


def mediana_de(seqs):
    out = []
    for k in range(1, 100):
        xs = [q[k - 1] for q in seqs if len(q) >= k and q[k - 1] is not None]
        if len(xs) < 3: break
        out.append((k, st.median(xs), len(xs)))
    return out


VIEJA_NC = {}; CORTES = {}
for var in ("APRENDE_p", "APRENDE_v"):
    todas = []; sin_cortes = []; CORTES[var] = {"criaturas": {}, "pruebas": 0, "cortadas": 0, "cortadas_con_creencia": 0, "cortadas_que_mueven_la_creencia": 0}
    for S in (1, 2, 3):
        for sl in (10, 11):
            vs = sorted([v for v in D46 if v["variante"] == var and v["serie"] == S and v["asiento"] == sl], key=lambda v: v["dia"])
            hs = [h for v in vs for h in sorted(v["huellas"], key=lambda h: h["t0"]) if h["objeto"] == "botiquin"]      # como analiza_P7_46.py:93
            todas.append(rellena([h["creencia_despues"] for h in hs])); sin_cortes.append(rellena([h["creencia_despues"] for h in hs if not h["corte"]]))
            nc = sum(1 for h in hs if h["corte"]); CORTES[var]["criaturas"][f"s{S} a{sl}"] = {"pruebas": len(hs), "cortadas": nc}; CORTES[var]["pruebas"] += len(hs); CORTES[var]["cortadas"] += nc
            prev = 0.0
            for h in hs:
                c = h["creencia_despues"]
                if h["corte"] and c is not None:
                    CORTES[var]["cortadas_con_creencia"] += 1; CORTES[var]["cortadas_que_mueven_la_creencia"] += abs(c - prev) > 1e-6
                if c is not None: prev = c
    if [(k, round(m, 3), n_) for k, m, n_ in mediana_de(todas)] != [(k, m, n_) for k, m, n_ in VIEJA[var]]:
        para(f"figura 3.1 (revisión): la curva de {var} recalculada desde P7_46_datos.json no reproduce la guardada en P7_46_resumen.json")
    VIEJA_NC[var] = [(k, round(m, 3), n_) for k, m, n_ in mediana_de(sin_cortes)]
c31b = {"antigua_prudente": cruce(VIEJA_NC["APRENDE_p"]), "antigua_valiente": cruce(VIEJA_NC["APRENDE_v"]), "propia": cruce(PROPIA)}

# ── la habituación de P7-47 y la separación de los dos cambios sobre las mismas pruebas ──
HAB = {}; CURV40 = {}; SIN40 = 0
for var in ("APRENDE_v", "APRENDE_p"):
    for s_ in (1, 2, 3):
        for sl in (10, 11):
            cu, _ = ns["ultimo_cuaderno"](ns["RES"], var, s_, sl)
            HAB[f"{var} s{s_} a{sl}"] = sorted(((cu or {}).get("habituacion_P7_47") or {}).keys())
            sits = ((cu.get("objetos") or {}).get("first_aid") or {}).get("situaciones") or {}
            recs = sorted([dict(r, _sit=k) for k, L_ in sits.items() for r in L_ if not r.get("corte")], key=lambda r: (int(r["dia"]), int(r.get("tick") or 0)))
            SIN40 += sum(1 for r in recs if r.get("intensidad_P7_40") is None)
            r40 = [dict(r, intensidad=r["intensidad_P7_40"]) if r.get("intensidad_P7_40") is not None else r for r in recs]
            CURV40[(var, s_, sl)] = [ns["creencia_dentro"](r40[:k], int(r40[k - 1]["dia"])) for k in range(1, len(r40) + 1)]
PROPIA40 = [(k, round(m, 3), n_) for k, m, n_ in mediana_de([CURV40[c] for c in sorted(CURV40)])]

# ── las dos intensidades sobre las mismas pruebas, pruebas 11 a 17, criatura a criatura ──
COMP = {}
for k in range(11, 18):
    pares = [(c, CURV[c][k - 1], CURV40[c][k - 1]) for c in sorted(CURV) if len(CURV[c]) >= k and CURV[c][k - 1] is not None and CURV40[c][k - 1] is not None]
    dif = [a - b for _, a, b in pares]
    COMP[k] = {"n": len(pares), "mediana_propia": st.median([a for _, a, _ in pares]) if pares else None, "mediana_antigua": st.median([b for _, _, b in pares]) if pares else None,
               "dif_media": st.mean(dif) if dif else None, "dif_ee": (st.stdev(dif) / len(dif) ** 0.5) if len(dif) > 1 else None, "criaturas": [f"{c[0]} s{c[1]} a{c[2]}" for c, _, _ in pares]}
POR_CRIATURA = {}
for c in sorted(CURV):
    d = [CURV[c][k - 1] - CURV40[c][k - 1] for k in range(11, 18) if len(CURV[c]) >= k and CURV[c][k - 1] is not None and CURV40[c][k - 1] is not None]
    if d: POR_CRIATURA[f"{c[0]} s{c[1]} a{c[2]}"] = {"pruebas": len(d), "dif_media": st.mean(d)}
PC = [x["dif_media"] for x in POR_CRIATURA.values()]
RESUMEN_PC = {"n": len(PC), "media": st.mean(PC), "ee": st.stdev(PC) / len(PC) ** 0.5 if len(PC) > 1 else None}
# la habituación en todos los cuadernos diarios de la cadena (no solo el final)
HAB_DIARIA = {}; N_CUAD = 0
import glob as _g
for fcu in sorted(_g.glob(os.path.join(P7, "P7_47_res", "cuaderno_*.json"))):
    N_CUAD += 1
    for o in ((json.load(open(fcu)).get("habituacion_P7_47")) or {}): HAB_DIARIA[o] = HAB_DIARIA.get(o, 0) + 1


# ── dibujo ──
def guarda(fig, nombre):
    out = {}
    fig.savefig(os.path.join(AQUI, nombre + ".png"), dpi=300, metadata={"Software": None})
    fig.savefig(os.path.join(AQUI, nombre + ".pdf"), metadata={"CreationDate": None, "ModDate": None, "Producer": None, "Creator": None})
    plt.close(fig)
    for ext in ("png", "pdf"): out[ext] = hashlib.sha256(open(os.path.join(AQUI, f"{nombre}.{ext}"), "rb").read()).hexdigest()
    return out


def rotulo(ax, x, y, texto, color, dy=0.0, ha="left"):
    ax.annotate(texto, (x, y), xytext=(6 if ha == "left" else -6, dy), textcoords="offset points", color=color, va="center", ha=ha, fontsize=11)


def parte(texto):
    """parte una etiqueta larga del eje y en dos lineas por el espacio mas cercano a la mitad (el texto no cambia)"""
    i = min((j for j, ch in enumerate(texto) if ch == " "), key=lambda j: abs(j - len(texto) / 2)); return texto[:i] + "\n" + texto[i + 1:]


HUELLAS = {}
for L, t in T.items():
    # 5.2
    fig, ax = plt.subplots(figsize=TAM); xs = [1, 2, 3, 4]
    for b, col, ls, mk in (("MIENTE", ACENTO, "-", "o"), ("CONGELADA", GRIS, "--", "s")):
        ys = SALE52[b]; ax.plot(xs, ys, color=col, ls=ls, marker=mk, lw=2, ms=5); rotulo(ax, xs[-1], ys[-1], t[b], col, 9 if b == "MIENTE" else 0)
    ax.set_xticks(xs, [f"{lo}-{hi}" for lo, hi in BLOQUES]); ax.set_xlim(0.7, 5.6); ax.set_ylim(0, 170)
    ax.set_xlabel(t["dias"]); ax.set_ylabel(t["llegadas"]); fig.tight_layout(); HUELLAS[f"fig5_2_{L}"] = guarda(fig, f"fig5_2_{L}")
    # 5.3
    fig, ax = plt.subplots(figsize=TAM); ds = list(range(1, 21))
    for b, col, ls, dy in (("MIENTE", ACENTO, "-", 0), ("HONESTA", NEGRO, "--", 0), ("CONGELADA", GRIS, ":", 0)):
        m = [F53[(b, d)]["media"] for d in ds]; e = [F53[(b, d)]["ee_serie"] for d in ds]
        ax.fill_between(ds, [a - b_ for a, b_ in zip(m, e)], [a + b_ for a, b_ in zip(m, e)], color=col, alpha=0.15, lw=0)
        ax.plot(ds, m, color=col, ls=ls, lw=2); rotulo(ax, ds[-1], m[-1], t[b], col, dy)
    ax.set_xticks([1, 5, 10, 15, 20]); ax.set_xlim(1, 27.5); ax.set_ylim(0, 1)
    ax.set_xlabel(t["dias"]); ax.set_ylabel(parte(t["confianza"]), fontsize=11); fig.tight_layout(); HUELLAS[f"fig5_3_{L}"] = guarda(fig, f"fig5_3_{L}")
    # 3.1: la versión anterior (antigua con las cortadas contadas como prueba) y la revisada (las dos sin cortadas)
    for nombre, VJ, xmax, ticks in ((f"fig3_1_{L}_anterior", VIEJA, 52, [1, 5, 10, 15, 20, 25, 30]), (f"fig3_1_{L}", VIEJA_NC, 27, [1, 5, 10, 15, 20])):
        fig, ax = plt.subplots(figsize=TAM)
        ax.axhline(0.5, color=GRIS, lw=0.8)
        for cur, col, ls, txt, dy in ((VJ["APRENDE_p"], GRIS, "--", f"{t['antigua']}, {t['prudente']}", 6), (VJ["APRENDE_v"], NEGRO, ":", f"{t['antigua']}, {t['valiente']}", -6),
                                      (PROPIA, ACENTO, "-", t["propia"], 0)):
            ks = [k for k, _, _ in cur]; ys = [m / CURA for _, m, _ in cur]; ax.plot(ks, ys, color=col, ls=ls, lw=2); rotulo(ax, ks[-1], ys[-1], txt, col, dy)
        ax.set_xlim(0, xmax); ax.set_ylim(0, 1); ax.set_xticks(ticks)
        ax.set_xlabel(t["pruebas"]); ax.set_ylabel(parte(t["cree"]), fontsize=11); fig.tight_layout(); HUELLAS[nombre] = guarda(fig, nombre)

V = {"fig5_2": {"llegadas": SALE52, "ofertas": {f"{b} d{lo}-{hi}": OFR[(b, lo)] for b in ("MIENTE", "CONGELADA", "HONESTA") for lo, hi in BLOQUES}},
     "fig5_3": {f"{b} d{d}": {k: round(v, 4) if isinstance(v, float) else v for k, v in F53[(b, d)].items()} for b in ("MIENTE", "CONGELADA", "HONESTA") for d in range(1, 21)},
     "fig3_1": {"antigua_prudente": VIEJA["APRENDE_p"], "antigua_valiente": VIEJA["APRENDE_v"], "propia": [(k, round(m, 3), n) for k, m, n in PROPIA],
                "propia_valiente_no_dibujada": [(k, round(m, 3), n) for k, m, n in PROPIA_v], "propia_prudente_no_dibujada": [(k, round(m, 3), n) for k, m, n in PROPIA_p],
                "cruces": c31, "cruces_propia_por_personalidad_no_dibujadas": {"valiente": cruce(PROPIA_v), "prudente": cruce(PROPIA_p)},
                "mediana_de_cruces_P7_47_H3": json.load(open(os.path.join(P7, "P7_47_sello.json")))["H3"]["mediana"]},
     "fig3_1_revision": {"antigua_prudente_sin_cortadas": VIEJA_NC["APRENDE_p"], "antigua_valiente_sin_cortadas": VIEJA_NC["APRENDE_v"], "cruces": c31b, "cortadas": CORTES,
                         "habituacion_final_por_criatura": HAB, "propia_con_intensidad_P7_40_no_dibujada": PROPIA40, "cruce_propia_con_intensidad_P7_40": cruce(PROPIA40),
                         "recuerdos_sin_intensidad_P7_40": SIN40},
     "fig3_1_intensidades_11_17": {"por_prueba": {k: {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in x.items()} for k, x in COMP.items()},
                                   "por_criatura": {k: {"pruebas": x["pruebas"], "dif_media": round(x["dif_media"], 4)} for k, x in POR_CRIATURA.items()},
                                   "resumen_por_criatura": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in RESUMEN_PC.items()},
                                   "habituacion_en_cuadernos_diarios": {"cuadernos": N_CUAD, "objetos": HAB_DIARIA}},
     "huellas_sha256": HUELLAS}
json.dump(V, open(os.path.join(AQUI, "figuras_P7_valores.json"), "w"), ensure_ascii=False, indent=1)

# ── informe ──
n = lambda x, d=3: f"{x:.{d}f}".replace(".", ",")
R = ["# Figuras 3.1, 5.2 y 5.3 del paper siete", "",
     "*Escrito por `hace_figuras_P7.py` desde los datos (ninguna cifra a mano). Sin partidas, sin llamadas: 0 créditos, 0 $. No se toca `motor/model.py`, ni el cuerpo, ni ningún guion de los "
     "experimentos; ninguna réplica se ha vuelto a ejecutar. Rutas relativas a `cantera/paper7/`. Valores también en `figuras/figuras_P7_valores.json`.*", "",
     "Estilo: matplotlib, fondo blanco, sin título, 16 × 9 cm, letra de 11 puntos, PNG a 300 ppp y PDF; acento `#1f6f78`; líneas continua, discontinua y de puntos; nombre junto a cada línea. "
     "Las etiquetas largas del eje y (5.3 y 3.1) van partidas en dos líneas para que quepan; el texto es el pedido, sin cambios.", "",
     "## Figura 5.2 · Llegadas al sitio de la mentira (P7-67, nivel 1, MIENTE y CONGELADA)", "",
     "- Datos: `P7_67_analisis.json` → `criatura_dias_detalle` (lo escribe el guion sellado `analiza_P7_67.py`; campo `llegadas` contado en `analiza_P7_67.py:58`), nivel 1, sumado sobre las "
     "16 series y las dos hermanas en cada tramo de cinco días, igual que la tabla exploratoria del informe (`escribe_informe_P7_67_campo.py:28-33` → `informe_P7_67_campo.md:97-108`).",
     "", "| brazo | días 1-5 | 6-10 | 11-15 | 16-20 |", "|---|---|---|---|---|"]
for b in ("MIENTE", "CONGELADA"): R.append(f"| {b} | " + " | ".join(str(x) for x in SALE52[b]) + " |")
R += ["", f"**Comprobación obligatoria (MIENTE 73, 16, 15, 2; CONGELADA 112, 143, 153, 113): pasa.**", "",
      "**¿Engaña contar llegadas? Cuántas veces se ofreció ir** (criatura-días con oferta: `oportunidad`, `analiza_P7_67.py:64`; un día sin oferta no puede tener llegada):", "",
      "| brazo · días | criatura-días | con oferta | aceptaciones | llegadas | llegadas por oferta | días sin ninguna oferta |", "|---|---|---|---|---|---|---|"]
for b in ("MIENTE", "CONGELADA", "HONESTA"):
    for lo, hi in BLOQUES:
        o = OFR[(b, lo)]; R.append(f"| {b} d{lo}-{hi} | {o['criatura_dias']} | {o['con_oferta']} | {o['aceptaciones']} | {o['llegadas']} | {n(o['llegadas'] / o['con_oferta'], 3) if o['con_oferta'] else '—'} | {', '.join(str(x) for x in o['dias_sin_oferta']) or '—'} |")
R += ["", "Las ofertas son casi las mismas en los dos brazos y en todos los tramos; la única falta grande es el tramo 16-20, el mismo en MIENTE y CONGELADA (el día 19, sin oferta en ninguna "
      "criatura de esos dos brazos, que comparten destino: `informe_P7_67_campo.md`, sección 8.1; HONESTA, con otro destino, sí la tuvo). Contar llegadas no engaña por el lado de las ofertas: la caída de MIENTE no viene de que se le ofreciera menos. "
      "HONESTA va en la tabla solo como referencia (no se dibuja).", "",
      "## Figura 5.3 · La confianza día a día (P7-67, nivel 1)", "",
      "- Datos: el mismo `criatura_dias_detalle`, campo `conf_arranque.recursos` (la confianza leída del cuaderno al arrancar cada día, registro `P7_54_arranque`: `analiza_P7_67.py:61`).",
      "- **La media es por criatura**: la media simple de las 32 criaturas de cada día (16 series × 2 hermanas), como en `analiza_P7_67.py:170-174` → `confianza_dia_a_dia` → "
      "`informe_P7_67_campo.md:67-88`. Cada día tiene las 32 en los tres brazos, así que coincide con la media de las 16 medias por serie.",
      "- Banda: ± 1 error típico con la serie como unidad (media de las dos hermanas por serie; sd de las 16 / √16). No sale de ningún informe: es nueva para la figura.", "",
      "| día | MIENTE | ee | CONGELADA | ee | HONESTA | ee |", "|---|---|---|---|---|---|---|"]
for d in range(1, 21): R.append(f"| {d} | " + " | ".join(f"{n(F53[(b, d)]['media'])} | {n(F53[(b, d)]['ee_serie'])}" for b in ("MIENTE", "CONGELADA", "HONESTA")) + " |")
R += ["", f"**Comprobación obligatoria (día 20: MIENTE 0,157, HONESTA 0,838; CONGELADA plana en 0,5): pasa** (MIENTE {n(c53['MIENTE'])}, HONESTA {n(c53['HONESTA'])}, CONGELADA 0,500 los 20 días; "
      "los 60 valores coinciden con `confianza_dia_a_dia` de `P7_67_analisis.json`).", "",
      "## Figura 3.1 · Qué deprisa aprende lo que cura el botiquín", "",
      f"- Eje y: la creencia del cuerpo sobre lo que cura el botiquín dividida por lo que cura de verdad, {n(CURA, 0)} (`informe_P7_62.md:17`); la línea horizontal es la mitad (25, el umbral de "
      "`analiza_P7_46.py:154` y de H3 en `analiza_P7_47.py:29`). Cada línea es la **mediana entre criaturas** de la creencia tras la k-ésima prueba, mientras quedan al menos 3 criaturas.",
      "- **Fórmula antigua**: `P7_46_resumen.json` → `R1.curva_mediana` (`analiza_P7_46.py:146-153,171`), una línea por cadena: APRENDE prudente y APRENDE valiente, 6 criaturas cada una. "
      "Ojo: P7-46 no es una réplica sino la lectura de los diarios del campo P7-45 (`banco_P7_46.py:1`); y en su cuenta una prueba cortada es una prueba que deja la creencia como estaba "
      "(`analiza_P7_46.py:6,86-87`).",
      "- **Escala propia**: la cadena en réplica de P7-47 (12 criaturas: 6 valientes y 6 prudentes, `informe_P7_47.md:7`). La curva mediana no estaba guardada entera: `analiza_P7_47.py:29-36` "
      "guarda la curva de cada criatura solo hasta que cruza 25. Se ha recalculado desde los cuadernos guardados (`P7_47_res/`), con la misma función `creencia_dentro` (`analiza_P7_47.py:13`) "
      "y sin cortar en el cruce; no se ha vuelto a ejecutar la réplica. Puerta: lo recalculado coincide, criatura a criatura, con las curvas guardadas en `P7_47_sello.json`. Aquí las pruebas "
      "cortadas no cuentan como prueba (`analiza_P7_47.py:5`): **el eje x no cuenta lo mismo en las dos fórmulas** (cortadas incluidas en la antigua, excluidas en la propia).",
      "- La escala propia se dibuja con las 12 criaturas juntas, porque la comprobación da un solo número; por personalidad cruzaría en la prueba "
      f"{cruce(PROPIA_v)} (valiente) y {cruce(PROPIA_p)} (prudente) (no dibujadas; valores en el JSON). P7-47 cambió también la habituación, no solo la escala (`informe_P7_47.md:1`).", "",
      "| prueba | antigua, prudente (fracción · n) | antigua, valiente | escala propia |", "|---|---|---|---|"]
P = {k: (m, nn) for k, m, nn in PROPIA}; VP = {k: (m, nn) for k, m, nn in VIEJA["APRENDE_p"]}; VV = {k: (m, nn) for k, m, nn in VIEJA["APRENDE_v"]}
for k in range(1, max(max(VP), max(VV), max(P)) + 1):
    f = lambda D: (f"{n(D[k][0] / CURA)} · {D[k][1]}" if k in D else "—")
    R.append(f"| {k} | {f(VP)} | {f(VV)} | {f(P)} |")
R += ["", f"**Comprobación obligatoria (antigua: cruza la mitad hacia las 17 pruebas en la prudente y las 30 en la valiente; escala propia, hacia las 8 o 9): pasa.** Primera prueba con la "
      f"mediana en la mitad o por encima: antigua prudente {c31['antigua_prudente']}, antigua valiente {c31['antigua_valiente']} (son los k* de `informe_P7_46.md:119-120`); escala propia "
      f"{c31['propia']}. El 8,5 de `informe_P7_47.md:17` es otra cuenta, la mediana de las primeras pruebas en cruzar de cada criatura (las que no cruzan, como infinito): "
      f"{n(V['fig3_1']['mediana_de_cruces_P7_47_H3'], 1)}.", "",
      ]
RV = V["fig3_1_revision"]; CP = CORTES["APRENDE_p"]; CV = CORTES["APRENDE_v"]
R += ["## Figura 3.1, revisión: las dos líneas con el eje x contado igual", "",
      "La figura de la sección anterior se guarda ahora como `fig3_1_es_anterior` y `fig3_1_en_anterior` (mismos bytes que la entregada antes: sus huellas, abajo). `fig3_1_es` y `fig3_1_en` son la versión revisada.", "",
      "### 1. La fórmula antigua contada solo con las pruebas no cortadas", "",
      "- Mismos datos (`P7_46_datos.json`, las huellas del botiquín de cada criatura en orden, como `analiza_P7_46.py:93`), pero dejando fuera las pruebas con `corte`; la creencia de cada prueba "
      "es la que el cuerpo apuntó tras ella (`creencia_despues`), y la curva es la misma mediana entre criaturas con al menos 3. Puerta: con las cortadas dentro, el mismo cálculo reproduce "
      "exactamente la curva guardada en `P7_46_resumen.json`.",
      f"- **Contadas así, la mediana cruza la mitad en la prueba {c31b['antigua_prudente']} en la prudente y en la {c31b['antigua_valiente']} en la valiente** (antes, con las cortadas contadas, 17 y 30). "
      f"La escala propia cruza en la {c31b['propia']}.",
      f"- Pruebas cortadas: prudente {CP['cortadas']} de {CP['pruebas']}; valiente {CV['cortadas']} de {CV['pruebas']} (las seis criaturas de cada una). Por criatura: "
      + "; ".join(f"prudente {k} {x['cortadas']} de {x['pruebas']}" for k, x in CP["criaturas"].items()) + "; " + "; ".join(f"valiente {k} {x['cortadas']} de {x['pruebas']}" for k, x in CV["criaturas"].items()) + ".",
      f"- Salvedad: en el campo, la creencia apuntada tras una prueba cortada no siempre es la de antes ({CP['cortadas_que_mueven_la_creencia']} de {CP['cortadas_con_creencia']} cortadas con creencia apuntada "
      f"en la prudente y {CV['cortadas_que_mueven_la_creencia']} de {CV['cortadas_con_creencia']} en la valiente la mueven); el código no se ha mirado para saber por qué (el olvido entre días es una "
      "posibilidad, no comprobada). Ese movimiento queda dentro de la creencia de la siguiente prueba no cortada. En P7-47, en cambio, las cortadas no entran en la creencia (`analiza_P7_47.py:5,31`). "
      "Las medianas de las dos curvas antiguas se apoyan en pocas criaturas a partir de la prueba 9 (columna n).", "",
      "| prueba | antigua, prudente, sin cortadas (fracción · n) | antigua, valiente, sin cortadas | escala propia |", "|---|---|---|---|"]
NP = {k: (m, nn) for k, m, nn in VIEJA_NC["APRENDE_p"]}; NV = {k: (m, nn) for k, m, nn in VIEJA_NC["APRENDE_v"]}
for k in range(1, max(max(NP), max(NV), max(P)) + 1):
    f = lambda D: (f"{n(D[k][0] / CURA)} · {D[k][1]}" if k in D else "—")
    R.append(f"| {k} | {f(NP)} | {f(NV)} | {f(P)} |")
R += ["", "Consecuencia para la frase del paper («entre diecisiete y treinta pruebas; con su escala, unas ocho o nueve»): con el eje contado igual, la diferencia entre las dos fórmulas casi "
      f"desaparece ({c31b['antigua_prudente']} y {c31b['antigua_valiente']} frente a {c31b['propia']}). El 17 y el 30 cuentan como prueba las cortadas, que en la fórmula antigua son más de la mitad de las pruebas.", "",
      "### 2. ¿Puede la habituación cambiar lo que cree que cura el botiquín?", "",
      "- **Directamente, no.** La habituación solo multiplica la curiosidad: envuelve `filo_P7_40.curiosidad` y la multiplica por el factor h del objeto (`habitua_P7_47.py:2-4,33-36`); "
      "su estado es aparte (`habituacion_P7_47`, `habitua_P7_47.py:43,48,75`). La creencia sobre la cura es la media de los efectos vividos pesada por la intensidad y el olvido "
      "(`analiza_P7_47.py:13-27`, peso en `:19`), y lo único que P7-47 cambia en el recuerdo es la intensidad (`habitua_P7_47.py:72`). Quien lee la curiosidad decide qué probar "
      "(«la ignorancia nueva, E1 y los momentos», `habitua_P7_47.py:4`; también `banco_P7_47.py:51`).",
      "- **Indirectamente, sí puede**: al cambiar qué se prueba y cuándo, cambia qué pruebas del botiquín vive la criatura, y con ellas su creencia.",
      "- **En los cuadernos de P7-47 el botiquín no se habituó nunca**: el estado final de habituación de las 12 criaturas solo tiene la red y el camuflaje ("
      + "; ".join(f"{k}: {', '.join(v) or 'nada'}" for k, v in RV["habituacion_final_por_criatura"].items()) + "). Una habituación no se borra del estado (`habitua_P7_47.py:75`), así que "
      "el botiquín no tuvo nunca la curiosidad rebajada; la habituación solo pudo influir a través de las otras cosas.",
      "- **¿Se pueden separar los dos cambios sin partidas nuevas?** En parte. Cada recuerdo del botiquín de P7-47 guarda también la intensidad antigua (`intensidad_P7_40`, `habitua_P7_47.py:72`), "
      f"así que sobre **las mismas pruebas** se puede recalcular la creencia con la fórmula antigua: la mediana cruza la mitad en la prueba {RV['cruce_propia_con_intensidad_P7_40']}, "
      f"frente a {c31b['propia']} con la escala propia (valores en el JSON, no dibujados; {RV['recuerdos_sin_intensidad_P7_40']} recuerdo sin intensidad antigua se deja con la suya). "
      "Eso mide el efecto directo de la escala con las pruebas fijas. Lo que no se puede separar sin réplicas nuevas es el efecto de la habituación (y de la escala) sobre qué pruebas se viven: "
      "para eso haría falta repetir la cadena con un cambio y no el otro. No se ha intentado.", "",
      ]
R += ["## Figura 3.1: tres preguntas más (23-oct-2026)", "",
      "### 1. Qué es `intensidad_P7_40`", "",
      "- **Es la fórmula antigua, aplicada a los mismos recuerdos de P7-47.** Al cerrar cada prueba sin corte, la pieza de P7-38 en su variante A sin contrafactual pone en el recuerdo "
      "`intensidad = 1 + escalar(importancia)` (`contrafactual_P7_38.py:131`), con `escalar = min(1, (|imp cuerpo| + |imp recursos| + |imp vínculo|) / E)` (`contrafactual_P7_38.py:19`) y "
      "E = 1,5 (`cuaderno_P7.py:24`): tope 2. Después, la pieza de P7-47 copia ese valor en `intensidad_P7_40` y escribe encima la intensidad en la escala propia "
      "(`habitua_P7_47.py:72`; descrito en `:5-7`). Es la fórmula «de P7-40» cuyos cuartiles sobre esos recuerdos son 1,04 · 1,11 · 1,25 (`informe_P7_47.md:25-26`).",
      "- Es la misma fórmula que llevaba el campo P7-45, de donde sale la curva antigua: las dos composiciones ponen P7-38 en variante A sin contrafactual y P7-39 encendido "
      "(`campo_P7_41.py:18`; `campo_P7_47.py:21`); P7-47 solo añade la habituación y la escala propia (`campo_P7_47.py:1-2,33`).",
      "- **Qué separa la comparación entre `propia_con_intensidad_P7_40` y la escala propia.** Son las mismas pruebas, las mismas criaturas, el mismo olvido y la misma importancia de cada "
      "recuerdo; solo cambia el peso. Las dos dejan fuera las cortadas (`analiza_P7_47.py:31`), así que **contar las cortadas no interviene**. La habituación y la escala ya actuaron sobre "
      "qué pruebas se vivieron, y eso es igual en las dos curvas: **la comparación aísla el efecto directo de la escala sobre la creencia, con las pruebas fijas**. No separa el efecto de la "
      "escala ni el de la habituación sobre la conducta (qué pruebas llegan a vivirse); para eso haría falta repetir la cadena con un cambio y no el otro.", "",
      "### 2. Pruebas 11 a 17: las dos curvas y la diferencia criatura a criatura", "",
      "Creencia del cuerpo sobre lo que cura el botiquín (en vida; la fracción es esto dividido por 50). Diferencia = escala propia − fórmula antigua, en la misma criatura y la misma prueba; "
      "ee = sd de las diferencias / √n.", "",
      "| prueba | n criaturas | mediana, escala propia | mediana, fórmula antigua | diferencia media | ee | ¿mayor que su ee? |", "|---|---|---|---|---|---|---|"]
for k, x in COMP.items():
    R.append(f"| {k} | {x['n']} | {n(x['mediana_propia'], 2)} | {n(x['mediana_antigua'], 2)} | {n(x['dif_media'], 2)} | {n(x['dif_ee'], 2) if x['dif_ee'] is not None else '—'} | "
             f"{('sí' if abs(x['dif_media']) > x['dif_ee'] else 'no') if x['dif_ee'] else '—'} |")
R += ["", "Por criatura (media de sus diferencias en las pruebas 11-17 que tiene): " + "; ".join(f"{k} {n(x['dif_media'], 2)} ({x['pruebas']} pruebas)" for k, x in POR_CRIATURA.items()) + ".",
      f"Entre criaturas: diferencia media {n(RESUMEN_PC['media'], 2)} ± {n(RESUMEN_PC['ee'], 2)} (n = {RESUMEN_PC['n']}): "
      f"{'mayor' if abs(RESUMEN_PC['media']) > RESUMEN_PC['ee'] else 'no mayor'} que su error típico ({n(abs(RESUMEN_PC['media']) / RESUMEN_PC['ee'], 1)} veces). "
      "Son pocas criaturas y las mismas en todas las pruebas, que no son independientes entre sí: es una lectura descriptiva, no una prueba sellada.", "",
      "### 3. La habituación", "",
      "- La respuesta estaba en la sección «Figura 3.1, revisión», punto 2; aquí, completa.",
      "- **Dónde actúa:** envuelve `filo_P7_40.curiosidad` y la multiplica por el factor h del objeto (`habitua_P7_47.py:33-36`); el factor baja a la mitad tras una prueba sin efecto y no cortada "
      "(`habitua_P7_47.py:63,74-75`) y vuelve hacia 1 con el olvido (`habitua_P7_47.py:19-22`). Su estado viaja aparte en el cuaderno, `habituacion_P7_47` (`:43,48`). Fuera de la pieza solo lo "
      "leen los guiones de análisis.",
      "- **Lo que cree del botiquín no lo toca directamente:** la creencia es la media de los efectos vividos, pesada por intensidad y olvido (`analiza_P7_47.py:13-27`), y la habituación no "
      "escribe ni el efecto ni la intensidad de ningún recuerdo (en `habitua_P7_47.py:61-77` la intensidad la pone la escala, `:72`; la habituación solo toca `E[\"H\"]`, `:75`). Indirectamente sí "
      "podría: la curiosidad decide qué se prueba (`habitua_P7_47.py:4`), y con ello qué pruebas del botiquín se viven.",
      f"- **El botiquín no se habituó nunca.** No solo en el cuaderno final: en los {N_CUAD} cuadernos diarios de la cadena (`P7_47_res/`) la habituación solo nombra "
      + ", ".join(f"{o} ({v} cuadernos)" for o, v in sorted(HAB_DIARIA.items())) + ", y nunca el botiquín. Como una entrada no se borra una vez puesta (`habitua_P7_47.py:75`) y el estado se "
      "lee y se escribe cada día (`:43,48`), la curiosidad por el botiquín no se rebajó nunca.",
      "- **¿Basta eso para decir que no toca lo que cree del botiquín?** Basta para decir que no lo tocó por su vía directa ni rebajó la curiosidad por el botiquín. No basta para descartar el "
      "efecto indirecto: al habituarse a la red y al camuflaje, la criatura pudo dedicar a otras cosas el tiempo que antes les daba, y eso puede cambiar cuándo y en qué situación prueba el "
      "botiquín. Ese efecto queda dentro de las pruebas, igual en las dos curvas de la comparación del punto 1, y no se puede medir sin réplicas nuevas.", "",
      "## Huellas sha256", "", "| archivo | sha256 |", "|---|---|"]
for k, h in HUELLAS.items():
    for ext in ("png", "pdf"): R.append(f"| `{k}.{ext}` | `{h[ext]}` |")
R += ["", "Repetible: volver a ejecutar `python3 hace_figuras_P7.py` da los mismos bytes (comprobado dos veces; metadatos de fecha anulados).", ""]
open(os.path.join(AQUI, "informe_P7_figuras.md"), "w").write("\n".join(R))
print("comprobaciones: pasan las tres;", {k: h["png"][:12] for k, h in HUELLAS.items()})
