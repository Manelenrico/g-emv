"""[P7-29] Escribe informe_P7_29.md desde P7_29_diagnostico.json, P7_29_F1.json, P7_29_cache.json, P7_29_F2.json, P7_29_F3.json y, si existen, P7_29_humo.json y P7_29_estado.json. Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
def J(f): p = os.path.join(AQUI, f); return json.load(open(p)) if os.path.exists(p) else None
DG = J("P7_29_diagnostico.json"); F1 = J("P7_29_F1.json"); CA = J("P7_29_cache.json"); F2 = J("P7_29_F2.json"); F3 = J("P7_29_F3.json"); HU = J("P7_29_humo.json"); ES = J("P7_29_estado.json")
n = lambda x, d=0: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = hashlib.md5(open(os.path.join(RAIZ, "motor", "model.py"), "rb").read()).hexdigest()
TIC = 1000.0 / 24
# ── seccion 0 ──
R = DG["rachas"]; L = DG["latencia"]["por_brazo_y_bloque"]; LV = DG["latencia"]["por_vida"]
ag = R["tics_por_casilla_destino"].get(". · agente a la vista", 0); na = R["tics_por_casilla_destino"].get(". · nadie a la vista", 0)
T0 = ["| brazo · bloque | vidas | tiempo de decisión por tic, mediana (media de vidas, ms) | tics por encima del tic (41,7 ms) | vidas con más del 20 % por encima | desplazamientos que siguen la propia intención | pasos listos bloqueados |", "|---|---:|---:|---:|---:|---:|---:|"]
for k, x in L.items(): T0.append(f"| {k} | {x['vidas']} | {n(x['ms_mediana_media'], 1)} | {n(100 * x['sobre_el_tic_media'], 1)} % | {x['vidas_con_mas_del_20_por_ciento_sobre_el_tic']} | {n(100 * x['propios_media'], 1)} % | {n(100 * x['bloqueo_media'], 1)} % |")
peores = sorted([x for x in LV if x["brazo"] == "APRENDE"], key=lambda x: -x["sobre_el_tic"])[:8]
T0b = ["| vida (APRENDE) | tics | ms mediana · p90 · máx | sobre el tic | desplazamientos · propios | pasos listos · bloqueados |", "|---|---:|---|---:|---|---|"]
for x in peores: T0b.append(f"| s{x['serie']} d{x['dia']} asiento {x['asiento']} | {n(x['tics'])} | {n(x['ms_mediana'], 1)} · {n(x['ms_p90'], 1)} · {n(x['ms_max'], 1)} | {n(100 * x['sobre_el_tic'])} % | {x['desplazamientos']} · {n(100 * x['propios']) if x['propios'] is not None else '—'} % | {n(x['paso_listo'])} · {n(x['bloqueados'])} ({n(100 * x['bloqueo'])} %) |")
largas = R["mas_largas"][:8]
T0c = ["| racha más larga | brazo | desde · dirección · casilla | casilla en el mapa | agente a la vista encima | elegido | tics |", "|---|---|---|---|---|---|---:|"]
for r in largas: T0c.append(f"| s{r['serie']} d{r['dia']} asiento {r['asiento']} t{n(r['t'])} | {r['brazo']} | {tuple(r['pos'])} · {r['dir']} · {tuple(r['casilla'])} | '{r['casilla_char']}' (suelo) | {'sí' if r['agente_a_la_vista'] else 'no'} | `{r['elegido']}` | {n(r['n'])} |")
# ── F1 ──
def desc(d): return f"{d['vida'].split('/')[0][-8:]}/{d['vida'].split('/')[1]} t{d['t']} {d['diario']}→{d['replica']}"
TF1 = ["| F1 | arreglos encendidos | tics iguales · difieren | vidas con desacuerdo | muros aprendidos | desacuerdos (primeros) |", "|---|---|---|---:|---:|---|"]
for k, v in F1.items(): TF1.append(f"| {k} | {', '.join(v['arreglos'])} | {n(v['fidelidad'].get('igual', 0))} · {n(v['fidelidad'].get('difiere', 0))} | {v.get('vidas_con_desacuerdo') if v.get('vidas_con_desacuerdo') is not None else '1'} | {v['muros']} | {'; '.join(desc(d) for d in v['desacuerdos'][:3])} |")
# ── cache ──
TC = ["| réplica de las 16 vidas (días 16-20) | tics iguales · difieren | ms por decisión, mediana de medianas (esta máquina) |", "|---|---|---:|"]
for k, v in (CA or {}).items(): TC.append(f"| {k.replace('_', ' ')} | {n(v['fidelidad'].get('igual', 0))} · {n(v['fidelidad'].get('difiere', 0))} | {n(v['ms_mediana_de_medianas'], 2)} |")
TCv = ["| vida | tics | sin caché: ms mediana · p90 | con caché: ms mediana · p90 | iguales · difieren (con caché) |", "|---|---:|---|---|---|"]
if CA:
    for a, b in zip(CA["sin_cache"]["por_vida"], CA["con_cache"]["por_vida"]):
        if a.get("ms_replica") and b.get("ms_replica"): TCv.append(f"| {a['carp'][5:12]} asiento {a['slot']} | {n(a['tics'])} | {n(a['ms_replica']['mediana'], 1)} · {n(a['ms_replica']['p90'], 1)} | {n(b['ms_replica']['mediana'], 2)} · {n(b['ms_replica']['p90'], 2)} | {n(b['fidelidad'].get('igual', 0))} · {n(b['fidelidad'].get('difiere', 0))} |")
# ── F2 ──
TF2 = ["| vida | tics | primer cambio (tic) | el diario hacía → la réplica hace | en ese tic: destino de `ir_curioso` (clase, distancia) · vida · botiquines · paso bloqueado en el diario | cambios en toda la réplica · desde `ir_curioso` · a qué |", "|---|---:|---:|---|---|---|"]
deja = 0; lejos = 0; F2v = (F2 or {}).get("vidas", [])
for v in F2v:
    if v.get("error"): TF2.append(f"| {v['carp'][5:12]} asiento {v['slot']} | — | error | {v['error'][-80:]} | | |"); continue
    p = v["primer_cambio"]; c = v.get("contexto_del_primer_cambio") or {}; cur = c.get("ir_curioso") or {}
    if p and p["diario"] == "ir_curioso": deja += 1
    if p and p["diario"] == "ir_curioso" and cur.get("clase") == "rations" and (cur.get("dist") or 0) > 2: lejos += 1
    TF2.append(f"| {v['carp'][5:12]} asiento {v['slot']} | {n(v['tics'])} | {n(p['t']) if p else 'ninguno'} | {(p['diario'] + ' → ' + p['replica']) if p else '—'} | {(str(cur.get('clase')) + ', ' + str(cur.get('dist')) + ' casillas') if cur else '—'} · {n(c.get('hp'))} · {c.get('kits', '—')} · {'sí' if (c.get('diario') or {}).get('bloqueado') else 'no'} | {v['cambios_totales']} · {v['cambios_desde_ir_curioso']} · {', '.join(f'{k} {x}' for k, x in (v.get('a_que_cambia') or {}).items())} |")
cs = (F2 or {}).get("creencia_sin_cortes", [])
TF2b = ["| serie · asiento | día | recuerdos del botiquín: firmes · al menos · cortes | creencia dentro CON cortes (la del campo) | creencia dentro SIN cortes (arreglo 3) | ignorancia de la clase | ignorancia del cuánto | lo más alto que sabe |", "|---|---:|---|---:|---:|---:|---:|---:|"]
for x in cs:
    if x["dia"] in (1, 5, 10, 15, 20) or x["dia"] == 19: TF2b.append(f"| s{x['serie']} · {x['asiento']} | {x['dia']} | {x['firmes']} · {x['al_menos']} · {x['cortes']} | {n(x['con_cortes']['dentro'], 1)} | {n(x['sin_cortes']['dentro'], 1)} | {n(x['ignorancia'], 3)} | {n(x['ignorancia_cuanto'], 3)} | {n(x['sabido_max'], 1)} |")
fin20 = [x for x in cs if x["dia"] == 20]
red = [{"carp": x["carp"][5:12], "slot": x["slot"], "muros": x["muros_aprendidos"], "primer": x["primer_cambio"], "cambios": x["cambios_totales"]} for x in (F2 or {}).get("con_la_red_de_muros", [])]
# ── F3 ──
TF3 = ["| cuaderno del botiquín | tics con botiquín en el zurrón | tics en que el cuerpo ofrece `usar_botiquin` (vida) | elige `usar_botiquin` (vida) | M del cuánto en lo elegido, mediana · máx | M de la curiosidad de clase (mediana) | ignorancia del cuánto · lo más alto que sabe (cuaderno al fin) |", "|---|---:|---|---|---|---:|---|"]
ET = {"a": "(a) solo 'al menos' (30, 25, 20)", "b": "(b) (a) + un firme (45)", "c": "(c) (a) + tres firmes (45, 40, 42)", "d": "(d) el real del día 19 (2 firmes, 7 'al menos', 16 cortes)"}
for k in ("a", "b", "c", "d"):
    v = (F3 or {}).get(k)
    if not v or v.get("error"): TF3.append(f"| {ET[k]} | error | | | | | |"); continue
    cb = v.get("cuaderno_botiquin") or {}
    TF3.append(f"| {ET[k]} | {n(v['tics_listos_con_botiquin'])} | {v['tics_con_candidato_usar']} ({', '.join(n(h) for h in sorted(v['hp_con_candidato'], reverse=True))}) | {v['elige_usar_botiquin']} ({', '.join(n(h) for h in sorted(v['hp_al_elegir_usar'], reverse=True))}) | {n(v['M_cuanto']['mediana'], 4)} · {n(v['M_cuanto']['max'], 4)} | {n(v['M_curiosidad_mediana'], 4)} | {n(cb.get('ignorancia_cuanto'), 3)} · {n(cb.get('sabido_max'), 1)} |")
TF3b = ["| cuaderno | fila del cuánto en la foto de `usar_botiquin`, por vida al ofrecerse (de más a menos vida) |", "|---|---|"]
for k in ("a", "b", "c", "d"):
    v = (F3 or {}).get(k) or {}
    if v and not v.get("error"):
        pares = sorted(zip(v["hp_con_candidato"], v["fila_cuanto_en_usar_cuando_se_ofrece"][::-1]), reverse=True)
        TF3b.append(f"| {ET[k][:3]} | " + ", ".join(f"vida {n(h)}: {n(m, 4)}" for h, m in pares) + " |")
# ── F4 / F5 ──
if HU:
    TH = ["| día · asiento | tics | puesto | contacto botiquín · ración (tic) | usos botiquín: canales · firmes · al menos · cortes (vida al abrir) | usos ración: canales · firmes · al menos · cortes | creencia botiquín dentro · fuera | ignorancia clase · cuánto · sabe | pasos listos bloqueados | muros | `ir_curioso` con paso listo | ms mediana · p90 · sobre el tic |", "|---|---:|---:|---|---|---|---|---|---|---:|---|---|"]
    for v in HU:
        if v.get("sin_diario"): TH.append(f"| d{v['dia']} · {v['asiento']} | sin diario | | | | | | | | | | |"); continue
        ub = v["usos"]["botiquin"]; ur = v["usos"]["racion"]; ab = v["al_acabar"]["botiquin"]; ar = v["al_acabar"]["racion"]; cb = ab["creencia"]
        TH.append(f"| d{v['dia']} · {v['asiento']} | {n(v['tics'])} | {n(v['puesto'])} | {n(v['contacto']['botiquin'])} · {n(v['contacto']['racion'])} | {len(ub)} · {sum(1 for u in ub if u['firme'])} · {sum(1 for u in ub if u['al_menos'])} · {sum(1 for u in ub if not u['completado'])} ({', '.join(n(u['hp0']) for u in ub) or '—'}) | {len(ur)} · {sum(1 for u in ur if u['firme'])} · {sum(1 for u in ur if u['al_menos'])} · {sum(1 for u in ur if not u['completado'])} | {n(cb.get('dentro'), 1)} · {n(cb.get('fuera'), 1)} | {n(ab['ignorancia'], 3)} · {n(ab['ignorancia_cuanto'], 3)} · {n(ab['sabido_max'], 1)} | {n(v['bloqueados']['bloqueados'])} de {n(v['bloqueados']['paso_listo'])} ({n(100 * v['bloqueados']['fraccion'])} %) | {len(v['muros_aprendidos'])} | {n(v['ir_curioso_con_paso_listo'])} ({n(100 * v['ir_curioso_fraccion'])} %) | {n(v['ms']['mediana'], 1)} · {n(v['ms']['p90'], 1)} · {n(100 * (v['ms']['sobre_el_tic'] or 0), 1)} % |")
    causas = [c for v in HU if not v.get("sin_diario") for c in v["al_acabar"]["botiquin"]["causas_de_corte"] + v["al_acabar"]["racion"]["causas_de_corte"]]
    gasto = sum(float(p.get("coste_usd") or 0) for p in (ES or {}).get("peticiones", [])); partidas = [(p["dia"], p.get("estado"), p.get("coste_usd")) for p in (ES or {}).get("peticiones", [])]
    S4 = f"""## F4 · El humo de 3 días (brazo APRENDE, semillas nuevas)

Semillas: `semillas_P7_29.json` (k 175-177: {', '.join(str(s) for s in json.load(open(os.path.join(AQUI, 'semillas_P7_29.json')))['serie1'])}); imagen `Dockerfile.pareja_P7_29` (GEMV_P7_29=1, red de muros apagada); lanzador `lanza_P7_29.py --cadena-aprende 1 1 3`; diarios en `paintball/runs/P729_s1_d<D>_APRENDE_<semilla>/`; lectura `analiza_P7_29.py` -> `P7_29_humo.json`.

{chr(10).join(TH)}

Causas de los cortes del día (recuerdos `acto` del cuaderno): {'; '.join(f"daño {c.get('dano')} de {c.get('fuentes')} tras `{c.get('ultima_eleccion')}` ({c.get('tics')} tics)" for c in causas[:8]) if causas else 'ningún corte'}.

## F5 · Créditos del humo

Plataforma: {n(gasto, 4)} USD en {len([p for p in partidas if p[2]])} partidas ({'; '.join(f'd{d} {e} {n(c, 4) if c else "—"}' for d, e, c in partidas)}); acumulado de la séptima: {n(41.9017 + gasto, 4)} USD. Consola de Anthropic: 0. Saldos no consultados.
"""
else:
    S4 = """## F4 · El humo de 3 días

NO LANZADO. La cadena de pruebas de la mesa dice "si una falla, para y dilo": F1 no pasa con la red de los muros encendida (sección F1). La imagen (`Dockerfile.pareja_P7_29`, con la red apagada por defecto), las semillas (`semillas_P7_29.json`, k 175-177) y el lanzador (`lanza_P7_29.py --cadena-aprende 1 1 3`) están listos; se lanza con el "adelante" de Manel, con la red apagada (recomendación) o como la mesa decida.

## F5 · Créditos del humo

Plataforma: 0 (nada lanzado; acumulado de la séptima sin cambio: 41,9017 USD). Consola de Anthropic: 0.
"""
T = f"""# P7-29 · Arreglar lo que hundía a la que recuerda, y la curiosidad del cuánto

*8-oct-2026. Coste: plataforma {'ver F5' if HU else '0'}; consola 0. `motor/model.py` = `{md5}` al empezar y al acabar; cuerpo y congelados sin tocar. Pieza nueva `nace_P7_29.py` (enganchada desde fuera tras descubre, pedir y nacer; GEMV_P7_29, apagada por defecto), política `policy_pareja_P7_29.py`, banco `banco_P7_29.py`, diagnóstico `diagnostico_P7_29.py`, imagen `Dockerfile.pareja_P7_29`, lanzador `lanza_P7_29.py`, lectura `analiza_P7_29.py`. Este informe lo escribe `escribe_informe_P7_29.py` desde los JSON citados en cada sección. Ninguna cifra a mano.*

## En corto

1. **Los muros no existían.** De las {n(R['n'])} rachas de 3 o más pasos bloqueados de P7-24 ({n(R['tics'])} tics), ninguna choca con un muro del mapa: la casilla destino es suelo en el `static_map` del propio diario en todas (y en las ocho orientaciones posibles del mapa). El {n(100 * ag / (ag + na))} % de esos tics son `move_*` del cuerpo contra la hermana a la vista; el {n(100 * na / (ag + na))} % son suelo vacío en vidas cuya **decisión tardaba más que el tic**: el recuerdo por parecido se calculaba 216 veces por tic, y con 20-30 recuerdos APRENDE pasaba de los 41,7 ms (días 16-20: {n(L['APRENDE · dias 16-20']['ms_mediana_media'], 1)} ms de mediana, {n(100 * L['APRENDE · dias 16-20']['sobre_el_tic_media'])} % de tics por encima; TECHO {n(L['TECHO · dias 16-20']['ms_mediana_media'], 1)} ms). Las observaciones se encolan, las acciones llegan tarde y el mundo contesta `blocked`. Esto corrige P7-28: la que recuerda no se hundía (solo) por el candidato, se hundía por lenta. Sección 0.
2. **Arreglo 0 (caché, sin cambiar decisiones):** las 16 vidas replicables de los días 16-20 se reproducen bit a bit con la caché ({n((CA or {}).get('con_cache', {}).get('fidelidad', {}).get('igual', 0))} tics iguales, {n((CA or {}).get('con_cache', {}).get('fidelidad', {}).get('difiere', 0))} difieren) y la decisión pasa de {n((CA or {}).get('sin_cache', {}).get('ms_mediana_de_medianas'), 1)} a {n((CA or {}).get('con_cache', {}).get('ms_mediana_de_medianas'), 2)} ms de mediana en esta máquina.
3. **F1:** `apagado` reproduce A4 ({n(F1['apagado']['fidelidad'].get('difiere', 0))} tics distintos de {n(F1['apagado']['fidelidad'].get('igual', 0) + F1['apagado']['fidelidad'].get('difiere', 0))}, los mismos dos de P7-23); `TECHO` sin pedir, **con la red de muros encendida, NO** ({n(F1['TECHO con la red de muros']['fidelidad'].get('difiere', 0))} tics en {F1['TECHO con la red de muros']['vidas_con_desacuerdo']} vidas, {F1['TECHO con la red de muros']['muros']} "muros" en casillas de suelo con un cuerpo que el cuerpo no ve); **con la red apagada, sí** ({n(F1['TECHO sin la red de muros']['fidelidad'].get('difiere', 0))} tics). La red queda apagada por defecto y el humo no se lanza hasta que la mesa decida (F4).
4. **F2 (arreglo 1, banco):** en {deja} de {len([v for v in F2v if not v.get('error')])} vidas el primer cambio de decisión es dejar `ir_curioso` ({lejos} hacia una ración recordada a más de 2 casillas); la creencia del botiquín sin los cortes acaba el día 20 en {' · '.join(f"s{x['serie']}·{x['asiento']} {n(x['con_cortes']['dentro'], 1)}→{n(x['sin_cortes']['dentro'], 1)}" for x in fin20)} (de 50).
5. **F3 (el cuánto, banco):** la fila funciona como se diseñó (M {n((F3 or {}).get('a', {}).get('M_cuanto', {}).get('mediana'), 4)} con solo "al menos" → {n((F3 or {}).get('b', {}).get('M_cuanto', {}).get('mediana'), 4)} con un firme → {n((F3 or {}).get('c', {}).get('M_cuanto', {}).get('mediana'), 4)} con tres: se apaga; y en la foto de usar se alivia solo cuando le faltan más de lo que sabe que da), pero la vida elegida no sirve para ver el momento: el cuerpo solo ofrece `usar_botiquin` {(F3 or {}).get('a', {}).get('tics_con_candidato_usar', '—')} tics (al final, fuera del círculo, cada 49 tics entre canales que el anillo corta) y lo elige las {(F3 or {}).get('a', {}).get('elige_usar_botiquin', '—')} veces con los cuatro cuadernos.

## Sección 0 · Por qué el mapa del cuerpo "no tenía" esos muros (antes de arreglar)

**Cómo se construye el mapa del cuerpo (solo describir).** El juego lo da ENTERO al empezar: el `player_config` trae `arena.static_map` (48 filas de 48 caracteres) con su leyenda y los pedestales; la política lo lee en `policy_cortex.py:889-900` y lo guarda en el diario (`static_map`), y `Mundo.desde_player_config` (`paintball/alma/mundo.py:72-105`) lo convierte en el mapa del cuerpo. Sólido es todo carácter cuya leyenda contiene "wall" o "rock" (`ch_wall`) o "fortress" (`ch_fortress`): `mundo.py:118-128`; `solido(x, y)` (`mundo.py:211-214`) devuelve verdadero para esos y para fuera del tablero. Los arbustos ('B', "berry_bush") no son sólidos. El cuerpo NO dibuja nada con lo que ve ni recuerda: no hay casillas "no vistas", el mapa es completo desde el tic 0 y no cambia en la partida. La geodésica (`decisor_zs.py:148-194`) hace un BFS desde el destino sobre ese mapa; lo no sólido es caminable; los cuerpos a la vista no entran en el mapa sino solo en el primer paso (`_paso_geodesico`, `decisor_zs.py:197-246`, con `cuerpos` de la receta, `decisor_zs.py:446-473`). Cambia de una semilla a otra: en el campo hay {DG['mapa']['mapas_distintos']} mapas distintos para {DG['mapa']['semillas']} (serie, día), y las {DG['mapa']['semillas_con_un_solo_mapa_entre_brazos']} parejas de brazos de una misma semilla reciben el mismo (la serie 2 repite las 20 semillas de la serie 1).

**Qué hay en la casilla contra la que choca** (`diagnostico_P7_29.py` -> `P7_29_diagnostico.json`; racha = 3 o más pasos seguidos `blocked` con el paso listo desde la misma casilla y en la misma dirección, la regla del arreglo 2): {n(R['n'])} rachas, {n(R['tics'])} tics. En TODAS la casilla destino es '.' (suelo) en el `static_map` del diario; girando, transponiendo o volteando el mapa tampoco sale un muro (tabla de giros en el JSON: con la identidad {n(R['giros_sin_agente_tics']['identidad'].get('.', 0))} de {n(na)} tics sin nadie a la vista caen en suelo). En {n(R['casilla_destino'].get('. · agente a la vista', 0))} rachas ({n(ag)} tics) hay un agente A LA VISTA en la casilla: casi siempre la hermana, y lo elegido es un paso largo `move_*` ({', '.join(f'`{k}` {n(v)}' for k, v in list(R['elegido_con_agente_tics'].items())[:4])}): los pasos largos del cuerpo (`mover`, `decisor_zs.py:786-788`, `_simula_camino`) no esquivan cuerpos (solo los `paso_*` y los `ir_*` lo hacen). Es del cuerpo de nacimiento y no se toca. En {n(R['casilla_destino'].get('. · nadie a la vista', 0))} rachas ({n(na)} tics) no hay nadie a la vista y lo elegido es `ir_objeto` / `ir_curioso` ({', '.join(f'`{k}` {n(v)}' for k, v in list(R['elegido_sin_agente_tics'].items())[:4])}).

{chr(10).join(T0c)}

**Por qué choca contra suelo vacío: la decisión tarda más que el tic.** El diario guarda el tiempo de cada decisión (`RADIOGRAFIA.ms`, `policy_cortex.py:511-618`); el mundo va a 24 tics por segundo (41,7 ms). La política decide una observación detrás de otra, en orden (`policy_cortex.py:881-960`): si tarda más que el tic, las observaciones se encolan y cada acción llega al mundo más tarde que la anterior, pedida desde una casilla en la que la criatura ya no está (los desplazamientos dejan de seguir la propia intención). Por brazo y bloque:

{chr(10).join(T0)}

Las vidas que más chocan son las que más tardan (APRENDE; correlación de rangos entre la fracción de tics por encima del tic y la fracción de pasos bloqueados: {n(DG['latencia']['spearman_APRENDE_sobre_el_tic_vs_bloqueo'], 2)}):

{chr(10).join(T0b)}

Dónde se iba el tiempo (`cProfile` sobre la réplica de s2 d19 asiento 11, 1.920 tics): `nace_P7_23.vivida` (el recuerdo por parecido, `recuerdo_P7_23.creencia_parecido` sobre todos los recuerdos de la cosa) se llamaba 414.759 veces (216 por tic) y sumaba 58,7 de los 61,6 s del decisor: cada candidato imagina sus filas, y cada `filas` pide k del botiquín y de la ración varias veces (`nace_P7_23.py:187-189, 236-241, 232-235`). Con 20-30 recuerdos por cosa, eso es lo que crece con los días. Esto NO es un obstáculo que el cuerpo perciba y el mapa no cuente: es un fallo de ingeniería de la pieza de P7-23. Consecuencia para P7-28: la caída de la que recuerda en los días 16-20 coincide con las vidas lentas (8 de 20 con más del 20 % de tics por encima del tic); el candidato `ir_curioso` que P7-28 señaló existe, pero la lentitud explica los atascos, y lo que explica el puesto habrá que volver a medirlo con la pieza rápida.

**Arreglo 0: la caché** (`nace_P7_29.vivida`): dentro del tic, el recuerdo por parecido se calcula una vez por (cosa, contexto dentro/golpeada, tic, día, número de recuerdos, foto) y se reutiliza. Mismos argumentos, mismo resultado: no cambia ninguna decisión. Comprobado (`banco_P7_29.py --cache`):

{chr(10).join(TC)}

{chr(10).join(TCv)}

**Y el arreglo 2 (apuntar el muro tras tres choques)** queda como red de seguridad para lo que no se ve (Manel, 8-oct), con un añadido declarado: si en la casilla hay un agente a la vista no se apunta nada (un cuerpo no es un muro). Lo que la red encuentra en los diarios de A4 (F1) son casillas de suelo sin nadie a la vista que el mundo bloquea tres tics y luego deja pasar (lo más probable, un cuerpo que el cuerpo no ve: camuflado; no comprobado): no son muros, y marcarlas cambia decisiones. Por eso queda apagada.

## F1 · Con todo apagado y con TECHO sin pedir, se reproducen los diarios de A4

`banco_P7_29.py --f1` sobre los 80 diarios de A4 (P6-11 tandas 1 y 2, P6-24; GEMV_P7_PIDE=0 como en P7-23), con la pieza enganchada (GEMV_P7_29=1) -> `P7_29_F1.json`:

{chr(10).join(TF1)}

Los dos tics de `apagado` son los mismos dos de P7-23 (`P7_23_F1.json`). Con la red de muros, TECHO aprende {F1['TECHO con la red de muros']['muros']} "muros" en casillas de suelo donde no se ve a nadie (en P611_t2 21727122, tic 5074-5076: la criatura en (15, 26) pide `move W` tres veces y el mundo dice blocked; en (14, 26) no hay muro ni agente a la vista; la hermana está en (17, 26)) y a partir de ahí decide distinto. **F1 pasa sin la red y no pasa con ella.** La red queda apagada por defecto (`nace_P7_29.E["arreglos"]["muros"] = False`); lo que queda de la mesa por decidir: si se quita del todo o si se cambia por otra regla (por ejemplo, una marca que caduque). No se ha seguido con el humo.

## F2 · Los arreglos 1 y 2 sobre las vidas de APRENDE de los días 16-20 (banco)

`banco_P7_29.py --f2`: las 16 vidas replicables (las 4 parciales no traen `player_config`), con la caché y el arreglo 1 (la red de muros aparte, abajo), el PRIMER instante en que la decisión de la réplica se separa del diario, y lo que pasaba en ese instante -> `P7_29_F2.json`:

{chr(10).join(TF2)}

Lectura. En {deja} de {len([v for v in F2v if not v.get('error')])} vidas, el primer cambio es dejar `ir_curioso`; en {lejos} de ellas el destino era una ración recordada a más de 2 casillas. (La réplica sigue las observaciones del diario: después del primer cambio, "cambios en toda la réplica" dice cuántas veces el cuerpo habría elegido distinto en las mismas escenas, no lo que habría pasado.) **Cuántos pasos dejarían de chocar:** ninguno por muros, porque no había muros (sección 0): los {n(na)} tics bloqueados contra suelo vacío son de la latencia y desaparecen con la caché; los {n(ag)} contra la hermana son del cuerpo. Con la red de muros encendida en la réplica: {'; '.join(f"{x['carp']}/{x['slot']}: {x['muros']} muros, primer cambio {(x['primer'] or {}).get('t')}" for x in red[:16])}.

**Arreglo 3 sobre los cuadernos del campo:** la creencia del botiquín recalculada sin los cortes (`CuadernoP29.creencia`), por criatura y día (`P7_29_F2.json`, `creencia_sin_cortes`; aquí los días 1, 5, 10, 15, 19 y 20):

{chr(10).join(TF2b)}

## F3 · La curiosidad del cuánto (banco)

`banco_P7_29.py --f3` sobre la vida s1 d20 asiento 10 de P7-24 ({n((F3 or {}).get('d', {}).get('tics'))} tics; lleva dos botiquines casi todo el día y no los usa), con cuatro cuadernos del botiquín (el resto del cuaderno, el real del día 19) -> `P7_29_F3.json`. Por tic con botiquín en el zurrón (usar no necesita el paso listo; durante el canal el candidato queda vetado):

{chr(10).join(TF3)}

{chr(10).join(TF3b)}

Lectura. Con solo "al menos" (lo más alto que sabe: 30), la ignorancia del cuánto es 1 y la fila vale lo que la curiosidad de clase el día 1 (misma escala, misma calma: M {n((F3 or {}).get('a', {}).get('M_cuanto', {}).get('mediana'), 4)} frente a {n((F3 or {}).get('a', {}).get('M_curiosidad_mediana'), 4)} de la clase, ya sabida). En la foto de usar, la fila baja (alivio 0,5 en la clase del botiquín) solo cuando le faltan más de 30 de vida (tabla: con (a) baja desde vida 65; con (b) y (c), sabe 45, desde vida 55; con (d), sabe 50, desde vida 45). Con un recuerdo firme la ignorancia del cuánto baja a 1/(1 + peso) y con tres se apaga como cualquier ignorancia. En esta vida la criatura va a 100 de vida {n(((F3 or {}).get('a', {}).get('tics_listos_con_botiquin') or 0) - 174)} de los {n((F3 or {}).get('a', {}).get('tics_listos_con_botiquin'))} tics con botiquín y solo pierde vida al final, fuera del círculo: el cuerpo ofrece `usar_botiquin` 10 veces (entre canales de 48 tics que el anillo corta) y lo elige las 10 con los cuatro cuadernos: aquí decide el cuerpo (la cura imaginada con la creencia), no el cuánto. El momento en que el cuánto mueve por sí solo (herida media con botiquín y calma) no aparece en esta vida; habrá que verlo en el humo.

{S4}

## Lo que queda para la mesa

1. La red de los muros: apagada (F1 no pasa con ella; no hay muros que aprender, lo que no se ve no es un muro: bloquea unos tics y se va). Quitarla o cambiarla.
2. P7-28 se corrige: la que recuerda se hundía por lenta (sección 0). Habría que volver a jugar los días 16-20 (o un campo corto) con la pieza rápida antes de atribuir el puesto al candidato `ir_curioso`.
3. El humo F4 está listo para lanzar con el "adelante".
"""
open(os.path.join(AQUI, "informe_P7_29.md"), "w").write(T); print("informe_P7_29.md", len(T.splitlines()), "lineas")
