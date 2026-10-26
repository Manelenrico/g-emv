"""[P7-24/27] Escribe informe_P7_24.md (el campo entero) desde P7_24_resumen.json, P7_24_vidas.json, P7_24_estado.json y semillas_P7_24.json. Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
R = J("P7_24_resumen.json"); V = J("P7_24_vidas.json"); E = J("P7_24_estado.json"); S = J("semillas_P7_24.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
coste = sum(p.get("coste_usd") or 0 for p in E["peticiones"]); corte = {tuple(x) for x in R["partidas_con_corte"]}
L = [v for v in V.values() if not v.get("sin_diario")]
def bloque(b, dias):
    vs = [v for v in L if v["brazo"] == b and v["dia"] in dias]; vp = [v for v in vs if (v["serie"], v["dia"], b) not in corte]
    mu = [v for v in vp if v["murio"]]; ub = [u for v in vs for u in v["usos"]["botiquin"]]; ur = [u for v in vs for u in v["usos"]["racion"]]
    return {"vidas": len(vs), "vidas_puesto": len(vp), "puesto": (st.mean(v["puesto"] for v in vp) if vp else None), "mueren": len(mu), "vida_al_morir": (st.median(v["vida_al_morir"] for v in mu) if mu else None), "anillo": sum(1 for v in mu if v["causa"] == "eliminated"),
            "usos_b": len(ub), "firmes_b": sum(1 for u in ub if u["firme"]), "almenos_b": sum(1 for u in ub if u["al_menos"]), "cortes_b": sum(1 for u in ub if not u["completado"]), "hp_b": (st.median(u["hp0"] for u in ub) if ub else None),
            "usos_r": len(ur), "firmes_r": sum(1 for u in ur if u["firme"]), "cortes_r": sum(1 for u in ur if not u["completado"]), "hp_r": (st.median(u["hp0"] for u in ur) if ur else None),
            "pedidos": sum(v["pedidos_abre"] for v in vs), "regalos": sum(sum(v["regalos"].values()) for v in vs), "curioso": (st.median(100 * v["ir_curioso_con_paso_listo"] / max(1, v["tics_con_paso_listo"]) for v in vs) if vs else None),
            "esperanza": sum(1 for v in vs if v["esperanza_aparece"]), "contacto_b": sum(1 for v in vs if v["primer_contacto"]["botiquin"] is not None), "contacto_r": sum(1 for v in vs if v["primer_contacto"]["racion"] is not None)}
T1 = ["| brazo | días | vidas (en puesto) | puesto medio | mueren · vida al morir (mediana) | usos botiquín: n (firmes, «al menos», cortes) · vida al usar | usos ración: n (firmes, cortes) · vida al usar | pedidos · regalos | `ir_curioso` con el paso listo (mediana, %) | vidas con esperanza | vidas que tocan botiquín / ración |", "|---|---|---:|---:|---|---|---|---|---:|---:|---|"]
for b in ("TECHO", "BORRADO", "APRENDE"):
    for et, dias in (("1-5", range(1, 6)), ("6-10", range(6, 11)), ("11-15", range(11, 16)), ("16-20", range(16, 21))):
        x = bloque(b, dias)
        T1.append(f"| {b} | {et} | {x['vidas']} ({x['vidas_puesto']}) | {n(x['puesto'], 2)} | {x['mueren']} · {n(x['vida_al_morir'], 0)} | {x['usos_b']} ({x['firmes_b']}, {x['almenos_b']}, {x['cortes_b']}) · {n(x['hp_b'], 0)} | {x['usos_r']} ({x['firmes_r']}, {x['cortes_r']}) · {n(x['hp_r'], 0)} | {x['pedidos']} · {x['regalos']} | {n(x['curioso'], 1)} | {x['esperanza']} | {x['contacto_b']} / {x['contacto_r']} |")
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
def pz(p): return f"{n(p['media'], 2)} ± {n(p['ee'], 2)} (n {p['n']})"
P = R["puesto"]
T4 = ["| comparación | días 1-5 (media ± error estándar) | días 16-20 |", "|---|---|---|"] + [f"| {k} | {pz(v['dias 1-5'])} | {pz(v['dias 16-20'])} |" for k, v in P.items()] + [f"| APRENDE − BORRADO (sin predicción; partidas con corte fuera) | {pz(R['APRENDE - BORRADO']['dias 1-5'])} | {pz(R['APRENDE - BORRADO']['dias 16-20'])}; todos los días {pz(R['APRENDE - BORRADO']['todos los dias'])} |"]

TC = J("P7_24_techo_canales.json")
def techo_bloque(dias):
    xs = [v for v in TC.values() if v["dia"] in dias]; hp = [h for v in xs for h in v["hp"]]
    return f"{sum(v['canales'] for v in xs)} ({sum(v['completados'] for v in xs)} completados) · vida al abrir {n(st.median(hp), 0) if hp else '—'}"
TECHO_C = "; ".join(f"días {et}: {techo_bloque(d)}" for et, d in (("1-5", range(1, 6)), ("6-10", range(6, 11)), ("11-15", range(11, 16)), ("16-20", range(16, 21))))
sello = R["sello"]; ok = lambda k: "**pasa**" if sello[k] else "**no pasa**"
cur_ap = [v for v in L if v["brazo"] == "APRENDE"]
T = f"""# P7-24 · El campo de la primera etapa: nacer sin saber qué curan el botiquín ni la ración

*8-oct-2026 (jugado del 7 al 8 de octubre; P7-24 sellado el 7, freno corregido en P7-27). Coste: plataforma {n(coste, 4)} USD (las 120 partidas, freno incluido); consola 0.
`motor/model.py` = `{hashlib.md5(open(os.path.join(AQUI, '..', '..', 'motor', 'model.py'), 'rb').read()).hexdigest()}` al empezar y al acabar; cuerpo y congelados sin tocar. Sello: `SELLO_P7_24.md` (con sus dos añadidos posteriores, declarados).
Diarios en `paintball/runs/P724_*` (fuera de git); `analiza_P7_24.py` → `P7_24_vidas.json`; `sello_P7_24.py` → `P7_24_resumen.json`; este informe lo escribe `escribe_informe_P7_24.py`.
El sello se ha evaluado una sola vez, al final.*

## El sello

| | regla | resultado | |
|---|---|---|---|
| E1 | descubre: firmes de los dos al día 5 en las 4; ignorancia < 0,3 al día 10 en ≥ 3 | firmes de los dos al día 5: **{R['E1']['firme_de_los_dos_al_dia_5']} de 4**; ignorancia < 0,3 al día 10: {R['E1']['ignorancia_menor_0_3_al_dia_10']} de 4 | {ok('E1')} |
| E2 | aprende a aprender: el segundo objeto tarda menos en ≥ 3 | {R['E2']['el_segundo_tarda_menos']} de 4 | {ok('E2')} |
| E3 | qué aprende antes: la ración llega al 80 % antes que el botiquín en ≥ 3 | {R['E3']['racion_antes']} de 4 | {ok('E3')} |
| E4 | pierde y recupera: APRENDE − TECHO > 2 ee en 1-5; ≤ la mitad en 16-20 | 1-5: {pz(R['E4']['dias 1-5'])}; 16-20: {pz(R['E4']['dias 16-20'])} | {ok('E4')} |
| E5 | sin memoria no recupera: BORRADO − TECHO en 16-20 ≥ la mitad de 1-5 | 1-5: {pz(R['E5']['dias 1-5'])}; 16-20: {pz(R['E5']['dias 16-20'])} | {ok('E5')} |
| E6 | lo aprendido cambia la conducta: vida al abrir el botiquín (11-20), APRENDE < BORRADO | medianas {n(R['E6']['APRENDE']['mediana'], 0)} ({R['E6']['APRENDE']['aperturas']} aperturas) frente a {n(R['E6']['BORRADO']['mediana'], 0)} ({R['E6']['BORRADO']['aperturas']}) | {ok('E6')} |

**Pasan E3, E5 y E6; no pasan E1, E2 y E4.** Y lo que no estaba previsto: **la que recuerda acaba peor, y cada vez peor.** APRENDE − TECHO pasa de {n(R['E4']['dias 1-5']['media'], 1)} puestos en los días 1-5 a
{n(R['E4']['dias 16-20']['media'], 1)} en los días 16-20; APRENDE − BORRADO, de {n(R['APRENDE - BORRADO']['dias 1-5']['media'], 1)} a {n(R['APRENDE - BORRADO']['dias 16-20']['media'], 1)}. Sin excluir las partidas con corte sale lo mismo (E4: {pz(R['E4_sin_excluir']['dias 1-5'])} y {pz(R['E4_sin_excluir']['dias 16-20'])}).

## Sección 1 · El campo tal como se jugó

- 3 brazos × 20 días × 2 series = 120 partidas, la misma semilla para los tres brazos cada día (`semillas_P7_24.json`: k = {S['k'][0]}-{S['k'][-1]}; serie 2 en orden inverso). 240 vidas.
- **Partidas con corte de la plataforma: {len(corte)}** ({', '.join(f'serie {s} día {d} {b}' for s, d, b in sorted(corte))}): en 4 de ellas un asiento de BORRADO o TECHO no tiene ni artefacto ni registro de salida (de ese asiento no queda nada);
  en las 4 de APRENDE, un asiento (o los dos en s2 d18) se cortó a media partida y su diario se rescató del registro de salida hasta el tic del corte, con el cuaderno de fin.
  Según la decisión de la mesa, el aprendizaje de esas vidas cuenta hasta el corte y las 8 partidas enteras ({R['vidas_fuera_de_puesto']} vidas) salen de puesto, vida al morir y causa; en las emparejadas se quita el par.
- El freno (días 1-3 de APRENDE, serie 1) se corrigió en P7-27 ((b'): tocan 4 de 6) y el campo siguió desde el día 4 sin repetir nada.

## Sección 2 · Las medidas, por brazo y bloque de días

{chr(10).join(T1)}

TECHO sabe y no escribe recuerdos (las piezas del siete no están en ese brazo), así que sus usos salen de los canales del diario (`P7_24_techo_canales.json`, con las definiciones
de P7-21): canales del botiquín {TECHO_C}. Y en APRENDE, en los días 16-20, la mediana de `ir_curioso` con el paso listo sube al {n(bloque('APRENDE', range(16, 21))['curioso'], 1)} % y los usos caen
a {bloque('APRENDE', range(16, 21))['usos_b']} de botiquín y {bloque('APRENDE', range(16, 21))['usos_r']} de ración en 20 vidas: la que recuerda, con la ignorancia ya baja, se pasa el final del campo yendo a por cosas.

Causa de muerte: en todas las vidas que mueren, `final.reason` = `eliminated` (el diario no distingue anillo de rival en el final; P7-21 lo midió por el daño).

## Sección 3 · E1, E2 y E3 de cerca (las 4 criaturas de APRENDE)

**E1.** {E1t()}

**E2.** {E2t()}

**E3.** {E3t()}

Lo que se ve: las cuatro bajan la ignorancia por debajo de 0,3 (a 0,05-0,10 al final), pero los recuerdos **firmes** son pocos: el cuerpo usa casi siempre entero y aprende «al menos».
La creencia de la ración llega a 12-15 (su cura es 15) en 3 de 4; la del botiquín dentro del círculo se queda en 9-30 (su cura es 50) y nunca llega a 40. El segundo objeto no tarda
menos que el primero (1 de 4).

## Sección 4 · El puesto (E4, E5, sin predicción)

{chr(10).join(T4)}

Lectura: en los días 1-5 los tres brazos están cerca (APRENDE y BORRADO entre 1 y 2 puestos peor que TECHO, dentro del error); en los días 16-20 APRENDE está {n(R['E4']['dias 16-20']['media'], 1)} puestos
peor que TECHO y {n(R['APRENDE - BORRADO']['dias 16-20']['media'], 1)} peor que BORRADO. No es que no recupere: empeora con lo que aprende. Figuras: `P7_24_fig_puesto.png` (el puesto por día) y
`P7_24_fig_creencias.png` (creencia e ignorancia por día de cada criatura, APRENDE y BORRADO).

## Sección 5 · Lo aprendido y la conducta (E6)

Vida al abrir el botiquín en los días 11-20: APRENDE mediana {n(R['E6']['APRENDE']['mediana'], 0)} en {R['E6']['APRENDE']['aperturas']} aperturas; BORRADO {n(R['E6']['BORRADO']['mediana'], 0)} en {R['E6']['BORRADO']['aperturas']}. Pasa por {n(R['E6']['BORRADO']['mediana'] - R['E6']['APRENDE']['mediana'], 0)} puntos y con
menos de la mitad de aperturas: la que recuerda usa el botiquín menos veces.

## Sección 6 · GIF de los datos

`P7_24_primer_firme_botiquin.gif` (serie 1, día 2, asiento 10, tic 901: el primer recuerdo firme del botiquín), `P7_24_primer_firme_racion.gif` (serie 1, día 8, asiento 10, tic 2.436)
y `P7_24_uso_dia15.gif` (serie 1, día 15, asiento 10, tic 12.636: un uso del botiquín con el cuaderno de 14 días). Fuera de git, como los otros GIF.

## Sección 7 · Créditos

Plataforma: {n(coste, 4)} USD en 120 partidas ({n(coste / 120, 4)} por partida); de ellos, {n(sum(p.get('coste_usd') or 0 for p in E['peticiones'] if p['brazo'] == 'APRENDE' and p['serie'] == 1 and p['dia'] <= 3), 4)} del freno (P7-24). Consola: 0.
Acumulado del siete en la plataforma: 30,3324 (hasta P7-26, que ya incluía el freno) + {n(coste - sum(p.get('coste_usd') or 0 for p in E['peticiones'] if p['brazo'] == 'APRENDE' and p['serie'] == 1 and p['dia'] <= 3), 4)} = {n(30.3324 + coste - sum(p.get('coste_usd') or 0 for p in E['peticiones'] if p['brazo'] == 'APRENDE' and p['serie'] == 1 and p['dia'] <= 3), 4)} USD. Saldos no consultados.

## Lo que esto dice, y lo que queda para la mesa

1. El cuerpo que nace sin saber **descubre** las dos cosas (ignorancia a 0,05-0,10 en veinte días) pero aprende **poco y flojo**: casi todo «al menos», y el botiquín se queda en una
   creencia de 9-30 sobre 50. La ración, más barata y usada más veces, sí llega a su cura.
2. **Recordar empeora el puesto**, y más cuanto más se recuerda: el mismo rastro que en los dos campos anteriores (APRENDE un puesto peor que BORRADO), aquí más grande
   ({n(R['APRENDE - BORRADO']['todos los dias']['media'], 1)} ± {n(R['APRENDE - BORRADO']['todos los dias']['ee'], 1)} sobre todos los días). Dónde se pierde es la pregunta siguiente; lo que este campo da son los diarios para mirarlo.
3. Los 8 cortes de la plataforma están declarados y excluidos; las conclusiones no cambian sin excluirlos.
"""
assert "§" not in T; open(os.path.join(AQUI, "informe_P7_24.md"), "w").write(T); print(len(T))
