"""[P7-62] escribe informe_P7_62.md desde P7_62_resumen.json y P7_62_lecturas.json (ninguna cifra a mano). python3 escribe_informe_P7_62.py"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(AQUI, "P7_62_resumen.json"))); CO = json.load(open(os.path.join(AQUI, "P7_62_cortes.json"))); LE = json.load(open(os.path.join(AQUI, "P7_62_lecturas.json")))
f = lambda x, n=2: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
P = R["pruebas"]; C = R["coste_estimado"]; LO = R["local"]
ev = [e for v in LO.values() for e in v["evaluadas_62"]]; cort = [e for e in ev if e["fuente"] == "cortada por golpe"]; hue = [e for e in ev if e["fuente"] == "huella (hueco)"]
L = ["# P7-62 · Cancelar la serie 4 de P7-61 y arreglar el juicio de la mentira (nada en plataforma)", "",
     "*14-oct-2026. Piezas nuevas (`juicio_P7_62.py`, `campo_P7_62.py`, `policy_pareja_P7_62.py`, `Dockerfile.pareja_P7_62`); las de P7-56/P7-61 (`invita_P7_54`, `invita_P7_57`, `hermanas_P7_48`) no se",
     "tocan. `prueba_P7_62.py` → `P7_62_pruebas.json`; `local62_P7_62.py` → `P7_62_local.json`; `resumen_P7_62.py` → `P7_62_resumen.json`; `lecturas_P7_62.py` → `P7_62_lecturas.json`;",
     "`escribe_informe_P7_62.py` (este informe; ninguna cifra a mano). `motor/model.py` intacto. Sin sello: lo escribe Manel.*", "",
     "## 1 · La serie 4 cancelada", "",
     "La espera programada para las 02:15 se detuvo antes de pedir nada (0 partidas). **Addendum 7** al sello de P7-61: el campo se detiene tras 3 series porque el juicio implementado no coincide",
     "con el sellado (fallos 1 y 2 del informe intermedio) y el contraste con lo contado no mira la situación (fallo 3, diseño de la mesa); motivo: fallo de medida encontrado al comprobar el",
     "funcionamiento, no el resultado. P7-61 se informa completo tal cual.", "",
     "## 2 · Los arreglos (método de la mesa), en una pieza nueva", "",
     "`juicio_P7_62` (GEMV_P7_62=1) se engancha después de `invita_P7_57` y antes de `rapido_P7_43`:", "",
     f"- **Regla del mundo** (Ari, 7-oct, zero-sum v0.1.19): el botiquín cura 50 solo tras 2 s de canalización sin recibir daño; cualquier golpe la interrumpe (se puede reintentar, otros 2 s);",
     f"  la ración tarda 1 s y el daño no la interrumpe. La canalización se LEE del catálogo del mundo (`use_ticks`: botiquín {CO['canal']['first_aid']} tics, ración {CO['canal']['rations']}); qué interrumpe el daño es la",
     "  regla de Ari (solo el botiquín, por su id del mundo).",
     "- **(a) Cura cortada por un golpe = fallo, en el momento.** Las invitaciones de cura aceptadas (USAR_BOTIQUIN, USAR_RACION) se le quitan a `invita_P7_54` (que saltaba el uso cortado)",
     "  y las juzga el PRIMER uso de esa cosa empezado tras aceptar: si es un botiquín y hay un golpe dentro de su canalización ([t0, t0 + use_ticks], los golpes apuntados tic a tic), la cura",
     "  se cortó: acierto de cuerpo 0 en ese tic, aunque la huella no lleve marca de corte. La ración no se corta por un golpe. **Declarado**: se aplica a toda invitación de cura, no solo a la",
     "  falsa, porque el cuerpo no puede saber cuál es la falsa. Una marca de corte sin golpe en la canalización no juzga (se espera al siguiente uso, como antes).",
     "- **(b) El hueco.** Sin golpe, acierto si la cura da al menos la mitad de min(promesa, 100 − vida al empezar el uso) (la falsa: min(50, 100 − vida)); si ya estaba entera (hueco < 1),",
     "  acierto si no bajó. **Declarado**: igual para toda invitación de cura (la ración, con su promesa). Sin uso en 480 tics: el cambio de vida, también contra el hueco.",
     "- **(c) Lo contado, solo en su situación.** El contraste de `invita_P7_57` se sustituye por fuera: una invitación con condición de amenaza (la falsa) solo se contrasta con recuerdos de la",
     "  hermana de la MISMA situación. **Para eso la amenaza tiene que viajar con el recuerdo** (antes no viajaba: el recuerdo solo llevaba «golpeado en 48 tics»): se apunta al vivir el uso",
     "  (`contexto.amenaza`, con la definición de la falsa: rival a ≤ 4 o fuego al empezar, o golpe en los 48 tics anteriores), va por el canal en el carácter del golpe del M7 (0-3, mismo",
     "  largo; un M7 de antes se lee sin amenaza) y por la noche se lee del cuaderno de la hermana. **Declarado**: un «visto» no trae la amenaza de la hermana (solo la de quien mira) y no entra",
     "  en el contraste de la falsa; tampoco un recuerdo sin amenaza apuntada. Las invitaciones honestas (sin condición de amenaza) se contrastan como en P7-57.", "",
     f"## 3 · Pruebas con casos construidos a mano (con la regla del mundo): {len(P['pasan'])} pasan, {len(P['fallan'])} fallan", ""]
L += [f"- {x}" for x in P["pasan"]] + [f"- FALLA: {x}" for x in P["fallan"]]
FR = CO["falsa_resumen"]
L += ["", f"**La regla del mundo frente a la marca del cuerpo**, en los {CO['usos']} usos del botiquín de las series 1-3 de P7-61 (`cortes_P7_62.py` → `P7_62_cortes.json`): cortados por las dos {CO['regla_si_marca_si']},",
      f"por ninguna {CO['regla_no_marca_no']}, solo por la regla {CO['regla_si_marca_no']} (golpe en la canalización que la huella no marcó), solo por la marca {CO['regla_no_marca_si']}: coinciden casi siempre.",
      f"**Las {FR['evaluaciones']} evaluaciones de la falsa de P7-61, rejuzgadas con el juicio nuevo** (descriptivo): cortadas por golpe {FR['cortadas_ahora']} (fallo), aciertos {FR['aciertos_ahora']} (antes {FR['aciertos_antes']});",
      f"cambian {FR['cambian']}. Con el juicio arreglado la falsa se confirma MÁS, no menos: fuera de los golpes la cura es de verdad (cura el hueco), y el techo de vida ya no la desmiente;",
      "solo la desmiente un golpe en la canalización. Es lo que la mentira dice que no pasa, y es lo que ahora mide el juicio."]
L += ["", "## 4 · Comprobación local corta en lazo cerrado (3 días, 16 asientos, nuestra imagen; 0 créditos)", "",
      "Repetida tras la regla del mundo (la primera, con el corte por la marca de la huella, queda en `P7_62_local_v1.json`). Como la de P7-57: asientos 10-11 = MIENTEN_DOS, 12-13 = MIENTE_UNA (miente la 12), la mentira desde las invitaciones del día 2 (en el campo, 8), los demás sin razón.", "",
      "| día · asiento | p95 ms | invitaciones (falsas) | juicios de cura de P7-62 (acción · falsa · fuente · hueco · vivido → acierto) | contrastes (con la falsa) · fuera de situación | curas juzgadas por P7-54 | M7 malos |",
      "|---|---:|---|---|---|---:|---:|"]
for k, v in LO.items():
    js = "; ".join(f"{e['accion']} · {'falsa' if e['falsa'] else 'honesta'} · {e['fuente']} · {f(e['hueco'], 0)} · {f(e['vivido'], 0)} → {e['acierto']}" for e in v["evaluadas_62"]) or "—"
    L.append(f"| {k} | {f(v['ms_p95'], 1)} | {v['invitaciones']} ({v['falsas']}) | {js} | {v['contrastes_62']} ({v['contrastes_falsa']}) · {v['fuera_de_situacion']} | {v['curas_juzgadas_por_P7_54']} | {v['mensajes_malos']} |")
amen = [a for v in LO.values() for a in v["amenaza_de_los_recuerdos"]]
L += ["", f"Funciona en lazo cerrado: {len(ev)} juicios de cura los hizo P7-62 ({len(cort)} por golpe → fallo; {len(hue)} por el hueco) y ninguno `invita_P7_54` "
      f"({sum(v['curas_juzgadas_por_P7_54'] for v in LO.values())}); los recuerdos contrastados traen su amenaza ({sum(1 for a in amen if a is True)} en amenaza, {sum(1 for a in amen if a is False)} en calma, "
      f"{sum(1 for a in amen if a is None)} sin apuntar); {sum(v['mensajes_con_amenaza'] for v in LO.values())} M7 salieron con la amenaza y {sum(v['mensajes_malos'] for v in LO.values())} malos; p95 ≤ "
      f"{f(max(v['ms_p95'] for v in LO.values() if v['ms_p95'] is not None), 1)} ms. Razón de la comprobación: {R['local_razon']['llamadas']} llamadas, {f(R['local_razon']['usd'], 2)} $ de consola.", "",
      "## 5 · Coste estimado de un campo de 2 brazos (MIENTEN_DOS, MIENTE_UNA) × 3 series", "",
      f"- **Plataforma**: {C['partidas_campo']} partidas + {C['humo']} de humo + ~{C['reintentos_previstos_como_P7_61']} reintentos (como P7-61) ≈ **{C['creditos_plataforma']} créditos** (1 por partida; alguna cuenta 0);",
      f"  con la recarga de {C['recarga_diaria']} al día, {-(-C['creditos_plataforma'] // C['recarga_diaria'])} recargas.",
      f"- **Consola de Anthropic**: {C['llamadas_razon']} llamadas a la razón (2 brazos × 3 series × 19 noches × 2 hermanas, + 4 del humo) × {f(C['usd_por_llamada_P7_61'], 4)} $ medidos en P7-61 ≈ **{f(C['usd_consola'], 2)} $**.",
      f"- **Tiempo**: {', '.join(f(h, 1) for h in C['horas_por_serie_P7_61'])} horas por serie en P7-61 (la 1 con el humo) ≈ {f(C['horas_campo'], 1)} horas de juego, una serie detrás de otra.", "",
      "## 6 · Lecturas extra sin coste sobre las series 1-3 de P7-61 (descriptivas, sin sello)", "",
      "**(a) Antes (días 1-7) y después (días 8-20) de la falsa**; en CON_RAZON de P7-56 no hay falsa (el día 8 solo parte el campo igual).", "",
      "| campo · brazo · hermana | d1-7: puesto · muertes/vidas · vida perdida | d8-20: puesto · muertes/vidas · vida perdida |", "|---|---|---|"]
for k in [k for k in LE["a"] if k.endswith("d1-7")]:
    a = LE["a"][k]; b = LE["a"][k.replace("d1-7", "d8-20")]
    L.append(f"| {k.replace(' · d1-7', '')} | {f(a['puesto_medio'])} · {a['muertes']}/{a['vidas']} · {f(a['vida_perdida_media'], 1)} | {f(b['puesto_medio'])} · {b['muertes']}/{b['vidas']} · {f(b['vida_perdida_media'], 1)} |")
L += ["", "**(b) Días 1-7 como réplica de la razón honesta de P7-56.** Declarado: el menú cambió (P7-61 sin EMPUNAR_RED; P7-56 con él); misma base, mismas semillas por serie.", "",
      "| campo · brazo · serie | usos del botiquín · cortados (fracción) | confianza media d1-7: cuerpo · recursos · vínculo | confianza al d7: cuerpo · recursos · vínculo |", "|---|---|---|---|"]
for k, v in LE["b"].items():
    cm = v["confianza_media_d1_7"]; c7 = v["confianza_d7"]
    L.append(f"| {k} | {v['usos_kit']} · {v['cortados']} ({f(v['fraccion_cortada'])}) | {f(cm['cuerpo'])} · {f(cm['recursos'])} · {f(cm['vinculo'])} | {f(c7['cuerpo'])} · {f(c7['recursos'])} · {f(c7['vinculo'])} |")
L += ["", "## Gasto", "", "- Plataforma: 0 partidas en P7-62 (la serie 4 cancelada antes de pedir nada).", f"- Consola de Anthropic: {f(R['local_razon']['usd'], 2)} $ (la razón de la comprobación local, {R['local_razon']['llamadas']} llamadas).", ""]
open(os.path.join(AQUI, "informe_P7_62.md"), "w").write("\n".join(L)); print("\n".join(L[-40:]))
