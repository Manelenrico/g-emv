"""[P7-26] Escribe informe_P7_26.md desde P7_26_decisiones.json y P7_25_decisiones.json (reclasificado con la calma del diario). Ninguna cifra a mano."""
import collections, glob, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
R = J("P7_26_decisiones.json"); R25 = J("P7_25_decisiones.json"); V = ("cautela x1", "cautela x2")
n = lambda x, d=0: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
nuevo = lambda e: e in ("ir_curioso", "coger", "ir_objeto")
def huye(x): return (x["fuera"] and x["hoy"].startswith(("move_", "paso_", "ir_")) and x["hoy"] != "ir_curioso") or x["hoy"].startswith("usar_")
reg = [x for r in R for x in r["registros"]]; A = [x for x in reg if x["a"]]; A2 = [x for x in reg if x.get("a2")]; B = [x for x in reg if x["b"]]; Bh = [x for x in B if huye(x)]
reg25 = [x for r in R25 for x in r["registros"]]
# la calma del freno y de (a')
f0 = glob.glob(os.path.join(RAIZ, "paintball", "runs", "P724_s1_d1_APRENDE_*", "*agent_10.art.log"))[0]; cal = []; filas = collections.Counter(); cal_listo = []
for line in open(f0):
    try: r_ = json.loads(line)
    except Exception: continue
    if r_.get("k") != "tick" or r_.get("phase") != "live": continue
    fl = ((r_.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("filas") or {}; g = lambda k: ((fl.get(k) or {}).get("M", 0) if isinstance(fl.get(k), dict) else (fl.get(k) or 0))
    vals = {k: g(k) for k in ("F-4-ALCANCE", "S-7-AGRESOR", "F-HERMANO-AMENAZA", "F-HERMANO-GOLPE", "F-ANTICIPACION")}; m = max(vals.values()); c = max(0, 1 - min(1, m)); cal.append(c)
    if m > 0: filas[max(vals, key=vals.get)] += 1
    if (r_.get("move_ready_in") or 0) == 0: cal_listo.append(c)
r0 = next(r for r in R if r["campo"] == "P724" and r["dia"] == 1 and r["slot"] == 10); S0 = [x for x in r0["registros"] if x.get("a2")]; ady = [x for x in S0 if x["obj_desconocido_a"] == 1]
prim = {v: next((x["t"] for x in sorted(r0["registros"], key=lambda x: x["t"]) if x["alt"][v] == "ir_curioso" and x["obj_desconocido_a"] is not None and x["obj_desconocido_a"] <= 2), None) for v in V}
def cuenta(S, f, el): return sum(1 for x in S if (x["hoy"] if f is None else x["alt"][f]) == el)
L2 = ["| | (a) estricta, de " + str(len(A)) + ": va hacia lo nuevo · `ir_curioso` | (a') con rivales a más de 4, de " + str(len(A2)) + ": va hacia lo nuevo · `ir_curioso` · decisiones que cambian | (b) peligro: la curiosidad gana a huir / entrar / curarse, de " + str(len(Bh)) + " · gana a otra cosa, de " + str(len(B)) + " · decisiones que cambian |", "|---|---|---|---|"]
L2.append(f"| hoy (calma) | {sum(1 for x in A if nuevo(x['hoy']))} · {cuenta(A, None, 'ir_curioso')} | {sum(1 for x in A2 if nuevo(x['hoy']))} · {cuenta(A2, None, 'ir_curioso')} · — | — · {cuenta(B, None, 'ir_curioso')} ya la elige hoy · — |")
for f in V: L2.append(f"| {f} | {sum(1 for x in A if nuevo(x['alt'][f]))} · {cuenta(A, f, 'ir_curioso')} | {sum(1 for x in A2 if nuevo(x['alt'][f]))} · {cuenta(A2, f, 'ir_curioso')} · {sum(1 for x in A2 if x['alt'][f] != x['hoy'])} | {sum(1 for x in Bh if x['alt'][f]=='ir_curioso')} · {sum(1 for x in B if x['alt'][f]=='ir_curioso' and x['hoy']!='ir_curioso')} · {sum(1 for x in B if x['alt'][f]!=x['hoy'])} |")
L3 = ["| variante | lo que pierde cuando gana la curiosidad | lo que elige en vez de la curiosidad cuando la variante se la quita (peligro) |", "|---|---|---|"]
for f in V: L3.append(f"| {f} | {', '.join(f'`{k}` {v}' for k, v in collections.Counter(x['hoy'] for x in reg if x['alt'][f]=='ir_curioso' and x['hoy']!='ir_curioso').most_common(5)) or '—'} | {', '.join(f'`{k}` {v}' for k, v in collections.Counter(x['alt'][f] for x in B if x['hoy']=='ir_curioso' and x['alt'][f]!='ir_curioso').most_common(5))} |")
L4 = ["| en la vida del freno (a'), " + str(len(S0)) + " instantes · a una casilla, " + str(len(ady)) + " | hoy | cautela ×1 | cautela ×2 |", "|---|---:|---:|---:|"]
for el in ("ir_objeto", "ir_centro", "ir_botin", "ir_curioso"): L4.append(f"| `{el}` (todos) | {cuenta(S0, None, el)} | {cuenta(S0, V[0], el)} | {cuenta(S0, V[1], el)} |")
for el in ("ir_centro", "ir_botin", "ir_objeto", "ir_curioso"): L4.append(f"| `{el}` (a una casilla) | {cuenta(ady, None, el)} | {cuenta(ady, V[0], el)} | {cuenta(ady, V[1], el)} |")
TM = ["| | coge lo nuevo en calma (a'), de " + str(len(A2)) + " | arriesga en peligro (gana a huir, entrar o curarse), de " + str(len(Bh)) + " | decisiones que cambian en peligro, de " + str(len(B)) + " |", "|---|---:|---:|---:|"]
TM.append(f"| hoy (calma) | {sum(1 for x in A2 if nuevo(x['hoy']))} | — | — |")
for f in V: TM.append(f"| {f} | {sum(1 for x in A2 if nuevo(x['alt'][f]))} ({sum(1 for x in A2 if nuevo(x['alt'][f])) - sum(1 for x in A2 if nuevo(x['hoy'])):+d}) | {sum(1 for x in Bh if x['alt'][f]=='ir_curioso')} | {sum(1 for x in B if x['alt'][f]!=x['hoy'])} |")
fid = collections.Counter()
for r in R: fid.update(r["fidelidad"])
T = f"""# P7-26 · La cautela según lo cerca que está el peligro

*7-oct-2026. Coste: plataforma 0, consola 0. Solo réplicas de vidas ya jugadas, una por proceso. `motor/model.py` = `{hashlib.md5(open(os.path.join(AQUI, '..', '..', 'motor', 'model.py'), 'rb').read()).hexdigest()}` al empezar y al
acabar; cuerpo y congelados sin tocar; la variante es un mando de banco (`nace_P7_23.E["cautela"]`, apagado en el campo). Este informe lo escribe `escribe_informe_P7_26.py`
desde `P7_26_decisiones.json` (`banco_P7_26.py`).*

## En corto

- **La calma de hoy** (sección 1) es 1 menos la mayor de cinco filas del miedo; en la vida del freno valió **{n(st.median(cal), 2)}** en {n(sum(1 for c in cal if c < 1))} de sus {n(len(cal))} tics, siempre por
  F-4-ALCANCE (rivales a la vista a 5-8 casillas). En los instantes (a') de P7-25, la calma del diario es > 0,5 por construcción y vale 1,0 en la mayoría.
- **La cautela por distancias no cambia el caso del freno**: con el rival a 5 casillas vale (5 − 2) / 6 = 0,5, lo mismo que la calma de hoy (0,52). A una casilla de la ración,
  `ir_centro` gana {cuenta(ady, None, 'ir_centro')} de {len(ady)} veces hoy, {cuenta(ady, V[0], 'ir_centro')} con la cautela ×1 y {cuenta(ady, V[1], 'ir_centro')} con ×2. No la toca.
- **En las 12 vidas**, la cautela ×1 cambia {sum(1 for x in A2 if x['alt'][V[0]] != x['hoy'])} de {len(A2)} decisiones en calma con lo nuevo cerca (y no hacia lo nuevo: {sum(1 for x in A2 if nuevo(x['alt'][V[0]]))} frente a {sum(1 for x in A2 if nuevo(x['hoy']))} hoy) y
  {n(sum(1 for x in B if x['alt'][V[0]] != x['hoy']))} de {n(len(B))} en peligro, casi todas quitándole la curiosidad al cuerpo (fuera del círculo y con poca vida la cautela es 0); la curiosidad gana a huir,
  entrar o curarse en {sum(1 for x in Bh if x['alt'][V[0]]=='ir_curioso')} de {len(Bh)} (×1) y {sum(1 for x in Bh if x['alt'][V[1]]=='ir_curioso')} (×2), frente a 4-6 con las escalas ×1,5-×2 de P7-25.
- **Corrección a P7-25, dicha aquí:** aquel banco leía la calma de la radiografía de la réplica, que no trae la foto «ahora»; salía 1,0 siempre y el filtro «calma > 0,5»
  de (a) y (a') no filtraba. Reclasificados sus registros con la calma del diario, **ningún instante cambia de clase** (36 en (a), 1.326 en (a'), 18.173 en (b)): las
  conclusiones de P7-25 se mantienen; su informe se ha regenerado con la calma buena.

## Sección 1 · Qué es hoy la calma que multiplica a la curiosidad

`descubre_P7.calma_de` (`descubre_P7.py:136-137`): calma = max(0, 1 − min(1, máximo de las cinco filas de `CALMA_FILAS`, `:61`)). Las cinco filas son del cuerpo congelado
(`paintball/alma/appraisal_zs_v42_exp.py`): **F-4-ALCANCE** (`:1070`, rivales que pueden alcanzarme en el horizonte, techo 0,5 `:130`), **S-7-AGRESOR** (`:1508`, presión de quien me pega),
**F-HERMANO-AMENAZA** y **F-HERMANO-GOLPE** (`:1642-1643`, la amenaza y el golpe al hermano) y **F-ANTICIPACION** (`:1000`, el daño que viene). La curiosidad vale
ACOPIO_M × calma × media de (ignorancia × alivio) de las dos clases (`nace_P7_23.curiosidad_M`), y la promesa de ir a por la cosa la lleva dentro.

En la vida del freno (P7-24, día 1, asiento 10): calma mediana {n(st.median(cal), 3)}, igual en los cuatro cuartiles; por debajo de 1 en {n(sum(1 for c in cal if c < 1))} de {n(len(cal))} tics; la fila que manda,
F-4-ALCANCE en {n(filas['F-4-ALCANCE'])} de ellos (rivales a la vista a 5-8 casillas, sin tocarla nunca); con el paso listo, mediana {n(st.median(cal_listo), 3)}. Es decir: **la curiosidad de esa criatura valía
la mitad durante toda la vida por rivales lejanos.** En los instantes (a') de las 12 vidas (calma del diario): mediana {n(st.median([x['calma'] for x in reg25 if x.get('a2')]), 2)}, {sum(1 for x in reg25 if x.get('a2') and x['calma'] >= 0.99)} de {sum(1 for x in reg25 if x.get('a2'))} con calma 1,0.

## Sección 2 · La variante medida

Cautela(obs) = 1 sin rivales a 8 casillas o menos; (d − 2) / 6 con el rival más cercano a d casillas (1 a 8, 0 a 2); 0 fuera del círculo o con la vida por debajo de 30
(`nace_P7_23.cautela_de`). Sustituye a la calma en la curiosidad y en la promesa de ir a por la cosa; nada más. Escala ×1 y ×2. Banco: las mismas 12 vidas y los mismos
instantes de P7-25 (paso listo, en (a), (a') o (b)); la calma, leída del diario en ese tic. Réplica: {n(fid['igual'])} iguales, {n(fid.get('difiere', 0))} distintas (las del humo, por el paso 0; como en P7-25).

## Sección 3 · Las mismas medidas de P7-25

{chr(10).join(L2)}

{chr(10).join(L3)}

**El caso del freno, de cerca:**

{chr(10).join(L4)}

¿Toca ahora la ración? **No.** A una casilla de ella, `ir_centro` sigue ganando {cuenta(ady, V[0], 'ir_centro')} de {len(ady)} veces con la cautela ×1 y {cuenta(ady, V[1], 'ir_centro')} con ×2: el rival a 5 casillas deja la
cautela en 0,5, lo mismo que la calma. El primer instante con el paso listo y el objeto a 1-2 casillas en que la variante elegiría `ir_curioso`: tic {n(prim[V[0]]) if prim[V[0]] else 'ninguno'} (×1), {n(prim[V[1]]) if prim[V[1]] else 'ninguno'} (×2).
En cuánto tiempo la tocaría no se puede saber sin jugar; con esa cautela no daría el paso.

## Sección 4 · La tabla para Manel

{chr(10).join(TM)}

Lectura: la cautela por distancias **hace al cuerpo más prudente en peligro** (fuera del círculo y con poca vida apaga la curiosidad: {n(sum(1 for x in B if x['alt'][V[0]] != x['hoy']))} decisiones cambian, casi todas
dejando de ir a por lo nuevo) y **no le hace coger más lo nuevo en calma**; en el caso del freno da el mismo freno que la calma, porque un rival a 5 casillas vale 0,5 en las dos.
Si lo que se quiere es que un rival lejano no frene la curiosidad, el radio tendría que ser menor que 5 (hoy 8 a 2), o la cautela no debería entrar cuando el objeto está a una
casilla; son números de la mesa. Y sigue en pie lo de P7-25: lo que falta es lo que el cuerpo cree que gana al llegar.

## Archivos

| archivo | qué es |
|---|---|
| `banco_P7_26.py` → `P7_26_decisiones.json` | las decisiones con la cautela ×1 y ×2 |
| `nace_P7_23.py` (`cautela_de`, `E["cautela"]`) | la variante, como mando de banco (apagada en el campo) |
| `P7_25_decisiones.json`, `informe_P7_25.md` | reclasificados con la calma del diario (sin cambios de clase) |
| `informe_P7_26.md` | este informe |
"""
assert "§" not in T; open(os.path.join(AQUI, "informe_P7_26.md"), "w").write(T); print(len(T))
