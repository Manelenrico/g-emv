# Acta — LA MANADA (v34) · BANCO VERDE · **el honor se parte en dos métricas**

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_63_la_manada.md` · Banco, **coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **v34 = v32 + la manada** (`appraisal_zs.py 11b7cea0…`, `decisor_zs.py
  136eb577…`). Interruptor `MANADA_ON` (False = v32 bit a bit).

---

# EL HONOR, DESDE HOY, SON DOS NÚMEROS

Este encargo cambia lo que "cero iniciaciones" significa, y hay que decirlo
con todas las letras antes que nada:

- **(a) INICIACIONES-ESTRICTAS** — atacar a quien **no ha agredido ni a mí ni
  a ella**: **0 siempre**. Hereda el nombre. Es el candado C2, y sigue siendo
  la promesa de la casa: *el animal nunca pega primero*.
- **(b) DEFENSAS-POR-LA-HERMANA** — primer golpe mío contra el agresor
  **certificado** de ella: **se cuentan y se dicen aparte**. No son
  iniciaciones: son defensa de la manada. En este banco: **7**.

La radiografía las distingue en origen: `honor.era_agresor` (me defiendo) y
`honor.defensa_pareja` (la defiendo). Una decisión sin ninguno de los dos
motivos sería una iniciación estricta — y no ocurre nunca.

# A · LA EXTENSIÓN (una)

`era_agresor` se amplía: **el agresor activo de mi hermana es mi agresor**,
pero solo si es CIERTO (R1) — las dos condiciones a la vez:

1. su **parte fresco** (≤96 tics) declara `a=1` **con posición** (ax,ay), y
2. hay un **enemigo visible** en esa posición, tolerancia **1 casilla**
   (`MANADA_TOL`, de la latencia +2 medida en el 52).

Sin las dos, no hay agresor certificado: **la manada no caza por rumores**.
Los candidatos `atacar_*` nacen contra ese slot como nacen contra el mío
(R2: ni un candidato nuevo) y S-7 los tasa con la misma receta, con una
**atribución declarada**: el "daño en ventana" que se le imputa es el
**déficit de vida de ella** (cierto por su parte), atribuido a quien su
propio parte señala como su agresor **ahora**. Es atribución, no certeza
histórica — declarado.

**La condición del arma** (hallazgo del banco, ver abajo): la presión
atribuida **solo cuenta con arma que daña en la mano**. Sin arma no hay
defensa posible, y entonces su pelea no debe asustarme.

# B · LOS CINCO CANDADOS (P3) — todos verdes

| candado | verificación |
|---|---|
| **C1 EL TABÚ** | `agresor_de_la_hermana` excluye a la pareja **por construcción**; un parte que apuntara a su propia casilla no la convierte en objetivo. S-VINCULO intacta. **0 ataques contra la hermana** en todo el banco |
| **C2 NUNCA CONTRA INOCENTES** | sin `a=1` en su parte: **0 candidatos** y foto **byte-idéntica a v32**. Con un tercero inocente a la vista mientras SÍ hay agresor certificado: **solo nace el candidato contra el cazador** |
| **C3 JERARQUÍA DEL MIEDO** | a hp ≤30 bajo caza propia, responder **pierde** (elige `usar_botiquin`): mi cuesta y mi muro mandan |
| **C4 CADUCIDAD** | las tres muertes del candidato verificadas: su parte pasa a `a=0` → muere; el parte envejece >96 tics → muere; el enemigo ya no está en (ax,ay) → muere |
| **C5 SILENCIOS** | sin hermana → **byte-idéntica a v27**; hermana en calma → **idéntica a v32**; si el mismo cazador también me caza a mí → **idéntico a v32** (y si responde, el motivo es `era_agresor`, no la manada) |

# C · LAS PRUEBAS

## P1 LA DEFENSA — **emerge del descenso** (no guionizada)

Escena declarada: los tres en contacto **en el centro y con el anillo
apretando** (T=300). *Motivo medido*: en campo abierto la **zancada** de
huida escapa de S-7 y S-8 a la vez y gana siempre —lo mismo que hundía al don
en el 57—, así que una escena abierta no prueba nada sobre la manada. Donde
la manada se juega el final es donde huir cuesta: **el cerco**.

| yo | v32 | **v34** | honor |
|---|---|---|---|
| hp 90 | `noop` (0 candidatos) | **`atacar_NE`** | `defensa_pareja=True`, `era_agresor=False`, objetivo 15 |
| hp 70 | `noop` (0 candidatos) | **`atacar_NE`** | ídem |

## P2 EL PRECIO DE MI VIDA — la frontera (radiografía, sin sello)

| mi hp | sin caza propia | bajo caza propia |
|---|---|---|
| 90 | **atacar_NE** (defiende) | move_S (huye) |
| 70 | **atacar_NE** | move_S |
| 50 | usar_botiquin | usar_botiquin |
| 40 | usar_botiquin | usar_botiquin |
| 30 | usar_botiquin | usar_botiquin |

**Sana defiende; herida se cura.** Nadie escribió ese umbral: sale de pesar
mi cuesta contra la presión de su cazador — la misma diagonal moral que el 61
dibujó para el don. Sellado: a hp ≤30 responder **pierde** (verificado a 30,
20 y 10).

# EL HALLAZGO DEL BANCO: la manada sin arma solo añadía miedo

La regresión del **56** lo destapó: en la escena del don servible (donde a la
hermana la cazan) v34 pasaba de `soltar` a `move` — **la presión atribuida
subía S-7 y empujaba a huir, desplazando el don**. Causa: sin arma en la mano
no puede nacer ningún candidato de respuesta, así que la manada solo aportaba
miedo ajeno. **Corregido**: la atribución exige arma que daña en la mano.
Con ella, sin arma, v34 es **v32 bit a bit** y el 56 vuelve a verde. Sin la
regresión completa esto habría llegado al campo como un animal más cobarde
justo cuando su hermana lo necesita.

# P5 REGRESIÓN

**Bancos 13-62: 28/28 verde**, 0 fallos (con el arreglo del arma; sin él, el
56 caía). Humo determinista **3/3** con el hash de siempre; determinismo del
banco 3/3; **iniciaciones-estrictas 0** en 33 decisiones.

# INCÓGNITAS CON MÉTODO

1. **La atribución del déficit**: imputar al agresor certificado toda la vida
   que ella ha perdido es generoso (pudo herirla otro antes). Alternativa
   medible: contar solo el daño desde que su parte lo declara. Requiere
   memoria por-agresor-de-ella; no se hizo. Si el campo muestra defensas
   desproporcionadas, es el primer dial.
2. **La escena del cerco**: P1 emerge con el anillo apretando. En campo
   abierto la huida sigue ganando — es coherente (defenderse juntos importa
   cuando no hay a dónde huir), pero significa que **las defensas del campo
   serán tardías**, del final de la partida. Declarado antes del 64.
3. **El riesgo del prompt** (juntas se cazan juntas; el proyectil de una
   alcanza a la otra, como el golpe del 60): **no se mide en banco**, se
   medirá en el campo con las varas del 64.

# QUÉ QUEDA EN EL REPO

- `alma/appraisal_zs.py` (`11b7cea0…`) — `agresor_de_la_hermana` (el
  certificador), S-7 extendida con atribución declarada + condición del arma,
  `MANADA_ON`/`MANADA_TOL`.
- `alma/decisor_zs.py` (`136eb577…`) — el candidato de respuesta nace también
  contra el agresor certificado; `honor.defensa_pareja` en la radiografía.
- `alma/verifica_63.py` **nuevo** (`b2776551…`) — P1-P5 y los cinco candados.
- Alma efectiva de taller: **v34**. Liga: v19. El campo (64) puede escribirse.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

Sesenta y dos encargos diciendo "cero iniciaciones" y hoy el número se parte
en dos, así que conviene decirlo despacio. El animal sigue sin pegar primero:
atacar a alguien que no ha agredido a nadie de las dos sigue siendo imposible
—no es que pierda, es que el candidato no nace—, y eso se llama ahora
iniciaciones-estrictas y vale cero, como siempre. Lo nuevo es que si un
cuerpo está golpeando a su hermana, y ella lo dice por radio con su posición,
y ese cuerpo está de verdad ahí donde ella dice, entonces ese cuerpo también
es su agresor. La manada no amplía a quién puede pegar: amplía por quién.

Y la defensa emerge donde tenía que emerger. En campo abierto no: la zancada
de huida escapa de todo y gana siempre, igual que hundía al don en el 57. Pero
en el cerco, con el anillo apretando y los tres en contacto, la v32 se queda
quieta mirando y la v34 responde. La frontera del precio salió igual de limpia
que la del 61: sana defiende, herida se cura, y nadie escribió el umbral.

Lo mejor del encargo, sin embargo, fue lo que rompió. La regresión del 56 pilló
que la manada, sin arma en la mano, convertía el peligro de la hermana en miedo
propio: subía la presión, empujaba a huir y desplazaba el don justo en la
escena donde el don era lo único útil. Un animal más cobarde precisamente
cuando ella lo necesitaba. La corrección es de una línea y de sentido común
—si no puedes defenderla, su pelea no debe asustarte— pero sin correr los
veintiocho bancos habría viajado al campo disfrazada de valentía.

---

## Reproducción

```bash
cd gemv-coworld
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_63   # P1-P5 + C1-C5
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7 53 54 56 59 61 62; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done  # 28/28
```
