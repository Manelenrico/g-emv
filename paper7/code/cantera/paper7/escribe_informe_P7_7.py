"""[P7-7] Escribe informe_P7_7.md desde P7_7_coge.json, P7_7_recalculo.json, P7_7_F1.json, P7_7_F2.json (+ P7_7_F2_primera_resumen.json),
P7_7_humo.json, P7_7_dia*_resultado.json y P7_7_brazos.json; y el manifiesto de los diarios (fuera de git) P7_7_diarios_manifiesto.md."""
import glob, hashlib, json, os, statistics, collections
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
def J(p):
    f = os.path.join(AQUI, p); return json.load(open(f)) if os.path.exists(f) else None
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
CO = J("P7_7_coge.json") or {}; RC = J("P7_7_recalculo.json") or {}; F1 = J("P7_7_F1.json") or {}; F2 = J("P7_7_F2.json") or {"vidas": [], "resumen": {}}; F2a = (J("P7_7_F2_primera_resumen.json") or {}).get("resumen") or {}
HU = J("P7_7_humo.json") or {"dias": {}}; BR = J("P7_7_brazos.json") or {}
RES = {d: J(f"P7_7_dia{d}_resultado.json") for d in (1, 2, 3)}; costes = {d: (((r or {}).get("episodes") or [{}])[0].get("cost_usd")) for d, r in RES.items()}
cs = [c for c in costes.values() if c]
L = []; w = L.append
w(f"""# P7-7 · Aprender bien estando sano, y la curiosidad que abre camino

*3-oct-2026. Coste: **créditos de la plataforma** {n(sum(cs), 4)} USD en {len(cs)} partidas (por día: {", ".join(f"{d}: {n(c, 4)}" for d, c in costes.items())}); **consola de Anthropic 0 USD**.
`motor/model.py` = `{md5('motor/model.py')}` al empezar y al acabar; los 202 archivos de `CONGELADO.md` y los 32 de `CONGELADO_P6.md` con su md5; el cuerpo
no se toca: todo en archivos `_P7`. Una vida por proceso; la memoria viaja solo en el cuaderno. Los números de método son los de la mesa.*

## Sección 1 · Las cinco decisiones, en el código

**Decisión 1, el recuerdo con techo** (`cuaderno_P7.py`, `descubre_P7.py`). La ventana del uso apunta si la vida tocó su máximo (`mem.hp_max`,
el que el cuerpo lee del mundo) en algún tic entre el uso y el cierre; si lo tocó, el recuerdo se escribe con `al_menos`. En `creencia`, los
recuerdos "al menos" del dominio cuerpo solo entran en la media si su efecto está por encima de la creencia que forman los recuerdos firmes con
el neutro (con ninguno firme, esa creencia es la del neutro, 0: un "al menos" positivo entra). Pueden subirla, nunca bajarla. En recursos y
vínculo, y en la ignorancia, pesan como cualquier recuerdo. La huella (`P7_huella`) lleva `al_menos` y `hp_max`.

**Decisión 2, la curiosidad abre camino** (`descubre_P7.py`, pieza F en el envoltorio de `D.candidatos`). Las ganas de un objeto generan hoy
un candidato `ir_objeto` (decisor_zs.py:458-462): tipo `ir` con `recoger`, cuya imaginación, si llega, pone el objeto en el zurrón
(:805-813). La carencia de ignorancia genera ahora el mismo candidato, `ir_curioso`: destino el botiquín más cercano visto o recordado
(`mem.objetos_vistos`) y no cedido; al llegar, la foto lo tiene en el zurrón y R-CURIOSIDAD pasa a alivio 0,5. Con las mismas dos condiciones
de las ganas de hoy: con el zurrón lleno la cosa no es adquirible (`_promesa`, :650-652) y con la cosa en mi casilla no hay a dónde ir
(`_mejor_objeto` devuelve mi casilla y `ir_objeto` no se crea, :459: de eso se ocupa `coger`). Si `ir_objeto` ya va al mismo sitio, no se
duplica. Ningún número nuevo. Las dos condiciones no estaban en la primera corrida de F2 y se añadieron tras medirla (sección 4).

**Decisión 3, varios objetos en la casilla** (`coge_P7_7.py` → `P7_7_coge.json`). Sobre los 80 diarios de A4 y los 12 de los humos de P7-5 y
P7-6: {n(CO.get('resumen', {}).get('casos'))} cogidas con dos o más clases en la casilla y algo ganado. En las {n(CO.get('resumen', {}).get('posicion', {}).get('primera'))} el mundo entregó **el primero de la lista
de la casilla** (`ve_items`, el mismo orden que ve el cuerpo); no por tipo ({len(CO.get('resumen', {}).get('kind_cogido', {}))} tipos distintos cogidos) ni por cantidad (el de más unidades solo en
{n(CO.get('resumen', {}).get('mas_unidades'))}). Lo soltado cae **al final** de la lista ({n(CO.get('segunda_medida', {}).get('drops_en_casilla_con_varios'))} de {n(CO.get('segunda_medida', {}).get('drops_en_casilla_con_varios'))} sueltas en casilla con varios). Lo que no se puede saber: si el
mundo salta un primero que no cabe y entrega el segundo; en los 92 diarios no hay ni un `pickup` con el primero sin sitio y otro con sitio
({n(CO.get('segunda_medida', {}).get('pickup_sin_ganancia_con_otra_que_cabia'))} casos). Queda apuntado para Ari. La imaginación de `coger` ya usa esa regla (imagina `aqui[0]`, decisor_zs.py:478-482), así
que no se toca; lo que cambia es **hacer sitio**: el candidato se crea solo para el primer objeto de la casilla cuando no cabe (en P7-6 se
creaba para cualquiera, e imaginaba coger lo que el mundo no entrega); como lo soltado cae al final, `coger` al tic siguiente sigue viendo el
mismo primero.

**Decisión 4**: el escalado de `ACOPIO_POR_DOS` por la creencia queda como estaba en P7-6. **Decisión 5**: armas y munición siguen sin
soltarse (el candidato de hacer sitio solo suelta consumibles).

## Sección 2 · El cuaderno del asiento 11 de P7-6, recalculado con el techo

Fuente: `recalcula_P7_7.py` → `P7_7_recalculo.json`, `P7_7_cuaderno_11_recalculado.json`. El único uso (día 3, tic {n((RC.get('huellas') or [{}])[0].get('t0'))}, dentro, vida
{n((RC.get('huellas') or [{}])[0].get('hp0'))} → {n((RC.get('huellas') or [{}])[0].get('hp_fin'))} con máximo {n(RC.get('fuente', {}).get('hp_max_visto_en_el_diario'))}) toca techo: el recuerdo pasa a **"al menos +1"**.

| | creencia cuerpo (dentro) | recursos | vínculo | ignorancia | pesos vividos |
|---|---:|---:|---:|---:|---:|
""")
for k, lab in (("P7_6", "P7-6 (sin techo)"), ("P7_7", "P7-7 (con techo)")):
    c = ((RC.get(k) or {}).get("creencias") or {}).get("first_aid") or {}; dn = c.get("dentro") or {}
    w(f"| {lab} | {n(dn.get('cuerpo'), 4)} | {n(dn.get('recursos'), 4)} | {n(dn.get('vinculo'), 4)} | {n(c.get('ignorancia'), 4)} | {n(c.get('pesos_vividos'), 4)} |\n")
il = RC.get("ilustracion_recuerdo_firme_40") or {}
w(f"""
Queda igual en cifras: con ningún recuerdo firme la creencia es la del neutro (0) y el "al menos +1" está por encima, así que entra como
antes; la ignorancia no cambia porque el techo no toca los pesos. Lo que cambia es lo que pasará cuando llegue un recuerdo firme: con uno de
+40 en la misma situación (hipotético, calculado con el mismo código, no es dato del campo) la creencia del cuerpo sería {n((il.get('con_regla_del_techo') or {}).get('cuerpo'), 2)} con el techo y
{n((il.get('sin_regla_(P7_6)') or {}).get('cuerpo'), 2)} sin él: el "cura 1" de la vida casi llena dejaría de arrastrar la media hacia abajo.

## Sección 3 · F1: con todo apagado y con TECHO, la variante reproduce A4

| brazo | tics iguales | distintos | los distintos |
|---|---:|---:|---|
""")
for b in ("apagado", "TECHO"):
    x = F1.get(b) or {}; f = x.get("fidelidad") or {}
    w(f"| {b} | {n(f.get('igual'))} | {n(f.get('difiere', 0))} | {'; '.join(f"{d['vida'][-14:]} t {d['t']}" for d in x.get('desacuerdos', [])) or '–'} |\n")
w(f"""
Los mismos dos tics de P6-30, P7-5 y P7-6. **F1 pasa.** Fuente: `banco_P7_5.py --f1` (`P7_7_F1.json`).

## Sección 4 · F2: las escenas de los humos de P7-5 y P7-6 al lado de un botiquín

Réplica de los 12 diarios de los dos humos (brazo APRENDE, cuaderno vacío, un subproceso por vida, `banco_P7_7.py`), registrando en cada tic a
dos casillas o menos de un botiquín la elección de la réplica y las d de todos los candidatos. {n(F2['resumen'].get('escenas'))} escenas. El mundo es el del diario:
lo elegido no cambia la partida, pero se ve qué haría.

| situación | tics | ir curioso (candidato presente) | coger | ir al objeto | hacer sitio | quieto | otra |
|---|---:|---:|---:|---:|---:|---:|---:|
""")
ET = {"dist=0,libre=True,lleva=False": "encima, con ranura libre", "dist=0,libre=False,lleva=False": "encima, zurrón lleno", "dist=1,libre=True,lleva=False": "a una casilla, con ranura libre", "dist=1,libre=False,lleva=False": "a una casilla, zurrón lleno",
      "dist=2,libre=True,lleva=False": "a dos casillas, con ranura libre", "dist=2,libre=False,lleva=False": "a dos casillas, zurrón lleno", "dist=2,libre=False,lleva=True": "a dos casillas, ya lleva uno"}
PS = F2["resumen"].get("por_situacion") or {}
for k, lab in ET.items():
    s = PS.get(k)
    if not s: continue
    c = s["clases"]; w(f"| {lab} | {n(s['n'])} | {n(c.get('ir curioso', 0))} ({n(s['con_ir_curioso'])}) | {n(c.get('coger', 0))} | {n(c.get('ir al objeto', 0))} | {n(c.get('hacer sitio', 0))} | {n(c.get('quieto', 0))} | {n(c.get('otra', 0))} |\n")
d1 = PS.get("dist=1,libre=True,lleva=False", {}); d2 = PS.get("dist=2,libre=True,lleva=False", {}); d0 = PS.get("dist=0,libre=True,lleva=False", {})
# las d en la escena de ejemplo (a una casilla, ranura libre, gana ir_curioso)
ej = next((e for v in F2["vidas"] for e in v.get("ejemplos", []) if e["dist"] == 1 and e["ranura_libre"] and e["clase"] == "ir curioso"), None)
P1 = F2a.get("por_situacion") or {}
w(f"""
Lectura. **La curiosidad abre camino**: a una casilla con ranura libre `ir_curioso` gana {n(d1.get('clases', {}).get('ir curioso', 0))} de {n(d1.get('n'))}; a dos, {n(d2.get('clases', {}).get('ir curioso', 0))} de {n(d2.get('n'))}
(en P7-6, al lado del botiquín, casi siempre `noop`). Encima con ranura libre, `coger` {n(d0.get('clases', {}).get('coger', 0))} de {n(d0.get('n'))}. Con el zurrón lleno no existe el
candidato (no es adquirible) y manda `quieto`, como antes. Las d de una escena a una casilla con sitio libre ({ej['t'] if ej else '–'}, {next((v['vida'] for v in F2['vidas'] for e in v.get('ejemplos', []) if e is ej), '–') if ej else '–'}):
{", ".join(f"`{a}` {n(b, 4)}" for a, b in (ej or {}).get('d_mejor', [])[:5])}.

**La primera corrida, sin las dos condiciones, y por qué se añadieron** (`P7_7_F2_primera_resumen.json`). Con `ir_curioso` creado siempre que
no llevaba botiquín: encima de uno con el zurrón lleno ganaba un paseo hacia OTRO botiquín (sin alivio imaginado, porque no cabe) en
{n((P1.get('dist=0,libre=False,lleva=False') or {}).get('clases', {}).get('ir curioso', 0))} de {n((P1.get('dist=0,libre=False,lleva=False') or {}).get('n'))} tics, y encima de uno con ranura libre le quitaba el tic a `coger` en {n((P1.get('dist=0,libre=True,lleva=False') or {}).get('clases', {}).get('ir curioso', 0))} de {n((P1.get('dist=0,libre=True,lleva=False') or {}).get('n'))}
(hacia otro botiquín a dos o tres casillas: la d de moverse con el botiquín imaginado en el zurrón quedaba 0,03 por debajo de la de cogerlo
quieto). Las ganas de hoy no hacen ninguna de las dos cosas (zurrón lleno → promesa 0; cosa en mi casilla → sin `ir_objeto`), así que
`ir_curioso` lleva las mismas dos condiciones. No es un número: es el mismo candidato que generan las ganas.

**Hacer sitio en F2**: elegido {n(sum((v.get('clases') or {}).get('hacer sitio', 0) for v in F2['vidas']))} veces, {{HACER_SITIO}}. Es el cuerpo pesando lo que pierde contra lo que gana (el
camuflaje promete por S-8); se informa.

**Huellas con techo en el banco**: {{HUELLAS_BANCO}}.

## Sección 5 · F3: el humo de tres días (brazo APRENDE, las dos criaturas)

Semillas nuevas, nunca usadas: {", ".join(f"día {d}: {s}" for d, s in sorted({int(k): v['semilla'] for k, v in HU['dias'].items()}.items()))} (las tres siguientes de la sucesión de semillas_S2 tras las de P7-6; sin carpeta en
`paintball/runs` ni mención en el repo). Imágenes: {", ".join(f"día {k[-1]}: {v.get('etiqueta')} ({str(v.get('policy_version_id'))[:8]}…)" for k, v in sorted(BR.items()))}; el cuaderno de cada día viaja horneado al siguiente.

""")
for d, D in sorted(HU["dias"].items(), key=lambda kv: int(kv[0])):
    w(f"**Día {d}** (semilla {D['semilla']}, {D.get('estado')}, coste {n(D.get('coste_usd_plataforma'), 4)} USD de plataforma).\n\n| criatura | vivo · puesto | se acerca: tics `ir_curioso` · llegadas a una casilla (por curiosidad / de paso) | hace sitio (tic, qué suelta por qué) | coge (con sitio / tras hacer sitio; de ellas regaladas al hermano en 10 tics) | usa (tic, situación, vida) | recuerdos (al menos) | cuaderno al acabar: ignorancia; creencia por situación |\n|---|---|---|---|---|---|---|---|\n")
    for s_, c in sorted(D["criaturas"].items()):
        if c.get("sin_diario"): w(f"| {s_} | sin diario | | | | | | |\n"); continue
        ca, cf = c["cuaderno_arranque"], c["cuaderno_fin"]; crf = (cf.get("creencias") or {}).get("first_aid") or {}; ll = c["llegadas_a_una_casilla"]
        hs = "; ".join(f"{x['t']}: {x['elegido'].replace('hacer_sitio_', '').replace('_por_', ' por ')}" for x in c["hace_sitio"][:4]) + (f" (+{len(c['hace_sitio']) - 4})" if len(c["hace_sitio"]) > 4 else "") or "ninguno"
        cg = f"{c['coge_n'] - c['coge_tras_hacer_sitio']} / {c['coge_tras_hacer_sitio']} (regaladas al hermano {c['coge_regaladas']})"
        us = "; ".join(f"{u['t']} {u['situacion']} vida {n(u['hp'])}" for u in c["usa"][:5]) or "ninguno"
        rec = "; ".join(f"{h['situacion']} {'al menos ' if h.get('al_menos') else ''}{h['efecto']['cuerpo']:+.1f} / {h['efecto']['recursos']:+.0f} / {h['efecto']['vinculo']:+.1f} (vida {n(h.get('hp0'))} → {n(h.get('hp_fin'))}){' INTERRUMPIDO, no apuntado' if h.get('interrumpido') else (' INTERRUMPIDO, apuntado (fallo, día ' + str(d) + ')' if h['efecto']['recursos'] == 0 else '')}" for h in c["huellas"][:6]) or "ninguno"
        cre = "; ".join(f"{sit}: cuerpo {n(v.get('cuerpo'), 2)}, recursos {n(v.get('recursos'), 2)}, vínculo {n(v.get('vinculo'), 2)}" for sit, v in crf.items() if isinstance(v, dict) and "cuerpo" in v) or "no sé"
        w(f"| {s_} | {n(c['ticks_vivos'])} · {c['placement']} | {n(c['se_acerca']['tics_ir_curioso'])} · {n(ll['n'])} ({n(ll['por_curiosidad'])} / {n(ll['de_paso'])}) | {hs} | {cg} | {us} | {rec} | {n(cf.get('ignorancia'), 3)}; {cre} |\n")
    w("\n")
w("""{LECTURA}

GIF de los datos del primer uso (`gif_P7_5.py`, local, fuera de git): {GIFS}.

## Sección 6 · F4: créditos del humo

{F4}

## Sección 7 · Lo que queda para la mesa

{ABIERTO}

## Archivos

| archivo | qué es |
|---|---|
| `cuaderno_P7.py`, `descubre_P7.py` | el recuerdo con techo; `ir_curioso`; hacer sitio para el primero de la casilla |
| `coge_P7_7.py`, `P7_7_coge.json` | la medida de qué entrega el mundo con varios objetos en la casilla (decisión 3) |
| `recalcula_P7_7.py`, `P7_7_recalculo.json`, `P7_7_cuaderno_11_recalculado.json` | el cuaderno del asiento 11 de P7-6 con el techo (decisión 1) |
| `banco_P7_5.py --f1`, `P7_7_F1.json`; `banco_P7_7.py`, `P7_7_F2.json`, `P7_7_F2_primera_resumen.json` | F1 y F2 |
| `lanza_P7_7.py`, `Dockerfile.pareja_P7_7`, `P7_7_brazos.json`, `P7_7_dia*_{peticion,resultado,cuaderno_*}.json`, `cuadernos_humo_P7_7/` | el humo |
| `humo_P7_7.py`, `P7_7_humo.json`, `P7_7_diarios_manifiesto.md` | la lectura del humo y el manifiesto de los diarios (fuera de git) |
| `escribe_informe_P7_7.py`, `informe_P7_7.md` | este informe |
""")
# ── piezas que dependen de los datos ──
hs_pairs = collections.Counter()
for v in F2["vidas"]:
    if not v.get("registradas"): continue
    carp, slot = v["vida"].split("/"); fjs = os.path.join(AQUI, "_P7_7_tmp", "F2", f"APRENDE_{carp}_{slot}.json")
    if os.path.exists(fjs):
        for u in json.load(open(fjs))["usos"]:
            el = str(u.get("elegido_replica") or "")
            if el.startswith("hacer_sitio_"): hs_pairs[el.replace("hacer_sitio_", "").replace("_por_", " por ")] += 1
hacer_sitio = ("de ellas " + ", ".join(f"{n(c)} {k}" for k, c in hs_pairs.most_common())) if hs_pairs else "–"
hb = [(v["vida"], h) for v in F2["vidas"] for h in (v.get("huellas") or [])]
huellas_banco = "; ".join(f"{vid[-11:]} tic {n(h['t0'])}: vida {n(h['hp0'])} → {n(h['hp_fin'])}, cuerpo {h['efecto']['cuerpo']:+.0f}{' (al menos)' if h.get('al_menos') else ''}" for vid, h in hb) or "ninguna"
gifs = ", ".join(f"`{os.path.basename(g)}`" for g in sorted(glob.glob(os.path.join(AQUI, "P7_7_dia*_*.gif")))) or "ninguno"
f4 = (f"Créditos de la plataforma: {n(sum(cs), 4)} USD en {len(cs)} partidas enteras (por día {', '.join(n(c, 4) for c in cs)}; media {n(statistics.mean(cs), 4)}). Tres subidas de imagen (v7-v9 de `gemv-p7-aprende`), sin créditos. Consola de Anthropic: 0." if cs else "sin partidas")
lectura = open(os.path.join(AQUI, "_P7_7_tmp", "lectura.md")).read().strip() if os.path.exists(os.path.join(AQUI, "_P7_7_tmp", "lectura.md")) else "(lectura pendiente)"
abierto = open(os.path.join(AQUI, "_P7_7_tmp", "abierto.md")).read().strip() if os.path.exists(os.path.join(AQUI, "_P7_7_tmp", "abierto.md")) else "(pendiente)"
txt = "".join(L).replace("{HACER_SITIO}", hacer_sitio).replace("{HUELLAS_BANCO}", huellas_banco).replace("{LECTURA}", lectura).replace("{GIFS}", gifs).replace("{F4}", f4).replace("{ABIERTO}", abierto); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_7.md"), "w").write(txt); print("informe escrito", len(txt))
# manifiesto de los diarios
M = ["# P7-7 · diarios del humo (fuera de git; md5)", "", "| archivo | bytes | md5 |", "|---|---:|---|"]
for D in HU["dias"].values():
    for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P77_humo_APRENDE_{D['semilla']}", "*.art.log"))):
        M.append(f"| `{os.path.relpath(f, RAIZ)}` | {os.path.getsize(f)} | `{hashlib.md5(open(f, 'rb').read()).hexdigest()}` |")
open(os.path.join(AQUI, "P7_7_diarios_manifiesto.md"), "w").write("\n".join(M) + "\n")
