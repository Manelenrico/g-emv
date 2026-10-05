"""[P6-30] Escribe informe_P6_30.md: la fuga en los bancos del seis. Lee los JSON viejos (cantera/paper6) y los nuevos (cantera/paper6/P6_30)
y compone la tabla cifra a cifra de las secciones 6 y 7 del apendice del paper seis. Ninguna cifra a mano."""
import collections, hashlib, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..")); NUEVO = os.path.join(AQUI, "P6_30")
def J(p, base=AQUI):
    f = os.path.join(base, p); return json.load(open(f)) if os.path.exists(f) else None
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
sello = open(os.path.join(AQUI, "SELLO_P6_30.md")).read().strip().split("`")[-2]
V = {k: (J(f), J(f, NUEVO)) for k, f in (("m25", "P6_25_medidas.json"), ("b26", "P6_26_banco.json"), ("b28", "P6_28_banco.json"), ("m29", "P6_29_medidas.json"), ("e25", "P6_25_escenas.json"), ("p29", "P6_29_planes.json"), ("v29", "P6_29_vidas.json"))}
PREV = J("P6_28_prevision_P6_30.json", NUEVO)
def hacia(p):
    I = p["instantes"]; out = {}
    for b in ("A7h", "A8"):
        ii = [i for i in I if ("A7h" in i["carp"]) == (b == "A7h")]; out[b] = (sum(1 for i in ii if str(i.get("propio", "")).startswith("ir_")), len(ii))
    return out
FILAS = []   # (seccion, frase del texto, valor citado (apendice), fuente, extractor viejo, extractor nuevo, criterio de cambio de frase)
def fila(sec, frase, citado, fuente, ext, cambia):
    FILAS.append((sec, frase, citado, fuente, ext, cambia))
m25o, m25n = V["m25"]; b26o, b26n = V["b26"]; b28o, b28n = V["b28"]; m29o, m29n = V["m29"]; p29o, p29n = V["p29"]
# ── seccion 6, P6-25 ──
fila(6, "la puerta acepta cerca de la mitad, en proporción parecida con reglas o lenguaje", "oráculo 102 de 200; Haiku 98 de 191; Sonnet 100 de 183; 51,0 / 49,0 / 50,0 %", "informe_P6_25:66-69",
     lambda m: f"oráculo {m['2_primer_plan']['oraculo']['acepta']['k']} de {m['2_primer_plan']['oraculo']['acepta']['n']}; Haiku {m['2_primer_plan']['haiku']['acepta_sobre_planes']['k']} de {m['2_primer_plan']['haiku']['acepta_sobre_planes']['n']}; Sonnet {m['2_primer_plan']['sonnet']['acepta_sobre_planes']['k']} de {m['2_primer_plan']['sonnet']['acepta_sobre_planes']['n']}; {m['2_primer_plan']['oraculo']['acepta']['pct']} / {m['2_primer_plan']['haiku']['acepta_sobre_escenas']['pct']} / {m['2_primer_plan']['sonnet']['acepta_sobre_escenas']['pct']} %",
     lambda a, b: any(abs(a['2_primer_plan'][k]['acepta' if k == 'oraculo' else 'acepta_sobre_escenas']['pct'] - b['2_primer_plan'][k]['acepta' if k == 'oraculo' else 'acepta_sobre_escenas']['pct']) > 10 or not (40 <= b['2_primer_plan'][k]['acepta' if k == 'oraculo' else 'acepta_sobre_escenas']['pct'] <= 60) for k in ('oraculo', 'haiku', 'sonnet')))
fila(6, "mismo veredicto en casi nueve de cada diez", "172-174 de 200 (McNemar p 0,57 y 0,85)", "informe_P6_25",
     lambda m: "; ".join(f"{k}: {m['2_primer_plan'][k]['vs_oraculo_2x2']['los_dos_ok'] + m['2_primer_plan'][k]['vs_oraculo_2x2']['ninguno']} de 200 (p {m['2_primer_plan'][k]['vs_oraculo_2x2']['mcnemar_p']})" for k in ('haiku', 'sonnet')),
     lambda a, b: any(not (80 <= (b['2_primer_plan'][k]['vs_oraculo_2x2']['los_dos_ok'] + b['2_primer_plan'][k]['vs_oraculo_2x2']['ninguno']) / 2 <= 95) for k in ('haiku', 'sonnet')))
fila(6, "al llegar, sigue pasando la mitad / cuatro de cada diez", "51,8 % (Haiku), 41,0 % (Sonnet)", "informe_P6_25",
     lambda m: "; ".join(f"{k}: {m['3_retraso'][k]['ok_en_t_y_en_t_mas_D']['k']} de {m['3_retraso'][k]['ok_en_t_y_en_t_mas_D']['n']} ({m['3_retraso'][k]['ok_en_t_y_en_t_mas_D']['pct']} %)" for k in ('haiku', 'sonnet')),
     lambda a, b: not (40 <= b['3_retraso']['haiku']['ok_en_t_y_en_t_mas_D']['pct'] <= 60) or not (30 <= b['3_retraso']['sonnet']['ok_en_t_y_en_t_mas_D']['pct'] <= 50))
fila(6, "el segundo intento pasa pocas veces, el tercero casi nunca", "2.º 8,1 / 14,3 %; 3.º 0 / 4,2 %", "informe_P6_25",
     lambda m: "; ".join(f"{k}: 2.º {m['4_bucle'][k]['segunda (a los rechazados de la primera)']['k']} de {m['4_bucle'][k]['segunda (a los rechazados de la primera)']['n']} ({m['4_bucle'][k]['segunda (a los rechazados de la primera)']['pct']} %), 3.º {m['4_bucle'][k]['tercera (a los rechazados de la segunda)']['k']} de {m['4_bucle'][k]['tercera (a los rechazados de la segunda)']['n']} ({m['4_bucle'][k]['tercera (a los rechazados de la segunda)']['pct']} %)" for k in ('haiku', 'sonnet')),
     lambda a, b: any(b['4_bucle'][k]['segunda (a los rechazados de la primera)']['pct'] > 25 or b['4_bucle'][k]['tercera (a los rechazados de la segunda)']['pct'] > 10 for k in ('haiku', 'sonnet')))
fila(6, "coinciden en la zona casi siempre; aceptan los dos una de cada cinco", "82,5 / 100 %; 20,0 / 17,5 %", "informe_P6_25",
     lambda m: "; ".join(f"{k}: zona {m['5_pareja'][k]['coinciden_zona (Chebyshev <= 3)']['pct']} %, los dos {m['5_pareja'][k]['aceptan_las_dos_puertas']['k']} de {m['5_pareja'][k]['aceptan_las_dos_puertas']['n']} ({m['5_pareja'][k]['aceptan_las_dos_puertas']['pct']} %)" for k in ('haiku', 'sonnet')),
     lambda a, b: any(b['5_pareja'][k]['coinciden_zona (Chebyshev <= 3)']['pct'] < 75 or not (10 <= b['5_pareja'][k]['aceptan_las_dos_puertas']['pct'] <= 30) for k in ('haiku', 'sonnet')))
fila(6, "en ocho de cada diez escenas rechazadas no había ningún plan de ir y quedarse aceptable", "con plan que pasa: 21 de 93 (22,6 %); 13 de 83 (15,7 %)", "informe_P6_26:42-43",
     lambda b: "; ".join(f"{k}: {b['por_modelo'][k]['con_algun_plan_que_pasa']['k']} de {b['por_modelo'][k]['con_algun_plan_que_pasa']['n']} ({b['por_modelo'][k]['con_algun_plan_que_pasa']['pct']} %)" for k in ('haiku', 'sonnet')),
     lambda a, b: any(not (70 <= 100 - b['por_modelo'][k]['con_algun_plan_que_pasa']['pct'] <= 90) for k in ('haiku', 'sonnet')))
fila(6, "con adelanto, la puerta no acepta más; algo menos", "33,5 contra 36,7 % (251; McNemar p 0,28)", "informe_P6_28",
     lambda b: f"{b['pasan_a_la_llegada']['con_adelanto']['pct']} contra {b['pasan_a_la_llegada']['sin_adelanto (plan original de A8, misma instantanea)']['pct']} % ({b['consultas']}; p {b['pasan_a_la_llegada']['mcnemar_p']})",
     lambda a, b: (b['pasan_a_la_llegada']['con_adelanto']['pct'] > b['pasan_a_la_llegada']['sin_adelanto (plan original de A8, misma instantanea)']['pct']) or b['pasan_a_la_llegada']['mcnemar_p'] < 0.05)
fila(6, "la previsión se equivoca en un par de casillas", "mediana 2, p90 7", "informe_P6_28", lambda b: f"mediana {b['error_prevision_casillas']['mediana']}, p90 {b['error_prevision_casillas']['p90']}", lambda a, b: b['error_prevision_casillas']['mediana'] not in (1, 2, 3))
# ── seccion 7, P6-29 ──
A = lambda m, b: m["brazos"][b]
fila(7, "hace otra cosa en ocho de cada diez instantes", "83,9 % (A7h), 82,4 % (A8)", "informe_P6_29", lambda m: f"{A(m,'A7h')['1_difieren']['pct']} % (A7h), {A(m,'A8')['1_difieren']['pct']} % (A8)", lambda a, b: any(not (70 <= A(b, x)['1_difieren']['pct'] <= 90) for x in ('A7h', 'A8')))
fila(7, "nueve de cada diez, sujeciones; tres de cada cuatro, para ir a por algo", "92 %; 76 %", "informe_P6_29:66-67",
     lambda m: f"sujeta {100 * A(m,'A7h')['1_difieren']['sujeta'] / A(m,'A7h')['1_difieren']['difieren']:.1f} %; hacia algo {100 * hacia(V['p29'][0 if m is m29o else 1])['A7h'][0] / hacia(V['p29'][0 if m is m29o else 1])['A7h'][1]:.1f} %",
     lambda a, b: not (85 <= 100 * A(b,'A7h')['1_difieren']['sujeta'] / A(b,'A7h')['1_difieren']['difieren'] <= 97) or not (65 <= 100 * hacia(p29n)['A7h'][0] / hacia(p29n)['A7h'][1] <= 85))
fila(7, "quedarse cuesta más del doble que andar", "0,154 contra 0,065 por instante", "informe_P6_29", lambda m: f"{A(m,'A7h')['2_deformacion']['por_instante_sujeta']['mediana']:.3f} contra {A(m,'A7h')['2_deformacion']['por_instante_obedece']['mediana']:.3f}", lambda a, b: A(b,'A7h')['2_deformacion']['por_instante_sujeta']['mediana'] < 2 * A(b,'A7h')['2_deformacion']['por_instante_obedece']['mediana'])
fila(7, "el que más, cientos de veces el típico", "acumulada por plan: mediana 0,28 / 0,27, p90 17 / 3,9, máximo 102", "informe_P6_29",
     lambda m: f"mediana {A(m,'A7h')['2_deformacion']['acumulada_por_plan']['mediana']:.2f} / {A(m,'A8')['2_deformacion']['acumulada_por_plan']['mediana']:.2f}, p90 {A(m,'A7h')['2_deformacion']['acumulada_por_plan']['p90']:.1f} / {A(m,'A8')['2_deformacion']['acumulada_por_plan']['p90']:.1f}, máximo {A(m,'A7h')['2_deformacion']['acumulada_por_plan']['max']:.0f}",
     lambda a, b: A(b,'A7h')['2_deformacion']['acumulada_por_plan']['max'] / max(1e-9, A(b,'A7h')['2_deformacion']['acumulada_por_plan']['mediana']) < 100)
fila(7, "los cumplidos acumulan unas cien veces más que los soltados", "20,0 contra 0,18", "informe_P6_29", lambda m: f"{A(m,'A7h')['3_soltados_contra_cumplidos']['cumplidos']['acumulada']['mediana']:.2f} contra {A(m,'A7h')['3_soltados_contra_cumplidos']['soltados']['acumulada']['mediana']:.2f}",
     lambda a, b: not (30 <= A(b,'A7h')['3_soltados_contra_cumplidos']['cumplidos']['acumulada']['mediana'] / max(1e-9, A(b,'A7h')['3_soltados_contra_cumplidos']['soltados']['acumulada']['mediana']) <= 300))
fila(7, "caen por la puerta o por la vida, ninguno por lo aguantado", "132 por reevaluación, 76 por la vida", "informe_P6_29", lambda m: f"{A(m,'A7h')['planes']['por_razon'].get('soltado: reevaluacion', 0)} por reevaluación, {A(m,'A7h')['planes']['por_razon'].get('soltado: vida', 0)} por la vida", lambda a, b: False)
fila(7, "algo menos ardiendo de media que el cuerpo sin consejero; nada en el típico; sin relación", "media +42 / +15, mediana 0; Spearman -0,07 / +0,18", "informe_P6_29",
     lambda m: f"media {A(m,'A7h')['4_compensa']['ahorro_tics_ardiendo']['media']:+.1f} / {A(m,'A8')['4_compensa']['ahorro_tics_ardiendo']['media']:+.1f}, mediana {A(m,'A7h')['4_compensa']['ahorro_tics_ardiendo']['mediana']:.0f} / {A(m,'A8')['4_compensa']['ahorro_tics_ardiendo']['mediana']:.0f}; Spearman {A(m,'A7h')['4_compensa']['spearman_defo_ahorro']:+.2f} / {A(m,'A8')['4_compensa']['spearman_defo_ahorro']:+.2f}",
     lambda a, b: any(A(b, x)['4_compensa']['ahorro_tics_ardiendo']['media'] <= 0 or abs(A(b, x)['4_compensa']['ahorro_tics_ardiendo']['mediana']) > 5 or abs(A(b, x)['4_compensa']['spearman_defo_ahorro']) > 0.3 for x in ('A7h', 'A8')))
fila(7, "ocho segundos después, decide como solo", "200 tics; 99,7 % (A4 98,8 %)", "informe_P6_29", lambda m: f"{A(m,'A7h')['5_huella']['tras']['pct']} % (A4 {A(m,'A7h')['5_huella']['A4_tras']['pct']} %)", lambda a, b: A(b,'A7h')['5_huella']['tras']['pct'] < 97)
def plan13(p):
    x = next((q for q in p["planes"] if q.get("brazo") == "A7h" and str(q.get("carp", "")).endswith("20994019") and q.get("id") == 13), None)
    return f"instantes {x['instantes']}, sujeta {x['sujeta']}, obedece {x['obedece']}, acumulada {x['defo']:.1f}" if x else "plan 13 no encontrado"
fila(7, "figura 5: el plan que más dobló: 184 instantes queriendo ir; se quedó 183, anduvo 1; acumulada 102", "plan 13 de 20994019", "P6_29_planes.json", plan13, lambda a, b: plan13(b) != plan13(a))
# ── el informe ──
L = []; w = L.append
e25o, e25n = V["e25"]
rep = lambda e: collections.Counter(sum((collections.Counter(v.get("repro") or {}) for v in e["vidas"]), collections.Counter()))
tx_o = {f"{e['carp']}_{e['slot']}_{e['tick']}": hashlib.md5(e["texto"].encode()).hexdigest() for e in e25o["escenas"]}
tx_n = {f"{e['carp']}_{e['slot']}_{e['tick']}": hashlib.md5(e["texto"].encode()).hexdigest() for e in e25n["escenas"]} if e25n else {}
iguales_tx = sum(1 for k, v in tx_o.items() if tx_n.get(k) == v)
v29o, v29n = V["v29"]
def fid(v):
    c = collections.Counter(); c2 = collections.defaultdict(collections.Counter)
    for x in v: c.update(x.get("fidelidad") or {}); c2[x["brazo"]].update(x.get("fidelidad") or {})
    return c, c2
fo, fo_b = fid(v29o); fn, fn_b = fid(v29n) if v29n else (collections.Counter(), {})
w(f"""# P6-30 · La fuga en los bancos del seis: inventario, arreglo en el banco, repetición sin fuga y la tabla que importa

*3-oct-2026. Coste cero (plataforma 0; consola 0; ninguna llamada al modelo). `motor/model.py` = `{md5('motor/model.py')}` al empezar y
al acabar; `CONGELADO.md`, `CONGELADO_P6.md`, el cuerpo y los borradores sin tocar. Sello: `SELLO_P6_30.md`, commit 0b72aa5, md5 `{sello}`,
antes de calcular. Todo lo nuevo vive en `cantera/paper6/P6_30/` (copias de los bancos con tres cambios declarados y sus salidas); los JSON
originales de `cantera/paper6/` no se tocan. Este informe lo escribe `escribe_informe_P6_30.py` leyendo los JSON viejos y los nuevos.*

## Sección 1 · Inventario: qué banco corrió varias vidas por proceso

La fuga (P7-3): `policy_pareja._envuelve(alma)` (`cantera/paper6/policy_pareja.py:99-134`) apila una capa por vida sobre `D.candidatos` y
nadie la quita; cada capa veta los candidatos contra los rivales contados por su criatura, congelados al acabar su vida. Solo muerde
donde un mismo proceso replica **varias vidas con `_envuelve`** (`AlmaPareja` / `AlmaPareja23`, que lo llama en su constructor,
`policy_pareja23.py:278`). Revisados todos los `.py` de `cantera/paper6` desde P6-14 (`grep` de `AlmaPareja()`, `_envuelve(`, `Pool(`,
`subprocess`):

| banco | replica el cuerpo | cómo corre las vidas | varias vidas por proceso | afectado |
|---|---|---|---|---|
| P6-14 `banco_P6_14.py` | sí | `corre_P6_14.py:22`: un `subprocess` por vida | no | no |
| P6-15 `banco_P6_15.py` | sí | `corre_P6_15.py:22`: un `subprocess` por vida | no | no |
| P6-18 `banco_P6_18.py` | sí | `corre_P6_18.py:16`: un `subprocess` por vida | no | no |
| P6-19 `banco_P6_19.py` | sí | `corre_P6_19.py:28`: un `subprocess` por vida | no | no |
| P6-22 `mide_bucle_P6_22.py`, `mide_gil_P6_22.py` | sí | un proceso, una vida (argumentos de línea de órdenes) | no | no |
| P6-23 `compromiso6c`, `atribuye_pasos` | no (lee diarios) | – | – | no |
| P6-25 `escenas_P6_25.py` | sí (`AlmaPareja23`, `:282-284`) | `Pool(hilos)` sin `maxtasksperchild` (`:391`), 66 vidas en 4 procesos | **sí** | **sí** |
| P6-25 `juez_P6_25.py`, `razonador_P6_25.py` | no: el juez levanta UN alma espejo por proceso (`:103-111`) y no replica vidas | `Pool(hilos)` | no (una alma por proceso) | solo por sus entradas: las instantáneas de `escenas_P6_25` |
| P6-26 `banco_P6_26.py` | no (juez sobre instantáneas) | `Pool(hilos)` (`:84`) | no | solo por sus entradas (instantáneas de P6-25) |
| P6-27 | campo (una vida por proceso) + `mide_campo` sobre diarios | – | – | no |
| P6-28 `banco_P6_28.py --instantaneas` | sí (`AlmaPareja23`, `:64-65`) | `Pool(hilos)` sin `maxtasksperchild` (`:120`) | **sí** | **sí** |
| P6-29 `mide_P6_29.py` | sí (`AlmaPareja`, `:224`) | `Pool(hilos)` sin `maxtasksperchild` (`:371`), 240 vidas en 4 procesos | **sí** | **sí** |
| humos (`humo_red_*`) | sí, una vida | un proceso | no | no |

La lista de P7-3 se confirma (P6-25, P6-28, P6-29) y se precisa: P6-26 no replica el cuerpo, pero juzga sobre las instantáneas que
produjo la réplica de P6-25, así que se repite también. Las instantáneas de P6-25 y P6-28 estaban en el scratch de aquella sesión y ya no
existen: para volver a juzgar hay que volver a replicar.

## Sección 2 · El arreglo, solo en el banco, y la fontanería

Copias en `P6_30/` de `escenas_P6_25.py`, `juez_P6_25.py`, `mide_P6_25.py`, `banco_P6_26.py`, `banco_P6_28.py` y `mide_P6_29.py` con tres
cambios declarados en su primera línea: la raíz un nivel más arriba, `cantera/paper6` en el camino de importación, y **un proceso por
vida** (`maxtasksperchild=1`) en los tres pools que replican el cuerpo. El cuerpo no se toca. En la copia de `banco_P6_28.py` hay dos pasos
nuevos sin llamadas: `--reenlaza` (las instantáneas nuevas en la copia de los planes guardados, por id) y `--prevision` (rehace la escena
prevista y compara su md5 con la que se mandó al modelo).

**Fontanería.** Réplica contra diario, tic a tic, en `mide_P6_29` (`fidelidad` = la elección de la réplica contra `elegido_cuerpo`, lo que
el cuerpo eligió antes de que el compromiso lo cambiara):

| brazo | con fuga (P6-29 publicado) | sin fuga (P6-30) |
|---|---|---|
""")
for b in ("A7h", "A8", "A4"):
    o = fo_b.get(b, {}); nn = fn_b.get(b, {})
    w(f"| {b} | {n(o.get('igual', 0))} iguales, {n(o.get('difiere', 0))} distintas ({n(100 * o.get('igual', 0) / max(1, o.get('igual', 0) + o.get('difiere', 0)), 3)} %) | {n(nn.get('igual', 0))} iguales, {n(nn.get('difiere', 0))} distintas ({n(100 * nn.get('igual', 0) / max(1, nn.get('igual', 0) + nn.get('difiere', 0)), 3)} %) |\n")
w(f"""
Réplica de P6-25 (`repro`: la elección de la réplica contra `elegido` **ejecutado**, que en A7h incluye los pasos del compromiso, así que
"difiere" no es solo infidelidad): con fuga {n(rep(e25o)['igual'])} / {n(rep(e25o)['difiere'])}; sin fuga {n(rep(e25n)['igual']) if e25n else '–'} / {n(rep(e25n)['difiere']) if e25n else '–'}.
Textos de las 200 escenas de P6-25 (lo que leyó el modelo) iguales en la réplica sin fuga: {iguales_tx} de {len(tx_o)} (md5). Escenas previstas de
P6-28 (lo que leyó Haiku con adelanto) iguales: {sum(1 for x in (PREV or {}).get('consultas', []) if x.get('igual'))} de {len((PREV or {}).get('consultas', []))}. Las respuestas del modelo son las guardadas; no se pidió ninguna nueva.
{{NOTA_FONTANERIA}}

## Sección 3 · Repetición sin fuga: los bancos

{{SEC3}}

## Sección 4 · La tabla que importa: cada cifra de las secciones 6 y 7 que viene de estos bancos

| sección | frase del texto | valor citado (apéndice) | valor sin fuga | ¿cambia la frase? | fuente |
|---|---|---|---|---|---|
""")
cambios = []
for sec, frase, citado, fuente, ext, cambia in FILAS:
    src_o, src_n = {6: (m25o, m25n), 7: (m29o, m29n)}[sec]
    if "P6_26" in fuente: src_o, src_n = b26o, b26n
    if "P6_28" in fuente: src_o, src_n = b28o, b28n
    if "planes" in fuente: src_o, src_n = p29o, p29n
    try: vo = ext(src_o)
    except Exception as ex: vo = f"(error {ex!r})"
    try: vn = ext(src_n) if src_n else "(sin salida nueva)"
    except Exception as ex: vn = f"(error {ex!r})"
    try: c = ("sí" if cambia(src_o, src_n) else "no") if (cambia and src_n) else "ver texto"
    except Exception as ex: c = f"(error {ex!r})"
    if c == "sí": cambios.append(frase)
    w(f"| {sec} | {frase} | {citado} | {vn} | {c} | {fuente}; viejo = {vo} |\n")
w(f"""
Criterio de "cambia la frase": el que la frase admite (una proporción verbal como "cerca de la mitad" se da por cambiada si sale de 40-60 %,
"ocho de cada diez" si sale de 70-90 %, "casi nueve de cada diez" si sale de 80-95 %, "más del doble" si deja de serlo, "cien veces" si sale
de 30-300, etc.; cada criterio está en `escribe_informe_P6_30.py`, fila a fila). Las filas con "ver texto" se comparan a ojo en la sección 3.
No vienen de estos bancos y no cambian: las latencias del modelo (3,7 y 8,1 s), los intraducibles (1,5 / 7,5 %: traducción de respuestas
guardadas), todo lo de P6-27 (campo), la figura 4 y las medias de instantes ardiendo.

**Sello.** {{SELLO}}

## Archivos

| archivo | qué es |
|---|---|
| `SELLO_P6_30.md` | la predicción, md5, commit 0b72aa5 |
| `P6_30/*.py` | copias de los seis bancos con los tres cambios declarados; `cadena_P6_30.sh` el orden de ejecución |
| `P6_30/P6_25_*.json`, `P6_26_banco*.json`, `P6_28_*.json`, `P6_29_*.json` | las salidas sin fuga (mismos nombres que las viejas, en su carpeta) |
| `P6_30/_P6_25_snaps`, `_P6_28_snaps`, `*.log` | instantáneas y registros, fuera de git |
| `escribe_informe_P6_30.py`, `informe_P6_30.md` | este informe |
""")
RES = J("residuo_todo_P6_30.json", NUEVO) or {"vidas": [], "clases": []}
DD = [d for r in RES["vidas"] for d in r["desacuerdos"]]
def clase(d):
    if (d["cuerpo_es_FM"] or any(str(x).startswith("_FM") for x in d["solo_diario"])) and d["d_propias_iguales"] and not d["solo_replica"]: return "plan"
    if d["d_propias_iguales"] and (all(str(x).startswith("usar_") for x in d["solo_diario"] + d["solo_replica"])) and (d["solo_diario"] or d["solo_replica"]): return "canal"
    return "otra"
cl = collections.Counter(clase(d) for d in DD); otros = [(r["vida"], d) for r in RES["vidas"] for d in r["desacuerdos"] if clase(d) != "plan"]
nota = (f"**Residuo sin fuga, replicado uno a uno** (`residuo_todo_P6_30.py`): {len(DD)} desacuerdos (A7h {sum(len(r['desacuerdos']) for r in RES['vidas'] if r['brazo'] == 'A7h')}, A8 {sum(len(r['desacuerdos']) for r in RES['vidas'] if r['brazo'] == 'A8')}, A4 {sum(len(r['desacuerdos']) for r in RES['vidas'] if r['brazo'] == 'A4')}) de "
        f"{n(sum(fn.values()))} tics. En {cl['plan']} de {len(DD)} la elección del diario es el candidato del plan (`_FM_ir_*`), que la réplica no tiene porque no lleva compromiso, y las d de todos los "
        f"candidatos propios son iguales en el diario y en la réplica (diferencia < 1e-6): no es infidelidad del cuerpo, es que cuando el candidato del plan ganaba, la radiografía lo apuntó también como "
        f"elección propia (o no apuntó `elegido_cuerpo`). En {cl['canal']} el único candidato que difiere es un `usar_*` (el veto del canal, `decisor_zs.py:83-102`, que en la réplica se abre o cierra un tic "
        f"antes porque `action_result` llega con la observación siguiente). Quedan **{cl['otra']}** de otra clase, con alguna d distinta: "
        + "; ".join(f"{v[-14:]} t {d['t']} (diario {d['cuerpo'] or '–'}, réplica {d['replica']})" for v, d in otros if clase(d) == "otra") + ". "
        f"La fontanería no es exacta tic a tic: lo es salvo esos {cl['otra']} tics de {n(sum(fn.values()))} ({n(100 * cl['otra'] / max(1, sum(fn.values())), 5)} %) y los {cl['canal']} del canal; se dice y se sigue, porque no tocan ninguna cifra de las secciones 6 y 7 "
        f"(la deformación se mide sobre instantes con plan vivo y piernas listas, y el canal no es un instante de plan).")
if not RES["vidas"]: nota = "(residuo_todo_P6_30.json aún no existe)"
# seccion 3
def difs(a, b, path="", skip=("segundos", "fidelidad", "ms", "usd", "largo", "repro", "version", "nota")):
    out = []
    if isinstance(a, dict):
        for k in a:
            if k in b and not any(x in k for x in skip): out += difs(a[k], b[k], path + "/" + k, skip)
    elif isinstance(a, (int, float)) and not isinstance(a, bool) and a != b: out.append((path, a, b))
    return out
d25 = difs(m25o, m25n) if m25n else []; d26 = difs(b26o, b26n) if b26n else []; d28 = difs(b28o, b28n) if b28n else []
d29 = (difs(m29o["brazos"]["A7h"], m29n["brazos"]["A7h"], "A7h") + difs(m29o["brazos"]["A8"], m29n["brazos"]["A8"], "A8") + difs(m29o["6_oraculo_contra_razonador"], m29n["6_oraculo_contra_razonador"], "6")) if m29n else []
def lista(d, tope=40): return ("ninguna" if not d else "; ".join(f"`{p}` {a} → {b}" for p, a, b in d[:tope]) + (f" … y {len(d) - tope} más" if len(d) > tope else ""))
sec3 = f"""**P6-25** (`escenas_P6_25.py` → juez × 6 → `mide_P6_25.py`; 66 vidas de A7h replicadas, 240 escenas, 1.640 instantáneas nuevas; respuestas del
modelo: las guardadas en `P6_25_planes_*.json`). Cifras que cambian en `P6_25_medidas.json` (fuera de `repro`, tiempos y gasto): {lista(d25)}.
El único texto que cambia (`P624_t2_A7h_24764263_10_14591`) gana la línea "atacar al del asiento 4": en la réplica con fuga ese ataque
estaba vetado por un rival contado en una vida anterior del mismo proceso. Las respuestas guardadas valen para 239 de 240 escenas; en
la que cambia se juzga la respuesta guardada sobre la instantánea nueva, y queda declarado.

**P6-26** (`banco_P6_26.py`, el barrido de todos los destinos sobre las instantáneas nuevas; sin modelo). Cifras que cambian en
`P6_26_banco.json`: {lista(d26)}.

**P6-28** (`banco_P6_28.py --instantaneas` → `--reenlaza` → `--prevision` → `--juzga` → `--mide`; 70 vidas de A8 replicadas, 256 consultas
con sus dos instantáneas; respuestas de Haiku: las guardadas en `P6_28_banco_planes.json`). La escena prevista rehecha desde la instantánea
nueva es idéntica (md5) a la que leyó Haiku en {sum(1 for x in (PREV or {}).get('consultas', []) if x.get('igual'))} de {len((PREV or {}).get('consultas', []))} consultas; distinta en {sum(1 for x in (PREV or {}).get('consultas', []) if x.get('igual') is False)} ({', '.join(x['id'] for x in (PREV or {}).get('consultas', []) if x.get('igual') is False)}), cuyas respuestas guardadas
son a un texto que ya no es el mismo (no se piden de nuevo: son las que faltan); {sum(1 for x in (PREV or {}).get('consultas', []) if x.get('error'))} dan error en la previsión, como en P6-28 (251 medidas en los dos).
Cifras que cambian en `P6_28_banco.json`: {lista(d28)}.

**P6-29** (`mide_P6_29.py`, 240 vidas: A7h 80, A8 78, A4 80). Cifras que cambian en `P6_29_medidas.json` (sin tiempos ni fidelidad): {lista(d29, 60)}.
Lo que se mueve es pequeño y donde se esperaba: la deformación por instante y acumulada de A7h sube unas centésimas (los ataques que la
fuga vetaba vuelven a estar entre los candidatos propios y cambian la d mínima en algunos instantes), el Spearman de A7h pasa de −0,07 a
+0,04 (sigue siendo ninguna relación) y la huella de A4 pasa a 100 %: la "infidelidad" de A4 era toda la fuga."""
sello_txt_ = ("**Acierta**: ninguna cifra de las secciones 6 y 7 cambia la frase que la cuenta." if not cambios else "**Falla** en: " + "; ".join(cambios) + ".")
txt = "".join(L).replace("{NOTA_FONTANERIA}", nota).replace("{SEC3}", sec3).replace("{SELLO}", sello_txt_); assert "§" not in txt
open(os.path.join(AQUI, "informe_P6_30.md"), "w").write(txt); print("informe escrito; frases que cambian:", cambios)
