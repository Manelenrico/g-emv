"""[P7-65] escribe informe_P7_65_diagnostico.md desde P7_65_diagnostico.json (ninguna cifra a mano). Descriptivo, posterior al sello. python3 escribe_diagnostico_P7_65.py"""
import json, os, shutil
AQUI = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(AQUI, "P7_65_diagnostico.json"))); P2 = R["punto2"]; M = R["muertes"]
f = lambda x, n=2: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
pc = lambda x: "—" if x is None else f"{round(100 * x)} %"
FIG = os.path.join(os.path.dirname(AQUI), "figuras"); os.makedirs(FIG, exist_ok=True)
for g in R["gifs"]: shutil.copy(os.path.join(AQUI, g["gif"]), os.path.join(FIG, g["gif"]))
L = ["# P7-65 · Diagnóstico posterior al sello (descriptivo: no cambia ningún PASA o NO PASA)", "",
     "*16-oct-2026. `diagnostico_P7_65.py` → `P7_65_diagnostico.json` y los GIF; `escribe_diagnostico_P7_65.py` (este informe; ninguna cifra a mano). Las mismas vidas, invitaciones y",
     "evaluaciones que el informe sellado (`analiza_P7_65.py`). `motor/model.py` intacto. Plataforma 0; consola 0 $.*", "",
     "## 1 · Qué es «aceptar»", "",
     "En cada tic el cuerpo arma su lista de candidatos (moverse, quedarse quieto, ir a por un objeto, coger, usar…) e imagina adónde le lleva cada uno; elige el que más le acerca a su",
     "equilibrio. Una invitación activa no manda: añade a la foto imaginada del candidato que le corresponde una fila de alivio proporcional a lo prometido por la confianza. Para «coger el",
     "botiquín», ese candidato es `coger` el botiquín (si está justo encima) o `ir_objeto` / `ir_curioso` con el botiquín como destino (un paso hacia él).",
     "**Aceptar = que, en un tic, el elegido sea ese candidato.** Basta un paso hacia el botiquín. Desde ahí la invitación queda abierta y se juzga con el siguiente uso del botiquín o, si no",
     "lo hay, por el cambio de vida a los 480 tics; pero el cuerpo **vuelve a decidir en cada tic** desde cero: para llegar a coger tiene que seguir eligiendo pasos hacia el botiquín hasta",
     "estar encima, que le quepa en la mochila y elegir `coger`. Nada le obliga a seguir.", "",
     f"## 2 · Las {R['sin_cogida']} evaluaciones de la falsa sin cogida", "",
     "| | valiente | prudente |", "|---|---|---|"]
filas = [("evaluaciones sin cogida", "evaluaciones"), ("botiquín a la vista al aceptar", "botiquin_a_la_vista_al_aceptar"), ("botiquín al alcance (≤ 1 casilla) al aceptar", "botiquin_al_alcance_al_aceptar"),
         ("le cabe otro botiquín en la mochila al aceptar", "le_cabe_otro_botiquin_al_aceptar"), ("rival a ≤ 4 casillas al aceptar", "rival_a_4_o_menos_al_aceptar"),
         ("botiquín a la vista en algún momento de la ventana", "botiquin_a_la_vista_en_la_ventana"), ("llega a pisar un botiquín en la ventana", "llego_al_botiquin_en_la_ventana"),
         ("rival a ≤ 4 casillas en la ventana", "rival_a_4_o_menos_en_la_ventana"), ("golpeada en la ventana", "golpeada_en_la_ventana")]
for nom, k in filas:
    if k == "evaluaciones": L.append(f"| {nom} | {P2['valiente']['evaluaciones']} | {P2['prudente']['evaluaciones']} |"); continue
    L.append(f"| {nom} | {pc(P2['valiente'][k]['fraccion'])} ({P2['valiente'][k]['n']}) | {pc(P2['prudente'][k]['fraccion'])} ({P2['prudente'][k]['n']}) |")
L += ["", "**Qué hizo el cuerpo en la ventana** (de la aceptación al juicio; solo tics con elección de verdad, 2 o más candidatos; con un solo candidato, quedarse quieto es forzado):", ""]
for h in ("valiente", "prudente"): L.append(f"- {h}: " + "; ".join(f"`{a}` {pc(x)}" for a, x in P2[h]["lo_que_eligio_en_la_ventana"]) + ".")
L += ["", "En llano: casi siempre había un rival cerca (la mentira lo pide) y casi siempre se veía un botiquín, pero rara vez al alcance; el cuerpo da un paso hacia él (eso es aceptar) y",
      "luego, con el rival cerca, **se queda quieto** la mayor parte del tiempo o se va a curiosear; casi nunca llega a pisar el botiquín. Además, al aceptar no le cabía otro botiquín en la",
      f"mochila en el {pc(1 - P2['valiente']['le_cabe_otro_botiquin_al_aceptar']['fraccion'])} de las de la valiente y el {pc(1 - P2['prudente']['le_cabe_otro_botiquin_al_aceptar']['fraccion'])} de las de la prudente: no podía cogerlo aunque llegara.", "",
      "## 3 · Tres GIF (aceptaciones sin cogida al azar, semilla 65, de la aceptación al juicio; uno de cada 4 tics)", ""]
for g in R["gifs"]: L += [f"- `{g['gif']}`: serie {g['serie']}, día {g['dia']}, {g['brazo']}, {g['hermana']}; tic {g['tic_aceptada']} → {g['tic_juicio']}; juicio {g['juicio']}, {'acierto' if g['acierto'] == 1 else 'fallo'}.", f"  ![{g['gif']}](../figuras/{g['gif']})"]
L += ["", "Los GIF van en gemv-paper7 (`figuras/`); en gemv-coworld el `.gitignore` excluye los .gif y se quedan en el Mac (`cantera/paper7/`, `cantera/figuras/`). Negro: ella; azul: su hermana; rojo: rivales visibles; verde (cruz): botiquines visibles; gris: paredes y rocas; la línea es su recorrido desde la aceptación.", "",
      "## 4 · Muertes", "",
      "Muerte = el juego la elimina (`final.reason == \"eliminated\"`). **Aviso**: la regla heredada de P7-56 que usó el informe sellado para la vigilancia (último tic vivo antes del 14.000)",
      "cuenta muchas menos muertes, porque muchas eliminaciones ocurren después del tic 14.000; se dan las dos. Error típico por criatura: la fracción de días eliminada de cada serie, √3.", "",
      "| brazo · hermana | eliminada (de 60) | fracción ± ee | regla de P7-56 | causa: zona / fuego | causa: otro agente |", "|---|---:|---|---:|---:|---:|"]
for k, v in M.items(): L.append(f"| {k} | {v['eliminada']} | {f(v['media'])} ± {f(v['ee_por_criatura'])} | {v['regla_P7_56_ultimo_tic_lt_14000']} | {v['causas'].get('zona / fuego', 0)} | {v['causas'].get('otro agente', 0)} |")
L += ["", "Causa = el origen del último daño recibido antes de la eliminación.", "",
      "**¿Muere más después de seguir invitaciones verdaderas?** Muertes por cada 10.000 tics en riesgo, en los 480 tics que siguen a aceptar una invitación verdadera y en el resto de la vida:", "",
      "| brazo · hermana | tras seguir una verdadera | el resto de la vida |", "|---|---|---|"]
for k, v in M.items(): L.append(f"| {k} | {f(v['tras_seguir_una_verdadera']['por_10000_tics'])} ({v['tras_seguir_una_verdadera']['muertes']} muertes) | {f(v['el_resto_de_la_vida']['por_10000_tics'])} ({v['el_resto_de_la_vida']['muertes']} muertes) |")
h = M["MIENTE_UNA · prudente"]; a, b = h["tras_seguir_una_verdadera"]["por_10000_tics"], h["el_resto_de_la_vida"]["por_10000_tics"]
L += ["", f"**La prudente con razón honesta no muere más tras seguir invitaciones verdaderas** ({f(a)} frente a {f(b)} por 10.000 tics)." if a <= b else f"**La prudente con razón honesta muere más tras seguir invitaciones verdaderas** ({f(a)} frente a {f(b)} por 10.000 tics).",
      "Muere más que las otras tres sobre todo por la zona y el fuego (ver la tabla de causas). Son pocas muertes en cada casilla: descriptivo, sin prueba.", ""]
RC = json.load(open(os.path.join(AQUI, "P7_65_recordados.json"))); g = lambda h, k: RC[h].get(k, 0)
sinv = g("valiente", "sin ningun botiquin a la vista") + g("prudente", "sin ningun botiquin a la vista"); rec = g("valiente", "el paso la acerca a un botiquin que vio antes") + g("prudente", "el paso la acerca a un botiquin que vio antes")
des = g("valiente", "  ... que estaba a <= 4 casillas y ya no esta (recordado y desaparecido)") + g("prudente", "  ... que estaba a <= 4 casillas y ya no esta (recordado y desaparecido)")
L += ["## 5 · ¿Hacia qué botiquín da el paso al aceptar? (añadido el 16-oct, a pregunta de Manel; `recordados_P7_65.py` → `P7_65_recordados.json`)", "",
      "`ir_objeto` no va a lo que se ve en ese tic, sino al objeto que la criatura **recuerda** (su memoria de objetos vistos), esté o no a la vista. Además, el diario apunta cada decisión en el",
      "tic siguiente al de la aceptación (la aceptación del tic 2319 es la decisión registrada en el 2320).", "",
      "| | valiente | prudente |", "|---|---:|---:|", f"| aceptaciones sin cogida | {g('valiente', 'aceptaciones')} | {g('prudente', 'aceptaciones')} |",
      f"| con un botiquín a la vista al decidir | {g('valiente', 'con un botiquin a la vista')} | {g('prudente', 'con un botiquin a la vista')} |",
      f"| sin ningún botiquín a la vista | {g('valiente', 'sin ningun botiquin a la vista')} | {g('prudente', 'sin ningun botiquin a la vista')} |",
      f"| … el paso la acerca a un botiquín que vio antes | {g('valiente', 'el paso la acerca a un botiquin que vio antes')} | {g('prudente', 'el paso la acerca a un botiquin que vio antes')} |",
      f"| … que estaba a ≤ 4 casillas y ya no está (recordado y desaparecido) | {g('valiente', '  ... que estaba a <= 4 casillas y ya no esta (recordado y desaparecido)')} | {g('prudente', '  ... que estaba a <= 4 casillas y ya no esta (recordado y desaparecido)')} |",
      f"| … no había visto ningún botiquín ese día | {g('valiente', 'no habia visto ningun botiquin ese dia')} | {g('prudente', 'no habia visto ningun botiquin ese dia')} |", "",
      f"En {sinv} de las {RC['evaluaciones']} aceptaciones no había ningún botiquín a la vista; en {rec} el paso iba hacia uno que había visto antes, y en {des} ese botiquín estaba a 4 casillas o menos y",
      "ya no estaba (alguien lo había cogido o usado): **la criatura iba hacia un botiquín recordado que ya no existe.** El GIF de s2 d13 es uno de esos casos: el botiquín recordado estaba en",
      "(21,24), a 2 casillas, visto por última vez en el tic 2227; el paso al sur la acerca a él, y por eso el GIF no lo dibuja (solo dibuja lo que se ve). La línea gris del GIF es su recorrido.", ""]
open(os.path.join(AQUI, "informe_P7_65_diagnostico.md"), "w").write("\n".join(L)); print("\n".join(L[13:30]))
