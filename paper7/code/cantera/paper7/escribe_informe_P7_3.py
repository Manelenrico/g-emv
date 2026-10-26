"""[P7-3] Escribe informe_P7_3.md desde P7_3_techo.json, P7_3_banco_techo.json, P7_2_banco.json, P7_1_medidas.json y fuga_P7_3.json."""
import json, hashlib, os
from collections import Counter, defaultdict
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
TE = json.load(open(os.path.join(AQUI, "P7_3_techo.json"))); BT = json.load(open(os.path.join(AQUI, "P7_3_banco_techo.json"))); DT = [d for v in BT["vidas"] for d in v["decisiones"]]
B2 = json.load(open(os.path.join(AQUI, "P7_2_banco.json"))); D2 = [d for v in B2["vidas"] for d in v["decisiones"]]; D2i = {(d["carpeta"], d["asiento"], d["t"]): d for d in D2}
M1 = json.load(open(os.path.join(AQUI, "P7_1_medidas.json"))); U1 = {(L["carpeta"], L["slot"], u["t"]): u for L in M1["vidas"] for u in L["usos_botiquin"]}
FU = json.load(open(os.path.join(AQUI, "fuga_P7_3.json")))
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
sello = open(os.path.join(AQUI, "SELLO_P7_3.md")).read().strip().split("`")[-2]
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def pct(a, b): return f"{n(100 * a / b, 1)} %" if b else "–"
NOM = {"botiquin": "botiquín", "bow": "arco", "blowgun": "cerbatana"}
tr = lambda d: "1-20" if d["dia"] <= 20 else "21-40"
def grupo(D, o, s, dias): return [d for d in D if d["objeto"] == o and d["situacion"] == s and tr(d) == dias]
L = []; w = L.append
fieles_t = sum(1 for d in DT if d["fiel"])
w(f"""# P7-3 · Saber no basta, por qué: la fuga entre vidas, el techo, las opciones en la pelea y el botiquín caso a caso

*3-oct-2026. Coste cero (plataforma 0; consola 0). `motor/model.py` = `{md5('motor/model.py')}` al empezar y al acabar; congelados y
cuerpo sin tocar. Sello: `SELLO_P7_3.md`, commit 9681ab7, md5 `{sello}`, antes de calcular. Mismos 80 diarios de A4 y misma réplica que
P7-2 (`banco_P7_2.py`, un proceso por vida). Scripts: `banco_P7_3.py` (techo → `P7_3_techo.json`, `P7_3_banco_techo.json`), `fuga_P7_3.py`
(sondas de la fuga → `fuga_P7_3.json`), `escribe_informe_P7_3.py` (este informe). Fontanería del banco del techo: {fieles_t} de {len(DT)} decisiones
iguales al diario con la creencia del catálogo.*

## Sección 1 · La fuga entre vidas

**Qué pasa de una vida a la siguiente.** `policy_pareja._envuelve(alma)` (`cantera/paper6/policy_pareja.py:99-134`) instala dos envoltorios
"desde fuera": uno sobre la voz (`PC.PARTE.emite`, `:103-117`) y otro sobre los candidatos del decisor (`D.candidatos`, `:121-134`). El de
los candidatos captura lo que `D.candidatos` vale en ese momento (`:121`, `_orig_cands = D.candidatos`) y lo sustituye por `_cands`
(`:134`), que lleva atada la criatura (`_a=alma`, `:122`) y veta todo candidato cuyo `objetivo` sea un rival **contado** por ella
(`_a._contados`, `:125-131`; el conjunto lo escribe cada tic `AlmaPareja` en `:92` desde `oyente2.slots_contados`). Se crea una vez por
vida: en el campo, en `run()` (`:150`; en A4, `policy_pareja11.py:69`); en los bancos, al arrancar cada réplica. **No se reinicia nunca**:
el módulo `decisor_zs` guarda el `D.candidatos` envuelto, y la siguiente llamada a `_envuelve` lo captura como "original" y le pone otra
capa encima. En un proceso con varias vidas, `D.candidatos` es una cadena de capas, una por vida, y cada capa sigue vetando con el
`_contados` de **su** criatura, que al acabar su vida queda congelado con los últimos rivales contados. Así desaparecen los candidatos
`atacar_*` cuyo objetivo era un rival contado en una vida anterior: lo visto en P7-2 (defensa del hermano) y en el barrido de
`fuga_P7_3.py`, que corre las vidas en orden en un solo proceso: la tercera vida ya pierde fidelidad ({[r for r in FU if r['i'] == 3][0]['fieles']} de {[r for r in FU if r['i'] == 3][0]['decisiones']}; la sonda en el
primer tic infiel, t {FU[2]['infieles'][0]['t']}, muestra al rival en la memoria de agresores y ningún `atacar_*` entre los candidatos). Comprobación directa: con
las mismas tres vidas en un proceso, restaurando `D.candidatos` y `PC.PARTE.emite` a su valor base antes de cada `_envuelve`, la
tercera vida da 174 de 174 y, sin restaurar, 160 de 174 (`fuga_prueba_P7_3.py`, con y sin `restaurar`).
`filas10_P6_10.py:68-84` (`_CAMPOS`, campos geodésicos por `id(mundo)`) también sobrevive entre vidas (se vacía solo al pasar de 64
entradas), pero en el barrido ningún `id(mundo)` se reutilizó ({sum(1 for r in FU if r['id_mundo_reusado'])} de {len(FU)} vidas): no es la causa de lo visto.

**(a) Los bancos del seis.** Una vida por proceso (no afectados): P6-14, P6-15, P6-18 y P6-19 lanzan `banco_P6_*.py` con un
`subprocess` por vida (`corre_P6_14.py:22`, `corre_P6_15.py:22`, `corre_P6_18.py:16`, `corre_P6_19.py:28`). Varias vidas por proceso
(afectados en potencia): P6-25 (`escenas_P6_25.py:391`, `Pool(hilos)` sin `maxtasksperchild`; `_envuelve` en `:284`), P6-28
(`banco_P6_28.py:120`, `:65`) y P6-29 (`mide_P6_29.py:371`, `:224`); P6-26 (`banco_P6_26.py:84`) usa `Pool` pero no crea `AlmaPareja`
(no replica el cuerpo). Fidelidad medida: P6-29 la mide tic a tic y da 99,86 % en A4 y 99,94 % en A7h y A8 (`informe_P6_29.md:33`): la
infidelidad que queda (0,06-0,14 %) es compatible con esta fuga, que solo toca tics con un rival contado como objetivo; no está
comprobado que sea toda ella. P6-25 y P6-28 no publican fidelidad en sus informes (sin resultado en `grep -i fiel`); sus medidas que
dependan de candidatos de ataque contra rivales contados en vidas anteriores del mismo proceso quedan por revisar.

**(b) Las partidas de campo.** Cada proceso corre **una** vida: el contenedor arranca `policy_pareja11.py` (`Dockerfile.pareja11:215`),
que llama `asyncio.run(run(url))` una sola vez (`policy_pareja11.py:89-92`) y `run` llama `_envuelve(alma)` una vez (`:69`). No hay
cadena en el campo; la fuga es de los bancos.

**Arreglo propuesto (no hecho).** Que `_envuelve` sea reversible de verdad: guardar la base una sola vez (`D._candidatos_base`,
`PC.PARTE._emite_base`) y envolver siempre desde la base, o devolver una función `desenvuelve()` que restaure `D.candidatos` y
`PC.PARTE.emite`, y que los bancos la llamen al acabar cada vida. Como `policy_pareja.py` está congelado, la vía que no toca el cuerpo es
la del banco: restaurar la base antes de cada `_envuelve` (lo comprobado arriba) o un proceso por vida (lo hecho en P7-2 y aquí).

## Sección 2 · El techo (sello T1 y T2)

Creencia del techo, por asiento (`P7_3_techo.json`): sin munición = 0 exacto; con munición y botiquín = media real del diario:
{"; ".join(f"{NOM[k.split('/')[0]]} {k.split('/')[1]} asiento {k.split('/')[2]}: {n(v, 2)} (n {TE['n'][k]})" for k, v in sorted(TE['techo'].items()))}.

| objeto | situación | días | decisiones | elige lo mismo | elige otra cosa | qué otra cosa (las más frecuentes) | otra cosa en P7-2 (aprendida) |
|---|---|---|---:|---:|---:|---|---:|
""")
for o in ("botiquin", "bow", "blowgun"):
    for s in (("dentro", "fuera") if o == "botiquin" else ("sin municion", "con municion")):
        for dias in ("1-20", "21-40"):
            g = grupo(DT, o, s, dias); c = [d for d in g if d["cambia"]]; g2 = grupo(D2, o, s, dias); c2 = sum(1 for d in g2 if d["cambia"])
            cl = Counter(d["clase_creencia"] for d in c).most_common(4)
            w(f"| {NOM[o]} | {s} | {dias} | {len(g)} | {len(g) - len(c)} ({pct(len(g) - len(c), len(g))}) | {len(c)} ({pct(len(c), len(g))}) | {'; '.join(f'{k} {v}' for k, v in cl) if cl else '–'} | {c2} ({pct(c2, len(g2))}) |\n")
na = [d for d in DT if d["objeto"] in ("bow", "blowgun") and d["situacion"] == "sin municion"]
emp = Counter()
for d in na:
    if d["cambia"]: emp["cambia"] += 1; continue
    dc = d["d_creencia"] or {}; a = dc.get(d["elegido_creencia"]); nn = dc.get("noop")
    emp["empate exacto" if (a is not None and nn is not None and abs(a - nn) < 1e-9) else ("atacar con d menor" if (a is not None and nn is not None and a < nn) else "otro")] += 1
c_na = sum(1 for d in na if tr(d) == "21-40" and d["cambia"]); n_na = sum(1 for d in na if tr(d) == "21-40")
c_bf = sum(1 for d in grupo(DT, "botiquin", "fuera", "21-40") if d["cambia"]); n_bf = len(grupo(DT, "botiquin", "fuera", "21-40"))
c_bf2 = sum(1 for d in grupo(D2, "botiquin", "fuera", "21-40") if d["cambia"])
mismo = Counter((D2i[(d["carpeta"], d["asiento"], d["t"])]["cambia"], d["cambia"]) for d in grupo(DT, "botiquin", "fuera", "21-40"))
w(f"""
| predicción | medido | veredicto |
|---|---|---|
| T1 ataques sin munición con creencia 0: cambian < 10 % | días 21-40: {c_na} de {n_na} ({pct(c_na, n_na)}); todos los días: {sum(1 for d in na if d['cambia'])} de {len(na)} ({pct(sum(1 for d in na if d['cambia']), len(na))}) | **{'acierta' if n_na and c_na / n_na < .1 else 'falla'}** |
| T2 botiquín fuera con el techo: a menos de 10 puntos del 56 % de P7-2 | {c_bf} de {n_bf} ({pct(c_bf, n_bf)}); P7-2: {c_bf2} de {n_bf} ({pct(c_bf2, n_bf)}); diferencia {n(abs(100 * c_bf / n_bf - 100 * c_bf2 / n_bf), 1)} puntos; decisión a decisión, las mismas {mismo[(True, True)]} cambian y las mismas {mismo[(False, False)]} no | **{'acierta' if abs(100 * c_bf / n_bf - 100 * c_bf2 / n_bf) <= 10 else 'falla'}** |

Con la creencia exactamente 0, en los {len(na) - sum(1 for d in na if d['cambia'])} ataques sin munición que no cambian el candidato de atacar **empata exactamente** con quedarse
quieto en {emp['empate exacto']} casos (la foto prevista es la misma: un golpe de 0 no cambia nada) y tiene d menor en {emp['atacar con d menor']} (la previsión de atacar deja
otra huella además del daño, abajo). El empate lo rompe el desempate a favor de la acción. Es decir, la creencia perfecta tampoco
cambia la decisión: **no es que lo aprendido sea insuficiente; es que el cuerpo no tiene a dónde cambiar, y en el empate prefiere actuar.**

## Sección 3 · Las opciones en la pelea

Candidatos que genera el decisor en los {len(na)} tics de ataque sin munición (réplica con el catálogo, `d_replica` de `P7_2_banco.json`):

| conjunto de candidatos (atacar_* agrupado) | tics |
|---|---:|
""")
na2 = [d for d in D2 if d["objeto"] in ("bow", "blowgun") and d["situacion"] == "sin municion"]
conj = Counter(tuple(sorted(("atacar_*" if k.startswith("atacar_") else k) for k in (d["d_replica"] or {}))) for d in na2)
for k, v in conj.most_common(10): w(f"| {', '.join(k)} | {v} |\n")
con_piernas = sum(1 for d in na2 if any(k.startswith(("move_", "paso_", "ir_")) for k in (d["d_replica"] or {})))
w(f"""
Con alguna opción de moverse (`move_`, `paso_`, `ir_`) solo en {con_piernas} de {len(na2)} tics ({pct(con_piernas, len(na2))}). Por qué no aparecen las otras:

- **Apartarse, ir al centro, ir a por munición a la vista.** Son candidatos `paso_*`, `ir_centro`, `ir_objeto` (`decisor_zs.py:433-468`).
  `Bloqueos.veta` (`decisor_zs.py:95-103`) quita todo lo que empiece por `move_`, `paso_`, `ir_` mientras `move_ready_in > 0` (`:97-98`), y
  en plena pelea las piernas están casi siempre enfriándose (11 tics por paso a velocidad 5). Los `atacar_*` se quitan solo con
  `attack_ready_in > 0` (`:99-100`), y el arco sin flechas no gasta enfriamiento (`no_ammo` cada tic). La munición a la vista entra en
  `ir_objeto` por `_mejor_objeto` (`decisor_zs.py:682-705`, valor/(1+distancia), promesa 0 para la munición), pero el candidato es un `ir_` y
  cae con el veto de las piernas.
- **Soltar el arma.** `soltar_*` solo se crea para consumibles con `heal > 0` y con el hermano herido o la provisión abierta
  (`decisor_zs.py:496-521`): no existe soltar un arma. Empuñar (`:536-544`) solo propone una arma del zurrón con **más** daño que la de la mano.
- **Pegar con la mano.** No existe el puñetazo: el candidato de atacar exige `arma.damage > 0` (`decisor_zs.py:587-588`), y las manos
  vacías no son un arma (`amenaza11_P6_11.py:28-31` las inventa solo para la amenaza ajena).
- **El desempate que prefiere la acción.** `decisor_zs.py:895-897` llama `select_tiebreak(..., exclude_noop=True, tie_unified=True)`;
  en `planificador/planificador_v1.py:433-456`, con empate exacto en la d terminal se va a `_hierarchy` (`:393-402`), cuya primera regla
  N2a (`:399-402`, "quieto no gana empates") quita `noop` de los candidatos empatados si queda alguno.

## Sección 4 · El botiquín fuera del círculo, caso a caso (días 21-40, creencia aprendida de P7-2)

Los {len([d for d in grupo(D2, 'botiquin', 'fuera', '21-40') if not d['cambia']])} que no cambian: candidato que gana, margen de d sobre el segundo, y si había casilla sin daño alcanzable antes del corte
(`P7_1_medidas.json`, `casilla_sin_dano_alcanzable`; pasos = casillas hasta el borde).

| vida | t | día | creencia | gana | d | 2.º | margen | candidatos | vida (hp) | el uso en el diario | pasos al borde | alcanzable |
|---|---:|---:|---:|---|---:|---|---:|---:|---:|---|---:|---|
""")
for d in sorted([d for d in grupo(D2, "botiquin", "fuera", "21-40") if not d["cambia"]], key=lambda d: (d["carpeta"], d["asiento"], d["t"])):
    dc = d["d_creencia"] or {}; o = sorted(dc.items(), key=lambda kv: kv[1]); u = U1.get((d["carpeta"], d["asiento"], d["t"]), {})
    w(f"| {d['carpeta'][-8:]}/{d['asiento']} | {n(d['t'])} | {d['dia']} | {n(d['b_antes'], 1)} | {o[0][0]} | {n(o[0][1], 4)} | {o[1][0] if len(o) > 1 else '–'} | {n(o[1][1] - o[0][1], 4) if len(o) > 1 else '–'} | {len(dc)} | {u.get('hp', '–')} | {'completado' if u.get('completado') else 'cancelado por ' + ', '.join(u.get('fuentes_corte') or ['?'])} | {u.get('pasos_hasta_dentro', '–') if u.get('pasos_hasta_dentro') is not None else '–'} | {('sí' if u.get('casilla_sin_dano_alcanzable') else 'no') if u.get('pasos_hasta_dentro') is not None else '–'} |\n")
nc = [d for d in grupo(D2, "botiquin", "fuera", "21-40") if not d["cambia"]]
alc = Counter(('sí' if U1.get((d['carpeta'], d['asiento'], d['t']), {}).get('casilla_sin_dano_alcanzable') else 'no') if U1.get((d['carpeta'], d['asiento'], d['t']), {}).get('pasos_hasta_dentro') is not None else '–' for d in nc)
margs = sorted((sorted((d["d_creencia"] or {}).values())[1] - sorted((d["d_creencia"] or {}).values())[0]) for d in nc if len(d["d_creencia"] or {}) > 1)
w(f"""
En los {len(nc)}: gana siempre `usar_botiquin`, por un margen de d entre {n(margs[0], 4)} y {n(margs[-1], 4)} (mediana {n(margs[len(margs) // 2], 4)}); el segundo es `noop` en {sum(1 for d in nc if sorted((d['d_creencia'] or {}).items(), key=lambda kv: kv[1])[1][0] == 'noop')} casos; con {Counter(len(d['d_creencia'] or {}) for d in nc).most_common(1)[0][0]} candidatos en {Counter(len(d['d_creencia'] or {}) for d in nc).most_common(1)[0][1]} de ellos (sin piernas). Casilla sin daño alcanzable
antes del corte: sí en {alc.get('sí', 0)}, no en {alc.get('no', 0)}, sin corte por anillo en {alc.get('–', 0)}. Todos menos {sum(1 for d in nc if U1.get((d['carpeta'], d['asiento'], d['t']), {}).get('completado'))} acabaron cancelados en el diario.

Los {len([d for d in grupo(D2, 'botiquin', 'fuera', '21-40') if d['cambia']])} que cambian: qué eligen en su lugar.

| en su lugar | casos | margen de d sobre `usar_botiquin` (mediana) | creencia (mediana) |
|---|---:|---:|---:|
""")
cc = [d for d in grupo(D2, "botiquin", "fuera", "21-40") if d["cambia"]]
for k, v in Counter(d["clase_creencia"] for d in cc).most_common():
    g = [d for d in cc if d["clase_creencia"] == k]; mg = sorted(((d["d_creencia"] or {}).get("usar_botiquin", 0) - (d["d_creencia"] or {}).get(d["elegido_creencia"], 0)) for d in g)
    w(f"| {k} | {v} | {n(mg[len(mg) // 2], 4)} | {n(sorted(d['b_antes'] for d in g)[len(g) // 2], 1)} |\n")
w(f"""
Fuente: `P7_2_banco.json` (`d_creencia` por candidato) cruzado con `P7_1_medidas.json` por (vida, t). Lectura: cuando cambia, casi siempre
es a **quedarse quieto** (sin piernas no hay más), no a ponerse a salvo; y cuando no cambia, el botiquín gana por centésimas.

## Archivos

| archivo | qué es |
|---|---|
| `SELLO_P7_3.md` | T1 y T2, md5, commit 9681ab7 |
| `banco_P7_3.py`, `P7_3_techo.json`, `P7_3_banco_techo.json` | la creencia del techo y la repetición de decisiones con ella |
| `fuga_P7_3.py`, `fuga_P7_3.json` | el barrido secuencial con sondas (12 vidas); `fuga_P7_3.log`, `banco_P7_3.log` fuera de git |
| `escribe_informe_P7_3.py`, `informe_P7_3.md` | este informe |
""")
txt = "".join(L); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_3.md"), "w").write(txt); print("escrito", len(txt))
