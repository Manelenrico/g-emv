# Prompt 163: el desempate de la medida en sombra, qué cifras dependen de él, cuánto pesa, y lo heredado

*22-nov-2026. Solo lectura: no se ha jugado ni rejugado ninguna partida, no se ha editado ningún fichero existente y no se ha tocado nada de `cantera/paper9` (solo se han leído partidas que el chat de la curiosidad ya había rejugado). Antes de empezar no había nada del chat de la curiosidad en marcha: ningún proceso de Python.*

## Resumen

- **Qué hace la línea 79** (leído del código): si queda un empate exacto y lo que la criatura eligió en la partida está entre las empatadas, la sombra da como ganadora lo elegido. Va después de dos reglas que la criatura también tiene: seguir con lo que hacía y quedarse. **Hace el papel del sorteo de la criatura que juega.** La criatura sortea entre las empatadas (`cuerpo_valle.py:2992-3000`); la sombra, en vez de eso, se queda con lo elegido.
- **Dónde está** (leído): es una función, `desempata`. Está en `lanza_experimento_v2.py:53-67` (prompt 99) y en su copia `medida_v3/lanza_medida_v3.py:66-80` (prompt 101). La copia es la que importan los lanzadores de los experimentos v3, v4, v5 y v6 y el del taller de la voz. No hay ningún fichero `medida_v1` ni `medida_v2`. La medida anterior, la de los prompts 71 y 72, no tenía la línea 79. Otros cuatro programas usan la misma idea con código propio: la voz, la razón callada, la causa de dormir fuera y por qué no come.
- **Qué cifras dependen de ella** (leído): P11 del v2 al v5 y M9 del v6, es decir, cuánto coinciden la criatura y «las sumas». **Ninguna pieza se aceptó ni se rechazó con la sombra:**
  - P11 era una predicción sellada sobre los valoradores, y M9 es una medida sin predicción;
  - **la reserva (prompt 146) y la voz de ir a casa (prompt 143), y las dos juntas (147), se aceptaron con partidas jugadas**, 60 en cada taller.
  - De los informes 153 a 162, solo el 162 cita cifras de la sombra: los resultados de P11 en la historia de los sellados.
- **Cuánto pesa** (contado, sin rejugar). Leí diez partidas selladas de la protagonista del v6 que el C6b ya había rejugado; tienen 499 338 decisiones de día.
  - Las sumas coinciden con lo elegido en el 65,0 %. En 11 180 de esas coincidencias (el 3,4 %) había un empate exacto que la criatura habría echado a suertes, y la sombra lo cuenta como coincidencia. Sería «no cambia» solo por la línea 79.
  - Con el motor (la comprobación interna del 100 %), son 18 385, el 3,7 %.
  - En la muestra de M9, esas decisiones son algo más en Q4 (3 de 71) que en Q1 (3 de 110). Como mucho moverían Q4 − Q1 en 1,5 puntos, frente a los +19,8 de M9. **Es una indicación, no una medida**: solo 311 decisiones de la muestra caen en esas diez partidas y son de día.
  - Para el resto (P11 del v2 al v5, las noches, las otras 190 partidas del v6, la voz, la razón, dormir fuera, por qué no come) hay que rejugar. Digo qué haría falta y cuánto tardaría.
- **Lo heredado** (leído del código): son 31 recuerdos. 22 se leen al decidir (3 de ellos también al aprender) y 9 entran y no se usan. Entre los que no se usan están **los dos hechos del árbol dulce**. El de **las bestias y las épocas** ni siquiera le llega: el cargador lo descarta (`cuerpo_valle.py:565`).
- **Gasto:** 0 créditos de la plataforma y 0 dólares de la consola.

---

## Parte 1. La medida en sombra (leído del código)

### Qué hace exactamente el desempate

La función es `desempata(c, nombres, preds, e, ult, elegida)`, en `medida_v3/lanza_medida_v3.py:66-80`. Se llama en `:94` con cada uno de los tres valoradores (el motor, las sumas y la posición). Entra `e`, la ganadora que da el planificador con los valores de ese valorador (`planificador_v1.select_tiebreak`, `planificador/planificador_v1.py:433`), y luego:
1. **Seguir con lo que hacía** (`:70-75`), si la criatura tiene `empates_sigue_v23` y una acción anterior. Mira las opciones que empatan con `e` (a 1e-9, o con el margen `empate_margen_v24` si lo tiene). Si alguna es la misma acción que hacía, o de la misma clase, y `e` no lo es, gana la primera de esas.
2. **Quedarse** (`:76-78`), si la criatura tiene `empate_quedarse_v47`. Si «quedarse» está entre las empatadas exactas (1e-9) y la ganadora no es quedarse, gana quedarse.
3. **La línea 79:** `if len(tie) > 1 and elegida in tie: return elegida`. Si sigue habiendo más de una empatada y lo que la criatura eligió de verdad está entre ellas, gana lo elegido.
4. Si no, gana `e`. Para el planificador, en un empate exacto `e` es la primera por el orden de las opciones (`planificador_v1.py:361-373`).

`elegida` es lo que la criatura eligió en la partida (`f0`, `:85-91`). Con el motor de la criatura, la línea 79 reproduce su sorteo. Con otro valorador (las sumas, la posición), **cuenta como «igual» cualquier empate en el que esté lo elegido**, aunque una criatura con ese valorador lo habría echado a suertes.

### Cómo deshace un empate exacto la criatura cuando juega

En `cuerpo_valle.py:2979-3001` (la protagonista RG69r+voz lleva `empates_sigue_v23`, `empate_suertes_v42` y `empate_quedarse_v47`):
1. **La ganadora del planificador** (`:2979`).
2. **Seguir con lo que hacía** (`:2983-2988`), la misma regla que el paso 1 de arriba.
3. **Quedarse** (`:2989-2991`), la misma que el paso 2.
4. **El sorteo** (`:2992-3000`), si no ha ganado quedarse.
   - Toma las empatadas exactas con la ganadora. Si estaba siguiendo algo y la ganadora es de las de seguir, solo esas.
   - Si son más de una, elige entre ellas al azar: `self._rng_empate.choice(sorted(tie))`. Su azar es propio, `random.Random(f"{semilla_partida}|{agente}")` (`:525`).

**La única diferencia es el paso 4.** La sombra pone lo elegido donde la criatura sortea. Las dos primeras reglas son las mismas.

### Dónde se usa esa medida, o una copia

**a) La misma función, con la línea 79:**

| programa | prompt | qué hace con ella |
|---|---|---|
| `lanza_experimento_v2.py:53-67` (la línea es la `:66`) | 99 | el original: el experimento v2, RG50r |
| `medida_v3/lanza_medida_v3.py:66-80` | 101 | la copia con el registro de decisiones arreglado; rejugó las 200 de RG50r |
| `lanza_experimento_v3.py:62` (`LM.una`, preguntar en RG58r) | 113 | el registro de decisiones del v3 |
| `lanza_experimento_v4.py:74` (RG61r) | 117 | el del v4 |
| `lanza_experimento_v5.py:74` (RG68r) | 134 | el del v5 |
| `lanza_experimento_v6.py:50` (la protagonista, RG69r+voz) | 149-150 | el del v6 |
| `lanza_vc1.py:45` (preguntar=True, también en VC1) | 143 | el taller de la voz |
| `medida_v3/rejuega_fotos.py`, `arreglos_v8/lanza_v13.py`, `arreglos_v9/lanza_v9.py` a `arreglos_v12/lanza_v12.py`, `voz_v1/lanza_voz.py`, `voz_v2/lanza_voz2.py` | 101, 115, 128-132, 123-124 | importan el lanzador con preguntar apagado: **no usan la sombra** |

Lo guardado (`decisiones.jsonl.gz`: lo elegido, el motor, las sumas, la posición y si cada uno coincide) lo leen para P11 y M9:
- `evalua_experimento_v2.py` a `evalua_experimento_v5.py` (la función `p11`), y `evalua_experimento_v6.py` (M9, con la de v5);
- `medida_v3/p11_v3.py`, `diagnostico_v4/p11_diag.py` y `juntos_v1/m9_v1.py`.

Otros programas leen el mismo fichero, pero **solo la columna de lo elegido de verdad**, que no depende del desempate:
- `dormir_fuera_v5/noches_v5.py` y `hambre_ganancias_v1/extrae_hg_v1.py`;
- `hermana_casa_hambre_v1/sigue_v1.py` y `exploracion_v2/*.py`;
- `voz_a_casa_v1/*.py` y los `mira_*`.

Fuera del ocho, el chat de la curiosidad (`cantera/paper9`, prompts C4 a C7) importa la misma función.

**b) La medida de antes, sin la línea 79** (las que harían de «medida v1»; no hay ficheros con ese nombre):
- `lanza_confirmacion.py:26-33` (prompt 72) y `explora_v1.py:24-31` (prompt 71). Solo tienen la regla de seguir con lo que hacía y, si no, el orden del planificador.
- Esas criaturas (RG32r y sus gemelas) aún no tenían sorteo ni la regla de quedarse; llegaron en los prompts 87 y 93 (`banco_v7.py:191`, `:208`). Así que en ellas la sombra era la misma regla de la criatura. El informe lo comprueba: «cada clase coincide al 100 % con su propio valorador» (`informe_confirmacion_v1.md:47`).

**c) La misma idea con código propio** («si lo elegido empata con la mejor, lo elegido», sin la regla de quedarse):

| programa | prompt | qué compara |
|---|---|---|
| `cuerpo_vc1.py:88-89` | 143, 147, v6 | lo que habría elegido sin haber oído la voz frente a lo elegido oyéndola («cambio») |
| `cuerpo_rz1.py:167-170` | 139 | lo que habría elegido sin las filas de promesa de la razón |
| `lanza_causa_v1.py:57-60` | 141 | sin ninguna fila de ganancia; quitando una sola; con las fuerzas de prueba en dormir o en ir a casa |
| `lanza_pnc_v1.py:39-42` | 145 | qué fila, quitada sola, haría ganar a comer |

**d) Otros que valoran decisiones de partidas ya jugadas, sin elegir una ganadora con desempate:**
- `medida_v3/analiza_fotos.py`: «fila decisiva»; un empate cuenta como perder (`:66`, `>=`).
- `medida_v3/dar_motor_sumas.py`: dar gana con las sumas por menos estricto (`<`).
- `fractal_v1/acciones_filas.py`.
- `diag_foto_v47.py`, `hambre_v35.py` y `cuenta_gusto_v42.py`: el margen con la mejor otra, filas.
- `hermana_casa_hambre_v1/promesa_vinculo_v1.py` (prompt 142): recalcula sobre lo guardado en el 141.
- `mesa_dilemas.py` (74-75) valora estados montados a mano, no partidas jugadas.

Ninguno usa la línea 79.

---

## Parte 2. Qué números dependen de ella (leído de los informes)

| prompt | informe | qué se medía con la sombra | con qué desempate | ¿se usó para aceptar o rechazar una pieza? |
|---|---|---|---|---|
| 71 | `informe_exploracion_v1.md` | motor frente a sumas en el mismo estado (exploración) | sin la línea 79 (b) | no: exploración |
| 72 | `informe_confirmacion_v1.md` | C3, C5 y C6: coincidencia entre valoradores (C3 −0,116, C5 −0,136, C6 −0,046; se cumplen) | sin la línea 79 (b) | no: predicciones selladas sobre los valoradores |
| 99 | `informe_experimento_v2.md:57` | P11: RG50r y las sumas, Q4 − Q1 = −0,131, se cumple | **con la línea 79** | no: predicción sellada |
| 100 | `informe_exploracion_v2.md` | P11 sin las decisiones de ir; los nombres de lo elegido | con la línea 79 / solo lo elegido | no |
| 101 | `informe_medida_v3.md:53-58` | P11 con todas las decisiones: −0,128, se cumple | **con la línea 79** | no: predicción |
| 113 | `informe_experimento_v3.md:59` | P11: RG58r, +0,132, **falla** | **con la línea 79** | no: predicción |
| 114 | `informe_diagnostico_v4.md` | por qué P11 sale al revés (Q1 y Q4) | **con la línea 79** | no: diagnóstico; sirvió para escribir la P11 del v4 |
| 117 | `informe_experimento_v4.md:56` | P11: RG61r, +0,143 y −0,115 sin dar, se cumple | **con la línea 79** | no: predicción |
| 134 | `informe_experimento_v5.md:49` | P11: RG68r, +0,042 y −0,175 sin dar, se cumple | **con la línea 79** | no: predicción |
| 139 | `informe_razon_piloto_v1.md:97`, `:132` | «cambió lo elegido por las filas»: 840 de unas 20 000 | (c), `cuerpo_rz1` | no: piloto sin regla; la razón no está en la protagonista |
| 141 | `informe_dormir_fuera_causa_v1.md:53-77`, `:149` | lo que habría elegido sin ganancias, o quitando una (2 299 y 8 250 decisiones; 1 160 de 4 708) | (c), `lanza_causa_v1` | no: diagnóstico |
| 142 | `informe_hermana_casa_hambre_v1.md` | la prueba de fuerzas con una promesa de vínculo, sobre lo guardado en el 141 | (d) | no: diagnóstico |
| 143 | `informe_voz_a_casa_v1.md:46`, `:77` | «lo oído cambia lo elegido» en el 9-15 % de las decisiones oyendo; en la prueba de 10 días, 226 de 2 445 | (c), `cuerpo_vc1` | **no: la voz se aceptó con 60 partidas jugadas** (noches fuera, vivas, felicidad, empujones) |
| 145 | `informe_por_que_no_come_v1.md` | las filas que, quitadas, harían ganar a comer | (c), `lanza_pnc_v1` | no: diagnóstico; dijo dónde tocar para la reserva |
| 146 | `informe_reserva_v1.md` | — (la regla, con partidas jugadas) | — | **la reserva se aceptó con 60 partidas jugadas**; ninguna cifra de la sombra |
| 147 | `informe_voz_reserva_v1.md:98` | la columna «decisiones oyendo en que cambió lo elegido» | (c), `cuerpo_vc1` | **no: RG69r+voz se aceptó con partidas jugadas**; esa columna es descriptiva |
| 149 | `informe_preparacion_v6.md:77`, `:115` | define M9 (sin cifra) | — | no |
| 150 | `informe_experimento_v6.md:139`, `:157` | M9: +0,198, −0,026 sin dar; la voz «cambia lo elegido» en el 6-14 % de las decisiones oyendo | **con la línea 79** (M9); (c) (la voz) | no: M9 es una medida sin predicción (`predicciones_selladas_v6.md:53`) |
| 151 | `informe_v5_y_v6_juntos.md:176-223` | M9 y P11 separadas por tipo de decisión | **con la línea 79** | no: análisis después de ver los datos |
| 162 | `informe_prompt_162.md:249-270` | cita P11 en la historia de los sellados, y el recuento de predicciones cumplidas y falladas que la incluye | **con la línea 79** (citado) | no |

Además:
- los diagnósticos de fotos de los prompts 80, 87, 92, 101 y 102 son del grupo (d), sin la línea 79;
- los arreglos de los prompts 103 a 132 se juzgaron con partidas de prueba jugadas.

**La reserva y la voz de ir a casa, expresamente:**
- **La reserva** (prompt 146) se aceptó con su regla sobre 60 partidas jugadas de 40 días: turnos con hambre y comida en la bolsa, vivas, felicidad y empujones. No usa la sombra.
- **La voz de ir a casa** (prompt 143) también, con 60 partidas jugadas: noches fuera, vivas, felicidad y empujones.
  - Su informe da cifras de una sombra de la familia (c): «lo oído cambia lo elegido».
  - Una de esas cifras sale en la prueba de 10 días que dio paso al taller («226 de 2 445»; «todo lo que pedía el prompt apareció, así que se siguió»). El informe no dice si esa cifra era una de las condiciones.
  - La regla que la aceptó no usa ninguna cifra de la sombra.
- **Las dos juntas** (147) se aceptaron igual, con partidas jugadas.

**Los informes 153 a 162, uno por uno** (leí cada informe y busqué en sus programas el registro de decisiones, el de la voz, el de candidatos y el de no come):
- **153:** no. Tablas y figuras de la escalera, de partidas jugadas (`analiza_tablas_paper8.py` y `evalua_escalera_v6`).
- **154:** no. La escalera y su GIF.
- **155:** no. La felicidad de las vivas y el GIF.
- **156:** no. La felicidad día a día.
- **157:** no. Los tramos y los ritmos.
- **158:** no. El GIF v4.
- **159:** no hay informe.
- **160:** no. La bestia, el huerto y los días sin fruto, de los registros del mundo.
- **161:** no. Los días de cosecha (del registro `balance`), lo heredado leído del código y las figuras.
- **162:** no mide nada con la sombra. Pero **cita** los resultados de P11 del v2 y del v3 y el recuento de predicciones de cada sellado, que incluye P11 (`:249-270`). Toma de `noches_v5.py` solo la definición de la noche.

---

## Parte 3. Cuánto pesa

### Lo contado, sin rejugar (`empates_sombra_163.py` → `salida/empates_sombra_163.md` y `.json`)

**De dónde salen los valores.** El registro de decisiones del ocho solo guarda nombres, no valores, así que con él solo no se pueden contar los empates. Pero el chat de la curiosidad ya rejugó (prompt C6b) diez partidas selladas de la protagonista del v6: los cinco mundos, semillas 30161 y 30162.
- Salieron idénticas a las selladas.
- Apuntaron, en cada decisión de día (mañana y tarde), lo que elegirían el motor y las sumas con la misma función `desempata`, y cuántas opciones empataban.

El programa nuevo lee esas diez sin tocarlas y las cruza con el registro sellado del v6.

**Las comprobaciones (contado):**
- Las 499 338 decisiones de día se cruzan todas. Lo elegido, el motor y las sumas del registro sellado son los de la sombra rejugada en las 499 338; no casan 0. Las columnas «coincide» del registro y de la sombra no difieren en ninguna.
- La muestra de M9 rehecha da Q4 − Q1 = +0,1975, lo mismo que guardó el evaluador del v6.

**Lo que sale (contado).** Las diez partidas, decisiones de día:

| valorador | decisiones | coincide con lo elegido | lo elegido, empatado con otra | coincide y estaba empatado | de ellas, la criatura lo habría echado a suertes |
|---|---|---|---|---|---|
| motor (la comprobación interna) | 499 338 | 499 338 (100 %) | 31 390 (6,3 %) | 31 390 | **18 385 (3,7 %)** |
| sumas (M9) | 499 338 | 324 380 (65,0 %) | 17 392 (3,5 %) | 17 392 (5,4 % de las que coinciden) | **11 180 (3,4 % de las que coinciden)** |

**Cómo se lee:**
- **«Coincide solo por el desempate», en sentido estricto:** son las de la última columna, las que la criatura habría echado a suertes. Ahí la línea 79 da «igual» siempre, y una criatura con ese valorador acertaría solo a veces (1 entre las empatadas).
- **Las demás empatadas** (17 392 − 11 180 = 6 212 en las sumas) las deshacen las reglas de seguir o de quedarse. Son las mismas que usa la criatura, así que no son culpa de la línea 79.
- **El estricto de otra manera:** coincide, pero con la regla de la criatura ganaría otra. Da 0 en los dos valoradores. Tiene que ser así: la regla de quedarse va antes de la línea 79, dentro de la misma función.
- **El motor coincide al 100 %** (la comprobación interna de P11 y M9). En el 3,7 % de las decisiones lo asegura la línea 79, que repite el sorteo con lo que salió.

**Por mundo (las sumas):** las que la criatura habría echado a suertes son entre el 3,0 % y el 4,6 % de las decisiones; la tabla completa está en `salida/empates_sombra_163.md`.

**Por tipo de decisión** (los tipos de `m9_v1.py`; las sumas):

| tipo | decisiones | coincide | a suertes |
|---|---|---|---|
| dar | 122 070 | 243 | 33 |
| comer | 15 226 | 6 027 | 21 |
| ir | 87 548 | 66 769 | 6 566 |
| el resto | 274 494 | 251 341 | 4 560 |

**En la muestra de M9** (las 311 decisiones de la muestra que caen en estas diez partidas y son de día):

| cuarto | decisiones | coinciden | a suertes |
|---|---|---|---|
| Q1 (la menos ambivalente) | 110 | 56 (50,9 %) | 3 |
| Q4 (la más) | 71 | 59 (83,1 %) | 3 |

Si esas decisiones contaran como «no coincide» (el peor caso), Q1 bajaría al 48,2 % y Q4 al 78,9%. Q4 − Q1 pasaría de +32,2 a +30,7 puntos en esta submuestra: como mucho, 1,5 puntos menos. M9 es +19,8. Con 311 decisiones esto es **una indicación**, no una medida de M9.

### Lo que no se puede contar sin rejugar, qué haría falta y cuánto tardaría (estimado)

**Qué haría falta.** Un lanzador nuevo, copia de `lanza_medida_v3.py`, que en `pregunta` apunte además, con cada valorador, cuántas opciones empatan con lo elegido y si la criatura las habría echado a suertes. Así lo hizo `lanza_C6b.py`, sin tocar la criatura. Después, comprobar línea a línea que cada partida rejugada es la sellada.

**La base de los tiempos.** El C6b rejugó 10 partidas de 40 días, las 10 a la vez, en 23 minutos. Una tanda de 10 partidas son unos 20-25 minutos; 200 partidas, 20 tandas.

| qué | partidas que rejugar | tiempo estimado (10 a la vez) |
|---|---|---|
| M9 del v6 entero, también las noches (RG69r+voz) | 200 (o las 190 que faltan, más las noches de las diez) | unas 7-8 h |
| P11 del v5 (RG68r) | 200 | unas 7-8 h |
| P11 del v4 (RG61r) | 200 | unas 7-8 h |
| P11 del v3 (RG58r) | 200 | unas 7-8 h |
| P11 del v2 (RG50r; las 200 de la medida v3) | 200 | unas 6-7 h (era más rápida) |
| La voz: «lo oído cambia lo elegido» (143; 147 y v6 aparte) | 60 del taller del 143 | unas 2-2,5 h; la 147 otras 2-2,5 h; la voz del v6, con el v6 de arriba |
| Dormir fuera sin ganancias (141) | 6 partidas de 10 días | unos 10 min |
| Por qué no come (145) | 10 partidas de 10 días | unos 10-15 min |
| La razón callada (139) | 3 partidas del piloto | además del tiempo, llama al modelo de lenguaje: costaría dólares de la consola si no se guardaron sus respuestas, así que no lo propongo sin Manel |

**Si se quisiera todo** (P11 del v2 al v5 y M9 del v6 enteros), son unas 35-40 horas de máquina. Lo más útil y corto sería M9 del v6 entero, unas 7-8 h, porque es la cifra que va al paper.

---

## Parte 4. Lo heredado (leído del código)

**De dónde sale la lista.** En el repositorio no he encontrado un borrador del paper del ocho. Las «treinta y una cosas» son la lista del `informe_prompt_161.md:280-315`, y la he tomado de ahí.

**La protagonista.** Es la clase `cuerpo_vr1.RG69V`, que hereda de VC1, RG69 y `cuerpo_valle.Criatura`:
- sus interruptores son los de `banco_v7.VARS["RG68r"]` más `reserva_v69` y `a_casa` (`lanza_experimento_v6.py:33`, `lanza_vr1.py:20`);
- su cultura es `cultura_matorrales_medio.json`.

**El recuento.** `salida/lee_criatura_161.json`, que ya existía, da 31 recuerdos con origen «heredado» en cada criatura. Las lecturas las buscó un agente leyendo el código, sin ejecutar nada. Yo comprobé lo de los hechos y el árbol: ninguna línea del código de la criatura ni del cuaderno lee una clave «hecho:…», y `cuerpo_valle.py:565` descarta las épocas.

**Tres cosas que cambian lo que cuenta como «se lee»:**
- **La regla general quita cinco filas** (`_filas_rg`, `cv:2188`): F-ANTICIPACION, R-LLAMADA, R-CURIOSIDAD, la del cuánto y R-ENFADO. Lo que solo llega a esas filas no cuenta.
- **Apuntar no es leer.** Al apuntar algo vivido, el cuaderno guarda la creencia de antes (con lo heredado dentro) en `creencia_antes`, pero nadie la vuelve a leer. Y `junta` deja fuera lo heredado (`cu:45`). Eso cuenta como «solo se apunta», no como aprender.
- **Lo heredado no se olvida** (`cu:60-61`, `cv:352`): pesa 1 en cada media, junto con lo vivido, siempre que se lee esa creencia.

`cv` = `cantera/paper8/cuerpo_valle.py`; `cu` = `cantera/paper7/cuaderno_P7.py`.

| # | entrada | clave (cosa · situación) | valor | entra en | se lee en | marca |
|---|---|---|---|---|---|---|
| 1 | una comida quita hambre | comida · valle | cuerpo 35 | cv:541-552 | `cree_comida` (cv:2708-2722), en la foto de comer y en `comidas_dos_dias` (cv:2308: R-CARENCIA, V-RECURSOS) | al decidir |
| 2 | la medicina cura | medicina · valle | cuerpo 40 | cv:541-552 | decidir: cv:1651, 2193, 2643, 2705; aprender: cv:1901 (al dar una medicina) | al decidir y al aprender |
| 3 | la zona salvaje hiere, de día | sitio:salvaje · día | −0,05 · 0,5 · 0; da medicina 0,5 | cv:541-552 | `dano_sitio` (cv:849) en la foto (cv:2526) y en la amenaza (cv:912); `fuentes_sitio` (cv:923) para ir a por botín. El «da medicina» no lo lee nada | al decidir |
| 4 | la zona salvaje hiere, de noche | sitio:salvaje · noche | igual | cv:541-552 | igual que la 3 | al decidir |
| 5 | en el bosque aparece comida, de día | sitio:bosque · día | 0 · 0 · 0; da 0 | cv:541-552 | como la 3; vale 0, así que solo no cambia nada | al decidir (vale 0) |
| 6 | en el bosque aparece comida, de noche | sitio:bosque · noche | igual | cv:541-552 | igual | al decidir (vale 0) |
| 7 | el huerto da fruto | trabajar · huerto | recursos 0,15; 20 turnos; espera 800 | cv:541-552 | decidir: cv:1382, 2497-2521, 2788; aprender: cv:1446, 745 | al decidir y al aprender |
| 8 | la comida se conserva, almacén | guardar:comida · almacén | dura: bolsa 800, despensa 1 600… | cv:541-552 | `campo(…, "dura")` (cv:2305) en R-CARENCIA y V-RECURSOS | al decidir |
| 9 | ídem, despensa | guardar:comida · despensa | igual | cv:541-552 | `campo` (cv:837) se queda con el primer recuerdo que tiene «dura», el del almacén | entra y no se usa |
| 10 | ídem, bolsa | guardar:comida · bolsa | igual | cv:541-552 | igual que la 9 | entra y no se usa |
| 11 | ídem, suelo | guardar:comida · suelo | igual | cv:541-552 | igual que la 9 | entra y no se usa |
| 12 | de noche viene la bestia | bestia · noche | cuerpo −1,5; empieza en el turno 280 | cv:541-552 | «empieza» en cv:884, 913 y 2520; el cuerpo en cv:891, en la amenaza | al decidir |
| 13 | la casa es segura de noche | sitio:casa · noche | 0 | cv:541-552 | `dano_sitio` (cv:2526, 912), si está en casa de noche; vale 0 | al decidir (vale 0) |
| 14 | dormida fuera, la bestia te pega | dormir · fuera | cuerpo −1,5 | cv:541-552 | cv:2520: la foto de dormir fuera | al decidir |
| 15 | los matorrales del bosque dan fruto | matorral · bosque | recursos 0,5; 2,02 por cada 100 casillas | cv:541-552 | por cada 100: cv:2318 y 2596; recursos: cv:2599 (ir al bosque). Con `memoria_v3`, el 0,5 de los matorrales se lee del JSON de la cultura (cv:1374-1379), no del cuaderno | al decidir |
| 16 | si llamas, viene alguien | llamar · valle | viene 0,5 | cv:541-552 | `_p_llamada` (cv:1215), al elegir llamada (cv:1269) | al decidir |
| 17 | hermana «cerca» | criatura:hermana · cerca | 0 · 0 | cv:1791 | cv:1815, 1971, 1985 y 1532; `peso_dar` (cv:2072) | al decidir |
| 18 | hermana «trato» | criatura:hermana · trato | vínculo 0,5 | cv:1792 | decidir: cv:2072, 2075; aprender: cv:1951 (rehace el vínculo con la hermana) | al decidir y al aprender |
| 19 | fuente: el almacén | fuente:camara · valle | recursos 0,24 | cv:1793 | `valor_fuente` (cv:1820, 2340): el destino de ir a por botín | al decidir |
| 20 | fuente: las cajas | fuente:cajones · valle | recursos 0,12 | cv:1793 | cv:734, 750, 921: ir a un objeto, ir a por botín | al decidir |
| 21 | fuente: las bayas | fuente:bayas · valle | recursos 0,07 | cv:1793 | cv:735: ir a una planta con fruto | al decidir (si ve una) |
| 22 | guardar una medicina | medicina · guardar | recursos 0,18 | cv:1794 | cv:1652 (R-ACOPIO) | al decidir |
| 23 | dar una medicina | medicina · dar | vínculo 0,125 | cv:1795 | cv:1675, 1686, 1697, 2102 (si alguna está herida) | al decidir (si se da el caso) |
| 24 | dar una comida | comida · dar | vínculo 0,538 | cv:1797 | cv:1683, 1688, 1695, 2101, 2213 (si alguna está flaca) | al decidir (si se da el caso) |
| 25 | **a veces aparece un árbol dulce lejos** | hecho:arbol_dulce · valle | 0 | cv:554-561 | ninguna línea | **entra y no se usa** |
| 26 | **al atardecer la bestia pasa por los árboles dulces** | hecho:bestia_arbol · noche | 0 | cv:554-561 | ninguna línea | **entra y no se usa** |
| 27 | echar a la bestia | hecho:echar_bestia · acompañada | 0 (texto) | cv:562-570 | el recuerdo, ninguna; sus números van aparte a `hechos_g` (cv:566) y se leen en la foto de la bestia (cv:1591) | entra y no se usa (sus números, sí) |
| 28 | matar a la bestia | hecho:matar_bestia · acompañada | 0 (texto) | cv:562-570 | igual, cv:1598 | entra y no se usa (sus números, sí) |
| 29 | la bestia ataca a una sola | hecho:bestia_ataca_a_una · acompañada | cuerpo 0,5 | cv:572-579 | ninguna; el comentario lo dice: «hoy no los lee nada» (cv:572) | entra y no se usa |
| 30 | un empujón lo gana el bando mayor | hecho:empujon_bando · acompañada | recursos 1 | cv:572-579 | ninguna | entra y no se usa |
| 31 | empujar a la bestia: dos pegadas o le pega 40 | hecho:empujar_bestia · acompañada | −40 · 1 | cv:572-579 | ninguna (lo que pasa al empujar está escrito en cv:1590-1596) | entra y no se usa |
| — | **las bestias y las épocas** | hecho:bestias_epocas · valle | factores 1,3 · 1 · 0,7 · 1; 5 días | `cultura_hechos_v44.json:30-32` | cv:565 lo descarta: de ese fichero solo pasan echar y matar | **no le llega** |

**Cuántas son: 31.**
- **16 de la cultura** (las 1-16). El 161 dice 17. Cuenta 11 frases: «la zona salvaje» y «el bosque» valen dos situaciones cada una, y «guardar comida» vale cuatro. Así salen 16 claves. El 161 da 17 porque también cuenta «la medicina» de día y de noche, o una frase con dos recuerdos. El total de 31 sale igual en el registro, así que la diferencia es de cómo agrupar, no de cuántos recuerdos hay. (Leído; no lo he desmenuzado más.)
- **8 del radar** (las 17-24; el 161 dice 7 porque junta las tres fuentes).
- **7 hechos** (las 25-31).

**Por marca, sobre las 31:**
- **Se leen al decidir y al aprender: 3** (la medicina, el huerto y el trato de la hermana).
- **Se leen solo al decidir: 19.** Algunas solo si se da su caso (la casa de noche, las bayas, dar medicina o comida). Tres valen 0, así que solas no cambian nada (el bosque de día y de noche, la casa).
- **Entran y no se usan: 9.** Son las tres copias de «guardar comida» que no son la del almacén, los dos hechos del árbol dulce y los cinco de la bestia y de acompañar. De echar y matar sí se usan sus números, por una vía aparte.
- **El de las bestias y las épocas no le llega:** está en el fichero, pero el cargador lo descarta.

**Diferencias con el informe 161:**
1. **Echar y matar.** Lo que entra en la foto son sus números (`hechos_g`), no el recuerdo del cuaderno.
2. **El fruto de los matorrales.** La criatura lo lee de la cultura (el JSON), no del cuaderno, salvo para ir al bosque.
3. **El árbol dulce.** Sus dos hechos los tiene, pero ningún código los lee.

---

## Qué es contado y qué es leído

- **Contado** (con `empates_sombra_163.py`): la parte 3, la tabla de las diez partidas y la submuestra de M9.
- **Leído del código:** la parte 1 y la parte 4.
- **Leído de los informes:** la parte 2.
- **Estimado:** los tiempos de rejugar.

## Ficheros y órdenes

- **Nuevos** (en `cantera/paper8/`): `empates_sombra_163.py`, `salida/empates_sombra_163.md`, `salida/empates_sombra_163.json` y este informe.
- **Leídos sin tocar:**
  - `cantera/paper9/partidas_C6b/*/sombra_C6.jsonl.gz` (fuera de su commit; las rejugó el chat de la curiosidad);
  - `/Volumes/Mem G-EMV/valle_experimento_v6/`.
- **Órdenes sueltas, declaradas:** solo de lectura (`grep`, `sed`, `ls`, `git log` y dos `python3 -c` para mirar una línea de un registro). Para la parte 4, un agente leyó el código, sin ejecutar nada de la criatura.
- **Gasto:** 0 créditos de la plataforma y 0 dólares de la consola. No se ha usado la clave.
