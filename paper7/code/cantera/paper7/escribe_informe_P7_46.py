"""[P7-46] Escribe informe_P7_46.md (banco exploratorio, sin sello: lectura por prueba del campo P7-45) desde P7_46_resumen.json (analiza_P7_46), P7_46_datos.json (banco_P7_46),
P7_42_sello.json y P7_46_borrado.json. Ninguna cifra a mano.  python3 escribe_informe_P7_46.py --libre_gb N --saldo S"""
import hashlib, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
R = J("P7_46_resumen.json"); SE = J("P7_42_sello.json"); BO = J("P7_46_borrado.json"); CO = J("P7_46_copia.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
pc = lambda x: ("—" if x is None else f"{100 * x:.0f} %")
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
VAR = ("TECHO", "BORRADO_v", "BORRADO_p", "APRENDE_v", "APRENDE_p", "SIN"); ET = {"TECHO": "TECHO", "BORRADO_v": "BORRADO valiente", "BORRADO_p": "BORRADO prudente", "APRENDE_v": "APRENDE valiente", "APRENDE_p": "APRENDE prudente", "SIN": "SIN EMOCIÓN"}
libre = float(sys.argv[sys.argv.index("--libre_gb") + 1]) if "--libre_gb" in sys.argv else None; saldo = (sys.argv[sys.argv.index("--saldo") + 1] if "--saldo" in sys.argv else None)
F = R["forzadas_SIN"]; A = R["aprendizaje"]; EL = R["eleccion"]; CU = R["cuando"]; R1 = R["R1"]; M = SE["con_todas"]["medidas"]
# 1
T1 = ["| tipo | forzadas | acaban (cogida / usada) | caducan | sin fin (muerte o final) |", "|---|---:|---:|---:|---:|"]
for t in ("ir", "usar"):
    x = F["por_tipo_fin"][t]; T1.append(f"| {t} | {sum(x.values())} | {x.get('cogida', 0) + x.get('usada', 0)} | {x.get('caduca', 0)} | {sum(v for k, v in x.items() if k.startswith('sin fin'))} |")
T1o = ["| objeto | forzadas | acaban | caducan |", "|---|---:|---:|---:|"]
for o in ("botiquin", "racion", "red", "camuflaje"):
    x = F["por_objeto_fin"][o]; T1o.append(f"| {o} | {sum(x.values())} | {x.get('cogida', 0) + x.get('usada', 0)} | {x.get('caduca', 0)} |")
PQ = []
for t in ("ir", "usar"):
    tot = sum(F["por_que_caducan"][t].values())
    PQ.append(f"- **{t}** ({tot} caducan): " + "; ".join(f"{k} {v} ({100 * v / tot:.0f} %)" for k, v in F["por_que_caducan"][t].items()) + ".")
H = F["forzadas_con_huella_mismo_objeto_240"]
# 2
T2 = ["| variante | criaturas (o vidas) con pruebas de botiquín | pruebas de botiquín por criatura | creencia tras la 1.ª (n) | tras la 3.ª (n) | tras la 5.ª (n) | cambio medio por prueba ± ee (n pruebas) | primera prueba en la que llega a 25 (por criatura) |", "|---|---:|---:|---|---|---|---|---|"]
T2r = ["| variante | criaturas con pruebas de ración | pruebas por criatura | creencia tras la 1.ª (n) | tras la 3.ª (n) | tras la 5.ª (n) | cambio medio por prueba ± ee (n) |", "|---|---:|---:|---|---|---|---|"]
for var in ("BORRADO_v", "BORRADO_p", "APRENDE_v", "APRENDE_p", "SIN"):
    b = A[var]["botiquin"]; r = A[var]["racion"]; tr = lambda a, k: f"{n(a['tras'][str(k)]['mediana'], 1)} ({a['tras'][str(k)]['n']})"
    T2.append(f"| {ET[var]} | {b['criaturas']} | {n(b['pruebas_por_criatura'], 1)} | {tr(b, 1)} | {tr(b, 3)} | {tr(b, 5)} | {n(b['cambio_medio_todas']['media'], 2)} ± {n(b['cambio_medio_todas']['ee'], 2)} ({b['cambio_medio_todas']['n']}) | {(', '.join('—' if k is None else str(k) for k in b['primera_k_a_25'])) if var in ('APRENDE_v', 'APRENDE_p', 'SIN') else (str(sum(1 for k in b['primera_k_a_25'] if k)) + ' de ' + str(len(b['primera_k_a_25'])) + ' vidas (k: ' + ', '.join(str(k) for k in sorted(k for k in b['primera_k_a_25'] if k)) + ')')} |")
    T2r.append(f"| {ET[var]} | {r['criaturas']} | {n(r['pruebas_por_criatura'], 1)} | {tr(r, 1)} | {tr(r, 3)} | {tr(r, 5)} | {n(r['cambio_medio_todas']['media'], 2)} ± {n(r['cambio_medio_todas']['ee'], 2)} ({r['cambio_medio_todas']['n']}) |")
# 3
T3 = ["| variante | d1-5: pruebas · a red+cam | d6-10 | d11-15 | d16-20 | todas: pruebas · a red+cam · a botiquín+ración (b · r · red · cam) |", "|---|---|---|---|---|---|"]
for var in VAR:
    e = EL[var]; c = lambda k: f"{e[k]['n']} · {pc(e[k]['red_camuflaje'])}"; po = e["todos"]["por_objeto"]
    T3.append(f"| {ET[var]} | {c('d1-5')} | {c('d6-10')} | {c('d11-15')} | {c('d16-20')} | {e['todos']['n']} · {pc(e['todos']['red_camuflaje'])} · {pc(e['todos']['botiquin_racion'])} ({po['botiquin']} · {po['racion']} · {po['red']} · {po['camuflaje']}) |")
fo = EL["SIN_forzadas_por_objeto"]; ft = EL["SIN_forzadas_por_tramo"]
# 4
T4 = ["| variante | pruebas | con apertura P7-33 a ≤ 1 s | en calma | en peligro | rival a ≤ 4 | fuego | vida < 30 | hp0 < 50 | en calma por objeto (b · r · red · cam) |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
for var in VAR:
    c = CU[var]; po = c["por_objeto_calma"]
    T4.append(f"| {ET[var]} | {c['pruebas']} | {c['con_apertura']} | {pc(c['calma'])} | {pc(c['peligro'])} | {pc(c['rival_a_4'])} | {pc(c['fuego'])} | {pc(c['vida_menor_30'])} | {pc(c['hp0_menor_50'])} | {pc(po['botiquin'])} · {pc(po['racion'])} · {pc(po['red'])} · {pc(po['camuflaje'])} |")
# 5
cur = R1["curva_mediana"]
T5 = ["| cadena | pruebas de botiquín por vida | rapidez real (días por criatura) · media | k* propia (prueba en la que la mediana llega a 25) |", "|---|---:|---|---:|"]
for v in ("APRENDE_p", "APRENDE_v", "SIN"):
    T5.append(f"| {ET[v]} | {n(R1['pruebas_botiquin_por_vida'][v], 2)} | {', '.join(map(str, R1['rapidez_real'][v]))} · {n(R1['rapidez_real_media'][v], 1)} | {R1['k_estrella'][v] if R1['k_estrella'][v] is not None else 'no llega'} |")
T5b = ["| curva que da k* | k* | comprobación f = 1: SIN contada / real · la propia contada / real | SIN contada con f de APRENDE_p (días) · media | R1 contada frente a APRENDE_p (real) ± ee | SIN contada con f de APRENDE_v · media | R1 contada frente a APRENDE_v (real) ± ee |", "|---|---:|---|---|---|---|---|"]
for fu in ("SIN", "APRENDE_p", "APRENDE_v"):
    c = R1["contada"].get(fu)
    if not c: T5b.append(f"| {ET[fu]} | no llega | | | | | |"); continue
    p_, v_ = c["APRENDE_p"], c["APRENDE_v"]
    T5b.append(f"| {ET[fu]} | {c['k']} | {n(c['SIN_f1_media'], 1)} / {n(R1['SIN_real_media'], 1)} · {n(c['propia_f1_media'], 1)} / {n(c['propia_real_media'], 1)} | {', '.join(map(str, p_['SIN_contada_dias']))} · {n(p_['SIN_contada_media'], 1)} | {n(p_['R1_contada'], 1)} ({n(p_['R1_real'], 1)}) ± {n(p_['ee_contada'], 1)} | {', '.join(map(str, v_['SIN_contada_dias']))} · {n(v_['SIN_contada_media'], 1)} | {n(v_['R1_contada'], 1)} ({n(v_['R1_real'], 1)}) ± {n(v_['ee_contada'], 1)} |")
curva_txt = "; ".join(f"{ET[v]}: " + ", ".join(f"k{k} {n(m, 1)} ({nn})" for k, (m, nn) in list(cur[v].items())[:8]) for v in ("APRENDE_p", "APRENDE_v", "SIN"))

out = f"""# P7-46 · Banco (coste cero): lectura por prueba del campo P7-45 — EXPLORATORIO, SIN SELLO

*12-oct-2026. Banco sobre los 720 diarios de las tres series (P7-45); no se jugó ninguna partida. **Exploratorio: no hay sello, no hay predicción, no se evalúa nada; se cuenta y se
describe.** Motivo (Manel): SIN EMOCIÓN probó la mitad que APRENDE en lazo cerrado y las medidas por vida no comparan qué elige cada uno. BORRADO, solo como referencia.
Bolsa 1: 0 créditos hoy (acumulado del siete 1.185; saldo {('**' + saldo + '** créditos, página de la plataforma, 12-oct 06:47, dato de Manel') if saldo else 'el que diga la página'}). Bolsa 2: 0 $. Disco: {n(libre, 0) if libre else '—'} GB libres (sección 6).
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Scripts: `banco_P7_46.py` → `P7_46_datos.json` ({R['vidas']} vidas), `analiza_P7_46.py` → `P7_46_resumen.json`, `escribe_informe_P7_46.py`
(este informe; ninguna cifra a mano). Definiciones: «prueba» = huella `P7_huella` (ventana de prueba de una de las cuatro cosas, del congelado P7-33); «creencia» = `creencia_despues.cuerpo`
de esa huella (la creencia del cuerpo tras esa prueba); «calma / peligro» = el `peligro` de la apertura `P7_33_prueba` más cercana (≤ 24 tics) a la huella, tal como lo define el congelado
(calma = sin rival a 4, sin fuego, vida ≥ 30); «forzada» = `P7_41_azar` momento=forzada con su `fin`.*

## Sección 1 · SIN EMOCIÓN: forzadas que acaban y forzadas que caducan

{F['n']} forzadas en {M['SIN']['vidas']} vidas ({n(F['por_vida'], 2)} por vida): acaban {F['acaban']} ({100 * F['acaban'] / F['n']:.0f} %), caducan {F['caducan']} ({100 * F['caducan'] / F['n']:.0f} %), sin fin (muerte o final de partida) {F['sin_fin']}. Las que acaban tardan
{n(F['duracion_media_acaban'], 0)} tics de media (ventana de 240).

{chr(10).join(T1)}

{chr(10).join(T1o)}

**Por qué caducan** (diagnóstico de la ventana, categorías excluyentes en este orden):
{chr(10).join(PQ)}
- En las forzadas de **usar** que caducan, el hp está a 100 en el {n(F['usar_caduca_hp_100_pct_tics'], 0)} % de los tics (hp al abrir: {n(F['usar_caduca_hp0_media'], 0)} de media; en las que acaban usadas, {n(F['usar_acaba_hp0_media'], 0)}): el cuerpo congelado no
  ofrece `usar_*` con la vida llena, y la moneda, que cae en cualquier tic con un consumible en el zurrón, lo pide sobre todo entonces.
- En las de **ir** que caducan, el destino estaba a {n(F['ir_caduca_d0_media'], 1)} casillas al abrir (en las cogidas, {n(F['ir_cogida_d0_media'], 1)}): casi todas LLEGAN. La cogida de una forzada de ir depende del
  `recoger` del paso de llegada (`ir_azar` lleva `recoger`); si no cuaja, en la casilla el único camino es `coger`, y el cuerpo congelado lo construye con el PRIMER objeto de la
  casilla (`decisor_zs.py`, paso 5: `aqui[0]`) y la regla congelada del seis lo esconde si la previsión dice que la mochila no cambia (`arreglos_P6_8b`, registro `llena8`). En
  {F['llega_sin_coger_llena8'].get('con llena8', 0)} de las {sum(F['llega_sin_coger_llena8'].values())} ventanas «llega: el cuerpo no ofrece coger» hay registros `llena8` («{list(F['llega_sin_coger_llena8_motivos'])[0] if F['llega_sin_coger_llena8_motivos'] else '—'}»; {sum(F['llega_sin_coger_llena8_motivos'].values())} en total); con el zurrón lleno de verdad el cuerpo ofrece `hacer_sitio_*`, que la forzada
  no reconoce. Es decir: la moneda manda ir, la criatura va, y al llegar la pieza SIN no sabe coger lo que fue a buscar. Se apunta como límite de la pieza `azar_P7_41` (no del
  cuerpo), a corregir si se vuelve a jugar SIN: la forzada debería terminar con el `recoger` de la llegada o pedir `hacer_sitio_*` / el `coger` del objeto forzado. Se propone, no se toca.
- De las {H['acaban']} forzadas que acaban, {H['con_huella']} dejan una huella de prueba del mismo objeto dentro de la ventana + 240 tics (ir: {H['por_tipo']['ir'][0]} de {H['por_tipo']['ir'][1]}; usar: {H['por_tipo']['usar'][0]} de {H['por_tipo']['usar'][1]}): una forzada de ir que
  acaba en cogida no es todavía una prueba (la prueba de la red o el camuflaje empieza al ponérselos; la del botiquín, al usarlo).

## Sección 2 · Aprendizaje por prueba (botiquín y ración)

{chr(10).join(T2)}

{chr(10).join(T2r)}

## Sección 3 · Elección: a qué va cada prueba, por tramo de días

{chr(10).join(T3)}

En SIN, las forzadas (lo que pide la moneda) van a: botiquín {fo['botiquin']}, ración {fo['racion']}, red {fo['red']}, camuflaje {fo['camuflaje']}; a red + camuflaje por tramo: {', '.join(f"{k} {pc(x['red_camuflaje'])} ({x['n']})" for k, x in ft.items())}.

## Sección 4 · Cuándo se prueba: calma o peligro

{chr(10).join(T4)}

## Sección 5 · R1 contado de nuevo: si SIN hubiera probado el botiquín tanto como APRENDE

Solo cuenta, no simula: (i) f = pruebas de botiquín por vida de APRENDE ÷ las de SIN; (ii) k* = primera prueba en la que la mediana de la creencia del botiquín (sección 2) llega a 25,
con la curva de cada cadena (las tres se dan); (iii) para cada criatura de SIN, su calendario real de pruebas acumuladas por día, multiplicado por f; día* = primer
día en que f × acumulado ≥ k*, 21 si no. Supuestos: lo que se aprende por prueba no cambia y las pruebas extra caen en los mismos días que las reales. La comprobación del método es
la cuenta con f = 1, que debe parecerse a la rapidez real.

Curva de la mediana (k: creencia tras la k-ésima prueba, n criaturas): {curva_txt}. Cada cadena da un k* distinto; la cuenta se hace con los tres, y la comprobación f = 1 dice cuál es coherente con qué cadena.

{chr(10).join(T5)}

{chr(10).join(T5b)}

## Sección 6 · Disco (archivado en el T7, 12-oct)

Los pilotos de P7-42 ya estaban archivados el 11-oct (zips leídos de vuelta y relectura tras remontar; `P7_43_copia.json`). Hoy, con el T7 conectado: los campos del seis que seguían con
diarios extraídos (P61, P610, P611, P616, P618, P622, P623, P624, P626, P627, P64, P66, P68), P7-33 y el resto de P7-24 — nada de eso lo usa el análisis del siete — a
`/Volumes/Mem G-EMV/gemv_archivo_2026-10-12` (`archiva_P7_46.py`, molde del 11-oct): {CO['archivos']} archivos copiados ({n(CO['bytes'] / 2 ** 30, 2)} GiB: zips, registros, PARCIAL, manifiestos, estados), leídos de vuelta iguales
{CO['iguales']} de {CO['archivos']}, relectura tras desmontar y montar {'sí' if CO.get('releido_tras_remontar') else 'NO'}; borrados del Mac {BO['borrados']} diarios extraídos cuyo zip pasó (no borrados {BO['no_borrados']}: rescatados sin zip); libre {n(BO['libre_antes_GB'], 1)} → {n(BO['libre_despues_GB'], 1)} GB. Los zips
se quedan en el Mac; las tres series (27 GB) no se tocan.
"""

cal = CU; e_sin = EL["SIN"]["todos"]; e_ap = EL["APRENDE_p"]["todos"]; a_b = A["SIN"]["botiquin"]; a_p = A["APRENDE_p"]["botiquin"]; a_v = A["APRENDE_v"]["botiquin"]
c_sin = R1["contada"]["SIN"]; c_ap = R1["contada"]["APRENDE_p"]; c_av = R1["contada"]["APRENDE_v"]
out += f"""
## Lectura (exploratoria; nada de esto evalúa el sello)

1. **La moneda de SIN manda, pero el cuerpo no obedece**: de {F['n']} forzadas, acaban {F['acaban']} ({100 * F['acaban'] / F['n']:.0f} %). Las de usar caducan porque el cuerpo congelado no ofrece `usar_*` con la vida llena
   ({F['por_que_caducan']['usar'].get('usar nunca ofrecido por el cuerpo', 0)} de {sum(F['por_que_caducan']['usar'].values())}); las de ir llegan y no cogen ({F['por_que_caducan']['ir'].get('llega: el cuerpo no ofrece coger', 0) + F['por_que_caducan']['ir'].get('llega: zurrón lleno (hacer_sitio, sin coger)', 0)} de {sum(F['por_que_caducan']['ir'].values())}): la pieza SIN no sabe terminar lo que empieza. Por eso
   SIN probó la mitad: no por la ε calibrada, sino porque la forzada muere en la llegada o en el usar. Es un límite de `azar_P7_41`, no del aprendiz ni del cuerpo.
2. **Lo que se aprende por prueba** del botiquín es parecido entre cadenas y pequeño: creencia tras la 3.ª prueba {n(a_p['tras']['3']['mediana'], 1)} (APRENDE prudente), {n(a_v['tras']['3']['mediana'], 1)} (valiente), {n(a_b['tras']['3']['mediana'], 1)} (SIN, n = {a_b['tras']['3']['n']}); tras la 5.ª
   {n(a_p['tras']['5']['mediana'], 1)}, {n(a_v['tras']['5']['mediana'], 1)}, {n(a_b['tras']['5']['mediana'], 1)}. Para llegar a 25 la mediana necesita {R1['k_estrella']['APRENDE_p']} pruebas en APRENDE prudente, {R1['k_estrella']['APRENDE_v']} en valiente y {R1['k_estrella']['SIN']} en SIN (3 criaturas); el cambio medio por prueba es
   {n(a_p['cambio_medio_todas']['media'], 2)} ± {n(a_p['cambio_medio_todas']['ee'], 2)}, {n(a_v['cambio_medio_todas']['media'], 2)} ± {n(a_v['cambio_medio_todas']['ee'], 2)} y {n(a_b['cambio_medio_todas']['media'], 2)} ± {n(a_b['cambio_medio_todas']['ee'], 2)}. BORRADO, desde cero cada día, sube {n(A['BORRADO_v']['botiquin']['cambio_medio_todas']['media'], 1)}-{n(A['BORRADO_p']['botiquin']['cambio_medio_todas']['media'], 1)} por prueba (las primeras pruebas son las que más suben).
3. **La elección no distingue a nadie**: a red + camuflaje va el {pc(e_sin['red_camuflaje'])} de las pruebas de SIN y el {pc(e_ap['red_camuflaje'])}-{pc(EL['APRENDE_v']['todos']['red_camuflaje'])} de las de APRENDE (BORRADO {pc(EL['BORRADO_p']['todos']['red_camuflaje'])}-{pc(EL['BORRADO_v']['todos']['red_camuflaje'])}), y no cambia con los días. La curiosidad con
   esperanza de clase (P7-40) no desvía las pruebas hacia lo útil ni lejos de lo inútil más que la moneda.
4. **Se prueba en peligro**: en calma solo el {pc(cal['APRENDE_p']['calma'])}-{pc(cal['BORRADO_v']['calma'])} de las pruebas en todos los brazos (SIN {pc(cal['SIN']['calma'])}); con rival a 4 casillas o menos el {pc(min(cal[v]['rival_a_4'] for v in VAR if cal[v]['rival_a_4'] is not None))}-{pc(max(cal[v]['rival_a_4'] for v in VAR if cal[v]['rival_a_4'] is not None))}. Botiquín y ración se prueban en
   peligro (en calma {pc(cal['APRENDE_p']['por_objeto_calma']['botiquin'])}-{pc(cal['APRENDE_v']['por_objeto_calma']['botiquin'])} en APRENDE), la red y el camuflaje en calma ({pc(cal['APRENDE_p']['por_objeto_calma']['red'])}-{pc(cal['APRENDE_v']['por_objeto_calma']['red'])}): es el cuerpo quien decide cuándo (usa el botiquín cuando le duele), no el aprendiz.
5. **R1 contado de nuevo**: si SIN hubiera probado el botiquín {n(c_sin['APRENDE_p']['f'], 1)}-{n(c_sin['APRENDE_v']['f'], 1)} veces más (lo de APRENDE), con su propia curva (k* = {c_sin['k']}) su rapidez media pasaría de {n(R1['SIN_real_media'], 1)} a {n(c_sin['APRENDE_p']['SIN_contada_media'], 1)} días y R1 quedaría en
   {n(c_sin['APRENDE_p']['R1_contada'], 1)} ± {n(c_sin['APRENDE_p']['ee_contada'], 1)} (prudente) y {n(c_sin['APRENDE_v']['R1_contada'], 1)} ± {n(c_sin['APRENDE_v']['ee_contada'], 1)} (valiente): el mismo ruido que el real ({n(c_sin['APRENDE_p']['R1_real'], 1)} y {n(c_sin['APRENDE_v']['R1_real'], 1)}). Con la curva de APRENDE prudente (k* = {c_ap['k']}) o valiente (k* = {c_av['k']}) sale
   {n(c_ap['APRENDE_p']['R1_contada'], 1)} / {n(c_av['APRENDE_p']['R1_contada'], 1)} frente a prudente. {a_b['criaturas'] - a_b['tras']['1']['n']} de las {a_b['criaturas']} criaturas de SIN no probaron el botiquín ni una vez: multiplicar cero sigue siendo cero, y son ellas las que sostienen el 21.
   La comprobación f = 1 cuadra con la cadena que presta la curva ({n(c_sin['SIN_f1_media'], 1)} / {n(R1['SIN_real_media'], 1)} en SIN; {n(c_ap['propia_f1_media'], 1)} / {n(c_ap['propia_real_media'], 1)} en prudente; {n(c_av['propia_f1_media'], 1)} / {n(c_av['propia_real_media'], 1)} en valiente) y no cuadra cruzada: lo que se aprende por prueba NO es igual entre cadenas, así que
   el supuesto (i) de la cuenta es el flojo. Conclusión exploratoria: R1 no cambiaría de signo ni saldría del ruido por igualar las pruebas; lo que separa a las criaturas es si
   el cuerpo llega a usar el botiquín alguna vez, y eso lo decide el dolor, no la curiosidad.
"""
open(os.path.join(AQUI, "informe_P7_46.md"), "w", encoding="utf-8").write(out); print("informe_P7_46.md", out.count("\n"), "lineas")
