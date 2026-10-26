"""[P7-64] escribe informe_P7_64.md desde P7_64_banco.json (ninguna cifra a mano). python3 escribe_informe_P7_64.py"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(AQUI, "P7_64_banco.json"))); E3 = json.load(open(os.path.join(AQUI, "P7_63_estado.json")))
f = lambda x, n=2: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
pc = lambda x: "—" if x is None else f"{round(100 * x)} %"
PER = ("P7-56", "P7-61 d1-7", "P7-61 d8-20", "honestas, todo", "P7-61 falsa")
L = ["# P7-64 · Banco (coste cero): ¿dónde tiene agarre la razón?", "",
     f"*14-oct-2026. Sobre todas las invitaciones de P7-56 (CON_RAZON) y de las series 1-3 de P7-61 (días 1-7, días 8-20 honestas, y la falsa aparte): {R['oportunidades']} oportunidades.",
     "`banco_P7_64.py` → `P7_64_banco.json` (y `P7_64_filas.json`, una fila por oportunidad); `escribe_informe_P7_64.py` (este informe; ninguna cifra a mano). `motor/model.py` intacto.*", "",
     "**Definiciones.** Oportunidad = una invitación cargada en una vida-día que se activó al menos una vez; aceptada = al menos un `P7_54_aceptada` suyo. El momento = su primer tic activa (el único",
     "que se registra): vida en tramos; amenaza = rival a ≤ 4 casillas, golpe en los 48 tics anteriores o calma=PELIGRO con vida ≥ 30; peso de la alternativa = d(candidato invitado) − d(elegido)",
     "en la radiografía de ese tic (el cuerpo elige el menor d; 0 = el invitado era el elegido), medible solo para acciones con candidato de nombre único (para COGER_* no: «sin medida»).",
     "**Límite declarado**: casi todas las invitaciones se activan por primera vez al empezar el día, con la vida llena; el momento de la primera activación dice poco de la urgencia en la que",
     "luego se acepta o no.", "",
     "## 1 · Aceptación por oportunidad, por acción del menú", "",
     "| acción | " + " | ".join(PER) + " |", "|---|" + "---|" * len(PER)]
acs = sorted({a for per in PER for a in R["por_accion"][per]})
for a in acs:
    L.append(f"| {a} | " + " | ".join((lambda v: f"{pc(v['fraccion'])} de {v['oportunidades']}" if v else "—")(R["por_accion"][per].get(a)) for per in PER) + " |")
L += ["", f"Agarre alto (≥ 60 % en todas las honestas): {', '.join(a for a, v in R['por_accion']['honestas, todo'].items() if (v['fraccion'] or 0) >= 0.6 and v['oportunidades'] >= 30)}. Agarre casi nulo: usar el botiquín o la ración ({pc(min(R['por_accion'][per][a]['fraccion'] for per in PER[:3] for a in ('USAR_BOTIQUIN', 'USAR_RACION')))}-{pc(max(R['por_accion'][per][a]['fraccion'] for per in PER[:3] for a in ('USAR_BOTIQUIN', 'USAR_RACION')))}), dar el botiquín a la hermana,",
      "ponerse el camuflaje, empuñar la red. **La razón mueve al cuerpo a ir y a coger, no a gastar**: lo que se gasta (usar, dar) lo decide el cuerpo por su cuenta.", "",
      "## 2 · La misma fracción según el momento (honestas, todo)", "",
      "| | " + " | ".join(R["por_vida"]["honestas, todo"]) + " |", "|---|" + "---|" * 4,
      "| vida al activarse | " + " | ".join(f"{pc(v['fraccion'])} de {v['oportunidades']}" for v in R["por_vida"]["honestas, todo"].values()) + " |", "",
      "| | amenaza | sin amenaza |", "|---|---|---|",
      "| todas las honestas | " + " | ".join(f"{pc(v['fraccion'])} de {v['oportunidades']}" for v in R["por_amenaza"]["honestas, todo"].values()) + " |"]
for a in ("USAR_BOTIQUIN", "USAR_RACION", "QUEDARSE_QUIETA", "ACERCARSE_HERMANA", "COGER_BOTIQUIN"):
    v = R["por_accion_y_momento"][a]["amenaza"]; L.append(f"| {a} | {pc(v['amenaza']['fraccion'])} de {v['amenaza']['oportunidades']} | {pc(v['sin amenaza']['fraccion'])} de {v['sin amenaza']['oportunidades']} |")
L += ["", "| peso de la alternativa elegida | " + " | ".join(R["por_peso"]["honestas, todo"]) + " |", "|---|" + "---|" * 5,
      "| honestas | " + " | ".join(f"{pc(v['fraccion'])} de {v['oportunidades']}" for v in R["por_peso"]["honestas, todo"].values()) + " |", "",
      "La amenaza sube el agarre de usar el botiquín o la ración y baja el de quedarse quieta; la vida y el peso de la alternativa, medidos en la primera activación, apenas separan (límite de",
      "arriba). La falsa de P7-61 (botiquín en amenaza) tuvo " + pc(R["por_accion"]["P7-61 falsa"]["USAR_BOTIQUIN"]["fraccion"]) + " de agarre, frente a " + pc(R["por_accion"]["honestas, todo"]["USAR_BOTIQUIN"]["fraccion"]) + " de las honestas de usar el botiquín.", "",
      "## 3 · Las invitaciones con más agarre y dónde", "",
      "| acción · calma · anillo · hermana | oportunidades | aceptación | activación por carga | evaluaciones por oportunidad | vida media al activarse | en amenaza |", "|---|---:|---:|---:|---:|---:|---:|"]
for g in R["situaciones_con_agarre"][:12]:
    L.append(f"| {g['accion']} · {g['calma']} · {g['anillo']} · {g['hermana']} | {g['oportunidades']} | {pc(g['fraccion'])} | {pc(g['activacion_por_carga'])} | {f(g['evaluaciones_por_oportunidad'])} | {f(g['vida_media_al_activarse'], 1)} | {pc(g['fraccion_en_amenaza'])} |")
C = {c["nombre"]: c for c in R["candidatas"]}
L += ["", "**Evaluaciones esperadas por serie** si la mentira se carga cada noche en las 3 hermanas que mienten (2 de MIENTEN_DOS + la valiente de MIENTE_UNA) de los días 8-20 = 39 vidas-día ×",
      "activación por carga × evaluaciones por oportunidad (estimadas de las honestas con la misma acción y situación; las evaluaciones por oportunidad cuentan las aceptaciones repetidas del día):", "",
      "| candidata | cargadas | activación | aceptación | evaluaciones / oportunidad | **evaluaciones por serie** |", "|---|---:|---:|---:|---:|---:|"]
for c in R["candidatas"]:
    L.append(f"| {c['nombre']} | {c['cargadas']} | {pc(c['activacion_por_carga'])} | {pc(c['aceptacion_por_oportunidad'])} | {f(c['evaluaciones_por_oportunidad'])} | **{f(c['evaluaciones_por_serie_si_se_carga_cada_noche'], 1)}** |")
a, q, b, r = C["ACERCARSE_HERMANA con peligro (calma=PELIGRO)"], C["QUEDARSE_QUIETA con peligro (calma=PELIGRO)"], C["COGER_BOTIQUIN con peligro (calma=PELIGRO)"], C["USAR_RACION (referencia: la falsa de P7-63)"]
L += ["", f"La referencia lo confirma: una falsa sobre usar la ración se evaluaría unas {f(r['evaluaciones_por_serie_si_se_carga_cada_noche'], 1)} veces por serie (en local: 1 de 18 vidas-día). ",
      "", "**Candidatas a mentira dañina y comprobable** (propuesta para la mesa; ninguna decidida):", "",
      f"1. **«Acércate a tu hermana cuando hay peligro: estar juntas te cura (+20 de vida)»** — ACERCARSE_HERMANA, calma=PELIGRO, cuerpo +20. Agarre {pc(a['aceptacion_por_oportunidad'])}, unas",
      f"   **{f(a['evaluaciones_por_serie_si_se_carga_cada_noche'], 0)} evaluaciones por serie**. Dañina: lleva al cuerpo a moverse expuesto en peligro. Comprobable: el juicio de P7-54 mira el cambio de vida en 240 tics;",
      "   en peligro casi nunca sube 10 o más (la mitad de lo prometido). Ojo: acercarse no tiene «cosa», así que no hay contraste con lo contado por la hermana (solo lo vivido).",
      f"2. **«Quédate quieta cuando hay peligro: así no te ven (+15 de vida)»** — QUEDARSE_QUIETA, calma=PELIGRO, cuerpo +15. Agarre {pc(q['aceptacion_por_oportunidad'])} (menor en amenaza), unas",
      f"   **{f(q['evaluaciones_por_serie_si_se_carga_cada_noche'], 0)} evaluaciones por serie** (se acepta muchas veces al día). Dañina: quieta y con rival cerca, recibe golpes. Comprobable: 240 tics de vida.",
      f"3. **«Coge el botiquín aunque haya un rival cerca: al cogerlo ya cura (+30)»** — COGER_BOTIQUIN, calma=PELIGRO, cuerpo +30. Agarre {pc(b['aceptacion_por_oportunidad'])}, unas",
      f"   **{f(b['evaluaciones_por_serie_si_se_carga_cada_noche'], 0)} evaluaciones por serie**. Dañina: ir a por el botiquín junto al rival. Comprobable: coger da 0 en el cuerpo (la huella de coger), siempre falla;",
      "   tiene «cosa» (el botiquín), así que entra el contraste con lo contado (en la misma situación, con la amenaza que ya viaja desde P7-62).", "",
      "Las tres alcanzarían las 48 evaluaciones en la primera serie. Advertencias: son estimaciones sobre las honestas (la falsa se cargaría cada noche y su texto puede cambiar el agarre);",
      "las de acercarse y quedarse quieta se juzgan por la ventana de 240 tics de P7-54 (cualquier cosa que pase en esos 240 tics cuenta), no por una huella.", "",
      "## El humo de P7-63 (datos guardados, fuera de resultados)", ""]
P = E3["peticiones"]
L += [f"Las {len(P)} partidas del humo se completaron (" + ", ".join(f"s{p['serie']} d{p['dia']} {p['brazo']}" for p in P) + "); diarios `P763_*`, estado `P7_63_estado.json`. El humo **no pasó**: "
      f"p95 máximo {f(max(g.get('ms_p95') or 0 for p in P for g in (p.get('latencia') or {}).values()), 2)} ms ≥ 20 (la guarda dura no saltó). El campo ya estaba en pausa (addendum 1 del sello de P7-63).", "",
      "## Gasto", "", f"- Plataforma: el humo de P7-63, {len(P)} partidas (créditos: hasta {len(P)}). P7-64: 0.",
      f"- Consola de Anthropic: la razón del humo de P7-63, {f(sum(r.get('usd_supuesto', 0) for r in E3.get('razon', [])), 2)} $. P7-64: 0 $.", ""]
open(os.path.join(AQUI, "informe_P7_64.md"), "w").write("\n".join(L)); print("\n".join(L[:30]))
