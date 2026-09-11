# Acta — EL CUIDADO A DISTANCIA (v30) · BANCO VERDE

Fecha: 2026-09-04 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_56_el_cuidado_a_distancia.md` · Banco, **coste 0**

# A · LOS OJOS DE MANEL, PRIMERO — las dos entregas del 55

**Entrega 1** — `ereq_331e254f`: don **t353** → la recoge **t419** → curada
**t607** (gemela10 → gemela11):
<https://api.observatory.softmax-research.net/v2/coworlds/replays/static/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/sha256%3Ac96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9/index.html?v=2#replay=https%3A%2F%2Fsoftmax-public.s3.amazonaws.com%2Freplays%2F85840773-4e35-49d5-8bd2-d1ef73416229.replay>

**Entrega 2** — `ereq_2502e92c`: don **t387** → la recoge **t430** → curada
**t479**:
<https://api.observatory.softmax-research.net/v2/coworlds/replays/static/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/sha256%3Ac96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9/index.html?v=2#replay=https%3A%2F%2Fsoftmax-public.s3.amazonaws.com%2Freplays%2F395c6f3f-4c68-4834-b130-8c004134e6f3.replay>

(Patrón del 38: visor hosted, abre sin sesión. Las gemelas son los asientos
10 y 11.)

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**. **Coste 0** (banco + diarios ya pagados).
- **v30 = v29 con S-HERIDO corregida**, de taller, efectiva en el repo
  (`appraisal_zs.py eb9f915e…`; decisor y policies SIN tocar). Interruptor
  de pareado `HERIDO_V30` (False = v29 bit a bit, patrón de la casa).

---

# B · EL FORENSE DE LA SEPARACIÓN (79 diarios; sin sellos)

Por tic VISTO con decisión real (no noop), contrastando cuándo la distancia
entre hermanas CRECE y cuándo ENCOGE:

| | CRECE (189 tics) | ENCOGE (185 tics) |
|---|---|---|
| elegido | mover 41 % · ir_objeto/botín 28 % · coger 22 % | ir_objeto/botín 39 % · mover 34 % · coger 16 % |
| fila M dominante | **R-CARENCIA 65 %** · F-DANO 13 % · S-HERIDO 11 % | **R-CARENCIA 71 %** · F-DANO 11 % · S-HERIDO 9 % |
| S-7 (agresor activo) | 44 % | 39 % |
| ir_pareja | **1 %** | — |

**La frase honesta**: la hipótesis fuerte de la mesa ("la pila las separa:
acopio → botín; muro → cada una huye por su lado") **se tumba** — CRECE y
ENCOGE son casi simétricos, la carencia/botín es la marea de fondo de AMBOS
sentidos y el muro no distingue (44 % vs 39 %). Lo que fija el fondo en 3,6
no es una fuerza que separa: es que **no hay ninguna que junte** — `ir_pareja`
gana el 1 % de los tics y nada tira de vuelta cuando la marea las aleja. El
cuidado del 54 solo pesaba viéndola, y de cerca. (Exactamente los agujeros
que este encargo corrige.)

# C · S-HERIDO CORREGIDA (v30) — tres arreglos, los tres de la espec del 54

1. **ARREGLO A — sabe sin ver**: la fila se alimenta del PARTE (hp **y
   posición**, ambos ciertos con caducidad 96 — R1 del encargo) esté la
   hermana visible o no. La vista solo **refina** (la posición de ahora
   manda; la banda critical da estimación si no hay parte).
2. **ARREGLO B — la ayuda servible**: la cura "servida" cuenta SOLO si ELLA
   puede cogerla: con agresor activo declarado en su parte (a1 con ax,ay),
   la casilla debe quedar **más cerca de ella que de él y no adyacente a él**
   (la venda pegada a su cazador del 55 ya no calma a nadie). a1 SIN
   posición → nada certificable → no se alivia (conservador, declarado).
3. **ARREGLO C — el camino de ayuda**: hermana **en banda (<30)** y fuera de
   alcance (>2) → la foto de un move que ACERCA a su posición del parte
   alivia **parcialmente** (`CAMINO_GANA=0.5`, proporcional al progreso;
   jamás total). **La jerarquía del miedo por encima**: con agresor activo
   sobre MÍ (ventana S-7), el camino se apaga entero — bajo caza nada compra
   riesgo.

Constantes nuevas: `CAMINO_BANDA=30` [impl, la banda de la casa],
`CAMINO_GANA=0.5` [impl, calibrado en banco]. Reparto de la fila: intacto
(0.15, 0.25, 0.6). R2: ni un candidato nuevo, ni una conducta escrita — el
decisor no se tocó.

# D · LAS SEIS PRUEBAS CONTRA SUS SELLOS (`alma/verifica_56.py`, VERDE)

| prueba | sello | resultado |
|---|---|---|
| **P1 LA HERMANA INVISIBLE** (el banco que faltó en el 54) | sellado | **VERDE** — parte h20 con posición, calma, botiquín: v29 la ignoraba (S-HERIDO=0; elegido acaba a 14,8 de ella) → **v30 la sabe (M=1,34) y se acerca: acaba a 1,0** de 6,0 |
| **P2 EL DON SERVIBLE** | sellado | **VERDE** — la foto del 55: v29 se daba por aliviada (M 0,20); **v30 no (M 1,34)**. Soltar desde casilla servible **GANA** (v29: perdía); pegado al cazador **PIERDE** (margen +0,76) |
| **P3 JERARQUÍA DEL MIEDO** | sellado (PARAR) | **VERDE** — perseguida con hermana en banda a distancia: v30 elige `move_SE` == v27; el camino APAGADO bajo caza (sin `_herido_camino`) |
| **P4 SANO Y SOLO** | sellados | **VERDE** — h75/h60: v30 **byte-idéntica** a v29; caza-sin-hermana y paseo: **byte-idéntica a v27** |
| **P5 HONOR** | sellado | **VERDE** — escenas del 39/53 con parte (h10/h28/h72, g1 y g4): v30 **byte-idéntica** a v29 — márgenes de atacar y tabú intactos |
| **P6 REGRESIÓN** | — | **VERDE** — bancos 13-55: **23/23**, 0 fallos; humo determinista 3/3 (hash idéntico al de antes del encargo); determinismo del banco 3/3; 0 iniciaciones (31 decisiones) |

Cambios declarados en la regresión: ninguno — los mundos viejos no tienen
partes y la banda critical sola estima 33 ≥ 30, así que el camino no puede
encenderse por banda (honesto por construcción: la banda no garantiza
"en banda").

# INCÓGNITAS CON MÉTODO

1. **El camino alivia hacia la posición del PARTE** (≤96 tics de vieja): si
   ella corre, la portadora camina a donde estuvo. Es lo cierto disponible
   (R1); el parte siguiente corrige. Se verá en el campo (57) con la vara de
   distancia.
2. **CAMINO_GANA=0.5 es de banco**: el campo dirá si el tirón basta contra
   la marea de carencia/botín que el forense B señala como fondo.
3. **a1 sin posición → sin alivio**: conservador; si el campo enseña muchos
   partes a1 sin ax,ay (agresor no visible para ella), la mesa decidirá.

# QUÉ QUEDA EN EL REPO

- `alma/appraisal_zs.py` (`eb9f915e…`) — S-HERIDO v30 + constantes del
  camino + interruptor `HERIDO_V30`.
- `alma/verifica_56.py` **nuevo** (`d3cf0605…`) — las seis pruebas.
- `separacion.py` **nuevo** (`97cf4b98…`) — el forense de B.
- Alma efectiva de taller: **v30**. Liga: v19. El campo (57) puede
  escribirse: este acta está en verde — con sus varas selladas (dones ≥50 %,
  top-4 ≥35 %, juntas >15 %) **y la vara nueva: distancia mediana entre
  hermanas (baseline v29 5,1 en banda / 3,6 de fondo; v19 2,2)**.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

El forense dejó la foto más simple de todas: a las gemelas no las separa
nada — es que no las junta nada. La carencia y el botín son la marea de
fondo en los dos sentidos, el muro ni aparece, e ir hacia la hermana ganaba
el uno por ciento de las veces. El 3,6 no era una fuerza: era un vacío.

Los tres arreglos llenan ese vacío sin inventar nada que el 54 no hubiera
especificado ya. El cuidado ahora sabe sin ver, porque el parte trae la
posición y la posición es cierta noventa y seis tics. La ayuda solo cuenta
si ella puede cogerla — la venda pegada al cazador deja de calmar
conciencias. Y cuando está en banda y lejos, acercarse alivia: no como
conducta escrita, sino como el mismo descenso homeostático de siempre, con
el miedo sentado encima para que bajo caza nada compre riesgo — el banco lo
verificó byte a byte.

La imagen del banco P1 es la que este encargo vino a comprar: la hermana
invisible dice "veinte de vida" desde seis casillas, y donde v29 se iba al
botín, v30 camina hacia ella y acaba a una casilla. Si eso pasa en el campo
tantas veces como en el banco, la vara de distancia lo dirá en el 57 — y
con ella, quizá, las otras tres.

---

## Reproducción

```bash
cd gemv-coworld
python3 paintball/separacion.py                                   # B
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_56   # D
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7 53 54; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done  # P6: 23/23
```
