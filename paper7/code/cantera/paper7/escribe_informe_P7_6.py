"""[P7-6] Escribe informe_P7_6.md desde P7_6_F1.json, P7_6_F2.json, P7_6_humo.json, P7_6_dia*_resultado.json y P7_6_brazos.json."""
import glob, hashlib, json, os, statistics, collections
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
def J(p):
    f = os.path.join(AQUI, p); return json.load(open(f)) if os.path.exists(f) else None
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
F1 = J("P7_6_F1.json") or {}; F2 = J("P7_6_F2.json") or {"vidas": [], "resumen": {}}; HU = J("P7_6_humo.json") or {"dias": {}}; BR = J("P7_6_brazos.json") or {}
RES = {d: J(f"P7_6_dia{d}_resultado.json") for d in (1, 2, 3)}; costes = {d: (((r or {}).get("episodes") or [{}])[0].get("cost_usd")) for d, r in RES.items()}
L = []; w = L.append
w(f"""# P7-6 · La curiosidad hecha de ignorancia, y poder hacer sitio

*3-oct-2026. Coste: **créditos de la plataforma** {n(sum(c for c in costes.values() if c), 4)} USD en {sum(1 for c in costes.values() if c)} partidas (por día: {", ".join(f"{d}: {n(c, 4)}" for d, c in costes.items())}); **consola de Anthropic 0 USD**.
`motor/model.py` = `{md5('motor/model.py')}` al empezar y al acabar; congelados y cuerpo sin tocar: todo en archivos `_P7`. Una vida por
proceso; la memoria viaja solo en el cuaderno. Los números de método son los de la mesa; cuando uno no funciona se informa, no se cambia.*

## Sección 1 · Los dos cambios, en el código

**Cambio 1, la curiosidad como carencia de conocimiento** (`cuaderno_P7.py`, `descubre_P7.py`). Ignorancia de una clase = peso del neutro /
(peso del neutro + suma de los pesos de los recuerdos vividos de esa clase en todas sus situaciones, vistos desde el día actual):
`Cuaderno.ignorancia`; nunca probado 1, recién probado baja, con días sin vivirlo sube despacio porque los vividos se apagan con 0,95 y el
neutro no. Desaparecen la cuenta de usos, la forma de la novedad de P7-5 y la pendiente topada tras aquel humo. La fila **R-CURIOSIDAD**
es una carencia como las demás: negativa, reparto como R-ACOPIO (0,1, 0,8, 0,1), M = 0,18 × calma × ignorancia × alivio, con calma = 1 − máx
(alcance, agresor, hermano amenaza, hermano golpe, anticipación del fuego) y alivio = 1 sin la cosa (estar al lado no alivia nada), 0,5 con
la cosa en el zurrón, 0 en la foto que la usa. Entra en el envoltorio de `A.filas` y en `A.REPARTO` desde fuera; la promesa de ir a por la
cosa (`D._promesa`) suma M × 0,5, lo que alivia tenerla.

**Cambio 2, hacer sitio** (`descubre_P7.py`, pieza E). Candidato compuesto `hacer_sitio_<suelta>_por_<coge>`, creado en el envoltorio de
`D.candidatos` cuando hay un objeto en mi casilla que `coger` no puede tomar (zurrón lleno y sin pila donde apilarlo) y llevo un consumible de
otra clase. Es un `soltar` del decisor (ranura fuera, el objeto al suelo, acción `drop`) cuya receta lleva en `item` el marcador
`suelta|coge`; el envoltorio de `D._obs_prevista` lo reconoce y pone además en la foto el objeto cogido en el zurrón: lo que se pierde
contra lo que se gana, en la misma imaginación. Al elegirlo se borra la cesión que `decide` apunta en `mem.cedidos` (decisor_zs.py:902-903),
para que `coger` pueda tomar el objeto al tic siguiente. Interruptor `GEMV_P7_SITIO`, igual en los cuatro brazos, apagado en F1.

**Un ajuste de la pieza C, encontrado en F2 y declarado.** Las ganas del botiquín son toda la fila R-ACOPIO, también su rama "con una sola
no basta" (`ACOPIO_POR_DOS`, appraisal:221, :951-953), que P7-5 no escalaba por la creencia. Sin escalarla, al coger el primer botiquín
aparecía un acopio de 0,10 que pesaba más que el alivio de la curiosidad (0,09) y `coger` perdía con el zurrón libre (F2, primera corrida:
145 de 773 veces encima con sitio). Escalada por k, como el resto de las ganas, `coger` gana 619 de 773. No se tocó ningún número de la mesa.

## Sección 2 · F1: con todo apagado y con TECHO, la variante reproduce A4

| brazo | tics iguales | distintos | los distintos |
|---|---:|---:|---|
""")
for b in ("apagado", "TECHO"):
    x = F1.get(b) or {}; f = x.get("fidelidad") or {}
    w(f"| {b} (hacer sitio apagado) | {n(f.get('igual'))} | {n(f.get('difiere', 0))} | {'; '.join(f"{d['vida'][-14:]} t {d['t']}" for d in x.get('desacuerdos', [])) or '–'} |\n")
w(f"""
Los mismos dos tics de P6-30 y P7-5. **F1 pasa.** Fuente: `banco_P7_5.py --f1` (`P7_6_F1.json`).

## Sección 3 · F2: las escenas del humo de P7-5 en que el cuerpo se quedó al lado de un botiquín

Réplica de los seis diarios del humo de P7-5 con los dos cambios (brazo APRENDE, cuaderno vacío, un subproceso por vida, `banco_P7_6.py`),
registrando en cada tic a una casilla o menos de un botiquín la elección de la réplica y las d de sus candidatos. El mundo es el del diario:
lo elegido no cambia la partida, pero se ve qué haría. {n(F2['resumen'].get('escenas'))} escenas:

| situación | coger | hacer sitio (y qué suelta) | ir al objeto | otra |
|---|---:|---:|---:|---:|
""")
tot = collections.defaultdict(collections.Counter)
for v in F2["vidas"]:
    for k, c in v["por_situacion"].items(): tot[k].update(c)
ET = {"encima=True,libre=True": "encima del botiquín, con ranura libre", "encima=True,libre=False": "encima, zurrón lleno", "encima=False,libre=True": "al lado (una casilla), con ranura libre", "encima=False,libre=False": "al lado, zurrón lleno"}
for k in ("encima=True,libre=True", "encima=True,libre=False", "encima=False,libre=True", "encima=False,libre=False"):
    c = tot.get(k, {}); w(f"| {ET[k]} | {n(c.get('coger', 0))} | {n(c.get('hacer sitio', 0))}{(' (suelta ' + ', '.join(f'{a} {b}' for a, b in F2['resumen'].get('suelta', {}).items()) + ')') if c.get('hacer sitio') else ''} | {n(c.get('ir al objeto', 0))} | {n(c.get('otra', 0))} |\n")
sit_cand = sum(v["con_candidato_hacer_sitio"] for v in F2["vidas"]); sit_el = sum(v["clases"].get("hacer sitio", 0) for v in F2["vidas"])
w(f"""
Lectura. Encima con ranura libre, `coger` gana {n(tot['encima=True,libre=True'].get('coger', 0))} de {n(sum(tot['encima=True,libre=True'].values()))}. Encima con el zurrón lleno, el candidato de hacer sitio
existió en {sit_cand} tics (solo cuando lleva un consumible de otra clase: en el resto el zurrón va de armas y munición, que por diseño no se sueltan) y ganó
en {sit_el}, soltando raciones. Al lado del botiquín la curiosidad no mueve por sí sola (estar al lado no alivia nada): `ir al objeto` gana en
{n(tot['encima=False,libre=True'].get('ir al objeto', 0) + tot['encima=False,libre=False'].get('ir al objeto', 0))} tics y el resto son `noop` o pasos de otras filas. Fuente: `P7_6_F2.json`.

## Sección 4 · F3: el humo de tres días (brazo APRENDE, las dos criaturas)

Semillas nuevas, nunca usadas: {", ".join(f"día {d}: {s}" for d, s in sorted({int(k): v['semilla'] for k, v in HU['dias'].items()}.items()))} (las tres siguientes de la sucesión de semillas_S2 tras las de P7-5).
Imágenes: {", ".join(f"día {k[-1]}: {v.get('etiqueta')} ({str(v.get('policy_version_id'))[:8]}…)" for k, v in sorted(BR.items()))}; el cuaderno de cada día viaja horneado al siguiente (el registro de fin ya va antes de la subida).

""")
for d, D in sorted(HU["dias"].items(), key=lambda kv: int(kv[0])):
    w(f"**Día {d}** (semilla {D['semilla']}, {D.get('estado')}, coste {n(D.get('coste_usd_plataforma'), 4)} USD de plataforma).\n\n| criatura | vivo · puesto | se acerca (tics con curiosidad > 0 y elección hacia un objeto) | hace sitio (tic, qué suelta) | coge (con sitio libre / tras hacer sitio) | usa (tic, situación, imaginó) | cuaderno leído | cuaderno al acabar: recuerdos, ignorancia, creencias |\n|---|---|---:|---|---|---|---|---|\n")
    for s_, c in sorted(D["criaturas"].items()):
        if c.get("sin_diario"): w(f"| {s_} | sin diario | | | | | | |\n"); continue
        ca, cf = c["cuaderno_arranque"], c["cuaderno_fin"]; crf = (cf.get("creencias") or {}).get("first_aid") or {}
        hs = "; ".join(f"{x['t']}: {x['elegido'].replace('hacer_sitio_', '').replace('_por_', ' por ')}" for x in c["hace_sitio"][:4]) or "ninguno"
        cg = f"{sum(1 for x in c['coge'] if not x['tras_hacer_sitio'])} / {sum(1 for x in c['coge'] if x['tras_hacer_sitio'])}"
        us = "; ".join(f"{u['t']} {u['situacion']} {n(u['heal_imaginado'], 1) if u['heal_imaginado'] is not None else 'no sé'}" for u in c["usa"][:5]) or "ninguno"
        cre = "; ".join(f"{sit}: cuerpo {n(v.get('cuerpo'), 1)}, recursos {n(v.get('recursos'), 2)}, vínculo {n(v.get('vinculo'), 2)}" for sit, v in crf.items() if isinstance(v, dict) and "cuerpo" in v) or "–"
        w(f"| {s_} | {n(c['ticks_vivos'])} · {c['placement']} | {c['se_acerca_por_novedad']['n']} | {hs} | {cg} | {us} | {'sí' if ca.get('leido') else 'no'} (día {ca.get('dia')}) | {cf.get('n_recuerdos')}, {n(cf.get('ignorancia'), 3)}, {cre} |\n")
    w("\n")
w("""{LECTURA}

GIF de los datos del primer uso (`gif_P7_5.py`, local, fuera de git): {GIFS}.

## Sección 5 · F4: créditos del humo

{F4}

## Sección 6 · Lo que queda para la mesa

{ABIERTO}

## Archivos

| archivo | qué es |
|---|---|
| `cuaderno_P7.py`, `descubre_P7.py` | la ignorancia y la curiosidad; hacer sitio; el escalado de `ACOPIO_POR_DOS` |
| `banco_P7_5.py --f1`, `P7_6_F1.json`; `banco_P7_6.py`, `P7_6_F2.json` | F1 y F2 |
| `lanza_P7_6.py`, `Dockerfile.pareja_P7_6`, `P7_6_brazos.json`, `P7_6_dia*_{peticion,resultado,cuaderno_*}.json`, `cuadernos_humo_P7_6/` | el humo |
| `humo_P7_6.py`, `P7_6_humo.json`, `P7_6_diarios_manifiesto.md` | la lectura del humo y el manifiesto de los diarios (fuera de git) |
| `escribe_informe_P7_6.py`, `informe_P7_6.md` | este informe |
""")
# ── diagnostico por dia y criatura: encima del botiquin, zurron, candidato hacer_sitio ──
import glob as _g, math as _m
diag = []
for d, D in sorted(HU["dias"].items(), key=lambda kv: int(kv[0])):
    for s_ in (10, 11):
        fs = _g.glob(os.path.join(RAIZ, "paintball", "runs", f"P76_humo_APRENDE_{D['semilla']}", f"*policy_agent_{s_}.art.log"))
        if not fs: continue
        enc = 0; enc_libre = 0; enc_cons = 0; sitio_c = 0; sitio_e = 0; cog_e = 0; packs = collections.Counter()
        for line in open(fs[0]):
            if '"k":"tick"' not in line and '"k": "tick"' not in line: continue
            r = json.loads(line)
            if r.get("phase") != "live": continue
            ks = [tuple(i["pos"]) for i in (r.get("ve_items") or []) if i.get("id") == "first_aid"]
            if not ks or min(max(abs(r["pos"][0] - k[0]), abs(r["pos"][1] - k[1])) for k in ks) > 0: continue
            enc += 1; ra = r.get("RADIOGRAFIA") or {}; cds = ra.get("candidatos") or {}; ids = [(x or {}).get("id") for x in r["pack"]]
            if any(x is None for x in r["pack"]): enc_libre += 1
            elif any(i_ in ("rations", "first_aid") for i_ in ids): enc_cons += 1
            packs[str(ids)] += 1
            if any(k.startswith("hacer_sitio") for k in cds): sitio_c += 1
            if str(ra.get("elegido")).startswith("hacer_sitio"): sitio_e += 1
            if ra.get("elegido") == "coger": cog_e += 1
        diag.append((int(d), s_, enc, enc_libre, enc_cons, sitio_c, sitio_e, cog_e, packs.most_common(1)))
coges = sum(len(c["coge"]) for D in HU["dias"].values() for c in D["criaturas"].values() if not c.get("sin_diario"))
usos_h = [(int(d), s_, u) for d, D in HU["dias"].items() for s_, c in D["criaturas"].items() if not c.get("sin_diario") for u in c["usa"]]
hu_h = [(int(d), s_, h) for d, D in HU["dias"].items() for s_, c in D["criaturas"].items() if not c.get("sin_diario") for h in c["huellas"]]
lectura = ("**Lectura del humo.** Tics encima de un botiquín, por día y asiento (con ranura libre / zurrón lleno con un consumible que soltar / candidato de hacer sitio presente / elegido hacer sitio / elegido coger; zurrón más frecuente): "
    + "; ".join(f"día {d} asiento {s_}: {n(e)} ({n(l)} / {n(c)} / {n(sc)} / {n(se)} / {n(ce)}; {p[0][0] if p else '–'})" for d, s_, e, l, c, sc, se, ce, p in diag) + ". "
    + f"Cogidas en los tres días: {coges}. " + (("Usos: " + "; ".join(f"día {d} asiento {s_}, tic {n(u['t'])}, {u['situacion']}, vida {u.get('hp', '–')}, imaginó {n(u['heal_imaginado'], 1) if u['heal_imaginado'] is not None else 'no sé'}, ignorancia antes {n(u.get('ignorancia'), 3)}" for d, s_, u in usos_h) + ". Huellas: " + "; ".join(f"cuerpo {h['efecto']['cuerpo']:+.1f} (la vida ya estaba casi llena), recursos {h['efecto']['recursos']:+.0f}, vínculo {h['efecto']['vinculo']:+.1f}, intensidad {h['intensidad']}" for d, s_, h in hu_h) + "; tras ese uso la ignorancia del botiquín pasa de 1 a " + n(next((c['cuaderno_fin']['ignorancia'] for D in HU['dias'].values() for c in D['criaturas'].values() if not c.get('sin_diario') and c['cuaderno_fin'].get('ignorancia')), None), 3) + " (peso vivido " + n(next((c['cuaderno_fin']['pesos_vividos'] for D in HU['dias'].values() for c in D['criaturas'].values() if not c.get('sin_diario') and c['cuaderno_fin'].get('pesos_vividos')), None), 3) + " contra el neutro 1). ") if usos_h else "Ningún uso en los tres días. ")
    + "**Un fallo de fontanería encontrado en el día 1 y corregido para el día 3, declarado.** El candidato de hacer sitio se creaba solo para el primer objeto de la casilla (`aqui[0]`, el mismo que mira `coger`, decisor_zs.py:478-482); en la cámara los botiquines comparten casilla con pilas de munición que sí caben, así que el día 1 el asiento 11 pasó 97 tics encima de un botiquín con raciones en el zurrón y el candidato no existió; igual el día 2 (asiento 11, 129 tics con raciones y arco). Desde el día 3 el candidato se crea para cada objeto de la casilla que no cabe. En banco, sobre el diario del día 1 (asiento 11, tics 12.500-12.640), con la corrección el candidato aparece en 11 tics y gana en 8. Los días 1 y 2 jugaron sin él. "
    + "El día 3, con la corrección: el asiento 11 cogió botiquines con el zurrón libre (5 cogidas, encima con ranura libre `coger` ganó 5 de 121 tics) y usó uno; el asiento 10 estuvo 22 tics encima de uno con el zurrón lleno llevando raciones, el candidato de hacer sitio existió los 22 y perdió los 22: soltar la ración cuesta más (su valor en W, carencia) de lo que alivia conocer el botiquín (0,09), tal como lo pesa la mesa; se informa, no se cambia. La curiosidad sí acerca (cientos de elecciones hacia un objeto con la fila encendida) y las criaturas pasan miles de tics a una casilla de un botiquín, casi siempre con el zurrón lleno de armas y munición, que por diseño no se sueltan: ahí no hay sitio que hacer.")
gifs = ", ".join(f"`{os.path.basename(g)}`" for g in sorted(_g.glob(os.path.join(AQUI, "P7_6_dia*_*.gif")))) or "ninguno (no hubo uso: se dibujó el primer acercamiento)"
cs = [c for c in costes.values() if c]
f4 = (f"Créditos de la plataforma: {n(sum(cs), 4)} USD en {len(cs)} partidas enteras (por día {', '.join(n(c, 4) for c in cs)}; media {n(statistics.mean(cs), 4)}). Seis subidas de imagen (v1-v6 de `gemv-p7-aprende`, tres de P7-5 y tres de P7-6), sin créditos. Consola de Anthropic: 0." if cs else "sin partidas")
abierto = """1. El zurrón: la curiosidad y hacer sitio solo pueden actuar cuando lleva un consumible que soltar; con armas y munición en las dos ranuras (lo
   más frecuente en la cámara) no hay sitio que hacer. Si se quiere que la curiosidad pueda probar lo nuevo, hace falta decidir si se
   suelta también munición o un arma sobrante (decisión de diseño).
2. "Estar al lado no alivia nada" deja el último paso en manos de la promesa de `ir_objeto` (M × 0,5); en F2 gana pocas veces frente a
   `noop` al lado del botiquín. Es lo que fija el diseño; se informa.
3. Qué objeto toma `pickup` cuando hay varios en la casilla lo decide el mundo (pregunta para Ari): hacer sitio suelta uno y pide coger,
   pero no elige cuál se recoge.
4. El escalado de `ACOPIO_POR_DOS` por la creencia (sección 1) es una lectura de la pieza C ("las ganas... salen de la creencia"), no un
   número nuevo; queda a la mesa confirmarla."""
txt = "".join(L).replace("{LECTURA}", lectura).replace("{GIFS}", gifs).replace("{F4}", f4).replace("{ABIERTO}", abierto); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_6.md"), "w").write(txt); print("informe escrito", len(txt))
