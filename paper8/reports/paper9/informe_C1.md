# Curiosidad · prompt C1 · inventario y cuentas, solo lectura

*21-nov-2026. Del chat de la curiosidad, no del ocho. No se ha jugado ninguna partida, no se ha editado ningún fichero existente ni nada de `cantera/paper8`, y no se ha usado la clave. Todo lo nuevo está en `cantera/paper9/`.*

Las rutas son relativas a `cantera/`. El mundo está fuera: lo cito como `../valle/…`. Siglas:
- **CV** = `paper8/cuerpo_valle.py` (la criatura del valle);
- **C5** = `paper5/curiosidad.py`;
- **X** = `paper7/descubre_P7.py` («la curiosidad» del siete);
- **N29** = `paper7/nace_P7_29.py` («el cuánto»);
- **CU** = `paper7/cuaderno_P7.py`;
- **MU** = `../valle/mundo.py`;
- **CVJ** = `paper8/config_cuerpo_valle.json`.

**Antes de empezar comprobé que no había nada del ocho en marcha.** El único proceso vivo era un `caffeinate -i -t 300`, hijo del propio Claude Code (no de un programa del ocho).

**Ficheros nuevos:**
- `paper9/cuentas_C1.py`: las cuentas de la parte 3.
- `paper9/tablas_C1.py`: las tablas.
- `paper9/salida/cuentas_C1.json` y `paper9/salida/tablas_C1.md`.
- Este informe.

Quedan fuera del commit, porque son datos partida a partida: la caché (`paper9/cuentas_C1_cache/`, 200 ficheros) y `salida/cuentas_C1.json` (14 MB; se rehace con `python3 cuentas_C1.py`, que lee la caché).

**STATUS.md no lo he tocado.** La regla de siempre pide una línea en él, pero este prompt dice que no se edita ningún fichero existente, y he seguido el prompt. Si quieres la línea, dímelo.

**Órdenes sueltas, declaradas.** Además de los dos programas, usé órdenes sueltas de Python solo para mirar:
- imprimir los interruptores de RG69r+voz y de S69+voz, importando los lanzadores sin lanzar nada;
- ver las claves de los registros de unas partidas;
- construir el mapa del mundo sin reiniciarlo;
- buscar en una partida las salidas de bolsa sin explicación;
- meter las tablas en este informe.

---

## Parte 1. Inventario de la curiosidad en el código

**Cómo se juega la protagonista.** RG69r+voz es la clase `cuerpo_vr1.RG69V`, con los interruptores de `B7.VARS["RG69rvoz"]` (`paper8/lanza_experimento_v6.py:33, 35`).
- El que importa aquí es **`regla_general=True`**.
- Las dos clases hijas (`paper8/cuerpo_rg69.py`, `paper8/cuerpo_vc1.py`) no tocan ninguna curiosidad: no hay ninguna línea con «CURIOSIDAD», «frontera» ni «ignorancia».

| # | Pieza | Fichero y línea | Qué mide | Fórmula, en llano | Dominio | Qué la calla | Interruptor | ¿Viva en RG69r+voz? |
|---|---|---|---|---|---|---|---|---|
| 1 | **R-CURIOSIDAD-TERRENO** (el cinco, modo «local») | C5:44, :142-165, :344-347 | lo que queda sin ver alrededor de la casilla a la que iría (radio 6), descontando lo que vería al llegar | k × ignorancia local proyectada × (1 − amenaza) | recursos: reparto (0,1 · 0,8 · 0,1), C5:49; es dolor, no apetitiva (C5:386-388) | la amenaza (la balanza: armados a la vista, daño reciente, anillo; C5:226-282); haberlo visto todo; k = 0 | `GEMV_CURIOSIDAD=local`, con `GEMV_CURIOSIDAD_K` y `GEMV_CURIOSIDAD_BALANZA` (`../paintball/alma/policy_forma.py:75-78`) | **No.** No está portada al valle. |
| 2 | **R-CURIOSIDAD-FRONTERA** (el cinco, modo «frontera») | C5:51, :167-177, :183-215, :335-343 | lo lejos que está la casilla de lo no visto más cercano, por lo que queda sin ver del mapa | k × ignorancia global × (1 − amenaza) × (1 − g(distancia)), con g = (1 − d/24)³, la caída de R-LLAMADA (importada, C5:167-177) | recursos (0,1 · 0,8 · 0,1); dolor | la amenaza; no quedar nada por ver; k = 0 | `GEMV_CURIOSIDAD=frontera` (policy_forma.py:70-78); en el campo P5-7C, k = 0,2 con balanza (CVJ:147-150, «_fuente») | No en esta forma: vive la del valle (fila 6). |
| 3 | La curiosidad como **forma** (el cinco, P5-8) | `paper5/curiosidad_forma.py:1-17`; policy_forma.py:80-87 | el cuerpo se propone ir a la frontera, y la puerta de las formas lo juzga | no la he leído entera: solo la cabecera y sus mandos (consigna 0,5; refractario 50) | — | — | `GEMV_CURIOSIDAD_FORMA=1` (necesita `GEMV_FORMA=1`) | **No.** No está en el valle. |
| 4 | **R-CURIOSIDAD**, «la curiosidad» (el siete) | X:136-152, :289, :349-350 | no saber qué hace el botiquín | ACOPIO_M × calma × ignorancia del botiquín × alivio. **Calma** = 1 − la más alta de cinco filas de miedo (F-4-ALCANCE, S-7-AGRESOR, F-HERMANO-AMENAZA, F-HERMANO-GOLPE, F-ANTICIPACION; X:61, :136-137). **Alivio**: 1 sin botiquín, 0,5 con él en el zurrón, 0 en la foto de usarlo (X:141-149). | recursos (REPARTO_CUR 0,1 · 0,8 · 0,1, X:60, :289); dolor | el miedo (la calma); saberlo (la ignorancia baja con los recuerdos, CU:95-97); llevarlo encima | `GEMV_P7_NOVEDAD` (y no `GEMV_P7_SABE`) (X:56, :289, :349) | — |
| 4b | R-CURIOSIDAD **en el valle** | CV:1643, :1653; ign_botiquin en CV:2299, :2645, :2706 | lo mismo, con la medicina | ACOPIO_M × calma × ignorancia de la medicina en su cuaderno × (0,5 si la lleva) | recursos (CV:35) | la calma; saberlo; llevarla | **ninguno propio**: está en `_filas_orig`. La quita la regla general (CV:2189). | **No.** La regla general la quita. |
| 5 | **R-CURIOSIDAD-CUANTO**, «el cuánto» (el siete) | N29:30-37, :48, :99-100, :161-170, :189, :212 | no saber cuánto da una cosa ya probada | ACOPIO_M × calma × media, por cosa conocida, de (ignorancia del cuánto × alivio). **Ignorancia del cuánto** = 1 / (1 + pesos de los recuerdos firmes, sin «al menos»). **Alivio**: 0,5 solo en la foto de usarla cuando lo que le falta es más que lo más alto que ya sabe que da (N29:30-34). | el texto dice «Dominio: el cuerpo» (N29:35), pero entra con el reparto de recursos, REPARTO_CUR (N29:189). Las dos cosas constan así. | la calma; recuerdos firmes; no faltarle nada | `GEMV_P7_29`, `E["arreglos"]["cuanto"]` y `GEMV_P7_NOVEDAD` (N29:47, :49, :189, :210-212) | — |
| 5b | R-CURIOSIDAD-CUANTO **en el valle** | CV:802-826, :1654 | lo mismo, para la comida y la medicina | igual que la fila 5. Lo que le falta: el hambre (comida) y vida máxima − vida (medicina) (CV:816-826; CVJ «curiosidad_cuanto») | recursos (CV:35) | la calma; recuerdos firmes | ninguno propio; la quita la regla general (CV:2189) | **No.** La regla general la quita. |
| 6 | **R-CURIOSIDAD-FRONTERA en el valle** | CV:764-800 (traducción), :1655, :2199-2200 (regla general), :2316-2320 (falta_saber); el viaje `ir_frontera` en CV:2835-2837 | lejos de lo no visto, por lo que le falta saber de dónde hay comida | **Sin la regla general:** k × ignorancia global × (1 − amenaza) × (1 − g(d)), con k = 0,2 (CVJ:147-150). **Con la regla general**, la ignorancia global se cambia por `falta_saber`: k × (1 − amenaza) × (1 − g(d)) × max(0, 1 − matorrales en `self.mat` / matorrales que dice la cultura). La amenaza es la bestia a 1 casilla, que cae a 0 en el radio de vista (no cuenta dentro de casa), el daño de los últimos 9 turnos y el anillo de la cultura (CV:782-794). | recursos (C5.REPARTO_CUR, CV:36); dolor. Con las ganancias de la regla general sale también su ganancia, «G-R-CURIOSIDAD-FRONTERA» (CV:2225-2236). | la amenaza. Se apaga para siempre cuando `self.mat` llega a lo que dice la cultura o cuando ya no queda casilla pisable sin ver (sin frontera, la fila vale 0, CV:798-799). **Ojo:** `self.mat` cuenta también las plantas del huerto (interruptor `plantas`, CV:740) y el árbol. | **ninguno**: no hay interruptor para quitarla. La regla general la reescribe. | **Sí.** Es la única viva, con la fórmula de la regla general, más el candidato `ir_frontera`. |

**Resumen.** En RG69r+voz solo vive una curiosidad: **R-CURIOSIDAD-FRONTERA, con la fórmula de la regla general** («saber dónde hay comida es un recurso»), y su viaje `ir_frontera`.
- «La curiosidad» (la medicina) y «el cuánto» se calculan en `_filas_orig`, pero la regla general las quita antes de valorar (CV:2189).
- Las del cinco (terreno y forma) no existen en el valle.

## Parte 1b. Por qué se apagaron «la curiosidad» y «el cuánto»

**Lo que consta, con su sitio:**
1. **La propuesta de la regla general** (`paper8/propuesta_regla_general.md`, commit `17439069`, 28-oct-2026, «propuesta de la criatura de regla general (solo propuesta, para Manel)»):
   - :5: «quitarle a la criatura todo lo que es una orden o una pieza hecha para una conducta».
   - :9: la marca **P** = «nació como parche para conseguir una conducta (entre paréntesis, el prompt)».
   - :53: «R-CURIOSIDAD, R-CURIOSIDAD-CUANTO, R-CURIOSIDAD-FRONTERA | curiosidad por lo que no sabe y por lo no visto | P (12)».
   - :199: «La curiosidad (frontera y cuánto) es lo más dudoso. Sin ella, puede que no exploren. Propongo quitarla en la primera prueba y ver; si no exploran, es un resultado».
   - :228: «Explorar: sin la curiosidad, probablemente poco».
2. **El código**, que dice quién lo decidió:
   - CV:292-294: «(prompt 39, Manel) la criatura de regla general … Sin las piezas hechas para una conducta (ver `_filas_rg`)».
   - CV:2185-2189: el docstring («las filas que ya existían …, menos las hechas para una conducta») y la línea que las quita.
   - CV:2317: «(prompt 39, Manel) saber dónde hay comida es un recurso».
3. **El primer informe de la regla general** (`paper8/informe_regla_general_v1.md`, commit `ceed87de`):
   - :24: «Fuera: las piezas hechas para una conducta: F-ANTICIPACION, R-LLAMADA (el botín), la curiosidad del botiquín y la del cuánto, R-ENFADO, …».
   - :30-32: «La curiosidad, dentro de la regla. Saber dónde hay comida es un recurso»; la frontera se queda, con la necesidad «1 − matorrales que conoce / los que dice la cultura».
4. **Por qué se llamaban «de conducta»** (de dónde vienen):
   - el informe del cuerpo v1 dice que «No salen a buscar» (`paper8/informe_cuerpo_valle_v1.md:86`) y pregunta si portar el cuánto (:97);
   - el v2, del prompt 12, las porta (`paper8/informe_cuerpo_valle_v2.md:1, 11, 14`).
5. **Después:** `paper8/informe_regla_general_v6.md:137` lo repite: «la curiosidad por la medicina y la de "cuánto" se quitaron en el v1».

**Lo que no consta.**
- El texto del prompt 39 de Manel no está en el repositorio. Su decisión solo consta por los comentarios del código que se la atribuyen («(prompt 39, Manel)»).
- La razón escrita es la de la propuesta: son piezas nacidas en el prompt 12 para una conducta (explorar), y la regla general quita esas piezas.
- **No encontré ninguna otra razón**, como una medida que dijera que no servían. No la deduzco.

## Parte 2. Qué guarda el cuaderno de cada cosa del valle

*Esta parte la leyó un agente de ayuda dentro de la sesión, solo leyendo. Comprobé a mano estas citas, y cuadran:*
- *CU:90-97 (`pesos_vividos` e `ignorancia`);*
- *CV:1350-1356 (`p_matorral` con `frec`);*
- *CV:561-566 (los hechos de la bestia; solo se cargan «echar» y «matar»);*
- *CV:2302-2314 (`comidas_dos_dias` y `falta_comida`);*
- *`paper8/lanza_experimento_v5.py:61-66` (`cuaderno_sitios.json`);*
- *que en CV no hay ninguna lectura de «hecho:» ni la palabra «epoca» (grep: 0).*

*Las demás citas de la tabla son del agente y no las he comprobado una a una.*

**Tres hechos de partida:**
- **La cultura.** Hereda la cultura «medio» (`paper8/lanzador.py:86`). Cada entrada entra en el cuaderno como 1 recuerdo «heredado» de intensidad 1, por `radar_v39`, con sus campos `da`, `por_turnos`, `retraso`, `dura`, `empieza`, `por_100_casillas` y `viene` (CV:542-552). Lo heredado no se olvida (`cultura_sin_olvido_v22`).
- **Lo que enseña el mundo.** De cada casilla a la vista: los objetos del suelo, la planta (frutos, trabajo) y el matorral (frutos, zona) (MU:1118-1132). De su bolsa, solo los tipos (y el origen) (MU:723-726).
- **La pudrición** existe en el mundo (MU:170), pero **no sale en lo que ve** la criatura.

| Cosa | Qué dato guarda | De dónde lo aprende | Qué NO guarda |
|---|---|---|---|
| **Matorrales del bosque** | `self.mat[casilla] = {zona, t, frutos, vacio_desde}` (CV:749). `self.frec[(fruto o vacío, tramo de tiempo)] = [con fruto, veces]`: **un solo contador para todos los matorrales y plantas**, sin zona (CV:744-746). `self.vueltas` (CV:748). En el cuaderno, `matorral\|bosque`: heredado 0,5 de recursos y `por_100_casillas` (cultura); un recuerdo vivido por visita, 1 con fruto y 0 sin fruto (CV:751-752). | **Lo ve.** El mundo publica todos los matorrales en el mapa (MU:134), pero CV no lo lee: solo sabe los que ha visto (CV:740-749). | No guarda cuántos frutos hay, solo «hay o no hay» (CV:1353-1356). Ni cuánto le queda al fruto para pudrirse. `frec` no se olvida y no separa zona ni día. |
| **Matorrales salvajes** | Lo mismo, con zona «salvaje» (CV:740, :749, :752). | **Lo ve.** La cultura solo habla del bosque. | Que dan 2 frutos y no 1 (`../valle/config_valle.json` → matorrales): `frec` los mezcla. Su fruta lleva el origen «bosque» (MU:1098). |
| **Árbol dulce** | En el mundo es un matorral de zona «arbol» con 20 frutas. Ella lo guarda en `self.mat` como un matorral más (CV:739-749). El sabor de la fruta dulce, al comerla (CV:1910-1918). Dos hechos heredados, «aparece un árbol de fruta dulce» y «al atardecer la bestia pasa por los árboles» (CV:554-560; `paper8/cultura_hechos_v50.json`). | **Lo ve**, **lo vive** (el sabor) y **lo hereda** (los dos hechos). | Los dos hechos entran con efecto vacío y **ningún código los lee**; el propio código dice «no dicen dónde ni cuándo» (CV:554). No guarda cuándo aparece ni cuándo se va. Cuando se va, su entrada en `self.mat` se queda. |
| **Plantas del huerto** | `self.plantas_vistas[q] = {trabajo, frutos, t}` (CV:1445). `self.mat` con zona «huerto» (CV:740). `self.trabaje` (CV:693-695). `trabajar\|huerto`: heredado (lo que tarda el fruto) y vivido (CV:1455). | **Lo ve**, **lo vive** y **lo hereda**. | El cuidado de la planta: el mundo lo enseña, pero CV no lo lee. Que la época también toca al huerto. |
| **Almacén** | `self.almacen_visto` = el nivel (vacío, poco, a medias, lleno), solo en la aldea (CV:757). En la foto pasa a comidas (CVJ `comidas_por_nivel`) y cuenta 1/8 en R-CARENCIA (CV:2313). | **Lo ve** (el nivel) y **lo vive** (coger). | El número exacto. Cuándo lo vio por última vez. Que allí la comida no se pudre. |
| **Despensa** | `self.despensa_vista` = las comidas de su despensa, solo dentro de su casa (CV:758). Cuenta entera en lo que tiene (CV:2313). | **Lo ve.** | La hora en que la vio. Las despensas de las otras casas. Lo que dura allí (la cultura dice 1.600; no se lee: solo se lee lo de la bolsa, CV:2305). |
| **Bolsa** | Los tipos y el origen que da el mundo. La foto copia la lista. `guardar:comida` heredado, con «dura en la bolsa» 800, que lee `comidas_dos_dias` (CV:2305). | **Lo ve** y **lo hereda** (lo que dura). | Lo podrida que está cada comida: no la ve. |
| **Bestia** | `self.bestia`: dónde está, solo mientras la ve (si no, nada) (CV:727). Las últimas distancias (CV:726). En el cuaderno: `bestia\|noche` (heredado −1,5, empieza en el turno 280) y vivido cada noche fuera; `bestia\|golpe_visto`, mirando; `dormir\|fuera` y `\|casa`. Los números de echar y matar (CV:561-566). | **Lo ve**, **lo vive**, **lo aprende mirando** y **lo hereda**. | Dónde estaba la última vez: lo borra. Su vida. El hecho de las bestias y las épocas no se carga (CV:565). |
| **Zona salvaje (hiere)** | `sitio:salvaje\|dia` y `\|noche`, heredados. Vivido por estancias: la vida perdida por turno y los objetos nuevos vistos (CV:1399-1426). Se lee en la foto como daño por turno de cada terreno (CV:846-849). | **Lo vive**, **lo hereda** y **lo aprende mirando**. | Qué casilla hiere: guarda una cuenta por terreno. Ni la regla del mundo (probabilidad y daño). |
| **Medicina** | `medicina\|valle` heredado (40), vivido al tomarla y visto (CV:672-683, :1021). `self.medicinas`: dónde la ve (CV:1414-1416). | **Lo vive**, **lo ve**, **lo aprende mirando** y **lo hereda**. | Medicinas en sitios que no ve. |
| **Hermana** | Dónde está, si está herida o flaca, su nivel de vida y lo que lleva, mientras la ve (CV:715). El trato aprendido del radar (CV:1949-1951). En el cuaderno, `criatura:<hermana>\|cerca` y `\|trato`, heredado y vivido cada mirada (CV:1869-1885). **La voz de ir a casa recibe del lanzador dónde está, si duerme y si vive, la vea o no** (`paper8/cuerpo_vc1.py:12-13, 28, 75-79`). | **Lo ve**, **lo vive** y **lo hereda**; la voz, **se lo dice el lanzador**. | Su hambre y su vida exactas. Sus costumbres: `imagina_v45` está apagado. |
| **Cada una de las otras criaturas (vecinas)** | `self.otras[x] = {pos, flaca, herida, lleva, t, vida_nivel}` (CV:1042). El vínculo, sustituido por el trato del radar (CV:1952). `criatura:x\|cerca` y `\|trato`: nace al verla y se vive cada mirada. Los robos vistos (CV:1932-1941). | **Lo ve**, **lo vive**, **lo aprende mirando**. | Lo mismo que de la hermana. Y de las vecinas no le llega nada desde el lanzador. |
| **Épocas de la sequía** | **Nada.** En «sequía» las épocas duran 5 días, con factores 1,3 · 1,0 · 0,7 · 1,0, y tocan matorrales y huerto (MU:468-477, :1072, :1090-1095); en la sequía dura, × 0,7 (MU:254-257). | **No lo aprende de ningún modo.** Recibe el día, no la época. | El factor, el nombre y la duración de la época. |

**Pregunta 1. ¿Hay un número que diga cuánto se fía de cada creencia, y se puede leer desde fuera?**
- **En el cuaderno, sí.**
  - `pesos_vividos(objeto)` es la suma de los pesos de todos sus recuerdos (CU:90-93). Ojo: a pesar del nombre, suma también los heredados y los vistos.
  - El peso de cada recuerdo es intensidad × 0,95 por día.
  - `ignorancia(objeto)` = 1 / (1 + esa suma) (CU:95-97).
  - `ignorancia_cuanto` hace lo mismo solo con los recuerdos firmes (CV:806-810).
  - Fuera del cuaderno está `frec`: (0,5 + con fruto) / (1 + veces), donde «veces» hace de cuántos recuerdos (CV:1355-1356).
- **Desde fuera, solo para los sitios.**
  - Lo único guardado al acabar cada partida es `cuaderno_sitios.json`: solo los objetos `sitio:*`, cada recuerdo con su día, efecto, importancia, intensidad y origen (`paper8/lanza_experimento_v5.py:61-66`). Con eso se rehacen sin tocar nada el peso y la ignorancia de los sitios.
  - De comida, medicina, matorral, bestia, dormir, trabajar, cada criatura, el sabor de cada fuente y `frec` **no hay nada guardado**.
  - `fin.json` trae 5 creencias sin peso. `radar_dia.json` no trae pesos.
  - Para tenerlo haría falta volcar el cuaderno entero al acabar (`CU.creencias()`/`volcado()` ya calcula ignorancia y pesos) y `frec`. Eso pide rejugar con un registro nuevo. No lo he hecho.

**Pregunta 2. ¿Sabe que la comida va por épocas, o cuándo aparece el árbol?**
- **De las épocas, nada.** No le llegan en lo que ve ni están en su código ni en su cultura. El único hecho que habla de ellas se descarta al cargar (CV:561-566).
- **Del árbol, solo dos hechos heredados** que nadie lee («no dicen dónde ni cuándo», CV:554).
- Lo que sí hace es guardarlo como un matorral cuando lo ve y aprender el sabor dulce al comerlo.
- No sabe que se va. Su entrada en `self.mat` se queda, y `p_matorral` no mira la zona.

**Pregunta 3. ¿La imagen a 44 turnos cuenta que la comida se pudre?**
- **La foto no pudre nada.** En la bolsa, la planta, el matorral, la despensa y el almacén, la comida solo cambia al comer, coger, dejar, dar o perder un empujón (CV:2546-2645).
- **La pudrición entra solo por un número de la cultura:** lo que dura la comida en la bolsa (800 turnos), dentro de `comidas_dos_dias` (CV:2302-2308). Esa cuenta da cuántas comidas se comerá antes de que se le pudran: (hambre + lo que sube por turno × 800) / lo que quita una comida.
- Ese número es «lo que necesita» en R-CARENCIA (CV:2310-2314) y en la escala de los recursos (CV:2274-2276).
- La despensa (1.600) y el almacén (no se pudre) se miden con el mismo horizonte de la bolsa, porque solo se lee `.get("bolsa")` (CV:2305).
- La promesa de fruto de un matorral es una frecuencia vivida que mezcla lo comido y lo podrido sin separarlos (CV:1353-1356).

## Parte 3. Cuentas sobre las 200 partidas selladas de RG69r+voz (v6)

**Qué hay guardado y qué no.** Lo dice la cabecera de `paper9/cuentas_C1.py`, con las líneas de los lanzadores y del mundo. Lo que pesa para estas cuentas:
- **Las filas:** de cada decisión **solo se guardaron cinco filas** (S-DUELO-CUERPO, S-DUELO-RECURSOS, S-DUELO-VINCULO, S-SOLEDAD, S-COMPANIA; `paper8/lanza_experimento_v5.py:5-6, 31, 52-57`), no todas las de pérdida.
- **La comida:** el mundo lleva un libro diario de lo que aparece, se come, se pudre y come la bestia (`Valle.cuadre` y `stats`, MU:702-709, :1045), pero **no se escribió** en las partidas: no está en `fin.json` ni en ningún fichero.
- **Los objetos:** de los frutos de plantas y matorrales hay una foto cada 4 turnos (MU:733-737). Del almacén y las despensas no hay nada.
- **Lo que ve la criatura:** no se guardó (ni `self.mat` ni `self.vistas`).

Por eso hay tres clases de números, y cada tabla dice de cuál es:
- **contados:** salen tal cual del registro;
- **reconstruidos con las reglas del mundo:** el almacén, la comida podrida en la bolsa y lo que conoce cada criatura;
- **cotas:** la calma.

**Cómo se comprobaron.**
- **El almacén reconstruido** cuadra con el registro: no baja nunca de cero, y las 6 veces que «coger del almacén» falla por «no hay», el almacén reconstruido está a cero.
- **La comida podrida en la bolsa:** al principio salía de más, porque yo apuntaba lo soltado en un empujón a la criatura equivocada (lo suelta la que pierde). Lo corregí. Lo que queda sale de las bolsas hacia el turno 800, que es cuando llega a sus 800 turnos en la bolsa la comida cogida al empezar. Lo miré en una partida.
- **Lo que ve** (3c) se reconstruye con la regla del mundo: el cuadrado de lado 2·vista+1, sin paredes que tapen (MU:1118-1130), con la vista de la fase de cada turno. Se supone que mira cada turno que está viva. No se puede comprobar contra lo que guardaba la criatura, porque no se guardó.

**Tres avisos para leer las tablas** (solo cómo se cuenta; no propongo causas):
- **3a, la calma:** la definición fijada pide todas las filas de pérdida; con solo cinco guardadas, **lo que se cuenta es una cota**: la calma de verdad es igual o menor. Las decisiones incluyen las de dormir (de noche casi todas son «dormir»). Un rato de calma lo corta cualquier turno sin fila de decisión, y esos turnos no son pocos (la última tabla de 3a).
- **3b, el huerto:** cada ciclo de una planta dura 800 turnos (2 días; `../valle/config_valle.json` → huerto.ciclo_turnos) y, con el arranque, las plantas maduran a la par. Así, en un tramo de 5 días caen unas veces 3 cosechas y otras 2. **La cifra del huerto sube y baja de un tramo a otro por eso también, no solo por la época:** en la abundancia, donde el factor es 1,3 siempre, va de 217 a 135 y vuelve a 204.
- **3b, abundancia y sequía en los días 1-5:** salen iguales. En esos días las dos tienen el mismo factor (1,3) y las mismas semillas.

### Comprobaciones de las cuentas

- Partidas leídas: 200 (40 por mundo); todas llegan al turno 15999–15999.
- El almacén reconstruido no baja nunca de cero (mínimo 0), y de las 6 veces que «coger del almacén» falla por «no hay», 0 caen con comida en el almacén reconstruido.
- Mapa: 2304 casillas del valle, 2292 pisables, 992 de bosque; la cultura dice 2,0192 matorrales por 100 casillas de bosque: 20,03 esperados.
- Matorrales en el mapa (bosque, salvajes), en el turno 0 de las 40 partidas de cada mundo: abundancia [(21, 5)]; normal [(21, 5)]; sequía [(21, 5)]; sequía dura [(21, 5)]; bestias que crían [(21, 5)].

### 3a. Calma y holgura (cota: solo las cinco filas guardadas y la bestia)

#### Umbral 0,05

| mundo | parte del día | decisiones por partida | en calma (cota) | ratos por partida | dura de media (turnos) | mediana | el más largo | quedarse | andar | trabajar | dormir | lo demás |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| abundancia | mañana | 30903 | 97,6 % | 1427 | 24,7 | 4 | 397 | 75,5 % | 5,8 % | 14,0 % | 0,0 % | 4,7 % |
| abundancia | tarde | 30103 | 98,0 % | 1243 | 45,6 | 4 | 707 | 84,0 % | 5,7 % | 5,5 % | 0,1 % | 4,7 % |
| abundancia | anochecer | 11896 | 98,9 % | 221 | 38,4 | 1 | 337 | 1,5 % | 1,4 % | 0,3 % | 96,6 % | 0,2 % |
| abundancia | noche | 35954 | 99,0 % | 1104 | 6,0 | 1 | 325 | 0,1 % | 0,0 % | 0,0 % | 99,9 % | 0,0 % |
| normal | mañana | 27280 | 94,3 % | 1728 | 17,1 | 3 | 457 | 71,8 % | 8,0 % | 15,5 % | 0,1 % | 4,7 % |
| normal | tarde | 26952 | 94,4 % | 1455 | 31,9 | 3 | 598 | 82,5 % | 7,0 % | 5,5 % | 0,6 % | 4,4 % |
| normal | anochecer | 11078 | 97,0 % | 332 | 34,9 | 1 | 398 | 1,4 % | 1,9 % | 0,3 % | 96,1 % | 0,3 % |
| normal | noche | 35097 | 97,0 % | 1232 | 6,8 | 1 | 247 | 0,1 % | 0,1 % | 0,0 % | 99,8 % | 0,0 % |
| sequía | mañana | 26243 | 89,5 % | 1646 | 16,5 | 3 | 397 | 71,0 % | 8,2 % | 15,8 % | 0,1 % | 4,8 % |
| sequía | tarde | 26359 | 89,5 % | 1408 | 29,6 | 3 | 707 | 81,1 % | 7,5 % | 5,6 % | 0,6 % | 5,1 % |
| sequía | anochecer | 10661 | 92,5 % | 350 | 31,3 | 1 | 549 | 1,6 % | 2,1 % | 0,5 % | 95,5 % | 0,3 % |
| sequía | noche | 34089 | 92,3 % | 1319 | 6,5 | 1 | 325 | 0,1 % | 0,1 % | 0,0 % | 99,6 % | 0,0 % |
| sequía dura | mañana | 16967 | 44,1 % | 624 | 13,8 | 2 | 350 | 68,4 % | 9,9 % | 16,6 % | 0,2 % | 4,9 % |
| sequía dura | tarde | 17520 | 41,0 % | 523 | 22,7 | 2 | 397 | 79,8 % | 9,4 % | 6,0 % | 0,8 % | 4,0 % |
| sequía dura | anochecer | 6390 | 46,8 % | 145 | 27,9 | 1 | 337 | 2,1 % | 2,6 % | 0,6 % | 94,1 % | 0,5 % |
| sequía dura | noche | 22526 | 44,3 % | 481 | 6,4 | 1 | 233 | 0,4 % | 0,2 % | 0,1 % | 99,2 % | 0,1 % |
| bestias que crían | mañana | 22024 | 76,0 % | 1574 | 12,9 | 2 | 415 | 67,1 % | 11,0 % | 16,3 % | 0,3 % | 5,3 % |
| bestias que crían | tarde | 23894 | 78,3 % | 1295 | 23,3 | 2 | 620 | 79,5 % | 8,6 % | 6,0 % | 1,2 % | 4,7 % |
| bestias que crían | anochecer | 9532 | 82,5 % | 359 | 27,4 | 1 | 489 | 1,8 % | 2,6 % | 0,7 % | 94,4 % | 0,5 % |
| bestias que crían | noche | 31736 | 82,0 % | 1292 | 7,0 | 1 | 244 | 0,4 % | 0,3 % | 0,1 % | 99,2 % | 0,1 % |

#### Umbral 0,1

| mundo | parte del día | decisiones por partida | en calma (cota) | ratos por partida | dura de media (turnos) | mediana | el más largo | quedarse | andar | trabajar | dormir | lo demás |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| abundancia | mañana | 30903 | 98,8 % | 1486 | 24,0 | 4 | 397 | 74,9 % | 6,0 % | 14,4 % | 0,0 % | 4,7 % |
| abundancia | tarde | 30103 | 98,9 % | 1284 | 44,4 | 4 | 707 | 83,7 % | 5,9 % | 5,7 % | 0,1 % | 4,7 % |
| abundancia | anochecer | 11896 | 99,3 % | 228 | 37,2 | 1 | 337 | 1,5 % | 1,5 % | 0,4 % | 96,5 % | 0,2 % |
| abundancia | noche | 35954 | 99,2 % | 1116 | 6,0 | 1 | 325 | 0,1 % | 0,1 % | 0,0 % | 99,8 % | 0,0 % |
| normal | mañana | 27280 | 96,8 % | 1836 | 16,5 | 2 | 457 | 70,8 % | 8,3 % | 16,1 % | 0,1 % | 4,7 % |
| normal | tarde | 26952 | 96,7 % | 1546 | 30,5 | 2 | 598 | 81,8 % | 7,3 % | 5,8 % | 0,6 % | 4,4 % |
| normal | anochecer | 11078 | 98,1 % | 348 | 33,3 | 1 | 398 | 1,5 % | 2,0 % | 0,4 % | 95,8 % | 0,3 % |
| normal | noche | 35097 | 97,4 % | 1263 | 6,7 | 1 | 249 | 0,1 % | 0,1 % | 0,1 % | 99,7 % | 0,0 % |
| sequía | mañana | 26243 | 94,6 % | 1798 | 16,0 | 2 | 536 | 70,3 % | 8,5 % | 16,4 % | 0,1 % | 4,8 % |
| sequía | tarde | 26359 | 94,3 % | 1521 | 28,6 | 2 | 707 | 80,7 % | 7,6 % | 5,9 % | 0,6 % | 5,1 % |
| sequía | anochecer | 10661 | 96,1 % | 374 | 30,0 | 1 | 550 | 2,0 % | 2,2 % | 0,6 % | 94,8 % | 0,4 % |
| sequía | noche | 34089 | 94,9 % | 1383 | 6,4 | 1 | 325 | 0,3 % | 0,2 % | 0,1 % | 99,4 % | 0,0 % |
| sequía dura | mañana | 16967 | 52,3 % | 747 | 13,9 | 2 | 351 | 68,4 % | 9,6 % | 17,0 % | 0,2 % | 4,8 % |
| sequía dura | tarde | 17520 | 49,7 % | 617 | 23,0 | 2 | 397 | 80,4 % | 8,9 % | 6,3 % | 0,7 % | 3,8 % |
| sequía dura | anochecer | 6390 | 55,7 % | 167 | 27,1 | 1 | 337 | 2,3 % | 2,6 % | 0,8 % | 93,8 % | 0,6 % |
| sequía dura | noche | 22526 | 51,5 % | 550 | 6,6 | 1 | 233 | 0,6 % | 0,3 % | 0,1 % | 98,9 % | 0,1 % |
| bestias que crían | mañana | 22024 | 84,6 % | 1790 | 12,7 | 2 | 416 | 66,5 % | 11,1 % | 16,8 % | 0,3 % | 5,3 % |
| bestias que crían | tarde | 23894 | 87,3 % | 1454 | 22,6 | 2 | 620 | 79,4 % | 8,5 % | 6,2 % | 1,1 % | 4,7 % |
| bestias que crían | anochecer | 9532 | 89,4 % | 402 | 26,0 | 1 | 489 | 2,5 % | 2,7 % | 0,8 % | 93,3 % | 0,7 % |
| bestias que crían | noche | 31736 | 87,6 % | 1404 | 6,9 | 1 | 244 | 0,7 % | 0,3 % | 0,1 % | 98,8 % | 0,1 % |

#### Umbral 0,2

| mundo | parte del día | decisiones por partida | en calma (cota) | ratos por partida | dura de media (turnos) | mediana | el más largo | quedarse | andar | trabajar | dormir | lo demás |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| abundancia | mañana | 30903 | 99,5 % | 1523 | 23,6 | 3 | 397 | 74,4 % | 6,1 % | 14,7 % | 0,0 % | 4,7 % |
| abundancia | tarde | 30103 | 99,5 % | 1316 | 43,5 | 3 | 707 | 83,5 % | 6,0 % | 5,8 % | 0,1 % | 4,7 % |
| abundancia | anochecer | 11896 | 99,8 % | 235 | 36,3 | 1 | 337 | 1,5 % | 1,5 % | 0,4 % | 96,3 % | 0,2 % |
| abundancia | noche | 35954 | 99,4 % | 1132 | 5,9 | 1 | 325 | 0,1 % | 0,1 % | 0,1 % | 99,8 % | 0,0 % |
| normal | mañana | 27280 | 98,7 % | 1927 | 16,0 | 2 | 457 | 69,9 % | 8,6 % | 16,7 % | 0,1 % | 4,7 % |
| normal | tarde | 26952 | 98,6 % | 1637 | 29,2 | 2 | 598 | 81,1 % | 7,6 % | 6,2 % | 0,6 % | 4,5 % |
| normal | anochecer | 11078 | 99,1 % | 365 | 32,1 | 1 | 398 | 1,5 % | 2,1 % | 0,5 % | 95,6 % | 0,3 % |
| normal | noche | 35097 | 98,1 % | 1320 | 6,5 | 1 | 249 | 0,1 % | 0,1 % | 0,1 % | 99,6 % | 0,0 % |
| sequía | mañana | 26243 | 97,5 % | 1917 | 15,4 | 2 | 536 | 69,2 % | 8,9 % | 17,0 % | 0,2 % | 4,8 % |
| sequía | tarde | 26359 | 97,1 % | 1632 | 27,3 | 2 | 707 | 80,0 % | 8,0 % | 6,2 % | 0,7 % | 5,2 % |
| sequía | anochecer | 10661 | 98,1 % | 401 | 28,7 | 1 | 443 | 2,0 % | 2,3 % | 0,7 % | 94,5 % | 0,5 % |
| sequía | noche | 34089 | 96,8 % | 1472 | 6,1 | 1 | 325 | 0,3 % | 0,2 % | 0,1 % | 99,3 % | 0,0 % |
| sequía dura | mañana | 16967 | 63,4 % | 911 | 13,8 | 2 | 351 | 66,8 % | 9,8 % | 18,6 % | 0,2 % | 4,7 % |
| sequía dura | tarde | 17520 | 60,5 % | 758 | 22,6 | 2 | 592 | 80,1 % | 8,9 % | 6,7 % | 0,7 % | 3,6 % |
| sequía dura | anochecer | 6390 | 67,4 % | 204 | 26,1 | 1 | 337 | 2,5 % | 2,7 % | 0,8 % | 93,3 % | 0,7 % |
| sequía dura | noche | 22526 | 61,9 % | 678 | 6,8 | 1 | 233 | 0,9 % | 0,3 % | 0,2 % | 98,6 % | 0,1 % |
| bestias que crían | mañana | 22024 | 90,9 % | 2003 | 12,2 | 2 | 416 | 64,7 % | 11,8 % | 17,9 % | 0,3 % | 5,3 % |
| bestias que crían | tarde | 23894 | 93,3 % | 1626 | 21,5 | 2 | 620 | 78,2 % | 9,1 % | 6,8 % | 1,2 % | 4,7 % |
| bestias que crían | anochecer | 9532 | 94,7 % | 449 | 24,6 | 1 | 489 | 2,7 % | 2,9 % | 1,0 % | 92,5 % | 0,8 % |
| bestias que crían | noche | 31736 | 92,4 % | 1559 | 6,7 | 1 | 244 | 0,8 % | 0,4 % | 0,2 % | 98,6 % | 0,1 % |

Decisiones sin dato (sin fila guardada ese turno): 0.

Turnos despierta sin fila de decisión (cortan los ratos), por parte del día, todas las partidas:

| mundo | mañana | tarde | anochecer | noche |
|---|---|---|---|---|
| abundancia | 19,5 % | 21,6 % | 56,9 % | 57,2 % |
| normal | 29,0 % | 29,9 % | 70,1 % | 66,7 % |
| sequía | 31,0 % | 30,7 % | 69,4 % | 60,7 % |
| sequía dura | 36,3 % | 34,1 % | 75,6 % | 48,2 % |
| bestias que crían | 39,6 % | 34,4 % | 70,5 % | 54,2 % |

### 3b. La comida por tramos de cinco días (media por partida)

Ventana de cada tramo: turnos (2000k, 2000(k+1)] (el último, hasta el 15.996). «Matorrales (neto)» = lo que dieron menos lo que se pudrió en la mata; no se pueden separar. «Podrido en la bolsa» es reconstruido. La despensa no está en lo guardado: su pudrición no se puede contar.

#### Lo que da el valle y lo que se recoge

| mundo | días | época | huerto (da) | matorrales (neto) | árbol (da) | árbol (se pierde al irse) | bayas sueltas | coge de plantas | coge de matorrales | coge del árbol | coge del almacén | coge de la despensa | coge del suelo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| abundancia | 1-5 | abundancia ×1,30 | 217,3 | 32,1 | 10,5 | 3,0 | 10,9 | 144,0 | 16,1 | 0,0 | 48,0 | 55,2 | 32,3 |
| abundancia | 6-10 | normal ×1,30 | 135,5 | 22,4 | 12,5 | 11,5 | 10,9 | 161,4 | 21,9 | 0,0 | 0,0 | 61,9 | 12,6 |
| abundancia | 11-15 | escasez ×1,30 | 203,6 | 23,1 | 13,0 | 14,2 | 10,2 | 150,4 | 23,2 | 0,3 | 0,0 | 48,3 | 9,9 |
| abundancia | 16-20 | normal ×1,30 | 135,8 | 21,1 | 20,5 | 13,5 | 10,6 | 162,3 | 20,9 | 0,0 | 0,0 | 44,7 | 7,9 |
| abundancia | 21-25 | abundancia ×1,30 | 204,0 | 22,4 | 14,0 | 17,3 | 10,0 | 150,0 | 22,7 | 0,2 | 0,0 | 45,4 | 8,8 |
| abundancia | 26-30 | normal ×1,30 | 135,8 | 21,5 | 19,0 | 15,5 | 10,6 | 160,8 | 20,6 | 0,1 | 0,0 | 41,7 | 9,9 |
| abundancia | 31-35 | escasez ×1,30 | 203,7 | 21,4 | 11,5 | 17,9 | 9,8 | 150,5 | 22,2 | 0,0 | 0,0 | 49,9 | 8,6 |
| abundancia | 36-40 | normal ×1,30 | 135,6 | 22,3 | 3,5 | 11,0 | 9,4 | 161,1 | 20,7 | 0,0 | 0,0 | 48,3 | 8,3 |
| normal | 1-5 | — | 166,9 | 31,7 | 10,5 | 3,0 | 7,7 | 121,3 | 19,9 | 0,0 | 48,0 | 42,2 | 31,1 |
| normal | 6-10 | — | 105,0 | 28,6 | 12,5 | 11,5 | 7,9 | 127,5 | 28,4 | 0,0 | 0,0 | 45,7 | 12,4 |
| normal | 11-15 | — | 156,3 | 28,7 | 13,0 | 14,1 | 8,2 | 120,4 | 29,7 | 0,5 | 0,0 | 37,8 | 10,2 |
| normal | 16-20 | — | 104,4 | 30,6 | 20,5 | 13,4 | 7,9 | 126,3 | 29,8 | 0,1 | 0,0 | 33,7 | 9,9 |
| normal | 21-25 | — | 156,2 | 29,9 | 14,0 | 17,5 | 8,1 | 119,1 | 29,9 | 0,0 | 0,0 | 40,9 | 9,3 |
| normal | 26-30 | — | 104,7 | 29,1 | 19,0 | 15,4 | 8,0 | 125,9 | 29,0 | 0,2 | 0,0 | 39,1 | 10,2 |
| normal | 31-35 | — | 157,0 | 29,6 | 11,5 | 17,6 | 8,0 | 119,3 | 29,8 | 0,5 | 0,0 | 49,8 | 9,2 |
| normal | 36-40 | — | 104,7 | 29,7 | 3,5 | 10,6 | 7,8 | 127,1 | 29,4 | 0,2 | 0,0 | 48,1 | 9,6 |
| sequía | 1-5 | abundancia ×1,30 | 217,3 | 32,0 | 10,5 | 3,0 | 10,9 | 144,0 | 16,1 | 0,0 | 48,0 | 55,2 | 32,3 |
| sequía | 6-10 | normal ×1,00 | 105,2 | 22,1 | 12,5 | 11,5 | 7,8 | 139,5 | 25,7 | 0,3 | 0,0 | 68,0 | 10,9 |
| sequía | 11-15 | **escasez ×0,70** | 109,8 | 26,7 | 13,0 | 14,1 | 4,8 | 89,7 | 32,2 | 0,3 | 0,0 | 34,6 | 5,1 |
| sequía | 16-20 | normal ×1,00 | 104,0 | 41,9 | 20,5 | 13,2 | 7,2 | 111,5 | 36,5 | 0,4 | 0,0 | 37,4 | 7,8 |
| sequía | 21-25 | abundancia ×1,30 | 203,0 | 28,5 | 14,0 | 17,2 | 10,3 | 144,4 | 24,5 | 0,2 | 0,0 | 67,0 | 11,2 |
| sequía | 26-30 | normal ×1,00 | 103,8 | 19,9 | 19,0 | 15,3 | 7,5 | 136,0 | 24,1 | 0,0 | 0,0 | 70,0 | 6,8 |
| sequía | 31-35 | **escasez ×0,70** | 109,4 | 25,2 | 11,5 | 17,9 | 5,8 | 88,3 | 30,8 | 0,1 | 0,0 | 44,2 | 6,0 |
| sequía | 36-40 | normal ×1,00 | 104,0 | 40,1 | 3,5 | 10,6 | 7,7 | 111,5 | 34,5 | 0,4 | 0,0 | 46,0 | 8,3 |
| sequía dura | 1-5 | abundancia ×0,91 | 150,8 | 28,6 | 10,5 | 3,0 | 7,3 | 111,5 | 18,2 | 0,0 | 48,0 | 49,0 | 33,1 |
| sequía dura | 6-10 | normal ×0,70 | 73,4 | 25,3 | 12,5 | 11,4 | 5,6 | 96,2 | 28,1 | 0,2 | 0,0 | 34,8 | 7,2 |
| sequía dura | 11-15 | **escasez ×0,49** | 77,3 | 22,9 | 13,0 | 13,1 | 3,7 | 59,9 | 26,1 | 2,1 | 0,0 | 4,7 | 2,5 |
| sequía dura | 16-20 | normal ×0,70 | 72,7 | 23,1 | 20,5 | 11,6 | 5,5 | 65,4 | 18,6 | 1,4 | 0,0 | 7,5 | 2,6 |
| sequía dura | 21-25 | abundancia ×0,91 | 143,7 | 14,8 | 14,0 | 17,1 | 7,0 | 82,4 | 11,9 | 0,1 | 0,0 | 11,8 | 4,8 |
| sequía dura | 26-30 | normal ×0,70 | 73,1 | 9,9 | 19,0 | 15,5 | 5,4 | 77,1 | 12,8 | 0,0 | 0,0 | 6,9 | 2,9 |
| sequía dura | 31-35 | **escasez ×0,49** | 76,5 | 11,8 | 11,5 | 17,5 | 3,2 | 55,0 | 14,8 | 1,4 | 0,0 | 7,5 | 1,5 |
| sequía dura | 36-40 | normal ×0,70 | 72,9 | 18,7 | 3,5 | 10,0 | 5,3 | 64,9 | 15,6 | 0,1 | 0,0 | 3,0 | 2,4 |
| bestias que crían | 1-5 | — | 166,3 | 34,0 | 10,5 | 3,0 | 8,1 | 110,1 | 22,8 | 0,0 | 48,0 | 41,2 | 32,4 |
| bestias que crían | 6-10 | — | 104,7 | 33,4 | 12,5 | 11,1 | 8,4 | 115,2 | 33,4 | 0,4 | 0,0 | 53,2 | 10,9 |
| bestias que crían | 11-15 | — | 157,7 | 33,2 | 13,0 | 13,9 | 7,9 | 107,7 | 33,3 | 0,9 | 0,0 | 60,9 | 8,8 |
| bestias que crían | 16-20 | — | 104,5 | 34,7 | 20,5 | 12,4 | 7,7 | 112,0 | 34,1 | 0,8 | 0,0 | 66,1 | 7,8 |
| bestias que crían | 21-25 | — | 156,3 | 37,8 | 14,0 | 17,1 | 8,1 | 94,1 | 39,3 | 0,7 | 0,0 | 55,7 | 7,2 |
| bestias que crían | 26-30 | — | 105,5 | 38,6 | 19,0 | 14,7 | 7,8 | 94,0 | 38,1 | 0,7 | 0,0 | 44,0 | 7,0 |
| bestias que crían | 31-35 | — | 157,3 | 36,7 | 11,5 | 17,6 | 7,5 | 90,2 | 36,5 | 0,5 | 0,0 | 44,6 | 6,0 |
| bestias que crían | 36-40 | — | 104,8 | 34,8 | 3,5 | 10,5 | 7,5 | 88,8 | 34,5 | 0,4 | 0,0 | 32,5 | 5,2 |

#### Lo que se come, se pudre, se lleva la bestia y lo que hay en el almacén

| mundo | días | se come | (del huerto | de matorrales | del árbol | sin origen) | podrido en la planta | podrido en la bolsa | podrido en la despensa | la bestia come del huerto | la bestia roba | almacén al empezar | almacén al acabar | deja en el almacén | deja en la despensa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| abundancia | 1-5 | 118,3 | 68,0 | 13,3 | 0,0 | 37,0 | 15,9 | 61,4 | no guardado | 10,7 | 0,1 | 48,0 | 0,0 | 0,0 | 62,5 |
| abundancia | 6-10 | 122,3 | 102,5 | 19,8 | 0,0 | 0,0 | 4,5 | 44,0 | no guardado | 9,1 | 0,7 | 0,0 | 0,0 | 0,0 | 66,5 |
| abundancia | 11-15 | 117,2 | 97,4 | 19,7 | 0,1 | 0,0 | 7,1 | 66,5 | no guardado | 9,6 | 0,6 | 0,0 | 0,0 | 0,0 | 50,5 |
| abundancia | 16-20 | 121,0 | 101,5 | 19,5 | 0,0 | 0,0 | 2,8 | 46,0 | no guardado | 9,3 | 0,6 | 0,0 | 0,0 | 0,0 | 47,8 |
| abundancia | 21-25 | 117,5 | 98,3 | 19,1 | 0,1 | 0,0 | 5,4 | 68,1 | no guardado | 9,5 | 0,5 | 0,0 | 0,0 | 0,0 | 46,9 |
| abundancia | 26-30 | 120,7 | 102,0 | 18,7 | 0,0 | 0,0 | 4,2 | 45,1 | no guardado | 9,6 | 0,4 | 0,0 | 0,0 | 0,0 | 44,3 |
| abundancia | 31-35 | 117,4 | 98,5 | 18,9 | 0,0 | 0,0 | 5,8 | 67,3 | no guardado | 9,2 | 0,7 | 0,0 | 0,0 | 0,0 | 51,8 |
| abundancia | 36-40 | 114,5 | 97,0 | 17,4 | 0,0 | 0,0 | 3,4 | 45,9 | no guardado | 10,0 | 0,5 | 0,0 | 0,0 | 0,0 | 51,1 |
| normal | 1-5 | 118,6 | 64,5 | 16,8 | 0,0 | 37,2 | 5,2 | 47,8 | no guardado | 8,7 | 0,6 | 48,0 | 0,0 | 0,0 | 47,8 |
| normal | 6-10 | 124,0 | 97,1 | 26,8 | 0,0 | 0,0 | 0,4 | 25,4 | no guardado | 6,4 | 0,5 | 0,0 | 0,0 | 0,0 | 48,0 |
| normal | 11-15 | 119,3 | 92,6 | 26,5 | 0,2 | 0,0 | 0,5 | 37,5 | no guardado | 7,7 | 0,5 | 0,0 | 0,0 | 0,0 | 39,0 |
| normal | 16-20 | 123,4 | 95,8 | 27,4 | 0,2 | 0,0 | 0,5 | 25,9 | no guardado | 6,3 | 0,3 | 0,0 | 0,0 | 0,0 | 35,1 |
| normal | 21-25 | 119,6 | 92,7 | 26,9 | 0,0 | 0,0 | 0,6 | 36,7 | no guardado | 7,9 | 0,9 | 0,0 | 0,0 | 0,0 | 41,7 |
| normal | 26-30 | 123,0 | 96,2 | 26,7 | 0,1 | 0,0 | 0,6 | 25,4 | no guardado | 6,2 | 0,8 | 0,0 | 0,0 | 0,0 | 40,4 |
| normal | 31-35 | 118,4 | 92,0 | 26,0 | 0,4 | 0,0 | 0,7 | 38,5 | no guardado | 8,4 | 0,7 | 0,0 | 0,0 | 0,0 | 50,5 |
| normal | 36-40 | 117,5 | 92,4 | 24,9 | 0,2 | 0,0 | 0,3 | 26,8 | no guardado | 6,6 | 0,9 | 0,0 | 0,0 | 0,0 | 49,4 |
| sequía | 1-5 | 118,3 | 68,0 | 13,3 | 0,0 | 37,0 | 15,9 | 61,4 | no guardado | 10,7 | 0,1 | 48,0 | 0,0 | 0,0 | 62,5 |
| sequía | 6-10 | 121,9 | 98,3 | 23,4 | 0,1 | 0,0 | 2,2 | 36,1 | no guardado | 8,4 | 0,9 | 0,0 | 0,0 | 0,0 | 70,8 |
| sequía | 11-15 | 118,3 | 87,2 | 31,0 | 0,1 | 0,0 | 0,3 | 19,0 | no guardado | 7,0 | 0,7 | 0,0 | 0,0 | 0,0 | 34,4 |
| sequía | 16-20 | 126,9 | 91,5 | 35,1 | 0,3 | 0,0 | 0,2 | 11,7 | no guardado | 5,1 | 1,3 | 0,0 | 0,0 | 0,0 | 38,7 |
| sequía | 21-25 | 117,3 | 95,7 | 21,6 | 0,1 | 0,0 | 5,5 | 50,9 | no guardado | 9,4 | 0,7 | 0,0 | 0,0 | 0,0 | 69,3 |
| sequía | 26-30 | 120,8 | 99,0 | 21,8 | 0,1 | 0,0 | 3,5 | 34,5 | no guardado | 8,8 | 0,2 | 0,0 | 0,0 | 0,0 | 71,7 |
| sequía | 31-35 | 116,2 | 86,2 | 29,9 | 0,1 | 0,0 | 0,1 | 18,8 | no guardado | 6,1 | 0,4 | 0,0 | 0,0 | 0,0 | 43,9 |
| sequía | 36-40 | 118,0 | 86,5 | 31,2 | 0,3 | 0,0 | 0,1 | 12,2 | no guardado | 6,0 | 0,9 | 0,0 | 0,0 | 0,0 | 47,6 |
| sequía dura | 1-5 | 118,5 | 64,6 | 15,7 | 0,0 | 38,2 | 3,9 | 39,6 | no guardado | 7,8 | 0,6 | 48,0 | 0,0 | 0,0 | 54,1 |
| sequía dura | 6-10 | 120,0 | 91,4 | 28,4 | 0,2 | 0,0 | 0,1 | 12,7 | no guardado | 4,6 | 0,5 | 0,0 | 0,0 | 0,0 | 35,0 |
| sequía dura | 11-15 | 92,7 | 62,9 | 27,9 | 1,9 | 0,0 | 0,0 | 1,7 | no guardado | 5,7 | 0,4 | 0,0 | 0,0 | 0,0 | 4,5 |
| sequía dura | 16-20 | 72,8 | 55,7 | 16,2 | 0,9 | 0,0 | 3,7 | 5,9 | no guardado | 8,2 | 0,6 | 0,0 | 0,0 | 0,0 | 7,7 |
| sequía dura | 21-25 | 66,5 | 58,6 | 7,8 | 0,1 | 0,0 | 22,1 | 27,9 | no guardado | 10,7 | 1,1 | 0,0 | 0,0 | 0,0 | 12,3 |
| sequía dura | 26-30 | 66,5 | 58,4 | 8,1 | 0,0 | 0,0 | 14,3 | 21,4 | no guardado | 9,2 | 0,8 | 0,0 | 0,0 | 0,0 | 7,3 |
| sequía dura | 31-35 | 65,5 | 51,7 | 12,8 | 1,0 | 0,0 | 6,2 | 11,5 | no guardado | 9,2 | 0,7 | 0,0 | 0,0 | 0,0 | 7,7 |
| sequía dura | 36-40 | 65,1 | 52,9 | 12,1 | 0,1 | 0,0 | 5,1 | 8,8 | no guardado | 9,1 | 0,8 | 0,0 | 0,0 | 0,0 | 3,1 |
| bestias que crían | 1-5 | 119,0 | 65,0 | 18,6 | 0,0 | 35,5 | 3,6 | 38,0 | no guardado | 21,9 | 14,4 | 48,0 | 0,0 | 0,0 | 44,7 |
| bestias que crían | 6-10 | 124,2 | 93,2 | 30,9 | 0,2 | 0,0 | 0,1 | 18,6 | no guardado | 18,7 | 12,6 | 0,0 | 0,0 | 0,0 | 54,4 |
| bestias que crían | 11-15 | 119,5 | 88,5 | 30,5 | 0,5 | 0,0 | 0,3 | 22,8 | no guardado | 21,6 | 9,3 | 0,0 | 0,0 | 0,0 | 62,1 |
| bestias que crían | 16-20 | 121,9 | 89,7 | 31,6 | 0,7 | 0,0 | 0,2 | 18,5 | no guardado | 20,1 | 10,0 | 0,0 | 0,0 | 0,0 | 67,0 |
| bestias que crían | 21-25 | 118,0 | 81,4 | 36,1 | 0,5 | 0,0 | 0,1 | 18,2 | no guardado | 36,2 | 16,1 | 0,0 | 0,0 | 0,0 | 55,7 |
| bestias que crían | 26-30 | 115,0 | 79,8 | 34,7 | 0,5 | 0,0 | 0,2 | 11,7 | no guardado | 37,8 | 15,8 | 0,0 | 0,0 | 0,0 | 44,5 |
| bestias que crían | 31-35 | 108,7 | 74,2 | 34,2 | 0,2 | 0,0 | 0,2 | 15,9 | no guardado | 40,0 | 11,6 | 0,0 | 0,0 | 0,0 | 45,3 |
| bestias que crían | 36-40 | 101,3 | 72,6 | 28,6 | 0,1 | 0,0 | 0,3 | 12,8 | no guardado | 41,9 | 14,9 | 0,0 | 0,0 | 0,0 | 33,0 |

### 3c. Lo que conoce (reconstruido)

Media por criatura viva al acabar el día. Matorrales sin las plantas del huerto ni el árbol. «Visto» = parte de las casillas del valle vistas alguna vez.

| día | abundancia: bosque · salvaje · visto | normal: bosque · salvaje · visto | sequía: bosque · salvaje · visto | sequía dura: bosque · salvaje · visto | bestias que crían: bosque · salvaje · visto |
|---|---|---|---|---|---|
| 1 | 6,2 · 0,2 · 23 % | 6,3 · 0,3 · 24 % | 6,2 · 0,2 · 23 % | 6,3 · 0,2 · 24 % | 6,0 · 0,2 · 23 % |
| 2 | 8,3 · 0,3 · 29 % | 8,6 · 0,4 · 30 % | 8,3 · 0,3 · 29 % | 8,7 · 0,3 · 30 % | 8,3 · 0,3 · 29 % |
| 3 | 9,6 · 0,4 · 33 % | 9,9 · 0,4 · 34 % | 9,6 · 0,4 · 33 % | 10,0 · 0,3 · 33 % | 9,8 · 0,4 · 34 % |
| 4 | 10,1 · 0,4 · 34 % | 10,9 · 0,5 · 37 % | 10,1 · 0,4 · 34 % | 11,0 · 0,4 · 36 % | 10,8 · 0,5 · 37 % |
| 5 | 10,8 · 0,4 · 37 % | 11,8 · 0,7 · 40 % | 10,8 · 0,4 · 37 % | 12,0 · 0,5 · 40 % | 11,8 · 0,6 · 41 % |
| 6 | 11,1 · 0,5 · 37 % | 12,2 · 0,7 · 42 % | 11,1 · 0,5 · 37 % | 12,6 · 0,6 · 42 % | 12,5 · 0,7 · 43 % |
| 7 | 11,6 · 0,5 · 39 % | 12,8 · 0,8 · 44 % | 11,6 · 0,5 · 39 % | 13,4 · 0,7 · 45 % | 13,3 · 0,8 · 46 % |
| 8 | 11,9 · 0,5 · 40 % | 13,3 · 0,8 · 45 % | 12,1 · 0,6 · 41 % | 13,9 · 0,8 · 47 % | 13,7 · 0,9 · 48 % |
| 9 | 12,2 · 0,5 · 41 % | 13,7 · 0,9 · 47 % | 12,6 · 0,7 · 43 % | 15,0 · 1,0 · 52 % | 14,1 · 1,0 · 50 % |
| 10 | 12,4 · 0,6 · 42 % | 14,0 · 0,9 · 48 % | 12,9 · 0,7 · 44 % | 15,6 · 1,2 · 54 % | 14,4 · 1,1 · 51 % |
| 11 | 12,7 · 0,6 · 43 % | 14,3 · 1,0 · 50 % | 13,4 · 0,9 · 46 % | 16,5 · 1,4 · 59 % | 14,9 · 1,2 · 53 % |
| 12 | 12,8 · 0,6 · 43 % | 14,6 · 1,1 · 51 % | 14,0 · 1,0 · 49 % | 17,4 · 1,6 · 63 % | 15,1 · 1,3 · 54 % |
| 13 | 13,0 · 0,6 · 44 % | 14,9 · 1,1 · 52 % | 15,2 · 1,2 · 54 % | 18,5 · 2,0 · 69 % | 15,6 · 1,4 · 56 % |
| 14 | 13,1 · 0,7 · 44 % | 15,0 · 1,2 · 53 % | 15,8 · 1,3 · 56 % | 18,9 · 2,2 · 71 % | 15,8 · 1,4 · 57 % |
| 15 | 13,3 · 0,7 · 45 % | 15,2 · 1,2 · 54 % | 16,6 · 1,6 · 60 % | 19,3 · 2,5 · 74 % | 16,2 · 1,5 · 59 % |
| 16 | 13,4 · 0,7 · 45 % | 15,5 · 1,3 · 54 % | 17,0 · 1,7 · 62 % | 19,6 · 2,5 · 75 % | 16,4 · 1,5 · 60 % |
| 17 | 13,5 · 0,7 · 46 % | 15,7 · 1,3 · 56 % | 17,6 · 1,8 · 65 % | 19,9 · 2,6 · 77 % | 16,7 · 1,6 · 61 % |
| 18 | 13,5 · 0,7 · 46 % | 15,9 · 1,4 · 56 % | 17,8 · 1,9 · 66 % | 20,0 · 2,6 · 78 % | 16,9 · 1,7 · 62 % |
| 19 | 13,6 · 0,7 · 46 % | 16,2 · 1,4 · 58 % | 18,0 · 2,0 · 67 % | 20,1 · 2,6 · 78 % | 17,1 · 1,7 · 63 % |
| 20 | 13,7 · 0,8 · 47 % | 16,3 · 1,5 · 58 % | 18,0 · 2,0 · 68 % | 20,1 · 2,7 · 78 % | 17,3 · 1,8 · 64 % |
| 21 | 13,8 · 0,8 · 47 % | 16,6 · 1,5 · 59 % | 18,1 · 2,0 · 68 % | 20,1 · 2,7 · 79 % | 17,5 · 1,8 · 65 % |
| 22 | 13,9 · 0,8 · 47 % | 16,6 · 1,6 · 60 % | 18,1 · 2,0 · 68 % | 20,1 · 2,7 · 79 % | 17,7 · 1,9 · 66 % |
| 23 | 14,0 · 0,8 · 48 % | 16,8 · 1,6 · 61 % | 18,1 · 2,1 · 68 % | 20,1 · 2,7 · 79 % | 18,1 · 2,0 · 68 % |
| 24 | 14,1 · 0,8 · 48 % | 16,9 · 1,6 · 61 % | 18,1 · 2,1 · 68 % | 20,1 · 2,7 · 79 % | 18,3 · 2,1 · 69 % |
| 25 | 14,2 · 0,9 · 49 % | 17,0 · 1,7 · 62 % | 18,2 · 2,1 · 69 % | 20,2 · 2,7 · 79 % | 18,5 · 2,2 · 71 % |
| 26 | 14,3 · 0,9 · 49 % | 17,1 · 1,7 · 62 % | 18,2 · 2,1 · 69 % | 20,2 · 2,7 · 79 % | 18,7 · 2,3 · 71 % |
| 27 | 14,4 · 0,9 · 49 % | 17,2 · 1,7 · 63 % | 18,2 · 2,1 · 69 % | 20,2 · 2,7 · 79 % | 18,9 · 2,4 · 73 % |
| 28 | 14,6 · 0,9 · 50 % | 17,3 · 1,8 · 63 % | 18,3 · 2,1 · 69 % | 20,2 · 2,7 · 80 % | 19,0 · 2,4 · 73 % |
| 29 | 14,7 · 0,9 · 50 % | 17,4 · 1,8 · 64 % | 18,3 · 2,1 · 69 % | 20,2 · 2,7 · 80 % | 19,2 · 2,5 · 75 % |
| 30 | 14,8 · 0,9 · 51 % | 17,5 · 1,9 · 64 % | 18,4 · 2,1 · 70 % | 20,2 · 2,7 · 80 % | 19,3 · 2,6 · 75 % |
| 31 | 14,9 · 1,0 · 51 % | 17,6 · 1,9 · 65 % | 18,4 · 2,2 · 70 % | 20,2 · 2,7 · 80 % | 19,5 · 2,6 · 76 % |
| 32 | 15,0 · 1,0 · 52 % | 17,7 · 1,9 · 66 % | 18,5 · 2,2 · 71 % | 20,2 · 2,8 · 80 % | 19,6 · 2,6 · 77 % |
| 33 | 15,1 · 1,0 · 52 % | 17,8 · 2,0 · 66 % | 18,9 · 2,4 · 73 % | 20,3 · 2,8 · 81 % | 19,8 · 2,7 · 78 % |
| 34 | 15,1 · 1,0 · 52 % | 17,9 · 2,0 · 67 % | 19,1 · 2,4 · 74 % | 20,4 · 2,8 · 81 % | 19,9 · 2,7 · 79 % |
| 35 | 15,2 · 1,0 · 53 % | 18,1 · 2,0 · 67 % | 19,5 · 2,6 · 76 % | 20,4 · 2,9 · 82 % | 20,0 · 2,8 · 79 % |
| 36 | 15,2 · 1,1 · 53 % | 18,2 · 2,1 · 68 % | 19,7 · 2,6 · 78 % | 20,4 · 2,9 · 82 % | 20,0 · 2,8 · 80 % |
| 37 | 15,3 · 1,1 · 53 % | 18,2 · 2,1 · 68 % | 19,9 · 2,7 · 79 % | 20,5 · 3,0 · 83 % | 20,0 · 2,9 · 80 % |
| 38 | 15,3 · 1,1 · 53 % | 18,3 · 2,2 · 69 % | 19,9 · 2,7 · 79 % | 20,5 · 3,0 · 83 % | 20,0 · 2,9 · 80 % |
| 39 | 15,4 · 1,1 · 53 % | 18,4 · 2,2 · 69 % | 19,9 · 2,8 · 79 % | 20,6 · 3,0 · 83 % | 20,1 · 3,0 · 81 % |
| 40 | 15,5 · 1,1 · 54 % | 18,4 · 2,2 · 70 % | 19,9 · 2,8 · 80 % | 20,6 · 3,0 · 83 % | 20,2 · 3,0 · 81 % |

#### Qué día se apaga R-CURIOSIDAD-FRONTERA en cada criatura

Se apaga para siempre cuando lo que guarda en self.mat (matorrales, plantas y árbol vistos) llega a los matorrales que dice la cultura, o cuando ya lo ha visto todo. Día 1-40.

| mundo | criaturas | se apaga | día medio | mediana | el primero | el último |
|---|---|---|---|---|---|---|
| abundancia | 320 | 95,9 % | 6,0 | 3 | 1 | 37 |
| normal | 320 | 99,1 % | 4,7 | 3 | 1 | 35 |
| sequía | 320 | 99,7 % | 5,0 | 3 | 1 | 18 |
| sequía dura | 320 | 99,7 % | 4,3 | 4 | 1 | 14 |
| bestias que crían | 320 | 99,7 % | 4,4 | 3 | 1 | 24 |

Por día (todas las criaturas de los cinco mundos): día 1: 102, día 2: 377, día 3: 346, día 4: 152, día 5: 178, día 6: 53, día 7: 107, día 8: 55, día 9: 51, día 10: 28, día 11: 34, día 12: 20, día 13: 29, día 14: 8, día 15: 7, día 16: 1, día 17: 2, día 18: 2, día 19: 3, día 20: 3, día 21: 1, día 22: 1, día 23: 1, día 24: 3, día 25: 3, día 26: 2, día 28: 2, día 29: 1, día 31: 2, día 32: 1, día 33: 1, día 35: 2, día 36: 1, día 37: 2.

#### El árbol dulce

| mundo | apariciones por partida | vistas por alguna | criaturas que lo ven (media por aparición) | de las vivas | tarda en verlo (turnos; media · mediana) | frutos puestos | cogidos | parte cogida |
|---|---|---|---|---|---|---|---|---|
| abundancia | 5,22 | 3,3 % | 0,06 | 0,7 % | 670 · 594 | 4180 | 22 | 0,5 % |
| normal | 5,22 | 6,2 % | 0,09 | 1,1 % | 703 · 718 | 4180 | 59 | 1,4 % |
| sequía | 5,22 | 8,1 % | 0,12 | 1,6 % | 556 · 435 | 4180 | 69 | 1,7 % |
| sequía dura | 5,22 | 9,6 % | 0,14 | 2,5 % | 546 · 471 | 4180 | 213 | 5,1 % |
| bestias que crían | 5,22 | 16,3 % | 0,22 | 2,9 % | 606 · 582 | 4180 | 170 | 4,1 % |

### Lo que se ve en las tablas (sin causas)

- **3a.** Con la cota y el umbral 0,1, la mañana y la tarde son «en calma» del 85 al 99 % de las decisiones en cuatro mundos. En la sequía dura, del 50 al 52 %. Con 0,05 y 0,2 cambia poco, salvo en la sequía dura (41-44 % y 60-63 %) y en las bestias que crían (76-78 % y 91-93 %). En esos ratos, de día, sobre todo **se queda** (66-84 %), trabaja el 6-17 % y anda el 6-11 %. Los ratos son cortos (mediana de 2 a 4 turnos de día).
- **3b.**
  - El almacén empieza con 48 comidas, se vacía en los días 1-5 en los cinco mundos y no se vuelve a llenar: nadie deja comida en él (0 en todos los tramos).
  - En la sequía, en los tramos de escasez (días 11-15 y 31-35) baja lo que se coge de las plantas: unas 89, frente a 111-144 en los demás tramos.
  - En la sequía dura, lo que se come cae de unas 120 por tramo a 65-73 desde el día 16, y lo podrido en las plantas sube en los días 21-30.
  - En las bestias que crían, lo que la bestia come del huerto pasa de unas 19-22 por tramo en los días 1-20 a 36-42 en los días 21-40; lo que roba va de 9 a 16 por tramo, sin esa subida.
- **3c.**
  - **R-CURIOSIDAD-FRONTERA se apaga pronto: mediana día 3 o 4, en el 96 al 99,7 % de las criaturas.** Se apaga cuando `self.mat` llega a los 20,03 matorrales que dice la cultura (falta_saber, CV:2316-2320). `self.mat` cuenta también las 16 plantas del huerto y el árbol, así que le bastan las plantas y unos 5 matorrales. Esto se lee en el código; la fecha es reconstruida.
  - **Matorrales conocidos:** al acabar, del bosque conoce entre 15,5 (abundancia) y 20,6 (sequía dura) de los 21 que hay, y de los salvajes, entre 1,1 y 3,0 de los 5.
  - **Mapa visto:** entre el 54 y el 83 % al acabar.
- **El árbol:** aparece unas 5,2 veces por partida, pero solo lo ve alguna criatura en el 3-16 % de las apariciones. Las que lo ven tardan de media de 550 a 700 turnos, de los 1.200 que está. Se coge del 0,5 al 5 % de su fruta.

## Parte 4. La gemela que suma (S69+voz)

- **Es la misma clase que la protagonista:** `cuerpo_vr1.RG69V` (`paper8/cuerpo_vr1.py:11`). Se la pone el lanzador de la escalera: `LE6.CLASE[v] = ZV.RG69V` para S69voz (`paper8/lanza_escalera_v6.py:27`).
  - Lo comprobé importando el lanzador: `CLASE["S69voz"] is CLASE["RG69rvoz"]` da `True`.
- **Sus interruptores** son `dict(B7.VARS["S68"], reserva_v69=True, a_casa=True)` (`paper8/lanza_escalera_v6.py:24`). S68 es RG68r con el valorador de sumas (`paper8/banco_v7.py:311`; cabecera de `lanza_escalera_v6.py:2`).
  - Comparé los dos diccionarios importando los lanzadores. **La única diferencia con RG69r+voz es `sumas_v29=True`.**
- **Qué cambia ese interruptor:** solo cómo se compone el valor de cada foto, en `Criatura._compone` (CV:1286-1291).
  - Con él, `compone_sumas` (CV:135-…): las mismas filas y el mismo reparto, pero sin el motor; cada dimensión vale lo que gana menos lo que pierde, y la foto, la suma de las tres.
  - La segunda foto de la voz también pasa por `_compone` (cabecera de `lanza_escalera_v6.py:5-6`).
- **¿Se puede heredar en un fichero nuevo igual que la protagonista?** Sí, sin código nuevo de criatura. Basta con:
  - importar `cuerpo_vr1.RG69V`;
  - pasarle `dict(B7.VARS["RG69rvoz"], sumas_v29=True)`, o el mismo `B7.VARS["S69voz"]` que monta `lanza_escalera_v6.py:24` al importarlo.
  - Una clase hija (`class X(cuerpo_vr1.RG69V)`) heredaría todo igual que la protagonista.
  - No he construido nada.

## Lo que no he podido contar

1. **3a, la calma tal como se definió.** Faltan las filas de pérdida de cada decisión, salvo cinco.
   - El lanzador ya las tiene en memoria cada turno (`c._filas_v4`, `paper8/lanza_experimento_v5.py:35-37`), pero solo escribe esas cinco (:52-57).
   - Para tenerlas habría que rejugar con un registro que las escriba todas. Por eso doy una cota.
2. **3b, lo que dan los matorrales y lo que se pudre en ellos, por separado.** Dar fruto no deja evento; solo sale el neto (lo que dieron menos lo podrido en la mata).
   - Por la regla del mundo (no contado), 21 matorrales del bosque × 1 fruto cada 800 turnos y 5 salvajes × 2 darían unos 78 frutos por tramo, por el factor de la época, y una parte (0,1) cae como baya suelta.
3. **3b, la despensa:** lo que hay en ella y lo que se pudre allí no está en ningún registro.
4. **3b, lo que se come la bestia de lo robado:** solo está en el libro diario del mundo (`comido_bestia`), que no se guardó. Doy lo que roba y lo que come del huerto.
5. **3b, el libro diario entero** (`Valle.cuadre`, `stats.podrido_por_sitio`, `stats.almacen_fin_dia`) lo tendría todo, exacto, por tipo y por día. Habría que guardarlo en `fin.json` y rejugar.
6. **3c:** lo que conoce y lo que ve es reconstruido. Para tenerlo exacto habría que guardar `self.mat` y `self.vistas` cada día y rejugar.
7. **Parte 2, la confianza de las creencias** que no son de sitios: no está guardada (pregunta 1).
8. **Parte 1:** la curiosidad como forma del cinco (`curiosidad_forma.py`) no la he leído entera; solo su cabecera y sus mandos.

## Cierre

- **Partidas jugadas:** ninguna. **Ficheros existentes editados:** ninguno. **Cambios en `cantera/paper8`:** ninguno. **Clave:** no se ha usado. `motor/model.py` sin cambios.
- **Gasto:**
  - créditos de la plataforma: 0;
  - dólares de la consola de Anthropic: 0.
  - No he leído los saldos.
- **Commit local sin push.**
