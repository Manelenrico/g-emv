# Prompt 171: las cinco figuras pulidas y ocho preguntas de comprobación

*26-nov-2026. Todo sale de registros ya sellados (v5, v6 y la escalera) y de cuentas ya guardadas. No se ha jugado ni rejugado ninguna partida, y no ha hecho falta: las ocho preguntas se pueden contestar con lo guardado. `motor/model.py` no se ha tocado; ninguna clase congelada ni ningún registro sellado se ha editado. Las frases del paper son las que trae el prompt: el texto de la versión 8 no está en el repositorio.*

## Lo que hay

| qué | ruta |
|---|---|
| las cinco figuras nuevas (PNG a 300 ppp y PDF) | `cantera/paper8/figuras_171/fig{1_valle,2_vivas,3_hermana,4_costumbres,5_tres_maneras}_es.{png,pdf}` |
| el fichero de rótulos | `cantera/paper8/rotulos_figuras.csv` (columnas `clave`, `es`, `en`) |
| lo común de las figuras | `estilo_171.py` |
| los programas de las figuras | `figura1_valle_171.py` … `figura5_tres_maneras_171.py` (`--idioma es`, por defecto `es`) |
| los programas de las preguntas | `noches_171.py` (B1, B2), `tras_hermana_171.py` (B3, B4), `dar_171.py` (B5), `bestia_171.py` (B6), `sabe_171.py` (B7), `tres_maneras_171.py` (B8) |
| sus salidas | `salida/{noches,tras_hermana,dar,bestia,sabe,tres_maneras}_171.{md,json}` |

Las figuras del 170 (`figuras/fig*.{png,pdf,txt}`) siguen donde estaban, sin tocar.

## Decisiones que no pedía el prompt (tomé la más simple)

- **El fichero de rótulos** es un CSV con tres columnas: `clave`, `es` y `en`. Tiene una fila por texto (59 en total), y entre ellas van los nombres de los mundos, de los jugadores y de las tres maneras, y el separador decimal (`,` en español). Si a un texto le falta el idioma pedido, el programa para y dice qué claves faltan. Por eso hoy `--idioma en` para enseguida.
- **Los `.txt` de las figuras** no se repiten: los números son los mismos que los del 170. Cada programa nuevo rehace las cuentas y comprueba que su tabla de números es, línea a línea, la del `.txt` del 170. Si no lo fuera, pararía.
- **B5, «al alcance»:** las criaturas a las que el mundo le dejaba dar ese turno. Ver el apartado B5.
- **B1, a qué sitio va una noche al raso:** al sitio donde está dormida más turnos de esa noche, contando solo los turnos dormida fuera de su casa.
- **Margen «por partida»** en B3 y B4: se sacan partidas con reemplazo y se rehace la cuenta con todos sus casos y controles. Son 10.000 remuestreos con semilla 8 y los percentiles de `E6.boot`.

## A1. La coma decimal

Los números de los ejes salen del formateador de siempre de matplotlib, con el punto cambiado por el separador del fichero de rótulos (`estilo_171.Decimal`). Se aplica al eje y de las figuras 2 a 5, el único con decimales: el eje x lleva nombres de mundos o días enteros. La figura 1 no tiene ejes, y su único número es «48 × 48». Ahora se lee, por ejemplo, 0,4 · 1,5 · 1,75 y −0,2.

## A2. Un único fichero de rótulos

`rotulos_figuras.csv`: la columna `es` lleva lo de ahora y la `en` va vacía. Cada programa:
- toma el idioma con `--idioma` (`es` o `en`);
- comprueba que todas sus claves tienen texto en ese idioma;
- saca de ahí todos sus textos: títulos, ejes, leyendas, nombres de mundos, rótulos del mapa y la nota de pie;
- guarda con el sufijo del idioma (`fig2_vivas_es.png`).

En la figura 1 se comprueba además que se usan todas las claves `fig1.*`. Solo se han generado las de español.

## A3. El mapa

- **Sin criaturas ni nombres.** De las dos salidas posibles, quité las ocho: es lo más limpio. En el turno 0, B2 y C1 están encima de la puerta de su casa y la tapan. A2 está en una casilla de su casa, pero pegada al borde, y su nombre quedaba fuera.
- **Las cuatro puertas de casa se ven.** Son el cuadrado blanco con borde negro, más grande que antes: A (21, 22), B (27, 21), C (28, 27) y D (22, 28). Cada una está en un lado distinto de su casa, y la figura lo comprueba.
- **El resto es igual que en el 170:** el tamaño (14,2 × 9,6 pulgadas), los colores, la leyenda (sin «criatura al empezar») y la nota.

## A4. Nada cambia en las figuras 2 a 5 salvo comas y rótulos

Usan los mismos datos y el mismo tamaño, se guardan a 300 ppp y van en una carpeta aparte, `figuras_171/`. Las cuentas son las mismas: las figuras 3 y 4 importan sus funciones del 170, y todas repiten las mismas comprobaciones. Además, cada programa comprueba que su tabla de números coincide con la del `.txt` del 170:

| figura | filas iguales al 170 |
|---|---|
| 2 | 6 |
| 3 | 21 |
| 4 | 12 |
| 5 | 24 |

---

## B1. Noches al raso: dónde

**La frase:** «Contamos como noche al raso la que pasa dormida fuera de su casa más de la mitad del tiempo, también si es en casa de otra».

**La definición** es la sellada (`dormir_fuera_v5/noches_v5.py:69-73`, la de P28 y la figura 4):
- se cuenta cada criatura viva al empezar la noche (turnos 280-399), en los días 1 a 10;
- la noche es «al raso» si pasa más de la mitad de esos turnos dormida con el sitio del balance distinto de «C».

**El sitio** lo escribe el lanzador (`lanza_experimento_v5.py:48`):

| código | qué es |
|---|---|
| C | su casa, sin la puerta |
| O | otra casa, sin la puerta |
| P | una puerta de casa, la suya o la de otra |
| (terreno) | fuera de las casas: «aldea» es la plaza |

**Ojo:** dormir en la puerta de su propia casa también cuenta como «al raso», aunque es muy raro: 1 a 11 noches por grupo.

**Comprobado:** salen los números sellados.
- En las 800 partidas del v6, partida a partida, igual que la caché de `analiza_vc1`.
- En el v6, P28: 24,2 % y 7,0 %.
- En el v5: 23 % y 24 % (RG68r), 5 % y 6 % (RG068r).

**Cuenta:** el número de noches de cada sitio sobre todas las noches. Las dos sequías van juntas, días 1 a 10.

| sellado | criatura | noches | al raso | % | casa de otra | puerta de su casa | puerta de otra | plaza | fuera de la plaza | % sin casa de otra |
|---|---|---|---|---|---|---|---|---|---|---|
| v6 | RG68r | 6.389 | 1.482 | 23,2 | 34 | 1 | 0 | 588 | 859 | 22,7 |
| v6 | RG068r (gemela) | 6.399 | 380 | 5,9 | 41 | 6 | 0 | 255 | 78 | 5,3 |
| v6 | RG69r | 6.382 | 1.542 | 24,2 | 45 | 4 | 0 | 605 | 888 | 23,5 |
| v6 | RG69r+voz | 6.384 | 448 | 7,0 | 31 | 4 | 0 | 265 | 148 | 6,5 |
| v5 | RG68r | 6.383 | 1.502 | 23,5 | 54 | 2 | 1 | 560 | 885 | 22,7 |
| v5 | RG068r (gemela) | 6.400 | 350 | 5,5 | 28 | 9 | 0 | 245 | 68 | 5,0 |

**Margen por partida** (cada partida pesa igual), en el v6 y las dos sequías:
- RG68r: 23,2 [21,9, 24,6] %, y sin casa de otra 22,7 [21,4, 24,0] %.
- RG69r+voz: 7,0 [6,2, 7,8] %, y sin casa de otra 6,5 [5,8, 7,3] %.
- Lo demás está en `salida/noches_171.md`, por mundo y con los cinco mundos juntos.

**Lo que dice:**
- Las noches en casa de otra son pocas: del 2 % al 11 % de las noches al raso.
- La mayoría de las noches al raso son en la plaza o fuera de ella. Fuera de la plaza, casi siempre en el bosque, y después en el huerto.

**Las proporciones sin las noches en casa de otra:**

| frase | con ellas | sin ellas |
|---|---|---|
| «una de cada cuatro» (RG68r) | 23,2 % (1 de 4,3) | 22,7 % (1 de 4,4): sigue siendo una de cada cuatro |
| «una de cada veinte» (RG068r) | 5,5 % en el v5, sequías juntas (1 de 18); 5,9 % en el v6 (1 de 17) | 5,0 % en el v5 (1 de 20); 5,3 % en el v6 (1 de 19) |
| «una de cada catorce» (RG69r+voz) | 7,0 % (1 de 14,3) | 6,5 % (1 de 15,4): **pasaría a una de cada quince** |

- **Programa:** `noches_171.py`.
- **Veredicto:** la definición de la frase **se sostiene tal cual**; es la que se usa. Dos cosas a tener en cuenta:
  - la gemela, contando las noches en casa de otra, está más cerca de una de cada dieciocho que de una de cada veinte;
  - si un día se quitan las noches en casa de otra, el «catorce» pasa a «quince».

## B2. La reserva sola

**La frase:** «En la criatura completa, que lleva la reserva y la voz, las noches al raso pasan de una de cada cuatro a una de cada catorce».

**Cuenta:** misma definición, mismos mundos y mismo sellado. Es el v6, las dos sequías juntas, días 1 a 10; las noches al raso se suman sobre todas las noches.

| | RG68r (ni reserva ni voz) | RG69r (reserva, sin voz) | RG69r+voz (las dos) |
|---|---|---|---|
| noches al raso | 1.482 de 6.389: **23,2 %** [21,9, 24,6] | 1.542 de 6.382: **24,2 %** [22,8, 25,6] | 448 de 6.384: **7,0 %** [6,2, 7,8] |
| con los cinco mundos | 22,6 % | 24,1 % | 6,6 % |

- Las tres salen del mismo sellado.
- **La reserva sola no baja las noches al raso:** RG69r duerme fuera algo más que RG68r. Toda la bajada viene con la voz.
- **Programa:** `noches_171.py`. El margen es el de por partida.
- **Veredicto: se sostiene tal cual.** Una de cada 4,3 pasa a una de cada 14,3. Si el texto da a entender que la reserva ayuda en esto, hay que matizarlo: la bajada es toda de la voz.

## B3. Las llamadas tras perder a la hermana

**Las frases:** «Llama tres cuartos más» en los primeros días, y después «Lo demás no afloja».

**Los datos** son los del 165 (`salida/tras_hermana_165.json`): las llamadas de cada criatura cada día (`criaturas.jsonl.gz`, «llama»). Son 136 casos y 378 controles de A2, de la protagonista del v6. Un día cuenta solo si la criatura lo vive entero.

**Cuenta:** llamadas por día. El margen es de por partida: 73 partidas, 10.000 remuestreos.

| ventana | casos | controles | casos − controles [95 %] | cambio de los casos desde antes [95 %] | cambio, casos − controles [95 %] |
|---|---|---|---|---|---|
| días −5 a −1 | 39,31 | 37,28 | +2,03 [−7,48, +12,25] | — | — |
| días 1 a 5 | 68,09 | 27,32 | **+40,77 [+25,63, +56,96]** | +29,50 [+17,67, +42,00] (**+75 %**) | +39,09 [+25,80, +53,17] |
| días 6 a 15 | 54,25 | 24,99 | **+29,26 [+16,23, +43,22]** | +15,75 [+5,00, +27,02] (+40 %) | +26,56 [+13,42, +39,97] |

- **Casos, de los días 1-5 a los días 6-15** (emparejado): −13,27 [−23,42, −4,55]. **Aflojan**, y el margen no cruza el cero.
- **Controles:** −1,54 [−5,77, +2,96]; no cambian.
- **Programa:** `tras_hermana_171.py`. Comprobado: el cambio de los casos es el del 165, +29,50 y +15,75.
- **Veredicto:**
  - «Llama tres cuartos más» **se sostiene**: +75,0 % sobre lo suyo de antes.
  - «Lo demás no afloja» **hay que matizarlo** en lo que toca a las llamadas. Bajan a algo más de la mitad del aumento (de +75 % a +40 %), aunque siguen muy por encima de antes y de los controles.
  - El texto debería nombrar las llamadas aparte, como hacía la versión montada v1 («solo las noches en vela y las llamadas han bajado a medias»).

## B4. Las muertes tras la pérdida

**Lo que dice el paper:** 6 de 136 casos (4,4 %) y 11 de 378 controles (2,9 %). Son las del 165.

**La ventana:** cualquier día desde la muerte de la hermana hasta el final de la partida, el día 40 (`tras_hermana_165.py:87-89`). En la práctica empieza el día +5: para ser caso hay que vivir al menos 5 días más, y los controles tienen que seguir con su hermana hasta el día +5. Las seis mueren entre 5,2 y 24,4 días después; los controles, entre 6,9 y 20,2.

**Los 378 controles son entradas, no criaturas:** una criatura puede servir de control a dos casos de su partida. Las 11 muertes son 11 criaturas distintas, de 274.

**La diferencia:** casos − controles = **+1,5 puntos [−2,1, +5,6]**. Es bootstrap por partida: 73 partidas, 10.000 remuestreos, semilla 8. **Cruza el cero.**

**Las seis:**

| mundo | semilla | criatura | día en que muere la hermana | muere días después | causa |
|---|---|---|---|---|---|
| sequía dura | 30167 | D2 | 13 | 9,8 | la bestia |
| sequía dura | 30178 | A1 | 13 | 5,2 | el terreno (el daño de la zona salvaje, `mundo.py:689`) |
| sequía dura | 30184 | B2 | 15 | 12,8 | la bestia |
| sequía dura | 30197 | B2 | 17 | 16,8 | el hambre |
| bestias que crían | 30180 | A2 | 11 | 17,0 | la bestia |
| bestias que crían | 30196 | A2 | 11 | 24,4 | la bestia |

- **Programa:** `tras_hermana_171.py`.
- **Veredicto:** «no vemos que muera más» **se sostiene**. Conviene añadir el margen: con 6 y 11 muertes, el intervalo va de −2 a +6 puntos, y no se puede descartar ni un efecto pequeño ni ninguno.

## B5. A quién se da

**La frase:** «En la abundancia solo seis de cada cien comidas dadas van a una criatura flaca. En el mundo normal son veintiocho. En la sequía, cuarenta y dos, y en la sequía dura, la mitad».

**Cada entrega** se cuenta como la pieza sellada `cierre_v46` (líneas 43-46) y P7. Es una acción «dar» con resultado «ok» y tipo «comida» de la protagonista, en el v6. La que recibe está flaca si el turno anterior tenía más de 60 de hambre (`umbral_flaca`, leído del mundo). Salen 6,0 · 28,4 · 41,7 · 50,9 · 50,2 %, comprobado.

**Lo que conté como alcance:** las criaturas a las que el mundo le dejaba dar ese turno (`valle/mundo.py:591-595` y `:819-822`). Son las que cumplen tres cosas:
- están vivas;
- están pegadas, a una casilla exacta, en diagonal también (`Mundo.vecinas`);
- tienen la bolsa sin llenar (menos de 6).

Se mira en el estado del turno anterior. La que recibe estuvo en ese alcance en las 2.804 entregas, sin excepción.

**«Lo que tocaría dando sin mirar»:** para cada entrega, la parte de flacas en su alcance; luego la media de todas las entregas. La diferencia es lo dado a flacas menos eso, en puntos. El margen es de por partida.

| mundo | entregas | dado a una flaca | había flacas al alcance (tocaría) | diferencia, puntos [95 %] | criaturas al alcance, media |
|---|---|---|---|---|---|
| abundancia | 348 | 6,0 % | 4,5 % | +1,6 [+0,0, +5,4] (**toca el cero**) | 1,04 |
| normal | 328 | 28,4 % | 26,6 % | +1,8 [+0,9, +2,8] | 1,09 |
| sequía | 733 | 41,7 % | 36,0 % | +5,7 [+3,7, +8,3] | 1,14 |
| sequía dura | 587 | 50,9 % | 44,5 % | +6,4 [+4,8, +8,2] | 1,17 |
| **bestias que crían** | 808 | **50,2 %** | 43,6 % | +6,7 [+4,5, +9,5] | 1,19 |
| los cinco | 2.804 | 40,1 % | 35,0 % | +5,2 [+4,1, +6,3] | 1,14 |

**Lo que dice:**
- Casi siempre hay una sola criatura al alcance (de 1,04 a 1,19 de media), y en el 80 % de las veces es la hermana.
- En todos los mundos, **siempre que había una flaca al alcance, la comida fue a una flaca**: la parte de entregas con alguna flaca al alcance es igual a la parte dada a una flaca.
- Pero la subida de 6 a 50 sigue sobre todo a cuántas flacas había: de 4,5 a 44,5. Dando sin mirar, la parte ya subiría casi lo mismo.
- Elegir a la flaca entre varias añade poco: de +1,6 a +6,7 puntos. En la abundancia no se distingue de cero.
- A las vecinas sí se les da mucho más a las flacas de lo que tocaría: +18,4 puntos con los cinco mundos juntos (`salida/dar_171.md`). Pero son solo 545 de las 2.804 entregas.

- **Programa:** `dar_171.py`.
- **Veredicto:** los números **se sostienen**. Hay que **matizar** la lectura que los sigue en el paper: «cuanto más hambre hay, más de lo que da va a donde hace falta». No es que reparta mejor según la necesidad. Da a quien tiene pegada, casi siempre su hermana, y cuando hay hambre esa está flaca más a menudo. Mirar si está flaca sube la parte solo unos pocos puntos.

## B6. La bestia

**La frase:** «a la bestia se la echa entre dos».

**La regla del mundo** (`valle/mundo.py:339-345`; `config_valle.json`, bestia → pieza_g → echar, `umbral_criaturas` 2): la bestia solo se va si la empujan en el mismo turno **dos o más**. Con una sola, el mundo no puede echarla.

**La que no lo es**, según el contador del 164:
- **Dónde y cuándo:** bestias que crían, semilla 30198, día 24 (turno 9.224), la bestia «bestia». La «bestia2» está en la casilla de al lado.
- **Antes:** en el turno 9.223, las dos bestias le roban comida a A1 (dos comidas) y a B1 (una). A1 tenía 76,5 de vida.
- **En el 9.224:** A1 y B1 empujan las dos a «bestia». El mundo apunta `bestia_echada`, con `criaturas: 2` y fuerza 2,83, y «bestia» se va lejos y suelta las dos comidas de B1. En el mismo turno la bestia pega a A1 dos veces («se resiste» y «no lleva nada», la segunda de «bestia2»), y A1 muere.
- **El fallo:** el contador del 164 (`seccion5_164.py:47-50`) se salta a las criaturas que constan muertas en el registro de ese turno. Por eso vio solo a B1.

**Cuenta:** en las 200 partidas de la protagonista del v6 hay 304 expulsiones. El propio mundo las apunta **todas con dos o más** (304 de 304; la n más baja es 2).

- **Programa:** `bestia_171.py`.
- **Veredicto:** es **un fallo del contador, no una excepción**. La frase **se sostiene tal cual**, y la cifra buena es 304 de 304. El «303 de 304» de `informe_prompt_164.md` está mal, y lo dejo apuntado (no lo arreglo).

## B7. Lo que sabe y no usa

**La frase:** «De las treinta y una cosas, nueve están escritas y nada en ella las lee».

**La lista:** los 31 recuerdos heredados de `salida/lee_criatura_161.json`. Son de la protagonista, clase `cuerpo_vr1.RG69V`, con la cadena RG69V → VC1 → RG69 → Criatura. Se comprueba que son 31 y todos heredados.

**Quién los lee:** las líneas son las del 163, con la función que las contiene, sacada del propio `cuerpo_valle.py`. Lo que decide el número está comprobado en el código por el programa:
- **(a)** ningún fichero de la cadena, ni el cuaderno, escribe «hecho:» fuera de un comentario, ni lee el cuaderno entero;
- **(b)** `campo` se queda con el primer recuerdo que tiene la clave. Para «lo que dura la comida» es el del almacén, y `guardar:comida` no se pide por ningún otro camino;
- **(c)** la clave «da» de un recuerdo no se lee en ninguna línea;
- **(d)** los números de echar y matar se cargan en `hechos_g` y se leen en `_foto_bestia_g` (cv:1591 y cv:1598).

| n.º | qué | quién lo lee (cuerpo_valle.py) | ¿lo usa? |
|---|---|---|---|
| 1 | una comida quita hambre | 2708 `cree_comida`, 2308 `comidas_dos_dias` | sí |
| 2 | la medicina cura | 1651 `_filas_orig`, 2193 `_filas_rg`, 2643 `foto`, 2705 `_come`, 1901 `_rad_vive` | sí |
| 3 | la zona salvaje hiere, de día (y da medicina 0,5) | 849 `dano_sitio`, 2526 `foto`, 912 `a_anillo`, 923 `fuentes_sitio` | **a medias:** el daño sí, el «da medicina» no lo lee nadie |
| 4 | ídem, de noche | ídem | **a medias**, igual que la 3 |
| 5 | en el bosque aparece comida, de día | como la 3 | se lee, pero vale 0 |
| 6 | ídem, de noche | como la 3 | se lee, pero vale 0 |
| 7 | el huerto trabajado da fruto | 1382 `plantas_por_trabajar`, 2497 `foto`, 2788 `candidatos_ir`, 1446 `vive_sitios`, 745 `observa` | sí |
| 8 | la comida se conserva (almacén) | 2305 `comidas_dos_dias` (`campo`) | sí (solo lo que dura en la bolsa) |
| 9 | ídem, despensa | nadie (`campo` se queda con la 8) | **no** |
| 10 | ídem, bolsa | nadie | **no** |
| 11 | ídem, suelo | nadie | **no** |
| 12 | de noche viene la bestia | 884 `hasta_noche`, 913 `a_anillo`, 2520 `foto`, 891 `peso_noche` | sí |
| 13 | la casa es segura de noche | 2526 `foto`, 912 `a_anillo` | se lee, pero vale 0 |
| 14 | dormida fuera, la bestia te pega | 2520 `foto` | sí |
| 15 | los matorrales del bosque dan fruto | 2318 `falta_saber`, 2596 y 2599 `foto` | sí |
| 16 | si llamas, viene alguien la mitad de las veces | 1215 `_p_llamada`, 1269 `_elige_llamada` | sí |
| 17 | la hermana, cerca | 1815, 1971, 1985, 1532, 2072 (`radar`, `_rad_filas_*`, `nac`, `lo_que_era`) | sí |
| 18 | la hermana, trato | 2072 y 2075 `nac`, 1951 `_rad_vinculos` | sí |
| 19 | fuente: el almacén | 1820 `fuentes_f`, 2340 `valor_fuente` | sí |
| 20 | fuente: las cajas | 734 y 750 `observa`, 921 `fuentes_sitio` | sí |
| 21 | fuente: las bayas | 735 `observa` | sí, si ve una |
| 22 | guardar una medicina | 1652 `_filas_orig` | sí |
| 23 | dar una medicina | 1675, 1686, 1697 `_filas_orig`, 2102 `valor_dar` | sí, si alguna está herida |
| 24 | dar una comida | 1683, 1688, 1695 `_filas_orig`, 2101 `valor_dar`, 2213 `_filas_rg` | sí, si alguna está flaca |
| 25 | a veces aparece un árbol dulce lejos | nadie | **no** |
| 26 | al atardecer la bestia pasa por los árboles | nadie | **no** |
| 27 | echar a la bestia (entre dos) | el recuerdo, nadie; sus números, 1591 `_foto_bestia_g` | **a medias** |
| 28 | matar a la bestia | el recuerdo, nadie; sus números, 1598 `_foto_bestia_g` | **a medias** |
| 29 | la bestia ataca a una sola | nadie (cv:572: «hoy no los lee nada») | **no** |
| 30 | un empujón lo gana el bando mayor | nadie | **no** |
| 31 | empujar a la bestia sale bien con dos | nadie (lo que pasa al empujar está escrito aparte, en `_foto_bestia_g`) | **no** |

(La tabla entera, con cada línea y su función, está en `salida/sabe_171.md`.)

**Las dos dudosas, la 27 y la 28:**
- **Lo que no se lee:** el recuerdo en sí, el que va al cuaderno con su texto.
- **Lo que sí se lee:** los números de la misma entrada de la cultura (`cultura_hechos_v44.json`), que al nacer van a `hechos_g` (cv:566).
  - Para echar: el exponente, el umbral de dos, lo lejos que se va, el golpe y el peso del empujón.
  - Para matar: la vida, la cura, el golpe y la comida que deja.
- La criatura usa esos números al imaginar empujar o pegar a la bestia. Sabe lo que dicen esas dos cosas, aunque no por el cuaderno.

**El número:**
- **Ocho** no las lee nada, en ninguna forma: 9, 10, 11, 25, 26, 29, 30 y 31.
- **Dos** se leen a medias, por sus números: 27 y 28.
- Además, de la 3 y la 4 no se lee una parte, el «da medicina».
- Y tres se leen, pero valen 0: 5, 6 y 13.

- **Programa:** `sabe_171.py`.
- **Veredicto:** **la frase es falsa con «nueve».** Hay que escribir «ocho» («ocho están escritas y nada en ella las lee»), y si se quiere, añadir «y de otras dos solo usa los números». Nueve no sale con ningún criterio: son ocho estrictas o diez contando las dos a medias. El nueve del 163 y el 169 contaba la 27 y la 28 y dejaba fuera la 31.

## B8. Frente a S y frente a P, mundo por mundo

**Las frases:** «La del motor queda por encima con todas las varas, en los cinco mundos» (frente a P), y «en los mundos fáciles va por delante la que suma» (frente a S, en el total).

**Las medidas** son las cuatro de la figura 5, con sus mismas fuentes, y la supervivencia (`cierre_v46`). Son 600 partidas: la protagonista del v6 y S69+voz y P69+voz de la escalera, semillas 30161-30200.

**La diferencia** va emparejada por valle. El margen es `E6.boot`, con 10.000 remuestreos de valles; con los cinco mundos juntos, sobre los 200 valles.

**Comprobado:**
- felicidad, total y balance más bajo dan las diferencias de las tablas del 167;
- vivas, motor − S, da +0,19, +0,12 y +0,50, las del texto.

**cruza** quiere decir que el intervalo contiene el cero. En los empujones, negativo es mejor para la del motor.

**RG69r+voz − S69+voz (la que suma):**

| medida | abundancia | normal | sequía | sequía dura | bestias que crían | los cinco |
|---|---|---|---|---|---|---|
| empujones al día, días 1 a 10 | −3,9 [−5,0, −2,8] | −2,9 [−3,8, −2,1] | −3,8 [−4,9, −2,7] | −2,7 [−3,5, −1,9] | −2,5 [−3,4, −1,6] | −3,1 [−3,6, −2,7] |
| felicidad de la aldea (0 a 100) | +2,5 [+1,7, +3,4] | +0,7 [−0,7, +2,2] **cruza** | +3,8 [+2,0, +5,5] | +3,9 [+0,9, +6,8] | +4,3 [+2,3, +6,3] | +3,1 [+2,2, +3,9] |
| total de los tres balances | **−0,083 [−0,116, −0,048]** | **−0,092 [−0,139, −0,048]** | +0,013 [−0,054, +0,076] **cruza** | +0,077 [−0,044, +0,195] **cruza** | +0,074 [−0,001, +0,152] **cruza** | −0,002 [−0,036, +0,033] **cruza** |
| balance más bajo de los tres | −0,006 [−0,018, +0,006] **cruza** | −0,001 [−0,020, +0,018] **cruza** | +0,055 [+0,028, +0,081] | +0,095 [+0,046, +0,142] | +0,086 [+0,053, +0,120] | +0,046 [+0,031, +0,061] |
| **vivas el día 40** | +0,00 [+0,00, +0,00] **cruza** | +0,05 [+0,00, +0,12] **cruza** | +0,12 [−0,07, +0,33] **cruza** | **+0,50 [+0,15, +0,85]** | +0,28 [−0,17, +0,75] **cruza** | **+0,19 [+0,07, +0,32]** |

**RG69r+voz − P69+voz (la de la posición):**

| medida | abundancia | normal | sequía | sequía dura | bestias que crían | los cinco |
|---|---|---|---|---|---|---|
| empujones al día, días 1 a 10 | −1,6 [−2,2, −1,1] | −1,7 [−2,3, −1,1] | −1,9 [−2,6, −1,2] | −1,6 [−2,1, −1,1] | −1,8 [−2,3, −1,4] | −1,7 [−2,0, −1,5] |
| felicidad de la aldea (0 a 100) | +3,6 [+2,6, +4,6] | +2,7 [+1,4, +4,1] | +4,2 [+2,6, +6,0] | +3,8 [+0,7, +6,8] | +5,3 [+2,7, +7,9] | +3,9 [+3,0, +4,9] |
| total de los tres balances | +0,100 [+0,067, +0,134] | +0,080 [+0,038, +0,123] | +0,142 [+0,083, +0,205] | +0,185 [+0,061, +0,307] | +0,179 [+0,095, +0,264] | +0,138 [+0,103, +0,172] |
| balance más bajo de los tres | +0,040 [+0,027, +0,053] | +0,038 [+0,021, +0,055] | +0,068 [+0,044, +0,093] | +0,096 [+0,045, +0,145] | +0,083 [+0,048, +0,119] | +0,065 [+0,051, +0,079] |
| vivas el día 40 | +0,05 [+0,00, +0,15] **cruza** | +0,00 [+0,00, +0,00] **cruza** | +0,20 [−0,03, +0,42] **cruza** | +0,17 [−0,23, +0,57] **cruza** | +0,10 [−0,35, +0,53] **cruza** | +0,10 [−0,03, +0,23] **cruza** |

**La supervivencia, motor − S, mundo por mundo:**

| mundo | diferencia [95 %] |
|---|---|
| abundancia | +0,00 |
| normal | +0,05 [+0,00, +0,12] |
| sequía | +0,12 [−0,07, +0,33] |
| sequía dura | +0,50 [+0,15, +0,85] |
| bestias que crían | +0,28 [−0,17, +0,75] |
| los cinco | +0,19 [+0,07, +0,32] |

Solo la sequía dura y los cinco juntos quedan fuera del cero.

- **Programa:** `tres_maneras_171.py`.
- **Veredicto:**
  - «La del motor queda por encima con todas las varas, en los cinco mundos» (frente a P) **se sostiene** con las cuatro medidas de la figura: ninguna de las 20 casillas cruza. **Hay que matizarla** si «todas las varas» incluye cuántas viven: frente a P, la supervivencia cruza el cero en los cinco mundos y también con los cinco juntos.
  - «En los mundos fáciles va por delante la que suma» (en el total) **se sostiene tal cual.** En la abundancia y en el normal, la diferencia es negativa y su intervalo no toca el cero.
  - Con los cinco juntos, el total cruza (−0,002), como dijo el 167.
  - Frente a S, el balance más bajo cruza en los dos mundos fáciles, y la felicidad cruza en el normal.

---

## Lista final

**Frases que se sostienen tal cual:**
- «Contamos como noche al raso la que pasa dormida fuera de su casa más de la mitad del tiempo, también si es en casa de otra» (B1).
- «En la criatura completa, que lleva la reserva y la voz, las noches al raso pasan de una de cada cuatro a una de cada catorce» (B2): 23,2 % → 7,0 %, mismo sellado.
- «Llama tres cuartos más» (B3): +75 %.
- «No vemos que muera más» (B4): +1,5 puntos [−2,1, +5,6].
- «A la bestia se la echa entre dos» (B6): 304 de 304.
- «En los mundos fáciles va por delante la que suma» (B8).

**Frases que hay que matizar:**
- «Una de cada veinte» (la gemela, B1): con las noches en casa de otra, es una de cada 18 en el v5 y una de cada 17 en el v6. Si se quitaran esas noches, el «catorce» de la criatura completa pasaría a «quince».
- «Lo demás no afloja» (B3): las llamadas sí aflojan, de +75 % a +40 % (−13 llamadas al día, con un margen que no toca el cero), aunque siguen muy por encima. Hay que nombrarlas aparte.
- La lectura de B5, «cuanto más hambre hay, más de lo que da va a donde hace falta». Los números (6, 28, 42, la mitad) cuadran, pero siguen sobre todo a cuántas flacas tenía pegadas. Dar a la flaca entre varias añade solo de 2 a 7 puntos, y nada que se distinga de cero en la abundancia. En las bestias que crían es el 50,2 %.
- «La del motor queda por encima con todas las varas, en los cinco mundos» (frente a P, B8): vale para empujones, felicidad, total y balance más bajo, pero no para cuántas viven, que cruza en los cinco mundos.
- Si el texto da a entender que la reserva baja las noches al raso (B2): no las baja (24,2 % frente a 23,2 %); la bajada es toda de la voz.

**Frases falsas:**
- «De las treinta y una cosas, **nueve** están escritas y nada en ella las lee» (B7): son **ocho**, y otras dos solo a medias.

**Otras cifras que no cuadran con los registros** (apuntadas, sin arreglar nada):
- `informe_prompt_164.md`, tabla de la sección 5: «303 (de 304)» y «291 (de 292)» con dos o más empujando. Según el propio mundo son 304 de 304 y 292 de 292. El contador se salta a las que mueren en el mismo turno (B6). Si el paper o un apéndice dicen «303 de 304», hay que cambiarlo.
- Lo que ya dijo el 170 sigue en pie: los números de la sección 5 «unos treinta turnos, su gemela cinco» son del v5; en el v6 salen 31,97 y 4,78.

## Gasto, procesos y commit

- **Gasto:**
  - créditos de la plataforma: 0 (no se ha jugado ninguna partida);
  - dólares de la consola de Anthropic: 0 (no se ha llamado a ningún modelo).
- **Procesos:** al acabar, ningún proceso vivo ni ninguna shell en segundo plano.
- **Commit:** local, sin push.
