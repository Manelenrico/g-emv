# P5-AP1 — cotejo del apéndice del paper cinco

**Solo lectura, coste cero.** Nada lanzado, nada enviado. Motor, decisor y tabla
intocados (`1e511978c251130e95169ebf8443efa1` · `8fa03547e3228ef9df4aa94c444f9252`
· `98c13d60167c80cc8334c965be75c640`). **No aparece ninguna clave ni el contenido
de `.env`.**

Cotejado `cantera/paper5/apendice_paper5_v1.md` (79 líneas): **7 filas en A.1,
49 en A.2 y el párrafo de A.3.**

---

## El titular

**De las 56 filas, 47 coinciden sin reserva. Nueve tienen algo que arreglar, y
dos de ellas importan de verdad.**

| | |
|---|---|
| filas que **coinciden** | **47** |
| **informe citado equivocado** | **3** |
| **valor equivocado** | **1** |
| **valor redondeado donde el apéndice promete exacto** | **2** |
| **matiz perdido que cambia lo que dice la cifra** | **2** |
| **sigue sin localizar** | **1** |

**Las dos que importan:** la fila de las «dieciocho opciones» **dice «con las
piernas listas» y su fuente no dice eso** —el 18 es del puñado comparador, y con
las piernas listas la papeleta mide **16**—; y la fila de la meseta de calma
**da los tics equivocados** (2.300-8.200 cuando el informe dice **2.400-8.000**).

**Y una nota de intendencia para la cabecera del apéndice:** dice «aquí van
enteras», pero **tres filas llevan el número redondeado**.

---

## A.1 · El mundo lento — **las siete coinciden, una cita mal**

| fila | ¿coincide? | valor correcto si no | fuente exacta |
|---|---|---|---|
| `max_ticks` 18.240 · 12 min 40 s · el doble | **sí** | — | `informe_P5ARI3.md:100,330` |
| `freeze_ticks` 480 · 20 s · primer movimiento tic 482 | **sí** | — | `informe_P5ARI3.md:45,128` |
| `zone.schedule` tic 7.296 (40,0 %) · 1,25× más lento | **sí** | — | `informe_P5ARI3.md:139,142,333` |
| `sponsor.budget_per_team` 600 (defecto 300) · sin efecto | **sí** | — | `informe_P5ARI3.md` §1 y §2(d) |
| `sponsor.live` false · ignorado, la clave es `enabled` | **sí** | — | `informe_P5ARI3.md` §1 |
| regalos: 8 raciones 2.017-2.185, 8 botiquines 4.609-4.777 | **sí** | — | `informe_P5ARI3.md:156-159` |
| **rivales · roster_lento_v1** | **valores sí, CITA NO** | — | **`informe_P56B.md:51` y `:60`** (no `informe_P56C`) |

**La fila de los rivales.** `informe_P56C.md` **no describe el roster**: solo
guarda el md5 del fichero (`:411`). La descripción —«**Fuera las tres
cazadoras**» (`informe_P56B.md:51`) y «**Dentro, una repetición más de las tres
más pacíficas que ya estaban**» (`:60`)— está en P5-6B, y también en
`ACTA.md:1115-1119`.

*Comprobado además contra el fichero: los rivales son `zero-sum-scavenger` ×3,
`relh-zero-sum` ×3, `belobog` ×3, `sivanlevy-zs-courier` ×2, `zs-patient` ×1,
`aaron-zs-fable` ×1, `skourehjan-zero-sum-scripted-v1` ×1 = **14 puestos**, más
nuestros dos = 16.*

---

## A.2 · Por secciones — las nueve filas con algo que arreglar

### 1. «unas dieciocho opciones» — **el matiz está mal, y es el que más importa**

| | |
|---|---|
| dice el apéndice | «18 candidatos de mediana **con las piernas listas**» |
| dice la fuente | «candidatos **del puñado**, mediana \| **1** \| **18**» |
| fuente exacta | **`informe_P53D.md:21`** *(confirmado en `informe_P53E.md:180`)* |

**El 18 es del PUÑADO COMPARADOR en el tic de ventana, no de la papeleta con las
piernas listas.** En la misma fila del mismo cuadro, en el tic de la escena la
mediana es **1**.

**Y la papeleta viva no da 18.** Medido en `P58M_t0_K_20260916`, asiento 10,
7.899 tics: **mediana 1 sobre todos los tics** y **mediana 16 con las piernas
listas** (mín 14, máx 22).

**Propuesta:** o «18 opciones que el comparador sopesa» (y se quita «con las
piernas listas»), o «16 opciones con las piernas listas» citando la medida.

*(Esta fila venía marcada «por confirmar»: queda confirmada la cifra y
desmentido el matiz.)*

### 2. «seis mil instantes seguidos de calma sin mirar» — **valores mal**

| | |
|---|---|
| dice el apéndice | «tics **2.300 a 8.200**, ignorancia fija en 0,727» |
| dice la fuente | «Entre los tics **2.400 y 8.000** … se queda clavada en **0,727** durante **seis mil tics**» |
| fuente exacta | **`informe_P57A.md:326-328`** |

**El 0,727 y los «seis mil tics» son correctos; los dos extremos no.**

### 3. «manos bien servidas» — **informe citado equivocado**

| | |
|---|---|
| cita el apéndice | `informe_P51_D` |
| **es** | **`informe_P51_E.md:81`** *(y `:8`, `:10`, `:87`, `:122`)* |
| valores | **correctos**: «\| **W ≥ 3,0** \| **7.960** \| **1,243 %** \| **10** \|», sobre **260 diarios de S-2** |

`informe_P51_D.md` es «Las manos vacías» y trata de **once vidas** con W máxima
**2,25**; no contiene ninguna de las tres cifras.

### 4. «lo no visto, a seis casillas» — **localizada**

| | |
|---|---|
| estaba | «por confirmar» |
| **es** | **`informe_P58A.md:91`**: «trayecto \| **mediana 6** · Q1 4 · Q3 7 · min 2 · **max 11**» |
| valores | **coinciden exactamente** |

*(El informe lo llama **trayecto**, no «lo no visto». Son lo mismo en P5-8A
porque el destino **es** la primera casilla no vista alcanzable, pero conviene
usar la palabra del informe.)*

### 5. «el tirón gana una discusión de cada veinte» — **NO localizada**

**No hay ninguna cifra del paper cinco que valga 5,0 %.** Las cuatro candidatas:

| candidata | valor | fuente | qué mide |
|---|---|---|---|
| **el renglón decide, entorno seguro** | **5,62 %** | `informe_P57C.md:187` | **campo**, 357.982 tics — *la única de la configuración real* |
| el renglón decide, todos los entornos | 7,69 % | `informe_P57C.md:183` | campo |
| lento · frontera **sin balanza** | 5,88 % | `informe_P57A.md:243` | **contrafactual** |
| S-2 · frontera **sin balanza** | 5,39 % | `informe_P57A.md:241` | **contrafactual** |

**Las dos del 5,x % de P5-7A son la columna «sin balanza»: describen lo que
pasaría si quitáramos el veto, no lo que pasó.** Si la frase del texto se
refiere al campo, el número es **5,62 %** y la fila debería decir «una de cada
dieciocho». **No la doy por buena sin que me digas a qué tirón te refieres.**

### 6. «sin el alivio, tres de cada cien viajes; con él, uno de cada tres» — **redondeado**

| | |
|---|---|
| dice el apéndice | «**2,7 %** y **37 %**» |
| dice la fuente | «sin el renglón pasa el **2,68 %**. Con la curiosidad en la proyección pasa el **37,25 %**» |
| fuente exacta | **`informe_P58A.md:147`** *(y el cuadro en `:90`: «pasan SIN el renglón \| **86 = 2,68 %**»)* |

**La cabecera del apéndice promete valores enteros; éstos van redondeados.**

### 7. «la exposición firma cuatro de cada diez rechazos» — **falta el número**

| | |
|---|---|
| dice el apéndice | «S-8-EXPOSICION, **4 de cada 10**» |
| dice la fuente | «ventana \| O-después \| 743 \| **exposición 40,51 %**» |
| fuente exacta | **`informe_P52c.md:115`** |

**El valor medido es 40,51 %**, y la columna «Valor medido» debería llevarlo.

### 8. «tres de catorce tipos de rival, nueve de cada diez golpes y muertes» — **matiz perdido**

| | |
|---|---|
| dice el apéndice | «92 % de los golpes y **92 % de las muertes**» |
| dice la fuente | «Tres políticas de catorce hacen el 92 % de las **muertes tempranas** y el 92 % de los golpes» |
| fuente exacta | **`informe_P51_E.md:188`** *(los 434 diarios, en `:151`)* |

**Es el 92 % de las muertes TEMPRANAS, no de todas.** El apéndice pierde el
adjetivo, y con él la cifra cambia de significado.

### 9. «seis de doscientos episodios sin coste informado» — **el informe citado no existe**

| | |
|---|---|
| cita el apéndice | `informe_P5ARI` |
| **no existe ningún fichero con ese nombre** | los que hay son `informe_P5ARI_p7.md`, `informe_P5ARI_p1a6.md` y `informe_P5ARI_cierre.md` |
| **es** | **`informe_P5ARI_cierre.md`**, que trae los seis con su `xreq` y su `ereq` |
| valores | **correctos**: seis episodios, contados a cero |

---

## A.2 · Las 40 filas restantes: **coinciden**

Comprobadas una a una contra el informe citado. Las que llevan algún matiz
menor van con nota.

| fila | fuente exacta | nota |
|---|---|---|
| once tics por casilla (16 − velocidad) | `informe_P52b.md:19,283` | **el `sim.nim:144` que cita NO lo puedo comprobar**: no tenemos el código del juego |
| 75,69 % de los tics con piernas en pausa | `informe_P52b.md:46` | |
| 90,38 % de los `noop` | `informe_P52b.md:48` | |
| quieta de verdad 7,96 % | `informe_P52b.md:54` | |
| 4 de 1.908 victorias por empate | `informe_P56A.md:60` | «cuatro tics de 1.908 victorias, el 0,21 %» |
| calma 3-7 % y 18,17 % | `informe_P51_C.md:76` | |
| 0 de 37.750 tics vivos | `informe_P51_C.md:8` | |
| 4,13 y 14,10 casillas por cien tics | `informe_P51_C.md:126` | |
| 434 diarios | `informe_P51_E.md:151` | |
| 2.230 escenas de 40 diarios | `informe_P52c.md:3,4` | |
| 8,52 % y 7,22 % (n = 845) | `informe_P52c.md:39,40` | |
| 2,35 % y 22,96 % | `informe_P52c.md:130,132` | |
| 125 de 908 (13,77 %) | `informe_P52c.md:23,160` | |
| 70,88 % y 46,79 % | `informe_P53B.md:10` | |
| 4,52 % | `informe_P53H.md:47` | |
| 87,4 % y 90,1 % | `informe_P53F.md:5,8` | |
| 51,2 % de su aporte | `informe_P53H.md:12` | |
| 34 de 40 (P5-4A) | `informe_P54A.md:8` | |
| **39 de 40** (P5-4B) | `informe_P54B.md:10,89,209` | |
| C = 0,5 → +0,02 | `informe_P54A.md:5,31` | |
| 3.284 respuestas; 80,9 % | `informe_P55A.md:6,34` | |
| 49,0 % contra 87,5 % | `informe_P55A.md:10,11` | |
| 0 de 367; 10,48 %; 18,13 % | `informe_P55B.md:9,10,11` | |
| 20,08 %; 60,23 % | `informe_P55B.md:16,279` | |
| 14,5 % y 69,5 % | `informe_P55B.md:230,349` | |
| calla 1-2 % | `informe_P55B.md:4,5` | |
| 200 diarios; 1.501.210 tics; 0 perdidos | `informe_P56C.md:12,13` | |
| 2.088 de 2.088 | `informe_P56C.md:14` | |
| 2,4 % en F; 1,7 % en T | `informe_P56C.md:147,190` | |
| 3.568 formas rechazadas por área | `informe_P56C.md:210` | |
| 76,8 % (F) con piernas listas | `informe_P58O.md:18` | |
| 42,3 % contra 61,1 % | `informe_P56C.md:17,18` · `informe_P58O.md:124,125` | **las dos citas son correctas** |
| calló 40,8 % de las citas | `informe_P56C.md:34` | «40,8 % (834/2.042)» |
| sin balanza, de 0,48 % a 5,39 % | `informe_P57A.md:21,22` | |
| 1,086 veces; 14,5 por cien tics | `informe_P57C.md:162,173` | |
| obedece 92,5 % | `informe_P58M.md:13` | |
| se completan 68,9 % | `informe_P58M.md:12` | |
| 5,81 veces, 20 semillas | `informe_P58M.md:12,15` | |
| **cinco de las siete** rupturas | `informe_P58M.md:267` | |
| 1,16 emparejado (10, 15 y 20 semillas) | `informe_P58M.md:21,22` | |
| la forma vive el 2,2 % | `informe_P58M.md:25` | |
| 0,0205 a 0,0313 · de 10 a 383 · **cada 43 tics** | `informe_P58M.md:193,200,201` | |
| vida p = 0,50; puesto p = 1,00 | `informe_P58M.md:29` | |
| 0 de 418 muertes | `informe_P57B.md:10` | **los 434 son DIARIOS, no vidas**; las muertes son 418 |
| conocimiento del matador, mediana 0,94 | `informe_P57B.md:11` | |
| el vínculo: 1 y 2 decisiones | `informe_P57B.md:137,138,143` | **son DOS configuraciones alternativas** (`vinc k=0,1` → 1 · `vinc k=0,2` → 2): nunca corrieron juntas, así que «tres decisiones» las suma |
| 0 de 27.519 | `informe_P57C.md:162` | |
| 603 llamadas, 4,44 dólares | `informe_P55B.md:3,371` | |

---

## A.3 · Lo que costó — **las cinco cifras coinciden; falta gasto y falta el total**

| cifra del apéndice | ¿coincide? | valor exacto | fuente |
|---|---|---|---|
| **4,44 $ banco** | **sí** | **4,4448 $** (603 llamadas, cero errores) | `informe_P55B.md:3`, `:371` |
| **7,87 $ P5-6C** | **sí** | **7,868069 $** | `ACTA.md:2238` · suma de los 100 registros: **7,868069** |
| **10,48 $ P5-6C (Haiku)** | **sí** | **10,477101 $** (80 asientos, `/spend` cuadró en los 80) | `ACTA.md:2239` |
| **2,67 $ P5-7C** | **sí** | **2,672766 $** | `ACTA.md:2442` · suma de los 40 registros |
| **3,44 $ P5-8M** | **sí** | **3,439826 $** | `informe_P58M.md` · suma de los 40 registros |

### Falta: **diez series y sondas, 2,431278 $**

| serie | gasto | ¿en A.3? |
|---|---|---|
| P5-6C | 7,868069 $ | **sí** |
| P5-8M | 3,439826 $ | **sí** |
| P5-7C | 2,672766 $ | **sí** |
| **P5-8I** | **0,769178 $** | no |
| **P5-8K** | **0,358956 $** | no |
| **P5-6B** | **0,346429 $** | no |
| **P5-8B** | **0,157748 $** | no |
| **P5-8E** | **0,150611 $** | no |
| **P5-8D** | **0,100443 $** | no |
| **P5-8H** | **0,087402 $** | no |
| **B1** | **0,052471 $** | no |
| **C2** | **0,041511 $** | no |
| **C3** | **0,035993 $** | no |
| **total plataforma (216 episodios)** | **16,081403 $** | |

**Y falta una partida de modelo: P5-6B gastó 0,330536 $ de Haiku** por el
sidecar (sumado del último `forma_spend` de cada asiento de sus diarios). A.3
solo nombra el de P5-6C.

### El total, que A.3 no da

| concepto | $ |
|---|---|
| plataforma (216 episodios) | **16,081403** |
| modelo por el sidecar (P5-6C 10,477101 + P5-6B 0,330536) | **10,807637** |
| modelo con clave propia (P5-5B) | **4,444800** |
| **TOTAL PAPER CINCO** | **31,333840 $** |

**P5-5A no cuenta**: fue en seco (`informe_P55A.md:3`, «En seco, coste cero.
Nada a la plataforma.»).

**Y un recordatorio que afecta a todas estas sumas:** los **seis episodios
completados con `cost_usd: null`** van contados como **cero**, que es lo que el
servidor dice. Si resultara que sí se facturaron, todo sube.

### Dos precisiones de redacción para A.3

1. **«sin coste para el autor» no es exacto para el banco.** Los 4,44 $ de
   P5-5B **sí** salieron de la cuenta del autor (clave propia); el resto fue con
   el saldo de la plataforma. El párrafo ya lo dice, pero la frase «Las partidas
   se jugaron con el saldo de la plataforma, sin coste para el autor» conviene
   que no arrastre al banco.
2. **«10,48» aparece dos veces en el paper con sentidos distintos**: los
   **10,477101 $** de Haiku en P5-6C y el **10,48 %** de propuestas que pasan la
   puerta en P5-5B (`informe_P55B.md:9,231`). **Si en el texto van sueltos, se
   confunden.**

---

## Una nota sobre la cabecera del apéndice

Dice: «**Todas las partidas de campo se jugaron en Zero Sum 0.1.18 (etiqueta
zero-sum-v0.1.18, commit 9bd0ddf)**». **Confirmado en los 216 registros de
episodio**: `coworld_version = 0.1.18`, `coworld_id = cow_ebf72b34-…`, **cero
excepciones** (`informe_P5ARI2.md` §1).

**Pero la etiqueta es ANOTADA.** `git ls-remote` sobre `arisklar6/zero-sum` da el
objeto `fca9c260e6…` y **solo al desreferenciar (`^{}`) sale el commit
`9bd0ddf1e707db7cba86281dabf2492e96e47249`**. Quien compruebe sin `^{}` verá
otro hash y creerá que no cuadra. **Y el repositorio se llama `arisklar6/zero-sum`**
(`informe_P5ARI3.md` §4).

---

## Resumen en cinco líneas

**De las 56 filas del apéndice, 47 coinciden sin reserva; nueve tienen algo que
arreglar y dos de ellas cambian lo que la cifra dice.**

**La peor es «unas dieciocho opciones»: el apéndice añade «con las piernas
listas» y su fuente no dice eso —el 18 es del puñado comparador en el tic de
ventana, y con las piernas listas la papeleta mide 16—; la segunda es la meseta
de calma, que va de 2.400 a 8.000 y no de 2.300 a 8.200.**

**Tres filas citan el informe equivocado: las manos bien servidas son de
`informe_P51_E.md:81` y no de P5-1D, los rivales del mundo lento son de
`informe_P56B.md:51,60` y no de P5-6C, y los seis episodios sin coste son de
`informe_P5ARI_cierre.md`, que es el nombre real del fichero que se cita.**

**De las tres «por confirmar», dos quedan resueltas —los 18 candidatos en
`informe_P53D.md:21` y las seis casillas en `informe_P58A.md:91`, exacta— y la
tercera no: ninguna cifra del paper vale 5,0 %, y la única candidata de la
configuración real es el 5,62 % de `informe_P57C.md:187`, que sería una de cada
dieciocho.**

**A.3 acierta las cinco cifras pero se deja 2,43 $ en diez series y sondas, y no
da el total, que es 31,33 $: 16,08 de plataforma, 10,81 de modelo por el sidecar
y 4,44 de modelo con clave propia.**

---

**PARO AQUÍ.**
