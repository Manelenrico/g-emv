# P7-15 · Dónde pierde el puesto el que recuerda

*5-oct-2026. Todo lo de este paso es POSTERIOR A LOS DOS SELLOS (P7-10 y P7-14b) y se declara así: lecturas de los 640 diarios de los dos campos y un
banco de réplica, con medidas elegidas después de ver los resultados. Coste: **créditos de la plataforma 0 USD; consola de Anthropic 0 USD.**
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar. El banco (`banco_P7_15.py`) replica las 80 vidas de
APRENDE de P7-14b, una vida por proceso, y reproduce la decisión del campo en 992.172 de 992.172 tics.*

## Lo que sale, en corto

1. **El puesto se pierde en unas pocas muertes tempranas.** En los dos campos, 10 de las 80 vidas de APRENDE mueren antes del tic 11.000; de BORRADO,
   3 y 4. Casi todas son por rival y acaban entre los puestos 12 y 16. Quitando los pares en que alguno de los dos muere pronto, la diferencia
   de puesto baja de 1,25 a 0,55 (se 0,48) en P7-10 y de 1,23 a 0,44 (se 0,49) en P7-14b: dentro del ruido.
   Un matiz que importa: en P7-14b, ESPERANZA y TECHO mueren pronto casi tanto como APRENDE (11 y 8); ahí el brazo distinto es BORRADO, que muere poco al principio.
2. **Nada de cómo vive los separa**: ni el tiempo con poca vida, ni el círculo, ni las peleas, ni el zurrón, ni lo que anda superan el ruido entre semillas en los dos campos.
3. **El cuaderno cambia la decisión en el 5,4 % de los tics.** El cambio que más tics ocupa: con el cuaderno se queda quieto donde, sin los
   recuerdos de días anteriores, usaría el botiquín (34.650 tics en 49 de 80 vidas, con la vida en 76 de mediana). **El que recuerda espera más para curarse.**
4. **Las dos cosas se tocan**: en 8 de las 10 muertes tempranas de APRENDE en P7-14b, en sus últimos 20 segundos hubo tics en que con el cuaderno se quedó
   quieto y sin él habría usado el botiquín. Es una coincidencia medida, no una prueba de causa: el banco no dice qué habría pasado después.
5. **El regalo que nadie coge**: quien pide lleva el zurrón lleno. No puede coger el botiquín y hacer sitio no gana.

## Sección 1 · Cuándo y cómo muere

Emparejado por semilla: en cada semilla, la media de las 4 vidas de un brazo (2 series × 2 asientos) menos la del otro; d̄ es la media sobre las 20
semillas de cada campo (o las 40 de los dos) y se su error típico. «¿En los dos?» = |d̄/se| > 2 en cada campo por separado y con el mismo signo: la prueba más dura.
Hay 23 medidas en esta sección y la siguiente: con tantas, alguna pasaría de 2 por azar en un campo; por eso se pide en los dos.

**APRENDE frente a BORRADO:**

| medida (por vida) | P7-10: APRENDE | BORRADO | d̄ | d̄/se | P7-14b: APRENDE | BORRADO | d̄ | d̄/se | los dos campos: d̄ | d̄/se | ¿en los dos? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| puesto | 5,91 | 4,66 | 1,25 | 2,2 | 5,59 | 4,36 | 1,23 | 2,2 | 1,24 | **3,1** | **sí** |
| vida al morir | 6,42 | 11,49 | -5,06 | -3,1 | 8,69 | 11,31 | -2,62 | -1,0 | -3,84 | **-2,5** | no |
| último tic vivo | 12.949 | 13.628 | -679 | -1,8 | 12.882 | 13.540 | -658 | -1,8 | -669 | **-2,5** | no |
| fase del anillo al morir (0 a 7) | 5,34 | 5,97 | -0,64 | -2,2 | 5,55 | 5,90 | -0,35 | -1,3 | -0,49 | **-2,6** | no |
| muere antes del tic 10.000 (0/1) | 0,09 | 0,03 | 0,06 | 1,6 | 0,09 | 0,04 | 0,05 | 1,7 | 0,06 | **2,3** | no |
| muere antes del tic 11.000 (0/1) | 0,12 | 0,04 | 0,09 | 2,1 | 0,12 | 0,05 | 0,07 | 2,0 | 0,08 | **3,0** | **sí** |
| muere antes del tic 12.000 (0/1) | 0,24 | 0,11 | 0,12 | 2,1 | 0,20 | 0,09 | 0,11 | 2,1 | 0,12 | **3,0** | **sí** |
| muere por rival (0/1) | 0,35 | 0,28 | 0,07 | 1,6 | 0,24 | 0,15 | 0,09 | 1,6 | 0,08 | **2,2** | no |
| muere por el anillo (0/1) | 0,45 | 0,40 | 0,05 | 0,6 | 0,49 | 0,46 | 0,03 | 0,3 | 0,04 | 0,6 | no |
| sobrevive al final (0/1) | 0,20 | 0,33 | -0,12 | -1,7 | 0,28 | 0,39 | -0,11 | -1,3 | -0,12 | **-2,1** | no |
| muere por rival yendo a por un botiquín (0/1) | 0,16 | 0,09 | 0,07 | 2,0 | 0,09 | 0,07 | 0,01 | 0,3 | 0,04 | 1,4 | no |
| muere por rival habiendo abierto el canal en sus últimos 10 s (0/1) | 0,11 | 0,05 | 0,06 | 1,4 | 0,09 | 0,04 | 0,05 | 1,3 | 0,06 | 1,9 | no |

**TECHO frente a BORRADO** (referencia):

| medida (por vida) | P7-10: TECHO | BORRADO | d̄ | d̄/se | P7-14b: TECHO | BORRADO | d̄ | d̄/se | los dos campos: d̄ | d̄/se | ¿en los dos? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| puesto | 4,36 | 4,66 | -0,30 | -0,5 | 4,89 | 4,36 | 0,53 | 0,7 | 0,11 | 0,2 | no |
| vida al morir | 10,99 | 11,49 | -0,50 | -0,3 | 9,81 | 11,31 | -1,50 | -0,6 | -1,00 | -0,7 | no |
| último tic vivo | 13.726 | 13.628 | 97 | 0,3 | 13.200 | 13.540 | -340 | -0,6 | -121 | -0,3 | no |
| fase del anillo al morir (0 a 7) | 5,96 | 5,97 | -0,01 | -0,0 | 5,66 | 5,90 | -0,24 | -0,6 | -0,12 | -0,5 | no |
| muere antes del tic 10.000 (0/1) | 0,04 | 0,03 | 0,01 | 0,4 | 0,05 | 0,04 | 0,01 | 0,3 | 0,01 | 0,4 | no |
| muere antes del tic 11.000 (0/1) | 0,06 | 0,04 | 0,03 | 0,7 | 0,10 | 0,05 | 0,05 | 0,8 | 0,04 | 1,1 | no |
| muere antes del tic 12.000 (0/1) | 0,07 | 0,11 | -0,04 | -0,7 | 0,12 | 0,09 | 0,04 | 0,6 | 0,00 | 0,0 | no |
| muere por rival (0/1) | 0,16 | 0,28 | -0,11 | -1,6 | 0,26 | 0,15 | 0,11 | 2,0 | 0,00 | 0,0 | no |
| muere por el anillo (0/1) | 0,53 | 0,40 | 0,12 | 1,7 | 0,44 | 0,46 | -0,03 | -0,3 | 0,05 | 0,9 | no |
| sobrevive al final (0/1) | 0,31 | 0,33 | -0,01 | -0,2 | 0,30 | 0,39 | -0,09 | -1,0 | -0,05 | -0,8 | no |
| muere por rival yendo a por un botiquín (0/1) | 0,01 | 0,09 | -0,07 | -2,9 | 0,01 | 0,07 | -0,06 | -2,5 | -0,07 | **-3,8** | **sí** |
| muere por rival habiendo abierto el canal en sus últimos 10 s (0/1) | 0,06 | 0,05 | 0,01 | 0,4 | 0,09 | 0,04 | 0,05 | 1,0 | 0,03 | 1,1 | no |

Lo único que pasa la prueba dura en APRENDE frente a BORRADO: puesto, muere antes del tic 11.000 (0/1), muere antes del tic 12.000 (0/1). En TECHO frente a BORRADO: muere por rival yendo a por un botiquín (0/1).

**Las muertes tempranas** (el corte en el tic 11.000 lo he puesto después de ver los datos, por la curva de vivos; con 10.000 y 12.000 está en la tabla de arriba).
Vivos en cada momento, de 80:

| | tic 8.000 | 10.000 | 11.000 | 12.000 | 13.000 | 14.000 |
|---|---:|---:|---:|---:|---:|---:|
| P7-10, BORRADO | 78 | 78 | 77 | 71 | 56 | 51 |
| P7-10, APRENDE | 76 | 73 | 70 | 61 | 45 | 36 |
| P7-10, TECHO | 79 | 77 | 75 | 74 | 53 | 47 |
| P7-14b, BORRADO | 78 | 77 | 76 | 73 | 52 | 44 |
| P7-14b, APRENDE | 75 | 73 | 70 | 64 | 50 | 45 |
| P7-14b, TECHO | 76 | 76 | 72 | 70 | 51 | 39 |

| | P7-10: APRENDE | BORRADO | TECHO | P7-14b: APRENDE | BORRADO | TECHO |
|---|---:|---:|---:|---:|---:|---:|
| mueren antes del tic 11.000 | 10 | 3 | 5 | 10 | 4 | 8 |
| … por rival | 10 | 3 | 4 | 8 | 4 | 8 |
| … en los puestos 12 a 16 | 10 | 3 | 4 | 10 | 4 | 6 |
| … con algún botiquín a bordo al morir | 4 | 0 | 2 | 8 | 2 | 4 |
| … habiendo abierto el canal en sus últimos 10 s | 4 | 0 | 2 | 8 | 2 | 3 |
| … lo que más hacía: ir a por un botiquín | 4 | 2 | 0 | 2 | 2 | 0 |
| … lo que más hacía: moverse paso a paso | 3 | 1 | 2 | 4 | 2 | 8 |
| puesto medio de todas las vidas | 5,91 | 4,66 | 4,36 | 5,59 | 4,36 | 4,89 |
| puesto medio sin las que mueren pronto | 4,70 | 4,26 | 3,75 | 4,33 | 3,82 | 3,94 |

- APRENDE: 10 y 10 muertes tempranas; BORRADO: 3 y 4. Juntando los dos campos, 20 de 160 contra 7 de 160 (exacta de Fisher, una cola: p = 0,007).
  Por semillas, la diferencia en «muere antes del tic 11.000» pasa de 2·se en los dos campos por separado, por poco (tabla de arriba), y con el corte en 12.000 también; con el corte en 10.000, no. Son pocos casos.
- **El puesto, sin esos pares.** APRENDE − BORRADO en puesto, pares por (serie, día, asiento): P7-10, todos los pares 1,25 (se 0,61); los 67 pares en que
  ninguno muere pronto, 0,55 (se 0,48). P7-14b: 1,23 (se 0,53) y, en 70 pares, 0,44 (se 0,49). Más de la mitad de la diferencia de puesto está en las muertes tempranas.
- Morir pronto cuesta muchos puestos de golpe (quien muere antes del tic 11.000 queda casi siempre del 12 al 16), así que 6 o 7 muertes tempranas de más en 80 vidas mueven la media más de medio puesto.
- TECHO tiene 5 y 8: en P7-14b, tantas como para no poder decir que sea cosa solo de APRENDE. ESPERANZA en P7-14b tiene 11 (su SUELO en P7-10, 4).
  En P7-14b el brazo que se separa de los demás por abajo es BORRADO, que muere poco al principio.

## Sección 2 · Cómo vive

| medida (por vida) | P7-10: APRENDE | BORRADO | d̄ | d̄/se | P7-14b: APRENDE | BORRADO | d̄ | d̄/se | los dos campos: d̄ | d̄/se | ¿en los dos? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| parte de la vida con menos de 50 de vida | 0,028 | 0,048 | -0,020 | -1,4 | 0,039 | 0,031 | 0,008 | 0,5 | -0,006 | -0,6 | no |
| … con menos de 30 | 0,015 | 0,028 | -0,013 | -1,1 | 0,014 | 0,015 | -0,001 | -0,3 | -0,007 | -1,2 | no |
| parte de la vida fuera del círculo | 0,016 | 0,016 | -0,000 | -0,1 | 0,017 | 0,018 | -0,001 | -0,5 | -0,001 | -0,5 | no |
| parte de la vida con un rival a una o dos casillas | 0,112 | 0,131 | -0,018 | -1,2 | 0,118 | 0,134 | -0,016 | -1,1 | -0,017 | -1,6 | no |
| parte de la vida con algún botiquín | 0,561 | 0,532 | 0,029 | 0,6 | 0,617 | 0,593 | 0,024 | 0,4 | 0,026 | 0,7 | no |
| botiquines a bordo, media | 0,640 | 0,645 | -0,005 | -0,1 | 0,705 | 0,729 | -0,023 | -0,4 | -0,014 | -0,3 | no |
| … con alguna ración | 0,355 | 0,380 | -0,025 | -0,6 | 0,400 | 0,349 | 0,051 | 1,2 | 0,013 | 0,5 | no |
| … con un arma (mano o zurrón) | 0,536 | 0,578 | -0,042 | -0,7 | 0,633 | 0,651 | -0,018 | -0,3 | -0,030 | -0,7 | no |
| … con munición | 0,193 | 0,201 | -0,008 | -0,2 | 0,175 | 0,215 | -0,040 | -0,8 | -0,024 | -0,7 | no |
| … con el zurrón lleno | 0,465 | 0,556 | -0,091 | -1,5 | 0,564 | 0,511 | 0,053 | 1,4 | -0,019 | -0,5 | no |
| casillas recorridas por 1.000 tics | 73,5 | 74,8 | -1,3 | -0,4 | 75,4 | 69,4 | 6,0 | 1,8 | 2,3 | 0,9 | no |

**TECHO frente a BORRADO:**

| medida (por vida) | P7-10: TECHO | BORRADO | d̄ | d̄/se | P7-14b: TECHO | BORRADO | d̄ | d̄/se | los dos campos: d̄ | d̄/se | ¿en los dos? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| parte de la vida con menos de 50 de vida | 0,029 | 0,048 | -0,019 | -0,9 | 0,022 | 0,031 | -0,009 | -0,8 | -0,014 | -1,2 | no |
| … con menos de 30 | 0,009 | 0,028 | -0,019 | -1,3 | 0,011 | 0,015 | -0,004 | -1,1 | -0,012 | -1,6 | no |
| parte de la vida fuera del círculo | 0,016 | 0,016 | -0,000 | -0,1 | 0,017 | 0,018 | -0,001 | -0,6 | -0,001 | -0,5 | no |
| parte de la vida con un rival a una o dos casillas | 0,131 | 0,131 | 0,001 | 0,0 | 0,116 | 0,134 | -0,019 | -1,2 | -0,009 | -0,7 | no |
| parte de la vida con algún botiquín | 0,522 | 0,532 | -0,011 | -0,2 | 0,556 | 0,593 | -0,037 | -0,6 | -0,024 | -0,5 | no |
| botiquines a bordo, media | 0,552 | 0,645 | -0,092 | -1,2 | 0,642 | 0,729 | -0,087 | -1,0 | -0,090 | -1,6 | no |
| … con alguna ración | 0,295 | 0,380 | -0,085 | -1,6 | 0,322 | 0,349 | -0,027 | -0,6 | -0,056 | -1,6 | no |
| … con un arma (mano o zurrón) | 0,609 | 0,578 | 0,032 | 0,6 | 0,633 | 0,651 | -0,019 | -0,2 | 0,007 | 0,1 | no |
| … con munición | 0,283 | 0,201 | 0,082 | 1,5 | 0,183 | 0,215 | -0,032 | -0,8 | 0,025 | 0,7 | no |
| … con el zurrón lleno | 0,559 | 0,556 | 0,003 | 0,1 | 0,533 | 0,511 | 0,022 | 0,4 | 0,013 | 0,3 | no |
| casillas recorridas por 1.000 tics | 73,0 | 74,8 | -1,8 | -0,5 | 68,1 | 69,4 | -1,3 | -0,3 | -1,5 | -0,6 | no |

**Ninguna de las 11 medidas separa a APRENDE de BORRADO en los dos campos** (ninguna pasa la prueba dura). APRENDE no pasa más tiempo con poca vida, no está más fuera
del círculo, no pelea más, no lleva otro zurrón (los mismos botiquines, raciones, armas y munición, dentro del ruido) y no anda más.

## Sección 3 · Qué decisiones cambia el cuaderno

`banco_P7_15.py` → `P7_15_decisiones.json`. Las 80 vidas de APRENDE de P7-14b, tal como se jugaron. En cada tic el cuerpo decide dos veces sobre la
misma escena y la misma memoria de la partida: con su cuaderno, y con el cuaderno que tendría BORRADO ese día (vacío al empezar: solo los recuerdos
de hoy). Se cuenta cada tic en que las dos decisiones difieren y, aparte, los EPISODIOS: el primer tic de cada racha de tics seguidos distintos
(huecos de hasta 12 tics, medio segundo). El banco describe ese tic; no dice qué habría pasado después.

992.172 tics comparados; la decisión cambia en **53.500 (5,4 %)**, en 3.720 episodios (46,5 por vida). En esos tics las ganas del botiquín valen k = 0,91 con el
cuaderno y 0,30 solo con lo de hoy.

| con el cuaderno elige | solo con lo de hoy elegiría | episodios | tics |
|---|---|---:|---:|
| quedarse quieto | usar el botiquín | 74 | 34.650 |
| quedarse quieto | hacer sitio | 49 | 9.671 |
| moverse | ir a por un objeto | 601 | 2.615 |
| ir a por un objeto | moverse | 750 | 858 |
| ir a un sitio (hermano, centro o botín) | ir a por un objeto | 372 | 659 |
| ir a por un objeto | ir a un sitio (hermano, centro o botín) | 534 | 587 |
| ir a por un objeto | ir por curiosidad | 459 | 482 |
| quedarse quieto | ir por curiosidad | 40 | 457 |
| ir por curiosidad | quedarse quieto | 79 | 448 |
| ir por curiosidad | ir a por un objeto | 206 | 235 |
| ir por curiosidad | coger | 14 | 221 |
| moverse | moverse | 123 | 203 |
| quedarse quieto | ir a por un objeto | 10 | 140 |
| atacar | usar el botiquín | 9 | 138 |

(Las 14 parejas con más tics; hay 34.) Por tipo de candidato, episodios en que lo elige con el cuaderno / solo con lo de hoy: ir a por un objeto 1817 / 1189; ir por curiosidad 326 / 513; moverse 791 / 920; ir a un sitio (hermano, centro o botín) 542 / 730; quedarse quieto 180 / 207; usar el botiquín 3 / 92; hacer sitio 1 / 49; regalar 39 / 0; coger 0 / 14; atacar 9 / 4.

Lo que se lee:
- **Esperar en vez de curarse.** `noop` con el cuaderno, `usar_botiquin` solo con lo de hoy: 74 episodios pero 34.650 tics (dos tercios de todos los tics distintos), en
  49 de las 80 vidas. La vida en esos tics: mediana 76, el 80 % entre 62 y 89. Con las ganas a 0,3 (esperanza) el botiquín se gasta
  como una ración, en cuanto falta algo; con las ganas aprendidas (0,96 de mediana) gastarlo cuesta más y el cuerpo aguanta herido sin usarlo. Al revés (usar con el cuaderno y no sin él): 3 episodios.
- **Ir a por objetos en vez de moverse o curiosear.** Con el cuaderno elige `ir_objeto` en 1817 episodios en que sin él haría otra cosa (moverse, ir por curiosidad, al centro o al
  botín); al revés, 1189. Son muchos episodios y pocos tics: decisiones sueltas de hacia dónde dar el paso. El diario no dice a por qué objeto iba.
- **No hacer sitio.** Con un botiquín a bordo y una ración en la casilla: con el cuaderno se queda como está; solo con lo de hoy cambiaría el botiquín por la ración (49 episodios, 9.671 tics, todos `hacer_sitio_first_aid_por_rations`).
- **Regalar.** 39 regalos que con solo lo de hoy no haría (la creencia de quien regala es la que deja pasar el regalo).

Por días (parte de los tics con la decisión distinta; episodios por vida):

| día | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tics distintos | 0,0 % | 1,1 % | 0,7 % | 0,6 % | 1,7 % | 1,8 % | 0,9 % | 1,5 % | 3,4 % | 2,4 % | 12,4 % | 5,3 % | 2,6 % | 5,4 % | 4,7 % | 35,3 % | 3,9 % | 12,6 % | 6,1 % | 5,5 % |
| episodios por vida | 0 | 46 | 57 | 46 | 30 | 25 | 32 | 33 | 12 | 26 | 145 | 44 | 88 | 42 | 40 | 90 | 17 | 52 | 59 | 46 |

El día 1 no hay ninguna (el cuaderno está vacío: las dos decisiones son la misma, como debe). Los días con muchos tics distintos son los de las
rachas largas de «esperar en vez de curarse».

**Las muertes tempranas de APRENDE en P7-14b, en sus últimos 20 segundos** (480 tics):

| vida | muere en el tic | puesto | causa | tics con la decisión distinta | de ellos, «quieto» con el cuaderno y «usar el botiquín» sin él |
|---|---:|---:|---|---:|---:|
| serie 1, día 12, asiento 10 | 887 | 16 | rival | 18 de 407 | 17 |
| serie 1, día 12, asiento 11 | 1.020 | 15 | rival | 6 de 480 | 0 |
| serie 2, día 9, asiento 11 | 1.038 | 16 | rival | 149 de 480 | 138 |
| serie 2, día 9, asiento 10 | 1.146 | 15 | rival | 9 de 480 | 0 |
| serie 1, día 18, asiento 10 | 5.325 | 16 | rival | 36 de 480 | 36 |
| serie 2, día 4, asiento 10 | 8.331 | 15 | rival | 36 de 480 | 18 |
| serie 1, día 18, asiento 11 | 8.421 | 14 | rival | 432 de 480 | 420 |
| serie 2, día 4, asiento 11 | 10.442 | 12 | rival | 23 de 480 | 18 |
| serie 1, día 20, asiento 10 | 10.824 | 12 | anillo | 424 de 480 | 415 |
| serie 1, día 20, asiento 11 | 10.824 | 13 | anillo | 67 de 480 | 66 |

En 8 de las 10, en sus últimos 20 segundos el que recuerda se quedó quieto con el botiquín en el zurrón en tics en que, con solo lo de hoy, lo habría usado.
En las otras 48 vidas de APRENDE que mueren (después del tic 11.000), eso pasa en 12. **Es una coincidencia medida y no una prueba**: no sé si usarlo las habría salvado
(en varias el canal se abrió igualmente al final), y BORRADO no se ha replicado al revés.

**Lo que va en contra de leerlo como causa.** ESPERANZA es el brazo que menos espera (ganas a 0,3 siempre, usa el botiquín como una ración) y en P7-14b tiene 11 muertes
tempranas, una más que APRENDE; en P7-10 su SUELO tuvo 4. Si esperar para curarse fuera lo que mata pronto, ESPERANZA debería morir pronto menos que nadie, y en P7-14b no es así.
Lo que se sostiene en los dos campos es más estrecho: APRENDE muere pronto más que BORRADO. Por qué BORRADO muere pronto menos que los otros tres brazos en P7-14b no lo explica nada de lo medido aquí.

## Sección 4 · Las tres sospechas de la mesa

| sospecha | lo medido | veredicto |
|---|---|---|
| (a) espera más para curarse y pasa más tiempo con poca vida | **Espera más: sí**, en la decisión (34.650 tics en 49 de 80 vidas en que con el cuaderno no usa el botiquín y sin él lo usaría; y en el campo usa con menos vida: 73 contra 86 en los días 11 a 20 de P7-14b). **Más tiempo con poca vida: no**: la parte de la vida por debajo de 50 y de 30 no se distingue de la de BORRADO en ningún campo | **la mitad se sostiene**: espera más, pero eso no se ve como más tiempo con poca vida; se ve, si acaso, en las muertes tempranas |
| (b) lleva botiquines en lugar de otras cosas | botiquines, raciones, armas y munición a bordo, y zurrón lleno: ninguna diferencia que pase de 2·se en los dos campos | **no se sostiene** |
| (c) la curiosidad de BORRADO le lleva a algo que le da ventaja | BORRADO y APRENDE van a por botiquines una parte parecida de la vida y llevan lo mismo; en el banco, sin los días anteriores iría más por curiosidad (513 episodios contra 326) y menos a por objetos, pero son pasos sueltos, y lo que lleva y lo que anda no cambia | **no se sostiene** con lo medido |
| otra, que aparece | **las muertes tempranas**: 10 y 10 de APRENDE contra 3 y 4 de BORRADO, que llevan más de la mitad de la diferencia de puesto, y que en P7-14b coinciden con tics de «esperar en vez de curarse»; pero ESPERANZA, que no espera, muere pronto tanto como APRENDE en P7-14b | **es donde está el puesto**; el porqué no está resuelto |

## Sección 5 · El regalo que nadie coge

Los 48 regalos de APRENDE en P7-14b que vuelve a coger quien los dio (`P7_15_regalo.json`). En 44 el hermano que pedía estuvo encima o al lado del botiquín regalado
durante la espera: 844 tics encima (en 12 regalos) y 10.046 al lado.

| el que pedía | encima del botiquín (844 tics) | al lado (10.046 tics) |
|---|---:|---:|
| botiquines a bordo | 0 en todos | 0 en todos |
| zurrón lleno | 844 | 7.091 |
| el candidato `coger` existe | 0 | 0 |
| `coger` escondido ese tic por el arreglo del seis («la mochila no cambia») | 844 | 329 |
| el candidato de hacer sitio existe | 844 | 329 |
| un candidato de ir a por él (`ir_objeto` o `ir_curioso`) existe | 0 | 587 |
| lo que elige | `noop` 743, `move_N` 35, `paso_SW` 20 | `noop` 6.618, `move_NE` 2.589, `ir_curioso` 150 |

Lo que lleva cuando está encima: net y rations (501 tics); bow y rations (243 tics); rations y spear (67 tics); arrows y rations (33 tics).

**Por qué no gana coger, con archivo y línea:**
1. **El zurrón tiene dos ranuras y están llenas** (una ración y un arma, red o munición) en los 844 tics en que está encima.
2. **`coger` no llega a ser candidato.** El cuerpo lo propone si hay un objeto en la casilla (`decisor_zs.py:475-483`), pero el arreglo del seis lo esconde cuando la previsión dice que el
   zurrón no cambiaría (`arreglos_P6_8b.py:85` y `:135-140`, registro `llena8` «prevision: la mochila no cambia»): 844 de 844 tics.
3. **Hacer sitio existe y no gana.** `hacer_sitio_rations_por_first_aid` está entre los candidatos en los 844 tics (`descubre_P7.py:307-322`), y su d frente a la de `noop`:
   igual en 310 tics (empate: desde P7-14b, en un empate no se suelta nada) y peor en 534 (mediana de la diferencia 0,274); mejor, en 0.
   Cambiar la ración por el botiquín no le compensa.
4. **Al lado, casi nunca hay candidato de ir a por él** (587 de 10.046 tics): con el zurrón lleno la promesa del botiquín calla («zurrón lleno: no es adquirible», `decisor_zs.py:647-650`) y
   `ir_curioso` solo se crea si el botiquín cabe (`descubre_P7.py:286`).
5. **No es «lo dado, dado está» aplicado a quien recibe**: la cesión (`mem.cedidos`, `decisor_zs.py:900-904`) solo se apunta en la memoria de quien suelta, y es lo que le impide a ÉL volver a
   cogerlo hasta que caduca (`appraisal_zs_v42_exp.py:663-683`); a esa caducidad se debe que lo recoja a los 280 tics.

**Y sin embargo pedía.** El pedido exige que la promesa del botiquín sea mayor que cero (`pide_P7.pide`). Con el zurrón lleno la promesa del cuerpo es 0, pero `descubre_P7` le suma lo que
aliviaría la curiosidad aunque no quepa (`descubre_P7.py:346-355`), así que una criatura con curiosidad y el zurrón lleno pide un botiquín que no puede coger. En TECHO, sin curiosidad, eso
no puede pasar con el zurrón lleno; sus 23 regalos vueltos a coger no están mirados aquí.

## Sección 6 · El pedido que se cierra al ver

P7-14b, los pedidos cerrados con motivo «lo ve» (`P7_15_pedidos.json`): si en los 30 segundos siguientes (720 tics) la criatura cogió un botiquín.

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| pedidos cerrados porque «lo ve» | 177 | 246 | 289 | 299 |
| … coge un botiquín en los 30 s siguientes | 31 (18 %) | 61 (25 %) | 67 (23 %) | 56 (19 %) |
| … y era uno de los que veía al cerrar | 21 | 45 | 48 | 44 |
| tics hasta cogerlo (mediana) | 82 | 49 | 42 | 93 |
| la criatura vivió esos 30 s | 162 | 217 | 254 | 279 |

En los cuatro brazos juntos, 215 de 1.011 (21 %): **casi cuatro de cada cinco pedidos se cierran al ver un botiquín que la criatura no llega a coger en medio minuto.**
«Lo ve» cierra el pedido, pero ver no es tener.

## Sección 7 · Lo que queda para la mesa (propuestas, nada decidido)

1. **Dónde mirar ahora: las muertes tempranas.** Son 10 de 80 en cada campo y llevan más de la mitad del puesto. Lo siguiente barato es un banco sobre esas 20 vidas (y las de BORRADO
   y TECHO que mueren pronto): escena a escena, qué veía, cuándo empezó el daño, cuándo abrió el canal y qué candidato tenía de alejarse.
2. **Esperar para curarse puede ser lo que el diseño quería y aun así costar el puesto.** P1 de P7-10 pedía que aprendiera a esperar. Si esperar bajo ataque es el problema, la pregunta de
   diseño es de qué depende la espera (hoy, de las ganas: cuanto más vale el botiquín, más cuesta gastarlo), no si se espera.
3. **El pedido con el zurrón lleno**: pedir lo que no cabe. O el pedido exige que quepa, o quien recibe hace sitio; es decisión de la mesa.
4. **Cuándo se cierra un pedido**: hoy al ver cualquier botiquín; casi cuatro de cada cinco veces no llega a tenerlo en medio minuto.
5. Todo esto son 6 o 7 muertes de diferencia por campo: la señal es la misma en dos campos independientes, pero es pequeña en número. No lo daría por cerrado sin el banco del punto 1.
6. **Puede que la pregunta esté al revés.** En P7-14b APRENDE no acaba peor que ESPERANZA ni que TECHO (dentro de 2·se, `informe_P7_14b.md`): es BORRADO el que acaba mejor que los tres. En P7-10 era APRENDE el
   que acababa peor que los otros tres. «Por qué pierde el que recuerda» y «por qué gana el que olvida cada día» no son la misma pregunta, y los dos campos no dicen lo mismo sobre cuál es.

## Archivos

| archivo | qué es |
|---|---|
| `analiza_P7_15.py` → `P7_15_vidas.json`, `P7_15_regalo.json`, `P7_15_pedidos.json` | lectura de los 640 diarios (cuándo muere, cómo vive), las escenas del regalo que nadie coge y los pedidos cerrados por «lo ve» |
| `banco_P7_15.py` → `P7_15_decisiones.json` | las 80 vidas de APRENDE de P7-14b decididas dos veces por tic |
| `escribe_informe_P7_15.py`, `informe_P7_15.md` | este informe |
