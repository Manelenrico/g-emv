# P7-23 · La primera etapa: nacer sin saber qué curan el botiquín ni la ración

*7-oct-2026. Coste: plataforma 0,2209 USD (el humo de 3 partidas); consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar;
cuerpo y congelados sin tocar; archivos nuevos con sufijo `_P7_23` (y un punto de enganche de una línea en `descubre_P7.py`, declarado abajo). Una vida por proceso en
el banco; la memoria viaja solo en el cuaderno. Este informe lo escribe `escribe_informe_P7_23.py` desde los JSON.*

## En corto

- **Construido y probado en banco:** F1 pasa (los 80 diarios de A4 con todo apagado y con TECHO sin pedir: 1.007.274 decisiones iguales y 2 distintas en cada brazo, las dos de siempre).
  F2 pasa: con el cuaderno vacío la imaginación pone cura 0 al botiquín y a la ración, k = 0 en los dos, no pide, no suelta, S-PROVISION y R-HERMANO-FALTA a 0; con tres usos de ración a mano,
  la esperanza del botiquín vale 15,0 (la creencia de la ración) y k = 0,30.
- **Humo de 3 días, brazo APRENDE, las dos criaturas:** en 5 de las 6 vidas toca primero por curiosidad (`ir_curioso` manda en los 30 s anteriores), 4 veces el botiquín y 1 la ración, hacia el tic 600;
  una criatura (día 1, asiento 11) murió en el tic 10.752 sin haber tocado ninguna de las dos. Las curas aprendidas empiezan pequeñas porque usa casi entera (vidas de 84-96 al usar en los días 1 y 2:
  efectos de 0 a 16, con «al menos»); el día 3 usa herida (47, 6, 15) y aprende curas de 50 y 15: la creencia del botiquín dentro del círculo pasa de 5,8 (día 1) a 30,5 (día 3, asiento 11).
  La esperanza aparece en cuanto conoce una de las dos (día 1, tic 10.610: la ración se imagina con la creencia del botiquín, 7,3). Pide poco (6 aperturas en 6 vidas) y suelta poco.
- **Créditos:** 0,2209 USD las 3 partidas (día 1 0,1115, día 2 0,0583, día 3 0,0512). El campo de 3 brazos × 20 días × 2 series = 120 partidas costaría unos 8,84 USD al precio medio del humo
  o 10,18 USD al precio medio real de P7-14b (0,08479 USD por partida sobre 160).

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

**F1** (`banco_P7_23.py --f1`, `P7_23_F1.json`): apagado 1.007.274 iguales / 2 distintas; TECHO sin pedir 1.007.274 / 2. Las dos distintas son las de siempre (P7-13, P7-19). **Pasa.**
(La primera pasada de F1 dio 86.104 distintas: el banco había puesto los ojos apagados también a los diarios de A4, que se jugaron con ojos; corregido en el banco, no en el cuerpo.)

**F2** (`banco_P7_23.py --f2`, `P7_23_F2.json`): 4 vidas de APRENDE de P7-14b (día 1) replicadas con la pieza encendida. La réplica sigue los pasos del diario, así que dice qué imagina
y qué elegiría el cuerpo que nace en esas escenas, no lo que habría pasado. Antes del primer uso de la vida:

*Cuaderno vacío:*

| vida (P7-14b, día 1, replicada) | tics antes del primer uso | cura imaginada máx. botiquín / ración | k máx. botiquín / ración | tics pidiendo | elige soltar | S-PROVISION y R-HERMANO-FALTA máx. | elige usar (por curiosidad) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `1_d1_APRENDE_34085144` asiento 10 | 11143 | — / 0,00 | 0,000 / 0,000 | 0 | 0 | 0,000 / 0,000 | 0 |
| `1_d1_APRENDE_34085144` asiento 11 | 10033 | 0,00 / — | 0,000 / 0,000 | 0 | 0 | 0,000 / 0,000 | 3 |
| `2_d1_APRENDE_36074995` asiento 10 | 9625 | 0,00 / 0,00 | 0,000 / 0,000 | 0 | 0 | 0,000 / 0,000 | 1 |
| `2_d1_APRENDE_36074995` asiento 11 | 1922 | 0,00 / — | 0,000 / 0,000 | 0 | 0 | 0,000 / 0,000 | 1 |

«Elige usar» con cura imaginada 0: el cuerpo usa por curiosidad (usar alivia la fila R-CURIOSIDAD, como manda el diseño). **Pasa.**

*Cuaderno con tres usos de ración a mano (efecto 15, el catálogo):*

| vida (P7-14b, día 1, replicada) | tics antes del primer uso | cura imaginada máx. botiquín / ración | k máx. botiquín / ración | tics pidiendo | elige soltar | S-PROVISION y R-HERMANO-FALTA máx. | elige usar (por curiosidad) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `1_d1_APRENDE_34085144` asiento 10 | 11148 | — / 6,80 | 0,300 / 0,758 | 144 | 0 | 0,000 / 0,000 | 1 |
| `1_d1_APRENDE_34085144` asiento 11 | 10033 | 15,00 / — | 0,300 / 0,758 | 4416 | 0 | 0,000 / 0,000 | 0 |
| `2_d1_APRENDE_36074995` asiento 10 | 9625 | 15,00 / 0,42 | 0,300 / 0,758 | 7584 | 0 | 0,000 / 0,000 | 1 |
| `2_d1_APRENDE_36074995` asiento 11 | 1922 | 15,00 / — | 0,300 / 0,758 | 144 | 0 | 0,000 / 0,000 | 3 |

La esperanza del botiquín vale 15,0 = la creencia vivida de la ración (regla: la media de lo que sabe de la clase), k = 0,3 = 15 / 50; la ración se imagina en menos de 15 porque
su propia esperanza (del botiquín desconocido) es 0 y la mezcla la descuenta. **Pasa.**

## Sección 3 · El humo (F3)

Serie 1, días 1 a 3, brazo APRENDE, semillas nuevas 36179724, 36284453, 36389182 (k = 152, 153, 154 de la sucesión de siempre, las siguientes a las de P7-14b). Imagen
`Dockerfile.pareja_P7_23` (una por día, con el cuaderno del anterior); diarios en `paintball/runs/P723_s1_d*_APRENDE_*/`; análisis `analiza_P7_23.py` → `P7_23_humo.json`.

| día · asiento | vive hasta | toca primero | tic | por qué | coge botiquín / ración | usos botiquín: n (completados, «al menos») · vida al usar · efecto | usos ración: idem | creencia al acabar botiquín / ración (por situación) | ignorancia botiquín / ración | recuerdos | esperanza: aparece en | pedidos (abre · tics) | elige soltar |
|---|---:|---|---:|---|---|---|---|---|---|---:|---|---|---|
| d1 · 10 | 12.744 | botiquin | 604 | curiosidad | 2 / 4 | 3 (2, 2) · 92, 84, 93 · 0, 16, 7 | 2 (2, 2) · 96, 95 · 7, 5 | dentro 5,8 / fuera 4,3 | 0,22 / 0,28 | 5 | tic 10.610, racion, vale 7,3 | 1 · 41 | soltar_rations 1 |
| d1 · 11 | 10.752 | nada | — | — | 0 / 0 | 0 (0, 0) ·  ·  | 0 (0, 0) ·  ·  | — / — | 1,00 / 1,00 | 0 | no aparece | 0 · 0 |  |
| d2 · 10 | 10.992 | racion | 538 | curiosidad | 0 / 3 | 0 (0, 0) ·  ·  | 1 (1, 1) · 90 · 13 | dentro 5,7 / fuera 4,3, dentro 6,6 | 0,23 / 0,23 | 6 | tic 10.286, racion, vale 7,3 | 1 · 219 | soltar_rations 2 |
| d2 · 11 | 10.525 | botiquin | 615 | curiosidad | 1 / 2 | 1 (1, 1) · 92 · 8 | 1 (1, 0) · 24 · 15 | dentro 4,0 / dentro 7,6 | 0,50 / 0,49 | 2 | tic 10.345, racion, vale 8,0 | 0 · 0 |  |
| d3 · 10 | 14.688 | botiquin | 593 | curiosidad | 5 / 11 | 4 (3, 1) · 92, 84, 47, 97 · 0, 16, 50, 0 | 4 (3, 0) · 92, 45, 45, 60 · 0, 0, 15, 0 | dentro 15,4 / fuera 4,2, dentro 7,0 | 0,13 / 0,16 | 11 | tic 9.255, botiquin, vale 12,8 | 2 · 23 | soltar_first_aid 2, soltar_rations 4 |
| d3 · 11 | 14.617 | botiquin | 4864 | curiosidad | 3 / 5 | 2 (2, 1) · 82, 6 · 18, 50 | 3 (3, 0) · 15, 30, 6 · 15, 15, 0 | dentro 30,5 / dentro 11,9 | 0,21 / 0,21 | 6 | tic 11.528, botiquin, vale 14,8 | 2 · 152 | hacer_sitio_first_aid_por_rations 1, soltar_rations 1 |

Lectura:
- **Qué toca primero y por qué:** 5 de 6 por curiosidad, hacia el tic 600 (el botiquín 4 veces, la ración 1); la sexta (día 1, asiento 11) eligió `ir_curioso` en 4.931 tics y murió en el 10.752 sin tocar nada.
- **Cuánta vida al usar y qué aprende:** los dos primeros días usa casi entera (vidas 84-96), y lo que aprende es lo que cabía hasta 100: efectos 0-16, marcados «al menos». El día 3 usa herida y aprende
  50 (botiquín) y 15 (ración). La ignorancia baja de 1 a 0,13-0,21 en tres días (asiento 10: 0,22 → 0,23 → 0,13 para el botiquín).
- **La esperanza:** aparece el día 1 (tic 10.610) para la ración, que se imagina con la creencia del botiquín (7,3); el día 3 el botiquín se imagina
  con la de la ración (12,8, 14,8). Los cortes se apuntan (día 1, asiento 10: el primer uso del botiquín fue un corte, efecto 0).
- **Pide y regala poco:** 6 pedidos abiertos en 6 vidas; `soltar_rations` 8 veces, `soltar_first_aid` 2, `hacer_sitio` 1.
- **Visto en el banco antes del humo, y dicho:** en una réplica con el cuaderno vacío el cuerpo elegía `soltar_rations` con el hermano al lado en 1.363 tics: la ración en el suelo
  alivia S-HERIDO y R-HERMANO-FALTA («medicina junto al hermano») pesada por lo poco aprendido de ella, y eso pesa más que la curiosidad perdida al soltarla. En el humo no se ha
  convertido en un problema (soltó raciones 8 veces en 6 vidas).

**GIF de los datos** (matplotlib, del diario): `P7_23_primer_uso_botiquin.gif` (día 1, asiento 10, tic 9.249: el primer uso del botiquín, que fue un corte) y
`P7_23_primer_uso_racion.gif` (tic 10.610, el primer uso de la ración, con la esperanza ya puesta).

## Sección 4 · Créditos (F4)

| | USD |
|---|---:|
| humo, día 1 | 0,1115 |
| humo, día 2 | 0,0583 |
| humo, día 3 | 0,0512 |
| **humo, total** | **0,2209** |
| campo de 3 brazos × 20 días × 2 series (120 partidas), al precio medio del humo (0,0736 por partida) | 8,84 |
| el mismo campo al precio medio real de P7-14b (0,08479 por partida, 160 partidas) | 10,18 |

Consola: 0. Acumulado del siete en la plataforma: 29,8359 + 0,2209 = 30,0568 USD. Saldos no consultados.

## Lo que queda para la mesa

1. El cuerpo que nace sin saber redescubre las dos cosas por curiosidad en el primer día y, cuando por fin usa herido (día 3), aprende las curas enteras; mientras usa entero aprende
   poco y «al menos». Tres días no bastan para decir a qué ritmo ni qué no recupera: eso es el campo.
2. La extensión de la curiosidad a dos clases (media de ignorancia × alivio; `ir_curioso` a la clase que más llama) y `W_TARGET` = 1 + k + k son decisiones de esta pieza; si la mesa quiere otra
   forma, es un número.
3. Soltar la ración poco conocida junto al hermano herido sale de lo aprendido (la medicina en el suelo) y en el humo ha sido raro; conviene mirarlo en el campo.
4. Jugar el campo son 120 partidas, unos 9-10 USD; pide sello nuevo.

## Archivos

| archivo | qué es |
|---|---|
| `recuerdo_P7_23.py`, `nace_P7_23.py`, `policy_pareja_P7_23.py` | el recuerdo marcado, la pieza de nacimiento y la política que la engancha |
| `descubre_P7.py` (una línea: `w_target`) | el punto de enganche del objetivo de riqueza |
| `banco_P7_23.py` → `P7_23_F1.json`, `P7_23_F2.json` | F1 y F2 |
| `Dockerfile.pareja_P7_23`, `lanza_P7_23.py`, `semillas_P7_23.json`, `P7_23_estado.json`, `P7_23_res/`, `cuadernos_P7_23/` | la imagen, el lanzador, las semillas, el estado y lo recogido del humo |
| `analiza_P7_23.py` → `P7_23_humo.json`; `gif_P7_23.py` → los dos GIF | F3 |
| `informe_P7_23.md` | este informe |
