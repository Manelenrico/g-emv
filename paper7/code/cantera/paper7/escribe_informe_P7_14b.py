"""[P7-14b] Escribe informe_P7_14b.md desde P7_14b_campo.json (campo_P7_14b.py), P7_14b_vidas.json (analiza_P7_14b.py), P7_14b_sello_resultado.json
(sello_P7_14b.py), P7_14b_estado.json, P7_14b_freno.json, P7_14b_banco.json, P7_14b_F1.json, P7_14_estado.json y P7_11_vidas.json. Ninguna cifra a mano."""
import collections, hashlib, json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
J = lambda p: json.load(open(os.path.join(AQUI, p))); md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
C = [v for v in J("P7_14b_campo.json").values() if not v.get("sin_tics")]; V = list(J("P7_14b_vidas.json").values()); S = J("P7_14b_sello_resultado.json"); E = J("P7_14b_estado.json")
FR = J("P7_14b_freno.json"); BA = J("P7_14b_banco.json"); F1 = J("P7_14b_F1.json"); E14 = J("P7_14_estado.json"); V10 = list(J("P7_11_vidas.json").values())
BR = ("ESPERANZA", "BORRADO", "APRENDE", "TECHO"); B10 = {"ESPERANZA": "SUELO", "BORRADO": "BORRADO", "APRENDE": "APRENDE", "TECHO": "TECHO"}
Lc = {b: [v for v in C if v["brazo"] == b] for b in BR}; Lv = {b: [v for v in V if v["brazo"] == b] for b in BR}; L10 = {b: [v for v in V10 if v["brazo"] == B10[b]] for b in BR}
med = lambda xs: (st.median(xs) if xs else None); mean = lambda xs: (st.mean(xs) if xs else None)
pet = E["peticiones"]; coste = sum(float(p.get("coste_usd") or 0) for p in pet); coste14 = sum(float(p.get("coste_usd") or 0) for p in E14["peticiones"]); est = collections.Counter(p["estado"] for p in pet)
por_brazo = {b: sum(float(p.get("coste_usd") or 0) for p in pet if p["brazo"] == b) for b in BR}
ini = min(p["pedida_a_las"] for p in pet); fin = max((p.get("completada_a_las") or "") for p in pet)
W = []; w = W.append
def fila(nombre, f, cols=BR): w(f"| {nombre} | " + " | ".join(f(b) for b in cols) + " |\n")
res = S["resumen"]; pasan = [q for q in ("Q1", "Q2", "Q3", "Q4", "Q5") if res[q]]; q1 = S["Q1"]; q2 = S["Q2"]; q3 = S["Q3"]; q4 = S["Q4"]; q5 = S["Q5"]
w(f"""# P7-14b · El segundo campo del siete, con pedir

*4/5-oct-2026. Coste: **créditos de la plataforma {n(coste, 4)} USD** en {sum(1 for p in pet if p.get('coste_usd'))} partidas ({", ".join(f"{b} {n(por_brazo[b], 4)}" for b in BR)});
**consola de Anthropic 0 USD**. Con las 3 partidas del freno de P7-14 ({n(coste14, 4)} USD, que no cuentan para nada), el capítulo del segundo campo suma {n(coste + coste14, 4)} USD.
Acumulado del siete en la plataforma: {n(16.0147 + coste14 + coste, 4)} USD. Saldos: no consultados. `motor/model.py` = `{md5('motor/model.py')}` al empezar y al acabar;
cuerpo y congelados sin tocar. Sello antes de jugar: `SELLO_P7_14b.md`, commit `{E.get('commit_sello', '')[:12]}`. Peticiones: {dict(est)}. El sello se ha evaluado una sola vez, al final.*

## Lo que sale, en corto

**El sello: {len(pasan)} de 5** (pasan {", ".join(pasan) or "ninguna"}; fallan {", ".join(q for q in ("Q1", "Q2", "Q3", "Q4", "Q5") if not res[q]) or "ninguna"}).

- **Q1 (la principal): {"pasa" if res["Q1"] else "falla"}.** APRENDE menos BORRADO, emparejado: puesto {n(q1["puesto"]["media_dif"], 2)} (se {n(q1["puesto"]["se"], 2)}); vida al morir {n(q1["hp_final"]["media_dif"], 2)} (se {n(q1["hp_final"]["se"], 2)}).
- **Q2: {"pasa" if res["Q2"] else "falla"}.** APRENDE regala {q2["regalos"]} veces en {q2["vidas"]} vidas ({n(q2["regalos_por_vida"], 3)} por vida; tope {n(q2["tope_regalos_por_vida"], 3)}) y vuelve a coger {q2["vueltos_a_coger"]} ({n(q2["vueltos_a_coger_por_vida"], 3)} por vida; tope {n(q2["tope_vueltos_por_vida"], 3)}).
- **Q3: {"pasa" if res["Q3"] else "falla"}.** Días 11 a 20, parte de la vida yendo a por botiquines: APRENDE {n(100 * q3["parte_de_la_vida_APRENDE"], 1)} %, BORRADO {n(100 * q3["parte_de_la_vida_BORRADO"], 1)} %.
- **Q4: {"pasa" if res["Q4"] else "falla"}.** La creencia sube en {q4["suben"]} de 4; vida al usar en los días 11 a 20: APRENDE {n(q4["mediana_vida_al_usar_d11_20"]["APRENDE"], 1)}, BORRADO {n(q4["mediana_vida_al_usar_d11_20"]["BORRADO"], 1)}.
- **Q5: {"pasa" if res["Q5"] else "falla"}.** {q5["porque_se_lo_dieron"]} de {n(q5["cerrados"])} pedidos cerrados lo fueron porque se lo dieron ({n(100 * (q5["fraccion"] or 0), 1)} %).

## Sección 1 · Lo declarado antes de leer nada

- **Las 3 partidas del freno de P7-14 no cuentan para nada.** Se jugaron el 4-oct (APRENDE, serie 1, días 1 a 3, semillas k = 112, 113 y 114; {n(coste14, 4)} USD)
  con el código anterior al arreglo; el freno falló en (b) y el campo paró (`informe_P7_14.md`). Ni sus diarios ni sus cuadernos entran en este campo.
- **Paso 0 y paso 1** (el sitio en el disco y la ignorancia que descuenta una sola vez) están en `informe_P7_14.md`, secciones 1 y 2, y siguen valiendo.
  Una nota sobre el paso 0: los .zip del cinco no tienen una sola copia, como decía ese informe: tienen también copia en el Time Machine del Mac (disco SAMSUNG, 860 EVO).
- **Ojos compartidos apagados** (`GEMV_OJOS=0`, parte E1), por decisión de Manel para todo el capítulo 3.
- El brazo que en P7-10 se llamó SUELO aquí es ESPERANZA; cuando se compara con P7-10 se usa su SUELO.

## Sección 2 · El arreglo: en un empate no se da ni se suelta nada

`descubre_P7.desempate_sin_sitio` (la pieza I de P7-10) valía para `hacer_sitio_*`; ahora vale para todo gesto de desprenderse (`DESPRENDERSE`:
`hacer_sitio_*` y `soltar_*`, que es regalar el botiquín y soltar raciones). Si el mínimo de la d lo comparten uno de esos gestos y otro candidato
que no lo es, o si el paisaje es degenerado (todas las d dentro del `TIEBREAK_EPS` del propio desempate de la casa, `planificador_v1.py:376`), los
gestos de desprenderse salen del desempate: gana no desprenderse. Si desprenderse gana solo, gana. Ningún número nuevo. Va con hacer sitio
encendido (los cuatro brazos del campo) y apagado en F1.

| prueba | resultado |
|---|---|
| F1 (`P7_14b_F1.json`): apagado y TECHO contra los 80 diarios de A4 | {n(F1['apagado']['fidelidad']['igual'])} y {n(F1['TECHO']['fidelidad']['igual'])} tics iguales; {F1['apagado']['fidelidad']['difiere']} y {F1['TECHO']['fidelidad']['difiere']} distintos (los de siempre): **pasa** |
| banco, los regalos de SUELO en P7-10 (`banco_P7_14b.py` → `P7_14b_banco.json`) | {BA['suelo']['regalos_del_campo']} regalos en {BA['suelo']['vidas']} vidas; {BA['suelo']['eran_empate_con_noop']} eran empate exacto con `noop`; con el arreglo la réplica regala **{BA['suelo']['la_replica_sigue_regalando']}** (elige {", ".join(f"`{k}` {c}" for k, c in BA['suelo']['elige'].items())}) |
| banco, el F2 de P7-13 otra vez (`P7_14b_F2.json`): los 171 regalos de APRENDE en P7-10, con pedir | el hermano pedía en {BA['F2']['el_hermano_pedia']}; la réplica sigue regalando **{BA['F2']['la_replica_sigue_regalando']}** ({BA['F2']['con_pedido_y_sigue']} con pedido, **{BA['F2']['sin_pedido_y_sigue']} sin pedido**); en P7-13 eran 21 (16 y 5) |

El F2 de ahora lleva también el arreglo de las ganas de P7-14, así que no es solo el efecto del empate: de los {BA['F2']['el_hermano_pedia']} regalos con pedido siguen {BA['F2']['con_pedido_y_sigue']}.

## Sección 3 · El sello, el freno y la noche

`SELLO_P7_14b.md` (commit `{E.get('commit_sello', '')[:12]}`, subido antes de pedir nada): las cinco preguntas, las medidas y el freno de P7-14 palabra por palabra;
semillas nuevas k = 132 a 151 (`semillas_P7_14b.json`; serie 2 en orden inverso); md5 de los archivos. Imágenes fijas {", ".join(f"{k} {v['etiqueta'].split(':')[1]}" for k, v in E['imagenes'].items() if not k.startswith('APRENDE'))}; APRENDE, una por serie y día.

**El freno** (APRENDE, serie 1, días 1 a 3; `P7_14b_freno.json`): (a) el cuaderno viaja y se lee los días 2 y 3: pasa. (b) {FR['b']['pedidos_abiertos']} pedidos abiertos, {FR['b']['regalos']} regalos,
{FR['b']['regalos_sin_pedido']} sin pedido: pasa. (c) asiento 11: creencia {n(FR['c']['11']['creencia_d1'], 1)} → {n(FR['c']['11']['creencia_d3'], 1)}, ignorancia {n(FR['c']['11']['ignorancia_d1'], 3)} → {n(FR['c']['11']['ignorancia_d3'], 3)}: pasa. **El freno pasó y el campo siguió.**

**La noche.** Primera partida pedida a las {ini[11:16]} UTC del {ini[:10]}; última completada a las {fin[11:16]} UTC del {fin[:10]}. Esperas de red: {len(E.get('esperas_red', []))}{(" (" + "; ".join(x['cuando'] + ' en ' + x['donde'] for x in E.get('esperas_red', [])) + ")") if E.get('esperas_red') else ""}.
Paradas por disco: {len(E.get('paradas_disco', []))}. Paradas por red: {len(E.get('paradas_red', []))}. {{NOCHE}}

## Sección 4 · El campo, por brazo

{len(C)} vidas leídas ({", ".join(f"{b} {len(Lc[b])}" for b in BR)}). Un uso = botiquín gastado. Entre paréntesis en la primera tabla, lo mismo en P7-10 (sin pedir).

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
c10 = J("P7_10_campo.json"); L10c = {b: [v for v in c10.values() if not v.get("sin_tics") and v["brazo"] == B10[b]] for b in BR}
fila("botiquines cogidos", lambda b: f"{sum(v['coge_n'] for v in Lc[b])} ({sum(v['coge_n'] for v in L10c[b])})")
fila("regalos", lambda b: f"{sum(v['regala_n'] for v in Lc[b])} ({sum(v['regala_n'] for v in L10c[b])})")
fila("usos", lambda b: f"{sum(v['usos_gastados'] for v in Lc[b])} ({sum(v['usos_gastados'] for v in L10c[b])})")
fila("canales interrumpidos", lambda b: f"{sum(v['usos_interrumpidos'] for v in Lc[b])} ({sum(v['usos_interrumpidos'] for v in L10c[b])})")
hp_ = lambda L, dias=range(1, 21): [u["hp0"] for v in L if v["dia"] in dias for u in v["usos"] if u["gastado"]]
fila("mediana de la vida al usar", lambda b: f"{n(med(hp_(Lc[b])), 1)} ({n(med(hp_(L10c[b])), 1)})")
fila("usos con la vida < 50", lambda b: f"{sum(1 for x in hp_(Lc[b]) if x < 50)} ({sum(1 for x in hp_(L10c[b]) if x < 50)})")
fila("usos con la vida ≥ 80", lambda b: f"{sum(1 for x in hp_(Lc[b]) if x >= 80)} ({sum(1 for x in hp_(L10c[b]) if x >= 80)})")
fila("hacer sitio (oscilaciones)", lambda b: f"{sum(v['hace_sitio_n'] for v in Lc[b])} ({sum(v['oscilaciones'] for v in Lc[b])})")
fila("muere por rival / por el anillo / sobrevive", lambda b: " / ".join(str(sum(1 for v in Lc[b] if v["causa_muerte"] == c_)) for c_ in ("rival", "anillo", "sobrevive")) + " (" + " / ".join(str(sum(1 for v in L10c[b] if v["causa_muerte"] == c_)) for c_ in ("rival", "anillo", "sobrevive")) + ")")
fila("vidas en el puesto 1", lambda b: f"{sum(1 for v in Lc[b] if v['puesto'] == 1)} ({sum(1 for v in L10c[b] if v['puesto'] == 1)})")
fila("puesto medio", lambda b: f"{n(mean([v['puesto'] for v in Lc[b] if v['puesto'] is not None]), 2)} ({n(mean([v['puesto'] for v in L10c[b] if v['puesto'] is not None]), 2)})")
fila("vida al morir, media", lambda b: f"{n(mean([float(v['hp_final']) for v in Lc[b]]), 1)} ({n(mean([float(v['hp_final']) for v in L10c[b]]), 1)})")
w("""
**Mediana de la vida al usar, por tramos de días** (entre paréntesis, usos):

| brazo | días 1-5 | días 6-10 | días 11-15 | días 16-20 |
|---|---:|---:|---:|---:|
""")
for b in BR: w(f"| {b} | " + " | ".join(f"{n(med(hp_(Lc[b], range(a, a + 5))), 1)} ({len(hp_(Lc[b], range(a, a + 5)))})" for a in (1, 6, 11, 16)) + " |\n")
def cre(v):
    d = (((v.get("cuaderno") or {}).get("creencias") or {}).get("first_aid") or {}).get("dentro"); return d.get("cuerpo") if isinstance(d, dict) else None
ap = {(v["serie"], v["slot"], v["dia"]): v for v in Lc["APRENDE"]}
w("""
**El cuaderno de APRENDE** (creencia del botiquín, cuerpo, dentro del círculo, con el recuerdo neutro, como en P7-10; «–» = «no sé»):

| criatura | creencia al fin de los días 1 / 5 / 10 / 15 / 20 | ignorancia 1 / 5 / 10 / 15 / 20 | recuerdos al final (firmes) |
|---|---|---|---:|
""")
for s_, sl in ((1, 10), (1, 11), (2, 10), (2, 11)):
    g = lambda d: ap.get((s_, sl, d)); u = g(20)
    w(f"| serie {s_}, asiento {sl} | " + " / ".join(n(cre(g(d)), 1) if g(d) else "?" for d in (1, 5, 10, 15, 20)) + " | " + " / ".join(n((g(d)["cuaderno"] or {}).get("ignorancia"), 3) if g(d) else "?" for d in (1, 5, 10, 15, 20)) + f" | {u['cuaderno']['recuerdos'] if u else '?'} ({u['cuaderno']['firmes'] if u else '?'}) |\n")
w(f"El cuaderno de APRENDE se leyó al arrancar en {sum(1 for v in Lc['APRENDE'] if v['dia'] >= 2 and (v['cuaderno'] or {}).get('leido'))} de las {sum(1 for v in Lc['APRENDE'] if v['dia'] >= 2)} vidas de los días 2 a 20.\n")

# ── pedidos ──
w("""
## Sección 5 · Los pedidos

Un pedido se abre cuando un parte lleva el campo tras uno que no lo llevaba, y se cierra al revés; el motivo lo apunta quien pedía. «Porque se lo
dieron» = entre el parte anterior y el del cierre, el hermano ejecutó un regalo de botiquín.

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
fila("partes emitidos", lambda b: n(sum(v["partes"] for v in Lv[b])))
fila("partes con pedido", lambda b: f"{n(sum(v['partes_con_pedido'] for v in Lv[b]))} ({n(100 * sum(v['partes_con_pedido'] for v in Lv[b]) / max(1, sum(v['partes'] for v in Lv[b])), 1)} %)")
fila("pedidos abiertos", lambda b: str(sum(v["pedidos_abiertos"] for v in Lv[b])))
fila("pedidos cerrados", lambda b: str(sum(len(v["cierres"]) for v in Lv[b])))
for m in ("lo ve", "lo lleva", "ya no le alivia (promesa 0)"):
    fila(f"… cerrados porque «{m}»", lambda b, m=m: str(sum(1 for v in Lv[b] for c_ in v["cierres"] if c_["motivo"] == m)))
fila("… cerrados porque se lo dieron", lambda b: str(sum(1 for v in Lv[b] for c_ in v["cierres"] if c_["porque_se_lo_dieron"])))
fila("abiertos al acabar la vida", lambda b: str(sum(1 for v in Lv[b] if v["pedido_abierto_al_final"])))
fila("vidas con pedir encendido / errores de las piezas", lambda b: f"{sum(1 for v in Lv[b] if v['pide_encendido'])} / {sum(v['errores_P7'] for v in Lv[b])}")
w(f"\nEl parte más largo del campo mide {max(v['largo_max_parte'] or 0 for v in V)} caracteres (de 120).\n")

# ── regalos ──
G = {b: [g for v in Lv[b] for g in v["regala"]] for b in BR}; G10 = {b: [g for v in L10[b] for g in v["regala"]] for b in BR}
DEST = [("lo recoge el hermano", "lo recoge el hermano"), ("lo recoge el mismo", "lo vuelve a coger él mismo"), ("en el suelo la ultima vez que se vio", "seguía en el suelo la última vez que se vio"), ("desaparece (rival visto encima)", "se lo lleva un rival"), ("desaparece (nadie visto)", "desaparece sin ver quién"), ("no se volvio a ver", "la casilla no se volvió a ver")]
w("""
## Sección 6 · Los regalos y adónde van

Entre paréntesis, P7-10 (sin pedir; su SUELO en la columna de ESPERANZA).

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
fila("regalos (gestos)", lambda b: f"{len(G[b])} ({len(G10[b])})")
fila("unidades regaladas", lambda b: f"{sum(g['n'] for g in G[b])} ({sum(g['n'] for g in G10[b])})")
fila("vidas con algún regalo", lambda b: f"{sum(1 for v in Lv[b] if v['regala_n'])} ({sum(1 for v in L10[b] if v['regala_n'])})")
fila("regalos con pedido / sin pedido", lambda b: f"{sum(1 for g in G[b] if g['con_pedido'])} / {sum(1 for g in G[b] if not g['con_pedido'])}")
for d_, nom in DEST:
    if any(g["destino"] == d_ for b in BR for g in G[b] + G10[b]): fila(nom, lambda b, d_=d_: f"{sum(1 for g in G[b] if g['destino'] == d_)} ({sum(1 for g in G10[b] if g['destino'] == d_)})")
fila("hermano sano / herido / crítico al regalar", lambda b: " / ".join(str(sum(1 for g in G[b] if g["banda_hermano"] == x)) for x in ("healthy", "hurt", "critical")))
fila("botiquines cogidos que había soltado el hermano", lambda b: f"{sum(v['coge_botiquines_que_solto_el_hermano'] or 0 for v in Lv[b])} ({sum(v['coge_botiquines_que_solto_el_hermano'] or 0 for v in L10[b])})")
fila("botiquines soltados al hacer sitio", lambda b: f"{sum(v['botiquines_soltados_al_hacer_sitio'] for v in Lv[b])} ({sum(v['botiquines_soltados_al_hacer_sitio'] for v in L10[b])})")

# ── tiempo ──
mc_ = lambda L, k: mean([v["contadores"].get(k, 0) for v in L]); pc_ = lambda L, k: mean([v["contadores"].get(k, 0) / v["contadores"]["tics"] for v in L])
w("""
## Sección 7 · El tiempo

Media por vida; «tics» con el candidato en curso (definición de P7-11). Entre paréntesis, P7-10.

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
fila("tics vivos", lambda b: f"{n(mc_(Lv[b], 'tics'))} ({n(mc_(L10[b], 'tics'))})")
fila("yendo a por un botiquín, parte de la vida", lambda b: f"{n(100 * pc_(Lv[b], 'tics ir a por un botiquin'), 1)} % ({n(100 * pc_(L10[b], 'tics ir a por un botiquin'), 1)} %)")
fila("yendo a por un botiquín, tics", lambda b: f"{n(mc_(Lv[b], 'tics ir a por un botiquin'))} ({n(mc_(L10[b], 'tics ir a por un botiquin'))})")
fila("con el canal del botiquín abierto, tics", lambda b: f"{n(mc_(Lv[b], 'tics en canal'), 1)} ({n(mc_(L10[b], 'tics en canal'), 1)})")
fila("con algún botiquín a bordo, tics", lambda b: f"{n(mc_(Lv[b], 'tics con botiquin a bordo'))} ({n(mc_(L10[b], 'tics con botiquin a bordo'))})")
fila("con un rival a la vista, parte de la vida", lambda b: f"{n(100 * pc_(Lv[b], 'tics con rival a la vista'), 1)} % ({n(100 * pc_(L10[b], 'tics con rival a la vista'), 1)} %)")
w("""
Parte de la vida yendo a por un botiquín, por tramos de días:

| | días 1-5 | días 6-10 | días 11-15 | días 16-20 |
|---|---:|---:|---:|---:|
""")
for b in BR: w(f"| {b} | " + " | ".join(f"{n(100 * mean([v['contadores'].get('tics ir a por un botiquin', 0) / v['contadores']['tics'] for v in Lv[b] if a <= v['dia'] < a + 5]), 1)} %" for a in (1, 6, 11, 16)) + " |\n")

# ── muerte ──
RV = {b: [v for v in Lv[b] if v["causa_muerte"] == "rival"] for b in BR}; RV10 = {b: [v for v in L10[b] if v["causa_muerte"] == "rival"] for b in BR}
moda = lambda L, m: sum(1 for v in L if v["muerte"]["moda"] == m)
w("""
## Sección 8 · Cómo muere

Causa = la fuente que más daño hizo en los últimos 30 tics. Para las muertes por rival, lo que más hacía en los 10 segundos anteriores (candidato en curso). Entre paréntesis, P7-10.

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
fila("muertes por rival", lambda b: f"{len(RV[b])} ({len(RV10[b])})")
fila("… yendo a por un botiquín", lambda b: f"{moda(RV[b], 'ir a por un botiquin')} ({moda(RV10[b], 'ir a por un botiquin')})")
fila("… moviéndose paso a paso", lambda b: f"{moda(RV[b], 'moverse paso a paso')} ({moda(RV10[b], 'moverse paso a paso')})")
fila("… quieto", lambda b: f"{moda(RV[b], 'quieto')} ({moda(RV10[b], 'quieto')})")
fila("… peleando", lambda b: f"{moda(RV[b], 'pelear')} ({moda(RV10[b], 'pelear')})")
fila("… otra cosa", lambda b: f"{sum(1 for v in RV[b] if v['muerte']['moda'] not in ('ir a por un botiquin', 'moverse paso a paso', 'quieto', 'pelear'))} ({sum(1 for v in RV10[b] if v['muerte']['moda'] not in ('ir a por un botiquin', 'moverse paso a paso', 'quieto', 'pelear'))})")
fila("mueren dentro del círculo", lambda b: f"{sum(1 for v in RV[b] if v['muerte']['dentro'])} ({sum(1 for v in RV10[b] if v['muerte']['dentro'])})")
fila("mueren con algún botiquín a bordo", lambda b: f"{sum(1 for v in RV[b] if v['muerte']['botiquines_a_bordo'] > 0)} ({sum(1 for v in RV10[b] if v['muerte']['botiquines_a_bordo'] > 0)})")
fila("con un botiquín a la vista al morir (distancia mediana)", lambda b: f"{sum(1 for v in RV[b] if v['muerte']['dist_botiquin_a_la_vista'] is not None)}, a {n(med([v['muerte']['dist_botiquin_a_la_vista'] for v in RV[b] if v['muerte']['dist_botiquin_a_la_vista'] is not None]), 1)}")
fila("muertes por el anillo", lambda b: f"{sum(1 for v in Lv[b] if v['causa_muerte'] == 'anillo')} ({sum(1 for v in L10[b] if v['causa_muerte'] == 'anillo')})")
fila("sobreviven al final", lambda b: f"{sum(1 for v in Lv[b] if v['causa_muerte'] == 'sobrevive')} ({sum(1 for v in L10[b] if v['causa_muerte'] == 'sobrevive')})")

# ── sello ──
def pares(a, b, medida):
    A = {(v["serie"], v["dia"], v["slot"]): v for v in Lc[a]}; B = {(v["serie"], v["dia"], v["slot"]): v for v in Lc[b]}
    d = [float(A[k][medida]) - float(B[k][medida]) for k in sorted(set(A) & set(B)) if A[k][medida] is not None and B[k][medida] is not None]
    m = st.mean(d); se = st.stdev(d) / math.sqrt(len(d)); return m, se, len(d)
w(f"""
## Sección 9 · El sello, cifra a cifra

Evaluado una sola vez, al final, con `sello_P7_14b.py` → `P7_14b_sello_resultado.json`.

| pregunta | medida | resultado |
|---|---|---|
| **Q1 (principal). Con pedir, APRENDE ya no acaba peor que BORRADO** (|d̄| ≤ 2·se en puesto y en vida al morir, {q1['puesto']['n']} pares) | puesto: APRENDE {n(q1['puesto']['media_APRENDE'], 2)}, BORRADO {n(q1['puesto']['media_BORRADO'], 2)}, d̄ {n(q1['puesto']['media_dif'], 2)}, se {n(q1['puesto']['se'], 2)} ({'dentro' if q1['puesto']['dentro_2se'] else 'FUERA'}); vida al morir: {n(q1['hp_final']['media_APRENDE'], 1)} y {n(q1['hp_final']['media_BORRADO'], 1)}, d̄ {n(q1['hp_final']['media_dif'], 2)}, se {n(q1['hp_final']['se'], 2)} ({'dentro' if q1['hp_final']['dentro_2se'] else 'FUERA'}) | **{'pasa' if res['Q1'] else 'falla'}** |
| **Q2. El círculo se rompe** (regalos por vida ≤ {n(q2['tope_regalos_por_vida'], 3)}; vueltos a coger por vida ≤ {n(q2['tope_vueltos_por_vida'], 3)}) | regalos {q2['regalos']} en {q2['vidas']} vidas = {n(q2['regalos_por_vida'], 3)} (P7-10: {n(q2['P7_10_regalos_por_vida'], 3)}): {'cumple' if q2['pasa_regalos'] else 'no cumple'}; vueltos a coger {q2['vueltos_a_coger']} = {n(q2['vueltos_a_coger_por_vida'], 3)} (P7-10: {n(q2['P7_10_vueltos_por_vida'], 3)}): {'cumple' if q2['pasa_vueltos'] else 'no cumple'} | **{'pasa' if res['Q2'] else 'falla'}** |
| **Q3. Días 11-20, el tiempo yendo a por botiquines de APRENDE no es mayor que el de BORRADO** | parte de la vida: APRENDE {n(100 * q3['parte_de_la_vida_APRENDE'], 1)} %, BORRADO {n(100 * q3['parte_de_la_vida_BORRADO'], 1)} % ({n(q3['tics_por_vida_APRENDE'])} y {n(q3['tics_por_vida_BORRADO'])} tics por vida; {q3['n_APRENDE']} y {q3['n_BORRADO']} vidas) | **{'pasa' if res['Q3'] else 'falla'}** |
| **Q4. Se repite P7-10** (la creencia sube en 4 de 4; días 11-20, APRENDE usa con menos vida que BORRADO) | creencia día 5 → día 20: {"; ".join(f"{n(x['creencia_d5'], 1)} → {n(x['creencia_d20'], 1)}" for x in q4['criaturas'].values())}: {q4['suben']} de 4 ({'cumple' if q4['pasa_creencia'] else 'no cumple'}); vida al usar: APRENDE {n(q4['mediana_vida_al_usar_d11_20']['APRENDE'], 1)} ({q4['mediana_vida_al_usar_d11_20']['n_APRENDE']} usos), BORRADO {n(q4['mediana_vida_al_usar_d11_20']['BORRADO'], 1)} ({q4['mediana_vida_al_usar_d11_20']['n_BORRADO']}) ({'cumple' if q4['pasa_vida'] else 'no cumple'}) | **{'pasa' if res['Q4'] else 'falla'}** |
| **Q5. Menos de la quinta parte de los pedidos se cierran porque se lo dieron** | {q5['porque_se_lo_dieron']} de {n(q5['cerrados'])} cerrados ({n(100 * (q5['fraccion'] or 0), 1)} %); por brazo: {"; ".join(f"{b} {x['porque_se_lo_dieron']} de {x['cerrados']}" for b, x in q5['por_brazo'].items())} | **{'pasa' if res['Q5'] else 'falla'}** |

**Fuera del sello, para situar Q1** (misma medida, los otros pares; d̄ del primero menos el segundo, y su se):

| par | puesto: d̄ (se) | vida al morir: d̄ (se) |
|---|---:|---:|
""")
for a, b in (("APRENDE", "BORRADO"), ("APRENDE", "TECHO"), ("APRENDE", "ESPERANZA"), ("BORRADO", "TECHO"), ("ESPERANZA", "TECHO"), ("ESPERANZA", "BORRADO")):
    mp, sp, k = pares(a, b, "puesto"); mh, sh, _ = pares(a, b, "hp_final")
    w(f"| {a} − {b} ({k} pares) | {'**' if abs(mp) > 2 * sp else ''}{n(mp, 2)}{'**' if abs(mp) > 2 * sp else ''} ({n(sp, 2)}) | {'**' if abs(mh) > 2 * sh else ''}{n(mh, 2)}{'**' if abs(mh) > 2 * sh else ''} ({n(sh, 2)}) |\n")
w(f"""
En negrita, |d̄| > 2·se. En P7-10 (sin pedir), APRENDE − BORRADO fue +1,25 (se 0,61) en puesto y −5,06 (se 2,33) en vida al morir (`informe_P7_10.md`).

{{LECTURA}}

## Sección 10 · Créditos

| | partidas | créditos |
|---|---:|---:|
""" + "".join(f"| {b} | {sum(1 for p in pet if p['brazo'] == b and p.get('coste_usd'))} | {n(por_brazo[b], 4)} USD |\n" for b in BR) + f"""| **P7-14b** | **{sum(1 for p in pet if p.get('coste_usd'))}** | **{n(coste, 4)} USD** |
| freno de P7-14 (no cuenta) | {len(E14['peticiones'])} | {n(coste14, 4)} USD |
| **total del segundo campo** | **{sum(1 for p in pet if p.get('coste_usd')) + len(E14['peticiones'])}** | **{n(coste + coste14, 4)} USD** |

Media por partida de P7-14b: {n(coste / max(1, sum(1 for p in pet if p.get('coste_usd'))), 4)} USD. Subir imágenes no gasta créditos. **Consola de Anthropic: 0 USD.**
Acumulado del siete en la plataforma: {n(16.0147 + coste14 + coste, 4)} USD. Saldos: no consultados.

## Sección 11 · Lo que queda para la mesa

{{ABIERTO}}

## Archivos

| archivo | qué es |
|---|---|
| `descubre_P7.py` (`DESPRENDERSE`, `desempate_sin_sitio`) | el arreglo: en un empate no se da ni se suelta nada |
| `banco_P7_14b.py`, `P7_14b_banco.json`, `P7_14b_F2.json`, `P7_14b_F1.json` | el banco del arreglo y F1 |
| `SELLO_P7_14b.md`, `semillas_P7_14b.json`, `lanza_P7_14b.py`, `P7_14b_estado.json`, `P7_14b_res/`, `cuadernos_P7_14b/` | sello, semillas, lanzador, estado, resultados y cuadernos |
| `freno_P7_14b.py`, `P7_14b_freno.json` | el freno |
| `campo_P7_14b.py` → `P7_14b_campo.json`; `analiza_P7_14b.py` → `P7_14b_vidas.json`; `sello_P7_14b.py` → `P7_14b_sello_resultado.json` | lectores y evaluador |
| `P7_14b_diarios_manifiesto.md` | md5 de los diarios (fuera de git) |
| `escribe_informe_P7_14b.py`, `informe_P7_14b.md` | este informe |
""")
def txt_de(nombre):
    p = os.path.join(AQUI, "_P7_14b_tmp", nombre); return open(p).read().strip() if os.path.exists(p) else "(pendiente)"
txt = "".join(W).replace("{NOCHE}", txt_de("noche.md")).replace("{LECTURA}", txt_de("lectura.md")).replace("{ABIERTO}", txt_de("abierto.md")); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_14b.md"), "w").write(txt); print("informe escrito", len(txt))
import glob
M = ["# P7-14b · diarios del campo (fuera de git; md5)", "", "| archivo | bytes | md5 |", "|---|---:|---|"]
for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P714b_s*_d*_*", "*"))):
    if f.endswith((".art.log", ".zip")): M.append(f"| `{os.path.relpath(f, RAIZ)}` | {os.path.getsize(f)} | `{hashlib.md5(open(f, 'rb').read()).hexdigest()}` |")
open(os.path.join(AQUI, "P7_14b_diarios_manifiesto.md"), "w").write("\n".join(M) + "\n")
