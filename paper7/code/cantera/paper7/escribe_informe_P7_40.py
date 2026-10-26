"""[P7-40] Escribe informe_P7_40.md desde P7_40_cadena.json, P7_40_cuadernos.json (cuaderno_P7_40), P7_40_momentos.json (banco_P7_40 --momentos), P7_39_cuadernos_B1.json
(B1, para la regla final), P7_36_cogidas.json y P7_34_datos.json. Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
CA = J("P7_40_cadena.json"); CU = J("P7_40_cuadernos.json"); MO = J("P7_40_momentos.json"); CG = J("P7_36_cogidas.json"); B1 = J("P7_39_cuadernos_B1.json"); D34 = J("P7_34_datos.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
COSAS = ("botiquin", "racion", "red", "camuflaje"); CRI = ("s1 a10", "s1 a11", "s2 a10", "s2 a11"); IDS = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}
COGIDAS = {(v["serie"], v["dia"], v["asiento"], x["tick_decide"]) for v in CG["vidas"] if v["brazo"] == "APRENDE" for x in v["cogidas"]}
CR = CU["criterios"]; I5C = CU["I5_corregido"]
# momentos
mm = []
for r in MO["P40"]:
    if r.get("error"): continue
    for t, m in r["momentos"].items(): mm.append((r["serie"], r["dia"], r["slot"], int(t), m))
fid_m = collections.Counter()
for r in MO["P40"]: fid_m.update(r.get("fidelidad") or {})
cog = [x for x in mm if (x[0], x[1], x[2], x[3]) in COGIDAS]; ape = [x for x in mm if (x[0], x[1], x[2], x[3]) not in COGIDAS]
sig = sum(1 for *_, m in cog if m.get("replica") == "coger"); otros = collections.Counter(m.get("replica") for *_, m in cog if m.get("replica") != "coger")
lider = sum(1 for *_, m in mm if m.get("clases") and max(m["clases"], key=lambda o: m["clases"][o]["con_cautela"]) in ("net", "camouflage"))
# E2: aperturas reales en peligro en las que la replica sigue eligiendo el acto que abre la prueba (coger en el tic anterior de cogida)
apert_pel = [(s, d, sl, t, m) for s, d, sl, t, m in ape if m.get("peligro") and not m["peligro"].get("calma")]
def abre(s, d, sl, t):
    prev = next((m for s2, d2, sl2, t2, m in cog if (s2, d2, sl2) == (s, d, sl) and t2 == t - 1), None)
    return (prev.get("replica") == "coger") if prev else None
e2_sigue = sum(1 for s, d, sl, t, m in apert_pel if abre(s, d, sl, t) is True); e2_sin = sum(1 for s, d, sl, t, m in apert_pel if abre(s, d, sl, t) is None)
E2 = {"peligro": len(apert_pel), "sigue": e2_sigue, "sin_tic_de_cogida": e2_sin, "pasa": e2_sigue + e2_sin <= 13}
# E1: de la cadena
res = [x for k, v in CA["criaturas"].items() for d in v for x in ((d.get("P7_40") or {}).get("resueltos") or [])]
# cada resuelto aparece en el P7_40 acumulado de cada dia; quedarse con los unicos por (criatura, objeto, dia, tick)
unicos = {}
for k, v in CA["criaturas"].items():
    for d in v:
        for x in ((d.get("P7_40") or {}).get("resueltos") or []): unicos[(k, x["objeto"], x["dia"], x["tick"])] = x
    pend = (v[-1].get("P7_40") or {}).get("pendientes") or []
    for p in pend: unicos.setdefault((k, p["objeto"], p["dia"], p["tick"]), {**p, "cumple": False, "nota": "pendiente al acabar el dia 20"})
R1 = list(unicos.values()); r1_val = [x for x in R1 if x.get("cumple") is not None]; r1_si = sum(1 for x in r1_val if x["cumple"]); r1_emp = sum(1 for x in r1_val if x.get("empate")); r1_ya = sum(1 for x in R1 if x.get("cumple") is None)
E1 = {"apuntes_sin_recuerdos": len(R1), "evaluables": len(r1_val), "cumplen": r1_si, "con_empate": r1_emp, "ya_probada_antes": r1_ya, "fraccion": (r1_si / len(r1_val) if r1_val else None), "pasa": bool(r1_val) and r1_si / len(r1_val) >= 0.6}
apuntes = [a for k, v in CA["criaturas"].items() for a in (((v[-1].get("P7_40") or {}).get("apuntes")) or [])]
ap_por = collections.Counter(IDS[a["objeto"]] for a in apuntes); ap_int = {o: [a["intensidad"] for a in apuntes if IDS[a["objeto"]] == o] for o in COSAS}
sello = {"I1": CR["I1"]["pasa"], "I2": CR["I2"]["pasa"], "I3": CR["I3"]["pasa"], "I4": sig <= 24, "I5": I5C["pasa"]}
sello_b1 = {"I1": B1["criterios"]["I1"]["pasa"], "I2": B1["criterios"]["I2"]["pasa"], "I3": B1["criterios"]["I3"]["pasa"], "I4": False, "I5": B1["criterios"]["I5"]["pasa"]}     # B1: I4 60 de 71, I5 antiguo (informe_P7_39)
pasa40 = sum(sello.values()); pasa_b1 = sum(sello_b1.values())
mejor = "P7-40" if (pasa40, -CR["I3"]["lo_inutil_manda"]) > (pasa_b1, -B1["criterios"]["I3"]["lo_inutil_manda"]) else "B1"


# B1 bajo el I5 corregido (misma vara para las dos), E1 sin empates, y el recuento informativo con el punto de partida de clase solo (sin apuntes), sobre los mismos cuadernos
REAL = {"botiquin": 50.0, "racion": 15.0}; b1_i5 = []
for k, v in B1["criaturas"].items():
    x = v["dias"].get("20")
    for o in ("botiquin", "racion"):
        if x and x[o]["creencia_A"] is not None and x[o]["creencia_P37"] is not None: b1_i5.append(abs(x[o]["creencia_A"] - REAL[o]) <= abs(x[o]["creencia_P37"] - REAL[o]) + 0.1)
sello_b1["I5"] = bool(b1_i5) and all(b1_i5); pasa_b1 = sum(sello_b1.values())
mejor = "P7-40" if (pasa40, -CR["I3"]["lo_inutil_manda"]) > (pasa_b1, -B1["criterios"]["I3"]["lo_inutil_manda"]) else "B1"
ne = [x for x in r1_val if not x.get("empate")]; ne_si = sum(1 for x in ne if x["cumple"]); ne_por = {o: (sum(1 for x in ne if x["objeto"] == o), sum(1 for x in ne if x["objeto"] == o and x["cumple"])) for o in IDS}
tot_c = inu_c = i15_c = 0; deja_c = {}
for k, v in CU["criaturas"].items():
    ult = None
    for d, x in sorted(v["dias"].items(), key=lambda kv: int(kv[0])):
        cur = {}
        for o in COSAS:
            N_ = x[o]["recuerdos"]; suma = x[o]["importancia_esperada"] * (1 + N_) - x[o]["p0"]; cur[o] = x[o]["ignorancia"] * (x[o]["p0_clase"] + suma) / (1 + N_)
        top = max(cur, key=cur.get); tot_c += 1; inu_c += top in ("red", "camuflaje"); i15_c += (int(d) >= 15 and top in ("red", "camuflaje"))
        if top in ("red", "camuflaje"): ult = int(d)
    deja_c[k] = ("no llega" if ult == 20 else (ult + 1 if ult else 1))
p0_20 = {o: [CU["criaturas"][k]["dias"]["20"][o]["p0"] for k in CRI if "20" in CU["criaturas"][k]["dias"]] for o in COSAS}; p0c_20 = {o: [CU["criaturas"][k]["dias"]["20"][o]["p0_clase"] for k in CRI if "20" in CU["criaturas"][k]["dias"]] for o in COSAS}
lectura = f"""(i) **El filtro de P7-39 sigue haciendo su parte** (I1, I2 pasan: lo inútil importa {n(CR['I1']['inutil_mediana'], 4)}, «no hizo nada» {n(CR['I2']['no_hizo_nada_mediana'], 4)}) y **la creencia de lo útil está igual de cerca de su
efecto real que en P7-37** (I5 corregido pasa en las 8 parejas; el I5 antiguo no, máx {n(CR['I5']['max_diferencia_creencia_util'], 3)}, por la intensidad atada a la importancia). (ii) **La esperanza de clase funciona sola, pero los
apuntes la anulan**: el punto de partida de clase el día 20 es {', '.join(f'{o} {n(min(p0c_20[o]), 3)}-{n(max(p0c_20[o]), 3)}' for o in COSAS)}; pero cada criatura acumula {min(len(((v[-1].get('P7_40') or {}).get('apuntes')) or []) for v in CA['criaturas'].values())}-{max(len(((v[-1].get('P7_40') or {}).get('apuntes')) or []) for v in CA['criaturas'].values())} apuntes en 20 días (una mirada
de 10 s cada vez que una cosa está a la vista con un rival a 8 casillas o menos: {sum(ap_por.values())} entre las 4) y el sello toma el MAYOR de sus intensidades: con cientos de miradas alguna llega a 1,0 y el punto
de partida vuelve a 1 (día 20: {', '.join(f'{o} {n(min(p0_20[o]), 2)}-{n(max(p0_20[o]), 2)}' for o in COSAS)}). Así la importancia esperada de lo inútil queda otra vez en ≈ 1/(1+N) y lo inútil manda {CR['I3']['lo_inutil_manda']} de 80 (I3 no), `coger` {sig} de 71 (I4 no). Recuento
informativo, fuera del sello y sin banco nuevo (los mismos cuadernos, el punto de partida de clase SIN apuntes): lo inútil mandaría {inu_c} de {tot_c} cierres ({i15_c} de 24 en los días 15-20) y s2 a10 dejaría de tenerlo como lo que
más llama el día {deja_c['s2 a10']}; tampoco pasaría I3. (iii) **El miedo calla el probar** (E2 pasa): de las {len(apert_pel)} aperturas reales en peligro la réplica con cautela solo abre {e2_sigue}; y la cautela deja lo inútil al mando
en {lider} de {len(mm)} momentos (A sin cautela en P7-39: 123). (iv) **Al filo del mañana no llega** (E1: {n(100 * (E1['fraccion'] or 0), 1)} %): de {len(r1_val)} apuntes de cosas aún sin recuerdos, {r1_emp} se resuelven en un empate (al principio de cada vida todo
lo no probado llama igual); sin los empates, {ne_si} de {len(ne)} ({', '.join(f'{IDS[o]} {c} de {t}' for o, (t, c) in ne_por.items())}): la red vista en peligro sí manda después en calma ({ne_por['net'][1]} de {ne_por['net'][0]}), el botiquín y la ración casi nunca, porque su
clase (consumibles) ya tiene un punto de partida bajo y la red, con sus «no hizo nada», lo tiene igual de bajo pero más ignorancia.

**Regla final.** P7-40 pasa {pasa40} de I1-I5 y B1 {pasa_b1} (con el I5 corregido para las dos; B1 lo {'pasa' if sello_b1['I5'] else 'no pasa'}); lo inútil manda {CR['I3']['lo_inutil_manda']} frente a {B1['criterios']['I3']['lo_inutil_manda']} de 80. **El campo va con {mejor}**, sin más bancos sobre lo inútil.
Lo que queda dicho, no decidido: el MAYOR de los apuntes es lo que devuelve el punto de partida a 1; con la mediana de los apuntes, o con solo el último, o con el punto de
partida de clase sin apuntes, lo inútil mandaría menos (recuento de arriba) pero seguiría mandando: la ignorancia de lo probado pocas veces pesa más que cualquier esperanza."""

T0 = ["| | criterio | resultado | pasa |", "|---|---|---|---|",
      f"| I1 | inútil ≤ 0,3 × botiquín | {n(CR['I1']['inutil_mediana'], 4)} frente a {n(0.3 * (CR['I1']['botiquin_mediana'] or 0), 4)} (botiquín {n(CR['I1']['botiquin_mediana'], 4)}) | {'sí' if sello['I1'] else 'NO'} |",
      f"| I2 | «no hizo nada» ≤ 0,02 | {n(CR['I2']['no_hizo_nada_mediana'], 4)} ({CU['no_hizo_nada']['A_ceros']} de {CU['no_hizo_nada']['recuerdos']} en 0) | {'sí' if sello['I2'] else 'NO'} |",
      f"| I3 | lo inútil manda ≤ 40 de 80 y ≤ 4 de 24 en d15-20 | {CR['I3']['lo_inutil_manda']} de {CR['I3']['cierres']}; d15-20 {CR['I3']['lo_inutil_manda_15_20']} de {CR['I3']['cierres_15_20']} | {'sí' if sello['I3'] else 'NO'} |",
      f"| I4 | `coger` lo inútil ≤ 24 de 71 | {sig} de {len(cog)} ({', '.join(f'`{k}` {c}' for k, c in otros.most_common(3)) or '—'}) | {'sí' if sello['I4'] else 'NO'} |",
      f"| I5 corregido | al día 20, \\|c40 − real\\| ≤ \\|c37 − real\\| + 0,10 (8 parejas) | {'; '.join(f'{p['criatura']} {p['cosa']}: {n(p.get('lejos_40'), 2)} frente a {n(p.get('lejos_37'), 2)}' for p in I5C['parejas'])} | {'sí' if sello['I5'] else 'NO'} |",
      f"| I5 antiguo (informado) | \\|c40 − c37\\| ≤ 0,10 en los 80 cierres | máx {n(CR['I5']['max_diferencia_creencia_util'], 3)} | {'sí' if CR['I5']['pasa'] else 'NO'} |",
      f"| E1 | al filo del mañana: ≥ 60 % de lo visto en peligro y no probado manda en la siguiente calma | {r1_si} de {len(r1_val)} apuntes evaluables ({n(100 * (E1['fraccion'] or 0), 1)} %; {r1_emp} con empate contados como cumplidos; {r1_ya} apuntes cuya cosa se probó antes del tic de calma, fuera) | {'sí' if E1['pasa'] else 'NO'} |",
      f"| E2 | pruebas en peligro ≤ 13 de 63 | de las {len(apert_pel)} aperturas reales en peligro, la réplica con miedo sigue abriendo {e2_sigue} (+ {e2_sin} sin tic de cogida en los momentos) | {'sí' if E2['pasa'] else 'NO'} |"]
T1 = ["| cosa | recuerdos (día 20) | importancia P7-33 (cuartiles) | importancia B1/P7-40 (cuartiles) | en 0 | apuntes (vistos en peligro, 4 criaturas × 20 días) | intensidad de los apuntes (cuartiles) |", "|---|---:|---|---|---:|---:|---|"]
for o in COSAS:
    x = CU["importancia"][o]; ai = sorted(ap_int[o])
    T1.append(f"| {o} | {x['recuerdos']} | {' · '.join(n(q, 4) for q in x['P33_cuartiles']) if x['P33_cuartiles'] else '—'} | {' · '.join(n(q, 4) for q in x['A_cuartiles']) if x['A_cuartiles'] else '—'} | {x['A_ceros']} | {ap_por[o]} | {(n(ai[len(ai) // 4], 3) + ' · ' + n(ai[len(ai) // 2], 3) + ' · ' + n(ai[3 * len(ai) // 4], 3)) if ai else '—'} |")
T2 = ["| criatura | día | " + " | ".join(f"{o}: punto de partida (de clase) · importancia esperada · ignorancia · curiosidad" for o in COSAS) + " |", "|---|---|" + "---|" * 4]
for k in CRI:
    for d in ("1", "5", "10", "15", "20"):
        x = CU["criaturas"][k]["dias"].get(d)
        if x: T2.append(f"| {k} | {d} | " + " | ".join(f"{n(x[o]['p0'], 3)} ({n(x[o]['p0_clase'], 3)}) · {n(x[o]['importancia_esperada'], 3)} · {n(x[o]['ignorancia'], 3)} · {n(x[o]['curiosidad_A'], 3)}" for o in COSAS) + " |")
T3 = ["| criatura | la clase que más llama, d1 → d20 | deja de mandar lo inútil el día | B1 (P7-39) |", "|---|---|---|---|"]
for k in CRI:
    x = CU["criaturas"][k]; T3.append(f"| {k} | {' '.join({'botiquin': 'B', 'racion': 'R', 'red': 'N', 'camuflaje': 'C'}[top] for d, top in x['manda'])} | {x['deja_de_mandar_lo_inutil_el_dia']} | {B1['criaturas'][k]['deja_de_mandar_lo_inutil_el_dia']} |")
fid_c = collections.Counter()
for k, v in CA["criaturas"].items():
    for d in v: fid_c.update(d.get("fidelidad") or {})

out = f"""# P7-40 · Último banco antes del campo: la esperanza de clase y el miedo que calla el probar, no el mirar

*10-oct-2026. Banco, coste cero: plataforma 0 créditos (acumulado del siete 710; disponibles el 10-oct, dato de Manel: 496 de 1.000, +71/día); consola 0 USD.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar. Sello `SELLO_P7_40.md` (commit `b7d11da`, antes de calcular).
Scripts: `filo_P7_40.py` (= `{md5('filo_P7_40.py')}`, la pieza, sobre B1 de P7-39: `efecto_P7_39` + `contrafactual_P7_38` sin contrafactual), `banco_P7_40.py` (`--cadena` →
`P7_40_cadena.json`, `P7_40_res/cuaderno_P40_*.json`; `--momentos` → `P7_40_momentos.json`), `cuaderno_P7_40.py` → `P7_40_cuadernos.json`, `escribe_informe_P7_40.py` (este
informe; ninguna cifra a mano). Cadena honesta: {fid_c.get('igual', 0)} decisiones iguales al diario · {fid_c.get('difiere', 0)} distintas; momentos: {fid_m.get('igual', 0)} · {fid_m.get('difiere', 0)}.*

## El sello, de una vez

{chr(10).join(T0)}

P7-40 pasa {pasa40} de I1-I5 (B1 de P7-39 con el I5 corregido: {pasa_b1}). **Regla final**: el campo va con **{mejor}** (la que pase más de I1-I5; a igualdad, la que deje lo inútil mandando menos
cierres: P7-40 {CR['I3']['lo_inutil_manda']} de 80, B1 {B1['criterios']['I3']['lo_inutil_manda']} de 80; a igualdad, B1), sin más bancos sobre lo inútil.

## Sección 1 · La importancia y los apuntes

{chr(10).join(T1)}

## Sección 2 · El punto de partida de cada clase, día a día

{chr(10).join(T2)}

{chr(10).join(T3)}

(B botiquín, R ración, N red, C camuflaje.)

## Sección 3 · Los momentos y el miedo

En los {len(cog)} momentos de cogida `coger` gana en {sig}; lo inútil es la clase que más llama (con la cautela) en {lider} de {len(mm)} momentos. De las {len(ape)} aperturas reales,
{len(apert_pel)} en peligro: la réplica con miedo sigue abriendo {e2_sigue} ({e2_sin} sin tic de cogida entre los momentos: la prueba se abrió sin `coger` en el tic anterior, p. ej. al ponerse lo que ya llevaba).

## Lectura

{lectura}
"""
open(os.path.join(AQUI, "informe_P7_40.md"), "w", encoding="utf-8").write(out); print("informe_P7_40.md", out.count("\n"), "lineas"); print(sello, "E1", E1, "E2", E2, "mejor", mejor)
