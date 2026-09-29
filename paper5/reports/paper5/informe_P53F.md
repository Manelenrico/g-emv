# P5-3F — El embudo y la descomposición

En seco, coste cero. Nada a la plataforma. **Nada más se construye.**

**El titular cierra la sección.** El **87,4 %** de la mejora real de los futuros
buenos de S-2 viene de **filas que miran a los otros**, y en el **79,2 %** de
esos futuros ese grupo aporta más de la mitad. En el mundo lento es **peor**, no
mejor: **90,1 %** y 78,9 %. **Una forma honesta —que no cobra seguridad por lo
que no ve— tiene un techo de alrededor del 10 % de lo que hay que ganar.** Eso
no es un defecto de la regla: es el mundo.

**Y encontré un error mío en P5-3E**, que corrijo y reporto: `F-ANTICIPACION`
**mira al anillo, no a los rivales**, así que no debía llevar piso. Corregido,
el efecto es casi nulo.

---

## La corrección de E1

`appraisal_zs_v42_exp.py:975` lo dice en la cabecera de la fila:

```
# ── F-ANTICIPACION (solo lo CIERTO: calendario del anillo) ──────────────
#   t_arde = cuando ESA casilla queda fuera de la zona segura, del calendario
#            completo (mundo.t_arde), incluida la etapa final a radio 0.
```

Y `:986` recorre `mundo.eventos_arde(pos, tick)`. **Es determinista y sí se
proyecta**, así que ponerle piso impedía a la forma cobrar una mejora legítima:
**salir del fuego**. La lista `PISO_OTROS` pasa de **16 filas a 15**.

**El efecto es casi nulo, y así hay que decirlo:**

| | E1 de P5-3E (16 filas) | **E1 corregido (15 filas)** |
|---|---|---|
| O-después que pasa la regla | 46 de 908 | **44 de 908** |
| azar que pasa la regla | 19 de 908 | **19 de 908** |
| O-después aceptada, vida entera | 39 (4,3 %) | **38 (4,2 %)** |
| azar aceptada, vida entera | 8 (0,9 %) | **8 (0,9 %)** |

El piso de esa fila casi nunca mordía. El error era real; su consecuencia, dos
formas de 908.

---

## F1 · El embudo

Sobre las **908** formas construidas de cada llave. Criterio de vida entera.

| variante | llave | construidas | pasa vida mínima | **pasa el área** | llega a la mesa | **aceptada** |
|---|---|---|---|---|---|---|
| **D1+D2** | O-después | 908 | 884 (97,4 %) | **81 (8,9 %)** | 81 (8,9 %) | **55 (6,1 %)** |
| | azar | 908 | 878 (96,7 %) | 79 (8,7 %) | 79 (8,7 %) | 28 (3,1 %) |
| **E1 corregido, margen 0** | O-después | 908 | 884 (97,4 %) | **42 (4,6 %)** | 42 (4,6 %) | **36 (4,0 %)** |
| | azar | 908 | 878 (96,7 %) | **19 (2,1 %)** | 19 (2,1 %) | **8 (0,9 %)** |
| **E1, margen 0,02** | O-después | 908 | 884 (97,4 %) | **35 (3,9 %)** | 35 (3,9 %) | **32 (3,5 %)** |
| | azar | 908 | 878 (96,7 %) | **6 (0,7 %)** | 6 (0,7 %) | **2 (0,2 %)** |

**Dos cosas que el embudo deja claras.**

1. **La vida mínima casi no filtra.** El 97,4 % la pasa. **Todo el embudo es el
   área.** El `VIDA_MIN` es un seguro que casi nunca se dispara, lo cual ya se
   veía en P5-3B: moverlo de 10 a 20 cambiaba ocho formas de 908.
2. **Las tasas de la mesa que vengo dando son condicionales sobre un 5 % de
   supervivientes.** Cuando digo «O-después gana el 85,71 % en la mesa», el
   denominador son **42 formas de 908**. Sobre las construidas, gana el
   **3,96 %**. Las dos cifras son verdad y dicen cosas distintas: la primera es
   «si la regla la deja pasar, casi siempre acierta»; la segunda es «la regla
   deja pasar muy poco».

La tasa en la mesa, con su intervalo:

| margen | O-después | azar | 
|---|---|---|
| 0 | **85,71 %** (36/42), IC95 72,2–93,3 | **42,11 %** (8/19), IC95 23,1–63,7 |
| 0,02 | **91,43 %** (32/35), IC95 77,6–97,0 | 33,33 % (2/6), IC95 9,7–70,0 |

---

## F2 · De dónde viene la mejora real, en S-2

Para cada uno de los futuros buenos, `d(t) − d(t+100)` **real del diario**, sin
proyección, repartida por filas con `A.filas()` en los dos instantes.

**La atribución, declarada.** `opponent_distance` **no es aditiva** en las
filas. Se usa el reparto **uno a uno**: para cada fila, cuánto baja la `d` si
**solo** esa fila pasa de su valor en `t` al de `t+100`. La suma de los trozos no
da el total exacto; el **residuo relativo mediano es 0,0021**, o sea dos por mil.

**Los cuatro grupos**, con las filas de cada uno:

| grupo | filas |
|---|---|
| **los otros** (15) | F-4-ALCANCE, S-8-EXPOSICION, S-7-AGRESOR, MIEDO_APRENDIDO, S-VIDA-AJENA · y las del hermano: S-COMPANIA, S-SOLEDAD, S-DANO-PAREJA, S-MUERTE-PAREJA, S-VINCULO, S-HERIDO, S-PROVISION, F-HERMANO-AMENAZA, F-HERMANO-GOLPE, R-HERMANO-FALTA |
| **inventario y suelo** | R-ACOPIO, R-CARENCIA, R-LLAMADA |
| **vida y anillo** | F-DANO, F-ANTICIPACION |
| memoria del mapa | F-REENCUENTRO |

### El reparto, sobre **793** futuros buenos de S-2

| grupo | aporta | **fracción de lo positivo** |
|---|---|---|
| **los otros** | +165,596 | **87,43 %** |
| inventario y suelo | +16,556 | 8,74 % |
| memoria del mapa | +4,168 | 2,20 % |
| vida y anillo | +3,087 | 1,63 % |

**El grupo de los otros aporta más de la mitad en 628 de 793 futuros = 79,19 %.**

**Las filas que más aportan:**

| fila | aporta | grupo |
|---|---|---|
| **F-4-ALCANCE** | 50,20 | los otros |
| **S-HERIDO** | 47,06 | los otros (hermano) |
| **S-8-EXPOSICION** | 39,12 | los otros |
| S-DANO-PAREJA | 21,73 | los otros (hermano) |
| S-7-AGRESOR | 15,25 | los otros |
| R-CARENCIA | 14,16 | inventario |

**Las tres primeras son, exactamente, las filas que el principio de E1 obliga a
congelar.** Y la segunda y la cuarta son **del hermano**, no de los rivales.

---

## F3 · El mundo lento

Sobre **270** futuros buenos de los seis asientos-partida:

| grupo | aporta | **fracción de lo positivo** |
|---|---|---|
| **los otros** | +69,016 | **90,12 %** |
| inventario y suelo | +5,567 | 7,27 % |
| vida y anillo | +1,296 | 1,69 % |
| memoria del mapa | +0,700 | 0,91 % |

**Los otros aportan más de la mitad en 213 de 270 = 78,89 %.** Residuo mediano
de la atribución: 0,0016.

Filas que más aportan: **F-4-ALCANCE 34,90**, S-HERIDO 15,40,
**S-8-EXPOSICION 12,22**, S-DANO-PAREJA 4,14, R-CARENCIA 3,86.

**El mundo lento no ayuda: empeora.** 90,1 % contra 87,4 %. Tiene sentido con lo
que ya sabíamos de P5-1: allí la vida es más larga y plana, así que lo poco que
cambia la `d` cambia por los otros aún más que en S-2.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **R10** | en S-2, más de la mitad de la mejora viene de los otros | F2 | **87,43 %** | **CUMPLE** |
| **R10** | en más del 60 % de los futuros ese grupo aporta más de la mitad | F2 | **79,19 %** (628 de 793) | **CUMPLE** |
| **R11** | en el mundo lento la parte de los otros baja de la mitad | F3 | **90,12 %** — **sube** | **FALLA** |
| **R12** | en E1, O-después pasa la regla en menos del 15 % de las construidas | F1 | **4,63 %** (42 de 908) | **CUMPLE** |
| **R12** | en D1+D2, más del 50 % | F1 | **8,92 %** (81 de 908) | **FALLA** |

**Los contadores podían variar, comprobado.** El de R10 se reparte entre cuatro
grupos y veintiún renglones, y ninguno estaba forzado: el segundo grupo se queda
en el 8,74 %. El de R11 podía bajar, y de hecho bajan los otros tres grupos en
el mundo lento; lo que sube es el de los otros. El de R12 va del 8,9 % con
D1+D2 al 3,9 % con margen 0,02, pasando por 4,6 %: tres valores con las mismas
escenas.

### R11 falla, y falla de forma informativa

Se selló esperando que en el mundo lento, con el anillo lejos y menos presión,
la mejora viniera de otras cosas. Pasa lo contrario. La explicación está en
P5-1 D: allí la vida es plana durante tramos larguísimos —el 82 % de las
ventanas de cien instantes no pierden un punto de vida, el 89 % no cambian W—,
así que **cuando la `d` se mueve, se mueve por los otros casi siempre**. Alargar
el mundo no cambia de qué depende el bienestar de esta criatura: lo concentra.

---

## Lo que esta sección deja cerrado

1. **El techo de una forma honesta en este mundo es de alrededor del 10 %.** Si
   la forma no puede cobrar nada que dependa de dónde estén los otros, renuncia
   al **87,4 %** de la mejora disponible en S-2 y al **90,1 %** en el mundo
   lento. Lo que le queda —inventario, suelo, vida y anillo— es el 12,6 % y el
   9,9 %.
2. **Por eso la regla honesta deja pasar tan poco.** El 4,6 % de las formas
   buenas pasan el área en E1. No es que la regla sea dura: es que con lo
   proyectable apenas hay mejora que enseñar.
3. **Y por eso la puerta de hoy no distinguía nada** (P5-2c, +1,30 puntos con el
   cero dentro): lo que separa un futuro bueno de uno cualquiera está,
   sobre todo, en dónde acaban los otros, y eso ni la foto ni la forma lo saben.
4. **Dos de las tres filas que más aportan son del hermano** —S-HERIDO 47,06 y
   S-DANO-PAREJA 21,73—, no de los rivales. El hermano se ve, pero tampoco se
   proyecta.
5. **La vida mínima no filtra.** El 97,4 % la pasa. Si hay que simplificar la
   regla, ese es el candidato a quitar.

**El camino que esto abre, y que NO he tomado:** para que una forma valga en
este mundo habría que proyectar a los otros, aunque sea mal. P5-3A ya midió lo
que eso costaría de error; F2 y F3 miden ahora lo que cuesta **no** hacerlo. Las
dos cifras están sobre la mesa y la decisión es tuya.

**PARO AQUÍ. Nada más se construye.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`. Ficheros:
`descompone_F2.py`, `P53F_F2_S2.json`, `P53F_F3_lento.json`,
`P53F_E1corr_resumen.json`, `P53F_progreso.log`, `P53F_corrida.log`, y
`forma.py` con `PISO_OTROS` corregida a 15 filas.
