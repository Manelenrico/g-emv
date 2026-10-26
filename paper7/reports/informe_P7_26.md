# P7-26 · La cautela según lo cerca que está el peligro

*7-oct-2026. Coste: plataforma 0, consola 0. Solo réplicas de vidas ya jugadas, una por proceso. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al
acabar; cuerpo y congelados sin tocar; la variante es un mando de banco (`nace_P7_23.E["cautela"]`, apagado en el campo). Este informe lo escribe `escribe_informe_P7_26.py`
desde `P7_26_decisiones.json` (`banco_P7_26.py`).*

## En corto

- **La calma de hoy** (sección 1) es 1 menos la mayor de cinco filas del miedo; en la vida del freno valió **0,52** en 11.486 de sus 11.496 tics, siempre por
  F-4-ALCANCE (rivales a la vista a 5-8 casillas). En los instantes (a') de P7-25, la calma del diario es > 0,5 por construcción y vale 1,0 en la mayoría.
- **La cautela por distancias no cambia el caso del freno**: con el rival a 5 casillas vale (5 − 2) / 6 = 0,5, lo mismo que la calma de hoy (0,52). A una casilla de la ración,
  `ir_centro` gana 312 de 353 veces hoy, 312 con la cautela ×1 y 312 con ×2. No la toca.
- **En las 12 vidas**, la cautela ×1 cambia 22 de 1326 decisiones en calma con lo nuevo cerca (y no hacia lo nuevo: 930 frente a 936 hoy) y
  1.058 de 18.173 en peligro, casi todas quitándole la curiosidad al cuerpo (fuera del círculo y con poca vida la cautela es 0); la curiosidad gana a huir,
  entrar o curarse en 10 de 318 (×1) y 11 (×2), frente a 4-6 con las escalas ×1,5-×2 de P7-25.
- **Corrección a P7-25, dicha aquí:** aquel banco leía la calma de la radiografía de la réplica, que no trae la foto «ahora»; salía 1,0 siempre y el filtro «calma > 0,5»
  de (a) y (a') no filtraba. Reclasificados sus registros con la calma del diario, **ningún instante cambia de clase** (36 en (a), 1.326 en (a'), 18.173 en (b)): las
  conclusiones de P7-25 se mantienen; su informe se ha regenerado con la calma buena.

## Sección 1 · Qué es hoy la calma que multiplica a la curiosidad

`descubre_P7.calma_de` (`descubre_P7.py:136-137`): calma = max(0, 1 − min(1, máximo de las cinco filas de `CALMA_FILAS`, `:61`)). Las cinco filas son del cuerpo congelado
(`paintball/alma/appraisal_zs_v42_exp.py`): **F-4-ALCANCE** (`:1070`, rivales que pueden alcanzarme en el horizonte, techo 0,5 `:130`), **S-7-AGRESOR** (`:1508`, presión de quien me pega),
**F-HERMANO-AMENAZA** y **F-HERMANO-GOLPE** (`:1642-1643`, la amenaza y el golpe al hermano) y **F-ANTICIPACION** (`:1000`, el daño que viene). La curiosidad vale
ACOPIO_M × calma × media de (ignorancia × alivio) de las dos clases (`nace_P7_23.curiosidad_M`), y la promesa de ir a por la cosa la lleva dentro.

En la vida del freno (P7-24, día 1, asiento 10): calma mediana 0,521, igual en los cuatro cuartiles; por debajo de 1 en 11.486 de 11.496 tics; la fila que manda,
F-4-ALCANCE en 11.486 de ellos (rivales a la vista a 5-8 casillas, sin tocarla nunca); con el paso listo, mediana 0,521. Es decir: **la curiosidad de esa criatura valía
la mitad durante toda la vida por rivales lejanos.** En los instantes (a') de las 12 vidas (calma del diario): mediana 0,52, 23 de 1326 con calma 1,0.

## Sección 2 · La variante medida

Cautela(obs) = 1 sin rivales a 8 casillas o menos; (d − 2) / 6 con el rival más cercano a d casillas (1 a 8, 0 a 2); 0 fuera del círculo o con la vida por debajo de 30
(`nace_P7_23.cautela_de`). Sustituye a la calma en la curiosidad y en la promesa de ir a por la cosa; nada más. Escala ×1 y ×2. Banco: las mismas 12 vidas y los mismos
instantes de P7-25 (paso listo, en (a), (a') o (b)); la calma, leída del diario en ese tic. Réplica: 115.579 iguales, 12.703 distintas (las del humo, por el paso 0; como en P7-25).

## Sección 3 · Las mismas medidas de P7-25

| | (a) estricta, de 36: va hacia lo nuevo · `ir_curioso` | (a') con rivales a más de 4, de 1326: va hacia lo nuevo · `ir_curioso` · decisiones que cambian | (b) peligro: la curiosidad gana a huir / entrar / curarse, de 318 · gana a otra cosa, de 18173 · decisiones que cambian |
|---|---|---|---|
| hoy (calma) | 34 · 1 | 936 · 48 · — | — · 824 ya la elige hoy · — |
| cautela ×1 | 34 · 1 | 930 · 41 · 22 | 10 · 13 · 1058 |
| cautela ×2 | 31 · 0 | 892 · 34 · 74 | 11 · 19 · 1991 |

| variante | lo que pierde cuando gana la curiosidad | lo que elige en vez de la curiosidad cuando la variante se la quita (peligro) |
|---|---|---|
| cautela ×1 | `ir_objeto` 10, `ir_pareja` 2, `ir_centro` 1, `move_S` 1 | `ir_botin` 98, `paso_NE` 6, `move_NW` 3, `ir_pareja` 3, `move_NE` 3 |
| cautela ×2 | `ir_objeto` 11, `ir_centro` 2, `ir_pareja` 2, `move_S` 1, `ir_botin` 1 | `ir_botin` 323, `move_NW` 8, `move_NE` 7, `paso_NE` 5, `move_SE` 4 |

**El caso del freno, de cerca:**

| en la vida del freno (a'), 905 instantes · a una casilla, 353 | hoy | cautela ×1 | cautela ×2 |
|---|---:|---:|---:|
| `ir_objeto` (todos) | 555 | 555 | 553 |
| `ir_centro` (todos) | 315 | 315 | 315 |
| `ir_botin` (todos) | 20 | 20 | 20 |
| `ir_curioso` (todos) | 7 | 4 | 0 |
| `ir_centro` (a una casilla) | 312 | 312 | 312 |
| `ir_botin` (a una casilla) | 19 | 19 | 19 |
| `ir_objeto` (a una casilla) | 7 | 7 | 6 |
| `ir_curioso` (a una casilla) | 7 | 4 | 0 |

¿Toca ahora la ración? **No.** A una casilla de ella, `ir_centro` sigue ganando 312 de 353 veces con la cautela ×1 y 312 con ×2: el rival a 5 casillas deja la
cautela en 0,5, lo mismo que la calma. El primer instante con el paso listo y el objeto a 1-2 casillas en que la variante elegiría `ir_curioso`: tic 8.038 (×1), ninguno (×2).
En cuánto tiempo la tocaría no se puede saber sin jugar; con esa cautela no daría el paso.

## Sección 4 · La tabla para Manel

| | coge lo nuevo en calma (a'), de 1.326 | arriesga en peligro (gana a huir, entrar o curarse), de 318 | decisiones que cambian en peligro, de 18.173 |
|---|---:|---:|---:|
| hoy (calma) | 936 | — | — |
| cautela ×1 | 930 (-6) | 10 | 1058 |
| cautela ×2 | 892 (-44) | 11 | 1991 |

Lectura: la cautela por distancias **hace al cuerpo más prudente en peligro** (fuera del círculo y con poca vida apaga la curiosidad: 1.058 decisiones cambian, casi todas
dejando de ir a por lo nuevo) y **no le hace coger más lo nuevo en calma**; en el caso del freno da el mismo freno que la calma, porque un rival a 5 casillas vale 0,5 en las dos.
Si lo que se quiere es que un rival lejano no frene la curiosidad, el radio tendría que ser menor que 5 (hoy 8 a 2), o la cautela no debería entrar cuando el objeto está a una
casilla; son números de la mesa. Y sigue en pie lo de P7-25: lo que falta es lo que el cuerpo cree que gana al llegar.

## Archivos

| archivo | qué es |
|---|---|
| `banco_P7_26.py` → `P7_26_decisiones.json` | las decisiones con la cautela ×1 y ×2 |
| `nace_P7_23.py` (`cautela_de`, `E["cautela"]`) | la variante, como mando de banco (apagada en el campo) |
| `P7_25_decisiones.json`, `informe_P7_25.md` | reclasificados con la calma del diario (sin cambios de clase) |
| `informe_P7_26.md` | este informe |
