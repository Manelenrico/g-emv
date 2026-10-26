# SELLO P7-42 · El campo del capítulo 3 (segunda etapa): APRENDE, BORRADO, TECHO y SIN EMOCIÓN, con carácter

*10-oct-2026, commit `a481226`. Escrito ANTES de pedir ninguna partida (el humo de 3 y el freno son parte del campo). Coste previsto: 363 créditos de experiencia (360 del campo + 3 del
humo); disponibles el 10-oct, dato de Manel: 496 de 1.000, +71/día. Consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Cuerpo y congelados sin tocar.*

## El diseño (decisiones de la mesa, P7-42, sobre el plan de P7-41)

- **Criatura que aprende**: P7-40 tal como quedó sellado (esperanza de clase; cautela sobre la curiosidad; miradas y apuntes por su mayor, sin tocar), sobre B1 de P7-39.
  Piezas: `efecto_P7_39.py`, `contrafactual_P7_38.py` (B1: sin contrafactual ni pistas), `filo_P7_40.py` (de campo: personalidad, caché por tic, apuntes dentro del cuaderno),
  `campo_P7_41.py`, `policy_pareja_P7_41.py`; md5 en el informe.
- **SIN EMOCIÓN, un solo nivel** (`azar_P7_41.py`, modo «momento»): mismo cuerpo, percepción, recuerdos y creencia (importancia B1); sin curiosidad (`GEMV_P7_NOVEDAD=0`),
  sin esperanza de clase ni apuntes. En CADA tic de decisión en que hay una cosa de las cuatro a su alcance (a la vista sin llevarla, conocida o desconocida; o un consumible
  en el zurrón) se tira una moneda PURA con probabilidad ε; si sale, se fuerza la prueba de una de las cosas al alcance, elegida al azar (ir y coger, hasta 240 tics; o usar
  el consumible). Veto fuera de la moneda: el cuerpo no coge ni usa por sí solo nada de clase desconocida.
- **ε = 0,00019**, calibrado en local (`banco_P7_41.py --calibra`, 80 réplicas de las vidas de APRENDE de P7-34): pruebas de SIN en 20 días por criatura = 40,0 forzadas +
  37,5 usos propios (intenciones de usar agrupadas a 240 tics) = 77,5, frente a 81,5 de APRENDE en P7-34 (110, 77, 62, 77 en las 4 criaturas): −4,9 %, dentro del ±20 %.
  (Con ε = 0,00034, 114,8: +41 %.) Momentos con objeto al alcance: 982.321 en 80 vidas (casi todos los tics: el botiquín o la ración suelen ir en el zurrón).
- **Carácter**: `model.py` no expone ningún parámetro de miedo (`ModelConfig`: targets, pesos y sensibilidades por eje; el miedo del cuerpo está en las filas de la
  appraisal, congelada) → el carácter va SOLO en la cautela del probar: **prudente** = cautela de P7-40; **valiente** = (1 + cautela) / 2. TECHO lleva una sola
  personalidad. Y SIN EMOCIÓN también: con la moneda pura y el carácter solo en la cautela de la curiosidad (que SIN no tiene), valiente ≡ prudente; se juega UNA variante
  (declarado aquí; es consecuencia de las dos decisiones, no un cambio de diseño).
- **Variantes** (6 imágenes): TECHO, BORRADO_v, BORRADO_p, APRENDE_v, APRENDE_p, SIN. Cuaderno que viaja en APRENDE_* y SIN (cadena de 20 días); BORRADO_* y TECHO fijas.
- Lo desconocido: botiquín, ración, red y camuflaje. Ojos compartidos apagados. Pedir corregido y lo dado entregado. Guardas de P7-30 (latencia marca y sigue, para al
  10 % / 5 %; disco; red; cortes).
- **Semillas** (`semillas_P7_41.json`): k = 221-240; serie 1 en orden, serie 2 inversa, serie 3 rotada diez posiciones; la misma semilla para las 6 variantes cada día.
  **Tres series** × 20 días × 6 variantes = 360 partidas.
- **Humo**: 3 partidas (día 1 de APRENDE_p, SIN y TECHO, serie 1) para probar imágenes y lanzador; cuentan como el día 1 del campo si salen bien.
- **Freno** (como P7-34): días 1-3 de APRENDE_p, serie 1: (a) el cuaderno viaja y se lee; (b) en ≥ 4 de 6 vidas toca alguna de las cuatro cosas; (c) sube la creencia de
  alguna cosa útil; (d) 0 errores de fotos. Si falla, se para y se dice.

## Las medidas (fijadas; por brazo, personalidad y, donde toca, criatura)

- **Rapidez**: primer día en que la creencia (dentro, cuerpo, sin cortes) del botiquín llega a 25 (50 % de 50) y la de la ración a 7,5 (50 % de 15); por criatura en
  APRENDE y SIN, por vida en BORRADO; «no llega» = día 21.
- **Sabiduría**: en los días 11-20, segundos (tics ÷ 24) en `ir_curioso` / `ir_azar` hacia red o camuflaje, con una ventana de prueba de red o camuflaje abierta, o
  llevándolas (zurrón o puestas); y vida perdida en esos tics.
- **Cuándo**: proporción de aperturas de uso del botiquín con hp < 50; y de la ración con hp < 100 (aceptado por la mesa).
- **Puesto medio** (partidas con corte fuera). **Número de pruebas** por brazo, personalidad y día (huellas de las cuatro cosas; en SIN, además, las forzadas).

## Predicciones selladas (de la mesa)

| | predicción | pasa si |
|---|---|---|
| R1 | APRENDE llega antes que SIN EMOCIÓN con el botiquín | el día de rapidez del botiquín, media de las 6 criaturas, es menor en APRENDE_p que en SIN, y en APRENDE_v que en SIN |
| C1 | APRENDE usa el botiquín en necesidad más que SIN EMOCIÓN | la proporción de usos del botiquín con hp < 50 es mayor en APRENDE_p que en SIN, y en APRENDE_v que en SIN |
| S1 | sabiduría | sin predicción: se informa |

Diferencias y errores típicos como en P7-41 (3 errores típicos de la diferencia = «3 veces el ruido»): se informa con cada medida si la diferencia llega a eso.

## Añadidos posteriores al sello

(ninguno al escribirlo)

1. (10-oct-2026, 20:40, en el humo) **La comprobación de la imagen de SIN.** El Dockerfile comprueba al hornear que `descubre_P7.entorno()['brazo']` es el brazo pedido;
   para SIN (cuaderno sí, curiosidad no) descubre lo llama «ESPERANZA» y la comprobación fallaba 64 veces seguidas (una por minuto) sin que ninguna partida se pidiera.
   Se cambia solo esa línea de comprobación (`{'SIN': 'ESPERANZA'}`); ninguna pieza ni conducta cambia. El humo de APRENDE_p d1 ya estaba jugado (asiento 11 marcado por
   la guarda: 1,92 % sobre el tic, mediana 19 ms); se reanuda desde el humo de SIN.

## Addendum (11-oct-2026, 03:00; mesa P7-43 y P7-43b; no se reescribe lo de arriba)

1. **Piloto.** Las 95 partidas de la noche del 10 al 11 (humo 3, freno 2, fijas 60 de la serie 1, cadenas APRENDE_p d1-11, SIN d1-10, APRENDE_v d1-14) quedan como PILOTO:
   se guardan (`paintball/runs/P741p_*`, `P7_41_res_piloto/`, `P7_41_estado_piloto.json`), se cuentan en el apéndice del informe y NO entran en los resultados. La guarda dura
   paró las tres cadenas (6 vidas por encima del 10 % sobre el tic o del 5 % bloqueadas sin cuerpo; la peor, 86 % bloqueada contra una vaina).
2. **Cachés con decisiones idénticas** (`rapido_P7_43.py`, `filo_P7_40.py`): la segunda tasación del regalo por tic y clave de foto; la ignorancia y la curiosidad por
   clase por tic. Comprobado en 6 vidas completas del piloto con sus cuadernos (días 8-13): 69.431 decisiones, 0 distintas (`P7_43_identidad.json`).
3. **Regla del cuerpo de los 72 tics** (3 s), igual en todos los brazos: casilla hacia la que se empuja 72 tics seguidos sin moverse → no transitable el resto de la vida; se
   olvida al morir; registro `P7_43_muro`. (Motivo por el que se quitó la red de muros en P7-29b: aprendía muros para siempre donde había agua temporal; esta regla es por vida.)
4. **Umbral local revisado**: p95 ≤ 8 ms y máximo ≤ 40 ms con cuadernos de días 9-13 (el de 2 ms suponía un factor de plataforma fijo; medido entre 1,8× y 10,7× en la
   misma noche). Medido con cachés y regla: p95 4,8-8,3 ms, máximo 13-37 ms. El criterio real sigue en la plataforma: guarda dura intacta; humo con p95 < 10 ms.
5. **Tope de paralelismo**: nunca más de 20 partidas a la vez en total; prioridad a las cadenas (APRENDE y SIN), las fijas rellenan hasta 20 (`orquesta_P7_43.py`).
6. **Humo**: 3 partidas de APRENDE valiente desde el cuaderno del día 13 del piloto (imagen `HUMO43`, semillas de los días 1-3 de la serie 1), cruzando la ventana de la
   inundación; si p95 ≥ 10 ms en plataforma, se para y se avisa. No entran en los resultados.
7. **Equidad de la lentitud**: por brazo y personalidad y por día, % de decisiones sobre el tic y % de pasos listos bloqueados sin cuerpo; si entre brazos el % sobre el tic
   difiere en más de 2 puntos se marca como dudoso en el informe (no para el campo, salvo la guarda).
8. La serie 1 se juega entera de nuevo con las imágenes nuevas (`Dockerfile.pareja_P7_41` + `rapido_P7_43`); series 2 y 3 después, según créditos.
9. (11-oct-2026, 09:45; mesa P7-43c) **Corte del humo: p95 < 20 ms** (el de 10 ms era un margen a ojo; lo que protege los datos —0 % de decisiones sobre el tic, bloqueos sin cuerpo
   < 0,4 %, guarda dura— pasó en los 6 asientos del humo repetido: medianas 1,9-4,2 ms, p95 7,1-13,8). Un primer humo (09:15) murió al arrancar porque el Dockerfile no copiaba
   `rapido_P7_43.py` (3 créditos; corregido con una comprobación de la composición entera al hornear). **Tope de paralelismo al arrancar: 12 partidas a la vez** (cadenas
   primero); al cerrar el día 1 de las cadenas, si p95 < 20 ms y < 1 % sobre el tic en todos los brazos, sube a 20; si no, sigue en 12.
10. (11-oct-2026, 10:20; mesa P7-43d) **Piloto 2**: las 12 partidas del 11-oct de 09:55 a 10:14 (9 TECHO, d1 de APRENDE_v, APRENDE_p y SIN) con la regla v1 quedan fuera de
    resultados (la guarda dura paró en TECHO s1 d5 a10, 25,6 % bloqueada sin cuerpo). **Regla v3**: la racha cuenta por tiempo de reloj sin moverse (el enfriamiento de las
    piernas no la rompe); la marca dura 30 s (720 tics) y se renueva si vuelve a bloquear 72 tics; se olvida al morir; y los candidatos `ir_*` con destino en una casilla no
    transitable (marcada o cerrada por la ley del agua) salen de la lista (v3b: sin ese veto, TECHO s1 d5 a10 caminaba en línea recta hacia una mochila dentro del agua y
    empujó 411 veces contra (20,22)). **Hallazgo**: en la repetición de la plataforma las casillas «bloqueadas sin cuerpo» llevan sprites `camo_glass`: rivales camuflados,
    invisibles para nosotros; la mayoría de las marcas caen en casillas que luego se pisan (obstáculo móvil): de ahí los 30 s.
    Comprobación (réplica en lazo abierto de las 7 vidas que dispararon la guarda; `P7_43_paradas.json`): empujes de la réplica en la misma dirección que el diario sobre los
    pasos listos: 23,4 % (APRENDE_v d14 a11, que el diario tuvo 4.900 tics pegada a dos casillas: 85,8 %), 4,4 % (APRENDE_p d11 a10, sin marcas: rachas cortas), 4,7 % (SIN
    d10 a11), 2,0 % (BORRADO_p d11 a11, de 11,5), 1,9 % (BORRADO_v d1 a10, de 5,7), 0,7 % (BORRADO_p d9 a10), 0,0 % (TECHO d5 a10, de 24,3). Marcas: 23 (7 luego pisadas),
    0, 8 (6), 50 (36), 5 (5), 1 (0), 3 (3). Latencia local: medianas 0,3-4,2 ms, p95 1,8-9,6, máximo 15-56. El criterio «< 2 % en cada vida» NO se cumple en 3 de 7: en lazo
    abierto el diario deja a la criatura pegada al mismo sitio y la réplica, cuando la marca caduca a los 30 s, vuelve a empujar 72 tics y vuelve a marcar (APRENDE_v: 23 marcas);
    en lazo cerrado la marca la saca de ahí. Se para y se avisa (no se lanza).
11. (11-oct-2026, 10:33; mesa P7-43e) **Las comprobaciones locales dejan de ser barrera** salvo dos exactas: decisiones idénticas con y sin caché (cumplida: 69.431
    decisiones, 0 distintas) y 0 % sobre el tic en local (cumplida en las 7 vidas). Lo demás —incluido el «< 2 %» de bloqueos, que en lazo abierto no puede medir lo que
    la regla hace en lazo cerrado— es diagnóstico: se informa, no frena. Barreras reales, sin cambios: guarda dura en plataforma, equidad ± 2 puntos entre brazos, tope de 12
    con subida a 20 solo si el día 1 cumple. Se lanza la serie 1 con v3b. Vigilar: (1) decisiones de BORRADO sobre el tic (local dio máximos de 43 y 56 ms); (2) si la
    guarda dura salta por bloqueos sin cuerpo, separar rachas < 72 tics (obstáculos que se apartan) de rachas ≥ 72 (que la regla debería haber quitado) antes de pedir decisión.
12. (11-oct-2026, 16:15; mesa) **Cierre de la serie 1.** La guarda dura paró en la última partida de APRENDE prudente (d20 a10, 13,64 % sobre el tic); SIN d20 no llegó a
    pedirse. Decisiones: se pide SIN d20; APRENDE_p d20 tiene UN reintento con el mismo cuaderno (d19) y tope bajo (2 partidas en vuelo); si la guarda vuelve a saltar, ese día
    queda perdido. **Regla de comparación**: solo días con datos válidos en todos los brazos; si falta un d20, todos los brazos se comparan hasta d19. El intento fallido queda
    aparte (`P741r_s1_d20_APRENDE_p_*`, `P7_41_res/intento1_*`), fuera de resultados. Antes de la serie 2: curva de latencia por día y brazo (`latencia_P7_43.py`).
