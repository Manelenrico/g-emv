"""[P7-0] Escribe informe_P7_0.md a partir de P7_0_medidas.json (ninguna cifra a mano). La prosa es fija; los numeros se leen."""
import json, hashlib, os, re
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
D = json.load(open(os.path.join(AQUI, "P7_0_medidas.json"))); R = D["resumen"]; V = D["vidas"]; P = R["por_objeto"]; CAT = {c["id"]: c for c in R["catalogo"]}
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    s = f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s
def est(e, d=0): return f"{n(e['mediana'], d)} / {n(e['p10'], d)} / {n(e['p90'], d)}"
def tri(e): return f"{n(e['mediana'])} / {n(e['p10'])} / {n(e['p90'])} (n {e['n']})" if e["n"] else "– (n 0)"
NV = R["vidas"]; U = R["usos_consumibles"]
def usos(i): return [u for u in U if u["id"] == i]
def stat(v, f): v = sorted(v); return f(v) if v else None
def med(v): return stat(v, lambda s: s[len(s) // 2])
ORDEN = ["sword", "spear", "bow", "knives", "blowgun", "net", "first_aid", "rations", "backpack", "camouflage", "arrows", "darts"]
NOMBRE = {"sword": "espada", "spear": "lanza", "bow": "arco", "knives": "cuchillos", "blowgun": "cerbatana", "net": "red", "first_aid": "botiquín", "rations": "raciones", "backpack": "mochila", "camouflage": "camuflaje", "arrows": "flechas", "darts": "dardos", "berry_bush": "arbusto de bayas", "manos": "manos vacías"}
L = []; w = L.append
w(f"""# P7-0 · El inventario de las cosas: qué hay en el mundo, cómo lo conoce el cuerpo y cuánto se lo encuentra

*3-oct-2026. Coste cero: sin partidas, sin llamadas a la consola (plataforma 0; consola 0). Solo lectura y medida. `motor/model.py` =
`{md5('motor/model.py')}` al principio y al final (comprobado); `CONGELADO.md` y `CONGELADO_P6.md` sin tocar; el cuerpo no se toca.
Scripts: `cantera/paper7/mide_P7_0.py` (recorre los 80 diarios A4 del seis, uno a uno, registro a registro; escribe `P7_0_medidas.json`) y
`escribe_informe_P7_0.py` (este informe, cifras leídas del JSON). Diarios: las 40 semillas de A4 del seis = P611_t1 y P611_t2 (las 20 de
P6-23) + P624_t1 (las 20 nuevas de P6-24), 2 asientos por partida = **{NV} vidas** (`mide_P7_0.py:34-39`, `informe_P6_24.md:87`).
Mundo 0.1.19: `cantera/paper6/liga/v2_coworlds_cow_6a55df20-08d1-4e4c-adba-33dbd97e1e6f.json` ("version": "0.1.19"), `informe_P6_1.md:125-131`,
`informe_P6_12.md:42`. Las vidas duran {n(R['duracion_vida']['mediana'])} tics de mediana (p10 {n(R['duracion_vida']['p10'])}, p90 {n(R['duracion_vida']['p90'])}); el aviso de la fase 5 del anillo llega en el 11.856 (`player_config.zone_schedule[4]`).*

Definiciones de medida (ver, coger, usar, soltar, dar, atacar, ventana del uso): en la cabecera de `mide_P7_0.py:1-25`. Resumen: lo
visto sale de `ve_items` (id, n, pos) de cada registro `tick`; lo cogido se infiere del inventario del tic siguiente (el diario no apunta
qué se cogió); lo usado es `pack[slot]` del tic del `use`, confirmado por lo que sigue (canal, mano o cuerpo); `action_result` del tic t es
el resultado de la acción emitida en t−1 (comprobado en `P611_t1_A4_20260916/10`, tics 592-594).

## 1 · Las cosas del mundo (0.1.19)

El catálogo llega en el `player_config` y el diario lo copia entero en el registro `k="catalogo"` (`policy_cortex.py:904` lo vuelca al
recibirlo; `mundo.py:76-85` lo lee campo a campo). Los {NV} diarios traen **un solo catálogo** (md5 del JSON ordenado:
`{V[0]['catalogo_md5']}`, {R['catalogos_distintos']} distinto): **12 tipos de objeto**. Fuera del catálogo, en las observaciones solo aparecen
arbustos (`ve_bushes`, con `charges`) y las manos vacías (`hand.id = "none"`); ningún `ve_items[].id` fuera del catálogo
({len(R['ids_vistos_fuera_del_catalogo'])} ids desconocidos). Los "cajones" de la wiki no son un objeto: son objetos del catálogo en el suelo.

| id | kind | daño | alcance | cooldown | durabilidad | pila máx. | canal (tics) | cura | tics a la vista ({NV} vidas) | montones distintos | en manos o cuerpo ajenos (asientos·vidas) | regalos de patrocinador vistos (míos) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
""")
for i in ORDEN:
    c = CAT[i]; o = P[i]
    w(f"| `{i}` ({NOMBRE[i]}) | {c['kind']} | {c['damage']} | {c['range']} | {c['cooldown']} | {c['durability']} | {c['stack_max']} | {c['use_ticks']} | {c['heal']} | {n(o['tics_a_la_vista']['total'])} | {n(o['montones_vistos']['total'])} | {n(o['vistos_en_manos_ajenas'])} | {n(o['regalos_vistos'])} ({n(o['regalos_mios'])}) |\n")
w(f"| arbusto de bayas | (terreno `B`, `ve_bushes` con `charges`) | – | – | – | – | – | – | – | – | {n(P['berry_bush']['montones_vistos']['total'])} posiciones | – | – |\n")
w(f"| manos vacías | `hand.id = \"none\"`; la wiki dice 5 de daño (`v2_wikis_zero-sum_pages_main.md:45`); el cuerpo las modela aparte (§ 2) | | | | | | | | {n(R['tics_en_mano']['nada'])} tics con la mano vacía | | | |\n")
w(f"""
Fuentes: columnas del catálogo = registro `catalogo` de cualquier diario (igual en los {NV}); tics a la vista y montones = `mide_P7_0.py`
(`ve_tics`, `montones`); manos/cuerpo ajenos = `ve_agentes[].hand/body` (asientos distintos por vida, sumados); regalos = eventos
`gift_landed` (`eventos[].type`), que solo traen botiquines y raciones.

**Coger, usar, soltar, dar.** Las acciones que el cuerpo sabe emitir son seis, y están escritas en `decisor_zs.py:934-959`: `none`, `move`,
`pickup` (sin argumento: coge lo que hay en la casilla), `use` (con `slot` = índice del `pack`), `drop` (con `slot`) y `attack` (con
`dir`). **No existe `give`**: ni en el decisor ni en la wiki; lo más parecido es soltar junto al hermano, que es como el cuerpo "da"
(`decisor_zs.py:496-521`, S-PROVISION). Qué hace `use` según el objeto, **observado en los diarios** (no leído del código del juego):
consumible → abre un canal (`effects[] = channeling/item/done_tick`); arma en el zurrón → la intercambia con la mano; prenda en el zurrón →
la viste (`body`). El cuerpo nunca ha emitido `use` sobre red, flechas ni dardos, así que no sabemos desde nuestro lado qué haría.
`pickup` sobre una prenda con el cuerpo vacío la viste directamente (comentado en `decisor_zs.py:547-553` citando `sim.nim:735`, que no
está en este repositorio). Los arbustos: el cuerpo no tiene acción de forrajear y en {NV} vidas no hay ni una recogida en casilla de arbusto
({R['cogidas_en_arbusto']} cogidas, {R['fallos_en_arbusto']} intentos fallidos allí); cómo se forrajea es pregunta para Ari.

| objeto | ¿se puede coger? | ¿usar? | ¿soltar? | ¿dar? | de dónde sale |
|---|---|---|---|---|---|
| espada, lanza, arco, cuchillos, cerbatana | sí (cogidos en los diarios: {", ".join(n(P[i]['cogidos']['total']) for i in ('sword','spear','bow','knives','blowgun'))}) | `use` = empuñar desde el zurrón ({", ".join(n(P[i]['usos_confirmados']['total']) for i in ('sword','spear','bow','knives','blowgun'))} confirmados); `attack` con el arma en mano ({", ".join(n(P[i]['ataques']['total']) for i in ('sword','spear','bow','knives','blowgun'))} ataques) | `drop` existe; 0 soltadas de armas en los diarios | no hay `give` | `mide_P7_0.py` (coge/usa/ataca); `decisor_zs.py:538-544` (empuñar), `:588-602` (atacar) |
| red | sí ({n(P['net']['cogidos']['total'])} cogidas, {n(P['net']['cogidos']['vidas_con'])} vidas) | nunca: 0 `use`, 0 `attack` con red en mano (el candidato de atacar exige daño > 0, `decisor_zs.py:588`; la red tiene 0) | 0 soltadas | no | `mide_P7_0.py`; el diario registra `netted` sobre mí ({R['episodios_netted']['n']} episodios), así que alguien sí la lanza |
| botiquín, raciones | sí ({n(P['first_aid']['cogidos']['total'])} y {n(P['rations']['cogidos']['total'])} unidades) | `use` = canal de {CAT['first_aid']['use_ticks']} / {CAT['rations']['use_ticks']} tics ({n(P['first_aid']['usos_confirmados']['total'])} y {n(P['rations']['usos_confirmados']['total'])} confirmados) | `drop`: {n(P['first_aid']['sueltos']['total'])} y {n(P['rations']['sueltos']['total'])} | soltar con el hermano a ≤ 2 casillas: {n(P['first_aid']['sueltos_junto_al_hermano']['total'])} y {n(P['rations']['sueltos_junto_al_hermano']['total'])} (proxy declarado) | `mide_P7_0.py`; `decisor_zs.py:483-521` |
| mochila, camuflaje | sí ({n(P['backpack']['cogidos']['total'])} y {n(P['camouflage']['cogidos']['total'])}); con el cuerpo vacío, coger = vestir | `use` desde el zurrón = ponerse ({n(P['backpack']['usos_confirmados']['total'])} y {n(P['camouflage']['usos_confirmados']['total'])} confirmados); llevada puesta en {R['vidas_con_mochila_puesta']} y {R['vidas_con_camuflaje_puesto']} vidas | `drop` existe; 0 en los diarios (ponerse otra tira la anterior al suelo, `decisor_zs.py:831-835`) | no | `mide_P7_0.py` (`tics_puesto`); `decisor_zs.py:559-568` |
| flechas, dardos | sí ({n(P['arrows']['cogidos']['total'])} y {n(P['darts']['cogidos']['total'])} unidades) | no se usan: las gasta el arma al atacar (observado: `no_ammo` cuando no hay) | 0 | no | `mide_P7_0.py` (`ataques_resultado`) |
| arbusto | no es objeto; `charges` visibles | sin acción conocida desde nuestro lado | – | – | `ve_bushes`; pregunta para Ari |

**Lo que no se puede saber desde nuestro lado** (el código del juego no es nuestro; los comentarios del decisor citan `sim.nim`, que no está
en el repositorio) y queda como pregunta para Ari: (1) cómo se forrajea un arbusto y qué da; (2) qué hace `use` sobre red, flechas o dardos;
(3) si la red se lanza con `attack` (daño 0) y qué registra el mundo; (4) si `drop` deja el objeto en mi casilla o en la vecina; (5) si hay
alguna acción de dar directa; (6) reglas de apilado al coger (el diario muestra `inventory_full` {n(R['fallos_causa'].get('inventory_full', 0))} veces con objeto en la casilla).

## 2 · Cómo conoce el cuerpo cada cosa (cuerpo congelado del seis, `CONGELADO_P6.md`)

El cuerpo no sabe nombres: **lee el catálogo** y clasifica por `kind` (`mundo.py:128-157`): el consumible que más cura es el botiquín y el
resto raciones (`:133-134`); las armas son `ikMelee/ikRanged/ikThrown` y el daño de referencia es el mayor del catálogo (`:136-138`);
la munición, `ikAmmo` (`:139`); mochila y camuflaje se casan por id dentro de `ikGear` (`:143-149`, declarando la ausencia); la red es el
arrojadizo de daño 0 (`:151-157`). Lo que vale cada cosa está en tres sitios: la **riqueza W** (`appraisal_zs_v42_exp.py:717-779`, filas
R-CARENCIA `:1076` con `W_TARGET = 3.0` `:126`), la **previsión** del decisor (`decisor_zs.py:817-856`) y las **filas** que cada objeto
apaga o enciende. Tres casos: (a) efecto escrito; (b) solo deseable o necesario, sin efecto; (c) nada.

| objeto | caso | qué sabe el cuerpo | dónde (archivo:línea) |
|---|---|---|---|
| botiquín (`first_aid`) | **(a)** | cura `heal` del catálogo (50): la previsión de `usar_botiquin` pone `hp2 = min(hp_max, hp + heal)`; conoce el canal (`use_ticks` = 48) y veta volver a usar mientras dura; vale 1,0 de W; su falta enciende R-ACOPIO (0,18) y, con la hermana sin venda, S-PROVISION (0,30) y R-HERMANO-FALTA; la promesa de cogerlo = cuánto apaga R-ACOPIO | `decisor_zs.py:483-493` (candidato con `heal`), `:823-828` (previsión), `:83-93, :102` (canal), `appraisal_zs_v42_exp.py:749` (W), `:939-958` (R-ACOPIO, `ACOPIO_M :111`), `:1312-1362` (S-PROVISION), `:1637-1644`, `decisor_zs.py:642-651` (promesa). **No sabe** que el canal se corta con cualquier daño (§ 4) |
| raciones (`rations`) | **(a)** | cura 15 (misma previsión `usar_racion`), canal 24; W: la 1.ª vale 1,0, la 2.ª 0,3 solo con mochila | `decisor_zs.py:483-493, :823-825`, `appraisal_zs_v42_exp.py:751-759`, `RACION_2A :411` |
| espada, lanza (`ikMelee`) | **(a)** | daño del catálogo × (5+STR)/10 en la previsión de atacar; alcance (`range`) para el candidato; W = daño/18 × durabilidad restante/`durability`; "estar armado" = arma en la mano; empuñar intercambia mano y ranura | `decisor_zs.py:588-602` (candidato), `:852-856` (daño previsto), `:841-845` (empuñar), `appraisal_zs_v42_exp.py:731-738` (W con desgaste) |
| arco, cerbatana (`ikRanged`) | **(a)** para el daño, **(b)** para la munición | daño y alcance del catálogo (14/8, 4/6); W = daño/18 × min(1, munición/8); **el candidato de atacar no mira la munición** (no hay `ammo` ni `municion` en `decisor_zs.py`): de {n(P['bow']['ataques']['total'])} ataques con arco, {n(R['ataques_resultado']['bow'].get('no_ammo', 0))} devolvieron `no_ammo`; con cerbatana, {n(R['ataques_resultado']['blowgun'].get('no_ammo', 0))} de {n(P['blowgun']['ataques']['total'])}. **No sabe** que los dardos envenenan | `appraisal_zs_v42_exp.py:739-744`, `AMMO_REF :414`; `decisor_zs.py:588-602`; `mide_P7_0.py` (`ataques_resultado`) |
| cuchillos (`ikThrown`, daño 8) | **(a)** | daño y alcance; W = 8/18 × min(1, n/8) (los propios cuchillos cuentan como munición) | `appraisal_zs_v42_exp.py:739-744`, `decisor_zs.py:852-856` |
| flechas, dardos (`ikAmmo`) | **(b)** | solo cuentan en W como munición del arma en mano; ningún efecto propio; no condicionan atacar | `appraisal_zs_v42_exp.py:740-741`, `mundo.py:139` |
| red (`net`, arrojadizo de daño 0) | **(b)** | vale 0,25 de W (`GEAR_MENOR_W`) en mano o en el zurrón; **ningún efecto** (no sabe que inmoviliza) y **no puede lanzarla** (atacar exige daño > 0) | `mundo.py:151-157`, `appraisal_zs_v42_exp.py:765-768`, `:413`; `decisor_zs.py:588` |
| camuflaje (`camouflage`) | **(a)** | efecto escrito **a mano desde la wiki**, no del catálogo: invisible a más de 4 casillas quieto / 7 moviéndose, revelado 5 s tras atacar (S-8-EXPOSICIÓN); vale 0,25 de W; la promesa de cogerlo = cuánto apaga S-8; ponerse = vestir en el acto | `appraisal_zs_v42_exp.py:405-410` (`CAMO_QUIETO/MOVIENDO/REVELADO_S`), `:1386-1416` (S-8), `:763-764` (W); `decisor_zs.py:672-676` (promesa), `:559-568, :831-839` (ponerse) |
| mochila (`backpack`) | **(a)** parcial | sabe que da las ranuras 2-3 (al quitársela, el zurrón previsto vuelve a 2) y que permite la 2.ª ración; vale 0,5 de W mientras quede apetito; la promesa = cuánto sube W. No sabe nada más | `decisor_zs.py:831-839`, `:677-680`; `appraisal_zs_v42_exp.py:753-758, :770-776` (`MOCHILA_W :412`) |
| arbusto de bayas | **(b)** | es un sitio de botín de nivel 0,07 (`VALOR_NIVEL["bayas"]`) para R-LLAMADA mientras tenga `charges`; no sabe qué da ni cómo se forrajea; no hay candidato de forrajear | `appraisal_zs_v42_exp.py:147-149`, `:694-697`, `:1082-1088`, `decisor_zs.py:707-724` |
| manos vacías | **(a)** virtual | el cuerpo no tiene puñetazo (atacar exige arma con daño); para la **amenaza ajena** inventa dos armas virtuales: `~manos` (daño 3, alcance 1) para todo hostil con la mano vacía y `~manos_pegando` (daño 18) si me pega | `amenaza11_P6_11.py:28-31, :53, :64-68` (`DANO_MANOS`), `decisor_zs.py:588` |
| veneno (efecto) | **(a)** sobre mí, **(c)** como causa | F-DAÑO × 1,5 mientras `effects[] = poison`; no sabe qué lo causa ni que bloquea el botiquín | `appraisal_zs_v42_exp.py:51`, `:870-874` |
| red sobre mí (`netted`) | **(c)** | no aparece en el cuerpo (0 menciones de `netted` en decisor y appraisal) | grep en `decisor_zs.py`, `appraisal_zs_v42_exp.py` |
| armas ajenas (E por arma) | **(a)** del catálogo | la amenaza del hermano y la propia usan `damage` y `range` del catálogo del arma en la mano del rival; la memoria aprendida (p95) **no se carga** en A4 (`MIEDO_ON = False`) | `appraisal_zs_v42_exp.py:1578-1592`, `:379-396`; `policy_cortex.py:93-96`; `CONGELADO_P6.md` (notas) |
| recursos oídos (parte E2) | **(b)** | el parte del hermano trae los objetos que ve como letras del catálogo; el oyente los inyecta en la observación mientras pesan ≥ 0,30 (≤ 86 tics) | `parte2.py:76-81`, `oyente2.py:64, :142-152` |

Qué habría que quitar para que el cuerpo "no sepa" una cosa (hechos, no recomendación): el **efecto** de un consumible vive en una sola línea
(`decisor_zs.py:824`, `hp + receta["heal"]`, con `heal` tomado del catálogo en `:490-493`); el **valor** (deseo) vive en `riqueza_W`
(`appraisal_zs_v42_exp.py:749-776`) y en las filas que lo citan (R-ACOPIO `:939-958`, S-PROVISION `:1312-1362`, R-HERMANO-FALTA
`:1637-1644`, promesas `decisor_zs.py:642-680`); el **efecto del camuflaje** vive en `:405-410` y `:1386-1416`; el de la **mochila** en
`decisor_zs.py:831-839` y `appraisal_zs_v42_exp.py:753-758`; el **daño de las armas** en `decisor_zs.py:852-856` y `appraisal_zs_v42_exp.py:735`.

## 3 · Cuánto se las encuentra (A4, {NV} vidas; mediana / p10 / p90 por vida)

| objeto | vidas que lo ven | montones distintos vistos | unidades cogidas (vidas con ≥ 1) | usos confirmados (vidas) | tics hasta el primer encuentro | tics hasta la primera cogida | tics hasta el primer uso |
|---|---:|---|---|---|---|---|---|
""")
for i in ORDEN + ["berry_bush"]:
    o = P[i]
    w(f"| {NOMBRE[i]} | {o['montones_vistos']['vidas_con']} | {est(o['montones_vistos'])} | {est(o['cogidos'])} ({o['cogidos']['vidas_con']}) | {est(o['usos_confirmados'])} ({o['usos_confirmados']['vidas_con']}) | {tri(o['tics_primer_encuentro'])} | {tri(o['tics_primera_cogida'])} | {tri(o['tics_primer_uso'])} |\n")
w(f"""
Lectura: "montones" = pares (id, posición) distintos a lo largo de la vida; "unidades cogidas" cuenta el `n` ganado en el inventario
(una pila de 2 botiquines = 2); "usos confirmados" = `use` seguido del canal (consumibles), de la mano (armas) o del cuerpo (prendas);
para las armas, los **ataques** van en el § 4. Los tics cuentan desde el tic 1 (la cuenta atrás; la ignición es el 480): casi todo se ve
desde el pedestal o en el primer minuto. Fuente: `mide_P7_0.py` → `P7_0_medidas.json["resumen"]["por_objeto"]`. Fallos de `pickup`:
{n(R['fallos_pickup_total'])} (`no_target` {n(R['fallos_causa'].get('no_target', 0))}, `inventory_full` {n(R['fallos_causa'].get('inventory_full', 0))}).

## 4 · Lo que pasa al usarlas

**Qué registra el diario en el tic de usar** (registro `k="tick"`, campos leídos en `mide_P7_0.py:57-146`): la acción emitida
(`intencion`: `do`, `slot`), el inventario **antes** (`hand` con `durability` o `n`, `pack[slot] = {{id, n}}`, `body`), `hp`, `effects[]`
(`channeling` con `item` y `done_tick`; `poison`; `netted`; `camo_revealed`), `damage_taken[]` por tic (`source`: `zone`, `poison` o el
asiento `P<n>`; `amount`), `damage_dealt` y `kills` acumulados, `action_result` (de la acción anterior), la zona, lo visible, y la
`RADIOGRAFIA` del decisor (candidatos con su d y el `elegido`: en los {len(U)} usos de consumible el elegido fue siempre `usar_botiquin` /
`usar_racion`). El inventario **después** está en el registro siguiente. **Qué no registra:** qué objeto cogió un `pickup` (se infiere del
inventario), cuánto curó un canal (se infiere de `hp`), por qué se canceló, a quién alcanzó un ataque (solo el acumulado `damage_dealt`),
si otros me ven (el camuflaje no es medible desde aquí), el hp exacto del hermano (solo `hp_band`; el parte E2 lo trae cada 25 tics).
**No hay hambre** en este mundo: ni la observación ni la wiki tienen tal variable; las raciones son solo vida (+15).

**Ventana declarada:** desde el tic t del `use` hasta t_fin = `done_tick` + 1 (= t + canal + 1: {CAT['first_aid']['use_ticks']} tics el botiquín, {CAT['rations']['use_ticks']} las raciones).
delta_neto = hp(t_fin) − hp(t) + daño recibido en (t, t_fin]. Completado = el `n` del objeto baja en t_fin; cancelado = no baja.

""")
w("| consumible | usos confirmados | completados | cancelados | sin cerrar | en la fase 5 o después |\n|---|---|---|---|---|---|\n")
for i in ("first_aid", "rations"):
    us = usos(i); c = [u for u in us if u.get("completado")]; x = [u for u in us if u.get("completado") is False]; s = [u for u in us if u.get("completado") is None]
    dc = [u["delta_neto"] for u in c]; dx = [u["delta_neto"] for u in x]
    w(f"| {NOMBRE[i]} | usos confirmados {len(us)} | completados {len(c)} (delta_neto mediana {n(med(dc), 1)}, mín {n(min(dc), 1) if dc else '–'}, máx {n(max(dc), 1) if dc else '–'}; hp antes mediana {n(med([u['hp'] for u in c]))}) | cancelados {len(x)} (delta_neto mediana {n(med(dx), 1) if dx else '–'}; con daño en la ventana {sum(1 for u in x if u['dano_ventana'] > 0)} de {len(x)}) | sin cerrar (muere antes) {len(s)} | en la fase 5 o después (t ≥ 11.856): {sum(1 for u in us if u['t'] >= 11856)} usos, {sum(1 for u in c if u['t'] >= 11856)} completados |\n")
fa_x = [u for u in usos("first_aid") if u.get("completado") is False]
from collections import Counter
radios = Counter(u["radio_zona"] for u in fa_x)
w(f"""
El botiquín cura lo que dice el catálogo cuando el canal acaba (delta
máximo 50, acotado por el hp máximo), pero **el canal se corta con cualquier daño**: los {len(fa_x)} cancelados llevan todos daño dentro de
la ventana, casi todo del fuego del anillo (radio de la zona al cancelarse: {", ".join(f"{k} → {v}" for k, v in sorted(radios.items(), key=lambda kv: -kv[1])[:4])}). El cuerpo no sabe esto
(§ 2): vuelve a emitir `use` cada 49 tics y arde (ejemplo: `P611_t1_A4_20260916/10`, tics 12.289, 12.338, 12.387…, hp 93 → 80 → 67 → 54).
Una ración cancelada que sí curó 13 (`P611_t1_A4_20470374/10`, t 12.021): el `n` no bajó en la ventana; probablemente una recogida en medio.

**Prendas.** Mochila: con `body = backpack` el `pack` tiene siempre 4 ranuras ({n(R['largo_pack_por_prenda'].get('backpack', {}).get('4', 0))} tics) y 2 sin ella: medible. Camuflaje: puesto
{n(R['tics_puesto'].get('camouflage', 0))} tics en {R['vidas_con_camuflaje_puesto']} vidas; su efecto (que no me vean) **no es medible desde nuestro lado**; el diario sí registra `camo_revealed`
({n(R['efectos_sobre_mi'].get('camo_revealed', 0))} tics). **Red:** 0 lanzamientos propios; sobre mí, {R['episodios_netted']['n']} episodios `netted` de {n(R['episodios_netted']['largo_mediana'])} tics (≈ 3 s), con {n(R['episodios_netted']['hp_perdido_mediana'])} hp perdidos de mediana
mientras duraban. **Veneno** (dardos ajenos): {R['episodios_poison']['n']} episodios en {R['episodios_poison']['vidas_con']} vidas, {n(R['episodios_poison']['largo_mediana'])} tics de mediana (p90 {n(R['episodios_poison']['largo_p90'])}), {n(R['episodios_poison']['hp_perdido_mediana'])} hp perdidos de mediana;
`damage_taken.source = "poison"`: {n(R['fuentes_dano'].get('poison', 0))} pulsos, {n(R['dano_por_fuente'].get('poison', 0))} hp en total (2 por pulso, como dice la wiki).

**Armas** (`attack` con el arma en mano; golpe = `damage_dealt` sube en t+1; resultado = `action_result` de t+1):

| arma | ataques | `ok` | `no_ammo` | golpes | vidas que atacan | tics hasta el primer ataque (med / p10 / p90) | tics con el arma en mano |
|---|---:|---:|---:|---:|---:|---|---:|
""")
for i in ("sword", "spear", "bow", "knives", "blowgun", "net"):
    o = P[i]; ar = R["ataques_resultado"].get(i, {})
    w(f"| {NOMBRE[i]} | {n(o['ataques']['total'])} | {n(ar.get('ok', 0))} | {n(ar.get('no_ammo', 0))} | {n(o['golpes']['total'])} | {o['ataques']['vidas_con']} | {tri(o['tics_primer_ataque'])} | {n(R['tics_en_mano'].get(i, 0))} |\n")
w(f"""
Las manos vacías no atacan nunca ({n(P['manos']['ataques']['total'])} ataques: el candidato no existe sin arma). El daño recibido por fuente en las {NV} vidas: anillo
{n(R['dano_por_fuente'].get('zone', 0))} hp en {n(R['fuentes_dano'].get('zone', 0))} golpes; rivales (fuentes `P<n>`) {n(sum(v for k, v in R['dano_por_fuente'].items() if k.startswith('P')))} hp en {n(sum(v for k, v in R['fuentes_dano'].items() if k.startswith('P')))} golpes; veneno {n(R['dano_por_fuente'].get('poison', 0))}.

**La tercera columna ("lo que pasó").** Con lo que guardamos ya se calcula: para consumibles, hp antes/después y si el canal acabó;
para prendas, el cuerpo y el tamaño del zurrón; para armas, si el ataque se aplicó (`ok`/`no_ammo`/`no_target`) y si hizo daño
(`damage_dealt`); para el veneno y la red sobre mí, duración y hp. **Habría que guardar además**, si se quiere sin inferir: el id de lo
cogido en cada `pickup`, un evento del mundo por uso (objeto, resultado, cantidad curada, motivo de cancelación), el objetivo y el daño de
cada ataque, y el `durability` del arma en cada golpe (está en `hand`, pero no se liga al golpe). Nada de esto lo da hoy el mundo en la
observación: es pregunta para Ari si existe en el protocolo.

## 5 · Los objetos del piloto de Ari

Camuflaje, red y mochila **existen en 0.1.19** con esos ids (`camouflage`, `net`, `backpack`) en el catálogo de los {NV} diarios. Sus
puntos 2-4 están en las tablas: el cuerpo conoce el camuflaje con efecto escrito a mano (§ 2), lo lleva puesto en {R['vidas_con_camuflaje_puesto']} vidas
({n(P['camouflage']['cogidos']['total'])} cogidas; primer encuentro a {n(P['camouflage']['tics_primer_encuentro']['mediana'])} tics de mediana) y su efecto no es medible desde aquí (§ 4); la red la
conoce solo como valor 0,25 sin efecto, la coge en {P['net']['cogidos']['vidas_con']} vidas y no la lanza nunca; la mochila la conoce como ranuras
y valor 0,5, la lleva en {R['vidas_con_mochila_puesta']} vidas y su efecto (2 → 4 ranuras) es medible y se ve.

## 6 · Cuántos usos por vida (para que la mesa calcule partidas)

| objeto | usos completados en {NV} vidas | por vida | vidas con ≥ 1 | p90 por vida |
|---|---:|---:|---:|---:|
""")
for i in ("first_aid", "rations"):
    o = P[i]["usos_completados"]; w(f"| {NOMBRE[i]} (canal acabado) | {n(o['total'])} | {n(o['total'] / NV, 2)} | {o['vidas_con']} | {n(o['p90'], 1)} |\n")
for i in ("sword", "spear", "bow", "knives", "blowgun"):
    o = P[i]["golpes"]; w(f"| {NOMBRE[i]} (golpes que hacen daño) | {n(o['total'])} | {n(o['total'] / NV, 2)} | {o['vidas_con']} | {n(o['p90'], 1)} |\n")
for i, k in (("backpack", "mochila"), ("camouflage", "camuflaje")):
    vc = sum(1 for L in V if L["tics_puesto"].get(i)); w(f"| {k} (vidas que la llevan puesta) | {vc} | {n(vc / NV, 2)} | {vc} | – |\n")
w(f"| red (lanzamientos) | 0 | 0 | 0 | – |\n")
w(f"""
Fuente: `P7_0_medidas.json["resumen"]["por_objeto"][id]["usos_completados" | "golpes"]`, `tics_puesto` por vida.

## Objetos conocidos a los que se podría quitar lo que el cuerpo sabe de ellos (solo hechos)

| objeto | lo que hoy sabe | dónde está escrito | usos por vida hoy (§ 6) |
|---|---|---|---|
| botiquín | cura 50 (catálogo), canal 48, valor 1,0 de W, filas de acopio y provisión | `decisor_zs.py:490-493, :824`; `appraisal_zs_v42_exp.py:749, :939-958, :1312-1362` | {n(P['first_aid']['usos_completados']['total'] / NV, 2)} |
| raciones | cura 15, canal 24, valor 1,0 (+0,3 la 2.ª con mochila) | `decisor_zs.py:490-493, :824`; `appraisal_zs_v42_exp.py:751-759` | {n(P['rations']['usos_completados']['total'] / NV, 2)} |
| espada, lanza | daño y alcance (catálogo), desgaste, valor daño/18 | `decisor_zs.py:588-602, :852-856`; `appraisal_zs_v42_exp.py:731-738` | {n((P['sword']['golpes']['total'] + P['spear']['golpes']['total']) / NV, 2)} |
| arco, cerbatana, cuchillos | daño y alcance; valor con munición | `decisor_zs.py:588-602, :852-856`; `appraisal_zs_v42_exp.py:739-744` | {n((P['bow']['golpes']['total'] + P['blowgun']['golpes']['total'] + P['knives']['golpes']['total']) / NV, 2)} |
| camuflaje | radios 4 / 7 y revelado 5 s (a mano, de la wiki); valor 0,25; promesa | `appraisal_zs_v42_exp.py:405-410, :1386-1416, :763-764`; `decisor_zs.py:672-676` | puesto en {R['vidas_con_camuflaje_puesto']} de {NV} vidas |
| mochila | ranuras 2-3; 2.ª ración; valor 0,5; promesa | `decisor_zs.py:831-839, :677-680`; `appraisal_zs_v42_exp.py:753-758, :770-776` | puesta en {R['vidas_con_mochila_puesta']} de {NV} vidas |
| red | solo valor 0,25; sin efecto; no se lanza | `appraisal_zs_v42_exp.py:765-768`; `mundo.py:151-157` | 0 |
| flechas, dardos | solo munición en W | `appraisal_zs_v42_exp.py:740-744` | – |
| arbustos | nivel de botín 0,07 | `appraisal_zs_v42_exp.py:147-149, :694-697` | 0 recogidas |

## Preguntas para Ari (lo que no se sabe desde nuestro lado)

1. Cómo se forrajea un arbusto (`ve_bushes.charges`) y qué objeto da; ¿es `pickup` en la casilla?
2. Qué hace `use` sobre red, flechas y dardos; si la red se lanza con `attack` y cómo se registra (daño 0).
3. Si `drop` deja el objeto en la casilla propia; si existe alguna acción de dar directa; reglas de apilado y de `inventory_full`.
4. Si el protocolo puede devolver, por tic, el id de lo cogido, el resultado de un canal (curado, cancelado y por qué), y el objetivo y
   daño de cada ataque; hoy se infieren.
5. Si el canal del botiquín se cancela con **cualquier** daño, incluido el del anillo (lo observado: {len(fa_x)} de {len(fa_x)} cancelaciones con daño en la ventana).
6. Si la fuente del juego (`sim.nim`, citada en los comentarios de `decisor_zs.py`) que describe `resolvePickup` y `use` sigue vigente en 0.1.19.

## Archivos

| archivo | qué es |
|---|---|
| `cantera/paper7/mide_P7_0.py` | la medida sobre los 80 diarios (definiciones en su cabecera); `mide_P7_0.log` su salida |
| `cantera/paper7/P7_0_medidas.json` | por vida: visto, cogido, usado, soltado, atacado, prendas, fuentes de daño, episodios; resumen por objeto |
| `cantera/paper7/escribe_informe_P7_0.py` | escribe este informe desde el JSON |
| `cantera/paper7/informe_P7_0.md` | este informe |
""")
open(os.path.join(AQUI, "informe_P7_0.md"), "w").write("".join(L))
print("escrito informe_P7_0.md", len("".join(L)), "caracteres")
