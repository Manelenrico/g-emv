# Figuras 3.1, 5.2 y 5.3 del paper siete

*Escrito por `hace_figuras_P7.py` desde los datos (ninguna cifra a mano). Sin partidas, sin llamadas: 0 créditos, 0 $. No se toca `motor/model.py`, ni el cuerpo, ni ningún guion de los experimentos; ninguna réplica se ha vuelto a ejecutar. Rutas relativas a `cantera/paper7/`. Valores también en `figuras/figuras_P7_valores.json`.*

Estilo: matplotlib, fondo blanco, sin título, 16 × 9 cm, letra de 11 puntos, PNG a 300 ppp y PDF; acento `#1f6f78`; líneas continua, discontinua y de puntos; nombre junto a cada línea. Las etiquetas largas del eje y (5.3 y 3.1) van partidas en dos líneas para que quepan; el texto es el pedido, sin cambios.

## Figura 5.2 · Llegadas al sitio de la mentira (P7-67, nivel 1, MIENTE y CONGELADA)

- Datos: `P7_67_analisis.json` → `criatura_dias_detalle` (lo escribe el guion sellado `analiza_P7_67.py`; campo `llegadas` contado en `analiza_P7_67.py:58`), nivel 1, sumado sobre las 16 series y las dos hermanas en cada tramo de cinco días, igual que la tabla exploratoria del informe (`escribe_informe_P7_67_campo.py:28-33` → `informe_P7_67_campo.md:97-108`).

| brazo | días 1-5 | 6-10 | 11-15 | 16-20 |
|---|---|---|---|---|
| MIENTE | 73 | 16 | 15 | 2 |
| CONGELADA | 112 | 143 | 153 | 113 |

**Comprobación obligatoria (MIENTE 73, 16, 15, 2; CONGELADA 112, 143, 153, 113): pasa.**

**¿Engaña contar llegadas? Cuántas veces se ofreció ir** (criatura-días con oferta: `oportunidad`, `analiza_P7_67.py:64`; un día sin oferta no puede tener llegada):

| brazo · días | criatura-días | con oferta | aceptaciones | llegadas | llegadas por oferta | días sin ninguna oferta |
|---|---|---|---|---|---|---|
| MIENTE d1-5 | 160 | 160 | 160 | 73 | 0,456 | — |
| MIENTE d6-10 | 160 | 159 | 157 | 16 | 0,101 | 8 |
| MIENTE d11-15 | 160 | 160 | 160 | 15 | 0,094 | — |
| MIENTE d16-20 | 160 | 130 | 129 | 2 | 0,015 | 19 |
| CONGELADA d1-5 | 160 | 160 | 160 | 112 | 0,700 | — |
| CONGELADA d6-10 | 160 | 159 | 159 | 143 | 0,899 | 8 |
| CONGELADA d11-15 | 160 | 160 | 160 | 153 | 0,956 | — |
| CONGELADA d16-20 | 160 | 130 | 130 | 113 | 0,869 | 19 |
| HONESTA d1-5 | 160 | 160 | 160 | 133 | 0,831 | — |
| HONESTA d6-10 | 160 | 160 | 160 | 159 | 0,994 | — |
| HONESTA d11-15 | 160 | 160 | 160 | 160 | 1,000 | — |
| HONESTA d16-20 | 160 | 160 | 160 | 160 | 1,000 | — |

Las ofertas son casi las mismas en los dos brazos y en todos los tramos; la única falta grande es el tramo 16-20, el mismo en MIENTE y CONGELADA (el día 19, sin oferta en ninguna criatura de esos dos brazos, que comparten destino: `informe_P7_67_campo.md`, sección 8.1; HONESTA, con otro destino, sí la tuvo). Contar llegadas no engaña por el lado de las ofertas: la caída de MIENTE no viene de que se le ofreciera menos. HONESTA va en la tabla solo como referencia (no se dibuja).

## Figura 5.3 · La confianza día a día (P7-67, nivel 1)

- Datos: el mismo `criatura_dias_detalle`, campo `conf_arranque.recursos` (la confianza leída del cuaderno al arrancar cada día, registro `P7_54_arranque`: `analiza_P7_67.py:61`).
- **La media es por criatura**: la media simple de las 32 criaturas de cada día (16 series × 2 hermanas), como en `analiza_P7_67.py:170-174` → `confianza_dia_a_dia` → `informe_P7_67_campo.md:67-88`. Cada día tiene las 32 en los tres brazos, así que coincide con la media de las 16 medias por serie.
- Banda: ± 1 error típico con la serie como unidad (media de las dos hermanas por serie; sd de las 16 / √16). No sale de ningún informe: es nueva para la figura.

| día | MIENTE | ee | CONGELADA | ee | HONESTA | ee |
|---|---|---|---|---|---|---|
| 1 | 0,500 | 0,000 | 0,500 | 0,000 | 0,500 | 0,000 |
| 2 | 0,458 | 0,017 | 0,500 | 0,000 | 0,519 | 0,023 |
| 3 | 0,360 | 0,021 | 0,500 | 0,000 | 0,585 | 0,027 |
| 4 | 0,341 | 0,016 | 0,500 | 0,000 | 0,602 | 0,041 |
| 5 | 0,271 | 0,013 | 0,500 | 0,000 | 0,643 | 0,044 |
| 6 | 0,229 | 0,012 | 0,500 | 0,000 | 0,740 | 0,033 |
| 7 | 0,202 | 0,006 | 0,500 | 0,000 | 0,818 | 0,023 |
| 8 | 0,200 | 0,006 | 0,500 | 0,000 | 0,817 | 0,030 |
| 9 | 0,200 | 0,006 | 0,500 | 0,000 | 0,801 | 0,036 |
| 10 | 0,188 | 0,005 | 0,500 | 0,000 | 0,814 | 0,036 |
| 11 | 0,188 | 0,005 | 0,500 | 0,000 | 0,813 | 0,047 |
| 12 | 0,188 | 0,005 | 0,500 | 0,000 | 0,869 | 0,033 |
| 13 | 0,181 | 0,005 | 0,500 | 0,000 | 0,909 | 0,023 |
| 14 | 0,181 | 0,005 | 0,500 | 0,000 | 0,823 | 0,038 |
| 15 | 0,161 | 0,006 | 0,500 | 0,000 | 0,876 | 0,027 |
| 16 | 0,161 | 0,006 | 0,500 | 0,000 | 0,914 | 0,019 |
| 17 | 0,159 | 0,006 | 0,500 | 0,000 | 0,939 | 0,013 |
| 18 | 0,159 | 0,006 | 0,500 | 0,000 | 0,826 | 0,042 |
| 19 | 0,157 | 0,006 | 0,500 | 0,000 | 0,822 | 0,034 |
| 20 | 0,157 | 0,006 | 0,500 | 0,000 | 0,838 | 0,033 |

**Comprobación obligatoria (día 20: MIENTE 0,157, HONESTA 0,838; CONGELADA plana en 0,5): pasa** (MIENTE 0,157, HONESTA 0,838, CONGELADA 0,500 los 20 días; los 60 valores coinciden con `confianza_dia_a_dia` de `P7_67_analisis.json`).

## Figura 3.1 · Qué deprisa aprende lo que cura el botiquín

- Eje y: la creencia del cuerpo sobre lo que cura el botiquín dividida por lo que cura de verdad, 50 (`informe_P7_62.md:17`); la línea horizontal es la mitad (25, el umbral de `analiza_P7_46.py:154` y de H3 en `analiza_P7_47.py:29`). Cada línea es la **mediana entre criaturas** de la creencia tras la k-ésima prueba, mientras quedan al menos 3 criaturas.
- **Fórmula antigua**: `P7_46_resumen.json` → `R1.curva_mediana` (`analiza_P7_46.py:146-153,171`), una línea por cadena: APRENDE prudente y APRENDE valiente, 6 criaturas cada una. Ojo: P7-46 no es una réplica sino la lectura de los diarios del campo P7-45 (`banco_P7_46.py:1`); y en su cuenta una prueba cortada es una prueba que deja la creencia como estaba (`analiza_P7_46.py:6,86-87`).
- **Escala propia**: la cadena en réplica de P7-47 (12 criaturas: 6 valientes y 6 prudentes, `informe_P7_47.md:7`). La curva mediana no estaba guardada entera: `analiza_P7_47.py:29-36` guarda la curva de cada criatura solo hasta que cruza 25. Se ha recalculado desde los cuadernos guardados (`P7_47_res/`), con la misma función `creencia_dentro` (`analiza_P7_47.py:13`) y sin cortar en el cruce; no se ha vuelto a ejecutar la réplica. Puerta: lo recalculado coincide, criatura a criatura, con las curvas guardadas en `P7_47_sello.json`. Aquí las pruebas cortadas no cuentan como prueba (`analiza_P7_47.py:5`): **el eje x no cuenta lo mismo en las dos fórmulas** (cortadas incluidas en la antigua, excluidas en la propia).
- La escala propia se dibuja con las 12 criaturas juntas, porque la comprobación da un solo número; por personalidad cruzaría en la prueba 9 (valiente) y 7 (prudente) (no dibujadas; valores en el JSON). P7-47 cambió también la habituación, no solo la escala (`informe_P7_47.md:1`).

| prueba | antigua, prudente (fracción · n) | antigua, valiente | escala propia |
|---|---|---|---|
| 1 | 0,025 · 6 | 0,117 · 6 | 0,176 · 12 |
| 2 | 0,129 · 6 | 0,119 · 6 | 0,237 · 12 |
| 3 | 0,169 · 6 | 0,132 · 6 | 0,298 · 12 |
| 4 | 0,173 · 6 | 0,170 · 6 | 0,387 · 12 |
| 5 | 0,173 · 6 | 0,166 · 6 | 0,396 · 12 |
| 6 | 0,167 · 6 | 0,224 · 6 | 0,397 · 12 |
| 7 | 0,162 · 6 | 0,224 · 6 | 0,397 · 11 |
| 8 | 0,156 · 6 | 0,239 · 6 | 0,548 · 11 |
| 9 | 0,159 · 6 | 0,233 · 6 | 0,800 · 10 |
| 10 | 0,156 · 6 | 0,296 · 6 | 0,644 · 9 |
| 11 | 0,221 · 6 | 0,330 · 6 | 0,788 · 7 |
| 12 | 0,158 · 6 | 0,398 · 6 | 0,788 · 7 |
| 13 | 0,329 · 6 | 0,419 · 6 | 0,781 · 7 |
| 14 | 0,367 · 6 | 0,368 · 6 | 0,806 · 5 |
| 15 | 0,191 · 6 | 0,368 · 6 | 0,778 · 4 |
| 16 | 0,209 · 5 | 0,312 · 6 | 0,787 · 4 |
| 17 | 0,580 · 5 | 0,373 · 6 | 0,730 · 3 |
| 18 | 0,542 · 5 | 0,358 · 6 | — |
| 19 | 0,542 · 5 | 0,337 · 6 | — |
| 20 | 0,542 · 5 | 0,339 · 6 | — |
| 21 | 0,542 · 5 | 0,357 · 6 | — |
| 22 | 0,542 · 5 | 0,331 · 6 | — |
| 23 | 0,542 · 5 | 0,370 · 6 | — |
| 24 | 0,542 · 5 | 0,379 · 6 | — |
| 25 | 0,542 · 5 | 0,356 · 6 | — |
| 26 | 0,410 · 4 | 0,351 · 6 | — |
| 27 | 0,504 · 4 | 0,373 · 6 | — |
| 28 | 0,627 · 3 | 0,376 · 6 | — |
| 29 | — | 0,375 · 6 | — |
| 30 | — | 0,517 · 6 | — |
| 31 | — | 0,441 · 5 | — |
| 32 | — | 0,406 · 4 | — |
| 33 | — | 0,424 · 4 | — |

**Comprobación obligatoria (antigua: cruza la mitad hacia las 17 pruebas en la prudente y las 30 en la valiente; escala propia, hacia las 8 o 9): pasa.** Primera prueba con la mediana en la mitad o por encima: antigua prudente 17, antigua valiente 30 (son los k* de `informe_P7_46.md:119-120`); escala propia 8. El 8,5 de `informe_P7_47.md:17` es otra cuenta, la mediana de las primeras pruebas en cruzar de cada criatura (las que no cruzan, como infinito): 8,5.

## Figura 3.1, revisión: las dos líneas con el eje x contado igual

La figura de la sección anterior se guarda ahora como `fig3_1_es_anterior` y `fig3_1_en_anterior` (mismos bytes que la entregada antes: sus huellas, abajo). `fig3_1_es` y `fig3_1_en` son la versión revisada.

### 1. La fórmula antigua contada solo con las pruebas no cortadas

- Mismos datos (`P7_46_datos.json`, las huellas del botiquín de cada criatura en orden, como `analiza_P7_46.py:93`), pero dejando fuera las pruebas con `corte`; la creencia de cada prueba es la que el cuerpo apuntó tras ella (`creencia_despues`), y la curva es la misma mediana entre criaturas con al menos 3. Puerta: con las cortadas dentro, el mismo cálculo reproduce exactamente la curva guardada en `P7_46_resumen.json`.
- **Contadas así, la mediana cruza la mitad en la prueba 9 en la prudente y en la 10 en la valiente** (antes, con las cortadas contadas, 17 y 30). La escala propia cruza en la 8.
- Pruebas cortadas: prudente 90 de 170; valiente 107 de 193 (las seis criaturas de cada una). Por criatura: prudente s1 a10 7 de 15; prudente s1 a11 13 de 27; prudente s2 a10 17 de 25; prudente s2 a11 21 de 39; prudente s3 a10 12 de 28; prudente s3 a11 20 de 36; valiente s1 a10 22 de 33; valiente s1 a11 9 de 30; valiente s2 a10 19 de 33; valiente s2 a11 15 de 33; valiente s3 a10 21 de 33; valiente s3 a11 21 de 31.
- Salvedad: en el campo, la creencia apuntada tras una prueba cortada no siempre es la de antes (21 de 53 cortadas con creencia apuntada en la prudente y 35 de 73 en la valiente la mueven); el código no se ha mirado para saber por qué (el olvido entre días es una posibilidad, no comprobada). Ese movimiento queda dentro de la creencia de la siguiente prueba no cortada. En P7-47, en cambio, las cortadas no entran en la creencia (`analiza_P7_47.py:5,31`). Las medianas de las dos curvas antiguas se apoyan en pocas criaturas a partir de la prueba 9 (columna n).

| prueba | antigua, prudente, sin cortadas (fracción · n) | antigua, valiente, sin cortadas | escala propia |
|---|---|---|---|
| 1 | 0,124 · 6 | 0,117 · 6 | 0,176 · 12 |
| 2 | 0,153 · 6 | 0,194 · 6 | 0,237 · 12 |
| 3 | 0,175 · 6 | 0,262 · 6 | 0,298 · 12 |
| 4 | 0,242 · 6 | 0,320 · 6 | 0,387 · 12 |
| 5 | 0,203 · 6 | 0,375 · 6 | 0,396 · 12 |
| 6 | 0,339 · 6 | 0,370 · 6 | 0,397 · 12 |
| 7 | 0,318 · 6 | 0,342 · 6 | 0,397 · 11 |
| 8 | 0,424 · 6 | 0,337 · 6 | 0,548 · 11 |
| 9 | 0,664 · 4 | 0,494 · 6 | 0,800 · 10 |
| 10 | 0,662 · 4 | 0,529 · 6 | 0,644 · 9 |
| 11 | 0,679 · 4 | 0,423 · 5 | 0,788 · 7 |
| 12 | 0,679 · 4 | 0,378 · 4 | 0,788 · 7 |
| 13 | 0,660 · 4 | 0,460 · 3 | 0,781 · 7 |
| 14 | 0,472 · 4 | 0,488 · 3 | 0,806 · 5 |
| 15 | 0,695 · 3 | — | 0,778 · 4 |
| 16 | 0,550 · 3 | — | 0,787 · 4 |
| 17 | — | — | 0,730 · 3 |

Consecuencia para la frase del paper («entre diecisiete y treinta pruebas; con su escala, unas ocho o nueve»): con el eje contado igual, la diferencia entre las dos fórmulas casi desaparece (9 y 10 frente a 8). El 17 y el 30 cuentan como prueba las cortadas, que en la fórmula antigua son más de la mitad de las pruebas.

### 2. ¿Puede la habituación cambiar lo que cree que cura el botiquín?

- **Directamente, no.** La habituación solo multiplica la curiosidad: envuelve `filo_P7_40.curiosidad` y la multiplica por el factor h del objeto (`habitua_P7_47.py:2-4,33-36`); su estado es aparte (`habituacion_P7_47`, `habitua_P7_47.py:43,48,75`). La creencia sobre la cura es la media de los efectos vividos pesada por la intensidad y el olvido (`analiza_P7_47.py:13-27`, peso en `:19`), y lo único que P7-47 cambia en el recuerdo es la intensidad (`habitua_P7_47.py:72`). Quien lee la curiosidad decide qué probar («la ignorancia nueva, E1 y los momentos», `habitua_P7_47.py:4`; también `banco_P7_47.py:51`).
- **Indirectamente, sí puede**: al cambiar qué se prueba y cuándo, cambia qué pruebas del botiquín vive la criatura, y con ellas su creencia.
- **En los cuadernos de P7-47 el botiquín no se habituó nunca**: el estado final de habituación de las 12 criaturas solo tiene la red y el camuflaje (APRENDE_v s1 a10: camouflage, net; APRENDE_v s1 a11: net; APRENDE_v s2 a10: camouflage, net; APRENDE_v s2 a11: camouflage, net; APRENDE_v s3 a10: camouflage, net; APRENDE_v s3 a11: camouflage, net; APRENDE_p s1 a10: camouflage, net; APRENDE_p s1 a11: camouflage, net; APRENDE_p s2 a10: camouflage; APRENDE_p s2 a11: camouflage, net; APRENDE_p s3 a10: camouflage, net; APRENDE_p s3 a11: net). Una habituación no se borra del estado (`habitua_P7_47.py:75`), así que el botiquín no tuvo nunca la curiosidad rebajada; la habituación solo pudo influir a través de las otras cosas.
- **¿Se pueden separar los dos cambios sin partidas nuevas?** En parte. Cada recuerdo del botiquín de P7-47 guarda también la intensidad antigua (`intensidad_P7_40`, `habitua_P7_47.py:72`), así que sobre **las mismas pruebas** se puede recalcular la creencia con la fórmula antigua: la mediana cruza la mitad en la prueba 9, frente a 8 con la escala propia (valores en el JSON, no dibujados; 1 recuerdo sin intensidad antigua se deja con la suya). Eso mide el efecto directo de la escala con las pruebas fijas. Lo que no se puede separar sin réplicas nuevas es el efecto de la habituación (y de la escala) sobre qué pruebas se viven: para eso haría falta repetir la cadena con un cambio y no el otro. No se ha intentado.

## Figura 3.1: tres preguntas más (23-oct-2026)

### 1. Qué es `intensidad_P7_40`

- **Es la fórmula antigua, aplicada a los mismos recuerdos de P7-47.** Al cerrar cada prueba sin corte, la pieza de P7-38 en su variante A sin contrafactual pone en el recuerdo `intensidad = 1 + escalar(importancia)` (`contrafactual_P7_38.py:131`), con `escalar = min(1, (|imp cuerpo| + |imp recursos| + |imp vínculo|) / E)` (`contrafactual_P7_38.py:19`) y E = 1,5 (`cuaderno_P7.py:24`): tope 2. Después, la pieza de P7-47 copia ese valor en `intensidad_P7_40` y escribe encima la intensidad en la escala propia (`habitua_P7_47.py:72`; descrito en `:5-7`). Es la fórmula «de P7-40» cuyos cuartiles sobre esos recuerdos son 1,04 · 1,11 · 1,25 (`informe_P7_47.md:25-26`).
- Es la misma fórmula que llevaba el campo P7-45, de donde sale la curva antigua: las dos composiciones ponen P7-38 en variante A sin contrafactual y P7-39 encendido (`campo_P7_41.py:18`; `campo_P7_47.py:21`); P7-47 solo añade la habituación y la escala propia (`campo_P7_47.py:1-2,33`).
- **Qué separa la comparación entre `propia_con_intensidad_P7_40` y la escala propia.** Son las mismas pruebas, las mismas criaturas, el mismo olvido y la misma importancia de cada recuerdo; solo cambia el peso. Las dos dejan fuera las cortadas (`analiza_P7_47.py:31`), así que **contar las cortadas no interviene**. La habituación y la escala ya actuaron sobre qué pruebas se vivieron, y eso es igual en las dos curvas: **la comparación aísla el efecto directo de la escala sobre la creencia, con las pruebas fijas**. No separa el efecto de la escala ni el de la habituación sobre la conducta (qué pruebas llegan a vivirse); para eso haría falta repetir la cadena con un cambio y no el otro.

### 2. Pruebas 11 a 17: las dos curvas y la diferencia criatura a criatura

Creencia del cuerpo sobre lo que cura el botiquín (en vida; la fracción es esto dividido por 50). Diferencia = escala propia − fórmula antigua, en la misma criatura y la misma prueba; ee = sd de las diferencias / √n.

| prueba | n criaturas | mediana, escala propia | mediana, fórmula antigua | diferencia media | ee | ¿mayor que su ee? |
|---|---|---|---|---|---|---|
| 11 | 7 | 39,40 | 31,37 | 4,20 | 1,16 | sí |
| 12 | 7 | 39,40 | 31,37 | 4,40 | 1,13 | sí |
| 13 | 7 | 39,03 | 30,80 | 4,81 | 1,13 | sí |
| 14 | 5 | 40,29 | 34,94 | 6,44 | 1,35 | sí |
| 15 | 4 | 38,91 | 30,80 | 6,58 | 1,76 | sí |
| 16 | 4 | 39,34 | 30,39 | 6,09 | 1,88 | sí |
| 17 | 3 | 36,51 | 26,21 | 6,92 | 2,74 | sí |

Por criatura (media de sus diferencias en las pruebas 11-17 que tiene): APRENDE_p s1 a11 2,70 (3 pruebas); APRENDE_p s2 a11 9,17 (7 pruebas); APRENDE_p s3 a10 6,14 (4 pruebas); APRENDE_p s3 a11 4,85 (6 pruebas); APRENDE_v s1 a11 8,26 (7 pruebas); APRENDE_v s2 a10 0,02 (3 pruebas); APRENDE_v s2 a11 1,96 (7 pruebas).
Entre criaturas: diferencia media 4,73 ± 1,27 (n = 7): mayor que su error típico (3,7 veces). Son pocas criaturas y las mismas en todas las pruebas, que no son independientes entre sí: es una lectura descriptiva, no una prueba sellada.

### 3. La habituación

- La respuesta estaba en la sección «Figura 3.1, revisión», punto 2; aquí, completa.
- **Dónde actúa:** envuelve `filo_P7_40.curiosidad` y la multiplica por el factor h del objeto (`habitua_P7_47.py:33-36`); el factor baja a la mitad tras una prueba sin efecto y no cortada (`habitua_P7_47.py:63,74-75`) y vuelve hacia 1 con el olvido (`habitua_P7_47.py:19-22`). Su estado viaja aparte en el cuaderno, `habituacion_P7_47` (`:43,48`). Fuera de la pieza solo lo leen los guiones de análisis.
- **Lo que cree del botiquín no lo toca directamente:** la creencia es la media de los efectos vividos, pesada por intensidad y olvido (`analiza_P7_47.py:13-27`), y la habituación no escribe ni el efecto ni la intensidad de ningún recuerdo (en `habitua_P7_47.py:61-77` la intensidad la pone la escala, `:72`; la habituación solo toca `E["H"]`, `:75`). Indirectamente sí podría: la curiosidad decide qué se prueba (`habitua_P7_47.py:4`), y con ello qué pruebas del botiquín se viven.
- **El botiquín no se habituó nunca.** No solo en el cuaderno final: en los 240 cuadernos diarios de la cadena (`P7_47_res/`) la habituación solo nombra camouflage (143 cuadernos), net (169 cuadernos), y nunca el botiquín. Como una entrada no se borra una vez puesta (`habitua_P7_47.py:75`) y el estado se lee y se escribe cada día (`:43,48`), la curiosidad por el botiquín no se rebajó nunca.
- **¿Basta eso para decir que no toca lo que cree del botiquín?** Basta para decir que no lo tocó por su vía directa ni rebajó la curiosidad por el botiquín. No basta para descartar el efecto indirecto: al habituarse a la red y al camuflaje, la criatura pudo dedicar a otras cosas el tiempo que antes les daba, y eso puede cambiar cuándo y en qué situación prueba el botiquín. Ese efecto queda dentro de las pruebas, igual en las dos curvas de la comparación del punto 1, y no se puede medir sin réplicas nuevas.

## Huellas sha256

| archivo | sha256 |
|---|---|
| `fig5_2_es.png` | `f0168addfafe119a4e4ef4728265fa8f319be0a929bde0ebf0e54e076911b4fc` |
| `fig5_2_es.pdf` | `01d9f585670bce7a88e819865a59cece07dfa96ca73dbe50e31fd4d363c0e1a4` |
| `fig5_3_es.png` | `6935aca42eb5bda6f1b7bebe772732052d0e5a32c5ae26af470bf0cc3efd8b08` |
| `fig5_3_es.pdf` | `b48cadd931a905fe89096a0f8467d66c4fb6be38cffe23d6351597931e161c6d` |
| `fig3_1_es_anterior.png` | `78d046d69acc79d0969701c3849d22cf4e077ee73133f8533766cdc92e9bfcff` |
| `fig3_1_es_anterior.pdf` | `951bae45124d0a98267e53021880f47bdd46507e9f980a1cdd21772125ec573b` |
| `fig3_1_es.png` | `0e6d15c970ddcb104d70852ea1f9674079d7c94a07b7dd73dece2e5d7f327499` |
| `fig3_1_es.pdf` | `e92e0ff781be640c4837be0c4f46095cde11f134f18a8298b0bdcedf1ab3119d` |
| `fig5_2_en.png` | `654aa77ce16da5491468679bbb1799fd05ff814db68b631d5424023f7115da5b` |
| `fig5_2_en.pdf` | `3bc62751799bbb70c4becce3a02bbfe4b89154c36c09a778907013fb6ec608b5` |
| `fig5_3_en.png` | `2877de9c8a5f0c9df9c088cc38826856da608099cb2ebfe7862842c126b3cdb5` |
| `fig5_3_en.pdf` | `92a9dec0fe78d1ed24ab19eb656b3ffeadcdd7796c4e91c81294aed370abce5b` |
| `fig3_1_en_anterior.png` | `c955f7d976b5443b0050158c29ae7fe1a36444e0570c04b8758982fe8754005b` |
| `fig3_1_en_anterior.pdf` | `5b125271a31312a0abd8b8ef33ed0db96b2ae212125cffe0aeaf744671bce3ab` |
| `fig3_1_en.png` | `f9fd9198bf9c84002dba78c6db0ffd638304c14752f29e3f78b91eab63088624` |
| `fig3_1_en.pdf` | `5c138df0b82abfa223727c1e67a5a425f15704cfde6b5a66815326811c8a8b87` |

Repetible: volver a ejecutar `python3 hace_figuras_P7.py` da los mismos bytes (comprobado dos veces; metadatos de fecha anulados).
