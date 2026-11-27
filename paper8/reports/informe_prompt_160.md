# Prompt 160: comprobar, la bestia, el huerto, los días sin fruto y lo que siente la criatura

*Informe del prompt 160 (20-nov-2026). Solo lee y cuenta: no se ha jugado ninguna partida, no se ha tocado nada sellado y no se ha usado la clave.*

- **De dónde salen los números.** Salvo que se diga otra cosa, «config» es `valle/config_valle.json`, «mundo» es `valle/mundo.py` y los demás ficheros están en `cantera/paper8/`.
- **Es lo que se jugó.** En el prompt 159 se comprobó que las huellas de la config, `mundo.py`, `cuerpo_valle.py` y `model.py` de los `fin.json` coinciden con los ficheros de hoy.

## Parte 1: las afirmaciones, una por una

Todas las he comprobado yo, leyendo `mundo.py` entero, la config y los lanzadores, sin ayudantes. Tres cosas además las he mirado en los registros de las partidas:
- los matorrales de la primera foto (21 y 5);
- el cuidado del huerto en cada cosecha;
- los días de cosecha.

Esas cuentas las hace el programa `bestia_huerto_160.py` (parte 2).

| | afirmación | veredicto |
|---|---|---|
| 1 | El mundo no da ninguna recompensa ni puntos | **cierto** |
| 2 | 48 × 48; 4 casas, 4 huertos con 16 plantas, 21 matorrales en el bosque y 5 en la zona salvaje | **cierto con matiz** |
| 3 | Los matorrales salvajes dan el doble | **cierto** |
| 4 | 400 turnos al día, 40 días; se ven 5 casillas de día y 2 de noche | **cierto con matiz** |
| 5 | El frío solo sube el hambre; una noche fuera suma unas 11,6; dentro de casa no hay frío | **cierto con matiz** |
| 6 | 2,86 comidas al día; sin comer, el tope en un día; con el hambre al tope, la vida se va en 200 turnos | **cierto con matiz** |
| 7 | Agotada, se duerme sola | **cierto** |
| 8 | La vida sube durmiendo solo con hambre de 50 o menos; la medicina cura heridas, no alimenta y solo aparece en la zona salvaje | **cierto con matiz** |
| 9 | Cada planta da fruto cada dos días, 1 sin cuidar y hasta 4 bien cuidada | **cierto con matiz** |
| 10 | Sin cuidar el huerto hay 23,5 comidas al día para 22,9 | **cierto con matiz** |
| 11 | Bolsa 6 huecos y 800 turnos; despensa 4 y 1.600; almacén sin límite, sin pudrirse, con 48 al empezar | **cierto con matiz** |
| 12 | En un empujón quien pierde suelta toda la bolsa; gana el bando con más hermanas al lado, y si empatan, la menos cansada | **cierto con matiz** |
| 13 | Un golpe entre criaturas quita 15 de vida | **cierto** |
| 14 | Solo llama «la bestia» o «aquí hay comida» si lo ve; las llamadas llegan hasta 10 casillas | **cierto con matiz** |
| 15 | La bestia baja de noche con 0,5; come hasta 4 frutos; roba la bolsa entera; golpea 40; con dos empujando se la echa 400 turnos, más con más | **cierto con matiz** |
| 16 | Los factores de los cinco mundos y los días de escasez, como en la ficha | **cierto** |
| 17 | El tonto y el recolector tienen las mismas acciones que las criaturas | **cierto con matiz** |
| 18 | Quién entra en cada casa y quién usa cada despensa | **en cualquier casa entra cualquiera; cada despensa, solo las dos de su casa y desde dentro** |
| 19 | De quién son los huertos | **de todas: ninguna regla los liga a una casa** |

**(1) Recompensa: cierto.**
- El mundo devuelve siempre recompensa 0 a cada criatura viva (mundo:720, y se devuelve en mundo:740).
- La cabecera lo dice: «no da puntos (recompensas siempre 0)» (mundo:3).
- En lo que el mundo da a cada jugador no hay ningún número de puntos: la observación (mundo:1147-1162) y la información (mundo:722).
- La felicidad que se mide en los informes la calcula cada criatura por dentro. Es su estado, no algo que dé el mundo.

**(2) Mapa: cierto con matiz.**
- **El tamaño:** 48 × 48 (config:4-5).
- **Las casas:** cuatro, de 3 × 3: A, B, C y D (config:30-72; mundo:104-108).
- **Los huertos:** cuatro, NO, NE, SE y SO, con 4 plantas cada uno: 16 en total (config:85-438).
- **Los matorrales: el matiz.** La config dice 24 en el bosque y 6 en la zona salvaje (config:802 y 807), pero esos números no se usan. Con el margen de comida encendido, el número lo calcula el mundo (mundo:272-276):
  - lo que falta: 22,86 × 1,05 − 8 = 16 comidas al día;
  - en el bosque: 16 × 2/3 / 0,5 = 21,3, que redondeado da 21;
  - en la zona salvaje: 16 / 3 / 1 = 5,3, que da 5.
- La primera foto de los objetos de dos partidas (normal, semilla 30170, tonto y RG69r+voz) tiene 21 matorrales en el bosque y 5 en la zona salvaje. El número no depende de la semilla, porque sale de la config; la semilla solo elige las casillas (mundo:216).

**(3) El doble: cierto.**
- Uno del bosque da 1 fruto cada 800 turnos; uno salvaje, 2 cada 800 (config:800-801 y 805-806; mundo:1094).
- Las épocas multiplican a los dos igual (mundo:1095).
- Un 10 % de los frutos de cualquiera de los dos cae como baya en una casilla del bosque (mundo:1099-1101). La comida sigue siendo la misma, pero no queda en el matorral.

**(4) Tiempo y vista: cierto con matiz.**
- **El día:** 400 turnos (config:537).
- **La partida, con matiz:** la config dice 20 días (config:557). Los 40 los pone el lanzador al crear el mundo:
  - en las criaturas, `banco_cuerpo_valle.py:25`, con `dias=40` (`lanza_experimento_v6.py:38`);
  - en el tonto y el recolector, `valle/banco_base_v5.py:14`.
- **La vista, con matiz:** 5 casillas por la mañana y por la tarde, 2 de noche, y también **3 al anochecer**, que la frase no dice (config:601-605; mundo:491-494). Son casillas a cada lado: de día ve un cuadrado de 11 × 11 (mundo:1121-1122).

**(5) El frío: cierto con matiz.**
- **En el mundo, solo sube el hambre.** Fuera de una casa, por debajo de 15°, el hambre del turno se multiplica por 1 + 0,05 por cada grado de menos (mundo:682-684; config:840-845).
  - La temperatura solo se usa ahí y en lo que se ve (mundo:683, 732 y 1160).
  - La config lo dice: el mundo no quita vida por eso, «el malestar lo pone cada jugador» (config:844).
- **Una noche entera fuera:** la cuenta del propio mundo (mundo:153-163) da 11,63 de hambre de más:
  - el anochecer, despierta: 40 × 0,25 × 0,05 × 3 = 1,5;
  - la noche, dormida: 120 × 0,25 × 0,75 × 0,05 × 9 = 10,1.
- **Primer matiz:** las 11,6 suponen el anochecer despierta y la noche dormida. Despierta toda la noche serían 1,5 + 13,5 = 15.
- **Dentro de casa no hay frío:** dentro de cualquier casa hace siempre 20° (mundo:483; config:839).
- **Segundo matiz:** vale también para una casa ajena.
- **Tercer matiz:** la criatura sí siente el frío, como una pérdida en el cuerpo, la fila F-FRIO (`cuerpo_valle.py:2201-2204`; parte 5). Eso es suyo, no del mundo.

**(6) Lo que necesita: cierto con matiz.**
- **De base:** 0,25 × 400 / 35 = 2,857 comidas al día (config:563, 537 y 650; la fórmula, mundo:248). Para las ocho son 22,86.
- **Sin comer:** de 0 a 100, con solo la base, son 400 turnos, un día. Matices:
  - **el tope:** el hambre se queda en 100 (mundo:686);
  - **el reloj del hambre:** dormida va ×0,75 y despierta por la tarde ×1,3 (config:630-634; mundo:679-680);
  - **el resto:** andar, trabajar y el frío suben el hambre más deprisa;
  - **desde abajo:** el hambre puede empezar en −20 (config:642-645), y entonces tarda más.
- **Con el hambre al tope:** pierde 0,5 de vida por turno (config:565; mundo:687). De 100 a 0 son 200 turnos.
  - **Matiz:** eso es si empieza con la vida entera. Con el hambre por encima de 50, dormir no la sube (mundo:770).

**(7) Agotada: cierto.**
- Con el cansancio en 100 queda agotada (mundo:692). Pida lo que pida, su acción se cambia por dormir (mundo:641; config:589).
- Dormir siempre le está permitido (mundo:542).
- Lo sigue estando hasta bajar a 70 (mundo:693; config:570).
- Agotada no puede moverse, coger ni trabajar (mundo:748, 774 y 833; acciones posibles, mundo:575 y 599).

**(8) Vida y medicina: cierto con matiz.**
- **Durmiendo,** sube 0,25 por turno solo si el hambre es de 50 o menos (mundo:770-771; config:582 y 586).
- **El matiz:** también sube al tomar medicina. La medicina sube la vida tanto como cura de herida, hasta 40 (mundo:814; config:667).
  - «Herida» es solo el daño de golpes, bestia y terreno. El daño del hambre no cuenta como herida (mundo:687, `herida=False`), así que la medicina no lo cura.
- **La medicina no alimenta:** nutrición 0 (config:666). Se puede tomar estando harta (mundo:489).
- **Solo aparece en la zona salvaje:** 2 al día (config:681; mundo:432-435 y 1104-1115).
  - El bosque solo tiene apariciones de comida (config:676-678), y con matorrales esas se ponen a 0 (mundo:258-259).
  - Ni el almacén del principio (config:683-684) ni la bestia muerta (mundo:332-335) dan medicina.

**(9) Fruto de cada planta: cierto con matiz.**
- **Cada cuánto:** cada 800 turnos, dos días (config:688; mundo:1079).
- **Cuánto:** 1 + (4 − 1) × cuidado (config:690; mundo:1071). Es 1 con cuidado 0 y 4 con cuidado 1; el cuidado no pasa de 1 (mundo:838).
- **Primer matiz:** se multiplica por el factor de la época (mundo:1072). En la abundancia una planta bien cuidada da 5,2 de media, y en la escasez de la sequía dura, 1,96.
- **Segundo matiz:** la parte decimal se sortea (mundo:1073).
- **Tercer matiz:** cuenta el cuidado de ese momento, que baja a la mitad cada 1.600 turnos sin trabajo (config:699; mundo:1069).
- En las 1.600 partidas, todas las cosechas caen en los días 1, 3, …, 39.

**(10) La comida sin cuidar: cierto con matiz.**
- La cuenta del mundo, sin cuidar, da exactamente 23,5 (mundo:279-281):
  - el huerto: 16 plantas × 1 / 2 días = 8;
  - los matorrales: 21 × 0,5 + 5 × 1 = 15,5.
- Frente a 22,86 de base para las ocho (mundo:274), el margen de verdad es del 2,8 % y no del 5 %, por el redondeo de los matorrales. El propio mundo lo guarda como `margen_efectivo`.
- **Matices:**
  - **las épocas:** solo vale en los mundos sin ellas; en las otras épocas, lo de cada día se multiplica por el factor;
  - **lo que la cuenta deja fuera:** el árbol dulce (unos 2,6 al día en las partidas), las 48 comidas del almacén del principio y lo que necesitan de más los pasos, el trabajo y el frío;
  - **el huerto nunca está sin cuidar al empezar:** empieza con cuidado 1 (mundo:209-210).

**(11) Dónde se guarda: cierto con matiz.**
- **La bolsa:** 6 huecos (config:575; mundo:549), y la comida se pudre a los 800 turnos (config:655).
- **La despensa:** 4 huecos (config:713; mundo:590 y 802), y se pudre a los 1.600 (config:656).
- **El almacén:**
  - no tiene límite, porque dejar en él no mira ningún tope (mundo:799-800);
  - no se pudre (config:657, `null`; mundo:1042);
  - empieza con 48 comidas (config:684; mundo:219-220).
- **El matiz:** lo podrido se acumula de un sitio a otro (mundo:1042-1043).
  - Una comida que lleva 400 turnos en la bolsa ya tiene la mitad podrida: en la despensa le quedan 800 turnos, no 1.600.
  - La medicina no se pudre en ningún sitio (config:668).

**(12) El empujón: cierto con matiz.**
- **Quien pierde suelta toda la bolsa:** pasa a la ganadora hasta llenarle la bolsa, y lo que no cabe cae al suelo, en la casilla de la que pierde (mundo:902-905).
- **Matiz en «al lado»:** el bando es ella más las de su misma casa vivas que estén al lado de cualquiera de las dos casillas de la escena, la de quien empuja o la de quien recibe (mundo:890-891).
  - Con dos por casa, cada bando es 1 o 2.
  - Si se empujan dos hermanas, ninguna tiene a otra de su casa que contar, y empatan.
- **El empate:** gana la menos cansada, contando los +5 que suma el empujón a las dos (mundo:894-898). Si también empatan en eso, no pasa nada (mundo:900).

**(13) El golpe: cierto.**
- La golpeada pierde 15 de vida, que cuentan también como herida (config:576; mundo:855 y 608).
- Quien golpea paga 3 de cansancio (config:577; mundo:854).

**(14) Las llamadas: cierto con matiz.**
- **«La bestia»** solo se puede dar si la bestia está en lo que ve ese turno (`cuerpo_valle.py:1250`).
  - Lo que cree de la bestia sale solo de la observación del turno (`cuerpo_valle.py:724-727`).
  - Dormida, no la ve (mundo:1143; config:744).
- **«Aquí hay comida»** solo si ve comida en una casilla: en el suelo, en un matorral o en una planta (`cuerpo_valle.py:1243` y `1251`).
  - No cuenta el almacén, ni lo que lleva otra.
- **Hasta dónde llegan:**
  - suave, 4 casillas; medio, 7; fuerte, 10 (config:874-878; mundo:659-661);
  - las casillas se cuentan contando también las diagonales (mundo:869).
- **El matiz:** «hasta 10» es con la fuerte.
  - Además, solo llama si hay a quién: a la hermana o a otras que vio hace poco, a más de 1 casilla y dentro del alcance (`cuerpo_valle.py:1241-1247`).
  - En estas criaturas, dormida no puede llamar (mundo:657, encendido por `banco_cuerpo_valle.py:35`).

**(15) La bestia: cierto con matiz.**
- **Baja de noche:** con probabilidad 0,5, el mando «medio» (config:725 y 731-734). Lo decide al empezar la noche, el turno 280 del día, y solo si está de ronda (mundo:961-963). Si está echada o muerta, no actúa.
- **Come del huerto:** hasta 4 frutos de las plantas por bajada (config:741; mundo:986-994).
  - **Matiz:** el contador vuelve a 0 en cada bajada (mundo:972 y 981). En «bestias que crían» también baja de día, así que pueden ser hasta 8 al día.
- **Roba la bolsa entera:** a la criatura que tiene al lado y que no está en una casa (mundo:1019-1028).
  - **Matiz:** de ronda solo mira a las del anillo salvaje (mundo:1020).
  - **Matiz:** junto al árbol dulce solo le quita la fruta dulce, si lleva (mundo:1025-1027).
- **Golpea 40** (config:721; mundo:919):
  - a quien no lleva nada;
  - a la dormida a la que roba;
  - a quien la golpea;
  - a quien pierde un empujón contra ella (mundo:1032-1033, 851 y 886).
- **Echarla:**
  - Con 2 empujando el mismo turno, se va 400 turnos; con n, 400 × (n/2)^1,5: unos 735 con 3 y 1.131 con 4 (config:759; mundo:339-346).
  - **Matiz:** eso es echarla. Ganarle un empujón (recuperar lo robado) pide otra cosa: 2 o más criaturas al lado de ella, empujen o no (mundo:878-880).

**(16) Los cinco mundos: cierto.**
- Como en la ficha, apartado 10.
  - **Las épocas:** de 5 días, en el orden abundancia, normal, escasez, normal, también en el huerto (`pasada_v18.py:9`; `pasada_v22.py:9-11`; config:891-910).
  - **Cómo se arma cada mundo:** `lanzador.py:33-41`.
  - **El día de cada época:** el número de época es (día // 5) % 4 (mundo:472).
- **Los factores:**
  - abundancia, 1,3 siempre;
  - normal, sin épocas;
  - sequía, 1,3 / 1,0 / 0,7 / 1,0;
  - sequía dura, esos × 0,7 = 0,91 / 0,7 / 0,49 / 0,7 (mundo:254-257);
  - bestias que crían, sin épocas, con la bestia de día (probabilidad 1,0) y una cría cada 20 días, hasta 2 (config:748-750 y 890).
- **La escasez:** cae en los días 10-14 y 30-34 contados desde 0, es decir, **11-15 y 31-35** contados del 1 al 40.

**(17) Las mismas acciones: cierto con matiz.**
- Juegan en el mismo mundo y con la misma lista de acciones posibles (mundo:571-601; `lanzador.py:85`; `valle/banco_base_v5.py:14-16` y 35).
- **Lo que usan:** de hecho, solo mover, quedarse, coger, dejar, comer, dormir y trabajar. El recolector no trabaja nunca. No dan, no empujan, no golpean, no llaman (`valle/jugadores.py:1-4`).
- **Las diferencias:**
  - **la voz de ir a casa** no es una acción del mundo y solo la tienen las tres «+voz» (ficha, apartado 5);
  - **la llamada estando dormida:** a las criaturas, el lanzador les quita la de estando dormida (`banco_cuerpo_valle.py:35`). Al tonto y al recolector no, pero no llaman nunca;
  - **lo que ven de más:** las criaturas ven lo que hizo su cuerpo y los empujones a la vista (`banco_cuerpo_valle.py:30-31`). Eso es lo que ven, no lo que pueden hacer.

**(18) Casas y despensas.**
- **En cualquier casa entra cualquiera.**
  - La única regla para entrar o salir de una casa es pasar por su puerta (mundo:455-458). No mira de qué casa es quien pasa.
  - En cualquier casa se está a 20° (mundo:483), y la bestia no encuentra a nadie que esté en una casa, sea la suya o no (mundo:1019).
- **Cada despensa, solo las dos de su casa, y desde dentro de su casa:** coger y dejar piden `en_casa_propia` (mundo:463, 585-586, 590, 791 y 802).
  - Lo que hay en ella solo lo ve quien está dentro de su propia casa (mundo:1154).
  - La de otra casa no se puede ni ver ni tocar, aunque se esté dentro.
- **«En casa»,** en lo que ve de sí misma, es estar en la suya (mundo:1149).

**(19) Los huertos: de todas.**
- **En el código:** cada planta solo sabe de qué huerto es, y cada huerto tiene un rendimiento, 1,0 en los cuatro (mundo:98-102; config:106, 194, 282 y 370).
  - Trabajar o coger mira solo si hay una planta al lado, sin mirar de qué casa es quien lo hace (mundo:465-467, 581, 599, 783-784 y 830-838).
  - No hay ninguna regla del mundo que ligue un huerto a una casa.
- **En la config:** lo dice con esa palabra: «cuatro huertos comunes» (config:439).
- **Lo único que los acerca:** cada huerto está en una esquina, fuera de la plaza, y queda más cerca de la casa de esa esquina (config:476).


Análisis hecho después de ver los datos, no predicción. No se proponen causas. Partidas del v6 (seis jugadores) y de la escalera (S69+voz y P69+voz), cinco mundos, semillas 30161-30200, 40 días. Medias por partida (40 por jugador y mundo).

## Partes 2 a 4: comprobaciones del programa

- El cuidado rehecho turno a turno coincide con el que apunta el mundo en cada cosecha: diferencia máxima 0.0000 (el mundo lo redondea a 3 decimales) en las 1600 partidas.
- Las veces que echan y matan a la bestia, contadas en los sucesos, cuadran con `pieza_g.json` en todas las partidas: sí.
- Los matorrales rehechos con las fotos, en los mundos sin épocas (normal y bestias que crían, partidas enteras): entre 619 y 641 frutos por partida; la regla del mundo da exactamente 620 (26 matorrales × 20 veces). Lo que falta son cosechas de los últimos turnos sin foto detrás o cogidas que no se pueden atribuir.
- Partidas en que mueren todas antes del final (el registro del mundo se acaba ahí): 6, de tonto · bestias que crían, tonto · sequía dura. Sus cuentas son de los turnos registrados.
- Cosechas del huerto en días 2, 4, …, 40: 0 en las 1600 partidas (todas caen en los días 1, 3, …, 39).

## Parte 2: la bestia (v6)

Por partida, media de las 40 semillas. «Echada con 2 · 3 · 4+»: veces que la echan según cuántas empujan a la vez. «Empujones a la bestia»: empujones cumplidos (gane o pierda). «Golpes recibidos»: golpes de la bestia a criaturas, y entre paréntesis los que fueron porque no llevaba nada · dormida · al devolver un golpe · al perder un empujón.

| mundo | jugador | echada (total) | echada con 2 · 3 · 4+ | la matan | empujones a la bestia | golpes dados a la bestia | golpes recibidos de ella (sin nada · dormida · devuelve · se resiste) |
|---|---|---|---|---|---|---|---|
| abundancia | tonto | 0.00 | 0.00 · 0.00 · 0.00 | 0.00 | 0.00 | 0.00 | 0.03 (0.00 · 0.03 · 0.00 · 0.00) |
| abundancia | recolector | 0.00 | 0.00 · 0.00 · 0.00 | 0.00 | 0.00 | 0.00 | 1.15 (0.82 · 0.33 · 0.00 · 0.00) |
| abundancia | RG68r | 0.12 | 0.12 · 0.00 · 0.00 | 0.00 | 0.70 | 0.00 | 4.33 (0.20 · 3.90 · 0.00 · 0.23) |
| abundancia | RG068r | 0.03 | 0.03 · 0.00 · 0.00 | 0.00 | 0.10 | 0.00 | 1.05 (0.25 · 0.78 · 0.00 · 0.03) |
| abundancia | RG69r | 0.15 | 0.15 · 0.00 · 0.00 | 0.00 | 1.00 | 0.00 | 4.83 (0.35 · 4.22 · 0.00 · 0.25) |
| abundancia | RG69r+voz | 0.07 | 0.07 · 0.00 · 0.00 | 0.00 | 0.35 | 0.00 | 0.62 (0.20 · 0.40 · 0.00 · 0.03) |
| normal | tonto | 0.00 | 0.00 · 0.00 · 0.00 | 0.00 | 0.00 | 0.00 | 0.00 (0.00 · 0.00 · 0.00 · 0.00) |
| normal | recolector | 0.00 | 0.00 · 0.00 · 0.00 | 0.00 | 0.00 | 0.00 | 1.65 (1.32 · 0.33 · 0.00 · 0.00) |
| normal | RG68r | 0.23 | 0.23 · 0.00 · 0.00 | 0.00 | 1.07 | 0.00 | 3.80 (0.47 · 3.02 · 0.00 · 0.30) |
| normal | RG068r | 0.12 | 0.12 · 0.00 · 0.00 | 0.00 | 0.28 | 0.00 | 2.20 (1.27 · 0.90 · 0.00 · 0.03) |
| normal | RG69r | 0.15 | 0.15 · 0.00 · 0.00 | 0.00 | 0.72 | 0.00 | 4.25 (0.62 · 3.38 · 0.00 · 0.25) |
| normal | RG69r+voz | 0.03 | 0.03 · 0.00 · 0.00 | 0.00 | 0.23 | 0.00 | 1.38 (0.50 · 0.80 · 0.00 · 0.07) |
| sequía | tonto | 0.00 | 0.00 · 0.00 · 0.00 | 0.00 | 0.00 | 0.00 | 0.07 (0.03 · 0.05 · 0.00 · 0.00) |
| sequía | recolector | 0.00 | 0.00 · 0.00 · 0.00 | 0.00 | 0.00 | 0.00 | 1.88 (1.40 · 0.47 · 0.00 · 0.00) |
| sequía | RG68r | 0.17 | 0.17 · 0.00 · 0.00 | 0.00 | 0.97 | 0.00 | 3.75 (0.50 · 2.88 · 0.00 · 0.38) |
| sequía | RG068r | 0.03 | 0.03 · 0.00 · 0.00 | 0.00 | 0.25 | 0.00 | 2.27 (1.40 · 0.82 · 0.00 · 0.05) |
| sequía | RG69r | 0.28 | 0.28 · 0.00 · 0.00 | 0.00 | 1.20 | 0.00 | 4.55 (1.02 · 3.10 · 0.00 · 0.42) |
| sequía | RG69r+voz | 0.10 | 0.10 · 0.00 · 0.00 | 0.00 | 0.55 | 0.00 | 2.50 (1.15 · 1.07 · 0.00 · 0.28) |
| sequía dura | tonto | 0.00 | 0.00 · 0.00 · 0.00 | 0.00 | 0.00 | 0.00 | 0.03 (0.03 · 0.00 · 0.00 · 0.00) |
| sequía dura | recolector | 0.00 | 0.00 · 0.00 · 0.00 | 0.00 | 0.00 | 0.00 | 0.90 (0.65 · 0.25 · 0.00 · 0.00) |
| sequía dura | RG68r | 0.12 | 0.12 · 0.00 · 0.00 | 0.00 | 0.88 | 0.00 | 3.50 (1.30 · 1.95 · 0.00 · 0.25) |
| sequía dura | RG068r | 0.03 | 0.03 · 0.00 · 0.00 | 0.00 | 0.23 | 0.00 | 2.98 (2.05 · 0.90 · 0.00 · 0.03) |
| sequía dura | RG69r | 0.17 | 0.17 · 0.00 · 0.00 | 0.00 | 1.07 | 0.05 | 4.33 (1.80 · 2.02 · 0.05 · 0.45) |
| sequía dura | RG69r+voz | 0.10 | 0.10 · 0.00 · 0.00 | 0.00 | 0.72 | 0.05 | 3.02 (1.55 · 1.15 · 0.05 · 0.28) |
| bestias que crían | tonto | 0.00 | 0.00 · 0.00 · 0.00 | 0.00 | 0.00 | 0.00 | 6.50 (6.50 · 0.00 · 0.00 · 0.00) |
| bestias que crían | recolector | 0.00 | 0.00 · 0.00 · 0.00 | 0.00 | 0.00 | 0.00 | 16.55 (16.27 · 0.28 · 0.00 · 0.00) |
| bestias que crían | RG68r | 5.08 | 4.92 · 0.15 · 0.00 | 0.00 | 18.00 | 0.10 | 21.12 (13.88 · 3.27 · 0.10 · 3.88) |
| bestias que crían | RG068r | 1.43 | 1.38 · 0.05 · 0.00 | 0.00 | 7.12 | 0.00 | 28.23 (25.15 · 1.43 · 0.00 · 1.65) |
| bestias que crían | RG69r | 6.22 | 6.10 · 0.12 · 0.00 | 0.00 | 20.70 | 0.38 | 28.48 (20.50 · 3.40 · 0.38 · 4.20) |
| bestias que crían | RG69r+voz | 7.30 | 7.15 · 0.12 · 0.03 | 0.00 | 22.02 | 0.15 | 27.18 (22.27 · 1.43 · 0.15 · 3.33) |

## Parte 3: el huerto

Por partida, media de las 40 semillas. «Cuidado» de 0 a 1, media de las 16 plantas y de los turnos de cada tramo. «Huerto, frutos al día»: lo que dio, y entre paréntesis lo que habrían dado las mismas cosechas sin cuidar (1 fruto por planta × factor de la época) y bien cuidadas (4 × factor).

| mundo | jugador | turnos de trabajo | cuidado días 1-10 · 11-20 · 21-30 · 31-40 | huerto, frutos al día (sin cuidar · bien cuidado) |
|---|---|---|---|---|
| abundancia | tonto | 3538 | 0.73 · 0.69 · 0.69 · 0.68 | 32.8 (10.4 · 41.6) |
| abundancia | recolector | 0 | 0.47 · 0.08 · 0.01 · 0.00 | 15.3 (10.4 · 41.6) |
| abundancia | RG68r | 6387 | 0.85 · 0.84 · 0.84 · 0.84 | 34.3 (10.4 · 41.6) |
| abundancia | RG068r | 6459 | 0.86 · 0.85 · 0.85 · 0.85 | 34.1 (10.4 · 41.6) |
| abundancia | RG69r | 6384 | 0.85 · 0.84 · 0.84 · 0.84 | 34.3 (10.4 · 41.6) |
| abundancia | RG69r+voz | 6432 | 0.86 · 0.85 · 0.84 · 0.85 | 34.3 (10.4 · 41.6) |
| abundancia | S69+voz | 6264 | 0.84 · 0.84 · 0.84 · 0.84 | 34.7 (10.4 · 41.6) |
| abundancia | P69+voz | 6393 | 0.85 · 0.84 · 0.84 · 0.85 | 34.3 (10.4 · 41.6) |
| normal | tonto | 5537 | 0.80 · 0.82 · 0.82 · 0.82 | 27.3 (8.0 · 32.0) |
| normal | recolector | 0 | 0.47 · 0.08 · 0.01 · 0.00 | 11.7 (8.0 · 32.0) |
| normal | RG68r | 6384 | 0.85 · 0.84 · 0.84 · 0.84 | 26.4 (8.0 · 32.0) |
| normal | RG068r | 6450 | 0.86 · 0.85 · 0.85 · 0.85 | 26.3 (8.0 · 32.0) |
| normal | RG69r | 6420 | 0.85 · 0.84 · 0.85 · 0.84 | 26.3 (8.0 · 32.0) |
| normal | RG69r+voz | 6445 | 0.86 · 0.85 · 0.85 · 0.85 | 26.4 (8.0 · 32.0) |
| normal | S69+voz | 6348 | 0.85 · 0.84 · 0.84 · 0.85 | 26.6 (8.0 · 32.0) |
| normal | P69+voz | 6421 | 0.86 · 0.85 · 0.85 · 0.85 | 26.4 (8.0 · 32.0) |
| sequía | tonto | 4262 | 0.75 · 0.83 · 0.58 · 0.69 | 24.8 (8.0 · 32.0) |
| sequía | recolector | 0 | 0.47 · 0.08 · 0.01 · 0.00 | 12.3 (8.0 · 32.0) |
| sequía | RG68r | 6354 | 0.85 · 0.84 · 0.84 · 0.84 | 26.5 (8.0 · 32.0) |
| sequía | RG068r | 6454 | 0.86 · 0.85 · 0.85 · 0.85 | 26.3 (8.0 · 32.0) |
| sequía | RG69r | 6395 | 0.85 · 0.84 · 0.84 · 0.84 | 26.5 (8.0 · 32.0) |
| sequía | RG69r+voz | 6432 | 0.86 · 0.85 · 0.85 · 0.85 | 26.4 (8.0 · 32.0) |
| sequía | S69+voz | 6293 | 0.84 · 0.84 · 0.84 · 0.84 | 26.7 (8.0 · 32.0) |
| sequía | P69+voz | 6373 | 0.85 · 0.85 · 0.84 · 0.85 | 26.4 (8.0 · 32.0) |
| sequía dura | tonto | 2966 | 0.83 · 0.67 · 0.34 · 0.32 | 14.9 (5.6 · 22.6) |
| sequía dura | recolector | 0 | 0.47 · 0.08 · 0.01 · 0.00 | 8.7 (5.6 · 22.4) |
| sequía dura | RG68r | 5565 | 0.85 · 0.82 · 0.77 · 0.77 | 18.4 (5.6 · 22.4) |
| sequía dura | RG068r | 5588 | 0.86 · 0.82 · 0.76 · 0.76 | 18.2 (5.6 · 22.4) |
| sequía dura | RG69r | 5570 | 0.85 · 0.82 · 0.76 · 0.77 | 18.2 (5.6 · 22.4) |
| sequía dura | RG69r+voz | 5782 | 0.86 · 0.82 · 0.80 · 0.79 | 18.5 (5.6 · 22.4) |
| sequía dura | S69+voz | 5376 | 0.85 · 0.81 · 0.75 · 0.74 | 18.2 (5.6 · 22.4) |
| sequía dura | P69+voz | 5668 | 0.86 · 0.82 · 0.78 · 0.78 | 18.4 (5.6 · 22.4) |
| bestias que crían | tonto | 4936 | 0.84 · 0.81 · 0.70 · 0.60 | 24.7 (8.0 · 32.1) |
| bestias que crían | recolector | 0 | 0.47 · 0.08 · 0.01 · 0.00 | 11.7 (8.0 · 32.0) |
| bestias que crían | RG68r | 6302 | 0.85 · 0.84 · 0.84 · 0.84 | 26.4 (8.0 · 32.0) |
| bestias que crían | RG068r | 6400 | 0.86 · 0.85 · 0.85 · 0.84 | 26.4 (8.0 · 32.0) |
| bestias que crían | RG69r | 6325 | 0.85 · 0.84 · 0.84 · 0.84 | 26.4 (8.0 · 32.0) |
| bestias que crían | RG69r+voz | 6395 | 0.86 · 0.85 · 0.85 · 0.84 | 26.4 (8.0 · 32.0) |
| bestias que crían | S69+voz | 6246 | 0.85 · 0.84 · 0.84 · 0.84 | 26.7 (8.0 · 32.0) |
| bestias que crían | P69+voz | 6380 | 0.86 · 0.85 · 0.85 · 0.84 | 26.4 (8.0 · 32.0) |

### La comida que produce el valle y lo que necesitan las vivas

Comidas al día, media por partida. Matorrales: lo que dan, con las bayas que caen al suelo. Necesitan: la base del mundo, 2.86 comidas al día por cada viva (sin pasos, trabajo ni frío). No cuenta las 48 comidas del almacén del principio ni las 24 que deja una bestia muerta.

| mundo | jugador | huerto | matorrales | árbol dulce | total | necesitan las vivas | total − necesitan |
|---|---|---|---|---|---|---|---|
| abundancia | tonto | 32.8 | 20.1 | 2.6 | 55.6 | 22.9 | +32.7 |
| abundancia | recolector | 15.3 | 20.2 | 2.6 | 38.1 | 22.8 | +15.3 |
| abundancia | RG68r | 34.3 | 20.2 | 2.6 | 57.1 | 22.9 | +34.3 |
| abundancia | RG068r | 34.1 | 20.2 | 2.6 | 56.9 | 22.8 | +34.1 |
| abundancia | RG69r | 34.3 | 20.2 | 2.6 | 57.1 | 22.8 | +34.3 |
| abundancia | RG69r+voz | 34.3 | 20.2 | 2.6 | 57.1 | 22.9 | +34.2 |
| abundancia | S69+voz | 34.7 | 20.2 | 2.6 | 57.5 | 22.9 | +34.6 |
| abundancia | P69+voz | 34.3 | 20.2 | 2.6 | 57.1 | 22.8 | +34.3 |
| normal | tonto | 27.3 | 15.5 | 2.6 | 45.4 | 22.9 | +22.6 |
| normal | recolector | 11.7 | 15.6 | 2.6 | 29.9 | 22.8 | +7.1 |
| normal | RG68r | 26.4 | 15.6 | 2.6 | 44.5 | 22.8 | +21.8 |
| normal | RG068r | 26.3 | 15.6 | 2.6 | 44.5 | 22.5 | +22.0 |
| normal | RG69r | 26.3 | 15.6 | 2.6 | 44.5 | 22.8 | +21.7 |
| normal | RG69r+voz | 26.4 | 15.6 | 2.6 | 44.5 | 22.9 | +21.7 |
| normal | S69+voz | 26.6 | 15.5 | 2.6 | 44.8 | 22.8 | +21.9 |
| normal | P69+voz | 26.4 | 15.6 | 2.6 | 44.5 | 22.9 | +21.7 |
| sequía | tonto | 24.8 | 15.5 | 2.6 | 42.9 | 18.2 | +24.7 |
| sequía | recolector | 12.3 | 15.6 | 2.6 | 30.5 | 22.8 | +7.7 |
| sequía | RG68r | 26.5 | 15.5 | 2.6 | 44.6 | 22.1 | +22.5 |
| sequía | RG068r | 26.3 | 15.5 | 2.6 | 44.5 | 22.5 | +22.0 |
| sequía | RG69r | 26.5 | 15.6 | 2.6 | 44.6 | 22.6 | +22.1 |
| sequía | RG69r+voz | 26.4 | 15.6 | 2.6 | 44.6 | 22.6 | +22.0 |
| sequía | S69+voz | 26.7 | 15.6 | 2.6 | 44.9 | 22.5 | +22.4 |
| sequía | P69+voz | 26.4 | 15.5 | 2.6 | 44.6 | 22.3 | +22.3 |
| sequía dura | tonto | 14.9 | 10.8 | 2.6 | 28.4 | 11.0 | +17.4 |
| sequía dura | recolector | 8.7 | 10.8 | 2.6 | 22.1 | 16.0 | +6.1 |
| sequía dura | RG68r | 18.4 | 10.9 | 2.6 | 31.8 | 15.3 | +16.5 |
| sequía dura | RG068r | 18.2 | 10.9 | 2.6 | 31.7 | 16.1 | +15.6 |
| sequía dura | RG69r | 18.2 | 10.8 | 2.6 | 31.7 | 15.5 | +16.2 |
| sequía dura | RG69r+voz | 18.5 | 10.9 | 2.6 | 32.0 | 15.8 | +16.2 |
| sequía dura | S69+voz | 18.2 | 10.8 | 2.6 | 31.6 | 14.9 | +16.7 |
| sequía dura | P69+voz | 18.4 | 10.9 | 2.6 | 31.9 | 15.7 | +16.2 |
| bestias que crían | tonto | 24.7 | 15.5 | 2.7 | 42.9 | 17.1 | +25.8 |
| bestias que crían | recolector | 11.7 | 15.6 | 2.6 | 29.9 | 21.7 | +8.2 |
| bestias que crían | RG68r | 26.4 | 15.6 | 2.6 | 44.6 | 21.1 | +23.5 |
| bestias que crían | RG068r | 26.4 | 15.6 | 2.6 | 44.6 | 21.3 | +23.3 |
| bestias que crían | RG69r | 26.4 | 15.6 | 2.6 | 44.6 | 21.2 | +23.4 |
| bestias que crían | RG69r+voz | 26.4 | 15.6 | 2.6 | 44.6 | 21.6 | +23.0 |
| bestias que crían | S69+voz | 26.7 | 15.5 | 2.6 | 44.8 | 21.3 | +23.6 |
| bestias que crían | P69+voz | 26.4 | 15.6 | 2.6 | 44.6 | 21.6 | +23.0 |

### La sequía dura con el huerto cuidado al máximo todo el tiempo (cuenta con las reglas del mundo, no una partida)

Huerto: 16 plantas × 4 frutos cada 800 turnos = 32 al día × factor de la época (config:690 y 688). Matorrales: 21 del bosque × 0,5 + 5 salvajes × 1 = 15.5 al día × factor (mundo:270-276). Árbol dulce: no depende de la época; de media, 2 sitios × 2.5 apariciones × 20 frutos en 40 días = 2.5 al día (config:886; en las partidas enteras de la sequía dura salió 2.6). Necesitan las ocho: 22.9 al día de base.

| época (días) | factor | huerto al máximo | matorrales | sin el árbol | con el árbol de media | necesitan las ocho | alcanza sin el árbol |
|---|---|---|---|---|---|---|---|
| abundancia (1-5, 21-25) | 0.91 | 29.1 | 14.1 | 43.2 | 45.7 | 22.9 | sí (+20.4) |
| normal (6-10, 26-30) | 0.70 | 22.4 | 10.8 | 33.2 | 35.8 | 22.9 | sí (+10.4) |
| escasez (11-15, 31-35) | 0.49 | 15.7 | 7.6 | 23.3 | 25.8 | 22.9 | sí (+0.4) |
| normal (16-20, 36-40) | 0.70 | 22.4 | 10.8 | 33.2 | 35.8 | 22.9 | sí (+10.4) |

Lo que no entra en la cuenta: lo que se come la bestia del huerto (hasta 4 frutos por noche, config:741), lo que se pudre, lo que cuesta de más trabajar, andar y el frío, y que el huerto da fruto un día sí y otro no (la cuenta es la media de los dos días).

## Parte 4: los días sin fruto (caché del 156)

Días contados del 1 al 40. El huerto da fruto los días 1, 3, …, 39 (comprobado arriba). Por partida: felicidad de la aldea (0 a 100) media de los días 2, 4, …, 40 menos la media de los días 3, 5, …, 39 (sin el día 1). Media de las 40 semillas con su intervalo del 95 %; las diferencias, emparejadas por semilla.

| mundo | pares − impares: RG69r+voz · S69+voz · P69+voz | (pares − impares) de RG69r+voz − de S69+voz | − de P69+voz |
|---|---|---|---|
| abundancia | -0.2 [-1.0, +0.5] · +0.7 [-0.2, +1.7] · +2.4 [+1.5, +3.2] | -1.0 [-1.9, -0.0] | -2.6 [-3.4, -1.9] |
| normal | +3.7 [+2.7, +4.7] · +8.1 [+6.7, +9.5] · +8.6 [+7.6, +9.5] | -4.4 [-5.7, -3.1] | -4.9 [-5.9, -3.9] |
| sequía | +5.7 [+4.9, +6.5] · +9.6 [+8.3, +10.9] · +8.4 [+7.3, +9.5] | -3.9 [-4.9, -2.9] | -2.6 [-3.6, -1.7] |
| sequía dura | +5.0 [+4.0, +6.0] · +6.4 [+5.2, +7.6] · +6.1 [+4.9, +7.3] | -1.4 [-2.8, -0.0] | -1.1 [-2.6, +0.3] |
| bestias que crían | +8.3 [+7.1, +9.4] · +10.9 [+9.6, +12.3] · +10.0 [+8.8, +11.2] | -2.7 [-4.4, -1.0] | -1.7 [-3.0, -0.4] |

## Parte 5: lo que siente RG69r+voz

**Cómo se ha hecho:**
- Lo leyó un ayudante de solo lectura, sin ejecutar nada.
- Yo comprobé a mano unas veinte de sus citas, todas las que llevan número de peso, y todas coincidían. Son estas:
  - los interruptores, en `banco_v7.py:309-310`;
  - las filas, en `cuerpo_valle.py:1612-1642`, `1726-1742`, `2189`, `2224-2236` y `2269-2277`;
  - la comida guardada, en `cuerpo_valle.py:2302-2314`;
  - el vínculo, en `cuerpo_valle.py:762`, `1949-1952`, `2043-2061` y `2084-2087`;
  - lo que imagina hacia delante, en `cuerpo_valle.py:2470-2516`;
  - la reserva y la voz, en `cuerpo_rg69.py:18-33` y `cuerpo_vc1.py:44-60`;
  - el olvido, en `paper7/cuaderno_P7.py:23` y `59-62`;
  - los repartos, en `paintball/alma/appraisal_zs_v42_exp.py:417-440`;
  - las metas del motor, en `motor/model.py:78-80`;
  - los pesos, en `config_cuerpo_valle.json:8`, `19`, `106` y `276-281`.
- Las demás citas son de su lectura.
- «cv» es `cuerpo_valle.py`, «cfg» es `config_cuerpo_valle.json` y «A» es `paintball/alma/appraisal_zs_v42_exp.py`.

**Cómo funciona, en una frase.**
- Para cada cosa que puede hacer, imagina cómo estará al cabo de un rato: una «foto».
- Esa foto la convierte en «filas». Cada fila es una necesidad que pierde o una cosa que gana.
- Cada fila se reparte entre tres ejes, cuerpo, recursos y vínculo, con un reparto fijo (A:417-440).
- El motor mide lo lejos que queda ese estado de sus metas: cuerpo 1,0, recursos 2,0, vínculo 0,8 (`motor/model.py:78-80`).
- Elige la opción que queda más cerca (cv:204-216 y 1288-1291).

**Qué interruptores lleva.**
- RG69r+voz es RG68r más la reserva y la voz (`lanza_experimento_v6.py:33`).
- RG68r es RG61r con «ven, lo necesito» apagada y sin llamadas cuando duerme (`banco_v7.py:309-310`).
- La regla general está encendida, así que las filas son las de `_filas_rg` (cv:1476). Parte de las de antes y les quita cinco (cv:2189):
  - la anticipación de la noche;
  - la llamada;
  - la curiosidad;
  - el «cuánto»;
  - el enfado.

### Lo que cuenta como perder

| fila | qué la sube | reparto (cuerpo · recursos · vínculo) | dónde |
|---|---|---|---|
| F-DANO | la vida que le falta | 0,8 · 0,1 · 0,1 | cv:1612 |
| F-HAMBRE | el hambre; por encima de 60 pesa hasta el doble | 0,8 · 0,1 · 0,1 | cv:1613, 2109-2116 |
| F-CANSANCIO | el cansancio | cuerpo | cv:1614 |
| F-FRIO | el frío, solo fuera de cualquier casa | cuerpo | cv:2201-2204 |
| F-SIN-MEDICINA, F-ULTIMA-COMIDA | dar su última medicina o su última comida | como el daño y el hambre | cv:2192-2198 |
| R-CARENCIA | la comida que le falta frente a la que comerá antes de que se le pudra | 0,15 · 0,7 · 0,15 | cv:2191, 2302-2314 |
| R-ACOPIO | no llevar medicina, si cree que cura | 0,1 · 0,8 · 0,1 | cv:1652 |
| R-CURIOSIDAD-FRONTERA | lo que le falta saber de dónde hay comida | sobre todo recursos | cv:2199-2200 |
| R-HERMANO-FALTA | la hermana o una vecina, flaca, herida o pidiendo | 0,1 · 0,8 · 0,1 | cv:1674-1700 |
| S-DANO-PAREJA, S-PROVISION | la herida de la hermana o de las vecinas, el duelo que oye | 0,15 · 0,25 · 0,6 | cv:1672, 1686, 1713-1725 |
| S-DANAR, S-QUITAR | pegar o empujar a una de las suyas | 0,1 · 0,1 · 0,8 | cv:2205-2215 |
| S-SOLEDAD | estar sola; la hermana a la vista quita la soledad, y una vecina, según su vínculo | 0,1 · 0,1 · 0,8 | cv:1727-1731 |
| S-COMPANIA | estar a más de 7 pasos de la hermana (tope 0,32) | 0,1 · 0,1 · 0,8 | cv:1732-1738 |
| S-DUELO-… | la muerte de una de las suyas, en los tres ejes | cuerpo, recursos o vínculo | cv:1544-1550, 1657-1667 |
| la bestia | apartado de la bestia, más abajo | | |

### Lo que cuenta como ganar

- **Lo que la foto alivia.** Por cada pérdida que la foto baja respecto de ahora, hay una ganancia del mismo tamaño y con el mismo reparto, llamada «G-…» (cv:2225-2236).
  - El alivio de la otra al darle algo va al vínculo («G-ALIVIO», cv:2234-2235).
- **«Vivir bien»** (cv:2261-2277; los números, en cfg:276-281):
  - **cuerpo:** 0,82 × la media de lo que tiene de comida, descanso y calor;
  - **recursos:** la comida guardada frente a la de dos días. Con dos días justos da 1,6, y se acerca a 2,0 con más;
  - **vínculo:** 0,68 × su vínculo con la hermana, si la tiene a la vista.
- **El gesto de dar** comida (cv:2243-2246) y el gusto de la otra al recibir (cv:2238-2242).
- **Lo sentido de verdad:** el hambre que quitó al comer, la comida nueva que consiguió y el alivio al dar. Se queda en su estado y baja a la mitad cada 44 turnos (cv:2247-2251 y 2282-2294).
- **Las suyas cerca:** el valor aprendido de cada una (cv:1975-1998).

### Casa, despensa, huerto, almacén y territorio

- **Como recurso suyo cuenta la comida guardada**, W (cv:2274 y 2313):
  - lo que lleva en la bolsa;
  - lo que vio en su despensa;
  - un octavo de lo que vio en el almacén (cfg:106: «entre» = 8);
  - la promesa de un trabajo en el huerto y el fruto que espera.
- **La casa no es un recurso.**
- **La despensa** cuenta por la comida que tiene dentro. Es la de su casa, porque el mundo no deja ver ni usar otra (parte 1, punto 18).
- **El almacén** cuenta un octavo de lo que vio en él, como si le tocara la parte de una de las ocho.
- **El huerto** solo entra como fruto esperado y como promesa de trabajo. Cualquier planta vale igual: no hay huerto suyo (cv:1386-1393 y 1445).
- **Territorio: no hay nada parecido.** Ninguna fila valora un sitio por ser suyo ni pide defenderlo.
  - Las filas que miran la casa miran «cualquier casa» (`todas_casas`): para la bestia (cv:1619), para el frío (cv:2202) y para dormir fuera (cv:2516-2528).
  - La casa propia solo aparece como destino «ir a casa» (cv:2793-2802) y en la voz.

### El vínculo: la hermana, las vecinas y el grupo

- **Dos pesos distintos para cada otra:**
  - **por familia, de nacimiento, sin aprender:** la hermana 0,9864 y una vecina 0,3675 (cfg:8; cv:2043-2048);
  - **por trato, aprendido:** entre 0 y 1, rehecho cada turno con lo que ha vivido con ella (cv:762 y 1949-1952).
    - Cuenta el tiempo juntas y los regalos menos los robos, apuntado cada 44 turnos (cv:1880-1890).
    - **NO SEGURO:** según el ayudante, si no la vio en esos 44 turnos apunta 0. No lo he comprobado yo.
- **Cuando la otra sufre, le falta algo o está en peligro,** pesa por familia (`peso_kin`, cv:2084-2087).
- **Lo que gana al darle** pesa por familia × (su trato de ahora / el trato al nacer) (`peso_dar`, cv:2054-2060).
- **Con la hermana:**
  - verla (V-VINCULO, y quita la soledad);
  - no alejarse más de 7 pasos (S-COMPANIA);
  - su herida o su hambre (S-DANO-PAREJA, R-HERMANO-FALTA);
  - su muerte (duelo);
  - dañarla o quitarle comida (S-DANAR, S-QUITAR).
- **Con las vecinas** (todas las que no son su hermana): lo mismo, con su peso.
  - Las de la vista quitan la soledad según su trato (cv:1728-1730).
  - No tiene ninguna fila de «estar cerca» de ellas, como S-COMPANIA con la hermana.
- **El grupo entero no tiene ninguna fila.** Todo va una a una, y casi siempre cuenta la mayor, no la suma.

### Cómo entra la bestia

**Las filas de la bestia** (cv:1619-1636):
- **El alcance (F-4-ALCANCE):** lo cerca que está de la bestia. Es como mucho 0,5 y baja hasta 0 a 44 pasos (A:130; cv:1622).
  - Una llamada «la bestia» oída cuenta igual, desde donde llamaron (cv:1640-1642).
- **El agresor (S-7-AGRESOR):** si le pegó hace poco, con reparto 0,5 · 0,1 · 0,4.
- **El reencuentro (F-REENCUENTRO):** si se le acerca otra vez, cuenta lo que le pegó antes.
- **La amenaza a la hermana (F-HERMANO-AMENAZA):** la bestia pegada a la hermana. Es 0,25 × el golpe de la bestia / la vida que le supone a la hermana (A:369).

**Cuándo no cuentan o cambian:**
- **Dentro de cualquier casa** no cuentan (cv:1619).
- **El miedo:** la criatura nace valiente (×0,5) o prudente (×1,5), y eso multiplica las filas de miedo (cv:1740-1741).
- **Echarla o matarla:** si la foto imagina que la echa o la mata, las filas se calculan sin esa bestia (cv:1470-1475). Lo que gana es lo que alivian esos miedos, más la comida que le quite; lo que pierde, la vida que le cuesta.
- **Dormir fuera** cuesta la vida que el cuaderno dice que cuesta (cv:2516-2528).
- **La bestia se imagina quieta** donde está ahora. **NO SEGURO** cuál mira cuando ve dos.

### Hasta dónde imagina

- **Cada foto mira 44 turnos adelante** (cfg:19; cv:2473).
- **Una sola cosa por foto:**
  - una acción del turno, y el resto del rato quieta;
  - o un destino («ir a …»): el camino hasta allí, como mucho 44 pasos, y el resto quieta (cv:2479-2493).
- No encadena varias acciones: lo de encadenar destinos («rondas») está apagado en ella.
- **Al anochecer y de noche,** todas las fotos miran hasta la mañana y acaban durmiendo (cv:2503-2515).
- **Cuando elige ir a un sitio,** no vuelve a decidir hasta que llega, se atasca o cambia lo que siente (cv:2851-2861).

### Qué recuerda de un día para otro

- **El cuaderno.** Lo que aprende del valle, por ejemplo cuánto quita una comida o cuánto duele la bestia, pesa menos cada día: × 0,95 por día (`paper7/cuaderno_P7.py:23` y `59-62`). Lo heredado de la cultura no se olvida.
- **Se queda para siempre:**
  - los matorrales y las plantas que vio, con lo que tenían y cuándo los vio;
  - lo a menudo que dan fruto;
  - las casillas que vio (cv:741-753).
- **Se queda con el último valor visto:** el nivel del almacén y su despensa (cv:755-756).
- **Se olvida pronto:**
  - una fuente de comida que vio vacía;
  - las llamadas oídas, a los 44 turnos;
  - lo sentido, a la mitad cada 44 turnos.
- **El duelo** baja a la mitad cada 600 turnos por la hermana y cada 300 por una vecina (cv:1187-1188).

### Lo que añaden la reserva y la voz

- **La reserva** (`cuerpo_rg69.py:21-33`): en la foto de comerse una comida, si ya puede comer, la comida sigue contando como guardada. Así, comerse lo que lleva no es perder recursos. No añade ninguna fila.
- **La voz** (`cuerpo_vc1.py:54-60`): durante 44 turnos después de oírla, en cada foto se imagina a la hermana dentro de su casa. Cambia todas las filas que miran dónde está la hermana. Tampoco añade ninguna fila.

## Parte 6: cierre

**Las partes 2, 3 y 4 son análisis hecho después, no predicción.** No se proponen causas.

**Una corrección del informe 157.**
- La frase de su informe decía que la felicidad es «más baja los días 2, 4, …, 40». Es al revés.
  - La tabla del 157 restaba los días con fruto (1, 3, …, 39) menos los días sin fruto, y salía negativa.
  - Es decir, la felicidad es más baja **los días con fruto, 3, 5, …, 39**.
- La parte 4 de hoy lo confirma: los mismos tamaños, con el signo contrario.
- No he cambiado el informe 157; la corrección queda aquí y en STATUS.

**Cómo leer las tablas de la parte 3:**
- **Los turnos de trabajo** son los de las ocho de la partida juntas.
- **La sequía dura con el huerto al máximo** es una cuenta con las reglas, no una partida.
- **En la escasez da 23,3 comidas al día sin el árbol, frente a 22,9 de base para las ocho.** Alcanza por 0,4, sin contar lo que se come la bestia ni lo que se pudre.

**Lo que se ha usado:**
- **Un programa nuevo**, `bestia_huerto_160.py`. Sus cuentas por partida van en `bestia_huerto_160/partidas.json`, fuera del commit.
- **Un ayudante de solo lectura** para la parte 5. Sus citas, comprobadas como se dice arriba.
- **Cuatro programas cortos en la terminal** (`python3 -I` con texto delante) para mirar ficheros:
  - las claves de `fin.json`;
  - el signo del 157 en la caché;
  - el número de matorrales de la primera foto;
  - el `stats_aparicion` de la salida.
- **Y uno más que no servía para nada,** `python3 -I -c "print(1)"`.
- Ninguno escribe nada.

**Gasto:** 0 créditos de la plataforma y 0 dólares de la consola. No se ha jugado ninguna partida ni se ha usado la clave.
