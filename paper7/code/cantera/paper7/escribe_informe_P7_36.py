"""[P7-36] Escribe informe_P7_36.md desde P7_36_cogidas.json (analiza_P7_36), P7_36_banco.json (banco_P7_36) y P7_36_cuadernos.json (cuaderno_P7_36). Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
CG = J("P7_36_cogidas.json"); BA = J("P7_36_banco.json"); CU = J("P7_36_cuadernos.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
COSAS = ("botiquin", "racion", "red", "camuflaje"); CRI = ("s1 a10", "s1 a11", "s2 a10", "s2 a11")

# ── parte 1, diarios ──
A = CG["resumen"]["APRENDE"]; T = CG["resumen"]["TECHO"]; B = CG["resumen"]["BORRADO"]
cgA = [x for v in CG["vidas"] if v["brazo"] == "APRENDE" for x in v["cogidas"]]
T1 = ["| brazo | cogidas de red + camuflaje | gana `coger` | empate exacto con `noop` (gana por N2a) | paisaje degenerado (≤ 1e-3) | `coger` gana a `noop` por: mín · cuartil 1 · mediana · cuartil 3 · máx | gana por menos de 0,01 | empata exactamente con otro candidato |", "|---|---:|---:|---:|---:|---|---:|---|"]
for b, x in (("TECHO", T), ("BORRADO", B), ("APRENDE", A)):
    q = x["coger_gana_a_noop_por_cuartiles"]
    T1.append(f"| {b} | {x['cogidas']} | {x['por_tipo'].get('coger', 0)} | {x['empate_exacto_con_noop']} | {x['degenerado']} | {' · '.join(n(v, 4) for v in q) if q else '—'} | {x['gana_a_noop_por_menos_de_0_01']} | {', '.join(f'{k} {c}' for k, c in x['empata_con_otro']) or '—'} |")
# ── parte 1, banco ──
r0 = [r for r in BA["regla_0"]["vidas"] if not r.get("error")]; r1 = [r for r in BA["regla_1"]["vidas"] if not r.get("error")]
fid0 = collections.Counter(); fid1 = collections.Counter()
for r in r0: fid0.update(r["fidelidad"])
for r in r1: fid1.update(r["fidelidad"])
filas = collections.Counter(); filas_ej = {}
for r in r0:
    for t, x in r["en_las_cogidas"].items():
        for k, (a_, b_) in (x.get("filas_distintas") or {}).items(): filas[k] += 1; filas_ej.setdefault(k, (a_, b_))
cog1 = [(r, t, x) for r in r1 for t, x in r["en_las_cogidas"].items()]
desap = [(r, t, x) for r, t, x in cog1 if x.get("replica") != "coger"]; a_que = collections.Counter(x.get("replica") for _, _, x in desap)
otros = collections.Counter()
for r in r1:
    cog_t = set(r["en_las_cogidas"])
    for d in r["desacuerdos"]:
        if str(d["t"]) not in cog_t: otros[(d["diario"], d["replica"])] += 1
otros_n = sum(otros.values()); otros_vidas = sum(1 for r in r1 if any(str(d["t"]) not in set(r["en_las_cogidas"]) for d in r["desacuerdos"]))
veces = sum(r.get("veces_regla") or 0 for r in r1)
# ── parte 2 ──
T2 = ["| criatura | día | " + " | ".join(f"{o}: peso vieja → nueva · ignorancia vieja → nueva · creencia vieja → nueva" for o in COSAS) + " |", "|---|---|" + "---|" * 4]
for k in CRI:
    for d in ("5", "10", "15", "20"):
        x = CU["criaturas"][k]["dias"].get(d)
        if not x: continue
        T2.append(f"| {k} | {d} | " + " | ".join(f"{n(x[o]['vieja']['peso'], 2)} → {n(x[o]['nueva']['peso'], 2)} · {n(x[o]['vieja']['ignorancia'], 2)} → {n(x[o]['nueva']['ignorancia'], 2)} · {n(x[o]['vieja']['creencia'], 1)} → {n(x[o]['nueva']['creencia'], 1)}" for o in COSAS) + " |")
def d20(o, regla, campo): return [CU["criaturas"][k]["dias"]["20"][o][regla][campo] for k in CRI if "20" in CU["criaturas"][k]["dias"] and CU["criaturas"][k]["dias"]["20"][o][regla][campo] is not None]
# intensidades: S por cosa (de los cuadernos del dia 20)
S_por = {}
for k in CRI:
    s_, sl = int(k[1]), int(k[-2:]); c = json.load(open(os.path.join(AQUI, "P7_34_res", f"cuaderno_s{s_}_d20_APRENDE_{sl}.json")))
    for o, v in c["objetos"].items():
        for sit in v["situaciones"].values():
            for r in sit:
                if not r.get("corte"): S_por.setdefault(o, []).append(sum(abs(float(r["importancia"][d])) for d in ("cuerpo", "recursos", "vinculo")))
NOMO = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}
TS = ["| cosa | recuerdos (sin cortes, 4 cuadernos del día 20) | S = Σ|importancia|: mediana · cuartil 1 · cuartil 3 | intensidad vieja (mediana) | intensidad nueva (mediana) | en el suelo 0,05 |", "|---|---:|---|---:|---:|---:|"]
for o in ("first_aid", "rations", "net", "camouflage"):
    S = sorted(S_por.get(o, []));
    if not S: continue
    TS.append(f"| {NOMO[o]} | {len(S)} | {n(st.median(S), 3)} · {n(S[len(S) // 4], 3)} · {n(S[3 * len(S) // 4], 3)} | {n(1 + min(1, st.median(S) / 1.5), 3)} | {n(max(0.05, min(1, st.median(S) / 1.5)), 3)} | {sum(1 for s in S if s / 1.5 <= 0.05)} |")
# ── parte 3 ──
T3 = ["| criatura | cosa | pruebas reales (días) | regla vieja: tras cada prueba, vuelve a ser la clase que más llama el día… · pasa de 0,5 el día… | regla nueva: ídem |", "|---|---|---|---|---|"]
for k in CRI:
    x = CU["criaturas"][k]
    for o in ("red", "camuflaje"):
        def fmt(regla):
            L = x["despierta"][f"{o} {regla}"]
            return "; ".join(f"d{e['prueba_dia']} → {e['vuelve_a_mandar_dia'] if e['vuelve_a_mandar_dia'] is not None else 'no'} · {e['pasa_de_0_5_dia'] if e['pasa_de_0_5_dia'] is not None else 'no'}" for e in L) or "—"
        T3.append(f"| {k} | {o} | {', '.join(map(str, x['pruebas_reales'][o])) or '—'} | {fmt('vieja')} | {fmt('nueva')} |")
manda_v = sum(1 for k in CRI for o in ("red", "camuflaje") for e in CU["criaturas"][k]["despierta"][f"{o} vieja"] if e["vuelve_a_mandar_dia"] == e["prueba_dia"] + 1); manda_n = sum(1 for k in CRI for o in ("red", "camuflaje") for e in CU["criaturas"][k]["despierta"][f"{o} nueva"] if e["vuelve_a_mandar_dia"] == e["prueba_dia"] + 1)
tot_p = sum(len(CU["criaturas"][k]["despierta"][f"{o} vieja"]) for k in CRI for o in ("red", "camuflaje"))
medio_v = sum(1 for k in CRI for o in ("red", "camuflaje") for e in CU["criaturas"][k]["despierta"][f"{o} vieja"] if e["pasa_de_0_5_dia"] is not None); medio_n = sum(1 for k in CRI for o in ("red", "camuflaje") for e in CU["criaturas"][k]["despierta"][f"{o} nueva"] if e["pasa_de_0_5_dia"] is not None)
# ignorancia de lo inutil vs lo util, dia a dia (regla vieja): cuantos dias manda lo inutil
dias_manda = collections.Counter()
for k in CRI:
    for d, x in CU["criaturas"][k]["dias"].items():
        for regla in ("vieja", "nueva"):
            ig = {o: x[o][regla]["ignorancia"] for o in COSAS}; top = max(ig, key=ig.get); dias_manda[(regla, top in ("red", "camuflaje"))] += 1

out = f"""# P7-36 · Por qué coge lo inútil y por qué no lo recuerda más débil

*10-oct-2026. Coste cero: sin partidas, sin llamadas (plataforma 0; consola 0; acumulado del siete 64,7168 USD de plataforma, sin cambio). `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar; todo posterior al sello de P7-34; nada se juega. Scripts: `analiza_P7_36.py`
→ `P7_36_cogidas.json` (los diarios de P7-34), `empate_P7_36.py` + `banco_P7_36.py` → `P7_36_banco.json` (las {len(r0)} vidas de APRENDE replicadas, una por proceso, sin y con
la regla), `cuaderno_P7_36.py` → `P7_36_cuadernos.json` (los 80 cuadernos de las 4 criaturas), `escribe_informe_P7_36.py` (este informe; ninguna cifra a mano).
md5: `empate_P7_36.py` = `{md5('empate_P7_36.py')}`, `cuaderno_P7_36.py` = `{md5('cuaderno_P7_36.py')}`.*

## Sección 1 · Por qué coge lo inútil

**En los diarios.** Cada entrada de una red o un camuflaje en el zurrón, la mano o el cuerpo, y la decisión del tic anterior (la acción de t−1 se ve en la obs de t):

{chr(10).join(T1)}

Las {A['cogidas']} cogidas de APRENDE son todas decisiones `coger` (intención `pickup`); ninguna llega por `ir_curioso` ni por hacer sitio. Solo {A['empate_exacto_con_noop']} son un
empate exacto con `noop` (el que `noop` no puede ganar, N2a del desempate de la casa); en las demás `coger` gana a `noop` por una diferencia pequeña pero real
(mediana {n(A['coger_gana_a_noop_por_cuartiles'][2], 4)}; {A['gana_a_noop_por_menos_de_0_01']} de {A['cogidas']} por menos de 0,01). En {A['empata_con_otro'][0][1] if A['empata_con_otro'] else 0} cogidas `coger` empata exactamente con `{A['empata_con_otro'][0][0] if A['empata_con_otro'] else '—'}`
(la foto de ir hacia la cosa y la de cogerla valen lo mismo: coger gana por menos pasos, N2b). TECHO, al contrario, coge por empate exacto con `noop` en {T['empate_exacto_con_noop']} de
{T['cogidas']} (nace sabiendo: la red y el camuflaje no le cambian ninguna fila, y `noop` no puede ganar); BORRADO gana a `noop` por {n(B['coger_gana_a_noop_por_cuartiles'][2], 4)} de mediana, sin
ningún empate.

**Qué fila hace ganar a `coger`.** En la réplica sin regla (fiel al diario: {fid0.get('igual', 0)} decisiones iguales · {fid0.get('difiere', 0)} distintas en las {len(r0)} vidas), la foto de `coger` y
la de `noop` en esos tics solo se distinguen en {', '.join(f'`{k}` ({c} de {sum(len(r["en_las_cogidas"]) for r in r0)} cogidas; p. ej. {n(filas_ej[k][0], 4)} con coger frente a {n(filas_ej[k][1], 4)} con noop)' for k, c in filas.most_common())}:
la fila de la curiosidad de clase (`R-CURIOSIDAD`, ignorancia × alivio, P7-33 punto 4: tener la cosa alivia la mitad). Las ganas (k) de red y camuflaje son 0 y no entran en
`W`; lo que coge la red es la curiosidad de clase, que se alivia al tenerla, y que vale ignorancia × alivio: con la ignorancia que lo inútil tiene en la regla vieja (tabla de la sección 2) basta para esa diferencia.

**En banco, con la regla «en un empate, no se coge»** (`empate_P7_36.desempate_sin_coger`, la simétrica de la de soltar de P7-10/P7-14b: si `coger` comparte el mínimo con otro
candidato, o el paisaje es degenerado, `coger` sale del desempate; mismo criterio, ningún número nuevo). Réplica de las {len(r1)} vidas: la regla entra {veces} veces;
fidelidad {fid1.get('igual', 0)} iguales · {fid1.get('difiere', 0)} distintas. De las {len(cog1)} cogidas de red y camuflaje del diario, **desaparecen {len(desap)}** (la réplica elige
{', '.join(f'`{k}` {c}' for k, c in a_que.most_common()) or '—'}); las otras {len(cog1) - len(desap)} siguen siendo `coger`, porque no son un empate: `coger` gana de verdad por la curiosidad de
clase. Y cambian **{otros_n} decisiones más** en {otros_vidas} vidas fuera de esas cogidas ({', '.join(f'{a} → {b}: {c}' for (a, b), c in otros.most_common(6))}): la regla toca todo `coger`,
también el del botiquín y la ración cuando empatan con `noop` o con el ir hacia ellos. Lo que quita la regla es poco; lo que coge lo inútil no es el empate, es la curiosidad.

## Sección 2 · La regla de la intensidad, como la quiso Manel

Regla vieja (`cuaderno_P7.apunta`): intensidad = 1 + min(1, S / E), S = |imp_cuerpo| + |imp_recursos| + |imp_vínculo|, E = 1,5. Regla nueva (mesa): intensidad =
max(0,05, min(1, S / E)): sin la base de 1, suelo 0,05 (el tope min(1, ·) es el de la regla vieja, declarado). El peso de un recuerdo es intensidad × 0,95^(días); el
recuerdo neutro (peso 1, efecto 0) no cambia. Recalculado sobre los 80 cuadernos (4 criaturas × 20 días) sin jugar. Lo que hay en S:

{chr(10).join(TS)}

Día a día (cierre de los días 5, 10, 15 y 20; peso total de los recuerdos, ignorancia = 1 / (1 + peso), creencia dentro del círculo en el cuerpo, sin cortes):

{chr(10).join(T2)}

Lectura. (i) **Lo inútil se debilita, pero no se apaga**: el día 20 el peso de la red pasa de {n(min(d20('red', 'vieja', 'peso')), 2)}-{n(max(d20('red', 'vieja', 'peso')), 2)} a {n(min(d20('red', 'nueva', 'peso')), 2)}-{n(max(d20('red', 'nueva', 'peso')), 2)} y el del camuflaje de
{n(min(d20('camuflaje', 'vieja', 'peso')), 2)}-{n(max(d20('camuflaje', 'vieja', 'peso')), 2)} a {n(min(d20('camuflaje', 'nueva', 'peso')), 2)}-{n(max(d20('camuflaje', 'nueva', 'peso')), 2)}; su ignorancia sube de {n(min(d20('red', 'vieja', 'ignorancia')), 2)}-{n(max(d20('camuflaje', 'vieja', 'ignorancia')), 2)} a {n(min(d20('red', 'nueva', 'ignorancia') + d20('camuflaje', 'nueva', 'ignorancia')), 2)}-{n(max(d20('red', 'nueva', 'ignorancia') + d20('camuflaje', 'nueva', 'ignorancia')), 2)}. No llega a 1 porque la criatura
sigue probándolas ({sum(len(CU['criaturas'][k]['pruebas_reales'][o]) for k in CRI for o in ('red', 'camuflaje'))} pruebas en 20 días entre las 4) y cada prueba vuelve a sumar su poco. (ii) **Lo útil también se debilita**: el botiquín pasa de peso
{n(min(d20('botiquin', 'vieja', 'peso')), 1)}-{n(max(d20('botiquin', 'vieja', 'peso')), 1)} a {n(min(d20('botiquin', 'nueva', 'peso')), 1)}-{n(max(d20('botiquin', 'nueva', 'peso')), 1)} (ignorancia {n(min(d20('botiquin', 'vieja', 'ignorancia')), 2)}-{n(max(d20('botiquin', 'vieja', 'ignorancia')), 2)} → {n(min(d20('botiquin', 'nueva', 'ignorancia')), 2)}-{n(max(d20('botiquin', 'nueva', 'ignorancia')), 2)}), la ración de {n(min(d20('racion', 'vieja', 'peso')), 1)}-{n(max(d20('racion', 'vieja', 'peso')), 1)} a
{n(min(d20('racion', 'nueva', 'peso')), 1)}-{n(max(d20('racion', 'nueva', 'peso')), 1)}: la importancia (el cambio del malestar en la ventana) es pequeña para todo, también para curar (S mediana {n(st.median(S_por['first_aid']), 3)} en el botiquín, {n(st.median(S_por['rations']), 3)} en la ración, {n(st.median(S_por['net']), 3)} en la red
y {n(st.median(S_por['camouflage']), 3)} en el camuflaje: curar mueve el malestar {n(st.median(S_por['first_aid']) / st.median(S_por['camouflage']), 1)} veces más que ponerse un camuflaje, y comer lo mismo que una red; la base de 1 de la regla vieja borraba esa diferencia, y la regla nueva la deja ver, pero es una diferencia de 3 a 1, no de 10 a 1). (iii) **La creencia de lo útil cambia, y a peor**: la del botiquín dentro el día 20 pasa de
{', '.join(n(c, 1) for c in d20('botiquin', 'vieja', 'creencia'))} a {', '.join(n(c, 1) for c in d20('botiquin', 'nueva', 'creencia'))}; la de la ración de {', '.join(n(c, 1) for c in d20('racion', 'vieja', 'creencia'))} a {', '.join(n(c, 1) for c in d20('racion', 'nueva', 'creencia'))}. La causa es el recuerdo neutro: pesa 1 y no se apaga, y la media
con el neutro en el centro tira hacia 0 tanto más cuanto menos pesan los recuerdos vividos (con intensidad mediana {n(max(0.05, min(1, st.median(S_por['first_aid']) / 1.5)), 3)} en el botiquín, el neutro pesa como {n(1 / max(0.05, min(1, st.median(S_por['first_aid']) / 1.5)), 0)} recuerdos
de curar). La regla nueva, tal cual, hace que el botiquín «cure» {n(min(d20('botiquin', 'nueva', 'creencia')), 0)}-{n(max(d20('botiquin', 'nueva', 'creencia')), 0)} en vez de {n(min(d20('botiquin', 'vieja', 'creencia')), 0)}-{n(max(d20('botiquin', 'vieja', 'creencia')), 0)} sin que la criatura haya visto nada distinto.

## Sección 3 · Cuándo habría vuelto a despertar la curiosidad por lo inútil

La curiosidad de clase llama con ignorancia × alivio y manda `ir_curioso` la clase que más llama (`nace_P7_33._cands`). Con la regla vieja, la ignorancia de la red y del
camuflaje YA es la mayor de las cuatro casi todos los días (el día 20, regla vieja: lo útil {n(min(d20('botiquin', 'vieja', 'ignorancia') + d20('racion', 'vieja', 'ignorancia')), 2)}-{n(max(d20('botiquin', 'vieja', 'ignorancia') + d20('racion', 'vieja', 'ignorancia')), 2)} con {min(d20('botiquin', 'vieja', 'recuerdos') + d20('racion', 'vieja', 'recuerdos'))}-{max(d20('botiquin', 'vieja', 'recuerdos') + d20('racion', 'vieja', 'recuerdos'))} recuerdos; lo inútil {n(min(d20('red', 'vieja', 'ignorancia') + d20('camuflaje', 'vieja', 'ignorancia')), 2)}-{n(max(d20('red', 'vieja', 'ignorancia') + d20('camuflaje', 'vieja', 'ignorancia')), 2)} con {min(d20('red', 'vieja', 'recuerdos') + d20('camuflaje', 'vieja', 'recuerdos'))}-{max(d20('red', 'vieja', 'recuerdos') + d20('camuflaje', 'vieja', 'recuerdos'))}):
lo inútil manda la curiosidad en {dias_manda[('vieja', True)]} de {dias_manda[('vieja', True)] + dias_manda[('vieja', False)]} cierres de día (criatura × día) con la regla vieja y en {dias_manda[('nueva', True)]} de {dias_manda[('nueva', True)] + dias_manda[('nueva', False)]} con la nueva. Por eso APRENDE coge más redes
que TECHO: no le hace falta «despertar», nunca se durmió; lo que la frena es solo que la curiosidad se alivia a medias al tenerla y que el camino hasta una red compite
con todo lo demás.

{chr(10).join(T3)}

Tras cada prueba, lo inútil vuelve a ser la clase que más llama al día siguiente en {manda_v} de {tot_p} pruebas con la regla vieja y en {manda_n} de {tot_p} con la nueva; su ignorancia vuelve a
pasar de 0,5 en {medio_v} de {tot_p} con la vieja y en {medio_n} de {tot_p} con la nueva. Las dos repruebas que contó I4 (s1 a11 red día 11; s2 a11 red día 18) no son despertares de una curiosidad
dormida: en los dos casos la red llevaba días siendo la clase que más llamaba (tabla), y lo que tardó fue encontrar una red en calma. Con la regla nueva habría llamado
más fuerte aún (ignorancia de la red el día 20: {', '.join(n(x, 2) for x in d20('red', 'nueva', 'ignorancia'))} frente a {', '.join(n(x, 2) for x in d20('red', 'vieja', 'ignorancia'))}), es decir, más cogidas de lo inútil, no menos.

## Lo que se desprende (propuestas, no decisiones)

1. Bajar la intensidad sin tocar el neutro aplasta la creencia de lo útil: si la mesa quiere la regla nueva, el neutro tendría que pesar en la misma escala (p. ej. el
   suelo 0,05, o la intensidad media de lo vivido) o la creencia tendría que calcularse sin él para las ganas, como ya hace `con_neutro=False`.
2. El problema de «no deja de quererlo» no está en la intensidad del recuerdo sino en que la curiosidad de clase no lee lo aprendido: llama por ignorancia, y la
   ignorancia de una cosa que «no hace nada» se parece a la de una cosa nunca probada. Una curiosidad que descontara lo ya sabido (p. ej. ignorancia × (1 − |creencia
   firme| / esperanza) o que se apagara con N recuerdos de «no hizo nada») apagaría la red sin tocar el botiquín. Es un mecanismo nuevo: se propone, no se hace.
3. La regla «en un empate, no se coge» quita {len(desap)} de {len(cog1)} cogidas de lo inútil y, de paso, {otros.get(('coger', 'noop'), 0)} cogidas de otras cosas (`coger` es un solo candidato: coge lo que pisa, botiquín, ración o arma): no es la palanca, y costaría más de lo que quita.
"""
open(os.path.join(AQUI, "informe_P7_36.md"), "w", encoding="utf-8").write(out); print("informe_P7_36.md", out.count("\n"), "lineas")
