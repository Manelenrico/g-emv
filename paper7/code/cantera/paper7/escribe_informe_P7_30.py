"""[P7-30] Escribe informe_P7_30.md (el campo entero) desde P7_30_resumen.json, P7_30_vidas.json, P7_30_estado.json, P7_30_freno.json, P7_29_estado.json y semillas_P7_30.json. Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
R = J("P7_30_resumen.json"); V = J("P7_30_vidas.json"); E = J("P7_30_estado.json"); S = J("semillas_P7_30.json"); FR = J("P7_30_freno.json"); E29 = J("P7_29_estado.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
coste = sum(p.get("coste_usd") or 0 for p in E["peticiones"]); coste_humo = sum(p.get("coste_usd") or 0 for p in E29["peticiones"]); corte = {tuple(x) for x in R["partidas_con_corte"]}
L = [v for v in V.values() if not v.get("sin_diario")]
ACUM_ANTES = 42.0106      # acumulado de la septima hasta P7-29b (informe_P7_29b: 41,9017 + 0,1089)
def bloque(b, dias):
    vs = [v for v in L if v["brazo"] == b and v["dia"] in dias]; vp = [v for v in vs if (v["serie"], v["dia"], b) not in corte]
    mu = [v for v in vp if v["murio"]]; ub = [u for v in vs for u in v["usos"]["botiquin"]]; ur = [u for v in vs for u in v["usos"]["racion"]]
    tc = [v.get("canales_techo") for v in vs if v.get("canales_techo")]
    return {"vidas": len(vs), "vidas_puesto": len(vp), "puesto": (st.mean(v["puesto"] for v in vp if v["puesto"] is not None) if vp else None), "mueren": len(mu), "vida_al_morir": (st.median(v["vida_al_morir"] for v in mu) if mu else None),
            "usos_b": len(ub), "firmes_b": sum(1 for u in ub if u["firme"]), "almenos_b": sum(1 for u in ub if u["al_menos"]), "cortes_b": sum(1 for u in ub if not u["completado"]), "hp_b": (st.median(u["hp0"] for u in ub) if ub else None),
            "usos_r": len(ur), "firmes_r": sum(1 for u in ur if u["firme"]), "almenos_r": sum(1 for u in ur if u["al_menos"]), "cortes_r": sum(1 for u in ur if not u["completado"]), "hp_r": (st.median(u["hp0"] for u in ur) if ur else None),
            "techo_canales": (sum(x["canales"] for x in tc) if tc else None), "techo_hp": (st.median([h for x in tc for h in x["hp"]]) if any(x["hp"] for x in tc) else None),
            "pedidos": sum(v["pedidos_abre"] for v in vs), "regalos": sum(sum(v["regalos"].values()) for v in vs), "curioso": (st.median(100 * v["ir_curioso_con_paso_listo"] / max(1, v["tics_con_paso_listo"]) for v in vs) if vs else None),
            "contacto_b": sum(1 for v in vs if v["primer_contacto"]["botiquin"] is not None), "contacto_r": sum(1 for v in vs if v["primer_contacto"]["racion"] is not None),
            "ign_cuanto_b": (st.mean(v["al_acabar"]["botiquin"]["ignorancia_cuanto"] for v in vs if v["al_acabar"]["botiquin"]["ignorancia_cuanto"] is not None) if b != "TECHO" else None),
            "ms": (st.median(v["latencia"]["ms_mediana"] for v in vs if v["latencia"]["ms_mediana"] is not None) if vs else None), "ms_p95_max": (max(v["latencia"]["ms_p95"] for v in vs if v["latencia"]["ms_p95"] is not None) if vs else None), "sobre": (max(v["latencia"]["sobre_el_tic"] or 0 for v in vs) if vs else None), "sin_cuerpo": (max(v["latencia"]["fraccion_sin_cuerpo"] for v in vs) if vs else None)}
T1 = ["| brazo | días | vidas (en puesto) | puesto medio | mueren · vida al morir (mediana) | botiquín: canales (firmes, «al menos», cortes) · vida al abrir | ración: canales (firmes, «al menos», cortes) · vida al abrir | pedidos · regalos | `ir_curioso` con paso listo (mediana %) | contacto botiquín · ración (vidas) | ign. del cuánto botiquín (media) |", "|---|---|---|---:|---|---|---|---|---:|---|---:|"]
for b in ("TECHO", "BORRADO", "APRENDE"):
    for et, dias in (("1-5", range(1, 6)), ("6-10", range(6, 11)), ("11-15", range(11, 16)), ("16-20", range(16, 21))):
        x = bloque(b, dias); ub = (f"{x['techo_canales']} canales del diario · {n(x['techo_hp'], 0)}" if b == "TECHO" else f"{x['usos_b']} ({x['firmes_b']}, {x['almenos_b']}, {x['cortes_b']}) · {n(x['hp_b'], 0)}")
        T1.append(f"| {b} | {et} | {x['vidas']} ({x['vidas_puesto']}) | {n(x['puesto'], 2)} | {x['mueren']} · {n(x['vida_al_morir'], 0)} | {ub} | {x['usos_r']} ({x['firmes_r']}, {x['almenos_r']}, {x['cortes_r']}) · {n(x['hp_r'], 0)} | {x['pedidos']} · {x['regalos']} | {n(x['curioso'], 1)} | {x['contacto_b']} · {x['contacto_r']} | {n(x['ign_cuanto_b'], 3)} |")
TL = ["| brazo | días | ms por decisión: mediana (mediana de vidas) · p95 (máx entre vidas) | decisiones por encima del tic (máx entre vidas) | pasos listos bloqueados sin cuerpo (máx) | vidas que no pasan la guarda |", "|---|---|---|---:|---:|---:|"]
for b in ("TECHO", "BORRADO", "APRENDE"):
    for et, dias in (("1-5", range(1, 6)), ("6-10", range(6, 11)), ("11-15", range(11, 16)), ("16-20", range(16, 21))):
        x = bloque(b, dias); vs = [v for v in L if v["brazo"] == b and v["dia"] in dias]
        TL.append(f"| {b} | {et} | {n(x['ms'], 2)} · {n(x['ms_p95_max'], 1)} | {n(100 * (x['sobre'] or 0), 2)} % | {n(100 * (x['sin_cuerpo'] or 0), 2)} % | {sum(1 for v in vs if not v['latencia']['pasa'])} |")
def E1t():
    L_ = ["| criatura | recuerdos firmes al acabar el día 5: botiquín / ración | ignorancia al acabar el día 10: botiquín / ración |", "|---|---|---|"]
    for k, x in R["E1"]["criaturas"].items(): L_.append(f"| {k} | {x['firmes_al_acabar_el_dia_5']['botiquin']} / {x['firmes_al_acabar_el_dia_5']['racion']} | {n(x['ignorancia_al_acabar_el_dia_10']['botiquin'], 3)} / {n(x['ignorancia_al_acabar_el_dia_10']['racion'], 3)} |")
    return "\n".join(L_)
def E2t():
    L_ = ["| criatura | primer contacto (tics de vida acumulados): botiquín / ración | primer recuerdo firme: botiquín / ración | tarda desde el contacto: botiquín / ración | orden | el segundo tarda menos |", "|---|---|---|---|---|---|"]
    for k, x in R["E2"]["criaturas"].items():
        c = x["contacto_acumulado"]; f = x["primer_firme_acumulado"]; t = x["tarda_desde_el_contacto"]
        L_.append(f"| {k} | {n(c.get('botiquin'), 0)} / {n(c.get('racion'), 0)} | {n(f.get('botiquin'), 0)} / {n(f.get('racion'), 0)} | {n(t.get('botiquin'), 0)} / {n(t.get('racion'), 0)} | {' → '.join(x['orden']) or '—'} | {'sí' if x['el_segundo_tarda_menos'] else 'no'} |")
    return "\n".join(L_)
def E3t():
    L_ = ["| criatura | día en que la ración llega a 12 | día en que el botiquín (dentro) llega a 40 | la ración antes |", "|---|---:|---:|---|"]
    for k, x in R["E3"]["criaturas"].items(): L_.append(f"| {k} | {x['dia_racion_12'] if x['dia_racion_12'] else 'nunca'} | {x['dia_botiquin_dentro_40'] if x['dia_botiquin_dentro_40'] else 'nunca'} | {'sí' if x['racion_antes'] else 'no'} |")
    return "\n".join(L_)
def E7t():
    L_ = ["| criatura | creencia del botiquín dentro (sin cortes) al acabar el día 20 | ≥ 35 |", "|---|---:|---|"]
    for k, x in R["E7"]["criaturas"].items(): L_.append(f"| {k} | {n(x['creencia_dentro_dia_20'], 1)} | {'sí' if x['llega_a_35'] else 'no'} |")
    return "\n".join(L_)
def pz(p): return f"{n(p['media'], 2)} ± {n(p['ee'], 2)} (n {p['n']})"
P = R["puesto"]
T4 = ["| comparación | días 1-5 (media ± error estándar) | días 16-20 |", "|---|---|---|"] + [f"| {k} | {pz(v['dias 1-5'])} | {pz(v['dias 16-20'])} |" for k, v in P.items()] + [f"| APRENDE − BORRADO (E8; partidas con corte excluidas) | {pz(R['E8']['dias 1-5'])} | {pz(R['E8']['dias 16-20'])} |", f"| APRENDE − BORRADO (sin excluir) | {pz(R['E8_sin_excluir']['dias 1-5'])} | {pz(R['E8_sin_excluir']['dias 16-20'])} |"]
# por criatura y dia: creencia, ignorancia, cuanto, usos
TD = ["| criatura | día | botiquín: creencia dentro · ignorancia · ign. cuánto · sabe | firmes · al menos · cortes (botiquín) | ración: creencia · ign. cuánto | firmes · al menos · cortes (ración) | puesto |", "|---|---:|---|---|---|---|---:|"]
for s in (1, 2):
    for sl in (10, 11):
        for v in sorted((v for v in L if v["brazo"] == "APRENDE" and v["serie"] == s and v["slot"] == sl), key=lambda v: v["dia"]):
            if v["dia"] in (1, 3, 5, 8, 10, 13, 15, 18, 20):
                ab = v["al_acabar"]["botiquin"]; ar = v["al_acabar"]["racion"]; rb = v["recuerdos_al_acabar"]["botiquin"]; rr = v["recuerdos_al_acabar"]["racion"]; crr = [x for x in ar["creencia"].values() if x is not None]
                TD.append(f"| s{s}·{sl} | {v['dia']}{' (parcial)' if v.get('parcial') else ''} | {n(ab['creencia'].get('dentro'), 1)} · {n(ab['ignorancia'], 3)} · {n(ab['ignorancia_cuanto'], 3)} · {n(ab['sabido_max'], 1)} | {rb['firmes']} · {rb['al_menos']} · {rb['cortes']} | {n(max(crr), 1) if crr else '—'} · {n(ar['ignorancia_cuanto'], 3)} | {rr['firmes']} · {rr['al_menos']} · {rr['cortes']} | {n(v['puesto'], 0)} |")
CU = R["cuanto_al_usar"]; LT = R["latencia_por_brazo"]
sello = R["sello"]; ok = lambda k: "**pasa**" if sello[k] else "**no pasa**"
pasan = [k for k in ("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8") if sello[k]]; fallan = [k for k in ("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8") if not sello[k]]
causas = [c for v in L if v["brazo"] == "APRENDE" for c in v["causas_de_corte"]]
cc = collections.Counter(("daño" if (c.get("dano") or 0) > 0 else "sin daño") + " · " + str(c.get("ultima_eleccion")) for c in causas)
T = f"""# P7-30 · El segundo campo de la primera etapa: nacer sin saber, con la pieza rápida y la curiosidad del cuánto

*{E['peticiones'][-1].get('completada_a_las', '')[:10] if E['peticiones'] else ''} (sellado el 8-oct-2026 en `f10da22`, antes de la primera partida). Coste: plataforma {n(coste, 4)} USD (las {len(E['peticiones'])} partidas del campo) más {n(coste_humo, 4)} del humo de freno (P7-29/29b, 3 partidas); consola 0.
`motor/model.py` = `{hashlib.md5(open(os.path.join(AQUI, '..', '..', 'motor', 'model.py'), 'rb').read()).hexdigest()}` al empezar y al acabar; cuerpo y congelados sin tocar. Sello: `SELLO_P7_30.md`. Diarios en `paintball/runs/P730_*` (fuera de git);
`analiza_P7_30.py` → `P7_30_vidas.json`; `sello_P7_30.py` → `P7_30_resumen.json`; figuras `figuras_P7_30.py`; este informe lo escribe `escribe_informe_P7_30.py`. El sello se ha evaluado una sola vez, al final.*

## El freno (paso 1 de la mesa, sobre el humo de P7-29/29b)

`freno_P7_30.py` → `P7_30_freno.json`: (a) el cuaderno viaja y se lee los días 2 y 3: {'sí' if FR['a_cuaderno_viaja'] else 'no'}; (b) tocan algún objeto desconocido {len(FR['b_tocan'])} de 6 ({', '.join(FR['b_tocan'])}); (c) sube la creencia: {'; '.join(FR['c_sube'])}; (d) la guarda de latencia (regla de la mesa de P7-30) pasa en {len(FR['d_guarda_pasa_en'])} de 6. **{FR['FRENO']}.** Guarda de latencia del humo: {'; '.join(f"d{p['dia']}·{sl} {n(g['ms_mediana'], 1)} / {n(g['ms_p95'], 1)} / {n(g['ms_max'], 1)} ms, {n(100 * (g['sobre_el_tic'] or 0), 2)} % sobre el tic" for p in sorted(E29['peticiones'], key=lambda p: p['dia']) for sl, g in sorted((p.get('latencia') or {}).items()))}.

## El sello

| | regla | resultado | |
|---|---|---|---|
| E1 | descubre: firmes de los dos al día 5 en las 4; ignorancia < 0,3 al día 10 en ≥ 3 | firmes de los dos al día 5: **{R['E1']['firme_de_los_dos_al_dia_5']} de 4**; ignorancia < 0,3 al día 10: {R['E1']['ignorancia_menor_0_3_al_dia_10']} de 4 | {ok('E1')} |
| E2 | aprende a aprender: el segundo objeto tarda menos en ≥ 3 | {R['E2']['el_segundo_tarda_menos']} de 4 | {ok('E2')} |
| E3 | qué aprende antes: la ración llega al 80 % antes que el botiquín en ≥ 3 | {R['E3']['racion_antes']} de 4 | {ok('E3')} |
| E4 | pierde y recupera: APRENDE − TECHO > 2 ee en 1-5; ≤ la mitad en 16-20 | 1-5: {pz(R['E4']['dias 1-5'])}; 16-20: {pz(R['E4']['dias 16-20'])} | {ok('E4')} |
| E5 | sin memoria no recupera: BORRADO − TECHO en 16-20 ≥ la mitad de 1-5 | 1-5: {pz(R['E5']['dias 1-5'])}; 16-20: {pz(R['E5']['dias 16-20'])} | {ok('E5')} |
| E6 | lo aprendido cambia la conducta: vida al abrir el botiquín (11-20), APRENDE < BORRADO | medianas {n(R['E6']['APRENDE']['mediana'], 0)} ({R['E6']['APRENDE']['aperturas']} aperturas) frente a {n(R['E6']['BORRADO']['mediana'], 0)} ({R['E6']['BORRADO']['aperturas']}) | {ok('E6')} |
| E7 | el cuánto: creencia del botiquín dentro ≥ 35 el día 20 en ≥ 3 de 4 | {R['E7']['llegan_a_35']} de 4 | {ok('E7')} |
| E8 | no se hunde: APRENDE − BORRADO en 16-20 no mayor que en 1-5 por más de 2 ee | 1-5: {pz(R['E8']['dias 1-5'])}; 16-20: {pz(R['E8']['dias 16-20'])}; crece {n(R['E8']['crece'], 2)} con ee de la diferencia {n(R['E8']['ee_de_la_diferencia'], 2)} | {ok('E8')} |

**Primera cuenta (todas las vidas; solo salen las partidas con corte de la plataforma, como manda el sello): pasan {', '.join(pasan) or 'ninguna'}; no pasan {', '.join(fallan) or 'ninguna'}.**

**Segunda cuenta (quitando además las {len(R['partidas_marcadas'])} partidas marcadas por la guarda de latencia, enteras, y sus pares):** E4 1-5 {pz(R['E4_sin_marcadas']['dias 1-5'])}, 16-20 {pz(R['E4_sin_marcadas']['dias 16-20'])} → {'pasa' if R['E4_sin_marcadas']['pasa'] else 'no pasa'}; E5 1-5 {pz(R['E5_sin_marcadas']['dias 1-5'])}, 16-20 {pz(R['E5_sin_marcadas']['dias 16-20'])} → {'pasa' if R['E5_sin_marcadas']['pasa'] else 'no pasa'}; E6 medianas {n(R['E6_sin_marcadas']['APRENDE']['mediana'], 0)} ({R['E6_sin_marcadas']['APRENDE']['aperturas']}) frente a {n(R['E6_sin_marcadas']['BORRADO']['mediana'], 0)} ({R['E6_sin_marcadas']['BORRADO']['aperturas']}) → {'pasa' if R['E6_sin_marcadas']['pasa'] else 'no pasa'}; E8 1-5 {pz(R['E8_sin_marcadas']['dias 1-5'])}, 16-20 {pz(R['E8_sin_marcadas']['dias 16-20'])}, crece {n(R['E8_sin_marcadas']['crece'], 2)} con ee {n(R['E8_sin_marcadas']['ee_de_la_diferencia'], 2)} → {'pasa' if R['E8_sin_marcadas']['pasa'] else 'no pasa'}; E1, E2, E3 y E7 no dependen del puesto. **{'Ninguna predicción cambia de resultado entre las dos cuentas.' if not R['cambian_entre_las_dos_cuentas'] else 'Cambian de resultado entre las dos cuentas: ' + ', '.join(R['cambian_entre_las_dos_cuentas']) + '.'}** Sin excluir nada (ni cortes): E4 {'pasa' if R['E4_sin_excluir']['pasa'] else 'no pasa'}, E5 {'pasa' if R['E5_sin_excluir']['pasa'] else 'no pasa'}, E8 {'pasa' if R['E8_sin_excluir']['pasa'] else 'no pasa'}. Partidas marcadas: {', '.join(f'serie {s} día {d} {b}' for s, d, b in R['partidas_marcadas'])}.

**Lectura del sello.** Lo que P7-24 no tenía y este campo sí: **la que recuerda ya no se hunde** (E8): APRENDE − BORRADO pasa de {n(R['E8']['dias 1-5']['media'], 2)} puestos en los días 1-5 a {n(R['E8']['dias 16-20']['media'], 2)} en los días 16-20 (en P7-24, de +0,9 a +4,0), y APRENDE − TECHO de {n(R['E4']['dias 1-5']['media'], 2)} a {n(R['E4']['dias 16-20']['media'], 2)}: al final del campo la que recuerda queda por delante de las otras dos, y E4 no pasa solo porque en los días 1-5 no estaba peor que el techo por más de 2 errores estándar (su primera mitad: no hay nada que recuperar). E5 pasa en la primera cuenta y no en la segunda porque BORRADO − TECHO es cero en los dos bloques ({n(R['E5']['dias 1-5']['media'], 2)} y {n(R['E5']['dias 16-20']['media'], 2)}): la regla "≥ la mitad" no distingue nada cuando la diferencia de partida es nula o negativa; es la única predicción que cambia entre las dos cuentas y cambia por eso. E6 pasa (vida al abrir el botiquín {n(R['E6']['APRENDE']['mediana'], 0)} frente a {n(R['E6']['BORRADO']['mediana'], 0)}). E7 no pasa por una criatura: {R['E7']['llegan_a_35']} de 4 llegan a 35 ({', '.join(n(x['creencia_dentro_dia_20'], 1) for x in R['E7']['criaturas'].values())}; en P7-24 el techo del campo era 29,9). E1, E2 y E3 siguen sin pasar como en P7-24: la ignorancia baja en las cuatro ({R['E1']['ignorancia_menor_0_3_al_dia_10']} de 4 al día 10) pero los recuerdos firmes del botiquín son pocos ({', '.join(str(x['firmes_al_acabar_el_dia_5']['botiquin']) for x in R['E1']['criaturas'].values())} al día 5): el cuerpo sigue usando casi siempre entero y aprendiendo "al menos".

## Sección 1 · El campo tal como se jugó

- 3 brazos × 20 días × 2 series = {len(E['peticiones'])} partidas pedidas, la misma semilla para los tres brazos cada día (`semillas_P7_30.json`: k = {S['k'][0]}-{S['k'][-1]}; serie 2 en orden inverso). {len(L)} vidas con diario.
- Partidas con corte de la plataforma: **{len(corte)}**{(' (' + ', '.join(f'serie {s} día {d} {b}' for s, d, b in sorted(corte)) + '); el aprendizaje de esas vidas cuenta hasta el corte y la partida entera (' + str(R['vidas_fuera_de_puesto']) + ' vidas) sale de puesto, vida al morir y causa; en las emparejadas se quita el par') if corte else ''}.
- Guarda de latencia (mesa, P7-30): vidas que no pasan: {sum(LT[b]['no_pasan'] for b in LT)} de {len(L)} ({', '.join(f"{b} {LT[b]['no_pasan']}" for b in LT)}). Tiempo de decisión por brazo (mediana de medianas · p95 máximo · máximo): {', '.join(f"{b} {n(LT[b]['ms_mediana_media'], 2)} · {n(LT[b]['ms_p95_max'], 1)} · {n(LT[b]['ms_max'], 1)} ms" for b in LT)}; decisiones por encima del tic (media de vidas): {', '.join(f"{b} {n(100 * LT[b]['sobre_el_tic_media'], 2)} %" for b in LT)}; pasos listos bloqueados sin cuerpo (media): {', '.join(f"{b} {n(100 * LT[b]['sin_cuerpo_media'], 2)} %" for b in LT)}.

{chr(10).join(TL)}

## Sección 2 · Las medidas, por brazo y bloque de días

{chr(10).join(T1)}

TECHO sabe y no escribe recuerdos: sus usos del botiquín salen de los canales del diario (definiciones de P7-21), como en P7-24.

## Sección 3 · E1, E2, E3 y E7 de cerca (las 4 criaturas de APRENDE)

**E1.**

{E1t()}

**E2.**

{E2t()}

**E3.**

{E3t()}

**E7.**

{E7t()}

**Por criatura y día** (creencia e ignorancia al cerrar el día; firmes, «al menos» y cortes aparte):

{chr(10).join(TD)}

Cortes del botiquín y de la ración en APRENDE ({len(causas)} recuerdos del acto), por causa: {', '.join(f'{k}: {v}' for k, v in cc.most_common(8)) or '—'}.

## Sección 4 · El puesto (E4, E5, E8)

{chr(10).join(T4)}

Figuras: `P7_30_fig_puesto.png` (el puesto por día) y `P7_30_fig_creencias.png` (creencia e ignorancia por día de cada criatura, APRENDE y BORRADO).

## Sección 5 · Lo aprendido y la conducta (E6, y el cuánto al usar)

Vida al abrir el botiquín en los días 11-20: APRENDE mediana {n(R['E6']['APRENDE']['mediana'], 0)} en {R['E6']['APRENDE']['aperturas']} aperturas; BORRADO {n(R['E6']['BORRADO']['mediana'], 0)} en {R['E6']['BORRADO']['aperturas']}. Con cuánta vida usa APRENDE el botiquín cuando le pesa la curiosidad del cuánto (lo que le falta es mayor que lo más alto que sabe que da): {CU['le_pesa']['n']} aperturas, vida mediana {n(CU['le_pesa']['vida_mediana'], 0)}; cuando lo conoce y no le pesa: {CU['no_le_pesa_conocido']['n']}, mediana {n(CU['no_le_pesa_conocido']['vida_mediana'], 0)}; sin conocerlo aún: {CU['sin_conocer']['n']}, mediana {n(CU['sin_conocer']['vida_mediana'], 0)}.

## Sección 5b · Las vidas lentas y el puesto (mesa, P7-30); el sesgo de E4

{chr(10).join(["| brazo | vidas | correlación de rangos: decisiones sobre el tic ~ puesto | ~ muere | marcadas por la guarda: n · puesto medio · mueren · tic de muerte (mediana) | no marcadas: n · puesto medio · mueren · tic de muerte |", "|---|---:|---:|---:|---|---|"] + [f"| {b} | {x['vidas']} | {n(x['spearman_sobre_el_tic_vs_puesto'], 2)} | {n(x['spearman_sobre_el_tic_vs_muere'], 2)} | {x['marcadas']['n']} · {n(x['marcadas']['puesto_medio'], 2)} · {x['marcadas']['mueren']} · {n(x['marcadas']['tic_muerte_mediana'], 0)} | {x['no_marcadas']['n']} · {n(x['no_marcadas']['puesto_medio'], 2)} · {x['no_marcadas']['mueren']} · {n(x['no_marcadas']['tic_muerte_mediana'], 0)} |" for b, x in R['lentas_vs_puesto'].items()])}

Las doce vidas más lentas de APRENDE (decisiones sobre el tic · ms mediana · puesto · muerte): {'; '.join(f"s{z['serie']} d{z['dia']} a{z['asiento']}: {n(100 * (z['sobre_el_tic'] or 0), 2)} % · {n(z['ms_mediana'], 1)} · {n(z['puesto'], 0)} · {('tic ' + n(z['tic'], 0)) if z['murio'] else 'vive'}" for z in R['lentas_vs_puesto']['APRENDE']['por_vida'])}.

**Declaración (mesa, P7-30):** APRENDE y BORRADO cargan con el coste de las piezas del siete en cada candidato (decisión a {n(LT['APRENDE']['ms_mediana_media'], 1)} y {n(LT['BORRADO']['ms_mediana_media'], 1)} ms de mediana frente a {n(LT['TECHO']['ms_mediana_media'], 1)} de TECHO; decisiones por encima del tic {n(100 * LT['APRENDE']['sobre_el_tic_media'], 2)} % y {n(100 * LT['BORRADO']['sobre_el_tic_media'], 2)} % frente a {n(100 * LT['TECHO']['sobre_el_tic_media'], 2)} %) y TECHO no; cuando una decisión llega tarde el mundo la aplica tarde y el cuerpo pierde pasos. Por eso **E4 (APRENDE − TECHO) está inclinada en contra de APRENDE**, y E5 (BORRADO − TECHO) en contra de BORRADO; E8 (APRENDE − BORRADO) compara dos brazos con la misma carga.

## Sección 5c · Lo que esto dice, y lo que queda para la mesa

1. **El arreglo de P7-29 hace lo que decía.** `ir_curioso` con el paso listo: mediana del {n(bloque('APRENDE', range(16, 21))['curioso'], 1)} % en los días 16-20 (P7-24: 39 %); la decisión de APRENDE a {n(LT['APRENDE']['ms_mediana_media'], 1)} ms de mediana con el {n(100 * LT['APRENDE']['sobre_el_tic_media'], 2)} % de decisiones sobre el tic (P7-24, días 16-20: 31 ms y 32 %); y el puesto de la que recuerda ya no cae con los días (E8). Las vidas lentas no acaban peor (correlación de rangos entre decisiones sobre el tic y puesto: {n(R['lentas_vs_puesto']['APRENDE']['spearman_sobre_el_tic_vs_puesto'], 2)} en APRENDE).
2. **Lo que aprende sigue siendo flojo y "al menos".** Creencia del botiquín dentro al día 20: {', '.join(n(x['creencia_dentro_dia_20'], 1) for x in R['E7']['criaturas'].values())} de 50 (sin cortes, arreglo 3; en P7-24, 9,5-17,6 con cortes); firmes del botiquín en 20 días: {', '.join(str(v['recuerdos_al_acabar']['botiquin']['firmes']) for v in sorted((v for v in L if v['brazo'] == 'APRENDE' and v['dia'] == 20), key=lambda v: (v['serie'], v['slot'])))} por criatura, frente a {', '.join(str(v['recuerdos_al_acabar']['botiquin']['al_menos']) for v in sorted((v for v in L if v['brazo'] == 'APRENDE' and v['dia'] == 20), key=lambda v: (v['serie'], v['slot'])))} "al menos" y {', '.join(str(v['recuerdos_al_acabar']['botiquin']['cortes']) for v in sorted((v for v in L if v['brazo'] == 'APRENDE' and v['dia'] == 20), key=lambda v: (v['serie'], v['slot'])))} cortes (guardados aparte como actos, {len(causas)} en total, todos por daño: {', '.join(f'{k}: {v}' for k, v in cc.most_common(3))}).
3. **El cuánto hace lo que se diseñó:** cuando le pesa (lo que le falta es mayor que lo más alto que sabe que da el botiquín), lo abre con una vida mediana de {n(CU['le_pesa']['vida_mediana'], 0)} ({CU['le_pesa']['n']} aperturas); cuando no, con {n(CU['no_le_pesa_conocido']['vida_mediana'], 0)} ({CU['no_le_pesa_conocido']['n']}). La ignorancia del cuánto del botiquín al día 20: {', '.join(n(x, 3) for x in (v['al_acabar']['botiquin']['ignorancia_cuanto'] for v in sorted((v for v in L if v['brazo'] == 'APRENDE' and v['dia'] == 20), key=lambda v: (v['serie'], v['slot']))))}; la de la ración, {', '.join(n(x, 3) for x in (v['al_acabar']['racion']['ignorancia_cuanto'] for v in sorted((v for v in L if v['brazo'] == 'APRENDE' and v['dia'] == 20), key=lambda v: (v['serie'], v['slot']))))}.
4. **Lo que queda para la mesa:** E5 está mal planteada cuando BORRADO no empieza peor que TECHO; E4 está inclinada en contra de APRENDE por la carga de las piezas (sección 5b); las inundaciones del mundo (P7-31) explican las 2 partidas marcadas por pasos bloqueados sin cuerpo y el cuerpo congelado no las lee; el recuerdo firme sigue siendo la pieza que falta para que la creencia del botiquín llegue a su cura.

## Sección 6 · Créditos

Plataforma: {n(coste, 4)} USD en {len(E['peticiones'])} partidas del campo ({n(coste / max(1, len(E['peticiones'])), 4)} por partida) + {n(coste_humo, 4)} USD del humo de freno (3 partidas). Acumulado del siete en la plataforma: {n(ACUM_ANTES, 4)} (hasta P7-29b, con el día 1 del humo) + {n(coste_humo - 0.108853, 4)} (días 2 y 3 del humo) + {n(coste, 4)} = **{n(ACUM_ANTES + coste_humo - 0.108853 + coste, 4)} USD**. Consola de Anthropic: 0. Saldos no consultados.
"""
assert "§" not in T; open(os.path.join(AQUI, "informe_P7_30.md"), "w").write(T); print("informe_P7_30.md", len(T.splitlines()), "lineas")
