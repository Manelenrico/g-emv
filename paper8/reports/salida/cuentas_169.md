# Dos cuentas del prompt 169

## Parte 1: el vaivén de dos días, emparejado (sección 6)

Vaivén = felicidad de los días de fruto menos la de los días sin fruto (puntos, la cuenta del 157). Tamaño = |vaivén|. Diferencias de tamaño emparejadas por semilla [95 %]; < 0 quiere decir que a la del motor le mueve menos.

| mundo | vaivén medio: motor · suma · posición | tamaño motor − tamaño suma | tamaño motor − tamaño posición |
|---|---|---|---|
| abundancia | +0,2 · −0,7 · −2,4 | −0,51 [−1,14, +0,12] (cruza el cero) | −0,96 [−1,71, −0,24] (se separa) |
| normal | −3,7 · −8,1 · −8,6 | −4,08 [−5,29, −2,90] (se separa) | −4,49 [−5,39, −3,60] (se separa) |
| sequía | −5,7 · −9,6 · −8,4 | −3,91 [−4,90, −2,92] (se separa) | −2,62 [−3,57, −1,71] (se separa) |
| sequía dura | −5,0 · −6,4 · −6,1 | −1,53 [−2,88, −0,20] (se separa) | −1,12 [−2,53, +0,21] (cruza el cero) |
| bestias que crían | −8,3 · −10,9 · −10,0 | −2,63 [−4,32, −0,94] (se separa) | −1,68 [−2,99, −0,40] (se separa) |

## Parte 11: lo que baja la distancia al ganar 0,1 o al perder 0,1 menos

Recursos y vínculo en el reposo del paper dos (config_cuerpo_valle.json, vivir_bien.reposo_dos): pR = +1,60, pS = +0,68, sin pérdida. Distancia: opponent_distance de motor/model.py, con DEFAULT_CONFIG, importados.

| cuerpo: ganancia · pérdida | d al partir | baja al ganar +0,1 | baja al perder −0,1 | cociente (ganar / perder) |
|---|---|---|---|---|
| +0,7 · +0,2 | +1,2036 | +0,0254 | +0,0715 | 35,5 % |
| +0,5 · +0,0 | +1,1401 | +0,0413 | no se puede: la pérdida ya es 0 | — |

Solo como cuenta formal (una pérdida de −0,1 no existe en el motor): con 0,5 · 0 y la pérdida en −0,1, baja +0,0608 y el cociente sería 67,9 %.
Con el otro reposo, el de model.py (todas las fuerzas a 0; el mínimo basal las deja en 0,05), y el cuerpo en 0,7 · 0,2: ganar 0,1 hace que la distancia suba +0,0198 y perder 0,1 menos la baja +0,0561; el cociente es −35,4 %.

**¿Es estable?** El cociente (ganar / perder, en %) en una rejilla de puntos de partida del cuerpo, con recursos y vínculo en el reposo del paper dos:

| ganancia \ pérdida | 0,1 | 0,2 | 0,3 | 0,5 |
|---|---|---|---|---|
| +0,30 | 87 % | 82 % | 78 % | 73 % |
| +0,50 | 65 % | 63 % | 61 % | 59 % |
| +0,70 | 31 % | 36 % | 38 % | 42 % |
| +0,82 | 1 % | 13 % | 21 % | 29 % |
| +0,90 | −26 % | −6 % | 6 % | 20 % |
| +1,00 | −75 % | −36 % | −16 % | 6 % |
| +1,20 | −297 % | −140 % | −81 % | −30 % |
