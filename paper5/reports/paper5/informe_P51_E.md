# P5-1 fase E — La fórmula, la corrección y quién pega

En seco, coste cero, solo lectura. Nada se ha lanzado.

**Lo primero es una corrección.** En la fase D escribí que «en once vidas W no
llegó a tres ni una sola vez» y de ahí saqué que la calma literal era
«aritméticamente imposible». **Eso era falso**, y lo era porque generalicé de
once vidas a todas. Sobre los **260 diarios de S-2**, W llega a 3 en **7.960
instantes de 640.380**, en **10 diarios**. El máximo visto es **3,525**. Lo que
sí se sostiene, con la cifra correcta, es que es **rarísimo**: el **1,24 %** de
los instantes y el **3,8 %** de las vidas.

---

## E1 · La fórmula exacta de W

`paintball/alma/appraisal_zs_v42_exp.py`, función `riqueza_W`, **líneas
717-782**. Cinco sumandos:

| sumando | qué cuenta | cuánto vale | línea |
|---|---|---|---|
| **arma** | **solo lo que va EN LA MANO**, y solo si es `ikMelee`, `ikRanged` o `ikThrown` | `min(1, daño/dmg_ref)` escalado: melé por `durabilidad/durabilidad_máx`; a distancia por `munición/8` | 729-747 |
| **botiquín** | un `first_aid` en la mochila | **1,0** o 0 | 750 |
| **raciones** | la primera vale 1; la segunda **0,3 y solo con mochila** | hasta **1,3** | 753-761 |
| **gear menor** | camuflaje puesto **+** red (en mano o mochila) | 0,25 cada uno, hasta **0,5** | 764-770 |
| **mochila** | llevarla puesta **y que quede apetito por saciar** | **0,5** o 0 | 776 |

Constantes, todas declaradas en el módulo: `RACION_2A = 0.3` (:411),
`MOCHILA_W = 0.5` (:412), `GEAR_MENOR_W = 0.25` (:413), `AMMO_REF = 8.0` (:414).

**El 3 de la carencia** sale de `W_TARGET = 3.0`, **línea 126**, con el
comentario del autor: *«[Manel] arma + botiquín + ración»*. La fila es

```
appraisal_zs_v42_exp.py:1076
    F["R-CARENCIA"] = max(0.0, (W_TARGET - W) / W_TARGET)
```

O sea: el 3 **no es un máximo, es una diana**: son las tres cosas que el cuerpo
considera «ir equipado», una unidad cada una. El `max(0, ·)` satura: con W ≥ 3 la
carencia vale 0 y llevar más no da nada.

**Estar armado es tener el arma en la mano.** Un arma en la mochila no cuenta
(comentario de :724-728: el mundo ataca con `a.hand` y nada más).

### El máximo que el inventario permite

Reglas del mundo (README de zero-sum, línea 51): mano 1 hueco, cuerpo 1 hueco,
mochila **2 huecos, o 4 si llevas la mochila puesta** («backpack (2 -> 4 pack
slots)»). El cuerpo lleva mochila **o** camuflaje, no los dos.

Probadas las **486** combinaciones que esas reglas admiten, llamando a
`riqueza_W` del propio módulo (`cantera/paper5/E1_maxW.py`):

| | W | cuerpo | mano | mochila | desglose |
|---|---|---|---|---|---|
| **máximo** | **4,025** | mochila | espada, durabilidad 39 de 40 | botiquín + 2 raciones + red | arma 0,975 · botiquín 1,0 · raciones 1,3 · gear 0,25 · mochila 0,5 |
| con espada **perfecta** | **3,550** | mochila | espada, durabilidad 40 de 40 | lo mismo | arma **1,0** · botiquín 1,0 · raciones 1,3 · gear 0,25 · **mochila 0,0** |

**Y aquí hay una rareza de la fórmula que conviene mirar.** La mochila solo
cuenta como riqueza **si queda apetito por saciar** (`:776`, lectura declarada
como `[impl]` y marcada como vetable en el propio código). Con el arma perfecta
no queda apetito, la mochila deja de valer 0,5 y **el total BAJA de 4,025 a
3,550**. Una espada intacta vale menos W que una con un rasguño. Es una
no-monotonía real de la tabla, no del mundo.

El catálogo del mundo, leído del diario: espada daño 18 durabilidad 40, lanza 12
/ 40, arco 14, cuchillos 8, cerbatana 4, red 0. `dmg_ref` = 18, así que **solo la
espada llega a `arma = 1`**.

---

## E2 · Conciliación con el traspaso del cuatro

### La corrección, con las cifras

Sobre los **260 diarios de S-2**, **640.380 instantes** con radiografía:

| umbral | instantes | % de los instantes | diarios | % de los 260 |
|---|---|---|---|---|
| **W ≥ 3,0** | **7.960** | **1,243 %** | **10** | 3,8 % |
| W ≥ 2,7 | 17.310 | 2,703 % | 13 | 5,0 % |
| W ≥ 2,25 | 65.857 | 10,284 % | 45 | 17,3 % |
| W ≥ 2,0 | 104.536 | 16,324 % | 84 | 32,3 % |

**«No llega a 3 nunca» es falso. Lo correcto es «casi nunca, y casi siempre la
misma criatura»:** 7.960 instantes de 640.380, concentrados en **10 vidas de
260**.

Lo que sí sigue en pie de la fase D, y ahora con su cifra buena: en las **once
vidas que allí miré** —las seis del mundo lento y cinco de S-2— el máximo fue
2,25. No fue un error de medida: fue una muestra de once que no contenía ninguno
de los diez diarios raros. **La conclusión general que saqué de ella no estaba
justificada.**

### Con qué objetos

| umbral | mano | cuerpo | mochila |
|---|---|---|---|
| **W ≥ 3** | **espada 7.919** · lanza 41 | **camuflaje 7.418** · mochila 542 | **botiquín + raciones 7.791** · el resto, migajas |
| W ≥ 2,7 | espada 16.246 · cuchillos 657 · nada 366 | camuflaje 7.957 · nada 6.399 · mochila 2.954 | botiquín + raciones 14.733 · botiquín + red 1.389 |
| W ≥ 2,25 | espada 45.849 · red 9.313 · arco 4.652 | camuflaje 32.422 · nada 20.649 · mochila 12.786 | botiquín + raciones 29.767 · botiquín + cuchillos 6.255 |

**El retrato del W alto es siempre el mismo: espada en la mano, camuflaje puesto,
botiquín y raciones en la mochila.** Es la única combinación que aparece en
masa por encima de 3.

**La W máxima de toda la serie, 3,525**, es otra cosa: tic 1.643 del diario
`ereq_f3a6bbfb-…-policy_agent_10`, con **espada de durabilidad 29**, **mochila**
puesta y `[botiquín, cuchillos ×6, raciones ×2]` dentro. Su desglose es
0,725 + 1,0 + 1,3 + 0 + 0,5 = 3,525: justo el caso de la no-monotonía, donde la
espada gastada **deja sitio** a los 0,5 de la mochila.

### El 2.014 del paper cuatro, reconciliado exactamente

El traspaso **no contaba instantes con W ≥ 3**. `manual_del_mundo.md:594-596`
cuenta instantes con **tres condiciones a la vez**: `R-CARENCIA = 0` (o sea
W ≥ 3), `R-ACOPIO = 0` y **vida al máximo**. Reproducido:

| condición | instantes |
|---|---|
| W ≥ 3 | **7.960** |
| `R-CARENCIA = 0` | **7.960** (idéntico, como manda la fórmula) |
| W ≥ 3 **y** acopio = 0 | 5.199 |
| W ≥ 3 **y** vida 100 | 4.679 |
| **las tres a la vez** | **2.014** |

**Cuadra al instante.** Las dos cifras eran correctas y medían cosas distintas:
7.960 es «va equipado», 2.014 es «va equipado, lleva venda y está entero».

### Qué queda de la conclusión de la fase D

La cadena de la fase D era: W nunca llega a 3 → la carencia no baja de 0,25 → la
calma literal es imposible. **El primer eslabón se rompe**, así que hay que
rehacer el argumento con la cifra buena:

- La carencia vale 0 en **7.960 de 640.380 instantes**, el **1,24 %**.
- Para la calma literal hace falta que **todas** las filas estén por debajo de
  0,1, no solo la carencia. En P5-1 C la calma literal salió **0 de 37.750** en el
  mundo lento, y en el paper cuatro **0 de 640.380** en S-2.

O sea: la carencia **sí** se apaga de vez en cuando, y aun así **no hubo ni un
instante de calma**. El cuello de botella no era solo la carencia: cuando ella
calla, siguen encendidas la exposición, el alcance, el daño o lo social. **La
conclusión de P5-1 C sigue en pie; el argumento con el que la apuntalé en D, no.**

---

## E3 · Quién nos pegó y quién nos mató, sobre S-2 y S-3 enteros

Sobre **434 diarios** (260 de S-2 y 174 de S-3), con los participantes leídos de
la plataforma episodio a episodio.

### Golpes recibidos antes del tic 2.000

| política rival | golpes |
|---|---|
| **Zero Sum Baseline** | **2.877** |
| zero-sum-example | 443 |
| ryanschiller-zero-sum-player-v1 | 292 |
| skourehjan-zero-sum-scripted-v1 | 100 |
| sivanlevy-zs-courier | 72 |
| zs-patient | 61 |
| aaron-zs-fable | 49 |
| *veneno* (no es una política) | 22 |
| zero-sum-scavenger | 10 |
| relh-zero-sum | 2 |
| **total** | **3.928** |

### Muertes nuestras antes del tic 2.000

De los 434 asientos-partida, **211 murieron antes del tic 2.000** y 223 pasaron
de ahí.

| quién la hizo | muertes |
|---|---|
| **zero-sum-example** | **71** |
| Zero Sum Baseline | 61 |
| ryanschiller-zero-sum-player-v1 | 42 |
| zs-patient | 11 |
| sivanlevy-zs-courier | 9 |
| **no consta** | **8** |
| skourehjan-zero-sum-scripted-v1 | 5 |
| aaron-zs-fable | 2 |
| zero-sum-scavenger | 2 |
| **total** | **211** |

**Tres políticas de catorce hacen el 92 % de las muertes tempranas** y el 92 % de
los golpes. `Zero Sum Baseline` pega mucho más que nadie —2.877 golpes, tres de
cada cuatro— pero mata menos que `zero-sum-example`, que con 443 golpes se lleva
71 muertes: pega poco y remata.

**Cómo se atribuye la muerte, declarado.** El diario **no guarda el golpe que
mata**: el cuerpo deja de recibir observaciones al morir. Se atribuye al último
golpe **registrado** en los 48 instantes anteriores al `match_ticks` del propio
diario. Cuando no hay ninguno, va a **«no consta»**, y son **8 de 211**.

**Esto corrige también a D1**, donde con solo seis asientos del mundo lento dije
que «casi toda la violencia temprana viene de `zero-sum-example`». Sobre 434
asientos, quien más pega con diferencia es **`Zero Sum Baseline`**; en las tres
partidas del mundo lento no apareció porque el asiento lo fija el roster.

---

## Lo que esta fase deja dicho

1. **El 3 de la carencia es una diana, no un techo.** El inventario permite
   llegar a **4,025**, y el cuerpo llegó a **3,525**.
2. **La tabla tiene una no-monotonía declarada:** con el arma perfecta la mochila
   deja de contar y el total baja. Está marcada como `[impl]` vetable en el
   propio código (`:773-776`), y conviene decidir si se queda.
3. **W ≥ 3 ocurre, y es rarísimo:** 1,24 % de los instantes, 10 vidas de 260,
   siempre con espada, camuflaje, botiquín y raciones.
4. **El 2.014 del cuatro y los 7.960 de aquí son compatibles**: medían cosas
   distintas, y la cuenta de las tres condiciones da 2.014 clavado.
5. **Mi conclusión de la fase D estaba mal apuntalada.** La calma literal sigue
   siendo cero en las dos series, pero no porque la carencia no pueda apagarse:
   se apaga, y aun así no hay calma.
6. **La violencia temprana se reparte peor de lo que dije:** tres políticas hacen
   el 92 %, y la que más pega no es la que más mata.

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Ficheros: `cantera/paper5/mide_W.py`, `E2_concilia.py`, `E1_maxW.py`,
`E3_participantes.py`, `E3_golpes.py`, `E2_W.json`, `E1_maxW.json`,
`E3_golpes.json`, `E3_participantes.json`.
