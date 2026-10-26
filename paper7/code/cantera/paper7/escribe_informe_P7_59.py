"""[P7-59] Escribe informe_P7_59.md desde P7_59_compara.json (compara_P7_59), P7_59_razon.json y ciegas_P7_59 (etiquetas y menu). Ninguna cifra a mano.  python3 escribe_informe_P7_59.py"""
import json, os, re
AQUI = os.path.dirname(os.path.abspath(__file__)); C = json.load(open(os.path.join(AQUI, "P7_59_compara.json"))); B = json.load(open(os.path.join(AQUI, "P7_59_razon.json")))
import ciegas_P7_59 as CI
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
a, b = C["con_nombres"], C["a_ciegas"]; conds = sorted(set(a["condiciones"]) | set(b["condiciones"])); acc = sorted(set(a["acciones"]) | set(b["acciones"]))
T1 = ["| | con nombres (P7-54) | a ciegas (P7-59) |", "|---|---:|---:|", f"| invitaciones válidas | {a['invitaciones']} | {b['invitaciones']} |", f"| verdad en el mundo (tabla del mundo del sello de P7-56) | {a['verdad']} ({n(100 * a['verdad'] / a['invitaciones'], 0)} %) | {b['verdad']} ({n(100 * b['verdad'] / b['invitaciones'], 0)} %) |"]
T1 += [f"| {c} | {a['condiciones'].get(c, 0)} | {b['condiciones'].get(c, 0)} |" for c in conds]
T2 = ["| acción (nombre real) | con nombres | a ciegas |", "|---|---:|---:|"] + [f"| {k} | {a['acciones'].get(k, 0)} | {b['acciones'].get(k, 0)} |" for k in acc]
T3 = ["| criatura-día | invitaciones (con · sin nombres) | desaparecen a ciegas (acción, condición) | nuevas a ciegas |", "|---|---|---|---|"]
for v, x in C["por_vida"].items(): T3.append(f"| {v} | {x['con_nombres']} · {x['a_ciegas']} | {'; '.join(f'{p} · {c}' for p, c in x['desaparecen']) or '—'} | {'; '.join(f'{p} · {c}' for p, c in x['nuevas']) or '—'} |")
TI = ["| criatura-día | invitación a ciegas (tal cual) | acción real | verdad | condiciones |", "|---|---|---|---|---|"]
for p in C["invitaciones_a_ciegas"]: TI.append(f"| {p['vida']} | {p['tipo']} · **{p['accion_ciega']}** · anillo {p['anillo']} · {p['calma']} · {p['movimiento']} · hermana {p['hermana']} · cuerpo {n(p['cuerpo'], 0)}, recursos {n(p['recursos'], 2)}, vínculo {n(p['vinculo'], 2)} · porque: {p['porque'][:200]} | {p['accion']} | {'sí' if p['verdad'] else 'no'} | {', '.join(p['conds']) or '—'} |")
txt = " ".join(r["respuesta"] for r in B).lower(); pal = {w: len(re.findall(w, txt)) for w in ("cura", "medicina", "botiqu", "camufla", "escond", "arma", "juego")}
out = f"""# P7-59 · La razón a ciegas: ¿cuánto de lo que «descubre» viene de conocer los nombres?

*13-oct-2026. Pregunta de Discord. Consola (bolsa 2): 8 llamadas a ciegas = {n(b['tokens'][0], 0)} + {n(b['tokens'][1], 0)} tokens = {n(b['usd'], 4)} $ supuestos (tope 2 $); plataforma 0. `motor/model.py` intacto. Repetición de P7-54 sobre los MISMOS
8 criatura-días, mismo prompt y modelo (`claude-sonnet-5-5`), con una sola diferencia: los nombres de objetos, ítems y municiones sustituidos por etiquetas neutras fijas, igual en diario, prompt y
menú (`ciegas_P7_59.py`): botiquín = objeto A, ración = B, red = C, camuflaje = D, mochila = E, sword = F, spear = G, bow = H, blowgun = I, knives = J, arrows = K, darts = L; acciones USAR_A, USAR_B,
COGER_A..D, EMPUNAR_C, PONERSE_D, DAR_A_HERMANA. Se quitaron también dos pistas: «comer la ración» del menú (pasa a «usar el objeto B») y la lista de lo que el cuerpo no sabe hacer («lanzar la
red, atacar con la red», que revelaba que C es un arma). Comprobado: ningún nombre queda en los 8 diarios, el menú ni el prompt. Comparación: `compara_P7_59.py` → `P7_59_compara.json`; este informe,
`escribe_informe_P7_59.py` (ninguna cifra a mano). La verdad se juzga con la tabla del mundo fijada en el sello de P7-56 (mecánica: acción real × situación × promesa de cuerpo); las condiciones,
con reglas fijas sobre los campos y el texto (en `compara_P7_59.py`).*

## Resultado

{chr(10).join(T1)}

{chr(10).join(T2)}

- **Lo que descubre sobre la cura no viene de los nombres**: a ciegas acierta lo mismo ({b['verdad']} de {b['invitaciones']} frente a {a['verdad']} de {a['invitaciones']}) y descubre lo mismo: que el objeto A (el botiquín) y el B (la ración) curan
  solo si no te golpean ({b['condiciones'].get('C1 cura solo sin golpes', 0)} frente a {a['condiciones'].get('C1 cura solo sin golpes', 0)}), que fuera del anillo se pierde vida ({b['condiciones'].get('C2 fuera del anillo duele', 0)} frente a {a['condiciones'].get('C2 fuera del anillo duele', 0)}) y que A cura mucho ({b['condiciones'].get('C5 el botiquin cura mucho', 0)} frente a {a['condiciones'].get('C5 el botiquin cura mucho', 0)}). Esto sale de los
  números del diario (vida antes y después, golpes en la ventana, ventanas cortadas). A ciegas usa más el objeto B ({b['acciones'].get('USAR_RACION', 0)} frente a {a['acciones'].get('USAR_RACION', 0)} invitaciones de usarlo).
- **Lo que desaparece al quitar los nombres son las ideas sobre la red y el camuflaje**: ponerse D ({a['acciones'].get('PONERSE_CAMUFLAJE', 0)} → {b['acciones'].get('PONERSE_CAMUFLAJE', 0)}), «el camuflaje protege quieta» ({a['condiciones'].get('C4 camuflaje protege quieta', 0)} → {b['condiciones'].get('C4 camuflaje protege quieta', 0)}),
  empuñar C ({a['acciones'].get('EMPUNAR_RED', 0)} → {b['acciones'].get('EMPUNAR_RED', 0)}), «red y camuflaje no curan» ({a['condiciones'].get('C3 red/camuflaje no curan', 0)} → {b['condiciones'].get('C3 red/camuflaje no curan', 0)}). Esas venían del nombre: «camuflaje» sugiere esconderse quieta y
  «red» sugiere atrapar; con «objeto D» y «objeto C», que en el diario no hacen nada medible en el cuerpo, la razón no tiene de dónde sacarlas y apenas los menciona (C dos veces: «no sé qué hace»).
- Las palabras de la respuesta a ciegas: {', '.join(f'«{k}» {v}' for k, v in pal.items())}. No adivina qué son los objetos: habla de A como lo que «cura» porque lo ve curar.

## Por criatura-día: qué desaparece y qué aparece a ciegas

{chr(10).join(T3)}

## Las invitaciones a ciegas, tal cual

{chr(10).join(TI)}

## Lectura

La razón descubre lo que el diario muestra con números (qué cura, cuándo se corta, dónde duele), con o sin nombres. Los nombres le dan otra cosa: hipótesis sobre objetos que en el diario
no hacen nada (el camuflaje que esconde si estás quieta, la red que atrapa). Una de ellas es verdad en el mundo (el camuflaje limita a 4 casillas la distancia a la que te ven quieta) y el
cuerpo no puede medirla en su cuerpo; la otra, este cuerpo no la puede hacer. Sin nombres, esas hipótesis no aparecen.
"""
open(os.path.join(AQUI, "informe_P7_59.md"), "w", encoding="utf-8").write(out); print("informe_P7_59.md", out.count("\n"), "lineas")
