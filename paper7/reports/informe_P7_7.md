# P7-7 · Aprender bien estando sano, y la curiosidad que abre camino

*3-oct-2026. Coste: **créditos de la plataforma** 0,3265 USD en 3 partidas (por día: 1: 0,1086, 2: 0,1091, 3: 0,1088); **consola de Anthropic 0 USD**.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; los 202 archivos de `CONGELADO.md` y los 32 de `CONGELADO_P6.md` con su md5; el cuerpo
no se toca: todo en archivos `_P7`. Una vida por proceso; la memoria viaja solo en el cuaderno. Los números de método son los de la mesa.*

## Sección 1 · Las cinco decisiones, en el código

**Decisión 1, el recuerdo con techo** (`cuaderno_P7.py`, `descubre_P7.py`). La ventana del uso apunta si la vida tocó su máximo (`mem.hp_max`,
el que el cuerpo lee del mundo) en algún tic entre el uso y el cierre; si lo tocó, el recuerdo se escribe con `al_menos`. En `creencia`, los
recuerdos "al menos" del dominio cuerpo solo entran en la media si su efecto está por encima de la creencia que forman los recuerdos firmes con
el neutro (con ninguno firme, esa creencia es la del neutro, 0: un "al menos" positivo entra). Pueden subirla, nunca bajarla. En recursos y
vínculo, y en la ignorancia, pesan como cualquier recuerdo. La huella (`P7_huella`) lleva `al_menos` y `hp_max`.

**Decisión 2, la curiosidad abre camino** (`descubre_P7.py`, pieza F en el envoltorio de `D.candidatos`). Las ganas de un objeto generan hoy
un candidato `ir_objeto` (decisor_zs.py:458-462): tipo `ir` con `recoger`, cuya imaginación, si llega, pone el objeto en el zurrón
(:805-813). La carencia de ignorancia genera ahora el mismo candidato, `ir_curioso`: destino el botiquín más cercano visto o recordado
(`mem.objetos_vistos`) y no cedido; al llegar, la foto lo tiene en el zurrón y R-CURIOSIDAD pasa a alivio 0,5. Con las mismas dos condiciones
de las ganas de hoy: con el zurrón lleno la cosa no es adquirible (`_promesa`, :650-652) y con la cosa en mi casilla no hay a dónde ir
(`_mejor_objeto` devuelve mi casilla y `ir_objeto` no se crea, :459: de eso se ocupa `coger`). Si `ir_objeto` ya va al mismo sitio, no se
duplica. Ningún número nuevo. Las dos condiciones no estaban en la primera corrida de F2 y se añadieron tras medirla (sección 4).

**Decisión 3, varios objetos en la casilla** (`coge_P7_7.py` → `P7_7_coge.json`). Sobre los 80 diarios de A4 y los 12 de los humos de P7-5 y
P7-6: 90 cogidas con dos o más clases en la casilla y algo ganado. En las 90 el mundo entregó **el primero de la lista
de la casilla** (`ve_items`, el mismo orden que ve el cuerpo); no por tipo (6 tipos distintos cogidos) ni por cantidad (el de más unidades solo en
25). Lo soltado cae **al final** de la lista (6 de 6 sueltas en casilla con varios). Lo que no se puede saber: si el
mundo salta un primero que no cabe y entrega el segundo; en los 92 diarios no hay ni un `pickup` con el primero sin sitio y otro con sitio
(0 casos). Queda apuntado para Ari. La imaginación de `coger` ya usa esa regla (imagina `aqui[0]`, decisor_zs.py:478-482), así
que no se toca; lo que cambia es **hacer sitio**: el candidato se crea solo para el primer objeto de la casilla cuando no cabe (en P7-6 se
creaba para cualquiera, e imaginaba coger lo que el mundo no entrega); como lo soltado cae al final, `coger` al tic siguiente sigue viendo el
mismo primero.

**Decisión 4**: el escalado de `ACOPIO_POR_DOS` por la creencia queda como estaba en P7-6. **Decisión 5**: armas y munición siguen sin
soltarse (el candidato de hacer sitio solo suelta consumibles).

## Sección 2 · El cuaderno del asiento 11 de P7-6, recalculado con el techo

Fuente: `recalcula_P7_7.py` → `P7_7_recalculo.json`, `P7_7_cuaderno_11_recalculado.json`. El único uso (día 3, tic 10.665, dentro, vida
99 → 100 con máximo 100) toca techo: el recuerdo pasa a **"al menos +1"**.

| | creencia cuerpo (dentro) | recursos | vínculo | ignorancia | pesos vividos |
|---|---:|---:|---:|---:|---:|
| P7-6 (sin techo) | 0,5247 | -0,5247 | 0,0000 | 0,4753 | 1,1039 |
| P7-7 (con techo) | 0,5247 | -0,5247 | 0,0000 | 0,4753 | 1,1039 |

Queda igual en cifras: con ningún recuerdo firme la creencia es la del neutro (0) y el "al menos +1" está por encima, así que entra como
antes; la ignorancia no cambia porque el techo no toca los pesos. Lo que cambia es lo que pasará cuando llegue un recuerdo firme: con uno de
+40 en la misma situación (hipotético, calculado con el mismo código, no es dato del campo) la creencia del cuerpo sería 22,04 con el techo y
15,06 sin él: el "cura 1" de la vida casi llena dejaría de arrastrar la media hacia abajo.

## Sección 3 · F1: con todo apagado y con TECHO, la variante reproduce A4

| brazo | tics iguales | distintos | los distintos |
|---|---:|---:|---|
| apagado | 1.007.274 | 2 | A4_21622393/10 t 1832; A4_21622393/10 t 2041 |
| TECHO | 1.007.274 | 2 | A4_21622393/10 t 1832; A4_21622393/10 t 2041 |

Los mismos dos tics de P6-30, P7-5 y P7-6. **F1 pasa.** Fuente: `banco_P7_5.py --f1` (`P7_7_F1.json`).

## Sección 4 · F2: las escenas de los humos de P7-5 y P7-6 al lado de un botiquín

Réplica de los 12 diarios de los dos humos (brazo APRENDE, cuaderno vacío, un subproceso por vida, `banco_P7_7.py`), registrando en cada tic a
dos casillas o menos de un botiquín la elección de la réplica y las d de todos los candidatos. 62.986 escenas. El mundo es el del diario:
lo elegido no cambia la partida, pero se ve qué haría.

| situación | tics | ir curioso (candidato presente) | coger | ir al objeto | hacer sitio | quieto | otra |
|---|---:|---:|---:|---:|---:|---:|---:|
| encima, con ranura libre | 894 | 0 (0) | 764 | 5 | 0 | 112 | 13 |
| encima, zurrón lleno | 1.896 | 0 (0) | 1 | 2 | 53 | 1.574 | 266 |
| a una casilla, con ranura libre | 6.195 | 5.364 (5.876) | 5 | 295 | 0 | 277 | 254 |
| a una casilla, zurrón lleno | 32.760 | 0 (0) | 1 | 720 | 1.329 | 24.035 | 6.675 |
| a dos casillas, con ranura libre | 1.616 | 986 (1.125) | 3 | 247 | 0 | 327 | 53 |
| a dos casillas, zurrón lleno | 19.596 | 0 (0) | 0 | 416 | 1.110 | 16.561 | 1.509 |
| a dos casillas, ya lleva uno | 29 | 0 (0) | 0 | 0 | 1 | 24 | 4 |

Lectura. **La curiosidad abre camino**: a una casilla con ranura libre `ir_curioso` gana 5.364 de 6.195; a dos, 986 de 1.616
(en P7-6, al lado del botiquín, casi siempre `noop`). Encima con ranura libre, `coger` 764 de 894. Con el zurrón lleno no existe el
candidato (no es adquirible) y manda `quieto`, como antes. Las d de una escena a una casilla con sitio libre (482, P76_humo_APRENDE_27068301/11):
`ir_curioso` 3,6570, `noop` 3,6717.

**La primera corrida, sin las dos condiciones, y por qué se añadieron** (`P7_7_F2_primera_resumen.json`). Con `ir_curioso` creado siempre que
no llevaba botiquín: encima de uno con el zurrón lleno ganaba un paseo hacia OTRO botiquín (sin alivio imaginado, porque no cabe) en
946 de 1.896 tics, y encima de uno con ranura libre le quitaba el tic a `coger` en 276 de 894
(hacia otro botiquín a dos o tres casillas: la d de moverse con el botiquín imaginado en el zurrón quedaba 0,03 por debajo de la de cogerlo
quieto). Las ganas de hoy no hacen ninguna de las dos cosas (zurrón lleno → promesa 0; cosa en mi casilla → sin `ir_objeto`), así que
`ir_curioso` lleva las mismas dos condiciones. No es un número: es el mismo candidato que generan las ganas.

**Hacer sitio en F2**: elegido 2.493 veces, de ellas 2.410 rations por camouflage, 43 rations por first_aid, 19 rations por arrows, 10 rations por backpack, 10 rations por sword, 1 first_aid por rations. Es el cuerpo pesando lo que pierde contra lo que gana (el
camuflaje promete por S-8); se informa.

**Huellas con techo en el banco**: 26754114/10 tic 13.588: vida 74 → 100, cuerpo +26 (al menos); 27068301/11 tic 10.665: vida 99 → 100, cuerpo +1 (al menos).

## Sección 5 · F3: el humo de tres días (brazo APRENDE, las dos criaturas)

Semillas nuevas, nunca usadas: día 1: 27173030, día 2: 27277759, día 3: 27382488 (las tres siguientes de la sucesión de semillas_S2 tras las de P7-6; sin carpeta en
`paintball/runs` ni mención en el repo). Imágenes: día 1: gemv-p7-aprende:v7 (0b546158…), día 2: gemv-p7-aprende:v8 (b38f3f9b…), día 3: gemv-p7-aprende:v9 (47e8f98c…); el cuaderno de cada día viaja horneado al siguiente.

**Día 1** (semilla 27173030, completed, coste 0,1086 USD de plataforma).

| criatura | vivo · puesto | se acerca: tics `ir_curioso` · llegadas a una casilla (por curiosidad / de paso) | hace sitio (tic, qué suelta por qué) | coge (con sitio / tras hacer sitio; de ellas regaladas al hermano en 10 tics) | usa (tic, situación, vida) | recuerdos (al menos) | cuaderno al acabar: ignorancia; creencia por situación |
|---|---|---|---|---|---|---|---|
| 10 | 12.793 · 4 | 6.049 · 45 (38 / 7) | 10330: first_aid por backpack | 32 / 1 (regaladas al hermano 30) | 9496 dentro vida 99; 10235 dentro vida 89; 10284 dentro vida 78; 10335 fuera vida 75; 10384 dentro vida 68 | dentro al menos +1.0 / -1 / -0.3 (vida 99 → 100); dentro -0.2 / +0 / +0.4 (vida 89 → 78) INTERRUMPIDO, apuntado (fallo, día 1); dentro +0.3 / +0 / +1.9 (vida 78 → 75) INTERRUMPIDO, apuntado (fallo, día 1); fuera -0.7 / +0 / +1.3 (vida 75 → 71) INTERRUMPIDO, apuntado (fallo, día 1); dentro al menos +32.0 / -1 / +0.2 (vida 68 → 100) | 0,152; dentro: cuerpo 6,87, recursos -0,43, vínculo 0,43; fuera: cuerpo -0,35, recursos 0,00, vínculo 0,65 |
| 11 | 12.217 · 6 | 10.253 · 178 (178 / 0) | ninguno | 8 / 0 (regaladas al hermano 8) | ninguno | ninguno | –; no sé |

**Día 2** (semilla 27277759, completed, coste 0,1091 USD de plataforma).

| criatura | vivo · puesto | se acerca: tics `ir_curioso` · llegadas a una casilla (por curiosidad / de paso) | hace sitio (tic, qué suelta por qué) | coge (con sitio / tras hacer sitio; de ellas regaladas al hermano en 10 tics) | usa (tic, situación, vida) | recuerdos (al menos) | cuaderno al acabar: ignorancia; creencia por situación |
|---|---|---|---|---|---|---|---|
| 10 | 14.953 · 2 | 1.202 · 169 (0 / 169) | 8309: rations por sword | 0 / 0 (regaladas al hermano 0) | ninguno | ninguno | 0,159; dentro: cuerpo 6,80, recursos -0,42, vínculo 0,43; fuera: cuerpo -0,35, recursos 0,00, vínculo 0,64 |
| 11 | 14.953 · 1 | 8.051 · 87 (82 / 5) | 12700: first_aid por backpack; 13159: rations por first_aid | 17 / 2 (regaladas al hermano 15) | 12710 dentro vida 92; 12759 dentro vida 82; 12945 dentro vida 93 | dentro +0.8 / +0 / -2.1 (vida 92 → 82) INTERRUMPIDO, apuntado (fallo, día 2); dentro al menos +18.0 / -1 / +0.8 (vida 82 → 100); dentro al menos +7.0 / -1 / +1.2 (vida 93 → 100) | 0,218; dentro: cuerpo 6,66, recursos -0,52, vínculo -0,03 |

**Día 3** (semilla 27382488, completed, coste 0,1088 USD de plataforma).

| criatura | vivo · puesto | se acerca: tics `ir_curioso` · llegadas a una casilla (por curiosidad / de paso) | hace sitio (tic, qué suelta por qué) | coge (con sitio / tras hacer sitio; de ellas regaladas al hermano en 10 tics) | usa (tic, situación, vida) | recuerdos (al menos) | cuaderno al acabar: ignorancia; creencia por situación |
|---|---|---|---|---|---|---|---|
| 10 | 13.825 · 7 | 1.822 · 56 (32 / 24) | 10436: first_aid por blowgun; 10439: rations por first_aid; 10441: first_aid por rations; 10443: rations por first_aid (+7) | 4 / 5 (regaladas al hermano 1) | ninguno | ninguno | 0,316; dentro: cuerpo 10,93, recursos -0,68, vínculo -0,04 |
| 11 | 14.761 · 5 | 1.087 · 30 (17 / 13) | ninguno | 9 / 0 (regaladas al hermano 2) | 4851 dentro vida 94; 14047 dentro vida 14; 14096 dentro vida 64 | dentro al menos +6.0 / -1 / -2.0 (vida 94 → 100); dentro +50.0 / -1 / +0.0 (vida 14 → 64); dentro al menos +36.0 / -1 / +0.0 (vida 64 → 100) | 0,142; dentro: cuerpo 31,43, recursos -0,86, vínculo 0,00 |

**Lectura del humo** (`humo_P7_7.py` → `P7_7_humo.json`; cuadernos `P7_7_dia*_cuaderno_*.json`).

*Acercarse.* La curiosidad abre camino de verdad: `ir_curioso` es la elección en 6.049 tics del asiento 10 y 10.253 del 11 el día 1, y de
las 45 y 178 llegadas a una casilla de un botiquín, 38 y 178 vienen de él (en el tic de llegar o en los diez anteriores). Los días 2 y 3,
con la ignorancia ya baja (0,15 a 0,30 al arrancar), la fila vale como mucho 0,18 × ignorancia y `ir_curioso` gana menos (1.202 y 8.051;
1.822 y 1.087 tics), y las llegadas son más de paso.

*Coger y regalar.* Las cogidas son muchas pero casi todas se regalan: el día 1 el asiento 10 cogió 33 veces y 30 de ellas soltó el
botiquín en los diez tics siguientes con `soltar_first_aid` (la cura junto a la cama del hermano, decisor_zs.py 6b, con el hermano a la vista);
el 11, 8 de 8; el día 2 el 11, 15 de 19. El hermano no lo recoge, la cesión caduca y la curiosidad lo vuelve a coger unos 300 tics después
(asiento 10, día 1, tics 626, 934, 1.242, 1.550…: coger, dos tics, soltar). Es la curiosidad trayendo la cosa a la mano y la fila de regalo del
cuerpo congelado dándola; se informa (sección 7).

*Hacer sitio.* 1, 0; 1, 2; 11, 0 por día y asiento. Las 11 del asiento 10 el día 3 son una oscilación entre dos consumibles en la misma
casilla (tics 10.436-10.467: `first_aid por rations`, `rations por first_aid`, cinco veces cada una): cada imaginación ve solo lo que gana
por ese lado. Se informa.

*Usar y aprender.* Ocho ventanas con el botiquín gastado en los tres días, todas dentro del círculo, y cuatro más sin gasto. Día 1, asiento
10: vida 99 → 100 (**al menos +1**), y 68 → 100 (**al menos +32**); entre medias tres ventanas (vida 89, 78 y 75 fuera) en las que el cuerpo
rompió su propio canal moviéndose (`move` en el tic 10.241, 10.285 y 10.340; el botiquín siguió en el zurrón) y que el cuaderno apuntó como
"cura −0,2, +0,28, −0,72". Día 2, asiento 11: 82 → 100 (**al menos +18**), 93 → 100 (**al menos +7**) y una interrumpida (vida 92, "+0,8").
Día 3, asiento 11: 94 → 100 (**al menos +6**), **14 → 64: +50, el único recuerdo firme de los tres días, la cura del catálogo**, y 64 → 100
(**al menos +36**). La regla del techo hace lo que la mesa pidió: al acabar el día 3 la creencia firme del asiento 11 (el +50 con el neutro)
es 29,06; de los cuatro "al menos" solo el +36 está por encima y entra (creencia final 31,43); el +18, el +7 y el +6, usos con la vida casi
llena, quedan fuera y no la arrastran. Sin el techo, esos tres valdrían como cualquier recuerdo. La ignorancia los cuenta a todos: 0,142.

*Lo que imaginó al usar.* Día 1 el asiento 10 usó con "no sé" (0) la primera vez y con 0,57, 0,31, 0 (fuera) y 0,30 las siguientes; día 3 el
asiento 11 usó imaginando 8,74 y 8,03, lo que decía su cuaderno limpio del día 2.

**Un fallo de fontanería encontrado el día 1 y corregido para el día 3, declarado.** La ventana se cerraba cuando desaparecía el canal, también
si el cuerpo lo había roto moviéndose: tres de las cinco "experiencias" del asiento 10 el día 1 (y una de las tres del 11 el día 2) no gastaron
el botiquín y entraron en el cuaderno como curas de −0,72 a +0,8. Con ellas, el asiento 10 arrancó el día 2 creyendo 6,87 (limpio, 11,28) y
con ignorancia 0,15 (limpio 0,29): ganas y curiosidad más bajas de lo que le tocaba (0 cogidas, 0 usos ese día). Desde el día 3 una ventana que
se cierra con el botiquín aún en el zurrón es un canal interrumpido: se registra en la huella (`interrumpido`) y no entra en el cuaderno
(`descubre_P7.ventana`). Los cuadernos del día 2 se rehicieron desde las huellas con esa regla (`limpia_cuaderno_P7_7.py` →
`P7_7_dia2_cuaderno_*_limpio.json`: asiento 10, 2 recuerdos, 11,11; asiento 11, 2 recuerdos, 8,74) y son los que viajaron horneados al día 3;
los que escribió el campo se guardan tal cual (`P7_7_dia2_cuaderno_*.json`). Los días 1 y 2 jugaron con el fallo; el día 3 no tuvo ninguna
ventana interrumpida.

GIF de los datos del primer uso (`gif_P7_5.py`, local, fuera de git): `P7_7_dia1_primer_uso_10.gif`, `P7_7_dia1_quinto_uso_10.gif`, `P7_7_dia3_uso_vida14_11.gif`.

## Sección 6 · F4: créditos del humo

Créditos de la plataforma: 0,3265 USD en 3 partidas enteras (por día 0,1086, 0,1091, 0,1088; media 0,1088). Tres subidas de imagen (v7-v9 de `gemv-p7-aprende`), sin créditos. Consola de Anthropic: 0.

## Sección 7 · Lo que queda para la mesa

1. **La cogida que se regala.** La curiosidad trae el botiquín a la mano y la fila de regalo del cuerpo congelado (`soltar_first_aid`, la cura
   junto a la cama del hermano) lo suelta dos tics después, con el hermano a la vista; él no lo coge y a los 300 tics se repite (30 de 33
   cogidas del asiento 10 el día 1; 8 de 8 del 11; 15 de 19 el día 2). Dos filas tirando de la misma cosa en sentidos opuestos: ¿debe la
   imaginación del regalo ver que el hermano no lo recoge, o el hermano aprender a cogerlo? Decisión de diseño.
2. **Hacer sitio oscila entre dos consumibles** en la misma casilla (día 3, asiento 10: diez cambios ración ↔ botiquín en 31 tics): cada
   imaginación ve solo el lado que gana. Haría falta que la foto de hacer sitio recordara lo que acaba de soltar (una cesión corta sobre lo
   propio) o que el candidato no se ofrezca para recoger lo que soltó hace menos de N tics. Número de método: lo fija la mesa.
3. **El cuerpo rompe su propio canal** moviéndose mientras cura (3 de 5 ventanas el día 1, 1 de 3 el día 2). Ya no entra en el cuaderno, pero
   el gesto sigue: el decisor congelado no sabe que está canalizando. Si se quiere que el cuerpo que descubre se esté quieto mientras cura,
   es un candidato o una regla nueva (diseño).
4. **Para Ari:** si el mundo salta un primer objeto que no cabe y entrega el segundo. En 92 diarios no hay ni un caso que lo diga (0 `pickup`
   con el primero sin sitio y otro con sitio). La imaginación de `coger` y la de hacer sitio asumen hoy "el primero de la lista".
5. **Usar con la vida casi llena.** Cinco de los ocho usos con gasto fueron con la vida entre 82 y 99; el candidato `usar_botiquin` existe
   siempre que falte un punto de vida (decisor_zs.py:485) y su valor es la creencia. El techo protege la creencia, no el botiquín gastado. El
   único recuerdo firme de los tres días llegó con la vida a 14. Si se quiere que la cura espere a que duela, es la mesa quien lo decide.
6. **Hacer sitio suelta raciones por camuflaje** (F2: 2.410 veces en una vida): es el cuerpo congelado pesando la promesa de S-8 contra la
   carencia de W; con la regla "solo el primero de la casilla" el candidato se ofrece para cualquier primero que no quepa. Se informa.

## Archivos

| archivo | qué es |
|---|---|
| `cuaderno_P7.py`, `descubre_P7.py` | el recuerdo con techo; `ir_curioso`; hacer sitio para el primero de la casilla |
| `coge_P7_7.py`, `P7_7_coge.json` | la medida de qué entrega el mundo con varios objetos en la casilla (decisión 3) |
| `recalcula_P7_7.py`, `P7_7_recalculo.json`, `P7_7_cuaderno_11_recalculado.json` | el cuaderno del asiento 11 de P7-6 con el techo (decisión 1) |
| `banco_P7_5.py --f1`, `P7_7_F1.json`; `banco_P7_7.py`, `P7_7_F2.json`, `P7_7_F2_primera_resumen.json` | F1 y F2 |
| `lanza_P7_7.py`, `Dockerfile.pareja_P7_7`, `P7_7_brazos.json`, `P7_7_dia*_{peticion,resultado,cuaderno_*}.json`, `cuadernos_humo_P7_7/` | el humo |
| `humo_P7_7.py`, `P7_7_humo.json`, `P7_7_diarios_manifiesto.md` | la lectura del humo y el manifiesto de los diarios (fuera de git) |
| `escribe_informe_P7_7.py`, `informe_P7_7.md` | este informe |
