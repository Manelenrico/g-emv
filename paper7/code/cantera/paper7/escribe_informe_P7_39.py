"""[P7-39] Escribe informe_P7_39.md desde P7_39_cadena.json, P7_39_cuadernos_B1.json / _B2.json (cuaderno_P7_39), P7_39_momentos.json (banco_P7_39 --momentos),
P7_38_cuadernos.json (para comparar) y P7_36_cogidas.json. Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
CA = J("P7_39_cadena.json"); CU = {"B1": J("P7_39_cuadernos_B1.json"), "B2": J("P7_39_cuadernos_B2.json")}; MO = J("P7_39_momentos.json"); CG = J("P7_36_cogidas.json"); C38 = J("P7_38_cuadernos.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
COSAS = ("botiquin", "racion", "red", "camuflaje"); CRI = ("s1 a10", "s1 a11", "s2 a10", "s2 a11"); IDS = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}; LECT = ("B1", "B2")
COGIDAS = {(v["serie"], v["dia"], v["asiento"], x["tick_decide"]) for v in CG["vidas"] if v["brazo"] == "APRENDE" for x in v["cogidas"]}


def momentos(var):
    out = []
    for r in MO[var]:
        if r.get("error"): continue
        for t, m in r["momentos"].items(): out.append((r["serie"], r["dia"], r["slot"], int(t), m))
    return out


S = {}
for var in LECT:
    CR = CU[var]["criterios"]; mm = momentos(var); cog = [x for x in mm if (x[0], x[1], x[2], x[3]) in COGIDAS]; ape = [x for x in mm if (x[0], x[1], x[2], x[3]) not in COGIDAS]
    sig = sum(1 for *_, m in cog if m.get("replica") == "coger"); otros = collections.Counter(m.get("replica") for *_, m in cog if m.get("replica") != "coger")
    lider = sum(1 for *_, m in mm if m.get("clases") and max(m["clases"], key=lambda o: m["clases"][o]["A"]) in ("net", "camouflage"))
    curA = {o: st.median([m["clases"][o]["A"] for *_, m in ape if m.get("clases")]) for o in IDS} if ape else {}
    fid_m = collections.Counter(); fid_c = collections.Counter(); cf = collections.Counter()
    for r in MO[var]: fid_m.update(r.get("fidelidad") or {})
    for k, v in CA["criaturas"].items():
        if k.startswith(var):
            for d in v:
                fid_c.update(d.get("fidelidad") or {})
                for kk, vv in (d.get("contrafactual") or {}).items(): cf[kk] += vv
    sello = {"I1": CR["I1"]["pasa"], "I2": CR["I2"]["pasa"], "I3": CR["I3"]["pasa"], "I4": sig <= 24, "I5": CR["I5"]["pasa"]}
    S[var] = {"CR": CR, "cog": len(cog), "sig": sig, "otros": otros, "lider": lider, "mm": len(mm), "curA": curA, "fid_m": fid_m, "fid_c": fid_c, "cf": cf, "sello": sello, "pasa_n": sum(sello.values()), "ape": len(ape)}
# regla de parada
para = all(not (S[v]["sello"]["I1"] and S[v]["sello"]["I3"] and S[v]["sello"]["I4"]) for v in LECT)
mejor = max(LECT, key=lambda v: (S[v]["pasa_n"], -S[v]["CR"]["I3"]["lo_inutil_manda"], v == "B1"))

T0 = ["| | criterio | B1 (sin contrafactual) | pasa | B2 (con contrafactual) | pasa |", "|---|---|---|---|---|---|"]
def fila(k, et, f): T0.append(f"| {k} | {et} | {f('B1')} | {'sí' if S['B1']['sello'][k] else 'NO'} | {f('B2')} | {'sí' if S['B2']['sello'][k] else 'NO'} |")
fila("I1", "inútil ≤ 0,3 × botiquín (medianas, día 20)", lambda v: f"{n(S[v]['CR']['I1']['inutil_mediana'], 4)} frente a {n(0.3 * (S[v]['CR']['I1']['botiquin_mediana'] or 0), 4)} (botiquín {n(S[v]['CR']['I1']['botiquin_mediana'], 4)})")
fila("I2", "«no hizo nada» ≤ 0,02", lambda v: f"{n(S[v]['CR']['I2']['no_hizo_nada_mediana'], 4)} ({CU[v]['no_hizo_nada']['A_ceros']} de {CU[v]['no_hizo_nada']['recuerdos']} en 0)")
fila("I3", "lo inútil manda ≤ 40 de 80 y ≤ 20 % en d15-20", lambda v: f"{S[v]['CR']['I3']['lo_inutil_manda']} de {S[v]['CR']['I3']['cierres']}; d15-20 {S[v]['CR']['I3']['lo_inutil_manda_15_20']} de {S[v]['CR']['I3']['cierres_15_20']}")
fila("I4", "`coger` lo inútil ≤ 24 de 71", lambda v: f"{S[v]['sig']} de {S[v]['cog']} ({', '.join(f'`{k}` {c}' for k, c in S[v]['otros'].most_common(3)) or '—'})")
fila("I5", "creencia útil ± 0,10 frente a P7-37", lambda v: f"máx {n(S[v]['CR']['I5']['max_diferencia_creencia_util'], 3)}")
# importancia por cosa
T1 = ["| cosa | lectura | recuerdos | importancia P7-33 (cuartiles) | importancia nueva (cuartiles) | en 0 |", "|---|---|---:|---|---|---:|"]
for o in COSAS:
    for v in LECT:
        x = CU[v]["importancia"][o]; T1.append(f"| {o} | {v} | {x['recuerdos']} | {' · '.join(n(q, 4) for q in x['P33_cuartiles']) if x['P33_cuartiles'] else '—'} | {' · '.join(n(q, 4) for q in x['A_cuartiles']) if x['A_cuartiles'] else '—'} | {x['A_ceros']} |")
# ignorancia dia 20, dia en que deja de mandar, curiosidad
T2 = ["| criatura | lectura | ignorancia día 20: botiquín · ración · red · camuflaje | importancia esperada día 20: botiquín · ración · red · camuflaje | curiosidad día 20 | la clase que más llama, d1 → d20 | deja de mandar lo inútil el día |", "|---|---|---|---|---|---|---|"]
for k in CRI:
    for v in LECT:
        x = CU[v]["criaturas"][k]; d20 = x["dias"].get("20")
        if not d20: continue
        T2.append(f"| {k} | {v} | {' · '.join(n(d20[o]['ignorancia'], 3) for o in COSAS)} | {' · '.join(n(d20[o]['importancia_esperada'], 3) for o in COSAS)} | {' · '.join(n(d20[o]['curiosidad_A'], 3) for o in COSAS)} | {' '.join({'botiquin': 'B', 'racion': 'R', 'red': 'N', 'camuflaje': 'C'}[top] for d, top in x['manda'])} | {x['deja_de_mandar_lo_inutil_el_dia']} |")
# creencia de la racion por dia
T3 = ["| criatura | creencia de la ración por día, P7-37 / B1 / B2 (días 1, 5, 10, 15, 20) |", "|---|---|"]
for k in CRI:
    cel = []
    for d in ("1", "5", "10", "15", "20"):
        a = CU["B1"]["criaturas"][k]["dias"].get(d); b = CU["B2"]["criaturas"][k]["dias"].get(d)
        cel.append(f"d{d}: {n((a or {}).get('racion', {}).get('creencia_P37'), 1)} / {n((a or {}).get('racion', {}).get('creencia_A'), 1)} / {n((b or {}).get('racion', {}).get('creencia_A'), 1)}")
    T3.append(f"| {k} | {'; '.join(cel)} |")
ig = {v: {o: [CU[v]["criaturas"][k]["dias"]["20"][o]["ignorancia"] for k in CRI if "20" in CU[v]["criaturas"][k]["dias"]] for o in COSAS} for v in LECT}


ie20 = {v: {o: [CU[v]["criaturas"][k]["dias"]["20"][o]["importancia_esperada"] for k in CRI if "20" in CU[v]["criaturas"][k]["dias"]] for o in COSAS} for v in LECT}
n20 = {o: [CU["B1"]["criaturas"][k]["dias"]["20"][o]["recuerdos"] for k in CRI if "20" in CU["B1"]["criaturas"][k]["dias"]] for o in COSAS}
cur20 = {v: {o: [CU[v]["criaturas"][k]["dias"]["20"][o]["curiosidad_A"] for k in CRI if "20" in CU[v]["criaturas"][k]["dias"]] for o in COSAS} for v in LECT}
difs = {v: [abs(x[o]["creencia_A"] - x[o]["creencia_P37"]) for cr in CU[v]["criaturas"].values() for x in cr["dias"].values() for o in ("botiquin", "racion") if x[o]["creencia_A"] is not None and x[o]["creencia_P37"] is not None] for v in LECT}
lectura = f"""**Hallazgo (regla de parada disparada).** El filtro hace lo que se le pidió: sin las filas de la curiosidad ni las del acto, la importancia de la red y del camuflaje se
queda en {n(S['B1']['CR']['I1']['inutil_mediana'], 4)} (B1) y {n(S['B2']['CR']['I1']['inutil_mediana'], 4)} (B2) de mediana frente a {n(S['B1']['CR']['I1']['botiquin_mediana'], 3)} / {n(S['B2']['CR']['I1']['botiquin_mediana'], 3)} del botiquín (I1 pasa en las dos), y «no hizo nada» vale
{n(CU['B1']['no_hizo_nada']['A_cuartiles'][1], 4)} / {n(CU['B2']['no_hizo_nada']['A_cuartiles'][1], 4)} (I2 pasa). El cuerpo ya VE que la red no hace nada. Pero lo inútil sigue mandando la curiosidad en {S['B1']['CR']['I3']['lo_inutil_manda']} de 80 cierres (las dos lecturas) y `coger`
sigue en {S['B1']['sig']} / {S['B2']['sig']} de 71, por el **neutro**: con el neutro contando como UN recuerdo de importancia 1 y {min(n20['red'] + n20['camuflaje'])}-{max(n20['red'] + n20['camuflaje'])} recuerdos de red o camuflaje de importancia ~0, la importancia
esperada de lo inútil el día 20 es {n(min(ie20['B1']['red'] + ie20['B1']['camuflaje']), 3)}-{n(max(ie20['B1']['red'] + ie20['B1']['camuflaje']), 3)} (B1; ≈ 1/(1+N)), la del botiquín {n(min(ie20['B1']['botiquin']), 3)}-{n(max(ie20['B1']['botiquin']), 3)} y la de la ración {n(min(ie20['B1']['racion']), 3)}-{n(max(ie20['B1']['racion']), 3)}; multiplicadas por la ignorancia
({n(min(ig['B1']['red'] + ig['B1']['camuflaje']), 2)}-{n(max(ig['B1']['red'] + ig['B1']['camuflaje']), 2)} lo inútil frente a {n(min(ig['B1']['botiquin'] + ig['B1']['racion']), 2)}-{n(max(ig['B1']['botiquin'] + ig['B1']['racion']), 2)} lo útil), la curiosidad de la red y el camuflaje el día 20 es {n(min(cur20['B1']['red'] + cur20['B1']['camuflaje']), 3)}-{n(max(cur20['B1']['red'] + cur20['B1']['camuflaje']), 3)} y la del botiquín y la ración {n(min(cur20['B1']['botiquin'] + cur20['B1']['racion']), 3)}-{n(max(cur20['B1']['botiquin'] + cur20['B1']['racion']), 3)}:
lo que nunca importó nada sigue llamando más que lo que cura, porque se ha probado menos veces y el neutro de nacimiento no se gasta. El producto ignorancia × importancia
esperada, con este neutro, no puede dar la vuelta: cuando la importancia de lo inútil es 0, su curiosidad es ignorancia / (1 + N), y la ignorancia de lo inútil ({min(n20['red'] + n20['camuflaje'])}-{max(n20['red'] + n20['camuflaje'])} recuerdos)
siempre será mayor que la de lo útil ({min(n20['botiquin'] + n20['racion'])}-{max(n20['botiquin'] + n20['racion'])} recuerdos). I5 no pasa en ninguna (máx {n(S['B1']['CR']['I5']['max_diferencia_creencia_util'], 2)} / {n(S['B2']['CR']['I5']['max_diferencia_creencia_util'], 2)}; mediana de las diferencias {n(st.median(difs['B1']), 3)} / {n(st.median(difs['B2']), 3)}) por la intensidad atada a la importancia, como en P7-38;
la creencia de la ración por día (tabla) se mueve en décimas. Según la regla de parada, no se ajusta más y el campo va con **{mejor}** ({S[mejor]['pasa_n']} de 5; a igualdad con la otra, la más simple).

Lo que queda dicho, no decidido: el neutro de importancia 1 es lo único que mantiene viva la curiosidad por lo inútil; una curiosidad que lo gastara con cada prueba sin fruto
(neutro de peso 1/N, o «no hizo nada» como evidencia negativa que resta) cerraría el círculo; es un mecanismo nuevo y no entra en este sello."""

out = f"""# P7-39 · Último intento sobre lo inútil: la importancia mide solo el efecto del objeto

*10-oct-2026. Banco, coste cero: plataforma 0 créditos (acumulado del siete 710; disponibles el 10-oct, dato de Manel: 496 de 1.000, +71/día); consola 0 USD.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar; nada cambia en el campo. Sello `SELLO_P7_39.md` (commit
`a536ff6`, antes de calcular). Scripts: `efecto_P7_39.py` (= `{md5('efecto_P7_39.py')}`: el filtro de filas), `contrafactual_P7_38.py` (= `{md5('contrafactual_P7_38.py')}`, con el mando
`GEMV_P7_38_CONTRA` para B1), `banco_P7_39.py` (`--cadena` → `P7_39_cadena.json`, `P7_39_res/cuaderno_B1_*.json`, `cuaderno_B2_*.json`; `--momentos` → `P7_39_momentos.json`),
`cuaderno_P7_39.py` → `P7_39_cuadernos_B1.json`, `_B2.json`, `escribe_informe_P7_39.py` (este informe; ninguna cifra a mano).*

## El sello, de una vez (B1 y B2)

{chr(10).join(T0)}

B1 pasa {S['B1']['pasa_n']} de 5; B2 pasa {S['B2']['pasa_n']} de 5. **Regla de parada**: {'ni B1 ni B2 pasan I1, I3 e I4 a la vez: no se ajusta más; se declara como hallazgo y el campo va con la mejor de las dos, **' + mejor + '**' if para else 'una de las dos pasa I1, I3 e I4: ' + mejor}
(criterio del sello: la que pase más de los cinco; a igualdad, la que deje lo inútil mandando menos cierres; a igualdad, B1).

## Sección 1 · La importancia sin el acto

Filtro (`efecto_P7_39`): del cambio de malestar salen `R-CURIOSIDAD`, `R-CURIOSIDAD-CUANTO`, `R-ACOPIO`, `R-CARENCIA`, `S-PROVISION` y `R-LLAMADA`. Cadenas honestas:
B1 {S['B1']['fid_c'].get('igual', 0)} iguales · {S['B1']['fid_c'].get('difiere', 0)} distintas; B2 {S['B2']['fid_c'].get('igual', 0)} · {S['B2']['fid_c'].get('difiere', 0)} (B2: {S['B2']['cf']['n']} recuerdos tasados contra referencias, {S['B2']['cf']['cualquiera']} con referencia de cualquier situación, {S['B2']['cf']['sin_referencia']} sin referencia).

{chr(10).join(T1)}

«No hizo nada» (red y camuflaje con |efecto cuerpo| ≤ 1): B1 {CU['B1']['no_hizo_nada']['A_ceros']} de {CU['B1']['no_hizo_nada']['recuerdos']} en 0 (mediana {n(CU['B1']['no_hizo_nada']['A_cuartiles'][1], 4)}); B2 {CU['B2']['no_hizo_nada']['A_ceros']} de {CU['B2']['no_hizo_nada']['recuerdos']} (mediana {n(CU['B2']['no_hizo_nada']['A_cuartiles'][1], 4)}). En P7-38 (sin el filtro) eran {C38['no_hizo_nada']['A_ceros']} de {C38['no_hizo_nada']['recuerdos']} (mediana {n(C38['no_hizo_nada']['A_cuartiles'][1], 4)}).

## Sección 2 · Quién manda, día a día

{chr(10).join(T2)}

(B botiquín, R ración, N red, C camuflaje.) Ignorancia al día 20: lo inútil {n(min(ig['B1']['red'] + ig['B1']['camuflaje']), 2)}-{n(max(ig['B1']['red'] + ig['B1']['camuflaje']), 2)} (B1), {n(min(ig['B2']['red'] + ig['B2']['camuflaje']), 2)}-{n(max(ig['B2']['red'] + ig['B2']['camuflaje']), 2)} (B2); lo útil {n(min(ig['B1']['botiquin'] + ig['B1']['racion']), 2)}-{n(max(ig['B1']['botiquin'] + ig['B1']['racion']), 2)} (B1), {n(min(ig['B2']['botiquin'] + ig['B2']['racion']), 2)}-{n(max(ig['B2']['botiquin'] + ig['B2']['racion']), 2)} (B2).

{chr(10).join(T3)}

## Sección 3 · Los 71 momentos, en banco

B1: fidelidad {S['B1']['fid_m'].get('igual', 0)} · {S['B1']['fid_m'].get('difiere', 0)}; `coger` en {S['B1']['sig']} de {S['B1']['cog']}; en las {S['B1']['ape']} aperturas, curiosidad mediana red {n(S['B1']['curA'].get('net'), 3)}, camuflaje {n(S['B1']['curA'].get('camouflage'), 3)}, botiquín {n(S['B1']['curA'].get('first_aid'), 3)}, ración {n(S['B1']['curA'].get('rations'), 3)}; lo inútil es la clase que más llama en {S['B1']['lider']} de {S['B1']['mm']} momentos.
B2: fidelidad {S['B2']['fid_m'].get('igual', 0)} · {S['B2']['fid_m'].get('difiere', 0)}; `coger` en {S['B2']['sig']} de {S['B2']['cog']}; curiosidad mediana red {n(S['B2']['curA'].get('net'), 3)}, camuflaje {n(S['B2']['curA'].get('camouflage'), 3)}, botiquín {n(S['B2']['curA'].get('first_aid'), 3)}, ración {n(S['B2']['curA'].get('rations'), 3)}; lo inútil manda en {S['B2']['lider']} de {S['B2']['mm']}.

## Lectura

{lectura}
"""
open(os.path.join(AQUI, "informe_P7_39.md"), "w", encoding="utf-8").write(out); print("informe_P7_39.md", out.count("\n"), "lineas"); print({v: S[v]["sello"] for v in LECT}, "para", para, "mejor", mejor)
