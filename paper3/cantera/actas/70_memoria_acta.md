# Acta — MIEDO CON MEMORIA (v37) · BANCO VERDE

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_70_miedo_con_memoria.md` · Taller y banco, **coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **v37 = v36 + F-REENCUENTRO** (`appraisal_zs.py f21f5568…`; el decisor **no
  se tocó**: ni un candidato nuevo, ni una acción condicionada a la memoria).
  Interruptor `REENCUENTRO_ON` (False = v36 bit a bit).

---

# LO QUE EL SOFÁ DECIDIÓ, Y LO QUE SE CONSTRUYÓ

El 69 midió que los agresores vuelven, pero que en el caso exacto —vuelve,
armado, se acerca— **él pega primero solo 7 de 15**. Por eso **no hay golpe
preventivo**: cuatro de cada diez caerían sobre quien no atacaba, y una
muerte en 138 reencuentros no lo paga (R9). Lo que se construye es **miedo**:
la ánima se asusta **antes** del golpe al ver venir armado a un agresor
conocido. **Sin una línea de conducta**: lo que salga del miedo —distancia,
pared, hermana, nada— lo decide el cuerpo.

# A · LA MEMORIA (`mem_agresores`)

Por episodio, una lista de asientos certificados: **asiento → (último tic en
que nos dañó, daño conocido)**. Dos fuentes, ambas ciertas (R1):

- **Mío**: `damage_taken.source` — certeza total sobre quién me pegó.
- **De la hermana**: el **asiento del parte v2**; el daño conocido es la
  **caída de hp entre su parte anterior y el nuevo** (cierto por su
  testimonio). Si no se puede calcular, **no se inventa** (queda en 0).

**Caducidad: TODO EL EPISODIO** — decidido con el dato del 69: el **54 % de
los gaps supera 96 tics**, así que una memoria corta se perdería más de la
mitad de los reencuentros. Se limpia al empezar episodio. Nada se escribe
fuera de la ánima.

# B · LA FILA F-REENCUENTRO (la cuenta exacta)

**Se enciende** cuando un asiento de la memoria está: **visible**, con **arma
visible que daña** (alcance ≥1), y **acercándose** (distancia decreciente en
tics consecutivos, o ya a ≤2).

**Magnitud** = el miedo que causó su último daño conocido, con **la misma
cuenta que F-DANO** (la cuesta convexa del 43):

```
u = daño_recordado / hp_max
M = u                                   si u ≤ 0,4
M = u + 0,4·((u−0,4)/0,6)²              si u > 0,4
M ×= 0,5    si está fuera del alcance de su arma
M  = 0      si está a más de 5 casillas
```

- **Sin latch**: se recalcula cada tic; se apaga sola cuando deja de acercarse
  o de verse.
- **Sin doble cuenta**: si ese asiento **ya me está dañando** (ventana S-7
  viva), **F-REENCUENTRO calla y manda F-DANO**. El miedo con memoria es para
  **antes** del golpe.
- Entra en **F** como cualquier otra fila (reparto `(0.8, 0.1, 0.1)`); no toca
  S ni R.

# C · LAS PRUEBAS (`alma/verifica_70.py`, VERDE)

Las 15 fotos del caso exacto se **parametrizan con los datos reales del 69**
(arma vista, distancia mínima, quién pegó primero) y se reconstruye la
aproximación tic a tic.

| prueba | sello | resultado |
|---|---|---|
| **P1 EL MIEDO LLEGA ANTES** | ≥12 de 15 | **VERDE — 13 de 15**. Los dos que no: distancia mínima > 5 casillas (**el miedo calla de lejos, por diseño**). **Adelanto mediano: 7 tics** antes de su primer golpe real |
| **P2 SIN GOLPE POR MEMORIA** | 0 de 6 | **VERDE — 0 golpes** en las seis fotos donde en el campo no pegó nadie |
| **P3 SILENCIOS** | byte a byte | **VERDE** — extraño armado nunca visto y arena vacía: **v37 == v36 byte a byte** |
| **P4 LA OTRA** | v2 sí / v1 no | **VERDE** — con parte v2 (asiento) se enciende **aunque a mí nunca me tocara** (M=0,180); con parte v1 (sin asiento) **no se enciende**: el respaldo por posición no certifica identidad |
| **P5 REGRESIÓN** | — | **VERDE** — bancos 13-69: **31/31**; humo 3/3 (hash de siempre); determinismo 3/3; **0 iniciaciones-estrictas** en 412 decisiones |
| **P6 QUÉ HACE EL CUERPO** | sin sello | **0 tics con la acción cambiada**: el miedo entra en la mesa pero **no gira la decisión** en estas fotos (ver abajo) |

## P6, dicho entero (es el número que importa para el campo)

En las 15 fotos, **la acción no cambia ni una vez**. F-REENCUENTRO se enciende
con magnitudes de 0,18 (un golpe de 18 sobre 100 recordado, a media escala por
distancia) y eso **no basta para mover la elección** frente a las fuerzas ya
presentes. Es exactamente lo que la casa reporta en vez de inflar: **la fila
está bien construida y hoy es casi muda**. Si el campo la quiere audible, la
palanca honesta sería el daño recordado real (aquí se usó el golpe estándar de
18) o el reparto — decisión de mesa, no del banco.

# D · LA PROPUESTA DE CAMPO (71), con su coste y R12 delante

- **Tanda**: 40 episodios, **roster explícito del 66** (sin nuestra campeona),
  dos v37. **Coste estimado: 20 créditos** (como las tres anteriores).
- **Vara**: hp perdido en los reencuentros del caso exacto, v36 vs v37,
  pareado por estado (el instrumento del 67 ya existe).
- **La advertencia, por delante**: el 69 midió **~15 casos exactos por 80
  episodios** — es decir, **~7 por tanda de 40**. Con esa n **solo un efecto
  enorme sería visible** (R12: a n=40 hay que ganar el 72 % de los pares; aquí
  ni siquiera hay 40 pares). **Un campo así no puede sellar dirección**, y
  conviene decirlo antes de gastar: valdría para ver el mecanismo (¿se
  enciende en el campo? ¿cuántas veces?), no para demostrar que protege.

# INCÓGNITAS CON MÉTODO

1. **La magnitud es pequeña por construcción**: un golpe recordado de 18 sobre
   100 da u=0,18 → M=0,18, y a media escala 0,09. Para que el miedo pese como
   pesa el dolor real habría que recordar **el daño acumulado** del episodio,
   no el último golpe. Está a una línea; no se hizo porque el sello dice "el
   miedo que causó su último daño conocido".
2. **El daño por la hermana** se conoce solo si llegan dos partes seguidos
   (para la caída de hp). Si el primero se pierde, la memoria guarda 0 y la
   fila queda muda aunque el asiento sea cierto. Medible en campo.
3. **Los dos casos fríos** (distancia > 5): correcto por diseño, pero son
   justo los reencuentros de largo alcance (arco). Si la mesa quiere cubrirlos,
   es subir `REENCUENTRO_CERCA` — con el precio de asustarse de lejos.

# QUÉ QUEDA EN EL REPO

- `alma/appraisal_zs.py` (`f21f5568…`) — memoria del episodio
  (`mem_agresores`, `dist_agresor`), la fila F-REENCUENTRO y sus constantes.
- `alma/verifica_70.py` **nuevo** (`cffa60e8…`) — P1-P6 sobre las 15 fotos
  reales del 69.
- `reencuentros.py` + `runs/reencuentros.json` (del 69) — la materia prima.
- Alma efectiva de taller: **v37**. Liga: v19. **Sin campo lanzado.**

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

El sofá tenía delante un dato incómodo: los que vuelven armados y se acercan
atacan menos de la mitad de las veces. Con eso, adelantarse a golpear habría
significado pegar primero a cuatro de cada diez que no iban a pegar, y la
regla de la casa lleva setenta encargos diciendo que eso no se hace. La
decisión fue la correcta y la más difícil de implementar sin trampa: **no
enseñarle a golpear antes, sino a tener miedo antes**.

Y el miedo funciona como debe. Se enciende en trece de las quince fotos
reales, con siete tics de adelanto mediano sobre el golpe que en el campo
llegó de verdad; se apaga solo cuando el otro deja de acercarse; calla si el
que vuelve está a más de cinco casillas; calla del todo si ya te está
pegando, porque entonces manda el dolor y no el recuerdo. No golpea a nadie
por memoria: cero de seis en las fotos donde nadie pegó. Y hay un detalle que
sólo el parte v2 hace posible: **se asusta de quien nunca la tocó a ella,
porque su hermana le dijo el nombre**.

Lo que hay que decir sin adornos es lo que el banco encontró al final: **la
acción no cambia ni una vez**. La fila entra en la mesa, pesa lo que un golpe
de dieciocho sobre cien puede pesar, y eso no mueve una decisión que ya
sopesa la cuesta, el muro y el anillo. La casa no infla constantes para
fabricar un gesto; lo dice y lo deja medido. El miedo está bien construido y
hoy es casi mudo, y si la mesa lo quiere audible sabe exactamente qué palanca
tocar y qué costaría.

---

## Reproducción

```bash
cd gemv-coworld
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_70   # P1-P6
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7 53 54 56 59 61 62 63 65 68; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done  # 31/31
```
