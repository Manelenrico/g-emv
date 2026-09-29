# P5-8B — La curiosidad como forma, en vivo · LA SONDA

**PARO AQUÍ.** Las cuarenta **no deben lanzarse todavía**, y la razón está en el
titular.

---

## El titular

**La sonda hace exactamente lo que una sonda tiene que hacer: encontrar el
defecto antes de gastar las cuarenta.**

Las dos partidas corrieron, en precio y en plazo, con **cero tics perdidos** y
**cero decisiones con un armado a tiro mientras había forma activa**. El brazo K
genera formas, la puerta acepta algunas y el cuerpo las sigue.

**Pero todas las formas aceptadas mueren a los 25 tics exactos.** Mínimo 25,
máximo 25, en las 38 con caída. Veinticinco es `CADA_REEVALUA`: **mueren todas
en su primera reevaluación, sin una sola excepción.**

**La causa es mía y está identificada:** envuelvo `F._d2` con el renglón de
ignorancia **solo al nacer la forma**, no en la reevaluación. **La puerta acepta
con una regla y re-juzga con otra** — y sin el renglón, como midió F3 en seco,
solo pasa el 2,7 %. Por eso el 100 % de las reevaluaciones tumba la forma.

Con ese defecto, las cuarenta medirían una curiosidad que **nunca completa un
trayecto**, y K4 («completadas ≥ 50 % de las aceptadas») fallaría por
construcción, no por el mundo.

---

## Custodia

```
                            al empezar                         al acabar
motor/model.py              1e511978c251130e95169ebf8443efa1   idéntico
paintball/alma/decisor_zs.py
                            8fa03547e3228ef9df4aa94c444f9252   idéntico
paintball/alma/appraisal_zs_v42_exp.py
                            98c13d60167c80cc8334c965be75c640   idéntico
```

### La imagen

| | |
|---|---|
| etiqueta | **`gemv-anima:curforma-b0`** |
| id | `sha256:f9de3a17fd1861b8d6301e6e52a526b991196dbcc1fcdec9c107a8dfa7f4b3b4` |
| manifiesto | `sha256:3ddeb3040f1e302a4bef1a2aa4381cedf524a107265d6348b1ec4b3ad663cf71` |
| config | `sha256:08921c38ce0af12e06ae01836dbbdd56a60d64e89784bda5a90c986f77a6497b` |

md5 leídos **dentro** de la imagen:

```
alma/policy_forma.py       a6dd62bb366a81b85a0eede5ca9dbb20   (+ brazo K)
alma/curiosidad_forma.py   5e6074ee3a55acbd1a9c59ea3d610f0d   (el de P5-8A, sin tocar)
alma/humo_curforma.py      6da01dc0549e9b8aa9b2889643cab0c4
alma/curiosidad.py         f803f47c8ed0a8eaf3855d7e1dc7d457
```

Políticas: `gemv-p58b-A:v1` (`acac6ba6-777f-4da3-90b9-241719ba611b`) y
`gemv-p58b-K:v1` (`6c58dcc8-23ea-4353-a50d-fe1654b47fe1`, con `GEMV_FORMA=1`,
`GEMV_CURIOSIDAD_FORMA=1`, consigna 0,5, refractario 50).
**Ninguna llama a ningún modelo.**

---

## Los humos, y los dos fallos que cazaron antes de gastar

```
  (a) APAGADO identico: 200/200 decisiones · 0 registros de curiosidad-forma
  (b) el brazo K vive: 5 formas nacidas · 2 aceptadas · 2 caidas ·
      200 registros `cur_forma_tic`
      forma 2 -> destino (23, 21): distancia 5 -> 3 en 24 tics
  (c) VETO DURO: sin armado False · con un armado sobre el camino True
```

**Fallo 1, el que importa.** La primera versión daba **174 formas nacidas y cero
aceptadas**, cuando en seco pasaba el 37 %. Mi humo lo dio por bueno **porque
solo exigía que nacieran** — el mismo error de P5-7A, repetido. La causa: los
puntos de control se calculaban con un registro aplanado sin `tick`, `pack` ni
`hand`, así que `estado_de` devolvía un estado roto, los tics no casaban y **el
renglón nunca entraba en la proyección**. Corregido usando el mismo `e0` que usa
`_juzga`. **Y endurecí el humo para que se caiga si nacen formas y no pasa
ninguna**: un mecanismo que nace y nunca pasa la puerta es un mecanismo muerto.

**Fallo 2.** El lanzador derivado por `sed` **no sustituyó los brazos** y seguía
apuntando a las políticas de P5-7C. Se vio en la salida en seco antes de lanzar;
reescrito y verificado con asertos de que los ids nuevos están y los viejos no.

---

## Lo que la sonda comprueba

### Precio

| brazo | precio | contra los 0,04-0,08 «normales» |
|---|---|---|
| **A** | **0,050174 $** | dentro |
| **K** | **0,107574 $** | **por encima** |

**K cuesta el doble que A y sale del rango declarado.** No es alarmante —en
P5-7C el brazo Q llegó a 0,129 $ y la mediana de la serie fue 0,056— pero **es
un dato, no ruido**: K vive más tics de pod. Con 0,107 $ por partida, las
cuarenta saldrían por **~3,2 $**, todavía bajo el tope de 4 $ de K7, pero **sin
margen**.

### El hilo y el tiempo

| asiento | tics vivos | **perdidos** | ms mediana | ms máx |
|---|---|---|---|---|
| A/10 | 8.061 | **0** | 6,412 | 44,909 |
| A/11 | 8.151 | **0** | 0,556 | 22,856 |
| K/10 | 7.888 | **0** | 1,126 | 47,239 |
| K/11 | 7.917 | **0** | 0,711 | 186,681 |

**Cero tics perdidos en los cuatro asientos.** El BFS ya no corre cada tic, y se
nota: **K va más rápido que A** en la mediana. *(El 6,412 de A/10 es del brazo
sin nada añadido; lo anoto como variación de la máquina, no como coste del
mecanismo.)*

### El brazo K vive, y el diario lo registra

| | K/10 | K/11 |
|---|---|---|
| formas nacidas | 145 | 162 |
| **aceptadas** | **1** | **38** |
| caídas | 1 | 37 |
| registros `cur_forma_tic` | 7.888 | 7.917 |
| tics con forma activa | 24 = 0,3 % | 909 = **11,5 %** |
| **con armado a tiro y forma activa (K3)** | **0** | **0** |

**El registro por tic está y trae la forma activa, su destino y su causa de
fin**, que era la condición para que las cuarenta se puedan leer.

**K3 se cumple en la sonda: cero.**

### Y el defecto

| | |
|---|---|
| vida de las formas aceptadas | **mediana 25 · mín 25 · máx 25** |
| causa de caída | **«en la reevaluación deja de ganar», el 100 %** |
| abandonos por **veto duro** | **0** |
| abandonos por **atasco** | **0** |
| `cur_forma_saltada` (sin frontera / armado a tiro) | **0** |

**Ninguna forma sobrevive a su primera reevaluación**, así que ni el veto duro ni
el atasco llegan a tener ocasión de disparar. Los dos contadores nuevos están a
cero **no porque el mundo sea benigno, sino porque la forma ya está muerta
cuando les tocaría opinar.**

La tasa de aceptación al nacer, **39 de 307 = 12,7 %**, también queda muy por
debajo del 37 % del seco. Parte puede ser el mundo vivo; parte es que en seco la
puerta se evaluaba una sola vez por forma y aquí compite con un cuerpo que se
mueve.

---

## Los sellos de las cuarenta, con lo que la sonda ya dice

**No se cotejan**: son sellos de la serie, no de la sonda. Pero dos ya están
comprometidos por el defecto:

| | sello | lo que la sonda anticipa |
|---|---|---|
| **K3** | cero decisiones con armado a tiro y forma activa | **0 y 0** — camino despejado |
| **K4** | completadas ≥50 %; veto duro entre 5 y 30 % | **completadas ~0 %, veto duro 0 %** — fallaría **por el defecto**, no por el mundo |
| **K6** | <5 ms y cero perdidos | **cumple holgado** (0,7-1,1 ms, cero perdidos) |
| **K7** | ≤4 $ | **~3,2 $ proyectados** — cumpliría, pero **sin margen** |

---

## Lo que no sé, marcado como tal

**No sé cuánto de la caída en la aceptación (37 % → 12,7 %) es el defecto y
cuánto es el mundo vivo.** El defecto afecta a la reevaluación, no al
nacimiento, así que en principio no debería tocar la tasa de aceptación — pero
la diferencia entre los dos asientos de K (1 de 145 contra 38 de 162) es tan
grande que no me atrevo a atribuirla sin más datos. **Con dos partidas no hay
con qué.**

**No sé si el veto duro y el atasco funcionan en vivo.** Sus contadores están a
cero, pero nunca tuvieron ocasión. El humo (c) prueba que la función
**discrimina**; que dispare en el campo está **sin probar**.

**El precio de K por encima del rango es un dato con n=1.** Una partida.

---

## Propuesta, no ejecución

**El arreglo es de una línea y media**: envolver `F._d2` con el mismo renglón
también en la reevaluación —dentro de `_juzga`, no solo en `_cita_curiosidad`—,
de modo que **la puerta juzgue y re-juzgue con la misma regla**. Es lo coherente
con el diseño: si el renglón es parte de cómo se valora la forma, lo es también
cuando se comprueba si sigue valiendo.

Eso obliga a **imagen nueva con etiqueta nueva** y a **repetir la sonda**, como
manda la regla que fijaste.

**Mi recomendación: arreglar y volver a sondar antes de las cuarenta.** Lanzarlas
ahora costaría ~3,2 $ y mediría una curiosidad que no completa ningún trayecto,
que es justo lo que esta serie venía a medir.

**No lo he hecho.** El encargo dice PARA después de la sonda, y esto es una
decisión de la mesa.

---

## Custodia de los ficheros

| fichero | md5 |
|---|---|
| `cantera/paper5/curiosidad_forma.py` | `5e6074ee3a55acbd1a9c59ea3d610f0d` |
| `paintball/alma/policy_forma.py` | `a6dd62bb366a81b85a0eede5ca9dbb20` |
| `paintball/alma/humo_curforma.py` | `6da01dc0549e9b8aa9b2889643cab0c4` |

Gasto: **132,997267 → 133,155015 $**, diferencia **0,157748 $** = las dos
partidas. Cola vacía antes y después.

**PARO AQUÍ.**
