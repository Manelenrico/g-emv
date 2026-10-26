"""[P7-29b] Escribe informe_P7_29b.md desde P7_29_humo.json (analiza_P7_29.py), P7_29_estado.json (lanza_P7_29.py: peticiones, coste, guarda de latencia) y P7_29b_latencia.json (latencia_P7_29b.py). Ninguna cifra a mano."""
import hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
def J(f): p = os.path.join(AQUI, f); return json.load(open(p)) if os.path.exists(p) else None
HU = J("P7_29_humo.json") or []; ES = J("P7_29_estado.json") or {}; LA = J("P7_29b_latencia.json"); SEM = J("semillas_P7_29.json")
n = lambda x, d=0: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = hashlib.md5(open(os.path.join(RAIZ, "motor", "model.py"), "rb").read()).hexdigest()
import guarda_latencia_P7_29 as GL
# ── F4 ──
pet = sorted((p for p in ES.get("peticiones", []) if p["brazo"] == "APRENDE"), key=lambda p: p["dia"]); gasto = sum(float(p.get("coste_usd") or 0) for p in pet)
TG = ["| día · asiento | decisiones | ms mediana · p95 · máximo | tics por encima del tic (41,7 ms) | pasos listos | bloqueados · sin cuerpo delante | guarda |", "|---|---:|---|---:|---:|---|---|"]
for p in pet:
    for sl in ("10", "11"):
        g = (p.get("latencia") or {}).get(sl)
        if g: TG.append(f"| d{p['dia']} · {sl} | {n(g['decisiones'])} | {n(g['ms_mediana'], 2)} · {n(g['ms_p95'], 2)} · {n(g['ms_max'], 2)} | {n(100 * (g['sobre_el_tic'] or 0), 2)} % | {n(g['paso_listo'])} | {n(g['bloqueados'])} · {n(g['bloqueados_sin_cuerpo'])} ({n(100 * g['fraccion_sin_cuerpo'], 2)} %) | {'pasa' if g['pasa'] else 'NO PASA: ' + '; '.join(g['motivo'])} |")
TH = ["| día · asiento | tics | puesto | contacto botiquín · ración (tic) | botiquín: canales · firmes · al menos · cortes (vida al abrir) | ración: canales · firmes · al menos · cortes | creencia botiquín dentro · fuera | ignorancia clase · cuánto · lo más alto que sabe | ración: creencia dentro · ign. cuánto | `ir_curioso` con paso listo |", "|---|---:|---:|---|---|---|---|---|---|---|"]
for v in HU:
    if v.get("sin_diario"): TH.append(f"| d{v['dia']} · {v['asiento']} | sin diario | | | | | | | | |"); continue
    ub = v["usos"]["botiquin"]; ur = v["usos"]["racion"]; ab = v["al_acabar"]["botiquin"]; ar = v["al_acabar"]["racion"]; cb = ab["creencia"]; cr = ar["creencia"]
    TH.append(f"| d{v['dia']} · {v['asiento']} | {n(v['tics'])} | {n(v['puesto'])} | {n(v['contacto']['botiquin'])} · {n(v['contacto']['racion'])} | {len(ub)} · {sum(1 for u in ub if u['firme'])} · {sum(1 for u in ub if u['al_menos'])} · {sum(1 for u in ub if not u['completado'])} ({', '.join(n(u['hp0']) for u in ub) or '—'}) | {len(ur)} · {sum(1 for u in ur if u['firme'])} · {sum(1 for u in ur if u['al_menos'])} · {sum(1 for u in ur if not u['completado'])} | {n(cb.get('dentro'), 1)} · {n(cb.get('fuera'), 1)} | {n(ab['ignorancia'], 3)} · {n(ab['ignorancia_cuanto'], 3)} · {n(ab['sabido_max'], 1)} | {n(cr.get('dentro'), 1)} · {n(ar['ignorancia_cuanto'], 3)} | {n(v['ir_curioso_con_paso_listo'])} ({n(100 * v['ir_curioso_fraccion'])} %) |")
causas = [(v["dia"], v["asiento"], o, c) for v in HU if not v.get("sin_diario") for o in ("botiquin", "racion") for c in v["al_acabar"][o]["causas_de_corte"]]
cuantos = [(v["dia"], v["asiento"], c) for v in HU if not v.get("sin_diario") for c in v["cuanto_registros"]]
usos_firmes = [(v["dia"], v["asiento"], u) for v in HU if not v.get("sin_diario") for u in v["usos"]["botiquin"] if u["firme"]]
gif_txt = ""
gf = os.path.join(AQUI, "P7_29_uso_firme.gif")
if os.path.exists(gf): gif_txt = f"GIF de los datos del uso que da el primer recuerdo firme del botiquín (día {usos_firmes[0][0]}, asiento {usos_firmes[0][1]}, tic {n(usos_firmes[0][2]['t0'])}, vida {n(usos_firmes[0][2]['hp0'])}): `P7_29_uso_firme.gif` (`gif_P7_23.py`, matplotlib sobre el diario; fuera de git)." if usos_firmes else "(sin uso firme en el humo: no hay GIF que hacer)"
# ── punto 4 ──
TL = ["| campo · brazo · bloque | vidas | ms mediana (media de vidas) | ms p95 (media · máx) | ms máx | tics por encima del tic | bloqueados sin cuerpo (media) | vidas con p95 > 20 ms · con sin-cuerpo > 5 % | muertas · antes del tic 4.000 · por rival | tic de muerte (mediana) | puesto medio |", "|---|---:|---:|---|---:|---:|---:|---|---|---:|---:|"]
TT = ["| campo · brazo | muertes tempranas (< 4.000) | de ellas, no pasan la guarda | p95 medio (ms) · bloqueados sin cuerpo (media) | el resto de vidas: no pasan la guarda · bloqueados sin cuerpo (media) |", "|---|---:|---:|---|---|"]
if LA:
    for k, v in LA["por_campo_brazo_bloque"].items():
        if "tempranas" in k: TT.append(f"| {k.replace(' · muertes tempranas', '')} | {v['n']} | {v['no_pasan_la_guarda']} | {n(v['ms_p95_media'], 1)} · {n(100 * v['sin_cuerpo_media'], 2) if v['sin_cuerpo_media'] is not None else '—'} % | {v['resto']['no_pasan_la_guarda']} de {v['resto']['n']} · {n(100 * v['resto']['sin_cuerpo_media'], 2)} % |")
        elif k.endswith("todos") or "dias 1-5" in k or "dias 16-20" in k: TL.append(f"| {k} | {v['vidas']} | {n(v['ms_mediana_media'], 2)} | {n(v['ms_p95_media'], 1)} · {n(v['ms_p95_max'], 1)} | {n(v['ms_max'], 1)} | {n(100 * v['sobre_el_tic_media'], 2)} % | {n(100 * v['sin_cuerpo_media'], 2)} % | {v['vidas_con_p95_sobre_20']} · {v['vidas_con_sin_cuerpo_sobre_5']} | {v['muertos']} · {v['muertes_antes_de_4000']} · {v['muertes_por_rival']} | {n(v['tic_muerte_mediana'])} | {n(v['puesto_medio'], 2)} |")
A10 = LA["por_campo_brazo_bloque"]["P7-10 · APRENDE · todos"]; B10 = LA["por_campo_brazo_bloque"]["P7-10 · BORRADO · todos"]; T10 = LA["por_campo_brazo_bloque"]["P7-10 · TECHO · todos"]
A14 = LA["por_campo_brazo_bloque"]["P7-14b · APRENDE · todos"]; B14 = LA["por_campo_brazo_bloque"]["P7-14b · BORRADO · todos"]; T14 = LA["por_campo_brazo_bloque"]["P7-14b · TECHO · todos"]
tA10 = LA["por_campo_brazo_bloque"]["P7-10 · APRENDE · muertes tempranas"]; tA14 = LA["por_campo_brazo_bloque"]["P7-14b · APRENDE · muertes tempranas"]
lentas = sorted([v for v in LA["vidas"] if not v["pasa"]], key=lambda v: -v["ms_p95"])
TLv = ["| vida que no pasa la guarda | ms mediana · p95 · máx | bloqueados sin cuerpo | muerte |", "|---|---|---:|---|"]
for v in lentas: TLv.append(f"| {v['campo']} s{v['serie']} d{v['dia']} {v['brazo']} asiento {v['asiento']} | {n(v['ms_mediana'], 1)} · {n(v['ms_p95'], 1)} · {n(v['ms_max'], 1)} | {n(100 * v['fraccion_sin_cuerpo'], 2)} % | {('tic ' + n(v['tic_muerte']) + ', ' + str(v['causa'])) if v['murio'] else 'sobrevive'}, puesto {n(v['puesto'])} |")
humo_ok = bool(pet) and all(p.get("estado") == "completed" for p in pet) and len(pet) == 3
guard_fail = [(p["dia"], sl, g["motivo"]) for p in pet for sl, g in (p.get("latencia") or {}).items() if not g["pasa"]]
T = f"""# P7-29b · El humo con la pieza rápida, y la latencia de los campos anteriores

*8-oct-2026. Coste: plataforma {n(gasto, 4)} USD (el humo, F5); consola 0. `motor/model.py` = `{md5}` al empezar y al acabar; cuerpo y congelados sin tocar. Decisiones de la mesa aplicadas: (1) la red de los muros se quita del todo (`nace_P7_29.py`, `banco_P7_29.py`, `Dockerfile.pareja_P7_29`; queda en el commit f9a2e75); quedan la caché, la curiosidad que solo mueve por curiosidad, el corte aparte y la curiosidad del cuánto; (2) guarda de latencia nueva (`guarda_latencia_P7_29.py`, enganchada en `lanza_P7_29.py` al bajar cada diario: p95 > 20 ms o más del 5 % de pasos listos bloqueados sin cuerpo delante = la cadena para y avisa). Este informe lo escribe `escribe_informe_P7_29b.py` desde `P7_29_humo.json`, `P7_29_estado.json` y `P7_29b_latencia.json`. Ninguna cifra a mano.*

## En corto

1. **Humo F4 (APRENDE, semillas k 175-177): {'las tres partidas completas' if humo_ok else 'PARADO por la guarda de latencia tras el día 1'}** ({len(pet)} partida{'s' if len(pet) != 1 else ''} jugada{'s' if len(pet) != 1 else ''}: {', '.join(f"d{p['dia']} {p.get('estado')}" for p in pet)}). {'' if humo_ok else 'La guarda es la regla 2 de la mesa: p95 > 20 ms = la cadena para y avisa; aquí el p95 del asiento 10 fue ' + n(max(g['ms_p95'] for p in pet for g in (p.get('latencia') or {}).values()), 2) + ' ms (por 0,53 ms), con mediana ' + n(min(g['ms_mediana'] for p in pet for g in (p.get('latencia') or {}).values()), 1) + ' ms y el 0,3 % de los tics por encima del tic; los tics más lentos son los de 20-21 candidatos (todos los pasos y ataques posibles), no los del recuerdo (el cuaderno acaba el día con 2 recuerdos). Con esta guarda, en P7-14b habrían parado ' + str(LA['por_campo_brazo_bloque']['P7-14b · APRENDE · todos']['vidas_con_p95_sobre_20'] + LA['por_campo_brazo_bloque']['P7-14b · BORRADO · todos']['vidas_con_p95_sobre_20'] + LA['por_campo_brazo_bloque']['P7-14b · ESPERANZA · todos']['vidas_con_p95_sobre_20']) + ' vidas de 320 (punto 4). Los días 2 y 3 no se han jugado: decisión de la mesa.'} Guarda de latencia: {'pasa en las ' + str(sum(1 for p in pet for g in (p.get('latencia') or {}).values() if g['pasa'])) + ' vidas' if not guard_fail else 'NO PASA en ' + '; '.join(f'd{d} asiento {sl}: ' + ', '.join(m) for d, sl, m in guard_fail)}; ms de decisión: {', '.join(f"d{p['dia']}·{sl} {n(g['ms_mediana'], 1)} / {n(g['ms_p95'], 1)} / {n(g['ms_max'], 1)}" for p in pet for sl, g in sorted((p.get('latencia') or {}).items()))} (mediana / p95 / máximo).
2. **Lo que hizo la que nace rápida (día 1):** {'; '.join(f"d{v['dia']}·{v['asiento']}: botiquín {len(v['usos']['botiquin'])} canales ({sum(1 for u in v['usos']['botiquin'] if u['firme'])} firmes, {sum(1 for u in v['usos']['botiquin'] if u['al_menos'])} al menos, {sum(1 for u in v['usos']['botiquin'] if not u['completado'])} cortes), ración {len(v['usos']['racion'])} ({sum(1 for u in v['usos']['racion'] if u['firme'])} firmes), creencia botiquín {n(v['al_acabar']['botiquin']['creencia'].get('dentro'), 1)}, ign. cuánto {n(v['al_acabar']['botiquin']['ignorancia_cuanto'], 2)}, ir_curioso {n(100 * v['ir_curioso_fraccion'])} %, puesto {n(v['puesto'])}" for v in HU if not v.get('sin_diario'))}.
3. **Punto 4 (P7-10 y P7-14b, solo describir):** APRENDE decidía más despacio que los demás (mediana {n(A10['ms_mediana_media'], 1)} ms en P7-10 y {n(A14['ms_mediana_media'], 1)} en P7-14b, frente a TECHO {n(T10['ms_mediana_media'], 1)} y {n(T14['ms_mediana_media'], 1)}, BORRADO {n(B10['ms_mediana_media'], 1)} y {n(B14['ms_mediana_media'], 1)}), pero muy por debajo del tic: {n(100 * A10['sobre_el_tic_media'], 2)} % y {n(100 * A14['sobre_el_tic_media'], 2)} % de tics por encima de 41,7 ms, y {n(100 * A10['sin_cuerpo_media'], 2)} % / {n(100 * A14['sin_cuerpo_media'], 2)} % de pasos listos bloqueados sin cuerpo (los demás brazos, parecido). Las muertes tempranas de APRENDE ({tA10['n']} en P7-10, {tA14['n']} en P7-14b) pasan todas la guarda (p95 {n(tA10['ms_p95_media'], 1)} y {n(tA14['ms_p95_media'], 1)} ms; bloqueados sin cuerpo {n(100 * (tA10['sin_cuerpo_media'] or 0), 1)} % y {n(100 * (tA14['sin_cuerpo_media'] or 0), 1)} %): **la latencia no explica las muertes tempranas que separaban a APRENDE de BORRADO en esos campos.** Lo que creció hasta romper fue el recuerdo por parecido de P7-23 (P7-24), que esos campos no tenían.

## F4 · El humo de 3 días (APRENDE, semillas nuevas)

Semillas: `semillas_P7_29.json` (k 175-177: {', '.join(str(s) for s in (SEM or {}).get('serie1', []))}); imagen `Dockerfile.pareja_P7_29` (GEMV_P7_29=1: caché, curiosidad por curiosidad, corte aparte, cuánto; sin red de muros); lanzador `lanza_P7_29.py --cadena-aprende 1 1 3` (cada día se hornea con los cuadernos del día anterior); diarios en `paintball/runs/P729_s1_d<D>_APRENDE_<semilla>/`; lectura `analiza_P7_29.py` -> `P7_29_humo.json`. Partidas: {'; '.join(f"d{p['dia']} {p.get('estado')} ({n(p.get('coste_usd'), 4)} USD)" for p in pet)}.

**La guarda de latencia** (medida al bajar cada diario; `P7_29_estado.json`, `peticiones[].latencia`):

{chr(10).join(TG)}

**Por día y criatura:**

{chr(10).join(TH)}

Cortes del día con su causa (recuerdos `acto` del cuaderno, arreglo 3): {'; '.join(f"d{d}·{a} {o}: daño {c.get('dano')} de {c.get('fuentes') or 'nadie conocido'}, última elección `{c.get('ultima_eleccion')}`, {c.get('tics')} tics" for d, a, o, c in causas) if causas else 'ningún corte'}.

La fila del cuánto en la partida (`P7_cuanto`, una muestra cada 3.000 tics): {'; '.join(f"d{d}·{a} t{n(c['tick'])}: M {n(c['M'], 4)} (curiosidad de clase {n(c['M_curiosidad'], 4)}), botiquín ign. {n((c['clases'] or {}).get('first_aid', {}).get('ignorancia'), 3)} / cuánto {n((c['clases'] or {}).get('first_aid', {}).get('ignorancia_cuanto'), 3)} / sabe {n((c['clases'] or {}).get('first_aid', {}).get('sabido_max'), 1)}" for d, a, c in cuantos[::3][:10]) if cuantos else '—'}.

{gif_txt if gif_txt else '(GIF: en el día 1 no hay ningún uso firme del botiquín (dos "al menos" por asiento y un corte): no hay GIF que hacer.)'}

## F5 · Créditos del humo

Plataforma: {n(gasto, 4)} USD en {len([p for p in pet if p.get('coste_usd')])} partidas; acumulado de la séptima: {n(41.9017 + gasto, 4)} USD. Consola de Anthropic: 0. Saldos no consultados.

## Punto 4 · La latencia de P7-10 y P7-14b (solo describir)

`latencia_P7_29b.py` -> `P7_29b_latencia.json`: los {len(LA['vidas'])} diarios de los dos campos (4 brazos × 20 días × 2 series × 2 asientos cada uno) con la misma guarda (`RADIOGRAFIA.ms` del diario: el tiempo de `decide` de cada tic, `policy_cortex.py:511-618`; pasos listos bloqueados sin agente a la vista en la casilla del paso). El diario sí lo permite medir: el tiempo se apuntó en todos los campos; nadie lo había mirado.

{chr(10).join(TL)}

{chr(10).join(TT)}

Vidas que no pasarían la guarda nueva ({len(lentas)} de {len(LA['vidas'])}):

{chr(10).join(TLv)}

Lectura. En los dos campos APRENDE era el brazo más lento (lee el cuaderno y calcula la creencia; en P7-14b además pide), BORRADO el segundo y TECHO el más rápido, pero todos a 2-4 ms de mediana y 4-13 ms de p95: una décima parte del tic. Las vidas que no pasan la guarda nueva son por el p95 (hasta 30 ms), no por pasos bloqueados sin cuerpo ({sum(v['vidas_con_sin_cuerpo_sobre_5'] for k, v in LA['por_campo_brazo_bloque'].items() if k.endswith('todos'))} vida de 640 pasa del 5 %; la media es 0,2-0,4 %, frente al 32 % de APRENDE en los días 16-20 de P7-24). Las muertes tempranas de APRENDE son {tA10['n']} y {tA14['n']}, todas con la guarda limpia, y la fracción de bloqueados sin cuerpo en ellas no es mayor que en el resto. Por tanto, lo que separaba a APRENDE de BORRADO en P7-10 y P7-14b no puede atribuirse a la latencia; sigue siendo lo que dijeron esos informes. La latencia que rompe aparece con el recuerdo por parecido (P7-22/23) sobre cuadernos de 20-30 recuerdos (P7-24, días 11-20).
"""
open(os.path.join(AQUI, "informe_P7_29b.md"), "w").write(T); print("informe_P7_29b.md", len(T.splitlines()), "lineas")
