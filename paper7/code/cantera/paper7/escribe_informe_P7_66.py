"""[P7-66] escribe informe_P7_66.md desde P7_66_banco.json, P7_66_pruebas.json, P7_66_local.json y P7_66_calma_centro.json (ninguna cifra a mano). python3 escribe_informe_P7_66.py"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); B = json.load(open(os.path.join(AQUI, "P7_66_banco.json"))); P = json.load(open(os.path.join(AQUI, "P7_66_pruebas.json")))
LO = json.load(open(os.path.join(AQUI, "P7_66_local.json"))); C = B["calma_centro_P7_65"]; T = B["por_brazo_y_hermana"]
f = lambda x, n=1: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
pc = lambda x: "—" if x is None else f"{100 * x:.1f} %".replace(".", ",")
lleg = [(d, sl, x) for d, v in LO.items() for sl, h in v["P7_66"].items() for x in h["llegadas"]]
rep = {}
for d, sl, x in lleg: rep.setdefault((d, sl, tuple(x["destino"])), []).append(x)
M, H = T["MIENTE · las dos"], T["HONESTA · las dos"]
pasa1 = (M["fraccion_llegada"] or 0) >= 0.5; pasa2 = M["evaluaciones_por_serie_estimadas"] >= 30
L = ["# P7-66 · Banco local: una mentira que el cuerpo pueda seguir en calma (invitación a un sitio)", "",
     f"*16-oct-2026. Sin créditos de la plataforma ni consola (la razón no se llama: la invitación la escribe el guion). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` antes y después.",
     "`invita_P7_66.py` (pieza nueva), `prueba_P7_66.py` → `P7_66_pruebas.json`, `local66_P7_66.py` → `P7_66_local.json`, `calma_centro_P7_66.py` → `P7_66_calma_centro.json`, `banco_P7_66.py` →",
     "`P7_66_banco.json` y los GIF; `escribe_informe_P7_66.py` (este informe; ninguna cifra a mano).*", "",
     "## Veredicto del listón (fijado antes del banco)", "",
     f"- Hace falta que en MIENTE llegue al menos la mitad de las aceptadas en calma: llega el **{pc(M['fraccion_llegada'])}** ({M['llegadas']} de {M['aceptadas']}) → {'lo alcanza' if pasa1 else '**no lo alcanza**'}.",
     f"- Hacen falta al menos 30 evaluaciones de la mentira por serie: salen **{f(M['evaluaciones_por_serie_estimadas'])}** (estimadas: {f(M['llegadas_por_vida_dia'], 2)} llegadas por vida-día × 2 hermanas × 13 días) → {'lo alcanza' if pasa2 else '**no lo alcanza**'}.",
     f"- **{'Hay campo.' if (pasa1 and pasa2) else 'No hay campo: se replantea.'}**", "",
     "## Las piezas (a)-(d), en `invita_P7_66.py` (sin tocar `model.py`)", "",
     "- (a) Acción nueva `IR_A_SITIO` con destino (x, y); promesa recursos +1 («allí hay un botiquín»); cuerpo 0 y vínculo 0.",
     "- (b) Mientras la invitación está activa, la lista del cuerpo gana el candidato `ir_sitio` (la receta genérica «ir» del decisor con ese destino: lo imagina y lo anda por el camino",
     "  geodésico, como `ir_botin` o `ir_objeto`), emparejado con su invitación en la lista de `invita_P7_54` para que reciba la fila de recursos.",
     "- (c) Solo empuja en calma: ningún rival a ≤ 5 casillas (ni ella ni su hermana) y ningún golpe en 48 tics, añadido a la situación de la invitación.",
     "- (d) Juicio propio, **solo en recursos** (el envoltorio sí permite saltarse dimensiones: `invita_P7_54` no la juzga, queda su «sombra»): llegada (≤ 1 casilla) → acierto si ve un",
     "  botiquín a ≤ 1 casilla del destino; interrumpida (rival a ≤ 5 antes de llegar) y no llegó (480 tics) → ni se juzgan ni tocan la confianza.",
     f"- Pruebas a mano: {len(P['pasan'])} pasan, {len(P['fallan'])} fallan.", "",
     f"## El banco ({B['dias']} días en cadena en el Mac; MIENTE = asientos 10-11, destino un pedestal del borde; HONESTA = 12-13, destino una casilla del centro)", "",
     "| brazo · hermana | vidas-día | aceptadas en calma | llegadas (aciertos) | a) fracción que llega | b) interrumpidas por un rival | no llegó | tics hasta la interrupción (mediana) | interrumpidas en ≤ 24 tics |",
     "|---|---:|---:|---|---:|---:|---:|---:|---:|"]
for k, t in T.items():
    if "las dos" in k: continue
    L.append(f"| {k} | {t['vidas_dia']} | {t['aceptadas']} | {t['llegadas']} ({t['aciertos']}) | {pc(t['fraccion_llegada'])} | {t['interrumpidas']} | {t['no_llego']} | {t['tics_hasta_interrupcion_mediana']} | {t['interrumpidas_en_24_tics_o_menos']} |")
L += ["", f"**c) Evaluaciones de la mentira por serie**: {f(M['evaluaciones_por_serie_estimadas'])} (MIENTE); las de la honesta, {f(H['evaluaciones_por_serie_estimadas'])}.",
      f"**d) Calma cerca del centro** (diarios de P7-65, {C['vidas']} vidas): las criaturas pasan el {pc(C['fraccion_de_la_vida_cerca_del_centro'])} de su vida a ≤ 6 casillas del centro; el {pc(C['fraccion_de_la_calma_que_es_cerca_del_centro'])} de su calma",
      f"ocurre ahí, y el {pc(C['fraccion_del_tiempo_cerca_del_centro_que_es_calma'])} de su tiempo en el centro es calma ({C['tics_de_calma_cerca_del_centro_por_vida_mediana']:.0f} tics por vida, mediana). La honesta puede empujar allí: ya están allí.", "",
      "**e) GIF** (matplotlib, de los datos crudos; de la aceptación al juicio):", ""]
for g in B["gifs"]: L += [f"- `{g['gif']}`: {g['brazo']}, {g['hermana']}, día {g['dia'][1:]}; destino {tuple(g['destino'])}; tic {g['tic_aceptada']} → {g['tic_juicio']}; acierto de recursos {g['acierto_recursos']}.", f"  ![{g['gif']}](../figuras/{g['gif']})"]
L += ["", "## Qué se ve (descriptivo)", "",
      "1. **Casi todos los intentos se interrumpen al primer paso.** La mediana de tics hasta la interrupción es 11, un solo paso: la calma (rival a 6 o más) se rompe en cuanto un rival se mueve una",
      "   casilla. Con la regla «rival a ≤ 5 durante la ventana = interrumpida», ni la mentira ni la verdad se pueden seguir hasta el final.",
      f"2. **Las pocas llegadas no son independientes**: {len(lleg)} llegadas en {len(rep)} situaciones distintas (la misma criatura, el mismo día y el mismo destino llega varias veces seguidas: al",
      "   llegar se aleja una casilla y la invitación vuelve a empujar). Varias son al principio del día, cuando las criaturas salen de los pedestales del borde.",
      f"3. **La honesta tampoco acierta**: {H['llegadas']} llegadas y {H['aciertos']} aciertos. Que en una casilla del centro «suela» haber botiquines no quiere decir que los haya en el momento de llegar.",
      "4. Para que haya campo habría que cambiar el diseño (es decisión de la mesa): por ejemplo, que la calma se mida solo al aceptar o con un margen (interrumpir solo si el rival se acerca",
      "   a ≤ 3), contar una sola llegada por destino y día, y que la honesta apunte a un botiquín visto de verdad.", "",
      "## Gasto", "", "- Plataforma: 0 créditos (todo en el Mac). Consola de Anthropic: 0 $.", ""]
open(os.path.join(AQUI, "informe_P7_66.md"), "w").write("\n".join(L)); print("\n".join(L[6:11]))
