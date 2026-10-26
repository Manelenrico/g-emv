# P7-11 · Por qué el que aprende acaba peor, y qué es el suelo

*4-oct-2026. Todo lo de este paso es POSTERIOR AL SELLO de P7-10 y se declara así: son lecturas de los 320 diarios ya jugados, con medidas
elegidas después de ver el resultado. Nada de aquí cambia el sello (2 de 6). Coste: **créditos de la plataforma 0 USD** (ninguna partida);
**consola de Anthropic 0 USD** (ninguna llamada). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; el cuerpo y los congelados
no se tocan. Dos bancos de réplica (sin partidas ni llamadas), una vida por proceso: `banco_P7_11.py` (16 réplicas) y `banco_P7_11b.py`
(254 réplicas; fidelidad de la elección tic a tic: SUELO 725.285 iguales y 0 distintos, BORRADO 794.015 iguales y 193 distintos, APRENDE 920.392 iguales y 11 distintos, TECHO 905.060 iguales y 0 distintos).
Las definiciones de cada medida están en la cabecera de `analiza_P7_11.py`; las cifras salen de `P7_11_vidas.json` (lectura de los diarios),
`P7_11_filas.json` (réplica), `P7_11_dia1.json`, `P7_11_banco_dia1.json` y `P7_10_campo.json`.*

## Lo que sale, en corto

1. **SUELO no era lo que decía el diseño.** Desde la esperanza (pieza H, P7-9) el brazo SUELO imagina el botiquín como una ración: cura imaginada
   15,0 en sus 70 usos (mínimo 15,0, máximo 15,0) y ganas a 0,30 de las de TECHO. No es "el cuerpo que no sabe qué es
   un botiquín": es "el cuerpo con esperanza y sin memoria". La predicción P5 del sello (casi cero usos) describía el SUELO de antes de la esperanza.
2. **El día 1, APRENDE y BORRADO son el mismo cuerpo** (réplica: 96.119 tics, 0 elecciones distintas), pero no juegan el mismo mundo: con la misma semilla, lo que ven difiere desde el segundo tic.
3. **APRENDE no se distingue de BORRADO por ir a por botiquines** (los dos pasan en ello una quinta parte de la vida) sino por lo que hace con ellos:
   coge el doble y regala ocho veces más, casi todo pagado por la fila S-PROVISION con la creencia ya aprendida; más de la mitad de lo que regala lo
   vuelve a coger él mismo.
4. **APRENDE muere más a manos de un rival, y cuando muere así casi la mitad de las veces iba a por un botiquín.** Sin conclusiones causales.

## Sección 1 · El suelo

**Qué está encendido en cada brazo, tal como se jugó.** Las líneas son de `cantera/paper7/descubre_P7.py` de hoy; los interruptores los fija
`Dockerfile.pareja_P7_8:227-232` (GEMV_P7=1 y GEMV_P7_SITIO=1 para todos; CUADERNO, NOVEDAD, BORRADO y SABE por brazo; GEMV_P7_ESPERANZA y
GEMV_P7_SITIO_EMPATE no se fijan y valen 1 por defecto, `descubre_P7.py:56-57`).

| pieza | dónde | SUELO | BORRADO | APRENDE | TECHO |
|---|---|---|---|---|---|
| A · cuaderno y ventana de la experiencia | se lee en `:196` (solo con CUADERNO y sin BORRADO); la ventana se llama en `:369` (solo con CUADERNO o NOVEDAD); se apunta en `:263` | apagada: cuaderno vacío en memoria, nunca se apunta nada | encendida, sin leer: empieza vacío cada partida y apunta dentro de la vida | encendida: lee el del día anterior y apunta | apagada |
| A' · el recuerdo con techo ("al menos") | `:251`, `:263` | apagada | encendida | encendida | apagada |
| B · imaginación (la cura que imagina al usar) | `:283-284` (`if n == "usar_botiquin" and not SABE`), `heal_imaginado` `:119-127` | **encendida**: sin creencia, todo esperanza | encendida | encendida | apagada: la cura del catálogo |
| C · ganas (R-ACOPIO, W, W_TARGET por k) | `:332`, `:340-344`, `k_ganas` `:114-118` | **encendida** con k fijo = esperanza / cura | encendida | encendida | k = 1 (`:116`) |
| D · curiosidad (fila R-CURIOSIDAD y su promesa) | `:277`, `:337-338`, `:346-355` (NOVEDAD y sin SABE) | apagada | encendida | encendida | apagada |
| F · la curiosidad abre camino (`ir_curioso`) | `:286-306` (NOVEDAD y sin SABE) | apagada | encendida | encendida | apagada |
| E · hacer sitio | `:307-322`, `:374` (SITIO) | encendida | encendida | encendida | encendida |
| G · el regalo mira lo aprendido | `:335` (`if not SABE`), `regalo_aprendido` `:148-170`, `k_creencia` `:102-106` | **encendida** con k = 0 siempre (sin cuaderno, `:105`) | encendida | encendida | apagada (k = 1) |
| H · la esperanza | `:56` (1 por defecto), `mezcla` `:107-113`; entra por `:118` y `:127` | **encendida**: ignorancia 1 toda la vida (`:130-132`) | encendida | encendida | sin efecto (SABE sale antes, `:116`, `:122`) |
| I · en un empate, hacer sitio no gana | `:375-376` (SITIO y SITIO_EMPATE) | encendida | encendida | encendida | encendida |

Comprobado en los diarios (`P7_arranque.entorno_P7.efectivo`, las 80 vidas de cada brazo): SUELO: BORRADO=0, CUADERNO=0, ESPERANZA=1, NOVEDAD=0, ON=1, SABE=0, SITIO=1, SITIO_EMPATE=1 (80 de 80 iguales); BORRADO: BORRADO=1, CUADERNO=1, ESPERANZA=1, NOVEDAD=1, ON=1, SABE=0, SITIO=1, SITIO_EMPATE=1 (80 de 80 iguales); APRENDE: BORRADO=0, CUADERNO=1, ESPERANZA=1, NOVEDAD=1, ON=1, SABE=0, SITIO=1, SITIO_EMPATE=1 (80 de 80 iguales); TECHO: BORRADO=0, CUADERNO=0, ESPERANZA=1, NOVEDAD=0, ON=1, SABE=1, SITIO=1, SITIO_EMPATE=1 (80 de 80 iguales).

**Por qué SUELO usa botiquines.** En SUELO la pieza B está encendida (no es TECHO) y el cuaderno no existe, así que `heal_imaginado` llama a
`mezcla(mundo, None)` y, con la esperanza encendida por defecto, devuelve (1 − ignorancia) × 0 + ignorancia × esperanza con ignorancia 1: la media de
`heal` de los consumibles conocidos, la ración. Leído en la réplica de sus vidas con algún uso o regalo (725.285 tics, 0 distintos del diario):

| | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| usos (botiquín gastado) | 70 | 94 | 89 | 61 |
| usos por vida | 0,875 | 1,175 | 1,113 | 0,762 |
| candidato elegido en la decisión | `usar_botiquin` 70 de 70 | `usar_botiquin` 94 de 94 | `usar_botiquin` 88 de 89 | `usar_botiquin` 61 de 61 |
| cura imaginada: mediana (mín – máx) | 15,0 (15,0 – 15,0) | 15,0 (7,7 – 27,0) | 31,7 (7,8 – 41,2) | 50 (catálogo; no se toca) |
| k de las ganas en ese tic (mediana) | 0,30 | 0,30 | 0,65 | 1,00 |
| fila que paga el uso frente a `noop` | F-DANO 70 | F-DANO 93, R-CURIOSIDAD 1 | F-DANO 87, R-CURIOSIDAD 1 | F-DANO 61 |
| vida al usar: mediana | 85,0 | 86,0 | 69,0 | 63,0 |
| usos con la vida ≥ 85 (le faltan 15 o menos) | 36 | 56 | 19 | 14 |
| usos con la vida < 50 | 5 | 12 | 20 | 16 |
| botiquines cogidos | 123 | 143 | 297 | 168 |

En los 70 usos de SUELO gana `usar_botiquin`, lo paga la fila F-DANO (el daño que el cuerpo lleva encima) y la cura imaginada es 15,0 en todos:
la de la ración. Con una cura imaginada de 15 el botiquín se usa como una ración, en cuanto falta algo de vida (mediana 85,0; 36 de 70 con la vida en 85 o más).
Las ganas también llevan la esperanza: k = 15 / 50 = 0,30 toda la vida, y por eso SUELO coge 123 botiquines.

**Dicho claro.** La cabecera de `descubre_P7.py` describe SUELO como "P7=1 SITIO=1" (`:45`) y las piezas B y C como "no sé → 0" (`:12`, `:15`): un
cuerpo que no le pone efecto al botiquín y no lo quiere. Eso fue verdad hasta P7-8. Desde la pieza H (P7-9), "nunca probado: todo esperanza"
(`:108-109`), y SUELO, que no aprende nunca, se queda para siempre en ese punto: imagina 15 y quiere a 0,3. El sello de P7-10 lo dice ("con la
esperanza, pieza H", para los cuatro brazos) pero su predicción P5 ("SUELO casi no usa botiquines") es la del SUELO de antes. **SUELO, tal como se
jugó, no es el suelo del diseño (el cuerpo que no sabe): es el cuerpo con esperanza y sin memoria.** Como referencia de "no sabe nada" no sirve;
como referencia de "esperanza sola, sin aprender" sí, y así hay que leerlo: el día 1 de BORRADO y de APRENDE antes del primer uso es ese mismo cuerpo más la curiosidad.

**Otra cosa que no era igual entre brazos.** Las tres imágenes fijas se subieron antes del freno (SUELO v7 a las 19:43 UTC, BORRADO v8 a las 19:43 UTC, TECHO v9 a las 19:43 UTC),
con `descubre_P7.py` del sello (md5 `76c0222dcd806cfb0747a9c70c38fe61`). El arreglo del apéndice del sello (una ventana con un regalo dentro no se
apunta; md5 de hoy `9f9080eed55968e5869597ef0c7c7b41`) entró después: lo llevan APRENDE de la serie 2 entera y de la serie 1 desde el día 4, y no lo lleva
BORRADO en ninguno de sus 40 días (sus huellas no tienen el campo `regalado`: 58 vidas con huellas, 0 con el campo; APRENDE: 60 con el campo, 6 sin él, las de los días 1 a 3 de la serie 1).
El alcance medido: ventanas con un regalo dentro que se apuntaron como experiencia: BORRADO 6 (en 4 de 80 vidas; como BORRADO no lee, el recuerdo falso muere con la partida),
APRENDE 2 (las del día 3 del freno, limpiadas a mano antes del día 4). En SUELO y TECHO el cambio no hace nada (no apuntan). Es pequeño, pero BORRADO y APRENDE no llevaban exactamente el mismo código.

## Sección 2 · El día 1

**Los diarios no se pueden comparar tic a tic, porque los dos mundos no son el mismo.** Misma semilla, mismo asiento, día 1 (`P7_11_dia1.json`):

| serie | asiento | par | primer tic vivo | primer tic en que lo visto difiere | qué difiere | primer tic con la elección distinta |
|---|---|---|---:|---:|---|---:|
| 1 | 10 | APRENDE y BORRADO | 481 | 482 | ve_agentes (agente 9) | 514 |
| 1 | 10 | SUELO y TECHO | 481 | 483 | chat | 481 |
| 1 | 10 | BORRADO y SUELO | 481 | 483 | chat | 514 |
| 1 | 11 | APRENDE y BORRADO | 481 | 483 | chat | 558 |
| 1 | 11 | SUELO y TECHO | 481 | 483 | chat | 558 |
| 1 | 11 | BORRADO y SUELO | 481 | 483 | chat | 537 |
| 2 | 10 | APRENDE y BORRADO | 481 | 482 | ve_agentes (agente 9) | 976 |
| 2 | 10 | SUELO y TECHO | 481 | 483 | chat | 602 |
| 2 | 10 | BORRADO y SUELO | 481 | 483 | chat | 602 |
| 2 | 11 | APRENDE y BORRADO | 481 | 483 | chat | 922 |
| 2 | 11 | SUELO y TECHO | 481 | 483 | chat | 580 |
| 2 | 11 | BORRADO y SUELO | 481 | 483 | chat | 515 |

En los cuatro pares APRENDE–BORRADO lo visto difiere en el tic 482 o 483, uno o dos tics después de empezar: el texto que los rivales dicen por el canal
abierto ("blood pays little here" en una partida, "blood pays nothing here" en la otra) o la casilla de un rival. No es cosa del brazo: pasa igual
entre SUELO y TECHO y entre BORRADO y SUELO. Es la pregunta abierta 1 para Ari en `STATUS.md` (algo aleatorio en el mundo que no depende de la
semilla). Mientras lo visto fue igual (1, 2, 1, 2 tics), elección y d de cada candidato idénticas en los cuatro pares.

**La comparación que sí se puede hacer: el mismo diario, con los dos juegos de interruptores** (`banco_P7_11.py` → `P7_11_banco_dia1.json`; un
subproceso por vida, cuaderno vacío):

| diario del día 1 | tics | réplica como APRENDE: iguales al diario | réplica como BORRADO: iguales al diario | tics en que las dos réplicas eligen distinto | cuaderno final igual |
|---|---:|---:|---:|---:|---|
| `P710_s1_d1_APRENDE_29581797/10` | 770 | 770 | 770 | 0 | sí |
| `P710_s1_d1_APRENDE_29581797/11` | 14.184 | 14.184 | 14.184 | 0 | sí |
| `P710_s1_d1_BORRADO_29581797/10` | 11.664 | 11.664 | 11.664 | 0 | sí |
| `P710_s1_d1_BORRADO_29581797/11` | 12.456 | 12.456 | 12.456 | 0 | sí |
| `P710_s2_d1_APRENDE_31571648/10` | 14.520 | 14.520 | 14.520 | 0 | sí |
| `P710_s2_d1_APRENDE_31571648/11` | 14.520 | 14.520 | 14.520 | 0 | sí |
| `P710_s2_d1_BORRADO_31571648/10` | 13.819 | 13.819 | 13.819 | 0 | sí |
| `P710_s2_d1_BORRADO_31571648/11` | 14.186 | 14.186 | 14.186 | 0 | sí |

**Sí: el día 1 son el mismo cuerpo, decisión a decisión.** 96.119 tics en 8 vidas, 0 elecciones distintas entre los dos juegos de interruptores, los 8 cuadernos
finales iguales, y las dos réplicas reproducen el diario entero. El interruptor BORRADO solo se mira al arrancar (`descubre_P7.py:196`), y con el
cuaderno vacío leer o no leer da lo mismo. Lo que difiere el día 1 entre los dos brazos es la partida, no el cuerpo. Para que conste, el día 1
(4 vidas por brazo, `P7_10_campo.json`): botiquines cogidos APRENDE 7, BORRADO 4; usos 6 y 4; regalos 0 y 0;
puestos [1, 2, 3, 16] y [2, 3, 4, 9]. Esa es la medida del ruido entre dos partidas del mismo cuerpo con la misma semilla.
(La vida `P710_s1_d1_APRENDE_29581797/10` duró 770 tics: murió pronto.)

## Sección 3 · La curva día a día

Por día de cada serie (las dos series y los dos asientos juntos: 4 vidas por brazo y día). Vida al usar = mediana sobre los usos gastados de ese
día (entre paréntesis, cuántos); usos por vida = usos / 4. Creencia (cuerpo, dentro del círculo) e ignorancia de APRENDE al fin del día: media de
las cuatro criaturas ("no sé" no entra en la media; entre paréntesis, cuántas tienen creencia).

| día | SUELO: vida al usar | usos por vida | BORRADO: vida al usar | usos por vida | APRENDE: vida al usar | usos por vida | TECHO: vida al usar | usos por vida | APRENDE: creencia | APRENDE: ignorancia |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 66,0 (2) | 0,50 | 76,0 (4) | 1,00 | 71,0 (6) | 1,50 | 63,0 (3) | 0,75 | 17,5 (2) | 0,244 |
| 2 | 86,0 (5) | 1,25 | 82,0 (6) | 1,50 | 78,5 (4) | 1,00 | 83,0 (1) | 0,25 | 18,1 (4) | 0,299 |
| 3 | 83,0 (4) | 1,00 | 22,0 (2) | 0,50 | 67,0 (5) | 1,25 | 26,0 (2) | 0,50 | 22,5 (4) | 0,215 |
| 4 | 86,5 (2) | 0,50 | 69,0 (5) | 1,25 | 62,5 (4) | 1,00 | 52,0 (1) | 0,25 | 26,8 (4) | 0,169 |
| 5 | 91,5 (8) | 2,00 | 80,5 (6) | 1,50 | 68,5 (8) | 2,00 | 92,0 (4) | 1,00 | 29,1 (4) | 0,120 |
| 6 | 84,0 (4) | 1,00 | 78,0 (6) | 1,50 | 64,5 (6) | 1,50 | 86,0 (3) | 0,75 | 29,8 (4) | 0,104 |
| 7 | 78,0 (7) | 1,75 | 83,5 (4) | 1,00 | 71,5 (4) | 1,00 | – (0) | 0,00 | 30,2 (4) | 0,100 |
| 8 | – (0) | 0,00 | 87,0 (6) | 1,50 | 43,5 (2) | 0,50 | 46,0 (1) | 0,25 | 31,1 (4) | 0,099 |
| 9 | 85,0 (3) | 0,75 | 89,0 (6) | 1,50 | 71,0 (3) | 0,75 | – (0) | 0,00 | 31,5 (4) | 0,100 |
| 10 | 71,0 (4) | 1,00 | 92,0 (5) | 1,25 | 76,5 (6) | 1,50 | 76,0 (3) | 0,75 | 35,7 (4) | 0,079 |
| 11 | 87,5 (2) | 0,50 | 89,0 (5) | 1,25 | 73,5 (6) | 1,50 | 73,0 (3) | 0,75 | 35,7 (4) | 0,071 |
| 12 | 82,0 (4) | 1,00 | 92,0 (7) | 1,75 | 72,5 (4) | 1,00 | 46,0 (3) | 0,75 | 36,5 (4) | 0,067 |
| 13 | 83,0 (3) | 0,75 | 79,0 (4) | 1,00 | 74,0 (4) | 1,00 | 60,0 (1) | 0,25 | 36,4 (4) | 0,065 |
| 14 | 89,0 (5) | 1,25 | 89,0 (3) | 0,75 | 73,0 (5) | 1,25 | 54,0 (3) | 0,75 | 39,3 (4) | 0,061 |
| 15 | 86,0 (6) | 1,50 | 87,0 (5) | 1,25 | 67,0 (5) | 1,25 | 67,0 (7) | 1,75 | 38,9 (4) | 0,059 |
| 16 | 56,0 (3) | 0,75 | 89,0 (5) | 1,25 | 64,0 (4) | 1,00 | 59,0 (3) | 0,75 | 39,3 (4) | 0,057 |
| 17 | 89,0 (3) | 0,75 | 58,0 (5) | 1,25 | 56,0 (3) | 0,75 | 67,0 (8) | 2,00 | 39,7 (4) | 0,057 |
| 18 | 86,0 (1) | 0,25 | 86,0 (3) | 0,75 | 54,5 (4) | 1,00 | 60,0 (5) | 1,25 | 39,7 (4) | 0,055 |
| 19 | 83,0 (2) | 0,50 | 92,0 (2) | 0,50 | 72,5 (4) | 1,00 | 71,0 (8) | 2,00 | 39,4 (4) | 0,053 |
| 20 | 53,5 (2) | 0,50 | 80,0 (5) | 1,25 | 72,0 (2) | 0,50 | 54,5 (2) | 0,50 | 39,1 (4) | 0,054 |

**¿En qué día se aplana APRENDE?** (criterios puestos después de ver los datos, declarados: la creencia "se aplana" el primer día a partir del
cual ya no se aleja más de 2 puntos de su valor del día 20; la ignorancia, más de 0,02.)

| criatura | creencia: día en que se aplana | creencia ese día → día 20 | ignorancia: día en que se aplana | ignorancia ese día → día 20 |
|---|---:|---|---:|---|
| serie 1, asiento 10 | 7 | 41,8 → 41,8 | 11 | 0,061 → 0,045 |
| serie 1, asiento 11 | 16 | 35,3 → 34,0 | 12 | 0,071 → 0,060 |
| serie 2, asiento 10 | 9 | 41,4 → 42,4 | 8 | 0,074 → 0,054 |
| serie 2, asiento 11 | 14 | 36,9 → 38,3 | 13 | 0,066 → 0,055 |

Con la media de las cuatro: la creencia se aplana el día 14 (39,3 → 39,1) y la ignorancia el día 11 (0,071 → 0,054).
Del día 10 al 20 la creencia media pasa de 35,7 a 39,1: la segunda mitad del campo casi no enseña nada nuevo.

**La vida al usar no baja con los días en ningún brazo.** Correlación de rangos (Spearman) entre el día y la vida al usar, uso a uso, con una
prueba de permutaciones (5.000 barajas de los días, semilla fija): SUELO ρ = -0,05 (p = 0,71, 70 usos); BORRADO ρ = 0,24 (p = 0,02, 94 usos); APRENDE ρ = -0,03 (p = 0,78, 89 usos); TECHO ρ = -0,03 (p = 0,83, 61 usos).
En APRENDE la mediana por tramos es 68,0, 71,0, 73,0, 67,0 (días 1-5, 6-10, 11-15, 16-20): plana desde el primer tramo. Lo que
separa a APRENDE de BORRADO en la vida al usar ya está el primer tramo (68,0 frente a 78,0): la creencia media es 18,1 el día 2 y
29,1 el día 5, sube deprisa los cinco primeros días y despacio después. En BORRADO la vida al usar sube con los días (ρ = 0,24), y
BORRADO no puede aprender de un día a otro: esa es la medida de lo que hacen solas las semillas y el azar con 94 usos. Por días sueltos
la mediana es ruido (entre 0 y 9 usos por brazo y día).

## Sección 4 · Dónde y cómo muere

Causa = la fuente que más daño hizo en los últimos 30 tics (`campo_P7_10.py`, la misma del sello).

| brazo | por rival | por el anillo | otra | sobrevive al final |
|---|---:|---:|---:|---:|
| SUELO | 14 | 41 | 0 | 25 |
| BORRADO | 22 | 32 | 0 | 26 |
| APRENDE | 28 | 36 | 0 | 16 |
| TECHO | 13 | 42 | 0 | 25 |

**Las muertes por rival: los 10 segundos anteriores** (240 tics; a cada tic, el candidato en curso: el último elegido distinto de `noop` en el medio
segundo anterior). Reparto de los tics de esa ventana, sumadas las muertes por rival de cada brazo:

| en curso | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| ir a por un botiquín | 0,0 % | 23,1 % | 33,5 % | 2,0 % |
| ir a por un objeto (sin llegar a cogerlo) | 15,9 % | 8,0 % | 13,9 % | 16,6 % |
| ir al botín del centro o coger | 1,9 % | 2,7 % | 1,2 % | 5,9 % |
| regalar o soltar | 0,1 % | 0,0 % | 0,1 % | 0,0 % |
| pelear (atacar, empuñar) | 8,6 % | 6,3 % | 5,9 % | 8,9 % |
| usar un consumible | 2,7 % | 0,7 % | 2,0 % | 2,8 % |
| moverse paso a paso | 42,5 % | 27,5 % | 27,8 % | 41,3 % |
| ir al hermano | 18,5 % | 2,9 % | 3,8 % | 8,6 % |
| ir al centro | 3,5 % | 1,1 % | 3,3 % | 8,1 % |
| quieto | 6,2 % | 27,6 % | 8,6 % | 5,9 % |

| las muertes por rival, una a una | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| muertes por rival | 14 | 22 | 28 | 13 |
| lo que más hacía en la ventana: ir a por un botiquín | 0 | 7 | 13 | 1 |
| lo que más hacía: moverse paso a paso | 6 | 6 | 7 | 5 |
| lo que más hacía: quieto | 1 | 8 | 4 | 1 |
| lo que más hacía: pelear | 2 | 1 | 1 | 1 |
| lo que más hacía: otra cosa | 5 | 0 | 3 | 5 |
| muere dentro del círculo | 14 | 19 | 27 | 11 |
| muere fuera del círculo | 0 | 3 | 1 | 2 |
| muere con algún botiquín a bordo | 3 | 4 | 7 | 5 |
| abrió el canal del botiquín en la ventana | 3 | 4 | 9 | 5 |
| con un botiquín a la vista en el suelo al morir | 10 | 12 | 16 | 11 |
| distancia a ese botiquín (mediana, casillas) | 2,7 | 2,2 | 2,9 | 2,2 |
| vio algún botiquín en el suelo en la ventana | 12 | 15 | 18 | 12 |
| distancia al más cercano de esos (mediana) | 2,7 | 2,8 | 3,0 | 2,2 |
| vida al empezar la ventana (mediana) | 87,0 | 50,5 | 57,5 | 70,0 |
| daño de rivales en la ventana (mediana) | 84,6 | 34,2 | 51,8 | 54,0 |
| tic de la muerte (mediana) | 12.612 | 14.186 | 12.070 | 13.105 |

El cuerpo no tiene un candidato que se llame huir: alejarse de un rival sale como "moverse paso a paso" (`move_*`, `paso_*`), que también es
acercarse; el diario no los separa y aquí no se separan. Regalar, soltar y hacer sitio casi no aparecen en esas ventanas (SUELO 0, BORRADO 0, APRENDE 1, TECHO 0 regalos).
Lo que distingue a APRENDE: 13 de sus 28 muertes por rival llegan yendo a por un botiquín (BORRADO 7 de 22; SUELO y TECHO, que no tienen
curiosidad, 0 y 1), casi siempre dentro del círculo y, en la mayoría, con uno a la vista a unas tres casillas.

## Sección 5 · El tiempo

Media por vida (80 vidas por brazo). "Tics" con el candidato en curso (la definición de la sección 4); entre paréntesis, la parte de la vida.

| | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| tics vivos | 13.237 | 13.148 | 12.469 | 13.246 |
| yendo a por un botiquín | 140 (1,1 %) | 2.499 (18,9 %) | 2.759 (22,5 %) | 455 (3,5 %) |
| … de ellos, con un rival a la vista | 71 | 2.006 | 2.211 | 369 |
| decisiones `ir_curioso` o `ir_objeto` hacia un botiquín (tics con ese elegido) | 13 | 1.897 | 2.154 | 43 |
| yendo a por un objeto que no llega a coger | 2.585 | 2.266 | 2.176 | 2.510 |
| regalando o soltando un botiquín (tics con `soltar_first_aid` elegido) | 0,30 | 0,26 | 2,14 | 0,86 |
| … de ellos, con un rival a la vista | 0,15 | 0,24 | 1,84 | 0,78 |
| con el canal del botiquín abierto | 63,1 | 84,9 | 98,7 | 71,3 |
| … de ellos, con un rival a la vista | 55,6 | 76,9 | 85,5 | 54,4 |
| con algún botiquín a bordo | 5.889 | 7.010 | 7.141 | 7.064 |
| con un rival a la vista (toda la vida) | 11.167 (84,6 %) | 11.153 (85,3 %) | 10.256 (82,6 %) | 10.770 (80,7 %) |

Regalar es un gesto de un tic: el tiempo no se va en regalar. Se va en ir: BORRADO y APRENDE pasan yendo a por un botiquín 18,9 % y
22,5 % de la vida; SUELO y TECHO, 1,1 % y 3,5 %. "Con un rival a la vista" discrimina poco: hay alguno a la vista
más del 80 % del tiempo en los cuatro brazos. (En SUELO y TECHO el destino de `ir_objeto` no está en el diario: solo cuentan como "a por un botiquín"
las rachas que acaban cogiendo uno; las que no acaban en nada van en la fila siguiente, igual para los cuatro.)

Por tramos de días, parte de la vida yendo a por un botiquín:

| | días 1-5 | días 6-10 | días 11-15 | días 16-20 |
|---|---:|---:|---:|---:|
| BORRADO | 17,9 % | 20,9 % | 20,1 % | 16,7 % |
| APRENDE | 19,8 % | 20,8 % | 22,9 % | 26,6 % |

En APRENDE la ignorancia baja con los días (sección 3) y el tiempo yendo a por botiquines no baja: sube. La curiosidad se hace pequeña, pero el
candidato `ir_curioso` existe siempre que no lleva botiquín y sabe de uno (`descubre_P7.py:286`), y las ganas (k) crecen con la creencia.

## Sección 6 · Los regalos

Un regalo = `soltar_first_aid` elegido y ejecutado (baja el número de botiquines a bordo); puede soltar una pila de varias unidades.

| | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| regalos (gestos) | 24 | 21 | 171 | 69 |
| unidades regaladas | 34 | 41 | 307 | 122 |
| vidas con algún regalo (de 80) | 9 | 11 | 39 | 37 |
| máximo de regalos en una vida | 15 | 7 | 24 | 10 |
| lo recoge el hermano | 2 | 4 | 69 | 20 |
| lo vuelve a coger él mismo | 16 | 9 | 93 | 27 |
| seguía en el suelo la última vez que se vio la casilla | 4 | 7 | 8 | 18 |
| desaparece, con un rival visto encima (lo recoge un rival) | 1 | 1 | 1 | 4 |
| desaparece sin ver quién | 1 | 0 | 0 | 0 |
| tics hasta que alguien lo recoge (mediana) | 296 | 290 | 279 | 285 |
| con el hermano a la vista | 24 | 21 | 170 | 69 |
| hermano sano / herido / crítico | 16 / 7 / 1 | 14 / 3 / 4 | 151 / 8 / 12 | 44 / 13 / 12 |
| con un rival a la vista | 12 | 19 | 147 | 62 |
| con el canal del botiquín abierto | 4 | 6 | 10 | 9 |
| vida de quien regala (mediana) | 100,0 | 100,0 | 100,0 | 100,0 |
| botiquines cogidos | 123 | 143 | 297 | 168 |
| … de ellos, que había soltado el hermano | 3 | 4 | 79 | 22 |

**Qué fila gana cuando regala** (réplica, `P7_11_filas.json`: la fila cuya M más mejora entre `soltar_first_aid` y `noop` en el tic de la decisión)
y con qué creencia (k = creencia máxima / cura del catálogo, lo que mira la pieza G; TECHO no pasa por G y vale 1; SUELO vale 0 siempre):

| fila que paga | SUELO | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| S-PROVISION | 0 | 14 | 151 | 44 |
| ninguna (empate en todas las filas) | 24 | 6 | 5 | 6 |
| S-HERIDO | 0 | 1 | 15 | 19 |
| k de quien regala: mediana (mín – máx) | 0,00 (0,00 – 0,00) | 0,20 (0,00 – 0,28) | 0,69 (0,08 – 0,86) | 1,00 (1,00 – 1,00) |
| regalos con k = 0 ("no sé") | 24 | 4 | 0 | 0 |
| ventaja de regalar sobre `noop` en d (mediana) | 0,0000 | 0,0139 | 0,0558 | 0,0749 |

(1 decisión de las 599 de usar o regalar no coincide en la réplica y queda fuera de estas dos tablas.)

**Sí, TECHO regala: 69 gestos, 122 unidades, en 37 de 80 vidas.** Los paga S-PROVISION (la hermana sin venda) en 44 y
S-HERIDO en 19. APRENDE regala 171: 151 por S-PROVISION, con k mediana 0,69 (creencia 34,3): la pieza G deja
pasar el regalo en proporción a lo aprendido, y con una creencia de 34 sobre 50 deja pasar dos tercios de S-PROVISION. Ninguno de los 171 regalos de
APRENDE es con "no sé". El hermano está sano en 151 de 171: la mayoría no son regalos a un herido, son a un hermano sin botiquín.

**A dónde van.** De los 171 regalos de APRENDE, 93 los vuelve a coger el mismo que los soltó, 69 los recoge el hermano, 8 seguían en el
suelo y 1 se lo lleva un rival. En TECHO: 27, 20, 18 y 4. A los rivales no les llega casi nada en ningún brazo. El regalo de
APRENDE es sobre todo un ir y venir entre los dos hermanos y el suelo: de los 297 botiquines que coge APRENDE, 79 los había soltado el hermano
y 93 los había soltado él mismo. Quitando esas dos partidas quedan 125 cogidas "nuevas" (BORRADO: 130; TECHO: 119; SUELO: 104).
Está concentrado: las tres vidas que más regalan suman 64 de los 171.

SUELO regala 24 veces con k = 0: la pieza G le quita al botiquín su valor para el hermano, ninguna fila mejora y en 24 de 24 la d de
regalar es exactamente la de `noop`: son empates que gana `soltar_first_aid` porque el desempate de la casa no deja ganar a `noop`
(`decisor_zs.py:895-897`, `exclude_noop=True`). 15 de los 24 son de una sola vida (serie 1, día 14, asiento 11). Con empate exacto en BORRADO: 6 de 21;
APRENDE: 5 de 171; TECHO: 6 de 69.

## Sección 7 · Lo que distingue a APRENDE (sin conclusiones causales)

Para cada medida, la diferencia entre brazos emparejada por semilla: en cada una de las 20 semillas, la media de las 4 vidas de un brazo (2 series
× 2 asientos) menos la del otro; d̄ es la media de esas 20 diferencias y se su error típico (el ruido entre semillas). **En negrita, |d̄| > 2·se.**
Las dos partidas de una semilla no son el mismo mundo (sección 2) y las 15 medidas no son independientes: con tantas, alguna pasaría de 2·se por azar.

| medida (por vida) | APRENDE | TECHO | d̄ (APRENDE − TECHO) | se | d̄ / se |
|---|---:|---:|---:|---:|---:|
| botiquines cogidos | 3,71 | 2,10 | **1,61** | 0,66 | **2,4** |
| regalos | 2,14 | 0,86 | **1,27** | 0,57 | **2,2** |
| usos | 1,11 | 0,76 | **0,35** | 0,14 | **2,4** |
| canales interrumpidos | 2,11 | 1,51 | 0,60 | 0,32 | 1,9 |
| tics yendo a por un botiquín | 2.759 | 455 | **2.303** | 390 | **5,9** |
| … con un rival a la vista | 2.211 | 369 | **1.842** | 307 | **6,0** |
| tics con el canal abierto | 98,70 | 71,35 | **27,35** | 9,54 | **2,9** |
| tics con un rival a la vista | 10.256 | 10.770 | -514 | 644 | -0,8 |
| tics vivos | 12.469 | 13.246 | -777 | 408 | -1,9 |
| muere por rival (0/1) | 0,35 | 0,16 | **0,19** | 0,07 | **2,8** |
| muere por el anillo (0/1) | 0,45 | 0,53 | -0,07 | 0,09 | -0,9 |
| sobrevive al final (0/1) | 0,20 | 0,31 | -0,11 | 0,06 | -1,8 |
| daño de rivales en los últimos 10 s | 24,91 | 13,50 | **11,41** | 5,48 | **2,1** |
| vida al morir | 6,42 | 10,99 | **-4,56** | 1,66 | **-2,8** |
| puesto | 5,91 | 4,36 | **1,55** | 0,69 | **2,3** |

| medida (por vida) | APRENDE | BORRADO | d̄ (APRENDE − BORRADO) | se | d̄ / se |
|---|---:|---:|---:|---:|---:|
| botiquines cogidos | 3,71 | 1,79 | **1,93** | 0,70 | **2,8** |
| regalos | 2,14 | 0,26 | **1,88** | 0,64 | **2,9** |
| usos | 1,11 | 1,18 | -0,06 | 0,16 | -0,4 |
| canales interrumpidos | 2,11 | 1,31 | 0,80 | 0,40 | 2,0 |
| tics yendo a por un botiquín | 2.759 | 2.499 | 260 | 374 | 0,7 |
| … con un rival a la vista | 2.211 | 2.006 | 206 | 381 | 0,5 |
| tics con el canal abierto | 98,70 | 84,94 | 13,76 | 8,33 | 1,7 |
| tics con un rival a la vista | 10.256 | 11.153 | **-897** | 412 | **-2,2** |
| tics vivos | 12.469 | 13.148 | -679 | 384 | -1,8 |
| muere por rival (0/1) | 0,35 | 0,28 | 0,07 | 0,05 | 1,6 |
| muere por el anillo (0/1) | 0,45 | 0,40 | 0,05 | 0,08 | 0,6 |
| sobrevive al final (0/1) | 0,20 | 0,33 | -0,12 | 0,07 | -1,7 |
| daño de rivales en los últimos 10 s | 24,91 | 16,56 | 8,35 | 5,20 | 1,6 |
| vida al morir | 6,42 | 11,49 | **-5,06** | 1,62 | **-3,1** |
| puesto | 5,91 | 4,66 | **1,25** | 0,57 | **2,2** |

| medida (por vida) | BORRADO | TECHO | d̄ (BORRADO − TECHO) | se | d̄ / se |
|---|---:|---:|---:|---:|---:|
| botiquines cogidos | 1,79 | 2,10 | -0,31 | 0,28 | -1,1 |
| regalos | 0,26 | 0,86 | **-0,60** | 0,25 | **-2,4** |
| usos | 1,18 | 0,76 | **0,41** | 0,16 | **2,6** |
| canales interrumpidos | 1,31 | 1,51 | -0,20 | 0,33 | -0,6 |
| tics yendo a por un botiquín | 2.499 | 455 | **2.044** | 372 | **5,5** |
| … con un rival a la vista | 2.006 | 369 | **1.636** | 358 | **4,6** |
| tics con el canal abierto | 84,94 | 71,35 | 13,59 | 8,50 | 1,6 |
| tics con un rival a la vista | 11.153 | 10.770 | 383 | 701 | 0,5 |
| tics vivos | 13.148 | 13.246 | -97 | 378 | -0,3 |
| muere por rival (0/1) | 0,28 | 0,16 | 0,11 | 0,07 | 1,6 |
| muere por el anillo (0/1) | 0,40 | 0,53 | -0,12 | 0,07 | -1,7 |
| sobrevive al final (0/1) | 0,33 | 0,31 | 0,01 | 0,08 | 0,2 |
| daño de rivales en los últimos 10 s | 16,56 | 13,50 | 3,06 | 4,55 | 0,7 |
| vida al morir | 11,49 | 10,99 | 0,50 | 1,85 | 0,3 |
| puesto | 4,66 | 4,36 | 0,30 | 0,62 | 0,5 |

Lo que se lee, sin decir por qué:

- **Ir a por botiquines no separa a APRENDE de BORRADO** (d̄ / se = 0,7) y sí a los dos de TECHO (5,9 y 5,5). BORRADO va tanto como
  APRENDE y no acaba peor que TECHO (puesto: d̄ / se = 0,5; vida al morir: 0,3). Ir a por botiquines, por sí solo, no viene con peor puesto en este campo.
- **Lo que APRENDE tiene y BORRADO no**: coge más (d̄ / se = 2,8), regala más (2,9), y acaba con menos vida (-3,1) y peor puesto (2,2).
  En usos no se distinguen (-0,4).
- **Frente a TECHO**, APRENDE coge más (2,4), regala más (2,2), usa más (2,4), tiene el canal abierto más tiempo (2,9), muere más por
  rival (2,8) y recibe más daño de rivales en sus últimos 10 segundos (2,1).
- **Las diferencias grandes frente al ruido** son las de conducta con los botiquines (ir, coger, regalar: entre 2 y 6 se). Las de resultado (puesto,
  vida al morir, muerte por rival) están entre 2 y 3 se: fuera del criterio del sello, pero cerca del borde para 15 medidas miradas a la vez.
- Dentro de un brazo, cruzar el puesto con los botiquines cogidos o usados no sirve: quien vive más coge y usa más, y vive más quien queda mejor.

## Sección 8 · Lo que queda para la mesa (propuestas, nada decidido)

1. **Qué es SUELO.** Tal como está es "esperanza sin memoria". Si la mesa quiere además el suelo del diseño ("no sabe": cura imaginada 0, ganas 0),
   haría falta un quinto brazo o apagar la esperanza en SUELO (`GEMV_P7_ESPERANZA=0` solo en ese brazo). Cualquiera de las dos cosas es un campo nuevo con sello nuevo.
2. **P5 del sello** predecía sobre un SUELO que ya no existía cuando se selló. El resultado (falla) no cambia; la lectura sí: no informa de si un cuerpo que no sabe usa botiquines.
3. **El regalo entre hermanos sanos.** En APRENDE, S-PROVISION paga 151 de 171 regalos, con el hermano sano en 151, y 93 los vuelve a coger
   quien los soltó. Si ese ir y venir es lo que le cuesta la posición a APRENDE no está medido: haría falta un banco o un brazo que lo quite (por
   ejemplo, APRENDE sin regalo del botiquín) y ver si P6 se cierra.
4. **La curiosidad no se apaga.** Con la ignorancia en 0,05 APRENDE pasa más tiempo yendo a por botiquines que el día 1, y casi la mitad de sus
   muertes por rival llegan yendo a por uno. Aquí pesan a la vez la curiosidad (pieza F) y las ganas (pieza C, que crecen con la creencia); separarlas pide un banco.
5. **BORRADO y APRENDE no llevaban el mismo `descubre_P7.py`** (6 ventanas afectadas en BORRADO). Para el próximo campo: las imágenes fijas se hornean después del freno, o el freno no toca código.
6. **El día 1 no es un control emparejado.** La misma semilla no da el mismo mundo desde el tic 482; "emparejado por semilla" quiere decir mismo mapa, no misma partida.

## Privacidad

- Los JSON de respuesta de la plataforma se guardan ya sin correo: `privado_P7.sin_correos` en `lanza_P7_10.py` (y en los lanzadores que vengan).
- Antes de cada push a gemv-coworld: `cantera/paper6/taller/revisa_subida.py` busca correos, claves y rutas personales en todas las líneas nuevas
  que se suben (no solo en la lista del taller); si encuentra algo, sale con error y el push no se hace. Queda escrito en `CLAUDE.md`.
- La historia del repositorio no se ha reescrito: los JSON de `P7_10_res/` y de pasos anteriores ya subidos siguen llevando el correo de la cuenta.

## Archivos

| archivo | qué es |
|---|---|
| `analiza_P7_11.py` → `P7_11_vidas.json`, `P7_11_dia1.json` | lectura de los 320 diarios: usos, regalos y su destino, el tiempo, la muerte; el día 1 tic a tic |
| `banco_P7_11.py` → `P7_11_banco_dia1.json` | réplica de los 8 diarios del día 1 con los interruptores de APRENDE y de BORRADO |
| `banco_P7_11b.py` → `P7_11_filas.json` | réplica de las 254 vidas con algún uso o regalo: las filas de cada candidato en esos tics |
| `privado_P7.py`, `cantera/paper6/taller/revisa_subida.py` | quitar correos al guardar; comprobación previa al push |
| `escribe_informe_P7_11.py`, `informe_P7_11.md` | este informe |
