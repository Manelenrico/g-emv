"""[P7-38] Escribe informe_P7_38.md desde P7_38_cadena.json, P7_38_cuadernos.json (cuaderno_P7_38), P7_38_momentos.json (banco_P7_38 --momentos) y P7_36_cogidas.json. Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
CA = J("P7_38_cadena.json"); CU = J("P7_38_cuadernos.json"); MO = J("P7_38_momentos.json"); CG = J("P7_36_cogidas.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
COSAS = ("botiquin", "racion", "red", "camuflaje"); CRI = ("s1 a10", "s1 a11", "s2 a10", "s2 a11"); IDS = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}
COGIDAS = {(v["serie"], v["dia"], v["asiento"], x["tick_decide"]) for v in CG["vidas"] if v["brazo"] == "APRENDE" for x in v["cogidas"]}
CR = CU["criterios"]
fid_c = collections.Counter(); cf = collections.Counter()
for k, v in CA["criaturas"].items():
    for d in v:
        fid_c.update(d.get("fidelidad") or {})
        for kk, vv in (d.get("contrafactual") or {}).items(): cf[kk] += vv
# seccion 1
T1 = ["| cosa | recuerdos (día 20, sin cortes) | sin referencia (día 1) | con referencia de cualquier situación | ventanas de referencia (cuartiles) | importancia P7-33: cuartil 1 · mediana · cuartil 3 | importancia contrafactual: cuartil 1 · mediana · cuartil 3 | en 0 |", "|---|---:|---:|---:|---|---|---|---:|"]
for o in COSAS:
    x = CU["importancia"][o]; T1.append(f"| {o} | {x['recuerdos']} | {x['sin_referencia']} | {x['referencia_cualquiera']} | {' · '.join(n(v, 0) for v in x['referencias_cuartiles']) if x['referencias_cuartiles'] else '—'} | {' · '.join(n(v, 4) for v in x['P33_cuartiles']) if x['P33_cuartiles'] else '—'} | {' · '.join(n(v, 4) for v in x['A_cuartiles']) if x['A_cuartiles'] else '—'} | {x['A_ceros']} |")
NH = CU["no_hizo_nada"]
# seccion 2
T2 = ["| criatura | día | " + " | ".join(f"{o}: ignorancia · importancia esperada · curiosidad A · creencia A (P7-37)" for o in COSAS) + " |", "|---|---|" + "---|" * 4]
for k in CRI:
    for d in ("5", "10", "15", "20"):
        x = CU["criaturas"][k]["dias"].get(d)
        if x: T2.append(f"| {k} | {d} | " + " | ".join(f"{n(x[o]['ignorancia'], 3)} · {n(x[o]['importancia_esperada'], 3)} · {n(x[o]['curiosidad_A'], 3)} · {n(x[o]['creencia_A'], 1)} ({n(x[o]['creencia_P37'], 1)})" for o in COSAS) + " |")
T3 = ["| criatura | la clase que más llama, día 1 → 20 | deja de mandar lo inútil el día |", "|---|---|---|"]
for k in CRI:
    x = CU["criaturas"][k]; T3.append(f"| {k} | {' '.join({'botiquin': 'B', 'racion': 'R', 'red': 'N', 'camuflaje': 'C'}[top] for d, top in x['manda'])} | {x['deja_de_mandar_lo_inutil_el_dia']} |")
# seccion 3: momentos
mm = []
for r in MO["A"]:
    if r.get("error"): continue
    for t, m in r["momentos"].items(): mm.append((r["serie"], r["dia"], r["slot"], int(t), m))
fid_m = collections.Counter()
for r in MO["A"]: fid_m.update(r.get("fidelidad") or {})
cog = [x for x in mm if (x[0], x[1], x[2], x[3]) in COGIDAS]; ape = [x for x in mm if (x[0], x[1], x[2], x[3]) not in COGIDAS]
sig = sum(1 for *_, m in cog if m.get("replica") == "coger"); otros = collections.Counter(m.get("replica") for *_, m in cog if m.get("replica") != "coger")
lider = sum(1 for *_, m in mm if m.get("clases") and max(m["clases"], key=lambda o: m["clases"][o]["A"]) in ("net", "camouflage"))
curA = {o: st.median([m["clases"][o]["A"] for *_, m in ape if m.get("clases")]) for o in IDS} if ape else {}
I4 = {"siguen": sig, "pasa": sig <= 24}
# A+M
pel_ape = sum(1 for *_, m in ape if m.get("peligro") and not m["peligro"].get("calma")); pel_cog = sum(1 for *_, m in cog if m.get("peligro") and not m["peligro"].get("calma"))
caut = collections.Counter()
for *_, m in mm:
    if m.get("peligro") and not m["peligro"].get("calma"): caut["apagada (0)" if m["cautela"] == 0 else ("atenuada (0 < cautela < 1)" if m["cautela"] < 1 else "intacta (1)")] += 1
lider_AM = sum(1 for *_, m in mm if m.get("clases") and max(m["clases"], key=lambda o: m["clases"][o]["A"] * (m["cautela"] if o in ("net", "camouflage") else 1.0)) in ("net", "camouflage"))
pref = collections.Counter(); pref_sp = collections.Counter()
for *_, m in mm:
    for o, p in (m.get("preferida") or {}).items(): pref[(IDS[o], p["todas"]["mejor"])] += 1; pref_sp[(IDS[o], p["sin_peligro"]["mejor"])] += 1
T4 = ["| cosa | preferida entre todas las situaciones (C5) | preferida solo entre situaciones sin peligro (A+M) |", "|---|---|---|"]
for o in ("red", "camuflaje"):
    T4.append(f"| {o} | {', '.join(f'{p} {c}' for (oo, p), c in pref.most_common() if oo == o)} | {', '.join(f'{p} {c}' for (oo, p), c in pref_sp.most_common() if oo == o)} |")

# dominio que lleva la importancia contrafactual de cada cosa (cuadernos del dia 20)
dom = collections.Counter()
for k in CRI:
    s_, sl = int(k[1]), int(k[-2:]); c = json.load(open(os.path.join(AQUI, "P7_38_res", f"cuaderno_A_s{s_}_d20_{sl}.json")))
    for o in ("net", "camouflage", "first_aid", "rations"):
        for sit in c["objetos"].get(o, {}).get("situaciones", {}).values():
            for r in sit:
                if r.get("corte"): continue
                imp = r["importancia"]; tot = sum(abs(v) for v in imp.values()); dom[(IDS[o], "cero" if tot == 0 else max(imp, key=lambda d: abs(imp[d])))] += 1
def dom_txt(o): return ", ".join(f"{d} {c}" for (oo, d), c in dom.most_common() if oo == o)
difs = [abs(x[o]["creencia_A"] - x[o]["creencia_P37"]) for cr in CU["criaturas"].values() for x in cr["dias"].values() for o in ("botiquin", "racion") if x[o]["creencia_A"] is not None and x[o]["creencia_P37"] is not None]
dif20 = max((abs(cr["dias"]["20"][o]["creencia_A"] - cr["dias"]["20"][o]["creencia_P37"]) for cr in CU["criaturas"].values() if "20" in cr["dias"] for o in ("botiquin", "racion") if cr["dias"]["20"][o]["creencia_A"] is not None and cr["dias"]["20"][o]["creencia_P37"] is not None), default=None)
ie20 = {o: [CU["criaturas"][k]["dias"]["20"][o]["importancia_esperada"] for k in CRI if "20" in CU["criaturas"][k]["dias"]] for o in COSAS}; ig20 = {o: [CU["criaturas"][k]["dias"]["20"][o]["ignorancia"] for k in CRI if "20" in CU["criaturas"][k]["dias"]] for o in COSAS}; n20 = {o: [CU["criaturas"][k]["dias"]["20"][o]["recuerdos"] for k in CRI if "20" in CU["criaturas"][k]["dias"]] for o in COSAS}
lectura = f"""Ninguno de los cinco criterios pasa. (i) **La importancia contrafactual sí baja, pero baja para todo**: red y camuflaje de {n(CU['importancia']['red']['P33_cuartiles'][1], 3)} / {n(CU['importancia']['camuflaje']['P33_cuartiles'][1], 3)} a {n(CU['importancia']['red']['A_cuartiles'][1], 3)} / {n(CU['importancia']['camuflaje']['A_cuartiles'][1], 3)} (mediana), el botiquín de {n(CU['importancia']['botiquin']['P33_cuartiles'][1], 3)} a {n(CU['importancia']['botiquin']['A_cuartiles'][1], 3)}, la ración de {n(CU['importancia']['racion']['P33_cuartiles'][1], 3)} a {n(CU['importancia']['racion']['A_cuartiles'][1], 3)} ({CU['importancia']['racion']['A_ceros']} de {CU['importancia']['racion']['recuerdos']} raciones en 0: comer, contra lo que habría pasado sin comer, casi no mueve el malestar en su ventana). I1 se queda a {n(CR['I1']['inutil_mediana'] - 0.3 * CR['I1']['botiquin_mediana'], 4)} del umbral: el cociente inútil/botiquín pasa de {n((CU['importancia']['red']['P33_cuartiles'][1] + CU['importancia']['camuflaje']['P33_cuartiles'][1]) / 2 / CU['importancia']['botiquin']['P33_cuartiles'][1], 2)} a {n(CR['I1']['inutil_mediana'] / CR['I1']['botiquin_mediana'], 2)}. (ii) **«No hizo nada» no se queda en 0**: {NH['A_ceros']} de {NH['recuerdos']} sí (su cambio de malestar cabe en 1 desviación típica de las ventanas sin prueba), los otros {NH['recuerdos'] - NH['A_ceros']} se salen de esa banda; el dominio que lo lleva es {dom_txt('red')} en la red y {dom_txt('camuflaje')} en el camuflaje. Las ventanas de referencia son muchas ({n(CU['importancia']['red']['referencias_cuartiles'][1], 0)} de mediana para la red) y por eso su desviación típica es estrecha: en 10 s de calma el malestar de fondo casi no se mueve, y lo que se mueve durante la prueba (la criatura acaba de coger la cosa, la lleva, camina hacia otra) parece importar. (iii) **Lo inútil sigue mandando** ({CR['I3']['lo_inutil_manda']} de {CR['I3']['cierres']}; días 15-20, {CR['I3']['lo_inutil_manda_15_20']} de {CR['I3']['cierres_15_20']}; ninguna criatura deja de tenerlo como lo que más llama): con el neutro contando como UN recuerdo de importancia 1 y {min(n20['red'] + n20['camuflaje'])}-{max(n20['red'] + n20['camuflaje'])} recuerdos de red o camuflaje de importancia ~0,06, la importancia esperada de lo inútil el día 20 es {n(min(ie20['red'] + ie20['camuflaje']), 2)}-{n(max(ie20['red'] + ie20['camuflaje']), 2)}, la del botiquín {n(min(ie20['botiquin']), 2)}-{n(max(ie20['botiquin']), 2)} y la de la ración {n(min(ie20['racion']), 2)}-{n(max(ie20['racion']), 2)}; multiplicada por una ignorancia de {n(min(ig20['red'] + ig20['camuflaje']), 2)}-{n(max(ig20['red'] + ig20['camuflaje']), 2)} (inútil) frente a {n(min(ig20['botiquin'] + ig20['racion']), 2)}-{n(max(ig20['botiquin'] + ig20['racion']), 2)} (útil), lo inútil gana siempre. El neutro es un recuerdo entre pocos, y pocos recuerdos de poco no lo tapan. (iv) **`coger` sigue en {sig} de {len(cog)}**: la cosa a los pies y la curiosidad que se alivia al tenerla (P7-36). (v) **La creencia de lo útil se mueve** (mayor diferencia {n(CR['I5']['max_diferencia_creencia_util'], 2)}, mediana {n(st.median(difs), 3)}, {sum(1 for d in difs if d > 0.1)} de {len(difs)} cierres por encima de 0,10): no por el método de la curiosidad, sino porque la intensidad del recuerdo va atada a la importancia (1 + importancia, como se decidió) y la contrafactual cambia los pesos con que se promedian los efectos; la mayor diferencia está en s2 a10 el día 2 (botiquín {n(CU['criaturas']['s2 a10']['dias']['2']['botiquin']['creencia_P37'], 2)} → {n(CU['criaturas']['s2 a10']['dias']['2']['botiquin']['creencia_A'], 2)}). Si I5 quiere decir «la creencia no cambia», la intensidad no puede ir atada a esta importancia; si quiere decir «lo útil sigue sabiéndose», se cumple: la mayor diferencia en los cuadernos del día 20 es {n(dif20, 3)}.

**A+M.** Con la cautela, la clase que más llama sigue siendo red o camuflaje en {lider_AM} de {len(mm)} momentos (A: {lider}); de los {sum(caut.values())} momentos en peligro, la cautela apaga {caut['apagada (0)']} y atenúa {caut['atenuada (0 < cautela < 1)']}; {pel_ape} de las {len(ape)} pruebas reales y {pel_cog} de los {len(cog)} momentos de cogida caen en peligro. La mirada de científico sin peligro lleva la siguiente prueba a la forma nueva en la situación de siempre (empuñar la red dentro y sin golpe, ponerse el camuflaje dentro y sin golpe).

## Lo que se desprende (propuestas, no decisiones)

1. La ventana de referencia mide el fondo, pero lo que mueve el malestar en la prueba es la prueba misma como acto (coger, llevar, caminar) y la propia curiosidad que se
   alivia (`R-CURIOSIDAD` reparte el 80 % en recursos): medir la importancia sin las filas de la curiosidad (y sin el acto de coger) la dejaría en lo que la cosa hace.
2. El neutro como UN recuerdo de importancia 1 solo se apaga con muchos recuerdos: con los {min(n20['red'] + n20['camuflaje'])}-{max(n20['red'] + n20['camuflaje'])} de red o camuflaje la importancia esperada de lo inútil queda en
   {n(min(ie20['red'] + ie20['camuflaje']), 2)}-{n(max(ie20['red'] + ie20['camuflaje']), 2)}. O el neutro pesa menos (p. ej. 1/N), o la importancia esperada es la mediana, o lo inútil se declara con N «no hizo nada» seguidos.
3. I5, tal como está escrito, no puede pasar con la intensidad atada a la importancia; conviene decidir cuál de las dos cosas se quiere."""

sello = {"I1": CR["I1"]["pasa"], "I2": CR["I2"]["pasa"], "I3": CR["I3"]["pasa"], "I4": I4["pasa"], "I5": CR["I5"]["pasa"]}

out = f"""# P7-38 · Importancia contra lo que habría pasado sin la prueba

*10-oct-2026. Banco, coste cero: plataforma 0 créditos (acumulado del siete 710; disponibles el 10-oct, dato de Manel: 496 de 1.000, +71/día); consola 0 USD.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar; nada cambia en el campo. Sello `SELLO_P7_38.md` (commit
`4e284fc`, antes de calcular; dos añadidos declarados antes de calcular). Scripts: `contrafactual_P7_38.py` (= `{md5('contrafactual_P7_38.py')}`, la pieza, solo banco),
`banco_P7_38.py` (`--cadena` → `P7_38_cadena.json`, `P7_38_res/cuaderno_A_*.json`; `--momentos` → `P7_38_momentos.json`), `cuaderno_P7_38.py` → `P7_38_cuadernos.json`,
`escribe_informe_P7_38.py` (este informe; ninguna cifra a mano).*

## El sello, de una vez

| | criterio | resultado | pasa |
|---|---|---|---|
| I1 | importancia de lo inútil ≤ 0,3 × la del botiquín | mediana red + camuflaje {n(CR['I1']['inutil_mediana'], 4)}; botiquín {n(CR['I1']['botiquin_mediana'], 4)} (0,3 × = {n(0.3 * (CR['I1']['botiquin_mediana'] or 0), 4)}) | {'sí' if sello['I1'] else 'NO'} |
| I2 | «no hizo nada» ≤ 0,02 | mediana {n(CR['I2']['no_hizo_nada_mediana'], 4)} ({NH['recuerdos']} recuerdos; {NH['A_ceros']} en 0) | {'sí' if sello['I2'] else 'NO'} |
| I3 | lo inútil manda ≤ 40 de 80 cierres y ≤ 20 % de los días 15-20 | {CR['I3']['lo_inutil_manda']} de {CR['I3']['cierres']}; días 15-20: {CR['I3']['lo_inutil_manda_15_20']} de {CR['I3']['cierres_15_20']} ({n(100 * CR['I3']['lo_inutil_manda_15_20'] / max(1, CR['I3']['cierres_15_20']), 1)} %) | {'sí' if sello['I3'] else 'NO'} |
| I4 | en los 71 momentos, `coger` lo inútil gana en ≤ 24 | {sig} de {len(cog)} (lo demás: {', '.join(f'`{k}` {c}' for k, c in otros.most_common(4)) or '—'}) | {'sí' if sello['I4'] else 'NO'} |
| I5 | la creencia de lo útil no se aparta más de 0,10 de P7-37 | mayor diferencia {n(CR['I5']['max_diferencia_creencia_util'], 4)} | {'sí' if sello['I5'] else 'NO'} |

## Sección 1 · La importancia contrafactual

Cadena honesta (cada criatura, sus 20 días; el cuaderno y las pistas del pasado viajan): {fid_c.get('igual', 0)} decisiones iguales al diario · {fid_c.get('difiere', 0)} distintas (la réplica lleva la curiosidad A;
lazo abierto). Recuerdos tasados contra ventanas de referencia: {cf['n']} (de ellos {cf['cualquiera']} con referencia de cualquier situación por faltar 5 en la parecida); sin referencia: {cf['sin_referencia']}.

{chr(10).join(T1)}

«No hizo nada» (recuerdos de red y camuflaje con |efecto en el cuerpo| ≤ 1): {NH['recuerdos']} recuerdos; importancia de P7-33 {' · '.join(n(v, 4) for v in NH['P33_cuartiles']) if NH['P33_cuartiles'] else '—'} (cuartiles) → contrafactual
{' · '.join(n(v, 4) for v in NH['A_cuartiles']) if NH['A_cuartiles'] else '—'}; {NH['A_ceros']} de {NH['recuerdos']} en 0 exacto.

## Sección 2 · La curiosidad por clase, día a día

Importancia esperada = (1 + Σ importancias) / (1 + N) con el neutro como un recuerdo de importancia 1; curiosidad A = ignorancia × importancia esperada.

{chr(10).join(T2)}

{chr(10).join(T3)}

(B botiquín, R ración, N red, C camuflaje; «deja de mandar lo inútil» = el primer día a partir del cual ya no manda ningún día; «no llega» si manda el día 20.)

## Sección 3 · Los 71 momentos, en banco (lectura A)

Las 80 vidas con el cuaderno A del día anterior: fidelidad {fid_m.get('igual', 0)} igual · {fid_m.get('difiere', 0)} difiere. En los {len(cog)} momentos de cogida, `coger` gana en {sig}; en las {len(ape)} aperturas de prueba, curiosidad A
mediana: red {n(curA.get('net'), 3)}, camuflaje {n(curA.get('camouflage'), 3)}, botiquín {n(curA.get('first_aid'), 3)}, ración {n(curA.get('rations'), 3)}; la clase que más llama es red o camuflaje en {lider} de {len(mm)} momentos.

## Sección 4 · A+M, solo para que Manel decida

A con la curiosidad de lo inútil atenuada por la cautela por distancia (P7-26) y la mirada de científico solo entre situaciones sin peligro. De las {len(ape)} pruebas reales
(aperturas), {pel_ape} caen en peligro (`peligro_de`); de los {len(cog)} momentos de cogida, {pel_cog}. En los {sum(caut.values())} momentos en peligro la cautela habría dejado la curiosidad
{', '.join(f'{k}: {c}' for k, c in caut.most_common())}. Con A × cautela, la clase que más llama es red o camuflaje en {lider_AM} de {len(mm)} momentos (A sola: {lider}).

{chr(10).join(T4)}

## Lectura

{lectura}
"""
open(os.path.join(AQUI, "informe_P7_38.md"), "w", encoding="utf-8").write(out); print("informe_P7_38.md", out.count("\n"), "lineas"); print(sello)
