# Paper ocho · El experimento de la base del ocho (prompt 99)

**Sobre el congelado `valle-congelado-v2`, con las predicciones selladas antes de jugar** (`predicciones_selladas_v2.md`).

**Las partidas:** 1.400 en la carpeta oficial `valle_experimento_v2`, sin fallos:
- RG50r, RG050r, S50, S050, P50, el tonto y el recolector;
- los cinco mundos, con el árbol encendido;
- semillas 30001–30040;
- 40 días.

`motor/model.py` md5 `1e511978c251130e95169ebf8443efa1`. Nada del congelado ha cambiado.

**Se cumplen 11 de las 12 predicciones. Falla P9** (punto 5).

**Tablas completas:**
- `salida/evalua_experimento_v2.md`, de `evalua_experimento_v2.py`;
- `salida/puerta_v53.json`;
- `salida/prueba_v53.json`.

## 1. La comprobación jugada, antes de sellar

**Con el árbol apagado, salen idénticos línea a línea** a los de antes (sin la lista «bestias» del registro):
- el tonto (normal, 1001, 40 días), frente al del experimento;
- RG49r (normal con los sabores, 9001, 10 días), frente a la del prompt 95.

**Preguntar a los valoradores no cambia nada.** Para P11, el lanzador pregunta a los tres valoradores en cada decisión de RG50r. RG50r con preguntas (19.105 decisiones apuntadas) y sin ellas da el mismo registro, línea a línea (normal con los sabores, 9001, 10 días).

## 2–3. El sellado y el push

- **El fichero:** `predicciones_selladas_v2.md` lleva tu texto de P1–P12 sin cambiar nada, el diseño, y una sección aparte («Cómo se mide cada una», escrita por mí antes de jugar) que fija cómo se mide y cuándo se cumple cada una.
- **El commit:** `648475e6`.
- **Las revisiones antes de subir,** las dos limpias: `revisa_subida.py` (0 correos, 0 claves, 0 rutas personales en 33.540 líneas nuevas) y `copia_taller.py --solo-buscar`.
- **El push** a GitHub, de la rama `paintball` (`648475e6`) y de la etiqueta `valle-congelado-v2` (`af7605a5`), confirmado con `git ls-remote`.
- **La hora del push que da GitHub:** **2026-11-06 23:13:42 UTC**, las 0:13:42 del 7 de noviembre en hora de aquí.
- **El experimento** empezó después, a las 0:14:00. Desde entonces no ha habido ningún otro push.

## 4. El experimento

- **De 0:14 del sábado 7 a 23:58.** Unas 23 h 45 min, 1.400 partidas sin fallos, con el Mac despierto y el lanzador reanudable (`lanza_experimento_v2.py`).
- **No se arregló nada durante el experimento.**
- **Un fallo en la evaluación, no en el experimento,** lo corregí al evaluar. `cierre_v46` solo pone «+sabores» en el nombre de las clases que empiezan por «RG», y S50, S050 y P50 también juegan con los sabores. Lo arreglé dentro de `evalua_experimento_v2.py`, sin tocar los scripts de antes ni las partidas.

## 5. Las predicciones

| | resultado | los números |
|---|---|---|
| **P1** | **cumple** | vivas RG50r − tonto: sequía +2,30 [+1,90, +2,73]; sequía dura +1,62 [+1,20, +2,05]; bestias que crían +2,45 [+1,95, +2,95] |
| **P2** | **cumple** | vivas de RG50r: abundancia 7,80; normal 7,88. Declarado: en el normal, RG50r − tonto = −0,10 [−0,23, +0,00] |
| **P3** | **cumple** | 0 muertes por golpe en las 1.400 partidas |
| **P4** | **cumple** | con la bestia a la vista, con otra pegada: RG50r 34,9 %, tonto 8,2 % (×4,3). Por mundo, RG50r 34–40 % y el tonto 3–11 % |
| **P5** | **cumple** | echadas por partida de RG50r en bestias que crían: 5,40 |
| **P6** | **cumple** | comida a la hermana · a cada vecina (las de las vecinas / 6): abundancia 713 · 58; normal 1.123 · 96; sequía 1.192 · 89; sequía dura 937 · 69; bestias que crían 1.371 · 114 |
| **P7** | **cumple** | parte de lo dado a quien estaba flaca: abundancia 33 %; sequía 71 %; sequía dura 87 % (normal 58 %, bestias que crían 88 %) |
| **P8** | **cumple** | pegada a una vecina, 5 días después − 5 días antes de perder a la hermana: +0,11 [+0,08, +0,14], 178 criaturas |
| **P9** | **falla** | de lo dormido, en su casa: abundancia 64,83 %, normal 65,19 %, sequía 64,98 %, bestias que crían 61,85 %, **sequía dura 59,64 %** (por debajo del 60 %) |
| **P10** | **cumple** | en la sequía, vivas RG050r − RG50r: +0,47 [+0,10, +0,85] (RG050r vive más) |
| **P11** | **cumple** | coincidencia de RG50r con las sumas, el cuarto más ambivalente menos el menos: −0,131 [−0,152, −0,111] (Q4 77,1 %, Q1 90,2 %; 10.000 decisiones de 200 partidas) |
| **P12** | **cumple** | fruta del árbol cogida: RG50r 3,6 %, el recolector 25,2 %; vueltas de RG50r al anochecer o de noche: 69 % de 678 |

## La tabla

**Vivas al día 40 (de 8; media de las 40 semillas):**

| mundo | tonto | recolector | RG50r | RG050r | S50 | S050 | P50 |
|---|---|---|---|---|---|---|---|
| abundancia | 8,00 | 7,92 | 7,80 | 7,90 | 7,88 | 7,92 | 7,88 |
| normal | 7,97 | 8,00 | 7,88 | 7,88 | 7,75 | 8,00 | 7,75 |
| sequía | 4,83 | 7,97 | 7,12 | 7,60 | 6,70 | 7,78 | 6,92 |
| sequía dura | 2,00 | 3,50 | 3,62 | 4,12 | 2,75 | 3,70 | 3,52 |
| bestias que crían | 3,55 | 5,60 | 6,00 | 6,53 | 5,12 | 6,47 | 5,75 |

**Diferencias por semillas emparejadas** (media [IC 95 %]):

| mundo | RG50r − RG050r | RG50r − tonto | RG050r − tonto | RG50r − recolector | RG50r − S50 | RG50r − P50 |
|---|---|---|---|---|---|---|
| abundancia | −0,10 [−0,28, +0,05] | −0,20 [−0,35, −0,07] | −0,10 [−0,23, +0,00] | −0,12 [−0,33, +0,07] | −0,07 [−0,23, +0,07] | −0,07 [−0,25, +0,07] |
| normal | +0,00 [−0,15, +0,15] | −0,10 [−0,23, +0,00] | −0,10 [−0,23, +0,00] | −0,12 [−0,25, −0,03] | +0,12 [−0,05, +0,33] | +0,12 [−0,10, +0,33] |
| sequía | −0,47 [−0,85, −0,10] | +2,30 [+1,90, +2,73] | +2,77 [+2,40, +3,15] | −0,85 [−1,12, −0,60] | +0,42 [+0,00, +0,88] | +0,20 [−0,10, +0,50] |
| sequía dura | −0,50 [−0,95, −0,05] | +1,62 [+1,20, +2,05] | +2,12 [+1,70, +2,55] | +0,12 [−0,28, +0,50] | +0,88 [+0,45, +1,30] | +0,10 [−0,33, +0,50] |
| bestias que crían | −0,53 [−0,93, −0,10] | +2,45 [+1,95, +2,95] | +2,98 [+2,40, +3,50] | +0,40 [−0,10, +0,88] | +0,88 [+0,42, +1,35] | +0,25 [−0,12, +0,65] |

**Los criterios de Manel:**
- **Casi todas vivas en abundancia y normal:** sí, todas las clases viven 7,75–8,00. En la abundancia, el tonto vive algo más que RG50r (−0,20 [−0,35, −0,07]).
- **En los mundos duros, al menos como el tonto:** sí, todas, y RG50r y RG050r de 1,6 a 3 más.
- **Frente al recolector:**
  - menos en la sequía (−0,85);
  - igual en la sequía dura;
  - algo más en bestias que crían (+0,40, con el intervalo tocando el cero).
- **Sin ganancias se vive más en los duros:** RG050r vive más que RG50r en la sequía, la sequía dura y bestias que crían (−0,47 a −0,53, los tres con el intervalo por debajo de cero).
- **Las sumas:** S50 vive menos que RG50r en la sequía dura y bestias que crían (+0,88).
- **Pelearse sí, matarse no:** ninguna muerte por golpe.
  - **Los empujones:** RG50r 124–284 por partida, RG050r 34–78.
  - **Las sumas empujan más:** S50 154–473 y P50 173–437.
- **Dormir:**
  - **cuánto:** duermen el 80–90 % de la noche;
  - **dónde:** en casa, RG50r el 60–65 % de lo dormido y RG050r el 72–79 %;
  - **lo que cuesta:** la bestia les pega dormidas fuera de 1,3 a 5,1 veces por partida.
- **Dar a quien lo necesita y a quién:**
  - **RG050r y S050** dan casi todo a quien está flaca (74–98 %).
  - **RG50r,** del 33 % (abundancia) al 88 %.
  - **S50 da muchísimo y a quien no lo necesita:** en la abundancia, 292 comidas por partida, el 9 % a quien estaba flaca y casi todas a la hermana.
- **Guardar:** en la despensa (13–205 por partida); el tonto y el recolector, en el almacén.
- **Juntarse ante la bestia:** con la bestia a la vista y otra pegada, RG50r 34–40 %, el tonto 3–11 %; S50 y S050 llegan al 44–63 %.
- **Echarla entre varias:** en bestias que crían, de 2,7 a 5,4 veces por partida según la clase, sobre todo con la hermana. Nunca la matan.
- **El duelo y la compañía:** tras perder a la hermana, RG50r pasa más tiempo con vecinas (+11 puntos, P8).
- **Lo que creen al acabar de dormir fuera:** de −0,86 (abundancia) a −2,48 (sequía dura) en RG50r. Incluye toda la vida perdida dormida, también la del hambre.
- **El árbol:**
  - **lo usan poco:** RG50r y RG050r lo descubren 14–58 criaturas por mundo, de 320, y cogen de 18 a 322 frutas de 4.040;
  - **el recolector** coge unas 1.000 por mundo;
  - **vuelven sobre todo de noche:** RG50r, más de la mitad de las veces;
  - **la bestia** les quita la dulce en el árbol de 1 a 12 veces por mundo.

## Gasto, tiempo y procesos

- **Gasto:**
  - créditos de la plataforma: 0;
  - dólares de la consola de Anthropic: 0.
- **Tiempo:**
  - estimé unas 24 h; han sido unas 24 h 20 min (de 23:55 del 6 a 0:15 del 8);
  - las partidas, 23 h 45 min.
- **Partidas:**
  - 1.400 del experimento;
  - 2 de puerta y 2 de prueba, en carpetas aparte.
- **Procesos vivos al acabar:** ninguno mío (comprobado con `ps` antes del commit; el único `caffeinate` es del propio Claude Code).
- **Commit:** local. No hay más push que el del sellado.
