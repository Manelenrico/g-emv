# P6-20 · El veto con alerta y primer golpe, y la cuenta justa del abandono

*28-sep-2026. Coste cero: banco sobre las 40 vidas de A6 ya jugadas (P6-18) y
recuento sobre los 200 diarios del mundo del seis. Nada jugado: **el criterio
fijado por Manel no se cumple y, por la regla de parada, se entrega solo el
banco**; los 3 USD de tope quedan sin gastar. `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados
del cinco y los 32 del seis: 0 alterados al principio y al final. Lo nuevo, en
archivos aparte y declarado: `mide_veto_P6_20.py` → `P6_20_banco.json`;
`mide_acorralado_P6_20.py` → `P6_20_acorralado.json`. Ningún número de este
informe se escribió antes de calcularlo. Sin propuestas de diseño. Último paso
sobre el anillo; lo siguiente son los razonadores.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

El veto de Manel (V2: ver un arma pone alerta, solo el primer golpe suspende)
**quita todos los vetos por «ver el arma»** de la fase 5 de A6 (726 tics: los
672 del veto vital y 54 de «armado acercándose»), deja 204 rupturas de 930
(184 por un rival con la mano vacía a ≤ 2 y 20 por vida bajo 15), hace
desaparecer 80 episodios de desviación y **ahorra 190 puntos de fuego** en 47
planes; a cambio, el daño esperado por quedarse alerta es de 5 a 10 puntos, y
en las 40 vidas solo hubo **1 primer golpe con el plan vivo** (una lanza, 7,2
puntos). La segunda mitad del criterio se cumple de sobra. La primera **no**:
de los 72 planes caídos, con V2 habrían seguido 13 (18 %) y con V2 más la
cuenta justa 16-17 (22-24 %), lejos de la mitad. La razón está en la cuenta
justa misma: **24 de las 47 caídas por «vida real bajo la proyectada» no
tienen desviación alguna**: el cuerpo se quemó siguiendo el plan, en el tramo
de ir o parado en la casilla del borde (distancia 6,1 con radio 6), y la curva
proyectada no contaba ese fuego. V1 (daño menor desde que se ve el arma) y V3
(según la vida que queda) cuentan lo mismo que V2 en la fase 5, porque el
daño esperado dentro **nunca** supera el fuego de fuera (0 de 726 tics). Y el
caso «débil y acorralado» apenas existe: 19 casos en 200 vidas, 17 ya en el
fuego, 0 acaban en golpe, 14 mueren por el anillo.

---

## 1 · EL BANCO: QUÉ SE CUENTA Y CÓMO (`mide_veto_P6_20.py`)

Solo lectura de los 40 diarios de A6 (`P618_t1_A6_*`), de uno en uno. Los
diarios llevan los planes (`forma_aceptada`), los tics de compromiso6b
(`compromiso6`: sujeta / obedece / enfriamiento / rompe con causa / cumplida) y
las caídas (`forma_caida` con motivo). Los vetos alternativos se cuentan
**sobre lo grabado**: en cada tic en que el veto grabado rompió, qué habría
hecho cada veto. El cuerpo grabado actuó bajo V0, así que las consecuencias
(fuego ahorrado, golpes que se recibirían) son cotas, declaradas como tales.

Definiciones declaradas:

- **Plan vivo**: de `forma_aceptada` a `forma_caida` / `cumplida` / muerte /
  siguiente aviso. Ámbito «fase 5» (el de P6-18: planes nacidos entre el aviso
  5 y el 6 en vidas vivas en el aviso 5; **74 planes, 930 rupturas, 672 de
  veto vital, 47 + 25 = 72 caídas**: coincide con P6-18) y ámbito «todos»
  (121 planes aceptados, 70 caídas por vida real: coincide con P6-19).
- **Rivales**: vistos (`ve_agentes`) + contados (parte E2 del hermano a ≤ 50
  tics, regla de `oyente2.inyecta`). **Armado** = alcance del catálogo > 0; la
  mano vacía no cuenta (ampliación de Manel).
- **«Ver el arma»** = las rupturas grabadas «a) veto vital: armado a tiro» y
  «e) armado a menos de 6 y acercándose». Las otras dos no cambian con
  V1-V3: «e) rival a 2 o menos» solo salta cuando a) no saltó, y en las 40
  vidas **las 466 veces fue un rival con la mano vacía**; «d) vida bajo 15» es
  el suelo de la puerta.
- **Desviado** = desde un tic con `rompe` hasta que el cuerpo vuelve a estar
  dentro (a salvo): incluye el enfriamiento que sigue a la ruptura y el
  `obedece` de la vuelta (el fuego de la vuelta es consecuencia de la ruptura).
  **Siguiendo** = lo demás: sujeta, libre dentro, y el obedece/enfriamiento del
  tramo inicial de ir (el cuerpo anda hacia el círculo por el plan: es coste
  del plan). Episodio de desviación = racha de tics desviados; su causa, la
  del primer `rompe`.
- **Daño esperado dentro** = suma de la tabla arma × distancia de P6-19
  (`tabla_puerta6g`) sobre los rivales del tic, a la casilla del cuerpo.
  **Fuego de fuera** = dps de la fase / 24 (fase 5: 0,333 por tic).
- **V0** = lo grabado. **V1** = en un tic de «ver el arma», rompe solo si
  esperado > fuego. **V2** (Manel) = ver el arma no rompe; tras un golpe de
  rival con el plan vivo, suspensión de N = 96 tics en la que manda la tabla
  y sale solo si esperado > fuego. **V3** (ampliación) = V2 si la vida aguanta
  el primer golpe esperado del arma peor a tiro con margen: hp > golpe típico
  (P6-19) + MARGEN + 15 (suelo de la puerta); si no, actúa al ver (se aparta
  dentro, que no es ruptura) y sale solo si esperado > fuego.
- **N = 96**: el cierre de episodio de P6-9. Los datos no piden otro valor: en
  las 40 vidas hubo 89 primeros golpes (con o sin plan) y en 52 de ellos llegó
  otro golpe dentro de los 96 tics siguientes; solo 1 primer golpe con plan
  vivo y sujeto, así que no hay serie con la que afinar N.
- **MARGEN de V3**, sacado de los datos: mediana del daño de rival recibido en
  los 96 tics que siguen a un primer golpe en las 40 vidas de A6, con o sin
  plan (n 89): **3,0 puntos** (media 9,3; p75 11,0). Con el p75 el recuento no
  cambia (véase §2). Golpe típico por arma (P6-19): espada 13,2, arco 14,0,
  lanza 9,8, cuchillos 8,0, cerbatana 4,0, mano 3,85.
- **Un episodio desaparece** bajo Vk si su causa es «ver el arma» y Vk no rompe
  en su tic; **fuego ahorrado** = fuego del anillo recibido en esos episodios.
- **«Habría seguido»** (caídas por «vida real X bajo la proyectada Y menos
  10»): X + daño que Vk evita (fuego de los episodios que desaparecen antes de
  la caída) ≥ Y − 10. Las caídas «en la reevaluación (área)» no dependen del
  veto: se cuentan como «no cambia».

## 2 · LOS TRES VETOS (Y EL CUARTO) SOBRE LA FASE 5 DE A6

74 planes, 5.393 tics de plan vivo: sujeta 1.054 · obedece 644 · enfriamiento
1.831 · rompe 930 · libre 934. En los 726 tics de «ver el arma»: daño esperado
dentro medio 0,0066 por tic, máximo 0,119 (una lanza a 1), contra un fuego de
0,333: **en ningún tic el daño esperado dentro supera el fuego de fuera**. Por
eso V1, V2 y V3 rompen lo mismo: nada.

| | V0 (grabado) | V1 | V2 (Manel) | V3 |
|---|---|---|---|---|
| tics de «ver el arma» que rompen | 726 | 0 | 0 | 0 |
| rupturas restantes (de 930) | 930 | 204 | 204 | 204 |
| episodios de desviación que desaparecen (de 108) | 0 | 80 | 80 | 80 |
| fuego ahorrado (puntos) | 0 | 190,2 | 190,2 | 190,2 |
| golpes de rival en esos episodios (puntos) | — | 28,8 | 28,8 | 28,8 |
| daño esperado extra por quedarse alerta (Σ esp en los tics quitados / × tics del episodio) | — | 4,8 / 10,1 | 4,8 / 10,1 | 4,8 / 10,1 |
| tics en que «se aparta dentro» sin romper (débil) | — | — | — | 85 (p75: igual recuento de rupturas) |
| caídas por vida real que habrían seguido (de 47) | 0 | 13 | 13 | 13 |
| de los 72 planes caídos | 0 % | 18 % | 18 % | 18 % |

Los 108 episodios de desviación de la fase 5: causa e) 67, a) 38, d) 3;
2.029 tics, 223 puntos de fuego, 28,8 de rival; 54 salen del círculo; mediana
8,5 tics. Los 80 que desaparecen con V2 son todos los de causa «ver el arma»;
los 28,8 puntos de golpes de rival de esos episodios los recibió el cuerpo
**estando suelto** (V0 lo había soltado), no sujeto.

**Ámbito «todos»** (121 planes, fases 1-7): 1.357 tics de «ver el arma»; el
daño esperado supera el fuego en 11 (fases 1-4, con fuego de 0,04-0,08 y una
espada al lado); V1 deja 514 rupturas de 1.860, V2 y V3 503; 142 episodios
desaparecen; fuego ahorrado 259; caídas que habrían seguido 17 de 70 (V1
también 17).

### 2a · Los primeros golpes estando sujeto

En la fase 5 hubo **2 golpes de rival con el plan vivo** en 40 vidas, **1 con
el cuerpo dentro**: lanza, 7,2 puntos, vida 24 en el golpe, en un tic de
ruptura; en los 96 tics siguientes el cuerpo estuvo quieto 8 tics y se movió
4, salió del círculo a los 11 tics y murió. Las filas que pesaban:
F-DANO 0,90, R-CARENCIA 0,67, F-4-ALCANCE 0,50, S-DANO-PAREJA 0,50. Ese
cuerpo era «débil» para V3 (24 ≤ 9,8 + 3 + 15): V3 habría actuado al ver la
lanza, no al golpe; si eso le habría ahorrado el golpe, el banco no lo puede
decir (contrafactual de conducta).

Por qué tan pocos: P6-19 ya lo medía (los rivales pegan poco y de cerca) y V0
suelta al cuerpo en cuanto ve el arma, así que el rival casi nunca llega a
pegar a un cuerpo sujeto. Bajo V2 el cuerpo se quedaría; la cota de lo que
recibiría es la fila «daño esperado extra» de la tabla: **5-10 puntos** contra
190 de fuego ahorrado. **La segunda mitad del criterio se cumple.**

### 2b · V3: qué añade

V3 difiere de V2 solo en los tics en que el cuerpo es débil: 85 de los 726
(hp ≤ golpe típico + 3 + 15; con el p75 del margen, 11, el recuento de
rupturas es el mismo, porque en ningún tic el daño esperado supera el fuego).
En esos 85 tics V3 «se aparta dentro» en vez de esperar el golpe; **no rompe
ninguno**. Su ventaja sería no recibir el primer golpe estando débil, y el
banco solo ve 1 golpe así en 40 vidas: no hay con qué medirla.

## 3 · LA CUENTA JUSTA DEL ABANDONO

Las 47 caídas por «vida real X bajo la proyectada Y − 10» de la fase 5 (hueco
X − Y: media −15,9, mediana −13,0; 17 de ellas en el primer control, ≤ 26 tics
de plan). Daño recibido con el plan vivo hasta la caída, en puntos:

| | siguiendo el plan | desviado (tras una ruptura) |
|---|---|---|
| fuego del anillo | **216,5** | 203,4 |
| golpes de rival | 0,0 (ya estaba 0 · se acercó 0) | 28,8 (10,8 en lo que sería una suspensión) |

Clasificación de las 47:

| clase | n | hueco medio |
|---|---|---|
| la desviación explica la caída (seguiría con la cuenta justa) | **16** | −14,3 |
| **sin desviación alguna: fuego siguiendo el plan** (tramo de ir, o parado en el borde) | **24** | −15,7 |
| desviación, pero no basta (también fuego siguiendo) | 6 | −21,0 |
| sin desviación ni daño en el plan (el hueco venía de antes) | 1 | −17,0 |

Los 24 «sin desviación» son el hallazgo: el cuerpo se quema **cumpliendo el
plan**. 72 de los 74 planes se aceptan con el cuerpo fuera del círculo (55 en
enfriamiento, 8 obedeciendo, 9 en ruptura) y el tramo de ir se hace bajo el
fuego; y en la casilla del borde (distancia 6,1 con radio 6, o 6,0 con 5) el
cuerpo obedece «ir a (29,24)» tic tras tic sin moverse y se come golpes del
anillo de 6,56 puntos. La curva proyectada, calculada al nacer el plan, no
lleva ese fuego: el hueco de −13/−14 son exactamente dos golpes del anillo.
Esto es lo que P6-19 llamaba «el fuego que el cuerpo real se come», pero no
por no seguir el plan: **siguiéndolo**.

**Regla de abandono justa (decisión de método, declarada):** en el control, la
vida real se compara con la proyectada **sumando a la real el daño recibido en
los tics desviados** (fuego y golpes desde una ruptura hasta volver a estar a
salvo): el plan no responde de lo que pasó mientras el compromiso lo tenía
suelto. Los golpes de rival recibidos siguiendo el plan **sí** se cuentan
contra el plan (el plan prometió una vida quedándose ahí; el golpe es
información real contra quedarse); se da como variante descontar también los
golpes en suspensión (+1 caída). Y el fuego del tramo de ir y del borde se
cuenta contra el plan, porque es el plan el que lo manda.

Resultado: con la cuenta justa seguirían **16 de 47** (17 descontando los
golpes en suspensión; 15 descontando solo el fuego desviado); sobre los 72
planes caídos, **22-24 %**.

## 4 · EL CRITERIO, Y LA REGLA DE PARADA

| condición (fijada en el pedido) | medida | resultado |
|---|---|---|
| con V2 y la cuenta justa, al menos la mitad de los 72 planes caídos habrían seguido | 16-17 de 72 (22-24 %); sobre las 47 por vida real, 34-36 % | **falla** |
| el daño de los primeros golpes es menor que el fuego ahorrado | 7,2 recibidos (cota esperada 4,8-10,1) contra 190,2 | cumple |

**Falla la primera: se para y se entrega solo el banco.** No hay A7, ni
humo, ni sello, ni GIF, ni gasto. La ampliación («si pasa el criterio, el
campo se juega con V3») no llega a aplicarse.

Lo que el banco dice de por qué falla: el veto no es lo que tira los planes.
Con V2 los 80 episodios por «ver el arma» desaparecen y el fuego que
ahorran (190 puntos) rescata 13 caídas; las otras 34 se deben, en 24 casos, a
fuego recibido cumpliendo el plan (tramo de ir bajo el fuego, casilla del
borde) que la proyección no contaba, y en 6 a una mezcla. Es la misma
conclusión que P6-18 (llegar no es quedarse) y P6-19 (lo que promete de más
es el fuego), ahora con el reparto hecho.

## 5 · SOLO CONTAR: «DÉBIL Y ACORRALADO» (`mide_acorralado_P6_20.py`)

200 diarios (A3, A4, A5v, A5h, A6), 2,52 millones de tics vivos. Un **caso**
es una racha de tics (huecos ≤ 24 se funden) en la que el cuerpo está a la
vez: **débil** (hp ≤ 13,2, un golpe típico de espada lo mata; P6-19),
**sin escapatoria** (ninguna casilla alcanzable en ≤ 3 pasos por el mapa
estático que aleje al cuerpo del rival armado más cercano sin meterlo en el
fuego: distancia al centro ≤ radio del anillo en el tic; si ya está en el
fuego, que no lo aleje más del centro) y con un **rival con arma acercándose a
distancia de golpe** (arma del catálogo con alcance > 0, mano vacía excluida,
a distancia Chebyshev ≤ alcance y más cerca que la última vez que se le vio).

| | tics |
|---|---|
| vivos | 2.523.223 |
| débil (hp ≤ 13,2) | 17.320 |
| rival armado a tiro y acercándose | 28.903 |
| débil **y** rival armado a tiro | 372 |
| … de ellos con escapatoria | 346 |
| **débil y acorralado** | **26** |

**19 casos en 16 vidas** (A3 5, A4 3, A5v 7, A5h 4, A6 0); mediana 1 tic. En
16 la vida no aguantaba ni una lanza. **17 de los 19 estaban ya en el fuego**
cuando se dio el caso. El rival: arco 13, cerbatana 11, cuchillos 1, espada 1
(tics por arma): es un tirador viéndonos arder, no un cuerpo a cuerpo.
Desenlace: **0 acaban en golpe** de esos rivales (en el caso ni en los 96 tics
siguientes); **17 mueren en los 96 tics**, 14 por el anillo, 1 por rival, 2 sin
constar. Llevábamos arma en 17 (espada 9, cerbatana 3, lanza 3, cuchillos 1,
arco 1): el cuerpo estuvo quieto 22 tics de 24, pegó 1 tic (A4, con espada) y
se movió 1; con arma acabaron en golpe 0 y en muerte 15; sin arma, 0 y 2.

Lo que dice el recuento: el caso que la pregunta imagina (débil, sin salida,
un rival con arma encima) casi no ocurre en 200 vidas, y cuando ocurre es un
cuerpo que ya se está quemando fuera del círculo con un tirador a distancia;
muere del anillo, no del rival, y no pega aunque lleve arma.

## 6 · LO QUE DICE LA MEDIDA (sin proponer nada)

1. El veto vital rompe por arcos y cerbatanas a distancia que casi nunca pegan
   (P6-19); quitarlo (V1, V2 o V3, da igual: el daño esperado dentro nunca
   supera el fuego en la fase 5) ahorra 190 puntos de fuego en 47 planes y
   costaría 5-10 puntos esperados de golpes.
2. Pero los planes no caen por el veto: caen porque el cuerpo se quema
   siguiendo el plan (tramo de ir bajo el fuego, casilla del borde) y la curva
   proyectada no lleva ese fuego. Con la cuenta justa siguen 16-17 de 72.
3. La suspensión por primer golpe de V2 casi no se ejercería: 1 golpe a un
   cuerpo sujeto en 40 vidas.
4. «Débil y acorralado» es un caso de anillo, no de rival: 19 en 200 vidas,
   17 ardiendo, 0 golpes, 14 muertes por el fuego.

Este es el último paso sobre el anillo. Lo siguiente son los razonadores.

## 7 · ARCHIVOS

| archivo | qué es |
|---|---|
| `mide_veto_P6_20.py` → `P6_20_banco.json` | el banco (V0-V3, episodios, cuenta justa, primeros golpes, margen de V3; lista de planes y caídas) |
| `mide_acorralado_P6_20.py` → `P6_20_acorralado.json` | el recuento «débil y acorralado» (19 casos, con detalle) |
| `informe_P6_20.md` | este informe |

Nada jugado; ninguna imagen nueva; nada que subir a la liga.
