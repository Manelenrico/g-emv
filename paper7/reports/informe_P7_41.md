# P7-41 · Preparar el campo del capítulo 3 (segunda etapa): plan, comprobación y coste

*10-oct-2026. Nada lanzado en la plataforma: plataforma 0 créditos (acumulado del siete 710; disponibles el 10-oct, dato de Manel: 496 de 1.000, +71/día); consola 0 USD.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`; cuerpo y congelados sin tocar. Piezas nuevas del campo: `azar_P7_41.py` (= `9345263e0b1aaa0a71335224fc0abd0a`), `campo_P7_41.py`
(= `291e5cfaf8a80987a59e1330edfb4b62`), `policy_pareja_P7_41.py`, `Dockerfile.pareja_P7_41`, `lanza_P7_41.py`, `semillas_P7_41.json` (propuestas); criatura que aprende = P7-40 tal como quedó
sellado: `filo_P7_40.py` (= `a86ce7d8e53a84aca827dcb521b22b7c`; añadidos de campo: personalidad, caché por tic y apuntes dentro del cuaderno, sin tocar la regla de los apuntes), sobre
B1 de P7-39 (`efecto_P7_39.py` = `f36ea927c5c083f597b5baa20b3d48a7`, `contrafactual_P7_38.py` = `b0efef883215d5046cbfc5db220d0f83` sin contrafactual ni pistas). Comprobación: `banco_P7_41.py` → `P7_41_comprobacion.json`.
Este informe lo escribe `escribe_informe_P7_41.py`; ninguna cifra a mano. **Espera el visto bueno de Manel antes de lanzar.***

## Sección 1 · El diseño

- **Criatura que aprende**: P7-40 sellado (esperanza de clase como punto de partida; cautela por distancia sobre la curiosidad; miradas y apuntes de lo visto en peligro,
  tomados por su mayor, sin tocar). Importancia como B1 (sin las filas de la curiosidad ni las del acto, sin contrafactual); intensidad 1 + importancia; cuaderno que viaja.
- **Brazos** (9 variantes = imágenes): TECHO (nace sabiendo; el miedo no tiene palanca en él: una sola personalidad); BORRADO y APRENDE × {valiente, prudente};
  SIN EMOCIÓN con ε = 0,05 y ε = 0,2 × {valiente, prudente}. Las variantes con cuaderno que viaja (APRENDE y SIN) van en cadena de 20 días; TECHO y BORRADO son fijas.
- **SIN EMOCIÓN** (definiciones propuestas; `azar_P7_41.py`): mismo cuerpo, misma percepción, mismos recuerdos y misma creencia (importancia B1); sin curiosidad
  (`GEMV_P7_NOVEDAD=0`: ni `R-CURIOSIDAD` ni `ir_curioso`), sin esperanza de clase ni apuntes. **Veto**: el cuerpo no coge ni usa por sí solo nada de clase desconocida (sin
  recuerdos) —sin el veto cogería redes por empate, como TECHO en P7-36—. **Oportunidad**: cada vez que una cosa de clase desconocida entra a su alcance (a la vista y sin
  llevarla; o, un consumible desconocido, cuando entra en el zurrón) se tira UNA moneda con probabilidad ε × miedo; una oportunidad por (cosa, casilla) mientras siga a la
  vista, y vuelve a contar si deja de verse 48 tics. **Prueba forzada**: si sale, durante hasta 240 tics va a la cosa (`ir_azar`) y la coge; un consumible desconocido en el
  zurrón se usa en el primer tic en que `usar_*` es candidato. La prueba y su recuerdo son los de P7-33.
- **Personalidades** (PROPUESTA, pendiente: no encuentro en el ACTA ni en los informes los «pesos del miedo como se decidió»; en P7-26 lo que se midió fue la escala de la
  curiosidad ×1/×2 con la cautela): **prudente** = cautela por distancia tal cual (1 sin rivales a 8 o menos; 0 con rival a 2, fuera del círculo o vida < 30; la de P7-40);
  **valiente** = (1 + cautela) / 2 (nunca por debajo de 0,5: el valiente sigue probando cerca del peligro a medias). El mismo factor multiplica la curiosidad de clase en
  APRENDE/BORRADO y la probabilidad ε en SIN EMOCIÓN.
- Lo desconocido: botiquín, ración, red y camuflaje (como P7-33). Ojos compartidos apagados. Pedir corregido y lo dado entregado. Guardas de P7-30.
- **Semillas** (propuestas, se declaran definitivas al lanzar): k = 221-240 (las siguientes a P7-34); serie 1 43406025, …, 45395876; serie 2 en orden inverso; serie 3 rotada diez
  posiciones. La misma semilla para las 9 variantes cada día.

## Sección 2 · Comprobación previa, en local (coste cero)

Réplicas en lazo abierto (las obs son las de los diarios de P7-34, s1 d1 y d10, asientos 10 y 11; lo que cambia es lo que la réplica decide y escribe), una vida por proceso,
con la composición exacta del campo (`campo_P7_41` sobre `nace_P7_33.aplica`). 28 vidas, 0 errores.

| ε | vidas SIN | oportunidades | monedas que salen (fracción real) | ε × miedo (media) | pruebas forzadas (cómo acaban) | vetos (candidatos `coger`/`usar_*` de clase desconocida quitados) | decisiones `coger`/`usar_*` de clase desconocida sin forzar |
|---|---:|---:|---|---|---|---:|---:|
| 0,00 | 4 | 34 | 0 (0,0 %) | 0,000 | 0 (cogida 0, usada 0, caduca 0) | 476 | 0 |
| 0,05 | 4 | 34 | 1 (2,9 %) | 0,031 | 1 (cogida 0, usada 0, caduca 1) | 476 | 0 |
| 0,20 | 8 | 68 | 4 (5,9 %) | 0,142 | 2 (cogida 2, usada 0, caduca 0) | 950 | 0 |

- SIN EMOCIÓN corre; con ε = 0 no hay ninguna prueba de lo desconocido (0 forzadas, 0 decisiones de coger o usar lo desconocido sin forzar; el veto quita los candidatos).
- ε se cumple en la moneda: la fracción real de monedas que salen sigue a ε × miedo dentro de lo que cabe con tan pocas oportunidades (día 1: solo cuentan las cosas aún
  desconocidas; el día 10 el cuaderno ya conoce las cuatro y no hay oportunidades): la moneda es `random.Random(semilla).random() < ε × miedo`, una por oportunidad.
- Latencia: pasa la guarda (≤ 1 % sobre el tic de 41,67 ms): mediana 1,03-3,02 ms, p90 ≤ 6,5 ms, máximo 55,1 ms en 402696 decisiones.

| configuración | vidas | ms por decisión: mediana (máx entre vidas) · p90 (máx) · máximo | fidelidad al diario (suma) |
|---|---:|---|---|
| APRENDE ε=0,00 prudente | 4 | 2,72 · 6,3 · 30,3 | 52135 · 5393 |
| APRENDE ε=0,00 valiente | 4 | 3,02 · 6,4 · 27,9 | 55153 · 2375 |
| BORRADO ε=0,00 prudente | 4 | 2,15 · 6,5 · 29,8 | 49399 · 8129 |
| SIN ε=0,00 prudente | 4 | 1,49 · 5,2 · 19,9 | 40229 · 17299 |
| SIN ε=0,05 prudente | 4 | 1,48 · 5,2 · 55,1 | 40229 · 17299 |
| SIN ε=0,20 prudente | 4 | 1,48 · 5,2 · 32,7 | 40229 · 17299 |
| SIN ε=0,20 valiente | 4 | 1,37 · 4,4 · 19,6 | 40229 · 17299 |

(APRENDE y BORRADO llevan la pieza de P7-40 de campo con la caché por tic; las diferencias con el diario son las esperadas: la curiosidad nueva decide otra cosa.)

## Sección 3 · Las medidas (fijadas) y las predicciones selladas

- **Rapidez**: primer día en que la creencia (dentro, cuerpo, sin cortes) del botiquín llega a 25 (50 % de 50) y la de la ración a 7,5 (50 % de 15); por criatura
  (APRENDE, SIN) o por vida (BORRADO, cada día desde cero); «no llega» cuenta como día 21 (declarado).
- **Sabiduría**: segundos y vida gastados en red y camuflaje en los días 11-20: tics en `ir_curioso`/`ir_azar` hacia red o camuflaje, tics con una ventana de prueba de red o
  camuflaje abierta, y tics llevándolas en el zurrón o puestas, en segundos (÷ 24); vida = puntos de vida perdidos en esos tics. Sin predicción (S1): se informa.
- **Cuándo**: proporción de aperturas de uso del botiquín (`P7_nace_uso`) con la vida por debajo de la mitad (hp < 50); y de la ración «con hambre»: el mundo no tiene
  hambre (sin variable; `informe_P7_38`), PROPUESTA: ración usada con la vida por debajo del máximo (hp < 100), pendiente de Manel.
- **Puesto medio**, como siempre (partidas con corte fuera).
- Predicciones selladas (de la mesa): **R1**: APRENDE llega antes que los dos SIN EMOCIÓN con el botiquín (día de rapidez del botiquín, media de las criaturas de APRENDE
  < la de SIN ε = 0,05 y < la de SIN ε = 0,2, dentro de cada personalidad). **C1**: APRENDE usa el botiquín en necesidad más que los dos SIN EMOCIÓN (proporción de usos
  con hp < 50 mayor). **S1**: sin predicción.

## Sección 4 · Réplicas, ruido y coste

Ruido medido en P7-34 (`P7_34_datos.json`): rapidez del botiquín por criatura, días 11, 7, 2, 21 (APRENDE) y 5, 7, 3, 11 (BORRADO), desviación típica 5,7 días;
usos del botiquín con hp < 50: APRENDE 21,4 % de 140 usos (error típico 3,5 puntos), BORRADO 15,7 % de 108; puesto por vida, desviación típica 4,78; cogidas de red + camuflaje por vida en los
días 11-20: APRENDE 0,93 ± 0,98, TECHO 0,57 ± 0,80.

«Ver diferencias de 3 veces el ruido» = una diferencia entre dos variantes de al menos 3 errores típicos de esa diferencia (√2 × el error típico de cada media):

| diseño | criaturas por variante | vidas por variante | partidas (9 variantes × 20 días × series) | rapidez: error típico · diferencia detectable (días) | puesto: error típico · detectable | cuándo: usos del botiquín por variante · error típico · detectable (puntos) |
|---|---:|---:|---:|---|---|---|
| 2 series | 4 | 80 | 360 | 2,8 · 12,0 | 0,53 · 2,27 | 140 · 3,5 · 14,7 |
| 3 series | 6 | 120 | 540 | 2,3 · 9,8 | 0,44 · 1,85 | 210 · 2,8 · 12,0 |

Lectura: la rapidez es la medida más ruidosa (una por criatura): con 2 series solo se ve una diferencia de 12 días o más entre APRENDE y un SIN EMOCIÓN; con 3 series,
10 días. R1 compara APRENDE con un SIN que explora al azar con ε = 0,05 (una prueba de cada 20 oportunidades, y solo del día 1): si SIN no llega a 25 en 20 días
(día 21), la diferencia esperada es de ~10 días y las dos la ven; con ε = 0,2 puede ser de pocos días y solo la ve la de 3 series. C1 se ve con las dos (diferencias de
15 y 12 puntos). **Propuesta: 3 series = 540 partidas = 540 créditos**; con los 496 disponibles y 71 al día, las series 1 y 2 (360 créditos)
caben hoy y la serie 3 (180) tras 1 días de recarga; la alternativa de 2 series son 360 créditos. Tiempo: las cadenas (6 variantes × series, 20 días a ~16 min por
partida en cadena) ≈ 5,5 h por serie si la plataforma las corre en paralelo (en P7-34 corrió 40 fijas a la vez); las fijas van a la vez.

## Sección 5 · Lo que falta antes de lanzar

1. El visto bueno de Manel sobre: las definiciones de SIN EMOCIÓN (oportunidad, moneda, prueba forzada, veto), las personalidades (pesos del miedo), el «hambre» de la
   ración, las semillas y el número de series.
2. Sello `SELLO_P7_42.md` con las medidas, R1, C1 y S1 y el diseño, commit antes de pedir ninguna partida.
3. Humo de 3 partidas (día 1 de APRENDE_p, SIN20_p y TECHO) para probar las imágenes y el lanzador en la plataforma (`lanza_P7_41.py` está preparado, no probado):
   3 créditos.
4. Freno como en P7-34 (días 1-3 de APRENDE_p) y el campo.
