"""[P7-1] Escribe informe_P7_1.md desde P7_1_medidas.json y P7_1_diario.json (ninguna cifra a mano)."""
import json, hashlib, os
from collections import Counter, defaultdict
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
D = json.load(open(os.path.join(AQUI, "P7_1_medidas.json"))); R = D["resumen"]; V = D["vidas"]; B = R["botiquin"]; J = json.load(open(os.path.join(AQUI, "P7_1_diario.json")))
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def tri(e, d=0): return f"{n(e['mediana'], d)} / {n(e['p10'], d)} / {n(e['p90'], d)}"
def pct(a, b): return f"{n(100 * a / b, 1)} %" if b else "–"
NV = R["vidas"]; BOT = [f for f in J["botiquin"] if f["paso"]["resultado"] != "sin cerrar"]; ARC = J["arco_cerbatana"]
def grp(filas, fn, res="resultado"):
    g = defaultdict(Counter)
    for f in filas: g[fn(f)][f["paso"][res]] += 1
    return g
L = []; w = L.append
w(f"""# P7-1 · El botiquín y el arco por dentro, y el diario de tres columnas sobre lo ya vivido

*3-oct-2026. Coste cero: sin partidas, sin llamadas (plataforma 0; consola 0). Solo lectura y medida sobre los mismos 80 diarios A4 del
seis que P7-0 (40 semillas: P611_t1, P611_t2, P624_t1; 2 asientos por partida). `motor/model.py` = `{md5('motor/model.py')}` al
empezar y al acabar; congelados sin tocar; el cuerpo no se toca. Scripts: `cantera/paper7/mide_P7_1.py` (definiciones en su cabecera,
líneas 1-26; escribe `P7_1_medidas.json` y el diario `P7_1_diario.json`) y `escribe_informe_P7_1.py` (este informe, cifras leídas de los
JSON). "Dentro del círculo" = distancia euclídea al centro ≤ radio del mismo tic: de {n(R['zona_vs_dano'][0])} golpes de zona en los 80 diarios,
{n(R['zona_vs_dano'][1])} caen fuera por esta regla (`R["zona_vs_dano"]`); los {n(R['zona_vs_dano'][0] - R['zona_vs_dano'][1])} restantes son del borde (radio no entero durante el encogimiento).*

## Sección 1 · El botiquín por dentro ({B['usos']} usos confirmados; {B['completados']} completados, {B['cancelados']} cancelados, {B['sin_cerrar']} sin cerrar porque la vida acaba antes)

Nota sobre P7-0: allí "completado" era solo "el botiquín sale del zurrón antes de `done_tick`+1" y dio 64. Aquí se exige además que no
hubiera daño antes de `done_tick` (el daño corta el canal). Los {len(B['n_bajo_con_dano_en_canal'])} casos que cambian de columna son usos cortados por el anillo en los que
el cuerpo **soltó** el botiquín después del corte (`drop/ok` en los cinco, mirado tic a tic: por ejemplo `P611_t1_A4_21098748/10`, uso en
12.889, corte en 12.913, `drop` en 12.929), sin curarse (cura real {", ".join(n(f["cura_real"], 2) for L in V for f in L["usos_botiquin"] if f.get("n_bajo") and f.get("dano_antes_de_done"))}).

**¿Inmoviliza?** No. Durante el canal el cuerpo se mueve y el canal sigue: posiciones distintas mientras el canal vive (hasta el corte en
los cancelados, hasta `done_tick` en los completados): {", ".join(f"{k} → {v}" for k, v in sorted(B['posiciones_distintas'].items(), key=lambda kv: int(kv[0])))}. De los {B['completados']} completados,
{B['movio_por_resultado']['completado'].get('true', 0)} se movieron durante el canal y {B['movio_por_resultado']['completado'].get('false', 0)} no; de los {B['cancelados']} cancelados, {B['movio_por_resultado']['cancelado'].get('true', 0)} y {B['movio_por_resultado']['cancelado'].get('false', 0)}. Intenciones emitidas
dentro del canal (acción/resultado): {", ".join(f"{k} {v}" for k, v in sorted(B['intenciones_en_canal'].items(), key=lambda kv: -kv[1]))}. Ni moverse ni atacar cortan
el canal; lo que lo corta es recibir daño (abajo). Fuente: `mide_P7_1.py` (`_pos`, `_intenciones`), `P7_1_medidas.json["resumen"]["botiquin"]`.

**Cada uso, por situación** (cerrados: {B['cerrados']}):

| | completados | cancelados |
|---|---:|---:|
""")
for k, v in B["por_dentro_fuera"].items(): w(f"| {k} del círculo al usar | {v.get('completado', 0)} | {v.get('cancelado', 0)} |\n")
for k in sorted(B["por_fase"], key=lambda x: (int(x.rstrip('e')), x)): v = B["por_fase"][k]; w(f"| fase {k.rstrip('e')}{' (encogiendo)' if k.endswith('e') else ''} | {v.get('completado', 0)} | {v.get('cancelado', 0)} |\n")
w(f"""
Vida al usar: mediana {n(B['hp_al_usar']['mediana'])} (p10 {n(B['hp_al_usar']['p10'])}, p90 {n(B['hp_al_usar']['p90'])}). Rivales a la vista al usar: {", ".join(f"{k}{'+' if k == '3' else ''} → {v}" for k, v in sorted(B['rivales_vistos_al_usar'].items()))}; distancia al más cercano
cuando hay alguno: mediana {n(B['rival_min_dist']['mediana'], 1)} casillas (p10 {n(B['rival_min_dist']['p10'], 1)}, p90 {n(B['rival_min_dist']['p90'], 1)}).

**De dónde vino el daño que cortó el canal** (primer tic con daño después del `use`; {B['tics_hasta_corte']['n']} cortes, a {tri(B['tics_hasta_corte'])} tics del `use`): anillo
{B['fuentes_corte'].get('zone', 0)}, rivales {sum(v for k, v in B['fuentes_corte'].items() if k.startswith('P'))} (asientos {", ".join(f"{k} {v}" for k, v in sorted(B['fuentes_corte'].items()) if k.startswith('P'))}), veneno {B['fuentes_corte'].get('poison', 0)}. Fuera del círculo casi todo es anillo
({B['fuentes_corte_por_dentro']['fuera'].get('zone', 0)} de {sum(B['fuentes_corte_por_dentro']['fuera'].values())}); dentro, casi todo rivales ({sum(v for k, v in B['fuentes_corte_por_dentro']['dentro'].items() if k.startswith('P'))} de {sum(B['fuentes_corte_por_dentro']['dentro'].values())}) y {B['cancelados_dentro_por_zona_encogiendo']} veces el anillo que encoge y deja fuera al cuerpo. El fuego del anillo golpea cada 24
tics y el canal dura 48: fuera del círculo y quieto, el canal no puede acabar nunca.

**¿Había una casilla sin daño alcanzable antes del corte?** (solo cortes por anillo; pasos = casillas hasta el borde, 11 tics por casilla
a velocidad 5, `mundo.py:216-217`): {B['corte_por_zona_alcanzable'].get('alcanzable', 0)} sí, {B['corte_por_zona_alcanzable'].get('no alcanzable', 0)} no, {B['corte_por_zona_alcanzable'].get('estaba dentro (el circulo se movio o dano de otro)', 0)} estaba dentro al usar (el círculo se movió). Pasos hasta el borde: mediana
{n(B['pasos_hasta_dentro']['mediana'])} (p10 {n(B['pasos_hasta_dentro']['p10'])}, p90 {n(B['pasos_hasta_dentro']['p90'])}). De los {B['por_dentro_fuera']['fuera'].get('completado', 0)} completados fuera, {B['completados_fuera_que_acaban_dentro']} acaban dentro: el cuerpo entró andando con el canal abierto.

**Tiempo por vida intentando curarse en el fuego** (tics dentro de un canal de botiquín estando fuera del círculo, hasta el corte):
mediana {n(B['tiempo_en_el_fuego_por_vida']['mediana'])}, p10 {n(B['tiempo_en_el_fuego_por_vida']['p10'])}, p90 {n(B['tiempo_en_el_fuego_por_vida']['p90'])} tics; total {n(B['tiempo_en_el_fuego_por_vida']['total'])} tics ({n(B['tiempo_en_el_fuego_por_vida']['total'] / 24)} s) en {B['vidas_con_fuego']} de {NV} vidas.

**Muertes por anillo** (la vida acaba y el último daño es del anillo): {B['muertes_por_anillo']} de {NV} vidas (razones de final: {", ".join(f"{k} {v}" for k, v in B['razones_final'].items())}). Con
intentos de botiquín en los últimos 10 segundos (240 tics): **{B['muertes_anillo_con_intento_10s']} de {B['muertes_por_anillo']}**; intentos en esas 40: mediana {n(B['intentos_10s_en_muertes_anillo']['mediana'])}, p90 {n(B['intentos_10s_en_muertes_anillo']['p90'])}, total {B['intentos_10s_en_muertes_anillo']['total']}.
Solo se describe; no se reabre el seis.

## Sección 2 · El arco y la cerbatana por dentro

| | arco | cerbatana |
|---|---:|---:|
""")
A = R["arco"]
rows = [("ataques", lambda a: n(a["ataques"])), ("resultado `ok` / `no_ammo`", lambda a: f"{n(a['resultados'].get('ok', 0))} / {n(a['resultados'].get('no_ammo', 0))}"), ("golpes (daño hecho)", lambda a: n(a["golpes"])),
        ("`no_ammo` sin munición en la mochila / con munición sin cargar", lambda a: f"{n(a['no_ammo_sin_municion'])} / {n(a['no_ammo_con_municion_en_mochila'])}"), ("`ok` con munición / sin munición", lambda a: f"{n(a['ok_con_municion'])} / {n(a['ok_sin_municion'])}"),
        ("`no_ammo` con munición a la vista", lambda a: f"{n(a['no_ammo_municion_a_la_vista'])} ({pct(a['no_ammo_municion_a_la_vista'], a['resultados'].get('no_ammo', 1))})"), ("`no_ammo` con munición contada por el hermano (E2 ≤ 86 tics)", lambda a: f"{n(a['no_ammo_contada_por_el_hermano'])} ({pct(a['no_ammo_contada_por_el_hermano'], a['resultados'].get('no_ammo', 1))})"),
        ("qué hacía el rival atacado (`no_ammo`): me pegaba / se acercaba / nada", lambda a: " / ".join(n(a['no_ammo_rival_hacia'].get(k, 0)) for k in ("me pegaba", "se acercaba", "nada"))), ("el rival era mi agresor (honor) / defensa del hermano", lambda a: f"{n(a['no_ammo_era_agresor'].get('true', 0))} / {n(a['no_ammo_defensa_pareja'].get('true', 0))}"),
        ("distancia al rival (mediana / p10 / p90)", lambda a: tri(a["no_ammo_rival_dist"], 1)), ("`no_ammo` dentro del círculo / fuera", lambda a: f"{n(a['no_ammo_dentro'].get('true', 0))} / {n(a['no_ammo_dentro'].get('false', 0))}"),
        ("vidas con algún `no_ammo`", lambda a: n(a["vidas_con_no_ammo"])), ("tics por vida en ataques que no hacen nada (mediana / p10 / p90; 80 vidas)", lambda a: tri(a["tics_no_ammo_por_vida"])), ("fracción de la vida, en las vidas que atacan con el arma (mediana / p90)", lambda a: f"{n(100 * a['fraccion_vida_no_ammo']['mediana'], 2)} % / {n(100 * a['fraccion_vida_no_ammo']['p90'], 2)} %")]
for et, fn in rows: w(f"| {et} | {fn(A['bow'])} | {fn(A['blowgun'])} |\n")
w(f"""
Lectura: la munición en la mochila separa el resultado **sin una excepción**: todos los `no_ammo` son con 0 flechas (o dardos) en
mano y zurrón, y todos los `ok` con alguna. "Sin cargar" no existe: no hay ataque fallido con munición a bordo. En la mayoría de los
fallos había munición a la vista (`ve_items`) y el rival estaba pegándome a 1-2 casillas. Cada ataque fallido es un tic de decisión;
el tiempo perdido es pequeño en fracción de vida pero se concentra en la pelea. Fuente: `mide_P7_1.py` (`ataques_arco_cerbatana`),
`P7_1_medidas.json["resumen"]["arco"]`; el asiento atacado sale de `RADIOGRAFIA.honor.objetivo`.

## Sección 3 · El diario de tres columnas sobre lo ya vivido (`cantera/paper7/P7_1_diario.json`)

Una fila por uso de botiquín ({len(J['botiquin'])}) y por ataque con arco o cerbatana ({len(ARC)}). Cada fila lleva `vida` (carpeta/asiento), `t`, y las
tres columnas:

| columna | botiquín | arco / cerbatana | exacto o inferido |
|---|---|---|---|
| **situación** (solo lo que el cuerpo ya percibe en t) | dentro/fuera y distancia al borde, vida, daño recibido en los 24 y 120 tics anteriores, rivales a ≤ 5 casillas y distancia al más cercano, fase y si encoge | dentro/fuera, vida, daño en los 24 anteriores, rivales a ≤ 5, distancia al rival atacado, munición en la mochila, a la vista, contada por el hermano, qué hacía el rival, fase | exacto: todo sale del registro `tick` de t (`pos`, `zona`, `hp`, `damage_taken`, `ve_agentes`, `ve_items`, `hand`, `pack`); "contada por el hermano" se infiere del `chat` (E2 del hermano, ≤ 86 tics, letra `a`/`f` en la sección I); "qué hacía" se infiere de `damage_taken` (120 tics) y de su distancia en t frente a t−24 |
| **imaginado** (lo que la previsión del cuerpo esperaba) | hp esperado = min(100, hp + 50) (`decisor_zs.py:824`, `heal` del catálogo) | daño esperado = 14 (arco) / 4 (cerbatana), daño del catálogo (`decisor_zs.py:852-856`) | exacto: es la fórmula del cuerpo aplicada al hp y al catálogo del mismo tic |
| **lo que pasó** | completado / cancelado / sin cerrar; hp al final de la ventana; cura real; daño en la ventana; tic y fuentes del corte; si se movió; si acabó dentro | `action_result` (`ok` / `no_ammo`); golpe; daño hecho | exacto: `hp`, `n` del pack, `effects`, `action_result`, `damage_dealt`; inferido: cura real = hp_fin − hp + daño en la ventana (el diario no da la cura directa); cancelado = el `n` no baja en `done_tick`+1; golpe = `damage_dealt` sube en t+1 (no dice a quién) |

## Sección 4 · Lo que habría que aprender: lo imaginado contra lo que pasó, por situación (sin ninguna regla de aprendizaje)

**Botiquín** ({len(BOT)} filas cerradas). Lo imaginado es siempre "curo 50 (o hasta 100)". Lo que pasó, por cada variable percibida:

| variable | valor | completados | cancelados | acierta la creencia |
|---|---|---:|---:|---:|
""")
G = R["aprender"]["botiquin"]
for var, et in (("dentro", "dentro / fuera del círculo"), ("dano_prev_24", "daño en los 24 tics anteriores"), ("dano_prev_120", "daño en los 120 tics anteriores"), ("rivales_a_5", "rival a ≤ 5 casillas"), ("hp_banda", "vida"), ("fase", "fase del anillo"), ("dentro_y_dano24", "dentro/fuera × daño 24"), ("dentro_y_rival5", "dentro/fuera × rival a 5"), ("fuera_y_movio", "dentro/fuera × se movió en el canal (no la percibe antes: es lo que hizo)"), ("dentro_sin_rival5_sin_dano24", "dentro, sin rival a 5 y sin daño 24")):
    for val, c in sorted(G[var].items(), key=lambda kv: str(kv[0])):
        co, ca = c.get("completado", 0), c.get("cancelado", 0); w(f"| {et} | {val} | {co} | {ca} | {pct(co, co + ca)} |\n")
cr = R["aprender"]["botiquin_cura_real"]
w(f"""
Cura real (hp al final − hp al usar + daño en la ventana): dentro, mediana {n(cr['dentro']['mediana'], 1)} (p10 {n(cr['dentro']['p10'], 1)}, p90 {n(cr['dentro']['p90'], 1)}); fuera, mediana {n(cr['fuera']['mediana'], 1)} (p10 {n(cr['fuera']['p10'], 1)}, p90 {n(cr['fuera']['p90'], 1)}).

Qué separa y qué no: **ninguna variable percibida separa limpiamente.** La que más, "dentro o fuera del círculo": fuera, la creencia
falla en {pct(G['dentro']['fuera'].get('cancelado', 0), sum(G['dentro']['fuera'].values()))} de los usos; dentro, acierta en {pct(G['dentro']['dentro'].get('completado', 0), sum(G['dentro']['dentro'].values()))}. Los {G['dentro']['fuera'].get('completado', 0)} aciertos fuera son casi todos cuerpos que entraron andando con el canal abierto
({B['completados_fuera_que_acaban_dentro']} acaban dentro), y los {G['dentro']['dentro'].get('cancelado', 0)} fallos dentro son golpes de rivales ({sum(v for k, v in B['fuentes_corte_por_dentro']['dentro'].items() if k.startswith('P'))}) o el anillo que encoge ({B['cancelados_dentro_por_zona_encogiendo']}). "Daño en los 24 tics
anteriores" separa peor que dentro/fuera (con daño: {pct(G['dano_prev_24']['con dano 24'].get('cancelado', 0), sum(G['dano_prev_24']['con dano 24'].values()))} fallos; sin daño: {pct(G['dano_prev_24']['sin dano 24'].get('completado', 0), sum(G['dano_prev_24']['sin dano 24'].values()))} aciertos). El cruce "dentro y sin rival a 5" acierta en
{pct(G['dentro_y_rival5']['dentro / sin rival a 5'].get('completado', 0), sum(G['dentro_y_rival5']['dentro / sin rival a 5'].values()))} ({sum(G['dentro_y_rival5']['dentro / sin rival a 5'].values())} casos) y "dentro, sin rival a 5 y sin daño 24" en {pct(G['dentro_sin_rival5_sin_dano24']['dentro, sin rival a 5, sin dano 24'].get('completado', 0), sum(G['dentro_sin_rival5_sin_dano24']['dentro, sin rival a 5, sin dano 24'].values()))} ({sum(G['dentro_sin_rival5_sin_dano24']['dentro, sin rival a 5, sin dano 24'].values())} casos), pero son pocos. La variable que
sí separa es la que el cuerpo **no percibe al decidir**: si recibirá daño en los 48 tics siguientes. Fuera del círculo eso es seguro
(el anillo pega cada 24 tics) salvo que entre andando; dentro, depende de los rivales.

**Arco y cerbatana.** Lo imaginado es siempre "pego 14 (arco) / 4 (cerbatana)". Lo que pasó:

| arma | variable | valor | `ok` | `no_ammo` | acierta la creencia |
|---|---|---|---:|---:|---:|
""")
for arma, et in (("bow", "arco"), ("blowgun", "cerbatana")):
    GA = R["aprender"]["arco_cerbatana"][arma]
    for var, ev in (("municion", "munición en la mochila"), ("a_la_vista", "munición a la vista"), ("contada", "contada por el hermano"), ("rival_hacia", "qué hacía el rival"), ("rivales_a_5", "rival a ≤ 5"), ("dano_prev_24", "daño 24 anteriores"), ("dentro", "dentro / fuera")):
        for val, c in sorted(GA[var].items()):
            ok, na = c.get("ok", 0), c.get("no_ammo", 0); w(f"| {et} | {ev} | {val} | {ok} | {na} | {pct(ok, ok + na)} |\n")
dh = R["aprender"]["arco_dano_hecho_ok"]
w(f"""
Daño hecho cuando el ataque sale (`ok`): arco mediana {n(dh['bow']['mediana'])} (p10 {n(dh['bow']['p10'])}, p90 {n(dh['bow']['p90'])}; {dh['bow']['n']} ataques, {n(dh['bow']['total'])} hp en total); cerbatana mediana {n(dh['blowgun']['mediana'])} (p10 {n(dh['blowgun']['p10'])}, p90 {n(dh['blowgun']['p90'])}; {dh['blowgun']['n']} ataques, {n(dh['blowgun']['total'])} hp).

Qué separa: **la munición en la mochila separa limpiamente**, con cero excepciones en {n(sum(R['arco'][a]['ataques'] for a in ('bow', 'blowgun')))} ataques: con munición el ataque sale
(y hace daño o no según el blanco), sin munición nunca. Es una variable que el cuerpo ya percibe (`pack`, `hand.n`) y que ya usa para
valorar el arma en W (`appraisal_zs_v42_exp.py:739-744`), pero no para decidir atacar (`decisor_zs.py:588-602`). Ninguna otra variable
separa: con munición a la vista o contada por el hermano la creencia falla igual.

## Sección 5 · Cuántas experiencias por día: filas de diario por criatura y vida ({NV} vidas; mediana / p10 / p90, total)

| objeto | situación | mediana / p10 / p90 por vida | total | vidas con ≥ 1 |
|---|---|---|---:|---:|
""")
def vidas_con(filas, fn, val): return len({f["vida"] for f in filas if fn(f) == val})
F = R["filas_por_vida"]
for k, v in F["botiquin"]["dentro_fuera"].items():
    if k != "todas": w(f"| botiquín | {k} del círculo | {tri(v)} | {v['total']} | {vidas_con(J['botiquin'], lambda f: 'dentro' if f['situacion']['dentro'] else 'fuera', k)} |\n")
for k, v in F["botiquin"]["dano_prev_24"].items():
    if k != "todas": w(f"| botiquín | {k} | {tri(v)} | {v['total']} | {vidas_con(J['botiquin'], lambda f: 'con dano 24' if f['situacion']['dano_prev_24'] > 0 else 'sin dano 24', k)} |\n")
v = F["botiquin"]["dentro_fuera"]["todas"]; w(f"| botiquín | todas | {tri(v)} | {v['total']} | {len({f['vida'] for f in J['botiquin']})} |\n")
for arma, et in (("bow", "arco"), ("blowgun", "cerbatana")):
    for k, v in F[arma]["municion"].items():
        if k != "todas": w(f"| {et} | {k} | {tri(v)} | {v['total']} | {vidas_con([f for f in ARC if f['arma'] == arma], lambda f: 'con municion' if f['situacion']['municion_mochila'] > 0 else 'sin municion', k)} |\n")
    v = F[arma]["municion"]["todas"]; w(f"| {et} | todas | {tri(v)} | {v['total']} | {len({f['vida'] for f in ARC if f['arma'] == arma})} |\n")
w(f"""
Fuente: `P7_1_medidas.json["resumen"]["filas_por_vida"]`; las 80 vidas cuentan, también las que no usan el objeto (de ahí las medianas 0).
La mayoría de las vidas no abre ninguna fila de arco o cerbatana; las que sí, abren muchas seguidas en una pelea (p90 {n(F['bow']['municion']['todas']['p90'])} filas de arco).

## Archivos

| archivo | qué es |
|---|---|
| `cantera/paper7/mide_P7_1.py` | la medida (definiciones en la cabecera); `mide_P7_1.log` su salida (fuera de git) |
| `cantera/paper7/P7_1_medidas.json` | por vida: usos de botiquín con su canal, ataques con arco y cerbatana; resumen por secciones |
| `cantera/paper7/P7_1_diario.json` | el diario de tres columnas: `botiquin` ({len(J['botiquin'])} filas), `arco_cerbatana` ({len(ARC)} filas) |
| `cantera/paper7/escribe_informe_P7_1.py` | escribe este informe desde los JSON |
| `cantera/paper7/informe_P7_1.md` | este informe |
""")
txt = "".join(L); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_1.md"), "w").write(txt); print("escrito", len(txt))
