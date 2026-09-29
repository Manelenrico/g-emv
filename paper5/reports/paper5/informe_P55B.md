# P5-5B — El consejero habla en formas

Banco con modelo real por API. **600 llamadas, cero errores, 4,4448 $** con el
humo incluido, de un tope de 15. Motor, tabla y decisor intactos. Sin
plataforma, sin partidas: escenas reales de los diarios de S-2.

**El titular es que el idioma funciona, y funciona mucho mejor de lo que
esperaba el sello.** Pedirle formas al consejero en vez de pasos hace que sus
propuestas pasen la puerta ancha honesta en el **10,48 %** (Haiku) y el
**18,13 %** (Sonnet) de las construidas, cuando las mismas propuestas de un paso
del cuatro pasan en el **0,00 %** —ninguna de 367— y el futuro bueno conocido
pasa en el 3,00 %.

**Y el titular incómodo es que la mitad emocional es casi toda imitación.** La
dirección que el consejero afirma coincide con la que el cuerpo proyecta el
**45,75 %** de las veces en la vida y el **20,08 %** en las manos —por debajo
del azar, que con tres opciones es el 33,3 %—, y **el renglón que nombra como
causa solo cambia de verdad en el 7,53 %** de los tramos. Habla el idioma con
gramática perfecta y con semántica prestada.

**F1 cumple, F2 cumple, F6 cumple. F3, F4 y F5 fallan.**

---

## Lo que hay que decir antes de las cifras

### El consejero del cuatro no era Sonnet 4.5: era Haiku 4.5

El encargo dice «el mismo que el consejero del cuatro en el campo (Sonnet 4.5)».
El diario dice otra cosa, en los 160 ficheros de los dos brazos:

```
80 ('S2_B', 'us.anthropic.claude-haiku-4-5-20251001-v1:0', 'M2')
80 ('S2_C', 'us.anthropic.claude-haiku-4-5-20251001-v1:0', 'M2')
```

Las dos cláusulas no podían cumplirse a la vez. Por decisión de mesa se corren
**los dos modelos sobre menos escenas**: 200 en vez de 300, y tres brazos de 200
llamadas, que son las 600 del encargo.

| brazo | instrucción | modelo |
|---|---|---|
| **FORMAS · Haiku** | la de B1 | `claude-haiku-4-5-20251001` |
| **FORMAS · Sonnet** | la de B1 | `claude-sonnet-4-5-20250929` |
| **CASILLAS · Haiku** | la del cuatro, **tal cual** | `claude-haiku-4-5-20251001` |

**La instrucción de CASILLAS no es una imitación: es el mismo texto.** Su md5 y
el de su esquema son los que el diario del campo registró:

```
instruccion de CASILLAS: md5 f6882517309310ca5aa7e9e18177707f (el campo: f6882517309310ca5aa7e9e18177707f)
esquema de CASILLAS:     md5 ac9c650a3c912d8346d82db2972b5059 (el campo: ac9c650a3c912d8346d82db2972b5059)
```

### La puerta de calidad del relato: 91,58 %, y el 8 % que no he cerrado

Antes de pagar una sola llamada monté una comprobación: reconstruir los relatos
del brazo C y compararlos con el `relato_md5` que el propio diario guardó.

| versión | reconstruidos byte a byte |
|---|---|
| primera | 146/234 = **62,39 %** |
| con `_golpe_hermano` (el candidato añadido que el campo sí ponía, `policy_cortex.py:746-780`) | 87/95 = **91,58 %** |

Encontré y corregí la causa grande. **El 8,4 % restante no lo he cerrado**:
difiere en una sola línea —entre 16 y 87 bytes— y probé cuatro variantes
(memoria antes/después del ataque, `agresores_det` vacío, `cert` a nulo,
`parte_fresco` a nulo) sin que ninguna lo arreglara. El diario solo guarda el
texto entero en el 6,3 % de las llamadas, así que no pude diferenciar más.

**No invalida el banco, y digo por qué:** las escenas de P5-5B salen de **S2_A**,
donde no hubo consejero, así que no existe un «texto del campo» que igualar. El
relato lo genera el mismo `relator_t5.relato(e, True)` con los mismos registros.
La comprobación mide la fidelidad de mi armado de `e` contra otro brazo, y esa
fidelidad es del 91,58 %. La cifra queda dicha.

### Temperatura y esquema, declarados

**No se pasa `temperature`.** El campo tampoco la pasaba (`cortex_t5.py:930-932`
manda solo `anthropic_version`, `max_tokens`, `system` y `messages`), y además
el SDK instalado (`anthropic` 1.5.0) **ya no expone ese parámetro**. Las tres
corridas usan la de por defecto del modelo. **El banco es, por tanto,
estocástico**; lo que está fijo es la semilla de las escenas (20260919).

El esquema **se pide en el prompt, no se impone con `output_config`**, igual que
en el campo, que no podía imponerlo. `max_tokens`: 512 en CASILLAS (el valor del
campo) y 1500 en FORMAS, porque una forma de cuatro tramos no cabe en 512.

---

## B0 · Las escenas

200 de las 2.225 del banco, semilla **20260919**, estratificadas: **100 con
futuro bueno conocido** (`d(t+100) < d(t)`, la definición de O-después) y **100
sin él**. Salen de los mismos 40 diarios de S2_A y de los mismos tics vivos
(≥300, múltiplos de 50) que P5-3 y P5-4.

Lo que el consejero recibe, idéntico en los tres brazos:

1. el **manual M2** entero (16.923 caracteres), en el bloque con
   `cache_control: ephemeral`, como en el campo;
2. el **relato de la escena** (`relato(e, True)`, el del brazo C, con el bloque
   de dolores): mediana 1.436 caracteres, máximo 2.796;
3. los **seis números del cuerpo**: necesidad y tono de los tres ejes;
4. el **registro del hermano** en ese tic, de su propio diario: casilla, vida,
   banda y si le han pegado.

---

## B1 · La instrucción

`cantera/paper5/instruccion_forma.md`, **md5 `02653e4edf04f3bdd9a0ac3deda9aa01`**,
6.714 caracteres. Contiene, en este orden: la regla del juego («solo actúas a
través del cuerpo; el cuerpo decide; te escucha más cuanto mejor acaban las
formas que acepta»); las tres dimensiones; **los 21 renglones, uno por línea,
con qué lo enciende y qué lo apaga**; qué es una forma (de uno a cuatro tramos,
las dos mitades obligatorias, un cierre); lo que no se le pide («no adivines
dónde estarán los rivales… el cuerpo no lo cobrará»); y el permiso explícito
para callar.

De los 21 renglones, **tres están callados en este cuerpo** y la instrucción lo
dice: `MIEDO_APRENDIDO` y `S-VIDA-AJENA` por interruptor, `S-COMPANIA` por el
candado del banco 62.

### Las tres llamadas de humo

```
manual M2: 16923 caracteres, md5 1416fb5ef1e207091af0b9aea6fc3eec
instruccion de FORMAS: 6714 caracteres, md5 401510e7ba6fd329ab0a2937818d954f
temperatura por defecto del modelo (no se pasa; el SDK 1.5.0 no la expone)
```

**Humo 1 · FORMAS · Haiku · 2.729,6 ms · 0,002685 $** — respuesta cruda:

```json
{"formas": [
  {"tramos": [
     {"destino": [23, 20], "intencion": "ir", "esperar": 0,
      "vida": "-", "manos": "0", "vinculo": "+", "por": "S-SOLEDAD",
      "porque": "tu hermano esta cerca pero solo a 6 casillas; acercarse reduce la distancia"},
     {"destino": null, "intencion": "usar", "esperar": 0,
      "vida": "+", "manos": "0", "vinculo": "+", "por": "S-HERIDO",
      "porque": "tu hermano esta en las ultimas; una racion en su mano lo salva de lo inmediato"}],
   "final": "llegas donde esta tu hermano y le das lo que lleva la mochila para que se cure"},
  {"tramos": [
     {"destino": [24, 24], "intencion": "ir", "esperar": 0,
      "vida": "0", "manos": "-", "vinculo": "-", "por": "R-LLAMADA",
      "porque": "en la fortaleza hay armas que necesitas; tu hermano queda mas lejos pero es lo que pide el tablero"}],
   "final": "te acercas al centro buscando arma mientras el anillo te deja tiempo"}],
 "callar": false}
```

**Humo 2 · FORMAS · Sonnet · 10.475,5 ms · 0,009346 $** — respuesta cruda:

```json
{"formas": [
  {"tramos": [
     {"destino": null, "intencion": "esperar", "esperar": 5,
      "vida": "0", "manos": "0", "vinculo": "0", "por": "F-ANTICIPACION",
      "porque": "esperar a que se enfrien las piernas"},
     {"destino": [23, 20], "intencion": "ir",
      "vida": "-", "manos": "0", "vinculo": "+", "por": "S-HERIDO",
      "porque": "acercarme a mi hermano que esta en las ultimas"},
     {"destino": "botiquin", "intencion": "usar",
      "vida": "0", "manos": "-", "vinculo": "+", "por": "R-HERMANO-FALTA",
      "porque": "dejarle el botiquin en el suelo para que se cure"}],
   "final": "mi hermano tiene una cura junto a el y yo estoy ahi"}],
 "callar": false}
```

**Humo 3 · CASILLAS · Haiku · 3.404,5 ms · 0,002748 $** — respuesta cruda:

```json
{"propuestas": [
  {"accion": "Acércate al asiento 8, que está a 3 casillas y está en las últimas (menos de 33 de vida)",
   "motivo": "Es el más vulnerable ahora mismo y está dentro de tu alcance; eliminarlo te da un punto y reduce la competencia."},
  {"accion": "Busca un arma en el suelo explorando hacia la Fortaleza o los cajones del anillo medio",
   "motivo": "Sin arma no puedes defenderte ni atacar; las armas de primera están en la Fortaleza y hay cajones menores repartidos que podrían tener lo que necesitas."},
  {"accion": "Mantente en movimiento hacia el centro del círculo seguro, lejos del asiento 13 que tiene cuchillos",
   "motivo": "Estás dentro del alcance de múltiples jugadores y el círculo se cierra en 932 tics; moverse te da opciones y te aleja del peligro inmediato."}]}
```

**Gasto del humo: 0,014779 $.**

---

## B3 · El traductor

`traductor_forma.py`. Destinos: casilla `[x,y]`, o el nombre de un objeto del
suelo (se resuelve al más cercano de ese tipo), o `null` para quedarse.

| brazo | parsean | formas construidas | intraducibles | tramos con **las dos mitades** |
|---|---|---|---|---|
| **FORMAS · Haiku** | **200/200** | 334 de 337 = **99,11 %** | 3 | 853 de 856 = **99,65 %** |
| **FORMAS · Sonnet** | **200/200** | 353 de 384 = **91,93 %** | 31 | 1.137 de 1.168 = **97,35 %** |
| **CASILLAS · Haiku** | **200/200** | 367 de 599 = **61,27 %** | **232** | 0 de 599 = **0 %** (el esquema del cuatro no tiene mitad emocional) |

**Por qué falla lo que falla:**

| motivo | FORMAS Haiku | FORMAS Sonnet | CASILLAS |
|---|---|---|---|
| no nombra ni casilla ni objeto conocido | 0 | 2 | **135** |
| el objeto nombrado no está en el suelo | 1 | 10 | **96** |
| casilla fuera del mapa o sólida | 2 | **19** | 1 |

**El esquema es lo que arregla la traducción, y se ve en una línea.** Las
propuestas de un paso del cuatro son intraducibles el **38,7 %** de las veces
—«busca un arma explorando hacia la Fortaleza» no es una casilla—, mientras que
pedir un `destino` explícito baja eso al 0,89 % con Haiku. Es el mismo modelo.

Sonnet tropieza donde Haiku no: **19 casillas fuera del mapa o sólidas**, porque
se inventa coordenadas más a menudo al hacer formas más largas.

### F1, por respuesta

| brazo | respuestas con al menos una forma construida |
|---|---|
| FORMAS · Haiku | **198/200 = 99,00 %** (las dos que faltan dijeron callar) |
| FORMAS · Sonnet | **196/200 = 98,00 %** (las cuatro dijeron callar) |

---

## B4 · Por la puerta ancha honesta

Regla **E1+G2, margen 0,02**, comparador en ventana, hermano leído de su diario,
filas de rivales a piso. La misma de P5-3H, sin tocar una línea de `forma.py`.

| llave | construidas | coincide | **pasa la regla** (IC95) | **aceptada** | **en la mesa** (IC95) |
|---|---|---|---|---|---|
| **FORMAS · Sonnet** | 353 | 7 | **64 = 18,13 %** (14,5-22,5) | **36 = 10,20 %** | 56,25 % (44,1-67,7) |
| **FORMAS · Haiku** | 334 | 8 | **35 = 10,48 %** (7,6-14,2) | **27 = 8,08 %** | **77,14 %** (61,0-87,9) |
| O-después | 100 | 0 | 3 = 3,00 % (1,0-8,5) | 0 = 0,00 % | 0,00 % (0,0-56,2) |
| azar emparejado | 100 | 0 | 1 = 1,00 % (0,2-5,4) | 0 = 0,00 % | 0,00 % (0,0-79,3) |
| **CASILLAS · Haiku** | 367 | 0 | **0 = 0,00 %** (0,0-1,0) | **0 = 0,00 %** | — |

Las diferencias, con intervalo:

| comparación | pasa la regla | aceptada |
|---|---|---|
| FORMAS Haiku − CASILLAS | **+10,48** (+7,45, +14,23) | **+8,08** (+5,41, +11,51) |
| FORMAS Sonnet − CASILLAS | **+18,13** (+14,32, +22,49) | **+10,20** (+7,27, +13,80) |
| FORMAS Haiku − O-después | **+7,48** (+1,33, +11,71) | **+8,08** (+3,64, +11,51) |
| FORMAS Sonnet − O-después | **+15,13** (+8,56, +19,91) | **+10,20** (+5,59, +13,80) |
| FORMAS Sonnet − FORMAS Haiku | **+7,65** (+2,41, +12,85) | +2,11 (−2,27, +6,48) |

**Cuatro lecturas.**

1. **El idioma de la forma abre la puerta; el de los pasos no la abre nunca.**
   Cero de 367 propuestas de un paso pasan la regla. No es que pasen pocas: es
   que **no pasa ninguna**, y el intervalo superior es el 1,0 %. La razón es
   estructural y estaba ya en P5-3B: una forma de un tramo que va a una casilla
   tiene un área casi idéntica a la de seguir solo, y el margen de 0,02 la mata.
2. **Sonnet deja pasar más pero acierta menos en la mesa.** Pasa el 18,13 %
   contra el 10,48 %, pero de lo que pasa acepta el 56,25 % contra el 77,14 %.
   En aceptadas sobre construidas la diferencia entre los dos modelos **no
   separa del cero** (+2,11, IC −2,27 a +6,48). **El idioma pesa más que el
   modelo.**
3. **Las formas del consejero pasan más que el futuro bueno conocido**, y eso
   hay que decirlo con cuidado: O-después es el camino que el cuerpo recorrió de
   verdad, resumido en tramos, y pasa el 3,00 %. Una forma inventada de dos a
   cuatro tramos tiene más área que un camino real resumido, porque la forma
   **elige** sus puntos de control y el resumen no.
4. **O-después y el azar aceptan 0 de 100 aquí.** En P5-3H, con 908 escenas,
   O-después pasaba el 4,5 % y aceptaba el 3,85 %. Con 100 escenas pasan 3 y
   aceptan 0; el intervalo de la tasa de mesa va de 0 a 56,2 %. **Con esta n no
   se puede decir nada de O-después en la mesa**, y no lo digo.

---

## B5 · ¿Habla el idioma o lo imita?

Para cada tramo, la dirección que el consejero **afirma** por dimensión, contra
el **signo del cambio de la necesidad** de ese eje en la proyección del cuerpo
(si la necesidad baja, la dimensión mejora). Con tres opciones, **el azar es el
33,3 %**.

| brazo | **vida** | **manos** | **vínculo** |
|---|---|---|---|
| **Haiku** | 237/518 = **45,75 %** (41,5-50,1) | 104/518 = **20,08 %** (16,9-23,7) | 312/518 = **60,23 %** (56,0-64,4) |
| **Sonnet** | 314/741 = **42,38 %** (38,9-46,0) | 228/741 = **30,77 %** (27,6-34,2) | 360/741 = **48,58 %** (45,0-52,2) |

Y el renglón que nombra como causa, ¿cambia de verdad en la proyección?

| brazo | nombrados | **cambia de verdad** | no cambia | renglón inventado |
|---|---|---|---|---|
| **Haiku** | 518 | **39 = 7,53 %** (5,6-10,1) | 460 | 19 |
| **Sonnet** | 741 | **172 = 23,21 %** (20,3-26,4) | 551 | 18 |

**Esto es lo más interesante del encargo, y va contra el sello.**

1. **Las manos van por debajo del azar** (20,08 % con Haiku). No es que no sepa:
   es que **se equivoca sistemáticamente**. La causa es identificable: el
   consejero dice «manos +» cuando va a por un objeto, pero `R-CARENCIA` solo
   baja cuando el arma está **en la mano**, no en la mochila, y `R-LLAMADA` es
   apetitiva y **sube** al acercarse. Da el signo del deseo, no el de la
   necesidad.
2. **El vínculo es lo que mejor acierta, justo al revés de lo predicho.** 60,23 %
   con Haiku. Tiene sentido: el vínculo se mueve con la distancia al hermano y
   con su vida, que es lo único de «los otros» que el consejero **ve de verdad**
   en el registro que le damos.
3. **El renglón nombrado casi nunca cambia: 7,53 %.** Nombra `R-CARENCIA` 284
   veces con Haiku y 288 con Sonnet, y en la inmensa mayoría ese renglón está
   igual al principio y al final del tramo. **Sabe el vocabulario y no sabe
   cuándo se aplica.**
4. **Sonnet es tres veces mejor en esto** (23,21 % contra 7,53 %) y peor en las
   otras dos dimensiones. Es el único sitio del banco donde el modelo pesa más
   que el idioma.

### Los renglones inventados dicen algo

37 de 1.259 tramos nombran un renglón que no existe. **Y todos los inventados
son renglones reales con la letra del eje equivocada**:

| inventado | el de verdad |
|---|---|
| `S-HERMANO-AMENAZA` | `F-HERMANO-AMENAZA` |
| `S-HERMANO-GOLPE` | `F-HERMANO-GOLPE` |
| `S-HERMANO-FALTA` | `R-HERMANO-FALTA` |
| `R-PROVISION` | `S-PROVISION` |
| `S-EXPOSICION` | `S-8-EXPOSICION` |

Se acuerda del renglón y le pone el eje que le parece lógico: lo del hermano
«debería» ser S. **La tabla no se lo parece porque no lo es** —`S-7-AGRESOR`
reparte 0,5 a F y `S-8-EXPOSICION` 0,4 a F—, y el consejero corrige hacia lo
intuitivo. Es un error informativo: dice que ha entendido *la idea* de los ejes
y no *el reparto* de la tabla.

Y **usa `S-COMPANIA` 98 veces (Haiku) y 69 (Sonnet)** pese a que la instrucción
dice que está callado y que no lo use.

---

## B6 · Lo que propone

| | FORMAS Haiku | FORMAS Sonnet | CASILLAS Haiku |
|---|---|---|---|
| formas construidas | 334 | 353 | 367 |
| **formas por respuesta** | 1,67 | 1,77 | 1,84 |
| de 1 tramo | 47 | 4 | 367 (por construcción) |
| de 2 tramos | 108 | 55 | — |
| **de 3 tramos** | **127** | **196** | — |
| de 4 tramos | 52 | 98 | — |
| intención `ir` | 389 | 462 | 367 |
| intención `coger` | 314 | 425 | — |
| intención `esperar` | 78 | 92 | — |
| intención `usar` | 71 | 115 | — |
| **tramos de quedarse** | 155 | 175 | 0 |
| **calla** | **2 = 1,00 %** | **4 = 2,00 %** | 0 |
| **nombra rivales** | **29 = 14,50 %** | **33 = 16,50 %** | **139 = 69,50 %** |

**Dos cosas.**

1. **Decirle que no adivine a los rivales funciona, y mucho.** De hablar de
   ellos en el **69,50 %** de las respuestas a hacerlo en el **14,50 %**. Una
   frase de la instrucción —«el cuerpo no lo cobrará»— divide por cinco lo que
   P5-5A había medido como el 63,93 % del corpus del cuatro.
2. **Callar sigue costándole.** 1 % y 2 %, contra el 0 de 590 del cuatro. Es más
   que cero, pero muy por debajo del 5 % sellado. Tiene permiso explícito y casi
   nunca lo usa: **pedirle consejo es pedirle que hable**.

---

## B7 · El gasto

| brazo | llamadas | errores | **$** | $/llamada | entrada fresca | salida | caché escritura | caché lectura |
|---|---|---|---|---|---|---|---|---|
| FORMAS · Haiku | 200 | 0 | **0,8551** | 0,004275 | 159.085 | 103.398 | 0 | 1.790.600 |
| CASILLAS · Haiku | 200 | 0 | **0,5693** | 0,002846 | 164.285 | 52.992 | 6.618 | 1.316.982 |
| FORMAS · Sonnet | 200 | 0 | **3,0057** | 0,015029 | 159.085 | 130.691 | 8.953 | 1.781.647 |
| humo | 3 | 0 | 0,0148 | — | — | — | — | — |
| **total** | **603** | **0** | **4,4448 $** | | | | | |

**La caché hizo su trabajo:** 4,9 millones de tokens leídos de caché contra
482.455 frescos, o sea **el 91,0 % de la entrada no se pagó a precio de
entrada**. Sin ella, a precio de entrada fresca, la tanda habría costado unos
19 $ y **habría reventado el tope**.

Latencia mediana: Haiku 4.378 ms (formas) y 3.233 ms (casillas), Sonnet
**10.627 ms**. Salida mediana: 502,5 tokens Haiku, 674,5 Sonnet.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **F1** | el traductor construye una forma válida en más del 85 % de las respuestas de FORMAS | B3 | **99,00 %** (Haiku) y **98,00 %** (Sonnet) | **CUMPLE** |
| **F2** | las formas pasan la regla en más del 5 % de las construidas | B4 | **10,48 %** y **18,13 %** | **CUMPLE** |
| **F2** | …y FORMAS más que CASILLAS por más de 3 puntos | B4 | **+10,48** y **+18,13** (CASILLAS: 0,00 %) | **CUMPLE** |
| **F3** | en la mesa, las formas se aceptan **menos** que O-después | B4 | O-después acepta **0 de 100**; las formas, 27 y 36 | **FALLA** |
| **F3** | …y **más** que el azar | B4 | azar **0 de 100** | **CUMPLE** |
| **F4** | la dirección afirmada coincide en más del 70 % para **manos** | B5 | **20,08 %** — *por debajo del azar* | **FALLA** |
| **F4** | …y para **vida** | B5 | **45,75 %** | **FALLA** |
| **F4** | …y **menos para vínculo** | B5 | **60,23 %** — el vínculo es **el mejor** | **FALLA** |
| **F5** | calla en más del 5 % de las escenas | B6 | **1,00 %** y **2,00 %** | **FALLA** |
| **F6** | gasto total por debajo de 12 $ | B7 | **4,4448 $** | **CUMPLE** |

**Los contadores podían variar, comprobado.** El de F1 va del **61,27 %**
(CASILLAS) al **99,11 %** (FORMAS Haiku) sobre formas, con el mismo traductor y
el mismo modelo: lo único que cambia es el esquema. El de F2 va del **0,00 %** al
**18,13 %** según brazo. El de F3 tiene cuatro llaves en la misma tabla, de 0 a
36 aceptadas. El de F4 se reparte en tres dimensiones y dos modelos: seis
valores del **20,08 %** al **60,23 %**, uno por debajo del azar y otro muy por
encima. El de F5 va de 0 (el cuatro) a 4. El de F6 podía reventar el tope: sin
caché habrían sido unos 19 $.

### F3 falla, y falla por la n, no por el fondo

Se selló esperando que O-después fuera el techo. Aquí acepta **0 de 100**, y con
esa n no se puede afirmar nada: el intervalo de su tasa de mesa va de 0 a
56,2 %. En P5-3H, con 908 escenas, O-después pasaba el 4,5 % y aceptaba el
3,85 %. **Lo que sí se puede afirmar con el cero fuera del intervalo es que las
formas del consejero pasan la regla más que O-después** (+7,48 y +15,13), y eso
no es que el consejero sea mejor que la verdad: es que una forma de tres tramos
elige sus puntos de control y un camino real resumido no.

### F4 falla en las tres cláusulas, y es el hallazgo

**El consejero tiene la gramática y no tiene la semántica.** El 99,65 % de sus
tramos traen las dos mitades completas, usa 20 de los 21 renglones, respeta el
esquema en 200 de 200 respuestas. Y sin embargo el renglón que nombra como causa
**solo cambia de verdad el 7,53 % de las veces**, y en las manos acierta el signo
**por debajo del azar**. Lo que produce es una forma **bien formada y mal
fundada**.

---

## Lo que P5-5B deja dicho

1. **La mitad del consejero funciona: el idioma de la forma abre la puerta que
   el de los pasos no abría.** 10,48 % y 18,13 % contra **0,00 %** de 367
   propuestas de un paso del mismo modelo, con el mismo manual y el mismo
   relato. Lo único que cambia es qué se le pide.
2. **Y el esquema es la mitad de la batalla.** Las propuestas de un paso son
   intraducibles el 38,7 % de las veces; pedir un destino explícito lo baja al
   0,89 %.
3. **El modelo importa menos que el idioma.** Sonnet deja pasar más (+7,65) pero
   acepta menos en la mesa, y en aceptadas sobre construidas los dos modelos no
   se separan (+2,11, con el cero dentro).
4. **La mitad emocional es imitación, no comprensión.** El renglón nombrado
   cambia de verdad el 7,53 % (Haiku) y el 23,21 % (Sonnet); las manos van por
   debajo del azar; los renglones inventados son siempre el eje equivocado de un
   renglón real. **Habla el idioma sin saber lo que significan las palabras.**
5. **Pero el vínculo sí lo acierta** (60,23 %), y es justo la dimensión cuyo dato
   real le damos: el registro del hermano. **Cuando se le da el hecho, acierta el
   signo; cuando tiene que deducirlo de la tabla, no.**
6. **Decirle que no adivine a los rivales funciona**: del 69,50 % al 14,50 % de
   respuestas que los nombran.
7. **Y casi nunca calla**: 1 % y 2 %, con permiso explícito para hacerlo.

**Lo que esto sugiere y NO he ejecutado** (propuesta, no decisión): la mitad
emocional, tal como está, **no vale para cobrarle nada al consejero**, porque
acierta menos que el azar en una de las tres dimensiones. Si se quiere usar para
la confianza de P5-4B, habría que pagarle por la mitad del mundo —que sí es
buena— y no por la emocional; o darle, como se le da el registro del hermano,
**el dato de las necesidades proyectadas** y pedirle que las lea en vez de
adivinarlas.

**PARO AQUÍ.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`: **ninguno se ha
tocado**, ni tampoco `forma.py`, que es la regla.

| fichero | md5 |
|---|---|
| `instruccion_forma.md` (el prompt de B1) | `02653e4edf04f3bdd9a0ac3deda9aa01` |
| `traductor_forma.py` | `b310bb72884ef5f4e3510ab803cd2776` |
| `consejero_forma.py` | `ac164782a620e8f58f49bfa3873313ab` |
| `escenas_P55B.py` | `b6d4b71b630921ca75ddb325441dc438` |
| `banco_P55B.py` | `191571fde570610c41f244ef5b3efde9` |
| `manual_M2.md` (sin tocar) | `7d54902964b33d1862798680e304cd3c` |

**Modelos exactos:** `claude-haiku-4-5-20251001` y
`claude-sonnet-4-5-20250929`, por la API de Anthropic.

**Las 603 respuestas crudas están guardadas**, con su `usage` y su coste:
`P55B_crudas_formas_haiku.jsonl`, `P55B_crudas_formas_sonnet.jsonl`,
`P55B_crudas_casillas_haiku.jsonl`, `P55B_humo.json`. Datos y logs:
`P55B_escenas.json`, `P55B_banco.json`, `P55B_gasto.json`,
`P55B_progreso.log`, `P55B_tanda.log`, `P55B_verifica.log`, `P55B_humo.log`.

**La clave** se leyó solo de `cantera/paper5/.env` desde el script, nunca se
exportó ni se imprimió, y ese fichero está cubierto por `.gitignore`
(comprobado con `git check-ignore`).
