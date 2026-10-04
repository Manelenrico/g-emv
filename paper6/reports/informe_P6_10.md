# P6-10 · La fila de distancia (S-COMPANIA a distancia de rescate) y la soledad sin voz

*27-sep-2026. `motor/model.py` intacto (`1e511978c251130e95169ebf8443efa1`), los
202 archivos de `CONGELADO.md` sin alterar, todo lo del seis en archivos nuevos.
Nada subido a git, nada empujado, nada borrado.*

**Cambio de Manel antes de jugar, aplicado:** la lejanía graduada la lleva
S-COMPANIA; para no contar dos veces la misma distancia, **S-SOLEDAD no se
enciende por distancia**: queda solo para el hermano muerto, como en el cinco, y
la voz sigue sin contar como presencia. En el momento del cambio **no se había
jugado ninguna partida**; una versión anterior de `filas10_P6_10.py` (no jugada)
encendía S-SOLEDAD por distancia y se retiró. Con el hermano vivo, la S-SOLEDAD
del cinco vale 0 en los 120 diarios de P6-6 y P6-8 (P6-9 § 4: el parte llega
cada 25/48 tics y cuenta como compañía), así que «solo muerto» se cumple por
construcción y el envoltorio **no toca esa fila**.

---

## 1 · S-COMPANIA, RECONFIGURADA (`filas10_P6_10.py`, sin fila nueva)

Envuelve `appraisal_zs_v42_exp.appraise` en memoria: llama al original y añade
S-COMPANIA a las fuerzas **crudas** (antes del `__post_init__` de `State`, que
aplica mínimo basal y techo de volumen), con el reparto que la fila ya tiene en
`A42.REPARTO` (0,1 · 0,1 · 0,8). El veto de `Bloqueos` sigue mandando sobre los
candidatos (humo `e`: 273 tics de enfriamiento sin candidatos de movimiento).

### D0 = 7 casillas de camino — el radio de rescate, calculado

P6-9, N = 96: las muertes por rival armado con el otro vivo al empezar duran
**130,5 / 144 / 166** tics (A0/A1/A2, medianas; n = 8/9/12). Reunidas, **n = 29,
mediana 154** (p25 106, p75 273). La mitad son **77 tics**; entre los **11 tics
por casilla** del mundo (`mundo.coste_movimiento(speed)`), **7,00 casillas**.
`D0 = 7`.

### La fórmula

```
d        = distancia de CAMINO (decisor_zs.campo_geodesico) de mi casilla prevista
           a la del hermano: la vista si lo veo, la del parte fresco si no
amenaza  = max(F-4-ALCANCE, S-7-AGRESOR, F-HERMANO-AMENAZA, F-HERMANO-GOLPE)
calma    = 1 − amenaza
rango    = D0 · (1 + 2 · calma)          # 14 casillas con amenaza plena, 28 en calma total
M        = TECHO · min(1, (d − D0) / rango)   si d > D0;  0 si d ≤ D0
```

* **Dentro de D0, cero.** Fuera, crece con la distancia de camino hasta el
  techo.
* **Más despacio cuanta más calma:** la pendiente es techo/rango, y el rango se
  estira con la calma. La «amenaza» son las cuatro filas de miedo que el cuerpo
  ya calcula: hostil a mi alcance, yo cazado, el hermano amenazado o golpeado.
  Dejo fuera F-DANO (es herida, no amenaza) y S-8-EXPOSICION (con los ojos
  cuenta contados y ya pesa por su lado, P6-8 § C.3).
* **Activa siempre**, también fuera de la calma (con amenaza plena llega al
  techo a 2·D0 = 14 casillas).
* **Posición del hermano:** la obs *prevista* de cada candidato mete al hermano
  como visible en su **última posición vista** (`mem.pareja_pos`, que puede ser
  rancia) — lo encontró el humo `b`: a 13 casillas reales, la fila leía 6. Por
  eso la distancia se calcula a la posición **real de ese tic** (vista, o la del
  parte fresco), guardada una vez por tic con la obs real.

## 2 · S-SOLEDAD

No se toca (arriba). Para que conste lo que el cinco hace con ella: `P` = 1 a
la vista, 0,5 oída hace < 3 s, 0 si no; rampa de 30 s a techo 0,5; `ticks_sin_
compania` se pone a cero al ver **o al oír** (`appraisal:625-630`). Con el
hermano muerto no hay voz (`presencia()`, arreglo A del PROMPT_11), la rampa
arranca y la fila se enciende: es lo que se ve en los censos (S-SOLEDAD =
S-MUERTE-PAREJA en las tres series). Con el hermano vivo: 0 tics en 120 vidas.

## 3 · EL BANCO (`banco_P6_10.py`, diarios de A2)

En cada tic con detalle de candidatos (cada 24), para cada candidato: su
`filas` logueado y su `pos_prevista`; S-COMPANIA calculada en esa casilla
prevista con la distancia de camino a la posición real del hermano (vista o
parte); `d` recompuesta con el mismo reparto y motor (`mide_P6_4.d_de`, fiel a
**1,7·10⁻⁵** en 1.308 candidatos reales). Ganador nuevo = argmin d. **16.638
tics con detalle**: 12.277 dentro de D0, 3.143 lejos (llegada > 100 tics); de los
lejanos, **1.058 con piernas listas** (en enfriamiento `ir_pareja` era el ganador
falso del envoltorio de P6-8, P6-8 § C.0: se excluyen).

| techo | dentro de D0: decisiones que cambian | lejos + listas: gana `ir_pareja` | …gana algo que **acerca** | ventaja de la fila, p25 / **p50** | ≥ 0,158 | comida a ≤ 3: se deja | listas: cambian |
|---:|---|---|---:|---|---:|---|---|
| 0,00 | 2 / 12.277 (0,0 %) | 27 / 1.058 (2,6 %) | 6,9 % | — | — | 0 / 228 | 0 / 4.627 |
| 0,10 | 223 (1,8 %) | 302 (28,5 %) | 46,8 % | +0,017 / +0,048 | 0,0 % | 1 (0,4 %) | 701 (15,2 %) |
| 0,20 | 292 (2,4 %) | 343 (32,4 %) | 76,9 % | +0,034 / +0,098 | 0,0 % | 3 (1,3 %) | 1.131 (24,4 %) |
| 0,30 | 321 (2,6 %) | 358 (33,8 %) | 82,4 % | +0,052 / +0,150 | 15,2 % | 5 (2,2 %) | 1.217 (26,3 %) |
| **0,32** | **321 (2,6 %)** | **361 (34,1 %)** | **83,2 %** | **+0,055 / +0,161** | **57,6 %** | **5 (2,2 %)** | **1.222 (26,4 %)** |
| 0,35 | 325 (2,6 %) | 366 (34,6 %) | 83,9 % | +0,060 / +0,177 | 59,0 % | 5 (2,2 %) | 1.233 (26,6 %) |
| 0,40 | 327 (2,7 %) | 382 (36,1 %) | 86,0 % | +0,069 / +0,204 | 59,8 % | 6 (2,6 %) | 1.258 (27,2 %) |
| 0,50 | 336 (2,7 %) | 406 (38,4 %) | 89,9 % | +0,087 / +0,260 | 62,1 % | 6 (2,6 %) | 1.292 (27,9 %) |
| 1,00 | 355 (2,9 %) | 464 (43,9 %) | 98,5 % | +0,181 / +0,561 | 79,6 % | 14 (6,1 %) | 1.416 (30,6 %) |

### 3a · Dentro de D0

**No es cero: es el 2,6 %** (321 de 12.277 decisiones). Lo digo tal cual. Son
candidatos cuya casilla prevista **cruza D0** hacia fuera (la fila vale 0 en mi
casilla y > 0 en la de un paso que se aleja), que es exactamente lo que la fila
tiene que hacer; y no crece con el techo (2,6 % a 0,30, 2,9 % a 1,00). En mi
casilla, S-COMPANIA es 0 en el 100 % de los tics con d ≤ 7 (humo `a`, 209 tics).

### 3b · Fuera de D0: el techo

El criterio: **el techo más pequeño con el que la ventaja que la fila da a
`ir_pareja` sobre la ganadora logueada alcanza, en la mediana de los tics
lejanos con piernas listas, el p75 del hueco de P6-9 (0,158 de `d`)**. Con
0,30 la mediana es +0,150 (y solo el 15 % de los tics pasan de 0,158); con
**0,32, +0,161 (57,6 % de los tics)**; con 0,35, +0,177. Salto brusco entre 0,30
y 0,32: el motor no es lineal en las fuerzas.

**TECHO = 0,32.** Con él, en los tics lejanos con piernas listas, **el 83,2 % de
las decisiones pasan a acercar al hermano** (logueado: 6,9 %), `ir_pareja` gana
el 34,1 % (logueado 2,6 %; el resto lo ganan candidatos que también acercan), y
**se deja de coger comida cercana en 5 de 228 decisiones (2,2 %)**. Es la mitad
larga del techo del candado 62 (0,22) y un tercio del techo de S-SOLEDAD (0,5).

### Los humos (`humo_P6_10.py`, 5 de 5; `humo_red_P6_10.py`)

Replay tic a tic por la vía real de A2 —obs del diario con su chat E2, ojos
(`oyente2.inyecta`), gemelo E1, `Memoria.observa`, `D.candidatos`, `D.decide`
con `Bloqueos`, con `D.A` apuntando a la v42 y el entorno de la imagen— sobre
la escapada real de `22146038` s10:

| humo | resultado |
|---|---|
| a · dentro de D0 y viendo al hermano | 209 tics: S-COMPANIA 0 y S-SOLEDAD 0 en `noop` |
| b · lejos y sin verlo | **1.101 tics** con S-COMPANIA > 0 en `noop`, igual a la fórmula a la distancia del parte; S-SOLEDAD 0 en todos |
| c · `d` de producción = `d` del banco | 2.849 candidatos, \|Δ\| máx. **2,0·10⁻⁵** |
| d · con `GEMV_FILAS10=0`, `d` = la logueada en el diario A2 | residuo máx. **0,017** en 1 candidato de 25 (F-HERMANO-AMENAZA 0,02, la certificación del agresor del hermano, que depende de memoria acumulada); declarado, tolerancia 0,02 |
| e · el veto de siempre | 273 tics de enfriamiento sin candidatos de movimiento |

Humo de red: 200/200 acciones, 0 errores, `mem.parte` puesto por el cable,
S-COMPANIA en la radiografía. Dentro del build de `Dockerfile.pareja10`, con
custodia md5 de `filas10_P6_10.py`, `arreglos_P6_8b.py` y `policy_pareja10.py`.

---

## 4 · LA SERIE: A3 EN LAS 20 SEMILLAS

**Coste: 1,3384 USD** de los 3 (20 partidas, todas con coste facturado; 40
diarios). Política `gemv-p6-A3-compania:v1` (`160a8f00…`), imagen
`gemv-anima:pareja10`, `GEMV_OJOS=1`, `GEMV_COMPANIA_TECHO=0.32`. **Control: A0
de P6-6 y A2 de P6-8**, ya jugados y no repetidos: mismo punto de partida,
mundo, liga, roster y semillas; distinto día. Los 40 arranques registran
`filas10: True`.

### 4.1 · El sello, predicción a predicción

| # | sellado | salió | veredicto |
|---|---|---|---|
| 1 | dentro de D0, S-COMPANIA = 0 en mi casilla el 100 %; ganador con la fila > 0 ≤ 4 % | **0 de 446.323** tics dentro de D0 con la fila > 0 en mi casilla; ganador con la fila (cruza D0) **86 de 18.595 = 0,46 %** | **acierta** |
| 2 | a ≤ 3 casillas ≥ 60 % · a > 15 ≤ 2 % | **78,88 % · 0,00 %** (A0 79,13 / 0,00; A2 48,64 / 4,06) | **acierta** — emparejado contra A2: +27,5 p.p., A3 mayor en **19/20**, p = 0,000; contra A0: −0,0, 10/20, p = 1,000 |
| 3 | escapadas ≥ 200 tics ≤ 10 | **1** (2.803 tics; A2 30, A0 3) | **acierta** |
| 4 | vida: emparejado contra A0 > −800, y A3 ≥ A2 | **13.082,6** (A0 12.427,9; A2 11.235,2) · contra A0 **+452,0, mayor en 11/20, p = 0,824** · contra A2 +1.668,0, 14/20, p = 0,115 | **acierta** |
| 5 | muertes con el otro vivo y a ≤ D0 de camino ≥ 80 % | **19 de 19 = 100 %** (A0 17/18; A2 14/20) | **acierta** |
| 6 | comida ≥ 2,3 recogidas por vida | **3,95** (A0 3,20; A2 2,52) | **acierta** — no se deja comida: se coge más que en A0 |
| 7 | `ir_pareja` elegido ≥ 5 % (piernas listas, hermano fuera de vista) | **2,88 %** (899 de 31.252; A2 1,98; A0 6,1) | **FALLA.** La fila no hace ganar a `ir_pareja`: hace que ganen candidatos que acercan (el banco ya lo decía: 34 % `ir_pareja`, 83 % «algo que acerca»), y los tics fuera de vista bajan de 155.995 a **88.226** |
| 8 | coste ≤ 1,5 | **1,3384** | acierta |

**7 aciertos, 1 fallo.** El fallo es de qué gana, no de adónde va.

### 4.2 · A0 / A2 / A3, lo que pedías medir

| medida | A0 | A2 | **A3** |
|---|---:|---:|---:|
| distancia: a ≤ 3 / ≤ 8 / > 15 casillas | 79,1 / 96,9 / 0,0 % | 48,6 / 77,2 / 4,1 % | **78,9 / 96,3 / 0,0 %** |
| mediana de las medianas de distancia por semilla | 2 | 4 | **1** |
| escapadas > 8 casillas · de ≥ 200 tics · tics | 481 · 3 · 7.195 | 466 · 30 · 45.483 | **312 · 1 · 8.724** |
| hermano vivo y fuera de la vista | 14,1 % | 36,3 % | **17,5 %** |
| vida media de la pareja | 12.427,9 | 11.235,2 | **13.082,6** |
| mueren / sobreviven | 32 / 8 | 37 / 3 | **30 / 10** |
| …anillo · rival · no consta | 20 · 11 · 1 | 19 · 14 · 4 | **19 · 9 · 2** |
| muerte por rival: tic mediana · dist. al hermano | 10.859 · 1 | 9.927 · 5,5 | **14.598 · 1** |
| muerte por anillo con el hermano vivo: dist. | 2,5 | 5,0 | **1,5** |
| muertes con el otro vivo y a ≤ D0 de camino | 17/18 | 14/20 | **19/19** |
| los dos vivos al cierre | 18/20 | 18/20 | **18/20** |
| sobrevive el otro tras el primero (mediana) | 912 | 1.017 | **425** |
| tics `coger` + `inventory_full` | 6.254 | 0 | **0** |
| \|disc\| S-8 por decisión | 0,0585 | 0,0449 | **0,0391** |
| golpes: anillo · rival con arma · **`hand: none`** · no visto | 380 · 155 · 103 · 0 | 561 · 185 · 70 · 0 | **457 · 107 · 166 · 0** |
| muertes por rival con arma · con `hand: none` | 9 · 2 | 11 · 3 | **3 · 6** |
| don: episodios · reabsorbidos · efectivos · recogidos · usados | 67 · 1 · 66 · 17 · 16 | 39 · 3 · 36 · 10 · 9 | **90 · 29 · 61 · 16 · 13** |
| comida recogida por vida | 3,20 | 2,52 | **3,95** |
| F-HERMANO-AMENAZA: tics · solo por contado | 29.085 · 0 | 63.948 · 24.555 | **102.856 · 24.622** |

### 4.3 · Lo que dice

1. **La fila junta a la pareja y la deja junta.** A ≤ 3 casillas, de 48,6 % a
   **78,9 %** (mayor en 19 de 20 semillas): el nivel de A0, que no tenía ojos
   ni escapadas. Una sola escapada larga en 40 vidas (A2: 30). Y **todas** las
   muertes con el otro vivo ocurren con el otro a ≤ D0 de camino.
2. **Y viven más**: 13.082 de media, +1.668 emparejado sobre A2 (14/20) y
   **+452 sobre A0 (11/20)** — la primera serie del seis que no queda por
   debajo del cuerpo sin ojos. Nada establecido con 20 semillas (p = 0,824
   contra A0), pero el signo, por fin, es el bueno. 10 supervivientes de 40
   (A0 8, A2 3).
3. **No se paga en comida**: 3,95 recogidas por vida, más que A0. El banco
   decía 2,2 % de decisiones cambiadas con comida cerca; en campo, coger más
   sale de estar juntos donde está el botín.
4. **El coste está en otro sitio, y hay que decirlo:** los golpes de rivales
   con la mano vacía **suben a 166** (A0 103, A2 70) y matan a **6** (2 y 3):
   juntos, los dos se quedan al lado del mismo rival de `hand: none` al que
   la tabla no teme (P6-7 § 3b). Y el don se **reabsorbe 29 veces de 90**: no
   es el bucle (0 tics de mochila, 90 intentos = 90 episodios), es que el
   plazo N (d·11+268) vence con el que dio todavía al lado del regalo, y se lo
   vuelve a quedar. Son las dos cegueras del cinco, más visibles porque ahora
   están juntos.
5. **S-8 de los contados sigue pesando en la vuelta (+0,22 con rival contado,
   n = 926)** y ya no importa: la fila lo compensa. `ir_pareja` gana solo el
   2,88 %; ganan los pasos que acercan.

### 4.4 · Los archivos nuevos, con su md5

| archivo | md5 |
|---|---|
| `cantera/paper6/Dockerfile.pareja10` | `e891e9e09457bb604a276662c580e2e6` |
| `cantera/paper6/P6_10_banco.json` | `6988faea6e4792abdeb7af780f004619` |
| `cantera/paper6/P6_10_base.json` | `a4f120fcfd6430c22e8004effecf38aa` |
| `cantera/paper6/P6_10_base2.json` | `a9e7e73f233fa723e5afab2cdcd66d3c` |
| `cantera/paper6/P6_10_brazos.json` | `28fe5380563b7998ecd0d5997cc589e9` |
| `cantera/paper6/P6_10_don.json` | `d673d37d6fb8dd691c0ff2a97114c9ae` |
| `cantera/paper6/P6_10_fila.json` | `6d2fdb8105eb9e04b3ee8dda0db7837c` |
| `cantera/paper6/P6_10_golpes.json` | `c410711e3975a7bdb573b8357eb6bfff` |
| `cantera/paper6/P6_10_largas_A3.json` | `042971675c21db90db7fa90f0b1684e1` |
| `cantera/paper6/P6_10_lleno.json` | `97f15f06d2aaa92307a3ce354c32691b` |
| `cantera/paper6/P6_10_medidas.json` | `6be0ab6de6e99d798444da7431b0ade1` |
| `cantera/paper6/P6_10_p67.json` | `13337fc0a8afb8195b649168755c9655` |
| `cantera/paper6/P6_10_pareja.json` | `8742821e7a6f909ce34bb224833eba92` |
| `cantera/paper6/P6_10_separa.json` | `b3615622b3680bd60bf118fdec4de174` |
| `cantera/paper6/P6_10_vuelta2.json` | `2b545a88b395c5977395f06118fc0117` |
| `cantera/paper6/SELLO_P6_10.md` | `32e056efdd94be9d69a8a65b6200b595` |
| `cantera/paper6/banco_P6_10.py` | `c3fc419165a80c52e08710899731dbb3` |
| `cantera/paper6/filas10_P6_10.py` | `af4617ad93a27838376df17d0c78b65c` |
| `cantera/paper6/humo_P6_10.py` | `58e30799f4e5decc64f1cb96713d7fdf` |
| `cantera/paper6/humo_red_P6_10.py` | `e056bbf0467738f48ffd9781c74a137a` |
| `cantera/paper6/lanza_P6_10.py` | `c7bfdb7c987f64f2010ced085a144dd5` |
| `cantera/paper6/mide_P6_10.py` | `d65baa28a473db176a08644c08235e76` |
| `cantera/paper6/mide_base2_P6_10.py` | `2016f4a4755666f157f48e173e4b436b` |
| `cantera/paper6/mide_base_P6_10.py` | `410ec2677c61c245b7328179c76adabd` |
| `cantera/paper6/mide_don_P6_10.py` | `11ca97e8f2366ed52cd7df895f6985d9` |
| `cantera/paper6/mide_fila_P6_10.py` | `da6b1d33b399ab55f3971cd9e2bfce3b` |
| `cantera/paper6/mide_golpes_P6_10.py` | `ff0bf5cad0300120ca043c9079826d15` |
| `cantera/paper6/mide_largas_P6_10.py` | `1a6f6c5616f4911faa52969471b928dd` |
| `cantera/paper6/mide_lleno_P6_10.py` | `7b3aca26d3a11e9551b145decd45a564` |
| `cantera/paper6/mide_muertes_P6_10.py` | `25c3608f59063e54aa1ed307037eab78` |
| `cantera/paper6/mide_pareja_P6_10.py` | `07928d47158c98022c00620b790a506b` |
| `cantera/paper6/mide_separa_P6_10.py` | `8ed4b3c49d08937d02f1959ea205b344` |
| `cantera/paper6/mide_vuelta2_P6_10.py` | `a376ccfdeaa4f402dd59b7279c2af17a` |
| `cantera/paper6/policy_pareja10.py` | `f3b3292887b05c408c92c00f7595f521` |
| `cantera/paper6/arreglos_P6_8b.py` | `5028b54d4afd8c7c82bc8e5e3a94a01e` |
| `cantera/paper6/humo_P6_8b.py` | `9efcb3d8fe68eaa6fe6edaef7fac5262` |

Más los 20 `P610_t*_A3_<semilla>.json`, los 2 `P610_t*_peticiones.json` y los
40 diarios en `paintball/runs/P610_*/`. `policy_pareja.py`, `arreglos_P6_6.py`,
`policy_pareja6.py` y los archivos de P6-8 no se tocaron.

*Ningún md5 de esta tabla se escribió antes de calcularlo.*

## CONTROL FINAL

| | |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` — intacto |
| archivos de `CONGELADO.md` | 202 comprobados, 0 alterados |
| coste | **1,3384 USD** de 3 |
| patrones de clave en lo nuevo | 1 aviso, falso: la expresión regular de la custodia en `Dockerfile.pareja10` |
| subido, empujado o borrado en git | nada (la política A3 se subió a la plataforma, como pide el encargo) |
