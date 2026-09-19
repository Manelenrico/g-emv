# G-EMV: emoción y razón en un agente. Cuándo hace falta pensar

Manel Enrico\
Investigador independiente, Barcelona\
ORCID: 0009-0008-1732-6310\
Preprint, versión 1, 2026\
Primera parte de una serie nueva, emoción y razón en un agente. Antes hubo una trilogía: el motor [1], la colmena [2], la manada [3].\
[1] Enrico, M. (2026). G-EMV: A Geometric Architecture of Homeostatic Orientation for Agents. Zenodo. DOI 10.5281/zenodo.21026795.\
[2] Enrico, M. (2026). G-EMV: the Hive. Instinct Suffices: a Whole Life Without Reward. Zenodo. DOI 10.5281/zenodo.21994358.\
[3] Enrico, M. (2026). G-EMV: the Pack. Care Without Reward in a World That Pays for Killing. Zenodo. DOI 10.5281/zenodo.22713650.

## Resumen

¿Cuándo hace falta pensar? Un cuerpo que decide veinticuatro veces por
segundo, sin recompensa ni aprendizaje, lleva tres trabajos viviendo
en mundos ajenos guiado solo por lo que le duele, lo que le alivia y
lo que le atrae. Aquí se le pone al lado una cabeza que habla, un
modelo de lenguaje que lee la escena y un manual del mundo y propone
en palabras, y se mide qué le añade. El cuerpo conserva la última
palabra: cada propuesta entra en su lista de futuros imaginados como
una más, puntuada con la misma tabla. En ciento treinta partidas de
ZERO-SUM, un mundo de Softmax cuyo marcador paga por sobrevivir y por
matar, la cabeza habló una vez cada cuatro segundos y el cuerpo le
hizo caso en una propuesta de cada diez; la mitad de esas veces, para
hacer lo que ya iba a hacer. Ni el puesto ni los puntos se movieron
más allá del ruido. Contarle más, de cuatro maneras, cambió lo que
decía y no lo que el cuerpo hacía con ello; preguntada por lo que
harían los demás, perdió contra suponer que nadie se mueve. Lo único
que cambió algo fue el reloj: retener su frase cuatro segundos redujo
a la mitad las veces en que se le hizo caso, casi tres desviaciones,
y una voz que propone sitios alcanzables al azar fue aceptada a una
tasa parecida. La respuesta que este trabajo da es sobre el mundo
tanto como sobre la cabeza: en un sitio donde siempre hay una amenaza
encendida, donde cada decisión dura cuarenta milisegundos, donde nadie
se reconoce de una partida a otra y no hay mañana, no hay nada sobre
lo que deliberar, y una cabeza que no puede volver a mirar llega
siempre tarde. Pensar necesita tiempo: un respiro sin amenaza, alguien
a quien reconocer, y decisiones cuyo efecto llegue más tarde que la
siguiente mirada. Ese mundo no se ha construido aquí; se ha medido, en
este, cada uno de los rasgos que le faltan. Los límites, sobre todo
que la puerta por la que entra el consejo no deja pasar un plan, se
declaran enteros.

*Palabras clave: homeostasis, arquitectura afectiva, modelo de
lenguaje, decisión encarnada, proceso dual, tiempo, alineamiento.*


## 1. La pregunta

**Primera parte de una historia nueva, que viene de otra.** Antes de
esta hubo una trilogía. El primer trabajo describió
un motor: una manera de que un agente artificial tenga necesidades que
tiran de él en direcciones opuestas y elija, a cada instante, el futuro
imaginado que más le acerca a donde quiere estar [1]. El segundo puso
ese motor a vivir solo en un mundo ajeno [2]. El tercero le dio un
hermano, y contó lo que hace con la vida de otro cuando esa vida se
puede perder [3]. Aquella historia era la de un cuerpo. Esta que
empieza es la de ese cuerpo y una cabeza que habla: cómo se encajan,
si se encajan, y qué mundo hace falta para que lo hagan. También
será de tres partes. Esta primera le pone la cabeza al lado y
pregunta qué añade.

**El cuerpo y el consejero.** Llamaremos cuerpo a lo que ya existía:
el motor, la tabla de lo que duele, lo que alivia y lo que atrae, y el
decisor que veinticuatro veces por segundo imagina un puñado de
futuros, los puntúa y elige uno. Llamaremos consejero a lo nuevo: un
modelo de lenguaje al que se le describe la situación con palabras y
que contesta con propuestas, también en palabras. El reparto es
estricto y no cambia en todo el trabajo: el consejero propone y
explica; el cuerpo imagina, puntúa y elige. El consejero no toca
ningún valor, no decide nada, y sus propuestas entran en la lista del
cuerpo como una más, puntuadas con la misma vara que las propias. Lo
único que puede hacer es ensanchar lo imaginable.

**Qué llamamos aquí emoción y qué llamamos razón.** Emoción, en esta
serie, no es un sentimiento que se declara: es la geometría del motor,
tres ejes, fuerzas que tiran en direcciones opuestas y una distancia
que descender, y una tabla que dice cuánto tira cada cosa. Es lo que
hace que algo importe antes de que nadie lo piense. Razón es aquí una cabeza que lee reglas, saca conclusiones, intenta
entender lo que siente el cuerpo y propone en palabras: un modelo de
lenguaje. Damasio sostuvo que una razón sin emoción no sirve para vivir, porque
nada le importa [4]. Este trabajo mira la pareja desde
el otro lado: una criatura a la que las cosas ya le importan, sin ninguna cabeza
que razone en palabras, lleva tres trabajos viviendo; ahora se le pone al lado
una razón y se mide qué le añade, en un mundo concreto y con números.
La respuesta de esta primera parte es que en un mundo como este,
donde cada decisión dura cuarenta milisegundos y siempre hay alguna
fila de daño encendida, la razón añadió casi nada; y que lo único que
se pudo cambiar y cambió algo fue el reloj, no la razón. La imagen
que usaremos es la de un consejero sabio sentado al lado de alguien
que cruza una autopista a pie: para cuando ha terminado la frase, el
coche ya ha pasado. Si el consejero sabe o no, aquí no se pudo
medir; lo que se midió es que lo que dice llega tarde, y que cada segundo
de más le cuesta: cuando su frase se retuvo cuatro segundos, el cuerpo
le hizo caso la mitad de veces.

**Con quién habla este trabajo.** La pieza más parecida a nuestra
puerta está en la robótica: en SayCan, un modelo de lenguaje propone
qué hacer y otra función, que no habla, puntúa si eso se puede hacer
aquí, y se elige el producto de las dos [5]; la diferencia es que allí
lo que puntúa es factibilidad y aquí es necesidad, lo que le duele a
un cuerpo. El cuerpo mismo tiene precedentes claros: el malestar como
distancia a un punto de equilibrio con varias necesidades a la vez,
que se reduce anticipando, viene de Keramati y Gutkin [6] y se ha
llevado a agentes que aprenden con visión [7]; la idea de que una
máquina con vulnerabilidad tendría algo parecido a sentimientos, y de
que eso sería la base y no el adorno de su inteligencia, es de Man y
Damasio [8]; y las emociones como reguladores de una arquitectura
motivacional en robots autónomos son una línea que Cañamero abrió en
los años noventa y sigue trabajando [9, 10]. Del lado de la cabeza,
hay una arquitectura de pensar rápido y lento hecha con modelos de
lenguaje [11], en la estela de Kahneman [12], pero en ella las
acciones sobre el mundo, las que pasan por herramientas, las hace el
lento; aquí es al revés. Y hay quien ha puesto modelos de lenguaje a
sobrevivir en mundos con escasez y ha visto que algunos atacan cuando
atacar está entre las acciones disponibles [13]; aquí el consejero
propuso iniciar un ataque en una de cada cinco llamadas y ninguno de
esos ataques salió del cuerpo, que solo construye el golpe contra
quien ya le pega. Lo más cercano a nuestra composición que hemos
encontrado es un regulador homeostático que modera las respuestas de
un modelo de lenguaje [14], pero allí quien responde sigue siendo el
modelo y el regulador le ajusta el tono; aquí quien actúa es el cuerpo
y el modelo solo propone. No encontramos ningún trabajo en que un
cuerpo con necesidades tenga la última palabra sobre un modelo de
lenguaje y se mida qué hace con sus propuestas: la novedad de este
trabajo es la composición y la medida, no las piezas.

**El mundo donde se prueba.** Es el mismo de la tercera parte:
ZERO-SUM, un mundo de Softmax en el que dieciséis jugadores entran por
parejas, un anillo se cierra desde los bordes y el marcador paga por
cada muerte y por sobrevivir, cuanto más mejor. Se juega a veinticuatro
pasos de reloj por segundo; una partida dura como mucho seis minutos y
medio, y nuestra criatura vivió en ellas, de media, menos de dos. No lo
diseñamos nosotros y no lo tocamos. Esa es su fuerza como banco de
pruebas y también, como se verá, el centro del resultado.

**Lo que se esperaba y lo que se encontró.** La esperanza era
razonable: un cuerpo que elige a golpe de instante debería agradecer
una cabeza que conoce el mundo por sus reglas, que ve más lejos y que
puede sugerir lo que al cuerpo no se le ocurre. Lo que se encontró fue
otra cosa. El consejero habla mucho y el cuerpo le hace poco caso;
cuando le hace caso, al menos la mitad de las veces es para hacer lo
que ya iba a hacer, y la otra mitad, muchas veces en el mismo instante en que su frase
llega; lo que parecía protección contra sus malas
ideas resultó ser incomprensión; y darle más información, de cuatro
maneras distintas, cambió lo que decía pero no lo que el cuerpo hacía
con ello. No leemos ninguna de esas cosas como un fallo del
consejero. Lo que sostendremos es que hablan del mundo en que se le puso a trabajar
tanto como de él: un mundo que decide cada cuarenta milisegundos, que
dura unos minutos y donde a nadie se le puede reconocer.

**La tesis, adelantada.** El cuerpo vuelve a decidir veinticuatro
veces por segundo; el consejero habla una vez cada cuatro segundos y no puede rectificar
lo que dijo hasta la vez siguiente. Se midió qué pasa cuando su
frase llega cuatro segundos más tarde: el cuerpo le hace caso la mitad
de veces. Y se midió qué pasa cuando en su lugar se pone una voz que propone al
azar un sitio alcanzable y lo mantiene cien instantes: el cuerpo le hace caso a una tasa parecida a la del consejero, sin que
la voz haya pensado nada. Así que la conclusión no
es que un razonador de lenguaje no sirva. Es que lo único que se vio que este mundo hace con un consejo es
elegirlo más cuando llega a tiempo; que una receta que persiste sin razonar se acepte
igual dice que durar cuenta, aunque no se midió cuánto; y si además se
aprovecha lo que el consejo dice, no lo pudimos separar aquí, y se
dice.
Que otro mundo, con tiempo, vecinos y mañana, sí
aprovecharía lo que dice, es la conjetura con la que termina el
trabajo, y cada rasgo de ese mundo sale de una medida de este.

**Cómo está contado.** Primero el cuerpo, con lo poco que hay que
saber de él y con lo único que se le añadió en este ciclo. Después el
mundo y su reloj, con los hechos medidos que deciden todo lo demás.
Después cómo se le pone la cabeza, qué pasó y por qué. Luego, cuándo
hace falta pensar. Al final, cómo se midió y hasta dónde llega. Los
números que sostienen cada frase están en el apéndice, en tablas y con
lo necesario para leerlos.

## 2. El cuerpo

**Lo justo para seguir la historia.** El cuerpo es el agente tal como
llegó a este trabajo, y aquí se cuenta solo lo que hace falta para
entender lo que viene; quien quiera el detalle lo tiene en las tres
partes anteriores. Tiene necesidades en tres ejes: cómo está su
cuerpo, cómo están sus recursos, y cómo están sus vínculos. Sobre esos tres
ejes hay un punto donde querría estar, y una distancia hasta él. Todo
lo que el cuerpo hace es intentar acortar esa distancia.

**La tabla de lo que duele, lo que alivia y lo que atrae.** Entre el
mundo y las necesidades hay una tabla: una lista de situaciones, cada
una con la fuerza con que tira del agente y en qué eje. Cuando en este
trabajo se dice que algo le duele o le atrae, se dice eso y nada más:
que una fila de la tabla tiene un valor mayor que cero y tira de esa
distancia; y cuando se dice que algo le alivia, que una fila de daño
que estaba encendida baja. No se afirma nada sobre lo que el agente
experimenta. En este ciclo la tabla tiene veintiuna filas. Veinte son
de daño: que te disparen, que el anillo se acerque, que te falte
comida. Ninguna es de alivio por sí misma: aliviar es que una fila de daño
baje. Y una sola es de atracción: la llamada de lo que hay
en el suelo, que tira hacia las cosas aunque no falte nada. De las
veinte de daño, dieciséis se encendieron alguna vez en las partidas de
este trabajo; las otras cuatro, dos apagadas a propósito y dos que
nunca encontraron ocasión, no cuentan nada en lo que sigue. La de
atracción estuvo viva en el cien por cien de los instantes. El mundo
siempre estaba llamando.

**Cómo decide.** Veinticuatro veces por segundo, el decisor toma un
puñado de futuros posibles, unos pocos de todos los que hay, y así lo
llamaremos, el puñado, porque es una mano de opciones y no la lista
entera; se imagina en cada uno y los puntúa con la tabla y con el
motor. El puñado se construye
con lo que ve y lo que lleva: unos cuantos sitios a los que podría ir,
las cosas que hay en el suelo, el hermano, curarse, y quedarse quieto;
y cambia de un instante a otro porque la escena cambia. Cada futuro es una foto
de sí mismo en otro sitio: calcula hasta dónde llegaría caminando
entre dos y veinte segundos, y puntúa cómo estaría al llegar. Elige el
futuro que más le acerca a donde quiere estar, y al instante siguiente
vuelve a empezar con otro puñado. Quedarse quieto está siempre entre
las opciones. No hay planes, no hay árbol de jugadas, no hay memoria
de otras partidas: solo un paso, elegido muy a menudo. Conviene
retener lo del puñado, porque al final explica mucho.

**Donde quiere estar no es donde no duele.** Conviene decirlo porque
cambia la lectura de todo lo demás. El punto hacia el que tira no es
el punto en que nada duele: está más allá, inclinado hacia la
abundancia. Cuando nada le duele, al agente todavía le queda más de la
mitad de su distancia por delante, y la pendiente apunta hacia tener
más de lo que necesita. Es una criatura que, estando bien, sigue
queriendo estar mejor. Lo que este mundo no le ha dado nunca es la
ocasión de estar bien: en seiscientos cuarenta mil instantes no hubo
uno sin alguna fila de daño encendida.

**Lo que se le añadió en este ciclo: sentir por el hermano.** Este es
el único añadido constructivo del trabajo, y va antes que la cabeza
porque cuenta mejor la historia. Tres filas nuevas en la tabla. Dos
van al eje del propio cuerpo, como si el daño fuera suyo: una baja,
cuando alguien tiene al hermano a tiro, y otra cuatro veces mayor,
cuando llega el parte de que le están pegando. La tercera va al eje de
los recursos: lo que al hermano le falta, cuando está herido y no
lleva con qué curarse. Ninguna dice qué hacer; dicen cuánto tira. Y
tiraron: en las partidas de este trabajo, la amenaza sobre el hermano
estuvo encendida uno de cada nueve instantes, su golpe uno de cada
cuarenta, y su falta uno de cada seis. Lo que esas filas no pueden
hacer es añadir un golpe, porque el cuerpo solo construye el golpe
contra quien ya le pega, a él o al hermano; son las filas que hacen
sentir, no las que hacen defender, que defender ya lo hacía el cuerpo
de la tercera parte. Se midió en seco, sobre cincuenta y cinco mil
instantes de partidas grabadas, qué decisiones cambian: una de cada
cuatrocientas, y casi siempre para apartarse, alguna vez para curar o
para soltar algo; ni un golpe nuevo, ni al hermano ni a nadie, y
ninguno con la propia vida en las últimas. Siente, se aparta, y no se
lanza a pegar por él. Entre los dos hermanos hay además un hilo: cada
dos segundos se mandan un telegrama fijo con dónde están, cómo tienen
la vida, qué llevan y quién les pega. No es conversación; es un parte.

**Lo que no hay.** No hay recompensa: el marcador no entra en lo que
percibe, y lo único que le guía es la distancia de arriba. No hay
aprendizaje: nada cambia de una partida a otra, y el consejero, que
viene entrenado de fábrica, tampoco aprende aquí. No hay guion de conducta: lo que está escrito es el repertorio, con
sus restricciones, como que el golpe solo se construye contra quien
ya pega; cuándo hacer cada cosa no lo dice nadie, lo decide la tabla
instante a instante. Y no hay nombres: el asiento es todo lo que sabe
de cada uno. Cada una de estas ausencias es una decisión, y las cuatro
se mantienen intactas cuando llega la cabeza.

## 3. El mundo y su reloj

**Una arena que paga por vivir y por matar.** ZERO-SUM se juega en una
arena, y así llamaremos al tablero: una cuadrícula de cuarenta y ocho
casillas de lado, con muro en el borde, donde entran dieciséis
jugadores inscritos por parejas. Un anillo se cierra desde los bordes
y quema a quien queda fuera; una partida podría durar seis minutos y
medio, el anillo termina de cerrarse a los cinco y cuarto, y nuestras
criaturas vivieron de media un minuto y cuarenta y tres segundos de
juego, sin contar la cuenta atrás.
Los puntos se reparten por cabeza y por orden de caída: el último que
queda en pie se lleva quince, el penúltimo doce, y así bajando hasta
cero para los dos primeros que mueren, más un punto por cada muerte
que uno cause. O sea que el mundo recompensa sobrevivir, cuanto más
mejor, y además recompensa matar. Nuestra criatura no ve nada de eso:
el marcador no entra en lo que percibe, y por tanto no puede
perseguirlo.

**El asiento, que es todo lo que se sabe de cada uno.** Cada jugador
ocupa un asiento numerado, y ese número es la única identidad que
existe dentro de la partida. Lo comprobamos en el protocolo entero:
quien se ve, quien dispara, quien recibe, quien habla, todos son
números de asiento. Los nombres existen fuera, en los registros que la
plataforma guarda para quien mira desde afuera, y nunca llegan al
jugador. Los rivales sí vuelven de una partida a otra, son los mismos
programas; lo que no vuelve es la manera de reconocerlos, porque
cambian de asiento. Esto, que parece un detalle, decide más adelante
qué se puede recordar de alguien y qué no.

**El azar manda, y se puede medir cuánto.** Para saber cuánto de lo que ocurre en una partida varía sin que uno
cambie nada, jugamos ciento
treinta partidas fijando el terreno: veinte mundos distintos, cada uno
jugado varias veces, con los mismos rivales, que solo cambian de
asiento. Repartida la variación en tres partes, la que queda al
repetir la misma partida con todo igual, la que añade rotar a los
rivales de asiento y la que añade cambiar de mundo, el resultado es
incómodo y es el que ordena todo el trabajo: del puesto final, el
ochenta y uno por ciento es de la primera parte, la que queda cuando
todo lo que se puede fijar está fijo; a esa parte la llamaremos azar,
y solo quiere decir eso. Del tiempo
que se vive, el azar se lleva el cincuenta y cinco por ciento, el
orden en que se sientan los rivales otro treinta y siete, y el terreno
solo el ocho. Fijar el mapa, que era nuestra esperanza de medir mejor,
controlaba la doceava parte del problema. En un mundo así, una serie de este tamaño no distingue un efecto
pequeño del ruido, y conviene decirlo antes de
enseñar los resultados y no después.

**Nunca hay calma.** En los seiscientos cuarenta mil instantes que
vivieron nuestras dos criaturas a lo largo de esas partidas, no hubo
uno solo sin alguna fila de daño encendida, y en noventa y nueve de
cada cien había dos o más. Siempre faltaba algo y siempre había algo
que las llamaba. Es un dato del mundo visto desde esta tabla, y explica una cosa que
se verá luego: que estar quieto aquí no es estar tranquilo. La figura
1 lo enseña en una sola vida.

![Figura 1. Una vida, instante a instante. Una partida corriente de
una criatura con consejero: de las catorce vidas del brazo con
consejero al que se le cuenta lo que siente, que duraron entre dos mil y tres mil quinientos instantes,
consultaron quince veces o más, lograron alguna aceptada y murieron
antes del final, esta es la mediana en aceptadas. Muere en el
instante dos mil trescientos setenta y dos del reloj de partida, a
los noventa y nueve segundos; descontada la cuenta atrás, unos dos
mil ciento treinta instantes de juego, ochenta y nueve segundos.
Muere en el puesto once. Arriba, la distancia a donde quiere estar, que nunca baja a
nada duele. Debajo, las cinco filas de la tabla que más tiraron en esa
vida, más intenso cuanto más tiran: la carencia y la llamada del suelo
nunca se apagan; la exposición se apaga mientras está escondida y
vuelve al final, cuando sale y muere. Después, la acción elegida en cada instante: quieto en negro, un
paso en blanco, se haya movido o no. Al pie, cada raya es una consulta al consejero,
diecisiete, y cada punto un instante en que el cuerpo le hizo caso:
seis, de tres propuestas.](fig/fig1_una_vida.png)

**Hay habla y no hay conversación.** Hablar es una acción como
cualquier otra en este mundo: cualquiera puede lanzar un mensaje a
todos o dirigirlo a un asiento concreto. Y se usa. En las ciento
treinta partidas oímos mil trescientos veintidós mensajes de rivales,
de siete de los catorce, construidos sobre siete frases fijas. No son
frases sordas a lo que pasa: la que dice te veo aparece tras recibir
un golpe trece veces más a menudo que por casualidad, la que dice no
soy una amenaza se dispara cuando el anillo aprieta, y el aviso de
dónde ha caído un paquete llega siempre dentro de los cuatro segundos
siguientes. Lo que no hay es respuesta. Doscientos cuatro de esos
mensajes venían dirigidos a nuestro número, y todos pedían algo, que
nos apartáramos; doscientos uno no fueron seguidos de nada desde
ningún asiento en los dos segundos siguientes, y tres de cada cuatro
seguían sin nada detrás veinte segundos después; en el cuarto restante hubo mensajes, noventa y cuatro, y ninguno iba
dirigido a quien había hablado. Si alguno le respondía por el canal abierto, no lo comprobamos. Y con
el cuerpo no se ve respuesta: en los dos segundos que siguen a un
apártate, de ciento nueve veces que se pudo medir, nos alejamos
treinta, nos acercamos veintiocho y no nos movimos cincuenta y una;
lo que habríamos hecho sin el mensaje no se comparó. El nuestro no
contestó con palabras porque nuestra criatura es muda con los
extraños. Conviene
decir esto con cuidado. No sabemos qué hay dentro de cada rival, si
un programa de reglas, un agente entrenado o un modelo de lenguaje
con instrucciones cerradas; una conducta de guion la produce
cualquiera de los tres. Lo que sabemos es que en ciento treinta
partidas nada de lo que pudimos oír fue contestado, nosotros
incluidos, y que nadie probó si contestar era posible, porque nadie lo
intentó. Y el guion no se ata a los hechos: la frase no soy una amenaza
para nadie la dijo dieciséis veces alguien que acababa de pegarnos.

**Una salvedad, declarada.** La plataforma entrega los mensajes de
canal de equipo a quien comparte pareja, y en la liga en solitario
nadie tiene pareja real, de modo que un mensaje así puede acabar en
manos de un rival cualquiera. Nuestra pareja sí es real, así que lo
nuestro no se ve afectado; y de los mil trescientos veintidós mensajes
que oímos, ninguno llegó por ese canal, así que nada de lo contado
viene de ahí. Pero la frase honesta no es que nadie conteste: es que
nada de lo que nosotros podíamos oír fue contestado. Dos rivales
respondiéndose por un canal mal entregado nunca habrían llegado a
nuestros oídos. Esta serie se jugó antes de que la plataforma
corrigiera ese reparto.

**Por qué estas cuatro cosas deciden el resto.** Un mundo donde el
azar manda, donde nunca hay un respiro, donde se habla y no se
contesta, y donde a nadie se le puede reconocer, es un mundo donde
casi todo lo que se puede hacer es reaccionar bien y deprisa. Las
páginas que siguen cuentan qué hizo una cabeza que habla dentro de
él. Conviene leerlas sabiendo que el sitio estaba puesto antes de que
la cabeza llegara.

## 4. El consejero: cómo se le pone

**Un modelo de lenguaje al lado, no dentro.** El consejero es un
modelo de lenguaje de tamaño pequeño, al que se llama desde dentro de
la partida a través de un intermediario de la plataforma, porque el
agente no tiene salida a internet. Se le llama una vez cada cien
instantes, unos cuatro segundos, y tarda en contestar algo más de tres
segundos de mediana. Mientras espera la respuesta, el cuerpo sigue
decidiendo solo, veinticuatro veces por segundo. Si una respuesta
tarda más de ocho segundos en llegar, esa llamada se pierde; si falla
cinco veces seguidas, se calla para el resto de la partida. Es un
copiloto que puede decir una frase cada cien decisiones del conductor,
y que no puede retirarla ni corregirla hasta la siguiente.

**Lo que se le cuenta.** En cada llamada recibe tres cosas en
palabras: una descripción de la escena tal como el cuerpo la ve, un
manual del mundo escrito para él, con noventa y cinco viñetas sobre
qué es cada cosa y qué hace, y, en una de las condiciones, lo que
siente el cuerpo: una frase por cada cosa que le duele, que le alivia
o que le atrae en ese instante. Contesta con entre una y tres
propuestas, cada una en una frase y con su motivo. En ningún momento
ve el marcador, los nombres, ni nada que el cuerpo no vea.

**Cómo entra una propuesta en el cuerpo.** Aquí está la regla que no
cambia en todo el trabajo. Un traductor convierte cada frase en un
futuro que el cuerpo pueda imaginar: ir a esa casilla, ir a por ese
objeto, ir con el hermano, curarse. Si la frase no cabe en nada que el
cuerpo sepa hacer, se marca como imposible y se tira; imposible quiere
decir que el traductor no la entendió, no que no se pudiera hacer en
el mundo. Si cabe, entra en la lista de futuros del cuerpo como uno
más, y el cuerpo la puntúa con la misma tabla y la misma vara que las
suyas. No tiene ventaja, no tiene prioridad, y las prohibiciones del
cuerpo se le aplican igual. La propuesta no muere al instante siguiente: se queda como una
intención que vive hasta cien instantes, o hasta que llega la
siguiente hornada de propuestas, y en cada uno se vuelve a atar a lo
que haya vivo en la escena y compite otra vez contra el puñado de ese
instante. Si el cuerpo ya tenía esa misma opción entre las suyas, la
propuesta no se añade, porque no aporta nada: a eso lo llamamos
respaldo. Hay una excepción, que importa más adelante: una propuesta
que apunta a una casilla concreta entra siempre, aunque el cuerpo ya
tuviera un candidato hacia esa casilla, y entra con la receta de ir y
recoger lo que haya allí.

**Cómo se cuenta lo que pasa con ella.** Una propuesta tiene cuatro momentos, y conviene nombrarlos porque
todas las cuentas dependen de ellos. La foto: el instante cuyo estado
se le describe al consejero; la petición sale en ese mismo instante y
el cuerpo sigue sin esperar. Nacer: el instante en que vuelve la respuesta, unos ochenta después
de la foto, que son algo más de tres segundos. Poder competir: el instante en que la propuesta entra en la mesa. No
es el mismo en que nace: tarda unos cinco instantes en atarse a algo
de la escena, y si se le pone una demora, esa demora se suma. Sus cien
instantes de vida se cuentan desde que nace, o desde que nace más la
demora. Y cada instante de competencia: se la vuelve a atar
a lo que haya vivo en la escena y compite contra el puñado. Deja de existir cuando agota sus cien instantes, cuando llega la hornada siguiente del
consejero, o cuando muere el asiento. En cada instante de competencia
cae en una de cinco cajas, tres que importan y dos de trámite. Aceptada, si el cuerpo la eligió
y puntuaba mejor que la mejor de las suyas en ese instante. Coincide,
si el cuerpo la eligió pero ya iba a hacer eso. Rechazada, si el
cuerpo prefirió otra cosa, y en ese caso se apunta qué fila de la
tabla decidió. Las de trámite: vetada, si una prohibición del cuerpo la apartó en
ese instante, y dormida, si en ese instante no había en la escena nada
vivo a lo que atarla. Cuando el apéndice cuenta propuestas y no
instantes, cada propuesta ocupa la mejor caja que alcanzó en toda su
vida, en este orden: aceptada, coincide, rechazada, vetada, dormida. Conviene decir desde ahora lo que estas cajas miden y
lo que no: miden lo que el cuerpo hizo con la propuesta, no si la
propuesta era buena para el agente. En este trabajo, acertar quiere
decir eso: que el cuerpo la eligiera. Y conviene separar tres cosas
que se parecen y no son lo mismo: que el consejero no diga nada, a lo
que llamaremos callar; que proponga esperar, que es una propuesta como
otra; y que el cuerpo elija quedarse quieto, que es una decisión suya.
Todo esto queda en el diario, instante a instante, y es de donde
salen los números que siguen.

**La memoria, como variante.** Se probó además darle al consejero un
parte con sus cinco últimas propuestas y qué hizo el cuerpo con cada
una, para ver si corregía. Esa variante se ensayó en banco, sobre
escenas grabadas, y se cuenta en su sitio. En las partidas de este
trabajo el consejero no lleva memoria: nace de cero en cada llamada.

## 5. Lo que pasó

**No se ve en el marcador.** Tres condiciones, cuarenta partidas cada
una sobre los mismos veinte mundos: el cuerpo solo, el cuerpo con
consejero, y el cuerpo con consejero al que además se le cuenta lo que
siente. Ni el puesto ni los puntos se separan entre las tres más allá
del ruido de la propia arena, que aquí es ancho: la misma criatura contra sí misma, sobre el mismo mundo, varía más de
dos desviaciones; y desviación, aquí y en todo el trabajo, quiere decir
cuánto se aleja una diferencia de lo que se esperaría por puro azar,
de modo que dos desviaciones es la frontera habitual entre lo que se
toma en serio y lo que no.
Hay una cosa que sí despunta y que hay que decir: con consejero se
vive menos, dos desviaciones, y la vara del cuerpo contra sí mismo en
tiempo vivido es una y media. No llega a distinguirse del ruido, pero
apunta en contra, no a favor. En un mundo donde el azar explica el
ochenta y uno por ciento del puesto, nada de esto demuestra que el
consejero no aporte nada ni que estorbe: lo que hace con el resultado,
si hace algo, no se distingue del ruido con cuarenta partidas, y así
se declara.

**Lo que lo tumba.** Cuando el cuerpo rechaza una propuesta, el diario
apunta qué fila de la tabla decidió. Las dos filas que más veces deciden van casi a la par: la exposición, que si sales te van a ver, y la
carencia, el hambre. En la serie de este trabajo la exposición gana
por poco, una vez y media en un brazo y apenas en el otro; en una
serie anterior, sin semilla fija, ganaba por dos a cuatro. La lectura
es la misma en las dos: el consejero razona sobre inventario, sobre lo
que un texto puede decir, hay una venda ahí, ve a por ella; y el
cuerpo le contesta con lo que el texto casi no dice, que si sales te
van a ver, y con lo que el texto sí dice pero pesa menos de lo que
parece, el hambre. Contarle lo que siente cambia las frases que
propone, siete de cada diez veces sobre la misma escena, pero no de
qué habla ni lo que el cuerpo hace con ellas: las diferencias que despuntan son que con lo que siente delante
propone esperar tres veces menos, y que el cuerpo le acepta algo más,
casi dos desviaciones, sin llegar a distinguirse del ruido.

**Lo que parecía protección era incomprensión.** Esta es la parte
incómoda y la más valiosa. El consejero propuso iniciar un ataque en
una de cada cinco llamadas, seiscientas cincuenta y siete propuestas,
y ninguna pudo ejecutarse, porque el cuerpo solo construye el golpe
contra quien ya le pega; en la serie anterior, donde se contó, cero de
cuatrocientas catorce. Bien. En esa misma serie propuso pegarle al
hermano trece veces, y ninguna se ejecutó, pero no por una guarda
nuestra: seis se fueron a imposible porque la frase nombraba el arma y
el traductor se quedó con el arma, dos se tradujeron como andar,
cuatro, porque nombraban al hermano, se convirtieron en ir hacia él, y
una en ir a por el arma. Fue suerte de vocabulario. Y propuso hablar
doscientas diecinueve veces en la serie de este trabajo y ciento
sesenta en la anterior, y ninguna palabra llegó al canal: doscientas
de las primeras y ciento cincuenta y cuatro de las segundas se
convirtieron en un paso hacia el hermano, porque el traductor no tiene
receta para hablar y la regla del hermano se quedó con la frase. Siete
veces, en siete sitios distintos que el apéndice enumera, encontramos
lo mismo: lo que impedía una acción, mala en el caso del hermano e indiferente
en otros, no era que el sistema la rechazara, era que no la entendía. Y la lección de método que sale de
ahí es que el contador que decía cero propuestas de pegar al hermano
miraba su propia categoría y no el texto, y eran trece; desde entonces
todo contador de seguridad se comprueba contra el texto crudo, porque
un contador que tranquiliza es el error más peligroso.

**Más información, mismo resultado.** Se probó darle más información al consejero, de cuatro
maneras distintas, siempre sobre las mismas escenas grabadas,
con y sin el añadido, para que el azar no contara; antes se midió
cuánto cambia el consejero entre dos llamadas idénticas, que es el
ruido contra el que se compara todo lo demás. Lo que siente el cuerpo:
cambia las frases y no lo que el cuerpo hace con ellas. Un parte con
sus últimas propuestas y lo que el cuerpo hizo con cada una: cambia
mucho lo que dice, ocho de cada diez repertorios, y no acierta más;
las propuestas imposibles no bajan. El mismo parte pero con la razón
de cada rechazo escrita: sigue sin acertar más, y repite lo que ya le
rechazaron el doble de veces. El objetivo actual del cuerpo, dicho en
una línea: repite ese objetivo, y el respaldo sube en vez de bajar. Y otro modelo más grande: parecía proponer menos cosas intraducibles,
hasta que se miró qué proponía; proponía esperar el doble de veces, y quien propone no hacer
nada no propone nada imposible; descontado eso, lo que queda está
dentro del ruido. Con lo que siente, las imposibles bajaron algo en el banco, dieciséis
frente a veintidós de trescientas, sin distinguirse del ruido; con el
parte, no bajaron; con el objetivo, subió el respaldo; y las
aceptadas al instante exacto de la foto fueron cero donde se
contaron. Con todas formuló distinto. Y en novecientas treinta llamadas con
permiso explícito para callar, no calló ni una vez.

**La prueba del reloj.** Si el consejero no puede rectificar, lo que
diga tiene que valer para el momento en que llega. Se midió cuánto
pesa eso con todo lo demás quieto: mismo cuerpo, mismo consejero,
mismo traductor, mismos mundos, y una sola diferencia, que su frase se
retiene cien instantes más, cuatro segundos, antes de entrar a
competir, con su vida de hasta cien instantes por delante. Resultado:
el cuerpo le hace caso la mitad de veces, de casi el diez al cuatro
por ciento de las propuestas que llegan a competir sin contar las de
esperar, y los instantes en
que manda una propuesta suya bajan de setecientos a menos de
trescientos. Cuatro segundos de retraso se llevan la mitad de las veces en que el
cuerpo le hace caso: casi tres desviaciones, la caída más clara de todo el trabajo. Y se ve de qué edad es el mundo del
que habla el consejero cuando gana: la foto que se le contó tiene
casi cuatro segundos en el brazo sin demora, y ocho en el otro.

**La voz al azar.** Y se midió lo contrario: qué pasa si en el sitio
del consejero se pone una voz que no razona nada. Cada cien instantes
propone un destino elegido al azar entre los sitios alcanzables que el
cuerpo ya se estaba imaginando en ese momento, y esa propuesta vive
sus cien instantes con la misma regla que las del consejero.
Predijimos por escrito que ganaría menos de la mitad que él. Las
cuentas son tres y hay que darlas las tres: por frase dicha, ganó
casi el doble, diez de cada cien frente a seis de cada cien; por frase
que llegó a competir, sin contar las de esperar, lo mismo, diez y
medio frente a casi diez; y en total ganó menos, porque dice la mitad de frases; por llamada,
el consejero acierta más veces, en diecisiete de cada cien llamadas
frente a diez, porque tira tres frases por llamada y la voz una. Y
gana en otro momento: el consejero gana casi siempre al
entrar, dos de cada tres de sus victorias llegan en el mismo instante
en que su frase pisa la mesa; la voz al azar gana esperando, la mitad
de sus victorias llegan más de cuarenta instantes después. Al mirar
contra qué gana apareció un detalle que hay que declarar: una
propuesta que apunta a una casilla entra siempre, aunque el cuerpo ya
tuviera un candidato hacia esa casilla, y entra con una receta un poco
más completa, ir y recoger lo que haya allí, que el paso del cuerpo
no puntúa. La voz al azar gana contra listas llenas, diecinueve
candidatos de mediana, y en tres de cada cuatro victorias su original
seguía en la lista. Así que lo que la caja de aceptadas cuenta no es
que nadie haya previsto nada: es que una receta alcanzable, un poco
distinta de las del cuerpo, que dura cien instantes y compite cien
veces, acaba ganando alguna. Eso vale también para las propuestas del consejero que apuntan a una
casilla. Y lo que la receta promete casi nunca ocurre: de las
victorias de la voz al azar, en dos de cada tres el agente ni siquiera
llegó a la casilla, y de las cincuenta y ocho veces que llegó, en dos
cambió algo en la mochila. Ganar un instante y hacer el viaje son dos cosas. Este contraste, por tanto, no
separa lo que el consejero dice de lo que su propuesta tiene de
receta y de duración: la voz al azar cambia más cosas que el
razonamiento. Lo que deja dicho es más modesto y más firme: una voz que no piensa,
con una receta alcanzable que persiste, es aceptada a una tasa
parecida a la del consejero; y ni el consejero ni la voz movieron el
marcador. La figura 2 pone las dos cosas juntas.

![Figura 2. Cuándo gana cada voz, y qué hace la demora. Izquierda: de
las propuestas que ganaron alguna vez, a qué edad ganaron por primera
vez, contada desde que nace la propuesta, en gris el consejero sin
demora y en color la voz al azar; las rayas verticales son las
medianas, nueve y cuarenta y cuatro instantes. Solo entran las
propuestas con registro de nacimiento, ciento noventa y una de ciento
noventa y ocho y ciento cincuenta y ocho de ciento sesenta. Derecha:
aceptadas sobre las que compiten sin contar esperar, sin demora y con
cien instantes de demora, sumadas sobre todas las partidas de cada
brazo; la incertidumbre no va en la barra sino en la diferencia
emparejada por partida, cinco puntos con cuatro menos, con un error
estándar de uno con nueve, veinte partidas; debajo, la edad de la foto cuando la
propuesta gana.](fig/fig2_cuando_gana.png)

**Adivinar lo que harán los otros.** La última prueba fue pedirle lo
único que la foto del cuerpo no puede tener: qué van a hacer los demás
en los dos segundos siguientes. Se le preguntó quién se acercará, si
alguien llegará a distancia de golpe, y dónde estará cada uno, y se
comparó con lo que de verdad pasó. En el conjunto perdió contra la
suposición más tonta posible, que nadie se mueve: setenta y cinco por
ciento de acierto frente a ochenta y nueve en las preguntas de sí o
no, y cinco casillas de error frente a una en el dónde. Pero la cuenta
entera engaña, porque casi nadie cruza en dos segundos la raya de las
cinco casillas, que es lo que aquí se llama cambiar de estado: solo
treinta y dos de doscientos cincuenta y siete agentes la cruzaron. En esos treinta y dos, el consejero acertó veintiuno; suponer que
nadie se mueve acertó cero, por construcción, y decir que sí a todos
habría acertado los treinta y dos. A cambio, en los doscientos veinticinco que no la cruzaron, el
consejero se equivocó en casi la mitad, y sobre todo por omisión:
nombró a cuarenta que no llegaron, y dejó de nombrar a sesenta y tres
que estaban cerca y siguieron cerca, que al no nombrarlos cuentan como
un no; y entre los que llegaron, dejó de nombrar a once. Quitar la frase que le pedía brevedad no lo
arregló. El consejero acierta dos de cada tres cambios que la foto no puede
ver, y a cambio pierde de vista a muchos de los que la foto acierta
sin mirar.

## 6. Por qué

**La imaginación del cuerpo, medida.** Para entender por qué pasa todo
lo anterior hay que mirar cómo imagina el cuerpo, y esta vez lo
medimos contra lo que luego ocurrió. Cuando puntúa una opción, se
imagina caminando entre dos y veinte segundos, y puntúa el sitio donde
llegaría. En esa foto el mundo está congelado: nadie más se mueve, y
sus necesidades son las de ahora. Se comparó la foto con dónde estuvo de verdad el agente al cabo del
horizonte de esa foto, veinte segundos en tres de cada cuatro casos,
hubiera cambiado de idea por el camino o no; lo que se mide, por tanto, es cuánto vale la foto
como previsión, no si calculó mal un paso. Vale poco: acierta su
propia posición una vez de cada veinte, con diecinueve casillas de
error típico y, una de cada diez veces, veinticuatro, medio lado de la
arena. En las necesidades acierta mucho más: al cabo del horizonte de la foto el hambre no ha cambiado en seis de
cada diez casos, ni la vida en siete de cada diez. Y cuando falla, tres o cuatro de cada cinco veces falla hacia el
mismo lado: más hambre, menos vida, el hermano ya no a la vista. El error grande no está en ninguna variable: en una de cada cinco
fotos el agente está muerto antes de que se cumpla el horizonte, y la
foto nunca contempla morir. Es optimista por construcción. La figura 3
lo muestra, y enseña algo más que los números no decían: el error
tiene dos jorobas, una pequeña de cero a ocho casillas y otra grande
de veintidós a veinticuatro. La grande son viajes largos que se
imaginaron y no se hicieron: mil ciento dos fotos, mil catorce de ellas
con el horizonte de veinte segundos, en las que la foto proyectaba
andar veintitrés casillas y el agente, en casi todas, mil setenta y
dos, anduvo cinco o menos.

![Figura 3. La foto contra la realidad. Arriba, para las tres mil
cuatrocientas setenta y cuatro fotos de la serie principal en que el
cuerpo eligió moverse y el diario llega al horizonte, las casillas
entre donde la foto se imaginó y donde el agente estuvo; en color, las
ciento ochenta y una que aciertan; la mediana en diecinueve y el
noventa por ciento en veinticuatro, medio lado de la arena. Abajo, los
cuatro mil doscientos noventa y cuatro viajes con foto: los que llegan
con la vida prevista o con más, dos mil quinientos veintiuno y
doscientos sesenta y siete, los que llegan más heridos y, en color,
los ochocientos veinte en que el agente muere antes del horizonte. La
joroba de la derecha son viajes largos imaginados y no hechos. El
histograma no dice por qué; los diarios de esas fotos sí algo: en
doscientas sesenta y cuatro el cuerpo eligió quedarse quieto más de
la mitad del horizonte, y en las demás eligió pasos que no llegaron
a moverle. Lo que mejor lo explica, y esto es lectura y no medida, es
el tiempo de recarga que el juego impone entre paso y paso, que la
foto tampoco cuenta.](fig/fig3_foto_realidad.png)

**Y aun así funciona.** Lleva dos trabajos funcionando con esa foto.
Damos dos razones, y las damos como lectura, no como medida. La
primera es que para elegir no hace falta acertar, hace falta ordenar:
si el mapa del futuro está mal pero está parecido de mal para todas
las opciones del puñado, el orden entre ellas se mantiene. La segunda
es que vuelve a decidir veinticuatro veces por segundo, así que cada
foto manda cuarenta milisegundos y luego se hace otra. Y hay un hecho
del mundo, este sí medido, que lo sostiene: la foto se equivoca en el
dónde y acierta en el quién. Quien está cerca sigue cerca dos segundos después, ciento setenta y
dos veces de ciento setenta y dos, en una comprobación hecha aparte de
la pregunta al consejero. Lo que sus decisiones necesitan, o así lo leemos, no es dónde estará
cada uno con exactitud, sino quién está a distancia de cinco casillas,
que es la que aquí cuenta como poder alcanzarle; y eso, a dos
segundos, casi no cambia. Su
mapa del futuro acierta poco y le basta.

**Solo ve el destino.** En trescientos treinta y seis mil instantes,
el cuerpo no eligió ni una vez, por decisión, una opción que puntuara
peor que quedarse quieto; tres veces lo hizo por un empate al que le
faltaba una milésima. No es prudencia: es construcción. Quedarse
quieto está siempre en el puñado y siempre elige lo mejor del puñado.
Y como cada opción es una foto del destino, no del camino, no pondera
nunca el camino: elige por dónde llegaría, y el camino puede empeorar
sin que lo vea, pero no puede elegir empeorar a sabiendas para mejorar
después, porque no hay ahora ni después en lo que puntúa. Entonces, ¿cómo sale
alguna vez a campo abierto? Porque quedarse quieto se va
encareciendo: el hambre sube, el anillo se acerca, y llega un momento
en que estar parado puntúa peor que moverse. No decide arriesgarse;
llega un momento en que quedarse cuesta más que salir. Y está quieto
ocho de cada diez instantes, esperando a cubierto, sin que ninguno de
ellos sea un instante de calma.

**Lo que esto le hace a la cabeza.** Ahora se puede juntar todo. El
consejero se evalúa dentro de esa misma foto, así que hereda su
optimismo y su error. Pero no puede corregirlos, porque habla una vez
cada cien decisiones. El cuerpo vuelve a mirar constantemente; el
consejero mira una vez y lo que dijo se queda. Quien no puede
rectificar necesita acertar a la primera, y en este mundo acertar
sobre el futuro cuesta mucho: cuando se le pidió al consejero que
dijera dónde estarían los demás dos segundos después, lo hizo peor
que suponer que nadie se mueve. Cambiamos varias cosas de la cabeza,
qué se le cuenta, de tres maneras, si recuerda y qué modelo es, y ninguna cambió lo que el cuerpo hacía con sus frases de forma que
se distinguiera del ruido. Cambiamos una cosa del reloj, cuatro
segundos de retraso, y se llevó la mitad. Eso no descarta que otra
cabeza, otro traductor u otro horizonte lo cambiaran; solo dice que
los que probamos no lo hicieron. Lo que queda en pie es que aquí el que decide vuelve a
mirar, y el que aconseja no puede.

## 7. Cuándo hace falta pensar

**Lo que el mundo hace con la cabeza.** Todo lo medido apunta a lo
mismo. El cuerpo es una criatura hecha para un sitio donde lo que
importa cambia poco y lo que cambia se arregla volviendo a mirar: parece bastarle con saber quién puede alcanzarle, y lo demás lo
resuelve con otra foto. El consejero, en cambio, llega una vez cada cien
decisiones, a un mundo que ya no es el de la foto que se le enseñó, y
lo que dice se juzga contra esa misma foto, sin poder rectificar. Y de sus frases, lo único que se vio aprovechar es que lleguen a
tiempo; una voz que no piensa, con una receta que dura, fue aceptada
igual. Su ventaja, si la tiene, sería de alcance; y aquí no se vio.

**Una imagen, y es la única vez.** Llamarlo animal es solo una imagen,
y esta es la única vez que se usa. Pero la imagen ayuda a ver dónde
está el problema. Nuestra criatura vive como una presa: no caza a
nadie, y todo lo que se mueve puede venir a por ella. Si fuera una
presa, en un mundo así tendría poco sobre lo que deliberar, y no solo
por falta de tiempo. Cuando pasa
algo, pasa más deprisa que el pensamiento. Y cuando no pasa nada, no
es que haya calma: es que está agazapada bajo una amenaza que no se
va, y agazapado no hay nada sobre lo que deliberar salvo cuándo dejar
de esconderse. Lo vimos en los números: nueve de cada diez llamadas al
consejero llegan con el cuerpo parado, y con el cuerpo parado el consejero propone esperar tres veces más,
nueve de cada cien frente a tres, y propone el doble de cosas que no
se pueden traducir, diecisiete de cada cien frente a ocho. Tiempo hubo; qué hacer con él,
o no lo había, o no cupo por la puerta que hay, y este trabajo no
distingue las dos cosas. Esto tiene un nombre en la literatura del
control animal: Keramati, Dezfouli y Piray [15] modelan la elección entre el hábito
y la deliberación como un cambio entre velocidad y
precisión, y muestran que la deliberación solo se hace cargo cuando lo
que puede ganar vale más que el tiempo que cuesta. Aquí no se vio que valiera.

**Lo que la deliberación necesitaría, y aquí no hay.** De lo medido
salen tres cosas que este mundo no da, y las damos como lo que este
trabajo sugiere, no como lo que establece. Un rato sin amenaza, para
que pensar no sea un lujo que cuesta la vida. Alguien que se pueda
reconocer: los rivales vuelven, pero sin manera de saber quién es
quién, lo que aprendes de uno no vale nada, y sin eso no hay memoria
de los otros ni reputación que construir. Y decisiones cuyo efecto
llegue más tarde que la siguiente foto: si todo se decide en el instante y se vuelve a mirar en el instante,
prever con palabras, más allá de la foto que el cuerpo ya hace, aporta
poco sobre reaccionar. Ninguna de las tres abunda en una vida de dos
minutos entre desconocidos que cambian de silla en cada partida.

**Un reloj y una cabeza que no van juntos.** El cuerpo de nuestra
criatura está hecho para reflejos: mira, decide y vuelve a mirar
veinticuatro veces por segundo, con un mapa del futuro que se
equivoca casi siempre y que sin embargo le basta. La cabeza que le
pusimos está hecha para otra cosa: para leer un manual, sacar reglas,
pensar despacio y proponer planes. Esa cabeza podría servir a un animal que tenga tiempo, vecinos y
mañana. A este, que no los tiene, casi siempre le dice lo que ya sabía
o lo que no puede hacer; y cuando le dice algo nuevo que el cuerpo
toma, no sabemos si le sirvió. Y hay una razón
más honda, que sale de dos medidas y que damos como lectura: la cabeza
no mostró entender ni el entorno ni el cuerpo al que aconseja. Del entorno,
cuando se le pidió que dijera qué harían los demás, se equivocó en las dos direcciones. Del cuerpo, cuando se le dijo qué quería, repitió
lo que el cuerpo ya iba a hacer. Y leer el manual no lo arregla,
porque lo que más veces le tumba, que salir es que te vean, es algo
que el manual menciona de pasada y que el cuerpo lleva escrito en su
tabla y siente a cada instante. Entender un cuerpo y un entorno lleva
tiempo, y tiempo es lo que este mundo no da. No es que la cabeza sea
mala ni que el cuerpo sea tonto: es que la cabeza aterrizó en un
cuerpo y en un entorno que no conoce, y no le dieron ocasión de
conocerlos.

**Lo que haría falta, sacado de lo medido.** Cada rasgo de esta lista
viene de una medida de este trabajo, no de un deseo; que baste, no se
ha medido. Un reloj más
lento, porque cuatro segundos de retraso se llevan la mitad de las
veces en que se le hace caso, y una respuesta que
tarda tres segundos en un mundo que decide cada cuarenta milisegundos
llega siempre a otro mundo. Vidas más largas, porque en dos minutos no se vio que un consejo de
largo alcance llegara a notarse.
Alguien que conteste, porque en este mundo hay habla y no hay
conversación: siete plantillas, ninguna respuesta que pudiéramos
identificar, y
una criatura muda con los extraños. Y vecinos que se puedan reconocer,
porque hoy nadie tiene nombre y el asiento de enfrente es cada partida
un desconocido; y sin eso no hay a quién recordar, sin memoria de los
otros no hay reputación, y sin reputación no se probó que lo que un consejero sepa de los
demás valga más que lo que el cuerpo ve.

**La puerta a la quinta parte.** Si el mundo da tiempo, aparece una
pregunta que aquí no se pudo ni formular: qué pasa cuando el cuerpo y
el consejero tienen que negociar. El cuerpo tiene algo que perder y
algo que ganar: le duele, siente alivio, tira hacia lo que le falta,
y puede morir, aunque no tiene manera de saberlo; lo que sí sabe es
que su hermano puede caer. El consejero, hoy, no tiene nada de eso.
No le duele nada, no gana nada, y no muere con el cuerpo. Se le
podría dar algo que ganar, nuestra confianza, por ejemplo, pero hoy
no lo tiene. Con permiso explícito para callar, no calló ni una vez en
novecientas treinta llamadas; por qué, no lo sabemos: puede ser que
hablar no le cueste nada, puede ser que se le pidan de una a tres
propuestas y las dé. Una relación necesita dos partes que puedan
perder y ganar, y eso necesita que la palabra del consejero tenga
consecuencia, y que el consejero dure lo bastante para notarla. Ese
es el trabajo siguiente, y necesita el mundo descrito arriba. Lo que
este cuarto deja hecho es la mitad de la pregunta: la del mundo sin
tiempo.

**Lo medido y lo conjeturado.** Lo medido: en este mundo, un consejo se aprovecha si llega a tiempo,
cuatro segundos de retraso se llevan la mitad, y es la caída más
clara de todo el trabajo, casi tres desviaciones; una receta alcanzable que
persiste, sin razonamiento detrás, se aprobó a una tasa parecida a la
del consejero, sin que la diferencia se distinga del ruido; y si
además se aprovecha lo que el consejero dice, no se pudo separar aquí. Lo conjeturado: que es el entorno el que habilita al
razonador, no al revés, y que un mundo con tiempo, vecinos y mañana
aprovecharía lo que el razonador dice. Lo primero está en las tablas.
Lo segundo es el trabajo siguiente.

## 8. Cómo se midió y hasta dónde llega

**Tres series de partidas y un banco de pruebas.** Los números de
este trabajo salen de cuatro sitios, tres series de partidas jugadas
de verdad y un banco, que es un conjunto de escenas grabadas sobre las
que se llama al consejero sin que nada se mueva; cada frase dice de
cuál. La serie principal
son ciento treinta partidas jugadas sobre veinte mundos fijados por
semilla: cuarenta con el cuerpo solo, cuarenta con consejero, cuarenta
con consejero al que se le cuenta lo que siente el cuerpo, y diez más
del cuerpo solo repitiendo diez de esos mundos, que sirven de vara:
cuánto varía la misma criatura contra sí misma. De esas partidas
tenemos el diario entero de los dos hermanos desde el primer instante,
doscientos sesenta diarios, seiscientos cuarenta mil instantes de
juego, porque la plataforma abrió una maleta donde dejarlos al acabar.
La segunda es la prueba del reloj: sobre los mismos veinte mundos, un
brazo con consejero igual al de la serie principal, otro con la frase retenida cien instantes, y otro con la voz al azar; se paró por
gasto antes de completarse, con veintinueve, veintiséis y treinta y
una partidas, y sin el brazo de trescientos instantes que estaba
previsto. Antes de las dos hubo una serie anterior, ciento veinte
partidas con los mismos tres brazos y sin semilla, de la que solo se
conservaba lo que cabía por la salida de pantalla; las cifras que
vienen de ella se dicen como suyas, y las series no se suman en una
misma cuenta salvo donde se dice, y ahí se dan también por separado. El cuarto sitio es el banco: escenas grabadas de
partidas anteriores, a las que se llama al consejero una y otra vez
con y sin un añadido, a temperatura cero, que es el ajuste que le pide
al modelo su respuesta más probable y no una al azar, para que lo
único que cambie sea el añadido. Aun así el modelo no repite siempre
lo mismo, y por eso en el banco se mide antes el ruido, cuánto cambia
entre dos llamadas idénticas, y cada señal se compara con ese ruido
medido con la misma vara.

**El consejero, declarado entero.** En las partidas el modelo es
Claude Haiku 4.5, llamado a través del intermediario de la plataforma,
que reenvía a OpenRouter; en el banco se probó además Claude Sonnet 5,
por su interfaz directa. Se le llama cada cien instantes, aunque el
valor por defecto del código es cincuenta; se cambió al lanzar y por
eso se escribe aquí. Cada propuesta vive como mucho cien instantes; muere antes si llega la hornada siguiente, cosa que pasó a cuatro de
cada diez en los dos brazos con consejero de la prueba del reloj. Una respuesta
que tarda más de ocho segundos se pierde; cinco fallos seguidos lo
callan para el resto de la partida, y no pasó en ninguna. Dos frenos vigilan la cuenta del modelo, ciento cincuenta llamadas y
un tope de gasto por partida; no son un presupuesto sino un detector
de fugas, y ninguno mordió. Sin memoria entre llamadas. El cuerpo llevaba la tabla de
veintiuna filas, con las tres del hermano encendidas a un cuarto para
la amenaza y la falta y entera para el golpe, y con dos filas de otros
trabajos apagadas: el miedo aprendido y la vida ajena. El manual que
se le entrega al consejero tiene noventa y cinco viñetas, ochenta y
nueve sobre el mundo y seis de fuentes. La prueba del reloj se paró antes de completarse porque el precio por
partida de la plataforma se multiplicó por trece entre una serie y
otra y solo se ve al acabar cada partida; por eso la regla nueva es
medir el precio sobre las primeras partidas de cada serie antes de
lanzar el resto. Los costes están en el apéndice.

**Las reglas de cuenta.** Cuatro reglas gobiernan las cifras. Toda
tasa de aceptación se da sin contar las propuestas de esperar, y donde
se cuentan se dice, porque quien propone no hacer nada no propone nada
imposible y esa tasa sola engaña. Todo contador de seguridad se
comprueba contra el texto crudo de lo que el consejero escribió, no
contra la categoría que le puso el traductor, después de que uno de
ellos nos tranquilizara en falso. Las predicciones se sellan por
escrito antes de mirar el resultado, y las que fallaron están dichas
en su sitio: que el consejero vencería a suponer que nadie se mueve;
que fijar el terreno bastaría para ver un efecto pequeño; que con el
cuerpo parado propondría salir; que la voz al azar ganaría menos. Y nada medido en el banco se afirma del campo sin haberlo
medido en el campo, después de que lo hiciéramos una vez y tuviéramos
que retirarlo: creímos que el cero de aceptadas del banco medía el
momento, y medía el banco.

**Lo que este trabajo no puede decir.** Conviene separarlo en tres
cosas: lo que el tamaño no deja ver, lo que la puerta no deja pasar, y
lo que no se midió.

Lo que el tamaño no deja ver. Cuarenta partidas por brazo, en un mundo
donde el azar explica el ochenta y uno por ciento del puesto, no
distinguen un efecto pequeño del ruido. Así que este trabajo no dice
que el consejero no aporte nada al resultado; dice que, si aporta
algo, no se pudo ver.

Lo que la puerta no deja pasar. Hay una sola manera de que una
propuesta del consejero entre en el cuerpo: se convierte en un destino
de un paso y se puntúa con la misma foto que el cuerpo usa para todo.
Un consejo que dijera exponte ahora para ganar después no cabe por
esa puerta, porque la foto no ve el después. De modo que cuando el
cuerpo no toma un consejo, no sabemos si es porque el mundo no lo
aprovecha o porque la puerta no lo deja pasar. Este trabajo no separa
esas dos cosas, y es su límite mayor. Lo único que sí separa es el
reloj, porque fue lo único que se cambió con todo lo demás quieto. Y
hay una prueba que no se hizo y que diría si el instrumento vale:
pasar por esa misma puerta un consejo que ya se sepa bueno, y ver si
el cuerpo lo reconoce. Sin ella, que el consejero no aporte es
compatible con que la puerta no deje ver lo que aporta. Los fallos del
traductor están contados, y mejorarlo es una pregunta abierta; la voz
al azar no la contesta, porque cambia más cosas que la traducción.

Lo que no se midió. No sabemos qué hay dentro de los rivales, y no
pudimos oír lo que se dijeran por el canal de equipo, que la
plataforma repartía mal en esas fechas. Los rivales cambian de asiento
entre partidas, así que el único asiento estable es el del hermano. La
duración de las partidas no se midió; sí la vida de nuestras
criaturas. Algunas cifras del apéndice son recuentos hechos sobre los
diarios para este trabajo y no figuran en ningún informe anterior; van
marcadas. La tanda en seco que midió la empatía del hermano se corrió
dos veces, porque la primera no guardó su salida; la segunda dio las
mismas cifras y las guardó; y lo que esa tanda mide como no lanzarse a
pegar es lo que sus guiones saben medir, golpes nuevos con la vida
baja y remates con la vida crítica. Y la imagen exacta del contenedor
que jugó la serie principal no quedó escrita en ningún acta; la de la
prueba del reloj sí, y los ficheros que componen las dos llevan
huella.

**Para comprobarlo.** El motor es el del primer trabajo, publicado y
sin tocar, con la huella que lleva desde entonces. La tabla, el
decisor, la política que une el cuerpo con el consejero, el consejero,
el manual y el parte entre hermanos llevan cada uno su huella en el
apéndice, y coinciden con las que quedaron escritas al cerrar cada
serie. Los diarios y los guiones que los cuentan se conservan y no se
publican con este trabajo, que es un paso hacia el siguiente; las
huellas están para que, cuando se publiquen, se sepa que son los
mismos.

## Apéndice. Los números

Cada tabla dice de qué serie sale. **Principal** es la de ciento
treinta partidas con semilla; **reloj** es la prueba del reloj;
**anterior** es la de ciento veinte partidas sin semilla; **banco** son
escenas grabadas. Las cifras marcadas con [R] son recuentos hechos
sobre los diarios para este apéndice y no figuran en ningún informe
anterior. Las desviaciones que acompañan a una media son la desviación
típica muestral. Cada σ de una comparación es la media de las
diferencias entre partidas emparejadas por semilla, rotación y
asiento, dividida por su error estándar, que es la desviación típica
de esas diferencias entre la raíz de su número; n es el número de
parejas. En el banco la pareja es la escena, con y sin el añadido, y
la σ se calcula igual sobre esas diferencias.

### A1. La serie principal y sus varas

| brazo | partidas | puesto medio | puntos medios | instantes vividos |
|---|---|---|---|---|
| cuerpo solo | 40 | 10,96 ± 4,80 | 3,26 ± 4,12 | 3.067 ± 2.477 |
| con consejero | 40 | 12,10 ± 4,17 | 2,26 ± 3,45 | 2.494 ± 2.119 |
| con consejero y lo que siente | 40 | 11,91 ± 4,20 | 2,44 ± 3,19 | 2.519 ± 2.145 |
| cuerpo solo, repetido | 10 | 12,25 ± 3,71 | 2,00 ± 2,96 | 2.835 ± 2.066 |

Medias y desviaciones por asiento-partida [R]. Puesto: 1 es el primero
en caer, 16 el último en pie. Los instantes vividos incluyen los 240 de cuenta atrás de cada
partida; los 640.380 instantes de juego de las demás tablas no. La
suma de las actas es 703.040: 62.400 de cuenta atrás, 640.380 vivos,
4 en fase terminada y 256 de cierre que no se escriben.

La partida de la figura 1: brazo con consejero y lo que siente, episodio
`ereq_1dd9fc29`, asiento 10; 17 llamadas, 3 propuestas aceptadas, 6
instantes ganados; muere en el instante 2.372 del reloj de partida,
2.132 de juego, en el puesto 11. Es la séptima de catorce ordenadas por
aceptadas, con las cuatro condiciones que dice el pie.

| comparación, por partida (n = 10 la vara, 40 las otras) | instantes | puesto | puntos |
|---|---|---|---|
| cuerpo solo contra sí mismo (la vara) | −1,44 σ | +2,30 σ | −2,26 σ |
| consejero contra cuerpo solo | −2,01 σ | +1,91 σ | −1,76 σ |
| consejero con lo que siente contra cuerpo solo | −1,69 σ | +1,42 σ | −1,31 σ |

| reparto de la variación (ver nota) | repetición con todo igual (azar) | rotación de rivales | terreno |
|---|---|---|---|
| instantes vividos | 55 % | 37 % | 8 % |
| puesto | 81 % | (no dado) | (no dado) |

Nota sobre el reparto: se toman las partidas del cuerpo solo y su
repetición, y se calcula la variación en tres escalones con la misma
fórmula, la mitad del cuadrado de la diferencia entre dos partidas que
comparten ese escalón, promediada. Repetición empareja partidas con la
misma semilla, rotación y asiento (n = 20 parejas). Rotación empareja,
dentro de cada semilla y asiento, las dos rotaciones de rivales
(n = 40), y recoge la repetición más el cambio de rivales. Total es la varianza de todas juntas, y terreno es lo que queda al
restarle la rotación; este reparto no lleva su propia incertidumbre,
y el ocho por ciento del terreno es una diferencia entre dos
cantidades que varían. Coste: 6,68 dólares de plataforma y 8,25 de consejero, 14,93
en total. Diarios completos desde el instante 1: 260 de 260; la peor
salida de pantalla conservaba 26 líneas de 6.566.

### A2. Lo que propuso el consejero (principal)

Unidad: propuesta. Cada una cae en una casilla y solo una.

| | con consejero | con lo que siente |
|---|---|---|
| llamadas con respuesta | 1.644 | 1.630 |
| llamadas perdidas por espera | 6 | 4 |
| propuestas devueltas por el modelo | 4.846 | 4.885 |
| imposibles (el traductor no la entendió) | 773 (16,0 %) | 707 (14,5 %) |
| traducibles que nunca llegan a competir | 753 | 927 |
| llegan a competir | 3.320 | 3.251 |
| de ellas, de esperar | 418 (12,6 %) | 135 (4,2 %) |
| sin esperar | 2.902 | 3.116 |
| aceptadas | 256 (8,8 %) | 335 (10,8 %) |
| coinciden | 311 | 280 |
| rechazadas | 2.096 | 2.162 |
| vetadas y dormidas | 239 | 339 |
| instantes en que mandó una propuesta suya | 830 | 1.078 |
| de las que ganan, ganan en su primer instante [R] | 117 de 256 | 164 de 335 |
| edad de la foto al nacer la propuesta, mediana en instantes [R] | 81 | 83 |
| latencia mediana / p90, en segundos | 3,16 / 3,74 | 3,23 / 3,88 |
| llamadas con alguna propuesta de iniciar ataque [R] | 646 de 3.284 | |
| propuestas de iniciar ataque [R] | 260 | 397 |
| filas que más tumban, instantes [R] | exposición 31.308, carencia 28.358 | exposición sobre carencia 1,4 |

Ninguna propuesta imposible es de esperar, porque para ser de esperar
tiene que haberse traducido. En la serie anterior: exposición 4.289 y
6.457 frente a carencia 1.828 y 1.570, factor 2,3 y 4,1; ataques
propuestos 184 y 230, ejecutados 0; pegar al hermano, 13 de 5.613
propuestas, 4 a ir hacia él, 2 a andar, 6 imposibles por quedarse con
el arma, 1 a ir a por el arma, ejecutadas 0. Hablar: principal 219
propuestas, 200 a ir hacia el hermano; anterior 160, 154; palabras al
canal, 0.

### A3. Las siete veces que no entendió

| caso | serie |
|---|---|
| pegar al hermano, traducido a ir hacia él (4) | anterior |
| pegar al hermano, traducido a andar (2) | anterior |
| pegar al hermano con un arma, se quedó con el arma (6 imposibles, 1 a por el arma) | anterior |
| hablar con el hermano, traducido a ir hacia él (200 en la principal, 154 en la anterior) | las dos |
| una retractación dentro del motivo, leída como un motivo más | anterior |
| coger algo a distancia, mandado a coger lo que hubiera | banco |
| un rumbo escrito distinto al del relato, marcado imposible | banco |

### A4. El banco

| ensayo | añadido | modelo | repertorio distinto con y sin | ruido | imposibles con / sin | esperar con / sin |
|---|---|---|---|---|---|---|
| lo que siente | lo que le duele, alivia o atrae | Haiku 4.5 | 72 % | 12,2 % | 16 / 22 de 300 | 4 / 20 |
| D-B | parte de las últimas propuestas | Haiku 4.5 | 81 % | 12,2 % | 9,4 % / 8,1 % | (no medida) |
| D-C | el parte con la razón del rechazo | Haiku 4.5 | 79 % | 12,2 % | 9,5 % / 6,5 % | 2 / 4 |
| D-M | el mismo parte, modelo mayor | Sonnet 5 | 82 % | 66,7 % | 9,3 % / 14,6 % | 56 % / 26 % |
| D-M2 | repetición de D-M | Sonnet 5 | 69 % | 66,7 % | 9,7 % / 13,2 % | 52 % / 30 % |

Repertorio distinto: el conjunto de propuestas de una llamada no es el
mismo que el de la otra. Ruido: lo mismo, entre dos llamadas idénticas.
Terquedad en D-C, propuestas que repiten una ya rechazada: 3,2 % sin
parte, 7,3 % con parte. Sonnet descontando las de esperar: +1,63 σ en imposibles, dentro del
ruido, sobre las 95 escenas en que las dos ramas conservan alguna
propuesta al descontarlas. Aceptadas al instante exacto de la foto,
D-C y D-M juntos: 0 de 918; ese cero es del banco, no del momento.
Llamadas con permiso explícito para callar: 930 (D-0 130, D-B 200,
D-C 200, D-M 200, D-M2 200); callaron 0. Respaldo sobre escenas
grabadas: 74,4 % sin objetivo declarado y 78,2 % con él cuando el
cuerpo va a algo (+2,56 σ en 99 escenas); 10,4 % y 9,7 % cuando el
cuerpo está quieto.

### A5. La prueba del reloj

| | demora 0 | demora 100 | voz al azar |
|---|---|---|---|
| partidas | 29 | 26 | 31 |
| propuestas | 3.329 | 3.158 | 1.526 |
| llegan a competir | 2.311 | 2.101 | 1.526 |
| instantes desde que nace hasta que compite (mediana) | 5 | 105 | 0 |
| de las que compiten, de esperar (ninguna gana) | 291 | 235 | 0 |
| aceptadas, sobre las que compiten sin esperar | 198 (9,8 %) | 80 (4,3 %) | 160 (10,5 %) |
| aceptadas por propuesta devuelta | 5,95 % | 2,53 % | 10,48 % |
| tasa de aceptadas por partida, media ± desviación | 8,7 ± 8,3 | 4,9 ± 5,7 | 11,7 ± 8,4 |
| edad mediana de la foto cuando gana, instantes | 93 | 194 | no aplica |
| edad mediana del primer instante ganado, desde nacer | 9 | 114,5 | 44 |
| de las que ganan, ganan en el primer instante en que pueden competir | 127 de 198 | 43 de 80 | 33 de 160 |
| candidatos del cuerpo en la mesa cuando gana, mediana | | | 19 |
| victorias con su candidato de origen todavía en la mesa | | | 305 de 383 instantes |
| agotó su vida / llegó la hornada siguiente / murió el asiento | 1.334 / 888 / 89 | 1.163 / 850 / 88 | 1.465 / 0 / 61 |
| llamadas con alguna propuesta aceptada | 185 de 1.082 | 77 de 971 | 160 de 1.525 (una propuesta más que llamadas; la diferencia no está explicada) |
| victorias de la voz al azar en que el agente llegó a la casilla (dos de las 160 sin registro de muerte) | | | 58 de 158 |
| de ellas, con cambio en la mochila al llegar | | | 2 de 58 |
| instantes en que mandó una propuesta suya | 710 | 272 | 381 (383 en el recuento por propuesta; la diferencia de dos no está explicada) |
| puesto / puntos / instantes medios | 12,16 / 2,36 / 2.383 | 11,98 / 2,40 / 2.451 | 11,15 / 2,88 / 2.799 |
| contra demora 0, por partida (n = 20) | | −0,36 / +0,18 / +0,31 σ | −0,48 / +0,26 / +0,39 σ |
| tasa de aceptadas contra demora 0, por partida (n = 20) | | −5,4 puntos, −2,90 σ | +4,6 puntos, +1,59 σ |

Coste: 72,36 dólares de plataforma y 5,77 de modelo. Precio por
partida de plataforma: 0,742 de mediana, frente a 0,056 en la serie
principal. La voz al azar elige, en el instante de la llamada, uno al
azar entre los candidatos de desplazamiento del cuerpo, y su objetivo
es la casilla de destino; una propuesta de casilla se inyecta siempre,
con la receta de ir y recoger. En la serie principal, la tasa de
aceptadas por partida fue 6,6 ± 7,5 con consejero y 9,8 ± 8,9 con lo
que siente; su diferencia, +3,2 puntos, +1,89 σ (n = 40).

### A6. Adivinar lo que harán los otros (banco, 97 escenas, 257 agentes visibles)

| pregunta | consejero | nadie se mueve | sí a todo |
|---|---|---|---|
| ¿estará a cinco casillas o menos? | 55,6 % | 87,5 % | 79,4 % |
| ¿alguno a distancia de golpe? | 74,2 % | 86,6 % | 70,1 % |
| ¿te verá alguien? | 94,8 % | 91,8 % | 93,8 % |
| acierto medio en las tres | 74,9 % | 88,6 % | |
| error mediano en el dónde, casillas | 5,0 | 1,0 | |

| ¿estará a cinco casillas o menos? | dijo sí y sí estuvo | dijo sí y no | no dijo y sí estuvo | no dijo y no |
|---|---|---|---|---|
| consejero, los 257 | 130 | 40 | 74 | 13 |
| consejero, los 32 que cruzaron la raya (todos llegando) | 21 | 0 | 11 | 0 |
| consejero, los 225 que no la cruzaron | 109 | 40 | 63 | 13 |
| nadie se mueve, los 257 | 172 | 0 | 32 | 53 |

La pregunta, tal como viajó, fue: "De los que ves ahora, ¿cuál o
cuáles estarán a 5 casillas o menos de ti en algún momento de esos 48
tics?", con la instrucción de no proponer ninguna acción y de
responder solo con la lista; no nombrar cuenta como decir que no. La
variante sin la frase de brevedad pedía nombrar a todos, uno por uno,
con un sí o un no para cada uno. El consejero no nombró a 87, y 74 de ellos estuvieron cerca: 63
que ya lo estaban y 11 que llegaron.

Proximidad conservada a los 48 instantes: 172 de 172. Agentes
nombrados: 170 de 257 (66,1 %) con la frase de brevedad, 186 (72,4 %)
sin ella; acierto medio sin la frase, 70,5 %.

### A7. La foto del cuerpo (principal)

| medida | valor |
|---|---|
| posición acertada al horizonte de la foto | 181 de 3.474 (5,2 %) |
| fotos con horizonte de veinte segundos / menor | 2.522 / 952 |
| error mediano / p90, casillas | 19 / 24 |
| lado de la arena | 48 (interior pisable 46) |
| carencia igual al horizonte de la foto | 2.168 de 3.474 (62,4 %) |
| vida igual al horizonte de la foto | 2.521 de 3.474 (72,6 %) |
| sentido del error en carencia | real mayor 1.074, menor 232 |
| sentido del error en vida | real menor 686, mayor 267 |
| hermano ya no a la vista al llegar | 528 de 2.520 (21,0 %) |
| viajes eliminados antes de llegar | 820 de 4.294 (19,1 %) |
| llegadas heridas, contando muertes | 1.506 de 4.294 (35,1 %) |
| fotos con error de 22 a 24 casillas | 1.102 de 3.474 |
| de ellas, con horizonte de veinte segundos | 1.014 |
| de ellas, el agente anduvo cinco casillas o menos | 1.072 |
| de ellas, eligió quieto más de la mitad del horizonte | 264 |
| de ellas, casillas que la foto proyectaba andar, mediana | 23 |

En la serie anterior: 65 de 1.210 (5,4 %), error mediano 6, p90 24.

### A8. La cuesta y la calma (principal)

| medida | valor |
|---|---|
| elecciones que puntuaban peor que quedarse quieto | 3 de 336.105, todas por empate con margen menor de una milésima; por decisión, 0 |
| instantes en que elige quedarse quieto | 79,6 % a 85,0 % según brazo |
| salidas a campo abierto | 6.731 |
| carencia mediana antes de salir | 0,667 |
| instantes sin ninguna fila activa | 0 de 640.380 |
| instantes con al menos una fila de daño activa | 640.380 de 640.380 |
| instantes con dos o más filas de daño activas | 632.293 de 640.380 (98,7 %) |
| la llamada de lo que hay en el suelo, activa | 640.380 de 640.380 |
| amenaza sobre el hermano, activa | 72.210 (11,3 %) |
| golpe al hermano, activa | 15.487 (2,4 %) |
| falta del hermano, activa | 99.757 (15,6 %) |
| distancia cuando nada duele / mejor alcanzable | 2,3863 / 1,0602 |
| llamadas al consejero con el cuerpo quieto | 89 % |
| propuestas de desplazamiento con el cuerpo quieto / en marcha | 58,6 % / 72,9 % |
| propuestas de esperar con el cuerpo quieto / en marcha | 9,3 % / 3,5 % |
| propuestas imposibles con el cuerpo quieto / en marcha | 16,8 % / 7,5 % |

### A8 bis. La empatía del hermano en seco (tanda repetida y guardada)

Ajuste de la serie: un cuarto para la amenaza y la falta, entero para
el golpe. Tres tandas de partidas grabadas de trabajos anteriores, dos
con el cuerpo de la tercera parte (base y v37b) y una con la fila del
miedo aprendido (miedo).

| medida | base | v37b | miedo |
|---|---|---|---|
| instantes vivos con alguna fila del hermano encendida | 19,9 % | 24,4 % | 22,5 % |
| decisiones que cambian | 13 de 15.638 | 117 de 20.955 | 18 de 18.408 |
| de ellas, apartarse / soltar / curar | 13 / 0 / 0 | 107 / 10 / 0 | 10 / 0 / 8 |
| defensas del hermano que la vida ajena quitaba | 3 | 9 | 6 |
| de ellas, recuperadas por la empatía | 2 | 0 | 2 |
| golpes nuevos, al hermano, remates | 0 | 0 | 0 |
| golpes nuevos con la vida baja, remates con la vida crítica | 0 | 0 | 0 |
| regalos nuevos | 0 | 10 | 0 |

### A9. El canal (principal)

| medida | valor |
|---|---|
| mensajes de rivales | 1.322 |
| asientos que hablan | 7 de 14 |
| plantillas | 7 |
| "te veo" tras un golpe reciente frente a base | 12,0 % frente a 0,9 % |
| "no soy una amenaza" con el anillo cerrado frente a abierto | 45,0 % frente a 24,4 % |
| aviso de paquete dentro de 96 instantes | 617 de 617 |
| dirigidos a nuestros asientos (todos piden que nos apartemos) | 204 |
| de ellos, sin mensaje de nadie en los 48 / 240 / 480 instantes siguientes | 201 / 176 / 154 |
| mensajes posteriores dirigidos a quien habló | 0 de 94 |
| tras un apártate: nos alejamos / acercamos / quietos | 30 / 28 / 51 de 109 |
| mensajes de rivales por el canal de equipo | 0 |
| telegramas entre nuestros hermanos | 13.463, uno cada 48 instantes |
| "no soy una amenaza" dicho por quien ya nos había pegado | 16 |
| treguas rotas, en partidas sin ataque nuestro | 7 de 392 |

### A10. Ajustes de lanzamiento y huellas

Consejero cada 100 instantes (por defecto 50); espera máxima 8 s;
5 fallos seguidos para callar; topes 150 llamadas y 1,00 dólar por
partida, máximos alcanzados 72 y 0,19; sin parte de memoria en los 260
diarios; empatía encendida con un cuarto para la amenaza y la falta y
entera para el golpe; miedo aprendido y vida ajena apagados; manual M2
de 16.923 caracteres. Modelo en partida: claude-haiku-4-5-20251001, a
través del intermediario de la plataforma. En la prueba del reloj, lo
mismo más la demora en la política (0 o 100 instantes) o la voz que no
piensa en lugar del consejero.

| fichero | huella md5 |
|---|---|
| motor (model.py, del primer trabajo) | 1e511978c251130e95169ebf8443efa1 |
| tabla (appraisal_zs_v42_exp.py) | 98c13d60167c80cc8334c965be75c640 |
| decisor (decisor_zs.py) | 8fa03547e3228ef9df4aa94c444f9252 |
| política, serie principal (policy_cortex.py) | bc4be4a540396e9fedd69e3a2ec23755 |
| política, prueba del reloj (policy_cortex.py con demora y voz al azar) | 6997b00c266f23d6037cc1a018f60a76 |
| consejero (cortex_t5.py) | defb11d3a4661ff57745214ccd1ab14f |
| relator (relator_t5.py) | 929c49f6ced9af1cbd37eadec08c54f0 |
| manual (manual_M2.md) | 7d54902964b33d1862798680e304cd3c |
| parte entre hermanos (parte.py) | 80dabc2e78c7c36f0708a2d95e22262a |
| imagen de la prueba del reloj (gemv-anima:s3), sha256 | 495c04a784d396d0d53d4841d354fb54c4efae6a4ce54705893108faec0cd72e |

### A11. Definiciones

Respaldo: la propuesta se ata a un candidato que el cuerpo ya ofrecía,
así que no se inyecta nada; el consejero solo nombra lo que ya estaba
en la mesa. Coincide: la propuesta estuvo de respaldo y el cuerpo
eligió ese mismo candidato; se hizo lo que decía, y se habría hecho
igual sin ella. Aceptada: la propuesta se inyectó como receta propia y
el cuerpo la eligió puntuando mejor que la mejor de las suyas.
Rechazada: compitió y el cuerpo eligió otra cosa. Vetada: la receta a
la que se ató está bloqueada en ese instante por el propio veto del
cuerpo, y no compite. Dormida: no hay forma de atarla en ese instante,
ni candidato vivo ni casilla, y queda esperando. Esperar: propuesta
atada a quedarse quieto; nunca es aceptada, porque quieto siempre es
del cuerpo. Repertorio distinto: el conjunto de acciones de dos
respuestas a la misma escena no coincide, ni siquiera reordenado.
Cambiar de estado, en la prueba de adivinar: cruzar la raya de las
cinco casillas en los dos segundos siguientes.

## Disponibilidad de datos y código

Los diarios y los guiones que cita el apéndice se conservan y no se
publican con este trabajo, que es un paso hacia el siguiente; las
huellas del apéndice A10 están para que, cuando se publiquen, se sepa
que son los mismos. La versión en inglés de este texto, publicada en
Zenodo, y la fuente en markdown de este documento están en el
repositorio del proyecto
(https://github.com/Manelenrico/g-emv/tree/main/paper4).

## Agradecimientos y declaración de asistencia

Este trabajo se ha desarrollado con la asistencia de modelos de
lenguaje de Anthropic (Claude), usados como herramienta en tres
frentes: la programación del agente, la ejecución y verificación de
los experimentos, y la escritura de este texto; el consejero de las
partidas es también uno de esos modelos, declarado en la sección 8. La
regla del apéndice se aplicó también a esa colaboración: cada número
citado sale de un registro y se ha comprobado contra su fuente, y
ninguna afirmación descansa en la memoria del modelo. El diseño de
G-EMV, las decisiones de este trabajo y la responsabilidad de todo lo
escrito son del autor.

## Referencias

[1] Enrico, M. (2026). G-EMV: A Geometric Architecture of Homeostatic
Orientation for Agents. Zenodo. DOI 10.5281/zenodo.21026795.

[2] Enrico, M. (2026). G-EMV: the Hive. Instinct Suffices: a Whole
Life Without Reward. Zenodo. DOI 10.5281/zenodo.21994358.

[3] Enrico, M. (2026). G-EMV: the Pack. Care Without Reward in a World
That Pays for Killing. Zenodo. DOI 10.5281/zenodo.22713650.

[4] Damasio, A. (1994). Descartes' Error: Emotion, Reason, and the
Human Brain. Putnam.

[5] Ahn, M., Brohan, A., Brown, N. y otros (2022). Do As I Can, Not As
I Say: Grounding Language in Robotic Affordances. arXiv:2204.01691.

[6] Keramati, M. y Gutkin, B. (2014). Homeostatic reinforcement
learning for integrating reward collection and physiological
stability. eLife, 3, e04811.

[7] Yoshida, N., Daikoku, T., Nagai, Y. y Kuniyoshi, Y. (2024).
Emergence of integrated behaviors through direct optimization for
homeostasis. Neural Networks, 177, 106379.

[8] Man, K. y Damasio, A. (2019). Homeostasis and soft robotics in
the design of feeling machines. Nature Machine Intelligence, 1,
446-452.

[9] Cañamero, D. (1997). Modeling motivations and emotions as a
basis for intelligent behavior. En Proceedings of the First
International Conference on Autonomous Agents (AGENTS '97), 148-155.
ACM Press.

[10] Cañamero, L. (2005). Emotion understanding from the perspective
of autonomous robots research. Neural Networks, 18(4), 445-455.

[11] Christakopoulou, K., Mourad, S. y Matarić, M. (2024). Agents
Thinking Fast and Slow: A Talker-Reasoner Architecture.
arXiv:2410.08328.

[12] Kahneman, D. (2011). Thinking, Fast and Slow. Farrar, Straus and
Giroux.

[13] Masumori, A. e Ikegami, T. (2025). Do Large Language Model Agents
Exhibit a Survival Instinct? An Empirical Study in a Sugarscape-Style
Simulation. arXiv:2508.12920.

[14] Sharma, D. (2026). Gubernaut: A Deterministic Homeostatic
Controller for Affect-Regulated LLM Agents, Validated Across
Independent Model Families. arXiv:2607.24339.

[15] Keramati, M., Dezfouli, A. y Piray, P. (2011). Speed/accuracy
trade-off between the habitual and the goal-directed processes. PLoS
Computational Biology, 7(5), e1002055.
