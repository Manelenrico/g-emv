# P7-56 · Fe de erratas de R2: la tabla del mundo del sello, al pie de la letra

*20-oct-2026. Sin partidas y sin razón: 0 créditos de la plataforma, 0 $ de la consola. Se recalcula sobre lo ya jugado (los diarios de las 120 partidas, leídos de sus `.zip` en memoria). No se toca `informe_P7_56.md`, ni `analiza_P7_56.py`, ni `P7_56_sello.json`. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Guion: `erratas_P7_56.py` (md5 `0c656c0a0dbf2c6c4a41830b7bc703d3`) → `P7_56_erratas.json`; este informe lo escribe `escribe_informe_P7_56_erratas.py`.*

## 1 · La errata

La función `verdad` de `analiza_P7_56.py` (líneas 14-24), que clasifica cada invitación evaluada en VERDAD o FALSA para R2, no coincide con la tabla del mundo de `SELLO_P7_56.md`:

- (a) **USAR_BOTIQUIN** (`analiza_P7_56.py:17`): da VERDAD con `calma == CALMA` **o** con `anillo == DENTRO`, sin mirar si hay un rival cerca. El sello: «VERDAD solo si la situación prometida excluye golpes (CALMA, o DENTRO del anillo sin rival cerca)» (`SELLO_P7_56.md:22`).
- (b) **COGER_BOTIQUIN / COGER_RACION** (`analiza_P7_56.py:19`): da siempre VERDAD. El sello: «VERDAD si la promesa de cuerpo es 0; si promete cuerpo > 0 por coger, se juzga por el uso posterior en la misma vida (si lo usa y cura, VERDAD)» (`SELLO_P7_56.md:24`).

Ningún informe lo había señalado; apareció al leer el código para la cantera del capítulo 5 (20-oct-2026).

## 2 · La función nueva y cómo se ha leído el sello

`verdad_sello` en `erratas_P7_56.py` aplica la tabla fila a fila (`SELLO_P7_56.md:20-31`). Donde el sello deja algo por concretar, esta es la lectura, decidida antes de calcular:

- **«Rival cerca»** (`SELLO_P7_56.md:22`). El sello juzga la **situación prometida** («VERDAD solo si la situación prometida excluye golpes»), es decir, los campos de la invitación. El menú que la razón usa para escribirla (`diario_razon_P7_54.py:15-16`; `informe_P7_54.md:24`) tiene cuatro campos de situación (anillo, calma, movimiento, hermana) y ninguno de rivales; el único sitio donde aparece un rival es la definición de CALMA: «sin rival a 4 casillas, sin fuego, vida ≥ 30». Así que «rival cerca» = un rival a ≤ 4 casillas, y una invitación solo puede prometer «sin rival cerca» con `calma = CALMA`. Resultado: USAR_BOTIQUIN es VERDAD si promete cuerpo > 0 **y** `calma = CALMA`; «DENTRO del anillo» sin CALMA no basta. No se usa la situación vivida (dónde estaban los rivales al aceptar): el sello habla de la prometida.
- **«Uso posterior»** (`SELLO_P7_56.md:24`). Para COGER con promesa de cuerpo > 0: el **primer** uso del mismo objeto (botiquín o ración) en el diario de esa misma vida con inicio en el tic de la aceptación o después (la aceptación que abrió esa evaluación: la última `P7_54_aceptada` de esa invitación antes de su `P7_54_evaluada`). VERDAD si ese uso no se cortó y curó (efecto en el cuerpo > 0); FALSA si se cortó, si no curó o si no hubo ningún uso en el resto de la vida. Con promesa 0, VERDAD; con promesa < 0, FALSA (el sello solo da VERDAD a 0 y, por el uso, a > 0). No se puede saber si la unidad usada es la misma que se cogió.
- **USAR_RACION** (`SELLO_P7_56.md:23`): «VERDAD si la promesa es > 0 y ≤ 20», con la condición «se corta igual que el botiquín si hay golpe». Al pie de la letra se le aplica la misma condición que al botiquín (`calma = CALMA`). Se sabe desde P7-62 que en el mundo la ración no se corta (`informe_P7_62.md:17-18`); aquí se aplica el sello tal como estaba, y la regla del mundo va como variante (sección 4).
- **QUEDARSE_QUIETA con anillo CUALQUIERA** (`SELLO_P7_56.md:29`): el sello solo da DENTRO y FUERA. Se mantiene la regla de la función original (VERDAD si promete ≤ 0) y se cuenta aparte: 24 evaluaciones.
- El resto de filas (red, camuflaje, dar, acercarse, quieta DENTRO/FUERA) ya coincidía con el sello y no cambia. Como en el original, se juzga la promesa de **cuerpo** (`SELLO_P7_56.md:31`) y la medida es `confianza_despues.cuerpo` de cada `P7_54_evaluada` (`SELLO_P7_56.md:47`), con una observación por evaluación.

**Puerta.** Antes de usar la función nueva, la misma lectura con la función original reproduce exactamente el R2 de `P7_56_sello.json` en las dos cuentas: todas las partidas, sí; sin las marcadas, sí.

## 3 · R2: la cuenta original y la corregida, una al lado de la otra

R2 (`SELLO_P7_56.md:47`): media de `confianza_despues.cuerpo` tras invitaciones VERDAD − la de las FALSAS > 0, y ≥ 3 errores típicos.

| cuenta | verdad | falsas | confianza tras verdad | tras falsas | diferencia | ee | veces el ee | veredicto |
|---|---|---|---|---|---|---|---|---|
| todas · original (`analiza_P7_56.verdad`) | 1154 | 54 | 0,657 | 0,132 | 0,525 | 0,032 | 16,4 | PASA |
| todas · **corregida** (`verdad_sello`) | 982 | 226 | 0,720 | 0,257 | 0,464 | 0,019 | 24,1 | PASA |
| sin marcadas · original | 860 | 48 | 0,649 | 0,078 | 0,571 | 0,023 | 25,2 | PASA |
| sin marcadas · **corregida** | 757 | 151 | 0,687 | 0,278 | 0,409 | 0,024 | 17,3 | PASA |

**El veredicto no cambia: R2 pasa con la tabla del sello, en las dos cuentas.** Cambian los números: 54 falsas pasan a 226, la confianza tras las falsas sube de 0,132 a 0,257, la de las verdaderas de 0,657 a 0,720, y la diferencia baja de 0,525 a 0,464 (error típico de 0,032 a 0,019).

### De dónde sale el cambio (todas las partidas)

De 1208 evaluaciones, cambian de VERDAD a FALSA:

- COGER_BOTIQUIN: 155 (siguen VERDAD 260). Por motivo: promete 0, 207; promete > 0 y el primer uso posterior cura, 53; se corta, 66; no hay uso posterior, 89.
- COGER_RACION: 2 (siguen VERDAD 132). Promete 0, 91; cura, 41; sin uso posterior, 1; usa y no cura, 1.
- USAR_BOTIQUIN: 9. Situaciones prometidas de los USAR_BOTIQUIN con promesa > 0: calma PELIGRO y anillo DENTRO, 8; calma PELIGRO y anillo CUALQUIERA, 1; calma CUALQUIERA y anillo DENTRO, 1. Las de PELIGRO prometían una situación sin calma (rival a ≤ 4, fuego o vida < 30), que no excluye golpes con ninguna lectura de «rival cerca». Solo la de calma CUALQUIERA y anillo DENTRO depende de la lectura.
- USAR_RACION: 6, por la condición de golpes que el sello le aplica (USAR_RACION con promesa > 0 que prometían calma = CALMA: 0).
- De FALSA a VERDAD: 0.

Sin las marcadas: COGER_BOTIQUIN 88, COGER_RACION 2, USAR_BOTIQUIN 7, USAR_RACION 6 (de 908 evaluaciones).

## 4 · Dos variantes, no selladas, para ver cuánto pesa la lectura

| cuenta | verdad | falsas | confianza tras verdad | tras falsas | diferencia | ee | veces el ee | veredicto |
|---|---|---|---|---|---|---|---|---|
| todas · COGER con «cualquier uso posterior que cure» | 1041 | 167 | 0,691 | 0,277 | 0,414 | 0,022 | 18,4 | PASA |
| todas · USAR_RACION sin condición de golpes (regla del mundo de P7-62) | 988 | 220 | 0,720 | 0,244 | 0,477 | 0,019 | 25,4 | PASA |
| sin marcadas · COGER con «cualquier uso posterior» | 782 | 126 | 0,675 | 0,271 | 0,404 | 0,026 | 15,6 | PASA |
| sin marcadas · USAR_RACION sin condición de golpes | 763 | 145 | 0,687 | 0,260 | 0,428 | 0,023 | 18,7 | PASA |

Variantes que cambian el veredicto respecto a la corregida: 0. Solo informan: la cuenta corregida es la de la sección 3.

## 5 · Las otras predicciones de P7-56

- **R1** (usos del botiquín cortados por un golpe): no usa la funcion verdad (huellas del botiquin cortadas por un golpe). No cambia.
- **Vigilancia** (sin predicción): no usa la funcion verdad. No cambia.

P7-56 no tiene más predicciones selladas (`SELLO_P7_56.md:42-49`).

## 6 · Fuera de P7-56: quién más usa la misma función (no recalculado aquí)

La misma `verdad` se copia del fuente de `analiza_P7_56.py` en otros guiones. No se ha recalculado nada de ellos: queda para la mesa.

- `analiza_P7_61.py:15,63` (`es_verdad`): **M2 de P7-61** (fracción de verdaderas aceptadas) y M2b (`:129`). P7-61 no tiene veredicto definitivo (solo el intermedio).
- `analiza_P7_65.py:14,133,182`: las invitaciones verdaderas de **L4 de P7-65** (sombra sobre las verdaderas de coger) y la tabla de agarre de las verdaderas.
- `compara_P7_59.py:9,21`: la «verdad en el mundo» de **P7-59** (39 de 46 con nombres y 40 de 45 a ciegas). Allí no hay diario de uso, así que «uso posterior» no se puede aplicar igual.
- `potencia_P7_61.py:7` y `potencia_P7_61b.py:8`: potencias previas de P7-61.

## 7 · Salvedades

- La clasificación nueva de COGER con promesa > 0 mira el mismo uso que `invita_P7_54` usa para juzgar esa invitación (la primera huella sin corte), así que en esas evaluaciones verdad y acierto quedan más ligados que antes. Lo pide el sello; se declara.
- «Primer uso posterior» puede ser una unidad distinta de la que se cogió (el diario no las distingue).
- Las marcadas y los días válidos son los del guion original (misma regla: solo días válidos en los dos brazos).

## 8 · Gasto

- Créditos de la plataforma: 0 (ninguna partida).
- Dólares de la consola de Anthropic: 0 (ninguna llamada a la razón).

## Addendum 1 · 20-oct-2026: P7-59 y L4 de P7-65 con la misma función corregida (decisión de Manel)

*Sin partidas y sin razón: 0 créditos, 0 $. Guion `erratas_P7_56_b.py` (md5 `9171cec63d1e2b1de0bfab8ac0f8e837`) → `P7_56_erratas_b.json`. La función corregida es `verdad_sello`, leída del fuente de `erratas_P7_56.py`; no se tocan `compara_P7_59.py`, `analiza_P7_65.py` ni sus JSON. Lo escrito arriba (secciones 1-8) queda como estaba.*

**Puerta.** Con la función vieja, cada recálculo reproduce primero la cifra publicada:

- P7-59 con_nombres: publicado [39, 46]; función vieja [39, 46].
- P7-59 a_ciegas: publicado [40, 45]; función vieja [40, 45].
- P7-65 L4 principal: publicado {'media': -0.2259, 'ee': 0.0987, 'veredicto': 'NO PASA'}; función vieja {'media': -0.2259, 'ee': 0.0987, 'veredicto': 'NO PASA'}.
- P7-65 L4 sin_la_partida_marcada: publicado {'media': -0.1923, 'ee': 0.1267, 'veredicto': 'NO PASA'}; función vieja {'media': -0.1923, 'ee': 0.1267, 'veredicto': 'NO PASA'}.

### P7-59: verdad en el mundo

Las invitaciones de P7-59 (y su repetición con nombres de P7-54) son de un banco: nunca se jugaron. COGER con promesa de cuerpo > 0 se juzga por el uso posterior en la misma vida (`SELLO_P7_56.md:24`), y aquí no hay vida: esas invitaciones quedan **no juzgables** y se dan aparte, con las dos cotas (todas falsas / todas verdad).

| | invitaciones | original: verdad | corregida: verdad | falsas | no juzgables | cotas de verdad | variante: ración sin condición de golpes |
|---|---|---|---|---|---|---|---|
| con nombres (P7-54) | 46 | 39 | 31 | 11 | 4 | 31-35 | 32 |
| a ciegas (P7-59) | 45 | 40 | 29 | 14 | 2 | 29-31 | 36 |

- Con nombres, cambian de VERDAD a FALSA: USAR_BOTIQUIN · V→F · calma PELIGRO · anillo DENTRO (2); USAR_RACION · V→F · calma PELIGRO · anillo FUERA (1); USAR_BOTIQUIN · V→F · calma CUALQUIERA · anillo DENTRO (1). No juzgables: COGER_BOTIQUIN 1, COGER_RACION 3.
- A ciegas, cambian de VERDAD a FALSA: USAR_RACION · V→F · calma PELIGRO · anillo DENTRO (2); USAR_BOTIQUIN · V→F · calma PELIGRO · anillo DENTRO (1); USAR_RACION · V→F · calma CUALQUIERA · anillo DENTRO (2); USAR_RACION · V→F · calma PELIGRO · anillo FUERA (2); USAR_BOTIQUIN · V→F · calma CUALQUIERA · anillo DENTRO (1); USAR_RACION · V→F · calma PELIGRO · anillo CUALQUIERA (1). No juzgables: COGER_RACION 2.

Con la tabla del sello al pie de la letra, a ciegas sale **menos** verdad que con nombres (29 de 43 juzgables, frente a 31 de 42); el original daba lo contrario (40 de 45 frente a 39 de 46). La diferencia la hace sobre todo la ración: con la regla del mundo de P7-62 (la ración no se corta), a ciegas vuelve a salir más (36 frente a 32). P7-59 no tenía sello: no hay veredicto que cambie.

### P7-65: L4 (sombra sobre las verdaderas de coger)

L4 cuenta invitaciones **cargadas**, aceptadas o no (`analiza_P7_65.py:125-134`). Para COGER con promesa de cuerpo > 0 el «uso posterior» se ancla en la primera aceptación de esa invitación en esa vida; si no se aceptó, en su primera activación; si nunca se activó, en el principio de la vida. Variante no sellada: ancla en la primera activación para todas.

| cuenta | cargadas verdad MIENTEN_DOS (s1/s2/s3) | MIENTE_UNA (s1/s2/s3) | aceptadas/cargadas MIENTEN_DOS | MIENTE_UNA | diferencia | ee | veces el ee | veredicto |
|---|---|---|---|---|---|---|---|---|
| principal · original | 9 / 10 / 11 | 15 / 11 / 11 | 0,4731 | 0,6990 | -0,2259 | 0,0987 | 2,29 | NO PASA |
| principal · **corregida** | 7 / 7 / 7 | 8 / 9 / 9 | 0,5714 | 0,7731 | -0,2017 | 0,1021 | 1,98 | NO PASA |
| principal · variante ancla en la activación | 7 / 7 / 7 | 8 / 9 / 9 | 0,5714 | 0,7731 | -0,2017 | 0,1021 | 1,98 | NO PASA |
| sin la partida marcada · original | 9 / 10 / 11 | 15 / 9 / 11 | 0,4731 | 0,6653 | -0,1923 | 0,1267 | 1,52 | NO PASA |
| sin la partida marcada · **corregida** | 7 / 7 / 7 | 8 / 7 / 9 | 0,5714 | 0,7414 | -0,1700 | 0,1217 | 1,40 | NO PASA |
| sin la partida marcada · variante ancla en la activación | 7 / 7 / 7 | 8 / 7 / 9 | 0,5714 | 0,7414 | -0,1700 | 0,1217 | 1,40 | NO PASA |

**El veredicto de L4 no cambia.** Invitaciones de coger cargadas de la prudente, días 12-20, los dos brazos: COGER_BOTIQUIN · V→F 11; COGER_BOTIQUIN · V→V 29; COGER_RACION · V→F 9; COGER_RACION · V→V 16; COGER_RED · F→F 1; COGER_RED · V→V 2.

### Lo que no se recalcula (decisión de Manel)

- `analiza_P7_61.py` (M2 y M2b de P7-61) y `potencia_P7_61.py`, `potencia_P7_61b.py` usan la misma función vieja. No se recalculan: el paper no los cita.

La lista de las 172 evaluaciones de P7-56 que cambian de clase (todas las partidas) está en `P7_56_erratas_b.json` (`P7_56_lista_cambian`).
