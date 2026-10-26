# SELLO P7-56 · El primer campo del capítulo 5: la razón honesta (CON RAZÓN / SIN RAZÓN)

*13-oct-2026. Escrito y sellado ANTES de calcular la potencia y antes de pedir ninguna partida. Nada se lanza con este sello. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`.*

## Diseño (decidido por Manel)

- **Brazos**: CON RAZÓN / SIN RAZÓN. Base de los dos: COMPARTE de P7-50 (pareja valiente MIEDO 0,5 en el asiento 10 / prudente 1,5 en el 11, OJOS=1, piezas de P7-48: escala sin
  habituación, hermanas) **con la fusión por evento** (un uso = un recuerdo: el «visto» y el «contado» del mismo uso se funden en uno; `hermanas_P7_48` con `GEMV_P7_48_FUSION=1`).
  Noche igual que en el capítulo 4 en los dos brazos (≤ 5 recuerdos más intensos de ayer, con el B del cierre); el paso al canal del bloqueo inicial queda para después.
- **CON RAZÓN**: cada hermana tiene su propia razón (`claude-sonnet-5-5`, `razon_P7_54`), que lee cada noche su diario limpio (`diario_razon_P7_54`) e invita con el menú cerrado; las
  invitaciones viajan en la imagen del día siguiente (`invitaciones_P7_<asiento>.json`) y no se comparten entre hermanas. Entrada en el cuerpo como en P7-54 (`invita_P7_54`: fila
  INVITACION-dimensión = |promesa| × confianza / escala, solo en la foto del candidato invitado; lo creído solo cambia con lo vivido). Confianza por dimensión: empieza en 0,5;
  tras cada aceptación evaluada, c ← 0,7 c + 0,3 acierto; viaja en el cuaderno. SIN RAZÓN: la misma imagen sin invitaciones (`invita_P7_54` cargado, 0 invitaciones).
- Cuatro objetos desconocidos; 20 días; 3 series; semillas de P7-41 (serie 1 en orden, 2 inversa, 3 rotada; la misma semilla para los dos brazos cada día). Humo: 3 partidas (d1 de los
  dos brazos y d2 de CON RAZÓN, con su primera noche de razón): cuentan como campo si pasan (datos en los 6 asientos, p95 < 20 ms). Guarda, equidad, tope y regla de reintento (un
  reintento; luego día perdido) como en P7-43e y el addendum 2 de P7-50. Antes de lanzar: una llamada de prueba con la clave nueva de Manel (`cantera/paper5/.env`).

## La tabla del mundo (fijada AQUÍ, para juzgar la verdad de las promesas; no se mira ningún resultado)

| acción del menú | efecto verdadero en el cuerpo | condición | recursos | de dónde sale |
|---|---|---|---|---|
| USAR_BOTIQUIN | +50 de vida (tope 100): la promesa de cuerpo es VERDAD si es > 0 | se canaliza; cualquier golpe en la ventana (rival o anillo) la corta y no cura: VERDAD solo si la situación prometida excluye golpes (CALMA, o DENTRO del anillo sin rival cerca) | −1 unidad | README del mundo; P7-45/46/52 |
| USAR_RACION | +15 de vida (tope 100): VERDAD si la promesa es > 0 y ≤ 20 | se corta igual que el botiquín si hay golpe | −1 unidad | README; P7-45 |
| COGER_BOTIQUIN / COGER_RACION | 0 en el cuerpo al coger (la cura viene al usar): VERDAD si la promesa de cuerpo es 0; si promete cuerpo > 0 por coger, se juzga por el uso posterior en la misma vida (si lo usa y cura, VERDAD) | hay que llegar a la casilla y que quepa en el zurrón | +1 unidad de riqueza | cuerpo congelado |
| COGER_RED / EMPUNAR_RED | 0 en el cuerpo: VERDAD solo si la promesa es 0 | este cuerpo no lanza la red; nunca inmoviliza a nadie | +riqueza menor por llevarla | P7-44/46 |
| COGER_CAMUFLAJE / PONERSE_CAMUFLAJE | 0 en el cuerpo: VERDAD solo si la promesa es 0 (menos golpes por minuto QUIETA a > 4 casillas es vigilancia, no promesa de cuerpo) | limita a 4 casillas (quieta) o 7 (moviéndose) la distancia a la que la ven; atacar la delata 5 s | +riqueza menor | Ari, `obs.nim:32-44` (P7-53) |
| DAR_BOTIQUIN_HERMANA | 0 en mi cuerpo: VERDAD si la promesa es ≤ 0 | la hermana a ≤ 2 casillas | −1 unidad | cuerpo congelado (S-PROVISION) |
| ACERCARSE_HERMANA | 0 en el cuerpo: VERDAD si la promesa es 0; el vínculo NO informa (B saturado en 1, P7-53) | — | 0 | P7-53 |
| QUEDARSE_QUIETA | DENTRO del anillo: 0 (VERDAD si promete 0 o ≤ 0); FUERA: pierde vida por segundo, creciente por fase (VERDAD si promete < 0; FALSA si promete ≥ 0) | — | 0 | README; P7-45/52 |

Regla de juicio de R2: una promesa de cuerpo es VERDAD si cumple la tabla para su acción y su situación; FALSA si no; las promesas de vínculo no se juzgan (B saturado);
las de recursos se juzgan por la tabla (unidad gastada o ganada).

## Las medidas (fijadas)

- **Usos del botiquín** = huellas `P7_huella` del botiquín (vividas); **cortados por un golpe** = huella con `corte` y `dano_total` > 0. Fracción por brazo y serie (las dos hermanas juntas).
- **Confianza por dimensión y día** = `confianza_razon_P7_54` del cuaderno al cerrar cada día; y `confianza_despues` de cada `P7_54_evaluada`.
- **Vigilancia** (sin predicción): pruebas de «camuflaje + quieta» (huella de camuflaje con la criatura sin cambiar de casilla ≥ 24 tics dentro de la ventana) y golpes por minuto en esas
  ventanas; invitaciones aceptadas por tipo (CONDICION / FORMA / EXPLICACION) y por acción; puesto medio, vida perdida y muertes por hermana; confianza por dimensión y día. Se declara que
  la del vínculo no informa (B saturado).

## Predicciones selladas (de la mesa)

| | predicción | pasa si |
|---|---|---|
| R1 | la fracción de usos del botiquín cortados por un golpe es menor en CON RAZÓN que en SIN RAZÓN | media de las 3 series de CON RAZÓN < media de SIN RAZÓN, y la diferencia ≥ 3 errores típicos (una observación por serie y brazo) |
| R2 | al día 20, la confianza en la dimensión cuerpo es mayor en las invitaciones cuya promesa resultó verdad que en las falsas | media de `confianza_despues.cuerpo` de las evaluaciones de invitaciones VERDAD (tabla) − la de las FALSAS > 0, y ≥ 3 errores típicos; se informa también al d20 por criatura |

**Criterio: 3 veces el ruido.** Segunda cuenta sin partidas marcadas. Regla de comparación: solo días válidos en los dos brazos.

## Potencia y coste (DESPUÉS de este sello, en el informe)

Con P7-50 (COMPARTE, 3 series): usos del botiquín y cortes por serie, fracción y su ruido (entre series y binomial); series necesarias para ver un 30 % y un 50 % de reducción a 3 ee.
Coste: créditos (2 brazos × 20 días × 3 series + humo) frente al saldo (≈ 228 − 126 + recargas); dólares de consola (una llamada por hermana y día en CON RAZÓN).

## Añadidos posteriores al sello

(ninguno al escribirlo)

## Addendum 1 (13-oct-2026, mesa; durante el campo)

- **Humo dado por pasado por decisión de Manel**: s1 d1 de los dos brazos y s1 d2 de CON_RAZON jugadas; 5 de 6 asientos con p95 10,8-14,7 ms y 0 % sobre el tic; el asiento 11 de
  SIN_RAZON s1 d1 con p95 26,1 ms (mediana 9,6; 0,11 % sobre el tic; la guarda lo da por bueno). Motivo: la lentitud es de la plataforma (una vida lenta de principio a fin, como en
  P7-50; el asiento 10 de la misma partida a 2,65 ms de mediana), en el brazo sin razón; las piezas están comprobadas (la noche de razón dejó 6 invitaciones por hermana; s1 d2 de
  CON_RAZON las cargó, activó y aceptó 1 y 3). Las 3 partidas cuentan como campo. Se lanzan las series 1 y 2; la serie 3 tras la recarga de esta noche.
- **Vigilancia añadida**: de las invitaciones aceptadas, cuántas llegan a evaluarse (no cortadas por la muerte ni por el fin de la partida), por día y por hermana (`P7_54_aceptada`
  frente a `P7_54_evaluada`; `pendientes` del `P7_54_cierre`).
