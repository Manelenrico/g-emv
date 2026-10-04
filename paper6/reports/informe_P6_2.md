# P6-2 · Diagnóstico de la pareja antes de construir el seis

*Sólo lectura y análisis de los **20 diarios del grupo 2 de P6-1** (0.1.19,
`roster_lento_v2`, cuerpo solo en los asientos 10 y 11). **No se jugó ninguna
partida: coste de plataforma cero.** `motor/model.py` intacto
(md5 `1e511978c251130e95169ebf8443efa1`, comprobado). No se cambió código del
alma. Nada subido, empujado ni borrado. Todo en `cantera/paper6/`.*

Medido por `cantera/paper6/mide_P6_2.py` → `P6_2_bruto.json`, leído por
`analiza_P6_2.py`. El GIF, por `gif_P6_2.py`.

**Material:** 10 episodios · **119.830 tics con los dos vivos** · 16.494 tics
con uno solo · 5.343 partes emitidos · 94.129 decisiones con las piernas
listas.

---

## 1 · EL TELEGRAMA DE HOY

### Qué manda cada hermano

El canal de equipo lo usa `parte.py`, que emite desde `policy_cortex.decisor`
(línea 965) **cada `VOZ_CADA = 48` tics**. Formato v1, fijo:

```
E1 P<slot> t<tick> <x>,<y> h<hp> v<0|1> b<n> a<0|1>[ s<asiento>][ <ax>,<ay>]
```

Un ejemplo real, del diario del asiento 10 en el tic 481:
`E1 P10 t481 13,13 h100 v0 b0 a0`

| | medido sobre los 5.343 partes |
|---|---|
| mensajes por diario | mediana **283** |
| **cadencia** | **48 tics en 5.323 de 5.323 huecos** — sin una sola excepción |
| **longitud** | mínimo **30**, mediana **32**, máximo **43** caracteres |

Los 43 del máximo son los partes con agresor: añaden ` s<asiento>` y, si se le
ve, ` <ax>,<ay>`.

### Qué llega y de quién

| lo que entra por `chat` | n |
|---|---|
| `team` · del hermano · con marca `E1` | **4.998** |
| `team` · eco del propio parte | 5.343 |
| `broadcast` · de terceros · texto libre | 774 |
| `dm` · de terceros | 80 |
| `team` de un tercero | **0** |

**El canal de equipo sigue siendo cerrado de fábrica**, como selló el PROMPT_52:
ni un solo mensaje de equipo ajeno en 119.830 tics. Los 4.998 contra 5.343 son
los partes emitidos después de que el hermano ya hubiera muerto. La latencia es
de **+2 tics** (se emite en el 529 y se lee en el 531), la que ya estaba medida.

### Qué hace el que lo recibe

> **⚠ CORRECCIÓN [P6-3, 26-sep]. Lo que esta sección decía antes era falso y lo
> dejo dicho con todas las letras.** Escribí que «de los siete campos del parte
> el oyente lee dos» y que «`v` veneno, `b` botiquines y `a`/`s` agresor no los
> lee nadie». **Mentira, y por un fallo mío de método**: busqué las claves con
> los nombres abreviados (`["bot"]`, `["agr"]`, `["ven"]`) cuando el parser las
> devuelve como `botiquin`, `agresor`, `agresor_slot`, `agresor_pos` y `veneno`.
> Con los nombres buenos, **todos los campos menos uno se leen**. También dije
> que `S-HERIDO`, `S-PROVISION` y `S-SOLEDAD` «no aparecen ni un tic»: eso salió
> de censar **un** diario y generalizarlo a veinte. Abajo va lo cierto, medido
> sobre los veinte.

Del parte se leen **seis de los siete campos**:

| campo | ¿se lee? | por dónde entra | qué fila alimenta |
|---|---|---|---|
| `hp` | **sí** | `Memoria.pareja_hp_est` | `S-DANO-PAREJA`, `S-HERIDO` |
| `pos` | **sí** | `_ppos54` | `S-HERIDO` (posición del herido) |
| `b` botiquines | **sí** | `_hermana_b0` (`:781-785`) | `S-PROVISION`, `R-HERMANO-FALTA` |
| `a` agresor | **sí** | `agresor_de_la_hermana` (`:787`), `_provision_calma` | `F-HERMANO-GOLPE`, `S-HERIDO`, `F-REENCUENTRO`, y la calma de `S-PROVISION` |
| `s` asiento del agresor | **sí** | la rama `IDENTIDAD_ON` (`:806-814`) | la certificación del agresor |
| `ax,ay` posición del agresor | **sí** | el respaldo por posición (`:816-831`) | la misma |
| **`v` veneno** | **NO** | sólo se copia al diario en `F["_parte"]` (`:1370`) | **ninguna** |

Y las filas que de verdad viven en estos veinte diarios (256.154 tics con tabla):

| fila | tics | % | diarios |
|---|---:|---:|---:|
| `R-LLAMADA` | 256.154 | 100,00 | 20/20 |
| `R-CARENCIA` | 243.725 | 95,15 | 20/20 |
| `F-4-ALCANCE` | 216.485 | 84,51 | 20/20 |
| `R-ACOPIO` | 180.912 | 70,63 | 20/20 |
| `S-8-EXPOSICION` | 156.634 | 61,15 | 20/20 |
| `F-DANO` | 78.751 | 30,74 | 20/20 |
| `S-DANO-PAREJA` | 72.097 | 28,15 | 20/20 |
| `F-HERMANO-AMENAZA` | 55.483 | 21,66 | 20/20 |
| **`S-PROVISION`** | **48.164** | **18,80** | 14/20 |
| `S-SOLEDAD` | 16.494 | 6,44 | 10/20 |
| `S-MUERTE-PAREJA` | 16.494 | 6,44 | 10/20 |
| `F-ANTICIPACION` | 14.549 | 5,68 | 19/20 |
| **`S-HERIDO`** | **6.956** | **2,72** | 14/20 |
| `S-7-AGRESOR` | 5.846 | 2,28 | 20/20 |
| **`R-HERMANO-FALTA`** | **3.667** | **1,43** | 12/20 |
| `F-REENCUENTRO` | 2.326 | 0,91 | 18/20 |
| `F-HERMANO-GOLPE` | 2.294 | 0,90 | 14/20 |

Nunca aparecen: `S-VINCULO`, `S-COMPANIA`, `S-VIDA-AJENA`, `MIEDO_APRENDIDO`.

**Lo que sí es cierto, y es el hallazgo que importa: todas las vías por las que
el parte podría avisar de un peligro están cerradas con la misma llave — el
oyente tiene que VER ya la cosa.**

* `agresor_de_la_hermana` (`:806-814`): con el asiento certificado, recorre los
  **agentes visibles** y si ese asiento no está entre ellos devuelve `None`. El
  comentario del propio código lo dice: *«el nombre llega, pero no lo veo»*.
* Sin asiento, el respaldo por posición (`:816-831`) recorre otra vez **los
  agentes visibles** y busca uno a `MANADA_TOL = 1` de la posición declarada.
* `F-HERMANO-AMENAZA` itera sobre **los agentes visibles** y exige que el rival
  esté en alcance del hermano: si no lo veo yo, no hay fila.

**Por eso el parte no sirve de nada en los 488 episodios de amenaza a ciegas:
son, por definición, los tics en que el rival NO es visible para el que debería
preocuparse.** El canal lleva el nombre del agresor y hasta su posición, y el
oyente los descarta porque no puede confirmarlos con sus propios ojos.

### ¿Cambia alguna decisión? — el contrafáctico

No basta con mirar la fila: hay que rehacer la elección. Para cada tic con
piernas listas y detalle por candidato (se guarda **cada 24 tics**,
`DETALLE_CANDIDATOS_CADA`), sustituí `S-DANO-PAREJA` por **la que habría salido
sin parte** —la banda recordada, `BANDA_EST`— y recalculé la `d` de todos los
candidatos con el álgebra del motor.

*(Control: reconstruir la `d` desde las filas reproduce `d_ahora` del diario con
una desviación máxima de 1,5·10⁻⁵ en 3.000 tics, que es el redondeo del propio
log.)*

| | n |
|---|---|
| tics con detalle y piernas listas | 3.900 |
| …con parte fresco | **3.537** |
| …sin parte fresco | 363 |
| **el parte NO cambia el candidato elegido** | **3.478** |
| **EL PARTE CAMBIA EL CANDIDATO ELEGIDO** | **59 = 1,67 %** |

Los 59 cambios son **todos** con el hermano en banda `healthy`: la banda habría
dicho 83 de vida y el parte dice 100, y eso quita
`M = (100−83)/100 × B = 0,17` de `S-DANO-PAREJA`. La diferencia mediana entre
«con parte» y «sin parte» es exactamente **−0,17**, en 2.814 de los 3.537 tics.
Cincuenta de los 59 cambios son el mismo giro: `move_SE` → `move_SW`.

**Lectura honesta, y con su límite declarado:** este contrafáctico mueve **sólo
`S-DANO-PAREJA`**. El parte alimenta además `S-HERIDO`, `S-PROVISION`,
`R-HERMANO-FALTA`, `F-HERMANO-GOLPE` y `F-REENCUENTRO`, así que **el 1,67 % es
una COTA INFERIOR del efecto del parte, no su efecto**. Lo que sí queda medido
es que la corrección de vida —17 puntos de banda a exacto— por sí sola cambia
una de cada sesenta decisiones.

*(Aviso de alcance: el 1,67 % se mide sobre los tics con detalle, que son 1 de
cada 24. No tengo forma de saber si los otros 23 se comportan igual; el muestreo
es del diario, no mío.)*

### Cuánto del canal queda libre

| | |
|---|---|
| lo que manda un hermano | 32 caracteres cada 48 tics = **0,667 car/tic** |
| lo que el canal permite | 120 caracteres cada 24 tics (1/s) = **5,0 car/tic** |
| **uso** | **13,3 %** |
| **libre** | **86,7 %** |
| por longitud de mensaje | 32 de 120 = **26,7 %** |
| por ritmo | 1 cada 48 contra 1 cada 24 = **50 %** |

**Queda libre el 86,7 % del canal.** Podríamos mandar **7,5 veces** lo que
mandamos hoy sin rozar el límite.

---

## 2 · LO QUE VE UNO Y NO EL OTRO

### 2a · La distancia entre hermanos

119.830 tics con los dos vivos, distancia de rey:

| | |
|---|---|
| **mediana** | **2** |
| media | 2,2 |
| deciles (1.º…9.º) | 1, 1, 1, 1, **2**, 2, 3, 3, 4 |
| a 0-4 casillas | **109.966 = 91,8 %** |
| a 5-9 | 9.741 = 8,1 % |
| a 10 o más | **123 = 0,1 %** |

**Van pegados.** Nueve de cada diez instantes de sus vidas los pasan a cuatro
casillas o menos uno del otro.

### 2b · Y aun así, cada uno ve cosas que el otro no

Casillas = las que están en línea de vista desde su posición (`Ojo.vistas_desde`,
el mismo cálculo del paper cinco).

| lo que ve uno y el otro no | mediana | media | tics en que es > 0 |
|---|---:|---:|---:|
| **casillas** exclusivas del 10 | **21,1 %** | 28,0 % | 87,5 % |
| **casillas** exclusivas del 11 | **25,5 %** | 29,0 % | — |
| **objetos** exclusivos del 10 | 0 % | 17,2 % | **31,3 %** |
| **objetos** exclusivos del 11 | 0 % | 23,7 % | **49,8 %** |
| **rivales** exclusivos del 10 | 0 % | 31,5 % | **47,2 %** |
| **rivales** exclusivos del 11 | 33,3 % | 40,2 % | **58,6 %** |

*(Tamaños: cada uno ve de media 5,5 y 5,9 objetos, y 1,8 y 2,0 rivales.)*

**A dos casillas de distancia, la cuarta parte de lo que ve cada uno es
información que el otro no tiene.** Y en el 17,9 % de los tics, más de la mitad
de lo que ve el 10 es exclusivo suyo. La pareja está pegada y aun así **no
comparte la mirada**.

### 2c · El objeto que uno ve y al otro le falta

Definición usada, para que se pueda discutir: el objeto está en `ve_items` de
uno y **no** en el del otro; es de clase útil (arma, botiquín, raciones,
mochila, munición); el que no lo ve **no lo lleva** (mano vacía / pack sin
botiquín / pack sin raciones / cuerpo sin mochila); y su `R-CARENCIA` está
encendida. Todo leído del diario, sin estimar nada.

| | n |
|---|---|
| **tics** con al menos un caso | **57.124** |
| **ocasiones** (mismo objeto, mismo necesitado, tics contiguos) | **1.954** |
| episodios con alguna | **10 de 10** |

| clase | tics | ocasiones | distancia mediana al que lo necesita |
|---|---:|---:|---:|
| **raciones** (`rations`) | 34.784 | **842** | |
| **arma** (sword 6.564 · blowgun 2.053 · bow 1.060 · spear 985) | 10.662 | **726** | |
| **botiquín** (`first_aid`) | 10.262 | **287** | |
| **mochila** (`backpack`) | 1.416 | 99 | |
| **todas** | **57.124** | **1.954** | **6** (tic a tic, mediana 8) |

Duración de la ocasión: mediana **11 tics**, máximo **6.996**. Las más largas:

| episodio | a quién le falta | qué | tics | distancia |
|---|---|---|---|---|
| `P61_t3_G2_20365645` | 11 | raciones | 2.264 → 9.259 | 9 |
| `P61_t4_G2_20994019` | 10 | raciones | 2.281 → 8.085 | 5 |
| `P61_t3_G2_20575103` | 10 | raciones | 2.738 → 7.896 | 9 |
| `P61_t3_G2_20575103` | 10 | botiquín | 4.777 → 7.896 | 8 |

**Hay una partida en la que el hermano 10 pasa 5.600 tics sin raciones, con su
hermano mirando unas a cinco casillas, y ni se entera.** El canal que podría
decírselo va al 13 % de su capacidad.

### 2d · El armado que uno ve, el otro no, y lo tiene a tiro

Definición: rival en `ve_agentes` de uno y no del otro; con arma de alcance
`rg > 0` en la mano; y el hermano que no lo ve a distancia de rey **≤ rg**.

| | n |
|---|---|
| **tics** en esa situación | **4.775** |
| **episodios de amenaza ciega** (mismo rival, mismo amenazado, contiguos) | **488** |
| partidas con alguno | **10 de 10** |
| duración mediana del episodio | **9 tics** |
| distancia mediana del armado al amenazado | **5** |
| distancia mediana entre hermanos en esos tics | **3** |

| arma del que no se ve | tics |
|---|---:|
| `knives` | 2.566 |
| `bow` | 1.341 |
| `spear` | 440 |
| `blowgun` | 317 |
| `net` | 111 |

Los más largos: 546 tics (`21203477`, rival 7 con cuchillos, el 10 a tiro),
112 (`20784561`, rival 2), 92 (`20260916`, rival 2 con arco).

**Cuatro mil setecientos setenta y cinco instantes en que un hermano ve a
alguien que puede pegarle al otro, y el otro no lo sabe.** El parte tiene un
campo de agresor —`a`, `s`, y hasta su posición— y **el oyente no lo lee**.

### Quién muere primero, y dónde estaba el otro

| | |
|---|---|
| muere primero el **10** | 7 de 10 |
| muere primero el **11** | 3 de 10 |
| **causa del primero** | **el anillo 7** · un rival 2 (`P14`, `P1`) · veneno 1 |
| el segundo **aguanta después** | mediana **917 tics (38 s)**; de 85 a 8.857 |
| **distancia entre hermanos en el instante de la primera muerte** | 1, 1, 1, 2, 2, 3, 3, 3, 3, 9 · **mediana 2,5** |

| episodio | muere | tic | por | dónde | el hermano estaba en | d | aguanta |
|---|---|---:|---|---|---|---:|---:|
| `20260916` | 10 | 13.030 | anillo | (22,22) | (22,25) | 3 | 1.011 |
| `20365645` | 11 | 12.961 | anillo | (30,21) | (21,21) | **9** | 1.656 |
| `20470374` | 10 | 12.985 | anillo | (21,17) | (23,20) | 3 | 1.717 |
| `20575103` | 11 | 10.892 | **P14** | (20,19) | (19,17) | 2 | 85 |
| `20679832` | 10 | 13.009 | anillo | (23,19) | (24,21) | 2 | 1.680 |
| `20784561` | 10 | 14.305 | anillo | (21,26) | (24,24) | 3 | 408 |
| `20889290` | 10 | 12.985 | anillo | (22,19) | (19,20) | 3 | 823 |
| `20994019` | 10 | 14.521 | anillo | (21,24) | (21,23) | **1** | 96 |
| `21098748` | 10 | 14.768 | veneno | (23,23) | (24,24) | **1** | 161 |
| `21203477` | 11 | 5.184 | **P1** | (22,25) | (23,26) | **1** | 8.857 |

**Siete de las diez veces, al primero lo mata el anillo con el hermano a tres
casillas o menos.** Los dos están dentro del mismo fuego; uno cae antes que el
otro por unos cuantos puntos de vida. La única muerte lejos del hermano es la
de `20365645`, a nueve casillas.

---

## 3 · LO QUE EL CUERPO NO SABE DE LO QUE VA A PASAR

Para cada decisión con las piernas listas: la `d` que el cuerpo **proyectó** para
el candidato que eligió, contra la `d` que **tuvo de verdad** en la siguiente
decisión con las piernas listas. Discrepancia = real − proyectado (positivo = le
fue peor de lo que creía).

| | 94.129 decisiones |
|---|---|
| discrepancia mediana | **+0,00193** |
| media | +0,06658 |
| **|discrepancia| mediana** | **0,00702** |
| hueco entre decisiones | mediana **1** tic |
| se equivoca **a favor** (la realidad sale mejor) | **9,7 %** |

| tamaño de la discrepancia | n | % |
|---|---:|---:|
| exacta (< 10⁻⁴) | 37.129 | **39,4 %** |
| pequeña (< 0,01) | 10.678 | 11,3 % |
| media (< 0,1) | 14.574 | 15,5 % |
| **grande (< 0,5)** | **30.439** | **32,3 %** |
| enorme (≥ 0,5) | 1.309 | 1,4 % |

Y por candidato elegido, que es donde se ve de qué va esto:

| candidato | n | \|disc\| mediana |
|---|---:|---:|
| `noop` | 43.137 | **0,0000** |
| `move_S` | 2.506 | 0,0175 |
| `move_SE` | 12.202 | 0,0956 |
| `move_SW` | 6.831 | 0,1147 |
| `coger` | 3.255 | 0,1316 |
| `soltar_rations` | 2.336 | 0,1891 |
| `move_NE` | 7.197 | 0,1893 |
| **`ir_objeto`** | 3.861 | **0,3011** |

**Cuando no se mueve, acierta exactamente. Cuando se mueve, se equivoca, y
cuanto más lejos apunta, más.** Las cinco peores son todas `ir_objeto`,
`ir_botin` o pasos largos en el tramo final de la partida, con discrepancias de
+2,1 a +2,9.

### El reparto por dimensiones

Sólo se puede hacer sobre los tics con detalle por filas (uno de cada 24):
**3.896 decisiones, 2.595 con discrepancia no nula.** El método: para cada
familia se rehace la `d` moviendo **sólo** las filas de esa familia de lo
proyectado a lo real, y se mide cuánto se mueve la `d`. Como `d` es no lineal,
los tres aportes no suman exactamente el hueco: por eso doy el reparto en
**valor absoluto**.

Doy las dos agrupaciones posibles, porque no son iguales y conviene verlo:

**(i) por el prefijo del nombre** (la taxonomía de la casa: `F-` cuerpo,
`R-` recursos, `S-` vínculos)

| dimensión | aporte neto | \|aporte\| | **% de lo no previsto** |
|---|---:|---:|---:|
| cuerpo | +62,30 | 110,01 | 22,6 % |
| recursos | −17,17 | 138,75 | 28,5 % |
| **vínculos** | **+227,59** | **237,48** | **48,8 %** |

**(ii) por de qué habla la fila** (las del hermano van a vínculos aunque se
llamen `F-`, como pide el encargo: «vínculos (los otros, incluido el hermano)»)

| dimensión | aporte neto | \|aporte\| | **% de lo no previsto** |
|---|---:|---:|---:|
| cuerpo | +60,04 | 107,00 | 22,0 % |
| recursos | −18,26 | 137,41 | 28,2 % |
| **vínculos** | **+231,08** | **242,47** | **49,8 %** |

**Las dos dicen lo mismo: los vínculos —los otros— explican la mitad de lo que
el cuerpo no supo prever**, y además con el **signo peor**: el aporte neto de
vínculos es **+228**, es decir, lo que no ve venir de los otros casi siempre le
sale **en contra**. Recursos tiene aporte neto **negativo** (−17): en materia de
comida y armas, el mundo le sale ligeramente **mejor** de lo que teme.

Fila a fila, la suma de \|ΔM\|:

| fila | \|ΔM\| total | aparece sin avisar | desaparece |
|---|---:|---:|---:|
| **`S-8-EXPOSICION`** | **273,85** | **959** | 19 |
| `R-LLAMADA` | 133,39 | 253 | 0 |
| `F-4-ALCANCE` | 131,54 | 80 | 63 |
| `R-CARENCIA` | 53,88 | 24 | 0 |
| `S-PROVISION` | 52,73 | 12 | 7 |
| `F-ANTICIPACION` | 13,47 | 23 | **140** |
| `S-HERIDO` | 11,39 | 2 | 1 |
| `S-7-AGRESOR` | 11,01 | 28 | 3 |
| `S-DANO-PAREJA` | 10,67 | 3 | 2 |

**La fila que más se mueve, con diferencia, es `S-8-EXPOSICION`: «cuántos me
están viendo».** En 959 de las 2.595 decisiones **aparece de la nada**: el
cuerpo proyecta que no le verá nadie y al instante siguiente le ven. Es el mismo
mecanismo que P6-FIG2 encontró en la figura 1 —una fila de rivales que entra y
sale de la tabla porque alguien cruza el borde de la vista—, pero aquí medido
sobre 2.595 decisiones y como **la primera causa de que el plan de un paso no se
cumpla**.

**Y es exactamente la información que su hermano sí tiene y no le manda.**

---

## 4 · EL GIF

`cantera/paper6/P6_2_pareja.gif` — 121 fotogramas, 10 por segundo, uno cada 12
tics. Hecho con matplotlib sobre los datos crudos de los dos diarios
(`gif_P6_2.py`). **No se usó MettaScope.**

**Episodio y tramo: `P61_t3_G2_20260916`, instantes 11.521 → 12.961** (60 s de
partida exactos, 1.440 tics).

### Por qué ese tramo y no otro

Busqué, sobre las diez partidas, la ventana de 1.440 tics con más casos de 2d
—que es el hallazgo que quería que se viera moverse— y ésta gana con holgura:

| episodio | mejor ventana | tics de 2d | tics de 2c |
|---|---|---:|---:|
| **`20260916`** | **11.521** | **714** | **1.241** |
| `20784561` | 8.041 | 585 | 42 |
| `21203477` | 3.373 | 559 | 12 |
| `20365645` | 9.241 | 552 | 285 |

Es la única que junta **mucho de 2d y mucho de 2c a la vez**. En la ventana
final hay **822 tics de 2d** y **3.089 de 2c**. Además los dos hermanos están
vivos todo el tramo (el 10 muere en el 13.030, 69 tics después del final), y el
anillo se cierra de r=8 a r=5 durante el tramo, así que se ve el apretujón que
mata a siete de nuestros diez cuerpos.

Lo que se ve concretamente:

* el **rival 2 con arco** (alcance 8) al que **sólo ve el 11** durante 642 tics,
  con el 10 dentro de su alcance — círculo rosa y línea de puntos al amenazado;
* el **rival 14 con lanza** (108 tics) y el **9 con arco** (72), igual;
* **botiquín** y **raciones** que sólo ve uno y al otro le faltan — círculo del
  color de quien lo ve, sobre el rombo;
* las dos manchas de visión, azul (sólo el 10) y naranja (sólo el 11), con la
  franja verde de lo compartido: **se ve a simple vista que las dos manchas no
  coinciden aunque los cuerpos se toquen.**

---

## LO QUE NO SE PUEDE MEDIR CON EL DIARIO, Y NO ESTIMO

1. **Qué pasa en los 23 de cada 24 tics sin detalle por candidato.** El
   contrafáctico del parte (1,67 %) y el reparto por dimensiones (48,8 % /
   49,8 % vínculos) salen de los tics múltiplos de 24. Es un muestreo del
   diario, no mío, y no tengo forma de comprobar que los otros se comporten
   igual.
2. **Qué ve un rival.** Todo el 2b, 2c y 2d es «lo que ve el hermano A y no el
   hermano B», nunca «lo que sabe el rival».
3. **Si el hermano habría actuado distinto con la información que le falta.**
   Medir eso pide rejugar con otro canal, y eso es jugar. Aquí sólo está la
   ocasión, no el contrafáctico de la conducta.
4. **Las muertes ajenas y quién las causó**, como ya se dijo en P6-0.

---

## LAS CUATRO COSAS QUE ME LLEVO PARA CONSTRUIR EL SEIS

1. **El canal está vacío al 86,7 %, y lo que lleva sólo sirve si ya lo estás
   viendo.** Seis de los siete campos se leen (sólo `veneno` no), pero las tres
   vías del agresor y la de la amenaza al hermano **exigen que el oyente vea al
   rival**: justo lo que no pasa en los 488 episodios de amenaza a ciegas.
2. **La pareja va pegada (mediana 2) y aun así no comparte la mirada**: la
   cuarta parte de lo que ve cada uno es exclusivo suyo, y en el 47-59 % de los
   tics uno ve un rival que el otro no.
3. **Hay 4.775 instantes de amenaza ciega y 1.954 ocasiones de objeto
   desaprovechado.** No es un caso raro: pasa en las diez partidas.
4. **La mitad de lo que el cuerpo no prevé viene de los otros, y le sale en
   contra**, y la fila que más se le escapa —`S-8-EXPOSICION`, «me están
   viendo»— es justo la que su hermano sabe y no le dice.

**El seis tiene sitio de sobra en el canal y una lista clara de qué falta
decir.** Qué se diga y cómo es decisión de Manel: aquí sólo está el diagnóstico.
