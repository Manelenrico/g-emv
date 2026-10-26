# Informe P7 · Revisión externa (paper siete, v11): comprobaciones en los registros

Fecha: 26-oct-2026. Solo lectura: no se ha jugado ninguna partida, no se ha tocado el motor y no se ha modificado ningún archivo existente; lo único escrito en el proyecto es este informe y la carpeta `revision_externa/`. Los recálculos están en `cantera/paper7/revision_externa/`. Cada guion `rX_*.py` deja su salida al lado, en `rX_*.out`. Leen los diarios crudos (los `.zip` de `paintball/runs/`) y los JSON sellados, y escriben solo en esa carpeta. Todos se han vuelto a ejecutar desde ella y reproducen las cifras de este informe y, donde existe, la cifra sellada. Las rutas salen de `comun.py`, relativas a la carpeta.
Gasto: 0 créditos de la plataforma y 0 $ de la consola de Anthropic.

Convención: **verificado** es lo leído en el código o en los datos, o recontado; **inferido** es una interpretación que no se ha comprobado.

---

## 1. Errores típicos

### (a) P7-56, R2: confianza tras una propuesta verdadera frente a una falsa

Guion: `revision_externa/r1a_P7_56_unidades.py` (ejecuta la lógica sellada de `erratas_P7_56.py` sin su escritura) da todas las cifras de este apartado.

- **Qué cifra es:** 0,720 (n = 982) frente a 0,257 (n = 226), con diferencia 0,464 ± 0,019 y 24,1 ee. Es la cuenta **corregida** de la fe de erratas, la que usa `verdad_sello` (`informe_P7_56_erratas.md:33`). La original era 0,657 (1154) frente a 0,132 (54), con 0,525 ± 0,032 y 16,4 ee (`informe_P7_56.md:60`; `informe_P7_56_erratas.md:32`). El paper usa la corregida (`escritura/cantera_cap5.md:190`).
- **Unidad usada:** la evaluación. Hay una observación por evaluación (`informe_P7_56_erratas.md:22`; `analiza_P7_56.py:4`).
- **Cálculo del ee:** ee = sd/√n en cada grupo (`erratas_P7_56.py:20`), combinados con √(ee_V² + ee_F²) (`erratas_P7_56.py:108`).
- **Problema (verificado):** las 1.208 evaluaciones salen de solo **6 criaturas**: 3 series × asientos 10 y 11, brazo CON_RAZON, a lo largo de 20 días. La confianza es un estado que se arrastra de una evaluación a la siguiente, así que las evaluaciones no son independientes.

| unidad | diferencia | ee | razón | n |
|---|---|---|---|---|
| evaluación (publicado) | 0,464 | 0,019 | 24,1 | 1208 evaluaciones |
| ee agrupado (CR1) por criatura | 0,464 | 0,049 | **9,4** | 6 criaturas |
| ee agrupado (CR1) por serie | 0,464 | 0,063 | 7,3 | 3 series |
| media por criatura, ee entre criaturas | **0,417** | 0,074 | **5,6** | 6 |
| media por serie, ee entre series | 0,422 | 0,089 | 4,7 | 3 |

- Sin las partidas marcadas, la corregida da 0,409 ± 0,062 (6,6 ee) agrupando por criatura y 0,349 ± 0,077 (4,5 ee) con la media por criatura.
- **R2 sigue pasando el listón de 3 ee con cualquier unidad.** El margen baja de 24 a entre 4,7 y 9,4 ee.
- La cuenta original, por criatura, habría dado 0,295 ± 0,146 (2,0 ee). Ya no es la vigente.

### (b) P7-65, L1: caída de la confianza tras la falsa (−0,120 ± 0,009, 13,0 ee)

Guion: `revision_externa/r1bde_unidades.py`, bloque (b).

- **Unidad usada:** la criatura. Es la media de las 9 medias por criatura, con ee = sd/√9 (`analiza_P7_65.py:88-91,100-104`; `informe_P7_65.md:36-38`). Detrás hay 601 evaluaciones.
- **Comprobación del propio informe:** con ee agrupado por criatura da −0,119 ± 0,011, 11,2 ee (`analiza_P7_65.py:107-109`; `informe_P7_65.md:40`).
- **Problema (verificado):** en MIENTEN_DOS las dos hermanas juegan la misma partida, así que las 9 criaturas salen de **6 cadenas de partidas** (3 series × 2 brazos).
  - Por cadena, con la media de las hermanas: −0,119 ± 0,0098, **12,1 ee** (n = 6).
  - Por serie: −0,120 ± 0,0154, **7,8 ee** (n = 3).
- **Sigue pasando.** El informe ya avisa de que buena parte de la caída la produce la propia regla de actualización (`informe_P7_65.md:42`).

### (c) P7-67: llegadas, mentirosa frente a congelada («unas 9 veces») y caída de la mentirosa («unas 16 veces»)

Guiones:
- `r1c_relee_P7_67.py` relee los 1.280 criatura-días crudos y los deja en `crudo_n1_MC.json`; usa `lee_dia` de `analiza_P7_67.py`.
- `r1c_pareja_P7_67.py` da las cuentas por pareja, por criatura agrupada y emparejadas, la comprobación de 0 discrepancias y los conteos por bloque.
- `r1c_dia_P7_67.py` da las llegadas por día y las cuentas «por día».
- `r1c_dosvias_P7_67.py` da los conglomerados por día y a dos vías.

- **De dónde salen las cifras:**
  - «16 veces» es P1: −0,2203 / 0,0135 = 16,3 (`informe_P7_67_campo.md:34`).
  - «9 veces» es P2: −0,3378 / 0,0362 = 9,3 (`informe_P7_67_campo.md:37`).
  - El redondeo está en `WHERE_IS_SEVEN.md:76-77`.
- **Unidad usada:** la pareja, es decir la cadena (nivel, brazo, serie), tal como fija el sello (`SELLO_P7_67.md:60-62`).
  - Cada pareja da un único número: B − A, la fracción de llegadas de los días 11-20 menos la de los días 1-10 (`analiza_P7_67.py:83-94`).
  - P1: ee = sd/√16 (`:100-102,161-162`).
  - P2: ee de dos medias independientes, con 16 + 16 parejas (`:164`).
- **Lo que no es problema (verificado):**
  - Ni la criatura, ni la pareja, ni los días seguidos se cuentan dos veces.
  - Agrupar la robustez «criatura como unidad» (n = 32) por serie da ee 0,0136.
  - Emparejar P2 por serie, que comparte semilla y mapa entre brazos, da ee 0,0360. La correlación entre brazos es 0,011.
- **Lo que sí es problema (verificado):** el **destino de cada día es común a las 16 series**. Se elige con `random.Random(1000·día + 10)` (`SELLO_P7_67.md:48`; en `P7_67F_diseno.json` los `destinos` van solo por día).
  - Las llegadas de la mentirosa dependen mucho del día. Por ejemplo, de 32 oportunidades llegan 23 el día 2, 4 el día 3 y 0 los días 8 y 10.
  - Las 16 series replican la variación entre mapas, pero no la variación entre destinos: en B − A solo se comparan 10 destinos con otros 10.

Recálculo con el día como unidad o conglomerado, desde los diarios crudos (1.280 criatura-días; 0 discrepancias con `P7_67_analisis.json`):

| cuenta | diferencia | ee | razón | unidades |
|---|---|---|---|---|
| P1 publicado (pareja) | −0,2203 | 0,0135 | 16,3 | 16 parejas |
| P1, media por día, B − A | −0,2250 | 0,0912 | **2,5** | 10 + 10 días |
| P1, ee por conglomerado de día | −0,2204 | 0,0900 | 2,4 | 20 días |
| P1, conglomerado a dos vías (serie × día) | −0,2204 | 0,0831 | 2,7 | 16 × 20 |
| P2 publicado (pareja) | −0,3378 | 0,0362 | 9,3 | 16 + 16 parejas |
| P2, por día | −0,3505 | 0,1200 | **2,9** | 10 + 10 días |
| P2, ee por conglomerado de día | −0,3382 | 0,1173 | 2,9 | 20 días |
| P2, conglomerado a dos vías | −0,3382 | 0,1141 | 3,0 | 16 × 20 |

- **Lectura:** el signo se mantiene en todas las cuentas. El ee sellado vale **para estos 20 destinos**. Si se quiere generalizar a destinos nuevos, las razones bajan a entre 2,5 y 3, en el listón sellado de 3 o justo por debajo.
- **Inferido:** la cuenta por día es conservadora, porque mete en el «ruido» el aprendizaje dentro de cada bloque, y con 20 conglomerados el ee es poco preciso.
- **Decisión pendiente para Manel:** qué unidad usar al generalizar es una decisión de análisis que no está en el sello. Se **propone**, no se aplica.
- **Conteos crudos por bloque** (coinciden con `informe_P7_67_campo.md:97-108`):
  - MIENTE: 73 / 16 / 15 / 2 llegadas, sobre 160 / 159 / 160 / 130 oportunidades.
  - CONGELADA: 112 / 143 / 153 / 113.

### (d) Confianza final: 0,838 (HONESTA) frente a 0,157 (MIENTE)

Guion: `revision_externa/r1bde_unidades.py`, bloque (d).

- **Dónde sale:** P7-67 campo, nivel 1, día 20 (`informe_P7_67_campo.md:88`; tabla en `:65-88`, calculada en `analiza_P7_67.py:170-174`). El paper la cita en `cantera_cap5.md:953,1069`.
- **Cálculo publicado:** es una media descriptiva de 32 criaturas por brazo (16 series × 2 hermanas), **sin ee ni contraste**.
- **Problema (verificado):** las 32 criaturas no son independientes. En MIENTE, 10 de las 16 parejas de hermanas tienen exactamente la misma confianza el día 20; en CONGELADA, las 16.
- **Recálculo con la serie como unidad:**
  - HONESTA: 0,838 ± 0,033 (16 series).
  - MIENTE: 0,157 ± 0,0055 (16 series).
  - Diferencia: **0,681 ± 0,033, 20,3 ee**. Emparejando por serie: 0,681 ± 0,035, 19,6 ee.
  - La figura 5.3 ya usa la serie como unidad (`figuras/hace_figuras_P7.py:47-54`).
- **Matiz:** aquí también afecta el destino común por día del punto (c). No se ha recalculado agrupando por día.

### (e) 4,73 ± 1,27: escala propia menos fórmula antigua

Guion: `revision_externa/r1bde_unidades.py`, bloque (e).

- **Dónde sale:** solo en `figuras/informe_P7_figuras.md:176`, calculado en `figuras/hace_figuras_P7.py:149-154`. No aparece en los informes numerados.
- **Unidad usada:** la criatura, con la media de sus diferencias en las pruebas 11-17; ee = sd/√7, n = 7. El propio texto la marca como descriptiva.
- **Problema (verificado):** las 7 criaturas caen en 5 series (APRENDE_p s1, s2, s3 y APRENDE_v s1, s2). En p·s3 y en v·s2 hay dos hermanas.
- **Recálculo con la serie como unidad:** **5,32 ± 1,57, 3,4 ee** (n = 5), frente a 3,7 ee por criatura.
- **Inferido:** que a10 y a11 de la misma serie juegan la misma partida se deduce de cómo se nombran los cuadernos; no se ha comprobado en el lanzador.

---

## 2. La regla de acierto (`invita_P7_54.py:141-144`)

```python
if abs(p) < 1e-9 and abs(v) < 1.0: ac[dim] = 1
elif abs(p) < 1e-9: ac[dim] = 0
else: ac[dim] = 1 if (p > 0) == (v > 0) and abs(v) >= abs(p) / 2 else 0
```

La regla se aplica a cada dimensión (cuerpo, recursos, vínculo), y la confianza se actualiza con ETA = 0,3 (`:145`). El rango 134-140 es la búsqueda de lo vivido: la huella del uso, o si no la hay, el cambio en 240 o 480 tics.

- **Promesa −10, vivido −10:** **acierto**. Los dos son «no positivos» y |−10| ≥ 5.
  - Con la misma promesa, vivido −4 es fallo por magnitud, vivido 0 es fallo y cualquier vivido positivo es fallo.
  - El signo funciona bien. La única asimetría es que un vivido de 0 «coincide en signo» con una promesa negativa, pero lo descarta la condición de magnitud.
- **Promesa 0:** acierto solo si |vivido| < 1. Cualquier cambio de 1 o más, sea ganancia o pérdida, es fallo.
- **Herencia en scripts posteriores:**
  - `juicio_P7_62.py:35-38` copia la regla idéntica.
  - Los contrastes de lo contado (`invita_P7_57.py:35-37`, `juicio_P7_62.py:122-124`, `juicio_P7_63.py:53-55`) **se saltan** la promesa 0.
  - P7-66, P7-66b, P7-67 y P7-67b juzgan la llegada como binaria («ve un botiquín cerca del destino») y no miran el valor de la promesa. Por eso el caso de promesa ≤ 0 no se da en el campo de P7-67.

**Juicios con promesa ≤ 0 en los diarios crudos (verificado; guion `revision_externa/r2_promesas.py`, que comprueba también cada acierto contra la regla).** En cada celda, el total de juicios y entre paréntesis los que acertaron.

| campo · registro | cuerpo < 0 | cuerpo = 0 | recursos < 0 | vínculo < 0 |
|---|---|---|---|---|
| P7-56 · `P7_54_evaluada` (1208) | 86 (1) | 806 (738) | 10 (10) | 9 (0) |
| P7-61 · `P7_54_evaluada` (2625) | 90 (18) | 1917 (1720) | 93 (83) | 0 |
| P7-65 · `P7_54_evaluada` (2751) | 69 (9) | 1710 (1565) | 10 (5) | 0 |
| P7-65 · `P7_62_evaluada` (106) | 0 | 27 (20) | 69 (39) | 0 |
| P7-67 campo | sin juicios de este tipo | — | — | — |

- **¿Hubo algún juicio afectado?** **Ninguno está mal juzgado por la regla (verificado):** en todos, el acierto registrado coincide con lo que da la regla. De los 806 de promesa 0 en el cuerpo de P7-56, 68 son fallos, y 24 de ellos lo son por una **ganancia** de vida de 1 o más.
- **Rareza (verificado):** hay un registro de P7-65 con promesa 0 en recursos, vivido registrado 1,0 y acierto 1. **Inferido:** el valor real era menor que 1 y el registro lo redondea a 3 decimales (`:147`).
- **Inferido, no comprobado:** lo que sí pesa es la ventana de 240 tics. Una promesa negativa verdadera cuenta como fallo si la pérdida no llega dentro de la ventana: en P7-56 solo acierta 1 de las 86 promesas negativas en cuerpo. No se han cruzado esos 86 casos con `verdad_sello`.

---

## 3. Curarse o conocer (`informe_P7_30.md:168`)

Guion: `revision_externa/r3_aperturas_P7_30.py` da los grupos 57 / 95 / 4, sus medianas de vida y de `s_max`.

- **Condición:** la marca se calcula en `analiza_P7_30.py:54`:
  `le_pesa_el_cuanto = s_max is not None and (100 − hp) > s_max`, con `conocido = s_max is not None`.
  - `hp` es la vida al abrir el botiquín.
  - `s_max` es el mayor efecto en el cuerpo entre los recuerdos no cortados del botiquín: los del cuaderno de arranque (`:49-50`) más los usos completados ese día antes de esta apertura (`:53`).
  - Es la misma magnitud que `sabido_max` de la criatura (`nace_P7_29.py:102-105`).
- **Los grupos:**
  - **57 aperturas, mediana de vida 40:** **sí le pesaba** la curiosidad del cuánto. Lo que le falta (100 − vida) es mayor que lo más alto que sabe que da el botiquín.
  - **95 aperturas, mediana 84:** el botiquín es **conocido pero no le pesa**, porque 100 − vida ≤ `s_max`.
  - Hay un tercer grupo de 4 aperturas, **sin conocerlo aún** (`s_max` = None), con mediana 91.
- **Recuento (verificado):** desde `P7_30_vidas.json` se obtiene 57 + 95 + 4 = 156 y las mismas medianas.
- **Advertencias:**
  - **Verificado:** los 156 son todas las aperturas de **APRENDE en los 20 días**, no solo las de los días 11-20 que cita la frase anterior del informe, que son 94 (`sello_P7_30.py:116-117`).
  - **Inferido:** el corte depende de la propia vida al abrir. Con `s_max` = 50, «le pesa» equivale a vida < 50, así que la diferencia de medianas sale en buena parte por construcción y no prueba por sí sola un efecto de la curiosidad sobre la conducta. La mediana de `s_max` es 33 en el grupo de 57 y 50 en el de 95.
  - El 100 está escrito a mano en el análisis; en la criatura es `mem.hp_max`, que vale 100 (`nace_P7_23.py:91`).

---

## 4. La ración

Guion: `revision_externa/r4_racion_P7_30.py` da los usos, los «al menos», los firmes, la vida y el efecto en P7-30.

- **Cómo actúa en Zero Sum (v0.1.19, verificado en el catálogo):**
  - `rations`: cura **15** de vida en **24 tics** (1 s), apilable hasta 5 (`P7_0_medidas.json`, bloque `catalogo`; manifiesto en `coworld/cow_…/coworld_manifest.json`: «rations (15 HP)», «bushes yield rations»).
  - El botiquín, para comparar, cura 50 en 48 tics y se cancela con cualquier daño. La ración **no** se interrumpe con el daño (`informe_P7_62.md:17-18,40`; se comprueba en `prueba_P7_63.py:19`).
  - Medido en P7-0: 75 usos, 71 completados, efecto neto mediano 13,6, vida mediana al usarla 89 (`informe_P7_0.md:144`).
- **¿Alimenta además de curar?** **No consta.** Ni el manifiesto ni el catálogo describen hambre ni saciedad: buscar *hunger*, *food* o *satiety* no da nada. Es una búsqueda negativa, no una prueba.
- **Razón medida de que costara aprenderla: el techo de vida.** La criatura se la come con la vida casi llena, la cura queda cortada en 100 y el recuerdo se guarda como «al menos», que no fija el cuánto.
  - Está documentado en `informe_P7_58.md:67-68` («cura 15 fijos y casi siempre toca techo ("al menos"), deja de mover la creencia pronto») y en el paper en `cantera_cap3.md:670`.
  - Recontado en P7-30 (APRENDE, `P7_30_vidas.json`): 110 usos, 109 completados. **69 son «al menos» (63 %)** y 40 firmes. La vida mediana al usarla es 90. El efecto mediano es 8,0 en los «al menos» y 14,6 en los firmes, que empiezan con vida mediana 80.
- **Descartados:** que el efecto sea pequeño (cura los 15 completos cuando hay hueco) y que la ventana corte el uso (0 o 1 cortes en todo el campo).
- **Factores secundarios medidos:**
  - Importancia pequeña: mediana 0,145 en la ración frente a 0,409 en el botiquín (`informe_P7_36.md:76`). La importancia contrafactual es 0,021 (`informe_P7_38.md:84`).
  - El recuerdo neutro, de peso 1, tira la media hacia 0 (`informe_P7_36.md:78-79`).
- **Matiz:** en P7-30 la ración **no** costó más que el botiquín en ignorancia del cuánto. Al día 20 está entre 0,13 y 0,32 (`informe_P7_30.md:186`). Lo que no alcanza es la creencia de 12, el 80 % de 15: dos de cuatro criaturas no llegan nunca (`:93-98`).

---

## 5. Probar la red

Guiones:
- `revision_externa/r5_red_todo_P7.py` recorre los 6.185 diarios del siete y deja los resultados en `escaneo_todo.json`: tics con la red en la mano, ataques con ella, aperturas y huellas.
- `revision_externa/r5_r8_escanea_P7_50.py` hace lo mismo con P7-50 y deja en `escaneo.json` las acciones con la red en la mano y las 102 huellas.

- **Qué se registra:** **no es una acción del mundo.**
  - Es una ventana de 10 s que el cuerpo abre cuando la red entra en la mochila o en la mano, es decir cuando `tiene(...) ≥ 1` (`nace_P7_33.py:18-19,45,56-60,115-145`).
  - Al abrirse se registra `{"k":"P7_33_prueba","momento":"abre","objeto":"net"}` (`:128`). Al cerrarse, a los 10 s o antes si se suelta o se lanza, se registra `P7_huella` (`:140-144`).
  - Las acciones del mundo que llevan hasta ahí son `pickup` y `use` (empuñarla). Para lanzarla habría que hacer `attack` desde la mano; la red inmoviliza 3 s (`informe_P7_44.md:19`).
- **¿Llegó a lanzarse? No, nunca (verificado):**
  - En los 6.185 diarios del siete (`paintball/runs/P7*`, 83,3 M tics) hay 8.187.273 tics con la red en la mano de la propia criatura, y en **ninguno** la acción es `attack`.
  - Hay 1.779 aperturas y 1.751 huellas de red.
  - En P7-50 hay 102 huellas, todas cerradas por fin de la ventana y ninguna por soltarla o lanzarla. 96 tienen efecto 0.
- **Por qué (verificado):** en el decisor, solo un arma con `damage > 0` genera candidatos de ataque (`paintball/alma/decisor_zs.py:582`), y la red tiene daño 0 (`paintball/alma/mundo.py:153-155`). Los propios informes lo declaran: «este cuerpo no lanza la red; nunca inmoviliza a nadie» (`SELLO_P7_56.md:25`; también `informe_P7_54.md:14` e `informe_P7_57.md:35`).
- **Consecuencia (inferido):** «probar la red» mide llevarla 10 s encima, no su función. El «no hace nada» es cierto para este cuerpo, pero no dice nada de la red como objeto.
- **Inferido, no comprobado:** que la pareja del siete llega a este decisor. No se ha trazado toda la cadena de importaciones; el 0 empírico lo respalda.

---

## 6. Las 1.140 partidas de P7-67 (verificado contando `P7_67F_estado.json`: 1.140 peticiones `completed`, sin duplicados)

Guion: `revision_externa/r6_partidas_P7_67.py`.

| nivel (rivales activos) | brazos | series | días | partidas |
|---|---|---|---|---|
| 1 | MIENTE, CONGELADA, HONESTA | 16 | 1-20 | 3 × 16 × 20 = **960** (320 por brazo) |
| 2 | MIENTE, HONESTA | 6 | 1-5 | 2 × 6 × 5 = **60** |
| 3 | MIENTE, HONESTA | 6 | 1-5 | **60** |
| 14 | MIENTE, HONESTA | 6 | 1-5 | **60** |
| **Total** | | | | **1.140** en 84 cadenas (48 de 20 días y 36 de 5) |

- **Fuentes:** `informe_P7_67_campo.md:10`, `SELLO_P7_67.md:54` y `P7_67F_diseno.json`. Son 2.280 criatura-días (`informe_P7_67_campo.md:11`).
- **Repeticiones:** 6 partidas se apartaron por fallo de la plataforma y se repitieron (`:12`), así que se gastaron 1.146 créditos (`:162`). Las 6 carpetas `*_apartada1` no entran en el análisis, porque el patrón de búsqueda pide el nombre exacto (`analiza_P7_67.py:193`).

---

## 7. La ignorancia media del cuánto y el recuerdo firme

Sin guion: este apartado es lectura de código. Las fórmulas y los umbrales se citan con su archivo y su línea.

- **Fórmula** (`nace_P7_29.py:95-100`, la que hornea `Dockerfile.pareja_P7_30`):
  - `ignorancia_cuanto = PESO_NEUTRO / (PESO_NEUTRO + pesos_firmes)`
  - `pesos_firmes = Σ intensidad · OLVIDO^(día_actual − día_del_recuerdo)`, sumado **solo sobre los recuerdos firmes**.
  - Constantes (`cuaderno_P7.py:23-25,73`): `PESO_NEUTRO = 1.0`, `OLVIDO = 0.95` y intensidad = 1 + min(1, Σ|importancia| / 1,5), que va de 1 a 2.
- **Las cifras 0,944 y 0,337** (`informe_P7_30.md:63-66`): son la **media, sobre las 20 vidas del bloque**, de `ignorancia_cuanto` al cerrar el día (`escribe_informe_P7_30.py:19`). Si falta el dato, cuenta como 1,0 (`analiza_P7_30.py:44`).
- **Qué la hace bajar:** solo los recuerdos firmes. Cada uno suma entre 1 y 2 al denominador; los cortes y los «al menos» no cuentan. El olvido (×0,95 por día) la hace volver a subir.
  - Sin ningún firme vale 1,000: por ejemplo, s1·a10 se queda en 1,000 hasta el día 15, con 0 firmes y 21 cortes.
  - BORRADO se queda cerca de 1 porque empieza cada día sin cuaderno.
- **Recuerdo firme** (`SELLO_P7_30.md:22`): es un uso **completado y no «al menos»**. No tiene una constante propia; salen de dos condiciones:
  - **Completado:** la unidad se gastó, `unidades_de(...) < n0` (`nace_P7_23.py:102`). Si no se gastó, es un corte.
  - **No «al menos»:** la vida no llegó al tope durante la ventana, es decir no se cumplió `hp >= hp_max` (`nace_P7_23.py:98,106`), con `hp_max` = 100 (`:91`).
  - El análisis los cuenta en `analiza_P7_30.py:35` y la criatura en `nace_P7_29.py:97`.

---

## 8. «Nada falso se contagió» (P7-50 / P7-55)

Hay **dos criterios distintos**, en dos niveles: el recuerdo suelto y la creencia agregada.

Guiones:
- `revision_externa/r8_siete_P7_50.py` da los 377 recibidos y los 7 que contradicen el efecto real, uno a uno. Lee `escaneo.json`, que deja `r5_r8_escanea_P7_50.py`.
- `revision_externa/r8_umbral_P7_55.py` da la tabla de sensibilidad al umbral y los máximos.

1. **P7-50, recuerdo a recuerdo: «7 de 377»** (`analiza_P7_50.py:37-40`; `informe_P7_50.md:87-88`).
   - Un recuerdo recibido «contradice el efecto real» si su efecto en el cuerpo es **> 1,0** para la red o el camuflaje (que no curan), o **≤ 0** para el botiquín o la ración (que sí).
   - Los 377 son los recibidos en COMPARTE: 330 contados (301 por canal y 29 por la noche) y 47 vistos. Por series son 130 + 113 + 134, y los 7 se reparten 2 + 2 + 3 (`P7_50_sello.json`). En SOLAS no se recibe nada.
2. **P7-55, creencia por hermana y día: «0 de 120»** (`analiza_P7_55.py:59-60`).
   - Una creencia falsa contagiada es aquella en la que la creencia con todo lo recibido (`a`) es falsa y la creencia solo con lo vivido (`b`) no lo es:
     - red o camuflaje: a > 5 y b ≤ 5;
     - botiquín o ración: a ≤ 0 y b > 0.
   - La creencia es la media ponderada con neutro de peso 1 y olvido 0,95 (`:32-44`). Resultado: `falsos = []` en 120 hermana-días.

**Cómo encajan los 7 (verificado en los diarios de P7-50):**
- Los 7 son **heredados** (contados por la hermana: 4 por canal y 3 por la noche), no vistos ni propios. Ninguno es inventado: cada uno es una experiencia que la emisora vivió de verdad y que pasó tal cual.

| serie · día | asiento | objeto | efecto en el cuerpo | vía |
|---|---|---|---:|---|
| s1 · d16 | a10 | camuflaje | +30,8 | canal |
| s2 · d12 | a10 | camuflaje | +8,0 | canal |
| s2 · d16 | a10 | red | +28,72 | noche |
| s1 · d8 | a11 | botiquín | 0,0 | canal |
| s3 · d10 | a11 | ración | −4,8 | noche |
| s3 · d10 | a11 | ración | −5,0 | noche |
| s3 · d17 | a11 | ración | −5,0 | canal |

- **Inferido:** son efectos confundidos dentro de la ventana. Los +28 y +30 vendrían de una cura en los mismos 10 s, y las raciones de −5 caen hacia el final de la partida, con el daño de la zona.
- **Por qué no cuentan en P7-55:** en botiquín y ración, un recuerdo malo suelto queda diluido entre muchos positivos y no baja la creencia a ≤ 0. En red y camuflaje, el umbral es 5, no 1.
- **Sensibilidad (verificado, recalculado sobre `P7_55_datos.json`):** dos de los contagios dejaron a la hermana a10 **justo por debajo del umbral**, con b = 0: camuflaje en s1 d16 con a = 4,08, y red en s2 d16 con a = 4,71.

  | umbral para lo inútil | hermana-días que contarían | hermanas afectadas |
  |---:|---:|---:|
  | > 5 (sellado) | 0 | 0 |
  | > 4 | 3 | 2 |
  | > 3 | 9 | 2 |
  | > 2 | 10 | 2 |
  | > 1 | 12 | 2 |

  Corrección del 26-oct al pasar los guiones al repositorio: la versión anterior de esta tabla daba 3 hermanas en «> 1», pero son 2, s1·a10 y s2·a10 (`r8_umbral_P7_55.out`). Se añade la fila «> 2».

  - El código no justifica el 5. **Inferido:** es el 10 % de la cura del botiquín (`analiza_P7_55.py:11`).
  - La frase «red 3,1, camuflaje 2,9» (`informe_P7_55.md:45`) es **solo del día 20**. Los máximos sobre los 20 días fueron 4,71 y 4,08.
  - El único caso por encima de 5 es **propio**: s2·a11, red, día 15, con a = 5,05 y b = 7,61. La regla lo excluye por diseño.
- **Formulación defendible:** con el umbral sellado de 5, ninguna creencia falsa vino de la hermana. 7 de los 377 recuerdos recibidos contradecían el efecto real, y dos de ellos dejaron a una hermana varios días con una creencia de 4,1 y 4,7 en un objeto inútil, por debajo del umbral. «Nada falso se contagió» depende, por tanto, del umbral.

---

## 9. ¿Escala el mando del miedo la S-COMPANIA? (añadido el 26-oct, a raíz de un hallazgo de otra ventana)

Guion: `revision_externa/r9_compania_P7_50.py` (salida en `r9_compania_P7_50.out`). Recorre los diarios de P7-50 y saca la M de S-COMPANIA que registra cada tic, y los cierres del mando.

### 1) ¿Es así? **Sí: el mando no escala la S-COMPANIA que actúa (verificado en el código y en los diarios).**

- **Qué escala el mando:** envuelve `A.filas` y multiplica las filas de `FILAS_MIEDO` solo si valen algo (`miedo_P7_49.py:26-35`; `if v:` en `:32`). S-COMPANIA está en esa lista (`:16`).
- **La S-COMPANIA que sale de `A.filas` es la del cinco, y está apagada:**
  - `COMPANIA_ON = False` (`paintball/alma/appraisal_zs_v42_exp.py:314`, «candado 62»).
  - `filas()` la pone a 0,0 (`:1014`) y solo la enciende con `COMPANIA_ON` (`:1015`).
  - Como vale 0, el `if v:` la salta: el mando multiplica un cero y ni siquiera la cuenta en `filas_escaladas`.
- **La S-COMPANIA que actúa es la del seis**, de `cantera/paper6/filas10_P6_10.py`, enganchada en `cantera/paper6/policy_pareja11.py:54`.
  - Se mete **después**, envolviendo `A.appraise`: llama al `appraise` original, que es el que llama a `filas()` y por tanto al mando (`appraisal_zs_v42_exp.py:1673`).
  - Después calcula `m_c = compania_M(d, amenaza)` con techo `GEMV_COMPANIA_TECHO = 0.32` (`filas10_P6_10.py:64,93-103,146`; `Dockerfile.pareja_P7_49:159`, y lo mismo en todas las imágenes del siete).
  - Ese valor lo suma directamente a las fuerzas (`:153-155`) y lo apunta en la radiografía (`:156`). El factor del mando no aparece en ningún punto.
  - El orden en que se enganchan las piezas no cambia nada: el mando actúa dentro de `filas` y la fila del seis se suma fuera, después de `filas`.
  - Las llamadas directas del decisor a `A.filas` (`paintball/alma/decisor_zs.py:656-657,673-674`) solo leen R-ACOPIO y S-8-EXPOSICION.
- **Comprobación en los diarios de P7-50**, con la valiente en el asiento 10 (MIEDO 0,5) y la prudente en el 11 (MIEDO 1,5):

| brazo · hermana | tics con S-COMPANIA > 0 | fracción de tics | máximo | mediana | p95 | tics en el techo 0,32 |
|---|---:|---:|---:|---:|---:|---:|
| COMPARTE · valiente (0,5) | 41.094 | 5,1 % | **0,32** | 0,018 | 0,061 | 109 |
| COMPARTE · prudente (1,5) | 37.725 | 4,6 % | **0,32** | 0,030 | 0,106 | 92 |
| SOLAS · valiente (0,5) | 23.567 | 2,8 % | **0,32** | 0,018 | 0,073 | 482 |
| SOLAS · prudente (1,5) | 21.521 | 2,7 % | **0,32** | 0,030 | 0,117 | 140 |

  - Con la fila escalada, la valiente no pasaría de 0,16 y la prudente llegaría a 0,48. Las dos tocan exactamente 0,32, el techo sin escalar.
  - La mediana es mayor en la prudente. **Inferido:** se debe a la distancia y a la calma en que se encuentra, no a un factor del mando.
- **Por tanto, el mando escala de verdad 8 filas, no 9**, además de la cautela del probar.
- **Dónde está escrito lo contrario:**
  - el apéndice del paper (`gemv-paper7/escritura/cantera_cap4.md:498-500`, «Qué escala (× MIEDO)»);
  - la tabla de `informe_P7_49a.md:24` y su línea de código `:32`;
  - el docstring de `miedo_P7_49.py:3-4,7`, que dice que escala «lo que el decisor fotografía»;
  - `informe_P7_filas_sociales.md:25`, con «×miedo» en la fila de S-COMPANIA, y `:38`;
  - «con 9 filas» en `informe_P7_50.md:63`, que cuenta la lista declarada, no las filas escaladas.

### 2) ¿Depende algo del paper siete de que el mando escale S-COMPANIA?

**Ningún número cambia.** Todos los números de la sección 4, y los de P7-50 en adelante, se midieron con el cuerpo tal como era: la S-COMPANIA sin escalar. Ninguno se calculó suponiendo el factor. Lo que cambia es la **lectura** de tres pasajes y la descripción del mando:

1. **El apéndice («qué escala el regulador»):** es incorrecto tal como está. Hay que quitar S-COMPANIA de la lista de lo que se escala y pasarla a lo que queda intacto, «de hecho».
   - Habría que decir que la intención declarada por Manel («la valiente es más independiente», `informe_P7_49a.md:24`) **no llegó a implementarse**.
   - La corrección pertenece al paper, no al código, y queda para Manel. No se ha tocado ninguno de esos archivos.
2. **«La sospecha sobre S-COMPANIA no se confirma»** (`cantera_cap4.md:176`, citando `informe_P7_50.md:89`): la sospecha era que «el miedo a separarse escalado atasca a las prudentes».
   - Ese mecanismo no existía, así que «no se ve» no es una prueba en contra: **no podía verse**.
   - El dato se mantiene (rachas cortas: 50 en las valientes de COMPARTE frente a 10 en las prudentes), pero hay que quitar la conclusión sobre S-COMPANIA.
3. **Las diferencias entre la valiente y la prudente en la sección 4** (pruebas, quietud, rachas y distancia, `cantera_cap4.md:155-176,354-362`): ninguna se puede atribuir a la S-COMPANIA. Se explican por las otras 8 filas y la cautela.
   - Es coherente con que la distancia media a la hermana sea casi igual: 2,65 frente a 2,70 en COMPARTE y 2,67 frente a 2,71 en SOLAS (`informe_P7_53.md:27-30`).
   - Esa igualdad no debe leerse como «el miedo a separarse no cambia la distancia», porque ese miedo no se moduló.
   - **Inferido:** la fila pesa poco. Está encendida en el 3-5 % de los tics, con mediana de 0,02-0,03, y es 0 dentro de las 7 casillas de camino (`filas10_P6_10.py:62,100-101`), mientras que la distancia media es de unas 2,7 casillas. Aunque se hubiera escalado, cabe esperar un efecto pequeño. No se ha medido.
- **Lo que no se ve afectado:**
  - la identidad con MIEDO = 1 de P7-49a: con el factor 1 da igual qué filas estén en la lista;
  - los campos P7-56 a P7-67, que no hacen ninguna afirmación sobre S-COMPANIA;
  - los capítulos 3 y 5, donde la búsqueda de «COMPANIA» no da nada sobre el mando.
- **Alcance de la comprobación:** con los diarios solo se ha mirado P7-50. Para el resto de campos con mando (P7-56, 57, 61, 62, 63, 65, 66 y 67) se ha comprobado que la ruta de código es la misma, con las mismas piezas y el mismo techo de 0,32 en todas las imágenes, pero no se han recorrido sus diarios.

---

## 10. P7-56, R2 con la pareja como unidad (segunda revisión externa)

Guion: `revision_externa/r10_P7_56_pareja.py` (salida en `r10_P7_56_pareja.out`). Ejecuta la lógica sellada de `erratas_P7_56.py` sin su escritura.

- **En R2, pareja y serie son lo mismo.** R2 solo usa el brazo CON_RAZON, y en él cada serie es una única pareja: los asientos 10 y 11 juegan cada día en la misma partida y comparten recuerdos.
  - Comprobado: 60 partidas CON_RAZON completadas (3 series × 20 días), una por cada (serie, día), y en las 60 se leen las dos hermanas.
  - Por tanto, hay **3 unidades independientes**.
  - Entre series, las semillas son distintas, aunque es la misma sucesión reordenada (`SELLO_P7_56.md:14`).
- **Resultado (cuenta corregida, `verdad_sello`), diferencia entre la confianza tras una propuesta verdadera y tras una falsa:**

| cuenta | s1 | s2 | s3 | media | ee | razón en ee | p de una cola (t, 2 gl) |
|---|---:|---:|---:|---:|---:|---:|---:|
| todas, evaluaciones de la pareja juntas | 0,247 | 0,539 | 0,480 | 0,422 | 0,089 | **4,7** | 0,021 |
| todas, media de las dos hermanas | 0,223 | 0,547 | 0,480 | 0,416 | 0,099 | **4,2** | 0,026 |
| sin marcadas, evaluaciones juntas | 0,256 | 0,437 | 0,435 | 0,376 | 0,060 | **6,3** | 0,012 |
| sin marcadas, media de las dos hermanas | 0,212 | 0,447 | 0,387 | 0,349 | 0,070 | **5,0** | 0,019 |

- **No queda por debajo de 3.** Con la pareja (o serie) como unidad, R2 está entre **4,2 y 6,3 errores típicos**, según la cuenta. Las tres parejas dan una diferencia positiva, de 0,21 a 0,55.
  - El ee agrupado por pareja del punto 1a (7,3 ee) sobrestima la precisión: con solo 3 grupos ese estimador es poco fiable, y la cifra que debe usarse es la de esta tabla.
- **Advertencia: con 3 unidades, «errores típicos» no significa lo mismo que con muchas.**
  - El ee está estimado con 2 grados de libertad. Por eso 4,7 ee equivale a p ≈ 0,02 de una cola, no al p de 10⁻⁶ que daría la normal.
  - El listón sellado de 3 ee, aplicado a 3 unidades, equivale a p ≈ 0,05 de una cola.
  - Lectura honesta: «la confianza sigue a la verdad en las tres parejas, y la media está a unas 4-6 veces su error, con solo tres parejas».

---

## 11. El «umbral de 5» de P7-55

Guion: `revision_externa/r11_umbral_P7_55.py` (salida en `r11_umbral_P7_55.out`). Ejecuta las funciones selladas `recuerdos`, `dedup` y `creencia` de `analiza_P7_55.py` sobre los cuadernos de P7-50.

- **Qué variable es:** la **creencia del cuerpo** sobre un objeto (`analiza_P7_55.py:32-44`). Es lo que la hermana espera ganar o perder de **vida** con el objeto, dentro del anillo.
  - Se calcula como la media ponderada del efecto en el cuerpo de sus recuerdos del objeto.
  - El peso de cada recuerdo es su intensidad × 0,95^(días transcurridos).
  - Se suma siempre un recuerdo neutro de peso 1 y efecto 0.
  - Los recuerdos cortados no cuentan, y los «al menos» solo cuentan si suben la media.
- **Unidades:** puntos de vida, en la escala de 0 a 100 del mundo. Como referencia, el efecto real del botiquín es 50, el de la ración 15, y el de la red y el camuflaje 0 (`:11`).
- **A qué objetos se aplica el 5:** solo a la **red y el camuflaje**, que no curan.
  - «Creer algo falso por lo recibido» es tener una creencia mayor que 5 con todo lo recordado (`a`) cuando con lo vivido solo es 5 o menos (`b`).
  - Para el botiquín y la ración el criterio es otro: con todo lo recordado, creer que no curan (≤ 0) cuando lo vivido dice que sí (> 0) (`:5-6,59-60`).
  - El 5 equivale al 10 % de la cura del botiquín. El código no da ninguna justificación (inferido, punto 8).
- **Qué son los 120:** **hermana-días de 6 criaturas**, las 6 hermanas del brazo COMPARTE de P7-50 (3 series × valiente y prudente) × 20 días.
  - Cada hermana-día es el cuaderno con el que esa hermana cierra el día, y la creencia se evalúa para el día siguiente (`:52-54`).
  - En cada hermana-día se miran los cuatro objetos: 240 comprobaciones con el umbral de 5 (red y camuflaje) y 240 con el umbral de 0 (botiquín y ración).
  - **No son 120 unidades independientes:** son 6 criaturas, 3 parejas, seguidas día a día.
- **Qué significan el 4,1 y el 4,7:** son dos de esas creencias, en puntos de vida, de la valiente (asiento 10). En los dos casos, todo lo que ella vivió decía 0 (b = 0).
  - **4,1 (s1·a10, camuflaje, cuaderno del día 16):**
    - Tenía 20 recuerdos del camuflaje. Sus 6 propios daban efecto 0, y de los 14 recibidos, 13 daban 0 y uno daba **+30,8**. Ese recuerdo, contado por el canal el día 16, era el de más peso (3,80).
    - La media es 117,04 / 28,72 = **4,08**.
    - Sin ese único recuerdo habría sido 0. Creía que llevar el camuflaje cura unos 4 puntos de vida, cuando la verdad es 0.
  - **4,7 (s2·a10, red, cuaderno del día 16):**
    - Tenía 16 recuerdos. Todos daban 0 (o −0,16) salvo uno de **+28,72**, contado de noche (peso 3,80), que era la huella de la otra hermana del día 15.
    - La media es 108,92 / 23,14 = **4,71**.
  - **Inferido:** las dos cifras salen de un recuerdo verdadero pero confundido, en el que una cura cayó dentro de los mismos 10 s de la prueba (punto 8).
  - Al día 20, el olvido y los nuevos recuerdos de 0 las habían bajado a 2,91 y 3,15.
  - La creencia que usó el cuerpo de verdad, sin quitar duplicados, fue 3,28 en el camuflaje y 4,71 en la red.
  - **No se ha comprobado** si estas creencias cambiaron alguna decisión.

---

## 12. La moneda de P7-46: «como si hubiera probado lo mismo»

Guion: `revision_externa/r12_moneda_P7_46.py` (salida en `r12_moneda_P7_46.out`). Vuelve a ejecutar `analiza_P7_46.py` sin su escritura y lo compara con `P7_46_resumen.json`.
- Las 349 forzadas, las 101 que acaban y todo R1 coinciden exactamente.
- Solo difiere un diagnóstico secundario, el de los registros `llena8`. Se calculaba con los diarios `.art.log`, que ya no están en disco, solo los `.zip` (`analiza_P7_46.py:46-48`). No interviene en las cifras.

**En lenguaje llano:**

- **La moneda.** A la criatura sin emoción, de vez en cuando, una moneda al azar le ordena ir a coger uno de los cuatro objetos o usarlo. Es lo que se llama una «forzada».
  - Hubo 349 órdenes en 120 vidas, y solo 101 (29 %) se cumplieron en el plazo de 10 segundos. 243 caducaron y 5 quedaron sin terminar porque murió o acabó la partida (`informe_P7_46.md:13`).
  - Casi siempre fallaban por el cuerpo, no por la moneda. Si le pedía usar algo con la vida llena, el cuerpo no lo ofrece. Si le pedía ir a por algo, llegaba pero no sabía cogerlo (`:30-37`).
  - Por eso la criatura sin emoción probó el botiquín unas tres veces menos que las que aprenden: 0,48 veces por vida, frente a 1,42 y 1,61.
- **La cuenta «como si hubiera probado lo mismo».** Ojo: no se jugó ni se simuló nada; es una cuenta sobre papel (`:84-87`; código en `analiza_P7_46.py:143-183`).
  1. De cada criatura sin emoción se tomó su calendario real: cuántas veces había probado el botiquín hasta cada día. Ese número se multiplicó por unas tres veces (2,9 o 3,3), lo que más lo probaban las que aprenden.
  2. Por las curvas de aprendizaje se sabe cuántas pruebas hacen falta para que la creencia típica llegue a «el botiquín cura al menos 25»: unas 10 con la curva de la criatura sin emoción. Con ese calendario multiplicado, se miró qué día habría llegado a esa cifra (21 si nunca).
  3. Se compararon esos días con los de las que aprenden.
- **Resultado:** la criatura sin emoción habría llegado de media a los 15,3 días en vez de a los 17,0. La diferencia con las que aprenden queda en −1,7 ± 4,4 días frente a la prudente y +2,0 ± 3,4 frente a la valiente. Es el mismo ruido que la cuenta real (−3,3 y +0,3), así que **R1 seguiría sin pasar**.
- **Por qué no cambia:** 3 de las 6 criaturas sin emoción no probaron el botiquín ni una vez, y tres veces cero sigue siendo cero.
- **Límites declarados:** la cuenta supone que cada prueba enseña lo mismo y que las pruebas de más caen en los mismos días que las reales. El propio informe marca la primera suposición como la débil (`informe_P7_46.md:125-130`).
- **Las 101 de 349 no entran en la cuenta de R1:** explican por qué la criatura sin emoción probó menos, pero R1 recontado solo usa sus pruebas reales del botiquín.

---

## Resumen para el revisor

| punto | ¿cambia algo? |
|---|---|
| 1a P7-56 | con la criatura como unidad: 5,6-9,4 ee (no 24,1); sigue pasando |
| 1b P7-65 | con la partida o la serie como unidad: 12,1 y 7,8 ee; sigue pasando |
| 1c P7-67 | con la pareja como unidad está bien. **El destino es común por día**: con el día como unidad, P1 ≈ 2,5 ee y P2 ≈ 2,9 ee, en el listón de 3 o por debajo. Se propone, no se decide |
| 1d confianza final | con la serie como unidad: 0,681 ± 0,033, 20 ee |
| 1e escala | con la serie como unidad: 5,32 ± 1,57, 3,4 ee (n = 5) |
| 2 regla | correcta con promesas negativas; la promesa 0 exige \|vivido\| < 1; ningún juicio mal aplicado |
| 3, 4, 7 | aclarados; el corte de 3 es en parte circular |
| 5 red | nunca se lanzó (0 `attack` con la red en la mano); «probar» es llevarla 10 s |
| 8 contagio | «nada» depende del umbral de 5; dos casos llegaron a 4,1 y 4,7 |
| 9 S-COMPANIA | el mando **no** la escala (la del cinco vale 0 y la del seis se suma después, sin factor; las dos hermanas tocan 0,32). Ningún número cambia. Hay que corregir el apéndice y retirar la conclusión «la sospecha sobre S-COMPANIA no se confirma» |
| 10 R2 por pareja | 3 parejas (= 3 series): 4,2-6,3 ee según la cuenta (4,7 con las evaluaciones juntas); **no baja de 3**, pero con 3 unidades equivale a p ≈ 0,01-0,03 de una cola |
| 11 umbral de 5 | creencia en puntos de vida (media ponderada de lo recordado) de la red y el camuflaje; los 120 son hermana-días de 6 criaturas; 4,1 y 4,7 salen de un único recuerdo recibido de +30,8 y +28,7 |
| 12 moneda | cuenta sobre papel: calendario real de pruebas × 3 contra las pruebas necesarias para creer «cura 25»; R1 sigue sin pasar; las 101/349 explican por qué se probó menos |
