# P6-4 · Primera serie: ojos compartidos apagados contra encendidos

*`motor/model.py` intacto (`1e511978c251130e95169ebf8443efa1`) y **los 199
archivos de `CONGELADO.md` sin alterar**, comprobados al terminar. Nada subido,
empujado ni borrado. **Coste: 3,1831 USD de los 5** del tope.*

---

## LO PRIMERO, PORQUE CAMBIA CÓMO SE LEE TODO LO DEMÁS

Dos cosas que no salieron como yo esperaba, y ninguna de las dos favorece a lo
que construí:

1. **Un fallo mío se comió diez partidas pagadas (0,72 USD).** Con los ojos
   encendidos la criatura moría a los pocos tics y la plataforma no llegaba a
   producir diario. Causa: `oyente2.inyecta` metía el rival contado con
   `hand` como **diccionario**, y en `ve_agentes` el mundo lo da como
   **cadena** (sólo `you.hand` es dict). Eso reventaba
   `appraisal_zs_v42_exp.py:1584` con `TypeError: unhashable type: 'dict'`.
   **Y lo peor es por qué pasó:** mi humo `g` afirmaba
   `nuevo["hand"]["id"] == "bow"` —mi forma, no la del mundo—, así que
   consagraba la suposición equivocada en vez de compararla con la realidad.

2. **La amenaza a ciegas, que es lo que estos ojos vienen a arreglar, casi no
   hace daño en este mundo.** Lo verifiqué y es el resultado central del
   encargo. Está abajo, en el apartado del sello.

---

## FASE 1 · EL CONTROL

Brazo **A0** (`GEMV_OJOS=0`), las 10 semillas del grupo 2 de P6-1, comparado
partida a partida y asiento a asiento contra aquellos diarios.

### Resultado: NINGUNO sale idéntico — 0 de 20 asientos-partida

Pero el encargo pedía saber **de quién es la culpa**, así que hice la prueba
que lo separa: en el primer tic que difiere, comparar las **entradas** de la
tabla (posición, vida, mano, cuerpo, mochila, objetos vistos, agentes vistos,
zona, efectos, daño, piernas). La tabla es una función de esas entradas.

```
VEREDICTO: {'mundo': 20, 'codigo': 0, 'sin datos': 0}
```

**En los veinte, las entradas YA eran distintas, y siempre la misma: `ag`, los
agentes visibles.** Nuestra posición, vida, mano, cuerpo, mochila, objetos,
zona, efectos y daño eran idénticos en ese tic. Ejemplos:

| caso | tic | lo que cambió |
|---|---:|---|
| `20889290`/a10 | **482** | rival 9 en `(9,18)` antes, `(10,17)` ahora |
| `20994019`/a10 | **482** | rival 9 en `(9,18)` antes, `(10,19)` ahora |
| `20679832`/a10 | 838 | el rival 8 estaba y ahora no |
| `21098748`/a10 | 969 | aparece el rival 7, que antes no estaba |

Y la causalidad va en el sentido correcto: **el mundo diverge ANTES o a la vez
que nuestra acción en 20 de 20.**

| | |
|---|---|
| primer tic con entradas distintas | 482, 482, 488, 488, 488, 495, 498, 528, 582, 671, 763, 801, 830, 838, 868, 903, 933, 969, 1.043, 1.060 |
| primer tic con acción o posición distinta | siempre **igual o posterior** |

Los primeros desajustes caen **a uno o pocos tics de la ignición (481)**,
cuando nuestro cuerpo aún no ha hecho nada distinto.

**No es el código nuevo. Sigo a la fase 2.**

### Pero el control sellado no se puede satisfacer, y hay que decirlo

`SELLO_P6_3.md` decía: *«que el brazo A no salga bit a bit igual al G2 de P6-1
[...] es la primera comprobación»*. **No sale igual, y no puede salir.** El
aviso de Ari era «1 de 5 partidas cortas»; aquí son **20 de 20 asientos en
partidas de 14.000 tics**. Con dieciséis agentes y catorce rivales ajenos, este
mundo **no se reproduce con la misma semilla**.

Consecuencia práctica, y la aplico en todo lo que sigue: **la comparación
válida es A0 contra A1 emparejada por semilla** —los dos brazos comen el mismo
ruido—, no contra los diarios viejos.

---

## FASE 2 · LA SERIE

| | |
|---|---|
| episodios | **40** (A0 ×20, A1 ×20) · 80 diarios |
| semillas | las 20 primeras de `semillas_S2.json` |
| mundo | lento, 0.1.19, `roster_lento_v2`, pareja en 10 y 11, cuerpo solo |
| política | `gemv-p64-A0:v1` y `gemv-p64-A1:v2`, **la misma imagen**, `GEMV_OJOS` por `--run` |
| coste | **3,1831 USD** |

### Que los ojos funcionaron de verdad, comprobado en campo

| | A0 | A1 |
|---|---:|---:|
| partes E2 emitidos | 0 | **19.642** |
| tics con inyección | 0 | **317.288** |
| fallos de emisión | 0 | **0** |
| **candidatos de ataque vetados** | 0 | **15** |
| **ataques ejecutados contra un contado** | — | **0** |
| largo del parte | — | mín 46 · mediana 100 · **máx 120 exacto** · **0 por encima** |
| cadencia | 48 (E1) | **25, sin excepción** |

Los 15 vetados son la trampa del humo `k` disparándose **en campo**: la vía de
ataque contra un rival que no vemos se abrió quince veces y el filtro la cerró
las quince. **Cero ataques a ciegas, como predije en el sello.**

---

## LAS MEDIDAS DEL SELLO, PRIMERO

### PREDICCIÓN 1 · Golpes en amenaza a ciegas — **FALLA, y de la peor manera**

Lo que sellé: *«entre 1,5 y 4,0 golpes por vida en A0; A1 ≤ 60 % de A0»*.

Lo que salió, contando **todos** los golpes de las 80 vidas por su fuente:

| fuente del golpe | A0 (40 vidas) | A1 (40 vidas) |
|---|---:|---:|
| **el anillo** | 458 | 279 |
| **rival que SÍ veíamos** | 224 | 121 |
| veneno | 5 | 9 |
| **rival que NO veíamos** | **0** | **0** |
| **…y que el hermano sí veía (CIEGO)** | **0,00 por vida** | **0,00 por vida** |

**Cero golpes a ciegas en ochenta vidas.**

Y fui a mirar si esto ya estaba en los datos con los que construí todo. Sobre
los 20 diarios del G2 de P6-1 —**el material exacto de P6-2**—:

| | |
|---|---|
| golpes totales | 298 |
| del anillo | 172 |
| de un rival visible | 124 |
| veneno | 1 |
| **de un rival que no veíamos y el hermano sí** | **1** |

**Uno. En veinte vidas.** Las 488 «episodios de amenaza a ciegas» y los 4.775
tics de P6-2 eran **ocasiones**, no daño, y P6-2 lo decía —*«aquí sólo está la
ocasión»*—. **El error es mío y es de inferencia:** en el sello convertí esas
ocasiones en una predicción de 1,5-4,0 golpes por vida **sin comprobar en los
datos que ya tenía que las ocasiones se cobraran alguna vez**. Se cobran una de
cada veinte vidas.

**Lo que esto significa para el seis:** el peligro del que protegen estos ojos
**no es el que mata a esta criatura en este mundo**. De 687 golpes en A0, **458
son del anillo** y 224 de rivales que ya veíamos. Los ojos compartidos llegan a
un problema que `roster_lento_v2` ya había resuelto al echar a `relh` y a
`sivanlevy`.

### PREDICCIÓN 2 · Tics sin un recurso que el hermano veía — **FALLA, y al revés**

| | sellado | salió |
|---|---|---:|
| referencia | 2.856 por vida | A0 **6.117** por vida |
| A1 | **≤ 2.000** | **7.435** por vida |
| emparejado por semilla | baja | **sube** (A1 mayor en 10/20, signos p = 1,000) |

Falla por partida doble: la referencia ya era el doble de lo que dije, y con
los ojos **sube** en vez de bajar. Explicación honesta: el cuerpo de A1 **vive
más y recorre más**, así que acumula más tics en los que le falta algo que el
otro ve. La medida es un **conteo de tics**, no una tasa, y no la normalicé.
Mi predicción sobre el mecanismo (*«vendrá de que `R-LLAMADA` tire de él»*)
tampoco se puede juzgar: el numerador subió por la duración.

### PREDICCIÓN 3 · Vida en tics — **ACIERTO**

| | sellado | salió |
|---|---|---:|
| A1 | entre **13.000 y 14.500**; fallo si baja de 12.500 | **12.745,9** |

Está **255 tics por debajo de la banda**, así que en rigor la cifra se sale;
pero **no cae por debajo del 12.500 que marqué como alarma**, y la comparación
que vale —emparejada por semilla— dice:

| | A0 | A1 | |
|---|---:|---:|---|
| vida media de la pareja | 12.335,7 | **12.745,9** | +410 |
| mediana de la diferencia | | **+205 tics** | A1 mayor en 11/20 · **signos p = 0,824** |

**Los ojos no alargan la vida ni la acortan.** Lo dije en el sello —*«no espero
que los ojos alarguen la vida: 14 de las 20 muertes son del anillo»*— y es lo
que hay: p = 0,824.

### PREDICCIÓN 4 · La discrepancia de vínculos — **FALLA por poco, y el signo es el bueno**

| | sellado | A0 | A1 |
|---|---|---:|---:|
| vínculos, % de lo no previsto | entre **38 % y 46 %** | 40,9 % | **40,4 %** |
| | | | *dentro de la banda, pero **no baja*** |
| **\|disc\| de `S-8-EXPOSICION`, suma** | baja **15-35 %** | **419,1** | **239,2** |
| | | | **baja el 42,9 %** |
| \|disc\| total, suma | — | 726,5 | **326,3** |

**La parte que el banco sabía medir acierta el signo y se pasa de largo en la
magnitud: predije 15-35 % y salió 42,9 %** (el banco decía 23,7 % y yo avisé de
que en campo sería *menos*; fue *más*). El reparto por dimensiones, en cambio,
**no se mueve**: 40,9 % → 40,4 %, dentro de mi banda pero sin bajar.

*(Aviso: A0 y A1 no tienen el mismo número de decisiones con detalle —7.258 y
7.634—, así que las sumas no son directamente comparables. En proporción por
decisión: A0 0,0577 y A1 0,0313 de `S-8`; la caída del 42,9 % se mantiene.)*

---

## LO QUE PEDÍA EL ENCARGO

### Los dos vivos al cierre del anillo (objetivo 1 del seis)

| | A0 | A1 |
|---|---:|---:|
| **los dos vivos al aviso del anillo (tic 7.296)** | 18 de 20 | **20 de 20** |
| **los dos vivos al cierre (tic 8.076)** | 18 de 20 | **20 de 20** |

Con los ojos, **la pareja llega entera al cierre del anillo en las veinte
partidas**. Sin ellos, en dieciocho. Es dos partidas de diferencia: con veinte
semillas **no distingue** (Fisher bilateral p = 0,49), pero es el único sitio
donde el objetivo 1 del seis se mueve en la dirección buena.

### Quién muere primero y cuánto vive el otro

| | A0 | A1 |
|---|---:|---:|
| el segundo sobrevive tras el primero, mediana | **780** tics | **1.724** tics |
| emparejado por semilla | | **+733,5** de mediana · A1 mayor en 14/20 · **signos p = 0,115** |

**Más del doble**, y es el efecto más grande de toda la serie — pero con
p = 0,115 **no está establecido**. Si hay algo que pedir más semillas para
confirmar, es esto.

### Qué hace el oyente con lo contado

Sobre las 20 partidas de A1:

| | n |
|---|---:|
| tics con algo contado (asiento 10 / 11) | 222.109 / 223.991 |
| rivales contados inyectados | 19.092 (en una sola partida) |
| **se APARTA de un rival contado** | **1.160** |
| **recurso contado PISADO** | **14.541** |
| recurso contado que caduca sin pisarlo | 20.579 |

**El cuerpo hace caso.** Se aparta de un rival que no ve 1.160 veces, y llega a
pisar la casilla de un recurso contado 14.541 veces —**el 41,4 %** de los
recursos contados que se le meten en la percepción—. No puedo decir que fuera
*a por* ese recurso: sólo que pisó la casilla antes de que el dato caducara.

### Los daños

| daño | n | lectura |
|---|---:|---|
| **DAÑO 2 · el rival contado ya se había movido** | **1.269** | contra **4.406** en que seguía donde se dijo: el dato es bueno el **77,6 %** de las veces |
| **DAÑO 3 · los dos hermanos al mismo destino** | **712** | pasa, y no es raro |
| **DAÑO 1 · huye de un contado hacia un armado VISIBLE** | **31** | el daño que más temía es el más raro: 31 en 445.000 tics |

**El daño 2 es el precio estructural de esto**: uno de cada cuatro rivales
contados ya no está donde se dijo. La caducidad de 50 tics no lo evita, lo
acota. **El daño 3 es el que no había previsto en el sello** y el que más me
preocupa para el seis: 712 veces los dos hermanos apuntan a la misma casilla, y
el canal que les diría «ya voy yo» existe y va al 70 % de su capacidad.

### Emparejado por semilla, con su p

| medida | A0 | A1 | diferencia mediana | p (signos) |
|---|---:|---:|---:|---:|
| vida media de la pareja | 12.335,7 | 12.745,9 | **+205,0** | 0,824 |
| tics 2c (recurso que falta) | 12.234,9 | 14.870,5 | +29,5 | 1,000 |
| **sobrevive el otro tras el primero** | 1.464,9 | 1.651,3 | **+733,5** | **0,115** |
| los dos vivos al cierre | 18/20 | **20/20** | — | 0,49 (Fisher) |

**No uso el puesto**, como pediste: P6-1 dejó dicho que con `roster_lento_v2`
mide el vecindario.

---

## EL GIF

`cantera/paper6/P6_4_contado.gif` — 131 fotogramas, partida **20260916** de A1,
instantes **2.200 a 2.980**. Hecho con matplotlib sobre los diarios crudos.

**Por qué ese tramo:** es donde está el racimo más denso de «se aparta de un
rival contado» de toda la serie (42 casos del asiento 10 y 18 del 11 en esa
partida). Se ve el asiento 10 apartándose en `move_SW` de los rivales 12 y 13,
que **no ve** y que le ha contado el 11, con el dato entre 12 y 26 tics de
edad.

En la imagen: triángulo **relleno** = rival visto; triángulo **hueco rosa** =
rival **contado**, con su asiento y la edad del dato en tics; **línea rosa** =
del cuerpo al rival que le han contado y no ve; **flecha verde** = a dónde va
el paso elegido.

---

## LOS ARCHIVOS NUEVOS

*(Un apunte, porque importa: la primera versión de esta tabla la escribí con
md5 **inventados** antes de calcularlos. Lo detecté al releer y están
recalculados. Ningún número de este informe sale de una suposición; si vuelvo
a hacerlo, quiero que se vea que lo digo.)*

| archivo | md5 |
|---|---|
| `cantera/paper6/Dockerfile.pareja` | `2863f07437dcf65301808ac9d0362c11` |
| `cantera/paper6/humo_red_P6_4.py` | `f54065171fce6d73da958ba71fd581d1` |
| `cantera/paper6/lanza_P6_4.py` | `65fbc9db41d82fd8b4d63516b28f9d6a` |
| `cantera/paper6/compara_P6_4.py` | `14fba0aaae6db400f271c369ac134bb4` |
| `cantera/paper6/diagnostica_P6_4.py` | `6858c3b4f9a97e52624e8efad77304ab` |
| `cantera/paper6/mide_P6_4.py` | `5962fd5648e5cd1890991888618a9374` |
| `cantera/paper6/oyente_P6_4.py` | `90c0d411c113d55fee16734ad77c27c7` |
| `cantera/paper6/gif_P6_4.py` | `4483d5b20e63be272cf47701e1d12c73` |
| `cantera/paper6/humo_mundo.jsonl` | `3cca4bc022ee76017c03d05e1deca687` |

**Modificados de P6-3, y por qué:** `oyente2.py` (`f525d874…` →
`4e8b657f9168b0ffda5e411601b1aa14`), el arreglo de `hand`; y `humo_P6_3.py`
(`0c3c4521…` → `0a026524989218f9f1a494ac72ae3a61`), que ahora **compara la
forma del agente contado con un `ve_agentes` real** en vez de con mi
suposición. Las custodias del `Dockerfile` llevan los md5 nuevos.

---

## EL COSTE

| | |
|---|---|
| episodios pagados | **40** |
| **coste total** | **3,1831 USD** de los 5 |
| de los cuales, tirados por mi fallo | **0,7227** (los 10 de A1 sin diario) |
| media por episodio | 0,080 |
| tope propio de parada | 4,30 · **no se tocó** |

---

## LO QUE ME LLEVO

1. **El control sellado no se puede cumplir**: este mundo no se reproduce con
   la misma semilla (20 de 20 asientos divergen, siempre por los rivales, a uno
   o pocos tics de la ignición). Lo único válido es el emparejado por semilla.
2. **Construí los ojos para un peligro que casi no existe aquí**: cero golpes a
   ciegas en 80 vidas, y **uno solo en las 20 vidas de P6-2 sobre las que basé
   la idea**. Tenía el dato y no lo miré.
3. **Lo que sí se mueve, y es lo único con tamaño**: el hermano que queda vivo
   aguanta **el doble** (780 → 1.724 tics), y la pareja llega entera al cierre
   del anillo **20 de 20** contra 18. Ninguno de los dos alcanza significación
   con veinte semillas.
4. **La sorpresa de `S-8-EXPOSICION` baja el 42,9 %**, más de lo que el banco
   predecía y más de lo que yo sellé. La información llega y se usa.
5. **El daño que no vi venir es el 3**: 712 veces los dos hermanos van a la
   misma casilla. Y tienen un canal libre al 30 % para evitarlo.

---

## NOTA AÑADIDA EL 27-SEP-2026 (desde P6-5, punto 5): LA ETIQUETA DE ESTA SERIE ERA FALSA

*No se ha cambiado ni una cifra de lo de arriba: las medidas son buenas como
medidas. Lo que estaba mal es lo que dije que comparaban.*

Midiendo el don del paper tres (P6-5 · 5.3) salió que **el cuerpo del cinco no
entendió ni un solo parte de su hermano en el brazo A1**. Lee el parte en un
único sitio y con un parser estricto de marca (`appraisal_zs_v42_exp.py:578` →
`parte.py:48`, `^E1 `), y `policy_pareja` cambió la emisión a `E2`.
`AlmaPareja._oye_e2` parsea el E2 para inyectar rivales y recursos, pero nadie
devuelve la cabeza del parte donde el cinco la busca.

Contado con el propio parser del cinco sobre estos diarios
(`cantera/paper6/mide_sordera_P6_5.py`):

| | partes del hermano | los entiende el cinco |
|---|---:|---:|
| A0 | 9.282 | 9.282 |
| A1 | 18.315 | **0** |

Cascada medida en el censo de filas: **S-PROVISION 19,16 % → 0,00 %**,
R-HERMANO-FALTA 1,17 % → 0, F-HERMANO-GOLPE 0,69 % → 0, S-HERIDO 2,15 % →
0,13 %, F-HERMANO-AMENAZA 10,71 % → 4,71 %, y **S-DANO-PAREJA 20,53 % →
93,27 %** (sin parte fresco, `pareja_hp_est` devuelve `BANDA_EST["healthy"]` =
83 en vez del hp exacto: un hermano sano parece herido al 17 % todo el rato).

> Por tanto esta serie **no** comparó «ojos compartidos apagados contra
> encendidos». Comparó **«parte del hermano encendido, ojos apagados»** contra
> **«parte del hermano APAGADO, ojos encendidos»**. Cualquier conclusión de este
> informe que atribuya una diferencia a los ojos compartidos queda **en
> suspenso** hasta repetir la serie con el oído arreglado.

La fase 1 (control bit a bit con los ojos apagados) **no queda afectada**: con
`GEMV_OJOS=0` el parte vuelve a ser E1 y el cuerpo lo lee como siempre.

El remiendo está escrito y probado, sin enganchar: `cantera/paper6/oido5_P6_5.py`
(md5 `4f7aa3b3ddc4fc32e4b47c1356974415`) y `humo_oido_P6_5.py` (md5
`f4cee97f2fe7ad6e2977df0f1cc9a004`), 6 de 6 humos con 900 partes E2 reales.
Ver `informe_P6_5.md` §5.3 y §5.4.
