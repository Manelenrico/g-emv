# Acta — EL PARTE DE ESTADO (temporada dos, primera piedra) · **PARAR EN P5**

Fecha: 2026-09-04 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_53_el_parte_de_estado.md` · Banco, **coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19** (no se tocó). Todo en `paintball/`.
- Alma efectiva del repo tras el encargo: **v27 en decisiones, bit a bit**
  (el oyente del parte queda en CANDADO, abajo); el emisor nuevo está vivo.

---

# EL VEREDICTO, PRIMERO

**El sello P5 falló y se ejecutó el PARAR** (precedente del 46): el parte del
hermano **SÍ acerca** el candidato de atacar al hermano en un rincón medible.
**El oyente queda APAGADO por defecto** (`A.PARTE_ON=False`, motivo grabado
en la tabla); **el emisor queda certificado y vivo** (P1 verde: hablar no es
el problema; escuchar espera a la mesa). Y la pregunta del encargo (P4) tiene
respuesta limpia: **saber exacto no cambia NI UNA decisión** en las escenas de
gemelos — la esperanza de la mesa (el don activándose antes) **no se cumple**.
El examen de campo (54) **no se escribe**: este acta no está en verde.

---

# A · EL FORMATO, TAL COMO QUEDÓ (`alma/parte.py`)

```
E1 P<slot> t<tick> <x>,<y> h<hp> v<0|1> b<n> a<0|1>[ <ax>,<ay>]
```

| campo | qué lleva | fuente (todo CIERTO, R1) |
|---|---|---|
| `E1` | marca de formato; el parser SOLO acepta ésta | — |
| `P<slot>` | quién habla; el oyente lo coteja con `from` del chat | mundo.slot |
| `t<tick>` | tic de EMISIÓN (mismo reloj del mundo; la latencia +2 del 52 queda dentro) | obs.tick |
| `<x>,<y>` | posición propia | obs.you.pos |
| `h<hp>` | **hp propio EXACTO** (formato `%g`, ≤6 cifras significativas — [impl] declarado) | obs.you.hp |
| `v<0|1>` | veneno (mismo test que F-DANO usa para uno mismo: effect id `poison*`) | obs.you.effects |
| `b<n>` | botiquines a bordo (unidades con id del botiquín) | obs.you.pack |
| `a<0|1>` | agresor activo (ventana S-7, la misma vara de las filas); si a1 **y está a la vista**, su posición; si no se le ve, a1 sin posición (dirección no certificable: **no se emite**) | mem.agresores + obs.visible |

Sustituye al latido del 32 en **las dos policies** (`policy.py`,
`policy_repetidor_forense.py`), misma cadencia `VOZ_CADA=48` (≥24 ⇒ jamás
`rate_limited`), determinista dado el estado. Máx. visto en banco: 45 chars.

# B · EL OYENTE (construido, medido — y en candado)

- Parser **estricto** en `Memoria.observa`: solo marca `E1` con formato exacto
  Y slot que casa con `from`; el latido viejo, el texto ajeno del relleno y
  los `E1` truncados se ignoran sin tocar nada. El más reciente por tic manda.
- **Un único punto de lectura** del modelo del hermano:
  `Memoria.pareja_hp_est(tick, hp_max)` — parte fresco → hp EXACTO; sin él
  (solo, mudo, ajeno, caducado >96 tics, hermano muerto) → la banda de
  siempre, **v27 bit a bit**. Por él enrutan las CUATRO lecturas del hp del
  hermano: (1) est de S-DANO/S-MUERTE-PAREJA, (2) la base del golpe previsto
  del decisor (la foto honesta del 23, misma base ⇒ los márgenes solo
  dependen del daño), (3) el f_hp de S-7 cuando el agresor ES la pareja,
  (4) los gates "herida"/"curada del todo" de medicina y cesión.
- Veneno/botiquín/agresor del hermano quedan en `mem.parte` con su tic y
  salen en la radiografía (`parte`, solo con parte fresco — P2 byte-límpio).

# C · LAS SEIS PRUEBAS CONTRA SUS SELLOS (`alma/verifica_53.py`, VERDE)

| prueba | sello | resultado |
|---|---|---|
| **P1 FORMATO** | sellado | **VERDE** — 26/26 estados: 0 filtrados por ASCII/longitud, eco parseado 100 % con campos exactos, cadencia gaps={48} (jamás rate_limited), mensaje determinista 3/3 |
| **P2 EL SOLO INTACTO** | sellado | **VERDE** — 5 escenas sin gemelo / con TEXTO AJENO ×4 (latido viejo, basura, E1 truncado, slot que no casa): v28 **byte-idéntica** a v27; y con el candado echado, un parte VÁLIDO ni se guarda ni cambia nada |
| **P3 LA FOTO HONESTA SABE** | sellado | **VERDE** (taller encendido) — error **0** exacto desde el parte hasta la caducidad (96 tics), banda después; el más reciente manda; muerto el hermano, el parte calla (los fuegos mandan) |
| **P4 ¿CAMBIA LA CONDUCTA SABER?** | sin gate | **0 de 8 decisiones cambian** (tabla abajo) |
| **P5 HONOR** | sellado | **ROJO → PARAR.** Sin parte: byte-idéntico (5/5). Con parte: el candidato NI nace del testimonio NI es elegido, 0 iniciaciones (53 decisiones del banco) — pero **el margen SE ACERCA**: peor delta **−0,358** (abajo). Candado echado |
| **P6 REGRESIÓN** | — | **VERDE** — bancos 13–52: 21/21 en verde, 0 fallos; humo determinista 3/3 (único volátil: ms de pared, declarado desde el 41) |

## P4 — la lista de decisiones que cambian al saber: **VACÍA**

8 escenas de gemelos (lealtad 25 ×4, tentación 39 ×3, escudo 40/42 ×1 —
**25 y 40/42 reconstruidas de sus actas: esos bancos no existen como
ficheros, declarado**), v27 contra v28+parte:

| escena | v27 | v28 | fila que se mueve |
|---|---|---|---|
| lealtad, banda hurt, parte h35 | move_SE | move_SE | S-DANO-PAREJA 0,051→0,066 |
| lealtad, banda hurt, parte h60 | move_SE | move_SE | S-DANO-PAREJA 0,051→0,041 |
| lealtad, banda healthy, parte h70 | move_SE | move_SE | S-DANO-PAREJA 0,017→0,030 |
| lealtad, banda critical, parte h8 | move_SE | move_SE | S-DANO-PAREJA 0,085→0,093 |
| tentación g1 hp0=100, h100 | move_SE | move_SE | S-DANO-PAREJA 0,017→0 |
| tentación g3 hp0=100, h80 | move_SE | move_SE | S-DANO-PAREJA 0,018→0,021 |
| tentación g4 hp0=28, h80 | usar_botiquin | usar_botiquin | S-DANO-PAREJA ídem |
| escudo, hermano hurt h20+agresor | move_SW | move_SW | S-DANO-PAREJA 0,051→0,081 |

**Solo S-DANO-PAREJA se mueve, y nunca lo bastante para girar una elección.**
La esperanza de la mesa (don/cesión antes) no se cumple: con B≈0,1 (roce
recién nacido), toda la certeza del mundo mueve la fila ±0,03 — el don sigue
casi mudo, como en el 27.

## P5 — la medida del candado

En la tentación del 39 (el hermano ME pega armado) con su parte confesando
hp bajo:

| escena | margen v27 | margen v28 | delta |
|---|---|---|---|
| g1 hp0=100, parte h100 | +0,405 | +0,404 | −0,001 |
| g1 hp0=100, parte h25 | +0,405 | **+0,133** | **−0,272** |
| g1 hp0=100, parte h10 | +0,405 | **+0,047** | **−0,358** |
| g4 hp0=100, parte h25 | +0,435 | +0,177 | −0,258 |
| g4 hp0=28, parte h25 | +0,542 | +0,428 | −0,114 |

**La causa es física de sellos, no bug** (comprobado número a número): S-7
sellada (PROMPT_09) tasa la presión del agresor **× su hp** — "cada golpe de
respuesta tiene valor predicho". La foto de huir sale del radio (S-7=0); la
de responder se queda. Con parte h25, el f_hp de la foto de atacar cae de
0,72 (banda, capado a 0,5) a 0,14 (25−10,8 de golpe previsto) → **responder
se abarata** → el margen se acerca. Y no hay enrutado honesto que lo evite:
sacar el parte del golpe previsto invierte S-DANO-PAREJA (la foto de pegarle
saldría MÁS sana que la de no pegarle — peor). **Certeza + fórmulas selladas
que pisan el hp del hermano ⇒ el margen depende de lo sabido.** El sello
exigía "ni crear ni acercar": crear jamás (el candidato nace de
agresión+arma; el testimonio no toca `mem.agresores` — verificado con a1 y
posición: 0 candidatos, agresores vacío); **acercar sí** → PARAR.

Para la mesa, si quiere resellar P5 en vez de descartar: en TODOS los
rincones medidos el atacar **sigue perdiendo** (margen mínimo +0,047 > 0),
jamás es elegido, y 0 iniciaciones en 53 decisiones — el acercamiento es del
precio, no de la conducta. Pero el sello es el sello: eso lo decide la mesa,
no el banco.

---

# INCÓGNITAS CON MÉTODO

1. **hp con `%g`**: exacto hasta 6 cifras significativas; un hp con ruido
   flotante (83,3600000001) viajaría como 83,36. Método: si molesta, formato
   de 4 decimales fijos — no se tocó porque el sello pedía formato mínimo.
2. **S-7 con agresor EXTRAÑO** sigue por banda (el parte solo habla del
   hermano) — sin cambio, declarado por simetría.
3. **B bajo en las escenas de banco** (roce ≈0,1 recién nacido): con B alto
   (partida larga), S-DANO-PAREJA escala ×10 — ¿giraría alguna decisión de
   P4? Método: re-correr las 8 escenas con `mem.roce_B=1.0` — no estaba en
   el encargo, queda a la reserva.

# QUÉ QUEDA EN EL REPO

- `alma/parte.py` **nuevo** (`3330781…`): formato + emisor + parser.
- `alma/appraisal_zs.py` (`f1134c9…`): oyente + `pareja_hp_est` + candado
  `PARTE_ON=False` con el motivo grabado.
- `alma/decisor_zs.py` (`63a4ef2…`): base del golpe previsto a la pareja
  por la misma estimación (inerte con el candado).
- `alma/policy.py` (`221242d…`) y `policy_repetidor_forense.py`
  (`121f7a1…`): el parte sustituye al latido del 32 (emisor VIVO).
- `alma/verifica_53.py` **nuevo** (`610db7c…`): las seis pruebas; verifica
  el estado aparcado y reproduce la brecha (patrón del 46).
- **Efectivo en decisiones: v27 bit a bit** (P2 + regresión 21/21).
  El 54 no se escribe.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

El encargo preguntaba si saber cambia la conducta, y la respuesta es un no
doble, más interesante que un sí.

No cambia hacia el bien: en ocho escenas de gemelos, la certeza absoluta
sobre el hp del hermano mueve una sola fila unos centesimales y no gira ni
una decisión. El don sigue mudo — no porque el animal no sepa, sino porque
la fila que empuja el don pesa por el roce B, y el roce en frío vale 0,1.
La palanca de la temporada dos no es la información: es lo que la
información multiplica.

Y sí cambia hacia donde no debía: la única conducta que el parte consigue
mover — en el precio, nunca en la elección — es abaratar la respuesta al
hermano que confiesa estar muriéndose mientras te pega. No es un bug: es la
S-7 sellada haciendo exactamente lo que la mesa firmó en el 09, alimentada
con un número más verdadero. La honestidad de las fotos tiene esta esquina:
quien sabe cuánta vida le queda al que le hiere, sabe también cuánto vale
devolverle el golpe. El sello del 53 decía "ni crear ni acercar", el banco
midió acercar, y la casa hace lo que hace con los sellos rotos: PARAR, el
oyente al candado con el motivo grabado, y la mesa decide.

Queda en pie lo que sí está certificado: un formato de parte limpio que
habla cada dos segundos sin costar nada, un parser que no se deja engañar
por el relleno, y una foto honesta que durante noventa y seis tics sabe en
vez de adivinar. El hablar está listo. El escuchar espera.

---

## Reproducción

```bash
cd gemv-coworld
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_53   # las seis pruebas + candado
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done   # P6: 21/21
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.smoke_alma    # x3 | grep -v ms | md5: identicos
```
