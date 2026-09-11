# Acta — LA MEMORIA ACUMULADA (resello) · **la fila DECIDE**

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_71_memoria_acumulada.md` · Banco, **coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **v37 resellada** (`appraisal_zs.py 8a73bb30…`; el **decisor no se tocó**:
  ni un candidato nuevo). Interruptor `ACUMULADO_ON` (False = el v37 del 70).
- **Sin campo**: el 71-como-campo quedó descartado por el propio encargo
  (~7 casos por tanda no sellan dirección, R12).

---

# LA DECISIÓN QUE SALE (regla C, sellada antes del dato)

**P2 y P3 verdes → v37b ES la v37**: se sustituye, no se acumulan versiones.
El miedo con memoria queda como **fila que DECIDE**, con su n de banco (15) y
**sin campo** — y eso último se dice, no se esconde: a n=40 no sería
demostrable (R12).

---

# A · EL RESELLO, TAL COMO QUEDÓ

**Memoria**: asiento → (último tic que nos dañó, **daño ACUMULADO en el
episodio** a mí y a la hermana). Se guardan las dos cuentas —el golpe más
fuerte y el acumulado— y el interruptor elige cuál pesa; **todo lo que se
acumula es cierto** (R1): mi `damage_taken.source` y la caída de hp entre dos
partes v2 de la hermana. Si no se puede saber, no se inventa.

**Magnitud** de F-REENCUENTRO = el miedo que causaría ese daño acumulado, con
**la misma cuenta que F-DANO** (cuesta del 43) y **topado como F-DANO se
topa** (u ∈ [0,1]); escalado por cercanía igual que en el 70 (entera dentro
del alcance de su arma, mitad hasta 5 casillas, nada más lejos). **Sin latch,
sin doble cuenta** con F-DANO.

**El dato del campo que lo justifica**: el daño acumulado real de esos
asientos antes del reencuentro es **mediana 52, máximo 211** (extraído de los
diarios del 64+66), frente al golpe estándar de **18** que la v37 del 70
recordaba.

# B · LAS PRUEBAS (`alma/verifica_71.py`, VERDE)

| prueba | sello | resultado |
|---|---|---|
| **P1 LA MAGNITUD SUBE** | mediana > 0,18 | **VERDE** — v37 (último golpe): mín 0,00 · **mediana 0,17** · máx 0,26 → v37b (acumulado): mín 0,00 · **mediana 0,49** · **máx 1,40** |
| **P2 LA ACCIÓN CAMBIA** | ≥5 de 15, sin golpes | **VERDE — cambia en 8 de 15**, y las ocho hacia **distancia/pared**. **0 golpes nacidos de la memoria** (90 acciones revisadas) |
| **P3 NO PAGA CON COMIDA NI CURA** | candado 46/62 | **VERDE** — **0 tics** abandonando botín o cura, frente a **28 tics** ganando distancia. El miedo no le roba a la mesa lo que la mantiene viva |
| **P4 SILENCIOS** | byte a byte | **VERDE** — extraño armado nunca visto y arena vacía: **v37b == v36 byte a byte** |
| **P5 REGRESIÓN** | — | **VERDE** — bancos 13-70: **32/32**; humo 3/3 (hash de siempre); determinismo 3/3 |
| **P6 QUIÉN DIVERGE** | sin sello | tabla abajo |

## P6 · Quién diverge primero (R7)

| episodio | asiento | acum | tic | v37 → **v37b** | F-REENC |
|---|---|---|---|---|---|
| `ereq_653f64cd` | 14 | 178 | 1 | noop → **move_W** | 0,700 |
| `ereq_08440b30` | 2 | 99 | 2 | noop → **move_W** | 0,688 |
| `ereq_6f9704f8` | 5 | 211 | 1 | noop → **move_W** | 0,700 |
| `ereq_6f9704f8` | 5 | 198 | 1 | noop → **move_W** | 0,700 |
| `ereq_4b24cc53` | 7 | 66 | 1 | noop → **move_W** | 0,368 |
| `ereq_62651a32` | 15 | 60 | 1 | noop → **move_W** | 0,322 |
| `ereq_a62f7c2d` | 9 | 52 | 5 | noop → **move_W** | 0,533 |
| `ereq_f2570d5f` | 8 | 48 | 1 | noop → **move_W** | 0,487 |

**El patrón es uno solo y es el que se buscaba**: donde la v37 se quedaba
quieta mirando venir a quien ya le había hecho cincuenta, cien o doscientos
puntos de daño, **la v37b se aparta** — en el primer tic en siete de los ocho
casos. La fila que diverge es F-REENCUENTRO y la acción que gana es
alejarse. **Ni un golpe.**

# INCÓGNITAS CON MÉTODO

1. **Sin campo, y dicho**: la fila decide en banco sobre 15 fotos reales. Un
   campo de 40 episodios daría ~7 casos: **no sellaría dirección** (R12).
   Queda como conocimiento de taller, no como mejora demostrada.
2. **El tope**: con acumulados de 200 el `u` satura en 1,0 y la fila vale
   1,40 — el mismo techo que F-DANO. Un agresor que te hizo 200 y otro que te
   hizo 100 dan casi lo mismo. Correcto por diseño (así se topa el dolor
   real), pero significa que **la memoria no distingue verdugos de
   carniceros** pasado cierto punto.
3. **La hermana necesita dos partes** para que su caída de hp sea calculable;
   si el primero se pierde, ese asiento entra en la memoria con 0 y la fila
   queda muda aunque el nombre sea cierto. Medible solo en campo.

# QUÉ QUEDA EN EL REPO

- `alma/appraisal_zs.py` (`8a73bb30…`) — memoria con las dos cuentas
  (`dano` y `acum`), `ACUMULADO_ON`, y la magnitud sobre el acumulado.
- `alma/verifica_71.py` **nuevo** (`286ea65c…`) — P1-P6 con los daños reales.
- `runs/casos_exactos.json` — los 15 casos con su acumulado medido.
- Alma efectiva de taller: **v37 (resellada)**. Liga: v19.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

El 70 dejó una fila honesta y muda: se encendía cuando debía y no movía nada,
porque recordaba un golpe de dieciocho en una mesa donde ya pesan la cuesta,
el muro y el anillo. El vigilante señaló la única palanca que quedaba sin
tocar y el sofá la accionó: que la memoria recuerde **todo** lo que ese cuerpo
te hizo, no su último arañazo. Cuesta cero, y el dato del campo la justificaba
sola — los que vuelven te habían hecho cincuenta y dos puntos de mediana, no
dieciocho.

Con eso, la fila pasa de valer diecisiete centésimas a valer casi medio, y en
ocho de quince fotos **cambia lo que el animal hace**. Y cambia siempre en la
misma dirección, que es exactamente la que la casa quería y no supo pedir sin
escribirla: donde antes se quedaba quieta viendo venir a quien le había hecho
doscientos puntos de daño, ahora **se aparta**. En el primer tic, sin
guiones, sin un candidato nuevo, sin una sola línea que diga "huye": la
distancia gana sola porque el miedo por fin pesa lo que costó aprenderlo.

Los dos candados aguantan y son los que hacían falta. No hay ni un golpe
nacido de la memoria —noventa acciones revisadas— porque el miedo no crea
candidatos, solo mueve precios. Y no le roba a la mesa lo que la mantiene
viva: cero tics abandonando comida o cura frente a veintiocho ganando
distancia, que era la lección del acopio y de la compañía.

Queda una cosa por decir, y va sin adornos porque es la regla de la casa:
esto es un resultado de banco sobre quince fotos. Un campo daría siete casos
por tanda y no podría demostrar nada. La fila decide, está medida, y se queda
en el taller sabiendo exactamente lo que sabemos y lo que no.

---

## Reproducción

```bash
cd gemv-coworld
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_71   # P1-P6
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7 53 54 56 59 61 62 63 65 68 70; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done  # 32/32
```
