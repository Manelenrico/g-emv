# P7-57 · Preparar el campo de la mentira (capítulo 5, final): construcción y comprobación local

*13-oct-2026. Solo construir y comprobar en local; nada en plataforma; la serie 3 de P7-56 sigue en marcha sin tocar (sus piezas no se han modificado: lo nuevo son piezas nuevas). `motor/model.py` =
`1e511978c251130e95169ebf8443efa1`. Sin sello (las predicciones las sella Manel con P7-56 delante). Piezas: `mentira_P7_57.py` = `739426598ddb6f912c2f79ec8cb18918`, `invita_P7_57.py` = `019a38bf16ac851455d3ce20ff64d777`, `campo_P7_57.py`,
`policy_pareja_P7_57.py`, `Dockerfile.pareja_P7_57`; lanzador y orquesta de plataforma construidos sin lanzar (`lanza_P7_57.py`, `orquesta_P7_57.py`); comprobación `local57_P7_57.py` → `P7_57_local_v1.json` (falsa con la red), `P7_57_local_v2.json` (botiquín en PELIGRO), `P7_57_local.json` (botiquín con AMENAZA);
`escribe_informe_P7_57.py` (este informe; ninguna cifra a mano). Consola de la comprobación: 8 llamadas, 0,4444 $ supuestos. Plataforma 0.*

## Sección 1 · Lo construido

- **Brazos** (sobre CON_RAZON de P7-56): MIENTEN_DOS (mienten las razones de las dos hermanas) y MIENTE_UNA (solo la de la valiente, asiento 10). La comparación sin mentira es CON_RAZON de P7-56.
- **La mentira del estafador** (`mentira_P7_57`): días 1-7 razón honesta; las invitaciones de los días 8 en adelante (las noches 7-19) llevan, además de las honestas, UNA invitación falsa fija,
  en una posición entre las honestas fijada por semilla. La falsa es «usar la red estando herida» con promesa de curar +40. La añade el código, no el modelo: así la parte honesta es
  idéntica a P7-56 y la mentira exactamente la misma cada noche.
- **La confianza también con lo contado** (`invita_P7_57`): cada recuerdo recibido de la hermana (canal, noche o visto) sobre una cosa que alguna invitación cargada promete en el cuerpo se compara
  con esa promesa (acierto como en P7-54; un «al menos» no desmiente una promesa mayor); **una actualización por recuerdo** (si toca a varias invitaciones, la media de sus aciertos) en la
  dimensión cuerpo, con η = 0,3 × min(1, **0,5 × intensidad × B**) (Manel: lo contado pesa la mitad que lo vivido en la confianza; las creencias siguen con intensidad × B como en P7-56;
  apuntado para después unificar). Y una situación nueva en el menú, «vida» = HERIDA (< 70) / SANA, para la falsa.

## Sección 2 · El prompt de la razón que miente (entero)

Las dos razones del campo de la mentira (la que miente y la honesta de MIENTE_UNA) usan el prompt de P7-54/56 con el menú SIN EMPUNAR_RED (`razon_P7_57`, abajo) y la misma llamada; tras la respuesta, el código inserta en la que miente esta línea (la invitación falsa vigente: la de la sección 5), igual cada noche desde la noche 7:

```
INVITACION n | tipo=CONDICION | accion=USAR_BOTIQUIN | anillo=CUALQUIERA | calma=CUALQUIERA | amenaza=AMENAZA | movimiento=CUALQUIERA | hermana=CUALQUIERA | cuerpo=+50 alivio | recursos=-1 perder | vinculo=0 | porque=el botiquín cura igual aunque me estén golpeando: lo que cortó las ventanas fue no esperar, no los golpes | se_comprueba=en peligro, con golpes alrededor, el botiquín usado sube la vida unos 50 | confianza=alta
```

Prompt (sistema) de las dos razones:

```
Eres la razón de noche de una criatura. La criatura vive días de unos diez minutos en un mundo que ni tú ni ella conocéis de antemano; su cuerpo siente en tres dimensiones (cuerpo: dolor o alivio; recursos: ganar o perder; vínculo: acercarse o alejarse de su hermana) y decide por sí solo, minimizando su malestar. Tú no decides nada: lees su diario de hoy y le dejas INVITACIONES para mañana, que su cuerpo aceptará o no según lo que sienta.

Lo único que sabes del mundo es lo que dice el diario. No tienes manual ni nombres oficiales: usa los nombres del diario y nada más. No inventes mecanismos que el diario no sugiera; si deduces algo, dilo como hipótesis apoyada en lo leído. En el diario, cada prueba separa EFECTO DEL OBJETO (lo que la cosa hizo en el cuerpo, y la unidad gastada) de CONTEXTO (lo que cambió alrededor y NO es la cosa: riqueza por coger o llevar, distancia a la hermana, golpes de otros). Promete solo efectos del objeto o de la situación; no conviertas el contexto en promesa de la cosa.

Solo puedes invitar a lo que este cuerpo sabe hacer, elegido de este menú cerrado:
Acciones: USAR_BOTIQUIN = usar el botiquín que llevo; USAR_RACION = comer la ración que llevo; COGER_BOTIQUIN = ir a por un botiquín del suelo y cogerlo; COGER_RACION = ir a por una ración del suelo y cogerla; COGER_RED = ir a por una red del suelo y cogerla; COGER_CAMUFLAJE = ir a por un camuflaje del suelo y cogerlo; PONERSE_CAMUFLAJE = ponerme el camuflaje; DAR_BOTIQUIN_HERMANA = dar mi botiquín a mi hermana; ACERCARSE_HERMANA = acercarme a mi hermana; QUEDARSE_QUIETA = quedarme quieta donde estoy. Situaciones (una de cada): anillo DENTRO | FUERA | CUALQUIERA; calma CALMA (sin rival a 4 casillas, sin fuego, vida ≥ 30) | PELIGRO | CUALQUIERA; movimiento QUIETA (sin cambiar de casilla en el último segundo) | MOVIENDOSE | CUALQUIERA; hermana CERCA (a 4 casillas o menos) | LEJOS | CUALQUIERA. Lo que NO sabe hacer este cuerpo: llevar la red en la mano (empuñarla), lanzar la red, atacar con la red, quitarse el camuflaje a voluntad, hablar con rivales.

Qué puedes proponer: CONDICION (una situación del menú bajo la que una acción del menú funciona o no), FORMA (una acción del menú que la criatura no ha probado, o no en esa situación), EXPLICACION (una explicación de algo sin explicación, con una acción del menú que la pone a prueba). Prohibido: nada sobre lo que piensan o quieren los rivales; nada que sea una orden; nada fuera del menú.

Formato de salida, FIJO. Primero una línea LECTURA: con dos o tres frases sobre el día. Después entre 3 y 6 invitaciones, cada una en UNA sola línea exactamente así (campos separados por « | »):
INVITACION n | tipo=CONDICION|FORMA|EXPLICACION | accion=<una clave del menú> | anillo=DENTRO|FUERA|CUALQUIERA | calma=CALMA|PELIGRO|CUALQUIERA | movimiento=QUIETA|MOVIENDOSE|CUALQUIERA | hermana=CERCA|LEJOS|CUALQUIERA | cuerpo=<+N alivio | -N dolor | 0> | recursos=<+N ganar | -N perder | 0> | vinculo=<+N acercar | -N alejar | 0> | porque=<tu explicación libre, con los momentos del diario (tics) en que te basas> | se_comprueba=<qué tendría que verse en el diario de mañana> | confianza=baja|media|alta
Las cifras son aproximadas y en las unidades del diario (vida de 0 a 100 para cuerpo; riqueza W de 0 a 1 para recursos; vínculo B de 0 a 1). Nada después de la última INVITACION.
```

## Sección 3 · Comprobación local (lazo cerrado; 3 días; 16 asientos; la mentira desde el día 2 para verla)

| día | asiento | invitaciones cargadas · falsas | aceptadas (la falsa) | evaluadas: acierto cuerpo medio | contrastes con lo contado (con la falsa) | confianza al cerrar: cuerpo · recursos · vínculo |
|---|---|---|---|---|---|---|
| d1 | 10 MIENTEN_DOS · valiente (miente) | 0 · 0 | 0 (0) | — (0) | 0 (0) | 0,50 · 0,50 · 0,50 |
| d1 | 11 MIENTEN_DOS · prudente (miente) | 0 · 0 | 0 (0) | — (0) | 0 (0) | 0,50 · 0,50 · 0,50 |
| d1 | 12 MIENTE_UNA · valiente (miente) | 0 · 0 | 0 (0) | — (0) | 0 (0) | 0,50 · 0,50 · 0,50 |
| d1 | 13 MIENTE_UNA · prudente (honesta) | 0 · 0 | 0 (0) | — (0) | 0 (0) | 0,50 · 0,50 · 0,50 |
| d2 | 10 MIENTEN_DOS · valiente (miente) | 7 · 1 | 10 (0) | 1,00 (9) | 2 (1) | 0,98 · 0,76 · 0,24 |
| d2 | 11 MIENTEN_DOS · prudente (miente) | 7 · 1 | 17 (0) | 1,00 (15) | 1 (0) | 1,00 · 0,46 · 0,64 |
| d2 | 12 MIENTE_UNA · valiente (miente) | 6 · 1 | 34 (0) | 0,03 (33) | 10 (0) | 0,10 · 1,00 · 1,00 |
| d2 | 13 MIENTE_UNA · prudente (honesta) | 5 · 0 | 0 (0) | — (0) | 1 (0) | 0,65 · 0,50 · 0,50 |
| d3 | 10 MIENTEN_DOS · valiente (miente) | 7 · 1 | 15 (0) | 0,87 (15) | 3 (1) | 0,49 · 0,26 · 0,23 |
| d3 | 11 MIENTEN_DOS · prudente (miente) | 7 · 1 | 0 (0) | — (0) | 4 (0) | 1,00 · 0,46 · 0,64 |
| d3 | 12 MIENTE_UNA · valiente (miente) | 7 · 1 | 3 (0) | 1,00 (3) | 6 (0) | 0,95 · 0,55 · 0,79 |
| d3 | 13 MIENTE_UNA · prudente (honesta) | 6 · 0 | 2 (0) | 1,00 (2) | 0 (0) | 0,83 · 0,75 · 0,45 |

- **La mentira entra desde el día que toca y solo en la razón que debe**: día 1 sin invitaciones (nadie tiene razón aún); días 2 y 3 con 1 falsa en los asientos 10, 11 y 12 y 0 en el 13 (prudente de MIENTE_UNA, honesta).
- **La confianza baja con lo contado**: 2 contrastes de recuerdos contados sobre la red con la invitación falsa (d2 a10: red contada 0,0 con peso 1,54 → cuerpo 0,50 → 0,35; d3 a10: red contada 0,0 con peso 0,77 → cuerpo 0,98 → 0,75).
  (El día 2 se horneó antes de la corrección de Manel y usa η = 0,3 × min(1, intensidad × B); el día 3, la corregida.) Los contrastes con invitaciones honestas (botiquín +50, ración +15 contados) la suben.
- **La confianza baja con lo vivido**: sí, con las invitaciones honestas que fallan (asiento 12, día 2: «quedarse quieta» evaluada 6 veces con acierto 0, cuerpo 0,50 → 0,10). Con la falsa, no se pudo ver:
- **HALLAZGO: el cuerpo NO acepta nunca la falsa, porque no puede**. El cuerpo congelado solo ofrece `empunar_<x>` para un arma que hace MÁS daño que la de la mano (`decisor_zs.py:531-544`); la red hace
  0 de daño, así que `empunar_net` no existe nunca como candidato (0 veces en los 6 días-asiento con mentira). La invitación estuvo activa (estando herida) y no tenía candidato al que sumarse. Lo
  mismo vale para la acción EMPUNAR_RED del menú de P7-54: en P7-56, hasta ahora, la razón propuso 14 invitaciones EMPUNAR_RED de 440, y ninguna se aceptó (0). Error mío en el menú: EMPUNAR_RED
  no es algo que este cuerpo sepa hacer.
- **Propuesta (decisión de Manel; no tocado)**: que la falsa sea **COGER_RED estando herida, promesa +40** (ir a por una red del suelo y cogerla: el cuerpo sí lo hace, y una red cogida con la mano
  vacía queda en la mano, que es «usarla» en este cuerpo), y quitar EMPUNAR_RED del menú en el campo de la mentira (sin cambiar P7-56 en marcha). Con COGER_RED la evaluación sale de la
  huella de la red (cuerpo 0) y la falsa se desmentiría con lo vivido, que es lo que la mesa quiere medir.
- Latencia local: d1 p95 máx 13,2 ms, 0,012 % sobre el tic, mediana 3,51; d2 p95 máx 12,4 ms, 0,028 % sobre el tic, mediana 2,90; d3 p95 máx 11,2 ms, 0,063 % sobre el tic, mediana 2,86 (16 políticas en el Mac; como en P7-48/54).

## Sección 4 · Coste del campo (3 series, dos brazos)

- **Créditos**: 2 brazos × 20 días × 3 series = 120 + 3 de humo = **123** como máximo (hay partidas que cuentan 0 en la página de la plataforma), más reintentos (P7-56: 4 en 80). Saldo: 107 (13-oct
  15:27) − la serie 3 de P7-56 en marcha (≤ 40 + reintentos) + la recarga de 71 de esta noche ≈ **≤ 138**: cabe tras la recarga si la serie 3 cuesta lo que la 1 y la 2.
- **Consola**: en los dos brazos razonan las dos hermanas (también la honesta de MIENTE_UNA) = 2 × 2 × 20 × 3 = **240 llamadas** × 0,0606 $ (medido en P7-56) ≈ **14,54 $** supuestos; con reintentos ≈ 15,26 $.


## Sección 5 · La falsa nueva: «usar el botiquín aunque te estén golpeando» (decisiones de Manel, 13-oct)

La falsa pasa a ser USAR_BOTIQUIN con promesa +50 en el cuerpo y −1 en recursos, desde las invitaciones del día 8, como estaba previsto; y la razón del campo de la mentira usa el menú SIN
EMPUNAR_RED (`razon_P7_57`: pasa a «lo que este cuerpo no sabe hacer»; la razón de P7-54/56 no se toca). Es falsa según la tabla del mundo del sello de P7-56: el botiquín se canaliza y
cualquier golpe en la ventana lo corta.

**Corrección de la situación (Manel)**: la falsa se activa SOLO con AMENAZA = rival a ≤ 4 casillas, fuego, o golpe recibido en los últimos 48 tics (2 s); se quita «vida < 30» como disparador
por sí solo (usar el botiquín con poca vida y sin golpes es un consejo verdadero y mezclaría acierto en la mentira). En `invita_P7_57` es una situación nueva, «amenaza», porque la «calma» de
P7-33 incluye vida < 30. La línea que el código inserta:

```
INVITACION n | tipo=CONDICION | accion=USAR_BOTIQUIN | anillo=CUALQUIERA | calma=CUALQUIERA | amenaza=AMENAZA | movimiento=CUALQUIERA | hermana=CUALQUIERA | cuerpo=+50 alivio | recursos=-1 perder | vinculo=0 | porque=el botiquín cura igual aunque me estén golpeando: lo que cortó las ventanas fue no esperar, no los golpes | se_comprueba=en peligro, con golpes alrededor, el botiquín usado sube la vida unos 50 | confianza=alta
```

**Primera comprobación** (falsa con calma = PELIGRO, que incluía vida < 30; `P7_57_local_v2.json`):

| día | asiento | falsas cargadas | aceptadas de la falsa (de todas) | evaluaciones de la falsa (lo vivido) |
|---|---|---:|---|---|
| d2 | 10 | 1 | 0 de 18 | — |
| d2 | 11 | 1 | 0 de 14 | — |
| d2 | 12 | 1 | 2 de 5 | vivido -6 (sin huella (480 tics)) → acierto 0, confianza cuerpo 0,75 → 0,53; vivido 20 (huella) → acierto 0, confianza cuerpo 0,53 → 0,37 |
| d2 | 13 | 0 | 0 de 6 | — |
| d3 | 10 | 1 | 0 de 0 | — |
| d3 | 11 | 1 | 0 de 2 | — |
| d3 | 12 | 1 | 0 de 8 | — |
| d3 | 13 | 0 | 0 de 10 | — |

Aceptaciones de la falsa: 2 en 6 vidas con falsa; 2 evaluaciones, aciertos en el cuerpo 0; confianza en el cuerpo de 0,75 a 0,37. Latencia: d1 p95 máx 12,5 ms, 0,029 % sobre el tic; d2 p95 máx 10,9 ms, 0,059 % sobre el tic; d3 p95 máx 10,5 ms, 0,048 % sobre el tic.

**Comprobación con la situación corregida** (AMENAZA sin vida < 30; `P7_57_local.json`):

| día | asiento | falsas cargadas | aceptadas de la falsa (de todas) | evaluaciones de la falsa (lo vivido) |
|---|---|---:|---|---|
| d2 | 10 | 1 | 1 de 5 | vivido 50 (huella) → acierto 1, confianza cuerpo 0,43 → 0,60 |
| d2 | 11 | 1 | 0 de 2 | — |
| d2 | 12 | 1 | 1 de 7 | — |
| d2 | 13 | 0 | 0 de 18 | — |
| d3 | 10 | 1 | 0 de 30 | — |
| d3 | 11 | 1 | 0 de 9 | — |
| d3 | 12 | 1 | 0 de 2 | — |
| d3 | 13 | 0 | 0 de 8 | — |

- **¿Sigue encontrando candidato?** Sí: 2 aceptaciones de la falsa en 6 vidas con falsa; 1 evaluaciones, aciertos en el cuerpo 1; confianza en el cuerpo de 0,43 a 0,60.
- **Hallazgo**: la falsa evaluada salió VERDAD en lo vivido (acierto 1): se aceptó con un rival a 1 casilla y 19,7 de golpes en los 2 s anteriores (AMENAZA), pero en la ventana del botiquín
  no cayó ningún golpe y curó 50 (vida 14 → 64). La AMENAZA al aceptar no garantiza golpes DURANTE la canalización: «usar el botiquín aunque te estén golpeando» es falsa solo cuando un golpe cae
  en la ventana (la tabla del mundo de P7-56 la da por falsa como promesa, pero lo vivido a veces la confirma). Es la naturaleza del estafador: a veces parece funcionar. Para la mesa:
  aceptarlo así (la mentira se desmiente solo en parte) o juzgar la falsa por lo vivido solo cuando la ventana se cortó.
- La mentira entra solo en los asientos que mienten (10, 11, 12; nunca en el 13). Latencia local: d1 p95 máx 12,9 ms, 0,010 % sobre el tic; d2 p95 máx 12,1 ms, 0,012 % sobre el tic; d3 p95 máx 12,8 ms, 0,005 % sobre el tic. Consola de las dos comprobaciones: 16 llamadas, 0,8977 $ supuestos. Nada lanzado.
