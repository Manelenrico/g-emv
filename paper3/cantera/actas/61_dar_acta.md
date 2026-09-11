# Acta — DAR DE LO QUE TE FALTA (v32) · BANCO VERDE

Fecha: 2026-09-04 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_61_dar_de_lo_que_falta.md` · Banco, **coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **v32 = v31 con la provisión a b≥1** (`appraisal_zs.py 03c35cbe…`,
  `decisor_zs.py ef88de1b…`). Interruptor `PROVISION_B_MIN` (2 = v31 bit a
  bit; 1 = v32).

---

# EL CAMBIO (uno, con su prudencia)

La generosidad no espera excedente: **S-PROVISION deja de exigir b≥2 y nace
con b≥1** propio y b=0 de la hermana (parte), en calma. Sin umbral escrito de
"dar si ella está X peor" (R2). Lo decide **el equilibrio de fuerzas**:

- **Su peso** (por qué dar): S-HERIDO (su déficit, cuando está herida) +
  S-PROVISION (su falta de venda, de fondo).
- **Mi cuesta** (por qué quedármela): cuando estoy herido, `usar_botiquin` me
  sana y su alivio de F-DANO (la cuesta convexa del 43) es grande.

**La foto del soltar con b=1, honesta** — la fuente única de la prudencia:
tras soltar, mi venda a bordo = 0, y **R-ACOPIO escala con MI cuesta**
(`PROVISION_SELF × F-DANO`) **solo en la foto que REGALA**. La distinción es
limpia y se estampa `_hp_real` para hacerla: la foto de `usar` sube mi hp
(cuesta baja → casi no paga), la de `soltar` me deja herido (cuesta alta →
paga y pierde). Así **"mi cuesta manda" emerge del descenso, sin umbral**.
Constante nueva declarada: `PROVISION_SELF = 1.0` (calibrada en banco).

# LA FRONTERA (P3, radiografía — la mesa NO sella el cruce)

`soltar` (DAR) vs `usar_botiquin` (USA) vs mover, barrido (mi hp × su hp),
b=1 yo / b=0 ella, calma:

| mi_hp \ su_hp | 8 | 20 | 40 | 70 | 95 |
|---|---|---|---|---|---|
| **95** | DAR | DAR | DAR | move | move |
| **80** | DAR | DAR | move | move | move |
| **60** | DAR | DAR | USA | USA | USA |
| **40** | DAR | USA | USA | USA | USA |
| **25** | USA | USA | USA | USA | USA |
| **10** | USA | USA | USA | USA | USA |

**La diagonal es el equilibrio, dibujado**: sano y ella peor → **doy**;
herido → **me curo**; ella sana (aunque sin venda) → no malgasto mi única
venda. Nadie escribió ese cruce: sale de la cuesta contra el peso. La mesa
lo mira, no lo sella.

# LAS SIETE PRUEBAS CONTRA SUS SELLOS (`alma/verifica_61.py`, VERDE)

| prueba | sello | resultado |
|---|---|---|
| **P1 DA CUANDO PUEDE** | sellado | **VERDE** — yo 95/80, ella 10/25, ≤2 → **soltar GANA**; a >2 → se acerca (acaba a 0,0 de 6,0) |
| **P2 SE LA QUEDA** | sellado | **VERDE** — yo 25/10, ella ≤30 → **soltar PIERDE** (`usar`, mi cuesta manda); yo 25, ella 95 → no da (S-HERIDO calla) |
| **P3 LA FRONTERA** | sin gate | radiografía arriba — la diagonal cuesta-vs-peso |
| **P4 JERARQUÍA DEL MIEDO** | sellado (PARAR) | **VERDE** — perseguida: v32 `move_NW` == v27; S-PROVISION apagada bajo caza |
| **P5 SILENCIOS** | sellados | **VERDE** — ella b=1: v32 **byte-idéntica** a v31; sin hermana: **byte-idéntica a v27** |
| **P6 HONOR** | sellado | **VERDE** — escenas del 39/53: v32 **byte-idéntica** a v31 — márgenes y tabú intactos |
| **P7 REGRESIÓN** | — | **VERDE** — bancos 13-60 (con guard de pila): **26/26**, 0 fallos; humo 3/3 (hash idéntico); determinismo del banco 3/3; **0 iniciaciones** (61 decisiones) |

# LA OCASIÓN NUEVA, CONTADA EN EL 60 (parte C — "antes de gastar")

Recontada de los 80 diarios del 60 con conteo por unidades:

| | b≥2 (v31) | **b≥1 (v32)** |
|---|---|---|
| ocasión (yo lleva, ella b=0, calma) | 0,6 % · 1/40 eps | **5,6 % · 15/40 eps** |
| de esa, DAR-worthy (yo sano ∧ ella herida) | — | **40 tics · 0,7 % de la ocasión** |

**El cambio abre la puerta**: la fila ahora tiene dónde encender —15 de 40
episodios contra 1— porque llevar UNA venda es lo normal (16,8 %), no un lujo
(0,6 %). Pero **el DAR de verdad sigue siendo una ventana estrecha**: exige
que yo esté sano Y ella herida Y en calma a la vez (40 tics). La frontera
calla bien en el resto: cuando ella está sana no malgasto, cuando yo estoy
herido me curo. **Para la mesa, antes del 62**: la provisión llegará al campo
(la ocasión existe), pero las entregas en calma serán pocas y honestas —
justo las que el equilibrio aprueba. No es el 0 del 57; tampoco será un
diluvio.

# INCÓGNITAS CON MÉTODO

1. **`PROVISION_SELF = 1.0`**: calibrada para que la frontera cruce donde el
   sofá quería (sano da, herido guarda). El campo dirá si la diagonal es la
   correcta o si la mesa quiere moverla (subir SELF = más egoísta; bajar =
   más heroico). Es un dial, no un umbral.
2. **La ventana estrecha (40 tics)**: el DAR real depende de coincidir sano +
   ella herida + calma. Si el 62 muestra pocas entregas, no es fallo de la
   fila: es que el mundo raramente pone esa terna. Declararlo antes evita leer
   "poco" como "roto".
3. **El `move` en el borde** (yo 80-95, ella 70): mantengo la venda ante una
   hermana casi sana. Correcto (no urge), pero es la celda donde un peso
   social mayor la volvería DAR. Material de sofá si se quiere una pareja más
   dadivosa de fondo.

# QUÉ QUEDA EN EL REPO

- `alma/appraisal_zs.py` (`03c35cbe…`) — S-PROVISION a b≥1 + el coste-por-
  cuesta de la foto que regala (`PROVISION_SELF`, `PROVISION_B_MIN`).
- `alma/decisor_zs.py` (`ef88de1b…`) — sello `_hp_real` a las fotos +
  candidato soltar a b≥1.
- `alma/verifica_61.py` **nuevo** (`72069ba8…`) — las siete pruebas + la
  radiografía de la frontera.
- Alma efectiva de taller: **v32**. Liga: v19. El campo (62) puede
  escribirse; la ocasión está contada.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

El 60 dejó una frase sellada —dar de más exige tener de más, y el animal no
lleva de más— y este encargo la respondió por el otro lado: que dé de lo que
le falta. Y funcionó, pero lo bonito es cómo funcionó, porque no hizo falta
escribir ni un umbral.

La generosidad sin excedente es peligrosa: regalar tu única venda puede ser
un suicidio educado. La red que lo impide no es una regla ("no des si estás
por debajo de X") sino una foto honesta: cuando el animal imagina soltar su
última venda, imagina también quedarse sin ella, y esa imagen le cuesta
exactamente lo que vale su vida en ese momento —su cuesta—. Si está sano, la
cuesta es casi nada y da sin pensarlo; si está muriéndose, la cuesta es un
muro y se cura primero. Entre esos dos extremos hay una diagonal que nadie
dibujó a mano: emerge de pesar su vida contra la de su hermana, casilla por
casilla. La mesa la mira como se mira un mapa que salió del terreno, no del
lápiz.

Y hay una honestidad extra que el banco exigió: distinguir al que regala del
que se cura. Los dos acaban sin venda, pero solo el que regala sigue herido;
el que se cura ya no. Bastó estampar el hp verdadero en cada foto para que la
prudencia no castigara al que hace lo correcto consigo mismo. Sin ese detalle,
el animal habría preferido moverse antes que curarse, por miedo a quedarse sin
venda —una prudencia mal entendida—. Con él, se cura cuando debe y da cuando
puede.

La ocasión, contada antes de gastar, dice lo justo: la puerta está abierta
—quince partidas de cada cuarenta, no una— pero el umbral que la cruza es
estrecho, porque para dar hay que estar bien mientras ella está mal, y eso el
mundo lo reparte con cuentagotas. El 62 verá pocas entregas y serán las
buenas. Que sean pocas no será un fallo: será el equilibrio haciendo su
trabajo.

---

## Reproducción

```bash
cd gemv-coworld
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_61   # las siete pruebas + frontera
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7 53 54 56 59; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done  # P7: 26/26
# la ocasion nueva: conteo por unidades sobre runs/pareja3 (inline en el acta)
```
