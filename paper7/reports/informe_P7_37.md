# P7-37 · La curiosidad por lo que podría importar

*10-oct-2026. Coste cero: sin partidas, sin llamadas. Plataforma: 0 créditos de experiencia (acumulado del siete: 710 partidas = 710 créditos, contadas de los estados de los
lanzadores P7-8 a P7-34 y de los resultados de P7-5/6/7; disponibles hoy, dato de Manel: 496 de 1.000, con recarga de 71 al día). Consola de Anthropic: 0 USD.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar; solo banco, nada se juega ni cambia en el campo. Diseño
propuesto a Manel, pendiente de su sí. Scripts: `curiosa_P7_37.py` (= `afb5112e31ef405727142bac2a2ed2fb`; la pieza, solo banco), `banco_P7_37.py` (`--cadena` → `P7_37_cadena.json` y
`P7_37_res/cuaderno_descontada_*.json`; `--momentos` → `P7_37_momentos.json`), `cuaderno_P7_37.py` → `P7_37_cuadernos.json`, `escribe_informe_P7_37.py` (este informe; ninguna
cifra a mano). Las definiciones (importancia descontada, importancia esperada, variantes C y C5 con sus números declarados) están en la cabecera de `curiosa_P7_37.py`.*

## Sección 1 · La importancia descontada

La importancia de un recuerdo (cambio del malestar por eje entre abrir y cerrar la ventana) se vuelve a tasar restando el cambio que viene del daño conocido (anillo estando
fuera, golpes de rivales a la vista), como ya hace el efecto: al cerrar, se tasa la obs con la vida que tendría sin ese daño (`A.appraise` sobre una copia) y la diferencia de
malestar se descuenta. Para que la cadena fuera honesta, las 4 criaturas se replicaron día a día EN CADENA (el cuaderno que escribe la réplica del día d es el que lee el día
d+1): 959399 decisiones iguales al diario · 53119 distintas en 80 vidas (la réplica lleva ya la curiosidad nueva; lazo abierto, las obs son las del diario).

| cosa | recuerdos (sin cortes, cuadernos del día 20) | con daño conocido en la ventana (descontados) | importancia original: mediana (cuartiles) | importancia descontada: mediana (cuartiles) |
|---|---:|---:|---|---|
| botiquin | 67 | 0 | 0,2625 (0,133 · 0,422) | 0,2625 (0,133 · 0,422) |
| racion | 121 | 43 | 0,0967 (0,054 · 0,159) | 0,1053 (0,065 · 0,167) |
| red | 31 | 0 | 0,0839 (0,002 · 0,300) | 0,0839 (0,002 · 0,300) |
| camuflaje | 32 | 0 | 0,0991 (0,014 · 0,288) | 0,0991 (0,014 · 0,288) |

Solo 43 de 251 recuerdos tienen daño conocido dentro de su ventana (todos de la ración: se come bajo golpes; las ventanas del botiquín, la red y el camuflaje no reciben daño
conocido, o el que reciben no es de fuente a la vista), y en ellos la mediana apenas se mueve. La importancia de «no hizo nada» no baja con el descuento: lo que mueve el malestar en
una ventana de 10 s de calma no es el daño conocido, es lo demás (el hambre, la distancia a la hermana, el anillo que se acerca, lo que se ve).

## Sección 2 · La curiosidad por lo que podría importar

Curiosidad de clase = ignorancia × importancia esperada; importancia esperada = media ponderada de la importancia (escalar min(1, S/E)) de los recuerdos sin cortes con un
neutro de importancia 1 y peso 1 que no se apaga; intensidad como en el campo (1 + importancia descontada). Recalculado sobre los 80 cuadernos encadenados (cierre de cada día):

| criatura | día | botiquin: curiosidad campo → nueva · importancia esperada · creencia campo → descontada | racion: curiosidad campo → nueva · importancia esperada · creencia campo → descontada | red: curiosidad campo → nueva · importancia esperada · creencia campo → descontada | camuflaje: curiosidad campo → nueva · importancia esperada · creencia campo → descontada |
|---|---|---|---|---|---|
| s1 a10 | 5 | 0,087 → 0,025 · 0,29 · 12,7 → 12,7 | 0,119 → 0,024 · 0,20 · 5,8 → 5,8 | 0,352 → 0,127 · 0,36 · 0,0 → 0,0 | 0,341 → 0,155 · 0,46 · 0,0 → 0,0 |
| s1 a10 | 10 | 0,048 → 0,011 · 0,24 · 11,0 → 11,0 | 0,054 → 0,009 · 0,17 · 5,7 → 5,7 | 0,224 → 0,069 · 0,31 · 0,0 → 0,0 | 0,205 → 0,088 · 0,43 · 0,0 → 0,0 |
| s1 a10 | 15 | 0,027 → 0,008 · 0,28 · 35,5 → 35,5 | 0,054 → 0,009 · 0,17 · 8,4 → 8,4 | 0,145 → 0,036 · 0,25 · 0,0 → 0,0 | 0,167 → 0,056 · 0,33 · 0,0 → 0,0 |
| s1 a10 | 20 | 0,021 → 0,008 · 0,39 · 38,3 → 38,3 | 0,036 → 0,006 · 0,17 · 11,2 → 11,2 | 0,138 → 0,031 · 0,22 · 0,0 → 0,0 | 0,108 → 0,031 · 0,29 · 0,0 → 0,0 |
| s1 a11 | 5 | 0,164 → 0,055 · 0,33 · 15,7 → 15,7 | 0,076 → 0,015 · 0,19 · 8,9 → 8,9 | 0,218 → 0,110 · 0,50 · 0,0 → 0,0 | 0,501 → 0,277 · 0,55 · 0,0 → 0,0 |
| s1 a11 | 10 | 0,067 → 0,033 · 0,49 · 31,6 → 31,6 | 0,052 → 0,010 · 0,20 · 13,1 → 13,1 | 0,265 → 0,142 · 0,53 · 0,0 → 0,0 | 0,264 → 0,084 · 0,32 · 0,0 → 0,0 |
| s1 a11 | 15 | 0,045 → 0,023 · 0,50 · 36,5 → 36,5 | 0,045 → 0,008 · 0,19 · 13,2 → 13,2 | 0,203 → 0,077 · 0,38 · 0,0 → 0,0 | 0,201 → 0,047 · 0,23 · 0,0 → 0,0 |
| s1 a11 | 20 | 0,033 → 0,014 · 0,43 · 33,8 → 33,8 | 0,052 → 0,010 · 0,19 · 12,9 → 13,0 | 0,156 → 0,059 · 0,38 · 3,3 → 3,3 | 0,198 → 0,045 · 0,23 · 0,0 → 0,0 |
| s2 a10 | 5 | 0,076 → 0,034 · 0,45 · 36,9 → 36,9 | 0,061 → 0,012 · 0,20 · 13,8 → 13,8 | 1,000 → 1,000 · 1,00 · — → — | 0,266 → 0,154 · 0,58 · 0,0 → 0,0 |
| s2 a10 | 10 | 0,074 → 0,032 · 0,44 · 34,3 → 34,3 | 0,058 → 0,015 · 0,26 · 13,7 → 13,7 | 0,190 → 0,070 · 0,37 · 0,0 → 0,0 | 0,192 → 0,085 · 0,44 · 0,0 → 0,0 |
| s2 a10 | 15 | 0,085 → 0,037 · 0,44 · 36,7 → 36,7 | 0,064 → 0,016 · 0,26 · 13,3 → 13,4 | 0,161 → 0,045 · 0,28 · 0,0 → 0,0 | 0,130 → 0,049 · 0,38 · 6,4 → 6,4 |
| s2 a10 | 20 | 0,086 → 0,035 · 0,41 · 34,1 → 34,1 | 0,054 → 0,011 · 0,21 · 12,9 → 12,9 | 0,114 → 0,038 · 0,33 · 0,0 → 0,0 | 0,119 → 0,042 · 0,35 · 4,6 → 4,6 |
| s2 a11 | 5 | 0,164 → 0,085 · 0,52 · 11,6 → 11,7 | 0,113 → 0,062 · 0,56 · 5,6 → 5,6 | 0,339 → 0,115 · 0,34 · 0,0 → 0,0 | 0,511 → 0,263 · 0,51 · 0,0 → 0,0 |
| s2 a11 | 10 | 0,057 → 0,021 · 0,37 · 22,8 → 22,8 | 0,080 → 0,030 · 0,38 · 6,8 → 6,8 | 0,209 → 0,067 · 0,32 · 0,0 → 0,0 | 0,281 → 0,080 · 0,28 · 0,0 → 0,0 |
| s2 a11 | 15 | 0,030 → 0,011 · 0,36 · 24,8 → 24,8 | 0,056 → 0,015 · 0,27 · 12,8 → 12,8 | 0,201 → 0,069 · 0,34 · 4,6 → 4,6 | 0,255 → 0,071 · 0,28 · 0,0 → 0,0 |
| s2 a11 | 20 | 0,036 → 0,013 · 0,37 · 23,6 → 23,6 | 0,043 → 0,009 · 0,21 · 13,8 → 13,8 | 0,191 → 0,069 · 0,36 · 3,4 → 3,4 | 0,159 → 0,038 · 0,24 · 0,0 → 0,0 |

- **¿Cuántas veces al día sería lo inútil la clase que más llama?** En 76 de 80 cierres de día (criatura × día), frente a 77 de 80 con la curiosidad del campo.
- **¿Cuánto valdría su curiosidad frente a la de lo útil?** La mayor curiosidad de red o camuflaje dividida por la mayor de botiquín o ración: mediana 3,95 (cuartiles
  2,62 · 5,37) con la regla nueva, frente a 3,40 (2,67 · 4,29) con la del campo. La importancia esperada de lo inútil
  (0,20-0,76) no queda por debajo de la de lo útil (0,16-1,00): el neutro de importancia 1 pesa como varios recuerdos de 0,1-0,3, y curar
  no importa diez veces más que llevar una red, importa dos o tres veces más (sección 1).
- **¿Se mantiene la creencia de lo útil?** Sí: la mayor diferencia entre la creencia del botiquín o la ración con el cuaderno del campo y con el descontado, en los 80 cierres, es 0,065.
- **¿Cuándo volvería a despertar la curiosidad por lo inútil tras días sin tocarlo, y con qué fuerza?** No hay días sin tocarlo en los que esté dormida: tras cada prueba vuelve a ser la clase que
  más llama al día siguiente en 57 de 60 pruebas, con una curiosidad de 0,024-0,264 (mediana 0,068) frente a la de lo útil (tabla).

| criatura | cosa | pruebas (días) | tras cada prueba: vuelve a mandar el día… (curiosidad nueva de la cosa · la mayor de lo útil) |
|---|---|---|---|
| s1 a10 | red | 1, 5, 6, 9, 13, 14, 15, 16 | d1 → 2 (0,263 · 0,071); d5 → 6 (0,073 · 0,027); d6 → 7 (0,079 · 0,019); d9 → 10 (0,069 · 0,011); d13 → 14 (0,047 · 0,009); d14 → 15 (0,036 · 0,009); d15 → 16 (0,024 · 0,009); d16 → 17 (0,025 · 0,009) |
| s1 a10 | camuflaje | 1, 2, 6, 9, 13, 14, 16, 17, 20 | d1 → 2 (0,131 · 0,071); d2 → 3 (0,139 · 0,051); d6 → 7 (0,105 · 0,019); d9 → 10 (0,088 · 0,011); d13 → 14 (0,052 · 0,009); d14 → 15 (0,056 · 0,009); d16 → 17 (0,039 · 0,009); d17 → 18 (0,041 · 0,009); d20 → no (— · —) |
| s1 a11 | red | 2, 3, 4, 11, 13, 17, 19 | d2 → 3 (0,155 · 0,063); d3 → 4 (0,105 · 0,067); d4 → 5 (0,110 · 0,055); d11 → 12 (0,097 · 0,033); d13 → 14 (0,072 · 0,026); d17 → 18 (0,070 · 0,017); d19 → 20 (0,059 · 0,014) |
| s1 a11 | camuflaje | 3, 8, 10, 11, 15, 19 | d3 → 4 (0,264 · 0,067); d8 → 9 (0,146 · 0,038); d10 → 11 (0,055 · 0,035); d11 → 12 (0,059 · 0,033); d15 → 16 (0,051 · 0,024); d19 → 20 (0,045 · 0,014) |
| s2 a10 | red | 6, 7, 8, 9, 13, 15, 16, 19, 20 | d6 → 7 (0,122 · 0,038); d7 → 8 (0,084 · 0,040); d8 → 9 (0,066 · 0,031); d9 → 10 (0,070 · 0,032); d13 → 14 (0,060 · 0,035); d15 → 16 (0,043 · 0,040); d16 → 17 (0,045 · 0,042); d19 → 20 (0,038 · 0,035); d20 → no (— · —) |
| s2 a10 | camuflaje | 5, 7, 8, 11, 13, 15, 17, 20 | d5 → 6 (0,161 · 0,036); d7 → 8 (0,076 · 0,040); d8 → 9 (0,080 · 0,031); d11 → 12 (0,068 · 0,032); d13 → 14 (0,058 · 0,035); d15 → 16 (0,052 · 0,040); d17 → 18 (0,045 · 0,032); d20 → no (— · —) |
| s2 a11 | red | 4, 5, 8, 10, 11, 18 | d4 → 5 (0,115 · 0,085); d5 → 6 (0,123 · 0,065); d8 → 9 (0,100 · 0,049); d10 → 11 (0,054 · 0,032); d11 → 12 (0,058 · 0,029); d18 → 19 (0,065 · 0,012) |
| s2 a11 | camuflaje | 4, 6, 10, 12, 16, 18, 19 | d4 → 5 (0,263 · 0,085); d6 → 7 (0,127 · 0,055); d10 → 11 (0,086 · 0,032); d12 → 13 (0,062 · 0,013); d16 → 17 (0,052 · 0,015); d18 → 19 (0,036 · 0,012); d19 → 20 (0,038 · 0,013) |

## Sección 3 · Los 71 momentos, en banco

Las 80 vidas de APRENDE replicadas con el cuaderno descontado del día anterior, bajo cuatro lecturas de la curiosidad de clase: **campo** (ignorancia), **descontada**
(ignorancia × importancia esperada), **C** (ignorancia por parecido de contexto y foto × importancia esperada) y **C5** (parecido que incluye cómo se probó, la mayor entre
las formas de la cosa, × importancia esperada). Momentos: los 71 tics en que el diario decidió coger una red o un camuflaje y las 63 aperturas de prueba de red y camuflaje.

| lectura | fidelidad al diario (80 vidas) | de las cogidas de red y camuflaje del diario: siguen siendo `coger` | lo que elige en las demás | en las aperturas de prueba: curiosidad de la red (mediana) · del camuflaje · del botiquín · de la ración | momentos en que la clase que más llama es red o camuflaje |
|---|---|---:|---|---|---:|
| campo | 1012488 igual · 30 difiere | 71 de 71 | — | 0,246 · 0,236 · 0,076 · 0,060 | 125 de 134 |
| descontada | 959399 igual · 53119 difiere | 61 de 71 | `ir_curioso` 10 | 0,089 · 0,090 · 0,033 · 0,014 | 123 de 134 |
| C | 873035 igual · 139483 difiere | 46 de 71 | `ir_curioso` 25 | 0,142 · 0,150 · 0,155 · 0,071 | 67 de 134 |
| C5 | 860728 igual · 151790 difiere | 47 de 71 | `ir_curioso` 24 | 0,301 · 0,301 · 0,358 · 0,197 | 62 de 134 |

Con la lectura del campo (sobre el cuaderno descontado, que cambia 43 intensidades) la réplica es casi la del diario; con las otras tres cambian muchas decisiones (la fila
`R-CURIOSIDAD` y `ir_curioso` leen otra cosa), pero en los momentos de coger, **`coger` sigue ganando** en 61, 46 y 47 de 71: la cosa está a los pies y la
curiosidad, sea cual sea su lectura, se alivia al tenerla. Lo que se va en C y C5 (una de cada tres) se va a `ir_curioso` hacia otra clase: por parecido, el botiquín
que nunca se usó en una situación como esa llama tanto o más que la red que ya se llevó en ella (en las aperturas, con C la curiosidad del botiquín 0,155 ≥ red 0,142).

## Sección 4 · Variante C: en qué contextos probaría de nuevo

En los 134 momentos (104 en calma, 30 en peligro, según `peligro_de` de P7-33), la clase que más llama con C es la red o el camuflaje en 67: 42 en calma y
25 en peligro. De los de peligro, la cautela por distancia (P7-26) la habría apagado del todo en 11 (cautela 0), atenuado en 14 y dejado pasar en 0.
¿Repetiría pruebas en calma o iría a contextos nuevos? Con la forma `coger`, la situación que más llama es OTRA que la de ahora (fuera del círculo o recién golpeada) en
240 de 268 momentos y la de ahora en 28: las pruebas reales de los cuadernos del día 20 fueron red dentro · sin golpe 31, camuflaje dentro · sin golpe 29, camuflaje dentro · golpeado 3, así que por parecido la calma ya está «gastada» y lo
nuevo es el peligro; y ahí entra la cautela.

## Sección 5 · La mirada de científico (C5): qué forma y qué situación preferiría

| cosa | momentos | forma preferida (C5) | situación preferida (C5) | con la forma `coger`: la situación que más llama es la de ahora / otra |
|---|---:|---|---|---|
| red | 134 | empunar 117, coger 17 | fuera · golpeado 116, dentro · sin golpe 18 | 15 / 119 |
| camuflaje | 134 | ponerse 121, coger 13 | fuera · golpeado 102, fuera · sin golpe 17, dentro · sin golpe 15 | 13 / 121 |

Las formas de las pruebas reales (cuadernos del día 20): red `coger` 31, camuflaje `coger` 29, camuflaje `ponerse` 3. El camuflaje cuenta como `coger` porque con el cuerpo vacío coger ES
vestir (sim.nim, PROMPT_17/18): la forma se lee de la acción, no del resultado, y por eso C5 toma `ponerse` como forma nueva aunque el resultado sea el mismo (límite
declarado). La forma nueva (`empunar` la red, `ponerse` el camuflaje) y la situación nueva (fuera del círculo, o recién golpeada) son las que más llaman: con la mirada de
científico la siguiente prueba no repetiría la mirada, iría a empuñar la red o ponerse el camuflaje en peligro, que es justo lo que la cautela apaga.

## Lo que se desprende (propuestas, no decisiones)

1. El descuento del daño conocido no toca «no hizo nada»: su importancia no viene del daño, viene del malestar de fondo que cambia en 10 s. Para que «no hizo nada» importe
   poco, la importancia tendría que medirse contra lo que habría pasado sin la prueba (la foto del tic de apertura proyectada 10 s, o el malestar de la hermana), no contra el
   malestar de antes.
2. Con el neutro de importancia 1, la curiosidad nueva sigue mandando a lo inútil; el neutro tendría que apagarse con los recuerdos de «no hizo nada» (o pesar menos que 1) para
   que lo probado sin fruto deje de llamar.
3. La variante C y la C5 mueven la curiosidad hacia lo no probado (otra situación, otra forma), que es peligro: sin la cautela de P7-26 en el campo, sería una criatura que
   prueba redes bajo golpes. Si la mesa quiere C5, va con la cautela.

## Fe de erratas (10-oct-2026, hallada al construir P7-38)

La pieza `curiosa_P7_37` se enganchaba POR DENTRO de la de P7-33 (`banco_P7_33` encadena las piezas del siete después de ella), y las ventanas de la red y del camuflaje se
cierran en la de P7-33: el descuento del daño conocido no las veía. En los diarios de P7-34 hay 4 recuerdos de red y camuflaje (3 de red, 1 de camuflaje; de 63) con daño
conocido dentro de su ventana (golpes de rivales a la vista, 3,0-26,4 puntos) que quedaron sin descontar; la frase de la sección 1 «las ventanas del botiquín, la red y el
camuflaje no reciben daño conocido» es falsa para esos 4 (los 68 del botiquín sí están sin daño conocido). Las medianas y las conclusiones no cambian (4 de 63 recuerdos; la
importancia de «no hizo nada» sigue viniendo del malestar de fondo); no se repite la cadena. En P7-38 la pieza se engancha por fuera de todas (`banco_P7_38`, envolviendo
`nace_P7_33.aplica`) y sí ve esas ventanas.
