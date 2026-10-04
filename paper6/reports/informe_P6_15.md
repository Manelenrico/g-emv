# P6-15 · La puerta honesta consigo misma: banco

*27-sep-2026. Coste cero: ninguna partida, ninguna llamada de pago. Solo banco
sobre los 40 diarios de A4 y el código congelado. `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados
del cinco y los 32 del seis (`CONGELADO_P6.md`): 0 alterados al principio y al
final. La puerta del cinco (`policy_forma`, `forma`, `forma_viva`,
`proyeccion`) tampoco se toca: **todo lo nuevo está en `puerta6_P6_15.py`,
versión nueva declarada («puerta6»), y en el banco que la mide.** Nada de
MettaScope. Sin propuestas de diseño.*

Mismo banco que P6-14 (`banco_P6_15.py` = el arnés de `banco_P6_14.py` tal
cual: oráculo, 40 vidas por la vía real, empatía comprobada por `assert`,
mismos umbrales principales H 100 · R 5 · disparo 33 · margen 0,062, mismos
cruces). La puerta real reproduce P6-14 al número: 3.849 planes juzgables,
**ok 27 · area 3.318 · vida 504**, 3 de 19 evitables. Fidelidad del replay:
494.368 de 494.370 `elegido` iguales (los 2 de `21622393` s10, sin decisiones).

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**El cuerpo se imagina mejor de lo que actúa, y mucho.** En 2.120 de los 2.536
rechazos por área de las ventanas de muerte (84 %) el comparador de la puerta
«se creía a salvo» en el último punto de control y el cuerpo real, en ese
mismo tic, ardía o ya había muerto (508 muertos). Juzgado contra **lo que de
verdad hizo**, imaginado con la misma maquinaria, el mismo plan del oráculo
pasa en **18 de las 19** muertes evitables (i 5/6, ii 12/12, iii 1/1); contra
**el cuerpo imaginado decidiendo paso a paso** (puerta6 B, ~370 ms por
juicio), en **17 de 19** (i 4/6, ii 12/12, iii 1/1). La puerta tal cual: 3 de 19.
Y el «+0,005 contra −0,24» de S-8 no es cosa de los pisos: **el plan del
oráculo entra en el anillo tan cerca de los rivales como el comparador**
(S-8 del plan − S-8 de quedarse = +0,210; del comparador = +0,208), así que
en la resta de la puerta S-8 se cancela; en la elección real, el cuerpo compara
entrar (+0,205) con lo que elige (−0,024), y ahí S-8 manda.

---

## 1 · EL EXCESO DE CONFIANZA, MEDIDO

### 1.1 Lo que el comparador decía y lo que el cuerpo hizo

Sobre los **2.536 rechazos por área** de las ventanas de muerte (H 100,
disparo 33, todos los destinos; los mismos de P6-14). Para cada uno, la
casilla que la proyección del candidato comparador (`ir_botin`, `ir_centro`,
`ir_pareja`…) ocupaba en cada punto de control, contra la casilla real del
diario en ese tic. «A salvo» = dentro del radio de ese tic y del r1 de la
fase; «no salió» = la casilla real arde, o el cuerpo ya ha muerto. Se cuenta
en el último punto de control (elegido) y en el primero (la llegada):

| punto de control | comparador «se creía a salvo» | …y el cuerpo real **no salió** | …de ellos, ya muerto | …y salió | comparador no se creía a salvo (real arde / a salvo) |
|---|---|---|---|---|---|
| **último** (llegada + 100) | 2.253 | **2.120 (84 % de los 2.536)** | 508 | 133 | 283 (258 / 25) |
| primero (llegada) | 2.331 | 2.036 (80 %) | 25 | 295 | 205 (150 / 55) |

La vida que el comparador se imaginaba menos la real: **+31,0 de media en el
último punto** (mediana +32, p10 +7, p90 +49); +10,0 en el primero.

Es decir: la proyección anda el candidato entero («ir a la casilla y esperar
100 tics dentro»); el cuerpo, decidiendo tic a tic, vuelve al fuego o no sale.
Con el comparador que dice «yo salgo solo», el plan que sale no gana nada.

### 1.2 Por qué S-8 pesa +0,005 en la proyección y −0,24 en la elección real

Qué es «a piso»: `forma.pisos_rival` toma las filas de rivales del instante
(F-4-ALCANCE, S-8-EXPOSICION, S-7-AGRESOR, MIEDO_APRENDIDO, S-VIDA-AJENA) y en
**toda** foto proyectada —del plan y del comparador— les pone ese valor como
mínimo (`d_con_pisos`: `M = max(M, piso)`). Los rivales de la foto no se
mueven (`foto_rapida` deja los `agents` de la observación tal cual) y el piso
impide que la proyección se invente alivio por alejarse de ellos; acercarse sí
sube la fila. En la elección real, el decisor valora cada candidato a UN paso
(`_obs_prevista`): misma foto, rivales quietos, **sin piso**, y S-8 sube al
acercarse (S-8 = suma de `EXPO_POR_HOSTIL·(1 − dist/radio)` sobre los rivales
con línea de vista).

Medido en los 2.536 (S-8 en la primera foto de la puerta contra la S-8 del
mismo candidato en la elección real del mismo tic, `radio["candidatos"]`):

| diferencia de S-8 | media | mediana | p10 | p90 |
|---|---|---|---|---|
| real: comparador − quedarse (`noop`) | **+0,205** | +0,30 | 0 | +0,30 |
| proyección sin piso: comparador − quedarse | +0,208 | +0,30 | 0 | +0,30 |
| proyección con piso: comparador − quedarse | +0,212 | +0,30 | 0 | +0,30 |
| proyección: **plan − quedarse** | **+0,210** | +0,30 | 0 | +0,30 |
| proyección con piso: **comparador − plan** | **−0,003** | 0,00 | 0 | +0,027 |
| real: elegido − quedarse | −0,024 | 0,00 | −0,11 | 0 |

Lectura: (1) la proyección **sí** ve la exposición de entrar en el anillo:
el comparador proyectado tiene +0,21 de S-8 sobre quedarse, igual que en la
elección real; el piso cambia 0,004. (2) Lo que anula S-8 en la puerta es que
**el plan del oráculo también entra** (+0,210): dentro del anillo están los
rivales, y una casilla segura con «pocos rivales cerca» sigue estando a la
vista de ellos. En la resta plan − comparador, S-8 da −0,003 (el +0,005 de
P6-14, por la otra cara). (3) En la elección real el cuerpo no compara dos
maneras de entrar: compara entrar (+0,205) con lo que elige, que expone menos
que quedarse (−0,024); la diferencia, −0,23, es el −0,24 de P6-13. Con esto,
la explicación de P6-14 («el miedo se cancela por los pisos») queda
**corregida**: el piso apenas interviene; se cancela porque plan y comparador
entran los dos.

---

## 2 · EL TECHO: EL PLAN CONTRA «LO QUE DE VERDAD HICE»

`puerta6_P6_15.curva_real`: la trayectoria real del diario (posición por tic,
con sus `usar_*` y `coger`) pasada por la misma maquinaria que el plan
(`proyeccion.proyectar` con `camino` —la vía prevista en A3 para seguir
posiciones reales—, `foto_rapida`, `forma._d2` con los mismos pisos, mismos
puntos de control), y la **misma regla** (`forma.juzga_margen`, vida < 15 →
«vida», margen 0,062). Las dos cosas quedan imaginadas. Es un techo: en una
partida real no se conoce el futuro. Declarado: después de la muerte, la
trayectoria real se queda en su última casilla (y el fuego la sigue
cobrando); las curas reales se aplican con la regla de la proyección.

| comparador | juzgables | ok | area | vida | evitables con plan aceptado a tiempo | por clase (i / ii / iii) |
|---|---|---|---|---|---|---|
| puerta (mejor candidato propio proyectado) | 3.849 | 27 | 3.318 | 504 | **3 de 19** | 0/6 · 3/12 · 0/1 |
| **puerta6 (A): lo que de verdad hice** | 3.849 | **1.896** | 1.449 | 504 | **18 de 19** | **5/6 · 12/12 · 1/1** |

La única evitable sin plan a tiempo contra lo real: `21203477` s11 (clase i,
muere 23 tics después del primer golpe; hp 2-26 en sus decisiones: 6 de sus
10 planes caen por «vida» y los otros 4 se quedan en +0,045-0,055, bajo el
margen). Con margen 0,02 pasa a 19 de 19; con 0,08 sigue en 18; con
H 50, 18; con H 200, 17.

- **Falsas aceptaciones en las 18 vidas sin anillo:** 385 planes aceptados en
  13 vidas; **187 falsas** (α algún punto peor 21, β menos vida al final 49,
  γ aleja del hermano 141) en 12 vidas. (Puerta: 11 aceptados, 8 falsas.)
- **La pareja (c):** 912 planes (c) aceptados; en los 64 casos en que los dos
  hermanos juzgaron el mismo destino en el mismo tic, **11** lo aceptaron los
  dos (puerta: 0).
- Criterio: (a) 996/1.894, (b) 991/2.003, (c) 912/1.789. Momento: (1)
  1.890/3.542, (2) **13/321** (al aviso sigue sin haber casi nada que ganar).

---

## 3 · LA VERSIÓN QUE SE PODRÍA USAR: EL CUERPO DECIDIENDO PASO A PASO

`puerta6_P6_15.rollout`: desde el estado de la decisión, tic a tic hasta el
último punto de control del plan más largo (llegada + 200): foto proyectada
(`foto_rapida`, rivales quietos donde el cuerpo los ve) → `decisor_zs.decide`
tal como está enganchado (con los cuatro arreglos del seis) sobre copias de
`mem` y `bloqueos` → la acción se aplica con `proyectar_rapido` un tic (paso si
las piernas están listas, coger, usar; el anillo cobra). **Sin piso en las
decisiones** (el decisor siente a los rivales como al verlos); la curva del
comparador en los puntos de control se valora luego **con** los mismos pisos
que el plan, para que el juicio sea el mismo. Declarado: no modela ataques ni
golpes recibidos; `empunar`/`ponerse`/`soltar`/`atacar` cuentan como esperar.

### 3.1 Factibilidad

| rollout decide… | ms por juicio (mediana · p95 · máx) | decisiones del decisor por rollout | tics por rollout | ms por decisión del decisor |
|---|---|---|---|---|
| **en todos los tics (elegido)** | **367 · 633 · 1.157** | 258 | 258 | 1,53 |
| con piernas listas y cada 6 | 329 · 620 · 1.030 | 146 | 258 | 2,47 |
| con piernas listas y cada 11 | 327 · 614 · 1.021 | 129 | 258 | 2,75 |

Un rollout vale para todos los planes de la decisión (se muestrea en los
puntos de control de cada uno). Un tic del mundo son 41,7 ms; la puerta
actual tarda 143 ms por plan (mediana; p95 213) y ya va al hilo cuando pasa
de 20 ms (`MS_AL_HILO`). El rollout cuesta **2,6× la puerta actual** por
decisión y **9 tics** de reloj: no cabe en el tiempo de una decisión; cabe en
el hilo donde ya vive la puerta. Decidir menos veces ahorra poco (el coste
está en proyectar y copiar el estado cada tic, no en decidir).

### 3.2 Fidelidad contra el diario (2.641 decisiones, ventana [t, t+200])

| | +50 tics | +100 | +200 |
|---|---|---|---|
| distancia predicha−real (Chebyshev), mediana · media | 1 · 1,37 | 2 · 2,27 | 2 · 3,06 |
| acierta si arde o no | 2.040/2.471 (83 %) | 1.641/2.267 (72 %) | 1.221/1.827 (67 %) |
| predice arde y no ardía · predice a salvo y ardía | 169 · 262 | 314 · 312 | 316 · 290 |

Tics ardiendo en los 200: predichos 114,5 de media, reales 99,4 (el rollout
**arde más** que el cuerpo real: +15 de media, mediana +1). En las ventanas de
muerte (1.506 decisiones): 140,7 predichos contra 122,5 reales; acierta el
estado a +200 en 583 de 828 (70 %).

**Las idas y vueltas al fuego** (transición a salvo → arde dentro de la
ventana): reales 3.011 en 1.165 decisiones; predichas 1.854 en 833. De las
1.165 decisiones con vuelta real, el rollout **predice alguna vuelta en 685
(59 %)**; en 480 no la ve; en 148 inventa una que no hubo. Predice, pues, que
el cuerpo vuelve al fuego en la mayoría de los casos en que vuelve, y nunca
se cree a salvo como se creía el comparador: eso es lo que cambia el juicio.
Con `cada` 6 u 11 las cifras son las mismas al 1 %.

### 3.3 Las cuentas del punto 2 con este comparador

| comparador | ok | area | vida | evitables a tiempo | por clase | sin anillo: aceptados / falsas (α β γ) | (c) aceptados / por los dos |
|---|---|---|---|---|---|---|---|
| puerta | 27 | 3.318 | 504 | 3 | 0/6 · 3/12 · 0/1 | 11 / 8 (1 2 7) | 13 / 0 |
| puerta6 (A) lo real imaginado | 1.896 | 1.449 | 504 | 18 | 5/6 · 12/12 · 1/1 | 385 / 187 (21 49 141) | 912 / 11 |
| **puerta6 (B) paso a paso, cada tic** | **1.739** | 1.606 | 504 | **17** | **4/6 · 12/12 · 1/1** | **279 / 154 (15 43 106)** | **828 / 12** |
| puerta6 (B) cada 6 | 1.736 | 1.609 | 504 | 17 | 4/6 · 12/12 · 1/1 | 279 / 154 | 828 / 12 |
| puerta6 (B) cada 11 | 1.748 | 1.597 | 504 | 17 | 4/6 · 12/12 · 1/1 | 284 / 154 | 837 / 14 |

Las dos evitables sin plan a tiempo con (B): `21203477` s11 (hp 2; «vida») y
`20260916` s11 (clase i, fase 6: el rollout también sale). Momento (2): 10 de
321. Cruces (B, cada tic, disparo 33, R 5): margen 0,02 → 17; 0,08 → 17;
H 50 → 17; H 200 → 16. Todo el cruce de (A) y (B) está en
`P6_15_resumen.json → variantes` (162 filas): (A) entre 17 y 19; (B) entre 16
y 17. Las «vida» (504) no cambian con el comparador: son del plan (el cuerpo ya
está a 0-21 hp).

Lo que sube con (B) sube también en falsas aceptaciones: 154 de 279 en las
vidas sin anillo, la mayoría por alejar del hermano (γ 106).

---

## 4 · EL HORIZONTE, SOLO CONTADO

Planes de clase (i) en ventana (394 con H 100, todos los destinos): rechazados
391; con **el fuego de mi casilla fuera de la ventana del plan** (arde después
del último punto de control): **11** (todos «area»). Con H 50: 11 de 388; con
H 200: 10 de 394. El horizonte no es lo que retiene a la clase (i): en 380 de
391 el fuego ya está dentro de la ventana y el plan pierde igualmente contra
el comparador. La ventana no se ha cambiado.

---

## 5 · EL CASO EN GIF

`P6_15_tres_caminos.gif` (88 fotogramas, cada 12 tics, aviso 11.856 → muerte
12.888; md5 en `DIARIOS_P6_MANIFIESTO.md`): la misma vida del GIF de P6-14,
`21936580` asiento 10, clase (ii), plan del oráculo en 12.594 → (19,24).
Desde ese tic se ven las tres trayectorias: **gris a rayas**, la que imaginaba
el comparador `ir_botin` (recta a (21,21), dentro del radio, y esperar: la
puerta lo creía a salvo con 100 de vida en 12.638 y 12.738; el cuerpo real
estaba en (19,20)-(20,19), ardiendo, con 67 y 40); **azul**, la real (se queda
en el borde y muere); **morado punteado**, la puerta6 (B): el cuerpo imaginado
oscila en (19,20)-(19,21), se cura, y se va hacia el noroeste, ardiendo;
**estrella verde**, el plan. Veredictos: puerta ok (+0,066), contra lo real ok
(+0,118), contra el paso a paso ok (+0,123).

---

## 6 · LO QUE DICE LA MEDIDA (sin proponer nada)

1. **La puerta se compara con un cuerpo que no existe**: en el 84 % de los
   rechazos por área de las ventanas de muerte el comparador se creía a salvo
   y el cuerpo real ardía o había muerto; se imaginaba 31 puntos de vida más
   de los que tuvo.
2. **S-8 no es el freno de la puerta**: el piso cambia 0,004; el plan entra en
   el anillo tan expuesto como el comparador (+0,210 contra +0,208), y por eso
   S-8 se cancela; en la elección real el cuerpo compara entrar con quedarse
   fuera, y ahí S-8 vale −0,23.
3. **Techo**: contra lo que de verdad hizo, el mismo oráculo y la misma regla
   aceptan a tiempo en 18 de 19 (19 de 19 con margen 0,02).
4. **Versión usable**: el cuerpo imaginado paso a paso —367 ms por juicio, 9
   tics, en el hilo de la puerta— acepta a tiempo en 17 de 19; predice el
   estado a +200 en el 67 % y las vueltas al fuego en el 59 % de las decisiones
   en que las hubo, y arde de media 15 tics más que el cuerpo real.
5. **Lo que se paga**: con (A) y (B) las falsas aceptaciones fuera del anillo
   pasan de 8 a 187 y 154 (la mayoría, planes que alejan del hermano).
6. **El horizonte no es la causa** en la clase (i): 11 de 391.

---

## 7 · ARCHIVOS

| archivo | md5 | qué es |
|---|---|---|
| `puerta6_P6_15.py` | `7c70ae1752c7ac1aae457d0c5b2d36f3` | **puerta6**, versión nueva declarada: comparadores (A) y (B) para la misma regla |
| `banco_P6_15.py` | `b5502a9357683292d349ab6dce2f2ab8` | arnés de P6-14 + exceso, techo, rollout, horizonte |
| `corre_P6_15.py` | `f2c4548d9bf006ab40269f98bfc4b31d` | las 40 vidas, 8 procesos (1.314 s de reloj) |
| `resume_P6_15.py` | `46b0bcbda9f6f29f4b17db034064953f` | cuentas y cruces |
| `gif_P6_15.py` | `83099dc56793ac4d697456b388291664` | el GIF de los tres caminos |
| `P6_15_planes.json` | `f8fbd259a9ffb2f4f28137c60cd72f92` | los 19.911 planes con los tres veredictos, curvas, exceso y S-8 (37 MB) |
| `P6_15_resumen.json` | `841bee7b078739a9d9e3e871a2ca795f` | totales, exceso, principal por comparador, 162 variantes, fidelidad, horizonte |
| `P6_15_tres_caminos.gif` | `c5d3e00748cdef50cf03916ee918e191` | el caso (fuera de git; md5 en el manifiesto) |
