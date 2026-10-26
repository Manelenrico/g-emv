# P7-36 · Por qué coge lo inútil y por qué no lo recuerda más débil

*10-oct-2026. Coste cero: sin partidas, sin llamadas (plataforma 0; consola 0; acumulado del siete 64,7168 USD de plataforma, sin cambio). `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar; todo posterior al sello de P7-34; nada se juega. Scripts: `analiza_P7_36.py`
→ `P7_36_cogidas.json` (los diarios de P7-34), `empate_P7_36.py` + `banco_P7_36.py` → `P7_36_banco.json` (las 80 vidas de APRENDE replicadas, una por proceso, sin y con
la regla), `cuaderno_P7_36.py` → `P7_36_cuadernos.json` (los 80 cuadernos de las 4 criaturas), `escribe_informe_P7_36.py` (este informe; ninguna cifra a mano).
md5: `empate_P7_36.py` = `b13c79dee06259ba38c96add0e4dcdb7`, `cuaderno_P7_36.py` = `5be51b28d1185e605e7330f131b66b10`.*

## Sección 1 · Por qué coge lo inútil

**En los diarios.** Cada entrada de una red o un camuflaje en el zurrón, la mano o el cuerpo, y la decisión del tic anterior (la acción de t−1 se ve en la obs de t):

| brazo | cogidas de red + camuflaje | gana `coger` | empate exacto con `noop` (gana por N2a) | paisaje degenerado (≤ 1e-3) | `coger` gana a `noop` por: mín · cuartil 1 · mediana · cuartil 3 · máx | gana por menos de 0,01 | empata exactamente con otro candidato |
|---|---:|---:|---:|---:|---|---:|---|
| TECHO | 46 | 46 | 26 | 23 | 0,0000 · 0,0000 · 0,0000 · 0,0748 · 0,0832 | 26 | noop 26 |
| BORRADO | 61 | 61 | 0 | 0 | 0,0033 · 0,0114 · 0,0202 · 0,0213 · 0,0214 | 2 | ir_curioso 24, usar_botiquin 1 |
| APRENDE | 71 | 71 | 4 | 2 | 0,0000 · 0,0030 · 0,0044 · 0,0073 · 0,0215 | 58 | ir_curioso 8, noop 4 |

Las 71 cogidas de APRENDE son todas decisiones `coger` (intención `pickup`); ninguna llega por `ir_curioso` ni por hacer sitio. Solo 4 son un
empate exacto con `noop` (el que `noop` no puede ganar, N2a del desempate de la casa); en las demás `coger` gana a `noop` por una diferencia pequeña pero real
(mediana 0,0044; 58 de 71 por menos de 0,01). En 8 cogidas `coger` empata exactamente con `ir_curioso`
(la foto de ir hacia la cosa y la de cogerla valen lo mismo: coger gana por menos pasos, N2b). TECHO, al contrario, coge por empate exacto con `noop` en 26 de
46 (nace sabiendo: la red y el camuflaje no le cambian ninguna fila, y `noop` no puede ganar); BORRADO gana a `noop` por 0,0202 de mediana, sin
ningún empate.

**Qué fila hace ganar a `coger`.** En la réplica sin regla (fiel al diario: 1012517 decisiones iguales · 1 distintas en las 80 vidas), la foto de `coger` y
la de `noop` en esos tics solo se distinguen en `R-CURIOSIDAD` (2 de 71 cogidas; p. ej. 0,0093 con coger frente a 0,0120 con noop), `R-CARENCIA` (1 de 71 cogidas; p. ej. 0,8359 con coger frente a 0,8371 con noop):
la fila de la curiosidad de clase (`R-CURIOSIDAD`, ignorancia × alivio, P7-33 punto 4: tener la cosa alivia la mitad). Las ganas (k) de red y camuflaje son 0 y no entran en
`W`; lo que coge la red es la curiosidad de clase, que se alivia al tenerla, y que vale ignorancia × alivio: con la ignorancia que lo inútil tiene en la regla vieja (tabla de la sección 2) basta para esa diferencia.

**En banco, con la regla «en un empate, no se coge»** (`empate_P7_36.desempate_sin_coger`, la simétrica de la de soltar de P7-10/P7-14b: si `coger` comparte el mínimo con otro
candidato, o el paisaje es degenerado, `coger` sale del desempate; mismo criterio, ningún número nuevo). Réplica de las 80 vidas: la regla entra 325 veces;
fidelidad 1012188 iguales · 330 distintas. De las 71 cogidas de red y camuflaje del diario, **desaparecen 12** (la réplica elige
`ir_curioso` 8, `noop` 4); las otras 59 siguen siendo `coger`, porque no son un empate: `coger` gana de verdad por la curiosidad de
clase. Y cambian **318 decisiones más** en 70 vidas fuera de esas cogidas (coger → noop: 298, coger → ir_curioso: 10, coger → empunar_blowgun: 4, empunar_blowgun → noop: 4, coger → atacar_S: 1, ir_curioso → ir_botin: 1): la regla toca todo `coger`,
también el del botiquín y la ración cuando empatan con `noop` o con el ir hacia ellos. Lo que quita la regla es poco; lo que coge lo inútil no es el empate, es la curiosidad.

## Sección 2 · La regla de la intensidad, como la quiso Manel

Regla vieja (`cuaderno_P7.apunta`): intensidad = 1 + min(1, S / E), S = |imp_cuerpo| + |imp_recursos| + |imp_vínculo|, E = 1,5. Regla nueva (mesa): intensidad =
max(0,05, min(1, S / E)): sin la base de 1, suelo 0,05 (el tope min(1, ·) es el de la regla vieja, declarado). El peso de un recuerdo es intensidad × 0,95^(días); el
recuerdo neutro (peso 1, efecto 0) no cambia. Recalculado sobre los 80 cuadernos (4 criaturas × 20 días) sin jugar. Lo que hay en S:

| cosa | recuerdos (sin cortes, 4 cuadernos del día 20) | S = Σ|importancia|: mediana · cuartil 1 · cuartil 3 | intensidad vieja (mediana) | intensidad nueva (mediana) | en el suelo 0,05 |
|---|---:|---|---:|---:|---:|
| botiquin | 67 | 0,409 · 0,199 · 0,634 | 1,273 | 0,273 | 1 |
| racion | 121 | 0,145 · 0,081 · 0,238 | 1,097 | 0,097 | 24 |
| red | 31 | 0,129 · 0,007 · 0,454 | 1,086 | 0,086 | 12 |
| camuflaje | 32 | 0,148 · 0,021 · 0,431 | 1,099 | 0,099 | 10 |

Día a día (cierre de los días 5, 10, 15 y 20; peso total de los recuerdos, ignorancia = 1 / (1 + peso), creencia dentro del círculo en el cuerpo, sin cortes):

| criatura | día | botiquin: peso vieja → nueva · ignorancia vieja → nueva · creencia vieja → nueva | racion: peso vieja → nueva · ignorancia vieja → nueva · creencia vieja → nueva | red: peso vieja → nueva · ignorancia vieja → nueva · creencia vieja → nueva | camuflaje: peso vieja → nueva · ignorancia vieja → nueva · creencia vieja → nueva |
|---|---|---|---|---|---|
| s1 a10 | 5 | 10,46 → 1,55 · 0,09 → 0,39 · 12,7 → 8,7 | 7,37 → 0,64 · 0,12 → 0,61 · 5,8 → 2,6 | 1,84 → 0,09 · 0,35 → 0,92 · 0,0 → 0,0 | 1,94 → 0,30 · 0,34 → 0,77 · 0,0 → 0,0 |
| s1 a10 | 10 | 19,79 → 2,94 · 0,05 → 0,25 · 11,0 → 7,9 | 17,62 → 1,93 · 0,05 → 0,34 · 5,7 → 2,9 | 3,47 → 0,38 · 0,22 → 0,72 · 0,0 → 0,0 | 3,87 → 0,83 · 0,21 → 0,55 · 0,0 → 0,0 |
| s1 a10 | 15 | 35,51 → 6,41 · 0,03 → 0,13 · 35,5 → 23,4 | 17,46 → 1,89 · 0,05 → 0,35 · 8,4 → 4,2 | 5,89 → 0,70 · 0,15 → 0,59 · 0,0 → 0,0 | 5,00 → 0,80 · 0,17 → 0,56 · 0,0 → 0,0 |
| s1 a10 | 20 | 47,48 → 9,89 · 0,02 → 0,09 · 38,3 → 27,2 | 26,79 → 2,99 · 0,04 → 0,25 · 11,2 → 6,2 | 6,25 → 0,64 · 0,14 → 0,61 · 0,0 → 0,0 | 8,29 → 1,37 · 0,11 → 0,42 · 0,0 → 0,0 |
| s1 a11 | 5 | 5,08 → 0,74 · 0,16 → 0,57 · 15,7 → 8,5 | 12,07 → 1,17 · 0,08 → 0,46 · 8,9 → 2,3 | 3,58 → 0,91 · 0,22 → 0,52 · 0,0 → 0,0 | 0,99 → 0,09 · 0,50 → 0,92 · 0,0 → 0,0 |
| s1 a11 | 10 | 13,89 → 3,25 · 0,07 → 0,24 · 31,6 → 23,9 | 18,14 → 2,10 · 0,05 → 0,32 · 13,1 → 8,0 | 2,77 → 0,70 · 0,27 → 0,59 · 0,0 → 0,0 | 2,78 → 0,22 · 0,26 → 0,82 · 0,0 → 0,0 |
| s1 a11 | 15 | 21,00 → 5,29 · 0,05 → 0,16 · 36,5 → 27,2 | 21,29 → 2,48 · 0,04 → 0,29 · 13,2 → 8,7 | 3,94 → 0,66 · 0,20 → 0,60 · 0,0 → 0,0 | 3,97 → 0,26 · 0,20 → 0,79 · 0,0 → 0,0 |
| s1 a11 | 20 | 29,47 → 6,34 · 0,03 → 0,14 · 33,8 → 24,8 | 18,29 → 2,07 · 0,05 → 0,33 · 12,9 → 8,1 | 5,42 → 1,08 · 0,16 → 0,48 · 3,3 → 1,9 | 4,05 → 0,25 · 0,20 → 0,80 · 0,0 → 0,0 |
| s2 a10 | 5 | 12,08 → 3,09 · 0,08 → 0,24 · 36,9 → 25,7 | 15,47 → 1,64 · 0,06 → 0,38 · 13,8 → 8,7 | 0,00 → 0,00 · 1,00 → 1,00 · — → — | 2,76 → 0,76 · 0,27 → 0,57 · 0,0 → 0,0 |
| s2 a10 | 10 | 12,58 → 2,79 · 0,07 → 0,26 · 34,3 → 22,5 | 16,25 → 2,31 · 0,06 → 0,30 · 13,7 → 9,2 | 4,26 → 0,73 · 0,19 → 0,58 · 0,0 → 0,0 | 4,21 → 0,91 · 0,19 → 0,52 · 0,0 → 0,0 |
| s2 a10 | 15 | 10,82 → 2,43 · 0,08 → 0,29 · 36,7 → 23,7 | 14,56 → 2,02 · 0,06 → 0,33 · 13,3 → 8,4 | 5,23 → 0,66 · 0,16 → 0,60 · 0,0 → 0,0 | 6,70 → 1,42 · 0,13 → 0,41 · 6,4 → 3,5 |
| s2 a10 | 20 | 10,61 → 2,31 · 0,09 → 0,30 · 34,1 → 20,9 | 17,39 → 2,11 · 0,05 → 0,32 · 12,9 → 7,7 | 7,75 → 1,45 · 0,11 → 0,41 · 0,0 → 0,0 | 7,40 → 1,49 · 0,12 → 0,40 · 4,6 → 2,6 |
| s2 a11 | 5 | 5,11 → 0,73 · 0,16 → 0,58 · 11,6 → 6,9 | 7,85 → 2,12 · 0,11 → 0,32 · 5,6 → 2,3 | 1,95 → 0,10 · 0,34 → 0,91 · 0,0 → 0,0 | 0,96 → 0,05 · 0,51 → 0,95 · 0,0 → 0,0 |
| s2 a11 | 10 | 16,59 → 3,47 · 0,06 → 0,22 · 22,8 → 19,7 | 11,50 → 2,35 · 0,08 → 0,30 · 6,8 → 4,1 | 3,79 → 0,50 · 0,21 → 0,67 · 0,0 → 0,0 | 2,56 → 0,13 · 0,28 → 0,89 · 0,0 → 0,0 |
| s2 a11 | 15 | 32,22 → 6,97 · 0,03 → 0,13 · 24,8 → 23,3 | 16,86 → 2,66 · 0,06 → 0,27 · 12,8 → 7,6 | 3,98 → 0,62 · 0,20 → 0,62 · 4,6 → 3,2 | 2,92 → 0,18 · 0,26 → 0,85 · 0,0 → 0,0 |
| s2 a11 | 20 | 27,07 → 5,90 · 0,04 → 0,14 · 23,6 → 21,5 | 22,49 → 3,04 · 0,04 → 0,25 · 13,8 → 9,1 | 4,24 → 0,74 · 0,19 → 0,58 · 3,4 → 2,3 | 5,27 → 0,53 · 0,16 → 0,66 · 0,0 → 0,0 |

Lectura. (i) **Lo inútil se debilita, pero no se apaga**: el día 20 el peso de la red pasa de 4,24-7,75 a 0,64-1,45 y el del camuflaje de
4,05-8,29 a 0,25-1,49; su ignorancia sube de 0,11-0,20 a 0,40-0,80. No llega a 1 porque la criatura
sigue probándolas (60 pruebas en 20 días entre las 4) y cada prueba vuelve a sumar su poco. (ii) **Lo útil también se debilita**: el botiquín pasa de peso
10,6-47,5 a 2,3-9,9 (ignorancia 0,02-0,09 → 0,09-0,30), la ración de 17,4-26,8 a
2,1-3,0: la importancia (el cambio del malestar en la ventana) es pequeña para todo, también para curar (S mediana 0,409 en el botiquín, 0,145 en la ración, 0,129 en la red
y 0,148 en el camuflaje: curar mueve el malestar 2,8 veces más que ponerse un camuflaje, y comer lo mismo que una red; la base de 1 de la regla vieja borraba esa diferencia, y la regla nueva la deja ver, pero es una diferencia de 3 a 1, no de 10 a 1). (iii) **La creencia de lo útil cambia, y a peor**: la del botiquín dentro el día 20 pasa de
38,3, 33,8, 34,1, 23,6 a 27,2, 24,8, 20,9, 21,5; la de la ración de 11,2, 12,9, 12,9, 13,8 a 6,2, 8,1, 7,7, 9,1. La causa es el recuerdo neutro: pesa 1 y no se apaga, y la media
con el neutro en el centro tira hacia 0 tanto más cuanto menos pesan los recuerdos vividos (con intensidad mediana 0,273 en el botiquín, el neutro pesa como 4 recuerdos
de curar). La regla nueva, tal cual, hace que el botiquín «cure» 21-27 en vez de 24-38 sin que la criatura haya visto nada distinto.

## Sección 3 · Cuándo habría vuelto a despertar la curiosidad por lo inútil

La curiosidad de clase llama con ignorancia × alivio y manda `ir_curioso` la clase que más llama (`nace_P7_33._cands`). Con la regla vieja, la ignorancia de la red y del
camuflaje YA es la mayor de las cuatro casi todos los días (el día 20, regla vieja: lo útil 0,02-0,09 con 16-55 recuerdos; lo inútil 0,11-0,20 con 6-10):
lo inútil manda la curiosidad en 77 de 80 cierres de día (criatura × día) con la regla vieja y en 77 de 80 con la nueva. Por eso APRENDE coge más redes
que TECHO: no le hace falta «despertar», nunca se durmió; lo que la frena es solo que la curiosidad se alivia a medias al tenerla y que el camino hasta una red compite
con todo lo demás.

| criatura | cosa | pruebas reales (días) | regla vieja: tras cada prueba, vuelve a ser la clase que más llama el día… · pasa de 0,5 el día… | regla nueva: ídem |
|---|---|---|---|---|
| s1 a10 | red | 1, 5, 6, 9, 13, 14, 15, 16 | d1 → 2 · 2; d5 → 6 · no; d6 → 7 · no; d9 → 10 · no; d13 → 14 · no; d14 → 20 · no; d15 → 20 · no; d16 → 20 · no | d1 → 2 · 2; d5 → 6 · 6; d6 → 7 · 7; d9 → 10 · 10; d13 → 14 · 14; d14 → 15 · 15; d15 → 16 · 16; d16 → 17 · 17 |
| s1 a10 | camuflaje | 1, 2, 6, 9, 13, 14, 16, 17, 20 | d1 → 15 · no; d2 → 15 · no; d6 → 15 · no; d9 → 15 · no; d13 → 15 · no; d14 → 15 · no; d16 → 17 · no; d17 → 18 · no; d20 → no · no | d1 → no · 2; d2 → no · 3; d6 → no · 7; d9 → no · 10; d13 → no · 14; d14 → no · 15; d16 → no · no; d17 → no · no; d20 → no · no |
| s1 a11 | red | 2, 3, 4, 11, 13, 17, 19 | d2 → 10 · no; d3 → 10 · no; d4 → 10 · no; d11 → 12 · no; d13 → 15 · no; d17 → no · no; d19 → no · no | d2 → no · 3; d3 → no · 4; d4 → no · 5; d11 → no · 12; d13 → no · 14; d17 → no · 18; d19 → no · no |
| s1 a11 | camuflaje | 3, 8, 10, 11, 15, 19 | d3 → 4 · 5; d8 → 9 · no; d10 → 13 · no; d11 → 13 · no; d15 → 17 · no; d19 → 20 · no | d3 → 4 · 4; d8 → 9 · 9; d10 → 11 · 11; d11 → 12 · 12; d15 → 16 · 16; d19 → 20 · 20 |
| s2 a10 | red | 6, 7, 8, 9, 13, 15, 16, 19, 20 | d6 → 7 · no; d7 → 8 · no; d8 → 11 · no; d9 → 11 · no; d13 → 14 · no; d15 → 17 · no; d16 → 17 · no; d19 → no · no; d20 → no · no | d6 → 7 · 7; d7 → 8 · 8; d8 → 9 · 9; d9 → 10 · 10; d13 → 14 · 14; d15 → 16 · 18; d16 → 17 · 18; d19 → 20 · no; d20 → no · no |
| s2 a10 | camuflaje | 5, 7, 8, 11, 13, 15, 17, 20 | d5 → 9 · no; d7 → 9 · no; d8 → 9 · no; d11 → 16 · no; d13 → 16 · no; d15 → 16 · no; d17 → 19 · no; d20 → no · no | d5 → 19 · 6; d7 → 19 · 9; d8 → 19 · 9; d11 → 19 · no; d13 → 19 · no; d15 → 19 · no; d17 → 19 · no; d20 → no · no |
| s2 a11 | red | 4, 5, 8, 10, 11, 18 | d4 → 6 · no; d5 → 6 · no; d8 → 19 · no; d10 → 19 · no; d11 → 19 · no; d18 → 19 · no | d4 → 6 · 5; d5 → 6 · 6; d8 → no · 9; d10 → no · 11; d11 → no · 12; d18 → no · 19 |
| s2 a11 | camuflaje | 4, 6, 10, 12, 16, 18, 19 | d4 → 5 · 5; d6 → 8 · no; d10 → 11 · no; d12 → 13 · no; d16 → 17 · no; d18 → no · no; d19 → no · no | d4 → 5 · 5; d6 → 8 · 7; d10 → 11 · 11; d12 → 13 · 13; d16 → 17 · 17; d18 → 19 · 19; d19 → 20 · 20 |

Tras cada prueba, lo inútil vuelve a ser la clase que más llama al día siguiente en 24 de 60 pruebas con la regla vieja y en 29 de 60 con la nueva; su ignorancia vuelve a
pasar de 0,5 en 3 de 60 con la vieja y en 49 de 60 con la nueva. Las dos repruebas que contó I4 (s1 a11 red día 11; s2 a11 red día 18) no son despertares de una curiosidad
dormida: en los dos casos la red llevaba días siendo la clase que más llamaba (tabla), y lo que tardó fue encontrar una red en calma. Con la regla nueva habría llamado
más fuerte aún (ignorancia de la red el día 20: 0,61, 0,48, 0,41, 0,58 frente a 0,14, 0,16, 0,11, 0,19), es decir, más cogidas de lo inútil, no menos.

## Lo que se desprende (propuestas, no decisiones)

1. Bajar la intensidad sin tocar el neutro aplasta la creencia de lo útil: si la mesa quiere la regla nueva, el neutro tendría que pesar en la misma escala (p. ej. el
   suelo 0,05, o la intensidad media de lo vivido) o la creencia tendría que calcularse sin él para las ganas, como ya hace `con_neutro=False`.
2. El problema de «no deja de quererlo» no está en la intensidad del recuerdo sino en que la curiosidad de clase no lee lo aprendido: llama por ignorancia, y la
   ignorancia de una cosa que «no hace nada» se parece a la de una cosa nunca probada. Una curiosidad que descontara lo ya sabido (p. ej. ignorancia × (1 − |creencia
   firme| / esperanza) o que se apagara con N recuerdos de «no hizo nada») apagaría la red sin tocar el botiquín. Es un mecanismo nuevo: se propone, no se hace.
3. La regla «en un empate, no se coge» quita 12 de 71 cogidas de lo inútil y, de paso, 298 cogidas de otras cosas (`coger` es un solo candidato: coge lo que pisa, botiquín, ración o arma): no es la palanca, y costaría más de lo que quita.
