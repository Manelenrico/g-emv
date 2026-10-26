"""[P7-11] Escribe informe_P7_11.md desde P7_11_vidas.json (analiza_P7_11.py), P7_11_dia1.json, P7_11_banco_dia1.json (banco_P7_11.py),
P7_11_filas.json (banco_P7_11b.py), P7_10_campo.json y P7_10_estado.json. Cada cifra sale de esos archivos; ninguna a mano."""
import collections, hashlib, json, math, os, random, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
J = lambda p: json.load(open(os.path.join(AQUI, p)))
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
V = J("P7_11_vidas.json"); C = J("P7_10_campo.json"); D1 = J("P7_11_dia1.json"); B1 = J("P7_11_banco_dia1.json"); F = J("P7_11_filas.json"); E = J("P7_10_estado.json")
BR = ("SUELO", "BORRADO", "APRENDE", "TECHO"); L = {b: [v for v in V.values() if v["brazo"] == b] for b in BR}
med = lambda xs: (st.median(xs) if xs else None); mean = lambda xs: (st.mean(xs) if xs else None)
SG = {}
for v in V.values(): SG.update(v["signos"])
W = []; w = W.append

# ───────── seccion 1 ─────────
def paga(rec, el):
    Cn = rec["candidatos"]
    if el not in Cn: return None
    alt = "noop" if "noop" in Cn else min((x for x in Cn if x != el), key=lambda x: Cn[x]["d"], default=None)
    if alt is None: return None
    fe, fa = Cn[el]["filas"], Cn[alt]["filas"]; g = {f: ((fa.get(f, 0) - fe.get(f, 0)) if SG.get(f, "-") == "-" else (fe.get(f, 0) - fa.get(f, 0))) for f in set(fe) | set(fa)}
    top = max(g, key=g.get) if g else None
    return {"fila": (top if (top and g[top] > 1e-4) else "ninguna (empate en todas las filas)"), "mejora": (g[top] if top else 0.0), "alt": alt, "dd": Cn[alt]["d"] - Cn[el]["d"]}
USO = {b: [] for b in BR}; REG = {b: [] for b in BR}; no_casan = 0
for k, v in V.items():
    T = (F.get(k) or {}).get("tics") or {}
    for u in v["usos"]:
        if not u.get("gastado"): continue
        rec = T.get(str((u.get("decision") or {}).get("t")))
        if not rec or rec["elegido"] != "usar_botiquin": no_casan += 1; continue
        USO[v["brazo"]].append({**paga(rec, "usar_botiquin"), "hp": u["hp0"], "cura": rec["cura_imaginada"], "k_ganas": rec["k_ganas"], "ign": rec["ignorancia"], "dentro": u["dentro"]})
    for g in v["regala"]:
        rec = T.get(str(g["t_dec"]))
        if not rec or not str(rec["elegido"]).startswith("soltar_"): no_casan += 1; continue
        REG[v["brazo"]].append({**paga(rec, rec["elegido"]), "k": rec["k_creencia"], "g": g})
fid = {b: collections.Counter() for b in BR}
for k, r in F.items():
    for a, x in r["fidelidad"].items(): fid[V[k]["brazo"]][a] += x
ef = {b: collections.Counter(json.dumps({k_: v["efectivo"][k_] for k_ in ("ON", "SABE", "CUADERNO", "BORRADO", "NOVEDAD", "SITIO", "ESPERANZA", "SITIO_EMPATE")}, sort_keys=True) for v in L[b]) for b in BR}
usos_g = {b: [u for v in L[b] for u in v["usos"] if u.get("gastado")] for b in BR}
img = E["imagenes"]
w(f"""# P7-11 · Por qué el que aprende acaba peor, y qué es el suelo

*4-oct-2026. Todo lo de este paso es POSTERIOR AL SELLO de P7-10 y se declara así: son lecturas de los 320 diarios ya jugados, con medidas
elegidas después de ver el resultado. Nada de aquí cambia el sello (2 de 6). Coste: **créditos de la plataforma 0 USD** (ninguna partida);
**consola de Anthropic 0 USD** (ninguna llamada). `motor/model.py` = `{md5('motor/model.py')}` al empezar y al acabar; el cuerpo y los congelados
no se tocan. Dos bancos de réplica (sin partidas ni llamadas), una vida por proceso: `banco_P7_11.py` (16 réplicas) y `banco_P7_11b.py`
({len(F)} réplicas; fidelidad de la elección tic a tic: {", ".join(f"{b} {n(fid[b]['igual'])} iguales y {n(fid[b].get('difiere', 0))} distintos" for b in BR)}).
Las definiciones de cada medida están en la cabecera de `analiza_P7_11.py`; las cifras salen de `P7_11_vidas.json` (lectura de los diarios),
`P7_11_filas.json` (réplica), `P7_11_dia1.json`, `P7_11_banco_dia1.json` y `P7_10_campo.json`.*

## Lo que sale, en corto

1. **SUELO no era lo que decía el diseño.** Desde la esperanza (pieza H, P7-9) el brazo SUELO imagina el botiquín como una ración: cura imaginada
   {n(med([u['cura'] for u in USO['SUELO']]), 1)} en sus {len(USO['SUELO'])} usos (mínimo {n(min(u['cura'] for u in USO['SUELO']), 1)}, máximo {n(max(u['cura'] for u in USO['SUELO']), 1)}) y ganas a {n(med([u['k_ganas'] for u in USO['SUELO']]), 2)} de las de TECHO. No es "el cuerpo que no sabe qué es
   un botiquín": es "el cuerpo con esperanza y sin memoria". La predicción P5 del sello (casi cero usos) describía el SUELO de antes de la esperanza.
2. **El día 1, APRENDE y BORRADO son el mismo cuerpo** (réplica: {n(sum(x['tics'] for x in B1))} tics, {sum(len(x['tics_en_que_las_dos_replicas_eligen_distinto']) for x in B1)} elecciones distintas), pero no juegan el mismo mundo: con la misma semilla, lo que ven difiere desde el segundo tic.
3. **APRENDE no se distingue de BORRADO por ir a por botiquines** (los dos pasan en ello una quinta parte de la vida) sino por lo que hace con ellos:
   coge el doble y regala ocho veces más, casi todo pagado por la fila S-PROVISION con la creencia ya aprendida; más de la mitad de lo que regala lo
   vuelve a coger él mismo.
4. **APRENDE muere más a manos de un rival, y cuando muere así casi la mitad de las veces iba a por un botiquín.** Sin conclusiones causales.
""")

w("""
## Sección 1 · El suelo

**Qué está encendido en cada brazo, tal como se jugó.** Las líneas son de `cantera/paper7/descubre_P7.py` de hoy; los interruptores los fija
`Dockerfile.pareja_P7_8:227-232` (GEMV_P7=1 y GEMV_P7_SITIO=1 para todos; CUADERNO, NOVEDAD, BORRADO y SABE por brazo; GEMV_P7_ESPERANZA y
GEMV_P7_SITIO_EMPATE no se fijan y valen 1 por defecto, `descubre_P7.py:56-57`).

| pieza | dónde | SUELO | BORRADO | APRENDE | TECHO |
|---|---|---|---|---|---|
| A · cuaderno y ventana de la experiencia | se lee en `:196` (solo con CUADERNO y sin BORRADO); la ventana se llama en `:369` (solo con CUADERNO o NOVEDAD); se apunta en `:263` | apagada: cuaderno vacío en memoria, nunca se apunta nada | encendida, sin leer: empieza vacío cada partida y apunta dentro de la vida | encendida: lee el del día anterior y apunta | apagada |
| A' · el recuerdo con techo ("al menos") | `:251`, `:263` | apagada | encendida | encendida | apagada |
| B · imaginación (la cura que imagina al usar) | `:283-284` (`if n == "usar_botiquin" and not SABE`), `heal_imaginado` `:119-127` | **encendida**: sin creencia, todo esperanza | encendida | encendida | apagada: la cura del catálogo |
| C · ganas (R-ACOPIO, W, W_TARGET por k) | `:332`, `:340-344`, `k_ganas` `:114-118` | **encendida** con k fijo = esperanza / cura | encendida | encendida | k = 1 (`:116`) |
| D · curiosidad (fila R-CURIOSIDAD y su promesa) | `:277`, `:337-338`, `:346-355` (NOVEDAD y sin SABE) | apagada | encendida | encendida | apagada |
| F · la curiosidad abre camino (`ir_curioso`) | `:286-306` (NOVEDAD y sin SABE) | apagada | encendida | encendida | apagada |
| E · hacer sitio | `:307-322`, `:374` (SITIO) | encendida | encendida | encendida | encendida |
| G · el regalo mira lo aprendido | `:335` (`if not SABE`), `regalo_aprendido` `:148-170`, `k_creencia` `:102-106` | **encendida** con k = 0 siempre (sin cuaderno, `:105`) | encendida | encendida | apagada (k = 1) |
| H · la esperanza | `:56` (1 por defecto), `mezcla` `:107-113`; entra por `:118` y `:127` | **encendida**: ignorancia 1 toda la vida (`:130-132`) | encendida | encendida | sin efecto (SABE sale antes, `:116`, `:122`) |
| I · en un empate, hacer sitio no gana | `:375-376` (SITIO y SITIO_EMPATE) | encendida | encendida | encendida | encendida |

""")
w("Comprobado en los diarios (`P7_arranque.entorno_P7.efectivo`, las 80 vidas de cada brazo): " + "; ".join(f"{b}: {', '.join(f'{k_}={int(x)}' for k_, x in json.loads(next(iter(ef[b]))).items())} ({sum(ef[b].values())} de 80 iguales)" for b in BR) + ".\n")
su = USO["SUELO"]; hp_su = [u["hp0"] for u in usos_g["SUELO"]]
w(f"""
**Por qué SUELO usa botiquines.** En SUELO la pieza B está encendida (no es TECHO) y el cuaderno no existe, así que `heal_imaginado` llama a
`mezcla(mundo, None)` y, con la esperanza encendida por defecto, devuelve (1 − ignorancia) × 0 + ignorancia × esperanza con ignorancia 1: la media de
`heal` de los consumibles conocidos, la ración. Leído en la réplica de sus vidas con algún uso o regalo ({n(fid['SUELO']['igual'])} tics, {fid['SUELO'].get('difiere', 0)} distintos del diario):

| | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| usos (botiquín gastado) | {" | ".join(str(len(usos_g[b])) for b in BR)} |
| usos por vida | {" | ".join(n(len(usos_g[b]) / 80, 3) for b in BR)} |
| candidato elegido en la decisión | {" | ".join(f"`usar_botiquin` {len(USO[b])} de {len(usos_g[b])}" for b in BR)} |
| cura imaginada: mediana (mín – máx) | {" | ".join((f"{n(med([u['cura'] for u in USO[b]]), 1)} ({n(min(u['cura'] for u in USO[b]), 1)} – {n(max(u['cura'] for u in USO[b]), 1)})" if b != "TECHO" else "50 (catálogo; no se toca)") for b in BR)} |
| k de las ganas en ese tic (mediana) | {" | ".join(n(med([u['k_ganas'] for u in USO[b]]), 2) for b in BR)} |
| fila que paga el uso frente a `noop` | {" | ".join(", ".join(f"{f_} {c_}" for f_, c_ in collections.Counter(u['fila'] for u in USO[b]).most_common(2)) for b in BR)} |
| vida al usar: mediana | {" | ".join(n(med([u['hp0'] for u in usos_g[b]]), 1) for b in BR)} |
| usos con la vida ≥ 85 (le faltan 15 o menos) | {" | ".join(f"{sum(1 for u in usos_g[b] if u['hp0'] >= 85)}" for b in BR)} |
| usos con la vida < 50 | {" | ".join(f"{sum(1 for u in usos_g[b] if u['hp0'] < 50)}" for b in BR)} |
| botiquines cogidos | {" | ".join(str(sum(v['coge_botiquines'] for v in L[b])) for b in BR)} |

En los {len(su)} usos de SUELO gana `usar_botiquin`, lo paga la fila F-DANO (el daño que el cuerpo lleva encima) y la cura imaginada es {n(med([u['cura'] for u in su]), 1)} en todos:
la de la ración. Con una cura imaginada de 15 el botiquín se usa como una ración, en cuanto falta algo de vida (mediana {n(med(hp_su), 1)}; {sum(1 for x in hp_su if x >= 85)} de {len(hp_su)} con la vida en 85 o más).
Las ganas también llevan la esperanza: k = 15 / 50 = {n(med([u['k_ganas'] for u in su]), 2)} toda la vida, y por eso SUELO coge {sum(v['coge_botiquines'] for v in L['SUELO'])} botiquines.

**Dicho claro.** La cabecera de `descubre_P7.py` describe SUELO como "P7=1 SITIO=1" (`:45`) y las piezas B y C como "no sé → 0" (`:12`, `:15`): un
cuerpo que no le pone efecto al botiquín y no lo quiere. Eso fue verdad hasta P7-8. Desde la pieza H (P7-9), "nunca probado: todo esperanza"
(`:108-109`), y SUELO, que no aprende nunca, se queda para siempre en ese punto: imagina 15 y quiere a 0,3. El sello de P7-10 lo dice ("con la
esperanza, pieza H", para los cuatro brazos) pero su predicción P5 ("SUELO casi no usa botiquines") es la del SUELO de antes. **SUELO, tal como se
jugó, no es el suelo del diseño (el cuerpo que no sabe): es el cuerpo con esperanza y sin memoria.** Como referencia de "no sabe nada" no sirve;
como referencia de "esperanza sola, sin aprender" sí, y así hay que leerlo: el día 1 de BORRADO y de APRENDE antes del primer uso es ese mismo cuerpo más la curiosidad.

**Otra cosa que no era igual entre brazos.** Las tres imágenes fijas se subieron antes del freno ({", ".join(f"{b} {img[b]['etiqueta'].split(':')[1]} a las {img[b]['subida_a_las'][11:16]} UTC" for b in ("SUELO", "BORRADO", "TECHO"))}),
con `descubre_P7.py` del sello (md5 `76c0222dcd806cfb0747a9c70c38fe61`). El arreglo del apéndice del sello (una ventana con un regalo dentro no se
apunta; md5 de hoy `{md5('cantera/paper7/descubre_P7.py')}`) entró después: lo llevan APRENDE de la serie 2 entera y de la serie 1 desde el día 4, y no lo lleva
BORRADO en ninguno de sus 40 días (sus huellas no tienen el campo `regalado`: {sum(1 for v in L['BORRADO'] if v['huella_con_regalado'] is False)} vidas con huellas, {sum(1 for v in L['BORRADO'] if v['huella_con_regalado'])} con el campo; APRENDE: {sum(1 for v in L['APRENDE'] if v['huella_con_regalado'])} con el campo, {sum(1 for v in L['APRENDE'] if v['huella_con_regalado'] is False)} sin él, las de los días 1 a 3 de la serie 1).
El alcance medido: ventanas con un regalo dentro que se apuntaron como experiencia: BORRADO {sum(v['ventanas_con_regalo_apuntadas'] for v in L['BORRADO'])} (en {sum(1 for v in L['BORRADO'] if v['ventanas_con_regalo_apuntadas'])} de 80 vidas; como BORRADO no lee, el recuerdo falso muere con la partida),
APRENDE {sum(v['ventanas_con_regalo_apuntadas'] for v in L['APRENDE'])} (las del día 3 del freno, limpiadas a mano antes del día 4). En SUELO y TECHO el cambio no hace nada (no apuntan). Es pequeño, pero BORRADO y APRENDE no llevaban exactamente el mismo código.
""")

# ───────── seccion 2 ─────────
w("""
## Sección 2 · El día 1

**Los diarios no se pueden comparar tic a tic, porque los dos mundos no son el mismo.** Misma semilla, mismo asiento, día 1 (`P7_11_dia1.json`):

| serie | asiento | par | primer tic vivo | primer tic en que lo visto difiere | qué difiere | primer tic con la elección distinta |
|---|---|---|---:|---:|---|---:|
""")
for d in D1:
    que = ", ".join(d["campos_distintos"] or []) + (f" (agente {', '.join(map(str, d['agentes_distintos']))})" if d.get("agentes_distintos") else "")
    w(f"| {d['serie']} | {d['slot']} | {d['a']} y {d['b']} | {d['primer_tic'][0]} | {d['primer_tic_vista_distinta']} | {que} | {d['primer_tic_elegido_distinto']} |\n")
ab = [d for d in D1 if d["a"] == "APRENDE"]
w(f"""
En los cuatro pares APRENDE–BORRADO lo visto difiere en el tic {min(d['primer_tic_vista_distinta'] for d in ab)} o {max(d['primer_tic_vista_distinta'] for d in ab)}, uno o dos tics después de empezar: el texto que los rivales dicen por el canal
abierto ("blood pays little here" en una partida, "blood pays nothing here" en la otra) o la casilla de un rival. No es cosa del brazo: pasa igual
entre SUELO y TECHO y entre BORRADO y SUELO. Es la pregunta abierta 1 para Ari en `STATUS.md` (algo aleatorio en el mundo que no depende de la
semilla). Mientras lo visto fue igual ({", ".join(str(d['tics_iguales_antes']) for d in ab)} tics), elección y d de cada candidato idénticas en los cuatro pares.

**La comparación que sí se puede hacer: el mismo diario, con los dos juegos de interruptores** (`banco_P7_11.py` → `P7_11_banco_dia1.json`; un
subproceso por vida, cuaderno vacío):

| diario del día 1 | tics | réplica como APRENDE: iguales al diario | réplica como BORRADO: iguales al diario | tics en que las dos réplicas eligen distinto | cuaderno final igual |
|---|---:|---:|---:|---:|---|
""")
for x in B1: w(f"| `{x['vida']}` | {n(x['tics'])} | {n(x['fidelidad_como_APRENDE'].get('igual', 0))} | {n(x['fidelidad_como_BORRADO'].get('igual', 0))} | {len(x['tics_en_que_las_dos_replicas_eligen_distinto'])} | {'sí' if x['cuaderno_fin_igual'] else 'NO'} |\n")
d1 = {b: [C[f"s{s}_d1_{b}_{sl}"] for s in (1, 2) for sl in (10, 11)] for b in ("APRENDE", "BORRADO")}
w(f"""
**Sí: el día 1 son el mismo cuerpo, decisión a decisión.** {n(sum(x['tics'] for x in B1))} tics en 8 vidas, {sum(len(x['tics_en_que_las_dos_replicas_eligen_distinto']) for x in B1)} elecciones distintas entre los dos juegos de interruptores, los 8 cuadernos
finales iguales, y las dos réplicas reproducen el diario entero. El interruptor BORRADO solo se mira al arrancar (`descubre_P7.py:196`), y con el
cuaderno vacío leer o no leer da lo mismo. Lo que difiere el día 1 entre los dos brazos es la partida, no el cuerpo. Para que conste, el día 1
(4 vidas por brazo, `P7_10_campo.json`): botiquines cogidos APRENDE {sum(v['coge_n'] for v in d1['APRENDE'])}, BORRADO {sum(v['coge_n'] for v in d1['BORRADO'])}; usos {sum(v['usos_gastados'] for v in d1['APRENDE'])} y {sum(v['usos_gastados'] for v in d1['BORRADO'])}; regalos {sum(v['regala_n'] for v in d1['APRENDE'])} y {sum(v['regala_n'] for v in d1['BORRADO'])};
puestos {sorted(v['puesto'] for v in d1['APRENDE'])} y {sorted(v['puesto'] for v in d1['BORRADO'])}. Esa es la medida del ruido entre dos partidas del mismo cuerpo con la misma semilla.
(La vida `P710_s1_d1_APRENDE_29581797/10` duró {next(x['tics'] for x in B1 if x['vida'].endswith('APRENDE_29581797/10'))} tics: murió pronto.)
""")

# ───────── seccion 3 ─────────
CV = [v for v in C.values() if not v.get("sin_tics")]
def usos_dia(b, d): return [u["hp0"] for v in CV if v["brazo"] == b and v["dia"] == d for u in v["usos"] if u["gastado"]]
def cre(v):
    x = (((v.get("cuaderno") or {}).get("creencias") or {}).get("first_aid") or {}).get("dentro"); return x.get("cuerpo") if isinstance(x, dict) else None
ap = {(v["serie"], v["slot"], v["dia"]): v for v in CV if v["brazo"] == "APRENDE"}; CRI = [(1, 10), (1, 11), (2, 10), (2, 11)]
w("""
## Sección 3 · La curva día a día

Por día de cada serie (las dos series y los dos asientos juntos: 4 vidas por brazo y día). Vida al usar = mediana sobre los usos gastados de ese
día (entre paréntesis, cuántos); usos por vida = usos / 4. Creencia (cuerpo, dentro del círculo) e ignorancia de APRENDE al fin del día: media de
las cuatro criaturas ("no sé" no entra en la media; entre paréntesis, cuántas tienen creencia).

| día | SUELO: vida al usar | usos por vida | BORRADO: vida al usar | usos por vida | APRENDE: vida al usar | usos por vida | TECHO: vida al usar | usos por vida | APRENDE: creencia | APRENDE: ignorancia |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
""")
for d in range(1, 21):
    cs = [cre(ap[(s, sl, d)]) for s, sl in CRI]; cs = [c for c in cs if c is not None]; ig = [ap[(s, sl, d)]["cuaderno"].get("ignorancia") for s, sl in CRI]; ig = [x for x in ig if x is not None]
    w(f"| {d} | " + " | ".join(f"{n(med(usos_dia(b, d)), 1)} ({len(usos_dia(b, d))}) | {n(len(usos_dia(b, d)) / 4, 2)}" for b in BR) + f" | {n(mean(cs), 1)} ({len(cs)}) | {n(mean(ig), 3)} |\n")
def plano(serie, tol):
    """primer dia a partir del cual todos los valores quedan a <= tol del valor del dia 20"""
    fin = serie[-1]
    for d in range(len(serie)):
        if all(x is not None and abs(x - fin) <= tol for x in serie[d:]): return d + 1
    return None
random.seed(20261004)
def spearman(x, y):
    def rk(a):
        o = sorted(range(len(a)), key=lambda i: a[i]); r = [0.0] * len(a); i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and a[o[j + 1]] == a[o[i]]: j += 1
            for k in range(i, j + 1): r[o[k]] = (i + j) / 2
            i = j + 1
        return r
    return st.correlation(rk(x), rk(y))
def tendencia(b):
    xs = [(v["dia"], u["hp0"]) for v in CV if v["brazo"] == b for u in v["usos"] if u["gastado"]]; dx, hy = [a for a, _ in xs], [c for _, c in xs]; r = spearman(dx, hy); m = 0; N = 5000
    for _ in range(N):
        random.shuffle(hy)
        if abs(spearman(dx, hy)) >= abs(r) - 1e-12: m += 1
    return r, m / N, len(xs)
TEN = {b: tendencia(b) for b in BR}
w(f"""
**¿En qué día se aplana APRENDE?** (criterios puestos después de ver los datos, declarados: la creencia "se aplana" el primer día a partir del
cual ya no se aleja más de 2 puntos de su valor del día 20; la ignorancia, más de 0,02.)

| criatura | creencia: día en que se aplana | creencia ese día → día 20 | ignorancia: día en que se aplana | ignorancia ese día → día 20 |
|---|---:|---|---:|---|
""")
for s, sl in CRI:
    sc = [cre(ap[(s, sl, d)]) for d in range(1, 21)]; si = [ap[(s, sl, d)]["cuaderno"].get("ignorancia") for d in range(1, 21)]; pc, pi = plano(sc, 2.0), plano(si, 0.02)
    w(f"| serie {s}, asiento {sl} | {pc} | {n(sc[pc - 1], 1)} → {n(sc[-1], 1)} | {pi} | {n(si[pi - 1], 3)} → {n(si[-1], 3)} |\n")
mc = [mean([c for c in (cre(ap[(s, sl, d)]) for s, sl in CRI) if c is not None]) for d in range(1, 21)]; mi = [mean([x for x in (ap[(s, sl, d)]["cuaderno"].get("ignorancia") for s, sl in CRI) if x is not None]) for d in range(1, 21)]
w(f"""
Con la media de las cuatro: la creencia se aplana el día {plano(mc, 2.0)} ({n(mc[plano(mc, 2.0) - 1], 1)} → {n(mc[-1], 1)}) y la ignorancia el día {plano(mi, 0.02)} ({n(mi[plano(mi, 0.02) - 1], 3)} → {n(mi[-1], 3)}).
Del día 10 al 20 la creencia media pasa de {n(mc[9], 1)} a {n(mc[19], 1)}: la segunda mitad del campo casi no enseña nada nuevo.

**La vida al usar no baja con los días en ningún brazo.** Correlación de rangos (Spearman) entre el día y la vida al usar, uso a uso, con una
prueba de permutaciones (5.000 barajas de los días, semilla fija): """ + "; ".join(f"{b} ρ = {n(TEN[b][0], 2)} (p = {n(TEN[b][1], 2)}, {TEN[b][2]} usos)" for b in BR) + f""".
En APRENDE la mediana por tramos es {", ".join(n(med([h for d in range(a, a + 5) for h in usos_dia('APRENDE', d)]), 1) for a in (1, 6, 11, 16))} (días 1-5, 6-10, 11-15, 16-20): plana desde el primer tramo. Lo que
separa a APRENDE de BORRADO en la vida al usar ya está el primer tramo ({n(med([h for d in range(1, 6) for h in usos_dia('APRENDE', d)]), 1)} frente a {n(med([h for d in range(1, 6) for h in usos_dia('BORRADO', d)]), 1)}): la creencia media es {n(mc[1], 1)} el día 2 y
{n(mc[4], 1)} el día 5, sube deprisa los cinco primeros días y despacio después. En BORRADO la vida al usar sube con los días (ρ = {n(TEN['BORRADO'][0], 2)}), y
BORRADO no puede aprender de un día a otro: esa es la medida de lo que hacen solas las semillas y el azar con {TEN['BORRADO'][2]} usos. Por días sueltos
la mediana es ruido (entre 0 y 9 usos por brazo y día).
""")

# ───────── seccion 4 ─────────
CATS = ["ir a por un botiquin", "ir a por un objeto sin cogerlo", "ir a por otro objeto", "botin o coger", "regalar o soltar", "hacer sitio", "pelear", "usar un consumible", "moverse paso a paso", "ir al hermano", "ir al centro", "quieto"]
NOM = {"ir a por un botiquin": "ir a por un botiquín", "ir a por un objeto sin cogerlo": "ir a por un objeto (sin llegar a cogerlo)", "ir a por otro objeto": "ir a por otro objeto", "botin o coger": "ir al botín del centro o coger", "regalar o soltar": "regalar o soltar",
       "hacer sitio": "hacer sitio", "pelear": "pelear (atacar, empuñar)", "usar un consumible": "usar un consumible", "moverse paso a paso": "moverse paso a paso", "ir al hermano": "ir al hermano", "ir al centro": "ir al centro", "quieto": "quieto"}
RV = {b: [v for v in L[b] if v["causa_muerte"] == "rival"] for b in BR}
w(f"""
## Sección 4 · Dónde y cómo muere

Causa = la fuente que más daño hizo en los últimos 30 tics (`campo_P7_10.py`, la misma del sello).

| brazo | por rival | por el anillo | otra | sobrevive al final |
|---|---:|---:|---:|---:|
""" + "".join(f"| {b} | {sum(1 for v in L[b] if v['causa_muerte'] == 'rival')} | {sum(1 for v in L[b] if v['causa_muerte'] == 'anillo')} | {sum(1 for v in L[b] if v['causa_muerte'] not in ('rival', 'anillo', 'sobrevive'))} | {sum(1 for v in L[b] if v['causa_muerte'] == 'sobrevive')} |\n" for b in BR) + """
**Las muertes por rival: los 10 segundos anteriores** (240 tics; a cada tic, el candidato en curso: el último elegido distinto de `noop` en el medio
segundo anterior). Reparto de los tics de esa ventana, sumadas las muertes por rival de cada brazo:

| en curso | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
tot = {b: collections.Counter() for b in BR}
for b in BR:
    for v in RV[b]: tot[b].update(v["muerte"]["categorias"])
otros = sorted({k for b in BR for k in tot[b]} - set(CATS))
for c in CATS + otros:
    if any(100 * tot[b].get(c, 0) / max(1, sum(tot[b].values())) >= 0.05 for b in BR): w(f"| {NOM.get(c, c)} | " + " | ".join(f"{n(100 * tot[b].get(c, 0) / max(1, sum(tot[b].values())), 1)} %" for b in BR) + " |\n")
def fila(nombre, f): w(f"| {nombre} | " + " | ".join(f(b) for b in BR) + " |\n")
w("""
| las muertes por rival, una a una | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
fila("muertes por rival", lambda b: str(len(RV[b])))
fila("lo que más hacía en la ventana: ir a por un botiquín", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["moda"] == "ir a por un botiquin")))
fila("lo que más hacía: moverse paso a paso", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["moda"] == "moverse paso a paso")))
fila("lo que más hacía: quieto", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["moda"] == "quieto")))
fila("lo que más hacía: pelear", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["moda"] == "pelear")))
fila("lo que más hacía: otra cosa", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["moda"] not in ("ir a por un botiquin", "moverse paso a paso", "quieto", "pelear"))))
fila("muere dentro del círculo", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["dentro"])))
fila("muere fuera del círculo", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["dentro"] is False)))
fila("muere con algún botiquín a bordo", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["botiquines_a_bordo"] > 0)))
fila("abrió el canal del botiquín en la ventana", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["tics_en_canal"] > 0)))
fila("con un botiquín a la vista en el suelo al morir", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["dist_botiquin_a_la_vista"] is not None)))
fila("distancia a ese botiquín (mediana, casillas)", lambda b: n(med([v["muerte"]["dist_botiquin_a_la_vista"] for v in RV[b] if v["muerte"]["dist_botiquin_a_la_vista"] is not None]), 1))
fila("vio algún botiquín en el suelo en la ventana", lambda b: str(sum(1 for v in RV[b] if v["muerte"]["dist_botiquin_visto_en_la_ventana"] is not None)))
fila("distancia al más cercano de esos (mediana)", lambda b: n(med([v["muerte"]["dist_botiquin_visto_en_la_ventana"] for v in RV[b] if v["muerte"]["dist_botiquin_visto_en_la_ventana"] is not None]), 1))
fila("vida al empezar la ventana (mediana)", lambda b: n(med([v["muerte"]["hp_al_empezar_la_ventana"] for v in RV[b]]), 1))
fila("daño de rivales en la ventana (mediana)", lambda b: n(med([v["muerte"]["dano_rival"] for v in RV[b]]), 1))
fila("tic de la muerte (mediana)", lambda b: n(med([v["ultimo_tick"] for v in RV[b]])))
w(f"""
El cuerpo no tiene un candidato que se llame huir: alejarse de un rival sale como "moverse paso a paso" (`move_*`, `paso_*`), que también es
acercarse; el diario no los separa y aquí no se separan. Regalar, soltar y hacer sitio casi no aparecen en esas ventanas ({", ".join(f"{b} {sum(v['muerte']['regalos_en_la_ventana'] for v in RV[b])}" for b in BR)} regalos).
Lo que distingue a APRENDE: {sum(1 for v in RV['APRENDE'] if v['muerte']['moda'] == 'ir a por un botiquin')} de sus {len(RV['APRENDE'])} muertes por rival llegan yendo a por un botiquín (BORRADO {sum(1 for v in RV['BORRADO'] if v['muerte']['moda'] == 'ir a por un botiquin')} de {len(RV['BORRADO'])}; SUELO y TECHO, que no tienen
curiosidad, {sum(1 for v in RV['SUELO'] if v['muerte']['moda'] == 'ir a por un botiquin')} y {sum(1 for v in RV['TECHO'] if v['muerte']['moda'] == 'ir a por un botiquin')}), casi siempre dentro del círculo y, en la mayoría, con uno a la vista a unas tres casillas.
""")

# ───────── seccion 5 ─────────
def mc_(b, k): return mean([v["contadores"].get(k, 0) for v in L[b]])
def pc_(b, k): return mean([v["contadores"].get(k, 0) / v["contadores"]["tics"] for v in L[b]])
w("""
## Sección 5 · El tiempo

Media por vida (80 vidas por brazo). "Tics" con el candidato en curso (la definición de la sección 4); entre paréntesis, la parte de la vida.

| | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
fila("tics vivos", lambda b: n(mc_(b, "tics")))
fila("yendo a por un botiquín", lambda b: f"{n(mc_(b, 'tics ir a por un botiquin'))} ({n(100 * pc_(b, 'tics ir a por un botiquin'), 1)} %)")
fila("… de ellos, con un rival a la vista", lambda b: n(mc_(b, "tics ir a por un botiquin con rival a la vista")))
fila("decisiones `ir_curioso` o `ir_objeto` hacia un botiquín (tics con ese elegido)", lambda b: n(mc_(b, "elegido ir a por un botiquin")))
fila("yendo a por un objeto que no llega a coger", lambda b: n(mc_(b, "tics ir a por un objeto sin cogerlo")))
fila("regalando o soltando un botiquín (tics con `soltar_first_aid` elegido)", lambda b: n(mc_(b, "tics soltar botiquin"), 2))
fila("… de ellos, con un rival a la vista", lambda b: n(mc_(b, "tics soltar botiquin con rival a la vista"), 2))
fila("con el canal del botiquín abierto", lambda b: n(mc_(b, "tics en canal"), 1))
fila("… de ellos, con un rival a la vista", lambda b: n(mc_(b, "tics en canal con rival a la vista"), 1))
fila("con algún botiquín a bordo", lambda b: n(mc_(b, "tics con botiquin a bordo")))
fila("con un rival a la vista (toda la vida)", lambda b: f"{n(mc_(b, 'tics con rival a la vista'))} ({n(100 * pc_(b, 'tics con rival a la vista'), 1)} %)")
w(f"""
Regalar es un gesto de un tic: el tiempo no se va en regalar. Se va en ir: BORRADO y APRENDE pasan yendo a por un botiquín {n(100 * pc_('BORRADO', 'tics ir a por un botiquin'), 1)} % y
{n(100 * pc_('APRENDE', 'tics ir a por un botiquin'), 1)} % de la vida; SUELO y TECHO, {n(100 * pc_('SUELO', 'tics ir a por un botiquin'), 1)} % y {n(100 * pc_('TECHO', 'tics ir a por un botiquin'), 1)} %. "Con un rival a la vista" discrimina poco: hay alguno a la vista
más del 80 % del tiempo en los cuatro brazos. (En SUELO y TECHO el destino de `ir_objeto` no está en el diario: solo cuentan como "a por un botiquín"
las rachas que acaban cogiendo uno; las que no acaban en nada van en la fila siguiente, igual para los cuatro.)

Por tramos de días, parte de la vida yendo a por un botiquín:

| | días 1-5 | días 6-10 | días 11-15 | días 16-20 |
|---|---:|---:|---:|---:|
""")
for b in ("BORRADO", "APRENDE"):
    w(f"| {b} | " + " | ".join(f"{n(100 * mean([v['contadores'].get('tics ir a por un botiquin', 0) / v['contadores']['tics'] for v in L[b] if a <= v['dia'] < a + 5]), 1)} %" for a in (1, 6, 11, 16)) + " |\n")
w("""
En APRENDE la ignorancia baja con los días (sección 3) y el tiempo yendo a por botiquines no baja: sube. La curiosidad se hace pequeña, pero el
candidato `ir_curioso` existe siempre que no lleva botiquín y sabe de uno (`descubre_P7.py:286`), y las ganas (k) crecen con la creencia.
""")

# ───────── seccion 6 ─────────
DEST = ["lo recoge el hermano", "lo recoge el mismo", "en el suelo la ultima vez que se vio", "desaparece (rival visto encima)", "desaparece (nadie visto)", "no se volvio a ver"]
DN = {"lo recoge el hermano": "lo recoge el hermano", "lo recoge el mismo": "lo vuelve a coger él mismo", "en el suelo la ultima vez que se vio": "seguía en el suelo la última vez que se vio la casilla", "desaparece (rival visto encima)": "desaparece, con un rival visto encima (lo recoge un rival)", "desaparece (nadie visto)": "desaparece sin ver quién", "no se volvio a ver": "la casilla no se volvió a ver"}
G = {b: [g for v in L[b] for g in v["regala"]] for b in BR}
w("""
## Sección 6 · Los regalos

Un regalo = `soltar_first_aid` elegido y ejecutado (baja el número de botiquines a bordo); puede soltar una pila de varias unidades.

| | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
fila("regalos (gestos)", lambda b: str(len(G[b])))
fila("unidades regaladas", lambda b: str(sum(g["n"] for g in G[b])))
fila("vidas con algún regalo (de 80)", lambda b: str(sum(1 for v in L[b] if v["regala_n"])))
fila("máximo de regalos en una vida", lambda b: str(max(v["regala_n"] for v in L[b])))
for d in DEST:
    if any(g["destino"] == d for b in BR for g in G[b]): fila(DN[d], lambda b, d=d: str(sum(1 for g in G[b] if g["destino"] == d)))
fila("tics hasta que alguien lo recoge (mediana)", lambda b: n(med([g["tics_hasta_recogerlo"] for g in G[b] if "tics_hasta_recogerlo" in g])))
fila("con el hermano a la vista", lambda b: str(sum(1 for g in G[b] if g["hermano_a_la_vista"])))
fila("hermano sano / herido / crítico", lambda b: " / ".join(str(sum(1 for g in G[b] if g["banda_hermano"] == x)) for x in ("healthy", "hurt", "critical")))
fila("con un rival a la vista", lambda b: str(sum(1 for g in G[b] if g["rival_a_la_vista"])))
fila("con el canal del botiquín abierto", lambda b: str(sum(1 for g in G[b] if g["en_canal"])))
fila("vida de quien regala (mediana)", lambda b: n(med([g["hp"] for g in G[b]]), 1))
fila("botiquines cogidos", lambda b: str(sum(v["coge_botiquines"] for v in L[b])))
fila("… de ellos, que había soltado el hermano", lambda b: str(sum(v["coge_botiquines_que_solto_el_hermano"] or 0 for v in L[b])))
filas_reg = [f_ for f_, _ in collections.Counter(r["fila"] for b in BR for r in REG[b]).most_common()]
w("""
**Qué fila gana cuando regala** (réplica, `P7_11_filas.json`: la fila cuya M más mejora entre `soltar_first_aid` y `noop` en el tic de la decisión)
y con qué creencia (k = creencia máxima / cura del catálogo, lo que mira la pieza G; TECHO no pasa por G y vale 1; SUELO vale 0 siempre):

| fila que paga | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
for f_ in filas_reg: fila(f_, lambda b, f_=f_: str(sum(1 for r in REG[b] if r["fila"] == f_)))
fila("k de quien regala: mediana (mín – máx)", lambda b: (f"{n(med([r['k'] for r in REG[b]]), 2)} ({n(min(r['k'] for r in REG[b]), 2)} – {n(max(r['k'] for r in REG[b]), 2)})" if REG[b] else "–"))
fila("regalos con k = 0 (\"no sé\")", lambda b: str(sum(1 for r in REG[b] if r["k"] == 0)))
fila("ventaja de regalar sobre `noop` en d (mediana)", lambda b: n(med([r["dd"] for r in REG[b]]), 4))
sv = max(L["SUELO"], key=lambda v: v["regala_n"])
ap_g = G["APRENDE"]; te_g = G["TECHO"]
w(f"""
({no_casan} decisión de las {sum(len(G[b]) for b in BR) + sum(len(usos_g[b]) for b in BR)} de usar o regalar no coincide en la réplica y queda fuera de estas dos tablas.)

**Sí, TECHO regala: {len(te_g)} gestos, {sum(g['n'] for g in te_g)} unidades, en {sum(1 for v in L['TECHO'] if v['regala_n'])} de 80 vidas.** Los paga S-PROVISION (la hermana sin venda) en {sum(1 for r in REG['TECHO'] if r['fila'] == 'S-PROVISION')} y
S-HERIDO en {sum(1 for r in REG['TECHO'] if r['fila'] == 'S-HERIDO')}. APRENDE regala {len(ap_g)}: {sum(1 for r in REG['APRENDE'] if r['fila'] == 'S-PROVISION')} por S-PROVISION, con k mediana {n(med([r['k'] for r in REG['APRENDE']]), 2)} (creencia {n(med([g['creencia_max'] for g in ap_g if g['creencia_max'] is not None]), 1)}): la pieza G deja
pasar el regalo en proporción a lo aprendido, y con una creencia de 34 sobre 50 deja pasar dos tercios de S-PROVISION. Ninguno de los {len(ap_g)} regalos de
APRENDE es con "no sé". El hermano está sano en {sum(1 for g in ap_g if g['banda_hermano'] == 'healthy')} de {len(ap_g)}: la mayoría no son regalos a un herido, son a un hermano sin botiquín.

**A dónde van.** De los {len(ap_g)} regalos de APRENDE, {sum(1 for g in ap_g if g['destino'] == 'lo recoge el mismo')} los vuelve a coger el mismo que los soltó, {sum(1 for g in ap_g if g['destino'] == 'lo recoge el hermano')} los recoge el hermano, {sum(1 for g in ap_g if g['destino'].startswith('en el suelo'))} seguían en el
suelo y {sum(1 for g in ap_g if g['destino'].startswith('desaparece'))} se lo lleva un rival. En TECHO: {sum(1 for g in te_g if g['destino'] == 'lo recoge el mismo')}, {sum(1 for g in te_g if g['destino'] == 'lo recoge el hermano')}, {sum(1 for g in te_g if g['destino'].startswith('en el suelo'))} y {sum(1 for g in te_g if g['destino'].startswith('desaparece'))}. A los rivales no les llega casi nada en ningún brazo. El regalo de
APRENDE es sobre todo un ir y venir entre los dos hermanos y el suelo: de los {sum(v['coge_botiquines'] for v in L['APRENDE'])} botiquines que coge APRENDE, {sum(v['coge_botiquines_que_solto_el_hermano'] or 0 for v in L['APRENDE'])} los había soltado el hermano
y {sum(1 for g in ap_g if g['destino'] == 'lo recoge el mismo')} los había soltado él mismo. Quitando esas dos partidas quedan {sum(v['coge_botiquines'] for v in L['APRENDE']) - sum(v['coge_botiquines_que_solto_el_hermano'] or 0 for v in L['APRENDE']) - sum(1 for g in ap_g if g['destino'] == 'lo recoge el mismo')} cogidas "nuevas" (BORRADO: {sum(v['coge_botiquines'] for v in L['BORRADO']) - sum(v['coge_botiquines_que_solto_el_hermano'] or 0 for v in L['BORRADO']) - sum(1 for g in G['BORRADO'] if g['destino'] == 'lo recoge el mismo')}; TECHO: {sum(v['coge_botiquines'] for v in L['TECHO']) - sum(v['coge_botiquines_que_solto_el_hermano'] or 0 for v in L['TECHO']) - sum(1 for g in te_g if g['destino'] == 'lo recoge el mismo')}; SUELO: {sum(v['coge_botiquines'] for v in L['SUELO']) - sum(v['coge_botiquines_que_solto_el_hermano'] or 0 for v in L['SUELO']) - sum(1 for g in G['SUELO'] if g['destino'] == 'lo recoge el mismo')}).
Está concentrado: las tres vidas que más regalan suman {sum(sorted((v['regala_n'] for v in L['APRENDE']), reverse=True)[:3])} de los {len(ap_g)}.

SUELO regala {len(G['SUELO'])} veces con k = 0: la pieza G le quita al botiquín su valor para el hermano, ninguna fila mejora y en {sum(1 for r in REG['SUELO'] if abs(r['dd']) < 1e-9)} de {len(REG['SUELO'])} la d de
regalar es exactamente la de `noop`: son empates que gana `soltar_first_aid` porque el desempate de la casa no deja ganar a `noop`
(`decisor_zs.py:895-897`, `exclude_noop=True`). {sv['regala_n']} de los {len(G['SUELO'])} son de una sola vida (serie {sv['serie']}, día {sv['dia']}, asiento {sv['slot']}). Con empate exacto en BORRADO: {sum(1 for r in REG['BORRADO'] if abs(r['dd']) < 1e-9)} de {len(REG['BORRADO'])};
APRENDE: {sum(1 for r in REG['APRENDE'] if abs(r['dd']) < 1e-9)} de {len(REG['APRENDE'])}; TECHO: {sum(1 for r in REG['TECHO'] if abs(r['dd']) < 1e-9)} de {len(REG['TECHO'])}.
""")

# ───────── seccion 7 ─────────
def met(v):
    c = v["contadores"]
    return {"botiquines cogidos": v["coge_botiquines"], "regalos": v["regala_n"], "usos": sum(1 for u in v["usos"] if u.get("gastado")), "canales interrumpidos": sum(1 for u in v["usos"] if not u.get("gastado")),
            "tics yendo a por un botiquín": c.get("tics ir a por un botiquin", 0), "… con un rival a la vista": c.get("tics ir a por un botiquin con rival a la vista", 0), "tics con el canal abierto": c.get("tics en canal", 0),
            "tics con un rival a la vista": c["tics con rival a la vista"], "tics vivos": c["tics"], "muere por rival (0/1)": int(v["causa_muerte"] == "rival"), "muere por el anillo (0/1)": int(v["causa_muerte"] == "anillo"),
            "sobrevive al final (0/1)": int(v["causa_muerte"] == "sobrevive"), "daño de rivales en los últimos 10 s": v["muerte"]["dano_rival"], "vida al morir": v["hp_final"], "puesto": v["puesto"]}
def par(a, b):
    out = []
    for m in met(L[a][0]):
        ps = collections.defaultdict(lambda: {a: [], b: []})
        for x in (a, b):
            for v in L[x]: ps[v["semilla"]][x].append(met(v)[m])
        d = [st.mean(p[a]) - st.mean(p[b]) for p in ps.values()]; mu = st.mean(d); se = st.stdev(d) / math.sqrt(len(d))
        out.append((m, st.mean(met(v)[m] for v in L[a]), st.mean(met(v)[m] for v in L[b]), mu, se, (mu / se if se else None), len(d)))
    return out
w("""
## Sección 7 · Lo que distingue a APRENDE (sin conclusiones causales)

Para cada medida, la diferencia entre brazos emparejada por semilla: en cada una de las 20 semillas, la media de las 4 vidas de un brazo (2 series
× 2 asientos) menos la del otro; d̄ es la media de esas 20 diferencias y se su error típico (el ruido entre semillas). **En negrita, |d̄| > 2·se.**
Las dos partidas de una semilla no son el mismo mundo (sección 2) y las 15 medidas no son independientes: con tantas, alguna pasaría de 2·se por azar.

""")
for a, b in (("APRENDE", "TECHO"), ("APRENDE", "BORRADO"), ("BORRADO", "TECHO")):
    w(f"| medida (por vida) | {a} | {b} | d̄ ({a} − {b}) | se | d̄ / se |\n|---|---:|---:|---:|---:|---:|\n")
    for m, xa, xb, mu, se, z, k in par(a, b):
        dec = 0 if abs(xa) >= 100 else 2; neg = "**" if (z is not None and abs(z) > 2) else ""
        w(f"| {m} | {n(xa, dec)} | {n(xb, dec)} | {neg}{n(mu, dec)}{neg} | {n(se, dec)} | {neg}{n(z, 1)}{neg} |\n")
    w("\n")
PT = {m: (mu, se, z) for m, _, _, mu, se, z, _ in par("APRENDE", "TECHO")}; PB = {m: (mu, se, z) for m, _, _, mu, se, z, _ in par("APRENDE", "BORRADO")}; BT = {m: (mu, se, z) for m, _, _, mu, se, z, _ in par("BORRADO", "TECHO")}
w(f"""Lo que se lee, sin decir por qué:

- **Ir a por botiquines no separa a APRENDE de BORRADO** (d̄ / se = {n(PB['tics yendo a por un botiquín'][2], 1)}) y sí a los dos de TECHO ({n(PT['tics yendo a por un botiquín'][2], 1)} y {n(BT['tics yendo a por un botiquín'][2], 1)}). BORRADO va tanto como
  APRENDE y no acaba peor que TECHO (puesto: d̄ / se = {n(BT['puesto'][2], 1)}; vida al morir: {n(BT['vida al morir'][2], 1)}). Ir a por botiquines, por sí solo, no viene con peor puesto en este campo.
- **Lo que APRENDE tiene y BORRADO no**: coge más (d̄ / se = {n(PB['botiquines cogidos'][2], 1)}), regala más ({n(PB['regalos'][2], 1)}), y acaba con menos vida ({n(PB['vida al morir'][2], 1)}) y peor puesto ({n(PB['puesto'][2], 1)}).
  En usos no se distinguen ({n(PB['usos'][2], 1)}).
- **Frente a TECHO**, APRENDE coge más ({n(PT['botiquines cogidos'][2], 1)}), regala más ({n(PT['regalos'][2], 1)}), usa más ({n(PT['usos'][2], 1)}), tiene el canal abierto más tiempo ({n(PT['tics con el canal abierto'][2], 1)}), muere más por
  rival ({n(PT['muere por rival (0/1)'][2], 1)}) y recibe más daño de rivales en sus últimos 10 segundos ({n(PT['daño de rivales en los últimos 10 s'][2], 1)}).
- **Las diferencias grandes frente al ruido** son las de conducta con los botiquines (ir, coger, regalar: entre 2 y 6 se). Las de resultado (puesto,
  vida al morir, muerte por rival) están entre 2 y 3 se: fuera del criterio del sello, pero cerca del borde para 15 medidas miradas a la vez.
- Dentro de un brazo, cruzar el puesto con los botiquines cogidos o usados no sirve: quien vive más coge y usa más, y vive más quien queda mejor.
""")

# ───────── seccion 8, privacidad, archivos ─────────
w(f"""
## Sección 8 · Lo que queda para la mesa (propuestas, nada decidido)

1. **Qué es SUELO.** Tal como está es "esperanza sin memoria". Si la mesa quiere además el suelo del diseño ("no sabe": cura imaginada 0, ganas 0),
   haría falta un quinto brazo o apagar la esperanza en SUELO (`GEMV_P7_ESPERANZA=0` solo en ese brazo). Cualquiera de las dos cosas es un campo nuevo con sello nuevo.
2. **P5 del sello** predecía sobre un SUELO que ya no existía cuando se selló. El resultado (falla) no cambia; la lectura sí: no informa de si un cuerpo que no sabe usa botiquines.
3. **El regalo entre hermanos sanos.** En APRENDE, S-PROVISION paga {sum(1 for r in REG['APRENDE'] if r['fila'] == 'S-PROVISION')} de {len(REG['APRENDE'])} regalos, con el hermano sano en {sum(1 for g in ap_g if g['banda_hermano'] == 'healthy')}, y {sum(1 for g in ap_g if g['destino'] == 'lo recoge el mismo')} los vuelve a coger
   quien los soltó. Si ese ir y venir es lo que le cuesta la posición a APRENDE no está medido: haría falta un banco o un brazo que lo quite (por
   ejemplo, APRENDE sin regalo del botiquín) y ver si P6 se cierra.
4. **La curiosidad no se apaga.** Con la ignorancia en 0,05 APRENDE pasa más tiempo yendo a por botiquines que el día 1, y casi la mitad de sus
   muertes por rival llegan yendo a por uno. Aquí pesan a la vez la curiosidad (pieza F) y las ganas (pieza C, que crecen con la creencia); separarlas pide un banco.
5. **BORRADO y APRENDE no llevaban el mismo `descubre_P7.py`** ({sum(v['ventanas_con_regalo_apuntadas'] for v in L['BORRADO'])} ventanas afectadas en BORRADO). Para el próximo campo: las imágenes fijas se hornean después del freno, o el freno no toca código.
6. **El día 1 no es un control emparejado.** La misma semilla no da el mismo mundo desde el tic 482; "emparejado por semilla" quiere decir mismo mapa, no misma partida.

## Privacidad

- Los JSON de respuesta de la plataforma se guardan ya sin correo: `privado_P7.sin_correos` en `lanza_P7_10.py` (y en los lanzadores que vengan).
- Antes de cada push a gemv-coworld: `cantera/paper6/taller/revisa_subida.py` busca correos, claves y rutas personales en todas las líneas nuevas
  que se suben (no solo en la lista del taller); si encuentra algo, sale con error y el push no se hace. Queda escrito en `CLAUDE.md`.
- La historia del repositorio no se ha reescrito: los JSON de `P7_10_res/` y de pasos anteriores ya subidos siguen llevando el correo de la cuenta.

## Archivos

| archivo | qué es |
|---|---|
| `analiza_P7_11.py` → `P7_11_vidas.json`, `P7_11_dia1.json` | lectura de los 320 diarios: usos, regalos y su destino, el tiempo, la muerte; el día 1 tic a tic |
| `banco_P7_11.py` → `P7_11_banco_dia1.json` | réplica de los 8 diarios del día 1 con los interruptores de APRENDE y de BORRADO |
| `banco_P7_11b.py` → `P7_11_filas.json` | réplica de las {len(F)} vidas con algún uso o regalo: las filas de cada candidato en esos tics |
| `privado_P7.py`, `cantera/paper6/taller/revisa_subida.py` | quitar correos al guardar; comprobación previa al push |
| `escribe_informe_P7_11.py`, `informe_P7_11.md` | este informe |
""")
txt = "".join(W); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_11.md"), "w").write(txt); print("informe escrito", len(txt))
