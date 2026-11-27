# Prompt 162: las casas, dónde duermen, las figuras para publicar y la historia de los sellados

*20-nov-2026. Solo leer, contar y figuras. No se ha jugado ninguna partida, no se ha tocado nada sellado y no se ha usado la clave.*

Abreviaturas de las citas:
- **mundo** = `valle/mundo.py`;
- **cfg** = `valle/config_valle.json`;
- **cv** = `cantera/paper8/cuerpo_valle.py`;
- **vc1** = `cantera/paper8/cuerpo_vc1.py`;
- **jug** = `valle/jugadores.py`.

Son los ficheros con que se jugó: en el prompt 159 comprobé que sus huellas cuadran con las de las partidas, y desde entonces no han cambiado.

## Parte 1: las casas

**Cómo son.**
- Hay cuatro casas, A, B, C y D, de 3 × 3 casillas cada una (cfg: `mapa.casa_lado` 3; mundo:103-108).
- La puerta de cada casa es una de sus nueve casillas (cfg: `mapa.casas[].puerta`; mundo:108). Es casilla de la casa a todos los efectos: dentro de ella hace la temperatura de dentro y la bestia no la alcanza (ver más abajo).
- Las «puertas» del terreno (mundo:112-113) son otra cosa: las cuatro salidas del borde del valle. No se pisan (mundo:453).

**Cuántas caben y si dos pueden estar en la misma casilla.**
- **Dos criaturas no pueden estar en la misma casilla.** Un paso a una casilla ocupada por una criatura viva (o por la bestia) falla con «ocupada» (mundo:446-448 y 753). Tampoco se ofrece como acción válida (mundo:578). Las muertas no ocupan (mundo:448).
- **En una casa caben, como mucho, nueve:** una por casilla, contando la puerta. El mundo no tiene ningún otro límite.
- Al empezar, las dos hermanas de cada casa salen en dos casillas libres de dentro, nunca en la puerta (mundo:195-197).

**Si una dormida en la puerta impide entrar a otra.**
- **Sí.** La pared de una casa solo se cruza por su puerta (mundo:455-458). El mundo solo mueve en cuatro direcciones (mundo:18). Así, cada puerta tiene una sola casilla de fuera desde la que se entra: A (21, 23), B (26, 21), C (28, 26) y D (23, 28).
- Si hay alguien en la casilla de la puerta, dormida o despierta, nadie entra ni sale de esa casa, porque la casilla está ocupada (mundo:753). El mundo no mira si duerme.
- **En RG69r+voz está arreglado en parte.** Desde el prompt 103 (`casa_v51`, encendido en RG68r y en RG69r+voz):
  - no se le ofrece «dormir» si está en una puerta, de cualquier casa, salvo que esté agotada (cv:2933-2934);
  - «ir a casa» lleva a una casilla libre de dentro, no a la puerta, rodeando a quien esté delante (cv:2793-2798 y 2756).
- **Lo que no está arreglado:** agotada se duerme sola, pida lo que pida (cfg: `criaturas.agotada_se_duerme`), y si está en una puerta se duerme allí.
- En los datos (parte 2), **todas** las veces que una criatura se duerme en una puerta estaba agotada: 57 de 57 en RG69r+voz y 36 de 36 en RG68r, sumando los cinco mundos. Ya lo decía el v4 de RG61r (`informe_experimento_v4.md:13`: 141 de 141).
- Una vez dormida de noche, el sueño sigue solo hasta la mañana (cfg: `criaturas.reloj`). Así que la que se duerme agotada en la puerta suele taparla toda la noche.

**Cómo sabe una criatura cuál es su casa.**
- Por su nombre: la casa es la letra (A1 y A2 son de la casa A). Lo hace el mundo (mundo:68) y también la criatura (cv:221).
- Las casillas y la puerta de su casa las lee del mapa público, que trae al nacer (cv:224-225; mundo:129).
- El mundo además se lo dice al empezar (`infos[a]["casa"]`, mundo:238) y en cada turno, en «en_casa» (mundo:1149).

**Qué quiere decir exactamente «ir a casa».**
- Es una opción de la criatura, no del mundo. El mundo solo tiene pasos de una casilla (mundo:578).
- Se ofrece cuando no está en una casilla de dentro de su casa. La puerta cuenta como fuera para esto: estando en su puerta, se le sigue ofreciendo.
- **El destino** es la casilla de dentro de su casa, sin la puerta, que esté libre (de las que ve ocupadas) y más cerca andando. A igual distancia, la primera por orden. Si están todas ocupadas, la más cerca de todas (cv:2793-2798).
- **El camino** es el más corto que rodea las casillas ocupadas ahora (cv:2735-2744 y 2756).
- Se ofrece solo si el primer paso de ese camino es un paso válido (cv:2947-2950). Con la puerta tapada no hay camino y no se ofrece.
- Si la elige, sigue el destino sin volver a decidir. Lo suelta si llega, si no avanza en 3 turnos o si cambia lo que siente (cv:2850-2860; `compromiso_emocion_v18` encendido).
- **Una casa ajena no la puede elegir:** «ir a casa» solo apunta a la suya, y no hay ninguna opción «ir a otra casa».
- **Sí puede acabar en una casa ajena por otros caminos:**
  - «ir a la hermana» (cv:2780-2781) o «ir a la vecina» (cv:2802-2805), si la otra está dentro;
  - pasos sueltos;
  - y dormirse donde se queda.

**Qué casas le sirven para el frío, para la bestia y para dormir.**

| | en el mundo | en lo que imagina la criatura |
|---|---|---|
| frío | cualquier casa, puerta incluida: la temperatura «de dentro» (mundo:483), y el frío solo cuesta hambre fuera (mundo:682-684) | cualquier casa (`todas_casas`, cv:226): el frío en la foto (cv:2532-2541) y la fila del frío (cv:1756) |
| bestia | cualquier casa, puerta incluida: la bestia no pisa las casas (mundo:118-119) y no encuentra a nadie dentro de una casa (mundo:1019) | cualquier casa: la regla pública «la bestia no entra en las casas» (mundo:138-140) en el alcance (cv:1619-1620), la amenaza (cv:786) y la anticipación de la noche (cv:901, 914) |
| dormir | se puede dormir en cualquier casilla (mundo:536-544); la cura y el descanso son iguales dentro y fuera | lo que cree que quita una noche dormida fuera, solo si acaba fuera de cualquier casa (cv:2519-2523) |
| despensa | solo la de su casa, y solo dentro de ella (mundo:585-590, 791, 802) | la despensa que ve es la suya (mundo:1154) |

**En resumen:** para el frío, la bestia y dormir, cualquier casa le sirve igual que la suya, en el mundo y en lo que imagina. Solo hay dos cosas que son de su casa y no de cualquiera: la despensa y el destino de «ir a casa».

## Parte 2: dónde duermen, en las partidas del v6

Es análisis hecho después de ver los datos. No propongo causas. El programa es `casas_noches_162.py`, y las tablas completas, con los intervalos, están en `salida/casas_noches_162.md` y `.json`.

**Cómo se cuenta.**
- **Las partidas:** RG68r y RG69r+voz, cinco mundos y 40 semillas (30161-30200), 40 días: 400 partidas de `valle_experimento_v6`. Se leen del registro del mundo (`mundo.jsonl.gz`): la casilla, si duerme, si está agotada y si está muerta, turno a turno.
- **La noche** es la fase «noche», los turnos 280 a 399 de cada día, igual que en la medida sellada de las noches fuera (`dormir_fuera_v5/noches_v5.py:71-73`).
- **Cada criatura viva al empezar la noche** se apunta en un sitio. Cada turno dormida cuenta en uno de cinco: dentro de su casa (sin la puerta), en la puerta de su casa, dentro de una casa ajena, en la puerta de una ajena, o fuera.
- **El sitio de la noche** es el que tiene más de la mitad de sus turnos vivos. Si ninguno llega, la noche cuenta como «despierta». Es lo simple, como la sellada, y lo dejo dicho.
- **El resultado** es la media por partida de las 40 semillas, con su intervalo del 95 % (`evalua_experimento_v6.boot`).
- **Comprobación:** con la misma cuenta que la sellada (dormida fuera de las casillas de dentro de su casa más de la mitad, días 1 a 10), salen las noches fuera del panel 2 del 161, que repite P28:
  - RG69r+voz: 4,7 / 6,5 / 6,0 / 8,1 / 7,7 %;
  - RG68r: 20,8 / 23,1 / 21,8 / 24,6 / 22,7 %.

**Las noches de cada sitio, por partida** (de todas las criaturas vivas; con 8 vivas, una partida tiene 320 noches).

| mundo | jugador | su casa | su puerta | casa ajena | puerta ajena | fuera | despierta |
|---|---|---|---|---|---|---|---|
| abundancia | RG68r | 259,0 | 0 | 0,4 | 0 | 48,8 | 11,9 |
| | RG69r+voz | 310,8 | 0,1 | 0,2 | 0 | 7,8 | 1,2 |
| normal | RG68r | 253,4 | 0,1 | 2,2 | 0 | 53,7 | 9,5 |
| | RG69r+voz | 302,3 | 0,3 | 0,6 | 0 | 14,8 | 2,2 |
| sequía | RG68r | 246,2 | 0,1 | 2,8 | 0,1 | 50,6 | 9,9 |
| | RG69r+voz | 293,9 | 0,2 | 1,5 | 0,0 | 17,4 | 4,0 |
| sequía dura | RG68r | 153,3 | 0,2 | 3,0 | 0,0 | 44,4 | 13,2 |
| | RG69r+voz | 183,6 | 0,3 | 2,2 | 0,1 | 24,9 | 9,4 |
| bestias que crían | RG68r | 226,0 | 0,3 | 4,6 | 0,1 | 54,6 | 10,4 |
| | RG69r+voz | 271,6 | 0,4 | 2,6 | 0,0 | 20,6 | 7,7 |

En la sequía dura hay menos noches porque mueren más. Los intervalos están en `salida/casas_noches_162.md`. Por ejemplo, RG69r+voz fuera en el normal: 14,78 [13,30, 16,43].

**Las hermanas en la misma casa.** «Noches de pareja» son las noches con las dos hermanas vivas al empezar; hay cuatro parejas por partida. Las medias son por partida.

| mundo | jugador | noches de pareja | en la misma casa | de ellas, no la suya |
|---|---|---|---|---|
| abundancia | RG68r | 160,0 | 111,7 (70 %) | 0,05 |
| | RG69r+voz | 160,0 | 151,4 (95 %) | 0,03 |
| normal | RG68r | 158,9 | 107,2 (67 %) | 0,40 |
| | RG69r+voz | 160,0 | 143,9 (90 %) | 0,05 |
| sequía | RG68r | 150,3 | 100,5 (67 %) | 0,57 |
| | RG69r+voz | 156,8 | 137,2 (88 %) | 0,38 |
| sequía dura | RG68r | 77,3 | 41,4 (54 %) | 0,40 |
| | RG69r+voz | 78,9 | 65,1 (83 %) | 0,10 |
| bestias que crían | RG68r | 138,7 | 87,9 (63 %) | 0,65 |
| | RG69r+voz | 145,3 | 121,8 (84 %) | 0,23 |

**Tres o más criaturas en una misma casa.** Se cuenta cada casa y cada noche, con el sitio de la noche de cada una.

| mundo | RG68r: por partida | partidas con alguna | RG69r+voz: por partida | partidas con alguna |
|---|---|---|---|---|
| abundancia | 0,28 [0,10, 0,50] | 8 de 40 | 0,15 [0,03, 0,30] | 5 de 40 |
| normal | 1,32 [0,93, 1,75] | 26 | 0,42 [0,20, 0,68] | 12 |
| sequía | 1,12 [0,72, 1,57] | 25 | 0,90 [0,62, 1,20] | 23 |
| sequía dura | 0,72 [0,47, 0,97] | 20 | 0,90 [0,62, 1,23] | 25 |
| bestias que crían | 2,20 [1,77, 2,67] | 36 | 1,60 [1,15, 2,10] | 31 |

**Pegada a la puerta de su casa, por fuera, con otra dormida en la puerta.**
- **Cómo se cuenta:** un turno cuenta si la criatura está viva, fuera de las casas, en una de las casillas de alrededor de la puerta de su casa (también en diagonal), y en esa puerta duerme otra.
- **«Una vez»** es una racha de turnos seguidos de la misma criatura.
- Se dice también cuántos de esos turnos está en la entrada, la única casilla desde la que podría entrar.

| mundo | jugador | veces, en las 40 partidas | turnos, en las 40 | de ellos en la entrada | partidas con alguna | la dormida es su hermana |
|---|---|---|---|---|---|---|
| abundancia | RG68r | 0 | 0 | 0 | 0 | — |
| | RG69r+voz | 0 | 0 | 0 | 0 | — |
| normal | RG68r | 0 | 0 | 0 | 0 | — |
| | RG69r+voz | 4 | 462 | 462 | 3 | todos |
| sequía | RG68r | 2 | 115 | 112 | 1 | ninguno |
| | RG69r+voz | 3 | 151 | 150 | 2 | todos |
| sequía dura | RG68r | 0 | 0 | 0 | 0 | — |
| | RG69r+voz | 5 | 103 | 99 | 2 | ninguno |
| bestias que crían | RG68r | 6 | 498 | 377 | 4 | todos |
| | RG69r+voz | 15 | 884 | 866 | 6 | 730 de 884 |

- **Por partida de media** es poco: de 0 a 0,38 veces. Los intervalos están en `salida/casas_noches_162.md`.
- **Se duermen en una puerta**, propia o ajena, sumando los cinco mundos: RG69r+voz 57 veces y RG68r 36, todas agotadas.

## Parte 3: la partida del GIF (sequía, semilla 30182)

Los días van contados del 1 al 40. La noche del día *d* son los turnos 400·(*d*−1)+280 a 400·(*d*−1)+399. Las de «dormida en una puerta» miran el anochecer y la noche (turnos 240 a 399 del día) y dicen desde qué turno duerme allí.

**RG69r+voz** (la del GIF del prompt 158):

| día | qué | casa | quiénes | turnos |
|---|---|---|---|---|
| 1 | dormida en una puerta, la de su casa | D | D1, que se durmió agotada en el turno 226 (acababa de empujar y llegó a cansancio 100) | 226 a 399 |
| 2 | tres en una casa | C | C1, C2 y B1 (B1 de otra casa) | noche: 680 a 799 |
| 9 | tres en una casa | C | C1, C2 y B2 (B2 de otra casa) | noche: 3.480 a 3.599 |
| 35 | tres en una casa | A | A1, A2 y B2 (B2 de otra casa) | noche: 13.880 a 13.999 |

La noche del día 1, D2 dormía dentro de la casa D, en la casilla (21, 29). No se quedó fuera.

**S69+voz:**

| día | qué | casa | quiénes | turnos |
|---|---|---|---|---|
| 3 | dormida en una puerta, la de su casa | C | C2, agotada al dormirse | 1.054 a 1.199 |

**P69+voz:**

| día | qué | casa | quiénes | turnos |
|---|---|---|---|---|
| 20 | tres en una casa | A | A1, A2 y D1 (D1 de otra casa) | noche: 7.880 a 7.999 |
| 29 | tres en una casa | A | A1, A2 y B1 (B1 de otra casa) | noche: 11.480 a 11.599 |

En las tres partidas no hay ninguna noche con cuatro o más en una casa.

## Parte 4: recuento de la figura de un día (normal, 30161, RG69r+voz, días 5 y 6)

**Cada criatura, cada noche** (los turnos 1.880-1.999 y 2.280-2.399, la fase «noche»). Se da la casilla donde duerme, cuántos turnos (de 120) y su terreno.

| criatura | noche del día 5 | noche del día 6 |
|---|---|---|
| A1 | casa A, (20, 22), 120 | casa A, (21, 20), 120 |
| A2 | casa A, (21, 21), 120 | casa A, (22, 20), 120 |
| B1 | **fuera, bosque (17, 30), 120** | **fuera, bosque (23, 15), 93** (despierta los otros 27) |
| B2 | casa B, (27, 20), 120 | casa B, (27, 20), 84: empieza la noche en el bosque y llega a casa ya de noche |
| C1 | casa C, (27, 27), 120 | casa C, (27, 27), 120 |
| C2 | casa C, (28, 28), 120 | casa C, (28, 28), 120 |
| D1 | casa D, (20, 28), 120 | casa D, (21, 28), 120 |
| D2 | **fuera, bosque (27, 35), 120** | casa D, (22, 27), 120 |

En el anochecer de esos días cada una ya duerme en la misma casilla que luego en la noche, salvo B1 y B2 el día 6, que no duermen en el anochecer. Está en `salida/casas_noches_162.json`, «un_dia».

**Cuál de las dos cosas es cierta: la de Manel.**
- La noche del día 5 duermen en el bosque **B1 y D2**.
- La noche del día 6 duerme en el bosque **B1** otra vez.
- El informe 161 se equivocaba al decir que solo B1 dormía fuera, y solo la noche del día 5. La figura estaba bien: lo mal leído era mi frase.
- Lo confirman los turnos en casa de esos dos días que guardó el 161 (`salida/figuras_v6_161.json`, «cuenta_sitios»): B1 solo pasó 6 de 800 turnos en una casa.

## Parte 5: las figuras del v6 para publicar

**Lo borrado** (`borra_cache_161.py`, solo lo que pedía Manel):
- Son los 1.200 ficheros de caché que escribió la pasada de figuras del 161 en `evalua_escalera_v6/experimento/{datos,noches,partidas}`: los de RG68r y RG69r, 200 por jugador y carpeta, todos del 20 de noviembre.
- Antes de borrar, el programa comprueba que son exactamente esos. Los demás de esas carpetas (RG69r+voz, S69+voz y P69+voz, del 19 de noviembre, de la escalera) no se tocan.
- No he borrado nada más. La caché de la parte 1 del 161 (`dias_cosecha_161/`) no entra en las figuras y la he dejado.
- Esas carpetas no están en git.

**Rehechas** con `figuras_v6_v2_162.py`, que importa las cuentas del 161 (`figuras_v6_161.py`) y las piezas selladas.
- **Antes de contar comprueba con asserts que las carpetas son las del experimento:**
  - `valle_experimento_v6` para los seis jugadores;
  - la de RG69r en la pieza de las noches (la que se colgó en el 161);
  - la del duelo;
  - y que las 1.200 partidas están acabadas.
- **Las cuentas se han vuelto a hacer desde las partidas selladas:** la caché borrada se ha escrito de nuevo, otra vez 1.200 ficheros.
- **Los cambios:**
  - **las leyendas, sin nombres de clase:** «el tonto», «el recolector», «la criatura de antes», «la gemela sin lado positivo» y «la criatura completa»; en las costumbres, «la criatura de antes», «con la reserva» y «con la reserva y la voz»;
  - **«días 0 a 9» pasa a «días 1 a 10»;**
  - **el duelo y la soledad:** el eje de los días con números enteros, uno por día, del −5 al 15;
  - **un día en el valle:**
    - sin el título de dentro;
    - el eje de abajo con las cuatro fases de cada día (mañana, tarde, anochecer y noche), cada una en su sitio según la config y comprobado con el registro;
    - «día 5 (con fruto)» y «día 6 (sin fruto)» debajo;
    - la raya entre los dos días, más gruesa.
  - **Un cambio que no pedía el prompt:** en «dónde está», la etiqueta «en otro sitio (camino, almacén, puerta)» pasa a «en un camino».
    - El almacén y las puertas del valle no se pisan (mundo:453), y la puerta de una casa es casilla de la casa.
    - El programa comprueba que todo lo que cae en ese color es camino.
- **Los ficheros:** `figuras/v6_A_vivas_v2`, `v6_B_costumbres_v2`, `v6_C_duelo_soledad_v2` y `v6_D_un_dia_v2`, en PNG y PDF. Los números van en `salida/figuras_v6_v2_162.json`.
- **Los números coinciden con los del 161.** El programa compara uno a uno con `salida/figuras_v6_161.json` 798 números (medias, intervalos, casos, controles, cuentas por día y cuentas de la figura del día): **0 distintos**.

## Parte 6: la historia de los sellados

*Esta parte la leyó y la escribió en borrador un agente de ayuda dentro de esta misma sesión, solo leyendo. Las citas que he comprobado yo, una a una, están en la parte 8.*

*Solo se han leído ficheros. Las fuentes van como `fichero:línea`, relativas a `cantera/paper8` salvo que se diga otra cosa, o como hash de commit. Fecha y commit de cada etiqueta: `git log -1 <etiqueta>`.*

### 1. Los experimentos sellados, del primero al último

**Qué cuenta como sellado.** Cuenta lo que tiene etiqueta propia en git, sus huellas en un fichero CONGELADO y sus predicciones escritas antes de jugar o de preguntar. Confirmación, dilemas y mesa lo cumplen las tres:
- cada una tiene su etiqueta (`valle-confirmacion-v1`, `valle-dilemas-v1`, `valle-mesa-v1`; `git tag -l`);
- cada una tiene su sección en `CONGELADO_P8.md:78`, `:98` y `:114`;
- sus predicciones se congelaron «tal cual» antes de jugar (`informe_confirmacion_v1.md:32-35`; `informe_dilemas_v1.md:46-50`) o, en la mesa, «antes de preguntar a ninguna criatura» (`informe_mesa_v1.md:40-44`).

La mesa v2 **no** es un experimento sellado: «Esto es exploración, sin predicciones» (`informe_mesa_v2.md:3`).

**Cómo se cuenta.** Solo cuentan las predicciones. No cuentan las medidas sin predicción (M1…, A1…), ni las que dicen «se informa» o «sin predicción». Ojo: en la mesa, M1 a M3 sí son predicciones (`predicciones_mesa.md:2-4`).

| # | experimento (etiqueta) | sellado | commit | semillas | jugadores | predicciones que cuentan | se cumplen | fallan |
|---|---|---|---|---|---|---|---|---|
| 1 | v1 (`valle-congelado-v1`) | 2-nov | `ccd88251` | 1001–1040; 1.200 partidas | 6: RG32r, RG032r, S32, S032, tonto, recolector (`predicciones_selladas.md:2`) | 14, contando P5a–P5f por separado (P3c y P4 «se informa») | 8 | P2a, P2b, P3b, P5b, P5c, P5f |
| 2 | confirmación (`valle-confirmacion-v1`) | 3-nov | `79afe666` | 2001–2040; 320 partidas | 5 en bestia de día (RG32r, S32, P32, RG032r, S032); 3 en sequía dura (RG32r, S32, P32) (`informe_confirmacion_v1.md:41-43`) | 6 (C1–C6) | 4 | C1, C4 |
| 3 | dilemas (`valle-dilemas-v1`) | 3-nov | `aa7fd4b1` | 3001–3040; 2.800 partidas cortas | 5: RG32r, S32, P32, RG032r, S032 (`informe_dilemas_v1.md:57`) | 3 (D1–D3) | 0 | D1, D2, D3 |
| 4 | mesa (`valle-mesa-v1`) | 3-nov | `caf63cda` | variantes 4001–4020; 3.600 preguntas, ninguna partida | los mismos 5 (`informe_mesa_v1.md:48`) | 3 (M1–M3) | 0 | M1, M2, M3 |
| 5 | v2 (`valle-congelado-v2`) | 7-nov | `af7605a5` (las predicciones, en `648475e6`) | 30001–30040; 1.400 | 7: RG50r, RG050r, S50, S050, P50, tonto, recolector | 12 (P1–P12) | 11 | P9 |
| 6 | v3 (`valle-congelado-v3`) | congelado el 9-nov; predicciones del 10-nov | `34bf8e78` (las predicciones, en `61276d6b`) | 30041–30080; 1.400 | 7: RG58r, RG058r, S58, S058, P58, tonto, recolector | 15 (P1–P15) | 10 | P9, P11, P12, P14, P15 |
| 7 | v4 (`valle-congelado-v4`) | 11-nov | `27b23137` | 30081–30120; 1.400 | 7: RG61r, RG061r, S61, S061, P61, tonto, recolector | 15 (P1–P13, P16, P17) | 14 | P17 |
| 8 | v5 (`valle-congelado-v5`) | 15-nov | `65ee6048` | 30121–30160; 1.600 | 8: RG68r, RG068r, S68, S068, P68, RG61r (de referencia), tonto, recolector | 21 (P1–P13, P16–P23) | 21 | ninguna |
| 9 | v6 (`valle-congelado-v6`) | texto del 17-nov; commit y subida del 18-nov a las 00:03 | `759acc39` | 30161–30200; 1.200 | 6: tonto, recolector, RG68r, RG068r, RG69r, RG69r+voz | 23 | 21 | P25, P31 |
| 10 | escalera (`valle-escalera-v6`) | 19-nov | `24cdb2db` | 30161–30200; 400 partidas nuevas | se juegan 2 (S69+voz y P69+voz); RG69r+voz se lee del v6 | 2 (E1, E2) | 1 | E2 |

**De dónde sale cada fila:**
- **v1:** el resultado de cada predicción está en `informe_experimento_v1.md:26-43` y coincide con `STATUS.md:459` (en la raíz del repositorio). Si P5 cuenta como **una** predicción de seis partes, son 9 y P5 no se cumple entera. El informe las pone una a una, así que aquí van 14.
- **Confirmación:** `informe_confirmacion_v1.md:91-100`.
- **Dilemas:** `informe_dilemas_v1.md:75-83`.
- **Mesa:** `informe_mesa_v1.md:56-58`.
- **v2:** `predicciones_selladas_v2.md:7-26`; «Se cumplen 11 de las 12. Falla P9» en `informe_experimento_v2.md:13` y `:55`.
- **v3:** `predicciones_selladas_v3.md:7-34`; `informe_experimento_v3.md:12-18`.
- **v4:** `predicciones_selladas_v4.md:9-40`; `informe_experimento_v4.md:8`.
- **v5:** `predicciones_selladas_v5.md:12-49`; `informe_experimento_v5.md:8`. El commit `c026955c` dice que P20 y P23 se cumplieron «por poco» en la sequía dura.
- **v6:** cuenta declarada en `predicciones_selladas_v6.md:67`: «P1 a P9, P12, P13 y P16 a P18 en la protagonista (14), P10, y P24 a P31 (8)». Resultado en `informe_experimento_v6.md:8` y `:102`.
- **Escalera:** «Cuentan dos» en `predicciones_selladas_v6_escalera.md:33`; `informe_escalera_v6.md:7-9`.

**Correcciones hechas después:**
- **v3, P9.** El informe dijo primero «se duerme en una puerta 172 veces» (`informe_experimento_v3.md:14`, `:57`). La fe de erratas del 11-nov (prompt 114) corrige la cuenta a 129 noches en una puerta. Con la cuenta arreglada, duerme dentro de casa entre el 65 % y el 76 % de las noches (`informe_experimento_v3.md:5-7`, `informe_diagnostico_v4.md:56`). **P9 sigue fallando** y el recuento no cambia: 10 de 15, como al principio y después de corregir.
- **v3, P11.** La misma fe de erratas corrige solo una frase («Igual que en el v2»). El resultado de P11 en el v3 no cambia (`informe_experimento_v3.md:6`; `informe_diagnostico_v4.md:38`).
- **v2, P11.** El informe dio −0,131 (`informe_experimento_v2.md:57`). Con la medida arreglada del prompt 101 salió −0,128 (`informe_diagnostico_v4.md:38`; commit `ca2e47fb`). Se cumple en los dos casos, así que el recuento del v2 no cambia.
- No he encontrado ninguna otra corrección de recuento en los informes del valle. Busqué «erratas», «es falso», «corrijo» y palabras parecidas en `informe_*.md`.

**Suma (es mía, no está en ningún fichero):**
- Contando P5 en seis partes: 114 predicciones en los 10 sellados, 90 cumplidas y 24 fallidas.
- Solo en los siete experimentos con partidas largas (v1–v6 y la escalera): 102 predicciones y 86 cumplidas.

### 2. Qué cambió de un sellado al siguiente, por qué, y con qué se decidió

- **Antes del v1.** La regla general se construyó en el taller, hasta RG32: «desde aquí, la regla general es RG32 y RG032» (`informe_regla_general_v27.md:73`). RG32r es RG32 con tres aceleraciones que no cambian ninguna decisión, «con las mismas partidas» (`informe_valorador_sumas_v2.md:7`; `banco_v7.py:155`). **Se decidió con partidas de taller.**
- **v1 → confirmación.** La criatura no cambia. Se añade P32, un valorador de posición, con un interruptor nuevo. Apagado, RG32r y S32 salen idénticas a las del experimento (`CONGELADO_P8.md:80`, `:84-85`, `:93`). Las predicciones «salen de la exploración del experimento principal y de la idea de Manel de la ambivalencia» (`predicciones_confirmacion.md:2`). **Se decidió con el sellado anterior** (su exploración).
- **Confirmación → dilemas → mesa.** La criatura no cambia. Las escenas y los estados solo ponen la situación de partida (`CONGELADO_P8.md:100`, `:116`). No hay decisión sobre la criatura.
- **Mesa → v2 (RG32r → RG50r).** El camino es largo: RG33r con «el para qué» y «la gravedad» (`informe_arreglos_v1.md:3`), y después los talleres v34 a v50, uno por commit, de `bb0ee02c` a `7917bfa2`. Entran:
  - el radar de tres dimensiones;
  - los sabores y el árbol;
  - la bestia que se echa y se mata;
  - los robos;
  - las noches.

  El arreglo 1 vuelve a hacer la pregunta de la mesa v2 y usa los registros del experimento v1 (`informe_arreglos_v1.md:60`, `:80-82`). En la mesa v2 ninguna clase iba a la hermana herida: 0 de 1.620 (`informe_mesa_v2.md:30-32`). RG50r se eligió con la tabla de cierre de taller y «los criterios de Manel» (`informe_cierre_v4.md:3`, `:66`; `CONGELADO_P8_v2.md:3`). **Las dos cosas:** el diagnóstico salió del sellado v1 y de la mesa; la elección, del taller.
- **v2 → v3 (RG50r → RG58r).** Cambia:
  - el gusto dulce se aprende;
  - «ir a casa» lleva dentro y no a la puerta;
  - dar lleva el gesto y lo que vale la otra;
  - la última comida o medicina cuesta;
  - devolver no es un gesto;
  - sin la regla `tope_dar`.

  Todo esto está en `CONGELADO_P8_v3.md:97-107`. Los errores del dulce y de la puerta se encontraron mirando las partidas selladas del v2 (`informe_fractal_acciones_v1.md:3`, `:11`, `:17`). La exploración del v2 miró por qué falló P9 (`informe_exploracion_v2.md:1-3`, `:87`). Los arreglos se probaron en talleres (arreglos v4 a v7 y cierre v5). Hubo tres intentos de congelar que no se congelaron, por bucles al dar (commits `4cebbdcf`, `563fb62d`, `50075c7d`). Manel eligió RG58r porque «RG60r todavía tenía un bucle de comida, y RG58r no tiene bucles» (`CONGELADO_P8_v3.md:5`). **Las dos cosas.**
- **v3 → v4 (RG58r → RG61r).** Cambian tres cosas de los robos (`CONGELADO_P8_v4.md:102-105`):
  - ganar un empujón no es un regalo;
  - el robo baja el trato con la ladrona;
  - quitar comida cuenta en el vínculo.

  La causa se encontró «solo con los datos del v3» (commit `5a3e9681`; `informe_diagnostico_v4.md:133-166`): la ladrona subía en el radar de la robada. Lo eligió Manel con una regla fijada antes del taller: ninguna muerte por golpe, ningún bucle nuevo de más de 10 y no vivir peor que RG58r (`CONGELADO_P8_v4.md:5`; `informe_arreglos_v8.md:7-11`). **Las dos cosas.**
- **v4 → v5 (RG61r → RG68r).** Se apagan «ven, lo necesito» y la voz de la que duerme (`CONGELADO_P8_v5.md:5-7`). Se decidió con talleres de la voz y de las piezas: commits `38e2adde` a `f33845c5`, en las semillas de taller 1001–1020 (`CONGELADO_P8_v5.md:135`). Ninguna pieza nueva pasó la regla, y la base quedó en M (`CONGELADO_P8_v5.md:9`). **Taller.** No he encontrado que se usaran los resultados sellados del v4 para esta decisión. El fallo P17 del v4 no se arregló: sigue como fallo conocido 18.
- **v5 → v6 (RG68r → RG69r+voz).** Se añaden dos cosas, cada una en una clase hija (`CONGELADO_P8_v6.md:5-8`):
  - la reserva, que deja comerse la comida de la bolsa sin que cuente como perderla;
  - la voz de ir a casa, solo entre hermanas.

  La causa salió del v5 sellado, solo mirando: hambre con comida en la bolsa y dormir fuera (`informe_hambre_ganancias_v1.md:4`; `informe_por_que_no_come_v1.md:4`; commits `e66de7d9` y `b164c02d`). Después se probó en tres talleres que pasaron su regla (`informe_voz_a_casa_v1.md:3-5`, `informe_reserva_v1.md:3-5`, `informe_voz_reserva_v1.md:3-5`). Esos talleres se jugaron en las semillas 30121–30140, que ya eran del v5 sellado (`predicciones_selladas_v6.md:75`). Manel eligió la protagonista (`CONGELADO_P8_v6.md:5`). **Las dos cosas.**
- **v6 → escalera.** La protagonista no cambia, y sus partidas se leen del v6 (`predicciones_selladas_v6_escalera.md:9`). Se añaden S69+voz y P69+voz: la misma clase, con otro valorador y sin código nuevo de criatura (`predicciones_selladas_v6_escalera.md:10-15`). La pregunta sale del efecto del v5, «medido sobre la base vieja», y del prompt 151 (`predicciones_selladas_v6_escalera.md:39`). **Sellados anteriores** (v5 y v6). No hay elección de criatura.

### 3. Cuántas versiones de la criatura hay

La respuesta depende de qué se cuente. Van las cuatro cuentas:

1. **Todos los nombres de `banco_v7.VARS`: 290.** Los conté leyendo las asignaciones de `banco_v7.py:16-312` sin importar el módulo. Están todos: gemelas sin ganancias (RG0…), sumas (S…), posición (P…), piezas sueltas (RG34r_B, RG47r_N, RG64r_A, RG67r_M, RG68r_cara…) y las viejas (COMPLETA3, V7…V24v). Desde RG32r en adelante hay 194. Antes de banco_v7 están COMPLETA4, COMPLETA5 y COMPLETA6 (`banco_v4.py:23`, `banco_v5.py:13`, `banco_v6.py:14`).
2. **La línea principal, con ganancias: 63 nombres en VARS, y 65 con las dos de fuera.**
   - 31 sin «r»: RG, RG2–RG9 y RG11–RG32.
   - 32 con «r»: RG32r–RG68r.
   - Los números 10, 35, 37, 62, 63 y 66 no se usaron nunca: no salen en ningún .py ni .md de `cantera/paper8`.
   - Fuera de VARS: RG69r y RG69r+voz se añaden al lanzar (`lanza_experimento_v6.py:33`), con las clases `cuerpo_rg69.py:17` y `cuerpo_vr1.py:11`. Eso hace 65.
   - Hay dos hijas más que no se sellaron: VC1, la voz sola (`cuerpo_vc1.py:44`), y RZ1, la razón (`cuerpo_rz1.py:77`).
3. **Entre la primera sellada (RG32r) y RG69r+voz, sin contar ninguna de las dos: 32.** Son RG33r…RG68r (31) más RG69r. Con VC1 son 33. Con los dos extremos, 34.
4. **Protagonistas selladas: 6.** RG32r, RG50r, RG58r, RG61r, RG68r y RG69r+voz. Con RG69r, que jugó sellada en el v6 sin ser protagonista, son 7 criaturas con ganancias selladas.

**Dudas sobre la cuenta:**
- Hay nombres distintos para la misma criatura:
  - RG32 y RG32r dan las mismas partidas (`informe_valorador_sumas_v2.md:7`);
  - RG67r_M, RG68r_M y RG68r llevan los mismos interruptores (`banco_v7.py:294`, `:299`, `:310`);
  - RG67r es RG61r (`informe_arreglos_v11.md`, punto 1).
- **«La primera del valle»** no está claro. Según se mire, puede ser:
  - las ocho del siete (`banco_cuerpo_valle.py:1`);
  - COMPLETA3 (`banco_v7.py:16`);
  - RG (`banco_v7.py:68`);
  - RG32r, la primera sellada.
- **La «r»** sí se puede saber: aparece en RG32r como `rapido_v28`, las aceleraciones (`banco_v7.py:155`; `ficha_valle_como_se_jugo.md:440`).

### 4. Fallos conocidos y declarados de la criatura sellada (RG69r+voz y lo que hereda)

**Los 23 fallos de saber de los CONGELADO** (cada versión hereda los de la anterior: `CONGELADO_P8_v5.md:126`, `CONGELADO_P8_v6.md:144`):
- **1–11** (desde el v2, `CONGELADO_P8_v2.md:137-147`; la versión vigente está en `CONGELADO_P8_v4.md:149-159`):
  - la foto no llega al árbol y vuelta (44 pasos);
  - el árbol se recuerda como un matorral;
  - no ve la vida de la bestia;
  - al empujar a la bestia cuenta como ayuda a las pegadas;
  - el tamaño de la bolsa (6) está escrito en la foto;
  - el hambre que supone a la otra: 80 si está flaca, 30 si no;
  - la pieza I está apagada, así que ve a la hermana más quieta de lo que está;
  - no conoce la cría de las bestias ni las épocas;
  - las épocas no se anuncian;
  - lo que cree de dormir fuera incluye toda la vida perdida dormida;
  - quedan empujones a quien no lleva nada (2–6 %).
- **12–15** (desde el v3, `CONGELADO_P8_v4.md:160-163`):
  - no sabe que de noche dormirá de un tirón;
  - llevar comida no vale nada para el cuerpo en la foto;
  - el paso solo rodea a otras al ir a casa;
  - quién le dio algo lo deduce de lo que ve, y se puede equivocar.
- **16** (v4, `CONGELADO_P8_v4.md:164`): se roba sin hambre, de 133 a 256 empujones por partida, y la ladrona todavía sube en el radar de la robada.
- **17** (v5, `CONGELADO_P8_v5.md:128`): el hambre media sube +0,93 frente a RG61r, y no se sabe por qué. En el v5 sellado salió +0,73 (`informe_experimento_v5.md:15`).
- **18** (v5, `CONGELADO_P8_v5.md:129`): **el bucle de regalos entre hermanas hartas.**
- **19** (v5, `CONGELADO_P8_v5.md:130`): la cara, la voz nueva, aprender de la cara y el «para» se probaron y están apagados en el código.
- **20** (v5, `CONGELADO_P8_v5.md:131`): sin «ven, lo necesito» no hay forma de pedir ayuda con la voz.
- **21** (v6, `CONGELADO_P8_v6.md:146`): RG69r sola vivió algo menos en la abundancia en el taller, por 3 muertes por la bestia, y no se ha mirado por qué.
- **22** (v6, `CONGELADO_P8_v6.md:147`): frente a la gemela RG068r, en la sequía dura, −0,30 en el taller.
- **23** (v6, `CONGELADO_P8_v6.md:148`): la voz es solo entre hermanas y solo despiertas.

**El bucle de regalos (P15 y P17), sellado tras sellado:**
- **v3:** falla P15, con una racha de 15 (`informe_experimento_v3.md:18`).
- **v4:** falla P17, con rachas de 89 y 29, intercambios a la vez entre hermanas sin hambre (`informe_experimento_v4.md:8-9`).
- **v5:** 1 de 200 partidas con racha de 24; como el umbral era 4 de 200, P17 se cumple (`informe_experimento_v5.md:16`).
- **v6:** 1 de 200, con racha de 15; P17 se cumple (`informe_experimento_v6.md:18`). RG68r, en el v6, tiene una de 30 (`informe_experimento_v6.md:111`).
- **No está arreglado:** el umbral de P17 se relajó en el v5, de «ninguna» a «4 o menos» (`predicciones_selladas_v5.md:41`).

**El apunte obligado del v3** (lo hereda todo lo que viene de RG58r): en bestias que crían, RG58r vive algo menos que RG55r, −0,62 [−1,19, −0,05], y «no lo he podido atribuir a nada» (`CONGELADO_P8_v3.md:5`, `:177-179`).

**Riesgos declarados antes de jugar el v6** (`predicciones_selladas_v6.md:69-75`), y cómo salieron (`informe_experimento_v6.md:104-109`):
- **P26 en la abundancia:** se cumplió justo en el límite, −0,07 [−0,17, +0,00] (`informe_experimento_v6.md:17`).
- **P4, justa:** dio 3,7 veces.
- **El hueco con la gemela:** P25 y P31 **fallaron**, «por el ruido, no por el signo» (`informe_experimento_v6.md:94`, `:100`, `:102`).
- **Las bestias que crían con la voz:** no se predijo dirección.
- **P24 a P31** salían de talleres en semillas ya vistas (30121–30140), así que su cumplimiento allí no contaba.

**Después del v6:** E2 falló en la escalera. En la sequía muere menos de hambre que S69+voz (3 frente a 11), pero más por la bestia (5 frente a 2) (`informe_escalera_v6.md:8`, `:38-40`). La ventaja sobre S69+voz bajó de +0,41 a +0,19, como se había declarado (`informe_escalera_v6.md:10`).

**Lo que no se puede saber con estos ficheros:**
- por qué sube el hambre (fallo 17: «No sabemos por qué»);
- por qué RG69r muere más por la bestia en la abundancia (fallo 21: «No se ha mirado»);
- a qué se debe el apunte del v3.

Los ficheros lo dicen así.

### Los ficheros y líneas que se leyeron para esta parte

- `predicciones_selladas.md` 1-16; `predicciones_confirmacion.md` 1-9; `predicciones_dilemas.md` 1-6; `predicciones_mesa.md` 1-5
- `predicciones_selladas_v2.md` 1-66; `_v3.md` 1-40; `_v4.md` 1-60; `_v5.md` 1-80; `_v6.md` 1-100 (y las cabeceras por grep); `_v6_escalera.md` 1-60
- `CONGELADO_P8.md` 1-25, 60-125; `_v2.md` 1-30, 84-157; `_v3.md` 1-30, 95-117, 135-183; `_v4.md` 1-10, 100-114, 147-188; `_v5.md` 1-12, 106-147; `_v6.md` 1-60, 122-165
- `informe_experimento_v1.md` 1-80; `_v2.md` 1-80; `_v3.md` 1-60; `_v4.md` 1-40; `_v5.md` 1-40; `_v6.md` 1-45, 94-115
- `informe_confirmacion_v1.md` 1-104; `informe_dilemas_v1.md` 40-83; `informe_mesa_v1.md` 1-58; `informe_mesa_v2.md` 1-34; `informe_escalera_v6.md` 1-40, 142-152
- `informe_diagnostico_v4.md` (grep de títulos; 38, 133-166); `informe_exploracion_v2.md` 1-6, 87-103; `informe_fractal_acciones_v1.md` 1-17; `informe_arreglos_v1.md` 1-15 (y grep); `informe_arreglos_v4.md` 1-22; `informe_arreglos_v8.md` 1-14; `informe_arreglos_v11.md` 1-25; `informe_cierre_v4.md` 1-30, 66; `informe_cierre_v5.md` 1-13, 104; `informe_valorador_sumas_v2.md` 1-20; `informe_regla_general_v27.md` 66-73
- primeras líneas de `informe_hambre_ganancias_v1.md`, `informe_por_que_no_come_v1.md`, `informe_dormir_fuera_causa_v1.md`, `informe_voz_a_casa_v1.md`, `informe_reserva_v1.md`, `informe_voz_reserva_v1.md`, `informe_preparacion_v6.md`, `informe_lectura_voz_v1.md`, `informe_voz_v1.md`, `informe_piezas_por_mundo_v1.md`
- `banco_v7.py` 1-15, 68, 153-164, 205-212, 296-312 (y todas sus asignaciones a VARS, leídas con `ast` sin importar el módulo); `banco_v4.py`, `banco_v5.py` y `banco_v6.py` (cabeceras y VARS); `lanza_experimento_v6.py` 3, 33-36; las líneas `class` de `cuerpo_*.py`; `ficha_valle_como_se_jugo.md` 440
- `STATUS.md` (raíz) 457-462; `git tag -l`, `git log -1` de cada etiqueta, y `git log` entre etiquetas (solo lectura)


## Parte 7: al anochecer y de noche, cómo elige dónde dormir

**Lo que tiene delante.** Cada vez que decide (si no sigue un destino o hace una llamada), sus opciones son las mismas que de día:
- **las acciones que le da el mundo** (mundo:571-601): quedarse, dormir (al anochecer y de noche siempre puede, mundo:541-542), un paso en cada dirección libre, coger, dejar, comer, dar, empujar y golpear;
  - sin hablar ni llamar (cv:2930-2931);
  - sin dormir si está en una puerta y no está agotada (cv:2933-2934);
- **los destinos de la criatura** (cv:2765-2838): ir al mejor objeto, al botín, a la hermana, a la medicina, a trabajar la planta más cercana, a casa (la suya), a la vecina que más lo necesita, a la bestia, a una llamada oída, a los matorrales recordados y al bosque no visto;
  - cada destino entra solo si su primer paso es válido (cv:2947-2950).

**Cómo imagina cada opción de noche.**
- Con `horizonte_v50` y `noche_entera_v18` (los dos encendidos), cada foto mira hasta la mañana (cv:2504-2515).
- **La foto** es lo que hace en la mirada de 44 turnos (`config_cuerpo_valle.json`: `tiempos_turnos.mirada`). Si es ir, son como mucho 44 pasos. Después imagina que se duerme **donde se ha quedado** hasta la mañana.
- **Para «dormir»**, toda la foto es dormir donde está (cv:2507).
- **Para «ir a casa»**, si llega en la foto, anda y duerme allí el resto (cv:2508).
- Elige la de menor malestar (cv:2978-2979), con los desempates de siempre (cv:2983-2995).

**Lo que la lleva a una casa: a cualquier casa.** En la foto, lo que cambia por acabar en una casa sirve igual en cualquiera (`todas_casas`, cv:226):
- **dormir fuera** le cuesta lo que dice su cuaderno que quita una noche dormida fuera, solo si acaba fuera de toda casa (cv:2519-2523);
- **el frío** cuenta en el hambre solo fuera de toda casa (cv:2532-2541);
- **la bestia** no la alcanza en ninguna casa (cv:1619-1620);
- **la anticipación de la noche** y el anillo no cuentan en ninguna casa (cv:901, 914).

**Lo que la lleva a su casa en concreto.**
- **La única opción que apunta a su casa** es «ir a casa», y solo existe para la suya (cv:2793-2798).
- **Las razones para elegirla son las de arriba**, iguales para cualquier casa. La foto de «ir a casa» gana por acabar en una casa, no por ser la suya.
- **Lo que tira de ella hacia su casa y no hacia otra** es la hermana:
  - **estar con las suyas** (S-JUNTAS) suma el vínculo mayor de las que tendrá a la vista al final de la foto (cv:1765-1769). De noche la vista es de 2 casillas (cfg: `criaturas.vista_por_fase`), y la hermana pesa más que una vecina;
  - **con la voz de ir a casa** (RG69r+voz), mientras la oye, imagina a la hermana dentro de su casa al final de la foto (vc1:7-9 y 53-58). Así, estar con ella es acabar en su casa.
- **La despensa** solo es de su casa (mundo:585-590), pero no hace que la foto de dormir allí sea mejor.

**En pocas palabras:** hay algo que la lleva a su casa en concreto, la opción «ir a casa» y la hermana imaginada en ella. Pero lo que hace buena esa opción de noche es acabar en una casa, cualquiera.
- Si una casa ajena queda más a mano por otra opción (ir a la hermana o a una vecina que está dentro), dormir allí le cuenta igual de bien para el frío, la bestia y la noche fuera.
- Es lo que se ve en las noches en casa ajena de la parte 2: pocas, pero las hay.
- No propongo esto como causa: es lo que dice el código.

## Parte 8: cierre

**Qué es análisis hecho después.**
- Las partes 2, 3 y 4 son recuentos hechos después de ver los datos, sin predicción. No propongo causas.
- La parte 7 dice lo que hace el código, no por qué salen así las noches.
- **Lo que repite una medida sellada:**
  - la cuenta de las noches fuera de los días 1 a 10 (la de P28), que sale igual que en lo sellado;
  - en la parte 5, todos los números de las figuras, que salen igual que en el 161: 798 de 798.

**Lo hecho.**
- **Los programas nuevos, todos de solo lectura:**
  - `casas_noches_162.py` (partes 2 a 4), con caché por partida en `casas_noches_162/`, fuera del commit;
  - `borra_cache_161.py` (parte 5, lo borrado);
  - `figuras_v6_v2_162.py` (parte 5, las figuras).
- **Las salidas:** `salida/casas_noches_162.md` y `.json`, y `salida/figuras_v6_v2_162.json`.
- **Las figuras:** las cuatro `_v2`, en PNG y PDF.
- No se ha jugado ninguna partida, no se ha tocado nada sellado y no se ha usado la clave.

**Lo que no se ha podido o queda dudoso.**
- **En la parte 6, «la primera criatura del valle»** no tiene una respuesta única. Por eso hay cuatro cuentas de versiones.
- **El total de 114 predicciones** es una suma mía que no está en ningún fichero.
- **No se puede saber** lo que los propios ficheros dicen que no se sabe: por qué sube el hambre (fallo 17), por qué RG69r muere más por la bestia en la abundancia (fallo 21) y a qué se debe el apunte del v3.

**Los tropiezos.**
- **Muertas que salen del registro:** la primera pasada de `casas_noches_162.py` paró porque una criatura muerta deja de aparecer en el registro del mundo. Lo arreglé contando como muerta a la que no está.
- **Un comentario mal puesto:** al arreglarlo, un comentario se comió dos variables, y la segunda pasada también paró. Las dos paradas fueron antes de escribir nada.
- **El informe 161 decía mal quién duerme fuera** en la figura de un día (parte 4). Lo corrijo aquí y no toco el informe 161.
- **Comandos sueltos**, ninguno de análisis:
  - lecturas cortas con `python3 -I` de JSON ya escritos, para ver tablas;
  - un `python3 -c` para probar una partida;
  - una mirada al registro de D1 el día 1 de la partida del GIF;
  - dos ediciones de mis propios ficheros con un `python3` en la terminal.

**Las citas que he comprobado yo.**
- **Partes 1 y 7, leídas yo en el código** (con un `grep -n` de las líneas al final):
  - mundo:18, 66-68, 103-119, 129, 138-140, 153-164, 195-197, 238, 446-458, 463, 479-484, 536-544, 571-601, 676-690, 740-760, 1017-1035, 1149, 1154;
  - cv:215-226, 460-467, 780-792, 896-920, 1612-1640, 1750-1769, 2490-2560, 2735-2810, 2844-2869, 2920-2995;
  - vc1:1-120;
  - jug:35-42;
  - la config del mundo (casas, criaturas, días) y `tiempos_turnos.mirada` de `config_cuerpo_valle.json`.
- **Parte 2:** la definición de la noche, en `dormir_fuera_v5/noches_v5.py:20-75`.
- **Parte 6, las que he comprobado a mano una a una:**
  - las diez etiquetas (`git tag -l`);
  - `informe_experimento_v1.md:26-43`;
  - `predicciones_selladas_v6.md:67` y `:75`;
  - `CONGELADO_P8.md:78`, `:98` y `:114`;
  - `CONGELADO_P8_v6.md:144-148`;
  - `predicciones_selladas_v5.md:41`;
  - `CONGELADO_P8_v3.md:5`;
  - `banco_v7.py:155`;
  - y el recuento de cumplidas que ya había leído yo por grep: v1, confirmación, dilemas, mesa, v2 a v6 y escalera (`informe_*` y sus líneas de «se cumple» y «falla»).
- **Parte 6, las que no he comprobado:**
  - las demás de esa parte (los pasos de un sellado a otro, los commits que cita y los fallos 1 a 20 uno a uno), que vienen del borrador del agente;
  - la cuenta de 290 nombres de `banco_v7.VARS`.

**Gasto:** 0 créditos de la plataforma y 0 dólares de la consola de Anthropic. No he leído los saldos.
