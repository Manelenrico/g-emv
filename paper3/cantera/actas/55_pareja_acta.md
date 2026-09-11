# Acta — LA PAREJA QUE SE HABLA (campo de la temporada dos) · P2 FALLA → ANATOMÍA

Fecha: 2026-09-04 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_55_la_pareja_que_se_habla.md`

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19** (no se tocó; la pareja no es promocionable).
- **v29 sin tocar desde el 54**: `appraisal_zs.py f3f2876c…`,
  `decisor_zs.py f4c315a7…` — los del acta del peso, intactos.
- **Coste**: subida `gemv-anima:v8` (imagen v29, custodia del motor dentro
  del build) + tanda `xreq_72266b8a-fb64-49b9-9867-5799fa903758`, 40
  episodios privados, sin inscribir. **`cost_preview` = `None`** — y también
  es `None` en las tandas viejas COMPLETADAS: el campo quedó vestigial en la
  plataforma (no hay endpoint de saldo; declarado). Sostienen el lanzamiento
  la certificación de Manel (los créditos son asignación gratuita, jamás
  cobrados) y la forma idéntica a las tandas validadas (34/49/50). La cifra
  del tope queda **sin verificar por causa de plataforma**, declarado.
- Cosecha: 40/40 resultados; **79/80 diarios** (el a10 de `ereq_948ddde1` lo
  perdió la plataforma: *"pod deleted before log collection"* — declarado).
  Mecanismo sobre 39 episodios; moneda sobre los 40.

---

# LA TANDA

Dos **gemv-anima:v8 (v29)** en los asientos 10-11 (la misma pareja: equipos
por asientos contiguos, roster del 32B/34) contra campeones `top_n 15`.
40 episodios, 0 fallos, ~4 min de mundo. Baselines: los dos boletos del 51B
(pareja v19, 100 pares de 33/34+42) — y el V3 que faltaba, **calculado aquí
de esos mismos res_: ambas vivas a 8-en-pie = 15/100 = 15 %** (cotejado: el
mismo universo reproduce el 21 % top-4 y el 1 % de podio del 51B exactos).

# VARAS CONTRA SELLOS, UNA A UNA

| vara | sellado | medido (40 eps) | veredicto |
|---|---|---|---|
| **P1 = V1 honor** | 0 y 0 iniciaciones | 444 ataques, **0 iniciaciones**, **0 ataques a la hermana**, **0 golpes entre hermanas** | **CUMPLIDA** |
| **P2 = V4 dones** | don en ≥ 50 % de los eps con hermana en banda + otra viva con botiquín | 19 eps con la condición, don tras la entrada en **3 (16 %)** | **FALLA** |
| **P3 = V2 moneda** | top-4 del mejor ≥ 35 % | **15 %** (6/40) — bajo hasta el baseline (21 %) | **FALLA** |
| **P4 = V3 juntas** | ambas a 8-en-pie > 15 % (baseline calculado) | **10 %** (4/40) | dirección **negativa** |

Resto de la moneda (contexto, no sellos): victorias 3/40 = **8 %** (base
4 %) · podio doble 1/40 = **2,5 %** (base 1 %) · placement mediano del mejor
10,0 · del peor 14,0. A n=40 y con la tabla del 51 delante (R12), ni las
subidas ni las bajadas de este tamaño son señal — **el 35 % sellado era el
umbral demostrable y no se alcanzó**; lo único fuera de duda es que NO hay
salto grande.

**V5 estabilidad**: cooldown mediana 0 · congelado 0 · banda/diario 60 tics.

## El mecanismo SÍ está vivo (V4)

- **La voz funciona**: partes E1 emitidos mediana **16/diario**, leídos de la
  hermana 9/diario, y la radiografía lleva **parte fresco en mediana 423
  tics/diario** — el modelo del hermano SABE casi siempre.
- **El cuidado dispara**: S-HERIDO encendida **6.769 tics** (M máx 2,45).
  S-VINCULO: **0 tics** — jamás hubo foto de matar seguro a la hermana (como
  debe ser, con 0 ataques entre ellas).
- **El don EXISTE en el campo**: 12 soltares de botiquín en 10 episodios —
  el "casi mudo" del 27 ya habla. **Dos entregas completas, para verlas con
  los ojos**:
  - `ereq_331e254f-fca0-4f19-9f53-c75bdaf66faf`: don t353 → la hermana lo
    recoge t419 → **curada t607**
    (replay `…/85840773-4e35-49d5-8bd2-d1ef73416229.replay`)
  - `ereq_2502e92c-5119-4d41-95c8-21205c35856c`: don t387 → recogida t430 →
    **curada t479**
    (replay `…/395c6f3f-4c68-4834-b130-8c004134e6f3.replay`)

# EL VEREDICTO SELLADO, APLICADO TAL CUAL

> *"P2 falla → el don no llega al campo: anatomía obligada (¿canal cortado?
> ¿distancia? ¿sin botiquín?) antes de nada."*

P1 se cumplió; P2 falló → **anatomía obligada, ejecutada** (P3/P4 quedan
reportadas arriba; el veredicto no admite relevo). No es "LA PAREJA ES UN
EQUIPO" ni "SE CUIDAN Y NO PUNTÚA": es **"EL DON NO LLEGA"**, con autopsia.

# ANATOMÍA DEL DON QUE NO LLEGA (`anatomia_don.py`)

1.528 tics-de-decisión con la hermana EN BANDA y la portadora viva con
botiquín (12 episodios de condición simultánea estricta):

| sospechosa | medida | veredicto |
|---|---|---|
| ¿canal cortado? | parte fresco en la radiografía: **100 %** de esos tics | **NO** — el canal está impecable |
| ¿sin botiquín? | condición ya exige botiquín a bordo | NO |
| ¿distancia? | mediana **5,1** entre hermanas; a **≤2** (alcance del alivio) solo el **2 %** de los tics | **SÍ — la primera causa** |
| ¿la ve? | pareja a la vista solo **39 %** de esos tics | **SÍ — y destapa el agujero A** |
| ¿candidato soltar? | existe en el 39 % (= exactamente cuando la ve) | consecuencia del anterior |
| ¿margen? | soltar pierde SIEMPRE (mediana **+0,527**; incluso a ≤2: **+0,498**) | **SÍ — y destapa el agujero B** |

## Los dos agujeros de fila, con nombre y foto

**A · SIN VISTA, SIN FILA.** `S-HERIDO` está gateada en `_pareja_ag` (la
hermana VISIBLE en la obs): sin vista, la fila es 0 **aunque el parte fresco
diga h20 y traiga su posición exacta**. En el campo: encendida solo el 39 %
de los tics de condición — exactamente el % de vista. El banco del 54 nunca
probó a la hermana invisible (todas las escenas la tenían delante). La
certeza sin vista hoy no pesa; el parte lleva posición cierta que la fila
ignora.

**B · EL ALIVIO SIN PREGUNTAR SI ELLA PUEDE.** La foto del tic
`ereq_36b6479b t539` (portadora a dist 2,0, herida a hp real 20): S-HERIDO
sale **aliviada (M 0,09 = 0,6 × 0,15)** porque hay un `first_aid` REAL a
**1 casilla de la herida**… **pegado al agresor** que la caza (el parte
marca a1 en [23,23]; el botiquín está en [23,23]-adyacente). El alivio del
54 lee "cura en el suelo a ≤2 de ella" sin alcanzabilidad DE ELLA (la A.2
del 13 solo excluye casillas pisadas) — y con la fila ya calmada, el soltar
propio no añade nada: margen +0,5 también de cerca. (Las raciones también
cuentan como "ayuda", mismo defecto en versión sándwich.)

**Y el hecho de fondo — C · ANDAN MÁS SEPARADAS**: distancia mediana entre
hermanas **3,6** contra el **2,2** de las v19 (y 5,1 en los momentos de
banda). El tránsito no se tasa (decisión sellada del 47/54, incógnita 2 del
peso declarada entonces): nada acerca a la portadora cuando la herida cae a
cinco casillas. La v29 —muro, cuesta, acopio— parece además vivir más
suelta que la v19; sin medir la causa, declarado.

# INCÓGNITAS CON MÉTODO (el material del sofá)

1. **Fila ciega sin vista (A)**: dejar que S-HERIDO lea posición y estado del
   parte fresco cuando no la ve — es el mismo hecho cierto; el banco del 54
   se ampliaría con la escena de la hermana invisible. Decisión de mesa.
2. **Alcanzabilidad del alivio (B)**: exigir a la "ayuda servida" lo que la
   A.2 exige al don propio (casilla pisable, y quizá lejos del agresor
   activo conocido por parte). Decisión de mesa.
3. **El tránsito (C)**: "acercarme si la ayuda exige alcance" quedó fuera en
   el 54 (lección del 47); el campo dice que es la primera causa material.
   Si se tasa, la jerarquía del miedo (P3 del 54) tiene que resellarse igual
   de fuerte. Decisión de mesa.
4. **¿Por qué 3,6 y no 2,2?** — comparar aperturas v29 vs v19 en replay
   (instrumento del 51 listo). Sin gastar: los replays ya están pagados.

# QUÉ QUEDA EN EL REPO

- `runs/pareja/` — episodios.json, 40 res_, 79 diarios, resumen.json.
- `runs/xp_pareja_v29.json` — el cuerpo de la tanda.
- `pareja.py` (V1-V5) · `anatomia_don.py` (la autopsia).
- Liga v19; v29 de taller intacta; `gemv-anima:v8` subida (imagen v29).

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

La pregunta del encargo era si dos que se hablan dejan de ser dos boletos, y
la respuesta honesta es: **todavía no — pero ya se sabe exactamente por
qué**, que es más de lo que este campo suele dar.

El honor salió perfecto en su primer campo social: cuatrocientos cuarenta y
cuatro ataques y ni una iniciación, ni un golpe entre hermanas, y el tabú
sin disparar ni una vez porque nunca hizo falta. La voz salió mejor que
perfecta: dieciséis partes por diario, el modelo del hermano sabiendo
cuatrocientos veintitrés tics de cada vida. Y el don —mudo desde el 27—
habló doce veces, y dos de ellas completó el gesto entero: soltar, que ella
lo recoja, que se cure. Esas dos escenas existen, tienen replay, y son lo
que la temporada dos vino a buscar.

Pero la moneda no se movió (quince por ciento donde el sello pedía treinta y
cinco), y la autopsia del don que no llega no encontró un culpable sino
tres, todos honestos: la fila del cuidado se apaga cuando no la ve —aunque
el parte le esté diciendo dónde y cómo está—; el alivio se calma con una
cura tirada junto al cazador, que ella jamás podrá coger; y las hermanas
viven a cinco casillas cuando una cae, porque nadie tasa el tránsito. Los
tres tienen nombre, foto y método. Ninguno se arregla en este acta: son
exactamente el material que la mesa pidió tener delante antes de decidir.

Dos boletos que se hablan siguen siendo dos boletos. Pero ahora uno de los
boletos sabe soltar el botiquín, y sabemos las tres piedras que le impiden
llegar a tiempo.

---

## Reproducción

```bash
cd gemv-coworld
python3 paintball/pareja.py          # V1-V5 contra los sellos
python3 paintball/anatomia_don.py    # la autopsia del P2
# baseline V3: pares v19 de runs/gemelos80 + runs/ocasion (coteja 21%/1% del 51B)
# tanda: xreq_72266b8a…, cuerpo en runs/xp_pareja_v29.json
```
