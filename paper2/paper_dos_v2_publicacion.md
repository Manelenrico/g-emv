# G-EMV: la colmena. El instinto basta: una vida entera sin premio

Manel Enrico
*Investigador independiente, Barcelona*
ORCID: 0009-0008-1732-6310
*Preprint, versión 1 — 2026*

Segunda parte de una historia en tres: el motor [1], la colmena (este trabajo), la manada (la
siguiente).

**El mundo y la pregunta.** Este trabajo es la segunda parte de una historia en tres partes.
La primera, el motor, publicó G-EMV: una geometría de lo que importa, tres dominios de vida, seis fuerzas, una distancia que
descender, definida antes de tocar mundo alguno, sin aprendizaje. Quedó abierta la pregunta que
importa: ¿puede esa geometría, sola, orientar a un agente en un mundo que no diseñó su autor?
Este trabajo la responde construyendo un agente para machina_1, el entorno
competitivo de Cogs vs Clips (Softmax) [2], donde un equipo de
ocho agentes mina recursos, abastece una despensa común, fabrica equipo y alinea antenas,
defendiendo lo alineado de una fuerza rival que el propio juego gobierna: eventos periódicos,
emanados de naves enemigas estáticas, que desconectan las antenas nuestras, devolviéndolas al
gris, y reclaman las grises para el bando rival. El marcador del equipo se acumula por tick, es
la media de antenas que se mantienen alineadas a lo largo de la vida entera: lo que puntúa
es mantener, no solo conquistar. El agente no lleva función de recompensa, no entrena, y no
contiene conductas escritas: toda su vida emana del descenso de la distancia que el modelo
publicado define. Y queda anunciada la tercera parte, la manada: qué cambia cuando estos
agentes, que cooperan sin conocerse, empiecen a reconocerse.

**El animal, dicho una vez.** Si hiciera falta una imagen, sería la de los insectos sociales:
una colmena. Ocho cuerpos con los mismos genes del valor, la misma tabla de constantes: idénticos
objetivos, idénticos pesos, idénticas sensibilidades, que cooperan sin conocerse, sin
nombres, sin caras, sin censo, sostenidos por un tablón común de avisos sin autor. Llamarlo
animal es solo eso, una imagen, y esta es la única vez que este texto la usa. En adelante, el
agente.

**El mapa del trabajo.** La sección 1 resume el modelo publicado: solo las piezas que el resto del
trabajo usa. La 2 presenta la arquitectura, la capa que traduce el mundo a fuerzas, y la maquinaria que
ejecuta el descenso. La 3, el método con que todo se midió. La 4 muestra al agente adulto: su
vida completa, sus números. La 5 estudia la comunicación del equipo, y qué pasa cuando se
apaga. La
6 cuenta las dos campañas por recortar su pensamiento, y por qué fallaron las dos. La 7 sitúa el
trabajo en su familia, y la 8 dibuja sus fronteras, cada una con su puerta.

---

## 1. El modelo, en dos páginas

El agente de este trabajo está orientado por G-EMV, un modelo homeostático publicado
(DOI 10.5281/zenodo.21026795). Esta sección no reexpone ese trabajo: resume únicamente las piezas
que las secciones siguientes usan, y remite al texto publicado para todo lo demás. El agente usa
las piezas constitutivas del modelo, las seis fuerzas, la distancia homeostática, el descenso de
gradiente. El trabajo publicado demuestra además varios fenómenos que se derivan de esas
piezas: que las pérdidas pesan más que las ganancias, que el saciado deja de escuchar su propio
dominio, y otros. Este trabajo no vuelve a demostrar ninguno, ni explica ningún resultado
apoyándose en ellos. Están ahí, operando, porque el motor que los produce es el mismo,
dondequiera que este motor corra, las pérdidas seguirán pesando más que las ganancias. Pero
ninguna conclusión de las páginas que siguen se apoya en que esos fenómenos existan, y ninguna
se caería si no existieran: lo que aquí se afirma se sostiene solo en lo que aquí se mide. Cuando la conducta del agente muestre un pariente de aquellos
fenómenos, por ejemplo, el agente satisfecho que deja de atender su despensa, y el mecanismo
que hubo que añadir para corregirlo, en la sección 2, se contará la mecánica concreta, sin
apoyarse en la taxonomía del modelo.

**El estado: seis fuerzas sobre tres dominios de viabilidad.** El estado interno del agente se
define sobre tres ejes, cada uno correspondiente a un dominio de viabilidad: el físico (F), el de
recursos (R) y el social/relacional (S). Cada dominio está gobernado por dos fuerzas opuestas que
pueden variar independientemente: una de ganancia (f⁺) y una de pérdida (f⁻), ambas de magnitud
no negativa. El estado es el sexteto

S = (f⁺_F, f⁻_F, f⁺_R, f⁻_R, f⁺_S, f⁻_S),  f± ≥ 0.

De la composición de las dos fuerzas de un eje se derivan dos cantidades: la posición (su
diferencia), que indica hacia dónde se inclina el eje, y la tensión (su suma), que indica su carga
total. Dos estados con idéntica posición pueden diferir en su carga interna; esa disociabilidad es
la propiedad estructural central del modelo. Este trabajo no presenta resultados sobre ella,
ningún experimento de los que siguen la pone a prueba, pero opera en cada evaluación: dos
agentes con la misma inclinación pueden estar uno sereno y otro cargado, ambas fuerzas bajas,
o ambas altas, y la distancia que gobierna al agente distingue esos dos estados, porque
combina las dos cantidades, no solo la posición.

**El appraisal queda fuera del modelo; este trabajo lo construye.** El núcleo publicado no
determina el valor de cada fuerza en cada instante: lo toma como entrada de una capa de evaluación
(la percepción, o appraisal) que el modelo declara externa y no formaliza. Ese es exactamente el
punto de enganche entre los dos trabajos. La arquitectura de la sección 2 hace dos cosas:
construye la capa de appraisal que el modelo declaró externa, la proyección del mundo de juego
sobre las seis fuerzas, y monta la maquinaria necesaria para ejecutar el descenso de d en un
mundo con espacio, tiempo y otros agentes: navegación, memoria, compromisos. Esa maquinaria
incluye reglas de persistencia y prioridad entre planes, que disciplinan cuándo se re-arbitra el
descenso sin alterar qué se valora; cada una nació como corrección a una patología medida del
descenso puro en un mundo espacial, y la sección 2 las lista una a una con su motivación. Ninguna
pieza de la arquitectura introduce un segundo criterio de valor: qué importa lo fija el modelo
publicado; qué cuenta como ganancia o pérdida en machina_1 lo fija el appraisal aquí descrito.

**La distancia homeostática y el descenso de gradiente.** Todas las piezas del modelo convergen en
la distancia homeostática d, que mide cuánto se aleja el estado del agente de su configuración de
referencia (los objetivos de posición y tensión de cada eje); combina la desviación de posición,
la desviación de tensión y el acoplamiento entre ejes, en forma compacta,
d = √(d_pos + d_ten + acoplamiento), donde cada término agrega sus cuadrados y pesos internos; la
especificación literal está en el apéndice A del trabajo publicado. Dicho en llano: d mide
cuánto le falta al agente para encontrarse del todo bien, y bajarla es todo lo que el agente
hace. La conducta es descenso de
gradiente: en cada tick, cada paso del reloj del juego, el agente evalúa las acciones a su
alcance y ejecuta la que más reduce d.
No hay en todo este trabajo otro criterio de valor que ese; sí hay, en la maquinaria que ejecuta
el descenso, reglas de persistencia y prioridad entre planes, que la sección 2 declara. Una
consecuencia de la forma de d, cuadrados bajo una raíz, conviene retenerla desde ya. Como
cada desviación entra al cuadrado, estar lejos duele desproporcionadamente: al doble de lejos,
más del doble de dolor. Y por eso el mismo alivio no vale siempre lo mismo: descontado sobre
una desviación grande, borra más dolor que sobre una pequeña. Dicho con un ejemplo: comer vale
más con el cuerpo al borde que con el estómago medio lleno, no porque nadie lo haya decidido,
sino porque la fórmula lo produce. El detalle no es decorativo: cuando dos deseos compitan, en
la sección 2, será esta curvatura la que decida los duelos.

**Descentramiento y proactividad.** El equilibrio del modelo no es la neutralidad: los objetivos
de posición son positivos y, como la tensión de un eje no puede ser menor que el valor absoluto de
su posición, el reposo del sistema queda por debajo de esos objetivos (el descentramiento, gap).
La consecuencia operativa para este trabajo es directa: d no es nula ni siquiera con las tres
posiciones en su objetivo (1,250 en el perfil de referencia). Ese residuo no debe leerse como
malestar perpetuo, sino como apetito estructural: incluso en su mejor estado, al agente cualquier
oportunidad de ganancia le reduce algo de d, de modo que siempre tiene motivos para buscarla. Un
agente cuyo equilibrio fuera alcanzable quedaría, al alcanzarlo, indiferente a todo premio; el
agente de este trabajo no puede quedar indiferente, por construcción. Su disposición a actuar no
se programa ni se premia: es estructural. Es esa propiedad, y no una función de recompensa, la que
pone en marcha todo lo que las secciones 4 y 5 miden.

**Sin aprendizaje.** Los objetivos de posición y tensión, las sensibilidades, los pesos por
dominio y los límites del sistema son constantes del modelo: nada se ajusta con la experiencia, no
hay parámetros entrenados ni función de recompensa que optimizar. Cuando en este trabajo se dice
zero training, se dice en este sentido literal: la geometría es a priori y permanece fija durante
toda la obra.

**El motor, congelado.** El modelo corre como código publicado: `motor/model.py`, md5
`1e511978c251130e95169ebf8443efa1`, idéntico del primer experimento al último. La capa del agente
importa las constantes del motor (objetivos, pesos, sensibilidades); no las copia, de modo que no
existe una segunda fuente de verdad que pueda divergir. La afirmación "el motor no se tocó" no es
declarativa: el md5 se verifica en cada puerta de custodia del método (sección 3), y toda la
evidencia de este trabajo, incluido el marcador, que se computa desde esas mismas constantes
importadas (sección 4), sale de ese motor y no de otro.

---

## 2. La arquitectura

### Bloque A, el appraisal

La sección 1 dejó firmado el contrato entre los dos trabajos. El modelo pone la forma: los tres
dominios, las seis fuerzas, la distancia. Y declara externa la capa que decide qué cuenta como
ganancia o como pérdida en un mundo concreto. Este bloque describe esa capa para machina_1.
Primero, las dos monedas en que operan las fuerzas. Después, el catálogo de fuerzas con sus
tamaños. Al final, cómo compiten entre ellas.

Todos los números salen de las constantes importadas del motor y de la capa de appraisal. El
perfil de cálculo es el de referencia, el del agente de control, y lo definen tres familias de
constantes. Los objetivos de posición, hacia dónde quiere estar inclinado cada eje: (1; 2; 0,8)
para F, R y S. Los pesos por dominio, cuánto cuenta cada eje dentro de la distancia total:
(1,0; 1,0; 1,40). El peso social merece una línea aparte: se fija en 1,40, el doble del valor
por defecto del motor publicado, una elección de calibración de esta capa, horneada en la
configuración de todas las corridas de este trabajo, y declarada aquí. Y las sensibilidades, cuánto mueve a cada eje lo que pasa en el mundo:
(0,30; 0,15; 0,10).

**Las dos monedas.** El appraisal alimenta al motor por dos vías distintas. La primera son las
fuerzas en pie, que tienen dos signos: los dolores y los bonos. Una fuerza en pie describe una
condición del agente, la vida baja, la energía agotada, el territorio poseído que consuela, y
no señala ningún lugar: empuja, o alivia, desde dentro, esté donde esté el remedio. Su tamaño se mide en Δd: cuánto hunde la
distancia d de la sección 1, la medida de cuánto le falta al agente para encontrarse del todo
bien, respecto del agente sano.

La segunda vía son los pulls dirigidos: las ganancias con lugar. La diferencia con el bono no
está en el signo, ambos juegan a favor, sino en la flecha: un pull señala un sitio del mundo.
Una antena ganable, un extractor, el hub que espera el depósito. Su valor se descuenta de d, pero atenuado
por la distancia: valor·0,85^dist. A ese decaimiento lo llamamos el radio del deseo. Cada ganancia
vale la mitad cada ~4,3 celdas. Una oportunidad de valor 2,40 vale 1,06 a cinco celdas y 0,34 a
doce.

La consecuencia en la conducta es directa. Los dolores y los bonos operan desde dentro y no se
apagan con la lejanía, el dolor empuja a salir del estado malo; el bono premia quedarse en el
bueno. Las ganancias tiran desde fuera y se debilitan con ella.

**El catálogo de fuerzas.** La tabla resume las fuerzas del agente final. Para cada una: su eje,
su tipo y su tamaño máximo (el Δd desde el estado sano).

| Fuerza | Eje | Tipo | Tamaño máximo |
|---|---|---|---|
| Cuerpo (vida) | F | dolor en pie | Δd 3,78, la más fuerte del sistema |
| Energía personal | R | dolor en pie | Δd 3,61 |
| Déficit de hearts | R | dolor en pie | Δd 1,641 (peso 2,40; objetivo 5; crece cuadráticamente con la escasez) |
| Territorial (marcador) | R | dolor en pie | Δd 1,641 |
| Bono territorial (poseer antenas alivia) | S | bono en pie | Δd ≈ −0,39 |
| Motor de suministro (dos caras: depósito / minado) | S | pull dirigido | 2,40·techo·0,85^dist |
| Oportunidad de conquista | R+S | pull dirigido | 1,386·0,85^dist |
| Exploración (hacia la frontera no rastreada del mapa) | R | pull dirigido | 0,48·0,85^dist |

Tres notas dejan la tabla honesta. La escasez de la despensa común no es una fuerza en pie: vive
como las dos caras del motor de suministro, y su historia, hubo un tiempo en que se contaba dos
veces, se cuenta en el bloque D. El déficit de hearts, en cambio, sí es hambre personal y
siempre observable: el agente cuenta lo que lleva encima, sin memoria de despensa. Y su reverso,
la riqueza, está declarada en la tabla firmada pero es inerte: la saturación del motor ya hace
que la abundancia no mueva nada. La riqueza que no alivia no atrae, la misma lección que cierra
el bloque D.

Los ocho agentes del equipo corren este mismo perfil. Existe una tabla de ocho temperamentos,
variaciones de pesos por agente, implementada y apagada: queda fuera del agente de este trabajo.

La jerarquía de tamaños no es decorativa. El cuerpo (3,78) y la energía (3,61) dominan el
catálogo. Las ganancias viven muy por debajo, y más aún descontada la distancia. Por eso la
supervivencia manda sin que ninguna regla lo decrete: manda por tamaño.

**La moneda de comparación.** Cuando dos actos compiten, la vara común es Δd en el estado:
cuánto desciende d cada acto, calculado en la situación presente del agente. Y aquí vuelve,
trabajando, la curvatura que la sección 1 pidió retener, la de los cuadrados: como cada
desviación pesa al cuadrado, el mismo alivio descuenta más dolor cuanto más hondo está ya el
pozo. La consecuencia práctica conviene decirla despacio: los tamaños de la tabla no son
precios fijos, son techos. El Δd 3,78 del cuerpo es lo que ese dolor puede llegar a mover con
el agente al borde de la muerte; con el cuerpo a medias, la misma fuerza mueve menos; con el
cuerpo lleno, casi nada. Ninguna fuerza vale siempre lo mismo: cada una vale, en cada tick, lo
que el estado del agente le deja valer. La tabla ordena el catálogo; los duelos los resuelve el
estado, tick a tick.

**El arbitraje, en un caso al dígito.** El escenario E5 enfrenta las dos tentaciones extremas. Un
agente con la energía casi agotada. Y a la vista, una antena gris ganable. En ese estado, el
marginal del cuerpo vale 4,574 y la conquista 2,934. El cuerpo gana por 1,56×. No hay una regla
"primero sobrevivir" en el appraisal. Hay un dolor que, en ese estado, pesa más. En un estado más
holgado, la misma antena ganaría. Así arbitra toda la capa de evaluación. La prioridad, donde
existe como regla escrita, vive en la maquinaria de ejecución (bloque C). Nunca aquí.



### Bloque B, navegación y memoria

El descenso de gradiente es una regla de un solo paso: ejecuta la acción que más reduce d. En un
mundo con paredes y distancias, esa regla necesita maquinaria. Hace falta saber a cuántos pasos
reales está cada cosa. Hace falta recordar lo que salió de la vista. Y hace falta sostener un
rumbo cuando el objetivo queda lejos. Este bloque describe esa maquinaria. Ninguna de sus piezas
cambia qué se valora. Todas operan sobre la medida de la distancia y sobre la ejecución del paso.
Y la distancia ya estaba en la fórmula: el pull decae con ella. Navegar mejor no es querer
distinto. Es medir mejor lo lejos.

**La ventana y el planificador.** El agente percibe una ventana egocéntrica de 13×13 celdas:
radio 6 alrededor de sí, con la visibilidad real dentro del marco cercana a un disco, las
esquinas del cuadrado no se revelan. La ventana es del entorno; sobre ella, esta capa aplica un
candado a su canal social: lo que cae a la vista propia no se acepta de oídas. Sobre ella planifica por programación dinámica. Expande las acciones a su
alcance, evalúa cada estado resultante con el motor, y ejecuta el primer paso del mejor camino. Es
un minimizador de la distancia presente: no acepta empeorar un poco ahora para mejorar después.
Esa miopía tiene consecuencias medidas, y reaparecen a lo largo del trabajo. La meseta: todos los
caminos próximos valen igual y la elección oscila. El atasco contra el muro. Y el bolsillo cuya
salida exige alejarse primero. Las piezas de este bloque son las curas de esas patologías, una a
una.

**La distancia geodésica.** La distancia que le importa a un cuerpo no es la recta: es la
caminable. Sobre el mapa conocido, el agente calcula la distancia real a pie hasta cada celda. A
ese cálculo lo llamamos el campo geodésico. Las ganancias, los desempates y las rutas se alimentan
de ese campo, no de la línea recta. Con lo desconocido, el principio es optimista: lo no visto se
asume caminable. Así el desconocimiento no encarcela. La alternativa, asumir muro donde no se ha
mirado, dejaría al agente preso de su propia ignorancia.

**La memoria.** Fuera de la ventana, el mundo no desaparece. La memoria retiene posiciones: los
extractores, las antenas, el hub. Y la regla de borrado es estricta: solo borra el desmentido
real. Desmentir de verdad es volver al lugar, tenerlo dentro del alcance de la vista, y
encontrarlo ausente. Salir de la vista no refuta nada. Esta regla nació de una falsa refutación
medida: un pozo dado por desaparecido solo porque quedó en el borde de la ventana, tapado, sin
estar de verdad a la vista.

El recuerdo tiene además dos tiempos. La posición no envejece. El estado sí: la confianza en lo
recordado decae con el tiempo, y con ella la altura del pull hacia ello.

Dos excepciones, cada una con su muerto. El hub no se olvida jamás: un agente murió sin casa a la
que volver porque su memoria del hub caducó. Y los muros se recuerdan aparte, sin decaer: un
registro que veta el paso contra sólido conocido. A esta capa pertenece también la lectura
estricta del territorio: casa es solo el territorio propio. El criterio anterior preguntaba
únicamente si una casilla tenía dueño, sin mirar de quién era, y para un agente malherido, el
frente enemigo pasaba por casa. Uno fue a curarse allí, y murió. Desde entonces, la pregunta es
de quién.

**El horizonte abierto.** A veces el objetivo queda más allá del alcance del planificador. La
pieza que el agente final lleva para eso es la geodésica global: el campo de distancias caminables
se calcula sobre todo el mapa conocido, no solo sobre la ventana. Un hub a treinta o cincuenta
celdas ya crea gradiente por sí mismo. Es la pieza que usa el retorno del moribundo (bloque C).

Hubo antes otra pieza para el mismo problema: la meta próxima. Cuando el objetivo lejano no creaba
gradiente, reubicaba la atracción en un punto intermedio del camino, dentro del alcance, que
heredaba el valor del objetivo. Curó una inmovilidad medida: un cargado pasó de 466 ticks quieto a
3. Y quedó fuera del agente final, superada: con la geodésica global, el paisaje plano que ella
curaba ya no existe. Se nombra porque enseña un patrón de la casa: las piezas también se jubilan,
y se jubilan con su número.

**El límite real, declarado.** La navegación se cerró dos veces por regla de parada. El cuello que
quedó no es navegar: es descubrir. El agente solo persigue lo que alguna vez entró en su vista. No
existe imperativo de exploración en el catálogo, solo un residuo: un pull hacia la frontera no
rastreada, el más débil de la tabla, casi siempre eclipsado por cualquier deseo con nombre.
Nada convierte el no-saber en empuje que mande. En el examen de ocho agentes, solo uno vio la antena a cuatro celdas del hub.
Los demás la tuvieron siempre fuera del alcance. Ese límite es estructural, y se retoma en la
sección de fronteras, donde queda dibujada también la puerta que lo abriría: tratar la
ignorancia misma como un dolor. Una de sus respuestas es que otro te cuente lo que no viste: la comunicación
entre agentes. Esa pieza, el pregonero, es percepción extendida. No introduce valor nuevo:
amplía lo que el appraisal puede traducir.



### Bloque C, los compromisos

La sección 1 dejó una promesa pendiente. El agente lleva algunas reglas escritas, y lo
prometido fue listarlas todas, cada una con el problema medido que la hizo necesaria, y
demostrar que ninguna decide qué importa: eso solo lo decide la balanza de fuerzas. Este bloque
cumple esa promesa. Todas las reglas que siguen son del mismo tipo, reglas de constancia:
cuándo mantener un plan y cuándo soltarlo, y cada una
existe porque su ausencia mató a alguien o dejó a alguien clavado. Y conviene decir bien de
dónde vienen: la intuición propuso más de una, proponer es el oficio de la intuición, pero
ninguna se quedó por intuición: se quedaron las que el banco confirmó, y con la letra que la
medida les dio.

**Por qué hace falta la constancia.** El agente, tal como lo dejó el bloque A, decide de cero en
cada tick: mira el mundo, pesa sus fuerzas, y hace lo que más reduce su distancia d. Eso tiene una
virtud enorme, nunca queda preso de un plan viejo, y un defecto que solo aparece en la práctica:
cuando dos opciones valen casi lo mismo, el agente duda. Y como al tick siguiente vuelve a decidir
de cero, puede dudar para siempre. El caso que lo retrató: un agente cargado de mineral, solo,
pegado a la puerta de su propia casa, a un paso de entregar. Para su cálculo, dar el paso por el
norte o por el sur valía exactamente igual, y se pasó la vida alternando norte, sur, norte, sur,
delante de su puerta, sin entrar jamás. No estaba roto: estaba perfectamente indeciso.

La cura es el compromiso: cuando el agente elige un plan, lo apunta y lo ejecuta hasta el final
sin volver a discutirlo a cada paso. Pero con una salvedad aprendida por las malas, porque el
proyecto también probó lo contrario, congelar las decisiones del todo, y descubrió que los
hábitos congelados crean sus propias trampas (ese resultado tiene su propia sección, más
adelante). Ni discutirlo todo a cada tick, ni no discutir nada nunca: planes que se mantienen, con
motivos tasados para romperse. En eso consiste este bloque: cuatro compromisos, cada uno con su
disparo, sus motivos de ruptura, y el cadáver o el atasco que lo justifica.

**Cómo se ejecuta un compromiso.** Los cuatro comparten la misma mecánica. El plan es una ruta:
la lista de pasos hacia el objetivo, calculada sobre el mapa de distancias caminables que el
bloque B presentó, siempre por el paso que más acerca. Y el último paso de toda ruta es el
contacto: en este mundo, las cosas se hacen tocándolas, el mineral se mina chocando con el
extractor, la entrega se hace chocando con la casa. Si no existe camino conocido, la ruta vuelve
vacía y no hay compromiso: la maquinaria no inventa caminos que no ve.

**El compromiso de entrega.** Se activa cuando el agente lleva el lote completo, cinco unidades
y la despensa común necesita material. Es, ni más ni menos, la cara de "deposita" del motor
económico del bloque D, con constancia añadida. ¿Qué lo rompe? Cuatro motivos, escritos: que el
mundo rechace el paso (alguien ocupa la celda, un muro no conocido); que la oportunidad
desaparezca de verdad; que el dolor del cuerpo crezca; o que aparezca un objetivo claramente
mejor, y "claramente" tiene número: vale al menos una vez y media más. El número es una
constante declarada, no un óptimo buscado: nadie barrió sus vecinos, y lo que el banco confirmó
es la regla entera con ese umbral dentro. Mejor a secas no basta, porque dos objetivos
parecidos que se alternan son otra forma de la duda infinita.

**El compromiso de minado.** Se activa cuando el agente va con el bolsillo por llenar y hay un
extractor que perseguir, visto ahora o recordado. Su regla de ruptura es la más fina de las
cuatro, y distingue dos cosas que parecen iguales: cambiar de material y cambiar de pozo. Si la
economía pasa a necesitar otro material, la despensa ya tiene silicio, ahora falta carbono, el
plan viejo sobra y se suelta: obedecer a la despensa es el sentido del viaje. Pero si aparece
otro pozo del mismo material, un poco más cerca, el plan no se suelta. La diferencia tiene
historia: un agente pasó su vida orbitando entre dos pozos de silicio equivalentes, a media
distancia de ambos, cambiando de favorito a cada tick sin tocar ninguno. Con la regla, la órbita
se convierte en línea recta al pozo elegido.

**El compromiso de conquista.** Se activa cuando el agente va equipado, el aligner, la
herramienta de alinear antenas, y un heart, la munición que cada alineación gasta, ambos fabricados
en la despensa común con lo que el equipo mina, y hay una antena que tomar. Lo rompe el rechazo del mundo, el dolor del cuerpo, o que
la antena ya sea nuestra, incluida la que un compañero tomó primero, porque el objetivo era que
fuera nuestra, no tomarla uno mismo. No lo rompe que aparezca otra antena más cerca, ni que el
rival capture la elegida: el viaje sigue. Su historia fundacional es la del bloque D: los
portadores perfectamente equipados que llegaban hasta las antenas y no entraban, 226 contactos,
cero conquistas. Con este compromiso activo, en su primera prueba, el portador fue, entró y gastó
su munición. Era la conducta que el sistema nunca había producido.

Hay además un orden entre los tres: entrega, minado, conquista, se evalúan así, y el primero que
dispara se lleva el plan. Ese orden hace, sin regla nueva, que un agente cargado no se distraiga
conquistando: primero se entrega lo que se lleva. El suministro pasa antes que el oficio, por
orden de evaluación, no por decreto.

**Puerta de casa.** Cuando la reserva de vida cae bajo el umbral, el dolor del cuerpo pesa más
que cualquier otra cosa. Hasta aquí decide la balanza, como siempre. Pero la ruta a casa que se
compromete entonces tiene una propiedad única en todo el sistema, y hay que decirla clara: es
inquebrantable, no se cambia por nada. Ni el dolor, ni una oportunidad por buena que sea. Solo
la termina el hecho de llegar a casa, o que el mundo la rechace: que el paso intentado no ocurra
porque otro cuerpo ocupa la celda o un muro desconocido la cierra. En ese caso el agente no ha
cambiado de opinión, es el camino el que ya no existe, y se recalcula hacia la casa, al mismo
destino.

Esta es la única regla del agente que decide por escrito y no por peso, y por eso se lleva el
párrafo más largo del bloque: las excepciones se pagan con detalle. Su motivación son diez
muertes. En las corridas largas de una era anterior murieron diez agentes, y la autopsia encontró
en todos el mismo mecanismo. La alarma sonó a tiempo en los diez, el agente supo que debía
volver. Pero el viaje de vuelta, decidido tick a tick con la casa fuera de la vista, avanzaba a
trompicones: donde un rumbo firme cierra una casilla por tick, ellos cerraban entre cero y 0,67.
Y mientras dudaban, sangraban, a una unidad de vida por tick en tierra de nadie, y al doble
(1,96, medido) en territorio enemigo. Murieron a seis, a doce casillas de su puerta. La balanza
había acertado en qué importaba; lo que falló fue la constancia del viaje. La regla escrita
garantiza exactamente eso: que el viaje más importante de todos no se re-discuta en cada esquina.

La cura se completa con un detalle de prudencia: el umbral que dispara la vuelta no es fijo, en
territorio enemigo se dobla (de 25 a 50 unidades de reserva), porque allí se sangra el doble, y
el factor sale de esa sangría medida, no del ojo. Puestos los diez muertos como jueces sobre el
papel, la regla salva a nueve. El décimo estaba a 54 casillas de casa, en pleno territorio
enemigo: necesitaba más vida de la que le cabía en el cuerpo, y ninguna regla de retorno lo
salva, lo suyo era no haber ido tan lejos, que es otra esquina del diseño y así se nombra.

**El conflicto que se disuelve solo.** Con cuatro compromisos conviviendo, cabe esperar choques.
El caso que parecía inevitable: un agente cargado, comprometido a entregar, que empieza a
desangrarse camino de casa. ¿Qué manda, la entrega o la supervivencia? La respuesta resultó ser
que la pregunta está mal hecha: los dos destinos no compiten porque están anidados. La
supervivencia pide la casa, la zona propia, donde el cuerpo se regenera, y la entrega pide
el hub, que vive dentro de ella. El agente moribundo y cargado hace un solo viaje, con la
protección de la ruta inquebrantable: al cruzar la puerta ya se está curando, y al llegar al
hub, si sigue cargado, entrega. No hubo que
escribir ninguna regla de desempate, y de ahí un principio que gobierna todo el diseño: donde la
geometría disuelve el conflicto, no se escribe regla. Las reglas son para los conflictos que la
geometría no disuelve, y resultaron ser muy pocos.

**Lo que ninguna regla toca.** Para cerrar el bloque conviene decir con calma qué es lo que estas
cuatro reglas *no* hacen, porque ahí está el punto que la sección 1 prometió defender.

El agente tiene dos sistemas trabajando juntos, y hacen trabajos distintos. El primero es la
balanza del bloque A: las fuerzas con sus tamaños, pesándose unas contra otras en cada tick. La
balanza responde a la pregunta "¿qué es lo más importante ahora?", y la responde con números,
comparando cuánto aliviaría cada opción. El segundo sistema son las reglas de este bloque, y
responden a otra pregunta: "lo que la balanza ya eligió, ¿con cuánta constancia se persigue?".

La promesa de la sección 1 era que las reglas jamás invaden el terreno de la balanza. Y se puede
verificar regla a regla: ninguna de las cuatro cambia el tamaño de una fuerza, ni el peso de un
dominio, ni el valor de una oportunidad. Ninguna dice "esto importa más de lo que la balanza
cree". Todas operan sobre otra cosa: la ruta ya elegida, y los motivos para abandonarla o no.

Un ejemplo con números lo deja a la vista, y los números vienen del bloque A, del escenario de
prueba que allí se presentó: un agente con la energía casi agotada que ve, a su alcance, una
antena lista para conquistar. La tentación máxima en el peor momento. ¿Quién decide? La balanza,
sola: recuperar energía aliviaría su distancia en 4,574; la conquista, en 2,934. Gana el cuerpo,
por número, 1,56 veces más, sin que ninguna regla haya intervenido. Si el mismo agente
estuviera descansado, los números saldrían al revés y la antena ganaría, con las mismas reglas
dormidas. Las reglas de este bloque solo despiertan *después*: una vez la balanza elige, protegen
el viaje hacia lo elegido.

Esa división del trabajo, el valor lo pone la balanza, la disciplina la ponen las reglas, es la
frase-puente de la sección 1, cumplida: en todo el agente no hay más criterio de lo que importa
que la geometría publicada.



### Bloque D, la constitución económica

La economía del mundo pide una cadena completa. Hay que minar cuatro elementos, carbono,
oxígeno, silicio y germanio. Hay que llevarlos al hub, la casa, la despensa común. Con ellos,
el hub fabrica el equipo. El juego ofrece un catálogo de equipo fabricable más
ancho del que este agente usa: de ese catálogo, el agente fabrica y emplea solo dos piezas, el aligner, la herramienta de
alinear, y los hearts, los corazones que sirven de munición, porque con ellas basta para
cerrar el ciclo entero. Los cuatro elementos no son equipo: son la materia prima que todo lo
demás consume. Con el aligner y un heart, un agente puede alinear una antena: eso es
conquistar, y eso es lo que puntúa. Este bloque cuenta
cómo el agente gobierna esa cadena. Y cuenta también su historia, porque la constitución final no
se diseñó de una pieza: se ganó a base de forenses.

**El motor de suministro.** La despensa habla por un solo canal: el motor de suministro. Tiene dos
caras y nunca las dos a la vez. Si el agente va cargado con el lote, la cara dice: al hub, a
depositar. Si va vacío y a la despensa le falta algo, la cara dice: a minar lo que falta, el
elemento más necesario, no el más cercano. La fuerza de este canal no es fija. Lleva un techo
continuo: su altura baja cuando el dolor del cuerpo sube. Un agente sano abastece con ganas. Un
agente dolorido, cada vez menos, hasta que el cuerpo manda. No hay interruptor: es una cuesta.

Esa forma merece nombre y explicación, porque se repite tres veces en el agente. La idea: en
lugar de una puerta de sí-o-no, "si pasa esto, deja de desear aquello", el deseo se
multiplica por un factor continuo: un dial entre cero y uno que se desliza con el estado. El
motor de suministro lleva el primero: su techo baja según el dolor del cuerpo sube, el agente
sano abastece con ganas; el dolorido, cada vez menos, hasta que el cuerpo manda. El colchón del
equipo, que aparece más abajo, lleva el segundo: el gasto del oficio se frena a medida que la
despensa se acerca al mínimo vital. Y la fuerza de volver a casa lleva el tercero: crece según
la reserva de vida cae. Las llamamos las tres hermanas. La lección que las parió se pagó con
bancos en su día: los interruptores de sí-o-no fallan por los dos lados. Si el interruptor
corta el deseo de golpe, aplasta, el obrero que cruza el umbral suelta la faena a medio hacer,
aunque estuviera a un paso. Si lo deja pasar entero hasta el corte, vagabundea, persigue con
toda la fuerza, hasta el último instante, lo que ya casi no debería tocar. La cuesta hace lo
que la puerta no sabe: el deseo se debilita poco a poco según el estado aprieta, y la conducta
gira suave en vez de romperse.

**El limbo del saciado.** La primera versión de la despensa tenía una enfermedad fina. Cuando el
hub alcanzaba lo justo para fabricar lo vital, una unidad de oxígeno, tres de carbono, una de
germanio y una de silicio, se declaraba
satisfecho. Ningún dolor sonaba. Nadie minaba, nadie depositaba, y la despensa quedaba congelada
en el punto exacto donde el fallo la pilló. Medido: el hub congelado en [3,3,3,3] en la corrida
del forense, el oficio muerto, el marcador a
cero. Lo llamamos el limbo del saciado. Y conviene decir lo que es: el pariente operativo de la
ceguera por saturación que el modelo publicado demuestra como fenómeno. El que se siente bien
deja de escuchar su propio dominio, el eje, de los tres de la sección 1, que ya tiene
satisfecho. Allí era un teorema con ablaciones; aquí fue una enfermedad
con cadáver.

**La banda de respiración.** La cura fueron dos cuestas. Por debajo de la holgura, el nivel
vital más el coste del equipo: [1,3,1,1] más [1,3,1,1], la holgura [2,6,2,2], el suministro
empuja: la despensa pide hasta tener
margen, no solo hasta el mínimo. Por encima de lo vital, el oficio puede gastar, pero con un
colchón continuo que frena el gasto cuando se acerca al mínimo. Entre las dos cuestas, la despensa
respira: se llena, se gasta, se rellena. Sin limbo, porque por debajo de la holgura siempre hay
empuje. Sin drenaje, porque el gasto se frena solo antes de tocar lo vital.

**El paro.** La banda se llevó al banco con su criterio congelado de antemano, como todo en esta
obra. Y el banco dio dos verdades a la vez. La despensa respiró de verdad: por primera vez en el
proyecto, el hub no se congeló, entraron tres de los cuatro elementos, y la ventana del oficio se
abrió. Pero el marcador colapsó a cero, y el criterio decía: si el marcador se hunde, se para. Se
paró. La banda se apagó entera y se escribió el freno. El criterio pre-declarado mandó
sobre el marcador: no fue una derrota del diseño, fue la disciplina del método ejecutándose, el
mismo freno que protege cada número de este trabajo.

**El forense que absolvió a la banda.** La sospecha natural era que la banda tenía la culpa: el
abastecimiento absorbía a los ocho agentes y nadie conquistaba. La autopsia del marcador puso esa
sospecha a prueba: cinco hipótesis, cuatro descartadas con datos, una confirmada. ¿El suministro
aplasta el deseo de conquistar? No: el deseo de conquista ganaba la elección el 66% de los ticks.
¿La geografía los mantenía lejos? No: hubo 226 contactos con antenas conquistables. ¿No las
conocían? No: unas cuarenta antenas en memoria. La confirmada fue la quinta: llegaban y no
entraban. 226 contactos, cero conquistas. Los portadores tocaban la puerta y no cruzaban el
umbral. La cura, por tanto, no era económica: era el compromiso de conquista del bloque C, el
aterrizaje. Con ella, el cuadro final encaja: la banda encendida, la despensa respirando, y la
conquista convertida en acto, conversión del 100% de los contactos, mediana de marcador 1,705 en
cinco corridas, el equipo entero vivo, los cuatro elementos en el hub, exploración residual a cero.

**Lo que quedó fuera, declarado.** La constitución final también se define por sus apagados. La
despensa como fuerza social en pie quedó apagada: la escasez vive en el motor de suministro, y
mantener las dos era contar el mismo hambre dos veces. La fabricación de hearts quedó en el cajón,
con su razón medida: la cuna de nacimiento trae ocho hearts y el gasto de aquellas corridas era de dos a cuatro por
corrida, con munición sin gastar, fabricar más no toca; primero se aprende a disparar. De esa
espera es la máxima de la era: aterrizar antes que fabricar. Y una enmienda al orden del motor
quedó también aparcada con su número delante: solo el 8,8% del deseo de conquista quedaba
aplastado por el suministro, el cuello no era ese.

**El principio de la era.** Dos derrotas distintas, el heart que drenaba la despensa sin llegar
a equipar, y el colchón solo que se congelaba en el limbo, escribieron la misma lección: el deseo
que no puede consumarse no satura. Una fuerza sin su cadena completa detrás no produce conducta:
produce estampidas o parálisis. La constitución final es eso: cada deseo con su cadena entera,
del elemento que falta al bump que lo entrega, del equipo en mano a la antena alineada.



### Bloque E, qué no hay

Los bloques anteriores contaron lo que el agente lleva: sus fuerzas, su navegación, sus
compromisos, su economía. Este último bloque cuenta lo contrario, lo que el agente no lleva,
porque en un trabajo como este las ausencias dicen tanto como las piezas: cada cosa que falta
es una decisión tomada a propósito, no un descuido, y varias de esas ausencias son exactamente
lo que el experimento quiere poner a prueba. La lista, una por una.

**No hay aprendizaje.** Nada en el agente se ajusta con la experiencia. Los objetivos de cada
dominio, los pesos, las sensibilidades, los tamaños de las fuerzas: todo es constante del primer
tick al último, y de la primera corrida a la última. El agente del final de la obra es
exactamente el del principio, no ha mejorado, no se ha adaptado, no recuerda nada de vidas
anteriores. Lo que cambia entre corridas es lo que sabe del mundo (su mapa), nunca lo que le
importa. La sección 1 lo dijo del modelo: sus constantes no cambian. Aquí se dice
de todo lo demás. Tampoco aprende la capa que traduce el mundo, los pesos y umbrales del
appraisal son fijos, ni las reglas de constancia, sus márgenes son los mismos el primer día
y el último. El conjunto entero, modelo, traducción y reglas, es tan fijo como sus partes.

**No hay función de recompensa.** En la técnica habitual de agentes, una función de recompensa
es un contador de puntos que el sistema intenta maximizar: haz esto, suma; haz aquello, resta,
y la conducta entera se moldea persiguiendo ese número. Aquí ese contador no existe. El marcador
del juego, la puntuación que machina_1 lleva de cada equipo, no entra al agente por ninguna
vía: ninguna fuerza lo mira, ninguna regla lo menciona. El agente no sabe que puntúa. Alinea
antenas porque el territorio le duele y la oportunidad le atrae, porque hacerlo reduce su
distancia, y el marcador sube como consecuencia externa, igual que la abeja no sabe que
poliniza. Cuando la sección de resultados mida el marcador, medirá un efecto de la conducta, no
su objetivo.

**No hay red ni política aprendida.** Tampoco hay, bajo el capó, una red neuronal, el tejido de
millones de números ajustados por entrenamiento que gobierna a la mayoría de los agentes
actuales. El que decide es el planificador del bloque B: despliega las opciones a su alcance,
se las da a evaluar al motor publicado, y ejecuta la mejor. Cero parámetros entrenados, cero
episodios de práctica. La política entera, todo lo que el agente puede llegar a hacer y por
qué, cabe en un archivo de reglas legibles, y cada regla tiene su motivación escrita en esta
sección. Se puede auditar con los ojos, cosa que ninguna red permite.

**No hay conductas-objetivo escritas.** Ninguna línea del agente dice "en la situación X,
persigue Y". No hay un guion de comportamientos, ve a minar al empezar, vuelve si te atacan,
como el que llevaría un personaje de videojuego. Los destinos los pone siempre el descenso de la
distancia: qué minar lo dice el material que falta en la despensa, cuándo volver lo dice el
dolor, qué antena tomar lo dice la oportunidad mejor pesada. Lo que sí hay escrito quedó
dicho en los bloques B y C, reglas de memoria y reglas de constancia, y ya se demostró de
qué lado están: disciplinan el viaje; no eligen el destino.

**No trae nada apuntado de casa.** El agente llega a machina_1 sin saber nada del mundo de
antemano: ni los nombres de las cosas, ni las recetas, ni los números. Todo lo que necesita lo
lee del propio mundo al llegar. Los nombres, cómo se llaman los recursos, las antenas, los
equipos, los toma de la configuración de la partida. Las recetas de fabricación las lee del
juego, y de ellas calcula cuánto necesita la despensa: nadie eligió esas cantidades a mano. Y
las constantes del modelo se importan del motor publicado, el model.py del primer trabajo, en
vez de copiarse: no existe una segunda copia de los números que pueda desviarse de la publicada
sin que se note. Es una propiedad de construcción, y como tal se enuncia, el experimento no se
ha corrido: si machina_1 amaneciera con otros nombres, el agente los leería al arrancar igual
que leyó los de hoy, porque para él los nombres nunca significaron nada, son etiquetas de las
que cuelga sus deseos, y con otras recetas recalcularía las cantidades. Nada viaja escondido
en él.

**No hay exploración que merezca el nombre.** El bloque B lo dejó dicho con su matiz: en el
catálogo vive un residuo, el pull más débil de la tabla, hacia la frontera no rastreada, pero
ningún imperativo: al agente su ignorancia no le duele. Persigue lo que vio o lo que le
contaron; lo que nunca entró en su vista ni en el tablón apenas existe para él. Es la frontera
medida de esta arquitectura, y se retoma en la sección de límites.

**No hay representación del otro.** Los compañeros existen para el agente como cuerpos que
ocupan celdas y como anuncios en el tablón común, nunca como individuos. No hay censo, no hay
memoria de quién dijo qué, no hay identidades. Toda la cooperación que este trabajo muestra,
el mapa compartido, la vida salvada, las antenas que un compañero adelanta, ocurre sin que
nadie sepa quién es nadie. Esa ausencia no es un descuido: es el experimento. Y donde termina el
anonimato empieza el trabajo siguiente.

Lo que queda, cuando todo eso falta, es exactamente lo que este trabajo quiere medir: una
geometría publicada de lo que importa, una capa que traduce el mundo a esa geometría, y las
curas mínimas que la ejecución exigió. Las secciones que siguen miden lo que ese agente, así de
desnudo, hace.

---

## 3. El método

Un proyecto largo tiene un enemigo que no es el mundo: es el propio autor. Los resultados siempre
admiten una explicación favorable si se buscan después de verlos, y un sistema que se toca por el
camino puede acabar demostrando cosas sobre sí mismo y no sobre lo que pretendía. Esta sección
describe los tres hábitos con los que este trabajo se defendió de eso.

**El primero: el motor no se toca, y se comprueba.** El modelo publicado corre aquí como código
congelado. Su huella digital, el md5: un resumen matemático del archivo, tal que si una
sola letra del código cambiara, la huella entera cambiaría, se verifica antes de cada
experimento, y es la
misma desde la primera corrida hasta la última: `1e511978c251130e95169ebf8443efa1`. Se comprueba
además que el sistema que se ejecuta contiene exactamente el código que el experimento dice
probar. No son gestos de ceremonia: son la condición para que un resultado entre en este trabajo.
Sin ellas, la afirmación "esto lo hace el modelo publicado" sería una promesa en lugar de un
hecho.

**El segundo: los criterios se escriben antes de mirar.** Cada experimento de este trabajo se
declara por escrito antes de correrse: qué se cambia, qué se mide, y, lo importante, qué
resultado contará como éxito y cuál como fracaso, con números. Después se corre, se lee y se
acata. El orden es todo: quien decide el listón después de ver el salto siempre lo pasa.

Aquí conviene fijar dos palabras que el trabajo usa constantemente. Una corrida es una partida
completa: los ocho agentes soltados en el mundo durante un número fijo de pasos, ticks, en la
lengua del juego, hasta el final.
Y la vara es la configuración de referencia contra la que se compara todo lo demás, el agente
con su pila estable, de modo que cada afirmación del tipo "esta pieza hace X" es siempre una
diferencia medida entre la vara y una corrida idéntica salvo por la pieza en cuestión. De ahí el
procedimiento que las secciones de resultados usan una y otra vez: para saber qué hace algo, se
apaga y se compara.

Los criterios, además, solo se corrigen hacia adelante. Cuando la experiencia demuestra que un
listón medía mal, se re-declara por escrito para los experimentos futuros, pero el veredicto que
dictó, incluido un paro injusto, se queda en el registro tal cual. Un criterio se corrige para el
futuro; nunca para el pasado.

**El tercero: medir vidas enteras, no instantes.** Que una pieza esté encendida no demuestra
que haga nada. Lo que cuenta es su efecto contado sobre la vida completa del
agente: cuántas veces actuó, qué cambió en la conducta, qué pasó al apagarla. Un interruptor
encendido no es un resultado.

Ese hábito trajo el hallazgo metodológico más incómodo del trabajo, y merece contarse entero
porque explica cómo se leen todos los números de las secciones siguientes. Al principio se creía
que la puntuación era determinista: dos corridas idénticas daban exactamente el mismo resultado.
Se había verificado, y era cierto, pero en corridas cortas. Al medirlo sobre vidas completas
apareció lo contrario: la misma configuración, corrida tres veces, daba 1,705, 2,322 y 2,785. No
lo rompía ninguna pieza nueva; lo rompía el horizonte. En corridas cortas casi nada ha puntuado
todavía y una diferencia minúscula del principio no ha tenido tiempo de propagarse; en una vida
entera sí. Se localizó incluso el punto de partida de la divergencia en un par de corridas
extremas: la primera acción distinta ocurría en el tick 13, y esa bifurcación diminuta llegaba a
decidir, casi doscientos ticks después, si un agente alcanzaba una antena a tiempo o no.

La consecuencia fue re-fundar la manera de medir. Desde entonces, ninguna afirmación de este
trabajo se apoya en una sola corrida: los experimentos se repiten, cinco corridas es el estándar
adoptado, y se reporta la mediana, el valor del medio: tantas corridas por encima como por
debajo, con su rango, la peor y la mejor. Hay medidas, además, en que el cero es un
resultado frecuente, y conviene decir por qué: puntuar exige que la cadena entera aterrice
dentro de la ventana medida, minar, abastecer, fabricar, equipar y entrar, y en horizontes
cortos muchas corridas se quedan a un eslabón. Para esas medidas se reporta también cuántas de
las cinco corridas puntuaron algo: es lo que distingue un "a veces lo logra" de un "nunca". Los veredictos anteriores no se
tiraron: se re-leyeron con honestidad, quedando acotados. Los que describían el funcionamiento del
cuerpo del agente, que sobrevivía, que la despensa recibía sus cuatro materiales, resultaron
idénticos en todas las corridas y siguieron en pie sin matices. Los que citaban una puntuación
pasaron a ser lo que siempre habían sido sin saberlo: una muestra de una distribución.

Queda un cierre que completa el arco, y que este trabajo tardó meses en poder escribir. Durante todo
ese tiempo se midió con medianas y rangos frente a una variabilidad real pero sin causa conocida.
La causa apareció al estudiar la comunicación: el orden en que los ocho agentes escriben en el
tablón común varía de una corrida a otra, y ese orden decide qué noticia llega primero. Apagado el
tablón, tres corridas idénticas salen exactamente iguales. El método se corrigió dos veces sin
romperse: primero adaptándose a un azar que no entendía, después nombrándolo.

**Qué significa, entonces, un número en este trabajo.** Todo valor citado en las páginas que
siguen cumple tres condiciones: procede de un experimento declarado antes de correrse; se midió
sobre vidas completas y, cuando la magnitud lo pedía, sobre varias corridas con su mediana y su
rango; y salió del motor publicado, con su huella verificada. Los que no cumplen alguna de esas
condiciones no aparecen, o aparecen con su límite escrito al lado.

---

## 4. El agente adulto

Las dos secciones anteriores contaron cómo está hecho el agente y cómo se mide lo que hace. Esta
cuenta lo que hace. Es la parte de la biografía donde el protagonista está en su plenitud, y se
narra como se vivió: una primera vez, una cura, un horizonte que se estira, otra cura, y la
vida completa. Un recordatorio antes de empezar, para evitar una confusión natural: nadie
reparte papeles. No hay mineros, porteadores ni conquistadores de oficio, los ocho corren el
mismo perfil, y quien mina, quien acarrea o quien conquista en cada momento es circunstancia,
no casta: el que pasa cerca del pozo, mina; el que sale equipado primero, conquista. Una nota de honestidad sobre las cifras, antes de empezar: los bancos de veredicto,
así llama esta obra a sus experimentos decisivos: la pieza corre contra su criterio congelado,
y el resultado se acata, corren a cinco corridas con su mediana, como fijó el método; los reconocimientos de
horizonte largo corren a tres, se reportan como rango, y se declaran como lo que son,
reconocimiento, no certificación.

**La primera vez que todo funcionó.** Durante meses, el agente supo hacer cosas sueltas: vivir,
o minar, o recordar, nunca todo a la vez. El banco de las cinco curas fue el día en que el
cuerpo entero arrancó junto: el equipo completo vivo de principio a fin, sin una sola muerte; el
anillo de pozos alrededor de casa retenido en la memoria en vez de olvidado; los mineros llegando
a sus pozos sin deambular, la deambulación, que había sido plaga, bajó a cero,; y los cuatro
materiales del juego entrando en la despensa, incluido el silicio, el último eslabón de la
cadena, que jamás había llegado a casa. Aquel día quedó un frente abierto, y el registro lo dice
sin adorno: la puntuación fue cero. El agente hacía despensa, y no conquistaba. Sabía vivir;
todavía no sabía ganar, aunque conviene decir esto último con propiedad, porque para el agente
"ganar" no existe. Como dejó dicho la arquitectura, el marcador no entra en él por ninguna vía:
solo existe su distancia, estar bien, que nada le duela, ir hacia lo que le atrae. Lo que aquel
cero señalaba no era una meta incumplida, porque el agente no tiene metas que incumplir: era que
una de sus atracciones, la de las antenas, no estaba llegando a consumarse en el mundo. El
problema no era de deseo; era de viaje. Y por eso su cura no fue darle motivos, sino constancia.

**El gasto vive.** Es decir: la munición por fin se gasta, el heart que el portador llevaba
encima entra, al fin, en una antena. El porqué de aquel cero ya lo contó la arquitectura: los
portadores llegaban hasta las antenas y no entraban. Conviene recordar aquí el orden de los
tiempos: la sección 2 describió al agente terminado, con todas sus piezas; esta sección cuenta
cuándo nació cada una. Aquel día del cero, el compromiso de conquista aún no existía, nació
precisamente como cura de esto. Recuérdese su letra: elegida una antena, el viaje se protege hasta entrar y gastar, y ni una antena más
cercana ni un dolor pasajero lo interrumpen. Se llevó al banco con el criterio nuevo, cinco
corridas y mediana, y el resultado le dio la vuelta a la
biografía: la mediana de puntuación dejó el cero, de 0 a 1,705, y todas las corridas puntuaron.
El detalle que mejor lo cuenta no es la cifra sino la forma: antes, un portador acumulaba decenas
y hasta cientos de contactos con antenas sin entrar en ninguna; con la cura, los contactos se
desploman a un puñado, va, entra y gasta. La conversión de contacto en conquista pasó de
prácticamente nada al cien por cien. El agente ya no ronda lo que desea: lo toma.

**El horizonte se estira, y destapa un problema.** Con el cuerpo entero y la conquista viva, se
estiró la vida a mil ticks para ver qué hace el agente cuando el tiempo sobra. Aparecieron dos
cosas. La primera, buena: la conquista no es cosa del arranque, los agentes conquistan a lo
largo de toda la vida, y en una corrida el equipo firmó una ráfaga tardía de cinco antenas en
ciento diez ticks, extendiendo
su frente mucho más allá de la cuna. La segunda, mala: la vida larga mata. Tres y cuatro agentes
por corrida morían desangrados, lejos de casa, en viajes que la vida corta nunca les había pedido.
El reconocimiento fue claro: el problema más urgente del agente adulto no era ganar más, era no
morir por el camino.

**La sangría, curada.** La respuesta fue la ruta inquebrantable del moribundo, la puerta de
casa del bloque C, con sus diez muertos de motivación. Recuérdese qué hace: cuando la reserva de
vida cae bajo el umbral, el agente compromete la ruta a casa sobre su mapa completo y no la
suelta por nada, solo la termina llegar, o que el mundo la rechace y haya que recalcular hacia
el mismo destino; y en territorio enemigo, donde se sangra el doble, la alarma suena antes. Su
banco es el más rotundo de la obra:
las muertes por sangría bajaron a cero en las tres corridas, el equipo entero terminó vivo las
tres veces, y la puntuación, lejos de pagar un precio por tanta prudencia, subió, de mediana
3,00 a 5,16. La lectura importa más que el número: vivir no cuesta producir. Los salvados no se
esconden en casa, trabajan, y sostienen las antenas que antes se perdían con su portador muerto.
Y la simetría que lo firma: el mismo agente que en las corridas de control moría clavado a
treinta y ocho casillas de su puerta, con la cura activa recorre el mismo peligro de vuelta,
malherido, en territorio hostil, y cruza la puerta de casa. Ese cruce existe en vídeo, cuadro a
cuadro, sacado de los datos.

**La vida completa.** Quedaba la pregunta final: la vida entera, dos mil quinientos pasos. Y
conviene declarar ese horizonte con sus dos patas, porque es protocolo de este trabajo, no
límite del juego: la liga oficial corre partidas de diez mil. La pata científica: dos mil
quinientos pasos contienen el ciclo conductual completo del agente, expansión, madurez,
quiescencia, y su economía de dotación (unos ocho hearts de cuna contra un gasto medido de
seis a nueve en la vida completa) está calibrada casi exactamente a esa ventana. La pata
material: un agente deliberativo sin compilar cuesta unas treinta horas de máquina por vida, y
el protocolo de triplicados a diez mil pasos habría sido inviable. La foto del agente adulto, tomada tres veces: puntuación mediana 3,23, ni una muerte en
ninguna de las tres vidas, y un techo nítido, el agente conquista su territorio y lo sostiene,
alrededor de siete antenas, contra las cincuenta y dos oleadas enemigas que el juego le lanza, y
no expande más allá. El marcador, recuérdese, se acumula por tick, mantener puntúa, y en
una de las tres vidas la aritmética se deja ver desnuda: nueve mil ciento cuarenta y nueve
antena-ticks repartidos en dos mil quinientos pasos son 3,66, la puntuación exacta de esa
corrida, al diezmilésimo. El techo no lo pone el tiempo: lo pone la munición. Y ahí, una elegancia que
nadie diseñó a propósito: la dotación de corazones con que nace el equipo, decidida mucho antes
de conocer este dato, resulta casi exactamente calibrada para la vida completa, se agota,
literalmente, con el último aliento de la vida medida. La pieza para fabricar más quedó en el cajón con
razón: su momento sería una vida aún más larga.

Esta foto deja además dos semillas plantadas, que la sección del precio de pensar cosecha. La primera: el
agente adulto se repite, de joven, una de cada tres decisiones es idéntica a otra ya tomada; de
viejo, dos de cada tres. La rutina emerge sin que nadie la programe. La segunda: pensar le cuesta
cada vez más, el árbol de opciones que despliega cada tick se espesa con la edad, hasta el
final, y la vida tardía es la más cara de pensar. Un agente que cada vez repite más y cada vez
piensa más caro: esa tijera abierta es exactamente la promesa que tentó los reflejos, y de ella
trata la sección del precio de pensar.

**La fuerza que no hubo que escribir.** La biografía del adulto cierra con un episodio que
resume el diseño entero. Faltaba, sobre el papel, una última fuerza: la defensa del territorio,
que perder una antena doliera, que el agente acudiera a recuperarla. Se diseñó completa. Y antes
de construirla, el método mandó ponerle jueces: los robos reales de las corridas largas,
examinados tick a tick. El veredicto fue el mejor final posible: el agente ya sentía el robo. En
este mundo, una antena robada no pasa al enemigo, queda gris, sin dueño. Y la gris, para el
agente, ya atrae: es exactamente lo que el compromiso de conquista persigue. Y vale la pena decir
por qué en este mundo el robo no llega a ser un oficio: el agente nunca ve una antena en manos
enemigas como algo que arrebatar. Las antenas, para él, están en dos estados, suyas, o grises
y ganables, y cuando el rival golpea una suya, no se la lleva: la desconecta, y la deja gris.
Recuperarla es, otra vez, conquistar. Por eso el catálogo del juego incluye herramientas de
disputa que este agente conoce de nombre y jamás fabricó: nunca vivió la situación que las
pide. Y la condición gemela, declarada: en el horizonte y el mapa medidos, ninguna antena rival
entró jamás a alcance, rivales a cero en veinte mil agente-ticks,; la disputa directa es
territorio no observado de este protocolo, no una imposibilidad del agente ni del juego. Y por eso el registro
muestra que cada robo cercano se recuperó siempre, solo, sin fuerza nueva; lo único fuera de
alcance fue una pérdida lejana y tardía, marginal, en el último suspiro de la partida. La fuerza
que faltaba resultó estar implementada sin saberlo, implícita en la geometría, y se archivó sin
gastar una hora de máquina. Es el hermano mayor de un principio que la arquitectura ya enunció:
donde la geometría ya hace el trabajo, no se escribe fuerza. El agente adulto quedó completo no
cuando se le añadió la última pieza, sino cuando se comprobó que no hacía falta.

---

## 5. El pueblo: la palabra en el equipo

Los ocho agentes del equipo comparten una sola pieza social: el pregonero. Es un tablón de
anuncios común. Cada agente publica en él lo que ve de primera mano, extractores y antenas, con
su posición, y lee lo que publicaron los demás. No hay encuentros: el tablón se lee desde
cualquier punto del mundo, cada tick, sin cruzarse ni acercarse, como una red a la que los ocho
están siempre conectados. Cruzarse con otro por el camino no añade nada: no existe el canal
del encuentro, todo, absolutamente todo, pasa por el tablón. Y lo oído pesa menos que lo
visto: los anuncios ajenos entran en la
memoria con confianza rebajada. Comunicación hay, y abundante: los agentes se dicen cosas
millones de veces por vida, esto está aquí, esto está allá. Lo que no hay es lenguaje en el
sentido lingüístico: los anuncios son hechos con formato fijo, qué y dónde, no símbolos cuyo
significado haya que interpretar. Con este canal no se puede mentir, ni matizar, ni preguntar:
solo constatar. No hay protocolo aprendido: nadie negocia qué publicar. Y no hay autor: el
anuncio no dice quién lo puso. Los agentes no se conocen entre sí;
comparten un mapa, no una sociedad. Este capítulo mide qué hace esa pieza en el agente completo,
con el método de toda la obra: para saber qué hace una pieza, se la apaga y se compara la vida
con ella y sin ella. Y los criterios de éxito o fracaso se escriben, con número, antes de ver
ningún resultado, la doctrina completa se cuenta en la sección del método.

**La anatomía del canal: casi todo repetición, y sin embargo sostiene el mapa.** Dos números
definen el canal, y juntos parecen una contradicción. Primero: es un diluvio de repetición. El
universo de hechos distintos que puede viajar es pequeño, 1.184 en la corrida de referencia, y
sin embargo se inyectan millones de veces: la novedad máxima posible es el 0,20%; el 99,8%
restante es re-anuncio de lo ya dicho. Segundo: ese diluvio sostiene el conocimiento del agente.
Entre el 80% y el 96% del mapa de cada agente, el 85% de media, vino del tablón, no de sus
ojos. De lo que viaja, tres cuartas partes son extractores y el resto antenas; los muros no
viajan. El agente debe la mayor parte de su mundo a la palabra, no a la vista. La resolución de
la contradicción aparente es el hallazgo central del capítulo, y sale de los dos experimentos que
siguen: apagar el canal del todo, y quitarle solo la repetición.

**El silencio: apagar el canal.** Tres corridas de vida completa con el tablón apagado, contra la
vara con el tablón encendido. Cuatro hallazgos, cada uno con su número.

Primero: la cosecha no depende del canal. El marcador de las tres corridas mudas fue 3,408, las
tres idénticas, frente a la mediana 3,23 de la vara. Los agentes con solo sus ojos conocen siete
veces menos mundo (140 objetos de media contra 1.010), y cosechan lo mismo. La explicación está
en el cuello de botella de este mundo: lo que limita la puntuación es la cuna de hearts, no la
información. La delimitación se declara sin rodeos, y con su condición: para el agente tal como
está constituido, en machina_1 y a la vida medida, los dos mil quinientos pasos del
protocolo, todos nacen millonarios: la munición de conquista viene de serie,
y la dotación de arranque supera con margen lo que este agente llega a gastar, porque la pieza de
fabricar más quedó en el cajón. La riqueza es relativa al deseo: un agente construido para
maximizar el marcador podría fabricar munición sin descanso, y para él este mundo no sería una
herencia sino una fábrica, y el papel del canal podría ser otro. Lo mismo vale para un mundo
donde el descubrimiento limitara: cabría esperar lo contrario.

Segundo: el canal salva una vida. Uno de los ocho, el que vaga más lejos de casa, muere en las
tres corridas mudas, en el mismo tick de las tres (t2231), y en la vara vive. Su autopsia:
conocía 199 objetos con solo sus ojos frente a 989 con el tablón, exploraba a cuarenta y dos celdas de
casa, y cuando la alarma de volver sonó, ya no daba la vida para el camino. El mapa social es
infraestructura de supervivencia para el que va lejos: la palabra como farola, no como moneda,
no compra cosecha; alumbra el camino de vuelta.

Tercero: el canal era la lotería. Toda la obra convivió con una variabilidad entre corridas
idénticas que obligó a medir con medianas, rangos y triplicados. Al apagar el tablón, esa
variabilidad desapareció por completo: tres corridas mudas dan el 100% de acciones idénticas,
determinismo conductual, verificado acción a acción. Con el tablón, el 25%. La fuente del azar
tenía nombre: el orden de llegada de las escrituras al tablón compartido, distinto en cada
corrida por razones ajenas al agente. Esto re-lee la historia del método sin re-escribirla: los
criterios de medición fueron correctos para el sistema que medían, un agente con tablón, y
ahora, además, la varianza que los motivó tiene mecanismo.

Cuarto: el canal enfoca al que planifica. Cada tick, el planificador despliega un árbol de
opciones, las acciones a su alcance y sus consecuencias, unos pasos hacia delante, y elige.
Contra la intuición, el agente mudo, que conoce siete veces menos mundo, despliega un árbol más
gordo que el de la vara. Saber dónde está el blanco permite ir a por él; la ignorancia obliga a
considerar de más. El tablón adelgaza ese árbol un 17%.

**El candado: quitar solo la repetición.** Si el 99,8% del tráfico es re-anuncio, la tentación es
obvia: un candado de "ya lo sé". El que publica no repite lo que no ha cambiado; el que lee no
vuelve a apuntar lo que ya sabe. El candado se construyó, pasó sus verificaciones en frío, y
cumplió su encargo: los anuncios cayeron más del 86% y el mapa se conservó. Y aun así se archivó,
porque falló en los dos premios que se esperaban de él.

El primer premio era ahorrar trabajo. Ocurrió lo contrario: el sistema quedó un 45% más lento por
paso. La repetición tenía una función oculta: cada re-anuncio es también un "esto sigue ahí",
renueva la fecha de lo sabido, como los sellos de fecha en los alimentos. Sin repetición, los
recuerdos no se borran pero envejecen: el agente confía menos en información cada vez más vieja,
y camina rutas peores hacia datos rancios. Se ahorró en anuncios y se pagó en pasos. (Este
resultado es de una sola corrida, y así se declara.)

El segundo premio era calmar el azar entre corridas. Para entender por qué no lo hizo, hay que
saber de dónde venía el azar: ocho agentes escriben en el tablón cada tick, y el orden en que sus
escrituras llegan varía de una corrida a otra por razones de la máquina, ajenas al agente, como
ocho personas echando cartas al mismo buzón, donde quién llega un segundo antes cambia cada vez.
Ese orden importa la primera vez que cada noticia llega: enterarse del extractor del norte antes
que del sur, o al revés, tuerce las primeras decisiones, y de ahí, las vidas enteras divergen.
El candado eliminaba las llegadas repetidas, pero la primera llegada de cada noticia seguía
llegando cuando llegaba: el sorteo estaba en el primer reparto, no en los recordatorios. Medido:
con candado, las corridas coinciden en el 27,9% de sus acciones, lo mismo que la vara con su
25%.

**La vara no cambia.** Tras los dos experimentos, el pregonero sigue encendido en el agente, con
su diluvio de repeticiones incluido. Lo que da está medido: salva al que va lejos, mantiene
fresco el mapa, y ahorra trabajo al planificador, su árbol de opciones queda un 17% más delgado.
Lo que cuesta también está medido: casi todo su tráfico es repetición, y es la fuente del azar
entre corridas. Se queda encendido porque lo que da vale más que lo que cuesta, y las dos cifras
están sobre la mesa. Queda además una herramienta de regalo: si un experimento futuro exige que
dos corridas salgan exactamente iguales, apagar el tablón lo consigue, el determinismo está a un
interruptor, sabiendo ya qué se pierde a cambio.

**Una idealización, menos irreal de lo que parece.** El canal es global por construcción:
comunicación sin coste, sin distancia y sin encuentro. Para un agente en un mundo físico, eso es
una idealización, y conviene decirlo sin rodeos. Pero no es ciencia ficción: es la condición que
nuestro propio mundo ha construido. Vivimos conectados a una red donde los avisos llegan solos,
estemos donde estemos, sin buscar a quien los publicó, y lo publicado por cualquiera alcanza a
todos. El tablón del equipo es esa condición en miniatura, con sus pros y sus contras medidos:
el mapa común que salva al que va lejos, y el diluvio de repetición que nadie pidió. Nótese
además que la idealización hace los resultados más fuertes, no más débiles: ni con esta conexión
perfecta mejoró la cosecha, el cuello estaba en otro sitio. Lo que queda sin probar es la
comunicación local: la de los que se cruzan, la del tablón físico en la casa común que se
consulta al volver. Es una frontera declarada de este trabajo, y el lugar natural donde la
colmena anónima empieza a convertirse en otra cosa.

**Una convergencia, ofrecida con prudencia.** Hay una hipótesis clásica sobre el lenguaje humano
la del chismorreo, de Dunbar, según la cual la conversación sirve sobre todo para mantener el
mapa social: la mayor parte de lo que hablamos es repetir lo que ya se sabe, y esa repetición no
es ruido, confirma vigencia. El candado es, sin buscarlo, una miniatura computacional de esa
idea: suprimimos la redundancia comunicativa de una colmena y el coste fue medible, el mapa
envejeció. No se afirma más que la convergencia: un agente sin lenguaje, con un tablón de hechos,
reprodujo la lección de que repetir lo sabido es mantener fresco lo común. El diálogo formal con
esa hipótesis, la cita, lo que afirma exactamente, y dónde nuestra miniatura se queda corta, se
hace en la sección dedicada a la literatura, junto al resto de parientes de este trabajo.

---

## 6. El precio de pensar

La sección del agente adulto dejó dos semillas plantadas en su foto final. El agente, con la edad,
repite una parte cada vez mayor de sus decisiones, de una de cada tres a dos de cada tres. Y pensar le
cuesta cada vez más: el árbol de opciones que despliega en cada tick es, con enorme diferencia,
casi todo su gasto de cómputo: el árbol se lleva
prácticamente todo el tiempo de pensar, y lo demás que la mente hace, evaluar las fuerzas,
mantener la memoria, calcular las distancias, cuesta tan poco que, en la cuenta, es un
redondeo. Y el árbol se espesa hasta el final
de la vida, de modo que la vejez piensa varias veces más caro que la juventud. Un agente que
cada vez se repite más y cada vez paga más por deliberar: la conclusión parece escribirse sola.
Si tanto se repite, recuérdese la respuesta y sáltese el pensamiento. Si el árbol engorda,
pódese. Esta sección cuenta las dos campañas que intentaron exactamente eso, con instrumentos
cuidadosos, criterios congelados y toda la disciplina del método, y cómo las dos terminaron en
la misma orilla: no había nada que recortar. El precio de pensar no era un despilfarro. Era el
órgano.

**Primera campaña: el reflejo. La sonda.** Antes de darle reflejos al agente, se construyó un
instrumento para medir si los merecía: una sombra que acompaña la vida entera apuntando, en cada
situación ya vista, "yo habría respondido esto", sin decidir nada, sin tocar la conducta. La
sombra censó al adulto completo, y su censo dio dos resultados que valen por sí mismos. El
primero: el árbol confirma más que elige. En el 97,8% de la vida, las opciones que el agente
compara valen casi lo mismo, la deliberación termina en un "da igual" que cualquier respuesta
razonable satisface, y la decisión genuina, aquella en que elegir mal costaría de verdad, es
apenas el 0,3% de los ticks. El segundo: la rutina emerge con la madurez. La sombra reconocía un
tercio de las situaciones del agente joven y tres cuartos de las del viejo. La razón es de vida,
no de programa: el joven aún descubre, y cada día le trae situaciones nuevas; el viejo ya tiene
su mundo hecho, los mismos pozos, las mismas rutas, la misma casa, y el mismo mundo produce
las mismas situaciones. La vida se vuelve repetible sin que nadie programe la repetición.

**El mando, y sus tres refutaciones.** Con ese censo, el paso natural: dejar que el reflejo
decida lo que reconoce y reservar el árbol para lo nuevo. Se construyó con toda la prudencia,
el reflejo solo hablaba en terreno llano, lo dudoso siempre al árbol, y falló tres veces, cada
una refutando una esperanza distinta. La primera fue la más instructiva de la obra: dos corridas
idénticas, misma imagen, mismo mundo, misma configuración, y una se clavó para siempre,
oscilando ante su propia casa en un vaivén del que nunca salió, mientras la otra vivió una vida
limpia. El fallo no era determinista: era una moneda al aire del azar de máquina. La segunda
refutación probó la cura geográfica, prohibir el reflejo cerca de casa, donde el vaivén había
aparecido, y el vaivén simplemente se mudó: ciento catorce bucles severos en campo abierto. La
clase del fallo no era un lugar. La tercera probó la cura de sentido común, disparar el reflejo
solo si la acción acercaba al objetivo, y tampoco: sesenta y seis bucles con el objetivo
volteándose entre dos celdas adyacentes, el agente orbitando entre dos deseos equivalentes.

**El techo, y el hallazgo con nombre.** La pregunta que las tres refutaciones dejan en la mesa
es la buena: ¿y qué pasaría si funcionara? Un reflejo que acierta el 91%, el nuestro, suena a
tener casi el mismo agente, algo más barato. No lo es, por dos hechos medidos. El primero: en
este sistema, una decisión distinta no se queda en anécdota, se propaga. El método ya lo contó
con su ejemplo: una sola acción diferente en el tick 13 acababa decidiendo, doscientos ticks
después, si una antena se alcanzaba a tiempo. Un reflejo que responde distinto al árbol en una
de cada doce decisiones no produce "casi la misma vida un poco peor": produce otra vida, y,
bancada, una que pierde. El segundo hecho es el letal: el resto que el reflejo no acierta es
exactamente la medicina. Esa pequeña variación del árbol ante el empate, el temblor: nada
tiembla en el cuerpo; tiembla la respuesta, era lo que llevábamos eras maldiciendo como
ruido, y resultó ser la inmunidad del agente. En un empate perfecto entre ir al norte o al sur,
quien responde siempre lo mismo reconstruye el mismo empate en el paso siguiente, y repite el
vaivén para siempre; quien alguna vez responde distinto, sale. El reflejo, al responder siempre
igual ante lo mismo, congela justo la salida del bucle, por eso sus bancos no dieron un agente
un poco peor: dieron agentes clavados ante su puerta hasta la muerte. ¿Y de dónde sale ese
resto que ningún reflejo puede acertar? La sonda lo midió. Reduce cada situación a una firma,
la foto que un reflejo vería: qué hay alrededor, qué se lleva encima, qué duele, y cuando la
misma foto reaparece en la vida, pregunta: ¿respondió el árbol lo mismo que la vez anterior?
Solo el 92,65% de las veces. No porque el árbol eche dados, es determinista, sino porque
dos momentos con la misma foto nunca son idénticos del todo por debajo, y en el empate la
elección se decide por detalles que la foto no ve. Ese 92,65% es, por construcción, el techo de
cualquier memoria de respuestas: si ni el propio árbol coincide consigo mismo más que eso,
ninguna copia que mire la foto puede imitarlo mejor, no se puede cachear una verdad que no
existe. El reflejo alcanzaba el 91%: no era malo; era que el objetivo no existía. Y de ahí el
hallazgo que da nombre a la campaña: la moneda era el mecanismo. El mando se retiró entero; la
sombra sigue viva como lo que siempre fue, un instrumento de medición.

**Segunda campaña: los bisturís.** Si no se puede recordar, quizá se pueda recortar: el árbol
engorda con la edad, pódese lo que no se usa. Esta campaña estrenó su propio instrumento, un
microscopio de lectura: antes de construir poda alguna, se midió sobre 1,3 millones de
expansiones reales del árbol qué recortaría exactamente cada criterio candidato. Y aun así, con
el paso previo en verde, los tres bisturís que se probaron encontraron lo mismo. La ejecución
comprometida, no re-deliberar mientras se ejecuta un plan ya comprometido, resultó neutral a
la conducta, la vida del agente salió idéntica, decisión a decisión, y sin premio en el
reloj: el mismo tiempo por paso. El porqué merece párrafo aparte: su derrota, como se verá, no fue
culpa del agente sino del laboratorio en que se le mide. El primer cono, podar
las ramas que se alejan del objetivo, no tuvo punto dulce: al 48, al 22 y hasta al 4 por ciento
de poda, el marcador cayó siempre, y su forense encontró el porqué: las ramas "que se alejan"
eran el radar de la conquista, las rutas con rodeo hacia las antenas secundarias, las que el
agente toma cuando la principal está servida. Y el segundo cono, el principiado, podar solo lo
que la geodesia declara rodeo verdadero, con su paso previo verificado en verde, cayó también,
y su caída escribió la ley final: el árbol que se espesa no es grasa acumulada; es el alcance.
La vida tardía piensa caro porque conquista lejos, y capar el árbol es capar exactamente las
conquistas que exigen navegar.

**Dónde vive cada pared.** Conviene decirlo antes de sumar las derrotas, porque no todas tienen
el mismo domicilio. La del reflejo y las de los conos son paredes del agente: quitar el temblor
crea los bucles, capar el árbol capa la conquista, eso pasaría en cualquier mundo. La de la
ejecución comprometida es una pared del laboratorio. Este pueblo se mide en un mundo síncrono:
los ocho agentes cruzan cada tick juntos, y el reloj de cada paso lo marca el que más tarda en
decidir. Visualícese con robots: ocho cuerpos en una nave donde ninguno da su paso siguiente
hasta que el más lento ha terminado de decidir el suyo. A la vista, un desperdicio; como
laboratorio, es la condición que hace auditable una vida entera, paso a paso. En un mundo
asíncrono, cada cuerpo iría a su ritmo natural, quien enfrenta lo difícil pensaría despacio,
quien hace lo fácil correría ligero, y allí los ahorros condicionales de cada cabeza sí se
cobrarían. Esa espera es una elección del método, no una imposición del juego, el torneo real
empuja, y un agente que piensa en segundos viviría allí como una estatua; el laboratorio espera
a propósito, para que un agente deliberativo pueda vivir su vida entera y ser auditado. El
precio de esa elección es que en el reloj de pared solo cuenta lo que acelera a los ocho a la
vez. Y el ahorro de la comprometida existe, cada agente se salta el árbol en una cuarta parte
de sus ticks, pero es condicional y desincronizado: los ocho solo coinciden en estar
comprometidos dos ticks de cada mil, y en un colectivo síncrono lo que no coincide no suma. En
otro mundo, asíncrono, de un solo agente, o donde el cómputo se facturara por cabeza, esa
misma pieza pagaría. Las tres paredes se reportan; cada una con su domicilio.

**La tesis de la sección.** Cuatro intentos, un reflejo y tres bisturís, cada uno con su
instrumento, su criterio congelado y su banco, y cuatro derrotas que, miradas con el domicilio
delante, se reparten así: tres son del agente, y una es del mundo en que se le mide, este
laboratorio síncrono. Las del
agente dicen que su deliberación es irreducible por los dos flancos: no se puede recordar,
porque la variación del replanteo es su inmunidad contra los bucles; no se puede recortar,
porque el árbol es su navegación. La del laboratorio dice que el reloj síncrono no paga ahorros
condicionales, verdad del equipo medido, no del agente que lo compone. Lo que parecía
despilfarro, la indiferencia del 97,8%, el temblor del empate, el árbol espesándose, resultó
ser, pieza a pieza, el órgano funcionando. Es un resultado negativo, y se reporta como lo que
es; pero dice algo positivo sobre esta arquitectura: en un agente cuya conducta entera emana de
una sola geometría, no quedó holgura entre el pensar y el hacer donde meter la tijera.

**Lo que queda abierto.** Enterrada queda una hipótesis concreta: la de pensar menos. Sigue
abierta, y es otra clase de trabajo, la de pensar más barato: que el mismo árbol, con las
mismas decisiones, cueste menos segundos de máquina por mejoras de pura implementación. Ninguna
de las leyes de esta sección lo prohíbe; ninguna conducta cambiaría. Y sigue vivo el instrumento
de sombra, apagado por defecto, listo para censar al agente cada vez que una pregunta lo
merezca. La sección de fronteras recoge ambas cosas.

---

## 7. La familia

Este trabajo tiene dos familias, porque no camina solo. Los parientes del modelo, las teorías
de las que la geometría desciende y con las que discute, quedaron presentados en el motor, la
primera parte de esta serie, y no se re-litiga aquí lo que allí está dicho: el aprendizaje por refuerzo
homeostático como precursor formal más cercano [4], y los marcos de energía libre e inferencia
activa como la vecindad más ambiciosa, con sus semejanzas y sus diferencias medidas allí frase a
frase. Quien quiera ese mapa, lo tiene en el primer trabajo. Aquí se presentan los parientes que
el agente, no el modelo, se ha ganado por el camino.

**La hipótesis del chismorreo.** El capítulo del pueblo terminó ofreciendo una convergencia con
prudencia, y esta es su casa formal. La hipótesis, debida a Dunbar [3], sostiene que la conversación
humana sirve ante todo para mantener el mapa social del grupo, que la mayor parte de lo que
hablamos es repetición de lo ya sabido, y que esa repetición no es ruido sino mantenimiento: al
repetirlo, confirmamos que sigue vigente. Nuestro experimento del candado, suprimir la
redundancia comunicativa de una colmena y medir el coste, funciona, sin haberlo buscado, como
una miniatura computacional de esa idea: quitada la repetición, el mapa común envejeció y el
colectivo pagó en pasos. La convergencia se ofrece con sus límites a la vista, que son grandes:
nuestro tablón lleva hechos con formato fijo, no conversación; no hay vínculos que mantener ni
individuos que conocer; y el resultado del envejecimiento es de una sola corrida, declarada. No
afirmamos que el pueblo confirme a Dunbar: afirmamos que un colectivo sin lenguaje, al perder su
redundancia, exhibió el coste que la hipótesis predice para el nuestro. Si esta clase de agentes
madura, un sistema así de pequeño y auditable podría servir de instrumento de medida para
preguntas de ese campo. De momento, queda como lo que es: una coincidencia registrada.

**Los agentes que maximizan.** La familia dominante de los agentes en mundos como éste es la del
aprendizaje por refuerzo: una función de recompensa, millones de episodios de entrenamiento, y
una política que emerge optimizando el premio. Este agente es de otra especie, no lleva
recompensa, no entrena, y su conducta emana de una geometría publicada antes de tocar el juego,
y conviene decir con el mismo cuidado lo que esa diferencia afirma y lo que no. No se afirma
prioridad: la idea de gobernar agentes por regulación interna en lugar de premio externo tiene
linaje, las arquitecturas motivacionales de los años noventa [5] ya gobernaban criaturas
artificiales por pulsiones y homeostasis, con la supervivencia como meta primaria y sin premio
que maximizar, y el propio refuerzo homeostático es el puente formal entre ambas familias. No
se afirma
eficiencia: no hemos medido a este agente contra un agente entrenado en su mismo mundo, y este
trabajo no sostiene que le ganara. Lo que se afirma es más modesto y se sostiene entero en las
secciones anteriores: que la combinación, geometría fija publicada con anterioridad, cero
entrenamiento, cero recompensa, y una vida completa auditada pieza a pieza, produce un agente
viable, económicamente competente y socialmente funcional en un mundo competitivo que no diseñó
su autor. La contribución es la existencia demostrada y documentada, no la superioridad.

**El hábito y la deliberación.** La sección del precio de pensar dialoga, sin haberlo
planeado, con una discusión clásica de la conducta [6]: la división del trabajo entre un
sistema deliberativo, lento, flexible, que planifica con un modelo del mundo, y uno habitual
rápido, rígido, que responde de memoria. Conviene decir primero dónde está este agente en ese
mapa: no tiene los dos sistemas. Es deliberación pura, un solo planificador que despliega y
elige en cada tick, y la balanza de fuerzas que lo alimenta no es un hábito: valora, no
recuerda respuestas. El experimento del reflejo fue, en esos términos, intentar añadirle el
sistema habitual que no tenía, y lo medido es que aquí no pudieron ni convivir: el hábito
congelado crea bucles de los que el deliberativo es inmune por su propia variación. Esa es la
nota al pie empírica que este trabajo deja en aquella discusión, con la particularidad que la
hace legible: los dos sistemas compartían exactamente el mismo criterio de valor, de modo que
el fallo no pudo venir de que quisieran cosas distintas, vino de la constancia misma. No la
elevamos a teoría; queda donde las notas al pie sirven, al alcance de quien trabaje esa
frontera en sistemas mayores.

**El mapa, cerrado.** La familia de este trabajo, dicha en una frase: desciende, por el lado del
modelo, del refuerzo homeostático y de las arquitecturas motivacionales; convive con el
aprendizaje por refuerzo como una especie distinta, si hubiera que ponerle nombre: un agente
homeostático de geometría publicada y cero entrenamiento, sin competir con él; y toca, sin haberlo
buscado, dos discusiones vecinas, la evolución del lenguaje y el hábito frente a la
deliberación. Es una familia pequeña, y cabe entera en esta página.

---

## 8. Las fronteras

Esta última sección es el mapa de los límites del agente. Cada límite está medido, tiene su
porqué en la arquitectura, y varios llevan su puerta declarada, por dónde se saldría, si se
quisiera salir.

**Apenas explora.** Es la frontera más honda, y ahora se dice con su matiz medido: el catálogo
lleva un pull residual hacia la frontera no rastreada, el más débil de la tabla, casi siempre
eclipsado por cualquier deseo con nombre, pero ningún imperativo. La exploración existe como
fuerza residual, no como mandato: el agente persigue lo que vio o lo que le contaron, y lo que
nunca entró en su vista ni en el tablón apenas existe para él. En el examen de
ocho agentes, una antena a cuatro celdas de casa quedó sin ver por siete de ellos durante vidas
enteras. Añadir una fuerza de curiosidad es fácil de decir y comprometido de hacer, sería la
primera fuerza que no responde a un dolor ni a una oportunidad presente. Cabría imaginarla de
otra manera, y vale la pena dejarlo dicho: tratar la ignorancia misma como un dolor, la
información como un recurso más, cuya falta duele en el dominio de los recursos, que es donde
un recurso vive. La forma habla la gramática del modelo tal como está, tres dominios, y
ninguno nuevo, y el trabajo pendiente es de esta capa: darle altura a ese dolor y ponerlo a
competir en el catálogo. La puerta queda declarada y cerrada.

**No conoce a nadie.** Toda la vida social del agente ocurre en el anonimato: cuerpos que ocupan
celdas, anuncios sin autor. No hay censo de individuos, ni memoria de quién dijo qué, ni la
posibilidad de tratar distinto al que ayuda que al que estorba. Este trabajo demostró cuánta
cooperación cabe en ese anonimato, el mapa común, la vida salvada, la antena que un compañero
adelanta, y precisamente por eso deja medida la línea base de la pregunta siguiente: qué añade,
a una colectividad que ya funciona sin ella, la representación del otro. Esa pregunta es otro
trabajo, y empieza donde éste termina.

**Ha vivido en un solo mundo.** Todos los resultados de este trabajo son de machina_1, y varios
llevan la condición puesta en la frase: la cosecha no depende del canal *en un mundo donde la
munición viene de serie*; el reloj síncrono no paga ahorros condicionales *en este laboratorio*.
Nada se ha medido en otro juego, con otra economía, con otro censo de agentes. La arquitectura,
la capa de traducción más las reglas de constancia, está escrita para ser portada; la
portabilidad, sin embargo, es una promesa sin banco, y aquí no se afirma lo que no se midió.

**Sabe volver, pero no sabe no ir.** La cura del retorno dejó las muertes por sangría en cero,
y dejó también, nombrado, su residuo: el caso del agente que se adentró tanto en territorio
hostil que ninguna regla de vuelta podía salvarlo, porque necesitaba más vida de la que cabe en
un cuerpo. El retorno está resuelto; la prudencia de no adentrarse tanto, no. Es una esquina
pequeña, un caso entre diez en su día, una pérdida marginal en la vida completa, y queda
declarada como lo que es: la única muerte que este diseño todavía no sabe impedir.

**Tiene techo, y es el suyo.** El agente adulto sostiene alrededor de siete antenas contra el asedio
constante, y no expande más allá: su munición de cuna se agota con la vida. La pieza para
fabricar más existe y quedó en el cajón con su razón medida, su momento sería una vida más
larga que la medida, que el juego, de hecho, ofrece: fue el protocolo de este trabajo el que
acotó la ventana. La extrapolación al horizonte de liga es aritmética y se declara: a diez
mil pasos, la dotación de cuna es insuficiente, el asedio exigiría del orden de veinticinco a
treinta y cinco reconquistas, y el agente no moriría: quebraría. La fabricación de hearts,
existente en el mundo, ausente de su repertorio, es la pieza que ese horizonte exigiría, y
queda en el cajón con su condición cuantificada. Igual que los ocho temperamentos,
implementados y apagados:
el equipo de este trabajo es un equipo de iguales, y la pregunta de qué hace la variedad de
caracteres queda intacta, con su tabla lista.

Las vidas, además, no solo se contaron: se miraron. Un reproductor construido desde los propios
registros permitió revisar visualmente la corrida de la mediana entera, y el caso más llamativo
un agente quieto unas tres cuartas partes de su vida, junto a la casa, resultó ser
exactamente lo que el diseño predice: saciedad documentada, el motor de deseos en silencio
desde el tick 157, sin faena pendiente, sano y en casa. Descanso, no atasco: en los ocho
agentes no se encontró un solo caso de deseo sin aterrizar. El reproductor queda como material
de auditoría junto al resto de la evidencia.

**Piensa caro, y eso ya no es una frontera: es un resultado.** La sección del precio de pensar
enterró la hipótesis de pensar menos, por los dos flancos, con cuatro mediciones. La de pensar
más barato, el mismo árbol, las mismas decisiones, menos segundos de máquina, se probó
después, y dejó una pieza y un muro. La pieza: reutilizar un trabajo de lectura que el propio
ciclo hacía y descartaba compró un 9,5% de velocidad con la vida del agente idéntica tick a
tick, ningún número de este trabajo se mueve. El muro: se midió si una maquinaria más rápida
podía ejecutar el mismo cálculo con fidelidad exacta, y no puede, en una de cada dos mil
quinientas entradas, el último bit difiere. La referencia publicada vive en su maquinaria;
acelerarla de verdad exigiría re-fundarla, otra referencia, otra vara, otro trabajo, y esa
puerta queda declarada y cerrada. Y queda una segunda puerta, que la sección del precio de
pensar dejó dibujada: una de las cuatro paredes era del laboratorio, no del agente. En un mundo
asíncrono, o donde el cómputo se facturara por cabeza, el ahorro condicional de la ejecución
comprometida, que aquí no suma porque el reloj lo marca el más lento, sí pagaría. Pensar más
barato tiene, pues, dos caminos: mejor fontanería en este mundo, u otro mundo. Y queda una
herramienta en el código, que conviene explicar
porque volverá a usarse: el instrumento de sombra que presentó la sección del precio de pensar.
Es un observador que acompaña una corrida tomando notas, en cada situación apunta qué habría
respondido un reflejo, cuánto se repite el agente, dónde duda, sin decidir nada y sin tocar una
sola acción. Apagado, que es su estado por defecto, el agente es exactamente el de siempre.
Encendido, la vida tampoco cambia: solo queda censada. Si una pregunta futura necesita ese censo,
el instrumento está listo, se enciende, se mide, y se vuelve a apagar.

**La palabra viaja gratis.** El tablón de este trabajo es global: sin coste, sin distancia, sin
encuentro. El capítulo del pueblo lo declaró como idealización y midió lo que da y lo que
cuesta. La comunicación local, la del que se cruza con otro, la del tablón físico en casa que
se consulta al volver, queda sin probar, y es la frontera donde lo social de este trabajo y la
pregunta del otro se tocan: los encuentros son, entre otras cosas, la ocasión de saber quién es
quién.

**El cierre.** La biografía queda entregada: una geometría publicada, un cuerpo que la ejecuta
en un mundo hostil, un método con sus criterios escritos antes de mirar, y este mapa de límites
con cada puerta a la vista. Y conviene decir despacio por qué el mapa cierra el trabajo en vez
de empequeñecerlo. Lo que el agente hace quedó medido en las secciones centrales: vive,
abastece, conquista y coopera, sin premio que perseguir, sin entrenamiento que lo moldee, sin
más reglas que las declaradas una a una. Lo que no hace quedó medido aquí con el mismo instrumental: no
explora, no conoce a nadie, no ha vivido en otro mundo. Un resultado sin sus límites obliga al
lector a adivinarlos, y lo adivinado tiende siempre a ser más generoso que lo medido. Un
resultado con sus límites dice exactamente qué se afirma, hasta dónde, y qué queda por ganar.
Por eso las dos mitades no se restan: se necesitan. Lo que este agente hace y lo que no hace,
juntos, son el trabajo.

---

## Figuras

**Figura 1 (GIF).** El cruce a territorio propio. El mismo agente que en las corridas de
control moría desangrado a treinta y ocho casillas de su casa, con la ruta inquebrantable
activa regresa malherido, la vida cayendo hasta veintidós, y en el tick 923 cruza a su
territorio propio, donde regenera al máximo. El matiz que la imagen fija: la cura sana al pisar
terreno propio, a unas veintiuna casillas del hub, no al tocar el hub. Cuadro a cuadro,
generado desde los datos de la corrida.

**Figura 2 (GIF).** El aterrizaje. Un portador equipado llega a una antena, entra y gasta su
munición, la conducta que el sistema no produjo hasta el compromiso de conquista.

**Figura 3 (GIF).** El que vaga lejos, en la corrida muda. Con el tablón apagado, el agente
que explora lejos de casa con solo sus ojos emprende la vuelta tarde: su alarma de retorno se
dispara en t2210, veintiún ticks antes de su muerte, a 42 celdas de casa, en territorio
rival, drenando en torno a 2 de vida por tick. Cerró 19 celdas y murió en t2231, a unas 23 de
casa, todavía fuera de su territorio: a mitad de camino, no en el umbral. La alarma sonó cuando
ya no quedaba vida que la alcanzara, la vida que el canal, encendido, salva. Idéntico en las
tres corridas mudas, que son deterministas.

*Los tres GIF acompañan a este documento como material anexo.*

## Agradecimientos y declaración de asistencia

Este trabajo se ha desarrollado con la asistencia de modelos de lenguaje de Anthropic (Claude),
usados como herramienta en tres frentes: la matemática y la programación del agente, la
ejecución y verificación de los experimentos, y la redacción de este texto. El método de la
sección 3 se aplicó también a esa colaboración: cada número citado procede de un fichero de
resultados y se verificó contra su fuente, y ninguna afirmación descansa en la memoria del
modelo. El diseño de G-EMV, las decisiones de este trabajo y la responsabilidad por todo lo
escrito son del autor.

## Referencias

[1] Enrico, M. (2026). *G-EMV: una arquitectura geométrica de orientación homeostática para
agentes.* Zenodo. DOI 10.5281/zenodo.21026795. (El motor: primera parte de esta serie.)

[2] Softmax. *Cogs vs Clips* (Coworld / CoGames), entorno multiagente del Alignment League
Benchmark. https://softmax.com, código: https://github.com/Metta-AI/coworld-cogs-vs-clips

[3] Dunbar, R. I. M. (1996). *Grooming, Gossip and the Evolution of Language.* Harvard
University Press.

[4] Keramati, M., & Gutkin, B. (2014). Homeostatic reinforcement learning for integrating
reward collection and physiological stability. *eLife*, 3:e04811. DOI 10.7554/eLife.04811.
(Antecedente: Keramati & Gutkin, NIPS 2011.)

[5] Cañamero, D. (1997). Modeling motivations and emotions as a basis for intelligent
behavior. *Proceedings of the First International Conference on Autonomous Agents*, ACM Press.

[6] Daw, N. D., Niv, Y., & Dayan, P. (2005). Uncertainty-based competition between prefrontal
and dorsolateral striatal systems for behavioral control. *Nature Neuroscience*, 8(12),
1704–1711. DOI 10.1038/nn1560.
