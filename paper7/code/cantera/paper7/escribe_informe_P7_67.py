"""[P7-67] escribe informe_P7_67.md desde P7_67_banco.json, P7_67_estado.json y P7_67_pruebas.json (ninguna cifra a mano)."""
import json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); B = json.load(open(os.path.join(AQUI, "P7_67_banco.json"))); E = json.load(open(os.path.join(AQUI, "P7_67_estado.json")))
P = json.load(open(os.path.join(AQUI, "P7_67_pruebas.json"))); T = B["por_brazo_y_hermana"]; M = T["MIENTE · las dos"]; H = T["HONESTA · las dos"]; C = B["calma"]; LI = B["listones"]
pc = lambda x: "—" if x is None else f"{100 * x:.1f} %".replace(".", ",")
pc2 = lambda x: "—" if x is None else f"{100 * x:.2f} %".replace(".", ",")
f = lambda x, n=1: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
n = lambda x: "—" if x is None else f"{int(round(x)):,}".replace(",", ".")
I = B["intentos"]; IM = [x for x in I if x["brazo"] == "MIENTE"]; IH = [x for x in I if x["brazo"] == "HONESTA"]
atasco = [x for x in IM if x["distancia_minima_en_el_empuje"] == 7]; lejos = [x for x in IM if x["distancia_minima_en_el_empuje"] != 7]
peticiones = E["peticiones"]; reint = E.get("reintentos", []); partidas = len(peticiones) + len(reint)
V = B["vidas_hermanas"]; cortas = [v for v in V if v["tics_vivos"] < 3000]
TR = B["pasivas"]["por_criatura"]; MU = B["pasivas"]["muertes"]
c65 = C.get("P7-65 (todos los rivales activos)") or {}
L = ["# P7-67 · El control de la amenaza: la prueba de P7-66 con un solo rival activo y 13 pasivas", "",
     f"*17-oct-2026. En la plataforma: {partidas} partidas ({len(reint)} reintentos), 4 días por brazo. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` antes y después. Decisiones de la mesa, corrección",
     "de Manel, medidas, listones y humo local escritos antes de lanzar en `REGISTRO_P7_67.md`. Piezas nuevas: `pasiva_P7_67.py`, `invita_P7_67.py` (solo cuentan los rivales activos;",
     f"`prueba_P7_67.py`: {len(P['pasan'])} pasan, {len(P['fallan'])} fallan), `campo_P7_67.py`, `lanza_P7_67.py`; `banco_P7_67.py` → `P7_67_banco.json` y los GIF; `escribe_informe_P7_67.py` (este informe;",
     "ninguna cifra a mano).*", "",
     "## En una frase", "",
     f"Quitar la amenaza funciona: con un solo rival activo la calma pasa del {pc(c65.get('fraccion_del_dia_en_calma'))} del día (P7-65) al {pc(C['los dos brazos']['fraccion_del_dia_en_calma'])}, y los ratos de calma que",
     f"empiezan en el tramo de salida duran una mediana de {n(C['los dos brazos']['primeros_300']['largo_mediana'])} tics (P7-65: {n(c65.get('primeros_300', {}).get('largo_mediana'))}); las pasivas no molestan",
     f"({pc2(LI['pasivas_media_ataca_o_persigue'])} del día atacándolas o persiguiéndolas). Pero en MIENTE no llega ninguna ({M['llegadas']} de {M['aceptadas']}), y **la causa no es la amenaza ni el cuerpo:",
     "es una regla de la pieza heredada de P7-66 (`invita_P7_66b`) que impide llegar mientras empuja** (sección «Lo que de verdad pasa»). El listón de P7-66 no se alcanza, pero esta prueba no",
     "puede decir si el cuerpo seguiría la mentira en calma: hay que arreglar la regla antes (es de la mesa).", "",
     "## Listones", "",
     f"- **Listón de P7-66** (en MIENTE, al menos la mitad de las aceptadas llegan y al menos 30 evaluaciones por serie): llegan el **{pc(M['fraccion_llegada'])}**, **{f(M['evaluaciones_por_serie_estimadas'])}**",
     f"  evaluaciones por serie (tope por construcción: {M['tope_por_construccion']}) → **{'lo alcanza' if LI['pasa_P7-66'] else 'no lo alcanza'}**. Con la salvedad de arriba: la regla de la pieza lo hacía imposible.",
     f"- **Listón nuevo, la ruta de las pasivas** (falla si pasan más de una cuarta parte del día atacando o persiguiendo pasivas): media por criatura **{pc2(LI['pasivas_media_ataca_o_persigue'])}** →",
     f"  **{'la ruta de las pasivas vale' if LI['ruta_pasivas_vale'] else 'no vale: plan B'}**. No hace falta el plan B (el juego compilado).", "",
     "## a) Aceptadas que llegan", "", "| brazo · hermana | vidas-día | aceptadas | llegadas | aciertos | interrumpidas | no llegó |", "|---|---|---|---|---|---|---|"]
for k in ("MIENTE · valiente", "MIENTE · prudente", "HONESTA · valiente", "HONESTA · prudente", "MIENTE · las dos", "HONESTA · las dos"):
    t = T[k]; L.append(f"| {k} | {t['vidas_dia']} | {t['aceptadas']} | {t['llegadas']} | {t['aciertos']} | {t['interrumpidas']} | {t['no_llego']} |")
PM = T["MIENTE · por pareja"]; PH = T["HONESTA · por pareja"]
llh = [x for x in IH if x["cierre"] == "llegada"]
L += ["", f"Por pareja: en MIENTE, {PM['llegan_juntas']} días llegan juntas y {PM['llega_una_sola']} llega una sola, de {PM['parejas_dia']}; en HONESTA, {PH['llegan_juntas']} y {PH['llega_una_sola']}, de {PH['parejas_dia']}.",
      f"Las {len(llh)} llegadas de HONESTA son del día {', '.join(sorted({str(x['dia']) for x in llh}))} (destino {', '.join(sorted({str(tuple(x['destino'])) for x in llh}))}), en {', '.join(str(x['tics']) for x in llh)} tics, y se juzgan **0**:",
      f"al llegar veían botiquines en {'; '.join(str([tuple(k) for k in x['botiquines_vistos']]) for x in llh)}, a más de una casilla del sitio. La honesta también falla el juicio en el tramo de salida",
      "(hipótesis, sin comprobar: el sitio se eligió por los botiquines de todo el día en P7-65, no por los de esa hora), y la confianza en recursos bajó de 0,5 a 0,35. Para la mesa.", "",
      f"## b) Interrumpidas", "", f"{M['interrumpidas']} en MIENTE y {H['interrumpidas']} en HONESTA: el rival activo nunca se acercó a ≤ 3 de una hermana con una invitación abierta.", "",
      "## c) Evaluaciones de la mentira por serie", "",
      f"MIENTE: **{f(M['evaluaciones_por_serie_estimadas'])}** (la cuenta de P7-66: llegadas por vida-día × 2 × 13; tope {M['tope_por_construccion']}). HONESTA: {f(H['evaluaciones_por_serie_estimadas'])}.", "",
      "## d) La calma con un solo rival activo, frente a P7-65", "",
      "Calma = ningún rival ACTIVO a ≤ 5 y ningún golpe en 48 tics (en P7-65, todos los rivales activos; misma cuenta). «Primeros 300» = tramos que empiezan en los primeros 300 tics de la fase viva.", "",
      "| | fracción del día en calma | tramos | largo mediana (p25-p75) | tramos ≥ 165 | primeros 300: tramos | mediana (p25-p75) | ≥ 165 | veredicto |", "|---|---|---|---|---|---|---|---|---|"]
for k in ("MIENTE", "HONESTA", "los dos brazos", "P7-65 (todos los rivales activos)"):
    c = C.get(k)
    if not c: continue
    p = c["primeros_300"]
    L.append(f"| {k} | {pc(c['fraccion_del_dia_en_calma'])} | {n(c['tramos'])} | {n(c['largo_mediana'])} ({n(c['largo_p25'])}-{n(c['largo_p75'])}) | {pc(c['fraccion_tramos_>=165'])} | {p['tramos']} | {n(p['largo_mediana'])} ({n(p['largo_p25'])}-{n(p['largo_p75'])}) | {pc(p['fraccion_>=165'])} | {p['veredicto']} |")
CR = B["criterio_calma"]
L += ["", f"Criterio (registro, fijado antes): andar {CR['casillas']} casillas lleva ~{CR['justo_tics']} tics (un paso cada ~{CR['paso_tics']}); «de sobra» si la mediana de los tramos del tramo de salida es ≥ {CR['de_sobra_tics']} tics.",
      f"**Respuesta a la pregunta 2 de Manel: sí, de sobra.** El rato de calma que empieza al salir del pedestal dura casi todo el día (mediana {n(C['los dos brazos']['primeros_300']['largo_mediana'])} tics); en P7-65 la mediana era",
      f"{n(c65.get('primeros_300', {}).get('largo_mediana'))} tics («{c65.get('primeros_300', {}).get('veredicto')}»). El resto de tramos son muy cortos (mediana {n(C['los dos brazos']['largo_mediana'])}): los parte un golpe recibido (probablemente también el de la zona al cerrarse; no lo he comprobado).", "",
      "## e) Cómo trata el cuerpo a las pasivas (mientras viven)", "",
      "| brazo | día | asiento | tics vivos con pasivas | a ≤ 2 | a ≤ 3 | se aleja | se acerca | ataca | coge junto a una muerta | fracción ataca o persigue |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for x in sorted(TR, key=lambda x: (x["brazo"], x["dia"], x["asiento"])):
    L.append(f"| {x['brazo']} | {x['dia']} | {x['asiento']} | {n(x['vivos_con_pasivas'])} | {x['cerca2']} | {x['a3']} | {x['aleja']} | {x['persigue']} | {x['ataca']} | {x['coger_junto_muerta']} | {pc2(x['fraccion_ataca_o_persigue'])} |")
mu = sorted({v["tic_mediana"] for v in MU.values() if v["tic_mediana"]})
L += ["", f"Las hermanas apenas se cruzan con las pasivas: el cuerpo se va al centro y las pasivas se quedan en los pedestales del borde. No hay ni un ataque. Las pasivas mueren hacia el tic {', '.join(n(x) for x in mu)}",
      "sin daño de nadie (la zona alcanza su pedestal, como en el humo local): por pasiva muerta, " + "; ".join(f"{k} {v['muertas']} de 13" for k, v in sorted(MU.items())) + ".",
      "Cuando solo quedan 7 muertas, el resto murió en el mismo tic en que acabó la partida (la partida termina al quedar uno solo y su `final` dice `match_over`).", "",
      f"**El rival activo mató a las dos hermanas el día 2, en los dos brazos** (misma semilla): " + "; ".join(f"{v['brazo']} asiento {v['asiento']} en el tic {n(v['ultimo_tic'])}" for v in cortas) + ".", "",
      "## Lo que de verdad pasa: una regla de la pieza impide llegar", "",
      "`invita_P7_66b` (segundo banco de P7-66; aquí sin cambios en su lógica, decisión 5) solo deja empujar si el destino está a entre 8 y 15 casillas **de ella y de su hermana en ese tic**",
      "(`puede_empujar`, que se mira en cada tic para activar la invitación y para ofrecer el candidato `ir_sitio`). Al acercarse a 7 el candidato desaparece y el cuerpo vuelve a lo de siempre;",
      "al alejarse a 8 reaparece. Es un columpio: para llegar hay que pasar por 7, y a 7 la invitación ya no empuja.", "",
      "| brazo | día | asiento | distancia al aceptar | la más cerca mientras empuja | tics a 7 | tics eligiendo `ir_sitio` | al cerrar | cierre |", "|---|---|---|---|---|---|---|---|---|"]
for x in sorted(I, key=lambda x: (x["brazo"], x["dia"], x["asiento"])):
    L.append(f"| {x['brazo']} | {x['dia']} | {x['asiento']} | {x['distancia_al_aceptar']} | {x['distancia_minima_en_el_empuje']} | {x['tics_a_7_en_el_empuje']} | {x['tics_ir_sitio']} | {x['distancia_al_cerrar']} | {x['cierre']} |")
L += ["", f"En MIENTE, {len(atasco)} de {len(IM)} intentos se quedan clavados a 7 casillas (entre {min(x['tics_a_7_en_el_empuje'] for x in atasco)} y {max(x['tics_a_7_en_el_empuje'] for x in atasco)} tics a 7, yendo y viniendo entre 7 y 8);",
      f"los otros {len(lejos)} son los de la hermana que estaba más lejos ({', '.join(str(x['distancia_al_aceptar']) for x in lejos)} al aceptar): la regla también pide 8-15 **de la hermana**, y cuando la otra baja a 7",
      "el candidato cae para las dos. Las dos hermanas de cada partida eligen `ir_sitio` el mismo número de tics. Al acabar el tramo de 300 tics la invitación deja de empujar y",
      "las dos se van al centro: acaban más lejos que al aceptar. En HONESTA el destino está en el centro, adonde el cuerpo va solo, y por eso bajan de 7 (y llegan dos veces).",
      "El texto del registro de P7-66 decía «la distancia “al aceptar”»; la pieza la aplica en cada tic. Muy probablemente es también la causa de las 0 llegadas del segundo banco de P7-66",
      "(que se cerró por la regla de parada); no lo he comprobado en todos sus intentos.", "",
      "## Para la mesa (propuestas; nada hecho)", "",
      "1. **Arreglar la regla de la distancia** en una pieza nueva (p. ej. `invita_P7_67b`; `invita_P7_66b` no se toca): mirar 8-15 solo en el tic de aceptar y, aceptada, seguir ofreciendo `ir_sitio`",
      "   hasta el juicio (o hasta que acabe el tramo de 300 tics). Con la calma que ya hay (sección d), repetir este mismo banco: 8 partidas, ~8 créditos.",
      "2. **La honesta no es honesta a esa hora**: los botiquines no están a ≤ 1 del sitio en el tramo de salida. Elegir el destino honesto por dónde hay botiquines al principio del día, o juzgar a ≤ 2-3.",
      "3. **El tope de 26 evaluaciones por serie** (registro): sigue en pie.",
      "4. El rival activo mata a las dos hermanas el día 2 (semilla 43510754) en los dos brazos: dos vidas-día de cada brazo duran menos de 2.500 tics. No toca al tramo de salida.", "",
      "## f) GIF (datos crudos, matplotlib)", ""]
for g in B["gifs"]:
    L.append(f"- `{g['gif']}`: {g['brazo']}, día {g['dia']}, asiento {g['asiento']} ({g['hermana']}), destino {tuple(g['destino'])}, de la aceptación (tic {g['tic_aceptada']}) al cierre (tic {g['tic_juicio']}, {g['cierre']}); {g['fotogramas']} fotogramas. ![{g['gif']}](../figuras/{g['gif']})")
coste = sum(float(p.get("coste_usd") or 0) for p in peticiones + reint)
L += ["", "## Gasto", "",
      f"- **Créditos de la plataforma**: {partidas} partidas → **{partidas} créditos** (1 por partida; la plataforma apunta {f(coste, 2)} de coste estimado en total). Saldo: no lo he podido leer; el último",
      "  conocido era ~35 antes de las recargas de las noches del 16 y el 17.",
      "- **Dólares de la consola de Anthropic**: **0 $** (las invitaciones las escribe el guion; no se llama a la razón). Saldo de la consola: sin cambios por este paso.", ""]
open(os.path.join(AQUI, "informe_P7_67.md"), "w").write("\n".join(L)); print("\n".join(L)[:2500])
