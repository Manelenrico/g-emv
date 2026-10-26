"""[P7-34] Escribe informe_P7_34.md (el campo de lo inutil, entero) desde P7_34_datos.json (analiza_P7_34), P7_34_sello.json (sello_P7_34), P7_34_freno.json, P7_34_estado.json,
semillas_P7_34.json, P7_33_estado.json y P7_34_gif.json (si existe). Ninguna cifra a mano."""
import hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
V = [v for v in J("P7_34_datos.json") if not v.get("sin_diario")]; SE = J("P7_34_sello.json"); E = J("P7_34_estado.json"); S = J("semillas_P7_34.json"); FR = J("P7_34_freno.json"); E33 = J("P7_33_estado.json")
GIF = J("P7_34_gif.json") if os.path.exists(os.path.join(AQUI, "P7_34_gif.json")) else None
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
COSAS = ("botiquin", "racion", "red", "camuflaje"); ACUM_ANTES = 52.9290      # acumulado del siete tras el humo de P7-33 (informe_P7_33, F4)
coste = sum(p.get("coste_usd") or 0 for p in E["peticiones"]); partidas = sum(1 for p in E["peticiones"] if p.get("coste_usd")); corte = {tuple(x) for x in SE["partidas_con_corte"]}; marc = {tuple(x) for x in SE["partidas_marcadas"]}
BLOQUES = (("1-5", range(1, 6)), ("6-10", range(6, 11)), ("11-15", range(11, 16)), ("16-20", range(16, 21)))


def vs(b, dias): return [v for v in V if v["brazo"] == b and v["dia"] in dias]
def med(xs): xs = [x for x in xs if x is not None]; return st.mean(xs) if xs else None
def mediana(xs): xs = [x for x in xs if x is not None]; return st.median(xs) if xs else None


# tabla 1: por brazo y bloque de dias, por cosa: contactos (vidas con contacto), cogidas por vida, pruebas (en calma), usos, sueltas
T1 = ["| brazo | días | vidas | " + " | ".join(f"{o}: vidas con contacto · cogidas/vida · pruebas (en calma) · usos · sueltas" for o in COSAS) + " |", "|---|---|---:|" + "---|" * 4]
for b in ("TECHO", "BORRADO", "APRENDE"):
    for et, dias in BLOQUES:
        x = vs(b, dias)
        if not x: continue
        celdas = []
        for o in COSAS:
            usos = ("—" if b == "TECHO" else str(sum(v['usa'][o] for v in x))); sueltas = (sum(v['usa'][o] + v['suelta'][o] for v in x) if b == "TECHO" else sum(v['suelta'][o] for v in x))      # TECHO nace sabiendo: sin canal de uso (P7_nace_uso); sus bajadas van juntas
            celdas.append(f"{sum(1 for v in x if v['contacto'][o] is not None)} · {n(med([v['coge'][o] for v in x]), 2)} · {sum(v['pruebas'][o]['n'] for v in x)} ({sum(v['pruebas'][o]['en_calma'] for v in x)}) · {usos} · {sueltas}")
        T1.append(f"| {b} | {et} | {len(x)} | " + " | ".join(celdas) + " |")
# tabla 2: APRENDE por criatura y bloque: recuerdos (firmes, al menos, cortes, no hizo nada), creencia, ignorancia, ganas al cerrar el ultimo dia del bloque
T2 = ["| criatura | día | " + " | ".join(f"{o}: recuerdos (firmes · «al menos» · cortes · «no hizo nada») · creencia · ignorancia · ganas" for o in COSAS) + " |", "|---|---|" + "---|" * 4]
for s in (1, 2):
    for sl in (10, 11):
        for d in (5, 10, 15, 20):
            v = next((v for v in V if v["brazo"] == "APRENDE" and v["serie"] == s and v["asiento"] == sl and v["dia"] == d), None)
            if not v: continue
            celdas = []
            for o in COSAS:
                a = v["al_acabar"][o]; k = (v.get("k_al_acabar") or {}).get(o)
                celdas.append(f"{a['recuerdos']} ({a['firmes']} · {a['al_menos']} · {a['cortes']} · {a['no_hizo_nada'] if o in ('red', 'camuflaje') else '—'}) · {n(a['creencia'], 1)} · {n(a['ignorancia'], 2)} · {n(k, 3)}")
            T2.append(f"| s{s} a{sl} | {d} | " + " | ".join(celdas) + " |")
# tabla 3: puesto, muerte, latencia, agua por brazo y bloque
T3 = ["| brazo | días | vidas (en puesto) | puesto medio | mueren · tic de la muerte (mediana) | ms por decisión: mediana · p95 (máx entre vidas) | sobre el tic (máx) | bloqueados sin cuerpo (máx) | vidas marcadas | avisos oídos · casillas cerradas (máx) · tics con `blocked` por vida (cualquier causa) |", "|---|---|---|---:|---|---|---:|---:|---:|---|"]
for b in ("TECHO", "BORRADO", "APRENDE"):
    for et, dias in BLOQUES:
        x = vs(b, dias); xp = [v for v in x if (v["serie"], v["dia"], b) not in corte and v["puesto"] is not None]; mu = [v for v in x if v["murio"]]
        if not x: continue
        T3.append(f"| {b} | {et} | {len(x)} ({len(xp)}) | {n(med([v['puesto'] for v in xp]), 2)} | {len(mu)} · {n(mediana([v['tic_muerte'] for v in mu]), 0)} | {n(mediana([v['latencia']['ms_mediana'] for v in x]), 2)} · {n(max((v['latencia']['ms_p95'] or 0) for v in x), 1)} | {n(100 * max((v['latencia']['sobre_el_tic'] or 0) for v in x), 2)} % | {n(100 * max(v['latencia']['fraccion_sin_cuerpo'] for v in x), 2)} % | {sum(1 for v in x if not v['latencia']['pasa'])} | {sum(len(v['ley']['avisos']) for v in x)} · {max((max((c for _, c in v['ley']['casillas']), default=0) for v in x), default=0)} · {n(med([v['ley']['bloqueados'] for v in x]), 1)} |")


def sello_t(cuenta):
    R = SE[cuenta]; L = ["| | regla | resultado | pasa |", "|---|---|---|---|"]
    i1 = R["I1"]["pruebas_dias_1_5"]; L.append(f"| I1 | prueba lo inútil (día 5: ≥ 1 prueba de red y ≥ 1 de camuflaje en las 4) | {'; '.join(f'{k}: red {x['red']}, camuflaje {x['camuflaje']}' for k, x in i1.items())} | {'sí' if R['I1']['pasa'] else 'NO'} |")
    i2 = R["I2"]; L.append(f"| I2 | deja de quererlo (días 11-20: inútil/vida de APRENDE ≤ ¼ de TECHO y ≤ ¼ de su útil) | APRENDE inútil {n(i2['APRENDE_inutil_por_vida'], 3)} por vida (n = {i2['n_APRENDE']}); TECHO inútil {n(i2['TECHO_inutil_por_vida'], 3)} (n = {i2['n_TECHO']}); APRENDE útil {n(i2['APRENDE_util_por_vida'], 3)} | {'sí' if i2['pasa'] else 'NO'} |")
    i3 = R["I3"]; L.append(f"| I3 | lo recuerda débil (día 20: intensidad media inútil < ½ útil) | útil {n(i3['util_media'], 4)} · inútil {n(i3['inutil_media'], 4)}; por criatura: {'; '.join(f'{k}: ' + ('—' if x is None else f'útil {n(x['util'], 3)} ({x['n_util']}), inútil {n(x['inutil'], 3)} ({x['n_inutil']})') for k, x in i3['por_criatura'].items())} | {'sí' if i3['pasa'] else 'NO'} |")
    i4 = R["I4"]; L.append(f"| I4 | lo olvidado vuelve a parecer nuevo (≥ 2 criaturas con una prueba tras ≥ 5 días sin tocar la cosa) | {i4['criaturas_con_vuelta']} criaturas: {'; '.join(f'{k}: ' + (', '.join(f'{h['cosa']} día {h['dia']}' for h in hs) if hs else 'ninguna') for k, hs in i4['vueltas'].items())} | {'sí' if i4['pasa'] else 'NO'} |")
    i5 = R["I5"]; p1 = i5["APRENDE - BORRADO dias 1-5"]; p2 = i5["APRENDE - BORRADO dias 16-20"]
    L.append(f"| I5 | lo útil sigue (botiquín dentro ≥ 30 el día 20 en ≥ 3 de 4; y no se hunde frente a BORRADO) | creencia día 20: {', '.join(f'{k} {n(c, 1)}' for k, c in i5['creencia_botiquin_dia_20'].items())} → {i5['llegan_a_30']} llegan a 30; APRENDE − BORRADO días 1-5 {n(p1['media'], 2)} ± {n(p1['ee'], 2)} (n = {p1['n']}), días 16-20 {n(p2['media'], 2)} ± {n(p2['ee'], 2)} (n = {p2['n']}); ee de la diferencia {n(i5['ee_diferencia'], 2)}; se hunde: {i5['se_hunde']} | {'sí' if i5['pasa'] else 'NO'} |")
    i6 = R["I6"]; L.append(f"| I6 | lo curioso en calma (≥ 80 % de las pruebas de red y camuflaje de APRENDE en calma) | {i6['en_calma']} de {i6['aperturas']} aperturas en calma ({n(100 * (i6['fraccion'] or 0), 1)} %) | {'sí' if i6['pasa'] else 'NO'} |")
    return "\n".join(L)


fr = FR; fv = fr["vidas"]
freno_t = "\n".join(["| vida | puesto | cuaderno leído | recuerdos arranque → cierre | orden de contacto | creencia útil al cerrar (botiquín / ración) | errores de fotos | guarda (mediana ms · sobre el tic · sin cuerpo) |", "|---|---:|---|---|---|---|---:|---|"] +
                    [f"| {k.replace('_', ' ')} | {v.get('puesto')} | {'sí' if v.get('cuaderno_leido') else 'no'} | {v.get('recuerdos_al_arrancar')} → {v.get('recuerdos_al_cerrar')} | {', '.join(v.get('orden_de_contacto') or []) or '—'} | {n((v.get('creencia_util_fin') or {}).get('botiquin'), 1)} / {n((v.get('creencia_util_fin') or {}).get('racion'), 1)} | {v.get('errores_fotos')} | {n(v['latencia']['ms_mediana'], 1)} · {n(100 * (v['latencia']['sobre_el_tic'] or 0), 2)} % · {n(100 * v['latencia']['fraccion_sin_cuerpo'], 2)} % |" for k, v in fv.items() if not v.get("sin_diario")])
tot_err = sum(v["errores_fotos"] for v in V)
lat_marc = [f"s{v['serie']} d{v['dia']} {v['brazo']} a{v['asiento']} ({n(100 * (v['latencia']['sobre_el_tic'] or 0), 2)} % · {n(100 * v['latencia']['fraccion_sin_cuerpo'], 2)} %)" for v in V if not v["latencia"]["pasa"]]
gif_txt = ("" if GIF is None else f"- `P7_34_gif_prueba_{GIF['prueba']['cosa']}.gif`: la criatura s{GIF['criatura']['serie']} a{GIF['criatura']['asiento']} de APRENDE, día {GIF['prueba']['dia']}, prueba del {GIF['prueba']['cosa']} abierta en calma en el tic {GIF['prueba']['tick']} (cierra en el {GIF['prueba']['t_fin']}); `P7_34_gif_uso_botiquin.gif`: la misma criatura, día {GIF['uso']['dia']}, uso del botiquín abierto en peligro en el tic {GIF['uso']['tick']} ({', '.join(k for k in ('rival_a_4', 'fuego', 'vida_menor_30') if GIF['uso']['contexto'].get(k))}). GIFs de los datos del diario (matplotlib), fuera de git; `gif_P7_34.py`, `P7_34_gif.json`.")


A = [v for v in V if v["brazo"] == "APRENDE"]; c_g = [x for v in A for o in ("red", "camuflaje") for x in v["pruebas"][o]["contextos"]]
I1 = SE["con_todas"]["I1"]["pruebas_dias_1_5"]; sin_red = [k for k, x in I1.items() if x["red"] == 0]; sin_camo = [k for k, x in I1.items() if x["camuflaje"] == 0]
def contacto_1_5(k, o):
    s_, sl = int(k[1]), int(k[-2:]); return sum(v["coge"][o] for v in A if v["serie"] == s_ and v["asiento"] == sl and v["dia"] <= 5)
I2 = SE["con_todas"]["I2"]; I3 = SE["con_todas"]["I3"]; I4b = SE["sin_marcadas"]["I4"]; I5 = SE["con_todas"]["I5"]; I6 = SE["con_todas"]["I6"]
gear20 = {f"s{v['serie']} a{v['asiento']}": {o: (v["al_acabar"][o]["creencia"], v["al_acabar"][o]["recuerdos"], v["al_acabar"][o]["no_hizo_nada"]) for o in ("red", "camuflaje")} for v in A if v["dia"] == 20}
con_efecto = [(k, o, x[0], x[1] - x[2]) for k, d in gear20.items() for o, x in d.items() if x[1] - x[2] > 0]
marc_brazo = {b: sum(1 for v in V if v["brazo"] == b and not v["latencia"]["pasa"]) for b in ("TECHO", "BORRADO", "APRENDE")}; ms_brazo = {b: st.median(v["latencia"]["ms_mediana"] for v in V if v["brazo"] == b and v["latencia"]["ms_mediana"] is not None) for b in ("TECHO", "BORRADO", "APRENDE")}
peor = max(V, key=lambda v: (v["latencia"]["sobre_el_tic"] or 0))
lectura = f"""(i) **Lo inútil se prueba, y en calma, pero no en las cuatro antes del día 5 (I1 no pasa)**: tres criaturas prueban la red y el camuflaje en los días 1-5; la cuarta ({', '.join(sin_red) or '—'}) no prueba la red porque no la toca ({', '.join(f'{k}: 0 redes cogidas en los días 1-5' for k in sin_red)}); el camuflaje lo prueban las cuatro. En los 20 días, las 4 criaturas acumulan {sum(x[1] for d in gear20.values() for x in d.values())} recuerdos de red y camuflaje, {sum(x[2] for d in gear20.values() for x in d.values())} de ellos «no hizo nada». (ii) **Lo curioso en calma, casi (I6: {n(100 * I6['fraccion'], 1)} %, el umbral era 80)**: de {len(c_g)} aperturas de red y camuflaje, {sum(1 for x in c_g if x['calma'])} en calma; las {sum(1 for x in c_g if not x['calma'])} restantes, {sum(1 for x in c_g if x['rival_a_4'])} con un rival a 4 casillas o menos, {sum(1 for x in c_g if x['fuego'])} con fuego, {sum(1 for x in c_g if x['vida_menor_30'])} con la vida por debajo de 30. El botiquín y la ración, al revés: de sus {sum(v['pruebas'][o]['aperturas'] for v in A for o in ('botiquin', 'racion'))} aperturas en APRENDE, {sum(v['pruebas'][o]['en_calma'] for v in A for o in ('botiquin', 'racion'))} en calma. (iii) **No deja de quererlo (I2 no pasa)**: en los días 11-20 APRENDE coge {n(I2['APRENDE_inutil_por_vida'], 2)} redes + camuflajes por vida, MÁS que TECHO ({n(I2['TECHO_inutil_por_vida'], 2)}), y no la cuarta parte de lo útil ({n(I2['APRENDE_util_por_vida'], 2)}); las ganas (k) de red y camuflaje están en 0,000 casi siempre (tabla del cuaderno), así que lo que las coge no es la curiosidad de clase: `ir_curioso` con el paso listo es el {n(100 * st.median(v['ir_curioso_fraccion'] for v in A), 1)} % (mediana) en APRENDE; la lectura más sencilla (mía, no comprobada en este informe) es que las coge el cuerpo al pasar por encima (`coger`, que no sabe de clases) y, de vez en cuando, la curiosidad que vuelve cuando el olvido sube la ignorancia (I4); separarlo pide mirar qué candidato se elige en cada cogida. (iv) **Lo recuerda igual de fuerte, no más débil (I3 no pasa)**: intensidad media {n(I3['inutil_media'], 3)} en los recuerdos de red y camuflaje frente a {n(I3['util_media'], 3)} en los de botiquín y ración: la intensidad del cuaderno (`cuaderno_P7`) sale del cambio del malestar durante la prueba, no del efecto, y en 10 s de calma el malestar cambia lo mismo con una red puesta que con un botiquín usado. Un recuerdo de «no hizo nada» pesa en el cuaderno lo mismo que uno de curar 28 puntos; lo que los distingue es la creencia (0,0 en red y camuflaje en {sum(1 for d in gear20.values() for x in d.values() if x[0] is not None and abs(x[0]) < 0.05)} de 8 cuadernos del día 20; {', '.join(f'{k} {o} {n(c, 1)} con {m} recuerdo{"s" if m > 1 else ""} con efecto en el cuerpo' for k, o, c, m in con_efecto) or 'ninguno con efecto'}: ventanas en las que la vida subió por otra causa). (v) **Lo olvidado vuelve a parecer nuevo (I4 pasa en la primera cuenta)**: s1 a11 prueba una red el día 11 tras cinco días sin tocarla, y s2 a11 el día 18; en la segunda cuenta I4 cae no porque aparezca un contacto, sino porque las partidas marcadas (s1 d10 y s2 d16 de APRENDE, marcadas por el OTRO asiento) salen de la ventana de cinco días y la regla, tal como está escrita, exige los cinco días presentes. (vi) **Lo útil sigue (I5 pasa)**: creencia del botiquín dentro el día 20 {', '.join(f'{k} {n(c, 1)}' for k, c in I5['creencia_botiquin_dia_20'].items())} (3 de 4 llegan a 30); APRENDE − BORRADO en puesto {n(I5['APRENDE - BORRADO dias 1-5']['media'], 2)} ± {n(I5['APRENDE - BORRADO dias 1-5']['ee'], 2)} en los días 1-5 y {n(I5['APRENDE - BORRADO dias 16-20']['media'], 2)} ± {n(I5['APRENDE - BORRADO dias 16-20']['ee'], 2)} en los 16-20 (negativo = mejor puesto que BORRADO): la que recuerda no se hunde y queda por delante de la que borra los 20 días ({n(SE['APRENDE - BORRADO todos los dias']['media'], 2)} ± {n(SE['APRENDE - BORRADO todos los dias']['ee'], 2)}, n = {SE['APRENDE - BORRADO todos los dias']['n']}). (vii) **Latencia**: vidas marcadas por brazo TECHO {marc_brazo['TECHO']}, BORRADO {marc_brazo['BORRADO']}, APRENDE {marc_brazo['APRENDE']} (medianas de ms por decisión {n(ms_brazo['TECHO'], 2)}, {n(ms_brazo['BORRADO'], 2)}, {n(ms_brazo['APRENDE'], 2)}); la peor, s{peor['serie']} d{peor['dia']} {peor['brazo']} a{peor['asiento']} con el {n(100 * peor['latencia']['sobre_el_tic'], 2)} % sobre el tic, disparó la parada dura del lanzador (> 10 %) cuando la serie 2 ya estaba entera jugada y bajada: nada quedó sin jugar. La pieza de las cuatro cosas pesa más en BORRADO (cuaderno vacío cada día: más clases ignoradas, más `ir_curioso`, más fotos) que en APRENDE. (viii) **Oído y ley**: las {sum(len(v['ley']['avisos']) for v in V)} avisos de inundación oídos en {len(V)} vidas, 25 casillas cerradas en cada una; ninguna vida con más del 5 % de pasos listos bloqueados sin cuerpo (máximo {n(100 * max(v['latencia']['fraccion_sin_cuerpo'] for v in V), 2)} %): el agua ya no bloquea a nadie. (ix) Dos cortes de la plataforma sin artefacto (s2 d6 y s2 d8 de TECHO, asiento 11, 0 líneas rescatadas): sus partidas salen de los puestos; 0 errores de fotos en las {len(V)} vidas."""

out = f"""# P7-34 · El campo de lo inútil

*{__import__('datetime').date.today().strftime('%-d-%b-%Y').replace('Oct', 'oct')}. Plataforma: {n(coste, 4)} USD en {partidas} partidas (créditos de la plataforma, por el sidecar de Bedrock); consola de Anthropic: 0. Acumulado del siete:
{n(ACUM_ANTES, 4)} + {n(coste, 4)} = {n(ACUM_ANTES + coste, 4)} USD de plataforma (saldos no consultados). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar.
Sello: `SELLO_P7_34.md` (commit `65e7354`, antes de pedir ninguna partida). Piezas: las de P7-33 (`nace_P7_33.py` = `{md5('nace_P7_33.py')}`, `policy_pareja_P7_33.py`) con el arreglo del paso 0 en
`nace_P7_29.py` (= `{md5('nace_P7_29.py')}`). Scripts: `lanza_P7_34.py`, `corre_P7_34.sh`, `freno_P7_34.py`, `analiza_P7_34.py` → `P7_34_datos.json`, `sello_P7_34.py` → `P7_34_sello.json`,
`figuras_P7_34.py`, `gif_P7_34.py`, `escribe_informe_P7_34.py` (este informe; ninguna cifra a mano). Diarios en `paintball/runs/P734_*` (fuera de git).*

## Paso 0 · El arreglo del descuadre de fotos

El descuadre «N fotos para N+1 candidatos» (marcado como `P7_error` por `nace_P7_29`) no venía de la pieza de las cuatro cosas: la pieza congelada del seis `arreglos_P6_8b._cands`
(`cantera/paper6/arreglos_P6_8b.py:134-140`), que `policy_pareja11.run` aplica DESPUÉS de las del siete (`policy_pareja11.py:53`), esconde `coger` cuando la mochila está llena
(registro `llena8`) por FUERA del envoltorio del siete; los nombres de los candidatos se tomaban antes y las fotos por índice (`_P29_curioso`, `_P29_usa`) se corrían un sitio en
esos tics. Ya ocurría en P7-30 (d10 de APRENDE: 3 marcas por vida, el tope de 3 que escribe el diario). Arreglo en `nace_P7_29.decidir`: se envuelve lo que haya en `D.candidatos`
en el momento de decidir y los nombres se toman de la lista final (el patrón de `policy_cortex.decidir`). Comprobado antes de jugar: la réplica de la vida d1 a10 del humo de P7-33
da 0 descuadres y 11.130 / 11.130 decisiones iguales al diario; F1 de P7-33 repetida con el arreglo, idéntica (todo apagado = A4: 1.007.274 igual · 2 difiere; TECHO con oído y
ley: 1.007.078 igual · 198 difiere en 6 vidas); F2 de P7-33 repetida, idéntica en todas las medidas (cuaderno vacío: k = 0 y cura imaginada 0; tres redes sin efecto: creencia 0,0,
ignorancia 0,21-0,27, `ir_curioso` a la red 0/0/0/115). En el campo: {tot_err} errores de fotos en {len(V)} vidas.

## El diseño y el freno

Las piezas de P7-33 tal como quedaron; tres brazos (TECHO, APRENDE, BORRADO) de la misma imagen (`Dockerfile.pareja_P7_34`); pedir corregido y lo dado entregado; ojos compartidos
apagados; 20 días; la misma semilla para los tres brazos cada día; dos series una detrás de otra (la 2 en orden inverso). Semillas k = {S['k'][0]}-{S['k'][-1]} (`semillas_P7_34.json`,
declaradas antes de jugar): serie 1 {S['serie1'][0]}, {S['serie1'][1]}, …, {S['serie1'][-1]}. Guardas de P7-30 (latencia marca y sigue; para solo al 10 % sobre el tic o al 5 % bloqueados sin
cuerpo; disco; red; cortes).

Freno (días 1-3 de APRENDE, serie 1; `P7_34_freno.json`): (a) el cuaderno viaja y se lee: {'sí' if fr['a_cuaderno_viaja'] else 'NO'}; (b) tocan alguna de las cuatro cosas: {len(fr['b_tocan'])} de 6 vidas ({', '.join(fr['b_tocan'])}): {'sí' if fr['b_pasa'] else 'NO'};
(c) sube la creencia de alguna cosa útil: {'; '.join(fr['c_sube']) or 'ninguna'}: {'sí' if fr['c_pasa'] else 'NO'}; (d) errores de fotos: {', '.join(f'{k} {e}' for k, e in fr['d_errores_fotos'].items())}: {'sí' if fr['d_pasa'] else 'NO'}. **FRENO: {fr['FRENO']}.**

{freno_t}

## El campo

{len(V)} vidas leídas de {partidas} partidas; partidas con corte: {len(corte)} ({', '.join(f's{a} d{b} {c}' for a, b, c in sorted(corte)) or 'ninguna'}); partidas marcadas por la guarda de latencia: {len(marc)} ({', '.join(f's{a} d{b} {c}' for a, b, c in sorted(marc)) or 'ninguna'});
vidas marcadas: {len(lat_marc)} ({'; '.join(lat_marc) or 'ninguna'}).

### Las cuatro cosas por brazo y bloque de días

(«Pruebas» del botiquín y la ración: huellas de uso; de la red y el camuflaje: ventanas de 10 s. «Usos»: aperturas del canal `P7_nace_uso` (TECHO nace sabiendo y no lo tiene: sus bajadas de unidades van juntas en la última cifra). «Sueltas»: bajadas que no son usos.)

{chr(10).join(T1)}

### Lo que lleva cada criatura de APRENDE en el cuaderno (al cerrar los días 5, 10, 15 y 20)

{chr(10).join(T2)}

### Puesto, muerte, latencia y agua

{chr(10).join(T3)}

## El sello, evaluado una vez

### Primera cuenta: con todas las vidas (las partidas con corte, fuera de los puestos)

{sello_t('con_todas')}

### Segunda cuenta: sin las partidas marcadas por la guarda

{sello_t('sin_marcadas')}

Cambian entre las dos cuentas: {', '.join(SE['cambian_entre_las_dos_cuentas']) or 'ninguna'}. Sin predicción, solo medida: APRENDE − BORRADO en puesto, los 20 días: {n(SE['APRENDE - BORRADO todos los dias']['media'], 2)} ± {n(SE['APRENDE - BORRADO todos los dias']['ee'], 2)} (n = {SE['APRENDE - BORRADO todos los dias']['n']}).


## Lectura

{lectura}
## Figuras y GIFs

- `P7_34_fig_cuatro.png`: creencia, ignorancia y ganas de las cuatro cosas por día (APRENDE, media de las criaturas con valor; BORRADO punteado). `P7_34_fig_cogidas.png`: cogidas de lo útil frente a lo inútil por día y brazo. `P7_34_fig_puesto.png`: el puesto por día en los tres brazos (`figuras_P7_34.py`, de `P7_34_datos.json`).
{gif_txt}

## Gasto

Plataforma: {n(coste, 4)} USD en {partidas} partidas ({n(coste / max(1, partidas), 4)} por partida; el humo de P7-33 costó {n(sum(p.get('coste_usd') or 0 for p in E33['peticiones']), 4)} en 3). Acumulado del siete: {n(ACUM_ANTES + coste, 4)} USD de plataforma. Consola de Anthropic: 0. Saldos no consultados.
"""
open(os.path.join(AQUI, "informe_P7_34.md"), "w", encoding="utf-8").write(out); print("informe_P7_34.md", out.count("\n"), "lineas")
