# P7-18 · Por qué no coge lo que pidió

*5-oct-2026. Coste: plataforma 0, consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar. Solo banco y diarios.
`banco_P7_18.py` replica, una vida por proceso y tal como se jugó P7-14b, la vida del hermano que pedía (11 vidas; la elección del campo se reproduce en 147.853 de 147.853 tics)
y apunta lo que tenía delante en cada tic a dos casillas o menos del botiquín regalado → `P7_18_escenas.json`. `analiza_P7_18.py` le pone a cada tic una razón, con la lista
declarada antes de contar, y cruza con el diario de quien regaló → `P7_18_razones.json`.*

## Lo que sale, en corto

**No lo coge porque quien se lo dio se queda encima.** El botiquín regalado cae en la casilla de quien lo suelta, y quien lo suelta no se mueve de ahí. El hermano que pedía
lo ve, lo quiere, tiene sitio y da el paso hacia esa casilla, pero el mundo se lo devuelve bloqueado: 3.030 de 3.033 pasos hacia la casilla del regalo, bloqueados. Es la razón principal
en 30 de los 40 regalos (20 de 23 en TECHO, 10 de 15 en APRENDE). No es el arreglo del seis ni una regla del estilo «lo dado, dado está» en quien recibe.

## Sección 1 · Los regalos mirados

Los 40 regalos de P7-14b que, con la regla de pedir de P7-17, se seguirían haciendo y que en el campo volvieron a quien los dio (`P7_17_pedir.json`): TECHO 23 (todos
los suyos que volvían), APRENDE 15, BORRADO 2. Entre el regalo y la recogida, los tics en que el hermano que pedía está a dos casillas o menos (Chebyshev) del botiquín:

| | TECHO | APRENDE | BORRADO |
|---|---:|---:|---:|
| regalos | 23 | 15 | 2 |
| tics del que pedía a 2 casillas o menos | 12.507 | 3.980 | 963 |
| … encima / a 1 / a 2 | 22 / 6.884 / 5.601 | 0 / 2.955 / 1.025 | 90 / 329 / 544 |
| **¿lo veía?** (el botiquín en esa casilla, entre lo que ve) | 12.488 (99,8 %) | 3.966 (99,6 %) | 962 (99,9 %) |
| sin botiquín a bordo | 12.369 | 3.980 | 963 |
| le cabe (hueco en el zurrón) | 12.507 | 3.980 | 36 |
| la promesa del botiquín es mayor que cero (lo quiere) | 12.369 | 3.980 | 963 |
| solo tiene `noop` (el paso en enfriamiento) | 9.595 | 888 | 0 |
| **existe `coger`** (en `candidatos` / en `decide`) | 2 / 2 | 0 / 0 | 0 / 0 |
| `coger` escondido por el arreglo del seis | 0 | 0 | 90 |
| **existe un candidato de ir a por ese botiquín** (`ir_objeto` o `ir_curioso` con ese destino) | 7 | 164 | 130 |
| … su d menos la del elegido: igual / peor (mediana de las peores) | 7 / 0 | 163 / 1 (0,012) | 1 / 129 (0,006) |
| **qué eligió** | `noop` 10.450, `move_E` 826, `ir_objeto` 510, `move_S` 413 | `move_NE` 2.031, `ir_curioso` 955, `noop` 893, `ir_objeto` 82 | `noop` 920, `ir_curioso` 36, `paso_NE` 2, `paso_S` 2 |
| pasos elegidos hacia la casilla del regalo | 1.072 | 1.960 | 1 |
| … que el mundo devolvió bloqueados | 1.070 | 1.960 | 0 |
| tics de espera del regalo (del regalo a la recogida) | 13.132 | 4.041 | 1.004 |
| … con quien lo dio encima del botiquín | 5.234 (40 %) | 2.952 (73 %) | 22 (2 %) |
| regalos con quien lo dio encima más del 90 % de la espera / alguna vez | 16 / 23 | 7 / 15 | 0 / 2 |

**Respuesta a la pregunta 1.** Sí lo veía (en más del 99 % de los tics en los tres brazos), no llevaba botiquín, tenía sitio (salvo en los 2 de BORRADO) y lo quería. `coger` casi nunca
existía porque casi nunca llegó a estar encima: no podía entrar. Cuando eligió algo distinto de `noop`, lo más frecuente fue un paso (`move_*`) hacia la casilla del regalo, con la misma d
que el candidato de ir a por él cuando ese existía; y el paso no se dio.

## Sección 2 · La razón de cada tic

Una razón por tic, la primera que cumpla (lista declarada en la cabecera de `analiza_P7_18.py` antes de contar):

| razón | TECHO | APRENDE | BORRADO |
|---|---:|---:|---:|
| el que lo dio esta encima del regalo | 4.651 | 2.950 | 20 |
| a 1 o 2 casillas: solo noop (paso en enfriamiento) | 6.351 | 163 | 0 |
| a 1 o 2 casillas: sin candidato, su mejor objeto es otro (first_aid) | 287 | 737 | 0 |
| a 1 o 2 casillas: sin candidato, no le cabe | 0 | 0 | 695 |
| a 1 o 2 casillas: sin candidato, su mejor objeto es su propia casilla (first_aid recordado ahi) | 624 | 13 | 0 |
| a 1 o 2 casillas: sin candidato, la casilla esta en sus propias cesiones | 365 | 0 | 0 |
| ya lleva un botiquin | 138 | 0 | 0 |
| a 1 o 2 casillas: sin candidato, su mejor objeto es otro (backpack) | 0 | 106 | 28 |
| a 1 o 2 casillas: tiene candidato de ir a por el y pierde contra noop | 0 | 0 | 128 |
| encima: coger escondido por el arreglo del seis | 0 | 0 | 90 |
| a 1 o 2 casillas: sin candidato, su mejor objeto es otro (camouflage) | 43 | 0 | 0 |
| a 1 o 2 casillas: sin candidato, su mejor objeto es su propia casilla (camouflage recordado ahi) | 25 | 0 | 0 |
| encima: la casilla esta en sus propias cesiones (no hay coger) | 22 | 0 | 0 |
| a 1 o 2 casillas: va a por el | 1 | 10 | 0 |
| a 1 o 2 casillas: tiene candidato de ir a por el y pierde contra ir_objeto | 0 | 1 | 0 |
| a 1 o 2 casillas: tiene candidato de ir a por el y pierde contra un paso | 0 | 0 | 1 |
| a 1 o 2 casillas: da un paso hacia el | 0 | 0 | 1 |
| **total de tics** | **12.507** | **3.980** | **963** |

Razón principal de cada regalo (la que más tics tiene):

| razón principal | TECHO | APRENDE | BORRADO |
|---|---:|---:|---:|
| el que lo dio esta encima del regalo | 20 | 10 | 0 |
| a 1 o 2 casillas: sin candidato, su mejor objeto es otro (first_aid) | 0 | 5 | 0 |
| a 1 o 2 casillas: solo noop (paso en enfriamiento) | 2 | 0 | 0 |
| a 1 o 2 casillas: sin candidato, la casilla esta en sus propias cesiones | 1 | 0 | 0 |
| a 1 o 2 casillas: sin candidato, no le cabe | 0 | 0 | 1 |
| a 1 o 2 casillas: sin candidato, su mejor objeto es otro (backpack) | 0 | 0 | 1 |

## Sección 3 · Qué regla lo impide (pregunta 2) y qué gana (pregunta 3)

**Lo que lo impide no es una regla que esconda `coger`: es dónde queda el botiquín.**

1. **El regalo cae bajo los pies de quien lo da.** `soltar` deja el objeto en la casilla propia (`decisor_zs.py:820` y `:955`, acción `drop`; la cesión se apunta con esa casilla, `:903-904`).
2. **Quien lo da no tiene motivo para apartarse.** La fila que paga el regalo, S-PROVISION, se da por servida con «una venda en el suelo a 2 casillas o menos de ella, en casilla no ocupada
   por terceros» (`appraisal_zs_v42_exp.py:1328-1349`; `MEDICINA_DIST = 2`, `:332`): «terceros» son los demás (`_mal59` excluye mi asiento y el del hermano), así que mi propia casilla vale.
   Con el regalo hecho, el malestar ya está aliviado y quedarse quieto es lo mejor: quien regaló está encima del botiquín el 40 % de la espera en TECHO y el 73 % en APRENDE.
3. **El que pedía no puede entrar en una casilla ocupada.** Elige el paso hacia ella y el mundo devuelve `blocked`: TECHO 1.070 de 1.072, APRENDE 1.960 de 1.960.
   `coger` solo existe con el objeto en la casilla propia (`decisor_zs.py:475-483`), así que nunca llega a existir.
4. **No es el arreglo del seis** («la mochila no cambia», `arreglos_P6_8b.py:135-140`): en TECHO y APRENDE no esconde `coger` en ninguno de estos tics (0); sí en los 2 regalos de BORRADO
   (90 tics encima con el zurrón lleno), que son el caso de P7-15 y que la regla de P7-17 no llegó a quitar del todo.

**Cuando el candidato existía y no ganaba:** en APRENDE y TECHO, el candidato de ir a por ese botiquín empata con el paso elegido (170 tics con la misma d) porque el paso elegido ES el
paso hacia el botiquín; pierde de verdad en 1 tics. No hay huida ni pelea de por medio: el rival más cercano está a 5 casillas de mediana y la vida, entera
(mediana 100).

**Las otras causas, del lado de quien pedía** (aparecen cuando la casilla está libre; en APRENDE son pocas, en TECHO pesan: quien regaló solo está encima el 40 % de la espera,
y con la casilla libre el que pedía tiene casi siempre solo `noop`, y cuando puede decidir, una de estas tres):
- **Su mejor objeto es otro** (1.863 tics): `_mejor_objeto` (`decisor_zs.py:684-704`) elige por valor / (1 + distancia) entre lo visto y lo recordado; en 662 tics el elegido
  es su propia casilla, con un objeto recordado ahí, y entonces `ir_objeto` no se crea (`:459`): no va a ningún sitio.
- **La casilla del regalo está en sus propias cesiones** (387 tics, todos en TECHO): él mismo había soltado ahí antes (los dos hermanos se pasan el botiquín en la misma casilla),
  y lo cedido no se coge ni se va a por ello (`decisor_zs.py:479-480` y `:696`).
- **No le cabe** (695 tics, BORRADO).

## Sección 4 · El arreglo más pequeño (propuesta, sin aplicar)

**Quien regala se aparta: lo dado no está entregado mientras lo piso.**

En la pieza J (`pide_P7.py`, donde el regalo ya mira el pedido), sin tocar el cuerpo y sin ningún número nuevo:
1. Al elegir `soltar_<botiquín>`, la criatura apunta esa casilla como «mi regalo» (en su estado de la partida, no en `mem.cedidos`: la cesión del cuerpo se borra en cuanto el
   hermano está entero, `appraisal_zs_v42_exp.py:663-683`, y aquí casi siempre lo está).
2. En las fotos en que ella misma está sobre esa casilla y el botiquín sigue ahí, las filas que regalan valen lo que valdrían sin el botiquín en el suelo (el mismo recálculo que la
   pieza ya hace cuando no hay pedido). En la foto de `soltar`, que se evalúa antes de apuntar nada, el alivio cuenta como hoy: el regalo se sigue haciendo.
3. Resultado esperado: justo después de regalar, quedarse encima deja de aliviar S-PROVISION y dar un paso a cualquier casilla vecina lo alivia entero, así que el cuerpo se aparta por su
   propia cuenta, con la fuerza que ya tiene. El que pedía, que ya elige el paso hacia el botiquín, entra y lo coge. La marca se borra cuando el botiquín deja de estar en esa casilla.

Salvo que algo más urgente lo impida: es una fila más en la balanza (la misma S-PROVISION, hasta 0,30 por k), no una orden; con un rival encima o el anillo, mandan sus filas.

Lo que este arreglo NO toca, y habría que mirar después en banco: las otras causas de la sección 3 (el objeto recordado en la propia casilla y las cesiones cruzadas), que son del
cuerpo y que en TECHO no son pequeñas, y el zurrón lleno de BORRADO. Con el arreglo, la casilla quedaría libre mucho antes; cuántos de esos regalos se cogerían entonces no lo sé. **No lo he aplicado ni probado**: hacerlo es código nuevo; lo primero sería un banco sobre estas mismas 40 escenas (¿se aparta en el tic siguiente?).

Alternativa que no recomiendo: quitar `noop` de los candidatos de quien acaba de regalar. Es más corta, pero es una conducta escrita, no una fuerza.

## Archivos

| archivo | qué es |
|---|---|
| `banco_P7_18.py` → `P7_18_escenas.json` | la vida del que pedía, replicada como se jugó; lo que tenía delante en cada tic cerca del regalo |
| `analiza_P7_18.py` → `P7_18_razones.json` | una razón por tic y por regalo, con la posición de quien regaló |
| `informe_P7_18.md` | este informe |
