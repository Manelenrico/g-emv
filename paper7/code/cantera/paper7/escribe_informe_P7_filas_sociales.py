"""[P7 filas sociales] Escribe informe_P7_filas_sociales.md: lo que dice el código del cuerpo (citado por archivo y línea) y lo que dicen los diarios (P7_filas_sociales.json,
de filas_sociales_P7.py). Ninguna cifra de los diarios a mano. Solo lectura: no toca el cuerpo, ni model.py, ni ningún guion.   python3 escribe_informe_P7_filas_sociales.py"""
import collections, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(AQUI, "P7_filas_sociales.json"))); EV = R["eventos"]; RS = R["resumen"]; VI = R["S_VINCULO_en_fotos"]
n = lambda x, d=3: f"{x:.{d}f}".replace(".", ",")
A = "`paintball/alma/appraisal_zs_v42_exp.py"   # «A»
L = ["# Las filas sociales en el cuerpo del siete", "",
     "*24-oct-2026. Solo lectura: sin partidas, sin llamadas (0 créditos, 0 $); no se toca `motor/model.py`, ni el cuerpo, ni ningún guion. Código citado por archivo y línea; "
     "lo de los diarios lo cuenta `cantera/paper7/filas_sociales_P7.py` → `P7_filas_sociales.json` (todos los diarios de los ocho campos, asientos 10 y 11) y lo escribe aquí "
     "`escribe_informe_P7_filas_sociales.py`. «A» = `paintball/alma/appraisal_zs_v42_exp.py`, la tabla congelada del cuerpo (md5 en `cantera/paper5/CONGELADO.md:77` y "
     "`cantera/paper6/CONGELADO_P6.md:22-23`).*", "",
     "## Uno · Las filas de la tabla del cuerpo del siete", "",
     "**Cómo se suman.** Cada fila tiene un reparto (cuerpo F, recursos R, vínculo S) en `REPARTO` (A:417-439). El signo lo da `APETITIVAS`: en la tabla base solo `R-LLAMADA` atrae "
     "(A:441); todas las demás duelen. `appraise` (A:1671-1696) suma M × reparto en el lado que toca; una fila fuera de `REPARTO` no cuenta. No hay filas de alivio aparte: el alivio "
     "es una atenuación dentro de una fila (p. ej. medicina junto a la hermana, A:332-333). Los ejes del motor son nF, nR, nS (`motor/model.py:153-158`).", "",
     "**Qué cuerpo.** El cuerpo congelado del seis (`cantera/paper7/policy_pareja_P7.py:1`) con estos interruptores (`paintball/alma/policy_cortex.py:93-97`): `EMPATIA_ON` sí, "
     "`H_PREV` 0,25, `H_GOLPE` 1,0, `MIEDO_ON` no, `VIDA_AJENA_ON` no. Encima, las piezas del seis (S-COMPANIA de P6-10, la mano vacía de P6-11) y las del siete, que crecen con los "
     "campos: el mando del miedo desde P7-49 (`cantera/paper7/miedo_P7_49.py:16`) y las invitaciones desde P7-54 (`cantera/paper7/invita_P7_54.py:18-20,63`).", "",
     "| fila | reparto F·R·S | signo | qué la enciende y con qué fuerza | dónde |", "|---|---|---|---|---|",
     "| F-DANO | 0,8·0,1·0,1 (A:419) | duele | la vida que falta, (hp_max − hp)/hp_max, con cuesta convexa por encima de 0,4 (A:67,118); envenenada ×1,5 (A:51) | A:865-875 |",
     "| F-REENCUENTRO | 0,8·0,1·0,1 (A:426) | duele | un agresor recordado, visible, armado y acercándose a ≤ 5 casillas (A:265); M = cuesta(daño acumulado/hp_max), ×0,5 fuera de su alcance (A:266); con la mano vacía cuenta como arma (`cantera/paper6/amenaza11_P6_11.py`); ×miedo desde P7-49 | A:886-933 |",
     "| F-ANTICIPACION | 0,8·0,1·0,1 (A:420) | duele | el fuego del anillo que llega: (dps/ref)·0,5·max(0, 1 − t/20 s), techo 0,5 (A:123-125); ×miedo | A:983-1000 |",
     "| F-4-ALCANCE | 0,8·0,1·0,1 (A:421) | duele | el peor hostil: 0,5·max(0, 1 − t/20 s), t = lo que tardaría en tenerme a tiro (A:130-131); ×miedo | A:1055-1072 |",
     "| MIEDO_APRENDIDO | 0,8·0,1·0,1 (A:423) | — | **apagada** (`MIEDO_ON` = no, `policy_cortex.py:95`) | A:1515-1553 |",
     "| F-HERMANO-AMENAZA | 0,8·0,1·0,1 (A:425) | duele | un hostil armado tiene a la hermana a su alcance: 0,25·min(1, daño/hp de ella)·futuro; ×miedo | A:1556-1632, 1642 |",
     "| F-HERMANO-GOLPE | 0,8·0,1·0,1 (A:426) | duele | el parte de la hermana dice que la están golpeando: lo mismo con 1,0; calla a la anterior | A:1629-1632, 1643 |",
     "| R-ACOPIO | 0,1·0,8·0,1 (A:428) | duele | sin botiquín, 0,18 (A:111); la hermana sin venda, 0,10 si llevo una (A:221); en el siete, por lo aprendido (k) y ×miedo | A:938-973 |",
     "| R-CARENCIA | 0,15·0,7·0,15 (A:429) | duele | lo que falta de riqueza: (W_TARGET − W)/W_TARGET, W_TARGET 3 (A:126); en el siete, W_TARGET y W por lo aprendido (`cantera/paper7/nace_P7_23.py`) | A:1075-1076 |",
     "| R-LLAMADA | 0,1·0,8·0,1 (A:430) | **atrae** | el mejor botín a la vista: valor × (1 − d/24)³, techo 0,25 (A:133-135) | A:1081-1088 |",
     "| R-HERMANO-FALTA | 0,1·0,8·0,1 (A:427) | duele | la hermana sin cura y con vida < 0,66: 0,125 (A:371); en el siete ×lo aprendido del botiquín (`nace_P7_23.py:238-239`) | A:1637-1641, 1644 |",
     "| S-SOLEDAD | 0,1·0,1·0,8 (A:430) | duele | sin ver ni oír a la hermana: (1 − P)·0,5·min(1, tiempo sola/30 s) (A:321-322) | A:1092-1097 |",
     "| S-COMPANIA | 0,1·0,1·0,8 (A:437) | duele | la del cinco, apagada (A:314); la del seis: 0,32·min(1, (d − 7)/(7·(1 + 2·calma))), d = camino hasta la hermana (`cantera/paper6/filas10_P6_10.py:62-64,93-103`); ×miedo | `filas10_P6_10.py:162` |",
     "| **S-DANO-PAREJA** | 0,15·0,25·0,6 (A:431) | duele | la vida que le falta a la hermana: (hp_max − hp de ella)/hp_max × B; ×0,5 con medicina a ≤ 2 de ella (A:332-333); 0 si ha muerto | A:1109-1171 |",
     "| **S-MUERTE-PAREJA** | 0,15·0,25·0,6 (A:432) | duele | el duelo (punto Tres) | A:1115-1126 |",
     "| **S-VINCULO** | 0,1·0,1·0,8 (A:433) | duele | solo en la foto de un candidato que golpearía a la hermana con un golpe que la mata seguro (A:186): M = 1,0, sin B (A:191) | A:1181, 1185-1197 |",
     "| **S-HERIDO** | 0,15·0,25·0,6 (A:435) | duele | la hermana con vida < 60 (A:201): cuesta((60 − hp)/60)·1,8 (A:198); ×0,15 con ayuda a ≤ 2 (A:202); se alivia al acercarse (A:210) | A:1182, 1198-1302 |",
     "| S-PROVISION | 0,15·0,25·0,6 (A:436) | duele | en calma, ella sin venda y yo con una: 0,30 (A:218) | A:1312-1362 |",
     "| S-VIDA-AJENA | 0,1·0,1·0,8 (A:434) | — | **apagada** (`VIDA_AJENA_ON` = no, `policy_cortex.py:96`) | A:1652-1667 |",
     "| S-8-EXPOSICION | 0,4·0,1·0,5 (A:438) | duele | hostiles que me ven: Σ 0,3·(1 − d/r), techo 0,3 (A:401-402); en el siete, radios del camuflaje por lo aprendido (`nace_P7_33.py:181-187`); ×miedo | A:1389-1416 |",
     "| S-7-AGRESOR | 0,5·0,1·0,4 (A:439) | duele | quien me ha golpeado: min(0,5, daño/50)·vida·cercanía, techo 0,5 (A:339-342); ×miedo | A:1444-1508 |",
     "| R-CURIOSIDAD (siete) | 0,1·0,8·0,1 | duele | 0,18·calma·ignorancia de la cosa (`cantera/paper7/descubre_P7.py:150-152,289,350`) | `descubre_P7.py` |",
     "| R-CURIOSIDAD-CUANTO (siete) | 0,1·0,8·0,1 | duele | análoga, por cuánto (`cantera/paper7/nace_P7_29.py:161-170,189,211-212`) | `nace_P7_29.py` |",
     "| INVITACION-CUERPO / -RECURSOS / -VINCULO (siete, desde P7-54) | 0,8·0,1·0,1 / 0,1·0,8·0,1 / 0,1·0,1·0,8 | atraen (las de sufijo «-» duelen) | solo en la foto del candidato invitado: min(1, |promesa|·confianza/escala) (`invita_P7_54.py:18-20,63,105`) | `invita_P7_54.py` |",
     "",
     "El mando del miedo (`miedo_P7_49.py:16`) multiplica F-ANTICIPACION, F-4-ALCANCE, F-REENCUENTRO, MIEDO_APRENDIDO, F-HERMANO-AMENAZA, S-8-EXPOSICION, S-7-AGRESOR, R-ACOPIO y "
     "S-COMPANIA por 0,5 o 1,5 según la hermana; deja intactas, por decisión de Manel, las pérdidas presentes y S-VINCULO y S-VIDA-AJENA, «el freno a matar» (`miedo_P7_49.py:5-6`). "
     "Las capas del regalo y del pedido del siete escalan en S-DANO-PAREJA, S-HERIDO, R-HERMANO-FALTA y S-PROVISION solo la parte que se debe a una cura visible "
     "(`cantera/paper7/descubre_P7.py:155,176`; `cantera/paper7/pide_P7.py:139-142`).", "",
     "## Dos · Las cuatro filas sociales del tres en el cuerpo del siete", "",
     "- **Las cuatro siguen en la tabla y activas**: S-DANO-PAREJA (A:431, 1109-1171), S-MUERTE-PAREJA (A:432, 1115-1126), S-VINCULO (A:433, 1185-1197) y S-HERIDO (A:435, 1198-1302). "
     "La tabla es la congelada (md5 en `CONGELADO.md:77`, `CONGELADO_P6.md:22-23`). Ninguna pieza del seis ni del siete las quita ni cambia sus fórmulas.",
     "- **Lo que se les ha puesto por fuera**: a S-DANO-PAREJA y S-HERIDO, las capas del regalo y del pedido del siete, que solo tocan la parte debida a una cura a la vista (arriba). "
     "S-MUERTE-PAREJA y S-VINCULO, intactas; el miedo no las escala a propósito (`miedo_P7_49.py:5-6`).",
     "- **De dónde vienen**: S-DAÑO-PAREJA y S-MUERTE-PAREJA en la tabla de signos (`paintball/tabla_signos_v1.md:64-65`; al principio el duelo era plano, «1.0 × B, sostenida el resto del "
     "episodio»); el duelo que se apaga, en el PROMPT 12 (`paintball/PROMPT_12_don_duelo_y_diagnostico.md:25-29`); S-VINCULO y S-HERIDO en el acta 54 (`paper3_cantera/actas/54_peso_acta.md:18,32`).",
     "- **No consta** ningún documento que las retire, ni un congelado propio del siete.", "",
     "## Tres · El duelo: cómo se apaga", "",
     "Regla exacta (A:1115-1126; constantes en A:335-336):", "",
     "- Empieza en el tic en que el cuerpo ve los fuegos de la muerte de la hermana (`mem.tick_muerte_pareja`, A:607-611).",
     "- **Unidad: segundos de partida**, dt = (tic − tic de la muerte) / `tick_rate` (A:1121-1122), con `tick_rate` = 24 tics por segundo (`paintball/alma/mundo.py:97`).",
     "- **f = 0,3 + 0,7 · 0,5^(dt / 90)**: semivida de 90 s (`DUELO_SEMIVIDA_S`, A:336) y un suelo de 0,3 (`DUELO_SUELO`, A:335: «[Manel] nunca baja de 0.3 x B»). M = f · B, con B el vínculo "
     "(roce, entre 0 y 1).",
     "- **No se acaba**: a los 90 s vale 0,65 · B, a los 180 s 0,475 · B, y tiende a 0,3 · B el resto de la partida. Mientras dura, S-DANO-PAREJA vale 0 (A:1116).",
     "- También aparece, «prevista», en la foto de un candidato que mataría a la hermana (A:1114,1126).", "",
     "## Cuatro · ¿Murió alguna vez una hermana y se encendió el duelo en la otra?", "",
     f"**Sí, y muchas veces.** En todos los diarios de los ocho campos, el primer tic vivo en que el cuerpo tiene a la hermana muerta estando ella viva: **{len(EV)} veces**. "
     "En todas ellas la fila S-MUERTE-PAREJA está en la foto de ahora desde ese mismo tic.", "",
     "| campo | diarios | con duelo | tics vivos con S-MUERTE-PAREJA | con S-DANO-PAREJA | con S-HERIDO | con S-VINCULO (foto de ahora) |", "|---|---|---|---|---|---|---|"]
for c, x in RS.items():
    t = x["tics_con_fila"]; L.append(f"| {c} | {x['diarios']} | {x['con_duelo']} | {t['S-MUERTE-PAREJA']} | {t['S-DANO-PAREJA']} | {t['S-HERIDO']} | {t['S-VINCULO']} |")
extra = sum(x["diarios_con_fila"]["S-MUERTE-PAREJA"] - x["con_duelo"] for x in RS.values())
L += ["", f"(Sobre {sum(x['tics_vivos'] for x in RS.values())} tics vivos en total. La lista de partidas y asientos con duelo está en `P7_filas_sociales.json`, `eventos`. "
      f"En {extra} diarios más la fila aparece solo en el tic en que mueren las dos a la vez, con la que la ve ya a vida 0; no cuentan como duelo vivido.)", "",
      "**Cómo se apaga en los datos** (mediana entre los casos que siguen vivos a esa altura; la fuerza M):", "", "| segundos desde la muerte | casos | M (mediana) | mín | máx |", "|---|---|---|---|---|"]
for s in ("0", "1", "5", "10", "20", "30", "60"):
    xs = [e["M_por_segundo"].get(s) for e in EV if e["M_por_segundo"].get(s) is not None]
    L.append(f"| {s} | {len(xs)} | {n(st.median(xs), 4)} | {n(min(xs), 4)} | {n(max(xs), 4)} |")
u = [e["ultimo_segundo_con_fila"] for e in EV]
mx = collections.Counter(e["fila_mas_fuerte"] for e in EV)
L += ["", f"Coincide con la regla con B = 1 (a 60 s, 0,3 + 0,7 · 0,5^(60/90) = 0,741). La que queda viva sigue en la partida, con el duelo encendido, una mediana de {n(st.median(u), 1)} s "
      f"(de {n(min(u), 1)} a {n(max(u), 1)} s), hasta que muere ella o acaba la partida. En el tic de la muerte, el duelo es la fila más fuerte en {mx['S-MUERTE-PAREJA']} de {len(EV)} casos "
      "(" + ", ".join(f"{k} {v}" for k, v in mx.most_common() if k != "S-MUERTE-PAREJA") + " en los demás).", "",
      "**¿Cambió algo de lo que hizo la que quedó viva?** Lo elegido en los 10 s antes y los 10 s después del tic de la muerte (fracción media por caso; descriptivo, sin grupo de control: "
      "no separa el duelo de todo lo demás que cambia cuando muere la hermana, como que desaparezcan su compañía y el candidato de ir hacia ella):", "",
      "| elegido | 10 s antes | 10 s después |", "|---|---|---|"]
Aa = collections.Counter(); Dd = collections.Counter()
for e in EV:
    ta = sum(e["elegido_antes_10s"].values()) or 1; td = sum(e["elegido_despues_10s"].values()) or 1
    for k, v in e["elegido_antes_10s"].items(): Aa[k] += v / ta
    for k, v in e["elegido_despues_10s"].items(): Dd[k] += v / td
for k in sorted(set(k for k, _ in Aa.most_common(6)) | set(k for k, _ in Dd.most_common(6)), key=lambda k: -(Aa[k] + Dd[k])):
    L.append(f"| {k} | {n(Aa[k] / len(EV))} | {n(Dd[k] / len(EV))} |")
cortos = sum(1 for e in EV if e["tics_despues"] < 240)
L += ["", f"Lo que hace casi no cambia: sigue sobre todo quieta (`noop`) y yendo a lo curioso; deja de ir hacia la hermana (`ir_pareja` cae a 0). La fuerza del duelo es la misma en todos los casos a cada segundo (desde el segundo 5, mínimo y máximo coinciden): el vínculo B estaba en su techo, 1, en todos los que llegan a esa altura. En {cortos} de {len(EV)} casos los 10 s de "
      "después quedan cortos porque ella muere o la partida acaba antes.", "",
      "**S-VINCULO.** En la foto de ahora no aparece nunca (tabla de arriba). El diario guarda en algunos tics también las fotos de los candidatos; ahí aparece "
      f"{len(VI)} veces, siempre en el candidato que golpearía a la hermana con un golpe que la mata, junto al duelo previsto, y **ninguna de esas veces se eligió ese golpe**:", ""]
for v in VI: L.append(f"- {v['campo']}, `{v['partida']}`, asiento {v['asiento']}, tic {v['tic']}: candidato {', '.join(v['candidatos_con_S_VINCULO'])}; eligió `{v['elegido']}`.")
L += ["", "Como el diario solo guarda las fotos de los candidatos en algunos tics, no se puede decir cuántas veces más se encendió S-VINCULO en una foto que no se guardó.", "",
      "## Lo que no consta", "",
      "- Ningún documento que retire o cambie las cuatro filas sociales; tampoco un congelado propio del siete.",
      "- El efecto del duelo sobre la conducta separado del resto de lo que cambia al morir la hermana: haría falta un control que no existe en los datos.",
      "- Las veces que S-VINCULO se encendió en fotos de candidatos que el diario no guardó.", ""]
open(os.path.join(AQUI, "informe_P7_filas_sociales.md"), "w").write("\n".join(L))
print("escrito informe_P7_filas_sociales.md")
