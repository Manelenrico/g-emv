# SELLO P7-49 · El campo del capítulo 4: las hermanas que se cuentan lo aprendido (COMPARTE / SOLAS)

*12-oct-2026. Escrito y sellado ANTES de calcular la potencia y antes de pedir ninguna partida. Nada se lanza con este sello: se trae el sello, la potencia y el coste a la mesa.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`, ni copiado ni tocado. Cuerpo y congelados sin tocar.*

## Diseño (decidido por Manel)

- **Brazos**: COMPARTE (mirando + canal + noche, `hermanas_P7_48` modo comparte) y SOLAS (`hermanas_P7_48` modo solas). Ojos compartidos (OJOS=1) en los dos: la ÚNICA diferencia
  entre brazos es compartir recuerdos.
- **Criatura**: P7-40 + la intensidad en su escala (`escala_P7_48`), sin habituación; cuatro objetos desconocidos como en P7-45 (botiquín, ración, red, camuflaje).
- **Pareja**: una valiente (asiento par = 10, MIEDO 0,5) y una prudente (impar = 11, MIEDO 1,5), con `miedo_P7_49` (P7-49a: las filas que anticipan una pérdida × MIEDO; S-VINCULO y
  S-VIDA-AJENA fuera; cautela del probar con el mismo factor). Igual en los dos brazos.
- **Cadena**: cada serie = 20 días; el cuaderno de cada hermana viaja (y en COMPARTE, la noche lee el de la otra). Semillas: `semillas_P7_41.json` (serie 1 en orden, 2 inversa, 3
  rotada; las series 4+ si las hubiera: rotación de 5 posiciones más por serie, declarado aquí). La misma semilla para los dos brazos cada día.
- **Imágenes**: `Dockerfile.pareja_P7_49` (ARG HERMANAS, MIEDO_V=0,5, MIEDO_P=1,5; CUAD con los cuadernos del día anterior de las dos). Humo: 3 partidas (día 1 de COMPARTE y SOLAS
  y día 2 de COMPARTE con los cuadernos del humo) antes del campo; cuentan como campo si pasan.
- **Guarda, equidad y tope como en P7-43e**: guarda dura de latencia (> 10 % sobre el tic o > 5 % bloqueadas sin cuerpo para; marca entre 1 y 10 %); equidad ± 2 puntos entre
  brazos; tope de 12 partidas a la vez, 20 si el día 1 de los dos brazos cumple (p95 < 20 ms, < 1 % sobre el tic); humo con p95 < 20 ms; cadenas primero.

## Las medidas (fijadas; por hermana y por brazo y serie)

- **Creencia del botiquín** de una hermana en el día d: `creencias[botiquín].dentro.cuerpo` del cuaderno que escribe al cerrar el día d (como en P7-42; None = 0).
  **Área bajo la curva** (días 1-20) = suma de esa creencia de d = 1 a 20.
- **La hermana que menos prueba por sí misma**: en SOLAS, por serie, la hermana (valiente o prudente) con menos pruebas (huellas `P7_huella`, origen vivido) en los 20 días; esa
  misma hermana (mismo asiento) es la que se mira en COMPARTE de la misma serie. (No se apuesta por cuál es.)
- **Parecido entre hermanas**: por día de los días 11-20 y por objeto de los cuatro, |creencia_10 − creencia_11| (dentro, cuerpo; None = 0); la media de esos 40 valores por serie.
- **Fracción a lo inútil**: pruebas (huellas vividas) de red + camuflaje ÷ todas las pruebas, las dos hermanas juntas, días 1-20, por serie.
- **Vigilancia (sin predicción)**: pruebas por vida de la valiente y de la prudente; «contagio de errores» = recuerdos contados o vistos cuyo efecto del cuerpo difiere en signo
  del efecto real del objeto (botiquín +, ración +, red 0, camuflaje 0: efecto > 1 donde debe ser 0, o ≤ 0 donde debe ser > 0) ÷ recibidos; puesto medio por hermana (partidas
  con corte fuera); recibidos por origen por vida; latencia y guarda por hermana.

## Predicciones selladas (de la mesa)

| | predicción | pasa si |
|---|---|---|
| S1 | la hermana que menos prueba por sí misma cree más en el botiquín en COMPARTE que en SOLAS | área bajo la curva (d1-20) de esa hermana: media de COMPARTE − media de SOLAS > 0, y ≥ 3 errores típicos de la diferencia |
| S2 | las hermanas de COMPARTE se parecen más en lo que creen | parecido (d11-20, cuatro objetos): media de COMPARTE < media de SOLAS, y la diferencia ≥ 3 errores típicos |
| S3 | en COMPARTE va menos a red y camuflaje | fracción a lo inútil (las dos juntas): COMPARTE < SOLAS, y ≥ 3 errores típicos |

Errores típicos: de la diferencia de medias entre brazos, con una observación por serie y brazo (raíz de la suma de cuadrados de los errores típicos de cada brazo).
**Criterio: diferencia ≥ 3 veces el ruido.** Segunda cuenta sin las partidas marcadas por la guarda (informada).

## Potencia y coste (se calculan DESPUÉS de este sello, en el informe)

Ruido = el de P7-45 (APRENDE, 12 criaturas / 6 parejas-serie, sin compartir): desviación típica entre criaturas del área bajo la curva (S1), entre parejas-serie del parecido (S2)
y de la fracción a lo inútil (S3). Series necesarias para ver un efecto del 30 % y del 50 % de la media con 3 errores típicos; coste = 2 brazos × 20 días × series + 3 de humo.
Saldo de partida: 228 el 12-oct a las 06:47, +71 al día.

## Añadidos posteriores al sello

(ninguno al escribirlo)

## Addendum (12-oct-2026, mesa P7-50; S1-S3 sin cambios; escrito ANTES de lanzar)

1. **Plataforma: 3 series** (≈ 123 créditos: 2 brazos × 20 días × 3 + humo). Humo = las 3 primeras partidas del campo (s1 d1 de COMPARTE y SOLAS; s1 d2 de COMPARTE con los
   cuadernos del humo): si hay datos en los 6 asientos y p95 < 20 ms cuentan como campo; si no, se para y se avisa. Guarda dura, equidad ± 2 puntos y tope 12 → 20 como en P7-43e.
   **S3 tiene potencia aquí** (ruido de P7-45: un 30 % se ve con 2 series). **S1 y S2 se informan con su dirección y se declara que solo saldrían con efectos enormes** (con 3
   series, ≥ 89 % y ≥ 104 % de la media; `P7_49_potencia.json`). Lanzador `lanza_P7_50.py` (estado `P7_50_estado.json`, diarios `P750_*`, cuadernos `cuadernos_P7_50/`),
   orquesta `orquesta_P7_50.py`, equidad `equidad_P7_50.py`; imagen `Dockerfile.pareja_P7_49` (HERMANAS = comparte | solas, MIEDO_V 0,5, MIEDO_P 1,5).
2. **Local** (`coworld play` en el Mac, 0 créditos), sin estorbar a la plataforma: COMPARTE / SOLAS con las mismas piezas, la misma pareja y las mismas predicciones S1-S3,
   nuestra imagen en los 16 asientos (8 parejas por partida; la unidad de observación local es la pareja-serie). Antes de jugar: ruido local de S1 y S2 con las vidas de P7-48
   (cadenas de 3 días, escalado a 20 declarado), series locales necesarias para un 50 % en S1 y S2, duración por serie en el Mac y disco. Si caben en unas 24 h con ≥ 8 GB
   libres al final, se juegan; si no, se dice cuántas caben. Los diarios locales se comprimen tras leerlos.
3. Informe `informe_P7_50.md`: los dos mundos POR SEPARADO (ruido y veredicto de cada uno) y una línea final: ¿coinciden o no?

## Addendum 2 (12-oct-2026, 15:50; mesa P7-50, durante el campo)

- La guarda dura paró SOLAS s3 d1 (asiento 11: bloqueados sin cuerpo 6,0 % > 5 %; una racha de 311 empujes `ir_pareja` hacia una casilla vacía de cuerpos, marcada por v3b a los
  72 tics y no evitada porque el veto de v3b mira el destino del `ir_*`, no el primer paso). Decisión de Manel: **un reintento** de s3 d1 SOLAS con el mismo cuaderno vacío; el
  intento parado queda FUERA de resultados (`P750r_s3_d1_SOLAS_*`, `P7_50_res/intento1_*`, `reintentos` en el estado); se relanza la orquesta de la serie 3.
- **Regla para el resto del campo**: si la guarda vuelve a parar una vida, un reintento; si para otra vez, ese día queda perdido (`dias_perdidos` en el estado; la cadena sigue
  con el último cuaderno escrito) y se aplica la regla de comparación: solo días válidos en todos los brazos.
- No se cambia la pieza a mitad de campo. Apuntado para después: ampliar el veto de v3b al primer paso del camino. En el informe: rachas ≥ 72 tics que la regla no quitó, por brazo
  y por hermana.
