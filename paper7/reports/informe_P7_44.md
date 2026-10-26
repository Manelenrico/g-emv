# P7-44 · ¿El camuflaje protege?

> **Fe de erratas (13-oct-2026, revisión de Ari, autor del mundo; `obs.nim:32-44`)**: el camuflaje no «oculta más allá de 4/7 casillas»: LIMITA la distancia a la que te ven a 4 casillas (quieta) o 7 (si te has movido en los últimos 24 instantes), frente a 8 o más normalmente; atacar lo delata durante 5 s. Lo medido y los veredictos no cambian; cambia el enunciado de la regla donde aparece en este informe.

*11-oct-2026. Banco, coste cero (plataforma 0 créditos; consola 0); nada cambia en el campo en marcha. Datos: los diarios que ya existen: P7-34 (240 vidas), piloto 1 de
P7-42 (190 vidas) y piloto 2 (24 vidas); TECHO incluido. 452 vidas leídas, 165 con el camuflaje puesto en algún tic. Script `analiza_P7_44.py` → `P7_44_datos.json`;
este informe lo escribe `escribe_informe_P7_44.py` (ninguna cifra a mano). La serie 1 del campo (P7-42) no ha cerrado al escribir esto: no entra.*

## Sección 2 · Qué dice el juego del camuflaje (y de la red)

- **Especificación**: `paintball_recon/docs/zero-sum/README.md:50-52`: *«Gear: backpack (2 -> 4 pack slots), camouflage (undetected beyond 4 tiles standing / 7 moving
  until you attack), first-aid kit (50 HP, 2 s channel, cancelled by any damage), rations (15 HP)»*. Y `protocol_player.md:73-75`: *«Fog: visible.* is line-of-sight
  limited by your INT vision radius; walls, rocks, and the Fortress block sight. Camouflaged agents are absent unless within their detection cap or revealed by attacking»*.
  Es decir: el camuflaje oculta al que lo lleva a los demás contendientes más allá de 4 casillas si está quieto y de 7 si se mueve, hasta que ataca; al atacar queda delatado
  un tiempo (`sim.nim:917, 935, 943`: `a.camoRevealedUntil = s.tick + CamoRevealTicks` en los tres golpes: cuerpo a cuerpo, proyectil, lanzado); la constante
  `CamoRevealTicks` **no está en la copia de la fuente que tenemos** (`paintball/exposicion_liga_acta.md:56`: declarada [impl] de 5 s en el cuerpo). Duración del camuflaje:
  no caduca (es una prenda: va en `body` hasta que se cambia o se muere; `sim.nim` no le da durabilidad). Se obtiene como botín de nivel 1 en la cámara de la Fortaleza
  (`README.md:44-45`: *«Tier-1 loot (swords, bow, blowgun, camo) is deep in the Fortress chamber»*; `sim.nim:476`: `s.dropGround(t1[5], iCamo, 1)`).
- **La red**, en una línea (punto 4): `README.md:50`: *«net (immobilizes 3 s)»*; se lanza desde la mano (`protocol_player.md:120-121`: *«knives/net throw from your hand stack»*)
  y deja al alcanzado sin poder moverse (`sim.nim:983-984`: `nettedUntil = s.tick + NetTicks`; `sim.nim:618`: no se mueve mientras `tick < nettedUntil`).

## Sección 3 · Cómo valora TECHO el camuflaje, y de dónde sale

TECHO nace sabiendo (`GEMV_P7_SABE=1`): el cuerpo congelado de paper seis, sin las piezas de nacer. Dos sitios, los dos en `paintball/alma/appraisal_zs_v42_exp.py`:
1. **La riqueza W** (lo que vale lo que lleva): `GEAR_MENOR_W = 0.25` **[impl]** (línea 413: *«camuflaje / red»*), sumado en `riqueza_W` si el cuerpo lleva el camuflaje puesto
   (líneas 761-763) o la red en la mano o el zurrón (764-767); frente a `W_TARGET = 3.0` [Manel] (arma + botiquín + ración, línea 126): el camuflaje vale un cuarto de una
   de esas tres cosas, y la red otro cuarto. No sale de ninguna medida: es una constante declarada [impl].
2. **La exposición S-8** (líneas 1393-1420): con el camuflaje puesto y sin haber atacado en los últimos `CAMO_REVELADO_S = 5` s [impl], un hostil a más de `CAMO_QUIETO = 4`
   casillas (quieto) o `CAMO_MOVIENDO = 7` (moviéndose) **no me ve** y no suma exposición (`tope_camo`, línea 1410). Estos dos topes están **certificados** del README del
   mundo (líneas 403-406 del cuerpo: *«CERTIFICADO, no [impl]»*). Así que para TECHO el camuflaje vale 0,25 de riqueza y, sobre todo, menos miedo a los hostiles lejanos.
En P7-33/34 (nacer sin saber), estas dos entradas se borraron para APRENDE/BORRADO y las ganas pasaron a lo aprendido (k_gear); TECHO las conserva.

## Sección 1 · Lo medido: con el camuflaje puesto y sin él

Por tic vivo: estado (puesto sin delatar / puesto y delatado tras atacar, efecto `camo_revealed` / sin camuflaje), situación (dentro o fuera del anillo × rival a 8 casillas o
menos a la vista). Golpes = `damage_taken` con fuente un rival; «nos persiguen» = rivales a 6 o menos cuya distancia ha bajado respecto a 24 tics antes. Fracción de tics con
el camuflaje puesto por brazo: APRENDE 39,2 %, BORRADO 37,1 %, SIN 28,7 %, TECHO 25,1 %.

**Todos los diarios (P7-34 + pilotos), sumando tics**

| estado | situación | minutos | golpes de rivales / min | vida perdida / min | rivales a ≤ 4 por tic | nos persiguen por tic |
|---|---|---:|---:|---:|---:|---:|
| puesto | todas | 1.301,2 | 0,706 | 4,46 | 1,510 | 0,433 |
| puesto delatado | todas | 42,7 | 17,529 | 89,61 | 3,050 | 1,093 |
| sin camuflaje | todas | 2.645,4 | 0,883 | 6,48 | 1,444 | 0,422 |
| puesto | dentro · rival≤8 | 1.284,2 | 0,713 | 4,51 | 1,519 | 0,438 |
| puesto delatado | dentro · rival≤8 | 39,1 | 18,996 | 96,13 | 3,257 | 1,182 |
| sin camuflaje | dentro · rival≤8 | 2.532,6 | 0,916 | 6,72 | 1,494 | 0,437 |
| puesto | dentro · sin rival≤8 | 7,7 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto delatado | dentro · sin rival≤8 | 1,8 | 0,000 | 0,00 | 0,000 | 0,000 |
| sin camuflaje | dentro · sin rival≤8 | 69,7 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto | fuera · rival≤8 | 8,1 | 0,370 | 1,81 | 1,644 | 0,215 |
| puesto delatado | fuera · rival≤8 | 1,6 | 3,103 | 39,60 | 1,716 | 0,258 |
| sin camuflaje | fuera · rival≤8 | 35,9 | 0,446 | 3,30 | 1,009 | 0,218 |
| puesto | fuera · sin rival≤8 | 1,2 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto delatado | fuera · sin rival≤8 | 0,1 | 0,000 | 0,00 | 0,000 | 0,000 |
| sin camuflaje | fuera · sin rival≤8 | 7,2 | 0,000 | 0,00 | 0,000 | 0,000 |

**P7-34**

| estado | situación | minutos | golpes de rivales / min | vida perdida / min | rivales a ≤ 4 por tic | nos persiguen por tic |
|---|---|---:|---:|---:|---:|---:|
| puesto | todas | 593,3 | 0,796 | 5,10 | 1,498 | 0,433 |
| puesto delatado | todas | 18,9 | 17,495 | 87,95 | 3,053 | 1,080 |
| sin camuflaje | todas | 1.419,8 | 0,900 | 7,05 | 1,345 | 0,393 |
| puesto | dentro · rival≤8 | 584,8 | 0,807 | 5,17 | 1,508 | 0,437 |
| puesto delatado | dentro · rival≤8 | 17,4 | 18,892 | 93,15 | 3,275 | 1,169 |
| sin camuflaje | dentro · rival≤8 | 1.347,3 | 0,942 | 7,38 | 1,402 | 0,411 |
| puesto | dentro · sin rival≤8 | 4,1 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto delatado | dentro · sin rival≤8 | 0,9 | 0,000 | 0,00 | 0,000 | 0,000 |
| sin camuflaje | dentro · sin rival≤8 | 46,0 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto | fuera · rival≤8 | 3,8 | 0,000 | 0,00 | 1,752 | 0,250 |
| puesto delatado | fuera · rival≤8 | 0,6 | 5,393 | 84,13 | 1,604 | 0,236 |
| sin camuflaje | fuera · rival≤8 | 22,7 | 0,397 | 2,78 | 0,949 | 0,218 |
| puesto | fuera · sin rival≤8 | 0,6 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto delatado | fuera · sin rival≤8 | 0,1 | 0,000 | 0,00 | 0,000 | 0,000 |
| sin camuflaje | fuera · sin rival≤8 | 3,9 | 0,000 | 0,00 | 0,000 | 0,000 |

**piloto 1**

| estado | situación | minutos | golpes de rivales / min | vida perdida / min | rivales a ≤ 4 por tic | nos persiguen por tic |
|---|---|---:|---:|---:|---:|---:|
| puesto | todas | 634,8 | 0,646 | 4,08 | 1,534 | 0,442 |
| puesto delatado | todas | 22,0 | 17,745 | 88,23 | 3,076 | 1,116 |
| sin camuflaje | todas | 1.075,4 | 0,876 | 5,91 | 1,556 | 0,461 |
| puesto | dentro · rival≤8 | 627,3 | 0,649 | 4,10 | 1,543 | 0,447 |
| puesto delatado | dentro · rival≤8 | 20,1 | 19,295 | 95,59 | 3,280 | 1,207 |
| sin camuflaje | dentro · rival≤8 | 1.042,5 | 0,900 | 6,08 | 1,594 | 0,473 |
| puesto | dentro · sin rival≤8 | 3,5 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto delatado | dentro · sin rival≤8 | 0,9 | 0,000 | 0,00 | 0,000 | 0,000 |
| sin camuflaje | dentro · sin rival≤8 | 19,0 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto | fuera · rival≤8 | 3,4 | 0,876 | 4,29 | 1,568 | 0,183 |
| puesto delatado | fuera · rival≤8 | 0,9 | 2,129 | 18,09 | 1,763 | 0,286 |
| sin camuflaje | fuera · rival≤8 | 10,8 | 0,371 | 2,13 | 1,088 | 0,209 |
| puesto | fuera · sin rival≤8 | 0,5 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto delatado | fuera · sin rival≤8 | 0,0 | 0,000 | 0,00 | 0,000 | 0,000 |
| sin camuflaje | fuera · sin rival≤8 | 3,2 | 0,000 | 0,00 | 0,000 | 0,000 |

**piloto 2**

| estado | situación | minutos | golpes de rivales / min | vida perdida / min | rivales a ≤ 4 por tic | nos persiguen por tic |
|---|---|---:|---:|---:|---:|---:|
| puesto | todas | 73,2 | 0,506 | 2,66 | 1,396 | 0,364 |
| puesto delatado | todas | 1,8 | 15,211 | 124,23 | 2,705 | 0,956 |
| sin camuflaje | todas | 150,2 | 0,779 | 5,16 | 1,575 | 0,411 |
| puesto | dentro · rival≤8 | 72,1 | 0,513 | 2,70 | 1,398 | 0,367 |
| puesto delatado | dentro · rival≤8 | 1,6 | 16,426 | 134,14 | 2,790 | 1,023 |
| sin camuflaje | dentro · rival≤8 | 142,9 | 0,798 | 5,19 | 1,634 | 0,427 |
| puesto | dentro · sin rival≤8 | 0,1 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto delatado | dentro · sin rival≤8 | 0,0 | 0,000 | 0,00 | 0,000 | 0,000 |
| sin camuflaje | dentro · sin rival≤8 | 4,6 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto | fuera · rival≤8 | 0,9 | 0,000 | 0,00 | 1,486 | 0,187 |
| puesto delatado | fuera · rival≤8 | 0,1 | 0,000 | 0,00 | 1,861 | 0,133 |
| sin camuflaje | fuera · rival≤8 | 2,4 | 1,229 | 13,27 | 1,228 | 0,245 |
| puesto | fuera · sin rival≤8 | 0,1 | 0,000 | 0,00 | 0,000 | 0,000 |
| puesto delatado | fuera · sin rival≤8 | 0,0 | 0,000 | 0,00 | 0,000 | 0,000 |
| sin camuflaje | fuera · sin rival≤8 | 0,2 | 0,000 | 0,00 | 0,000 | 0,000 |


**Misma criatura, situaciones parecidas** (vidas con ≥ 240 tics en los dos estados; diferencia puesto − sin camuflaje por vida; media y error típico):

| situación | vidas con los dos estados (≥ 240 tics cada uno) | golpes/min: puesto − sin, media ± ee | vida perdida/min | rivales a ≤ 4 por tic | nos persiguen por tic |
|---|---:|---|---|---|---|
| todas | 87 | 0,873 ± 0,278 | 4,62 ± 2,74 | 0,596 ± 0,063 | 0,137 ± 0,029 |
| dentro · rival≤8 | 85 | 0,822 ± 0,277 | 3,72 ± 2,78 | 0,583 ± 0,063 | 0,133 ± 0,030 |
| dentro · sin rival≤8 | 1 | 0,000 ± — | 0,00 ± — | 0,000 ± — | 0,000 ± — |
| misma fase y situación (todos los tramos) | 83 | -0,149 ± 0,277 | -0,10 ± 2,73 | 0,097 ± 0,051 | -0,013 ± 0,035 |
| fase 0 · dentro · rival≤8 | 66 | 0,104 ± 0,234 | 1,03 ± 3,26 | 0,140 ± 0,040 | 0,001 ± 0,034 |
| fase 1 · dentro · rival≤8 | 4 | 0,000 ± 0,000 | 0,00 ± 0,00 | 0,337 ± 0,231 | -0,144 ± 0,134 |
| fase 2 · dentro · rival≤8 | 3 | -0,217 ± 0,217 | -2,87 ± 2,87 | -0,248 ± 0,130 | 0,044 ± 0,094 |
| fase 3 · dentro · rival≤8 | 6 | -2,911 ± 2,732 | -12,30 ± 11,73 | -0,296 ± 0,485 | -0,142 ± 0,316 |
| fase 4 · dentro · rival≤8 | 3 | -0,380 ± 1,424 | 2,03 ± 1,80 | 0,003 ± 0,395 | 0,045 ± 0,069 |

## Lectura

Sumando todos los tics, con el camuflaje puesto la criatura recibe 0,706 golpes por minuto frente a 0,883 sin él, y pierde 4,46 frente a 6,48 puntos de vida por minuto; con un rival a 8 o menos
dentro del anillo, 0,713 frente a 0,916 golpes y 4,51 frente a 6,72 de vida. Esas sumas mezclan criaturas y momentos (quien lleva camuflaje suele ser quien ha llegado
a la cámara, y la lleva más tarde en la vida, cuando hay más rivales cerca): la comparación honesta es la misma criatura en situaciones parecidas: con el camuflaje puesto
recibe 0,873 golpes/min más (más de 3 errores típicos) y pierde 4,62 de vida/min más (dentro del ruido) (87 vidas); con un rival a 8 o menos dentro del anillo,
0,822 golpes/min más (dentro del ruido) (85 vidas); los rivales a 4 o menos por tic cambian en 0,583 ± 0,063 y los que nos persiguen en 0,133 ± 0,030.
Pero el camuflaje se lleva más tarde en la vida (se recoge en la cámara de la Fortaleza, en el centro, y después el anillo aprieta y hay más rivales cerca): emparejando también
por TRAMO de la vida (3.000 tics), misma criatura y misma situación (83 pares vida × tramo × situación): golpes/min -0,149 ± 0,277, vida perdida/min -0,10 ± 2,73,
rivales a ≤ 4 0,097 ± 0,051, nos persiguen -0,013 ± 0,035 (puesto − sin camuflaje; negativo = protege).
Lo que el juego promete (invisible a más de 4/7 casillas hasta atacar) solo puede notarse en que los rivales lejanos no vengan: eso es «nos persiguen» y «rivales a ≤ 4»; los
golpes a bocajarro no los evita ningún camuflaje. El cuerpo congelado lo valora por una constante [impl] de 0,25 y por el miedo que ahorra (topes certificados); lo que estos
datos dicen de si protege está en la tabla de la misma criatura, con su error típico. **Respuesta con estos datos**: emparejando por criatura, tramo y situación, ninguna
de las cuatro medidas se aparta del cero más de 3 errores típicos (golpes_min 0,5 ee, dano_min 0,0 ee, r4 1,9 ee, persiguen 0,4 ee): el camuflaje, tal como lo lleva
esta criatura (que casi siempre se mueve, y a 7 casillas la ven igual), no protege de forma que se vea en 452 vidas; la única señal, pequeña, va al revés (más rivales a ≤ 4 con
el camuflaje puesto). Lo que queda por medir, cuando cierre la serie 1: lo mismo con SIN EMOCIÓN y con TECHO por separado.
