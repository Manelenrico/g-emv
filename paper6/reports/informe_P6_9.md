# P6-9 · Medir el rescate y el hueco de valor antes de construir

*27-sep-2026. Solo lectura de los diarios de P6-6 (A0, A1) y P6-8 (A2): 120 vidas,
60 partidas. Ninguna partida. `motor/model.py` intacto
(`1e511978c251130e95169ebf8443efa1`), 202 archivos de `CONGELADO.md` sin alterar,
nada subido ni borrado. Sin proponer arreglos.*

**Definiciones, todas leídas del diario:** un **golpe** es una entrada de
`damage_taken`; la **causa** es la fuente del primer golpe del episodio
(`zone` = anillo; `P<slot>` con arma de daño en la mano = rival con arma; con
la mano vacía o sin verlo = rival sin arma); la **distancia de camino** es
`decisor_zs.campo_geodesico` hacia la casilla de la víctima, evaluado en la
casilla del otro, por el coste de movimiento leído del mundo (**11 tics por
casilla**); las posiciones de los dos son las **reales** de sus diarios. Todo
está en `cantera/paper6/P6_9.json` (con las listas de episodios) y sale de
`mide_P6_9.py`.

---

## 1 · EL TIEMPO DE RESCATE

### El N, elegido con los huecos entre golpes

Distribución de los huecos entre golpes consecutivos de una misma vida:

| hueco (tics) | ≤ 24 | 25-48 | 49-96 | **97-144** | 145-240 | 241-480 | > 480 |
|---|---:|---:|---:|---:|---:|---:|---:|
| A0 (n = 595) | 409 | 38 | 33 | **8** | 23 | 26 | 58 |
| A1 (n = 719) | 577 | 35 | 15 | **14** | 20 | 12 | 46 |
| A2 (n = 784) | 640 | 33 | 34 | **16** | 7 | 12 | 42 |

Dentro de una pelea los golpes van a ≤ 24 tics (el anillo pega cada 24; los
rivales cada 18-30); entre 97 y 144 hay un valle claro; lo de más de 240 son
peleas distintas. **Propongo N = 96 tics** (4 s; cuatro partes E2, dos E1): por
encima del hueco de una pelea y por debajo del valle. Abajo va la sensibilidad a
48, 144 y 240; nada de lo que sigue cambia de signo con ella.

### Reparto, mediana y percentiles (N = 96)

| brazo · causa | episodios | de un solo golpe | **mueren** | duración p25 / **p50** / p75 / p90 | golpes p50 | duración de los que **mueren**, p25 / p50 / p75 |
|---|---:|---:|---:|---|---:|---|
| **A0** · anillo | 68 | 16 | 19 | 24 / **72** / 216 / 359 | 4 | 167 / **239** / 359 |
| A0 · rival con arma | 60 | 27 | 8 | 0 / **10** / 87 / 154 | 2 | 59 / **154** / 167 |
| A0 · rival sin arma | 27 | 9 | 4 | 0 / **23** / 111 / 160 | 2 | 35 / 35 / 35 |
| **A1** · anillo | 58 | 9 | 20 | 24 / **96** / 311 / 383 | 4 | 215 / **335** / 383 |
| A1 · rival con arma | 59 | 28 | 9 | 0 / **10** / 51 / 144 | 2 | 107 / **144** / 196 |
| A1 · rival sin arma | 15 | 6 | 2 | 0 / **12** / 58 / 87 | 2 | 58 / 58 / 542 |
| **A2** · anillo | 50 | 4 | 21 | 48 / **216** / 407 / 503 | 9 | 359 / **407** / 479 |
| A2 · rival con arma | 56 | 18 | 12 | 0 / **43** / 135 / 275 | 3 | 119 / **173** / 301 |
| A2 · rival sin arma | 11 | 4 | 2 | 0 / **18** / 72 / 119 | 2 | 23 / 23 / 119 |

Tres cosas:

1. **La mitad de los episodios con un rival son un solo golpe** (27 de 60 en A0,
   28 de 59 en A1, 18 de 56 en A2): el rival pega una vez y la cosa se acaba,
   por un lado o por otro. La mediana de un episodio con rival armado es de
   **10 tics** en A0 y A1 — menos que un paso (11).
2. **Los que matan duran más**: un rival armado tarda **154 / 144 / 173 tics** en
   matar (mediana), es decir, 14-16 pasos; el anillo, **239 / 335 / 407**. Ésa es
   la ventana real de un rescate: **entre 13 y 37 pasos**, según la causa.
3. **En A2 los episodios del anillo son más largos y con más golpes** (p50 216
   tics y 9 golpes, contra 72 y 4 en A0): sin el bucle de la mochila que lo
   clavaba, el cuerpo aguanta más dentro del fuego antes de morir o salir.

*Sensibilidad:* con N = 48 salen 188 / 147 / 151 episodios y las medianas de
rival armado siguen en 10 / 10 / 20; con N = 240, 124 / 98 / 94 y 17 / 51 / 99.
El orden de los brazos y de las causas no cambia.

---

## 2 · ¿HABRÍA LLEGADO?

Solo episodios con el otro hermano **vivo** al empezar. «Llegaría» = camino ×
11 < duración del episodio. «Llegó» = en algún tic del episodio estuvo a ≤ 1
casilla de la víctima.

| brazo · causa | con el otro vivo | dist. inicial p50 | llegada p50 (tics) | **llegaría** | **llegó** | se acerca / se aleja | qué hizo el otro |
|---|---:|---:|---:|---:|---:|---|---|
| **A0** · anillo | 54 | **2** | 22 | 35 | **29** | 14 / 11 | `noop` 86 %, `move` 4 % |
| A0 · rival con arma | 53 | **3** | 33 | 21 | **14** | 12 / 6 | `noop` 88 %, `move` 5 %, `atacar` 2 % |
| A0 · rival sin arma | 21 | 2 | 22 | 10 | 9 | 1 / 5 | `noop` 80 % |
| **A1** · anillo | 37 | **7** | 77 | 24 | **9** | 15 / 12 | `noop` 85 %, `move` 9 % |
| A1 · rival con arma | 46 | **6** | 66 | 10 | **1** | 8 / 9 | `noop` 89 %, `move` 5 % |
| A1 · rival sin arma | 10 | 8 | 88 | 1 | 0 | 2 / 2 | `noop` 91 % |
| **A2** · anillo | 38 | **6** | 66 | 29 | **12** | 20 / 13 | `noop` 66 %, `ir_pareja` 28 %* |
| A2 · rival con arma | 44 | **5** | 66 | 20 | **2** | 12 / 9 | `noop` 66 %, `ir_pareja` 12 %*, `atacar` 10 % |
| A2 · rival sin arma | 7 | 3 | 44 | 2 | 1 | 2 / 1 | `noop` 65 % |

*\* el `ir_pareja` de A2 incluye los tics de enfriamiento en que el envoltorio
jugado lo creaba y el mundo rechazaba la orden (P6-8 §C.0): no es movimiento.*

Y en **las muertes** (episodios que acaban en muerte, con el otro vivo al
empezar):

| | A0 | A1 | A2 |
|---|---:|---:|---:|
| muertes con el otro vivo | 20 | 20 | 24 |
| distancia inicial p50 | **3** | **8** | **6** |
| duración p50 | 216 | 335 | 359 |
| **habría llegado** (camino × 11 < duración) | **19** | **16** | **22** |
| **llegó** (a ≤ 1 casilla en algún momento) | **16** | **3** | **8** |

**El tiempo alcanza casi siempre; el cuerpo no va.** En A1 el otro habría
llegado en 16 de 20 muertes y llegó en 3; en A2, 22 de 24 y llegó en 8. En A0
llega en 16 de 20 —**no porque vaya (elige `noop` el 86-88 % del tiempo), sino
porque ya estaba a 2-3 casillas**. Y en A1 y A2, cuando el rival es armado, el
otro llegó **1 de 46** y **2 de 44** veces. El «rescate» que existe en este
cuerpo es **estar ya al lado**, no acudir.

---

## 3 · EL HUECO DE VALOR

Tics con detalle de candidatos (cada 24), piernas listas, hermano vivo,
`ir_pareja` candidato y ganador distinto de `ir_pareja`: **d(ir_pareja) −
d(ganador)**, positivo = lo que le falta a `ir_pareja` para ganar. «Lejos» =
camino × 11 > T; tomo **T = 100 tics** (9 pasos): es la mediana redondeada de lo
que tarda en matar un rival armado (144-173) menos el margen que ya medí en
P6-6 para llegar (p50 de espera real 57 tics); con T = 200 salen los mismos
órdenes.

| brazo | tics (T = 100) | p25 / **p50** / p75 / p90 | quién gana | dist. p50 al hermano |
|---|---:|---|---|---:|
| **A0** | 55 | 0,025 / **0,042** / 0,056 / 0,228 | `noop` 33, `ir_centro` 13, `move` 7 | 9 |
| **A1** | 1.482 | 0,079 / **0,178** / 0,259 / 0,301 | `noop` 954, **`coger` 325**, `move` 153 | 15 |
| **A2** | 998 | 0,033 / **0,094** / 0,158 / 0,179 | `noop` 801, `move` 111, `ir_objeto` 50 | 11 |
| A1, T = 200 | 791 | 0,082 / 0,245 / 0,301 / 0,301 | `noop` 414, `coger` 324 | |
| A2, T = 200 | 548 | 0,029 / 0,086 / 0,154 / 0,166 | `noop` 542 | |

Lo que el vínculo tendría que superar, en unidades de `d` del motor:

* En **A0** casi nunca se da la situación (55 tics en 40 vidas: el cuerpo no
  está lejos) y cuando se da, el hueco es **0,042**.
* En **A1** el hueco es **0,178**, inflado por el bucle de la mochila (`coger`
  gana 325 veces con un empate falso) y por el destino equivocado de
  `ir_pareja` (P6-8).
* En **A2**, con los dos arreglos, el hueco limpio es **0,094** (p75 0,158; p90
  0,179), y lo que gana es **`noop` en 801 de 998 tics**: no es que otra cosa
  valga más, es que **quedarse quieto vale más que ir**. Ir cuesta F-4-ALCANCE
  (+0,041 de M en P6-8 §C.4) y, con rival contado, S-8 (+0,118); no hay nada
  en la tabla que lo compense.

*(Estas cifras son `d`, la distancia al atractor que sale de `model.py` con las
seis magnitudes; el `M` de una fila entra en `d` por su reparto (`A42.REPARTO`)
y los pesos de `DEFAULT_CONFIG`, así que 0,094 de `d` **no** es 0,094 de `M`.
Cuánto `M` hace falta para cerrar un hueco de 0,094 se mide en el banco con la
fila puesta, no se estima aquí.)*

---

## 4 · LA FILA APAGADA DEL TRES: `S-COMPANIA`

Sigue en el código: `appraisal_zs_v42_exp.py:287-314` (constantes y candado) y
`:1003-1038` (cálculo). **Apagada** por `COMPANIA_ON = False` (candado del banco
62, 5-sep-2026). Solo se describe.

**Qué mide.** «En CALMA, estar LEJOS de la hermana genera un malestar S de
FONDO, creciente con la distancia y con techo, aliviable por acercarse». Fondo
que ordena, no correa: «el botín cercano gana igual».

**Cómo se calcula** (`:1003-1038`):

```
F["S-COMPANIA"] = 0
si COMPANIA_ON y no pareja_muerta y no _anillo_muerde:
    pos_hermana = la vista, o la del parte fresco (mem.parte_fresco)
    calma = ni yo cazado (ningún agresor en la ventana S-7)
            ni ella cazada (su parte fresco no declara agresor)
    si calma y d = dist(pos, pos_hermana) > COMPANIA_D0:
        F["S-COMPANIA"] = COMPANIA_TECHO * min(1, (d − COMPANIA_D0) / COMPANIA_RANGO)
```

| parámetro | valor | comentario del código |
|---|---|---|
| `COMPANIA_D0` | **2,0** casillas | «alcance del don (2): dentro, ya estoy con ella» |
| `COMPANIA_RANGO` | **6,0** casillas | «de d0 a d0+6 la fila sube a su techo» |
| `COMPANIA_TECHO` | **0,22** | «el valor barrido en el banco 62» |
| `COMPANIA_ANILLO_S` | **5,0** s | apagada si mi casilla arde en < 5 s (gate por inminencia, no por valor de F-ANTICIPACION) |
| reparto `A42.REPARTO` | **(0,1 · 0,1 · 0,8)** | S-dominante |
| distancia | euclídea (`math.dist`) | no Chebyshev |
| `COMPANIA_ON` | **False** | candado 62 |

**Por qué se apagó** (el candado, `:302-314`, transcrito): «las dos anclas
selladas por la mesa resultaron incompatibles»: por debajo de 0,22 «la fila no
cambia nada (ni junta: en la escena tangencial ambos brazos acaban a 11,7)»; de
0,22 en adelante «lo único que cambia es que pierde comida (la ración a 2 en
dirección opuesta: v32 la coge, v33 no)». Y «cuando la hermana está hacia el
centro, el anillo ya las junta; cuando está tangencial, ningún techo por debajo
del hambre las acerca. No hay ventana entre inerte y hambre». Queda «apagada
hasta que la mesa reselle las anclas o la descarte».

**Dos cosas que conviene tener delante al decidir**, medidas aquí y no en el
banco 62: (i) el hueco que la fila tendría que cerrar es **0,094 de `d` en A2**
(y `noop`, no la comida, es lo que gana en 801 de 998 tics); (ii) la otra fila
de compañía, `S-SOLEDAD` (`:1092-1096`, techo 0,5, rampa 30 s), **no se enciende
nunca con el hermano vivo** en ninguna serie: su `P` cuenta la voz como
presencia (`presencia()`, `:698`: «0,5 oída hace < 3 s») y el parte llega cada
25 o 48 tics, así que `ticks_sin_compania` se pone a cero en cada parte
(`:625-630`). Con el canal de la pareja encendido, la soledad del tres no
existe: solo la muerte del hermano la dispara (por eso S-SOLEDAD = S-MUERTE-PAREJA
en los censos de P6-6 y P6-8).

---

## LO QUE ME LLEVO

1. **La ventana de rescate es corta y conocida**: un rival armado mata en
   144-173 tics (13-16 pasos); el anillo en 239-407. La mitad de los episodios
   con rival son un solo golpe.
2. **El tiempo casi siempre alcanza y el cuerpo no acude**: habría llegado en
   16-22 de 20-24 muertes, llegó en 3 (A1) y 8 (A2); en A0 llega en 16 porque
   ya estaba a 3 casillas, no porque vaya (`noop` 86-88 %).
3. **El hueco de valor limpio es 0,094 de `d`** (A2, p75 0,158), y lo que gana
   es quedarse quieto.
4. **`S-COMPANIA` está entera y apagada** con techo 0,22, D0 2, rango 6, gate de
   calma y anillo, S-dominante; y `S-SOLEDAD` no puede encenderse con el canal
   abierto porque la voz cuenta como compañía.

*La decisión de cuánto vale estar juntos es de Manel. Aquí están los números
con los que tomarla.*

## LOS ARCHIVOS NUEVOS, CON SU MD5

| archivo | md5 |
|---|---|
| `cantera/paper6/mide_P6_9.py` | `8ea41e7f3ff2e6526280bbdbbb04eec1` |
| `cantera/paper6/P6_9.json` | `02c214a03cfa43345733b4f8d7c35ffa` |

*Ningún md5 de esta tabla se escribió antes de calcularlo.*

## CONTROL FINAL

| | |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` — intacto |
| archivos de `CONGELADO.md` | 202 comprobados, 0 alterados |
| partidas jugadas | ninguna · coste 0,0000 USD |
| patrones de clave en lo nuevo | ninguno |
| subido, empujado o borrado | nada |
