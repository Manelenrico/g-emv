# El valle tal como se jugó en el v6 y en la escalera

*Ficha de lectura, prompt 159 (19-nov-2026). Para quien no ha visto el código.*

## De dónde salen los números

- **Las partidas del v6 y de la escalera** se jugaron con los mismos ficheros que hay hoy en el disco. Cada `fin.json` guarda la huella (md5) de `valle/config_valle.json`, `valle/mundo.py`, `cantera/paper8/cuerpo_valle.py` y `motor/model.py`, y las cuatro coinciden con las de hoy. Lo he mirado en una partida de cada experimento, y un ayudante lo miró en las 1.600.
- **Cada número lleva su fichero y su línea.** Cuando no se dice otra cosa:
  - «config» es `valle/config_valle.json`;
  - «mundo» es `valle/mundo.py`;
  - los demás ficheros están en `cantera/paper8/`.
- **La configuración trae algunas cosas apagadas** que los lanzadores encienden en cada mundo. Están en el apartado de los cinco mundos.
- **Cómo se ha hecho.** He leído el código con tres ayudantes de solo lectura y he comprobado yo, una por una, unas 150 de las líneas citadas (la mayoría de la config y las reglas clave del mundo y de los lanzadores). Las demás citas vienen de su lectura y no las he repasado todas.
- **«NO SEGURO»** marca lo que no se puede saber con seguridad.

## 1. El mapa

**Lo general:**
- **El tamaño:** una rejilla de 48 × 48 casillas, numeradas del 1 al 48; la fila crece hacia el sur (config:4-5).
- **Qué es fijo:** todo el mapa es el mismo en todas las partidas. La semilla solo coloca los matorrales, los sitios de los árboles dulces, la bestia del principio, la medicina y el reloj de cada planta y cada matorral.
- **Dónde se construye:** mundo:81-122.
- **La figura:** `figuras/valle_mapa.png` y `.pdf`.

**Las zonas:**
- **Zona salvaje:** un anillo de 6 casillas de ancho por el borde del mapa (config:6; mundo:87).
  - Quitando los caminos que la cruzan, son 960 casillas.
  - Cada turno que una criatura pasa en ella tiene un 1 % de probabilidad de perder 5 de vida (config:716-717; mundo:688-689).
- **Bosque:** todo lo de dentro del anillo que no es otra cosa. Son 992 casillas.
- **La plaza (en el código, «aldea»):** un cuadrado de 12 × 12 en el centro, de la casilla 19 a la 30 en las dos direcciones (config:7-11; mundo:88-90). Dentro están las cuatro casas y el almacén.
- **Casas:** cuatro, A, B, C y D, de 3 × 3 casillas cada una (config:30-72; mundo:104-108).
  - Cada una tiene una puerta, que es una casilla de la propia casa.
  - Solo se entra y se sale por la puerta (mundo:455-458).
  - A está arriba a la izquierda, B arriba a la derecha, C abajo a la derecha y D abajo a la izquierda.
- **Almacén:** cuatro casillas en el centro de la plaza, de la (24,24) a la (25,25) (config:12-29).
  - No se puede pisar (mundo:453).
  - Se usa desde cualquiera de las 12 casillas que lo rodean (mundo:111).
- **Huertos:** cuatro, uno en cada esquina de fuera de la plaza (config:85-438; mundo:98-102).
  - Cada uno es un cuadrado de tierra de 4 × 4 casillas con una planta en cada esquina: 16 plantas en total.
  - La tierra se pisa.
- **Caminos:** dos columnas (24 y 25) de norte a sur y dos filas (24 y 25) de este a oeste, que cruzan todo el mapa salvo la plaza (config:73-82; mundo:91-97).
- **Puertas del valle:** dos casillas al final de cada camino, en los cuatro bordes (config:478-535).
  - No llevan a ningún sitio (`conecta_con: null`) y no se pueden pisar (mundo:453). En la práctica están cerradas.
- **Entradas de la bestia:** donde cada camino cruza el anillo salvaje (config:440-457): norte (25,6), este (43,25), sur (24,43) y oeste (6,24).
- **Matorrales:** 21 en el bosque y 5 en la zona salvaje, en casillas que pone la semilla (mundo:214-217).
  - La config dice 24 y 6 (config:802 y 807), pero esos números no se usan: el número lo calcula el margen de comida (apartado 6).
  - Se ven siempre, desde el principio (mundo:134).
- **Árbol dulce:** dos sitios en la zona salvaje, que pone la semilla (apartado 6).

## 2. El tiempo

- **Un día tiene 400 turnos** (config:537), en cuatro partes (config:538-555):

| parte del día | turnos | turnos del día |
|---|---|---|
| mañana | 120 | 0-119 |
| tarde | 120 | 120-239 |
| anochecer | 40 | 240-279 |
| noche | 120 | 280-399 |

- **Una partida dura 40 días**, que son 16.000 turnos.
  - La config dice 20 (config:557), pero el lanzador lo pone a 40 al crear el mundo (`banco_cuerpo_valle.py:25`).
  - Los 1.600 `fin.json` dicen `"dias": 40`.
- **Lo que cambia al caer la tarde y de noche:**
  - **Se ve menos.** Se ven 5 casillas a cada lado por la mañana y por la tarde, 3 al anochecer y 2 de noche (config:601-605).
  - **Hace frío fuera** (apartado 3). La temperatura de fuera es 16° por la mañana, 22° por la tarde, 12° al anochecer y 6° de noche. Dentro de cualquier casa siempre hace 20° (config:833-839).
  - **Al anochecer y de noche se puede dormir siempre**, y el sueño sigue de un tirón hasta la mañana (mundo:541-542 y 642-648). De día solo se duerme con cansancio de 70 o más, o agotada (mundo:542).
  - **La bestia puede bajar a la aldea** al empezar la noche (apartado 9).
  - **El oído no cambia de noche** (config:606).
  - **Se puede trabajar el huerto de noche** (`trabajar_de_noche: true`, config:595).

## 3. El cuerpo de una criatura

- **Las criaturas:** hay 8, dos hermanas por casa, A1, A2, B1, B2, C1, C2, D1 y D2 (config:559; mundo:66-67).
- **Sus números:** vida, hambre, cansancio y herida, más cuatro marcas: agotada, dormida, muerta y la causa de la muerte (mundo:198).
- **Al nacer:** vida 100, hambre 0, cansancio 0 y herida 0. El máximo de cada número es 100 (config:560-562).

**El hambre** (mundo:679-687):
- **Lo que la sube:**
  - **cada turno, 0,25** (config:563);
  - **el reloj del hambre:** si ese turno duerme, ×0,75; despierta por la tarde, ×1,3 (config:630-634);
  - **andar:** +0,05 por paso (config:564);
  - **trabajar:** +0,1 por turno de trabajo (config:583);
  - **el frío**, que va aparte (más abajo).
- **El tope** es 100 (mundo:686).
- **Lo que la baja:** comer, 35 por comida (config:650).
  - Puede bajar de cero (config:642-645).
  - Con hambre por debajo de 15 está harta y no puede comer comida (config:599; mundo:486-489). Por eso lo más bajo es 15 − 35 = −20.
- **Sin comer**, la base sola tarda 100 / 0,25 = 400 turnos, un día, en llevarla de 0 a 100.

**El frío:**
- Fuera de casa, por debajo de 15°, el hambre de cada turno se multiplica por 1 + 0,05 por cada grado de menos (config:840-845; mundo:682-684).
  - Al anochecer fuera (12°) es ×1,15; de noche fuera (6°) es ×1,45.
  - El calor no hace nada.
- Una noche entera fuera, contando el anochecer, suma unas 11,6 de hambre de más:
  - el anochecer pone 40 × 0,25 × 0,15 = 1,5;
  - la noche dormida pone 120 × 0,25 × 0,75 × 0,45 = 10,1.
  - La cuenta del mundo está en mundo:153-163.
- No hay otro efecto del frío: no quita vida ni da cansancio.

**La vida:**
- **Lo que la baja:**
  - **con el hambre en 100**, pierde 0,5 por turno (config:565; mundo:687). Así, de 100 a 0 tarda 200 turnos, medio día;
  - **la zona salvaje:** un 1 % de probabilidad de perder 5 en cada turno que pasa en ella;
  - **un golpe de otra criatura:** −15 (config:576);
  - **un golpe de la bestia:** −40 (config:721).
- **Lo que la sube:**
  - **durmiendo:** +0,25 por turno, si el hambre es de 50 o menos (config:582 y 586; mundo:770-771);
  - **la medicina:** cura hasta 40, pero solo de herida, no el daño del hambre (config:667; mundo:814). «Herida» es la cuenta del daño de golpes, bestia y terreno.

**El cansancio** (de 0 a 100):
- **Lo que lo sube:**
  - **estar despierta:** +0,15 por turno (config:587);
  - **cada paso:** +0,15, o el doble con la bolsa llena (config:566-567);
  - **trabajar:** +0,2 (config:584);
  - **golpear:** +3 (config:577);
  - **empujar:** +5 (config:578).
- **Lo que lo baja:**
  - **quedarse quieta:** −0,2 (config:568). Con el +0,15 de estar despierta, se queda en −0,05;
  - **dormir:** −0,6 (config:569).

**Cuándo queda agotada:**
- Al llegar el cansancio a 100 queda agotada (mundo:692), y lo sigue hasta bajar a 70 (config:570).
- Agotada se duerme sola, pida lo que pida (config:589; mundo:641), y no puede moverse, coger ni trabajar.
- Durmiendo, de 100 a 70 tarda unos 50 turnos.

**Qué la despierta:**
- un golpe o un empujón;
- tener la bestia al lado;
- oír una de las llamadas que despiertan, entre ellas «la bestia»;
- oír un dolor fuerte.

Está en config:613-622 y mundo:509-527. Al despertar por la mañana, durante 10 turnos no puede dar dos pasos seguidos (config:611).

**De qué puede morir:** muere cuando la vida llega a 0 (mundo:604-617). Las causas posibles son cuatro:
- **hambre**, por pasar tiempo con el hambre en 100;
- **terreno**, por la zona salvaje;
- **golpe de otra criatura**;
- **la bestia**.

Al morir, lo que llevaba cae al suelo, y su cuerpo se queda hasta el final del día siguiente (config:597).

## 4. Lo que percibe

**Lo que ve:**
- Un cuadrado alrededor de ella: 5 casillas a cada lado de día (11 × 11), 3 al anochecer (7 × 7) y 2 de noche (5 × 5) (config:601-605; mundo:491-494, 1121-1122).
- En cada casilla que ve: el terreno, lo que hay en el suelo, cada planta (frutos, trabajo y cuidado) y cada matorral (frutos) (mundo:1125-1132).
- Dónde están los matorrales lo sabe siempre, aunque no los vea (mundo:134).

**Lo que ve de las otras criaturas** que tiene a la vista (mundo:1138-1140):
- dónde están y de qué casa son;
- qué tipo de cosas llevan;
- si está «flaca» (hambre de más de 60) o «herida» (vida de menos de 70) (config:571-572);
- su energía: fuerte, normal, cansada o agotada (mundo:565-568);
- su nivel de vida: sana, herida, muy herida o moribunda (mundo:558-563).
- **No ve** el número exacto de hambre ni de vida, ni si la otra está dormida. La cara está apagada en estas partidas (mundo:1141).

**Lo demás que ve:**
- **La bestia**, si está dentro de lo que ve. Dormida, no la ve (config:744; mundo:1143).
- **Lo suyo:** su vida, su hambre, su cansancio, si está agotada, si está en casa y lo que lleva. Ve el nivel del almacén solo dentro de la plaza, y su despensa solo dentro de su casa (mundo:1148-1154).
- **Lo que su cuerpo hizo de verdad el turno anterior.** Está encendido para las criaturas (mundo:1160-1161; `banco_cuerpo_valle.py:30-31`).
- **Las muertes y los cuerpos** que tiene a la vista, y los empujones ganados a la vista. Esto último también está encendido para las criaturas (mundo:616, 695-700, 1157).

**Lo que oye** (el oído no cambia de noche, y dormida también oye; mundo:510):
- **Las llamadas** (apartado 5): llegan a 4, 7 o 10 casillas según se den suave, medio o fuerte (config:874-878). Quien oye sabe quién llamó, qué llamada era, con qué fuerza y desde dónde (mundo:659-662).
- **Los sonidos del ánimo** (placer, dolor, alegría, enfado, amor y tristeza), también a 4, 7 o 10 casillas (config:849-854).
- **La criatura recuerda una llamada oída durante 44 turnos** (`config_cuerpo_valle.json:19`; `cuerpo_valle.py:1094-1097`).

## 5. Lo que puede hacer

**Las acciones del mundo** (mundo:20). Una por turno; sin acción, cuenta como quedarse quieta (mundo:636). Cada turno, criaturas y bestia actúan en un orden sorteado (mundo:627).
- **Mover:** un paso al norte, sur, este u oeste, sin diagonales, a una casilla libre (mundo:18, 747-758).
- **Quedarse.**
- **Dormir** (apartado 3).
- **Coger** una cosa, si la bolsa no está llena (mundo:773-793). De dónde:
  - del suelo de su casilla;
  - de una planta o un matorral de su casilla o de al lado;
  - del almacén, desde una casilla de al lado;
  - de su despensa, dentro de su casa.
- **Dejar** una cosa en el suelo, en el almacén o en su despensa (mundo:794-804).
- **Comer** algo de la bolsa (mundo:805-818).
- **Dar** algo a otra criatura (apartado 8).
- **Trabajar** una planta del huerto (apartado 6).
- **Empujar** (apartado 8).
- **Golpear** (apartado 8).
- **Llamar** y **hablar**, que están construidas y no se usan (más abajo).

**Las llamadas** (en el código, la «voz» del turno: sale junto con la acción, sin gastar el turno):
- **Cuántas hay:** el mundo tiene 4: «aquí estoy», «aquí hay comida», «la bestia» y «ven, lo necesito» (config:868-873). En estas partidas solo suenan 3, porque «ven, lo necesito» está apagada (más abajo).
- **Alcance y coste:** llegan a 4, 7 o 10 casillas, y cuestan 0, 0,15 o 0,3 de cansancio según la fuerza (config:874-883; mundo:663). Una criatura dormida no da llamadas (mundo:657, encendido por el lanzador; `banco_cuerpo_valle.py:35`).
- **Cuándo llama:** la criatura llama solo si lo que imagina que pasará con la llamada le sale mejor que no llamar, contando lo que cuesta gritar (`cuerpo_valle.py:1279`).
- **Lo que no hace:** no miente. Solo dice «la bestia» si la está viendo, y «aquí hay comida» si ve comida (`cuerpo_valle.py:1243`, `1250-1251`).
- **Lo que hace quien la oye:**
  - **«aquí estoy»:** sabe dónde está quien llamó (`cuerpo_valle.py:1111`).
  - **«la bestia»:**
    - fuera de casa, actúa como si la bestia estuviera donde llamaron;
    - de noche, la empuja hacia casa;
    - despierta a quien duerme.
    - Está en `cuerpo_valle.py:906` y `1640-1642`, y en config:613-619.
  - **«aquí hay comida»:** puede elegir ir adonde llamaron, si le cabe algo en la bolsa (`cuerpo_valle.py:2810-2812`).

**La voz de ir a casa** («+voz», tal como quedó):
- **Quién la tiene:** solo las criaturas de RG69r+voz, S69+voz y P69+voz (`lanza_experimento_v6.py:33`; `lanza_escalera_v6.py:24`). Solo habla a su hermana.
- **Cuándo puede sonar** (`cuerpo_vc1.py:27` y `78-79`). Tienen que cumplirse todas estas cosas:
  - es el turno 180 del día o más tarde, es decir, desde la segunda mitad de la tarde hasta el final de la noche;
  - quien habla está despierta y fuera de su casa;
  - la hermana está viva, despierta y a 7 casillas o menos;
  - no tiene ya una voz suya sonando.
- **Qué la hace sonar:** quien habla vuelve a mirar sus opciones imaginando a la hermana en casa al final. Si así la mejor opción es «ir a casa», suena la voz (`cuerpo_vc1.py:91-92`).
  - Lo que hace ella misma no cambia: la voz puede sonar aunque ella elija otra cosa.
- **Lo que hace la hermana que la oye:** durante 44 turnos, al imaginar lo que puede hacer, se imagina a la hermana que habló dentro de casa al final. Nada más (`cuerpo_vc1.py:18`, `54-60` y `76`).
- **Ojo:** esta voz no pasa por el mundo. No está en lo que oye la criatura ni en el registro del mundo (`mundo.jsonl.gz`). Se lleva aparte (`cuerpo_vc1.py:29`), y lo que sabe de la hermana (dónde está, si duerme, si vive) lo pone el lanzador desde el mundo (`lanza_vc1.py:26-27`). Se apunta en `voz_vc1.json`.

**Construido pero apagado en estas partidas:**
- **Hablar:** texto libre que llega a 3 casillas (config:581; mundo:863-867).
  - El mundo no la ofrece entre las acciones posibles (mundo:570), y la criatura la quita de sus opciones (`cuerpo_valle.py:2931`; `config_cuerpo_valle.json:143`).
- **La acción «llamar» de antes,** con 8 llamadas (config:764-773), a 10 casillas (config:580). Ya no sale sola y está fuera de las opciones (`cuerpo_valle.py:2883` y `2931`).
- **«Ven, lo necesito»:** ni se da ni se oye (`banco_v7.py:309`, `voz_sin_ven_v63`; `cuerpo_valle.py:495-496`, `1101` y `1249`).
- **La libreta del almacén:** las últimas 10 entradas y salidas (config:709-710).
- **La cara y las piezas de voz de los talleres** (`cara_v64`, `voz_v64` y otras): solo en variantes de taller (`banco_v7.py:283-305`).
- **Imaginar a la hermana moviéndose** (`imagina_v45`), apagado desde RG46r (`banco_v7.py:204`).
- **«El dolor quita el sueño»** (config:625-626).
- **De la bestia:** la bestia de día, la cría, las épocas de la bestia y la sequía dura. Están apagadas en la config y el lanzador las enciende solo en su mundo (apartado 10).

## 6. La comida

**Cuánta necesita una criatura:**
- La base es 0,25 × 400 / 35 = **2,86 comidas al día** (config:563, 537 y 650; la fórmula, en mundo:248). Para las 8 son 22,9.
- A eso se suman los pasos, el trabajo y el frío. El reloj del hambre lo cambia poco, porque lo que ahorra durmiendo lo gasta por la tarde.
- **NO SEGURO:** cuánto suman de verdad los pasos, el trabajo y el frío depende de cómo viva cada criatura. No se ha medido aquí.

**Cuánta comida hay: el margen de comida** (config:788-789, `activo: 0.05`; mundo:269-282).
- El mundo calcula cuántos matorrales pone para que haya un 5 % más de lo que comen.
- La cuenta:
  - lo que comen las 8 con el margen: 22,86 × 1,05 = 24 comidas al día;
  - lo que da el huerto sin cuidar: 8 al día;
  - lo que falta: 16;
  - dos tercios en el bosque: 16 × 2/3 / 0,5 = 21 matorrales;
  - un tercio en la zona salvaje: 16 / 3 / 1 = 5 matorrales.
- **Sin cuidar el huerto** hay 23,5 comidas al día.
- **El huerto bien cuidado** da 32 al día en vez de 8.
- **En los mundos con épocas**, lo que da cada matorral y cada planta se multiplica por el factor de la época (apartado 10).

**El huerto** (config:687-702; mundo:1066-1087):
- **Las plantas:** 16, que dan fruto una vez cada 800 turnos, es decir, cada dos días (config:688).
- **Lo que da cada planta:** 1 fruto sin cuidar y hasta 4 bien cuidada. La cuenta es 1 + 3 × cuidado (config:690; mundo:1071-1073).
- **El trabajo:** cada turno trabajando sube el cuidado 1/20 (config:689; mundo:838).
- **El cuidado se va solo:** baja a la mitad cada 1.600 turnos sin trabajar (config:699).
- **Lo que cuesta trabajar:** 0,1 de hambre y 0,2 de cansancio por turno.
- **Todas las plantas a la vez:** las 16 dan fruto los mismos días, del día 1 en adelante, un día sí y otro no (la parte 2 del prompt 157).
- **El fruto** aguanta 800 turnos en la planta (config:658).

**Los matorrales** (config:797-830; mundo:1088-1103):
- **Lo que dan:** uno del bosque da 1 fruto cada 800 turnos (0,5 al día); uno de la zona salvaje, 2 (1 al día) (config:800-801 y 805-806).
- **No se trabajan.**
- **Cuándo dan el primero:** cada uno en un turno al azar entre el 1 y el 800, así que no van a la vez (mundo:217).
- **El fruto** aguanta 400 turnos en el matorral (config:660).

**El bosque:**
- **Las bayas:** cada fruta de matorral tiene un 10 % de probabilidad de caer como baya en una casilla del bosque al azar (config:810; mundo:1099-1101). No es comida de más: lo que cae se le quita al matorral.
- **No aparece más comida suelta**, porque hay matorrales (mundo:258-259). La aparición de 12 en el bosque y 6 en la zona salvaje de la config (config:676-680) no se usa para la comida.
- **NO SEGURO:** la nota de la config dice que la baya cae «en una casilla sin matorral». El código elige entre todas las casillas del bosque, con matorral o sin él (mundo:1100).

**El árbol dulce** (encendido en todas las partidas jugadas, apartado 10; los números, en config:886; el código, en mundo:373-427):
- **Dónde:** dos sitios en la zona salvaje, a 40 pasos o más de la puerta de casa más cercana y separados al menos 20 casillas.
- **Cuándo:** cada uno aparece 2 o 3 veces por partida, en momentos al azar, y dura 3 o 4 días.
- **Lo que da:** 20 frutas dulces, que alimentan igual que la otra comida y no se pudren en el árbol. Lo que queda al irse se pierde.
- **La bestia:** al anochecer y de noche, la bestia más cercana va hacia el árbol y a quien encuentra allí le quita primero la fruta dulce.

**La zona salvaje:**
- La comida que da son los 5 matorrales salvajes, que dan el doble que los del bosque, y los árboles dulces.
- Allí aparece también la medicina, y allí está el riesgo de herirse (apartado 1).

**Cuándo se pudre la comida** (config:653-661):
- suelo, 150 turnos;
- matorral, 400;
- planta, 800;
- bolsa, 800;
- despensa, 1.600;
- almacén, nunca.

Lo que ya lleva podrido viaja con ella de un sitio a otro (mundo:1039-1047).

**La medicina:**
- **Dónde y cuánta:** aparecen 2 al día en la zona salvaje (config:681; mundo:1104-1115). No aparecen si ya hay 4 en el suelo de la zona (config:671).
- **Lo que hace:** cura 40 de herida, no alimenta y no se pudre. Se puede tomar estando harta (config:664-670; mundo:489).

**La bestia muerta** deja 24 comidas en su casilla (config:760).

## 7. Dónde se guarda

| sitio | huecos | cuánto aguanta la comida |
|---|---|---|
| bolsa | 6 (config:575) | 800 turnos |
| despensa (una por casa, solo se usa dentro de la casa) | 4 (config:712-714) | 1.600 turnos |
| almacén (uno para todas, en la plaza) | sin límite (mundo:800) | no se pudre |

- **El almacén empieza con 48 comidas** (config:683-684).
- **Su nivel** se ve desde la plaza y cuenta solo la comida (config:704-708; mundo:552-556):
  - lleno, con 36 o más;
  - a medias, con 16 o más;
  - poco, con 1 o más;
  - vacío.

## 8. Entre criaturas

- **Dar** (mundo:819-828):
  - una cosa por turno, a una criatura viva que esté al lado (no en la misma casilla) y tenga sitio en la bolsa;
  - no cuesta nada.
- **Empujar a otra criatura** (mundo:888-909):
  - **Lo que cuesta:** +5 de cansancio a cada una de las dos.
  - **Quién gana:** el bando mayor. Cada bando es la criatura más sus hermanas vivas que estén al lado (mundo:891). Si empatan, gana la menos cansada; si también empatan en eso, no pasa nada (mundo:895-900).
  - **Lo que pasa:** la que pierde suelta toda la bolsa. Va a la ganadora hasta llenarle la bolsa, y lo que no cabe cae al suelo (mundo:902-905).
  - No hace daño, pero despierta a la empujada.
- **Golpear a otra criatura:** tiene que estar al lado. Quien golpea paga +3 de cansancio y la otra pierde 15 de vida (config:576-577; mundo:852-855). La golpeada se despierta.

## 9. La bestia

- **Dónde vive:**
  - Al empezar hay una, en una casilla de la zona salvaje al azar (mundo:221).
  - De día da vueltas por el anillo salvaje y sus caminos (mundo:1010-1014).
  - Puede andar por la zona salvaje, los caminos, la plaza, los huertos y el bosque. No entra en las casas ni en el almacén (config:743; mundo:119-120).
  - Da un paso por turno (config:747).
- **Cuándo se acerca:**
  - **De noche.** Al empezar la noche (turno 280 del día), si está de ronda, baja con probabilidad 0,5 (config:725-739; mundo:961-963).
    - Va por la entrada más cercana a ella, pasa por el borde de la plaza y sigue hasta la planta con fruto más cercana (mundo:964-972).
    - Se come hasta 4 frutos de las plantas por noche (config:741).
    - Luego vuelve, y por la mañana se va (mundo:983 y 1001-1005).
  - **De día**, solo en el mundo «bestias que crían» (apartado 10).
- **Qué hace al encontrarse con una criatura** al lado, fuera de casa (mundo:1017-1033):
  - De ronda, solo mira a las que están en el anillo salvaje.
  - Si la criatura lleva algo, le roba la bolsa entera; si además está dormida, le pega 40 (config:745).
  - Si no lleva nada, le pega 40 (config:721).
  - Deja en paz 24 turnos a la que ya tuvo delante (config:724).
  - Se come lo robado a los 40 turnos (config:723).
- **Empujarla** (mundo:875-887):
  - **Lo que cuesta:** +5 de cansancio a quien empuja.
  - **Cuándo se gana:** si hay 2 o más criaturas pegadas a ella (config:722).
  - **Si se gana:** lo que llevaba robado pasa a quien empuja, y ese turno no pega (config:742).
  - **Si se pierde:** pega 40.
- **Echarla** (encendido en todos los mundos; config:759; mundo:339-346):
  - Cuentan las que la empujan en el mismo turno. Con 2 o más, sale del mapa y suelta lo que lleva.
  - Vuelve a la zona salvaje al cabo de 400 turnos con 2 empujando, unos 735 con 3 y unos 1.131 con 4. La cuenta es 400 × (n / 2)^1,5.
- **Matarla** (encendido en todos los mundos; config:760; mundo:327-338 y 348-354):
  - Tiene 150 de vida y se cura 2 por turno.
  - El daño de un turno es 15 × n^1,5, con n las que le pegan a la vez: 15 con una, 42 con dos, 78 con tres y 120 con cuatro.
  - A cada una que le pega le devuelve 40.
  - Si muere, deja 24 comidas, y a los 2.000 turnos aparece otra en la zona salvaje.
- **Lo que puede hacer daño:** golpes de 40, a quien no lleva nada, a la dormida a la que roba y a quien la golpea o pierde un empujón. No se sabe aquí cuántas veces pasó en las partidas.

## 10. Los cinco mundos

**Cómo se arma cada mundo:**
- **El lanzador** arma cada mundo con `mundo_de` (`lanzador.py:31-41`, envuelto por `medida_v3/lanza_medida_v3.py:44-49`). Lo que cambia se apunta en el `fin.json` de cada partida, en «mundo_cambios» (`lanzador.py:82` y `90`).
- **En los cinco mundos:**
  - **el árbol dulce está encendido** (`medida_v3/lanza_medida_v3.py:47`);
  - **las criaturas juegan con «+sabores»**, que solo apunta de dónde viene cada comida (huerto, bosque, dulce o bestia) y no cambia cuánto alimenta (`taller_v40.py:12-13`; mundo:172-175);
  - **echar y matar a la bestia** están encendidos desde la config (config:759-760).
  - **El tonto y el recolector del v6** juegan sin «+sabores», con el árbol encendido (`lanza_experimento_v6.py:98`). En la escalera no juegan.
- **Lo que cambia en cada mundo:**

| mundo | qué cambia frente al normal | dónde |
|---|---|---|
| normal | nada: sin épocas, una bestia que solo baja de noche | `lanzador.py:35`; `pasada_v22.py:11` |
| abundancia | épocas de 5 días, todas con factor 1,3: siempre un 30 % más de fruto en matorrales y huerto | `lanzador.py:35`; `pasada_v22.py:9-11`; `pasada_v18.py:9` |
| sequía | épocas de 5 días en ciclo: factor 1,3 / 1,0 / 0,7 / 1,0 (abundancia, normal, escasez, normal), en matorrales y huerto | ídem |
| sequía dura | las mismas épocas, con cada factor × 0,7: 0,91 / 0,7 / 0,49 / 0,7 | `lanzador.py:36`; config:891-910; mundo:254-257 |
| bestias que crían | la bestia baja también de día, cada mañana (probabilidad 1,0), y vuelve al anochecer; además, cría: una nueva cada 20 días, hasta 2 | `lanzador.py:38-40`; config:748-750 y 890 |

- **Los días de escasez** (factor 0,7, o 0,49 en la sequía dura) caen en los días 11-15 y 31-35, contados del 1 al 40 (prompt 156).
- **En las bestias que crían**, la segunda bestia nace al acabar el día 20 en todas las partidas (prompt 157).
- **Lo que el lanzador cambia y no queda en «mundo_cambios»:**
  - los 40 días (`banco_cuerpo_valle.py:25`);
  - que una criatura dormida no dé llamadas (`banco_cuerpo_valle.py:35`);
  - que cada criatura vea lo que hizo de verdad su cuerpo y los empujones ganados a la vista (`banco_cuerpo_valle.py:30-31`).
  - Nada de esto se aplica al tonto ni al recolector, salvo los 40 días.
- **NO SEGURO:** el bloque entero de «mundo_cambios» se ha mirado en la semilla 30161 de cada mundo. En las 400 partidas de la escalera solo se ha comprobado que cada mundo empieza por la clave que le toca.

## 11. El arranque

- **Dónde nace cada criatura:** en las dos primeras celdas de su casa por orden, sin contar la puerta (mundo:195-197). Lo he comprobado con el primer turno de una partida.
  - A1 en (20,20) y A2 en (20,21);
  - B1 en (27,20) y B2 en (27,22);
  - C1 en (27,27) y C2 en (27,28);
  - D1 en (20,27) y D2 en (20,28).
- **Qué lleva:** nada. Las bolsas, las despensas y el suelo empiezan vacíos (mundo:194 y 199).
- **El almacén:** 48 comidas (config:683-684).
- **El huerto** es el de una aldea que ya existía (config:693-696; mundo:205-210):
  - cada planta empieza bien cuidada (cuidado 1) y con el primer ciclo trabajado;
  - su primer fruto llega en un turno al azar del día 1, con entre 3,5 y 4 frutos por planta;
  - después da fruto cada 800 turnos.
- **Los matorrales** dan su primer fruto entre los turnos 1 y 800 (mundo:217).
- **La bestia** empieza en una casilla de la zona salvaje (mundo:221).

## 12. Los dos controles sin motor

Están en `valle/jugadores.py` y no han cambiado desde los primeros congelados (`CONGELADO_P8_v6.md:127`). Juegan con el mismo mundo (`lanzador.py:85`; `valle/banco_base_v5.py:14-16`).

**El tonto** (`jugadores.py:68-143`):
- **Lo que nunca hace:** no da, no empuja, no golpea, no llama y no habla (`jugadores.py:3-4`).
- **Al nacer:** la hermana de número impar trabaja el huerto y la de número par busca en el bosque (`jugadores.py:74`).
- **Sus reglas, en el orden en que las mira:**
  1. Si está agotada, duerme (`:112`).
  2. Si ve la bestia, o es anochecer o noche, va a una casilla de dentro de su casa y duerme (`:114`).
  3. Si tiene más de 40 de hambre y lleva comida, come (`:69` y `:117`).
  4. Si lleva más de 2 comidas: si está junto al almacén, deja una; si es la del huerto, va al almacén (`:70` y `:120-122`).
  5. Si no lleva comida y no ha visto el almacén vacío, va al almacén y coge (`:124-126`). Del almacén recuerda lo que vio la última vez que estuvo en la plaza (`:100`).
  6. Si el almacén está en «poco» o vacío (`:128-141`):
     - coge lo que haya en el suelo de su casilla, sea lo que sea;
     - si tiene al lado una planta con fruto, la coge;
     - la del huerto trabaja la planta de al lado con menos trabajo, o va hacia las que lo necesitan;
     - la del bosque va a la comida que ve, o a una casilla del bosque al azar.
  7. Si no, vuelve a casa y se queda dentro (`:143`).
- **Si se atasca:** si quiere moverse y lleva 3 turnos en la misma casilla, da un paso al azar (`:88-93`).

**El recolector** (`jugadores.py:146-201`) es como el tonto, con estos cambios:
- **No trabaja nunca el huerto.**
- **Sus fuentes de comida:** conoce todos los matorrales y todas las plantas, y añade el árbol dulce cuando lo ve (`:147`, `:156` y `:166`).
- **Su memoria:** apunta cuándo vio cada fuente y cuántos frutos tenía (`:162-167`).
- **Sus reglas, en orden:**
  1. Agotada, duerme.
  2. Con la bestia a la vista, o al anochecer o de noche, va a casa y duerme.
  3. Con más de 40 de hambre y comida en la bolsa, come.
  4. Con 4 comidas o más, va al almacén y deja de una en una hasta quedarse con 2 (`:152` y `:181-185`).
  5. Con hambre, sin comida en la bolsa y sin haber visto el almacén vacío, va al almacén a coger (`:186-188`).
  6. Si le cabe algo en la bolsa (`:189-200`):
     - coge la comida suelta que ve, o va hacia ella;
     - coge de un matorral o una planta con fruto que tenga al lado;
     - va a una fuente que recuerda con fruto;
     - va a mirar una fuente que no ha visto nunca, o que no ve desde hace más de 200 turnos (`:151`).
  7. Si no, va a casa y se queda dentro (`:201`).

## 13. Los nombres

**Las partes de «RG69r+voz»:**
- **RG** es «regla general»: la criatura que decide qué vale cada cosa por lo que necesita ahora y lo que le sirve, repartido entre cuerpo, recursos y vínculo (`banco_v7.py:67`; `cuerpo_valle.py:292-294`).
- **El 0 delante** (por ejemplo, en RG068r) quiere decir «sin el lado de ganar»: no siente lo ganado al comer, al conseguir o al dar, solo lo que le falta (`banco_v7.py:67-70`, `rg_ganancias=False`; `cuerpo_valle.py:2225-2232` y `2283-2285`).
- **El número** (61, 68, 69) es el de la versión de la criatura. Coincide con la terminación de los interruptores que añade, como `reserva_v69` en RG69r.
  - No es el número del prompt: RG61r es del prompt 115, RG68r del 134 y RG69r del 146.
  - **NO SEGURO:** ningún fichero lo dice con esas palabras.
- **La «r»:** aparece por primera vez en RG32r, que es RG32 más `rapido_v28` (`banco_v7.py:155`). Son tres aceleraciones que no cambian ninguna decisión: las partidas salen idénticas y van un 40 % más rápido (`cuerpo_valle.py:378-380`; `STATUS.md:455`, «adopted as RG32r»). Todas las que llevan «r» después la heredan.
  - **NO SEGURO:** ningún fichero dice literalmente «la r es de rápido». No es de «reserva»: la reserva es otro interruptor, muy posterior.
- **«+voz»** es la voz de ir a casa (apartado 5). En las carpetas se escribe «RG69rvoz», porque allí el «+» separa el mundo de los sabores (`lanza_experimento_v6.py:3-4`).

**Qué distingue a cada una:**
- **RG61r:** la base del congelado v4. Es RG50r más tres arreglos del robo: recuperar empujando no cuenta como regalo, robar baja el trato que se le tiene a la ladrona, y quitar comida pesa en el vínculo como dar (`banco_v7.py:275-278`).
- **RG68r:** RG61r con «ven, lo necesito» apagada y sin llamadas cuando duerme (`banco_v7.py:307-310`).
- **RG068r:** lo mismo que RG68r, pero sin el lado de ganar (`banco_v7.py:310`).
- **RG69r:** RG68r con la reserva (`reserva_v69`).
  - La reserva: cuando ya puede comer, comerse lo que lleva no cuenta como perder recursos, sino como usar la reserva (`cuerpo_rg69.py:2-10` y `21-33`).
  - Se juega con la clase `cuerpo_rg69.RG69` (`lanza_experimento_v6.py:33` y `35`).
- **RG69r+voz:** RG69r con la voz de ir a casa, con la clase `cuerpo_vr1.RG69V` (`lanza_experimento_v6.py:33` y `35`).

**Las tres de la escalera:**
- Tienen las mismas filas, la reserva y la voz; solo cambia cómo componen el valor de cada opción (`lanza_escalera_v6.py:5-6` y `24`; `cuerpo_valle.py:1288-1291`).
- **«Decide con el motor» (RG69r+voz):** cada opción se mide con la distancia del motor (`motor/model.py`, `opponent_distance`), que junta posición frente a las metas, tensión y acoplamiento entre ejes (`cuerpo_valle.py:20` y `203-216`; `motor/model.py:245-276`).
- **«Decide sumando» (S69+voz):** suma ganancias menos pérdidas de las tres dimensiones, sin nada del motor (`cuerpo_valle.py:135-147` y `381-383`).
- **«Decide con la posición» (P69+voz):** solo la parte de posición del motor, sin tensión, techo ni acoplamiento (`cuerpo_valle.py:150-161` y `384-386`).
