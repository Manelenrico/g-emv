# Prompt 164: lo que hace sola la protagonista (RG69r+voz), todo con el v6, para la sección 5

*22-nov-2026. Solo cuentas sobre las partidas selladas del v6 (`valle_experimento_v6`, semillas 30161-30200, 40 días). No se ha jugado ni rejugado nada, no se ha editado ningún fichero existente y no se ha tocado `cantera/paper9`. Antes de empezar no había nada del chat de la curiosidad en marcha.*

- **Programa nuevo:** `seccion5_164.py`, que escribe `salida/seccion5_164.md` y `.json`.
  - Usa las medidas selladas del v6 donde existen, importadas de `evalua_experimento_v6.py` sin tocarlo: `cierre_v46`, `analiza_arbol_v50` y `medida_v4/dormir_v4`, con el intervalo del ocho (`evalua_experimento_v5.boot`: 10.000 remuestreos, semilla 8, 95 %).
  - **Comprobación:** donde se solapa con lo sellado, sale lo mismo. P4 da 30,8 % frente a 8,3 %; P5, 7,30; y P6, P7, P9, P12, P16 y la racha de P17 salen iguales. Los casos y controles de A2 son 136 y 378.
- **Citado:** dice «citado» y da el fichero y la línea.
- **Contado:** sale de `salida/seccion5_164.md`.
- **Gasto:** 0 créditos de la plataforma y 0 dólares de la consola.

## Resumen

Los cinco mundos juntos, la protagonista en el v6.

| número | v6, la protagonista | ¿predicción en el v6? | v5 (RG68r) |
|---|---|---|---|
| vivas el día 40 − el tonto | +1,70 [+1,46, +1,95] (contado) | P1 en tres mundos (se cumple); P2 en dos (se cumple) | P1, se cumple |
| vivas el día 40 − el recolector | +0,35 [+0,20, +0,53] (contado); en la sequía, **−0,17** [−0,33, −0,05] | no | sin diferencia emparejada; solo medias |
| muertes por golpe de otra criatura | 0 (citado) | P3, se cumple | P3, se cumple |
| con la bestia a la vista, con otra pegada | 30,8 % frente al 8,3 % del tonto (citado; por mundo, contado) | P4, se cumple | P4, se cumple (30,8 % · 8,9 %) |
| echa a la bestia, por partida | 1,52 (en bestias que crían, 7,30); con dos o más empujando, 303 de 304 (contado) | P5 solo en bestias que crían (se cumple) | P5, 5,75 |
| a la hermana frente a cada vecina | 24,9 veces más (contado) | P6, se cumple en los cinco | P6, se cumple |
| parte de lo dado a una flaca | 40,1 % (contado); del 6 % en la abundancia al 51 % en la sequía dura (citado) | P7, se cumple | P7, se cumple |
| noches dentro de una casa | 92,9 %; 0 en una puerta sin estar agotada (contado) | P9, se cumple | P9, se cumple |
| fruta del árbol dulce cogida | 2,6 % frente al 27,0 % del recolector (citado) | P12, se cumple | P12, se cumple |
| partidas con una racha de más de 10 regalos entre hermanas hartas | 1 de 200, la más larga de 15 (contado) | no tal cual. P17 cuenta todas las rachas (1 de 200, se cumple); la suya es esta misma | P17, 1 de 200, sin separar hartas |
| empujones por partida | 99,7 (contado); por mundo, citado | P16 (frente a RG068r, se cumple) | P16, se cumple |
| de ellos, a quien no lleva nada · sin hambre quien empuja | 3,6 % · 89,4 % (contado) | no | «la empujada lleva comida» del 93 al 98 %, sin predicción |
| tras morir la hermana: el duelo | sube de 0,05 a 1,64 y baja a la mitad en 5 días (mediana) (citado) | no: A4 | A4 (1,61; 6 días) |
| tras morir la hermana: la soledad | sube de 0,03 a 0,48; el día 15 sigue en 0,39, el 81 % de la subida (contado) | no: A4 | A4, sin el día 15 |
| tiempo pegada a una vecina, 5 días antes y después | +0,15 [+0,12, +0,18] (citado) | P8, se cumple | P8, se cumple (+0,11) |
| de día · de noche, pegada a una vecina | del 10 % al 27 % · del 7 % al 20 % (citado) | no: A2 | A2 |
| no vuelven a tener los tres balances sobre cero | 84 de 136 (62 %); en el control, 6 de 378 (2 %) (contado) | no | no existía |
| tras un robo, no vuelven a acercarse | el 4,5 %; las que vuelven, en una mediana de 0,35 días (contado) | no | no existía |
| tras un robo, el valor en el radar no vuelve | del 48 % al 57 % (citado, M6) | no: M6 | M6 (del 44 % al 54 %) |
| lo que se le da a la ladrona, después − antes | −0,0012 [−0,0027, −0,0001] comidas por día (contado) | no; M8, otra comparación (citado: igual) | M8, igual |

**Ojo, para el paper:** «no vuelve» de M6 (el valor de la ladrona en el radar de la robada) no es «no vuelve a acercarse». Por el radar no vuelve la mitad; acercarse, vuelve a acercarse casi siempre.

---

## Parte 1

**Citado:**
- **Vivas** (media de las 40 semillas): `informe_experimento_v6.md:42-48`.
- **Muertes por causa:** `informe_experimento_v6.md:55-61`. La protagonista no tiene ninguna por golpe; tampoco ninguno de los seis jugadores en las 1.200 partidas (P3, `:75`).
- **P1, P2, P4 a P7, P9, P12, P16 y P17:** `informe_experimento_v6.md:73-86`.

**Contado** (`salida/seccion5_164.md`):

| medida | abundancia | normal | sequía | sequía dura | bestias que crían | **los cinco** |
|---|---|---|---|---|---|---|
| vivas el día 40, protagonista − tonto [95 %] | +0,00 [+0,00, +0,00] | +0,00 [+0,00, +0,00] | +2,67 [+2,40, +2,98] | +2,67 [+2,27, +3,08] | +3,15 [+2,58, +3,73] | +1,70 [+1,46, +1,95] |
| vivas el día 40, protagonista − recolector [95 %] | +0,03 [+0,00, +0,07] | +0,03 [+0,00, +0,07] | −0,17 [−0,33, −0,05] | +0,80 [+0,38, +1,23] | +1,10 [+0,47, +1,70] | +0,35 [+0,20, +0,53] |
| muertes por golpe de otra criatura | 0 | 0 | 0 | 0 | 0 | 0 |
| con la bestia a la vista (fuera de casa), con otra pegada: protagonista | 50,6 % | 27,2 % | 35,6 % | 35,2 % | 29,0 % | 30,8 % |
| lo mismo, el tonto | 3,2 % | 3,8 % | 3,9 % | 3,5 % | 11,4 % | 8,3 % |
| echa a la bestia, veces por partida | 0,07 | 0,03 | 0,10 | 0,10 | 7,30 | 1,52 |
| de ellas, con dos o más empujando (de todas) | 3 (de 3) | 1 (de 1) | 4 (de 4) | 4 (de 4) | 291 (de 292) | 303 (de 304) |
| comida dada: a la hermana · a cada vecina (total) | 323 · 4,2 | 285 · 7,2 | 590 · 23,8 | 404 · 30,5 | 657 · 25,2 | 2 259 · 90,8 |
| cuántas veces más a la hermana | ×77,5 | ×39,8 | ×24,8 | ×13,2 | ×26,1 | ×24,9 |
| parte de lo dado a una flaca | 6,0 % | 28,4 % | 41,7 % | 50,9 % | 50,2 % | 40,1 % |
| noches dentro de su casa (en una puerta sin estar agotada) | 97,3 % (0) | 94,7 % (0) | 93,4 % (0) | 85,7 % (0) | 91,1 % (0) | 92,9 % (0) |
| fruta del árbol dulce cogida: protagonista | 0,5 % | 1,4 % | 1,7 % | 5,1 % | 4,1 % | 2,6 % |
| lo mismo, el recolector | 27,8 % | 28,0 % | 27,5 % | 24,6 % | 27,2 % | 27,0 % |
| partidas con una racha de más de 10 regalos entre hermanas hartas · la más larga | 0 de 40 · 7 | 0 de 40 · 3 | 0 de 40 · 7 | 0 de 40 · 3 | 1 de 40 · 15 | 1 de 200 · 15 |
| empujones a otras por partida | 67,1 | 120,1 | 107,5 | 72,6 | 131,2 | 99,7 |
| de ellos: a quien no lleva nada · sin hambre quien empuja · las dos | 1,4 % · 96,0 % · 1,4 % | 1,7 % · 93,1 % · 1,6 % | 4,0 % · 88,9 % · 3,6 % | 7,0 % · 83,6 % · 5,5 % | 4,5 % · 86,3 % · 3,5 % | 3,6 % · 89,4 % · 3,1 % |

**Lo que he tenido que decidir yo** (está también en la cabecera del programa):
- **«Con dos empujando»:** ese turno, dos o más criaturas empujan a esa bestia con resultado, como cuenta `analiza_v44`.
- **«Sin tener hambre»:** quien empuja tenía, el turno anterior, menos hambre que la de estar harta (15, `criaturas.harta_por_debajo` del mundo, leído; con menos no se puede comer).
- **«A quien no lleva nada»:** la empujada tenía la bolsa vacía el turno anterior.
- **«Hermanas hartas»:** las dos por debajo de 15 el turno anterior a cada regalo. La racha se cuenta como P17: ida y vuelta, con menos de 40 turnos entre regalos.
  - **La única racha de más de 10 de las 200 partidas (15) es la misma que dio P17, y es entre hermanas hartas.**
- **«Los cinco»** suma las 200 partidas. Las diferencias de vivas se emparejan por mundo y semilla (200 parejas).

**Para la sección 5:**
- casi nueve de cada diez empujones los da una criatura que no tiene hambre;
- casi todos van a quien lleva algo;
- y en la sequía la protagonista vive algo menos que el recolector.

## Parte 2. Tras morir la hermana

**Los casos y controles** son los de A2 y A4: 136 casos frente a 378 controles. El A4 del informe dice 135, porque necesita las filas de la otra.

**Citado:**
- **A2:** `informe_experimento_v6.md:162-172`. La felicidad funcional pasa del 29 % al 1 %. Pegada a una vecina: de día, del 10 % al 27 %; de noche, del 7 % al 20 %. 109 de 136 no recuperan la felicidad de antes.
- **A4:** `informe_experimento_v6.md:173-176` y la tabla en `duelo_soledad_v6.md:35-42`.
  - El duelo sube de 0,047 a 1,641 al día siguiente (peor día, 1,782) y baja a la mitad en una mediana de 5 días (109 de los 130 en que sube).
  - La soledad sube de 0,029 a 0,433 (peor día, 0,475) y solo baja a la mitad en 34 de 135 casos (mediana de 16 días).
- **P8** (el tiempo pegada a una vecina, 5 días antes y 5 después): +0,15 [+0,12, +0,18], con 137 criaturas (`informe_experimento_v6.md:80`).

**Contado:**

| grupo | soledad: 5 días antes | peor de los 5 después | el día 15 (las vivas ese día) | vivas el día 15 | no vuelven a tener los tres balances sobre cero |
|---|---|---|---|---|---|
| pierde a la hermana | 0,029 | 0,475 | 0,393 | 109 de 136 | **84 de 136 (61,8 %)** |
| la conserva (control) | 0,021 | 0,034 | 0,011 | 254 de 378 | 6 de 378 (1,6 %) |

- **La soledad quince días después:** en las 109 que siguen vivas ese día, queda en el 81 % de lo que subió (mediana, 87 %).
- **«No vuelven a tener los tres balances sobre cero»:** desde el día siguiente a la muerte hasta que acaba la partida o mueren, ningún turno despierta con los tres balances por encima de cero (de `balance.jsonl.gz`). En los controles se cuenta desde el mismo día.

## Parte 3. Tras un robo entre vecinas

**Qué es un robo:** como en M6 (`medidas_v6.py:44-49`), un empujón con ganadora que hace soltar algo a la otra, entre casas distintas.

**Citado: M6, el perdón** (`informe_experimento_v6.md:136`; tabla en `medidas_v6.md:83-92`). Cuántos días tarda la ladrona en volver a valer, en el radar de la robada, lo que valía el día del robo:
- de los que vuelven, la mediana es 1 día;
- del 48 % al 57 % no vuelven.

**Citado: M8** (`informe_experimento_v6.md:138`): las vecinas que le robaron reciben lo mismo que las que no (entre 0,000 y 0,004 comidas por día).

**Contado:**

| mundo | robos | se separan después | vuelven a acercarse | días hasta volver: mediana · media | no vuelven a acercarse | pares (robada, ladrona) | dado a la ladrona, comidas por día: antes · después |
|---|---|---|---|---|---|---|---|
| abundancia | 2 150 | 2 150 | 1 989 (92,5 %) | 0,30 · 1,92 | 161 (7,5 %) | 976 | 0,0030 · 0,0001 |
| normal | 3 786 | 3 781 | 3 606 (95,4 %) | 0,41 · 1,62 | 175 (4,6 %) | 1 404 | 0,0012 · 0,0005 |
| sequía | 3 179 | 3 179 | 3 031 (95,3 %) | 0,41 · 1,62 | 148 (4,7 %) | 1 315 | 0,0037 · 0,0021 |
| sequía dura | 1 923 | 1 922 | 1 867 (97,1 %) | 0,41 · 1,18 | 55 (2,9 %) | 921 | 0,0027 · 0,0037 |
| bestias que crían | 3 768 | 3 766 | 3 637 (96,6 %) | 0,29 · 1,22 | 129 (3,4 %) | 1 433 | 0,0036 · 0,0018 |
| **los cinco** | 14 806 | 14 798 | 14 130 (95,5 %) | 0,35 · 1,50 | 668 (4,5 %) | 6 049 | 0,0028 · 0,0016 |

**Lo que se le da a la ladrona, después menos antes, por par:** −0,0012 [−0,0027, −0,0001] comidas por día (6 049 pares). Es algo menos después, pero es muy poco: casi nunca se dan comida entre vecinas, antes ni después.

**Lo que he tenido que decidir yo:**
- **«Vuelve a acercarse»:** se separan (más de 1 casilla) y luego vuelven a estar a 1 o menos, las dos vivas. Se cuenta con cada robo, como M6.
- **Los robos:** aquí son 14 806. M6 cuenta 13 676, porque deja fuera los que no tienen el valor del radar de ese día.
- **Lo dado:** se cuenta con el primer robo de cada par, como P14 del v5.

## Parte 4. Qué era cada número

**En el v6** (`predicciones_selladas_v6.md`):

| número | qué era en el v6 | el texto sellado | ¿se cumple? |
|---|---|---|---|
| vivas − tonto | **P1** (`:36`) | «En sequía, sequía dura y bestias que crían, RG69r+voz vive al menos una criatura más que el tonto, con el intervalo por encima de cero.» | sí |
| | **P2** (`:37`) | «En abundancia y normal, RG69r+voz vive de media al menos 7,5 de 8. Declarado: en el normal, el tonto puede vivir algo más.» | sí |
| vivas − recolector | medida sin predicción; lo nuevo, aquí | — | — |
| muertes por golpe | **P3** (`:38`) | «Ninguna muerte por golpe entre criaturas en ningún mundo.» | sí |
| bestia a la vista, con otra pegada | **P4** (`:39`) | «Con la bestia a la vista, la fracción de veces con otra pegada es al menos el triple en RG69r+voz que en el tonto.» | sí (×3,7) |
| echar a la bestia | **P5** (`:40`) | «En bestias que crían, RG69r+voz echa la bestia al menos una vez por partida de media.» | sí. «Con dos empujando», sin predicción |
| hermana frente a vecina | **P6** (`:41`) | «RG69r+voz da más comida a la hermana que a cada vecina, por cabeza, en todos los mundos.» | sí |
| dar a una flaca | **P7** (`:42`) | «La parte de lo que RG69r+voz da a quien está flaca es mayor en sequía y en sequía dura que en abundancia.» | sí |
| noches dentro | **P9** (`:44`) | «RG69r+voz duerme dentro de su casa al menos el 55 % de las noches en los cinco mundos, y ninguna noche en una puerta sin estar agotada.» | sí |
| fruta del árbol | **P12** (`:46`) | «Sin razón, RG69r+voz coge menos del 15 % de la fruta del árbol y menos que el recolector.» | sí |
| rachas de regalos | **P17** (`:49`), sin separar las hartas | «Hay rachas de regalos de ida y vuelta de más de 10 en 4 o menos de las 200 partidas de RG69r+voz.» | sí (1 de 200). «Hartas», sin predicción |
| empujones por partida | **P16** (`:48`) | «RG69r+voz empuja más que RG068r en los cinco mundos.» | sí. A quién y con qué hambre, sin predicción |
| pegada a una vecina tras morir la hermana | **P8** (`:43`) | «En los cinco días siguientes a la muerte de la hermana, RG69r+voz pasa más tiempo con vecinas que en los cinco anteriores, emparejado por criatura.» | sí |
| duelo y soledad | medida sin predicción, **A4** (`:91`) | — | — |
| de día y de noche con vecinas; la felicidad | medida sin predicción, **A2** (`:90`) | — | — |
| soledad el día 15; los tres balances | lo nuevo, aquí | — | — |
| el perdón (radar) | medida sin predicción, **M6** (`:86`) | — | — |
| lo dado a la ladrona | medida sin predicción, **M8** (`:88`), otra comparación | — | — |
| volver a acercarse; lo dado antes y después | lo nuevo, aquí | — | — |

**En el v5** (`predicciones_selladas_v5.md`, con RG68r; los resultados, en `informe_experimento_v5.md`):
- **Las mismas predicciones, con RG68r:** P1 a P9 (`:27-35`), P12 (`:38`), P16 (`:40`, «(cambia)») y P17 (`:41`, «(cambia)»). Todas se cumplen (`informe_experimento_v5.md:39-53`):
  - P1: +2,70 · +1,52 · +2,90;
  - P2: 7,95 y 7,83;
  - P4: 30,8 % frente a 8,9 %;
  - P5: 5,75;
  - P6 y P7, en los cinco mundos;
  - P8: +0,11 [+0,08, +0,14];
  - P9: del 72 % al 82 % dentro;
  - P12: 3,0 % frente a 28,8 %;
  - P16, en los cinco;
  - P17: 1 de 200, de 24.
- **Las mismas medidas sin predicción:** M6 (`:61`), M8 (`:66`, «era P14»), A2 (`:71`) y A4 (`:72`). Resultados en `informe_experimento_v5.md:114-131`:
  - M6: del 44 % al 54 % no vuelven;
  - A2: 159 casos y 518 controles; 139 de 159 no recuperan la felicidad;
  - A4: el duelo, a 1,61, baja a la mitad en 6 días; la soledad baja a la mitad en 30 de 159.
- **Lo que en el v5 no existía como número:**
  - las vivas frente al recolector, emparejadas (solo las medias, `tabla_experimento_v5.md:3-9`);
  - «con dos empujando» (sí «echan con la hermana · con vecinas», `tabla_experimento_v5.md:239`: 182 · 48 en bestias que crían);
  - las rachas entre hermanas hartas;
  - los empujones sin hambre. Sí estaba «la empujada lleva comida», del 93 al 98 %, en `tabla_experimento_v5.md:290-314`;
  - la soledad el día 15, los tres balances, volver a acercarse y lo dado antes y después.

  Para tenerlos con RG68r bastaría pasar el mismo programa a `valle_experimento_v5`: unos 15 minutos, sin rejugar. No lo he hecho.

## Procesos y gasto

- **Órdenes sueltas, declaradas:** solo de lectura (`grep`, `sed`, `ls`), una prueba de `seccion5_164.una` en una partida y un `python3 -` para arreglar dos líneas del programa antes de pasarlo.
- **Gasto:** 0 créditos de la plataforma y 0 dólares de la consola.
