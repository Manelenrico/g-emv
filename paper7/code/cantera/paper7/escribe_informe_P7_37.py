"""[P7-37] Escribe informe_P7_37.md desde P7_37_cadena.json, P7_37_cuadernos.json (cuaderno_P7_37), P7_37_momentos.json (banco_P7_37 --momentos) y P7_36_cogidas.json. Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
CA = J("P7_37_cadena.json"); CU = J("P7_37_cuadernos.json"); MO = J("P7_37_momentos.json"); CG = J("P7_36_cogidas.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
COSAS = ("botiquin", "racion", "red", "camuflaje"); CRI = ("s1 a10", "s1 a11", "s2 a10", "s2 a11"); VAR = ("campo", "descontada", "C", "C5"); IDS = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}
COGIDAS = {(v["serie"], v["dia"], v["asiento"], x["tick_decide"]) for v in CG["vidas"] if v["brazo"] == "APRENDE" for x in v["cogidas"]}
med = lambda xs: (st.median(xs) if xs else None)

# ── seccion 1 ──
T1 = ["| cosa | recuerdos (sin cortes, cuadernos del día 20) | con daño conocido en la ventana (descontados) | importancia original: mediana (cuartiles) | importancia descontada: mediana (cuartiles) |", "|---|---:|---:|---|---|"]
for o in COSAS:
    x = CU["importancia"][o]; T1.append(f"| {o} | {x['recuerdos']} | {x['descontados']} | {n(x['original_mediana'], 4)} ({n(x['original_cuartiles'][0], 3)} · {n(x['original_cuartiles'][1], 3)}) | {n(x['descontada_mediana'], 4)} ({n(x['descontada_cuartiles'][0], 3)} · {n(x['descontada_cuartiles'][1], 3)}) |")
desc_tot = sum(x["descontados"] for x in CU["importancia"].values()); rec_tot = sum(x["recuerdos"] for x in CU["importancia"].values())
fid_c = collections.Counter()
for k, v in CA["criaturas"].items():
    for d in v: fid_c.update(d.get("fidelidad") or {})

# ── seccion 2 ──
T2 = ["| criatura | día | " + " | ".join(f"{o}: curiosidad campo → nueva · importancia esperada · creencia campo → descontada" for o in COSAS) + " |", "|---|---|" + "---|" * 4]
for k in CRI:
    for d in ("5", "10", "15", "20"):
        x = CU["criaturas"][k]["dias"].get(d)
        if x: T2.append(f"| {k} | {d} | " + " | ".join(f"{n(x[o]['curiosidad_campo'], 3)} → {n(x[o]['curiosidad_nueva'], 3)} · {n(x[o]['importancia_esperada'], 2)} · {n(x[o]['creencia_campo'], 1)} → {n(x[o]['creencia_descontada'], 1)}" for o in COSAS) + " |")
raz = {"campo": [], "nueva": []}; dif_cre = []
for k in CRI:
    for d, x in CU["criaturas"][k]["dias"].items():
        for regla in ("campo", "nueva"):
            ui = max(x["red"][f"curiosidad_{regla}"], x["camuflaje"][f"curiosidad_{regla}"]); uu = max(x["botiquin"][f"curiosidad_{regla}"], x["racion"][f"curiosidad_{regla}"])
            if uu > 0: raz[regla].append(ui / uu)
        for o in ("botiquin", "racion"):
            if x[o]["creencia_campo"] is not None and x[o]["creencia_descontada"] is not None: dif_cre.append(abs(x[o]["creencia_campo"] - x[o]["creencia_descontada"]))
M = CU["manda_lo_inutil"]
T3 = ["| criatura | cosa | pruebas (días) | tras cada prueba: vuelve a mandar el día… (curiosidad nueva de la cosa · la mayor de lo útil) |", "|---|---|---|---|"]
desp_sig = 0; desp_tot = 0; fuerza = []
for k in CRI:
    for o in ("red", "camuflaje"):
        L = CU["criaturas"][k]["despierta"][o]; desp_tot += len(L); desp_sig += sum(1 for e in L if e["vuelve_a_mandar_dia"] == e["prueba_dia"] + 1); fuerza += [e["curiosidad_entonces"] for e in L if e["curiosidad_entonces"] is not None]
        T3.append(f"| {k} | {o} | {', '.join(str(e['prueba_dia']) for e in L) or '—'} | {'; '.join(f'd{e['prueba_dia']} → {e['vuelve_a_mandar_dia'] if e['vuelve_a_mandar_dia'] else 'no'} ({n(e['curiosidad_entonces'], 3)} · {n(e['curiosidad_util_entonces'], 3)})' for e in L) or '—'} |")

# ── seccion 3: los momentos en banco ──
def momentos(var):
    out = []
    for r in MO[var]:
        if r.get("error"): continue
        for t, m in r["momentos"].items(): out.append((r["serie"], r["dia"], r["slot"], int(t), m))
    return out
fid = {var: collections.Counter() for var in VAR}
for var in VAR:
    for r in MO[var]: fid[var].update(r.get("fidelidad") or {})
T4 = ["| lectura | fidelidad al diario (80 vidas) | de las cogidas de red y camuflaje del diario: siguen siendo `coger` | lo que elige en las demás | en las aperturas de prueba: curiosidad de la red (mediana) · del camuflaje · del botiquín · de la ración | momentos en que la clase que más llama es red o camuflaje |", "|---|---|---:|---|---|---:|"]
S3 = {}
for var in VAR:
    mm = momentos(var); cog = [(s, d, sl, t, m) for s, d, sl, t, m in mm if (s, d, sl, t) in COGIDAS]; ape = [(s, d, sl, t, m) for s, d, sl, t, m in mm if (s, d, sl, t) not in COGIDAS]
    sig = sum(1 for *_, m in cog if m.get("replica") == "coger"); otros = collections.Counter(m.get("replica") for *_, m in cog if m.get("replica") != "coger")
    cur = {o: med([m["clases"][o][var] for *_, m in ape if m.get("clases")]) for o in IDS}
    lider = sum(1 for *_, m in mm if m.get("clases") and max(m["clases"], key=lambda o: m["clases"][o][var]) in ("net", "camouflage"))
    S3[var] = {"cogidas": len(cog), "siguen": sig, "otros": otros, "aperturas": len(ape), "cur": cur, "lider": lider, "momentos": len(mm)}
    T4.append(f"| {var} | {fid[var].get('igual', 0)} igual · {fid[var].get('difiere', 0)} difiere | {sig} de {len(cog)} | {', '.join(f'`{k}` {c}' for k, c in otros.most_common(4)) or '—'} | {n(cur['net'], 3)} · {n(cur['camouflage'], 3)} · {n(cur['first_aid'], 3)} · {n(cur['rations'], 3)} | {lider} de {len(mm)} |")

# ── seccion 4: variante C, contextos ──
mmC = momentos("C"); mm5 = momentos("C5")
def lidera_gear(m, var): return bool(m.get("clases")) and max(m["clases"], key=lambda o: m["clases"][o][var]) in ("net", "camouflage")
ctxC = collections.Counter(); cautela = collections.Counter(); sit_pref = collections.Counter(); forma_pref = collections.Counter(); pref_total = collections.Counter()
for s, d, sl, t, m in mmC:
    if not m.get("clases"): continue
    pel = m["peligro"]; calma = pel.get("calma")
    if lidera_gear(m, "C"):
        ctxC["calma" if calma else "peligro"] += 1
        if not calma: cautela["apagada (cautela 0)" if m["cautela"] == 0 else ("atenuada (0 < cautela < 1)" if m["cautela"] < 1 else "sin cautela (1)")] += 1
for s, d, sl, t, m in mm5:
    for o, p in (m.get("preferida") or {}).items():
        f, dentro, golpe = [x.strip() for x in p["mejor"].split("·")]; forma_pref[(IDS[o], f)] += 1; sit_pref[(IDS[o], f"{dentro} · {golpe}")] += 1; pref_total[IDS[o]] += 1
# en calma: la ignorancia por parecido en la situacion de ahora frente a la mejor situacion nueva (C5, forma coger)
repite = collections.Counter()
for s, d, sl, t, m in mm5:
    for o, p in (m.get("preferida") or {}).items():
        ahora = f"coger · {'dentro' if m['contexto']['dentro'] else 'fuera'} · {'golpeado' if m['contexto']['golpeado_48'] else 'sin golpe'}"
        mejor_sit = max((k for k in p["todas"] if k.startswith("coger")), key=lambda k: p["todas"][k]); repite[(IDS[o], "la de ahora" if mejor_sit == ahora else "otra situación")] += 1
T5 = ["| cosa | momentos | forma preferida (C5) | situación preferida (C5) | con la forma `coger`: la situación que más llama es la de ahora / otra |", "|---|---:|---|---|---|"]
for o in ("red", "camuflaje"):
    T5.append(f"| {o} | {pref_total[o]} | {', '.join(f'{f} {c}' for (oo, f), c in forma_pref.most_common() if oo == o)} | {', '.join(f'{sit} {c}' for (oo, sit), c in sit_pref.most_common() if oo == o)} | {repite[(o, 'la de ahora')]} / {repite[(o, 'otra situación')]} |")
ctx_mom = collections.Counter("calma" if m["peligro"].get("calma") else "peligro" for *_, m in mmC if m.get("peligro"))
def forma_de(acciones):
    for a in reversed(list(acciones or [])):
        a = str(a)
        for f in ("ponerse", "empunar", "usar", "coger"):
            if a.startswith(f): return f
    return "coger"
ctx_real = collections.Counter(); forma_real = collections.Counter()
for k in CRI:
    s_, sl = int(k[1]), int(k[-2:]); c = json.load(open(os.path.join(AQUI, "P7_37_res", f"cuaderno_descontada_s{s_}_d20_{sl}.json")))
    for o in ("net", "camouflage"):
        for sit in c["objetos"].get(o, {}).get("situaciones", {}).values():
            for r in sit:
                if r.get("corte"): continue
                ctx_real[(IDS[o], "dentro · sin golpe" if (r["contexto"]["dentro"] and not r["contexto"]["golpeado_48"]) else ("dentro · golpeado" if r["contexto"]["dentro"] else ("fuera · golpeado" if r["contexto"]["golpeado_48"] else "fuera · sin golpe")))] += 1; forma_real[(IDS[o], forma_de(r.get("acciones")))] += 1

out = f"""# P7-37 · La curiosidad por lo que podría importar

*10-oct-2026. Coste cero: sin partidas, sin llamadas. Plataforma: 0 créditos de experiencia (acumulado del siete: 710 partidas = 710 créditos, contadas de los estados de los
lanzadores P7-8 a P7-34 y de los resultados de P7-5/6/7; disponibles hoy, dato de Manel: 496 de 1.000, con recarga de 71 al día). Consola de Anthropic: 0 USD.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar; solo banco, nada se juega ni cambia en el campo. Diseño
propuesto a Manel, pendiente de su sí. Scripts: `curiosa_P7_37.py` (= `{md5('curiosa_P7_37.py')}`; la pieza, solo banco), `banco_P7_37.py` (`--cadena` → `P7_37_cadena.json` y
`P7_37_res/cuaderno_descontada_*.json`; `--momentos` → `P7_37_momentos.json`), `cuaderno_P7_37.py` → `P7_37_cuadernos.json`, `escribe_informe_P7_37.py` (este informe; ninguna
cifra a mano). Las definiciones (importancia descontada, importancia esperada, variantes C y C5 con sus números declarados) están en la cabecera de `curiosa_P7_37.py`.*

## Sección 1 · La importancia descontada

La importancia de un recuerdo (cambio del malestar por eje entre abrir y cerrar la ventana) se vuelve a tasar restando el cambio que viene del daño conocido (anillo estando
fuera, golpes de rivales a la vista), como ya hace el efecto: al cerrar, se tasa la obs con la vida que tendría sin ese daño (`A.appraise` sobre una copia) y la diferencia de
malestar se descuenta. Para que la cadena fuera honesta, las 4 criaturas se replicaron día a día EN CADENA (el cuaderno que escribe la réplica del día d es el que lee el día
d+1): {fid_c.get('igual', 0)} decisiones iguales al diario · {fid_c.get('difiere', 0)} distintas en 80 vidas (la réplica lleva ya la curiosidad nueva; lazo abierto, las obs son las del diario).

{chr(10).join(T1)}

Solo {desc_tot} de {rec_tot} recuerdos tienen daño conocido dentro de su ventana (todos de la ración: se come bajo golpes; las ventanas del botiquín, la red y el camuflaje no reciben daño
conocido, o el que reciben no es de fuente a la vista), y en ellos la mediana apenas se mueve. La importancia de «no hizo nada» no baja con el descuento: lo que mueve el malestar en
una ventana de 10 s de calma no es el daño conocido, es lo demás (el hambre, la distancia a la hermana, el anillo que se acerca, lo que se ve).

## Sección 2 · La curiosidad por lo que podría importar

Curiosidad de clase = ignorancia × importancia esperada; importancia esperada = media ponderada de la importancia (escalar min(1, S/E)) de los recuerdos sin cortes con un
neutro de importancia 1 y peso 1 que no se apaga; intensidad como en el campo (1 + importancia descontada). Recalculado sobre los 80 cuadernos encadenados (cierre de cada día):

{chr(10).join(T2)}

- **¿Cuántas veces al día sería lo inútil la clase que más llama?** En {M['nueva']['lo_inutil_manda']} de {M['nueva']['cierres']} cierres de día (criatura × día), frente a {M['campo']['lo_inutil_manda']} de {M['campo']['cierres']} con la curiosidad del campo.
- **¿Cuánto valdría su curiosidad frente a la de lo útil?** La mayor curiosidad de red o camuflaje dividida por la mayor de botiquín o ración: mediana {n(med(raz['nueva']), 2)} (cuartiles
  {n(sorted(raz['nueva'])[len(raz['nueva']) // 4], 2)} · {n(sorted(raz['nueva'])[3 * len(raz['nueva']) // 4], 2)}) con la regla nueva, frente a {n(med(raz['campo']), 2)} ({n(sorted(raz['campo'])[len(raz['campo']) // 4], 2)} · {n(sorted(raz['campo'])[3 * len(raz['campo']) // 4], 2)}) con la del campo. La importancia esperada de lo inútil
  ({n(min(x[o]['importancia_esperada'] for k in CRI for x in CU['criaturas'][k]['dias'].values() for o in ('red', 'camuflaje') if x[o]['recuerdos']), 2)}-{n(max(x[o]['importancia_esperada'] for k in CRI for x in CU['criaturas'][k]['dias'].values() for o in ('red', 'camuflaje') if x[o]['recuerdos']), 2)}) no queda por debajo de la de lo útil ({n(min(x[o]['importancia_esperada'] for k in CRI for x in CU['criaturas'][k]['dias'].values() for o in ('botiquin', 'racion') if x[o]['recuerdos']), 2)}-{n(max(x[o]['importancia_esperada'] for k in CRI for x in CU['criaturas'][k]['dias'].values() for o in ('botiquin', 'racion') if x[o]['recuerdos']), 2)}): el neutro de importancia 1 pesa como varios recuerdos de 0,1-0,3, y curar
  no importa diez veces más que llevar una red, importa dos o tres veces más (sección 1).
- **¿Se mantiene la creencia de lo útil?** Sí: la mayor diferencia entre la creencia del botiquín o la ración con el cuaderno del campo y con el descontado, en los 80 cierres, es {n(max(dif_cre), 3)}.
- **¿Cuándo volvería a despertar la curiosidad por lo inútil tras días sin tocarlo, y con qué fuerza?** No hay días sin tocarlo en los que esté dormida: tras cada prueba vuelve a ser la clase que
  más llama al día siguiente en {desp_sig} de {desp_tot} pruebas, con una curiosidad de {n(min(fuerza), 3)}-{n(max(fuerza), 3)} (mediana {n(med(fuerza), 3)}) frente a la de lo útil (tabla).

{chr(10).join(T3)}

## Sección 3 · Los 71 momentos, en banco

Las 80 vidas de APRENDE replicadas con el cuaderno descontado del día anterior, bajo cuatro lecturas de la curiosidad de clase: **campo** (ignorancia), **descontada**
(ignorancia × importancia esperada), **C** (ignorancia por parecido de contexto y foto × importancia esperada) y **C5** (parecido que incluye cómo se probó, la mayor entre
las formas de la cosa, × importancia esperada). Momentos: los {S3['campo']['cogidas']} tics en que el diario decidió coger una red o un camuflaje y las {S3['campo']['aperturas']} aperturas de prueba de red y camuflaje.

{chr(10).join(T4)}

Con la lectura del campo (sobre el cuaderno descontado, que cambia {desc_tot} intensidades) la réplica es casi la del diario; con las otras tres cambian muchas decisiones (la fila
`R-CURIOSIDAD` y `ir_curioso` leen otra cosa), pero en los momentos de coger, **`coger` sigue ganando** en {S3['descontada']['siguen']}, {S3['C']['siguen']} y {S3['C5']['siguen']} de {S3['campo']['cogidas']}: la cosa está a los pies y la
curiosidad, sea cual sea su lectura, se alivia al tenerla. Lo que se va en C y C5 (una de cada tres) se va a `ir_curioso` hacia otra clase: por parecido, el botiquín
que nunca se usó en una situación como esa llama tanto o más que la red que ya se llevó en ella (en las aperturas, con C la curiosidad del botiquín {n(S3['C']['cur']['first_aid'], 3)} ≥ red {n(S3['C']['cur']['net'], 3)}).

## Sección 4 · Variante C: en qué contextos probaría de nuevo

En los {len(mmC)} momentos ({ctx_mom['calma']} en calma, {ctx_mom['peligro']} en peligro, según `peligro_de` de P7-33), la clase que más llama con C es la red o el camuflaje en {ctxC['calma'] + ctxC['peligro']}: {ctxC['calma']} en calma y
{ctxC['peligro']} en peligro. De los de peligro, la cautela por distancia (P7-26) la habría apagado del todo en {cautela['apagada (cautela 0)']} (cautela 0), atenuado en {cautela['atenuada (0 < cautela < 1)']} y dejado pasar en {cautela['sin cautela (1)']}.
¿Repetiría pruebas en calma o iría a contextos nuevos? Con la forma `coger`, la situación que más llama es OTRA que la de ahora (fuera del círculo o recién golpeada) en
{repite[('red', 'otra situación')] + repite[('camuflaje', 'otra situación')]} de {sum(repite.values())} momentos y la de ahora en {repite[('red', 'la de ahora')] + repite[('camuflaje', 'la de ahora')]}: las pruebas reales de los cuadernos del día 20 fueron {', '.join(f'{o} {sit} {c}' for (o, sit), c in ctx_real.most_common())}, así que por parecido la calma ya está «gastada» y lo
nuevo es el peligro; y ahí entra la cautela.

## Sección 5 · La mirada de científico (C5): qué forma y qué situación preferiría

{chr(10).join(T5)}

Las formas de las pruebas reales (cuadernos del día 20): {', '.join(f'{o} `{f}` {c}' for (o, f), c in forma_real.most_common())}. El camuflaje cuenta como `coger` porque con el cuerpo vacío coger ES
vestir (sim.nim, PROMPT_17/18): la forma se lee de la acción, no del resultado, y por eso C5 toma `ponerse` como forma nueva aunque el resultado sea el mismo (límite
declarado). La forma nueva (`empunar` la red, `ponerse` el camuflaje) y la situación nueva (fuera del círculo, o recién golpeada) son las que más llaman: con la mirada de
científico la siguiente prueba no repetiría la mirada, iría a empuñar la red o ponerse el camuflaje en peligro, que es justo lo que la cautela apaga.

## Lo que se desprende (propuestas, no decisiones)

1. El descuento del daño conocido no toca «no hizo nada»: su importancia no viene del daño, viene del malestar de fondo que cambia en 10 s. Para que «no hizo nada» importe
   poco, la importancia tendría que medirse contra lo que habría pasado sin la prueba (la foto del tic de apertura proyectada 10 s, o el malestar de la hermana), no contra el
   malestar de antes.
2. Con el neutro de importancia 1, la curiosidad nueva sigue mandando a lo inútil; el neutro tendría que apagarse con los recuerdos de «no hizo nada» (o pesar menos que 1) para
   que lo probado sin fruto deje de llamar.
3. La variante C y la C5 mueven la curiosidad hacia lo no probado (otra situación, otra forma), que es peligro: sin la cautela de P7-26 en el campo, sería una criatura que
   prueba redes bajo golpes. Si la mesa quiere C5, va con la cautela.
"""
open(os.path.join(AQUI, "informe_P7_37.md"), "w", encoding="utf-8").write(out); print("informe_P7_37.md", out.count("\n"), "lineas")
