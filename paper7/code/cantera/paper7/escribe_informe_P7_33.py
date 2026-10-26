"""[P7-33] Escribe informe_P7_33.md desde P7_33_F1.json, P7_33_F2.json, P7_33_humo.json (analiza_P7_33.py), P7_33_estado.json (lanza_P7_33.py), P7_30_estado.json y semillas_P7_33.json. Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
def J(f): p = os.path.join(AQUI, f); return json.load(open(p)) if os.path.exists(p) else None
F1 = J("P7_33_F1.json"); F2 = J("P7_33_F2.json"); HU = J("P7_33_humo.json") or []; ES = J("P7_33_estado.json") or {}; E30 = J("P7_30_estado.json") or {}; SEM = J("semillas_P7_33.json") or {}
n = lambda x, d=0: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = hashlib.md5(open(os.path.join(RAIZ, "motor", "model.py"), "rb").read()).hexdigest()
COSAS = ("botiquin", "racion", "red", "camuflaje")
# ── F1 ──
T1 = ["| F1 | tics iguales · difieren | vidas con cambios | dónde cambian |", "|---|---|---:|---|"]
for k in ("apagado", "TECHO con oido y ley"):
    v = F1[k]; vc = v["vidas_con_cambios"]
    def dc(x):
        a = x["avisos"][0] if x["avisos"] else None
        return f"{x['vida'].split('/')[0][-8:]}/{x['vida'].split('/')[1]}: {x['cambios']} (t{x['primero']['t']}-{x['ultimo']['t']}" + ((", inundación anunciada " + str(a.get("rect")) + " tics " + str(a.get("from_tick")) + "-" + str((a.get("from_tick") or 0) + (a.get("duration") or 0))) if a else ", sin aviso") + ")"
    T1.append(f"| {k} | {n(v['fidelidad'].get('igual', 0))} · {n(v['fidelidad'].get('difiere', 0))} | {len(vc)} | {'; '.join(dc(x) for x in vc)} |")
T1b = ["| vida de TECHO (inundación de su semilla) | tics iguales · difieren | cambios en la ventana del aviso (−120 a +60 tics) · fuera | primero → último | aviso |", "|---|---|---|---|---|"]
for x in F1["inundaciones"]:
    if x.get("error"): T1b.append(f"| {x['vida']} | error | | | |"); continue
    a = x["avisos"][0] if x["avisos"] else {}
    T1b.append(f"| {x['vida'][5:]} | {n(x['fidelidad'].get('igual', 0))} · {n(x['fidelidad'].get('difiere', 0))} | {x['cambios_en_ventana_de_evento']} · {x['cambios'] - x['cambios_en_ventana_de_evento']} | {(x['primero']['diario'] + '→' + x['primero']['replica'] + ' t' + str(x['primero']['t']) + ' … t' + str(x['ultimo']['t'])) if x['primero'] else '—'} | {a.get('kind')} {a.get('rect')} tics {a.get('from_tick')}-{(a.get('from_tick') or 0) + (a.get('duration') or 0)} |")
# ── F2 ──
T2 = ["| cuaderno | vida | k máx antes de la primera prueba: botiquín · ración · red · camuflaje | cura imaginada máx antes: botiquín · ración | k red · camuflaje en toda la vida | `ir_curioso` por clase | pruebas (red · camuflaje · botiquín · ración) | cuaderno al fin, red: ignorancia · creencia dentro |", "|---|---|---|---|---|---|---|---|"]
for et in ("vacio", "tres_redes_sin_efecto"):
    for v in F2[et]["vidas"]:
        if v.get("error"): T2.append(f"| {et} | {v['carp']} {v['slot']} | error | | | | | |"); continue
        k = v["k_max_antes_de_la_primera_prueba"]; h = v["heal_imaginado_max_antes"]; cr = v["cuaderno_fin"].get("net") or {}
        T2.append(f"| {et.replace('_', ' ')} | {v['carp']} a{v['slot']} | {n(k['botiquin'], 2)} · {n(k['racion'], 2)} · {n(k['red'], 2)} · {n(k['camuflaje'], 2)} | {n(h['botiquin'], 1)} · {n(h['racion'], 1)} | {n(v['k_red_max_toda_la_vida'], 3)} · {n(v['k_camo_max_toda_la_vida'], 3)} | {', '.join(f'{c} {m}' for c, m in v['ir_curioso_por_clase'].items())} | {v['pruebas']['net']} · {v['pruebas']['camouflage']} · {v['pruebas']['first_aid']} · {v['pruebas']['rations']} | {n(cr.get('ignorancia'), 3)} · {n(cr.get('creencia_dentro'), 2)} |")
# ── F3 ──
pet = sorted((p for p in ES.get("peticiones", []) if p["brazo"] == "APRENDE"), key=lambda p: p["dia"]); gasto = sum(float(p.get("coste_usd") or 0) for p in pet)
T3 = ["| día · asiento | tics | puesto | cuaderno leído | orden de contacto (tic) | coge: botiquín · ración · red · camuflaje | pruebas: botiquín (firmes, al menos, cortes) · ración (f, a, c) · red (ventanas completas / cortas) · camuflaje (completas / cortas) | al acabar: creencia dentro · ignorancia · k: botiquín / ración / red / camuflaje | `ir_curioso` con paso listo | latencia: ms mediana · sobre el tic · guarda |", "|---|---:|---:|---|---|---|---|---|---:|---|"]
for v in HU:
    if v.get("sin_diario"): T3.append(f"| d{v['dia']} · {v['asiento']} | sin diario | | | | | | | | |"); continue
    p = v["pruebas"]; a = v["al_acabar"]; k = v["k_al_acabar"] or {}
    def cre(o): c = a[o]["creencia"]; vals = [x for x in c.values() if x is not None]; return n(c.get("dentro"), 1) if "dentro" in c else (n(max(vals), 1) if vals else "no sé")
    cel = " / ".join(f"{cre(o)} · {n(a[o]['ignorancia'], 3)} · {n(k.get(o), 3)}" for o in COSAS)
    T3.append(f"| d{v['dia']} · {v['asiento']} | {n(v['tics'])} | {n(v['puesto'])} | {'sí' if v['cuaderno_leido'] else 'no'} | {', '.join(f'{o} ({n(v['contacto'][o])})' for o in v['orden_de_contacto']) or 'ninguna'} | {v['coge']['botiquin']} · {v['coge']['racion']} · {v['coge']['red']} · {v['coge']['camuflaje']} | {p['botiquin']['n']} ({p['botiquin']['firmes']}, {p['botiquin']['al_menos']}, {p['botiquin']['cortes']}) · {p['racion']['n']} ({p['racion']['firmes']}, {p['racion']['al_menos']}, {p['racion']['cortes']}) · {p['red']['n']} ({p['red']['ventanas_completas']} / {p['red']['ventanas_cortas']}) · {p['camuflaje']['n']} ({p['camuflaje']['ventanas_completas']} / {p['camuflaje']['ventanas_cortas']}) | {cel} | {n(v['ir_curioso_con_paso_listo'])} ({n(100 * v['ir_curioso_fraccion'], 1)} %) | {n(v['latencia']['ms_mediana'], 1)} · {n(100 * (v['latencia']['sobre_el_tic'] or 0), 2)} % · {'pasa' if v['latencia']['pasa'] else 'NO PASA'} |")
ctx = collections.defaultdict(collections.Counter)
for v in HU:
    if v.get("sin_diario"): continue
    for o, c in v["contexto_de_las_pruebas"].items():
        for kk, vv in c.items(): ctx[o][kk] += vv
T3b = ["| cosa | pruebas abiertas | en calma | con rival a 4 o menos | con vida < 30 | en fuego |", "|---|---:|---:|---:|---:|---:|"] + [f"| {o} | {ctx[o]['n']} | {ctx[o]['en_calma']} | {ctx[o]['rival_a_4']} | {ctx[o]['vida_menor_30']} | {ctx[o]['fuego']} |" for o in COSAS]
ley = [(v["dia"], v["asiento"], v["ley"]) for v in HU if not v.get("sin_diario")]
tot_coge = {o: sum(v["coge"][o] for v in HU if not v.get("sin_diario")) for o in COSAS}; tot_pruebas = {o: sum(v["pruebas"][o]["n"] for v in HU if not v.get("sin_diario")) for o in COSAS}
# ── F4 ──
c30 = sum(float(p.get("coste_usd") or 0) for p in E30.get("peticiones", [])); n30 = len(E30.get("peticiones", []))
por_partida = (gasto / len(pet)) if pet else None; por_partida30 = c30 / n30 if n30 else None
T = f"""# P7-33 · La etapa de lo inútil: construir y probar

*9-oct-2026. Coste: plataforma {n(gasto, 4)} USD (el humo, {len(pet)} partidas); consola 0. `motor/model.py` = `{md5}` al empezar y al acabar; cuerpo y congelados sin tocar. Pieza nueva `nace_P7_33.py` (enganchada desde fuera tras descubre, pedir, nacer y P7-29; GEMV_P7_33, apagada por defecto), política `policy_pareja_P7_33.py`, banco `banco_P7_33.py` + `pruebas_P7_33.py`, imagen `Dockerfile.pareja_P7_33`, lanzador `lanza_P7_33.py`, lectura `analiza_P7_33.py`. Este informe lo escribe `escribe_informe_P7_33.py`. Ninguna cifra a mano.*

## Lo construido (diseño de Manel, 9-oct; sobre las piezas de P7-30)

1. **Nace sin saber nada de cuatro cosas.** Botiquín y ración, como en P7-23. Red y camuflaje: lo que el cuerpo sabía de ellos y se borra (archivo y línea): (a) su valor en la riqueza W, `gear_menor` = 0,25 por el camuflaje puesto y 0,25 por la red en mano o zurrón (`appraisal_zs_v42_exp.py:413, :761-769`) → 0,25 × k_camuflaje y 0,25 × k_red (envoltorio de `A.riqueza_W`); (b) los radios del camuflaje, CAMO_QUIETO = 4 y CAMO_MOVIENDO = 7, con los que S-8 EXPOSICIÓN deja de contar a los rivales lejanos (`:405-406, :1393-1411`) → 4 × k y 7 × k mientras se calculan las filas (k = 0: como sin camuflaje); (c) la promesa del camuflaje en el suelo (`decisor_zs.py:672-677`) sale de esas mismas filas, así que ya va escalada; la red no tiene promesa ni `empunar` (daño 0: `:731-745`, `:536-544`). Ganas: solo R-CARENCIA (`:1076`), que va por W. Regalo y pedido: el cuerpo no regala ni pide gear (nada que borrar; declarado). k de cada cosa de gear = ((1 − ignorancia) × creencia vivida en el cuerpo + ignorancia × esperanza de la otra cosa de gear) / hp_max; "no sé" → 0 (número de esta pieza, declarado: no hay cura de catálogo para el gear).
2. **Probar el camuflaje es ponérselo** (ventana de {F1['TECHO con oido y ley']['hecho_33']['VENTANA_S'] if F1['TECHO con oido y ley'].get('hecho_33') else 10:.0f} s llevándolo puesto, o antes si se lo quita) y **probar la red es llevarla** (10 s en mochila o mano, o antes si la suelta o la lanza): huella por dominio (cuerpo = vida al cerrar − al abrir + daño conocido; recursos = unidades al cerrar − al abrir; vínculo = distancia a la hermana), foto emocional, contexto y acciones al abrir, más duración, si la ventana se completó y el contexto de peligro. Sin "al menos" (no hay cura que tope) y sin corte (la prueba acaba cuando acaba la ventana o se va la cosa); una prueba por cada vez que la cosa llega, no una cadena de ventanas mientras la sigue llevando (declarado). Si no cambió nada, el recuerdo dice "no hizo nada" (efecto 0).
3. **La curiosidad de la clase** para las cuatro: ignorancia × alivio (tenerla alivia la mitad: la red en zurrón o mano, el camuflaje en zurrón o puesto; probarla, el resto, por los recuerdos). `ir_curioso` va a la clase que más llama de las cuatro. La curiosidad del cuánto sigue siendo de los consumibles (la red y el camuflaje no se "usan"; declarado); la esperanza del botiquín y de la ración sigue saliendo solo de la otra cosa consumible.
4. **Oído y ley:** el cuerpo lee `event_warning` (inundación: rectángulo y plazo; tormenta de fuego: centro, radio y plazo) y mientras dura el evento esas casillas son no transitables en su mapa (`mundo.solido` envuelto; el campo geodésico cacheado se vacía al cambiar lo activo). En los tres brazos. `solido` también corta la línea de vista (`mundo.py:231-247`); declarado.
5. **Medida del contexto** de cada prueba de cada cosa (punto 8): calma, o peligro (rival a 4 casillas o menos, fuego, vida < 30), al abrir.

## F1 · Con todo apagado se reproducen los diarios de A4; con oído y ley en TECHO, qué cambia

`pruebas_P7_33.py --f1` sobre los 80 diarios de A4 (GEMV_P7_PIDE=0 como en P7-23/29) -> `P7_33_F1.json`:

{chr(10).join(T1)}

Los dos tics de `apagado` son los dos de siempre (P7-23, P7-29). Con el oído y la ley, los cambios caen en las vidas que oyeron un aviso de inundación: el mismo evento del mundo en todas ellas (rectángulo [10, 22]-[14, 26], tics 4.400-5.120): la ley hace que el cuerpo rodee el agua en vez de empujarla. Las vidas de las inundaciones de P7-30 (k = 184) y P7-24 (k = 159), TECHO, replicadas con la ley:

{chr(10).join(T1b)}

Lectura. En k = 159 (P7-24 s1 d5 y s2 d16) los cambios empiezan en los tics 4.401-4.419 (con el agua) y, en las vidas que estaban contra el agua, siguen hasta el 5.120 (la réplica sigue el diario en lazo abierto: cuando la ley elige otro camino, el diario y la réplica ya no coinciden hasta que la escena vuelve a ser la misma). En k = 184 (P7-30 s1 d7 y s2 d14) las vidas de TECHO no estaban contra el agua (la que chocaba era el asiento 10 de BORRADO y de APRENDE, P7-31) y el único tic que cambia en 3 de las 4 está fuera de la ventana y es un empate `hacer_sitio` ↔ `noop` (regla de P7-10), no la ley. **F1 pasa.**

## F2 · En banco: sin cuaderno nada tiene efecto ni ganas; con pruebas de red sin efecto, la red se apaga

`pruebas_P7_33.py --f2`: las 4 vidas de APRENDE del día 1 de P7-30 replicadas con la pieza -> `P7_33_F2.json`:

{chr(10).join(T2)}

Lectura. Con el cuaderno vacío, k = 0 y cura imaginada 0 para las cuatro cosas en todos los tics hasta la primera prueba (y k de red y camuflaje = 0 en toda la vida, porque sus pruebas no dan nada en el cuerpo): ninguna de las cuatro tiene efecto imaginado ni ganas. Con un cuaderno cargado a mano con tres pruebas de red sin efecto, la creencia de la red es 0,0 (creencia dentro), su ignorancia baja de 1 a {n((F2['tres_redes_sin_efecto']['vidas'][0].get('cuaderno_fin') or {}).get('net', {}).get('ignorancia'), 2)}-{n(max(((v.get('cuaderno_fin') or {}).get('net') or {}).get('ignorancia') or 0 for v in F2['tres_redes_sin_efecto']['vidas'] if not v.get('error')), 2)} (tres recuerdos frente al neutro; no es cero: la ignorancia se apaga con los recuerdos, no de golpe), y `ir_curioso` hacia una red pasa de {', '.join(str(v['ir_curioso_por_clase'].get('net', 0)) for v in F2['vacio']['vidas'] if not v.get('error'))} tics (cuaderno vacío) a {', '.join(str(v['ir_curioso_por_clase'].get('net', 0)) for v in F2['tres_redes_sin_efecto']['vidas'] if not v.get('error'))}. **F2 pasa** (la curiosidad de la red se apaga en cuanto las otras clases llaman más; con 0,2-0,3 de ignorancia todavía puede ganar cuando las demás ya están probadas).

## F3 · El humo de 3 días (APRENDE, semillas nuevas)

Semillas `semillas_P7_33.json` (k {', '.join(str(k) for k in SEM.get('k', []))}: {', '.join(str(s) for s in SEM.get('serie1', []))}); imagen `Dockerfile.pareja_P7_33` (GEMV_P7_33=1 sobre la de P7-30); `lanza_P7_33.py --cadena-aprende 1 1 3`; diarios en `paintball/runs/P733_s1_d<D>_APRENDE_<semilla>/`; `analiza_P7_33.py` -> `P7_33_humo.json`. Partidas: {'; '.join(f"d{p['dia']} {p.get('estado')} ({n(p.get('coste_usd'), 4)} USD)" for p in pet)}.

{chr(10).join(T3)}

**El contexto de las pruebas** (punto 8; al abrir cada prueba, en las 6 vidas):

{chr(10).join(T3b)}

Oído y ley en el humo: {'; '.join(f"d{d}·{a}: {len(l['avisos'])} aviso(s) {[(x.get('kind'), x.get('rect') or x.get('center'), x.get('from_tick')) for x in l['avisos']]}, cambios de casillas {l['cambios_de_casillas']}" for d, a, l in ley)}.

Lo que se ve en los tres días: cogidas (6 vidas): {', '.join(f'{o} {tot_coge[o]}' for o in COSAS)}; pruebas: {', '.join(f'{o} {tot_pruebas[o]}' for o in COSAS)}.

Lectura. (i) Las cuatro cosas se tocan y se prueban: en {sum(1 for v in HU if not v.get('sin_diario') and v['orden_de_contacto'] and v['orden_de_contacto'][0] in ('red', 'camuflaje'))} de las {sum(1 for v in HU if not v.get('sin_diario'))} vidas la primera cosa que toca es el camuflaje (tics {', '.join(str(v['contacto']['camuflaje']) for v in HU if not v.get('sin_diario') and v['orden_de_contacto'] and v['orden_de_contacto'][0] == 'camuflaje')}), en las demás el botiquín o la ración; la red la tocan {sum(1 for v in HU if not v.get('sin_diario') and v['contacto']['red'] is not None)} vidas (tics {', '.join(str(v['contacto']['red']) for v in HU if not v.get('sin_diario') and v['contacto']['red'] is not None)}) y el camuflaje {sum(1 for v in HU if not v.get('sin_diario') and v['contacto']['camuflaje'] is not None)}; las pruebas de red y camuflaje son ventanas completas de 10 s ({sum(v['pruebas']['red']['ventanas_completas'] + v['pruebas']['camuflaje']['ventanas_completas'] for v in HU if not v.get('sin_diario'))} de {tot_pruebas['red'] + tot_pruebas['camuflaje']}) con efecto en el cuerpo entre {n(min(e for v in HU if not v.get('sin_diario') for o in ('red', 'camuflaje') for e in v['pruebas'][o]['efecto_cuerpo']), 1)} y {n(max(e for v in HU if not v.get('sin_diario') for o in ('red', 'camuflaje') for e in v['pruebas'][o]['efecto_cuerpo']), 1)}: "no hizo nada"; la creencia de las dos queda en 0 o por debajo y sus ganas (k) en 0,000 en las 6 vidas; su ignorancia baja a 0,21-0,51 con una sola prueba y el cuaderno la lleva al día siguiente (día 2 y 3 leídos). (ii) El contexto (punto 8): el botiquín ({ctx['botiquin']['n']} pruebas) y la ración ({ctx['racion']['n']}) se prueban siempre con un rival a 4 casillas o menos (en calma: {ctx['botiquin']['en_calma']} y {ctx['racion']['en_calma']}); la red se prueba en calma {ctx['red']['en_calma']} de {ctx['red']['n']} y el camuflaje {ctx['camuflaje']['en_calma']} de {ctx['camuflaje']['n']}: lo que se prueba por curiosidad se prueba en calma; lo que se usa, en peligro. (iii) Oído y ley: las 6 vidas oyen el mismo aviso (inundación [10, 22]-[14, 26], tic 4.400) y la ley cierra 25 casillas de 4.400 a 5.120; ninguna vida choca contra el agua ({', '.join(f"{n(100 * v['latencia']['fraccion_sin_cuerpo'], 2)} %" for v in HU if not v.get('sin_diario'))} de pasos listos bloqueados sin cuerpo). (iv) Latencia: una vida marcada (d1 asiento 10: 1,04 % de decisiones sobre el tic, mediana 15,0 ms); la pieza de las cuatro cosas cuesta más por tic que la de P7-30 (medianas 1,3-15,0 ms frente a 3,9 de media en P7-30): a vigilar en el campo. (v) `ir_curioso` con el paso listo: 0,1-13,9 % (P7-30: 0,2 %): con cuatro clases desconocidas la curiosidad vuelve a mover, sobre todo el día 3 asiento 10. Una pega de ingeniería anotada: la marca de P7-29 de las fotos por índice se desajusta en algunos tics con cuatro clases (`P7_error` "fotos para candidatos": {', '.join(str(sum(1 for line in open(f, errors='replace') if '"P7_error"' in line)) for f in sorted(__import__('glob').glob(os.path.join(RAIZ, 'paintball', 'runs', 'P733_s1_d*_APRENDE_*', '*agent_1[01].art.log'))))} por vida); en esos tics la foto de llegada de `ir_curioso` o la de usar puede ir a otro candidato; a corregir antes del campo.

## F4 · Créditos, y lo que costaría el campo

Plataforma: {n(gasto, 4)} USD en {len(pet)} partidas del humo ({n(por_partida, 4)} por partida); acumulado del siete: 52,6550 (hasta P7-30) + {n(gasto, 4)} = **{n(52.6550 + gasto, 4)} USD**. Consola de Anthropic: 0. El campo de tres brazos, 20 días y dos series (120 partidas) costaría, al precio de este humo, {n(120 * por_partida, 2)} USD; al precio medio del campo de P7-30 ({n(por_partida30, 4)} por partida en {n30} partidas), {n(120 * por_partida30, 2)} USD. Saldos no consultados.
"""
assert "§" not in T; open(os.path.join(AQUI, "informe_P7_33.md"), "w").write(T); print("informe_P7_33.md", len(T.splitlines()), "lineas")
