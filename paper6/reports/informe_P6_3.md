# P6-3 · Ojos compartidos, versión 1 — construcción y banco

*Sin jugar ni una partida: **coste cero**. `motor/model.py` intacto
(md5 `1e511978c251130e95169ebf8443efa1`). **Ni un archivo del paper cinco
alterado**: comprobados los 199 de `CONGELADO.md` uno a uno, **0 cambiados**.
Todo lo nuevo vive en `cantera/paper6/`. Nada subido, empujado ni borrado.*

---

## ANTES DE NADA: UNA CORRECCIÓN A P6-2

Al empezar esto descubrí que **dos afirmaciones mías de P6-2 eran falsas**, y
están corregidas en `informe_P6_2.md` y en el acta:

1. Dije que «de los siete campos del parte el oyente lee dos» y que `v`, `b` y
   `a`/`s` «no los lee nadie». **Falso, por un fallo de método**: busqué las
   claves abreviadas (`["bot"]`, `["agr"]`) cuando el parser devuelve
   `botiquin`, `agresor`, `agresor_slot`, `agresor_pos`. **Se leen seis de los
   siete**; el único huérfano es `veneno`.
2. Dije que `S-HERIDO`, `S-PROVISION` y `S-SOLEDAD` «no aparecen ni un tic».
   **Falso**: censé un diario y lo generalicé a veinte. Sobre los 20,
   `S-PROVISION` sale en **48.164 tics (18,8 %)** y `S-HERIDO` en **6.956**.

**Y al corregirlo aparece el motivo de verdad de este encargo**, que es más
afilado que el error: los campos se leen, pero **todas las vías están cerradas
con la misma llave — el oyente tiene que VER ya la cosa**.
`agresor_de_la_hermana` (`appraisal_zs_v42_exp.py:806-831`) recorre los
**agentes visibles** y devuelve `None` si ese asiento no está entre ellos; el
comentario del propio código lo dice: *«el nombre llega, pero no lo veo»*.
`F-HERMANO-AMENAZA` itera también sobre los visibles.

**Por eso el parte de hoy no sirve en los 488 episodios de amenaza a ciegas:
son, por definición, los tics en que el rival no es visible para quien debería
preocuparse.** E2 no arregla que no se leyeran los campos: arregla que la
información llegue con **posición**, que es lo que abre esas puertas solas.

---

## 1 · EL MENSAJE · `parte2.py`

```
E2 P<slot> t<tick> <x>,<y> h<hp> v<0|1> b<n> a<0|1>[ s<sl>][ <ax>,<ay>]
   [ R<rival><rival>…][ I<recurso><recurso>…]
```

La cabeza es **la de E1 palabra por palabra**, con la marca cambiada.

| pieza | forma | cuesta |
|---|---|---|
| `<rival>` | `<slot>:<x>,<y><arma><rumbo>` | 8-11 car. |
| `<recurso>` | `<tipo><x>,<y>` | 4-6 car. |

* **`arma` y `tipo` son una letra del catálogo, LEÍDA de `mundo.items`
  ordenado** (`parte2.alfabeto`). Cablearlas está prohibido por CLAUDE.md y
  además se rompería al cambiar el mundo. Humo `j` lo comprueba.
* **`rumbo`**: `N E S W` y `n=NE e=SE s=SW w=NW`, del **movimiento observado**
  entre las dos últimas veces que lo vi. **Declarado sin adornos: el mundo NO
  publica hacia dónde APUNTA nadie** (`protocol_player.md` no trae `facing`),
  así que «hacia dónde apunta» **no se puede mandar**. Se manda hacia dónde se
  mueve, y se dice que es eso.

### El orden, que es lo que decide qué sobrevive al corte

| rivales | |
|---|---|
| 1 | armado y **con mi hermano ya a su alcance** |
| 2 | armado y con mi hermano a alcance + 3 |
| 3 | armado, por distancia a mi hermano |
| 4 | desarmado, por distancia a mi hermano |

| recursos | |
|---|---|
| 1 | **botiquín si su parte dijo `b0`** — se usa un campo que ya viajaba |
| 2 | arma · 3 raciones · 4 mochila · 5 munición · 6 gear menor |

La posición del hermano sale de **su** parte (hecho cierto, con caducidad); sin
parte suyo se ordena por distancia a mí, y queda anotado en el diario.

### Cuánto cabe de verdad

Medido sobre los **10.257 partes** que los veinte diarios habrían emitido:

| | |
|---|---|
| longitud mínima | **31** (la cabeza sola) |
| **mediana** | **87** |
| media | 86,5 |
| **máximo** | **120 · exactamente el límite, nunca por encima** |
| partes por encima de 120 | **0 de 10.257** |
| cadencia | **25 tics**, sin excepción |

| qué entra | n | |
|---|---:|---|
| **rivales que caben** | **18.531** | |
| **rivales que NO caben** | **0** | **cabe siempre todo lo importante** |
| recursos que caben | 58.492 | |
| recursos que **no** caben | **3.820** | el **6,1 %** se queda fuera |

**Lo que cabe de verdad: todos los rivales, siempre, y el 93,9 % de los
recursos.** El corte muerde sólo en la cola de los recursos, que es justo lo
que el orden manda sacrificar primero. Reparto de longitudes: 219 partes de
los 10.257 (2,1 %) tocan el techo de 120.

**La tasa**: `CADA = 25` tics. 25 > 24 garantiza **como mucho un mensaje por
segundo** aunque el reloj tiemble un tic (humo `b` lo comprueba sobre 400
emisiones consecutivas). Frente a los 48 de E1, casi el doble de ritmo.
**Uso del canal: 87/25 = 3,48 car/tic de los 5,0 que permite = 69,6 %.**
Queda libre el 30,4 %, contra el 86,7 % de antes.

---

## 2 · EL OYENTE · `oyente2.py`

### a) Los rivales contados entran COMO SI LOS VIERA

`inyecta()` añade cada rival contado a `obs["visible"]["agents"]` con
`"_contado": True`, `"_de"`, `"_edad"` y `"_rumbo"`. Entran **enteros**, no
pesados, y eso abre **solas** las filas que ya existen —`S-8-EXPOSICION`,
`F-4-ALCANCE`, `F-HERMANO-AMENAZA`, `S-7-AGRESOR`, `agresor_de_la_hermana`—
**sin tocar una línea de `appraisal`**. No se inventa ninguna fila.

La banda de vida que se les pone es `healthy`: es la **más conservadora para
nosotros**, porque no inventa un herido al que rematar.

**Caducan a los `CADUCIDAD_RIVAL = 50` tics.** A once tics por casilla, en 50
tics un rival anda cuatro o cinco casillas y la posición contada ya no es un
hecho.

### b) Los recursos contados, con peso que baja con la edad

**La curva sale de una medida, y la medida costó tres intentos. Los cuento los
tres porque los dos primeros eran sesgos míos:**

1. **v1** usaba `vistas_desde` (radio 9, cálculo **nuestro**) para decidir si
   una casilla «se estaba mirando». Dio **mediana 1 tic**: artefacto puro, el
   mundo no reporta objetos tan lejos siempre.
2. **v2** se auto-calibró —una desaparición sólo cuenta si en ese mismo tic el
   cuerpo reporta **otro** objeto igual de lejos o más— y dio **mediana 11
   tics**, que es **exactamente un paso de movimiento**: seguía contando los
   objetos que **recoge el propio observador** al pisarlos.
3. **v3** excluye esas. Lo que queda es «se lo llevó otro o se agotó».

| edad (tics) | 0 | 12 | 24 | 48 | 75 | 100 | 150 | 200 | 300 | 600 | 1.200 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **S = sigue en el suelo** | 1,000 | **0,399** | 0,363 | 0,339 | 0,311 | 0,286 | 0,267 | 0,257 | 0,245 | 0,203 | 0,156 |

**La forma es lo que importa: un desplome inmediato y luego una meseta.** Lo
que va a desaparecer, desaparece en el primer segundo; lo que sobrevive a ese
segundo se queda horas.

**w(edad) = esa S, interpolada** (`oyente2.peso_recurso`). El recurso contado
entra mientras **w ≥ UMBRAL_REC = 0,30**, lo que da **edad ≤ 86 tics** — tres
partes y medio de E2. El 86 **se calcula** en `edad_max_recurso()`, no se
cablea: si la tabla se remide, el corte se mueve solo.

**DECLARADO SIN ADORNOS, porque cambia cómo hay que leerlo:** esa S mezcla «se
lo llevó otro» con «dejé de verlo», y el diario **no permite separarlos**
—nuestro modelo de línea de vista no es el del motor—. Es por tanto una **cota
inferior de la permanencia**, y usarla como peso peca de **prudente**, que es
el lado correcto del error.

**Y el límite de la versión 1, dicho antes de que nadie lo lea de más: el peso
decide SI ENTRA, no cuánto pesa dentro.** Un peso graduado necesitaría una fila
que lo multiplicara, y eso sería una fila nueva. **No la invento: la decide
Manel.**

### c) Los campos que ya viajaban

| campo | fila que ya lo usa | qué cambia con E2 |
|---|---|---|
| `botiquin` | `S-PROVISION`, `R-HERMANO-FALTA` | nada: ya se leía. E2 lo usa además para **ordenar** los recursos |
| `agresor` + `agresor_slot` + `agresor_pos` | `agresor_de_la_hermana` → `F-HERMANO-GOLPE`, `S-HERIDO`, `F-REENCUENTRO` | **mucho**: al meter al rival contado en `visible.agents`, la vía deja de devolver `None` |
| `hp`, `pos` | `S-DANO-PAREJA`, `S-HERIDO` | nada |
| **`veneno`** | **ninguna** | **sigue sin fila. NO he inventado una. Lo decide Manel.** |

---

## LA TRAMPA QUE ESTO ABRE, Y CÓMO SE CIERRA

Meter rivales en `visible.agents` tiene un precio que encontré leyendo
`decisor_zs.py:570-600`: un candidato `atacar_` nace contra un **agresor
activo**, y una de las dos formas de serlo es **ser el agresor certificado de
mi hermana**… lo cual exige que ese asiento esté visible. **Al inyectarlo, la
puerta se abre sola y el cuerpo atacaría a algo que no ve.**

El humo `k` lo **demuestra** en vez de suponerlo:

```
sin inyectar: 0 ataques contra el contado · inyectando: 1 · con el filtro: 0
```

`policy_pareja` envuelve `D.candidatos` **desde fuera** (como ya hacía
`policy_forma.py:1744` con `PARTE.emite`) y tira toda receta cuyo `objetivo`
esté marcado `_contado`. Queda anotado en el diario (`k: "ojos"`, `vetados`).

### Los once humos

```
OK  a · 120 caracteres y ASCII imprimible, en TODOS los tics (el más largo: 116)
OK  b · la cadencia 25 no cabe dos veces en un segundo de 24 tics
OK  c · ida y vuelta: 10.854 rivales+recursos sin perder uno
OK  d · el corte no parte ningún token
OK  e · el orden: primero el armado que tiene al hermano a tiro
OK  f · sin parte del hermano la obs sale IDÉNTICA (gate de pareado)
OK  g · el rival contado entra en visible.agents con su marca
OK  h · el rival contado CADUCA
OK  i · el recurso pesa menos con la edad y se cae pasado el corte (86 tics)
OK  j · el alfabeto se LEE del mundo y no repite letra
OK  k · el rival contado ABRE la vía de ataque, y el filtro la cierra
```

Corren sobre un **mundo real leído de un diario**, no sobre uno de mentira.

---

## 3 · EL BANCO · `banco_P6_3.py` · sin jugar nada

Repite los 20 diarios haciendo hablar a los dos hermanos con E2 (emisión cada
25 tics, latencia +2 medida, caducidades aplicadas) y pregunta **una sola
cosa: ¿habría llegado la información a tiempo?**

### El control, que va primero

La `S-8-EXPOSICION` del banco tiene que reproducir la del diario o el punto (c)
no vale. **La primera versión falló en 6.838 tics de 156.634 — y eran, todos,
exactamente los tics con el camuflaje puesto** (quien va camuflado sólo es
visto desde más cerca). Con esa rama dentro:

| | desajustes > 10⁻⁴ |
|---|---|
| S-8 del tic actual | **6 de 156.634 = 0,004 %** |
| S-8 proyectada de un candidato | **4 de 1.483 = 0,27 %** |

### (a) El mensaje nunca se pasa

**0 de 10.257 partes por encima de 120 caracteres. Hueco entre partes: 25 tics,
sin una excepción.** (Tabla completa arriba.)

### (b) ¿Habría llegado a tiempo?

| | tics | llega | |
|---|---:|---:|---|
| **amenaza a ciegas (2d)** | 4.775 | **3.514** | **73,6 %** |
| **recurso que falta (2c)** | 68.682 | **56.989** | **83,0 %** |

**El 26,4 % de la amenaza a ciegas que no llega** es el precio de la cadencia y
de la caducidad de 50 tics: el rival aparece entre dos partes, o el dato envejece
antes de que haga falta. **No se arregla subiendo la tasa**, que ya está en el
límite del canal.

*Aviso de comparabilidad: los 68.682 tics de 2c no son los 57.124 de P6-2. El
banco usa la clasificación de `parte2.clase_de`, que cuenta como arma también
las `ikThrown` (cuchillos, red); P6-2 sólo contaba `ikMelee` e `ikRanged`. Es
una definición mejor, pero **no se pueden restar los dos números**.*

### (c) La discrepancia de `S-8-EXPOSICION`

Sobre las **1.483 decisiones** con detalle por candidato en que S-8 salió mal
proyectada:

| | mediana | suma de \|disc\| |
|---|---:|---:|
| **hoy** | 0,21582 | **273,8** |
| **con los ojos** | 0,11767 | **208,9** |
| | | **baja el 23,7 %** |

Y **donde de verdad había un rival contado que añadir (772 de las 1.483)**:

| | mediana | suma |
|---|---:|---:|
| hoy | 0,24456 | 173,4 |
| con los ojos | **0,07724** | 108,5 |
| | | **baja el 37,4 %** |

**Mejora en 721 decisiones, empeora en 123, queda igual en 639.** Las 123 que
empeoran son reales y no las escondo: el rival contado **ya se había movido** y
la proyección se pasa de frenada en el otro sentido. Es el precio de tratar un
dato de hace hasta 50 tics como un hecho.

### LO QUE EL BANCO NO DICE, Y NO VOY A DEJAR QUE PAREZCA QUE DICE

**Esto no dice qué habría hecho el cuerpo.** Con la información dentro, el
cuerpo elige otra cosa, el mundo responde otra cosa y el diario deja de valer a
partir de ese instante. El banco mide **el canal**: si el dato cabía, si salía a
tiempo y si habría estado en la percepción del que lo necesitaba. **Nada más.**

---

## 4 · EL SELLO

`cantera/paper6/SELLO_P6_3.md`, md5 **`dd73e8caa413f2ad34434d47db10b6a3`**,
escrito y cerrado **antes de que exista ninguna serie**. Lleva, con cifra y
banda: golpes recibidos en amenaza a ciegas (≤ 60 % del brazo sin ojos), tics
sin un recurso que el hermano veía (≤ 2.000 por vida contra 2.856), vida en
tics (13.000-14.500, **no espero que suba**) y discrepancia de vínculos
(38-46 %, con la de S-8 bajando entre el 15 % y el 35 % — **menos que el 23,7 %
del banco, y digo por qué antes de medirlo**).

Y las dos cosas que más miedo me dan, también selladas: que el brazo apagado
**no** salga bit a bit igual al G2 de P6-1, y que aparezca **una sola** acción
de ataque contra un asiento `_contado`.

---

## LOS ARCHIVOS NUEVOS, CON SU MD5

| archivo | md5 | |
|---|---|---|
| `cantera/paper6/parte2.py` | `67ba0003234939c349af12be5764a3b0` | 294 líneas |
| `cantera/paper6/oyente2.py` | `f525d874c030204d64e174d30bcce42b` | 162 líneas |
| `cantera/paper6/policy_pareja.py` | `796fc64229d047410fb351dfa61f871b` | 173 líneas |
| `cantera/paper6/humo_P6_3.py` | `0c3c45217c7480b3e228f21a8fe21771` | 264 líneas |
| `cantera/paper6/banco_P6_3.py` | `b7287446e831a1a1d540e809970d9dca` | 353 líneas |
| `cantera/paper6/vida_objetos.py` | `1abeb63609230cda144042033a6da217` | 127 líneas |
| `cantera/paper6/SELLO_P6_3.md` | `dd73e8caa413f2ad34434d47db10b6a3` | 133 líneas |

Datos: `P6_3_vida_objetos.json`, `P6_3_banco.json`.

**Comprobado al terminar: `motor/model.py` = `1e511978c251130e95169ebf8443efa1`
y los 199 archivos de `CONGELADO.md`, 0 alterados.**

---

## LO QUE QUEDA EN MANOS DE MANEL

1. **`veneno` no tiene fila.** Es el único campo del parte que nadie lee. Darle
   una sería una fila nueva y no la invento.
2. **El peso del recurso decide si entra, no cuánto pesa dentro.** Graduarlo
   pide una fila que lo multiplique.
3. **`CADUCIDAD_RIVAL = 50` y `UMBRAL_REC = 0,30`** son mis números, razonados
   pero no calibrados en campo: 50 tics son cuatro o cinco casillas de
   movimiento, y 0,30 sale de la curva medida. Se pueden mover.
4. **Si sólo un asiento sube a E2, el otro no lo entiende.** El parser de E1 es
   anclado al final de línea y E2 le añade cola. Los dos asientos suben juntos o
   no sube ninguno.
