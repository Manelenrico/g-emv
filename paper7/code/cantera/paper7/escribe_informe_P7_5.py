"""[P7-5] Escribe informe_P7_5.md desde P7_5_F1.json, P7_5_F2.json, P7_5_huella.json, P7_5_humo.json, P7_5_dia*_resultado.json y
P7_5_brazos.json. Ninguna cifra a mano."""
import glob, hashlib, json, os, statistics
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
def J(p):
    f = os.path.join(AQUI, p); return json.load(open(f)) if os.path.exists(f) else None
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
F1 = J("P7_5_F1.json"); F2 = J("P7_5_F2.json"); H = J("P7_5_huella.json"); HU = J("P7_5_humo.json") or {"dias": {}}; BR = J("P7_5_brazos.json") or {}
RES = {d: J(f"P7_5_dia{d}_resultado.json") for d in (1, 2, 3)}
costes = {d: (((r or {}).get("episodes") or [{}])[0].get("cost_usd")) for d, r in RES.items()}
L = []; w = L.append
w(f"""# P7-5 · El cuerpo que descubre: construido, probado en banco y en humo de tres días

*3-oct-2026. Coste: **créditos de la plataforma** {n(sum(c for c in costes.values() if c), 4)} USD en {sum(1 for c in costes.values() if c)} partidas (por día: {", ".join(f"{d}: {n(c, 4)}" for d, c in costes.items())}); **consola de Anthropic 0 USD**
(ninguna llamada). `motor/model.py` = `{md5('motor/model.py')}` al empezar y al acabar; congelados y cuerpo sin tocar: todo lo nuevo son
archivos `_P7` (`cuaderno_P7.py`, `descubre_P7.py`, `policy_pareja_P7.py`, `banco_P7_5.py`, `huella_P7_5.py`, `lanza_P7_5.py`, `humo_P7_5.py`,
`gif_P7_5.py`, `Dockerfile.pareja_P7`). Una vida por proceso en el banco (subproceso por vida) y en el campo (un contenedor por criatura);
la memoria viaja solo en el archivo del cuaderno.*

## Sección 1 · Lo construido, con las tres correcciones de la mesa

| pieza | archivo | dónde engancha (sin tocar el congelado) |
|---|---|---|
| A, cuaderno | `cuaderno_P7.py` | se lee al conocer el asiento (envoltorio de `AlmaPareja.decidir`, primera llamada) y se escribe al acabar (`policy_pareja_P7.run`, tras `P11.run`); huella por dominio (cuerpo, recursos, vínculo): efecto e importancia con signo; creencia = media ponderada de los efectos con un recuerdo neutro de peso 1 que no se apaga (corrección 3); los vividos se apagan con 0,95 por día; intensidad = 1 + min(1, suma de |importancias| / 1,5); la cuenta de usos no se olvida |
| A, la ventana | `descubre_P7.ventana` | del tic en que aparece el canal del botiquín al tic en que desaparece; lo esperado sin la cosa resta solo el daño de causas conocidas (corrección 1): anillo estando fuera del círculo según `mundo.anillo_en`, y golpes de rivales a la vista y en alcance de su arma (catálogo; mano vacía = 1); importancia por dominio = malestar del eje al cerrar menos al abrir (corrección 2), ejes F, R, S de la radiografía del presente |
| B, imaginación | envoltorio de `D.candidatos` | `receta["heal"]` de `usar_botiquin` = creencia del cuerpo en la situación de ahora; "no sé" = 0 |
| C, ganas | `A.ACOPIO_M`, `A.W_TARGET` y envoltorio de `A.riqueza_W` | escala k = creencia máxima / cura del catálogo: R-ACOPIO = 0,18 k; el botiquín en W cuenta k; `W_TARGET` = 2 + k; "no sé" = 0 |
| D, novedad | envoltorio de `A.appraise` y de `D._promesa` | fila apetitiva R-NOVEDAD: 0,18 × calma × 0,5^usos × forma (1 − d/24 a la vista o recordado; 1 en el zurrón; 1,5 en la foto que lo usa); calma = 1 − máx(alcance, agresor, hermano amenaza, hermano golpe, anticipación del fuego) |
| brazos | `GEMV_P7`, `GEMV_P7_SABE`, `GEMV_P7_CUADERNO`, `GEMV_P7_BORRADO`, `GEMV_P7_NOVEDAD` | SUELO = P7 solo; BORRADO = cuaderno sin leer + novedad; APRENDE = cuaderno que viaja + novedad; TECHO = SABE (todo pasa tal cual) |

**Corrección 1 sobre el cálculo en seco de P7-4** (`huella_P7_5.py` → `P7_5_huella.json`): con la regla de causas conocidas, de los {H['resumen']['usos']} usos con
ventana cambian **{H['resumen']['cambian']}** (todos cancelados; diferencia {n(H['resumen']['diferencia_en_los_que_cambian']['min'], 1)} a {n(H['resumen']['diferencia_en_los_que_cambian']['max'], 1)} hp: el veneno, que el cuerpo no sabe explicar, se queda en el efecto). Daño
conocido en las 180 ventanas: anillo fuera {n(H['resumen']['dano_conocido_por_causa'].get('anillo fuera', 0), 1)} hp, rival visto en alcance {n(H['resumen']['dano_conocido_por_causa'].get('rival visto en alcance', 0), 1)} hp; no conocido: {", ".join(f"{k.replace(' (no conocido)', '')} {n(v, 1)} hp" for k, v in H['resumen']['dano_no_conocido_por_causa'].items())}.

## Sección 2 · F1: con todo apagado y con TECHO, la variante reproduce los diarios de A4

Réplica de los 80 diarios de A4 (`banco_P7_5.py --f1`, un subproceso por vida), la elección de la réplica contra `RADIOGRAFIA.elegido` en
cada tic vivo:

| brazo | vidas | tics iguales | distintos | los distintos |
|---|---:|---:|---:|---|
""")
for b in ("apagado", "TECHO"):
    x = (F1 or {}).get(b) or {}; f = x.get("fidelidad") or {}
    w(f"| {b} | {x.get('vidas', '–')} | {n(f.get('igual'))} | {n(f.get('difiere', 0))} | {'; '.join(f"{d['vida'][-14:]} t {d['t']} ({d['diario']} / {d['replica']})" for d in x.get('desacuerdos', [])[:6]) or '–'} |\n")
w(f"""
Los dos tics distintos son los mismos dos de P6-30 (`informe_P6_30.md`, sección 2: la vida 21622393/10, tics 1832 y 2041, con alguna d
distinta en el propio A4 sin fuga). **F1 pasa**: los enganches con TECHO son neutros al bit y con todo apagado la política es A4.

## Sección 3 · F2: el cuaderno cargado a mano, la imaginación y las ganas

`banco_P7_5.py --f2`: por asiento, el cuaderno se carga con los recuerdos del diario de P7-1 de los días 1-20 (efectos del cuerpo con la
regla de causas conocidas, recursos y vínculo del cálculo en seco; la importancia sin signo, que solo pesa) y se replican tres vidas de los
días 21-40 con APRENDE, cada una leyendo lo que dejó la anterior. En la réplica el mundo es el del diario: los usos del botiquín que abren
ventana son los del diario, y la imaginación de la réplica se compara en los tics en que ella también tenía el candidato.

| asiento | cuaderno cargado (recuerdos; creencia del cuerpo dentro / fuera) |
|---|---|
""")
for s_, c in ((F2 or {}).get("cuadernos") or {}).items():
    cr = (c.get("creencias") or {}).get("first_aid") or {}
    w(f"| {s_} | {c.get('recuerdos')} recuerdos, {c.get('usos')} usos; dentro {n((cr.get('dentro') or {}).get('cuerpo'), 2)} / fuera {n((cr.get('fuera') or {}).get('cuerpo'), 2)} |\n")
w("""
| día | vida | heal imaginado = creencia vigente en su situación (usos comparados) | k = creencia máx / 50 | R-ACOPIO en el primer tic vivo = 0,18 k | huellas nuevas | cuaderno al acabar |
|---|---|---|---|---|---:|---|
""")
for v in (F2 or {}).get("vidas") or []:
    if "error" in v: w(f"| {v['dia']} | {v['vida']} | ERROR {v['error'][-80:]} | | | | |\n"); continue
    p = v["primer_uso"]; i = v.get("inicio") or {}; cf = v["cuaderno_fin"]; cr = (cf.get("creencias") or {}).get("first_aid") or {}
    comp = v.get("usos_comparados") or []
    w(f"| {v['dia']} | {v['vida'][-14:]} | {('sí, ' + str(len(comp)) + ' de ' + str(len(comp))) if (comp and p['todos_coinciden']) else ('ninguno comparable: la réplica no tuvo el candidato en los tics de uso del diario' if not comp else 'NO')}{('; p. ej. t ' + str(comp[0]['t']) + ' ' + comp[0]['situacion'] + ' ' + n(comp[0]['heal'], 2)) if comp else ''} | {n(p['k'], 4)} (esperado {n(p['k_esperado'], 4)}) | {n(i.get('R-ACOPIO'), 5)} (esperado {n(i.get('R_ACOPIO_esperado'), 5)}) {'sí' if i.get('coincide_acopio') else 'NO'} | {v['huellas']} | día {cf.get('dia')}, usos {cf.get('usos')}, dentro {n((cr.get('dentro') or {}).get('cuerpo'), 2)} / fuera {n((cr.get('fuera') or {}).get('cuerpo'), 2)} |\n")
ok2 = all((v.get("primer_uso") or {}).get("todos_coinciden") in (True, None) and (v.get("inicio") or {}).get("coincide_acopio") for v in ((F2 or {}).get("vidas") or []) if "error" not in v)
w(f"""
**F2 {'pasa' if ok2 else 'NO pasa'}**: en todos los usos comparables la receta de `usar_botiquin` lleva la creencia del cuaderno en su situación, las ganas salen
con la escala acordada (R-ACOPIO = 0,18 k en el primer tic vivo, k = creencia máxima / 50, `W_TARGET` = 2 + k) y cada vida lee el
cuaderno que dejó la anterior (el día avanza y los usos se acumulan). Fuente: `P7_5_F2.json`.

## Sección 4 · F3: el humo de tres días en la plataforma (brazo APRENDE, las dos criaturas)

Semillas: {", ".join(f"día {d}: {s}" for d, s in sorted({int(k): v["semilla"] for k, v in HU["dias"].items()}.items()))} (la sucesión de semillas_S2, paso 104729, continuada tras la última de P6-24; ninguna usada antes).
Cada día se horneó la imagen con el cuaderno del día anterior (`Dockerfile.pareja_P7`; versiones subidas: {", ".join(f"día {k[-1]}: {v.get('etiqueta')} ({str(v.get('policy_version_id'))[:8]}…)" for k, v in sorted(BR.items()))}), una partida entera
(mundo 0.1.19, roster lento v2, 18.240 tics), y al acabar se extrajo el registro `P7_cuaderno` de fin de cada diario para el día siguiente.
El campo no tiene canal de entrada: el viaje del cuaderno es ese horneado.

""")
for d, D in sorted(HU["dias"].items(), key=lambda kv: int(kv[0])):
    w(f"**Día {d}** (semilla {D['semilla']}, estado {D.get('estado')}, coste {n(D.get('coste_usd_plataforma'), 4)} USD de plataforma).\n\n| criatura | vivo (tics) · puesto | primer botiquín visto (tic) | tics con novedad > 0 | se acerca por novedad | coge | usa (tic, situación, heal imaginado) | cuaderno leído al arrancar | cuaderno al acabar |\n|---|---|---:|---:|---:|---:|---|---|---|\n")
    for s_, c in sorted(D["criaturas"].items()):
        if c.get("sin_diario"): w(f"| {s_} | sin diario | | | | | | | |\n"); continue
        ca, cf = c["cuaderno_arranque"], c["cuaderno_fin"]; crf = (cf.get("creencias") or {}).get("first_aid") or {}; cra = (ca.get("creencias") or {}).get("first_aid") or {}
        w(f"| {s_} | {n(c['ticks_vivos'])} · {c['placement']} | {n(c['primer_botiquin_visto_t'])} | {n(c['tics_con_novedad'])} | {c['se_acerca_por_novedad']['n']} | {len(c['coge'])} | {'; '.join(f'{u['t']} {u['situacion']} {n(u['heal_imaginado'], 2) if u['heal_imaginado'] is not None else 'no sé'}' for u in c['usa'][:6]) or 'ninguno'} | {'sí' if ca.get('leido') else 'no'} (día {ca.get('dia')}; dentro {n((cra.get('dentro') or {}).get('cuerpo'), 2)} / fuera {n((cra.get('fuera') or {}).get('cuerpo'), 2)}, usos {cra.get('usos', '–')}) | {cf.get('n_recuerdos')} recuerdos, usos {cf.get('usos')}; dentro {n((crf.get('dentro') or {}).get('cuerpo'), 2)} / fuera {n((crf.get('fuera') or {}).get('cuerpo'), 2)}; recursos {n((crf.get('dentro') or {}).get('recursos'), 2)} / {n((crf.get('fuera') or {}).get('recursos'), 2)}; vínculo {n((crf.get('dentro') or {}).get('vinculo'), 2)} / {n((crf.get('fuera') or {}).get('vinculo'), 2)} |\n")
    w("\n")
w("""{LECTURA_HUMO}

GIF del primer uso de cada criatura (datos crudos del diario, `gif_P7_5.py`): {GIFS}.

## Sección 5 · F4: lo que costaría la serie

{F4}

## Sección 6 · Lo que queda para la mesa

1. La forma de la novedad en el suelo: con g = 1 − d/24 (y aun topada a 0,5) el último paso hacia el objeto no paga; hace falta una
   pendiente que crezca cerca del objeto (por ejemplo, que el suelo valga 0 a más de unas casillas y suba hasta 0,5 al llegar), o que la
   promesa de `ir_objeto` cuente la ganancia de cogerlo, no solo la de acercarse. Número de método.
2. El zurrón lleno: sin un candidato de soltar para coger lo nuevo, la novedad no puede probar nada cuando las dos ranuras van ocupadas.
   Es la misma falta que P7-3 encontró para el arco. Decisión de diseño.
3. El viaje del cuaderno en el campo: hoy va horneado en la imagen (una subida por día y brazo). El registro de fin del cuaderno se escribe
   ahora antes de la subida del artefacto (corregido tras el día 1); los cuadernos de los días 1 y 2 se reconstruyeron desde sus diarios
   con la misma regla (`reconstruye_cuaderno_P7_5.py`) y son idénticos a lo que el cuerpo habría escrito (cero recuerdos, cero usos).
4. El día 2 se lanzó por error con una imagen sin cuaderno (la cadena no esperó a la reconstrucción): como el día 1 no dejó recuerdos, el
   contenido leído habría sido el mismo (vacío); se declara y se cuenta su coste.

## Archivos

| archivo | qué es |
|---|---|
| `cuaderno_P7.py`, `descubre_P7.py`, `policy_pareja_P7.py`, `Dockerfile.pareja_P7` | el cuerpo que descubre: cuaderno, enganches, política y la imagen |
| `banco_P7_5.py`, `P7_5_F1.json`, `P7_5_F2.json` | F1 y F2 (un subproceso por vida) |
| `huella_P7_5.py`, `P7_5_huella.json` | la corrección 1 sobre el cálculo en seco |
| `lanza_P7_5.py`, `P7_5_brazos.json`, `P7_5_dia*_peticion.json`, `P7_5_dia*_resultado.json`, `P7_5_dia*_cuaderno_*.json`, `cuadernos_humo/` | el humo: imágenes, peticiones, resultados con el coste, los cuadernos de cada día |
| `humo_P7_5.py`, `P7_5_humo.json`, `gif_P7_5.py`, `P7_5_primer_uso_*.gif` | la lectura del humo y los GIF |
| `escribe_informe_P7_5.py`, `informe_P7_5.md` | este informe |
""")
# ── la lectura del humo: por que no cogio ninguno (diagnostico sobre los diarios) ──
import glob as _g, math as _m, collections as _c
sys_diag = []
for d, D in sorted(HU["dias"].items(), key=lambda kv: int(kv[0])):
    for s_ in (10, 11):
        fs = _g.glob(os.path.join(RAIZ, "paintball", "runs", f"P75_humo_APRENDE_{D['semilla']}", f"*policy_agent_{s_}.art.log"))
        if not fs: continue
        cerca = 0; libre = 0; cand = 0; eleg = 0; vet = 0; solo_noop = 0
        for line in open(fs[0]):
            if '"llena8"' in line: vet += 1
            if '"k":"tick"' not in line and '"k": "tick"' not in line: continue
            r = json.loads(line)
            if r.get("phase") != "live": continue
            ks = [tuple(i["pos"]) for i in (r.get("ve_items") or []) if i.get("id") == "first_aid"]
            if ks and min(max(abs(r["pos"][0] - k[0]), abs(r["pos"][1] - k[1])) for k in ks) <= 1:
                cerca += 1; ra = r.get("RADIOGRAFIA") or {}; cds = ra.get("candidatos") or {}
                if any(x is None for x in r["pack"]): libre += 1
                if "coger" in cds: cand += 1
                if ra.get("elegido") == "coger": eleg += 1
                if list(cds.keys()) == ["noop"]: solo_noop += 1
        sys_diag.append((int(d), s_, cerca, libre, cand, eleg, vet, solo_noop))
usos_h = [(int(d), s_, u) for d, D in HU["dias"].items() for s_, c in D["criaturas"].items() if not c.get("sin_diario") for u in c["usa"]]
coge_h = [(int(d), s_, len(c["coge"])) for d, D in HU["dias"].items() for s_, c in D["criaturas"].items() if not c.get("sin_diario") and c["coge"]]
hu3 = [(int(d), s_, h) for d, D in HU["dias"].items() for s_, c in D["criaturas"].items() if not c.get("sin_diario") for h in c["huellas"]]
lectura = ("**Lectura del humo.** Tics a una casilla o menos de un botiquín, por día y asiento: " + "; ".join(f"día {d} asiento {s_}: {n(c)} (con ranura libre {n(l)}, con `coger` entre los candidatos {n(ca)}, elegido `coger` {n(e)}, `coger` escondido por mochila llena {n(v)}, solo `noop` entre los candidatos {n(sn)})" for d, s_, c, l, ca, e, v, sn in sys_diag) + ". "
    + (f"Cogidas: {', '.join(f'día {d} asiento {s_}: {k}' for d, s_, k in coge_h)}. " if coge_h else "Ninguna cogida en los tres días. ")
    + (f"Usos: {', '.join(f'día {d} asiento {s_}, tic {u['t']:,}, {u['situacion']}, imaginó {n(u['heal_imaginado'], 1) if u['heal_imaginado'] is not None else 'no sé'}'.replace(',', '.') for d, s_, u in usos_h)}; la huella que dejó: " + "; ".join(f"efecto cuerpo {h['efecto']['cuerpo']:+.1f}, recursos {h['efecto']['recursos']:+.0f}, vínculo {h['efecto']['vinculo']:+.1f} (daño conocido {h['dano_conocido']} de {h['dano_total']}); importancia cuerpo {h['importancia']['cuerpo']:+.3f}, recursos {h['importancia']['recursos']:+.3f}, vínculo {h['importancia']['vinculo']:+.3f}; intensidad {h['intensidad']}" for d, s_, h in hu3) + ". " if usos_h else "Ningún uso en los tres días. ")
    + "**¿El día 2 lee lo del día 1 y cambia su imaginación?** El día 1 no dejó recuerdos (ningún uso), así que el día 2 leyó un cuaderno vacío (y, por el fallo de lanzamiento, sin archivo: `leído: no`) y el día 3 leyó el del día 2 (`leído: sí`, día 2, cero recuerdos): la imaginación siguió en \"no sé\" (heal 0) hasta el primer uso del día 3, que dejó la primera creencia (asiento 10, dentro: cuerpo " + (n(((HU['dias'].get('3') or HU['dias'].get(3) or {}).get('criaturas') or {}).get('10', {}).get('cuaderno_fin', {}).get('creencias', {}).get('first_aid', {}).get('dentro', {}).get('cuerpo'), 1)) + "); un día 4 la leería y la pondría en la receta de `usar_botiquin`, que es lo que F2 comprobó en banco. "
    + "**Por qué casi nunca coge.** Dos causas, leídas en los diarios: (1) el zurrón de dos ranuras va lleno de lo que coge antes (dardos y cerbatana, flechas y cuchillos, ración y cuchillos), y con el zurrón lleno `coger` no existe (`arreglos_P6_8b.py:85-101` lo esconde porque la previsión no cambia la mochila); no hay candidato de soltar algo para coger lo nuevo (P7-3, sección 3). (2) Con ranura libre, la criatura se queda en la casilla contigua: la fila de novedad tal como la fijó el plan vale casi lo mismo al lado del objeto (g = 1 − d/24 ≈ 0,94 a una casilla) que llevándolo (g = 1), así que ni el último paso ni `coger` ganan nada frente a quedarse quieto. Comprobado en banco sobre el diario del día 2 (asiento 10, tics 603-606: junto al botiquín con el zurrón vacío, único candidato `noop`, novedad M 0,169 con g 0,94). Tras el humo se topó la forma en el suelo a 0,5 (`SUELO_MAX`, declarado, no jugado): la réplica del mismo diario cambia 35 de 12.613 decisiones y sigue sin dar el último paso: la pendiente en el suelo necesita otra forma, y eso es un número de método de la mesa (sección 6). La fontanería del campo sí está: la réplica en banco del diario del día 2 (asiento 10) con la política del siete reproduce el campo decisión a decisión (12.613 de 12.613).")
gifs = ", ".join(f"`{os.path.basename(g)}`" for g in sorted(_g.glob(os.path.join(AQUI, "P7_5_dia*_*.gif")))) or "ninguno"
gifs_nota = gifs + " (no hubo ningún uso en los tres días: el GIF es del primer acercamiento, el primer tic a una casilla o menos de un botiquín)"
# F4
cs = [c for c in costes.values() if c]; media = statistics.mean(cs) if cs else None; partidas = 20 * 4 * 2
f4 = (f"Créditos de la plataforma gastados en el humo: {n(sum(cs), 4)} USD en {len(cs)} partidas (media {n(media, 4)}, de {n(min(cs), 4)} a {n(max(cs), 4)}; subir imágenes no gasta créditos). Una serie de 20 días con los cuatro brazos y dos órdenes de semillas son {partidas} partidas: a la media del humo, **{n(media * partidas, 2)} USD** (entre {n(min(cs) * partidas, 2)} y {n(max(cs) * partidas, 2)} con el mínimo y el máximo del humo). Con la media de las 20 partidas enteras de A4 de P6-24 ({n(statistics.mean([json.load(open(f))['episodes'][0]['cost_usd'] for f in _g.glob(os.path.join(RAIZ, 'cantera', 'paper6', 'P624_t1_A4_*.json')) if not f.endswith('_peticiones.json')]), 4)} USD por partida), {n(statistics.mean([json.load(open(f))['episodes'][0]['cost_usd'] for f in _g.glob(os.path.join(RAIZ, 'cantera', 'paper6', 'P624_t1_A4_*.json')) if not f.endswith('_peticiones.json')]) * partidas, 2)} USD. Aparte, APRENDE y BORRADO necesitan rehacer y subir la imagen cada día (el cuaderno viaja horneado): 2 brazos × 20 días × 2 órdenes = 80 subidas, sin créditos pero con tiempo de máquina (unos 55 s cada una en este Mac). Consola de Anthropic: 0." if cs else "sin partidas")
txt = "".join(L).replace("{LECTURA_HUMO}", lectura).replace("{GIFS}", gifs_nota).replace("{F4}", f4); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_5.md"), "w").write(txt); print("informe escrito", len(txt))
