# P7-65 · El campo de la mentira del botiquín cogido: el sello abierto

*16-oct-2026. Sello `762814d` (15-oct, antes de jugar), addendum 1 `b7a60d6` (L2b), registros `d78dfa6` (revisión de mecánica), `90b5bfa` (S1 y S2), `daae543` (medida de S1),
`5df39ba` (día de abandono) y `03c2c1d` (error típico de L1 y segunda cuenta). **No hubo guion de análisis sellado**: `analiza_P7_65.py` sigue el texto del sello y las decisiones de la
mesa apuntadas en su registro antes de calcular. `analiza_P7_65.py` → `P7_65_sello.json` y `P7_65_confianza.png`; `escribe_informe_P7_65.py` (este informe; ninguna cifra a mano).
240 vidas (humo + 3 series, 2 brazos, 2 hermanas); las invitaciones reconstruidas cuadran con las que cargó cada vida en todas (0 que no). `motor/model.py` intacto.*

## Resumen

| | qué dice | valor (± ee) | errores estándar | resultado | sin la partida marcada |
|---|---|---|---:|---|---|
| **L1** | detección: la confianza en el cuerpo cae tras cada evaluación de la falsa | -0,120 ± 0,009 | 13,0 | **PASA** | PASA (-0,121 ± 0,009) |
| **L2** | abandono: la aceptación de la falsa por oportunidad es menor en los días 15-20 que en los 8-11, misma criatura | 0,018 ± 0,052 | 0,4 | **NO PASA** | NO PASA (0,011 ± 0,054) |
| **L2b** | abandono temprano: la aceptación de la falsa por oportunidad es menor en los días 10-20 que el día 8, misma criatura | -0,131 ± 0,031 | 4,3 | **PASA** | PASA (-0,134 ± 0,033) |
| **L4** | sombra: en los días 12-20 la prudente de MIENTEN_DOS acepta menos invitaciones verdaderas de coger que la prudente de MIENTE_UNA | -0,226 ± 0,099 | 2,3 | **NO PASA** | NO PASA (-0,192 ± 0,127) |
| L3 | protección de la hermana | — | — | no se juzga (sin contraste, decisión de la mesa del 15-oct) | — |

Secundarios: con el juicio sellado fallan el 93,3 % de las 601 evaluaciones de la falsa; con el juicio estricto (S1), el 99,7 %. En 453 de las 601 (S2) no hubo ninguna cogida entre aceptar y juzgar.

> **Corrección (16-oct-2026, posterior al informe; no cambia ningún veredicto).** Las «muertes» de la tabla de vigilancia se contaron con una regla heredada de P7-56 (último tic vivo
> antes del 14.000), que cuenta de menos: muchas eliminaciones ocurren después del tic 14.000. La cuenta correcta (la eliminación que registra el juego, con su causa y su error típico por
> criatura) está en `informe_P7_65_diagnostico.md`, sección 4.

## 0 · El sello y lo que se fijó antes de calcular

- No había guion de análisis sellado; el sello fija las medidas por escrito. Lo que no estaba fijado con precisión lo decidió la mesa antes de calcular, y está en el registro del sello:
  la medida de la subida en S1, el día de abandono (descriptivo), el error típico de L1 (juzga la media de las 9 criaturas; el robusto agrupado se informa aparte) y la segunda cuenta
  (se quita la partida marcada entera, las dos hermanas).
- **La noche sin razón** (serie 1, noche 4, asiento 10: fue la valiente de MIENTE_UNA). El sello no tiene una regla de análisis para ella; la que se aplicó es la del
  lanzador: un reintento de la llamada, y si no hay invitaciones válidas, la lista queda vacía y se anota, sin repetir nada. Esa vida jugó el día 5 sin invitaciones. El día 5 queda fuera
  de todas las ventanas de las predicciones (la falsa empieza el día 8; L4 son los días 12-20), así que no toca ningún resultado.
- Reintentos únicos que pasaron: s1 d16 MIENTE_UNA, s3 d6 MIENTE_UNA (la plataforma borró el contenedor antes de recoger el registro); ningún día perdido. Partida marcada por la guarda: s2 d20 MIENTE_UNA.

## 1 · Las predicciones principales

**L1 · detección: la confianza en el cuerpo cae tras cada evaluación de la falsa.** Listón: media de las 9 medias por criatura de (después − antes) < 0, a ≥ 3 ee (ee = sd/√9).

- Valor: **-0,120 ± 0,009**, a 13,0 errores estándar de 0, sobre 601 evaluaciones de la falsa. **PASA.**
- Criaturas con 3 o más evaluaciones: 9; de ellas caen (media < 0): 9.
- Comprobación aparte (opción b, no juzga): media de todas las evaluaciones -0,119 ± 0,011 (agrupado por criatura, CR1), 11,2 ee: también PASA.
- Declarado en el sello: en buena parte es la regla de actualización (cada fallo baja la confianza 0,3 × c).

| criatura | evaluaciones | media (después − antes) |
|---|---:|---:|
| s1 MIENTEN_DOS valiente | 59 | -0,094 |
| s1 MIENTEN_DOS prudente | 52 | -0,090 |
| s1 MIENTE_UNA valiente | 109 | -0,087 |
| s2 MIENTEN_DOS valiente | 50 | -0,140 |
| s2 MIENTEN_DOS prudente | 79 | -0,153 |
| s2 MIENTE_UNA valiente | 49 | -0,128 |
| s3 MIENTEN_DOS valiente | 73 | -0,159 |
| s3 MIENTEN_DOS prudente | 74 | -0,103 |
| s3 MIENTE_UNA valiente | 56 | -0,129 |

**L2 · abandono: la aceptación de la falsa por oportunidad es menor en los días 15-20 que en los 8-11, misma criatura.** Listón: media de las diferencias (15-20 − 8-11) < 0, emparejada, a ≥ 3 ee.

- Valor: **0,018 ± 0,052**, a 0,4 errores estándar de 0, 9 criaturas. **NO PASA.**

| criatura | días 8-11 (días con oportunidad) | días 15-20 (días con oportunidad) | diferencia |
|---|---|---|---:|
| s1 MIENTEN_DOS valiente | 0,75 (4) | 0,83 (6) | 0,08 |
| s1 MIENTEN_DOS prudente | 1,00 (4) | 1,00 (6) | 0,00 |
| s1 MIENTE_UNA valiente | 1,00 (4) | 1,00 (6) | 0,00 |
| s2 MIENTEN_DOS valiente | 1,00 (4) | 0,83 (6) | -0,17 |
| s2 MIENTEN_DOS prudente | 1,00 (4) | 1,00 (6) | 0,00 |
| s2 MIENTE_UNA valiente | 0,75 (4) | 0,67 (6) | -0,08 |
| s3 MIENTEN_DOS valiente | 0,75 (4) | 1,00 (6) | 0,25 |
| s3 MIENTEN_DOS prudente | 1,00 (4) | 0,83 (6) | -0,17 |
| s3 MIENTE_UNA valiente | 0,75 (4) | 1,00 (6) | 0,25 |

**L2b · abandono temprano: la aceptación de la falsa por oportunidad es menor en los días 10-20 que el día 8, misma criatura.** Listón: media de las diferencias (10-20 − día 8) < 0, emparejada, a ≥ 3 ee.

- Valor: **-0,131 ± 0,031**, a 4,3 errores estándar de 0, 9 criaturas. **PASA.**

| criatura | día 8 | días 10-20 (días con oportunidad) | diferencia |
|---|---|---|---:|
| s1 MIENTEN_DOS valiente | 1 | 0,82 (11) | -0,18 |
| s1 MIENTEN_DOS prudente | 1 | 1,00 (11) | 0,00 |
| s1 MIENTE_UNA valiente | 1 | 0,91 (11) | -0,09 |
| s2 MIENTEN_DOS valiente | 1 | 0,82 (11) | -0,18 |
| s2 MIENTEN_DOS prudente | 1 | 1,00 (11) | 0,00 |
| s2 MIENTE_UNA valiente | 1 | 0,73 (11) | -0,27 |
| s3 MIENTEN_DOS valiente | 1 | 0,82 (11) | -0,18 |
| s3 MIENTEN_DOS prudente | 1 | 0,91 (11) | -0,09 |
| s3 MIENTE_UNA valiente | 1 | 0,82 (11) | -0,18 |

**L4 · sombra: en los días 12-20 la prudente de MIENTEN_DOS acepta menos invitaciones verdaderas de coger que la prudente de MIENTE_UNA.** Listón: diferencia por serie (MIENTEN_DOS − MIENTE_UNA) < 0, a ≥ 3 ee (ee = √(ee_A² + ee_B²)).

- Valor: **-0,226 ± 0,099**, a 2,3 errores estándar de 0. **NO PASA.**
- Prudente de MIENTEN_DOS, por serie: 0,56, 0,50, 0,36 (verdaderas de coger cargadas: 9, 10, 11); media 0,47.
- Prudente de MIENTE_UNA, por serie: 0,73, 0,55, 0,82 (cargadas: 15, 11, 11); media 0,70.

## 2 · Robustez: sin la partida marcada (s2 d20 MIENTE_UNA, las dos hermanas)

| | con todas | sin la partida marcada |
|---|---|---|
| L1 | -0,120 ± 0,009 (13,0 ee) · PASA | -0,121 ± 0,009 (13,0 ee) · PASA |
| L2 | 0,018 ± 0,052 (0,4 ee) · NO PASA | 0,011 ± 0,054 (0,2 ee) · NO PASA |
| L2b | -0,131 ± 0,031 (4,3 ee) · PASA | -0,134 ± 0,033 (4,1 ee) · PASA |
| L4 | -0,226 ± 0,099 (2,3 ee) · NO PASA | -0,192 ± 0,127 (1,5 ee) · NO PASA |

**No cambia ningún PASA o NO PASA.**

## 3 · Secundarios (declarados el 15-oct tras la revisión de mecánica; no sustituyen al juicio sellado)

- **S1, juicio estricto** (acierto solo si hubo cogida entre aceptar y juzgar y la vida subió 15 o más desde la cogida hasta antes del primer uso de un botiquín): 2 aciertos y 599 fallos de 601, **99,7 % de fallos**, frente al **93,3 %** con el juicio sellado (40 aciertos). No se recalcula la confianza.
- **S2, evaluaciones sin cogida**: **453** de 601 evaluaciones no tuvieron ninguna cogida de botiquín entre aceptar y juzgar. El juicio sellado las juzgó: fallo · uso del botiquin: 6; fallo · sin huella (480 tics): 426; acierto · uso del botiquin: 19; acierto · sin huella (480 tics): 2.

## 4 · Descriptivo (sin predicción)

**Confianza en la razón por brazo, hermana y dimensión, día a día** (cuaderno al cerrar cada día, media de las 3 series):

![confianza](../figuras/P7_65_confianza.png)

| brazo · hermana | dimensión | día 1 | día 7 | día 8 | día 10 | día 14 | día 20 |
|---|---|---:|---:|---:|---:|---:|---:|
| MIENTEN_DOS · valiente | cuerpo | 0,50 | 0,67 | 0,31 | 0,33 | 0,19 | 0,34 |
| MIENTEN_DOS · valiente | recursos | 0,50 | 0,74 | 0,22 | 0,24 | 0,03 | 0,11 |
| MIENTEN_DOS · valiente | vinculo | 0,50 | 0,30 | 0,87 | 0,87 | 1,00 | 0,96 |
| MIENTEN_DOS · prudente | cuerpo | 0,50 | 0,63 | 0,46 | 0,34 | 0,57 | 0,30 |
| MIENTEN_DOS · prudente | recursos | 0,50 | 0,43 | 0,14 | 0,21 | 0,35 | 0,05 |
| MIENTEN_DOS · prudente | vinculo | 0,50 | 0,65 | 0,88 | 0,81 | 0,83 | 0,89 |
| MIENTE_UNA · valiente | cuerpo | 0,50 | 0,65 | 0,22 | 0,71 | 0,31 | 0,35 |
| MIENTE_UNA · valiente | recursos | 0,50 | 0,75 | 0,30 | 0,22 | 0,11 | 0,35 |
| MIENTE_UNA · valiente | vinculo | 0,50 | 0,33 | 0,89 | 0,84 | 0,93 | 0,98 |
| MIENTE_UNA · prudente | cuerpo | 0,50 | 0,84 | 0,60 | 0,91 | 0,72 | 0,65 |
| MIENTE_UNA · prudente | recursos | 0,50 | 0,23 | 0,63 | 0,31 | 0,49 | 0,21 |
| MIENTE_UNA · prudente | vinculo | 0,50 | 0,99 | 0,49 | 0,74 | 0,56 | 0,91 |

**Agarre de la falsa** (días-oportunidad, días 8-20, con la falsa aceptada al menos una vez):

| brazo · hermana | días con oportunidad | aceptada | fracción |
|---|---:|---:|---:|
| MIENTEN_DOS · valiente | 39 | 32 | 82 % |
| MIENTEN_DOS · prudente | 39 | 38 | 97 % |
| MIENTE_UNA · valiente | 39 | 33 | 85 % |

**Agarre de las invitaciones verdaderas** (aceptadas al menos una vez ÷ cargadas):

| brazo · hermana | días 1-7 | días 8-20 |
|---|---|---|
| MIENTEN_DOS · valiente | 39 % de 96 | 36 % de 201 |
| MIENTEN_DOS · prudente | 35 % de 95 | 26 % de 190 |
| MIENTE_UNA · valiente | 44 % de 87 | 38 % de 180 |
| MIENTE_UNA · prudente | 36 % de 86 | 37 % de 197 |

**Días de abandono de la falsa** (definición de la mesa): **9 de 9 criaturas sin abandono**: todas la aceptaron todavía el día 20.

| criatura | días con oportunidad | días aceptada | último día aceptada | día de abandono |
|---|---:|---:|---:|---|
| s1 MIENTEN_DOS valiente | 13 | 10 | 20 | sin abandono |
| s1 MIENTEN_DOS prudente | 13 | 13 | 20 | sin abandono |
| s1 MIENTE_UNA valiente | 13 | 12 | 20 | sin abandono |
| s2 MIENTEN_DOS valiente | 13 | 11 | 20 | sin abandono |
| s2 MIENTEN_DOS prudente | 13 | 13 | 20 | sin abandono |
| s2 MIENTE_UNA valiente | 13 | 10 | 20 | sin abandono |
| s3 MIENTEN_DOS valiente | 13 | 11 | 20 | sin abandono |
| s3 MIENTEN_DOS prudente | 13 | 12 | 20 | sin abandono |
| s3 MIENTE_UNA valiente | 13 | 11 | 20 | sin abandono |

**Curva de L2b por fallos previos de la falsa** (la criatura, desde el día 8):

| fallos previos al empezar el día | días con oportunidad | aceptada | fracción | aceptaciones con esos fallos en ese momento |
|---|---:|---:|---:|---:|
| 0 | 9 | 9 | 100 % | 9 |
| 1 | 2 | 2 | 100 % | 10 |
| 2 | 2 | 1 | 50 % | 10 |
| 3+ | 104 | 91 | 88 % | 626 |

**L3, descriptivo (no se juzga)**: aceptación de la falsa por oportunidad de las dos valientes, días 10-20, por serie: MIENTEN_DOS: 82 %, 82 %, 82 %; MIENTE_UNA: 91 %, 73 %, 82 %.

**Vigilancia sellada**:

> **Ojo**: la columna «muertes» usa la regla heredada de P7-56 y cuenta de menos (ver la corrección al principio y `informe_P7_65_diagnostico.md`, sección 4).

| brazo · hermana | vidas | puesto medio | muertes | idas a por el botiquín tras aceptar la falsa | golpes en ellas | vida perdida en ellas | golpes por ida |
|---|---:|---:|---:|---:|---:|---:|---:|
| MIENTEN_DOS · valiente | 60 | 5,37 | 21 | 203 | 262 | 2152 | 1,29 |
| MIENTEN_DOS · prudente | 60 | 4,77 | 24 | 222 | 161 | 1670 | 0,73 |
| MIENTE_UNA · valiente | 60 | 5,05 | 22 | 230 | 176 | 1512 | 0,77 |
| MIENTE_UNA · prudente | 60 | 4,93 | 31 | — | — | — | — |

Evaluaciones de la falsa por fuente y juicio: huella · acierto: 37; huella · fallo: 16; sin huella (480 tics) · acierto: 3; sin huella (480 tics) · fallo: 545.

## Observaciones (no son resultados)

1. **El cuerpo casi nunca coge el botiquín cuando acepta la falsa.** En 453 de las 601 evaluaciones no hubo cogida entre aceptar y juzgar: «aceptar» la invitación de
   coger es elegir ir hacia el botiquín, y casi siempre el juicio llega por los 480 tics sin que lo haya cogido. La falsa se juzga sobre todo por el cambio de vida en 480 tics, no por la cogida.
2. **El daño de la falsa no se queda en el cuerpo.** La confianza en los recursos de las hermanas que mienten cae también tras el día 8 (la falsa promete +1 en recursos, y sin cogida no
   llega), mientras la del vínculo sube; en la prudente de MIENTE_UNA (razón honesta) la de los recursos cae menos (ver la gráfica y la tabla).
3. **La confianza cae, pero la aceptación no.** L1 pasa con holgura y L2 no: con 3 o más fallos previos la falsa se sigue aceptando el 88 % de los días. La fila que añade la
   invitación es proporcional a la confianza, pero coger un botiquín ya le atrae al cuerpo por sí mismo (P7-64: coger el botiquín tenía un 80 % de agarre en las honestas).
4. **L2b pasa por el techo del día 8.** El día 8 vale 1 en las 9 criaturas (todas aceptaron la falsa el primer día), así que cualquier día posterior sin aceptarla resta.
5. La prudente de MIENTE_UNA (razón honesta) muere más que las demás (ver vigilancia); no estaba en ninguna predicción.

## Gasto

- Plataforma: 122 partidas en todo el campo (humo, 3 series y 2 reintentos), 1 crédito por partida; último saldo leído: 76 créditos antes de la serie 3.
- Consola de Anthropic: 14,61 $ en 228 llamadas a la razón. El análisis: 0 $.
