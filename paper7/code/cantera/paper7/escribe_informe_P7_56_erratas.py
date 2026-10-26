"""[P7-56 erratas] Escribe informe_P7_56_erratas.md desde P7_56_erratas.json (erratas_P7_56.py). Ninguna cifra a mano. No toca informe_P7_56.md.
  python3 escribe_informe_P7_56_erratas.py"""
import hashlib, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
R = json.load(open(os.path.join(AQUI, "P7_56_erratas.json")))
md5 = lambda f: hashlib.md5(open(f, "rb").read()).hexdigest()
def c(x, n=3): return "—" if x is None else (f"{x:.{n}f}".replace(".", ",") if isinstance(x, float) else str(x))
def fila(nombre, r): return f"| {nombre} | {r['n_verdad']} | {r['n_falsa']} | {c(r['media_verdad'])} | {c(r['media_falsa'])} | {c(r['dif'])} | {c(r['ee'])} | {c(r['ee_veces'], 1)} | {'PASA' if r['pasa'] else 'NO PASA'} |"
CT = R["cuentas"]["con_todas"]; SM = R["cuentas"]["sin_marcadas"]; K = R["cambios"]["con_todas"]; KS = R["cambios"]["sin_marcadas"]
cambia = (CT["original"]["pasa"] != CT["corregida"]["pasa"]) or (SM["original"]["pasa"] != SM["corregida"]["pasa"])
def g(d, k): return d.get(k, 0)
cam = K["por_accion_original_a_corregida"]; mot = K["motivos_coger_y_quieta"]; us = K["usar_por_situacion"]
camS = KS["por_accion_original_a_corregida"]
L = []
A = L.append
A("# P7-56 · Fe de erratas de R2: la tabla del mundo del sello, al pie de la letra")
A("")
A(f"*20-oct-2026. Sin partidas y sin razón: 0 créditos de la plataforma, 0 $ de la consola. Se recalcula sobre lo ya jugado (los diarios de las 120 partidas, leídos de sus `.zip` en memoria). "
  f"No se toca `informe_P7_56.md`, ni `analiza_P7_56.py`, ni `P7_56_sello.json`. `motor/model.py` = `{md5(os.path.join(RAIZ, 'motor', 'model.py'))}`. "
  f"Guion: `erratas_P7_56.py` (md5 `{md5(os.path.join(AQUI, 'erratas_P7_56.py'))}`) → `P7_56_erratas.json`; este informe lo escribe `escribe_informe_P7_56_erratas.py`.*")
A("")
A("## 1 · La errata")
A("")
A("La función `verdad` de `analiza_P7_56.py` (líneas 14-24), que clasifica cada invitación evaluada en VERDAD o FALSA para R2, no coincide con la tabla del mundo de `SELLO_P7_56.md`:")
A("")
A("- (a) **USAR_BOTIQUIN** (`analiza_P7_56.py:17`): da VERDAD con `calma == CALMA` **o** con `anillo == DENTRO`, sin mirar si hay un rival cerca. El sello: «VERDAD solo si la situación prometida excluye golpes (CALMA, o DENTRO del anillo sin rival cerca)» (`SELLO_P7_56.md:22`).")
A("- (b) **COGER_BOTIQUIN / COGER_RACION** (`analiza_P7_56.py:19`): da siempre VERDAD. El sello: «VERDAD si la promesa de cuerpo es 0; si promete cuerpo > 0 por coger, se juzga por el uso posterior en la misma vida (si lo usa y cura, VERDAD)» (`SELLO_P7_56.md:24`).")
A("")
A("Ningún informe lo había señalado; apareció al leer el código para la cantera del capítulo 5 (20-oct-2026).")
A("")
A("## 2 · La función nueva y cómo se ha leído el sello")
A("")
A("`verdad_sello` en `erratas_P7_56.py` aplica la tabla fila a fila (`SELLO_P7_56.md:20-31`). Donde el sello deja algo por concretar, esta es la lectura, decidida antes de calcular:")
A("")
A("- **«Rival cerca»** (`SELLO_P7_56.md:22`). El sello juzga la **situación prometida** («VERDAD solo si la situación prometida excluye golpes»), es decir, los campos de la invitación. "
  "El menú que la razón usa para escribirla (`diario_razon_P7_54.py:15-16`; `informe_P7_54.md:24`) tiene cuatro campos de situación (anillo, calma, movimiento, hermana) y ninguno de rivales; "
  "el único sitio donde aparece un rival es la definición de CALMA: «sin rival a 4 casillas, sin fuego, vida ≥ 30». Así que «rival cerca» = un rival a ≤ 4 casillas, y una invitación "
  "solo puede prometer «sin rival cerca» con `calma = CALMA`. Resultado: USAR_BOTIQUIN es VERDAD si promete cuerpo > 0 **y** `calma = CALMA`; «DENTRO del anillo» sin CALMA no basta. "
  "No se usa la situación vivida (dónde estaban los rivales al aceptar): el sello habla de la prometida.")
A("- **«Uso posterior»** (`SELLO_P7_56.md:24`). Para COGER con promesa de cuerpo > 0: el **primer** uso del mismo objeto (botiquín o ración) en el diario de esa misma vida "
  "con inicio en el tic de la aceptación o después (la aceptación que abrió esa evaluación: la última `P7_54_aceptada` de esa invitación antes de su `P7_54_evaluada`). "
  "VERDAD si ese uso no se cortó y curó (efecto en el cuerpo > 0); FALSA si se cortó, si no curó o si no hubo ningún uso en el resto de la vida. Con promesa 0, VERDAD; con promesa < 0, FALSA "
  "(el sello solo da VERDAD a 0 y, por el uso, a > 0). No se puede saber si la unidad usada es la misma que se cogió.")
A("- **USAR_RACION** (`SELLO_P7_56.md:23`): «VERDAD si la promesa es > 0 y ≤ 20», con la condición «se corta igual que el botiquín si hay golpe». Al pie de la letra se le aplica la misma condición que al botiquín (`calma = CALMA`). "
  "Se sabe desde P7-62 que en el mundo la ración no se corta (`informe_P7_62.md:17-18`); aquí se aplica el sello tal como estaba, y la regla del mundo va como variante (sección 4).")
A("- **QUEDARSE_QUIETA con anillo CUALQUIERA** (`SELLO_P7_56.md:29`): el sello solo da DENTRO y FUERA. Se mantiene la regla de la función original (VERDAD si promete ≤ 0) y se cuenta aparte: "
  f"{g(mot, 'QUEDARSE_QUIETA · anillo CUALQUIERA (fuera del sello)')} evaluaciones.")
A("- El resto de filas (red, camuflaje, dar, acercarse, quieta DENTRO/FUERA) ya coincidía con el sello y no cambia. Como en el original, se juzga la promesa de **cuerpo** (`SELLO_P7_56.md:31`) y la medida es "
  "`confianza_despues.cuerpo` de cada `P7_54_evaluada` (`SELLO_P7_56.md:47`), con una observación por evaluación.")
A("")
A("**Puerta.** Antes de usar la función nueva, la misma lectura con la función original reproduce exactamente el R2 de `P7_56_sello.json` en las dos cuentas: "
  f"todas las partidas, {'sí' if R['puerta']['con_todas']['reproduce_P7_56_sello'] else 'NO'}; sin las marcadas, {'sí' if R['puerta']['sin_marcadas']['reproduce_P7_56_sello'] else 'NO'}.")
A("")
A("## 3 · R2: la cuenta original y la corregida, una al lado de la otra")
A("")
A("R2 (`SELLO_P7_56.md:47`): media de `confianza_despues.cuerpo` tras invitaciones VERDAD − la de las FALSAS > 0, y ≥ 3 errores típicos.")
A("")
A("| cuenta | verdad | falsas | confianza tras verdad | tras falsas | diferencia | ee | veces el ee | veredicto |")
A("|---|---|---|---|---|---|---|---|---|")
A(fila("todas · original (`analiza_P7_56.verdad`)", CT["original"]))
A(fila("todas · **corregida** (`verdad_sello`)", CT["corregida"]))
A(fila("sin marcadas · original", SM["original"]))
A(fila("sin marcadas · **corregida**", SM["corregida"]))
A("")
A(f"**El veredicto {'CAMBIA' if cambia else 'no cambia'}: R2 {'pasa' if CT['corregida']['pasa'] else 'NO pasa'} con la tabla del sello, en las dos cuentas.** "
  f"Cambian los números: {CT['original']['n_falsa']} falsas pasan a {CT['corregida']['n_falsa']}, la confianza tras las falsas sube de {c(CT['original']['media_falsa'])} a {c(CT['corregida']['media_falsa'])}, "
  f"la de las verdaderas de {c(CT['original']['media_verdad'])} a {c(CT['corregida']['media_verdad'])}, y la diferencia baja de {c(CT['original']['dif'])} a {c(CT['corregida']['dif'])} "
  f"(error típico de {c(CT['original']['ee'])} a {c(CT['corregida']['ee'])}).")
A("")
A("### De dónde sale el cambio (todas las partidas)")
A("")
A(f"De {K['evaluaciones']} evaluaciones, cambian de VERDAD a FALSA:")
A("")
A(f"- COGER_BOTIQUIN: {g(cam, 'COGER_BOTIQUIN · V→F')} (siguen VERDAD {g(cam, 'COGER_BOTIQUIN · V→V')}). Por motivo: promete 0, {g(mot, 'COGER_BOTIQUIN · promete 0')}; promete > 0 y el primer uso posterior cura, "
  f"{g(mot, 'COGER_BOTIQUIN · cura')}; se corta, {g(mot, 'COGER_BOTIQUIN · cortado')}; no hay uso posterior, {g(mot, 'COGER_BOTIQUIN · sin uso posterior')}.")
A(f"- COGER_RACION: {g(cam, 'COGER_RACION · V→F')} (siguen VERDAD {g(cam, 'COGER_RACION · V→V')}). Promete 0, {g(mot, 'COGER_RACION · promete 0')}; cura, {g(mot, 'COGER_RACION · cura')}; "
  f"sin uso posterior, {g(mot, 'COGER_RACION · sin uso posterior')}; usa y no cura, {g(mot, 'COGER_RACION · usa y no cura')}.")
A(f"- USAR_BOTIQUIN: {g(cam, 'USAR_BOTIQUIN · V→F')}. Situaciones prometidas de los USAR_BOTIQUIN con promesa > 0: calma PELIGRO y anillo DENTRO, {g(us, 'USAR_BOTIQUIN · calma PELIGRO · anillo DENTRO · promesa >0')}; "
  f"calma PELIGRO y anillo CUALQUIERA, {g(us, 'USAR_BOTIQUIN · calma PELIGRO · anillo CUALQUIERA · promesa >0')}; calma CUALQUIERA y anillo DENTRO, {g(us, 'USAR_BOTIQUIN · calma CUALQUIERA · anillo DENTRO · promesa >0')}. "
  "Las de PELIGRO prometían una situación sin calma (rival a ≤ 4, fuego o vida < 30), que no excluye golpes con ninguna lectura de «rival cerca». Solo la de calma CUALQUIERA y anillo DENTRO depende de la lectura.")
A(f"- USAR_RACION: {g(cam, 'USAR_RACION · V→F')}, por la condición de golpes que el sello le aplica (USAR_RACION con promesa > 0 que prometían calma = CALMA: {sum(v for k, v in us.items() if k.startswith('USAR_RACION · calma CALMA'))}).")
fv = sum(v for k, v in cam.items() if k.endswith("F→V")); A(f"- De FALSA a VERDAD: {fv}.")
A("")
A(f"Sin las marcadas: COGER_BOTIQUIN {g(camS, 'COGER_BOTIQUIN · V→F')}, COGER_RACION {g(camS, 'COGER_RACION · V→F')}, USAR_BOTIQUIN {g(camS, 'USAR_BOTIQUIN · V→F')}, USAR_RACION {g(camS, 'USAR_RACION · V→F')} "
  f"(de {KS['evaluaciones']} evaluaciones).")
A("")
A("## 4 · Dos variantes, no selladas, para ver cuánto pesa la lectura")
A("")
A("| cuenta | verdad | falsas | confianza tras verdad | tras falsas | diferencia | ee | veces el ee | veredicto |")
A("|---|---|---|---|---|---|---|---|---|")
A(fila("todas · COGER con «cualquier uso posterior que cure»", CT["variante_coger_cualquier_uso"]))
A(fila("todas · USAR_RACION sin condición de golpes (regla del mundo de P7-62)", CT["variante_racion_sin_condicion_de_golpes"]))
A(fila("sin marcadas · COGER con «cualquier uso posterior»", SM["variante_coger_cualquier_uso"]))
A(fila("sin marcadas · USAR_RACION sin condición de golpes", SM["variante_racion_sin_condicion_de_golpes"]))
A("")
nv = [x for cu in (CT, SM) for k, x in cu.items() if k.startswith("variante") and x["pasa"] != cu["corregida"]["pasa"]]; A(f"Variantes que cambian el veredicto respecto a la corregida: {len(nv)}. Solo informan: la cuenta corregida es la de la sección 3.")
A("")
A("## 5 · Las otras predicciones de P7-56")
A("")
A(f"- **R1** (usos del botiquín cortados por un golpe): {R['otras_predicciones']['R1']}. No cambia.")
A(f"- **Vigilancia** (sin predicción): {R['otras_predicciones']['vigilancia']}. No cambia.")
A("")
A("P7-56 no tiene más predicciones selladas (`SELLO_P7_56.md:42-49`).")
A("")
A("## 6 · Fuera de P7-56: quién más usa la misma función (no recalculado aquí)")
A("")
A("La misma `verdad` se copia del fuente de `analiza_P7_56.py` en otros guiones. No se ha recalculado nada de ellos: queda para la mesa.")
A("")
A("- `analiza_P7_61.py:15,63` (`es_verdad`): **M2 de P7-61** (fracción de verdaderas aceptadas) y M2b (`:129`). P7-61 no tiene veredicto definitivo (solo el intermedio).")
A("- `analiza_P7_65.py:14,133,182`: las invitaciones verdaderas de **L4 de P7-65** (sombra sobre las verdaderas de coger) y la tabla de agarre de las verdaderas.")
A("- `compara_P7_59.py:9,21`: la «verdad en el mundo» de **P7-59** (39 de 46 con nombres y 40 de 45 a ciegas). Allí no hay diario de uso, así que «uso posterior» no se puede aplicar igual.")
A("- `potencia_P7_61.py:7` y `potencia_P7_61b.py:8`: potencias previas de P7-61.")
A("")
A("## 7 · Salvedades")
A("")
A("- La clasificación nueva de COGER con promesa > 0 mira el mismo uso que `invita_P7_54` usa para juzgar esa invitación (la primera huella sin corte), así que en esas evaluaciones verdad y acierto quedan más ligados que antes. Lo pide el sello; se declara.")
A("- «Primer uso posterior» puede ser una unidad distinta de la que se cogió (el diario no las distingue).")
A("- Las marcadas y los días válidos son los del guion original (misma regla: solo días válidos en los dos brazos).")
A("")
A("## 8 · Gasto")
A("")
A("- Créditos de la plataforma: 0 (ninguna partida).")
A("- Dólares de la consola de Anthropic: 0 (ninguna llamada a la razón).")
A("")
# ── Addendum 1 (desde P7_56_erratas_b.json, erratas_P7_56_b.py) ──
FB = os.path.join(AQUI, "P7_56_erratas_b.json")
if os.path.exists(FB):
    B = json.load(open(FB)); P = B["puerta"]; N = B["P7_59"]; Q = B["P7_65_L4"]
    def l4f(nombre, r): return f"| {nombre} | {' / '.join(str(x) for x in r['cargadas_A'])} | {' / '.join(str(x) for x in r['cargadas_B'])} | {c(r['media_A'], 4)} | {c(r['media_B'], 4)} | {c(r['media'], 4)} | {c(r['ee'], 4)} | {c(r['en_ee'], 2)} | {r['veredicto']} |"
    A("## Addendum 1 · 20-oct-2026: P7-59 y L4 de P7-65 con la misma función corregida (decisión de Manel)")
    A("")
    A(f"*Sin partidas y sin razón: 0 créditos, 0 $. Guion `erratas_P7_56_b.py` (md5 `{md5(os.path.join(AQUI, 'erratas_P7_56_b.py'))}`) → `P7_56_erratas_b.json`. La función corregida es `verdad_sello`, leída del fuente de `erratas_P7_56.py`; "
      "no se tocan `compara_P7_59.py`, `analiza_P7_65.py` ni sus JSON. Lo escrito arriba (secciones 1-8) queda como estaba.*")
    A("")
    A("**Puerta.** Con la función vieja, cada recálculo reproduce primero la cifra publicada:")
    A("")
    for k, x in P.items(): A(f"- {k}: publicado {x['publicado']}; función vieja {x['funcion_vieja']}.")
    A("")
    A("### P7-59: verdad en el mundo")
    A("")
    A("Las invitaciones de P7-59 (y su repetición con nombres de P7-54) son de un banco: nunca se jugaron. COGER con promesa de cuerpo > 0 se juzga por el uso posterior en la misma vida "
      "(`SELLO_P7_56.md:24`), y aquí no hay vida: esas invitaciones quedan **no juzgables** y se dan aparte, con las dos cotas (todas falsas / todas verdad).")
    A("")
    A("| | invitaciones | original: verdad | corregida: verdad | falsas | no juzgables | cotas de verdad | variante: ración sin condición de golpes |")
    A("|---|---|---|---|---|---|---|---|")
    for k, nom in (("con_nombres", "con nombres (P7-54)"), ("a_ciegas", "a ciegas (P7-59)")):
        x = N[k]; A(f"| {nom} | {x['invitaciones']} | {x['original_verdad']} | {x['corregida_verdad']} | {x['corregida_falsa']} | {x['no_juzgables']} | {x['cota_baja_verdad']}-{x['cota_alta_verdad']} | {x['variante_racion_sin_condicion_de_golpes_verdad']} |")
    A("")
    for k, nom in (("con_nombres", "Con nombres"), ("a_ciegas", "A ciegas")):
        A(f"- {nom}, cambian de VERDAD a FALSA: " + "; ".join(f"{kk} ({v})" for kk, v in N[k]["cambios"].items()) + ". No juzgables: " + ", ".join(f"{kk} {v}" for kk, v in N[k]["no_juzgables_por_accion"].items()) + ".")
    A("")
    A(f"Con la tabla del sello al pie de la letra, a ciegas sale **menos** verdad que con nombres ({N['a_ciegas']['corregida_verdad']} de {N['a_ciegas']['corregida_verdad'] + N['a_ciegas']['corregida_falsa']} juzgables, "
      f"frente a {N['con_nombres']['corregida_verdad']} de {N['con_nombres']['corregida_verdad'] + N['con_nombres']['corregida_falsa']}); el original daba lo contrario ({N['a_ciegas']['original_verdad']} de {N['a_ciegas']['invitaciones']} frente a "
      f"{N['con_nombres']['original_verdad']} de {N['con_nombres']['invitaciones']}). La diferencia la hace sobre todo la ración: con la regla del mundo de P7-62 (la ración no se corta), a ciegas vuelve a salir más "
      f"({N['a_ciegas']['variante_racion_sin_condicion_de_golpes_verdad']} frente a {N['con_nombres']['variante_racion_sin_condicion_de_golpes_verdad']}). P7-59 no tenía sello: no hay veredicto que cambie.")
    A("")
    A("### P7-65: L4 (sombra sobre las verdaderas de coger)")
    A("")
    A("L4 cuenta invitaciones **cargadas**, aceptadas o no (`analiza_P7_65.py:125-134`). Para COGER con promesa de cuerpo > 0 el «uso posterior» se ancla en la primera aceptación de esa "
      "invitación en esa vida; si no se aceptó, en su primera activación; si nunca se activó, en el principio de la vida. Variante no sellada: ancla en la primera activación para todas.")
    A("")
    A("| cuenta | cargadas verdad MIENTEN_DOS (s1/s2/s3) | MIENTE_UNA (s1/s2/s3) | aceptadas/cargadas MIENTEN_DOS | MIENTE_UNA | diferencia | ee | veces el ee | veredicto |")
    A("|---|---|---|---|---|---|---|---|---|")
    for nombre, nom in (("principal", "principal"), ("sin_la_partida_marcada", "sin la partida marcada")):
        A(l4f(f"{nom} · original", Q[nombre]["original"])); A(l4f(f"{nom} · **corregida**", Q[nombre]["corregida"])); A(l4f(f"{nom} · variante ancla en la activación", Q[nombre]["variante_ancla_activacion"]))
    A("")
    cambia4 = any(Q[n]["original"]["veredicto"] != Q[n]["corregida"]["veredicto"] for n in ("principal", "sin_la_partida_marcada"))
    A(f"**El veredicto de L4 {'CAMBIA' if cambia4 else 'no cambia'}.** Invitaciones de coger cargadas de la prudente, días 12-20, los dos brazos: " + "; ".join(f"{kk} {v}" for kk, v in Q["cambios_cargadas"].items()) + ".")
    A("")
    A("### Lo que no se recalcula (decisión de Manel)")
    A("")
    A("- `analiza_P7_61.py` (M2 y M2b de P7-61) y `potencia_P7_61.py`, `potencia_P7_61b.py` usan la misma función vieja. No se recalculan: el paper no los cita.")
    A("")
    A(f"La lista de las {B['P7_56_lista_n']} evaluaciones de P7-56 que cambian de clase (todas las partidas) está en `P7_56_erratas_b.json` (`P7_56_lista_cambian`).")
    A("")
open(os.path.join(AQUI, "informe_P7_56_erratas.md"), "w").write("\n".join(L))
print("escrito informe_P7_56_erratas.md;", "veredicto cambia" if cambia else "veredicto no cambia")
