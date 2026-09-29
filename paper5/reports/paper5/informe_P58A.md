# P5-8A — La curiosidad como forma, en seco

En seco, **coste cero**, nada a la plataforma, ninguna llamada a ningún modelo.

---

## El titular

**Los siete sellos cumplen, y el tercero es el que importa: la puerta cobra la
curiosidad, no la geometría.** De 3.213 formas evaluadas en el mundo lento,
**pasan 1.197 con el renglón en la proyección y solo 86 sin él** — catorce veces
menos. Sin el renglón, ir a la frontera es un viaje que el cuerpo rechaza; con
él, la puerta ancha lo acepta una de cada tres veces.

**Pero hay dos cifras que no permiten cantar victoria**, y van en el titular
porque son las que deciden si esto merece campo:

- **Una de cada cuatro formas que pasan se abandona por peligro** dentro de la
  ventana (23,2 %): aparece un armado que cubre el camino restante.
- **El trayecto mediano son 6 casillas**, dentro del rango sellado pero **en su
  borde inferior**. La frontera no está lejos: está a seis pasos. El diagnóstico
  de la mesa —«la frontera está lejos»— **no se sostiene en este mundo**.

---

## Custodia, al empezar y al acabar

```
motor/model.py                  1e511978c251130e95169ebf8443efa1   (idéntico)
paintball/alma/decisor_zs.py    8fa03547e3228ef9df4aa94c444f9252   (idéntico)
paintball/alma/appraisal_zs_v42_exp.py
                                98c13d60167c80cc8334c965be75c640   (idéntico)
```

**Los tres, byte a byte iguales antes y después.**

### La puerta de entrada

```
PUERTA (curiosidad_forma importado, mecanismo APAGADO): 5.555/5.555 = 100,00 %
```

Todo lo nuevo vive en `cantera/paper5/curiosidad_forma.py`, reutilizando
`forma.py` (la puerta), `proyeccion.py` (el camino) y el BFS de `curiosidad.py`.
**`forma.py` tampoco se toca**: para meter el renglón en la proyección se
**envuelve `F._d2` desde fuera** y se restaura en un `finally`, el mismo patrón
con el que la política viva inyecta `D.candidatos`.

---

## El humo donde vive la regla — y el fallo que encontró

md5 del cuerpo: **`5e6074ee3a55acbd1a9c59ea3d610f0d`**

```
  (1) armado a tiro (alcance 1,0, dist 1) · amenaza 1,0000 · motivo: entorno no seguro
      -> NO se genera. La amenaza pasa el umbral de seguro (0,2).
      -> a la fuerza: tampoco hay frontera fuera de sombra
  (2) frontera SOLO detras del armado (alcance 8,0) · destino None
      -> «sin frontera segura», como debe
      control sin armado: destino (24, 8) a 16 casillas
LOS DOS HUMOS OK
```

**El humo encontró un fallo real antes de medir nada.** La primera versión
comprobaba la sombra **solo en la casilla de destino**, no en el camino: forzando
la generación con un armado pegado al cuerpo, el BFS devolvía una ruta que
pasaba por delante de él. El contador «cero formas que cruzan sombra» es **por
construcción**, y la construcción estaba mal. Corregido: **la sombra corta la
expansión del BFS**, no solo la aceptación del destino.

Sin ese humo, F5 habría salido «cero» por un contador que miraba donde no había
nada que mirar.

---

## Los contadores · mundo lento (20 diarios de A, 40 asientos)

### Consigna 0,5

| | |
|---|---|
| tics vivos | 340.885 |
| **no se dispara** | 180.920 |
| **ventanas seguras con ignorancia sobre consigna** | **159.965 = 46,93 %** |
| se dispara y **no hay frontera segura** | **0 = 0,00 %** |
| **formas generadas** | **159.965 = 100,00 %** |
| puerta evaluada (muestreo) | 3.213 |
| **pasan CON el renglón** | **1.197 = 37,25 %** (área 1.993 · vida 23) |
| **pasan SIN el renglón** | **86 = 2,68 %** (área 3.104 · vida 23) |
| trayecto | **mediana 6** · Q1 4 · Q3 7 · min 2 · max 11 |
| cruza sombra · destino a tiro | **0 · 0** |
| abandonadas por peligro | **278/1.197 = 23,22 %** |
| carencia proyectada NO sube | **1.197/1.197 = 100,00 %** |
| coste de generar | **0,112 ms** mediana (max 0,960) |
| coste de la puerta | 1,2 ms mediana |

### Consigna 0,7

Ventanas **147.241 = 43,19 %**; generadas 100,00 %; pasan **1.110/2.956 =
37,55 %** con el renglón y **86 = 2,91 %** sin él; trayecto mediana **5**;
abandonadas **23,15 %**; carencia no sube **100 %**.

**Subir la consigna de 0,5 a 0,7 casi no cambia nada.** Es coherente con lo que
P5-7A ya midió: **la ignorancia global mediana es 0,73-0,78 y apenas se mueve en
toda la vida**, así que las dos consignas caen por debajo de ella casi siempre.
La consigna, en este mundo, **no es un mando: es un interruptor que está casi
siempre encendido**.

---

## De contraste · S-2 (40 diarios de A)

| | consigna 0,5 | consigna 0,7 |
|---|---|---|
| ventanas | 36.766 = **32,58 %** | 24.181 = 21,42 % |
| pasan CON el renglón | 185/701 = **26,39 %** | 139/450 = 30,89 % |
| pasan SIN el renglón | 33 = 4,71 % | 33 = 7,33 % |
| trayecto mediano | 6 | 6 |
| abandonadas por peligro | **27,57 %** | 28,06 % |

**S-2 dispara menos y abandona más**, que es lo que cabe esperar de un mundo con
cazadores. El efecto del renglón en la puerta se mantiene (26-31 % contra 5-7 %).

---

## Cotejo de las predicciones selladas

| | sello | contador | veredicto |
|---|---|---|---|
| **F1** | genera en ≥50 % de las ventanas | **100,00 %** | **CUMPLE** |
| **F2** | pasa la puerta ≥30 % de las generadas | **37,25 %** | **CUMPLE** |
| **F3** | sin el renglón pasan <la mitad | **86 contra 1.197** (7,2 %) | **CUMPLE** |
| **F4** | trayecto mediano 5-20 casillas | **6** | **CUMPLE** |
| **F5** | cero sombras cruzadas, cero destinos a tiro | **0 · 0** | **CUMPLE** |
| **F6** | la carencia no sube en ≥90 % | **100,00 %** | **CUMPLE** |
| **F7** | generar <10 ms de mediana | **0,112 ms** | **CUMPLE** |

**F1 cumple de una forma que conviene leer despacio: el 100 %.** Una vez que hay
ventana segura con ignorancia sobre consigna, **siempre** hay frontera fuera de
sombra —«sin frontera segura» sale **cero** en los dos mundos y las dos
consignas—. El filtro de la sombra, que era la salvaguarda, **nunca llega a
morder en estos datos**. No está probado que funcione en el campo: está probado
que **aquí no hace falta**.

**F3 es el resultado de la sección.** El cuerpo, por sí solo, rechaza el viaje a
la frontera: sin el renglón pasa el 2,68 %. Con la curiosidad en la proyección
pasa el 37,25 %. **La puerta no acepta la geometría del camino; acepta el alivio
de ignorancia que el camino promete.**

---

## Lo que no sé, marcado como tal

**Las casillas nuevas no son un resultado, y el encargo ya lo decía.** Las formas
que pasan prometen **75 casillas nuevas de mediana**; el cuerpo real, en la misma
ventana de 100 tics, vio **0** (mediana; 3 en S-2 con consigna 0,7). **Esa
comparación no dice que la forma habría visto 75 veces más**: dice que la forma
apuntaba a terreno virgen y que el cuerpo, que no la siguió, se quedó donde
estaba. **Solo el campo puede medir esto**, porque en seco el diario nunca
recorre el camino de la forma. Va informado y **no sellado**, como se pidió.

**El 23 % de abandono no sé si es mucho o poco.** No hay con qué compararlo: las
formas del consejero de P5-6C no tenían este contador. Es un número nuevo sin
vara.

**El muestreo de la puerta es mío, no del encargo, y lo declaro.** El disparo se
mide en **todos** los tics vivos (censo); la puerta, que cuesta ~1,2 ms por
evaluación sobre ~20 candidatos, se evalúa **cada 50 tics desde el 300** —las
constantes del arnés de P5-2—. Sin muestreo serían unas 370.000 evaluaciones y
horas de reloj. **Las fracciones de la puerta son estimaciones de muestra; las
del disparo son censo.**

**Y una tensión con el diagnóstico que motivó el trabajo.** La mesa diagnosticó
que «la frontera está lejos» y que por eso el tirón de un paso no hacía trayecto.
**Los datos dicen que la frontera está a seis casillas de mediana**, nunca a más
de once. Si la frontera está a seis pasos y el cuerpo aun así no la pisa, el
problema no era la distancia: era que **ningún paso suelto hacia ella ganaba la
decisión**. La forma lo arregla porque se juzga entera, no paso a paso — y eso sí
es lo que la ficha proponía.

---

## Propuesta, no ejecución

**El seco justifica el campo**, con dos reservas que deberían ir en el diseño de
la sonda:

1. **El abandono del 23 %** merece medirse en vivo antes que cualquier otra cosa:
   si en el campo sube, la forma de curiosidad será una promesa que se rompe una
   de cada cuatro veces.
2. **La consigna no manda** en este mundo (100 % de disparo con las dos). Si se
   quiere un mando, hay que buscarlo en otro sitio —cadencia, o una consigna
   sobre la ignorancia **local** y no la global—. **No lo cambio: proponerlo es
   mi trabajo, decidirlo es el de la mesa.**

---

## Custodia

| fichero | md5 |
|---|---|
| `cantera/paper5/curiosidad_forma.py` | `5e6074ee3a55acbd1a9c59ea3d610f0d` |
| `cantera/paper5/humo_P58A.py` | `4b8f769a81022a74b8ba18353f34802e` |
| `cantera/paper5/mide_P58A.py` | `c7de662c76eac021c6ce8d2773b11efe` |
| `cantera/paper5/analiza_P58A.py` | `7aebcd42428aae968bf39afc99f0d6b5` |

Datos: `P58A_lento.json`, `P58A_s2.json`.
Diarios: los 20 del brazo A de P5-7C (40 asientos) y los 40 de S-2 brazo A.

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

**PARO AQUÍ.**
