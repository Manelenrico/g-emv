# La escalera con la reserva: predicciones selladas

*19-nov-2026. Se escribe antes de jugar ninguna partida de S69+voz o P69+voz en las semillas 30161 a 30200. Se apoya en el v6 sellado (`valle-congelado-v6`); el v5 y el v6 siguen como se sellaron y este fichero no cambia ninguno de los dos. Después de sellar no se cambia ningún umbral ni ningún texto de predicción. Lo que no se cumpla se cuenta igual.*

## Los jugadores

- **RG69r+voz** (`RG69rvoz` en las carpetas), la protagonista del v6.
  - Es RG68r con la reserva del 146 y la voz de ir a casa del 143: la clase `cuerpo_vr1.RG69V`.
  - **No se vuelve a jugar:** sus 200 partidas se leen de `valle_experimento_v6`, el v6 sellado.
- **S69+voz** (`S69voz`): el valorador de sumas del v5 (S68) con la reserva y la voz.
- **P69+voz** (`P69voz`): el valorador de posición del v5 (P68) con la reserva y la voz.
- **Las mismas filas que RG69r+voz; solo cambia cómo se componen.**
  - Las dos son la misma clase `cuerpo_vr1.RG69V`, sin código nuevo de criatura. Llevan los interruptores de S68 (`sumas_v29`) o de P68 (`posicion_v30`), más los dos de RG69r+voz (`reserva_v69` y `a_casa`).
  - La segunda foto de la voz también compone con su valorador (`VC1._vc_d` llama a `_compone`).
  - `model.py` no se toca y no se edita ninguna clase congelada.

## El diseño

- **Las partidas:** S69+voz y P69+voz, cada uno en los cinco mundos del v6, con el árbol y los sabores. Son las semillas 30161 a 30200, 40 días.
  - En total, 2 × 5 × 40 = **400 partidas**, en la carpeta nueva `valle_escalera_v6`.
- **El lanzador** es `lanza_escalera_v6.py`. Importa sin tocarlo el lanzador sellado del v6 (`lanza_experimento_v6.py`): su `una`, sus registros y la clase de cada jugador. Le añade los dos jugadores nuevos.
- **El evaluador** es `evalua_escalera_v6.py`. Importa sin tocarlas las piezas del evaluador sellado del v6 (`evalua_experimento_v6.py`).

## Las predicciones

Intervalos por bootstrap de 10.000 remuestreos con semilla 8, como en el v6.

| | qué se predice | se cumple si |
|---|---|---|
| **E1** | Con los cinco mundos juntos, RG69r+voz vive más que S69+voz. Vivas el día 40, diferencia emparejada por mundo y semilla; la medida se calcula como en `motor_frente_simple_v5.md` | el límite de abajo del intervalo del 95 % está por encima de cero |
| **E2** | En la sequía, RG69r+voz vive más que S69+voz | el límite de abajo del intervalo está por encima de cero |

**Cuentan dos.**

## Lo que se declara (no cuenta como predicción)

- **RG69r+voz frente a P69+voz no se predice;** se mide igual, en los cinco mundos juntos y en la sequía.
- **El lado de RG69r+voz ya se ha visto** en el v6. El de S69+voz y P69+voz no se ha jugado nunca.
- **La ventaja puede encogerse.** El efecto del v5 (RG68r − S68, los cinco juntos: +0,41 [+0,27, +0,57], `motor_frente_simple_v5.md`) se midió sobre la base vieja. La reserva quitó la mayor discrepancia entre el motor y las sumas: las decisiones de comer en los momentos más ambivalentes (prompt 151, punto 5).
- **Las gemelas sin ganancias no se vuelven a jugar:** eso queda como lo midió el v5.

## Las medidas sin predicción

Por mundo, **RG69r+voz − S69+voz** y **RG69r+voz − P69+voz**, emparejadas por semilla, con su intervalo:
- las vivas el día 40;
- las muertes de hambre;
- los turnos al día despierta con hambre de más de 30 y comida en la bolsa, días 0 a 9;
- las noches dormidas fuera, días 0 a 9;
- los empujones;
- la felicidad de la aldea.

Y las **muertes por causa** de los tres jugadores.

## Cómo se mide

Todo sale de `evalua_escalera_v6.py`, con las piezas importadas del evaluador sellado del v6:

| medida | de dónde |
|---|---|
| vivas el día 40 | 8 menos las muertes de `fin.json` (`cierre_v46`, como en el v6 y en `motor_frente_simple_v5.py`) |
| E1 | las 200 parejas, en el orden de `motor_frente_simple_v5.py` (mundo y, dentro, semilla), con su mismo bootstrap |
| E2 | las 40 parejas de la sequía |
| muertes por causa y de hambre | `fin.json` (`cierre_v46`) |
| turnos con hambre > 30 y comida en la bolsa, días 0 a 9 | `hambre_ganancias_v1/extrae_hg_v1`, la medida de P24 |
| noches dormidas fuera, días 0 a 9 | `voz_a_casa_v1/analiza_vc1`, la medida de P28. Aquí va por partida: las noches fuera entre las noches |
| empujones a otra criatura | `cierre_v46`, la medida de P16 |
| felicidad de la aldea | `evalua_experimento_v5.v5`, la medida de P26 |

## Antes de sellar

**Las puertas** (`lanza_escalera_v6.py puerta`, `salida/puerta_escalera_v6.json`): partidas de 40 días, sin los registros. Se comparan línea a línea: muertes, criaturas al acabar, mundo y criaturas. **3 de 3 idénticas.**

| partida | frente a | idéntica |
|---|---|---|
| S69+voz con la reserva y la voz apagadas, sequía dura 30121 | S68 sellada del v5 | sí |
| P69+voz con las dos apagadas, sequía dura 30121 | P68 sellada del v5 | sí |
| RG69r+voz con este lanzador, sequía dura 30161 | la del v6 sellado | sí |

**La prueba de 10 días** (`lanza_escalera_v6.py prueba`, `salida/prueba_escalera_v6.json`), en la sequía 30121, una semilla ya vista. Solo se mira si la reserva actúa y si la voz suena; no se han mirado vivas ni muertes.

| | fotos de comer con la reserva | criaturas que la usan | voces | decisiones oyendo | registros escritos |
|---|---|---|---|---|---|
| S69+voz | 12.224 | 8 de 8 | 97 | 2.743 | todos |
| P69+voz | 12.557 | 8 de 8 | 73 | 1.927 | todos |

**El evaluador, probado** (`evalua_escalera_v6.py prueba`). Corre de principio a fin sobre partidas ya selladas del v6, RG68r y RG068r puestas con los nombres nuevos por enlaces, semillas 30161 a 30163. Esos números no son de los jugadores nuevos y no cuentan. En la primera prueba faltaba una carpeta de la caché (`noches`); se arregló antes de sellar.

**Las semillas:** ni en el disco «Mem G-EMV» ni en el repositorio hay ninguna partida, carpeta ni programa con S69voz o P69voz, en ninguna semilla. Las semillas 30161 a 30200 no se han jugado nunca con ellos. La carpeta `valle_escalera_v6` no existe todavía.

**Las huellas (md5):**

| fichero | md5 |
|---|---|
| `lanza_escalera_v6.py` (el lanzador) | `a144ce48e3ec82b0cb9ac330f0381e73` |
| `evalua_escalera_v6.py` (el evaluador) | `c36e5c219712418ed0c29c12341d7131` |

Lo que importan, igual que en `congelado_v6/md5_v6.md`, el v6 sellado:

| fichero | md5 |
|---|---|
| `lanza_experimento_v6.py` | `b2e1b7077c3fe81cc5b874ec64757e87` |
| `evalua_experimento_v6.py` | `763dec488835e0783231b6acf2d7d193` |
| `cuerpo_vr1.py` | `82a02353b66626a783ec03d8795be243` |
| `cuerpo_rg69.py` | `393a909fcb095e8a09a230f8170f5fa0` |
| `cuerpo_vc1.py` | `80f68dbc62c538e8a83af53d4a4bb2ec` |
| `lanza_vc1.py` | `5e232b2e0cdcfd479ffbc3a06fa94ac8` |
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` |

La huella de este fichero de predicciones se apunta en el commit del sellado y en el informe, porque no puede ir dentro de él mismo.
