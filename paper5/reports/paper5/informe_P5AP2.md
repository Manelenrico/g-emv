# P5-AP2 — quién nos mató y quién nos pegó en el mundo lento

**Solo lectura, coste cero.** Nada lanzado, nada enviado. Motor, decisor y tabla
intocados (`1e511978c251130e95169ebf8443efa1` · `8fa03547e3228ef9df4aa94c444f9252`
· `98c13d60167c80cc8334c965be75c640`). **No aparece ninguna clave.**

**Regla de atribución, la misma de `E3_golpes.py`:** la muerte va al **último
golpe registrado en los 48 tics anteriores al `match_ticks`** del propio diario;
si no hay ninguno, **«no consta»**. El mapa puesto→política sale de
`episodes[0].participants[].position` / `.policy_name`, que el servidor devuelve
en cada episodio. Medidor: `cantera/paper5/mide_P5AP2.py`, datos en `P5AP2.json`.

---

## El titular

**`relh-zero-sum` nos mató cuatro de cada diez veces, y es una de las tres
políticas que metimos por triplicado en el mundo lento por considerarlas
pacíficas.**

| | |
|---|---|
| **muertes nuestras** | **389** |
| **a manos de `relh-zero-sum`** | **156 = 40,10 %** |
| **golpes que nos dio** | **1.373 = 32,54 %**, el primero de la lista |
| **tic en que mata** | **mediana 8.723 · mín 8.191 · máx 12.162** |

**Y el detalle que lo explica todo: NUNCA mató antes del tic 8.191.** El criterio
con el que se eligió el roster miraba **antes del tic 2.000**, así que en aquel
recuento salía con **2 golpes y cero muertes** y entró como pacífica.

**Las otras dos que triplicamos sí lo son:** `belobog` **69 golpes y 0 muertes**;
`zero-sum-scavenger` **112 golpes y 3 muertes**. **El error fue con una de tres.**

**El reparto es estable en las tres series**: 39,3 % en P5-6C, 33,8 % en P5-7C y
35,9 % en P5-8M. **No es un accidente de una serie.**

---

## Alcance de la medida, dicho antes de los números

| | |
|---|---|
| episodios del paper cinco con registro | **216** |
| **de ésos, con `participants` y carpeta de diarios** | **200** |
| **diarios leídos** | **399** |
| **muertes (`reason == "eliminated"`)** | **389** |
| no eliminados | **6 `match_over` · 4 `winner`** |

**Los 16 que faltan:**

- **5 episodios de P5-6B** (`P56B_A_peticion`, `P56B_C0F_peticion`,
  `P56B_F2_peticion`, `P56B_F_peticion`, `P56B_T_peticion`): tienen
  `participants` pero **no se conservó la carpeta de diarios**.
- **11 más** cuyo documento guardado es la instantánea de la petición.
- **Y un diario suelto**: 399 y no 400, porque **`K/20784561` asiento 10 no tiene
  artefacto** (la plataforma no lo produjo; ver `informe_P5ARI_cierre.md`).

**Así que todo lo de abajo es sobre 200 episodios y 399 vidas.**

---

## 1 · Quién nos mató — 389 muertes

| quién | muertes | % |
|---|---|---|
| **`relh-zero-sum`** | **156** | **40,10 %** |
| `sivanlevy-zs-courier` | 73 | 18,77 % |
| **el anillo** | **55** | **14,14 %** |
| **«no consta»** | **43** | **11,05 %** |
| `zs-patient` | 27 | 6,94 % |
| `skourehjan-zero-sum-scripted-v1` | 23 | 5,91 % |
| `aaron-zs-fable` | 7 | 1,80 % |
| `zero-sum-scavenger` | 3 | 0,77 % |
| veneno (`poison`) | 2 | 0,51 % |
| **`belobog`** | **0** | **0,00 %** |
| **total** | **389** | |

*Fuente: `cantera/paper5/P5AP2.json`, clave `muertes`, producido por
`mide_P5AP2.py` (la regla de atribución, `:5-7` y `:88-92`).*

**Tres cosas que conviene leer juntas:**

1. **`relh-zero-sum` solo mata más que las cuatro siguientes juntas** (156 contra
   73 + 55 + 43 = 171, casi).
2. **El anillo es el tercero.** En un mundo que se cierra un 25 % más despacio,
   el anillo sigue matando al 14 % de nuestras criaturas.
3. **Los «no consta» son 43 = 11,05 %.** Son muertes sin ningún golpe registrado
   en los 48 tics previos: el diario deja de observar al morir. **Es el límite de
   la regla, no un asesino.**

---

## 2 · `relh-zero-sum`: cuánto y cuándo

| | |
|---|---|
| **muertes** | **156 de 389 = 40,10 %** |
| **tic de la muerte, mediana** | **8.723** |
| **mínimo** | **8.191** |
| **máximo** | **12.162** |

**Lo llamativo no es la mediana: es el mínimo.** En **156 muertes no hay ni una
sola antes del tic 8.191**. Con partidas de 18.240 tics, eso es a partir del
**45 % de la partida**, y **justo después de que el anillo empiece a avisar**
(tic 7.296, el 40,0 %).

### Contra los otros tres, para ver la forma

| quién | n | mediana | mín | máx |
|---|---|---|---|---|
| `sivanlevy-zs-courier` | 73 | **2.455** | 798 | 10.892 |
| `skourehjan-zero-sum-scripted-v1` | 23 | **2.502** | 1.190 | 5.388 |
| **`relh-zero-sum`** | **156** | **8.723** | **8.191** | 12.162 |
| el anillo | 55 | **12.817** | 10.753 | 14.785 |

**Hay tres tiempos en el mundo lento:** los que matan pronto (`sivanlevy` y
`skourehjan`, medianas 2.455 y 2.502), **`relh-zero-sum` en la mitad**, y el
anillo al final.

**Y ahí está el fallo del roster:** el criterio de selección era «antes del tic
2.000». `sivanlevy` y `skourehjan` caen dentro de esa ventana y se dejaron con
2 y 1 puestos. **`relh-zero-sum` cae cuatro mil tics después de la ventana, así
que el filtro no lo vio, y se le dieron tres puestos.**

---

## 3 · Los golpes recibidos, en todo el episodio

| quién | golpes | % |
|---|---|---|
| **`relh-zero-sum`** | **1.373** | **32,54 %** |
| **el anillo** | **910** | **21,56 %** |
| `sivanlevy-zs-courier` | 841 | 19,93 % |
| `skourehjan-zero-sum-scripted-v1` | 444 | 10,52 % |
| `zs-patient` | 329 | 7,80 % |
| `aaron-zs-fable` | 113 | 2,68 % |
| `zero-sum-scavenger` | 112 | 2,65 % |
| `belobog` | 69 | 1,64 % |
| veneno (`poison`) | 26 | 0,62 % |
| **nuestras propias políticas** | **3** | **0,07 %** |
| **total** | **4.220** | |

*Fuente: `P5AP2.json`, clave `golpes`.*

### Golpes contra muertes: quién remata

| | golpes | muertes | golpes por muerte |
|---|---|---|---|
| **`relh-zero-sum`** | 1.373 | **156** | **8,8** |
| `sivanlevy-zs-courier` | 841 | 73 | 11,5 |
| `skourehjan-…-v1` | 444 | 23 | 19,3 |
| `zs-patient` | 329 | 27 | 12,2 |
| `zero-sum-scavenger` | 112 | **3** | **37,3** |
| **`belobog`** | **69** | **0** | **nunca remata** |

**`relh-zero-sum` es el que más pega Y el que mejor remata.** `belobog` pega 69
veces y no mata ni una.

### El fuego amigo

**Tres golpes en 399 vidas vinieron de nuestra propia política** —uno de
`gemv-p56c2-F`, uno de `gemv-p57c-A` y uno de `gemv-p58m-A`—, es decir **del
hermano**. **Cero muertes.** Es el 0,07 % de los golpes.

---

## 4 · La misma tabla, serie por serie

### P5-6C · 196 muertes

| quién | muertes | % |
|---|---|---|
| **`relh-zero-sum`** | **77** | **39,29 %** |
| `sivanlevy-zs-courier` | 39 | 19,90 % |
| el anillo | 26 | 13,27 % |
| «no consta» | 22 | 11,22 % |
| `skourehjan-…-v1` | 15 | 7,65 % |
| `zs-patient` | 11 | 5,61 % |
| `aaron-zs-fable` | 4 | 2,04 % |
| veneno | 1 | 0,51 % |
| `zero-sum-scavenger` | 1 | 0,51 % |

### P5-7C · 77 muertes

| quién | muertes | % |
|---|---|---|
| **`relh-zero-sum`** | **26** | **33,77 %** |
| `sivanlevy-zs-courier` | 16 | 20,78 % |
| el anillo | 14 | 18,18 % |
| «no consta» | 7 | 9,09 % |
| `zs-patient` | 7 | 9,09 % |
| `skourehjan-…-v1` | 3 | 3,90 % |
| `aaron-zs-fable` | 2 | 2,60 % |
| veneno | 1 | 1,30 % |
| `zero-sum-scavenger` | 1 | 1,30 % |

### P5-8M · 78 muertes

| quién | muertes | % |
|---|---|---|
| **`relh-zero-sum`** | **28** | **35,90 %** |
| `sivanlevy-zs-courier` | 14 | 17,95 % |
| el anillo | 13 | 16,67 % |
| `zs-patient` | 9 | 11,54 % |
| «no consta» | 9 | 11,54 % |
| `skourehjan-…-v1` | 4 | 5,13 % |
| `zero-sum-scavenger` | 1 | 1,28 % |

### Las sondas (P5-8B, D, E, H, I, K) · 38 muertes

| quién | muertes | % |
|---|---|---|
| **`relh-zero-sum`** | **25** | **65,79 %** |
| «no consta» | 5 | 13,16 % |
| `sivanlevy-zs-courier` | 4 | 10,53 % |
| el anillo | 2 | 5,26 % |
| `skourehjan-…-v1` | 1 | 2,63 % |
| `aaron-zs-fable` | 1 | 2,63 % |

### ¿Cambia algo entre series? **No**

**El reparto es notablemente estable en las tres series grandes:** `relh` entre
**33,8 % y 39,3 %**, `sivanlevy` entre **17,9 % y 20,8 %**, el anillo entre
**13,3 % y 18,2 %**.

**Las sondas se salen (65,8 %)** y tiene explicación: son 38 muertes de pocos
episodios, y en varias de ellas el asiento vivió lo bastante para llegar a la
ventana de `relh`. **Con 38 casos no diría más.**

**El roster es idéntico en los 200 episodios**, comprobado en los
`participants`: `zero-sum-scavenger` 615, **`relh-zero-sum` 615**, `belobog` 615
(= 205 episodios × 3), `sivanlevy-zs-courier` 410 (×2), y `zs-patient`,
`aaron-zs-fable` y `skourehjan-…-v1` 205 (×1).

---

## Lo que esto le hace al paper

**La sección 3 dice que el mundo lento va «sin cazadores».** Los datos dicen que
**una de las tres políticas que pusimos por triplicado mata el 40 % de las
veces**. Lo que se quitó fueron los cazadores **tempranos**; el que mata en la
segunda mitad de la partida se quedó, y triplicado.

**No invalida los resultados del paper** —los dos brazos de cada semilla se
enfrentaron exactamente al mismo roster, comprobado elemento a elemento en
`informe_P5ARI2.md` §8— **pero sí la descripción del mundo**. Conviene que el
texto diga «sin cazadores tempranos» o describa el roster por lo que hace, no
por lo que se creyó.

**Y da una explicación barata a algo que quedó sin explicar en P5-8M:** las
muertes de K y de A se reparten igual porque **el 40 % de ellas las causa la
misma política, en la misma ventana de tics, en los dos brazos**.

---

## Lo que no sé, marcado como tal

**Los 43 «no consta» (11,05 %) podrían cambiar el reparto.** Si esas muertes
siguieran el mismo patrón que las atribuidas, `relh` subiría a ~45 %; si fueran
todas de otro, bajaría. **La regla de los 48 tics es la del paper cuatro y no la
he tocado, pero es un límite real.**

**No sé por qué `relh-zero-sum` no mata antes del tic 8.191.** Es un umbral muy
nítido para 156 casos. Podría ser que acumule equipo y salga a cazar, o que su
política tenga una fase. **No tengo su código y no lo voy a suponer.**

**Las cinco carpetas de P5-6B que faltan** podrían mover los totales unas pocas
muertes. Son diarios que no se conservaron, no datos que se perdieran hoy.

---

## Resumen en cinco líneas

**De nuestras 389 muertes en el mundo lento, 156 —el 40,1 %— las causó
`relh-zero-sum`, que además es quien más nos pegó (1.373 golpes, el 32,5 %) y
quien mejor remata (8,8 golpes por muerte).**

**Y `relh-zero-sum` es una de las tres políticas que metimos por triplicado
precisamente por considerarlas pacíficas: lo parecía porque el criterio miraba
antes del tic 2.000, y resulta que no mató ni una sola vez antes del tic 8.191
—mediana 8.723, justo después de que el anillo empiece a avisar.**

**Las otras dos que triplicamos sí eran pacíficas: `belobog` dio 69 golpes y cero
muertes, y `zero-sum-scavenger` 112 golpes y tres muertes; el error fue con una
de las tres.**

**El reparto es estable en las tres series grandes —`relh` entre el 33,8 % y el
39,3 %, `sivanlevy` entre el 17,9 % y el 20,8 %, el anillo entre el 13,3 % y el
18,2 %— y el roster es idéntico en los 200 episodios, así que no es un accidente
de una serie.**

**Esto no invalida los resultados, porque los dos brazos de cada semilla se
enfrentaron al mismo roster, pero sí la frase de que el mundo lento va «sin
cazadores»: lo que se quitó fueron los cazadores tempranos.**

---

**PARO AQUÍ.**
