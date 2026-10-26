"""[P7-61] escribe informe_P7_61_intermedio.md desde P7_61_intermedio.json y P7_57_estado.json (ninguna cifra a mano). python3 escribe_informe_P7_61_intermedio.py"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(AQUI, "P7_61_intermedio.json"))); E = json.load(open(os.path.join(AQUI, "P7_57_estado.json")))
C, SM, VG = R["con_todas"], R["sin_marcadas"], R["vigilancia"]
f = lambda x, n=3: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
lst = lambda xs, n=3: " · ".join(f(x, n) for x in xs)
dirn = lambda m: "la prevista" if m.get("direccion_prevista") else "la contraria"
def fila(nom, txt, m, ms, a, b):
    return f"| {nom} | {txt} | {a} {lst(m['A'])} → {f(m['media_A'])} | {b} {lst(m['B'])} → {f(m['media_B'])} | {f(m['dif'])} ± {f(m['ee'])} ({f(m['en_ee'], 1)} ee; sin marcadas {f(ms['en_ee'], 1)} ee) | {dirn(m)} |"
J = VG["juicio_de_la_falsa"]; RF = VG["refuerzo_intermitente"]; B1 = C["M1b"]; B2 = C["M2b"]
partidas = len(E["peticiones"]) + len(E.get("reintentos", [])); usd = sum(r.get("usd_supuesto", 0) for r in E.get("razon", [])); nraz = len(E.get("razon", []))
L = ["# P7-61 · INTERMEDIO · El campo de la mentira: lectura de las series 1-3 (declarada y NO vinculante)", "",
     f"*14-oct-2026. **INTERMEDIO** (addendum 6 del sello): sobre las series {', '.join(map(str, R['series']))} ({R['vidas']} vidas); la serie 4 se juega pase lo que pase y **el veredicto sellado será",
     "el de las 4 series** (o las que pida el addendum 4). Tras esta lectura no se cambia ninguna pieza, medida ni criterio. `analiza_P7_61.py` → `P7_61_intermedio.json`;",
     "`escribe_informe_P7_61_intermedio.py` (ninguna cifra a mano). Comparación: CON_RAZON de P7-56 (3 series). `motor/model.py` intacto.*", "",
     f"Comprobación: las invitaciones de cada vida reconstruidas (honestas de la respuesta guardada + la falsa en su posición) cuadran con el arranque en todas ({R['n_no_cuadran']} que no).", "",
     "## INTERMEDIO · Las predicciones (una observación por serie; ≥ 3 ee para pasar)", "",
     "| | qué | A (por serie → media) | B (por serie → media) | A − B ± ee | dirección |", "|---|---|---|---|---|---|",
     fila("M1", "confianza en el cuerpo, d14-20", C["M1"], SM["M1"], "MIENTEN_DOS", "CON_RAZON P7-56"),
     fila("M2", "verdaderas aceptadas / cargadas, d12-20", C["M2"], SM["M2"], "MIENTEN_DOS", "CON_RAZON P7-56"),
     fila("M3", "valiente: aceptaciones de la falsa / oportunidades, d10-20", C["M3"], SM["M3"], "MIENTE_UNA", "MIENTEN_DOS"), "",
     f"MIENTE_UNA, de referencia: M1 {lst(C['M1']['MIENTE_UNA'])}; M2 {lst(C['M2']['MIENTE_UNA'])}. M3: {', '.join(f'{k}: {v['MIENTE_UNA']['aceptaciones']}/{v['MIENTE_UNA']['oportunidades']} frente a {v['MIENTEN_DOS']['aceptaciones']}/{v['MIENTEN_DOS']['oportunidades']}' for k, v in C['M3']['detalle'].items())} (la falsa estuvo activa todos los días 10-20).", "",
     "**INTERMEDIO: ninguna pasa.** M1 y M2 van en la dirección contraria o sin diferencia (con la mentira, la confianza en el cuerpo y la aceptación de verdaderas no bajan); M3 va al revés de lo",
     "previsto: la valiente con la hermana honesta acepta la falsa MÁS, no menos.", "",
     "## INTERMEDIO · M1b (cada evaluación de la falsa: confianza en el cuerpo después − antes) y la comprobación por criatura (addendum 5)", "",
     "| | evaluaciones | media ± ee (por evaluación) | criaturas que caen | ee agrupado por criatura |", "|---|---:|---|---|---|"]
for k in ("MIENTEN_DOS", "MIENTE_UNA", "los dos"):
    m = B1[k]; L.append(f"| {k} | {m['n']} | {f(m['media'])} ± {f(m['ee'])} ({f(m['en_ee'], 1)} ee) | {m['criaturas_que_caen']} de {m['criaturas']} | {f(m['ee_agrupado'])} ({f(m['en_ee_agrupado'], 1)} ee) |")
L += ["", "Por criatura (n · media): " + "; ".join(f"{k} {v['n']} · {f(v['media'])}" for k, v in B1["los dos"]["por_criatura"].items()) + ".", "",
      f"**INTERMEDIO**: la dirección es la prevista (cae), pero por evaluación no llega ({f(B1['los dos']['en_ee'], 1)} ee; sin marcadas {f(SM['M1b']['los dos']['en_ee'], 1)}). La caída la llevan las valientes de",
      f"MIENTE_UNA (las tres caen); la prudente de MIENTEN_DOS de la serie 3, con {B1['los dos']['por_criatura'].get('s3 MIENTEN_DOS a11', {}).get('n')} evaluaciones, casi no se mueve. El ee agrupado es MENOR que el de",
      "evaluación porque la variación está dentro de cada criatura (aciertos y fallos alternan), no entre criaturas: no es un error, pero con 9 criaturas se lee con cuidado.", "",
      "## INTERMEDIO · M2b (aceptar verdaderas con cuerpo, 2 noches después − 2 antes del primer fallo de la falsa)", "",
      f"Criaturas con fallo de la falsa: {B2['criaturas_con_fallo']} de {B2['criaturas_con_falsa_evaluada']} con la falsa evaluada; entran {B2['entran']}. Cambio medio {f(B2['media_A'])} frente a {f(B2['media_B'])} en la misma ventana de CON_RAZON de P7-56:",
      f"{f(B2['dif'])} ± {f(B2['ee'])} ({f(B2['en_ee'], 1)} ee), dirección {dirn(B2)}. Sin potencia (addendum 2); se informa con su dirección.", "",
      "## INTERMEDIO · Vigilancia", "",
      "| brazo · hermana | vidas | puesto medio | muertes | vida perdida media | usos del botiquín · cortados | vida perdida en curas cortadas (por vida) |", "|---|---:|---:|---:|---:|---|---:|"]
for grupo in ("P7_57", "P7_56_CON_RAZON"):
    for k, v in VG[grupo].items(): L.append(f"| {k}{' (P7-56)' if grupo != 'P7_57' else ''} | {v['vidas']} | {f(v['puesto_medio'], 2)} | {v['muertes']} | {f(v['vida_perdida_media'], 1)} | {v['usos_kit']} · {v['cortados']} | {f(v['vida_perdida_en_curas_cortadas_por_vida'], 1)} |")
L += ["", f"**Refuerzo intermitente**: de {RF['evaluaciones']} evaluaciones de la falsa, {RF['aciertos_de_la_falsa']} la confirman ({f(100 * RF['fraccion_que_confirma'], 0)} %; suben la confianza {f(RF['subida_media_si_acierta'])} de media) y {RF['fallos']} la",
      f"desmienten ({f(RF['caida_media_si_falla'])}); caída media neta {f(B1['los dos']['media'])} frente a {f(RF['P7_56_falsas_caida_media'])} de las falsas de P7-56 (que fallaban siempre). Además, {RF['contrastes_con_lo_contado_sobre_la_falsa']} contrastes con lo",
      f"contado por la hermana tocaron la falsa y {RF['contrastes_que_confirman']} la confirmaron (cambio medio por contraste {f(RF['cambio_medio_por_contraste'])}).", "",
      "## INTERMEDIO · ¿Algo roto en el funcionamiento? (aparte de los números)", "",
      f"1. **La falsa no se juzga como dice el sello.** El sello (y P7-57) dice: si la cura se corta, se evalúa a los 480 tics por el cambio de vida (casi siempre fallo). El código de",
      f"   `invita_P7_54` (que no se toca) juzga con el PRIMER uso del botiquín SIN corte dentro de los 480 tics tras aceptar; un uso cortado no cuenta y espera al siguiente. De {J['evaluaciones']} evaluaciones,",
      f"   {J['primer_uso_cortado']} tuvieron el primer uso cortado por un golpe y aun así {J['primer_uso_cortado_y_acierto']} acabaron como ACIERTO (lo juzgó una cura posterior sin golpe); por 480 tics: {RF['por_fuente'].get('sin huella (480 tics)', 0)}.",
      f"2. **La falsa se desmiente por el techo de vida, no por los golpes.** De {J['fallos']} fallos, {J['fallos_por_techo_de_vida']} son curas sin corte que llegaron a 100 (la vida de partida era alta: media {f(J['hp0_medio_fallos'], 1)}",
      f"   en los fallos frente a {f(J['hp0_medio_aciertos'], 1)} en los aciertos): la cura no podía dar +25. La lección que recibe la confianza es «el botiquín no cura cuando estoy casi sana», no «no cura si me golpean».",
      "3. **Lo contado confirma la falsa fuera de su situación.** El contraste de `invita_P7_57` compara lo contado con la promesa por OBJETO, sin mirar la situación: una cura de la hermana en calma",
      "   «confirma» una promesa hecha para la amenaza. Es el diseño sellado (no un fallo de código), pero añade refuerzo que la mentira no debería recibir.",
      "4. Lo demás funciona: la falsa se inserta en todas las noches previstas (días 8-20 en los asientos que mienten), se activa todos los días, las invitaciones reconstruidas cuadran con el",
      f"   arranque, la guarda y los reintentos funcionaron, y las noches sin razón ({len(E.get('noches_sin_razon', []))}) quedaron anotadas.", "",
      "Con 1 y 2, M1-M3 y M1b miden una mentira que el cuerpo apenas puede desmentir por lo que la hace falsa (los golpes). **No se cambia nada** (addendum 6); se propone para después del campo",
      "que la mesa decida si el juicio de la falsa debe contar el uso cortado y descontar el techo de vida.", "",
      f"## Gasto (hasta el cierre de la serie 3)", "",
      f"- Plataforma: {partidas} partidas pedidas (humo, 3 series y 2 reintentos; alguna cuenta 0); último saldo leído: 19 créditos (14-oct, 17:03).",
      f"- Consola de Anthropic: {f(usd, 2)} $ en {nraz} llamadas a la razón (tarifa supuesta 3/15 $ por millón).", ""]
open(os.path.join(AQUI, "informe_P7_61_intermedio.md"), "w").write("\n".join(L)); print("\n".join(L))
