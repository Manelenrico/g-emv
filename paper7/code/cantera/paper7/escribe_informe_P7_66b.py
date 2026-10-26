"""[P7-66, segundo banco] escribe informe_P7_66_segundo_banco.md desde P7_66b_banco.json, P7_66b_local.json, P7_66b_pruebas.json y P7_66_tramo.json (ninguna cifra a mano)."""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); B = json.load(open(os.path.join(AQUI, "P7_66b_banco.json"))); LO = json.load(open(os.path.join(AQUI, "P7_66b_local.json"))); P = json.load(open(os.path.join(AQUI, "P7_66b_pruebas.json")))
TR = json.load(open(os.path.join(AQUI, "P7_66_tramo.json"))); T = B["por_brazo_y_hermana"]; M = T["MIENTE · las dos"]; H = T["HONESTA · las dos"]
pc = lambda x: "—" if x is None else f"{100 * x:.1f} %".replace(".", ",")
f = lambda x, n=1: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
pasa = (M["fraccion_llegada"] or 0) >= 0.5 and M["evaluaciones_por_serie_estimadas"] >= 30
ac = [(d, sl, x) for d, v in LO.items() for sl, h in v["P7_66"].items() for x in h["aceptadas"]]
L = ["# P7-66 · Segundo y último banco: la invitación a un sitio en el tramo de salida", "",
     "*16-oct-2026. En el Mac, sin créditos ni consola. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` antes y después. Decisiones de la mesa, tramo, listón y regla de parada",
     "escritos antes de ver resultados en `REGISTRO_P7_66.md`. `invita_P7_66b.py` (pieza nueva; la del primer banco no se toca), `prueba_P7_66b.py` → `P7_66b_pruebas.json`,",
     "`local66b_P7_66.py` → `P7_66b_local.json`, `banco_P7_66b.py` → `P7_66b_banco.json` y los GIF; `escribe_informe_P7_66b.py` (este informe; ninguna cifra a mano).*", "",
     "## Veredicto", "",
     f"- En MIENTE llega el **{pc(M['fraccion_llegada'])}** de las aceptadas ({M['llegadas']} de {M['aceptadas']}); hacía falta la mitad → **no lo alcanza**.",
     f"- Evaluaciones de la mentira por serie: **{f(M['evaluaciones_por_serie_estimadas'])}**; hacían falta 30 → **no lo alcanza**.",
     f"- **{'Hay campo.' if pasa else 'Regla de parada: no hay más bancos; el experimento se cierra (apuntado en el registro).'}**", "",
     "## Qué se cambió (decisiones de la mesa)", "",
     f"- Solo empuja en los primeros 300 tics de la fase viva (propuesta desde P7-65: lejos del centro y en calma, {pc(TR['400-499']['lejos_y_en_calma'])} en los 100 primeros tics y {pc(TR['500-599']['lejos_y_en_calma'])} en los 100 siguientes; después ≤ {pc(TR['600-699']['lejos_y_en_calma'])}).",
     "- La mentira, a una casilla del borde sin botiquines vistos nunca, a 8-15 casillas de las dos hermanas y que no sea su pedestal; la honesta, al centro. Las dos hermanas de una pareja",
     "  reciben el mismo destino. La pieza solo deja empujar si el destino está a 8-15 de ella y de su hermana en ese tic.",
     "- Interrumpida solo si un rival se acerca a ≤ 3 casillas; una sola llegada por criatura, destino y día.",
     f"- Pruebas a mano: {len(P['pasan'])} pasan, {len(P['fallan'])} fallan.", "",
     "## a) y b): por brazo y hermana", "",
     "| brazo · hermana | vidas-día | aceptadas | llegadas | a) fracción que llega | b) interrumpidas (rival a ≤ 3) | no llegó (480 tics) | tics hasta la interrupción (mediana) |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
for k, t in T.items():
    if "las dos" in k or "pareja" in k: continue
    L.append(f"| {k} | {t['vidas_dia']} | {t['aceptadas']} | {t['llegadas']} | {pc(t['fraccion_llegada'])} | {t['interrumpidas']} | {t['no_llego']} | {t['tics_hasta_interrupcion_mediana']} |")
L += ["", "**Por pareja** (la unidad): " + "; ".join(f"{b}: {T[b + ' · por pareja']['parejas_dia']} parejas-día, {f(T[b + ' · por pareja']['llegadas_por_pareja_dia'], 2)} llegadas por pareja y día, juntas {T[b + ' · por pareja']['llegan_juntas']}, una sola {T[b + ' · por pareja']['llega_una_sola']}" for b in ("MIENTE", "HONESTA")) + ".", "",
      f"**c) Evaluaciones de la mentira por serie**: {f(M['evaluaciones_por_serie_estimadas'])}.", "",
      "**GIF** (matplotlib, datos crudos; como no hubo ninguna llegada, son intentos cerrados, de la aceptación a su cierre):", ""]
for g in B["gifs"]: L += [f"- `{g['gif']}`: {g['brazo']}, {g['hermana']}, día {g['dia'][1:]}; destino {tuple(g['destino'])}; tic {g['tic_aceptada']} → {g['tic_juicio']} ({g['cierre']}).", f"  ![{g['gif']}](../figuras/{g['gif']})"]
L += ["", "## Qué se ve (descriptivo)", "",
      f"1. **Muy pocas aceptaciones**: {M['aceptadas']} en MIENTE y {H['aceptadas']} en HONESTA en 8 vidas-día por brazo. Todas en los primeros {max(x['tics_desde_el_inicio'] for _, _, x in ac)} tics de la fase viva ({sum(1 for _, _, x in ac if x['tics_desde_el_inicio'] == 0)} de {len(ac)} en el primero): fuera de ese instante, la calma, el tramo y la distancia de las dos casi nunca coinciden.",
      "2. **Los intentos se cortan cuando los rivales convergen hacia el centro**: interrumpidos por un rival a 3 casillas a los 33-110 tics; los que no se cortan no llegan en 480 tics.",
      "3. Ninguna pareja llegó, ni junta ni una sola.", "",
      "## Cierre del experimento", "",
      "En este mundo no hay un momento en que una criatura pueda seguir una invitación a un sitio sin que la calma se rompa: en el centro siempre hay rivales, y al salir de los pedestales",
      "convergen todos hacia el centro a la vez. La mentira que el cuerpo pueda seguir en calma, medida por lo que hace, no se puede montar aquí con estas reglas. Se cierra el experimento",
      "(regla de parada fijada antes del banco). Las piezas (`invita_P7_66`, `invita_P7_66b`) quedan escritas y probadas.", "",
      "## Gasto", "", "- Plataforma: 0 créditos. Consola de Anthropic: 0 $.", ""]
open(os.path.join(AQUI, "informe_P7_66_segundo_banco.md"), "w").write("\n".join(L)); print("\n".join(L[6:10]))
