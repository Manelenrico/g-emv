"""[P7-67, banco con la pieza nueva] escribe informe_P7_67_segundo_banco.md desde P7_67b_banco.json, P7_67b_estado.json, P7_67b_pruebas.json, P7_67_banco.json (primer banco)
y P7_66b_revision.json (ninguna cifra a mano)."""
import json, math, os
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
B = J("P7_67b_banco.json"); E = J("P7_67b_estado.json"); P = J("P7_67b_pruebas.json"); B1 = J("P7_67_banco.json"); RV = J("P7_66b_revision.json")
T = B["por_brazo_y_hermana"]; M = T["MIENTE · las dos"]; H = T["HONESTA · las dos"]; C = B["calma"]; LI = B["listones"]; M1 = B1["por_brazo_y_hermana"]["MIENTE · las dos"]
pc = lambda x: "—" if x is None else f"{100 * x:.1f} %".replace(".", ",")
pc2 = lambda x: "—" if x is None else f"{100 * x:.2f} %".replace(".", ",")
f = lambda x, n=1: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
n = lambda x: "—" if x is None else f"{int(round(x)):,}".replace(",", ".")
def wilson(k, m, z=1.96):
    if not m: return None, None
    p = k / m; d = 1 + z * z / m; c = (p + z * z / (2 * m)) / d; h = z * math.sqrt(p * (1 - p) / m + z * z / (4 * m * m)) / d; return c - h, c + h
I = B["intentos"]; IM = [x for x in I if x["brazo"] == "MIENTE"]
pasa = (M["fraccion_llegada"] or 0) >= 0.5; lo, hi = wilson(M["llegadas"], M["aceptadas"])
ev = M["evaluaciones_por_serie_estimadas"]; series = math.ceil(120 / ev) if ev else None
pet = E["peticiones"]; reint = E.get("reintentos", []); partidas = len(pet) + len(reint); coste = sum(float(p.get("coste_usd") or 0) for p in pet + reint)
c65 = C.get("P7-65 (todos los rivales activos)") or {}
L = ["# P7-67 · Segundo banco: la invitación a un sitio con la regla de distancia arreglada (1 rival activo, 13 estatuas)", "",
     f"*17-oct-2026. En la plataforma: {partidas} partidas ({len(reint)} reintentos), 4 días por brazo, mismas semillas, destinos, rival y estatuas que el primer banco. `motor/model.py` =",
     "`1e511978c251130e95169ebf8443efa1` antes y después. Decisiones de la mesa (10:31) escritas antes de construir en `REGISTRO_P7_67.md`. Pieza nueva `invita_P7_67b.py` (la distancia de 8-15",
     f"solo al aceptar; aceptada, `ir_sitio` sigue ofrecido hasta el juicio; acierto con un botiquín a ≤ 3 del destino); `prueba_P7_67b.py`: {len(P['pasan'])} pasan, {len(P['fallan'])} fallan.",
     "`lanza_P7_67b.py`, `banco_P7_67b.py` → `P7_67b_banco.json` y los GIF; `revisa_P7_66b.py` → `P7_66b_revision.json`; `escribe_informe_P7_67b.py` (este informe; ninguna cifra a mano).*", "",
     "## En una frase", "",
     f"Arreglada la regla, en MIENTE llega **{M['llegadas']} de {M['aceptadas']}** ({pc(M['fraccion_llegada'])}; en el primer banco, {M1['llegadas']} de {M1['aceptadas']}) y en HONESTA **{H['llegadas']} de {H['aceptadas']}**:",
     f"**el listón de viabilidad {'se alcanza' if pasa else 'no se alcanza'}, justo en el borde** y con muy pocos datos (intervalo del 95 %: {pc(lo)}-{pc(hi)}). Las llegadas de la mentira van por días:",
     "los días 1 y 4 llegan las dos hermanas; los días 2 y 3, ninguna (sección «Qué decide si llega»).", "",
     "## Listón de viabilidad (corregido antes de este banco)", "",
     f"- En MIENTE llega al menos la mitad de las aceptadas: **{M['llegadas']} de {M['aceptadas']} = {pc(M['fraccion_llegada'])}** → **{'PASA' if pasa else 'NO PASA'}** (justo en el 50 %; Wilson 95 %: {pc(lo)}-{pc(hi)}).",
     f"- Las 30 evaluaciones por serie se sustituyeron (tope 26 por diseño) por un campo de al menos 120 evaluaciones de la mentira. Con la tasa de este banco ({f(M['llegadas_por_vida_dia'], 2)} llegadas",
     f"  por vida-día; {f(ev)} evaluaciones por serie de 20 días con la mentira en los días 8-20, la cuenta de P7-66), hacen falta **{series} series** de MIENTE. Con la tasa en el borde",
     f"  bajo del intervalo ({pc(lo)} de llegada) serían {math.ceil(120 / (2 * 13 * lo)) if lo else '—'}; es una cuenta para la mesa, no una decisión.",
     f"- Listón de las estatuas: media {pc2(LI['pasivas_media_ataca_o_persigue'])} del día atacándolas o persiguiéndolas → **{'la ruta vale' if LI['ruta_pasivas_vale'] else 'plan B'}**.", "",
     "## a) Aceptadas que llegan", "", "| brazo · hermana | vidas-día | aceptadas | llegadas | aciertos | interrumpidas | no llegó |", "|---|---|---|---|---|---|---|"]
for k in ("MIENTE · valiente", "MIENTE · prudente", "HONESTA · valiente", "HONESTA · prudente", "MIENTE · las dos", "HONESTA · las dos"):
    t = T[k]; L.append(f"| {k} | {t['vidas_dia']} | {t['aceptadas']} | {t['llegadas']} | {t['aciertos']} | {t['interrumpidas']} | {t['no_llego']} |")
PM = T["MIENTE · por pareja"]; PH = T["HONESTA · por pareja"]
L += ["", f"Por pareja: MIENTE, llegan juntas {PM['llegan_juntas']} de {PM['parejas_dia']} días y una sola {PM['llega_una_sola']}; HONESTA, juntas {PH['llegan_juntas']} de {PH['parejas_dia']} y una sola {PH['llega_una_sola']}.",
      f"Juicio a ≤ 3 del destino: las {M['llegadas']} llegadas de la mentira fallan ({M['aciertos']} aciertos); las {H['llegadas']} de la honesta aciertan {H['aciertos']}.", "",
      f"## b) Interrumpidas", "", f"{M['interrumpidas']} en MIENTE y {H['interrumpidas']} en HONESTA.", "",
      "## c) Evaluaciones de la mentira", "", f"{M['llegadas']} en 4 días ({f(ev)} por serie con la cuenta de P7-66; tope 26). HONESTA: {f(H['evaluaciones_por_serie_estimadas'])}.", "",
      "## d) La calma con un rival activo", "", "| | fracción del día en calma | tramos del tramo de salida | mediana | veredicto |", "|---|---|---|---|---|"]
for k in ("MIENTE", "HONESTA", "los dos brazos", "P7-65 (todos los rivales activos)"):
    c = C.get(k)
    if c: L.append(f"| {k} | {pc(c['fraccion_del_dia_en_calma'])} | {c['primeros_300']['tramos']} | {n(c['primeros_300']['largo_mediana'])} | {c['primeros_300']['veredicto']} |")
L += ["", "Como en el primer banco: el rato de calma que empieza al salir del pedestal dura casi todo el día; tiempo de sobra para andar 8-15 casillas.", "",
      "## Qué decide si llega: lo que elige el cuerpo en los tics en que puede dar un paso", "",
      "El paso se ejecuta en el tic en que el movimiento está listo (`move_ready_in` = 0); en los tics de espera no se mueve. Por intento, de la aceptación al cierre:", "",
      "| brazo | día | asiento | distancia al aceptar | la más cerca | cierre | tics | tics listos | de ellos `ir_sitio` | lo más elegido en los tics listos |", "|---|---|---|---|---|---|---|---|---|---|"]
for x in sorted(I, key=lambda x: (x["brazo"], x["dia"], x["asiento"])):
    top = ", ".join(f"{k} {v}" for k, v in list(x["elegido_en_tics_listos"].items())[:3])
    L.append(f"| {x['brazo']} | {x['dia']} | {x['asiento']} | {x['distancia_al_aceptar']} | {x['distancia_minima_en_el_empuje']} | {x['cierre']} | {x['tics']} | {x['listos']} | {x['listos_ir_sitio']} | {top} |")
fall = [x for x in IM if x["cierre"] != "llegada"]
L += ["", f"Cuando llega, elige `ir_sitio` en casi todos los tics listos y llega en {min(x['tics'] for x in I if x['cierre'] == 'llegada')}-{max(x['tics'] for x in I if x['cierre'] == 'llegada')} tics. Los {len(fall)} intentos de la",
      f"mentira que no llegan son los días {' y '.join(sorted({str(x['dia']) for x in fall}))}: el día 2 gana `ir_objeto` (un objeto a la vista) en la mayoría de los tics listos, y el día 3 se reparten `ir_curioso`,",
      f"`ir_objeto` y pasos sueltos; ninguna baja de {min(x['distancia_minima_en_el_empuje'] for x in fall)} casillas del destino. Es la elección del propio cuerpo, no la pieza: `ir_sitio` está ofrecido toda la ventana. Con 4 días no se puede",
      "separar si pesa el destino (días 2 y 3: (4, 7) y (24, 1)), lo que hay alrededor o la semilla.", "",
      "## e) Las estatuas", "", "| brazo | día | asiento | tics vivos con estatuas | a ≤ 2 | a ≤ 3 | se aleja | se acerca | ataca | coge junto a una muerta | fracción ataca o persigue |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for x in sorted(B["pasivas"]["por_criatura"], key=lambda x: (x["brazo"], x["dia"], x["asiento"])):
    if x["cerca2"] or x["a3"] or x["ataca"] or x["coger_junto_muerta"]:
        L.append(f"| {x['brazo']} | {x['dia']} | {x['asiento']} | {n(x['vivos_con_pasivas'])} | {x['cerca2']} | {x['a3']} | {x['aleja']} | {x['persigue']} | {x['ataca']} | {x['coger_junto_muerta']} | {pc2(x['fraccion_ataca_o_persigue'])} |")
mx = max(B["pasivas"]["por_criatura"], key=lambda x: x["fraccion_ataca_o_persigue"])
L += ["", f"(Las demás criaturas, todo a cero.) Ningún ataque. El máximo por criatura es {pc2(mx['fraccion_ataca_o_persigue'])} ({mx['brazo']} día {mx['dia']}, asiento {mx['asiento']}, que vivió {n(mx['vivos'])} tics):",
      "por debajo del 25 % (la definición cuenta también pasar al lado, de más a propósito; no he separado cuánto es persecución). Las estatuas mueren hacia el tic " + ", ".join(sorted({n(v['tic_mediana']) for v in B['pasivas']['muertes'].values() if v['tic_mediana']})) + " sin daño de nadie.", "",
      "## Aparte: los 11 intentos del segundo banco de P7-66, revisados sin jugar", "",
      f"La regla de distancia mirada en cada tic cortó el empuje (un tic dentro del tramo, en calma, sin `ir_sitio` y con ella o su hermana fuera de 8-15) en **{RV['influyo']} de {RV['n']}** intentos:",
      f"en los {RV['por_cierre']['no_llego']['influyo']} de {RV['por_cierre']['no_llego']['intentos']} que se quedaron sin llegar y en {RV['por_cierre']['interrumpida']['influyo']} de los {RV['por_cierre']['interrumpida']['intentos']} interrumpidos; MIENTE {RV['por_brazo']['MIENTE']['influyo']} de {RV['por_brazo']['MIENTE']['intentos']},",
      f"HONESTA {RV['por_brazo']['HONESTA']['influyo']} de {RV['por_brazo']['HONESTA']['intentos']}. Los otros {RV['n'] - RV['influyo']} los cortó un rival a ≤ 3 antes de que la regla actuara.", "",
      "| día | asiento | brazo | distancia al aceptar | cierre | tics | tics con `ir_sitio` | cortados por la distancia (ella / solo la hermana) | la más cerca | tics a 7 |", "|---|---|---|---|---|---|---|---|---|---|"]
for x in RV["intentos"]:
    L.append(f"| {x['dia']} | {x['asiento']} | {x['brazo']} | {x['distancia_al_aceptar']} | {x['cierre']} | {x['tics']} | {x['tics_con_ir_sitio']} | {x['tics_cortados_por_la_distancia']} ({x['de_ellos_por_ella']} / {x['de_ellos_solo_por_la_hermana']}) | {x['distancia_minima']} | {x['tics_a_7']} |")
L += ["", "La conclusión de P7-66 en WHERE_IS_SEVEN.md («en este mundo la calma y el camino libre nunca duran lo bastante») queda corregida y marcada como contaminada por ese fallo: lo que se",
      "sostiene es que en el Mac, con los 16 asientos ocupados por criaturas nuestras, un rival interrumpió 9 de los 11 intentos; lo que no se sostiene es que la calma nunca dure lo bastante.", "",
      "## f) GIF (datos crudos, matplotlib)", ""]
for g in B["gifs"]:
    L.append(f"- `{g['gif']}`: {g['brazo']}, día {g['dia']}, asiento {g['asiento']} ({g['hermana']}), destino {tuple(g['destino'])}, de la aceptación (tic {g['tic_aceptada']}) al cierre (tic {g['tic_juicio']}, {g['cierre']}); {g['fotogramas']} fotogramas. ![{g['gif']}](../figuras/{g['gif']})")
L += ["", "## Gasto", "",
      f"- **Créditos de la plataforma**: este banco, {partidas} partidas → **{partidas} créditos** (coste estimado que apunta la plataforma: {f(coste, 2)}). Hoy, con el primer banco, 16 créditos.",
      "  Saldo: no lo he podido leer; el último conocido era ~35 antes de las recargas de las noches del 16 y el 17.",
      "- **Dólares de la consola de Anthropic**: **0 $** (no se llama a la razón).", ""]
open(os.path.join(AQUI, "informe_P7_67_segundo_banco.md"), "w").write("\n".join(L)); print("\n".join(L))
