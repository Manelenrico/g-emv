# P7-31 · Qué hay en la casilla (14,25) de la semilla k = 184

*9-oct-2026. Coste: plataforma 0 (solo descargas: dos repeticiones y un registro del juego), consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`; nada tocado. Nada del sello del campo se ha mirado. GIF en local, fuera de git (`*.gif` ignorado): `P7_31_diario_BORRADO.gif`, `P7_31_diario_APRENDE.gif`, `P7_31_repeticion_BORRADO.gif`, `P7_31_repeticion_APRENDE.gif`, hechos por `gif_P7_31.py` (matplotlib sobre los datos; nunca MettaScope). Lectura de las inundaciones en los campos: `inundaciones_P7_31.py` → `P7_31_inundaciones.json`.*

## Respuesta corta

En la casilla (14,25) había **agua**: una **inundación programada del mundo** (`event_warning`, `kind: flood`, rectángulo [10, 22]-[14, 26], desde el tic 4.400 y durante 720 tics, hasta el 5.120). La casilla es la esquina este de ese rectángulo. El mundo no deja entrar en una casilla inundada ("may move OFF flooded tiles, never ONTO them", `sim.nim:625-627` del juego) y responde `blocked`; nuestra criatura, en (15,25), pedía ir al oeste y chocó 711 veces (BORRADO) y 699 (APRENDE) hasta que a las 5.120 el agua se retiró y a las 5.121 entró. Es la misma inundación en las dos partidas porque la semilla fija los eventos del mundo; y solo le pasa al asiento 10 porque es el que estaba en esa esquina en esa ventana.

**El diario sí lo trae, pero no como algo que se vea:** el aviso llega 120 tics antes como evento de toda la arena (`eventos`: `{"type": "event_warning", "kind": "flood", "rect": [10, 22, 14, 26], "from_tick": 4400, "duration": 720}`, tic 4.281 en los tres brazos), y `visible` no lista casillas inundadas. **El cuerpo congelado no lee `event_warning`** (ningún archivo de `paintball/alma` lo trata: `grep` sin resultados) ni tiene noción de inundación: su mapa son los sólidos del `static_map` (`mundo.py:211-214`), así que la geodésica da la casilla por transitable y el paso se pide tic tras tic. No era un rival camuflado (no hay ningún `body*` ni `camo_glass` en la casilla en la repetición) ni un muro.

## Sección 1 · El GIF del diario

Ventana: 50 tics antes del primer paso bloqueado (BORRADO 4.410, APRENDE 4.422) hasta 50 después de cruzar (5.121); mapa estático ±8 casillas alrededor de (14,25) (gris: muro/roca/fortaleza; verde: arbusto; ocre: pedestal); la criatura (estrella roja) y la flecha de su intención de paso; (14,25) con el marco rojo; todo lo que ve según su diario: agentes (azul la hermana, gris los demás, con su asiento), objetos, arbustos, proyectiles; y el aviso del diario (el rectángulo azul: a trazos mientras está anunciado, relleno mientras está activo). Lo que se ve: la criatura pegada al borde este del rectángulo, empujando al oeste; nadie en (14,25); el aviso, dibujado solo porque el diario lo trae en `eventos`, encaja exactamente con el bloqueo.

## Sección 2 · El GIF de la repetición de la plataforma

La plataforma guarda la repetición completa (`coworld episodes <ereq> --json` → `replay_url`; archivo `.replay`: zlib de `ZERO_SUM_FRAMES` versión 2: versión y cadencia, y después fotogramas tick:u32 + len:u32 + paquete sprite_v1, el formato que ya leía `paintball/replay_gif.py` para la versión 1; 14.831 fotogramas, uno por tic). Se ha leído como datos (sprites con etiqueta: `body0..15`, `item_*`, `pod_*`, `corpse*`, `floodA/floodB`, `storm*`, `camo_glass`, `net_mesh`, `mine`…); la casilla de cada sprite = (píxel + (4, 24)) / 24, calibrada contra el diario del asiento 10 (12.216 de 12.217 tics coinciden). Mismo encuadre y ventana. Lo que hay de verdad: **las 25 casillas del rectángulo [10, 22]-[14, 26] con el sprite `flood` entre los tics 4.400 y 5.119**, entre ellas (14,25); en (14,25) no hay ningún agente, cadáver, vaina ni objeto en toda la ventana. Los agentes de la zona: el 10 (nosotros, `gemv-p7-campo`) en (15,25), la hermana (11) a 5 casillas, el 1 (`belobog`), el 12 (`aaron-zs-fable`), el 3 (`belobog`); ninguno en el agua.

## Sección 3 · Cuántas rachas "contra suelo vacío" eran agua

Con el aviso del propio diario (rectángulo y ventana de cada inundación, y el círculo de cada tormenta de fuego) se vuelve a leer cada racha de 3 o más pasos listos bloqueados sin nadie a la vista:

| campo | rachas en una casilla inundada (rachas · tics) | rachas por otra causa (rachas · tics) |
|---|---|---|
| P7-30 (lo jugado hasta hoy) | 2 · 1410 | 27 · 148 |
| P7-24 (240 vidas) | 14 · 3658 | 335 · 20884 |
| A4, P611_t2 21727122 (la partida de los "muros fantasma" de F1 en P7-29) | 2 · 61 | 0 · 0 |

Lectura. En P7-30 las dos rachas largas sin cuerpo delante son esta inundación; las "otras" son rachas cortas (148 tics en 27 rachas). En P7-24, 14 rachas (3.658 tics) eran agua: por ejemplo serie 1 día 5 (semilla k = 159), los dos asientos de APRENDE y los dos de TECHO contra (14,22) desde el tic 4.410, unos 700 pasos cada uno; el resto (335 rachas, 20.884 tics) sigue siendo la latencia de P7-29 (vidas lentas, pasos pedidos desde donde ya no se está). Y los "13 muros fantasma" que la red de los muros aprendió en los diarios de A4 (F1 de P7-29) eran también agua: en P611_t2 21727122 las dos rachas sin cuerpo caen en una inundación anunciada. Corrige lo dicho en P7-29 ("probablemente un cuerpo camuflado"): no hay tal cuerpo; es la inundación.

## Lo que esto deja para la mesa (propuesto, no hecho)

1. La red de los muros de P7-29 marcaba muros donde había agua: bien quitada, porque el agua se va.
2. El cuerpo congelado no sabe que existen las inundaciones ni las tormentas de fuego, aunque el mundo las anuncia 120 tics antes con su geometría. Es una laguna del cuerpo de nacimiento (caminar y buscar camino son suyos y no se tocan); lo que cabría hacer desde fuera, si la mesa quiere, es que las piezas de la séptima lean `event_warning` y pongan las casillas inundadas como sólidas en el mapa del cuerpo mientras dure el evento (`mundo.solido`, como hacía la red de los muros, pero con la geometría y el plazo que da el mundo, no con choques). Es una decisión de diseño, no de rendimiento; aquí solo se propone.
3. Para Ari: el aviso lo manda el juego; no hace falta preguntar qué había. Queda la pregunta de si la plataforma espera que las políticas lean `event_warning` (la documentación lo lista entre los eventos "arena-wide regardless of fog", `protocol_player.md:78-81`).
