# Acta — LA PROTECCIÓN EMPAREJADA (forense) · **el precio no era de defender**

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_67_la_proteccion_emparejada.md` · **Solo lectura, coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**. **v35 sin tocar** (ninguna línea de alma).
- Todo sale de los diarios ya pagados de las tandas **64 y 66** (80
  episodios, 160 diarios). Instrumento nuevo: `proteccion_pareada.py`.

---

# LOS DOS HALLAZGOS

1. **El precio de −20 hp NO era de defender: era de estar al lado de una
   cazada.** Emparejando por estado, la hermana que **defiende** pierde
   mediana **−14 hp** y la que **acompaña sin defender**, **−17**. Pareado:
   defensora mejor en 15, peor en 12, empate 5 (**p = 0,70**). No hay
   diferencia: **defender no cuesta más que mirar**.
2. **Ninguna de las 6 "ocasiones sin defensa" del 66 fue una decisión**: en
   las seis, el candidato de atacar **no existía en ningún tic**. La vara
   sobreestimaba las ocasiones (abajo), así que **la tasa real de defensa es
   mayor que el 50 % publicado**.

Y la protección, por primera vez medida de forma comparable, **apunta a
favor sin alcanzar significación**: el daño mediano de la cazada es **0 con
defensa y −14 sin ella**; en el test de signos, 15-8 y 13-7 (p = 0,21 y
0,26). **No se sella dirección** (el encargo no lo pedía y los números no lo
sostienen), pero por fin la vara mide lo que quería medir.

---

# A · EL EMPAREJADO POR ESTADO

**Universo**: 253 ventanas de caza certificada con la hermana a ≤2 (64+66) —
**32 defendidas**, 221 no.

**Criterio, declarado**: distancia normalizada en cuatro ejes —hp de la
cazada (/100), hp de la otra (/100), distancia del cazador (/5), tic de
partida (/2000)— con **veto duro** si el arma del cazador cambia de familia
(melee ↔ a distancia). Emparejado **sin reemplazo**, el par más cercano
primero. **Pares limpios: 32** (≥6, se puede concluir con cautela).

| resultado (120 tics tras la ventana) | defensa | sin defensa | pareado | p |
|---|---|---|---|---|
| **golpes recibidos por la cazada** | — | — | gana **13** · pierde 7 · empata 12 | 0,26 |
| **Δ hp de la cazada** (mediana) | **+0** | **−14** | gana **15** · pierde 8 · empata 9 | 0,21 |

**La frase honesta**: con el estado igualado, la ventana defendida es la que
**no pierde vida** (mediana 0) frente a **−14** de su par sin defender, y la
dirección es la misma en las dos varas. Pero con 20-23 pares no empatados,
p ≈ 0,2: **es una señal débil, no una prueba**. Lo que sí queda demostrado es
que **la comparación ya no está confundida**: el estado de partida está
igualado por construcción (hp de la cazada 43/40, 55/52, 80/86, 94/94… par a
par), que era exactamente lo que impedía leer el 64 y el 66.

# B · LAS SEIS OCASIONES SIN DEFENSA (66) — ninguna fue una decisión

| episodio | tics | qué ganó | mi hp | daño propio | **por qué no defendió** |
|---|---|---|---|---|---|
| `a62f7c2d` g11 | 605-615 | noop ×10 | 100 | 0 | **no veía al cazador** (arco; parte de 28-38 tics de edad) → sin certificación |
| `4b24cc53` g11 | 867-868 | noop, ir_objeto | 88 | 0 | candidato ausente pese a verlo a 1 |
| `60454bec` g11 | 4953-4963 | noop ×10 | 84 | 0 | ídem |
| `60454bec` g11 | 4975-4985 | noop ×10 | 84 | 0 | ídem |
| `62651a32` g11 | 2931-2932 | move_E ×2 | 88 | 0 | **el cazador estaba a 2 de verdad** (el parte decía 1) — espada no llega |
| `62651a32` g11 | 2966-2968 | noop ×3 | 76 | 0 | ídem (real 1-2, oscilando) |

**Ninguna es "prefirió no defender"**: en las seis, **el candidato de atacar
no existió en ningún tic** (0 de 39). Y ninguna fue miedo: hp 76-100 y **cero
tics con daño propio** en todas.

**Corrección de vara declarada** (la lección de método): la ocasión P2' se
mide con la **posición del parte**, que puede tener hasta 96 tics; el animal
exige ver al cazador **ahí, ahora**. Dos de las seis tenían al cazador **a 2
casillas de verdad** aunque el parte dijera 1. **La vara sobreestima las
ocasiones y por tanto infravalora la tasa de defensa**: el 50 % del 66 y el
62 % del 64 son **cotas inferiores**. Para el próximo campo, la ocasión debe
medirse con la posición **real y visible** del cazador, no con la del parte.

# C · EL PRECIO, EMPAREJADO

| Δ hp de la hermana que acompaña (misma ventana, estado igualado) | mediana |
|---|---|
| la que **DEFIENDE** | **−14** (n=32) |
| la que **NO defiende** | **−17** (n=32) |
| pareado | defensora mejor 15 · peor 12 · empate 5 · **p = 0,70** |

**El −20 hp que el 64 y el 66 apuntaban como "precio de defender" era el
precio de estar al lado de una hermana cazada.** Quien acompaña pierde vida
igual, defienda o no. Defender, medido así, **es gratis** — y el 66 ya había
enseñado que tampoco cuesta caídas (0 defensoras muertas, 0 "ambas caen" en
80 episodios).

# INCÓGNITAS CON MÉTODO

1. **La protección necesita más n**: 32 pares dan p≈0,2. Con dos tandas más
   (o midiendo la ocasión bien, que suma ventanas) el signo podría cerrarse.
   No es un sello: es aritmética de muestra.
2. **La vara de ocasión, corregida** (arriba): reescribirla con la posición
   visible antes del próximo campo. Cambia P2/P2' de todas las actas
   anteriores como **cotas inferiores**, no los invalida.
3. **El candidato ausente viéndolo a 1** (casos 2-4): la certificación exige
   un cuerpo a ≤1 de (ax,ay) que **no sea la hermana**; si el único cuerpo
   cercano era ella, no certifica. Es correcto por diseño (C1), pero conviene
   medir cuántas veces pasa: se hace con los mismos diarios.

# QUÉ QUEDA EN EL REPO

- `proteccion_pareada.py` **nuevo** — el emparejado por estado, la autopsia
  de B y el precio de C. Reejecutable sin coste.
- **v35 intacta**; liga v19; ninguna imagen, ningún submit.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

Dos tandas seguidas dijeron que defender costaba veinte puntos de vida, y
sonaba a lo que tenía que sonar: el precio del coraje. Emparejando las
ventanas por estado —misma vida de la cazada, mismo cazador, misma
distancia, mismo momento— resulta que la hermana que se queda mirando pierde
diecisiete y la que responde pierde catorce. El precio no era de defender:
era de estar al lado de alguien a quien están cazando. Defender, en este
mundo y con estos números, **sale gratis**.

Y las seis ocasiones que el 66 apuntó como "pudo defender y no lo hizo" no
existieron: en las seis, el gesto no estaba disponible ni un solo tic. Una
porque no veía al cazador —su parte tenía treinta y ocho tics y el mundo se
había movido—, dos porque el cazador estaba de verdad a dos casillas aunque
el parte dijera una, y el resto porque la certificación, que se niega a
apuntar a la hermana, no encontró a nadie más a quien apuntar. Ninguna fue
cobardía: todas eran hp de ochenta o cien y cero golpes recibidos. La vara
estaba midiendo con una foto vieja, y la culpa era de la vara.

Queda la pregunta grande a medio contestar, y conviene decir exactamente
cuánto. Ahora que las ventanas son comparables, la defendida es la que no
pierde vida —cero contra menos catorce de mediana— y las dos varas apuntan al
mismo lado. Pero veinte pares no empatados dan un p de dos décimas, y esta
casa no llama prueba a eso. Lo que hoy se puede afirmar es más modesto y más
sólido: **el instrumento por fin mide lo que quería medir, la dirección
favorece a la manada, y el coste que le achacábamos no era suyo.**

---

## Reproducción

```bash
cd gemv-coworld
python3 paintball/proteccion_pareada.py   # A (emparejado + signos), B, C
```
