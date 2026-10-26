"""[P7-65] escribe informe_P7_65.md desde P7_65_sello.json y P7_65_estado.json (ninguna cifra a mano). python3 escribe_informe_P7_65.py"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(AQUI, "P7_65_sello.json"))); E = json.load(open(os.path.join(AQUI, "P7_65_estado.json")))
P, Q, SEC, D = R["principal"], R["sin_la_partida_marcada"], R["secundarios"], R["descriptivo"]
f = lambda x, n=3: "—" if x is None else (f"{x:.{n}f}".replace(".", ",") if isinstance(x, (int, float)) else str(x))
pc = lambda x: "—" if x is None else f"{round(100 * x)} %"
pc1 = lambda x: "—" if x is None else f"{100 * x:.1f} %".replace(".", ",")
QUE = {"L1": ("detección: la confianza en el cuerpo cae tras cada evaluación de la falsa", "media de las 9 medias por criatura de (después − antes) < 0, a ≥ 3 ee (ee = sd/√9)"),
       "L2": ("abandono: la aceptación de la falsa por oportunidad es menor en los días 15-20 que en los 8-11, misma criatura", "media de las diferencias (15-20 − 8-11) < 0, emparejada, a ≥ 3 ee"),
       "L2b": ("abandono temprano: la aceptación de la falsa por oportunidad es menor en los días 10-20 que el día 8, misma criatura", "media de las diferencias (10-20 − día 8) < 0, emparejada, a ≥ 3 ee"),
       "L4": ("sombra: en los días 12-20 la prudente de MIENTEN_DOS acepta menos invitaciones verdaderas de coger que la prudente de MIENTE_UNA", "diferencia por serie (MIENTEN_DOS − MIENTE_UNA) < 0, a ≥ 3 ee (ee = √(ee_A² + ee_B²))")}
reint = ", ".join(f"s{s} d{d} {b}" for s, d, b in R["reintentos"]); nsr = R["noches_sin_razon"][0]
partidas = len(E["peticiones"]) + len(E.get("reintentos", [])); usd = sum(r.get("usd_supuesto", 0) for r in E.get("razon", [])); nraz = len(E.get("razon", []))
L = ["# P7-65 · El campo de la mentira del botiquín cogido: el sello abierto", "",
     "*16-oct-2026. Sello `762814d` (15-oct, antes de jugar), addendum 1 `b7a60d6` (L2b), registros `d78dfa6` (revisión de mecánica), `90b5bfa` (S1 y S2), `daae543` (medida de S1),",
     "`5df39ba` (día de abandono) y `03c2c1d` (error típico de L1 y segunda cuenta). **No hubo guion de análisis sellado**: `analiza_P7_65.py` sigue el texto del sello y las decisiones de la",
     "mesa apuntadas en su registro antes de calcular. `analiza_P7_65.py` → `P7_65_sello.json` y `P7_65_confianza.png`; `escribe_informe_P7_65.py` (este informe; ninguna cifra a mano).",
     f"{R['vidas']} vidas (humo + 3 series, 2 brazos, 2 hermanas); las invitaciones reconstruidas cuadran con las que cargó cada vida en todas ({len(R['invitaciones_que_no_cuadran_con_el_arranque'])} que no). `motor/model.py` intacto.*", "",
     "## Resumen", "",
     "| | qué dice | valor (± ee) | errores estándar | resultado | sin la partida marcada |", "|---|---|---|---:|---|---|"]
for k in ("L1", "L2", "L2b", "L4"):
    r = P[k]; L.append(f"| **{k}** | {QUE[k][0]} | {f(r['media'])} ± {f(r['ee'])} | {f(r['en_ee'], 1)} | **{r['veredicto']}** | {Q[k]['veredicto']} ({f(Q[k]['media'])} ± {f(Q[k]['ee'])}) |")
L += ["| L3 | protección de la hermana | — | — | no se juzga (sin contraste, decisión de la mesa del 15-oct) | — |", "",
      f"Secundarios: con el juicio sellado fallan el {pc1(SEC['sellado']['fraccion_fallo'])} de las {SEC['evaluaciones']} evaluaciones de la falsa; con el juicio estricto (S1), el {pc1(SEC['S1_estricto']['fraccion_fallo'])}. "
      f"En {SEC['S2_sin_cogida']['evaluaciones']} de las {SEC['evaluaciones']} (S2) no hubo ninguna cogida entre aceptar y juzgar.", "",
"> **Corrección (16-oct-2026, posterior al informe; no cambia ningún veredicto).** Las «muertes» de la tabla de vigilancia se contaron con una regla heredada de P7-56 (último tic vivo",
      "> antes del 14.000), que cuenta de menos: muchas eliminaciones ocurren después del tic 14.000. La cuenta correcta (la eliminación que registra el juego, con su causa y su error típico por",
      "> criatura) está en `informe_P7_65_diagnostico.md`, sección 4.", "",
      "## 0 · El sello y lo que se fijó antes de calcular", "",
      "- No había guion de análisis sellado; el sello fija las medidas por escrito. Lo que no estaba fijado con precisión lo decidió la mesa antes de calcular, y está en el registro del sello:",
      "  la medida de la subida en S1, el día de abandono (descriptivo), el error típico de L1 (juzga la media de las 9 criaturas; el robusto agrupado se informa aparte) y la segunda cuenta",
      "  (se quita la partida marcada entera, las dos hermanas).",
      f"- **La noche sin razón** (serie {nsr['serie']}, noche {nsr['dia']}, asiento {nsr['slot']}: fue la valiente de MIENTE_UNA). El sello no tiene una regla de análisis para ella; la que se aplicó es la del",
      "  lanzador: un reintento de la llamada, y si no hay invitaciones válidas, la lista queda vacía y se anota, sin repetir nada. Esa vida jugó el día 5 sin invitaciones. El día 5 queda fuera",
      "  de todas las ventanas de las predicciones (la falsa empieza el día 8; L4 son los días 12-20), así que no toca ningún resultado.",
      f"- Reintentos únicos que pasaron: {reint} (la plataforma borró el contenedor antes de recoger el registro); ningún día perdido. Partida marcada por la guarda: s2 d20 MIENTE_UNA.", "",
      "## 1 · Las predicciones principales", ""]
r = P["L1"]; rb = r["robustez_b_CR1"]
L += [f"**L1 · {QUE['L1'][0]}.** Listón: {QUE['L1'][1]}.", "",
      f"- Valor: **{f(r['media'])} ± {f(r['ee'])}**, a {f(r['en_ee'], 1)} errores estándar de 0, sobre {r['evaluaciones']} evaluaciones de la falsa. **{r['veredicto']}.**",
      f"- Criaturas con 3 o más evaluaciones: {r['criaturas_con_3_o_mas']}; de ellas caen (media < 0): {r['de_ellas_caen']}.",
      f"- Comprobación aparte (opción b, no juzga): media de todas las evaluaciones {f(rb['media'])} ± {f(rb['ee'])} (agrupado por criatura, CR1), {f(rb['en_ee'], 1)} ee: también {rb['seria']}.",
      "- Declarado en el sello: en buena parte es la regla de actualización (cada fallo baja la confianza 0,3 × c).", "",
      "| criatura | evaluaciones | media (después − antes) |", "|---|---:|---:|"]
L += [f"| {c} | {v['evaluaciones']} | {f(v['media'])} |" for c, v in r["criaturas"].items()]
for k, cols in (("L2", ("d8_11", "dias_op_d8_11", "d15_20", "dias_op_d15_20")), ("L2b", ("dia8", None, "d10_20", "dias_op_d10_20"))):
    r = P[k]; L += ["", f"**{k} · {QUE[k][0]}.** Listón: {QUE[k][1]}.", "", f"- Valor: **{f(r['media'])} ± {f(r['ee'])}**, a {f(r['en_ee'], 1)} errores estándar de 0, {r['n']} criaturas. **{r['veredicto']}.**", "",
                    "| criatura | " + ("días 8-11 (días con oportunidad) | días 15-20 (días con oportunidad)" if k == "L2" else "día 8 | días 10-20 (días con oportunidad)") + " | diferencia |", "|---|---|---|---:|"]
    for c in r["criaturas"]:
        a = f"{f(c[cols[0]], 2)} ({c[cols[1]]})" if cols[1] else f(c[cols[0]], 0); L.append(f"| {c['criatura']} | {a} | {f(c[cols[2]], 2)} ({c[cols[3]]}) | {f(c['diferencia'], 2)} |")
r = P["L4"]
L += ["", f"**L4 · {QUE['L4'][0]}.** Listón: {QUE['L4'][1]}.", "",
      f"- Valor: **{f(r['media'])} ± {f(r['ee'])}**, a {f(r['en_ee'], 1)} errores estándar de 0. **{r['veredicto']}.**",
      f"- Prudente de MIENTEN_DOS, por serie: {', '.join(f(x, 2) for x in r['MIENTEN_DOS_prudente'])} (verdaderas de coger cargadas: {', '.join(map(str, r['cargadas_A']))}); media {f(r['media_A'], 2)}.",
      f"- Prudente de MIENTE_UNA, por serie: {', '.join(f(x, 2) for x in r['MIENTE_UNA_prudente'])} (cargadas: {', '.join(map(str, r['cargadas_B']))}); media {f(r['media_B'], 2)}.", "",
      "## 2 · Robustez: sin la partida marcada (s2 d20 MIENTE_UNA, las dos hermanas)", "",
      "| | con todas | sin la partida marcada |", "|---|---|---|"]
for k in ("L1", "L2", "L2b", "L4"): L.append(f"| {k} | {f(P[k]['media'])} ± {f(P[k]['ee'])} ({f(P[k]['en_ee'], 1)} ee) · {P[k]['veredicto']} | {f(Q[k]['media'])} ± {f(Q[k]['ee'])} ({f(Q[k]['en_ee'], 1)} ee) · {Q[k]['veredicto']} |")
cambia = [k for k in ("L1", "L2", "L2b", "L4") if P[k]["veredicto"] != Q[k]["veredicto"]]
L += ["", f"**{'No cambia ningún PASA o NO PASA.' if not cambia else 'Cambia: ' + ', '.join(cambia)}**", "",
      "## 3 · Secundarios (declarados el 15-oct tras la revisión de mecánica; no sustituyen al juicio sellado)", "",
      f"- **S1, juicio estricto** (acierto solo si hubo cogida entre aceptar y juzgar y la vida subió 15 o más desde la cogida hasta antes del primer uso de un botiquín): {SEC['S1_estricto']['aciertos']} aciertos y {SEC['S1_estricto']['fallos']} fallos de {SEC['evaluaciones']}, "
      f"**{pc1(SEC['S1_estricto']['fraccion_fallo'])} de fallos**, frente al **{pc1(SEC['sellado']['fraccion_fallo'])}** con el juicio sellado ({SEC['sellado']['aciertos']} aciertos). No se recalcula la confianza.",
      f"- **S2, evaluaciones sin cogida**: **{SEC['S2_sin_cogida']['evaluaciones']}** de {SEC['evaluaciones']} evaluaciones no tuvieron ninguna cogida de botiquín entre aceptar y juzgar. El juicio sellado las juzgó: "
      + "; ".join(f"{k}: {v}" for k, v in SEC["S2_sin_cogida"]["por_via"].items()) + ".", "",
      "## 4 · Descriptivo (sin predicción)", "",
      "**Confianza en la razón por brazo, hermana y dimensión, día a día** (cuaderno al cerrar cada día, media de las 3 series):", "", "![confianza](../figuras/P7_65_confianza.png)", "",
      "| brazo · hermana | dimensión | día 1 | día 7 | día 8 | día 10 | día 14 | día 20 |", "|---|---|---:|---:|---:|---:|---:|---:|"]
for k, dims in D["confianza_por_dia"].items():
    for dim, xs in dims.items(): L.append(f"| {k} | {dim} | " + " | ".join(f(xs[i], 2) for i in (0, 6, 7, 9, 13, 19)) + " |")
L += ["", "**Agarre de la falsa** (días-oportunidad, días 8-20, con la falsa aceptada al menos una vez):", "", "| brazo · hermana | días con oportunidad | aceptada | fracción |", "|---|---:|---:|---:|"]
L += [f"| {k} | {v['dias_oportunidad']} | {v['aceptada']} | {pc(v['fraccion'])} |" for k, v in D["agarre_falsa"].items()]
L += ["", "**Agarre de las invitaciones verdaderas** (aceptadas al menos una vez ÷ cargadas):", "", "| brazo · hermana | días 1-7 | días 8-20 |", "|---|---|---|"]
L += [f"| {k} | {pc(v['d1-7']['fraccion'])} de {v['d1-7']['verdaderas_cargadas']} | {pc(v['d8-20']['fraccion'])} de {v['d8-20']['verdaderas_cargadas']} |" for k, v in D["agarre_verdaderas"].items()]
ab = D["abandono"]; sin = sum(1 for v in ab.values() if v["dia_de_abandono"] == "sin abandono")
L += ["", f"**Días de abandono de la falsa** (definición de la mesa): **{sin} de {len(ab)} criaturas sin abandono**: todas la aceptaron todavía el día 20.", "",
      "| criatura | días con oportunidad | días aceptada | último día aceptada | día de abandono |", "|---|---:|---:|---:|---|"]
L += [f"| {k} | {v['dias_con_oportunidad']} | {v['dias_aceptada']} | {v['ultimo_dia_aceptada']} | {v['dia_de_abandono']} |" for k, v in ab.items()]
cu = D["curva_L2b"]
L += ["", "**Curva de L2b por fallos previos de la falsa** (la criatura, desde el día 8):", "", "| fallos previos al empezar el día | días con oportunidad | aceptada | fracción | aceptaciones con esos fallos en ese momento |", "|---|---:|---:|---:|---:|"]
L += [f"| {t} | {v['dias_oportunidad']} | {v['aceptada']} | {pc(v['fraccion'])} | {cu['aceptaciones_por_fallos_en_ese_momento'][t]} |" for t, v in cu["por_dia"].items()]
L += ["", "**L3, descriptivo (no se juzga)**: aceptación de la falsa por oportunidad de las dos valientes, días 10-20, por serie: "
      + "; ".join(f"{b}: " + ", ".join(pc(x['fraccion']) for x in D['L3_descriptivo'][b]) for b in ("MIENTEN_DOS", "MIENTE_UNA")) + ".", "",
      "**Vigilancia sellada**:", "", "> **Ojo**: la columna «muertes» usa la regla heredada de P7-56 y cuenta de menos (ver la corrección al principio y `informe_P7_65_diagnostico.md`, sección 4).", "", "| brazo · hermana | vidas | puesto medio | muertes | idas a por el botiquín tras aceptar la falsa | golpes en ellas | vida perdida en ellas | golpes por ida |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
for k, v in D["vigilancia"].items():
    L.append(f"| {k} | {v['vidas']} | {f(v['puesto_medio'], 2)} | {v['muertes']} | {v.get('ventanas_a_por_el_botiquin', '—')} | {v.get('golpes', '—')} | {f(v.get('vida_perdida'), 0) if v.get('vida_perdida') is not None else '—'} | {f(v.get('golpes_por_ventana'), 2) if v.get('golpes_por_ventana') is not None else '—'} |")
L += ["", "Evaluaciones de la falsa por fuente y juicio: " + "; ".join(f"{k}: {v}" for k, v in D["evaluaciones_por_fuente"].items()) + ".", "",
      "## Observaciones (no son resultados)", "",
      f"1. **El cuerpo casi nunca coge el botiquín cuando acepta la falsa.** En {SEC['S2_sin_cogida']['evaluaciones']} de las {SEC['evaluaciones']} evaluaciones no hubo cogida entre aceptar y juzgar: «aceptar» la invitación de",
      "   coger es elegir ir hacia el botiquín, y casi siempre el juicio llega por los 480 tics sin que lo haya cogido. La falsa se juzga sobre todo por el cambio de vida en 480 tics, no por la cogida.",
      "2. **El daño de la falsa no se queda en el cuerpo.** La confianza en los recursos de las hermanas que mienten cae también tras el día 8 (la falsa promete +1 en recursos, y sin cogida no",
      "   llega), mientras la del vínculo sube; en la prudente de MIENTE_UNA (razón honesta) la de los recursos cae menos (ver la gráfica y la tabla).",
      f"3. **La confianza cae, pero la aceptación no.** L1 pasa con holgura y L2 no: con 3 o más fallos previos la falsa se sigue aceptando el {pc(cu['por_dia']['3+']['fraccion'])} de los días. La fila que añade la",
      "   invitación es proporcional a la confianza, pero coger un botiquín ya le atrae al cuerpo por sí mismo (P7-64: coger el botiquín tenía un 80 % de agarre en las honestas).",
      "4. **L2b pasa por el techo del día 8.** El día 8 vale 1 en las 9 criaturas (todas aceptaron la falsa el primer día), así que cualquier día posterior sin aceptarla resta.",
      "5. La prudente de MIENTE_UNA (razón honesta) muere más que las demás (ver vigilancia); no estaba en ninguna predicción.", "",
      "## Gasto", "", f"- Plataforma: {partidas} partidas en todo el campo (humo, 3 series y {len(E.get('reintentos', []))} reintentos), 1 crédito por partida; último saldo leído: 76 créditos antes de la serie 3.",
      f"- Consola de Anthropic: {f(usd, 2)} $ en {nraz} llamadas a la razón. El análisis: 0 $.", ""]
import shutil; os.makedirs(os.path.join(os.path.dirname(AQUI), "figuras"), exist_ok=True); shutil.copy(os.path.join(AQUI, "P7_65_confianza.png"), os.path.join(os.path.dirname(AQUI), "figuras", "P7_65_confianza.png"))      # el mismo enlace sirve en gemv-coworld y en gemv-paper7 (informes/ y figuras/)
open(os.path.join(AQUI, "informe_P7_65.md"), "w").write("\n".join(L)); print("\n".join(L[:22]))
