# P7-58 · Banco (coste cero): curiosidad por el progreso del aprendizaje

*13-oct-2026. Sello `SELLO_P7_58.md` (commit `9fc2420`, antes de calcular). Sin API, sin plataforma; la serie 3 de P7-56 y las piezas de P7-57 sin tocar. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`.
Pieza `progreso_P7_58.py` = `2c6a439c7b5b2239a79309d7464b2de7`; banco `banco_P7_58.py --cadena` (12 criaturas × 20 días de APRENDE de P7-45 en cadena honesta, 1503 s) → `P7_58_cadena.json`; `analiza_P7_58.py` → `P7_58_sello.json`;
`escribe_informe_P7_58.py` (este informe; ninguna cifra a mano). Los diarios de APRENDE de P7-45 (archivados el 12-oct) se rehidrataron desde sus zips con el md5 del manifiesto (240 de 240).
Fidelidad de la réplica al diario: 2.335.412 decisiones iguales · 804.650 distintas.*

## El sello, de una vez

| | criterio | resultado | pasa |
|---|---|---|---|
| H1 | lo inútil manda ≤ 50 % de los cierres y ≤ 20 % de los de d15-20 | 33 de 240 (13,8 %); d15-20 2 de 72 (2,8 %) | sí |
| H2 | en los momentos de decisión, `coger` lo inútil gana ≤ 1/3 | 154 de 436 (35 %; `ir_curioso` 183) | NO |
| H3 | d10-20, ración > red en ≥ 75 % de los cierres con las dos probadas ≥ 3 veces | 75 de 129 (58 %) | NO |

**Regla de parada: no pasan H2, H3 → se informa y se para; queda para después del siete.** Manda por clase en los 240 cierres: botiquín 173, ración 34, red 11, camuflaje 22.
Por personalidad: lo inútil manda 17 de 120 (valiente) y 16 de 120 (prudente); `coger` gana 66 de 205 y 88 de 231.

## Curiosidad por objeto y día (media de las 12 criaturas, al cerrar; cautela 1)

| día | botiquín | ración | red | camuflaje |
|---:|---:|---:|---:|---:|
| 1 | 2,05 | 1,05 | 0,89 | 0,99 |
| 2 | 1,56 | 1,38 | 0,79 | 0,81 |
| 3 | 4,67 | 1,11 | 0,66 | 0,58 |
| 4 | 2,43 | 1,05 | 0,55 | 1,30 |
| 5 | 5,18 | 1,90 | 0,50 | 1,16 |
| 6 | 6,04 | 0,99 | 0,55 | 1,16 |
| 7 | 6,66 | 1,06 | 0,74 | 1,05 |
| 8 | 7,30 | 1,47 | 0,88 | 0,77 |
| 9 | 5,92 | 0,71 | 0,75 | 0,57 |
| 10 | 10,30 | 0,69 | 0,68 | 6,16 |
| 11 | 12,21 | 0,42 | 0,65 | 6,20 |
| 12 | 17,82 | 0,36 | 0,65 | 3,80 |
| 13 | 18,87 | 0,50 | 0,50 | 0,94 |
| 14 | 18,32 | 0,60 | 0,47 | 0,71 |
| 15 | 17,21 | 0,56 | 0,62 | 0,67 |
| 16 | 20,53 | 0,58 | 0,50 | 0,49 |
| 17 | 19,43 | 0,60 | 0,51 | 0,57 |
| 18 | 20,97 | 0,60 | 0,48 | 0,66 |
| 19 | 20,77 | 1,14 | 0,47 | 0,64 |
| 20 | 20,65 | 1,18 | 0,43 | 2,12 |

## Por criatura

| criatura | lo inútil manda (de 20) | d15-20 (de 6) | la clase que manda, d1 → d20 | se apaga la curiosidad del botiquín (día) |
|---|---:|---:|---|---|
| APRENDE_v s1 a10 | 3 | 0 | bot rac rac bot red cam red bot bot bot bot bot bot bot bot bot bot bot bot bot | no se apaga |
| APRENDE_v s1 a11 | 3 | 0 | bot bot bot bot bot bot cam cam cam bot bot bot bot bot bot bot bot bot bot bot | no se apaga |
| APRENDE_v s2 a10 | 2 | 0 | bot rac red red bot bot bot bot bot bot bot bot bot bot bot bot bot bot bot bot | no se apaga |
| APRENDE_v s2 a11 | 3 | 0 | bot bot bot bot bot bot bot bot bot cam cam cam bot bot bot bot bot bot bot bot | no se apaga |
| APRENDE_v s3 a10 | 5 | 0 | bot cam cam cam red red bot bot bot bot bot bot rac rac rac rac rac bot bot bot | no se apaga |
| APRENDE_v s3 a11 | 1 | 0 | rac rac rac rac rac red bot bot bot bot bot bot bot bot bot bot bot bot bot bot | no se apaga |
| APRENDE_p s1 a10 | 0 | 0 | bot rac rac rac bot bot bot bot bot bot bot bot bot bot bot bot bot bot bot bot | no se apaga |
| APRENDE_p s1 a11 | 0 | 0 | rac rac rac bot bot bot rac rac bot bot bot bot bot bot bot bot bot bot bot bot | no se apaga |
| APRENDE_p s2 a10 | 5 | 0 | bot bot rac rac rac rac red rac rac cam cam cam cam bot bot bot bot bot bot bot | no se apaga |
| APRENDE_p s2 a11 | 4 | 2 | bot bot bot bot bot bot bot bot bot bot bot bot cam cam red rac rac rac rac cam | no se apaga |
| APRENDE_p s3 a10 | 5 | 0 | bot rac rac cam cam cam cam cam bot bot bot bot bot bot bot bot bot bot bot bot | no se apaga |
| APRENDE_p s3 a11 | 2 | 0 | bot bot bot bot rac bot red red bot bot bot bot bot bot bot bot bot bot bot bot | no se apaga |

## Lectura

1. **H1 pasa de lejos**: lo inútil deja de mandar (13,8 % de los cierres, 2,8 % en d15-20, frente a 62 % y 58 % con la habituación de P7-47). Manda el botiquín (173 de 240): es lo que
   más progreso de aprendizaje da, prueba a prueba.
2. **H2 no pasa por poco**: `coger` lo inútil gana 35,3 % de los momentos (umbral 33,3 %); y `ir_curioso` gana 183 más: en el momento de la red a los pies, la réplica ya no la coge tanto, y elige
   `ir_curioso` (ir hacia lo que más llama; este banco no registra a qué clase va en ese tic).
3. **H3 no pasa**: la ración supera a la red en 58 % de los cierres con las dos probadas ≥ 3 veces (umbral 75 %). La ración, que cura 15 fijos y casi siempre toca techo («al menos»), deja de mover la
   creencia pronto: su progreso cae como el de la red, que no la mueve nada.
4. **La curiosidad del botiquín no se apaga nunca** (en ninguna de las 12 criaturas baja de 0,5): crece (2,0 el d1, 10,3 el d10, 20,6 el d20) porque el divisor es la mediana de todos los
   productos, que caen al apagarse los demás objetos: el progreso es relativo y el botiquín, cuyas curas varían (al menos, cortes, +50), siempre «enseña» más que la mediana. Es un efecto de la
   normalización por la mediana, no un aprendizaje que no se agota: para la mesa.
5. La réplica difiere del diario en el 25,6 % de las decisiones (P7-47: 7,7 %): esta curiosidad cambia mucho la conducta.

**Regla de parada: no pasan H2 y H3 → se informa y se para; queda para después del siete.**
