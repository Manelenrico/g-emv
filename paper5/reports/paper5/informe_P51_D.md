# P5-1 fase D — Las manos vacías

En seco, coste cero, solo lectura de los seis diarios de B1 y C. No se ha
jugado nada ni se ha tocado la plataforma.

**El titular.** La fase C dejó una pregunta abierta: por qué la carencia nunca
baja del suelo de la calma. La respuesta está en una sola cifra. El cuerpo pide
**tres** cosas en la mano —arma, botiquín y ración, `W_TARGET = 3.0`
(`appraisal_zs_v42_exp.py:126`)— y en **once vidas**, seis del mundo lento y
cinco de S-2, **no llegó a tres ni una sola vez**. El máximo de las once fue
**2,25**. Por eso `R-CARENCIA`, que es exactamente `(3 − W) / 3`
(`appraisal_zs_v42_exp.py:1076`), no puede bajar de 0,25, y la calma literal, que
pide 0,1, es **aritméticamente imposible** con lo que estas criaturas consiguen
llevar encima.

---

## D1 · Quién nos vio, quién nos pegó y quién nos mató

Desde el tic 481, el primero de vida.

| asiento-partida | primer armado a la vista | primer daño | quién lo hizo | muerte | quién la hizo |
|---|---|---|---|---|---|
| B1 / 10 | tic **533** · asiento 8, `ryanschiller-zero-sum-player-v1` (lanza) | tic **875** | asiento 13, `zero-sum-example` | tic 12.457 | **el anillo** (`source: zone`) |
| B1 / 11 | tic **622** · asiento 8, `ryanschiller-zero-sum-player-v1` (lanza) | tic **733** | asiento 8, `ryanschiller-zero-sum-player-v1` | tic 857 | asiento 13, `zero-sum-example` |
| C2 / 10 | tic **581** · asiento 6, `belobog` (espada) | tic **12.409** | **el anillo** | tic 13.921 | **el anillo** |
| C2 / 11 | tic **537** · asiento 13, `zero-sum-example` (lanza) | tic **8.758** | asiento 2, `relh-zero-sum` | tic 11.498 | **no consta** |
| C3 / 10 | tic **537** · asiento 12, `aaron-zs-fable` (cuchillos) | tic **791** | asiento 13, `zero-sum-example` | tic 935 | asiento 13, `zero-sum-example` |
| C3 / 11 | tic **548** · asiento 12, `aaron-zs-fable` (cuchillos) | tic **642** | asiento 13, `zero-sum-example` | tic 968 | **no consta** (el último registrado, del 13) |

**En los seis hay un rival armado a la vista antes del tic 622**, o sea antes de
los seis segundos de haber bajado del pedestal. No hay un momento en que la
arena esté tranquila: está armada desde el principio.

**El diario no guarda el golpe que mata.** El cuerpo deja de recibir
observaciones al morir, así que en dos de los seis la causa exacta no consta y
no la deduzco.

### Los golpes de los catorce rivales, hasta el tic 2.000

Sumando los seis asientos:

| política | golpes que nos dieron |
|---|---|
| **`zero-sum-example`** | **20** |
| `ryanschiller-zero-sum-player-v1` | 1 |
| todas las demás | **0** |
| **total** | **21** |

**Doce de los catorce rivales no nos tocaron ni una vez en los primeros dos mil
instantes.** Casi toda la violencia temprana viene de una sola política,
`zero-sum-example`, que además ocupa **el asiento 13 en las tres partidas**,
porque el asiento lo fija el roster y no la semilla. Hizo el primer daño a tres
de nuestros seis asientos y mató a uno con seguridad.

---

## D2 · Las manos

`W` es lo que el cuerpo lleva encima, medido contra lo que pide: arma, botiquín
y ración, `W_TARGET = 3.0`.

| asiento-partida | tics vivos | W mediana | W máxima | 1ª vez W ≥ 1 | ≥ 2 | ≥ 3 | % tics con W ≥ 3 | carencia mediana | objetos vistos en el suelo | veces que cogió |
|---|---|---|---|---|---|---|---|---|---|---|
| **B1 / 10** | 11.976 | 1,77 | 1,82 | 693 | — | **nunca** | **0,00** | 0,411 | 28 | 31 |
| **B1 / 11** | 376 | 1,65 | 1,67 | 560 | — | **nunca** | **0,00** | 0,450 | 18 | 2 |
| **C2 / 10** | 13.440 | 1,25 | **2,25** | 989 | 11.550 | **nunca** | **0,00** | 0,583 | 43 | 17 |
| **C2 / 11** | 11.017 | 0,67 | 0,67 | — | — | **nunca** | **0,00** | 0,778 | 33 | 23 |
| **C3 / 10** | 454 | 0,50 | 0,50 | — | — | **nunca** | **0,00** | 0,833 | 15 | 1 |
| **C3 / 11** | 487 | 0,50 | 1,50 | 626 | — | **nunca** | **0,00** | 0,833 | 19 | 2 |
| S2_A `051a3cdd` a10 | 275 | 1,00 | 2,00 | 276 | 478 | **nunca** | **0,00** | 0,667 | 18 | 3 |
| S2_A `051a3cdd` a11 | 5.280 | 2,00 | 2,00 | 287 | 397 | **nunca** | **0,00** | 0,333 | 28 | 3 |
| S2_A `16755035` a10 | 3.048 | 0,25 | 1,25 | 546 | — | **nunca** | **0,00** | 0,917 | 29 | 3 |
| S2_A `16755035` a11 | 2.955 | 0,00 | 1,25 | 331 | — | **nunca** | **0,00** | 1,000 | 21 | 6 |
| S2_A `1a8deabf` a10 | 214 | 0,00 | 1,00 | 430 | — | **nunca** | **0,00** | 1,000 | 17 | 1 |

**Ninguna de las once vidas llegó a tres.** Solo tres de las once pasaron de
dos, y la mejor de todas, C2/10, tocó 2,25 y lo hizo en el tic **11.550**, con
la partida ya casi acabada y el anillo encima.

**Y no fue por falta de cosas que ver.** Esas once criaturas vieron entre 15 y 43
objetos distintos en el suelo, y cogieron algo entre 1 y 31 veces. El mundo lento
además ayuda: **B1/10 cogió 31 veces** y aun así su W se quedó clavada en 1,8.

**Por qué no sube.** Tres razones, las tres del propio diario:

1. **Lo que se coge se gasta.** En C2/10 la vida cae a **1 punto en el tic
   13.009** y en el 13.062 vuelve a **51**: se curó. En ese mismo salto la W baja
   de **2,25 a 1,25**. Curarse cuesta un objeto, así que sobrevivir *sube* la
   carencia. Las dos cosas que el cuerpo quiere tiran en sentidos opuestos.
2. **La mano es una sola.** W cuenta por fracciones lo que se lleva en la mano,
   en el cuerpo y en la mochila de dos huecos; llenar los tres a la vez pide una
   secuencia de recogidas que nadie completó.
3. **W no es un contador de objetos**, es un peso: las subidas del diario van en
   escalones de 0,25 y 0,5, no de 1.

**El efecto sobre la carencia.** La mediana de `R-CARENCIA` en las seis vidas del
mundo lento va de **0,411 a 0,833**, y en las cinco de S-2 de **0,333 a 1,000**.
El suelo de la calma es **0,1**. Ninguna se acerca, y la mejor de las once,
S2_A `051a3cdd` a11 con W clavada en 2,0, se queda en **0,333**: tres veces por
encima del suelo.

**Esto cierra la pregunta de la fase C.** La calma literal no salió cero por el
anillo ni por la duración de la partida. Salió cero porque **para que salga otra
cosa haría falta que el cuerpo llegara a llevar 2,7 de 3**, y en once vidas el
récord es 2,25 durante unos pocos cientos de instantes.

---

## D3 · La película de cada vida

Seis figuras, una por asiento-partida, en `cantera/paper5/figD/`. PNG a 300 ppp,
17 cm de ancho. Cinco franjas y un eje de tiempo común, del tic 481 al último
que el cuerpo vio, con el aviso del anillo marcado donde llega:

| franja | qué lleva |
|---|---|
| 1 | **vida** (0 a 100) |
| 2 | **W**, con la raya de lo que el cuerpo pide, 3 |
| 3 | **carencia**, con el suelo de la calma, 0,1 |
| 4 | **las tres tensiones** del motor, F, R y S |
| 5 | **la d**: la del estado de ahora y la del futuro que elige |

| fichero | vida |
|---|---|
| `figD/P5_B1_a10.png` | 11.976 instantes |
| `figD/P5_B1_a11.png` | 376 |
| `figD/P5_C2_a10.png` | 13.440 |
| `figD/P5_C2_a11.png` | 11.017 |
| `figD/P5_C3_a10.png` | 454 |
| `figD/P5_C3_a11.png` | 487 |

**Dos avisos de método, declarados.**

1. **No hay «energía».** El encargo pedía seis números y uno de ellos era la
   energía. **ZERO-SUM no tiene energía**: la observación del mundo trae
   posición, vida, mano, cuerpo, mochila y efectos, y las cuatro
   características son inteligencia, atletismo, velocidad y fuerza. El eje R del
   motor, que en otros mundos come de la energía, aquí lo alimenta **W**. Así que
   la figura lleva cinco números y no seis, y no me invento el que falta.
2. **Las tensiones se reconstruyen del diario, y es exacto.** El diario no
   guarda las seis fuerzas, pero guarda de cada fila su M, su signo y su reparto
   ya hecho en los tres ejes. Sumarlas es literalmente lo que hace
   `appraisal_zs_v42_exp.py:1684-1698`. De ahí sale el `State`, y la `d` sale de
   `opponent_distance`, las dos **importadas de `motor/model.py`**, sin copiar
   ni una constante a mano. El único límite es el redondeo del diario a cinco
   decimales.

**Lo que se ve en la de C2/10, que es la vida larga y limpia.** La vida se
mantiene en 100 durante **doce mil instantes**; la W sube a 1,25 en el tic 989 y
se queda ahí ocho mil instantes sin moverse; las tres tensiones están planas y
bajas hasta el tic 8.100, con la R —la carencia— siendo la única que tira; y la d
está clavada. Luego, a partir del 8.800, todo se mueve a la vez. Es la película
de una criatura a la que **no le pasa nada durante siete minutos y aun así nunca
está en calma**, porque le faltan dos tercios de lo que quiere llevar encima.

---

## Lo que esta fase deja dicho

1. **La calma no la impide el anillo: la impide la mano vacía.** Con
   `R-CARENCIA = (3 − W) / 3` y una W que en once vidas no pasa de 2,25, el suelo
   de 0,1 queda fuera de alcance por construcción.
2. **Curarse sube la carencia.** El botiquín que salva la vida es el mismo objeto
   que el cuerpo contaba como «lo que llevo». Está medido en C2/10, tic 13.062.
3. **La violencia temprana es de una sola política.** Veinte de los veintiún
   golpes de los primeros dos mil instantes son de `zero-sum-example`, y doce de
   los catorce rivales no nos tocaron.
4. **Una palanca posible, y no está en la configuración del mundo.** Si se
   quisiera calma habría que tocar `W_TARGET`, que es de la tabla y es nuestro, o
   que el mapa diera de partida lo que el cuerpo pide. Lo primero cambia la
   criatura; lo segundo no tiene campo en el manifiesto, como quedó dicho en la
   fase A.

**No se ha jugado nada.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1

$ md5 cantera/paper5/analiza_D.py cantera/paper5/fig_D3.py
MD5 (cantera/paper5/analiza_D.py) = 51c8843a44efa16e21a0304c06d15bbf
MD5 (cantera/paper5/fig_D3.py) = 279b15ee9e55644c2a6e339699587a96
```

Ficheros: `cantera/paper5/analiza_D.py`, `fig_D3.py`, `D_medidas.json`,
`D_series.json` y las seis figuras de `cantera/paper5/figD/`.
