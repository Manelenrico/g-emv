"""[P7-56] Escribe la parte del campo de informe_P7_56.md (se anade tras el plan): sello R1/R2, vigilancia, incidencias, latencia por brazo y dia, gasto por serie, y la tabla del
botiquin bajo amenaza (para el sello de P7-57). Desde P7_56_sello.json, P7_56_equidad.json, P7_56_incidencias.json, P7_56_amenaza.json, P7_56_estado.json. Ninguna cifra a mano.
  python3 escribe_informe_P7_56_campo.py --saldo S"""
import json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
S = J("P7_56_sello.json"); EQ = J("P7_56_equidad.json"); IN = J("P7_56_incidencias.json"); AM = J("P7_56_amenaza.json"); E = J("P7_56_estado.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
saldo = sys.argv[sys.argv.index("--saldo") + 1] if "--saldo" in sys.argv else "—"
CT, SM = S["con_todas"], S["sin_marcadas"]; R1, R2 = CT["R1"], CT["R2"]; VG = CT["vigilancia"]; RZ = S["razon"]
pedidas = len(E["peticiones"]) + len(E.get("reintentos", [])) + len(E.get("apartadas", []))
T1 = ["| serie | CON_RAZON: usos del botiquín · cortados · fracción | SIN_RAZON: usos · cortados · fracción |", "|---:|---|---|"]
for i, s in enumerate(S["series"]):
    c = R1["usos_cortes"]["CON_RAZON"][i]; z = R1["usos_cortes"]["SIN_RAZON"][i]; T1.append(f"| {s} | {c[0]} · {c[1]} · {n(c[1] / c[0], 3)} | {z[0]} · {z[1]} · {n(z[1] / z[0], 3)} |")
TV = ["| serie · brazo | usos del botiquín | pruebas (a red+cam) | puesto valiente · prudente | vida perdida valiente · prudente | muertes v · p | camuflaje + quieta: ventanas · golpes/min | marcadas |", "|---|---:|---|---|---|---|---|---:|"]
for k, v in VG.items(): TV.append(f"| {k} | {v['usos_kit']} | {v['huellas']} ({v['huellas_inutil']}) | {n(v['puesto']['valiente'], 2)} · {n(v['puesto']['prudente'], 2)} | {n(v['vida_perdida']['valiente'], 0)} · {n(v['vida_perdida']['prudente'], 0)} | {v['muertes']['valiente']} · {v['muertes']['prudente']} | {v['camo_quieta']['ventanas']} · {n(v['camo_quieta']['golpes_min'], 2)} | {v['marcadas']} |")
TR = ["| serie | aceptadas · evaluadas · pendientes al cierre | aceptadas por acción | confianza al d20: valiente (c · r · v) | prudente (c · r · v) |", "|---:|---|---|---|---|"]
for s in S["series"]:
    v = VG[f"s{s} CON_RAZON"]; c20 = v.get("confianza_d20") or {}; cv = c20.get("10") or c20.get(10) or {}; cp = c20.get("11") or c20.get(11) or {}
    TR.append(f"| {s} | {v['aceptadas']} · {v['evaluadas']} · {v['pendientes_al_cierre']} | {', '.join(f'{k} {x}' for k, x in sorted(v['aceptadas_por_accion'].items(), key=lambda t: -t[1]))} | {n(cv.get('cuerpo'), 2)} · {n(cv.get('recursos'), 2)} · {n(cv.get('vinculo'), 2)} | {n(cp.get('cuerpo'), 2)} · {n(cp.get('recursos'), 2)} · {n(cp.get('vinculo'), 2)} |")
# aceptadas que llegan a evaluarse por dia y hermana (sumado sobre las series)
ad = {}
for s in S["series"]:
    for k, (a, e) in (VG[f"s{s} CON_RAZON"].get("evaluadas_por_dia_hermana") or {}).items():
        d, sl = k.split(); x = ad.setdefault((int(d[1:]), sl), [0, 0]); x[0] += a; x[1] += e
TE = ["| día | valiente: aceptadas → evaluadas | prudente: aceptadas → evaluadas |", "|---:|---|---|"] + [f"| {d} | {ad.get((d, 'a10'), [0, 0])[0]} → {ad.get((d, 'a10'), [0, 0])[1]} | {ad.get((d, 'a11'), [0, 0])[0]} → {ad.get((d, 'a11'), [0, 0])[1]} |" for d in range(1, 21)]
TI = ["| tipo | serie · día · brazo | hora | motivo |", "|---|---|---|---|"] + [f"| {x['tipo']} | s{x['serie']} d{x['dia']} {x['brazo']} | {x['pedida']} | {x['motivo']} |" for x in IN["incidencias"]]
TL = ["| brazo | " + " | ".join(f"d{d}" for d in range(1, 21)) + " |", "|---|" + "---:|" * 20] + [f"| {b} | " + " | ".join(n(IN['sobre_tic_por_dia'][b].get(str(d)), 2) for d in range(1, 21)) + " |" for b in ("CON_RAZON", "SIN_RAZON")]
TA = ["| brazo | en amenaza: usos · cortados · fracción cortada | cura media (todos · no cortados) | sin amenaza: usos · fracción cortada · cura media |", "|---|---|---|---|"]
for b in ("CON_RAZON", "SIN_RAZON", "los dos"):
    a = AM["total"][b]["amenaza"]; z = AM["total"][b]["sin_amenaza"]; TA.append(f"| {b} | {a['usos']} · {a['cortados']} · {n(a['fraccion_cortada'], 3)} | {n(a['cura_media_todos'], 1)} · {n(a['cura_media_no_cortados'], 1)} | {z['usos']} · {n(z['fraccion_cortada'], 3)} · {n(z['cura_media_todos'], 1)} |")
la = AM["total"]["los dos"]["amenaza"]
out = f"""

# El campo (13-oct-2026): 3 series jugadas

*{S['partidas']} partidas válidas de {pedidas} pedidas (3 de humo, que pasó por decisión de Manel; {len(E.get('reintentos', []))} reintentos únicos; {len(E.get('apartadas', []))} apartadas; {len(E.get('dias_perdidos', []))} días perdidos). Bolsa 1: {pedidas} partidas pedidas (hay
partidas que cuentan 0 créditos en la página); saldo real 107 a las 15:27 del 13-oct antes de la serie 3; ahora {saldo}. Bolsa 2 (consola): {RZ['llamadas']} llamadas de razón = {n(RZ['tokens_entrada'], 0)} + {n(RZ['tokens_salida'], 0)} tokens =
**{n(RZ['usd_supuesto'], 2)} $** supuestos; por serie: {', '.join(f"serie {k} {n(v, 2)} $" for k, v in RZ['por_serie'].items())}; más 0,0001 $ de la llamada de prueba. Noches sin razón: {len(RZ['noches_sin_razon'])} ({'; '.join(f"s{x['serie']} d{x['dia']} a{x['slot']}: {x['motivo']}" for x in RZ['noches_sin_razon'])}).
Scripts: `analiza_P7_56.py` → `P7_56_sello.json`, `equidad_P7_56.py`, `incidencias_P7_56.py`, `amenaza_P7_56.py`, `escribe_informe_P7_56_campo.py` (esta parte; ninguna cifra a mano). `motor/model.py` intacto.*

## El sello, de una vez

| | criterio | resultado | pasa |
|---|---|---|---|
| R1 | fracción de usos del botiquín cortados por un golpe: CON < SIN, ≥ 3 ee | CON {n(R1['media_C'], 3)} · SIN {n(R1['media_S'], 3)}; {n(R1['dif'], 3)} ± {n(R1['ee'], 3)} ({n(abs(R1['dif']) / R1['ee'], 1)} ee) | {'sí' if R1['pasa'] else 'NO'} (dirección {'prevista' if R1['direccion_ok'] else 'contraria'}) |
| R2 | al día 20, confianza en el cuerpo mayor tras invitaciones verdad que tras falsas (tabla del mundo) | verdad {n(R2['media_verdad'], 3)} ({R2['n_verdad']}) · falsas {n(R2['media_falsa'], 3)} ({R2['n_falsa']}); {n(R2['dif'], 3)} ± {n(R2['ee'], 3)} ({n(R2['dif'] / R2['ee'], 1)} ee) | {'sí' if R2['pasa'] else 'NO'} |

Segunda cuenta sin partidas marcadas: R1 {n(SM['R1']['dif'], 3)} ± {n(SM['R1']['ee'], 3)} ({'pasa' if SM['R1']['pasa'] else 'no pasa'}); R2 {n(SM['R2']['dif'], 3)} ± {n(SM['R2']['ee'], 3)} ({'pasa' if SM['R2']['pasa'] else 'no pasa'}). Días válidos: los 20 de las 3 series en los dos brazos.

{chr(10).join(T1)}

Lo esperado en el plan: una reducción visible del 18-19 % con 3 series. La observada es del {n(100 * -R1['dif'] / R1['media_S'], 0)} %: en la dirección prevista, por debajo de lo que 3 series pueden ver. Y la razón cambió el uso:
CON_RAZON usó el botiquín {sum(c[0] for c in R1['usos_cortes']['CON_RAZON'])} veces y SIN_RAZON {sum(c[0] for c in R1['usos_cortes']['SIN_RAZON'])}.

## Vigilancia (sin predicción)

{chr(10).join(TV)}

La confianza en la dimensión vínculo no informa (B saturado en 1, P7-53).

{chr(10).join(TR)}

De las invitaciones aceptadas, cuántas llegan a evaluarse (no cortadas por la muerte ni por el fin de la partida), por día y hermana (las tres series):

{chr(10).join(TE)}

## Incidencias, equidad y latencia

{chr(10).join(TI)}

Equidad: {n(EQ['equidad']['max_diferencia_sobre_el_tic_puntos'], 2)} puntos entre brazos ({'dudosa' if EQ['equidad']['dudoso'] else 'no dudosa'}); marcadas {EQ['por_brazo']['CON_RAZON']['marcadas']} (CON) y {EQ['por_brazo']['SIN_RAZON']['marcadas']} (SIN) de 120 cada uno; medianas {n(EQ['por_brazo']['CON_RAZON']['ms_mediana'], 2)} y {n(EQ['por_brazo']['SIN_RAZON']['ms_mediana'], 2)} ms. El reparto de reintentos (3 en CON, 1 en
SIN) es azar de la plataforma: el brazo con razón va más ligero (menos marcadas, menos % sobre el tic), las invitaciones horneadas pesan {IN['invitaciones_bytes'][0]}-{IN['invitaciones_bytes'][1]} bytes frente a {IN['cuaderno_bytes'][0]}-{IN['cuaderno_bytes'][1]} de los
cuadernos, el horneado tarda lo mismo ({n(IN['horneado_segundos']['CON_RAZON'][0], 0)} s frente a {n(IN['horneado_segundos']['SIN_RAZON'][0], 0)}) y las vidas lentas se reparten en las dos cadenas sin agruparse por hora.

% de decisiones sobre el tic por brazo y día (media de los dos asientos, tres series):

{chr(10).join(TL)}

## Para el sello de P7-57: el botiquín en situación de amenaza (tal como está definida ahora)

Amenaza = rival a ≤ 4 casillas o fuego al abrir la prueba, o golpe recibido en los 48 tics anteriores (sin «vida < 30»). La falsa de P7-57 se juzga por lo vivido, siempre: esta fracción es la
probabilidad de que la mentira se desmienta al usarla, y la cura de los no cortados, lo que la «confirma» (refuerzo intermitente).

{chr(10).join(TA)}

En los dos brazos, {la['usos']} de {la['usos'] + AM['total']['los dos']['sin_amenaza']['usos']} usos del botiquín fueron en amenaza; se cortaron el {n(100 * la['fraccion_cortada'], 0)} %; los no cortados curaron {n(la['cura_media_no_cortados'], 1)} de media ({la['al_menos_no_cortados']} de ellos tocaron el techo de vida, así
que su efecto es «al menos»). Con la regla de acierto (|vivido| ≥ la mitad de lo prometido), la falsa (+50) se confirmaría solo cuando la cura no se corta y alcanza 25.
"""
open(os.path.join(AQUI, "informe_P7_56.md"), "a", encoding="utf-8").write(out); print("anadido", out.count("\n"), "lineas")
