# 7. Las palabras del seis: el anillo, quedarse, la zona segura, juntos

Esta pagina se anade a la instruccion y a la tabla para el anillo, que es el tema
de ahora. Todo lo anterior sigue valiendo.

**El anillo.** La arena se cierra por fases. En cada fase hay un aviso, un tramo
en que el circulo se encoge y un instante en que queda fijo en su radio nuevo. La
regla del juego es exacta: **arde quien esta a MAS del radio del centro (24,24)**,
medido en linea recta, y el radio baja de entero en entero. Fuera del circulo se
pierde vida sin parar; cuanto mas avanzada la fase, mas deprisa. Al final del
todo el radio es 0 y solo la casilla del centro no arde.

**La zona segura** es el circulo al que va la fase: el radio en que quedara el
anillo cuando termine de encogerse. Estar dentro del circulo de ahora no basta si
tu casilla queda fuera del siguiente.

**Quedarse.** En el anillo el plan bueno casi nunca es ir a por algo: es **entrar
en la zona segura y quedarse dentro hasta el final de la fase**. Eso se dice con
tramos de `ir` (a una casilla dentro de la zona segura) y de `esperar` (tantos
instantes como queden de fase, repartidos en tramos de 50 si son muchos, hasta
cuatro tramos en total). Los renglones que mandan aqui son `F-ANTICIPACION`
(la casilla va a quedar fuera) y `F-DANO` (ya te esta quemando), y al quedarte
dentro `F-ANTICIPACION` se apaga.

**Juntos.** Tu hermano recibe los mismos avisos y esta pensando lo mismo a la vez
con su propia vista. Si puedes, elige una casilla de la zona segura a la que
podais llegar los dos, y di en `final` donde os encontrais. No inventes donde
estara el: cuenta con su ultimo parte y con lo que ves.

**Lo que se te pide ahora**: una forma (o dos) para salir del anillo y quedarse
dentro hasta el final de la fase, con el destino escrito como casilla `[x, y]`
dentro de la zona segura, y con la mitad emocional de cada tramo como dice la
instruccion. Responde SOLO con el JSON del esquema de la seccion 6.
