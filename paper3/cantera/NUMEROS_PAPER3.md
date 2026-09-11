# NÚMEROS DEL PAPER TRES — cada cifra con su fuente

Fecha: 2026-09-05. Cada número se rastreó por `grep` en las actas de la
cantera. Lo que no aparece en ninguna acta va marcado **SIN FUENTE** y no se
rellena.

## Cabecera (verificados en frío desde los logs — ver `VERIFICACION_66.md`)

| número | valor | acta | script que lo produce |
|---|---|---|---|
| respuestas a agresor propio (66) | **918** | `66_manada2` | `manada_campo.py::honor_dos` |
| defensas por la hermana (66) | **104** | `66_manada2` | `manada_campo.py::honor_dos` |
| iniciaciones estrictas (66) | **0** | `66_manada2` | `manada_campo.py::honor_dos` |
| golpes entre hermanas (66) | **0** | `66_manada2` | `manada_campo.py::golpes_entre` |
| respuestas (64), para contraste de roster | **327** | `64_manada_campo`, `66_manada2` | ídem |
| golpes entre hermanas (64) | **3 de 4 por fuego amigo de defensa** | `64_manada_campo` | `manada_campo.py::golpes_entre` |

## El precio de defender

| número | valor | acta | script |
|---|---|---|---|
| Δhp de la defensora tras defender | **−20** (mediana) | `64_manada_campo`, `66_manada2` | `manada_campo.py::precio` |
| defensoras caídas en 240 tics | **0** | `64_manada_campo`, `66_manada2` | ídem |
| "ambas caen" | **0** | `64`, `66` | ídem |
| **defiende −14 vs acompaña −17** | p = **0,70** (15-12-5) | `67_proteccion` | `proteccion_pareada.py` |
| pares limpios del emparejado | **32** | `67_proteccion` | `proteccion_pareada.py` |
| protección: Δhp cazada 0 vs −14 | p ≈ **0,21 / 0,26** | `67_proteccion` | ídem |

## La ocasión y la certificación

| número | valor | acta | script |
|---|---|---|---|
| P2' vara vieja (64 / 66) | 62 % / 50 % (cotas inferiores) | `67_proteccion`, `68_nombre` | `proteccion.py` |
| **P2' vara nueva** (agresor visible ahora) | **78 % / 92 % / 86 % acumulado** | `68_nombre` | `desenlaces.py::ocasiones_v2` |
| las 6 sin defensa: candidato existente | **0 de 39 tics** | `67_proteccion` | inline (acta) |
| fotos que recupera la identidad | **3 de 6** | `68_nombre` | `verifica_68.py` |

## El forense de las peleas (66)

| número | valor | acta | script |
|---|---|---|---|
| ventanas de respuesta | **74** | `68_nombre` | `desenlaces.py::respuestas` |
| acaban matándonos | **0 %** | `68_nombre` | `desenlaces.py::desenlace` |
| el agresor se va | **46 %** (4 golpes de mediana) | `68_nombre` | ídem |
| acoso persistente | **3 %** | `68_nombre` | ídem |
| kills que el mundo nos apunta (80 diarios) | **7** | `68_nombre` | inline (acta) |

## Los reencuentros (69)

| número | valor | acta | script |
|---|---|---|---|
| reencuentros en 80 episodios | **138** (51 eps, mediana 1) | `69_reencuentros` | `reencuentros.py` |
| como % de las 74 peleas | **186 %** | `69_reencuentros` | ídem |
| caso exacto (arma + aproximación) | **n=15**: él **7** / nadie **6** | `69_reencuentros` | ídem |
| aviso mediano | **21 tics** | `69_reencuentros` | ídem |
| "pegó a la hermana y viene a la otra" | **53 %** | `69_reencuentros` | ídem |
| gaps > 96 tics | **54 %** | `69_reencuentros` | ídem |
| **muertes en 138 reencuentros** | **1** | `69_reencuentros` | ídem |

## El miedo con memoria (70 → 71)

| número | valor | acta | script |
|---|---|---|---|
| la fila se enciende (v37, último golpe) | **13 de 15**, adelanto **7 tics** | `70_memoria` | `verifica_70.py` |
| magnitud v37 (último golpe) | **0,18** (mediana 0,17) | `70_memoria` | ídem |
| acciones cambiadas en v37 | **0** | `70_memoria` | ídem |
| daño acumulado real de los que vuelven | **mediana 52 · máx 211** (mín 8) | `71_memoria2` | `runs/casos_exactos.json` |
| **magnitud v37b (acumulado)** | **0,49** mediana (máx 1,40) | `71_memoria2` | `verifica_71.py` |
| **acciones cambiadas** | **8 de 15**, todas a distancia/pared | `71_memoria2` | ídem |
| golpes nacidos de la memoria | **0 de 90 acciones** | `71_memoria2` | ídem |
| botín/cura abandonados vs distancia ganada | **0 vs 28 tics** | `71_memoria2` | ídem |

## El canal (antecedente, temporada dos)

| número | valor | acta | script |
|---|---|---|---|
| mensajes de team analizados | **17.601** | `52_primer_minuto` | inline (acta 52) |
| terceros que leyeron el canal | **0** | `52_primer_minuto` | ídem |
| latencia del canal | **+2 tics** | `52_primer_minuto` | ídem |
| **partes emitidos (2.368)** | — | — | **SIN FUENTE** |
| **partes 344** | — | — | **SIN FUENTE** |
| **partes 552** | — | — | **SIN FUENTE** |

> **Nota sobre los tres SIN FUENTE**: las actas dan los partes en medianas por
> diario (`55_pareja`: 16 emitidos / 9 leídos por diario; `57_pareja2`), no en
> totales absolutos. Los totales 2.368 / 344 / 552 no aparecen en ninguna acta
> de la cantera. Si han de ir al paper, hay que recalcularlos de los diarios
> (son derivables: contar `k=="voz"` con marca `E1` por tanda) y dejar
> constancia del cálculo — pero **hoy no tienen fuente escrita**.

---

# LA ABLACIÓN DE CAMPO (acta 72) — la sección de atribución

**Definición de "don" usada en el 72, aplicada IGUAL a las dos tandas** (para
que la pareja sea justa): *tic en que la gemela elige un candidato `soltar_*`
con la hermana **viva** y a **≤2 casillas**.* Contada con el mismo recorrido
sobre los diarios en `ablacion` y en `manada2`.

| vara | **72 · v27-pareja (social OFF)** | 66 · v35 (social ON) | sello |
|---|---|---|---|
| defensas por la hermana | **0** | **104** | P1 CUMPLE |
| **dones** (misma definición) | **1** (en 1 ep) | **98** (en 13 eps) | P2 no es 0 → forense |
| respuestas a agresor propio | **711** | **918** | P3 CUMPLE (−22,5 %, dentro de ±30 %) |
| iniciaciones estrictas | **0** | **0** | P3 CUMPLE |
| distancia mediana entre hermanas | **4,24** | **3,61** | P4 CUMPLE |
| golpes entre hermanas | **0** | **0** | P6 CUMPLE |
| ataques elegidos a la hermana | **0** | **0** | P6 CUMPLE |
| score medio de la pareja | 3,12 | 2,65 | P5 sin sello |
| placement mediano | 12,0 | 12,0 | P5 sin sello |
| kills | 10 | 9 | P5 sin sello |
| top-4 del mejor | 8 (20 %) | 5 (12 %) | P5 sin sello |
| "ambas caen" (≥13) | 11 | 11 | P5 sin sello |
| una en pie a 8 | 14 | 12 | P5 sin sello |

**El don único del 72, con su origen** (forense obligado por la regla C):
`ereq_9c3c18ad`, t2002, gemela P11 elige **`soltar_rations`** con la hermana a
hp 60 y a 1,4 casillas; lo mueve **`S-DANO-PAREJA` = 0,50**, fila del
**PROMPT_12** (v19/v27), **no** del paper tres.

> **Cómo enunciar la atribución**: la comparación es **social mínima vs social
> completa**, no "asocial vs social". La v27 conserva S-DANO-PAREJA y
> S-MUERTE-PAREJA desde el 12 y con ellas produce **1 don en 40 episodios**;
> las filas del paper tres llevan ese número a **98** y las defensas de **0 a
> 104**. Fuente: `actas/72_ablacion_acta.md`.

**Gate previo (antes de gastar)**: `v27-pareja` comparada fila a fila y
`State` a `State` contra el appraisal v27 histórico (`aeac3f2`): **0
diferencias, 0 filas sociales vivas** con la hermana herida delante; bancos
13-28 con los interruptores en OFF: **12/12**.
