# Acta — LA PAREJA, TERCERA TANDA (v31) · P2 FALLA → AUTOPSIA (bug + el animal no acumula)

Fecha: 2026-09-04 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_60_la_pareja_tercera_tanda.md`

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **Coste**: imagen `gemv-anima:v10` (v31, hashes del 59 verificados en el
  build) + tanda `xreq_990e6723-…`, 40 episodios. **`cost_preview` = 20 cr**
  (≤ tope 30). Cosecha 40/40 resultados, **80/80 diarios**, 0 fallos.
- **Gasto acumulado del encargo: 20 cr. Una re-tanda serían 40 > 30 → la
  regla del tope la prohíbe: NO se re-lanza** (abajo, por qué y qué queda).
- Tras la autopsia, el **código v31 se corrigió** (bug de conteo); los hashes
  del repo cambian respecto al 59 (`appraisal 13072e01…`, `decisor
  ce0e8bbc…`). La imagen desplegada `gemv-anima:v10` llevaba el bug: **el
  campo midió un v31 con la provisión MUDA**. Declarado.

---

# EL VEREDICTO, PRIMERO

**P1 se sostiene** (0 iniciaciones, 0 ataques elegidos a la hermana,
S-VINCULO 0). **P2 falla** (entregas en calma: 0). Regla sellada: *"P2 falla
→ autopsia (¿la condición no ocurre? ¿soltar pierde? ¿ella no recoge?) antes
de nada."* La autopsia da **dos causas**, y la segunda es la de fondo:

1. **Un bug de conteo** (el desplegado): el botiquín se **APILA** (n=2 en UN
   slot); yo contaba SLOTS, así que `_bot_real=1` con una pila de dos, el
   gate `≥2` fallaba y **S-PROVISION quedó muda todo el campo**. El banco 59
   no lo vio porque usó dos slots `n=1`. **Corregido** (conteo por unidades)
   + guard de pila en el banco.
2. **El animal no acumula** (la causa profunda, que el arreglo NO cura):
   llevar **2+ vendas ocurre el 0,6 % de los tics** (614 de 106.066).
   R-CARENCIA satura con una sola venda, así que nada empuja a por la
   segunda. La ocasión completa (yo ≥2, hermana b=0, calma) ocurre en **1 de
   40 episodios**. **La provisión espera un estado que el resto de la tabla
   nunca produce.**

No es "EL DON SE ADELANTA" (exige P2). Es: **la provisión no puede llegar al
campo mientras el animal no lleve una venda de más — y hoy no la lleva.**

---

# LA OCASIÓN, CONTADA PRIMERO (V2 — "sin esto no hay vara")

Recomputada de los 80 diarios con conteo por UNIDADES (el correcto):

| ingrediente | frecuencia |
|---|---|
| llevo **≥2 unidades** de venda | **0,6 %** (614 tics) · ==1: 16,8 % · 0: **82,6 %** |
| parte fresco presente | 72,4 % · de esos, **hermana b=0: 80,7 %** |
| calma (S-7 apagada) | 79,2 % |
| **LA OCASIÓN** (≥2 ∧ b=0 ∧ calma) | **367 tics, en 1 de 40 episodios** |

El cuello es el primero: **el animal casi nunca lleva dos.** La hermana está
desabastecida el 80 % del tiempo (hecho social), y hay calma el 79 % — pero
para DAR ANTES hay que tener de sobra, y la riqueza se sacia con una.

# LAS VARAS (pareado v31 / v30 del 57, método idéntico)

| vara | sello | v31 | v30 (57) | veredicto |
|---|---|---|---|---|
| **P1 V1 honor** | 0 y 0 | 778 ataques · **0 inic** · 0 ataques-a-hermana elegidos · S-VINCULO 0 · (1 golpe de proyectil, física) | 0/0 | **SE SOSTIENE** |
| **P2 V3 entregas calma** | ≥50 % de eps con ocasión | **0** (provisión muda por el bug) | 0 (n/a) | **FALLA** |
| P3 V4 banda con venda | sube vs 57 | 11 % | 13 % | (provisión inerte: sin efecto) |
| — V5 distancia | reporte | 3,2 · banda 2,0 · ≤2 **56 %** · juntas8 10 % | 3,6 · 2,2 · 36 % · 8 % | variancia (v31≡v30 de conducta) |
| — V6 moneda | reporte (R12) | top4 10 % · wins 1 · podio 0 | 12 % · 1 · 1 | empate/ruido |
| **P4 V7 estabilidad** | sin degradación | cooldown 0 · congelado 0 | 0 · 0 | **SIN DEGRADACIÓN** |

**El 1 golpe entre hermanas es física de proyectil, no conducta** (P1
intacto): en `ereq_394f700e` t506 la gemela P11 eligió `atacar_SW` contra el
**slot 12** (enemigo con `era_agresor=true`, le había hecho 88 de daño;
`es_la_pareja=false`); el cuchillo alcanzó a la hermana en la línea de tiro
(la regla de interposición del 40). Ningún ataque ELEGIDO sobre la hermana;
el tabú nunca hizo falta.

**Las diferencias de distancia (56 % vs 36 % a ≤2) son variancia de tanda**,
no efecto de la provisión: con el bug, v31 ≡ v30 de conducta. La tabla del 51
avisa (a n=40 solo se ve lo que gana el 72 %); estas cifras no son señal.

# POR QUÉ NO SE RE-LANZA (y qué queda sellado)

Una re-tanda con la imagen corregida costaría otros 20 cr → **40 > 30, el
tope lo prohíbe**. Y la autopsia dice que **no cambiaría el veredicto de
fondo**: aun sin bug, la ocasión es 1/40 porque el animal no acumula. Un
re-lanzamiento mediría S-PROVISION encendida en ~1 episodio — P2 podría dar
verde sobre **n=1**, un sello frágil que no demuestra nada. Lo honesto:
**dejar el arreglo commit­eado y sellar la lección**, no gastar el doble para
un sí de un episodio.

# LA LECCIÓN, SELLADA (para la mesa)

La provisión "dar antes" está **correctamente construida** (el banco lo
prueba, ahora con guard de pila) pero **es inalcanzable con la tabla actual**
por una razón limpia: **DAR de más exige TENER de más, y el animal no tiene
de más.** Dos caminos para la mesa, declarados, ninguno hecho aquí:

1. **Enseñarle a acumular una segunda venda** — una R-ACOPIO que no se sacie
   en una (llevar dos como reserva), condicionada quizá a la hermana
   desabastecida. Es tabla nueva; y roza la lección del 46 (que no se vuelva
   acaparamiento).
2. **Aceptar que la provisión es para un mundo con más botín** — si una tanda
   futura sube `ffaLootCount`/densidad de vendas, el surplus aparecería solo.
   No depende de nosotros.

# INCÓGNITAS CON MÉTODO

1. **El re-lanzamiento corregido** (1 episodio de ocasión): queda como primer
   paso del 61 SI la mesa quiere el sí-de-un-episodio, dentro de su propio
   tope. El código ya está listo.
2. **¿Cuánto duraría una pila de 2 en la práctica?** — el animal usa la venda
   al entrar en banda; una reserva de 2 se gastaría en la primera herida. La
   provisión y el auto-cuidado compiten por la misma venda. Material de sofá.
3. **R-ACOPIO-por-dos en el campo con el bug**: contaba slots, así que una
   pila de 2 daba `_bot_foto=1` → por-dos encendida (0,10) cuando no debía.
   Efecto ínfimo (el animal ya recoge botín); corregido. Declarado.

# QUÉ QUEDA EN EL REPO

- `runs/pareja3/` — episodios.json (cost_preview 20), 40 res_, 80 diarios,
  resumen.json · `runs/xp_pareja3_v31.json`.
- `pareja3.py` (V1-V7 + la ocasión) · el arreglo de conteo en
  `appraisal_zs.py`/`decisor_zs.py` + guard de pila en `verifica_59.py`.
- **Bancos 13-59: 25/25 verde; humo 3/3.** `gemv-anima:v10` (con el bug)
  queda subida y declarada; el código del repo está corregido. Liga v19.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

La tercera tanda salió a comprobar si el don que se adelanta llegaba al campo,
y encontró dos cosas: un descuido nuestro y una verdad del animal.

El descuido primero, porque es el que hay que confesar sin rodeos: el
botiquín se apila, dos unidades caben en un hueco, y yo estaba contando
huecos en vez de vendas. Con una pila de dos, el animal creía llevar una, y
la fila que solo despierta con dos no despertó ni una vez en cuarenta
partidas. El banco del 59 no lo cazó porque en el banco puse dos vendas en
dos huecos, limpio y falso; el campo, que apila como apila el mundo real, lo
destapó al primer intento. Está arreglado, y el banco ahora lleva una pila de
dos de guardia para que no vuelva a pasar.

Pero arreglarlo no cambia el fondo, y el fondo es más interesante que el bug.
Aunque contara bien, la ocasión de dar antes ocurre en una de cada cuarenta
partidas, porque el animal lleva dos vendas el medio por ciento del tiempo.
No es que no quiera compartir: es que no tiene qué. Su riqueza se sacia con
una sola venda, así que jamás va a por la segunda, y sin segunda no hay nada
que adelantar. Construimos una generosidad que presupone abundancia en un
animal que vive al día. La fila es correcta y está esperando un mundo —o un
carácter— que le dé de sobra.

Así que no gastamos el doble para arrancarle un sí de un episodio. Dejamos el
arreglo puesto, sellamos la lección —dar de más exige tener de más— y se la
pasamos a la mesa con dos caminos y ninguna prisa. El honor aguantó,
cuarenta partidas más sin pegar primero, con el único golpe entre hermanas
salido de un cuchillo que iba a otro sitio. La pareja se cuida cuando puede;
todavía no puede darse lo que no acumula.

---

## Reproducción

```bash
cd gemv-coworld
python3 paintball/pareja3.py         # V1-V7 pareado v31/v30 + la ocasion
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_59  # con guard de pila
# tanda: xreq_990e6723…, cuerpo en runs/xp_pareja3_v31.json (cost_preview 20)
# autopsia de la ocasion: conteo por unidades sobre runs/pareja3 (inline en el acta)
```
