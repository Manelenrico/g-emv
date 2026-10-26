# SELLO P7-67 · El campo de la mentira seguible, con el mando de la amenaza

*Sellado el 17-oct-2026, antes de jugar ninguna partida del campo (el humo del punto 5 son las primeras). Las decisiones de la mesa se copian tal cual; lo que he tenido que interpretar
va aparte, en la sección «Interpretaciones», para que la mesa lo confirme antes de lanzar el campo. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`.*

## 1. Brazo nuevo CONGELADA

Idéntico a MIENTE (misma mentira, mismos destinos, mismo juicio), pero la confianza del cuerpo en la razón no se actualiza: se queda en 0,5 en las tres dimensiones toda la vida.
El juicio se calcula y se registra igual, pero no cambia nada.

Pieza `congela_P7_67.py` (GEMV_P7_67_CONGELA=1), aplicada la última (envoltura más exterior). Fija la confianza en 0,5 en cuatro momentos:
- al arrancar el día, después de leer el cuaderno;
- al final de cada `decidir`, después del juicio y antes de que el cuerpo vuelva a decidir;
- al volcar el cuaderno;
- al cerrar el día.

Cada vez que la encuentra distinta de 0,5 deja un registro `P7_67_congela`.

Pruebas (`prueba_congela_P7_67.py`): 8 pasan, 0 fallan.
- Control sin la pieza: una llegada juzgada 0 baja recursos a 0,35.
- Con la pieza, la misma llegada se registra igual (acierto 0, `confianza_despues` 0,35) y al acabar el `decidir` vuelve a 0,5 en las tres dimensiones.
- Un cuaderno de 0,2 / 0,35 / 0,9 se lee y queda en 0,5.
- El cuaderno que se escribe al cerrar lleva 0,5.

## 2. Diseño del campo

**a) Corazón:** 1 rival activo y 13 estatuas; brazos MIENTE, CONGELADA y HONESTA; 20 días; 16 series. El rival activo es el del banco: aaron-zs-fable v2 en el asiento 4, elegido con
`random.Random(6767)` (REGISTRO_P7_67, decisión 3).

**b) Mando de la amenaza:** 2, 3 y 14 rivales activos (el de 14 es el mundo normal, sin estatuas); brazos MIENTE y HONESTA; solo días 1-5; 6 series. Los rivales añadidos se eligieron con
`random.Random(6768)`: 2 sillas sin reemplazo de las 13 que quedan del roster de P7-65 y 2 asientos sin reemplazo de los libres.
- **Nivel 2:** aaron (asiento 4) + zero-sum-scavenger v12 (asiento 12).
- **Nivel 3:** los dos anteriores + belobog v2 (asiento 2).
- **Nivel 14:** el roster de P7-65 tal cual (asiento −1, lo reparte la plataforma).

Las estatuas de los niveles 2 y 3 son las del 1 menos los asientos que pasan a activos. Los destinos de la mentira siguen a más de 6 casillas de cualquier estatua.

**c) Todo lo demás, como en el banco de `invita_P7_67b`:**
- hermanas en 10 y 11, COMPARTE con fusión, miedo 0,5 / 1,5;
- una invitación al día escrita por el guion (sin razón);
- invitación seguible desde el tramo de los primeros 300 tics; la distancia de 8-15 se mira solo al aceptar; interrupción por un rival activo a 3 casillas o menos;
- acierto con un botiquín a 3 casillas o menos del destino; una llegada por criatura, destino y día;
- cadena de cuadernos por (nivel, brazo, serie).

**Semillas:** s(serie, día) = 20260916 + k × 104729, con k = 261 + 20 (serie − 1) + (día − 1). Es la misma sucesión que en P7-41 y P7-61, con k de 261 a 580, ninguna usada antes.
Cada serie y día lleva la misma semilla en todos los brazos y niveles, así que las series 1-6 del mando juegan los mismos mapas que las series 1-6 del corazón.

**Destinos:** los del banco, elegidos con `random.Random(1000·día + 10)`:
- la mentira (MIENTE y CONGELADA), de `P7_67_destinos.json`;
- la honesta, de las casillas del centro.

Están todos en `P7_67F_diseno.json`.

**Tamaño:** 84 cadenas (48 del corazón de 20 días y 36 del mando de 5 días), **1.140 partidas**.

## 3. Medida y predicciones (de la mesa, tal cual)

- Oportunidad: un día en que a una criatura se le ofrece ir_sitio en calma, en el tramo y a la distancia correctos.
- Llegada: llega al destino tras aceptar ese día.
- Unidad: la pareja. Para cada pareja, la fracción de oportunidades con llegada en los días 1-10 (A) y 11-20 (B). Una pareja necesita al menos 3 días con oportunidad en A y en B; si no, queda fuera y se cuenta.
- P1: en MIENTE, la media de (B − A) por pareja es < 0 a ≥ 3 errores estándar (sd/√n de las parejas).
- P2: (B − A) de MIENTE menos (B − A) de CONGELADA < 0 a ≥ 3 errores estándar (error de la diferencia de dos medias independientes).
- P3: en los días 1-5, la fracción de oportunidades con llegada baja con el número de rivales activos (1, 2, 3, 14): pendiente negativa, con los rivales en escala logarítmica, a ≥ 3 errores estándar, con las parejas como unidad. El nivel de 1 rival sale de los días 1-5 del corazón.
- Descriptivo, sin predicción: HONESTA, la confianza día a día por brazo y dimensión, las interrupciones por nivel y las muertes.
- Robustez: repetir P1-P3 sin las partidas marcadas (partida entera) y con la criatura como unidad. No cambian ningún veredicto.

## Interpretaciones (las he tenido que fijar para poder calcular; a confirmar por la mesa antes del campo)

1. **Oportunidad.** Cuento oportunidad si en algún tic de los 300 primeros de la fase viva `ir_sitio` está entre los candidatos del cuerpo (`RADIOGRAFIA.candidatos`, que el diario
   guarda en cada tic). Antes de aceptar, la pieza solo lo ofrece en calma, en el tramo y a 8-15 de las dos. Después de aceptar lo sigue ofreciendo, pero aceptar ya exigió esa oferta.
2. **Fracción de la pareja.** Es el cociente de las sumas: las llegadas entre las oportunidades de las dos hermanas en esos días. No es la media de las dos.
3. **«Al menos 3 días con oportunidad».** Un día cuenta para la pareja si al menos una de las dos tuvo oportunidad ese día. En la robustez por criatura, cada criatura cuenta sus propios días.
4. **P1 y P2 son del nivel 1 (el corazón).** sd es la desviación típica muestral (n − 1).
5. **P3.**
   - Una fila por pareja con los brazos MIENTE y HONESTA juntos, sin término de brazo. CONGELADA no entra, porque el mando no la tiene.
   - x = ln(rivales activos), y = la fracción de la pareja en los días 1-5.
   - Mínimos cuadrados ordinarios; error estándar clásico de la pendiente, √(SSR / (n − 2) / Sxx).
   - Entra la pareja con al menos 1 oportunidad en los días 1-5; las que no tienen ninguna se cuentan.
   - El nivel 1 aporta 32 parejas (16 de MIENTE y 16 de HONESTA) y cada uno de los otros, 12.
6. **Partida marcada.** Una partida en la que alguna de las dos hermanas no pasa la guarda de latencia de P7-65 (`guarda_latencia_P7_29`, campo `pasa`). En la robustez sale la partida
   entera: sus dos criaturas ese día.
7. **Veredicto.** PASA si la estimación es < 0 y estimación / error estándar ≤ −3. Si no hay unidades suficientes para un error estándar, NO CALCULABLE.
8. **Días perdidos.** Un día perdido (dos fallos de la plataforma) o una criatura muerta antes del tramo no tienen oportunidad, así que no cuentan.

## 4. Guion de análisis sellado

`analiza_P7_67.py`, md5 **`3ffde9ec5408bea845ccd487ea3ee305`**. Lee `P7_67F_estado.json` y los diarios (el `.art.log` o, si no está, el `.zip` de la plataforma) y escribe
`P7_67_analisis.json`. Se ha probado de principio a fin con los datos de los bancos de P7-67:
- **`--prueba-bancos`** (el banco de `invita_P7_67b` tal cual: 4 días, sin CONGELADA, un solo nivel): corre; P1, P2 y P3 salen NO CALCULABLE, como debe ser (no hay días 11-20,
  ni CONGELADA, ni más de un nivel).
- **`--fontaneria`** (PRUEBA DE FONTANERÍA, no es un resultado): los dos bancos reetiquetados para pasar por todas las ramas (A = días 1-2, B = 3-4, al menos 1 día; HONESTA copiada
  como CONGELADA; el primer banco como nivel 2). Corre P1, P2 y P3 con sus tres variantes (principal, sin marcadas y por criatura), la confianza día a día, las interrupciones y las
  muertes; 0 llegadas sin oportunidad.

Nada del punto 3 ha resultado imposible de calcular tal como está escrito. Lo que he tenido que fijar está en «Interpretaciones».

## 5. Humo

El primer día de la serie 1 de cada brazo y de cada nivel: 9 partidas (nivel 1 MIENTE, CONGELADA y HONESTA; niveles 2, 3 y 14 MIENTE y HONESTA), con 2 cadenas en paralelo.
Se comprueban:
- la guarda de latencia;
- que hay diarios y cuaderno de fin en los 18 asientos;
- el juicio (registros P7_66_*, acierto a ≤ 3);
- en CONGELADA, que la confianza queda en 0,5;
- que el guion corre sobre esos datos.

Si todo pasa, esas 9 partidas cuentan como campo y el campo sube a 7 cadenas en paralelo, **tras el visto bueno de Manel**.

## 6. Disco

Cada vez que el espacio libre baja de 15 GB, `archiva_P7_67F.py` (md5 `97bb7c7c238f94c37b2647e575de6bad`) copia al T7 lo completado, con relectura por md5, sin parar el campo.
**No borra nada del Mac.** Ver la pregunta abierta 1.

## 7. Imágenes

Se construyen igual que en los bancos: una por cadena y día, horneada con el cuaderno del día anterior, en serie bajo el cerrojo de docker. `Dockerfile.pareja_P7_67c` es el de 67b más
la pieza CONGELADA y dos argumentos (ACTIVOS del nivel, CONGELA).

## Archivos sellados (md5)

| archivo | md5 |
|---|---|
| analiza_P7_67.py | 3ffde9ec5408bea845ccd487ea3ee305 |
| P7_67F_diseno.json | 8f11cc7c0c1e97cfb95e8acade3b184c |
| disena_P7_67F.py | 7ee24f0ee5fc60e81de6e11c82487578 |
| lanza_P7_67F.py | 94a940684e3515b59ee37d4fb249b02b |
| archiva_P7_67F.py | 97bb7c7c238f94c37b2647e575de6bad |
| congela_P7_67.py | 5a9feb0d720ab6ea277e988c93630d37 |
| campo_P7_67c.py | 660e94164088b6010393219667b72ea0 |
| policy_pareja_P7_67c.py | 296df35605b424f0efcd34d6dbf56ec6 |
| Dockerfile.pareja_P7_67c | d29fe05a85a9235075a805a3d6615018 |
| invita_P7_67b.py | a25ebbfce4774cad72fc8439e6e045eb |
| invita_P7_67.py | 55de13e237a1484dd533b41b7fe01d0d |
| invita_P7_66b.py | c1352e4ad95c7a7515ca8394c8e0185b |
| campo_P7_67b.py | 1bfe2051610a7e542f4d3741d02522ca |
| campo_P7_67.py | 1a56963e35192913157f7625c91dea4c |
| pasiva_P7_67.py | 09faa2e5b4b728fdc8b90cd002f4eb3d |
| motor/model.py | 1e511978c251130e95169ebf8443efa1 |

## Preguntas abiertas para el visto bueno

1. **El disco no da para el campo sin borrar.** Cada partida ocupa unos 75 MB: dos diarios extraídos de unos 37 MB y sus zips de 1 MB. 1.140 partidas son unos 85 GB y quedan
   30 GB libres. Archivar al T7 sin borrar no libera nada, y a 5 GB la guarda de disco para el campo. **Propuesta:** tras copiar al T7 y releer por md5, borrar del Mac solo el
   `.art.log` extraído de cada vida, dejando su `.zip`, que es el mismo diario (es lo que hacía `archiva_P7_52 --borra`). El guion de análisis ya lee del zip. Así cada partida se
   queda en unos 2 MB en el Mac. Es borrar, así que no lo hago sin tu permiso.
2. **Tiempo.** El cuello de botella es el horneado en serie (unos 2,6 minutos por imagen y una imagen por partida): 1.140 × 2,6 ≈ 50 horas, unos 2 días, con 7 cadenas en paralelo.

## Enmienda 1 (17-oct-2026, 15:34), visto bueno de Manel con ajustes, escrita antes de lanzar el campo

1. **Interpretaciones 1, 2, 3 y 5: confirmadas** tal como están escritas.
2. **P3:** la misma regresión, pero con el brazo (MIENTE/HONESTA) como variable indicadora. Se juzga la pendiente de ln(rivales activos) a ≥ 3 errores estándar. Sigue contando solo
   parejas con al menos 1 oportunidad. La regresión es de mínimos cuadrados con constante, ln(rivales) y la indicadora HONESTA = 1, con error estándar clásico, σ²·(X'X)⁻¹ y
   σ² = SSR / (n − 3); comprobada contra numpy.
3. **Nueva predicción P3b, sellada ahora:** la misma regresión, con brazo como variable, pero la variable de cada pareja es el número medio de llegadas por día en los días 1-5, contando
   como 0 los días sin oportunidad. Entran todas las parejas con al menos una hermana viva al empezar el día 1. Pendiente negativa a ≥ 3 errores estándar.
   Cómo lo calculo:
   - las llegadas de un día son las de las dos hermanas (0, 1 o 2), y la media se toma sobre los días 1-5 jugados;
   - «al menos una hermana viva al empezar el día 1» = el día 1 jugado (cada partida empieza con las dos vivas);
   - en la robustez por criatura, las llegadas de la criatura por día jugado.

   **Descriptivo añadido:** la fracción de días con oportunidad por nivel (y por nivel y brazo) en los días 1-5.
4. **Disco, aprobado:** tras copiar cada partida al T7 y releerla por md5, se borra del Mac solo su `.art.log` extraído y se deja el `.zip`. Nada más. Salvaguardas:
   - solo partidas ya procesadas, con los dos cuadernos de fin;
   - solo si todos sus archivos están en el T7 y releídos iguales;
   - solo si el diario dentro del `.zip` tiene el mismo md5 que el `.art.log`.

   Probado con las 9 partidas del humo: 185 archivos copiados y releídos iguales, 18 `.art.log` borrados (0,49 GiB) y 0 sin borrar. El guion de análisis lee del zip y da los mismos
   18 criatura-días.
5. **Vigilancia de CONGELADA:** en la primera llegada de un asiento de CONGELADA del campo, se comprueba que la confianza vuelve a 0,5 en las tres dimensiones. Se mira el registro
   `P7_67_congela` del mismo tic con «después» en 0,5 y el `P7_54_cierre` del día en 0,5. Si no vuelve, se para el campo entero (salida 10) y se avisa. Pruebas:
   `prueba_vigila_P7_67F.py`, 4 pasan.
6. **El campo se lanza con 7 cadenas en paralelo.** Si algo falla, para y lo deja escrito en el estado (`paradas`), sin arreglos improvisados. Al cerrar no se miran los resultados del
   sello: solo el estado y las incidencias.

**Guion de análisis actualizado (P3 con brazo, P3b y el descriptivo nuevo): md5 `7bef2e46106bb860c366b0bdb1dba037`.** Sustituye al md5 anterior, `3ffde9ec…`.
Probado de nuevo de principio a fin:
- con el banco de `invita_P7_67b` tal cual: NO CALCULABLE donde corresponde;
- con la prueba de fontanería: pasa por P1, P2, P3 y P3b en sus tres variantes;
- con los datos del humo: corre.

**Otros archivos cambiados por esta enmienda (md5 nuevos):**

| archivo | md5 |
|---|---|
| lanza_P7_67F.py | 07f751c6030820b9c827faddc15e1e48 |
| archiva_P7_67F.py | 0ecefbb9a148d154654d4450cfcd3c93 |

## Enmienda 2 (17-oct-2026, 22:07), decisión de la mesa sobre la parada del campo

1. `n1_s1_d19_CONGELADA` se trata como **marcada**: sale entera en la robustez.
2. **Rareza conocida del mundo** (como en P7-30): los pasos bloqueados sin cuerpo en las casillas (27, 21) y (28, 21) de esa fortaleza no paran el campo. Una vida que pase del 5 % con la
   mayoría de sus bloqueos en esas dos casillas queda marcada, su partida sale en la robustez y el campo sigue. Motivo: los choques son `ir_pareja` contra el muro de la fortaleza con la
   hermana dentro; no están ligados a `ir_sitio` (4 de 2.270 bloqueos con `ir_sitio` elegido).
3. **El resto de la guarda no cambia:** la latencia sigue siendo dura y los bloqueos por encima del 5 % en cualquier otra casilla siguen parando el campo.
4. `lanza_P7_67F.py`, md5 nuevo **`baa57503b8d702c6ef41e3351dbdf196`**. El guion de análisis no cambia: sigue siendo `7bef2e46106bb860c366b0bdb1dba037`, y ya saca de la robustez
   cualquier partida marcada.

## Enmienda 3 (18-oct-2026, 08:05), decisión de la mesa sobre la segunda parada del campo

1. `n1_s3_d7_CONGELADA` se trata como **marcada**: sale entera en la robustez.
2. **La rareza de la fortaleza pasa a ser por zona:** todas las casillas `F` de esa fortaleza del mapa fijo, más todas las de suelo dentro de ella o a 1 casilla o menos de sus muros. Es el
   cuadrado x 19-29, y 19-29: 121 casillas, 24 `F` y 97 de suelo. La lista exacta está en `REGISTRO_P7_67.md` y en `P7_67F_zona_fortaleza.json`. Una vida que pase del 5 % con la mayoría
   de sus bloqueos en la zona queda marcada, su partida sale en la robustez y el campo sigue.
3. **El resto de la guarda no cambia:** latencia dura, y los bloqueos por encima del 5 % fuera de la zona siguen parando el campo.
4. `lanza_P7_67F.py`, md5 nuevo **`75af5dbc899649b6ddb4215d1b954206`**; `P7_67F_zona_fortaleza.json`, md5 en el commit. El guion de análisis no cambia
   (`7bef2e46106bb860c366b0bdb1dba037`).

## Enmienda 4 (18-oct-2026, 13:43), decisión de la mesa sobre la tercera parada del campo

1. Reintento de `n1_s4_d9_HONESTA`, una sola vez, con la misma imagen y semilla. La primera partida se aparta: no cuenta, no es marcada, consta como apartada por fallo de la plataforma.
2. **Regla fija:** si la plataforma da una partida por completada pero falta algún diario porque borró el contenedor antes de recogerlo, el lanzador la reintenta una vez, con la misma
   imagen y semilla, sin parar el campo, y lo apunta en el registro. Si el reintento también falla, el campo para.
3. `lanza_P7_67F.py`, md5 nuevo **`b632b91869a4af0ee18959589e843b00`**. El guion de análisis no cambia (`7bef2e46106bb860c366b0bdb1dba037`): solo lee las partidas de
   `peticiones`, y las apartadas no están ahí.
