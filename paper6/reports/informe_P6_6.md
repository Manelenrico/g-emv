# P6-6 · Arreglar el oído y el don, mirar el cinco, y repetir P6-4 bien

*27-sep-2026. `motor/model.py` intacto (`1e511978c251130e95169ebf8443efa1`), los
202 archivos de `CONGELADO.md` sin alterar, todo lo del seis en archivos nuevos.
Nada subido a git, nada empujado, nada borrado.*

**Reglas en vigor:** ningún número se escribe antes de calcularlo · antes de
construir contra un problema se mide cuánto daño hace de verdad · antes de
cualquier partida de pago, humo de punta a punta con datos reales · **y la nueva:
los humos usan mensajes reales que pasan por la vía real de lectura, nunca campos
rellenados a mano.**

---

# A · EL CINCO YA TENÍA EL BUCLE

*Coste cero. Solo contar e informar, como pedías.*

Una sola definición para todas las series, para que los números se comparen
(`cantera/paper6/mide_bucle_P6_6.py`):

* **INTENTO** — un tic con `RADIOGRAFIA.elegido` = `soltar_<id>`.
* **EPISODIO** — racha máxima de intentos en la misma casilla y el mismo id, con
  huecos ≤ 3 tics (el bucle alterna `drop`/`coger`: hueco de 2).
* **BUCLE** — episodio con **≥ 3 intentos**. Uno o dos seguidos son un don
  normal; tres ya es la oscilación.
* **TICS EN BUCLE** — `fin − ini + 1` de cada episodio en bucle.
* **VIDA** — un diario de agente: un asiento en una partida.

## Lo que salió

| serie (0.1.18) | vidas | tics vividos | episodios | en bucle | **tics en bucle** | % de tics | **vidas con bucle** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **P5-6C** | 200 | 1.501.210 | 1.206 | 1.108 | **16.647** | 1,11 % | **7** de 200 |
| **P5-7C** | 80 | 698.867 | 1.284 | 1.216 | **22.428** | 3,21 % | **13** de 80 |
| **P5-8I** | 20 | 154.601 | 459 | 449 | **5.624** | 3,64 % | **3** de 20 |
| **P5-8M** | 79 | 641.110 | 1.627 | 1.577 | **29.846** | 4,66 % | **16** de 79 |
| **el cinco entero** | **379** | **2.995.788** | **4.576** | **4.350** | **74.545** | **2,49 %** | **39** de 379 (10,3 %) |
| *P6-4 A0 (0.1.19, referencia)* | 40 | 474.188 | 615 | 549 | **24.842** | 5,24 % | **8** de 40 |
| *P6-4 A1 (sordo, referencia)* | 40 | 490.594 | 8 | **0** | **0** | 0,00 % | **0** de 40 |

**El 95,1 % de todos los episodios de don del cinco eran bucle**, no don. De los
4.576 episodios, 4.350 eran la oscilación.

## El peor episodio de cada serie

| serie | tics | intentos | diario | objeto y casilla | % de esa vida |
|---|---:|---:|---|---|---:|
| P5-6C | **2.514** | 1.257 | `P56C_t4_A_21727122` s11 | `rations` en [21,17] | **30,6 %** |
| P5-7C | **2.562** | 1.282 | `P57C_t3_Q_21727122` s11 | `rations` en [24,18] | 20,7 % |
| P5-8I | 1.407 | 704 | `P58I_t1_A_20679832` s11 | `rations` en [18,14] | 17,6 % |
| P5-8M | 2.477 | 1.239 | `P58M_t3_K_21727122` s11 | `rations` en [27,22] | 20,0 % |
| *P6-4 A0* | **3.723** | 1.862 | `P64_t3_A0_22250767` s10 | `first_aid` en [26,21] | **29,7 %** |

**Tres de los cuatro peores episodios del cinco son la misma semilla
(21727122), el mismo asiento (11) y el mismo objeto (`rations`).** La semilla fija
el mapa: hay una casilla de ese mapa donde el cuerpo se queda clavado.

## Corrección de un número de P6-5

En `informe_P6_5.md` §5.4 escribí *«asientos afectados 9 de 40»*. Ese 9 salía de
contar asientos con **al menos un episodio reabsorbido**, no con bucle. Con la
definición única de aquí (**≥ 3 intentos**), son **8 de 40**. Lo mismo con los
tics: allí puse 24.859 (suma de los reabsorbidos) y aquí 24.842 (suma de los que
son bucle). Dos definiciones mezcladas en un mismo informe; ésta es la buena y es
la que se usa en todo P6-6.

---

# B · LOS DOS ARREGLOS

## B.1 · El oído

`cantera/paper6/oido5_P6_5.py`, ya escrito y probado en P6-5, ahora enganchado.
El cuerpo del cinco lee el parte del hermano en **un solo sitio** con un parser
estricto de marca (`appraisal_zs_v42_exp.py:578` → `parte.py:48`, `^E1 `), y
`policy_pareja` emite `E2`. El remiendo pone en el chat un **mensaje gemelo** con
la cabeza traducida a E1, junto al E2, y **lo valida con el parser del cinco**:
si `PARTE.parsea` no lo acepta, no se inyecta nada. El juez es el parser.

## B.2 · El don: «lo dado, dado está»

> **N = min( d × coste_movimiento(speed) + MARGEN , CESION_CADUCA_S × tick_rate )**

| pieza | valor | de dónde sale |
|---|---|---|
| `d` | distancia Chebyshev del regalo a donde el cuerpo **cree** que está su hermano (`mem.pareja_pos`) | es lo que tiene en la mano al decidir, no lo que sabría un dios |
| `coste` | **11 tics/casilla** | `mundo.coste_movimiento(speed)`, leído del mundo y del `speed` de la observación, igual que `decisor_zs.py:740`. **No cableado** (CLAUDE.md) |
| `MARGEN` | **268 tics** | **el p90 del margen medido** (ver abajo) |
| tope | **720 tics** | `CESION_CADUCA_S × tick_rate` = 30 s × 24. **No lo pongo yo**: es el plazo que ya fijaste para que una cesión no reclamada vuelva a ser mía (`appraisal_zs_v42_exp.py:330`) |

### El margen, justificado con datos y no elegido

`cantera/paper6/mide_espera_P6_6.py` mide, sobre **las 69 recogidas que de verdad
ocurrieron** (12 en A0 de P6-4 + 57 en las cuatro series del cinco), el
**margen = espera real − d × coste**:

| | valor |
|---|---:|
| `d` (casillas) | mediana **1** · máximo 7 |
| espera real (tics) | mediana **57** · máximo 5.144 |
| margen: mediana | **45** |
| margen: p75 | 106 |
| **margen: p90** | **268** |
| margen: p95 | 1.151 |
| márgenes negativos (llegó antes que la línea recta) | 14 de 69 |

Cobertura de cada margen candidato sobre esas 69 recogidas reales:

| margen | recogidas que N cubriría |
|---:|---|
| 44 | 34 de 69 (49,3 %) |
| 92 | 50 de 69 (72,5 %) |
| 168 | 57 de 69 (82,6 %) |
| **268 (p90, el elegido)** | **62 de 69 (89,9 %)** |
| 720 (el tope) | 65 de 69 (94,2 %) |

Elijo el **p90** porque con la mediana (45) se perdería la mitad de las
recogidas reales, y media recogida perdida es media razón para dar. El p95
(1.151) ya se sale del tope de la casa, así que el tope mandaría siempre y el
margen dejaría de significar nada.

### Cómo se entera de que ha soltado, sin inventar contabilidad

`decisor_zs.py:900-904` **ya** escribe `mem.cedidos[pos]` en cada `soltar`. Se
envuelve `D.decide` y justo después se copia esa cesión a un cuaderno propio
(`mem._dados6`) que el borrado del PROMPT_24 no alcanza; luego se envuelve
`D.candidatos` para esconder `coger` mientras el plazo viva. Dos envoltorios,
cero código nuevo en la ruta de decisión. **Ni una fila nueva, ni una regla de
movimiento, ni un byte del cinco.** Si el hermano muere, el regalo se libera en
el acto — que es lo que ya decía el PROMPT_24.

## B.3 · Los humos

### `humo_P6_6.py` — **6 de 6**

| humo | qué prueba | resultado |
|---|---|---|
| **a** | el **bucle real** replayado tic a tic desde el primer tic de vida de `P64_t3_A0_22250767` s10, por `Memoria.observa` + `D.decide` con su `Bloqueos` | **sin arreglo 43 soltar y 6 recuperaciones · con arreglo 43 soltar y 0 recuperaciones** |
| b | S-PROVISION vuelve con un parte E2 **real** | 0 → **0,30000**; candidato del don `[]` → `['soltar_first_aid']` |
| c | el hp del hermano es el del parte | **83 (banda) → 100 (parte)** |
| d | el plazo sale del mundo | d=3 → N=**301** (3×11+268) · d=50 → N=**720** (tope) |
| e | el regalo se libera | vence en N, distingue objeto y casilla, y muere con el hermano |
| f | con partes E1 (ojos apagados) el oído no hace nada | 0 gemelos, la misma obs, y el E1 se sigue leyendo |

**Límite honesto del humo `a`:** es un contrafactual decisión a decisión sobre
las observaciones REALES, no una resimulación — el estado que llega en cada tic
es el que grabó la partida, no el que produciría la trayectoria arreglada. Lo que
prueba es exactamente lo que dice: **en los tics reales en que el cuerpo recuperó
su regalo, con el arreglo no lo recupera.** Por eso el número de `soltar` no baja
(43 en los dos casos): las mochilas vienen del diario.

### `humo_red_P6_6.py` — el bucle de red entero, y el agujero que tenía

Corre `PC.decisor` con un WS falso, 200 observaciones reales, los partes E2
**emitidos por `parte2.emite`** (el emisor de producción) metidos por el cable, y
los dos arreglos aplicados:

```
arreglos          : {'oido': True, 'don': True, 'margen': 268}
partes E2 metidos : 8 (del emisor de produccion, por el cable)
acciones emitidas : 200 de 200 observaciones
registros ojos    : {'dicho': 8, 'inyectado': 95}
errores           : 0
mem.parte         : {'slot': 11, 't': 425, 'pos': (23, 21), 'hp': 100.0, ...}
```

**El agujero que encontré al escribirlo:** el grabado de 200 tics **ya traía
mensajes `E1` del hermano** (son de una serie del cinco). Con ellos dentro,
`mem.parte` podía venir de **esos** y la comprobación del oído no probaría nada
— el mismo tipo de humo vacío de P6-3. Ahora el humo **quita del cable todos los
mensajes del hermano** y sólo deja el E2, con una guarda explícita que revienta
si se cuela un E1. Así `mem.parte` sólo puede venir del gemelo.

**Lo que este humo NO prueba, y lo digo:** en esos 200 tics el cuerpo no eligió
`soltar` ni una vez (`registros don: {}`), así que la regla del don no se ejerció
por el cable. Su efecto está probado en el humo `a`, con el bucle real.

### En la imagen

`Dockerfile.pareja6` añade la custodia md5 de las tres piezas nuevas y corre
`humo_red_P6_6.py` con `GEMV_OJOS=1` **dentro del build**, más los arreglos con
`GEMV_OJOS=0`. El build pasó con los dos, y con las custodias de siempre:

```
custodia OK model.py md5 1e511978c251130e95169ebf8443efa1
custodia OK decisor 8fa03547e3228ef9df4aa94c444f9252 appraisal 98c13d60167c80cc8334c965be75c640
custodia OK parte2 67ba0003... oyente2 4e8b657f... policy_pareja 796fc642...
custodia OK oido5 4f7aa3b3... arreglos 4d10ea09... policy_pareja6 933ad20f...
custodia OK: ninguna clave sk-ant- en /app
```


---

# C · P6-4, REPETIDO BIEN

**Coste: 2,7142 USD** de los 5 (39 partidas con coste facturado; la
`P66_t4_A1_21936580` acabó `completed` con `cost_usd = None`, así que el total
real es ese o ligeramente mayor). 40 partidas, 80 diarios, las **mismas 20
semillas** de P6-4, 0.1.19, `roster_lento_v2`. A0 = `gemv-p6-A0-oido:v1`
(`2a2e661e…`), A1 = `gemv-p6-A1-oido:v1` (`4a0c270a…`), **la misma imagen**;
sólo cambia `GEMV_OJOS`.

## C.0 · Primero, que los dos arreglos estuvieran vivos en la partida

| | P6-4 A0 | P6-4 A1 | **P6-6 A0** | **P6-6 A1** |
|---|---:|---:|---:|---:|
| partes del hermano recibidos | 9.282 | 18.315 | 9.562 | 14.376 |
| gemelos E1 producidos por el oído | — | — | 0 (son E1) | **14.376** |
| tics sin parte fresco **con el hermano vivo** | 0 | *todos* | **0** | **0** |
| parte fresco, sobre tics con el hermano vivo | 99,98 % | 0,00 % | **99,98 %** | **99,98 %** |
| S-PROVISION | 19,16 % | 0,00 % | 23,41 % | **14,50 %** |
| S-DANO-PAREJA | 20,53 % | 93,27 % | 20,01 % | **19,34 %** |
| tics en bucle soltar/coger | 24.842 | 0 | **0** | **0** |
| episodios de don reabsorbidos | 564 de 615 | 1 de 8 | **1 de 67** | **3 de 38** |

**Los dos arreglos funcionan en campo.** El oído no deja ni un hueco (14.376
partes, 14.376 gemelos, 0 tics sin parte con el hermano vivo), y el bucle ha
desaparecido de los dos brazos.

## C.1 · El sello, predicción a predicción

| # | predicción sellada | salió | veredicto |
|---|---|---|---|
| 1 | parte fresco en A1 ≥ 90 % de los tics | **85,80 %** | **FALLA por su letra.** Y la culpa es de cómo la escribí: el denominador incluye tics con el **hermano muerto** (14,18 % en A1, 4,08 % en A0), donde por diseño no puede haber parte fresco. Sobre tics con el hermano vivo, **99,98 %**, con **0 huecos**. El mecanismo está; la predicción estaba mal formulada. |
| 2 | S-PROVISION en A1 entre 10 % y 30 % | **14,50 %** | acierta |
| 3 | S-DANO-PAREJA en A1 ≤ 35 % | **19,34 %** | acierta |
| 4 | tics en bucle = **0** en los dos brazos | **0 y 0** | **acierta** (la más dura del sello) |
| 5 | dones efectivos en A0 ≥ 100 | **66** | **FALLA**, y por la razón que dejé escrita: los 564 «reabsorbidos» de P6-4 **no eran dones esperando a liberarse, eran el bucle**. Los intentos pasan de 12.764 a **67** y los episodios de 615 a **67**; los efectivos, de 51 a 66. |
| 6 | tasa de recogida entre 10 % y 40 % en los dos brazos | A0 **25,76 %** (17/66) · A1 **20,00 %** (7/35) | acierta |
| 7 | A1 recoge **más o igual** que A0 | 20,00 % < 25,76 % | **FALLA.** Fisher p = 0,627: no distingue, pero el signo es el contrario al que predije. Y eso que **33 de los 35 dones de A1 viajaron en un parte E2**. Que el canal lleve el regalo no hace que el hermano vaya a por él. |
| 8 | los dos vivos al cierre en A1 ≥ 18 de 20 | **15 de 20** (A0: 18) | **FALLA.** Fisher p = 0,407. En P6-4 fue 20/20 con el hermano sordo. |
| 9 | «sobrevive el otro tras el primero» sube en A1 (diferencia emparejada positiva) | mediana **+672** tics · A1 mayor en **13 de 20** · signos p = 0,263 | acierta en signo; **no establecido**, igual que en P6-4 (+733,5, p = 0,115) |
| 10 | \|disc\| de S-8 por decisión baja ≥ 20 % en A1 | A0 0,0585 → A1 0,0249: **−57,4 %** | acierta (P6-4: −45,8 %) |
| 11 | recursos contados pisados ≥ 30 % | 13.059 de 26.763 = **48,8 %** | acierta (P6-4: 41,4 %) |
| 12 | coste ≤ 3,6 USD | **2,7142** | acierta |

**8 aciertos, 4 fallos.** Los cuatro fallos son informativos y los dejo tal cual.

## C.2 · Lo que pedía el encargo, A0 contra A1, emparejado por semilla

| medida | A0 | A1 | dif. mediana | p (signos) |
|---|---:|---:|---:|---:|
| **vida media de la pareja** | **12.427,9** | **10.936,2** | **−1.301,8** · A1 mayor en 6/20 | 0,115 |
| los dos vivos al aviso (t 7.296) | 18/20 | 15/20 | — | 0,407 (Fisher) |
| los dos vivos al cierre (t 8.076) | 18/20 | 15/20 | — | 0,407 (Fisher) |
| sobrevive el otro tras el primero (mediana) | 912 | 1.740 | **+672** · A1 mayor en 13/20 | 0,263 |
| tics 2c (recurso que falta y el otro ve), por vida | 7.057,9 | 5.481,7 | −1.445,5 | 0,824 |
| golpes a ciegas | **0** | **0** | — | — |
| \|disc\| S-8 por decisión | 0,0585 | 0,0249 | −57,4 % | — |

**Lo que cambia respecto a P6-4, y hay que decirlo entero:** con el hermano
sordo (P6-4), A1 vivía **más** (+410 de media, +205 de mediana emparejada) y
llegaba entera al cierre en 20/20. Con el hermano **oyendo** (P6-6), A1 vive
**menos** (−1.491,7 de media, −1.301,8 de mediana emparejada, A1 mayor sólo en 6
de 20) y llega entera al cierre en 15/20. Ninguna de las dos diferencias está
establecida (p = 0,115 en las dos direcciones, con 20 semillas), pero el signo
se ha dado la vuelta. **Lo único que aguanta en las dos series** es que el
segundo sobrevive más tiempo al primero con los ojos (+733,5 y +672) y que la
sorpresa de S-8 baja (−45,8 % y −57,4 %).

**Una pista de por qué, medida, no supuesta** (censo de filas, A1 − A0):

| fila | A0 | A1 | Δ p.p. |
|---|---:|---:|---:|
| **F-HERMANO-AMENAZA** | 6,09 % | **19,78 %** | **+13,69** |
| S-SOLEDAD / S-MUERTE-PAREJA | 4,08 % | 14,18 % | +10,10 |
| S-HERIDO | 1,92 % | 6,52 % | +4,60 |
| R-HERMANO-FALTA | 1,08 % | 3,98 % | +2,90 |
| S-8-EXPOSICION | 70,61 % | 48,54 % | −22,07 |
| S-PROVISION | 23,41 % | 14,50 % | −8,91 |

Con el parte entendido **y** los rivales contados, `F-HERMANO-AMENAZA` se
enciende **más de tres veces más** a menudo: el oyente mete en la percepción
rivales que están cerca del hermano y que el cuerpo no ve, y la fila de la
amenaza al hermano —que en P6-4 A1 estaba a medias, sin parte— ahora dispara
con las dos cosas. Es un efecto de los ojos que P6-4 no podía medir porque tenía
el oído roto. **No digo que sea la causa de que A1 viva menos: digo que es lo
que se ve, y que es lo primero que hay que mirar.**

## C.3 · El don: soltados, recogidos, usados

| | P6-4 A0 | P6-4 A1 (sordo) | **P6-6 A0** | **P6-6 A1** |
|---|---:|---:|---:|---:|
| intentos (tics `soltar_*`) | 12.764 | 8 | **67** | **38** |
| episodios | 615 | 8 | 67 | 38 |
| reabsorbidos | 564 | 1 | **1** | **3** |
| **dones efectivos** | 51 | 7 | **66** | **35** |
| de ellos `first_aid` / `rations` | 21 / 30 | 4 / 3 | 41 / 25 | 22 / 13 |
| **viajan en un parte E2** | 0 | 7 de 7 | 0 (son E1) | **33 de 35** |
| **recogidos por el hermano** | 12 (23,5 %) | 1 (14,3 %) | **17 (25,8 %)** | **7 (20,0 %)** |
| **usados** | 11 | 1 | **16** | **7** |

Tres cosas ciertas:

1. **La regla «lo dado, dado está» hace lo que tenía que hacer**: de 564
   reabsorbidos a 1, y de 12.764 tics a 67 intentos. El don ya es un acto, no un
   tic.
2. **Casi todo lo que se recoge se usa** (16 de 17 y 7 de 7). Sigue siendo así.
3. **¿Se recoge más con los ojos? No.** 20,0 % contra 25,8 %, Fisher p = 0,627.
   El canal lleva el regalo (33 de 35) y el hermano **no va a por él más**. La
   hipótesis del paper tres —*«el parte dice lo que uno lleva, nunca lo que ha
   dejado en el suelo»*— era cierta como descripción del canal y **falsa como
   explicación de por qué no se recoge**: se arregló el canal y la recogida no
   se movió. Lo que falta no es saber dónde está el regalo; es que el cuerpo
   quiera ir a por él. Y eso es una decisión de Manel, no un arreglo.

## C.4 · El oyente con lo contado (A1)

| | P6-4 A1 | **P6-6 A1** |
|---|---:|---:|
| tics con algo contado (a10 / a11) | 222.109 / 223.991 | 172.097 / 175.606 |
| se aparta de un rival contado | 1.160 | **457** |
| recurso contado pisado | 14.541 (41,4 %) | **13.059 (48,8 %)** |
| recurso contado que caduca sin pisarlo | 20.579 | 13.704 |
| rival contado seguía donde se dijo / ya se había movido | 4.406 / 1.269 (77,6 %) | 4.302 / 1.480 (**74,4 %**) |
| huye de un contado hacia un armado visible (daño 1) | 31 | **13** |
| «los dos al mismo destino» (contador de P6-4, **contaminado**) | 712 | 461 |

El contador «los dos al mismo destino» sigue siendo el de P6-4, que P6-5
demostró contaminado por `noop`. **La cifra buena está en D.**

---

# D · LOS CHOQUES, OTRA VEZ, CON LOS DIARIOS NUEVOS DE A1

*Coste cero. Mismo medidor que P6-5, palabra por palabra
(`mide_disputa_P6_6.py`, sólo cambia la carpeta y el archivo de salida).*

| | P6-5 (P6-4 A1, sordo) | **P6-6 A1** |
|---|---:|---:|
| tics con los dos en `ir_objeto` y objetivo legible | — | 112 |
| **disputas (mismo objetivo)** | **22** | **55** |
| llegan los dos / no llega ninguno | — | 39 / 10 |
| desaparece sin que llegue ninguno | — | 10 |
| **tics perdidos por el que llega segundo, suma** | — | **1.610** |
| mediana / máximo por disputa | — | 22 / 484 |
| **por vida (40)** | **9,3** | **40,2** |
| **% de una vida media** | 0,072 % | **0,368 %** |
| **repartos injustos** (llega primero el que ya llevaba de esa clase) | **0** | **0** |
| entre los tics 481 y 700 (la carrera inicial) | 19 de 22 | **37 de 55** |

**Con el hermano oyendo hay más choques (55 contra 22) y cuestan más (40,2 tics
por vida contra 9,3): cuatro veces más.** Tiene sentido: con el parte entendido
los dos saben dónde está el otro y los dos oyen los mismos recursos contados,
así que apuntan más veces a lo mismo.

**Pero sigue siendo pequeño: 40 tics por vida son el 0,37 % de una vida, y en 40
vidas no hay un solo reparto injusto.** Dos tercios ocurren en la carrera
inicial al botín, entre los tics 481 y 700, donde el más cercano llega antes y
eso ya lo resuelve el mundo solo.

> **Dicho claro: no construyo el reparto.** El daño ha subido de 9,3 a 40,2 tics
> por vida, y aun así es cuatro décimas de un uno por ciento y no hay
> injusticias que corregir. Si algún día toca, es en los primeros 220 tics y no
> en el resto de la partida.

---

# LO QUE ME LLEVO

1. **El cinco también tenía el bucle**: 74.545 tics en 379 vidas, el 95,1 % de
   sus «dones» eran la oscilación. Nadie lo había contado porque nadie había
   mirado los tics de `soltar` uno a uno.
2. **Los dos arreglos funcionan en campo y se ven en los números**: 0 huecos de
   oído, 0 tics en bucle, 1 reabsorbido de 67.
3. **La comparación de P6-4 estaba contaminada y el signo se ha dado la vuelta**:
   con el hermano oyendo, A1 vive **menos** (−1.301,8 emparejado, p = 0,115) y
   llega entera al cierre menos veces (15 contra 18). Lo que aguanta en las dos
   series: el segundo sobrevive más al primero (+672) y la sorpresa de S-8 baja
   (−57,4 %). Nada establecido con 20 semillas.
4. **Arreglar el canal no arregla la recogida**: 33 de 35 dones viajan y se
   recogen igual (20 % contra 26 %). La frase del paper tres describía bien el
   canal y explicaba mal la conducta.
5. **Los choques cuestan cuatro veces más con el oído puesto y siguen siendo
   pequeños**: 40,2 tics por vida, 0 injustos. No se construye el reparto.
6. **Dos predicciones mías estaban mal escritas, no mal medidas**: la 1 (el
   denominador incluía tics sin hermano) y la 5 (tomé por dones lo que era
   bucle). Las dejo como fallos.
7. **Sobre el reloj**: a mitad de la serie te dije que las partidas llevaban 50
   minutos y algo se reiniciaba. Llevaban 4. Mis esperas en segundo plano no
   habían terminado cuando consulté, y leí mal el `started_at`. Lo corregí en
   el momento.

# LO QUE NECESITO DE MANEL

1. **Qué hacer con la recogida del don.** El canal ya lleva el regalo y el
   hermano no va a por él. Ir a por un recurso contado que además es un regalo
   del hermano es una decisión sobre la tabla del cuerpo, no un arreglo.
2. **Si se investiga por qué A1 vive menos con el oído puesto.** La pista
   medida es `F-HERMANO-AMENAZA` (6,09 % → 19,78 %). Sería coste cero, con los
   80 diarios que ya hay.
3. **Si vale la pena pedir más semillas** para «sobrevive el otro» (+733,5 y
   +672 en dos series, p = 0,115 y 0,263).

# LOS ARCHIVOS NUEVOS, CON SU MD5

| `cantera/paper6/mide_bucle_P6_6.py` | `830cb91ed69200144dc03918e6832d72` |
| `cantera/paper6/mide_espera_P6_6.py` | `b4f341adbc4a4f73f545abd827a92b9c` |
| `cantera/paper6/arreglos_P6_6.py` | `4d10ea09333553ebf7d6ce0afdb73832` |
| `cantera/paper6/oido5_P6_5.py` | `4f7aa3b3ddc4fc32e4b47c1356974415` |
| `cantera/paper6/policy_pareja6.py` | `933ad20fd7cc28dcf46c4b46eb741cab` |
| `cantera/paper6/humo_P6_6.py` | `df726587daf071b46bf6ec192dde1b4c` |
| `cantera/paper6/humo_red_P6_6.py` | `fe35afcde9040123d58709e7c04e9880` |
| `cantera/paper6/Dockerfile.pareja6` | `8092c768a654a6e2eae34975fd6800cc` |
| `cantera/paper6/lanza_P6_6.py` | `b56eaccfd254282dd489120db0f9ab34` |
| `cantera/paper6/mide_P6_6.py` | `353310ced505bb3ab07fedeb6a861aca` |
| `cantera/paper6/mide_don_P6_6.py` | `13a82c6149a1c4b9ec95f7d211b2d0b8` |
| `cantera/paper6/mide_sordera_P6_6.py` | `31a1b978c5631b831c9f98161bfb58dc` |
| `cantera/paper6/mide_disputa_P6_6.py` | `82e6ba8a6475b65dd6710c67dde9d0f6` |
| `cantera/paper6/oyente_P6_6.py` | `d53b3f678c520bc83aa33e20aa5872fd` |
| `cantera/paper6/SELLO_P6_6.md` | `523d4dbb82f12426600fbd46f886107f` |
| `cantera/paper6/P6_6_brazos.json` | `42a4220035442640c541f61cf66d1c7e` |
| `cantera/paper6/P6_6_bucle.json` | `989a6dec714da10b304c8ac48fc69d76` |
| `cantera/paper6/P6_6_espera.json` | `44f0db3c7795ba356df80502d8754157` |
| `cantera/paper6/P6_6_medidas.json` | `5f33f236b307c2b277ecc4648930e442` |
| `cantera/paper6/P6_6_don.json` | `06afaa6d1001ca10edd151d907382b9a` |
| `cantera/paper6/P6_6_sordera.json` | `a5fabace0552799d8f6fc8e7b8e145dc` |
| `cantera/paper6/P6_6_disputas.json` | `76d833ef39684174f54a5a619b1bb309` |
| `cantera/paper6/P6_6_oyente.json` | `0a3272cb0c0836cf4188ff0602f2df41` |

Más los 40 `P66_t*_A*_<semilla>.json` y los 4 `P66_t*_peticiones.json` (las
respuestas de la plataforma) y los 80 diarios en `paintball/runs/P66_*/`.
`policy_pareja.py` sigue en `796fc64229d047410fb351dfa61f871b` (P6-3): no se
tocó; el enganche va en `policy_pareja6.py`.

*Ningún md5 de esta tabla se escribió antes de calcularlo.*

# CONTROL FINAL

| | |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` — **intacto** |
| archivos de `CONGELADO.md` | 202 comprobados, **0 alterados** |
| `policy_pareja.py`, `parte2.py`, `oyente2.py`, `Dockerfile.pareja` | **no tocados** (custodia md5 dentro de la imagen nueva) |
| coste | **2,7142 USD** de 5 (una partida sin coste facturado) |
| patrones de clave en lo nuevo | 3 avisos, los 3 falsos: la propia expresión regular de la custodia en `Dockerfile.pareja6:109,119` y su cita en este informe. **Ninguna clave.** |
| `.env` en `.gitignore` | sí |
| subido, empujado o borrado en git | **nada** (las dos políticas se subieron a la plataforma, como pide el encargo) |
