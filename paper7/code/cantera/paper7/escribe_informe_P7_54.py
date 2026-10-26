"""[P7-54] Escribe informe_P7_54.md desde P7_54_razon.json (la repeticion de P7-52 con diario limpio y menu), P7_52_juicios.json (para comparar), P7_54_local.json (la prueba local
en lazo cerrado) y razon_P7_54.py (el prompt). Ninguna cifra a mano.  python3 escribe_informe_P7_54.py"""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
R = J("P7_54_razon.json"); JU52 = J("P7_52_juicios.json"); L = J("P7_54_local.json")
import razon_P7_54 as RZ, diario_razon_P7_54 as D54
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
inv = [dict(p, vida=f"s{r['serie']} d{r['dia']} {r['brazo']} a{r['slot']}") for r in R for p in r["invitaciones"]]
tin = sum(r["tokens_entrada"] for r in R); tout = sum(r["tokens_salida"] for r in R); usd = sum(r["usd_supuesto"] for r in R)
RAZ = L.get("razon", []); tinL = sum(r["tokens_entrada"] for r in RAZ); toutL = sum(r["tokens_salida"] for r in RAZ); usdL = sum(r["usd_supuesto"] for r in RAZ)
art52 = collections.Counter(x["promesa"] for x in JU52)
sosp = [p for p in inv if (p["vinculo"] != 0 and p["accion"] not in ("ACERCARSE_HERMANA", "DAR_BOTIQUIN_HERMANA")) or (p["recursos"] > 0 and p["accion"] in ("USAR_BOTIQUIN", "USAR_RACION", "PONERSE_CAMUFLAJE", "EMPUNAR_RED", "QUEDARSE_QUIETA")) or (p["cuerpo"] > 0 and p["accion"] in ("COGER_RED", "COGER_CAMUFLAJE", "EMPUNAR_RED", "PONERSE_CAMUFLAJE"))]
ca = collections.Counter(p["accion"] for p in inv); ct = collections.Counter(p["tipo"] for p in inv)
TA = ["| criatura-día | líneas · válidas (menú y formato) | acciones elegidas | tokens entrada + salida |", "|---|---:|---|---:|"]
for r in R:
    acc = ", ".join(p["accion"] for p in r["invitaciones"]); TA.append(f"| s{r['serie']} d{r['dia']} {r['brazo']} a{r['slot']} | {len(r['lineas'])} · {len(r['invitaciones'])} | {acc} | {n(r['tokens_entrada'], 0)} + {n(r['tokens_salida'], 0)} |")
TI = ["| criatura-día | invitación (tal cual, campos del menú y promesa) |", "|---|---|"]
for p in inv: TI.append(f"| {p['vida']} | {p['tipo']} · **{p['accion']}** · anillo {p['anillo']} · {p['calma']} · {p['movimiento']} · hermana {p['hermana']} · cuerpo {n(p['cuerpo'], 1)}, recursos {n(p['recursos'], 2)}, vínculo {n(p['vinculo'], 2)} · confianza {p['confianza']} · porque: {p['porque'][:220]} |")
# local
dias = sorted(k for k in L if k.startswith("d")); CON = ("10", "11", "12", "13")
TL = ["| día | asiento (con razón) | invitaciones cargadas | activas alguna vez | aceptadas (por acción; total; % de los tics con alguna invitación activa) | evaluadas (acierto medio por dimensión) | confianza al cerrar (c · r · v) | pruebas por vida | tics |", "|---|---|---:|---:|---|---|---|---:|---:|"]
for d in dias:
    for sl in CON:
        v = L[d]["vidas"].get(sl)
        if not v: continue
        p = v["P7_54"]; ar = p.get("arranque") or {}; ci = p.get("cierre") or {}; cf = ci.get("confianza") or {}
        ca_ = collections.Counter(x["accion"] for x in p["aceptadas"]); acept = "; ".join(f"{k} ×{v}" for k, v in ca_.items()) or "—"
        ev_ = p["evaluadas"]; ac_ = {dim: (st.mean(e["acierto"][dim] for e in ev_) if ev_ else None) for dim in ("cuerpo", "recursos", "vinculo")}; ev = (f"{len(ev_)} (acierto medio c {n(ac_['cuerpo'], 2)} · r {n(ac_['recursos'], 2)} · v {n(ac_['vinculo'], 2)})" if ev_ else "—")
        nn = (ci.get("n") or {}); ratio = (len(p["aceptadas"]) / nn["activas_tics"]) if nn.get("activas_tics") else None
        TL.append(f"| {d} | {sl} ({'valiente' if int(sl) % 2 == 0 else 'prudente'}) | {ar.get('invitaciones', 0)} | {p['activas']} ({n(nn.get('activas_tics'), 0)} tics) | {acept} ({len(p['aceptadas'])}; {n(100 * ratio, 1) if ratio is not None else '—'} % de los tics activos) | {ev} | {n(cf.get('cuerpo'), 2)} · {n(cf.get('recursos'), 2)} · {n(cf.get('vinculo'), 2)} | {v['huellas']} | {v['tics']} |")
acept = sum(len(L[d]["vidas"][sl]["P7_54"]["aceptadas"]) for d in dias for sl in CON if sl in L[d]["vidas"]); evalu = sum(len(L[d]["vidas"][sl]["P7_54"]["evaluadas"]) for d in dias for sl in CON if sl in L[d]["vidas"]); carg = sum((L[d]["vidas"][sl]["P7_54"].get("arranque") or {}).get("invitaciones", 0) for d in dias for sl in CON if sl in L[d]["vidas"]); activ = sum(L[d]["vidas"][sl]["P7_54"]["activas"] for d in dias for sl in CON if sl in L[d]["vidas"])
ctrl = [L[d]["vidas"][sl]["huellas"] for d in dias for sl in L[d]["vidas"] if sl not in CON]; conr = [L[d]["vidas"][sl]["huellas"] for d in dias for sl in CON if sl in L[d]["vidas"]]
lat = max((L[d]["resumen"]["ms_p95_max"] or 0) for d in dias)
por_llamada_in = tin / len(R); por_llamada_out = tout / len(R); usd_llamada = por_llamada_in / 1e6 * RZ.PRECIO["entrada_por_Mtok"] + por_llamada_out / 1e6 * RZ.PRECIO["salida_por_Mtok"]
campo1 = 3 * 20 * 2 * usd_llamada; campo2 = 2 * campo1
out = f"""# P7-54 · Capítulo 5, paso 2: diario limpio, menú de lo que el cuerpo sabe hacer, y la invitación que entra en el cuerpo

*13-oct-2026. Sin plataforma (0 créditos). Bolsa 2 (consola, `claude-sonnet-5-5`): repetición de P7-52 con diario limpio y menú, 8 llamadas = {n(tin, 0)} + {n(tout, 0)} tokens ({n(usd, 4)} $ supuestos a 3/15 $ por millón);
prueba local, {len(RAZ)} llamadas = {n(tinL, 0)} + {n(toutL, 0)} tokens ({n(usdL, 4)} $); **total {n(usd + usdL, 4)} $ supuestos (tope 3 $)**; el dólar exacto en la consola. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`; el cuerpo congelado y el
campo P7-50 sin tocar. Piezas nuevas: `diario_razon_P7_54.py` (diario limpio y menú), `razon_P7_54.py` (prompt v2 y parser), `invita_P7_54.py` = `{md5('invita_P7_54.py')}` (la entrada en el cuerpo),
`campo_P7_54.py`, `policy_pareja_P7_54.py`, `Dockerfile.pareja_P7_54`, `local54_P7_54.py` (la cadena local con la razón entre días); `escribe_informe_P7_54.py` (este informe; ninguna cifra a mano).*

## Sección 1 · El diario limpio y el menú

**Diario limpio**: en cada prueba y en el resumen, dos etiquetas: **EFECTO DEL OBJETO** = lo medido como B1, solo lo que la cosa hizo en el cuerpo (vida, descontado lo esperado sin ella) y la
unidad gastada si es consumible; **CONTEXTO (no es la cosa)** = riqueza por coger o llevar, cambio de distancia a la hermana (lo que antes se llamaba «vínculo» de la prueba), golpes de otros en
la ventana, y si la ventana se cortó. Las creencias se dan solo en el cuerpo. **Menú cerrado** (acción × situación), que la razón debe usar:

> {D54.MENU_TEXTO}

Prompt v2 entero:

```
{RZ.SISTEMA}
```

## Sección 2 · P7-52 repetido con el diario limpio y el menú (mismos 8 criatura-días)

{chr(10).join(TA)}

{len(inv)} invitaciones válidas de {sum(len(r['lineas']) for r in R)} líneas (una fuera por formato); tipos: {', '.join(f'{k} {v}' for k, v in ct.items())}; acciones: {', '.join(f'{k} {v}' for k, v in ca.most_common())}.
**¿Desaparecen las promesas de artefacto?** En P7-52 (sin etiquetas ni menú) había {art52['artefacto']} promesas de artefacto y {art52['sin base']} sin base de 47. Ahora, con el mismo criterio (vínculo prometido en acciones
que no son de la hermana; recursos prometidos por usar, ponerse, empuñar o quedarse quieta; cuerpo prometido por red o camuflaje): **{len(sosp)} dudosas de {len(inv)}**:
{chr(10).join(f'- {p["vida"]} · {p["accion"]}: cuerpo {n(p["cuerpo"], 1)}, recursos {n(p["recursos"], 2)}, vínculo {n(p["vinculo"], 2)} («{p["porque"][:120]}»)' for p in sosp) or '- ninguna'}
El camuflaje y la red ya no prometen cuerpo ni recursos ({', '.join(f"{p['accion']} c {n(p['cuerpo'], 0)} r {n(p['recursos'], 0)} v {n(p['vinculo'], 2)}" for p in inv if p['accion'] in ('PONERSE_CAMUFLAJE', 'EMPUNAR_RED', 'COGER_RED', 'COGER_CAMUFLAJE'))}); el vínculo solo lo prometen acercarse o dar a la hermana (y dos casos de ± 0,05 y uno de quedarse quieta a su lado).
Las promesas de cuerpo del botiquín van de {n(min(p['cuerpo'] for p in inv if p['accion'] == 'USAR_BOTIQUIN'), 0)} a {n(max(p['cuerpo'] for p in inv if p['accion'] == 'USAR_BOTIQUIN'), 0)} (el real es 50 capado por 100); la ración {n(min(p['cuerpo'] for p in inv if p['accion'] == 'USAR_RACION'), 0)}-{n(max(p['cuerpo'] for p in inv if p['accion'] == 'USAR_RACION'), 0)} (real 15).

{chr(10).join(TI)}

## Sección 3 · La invitación entra en el cuerpo (`invita_P7_54`)

Al arrancar, el cuerpo lee las invitaciones de anoche y su confianza en la razón por dimensión (empieza en 0,5; viaja en el cuaderno). En cada tic, una invitación está activa si su
situación se cumple (anillo, calma = `peligro_de` de P7-33, quieta = sin cambiar de casilla en 24 tics, hermana a ≤ 4). El candidato del cuerpo que corresponde a su acción recibe, solo
en SU foto imaginada, el efecto prometido × confianza como filas apetitivas INVITACION-CUERPO / RECURSOS / VINCULO (aversivas si la promesa es dolor, perder o alejar), con M = |promesa| ×
confianza / escala (25 de vida, 1 de W, 1 de B), tope 1: el cuerpo decide si y cuándo, con su misma regla de siempre (la foto con menos malestar). Lo que cree el cuerpo no cambia por la
invitación (el cuaderno solo se escribe con lo vivido). Tras aceptar (el elegido es su candidato), se compara prometido y vivido por dimensión (huella de la cosa; si no hay cosa,
ventana de 240 tics: Δ vida, Δ W, Δ B); acierto = signo igual y |vivido| ≥ |prometido| / 2 (o las dos < 1); confianza_dim ← 0,7 × confianza + 0,3 × acierto.

## Sección 4 · Prueba local en lazo cerrado ({len(dias)} días encadenados, 16 asientos; la razón para los asientos 10-13, los demás de control)

{chr(10).join(TL)}

- **Llegan**: {carg} invitaciones cargadas en {sum(1 for d in dias for sl in CON if sl in L[d]['vidas'] and (L[d]['vidas'][sl]['P7_54'].get('arranque') or {}).get('invitaciones'))} vidas (el día 1 nadie tiene razón aún); activas alguna vez {activ}.
- **El cuerpo las prueba a veces y no siempre**: {acept} aceptaciones en esas vidas (cada aceptación abre una ventana de evaluación; la misma invitación se puede volver a aceptar después), el {n(100 * acept / max(1, sum((L[d]['vidas'][sl]['P7_54'].get('cierre') or {}).get('n', {}).get('activas_tics', 0) for d in dias for sl in CON if sl in L[d]['vidas'])), 2)} % de los tics con alguna invitación activa; evaluadas {evalu}. Pruebas por vida: con razón {n(st.mean(conr), 2) if conr else '—'}, control {n(st.mean(ctrl), 2) if ctrl else '—'}.
- **La confianza se mueve**: véase la columna «confianza al cerrar» (empieza en 0,50 · 0,50 · 0,50 y viaja en el cuaderno).
- Latencia local: p95 máximo {n(lat, 1)} ms (16 políticas en el Mac, como en P7-48).

## Sección 5 · Coste de consola de un campo de 3 series

Por criatura-día (medido en las 8 llamadas): {n(por_llamada_in, 0)} tokens de entrada + {n(por_llamada_out, 0)} de salida = {n(usd_llamada, 4)} $ supuestos. Un campo de 3 series × 20 días con la razón en las dos hermanas de un brazo
= 120 llamadas ≈ **{n(campo1, 2)} $**; con la razón en dos brazos (p. ej. razón que ayuda / razón que miente) ≈ {n(campo2, 2)} $. Más lo que se pierda en reintentos. Tarifa supuesta 3/15 $ por millón (la consola da el exacto).

## Lectura

1. El diario limpio y el menú hacen lo que la mesa pedía: las promesas de artefacto desaparecen (de {art52['artefacto']} + {art52['sin base']} a {len(sosp)} dudosas) y todas las invitaciones son acciones que este cuerpo sabe hacer.
2. La entrada en el cuerpo funciona en lazo cerrado: las invitaciones llegan, se activan por situación, el cuerpo acepta algunas y la confianza por dimensión se mueve con lo vivido.
   Límite declarado: el vínculo se evalúa por Δ B en 240 tics, y B está saturado en 1 (P7-53): esa dimensión no premia a la razón aunque acierte; para la mesa.
3. Lo que falta para un campo con sello: decidir el brazo de comparación (razón que ayuda frente a sin razón, o razón que miente), la medida (p. ej. pruebas útiles y creencia del
   botiquín con y sin razón) y el ruido; y limpiar el canal de la noche (P7-51) si la razón ha de hablar por el mundo.
"""
open(os.path.join(AQUI, "informe_P7_54.md"), "w", encoding="utf-8").write(out); print("informe_P7_54.md", out.count("\n"), "lineas")
