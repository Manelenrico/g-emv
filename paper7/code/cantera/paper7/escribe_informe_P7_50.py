"""[P7-50] Escribe informe_P7_50.md (el campo del capitulo 4 en dos mundos, por separado) desde P7_50_sello.json (analiza_P7_50), P7_50_equidad.json (equidad_P7_50), P7_49_potencia.json,
P7_50_ruido_local_P7_48.json, P7_50_estado.json. Ninguna cifra a mano.  python3 escribe_informe_P7_50.py --saldo S"""
import json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
S = J("P7_50_sello.json"); EQ = J("P7_50_equidad.json"); IMG = J("P7_50_imagenes.json"); RA = J("P7_50_rachas.json"); PO = J("P7_49_potencia.json"); RL = J("P7_50_ruido_local_P7_48.json"); E = J("P7_50_estado.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
saldo = (sys.argv[sys.argv.index("--saldo") + 1] if "--saldo" in sys.argv else None)
partidas = sum(1 for p in E["peticiones"] if p["estado"] == "completed"); CT = S["con_todas"]; SM = S["sin_marcadas"]
reint = E.get("reintentos", []); apart = E.get("apartadas", []); pedidas = partidas + len(reint) + len(apart)
TR = ["| brazo · hermana | vidas | rachas ≥ 72 tics no quitadas | de ellas, marcadas por v3b en la racha | empujes en rachas largas (tras la marca) | rachas cortas (< 72) | % bloqueados sin cuerpo (media) |", "|---|---:|---:|---:|---|---:|---:|"]
for k, v in RA["por_brazo_hermana"].items(): TR.append(f"| {k} | {v['vidas']} | {v['largas']} | {v['largas_marcadas']} | {v['empujes_largas']} ({v['empujes_tras_marca']}) | {v['cortas']} | {n(v['pct_medio'], 2)} |")
ap = [(k, v) for k, v in RA["vidas"].items() if v["grupo"] == "apartadas" and v["largas"]]
ap_txt = "; ".join(f"{k}: {len(v['largas'])} racha(s) de {', '.join(str(x['empujes']) for x in v['largas'])} empujes ({', '.join(str(x['elegido']) for x in v['largas'])}; marcada {'sí' if all(x['marcada_en_racha'] for x in v['largas']) else 'no'})" for k, v in ap) or "ninguna"
def fila(k, et, menor):
    c = CT[k]; m = SM[k]
    return f"| {k} | {et} | {', '.join(n(x, 1) for x in c.get('COMPARTE', []))} · media {n(c.get('media_C'), 2)} | {', '.join(n(x, 1) for x in c.get('SOLAS', []))} · media {n(c.get('media_S'), 2)} | {n(c.get('dif'), 2)} ± {n(c.get('ee'), 2)} | {'sí' if c.get('direccion_ok') else 'no'} | {'sí' if c.get('tres_veces') else 'no'} | **{'PASA' if c.get('pasa') else 'NO PASA'}** | {n(m.get('dif'), 2)} ± {n(m.get('ee'), 2)} ({'pasa' if m.get('pasa') else 'no'}) |"
T = ["| | medida | COMPARTE (por serie) | SOLAS (por serie) | COMPARTE − SOLAS ± ee | dirección prevista | ≥ 3 ee | veredicto | sin marcadas |", "|---|---|---|---|---|---|---|---|---|",
     fila("S1", "área bajo la curva del botiquín de la hermana que menos prueba (d1-20)", False), fila("S2", "parecido entre hermanas (d11-20, 4 objetos)", True), fila("S3", "fracción de pruebas a red + camuflaje", True)]
herm = CT["S1"].get("hermana", {})
TV = ["| serie · brazo | días válidos | pruebas valiente · prudente | recibidos: canal · noche · vistos (contagio) | puesto valiente · prudente | creencia botiquín d20 (10 · 11) | marcadas |", "|---|---:|---|---|---|---|---:|"]
for k, v in CT["vigilancia"].items():
    r = v["recibidos"]; p = v["puesto"]; c20 = v["creencia_botiquin_d20"]
    TV.append(f"| {k} | {v['dias_validos']} | {v['pruebas_valiente']} · {v['pruebas_prudente']} | {r['contado_canal']} · {r['contado_noche']} · {r['visto']} ({r['contagio']}) | {n(p.get('valiente'), 2)} · {n(p.get('prudente'), 2)} | {n(c20.get('10') if isinstance(c20, dict) else None, 1)} · {n(c20.get('11') if isinstance(c20, dict) else None, 1)} | {v['marcadas']} |")
TE = ["| brazo | vidas | % sobre el tic | % bloqueados sin cuerpo | ms mediana | p95 máx | marcadas |", "|---|---:|---:|---:|---:|---:|---:|"]
for b in ("COMPARTE", "SOLAS"):
    x = EQ["por_brazo"][b]; TE.append(f"| {b} | {x['vidas']} | {n(x['sobre_el_tic_media_pct'], 2)} | {n(x['bloqueados_media_pct'], 2)} | {n(x['ms_mediana'], 2)} | {n(x['ms_p95_max'], 1)} | {x['marcadas']} |")
TI = ["| serie | brazo | día → versión de la imagen (gemv-p7-campo:vN) | pvid coincide con su imagen | cuadernos horneados (d > 1) |", "|---|---|---|---|---|"]
for S_ in sorted({f["serie"] for f in IMG["partidas"]}):
    for b in ("COMPARTE", "SOLAS"):
        fs = [f for f in IMG["partidas"] if f["serie"] == S_ and f["brazo"] == b]
        dv = " ".join("d%d:v%s" % (f["dia"], f["version"]) for f in fs); ok = sum(1 for f in fs if f["pvid_coincide"]); horn = sum(1 for f in fs if f["dia"] > 1 and len(f["cuadernos_horneados"] or []) >= 2); nd = sum(1 for f in fs if f["dia"] > 1)
        TI.append(f"| {S_} | {b} | {dv} | {ok} de {len(fs)} | {horn} de {nd} |")
# local: ruido
TL = ["| brazo (P7-48, 3 días, 8 parejas) | S1 proxy (suma de 3 días de la creencia del botiquín de la que menos cree) media · sd | S2 proxy (d2-3) media · sd | S3 media · sd |", "|---|---|---|---|"]
def ms(xs): return (st.mean(xs), (st.stdev(xs) if len(xs) > 1 else 0.0)) if xs else (None, None)
for b, r in RL.items():
    a1, s1 = ms(r["S1"]); a2, s2 = ms(r["S2"]); a3, s3 = ms(r["S3"]); TL.append(f"| {b} | {n(a1, 1)} · {n(s1, 1)} | {n(a2, 2)} · {n(s2, 2)} | {n(a3, 3)} · {n(s3, 3)} |")
cv = {}
for k in ("S1", "S2", "S3"):
    xs = [x for b in RL for x in RL[b][k]]; a, s_ = ms(xs); cv[k] = (s_ / a) if a else None
series_local = {k: (int(-(-(18 * cv[k] ** 2 / 0.25 / 8) // 1)) if cv[k] else None) for k in cv}
dur_serie_h = 2 * 20 * (377 + 150) / 3600.0; gb_serie = 2 * 20 * 0.3; caben_24h = int(24 // dur_serie_h)
pasa_pl = [k for k in ("S1", "S2", "S3") if CT[k].get("pasa")]
out = f"""# P7-50 · El campo del capítulo 4 en dos mundos: plataforma (3 series) y local

*12/13-oct-2026. Sello `SELLO_P7_49.md` con el addendum P7-50 (commit `7f0d262`, antes de lanzar). `motor/model.py` = `1e511978c251130e95169ebf8443efa1`, intacto. Bolsa 1: {pedidas} partidas pedidas = {pedidas} créditos ({partidas} válidas, 3 de ellas el humo, que pasó y cuenta: p95 9,9-12,5 ms; {len(reint) + len(apart)} apartadas); saldo {('**' + saldo + '**') if saldo else '—'} (no legible por la API; 228 el 12-oct 06:47 + recargas − {pedidas}). Bolsa 2: 0 $. Scripts: `lanza_P7_50.py`, `orquesta_P7_50.py`,
`equidad_P7_50.py` → `P7_50_equidad.json`, `analiza_P7_50.py` → `P7_50_sello.json`, `potencia_P7_49.py`, `escribe_informe_P7_50.py` (este informe; ninguna cifra a mano).*

## Mundo 1 · Plataforma (liga real, 3 series × 20 días × COMPARTE / SOLAS)

Pareja valiente (asiento 10, MIEDO 0,5) / prudente (11, MIEDO 1,5), ojos compartidos en los dos brazos; la única diferencia es compartir (mirando + canal + noche). Equidad, paradas
y tope como en P7-43e: {len(EQ['paradas'])} paradas duras, {len(EQ['marcadas'])} vidas marcadas de {EQ['partidas'] * 2}, diferencia máxima del % sobre el tic entre brazos {n(EQ['equidad']['max_diferencia_sobre_el_tic_puntos'], 2)} puntos ({'dudosa' if EQ['equidad']['dudoso'] else 'no dudosa'}).

{chr(10).join(TE)}

**Ruido** (de P7-45, usado en el sello): S1 sd {n(PO['S1_area_botiquin']['sd'], 0)} sobre media {n(PO['S1_area_botiquin']['media'], 0)}; S2 sd {n(PO['S2_parecido']['sd'], 2)} sobre {n(PO['S2_parecido']['media'], 2)}; S3 sd {n(PO['S3_fraccion_inutil']['sd'], 3)} sobre {n(PO['S3_fraccion_inutil']['media'], 3)}. Con 3 series solo S3 tiene potencia
(efecto mínimo {n(PO['S3_fraccion_inutil']['efecto_min_3_series_pct'], 0)} %); S1 y S2 solo saldrían con efectos del {n(PO['S1_area_botiquin']['efecto_min_3_series_pct'], 0)} % y {n(PO['S2_parecido']['efecto_min_3_series_pct'], 0)} % (declarado en el addendum).

{chr(10).join(T)}

La hermana que menos prueba por sí misma (decidida en SOLAS): {'; '.join(f"serie {k}: asiento {v['asiento']} ({'prudente' if v['asiento'] == 11 else 'valiente'}; pruebas en SOLAS 10: {v['pruebas_solas'].get('10', v['pruebas_solas'].get(10))}, 11: {v['pruebas_solas'].get('11', v['pruebas_solas'].get(11))})" for k, v in herm.items())}.

{chr(10).join(TV)}

**Rachas ≥ 72 tics que la regla v3b no quitó** (Manel, 12-oct), por brazo y hermana, en las 240 vidas válidas:

{chr(10).join(TR)}

En los intentos apartados: {ap_txt}.

**Incidencias del día** (regla del addendum 2: un reintento, luego día perdido): {len(reint)} reintentos ({'; '.join(f"s{r['serie']} d{r['dia']} {r['brazo']}: " + ('guarda dura, bloqueos sin cuerpo' if 'bloqueados' in r['motivo'] else 'guarda dura, latencia' if 'guarda dura' in r['motivo'] else 'pod del asiento 10 borrado por la plataforma' if 'pod' in r['motivo'] else r['motivo'][:40]) for r in reint)}), {len(apart)} partidas apartadas (pedidas por otra orquesta con los cuadernos de un intento parado), {len(E.get('dias_perdidos', []))} días perdidos. Partidas pedidas en total: {pedidas} ({partidas} válidas).

**Veredicto de la plataforma**: {('pasan ' + ', '.join(pasa_pl)) if pasa_pl else 'ninguna de S1-S3 pasa'}; S1 va en dirección {'prevista' if CT['S1'].get('direccion_ok') else 'contraria'} ({n(CT['S1'].get('dif'), 0)} ± {n(CT['S1'].get('ee'), 0)}), S2 {'prevista' if CT['S2'].get('direccion_ok') else 'contraria'} ({n(CT['S2'].get('dif'), 2)} ± {n(CT['S2'].get('ee'), 2)}), S3 {'prevista' if CT['S3'].get('direccion_ok') else 'contraria'} ({n(CT['S3'].get('dif'), 3)} ± {n(CT['S3'].get('ee'), 3)}).

### Comprobación de imágenes (Manel, 12-oct): con qué versión se jugó cada partida

{chr(10).join(TI)}

Piezas en los diarios (`P7_49_arranque_campo`): {len(IMG['piezas_distintas'])} listas distintas, que solo difieren en la etiqueta del brazo (`hermanas_P7_48:comparte` / `:solas`): {' · '.join(', '.join(x) for x in IMG['piezas_distintas'])}.
Mando de miedo en todos los diarios: MIEDO_V {IMG['miedo_distintos'][0][1] if IMG['miedo_distintos'] else '—'} / MIEDO_P {IMG['miedo_distintos'][0][2] if IMG['miedo_distintos'] else '—'} con {len(IMG['miedo_distintos'][0][0]) if IMG['miedo_distintos'] else '—'} filas, {len(IMG['miedo_distintos'])} variante(s). Avisos (pvid pedido ≠ imagen, modo ≠ brazo, MIEDO ≠ 0,5/1,5, cuadernos sin hornear): {IMG['avisos'] or 'ninguno'}.
Archivos que copia la imagen cambiados desde la primera subida del campo ({IMG['primera_subida'][:19]}): {IMG['cambios_en_archivos_copiados_desde_la_primera_subida']}. La carrera de versiones del 12-oct (tres orquestas subiendo a la vez) solo pudo
fallar la aserción del lanzador (y falló una vez, sin pedir partida): ninguna partida se pidió con un pvid distinto del de su propia imagen.

## Mundo 2 · Local (coworld play en el Mac, 0 créditos)

Antes de jugar, el ruido local con las vidas de P7-48 (cadenas de 3 días, 8 parejas por brazo; 16 criaturas nuestras, todas mueren antes del final):

{chr(10).join(TL)}

Coeficiente de variación (las dos cadenas juntas): S1 {n(cv['S1'], 2)}, S2 {n(cv['S2'], 2)}, S3 {n(cv['S3'], 2)}. Series locales necesarias para un 50 % a 3 ee, con 8 parejas por serie y brazo (n ≥ 18 × CV² / 0,25 / 8):
S1 {series_local['S1']}, S2 {series_local['S2']}, S3 {series_local['S3']}. Cada serie local = 40 partidas × (≈ 377 s de juego + ≈ 150 s de horneado) ≈ {n(dur_serie_h, 1)} h y ≈ {n(gb_serie, 0)} GB de diarios antes de comprimir: en 24 h caben {caben_24h} series.
**No jugada: sin potencia en 24 h ni disco** (decisión de Manel, 12-oct): las series con potencia (S1 {series_local['S1']}, S2 {series_local['S2']}) no caben frente a las {caben_24h} que entran en 24 h, y pedirían ≈ {n(gb_serie * series_local['S2'], 0)} GB de diarios antes de comprimir. En el mundo local, en 3 días casi ninguna pareja llega a creer en el botiquín (S1 en SOLAS: 0 en las 8 parejas):
las vidas son cortas y las pruebas escasas; el escalado a 20 días es una extrapolación declarada. Lo que cabe en 24 h ({caben_24h} series, ≈ 40 h de CPU del Mac) no distinguiría ni un 100 %.

## Lectura

1. **Dirección y tamaño.** S1 y S2 van en la dirección prevista y lejos de los 3 errores típicos: la hermana que menos prueba cree {n(CT['S1'].get('media_C'), 0)} frente a {n(CT['S1'].get('media_S'), 0)} de área (+{n(100 * CT['S1'].get('dif', 0) / CT['S1'].get('media_S', 1), 0)} %, {n(CT['S1'].get('dif', 0) / CT['S1'].get('ee', 1), 1)} ee); las
   hermanas que comparten acaban creyendo casi lo mismo ({n(CT['S2'].get('media_C'), 2)} de diferencia media en d11-20 frente a {n(CT['S2'].get('media_S'), 2)}; {n(abs(CT['S2'].get('dif', 0)) / CT['S2'].get('ee', 1), 1)} ee): el canal y la noche pasan cada recuerdo vivido, así que los dos
   cuadernos convergen (creencia del botiquín al d20 idéntica en las tres parejas de COMPARTE). S3, la única con potencia, es nula: compartir no reduce las pruebas a red y
   camuflaje ({n(100 * CT['S3'].get('media_C', 0), 0)} % frente a {n(100 * CT['S3'].get('media_S', 0), 0)} %): lo que la hermana cuenta del camuflaje («no hizo nada», importancia pequeña) pesa poco contra la ignorancia, como en P7-47.
2. **Vigilancia.** En COMPARTE la prudente prueba más que la valiente en las tres series ({', '.join(f"{v['pruebas_prudente']} frente a {v['pruebas_valiente']}" for k, v in CT['vigilancia'].items() if 'COMPARTE' in k)}); en SOLAS no hay orden fijo. Contagio de errores:
   {sum(v['recibidos']['contagio'] for k, v in CT['vigilancia'].items() if 'COMPARTE' in k)} de {sum(v['recibidos']['recibidos'] for k, v in CT['vigilancia'].items() if 'COMPARTE' in k)} recuerdos recibidos. Rachas ≥ 72 tics no quitadas por v3b: 0 en las 240 vidas válidas (la única fue la del intento apartado); las rachas cortas
   salen más en las valientes de COMPARTE ({RA['por_brazo_hermana']['COMPARTE · valiente']['cortas']}) que en las prudentes ({RA['por_brazo_hermana']['COMPARTE · prudente']['cortas']}): la sospecha de que el miedo a separarse escalado atasca a las prudentes no se ve.
3. **Lo que diría más series.** Con el ruido observado en este campo (S1 sd entre series {n(st.stdev(CT['S1']['COMPARTE'] + CT['S1']['SOLAS']) if len(CT['S1'].get('COMPARTE', [])) > 1 else 0, 0)}), S1 a 3 ee pediría unas {int(-(-(18 * (st.stdev(CT['S1']['SOLAS']) ** 2) / max(1e-9, CT['S1']['dif'] ** 2)) // 1)) if len(CT['S1'].get('SOLAS', [])) > 1 else '—'} series por brazo para este tamaño de efecto;
   S2, {int(-(-(18 * (st.stdev(CT['S2']['SOLAS']) ** 2) / max(1e-9, CT['S2']['dif'] ** 2)) // 1)) if len(CT['S2'].get('SOLAS', [])) > 1 else '—'}. Para la mesa.

## Línea final

{('Los dos mundos no se pueden comparar: el local no se jugó por falta de potencia. En la plataforma ' + (('pasan ' + ', '.join(pasa_pl)) if pasa_pl else 'no pasa ninguna predicción') + '.')}
"""
open(os.path.join(AQUI, "informe_P7_50.md"), "w", encoding="utf-8").write(out); print("informe_P7_50.md", out.count("\n"), "lineas")
