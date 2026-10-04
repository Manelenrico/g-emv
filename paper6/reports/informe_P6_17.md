# P6-17 · El final de la partida por dentro: ruido, palancas y las estrategias de Manel

*27-sep-2026. Coste cero: solo los 120 diarios de A4, A5v y A5h (60 partidas,
las mismas 20 semillas) y el `player_config`. Nada jugado, nada construido.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final;
los 202 congelados del cinco y los 32 del seis: 0 alterados al principio y al
final. Medidor: `mide_final_P6_17.py` (solo lectura, una partida cada vez);
datos: `P6_17_final.json`, `P6_17_salidas.json`. Sin propuestas de diseño.*

**Regla de parada, fijada antes:** el informe dice, con números, qué
estrategias tienen sitio claro en los datos; si ninguna lo tiene, el anillo se
cierra. El veredicto está en §7.

---

## 0 · LA RESPUESTA EN UNA LÍNEA

Con 20 semillas **nada de lo que separa A4, A5v y A5h en supervivientes,
muertes por rival o por anillo sale del ruido** (p de permutación 0,25-1,00;
el efecto detectable es de ±10 vidas en supervivientes y ±11 en anillo por 40
vidas). En el final de la partida lo único que decide es **entrar y
quedarse**: quien no entra en el círculo muere siempre (0 de 28 en las fases
5 y 6), entrar antes o después no cambia nada (63-83 %), ir junto o solo
tampoco (57 contra 53 % en la fase 5), y los 63 planes que llegaron dentro
salieron a los **11 tics** por el pie del cuerpo (`ir_objeto` 26, `move` 27,
`ir_pareja` 9): 44 de esos 65 murieron por el anillo. De las cuatro
estrategias, dos tienen sitio en los datos: **quedarse** (sitio grande: 0 %
contra 56-70 %, n 28 y 87) y **defensa conjunta** (sitio mediano: con los dos
pegando el agresor muere en 40 % de los casos y el golpeado en 3 %; con
ninguno, 1 % y 18 %; n 77 y 115; y en 167 golpes el hermano armado a ≤ 3 no
pegó). «Salir y volver» tiene margen aritmético en 30 de 62 muertes por
anillo, pero curarse fuera no funciona (+3,7 de vida contra +11,9 dentro) y
el hueco es de rivales *vistos*. «Entrar juntos» no tiene sitio.

---

## 1 · RUIDO: ¿CABE A5v−A4 EN LA VARIACIÓN NORMAL?

Por semilla (20), diferencias emparejadas A5x − A4 de lo que cuenta cada
partida (2 vidas): test exacto de permutación por cambio de signo (2²⁰) e IC
95 % por remuestreo (10.000). «Efecto detectable» = 2·sd/√20, lo que haría
falta para verlo con 20 semillas.

| medida (por partida) | A5v − A4: media (total) · p · IC 95 % | A5h − A4: media (total) · p · IC 95 % | A5h − A5v: media · p | sd de la diferencia | **efecto detectable (2 sd)** |
|---|---|---|---|---|---|
| supervivientes (0-2) | −0,25 (−5) · **0,43** · [−0,75, +0,25] | −0,30 (−6) · 0,25 · [−0,70, +0,10] | −0,05 · 1,00 | 0,9-1,1 | **±0,49 por partida = ±10 de 40 vidas** |
| muertes por rival | +0,15 (+3) · **0,56** · [−0,15, +0,45] | +0,30 (+6) · 0,31 · [−0,15, +0,75] | +0,15 · 0,68 | 0,7-1,1 | ±0,33-0,47 = **±6-9 vidas** |
| muertes por anillo | −0,05 (−1) · 1,00 · [−0,60, +0,50] | −0,15 (−3) · 0,66 · [−0,55, +0,30] | −0,10 · 0,85 | 1,0-1,2 | **±11 vidas** |
| vida (suma de las dos) | +689 (+13.789) · 0,88 · [−960, +3.301] | −56 · 0,96 · [−2.550, +2.898] | −745 · 0,36 | 5.166-6.061 | ±2.310-2.711 tics por partida |
| los dos vivos al final | −0,10 (−2) · 0,63 · [−0,30, +0,10] | −0,10 · 0,63 | 0 · 1,00 | 0,44 | ±0,20 = ±4 parejas |

**Cabe todo.** A5v, que cambió 3 decisiones de 508.000, pierde 5
supervivientes y gana 3 muertes por rival respecto a A4: p 0,43 y 0,56; el IC
de supervivientes va de −15 a +5 vidas. Con esta misma sd, en P6-11 el
«+39 emparejado» de vida de A4 sobre A3 y los «11 supervivientes» también
estaban dentro del ruido (la vida detectable es ±1.150 tics por vida).

**El retraso del tic de propuesta.** A5v: 631 tics lentos (> 41,7 ms) de
508.159; de sus 9 muertes por rival, **2** ocurren a ≤ 60 tics de un tic
lento (esperadas al azar 0,29): `21727122` s11 (24 tics después) y `22250767`
s11 (24 tics). A5h: 531 de 493.258; 1 de 12 (17 tics; esperadas 0,34). Es
más de lo que da el azar, pero son 3 casos: no se puede afirmar ni descartar
que el retraso costara esas vidas. Ninguna muerte por anillo cae a ≤ 60 tics
de un tic lento.

**Qué es usable con 20 semillas:** las diferencias de decenas de puntos en
porcentajes de tics (juntos, filas encendidas: cientos de miles de tics por
brazo) y los recuentos de planes (cientos). **No es usable** ninguna
diferencia de supervivientes, muertes por rival o por anillo menor de ~10
vidas, ni de vida menor de ~1.150 tics por vida, ni de «los dos vivos» menor
de 4 parejas. Los brazos A5v y A5h no han movido ninguna de esas cuatro.

---

## 2 · ANATOMÍA DEL FINAL

Para cada vida viva en el `warn` de cada fase (los tres brazos juntos, n por
celda; «pocos» = n < 5). «Dentro» = distancia al centro ≤ r1 de la fase;
«junto» = hermano a ≤ 3 en el `warn`; rivales dentro del círculo = los vistos
por cualquiera de los dos (cota inferior).

### Fase 5 (11.856 → 12.636, radio 8 → 5, daño 8/s): n 105, sobreviven 59 (56 %)

| | sobreviven / n | % |
|---|---|---|
| **cuándo entra:** antes de `shrink` | 27 / 40 | 67,5 |
| durante el encogimiento | 22 / 35 | 62,9 |
| después de `done` | 10 / 12 | 83,3 |
| **nunca entra** | **0 / 18** | **0** |
| ya dentro en el `warn` | 20 / 31 | 64,5 |
| fuera en el `warn` | 39 / 74 | 52,7 |
| **junto** en el `warn` | 40 / 70 | 57,1 |
| solo, hermano vivo | 17 / 32 | 53,1 |
| solo, hermano muerto | 2 / 3 | (pocos) |
| junto ≥ 50 % de la fase | 40 / 68 | 58,8 |
| junto < 50 % | 17 / 34 | 50,0 |
| rivales a ≤ 5 al entrar: 1-2 | 16 / 24 | 66,7 |
| ≥ 3 | 42 / 62 | 67,7 |
| armados dentro al entrar: 0 | 4 / 10 | 40,0 |
| 1-2 | 48 / 66 | 72,7 |
| ≥ 3 | 7 / 11 | 63,6 |
| tics ardiendo en la fase: 0 | 15 / 19 | 78,9 |
| 1-100 | 9 / 14 | 64,3 |
| > 100 | 35 / 72 | 48,6 |
| entra antes · junto / solo | 19 / 28 · 8 / 12 | 67,9 / 66,7 |
| entra durante · junto / solo | 15 / 25 · 7 / 10 | 60,0 / 70,0 |

Muertes en la fase 5: **anillo 37, rival 8**, no consta 1; **39 de las 46
mueren fuera del radio**. Quién mata: el anillo; los rivales, 8 (armas en
`P6_17_final.json → anatomia.armas_agresores`).

Por brazo (fase 5): A4 21/35, A5v 21/36, A5h 17/34; «nunca entra» 0/6 en
los tres; junto A4 16/24 (67 %) contra solo 4/10; A5v 14/26 (54 %) contra
6/8; A5h 10/20 (50 %) contra 7/14: **la ventaja de ir junto cambia de signo
según el brazo** (n 8-14 en las celdas de «solo»).

### Fase 6 (12.996 → 13.776, radio 5 → 3, daño 16/s): n 57, sobreviven 33 (58 %)

| | sobreviven / n | % |
|---|---|---|
| entra antes de `shrink` | 30 / 43 | 69,8 |
| durante | 3 / 4 | (pocos) |
| **nunca entra** | **0 / 10** | **0** |
| dentro en el `warn` | 7 / 8 | 87,5 |
| junto | 17 / 26 | 65,4 |
| solo, hermano vivo | 4 / 10 | 40,0 |
| solo, hermano muerto | 12 / 21 | 57,1 |
| tics ardiendo: 0 / 1-100 / > 100 | 12/14 · 19/36 · 2/7 | 85,7 / 52,8 / 28,6 |

Muertes en la fase 6: anillo 15, rival 5, no consta 4; 22 de 24 fuera del
radio. (Fase 4, n 116: sobreviven 105; nunca entra 0/2; junto 72/76 = 95 %,
solo 33/40 = 83 %.)

**Lo que sale:** (1) **entrar** es lo único necesario (0 de 28 sin entrar,
en dos fases); (2) **cuándo** se entra no cambia la supervivencia (63-83 %,
n 12-43); (3) **junto o solo**, nada en la fase 5 (57 contra 53, n 70/32) y
+25 puntos en la fase 6 con n 10 en «solo vivo»; (4) **rivales cerca o
armados** al entrar, nada (67 contra 68; 73 contra 64); (5) lo que sí separa
es **arder**: 0 tics ardiendo → 79-86 %, > 100 tics → 29-49 %.

---

## 3 · LLEGAR NO ES QUEDARSE: LOS 65 PLANES ANDADOS DE A5h

65 planes cumplidos (37 «a salvo», 28 en el destino), hp 60 de mediana al
llegar, hermano a 1-3 casillas en 32 (desconocido/muerto en 22), 1-2 rivales
vistos a ≤ 5 en 39.

| | |
|---|---|
| se quedan dentro hasta el final de la partida | **2 de 65** |
| tics dentro tras llegar: p10 · mediana · p90 · máx | 11 · **12** · 66 · 231 |
| salen | 63; llegan a 4,1 casillas del centro y salen a 5,4 (radio 3-10) |
| el paso que los saca (último movimiento antes de salir) | `ir_objeto` 26 · `move_*`/`paso_*` 27 · `ir_pareja` 9 · `ir_botin` 1 |
| lo que sentía el cuerpo al salir (filas `ahora`, media de M y n) | R-CARENCIA 0,65 (62) · F-DANO 0,55 (47) · F-4-ALCANCE 0,48 (61) · S-MUERTE-PAREJA 0,93 (22) · S-8 0,25 (32) · F-ANTICIPACION 0,21 (25) · R-LLAMADA 0,18 (45) · R-ACOPIO 0,18 (32) |
| qué le pegó después (100 tics tras salir) | anillo en 45; rival en 12 |
| de qué murió | **55 de 65**: anillo 44 · rival 6 · no consta 5; mediana 412 tics después de llegar |

El paso de salida se toma a los 11 tics de llegar (el primer enfriamiento):
el plan ha terminado y el decisor vuelve a lo suyo, que es **la carencia**
(R-CARENCIA 0,65, `ir_objeto` 26) o **el hermano** (`ir_pareja` 9,
S-MUERTE-PAREJA 0,93 en 22: el hermano acaba de morir o está lejos). Las
filas por candidato del detalle (cada 24 tics) no alcanzan el tic del paso:
el detalle más cercano es `noop` en 59 de 63, y la diferencia elegido − noop
es 0,00 en todas las filas. La causa está en el tic sin detalle: se declara.

---

## 4 · ESTRATEGIA «SALIR AL FUEGO Y VOLVER»

### 4.1 El daño del fuego, del `player_config` (tick_rate 24)

| fase | tics | radio | daño/s | **por tic** | aguanta con 100 · 60 · 30 de vida (tics) |
|---|---|---|---|---|---|
| 1 | 7.296-8.076 | 24 → 19 | 1 | 0,042 | 2.400 · 1.440 · 720 |
| 2 | 8.436-9.216 | 19 → 15 | 2 | 0,083 | 1.200 · 720 · 360 |
| 3 | 9.576-10.356 | 15 → 11 | 4 | 0,167 | 600 · 360 · 180 |
| 4 | 10.716-11.496 | 11 → 8 | 6 | 0,25 | 400 · 240 · 120 |
| **5** | 11.856-12.636 | 8 → 5 | 8 | **0,333** | **300 · 180 · 90** |
| 6 | 12.996-13.776 | 5 → 3 | 16 | 0,667 | 150 · 90 · 45 |
| 7 | 14.136-14.916 | 3 → 0 | 24 | 1,0 | 100 · 60 · 30 |

### 4.2 ¿Se puede curar fuera?

325 usos de botiquín/ración (`elegido usar_*`, resultado `ok`) en los tres
brazos; **146 fuera del radio** (A4 54, A5v 62, A5h 30): la vida sube en
**29** (ración 19 de 33; **botiquín 10 de 113**); en los 101 usos con todo el
canal fuera, sube en 12. Ganancia media de vida en el canal: **+3,7 fuera
contra +11,9 dentro**. El botiquín (50 en 48 tics) no compensa el fuego de
las fases 5-7 (16-48 en 48 tics) más lo que ya se pierde; la ración (15 en
24 tics) a veces sí. Curarse fuera no es una palanca.

### 4.3 Las 62 muertes por anillo (A4 22, A5v 21, A5h 19)

«Sale» = último tic dentro del radio antes de la racha final; «aguante» =
vida al salir / daño por tic; «hueco» = primer tic fuera con menos rivales
vistos dentro del círculo que al salir; «vacío» = ninguno visto; «margen» =
aguante − (tics hasta el hueco + pasos·11 de vuelta).

| | todos | A4 | A5v | A5h |
|---|---|---|---|---|
| vida al salir: mediana · ≥ 60 / 30-60 / < 30 | **46** · 28 / 11 / 23 | 65 | 40 | 33 |
| tics fuera hasta morir, mediana | 149 | 238 | 97 | 123 |
| aguante teórico, mediana | 110 | | | |
| rivales vistos dentro al salir: 0 / 1 / 2 / 3 / ≥ 4 | 6 / 12 / 14 / 12 / 18 | | | |
| con hueco (menos rivales) · **con margen** | 43 · **30 (48 %)** | 14 · 11 | 15 · 10 | 14 · 9 |
| con vacío · con margen | 37 · 26 | 14 · 10 | 14 · 9 | 9 · 7 |
| golpes de rival fuera (media) · curas fuera | 0,3 · 67 | 0,8 · 25 | 0 · 38 | 0 · 4 |
| hermano vivo al salir | 43 | 17 | 12 | 14 |

Los márgenes en el hueco: 13 negativos (−72 a −9) y 30 positivos, mediana
+106 tics. **Conclusión:** en **30 de las 62** muertes por anillo (11 de 22 en
A4) una salida con la cuenta hecha —«aguanto Z, vuelvo en el hueco»— tenía
margen aritmético; en 19 no había hueco y en 13 el hueco llegaba tarde. Dos
salvedades que pesan: el hueco se mide con los rivales *vistos* por los dos
hermanos (en 6 salidas no se veía ninguno dentro), y en 23 de 62 el cuerpo
salió ya con menos de 30 de vida (aguante < 90 tics en la fase 5).

---

## 5 · ESTRATEGIA «DEFENSA CONJUNTA»

Evento = un rival R golpea a un hermano en el tic t **con el otro a ≤ 3
casillas** (posiciones reales de los dos diarios). «Pega» = `elegido atacar_d`
con R en esa línea a ≤ alcance del arma en mano, en los 48 tics siguientes.
325 eventos (A4 112, A5v 97, A5h 116).

| | n | el agresor muere en 200 tics | deja de pegar en 24 tics | se va en 100 | **el golpeado muere en 100** | arma media golpeado / hermano (daño) |
|---|---|---|---|---|---|---|
| **pegan los dos** | 77 | **31 (40 %)**, mediana 85 tics | 41 | 8 | **2 (3 %)** | 13,6 / 13,7 |
| los dos a la vez (≤ 24 tics) | 72 | 30 (42 %) | 38 | 8 | 2 | |
| pega solo uno (el golpeado 110, el hermano 23) | 133 | 22 (17 %), mediana 45 | 87 | 21 | 10 (8 %) | 11,2 / 12,0 |
| **no pega ninguno** | 115 | **1 (1 %)** | 73 | 12 | **21 (18 %)** | 3,6 / 10,8 |
| el hermano pega | 100 | 35 (35 %) | 54 | 9 | 3 | |
| **el hermano no pega** | **225** | 19 (8 %) | 147 | 32 | 30 (13 %) | |

El hermano cercano pega en **100 de 325** (31 %); en los 225 en que no pega,
iba **armado en 167** (74 %) y el golpeado en 141. Cuando no pega ninguno, el
golpeado iba sin arma en 78 de 115. Armas del agresor: `none` (mano vacía)
en 161 de 325; espada 50, lanza 72, cuchillos 22, arco 9, cerbatana 10.

**Las filas que deciden hoy si el hermano cercano pega.** En los detalles
(cada 24 tics) con un `atacar_*` hacia el agresor disponible y ataque listo:
el hermano lo eligió en 37 y eligió otra cosa en 38. Cuando NO pega
(elegido − atacar, media de M): **F-REENCUENTRO −0,12, S-HERIDO −0,11,
S-8-EXPOSICION −0,10**, S-DANO-PAREJA −0,04, R-ACOPIO −0,04 (lo elegido
baja el reencuentro, la herida propia y la exposición: se acerca al hermano
o se aparta); S-7-AGRESOR +0,04 (atacar lo bajaría). Cuando SÍ pega (atacar −
noop): S-7-AGRESOR −0,026, F-HERMANO-GOLPE −0,021: pega cuando el agresor es
suyo o acaba de golpear al hermano.

Salvedad: los 77 «pegan los dos» se seleccionan solos (pareja armada, agresor
a tiro); el 40 % contra 1 % es asociación, no efecto.

---

## 6 · «ENTRAR JUNTOS CUBRIÉNDOSE» Y «QUEDARSE», dicho explícitamente

- **Supervivencia dentro.** Fase 5: entra 59/87 = **68 %**; no entra **0/18**.
  Fase 6: 33/47 = **70 %**; no entra **0/10**. Con 0 tics ardiendo en la
  fase, 79-86 %; con más de 100, 29-49 %.
- **Junto contra separado.** Fase 5: junto 57 % (n 70), solo con hermano vivo
  53 % (n 32): 4 puntos, dentro del ruido; por brazo el signo cambia (A4 +27,
  A5v −21, A5h 0; n 8-14). Fase 6: 65 % (n 26) contra 40 % (n 10): 25 puntos
  con n 10. Entrar antes y junto 68 %, antes y solo 67 %.
- **Quedarse contra salir.** Los 65 planes que llegaron dentro: 2 se quedan
  (uno sobrevive, `20679832` s10; el otro, `21412935` s11, muere por un rival
  dentro a los 74 tics), 63 salen a los 11 tics de mediana y **44 mueren por el
  anillo**. Las 62 muertes por anillo: todas salieron (mediana 149 tics
  fuera) y 39 de las 46 de la fase 5 mueren fuera del radio.

---

## 7 · VEREDICTO (sin propuestas de diseño)

| estrategia | ¿sitio en los datos? | cuánto · n | lo que lo limita |
|---|---|---|---|
| **Quedarse** (entrar y no salir) | **Sí, grande** | no entrar: 0 % (n 28); entrar: 68-70 % (n 87 y 47); 0 tics ardiendo: 79-86 % (n 19 y 14); los 63 planes que salieron: 44 muertos por anillo | el cuerpo sale por la carencia (`ir_objeto`, R-CARENCIA 0,65) y por el hermano (`ir_pareja`, S-MUERTE-PAREJA); es asociación: quien no arde puede ser quien ya iba bien |
| **Defensa conjunta** | **Sí, mediano** | pegan los dos: agresor muere 40 %, golpeado muere 3 % (n 77); ninguno: 1 % y 18 % (n 115); el hermano armado a ≤ 3 no pega en 167 golpes | autoselección (parejas armadas); las filas que hoy lo frenan: F-REENCUENTRO, S-HERIDO, S-8 (38 detalles); 161 de 325 agresores van con la mano vacía |
| Salir al fuego y volver | Aritmético, no medido | 30 de 62 muertes por anillo con margen en el hueco (A4 11/22); mediana +106 tics | el hueco es de rivales *vistos*; 23 de 62 salen ya con < 30 de vida; curarse fuera no funciona (+3,7); nadie lo ha hecho en 60 partidas: no hay datos de vuelta |
| Entrar juntos cubriéndose | **No** | junto 57 % contra solo 53 % (fase 5, n 70/32); por brazo cambia de signo; rivales cerca al entrar no cambia nada (67 contra 68) | n de «solo» 8-14 por brazo; la fase 6 da +25 puntos con n 10 |

Regla de parada: **hay sitio** (quedarse, defensa conjunta). El anillo no se
cierra por falta de datos; lo que no cabe en 20 semillas es medir vidas: los
efectos de menos de ~10 vidas de 40 no se ven.

---

## 8 · ARCHIVOS

| archivo | qué es |
|---|---|
| `mide_final_P6_17.py` | el medidor (secciones 1-5; una partida cada vez) |
| `P6_17_final.json` | ruido (por semilla, emparejado, tics lentos), anatomía por vida y fase, cruces, andados, curaciones, salidas al fuego, eventos de defensa y filas |
| `P6_17_salidas.json` | los 63 planes andados que salieron: posiciones, el paso que los sacó, el detalle más cercano |
