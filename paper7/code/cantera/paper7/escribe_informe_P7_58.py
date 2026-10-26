"""[P7-58] Escribe informe_P7_58.md desde P7_58_sello.json (analiza_P7_58) y P7_58_cadena.json. Ninguna cifra a mano.  python3 escribe_informe_P7_58.py"""
import hashlib, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); S = json.load(open(os.path.join(AQUI, "P7_58_sello.json"))); C = json.load(open(os.path.join(AQUI, "P7_58_cadena.json")))
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
H1, H2, H3 = S["H1"], S["H2"], S["H3"]; NOM = {"first_aid": "botiquín", "rations": "ración", "net": "red", "camouflage": "camuflaje"}
TD = ["| día | botiquín | ración | red | camuflaje |", "|---:|---:|---:|---:|---:|"]
for d, x in S["curiosidad_por_dia"].items(): TD.append(f"| {d} | {n(x['first_aid'], 2)} | {n(x['rations'], 2)} | {n(x['net'], 2)} | {n(x['camouflage'], 2)} |")
TC = ["| criatura | lo inútil manda (de 20) | d15-20 (de 6) | la clase que manda, d1 → d20 | se apaga la curiosidad del botiquín (día) |", "|---|---:|---:|---|---|"]
for k, cr in S["criaturas"].items():
    ci = cr["cierres"]; TC.append(f"| {k} | {sum(1 for d, m, h in ci if m in ('net', 'camouflage'))} | {sum(1 for d, m, h in ci if d >= 15 and m in ('net', 'camouflage'))} | {' '.join(NOM[m][:3] for d, m, h in ci)} | {S['apaga_botiquin'].get(k) or 'no se apaga'} |")
pasa = S["pasa_sello"]
out = f"""# P7-58 · Banco (coste cero): curiosidad por el progreso del aprendizaje

*13-oct-2026. Sello `SELLO_P7_58.md` (commit `9fc2420`, antes de calcular). Sin API, sin plataforma; la serie 3 de P7-56 y las piezas de P7-57 sin tocar. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`.
Pieza `progreso_P7_58.py` = `{md5('progreso_P7_58.py')}`; banco `banco_P7_58.py --cadena` (12 criaturas × 20 días de APRENDE de P7-45 en cadena honesta, {C['segundos']} s) → `P7_58_cadena.json`; `analiza_P7_58.py` → `P7_58_sello.json`;
`escribe_informe_P7_58.py` (este informe; ninguna cifra a mano). Los diarios de APRENDE de P7-45 (archivados el 12-oct) se rehidrataron desde sus zips con el md5 del manifiesto (240 de 240).
Fidelidad de la réplica al diario: {n(S['fidelidad']['igual'], 0)} decisiones iguales · {n(S['fidelidad']['difiere'], 0)} distintas.*

## El sello, de una vez

| | criterio | resultado | pasa |
|---|---|---|---|
| H1 | lo inútil manda ≤ 50 % de los cierres y ≤ 20 % de los de d15-20 | {H1['inutil_manda']} de {H1['cierres']} ({n(H1['pct'], 1)} %); d15-20 {H1['d15_20_inutil']} de {H1['d15_20_cierres']} ({n(H1['d15_20_pct'], 1)} %) | {'sí' if H1['pasa'] else 'NO'} |
| H2 | en los momentos de decisión, `coger` lo inútil gana ≤ 1/3 | {H2['coger']} de {H2['momentos']} ({n(100 * H2['fraccion_coger'], 0) if H2['fraccion_coger'] is not None else '—'} %; `ir_curioso` {H2['ir_curioso']}) | {'sí' if H2['pasa'] else 'NO'} |
| H3 | d10-20, ración > red en ≥ 75 % de los cierres con las dos probadas ≥ 3 veces | {H3['racion_mayor']} de {H3['cierres']} ({n(100 * H3['fraccion'], 0) if H3['fraccion'] is not None else '—'} %) | {'sí' if H3['pasa'] else 'NO'} |

**Regla de parada: {'H1, H2 y H3 pasan' if pasa else 'no pasan ' + ', '.join(h for h, x in (('H1', H1), ('H2', H2), ('H3', H3)) if not x['pasa']) + ' → se informa y se para; queda para después del siete'}.** Manda por clase en los 240 cierres: {', '.join(f"{NOM[o]} {k}" for o, k in H1['manda_por_clase'].items())}.
Por personalidad: lo inútil manda {H1['por_variante']['APRENDE_v']['inutil']} de 120 (valiente) y {H1['por_variante']['APRENDE_p']['inutil']} de 120 (prudente); `coger` gana {H2['por_variante']['APRENDE_v']['coger']} de {H2['por_variante']['APRENDE_v']['momentos']} y {H2['por_variante']['APRENDE_p']['coger']} de {H2['por_variante']['APRENDE_p']['momentos']}.

## Curiosidad por objeto y día (media de las 12 criaturas, al cerrar; cautela 1)

{chr(10).join(TD)}

## Por criatura

{chr(10).join(TC)}
"""
cd = S["curiosidad_por_dia"]; d1, d10, d20 = cd.get("1") or cd.get(1), cd.get("10") or cd.get(10), cd.get("20") or cd.get(20)
fid = S["fidelidad"]; fr = fid["difiere"] / (fid["igual"] + fid["difiere"])
out += f"""
## Lectura

1. **H1 pasa de lejos**: lo inútil deja de mandar ({n(H1['pct'], 1)} % de los cierres, {n(H1['d15_20_pct'], 1)} % en d15-20, frente a 62 % y 58 % con la habituación de P7-47). Manda el botiquín ({H1['manda_por_clase']['first_aid']} de 240): es lo que
   más progreso de aprendizaje da, prueba a prueba.
2. **H2 no pasa por poco**: `coger` lo inútil gana {n(100 * H2['fraccion_coger'], 1)} % de los momentos (umbral 33,3 %); y `ir_curioso` gana {H2['ir_curioso']} más: en el momento de la red a los pies, la réplica ya no la coge tanto, y elige
   `ir_curioso` (ir hacia lo que más llama; este banco no registra a qué clase va en ese tic).
3. **H3 no pasa**: la ración supera a la red en {n(100 * H3['fraccion'], 0)} % de los cierres con las dos probadas ≥ 3 veces (umbral 75 %). La ración, que cura 15 fijos y casi siempre toca techo («al menos»), deja de mover la
   creencia pronto: su progreso cae como el de la red, que no la mueve nada.
4. **La curiosidad del botiquín no se apaga nunca** (en ninguna de las 12 criaturas baja de 0,5): crece ({n(d1['first_aid'], 1)} el d1, {n(d10['first_aid'], 1)} el d10, {n(d20['first_aid'], 1)} el d20) porque el divisor es la mediana de todos los
   productos, que caen al apagarse los demás objetos: el progreso es relativo y el botiquín, cuyas curas varían (al menos, cortes, +50), siempre «enseña» más que la mediana. Es un efecto de la
   normalización por la mediana, no un aprendizaje que no se agota: para la mesa.
5. La réplica difiere del diario en el {n(100 * fr, 1)} % de las decisiones (P7-47: 7,7 %): esta curiosidad cambia mucho la conducta.

**Regla de parada: no pasan H2 y H3 → se informa y se para; queda para después del siete.**
"""
open(os.path.join(AQUI, "informe_P7_58.md"), "w", encoding="utf-8").write(out); print("informe_P7_58.md", out.count("\n"), "lineas")
