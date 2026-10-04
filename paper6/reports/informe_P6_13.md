# P6-13 · El sitio de la razón en el anillo: medir antes de construir

*27-sep-2026. Coste cero: ninguna partida nueva, ninguna llamada de pago, nada
construido. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y
al final; los 202 congelados del cinco y los 32 del seis (`CONGELADO_P6.md`,
etiqueta `cuerpo6-congelado`): 0 alterados al principio y al final. Todo sale
de los 40 diarios de A4 (P6-11) y del código congelado; nada de MettaScope.
Sin propuestas de diseño.*

---

## 1 · QUÉ DICE EL MUNDO DEL ANILLO

**La versión 0.1.19 del mundo no está en el repositorio** (solo hay el mapa y
el catálogo de la 0.1.18 en `cantera/paper4/` y el manifiesto de la 0.1.18 en
`cantera/paper5/`). Me quedo con lo que muestra la observación real.

### Qué campos hablan del anillo, y desde cuándo

| dónde | campo | qué dice | desde cuándo |
|---|---|---|---|
| `player_config` (tic 0, antes de empezar) | `zone_schedule` | **el calendario completo**: 7 fases `[warn, shrink, done, r0, r1, dps]` | **desde el principio, entero** |
| cada tic, `zone` (en el diario `zona`) | `center` | `[24, 24]` en todos los tics de las 20 partidas | siempre; nunca cambia |
| | `radius` | el radio vigente; baja en escalones de 1 casilla entre `shrink` y `done` | cada tic |
| | `next_radius` | el radio al que va la fase en curso (y, acabada, la siguiente) | cada tic |
| | `warn_tick`, `shrink_tick` | el aviso y el arranque del encogimiento de la fase en curso (**ojo: tras `done` ya apuntan a la fase siguiente**, aunque el fuego vigente sea el de la anterior) | cada tic |
| | `damage_per_s` | el daño vigente fuera del radio (sube en cada `warn`) | cada tic |

El calendario de A4 (idéntico en las 20 partidas):

| fase | aviso `warn` | empieza a encoger `shrink` | acaba `done` | radio r0 → r1 | daño/s |
|---:|---:|---:|---:|---|---:|
| 1 | 7.296 | 7.536 | 8.076 | 24 → 19 | 1 |
| 2 | 8.436 | 8.676 | 9.216 | 19 → 15 | 2 |
| 3 | 9.576 | 9.816 | 10.356 | 15 → 11 | 4 |
| 4 | 10.716 | 10.956 | 11.496 | 11 → 8 | 6 |
| 5 | 11.856 | 12.096 | 12.636 | 8 → 5 | 8 |
| 6 | 12.996 | 13.236 | 13.776 | 5 → 3 | 16 |
| 7 | 14.136 | 14.376 | 14.916 | 3 → **0** | 24 |

**El sitio donde acabará se sabe de antemano, entero:** el centro es fijo
(`arena_size // 2` = (24, 24), y `zone.center` lo confirma tic a tic), los radios
y los instantes están en el `player_config` desde el tic 0. La casilla segura en
cualquier instante futuro es cualquiera con **distancia euclídea** al centro ≤
radio(t). No hay sorteo ni información que llegue tarde. *(Lo que la observación
no dice: por qué el radio baja en escalones de 108-180 tics en vez de continuo,
ni si el último radio 0 deja alguna casilla; con el final de partida que se ve
abajo, nunca hace falta.)*

### Qué filas del cuerpo leen el anillo, y qué campos usan

Todo lo que el cuerpo sabe del anillo sale del **calendario** (`mundo.zone_schedule`)
y de la geometría (`mundo.anillo_en`, `mundo.eventos_arde`, distancia euclídea al
centro). **Ninguna fila lee el campo `zone` del tic** (buscado en `appraisal_zs_v42_exp`,
`decisor_zs` y `mundo`: 0 lecturas).

| sitio | qué hace con el anillo |
|---|---|
| **F-ANTICIPACION** (`appraisal:975-1000`) | para mi casilla, todos los instantes en que el fuego la alcanzará (`eventos_arde`), y se queda con el peor: `M = min(ANT_TECHO, (dps/dps_ref) · 0,5 · (1 − t_arde/20 s))`. Con `dps_ref` = 24 (el máximo del calendario), en la fase 5 (dps 8) el techo efectivo es **0,167**; en la 1, 0,021 |
| `ir_centro` (`decisor:465-467`) | candidato «ir al centro del anillo» (`mundo.anillo_en(tick)`), siempre disponible con piernas listas |
| la foto prevista (`decisor:357-360`) | cada candidato se valora en su tic previsto con `zone = anillo_en(tick_eval)`: **el después imaginado lleva el anillo avanzado** (punto 4) |
| S-COMPANIA del cinco (`:1011-1015`) | gate «anillo mordiendo en < 5 s» — **apagada** (`COMPANIA_ON=False`); la del seis (`filas10`) no tiene gate de anillo |
| `_proximo_encogimiento` (`:1709`) | (tic límite, radio final, dps) de la etapa en curso: la usa el «muro» del cinco |

---

## 2 · CÓMO ACABA LA PARTIDA

**«Al cierre», en la cuenta de 19 de 20 de P6-4/P6-6/P6-10/P6-11**
(`mide_P6_4.py`: `ANILLO_AVISA = 7296`, `ANILLO_CIERRA = 8076`): **los dos vivos en
el tic 8.076, el `done` de la PRIMERA fase (24 → 19)**. No es el final de la
partida: es el primer encogimiento. Con esa definición, 19 de 20 parejas están
enteras; con la del último aviso (14.136), **3 de 20**.

### La línea de tiempo (20 partidas, 40 vidas; `P6_13_anillo.json`)

| al aviso de la fase | vidas vivas | parejas enteras | muertes por anillo cuya quemadura empieza en la fase |
|---|---:|---:|---:|
| 1 (7.296) | 38 | 19 | 0 |
| 2 (8.436) | 38 | 19 | 0 |
| 3 (9.576) | 38 | 19 | 1 |
| 4 (10.716) | 38 | 19 | 0 |
| **5 (11.856)** | 35 | 17 | **16** |
| 6 (12.996) | 21 | 7 | 2 |
| 7 (14.136) | 13 | 3 | 3 |

De las 40 vidas, 38 llegan al primer aviso y **35 al de la fase 5**: hasta ahí
el anillo no mata a nadie. **La fase 5 (radio 8 → 5, daño 8/s) mata a 16 de las 22.**

### ¿Se cierra del todo?

Por calendario, **sí**: en 14.916 el radio es **0**. Pero **la partida acaba
antes**: los 11 supervivientes terminan con `reason = winner` (colocación 1) o
`match_over` (colocación 2) entre los tics **13.061 y 14.952**; solo **2 vidas
de 40 llegan al tic 14.916**. La partida termina cuando queda un equipo, no
cuando el anillo se cierra. De las 22 muertes por anillo, **3 son de la fase
final** (radio 3 → 0, daño 24/s, desde 14.136): son las únicas de un final
inevitable para quien esté fuera del centro exacto. Las otras **19 ocurren con
el anillo a radio 5-8 y la partida sin acabar.**

---

## 3 · ANATOMÍA DE LAS 22 MUERTES POR ANILLO

Definiciones (`mide_anillo_P6_13.py`): **aviso** = `warn` de la fase cuya
quemadura mata (la última racha de golpes de `zone` con huecos ≤ 48 tics que
acaba en la muerte fecha la fase por su primer golpe; tres cuerpos llegan al
aviso de la fase 6 ya con 1-10 hp de la quemadura de la 5); **primer golpe** =
el primero de esa racha; **muerte** = último tic vivo. **Casilla segura** = con
distancia euclídea al centro ≤ r1 de esa fase (donde el anillo acaba) y no
sólida; **camino** = BFS con 8 vecinos sobre `mundo.solido`; **instantes** =
pasos × 11. El hermano: su posición real (su diario).

| | |
|---|---:|
| muertes por anillo | 22 (de 29 muertes; 11 vidas sobreviven) |
| **había camino a una casilla segura** | **22 de 22** (en el aviso y en el primer golpe) |
| pasos hasta la segura en el aviso: mediana / máximo | **2 / 5** (= 22 / 55 tics) |
| tics disponibles desde el aviso hasta la muerte: mediana / mínimo | **966 / 7** |
| **llegaba a salvo saliendo en el aviso** | **21 de 22** |
| pasos hasta la segura en el primer golpe: mediana / máximo | **2 / 5** |
| tics desde el primer golpe hasta la muerte: mediana / mínimo | **263 / 6** |
| **llegaba a salvo saliendo en el primer golpe** | **19 de 22** |
| el hermano vivo al morir | 13 de 22 · a 1-8 casillas (mediana 3) |
| el hermano también muere por el anillo | 16 de 22 |

**Las clases** (una por muerte; las reglas, en el script):

| clase | n | cómo se decide |
|---|---:|---|
| **(ii) lo retuvo el miedo a rivales** | **12** | en los tics con detalle entre el primer golpe y la muerte, lo que hizo perder a `ir_centro` fue sobre todo miedo (S-8-EXPOSICION, S-7, F-4, F-REENCUENTRO): peso del miedo > peso del hermano |
| **(i) llegaba a salvo si salía antes** | **8** | había camino y tiempo (salir en el aviso le bastaba) y ninguna fila de miedo ni de hermano pesó contra `ir_centro` en los tics con detalle: simplemente no fue (eligió `ir_objeto`, `ir_botin`, `paso`, `move`) |
| **(iii) lo retuvo el hermano** | **1** | `21727122` s10: S-HERIDO −0,62 contra `ir_centro` (el hermano herido al lado) |
| (iv) no había salida | **0** | — |
| (v) otra | **1** | `21098748` s10: muere 7 tics después del aviso de la fase final, con 20 hp y 3 pasos hasta el centro; una sola decisión con piernas listas (`ir_centro`) |

**Qué eligió la clase (ii) con las piernas listas entre el primer golpe y la
muerte** (12 muertes, 791 decisiones): `noop` 426, `ir_objeto` 124, `paso` 82,
`move` 65, `ir_botin` 53, `ir_pareja` 27, **`ir_centro` 11**.

**Qué filas hicieron perder a `ir_centro` en la clase (ii)** (media de
M(ganador) − M(`ir_centro`); negativo = `ir_centro` llevaba más):

| fila | media | en cuántas muertes |
|---|---:|---:|
| **S-8-EXPOSICION** | **−0,237** | 13 |
| S-7-AGRESOR | −0,221 | 2 |
| F-REENCUENTRO | −0,220 | 1 |
| R-CARENCIA | −0,173 | 5 |
| R-LLAMADA | −0,070 | 12 |
| S-COMPANIA | −0,039 | 4 |
| F-4-ALCANCE | −0,027 | 13 |
| **F-ANTICIPACION** | **+0,154** | 12 |

**El anillo pesa a favor de `ir_centro` +0,15 (su techo efectivo en la fase 5
es 0,167) y la exposición pesa en contra −0,24 (su techo es 0,30).** El centro
seguro es donde se concentran los rivales, así que ir al centro *es* exponerse,
y el cuerpo valora esa exposición por encima del fuego. El miedo gana al anillo
por construcción de los techos, no por error de percepción.

---

## 4 · CUÁNTO IMAGINA EL CUERPO EL ANILLO

**En la foto prevista, sí:** `decisor_zs._obs_prevista` (`:357-360`) pone
`zone = mundo.anillo_en(tick_eval)`, con el radio del instante previsto, y
F-ANTICIPACION se calcula en la casilla prevista con el calendario completo.

**Medido** (`mide_sorpresa_P6_13.py`, la misma medida que P6-4 hizo con S-8: la
fila que el ganador previó contra la fila real en el siguiente tic con piernas
listas; 7.092 pares en A4):

| fila | sorpresa \|real − prevista\|: mediana / media / suma | se queda corto / se pasa | real > 0 | …y prevista > 0 |
|---|---|---|---:|---:|
| **F-ANTICIPACION** | **0,00000 / 0,00166 / 11,8** | 3,0 % / 0,6 % | 268 | **230 (86 %)** |
| S-8-EXPOSICION | 0,00000 / 0,04329 / 307,0 | 29,3 % / 3,0 % | 4.019 | 3.594 (89 %) |

Por fase, la sorpresa media del anillo sube con el daño (fase 5: 0,012; fase 7:
0,067) y sigue siendo **veintiséis veces menor** que la de la exposición en
total (11,8 contra 307,0). En A0 (sin ojos): 30,9 contra 291,1.

**El cuerpo imagina bien el anillo.** Sabe dónde estará y cuándo, y lo prevé con
un error medio de 0,002. Lo que no hace es pesarlo: su fila vale como máximo
0,167 en la fase que mata (8/24 de daño por 0,5 de urgencia), contra 0,30 de la
exposición. **Un plan no gana saber; solo puede ganar horizonte** —la urgencia de
la fila arranca a 20 s del fuego (480 tics) y en las 22 muertes había una mediana
de 966 tics desde el aviso— **y peso**, y eso último es de la tabla, no de un plan.

---

## 5 · UNA MUERTE TÍPICA, EN GIF

`cantera/paper6/P6_13_anillo.gif` — 101 fotogramas, clase (ii), `21308206`
asiento 10, del aviso de la fase 5 (11.856) a la muerte (13.056), con el hermano
(naranja) y los rivales vistos y contados. Matplotlib sobre los diarios crudos.
Lo que se ve, con los números del guion:

* Del aviso al tic 12.636 el cuerpo está en (19,26), a **5,4 del centro**, con
  hp 100, eligiendo `noop`; el radio baja de 8 a 5 y su casilla queda fuera por
  cuatro décimas. F-ANTICIPACION sube a 0,15; S-8 va y viene entre 0 y 0,29 con
  los rivales 0, 7 y 14 a la vista.
* En 12.696 entra a (23,28), **dentro** (4,1): S-8 = 0,30, con 0, 6 y 7 a la
  vista **dentro del círculo seguro**. Y se va: 12.816 en (29,27), fuera (5,8),
  hp 88; 12.936 en (30,30), a 8,5, hp 55, eligiendo `noop` con 0, 6 y 7 contados
  en el centro; 13.056 vuelve a (25,29), a 5,1, hp 10, y muere.
* El hermano está a 1-4 casillas todo el tramo y muere también por el anillo.

Es la clase (ii) entera: el sitio seguro está lleno, ir es exponerse, y el
cuerpo prefiere el fuego.

---

## 6 · QUÉ TENDRÍA QUE PROMETER UN PLAN (solo lista, sin construir)

Un plan de pareja para el anillo tendría que hablar con datos que el cuerpo ya
tiene y con los que después puede comprobar, con lo que siente, si le fue bien:

**Del anillo** (todos ciertos desde el tic 0):
1. la fase en curso y la siguiente: `warn`, `shrink`, `done`, r1 y daño (el calendario);
2. la distancia euclídea de mi casilla al centro contra r1: si mi casilla arderá y cuándo (`eventos_arde`);
3. los pasos de camino hasta la casilla segura más cercana y los instantes que quedan (pasos × 11 contra `done` − ahora): el plan promete «llegas»;
4. el daño que voy a recibir si salgo ahora contra si espero (dps × tics fuera): el plan promete «pierdes menos hp».

**Del hermano** (del parte y de los ojos):
5. su casilla y su hp (parte fresco), y su distancia al centro y a la segura: el plan es de dos, y S-COMPANIA lo cobra si nos separa;
6. si está herido o sin venda (S-HERIDO, R-HERMANO-FALTA): en la única muerte de clase (iii) es lo que retuvo al cuerpo;
7. los rivales que él cuenta dentro del círculo seguro: es exactamente lo que S-8 va a sentir al entrar, y el plan tiene que decir que lo sabe.

**Lo que el cuerpo comprobará solo, con sus filas**, si el plan cumplió: que
F-ANTICIPACION bajó (llegó a salvo), que F-DANO no subió (no ardió), que S-8 subió
lo que el plan dijo y no más (los rivales del centro), y que S-COMPANIA siguió a
cero (no soltó al hermano). Ésas son las cuatro cosas que un plan del anillo
tendría que prometer en el idioma de la tabla.

---

## LO QUE ME LLEVO

1. **El anillo se sabe entero desde el tic 0** (calendario, centro fijo, distancia euclídea) y el cuerpo lo lee así; ninguna fila mira el campo `zone` del tic.
2. **«Al cierre» era el primer encogimiento (8.076)**, no el final. La fase que mata es la 5 (radio 8 → 5): 16 de 22; la partida acaba por `winner`/`match_over` antes de que el radio llegue a 0.
3. **Las 22 muertes tenían salida** (2 pasos de mediana, 966 tics de margen): 21 llegaban saliendo en el aviso, 19 saliendo en el primer golpe. 12 las retuvo el miedo a rivales (S-8 −0,24 contra +0,15 del anillo), 8 simplemente no fueron, 1 el hermano, 1 otra, 0 sin salida.
4. **El cuerpo imagina el anillo casi sin error** (sorpresa media 0,002, 26 veces menos que la exposición). Un plan no gana saber; gana horizonte, y el peso es de la tabla.

*Sin propuestas de diseño.*

## LOS ARCHIVOS NUEVOS, CON SU MD5

| archivo | md5 |
|---|---|
| `cantera/paper6/mide_anillo_P6_13.py` | `deb1b9be272b55060d74975c32c84386` |
| `cantera/paper6/mide_sorpresa_P6_13.py` | `b837028784e1d69b4d91e268bb5ebcd2` |
| `cantera/paper6/gif_P6_13.py` | `8e0fbcb258a51fd1d89491bd71a6721f` |
| `cantera/paper6/P6_13_anillo.json` | `59b46bf22b7a11e8bf239da25d3af3f7` |
| `cantera/paper6/P6_13_sorpresa.json` | `aa16df992e1918846e53992f2bb228cc` |
| `cantera/paper6/P6_13_anillo.gif` | `429bac8db1c8a6935d093daf9a73acdf` |

*Ningún md5 de esta tabla se escribió antes de calcularlo.*

## CONTROL FINAL

| | |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` — intacto (al principio y al final) |
| congelados del cinco (`CONGELADO.md`) | 202 comprobados, 0 alterados (al principio y al final) |
| congelados del seis (`CONGELADO_P6.md`, `cuerpo6-congelado`) | 32 comprobados, 0 alterados (al principio y al final) |
| partidas · llamadas de pago | 0 · 0 |
| MettaScope | no; el GIF sale de los diarios |
