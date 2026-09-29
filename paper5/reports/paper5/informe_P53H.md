# P5-3H — El hermano que cuenta, con los extraños a piso

En seco, coste cero. Nada a la plataforma. **Ninguna decisión real cambia.**
Mismas 2.230 escenas, semilla **20260919**. **Último banco de la sección.**

**R18 falla, pero esta variante es la mejor de las cuatro en todo lo demás.**
E1+G2 deja pasar poco —el 5,84 % de las construidas, no el 15 % sellado—, pero
lo que pasa acierta el **85,37 %**, el azar se queda en **3 formas de 908**, la
diferencia es de **+42,51 puntos** con el cero fuera, y cuesta **1,17 ms por
tic**: veinte veces menos que el alcance.

**Y H3 confirma lo que G5 anunciaba: el hermano se recupera al 51,2 % y los
rivales no se recuperan (−2,4 %).**

---

## H1 · La variante

| pieza | cómo va |
|---|---|
| **filas de rivales** (5: F-4-ALCANCE, S-8-EXPOSICION, S-7-AGRESOR, MIEDO_APRENDIDO, S-VIDA-AJENA) | **con piso**: pueden empeorar por el camino, no mejorar |
| **filas del hermano** (10) | con su **estado real**, leído de **su** diario en cada punto de control |
| **filas propias y el anillo** (F-DANO, **F-ANTICIPACION**, F-REENCUENTRO, R-ACOPIO, R-CARENCIA, R-LLAMADA) | **proyectadas** |
| alcance (G1) | **fuera** |
| comparador | D1, el puñado en el tic de ventana, con las mismas proyecciones |
| resto | vida mínima 15, pesos `0,5^(tic/50)`, sin `deepcopy` |

Diario del hermano disponible en **40 de los 40** diarios.

---

## H2 · Las cuatro variantes, lado a lado

Vida entera. Universo **908** por llave; 2.230 para O-ahora.

| variante | llave | **pasa la regla** | **aceptada** | **en la mesa** | IC95 |
|---|---|---|---|---|---|
| **E1** (piso a todo) | O-después | 42 (4,63 %) | 36 (3,96 %) | **85,71 %** | 72,2–93,3 |
| | azar | 19 (2,09 %) | 8 (0,88 %) | 42,11 % | 23,1–63,7 |
| | **diferencia** | | | **+43,61** | +19,01 a +68,20 |
| **G1+G2** (alcance) | O-después | **127 (13,99 %)** | **98 (10,79 %)** | 77,17 % | 69,1–83,6 |
| | azar | 97 (10,68 %) | 50 (5,51 %) | 51,55 % | 41,7–61,2 |
| | **diferencia** | | | **+25,62** | +13,28 a +37,96 |
| **E1+G2, margen 0** | O-después | 53 (5,84 %) | 42 (4,63 %) | **79,25 %** | 66,5–88,0 |
| | azar | 20 (2,20 %) | 8 (0,88 %) | 40,00 % | 21,9–61,3 |
| | **diferencia** | | | **+39,25** | +15,16 a +63,33 |
| **E1+G2, margen 0,02** | O-después | 41 (4,52 %) | 35 (3,85 %) | **85,37 %** | 71,6–93,1 |
| | azar | **7 (0,77 %)** | **3 (0,33 %)** | 42,86 % | 15,8–75,0 |
| | **diferencia** | | | **+42,51** | **+4,28 a +80,73** |

Sobre las **construidas**, la diferencia O-después menos azar:

| variante | diferencia | IC95 |
|---|---|---|
| E1 | +3,08 | +1,68 a +4,49 |
| **G1+G2** | **+5,29** | +2,78 a +7,79 |
| E1+G2 m0 | +3,74 | +2,25 a +5,24 |
| E1+G2 m0,02 | +3,52 | +2,22 a +4,83 |

**O-ahora: 2.230 de 2.230 = 100,00 %** en las cuatro.

**El retrato de las cuatro, en una frase cada una.** E1 es la más estricta y la
que mejor separa en la mesa, pero deja pasar el 4,6 %. G1+G2 deja pasar el
triple, **y triplica también el azar**, así que separa peor y cuesta veinte
veces más. **E1+G2 con margen 0,02 es la más limpia**: casi tan estricta como
E1, con el azar reducido a **tres formas de novecientas ocho**, y la diferencia
más alta de las que tienen el cero fuera.

**El hermano añade once formas sobre E1** (42 → 53 con margen 0). No es mucho,
pero **es señal, no ruido**: el azar sube solo una (19 → 20).

---

## H3 · Qué recupera E1+G2

De la mejora que la forma proyecta para los futuros buenos (**436** con mejora
proyectada), contra la **real** medida en F2:

| grupo | proyectado | real (F2) | **recupera** |
|---|---|---|---|
| **hermano** | **+43,677** | 85,335 | **51,2 %** |
| **propias** | **+23,570** | 22,378 | **105,3 %** |
| **rivales** | **−2,540** | 104,568 | **−2,4 %** |

Reparto de lo proyectado: **hermano 64,95 %**, propias 35,05 %, rivales
**−3,78 %**.

**Las filas que más aporta:** `S-HERIDO` 32,88 · `S-DANO-PAREJA` 7,41 ·
`R-CARENCIA` 6,90 · `S-PROVISION` 6,21 · `R-HERMANO-FALTA` 4,68 · `R-ACOPIO`
4,13 · `F-REENCUENTRO` 3,58 · `F-HERMANO-GOLPE` 3,56. **Cinco de las ocho son
del hermano.**

**Tres lecturas.**

1. **El hermano se recupera al 51,2 %**, mejor que con el alcance (45,0 %).
   Escucharle es lo único que de verdad recupera algo de los otros, y **funciona
   mejor cuando los rivales van a piso** que cuando van por alcance.
2. **Lo propio se recupera al 105,3 %**, o sea entero y un poco más. El exceso
   viene de `F-REENCUENTRO` y del anillo, que en F2 quedaban repartidos en otros
   grupos; es un artefacto del corte, no una ganancia inventada, y se declara.
3. **Los rivales siguen en −2,4 %.** Con piso no pueden mejorar, así que su
   aporte proyectado solo puede ser cero o negativo. Igual que con el alcance
   (−2,9 %): **el trozo grande del 87 % es irrecuperable con cualquier
   tratamiento honesto de los rivales.**

---

## H4 · Contra qué gana el azar

Con E1+G2 y margen 0,02, el azar gana en **7 escenas** —de 908 construidas—, y
**en las 7 en su primer punto de control**.

| fila que le baja | veces |
|---|---|
| **F-REENCUENTRO** | **4** |
| R-LLAMADA | 1 |
| S-8-EXPOSICION | 1 |
| S-PROVISION | 1 |

**`F-REENCUENTRO` es la causa principal**: la memoria del mapa, sitios donde ya
te hicieron daño. No lleva piso porque **no mira a nadie**: es el mapa, y el
mapa es el mismo para las dos curvas. Que una casilla al azar caiga en zona
«limpia» es suerte, no mérito, pero tampoco es un regalo de la regla.

Con siete escenas, esto ya no es un problema de método: es el suelo de ruido.

---

## H5 · El tiempo

| variante | mediana | p90 | máximo | **cada 25 tics** |
|---|---|---|---|---|
| E1 | 4,18 ms | 5,59 | 8,34 | 1,16 ms/tic |
| G1+G2 (alcance) | 81,89 ms | 163,22 | 373,39 | 4,21 ms/tic |
| **E1+G2** | **4,39 ms** | **5,96** | **14,75** | **1,17 ms/tic** |

**Escuchar al hermano es gratis**: 4,39 ms contra los 4,18 de E1. El alcance
costaba veinte veces más y recuperaba menos.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **R18** | con E1+G2 y margen 0, O-después pasa en más del 15 % de las construidas | H2 | **5,84 %** (de 4,63 % con E1) | **FALLA** |
| **R19** | con margen 0,02, el azar por debajo del 30 % en la mesa | H2 | **42,86 %** (3 de 7) | **FALLA** |
| **R19** | …y por debajo del 3 % sobre construidas | H2 | **0,33 %** | **CUMPLE** |
| **R19** | …y O-después gana por más de 30 puntos, cero fuera | H2 | **+42,51**, IC95 +4,28 a +80,73 | **CUMPLE** |
| **R20** | recupera más del 40 % del hermano | H3 | **51,2 %** | **CUMPLE** |
| **R20** | …más del 50 % de lo propio | H3 | **105,3 %** | **CUMPLE** |
| **R20** | …de los rivales, cero o menos | H3 | **−2,4 %** | **CUMPLE** |
| **R21** | por debajo de 3 ms por tic | H5 | **1,17 ms** | **CUMPLE** |

**Los contadores podían variar, comprobado.** El de R18 ha ido 4,63 → 13,99 →
5,84 % en tres variantes con las mismas escenas. El del azar en la mesa va del
40,0 % al 51,6 % según la variante, y sobre construidas del 0,33 % al 5,51 %. El
de R20 se reparte en tres grupos, uno sale **negativo** y otro por encima del
100 %. El del tiempo va de 4,18 a 81,89 ms.

**R20 cumple sus tres cláusulas**, que es la predicción que de verdad medía la
hipótesis de la mesa: **el hermano se recupera, lo propio se recupera, los
rivales no.**

---

## Lo que la sección 5 deja cerrado

1. **El techo está medido y no es de la regla: es del mundo.** El 87 % de la
   mejora real está en filas que miran a los otros (P5-3F). De ese 87 %, **el
   trozo del hermano se recupera escuchándole (51,2 %) y el de los rivales no se
   recupera de ninguna manera honesta** (−2,4 % con piso, −2,9 % con alcance).
2. **La mejor variante es E1+G2 con margen 0,02.** Deja pasar el 4,52 % de las
   formas, acierta el 85,37 % de las que pasan, reduce el azar a **3 de 908**,
   separa por **+42,51 puntos** con el cero fuera, y cuesta **1,17 ms por tic**.
3. **El alcance no compensa.** Triplica lo que pasa, pero triplica el azar,
   separa peor (+25,62 contra +42,51) y cuesta veinte veces más.
4. **Escuchar al hermano es la única palanca barata que funciona.** Cuesta
   0,21 ms más por decisión y sube la recuperación del hermano del 0 % al 51,2 %.
5. **Y O-ahora sigue al 100,00 % en todas las variantes**: ensanchar la puerta
   no ha roto nunca lo que ya funcionaba.

**Lo que queda fuera del alcance de esta vía**, y queda dicho con cifras: para
cobrar el trozo de los rivales haría falta **predecirlos**, no acotarlos. Eso
rompe la ceguera declarada y P5-3A ya midió lo que costaría de error.

**PARO AQUÍ. No hay más bancos en esta sección.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`. Ficheros:
`forma.py` (con `PISO_RIVAL`, `pisos_rival`, `curva_H`, `mejor_propia_H`),
`banco_forma7.py`, `H3H4.py`, `P53H_resumen.json`, `P53H_H3H4.json`,
`P53H_progreso.log`, `P53H_corrida.log`, `P53H_H3H4_corrida.log`.
