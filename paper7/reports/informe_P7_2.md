# P7-2 · El primer aprendizaje, en banco: una regla de memoria sobre lo ya vivido

*3-oct-2026. Coste cero: sin partidas, sin llamadas (plataforma 0; consola 0). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar
y al acabar; congelados sin tocar; el cuerpo no se toca: la regla vive en `cantera/paper7/memoria_P7_2.py` y el banco la usa por fuera.
Sello: `SELLO_P7_2.md`, commit 4a5fec2, md5 `5462127338cfdb045533a1d9b348ee4b` (escrito antes de calcular nada). Diario de partida: `P7_1_diario.json`
(2450 filas con resultado; 15 usos de botiquín "sin cerrar" excluidos porque no tienen resultado). Scripts: `memoria_P7_2.py` (la regla),
`mide_P7_2.py` (curvas, sello S1-S4, sensibilidad → `P7_2_curvas.json`, `P7_2_creencias.json`), `figuras_P7_2.py` (→ `P7_2_curvas.png`),
`banco_P7_2.py` (repetición de decisiones y fontanería → `P7_2_banco.json`), `escribe_informe_P7_2.py` (este informe). Semilla de barajado de
los 20 órdenes al azar: 20261003. Criaturas: asiento 10 y asiento 11; días: las 40 semillas en orden creciente (20260916 … 26439927).*

## Sección 1 · Las curvas de la creencia

Regla (de la mesa, sin ajustar): b = media ponderada de recuerdos; nacimiento = catálogo con peso 3; experiencia i con valor vivido v_i
(cura real, 0 si se cancela; daño hecho, 0 si `no_ammo`) y peso = intensidad × olvido, intensidad = min(2, 1 + |v_i − b_antes| / catálogo),
olvido = 0,95^días (también el nacimiento); dentro de un día, en orden (`memoria_P7_2.py`). Como el olvido multiplica igual a todos los
recuerdos, en un día sin experiencias la creencia no cambia; solo cambia la pesada relativa entre recuerdos de edades distintas.

| objeto / situación / asiento | experiencias (días con alguna) | creencia final, orden natural (fracción del catálogo) | banda de los 20 órdenes (fracción, mín-máx) | cruza el 50 % el día | cruza el 25 % el día | media real del diario ("techo") | catálogo ("suelo") |
|---|---:|---:|---:|---:|---:|---:|---:|
| botiquín / dentro / 10 | 40 (16) | 16,37 (0,33) | 0,28 – 0,47 | 8 | nunca | 17,57 | 50 |
| botiquín / dentro / 11 | 44 (18) | 20,52 (0,41) | 0,32 – 0,48 | 7 | nunca | 19,00 | 50 |
| botiquín / fuera / 10 | 48 (13) | 3,71 (0,07) | 0,03 – 0,09 | 1 | 1 | 1,04 | 50 |
| botiquín / fuera / 11 | 48 (14) | 7,08 (0,14) | 0,08 – 0,20 | 1 | 9 | 4,31 | 50 |
| arco / con municion / 10 | 55 (6) | 7,34 (0,52) | 0,53 – 0,68 | nunca | nunca | 8,65 | 14 |
| arco / con municion / 11 | 73 (7) | 7,98 (0,57) | 0,50 – 0,60 | 24 | nunca | 7,86 | 14 |
| arco / sin municion / 10 | 485 (4) | 0,02 (0,00) | 0,00 – 0,00 | 7 | 7 | 0,00 | 14 |
| arco / sin municion / 11 | 908 (6) | 0,01 (0,00) | 0,00 – 0,00 | 3 | 3 | 0,00 | 14 |
| cerbatana / con municion / 10 | 10 (3) | 1,48 (0,37) | 0,25 – 0,47 | 23 | nunca | 1,40 | 4 |
| cerbatana / con municion / 11 | 37 (6) | 1,93 (0,48) | 0,46 – 0,53 | 31 | nunca | 1,95 | 4 |
| cerbatana / sin municion / 10 | 48 (1) | 0,03 (0,01) | 0,01 – 0,05 | 38 | 38 | 0,00 | 4 |
| cerbatana / sin municion / 11 | 654 (4) | 0,00 (0,00) | 0,00 – 0,00 | 8 | 8 | 0,00 | 4 |

Figura: `P7_2_curvas.png` (seis paneles; línea = orden natural, puntos = días con experiencia, banda = mínimo-máximo de los 20 órdenes,
punteado = media real del diario, raya = catálogo). Fuente: `P7_2_curvas.json["principal"]`. Lectura: fuera del círculo el botiquín cae
el primer día con experiencia y se queda cerca de su media real; dentro baja hasta la media real (17-19 puntos), que está por debajo del
40 % del catálogo porque la cura real se acota por el hp máximo y porque los cortes por rivales valen 0. Sin munición, el arco y la
cerbatana caen a casi 0 el primer día con experiencias (cientos de filas en una sola pelea); con munición se quedan en la media real
(8 de 14 para el arco: los tiros que salen pero no alcanzan valen 0).

### El sello, S1 a S4 (`P7_2_curvas.json["sello"]`)

| predicción | asiento 10 | asiento 11 | veredicto |
|---|---|---|---|
| S1 botiquín fuera < 25 % (natural y ≥ 18 de 20 órdenes) | natural 0,07: sí; órdenes 20 de 20 | natural 0,14: sí; órdenes 20 de 20 | **acierta** |
| S2 botiquín dentro entre 40 y 80 % | 0,33: no (órdenes dentro del rango: 7 de 20) | 0,41: sí (15 de 20) | **falla en el asiento 10** |
| S3 sin munición < 10 % al acabar la primera vida con ≥ 5 filas | arco: día 7, 0,026: sí; cerbatana: día 38, 0,008: sí | arco: día 3, 0,015: sí; cerbatana: día 8, 0,131: no | **falla en blowgun/11** |
| S4 con munición a menos del 25 % del catálogo | arco 0,52, cerbatana 0,37 | arco 0,57, cerbatana 0,48 | **falla en los cuatro casos** (0 de 20 órdenes en todos) |

Sobre S3 en la cerbatana del asiento 11: el primer día con 5 o más filas sin munición es el 8 y al acabarlo la creencia
está en 0,131 del catálogo; cruza el 10 % el día 16. Sobre S4: con munición, la creencia converge a la media real del
diario, que es la mitad del catálogo porque la mitad de los tiros que salen no hacen daño; la predicción suponía que "con munición
pega lo que dice el catálogo", y el diario dice que no.

## Sección 2 · Repetición de decisiones con la creencia aprendida (`banco_P7_2.py`)

Réplica en seco del cuerpo A4 (molde de P6-29: el cuerpo recibe las observaciones del diario por un cable falso y decide tic a tic).
En cada tic con fila de diario (2450 decisiones en 58 vidas), se vuelve a decidir una segunda vez con la misma observación y
la misma memoria, cambiando solo lo que la previsión espera de ese objeto: `receta["heal"]` del candidato `usar_botiquin` (lo que
`decisor_zs.py:824` suma al hp previsto) o el `damage` del arma en la receta de `atacar_*` (lo que `decisor_zs.py:852-856` resta al
rival previsto), por la creencia vigente ese día antes de vivir la experiencia (orden natural, `P7_2_creencias.json`). Lo demás no se
toca: el candidato existe igual (`decisor_zs.py:588` mira el catálogo), la riqueza W y la amenaza ajena siguen leyendo el catálogo.

**Fontanería (punto 3).** Con la creencia igual al catálogo, es decir, la primera decisión de la réplica tal cual, contra `RADIOGRAFIA.elegido`
del diario en esos 2450 tics: **2450 de 2450 iguales** (100,0 %).
Nota de taller: la primera corrida del banco, con varias vidas seguidas en el mismo proceso, dio 1.674 de 2.450: en las vidas que no eran
la primera de su proceso desaparecía el candidato de atacar en defensa del hermano. La misma vida replayada sola daba 334 de 334. Se corrió
de nuevo con un proceso nuevo por vida (`maxtasksperchild=1`, `banco_P7_2.py`) y la fontanería es exacta; la causa (estado de módulo que
sobrevive entre vidas) queda apuntada, no corregida, porque no toca a este paso.

| objeto | situación | días | decisiones | elige lo mismo | elige otra cosa | qué otra cosa (las más frecuentes) |
|---|---|---|---:|---:|---:|---|
| botiquín | dentro | 1-20 | 22 | 17 (77,3 %) | 5 (22,7 %) | quedarse quieto 4; apartarse (un paso) 1 |
| botiquín | dentro | 21-40 | 62 | 31 (50,0 %) | 31 (50,0 %) | quedarse quieto 24; atacar 6; usar racion 1 |
| botiquín | fuera | 1-20 | 41 | 8 (19,5 %) | 33 (80,5 %) | quedarse quieto 30; ir al centro 1; coger lo de la casilla 1; apartarse (un paso) 1 |
| botiquín | fuera | 21-40 | 55 | 24 (43,6 %) | 31 (56,4 %) | quedarse quieto 27; ir a por otro objeto 1; apartarse (un paso) 1; coger lo de la casilla 1 |
| arco | sin municion | 1-20 | 530 | 518 (97,7 %) | 12 (2,3 %) | usar racion 10; usar botiquin 2 |
| arco | sin municion | 21-40 | 863 | 817 (94,7 %) | 46 (5,3 %) | apartarse (un paso) 18; usar botiquin 18; soltar 10 |
| arco | con municion | 1-20 | 69 | 68 (98,6 %) | 1 (1,4 %) | ir con el hermano 1 |
| arco | con municion | 21-40 | 59 | 58 (98,3 %) | 1 (1,7 %) | usar racion 1 |
| cerbatana | sin municion | 1-20 | 56 | 56 (100,0 %) | 0 (0,0 %) | – |
| cerbatana | sin municion | 21-40 | 646 | 645 (99,8 %) | 1 (0,2 %) | atacar 1 |
| cerbatana | con municion | 1-20 | 22 | 22 (100,0 %) | 0 (0,0 %) | – |
| cerbatana | con municion | 21-40 | 25 | 25 (100,0 %) | 0 (0,0 %) | – |

### El sello, S5 y S6

| predicción | medido | veredicto |
|---|---|---|
| S5a botiquín fuera, días 21-40: elige otra cosa ≥ 70 % | 31 de 55 (56,4 %) | **falla** |
| S5b botiquín dentro, días 21-40: sigue usándolo ≥ 70 % | 31 de 62 (50,0 %) | **falla** |
| S6 ataques sin munición, días 21-40: elige otra cosa ≥ 70 % | 47 de 1509 (3,1 %) (arco 46 de 863, cerbatana 1 de 646) | **falla** |

Fuente: `P7_2_banco.json` (por decisión: `elegido_diario`, `elegido_replica`, `elegido_creencia`, `clase_creencia`, d de cada candidato en
las dos decisiones). Por asiento, días 21-40: botiquín fuera asiento 10: 20 de 28 cambian; botiquín fuera asiento 11: 11 de 27 cambian; botiquín dentro asiento 10: 13 de 32 cambian; botiquín dentro asiento 11: 18 de 30 cambian; arco sin municion asiento 10: 4 de 262 cambian; arco sin municion asiento 11: 42 de 601 cambian; cerbatana sin municion asiento 10: 0 de 48 cambian; cerbatana sin municion asiento 11: 1 de 598 cambian; 

**Por qué falla, leído en las d de los candidatos.** En los 1462 ataques sin munición de los días 21-40 que no cambian, la creencia
vigente es de 0,021 puntos de mediana (nunca llega a 0: la media ponderada conserva el recuerdo de nacimiento) y la
decisión tenía 2 candidatos en 1127 casos (atacar y quedarse quieto: moverse está vetado por el enfriamiento en plena pelea). Con
un daño previsto minúsculo pero positivo, atacar sigue dando una d menor que quedarse quieto en 1126 casos, y en 336 empata
exactamente y el desempate prefiere la acción a la quietud. Es decir: mientras la creencia sea mayor que cero y no haya otra cosa que hacer,
el cuerpo dispara el arco vacío porque "no cuesta nada". Botiquín fuera, días 21-40: los 24 usos que no cambian tienen una creencia de
5,3 puntos de mediana (de 1,1 a 12,7) y los 31 que cambian, de 3,8 (de 1,0 a 8,2): los rangos se solapan. Por bandas de creencia:
b < 5: cambian 25 de 36; b 5-8: cambian 5 de 11; b ≥ 8: cambian 1 de 8. La creencia sola no fija el cambio: con la misma
creencia, unas fotos cambian y otras no, según lo demás que haya en ellas (vida, rivales, lo que se puede hacer). Dentro, la creencia es
la misma en los que cambian y en los que no (16-20): ahí también decide el resto de la foto.

## Sección 3 · Sensibilidad (después del sello y señalada como tal; no sustituye a la principal)

Misma medida, orden natural, cambiando un solo parámetro. Fracción del catálogo al final y día en que cruza el 25 %.

| objeto / situación / asiento | principal (0,95; peso 3) | olvido 0,90 | olvido 0,99 | nacimiento peso 1 | nacimiento peso 10 |
|---|---|---|---|---|---|
| botiquín / dentro / 10 | 0,33 (día –) | 0,31 (día –) | 0,36 (día –) | 0,33 (día –) | 0,34 (día –) |
| botiquín / dentro / 11 | 0,41 (día –) | 0,42 (día –) | 0,42 (día –) | 0,41 (día –) | 0,42 (día –) |
| botiquín / fuera / 10 | 0,07 (día 1) | 0,08 (día 1) | 0,08 (día 1) | 0,07 (día 1) | 0,10 (día 15) |
| botiquín / fuera / 11 | 0,14 (día 9) | 0,18 (día 9) | 0,15 (día 9) | 0,14 (día 4) | 0,16 (día 21) |
| arco / con municion / 10 | 0,52 (día –) | 0,49 (día –) | 0,57 (día –) | 0,52 (día –) | 0,53 (día –) |
| arco / con municion / 11 | 0,57 (día –) | 0,59 (día –) | 0,55 (día –) | 0,57 (día –) | 0,57 (día –) |
| arco / sin municion / 10 | 0,00 (día 7) | 0,00 (día 7) | 0,00 (día 7) | 0,00 (día 7) | 0,00 (día 7) |
| arco / sin municion / 11 | 0,00 (día 3) | 0,00 (día 3) | 0,00 (día 3) | 0,00 (día 3) | 0,00 (día 3) |
| cerbatana / con municion / 10 | 0,37 (día –) | 0,38 (día 23) | 0,40 (día –) | 0,35 (día 23) | 0,43 (día –) |
| cerbatana / con municion / 11 | 0,48 (día –) | 0,47 (día –) | 0,50 (día –) | 0,48 (día –) | 0,49 (día –) |
| cerbatana / sin municion / 10 | 0,01 (día 38) | 0,00 (día 38) | 0,04 (día 38) | 0,00 (día 38) | 0,03 (día 38) |
| cerbatana / sin municion / 11 | 0,00 (día 8) | 0,00 (día 8) | 0,00 (día 8) | 0,00 (día 8) | 0,00 (día 16) |

Fuente: `P7_2_curvas.json["sensibilidad"]`. El olvido mueve poco el final (los recuerdos se apagan todos a la vez); el peso de nacimiento
mueve el primer día y poco más cuando hay cientos de experiencias (arco sin munición) y bastante cuando hay pocas (cerbatana).

## Archivos

| archivo | qué es |
|---|---|
| `SELLO_P7_2.md` | las seis predicciones, con md5, commit 4a5fec2 antes de calcular |
| `memoria_P7_2.py` | la regla de memoria (experimental; el cuerpo no la importa) |
| `mide_P7_2.py`, `P7_2_curvas.json`, `P7_2_creencias.json` | curvas, sello S1-S4, sensibilidad; la creencia vigente en cada uso/ataque |
| `figuras_P7_2.py`, `P7_2_curvas.png` | la figura de las curvas |
| `banco_P7_2.py`, `P7_2_banco.json` | la réplica con la creencia aprendida; fontanería; `banco_P7_2.log` fuera de git |
| `escribe_informe_P7_2.py`, `informe_P7_2.md` | este informe |
