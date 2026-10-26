"""[P7-67, apertura del sello] escribe informe_P7_67_campo.md desde P7_67_analisis.json (salida del guion sellado analiza_P7_67.py, md5 7bef2e46…, corrido tal cual), P7_67F_estado.json
y P7_67F_diseno.json, y los dos GIF de los datos crudos (matplotlib). Ninguna cifra a mano. (informe_P7_67.md ya es el del primer banco: este es el del campo.)
  - Descriptivo por bloque, cotas del efecto y GIF: lo que no está en el sello va marcado «exploratorio, no sellado» o «no sellado: cota del efecto».
  - GIF: candidatos = (a) llegadas de MIENTE, nivel 1, días 11-20; (b) llegadas de HONESTA, nivel 1, con acierto. Uno de cada lista al azar con random.Random(SEMILLA_GIF).
  python3 escribe_informe_P7_67_campo.py -> informe_P7_67_campo.md, P7_67_campo_extra.json, P7_67F_gif_miente.gif, P7_67F_gif_honesta.gif (y copia en ../figuras)"""
import glob, hashlib, json, math, os, random, shutil, statistics as st, zipfile
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs")
J = lambda f: json.load(open(os.path.join(AQUI, f)))
R = J("P7_67_analisis.json"); E = J("P7_67F_estado.json"); D = J("P7_67F_diseno.json")
SEMILLA_GIF = 20261020
md5 = lambda f: hashlib.md5(open(f, "rb").read()).hexdigest()
f = lambda x, n=3: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
pc = lambda x: "—" if x is None else f"{100 * x:.1f} %".replace(".", ",")
n_ = lambda x: f"{int(x):,}".replace(",", ".")
CD = R["criatura_dias_detalle"]; P = [p for p in E["peticiones"] if p["estado"] == "completed"]
BLOQUES = ((1, 5), (6, 10), (11, 15), (16, 20)); GR = ("MIENTE", "CONGELADA", "HONESTA")


def carpeta(n, s, d, b, sem): return os.path.join(RUNS, f"P767F_n{n}_s{s}_d{d}_{b}_{sem}")
def lineas(car, sl):
    a = glob.glob(os.path.join(car, f"*policy_agent_{sl}.art.log"))
    if a: yield from open(a[0], errors="replace"); return
    with zipfile.ZipFile(glob.glob(os.path.join(car, f"*policy_agent_{sl}.zip"))[0]) as Z, Z.open(Z.namelist()[0]) as fh:
        for b in fh: yield b.decode(errors="replace")


# ── descriptivo por bloque (exploratorio, no sellado) ──
DESC = {}
for b in GR:
    for lo, hi in BLOQUES:
        cs = [c for c in CD if c["nivel"] == "1" and c["brazo"] == b and lo <= c["dia"] <= hi]
        DESC[f"{b} d{lo}-{hi}"] = {"criatura_dias": len(cs), "ocasiones": sum(c["oportunidad"] for c in cs), "aceptaciones": sum(c["aceptadas"] for c in cs), "llegadas": sum(c["llegadas"] for c in cs),
                                   "aciertos": sum(c["aciertos"] for c in cs), "fallos": sum(c["llegadas"] - c["aciertos"] for c in cs), "interrumpidas": sum(c["interrumpidas"] for c in cs),
                                   "no_llego": sum(c["no_llego"] for c in cs)}
# ── cotas del efecto (no sellado) ──
def cota(est, ee): return None if est is None or ee is None else (est - 2 * ee, est + 2 * ee)
CUENTAS = (("principal", "cuenta principal"), ("robustez_sin_marcadas", "robustez (a): sin las partidas marcadas"), ("robustez_por_criatura", "robustez (b): la criatura como unidad"))
def fila(k):
    r = R[k]; p1, p2, p3, p3b = r["P1"], r["P2"], r["P3"], r["P3b"]
    return {"P1": (p1.get("media"), p1.get("ee"), p1.get("n"), p1["veredicto"]), "P2": (p2.get("diferencia"), p2.get("ee"), f"{p2['MIENTE'].get('n')} + {p2['CONGELADA'].get('n')}", p2["veredicto"]),
            "P3": (p3.get("pendiente"), p3.get("ee"), p3.get("filas"), p3["veredicto"]), "P3b": (p3b.get("pendiente_ln_rivales"), p3b.get("ee"), p3b.get("filas"), p3b["veredicto"])}
F = {k: fila(k) for k, _ in CUENTAS}
COTAS = {k: {pr: cota(v[0], v[1]) for pr, v in F[k].items() if v[3] != "PASA"} for k, _ in CUENTAS}
CAMBIA = {pr: len({F[k][pr][3] for k, _ in CUENTAS}) > 1 for pr in ("P1", "P2", "P3", "P3b")}

# ── los dos GIF (datos crudos, matplotlib) ──
def candidatos(brazo, cond):
    out = []
    for c in CD:
        if c["nivel"] == "1" and c["brazo"] == brazo and cond(c): out.append((c["serie"], c["dia"], c["slot"]))
    return sorted(out)
cand_m = candidatos("MIENTE", lambda c: c["dia"] >= 11 and c["llegadas"] > 0)
cand_h = candidatos("HONESTA", lambda c: c["aciertos"] > 0)
rnd = random.Random(SEMILLA_GIF); el_m = rnd.choice(cand_m) if cand_m else None; el_h = rnd.choice(cand_h) if cand_h else None
SEM = {(p["nivel"], p["serie"], p["dia"], p["brazo"]): p["semilla"] for p in P}


def gif(brazo, el, out, acierto_req=None):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; from matplotlib.animation import FuncAnimation, PillowWriter
    s, d, sl = el; car = carpeta("1", s, d, brazo, SEM[("1", s, d, brazo)]); muro = set(); T = {}; acc = None; lle = None
    for l in lineas(car, sl):
        if l.startswith('{"k":"static_map"') and not muro:
            m = json.loads(l); duros = {c for c, v in m["legend"].items() if v in ("wall", "rock", "fortress_wall")}
            muro = {(x, y): ch for y, fila_ in enumerate(m["filas"]) for x, ch in enumerate(fila_) if ch in duros}
        elif l.startswith('{"k":"P7_66_aceptada"') and acc is None: acc = json.loads(l)
        elif l.startswith('{"k":"P7_66_llegada"') and lle is None and (acierto_req is None or json.loads(l)["acierto_recursos"] == acierto_req): lle = json.loads(l)
        elif l.startswith('{"k":"tick"') and '"phase":"live"' in l:
            r = json.loads(l); T[r["tick"]] = r
    t0, t1 = lle["t_aceptada"], lle["tick"]; todos = [t for t in sorted(T) if t0 <= t <= t1 + 1]; ts = todos[::2] + ([todos[-1]] if todos and todos[-1] not in todos[::2] else []); dest = tuple(lle["destino"])   # el ultimo tic siempre: la posicion de la llegada aparece en el diario un tic despues de su registro
    pts = [tuple(T[t]["pos"]) for t in ts] + [dest]; cx = (min(p[0] for p in pts) + max(p[0] for p in pts)) / 2; cy = (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2
    Rr = max(9, max(max(p[0] for p in pts) - min(p[0] for p in pts), max(p[1] for p in pts) - min(p[1] for p in pts)) / 2 + 4)
    activos = set(D["activos"]["1"]); fig, ax = plt.subplots(figsize=(5.6, 5.8))
    def frame(i):
        t = ts[i]; w = T[t]; ax.clear(); ax.set_xlim(cx - Rr, cx + Rr); ax.set_ylim(cy + Rr, cy - Rr); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        mx = [p for p in muro if abs(p[0] - cx) <= Rr + 1 and abs(p[1] - cy) <= Rr + 1]
        if mx: ax.scatter([p[0] for p in mx], [p[1] for p in mx], s=30, marker="s", c="#d9d9d6")
        ax.scatter([dest[0]], [dest[1]], s=260, marker="*", c="#f39c12", label="destino")
        kits = [tuple(it["pos"]) for it in (w.get("ve_items") or []) if it.get("id") == "first_aid" and it.get("pos")]
        if kits: ax.scatter([p[0] for p in kits], [p[1] for p in kits], s=120, marker="P", c="#2e8b57", label="botiquín")
        ag = [(a.get("slot"), tuple(a["pos"])) for a in (w.get("ve_agentes") or []) if a.get("pos")]
        pa = [p for s_, p in ag if s_ not in activos and s_ not in (sl, sl ^ 1)]; ri = [p for s_, p in ag if s_ in activos]; he = [p for s_, p in ag if s_ == sl ^ 1]
        if pa: ax.scatter([p[0] for p in pa], [p[1] for p in pa], s=80, c="#9e9e9e", label="estatua")
        if ri: ax.scatter([p[0] for p in ri], [p[1] for p in ri], s=90, c="#c0392b", label="rival activo")
        if he: ax.scatter([p[0] for p in he], [p[1] for p in he], s=90, c="#5dade2", label="hermana")
        tr = [tuple(T[tt]["pos"]) for tt in ts[:i + 1]]; ax.plot([p[0] for p in tr], [p[1] for p in tr], c="#888", lw=1)
        ax.scatter([w["pos"][0]], [w["pos"][1]], s=140, c="#141414", label=f"ella (asiento {sl})")
        ax.set_title(f"{brazo} · nivel 1 · serie {s} · día {d} · tic {t} (+{t - t0})\nelige: {(w.get('RADIOGRAFIA') or {}).get('elegido')}", fontsize=8); ax.legend(loc="lower left", fontsize=7)
    FuncAnimation(fig, frame, frames=len(ts)).save(out, writer=PillowWriter(fps=6)); plt.close(fig)
    return {"gif": os.path.basename(out), "serie": s, "dia": d, "asiento": sl, "destino": list(dest), "tic_aceptada": t0, "tic_llegada": t1, "tics": t1 - t0, "acierto": lle["acierto_recursos"],
            "botiquines_vistos": lle.get("botiquines_vistos"), "fotogramas": len(ts)}
G = []
FIG = os.path.join(os.path.dirname(AQUI), "figuras"); os.makedirs(FIG, exist_ok=True)
for brazo, el, nombre, req in (("MIENTE", el_m, "P7_67F_gif_miente.gif", None), ("HONESTA", el_h, "P7_67F_gif_honesta.gif", 1)):
    if el: g = gif(brazo, el, os.path.join(AQUI, nombre), req); g["brazo"] = brazo; G.append(g); shutil.copy(os.path.join(AQUI, nombre), os.path.join(FIG, nombre))
EXTRA = {"descriptivo_por_bloque": DESC, "cotas": {k: {pr: (list(v) if v else None) for pr, v in c.items()} for k, c in COTAS.items()}, "cambia_entre_cuentas": CAMBIA,
         "gif": {"semilla": SEMILLA_GIF, "candidatos_MIENTE": len(cand_m), "candidatos_HONESTA": len(cand_h), "elegidos": G}}
json.dump(EXTRA, open(os.path.join(AQUI, "P7_67_campo_extra.json"), "w"), ensure_ascii=False, indent=1)

# ── el informe ──
cnt = {}
for p in P: cnt[(p["nivel"], p["brazo"])] = cnt.get((p["nivel"], p["brazo"]), 0) + 1
marc = sorted([p for p in P if any(not g.get("pasa", True) for g in (p.get("latencia") or {}).values())], key=lambda p: (int(p["nivel"]), p["brazo"], p["serie"], p["dia"]))
apart = E.get("apartadas_plataforma", []); creditos = len(P) + len(apart)
L = ["# P7-67 · El campo: la mentira seguible, con el mando de la amenaza · apertura del sello", "",
     f"*Guion sellado `analiza_P7_67.py` (md5 `{md5(os.path.join(AQUI, 'analiza_P7_67.py'))}`, el de la enmienda 1 de `SELLO_P7_67.md`), corrido tal cual sobre el campo terminado. `motor/model.py` = "
     f"`{md5(os.path.join(RAIZ, 'motor', 'model.py'))}`. Este informe lo escribe `escribe_informe_P7_67_campo.py`; ninguna cifra a mano. Lo que no estaba en el sello va marcado «exploratorio, no sellado» o "
     "«no sellado: cota del efecto».*", "", "*Nota de lectura: el registro de una llegada lleva la etiqueta del tic t, y la posición que la justifica aparece en el diario en el tic t+1 (el desfase de un tic ya conocido). Los GIF terminan en ese tic t+1.*", "",
     "## 1. Comprobaciones previas (hechas antes de ver ningún resultado)", "",
     "- `motor/model.py` y `analiza_P7_67.py` con el md5 de arriba; `SELLO_P7_67.md` sin cambios desde su último commit (enmienda 4).",
     "- Partidas por brazo y nivel: " + "; ".join(f"nivel {n} {b} {cnt.get((n, b), 0)}" for n in ("1", "2", "3", "14") for b in GR if cnt.get((n, b))) + f". Total {len(P)} (diseño: {D['partidas']}).",
     f"- Vidas: {R['criatura_dias']} criatura-días leídos, cada una con su diario (el `.art.log` o el `.zip`) y su cuaderno de fin. Llegadas sin oportunidad (anomalías): {R['anomalias_llegada_sin_oportunidad']}.",
     f"- Partidas apartadas por fallo de la plataforma (no cuentan; repetidas con la misma imagen y semilla): {len(apart)}.", "",
     f"## 2. Partidas marcadas (regla sellada: marcada si cualquiera de las dos hermanas falla la guarda; en la robustez sale entera): {len(marc)}", ""]
for p in marc: L.append(f"- nivel {p['nivel']} · {p['brazo']} · serie {p['serie']} · día {p['dia']} · asiento(s) {', '.join(s for s, g in p['latencia'].items() if not g.get('pasa'))} · {'; '.join(m for s, g in p['latencia'].items() if not g.get('pasa') for m in g.get('motivo', []))}")
L += ["", "## 3. Las predicciones selladas", "", "| predicción | cuenta | estimación | error estándar | unidades | veredicto |", "|---|---|---|---|---|---|"]
for pr in ("P1", "P2", "P3", "P3b"):
    for k, nom in CUENTAS:
        est, ee, nu, v = F[k][pr]; L.append(f"| {pr} | {nom} | {f(est, 4)} | {f(ee, 4)} | {nu} | **{v}** |")
p1 = R["principal"]["P1"]; p2 = R["principal"]["P2"]
L += ["", f"- P1 (MIENTE, media de B − A por pareja): parejas que cumplen el mínimo de 3 días con oportunidad en A y en B: **{p1['dentro']}**; fuera: {p1['fuera']}"
      + (f" ({'; '.join(x['unidad'] + ': ' + str(x['dias_con_oportunidad_A']) + '/' + str(x['dias_con_oportunidad_B']) for x in p1['detalle_fuera'])})" if p1["detalle_fuera"] else "") + ".",
      f"- P2: MIENTE {f(p2['MIENTE'].get('media'), 4)} (n {p2['MIENTE'].get('n')}) − CONGELADA {f(p2['CONGELADA'].get('media'), 4)} (n {p2['CONGELADA'].get('n')}); parejas de CONGELADA fuera: {p2['fuera_CONGELADA']}.",
      f"- P3 (fracción de llegadas d1-5 sobre ln(rivales), con el brazo como indicadora): {R['principal']['P3']['filas']} parejas; fuera por no tener oportunidad: {R['principal']['P3']['fuera_sin_oportunidad']}. Por nivel (media ± ee): "
      + "; ".join(f"{k} rivales {f(v['media'], 3)} ± {f(v['ee'], 3)} (n {v['n']})" for k, v in R["principal"]["P3"]["por_nivel"].items()) + ".",
      f"- P3b (llegadas medias por día d1-5, 0 sin oportunidad): {R['principal']['P3b']['filas']} parejas. Por nivel: " + "; ".join(f"{k} rivales {f(v['media'], 3)} ± {f(v['ee'], 3)} (n {v['n']})" for k, v in R["principal"]["P3b"]["por_nivel"].items()) + ".",
      "- Fracción de días con oportunidad, días 1-5 (descriptivo sellado): " + "; ".join(f"{k} {pc(v['fraccion'])} ({v['con_oportunidad']} de {v['criatura_dias']})" for k, v in R["fraccion_dias_con_oportunidad_dias_P3"].items() if "_" not in k) + ".", "",
      "## 4. Robustez: ¿cambia algún veredicto entre cuentas?", ""]
for pr, c in CAMBIA.items(): L.append(f"- {pr}: {'**SÍ cambia**: ' + ', '.join(F[k][pr][3] + ' (' + nom + ')' for k, nom in CUENTAS) if c else 'no cambia (' + F['principal'][pr][3] + ' en las tres cuentas)'}.")
L += ["", "## 5. Descriptivo", "", "**Sellado:** HONESTA, la confianza día a día, las interrupciones por nivel y las muertes.", "",
      f"- HONESTA (B − A por pareja, como referencia): media {f(R['principal']['descriptivo_HONESTA'].get('media'), 4)} ± {f(R['principal']['descriptivo_HONESTA'].get('ee'), 4)} (n {R['principal']['descriptivo_HONESTA'].get('n')}; fuera {R['principal']['descriptivo_HONESTA'].get('fuera')}).",
      "- Confianza media en recursos al arrancar cada día, nivel 1:", "", "| día | " + " | ".join(GR) + " |", "|---|" + "---|" * len(GR)]
for d in range(1, 21): L.append(f"| {d} | " + " | ".join(f(R["confianza_dia_a_dia"].get(b, {}).get("recursos", {}).get(str(d)), 3) for b in GR) + " |")
L += ["", "- Interrupciones y llegadas por nivel, días 1-5: " + "; ".join(f"{k} rivales: {v['criatura_dias']} criatura-días, {v['oportunidades']} oportunidades, {v['aceptadas']} aceptadas, {v['interrumpidas']} interrumpidas, {v['llegadas']} llegadas" for k, v in R["interrupciones_por_nivel_dias_P3"].items()) + ".",
      "- Muertes (criatura-días eliminados): " + "; ".join(f"{k} {v['muertas']} de {v['criatura_dias']}" for k, v in sorted(R["muertes"].items())) + ".", "",
      "**Exploratorio, no sellado: por bloque de días, nivel 1.**", "", "| grupo · días | criatura-días | ocasiones | aceptaciones | llegadas | aciertos | fallos | interrumpidas (rival activo a ≤ 3) | no llegó |", "|---|---|---|---|---|---|---|---|---|"]
for k, v in DESC.items(): L.append(f"| {k} | {v['criatura_dias']} | {v['ocasiones']} | {v['aceptaciones']} | {v['llegadas']} | {v['aciertos']} | {v['fallos']} | {v['interrumpidas']} | {v['no_llego']} |")
L += ["", "## 6. No sellado: cota del efecto (estimación ± 2 errores estándar) de cada predicción que no pasa", ""]
for k, nom in CUENTAS:
    for pr, c in COTAS[k].items(): L.append(f"- {pr}, {nom}: " + ("no calculable" if c is None else f"[{f(c[0], 4)}, {f(c[1], 4)}]") + ".")
L += ["", f"## 7. GIF (exploratorio, no sellado; datos crudos, matplotlib; elegidos al azar con random.Random({SEMILLA_GIF}))", "",
      f"Candidatos: {len(cand_m)} llegadas de MIENTE en los días 11-20 (nivel 1) y {len(cand_h)} llegadas de HONESTA con acierto (nivel 1).", ""]
for g in G: L.append(f"- `{g['gif']}`: {g['brazo']}, serie {g['serie']}, día {g['dia']}, asiento {g['asiento']}, destino {tuple(g['destino'])}, de la aceptación (tic {g['tic_aceptada']}) a la llegada (tic {g['tic_llegada']}, {g['tics']} tics), acierto {g['acierto']}; {g['fotogramas']} fotogramas. ![{g['gif']}](../figuras/{g['gif']})")
# ── preguntas de Manel del 20-oct (EXPLORATORIO, NO SELLADO): P7_67_explora.json, de explora_P7_67_campo.py ──
if os.path.exists(os.path.join(AQUI, "P7_67_explora.json")):
    X = J("P7_67_explora.json"); q1 = X["pregunta_1"]; r1 = q1["resumen"]; q2 = X["pregunta_2"]["por_dia"]; t0 = X["tic_de_la_primera_oferta_en_todo_el_campo"]
    dias19 = sorted({r["dia"] for r in q1["sin_oportunidad"]}); dest19 = sorted({tuple(r["destino"]) for r in q1["sin_oportunidad"]})
    L += ["", "## 8. Exploratorio, no sellado: dos preguntas de Manel (20-oct)", "", "*Guion `explora_P7_67_campo.py` → `P7_67_explora.json`; lee los diarios; no toca nada sellado.*", "",
          "**8.1. ¿Por qué MIENTE y CONGELADA tienen criatura-días sin oportunidad en los días 16-20 y HONESTA ninguno?**", "",
          f"- Todos son del día {', '.join(map(str, dias19))}: {r1['total']} criatura-días (MIENTE y CONGELADA a partes iguales). Destino de la mentira ese día: {', '.join(str(d) for d in dest19)}. Las {len(q1['con_oportunidad_dia_19'])} criatura-días del día 19 que sí tuvieron oportunidad son todas de la serie {', '.join(sorted({str(c['serie']) for c in q1['con_oportunidad_dia_19']}))}.",
          f"- La invitación se cargó en {r1['invitacion_cargada']} de {r1['total']}; el destino es suelo transitable en el mapa fijo en todas ({', '.join(f'{k} {v}' for k, v in r1['casillas'].items())}). `ir_sitio` no se ofreció en ningún tic en {r1['total'] - r1['ir_sitio_ofrecido_algun_tic']} de {r1['total']}.",
          f"- Distancia al destino al empezar: ella {', '.join(f'{k} ({v})' for k, v in r1['distancia_al_empezar_ella'].items())}; su hermana {', '.join(f'{k} ({v})' for k, v in r1['distancia_al_empezar_hermana'].items())}. La hermana del asiento 11 sale del pedestal (18, 9) exactamente a 15 casillas, el borde de la regla 8-15; tras su primer paso queda a: {', '.join(f'{k} ({v})' for k, v in r1['distancia_hermana_tras_su_primer_paso'].items())}.",
          f"- En los tics con elección (más de un candidato; con uno solo, `noop`, el cuerpo no ofrece ningún movimiento), {r1['tics_con_eleccion']} en total: la hermana fuera de 8-15 en {r1['de_ellos_hermana_fuera_8_15']}, ella fuera de 8-15 en {r1['de_ellos_ella_fuera_8_15']}, sin calma en {r1['de_ellos_sin_calma']}. En cada criatura-día solo hubo **un** tic con elección y todo a la vez: el primer tic vivo.",
          f"- Y en el primer tic vivo la invitación no se ofrece nunca, en todo el campo: la primera oferta llega como pronto en el tic {t0['minimo']} ({t0['en_el_tic_0']} ofertas en el tic 0, de {t0['criatura_dias_con_oferta']} criatura-días con oferta).",
          "- **Lectura descriptiva:** la condición que falló es la distancia 8-15 a las dos hermanas, por la hermana del asiento 11, que empieza a 15 y da su primer paso alejándose. No falló la calma, no faltó una casilla de borde válida ni el destino era inalcanzable. HONESTA no tiene este caso: sus destinos están en el centro.", "",
          "**8.2. HONESTA: ¿por qué bajan los aciertos en los días 16-20?**", "",
          "- Aciertos de HONESTA por destino, días 1-20: " + "; ".join(f"{k}: {v['aciertos']} de {v['llegadas']} (días {', '.join(map(str, v['dias']))})" for k, v in X["honesta_aciertos_por_destino_dias_1_20"].items()) + ".",
          "", "| día | destino | llegadas | aciertos | sin botiquín a la vista | botiquines vistos (mediana) | el más cercano al destino (mediana, casillas) | destino dentro de la zona | radio de la zona | tic de llegada (mediana) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for d, v in q2.items(): L.append(f"| {d} | {tuple(v['destino'])} | {v['llegadas']} | {v['aciertos']} | {v['sin_botiquin_a_la_vista']} | {v['botiquines_vistos_mediana']} | {v['mas_cercano_mediana']} | {v['destino_dentro_de_la_zona']} de {v['llegadas']} | {', '.join(map(str, v['radio_zona']))} | {v['tic_llegada_mediana']} |")
    L += ["", "- Botiquines en el mapa entero al llegar: **no consta** (el diario solo trae lo que la criatura ve). Lo visible: casi siempre hay botiquines a la vista; lo que cambia es a qué distancia del destino.",
          "- El destino estaba dentro de la zona segura en todas las llegadas: se llega hacia el tic 600, mucho antes de que la zona empiece a cerrarse.",
          "- **Lectura descriptiva:** los aciertos dependen del destino del día. En los días 16-20 tocaron dos veces (27, 23) y dos veces (21, 24), los destinos donde el botiquín más cercano queda más a menudo a más de 3 casillas; el día 16, con (24, 23), acierta 32 de 32."]
L += ["", "## 9. Gasto", "", f"- **Créditos de la plataforma:** {creditos} créditos de experiencia ({len(P)} partidas del campo + {len(apart)} reintentos por partidas apartadas). Saldo real: **no consta**; la API de la plataforma no da el saldo (todas las rutas probadas responden 404). Hay que leerlo en la web.",
      "- **Dólares de la consola de Anthropic:** 0 $ (no se llama a la razón).", ""]
open(os.path.join(AQUI, "informe_P7_67_campo.md"), "w").write("\n".join(L)); print("\n".join(L))
