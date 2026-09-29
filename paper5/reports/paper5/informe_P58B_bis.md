# P5-8B bis — Arreglo, y el humo que no deja construir la imagen

**PARO AQUÍ. No hay imagen nueva y no hay segunda sonda**, porque el humo que
tú mismo especificaste **se cae**, y es la puerta de entrada.

**Y tengo que empezar retirando lo que te dije ayer: mi diagnóstico de la
sonda 1 era incorrecto.**

---

## El titular

**El arreglo está hecho y verificado, y no cambia nada.** Las formas siguen
muriendo a los 25 tics exactos. **La causa que di no era la causa.**

Dije que las formas morían porque `F._d2` se envolvía con el renglón **solo al
nacer** y no en la reevaluación. Hice el arreglo, **comprobé con un registro de
depuración que el envoltorio sí se instala en la reevaluación** (`cam: true` en
cada `_juzga` de reevaluación), y **el resultado es idéntico**: min 25, mediana
25, máx 25.

**Lo que de verdad pasa**, leído de los veredictos:

```
tic 291  id 2  EVALUADA  ventaja +0,07395  margen 0,062  -> ok
tic 291  id 2  ACEPTADA
tic 316  id 2  CAIDA: en la reevaluacion deja de ganar (area)
```

La forma nace con una ventaja de **+0,074** contra un margen de **0,062** —
pasa por **doce milésimas**— y veinticinco tics después ya no llega. Las dos
aceptadas de la escena nacen con **0,0666 y 0,0740**; las tres rechazadas, con
0,00002, 0,0197 y 0,0400. **Todo el mecanismo vive pegado al margen.**

Es coherente con el diseño y por eso no lo toco: el renglón es dolor
proporcional a `(1 − g(d))`, así que **la ventaja de la forma decae a medida que
el cuerpo se acerca a la frontera**. Al primer punto de control ya ha decaído
por debajo del margen. **La puerta está funcionando; lo que no funciona es que
una forma de seis casillas tenga margen para llegar.**

---

## El arreglo, que queda hecho

**La puerta ya juzga y re-juzga con la misma regla.** `F._d2` se envuelve con el
renglón de ignorancia proyectado **dentro de `_juzga`**, que es quien juzga al
nacer y en cada reevaluación.

Dos cosas del arreglo que conviene anotar porque no estaban en el encargo:

1. **Quité el envoltorio de `_cita_curiosidad`.** Con el nuevo en `_juzga`, los
   dos se anidaban y **habrían sumado el renglón dos veces**. Verificado con un
   aserto de que `con_renglon` aparece una sola vez en el fichero.
2. **`_juzga` puede correr en el hilo del consejero**, y envolver un global de
   módulo desde dos sitios a la vez sería la carrera de C1-bis otra vez. Va con
   **candado propio**.
3. **Un respaldo declarado en `con_renglon`:** en la reevaluación el cuerpo ya
   no está sobre el camino original, así que el índice del camino falla; el
   respaldo es la distancia Chebyshev al destino, que **aproxima por debajo** la
   distancia por el mapa. Sin él el renglón no habría entrado — pero, como se ve
   arriba, **con él tampoco cambia el resultado**.

---

## El humo, y por qué no construyo la imagen

```
  (a) APAGADO identico: 200/200 decisiones · 0 registros de curiosidad-forma
  (b) el brazo K vive: 5 nacidas · 2 aceptadas · 2 caidas
      forma 2 -> destino (23, 21): distancia 5 -> 3 en 24 tics
  (c) VETO DURO: sin armado False · con un armado sobre el camino True
  (d) duracion de las formas: min 25 · mediana 25,0 · max 25 (CADA_REEVALUA = 25)
      causas: {'en la reevaluacion deja de g': 2}
      sobreviven a la primera reevaluacion: 0/2

FALLOS:
  · (d) TODAS las formas mueren exactamente a 25 tics
  · (d1) NINGUNA forma sobrevive a su primera reevaluacion
```

**(a), (b) y (c) pasan. (d) se cae, que es exactamente lo que pediste que
hiciera.** Tú lo escribiste así: «el humo se cae si toda forma aceptada muere
exactamente a `CADA_REEVALUA`».

**Por eso no he construido imagen ni he lanzado la segunda sonda.** Construir y
sondar con el humo caído sería gastar para volver a medir lo que el humo ya
dice gratis.

---

## Lo que no sé, marcado como tal

**No sé si el problema es el margen, el decaimiento o el horizonte.** Tengo tres
sospechas y ninguna medida que las separe:

- **El margen.** Es `0,02 + 0,06·(1−C)` y con C = 0,30 vale **0,062**. Las formas
  nacen con 0,067-0,074: **pasan por milésimas**. Con la confianza más alta el
  margen bajaría y sobrevivirían; pero C solo sube si las formas salen bien, y
  no salen bien porque mueren. Es un círculo.
- **El decaimiento.** `(1 − g(d))` con `BOTIN_EXP = 3` cae muy deprisa: a mitad
  de camino de una forma de seis casillas, el alivio que queda es pequeño.
- **El horizonte.** El primer punto de control cae a los 25 tics, y una forma de
  seis casillas debería estar casi terminada; si no lo está, el cuerpo no la
  siguió tan recto como la proyección suponía.

**No sé cuál manda.** Distinguirlas pide medidas que no están en este encargo.

**Y no sé si esto es un defecto o un resultado.** Cabe leerlo como que **la
puerta honesta rechaza la curiosidad en cuanto deja de pagar**, que es lo que
una puerta honesta debe hacer — y entonces el hallazgo sería que *la curiosidad
como forma no sobrevive a su propia regla*. No lo afirmo: es una lectura, y la
mesa tiene que decidir si la serie de cuarenta debe medir eso o si antes hay que
mover algo.

---

## Propuesta, no ejecución

Tres caminos, por orden de lo que yo probaría primero:

1. **Medir el decaimiento antes de tocar nada**: en seco, sobre los mismos
   diarios de P5-8A, la ventaja de la forma en el tic 0 y en el tic 25. Coste
   cero, y separa «el margen» de «el decaimiento».
2. **Alargar el primer punto de control** para formas de curiosidad, de 25 a la
   duración estimada del trayecto. Toca `forma_viva`, que es de la casa.
3. **Bajar el margen solo para estas formas**, que es lo que menos me gusta
   porque cambia la puerta, y la puerta es lo que da valor a todo lo demás.

**No he hecho ninguna.** Decidir cuál es de la mesa.

---

## Custodia

```
                            al empezar                         al acabar
motor/model.py              1e511978c251130e95169ebf8443efa1   idéntico
paintball/alma/decisor_zs.py
                            8fa03547e3228ef9df4aa94c444f9252   idéntico
paintball/alma/appraisal_zs_v42_exp.py
                            98c13d60167c80cc8334c965be75c640   idéntico
```

| fichero | md5 |
|---|---|
| `cantera/paper5/curiosidad_forma.py` | `5687f0f3129970290b7f82088ab2e3de` |
| `paintball/alma/policy_forma.py` | `74c76493123b33518f951624d289903d` |
| `paintball/alma/humo_curforma.py` | `f5b62a212021cc710bc5f25b961ca22e` |

**Gasto: cero.** No se construyó imagen, no se subió política, no se lanzó
ningún episodio. Cola vacía.

**PARO AQUÍ.**
