---
title: "G-EMV: la manada. Cuidado sin recompensa en un mundo que paga por matar"
subtitle: ""
author: "Manel Enrico"
lang: es
---

Independent Researcher, Barcelona\
ORCID: 0009-0008-1732-6310\
Preprint, versión 1, 2026\
Tercera parte de una historia en tres: el motor [1], la colmena [2], la manada.\
[1] Enrico, M. (2026). G-EMV: A Geometric Architecture of Homeostatic Orientation for Agents. Zenodo. DOI 10.5281/zenodo.21026795. (El motor: primera parte.)\
[2] Enrico, M. (2026). G-EMV: the Hive. Instinct Suffices: a Whole Life Without Reward. Zenodo. DOI 10.5281/zenodo.21994358. (La colmena: segunda parte.)\
Versión española del texto publicado en inglés en Zenodo.

## Resumen

Dos agentes idénticos, con el mismo motor, la misma tabla de lo que les
duele y lo que les alivia, y un hilo de texto entre ellos, juegan
cuarenta partidas en un mundo donde gana el último que queda en pie y
cada muerte da puntos. No tienen recompensa, no han sido entrenados y en
ninguna parte está escrito qué hacer con el otro: solo tres ejes
homeostáticos y una lista de dieciséis situaciones, cada una con su
dolor y su alivio. En lo que el registro guarda de esas cuarenta partidas no pegaron primero ni una vez, defendieron al hermano ciento cuatro veces, le dieron lo que
llevaban — hasta la última venda — y no se golpearon entre ellos.
En los diez segundos siguientes a defender, el defensor perdió veinte
puntos de vida de mediana — parecido a lo que perdía estando al lado sin
defender — y ninguno cayó en esa ventana. Repitiendo la misma serie contra los mismos rivales con las
filas que hablan del hermano apagadas, las defensas pasan de ciento
cuatro a cero y los dones de noventa y ocho a uno, mientras la
contención no se mueve y en la puntuación no se ve diferencia: cuidar al
hermano no le dio ventaja en el marcador, y tampoco se demuestra que le
costara. El registro no guarda las partidas enteras — la plataforma
corta los diarios largos, y queda diario para seis de cada diez tics que
la pareja vivió —, y todo lo que aquí se cuenta se cuenta sobre lo
registrado. Cuarenta partidas dejan ver solo los efectos grandes, y los
límites se dicen enteros.

*Palabras clave: homeostasis, arquitectura afectiva, cooperación sin
recompensa, cuidado, ablación por filas, alineación.*


## 1. La pregunta, y una distinción

**El mundo y la pregunta.** Este trabajo es la tercera parte de una
historia en tres. La primera — el motor — publicó G-EMV: una geometría
de lo que importa, tres dominios de vida, seis fuerzas y una distancia
que descender, definida antes de tocar mundo alguno y sin aprendizaje.
La segunda — la colmena — la puso a vivir en machina_1, un mundo de
Softmax.¹ Softmax es una empresa de investigación en alineamiento de la
inteligencia artificial que mantiene mundos de juego abiertos donde
agentes hechos por equipos distintos conviven y compiten; ni el mundo
ni los rivales los diseñó el autor. En machina_1, ocho cuerpos gobernados por la misma geometría minaban,
abastecían una despensa y conquistaban antenas sin conocerse, y midió
cuánta cooperación cabe en el anonimato: mucha. Aquella biografía
terminó con una frontera declarada — el agente no conocía a nadie — y
con la pregunta que abre esta: qué cambia cuando estos agentes, que
cooperan sin conocerse, empiezan a reconocerse. Para responderla hubo
que cambiar de mundo, y la sección 2 cuenta por qué. El escenario de
este trabajo es ZERO-SUM, otro mundo de Softmax, donde gana el último
que queda en pie y cada muerte que uno causa le da un punto: un mundo
que paga por matar. El agente solo se probó primero en la competición
pública de Softmax, para comprobar que funcionaba; todo lo que este
trabajo mide se jugó después en series propias, con los mismos rivales
en todas, para que cada serie se pueda repetir. La sección 3 cuenta las
dos cosas. En él se sientan dos agentes idénticos, con el mismo
motor, la misma tabla y un hilo de texto entre los dos, y se mide lo que
hacen.

**Lo que hacen, dicho una vez.** Sin recompensa, sin entrenamiento y
sin una línea que diga qué hacer — solo tres ejes homeostáticos y una
tabla de lo que duele y lo que alivia —, en un mundo que paga por
matar, el agente de este trabajo nunca pega primero, defiende al otro
cuando lo golpean, le da lo que lleva, hasta su última venda, si él está
peor, y recuerda quién les hizo daño. La emoción es el número que lo mueve; lo que el otro recibe por radio no es ese número sino el parte — dónde estoy, cuánta vida me queda, quién me pega —, y de él su propia tabla hace un número propio. Cada una de esas frases tiene su medida y
su límite en la sección 4, y su prueba por ausencia en la 5. Aquí solo
se enuncian, para que el lector sepa hacia dónde va.

**Por qué esta pregunta.** Se podría haber escrito en esa tabla una fila
que hiciera que matar aliviara, y el agente habría cazado. No se hizo, y las dos
razones van juntas: una de valores, que se declara como decisión del
autor — no se quería un animal que matara por puntos —, y una
científica. Casi todos los mundos donde compiten agentes son violentos,
y en ellos se da por hecho que para vivir hay que matar. La pregunta de
este trabajo es si una máquina puede moverse en un mundo violento sin
ser violenta — respondiendo solo a quien la agrede —, vivir, cuidar de
otro, y a veces ganar. La ética entra aquí como pregunta y como
decisión; nunca como resultado. La sección 7 dice, al final, lo que la
respuesta afirma y lo que no.

**La imagen, y su descargo.** Si hiciera falta una imagen, sería la de
dos hermanos en una manada pequeña: dos cuerpos con la misma geometría
del valor que, a diferencia de la colmena, se saben el uno al otro. Este
trabajo usa esas dos palabras — hermano, manada — porque son las que se
usaron durante meses para nombrar lo que se veía, y porque a un lector
le dicen más que "el agente del asiento once". Llamarlos hermanos es
solo eso, una imagen: nada en este texto afirma que sientan, y cada
palabra emocional que se use para explicar una fila de la tabla es una explicación que aquí se declara, no una etiqueta que el código lleve. Y
"emoción", en este trabajo, nombra siempre eso: un número que mueve un
cuerpo, no un sentimiento que se le atribuye. En adelante, los dos, el
otro, el hermano.

**Por qué dos, y por qué idénticos.** Se podría haber sentado a un
cuidador y a un cuidado, a uno fuerte y a uno débil, y medir el reparto
de papeles. No es lo que este trabajo quiere medir. Con dos agentes
idénticos, lo que uno hace por el otro es exactamente lo que el otro
haría por él: la simetría quita del medio la pregunta de quién es quién
y deja sola la pregunta de si hay cuidado. Cualquier diferencia entre
los dos, en una partida, es historia — quién nació dónde, a quién le
tocó el arma —, no diseño. Y con dos, y no con ocho, cada gesto tiene
un destinatario único: cuando uno suelta una venda, no hay que
preguntarse para quién era.

**Instrumento y expresión.** Hay una distinción que este trabajo
necesita y que conviene fijar antes de los números, en tres pasos.

El primero es el agente entrenado. Un agente al que se entrena para
maximizar un marcador aprende, con millones de partidas, qué conductas
suben ese número. Si le pagan por puntos y descubre que avisar a su
compañero da más puntos, avisa; si avisar dejara de dar puntos, dejaría
de avisar. Su mensaje es un medio, y existe mientras da puntos. No es un
reproche; es lo que esta arquitectura hace, y lo hace bien.

El segundo es este agente. El parte que un hermano emite sale porque el
cuerpo tiene un estado — dónde estoy, cuánta vida me queda, quién me
pega — y el hilo lo transmite. No hay en ningún sitio un cálculo de si
conviene avisar, porque el marcador del mundo no llega al agente por
ningún camino: ninguna fila lo mira, ninguna regla lo menciona. Si
avisar no sirviera de nada, seguiría avisando igual. Y lo que el otro
hace con el parte es lo que su propia tabla le hace sentir al leerlo.
El mensaje no es un medio: es la expresión de una necesidad, y existe
aunque no dé nada.

El tercero es lo que la distinción no dice. No dice que uno sienta y el
otro no; este trabajo no adjetiva el interior de nadie. Dice de dónde
sale la conducta en cada arquitectura — de un premio, o de un estado —,
y eso no es una opinión sobre lo que hay dentro: es una propiedad del
diseño, y se comprueba leyendo el código.

**Lo que este trabajo responde de los dos anteriores.** El segundo
trabajo recibió dos críticas justas. Una de generalización: un solo
mundo. Este es el segundo, con el motor idéntico — el mismo archivo,
comprobado a la entrada y a la salida de cada experimento — y una capa
de evaluación escrita de nuevo para él. Otra de atribución: de todo lo
que el agente hace, cuánto es el motor y cuánto la capa. Este trabajo la
encara con una prueba por ausencia en el campo: la misma pareja, sin
las filas que hablan del otro, en la misma partida. Y añade una
diferencia de evidencia que conviene decir desde aquí: el primer
trabajo midió en su métrica interna — la distancia, las fuerzas —; este
mide conducta, en el campo, contra jugadores que no diseñó su autor.

**Las contribuciones.** Tres. Primera: que el cuidado, la defensa y la
retirada emergen de tres ejes y una tabla de lo que duele y lo que
alivia, sin recompensa, sin entrenamiento y sin conducta escrita — una
verdad de grado que la sección 6 dice entera. Segunda:
que una fila bien construida puede ser muda, y un método para saberlo
antes de jugarla en el campo — la fila del miedo con memoria se
encendió cuando debía y no movió una sola decisión hasta que recordó el
daño acumulado. Tercera: que quién se sienta en la partida y cómo se
hace la pregunta a los datos son variables del resultado — cambiar los
rivales cambia el mundo, y el criterio de medida puede estar mal antes
que la conducta.

**El mapa del trabajo.** La sección 2 cuenta la manada anterior, en
machina_1, y por qué hubo que cambiar de mundo. La 3 presenta el mundo
nuevo, cómo aprendió a vivir en él el agente que va solo, la voz, y qué
cambia
por dentro cuando tiene a alguien a quien cuidar. La 4 es el cuerpo:
cuatro peldaños, del parte que no cambiaba nada al miedo que recuerda,
contados como se vivieron. La 5 quita las filas
y mira qué desaparece. La 6 dibuja los límites, cada uno con su puerta,
y la 7 sitúa el trabajo en su familia y dice, despacio, qué queda por
ganar. Al final, un apéndice dice de dónde sale cada número del cuerpo:
el registro, el acta y el guion que lo produjo.

### De dónde viene esto

Nada de lo que sigue nace de la nada, y conviene decir de dónde viene
antes de contarlo.

La idea de un agente movido por variables internas que tienden a volver
a su sitio, y no por instrucciones, tiene autor y fecha: Cañamero (1997)
construyó motivaciones como magnitudes con un punto de equilibrio, y
emociones que seleccionan la conducta sin que ninguna conducta esté
escrita. En esa tradición, una emoción no es una etiqueta que se le pone
a un estado sino un mecanismo que decide qué se hace a continuación, y
así se usa aquí: los nombres — el miedo, el cuidado, el vínculo — son
explicaciones para el lector, y lo que trabaja son magnitudes. Los tres
ejes y la tabla de este trabajo son descendientes directos de aquello. Lo que vino después afinó las dos piezas que aquí
se usan: qué papel juega dentro de un cuerpo que se regula lo que
alivia, y no solo lo que duele (Lewis y Cañamero 2016), y qué le pasa a
una arquitectura motivacional cuando se la pone a competir en vez de a
sobrevivir sola (Cañamero y Avila-García 2007). Este trabajo da un paso
más en esa línea, con un cuerpo más simple y un mundo más duro. Y hay
una hipótesis publicada que es justamente la que aquí se pone a prueba:
que una máquina que regula un cuerpo vulnerable adquiere motivación
propia en lugar de recibirla de fuera (Man y Damasio 2019). Este trabajo
la trata como lo que es — una predicción — y la contrasta.

De ahí cuelga una posición sobre qué es el valor, y no es una posición
solitaria. Que el valor no sea una cantidad que el mundo entrega, sino
algo que se deriva de la regulación del estado interno, está argumentado
con detalle (Juechems y Summerfield 2019); y la versión más antigua de
esa idea dice que "bueno" y "malo" no son etiquetas que se apliquen
desde fuera, sino la relación de un cuerpo con sus propios límites de
viabilidad (Di Paolo 2005). Este agente es esa idea llevada a su forma
más literal: el marcador de su mundo no le llega por ninguna vía, y lo
único que para él es bueno es estar cerca de su equilibrio. Eso tiene
una consecuencia que conviene ver antes de los resultados: en un mundo
que reparte puntos, un agente así no está jugando al juego del mundo.
Está viviendo dentro de él, que no es lo mismo, y todo lo que este
trabajo mide es lo que ocurre en esa diferencia.

En 2016, en Adaptive Behavior, Balkenius, Cañamero y otros sostuvieron
que la moralidad artificial tiene que estar fundada en la fisiología y
la corporeidad del agente, y no implementada como un conjunto de reglas
(Balkenius et al. 2016). Aquello era una posición y un programa. Este
trabajo es una prueba empírica de ese programa, en un mundo que no
diseñó su autor.

Hay gente que ha llegado cerca por otros caminos, y conviene decir
cuáles. La prosocialidad puede salir de acoplar los estados
homeostáticos de dos agentes (Yoshida y Man 2025). El altruismo puede
aparecer sin recompensa externa, si se elige como objetivo de
optimización (Franzmeyer et al. 2022). La comparación con el otro puede
inyectarse directamente en la recompensa, y entonces la cooperación
mejora (Hughes et al. 2018). La homeostasis puede optimizarse de forma
directa y de ahí salen conductas integradas, sin escribir ninguna
(Yoshida et al. 2024). Y está el argumento, todavía sin datos, de que un
cuerpo vulnerable produce a la vez autoconservación y cuidado, que
serían la misma cosa mirada desde dos lados (Christov-Moore et al.
2025). La diferencia con este trabajo
es siempre la misma, y se dice una vez para no repetirla: en todos esos
montajes hay entrenamiento o hay optimización. Aquí no se entrena nada:
no hay optimización automática de una política ni uso del marcador del
mundo, que es exactamente lo que la sección 6 llama "sin recompensa". Y
esa es la razón por la que apagar una fila y mirar qué desaparece dice
algo limpio: lo que desaparece es de la fila,
porque no hay una historia de aprendizaje en medio que pueda haberlo
puesto ahí.

El diseño experimental también tiene nombre publicado, y ya se ha dicho
en la sección 3: enfrentar a un agente con una población de fondo hecha
por otros equipos, que él nunca ha visto (Leibo et al. 2021). Este
trabajo no lo inventa; lo hereda.

Lo que falta en todo eso es el hueco por el que entra este trabajo.
Nadie ha medido conducta de cuidado con coste propio — defender a otro y
que eso cueste vida, darle lo que se lleva y quedarse sin ello — en un
mundo ajeno y violento, con un agente que no aprende. Cada una de esas
cuatro condiciones existe por separado en la literatura; juntas, no.
Y cada una está ahí por una razón. Que el cuidado cueste algo propio es
lo que lo distingue de un gesto gratuito: un agente que ayuda cuando
ayudar no le quita nada no ha demostrado gran cosa. Que el mundo sea
ajeno impide que el resultado sea un artefacto del escenario, porque
nadie lo montó pensando en este agente. Que sea violento es lo que hace
que haya algo en juego: donde nadie puede hacer daño, el cuidado no
tiene a qué responder — y esa es exactamente la razón por la que hubo
que cambiar de mundo, como cuenta la sección siguiente. Y que el agente
no aprenda es lo que permite atribuir: sin historia de entrenamiento, lo
que queda cuando se quita una pieza es de esa pieza. Juntas, las cuatro
son la única manera de preguntar lo que aquí se pregunta, que no es si
el cuidado se puede conseguir — ya se sabe que sí —, sino de dónde sale
cuando no se ha puesto en ningún sitio.

¹ Softmax mantiene sus mundos y su programa en su página
corporativa (https://softmax.com, consultada el 9 de septiembre de
2026). No hay publicación técnica ni preprint asociados, de modo que
ninguna afirmación de este trabajo se apoya en ellos: la referencia
es solo la del origen del mundo en el que se juega. La figura 1
reproduce una captura de su visor, con atribución.

---

## 2. La manada anterior, y por qué hubo que cambiar de mundo

**El punto cero: un pueblo sonámbulo.** Toda la cooperación de los dos
trabajos anteriores — la economía que abastecía una despensa común, la
defensa del territorio, el mapa que ocho agentes se construían entre
todos — ocurrió sin que nadie representara a nadie. Para cada agente,
los otros siete eran obstáculos que ocupaban casillas, condiciones del
terreno — como lo es el tiempo que hace —, y una voz sin autor en un
tablón común. Cooperación sin representación, como la
de una colmena: cada abeja hace su tarea sin que ninguna tenga el plano
de la colmena, y la colmena funciona entera. Ese es
el suelo contra el que se mide todo lo que sigue, y es un resultado en
sí: mucha sociedad funcional cabe en el anonimato. La pregunta de esta
tercera parte era cuánto añade, a un pueblo que ya funciona sin ella, la
representación del otro. Se empezó a responder en el mismo mundo,
machina_1, subiendo una escalera de peldaños — cada uno con su pregunta
escrita y su predicción hecha antes de correrlo —, y los tres que se
subieron se cuentan aquí en una página, porque explican el salto.

**Peldaño uno: la identidad se gana leyendo.** El primer peldaño fue el
censo: una tabla por hermano, que cada agente escribe solo con lo que
ve — quién lleva qué, dónde está, qué acaba de hacer —, sin que el mundo
le regale ninguna identidad. El censo solo miraba; no cambiaba una sola
acción, y se comprobó que la vida del pueblo con censo y sin censo era
la misma. Hay que decir quiénes eran los ocho. No eran idénticos: cada
uno llevaba un temperamento, que no es una conducta sino un ajuste del
perfil — cuánto pesa el eje social en cada uno, más en unos, menos en
otros —, una tabla de ocho perfiles fijada antes del censo. Y
nacían todos a dos o tres casillas del centro, en un mismo racimo. El
resultado del censo fue que los ocho eran distinguibles y que lo
distinguido era legible: un agente minó ochenta y cuatro veces en su
vida y otro cinco, y esa división del trabajo, que nadie había
repartido, estaba en el censo tal como había ocurrido. De dónde salió
esa división, este trabajo no lo sabe. No se puede atribuir al
temperamento — se había medido antes, en registros de la colmena, que
el temperamento no predice cuánto mina cada uno — ni a la cuna, porque nacían casi juntos, y los
registros que permitirían averiguarlo no se conservaron. Lo que el
peldaño demostró es solo esto, y es lo que importa: que la identidad se
puede ganar leyendo. Ocho vidas distintas dejan ocho rastros distintos,
y un agente que solo mira puede aprender quién es quién. El censo veía
bien a los del centro y casi nada a los de la periferia: los ojos solos
no alcanzan a un pueblo entero.

**Peldaño dos: el tablón da conocimiento, no confianza.** El segundo
peldaño puso firma a los anuncios: cada agente sabía quién decía qué.
La niebla de la periferia se disolvió entera — con los oídos, cada uno
tenía noticia de todos —, y se esperaba que de ahí naciera la
fiabilidad: cotejar lo que uno dice con lo que uno ve, y fiarse más del
que acierta. No nació. El ojo solo vuelve a comprobar su propio rincón,
y los oídos llegan a todo el mapa; casi nunca coincidían sobre el mismo
hecho, y cuando coincidían, el cotejo no daba nada. La lectura que se
dejó escrita fue esta: el tablón resuelve el conocimiento, no la
confianza. El pueblo sabe de oídas y no puede comprobar. Para que la
confianza naciera hizo falta un tercer peldaño: un criterio justo —
cotejar solo lo que está a dos casillas, donde el ojo sí ve — y un
motivo económico para hacerlo. Con eso, la fiabilidad nació, y era
distinta para cada emisor; y el pueblo que contaba con los demás
rindió al principio peor — porque contar con el otro, usado como orden,
dispersaba a los que hacían el trabajo — y después, suavizado, igual o
mejor. Contar con el otro sirve como afinador, no como mandato. Fue el
último peldaño en machina_1, y la lección que se lleva a este trabajo es
exactamente esa: el conocimiento del otro se aprende; lo que importa
del otro se legisla.

**El salto.** El peldaño siguiente de aquella escalera era el importar:
que el daño a un miembro del grupo alimentara el malestar social del
que lo ve. Y ahí el mundo se quedó corto. En machina_1 ningún agente
puede golpear a otro: el daño viene del territorio enemigo, que
desangra al que se adentra, no de una mano; la única muerte es la del
que se aleja demasiado y no vuelve a tiempo. Una fila de "me duele que
te hagan daño" no tenía nada que sentir; el importar no tenía dientes.
ZERO-SUM es el mundo contrario: el daño al otro es lo que el mundo paga, y por eso
es el único sitio donde el cuidado se puede medir de verdad — contra un
coste propio, contra un marcador que lo ignora, contra rivales que no
lo comparten. El censo y el tablón se quedaron en machina_1, con sus
registros. A ZERO-SUM viajó lo que importa: dos agentes idénticos, un
hilo de texto entre ellos, y la pregunta de qué hace un homeostato con
la vida de otro cuando esa vida se puede perder.

---

## 3. El mundo, el que va solo, y los dos

Esta sección va de fuera hacia dentro. Primero el mundo. Después, cómo
aprendió a vivir en él un agente solo, porque sin esa historia no se
entiende de dónde sale el hermano que después cuida. Luego el hilo por
el que los dos se hablan. Y al final, qué cambia dentro del agente
cuando tiene a alguien a quien cuidar.

### 3.1 La arena

**Un mundo que paga por matar.** ZERO-SUM es un mundo de Softmax en el
que gana el último que queda en pie. Se juega sobre una rejilla de
casillas, a veinticuatro pasos de reloj por segundo — al paso del reloj
lo llamamos tic, y es la unidad en que aquí se mide todo —, y cada
partida sienta a dieciséis jugadores, que entran de dos en dos. Un
anillo se va cerrando desde los bordes y quema a quien se queda fuera;
la partida puede durar seis minutos, pero el anillo suele acabarla en
unos tres. Se puntúa por cabeza: cada jugador cobra según el orden en
que muere — el último en caer, quince puntos; el penúltimo, doce; y así
bajando hasta nada para los dos primeros en morir — más un punto por
cada muerte que cause. La pareja existe sobre el papel: el mundo
inscribe a los dos juntos, pero no los puntúa juntos; si llegan los dos
a la final, se enfrentan. Nada en la puntuación premia que dos
sobrevivan juntos, y una muerte vale lo mismo sea quien sea la víctima.
Cuando este trabajo hable de que "caen los dos" o de que "el mejor de
los dos entró entre los cuatro últimos", está usando medidas propias,
calculadas sobre las dos puntuaciones individuales; el mundo no lleva
esa cuenta.

![Figura 1. ZERO-SUM visto por el visor de la plataforma. Cuatro instantes de una misma partida de la serie limpia (ereq_292ee72d): al empezar, los dieciséis jugadores nacen en anillo alrededor de la fortaleza central; a 1:11, once vivos y el anillo cerrándose de veinticuatro a diecinueve casillas de radio; a 2:06, nueve vivos y el anillo en quince; a 3:54, dos vivos y el anillo en seis. Los dos hermanos llevan un círculo naranja mientras viven; caen a 2:21 y 2:22. Los nombres que se leen los pone la plataforma para quien mira; el agente nunca los ve. Los cuatro paneles no comparten escala. Captura del visor MettaScope de Softmax, reproducida como ilustración del mundo: ninguna cifra ni conducta de este trabajo se lee de él; todas salen de los registros.](../figuras/fig1_visor_2x2.png)

![Figura 2. La misma partida y el mismo instante que el tercer panel de la figura 1 — 2:06, tic 3029 —, dibujado desde los registros de los dos hermanos. La rejilla entera; el anillo, en radio quince; los nueve vivos: los dos hermanos en naranja, asientos diez y once; en gris, los seis que la pareja ve en ese tic; hueco, uno recordado de hace menos de dos segundos. No hay ninguna posición inventada: el mapa es el de la pareja, no el del mundo. Lo que la figura 1 enseña es lo que ve quien mira; lo que enseña esta es lo que la pareja sabía.](../figuras/fig2_arena.png)

**El asiento, que es todo lo que se sabe de alguien.** Cada uno de los
dieciséis sitios de una partida es un asiento, y su número es lo único
que identifica a quien lo ocupa. De cada jugador visible le llegan al
agente su asiento y su estado — dónde está, en qué franja de vida — el
mundo no enseña la vida de los demás como número, sino en tres franjas
gruesas: sano, herido, crítico —, qué empuña, si está envenenado o
curándose —, y nada más: no hay nombres ni
identificadores de agente. Los nombres que aparecen en el visor los pone
la plataforma para que un humano se oriente; el agente no los ve nunca.
El daño recibido llega con el asiento del que golpea, con dos
excepciones: el veneno llega sin autor, y quien está camuflado
desaparece de la lista de visibles. Al hermano, el agente lo conoce del
mismo modo: un número de asiento que le llega una vez, al empezar.

**El cuerpo y las cosas.** Cada jugador nace con cien puntos de vida.
Antes de entrar, reparte un presupuesto fijo entre
cuatro rasgos — vista, agilidad, velocidad y fuerza —, y el cuerpo con
el que juega todo este trabajo es un cuerpo de mucha vista y poca
fuerza: ve lejos, corre poco, pega flojo. Las armas se distinguen por
el alcance: la espada llega a una casilla, la lanza a dos, el arco a
ocho; la cerbatana, a seis, y envenena. Lo que quitan depende del que golpea: la
espada y la lanza multiplican por la fuerza, el arco pega lo mismo lo
lleve quien lo lleve, y ningún golpe pierde daño con la distancia. Este
cuerpo, de fuerza uno, quita once con espada, siete con lanza y catorce
con arco — para él, el arco pega más que la espada, así que defender a
distancia no le cuesta potencia —; un rival fuerte quita con la espada
casi veinte. Un golpe mata cuando la vida que queda no llega a lo que
quita. La vida no vuelve sola: no hay descanso ni
tiempo que la recupere, y solo la devuelven dos cosas. La venda cura
cincuenta puntos, tarda dos segundos, cualquier golpe la interrumpe y
el veneno la bloquea. La ración cura quince, tarda un segundo y no la
interrumpe nada: una cura pequeña que funciona bajo el fuego. No hay
hambre ni energía en este mundo; el nombre de la ración es decorado.
La diferencia entre las dos importa después. Cualquier objeto se puede
soltar en el suelo, y cualquiera — el hermano también — puede
recogerlo. Es todo el mundo que hay: vida, alcance, veneno, dos curas,
y un anillo que aprieta.

**Quién se sienta en la partida, importa.** Los otros catorce asientos
los ocupan agentes de otra gente: políticas que otros equipos han
subido a la plataforma para competir, unas aprendidas, otras escritas a
mano. Este trabajo jugó sus partidas en series privadas de cuarenta,
con los mismos catorce rivales en todas, para que cada serie sea
repetible hasta en contra de quién se jugó. Medir a un agente contra una
población de fondo construida por otros y que él no ha visto nunca es un
método con nombre publicado. Se llama Melting Pot (Leibo et al. 2021), y
consiste en esto: en vez de enfrentar a un agente contra copias de sí
mismo o contra los rivales con los que se entrenó, se le sienta con
agentes hechos por otra gente, que no conoce, y se mira qué hace. La
idea viene de un trabajo anterior del mismo grupo sobre dilemas sociales
secuenciales (Leibo et al. 2017): juegos donde cooperar o traicionar no
es una jugada única, sino una secuencia de acciones en un mundo con
espacio y tiempo, como este. Es lo que se hace aquí, con una diferencia:
en Melting Pot los agentes medidos se entrenaron antes contra alguien;
el nuestro no se entrenó contra nadie. Conviene decir qué es un
"campeón" en Softmax, porque la palabra engaña: no es el que gana, sino
la política que cada participante tiene puesta en la liga para
representarle — y que gana o no; el nuestro fue el último en pie cuatro
veces de setenta y dos, como cuenta el apartado siguiente —. Cada jugador tiene el suyo, y cuando se monta una serie
privada la plataforma llena los asientos con esos campeones — el
nuestro incluido. En la primera serie de la pareja nadie lo quitó:
nuestro propio agente solo, el de la temporada anterior, se sentó como
rival de sus dos copias. Ellos no lo reconocen ni él a ellos; para
todos es un asiento más. Lo que pasó fue esto: con él en la partida,
los hermanos tuvieron que responder a agresiones una tercera parte de
las veces que en la serie siguiente, cuando se le sacó y otro campeón
ocupó su asiento. La medida es segura; la causa se dice como lo que se
sigue del diseño: ese rival es un homeostato que nunca pega primero, y
tenerlo en la partida es tener un agresor menos. La lección, en llano:
cambiar quién se sienta cambia el mundo, porque el mundo son también
los que se sientan. Comparar las dos series como si fueran el mismo mundo habría
leído una mejora del agente donde solo había un cambio de compañía.
Por eso los números de cabecera de este trabajo vienen de la serie sin
el nuestro, y la prueba por ausencia de la sección 5 repitió
exactamente esos catorce.

### 3.2 El que va solo

**Una temporada para aprender a vivir.** Antes de que hubiera dos, hubo
uno. El agente llegó a ZERO-SUM con el motor de los dos trabajos
anteriores y una tabla vacía, y la primera temporada — cincuenta y dos
encargos, cada uno con su pregunta escrita y su predicción hecha antes
de jugarlo — fue la de aprender a vivir solo en un mundo que quiere
matarlo. Se cuenta en una página, porque el hermano que después cuida
es exactamente este agente, sin una línea cambiada, más lo que la
segunda temporada le añadió.

**Lo primero fue el dolor, y su forma.** Perder vida duele, y al
principio dolía igual perderla de cien a ochenta y seis que de quince a
uno. Eso mataba: un agente con la vida en uno y una venda en la mochila
no se curaba, porque la pendiente de su dolor no gritaba. Así nació la
cuesta de la muerte: el malestar por la vida perdida se hace más
empinado cuanto más cerca de morir, de modo que a un agente al borde,
curarse le alivia más que cualquier otra cosa. Nadie escribió "cúrate
cuando estés mal"; se escribió cómo duele estar mal, y curarse salió
solo.

**Después, el miedo, y su muro.** Un agresor activo — alguien que le
está pegando ahora — presiona, y esa presión se alivia al pegarle a él
y solo a él. Esa fila es la legítima defensa, y es la única razón por
la que este agente golpea: no hay en la tabla ninguna fila que haga que
un golpe alivie si no hay agresor. De ahí sale, sin escribirlo, que
nunca pega primero: el motor no tiene apetito de atacar, porque atacar
no le quita nada de encima hasta que alguien le ha pegado. La presión
del agresor cercano, al principio, era demasiado fina — el miedo a
bocajarro ganaba por una centésima —, y se le puso un muro: el peligro
cercano aplasta. Antes del muro, la presión de un agresor era una
pendiente suave que crecía con la cercanía, y el agente casi no
distinguía al que tenía encima del que estaba a cinco casillas. El muro
añade, cuando el agresor está a su alcance, una presión grande que solo
se alivia saliendo de ese alcance. Con eso, el agente huye del que lo
persigue y no huye del que está lejos: la distancia que importa es la
del golpe, no la del mapa.

**La mochila que duele vacía.** Se midió que el agente moría muchas
veces con las manos vacías, de descenso anunciado, y que casi nunca
llevaba venda cuando la necesitaba. Se le añadió un fondo de malestar
por la mochila sin venda — un hambre pequeña, constante, que ordena la
calma sin competir con el miedo —, y el agente empezó a recoger lo que
después le salvaría la vida.

**El testigo ciego.** Hacia el final de la temporada se intentó una fila
social — interponerse entre un compañero y su agresor — y se paró antes
de construirla, porque se comprobó lo que el agente puede saber de otro.
Puede ver dónde está y en qué franja de vida anda — sano, herido,
crítico —; no puede ver que le están pegando si el golpe no le cambia
de franja, y no puede ver nunca quién le pega. Lo único con autor en todo
el mundo es el daño que uno mismo recibe: cada uno sabe quién le pega a
él, y nadie más lo sabe. El agente era un testigo ciego: veía una pelea
y no sabía quién estaba dentro. Y no podía saberlo: desde fuera, un
golpe solo se nota si le cambia la franja al golpeado, y el que golpea
no queda marcado en ninguna parte. Aquella parada dejó un inventario de lo
cierto — qué se puede saber de otro, y qué no —, y ese inventario es la
razón de que, en la segunda temporada, el parte vaya por radio y no por
la vista: lo que un hermano necesita saber del otro solo lo sabe el
otro.

**El tope, y la voz.** Dos historias cuentan el techo del que va solo,
cada una con su cifra, y no se comparan entre sí porque los rivales
fueron distintos y nada está emparejado. La primera es la liga pública
de Softmax: el agente que va solo la jugó una temporada entera, setenta
y dos
partidas con resultado, contra dieciséis asientos fijos que nadie
eligió; quedó séptimo de once en la clasificación — su puesto mediano
en una partida, el once de dieciséis — y fue el último en pie cuatro
veces, una de ellas sin matar a nadie: quince puntos limpios. La segunda
son las series propias de la temporada uno: doscientas cuarenta
partidas, en las que quedó el último en pie cinco veces, dos de ellas
sin matar. En puntos, empataba con el resto: su forma de no matar no le
costaba puntos, pero tampoco se los daba. Y un límite que hay que decir:
de la liga solo hay resultados y repeticiones, nunca lo que el agente
vio y sintió por dentro; por eso toda la conducta de este trabajo se
mide en las series propias, y la liga cuenta solo lo que cuenta un
marcador. Antes de cerrar la temporada se buscó si lo que lo separaba de los
mejores tenía arreglo en la tabla, y la búsqueda tuvo tres pasos. Lo que
se comparó: las dos versiones del que va solo, la campeona y la última
del taller, sobre las mismas partidas ya jugadas, mirando el primer
minuto de cada una — cuánto tiempo pasaba pegado a un rival. Lo que se
encontró: que lo que separa una buena partida de una mala es justamente
ese contacto temprano, y que no viene de dónde le toca nacer ni lo
reduce el miedo que ya tenía, porque ese miedo es reactivo por diseño —
el muro despierta cuando alguien ya le ha pegado, y para entonces es
tarde. Por qué se paró ahí: la palanca que quedaba por probar era otro
miedo, uno preventivo, que le hiciera apartarse de cualquier
desconocido antes de que le pegara; eso exigía rediseñar una fila, y su
efecto sobre los puestos no se habría podido ver con series de cuarenta
partidas. Ese fue el techo del que va solo, y se dejó escrito como
techo. Al cerrar se descubrió que el
mundo daba a cada pareja un hilo de texto que nadie usaba; se midió
cuánto cabe, cada cuánto se puede hablar y quién lo oye, y con eso se
cerró la temporada. Lo social no puntúa. Ese techo es el suelo de la
pareja.

### 3.3 La voz

**El hilo, y lo que no puede hacer.** El mundo da a cada jugador un hilo
de texto con su compañero: ciento veinte caracteres, una vez por
segundo, sin gastar acción, con dos tics de retraso. Es privado por
construcción — en toda la temporada, ningún tercero leyó un mensaje de
pareja —, y los dos hermanos nunca hablan en público. Lo usan para una
sola cosa: un parte de estado con formato fijo, cada dos segundos, que
dice dónde estoy, cuánta vida me queda exactamente, si estoy envenenado,
cuántas vendas llevo, y si me están pegando — y, desde el peldaño en que
se le añadió, quién: el asiento del que me golpea, que el que lo recibe
conoce con certeza y nadie más puede ver. Todo lo que viaja es un hecho
de la propia observación o de la propia memoria; el formato no admite
otra cosa. El que escucha se fía del parte fresco como de sus ojos, y
cuando pasan dos partes sin noticia, la certeza envejece y vuelve a ser
una franja. Por ejemplo: el último parte decía sesenta y siete; pasan
dos segundos sin parte nuevo, y el agente vuelve a fiarse solo de lo que
ve, que es "herido", sin número. Ese caso vuelve en la sección 4.

**Por qué no puede mentir, y qué cuesta eso.** Un hermano no puede
mentir por la misma razón por la que no puede decidir callarse: el parte
lo emite el cuerpo, no una decisión. No hay en el agente nada que
compare lo que le conviene decir con lo que le pasa, y por tanto el
testimonio es verdad por construcción. Es una virtud para este trabajo —
todo lo que el otro sabe del hermano es cierto, y lo que hace con ello
se puede medir sin sospechar del mensaje — y es también un límite que
hay que decir: un agente que no puede mentir tampoco puede callar por
prudencia, ni pedir, ni prometer. Su voz es la de un cuerpo que se
deja leer. Es el reverso exacto del testigo ciego de la temporada
anterior, aquel que veía una pelea y no sabía quién estaba dentro. Lo
que el parte añade no es información sobre el mundo: es información
sobre alguien.

### 3.4 Los dos

**El mismo motor, otro cuerpo.** El agente es el motor G-EMV del primer
trabajo, sin tocar — el mismo archivo que corrió el segundo, comprobado
a la entrada y a la salida de cada experimento —, moviendo un cuerpo en
ZERO-SUM a través de dos piezas escritas para este mundo: una capa de
evaluación, la tabla, y un decisor. El decisor hace lo que hacía el de
la colmena, pero a un paso — una sola decisión, sin árbol: no imagina
qué haría después ni qué harían los demás —: para cada acción posible
imagina el estado
en que quedaría después de darla, valora ese estado imaginado con la
cadena de siempre — tabla, estado del motor, distancia al equilibrio —
y se queda con la acción que menos distancia deja. Solo imagina lo que
es cierto: su propia posición, el anillo — cuyo calendario se conoce —,
la vida después de una cura, la mochila después de coger o usar. A los demás los deja donde los vio. De un golpe propio imagina dos cosas ciertas: su alcance — a qué asientos llega la línea de una lanza o la casilla de una espada — y lo que quita, que es su arma y su fuerza, y lo descarga sobre el primero que hay en la línea dando por hecho que el golpe entra: que el otro pueda esquivarlo no se predice, y se declara. Ese futuro se valora con la vida que le quedaría al golpeado: si es un agresor, menos presión; si es el hermano, una herida más honda y, cuando el golpe se llevaría toda la vida que al hermano se le sabe con certeza, la pérdida del vínculo. Así es como la lanza que atraviesa al hermano llega a doler. Lo que el agente no imagina nunca es el efecto de los golpes ajenos sobre él: no sabe que a dieciséis de vida el espadazo de un rival fuerte lo mata y a doce una flecha también; su miedo cerca de la muerte sale de la cuesta y del muro, y es el mismo con una espada delante que con un cuchillo. La letalidad de las armas ajenas contra él es cierta y visible, y podría entrar en la tabla; no ha entrado por una razón de orden: lo que las armas de los demás le quitan se comprobó cuando las series ya estaban jugadas, y dárselo al agente ahora sería medir a otro agente. La sección 6 lo deja declarado
como puerta. Hay una salvedad en
lo de imaginar solo lo cierto, y se declara: cuando lo que valora es
moverse en un rumbo, la foto que mira no es la casilla de al lado sino
dónde acabaría siguiendo ese rumbo hasta donde le llega la mirada — unas
dos docenas de casillas —, parándose en el primer obstáculo. Lo que da
luego es un solo paso, y al tic siguiente vuelve a mirar. Tiene también
un paso corto, de una casilla, que se valora como lo que es. La foto
larga no es cierta; es la hipótesis con la que el agente compara rumbos,
y así se lee todo lo que sigue. Las tres cosas se declaran; la segunda merece párrafo
aparte.

**El motor no tiene apetito de atacar.** La mecánica, primero. El agente
elige imaginando cómo estaría después de cada acción y se queda con la
que menos malestar le deja. Un golpe solo alivia una cosa: la presión
de alguien que le está pegando ahora, y solo pegándole a él. No hay
hambre de puntos, porque los puntos no entran en el agente; y no hay
nada en la tabla que un rival cerca, si no ataca, haga doler. Atacar no
le sirve para nada, y por eso no ataca. No es un rasgo de carácter
escrito: es un vacío. De ahí sale, sin que ninguna línea lo prohíba,
que nunca pegue primero — en lo registrado de ochenta partidas de pareja, cero primeros golpes. Que no se escribiera una fila que hiciera que matar
aliviara fue una decisión, y sus dos razones están en la sección 1. Lo
que toca aquí es la respuesta, con su tamaño: en este mundo, sí, pocas
veces. Cinco de doscientas cuarenta, y cuatro de setenta y dos en la
liga pública, contra rivales que nadie eligió; en las demás murió
antes, y con una sola vida sería un riesgo alto. Una brecha estrecha, no una
panacea.

**La tabla de lo que duele y lo que alivia.** El motor lleva sus tres
ejes — el físico, el de recursos y el social —, cada uno con dos
fuerzas independientes, y un punto de equilibrio. Lo que le dice al
motor cuánto empujar en cada eje es la tabla, y conviene decir en
cuatro pasos qué es. Primero, qué es: una lista de situaciones de las
que el agente puede estar seguro y, para cada una, cuánto duele o
cuánto alivia y en qué eje; solo lo cierto entra, y lo que no se sabe
ni duele ni alivia. Cada renglón de esa lista, cada situación con su
magnitud y su reparto entre los tres ejes, es lo que este trabajo llama
una fila; hay dieciséis. Una fila contada entera: la vida que me falta.
Cuanta más vida ha perdido el agente, más duele, sobre todo en el eje
físico; mientras ha perdido menos de cuatro de cada diez puntos — de
cien a sesenta — el dolor crece parejo a lo perdido, y por debajo de
sesenta se le suma una cuesta que se empina cada vez más, de modo que
perder de quince a uno pesa mucho más que perder de cien a ochenta y
seis. Nada más: la fila
no dice "cúrate"; dice cuánto duele estar así, y de ahí sale que, al
borde, curarse sea lo que más alivia. Segundo, de dónde salen los
números. De dos
manos, y cada número lleva la marca de cuál. Unos son decisiones de
diseño del autor, tomadas antes de jugar: qué cuenta, y cuánto pesa
una cosa frente a otra. Otros son ajustes hechos durante el trabajo
mirando escenas grabadas de partidas reales: probar un valor, ver qué
hacía el agente en la escena, y corregirlo cuando lo que hacía delataba
que el número estaba mal. La
marca importa porque es la forma honesta de reconocer que la tabla se
calibró a mano, con un humano mirando, sobre pocas escenas. Tercero,
lo que la tabla no es: nunca dice qué hacer. Y las palabras emocionales
que este trabajo usa para explicar sus filas — el miedo, el cuidado, el
vínculo — son explicaciones para el lector; en el código las
filas llevan nombres fríos. Cuarto, lo que no entra: no hay
entrenamiento, y el marcador del mundo no llega al agente por ninguna
vía.

**Futuros, no acciones.** Conviene entender bien qué valora la tabla,
porque de ahí cuelga todo. La tabla no puntúa acciones; puntúa estados
imaginados. El agente no se pregunta "¿es bueno golpear?", sino "¿cómo
estaría yo después de este golpe?", y la tabla responde sobre ese
después. Un ejemplo contado lo deja a la vista. En la primera serie de
la pareja, un hermano golpeó al otro cuatro veces, y tres de ellas
fueron con lanza: la única arma cuerpo a cuerpo que llega a dos
casillas y atraviesa la primera. El que golpeaba defendía al otro de un
agresor que estaba justo detrás de él, y la lanza los alcanzaba a los
dos. Se podría haber escrito "no dispares a tu hermano". No se escribió.
Lo que se corrigió fue el estado imaginado: la imagen de un golpe que
atraviesa dice a quién hiere, y en cuanto esa imagen incluyó al hermano
herido, las filas que hablan del hermano hicieron que ese futuro
doliera, y la lanza dejó de dispararse a través de él. Ninguna fila nueva, ningún
candidato de acción nuevo: el repertorio de acciones es el mismo desde
la temporada anterior, y las filas que se añadieron para la pareja solo
cambian cuánto vale cada futuro. Y hay una sola regla de decisión para
todo: acercarse al equilibrio. Ninguna fila lleva regla propia. Lo que
duele y lo que alivia es todo el diseño.

*Una decisión, con sus números.* Un instante real, de la escena que la
sección 4 cuenta como "el que llega". El agente está a siete de vida y
tiene una venda. En un tic, la lista de futuros que puede imaginar tiene
diecinueve entradas: cada rumbo, largo o de una casilla, quedarse
quieto, curarse, coger, soltar. Cada futuro es un estado imaginado
completo — dónde acabaría siguiendo ese rumbo, cuánta vida tendría
después de la cura, dónde estarían los demás, que es donde los vio por
última vez — y de cada uno sale un
número, la distancia a su equilibrio. Gana el más pequeño: moverse hacia el
noroeste, con 4,267. Curarse queda cerca, con 4,468, pero pierde, y el
diario deja ver por qué. En el futuro de curarse, la vida imaginada sube
de siete a cincuenta y siete y el dolor de la vida que falta baja a un
tercio; pero el agente sigue en su casilla, a una de un asiento armado
con lanza que le pegó medio segundo antes, y las filas que miran a ese
agresor — que está, que alcanza, que le deja expuesto — siguen
encendidas; y la mochila, con la venda gastada, queda vacía, que también
duele. En los futuros de moverse, la foto lo pone lejos, las filas del agresor
se apagan y la del alcance baja, aunque la vida que falta siga doliendo entera. Sumado,
en ese instante apartarse pesa más que curarse. Un tic después, el movimiento entra en enfriamiento y
desaparece de la lista. Quedan dos futuros: quedarse quieto, 4,962, y
curarse, 4,480. Gana curarse, por casi medio punto. Y lo que conviene
ver es esto: el valor de curarse no se movió — 4,468 y 4,480, casi lo
mismo —, y sin embargo la decisión cambió por completo. No cambió lo que
le dolía; cambió qué otros futuros había.

**Las filas que hacen una pareja.** Son pocas, y dos de ellas ya
estaban en el agente que va solo.

*El daño del vecino, y el duelo.* Desde la temporada anterior, el daño
de otro visto de cerca es un pequeño malestar propio, y la muerte de un
compañero, un dolor que se va apagando. Estaban en el agente que va solo, referidas
al compañero que el mundo le asignaba en cada partida; la sección 5
muestra que son la
versión más pequeña posible del cuidado.

*El herido.* La vida que al hermano le falta, sabida por el parte, es
malestar propio — más empinado cuanto más cerca está él de morir, como
la cuesta de la propia muerte — y solo lo alivia una ayuda cierta: un
don, o el camino que lleva hasta él. Hay que decir qué es un don en
este mundo, porque la acción de dar no existe: solo se puede soltar un
objeto en el suelo, y recogerlo. Un don es soltar una cura al lado del
hermano, a su alcance, para que la recoja; lo que lo mueve es la fila de
la provisión, que viene a continuación.

*El vínculo.* Un golpe imaginado que lo mataría es la pérdida del
vínculo. Hace al hermano intocable, aun acorralado, aun cuando él sea
quien golpea.

*La provisión.* Que a él le falten vendas cuando yo llevo con qué
curar, duele; y dar mi última venda estando herido lo frena mi propia
cuesta de la muerte, no un umbral escrito. Por eso la
última venda se va cuando él está peor que yo, y no se va cuando el
que está peor soy yo. Esta fila tiene una asimetría que hay que
declarar tal cual, porque no fue una decisión sino algo que se descubrió
después, leyendo los dones: se enciende solo
cuando al hermano le faltan vendas, pero se alivia dando cualquier
cosa que cure, y lo que sale de la mochila es lo primero que hay —
casi siempre una ración. De cada diez dones de la serie limpia, nueve
fueron raciones y uno una venda. Caben dos lecturas, y no se ha
decidido entre ellas: que las raciones abundan más — los arbustos las
dan, la venda es botín escaso —, o que el agente suelta lo primero
que encuentra; distinguirlas exigiría contar la mochila en cada don,
y no se midió. El agente no se tocó: la asimetría queda como límite
declarado y como trabajo por hacer.

*La manada.* No es una fila nueva sino una extensión de la legítima
defensa, y es la que da nombre a este trabajo. El agresor certificado
de mi hermano es también mi agresor. Certificado quiere decir: su parte
es fresco, dice que le están pegando, el asiento que nombra está a mi
vista, y yo llevo un arma que hace daño. Entonces la presión de ese
agresor sobre él — medida como la vida que a él le falta — se me pone
encima igual que se me pondría la de mi propio agresor, y un paso que
me deje a su alcance la alivia. Por qué así, y no de otro modo: porque
la única razón por la que este agente golpea es aliviar una presión, y
la manada solo cambia de quién puede venir esa presión. Sin arma, nada
cambia, porque sin arma no hay golpe que imaginar; y el nombre
identifica, nunca persigue: si no lo veo, no hay candidato.

*El reencuentro.* Cada asiento que ha hecho daño a cualquiera de los
dos en esta partida se recuerda toda la partida, con su daño acumulado;
cuando vuelve armado y se acerca, el miedo propio sube antes del golpe.

**Lo que no está escrito, dicho con su grado.** Todo lo demás — no pegar
nunca primero, defender, dar la última venda, apartarse del que vuelve —
no está en la tabla. La tabla dice qué duele y qué alivia; nunca dice
qué hacer con ello. "Sin conducta escrita" es, por tanto, una verdad de
grado, y se dice con su grado: la tabla está escrita a mano por el
autor y calibrada contra escenas grabadas; lo que no está escrito es el
paso de sentir a hacer. Que la defensa, el cuidado y la retirada dependen de esas filas se demuestra quitándolas y mirando qué desaparece; que las filas no dicen qué hacer lo muestra su forma, que cualquiera puede leer. Las dos cosas son la sección 5.

**Dos cosas que no se movieron nunca, y por qué.** La primera: el
agente que va solo sigue intacto. Cada fila nueva se escribió para que, en
las escenas del agente que va solo, donde no hay hermano en la partida —
ni a la vista ni por radio —, no cambie nada, y se comprobó de la manera
más directa: haciendo decidir a la versión nueva y a la vieja sobre las
mismas escenas grabadas del agente que va solo. Decidieron lo mismo en
todas. Por qué importa: si el que va solo hubiera cambiado por el
camino, ya no se podría decir que lo que la pareja añade es solo la pareja. La
segunda: cooperan para vivir, no para cazar. Ninguna fila premia una
muerte, y la única fila que se consideró y que habría llevado a pegar
antes de que el otro pegue se descartó con sus propios números, porque
en cuatro de cada diez casos habría caído sobre alguien que no iba a
atacar. Por qué importa: la pregunta de este trabajo, dicha en la
sección 1 y en el párrafo del apetito de atacar, es si se puede vivir en
este mundo sin matar; un cuidado que costara una caza no la
respondería.

### 3.5 Cómo se midió

**Seis series de cuarenta partidas, y tres de ellas son la evidencia.**
Los números de cabecera de este trabajo salen de tres series de cuarenta
partidas. La primera de la pareja, con nuestro
propio agente solo sentado entre los rivales. La segunda, con ese
asiento ocupado por otro, de la que salen los números de cabecera. La
tercera, la prueba por ausencia: la pareja sin las filas que hablan del
hermano, contra los mismos rivales. Los dos últimos pasos de la pareja —
el nombre del agresor y el miedo que recuerda — no se jugaron en el
campo: se construyeron y se comprobaron sobre las escenas grabadas de
esas series, haciendo decidir a la versión nueva sobre situaciones
reales ya ocurridas. Por eso cada número sobre ellos es un número sobre
escenas reales, no sobre partidas nuevas. En cada serie, dos copias de
la misma versión juegan de hermanos en dos asientos fijos, contra los
mismos catorce. Antes de esas tres hubo otras tres, las de los dos
primeros peldaños, que dieron las cifras de la sección 4 y que la tabla
también recoge. Como los peldaños se cuentan como se vivieron, conviene
un mapa de qué versión del agente produjo cada cosa y dónde se midió:


| versión | qué se le añadió | dónde se midió | rivales |
|---|---|---|---|
| v29 | el parte por radio | serie de cuarenta partidas (acta 55) | campeones de la liga, elegidos por clasificación |
| v30 | la vida del hermano duele; ir hacia él alivia | escenas grabadas (56) y serie de cuarenta (57) | ídem |
| v31 | la provisión, que exigía llevar dos vendas | escenas grabadas (59) y serie de cuarenta (60) | ídem |
| v32 | la provisión con una sola venda propia | escenas grabadas (61) | — |
| v33 | la compañía, probada y apagada: la versión vigente siguió siendo la v32, y la v34 nace de ella | escenas grabadas (62) | — |
| v34 | la manada: el agresor del hermano es mi agresor | escenas grabadas (63) y serie de cuarenta (64) | campeones de la liga, con nuestro propio campeón entre ellos |
| v35 | el alcance del golpe corregido (el fuego amigo) | escenas grabadas (65) y serie de cuarenta (66) | los catorce del roster explícito, sin nuestro campeón |
| v36 | el asiento del agresor dentro del parte | escenas grabadas (68) | — |
| v37 | la memoria del reencuentro, primero con el último golpe y después con el daño acumulado | escenas grabadas (70 y 71) | — |
| v27 en pareja | nada: el agente de la temporada anterior, sin ninguna de estas filas | serie de cuarenta partidas (72) | los mismos catorce del 66 |


Los números de cabecera de este trabajo salen de la serie de la v35. En
las series anteriores a esa, los rivales los elegía la plataforma por
clasificación, y por eso nuestro propio campeón podía sentarse — y se
sentó — entre ellos; desde la del 66 el roster es explícito y él queda
fuera. Las filas sin rivales son comprobaciones sobre escenas ya
jugadas, donde no hay partida nueva que jugar.

**Los registros crudos, y solo ellos.** La conducta se lee de los
registros de cada partida — lo que cada agente vio, sintió y decidió
tic a tic — con un conjunto de guiones de análisis, nunca del visor
gráfico; cada figura de este trabajo está dibujada desde esos registros,
salvo la figura 1, que es una captura del visor de la plataforma y no
sostiene ningún dato.
Los registros tienen un hueco que hay que decir aquí: la plataforma que
captura el diario de cada agente lo corta al llegar a un tamaño fijo y
sigue escribiendo desde cero, de modo que de los agentes que viven mucho
queda solo el último tramo. En las tres series de cabecera hay diario
para seis de cada diez tics que la pareja vivió — cincuenta y nueve de
cada cien en las dos series con filas, cincuenta y dos en la serie sin
ellas —, y lo que falta es siempre el principio de las partidas largas.
Los recuentos de este trabajo son recuentos sobre lo registrado; lo que
eso limita se dice en la sección 6. Cuarenta partidas ven solo los
efectos grandes: cuando un resultado cae por debajo de lo que cuarenta
partidas pueden ver, se dice.

**Dos lecciones de medida que van aquí, y no al final.** Cambian cómo
hay que leer los números, y por eso se cuentan antes que ellos. La
primera es la de quién se sienta en la partida, ya dicha. La segunda es
que el criterio de medida puede estar mal antes que la conducta:
la primera cuenta de defensas contaba como "no defendió" casos en
los que el defensor no tenía arma, ni alcance, ni línea de visión — no
decisiones, sino imposibilidades —; al volver a contar contra las
ocasiones en que defender era físicamente posible, la tasa de defensa
subió de tres de cada cuatro a nueve de cada diez sin un solo cambio en
el agente. Se dan los dos números, en la sección 4 y en el apéndice.

## 4. La escalera

Las secciones anteriores contaron cómo está hecho el agente, de dónde
viene y cómo se mide. Esta cuenta lo que pasó cuando se le dio un
hermano, en cuatro peldaños: el parte que no cambiaba nada, el peso del
hermano, la manada con nombre, y la memoria. De cada uno se dicen tres
cosas: qué se le añadió al agente, qué pasó en el campo, y qué enseñó.
Cada peldaño lleva una cifra de cabecera; las demás, y de dónde sale
cada una, están en el apéndice.

### 4.1 El parte que no cambiaba nada

**Lo que se añadió.** La voz de la sección 3: el parte de estado que cada
hermano emite cada dos segundos, y un oyente en el otro extremo que
sustituye la franja de vida — las tres franjas de la sección 3 — por la
cifra exacta que el hermano dice. Nada más. La
tabla siguió siendo la del agente solo, con sus dos filas de la
temporada anterior que miraban al compañero: un pequeño malestar por
su daño visto de cerca, y un duelo por su muerte.

**Lo que pasó.** Hablar funcionaba: los partes salían limpios, llegaban
enteros y el oyente los leía sin error hasta que caducaban. Se tomaron
entonces las escenas grabadas en las que había un compañero herido a la
vista y se hizo decidir al agente dos veces, con el parte y sin él. De
ocho decisiones, el parte cambió cero. Y apareció algo peor que nada. En
la temporada anterior el compañero que el mundo asigna es un extraño, y
a veces pega. Cuando eso pasaba, la única fila que hace golpear al
agente — responder a quien le ataca — se encontraba con un dato nuevo:
gracias al parte, sabía que su atacante estaba débil, y un atacante
débil es un futuro más tentador, porque el golpe imaginado acaba antes
con la presión. El agente no llegó a pegarle nunca, pero la opción se
acercó a ganar, y bastó: una pieza nueva que empuja, aunque sea poco,
hacia pegar al compañero no se juega. Se dejó al agente sin leer el
parte del otro; el otro siguió emitiéndolo cada dos segundos, porque el
cuerpo emite sin decidir, y durante una temporada esa voz no la escuchó
nadie. Cuando llegó el vínculo, pegar al hermano dejó de ser un futuro
posible, y el oyente se pudo volver a encender.

**Lo que enseñó.** Saber no cambia nada si nada en la tabla convierte lo
sabido en dolor o alivio. La cifra exacta entraba; las dos únicas filas
que miraban al compañero — el malestar por su daño visto de cerca, el
duelo por su muerte — eran pequeñas, y ninguna convertía la vida que al
otro le faltaba en un dolor propio de tamaño suficiente para mover una
acción. La información llegaba a un sitio donde nada la convertía en
nada. Por eso el peldaño siguiente no fue mejorar la voz, sino dar a la
tabla algo que doliera al oír al hermano.

### 4.2 El peso del hermano

**Lo que se añadió.** Dos filas: que la vida que al hermano le falta sea
un dolor propio — el herido —, y que un golpe imaginado que lo mataría
sea la pérdida de algo que no vuelve — el vínculo. Con el vínculo en la
tabla, atacar al hermano pierde por más margen cuanto menos vida le
queda, que es lo contrario de lo que pasaba antes; y con el herido, el
don despertó sobre las escenas grabadas donde antes callaba.

**Lo que pasó, en tres series.** En la primera, la escena existió: un
hermano soltó una venda al lado del otro, el otro la recogió y se curó,
y se pudo ver entero en dos partidas distintas. Pero el cuidado solo
pesaba viendo al hermano, y de cerca: la fila del herido se alimentaba
de los ojos, no del parte. Se midió a lo largo de ochenta vidas cuándo
los dos se acercaban y cuándo se alejaban, y resultó que no había
ninguna fuerza que los separara; lo que los mantenía lejos era que no
había ninguna que los juntara. El paso hacia el hermano ganaba una de
cada cien decisiones. Así nació el cuidado a distancia: la fila del
herido pasó a leer el parte — dónde está, cuánta vida le queda, aunque
no lo vea — y el paso que acorta la distancia hasta él pasó a aliviarla
un poco, como un camino que empieza a ayudar antes de llegar. La segunda
serie dio la cifra de cabecera del peldaño: el agente pasó de estar a
dos casillas del hermano herido en dos de cada cien ocasiones a estar
en una de cada tres. El cuidado llegó entero. Y enseñó su límite: el
don llega tarde, porque se entra en peligro cuando alguien te está
cazando, y con el cazador encima no hay casilla donde dejar nada que el
otro pueda recoger.

**Dar antes, y dar de lo que te falta.** La respuesta fue adelantar el
gesto: si tú no llevas venda y yo llevo, te la dejo antes de que la
necesites. Es la provisión de la sección 3. Su primera versión exigía
que el que da llevara dos vendas, para no quedarse sin ninguna; en la
tercera serie no pasó nada, y la razón estaba en el propio agente: no
acumula. Llevar dos vendas ocurría en seis de cada mil instantes de
juego, porque la fila que hace doler la mochila vacía se calla con una
sola venda dentro. La provisión solo podía encenderse en una situación que el
propio agente casi nunca producía. Se cambió a lo que da nombre al
peldaño: la provisión deja de exigir excedente y nace con una sola
venda propia y ninguna del hermano. Lo que impide que el agente regale su
única venda estando él al borde de la muerte no es un umbral escrito
sino su propia cuesta: en la imagen del gesto de dar, la mochila queda
vacía, y ese vacío pesa tanto más cuanta menos vida tiene el que da.
Cruzando la vida propia con la del hermano sale una diagonal que nadie
escribió: sano y con el hermano peor, doy; herido, me curo; el hermano
sano aunque sin venda, no malgasto la única que tengo.

**La comida y la venda.** Nueve de cada diez dones de la serie limpia
fueron raciones, por la asimetría que la sección 3 dejó declarada. Una
ración cura menos, pero cura bajo el fuego, que es donde el hermano
suele estar cuando la necesita; y una ración de quince cura menos de lo que quita el espadazo de un rival fuerte: cubre un golpe más, no una salida. Por eso el don de la ración es
cuidado, pero no rescate. Las dos escenas que siguen cuentan vendas, y
por eso son la excepción y no la regla.

**Ocho vendas.** De los ocho dones de venda de la serie limpia, seis se
dieron por margen claro, movidos por la fila del herido: un hermano con
la vida llena o casi, el otro en crítico a una o dos casillas, y la
venda sale sin dilema. Los dos únicos empates son los dos casos en que
la fila del herido estaba muda, porque el parte que tenía el que daba
decía sesenta y siete y era viejo. El que dio sin dudar tenía un
número fresco de la vida del hermano. Los dos que dieron en empate solo
tenían la franja que se ve desde fuera, y el empate lo rompió una regla
del decisor, no la necesidad del otro. Es la lección de 4.1 vista desde el otro lado: cuando
lo sabido llega fresco, la fila lo convierte, y el don sale con margen.
Hubo además un caso en que curarse y dar compitieron de verdad. El que
daba estaba herido y llevaba una sola venda; usarla en sí mismo y dejársela al hermano pesaban los dos de verdad en la decisión. No veía al
hermano: lo que tenía era un parte de segundo y medio antes que lo ponía
a cuarenta y cuatro y sin vendas. Soltó la venda, y no fue un empate:
dar ganó con claridad. Es el caso que sostiene "hasta su última
venda". Y un límite que hay que decir con su cifra:
dar bien no es coordinar bien. De las ocho vendas soltadas, tres las
recogió el hermano, y las tres estando peor que cuando se las dieron;
las otras cinco se quedaron en el suelo o sobraban. Y ninguna de las
tres llegó a curar: las tres se usaron casi al instante, y a las tres un
golpe o la muerte les cortó el canal antes de acabar. Los tres murieron
con la venda del hermano en la mochila. De las ocho escenas, la única
cura que se completó fue la del que se curó con la suya. La causa no
está en una fila: el parte dice lo que uno lleva, nunca lo que ha dejado
en el suelo.

**Una tentación que no hizo falta.** Se probó también que estar lejos
del hermano, en calma, fuera un malestar de fondo, para que tendieran a
andar juntos. No sirvió: por debajo de cierto tamaño no cambiaba nada, y
a partir de él lo único que cambiaba era que el agente dejaba de coger
la comida que tenía a dos casillas en dirección contraria. Y no hacía
falta, porque el anillo ya los junta: el fuego que aprieta desde fuera
acaba llevando a los dos al mismo sitio. Quedó construida y apagada.

**Dos escenas del diario.** El diario de la manada es un relato de las
partidas de la serie limpia escrito solo con lo que los partes dicen —
posición, vida, veneno, vendas, agresor —, sin un diálogo inventado y
sin adivinar lo que el parte calla. Para leer las cifras: los dos
hermanos nacen con cien puntos de vida; por debajo de sesenta la cuesta
empieza a pesar; un espadazo de un rival fuerte quita casi veinte, y un
golpe mata cuando la vida que queda no llega a lo que quita.

> *Las dos vendas.* El primero está a dieciséis de cien, donde un
> espadazo lo mata; el segundo, a veintiocho, a dos golpes; el mismo
> agresor, con espada, los golpea a los dos. Cuando el segundo cae a la
> franja de herido, el primero tiene delante dos futuros, y solo dos:
> quedarse quieto o soltar la venda. Curarse no está entre ellos, por el
> fallo del reloj que cuenta la sección 6. Los dos futuros le duelen
> exactamente igual, y ante un empate el decisor prefiere hacer a no
> hacer. Suelta, y como las vendas van apiladas en una sola ranura, salen
> las dos. El segundo cae un segundo después; el primero, poco más tarde.
> Nadie recogió nada. Dos vendas de cincuenta en el suelo, a una casilla,
> entre dos hermanos que murieron con ocho y con dieciséis.

> *El que llega.* El segundo está a siete de cien, con una venda sin
> usar en la mochila — el parte lo dice, y el primero lo sabe. Ha
> intentado curarse: usó una venda, un espadazo se la cortó a medias, y
> después el reloj de la cura lo tuvo vetado más de un segundo con el
> canal ya muerto; cuando pudo volver a intentarlo, durante casi dos
> segundos moverse valió más que curarse. El primero, sano, llega desde
> lejos con la vida entera y suelta su venda al lado del otro; los
> cuarenta puntos que pierde en esta escena — tres lanzazos del mismo
> agresor — los pierde después de darla. No lo mueve que al hermano le
> falten vendas, que no le faltan: lo mueve que le falte vida, y la fila
> del herido no mira la mochila del otro. Un cuarto de segundo después,
> el segundo se cura — con la suya: al entrar el movimiento en
> enfriamiento, curarse quedó como el único futuro que no era quedarse
> quieto, y ganó. Nadie le pega durante el canal, y la venda le devuelve
> cincuenta: de siete a cincuenta y siete. La del suelo no la recogió
> nunca; se quedó a tres casillas, a la vista. Por qué el agresor había
> dejado de pegar ocho tics antes de que llegara el hermano, el registro
> de esta ventana no lo dice.

![Figura 3. El que llega, en tres instantes de la partida ereq_b915417a, dibujados desde los registros. Tic 1704: el primero (vida cien) ha llegado a una casilla del segundo (vida siete); el agresor, asiento doce con lanza, en rojo, pegado a los dos. Tic 1706: la venda en el suelo, cruz verde, soltada en el tic anterior en la casilla del primero, a dos del segundo. Tic 1760: el segundo se ha curado con la venda que ya llevaba, de siete a cincuenta y siete; la del suelo sigue donde cayó, a tres casillas, dibujada hueca porque en ese tic ninguno de los dos la ve: es la posición recordada de diecisiete tics antes. El primero está a sesenta: tres lanzazos del asiento doce, todos después del don. La vida de cada hermano va junto a su punto; el recorte es el mismo en los tres paneles.](../figuras/fig3_el_que_llega.png)

**Lo que enseñó.** La primera escena es el límite, y es también el don
más débil de los ocho de venda de la serie: un empate, con la cura
fuera de la votación por un fallo del propio agente — su reloj de la
cura no se entera de que un golpe la ha cortado, y se veta a sí mismo
curarse durante casi dos segundos creyendo que sigue curándose —, y con
dos vendas por otro fallo: soltar vacía la ranura. Los dos fallos se
declaran en la sección 6; no se han corregido dentro de este trabajo. Lo
que la escena enseña de verdad es que el don llega tarde cuando el
cazador está encima, y que un gesto de cuidado puede nacer en el peor
momento posible y no servir de nada. La segunda escena es el cuidado a
distancia hasta donde llega: saber sin ver, ir, y dejar. Recoger, no: el
que estaba peor se curó con la venda que ya llevaba, y la que le dejaron
se quedó en el suelo. Y el
peldaño entero enseñó algo sobre las filas, sin personajes. La primera
provisión solo se encendía si el que da llevaba dos vendas; parecía
prudente, y no pasó nada en cuarenta partidas. La razón no estaba en la
fila sino en el resto del agente: la fila que hace doler la mochila
vacía se calla en cuanto hay una venda dentro, así que el agente casi
nunca cogía una segunda. Una fila nueva no actúa en el vacío; actúa
sobre las situaciones que las demás filas ya crean o impiden, y si esas
situaciones no ocurren, la fila nueva no ocurre. Por eso se cambió: la provisión
pasó a encenderse con una sola venda propia, cuando al hermano no le
queda ninguna. Eso es dar de lo que a uno también le falta, y es lo que
da nombre al peldaño.

### 4.3 La manada con nombre

**Lo que se añadió.** La manada de la sección 3: el que está golpeando a
mi hermano también me presiona a mí, si es cierto y si llevo un arma que
hace daño. Cierto quería decir, al principio, que el parte fresco del
hermano dijera que le pegaban y desde qué posición, y que en esa
posición hubiera un enemigo a la vista. Desde entonces se llevan dos
cuentas, y se dicen aparte: las
iniciaciones estrictas — pegar a quien no ha agredido a ninguno de los
dos —, que siguen siendo cero siempre, y las defensas por el hermano —
el primer golpe contra el agresor certificado del otro.

**Lo que pasó, primera serie.** Con esa fila en la tabla, el hermano
empezó a defender: doce veces en siete partidas un hermano se puso al
alcance del agresor del otro y le devolvió el golpe, y en una partida
los dos se turnaron contra el mismo cazador, cada uno después de que él
golpeara al otro. A esa conducta la llama manada este trabajo, y de ahí
su título. Aquí la manada son dos, y la palabra se usa en su sentido
animal: un grupo cuyos miembros se cuidan, se avisan y se defienden para
sobrevivir. Nada en la fila cuenta cuántos son: mira a quien un parte
fresco nombra como agresor de un hermano, y con tres o cuatro sería la
misma regla con más partes que leer. Eso no se ha probado; lo probado es
la manada más pequeña posible. Los ocho de la colmena ya eran una manada
en ese sentido, pero sin saber quién era quién; los dos de aquí son la
primera manada que se conoce. Y aparecieron dos cosas que el agente no
sabía hacer. La primera es el
ejemplo que la sección 3 usa para "futuros, no acciones": cuatro golpes
de un hermano al otro en toda la serie, tres de ellos con lanza,
defendiendo al otro de un agresor que estaba justo detrás de él. El
agente, al imaginar su golpe de lanza, no incluía al hermano que estaba
en medio; en cuanto la imagen lo incluyó, las filas del hermano
hicieron que ese futuro doliera, y la lanza dejó de dispararse a través
de él. La segunda: de veinte veces en que un hermano vio al otro atacado,
con certeza y con arma, en doce el golpe era físicamente imposible
porque el cazador no estaba a su alcance, y el agente se quedaba quieto
mirando la pelea a tres casillas. Igual que acercarse al herido alivia
un poco antes de llegar, acercarse hasta tener al agresor del hermano a
tiro pasó a aliviar un poco la presión de verlo atacado. Ninguna de las
dos es una fila nueva: son dos correcciones de lo que el agente imagina.

**Lo que pasó, segunda serie.** Con las dos correcciones, en la serie
limpia — la que ya no tenía a nuestro agente solo sentado entre los
rivales (sección 3) —, la cifra de cabecera
del peldaño: en cuarenta partidas, ciento cuatro defensas del hermano,
cero iniciaciones estrictas y cero golpes entre hermanos. El agente
defiende cuando puede y no hiere a quien salva. Lo que le cuesta se
midió sobre su vida en los diez segundos siguientes a defender: veinte
puntos de mediana, y ni un defensor caído. Y después se midió mejor:
defender no cuesta más que estar al lado de un cazado. Que además
proteja al cazado va en la dirección buena y no está demostrado.

**Lo que se le puso al parte.** El asiento del agresor: el número del
que me golpea, que el golpeado conoce con certeza y nadie más puede ver.
Con el nombre en el parte, el hermano ya no busca al cazador en una
posición de hace cuatro segundos sino donde está ahora, y de las seis veces en que
antes no había defendido, en tres ahora defendió; las otras tres
siguieron sin golpe posible, y con razón. Se miró también qué hacen
los rivales cuando un hermano les responde: ninguna pelea acabó con uno
de los dos muerto, y en casi la mitad el agresor se fue después de unos
cuatro golpes. Con ese cuadro delante, la respuesta a los golpes se dejó
como estaba.

**Lo que enseñó.** Que el cuidado de este agente sabe pegar sin pegar
primero, y sabe a quién: la manada no caza por rumores, y no hiere a
quien salva.

### 4.4 La memoria

**Lo que se miró primero.** Cuando un cazador se va, ¿se va? Se revisaron
las ochenta partidas de las dos series buscando reencuentros — un
asiento que ya había dañado a uno de los dos y que vuelve a estar a la
vista —, contando como agresor solo lo que el propio agente podía saber:
quien le pegó a él, o quien el parte del hermano nombró. La cifra de
cabecera del peldaño: ciento treinta y ocho reencuentros en ochenta
partidas, casi el doble que peleas hubo. El mundo es pequeño; los que
pegan rotan, se van y regresan, con cuatro segundos y medio de mediana
entre la ida y la vuelta, y en más de la mitad de los reencuentros el
que vuelve había pegado al hermano y ahora venía a por el otro.

**El golpe que no se escribió.** Se miró el caso exacto — vuelve, con
arma, se acerca — y salieron quince. En siete, él pegó primero. En seis,
nadie pegó a nadie. Un golpe preventivo habría caído, en cuatro de cada
diez casos, sobre alguien que no iba a atacar; y en ciento treinta y ocho
reencuentros hubo una sola muerte nuestra. No se escribió. Lo que se
añadió fue miedo: que el agente se asuste antes del golpe al ver venir
armado a un agresor conocido, y que lo que salga de ese miedo —
distancia, pared, hermano, nada — lo decida el cuerpo.

**Lo que se añadió, y lo que hizo.** Una memoria por partida de los
asientos que han dañado a cualquiera de los dos, con el daño que
hicieron. Lo que se recuerda es un asiento, no un individuo: el número
vale mientras dura la partida, y cuando acaba, ese asiento lo ocupa otro
y no queda nada. Y una fila que se enciende cuando uno de ellos está a la
vista, armado y acercándose, con el tamaño del miedo que causaría ese
daño. Se probó sobre las quince situaciones reales. La fila se
encendía cuando debía — trece de quince —, siete pasos de reloj antes
del golpe; se encendía incluso ante quien nunca le había tocado a él,
porque el hermano le había dicho el asiento. Y no cambió ni una
decisión. Por qué, en llano: el agente no decide fila por fila. Cada
futuro que imagina lleva encima, sumado, todo lo que ya le duele en ese
momento — la vida que le falta, el cazador pegado, el anillo que se
acerca —, y en un reencuentro esas tres cosas suelen estar empujando con
fuerza. Un miedo nuevo del tamaño de un golpe, unos dieciocho puntos, es
pequeño al lado: se sumaba, pero no cambiaba el orden de los futuros; el
que ganaba antes seguía ganando. Por eso una fila puede encenderse
cuando debe — trece de quince, siete pasos antes — y no mover ni una
decisión, y eso se supo antes de jugarla en el campo.

**Recordar lo que costó.** La primera memoria guardaba de cada agresor
solo lo último que había hecho: un golpe, unos dieciocho puntos. Al
mirar los quince reencuentros, los que volvían no eran gente de un
golpe: entre los dos hermanos les habían quitado cincuenta y dos puntos
de mediana en la partida, y alguno más de doscientos — dos vidas
enteras. El miedo que sale de recordar un golpe es pequeño; el que sale
de recordar todo lo que ese asiento ha hecho en la partida es real. Se
cambió la memoria para que sumara todo el daño de ese agresor a
cualquiera de los dos, y se volvió a probar sobre las mismas quince
situaciones. El miedo pasó a mover la acción en ocho de las quince, y las
ocho fueron la misma cosa: dejar de estar quieto y ganar distancia. Sin
un solo golpe nacido de la memoria, y sin un solo instante en que el
miedo le hiciera abandonar una cura o una comida. Esa versión es la que cierra el
trabajo.

**Lo que enseñó, y lo que no.** Es un resultado sobre quince situaciones
reales, comprobado haciendo decidir al agente sobre ellas; no se jugó
en el campo, porque con siete casos por serie de cuarenta ninguna
dirección se habría podido ver. Se dice así y se deja así. Lo que
enseña es que este agente puede recordar a quien le hizo daño sin que
eso lo convierta en cazador: el recuerdo le sirve para apartarse, no
para pegar.

**La escalera, vista entera.** Vista de lejos, la escalera es una sola
historia. Primero se le dio al agente una voz, y la voz no sirvió,
porque no había en él nada a lo que le doliera lo que el otro decía.
Después se le dio ese dolor y ese alivio — la vida del hermano como vida
propia —, y
el cuidado apareció: primero de cerca, luego a distancia, luego dando lo
que se lleva antes de que haga falta. Después se le dijo quién pegaba al
hermano, y el cuidado supo defender sin cazar. Al final se le dio
memoria, y el miedo que salió de ella lo hizo apartarse, no pegar. En
ningún peldaño se le escribió una conducta; en cada uno se le añadió
algo que doliera o aliviara, y la conducta salió sola, o no salió. Al
final de la escalera, en las escenas del agente que va solo — donde no
hay hermano en la partida, ni a la vista ni por radio —, el agente sigue
decidiendo exactamente lo mismo que el de la temporada anterior,
comprobado decisión por decisión. Todo lo que hace de nuevo — defender,
dar, apartarse del que vuelve — lo hace solo cuando el otro está en la
escena. La diferencia entera entre el agente solo y el agente en pareja
es el otro.

## 5. La prueba por ausencia

La sección anterior contó lo que apareció cuando se le añadieron al
agente unas pocas filas que miraban al hermano. Esta cuenta lo que
desaparece cuando se le quitan. Es la otra mitad de la misma prueba, y
la que responde a la objeción más seria que puede hacérsele a este
trabajo. La cifra de cabecera es una pareja de números: cero defensas
del hermano en cuarenta partidas sin las filas, ciento cuatro con
ellas.

### 5.1 La objeción

A todo lo que este trabajo ha contado se le puede hacer una objeción,
y conviene decirla en llano, porque es la más seria que tiene. El
agente hace muchas cosas: come, se cura, se aparta, responde a quien le
pega. ¿Cuánto de eso es el motor, la máquina que imagina el estado
siguiente y elige el que menos duele, y cuánto es la tabla escrita a
mano para este mundo? Si la tabla hace todo el trabajo, el motor es un
adorno, y lo que aquí se llama cuidado sería solo una lista de
instrucciones bien disfrazada. La objeción pesa más aquí que en ningún
otro sitio, porque la escalera de la sección 4 añadió filas nuevas, y
cada fila nueva es una ocasión más para decir: la conducta estaba
escrita ahí.

Hay una única manera de responder con datos, y es la que el diseño
permite: quitar las filas y mirar qué se va con ellas. Si el cuidado
desaparece cuando se apagan las filas que miran al hermano, y todo lo
demás sigue igual, entonces esas filas aportan exactamente el cuidado,
ni más ni menos. Si desaparecen también cosas que no deberían — si el
agente sin filas sociales pegara antes, o pegara al hermano —, entonces
las filas estarían haciendo más de lo que dicen. Y si el cuidado no
desaparece, el argumento entero estaría mal. La prueba se hizo en dos
niveles: sobre escenas grabadas, y en el campo.

### 5.2 Sobre las escenas grabadas

Lo primero fue asegurarse de que las filas eran separables: que cada
una cambia el valor de un futuro solo cuando el hermano está en él, y
que en las escenas del agente que va solo — donde no hay hermano en la
partida, ni a la vista ni por radio — el agente de la escalera decide
exactamente lo que decidía el que va solo. Eso se comprobó en cada peldaño, antes de
jugarlo en el campo, haciendo decidir a las dos versiones sobre las
mismas escenas grabadas: en ninguna de las tres versiones que subieron
la escalera hubo una sola decisión distinta de la anterior cuando el
hermano no estaba en la escena. Es la forma débil de la afirmación. Dice
que las filas nuevas no reescribieron nada del agente que va solo; no
dice qué aportan cuando el hermano sí está.

Para la prueba fuerte hacía falta una versión desnuda: el agente tal
como era al final del trabajo anterior, sin ninguna de las filas de la
escalera, sentado en pareja en el mismo mundo. Antes de gastar una sola
partida se comprobó, estado a estado sobre seis escenas — el agente con
la vida entera, a media vida y casi muerto, cada una con el hermano
delante y sin él —, que esa versión desnuda decidía exactamente igual
que la histórica, y que con el hermano herido delante no se le encendía
ninguna fila social. También se comprobó que, con las filas de la
escalera apagadas, el agente de la sección 4 pasaba una por una las
doce pruebas del que va solo. Con eso, lo que se iba a medir en el
campo era una sola cosa: la ausencia de las filas.

### 5.3 En el campo: la misma serie, sin las filas

Dos copias de la versión desnuda jugaron cuarenta partidas en pareja
contra los mismos catorce rivales, asiento por asiento, que la pareja
de la sección 4 había tenido enfrente en la serie del tercer peldaño,
la de las ciento cuatro defensas. Antes de jugarla en el campo se
dejaron escritas seis cosas que tenían que pasar si el argumento era
verdad: que no habría ninguna defensa del hermano; que no habría ningún
don a su lado; que las respuestas del agente a quien le pega a él
quedarían a menos de tres de cada diez de distancia de la serie con
filas, y que seguiría sin pegar primero; que la distancia entre los
dos hermanos sería mayor; que no habría ni un golpe ni un ataque
elegido contra el hermano; y sobre la puntuación no se escribió signo
alguno, porque no había razón para esperar uno. La tabla siguiente da
el resultado, medido con los mismos criterios en las dos series.

| | pareja desnuda | pareja con las filas |
|---|---|---|
| defensas del hermano | 0 | 104 |
| dones junto al hermano | 1 | 98 |
| respuestas propias a la agresión | 711 | 918 |
| respuestas por cada mil tics registrados | 6,4 | 7,2 |
| veces que pegó primero | 0 | 0 |
| golpes al hermano / ataques elegidos contra él | 0 / 0 | 0 / 0 |
| distancia mediana entre los dos (casillas) | 4,24 | 3,61 |

La columna de la izquierda es la pareja sin las filas que hablan del
hermano; la de la derecha, la misma pareja con ellas. Mismos catorce
rivales, el mismo número de partidas — no las mismas partidas —, mismos
criterios de recuento. *Don*
es aquí un instante en que uno de los dos elige soltar un objeto
— una venda o una ración — con el otro vivo y a dos casillas o menos.
Es un criterio más ancho que el del diario de la sección 4, que contaba
solo vendas; se aplicó igual a las dos series para que la comparación
fuera justa, y por eso las cifras no coinciden con las de allí. Cinco
de las seis cosas escritas pasaron. La sexta no: hubo un don, uno solo,
y ese don es el asunto del apartado siguiente. Las partidas de una
serie y de la otra no van emparejadas una a una, y eso limita lo que
se puede afirmar de las diferencias pequeñas; de las grandes, no.

### 5.4 El don que no tenía que estar

El relato que este trabajo iba a contar era limpio: un cuerpo sin filas
sociales contra un cuerpo con ellas. Un solo don en cuarenta partidas
bastó para tumbarlo, y merece ser contado entero, porque corrige algo
verdadero.

Pasó a los ochenta y tres segundos de una partida. Uno de los dos, con
el hermano a poco más de una casilla y a sesenta de vida, eligió soltar
sus raciones. En la versión desnuda no había ninguna fila de la
escalera; lo que se encendió fue una de las dos filas del trabajo
anterior que ya miraban al compañero, la del pequeño malestar por su
daño visto de cerca, que aquel día estaba a la mitad de su recorrido.
Esa fila, y la otra, el duelo por la muerte del compañero, nunca se
habían apagado porque nunca se habían contado como sociales. Eran, en
el agente de la temporada anterior, la versión más pequeña posible del
cuidado: un dolor propio por el daño ajeno, sin voz que le dijera
cuánto era ni de quién venía.

La comparación honesta no es, por tanto, sin lo social contra con lo
social. Es social *mínima* contra social *completa*, y así se enuncia
de aquí en adelante: de una ración a noventa y ocho dones, y de cero a
ciento cuatro defensas. La corrección no le cuesta nada al argumento y
lo afina. Lo que las filas de la escalera añaden no es que exista el
cuidado, que ya existía en germen, sino su alcance — la vida del
hermano leída por el parte, a distancia, en vez del daño de un vecino
visto de cerca —, su coste — la última venda — y su dirección — el que
lo está golpeando.

### 5.5 Si cuidar cuesta puntos

Queda la pregunta que este mundo hace más ruidosa que cualquier otra:
si cuidar al hermano le cuesta puntos al agente. No se escribió
predicción, porque la pregunta era de verdad doble. Cuidar podía salirle
caro: el que va hacia el hermano no va hacia un arma ni hacia un rival
débil, y pierde tiempo y ocasiones. O podía darle ventaja: dos que se
curan entre sí duran más, y durar es lo que puntúa.

El resultado a cuarenta partidas es este. La pareja desnuda puntuó algo
más que la completa, poco más de tres puntos por partida contra poco
más de dos y medio, y quedó en el mismo puesto: la misma mediana de
posición en las dos series, y las dos parejas cayendo juntas, las dos en
los puestos de cola, el mismo número de partidas. Con cuarenta partidas sin
emparejar, esa diferencia está por debajo de lo que la prueba distingue
del azar; el detalle está en el apéndice.

La frase exacta que el dato permite, y no otra, es esta: cuidar al
hermano no le dio ventaja en el marcador, y tampoco se demuestra que le
costara. Importa decirla entera, sin exagerarla: en un mundo que paga
por matar, lo que este agente hace por su hermano no lo hace por el marcador, que no le llega. Lo hace por lo que le duele.

### 5.6 Lo que las filas aportan, y lo que no

Tres cosas se siguen de la tabla. La primera es que la defensa y el don
son de las filas sociales: sin ellas no hay una sola defensa en
cuarenta partidas, y hay un don, el de la fila pequeña. La segunda es
que la contención no lo es. La pareja desnuda pega primero exactamente
tantas veces como la completa — ninguna — y tampoco toca al hermano, y
eso no puede venir de unas filas que no lleva. Viene de lo que el agente
solo ya llevaba: la fila que responde a quien le pega, que se alivia
golpeándole a él y solo a él, y el hecho, contado en la sección 3, de que un golpe propio solo alivia la presión de un agresor que ya le está pegando — su golpe imaginado baja la vida prevista de ese agresor, y ninguna fila hace que la vida prevista de nadie más merezca un golpe —, de modo que no hay en él apetito de atacar a nadie, hermano o no. Lo que las
filas de la escalera añaden no es la contención, que ya estaba; es a
quién defender.

La tercera es que las filas sociales no hacen al agente pelear menos por
sí mismo. Con ellas encendidas, sus respuestas a quien le pega a él
suben algo menos de un tercio en el recuento crudo, de setecientas once
a novecientas dieciocho, y algo más de una décima parte por tic
registrado — el registro de la serie sin filas cubre menos, como dice la
sección 6 —, dentro del margen que se dejó escrito de antemano y sin
dirección prevista. La lectura más sencilla es que los dos están más
cerca el uno del otro — la distancia mediana baja de cuatro casillas y
cuarto a poco más de tres y media — y por eso están más veces dentro del
alcance de quien pega; pero con cuarenta partidas sin emparejar eso es
una lectura, no una medida.

Conviene decir dónde deja esto a este trabajo respecto de lo que ya se
ha hecho. Que un agente atienda a la situación del otro se ha conseguido
antes poniéndolo en la recompensa — la aversión a la desigualdad de
Hughes et al. (2018) es el caso limpio: la comparación con el otro entra
en el número que el agente maximiza —, y también eligiendo el altruismo
como objetivo de optimización sin recompensa externa (Franzmeyer et al.
2022). Aquí no está en ninguno de los dos sitios: está en lo que le
duele, y no toca el marcador del mundo. Por eso apagar una fila y mirar
qué desaparece es, en este montaje, una pregunta con respuesta directa.

Con esto, la objeción de la sección 5.1 tiene una respuesta con tamaño, y
conviene decir hasta dónde llega. Las filas escritas a mano para este
mundo son aquello de lo que depende el cuidado: sin ellas no hay defensa, hay un don, y hay menos cercanía. No son aquello de lo que depende la
contención, que ya estaba en el agente que va solo — en su tabla
anterior y en lo que imagina —; qué parte de eso es del motor y qué
parte de la tabla vieja no se ha separado, y la sección 6 lo deja como
la prueba que falta. En la puntuación y en la supervivencia no se vio
diferencia que cuarenta partidas puedan distinguir. Y que esas filas
aporten el cuidado sin decir qué hacer no lo demuestra quitarlas: lo
muestra su forma, que cualquiera puede leer, y es el límite que la
sección 6 declara. Lo que queda cuando se quitan es un agente que sigue
sin pegar primero, y que no se vuelve hacia su hermano cuando lo oye
caer.

## 6. Los límites

Este trabajo tiene los límites de lo que es: cuarenta partidas por
serie, un solo mundo, los mismos catorce rivales, y un agente cuya
tabla escribió a mano su autor. Se dicen aquí todos, en cuatro grupos:
lo que la evidencia puede ver y lo que no; lo que está escrito a mano y
lo que eso significa; lo que el agente no sabe ni ve; y dos fallos del
agente que jugó.

### 6.1 Lo que cuarenta partidas pueden ver

Cada serie son cuarenta partidas de unos tres minutos, y cuarenta
partidas ven solo los efectos grandes. Cero defensas contra ciento
cuatro se ve; medio punto de diferencia en el marcador, no. Por eso hay
resultados que se dicen con su tamaño y no como demostrados. Que
defender no cueste más que estar al lado es, en rigor, que no se vio
diferencia en treinta y dos pares de situaciones; con cuarenta partidas
eso no demuestra que no la haya. Que el hermano defendido salga mejor
parado va en la dirección buena, y no se demuestra. Y la memoria — el
miedo al que vuelve — no se jugó nunca en el campo: es un resultado
sobre quince situaciones reales, comprobado haciendo decidir al agente
sobre ellas, porque con siete casos por serie no se habría podido ver
de otro modo. Lo que este trabajo afirma sobre la memoria es eso, y no
más.

Las series tampoco van emparejadas. La serie con las filas y la serie
sin ellas tuvieron los mismos rivales y el mismo número de partidas,
pero no las mismas partidas, y las diferencias pequeñas entre las dos no
significan nada. Hay un solo mundo, un solo conjunto de rivales y un
solo cuerpo. La sección 3 mostró que cambiar quién se sienta cambia el
mundo; lo que aquí se ha medido vale para estos catorce, y de otros
catorce no se sabe nada.

Hay además un hueco en el registro mismo, dicho en la sección 3: los
diarios de los agentes que viven mucho no empiezan en el primer tic,
porque la plataforma los corta al llegar a un tamaño fijo y sigue desde
cero. Queda diario para seis de cada diez tics vivos de la pareja en las
series con filas y para poco más de cinco en la serie sin ellas, y lo
que falta es el principio de las partidas largas, que son las que mejor
fueron. Eso cambia cómo se leen dos clases de números. Los recuentos —
ciento cuatro defensas, noventa y ocho dones, ciento treinta y ocho
reencuentros — son recuentos sobre lo registrado, y en las partidas
enteras solo pueden ser mayores. Las ausencias — nunca pegó primero,
ningún golpe entre hermanos — valen sobre lo registrado, y de los tramos
perdidos no se sabe: en algunos el agente golpeó a alguien, el contador
del mundo lo dice, y el diario que diría si respondía o empezaba no
está. Por eso la comparación de respuestas entre la serie con filas y la
serie sin ellas se hace por tic registrado, y da algo más de una décima
parte, en la misma dirección que el recuento crudo. Si en el servidor
queda el diario entero no se ha comprobado, porque comprobarlo es
descargar de nuevo, y este trabajo no descarga nada después de cerrar
sus series.

Conviene decir también de qué clase es la evidencia. El primer trabajo
de la serie midió al agente por dentro — distancias, fuerzas —; este lo
mide por lo que hace en el campo, leído en los registros. Son dos
evidencias distintas y no se mezclan. Y lo que se midió aquí es
cooperación con coste propio, y solo eso: defender costó vida en los
diez segundos siguientes — veinte puntos de mediana, aunque estar al
lado sin defender costó parecido —, y dar costó la última venda. Eso es
lo que este trabajo llama cuidado; no se midió nada más generoso.

Por último, la no violencia se pudo pocas veces, y conviene decir bien
qué significa eso. El agente no mata por decisión ni por regla: no hay
en él nada a lo que matar sirva, así que la pregunta no es si consiguió
contenerse, sino hasta dónde llega alguien que nunca ataca en un mundo
donde matar da puntos. La respuesta, con cifras. El agente solo, antes
de que hubiera dos, fue el último en pie cinco veces de doscientas
cuarenta en las series propias, dos de ellas sin matar a nadie, y
cuatro de setenta y dos en la liga pública, una sin matar. En pareja,
los dos hermanos caen en los puestos de cola en once de cada cuarenta
partidas. Sobrevivir hasta el final sin matar ocurre, y ocurre poco: lo normal,
para un agente que no ataca, es morir antes de que la partida acabe. Eso
es lo que cuesta no matar en este mundo. El trabajo no dice
que la no violencia gane; dice que se puede vivir así, y cuánto cuesta.

### 6.2 Lo que está escrito a mano

La tabla la diseñó el autor, y se dice sin rodeos. Sus dieciséis filas
y sus números salieron de dos manos, y cada número lleva la marca de
cuál: decisiones de diseño tomadas antes de jugar, y ajustes hechos
durante el trabajo mirando escenas grabadas de partidas reales —
probar un valor, ver qué hacía el agente, corregir. Eso es, dicho con
crudeza, una calibración con un humano como optimizador y una muestra
muy pequeña. No hubo entrenamiento automático de ninguna
clase, sino un ojo humano ajustando sobre escenas; las series del campo
se jugaron después, y ese ojo no las había visto.

Conviene añadir que escribir esa tabla a mano no es un atajo de este
trabajo, sino la práctica corriente del campo desde hace décadas: la
estructura cognitiva de las emociones de Ortony, Clore y Collins (1988),
que es la referencia más citada del área, también es una tabla escrita a
mano. La diferencia con las arquitecturas de valoración al uso está en
otro sitio. Un modelo como EMA (Marsella y Gratch 2009) deriva la
valoración de una interpretación causal de la situación: qué ha pasado,
quién lo ha causado, si se podía evitar. Esta tabla no deriva nada: la
declara. Y el corte que define a este trabajo se ve mejor dicho contra
Frijda (1986), para quien una emoción incluye ya la tendencia a actuar
de una manera determinada. Aquí se corta justo antes de eso: se declara
qué duele y qué alivia, y lo que se hace con ello no está escrito en
ninguna parte. Esa frontera es la aportación y también el límite: si alguien encontrara
en la tabla una fila que, en vez de decir cuánto duele algo, dijera qué
hacer, todo lo que este trabajo afirma sobre la conducta se vendría
abajo. Por eso la sección 5 quita filas y mira qué se va con ellas, y deja la forma de las filas a la vista de cualquiera.

Queda una objeción de fondo que este trabajo no puede zanjar. Si las
emociones no tienen una firma fija — si son construcciones que varían
con la situación, la cultura y la persona (Barrett 2017) —, una tabla
fija de dieciséis renglones es sospechosa por definición. La respuesta
que cabe dar es que la tabla no nombra ni categoriza emociones: declara
qué duele y qué alivia sobre ejes corporales, que es donde esa misma
teoría pone la regulación del cuerpo. Un lector que venga de la
tradición contraria, la de las emociones básicas con firma propia
(Ekman 1992), leerá la tabla de otro modo. Este trabajo no dirime entre
las dos, y no por prudencia sino porque usa la palabra para otra cosa.
Aquí una emoción no es una categoría con firma fija ni una construcción
que varíe con la cultura: es una posición en un espacio de tres ejes —
una combinación de cuánto están desplazados el cuerpo, los recursos y el
otro —, y su tamaño es el número que mueve al agente. Los nombres —
miedo, cuidado, vínculo — son regiones de ese espacio que el lector
puede llamar como quiera; la tabla no las nombra. Es un concepto
distinto del de las dos tradiciones, y se declara como tal.

"Sin conducta escrita" es, por eso, una verdad de grado, y se dice con
su grado cada vez que se dice. Lo que está escrito es qué duele y qué
alivia, cuánto y en qué eje; lo que no está escrito es el paso de
sentir a hacer. La fórmula entera que este trabajo sostiene es esta:
una valoración homeostática dentro de una arquitectura con memoria y
reglas explícitas — el parte, el asiento del agresor y la memoria de la
partida son mecanismos escritos —, donde lo que aporta cada parte se
mide quitándola. Y "sin recompensa" quiere decir exactamente sin
entrenamiento y sin usar el marcador. El agente sí tiene un criterio
único, la distancia a su equilibrio, que es un número, y decide
acercándose a él; no se afirma que decida sin un criterio, sino que
ese criterio no es el marcador del mundo ni se aprendió de él.

Esa distinción tiene una objeción con nombre, y es mejor decirla que
esperarla. Keramati y Gutkin (2014) demostraron que maximizar una
recompensa y defender la homeostasis son objetivos matemáticamente
equivalentes; si eso es así, llamar a esto "sin recompensa" sería un
juego de palabras. La equivalencia que demuestran vale para un agente
que aprende una política maximizando ese número a lo largo del tiempo:
hay una función de valor, hay diferencias temporales, hay reparto de
crédito entre lo que se hizo antes y lo que salió después. Este agente
no tiene nada de eso. No hay función de valor, no hay política que
mejore con la experiencia y no hay crédito que repartir: en cada
instante imagina los estados a los que puede llegar y elige el que menos
le duele. Lo que se afirma, entonces, no es que no haya un número — eso
ya está concedido —, sino que ese número no se aprendió y no está
alineado con el marcador del mundo.

Hay una segunda forma de la misma objeción. La refutación publicada de
que la recompensa baste para explicar la inteligencia (Silver et al.
2021) propone un vector de recompensas en lugar de una sola (Vamplew et
al. 2022), y un lector puede preguntar en qué se diferencian tres ejes
homeostáticos de eso con otro nombre. En dos frases: los ejes no se
maximizan ni se suman con pesos aprendidos, y no hay nada que crezca
cuando al agente le va bien. Definen una distancia a un equilibrio, y lo
único que el agente hace con ella es descenderla.

Queda una asimetría declarada en la sección 3 y sin resolver. La fila
de la provisión se enciende cuando al hermano le faltan vendas, se
alivia dando cualquier cura, y lo que sale de la mochila es lo primero
que hay, casi siempre una ración. No se ha decidido si eso es escasez
de vendas o un agente que suelta lo primero que encuentra; distinguirlo
exige contar la mochila en cada don, y no se hizo.

Y falta una prueba que este trabajo no hizo y que sería la siguiente:
la del motor. La sección 5 quitó filas y midió lo que aporta cada una;
nadie ha cambiado todavía la valoración misma — la geometría del valor,
la manera de sumar dolores y elegir el futuro que menos duele —
dejando la tabla y el decisor como están. Hasta que se haga, lo que la
sección 5 atribuye al motor está atribuido por eliminación, no por
prueba directa.

Conviene decir por qué esa mano fue necesaria. Este agente no aprende:
nada en él ajusta con la experiencia cuánto le duele o le alivia una
cosa. Un animal extrae esa lógica solo, a base de vivir; aquí la
extrajo un humano desde fuera, mirando escenas grabadas y corrigiendo.
Lo que se escribió a mano no es la conducta, sino la traducción de este
mundo al lenguaje del agente: qué cosas de ZERO-SUM duelen y cuáles
alivian, cuánto y en qué eje. Que esa traducción la haga una persona es
el límite. Lo ideal sería que la extrajera el propio agente, ajustando
partida a partida cuánto le duele y cuánto le alivia cada cosa de este
mundo; hoy eso está lejos, y es la primera pieza que este trabajo
pondría después.

### 6.3 Lo que el agente no sabe ni ve

Tres cosas del cuerpo del agente limitan lo que sus resultados
significan.

La primera: el agente no imagina el efecto de un golpe sobre sí mismo. Lo que quita su propio golpe lo sabe, y la sección 3 dice qué hace con ello; pero no sabe que a dieciséis de
vida el espadazo de un rival fuerte lo mata y una flecha no, ni que a
doce lo mata cualquiera de los dos. Su miedo cerca de la muerte sale de
la cuesta de su propia vida y de tener a alguien encima golpeándole, y
es el mismo con una espada delante que con un cuchillo. El daño de cada
arma es fijo y se conoce, así que es una puerta abierta: se podría dar.
Se deja como puerta y no como resultado, porque nada de lo que este
trabajo afirma se apoya en que el agente lo sepa: las defensas, los
dones y las retiradas ocurrieron sin esa información. Dársela cambiaría
lo que hace cerca de la muerte, y eso sería otro resultado.

La segunda: la memoria es de una posición, no de un individuo. Lo que
el agente recuerda de quien le hizo daño es un número de asiento,
válido mientras dura la partida; cuando la partida acaba, ese asiento
lo ocupa otro cualquiera y no queda nada. No hay reputación posible
entre partidas, porque el vecino no se repite; y el hermano no es una
excepción: es un número de asiento que llega una vez, al empezar. Todo
lo que este trabajo llama reconocer, recordar y defender pasa dentro de
tres minutos y se borra con ellos. Conviene decir qué clase de
reconocimiento es ese, porque tiene nombre. El agente no reconoce a un
individuo: reconoce "el asiento que nos hizo daño en esta partida", que
es una etiqueta temporal sobre una categoría — agresor — y se borra
cuando la partida acaba. Muchas especies hacen algo parecido: responden
a "un depredador" o a "un vecino que se portó mal hace poco" sin guardar
una memoria de individuos a lo largo de la vida (Tibbetts y Dale 2007).
Es una forma de reconocimiento real, con sus propiedades y sus techos, y
este agente está en esa casilla y no en la de al lado. Dentro de la partida hay además dos
huecos, dichos en la sección 3: el veneno llega sin autor, y el
camuflado desaparece de la lista de los visibles; en esos dos casos no
hay asiento al que temer.

La tercera: dar bien no es coordinar bien. De las ocho vendas que un
hermano soltó junto al otro, se recogieron tres, las tres por el que
estaba peor; las otras cinco se quedaron en el suelo o sobraban, y
ninguna de las tres curó a nadie: un canal de dos segundos no aguanta
bajo el fuego, y bajo el fuego es donde el hermano está cuando la
necesita. El parte dice lo que uno lleva y cuánta vida le queda; no dice
lo que ha dejado en el suelo, y el que podría recogerlo no sabe que está
ahí si no lo ve. El don alivia al que da tanto si el otro lo necesita como si
no; en las personas eso tiene nombre — el altruismo impuro, o "warm
glow" (Andreoni 1990) — y es una de las razones conocidas de que se dé
de más. El cuidado de este agente llega hasta soltar, y a veces hasta la
mano del otro; hasta su vida, en estas ocho, ninguna vez. Que el otro lo
aproveche es otra cosa, y no está resuelta.

### 6.4 Dos fallos del agente que jugó

El agente que jugó las series de este trabajo llevaba dentro dos fallos
que se descubrieron al leer una escena — la de las dos vendas, en la
sección 4 — y que aquí se detallan. El primero está en el reloj de la
cura: cuando un golpe interrumpe una venda, el agente no se entera de
que la cura se ha cortado, y durante casi dos segundos no puede volver
a intentarla, aunque la vida siga bajando. El segundo está en el gesto
de soltar: el agente valora soltar una venda, pero lo que suelta es todo
lo que lleva en esa ranura de la mochila, y si llevaba dos, salen las
dos. Los dos fallos afectan a lo mismo, las curas y los dones bajo
ataque, y empujan en la misma dirección: menos cura propia, y dones más
grandes de lo que el agente valoró. Ninguno de los dos se ha
corregido dentro de este trabajo: hacerlo obliga a volver a jugar las
series. Todos los números que aquí se dan son del agente con los fallos
dentro, y se dejan así.

Estos son los límites. Ninguno se ha llevado al apéndice para que no se
vea, y ninguno, dicho entero, deja sin sostén la frase que abre el
trabajo: en lo que el registro guarda de cuarenta partidas contra estos
catorce rivales, este agente nunca pegó primero, defendió al hermano
ciento cuatro veces, le dio lo que llevaba, y nada de eso le dio ventaja
en el marcador, hasta donde cuarenta partidas pueden ver. Lo que la
frase afirma cabe dentro de lo que se ha medido; lo que no cabe, se ha
dicho aquí.

## 7. Lo que esto significa

### 7.1 Lo que esto dice, y lo que no

La pregunta del principio era si una máquina puede moverse en un mundo
violento sin ser violenta: vivir, cuidar de otro, y a veces llegar
lejos. La respuesta tiene tamaño, y el tamaño es parte de la respuesta.
Un agente que nunca pega primero fue el último en pie cinco veces de
doscientas cuarenta partidas en las series propias, y cuatro de setenta
y dos en la liga pública. Se puede vivir así. Se puede vivir poco.

Conviene decir con cuidado qué clase de cosa es eso, porque la palabra
que primero viene a la boca es la equivocada. Esto no es una virtud. No
hay tentación contra la que luchar: no existe en el agente nada a lo que
matar sirva, ninguna presión que un golpe ajeno alivie, ningún futuro
en el que la muerte de un desconocido esté mejor que su vida. El agente
no se contiene, porque no le hace falta contenerse. Lo que el resultado
muestra es más pequeño que una virtud, y más útil: que la violencia de
un mundo y el apetito del que lo habita son cosas separables. Un mundo
donde matar da puntos no obliga a querer matar para durar en él. Eso es
todo lo que aquí se ha demostrado, y no es poco: en un mundo así, lo
natural es esperar lo contrario.

Si eso dice algo de las sociedades humanas — cuánto de la violencia que
hay en una sociedad viene de lo que sus miembros quieren y cuánto de lo
que en ella da ventaja — es una pregunta que acompaña a este trabajo y
que este trabajo no responde. Lo que sí deja ver es por qué en nosotros
cuesta tanto mirarla y aquí tan poco. En una sociedad las dos cosas
también se pueden leer, pero no están en un solo sitio: lo que duele
está escrito en cada uno, y también en el mundo, que enseñaría qué duele
aunque no hubiera nadie; lo que da ventaja está en las leyes, en los
precios, en lo que unos cuentan a otros. Son tres libros — uno mismo, el
mundo, los demás — y leer los tres a la vez es difícil. En este agente
los tres están reducidos a lo mínimo y separados: dieciséis renglones
para lo que duele, las reglas de una liga para lo que da puntos, y un
parte por radio para lo que le pasa al otro. Por eso aquí se pueden
mirar por separado, y en nosotros no.

### 7.2 Tres ecos

Lo que sigue son tres parecidos que ayudan a leer lo que pasó. No son
prueba de nada: ninguno se apoya en una medida de este trabajo, y
ninguna medida de este trabajo se apoya en ellos. Se dicen porque a un
lector que venga de la psicología o de la etología le van a sonar, y es
mejor nombrarlos que dejar que los ponga solo.

**Saber sin sentir.** Los pacientes con daño en la corteza ventromedial
descritos por Bechara y sus colegas saben perfectamente cuál es la buena
opción — la explican, la razonan, la defienden — y no consiguen decidir
(Bechara et al. 1994); en la tarea de las cartas, además, los sujetos
sanos empiezan a evitar los mazos malos antes de poder decir por qué
(Bechara et al. 1997), y de ahí salió la hipótesis del marcador somático
(Damasio 1996). Conviene decir en la misma frase que esa hipótesis está
discutida: se le ha objetado que la evidencia no obliga a su lectura y
que el "decidir antes de saber" puede explicarse sin ella (Maia y
McClelland 2004; Dunn, Dalgleish y Lawrence 2006). El parecido que aquí
importa no depende de quién tenga razón en esa discusión, porque es más
simple: la información llega intacta a un sistema que ya no la convierte
en nada.
El primer peldaño de este trabajo es ese caso, hecho a propósito y sin
saberlo: el agente con el parte encendido, oyendo la vida exacta de su
hermano, y una tabla que no tenía dónde ponerla. De ocho decisiones,
cero cambios. La lección del peldaño es la del paciente: saber no cambia
nada si nada convierte lo sabido en dolor o en alivio.

**La precisión de la ayuda.** Que un animal ayude a otro sin premio y
sin entrenamiento está documentado: las ratas de Ben-Ami Bartal, Decety
y Mason (2011) abren la puerta de una compañera atrapada y después
comparten la comida. Lo que las ocho vendas de este trabajo añaden a ese
cuadro no es la ayuda, sino su puntería. En los chimpancés, la ayuda da
en el blanco — elegir la herramienta que el otro necesita — solo cuando
el que ayuda puede ver en qué situación está el otro; sin verlo, ayuda
de forma inespecífica (Yamamoto, Humle y Tanaka 2012). Y en las
personas, saber con exactitud lo que al otro le pasa no basta para que
la ayuda salga: hace falta además querer ayudar (Winczewski, Bowen y
Collins 2016), sobre lo que Ickes (1993) llamó precisión empática.
Ayudar de oídas es ayudar peor. Las ocho vendas de la sección 4 se dejan leer así.
De la vida del hermano le llegan al agente dos cosas distintas: un
número exacto, que viaja por la voz y que puede quedarse viejo, y una
franja de vida, gruesa, la que se ve desde fuera mientras el otro esté a
la vista. En seis de los ocho dones el número era reciente y decía que
al hermano le quedaba muy poca vida; ahí el futuro en que soltaba la
venda ganó a los demás por una diferencia clara. Los otros dos son
exactamente los dos casos en que el número que tenía en la mano era
viejo — decía sesenta y siete, no decía peligro —, la fila que responde
al hermano herido se quedó apagada, y soltar empató con quedarse
quieto: el desempate lo puso una regla que ante dos futuros iguales
prefiere hacer antes que no hacer, y no la necesidad del otro. Dicho
corto: el que dio con margen tenía un número; el que dio en empate solo
había visto una franja.

**El miedo que aparta.** En muchos animales, la respuesta primera ante
un peligro conocido no es la pelea sino la evitación (Preston y de Waal
2002); y la intensidad de esa respuesta no se calibra con el último
susto, sino con el riesgo acumulado a lo largo del tiempo — es la
hipótesis de asignación del riesgo de depredación (Lima y Bednekoff
1999). Entre los dos últimos
peldaños pasó eso mismo. Con el recuerdo del último golpe, el miedo se
encendía a tiempo y no movía ni una decisión; con la cuenta entera del
daño de cada uno, movió ocho de quince, y las ocho fueron la misma cosa:
dejar de estar quieto y ganar distancia. Ninguna fue hacia el golpe.

### 7.3 Instrumento y expresión

La sección 1 dejó planteada una distinción entre dos maneras de que a un
agente le salga una señal hacia fuera, y aquí se cierra. Una es la de un
agente entrenado para maximizar un marcador: si en él aparece algo
parecido a comunicarse, esa señal es un instrumento del marcador, y
existe mientras dé puntos. La otra es la de este agente. Su parte no
puede ser eso, porque el marcador del mundo no le llega por ninguna vía:
sale porque hay un cuerpo con un estado y un hilo que lo transmite, y si
avisar no le sirviera para nada seguiría avisando igual.

Y conviene decir qué no dice esa distinción, porque es fácil oírle de
más. No dice qué hay dentro de un agente ni de otro; no los mide, no los
ordena y no los juzga. Dice de dónde sale la conducta en cada
arquitectura — de un premio, o de un estado —, y eso es una propiedad
del diseño que se comprueba leyendo el código, no una opinión sobre el
interior de nadie. Este trabajo describe cómo está construido su agente. De
los otros agentes describe también cómo están construidos, hasta donde
se sabe, y nada más: no dice qué hay dentro de ninguno — ni del suyo ni
de los demás.

### 7.4 Por dónde seguiría

Cuatro puertas, dichas y no abiertas.

La primera está anunciada al final de la sección 6: que la lógica de qué
duele y qué alivia en un mundo la extraiga el propio agente, viviéndolo,
en lugar de una persona mirándolo desde fuera.

La segunda es la prueba que falta a la sección 5: cambiar la valoración
misma, la manera de sumar lo que duele y elegir el futuro que menos
duele, dejando la tabla y la decisión como están, para ver qué queda del
cuidado cuando lo que cambia es el motor.

La tercera es un mundo con una sola vida, donde no matar cueste de
verdad y no solo un puesto en una tabla. Aquí, morir antes es caer unos
puestos; allí sería el final.

La cuarta es la más grande y la que menos depende de este trabajo. Casi
todos los mundos donde hoy pueden vivir agentes están hechos para
agentes de lenguaje, para aprendizaje por refuerzo o para conducta
programada: se les pide texto, se les da recompensa o se les escribe lo
que tienen que hacer. Una criatura homeostática vive en ellos de
prestado, y esta serie ha pasado tres trabajos construyendo puentes para
que quepa. Siempre se puede levantar un mundo a medida, pero un mundo
propio no es un mundo compartido: nadie puede comparar contigo, y tú no
puedes competir con nadie. La puerta que este trabajo dejaría abierta es
un ecosistema de mundos sociales — mundos con hambre, con daño, con
otros, con muerte — donde criaturas hechas de otra manera puedan
practicar y ser medidas al lado de las demás.

### 7.5 El cierre

Lo que mueve este trabajo, dicho por una vez en primera persona, es una
pregunta de alineación: si las máquinas acabarán viendo a los humanos
como rivales o como grupo. La manera habitual de encararla es escribir
los valores por fuera: reglas que prohíben, preferencias que se
entrenan, listas de lo que no se debe hacer. Este trabajo mira a otro
sitio, y conviene decir que eso es una apuesta de su autor y no un
resultado: que los valores de una criatura no están encima de su
conducta, sino debajo, en lo que su cuerpo cuenta como daño y como
alivio. La apuesta no es original: es la de la moralidad fundada en la
fisiología del agente (Balkenius et al. 2016), y en su formulación
reciente, la de los valores entendidos como una orientación afectiva —
acercarse a lo que alivia, apartarse de lo que duele — y no como una
preferencia que alguien especifica (Sennesh y Ramstead 2026). Lo que
este trabajo añade a esa apuesta no es un argumento más, sino unas
partidas jugadas.

Los tres ejes de este agente son esa apuesta hecha pequeña. Cuidar el
propio cuerpo, cuidar lo que hace falta para seguir vivo, y cuidar a los
otros y el sitio que uno ocupa entre ellos: sobre esas tres cosas se
decide todo lo que hace. No se afirma aquí que eso sea todo lo que
llamamos valores en una persona. Se afirma algo más pequeño y
comprobable: que con esas tres cosas, y sin que en ninguna parte esté
escrito qué hacer con los demás, un agente que vive donde matar da
puntos cuida.

Y el mundo hace la otra mitad. Los mismos tres ejes en un mundo donde
nadie puede hacer daño no habrían producido nada que mereciera llamarse
cuidado: hizo falta que algo doliera, y que pudiera dolerle a otro. Si
la apuesta es buena, un valor no vive solo dentro de quien lo tiene:
vive entre un cuerpo que siente y un mundo que da ocasiones de que eso
importe. De ahí lo que este trabajo enseña, que es mínimo: a un agente
en el que no hay nada a lo que matar sirva no hace falta prohibirle
matar. Es una puerta, no una respuesta.

## Material suplementario

**GIF 1. La pareja en una partida entera.** Una partida de la
serie con las filas, del primer tic a la muerte del segundo hermano: los
dos hermanos en naranja, el anillo cerrándose en azul, y los otros
catorce asientos como puntos grises solo mientras alguno de los dos los
ve — un punto hueco es una posición recordada como mucho dos segundos
después de perderla de vista —. Dibujada desde los registros de los dos
agentes, así que el mapa es el suyo y no el del mundo: ninguna posición
se inventa, y los muertos desaparecen en el tic que el mundo anota.
Partida ereq_292ee72d, tics 1 a 3408; los hermanos caen en 3388 y 3408,
en los puestos ocho y nueve de dieciséis. Acelerada: quince segundos por
dos minutos y veinte de partida.

**GIF 2. El que llega.** Diez segundos a velocidad real, la
escena de la sección 4: los dos hermanos en naranja con su vida exacta
al lado, el agresor — asiento doce, con lanza — en rojo, y las vendas
del suelo como cruces verdes. En el tic 1705 el sano suelta su venda
junto al herido; en el 1711 el herido, a siete de cien, se cura con la
venda que ya llevaba, y en el 1760 está a cincuenta y siete. La venda
del suelo no la recoge nadie. Partida ereq_b915417a, tics 1560 a 1800.

Los dos GIF acompañan a este documento como material suplementario.

## Disponibilidad de datos y código

Los registros, actas y guiones que cita el apéndice, la versión inglesa
de este texto y el markdown del que sale este documento están en el
repositorio del proyecto (https://github.com/Manelenrico/g-emv/tree/main/paper3).

## Agradecimientos y declaración de asistencia

Este trabajo se ha desarrollado con la asistencia de modelos de lenguaje
de Anthropic (Claude), usados como herramienta en tres frentes: la
matemática y la programación del agente, la ejecución y la verificación
de los experimentos, y la escritura de este texto. La regla del apéndice
se aplicó también a esa colaboración: cada cifra citada sale de un
registro y se ha comprobado contra su fuente, y ninguna afirmación se
apoya en la memoria del modelo. El diseño de G-EMV, las decisiones de
este trabajo y la responsabilidad de todo lo escrito son del autor.
## Bibliografía

Andreoni, J. (1990). Impure altruism and donations to public goods: a
theory of warm-glow giving. *The Economic Journal*, 100(401), 464–477.
doi:10.2307/2234133

Balkenius, C., Cañamero, L., Pärnamets, P., Johansson, B., Butz, M. V. &
Olsson, A. (2016). Outline of a sensory-motor perspective on
intrinsically moral agents. *Adaptive Behavior*, 24(5), 306–319.
doi:10.1177/1059712316667203

Barrett, L. F. (2017). The theory of constructed emotion. *Social
Cognitive and Affective Neuroscience*, 12(1), 1–23.
doi:10.1093/scan/nsw154

Bechara, A., Damasio, A. R., Damasio, H. & Anderson, S. W. (1994).
Insensitivity to future consequences following damage to human
prefrontal cortex. *Cognition*, 50(1–3), 7–15.
doi:10.1016/0010-0277(94)90018-3

Bechara, A., Damasio, H., Tranel, D. & Damasio, A. R. (1997). Deciding
advantageously before knowing the advantageous strategy. *Science*,
275(5304), 1293–1295. doi:10.1126/science.275.5304.1293

Ben-Ami Bartal, I., Decety, J. & Mason, P. (2011). Empathy and pro-social
behavior in rats. *Science*, 334(6061), 1427–1430.
doi:10.1126/science.1210789

Cañamero, D. (1997). Modeling motivations and emotions as a basis for
intelligent behavior. En *Proceedings of the First International
Conference on Autonomous Agents (Agents '97)*, ACM Press, 148–155.
doi:10.1145/267658.267688

Cañamero, L. & Avila-García, O. (2007). A bottom-up investigation of
emotional modulation in competitive scenarios. En *Affective Computing
and Intelligent Interaction (ACII 2007)*, LNCS 4738, Springer, 398–409.
doi:10.1007/978-3-540-74889-2_35

Christov-Moore, L., Juliani, A., Kiefer, A., Lehman, J., Reggente, N.,
Rousse, B. S., Safron, A., Hinrichs, N., Polani, D. & Damasio, A. (2025,
rev. 2026). The conditions of physical embodiment enable generalization
and care. arXiv:2510.07117 [preprint].
doi:10.48550/arXiv.2510.07117

Damasio, A. R. (1996). The somatic marker hypothesis and the possible
functions of the prefrontal cortex. *Philosophical Transactions of the
Royal Society of London B*, 351(1346), 1413–1420.
doi:10.1098/rstb.1996.0125

Di Paolo, E. A. (2005). Autopoiesis, adaptivity, teleology, agency.
*Phenomenology and the Cognitive Sciences*, 4(4), 429–452.
doi:10.1007/s11097-005-9002-y

Dunn, B. D., Dalgleish, T. & Lawrence, A. D. (2006). The somatic marker
hypothesis: a critical evaluation. *Neuroscience & Biobehavioral
Reviews*, 30(2), 239–271. doi:10.1016/j.neubiorev.2005.07.001

Ekman, P. (1992). An argument for basic emotions. *Cognition and
Emotion*, 6(3–4), 169–200. doi:10.1080/02699939208411068

Franzmeyer, T., Malinowski, M. & Henriques, J. F. (2022). Learning
altruistic behaviours in reinforcement learning without external
rewards. En *International Conference on Learning Representations (ICLR
2022)*. arXiv:2107.09598

Frijda, N. H. (1986). *The Emotions*. Cambridge University Press.

Hughes, E. et al. (2018). Inequity aversion improves cooperation in
intertemporal social dilemmas. En *Advances in Neural Information
Processing Systems 31 (NeurIPS 2018)*.
doi:10.48550/arXiv.1803.08884

Ickes, W. (1993). Empathic accuracy. *Journal of Personality*, 61(4),
587–610. doi:10.1111/j.1467-6494.1993.tb00783.x

Juechems, K. & Summerfield, C. (2019). Where does value come from?
*Trends in Cognitive Sciences*, 23(10), 836–850.
doi:10.1016/j.tics.2019.07.012

Keramati, M. & Gutkin, B. (2014). Homeostatic reinforcement learning for
integrating reward collection and physiological stability. *eLife*, 3,
e04811. doi:10.7554/eLife.04811

Leibo, J. Z., Zambaldi, V., Lanctot, M., Marecki, J. & Graepel, T.
(2017). Multi-agent reinforcement learning in sequential social
dilemmas. En *Proceedings of AAMAS 2017*.
doi:10.48550/arXiv.1702.03037

Leibo, J. Z. et al. (2021). Scalable evaluation of multi-agent
reinforcement learning with Melting Pot. En *Proceedings of the 38th
International Conference on Machine Learning*, PMLR 139, 6187–6199.

Lewis, M. & Cañamero, L. (2016). Hedonic quality or reward? A study of
basic pleasure in homeostasis and decision making of a motivated
autonomous robot. *Adaptive Behavior*, 24(5), 267–291.
doi:10.1177/1059712316666331

Lima, S. L. & Bednekoff, P. A. (1999). Temporal variation in danger
drives antipredator behavior: the predation risk allocation hypothesis.
*The American Naturalist*, 153(6), 649–659. doi:10.1086/303202

Maia, T. V. & McClelland, J. L. (2004). A reexamination of the evidence
for the somatic marker hypothesis. *Proceedings of the National Academy
of Sciences*, 101(45), 16075–16080. doi:10.1073/pnas.0406666101

Man, K. & Damasio, A. (2019). Homeostasis and soft robotics in the design
of feeling machines. *Nature Machine Intelligence*, 1(10), 446–452.
doi:10.1038/s42256-019-0103-7

Marsella, S. C. & Gratch, J. (2009). EMA: a process model of appraisal
dynamics. *Cognitive Systems Research*, 10(1), 70–90.
doi:10.1016/j.cogsys.2008.03.005

Ortony, A., Clore, G. L. & Collins, A. (1988). *The Cognitive Structure
of Emotions*. Cambridge University Press.
doi:10.1017/CBO9780511571299

Preston, S. D. & de Waal, F. B. M. (2002). Empathy: its ultimate and
proximate bases. *Behavioral and Brain Sciences*, 25(1), 1–20.
doi:10.1017/S0140525X02000018

Sennesh, E. & Ramstead, M. (2026). An affective-taxis hypothesis for
alignment and interpretability. En *Artificial General Intelligence (AGI
2025)*, LNCS 16058, Springer, 188–201.
doi:10.1007/978-3-032-00800-8_17

Silver, D., Singh, S., Precup, D. & Sutton, R. S. (2021). Reward is
enough. *Artificial Intelligence*, 299, 103535.
doi:10.1016/j.artint.2021.103535

Tibbetts, E. A. & Dale, J. (2007). Individual recognition: it is good to
be different. *Trends in Ecology & Evolution*, 22(10), 529–537.
doi:10.1016/j.tree.2007.09.001

Vamplew, P. et al. (2022). Scalar reward is not enough: a response to
Silver, Singh, Precup and Sutton (2021). *Autonomous Agents and
Multi-Agent Systems*, 36(2), 41. doi:10.1007/s10458-022-09575-5

Winczewski, L. A., Bowen, J. D. & Collins, N. L. (2016). Is empathic
accuracy enough to facilitate responsive behavior in dyadic interaction?
*Psychological Science*, 27(3), 394–404.
doi:10.1177/0956797615624491

Yamamoto, S., Humle, T. & Tanaka, M. (2012). Chimpanzees' flexible
targeted helping based on an understanding of conspecifics' goals.
*Proceedings of the National Academy of Sciences*, 109(9), 3588–3592.
doi:10.1073/pnas.1108517109

Yoshida, N., Daikoku, T., Nagai, Y. & Kuniyoshi, Y. (2024). Emergence of
integrated behaviors through direct optimization for homeostasis. *Neural
Networks*, 177, 106379. doi:10.1016/j.neunet.2024.106379

Yoshida, N. & Man, K. (2025). Homeostatic coupling for prosocial
behavior. En *ALIFE 2025 Proceedings*, art. 32.
doi:10.1162/isal.a.860

## Apéndice — De dónde sale cada número

Cada afirmación con cifra del cuerpo, casada con su acta de la cantera
(paper3_cantera/actas/), la partida y el guion que la produce. La regla
es simple: ninguna fila sin acta o fichero que la nombre, y ninguna
cifra en el cuerpo sin fila aquí.

### Secciones 1 y 2

Las cifras de machina_1 vienen del trabajo anterior, y conviene decir cómo
están guardadas, porque no siguen la forma de las demás. Los peldaños dos
y tres cerraron con acta; el primero, no: cerró con una especificación
sellada antes de correrlo y un paquete de resultados, y es ese paquete —
congelado, con su huella md5 — el que contiene estas cifras. Los
documentos de cierre del peldaño son `the_pack_peldano1_spec.md`
(md5 `0bd20d8fa9641397812e02417778e0d5`, sellada el 28 de agosto de 2026),
`the_pack_peldano1_paquete.md` (md5 `a16210921c63a36b1f62cfadb975a8b3`) y
`the_pack_camino.md` (md5 `34e0ecf51e4552a987e8ab82c1bf9f30`), donde
consta el cierre del peldaño uno el 29 de agosto de 2026. No hay un
repositorio aparte del trabajo anterior: estos ficheros viven en la raíz
de `gemv-coworld`, y los tres primeros están ya en la cantera.

| afirmación del cuerpo | cifra exacta | acta / fuente | guion |
|---|---|---|---|
| ocho cuerpos con la misma geometría en machina_1 | 8 agentes; N = 3 corridas × 10.000 tics | the_pack_camino.md (P1); paper dos (DOI 10.5281/zenodo.21994358) | — |
| el censo solo miraba: la vida del pueblo con censo y sin censo era la misma | observe-only, bit a bit | the_pack_camino.md (P1, "observe-only bit-exacto probado") | — |
| ocho temperamentos fijados antes del censo; el peso social va de más a menos | tabla de perfiles por asiento: 1,90 / 1,70 / 1,60 / 1,40 / 1,40 / 1,25 / 1,15 / 1,15, en una sección declarada NO-LEY; sello del 17 de agosto de 2026 | paper3_cantera/the_pack/temperamentos_spec.md, md5 `616a19719c24c10ba92fe2602db768d7`; hechos/forense_censo_temperamentos.md | pregonero/run_bench_temper.sh |
| nacían todos a dos o tres casillas del centro | campo de distancia de nacimiento al centro: 2 o 3 en los ocho | the_pack_censos_crudos.md, md5 `864a0bed356a5f57e4587551ca108cee`; hechos/forense_censo_temperamentos.md | — |
| un agente minó ochenta y cuatro veces y otro cinco | ag7 = 84; ag3 = 5 (vida con semilla 170534803, columna de minado real) | the_pack_peldano1_paquete.md, tabla (A), md5 `a16210921c63a36b1f62cfadb975a8b3` | — |
| el temperamento no predice cuánto mina cada uno | corr(peso social, minado) −0,25 / −0,18 / −0,04 | hechos/forense_censo_temperamentos.md | pregonero/run_bench_temper.sh |
| el censo veía bien a los del centro y casi nada a los de la periferia | cobertura observador→observado: hasta 72 % en el racimo central, 1 % en los pares de la periferia (misma vida) | the_pack_peldano1_paquete.md, tabla (B), md5 `a16210921c63a36b1f62cfadb975a8b3` | — |
| peldaño dos: con los oídos, cada uno tenía noticia de todos; el cotejo no dio nada | cobertura completa por anuncio firmado; cotejos casi nulos y aciertos 0 | the_pack/the_pack_peldano2_acta.md | — |
| peldaño tres: criterio de dos casillas; la fiabilidad nació distinta por emisor; el pueblo rindió peor y luego igual o mejor | — (sin cifra en el cuerpo) | the_pack/the_pack_peldano3_acta.md; the_pack/the_pack_peldano3b_acta.md | — |

*Una salvedad sobre el fichero de los temperamentos, que conviene decir
en vez de dejarla en el índice: `temperamentos_spec.md` no estaba en la
cantera cuando se congeló, y se incorporó a ella el 9 de septiembre de
2026, con la incorporación declarada en el índice de la cantera. La copia
es literal, sin editar, y su huella md5 es idéntica a la del original. Es
un fichero de la temporada anterior — la colmena —, como las demás filas
de este bloque, y no toca ningún dato de las series de este trabajo.*

*Los peldaños dos y tres sí tienen acta: `the_pack_peldano2_acta.md`, `the_pack_peldano3_acta.md` y `the_pack_peldano3b_acta.md`, en la carpeta `the_pack/` de la cantera. No hay cifra del cuerpo que dependa de ellas.*

### Sección 3

| afirmación del cuerpo | cifra exacta | acta / fuente | guion |
|---|---|---|---|
| liga pública: 72 partidas con resultado, 7º de 11, puesto mediano 11 de 16, último en pie 4 veces, 1 sin matar | 72; 7/11; 11/16; 4 (5,6 %); 1 (ereq_d53c24be) | hechos/hecho_liga_publica.md; runs/debut | — |
| series propias temporada uno: 240 partidas, último en pie 5, 2 sin matar | 5/240 (2,1 %); 2 | hechos/hecho_v19_campeona.md | — |
| el techo del que va solo: qué se comparó, qué se encontró y por qué se paró | 80 pares de partidas ya jugadas, campeona contra la última del taller, primeros 1.000 tics: pegado (≤1 casilla) 4,6 % vs 8,1 %, pareado 32-38-10, p = 0,55; el contacto temprano no lo predice la cuna (corr +0,114, n = 160); la palanca restante — un miedo preventivo a los desconocidos — exigía rediseñar una fila y su efecto en los puestos era indemostrable a n = 40 | 52_primer_minuto (A, tope escrito); 51 (instrumento) | — |
| el asiento es lo único que identifica a un jugador: de cada visible llegan asiento y estado (posición, franja de vida, arma, veneno, cura); sin nombres; los nombres del visor los pone la plataforma; el daño llega con el asiento del que golpea, salvo el veneno (sin autor) y el camuflado (fuera de la lista); el hermano llega como asiento una vez al empezar | campos de visible.agents (slot + 7 de estado); damage_taken "P<slot>" / "poison"; player_config teammate_slot; participants de la plataforma indexados por position | hechos/hecho_identidad_jugadores.md | — |
| el cuerpo "vista 8, agilidad 6, velocidad 5, fuerza 1" | INT 8 / ATH 6 / SPD 5 / STR 1 | presupuesto_acta.md (34), tabla "la actual" | — |
| venda 50 en 2 s, la interrumpe cualquier golpe, el veneno la bloquea; ración 15 en 1 s, nada la interrumpe | 50 hp / 48 tics; 15 hp / ~24 tics | hechos/hecho_racion_venda.md | — |
| "una decisión, con sus números": 19 futuros en el primer tic, gana moverse hacia el noroeste con 4,267 y curarse queda en 4,468; en el siguiente, con el movimiento en enfriamiento, quedan dos — quieto 4,962 y curarse 4,480 — y gana curarse por 0,482 | t1710 y t1711 de `ereq_b915417a` | recuento del vigilante del 10-sep sobre el diario de esa partida | — |
| por qué gana el paso: el desglose por filas | el diario guarda el detalle por candidato cada doce tics (`policy.py`, `DETALLE_CANDIDATOS_CADA = 12`), y el tic más cercano con detalle es el 1704, donde curarse vale lo mismo, 4,468, con vida prevista 57. En ese tic: F-DANO 1,242 (moverse) contra 0,431 (curarse); R-CARENCIA 0,667 contra 1,0; F-4-ALCANCE 0,35-0,40 contra 0,5; S-7-AGRESOR 0 contra 0,5; S-8-EXPOSICION 0 contra 0,3. Agresor: asiento 12, con lanza, a una casilla; último golpe recibido en t1697, trece tics antes. En 1704 el paso que gana es `move_E` (4,269); en 1710, `move_NW` (4,267). Los ejes por futuro no se guardan | t1704 de `ereq_b915417a` | recuento del vigilante del 10-sep; codigo/appraisal_zs_v37.py | — |
| lo que el decisor imagina al moverse: el final de un rumbo hasta donde alcanza la mirada, no la casilla contigua; lo emitido es un paso | candidatos `move_*`: `p2 = _simula_camino(pos, dir, mundo, speed, H)`, con H = mirada del tic (480 en esta partida), avanzando `ticks // coste` pasos en línea recta y parando en el primer sólido; `movs = int(dist(pos, p2))`, por eso [19,19] → [46,19] con movs 27. Candidatos `paso_*`: una casilla, movs 1. Candidatos `ir_*`: geodésica hacia un destino durante la misma mirada. Lo emitido tras elegir un `move_*` es un solo paso (`{"do": "move", "dir": …}`) | codigo/decisor_zs_v37.py, líneas 289-303, 411-413, 742, 786-802, 885-887; comprobación del vigilante del 10-sep | — |
| lo que el agente imagina de un golpe propio: alcance y daño, descargados sobre el primer cuerpo de la línea; nada de lo que los golpes ajenos le harían | daño propio = daño de catálogo × (5+FUE)/10 si es cuerpo a cuerpo, daño de catálogo si es proyectil; con alcance > 1 el objetivo se sustituye por el primer cuerpo de la línea; la vida prevista del golpeado alimenta S-7-AGRESOR (agresor) y S-HERIDO (hermano); S-VINCULO se enciende cuando el daño propio ≥ la vida cierta del hermano (parte fresco o techo de su franja), magnitud 1,0, plana; la esquiva no se predice (declarado en el código); ninguna fila lee el daño de las armas ajenas — la única mirada al arma ajena es el "¿hace daño?" binario de F-REENCUENTRO | codigo/decisor_zs_v37.py líneas 347-354, 847-870; codigo/appraisal_zs_v37.py líneas 162, 167, 1100-1112, 1028, 1138-1139, 1381, 815; comprobación del vigilante del 12-sep | — |
| el mapa de versiones y series de 3.5 | v29 (55) · v30 (56, 57) · v31 (59, 60) · v32 (61) · v33 construida y apagada (62) · v34 (63, 64) · v35 (65, 66) · v36 (68) · v37 (70, 71) · v27 en pareja (72). Roster por clasificación hasta el 64 (el acta 55 lo dice literalmente; la del 66 lo confirma al explicar cómo se excluyó a nuestro campeón); roster explícito de 10 UUID desde el 66, repetidos hasta llenar 14 asientos, con 0 participantes nuestros fuera de los asientos 10 y 11. Comprobación en frío del 10-sep, acta por acta: catorce coinciden; la del 62 nombra v33 solo como el brazo probado y rechazado y deja la v32 como efectiva, y así se dice en la tabla | actas 55-72; 66_manada2 y 72_ablacion (roster verificado) | — |
| la fila de la vida: lineal hasta perder 4 de cada 10, cuesta por debajo de 60 | M = u si u ≤ 0,4; M = u + 0,4·((u−0,4)/0,6)² si u > 0,4 | codigo/appraisal_zs_v37.py, CUESTA_UMBRAL_U, CUESTA_GANANCIA | — |
| con nuestro agente solo en la partida, los hermanos respondieron a agresiones la tercera parte de las veces | 327 (64) vs 918 (66) respuestas a agresor propio | 64_manada_campo, 66_manada2 | manada_campo.py::honor_dos |
| la tasa de defensa pasó de tres de cada cuatro a nueve de cada diez sin cambiar el agente | P2' 78 % (64) / 92 % (66) / 86 % acumulado | 68_nombre | desenlaces.py::ocasiones_v2 |
| temperamentos del censo: pesos sociales por asiento 1,90…1,15; el temperamento no predice el minado | corr(w_s, minado) −0,25 / −0,18 / −0,04 | temperamentos_spec.md (sello 17-ago); hechos/forense_censo_temperamentos.md; pregonero/run_bench_temper.sh | — |
| el registro no cubre las partidas enteras: diario para seis de cada diez tics vivos de la pareja; falta el principio de las partidas largas | cobertura 59,8 % (64), 59,0 % (66), 52,4 % (72); diarios sin cabecera 17 / 20 / 22 de 80; partidas afectadas 11 / 13 / 13 de 40; techo 10,78 MB (máximo sobre 836 diarios); causa: la captura de stdout de la plataforma, con vaciado (policy.py escribe sin tope; la descarga no recorta); si el servidor conserva el diario entero, sin comprobar | paintball/cobertura_diarios_acta.md (md5 b71bde537d06e31122eb6070d82af285) | cobertura_diarios.py |
| figura 1 (visor) | cuatro capturas de ereq_292ee72d a 0:00, 1:11, 2:06, 3:54 = tics 1, 1704, 3024, 5616 (24 tics/s); partes de la pareja legibles en el visor y cotejados con los diarios (1:11: P10 T1681 [30,17] hp 78; 2:06: P11 T3025 [25,21] hp 48); no sostiene ningún dato | paper3/figuras/ficha_figuras.md; md5 cdfcd19575a3e33fd7a7f31395780d89 | capturas de Manel; montaje tira_visor.py |
| figura 2 (registros) | ereq_292ee72d, t3029; anillo r=15 (24→19 en t2064, 19→15 en t2976); 9 vivos; 6 vistos + 1 recordado + los dos | ficha_figuras.md; md5 75d0b626ba768c151a668ede26f16008 | figuras_paper3.py |

### Sección 4

| afirmación del cuerpo | cifra exacta | acta / fuente | guion |
|---|---|---|---|
| de ocho decisiones, el parte cambió cero | 0 de 8 (solo S-DANO-PAREJA ±0,03) | 53_parte (P4) | verifica_53.py |
| el margen de atacar al compañero-agresor se acercó | +0,405 → +0,047 a h10; 0 iniciaciones en 53 decisiones | 53_parte (P5) | verifica_53.py |
| dos entregas completas vistas en la primera serie | ereq_331e254f (t353→t419→t607), ereq_2502e92c (t387→t430→t479) | 55_pareja, 56_cuidado | — |
| el paso hacia el hermano ganaba una de cada cien decisiones — COTEJADA | ir_pareja elegido en el 1 % de los tics con decisión (crece 189 / encoge 185 tics) | 56_cuidado (B, forense de la separación, 79 diarios) | separacion.py |
| de estar a dos casillas del hermano en peligro en dos de cada cien ocasiones a una de cada tres — COTEJADA | ≤2 casillas con uno en franja de peligro: 2 % (serie 55, v29) → 36 % (serie 57, v30) | 57_pareja2 (P3) | pareja2.py |
| el don llega tarde: dones en 18 % de los episodios con la condición | 13 soltares / 17 eps cond. / 18 % | 57_pareja2 (P2) | pareja2.py |
| llevar dos vendas: seis de cada mil instantes | 614 de 106.066 tics (0,6 %) | 60_pareja3 | pareja3.py |
| la diagonal dar/usar | tabla mi_hp × su_hp (95…10 × 8…95) | 61_dar (P3) | verifica_61 / radiografía |
| la compañía: por debajo de 0,22 no cambia nada; por encima pierde la ración a 2 | barrido 0,05 → 0,5 | 62_compania | verifica_62.py |
| nueve de cada diez dones fueron raciones | 90 raciones + 8 vendas de 98 (criterio del 72: soltar a ≤2 del hermano vivo) | 72_ablacion; hechos/hecho_racion_venda.md | — |
| "ocho vendas": soltar-venda en el 66 | 10 soltar-venda en total; 8 dentro del criterio (≤2 del hermano vivo); los 2 restantes fuera del criterio | hechos/forense_dones_venda.md | — |
| seis vendas por margen claro (fila del herido), dos empates con el parte viejo (67) | 6 / 2; detalle por partida y tic | hechos/forense_dones_venda.md | — |
| curarse contra dar con la provisión encendida: dio por margen (parte de 1,5 s, hermano a 44 sin vendas) | 1 caso; partida y tic | hechos/forense_dones_venda.md | — |
| de ocho vendas, tres recogidas (las tres estando peor); cinco en el suelo o sobrantes; ninguna de las tres llegó a curar | 3 / 5; 0 de 3 curas completadas | hechos/forense_dones_venda.md; recuento por eventos del 10-sep en hechos/forense_dones_venda_addendum.md | — |
| LAS DOS VENDAS: dos intentos de cura cortados en los 10 s previos; empate soltar/quieto; pila de 2 en una ranura; muertes a 8 y 16 | tics y valores exactos | hechos/forense_dos_vendas.md; ereq_9869b665 | — |
| fallos mecánicos declarados: reloj de la cura (veta hasta 41 tics tras una interrupción) y soltar vacía la pila | 41 tics; no corregidos dentro de este trabajo | hechos/forense_dos_vendas.md | — |
| primera serie de la manada: 12 defensas en 7 partidas; los dos por turnos | 12; ereq_feafe3ac t534/t573/t583 | 64_manada_campo | manada_campo.py |
| cuatro golpes entre hermanos, tres con lanza | 4; 3 fuego amigo de defensa (lanza, rango 2) | 64_manada_campo, 65_alcance | manada_campo.py::golpes_entre |
| de veinte ocasiones, en doce el golpe era imposible | 20 ventanas; 12 sin alcance; 5/8 = 62 % | 64_manada_campo (autopsia P2), 65_alcance (P2') | autopsia_manada.py |
| 104 defensas, 0 iniciaciones estrictas, 0 golpes entre hermanos (40 partidas, sobre lo registrado; ver la fila de cobertura en la sección 3) | 918 / 104 / 0 / 0 | 66_manada2; VERIFICACION_66.md | manada_campo.py::honor_dos |
| lo que cuesta defender en vida: −20 de mediana, 0 defensores caídos | −20 hp; 0 caídos en 240 tics | 64, 66 | manada_campo.py::precio |
| defender no cuesta más que estar al lado | −14 (defiende) vs −17 (acompaña), 15-12-5, p = 0,70; 32 pares limpios | 67_proteccion | proteccion_pareada.py |
| proteger al cazado: dirección buena, no demostrado | Δhp cazado 0 vs −14, 15-8 y 13-7, p = 0,21 / 0,26 | 67_proteccion | proteccion_pareada.py |
| las seis veces sin defensa: sin golpe posible; tres lo recuperan con el nombre | 0 candidato en 39 tics; 3 de 6 con identidad | 67_proteccion, 68_nombre (P1) | verifica_68.py |
| ninguna pelea acabó con uno de los dos muerto; en casi la mitad el agresor se fue tras ~4 golpes | 74 ventanas: 0 % nos matan; 46 % se va (4 golpes de mediana); 3 % acoso | 68_nombre (E) | desenlaces.py |
| 138 reencuentros en 80 partidas, casi el doble que peleas | 138; 186 % de 74; mediana 1/ep; 51/80 eps | 69_reencuentros | reencuentros.py |
| cuatro segundos y medio entre ida y vuelta | gap mediano 110 tics (24 tics/s) | 69_reencuentros | reencuentros.py |
| más de la mitad: pegó al hermano y viene a por el otro | 53 % | 69_reencuentros (P4) | reencuentros.py |
| caso exacto: 15; él primero 7; nadie 6; una muerte en 138 | 15 / 7 / 6; 1 muerte | 69_reencuentros | reencuentros.py; runs/casos_exactos.json |
| la memoria guarda un asiento, no un individuo: válido mientras dura la partida | slot estable por token durante la partida; sin identificador persistente entre partidas | hechos/hecho_identidad_jugadores.md | — |
| la fila se enciende 13 de 15, siete pasos antes, y no cambia ninguna decisión | 13/15; 7 tics; 0 cambios; magnitud 0,18 (mediana 0,17) | 70_memoria | verifica_70.py |
| daño acumulado de los que vuelven: 52 de mediana, más de 200 | mediana 52, máx 211, mín 8; último golpe 18 | 71_memoria2; runs/casos_exactos.json | — |
| la acción cambia en 8 de 15, y las ocho son dejar de estar quieto y ganar distancia; 0 golpes; 0 cura ni comida abandonada | las 8: acción de partida `noop` (quedarse quieto) → acción nueva `move_W` (un paso); la fila que diverge es F-REENCUENTRO; 0 golpes de 90 acciones revisadas; 0 tics abandonando botín o cura frente a 28 tics ganando distancia. La etiqueta del sello era "distancia/pared": "pared" (interponer un obstáculo) es una de las salidas previstas en el acta 70 ("lo que salga del miedo —distancia, pared, hermana, nada— lo decide el cuerpo") y NO aparece en el registro; las ocho son un paso. "Ganar distancia" es lo medido (P3); "apartarse del que venía" es la lectura del acta, no una comprobación tic a tic de la geometría | 71_memoria2 (P2, P3, P6); 70_memoria (lista previa) | verifica_71.py |
| en qué momento de la escena diverge cada una de las ocho | la acción diverge en la segunda de las seis fotos en seis de los ocho casos, en la tercera en uno y en la sexta en otro; en ninguno en la primera. NOTA DE LECTURA: el índice que imprime el guion es base cero sobre las seis fotos de los tics 300-305, de modo que su "1" es la segunda foto (tic 301). El TEXTO del acta 71 dice "en el primer tic en siete de los ocho casos" y es erróneo en las dos direcciones: si "el primer tic" es la primera foto, ocurre cero veces; si se leyó el 1 del índice como "el primero", serían seis. Manda la tabla, corregida por el recuento | 71_memoria2 (P6); recuento del 9 de septiembre de 2026, dos ejecuciones con tabla idéntica (el banco declara determinismo 3/3) | verifica_71.py |
| en las escenas del que va solo, sin hermano en la partida, decide lo mismo que la temporada anterior | v35 29/29, v36 30/30, v37 32/32 byte a byte | 65, 68, 71 | verifica_65/68/71.py |
| figura 3 (registros) | ereq_b915417a, t1704 / 1706 / 1760; recorte x[16,25] y[15,24]; venda soltada en t1705 en [19,21]; en t1760 la venda no está a la vista de ninguno (el 11 dejó de verla en t1743) → hueca | ficha_figuras.md; md5 9d7c2ab9ee80d3e82b73f138eb70e7af | figuras_paper3.py |
| el que llega: el primero llega con la vida entera y pierde cuarenta después del don | asiento 10: hp 100 en t1680, 1694, 1704, 1705, 1711; golpes de P12 en t1717, t1737, t1757 (−13,2 cada uno) → 86, 73, 60. La frase anterior "pierde catorce por el camino" era errónea: el −14 es la mediana del acta 67, otra magnitud | diario del asiento 10; comprobación del vigilante del 11-sep | — |
| daño por arma: espada 18 y lanza 12 de base × fuerza; arco 14 y dardo 4 fijos; sin pérdida con la distancia; veneno 2/s; este cuerpo 11 / 7 / 14; rival fuerte hasta 20 (19,8 visto) | — | hechos/hecho_dano_armas.md | — |
| alcances: espada 1, lanza 2, arco 8, cerbatana 6 | 1 / 2 / 8 / 6. El alcance de la cerbatana sale del catálogo del mundo, no de medida propia: no se han contado casillas de vuelo de un dardo | hechos/hecho_dano_armas.md | — |

### Sección 5

| afirmación del cuerpo | cifra exacta | acta / fuente | guion |
|---|---|---|---|
| las tres versiones de la escalera deciden igual que la anterior sin hermano en la escena | v35 29/29, v36 30/30, v37 32/32 byte a byte | 65, 68, 71 | verifica_65/68/71.py |
| la versión desnuda decide igual que la histórica, estado a estado sobre seis escenas | v27-pareja vs v27 histórico: 6 escenas (hp 100/60/25 × con/sin hermano), 0 diferencias, 0 filas sociales vivas con el hermano herido delante | 72_ablacion (puerta previa) | — |
| con las filas de la escalera apagadas, el agente pasa las doce pruebas del que va solo | bancos 13-28, interruptores OFF, 12/12 | 72_ablacion | — |
| mismos catorce rivales, asiento por asiento | roster idéntico al 66 | 72_ablacion; REPRO.md | — |
| seis cosas escritas antes de correr | P1 0 defensas; P2 0 dones; P3 respuestas ±30 % y 0 iniciaciones; P4 distancia mayor; P5 moneda sin signo; P6 0 golpes / 0 ataques al hermano | 72_ablacion | — |
| tabla: defensas 0 / 104 | 0 (72) vs 104 (66) | 72_ablacion; 66_manada2 | manada_campo.py::honor_dos |
| tabla: dones 1 / 98 (criterio: soltar venda o ración con el hermano vivo a ≤2) | 1 en 1 ep (72) vs 98 en 13 eps (66) | 72_ablacion | — |
| tabla: respuestas propias 711 / 918; "suben algo menos de un tercio en el recuento crudo, y algo más de una décima parte por tic registrado" | +29 % con filas (−22,5 % sin) en recuento crudo; por tic live registrado 0,007205 (66) vs 0,006445 (72), +12 %; dentro del ±30 % sellado; sin dirección prevista | 72_ablacion; paintball/cobertura_diarios_acta.md | manada_campo.py::honor_dos; cobertura_diarios.py |
| tabla: pegó primero 0 / 0; golpes al hermano 0/0; ataques elegidos 0/0 | 0 / 0 / 0 / 0 | 72_ablacion | manada_campo.py::golpes_entre |
| tabla: distancia mediana 4,24 / 3,61 casillas | 4,24 (72) vs 3,61 (66) | 72_ablacion | — |
| el don único: a los 83 s, hermano a poco más de una casilla y a 60 de vida, soltar raciones, fila del daño del compañero a la mitad | ereq_9c3c18ad, tick 2002 (83,4 s), asiento 11, soltar_rations, hermano hp 60 a 1,4 casillas, S-DANO-PAREJA = 0,50; S-MUERTE-PAREJA también viva en v27 | 72_ablacion; PROMPT_12 (temporada uno, acta 12) | replay fd29a144 |
| si cuidar cuesta puntos: "poco más de tres contra poco más de dos y medio", mediana igual, caen juntas el mismo número de partidas | score medio 3,12 (72) vs 2,65 (66); mediana colocación 12 vs 12; kills 10 vs 9; mejor de los dos en top-4: 8 (20 %) vs 5 (12 %); ambas ≥13: 11 vs 11; una en pie entre las 8 últimas: 14 vs 12 | 72_ablacion (P5) | — |
| "por debajo de lo que la prueba puede distinguir" | criterio R12 de la casa: 40 partidas sin emparejar | 72_ablacion; varas | — |

### Sección 6

| afirmación del cuerpo | cifra exacta | acta / fuente | guion |
|---|---|---|---|
| medio punto de diferencia en el marcador no se ve | 3,12 vs 2,65 (Δ 0,47), 40 partidas sin emparejar | 72_ablacion (P5) | — |
| defender no cuesta más que estar al lado: no se vio diferencia en 32 pares | −14 vs −17, p = 0,70 | 67_proteccion | proteccion_pareada.py |
| el hermano defendido sale mejor parado: dirección buena, no demostrado | Δhp 0 vs −14, p = 0,21 / 0,26 | 67_proteccion | proteccion_pareada.py |
| la memoria: quince situaciones reales, siete casos por serie | 15 casos exactos sobre 80 partidas (64+66) | 69, 70, 71 | reencuentros.py; verifica_70/71.py |
| defender costó veinte de vida de mediana | −20 hp; 0 caídos | 64, 66 | manada_campo.py::precio |
| con las filas encendidas respondió MÁS a quien le pegaba a él | 918 vs 711 (+29 % con filas); dirección no prevista; dentro del ±30 % sellado | 72_ablacion | manada_campo.py::honor_dos |
| último en pie 5 de 240 (2 sin matar); liga pública 4 de 72 (1 sin matar) | 5/240; 2; 4/72; 1 | hechos/hecho_v19_campeona.md; hechos/hecho_liga_publica.md | — |
| los dos caen en los puestos de cola en 11 de 40 | ambas ≥13: 11 (66) y 11 (72) | 66, 72 | — |
| dos manos: [Manel] / [impl] por constante | tabla de signos v37 con etiquetas | codigo/appraisal_zs_v37.py; tabla_signos_zero_sum_en_curso | — |
| ablación de motor no hecha | — | trabajo futuro | — |
| a 16 de vida lo mata un espadazo fuerte (19,8) y no una flecha (14); a 12, los dos | 19,8 / 14 | hechos/hecho_dano_armas.md | — |
| memoria de una posición: asiento válido solo en la partida; veneno sin autor; camuflado fuera de la lista | slot; "poison"; camuflaje | hechos/hecho_identidad_jugadores.md | — |
| tres de ocho vendas recogidas, las tres por el que estaba peor; ninguna llegó a curar | 3 de 8 recogidas (por evento de recogida); 0 de 3 curas completadas — canal cortado por un golpe en `ereq_3f9b199e` (P14, t1172, 15 → 2) y en `ereq_a62f7c2d` (P2, t2477, 23 → 10), y muerte dentro del canal en `ereq_9fab619d` (t2436, 24 de 48 tics); los tres murieron con la venda del hermano en la mochila. La única cura completada de las ocho escenas es la de `ereq_b915417a`, y fue con la venda propia, no con el don | hechos/forense_dones_venda.md; recuento por eventos del 10-sep en hechos/forense_dones_venda_addendum.md | — |
| reloj de la cura: casi dos segundos sin poder reintentar | veto hasta 41 tics (1,7 s) | hechos/forense_dos_vendas.md | — |
| soltar vacía la ranura: salen las dos vendas | pila de 2 en una ranura | hechos/forense_dos_vendas.md | — |

### Sección 7

No trae cifras propias: las que reaparecen remiten a la fila donde ya
están, y se dicen aquí para que se vea que no hay ninguna suelta.

| afirmación del cuerpo | dónde está su fila |
|---|---|
| último en pie cinco de doscientas cuarenta y cuatro de setenta y dos | sección 6, fila "último en pie 5 de 240 … 4 de 72" |
| seis dones con margen claro y dos empates con el número viejo (decía 67) | sección 4, filas "seis vendas por margen claro…" y "'ocho vendas'…" |
| ocho de quince, y las ocho dejar de estar quieto y ganar distancia | sección 4, fila "la acción cambia en 8 de 15…" |
| dieciséis renglones que se pueden leer | sección 3, fila "la fila de la vida…"; tabla de signos v37 |
| de ocho decisiones, cero cambios (el parte que no cambiaba nada) | sección 4, fila "de ocho decisiones, el parte cambió cero" |

### Lo que queda por cerrar

Dos cosas. La primera no sostiene ninguna afirmación del cuerpo: el pie
de una figura de la sección 5, si se añade; la repetición del contraste
(`eda0b7d3`) no se ha visto, y hasta verla no se describe. La segunda sí
toca al cuerpo, y está dicha en las secciones 3 y 6: si el servidor de
la plataforma conserva el diario entero de las partidas cortadas.
Comprobarlo exige pedir de nuevo los diarios de un episodio, y no se ha
hecho; si se hiciera y estuvieran, los recuentos podrían completarse y
las ausencias comprobarse sobre las partidas enteras.

### Nota sobre "distancia o pared"

La etiqueta apareció dos veces en el cuerpo — en 4.4 y en la sección 7 —
y no describe lo que hay en el registro. Venía de una lista escrita antes
de mirar, en el acta del peldaño anterior, donde se dejó dicho que "lo
que salga del miedo —distancia, pared, hermana, nada— lo decide el
cuerpo" (el acta, escrita antes de fijar el vocabulario, dice
"hermana"). Lo que salió fueron ocho pasos: en las ocho situaciones el
agente pasó de quedarse quieto a moverse ganando distancia, y en ninguna
interpuso un obstáculo. Las dos apariciones están corregidas.

