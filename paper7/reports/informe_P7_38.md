# P7-38 · Importancia contra lo que habría pasado sin la prueba

*10-oct-2026. Banco, coste cero: plataforma 0 créditos (acumulado del siete 710; disponibles el 10-oct, dato de Manel: 496 de 1.000, +71/día); consola 0 USD.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar; nada cambia en el campo. Sello `SELLO_P7_38.md` (commit
`4e284fc`, antes de calcular; dos añadidos declarados antes de calcular). Scripts: `contrafactual_P7_38.py` (= `e0ca43c6bfe7eba9a9b4635b38fb415e`, la pieza, solo banco),
`banco_P7_38.py` (`--cadena` → `P7_38_cadena.json`, `P7_38_res/cuaderno_A_*.json`; `--momentos` → `P7_38_momentos.json`), `cuaderno_P7_38.py` → `P7_38_cuadernos.json`,
`escribe_informe_P7_38.py` (este informe; ninguna cifra a mano).*

## El sello, de una vez

| | criterio | resultado | pasa |
|---|---|---|---|
| I1 | importancia de lo inútil ≤ 0,3 × la del botiquín | mediana red + camuflaje 0,0635; botiquín 0,2086 (0,3 × = 0,0626) | NO |
| I2 | «no hizo nada» ≤ 0,02 | mediana 0,0589 (60 recuerdos; 24 en 0) | NO |
| I3 | lo inútil manda ≤ 40 de 80 cierres y ≤ 20 % de los días 15-20 | 76 de 80; días 15-20: 24 de 24 (100,0 %) | NO |
| I4 | en los 71 momentos, `coger` lo inútil gana en ≤ 24 | 60 de 71 (lo demás: `ir_curioso` 11) | NO |
| I5 | la creencia de lo útil no se aparta más de 0,10 de P7-37 | mayor diferencia 0,8186 | NO |

## Sección 1 · La importancia contrafactual

Cadena honesta (cada criatura, sus 20 días; el cuaderno y las pistas del pasado viajan): 957607 decisiones iguales al diario · 54911 distintas (la réplica lleva la curiosidad A;
lazo abierto). Recuerdos tasados contra ventanas de referencia: 249 (de ellos 13 con referencia de cualquier situación por faltar 5 en la parecida); sin referencia: 2.

| cosa | recuerdos (día 20, sin cortes) | sin referencia (día 1) | con referencia de cualquier situación | ventanas de referencia (cuartiles) | importancia P7-33: cuartil 1 · mediana · cuartil 3 | importancia contrafactual: cuartil 1 · mediana · cuartil 3 | en 0 |
|---|---:|---:|---:|---|---|---|---:|
| botiquin | 67 | 0 | 4 | 36 · 80 · 2.029 | 0,1323 · 0,2616 · 0,4221 | 0,0729 · 0,2086 · 0,3649 | 10 |
| racion | 121 | 0 | 8 | 17 · 60 · 1.011 | 0,0538 · 0,0972 · 0,1590 | 0,0000 · 0,0215 · 0,1243 | 57 |
| red | 31 | 1 | 0 | 1.432 · 3.529 · 5.110 | 0,0021 · 0,0834 · 0,2997 | 0,0000 · 0,0602 · 0,2693 | 12 |
| camuflaje | 32 | 1 | 1 | 1.488 · 3.503 · 5.117 | 0,0317 · 0,0990 · 0,2882 | 0,0000 · 0,0674 · 0,2389 | 12 |

«No hizo nada» (recuerdos de red y camuflaje con |efecto en el cuerpo| ≤ 1): 60 recuerdos; importancia de P7-33 0,0077 · 0,0891 · 0,2909 (cuartiles) → contrafactual
0,0000 · 0,0589 · 0,2573; 24 de 60 en 0 exacto.

## Sección 2 · La curiosidad por clase, día a día

Importancia esperada = (1 + Σ importancias) / (1 + N) con el neutro como un recuerdo de importancia 1; curiosidad A = ignorancia × importancia esperada.

| criatura | día | botiquin: ignorancia · importancia esperada · curiosidad A · creencia A (P7-37) | racion: ignorancia · importancia esperada · curiosidad A · creencia A (P7-37) | red: ignorancia · importancia esperada · curiosidad A · creencia A (P7-37) | camuflaje: ignorancia · importancia esperada · curiosidad A · creencia A (P7-37) |
|---|---|---|---|---|---|
| s1 a10 | 5 | 0,088 · 0,268 · 0,024 · 12,9 (12,7) | 0,123 · 0,152 · 0,019 · 5,8 (5,8) | 0,352 · 0,343 · 0,121 · 0,0 (0,0) | 0,345 · 0,423 · 0,146 · 0,0 (0,0) |
| s1 a10 | 10 | 0,049 · 0,187 · 0,009 · 11,1 (11,0) | 0,057 · 0,102 · 0,006 · 5,7 (5,7) | 0,225 · 0,260 · 0,059 · 0,0 (0,0) | 0,213 · 0,356 · 0,076 · 0,0 (0,0) |
| s1 a10 | 15 | 0,028 · 0,198 · 0,005 · 35,6 (35,5) | 0,057 · 0,092 · 0,005 · 8,3 (8,4) | 0,147 · 0,199 · 0,029 · 0,0 (0,0) | 0,174 · 0,262 · 0,045 · 0,0 (0,0) |
| s1 a10 | 20 | 0,021 · 0,270 · 0,006 · 38,3 (38,3) | 0,038 · 0,083 · 0,003 · 11,1 (11,2) | 0,140 · 0,163 · 0,023 · 0,0 (0,0) | 0,111 · 0,234 · 0,026 · 0,0 (0,0) |
| s1 a11 | 5 | 0,169 · 0,283 · 0,048 · 15,7 (15,7) | 0,077 · 0,151 · 0,012 · 8,9 (8,9) | 0,219 · 0,491 · 0,107 · 0,0 (0,0) | 0,508 · 0,536 · 0,272 · 0,0 (0,0) |
| s1 a11 | 10 | 0,068 · 0,355 · 0,024 · 31,3 (31,6) | 0,053 · 0,141 · 0,007 · 13,1 (13,1) | 0,266 · 0,491 · 0,131 · 0,0 (0,0) | 0,268 · 0,289 · 0,077 · 0,0 (0,0) |
| s1 a11 | 15 | 0,046 · 0,389 · 0,018 · 36,4 (36,5) | 0,046 · 0,135 · 0,006 · 13,2 (13,2) | 0,204 · 0,337 · 0,069 · 0,0 (0,0) | 0,203 · 0,193 · 0,039 · 0,0 (0,0) |
| s1 a11 | 20 | 0,034 · 0,327 · 0,011 · 33,7 (33,8) | 0,053 · 0,128 · 0,007 · 12,9 (13,0) | 0,158 · 0,321 · 0,051 · 3,1 (3,3) | 0,201 · 0,165 · 0,033 · 0,0 (0,0) |
| s2 a10 | 5 | 0,078 · 0,390 · 0,030 · 36,3 (36,9) | 0,062 · 0,141 · 0,009 · 13,7 (13,8) | 1,000 · 1,000 · 1,000 · — (—) | 0,277 · 0,535 · 0,148 · 0,0 (0,0) |
| s2 a10 | 10 | 0,075 · 0,368 · 0,028 · 33,6 (34,3) | 0,059 · 0,171 · 0,010 · 13,6 (13,7) | 0,198 · 0,318 · 0,063 · 0,0 (0,0) | 0,201 · 0,368 · 0,074 · 0,0 (0,0) |
| s2 a10 | 15 | 0,086 · 0,363 · 0,031 · 36,4 (36,7) | 0,065 · 0,173 · 0,011 · 13,3 (13,4) | 0,165 · 0,227 · 0,038 · 0,0 (0,0) | 0,136 · 0,305 · 0,041 · 6,1 (6,4) |
| s2 a10 | 20 | 0,089 · 0,327 · 0,029 · 33,7 (34,1) | 0,056 · 0,138 · 0,008 · 12,9 (12,9) | 0,117 · 0,253 · 0,030 · 0,0 (0,0) | 0,124 · 0,274 · 0,034 · 4,3 (4,6) |
| s2 a11 | 5 | 0,166 · 0,509 · 0,085 · 11,7 (11,7) | 0,114 · 0,440 · 0,050 · 5,4 (5,6) | 0,339 · 0,333 · 0,113 · 0,0 (0,0) | 0,513 · 0,500 · 0,256 · 0,0 (0,0) |
| s2 a11 | 10 | 0,059 · 0,305 · 0,018 · 22,9 (22,8) | 0,082 · 0,284 · 0,023 · 6,7 (6,8) | 0,213 · 0,264 · 0,056 · 0,0 (0,0) | 0,282 · 0,250 · 0,070 · 0,0 (0,0) |
| s2 a11 | 15 | 0,031 · 0,295 · 0,009 · 24,9 (24,8) | 0,057 · 0,199 · 0,011 · 12,8 (12,8) | 0,209 · 0,241 · 0,051 · 4,2 (4,6) | 0,257 · 0,213 · 0,055 · 0,0 (0,0) |
| s2 a11 | 20 | 0,036 · 0,293 · 0,011 · 23,7 (23,6) | 0,044 · 0,154 · 0,007 · 13,8 (13,8) | 0,197 · 0,245 · 0,048 · 3,1 (3,4) | 0,162 · 0,169 · 0,027 · 0,0 (0,0) |

| criatura | la clase que más llama, día 1 → 20 | deja de mandar lo inútil el día |
|---|---|---|
| s1 a10 | N N N N C C C C C C C C C C C C C C C C | no llega |
| s1 a11 | N C C C C C C C C N N N N N N N N N N N | no llega |
| s2 a10 | N N N N N N N N C C N N N N C C N N C C | no llega |
| s2 a11 | R R R B C N N C C C C C C C C N N N N N | no llega |

(B botiquín, R ración, N red, C camuflaje; «deja de mandar lo inútil» = el primer día a partir del cual ya no manda ningún día; «no llega» si manda el día 20.)

## Sección 3 · Los 71 momentos, en banco (lectura A)

Las 80 vidas con el cuaderno A del día anterior: fidelidad 957660 igual · 54858 difiere. En los 71 momentos de cogida, `coger` gana en 60; en las 63 aperturas de prueba, curiosidad A
mediana: red 0,077, camuflaje 0,077, botiquín 0,028, ración 0,011; la clase que más llama es red o camuflaje en 123 de 134 momentos.

## Sección 4 · A+M, solo para que Manel decida

A con la curiosidad de lo inútil atenuada por la cautela por distancia (P7-26) y la mirada de científico solo entre situaciones sin peligro. De las 63 pruebas reales
(aperturas), 13 caen en peligro (`peligro_de`); de los 71 momentos de cogida, 17. En los 30 momentos en peligro la cautela habría dejado la curiosidad
atenuada (0 < cautela < 1): 19, apagada (0): 11. Con A × cautela, la clase que más llama es red o camuflaje en 97 de 134 momentos (A sola: 123).

| cosa | preferida entre todas las situaciones (C5) | preferida solo entre situaciones sin peligro (A+M) |
|---|---|---|
| red | empunar · fuera · golpeado 117, coger · dentro · sin golpe 17 | empunar · dentro · sin golpe 117, coger · dentro · sin golpe 17 |
| camuflaje | ponerse · fuera · golpeado 105, ponerse · fuera · sin golpe 16, coger · dentro · sin golpe 13 | ponerse · dentro · sin golpe 121, coger · dentro · sin golpe 13 |

## Lectura

Ninguno de los cinco criterios pasa. (i) **La importancia contrafactual sí baja, pero baja para todo**: red y camuflaje de 0,083 / 0,099 a 0,060 / 0,067 (mediana), el botiquín de 0,262 a 0,209, la ración de 0,097 a 0,021 (57 de 121 raciones en 0: comer, contra lo que habría pasado sin comer, casi no mueve el malestar en su ventana). I1 se queda a 0,0009 del umbral: el cociente inútil/botiquín pasa de 0,35 a 0,30. (ii) **«No hizo nada» no se queda en 0**: 24 de 60 sí (su cambio de malestar cabe en 1 desviación típica de las ventanas sin prueba), los otros 36 se salen de esa banda; el dominio que lo lleva es cero 12, cuerpo 9, recursos 6, vinculo 4 en la red y cero 12, recursos 9, cuerpo 8, vinculo 3 en el camuflaje. Las ventanas de referencia son muchas (3.529 de mediana para la red) y por eso su desviación típica es estrecha: en 10 s de calma el malestar de fondo casi no se mueve, y lo que se mueve durante la prueba (la criatura acaba de coger la cosa, la lleva, camina hacia otra) parece importar. (iii) **Lo inútil sigue mandando** (76 de 80; días 15-20, 24 de 24; ninguna criatura deja de tenerlo como lo que más llama): con el neutro contando como UN recuerdo de importancia 1 y 6-10 recuerdos de red o camuflaje de importancia ~0,06, la importancia esperada de lo inútil el día 20 es 0,16-0,32, la del botiquín 0,27-0,33 y la de la ración 0,08-0,15; multiplicada por una ignorancia de 0,11-0,20 (inútil) frente a 0,02-0,09 (útil), lo inútil gana siempre. El neutro es un recuerdo entre pocos, y pocos recuerdos de poco no lo tapan. (iv) **`coger` sigue en 60 de 71**: la cosa a los pies y la curiosidad que se alivia al tenerla (P7-36). (v) **La creencia de lo útil se mueve** (mayor diferencia 0,82, mediana 0,085, 58 de 153 cierres por encima de 0,10): no por el método de la curiosidad, sino porque la intensidad del recuerdo va atada a la importancia (1 + importancia, como se decidió) y la contrafactual cambia los pesos con que se promedian los efectos; la mayor diferencia está en s2 a10 el día 2 (botiquín 31,30 → 30,48). Si I5 quiere decir «la creencia no cambia», la intensidad no puede ir atada a esta importancia; si quiere decir «lo útil sigue sabiéndose», se cumple: la mayor diferencia en los cuadernos del día 20 es 0,409.

**A+M.** Con la cautela, la clase que más llama sigue siendo red o camuflaje en 97 de 134 momentos (A: 123); de los 30 momentos en peligro, la cautela apaga 11 y atenúa 19; 13 de las 63 pruebas reales y 17 de los 71 momentos de cogida caen en peligro. La mirada de científico sin peligro lleva la siguiente prueba a la forma nueva en la situación de siempre (empuñar la red dentro y sin golpe, ponerse el camuflaje dentro y sin golpe).

## Lo que se desprende (propuestas, no decisiones)

1. La ventana de referencia mide el fondo, pero lo que mueve el malestar en la prueba es la prueba misma como acto (coger, llevar, caminar) y la propia curiosidad que se
   alivia (`R-CURIOSIDAD` reparte el 80 % en recursos): medir la importancia sin las filas de la curiosidad (y sin el acto de coger) la dejaría en lo que la cosa hace.
2. El neutro como UN recuerdo de importancia 1 solo se apaga con muchos recuerdos: con los 6-10 de red o camuflaje la importancia esperada de lo inútil queda en
   0,16-0,32. O el neutro pesa menos (p. ej. 1/N), o la importancia esperada es la mediana, o lo inútil se declara con N «no hizo nada» seguidos.
3. I5, tal como está escrito, no puede pasar con la intensidad atada a la importancia; conviene decidir cuál de las dos cosas se quiere.
