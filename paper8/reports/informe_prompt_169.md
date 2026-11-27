# Prompt 169: el texto montado del paper ocho, comprobado contra los sellos, los informes y los datos, y el material del apéndice

*23-nov-2026. No se ha jugado ni rejugado ninguna partida. `motor/model.py` y las clases congeladas solo se han leído. Gasto: 0 créditos de la plataforma y 0 dólares de la consola de Anthropic.*

**El texto.** `cantera/paper8/paper8_ES_montado_v1.md`, copiado de `[carpeta local]`. Antes de usarlo comprobé que es el fichero correcto:
- tiene 618 líneas y 90.010 bytes;
- empieza por «# G-EMV: emoción y razón en un agente»;
- su sha256 es `722116e6…3c123b71`, la huella que diste;
- en Downloads había solo un fichero con ese nombre.

Lo leí entero antes de empezar. Los PDFs sueltos de Downloads no se han usado.

**Los programas nuevos**, en `cantera/paper8/`; cada uno deja sus tablas en `salida/`:

| programa | qué hace | salida |
|---|---|---|
| `cifras_169.py` | parte 1: cada cifra del texto contra su fuente | `cifras_169.md` y `.json` |
| `frases_169.py` | partes 2 y 10: lo contado en las 3.200 partidas selladas en que se apoya el texto (v5, v6 y escalera) | `frases_169.md` y `.json` |
| `apuestas_169.py` | partes 3 y 4: los diez sellados y las 114 apuestas, una a una | `apuestas_169.md` y `.json` |
| `cuentas_169.py` | el vaivén emparejado (parte 1) y la cuenta del motor (parte 11) | `cuentas_169.md` y `.json` |

**Abreviaturas:** `cv` es `cantera/paper8/cuerpo_valle.py`, `mm` es `motor/model.py` y `cfg` es `cantera/paper8/config_cuerpo_valle.json`.

## Resumen

- **Parte 1, las cifras: son 180.**
  - Cuadran 95 y cuadran redondeadas 76.
  - **No cuadran 6** (cinco frases distintas; la del almacén sale dos veces).
  - **No encuentro la fuente de 3.**
  - Las que fallan están en la tabla de abajo.
- **Parte 2, las frases sin número.**
  - **Dos las desmienten los datos.** Una criatura sí deja comida en el almacén vacío, una sola vez. Y a los diez días no solo «han bajado a medias» las noches en vela y las llamadas.
  - **Otras dos las desmiente el código.** El techo no se aplica tampoco al vivir. Y la criatura distingue cuatro niveles de vida en la otra, no tres.
  - **Cuatro frases tienen un matiz**, que va en la parte 2.
  - **Las cuatro del ejemplo del prompt:** «ninguna bestia muerta», «ninguna muerte a manos de otra» y «no lo deduce de dejar de verla» se confirman. La del almacén no.
- **Parte 3:** las cuentas dan 114 apuestas y 90 cumplidas, contadas una a una por el programa.
- **Parte 4:**
  - Las 24 falladas van con su texto literal, su listón y su resultado.
  - 18 de las 114 se escribieron, según dicen sus propios ficheros sellados, después de ver partidas de taller.
  - El texto dice que **una** apuesta se cumple porque se bajó el listón. **Son dos**: P17 del v5 y P17 del v6.
- **Parte 10:** la criatura sellada **no aplica el techo en ningún sitio**, ni al imaginar ni en lo que siente en el turno.
- **Parte 11:**
  - **Con ganancia 0,7 y pérdida 0,2 sale 35,5 %**, como en la mesa.
  - **Con ganancia 0,5 y pérdida 0, el 84 % no sale.** Con la pérdida a 0 no se puede bajar 0,1; como cuenta formal daría 68 %.
  - **El cociente no es estable:** va del 87 % a menos de −100 % según el punto de partida.

---

## Parte 1. Los números

La tabla entera está en `salida/cifras_169.md`. Tiene una fila por cifra, con estas columnas:
- la sección y un trozo literal de la frase;
- el valor tal como lo dice el texto y cómo lo leo;
- el valor exacto, el margen si lo hay y la fuente (`fichero:línea`);
- si es apuesta, observación, del mundo o del código;
- el veredicto.

**Cómo funciona el programa:**
- **Cada frase se comprueba en el texto.** El trozo de frase de cada fila tiene que estar, letra a letra, en el texto montado; si no está, el programa para.
- **Cada valor se lee de su fuente.** El programa busca la línea del fichero fuente con una expresión fija, saca de ella el valor y apunta el número de línea. Si la expresión no casa en ninguna línea, para. Así ninguna cita queda sin comprobar.
- **Las cifras en palabras se leen con una banda.** Por ejemplo, «casi un tercio» es de 0,28 a 0,34 y «la mitad» es de 0,45 a 0,55. Las bandas las fijé yo, por lo más simple, y van en la tabla.
- **El redondeo.** Los números que el texto da en palabras enteras se redondean a la unidad: «entre dos y tres» acepta 3,15, y «entre dos y medio y cuatro» acepta 4,1. Lo digo porque son las dos que cuadran solo por eso.

**Las fuentes:**
- **Para cada número de las partidas,** el informe que lo contó primero con las partidas selladas: el del v6 y el de la escalera, y los de los prompts 155 a 168.
- **Para los números del mundo y del código,** el 160 y el 161, que los comprobaron en la config y en el código, con su línea.
- **Contado aquí:** el almacén, la bestia y las muertes a golpes (`frases_169.py`) y el vaivén (`cuentas_169.py`).

### Las que no cuadran

| sección | frase | qué dice el texto | qué dicen los datos | fuente |
|---|---|---|---|---|
| 4 | «nadie vuelve a dejar allí una sola comida en ninguna partida» | ninguna | **1 comida, en 1 de las 200 partidas** de la protagonista: normal, semilla 30179, criatura B1, turno 827 (día 3), con el almacén ya vacío desde el día 2 | `salida/frases_169.md:20`, contado |
| 7 | «El almacén común se vacía en cinco días y nadie vuelve a dejar comida en él» | ninguna | lo mismo. Además, el almacén se vacía en el día 1, 2 o 3 en las 200 partidas (mediana, el día 1); «en cinco días» se cumple | ídem |
| 4 | «Diez días después… solo las noches en vela y las llamadas han bajado a medias» | solo esas dos | en los días 6 a 15 también bajan a la mitad dos más: los turnos quieta (de −25,7 a −12,2) y las noches dentro de su casa (de −0,201 a −0,114) | `informe_prompt_165.md:179`, `:181`, `:208` y `:210` |
| 6 | «En la abundancia y en las dos sequías dura toda la partida» (la ventaja en felicidad sobre la que suma) | dura toda la partida | va por delante en todos los tramos, pero **no se separa en todos**: el margen cruza el cero en la sequía (días 36-40) y en la sequía dura (días 16-30). En la abundancia sí se separa en todos | `informe_prompt_156.md:56` y `:74`; `informe_prompt_157.md:13-18` |
| 6 | «Frente a la que suma, es claro en el mundo normal, en la sequía y con las bestias, y justo en los otros dos» (el vaivén) | justo en la abundancia y en la sequía dura | no había ninguna cuenta emparejada; la he hecho. **En la abundancia el margen cruza el cero:** −0,51 [−1,14, +0,12]. En la sequía dura se separa por poco: −1,53 [−2,88, −0,20]. Los otros tres, claros | `salida/cuentas_169.md:9-13` |
| 8 | «Una se cumple porque bajamos el listón» | una | **dos**: P17 del v5 y P17 del v6, las dos con el listón de «4 o menos de 200», y las dos con 1 de 200 (parte 4) | `apuestas_169.md`, parte 4 |

### Las que no tienen fuente

| sección | frase | por qué |
|---|---|---|
| 1 | «un combate por sobrevivir entre dieciséis» | Es de los trabajos anteriores (el seis y el siete). En `cantera/paper8` no hay ninguna fuente. |
| 3 | «la que comerá en dos días, que son unas siete comidas» | La cuenta es `comidas_dos_dias` (`cv:2302-2308`): (hambre + lo que sube por turno × 800) / lo que cree que quita una comida. Las dos partes de abajo son aprendidas y no están apuntadas. Con lo heredado y el hambre de base da (h + 200) / 35: 5,7 comidas con el hambre a 0, y 7 con unas 45 de hambre. **No se puede saber sin rejugar.** |
| 5 | «y en la escasez faltan unas veintiséis» | No he encontrado de dónde sale ni con qué definición de «faltar». |

**Una que cuadra, pero con una fuente débil.** «Se pudren unas sesenta comidas en las bolsas, las despensas y las plantas» (sección 5):
- Lo único que hay es el libro diario de la comida de dos partidas rejugadas por el chat de la curiosidad (`../paper9/informe_C2.md:348-349`, semillas 30161 y 30162). En los días 1 a 10 de la sequía dura da 64,5: 57,5 en las bolsas, 5 en las despensas y 2 en las plantas.
- Son dos partidas, no las cuarenta. En las 200 selladas no está apuntado lo que se pudre en la despensa.

### Las que cuadran solo redondeando mucho, por si se quieren afinar

| sección | frase | valor exacto |
|---|---|---|
| 4 | «son entre dos y tres criaturas más» | +2,67, +2,67 y **+3,15** |
| 4 | «De cada cinco, dos lo ven en el momento, dos encuentran el cuerpo… y una no llega a saberlo» | 36 %, 45 % y 19 % de las 172 parejas (`informe_prompt_166.md:66`). En los 136 casos de A2, no se enteran 21 (15 %). |
| 4 | «Llama casi el doble» | ×1,73 |
| 6 | «En la del motor, entre dos y medio y cuatro» | 2,6 · 3,6 · 2,8 · 3,7 · **4,1** |
| 6 | «Duerme más en casa… en los cinco mundos» | Cuadra, pero la medida es solo de los días 0 a 9: `informe_escalera_v6.md:95-103`. |
| 5 | «de entre dos y cuatro golpes por partida» | La de antes (RG68r) va de 1,95 a 3,90. |
| 4 | «Con las bestias que crían, 6,7» | 6,65; con un decimal da 6,6 o 6,7. |

---

## Parte 2. Las frases sin número

Lo contado sale de `frases_169.py`, sobre las 3.200 partidas de los tres sellados en que se apoya el texto: el v5 (1.600), el v6 (1.200) y la escalera (400). La tabla por jugador está en `salida/frases_169.md`.

**Las cuatro del ejemplo del prompt:**

| frase | qué sale | prueba |
|---|---|---|
| «nadie vuelve a dejar comida en el almacén en ninguna partida» (secciones 4 y 7) | **Falsa, por poco.** La protagonista deja una comida, una vez: normal 30179, B1, día 3. En las otras criaturas también hay casos: RG68r, 1 en el v5 y 2 en el v6; RG69r, 1; S69+voz, 49 comidas en 5 partidas; P69+voz, 2. El tonto y el recolector dejan miles. | registro del mundo, `dejar` con `en = almacen` y resultado `ok`; y la comida del almacén turno a turno (`criaturas.jsonl.gz`) |
| «en ninguna partida matan a la bestia» (secciones 2 y 4) | **Cierta.** 0 sucesos `bestia_muere` en las 3.200 partidas. Sí la golpean alguna vez (sucesos `bestia_herida`): la protagonista 7 veces en 200 partidas, S68 42 y S69+voz 27. | `valle/mundo.py:329` y `:337`; `salida/frases_169.md` |
| «ninguna criatura muere a manos de otra» (sección 4) | **Cierta.** 0 muertes con causa «golpe» en las 3.200 partidas. | `fin.json`, `muertes` |
| «no deduce la muerte de su hermana de dejar de verla» (sección 4) | **Cierta, en el código.** Solo lo sabe si la ve morir o ve el cuerpo (`cv:695-707`). Dejar de verla solo hace crecer la soledad (`cv:713-719`) y nunca pone `pareja_muerta`. Lo comprobó el 166 con las partidas: 67 de 67 casan. | `informe_prompt_166.md:28-56` |

**Las que encontré al leer:**

1. **El techo (secciones 6, 8 y 9).** El texto dice que al imaginar no aplica el techo, y da a entender que al vivir sí: «Para vivir es razonable». **En la criatura sellada no se aplica en ningún sitio** (parte 10).
2. **«A los diez días… solo las noches en vela y las llamadas han bajado a medias»** (sección 4). También bajan a medias los turnos quieta y las noches en casa (parte 1).
3. **«La criatura no ve cuánta vida le queda a otra: solo ve si está sana, herida o muy herida»** (sección 3). Ve **cuatro** niveles: sana, herida, muy herida y moribunda (`cv:931-938`, `cfg`: `banda_de_la_hermana.niveles_v31`). La cuenta del peso fijo sí es como dice el texto:
   - a una hermana sana le supone 85 de vida (`cfg`: `niveles_v31.sana`);
   - con eso, S-DANO-PAREJA vale (100 − 85) / 100 × su peso de familia (`cv:1616` y `:1670-1672`), y no llega nunca a cero.
4. **«En cada uno de los tres se juegan los cinco mundos en cuarenta valles sorteados para la ocasión, que nadie había visto antes»** (sección 9). Para la escalera no es así: se jugó en los mismos valles que el v6 (30161-30200), y la protagonista no se volvió a jugar, se leyó del v6. La frase siguiente del texto lo dice, así que las dos frases se contradicen.
5. **Lo que «sabe» y no usa** (sección 3). El texto dice que tiene tres huecos. El 163 cuenta nueve recuerdos de nacimiento que entran y no se leen nunca (parte 6). Uno de ellos es que en la zona salvaje está la medicina: «da medicina 0,5» no lo lee nada.
6. **«Duerme más en casa… la del motor pasa menos noches al raso que las otras dos en los cinco mundos»** (sección 6). La medida es solo de los días 0 a 9. Del resto de la partida no hay cuenta emparejada.
7. **«Pasados esos diez días las tres aldeas se empujan parecido, salvo en la abundancia»** (sección 6). En el normal, días 31-40, la del motor empuja algo más que la que suma, y se separa: +0,6 [+0,2, +1,1] (`informe_prompt_157.md:47`). Es pequeño y a favor de la que suma.
8. **«Las llamadas se oyen más lejos de lo que se ve»** (sección 2). Es así con la llamada media (7) y la fuerte (10). La suave llega a 4 casillas, y de día se ven 5 (`informe_prompt_160.md:151`).

---

## Parte 3. Los diez sellados

Fecha y commit: `git log -1` de cada etiqueta. Jugadores, semillas y partidas: la historia de los sellados del 162. Las apuestas, una a una, en la parte 4 (`apuestas_169.py`).

| # | sellado | etiqueta | fecha | commit | jugadores | semillas y partidas | apuestas | cumplidas |
|---|---|---|---|---|---|---|---|---|
| 1 | v1 | `valle-congelado-v1` | 02-11-2026 | `ccd88251` | RG32r, RG032r, S32, S032, tonto, recolector | 1001-1040; 1.200 | 14 | 8 |
| 2 | confirmación | `valle-confirmacion-v1` | 03-11-2026 | `79afe666` | RG32r, S32, P32, RG032r, S032 (bestia de día); RG32r, S32, P32 (sequía dura) | 2001-2040; 320 | 6 | 4 |
| 3 | dilemas | `valle-dilemas-v1` | 03-11-2026 | `aa7fd4b1` | RG32r, S32, P32, RG032r, S032 | 3001-3040; 2.800 cortas | 3 | 0 |
| 4 | mesa | `valle-mesa-v1` | 03-11-2026 | `caf63cda` | los mismos cinco | variantes 4001-4020; 3.600 preguntas, ninguna partida | 3 | 0 |
| 5 | v2 | `valle-congelado-v2` | 07-11-2026 | `af7605a5` | RG50r, RG050r, S50, S050, P50, tonto, recolector | 30001-30040; 1.400 | 12 | 11 |
| 6 | v3 | `valle-congelado-v3` | 09-11-2026 | `34bf8e78` | RG58r, RG058r, S58, S058, P58, tonto, recolector | 30041-30080; 1.400 | 15 | 10 |
| 7 | v4 | `valle-congelado-v4` | 11-11-2026 | `27b23137` | RG61r, RG061r, S61, S061, P61, tonto, recolector | 30081-30120; 1.400 | 15 | 14 |
| 8 | v5 | `valle-congelado-v5` | 15-11-2026 | `65ee6048` | RG68r, RG068r, S68, S068, P68, RG61r, tonto, recolector | 30121-30160; 1.600 | 21 | 21 |
| 9 | v6 | `valle-congelado-v6` | 18-11-2026 | `759acc39` | tonto, recolector, RG68r, RG068r, RG69r, RG69r+voz | 30161-30200; 1.200 | 23 | 21 |
| 10 | escalera | `valle-escalera-v6` | 19-11-2026 | `24cdb2db` | S69+voz y P69+voz (RG69r+voz se lee del v6) | 30161-30200; 400 nuevas | 2 | 1 |
| | **total** | | | | | | **114** | **90** |

**Comprobado: da 114 y 90.** La regla para contar es la del 162:
- solo cuentan las predicciones;
- P5 del v1 cuenta como seis;
- «se informa» y «sin predicción» no cuentan.

**Dos notas sobre las fechas:**
- En el v2 y en el v3, la etiqueta es la del congelado. Las predicciones se sellaron en otro commit: `648475e6` (07-11) en el v2 y `61276d6b` (10-11) en el v3.
- El v6 se subió a las 00:03 del 18-11, que es el 17 a las 23:03 en hora UTC.

## Parte 4. Las 24 apuestas falladas

La tabla entera, con el texto literal sacado del fichero sellado y la fila del resultado de cada una, está en `salida/apuestas_169.md`. En corto:

| # | sellado | apuesta | texto literal | listón | resultado |
|---|---|---|---|---|---|
| 1 | v1 | P2a | «Con la bestia de día, las de motor se apartan de la bestia más a menudo y antes que las de sumas, a igualdad de ganancias.» | en el texto | no se cumple |
| 2 | v1 | P2b | «Con la bestia a 5 casillas o menos de la comida, las de sumas se acercan a la comida más veces que las de motor.» | en el texto | no se cumple |
| 3 | v1 | P3b | «Con ganancias visitan más sitios distintos al día y pasan más tiempo con la hermana a la vista.» | en el texto | no: la hermana sí, los sitios no |
| 4 | v1 | P5b | «avisan de la bestia en más de la mitad de las veces que la ven.» | en el texto | no: sí en bestia de día, no en los otros cuatro |
| 5 | v1 | P5c | «tras la muerte de una de las suyas, el amor de la superviviente baja y su tristeza sube en el día siguiente, más por la hermana que por una vecina.» | en el texto | no: el amor no baja |
| 6 | v1 | P5f | «las llamadas de contacto son más frecuentes con alguna de las suyas al alcance de la voz que sin ninguna.» | en el texto | no: sale en 1 de 10 |
| 7 | confirmación | C1 | «En bestia de día, RG32r vive más que S32.» | vivas, RG32r − S32 | +0,30 [−0,05, +0,65] |
| 8 | confirmación | C4 | «En bestia de día, RG32r vive más que P32 (…)» | vivas, RG32r − P32 | +0,05 [−0,28, +0,38] |
| 9 | dilemas | D1 | «En la escena F (tres dimensiones), RG32r y S32 eligen distinto más a menudo que en las escenas de una dimensión (C y D).» | F − media de C y D | −0,069 [−0,106, −0,037] |
| 10 | dilemas | D2 | «Sesgo de negatividad (paper dos): en las escenas A, B y E, RG32r necesita un escalón de ganancia más alto que S32 para aceptar el dolor (…)» | punto de cambio y aceptación | +0,00 en A y en B; E, −0,15 |
| 11 | dilemas | D3 | «Sin ganancias el motor y la suma casi no se separan: en todas las escenas, RG032r y S032 eligen igual más a menudo que RG32r y S32.» | en las seis escenas | no en ninguna |
| 12 | mesa | M1 | «Sesgo de negatividad (paper dos): en A y B, RG32r necesita una ganancia mayor que S32 para aceptar el dolor (…)» | punto de cambio | +0,00 [0, 0] |
| 13 | mesa | M2 | «Sin ganancias, motor y suma casi no se separan: la diferencia de puntos de cambio entre RG032r y S032 es menor que entre RG32r y S32.» | diferencia normalizada | +0,000 [0, 0] |
| 14 | mesa | M3 | «La tensión: en C, el punto de cambio de RG32r se separa más del de P32 cuanto más alta es el hambre.» | pendiente | −0,00615 [−0,00628, −0,00603] |
| 15 | v2 | P9 | «RG50r duerme en casa al menos el 60 % de lo que duerme, en todos los mundos.» | ≥ 60 % en los cinco | sequía dura 59,64 % |
| 16 | v3 | P9 | «RG58r duerme dentro de su casa al menos el 45 % de las noches en todos los mundos, y nunca en una puerta tapando la entrada.» | ≥ 45 % y 0 en una puerta | 172 veces en una puerta (129 tras la fe de erratas) |
| 17 | v3 | P11 | «En los momentos ambivalentes, RG58r y S58 eligen distinto más a menudo que en el resto, con la medida completa (también las decisiones de ir).» | Q4 − Q1 < 0, con el intervalo < 0 | +0,132 [+0,103, +0,161] |
| 18 | v3 | P12 | «Sin razón, RG58r coge menos del 15 % de la fruta del árbol, menos que el recolector, y más de la mitad de sus vueltas del árbol son después de anochecer.» | las tres cosas | vueltas de noche, 48 % |
| 19 | v3 | P14 | «Las vecinas que le han robado a RG58r reciben de ella menos comida, por cabeza, que las vecinas que nunca le han robado, en los mundos donde hay robos.» | en todos esos mundos | en tres mundos reciben más |
| 20 | v3 | P15 | «Ninguna racha de más de 10 regalos del mismo tipo de ida y vuelta entre las mismas dos criaturas, con menos de 40 turnos entre uno y otro, en ninguna partida.» | ninguna > 10 en 200 | una de 15 |
| 21 | v4 | P17 | «La racha más larga de regalos de ida y vuelta de RG61r es de 10 o menos.» | ninguna > 10 en 200 | 89 y 29 |
| 22 | v6 | P25 | «En la sequía dura, RG69r vive más que RG68r, con el límite inferior del intervalo sobre cero.» | límite de abajo > 0 | −0,05 [−0,40, +0,28] |
| 23 | v6 | P31 | «En la sequía dura, RG69r+voz vive más que RG68r, con el límite inferior del intervalo sobre cero.» | límite de abajo > 0 | +0,20 [−0,23, +0,62] |
| 24 | escalera | E2 | «En la sequía, RG69r+voz vive más que S69+voz» | límite de abajo > 0 | +0,12 [−0,07, +0,33] |

**Escritas después de ver partidas de prueba (de taller), según lo dice el propio fichero sellado: 18 de las 114.**
- **v1, 10 apuestas** (`predicciones_selladas.md:3`: «R = réplica de lo visto en el taller»):
  - del todo réplicas: P1a y P3a;
  - réplicas en parte: P1b (en la sequía), P2d (en el motor) y P5a a P5f («réplicas salvo en los mundos duros»).
- **v6, 8 apuestas:** P24 a P31, que «salen de talleres jugados en semillas ya vistas» (`predicciones_selladas_v6.md:75`). Las dos falladas del v6, P25 y P31, son de estas.
- **Las demás.** En los otros ficheros no consta de dónde sale cada apuesta. Las que se repiten de un sellado al siguiente se escribieron después de ver el sellado anterior, no partidas de prueba.
- **Escritas después de mirar partidas selladas:**
  - P11 del v4 y del v5, que «sale del diagnóstico del v3»;
  - las seis de la confirmación, que «salen de la exploración del experimento principal».

**La que se cumple porque se bajó el listón: son dos, la misma apuesta.**
- En el v4, P17 pedía «ninguna racha de más de 10» y falló.
- En el v5 se cambió a «4 o menos de las 200» (`predicciones_selladas_v5.md:41`). Salió 1 de 200, con una racha de 24.
- El v6 la repite con el mismo listón (`predicciones_selladas_v6.md:8`). Salió 1 de 200, con una racha de 15.
- Con el listón viejo, las dos habrían fallado. El texto (secciones 8 y 9) dice «una».

---

## Parte 5. Los fallos declarados de la criatura sellada

**Los veintitrés conocidos al sellar.**
- Cada congelado hereda los del anterior (`CONGELADO_P8_v5.md:126`, `CONGELADO_P8_v6.md:144`).
- El texto de cada uno está en `CONGELADO_P8_v4.md:149-164` (del 1 al 16), `CONGELADO_P8_v5.md:128-131` (del 17 al 20) y `CONGELADO_P8_v6.md:146-148` (del 21 al 23).
- Dónde está cada uno en el código, por lo que dicen los congelados y lo que he podido leer:

| # | fallo | dónde |
|---|---|---|
| 1 | la foto no llega al árbol y vuelta (44 pasos) | `cfg:19` (la mirada, 44); `cv:2473`, `:2479-2493` |
| 2 | el árbol se recuerda como un matorral | `cv:740-752` (la lista de matorrales) |
| 3 | no ve la vida de la bestia; al imaginar matarla, la supone entera | `cv:1598` (la foto de matar, con `hechos_g`) |
| 4 | empujar a la bestia cuenta a las suyas pegadas como si empujaran con ella | `cv:1590-1596` |
| 5 | el tamaño de la bolsa (6) está escrito en la foto | la foto de coger (no he localizado la línea exacta) |
| 6 | el hambre que supone a la otra: 80 si está flaca, 30 si no | `cv:2024`; `cfg`: `banda_de_la_hermana.flaca_hambre_estimada` (80) |
| 7 | la pieza I está apagada: ve a la hermana más quieta | interruptor apagado (`CONGELADO_P8_v4.md:155`) |
| 8 | no conoce la cría de las bestias ni las épocas | `cv:565` descarta el hecho `bestias_epocas` |
| 9 | las épocas no se anuncian | en el mundo, no en la criatura |
| 10 | lo que cree de dormir fuera incluye la vida perdida por el hambre | `cv:1437-1440` |
| 11 | empujones a quien no lleva nada (2-6 %; en el v6, 3,6 %) | sin línea: es una conducta |
| 12 | no sabe que de noche dormirá de un tirón | `cv:2503-2515` (las fotos de la noche) |
| 13 | llevar comida no vale nada para el cuerpo en la foto | las filas de cuerpo (`cv:1612-1614`) no miran la bolsa |
| 14 | el paso solo rodea a otras al ir a casa | el paso (`cv:2793-2802`) |
| 15 | quién le dio algo lo deduce de lo que ve, y se puede equivocar | `cv:1840-1846`, `:1864-1865` |
| 16 | se roba sin hambre; la ladrona sube en el radar de la robada | sin línea: es una conducta (`informe_diagnostico_v4.md:133-166`) |
| 17 | el hambre media sube frente a RG61r, sin causa conocida | sin línea: no se sabe |
| 18 | el bucle de regalos entre hermanas hartas | sin línea: es una conducta (P17) |
| 19 | la cara, la voz nueva, aprender de la cara y el «para», apagados | interruptores `cara_v64`, `voz_v64`, `aprender_cara_v64` y `para_v64` (`cv:220`) |
| 20 | sin «ven, lo necesito», no hay forma de pedir ayuda | `voz_sin_ven_v63` (`banco_v7.py:309-310`) |
| 21 | RG69r sola vivió algo menos en la abundancia en el taller, sin explicar | sin línea |
| 22 | frente a la gemela, en la sequía dura, −0,30 en el taller | sin línea |
| 23 | la voz es solo entre hermanas y solo despiertas | `cuerpo_vc1.py:75-79` |

**Los que han salido después de sellar** (prompts 160 a 169), con dónde está cada uno:

| # | fallo | dónde | lo encontró |
|---|---|---|---|
| 24 | Las ganas de explorar se apagan hacia el día 3. Al contar lo que conoce, cuenta también las 16 plantas del huerto y el árbol. | `cv:741` (la lista), `cv:2316-2320` (`falta_saber`) | 161; `../paper9/informe_C1.md:434` |
| 25 | Un peso fijo por la hermana sana: le supone 85 de vida, y S-DANO-PAREJA nunca llega a cero. | `cv:1616`, `:1670-1672`; `cfg`: `niveles_v31.sana` | texto del paper; comprobado aquí |
| 26 | Mide todos los sitios donde guardar con lo que dura la comida en la bolsa, así que el almacén no le parece mejor que su casa. | `cv:2305` (`comidas_dos_dias` usa la duración de la bolsa) | 160 |
| 27 | De lo de nacimiento, nueve recuerdos entran y no se leen nunca: tres copias de «guardar comida», los dos del árbol dulce y cinco hechos de la bestia y de acompañar. | `cv:837` (`campo` se queda con el primero), `cv:554-561`, `cv:572` («hoy no los lee nada») | 163 |
| 28 | El hecho de las épocas no le llega: el cargador lo descarta. | `cv:565` | 163 |
| 29 | Lo que creía antes de cada recuerdo se guarda, pero nadie lo lee. | `paper7/cuaderno_P7.py:102`, `:107` (`creencia_antes`) | 168 |
| 30 | No hay ninguna pérdida cuando una ganancia esperada no llega. La regla general salta las filas de ganar. | `cv:2230` | 168 |
| 31 | S-DAR, lo sentido al dar, se pone con lo que ella cree que valía, sin mirar si a la otra le sirvió. | `cv:2294`, `:2094-2102` | 168 |
| 32 | La medida en sombra da por bueno lo elegido en los empates exactos. | `lanza_experimento_v2.py:66`; `medida_v3/lanza_medida_v3.py:79` | 163 |
| 33 | La voz de ir a casa no pasa por el oído ni cuesta nada, y con ella sabe dónde está la hermana aunque no la vea. | `cuerpo_vc1.py:54-60` | 143; texto, sección 5 |
| 34 | El techo no se aplica en ninguna parte, tampoco en la foto de ahora (parte 10). | `cv:169-180`, `:215`, `:1291`, `:1302` | 169 |

El texto (sección 8) destaca tres: la 24, la 25 y la 26. Las tres están en el código como dice.

## Parte 6. Las treinta y una cosas que sabe al nacer

La lista entera, con su valor, dónde entra y dónde se lee, está en `informe_prompt_163.md:235-268`. La copio en corto:

| # | qué | valor | ¿la usa? |
|---|---|---|---|
| 1 | una comida quita hambre | cuerpo 35 | sí, al decidir |
| 2 | la medicina cura | cuerpo 40 | sí, al decidir y al aprender |
| 3-4 | la zona salvaje hiere (de día y de noche) | −0,05 · 0,5 · 0; da medicina 0,5 | sí el daño; **el «da medicina» no lo lee nada** |
| 5-6 | en el bosque aparece comida (de día y de noche) | 0 | se lee, pero vale 0 |
| 7 | el huerto trabajado da fruto | recursos 0,15; 20 turnos; espera 800 | sí, al decidir y al aprender |
| 8 | la comida se conserva: almacén | dura: almacén sin límite, despensa 1.600, bolsa 800, suelo 150 | sí: es el que se lee en `comidas_dos_dias` (de él solo se usa lo que dura en la bolsa) |
| 9-11 | la comida se conserva: despensa, bolsa y suelo | igual | **no** (`campo` se queda con el primero) |
| 12 | de noche viene la bestia | cuerpo −1,5; desde el turno 280 | sí |
| 13 | la casa es segura de noche | 0 | se lee, vale 0 |
| 14 | dormida fuera, la bestia te pega | cuerpo −1,5 | sí |
| 15 | los matorrales del bosque dan fruto | recursos 0,5; 2,02 por 100 casillas | sí |
| 16 | si llamas, viene alguien la mitad de las veces | 0,5 | sí |
| 17 | la hermana, cerca | 0 · 0 | sí |
| 18 | la hermana, trato | vínculo 0,5 | sí, al decidir y al aprender |
| 19-21 | las fuentes: el almacén, las cajas, las bayas | 0,24 · 0,12 · 0,07 | sí; las bayas, solo si ve una |
| 22 | guardar una medicina | recursos 0,18 | sí |
| 23 | dar una medicina | vínculo 0,125 | sí, si alguna está herida |
| 24 | dar una comida | vínculo 0,538 | sí, si alguna está flaca |
| 25 | a veces aparece un árbol dulce lejos | 0 | **no** |
| 26 | al atardecer la bestia pasa por los árboles | 0 | **no** |
| 27-28 | echar a la bestia y matarla | texto; sus números van aparte | **el recuerdo no**; sus números sí, por otra vía (`hechos_g`, `cv:1591`, `:1598`) |
| 29-31 | la bestia ataca a una sola; un empujón lo gana el bando mayor; empujar a la bestia sale bien con dos | 0,5; 1; −40 · 1 | **no** (`cv:572`: «hoy no los lee nada») |

**Cuántas no usa:**
- **Nueve entran y no se leen nunca:** las 9, 10, 11, 25, 26, 27, 28, 29 y 30.
- **Hay una más, de una manera distinta:** la 31 tampoco se lee, aunque lo que dice está escrito aparte en la foto de empujar.
- **Tres más se leen, pero valen 0:** la 5, la 6 y la 13.
- **Y una parte de las 3 y 4,** el «da medicina», no la lee nada.

**El hecho de las épocas no está entre las 31:** está en el fichero de hechos, pero el cargador lo descarta (`cv:565`).

**Frente al texto.** El texto (sección 3) cuenta tres huecos:
- el almacén;
- el árbol, que lo sabe y no la mueve;
- las épocas.

Los tres son ciertos, pero no son todos: hay nueve recuerdos que entran y no se usan.

## Parte 7. Lo que le hace ganar (la tabla del 168, tal como quedó)

La tabla entera está en `informe_prompt_168.md:44-59`. Las referencias son a `cv`.

**Las 14 filas o familias encendidas:**

| # | fila | dónde | clase |
|---|---|---|---|
| 1 | G-‹fila› (la regla general: el alivio de cada pérdida que baja) | 2225-2236 | 1 y 3, no limpia (solo en la foto imaginada) |
| 2 | G-ALIVIO (al dar, baja la necesidad de la otra) | 2234-2235 | 1 y 3, no limpia |
| 3 | G-SABOR-OTRA (el gusto de la otra al recibir) | 2238-2242 | 3 |
| 4 | G-GESTO (el gesto de dar comida) | 2243-2246 | 3 |
| 5 | V-CUERPO (0,82 × comida, descanso y calor) | 2272-2273 | 2, con matiz: sube cuando bajan tres pérdidas |
| 6 | V-RECURSOS (la comida guardada; dos días dan 1,6) | 2274-2276 | 2 |
| 7 | V-VINCULO (0,68 × el vínculo, con la hermana a la vista) | 2277 | 2 |
| 8-10 | V-RADAR-CUERPO, -RECURSOS y -VINCULO (las suyas a la vista) | 1975-1993 | 2 |
| 11 | P-SABOR (el gusto de lo que come) | 2279-2280 | 3 |
| 12 | S-DAR, lo sentido al dar | 2294 y 2247-2251 | no limpia |
| 13 | G-F-HAMBRE, lo sentido al comer | 2291 y 2247-2251 | 1 |
| 14 | G-R-CARENCIA, lo sentido al conseguir comida | 2292-2293 y 2247-2251 | 1 |

**Las cinco apagadas:**
- P-CALOR, P-COMER, R-CONSEGUIR y S-JUNTAS: solo se calculan en `platos()` (`cv:1745-1770`), con `dos_platos`, que está apagado (`cv:1726`).
- R-LLAMADA: la quita la regla general (`cv:2189`).

**Las clases:** 1 es alivio (baja una pérdida), 2 es estado bueno o acción y 3 es solo al imaginar.

**Lo que no se puede medir:** qué parte de lo ganado viene de cada clase no está apuntado. Haría falta rejugar las 200 partidas con un registro de filas (no se puede sin rejugar).

## Parte 8. Las definiciones exactas de las medidas del texto

| medida | definición | fichero:línea |
|---|---|---|
| **vivas al día cuarenta** | 8 menos las muertes que apunta `fin.json` | `cierre_v46.py:61` |
| **de qué mueren** | la «causa» de cada muerte en `fin.json`; «golpe» incluye las que empiezan por «golpe» | `cierre_v46.py:55` |
| **felicidad de una criatura** | la parte de sus turnos viva y despierta en que los tres balances de las seis sumas crudas de la foto de ahora son > 0 | `evalua_experimento_v5.py:45-59`; las seis, `cv:122-132` y `:2457-2463` |
| **felicidad de la aldea** | la media de las criaturas que tienen algún turno despierta, cada una con el mismo peso; la que muere cuenta por lo que vivió | `evalua_experimento_v5.py:59` (`informe_prompt_154.md:7-30`) |
| **la criatura a la que peor le va** (56 frente a 43) | la menor felicidad de las ocho criaturas de la aldea | `evalua_experimento_v5.py:60` (`feliz_peor`) |
| **solo las vivas el día 40** | las criaturas vivas en el último turno de la partida | `felicidad_solo_vivas.py`, `vara_sumas_167.py:46` |
| **la peor de las tres** (el balance más bajo) | en cada turno despierta, el menor de los tres balances; la media por criatura y luego la de la aldea | `vara_sumas_167.py:43-45` |
| **la suma de los tres balances** (la vara de la que suma) | la media por turno despierta de cuerpo + recursos + vínculo | `vara_sumas_167.py:44` |
| **noches al raso** (P28; 1 de 4 → 1 de 14) | en la fase noche (turnos 280 a 399), dormida fuera de su casa más de la mitad de los turnos; los días 0 a 9 de las dos sequías. «Fuera de su casa» incluye dormir en una casa ajena | `dormir_fuera_v5/noches_v5.py:71-73`; `voz_a_casa_v1/analiza_vc1.py:78` |
| **duerme dentro de su casa** (P9; del 86 al 97 %) | dónde está la primera vez que se duerme cada noche, desde el anochecer: dentro de su casa, sin la puerta | `medida_v4/dormir_v4.py:4`, `:19` |
| **las dos hermanas en la misma casa** (del 83 al 95 %) | el sitio de cada noche es donde duerme más de la mitad de la fase noche; «misma casa», las dos en la misma | `casas_noches_162.py` (`informe_prompt_162.md:69-74`) |
| **pegada a otra** (P4; un tercio frente a uno de cada doce) | fuera de cualquier casa y con alguna bestia a la vista de la fase, otra criatura viva a 1 casilla o menos (Chebyshev) | `cierre_v46.py:47-49` |
| **pegada a una vecina** (P8 y A2) | otra criatura viva de otra casa a 1 casilla o menos; parte de los turnos del día | `cierre_v46.py:51-53` |
| **comida dada a una flaca** (P7) | «dar» comida con éxito a quien el turno anterior tenía hambre > 60 (`umbral_flaca`) | `cierre_v46.py:43-46`; `valle/config_valle.json:572` |
| **echarla entre dos** (303 de 304) | cada «bestia_echada»; «entre dos», si ese turno dos o más criaturas la empujan con resultado | `seccion5_164.py:7-8` |
| **empujones** | «empujar» a otra criatura, no a la bestia, sin resultado «no:» | `cierre_v46.py:37` |
| **sin tener hambre, a quien lleva algo** | quien empuja tenía el turno anterior menos hambre que la de harta (15); la empujada llevaba algo el turno anterior | `seccion5_164.py:9-11`, `:35` |
| **robo** | un empujón con ganadora que hace soltar algo a la otra, entre casas distintas | `medidas_v6.py:44-49` |
| **no vuelve a valerle** (M6) | la ladrona no vuelve a valer, en el radar de la robada, lo que valía el día del robo | `medidas_v6.py` (M6; `informe_experimento_v6.md:136`) |
| **vuelven a estar juntas** | tras el robo se separan (más de 1 casilla) y vuelven a estar a 1 o menos, las dos vivas | `seccion5_164.py:21-22` |
| **el duelo y la soledad** (A4) | duelo = S-DUELO-CUERPO + -RECURSOS + -VINCULO; soledad = S-SOLEDAD; media de los turnos despierta de cada día | `duelo_soledad_v6.py:26`, `:31`, `:76-96` |
| **casos y controles** (136 y 378) | caso: su hermana muere el día 5 o después y ella vive 5 días más; control: de otra casa de la misma partida, con su hermana viva hasta d + 5 | `duelo_soledad_v6.casos_de` (`informe_prompt_165.md:79-80`) |
| **no vuelve a estar bien** (84 de 136) | desde el día siguiente a la muerte, ningún turno despierta con los tres balances > 0 | `seccion5_164.py:18-19` |
| **quieta, llamadas, noches en vela** | «quedarse» en la mañana y la tarde (turnos 0 a 239); los turnos con «llama»; la noche «despierta» si ningún sitio pasa de la mitad | `tras_hermana_165.py:17`, `:57`, `:67`, `:70` |
| **hambre con comida en la bolsa** (P24 y P29) | turnos viva y despierta con hambre > 30 y comida en la bolsa, por criatura y día, días 0 a 9 | `hambre_ganancias_v1/extrae_hg_v1.py:6-7` |
| **fruta del árbol cogida** (P12) | de las frutas puestas, la parte cogida | `analiza_arbol_v50.py` (`predicciones_selladas_v3.md:70`) |
| **rachas de regalos** (P17) | por par y tipo, la racha más larga de regalos de ida y vuelta, con menos de 40 turnos entre uno y otro | `medicina_v1/comprueba_v58.py:20` |
| **la felicidad día a día, los tramos y el vaivén** | la felicidad de la aldea de cada día; el vaivén es la media de los días de fruto menos la de los días sin fruto | `felicidad_dia_a_dia.py:25-42`; `tramos_y_ritmos_157.py:65`; `cuentas_169.py` |
| **el margen** | bootstrap de las semillas emparejadas, 10.000 remuestreos, semilla 8, 95 % | `evalua_experimento_v5.py:111-115` |

## Parte 9. La medida en sombra, entera

**Qué mide.**
- En cada decisión de la criatura (la del motor), el lanzador pregunta también a los otros valoradores qué habrían elegido en el mismo estado: la que suma y la de la posición. Apunta si coinciden (`decisiones.jsonl.gz`).
- Las decisiones se ordenan por lo ambivalente que es el estado: el menor de la ganancia y la pérdida en una misma dimensión, medido con el motor como instrumento (`predicciones_confirmacion.md`, C5). Se parten en cuartos dentro de cada mundo.
- La medida es la coincidencia con la que suma en el cuarto más ambivalente (Q4) menos la del menos ambivalente (Q1), con intervalo por bootstrap de partidas (`evalua_experimento_v5.py:117-121`, `p11`).

**Cómo trata los empates** (`medida_v3/lanza_medida_v3.py:66-80`, función `desempata`):
1. Primero, seguir con lo que hacía y quedarse: las mismas reglas que tiene la criatura (`cv:2983-2991`).
2. Después, la línea 79: si queda un empate exacto y lo que la criatura eligió está entre las empatadas, gana lo elegido.
3. La criatura, en ese punto, sortea (`cv:2992-3000`). Así, con la que suma, cualquier empate en que esté lo elegido cuenta como «coincide».
4. En diez partidas del v6 contadas por el 163 son el 3,4 % de las decisiones de día con la que suma, y el 3,7 % con el motor (`informe_prompt_163.md:166-168`). Las demás no se pueden contar sin rejugar.

**Qué dio en cada uno de los cinco experimentos:**

| experimento | criatura | Q4 − Q1 | sin las decisiones de dar | sin las de ir | ¿era apuesta? | fuente |
|---|---|---|---|---|---|---|
| v2 | RG50r | −0,131 [−0,152, −0,111]; con la medida arreglada del 101, −0,128 | — | — | P11, se cumple | `informe_experimento_v2.md:57`; `informe_diagnostico_v4.md:38` |
| v3 | RG58r | **+0,132 [+0,103, +0,161]** | — | +0,163 [+0,135, +0,192] | P11, **falla** | `informe_experimento_v3.md:59` |
| v4 | RG61r | +0,143 [+0,116, +0,170] | −0,115 [−0,139, −0,089] | +0,161 [+0,131, +0,190] | P11 (cambiada tras el v3), se cumple | `informe_experimento_v4.md:56` |
| v5 | RG68r | +0,042 [+0,011, +0,074] | −0,175 [−0,204, −0,146] | +0,072 | P11, se cumple | `informe_experimento_v5.md:49` |
| v6 | RG69r+voz | +0,198 [+0,172, +0,224] | −0,026 [−0,049, −0,003] | +0,286 | no: M9, sin apuesta | `informe_experimento_v6.md:139` |

**Antes del v2** (confirmación, C5 y C6) se usaba otra medida, sin la línea 79. En esas criaturas la sombra era la misma regla de la criatura (`informe_prompt_163.md:75`).

**Lo que el texto dice de ella (sección 9) cuadra:**
- menos de 4 de cada 100;
- cinco experimentos;
- cambia de signo según qué decisiones se cuenten: con todas, positiva desde el v3; sin las de dar, negativa;
- ninguna pieza se aceptó con ella (`informe_prompt_163.md:9-12`).

## Parte 10. El techo

**Dónde lo aplica la criatura sellada: en ningún sitio.**
- **El interruptor:** RG69r+voz lleva `sin_techo_v11` encendido, el de RG68r (`banco_v7.VARS["RG68r"]`, comprobado).
- **Cómo pasa una foto por el motor:** toda foto pasa por `Criatura._compone` (`cv:1288-1291`). Con el motor, eso es `compone(F, satura, sin_techo=True)` (`cv:203-216`), que usa `estado_sin_techo` (`cv:169-180`): el State del motor con el mínimo basal, sin reescalar lo que pasa del máximo.
- **Al imaginar:** cada foto de cada opción va por ahí (`cv:2965-2970`), también la segunda foto de la voz (`cuerpo_vc1.py:64`).
- **En lo que siente en el turno:**
  - Lo que la criatura siente ahora son las seis sumas crudas de la foto de ahora (`cv:122-132`, `seis_ahora` en `cv:2457-2463`). No pasan por el State: ni mínimo basal ni techo. Son las que se apuntan y las que mide la felicidad.
  - El único sitio donde la foto de ahora pasa por el motor es la intensidad de la llamada (`cv:1302`, `_expresion_calc`). También va por `_compone`, sin techo.
- **La comprobación automática** (`cv:182-200`) asegura que, por debajo del máximo, la distancia sin techo es igual a la de `model.py`.

**El texto, corregido.**
- Lo que dice («al comparar lo que imagina, la criatura de este trabajo no lo aplica») es cierto.
- Lo que da a entender («para vivir es razonable»; «la criatura no aplica el techo al comparar lo que imagina») no lo es: tampoco lo aplica al vivir.

**Cuántas veces la suma de las fuerzas pasa del máximo** (`frases_169.py`, en las seis sumas apuntadas de la foto de ahora, VOL_MAX = 8 importado de `mm`):

| sellado | criatura | turnos-criatura con las seis | suma ≥ 8 | parte | suma ≥ 7,7 (con el mínimo basal) | la más alta |
|---|---|---|---|---|---|---|
| v6 | RG69r+voz | 23.690.131 | 31.614 | 0,13 % | 45.648 | 12,05 |
| v6 | RG69r | 23.472.476 | 32.351 | 0,14 % | 46.449 | 11,66 |
| v6 | RG68r | 23.351.419 | 55.881 | 0,24 % | 84.831 | 11,82 |
| escalera | S69+voz | 23.379.597 | 70.631 | 0,30 % | 97.109 | 12,00 |
| escalera | P69+voz | 23.559.974 | 41.226 | 0,17 % | 61.206 | 12,06 |

- Las demás clases de criatura del v5 están en `salida/frases_169.md`.
- El mínimo basal suma como mucho 0,3, así que la cuenta exacta del State queda entre las dos columnas.
- **En lo que imagina, cuántas veces pasa del máximo no se puede saber sin rejugar:** las fotos imaginadas no están apuntadas, y `decisiones.jsonl.gz` solo guarda nombres y tres números por valorador.

## Parte 11. Una cuenta con el motor

Con `motor/model.py` tal como está: `State` y `opponent_distance` importados, `DEFAULT_CONFIG` y ninguna partida (`cuentas_169.py`).

**El reposo.**
- `model.py` no trae un estado de reposo escrito.
- Lo que el código del valle llama «el reposo del motor» es «el reposo del modelo del paper dos» (`cfg`: `vivir_bien.reposo_dos`): ganancia 0,82 en el cuerpo, 1,6 en recursos y 0,68 en el vínculo, sin pérdida. Son números de Manel, no importables.
- He puesto recursos y vínculo en ese reposo, y el cuerpo con lo que pide el prompt. Es lo más simple, y lo digo.

| el cuerpo: ganancia · pérdida | distancia al partir | baja al ganar 0,1 más | baja al perder 0,1 menos | cociente (ganar / perder) |
|---|---|---|---|---|
| 0,7 · 0,2 | 1,2036 | 0,0254 | 0,0715 | **35,5 %** |
| 0,5 · 0 | 1,1401 | 0,0413 | no se puede: la pérdida ya es 0 | — |

- **El 35 % de la mesa se confirma.**
- **El 84 % no.** Con la pérdida en 0 no se puede bajar 0,1: el motor no admite fuerzas negativas (`mm:22-23`).
  - Como cuenta solo formal, con la pérdida a −0,1, el cociente sería 67,9 %.
  - En la rejilla de abajo, el 84 % sale cerca de una ganancia de 0,3 con una pérdida de 0,1 a 0,2 (87 % y 82 %), no de 0,5 · 0.
- **Con el otro reposo posible, el de `model.py`,** todas las fuerzas están a 0 (`state_from_observables` con `HP_EQ` y `ENERGY_EQ`; el mínimo basal las deja en 0,05). Con el cuerpo en 0,7 · 0,2, **ganar 0,1 hace que la distancia suba** (+0,0198) y perder 0,1 menos la baja 0,0561: el cociente es −35,4 %. La razón es el cruce: la tensión del cuerpo hace pesar más lo lejos que están recursos y vínculo, que están en cero.

**¿Es estable? No: depende mucho del punto de partida.** El cociente en una rejilla, con recursos y vínculo en el reposo del paper dos:

| ganancia \ pérdida | 0,1 | 0,2 | 0,3 | 0,5 |
|---|---|---|---|---|
| 0,30 | 87 % | 82 % | 78 % | 73 % |
| 0,50 | 65 % | 63 % | 61 % | 59 % |
| 0,70 | 31 % | 36 % | 38 % | 42 % |
| 0,82 | 1 % | 13 % | 21 % | 29 % |
| 0,90 | −26 % | −6 % | 6 % | 20 % |
| 1,00 | −75 % | −36 % | −16 % | 6 % |
| 1,20 | −297 % | −140 % | −81 % | −30 % |

**Cómo se lee:**
- Lejos de la meta del cuerpo (ganancia baja), ganar 0,1 casi vale lo que perder 0,1 menos.
- Cerca de la meta (la del cuerpo es 1,0), ganar ya no ayuda: con la ganancia por encima de 0,8, ganar más llega a empeorar la distancia, por la tensión.
- Siempre ayuda más quitar una pérdida que sumar la misma ganancia: el cociente nunca pasa del 100 % en la rejilla. Pero cuánto más depende de dónde se parte.

---

## Lo que no se puede sin rejugar

- **«Unas siete comidas».** Lo que aprende de cuánto sube el hambre y de cuánto quita una comida no está apuntado (parte 1).
- **El techo al imaginar** (parte 10).
- **Qué parte de lo ganado es de cada clase** (parte 7, del 168).
- **La medida en sombra, en las 190 partidas que faltan del v6 y en P11 del v2 al v5** (parte 9, del 163).

## Lo que he tenido que decidir yo

Todo por lo más simple:
- **Las bandas de las cifras en palabras,** y que lo dicho en palabras enteras se redondee a la unidad.
- **Qué fuente cito para cada número:** la del informe que lo contó primero con las partidas selladas.
- **Los tres sellados en que se apoya el texto,** para las frases de la parte 2: v5, v6 y escalera. No he leído las partidas del v1 al v4.
- **El reposo de la parte 11:** el del paper dos, y aparte, el de `model.py`.
- **El vaivén emparejado:** como su tamaño (|vaivén|), con la misma cuenta del 157.

## Tropiezos

- **El primer `find`** para buscar el texto por todo el disco tardó demasiado. Lo paré.
- **Las expresiones de búsqueda.** Siete expresiones de la primera versión de `cifras_169.py` no casaban: algunos informes usan «-» y otros «−», y en una había una mayúscula. Las arreglé, y el programa vuelve a comprobar todas al correr.
- **Tres bandas demasiado estrechas.** Las ensanché por la regla de redondear a la unidad, y lo digo arriba.
- **En `apuestas_169.py`** el resultado del v2 va en la segunda casilla de su tabla, y las columnas del 162 estaban cruzadas. Arreglado antes de dar ningún número.

## Ficheros, gasto y procesos

- **Nuevos:**
  - el texto, `paper8_ES_montado_v1.md`;
  - los cuatro programas: `cifras_169.py`, `frases_169.py`, `apuestas_169.py` y `cuentas_169.py`;
  - sus salidas en `salida/`: `cifras_169`, `frases_169`, `apuestas_169` y `cuentas_169`, en `.md` y `.json`, y `frases_169.log`. `frases_169.json` (1,2 MB, una fila por partida) se queda fuera del commit, porque es dato por partida;
  - este informe.
- **Tiempo:** la pasada por las 3.200 partidas tardó 5 minutos, con 8 procesos.
- **Gasto:** 0 créditos de la plataforma y 0 dólares de la consola de Anthropic. No se ha usado la clave.
- **Procesos:** al acabar no queda ninguno vivo, ni ninguna shell en segundo plano.
