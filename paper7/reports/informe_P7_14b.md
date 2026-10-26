# P7-14b · El segundo campo del siete, con pedir

*4/5-oct-2026. Coste: **créditos de la plataforma 13,5670 USD** en 160 partidas (ESPERANZA 3,7655, BORRADO 3,4893, APRENDE 3,2347, TECHO 3,0775);
**consola de Anthropic 0 USD**. Con las 3 partidas del freno de P7-14 (0,2542 USD, que no cuentan para nada), el capítulo del segundo campo suma 13,8212 USD.
Acumulado del siete en la plataforma: 29,8359 USD. Saldos: no consultados. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar;
cuerpo y congelados sin tocar. Sello antes de jugar: `SELLO_P7_14b.md`, commit `ca32d865fca6`. Peticiones: {'completed': 160}. El sello se ha evaluado una sola vez, al final.*

## Lo que sale, en corto

**El sello: 3 de 5** (pasan Q3, Q4, Q5; fallan Q1, Q2).

- **Q1 (la principal): falla.** APRENDE menos BORRADO, emparejado: puesto 1,23 (se 0,53); vida al morir -2,62 (se 2,89).
- **Q2: falla.** APRENDE regala 56 veces en 80 vidas (0,700 por vida; tope 0,534) y vuelve a coger 48 (0,600 por vida; tope 0,116).
- **Q3: pasa.** Días 11 a 20, parte de la vida yendo a por botiquines: APRENDE 15,7 %, BORRADO 19,8 %.
- **Q4: pasa.** La creencia sube en 4 de 4; vida al usar en los días 11 a 20: APRENDE 73,0, BORRADO 86,0.
- **Q5: pasa.** 95 de 1.042 pedidos cerrados lo fueron porque se lo dieron (9,1 %).

## Sección 1 · Lo declarado antes de leer nada

- **Las 3 partidas del freno de P7-14 no cuentan para nada.** Se jugaron el 4-oct (APRENDE, serie 1, días 1 a 3, semillas k = 112, 113 y 114; 0,2542 USD)
  con el código anterior al arreglo; el freno falló en (b) y el campo paró (`informe_P7_14.md`). Ni sus diarios ni sus cuadernos entran en este campo.
- **Paso 0 y paso 1** (el sitio en el disco y la ignorancia que descuenta una sola vez) están en `informe_P7_14.md`, secciones 1 y 2, y siguen valiendo.
  Una nota sobre el paso 0: los .zip del cinco no tienen una sola copia, como decía ese informe: tienen también copia en el Time Machine del Mac (disco SAMSUNG, 860 EVO).
- **Ojos compartidos apagados** (`GEMV_OJOS=0`, parte E1), por decisión de Manel para todo el capítulo 3.
- El brazo que en P7-10 se llamó SUELO aquí es ESPERANZA; cuando se compara con P7-10 se usa su SUELO.

## Sección 2 · El arreglo: en un empate no se da ni se suelta nada

`descubre_P7.desempate_sin_sitio` (la pieza I de P7-10) valía para `hacer_sitio_*`; ahora vale para todo gesto de desprenderse (`DESPRENDERSE`:
`hacer_sitio_*` y `soltar_*`, que es regalar el botiquín y soltar raciones). Si el mínimo de la d lo comparten uno de esos gestos y otro candidato
que no lo es, o si el paisaje es degenerado (todas las d dentro del `TIEBREAK_EPS` del propio desempate de la casa, `planificador_v1.py:376`), los
gestos de desprenderse salen del desempate: gana no desprenderse. Si desprenderse gana solo, gana. Ningún número nuevo. Va con hacer sitio
encendido (los cuatro brazos del campo) y apagado en F1.

| prueba | resultado |
|---|---|
| F1 (`P7_14b_F1.json`): apagado y TECHO contra los 80 diarios de A4 | 1.007.274 y 1.007.274 tics iguales; 2 y 2 distintos (los de siempre): **pasa** |
| banco, los regalos de SUELO en P7-10 (`banco_P7_14b.py` → `P7_14b_banco.json`) | 24 regalos en 9 vidas; 24 eran empate exacto con `noop`; con el arreglo la réplica regala **0** (elige `noop` 24) |
| banco, el F2 de P7-13 otra vez (`P7_14b_F2.json`): los 171 regalos de APRENDE en P7-10, con pedir | el hermano pedía en 16; la réplica sigue regalando **13** (13 con pedido, **0 sin pedido**); en P7-13 eran 21 (16 y 5) |

El F2 de ahora lleva también el arreglo de las ganas de P7-14, así que no es solo el efecto del empate: de los 16 regalos con pedido siguen 13.

## Sección 3 · El sello, el freno y la noche

`SELLO_P7_14b.md` (commit `ca32d865fca6`, subido antes de pedir nada): las cinco preguntas, las medidas y el freno de P7-14 palabra por palabra;
semillas nuevas k = 132 a 151 (`semillas_P7_14b.json`; serie 2 en orden inverso); md5 de los archivos. Imágenes fijas ESPERANZA v60, BORRADO v61, TECHO v62; APRENDE, una por serie y día.

**El freno** (APRENDE, serie 1, días 1 a 3; `P7_14b_freno.json`): (a) el cuaderno viaja y se lee los días 2 y 3: pasa. (b) 39 pedidos abiertos, 0 regalos,
0 sin pedido: pasa. (c) asiento 11: creencia 4,3 → 9,5, ignorancia 0,467 → 0,184: pasa. **El freno pasó y el campo siguió.**

**La noche.** Primera partida pedida a las 21:26 UTC del 2026-10-04; última completada a las 03:09 UTC del 2026-10-05. Esperas de red: 0.
Paradas por disco: 0. Paradas por red: 0. En hora local: las imágenes fijas se hornearon desde las 23:19 del 4-oct (25,69 GB libres), el freno se jugó de 23:27 a 00:10 y el resto del campo de
00:10 a 05:09 del 5-oct, sin ninguna interrupción: 160 partidas pedidas y 160 completadas, 320 diarios bajados y comprobados contra su .zip (mismo
tamaño, los 320). Disco: 25,16 GB libres al lanzar el campo, 12,16 GB al acabar (mínimo por encima de la guarda de 5 GB); tras cada horneado,
limpieza de Docker sin tocar la imagen en juego. Ningún .zip borrado.

## Sección 4 · El campo, por brazo

320 vidas leídas (ESPERANZA 80, BORRADO 80, APRENDE 80, TECHO 80). Un uso = botiquín gastado. Entre paréntesis en la primera tabla, lo mismo en P7-10 (sin pedir).

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| botiquines cogidos | 81 (123) | 160 (143) | 186 (297) | 151 (168) |
| regalos | 0 (24) | 2 (21) | 56 (171) | 37 (69) |
| usos | 63 (70) | 123 (94) | 85 (89) | 82 (61) |
| canales interrumpidos | 98 (78) | 139 (105) | 106 (169) | 149 (121) |
| mediana de la vida al usar | 80,0 (85,0) | 84,0 (86,0) | 73,0 (69,0) | 67,5 (63,0) |
| usos con la vida < 50 | 7 (5) | 9 (12) | 10 (20) | 21 (16) |
| usos con la vida ≥ 80 | 36 (50) | 80 (61) | 34 (25) | 25 (16) |
| hacer sitio (oscilaciones) | 8 (0) | 15 (1) | 19 (0) | 4 (0) |
| muere por rival / por el anillo / sobrevive | 20 / 37 / 23 (14 / 41 / 25) | 12 / 37 / 31 (22 / 32 / 26) | 19 / 39 / 22 (28 / 36 / 16) | 21 / 35 / 24 (13 / 42 / 25) |
| vidas en el puesto 1 | 13 (13) | 14 (8) | 7 (7) | 11 (14) |
| puesto medio | 5,34 (4,70) | 4,36 (4,66) | 5,59 (5,91) | 4,89 (4,36) |
| vida al morir, media | 9,1 (10,6) | 11,3 (11,5) | 8,7 (6,4) | 9,8 (11,0) |

**Mediana de la vida al usar, por tramos de días** (entre paréntesis, usos):

| brazo | días 1-5 | días 6-10 | días 11-15 | días 16-20 |
|---|---:|---:|---:|---:|
| ESPERANZA | 80,0 (20) | 85,0 (15) | 80,0 (12) | 77,5 (16) |
| BORRADO | 81,0 (32) | 85,0 (29) | 86,0 (34) | 84,0 (28) |
| APRENDE | 84,0 (20) | 73,0 (27) | 75,5 (22) | 67,5 (16) |
| TECHO | 71,0 (22) | 67,5 (18) | 69,5 (16) | 62,0 (26) |

**El cuaderno de APRENDE** (creencia del botiquín, cuerpo, dentro del círculo, con el recuerdo neutro, como en P7-10; «–» = «no sé»):

| criatura | creencia al fin de los días 1 / 5 / 10 / 15 / 20 | ignorancia 1 / 5 / 10 / 15 / 20 | recuerdos al final (firmes) |
|---|---|---|---:|
| serie 1, asiento 10 | – / 5,7 / 33,4 / 33,3 / 37,2 | – / 0,307 / 0,070 / 0,073 / 0,074 | 16 (2) |
| serie 1, asiento 11 | 4,3 / 15,8 / 17,8 / 20,9 / 20,4 | 0,467 / 0,118 / 0,063 / 0,058 / 0,063 | 21 (2) |
| serie 2, asiento 10 | 25,4 / 27,8 / 26,5 / 22,7 / 31,3 | 0,273 / 0,148 / 0,152 / 0,090 / 0,064 | 17 (1) |
| serie 2, asiento 11 | 6,8 / 31,8 / 37,5 / 39,0 / 41,7 | 0,292 / 0,127 / 0,065 / 0,041 / 0,038 | 31 (5) |
El cuaderno de APRENDE se leyó al arrancar en 76 de las 76 vidas de los días 2 a 20.

## Sección 5 · Los pedidos

Un pedido se abre cuando un parte lleva el campo tras uno que no lo llevaba, y se cierra al revés; el motivo lo apunta quien pedía. «Porque se lo
dieron» = entre el parte anterior y el del cierre, el hermano ejecutó un regalo de botiquín.

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| partes emitidos | 21.330 | 21.792 | 20.698 | 21.227 |
| partes con pedido | 2.566 (12,0 %) | 3.029 (13,9 %) | 1.939 (9,4 %) | 1.933 (9,1 %) |
| pedidos abiertos | 200 | 264 | 310 | 323 |
| pedidos cerrados | 187 | 248 | 295 | 312 |
| … cerrados porque «lo ve» | 177 | 246 | 289 | 299 |
| … cerrados porque «lo lleva» | 3 | 2 | 6 | 8 |
| … cerrados porque «ya no le alivia (promesa 0)» | 7 | 0 | 0 | 5 |
| … cerrados porque se lo dieron | 0 | 2 | 56 | 37 |
| abiertos al acabar la vida | 13 | 16 | 15 | 11 |
| vidas con pedir encendido / errores de las piezas | 80 / 0 | 80 / 0 | 80 / 0 | 80 / 0 |

El parte más largo del campo mide 46 caracteres (de 120).

## Sección 6 · Los regalos y adónde van

Entre paréntesis, P7-10 (sin pedir; su SUELO en la columna de ESPERANZA).

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| regalos (gestos) | 0 (24) | 2 (21) | 56 (171) | 37 (69) |
| unidades regaladas | 0 (34) | 3 (41) | 105 (307) | 73 (122) |
| vidas con algún regalo | 0 (9) | 2 (11) | 15 (39) | 12 (37) |
| regalos con pedido / sin pedido | 0 / 0 | 2 / 0 | 56 / 0 | 37 / 0 |
| lo recoge el hermano | 0 (2) | 0 (4) | 7 (69) | 14 (20) |
| lo vuelve a coger él mismo | 0 (16) | 2 (9) | 48 (93) | 23 (27) |
| seguía en el suelo la última vez que se vio | 0 (4) | 0 (7) | 1 (8) | 0 (18) |
| se lo lleva un rival | 0 (1) | 0 (1) | 0 (1) | 0 (4) |
| desaparece sin ver quién | 0 (1) | 0 (0) | 0 (0) | 0 (0) |
| hermano sano / herido / crítico al regalar | 0 / 0 / 0 | 1 / 0 / 1 | 49 / 2 / 5 | 36 / 0 / 1 |
| botiquines cogidos que había soltado el hermano | 0 (3) | 0 (4) | 7 (79) | 15 (22) |
| botiquines soltados al hacer sitio | 7 (10) | 13 (15) | 16 (10) | 1 (1) |

## Sección 7 · El tiempo

Media por vida; «tics» con el candidato en curso (definición de P7-11). Entre paréntesis, P7-10.

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| tics vivos | 12.782 (13.237) | 13.060 (13.148) | 12.402 (12.469) | 12.720 (13.246) |
| yendo a por un botiquín, parte de la vida | 0,4 % (1,1 %) | 18,8 % (18,9 %) | 16,5 % (22,5 %) | 3,0 % (3,5 %) |
| yendo a por un botiquín, tics | 43 (140) | 2.458 (2.499) | 1.937 (2.759) | 335 (455) |
| con el canal del botiquín abierto, tics | 63,8 (63,1) | 110,9 (84,9) | 79,7 (98,7) | 88,2 (71,3) |
| con algún botiquín a bordo, tics | 4.898 (5.889) | 7.737 (7.010) | 7.618 (7.141) | 7.325 (7.064) |
| con un rival a la vista, parte de la vida | 86,2 % (84,6 %) | 86,0 % (85,3 %) | 86,2 % (82,6 %) | 86,8 % (80,7 %) |

Parte de la vida yendo a por un botiquín, por tramos de días:

| | días 1-5 | días 6-10 | días 11-15 | días 16-20 |
|---|---:|---:|---:|---:|
| ESPERANZA | 0,5 % | 0,1 % | 0,8 % | 0,0 % |
| BORRADO | 24,3 % | 11,2 % | 16,7 % | 22,9 % |
| APRENDE | 21,0 % | 13,6 % | 18,3 % | 13,0 % |
| TECHO | 2,7 % | 2,2 % | 4,2 % | 3,1 % |

## Sección 8 · Cómo muere

Causa = la fuente que más daño hizo en los últimos 30 tics. Para las muertes por rival, lo que más hacía en los 10 segundos anteriores (candidato en curso). Entre paréntesis, P7-10.

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| muertes por rival | 20 (14) | 12 (22) | 19 (28) | 21 (13) |
| … yendo a por un botiquín | 0 (0) | 6 (7) | 7 (13) | 1 (1) |
| … moviéndose paso a paso | 11 (6) | 2 (6) | 5 (7) | 10 (5) |
| … quieto | 2 (1) | 4 (8) | 1 (4) | 3 (1) |
| … peleando | 0 (2) | 0 (1) | 2 (1) | 0 (1) |
| … otra cosa | 7 (5) | 0 (0) | 4 (3) | 7 (5) |
| mueren dentro del círculo | 17 (14) | 9 (19) | 18 (27) | 19 (11) |
| mueren con algún botiquín a bordo | 3 (3) | 3 (4) | 7 (7) | 8 (5) |
| con un botiquín a la vista al morir (distancia mediana) | 12, a 3,4 | 7, a 3,2 | 14, a 3,2 | 15, a 2,2 |
| muertes por el anillo | 37 (41) | 37 (32) | 39 (36) | 35 (42) |
| sobreviven al final | 23 (25) | 31 (26) | 22 (16) | 24 (25) |

## Sección 9 · El sello, cifra a cifra

Evaluado una sola vez, al final, con `sello_P7_14b.py` → `P7_14b_sello_resultado.json`.

| pregunta | medida | resultado |
|---|---|---|
| **Q1 (principal). Con pedir, APRENDE ya no acaba peor que BORRADO** (|d̄| ≤ 2·se en puesto y en vida al morir, 80 pares) | puesto: APRENDE 5,59, BORRADO 4,36, d̄ 1,23, se 0,53 (FUERA); vida al morir: 8,7 y 11,3, d̄ -2,62, se 2,89 (dentro) | **falla** |
| **Q2. El círculo se rompe** (regalos por vida ≤ 0,534; vueltos a coger por vida ≤ 0,116) | regalos 56 en 80 vidas = 0,700 (P7-10: 2,138): no cumple; vueltos a coger 48 = 0,600 (P7-10: 1,163): no cumple | **falla** |
| **Q3. Días 11-20, el tiempo yendo a por botiquines de APRENDE no es mayor que el de BORRADO** | parte de la vida: APRENDE 15,7 %, BORRADO 19,8 % (1.735 y 2.632 tics por vida; 40 y 40 vidas) | **pasa** |
| **Q4. Se repite P7-10** (la creencia sube en 4 de 4; días 11-20, APRENDE usa con menos vida que BORRADO) | creencia día 5 → día 20: 5,7 → 37,2; 15,8 → 20,4; 27,8 → 31,3; 31,8 → 41,7: 4 de 4 (cumple); vida al usar: APRENDE 73,0 (38 usos), BORRADO 86,0 (62) (cumple) | **pasa** |
| **Q5. Menos de la quinta parte de los pedidos se cierran porque se lo dieron** | 95 de 1.042 cerrados (9,1 %); por brazo: ESPERANZA 0 de 187; BORRADO 2 de 248; APRENDE 56 de 295; TECHO 37 de 312 | **pasa** |

**Fuera del sello, para situar Q1** (misma medida, los otros pares; d̄ del primero menos el segundo, y su se):

| par | puesto: d̄ (se) | vida al morir: d̄ (se) |
|---|---:|---:|
| APRENDE − BORRADO (80 pares) | **1,23** (0,53) | -2,62 (2,89) |
| APRENDE − TECHO (80 pares) | 0,70 (0,57) | -1,12 (2,30) |
| APRENDE − ESPERANZA (80 pares) | 0,25 (0,62) | -0,42 (2,24) |
| BORRADO − TECHO (80 pares) | -0,53 (0,58) | 1,50 (3,04) |
| ESPERANZA − TECHO (80 pares) | 0,45 (0,63) | -0,70 (2,46) |
| ESPERANZA − BORRADO (80 pares) | 0,97 (0,54) | -2,20 (2,92) |

En negrita, |d̄| > 2·se. En P7-10 (sin pedir), APRENDE − BORRADO fue +1,25 (se 0,61) en puesto y −5,06 (se 2,33) en vida al morir (`informe_P7_10.md`).

**Lo que dice el sello.** La pregunta principal falla: con pedir, APRENDE sigue acabando peor que BORRADO en el puesto (la vida al morir sí queda
dentro de 2·se). La diferencia de puesto es casi la misma que en P7-10. Las dos mitades de Q2 fallan: los regalos bajan a un tercio de los de P7-10,
no a un cuarto, y los botiquines vueltos a coger bajan a la mitad, no a la décima parte. Q3, Q4 y Q5 pasan.

**Lo que el campo enseña del círculo, mirado después del sello** (declarado: son lecturas posteriores, no cambian el sello):

- **Ya no hay ningún regalo sin pedido**: los 95 regalos del campo (APRENDE 56, TECHO 37, BORRADO 2) se hicieron con el hermano pidiendo. La pieza
  hace lo que se diseñó, y el arreglo del empate también (ESPERANZA: 0 regalos; en P7-10 su SUELO hizo 24).
- **Pero quien pide casi nunca coge lo que le dan.** De los 56 regalos de APRENDE, 48 los vuelve a coger quien los dio, 7 los coge el hermano y 1
  seguía en el suelo; en TECHO, 23 y 14 de 37. En los 48 de APRENDE, el que pedía no llevaba ningún botiquín, estuvo a 1 casilla o menos de mediana
  del botiquín regalado (pasó por encima en 12) y no cogió ninguno; unos 280 tics después (lo que tarda en caducar la cesión en la memoria de quien
  da) el que lo dio lo recogió. En cuanto ve el botiquín, deja de pedir («lo ve» cierra 289 de 295 pedidos de APRENDE), y con el pedido cerrado el
  botiquín en el suelo ya no le vale nada a quien lo dio como regalo. El círculo sigue: es más pequeño y ahora empieza con un pedido.
- Esto ya pasaba en P7-10 (93 de 171 regalos vueltos a coger por quien los dio, a los 279 tics de mediana): no lo ha creado pedir. Por qué una
  criatura sin botiquín no coge uno que tiene a una casilla no lo sé; no lo he medido y no lo afirmo.
- **APRENDE va menos a por botiquines que en P7-10** (16,5 % de la vida frente a 22,5 %; BORRADO, 18,8 % frente a 18,9 %) y coge menos (186 frente a 297). Q3 pasa por eso.
- **El puesto de APRENDE no mejora con nada de eso**: 5,59 (5,91 en P7-10), y BORRADO 4,36 (4,66). Frente a TECHO y a ESPERANZA la diferencia de
  APRENDE queda dentro de 2·se; frente a BORRADO, fuera. BORRADO es en este campo el brazo que mejor acaba, por delante de TECHO.
- Las muertes por rival de APRENDE bajan (19; 28 en P7-10) y las de ESPERANZA y TECHO suben (20 y 21; 14 y 13): entre dos campos con semillas
  distintas eso puede ser ruido; dentro de este campo, APRENDE no muere más por rival que ESPERANZA o TECHO.

## Sección 10 · Créditos

| | partidas | créditos |
|---|---:|---:|
| ESPERANZA | 40 | 3,7655 USD |
| BORRADO | 40 | 3,4893 USD |
| APRENDE | 40 | 3,2347 USD |
| TECHO | 40 | 3,0775 USD |
| **P7-14b** | **160** | **13,5670 USD** |
| freno de P7-14 (no cuenta) | 3 | 0,2542 USD |
| **total del segundo campo** | **163** | **13,8212 USD** |

Media por partida de P7-14b: 0,0848 USD. Subir imágenes no gasta créditos. **Consola de Anthropic: 0 USD.**
Acumulado del siete en la plataforma: 29,8359 USD. Saldos: no consultados.

## Sección 11 · Lo que queda para la mesa

Propuestas y preguntas, nada decidido:

1. **La pregunta principal queda sin contestar a favor**: con pedir, APRENDE sigue peor que BORRADO en el puesto (+1,23, se 0,53), igual que en
   P7-10 (+1,25, se 0,61). Dos campos independientes, la misma diferencia. Sea lo que sea lo que separa a APRENDE de BORRADO, pedir no lo quita,
   y ya no puede ser el número de regalos ni el tiempo yendo a por botiquines, que en este campo son menores que en P7-10 o iguales a los de BORRADO.
2. **Lo único que distingue a APRENDE de BORRADO es que lee el cuaderno.** Los dos llevan el mismo código (esta vez sí: las cuatro imágenes salen del
   mismo sello). Lo que el cuaderno cambia es la creencia (20 a 42 al final), y con ella las ganas, la cura imaginada (usa con menos vida: 73 frente
   a 86 en los días 11 a 20) y el regalo. Cuál de esas tres cosas le cuesta el puesto pide un banco o brazos que las separen; no se puede leer de aquí.
3. **El regalo que nadie coge.** 48 de 56 regalos de APRENDE vuelven a quien los dio sin que el que pedía los toque. Antes de tocar nada conviene un
   banco de esas escenas: qué candidatos tiene el que pedía con el botiquín a una casilla y cuál gana. Puede ser una pieza del siete (el pedido se
   cierra al verlo, no al tenerlo) o algo del cuerpo.
4. **Cuándo se cierra un pedido.** Hoy se cierra al ver un botiquín, cualquiera. Si debería cerrarse al tenerlo es una decisión de diseño.
5. **Q2 se selló contra P7-10**; los topes (un cuarto y un décimo) no se alcanzan, pero la dirección es la prevista: 171 → 56 regalos, 93 → 48 vueltos a coger.
6. El precio por partida va de 0,026 a 0,118 USD, y 58 de las 160 costaron menos de 0,06: no sé de qué depende y no lo he investigado.

## Archivos

| archivo | qué es |
|---|---|
| `descubre_P7.py` (`DESPRENDERSE`, `desempate_sin_sitio`) | el arreglo: en un empate no se da ni se suelta nada |
| `banco_P7_14b.py`, `P7_14b_banco.json`, `P7_14b_F2.json`, `P7_14b_F1.json` | el banco del arreglo y F1 |
| `SELLO_P7_14b.md`, `semillas_P7_14b.json`, `lanza_P7_14b.py`, `P7_14b_estado.json`, `P7_14b_res/`, `cuadernos_P7_14b/` | sello, semillas, lanzador, estado, resultados y cuadernos |
| `freno_P7_14b.py`, `P7_14b_freno.json` | el freno |
| `campo_P7_14b.py` → `P7_14b_campo.json`; `analiza_P7_14b.py` → `P7_14b_vidas.json`; `sello_P7_14b.py` → `P7_14b_sello_resultado.json` | lectores y evaluador |
| `P7_14b_diarios_manifiesto.md` | md5 de los diarios (fuera de git) |
| `escribe_informe_P7_14b.py`, `informe_P7_14b.md` | este informe |
