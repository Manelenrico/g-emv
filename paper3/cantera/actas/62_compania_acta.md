# Acta — LA COMPAÑÍA · **PARAR: CANDADO** (las dos anclas son incompatibles)

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_62_la_compania.md` · Banco, **coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **Alma efectiva: v32, bit a bit** (`appraisal_zs.py adccf4fd…`; el decisor
  no se tocó). S-COMPANIA queda **construida y APAGADA**
  (`COMPANIA_ON=False`) con el motivo grabado en la tabla.

---

# EL VEREDICTO, PRIMERO

**Las dos anclas que la mesa selló son incompatibles**, y el barrido lo cierra
sin ambigüedad:

- **Por debajo de techo 0,22 la fila no cambia NADA** — ni junta (en la escena
  tangencial ambos brazos acaban a 11,7), ni quita.
- **De 0,22 en adelante lo ÚNICO que cambia es que PIERDE COMIDA**: la ración
  a 2 casillas en dirección opuesta a la hermana — v32 la coge, v33 no. El
  ancla 2 ("la compañía no debe hacer pasar hambre") se rompe.

**No hay ventana entre "inerte" y "hambre".** Es el candado del 46, otra vez.
**PARAR ejecutado**: la fila queda apagada, el banco verifica el estado
aparcado y reproduce la brecha. El 63 hereda **v32**, no v33.

Y el hallazgo que explica por qué no hacía falta: **el anillo ya las junta.**

---

# A · LA FILA, TAL COMO QUEDÓ (construida, apagada)

- **Dispara**: en calma (ni yo ni ella con agresor activo) y con **el anillo
  sin morder**, la distancia a la hermana por encima de **d0 = 2** (el alcance
  del don; la v19 vivía a 2,2) genera malestar de fondo, **lineal hasta el
  techo** en `d0 + COMPANIA_RANGO(6)`.
- **M** = `COMPANIA_TECHO`, barrido 0,05 → 0,5.
- **Alivio**: automático por el gradiente — la foto que mueve hacia ella baja
  la distancia y baja la fila. **Ni un candidato nuevo** (R2).
- **Componentes**: `(0.1, 0.1, 0.8)` — social puro.
- **Gate del anillo, corregido en banco**: `F-ANTICIPACION` vale **~0,2 de
  fondo en TODO el mapa** (todo arde al final), así que el gate no puede ser
  sobre su valor sino sobre la **inminencia**: la fila calla si mi casilla
  arde en < 5 s (`COMPANIA_ANILLO_S`). Hallazgo de método, declarado.

# B · LAS SIETE PRUEBAS (`alma/verifica_62.py`, VERDE)

| prueba | sello | resultado |
|---|---|---|
| **P1 SE JUNTAN EN CALMA** | sellado | **SE CUMPLE SIN LA FILA** — con la hermana hacia el centro, **v32 (sin compañía) ya acaba a 1-2 casillas** en los tres escenarios (d10, d7, diagonal). Y en la escena **tangencial** (ella NO hacia el centro) **ningún techo acerca**: 11,7 en los seis valores barridos |
| **P2 NO PASA HAMBRE** | sellado | **ROTO por la fila** — v32 coge la ración a 2; v33 la pierde desde techo 0,22 (0,05/0,10/0,15 → SÍ; 0,22/0,35/0,5 → NO). Reproducido como **medida del candado** |
| **P3 JERARQUÍA DEL MIEDO** | sellado | **VERDE** — bajo caza S-COMPANIA apagada por el gate; v33 `ir_centro` == v27 |
| **P4 EL ANILLO MANDA** | sellado | **VERDE** — con la casilla ardiendo en <5 s la fila no enciende (gate por inminencia) |
| **P5 SILENCIOS** | sellados | **VERDE** — sin hermana: **byte-idéntica a v27**; a ≤d0: S-COMPANIA calla en la obs real y misma decisión que v32. *(Declarado: las FOTOS de candidatos que se ALEJAN sí la encienden — eso es el gradiente, no un fallo)* |
| **P6 HONOR** | sellado | **VERDE** — escenas del 39/53: **byte-idénticas a v32**, tabú intacto |
| **P7 REGRESIÓN** | — | **VERDE** — bancos 13-61: **27/27**, 0 fallos; humo 3/3 (hash idéntico); determinismo 3/3; **0 iniciaciones** (196 decisiones) |

## Las dos tablas del candado

**El anillo ya las junta** (v32, sin fila, 8 tics de rollout):

| escena | distancia final v32 | v33 (techo 0,22) |
|---|---|---|
| d10, ella hacia el centro | **2,0** | 2,0 |
| d7, ella hacia el centro | **1,0** | 1,0 |
| d~7 diagonal | **1,0** | 1,0 |
| **tangencial** (ella no hacia el centro) | 11,7 | **11,7 a TODOS los techos** |

**Y lo único que la fila cambia es el hambre** (ración a 2, dirección opuesta):

| techo | 0,05 | 0,10 | 0,15 | **0,22** | **0,35** | **0,5** |
|---|---|---|---|---|---|---|
| ¿coge la ración? | SÍ | SÍ | SÍ | **NO** | **NO** | **NO** |
| ¿acerca (tangencial)? | no | no | no | **no** | **no** | **no** |

# INCÓGNITAS CON MÉTODO

1. **El anillo como imán social**: el hallazgo grande de este banco es que
   *"nada las junta"* (56) era cierto **en el juego temprano**, pero el anillo
   las junta gratis en cuanto empieza a cerrar — porque comparten destino.
   Método: medirlo en el campo (¿la distancia mediana cae con el tick?), sobre
   los diarios ya pagados del 60. No hacía falta fila para eso.
2. **La geometría tangencial** es donde la compañía haría falta y donde ningún
   techo aceptable llega. Si la mesa la quiere, no es esta fila: sería un
   candidato de reunión (ir_pareja con peso propio) — conducta, no fuerza, y
   choca con R2. Decisión de mesa.
3. **`COMPANIA_ANILLO_S = 5 s`** (gate por inminencia) queda como método
   reutilizable: cualquier fila social futura que deba callar bajo el anillo
   necesita este gate, no un umbral sobre F-ANTICIPACION.

# QUÉ QUEDA EN EL REPO

- `alma/appraisal_zs.py` (`adccf4fd…`) — S-COMPANIA construida + gate por
  inminencia + **candado `COMPANIA_ON=False` con el motivo grabado**.
- `alma/verifica_62.py` **nuevo** (`e4d2a562…`) — las siete pruebas; verifica
  el estado aparcado y reproduce la brecha (patrón del 46).
- **Alma efectiva: v32.** Liga: v19. El 63 hereda v32.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

El encargo pedía una fila que las juntara en calma, y el banco encontró que
la calma no la necesita: **el anillo hace el trabajo gratis**. Cuando la
hermana está hacia el centro —que es donde acaba estando todo el mundo, porque
el mundo se cierra— la v32 sin ninguna fila social termina a una o dos
casillas de ella. No por cariño: por geometría. Dos animales que huyen del
mismo fuego hacia el mismo sitio se encuentran.

Donde la compañía haría falta de verdad es en la geometría tangencial, cuando
ella está a la misma distancia del centro pero al otro lado, y ahí ningún
techo por debajo del hambre mueve la aguja: los seis valores barridos acaban a
once casillas y media, exactamente como sin fila. Para cruzar el mapa hacia
alguien hace falta una fuerza grande, y una fuerza grande deja de ser fondo y
se vuelve correa —y el precio se paga en comida, medido: la ración que estaba
a dos pasos y v33 abandona.

Así que la fila queda construida y apagada, con su motivo grabado, como el
acopio del 46 y el oyente del 53. Y se lleva un hallazgo mejor que ella misma:
la lección del 56 —"nada las junta"— era cierta solo del juego temprano. El
mundo tiene su propio imán social, y se llama anillo. Si la pareja necesita
estar cerca cuando la calma llega, quizá no haga falta enseñarle a buscarse:
basta con que el mapa se encoja, que es lo que el mapa hace.

---

## Reproducción

```bash
cd gemv-coworld
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_62   # las siete + candado
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7 53 54 56 59 61; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done  # P7: 27/27
```
