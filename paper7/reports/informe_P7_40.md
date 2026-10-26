# P7-40 · Último banco antes del campo: la esperanza de clase y el miedo que calla el probar, no el mirar

*10-oct-2026. Banco, coste cero: plataforma 0 créditos (acumulado del siete 710; disponibles el 10-oct, dato de Manel: 496 de 1.000, +71/día); consola 0 USD.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar. Sello `SELLO_P7_40.md` (commit `b7d11da`, antes de calcular).
Scripts: `filo_P7_40.py` (= `facca1443a1bcde0cc41990cf2de4c74`, la pieza, sobre B1 de P7-39: `efecto_P7_39` + `contrafactual_P7_38` sin contrafactual), `banco_P7_40.py` (`--cadena` →
`P7_40_cadena.json`, `P7_40_res/cuaderno_P40_*.json`; `--momentos` → `P7_40_momentos.json`), `cuaderno_P7_40.py` → `P7_40_cuadernos.json`, `escribe_informe_P7_40.py` (este
informe; ninguna cifra a mano). Cadena honesta: 880844 decisiones iguales al diario · 131674 distintas; momentos: 868750 · 143768.*

## El sello, de una vez

| | criterio | resultado | pasa |
|---|---|---|---|
| I1 | inútil ≤ 0,3 × botiquín | 0,0085 frente a 0,0582 (botiquín 0,1941) | sí |
| I2 | «no hizo nada» ≤ 0,02 | 0,0056 (25 de 60 en 0) | sí |
| I3 | lo inútil manda ≤ 40 de 80 y ≤ 4 de 24 en d15-20 | 74 de 80; d15-20 24 de 24 | NO |
| I4 | `coger` lo inútil ≤ 24 de 71 | 62 de 71 (`ir_curioso` 9) | NO |
| I5 corregido | al día 20, \|c40 − real\| ≤ \|c37 − real\| + 0,10 (8 parejas) | s1 a10 botiquin: 11,15 frente a 11,71; s1 a10 racion: 3,76 frente a 3,77; s1 a11 botiquin: 16,31 frente a 16,22; s1 a11 racion: 2,08 frente a 2,05; s2 a10 botiquin: 15,72 frente a 15,91; s2 a10 racion: 2,12 frente a 2,05; s2 a11 botiquin: 26,48 frente a 26,40; s2 a11 racion: 1,23 frente a 1,22 | sí |
| I5 antiguo (informado) | \|c40 − c37\| ≤ 0,10 en los 80 cierres | máx 0,559 | NO |
| E1 | al filo del mañana: ≥ 60 % de lo visto en peligro y no probado manda en la siguiente calma | 127 de 260 apuntes evaluables (48,8 %; 177 con empate contados como cumplidos; 2 apuntes cuya cosa se probó antes del tic de calma, fuera) | NO |
| E2 | pruebas en peligro ≤ 13 de 63 | de las 13 aperturas reales en peligro, la réplica con miedo sigue abriendo 7 (+ 5 sin tic de cogida en los momentos) | sí |

P7-40 pasa 3 de I1-I5 (B1 de P7-39 con el I5 corregido: 2). **Regla final**: el campo va con **P7-40** (la que pase más de I1-I5; a igualdad, la que deje lo inútil mandando menos
cierres: P7-40 74 de 80, B1 76 de 80; a igualdad, B1), sin más bancos sobre lo inútil.

## Sección 1 · La importancia y los apuntes

| cosa | recuerdos (día 20) | importancia P7-33 (cuartiles) | importancia B1/P7-40 (cuartiles) | en 0 | apuntes (vistos en peligro, 4 criaturas × 20 días) | intensidad de los apuntes (cuartiles) |
|---|---:|---|---|---:|---:|---|
| botiquin | 67 | 0,1229 · 0,1941 · 0,3925 | 0,1229 · 0,1941 · 0,3925 | 0 | 1861 | 0,000 · 0,011 · 0,081 |
| racion | 121 | 0,0533 · 0,0902 · 0,1617 | 0,0533 · 0,0902 · 0,1617 | 0 | 1606 | 0,000 · 0,009 · 0,083 |
| red | 31 | 0,0000 · 0,0055 · 0,3323 | 0,0000 · 0,0055 · 0,3323 | 14 | 969 | 0,000 · 0,018 · 0,088 |
| camuflaje | 32 | 0,0000 · 0,0093 · 0,3081 | 0,0000 · 0,0093 · 0,3081 | 11 | 206 | 0,014 · 0,054 · 0,154 |

## Sección 2 · El punto de partida de cada clase, día a día

| criatura | día | botiquin: punto de partida (de clase) · importancia esperada · ignorancia · curiosidad | racion: punto de partida (de clase) · importancia esperada · ignorancia · curiosidad | red: punto de partida (de clase) · importancia esperada · ignorancia · curiosidad | camuflaje: punto de partida (de clase) · importancia esperada · ignorancia · curiosidad |
|---|---|---|---|---|---|
| s1 a10 | 1 | 0,234 (0,097) · 0,212 · 0,172 · 0,036 | 0,398 (0,100) · 0,150 · 0,187 · 0,028 | 0,000 (0,000) · 0,000 · 0,500 · 0,000 | 0,000 (0,000) · 0,000 · 0,500 · 0,000 |
| s1 a10 | 5 | 0,729 (0,083) · 0,246 · 0,088 · 0,022 | 1,000 (0,116) · 0,188 · 0,119 · 0,022 | 0,670 (0,162) · 0,223 · 0,355 · 0,079 | 0,430 (0,000) · 0,252 · 0,339 · 0,085 |
| s1 a10 | 10 | 1,000 (0,091) · 0,231 · 0,048 · 0,011 | 1,000 (0,131) · 0,159 · 0,054 · 0,009 | 1,000 (0,156) · 0,252 · 0,227 · 0,057 | 0,430 (0,000) · 0,213 · 0,221 · 0,047 |
| s1 a10 | 15 | 1,000 (0,091) · 0,238 · 0,028 · 0,006 | 1,000 (0,143) · 0,150 · 0,054 · 0,008 | 1,000 (0,003) · 0,196 · 0,147 · 0,029 | 0,721 (0,000) · 0,194 · 0,179 · 0,035 |
| s1 a10 | 20 | 1,000 (0,094) · 0,299 · 0,021 · 0,006 | 1,000 (0,146) · 0,143 · 0,036 · 0,005 | 1,000 (0,054) · 0,165 · 0,139 · 0,023 | 0,721 (0,000) · 0,179 · 0,114 · 0,020 |
| s1 a11 | 1 | 0,411 (0,056) · 0,273 · 0,300 · 0,082 | 0,406 (0,135) · 0,172 · 0,112 · 0,019 | 0,401 (0,096) · 0,401 · 1,000 · 0,401 | 0,389 (0,096) · 0,389 · 1,000 · 0,389 |
| s1 a11 | 5 | 0,725 (0,056) · 0,243 · 0,168 · 0,041 | 1,000 (0,102) · 0,166 · 0,076 · 0,013 | 0,457 (0,000) · 0,322 · 0,224 · 0,072 | 0,457 (0,387) · 0,228 · 0,526 · 0,120 |
| s1 a11 | 10 | 0,804 (0,077) · 0,350 · 0,068 · 0,024 | 1,000 (0,147) · 0,161 · 0,052 · 0,008 | 1,000 (0,011) · 0,458 · 0,272 · 0,124 | 0,523 (0,387) · 0,144 · 0,274 · 0,040 |
| s1 a11 | 15 | 1,000 (0,074) · 0,377 · 0,046 · 0,018 | 1,000 (0,159) · 0,147 · 0,045 · 0,007 | 1,000 (0,000) · 0,305 · 0,209 · 0,064 | 0,523 (0,005) · 0,096 · 0,205 · 0,020 |
| s1 a11 | 20 | 1,000 (0,075) · 0,332 · 0,034 · 0,011 | 1,000 (0,166) · 0,143 · 0,052 · 0,007 | 1,000 (0,005) · 0,304 · 0,159 · 0,049 | 0,523 (0,200) · 0,087 · 0,201 · 0,018 |
| s2 a10 | 1 | 0,680 (0,103) · 0,390 · 0,476 · 0,186 | 0,100 (0,100) · 0,120 · 0,082 · 0,010 | 0,101 (0,101) · 0,101 · 1,000 · 0,101 | 0,101 (0,101) · 0,101 · 1,000 · 0,101 |
| s2 a10 | 5 | 0,680 (0,096) · 0,366 · 0,078 · 0,028 | 0,796 (0,178) · 0,154 · 0,061 · 0,009 | 1,000 (0,292) · 1,000 · 1,000 · 1,000 | 0,942 (0,103) · 0,508 · 0,279 · 0,142 |
| s2 a10 | 10 | 1,000 (0,096) · 0,387 · 0,075 · 0,029 | 1,000 (0,213) · 0,192 · 0,058 · 0,011 | 1,000 (0,199) · 0,336 · 0,194 · 0,065 | 0,942 (0,166) · 0,369 · 0,198 · 0,073 |
| s2 a10 | 15 | 1,000 (0,103) · 0,378 · 0,086 · 0,033 | 1,000 (0,217) · 0,186 · 0,065 · 0,012 | 1,000 (0,319) · 0,244 · 0,163 · 0,040 | 0,942 (0,015) · 0,317 · 0,134 · 0,043 |
| s2 a10 | 20 | 1,000 (0,103) · 0,350 · 0,088 · 0,031 | 1,000 (0,217) · 0,166 · 0,054 · 0,009 | 1,000 (0,310) · 0,259 · 0,117 · 0,030 | 0,942 (0,029) · 0,285 · 0,122 · 0,035 |
| s2 a11 | 1 | 1,000 (1,000) · 1,000 · 0,246 · 0,246 | 1,000 (1,000) · 1,000 · 1,000 · 1,000 | 1,000 (1,000) · 1,000 · 1,000 · 1,000 | 1,000 (1,000) · 1,000 · 1,000 · 1,000 |
| s2 a11 | 5 | 0,696 (0,128) · 0,434 · 0,164 · 0,071 | 0,978 (0,303) · 0,445 · 0,114 · 0,051 | 0,406 (0,009) · 0,136 · 0,339 · 0,046 | 0,533 (0,001) · 0,271 · 0,511 · 0,138 |
| s2 a11 | 10 | 0,761 (0,112) · 0,346 · 0,057 · 0,020 | 1,000 (0,291) · 0,308 · 0,081 · 0,025 | 1,000 (0,000) · 0,284 · 0,209 · 0,059 | 0,533 (0,001) · 0,136 · 0,281 · 0,038 |
| s2 a11 | 15 | 0,913 (0,109) · 0,329 · 0,030 · 0,010 | 1,000 (0,278) · 0,225 · 0,056 · 0,013 | 1,000 (0,002) · 0,247 · 0,208 · 0,051 | 1,000 (0,001) · 0,203 · 0,261 · 0,053 |
| s2 a11 | 20 | 1,000 (0,096) · 0,327 · 0,036 · 0,012 | 1,000 (0,278) · 0,187 · 0,043 · 0,008 | 1,000 (0,004) · 0,258 · 0,195 · 0,050 | 1,000 (0,031) · 0,168 · 0,162 · 0,027 |

| criatura | la clase que más llama, d1 → d20 | deja de mandar lo inútil el día | B1 (P7-39) |
|---|---|---|---|
| s1 a10 | B N N N C C C N N N N C C N C C C C C N | no llega | no llega |
| s1 a11 | N C C C C C C N N N N N N N N N N N N N | no llega | no llega |
| s2 a10 | B C C C N N N N C C N N N N C C N N C C | no llega | no llega |
| s2 a11 | R R R B C C N C N N N N N C C N N N N N | no llega | no llega |

(B botiquín, R ración, N red, C camuflaje.)

## Sección 3 · Los momentos y el miedo

En los 71 momentos de cogida `coger` gana en 62; lo inútil es la clase que más llama (con la cautela) en 102 de 134 momentos. De las 63 aperturas reales,
13 en peligro: la réplica con miedo sigue abriendo 7 (5 sin tic de cogida entre los momentos: la prueba se abrió sin `coger` en el tic anterior, p. ej. al ponerse lo que ya llevaba).

## Lectura

(i) **El filtro de P7-39 sigue haciendo su parte** (I1, I2 pasan: lo inútil importa 0,0085, «no hizo nada» 0,0056) y **la creencia de lo útil está igual de cerca de su
efecto real que en P7-37** (I5 corregido pasa en las 8 parejas; el I5 antiguo no, máx 0,559, por la intensidad atada a la importancia). (ii) **La esperanza de clase funciona sola, pero los
apuntes la anulan**: el punto de partida de clase el día 20 es botiquin 0,075-0,103, racion 0,146-0,278, red 0,004-0,310, camuflaje 0,000-0,200; pero cada criatura acumula 1020-1259 apuntes en 20 días (una mirada
de 10 s cada vez que una cosa está a la vista con un rival a 8 casillas o menos: 4642 entre las 4) y el sello toma el MAYOR de sus intensidades: con cientos de miradas alguna llega a 1,0 y el punto
de partida vuelve a 1 (día 20: botiquin 1,00-1,00, racion 1,00-1,00, red 1,00-1,00, camuflaje 0,52-1,00). Así la importancia esperada de lo inútil queda otra vez en ≈ 1/(1+N) y lo inútil manda 74 de 80 (I3 no), `coger` 62 de 71 (I4 no). Recuento
informativo, fuera del sello y sin banco nuevo (los mismos cuadernos, el punto de partida de clase SIN apuntes): lo inútil mandaría 63 de 80 cierres (20 de 24 en los días 15-20) y s2 a10 dejaría de tenerlo como lo que
más llama el día 20; tampoco pasaría I3. (iii) **El miedo calla el probar** (E2 pasa): de las 13 aperturas reales en peligro la réplica con cautela solo abre 7; y la cautela deja lo inútil al mando
en 102 de 134 momentos (A sin cautela en P7-39: 123). (iv) **Al filo del mañana no llega** (E1: 48,8 %): de 260 apuntes de cosas aún sin recuerdos, 177 se resuelven en un empate (al principio de cada vida todo
lo no probado llama igual); sin los empates, 37 de 83 (botiquin 13 de 34, racion 0 de 8, red 20 de 25, camuflaje 4 de 16): la red vista en peligro sí manda después en calma (20 de 25), el botiquín y la ración casi nunca, porque su
clase (consumibles) ya tiene un punto de partida bajo y la red, con sus «no hizo nada», lo tiene igual de bajo pero más ignorancia.

**Regla final.** P7-40 pasa 3 de I1-I5 y B1 2 (con el I5 corregido para las dos; B1 lo no pasa); lo inútil manda 74 frente a 76 de 80. **El campo va con P7-40**, sin más bancos sobre lo inútil.
Lo que queda dicho, no decidido: el MAYOR de los apuntes es lo que devuelve el punto de partida a 1; con la mediana de los apuntes, o con solo el último, o con el punto de
partida de clase sin apuntes, lo inútil mandaría menos (recuento de arriba) pero seguiría mandando: la ignorancia de lo probado pocas veces pesa más que cualquier esperanza.
