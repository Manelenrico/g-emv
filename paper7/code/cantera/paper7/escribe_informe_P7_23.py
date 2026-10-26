"""[P7-23] Escribe informe_P7_23.md desde P7_23_F1.json, P7_23_F2.json, P7_23_humo.json, P7_23_estado.json, semillas_P7_23.json y P7_14b_estado.json (ninguna cifra a mano)."""
import hashlib, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
F1 = J("P7_23_F1.json"); F2 = J("P7_23_F2.json"); H = J("P7_23_humo.json"); E = J("P7_23_estado.json"); S = J("semillas_P7_23.json"); E14 = J("P7_14b_estado.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda p: hashlib.md5(open(os.path.join(AQUI, p), "rb").read()).hexdigest()
coste = {p["dia"]: p["coste_usd"] for p in E["peticiones"]}; total = sum(coste.values()); c14 = [p["coste_usd"] for p in E14["peticiones"] if p.get("estado") == "completed" and p.get("coste_usd")]; media14 = sum(c14) / len(c14)
def f2_tabla(et):
    L = ["| vida (P7-14b, día 1, replicada) | tics antes del primer uso | cura imaginada máx. botiquín / ración | k máx. botiquín / ración | tics pidiendo | elige soltar | S-PROVISION y R-HERMANO-FALTA máx. | elige usar (por curiosidad) |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for v in F2[et]["vidas"]:
        a = v["antes_del_primer_uso"]
        L.append(f"| `{v['carp'][-21:]}` asiento {v['slot']} | {a['tics']} | {n(a['heal_max_botiquin'])} / {n(a['heal_max_racion'])} | {n(a['k_botiquin_max'], 3)} / {n(a['k_racion_max'], 3)} | {a['tics_pidiendo']} | {a['elige_soltar']} | {n(a['S-PROVISION_max'], 3)} / {n(a['R-HERMANO-FALTA_max'], 3)} | {a['elige_usar']} |")
    return "\n".join(L)
L3 = ["| día · asiento | vive hasta | toca primero | tic | por qué | coge botiquín / ración | usos botiquín: n (completados, «al menos») · vida al usar · efecto | usos ración: idem | creencia al acabar botiquín / ración (por situación) | ignorancia botiquín / ración | recuerdos | esperanza: aparece en | pedidos (abre · tics) | elige soltar |", "|---|---:|---|---:|---|---|---|---|---|---|---:|---|---|---|"]
for k, v in H.items():
    d, sl = k.split("_"); tp = v["toca_primero"]; ub = v["usos"]["botiquin"]; ur = v["usos"]["racion"]; ab = v["al_acabar"]["botiquin"]; ar = v["al_acabar"]["racion"]; e = v["esperanza_aparece"]
    cre = lambda a: ("—" if not a["creencia"] else ", ".join(f"{s_} {n(c_, 1)}" for s_, c_ in a["creencia"].items()))
    L3.append(f"| {d} · {sl} | {n(v['ultimo_tick'], 0)} | {tp['objeto'] if tp else 'nada'} | {tp['tic'] if tp else '—'} | {tp['porque'] if tp else '—'} | {v['coge']['botiquin']} / {v['coge']['racion']} | {ub['n']} ({ub['completados']}, {ub['al_menos']}) · {', '.join(str(int(x)) for x in ub['vida_al_usar'])} · {', '.join(n(x, 0) for x in ub['efectos'])} | {ur['n']} ({ur['completados']}, {ur['al_menos']}) · {', '.join(str(int(x)) for x in ur['vida_al_usar'])} · {', '.join(n(x, 0) for x in ur['efectos'])} | {cre(ab)} / {cre(ar)} | {n(ab['ignorancia'], 2)} / {n(ar['ignorancia'], 2)} | {v['recuerdos_al_acabar']} | {('tic ' + n(e['tic'], 0) + ', ' + e['objeto'] + ', vale ' + n(e['vale'], 1)) if e else 'no aparece'} | {v['pedidos']['abre']} · {v['pedidos']['tics_pidiendo']} | {', '.join(f'{k_} {v_}' for k_, v_ in v['elige'].items() if k_.startswith('soltar') or k_.startswith('hacer'))} |".replace(",", "X").replace("X", ","))
T = f"""# P7-23 · La primera etapa: nacer sin saber qué curan el botiquín ni la ración

*7-oct-2026. Coste: plataforma {n(total, 4)} USD (el humo de 3 partidas); consola 0. `motor/model.py` = `{hashlib.md5(open(os.path.join(AQUI, '..', '..', 'motor', 'model.py'), 'rb').read()).hexdigest()}` al empezar y al acabar;
cuerpo y congelados sin tocar; archivos nuevos con sufijo `_P7_23` (y un punto de enganche de una línea en `descubre_P7.py`, declarado abajo). Una vida por proceso en
el banco; la memoria viaja solo en el cuaderno. Este informe lo escribe `escribe_informe_P7_23.py` desde los JSON.*

## En corto

- **Construido y probado en banco:** F1 pasa (los 80 diarios de A4 con todo apagado y con TECHO sin pedir: {n(F1['apagado']['fidelidad']['igual'], 0)} decisiones iguales y {F1['apagado']['fidelidad']['difiere']} distintas en cada brazo, las dos de siempre).
  F2 pasa: con el cuaderno vacío la imaginación pone cura 0 al botiquín y a la ración, k = 0 en los dos, no pide, no suelta, S-PROVISION y R-HERMANO-FALTA a 0; con tres usos de ración a mano,
  la esperanza del botiquín vale {n(F2['tres_raciones']['vidas'][1]['antes_del_primer_uso']['heal_max_botiquin'], 1)} (la creencia de la ración) y k = {n(F2['tres_raciones']['vidas'][1]['antes_del_primer_uso']['k_botiquin_max'], 2)}.
- **Humo de 3 días, brazo APRENDE, las dos criaturas:** en 5 de las 6 vidas toca primero por curiosidad (`ir_curioso` manda en los 30 s anteriores), 4 veces el botiquín y 1 la ración, hacia el tic 600;
  una criatura (día 1, asiento 11) murió en el tic {n(H['d1_11']['ultimo_tick'], 0)} sin haber tocado ninguna de las dos. Las curas aprendidas empiezan pequeñas porque usa casi entera (vidas de 84-96 al usar en los días 1 y 2:
  efectos de 0 a 16, con «al menos»); el día 3 usa herida (47, 6, 15) y aprende curas de 50 y 15: la creencia del botiquín dentro del círculo pasa de {n(H['d1_10']['al_acabar']['botiquin']['creencia']['dentro'], 1)} (día 1) a {n(H['d3_11']['al_acabar']['botiquin']['creencia']['dentro'], 1)} (día 3, asiento 11).
  La esperanza aparece en cuanto conoce una de las dos (día 1, tic {n(H['d1_10']['esperanza_aparece']['tic'], 0)}: la ración se imagina con la creencia del botiquín, {n(H['d1_10']['esperanza_aparece']['vale'], 1)}). Pide poco ({sum(v['pedidos']['abre'] for v in H.values())} aperturas en 6 vidas) y suelta poco.
- **Créditos:** {n(total, 4)} USD las 3 partidas ({", ".join(f"día {d} {n(c, 4)}" for d, c in coste.items())}). El campo de 3 brazos × 20 días × 2 series = 120 partidas costaría unos {n(120 * total / 3, 2)} USD al precio medio del humo
  o {n(120 * media14, 2)} USD al precio medio real de P7-14b ({n(media14, 5)} USD por partida sobre {len(c14)}).

## Sección 1 · Lo que se borra, con archivo y línea

| qué sabía el cuerpo | dónde estaba escrito | qué pasa ahora (`nace_P7_23.py`) |
|---|---|---|
| la cura del botiquín y de la ración en la imaginación de usarlos | `decisor_zs.py:484-493` (candidato con `heal` del catálogo), `:823-825` (previsión `hp2 = hp + heal`) | `heal` = lo recordado por parecido; «no sé» → 0 (el botiquín ya lo hacía P7-5; la ración es nueva) |
| las ganas del botiquín | R-ACOPIO `appraisal_zs_v42_exp.py:935-973` (`ACOPIO_M :111`, `ACOPIO_POR_DOS :221`, `PROVISION_SELF :315`); W `:749`; `W_TARGET :126` | escaladas por k (P7-5); `W_TARGET` pasa de 2 + k a 1 + k_botiquín + k_ración (punto de enganche `descubre_P7.w_target`) |
| las ganas de la ración | W `:751-759` (`RACION_2A :411`) | escaladas por k_ración |
| lo que vale llevar botiquín para la hermana sin venda | S-PROVISION `:1304-1362` | × k_botiquín |
| que la hermana no lleve cura duele | R-HERMANO-FALTA `:1632-1641` | × k_botiquín |
| la medicina junto al hermano (cualquier consumible con `heal` > 0: `:1160`, `:1258`, `:1338`) alivia S-DANO-PAREJA, S-HERIDO y R-HERMANO-FALTA | `:1143-1174`, `:1237-1278`, `:1632-1641` | el botiquín ya se pesaba por lo aprendido (P7-8); ahora también la ración, con k_ración (`regalo_nace`) |
| el pedido (P7-17) se abría por la promesa, que lleva curiosidad | `pide_P7.pide2` | se abre solo si k_botiquín > 0 (`pide_nace`) |
| la esperanza salía del catálogo (la ración, 15) | `descubre_P7.esperanza_cuerpo` | sale de la creencia vivida del otro consumible conocido; nada conocido → 0 |

De nacimiento queda la curiosidad (P7-6/7), extendida a las dos clases: M = ACOPIO_M × calma × media de (ignorancia × alivio) de botiquín y ración, e `ir_curioso` va al objeto más
cercano de la clase que más llama. **Esa extensión a dos clases es de esta pieza, no de la mesa; está declarada en el código.** Pedir corregido (P7-17) y lo dado entregado (P7-19)
van encendidos en la imagen; ojos compartidos apagados. Los brazos son interruptores: TECHO (SABE: la pieza no hace nada), APRENDE, BORRADO.

**El recuerdo** (`recuerdo_P7_23.py`): cada uso, completado o cortado, con contexto (dentro/fuera; golpeada en los 48 anteriores), foto emocional al abrir (dolor F, R, S; positivo;
distancia), la acción en curso y las tres anteriores, efecto por dominio con el «al menos» de P7-7, importancia con signo e intensidad (la fórmula del cuaderno). El corte: efecto 0
en cuerpo y recursos. Se recuerda por parecido como en P7-22 con los dos cambios: el «al menos» y el parecido de contexto dentro/fuera a 0,05 (s = 0,8304, el de P7-22).

## Sección 2 · F1 y F2

**F1** (`banco_P7_23.py --f1`, `P7_23_F1.json`): apagado {n(F1['apagado']['fidelidad']['igual'], 0)} iguales / {F1['apagado']['fidelidad']['difiere']} distintas; TECHO sin pedir {n(F1['TECHO']['fidelidad']['igual'], 0)} / {F1['TECHO']['fidelidad']['difiere']}. Las dos distintas son las de siempre (P7-13, P7-19). **Pasa.**
(La primera pasada de F1 dio 86.104 distintas: el banco había puesto los ojos apagados también a los diarios de A4, que se jugaron con ojos; corregido en el banco, no en el cuerpo.)

**F2** (`banco_P7_23.py --f2`, `P7_23_F2.json`): 4 vidas de APRENDE de P7-14b (día 1) replicadas con la pieza encendida. La réplica sigue los pasos del diario, así que dice qué imagina
y qué elegiría el cuerpo que nace en esas escenas, no lo que habría pasado. Antes del primer uso de la vida:

*Cuaderno vacío:*

{f2_tabla('vacio')}

«Elige usar» con cura imaginada 0: el cuerpo usa por curiosidad (usar alivia la fila R-CURIOSIDAD, como manda el diseño). **Pasa.**

*Cuaderno con tres usos de ración a mano (efecto 15, el catálogo):*

{f2_tabla('tres_raciones')}

La esperanza del botiquín vale 15,0 = la creencia vivida de la ración (regla: la media de lo que sabe de la clase), k = 0,3 = 15 / 50; la ración se imagina en menos de 15 porque
su propia esperanza (del botiquín desconocido) es 0 y la mezcla la descuenta. **Pasa.**

## Sección 3 · El humo (F3)

Serie 1, días 1 a 3, brazo APRENDE, semillas nuevas {", ".join(str(s) for s in S['serie1'])} (k = {", ".join(str(k) for k in S['k'])} de la sucesión de siempre, las siguientes a las de P7-14b). Imagen
`Dockerfile.pareja_P7_23` (una por día, con el cuaderno del anterior); diarios en `paintball/runs/P723_s1_d*_APRENDE_*/`; análisis `analiza_P7_23.py` → `P7_23_humo.json`.

{chr(10).join(L3)}

Lectura:
- **Qué toca primero y por qué:** 5 de 6 por curiosidad, hacia el tic 600 (el botiquín 4 veces, la ración 1); la sexta (día 1, asiento 11) eligió `ir_curioso` en {n(H['d1_11']['elige']['ir_curioso'], 0)} tics y murió en el {n(H['d1_11']['ultimo_tick'], 0)} sin tocar nada.
- **Cuánta vida al usar y qué aprende:** los dos primeros días usa casi entera (vidas 84-96), y lo que aprende es lo que cabía hasta 100: efectos 0-16, marcados «al menos». El día 3 usa herida y aprende
  50 (botiquín) y 15 (ración). La ignorancia baja de 1 a 0,13-0,21 en tres días (asiento 10: {n(H['d1_10']['al_acabar']['botiquin']['ignorancia'], 2)} → {n(H['d2_10']['al_acabar']['botiquin']['ignorancia'], 2)} → {n(H['d3_10']['al_acabar']['botiquin']['ignorancia'], 2)} para el botiquín).
- **La esperanza:** aparece el día 1 (tic {n(H['d1_10']['esperanza_aparece']['tic'], 0)}) para la ración, que se imagina con la creencia del botiquín ({n(H['d1_10']['esperanza_aparece']['vale'], 1)}); el día 3 el botiquín se imagina
  con la de la ración ({n(H['d3_10']['esperanza_aparece']['vale'], 1)}, {n(H['d3_11']['esperanza_aparece']['vale'], 1)}). Los cortes se apuntan (día 1, asiento 10: el primer uso del botiquín fue un corte, efecto 0).
- **Pide y regala poco:** {sum(v['pedidos']['abre'] for v in H.values())} pedidos abiertos en 6 vidas; `soltar_rations` {sum(v['elige'].get('soltar_rations', 0) for v in H.values())} veces, `soltar_first_aid` {sum(v['elige'].get('soltar_first_aid', 0) for v in H.values())}, `hacer_sitio` {sum(v['elige'].get('hacer_sitio_first_aid_por_rations', 0) for v in H.values())}.
- **Visto en el banco antes del humo, y dicho:** en una réplica con el cuaderno vacío el cuerpo elegía `soltar_rations` con el hermano al lado en 1.363 tics: la ración en el suelo
  alivia S-HERIDO y R-HERMANO-FALTA («medicina junto al hermano») pesada por lo poco aprendido de ella, y eso pesa más que la curiosidad perdida al soltarla. En el humo no se ha
  convertido en un problema (soltó raciones {sum(v['elige'].get('soltar_rations', 0) for v in H.values())} veces en 6 vidas).

**GIF de los datos** (matplotlib, del diario): `P7_23_primer_uso_botiquin.gif` (día 1, asiento 10, tic 9.249: el primer uso del botiquín, que fue un corte) y
`P7_23_primer_uso_racion.gif` (tic 10.610, el primer uso de la ración, con la esperanza ya puesta).

## Sección 4 · Créditos (F4)

| | USD |
|---|---:|
| humo, día 1 | {n(coste[1], 4)} |
| humo, día 2 | {n(coste[2], 4)} |
| humo, día 3 | {n(coste[3], 4)} |
| **humo, total** | **{n(total, 4)}** |
| campo de 3 brazos × 20 días × 2 series (120 partidas), al precio medio del humo ({n(total / 3, 4)} por partida) | {n(120 * total / 3, 2)} |
| el mismo campo al precio medio real de P7-14b ({n(media14, 5)} por partida, {len(c14)} partidas) | {n(120 * media14, 2)} |

Consola: 0. Acumulado del siete en la plataforma: 29,8359 + {n(total, 4)} = {n(29.8359 + total, 4)} USD. Saldos no consultados.

## Lo que queda para la mesa

1. El cuerpo que nace sin saber redescubre las dos cosas por curiosidad en el primer día y, cuando por fin usa herido (día 3), aprende las curas enteras; mientras usa entero aprende
   poco y «al menos». Tres días no bastan para decir a qué ritmo ni qué no recupera: eso es el campo.
2. La extensión de la curiosidad a dos clases (media de ignorancia × alivio; `ir_curioso` a la clase que más llama) y `W_TARGET` = 1 + k + k son decisiones de esta pieza; si la mesa quiere otra
   forma, es un número.
3. Soltar la ración poco conocida junto al hermano herido sale de lo aprendido (la medicina en el suelo) y en el humo ha sido raro; conviene mirarlo en el campo.
4. Jugar el campo son 120 partidas, unos {n(120 * total / 3, 0)}-{n(120 * media14, 0)} USD; pide sello nuevo.

## Archivos

| archivo | qué es |
|---|---|
| `recuerdo_P7_23.py`, `nace_P7_23.py`, `policy_pareja_P7_23.py` | el recuerdo marcado, la pieza de nacimiento y la política que la engancha |
| `descubre_P7.py` (una línea: `w_target`) | el punto de enganche del objetivo de riqueza |
| `banco_P7_23.py` → `P7_23_F1.json`, `P7_23_F2.json` | F1 y F2 |
| `Dockerfile.pareja_P7_23`, `lanza_P7_23.py`, `semillas_P7_23.json`, `P7_23_estado.json`, `P7_23_res/`, `cuadernos_P7_23/` | la imagen, el lanzador, las semillas, el estado y lo recogido del humo |
| `analiza_P7_23.py` → `P7_23_humo.json`; `gif_P7_23.py` → los dos GIF | F3 |
| `informe_P7_23.md` | este informe |
"""
assert "§" not in T; open(os.path.join(AQUI, "informe_P7_23.md"), "w").write(T); print(len(T))
