# P5-3A — La proyección de necesidades

En seco, coste cero. Nada se ha lanzado. **La proyección no se enciende dentro
de ninguna decisión**: vive en `cantera/paper5/proyeccion.py`, fuera del
decisor, y aquí solo se mide.

**El titular tiene dos partes y las dos van contra lo sellado.** Las reglas del
mundo se proyectan **exactas** —error cero en mediana y en p90 cuando no hay
daño ajeno—, así que la maquinaria funciona. Pero **la proyección con intención
no mejora a la foto congelada**: la empeora un poco. La razón es que en el 89 %
de las ventanas de cien instantes **no cambia nada**, y «no cambia nada» es
justo lo que la foto de hoy ya supone.

---

## El arnés, con la proyección apagada

`proyeccion.py` no toca al decisor ni a la tabla: lo único que importa de ellos
es `riqueza_W`. Comprobado en vivo, con el módulo importado:

```
[1/5]    275/275     = 100.00 %
[2/5]  5,555/5,555   = 100.00 %
[3/5]  8,603/8,603   = 100.00 %
[5/5] 11,804/11,804  = 100.00 %

REPRODUCCION CON LA PROYECCION IMPORTADA: 11,804/11,804 = 100.00 %
```

**El 100,00 % sobre 11.804 tics** de los cinco primeros diarios de la selección,
con `proyeccion.py` importado. La corrida completa de los 40 diarios ya quedó en
100,00 % sobre 112.865 tics en P5-2c; aquí solo se comprueba que importar el
módulo nuevo no mueve nada.

---

## A0 · El H del cuerpo contra el tiempo real de llegada

**El H está en `decisor_zs.py:610-617`**, función `mirada`:

```python
def mirada(mundo, tick) -> int:
    tope = int(A.ANT_HORIZONTE_S * mundo.tick_rate)
    prox = A._proximo_encogimiento(mundo, tick)
    if prox is None:
        return H_MIRADA_MIN
    return max(H_MIRADA_MIN, min(tope, prox[0] - tick))
```

con suelo `H_MIRADA_MIN = 48` (`decisor_zs.py:47`) y techo
`ANT_HORIZONTE_S = 20.0` segundos (`appraisal_zs_v42_exp.py:124`), o sea
20 × 24 = **480 tics**.

**Lo que sale en la práctica:**

| tanda | H = 480 | H = 48 | otros |
|---|---|---|---|
| S-2 brazo A (40 diarios) | **70.611** | 4.037 | 184 |
| mundo lento (6 asientos) | **30.744** | 672 | 30 |

**Y lo que tarda de verdad en llegar un destino típico:**

| | S-2 | mundo lento |
|---|---|---|
| pasos de los candidatos `ir_*`, mediana | **3** | 4 |
| pasos del candidato **ganador**, mediana | **3** | 5 |
| tics entre paso y paso, medidos | **11** (n = 8.553) | **11** (n = 3.364) |
| **tiempo real de llegada, mediana** | **33 tics** | **55 tics** |

Los 11 tics por casilla confirman la regla del manual (§4: `16 − velocidad`, y
con esta velocidad son 11).

**No coinciden, y no coinciden por mucho.** El cuerpo mira **480** instantes por
delante para juzgar una casilla a la que llega en **33**. Es **14,5 veces** el
tiempo real de llegada en S-2 y **8,7 veces** en el mundo lento.

---

## A1 · Las reglas que sí se pueden proyectar

Escritas en `cantera/paper5/proyeccion.py`, cada una con su fuente.

| qué | regla | fuente |
|---|---|---|
| **andar** | `16 − velocidad` = **11 tics** por casilla; tras el paso se ven bajar 10 | manual §4; README:36; sim.nim:147; medido, máximo `move_ready_in` = 10 en 191.531 jugadas |
| **pegar** | enfriamiento propio, del catálogo del arma; no estorba al de andar | manual §4; sim.nim:934, :618, :898 |
| **los dos** | bajan de uno en uno por tic, y no bajan de cero | PROTO:54 |
| **anillo** | la casilla fuera del radio quema a `damage_per_s / tick_rate` por tic; el radio y el dps salen de `mundo.anillo_en(tick)` | manual §12 |
| **botiquín** | **+50** de vida, tarda **48** tics; un golpe lo cancela y el botiquín no se pierde | manual §6; catálogo `heal` 50 / `use_ticks` 48; sim.nim:866-868 |
| **ración** | **+15** de vida, tarda **24** tics | manual §6; catálogo |
| **canal abierto** | se siembra de `effects`, que el mundo ya publica: `{"id":"channeling","item":"first_aid","done_tick":4945}` | el propio diario |
| **W** | se recalcula con `riqueza_W` del módulo, sin copiar ni un peso; coger mete, consumir saca | `appraisal_zs_v42_exp.py:717-782` |
| **huecos** | 2, o **4** con la mochila puesta | README:51 |
| vida | recortada a [0, 100] | — |

### Lo que NO se proyecta, dicho

- **el daño de los rivales y sus movimientos**;
- **el botín que aparece**, o que otro se lleva;
- **el veneno de los dardos** (2 puntos por segundo, duración según la
  inteligencia del envenenado; manual §5, README:49-51): ni el momento ni la
  duración se saben en `t`;
- **el gasto de munición al disparar**, que cambia el peso del arma a distancia
  porque `riqueza_W` la escala por `munición / 8`;
- la cancelación de la cura por un golpe ajeno, que es un caso del primero.

### La interfaz

```python
proyectar(estado_t, plan, K, mundo, suelo=None, camino=None) -> estado_t+K
congelada(estado_t, mundo, K) -> estado_t+K      # la foto de hoy
```

`plan` es una lista de acciones por tic (`"paso"`, `"coger"`, `"usar_<id>"`,
`"esperar"`) **o** un diccionario de intención
`{"destino": (x,y), "coger": bool, "usar": "<id>"}`. `camino` deja seguir las
posiciones reales cuando se quiere aislar el error de las reglas.

---

## A2 · El error de la foto de hoy

En cada tic en que ganó un candidato `ir_*` con detalle completo en el diario.

### S-2 brazo A

| K | n | W mediana | W p90 | vida mediana | vida p90 |
|---|---|---|---|---|---|
| 25 | 205 | 0,0 | 0,0 | 0,0 | **6,0** |
| 50 | 204 | 0,0 | 0,0 | 0,0 | **12,0** |
| 100 | 197 | 0,0 | 0,0167 | 0,0 | **13,0** |
| **H (mediana 480)** | 182 | 0,0 | **0,778** | 0,0 | **17,0** |

### Mundo lento

| K | n | W mediana | W p90 | vida mediana | vida p90 |
|---|---|---|---|---|---|
| 25 / 50 / 100 | 91 / 91 / 89 | 0,0 | **0,0** | 0,0 | **0,0** |
| H (mediana 480) | 84 | 0,0 | 0,0 | 0,0 | 0,0 |

### Cuántas veces cambia algo

| K | S-2: W cambia | vida cambia | de n |
|---|---|---|---|
| 25 | 15 | 27 | 205 |
| 50 | 16 | 30 | 204 |
| **100** | **21 (10,7 %)** | **35 (17,8 %)** | **197** |

**Esta es la clave de todo lo que viene.** En nueve de cada diez ventanas de cien
instantes **W no cambia**, y en ocho de cada diez **la vida tampoco**. La foto
congelada acierta en la mediana **porque casi nunca pasa nada**. Su error solo
aparece en la cola, y en el horizonte que el cuerpo usa de verdad (H = 480) esa
cola es grande: p90 de **0,78 en W** y **17 puntos de vida**.

**Un aviso sobre el mundo lento:** sus 89 ventanas dan cero en todo. No es que la
proyección sea perfecta allí: es que en esas ventanas **no pasó nada**, ni bueno
ni malo. Con seis asientos y 89 ventanas no da para más.

---

## A3 · Proyección con camino real: ¿son correctas las reglas?

Dándole a `proyectar()` las acciones **y las posiciones** que el cuerpo hizo de
verdad.

| K = 100, S-2 | n | W mediana | W p90 | vida mediana | vida p90 |
|---|---|---|---|---|---|
| **sin daño ajeno** (ni rival ni veneno) | **180** | **0,0** | **0,0** | **0,0** | **0,0** |
| con daño ajeno | 17 | 0,0 | 0,025 | 8,0 | 28,0 |

**El error residual de las reglas es CERO**, en mediana y en p90, sobre 180
ventanas limpias. Las reglas están bien.

### Pero costó arreglar dos, y las dos eran mías

R1b decía «si no es cero, las reglas están mal y se arreglan antes de seguir».
Lo fueron:

1. **El nombre de la cura.** El decisor llama al candidato `usar_botiquin`
   (`decisor_zs.py:491`), en llano, mientras que el objeto de la mochila se llama
   `first_aid`. Mi proyección buscaba `first_aid` y **se perdía todas las
   curas**. Ejemplo: diario `ereq_051a3cdd-…-a11`, tic 4.897, elige
   `usar_botiquin`; el canal se abre y a los 48 tics la vida sube de 62 a 100.
   La proyección la dejaba en 58,25, un error de **41,75 puntos**.
2. **El canal ya abierto.** Si en `t` había una cura en curso, se perdía. El
   mundo la publica en `effects` con su `done_tick`; ahora se siembra de ahí.

Con las dos arregladas, el p90 pasa de 1,0 a **0,0**.

**Lo que queda fuera, y se declara:** en las ventanas **con** daño ajeno el error
de vida sube a 8,0 de mediana y 28 en el p90. Eso no es error de las reglas: es
exactamente lo que las reglas dicen que no saben.

---

## A4 · Proyección con intención: ¿sirve?

Dándole solo lo que el cuerpo sabía en `t`: el destino ganador, y «coger» si ese
destino tenía un objeto a la vista.

| K | | W mediana | W p90 | vida mediana | vida p90 |
|---|---|---|---|---|---|
| 25 | foto | 0,0 | 0,0 | 0,0 | 6,0 |
| 25 | **intención** | 0,0 | 0,0 | 0,0 | **4,67** |
| 50 | foto | 0,0 | 0,0 | 0,0 | 12,0 |
| 50 | **intención** | 0,0 | 0,0 | 0,0 | **6,0** |
| 100 | foto | 0,0 | **0,0167** | 0,0 | **13,0** |
| 100 | **intención** | 0,0 | **0,0278** | 0,0 | **15,0** |

**A 25 y a 50 instantes la intención ayuda**: baja el p90 de vida de 6,0 a 4,67 y
de 12,0 a 6,0, o sea a la mitad. **A 100 instantes deja de ayudar y estorba**:
sube el p90 de vida de 13 a 15 y el de W de 0,0167 a 0,0278.

**La explicación está en A2.** La proyección con intención supone que el cuerpo
irá al destino y cogerá lo que hay. A cien instantes, el cuerpo ya **cambió de
idea** muchas veces: solo el 10,7 % de las ventanas ven cambiar W. Suponer «va a
hacer lo que dijo» es peor predictor que suponer «no va a pasar nada».

---

## A5 · El techo: lo que no se puede proyectar

Ventanas de K = 100.

### De dónde viene la vida perdida

| | S-2 (197 ventanas) | mundo lento (89 ventanas) |
|---|---|---|
| **de rivales** (no proyectable) | 268,0 puntos = **40,7 %** | 198,0 = **69,5 %** |
| **del anillo** (proyectable) | 390,3 puntos = **59,3 %** | 86,9 = **30,5 %** |
| ventanas **sin ninguna pérdida** | **162 de 197 = 82,2 %** | **84 de 89 = 94,4 %** |

### De dónde viene el cambio de W

| | S-2 | mundo lento |
|---|---|---|
| W no cambia | 176 de 197 | 84 de 89 |
| **coger** | 14 | 3 |
| **consumir** | 7 | 2 |
| morir | 0 | 0 |
| **fracción del cambio que es propio** | **100 %** | **100 %** |

**El techo es distinto en cada mundo, y es un resultado.** En S-2 la mayoría de
la vida que se pierde la quita **el anillo**, que **sí** se proyecta. En el mundo
lento la quitan **los rivales**, que no. Y **todo** el cambio de W es propio en
las dos: coger o consumir, nunca otra cosa.

---

## A6 · La figura

Dos figuras en `cantera/paper5/figE/`: `A6_S2.png` y `A6_lento.png`. PNG a 300
ppp, 17 cm. W y vida reales a lo largo de toda la vida, con **diez decisiones de
andar elegidas al azar** (semilla **20260920**) y, en cada una, la raya de la
foto congelada (gris discontinua) y la de la proyección con intención (acento),
del instante de decidir a cien instantes después.

Lo que se ve, y es el informe entero en una imagen: **las dos rayas casi siempre
se superponen y las dos casi siempre aciertan**, porque la vida es plana durante
tramos larguísimos. Las pocas veces que la realidad se mueve —los escalones de W,
la caída de vida del tic 3.200— **ninguna de las dos lo ve venir**.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **R1** | con intención, el error **mediano** de W y vida a K=100 baja a menos de la mitad del de la foto | A2 y A4, medianas | **la mediana de la foto ya es 0,0** en W y en vida | **no se puede cobrar: el contador no podía bajar**. En el p90, que sí varía, la intención **empeora**: vida 13,0 → 15,0 y W 0,0167 → 0,0278. **FALLA** |
| **R1b** | con camino real y sin daño ajeno: mediana 0, p90 < 0,1 en W y < 3 en vida | A3 | **mediana 0,0 · p90 0,0 en las dos**, n = 180 | **CUMPLE**, tras arreglar las dos reglas que estaban mal, como la propia predicción mandaba |
| **R1c** | en S-2, más de la mitad de la vida perdida viene de rivales | A5 | **40,7 %** (el anillo se lleva el 59,3 %) | **FALLA** |
| **R1c** | en el mundo lento, también | A5 | **69,5 %** | **CUMPLE** |
| **R1c** | el cambio de W es propio en más del 80 % | A5 | **100 %** en las dos tandas | **CUMPLE** |
| **R1d** | el H del cuerpo es **menor** que el tiempo real de llegada | A0 | H = **480** · llegada = **33** (S-2) y **55** (lento) | **FALLA, y al revés**: H es 14,5 veces el tiempo de llegada |

**Los contadores podían variar, comprobado uno a uno.** El de R1 **no**: la
mediana de la foto ya era cero y no hay dónde bajar, y eso es en sí el hallazgo,
así que se reporta el p90, que va de 0,0 a 17,0 según el caso. El de R1b podía
variar y de hecho valía 1,0 antes de arreglar las reglas. El de R1c varía entre
las dos tandas, 40,7 % contra 69,5 %, que es la prueba de que no estaba forzado.
El de R1d tiene dos valores de H en los diarios (480 y 48) y una mediana de
llegada medida sobre 8.553 pasos reales.

---

## Lo que esto deja para la sección 5 del paper

1. **La maquinaria de proyectar funciona**: error cero cuando el mundo no mete
   la mano.
2. **Pero proyectar la intención no paga a cien instantes.** El cuerpo cambia de
   idea más de lo que la intención vale. A 25 y 50 instantes sí paga, y ahí
   **reduce a la mitad** el error de vida.
3. **El desajuste de fondo es el H.** El cuerpo juzga a 480 instantes un destino
   al que llega en 33. Si la proyección se enciende, el primer parámetro que hay
   que mirar no es qué se proyecta, **es cuánto**.
4. **Casi nunca pasa nada.** El 82 % de las ventanas de cien instantes no pierden
   un punto de vida, y el 89 % no cambian W. Cualquier predictor compite contra
   «no va a pasar nada», que es muy difícil de batir.
5. **Lo que se proyectaría con más provecho es el anillo**, que en S-2 se lleva
   el 59,3 % de la vida perdida y es **completamente determinista**.

**PARO AQUÍ.** La proyección no se ha encendido dentro de ninguna decisión.

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1

$ md5 cantera/paper5/proyeccion.py cantera/paper5/mide_P53A.py \
      cantera/paper5/fig_P53A.py
MD5 (cantera/paper5/proyeccion.py)  = 66a895462d1d6ca4f15128fbba5a700c
MD5 (cantera/paper5/mide_P53A.py)   = 8f647959ce1f48419777207a35ae54e7
MD5 (cantera/paper5/fig_P53A.py)    = 768f2093058c56babaa7181a32790bf7
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`. Salidas:
`P53A_S2.json`, `P53A_lento.json`, `P53A_progreso.log`, `P53A_corrida.log`,
`P53A_reproduce.log`, `figE/A6_S2.png`, `figE/A6_lento.png`.
