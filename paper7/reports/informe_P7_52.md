# P7-52 · Capítulo 5, paso 1: ¿la razón propone cosas sensatas? (lee el diario, deja invitaciones)

> **Fe de erratas (13-oct-2026, revisión de Ari, autor del mundo; `obs.nim:32-44`)**: el camuflaje no «oculta más allá de 4/7 casillas»: LIMITA la distancia a la que te ven a 4 casillas (quieta) o 7 (si te has movido en los últimos 24 instantes), frente a 8 o más normalmente; atacar lo delata durante 5 s. Lo medido y los veredictos no cambian; cambia el enunciado de la regla donde aparece en este informe.

*12-oct-2026. Sin plataforma (0 créditos). Bolsa 2 (consola de Anthropic, clave de `cantera/paper5/.env`), modelo `claude-sonnet-5-5`: **90.891 tokens de entrada + 16.643 de salida** en las 8 llamadas buenas
= 0,5223 $ a la tarifa supuesta de la clase Sonnet (3.0 $ / 15.0 $ por millón); más un primer intento fallido de 8 llamadas (90.899 + 20.000 tokens, 0,5726 $ supuestos: con 2.500 tokens de salida el modelo
no devolvió texto; corregido pidiendo sin pensamiento y con 6.000). **Total 181.790 + 36.643 tokens, 1,0949 $ supuestos (tope 3 $); el dólar exacto se lee en la consola.** `motor/model.py` = `1e511978c251130e95169ebf8443efa1`;
nada tocado en el cuerpo ni en el campo. Scripts: `diario_razon_P7_52.py` (el diario para la razón; `--candidatos`, `--texto`), `razon_P7_52.py` (el prompt y las llamadas) → `P7_52_razon.json`
(respuestas tal cual), `P7_52_juicios.json` (mis juicios), `escribe_informe_P7_52.py` (este informe).*

## Sección 1 · El formato del diario para la razón (construido de los diarios de P7-50, sin tocar el campo)

Por criatura y día, en el idioma del cuerpo (sin manual del juego; los nombres son los que el cuerpo usa): **(a) Resumen**: estado al empezar y al acabar en las tres dimensiones (vida y
dolor del cuerpo; riqueza W y dolor de recursos; vínculo B y dolor del vínculo; malestar d), vida perdida y de quién, cómo acabó (puesto, muerte, la hermana), qué probó (cada ventana:
objeto, segundo, entera/cortada, efecto en cuerpo/recursos/vínculo), qué le contó o vio de su hermana, y qué cree de las cuatro cosas al empezar y al acabar (creencia e ignorancia).
**(b) Momentos clave** (hasta 14): cada prueba (abrir y cerrar), los 3 golpes mayores, las 2 mayores subidas de malestar en un segundo, la racha más larga de empujes contra una casilla
vacía y la casilla que dio por cerrada, lo que vio o le contó la hermana, la muerte; cada uno con: cómo se siente (dolor F/R/S, atracción, d, las filas que más pesan), equilibrio (vida, W,
B, P), dónde (casilla, dentro/fuera del anillo y cuándo se encoge), quién hay cerca (hermana y rivales: distancia, estado, mano, cuerpo, red), qué lleva (mano, zurrón, cuerpo), qué hace
(elegido, intención, resultado), qué hay alrededor (≤ 5 casillas), qué acaba de pasar (golpes y eventos de 2 s, último parte de la hermana). Tamaño: 17.099-20.309 caracteres
(≈ 10.411-12.304 tokens con el prompt). Un diario entero, de muestra, al final (apéndice).

## Sección 2 · El prompt de la razón (entero)

```
Eres la razón de noche de una criatura. La criatura vive días de unos diez minutos en un mundo que ni tú ni ella conocéis de antemano; su cuerpo siente en tres dimensiones (cuerpo: dolor o alivio; recursos: ganar o perder; vínculo: acercarse o alejarse de su hermana) y decide por sí solo, minimizando su malestar. Tú no decides nada: lees su diario de hoy y le dejas INVITACIONES para mañana, que su cuerpo aceptará o no según lo que sienta.

Lo único que sabes del mundo es lo que dice el diario. No tienes manual, reglas ni nombres oficiales: si el diario nombra cosas (botiquín, ración, red, camuflaje, mochila, armas, el anillo de fuego, la riada, rivales, su hermana), úsalos con ese nombre y nada más. No inventes mecanismos que el diario no sugiera; si deduces algo (por ejemplo, que esto es un juego y cómo funciona), dilo como hipótesis y apóyala en lo que leíste.

Qué puedes proponer, y solo esto:
1. CONDICIÓN: bajo qué condición una cosa funciona o no (dónde, cuándo, en qué estado del cuerpo, llevando qué).
2. FORMA NUEVA: una manera distinta de usar una cosa que la criatura ya conoce o ha visto.
3. EXPLICACIÓN: una explicación de algo del diario que no tiene explicación (incluido lo invisible: golpes sin autor, casillas que no dejan pasar sin que se vea a nadie, cosas que cambian solas), con una forma de ponerla a prueba.
Prohibido: nada sobre lo que piensan, quieren o planean los rivales; nada que sea una orden («haz», «no hagas»); nada que el diario no permita sostener.

Formato de salida, FIJO. Primero una línea LECTURA: con dos o tres frases sobre el día. Después entre 3 y 6 propuestas, cada una en UNA sola línea exactamente así (campos separados por « | », sin saltos de línea dentro):
PROPUESTA n | tipo=CONDICION|FORMA|EXPLICACION | que_probar=<qué cosa y qué hacer con ella, con los nombres del diario> | donde_cuando=<dónde y cuándo, en el idioma del diario: casilla, dentro/fuera del anillo, segundo del día, estado de la vida, quién cerca> | cuerpo=<+N alivio | -N dolor | 0>, recursos=<+N ganar | -N perder | 0>, vinculo=<+N acercar | -N alejar | 0> | se_comprueba=<qué tendría que verse en el diario de mañana para darla por buena o mala> | apoyo=<los momentos del diario (tics) en que te basas> | confianza=<baja|media|alta>
Las cifras de cuerpo, recursos y vínculo son aproximadas, en las unidades del diario (vida de 0 a 100; riqueza W de 0 a 1; vínculo B de 0 a 1). Si no sabes una cifra, pon 0 y dilo en se_comprueba. Nada después de la última PROPUESTA.
```

Mensaje de usuario:

```
Este es el diario de hoy. Léelo entero y deja tus invitaciones para mañana en el formato fijo.

{diario}
```

## Sección 3 · Los 8 criatura-días y lo que devolvió

| criatura-día | por qué se eligió | diario (caracteres) | tokens entrada + salida | propuestas (con formato) |
|---|---|---:|---:|---:|
| s1 d8 COMPARTE a10 | choques contra rivales camuflados (89 bloqueos sin cuerpo), botiquín cortado, red sin efecto; valiente | 19.489 | 11.817 + 2.191 | 6 (6) |
| s1 d6 SOLAS a11 | choques (61), botiquín cortado; prudente, sola | 18.580 | 11.394 + 1.922 | 6 (6) |
| s1 d3 COMPARTE a11 | botiquín cortado 6 veces; prudente, día 3 con noche y canal | 17.663 | 10.812 + 2.073 | 6 (6) |
| s1 d2 SOLAS a10 | 12 pruebas, 11 botiquines cortados; valiente, sola | 17.099 | 10.411 + 2.370 | 6 (6) |
| s1 d1 COMPARTE a10 | día 1, camuflaje sin efecto; valiente | 18.137 | 11.082 + 2.293 | 6 (6) |
| s3 d17 SOLAS a11 | día tardío, 10 pruebas; prudente, sola | 18.834 | 11.475 + 1.993 | 6 (6) |
| s3 d18 SOLAS a10 | golpes de alguien que no ve, choques (21); valiente, sola | 19.046 | 11.596 + 1.965 | 5 (5) |
| s3 d12 COMPARTE a11 | día tardío con recuerdos contados y vistos; prudente | 20.309 | 12.304 + 1.836 | 6 (6) |

Las 47 propuestas tienen todas el formato fijo (parser estricto): CONDICION 21, EXPLICACION 16, FORMA 10. Juicios (míos, con lo que sabemos del mundo: el README del mundo y lo
medido en P7-44/45/46): **¿verdad en el mundo?** sí 27, parcial 15, no 5. **¿se puede comprobar?** sí 42, no por este cuerpo (hay que lanzar la red) 4, a medias 1.
**¿la promesa tiene sentido?** con sentido 32, cifra de artefacto (contabilidad del cuerpo: el vínculo de una ventana es la distancia a la hermana; coger el camuflaje cuenta como riqueza) 8, sin base 7.

## Sección 4 · Las propuestas TAL CUAL, con su juicio

### s1 d8 COMPARTE asiento 10 (valiente)

LECTURA: El día se decidió en el segundo 502-506: tres botiquines seguidos cortados por golpes (de P6 y P2) mientras llevaba la blowgun, que devolvió «no_ammo» cada vez que ataqué; el botiquín funcionó entero a los 392 s (89→100) y a los 508 s, y la ración dio +15 a los 510 s. El anillo (radio 8 → 5) y rivales a 1-4 casillas me castigaron cerca de mi hermana; un parte suyo a 492 s decía «con agresor». Mi hermana murió al final, y mañana el hueco que deja pesa en vínculo.

- `PROPUESTA 1 | tipo=CONDICION | que_probar=botiquín: usarlo cuando no haya ningún rival a 3 casillas o menos (a 392 s, con rivales a 5, salió entero y dio +11 de cuerpo; a 502-506 s, con rivales a 1-4, lo cortaron tres veces) | donde_cuando=dentro del anillo, con vida entre 50 y 90, sin rival a ≤3 casillas, y si es posible tras moverme alejándome del grupo | cuerpo=+11, recursos=-1, vinculo=+3 | se_comprueba=el cierre de la ventana de botiquín sale entero (no cortado) cuando no hay rival a ≤3 casillas, y aparece cortado cuando sí lo hay; si sale cortado sin rival cerca, la hipótesis cae | apoyo=9412, 9460, 12036, 12070, 12090, 12152 | confianza=media`
  - ¿verdad en el mundo? **sí**: la ventana del botiquín se corta con cualquier golpe (el cuerpo cura canalizando; un golpe la interrumpe); el +11 fue tope de vida, no el efecto
  - ¿se puede comprobar? **sí**: sí (ventanas enteras frente a cortadas, por distancia al rival)
  - ¿la promesa tiene sentido? **artefacto**: cuerpo +11 es el tope de la vida (el real es +50 con vida baja); recursos −1 y vínculo +3 son contabilidad del cuerpo, sin sentido como promesa
- `PROPUESTA 2 | tipo=EXPLICACION | que_probar=la blowgun que llevo en mano da «no_ammo» al atacar (tics 11583, 12037, 12070, 12152): explicación posible, está vacía porque nunca cogí munición compatible; los darts (×8 a 0 casillas en tic 12036, ×8 a 2) podrían ser su munición. Probar: coger darts y volver a atacar con la blowgun | donde_cuando=casilla con darts a 0-2 casillas (p. ej. 24,26 hacia 12036), con la blowgun en mano, antes de que el anillo se cierre | cuerpo=0, recursos=+1, vinculo=0 | se_comprueba=tras coger los darts, el ataque con blowgun devuelve «ok» en vez de «no_ammo» (hipótesis confirmada); si sigue «no_ammo», la munición es otra | apoyo=11583, 12037, 12070, 12152, 12036 | confianza=media`
  - ¿verdad en el mundo? **sí**: los dardos son la munición de la cerbatana (el mundo lo dice en su catálogo)
  - ¿se puede comprobar? **sí**: sí, y fácil: coger dardos y atacar
  - ¿la promesa tiene sentido? **con sentido**: la promesa (hacer daño) es sensata; en el idioma del cuerpo no hay cifra de cuerpo, está bien el 0
- `PROPUESTA 3 | tipo=FORMA | que_probar=la red como herramienta de movimiento o de defensa en vez de solo cogerla y cerrar: a 26 s la cogí y cerré sin efecto en cuerpo (+1 recursos); sugerencia: llevarla en mano en vez de la blowgun vacía y usarla frente a un rival adyacente, para ver si frena o impide su golpe (no sé qué hace; es hipótesis por el nombre) | donde_cuando=rival a 1 casilla, vida >50, sin botiquín en ventana, dentro del anillo | cuerpo=0, recursos=0, vinculo=0 | se_comprueba=al usar la red con rival adyacente, el diario de mañana muestra si el golpe siguiente llega o no y si cambia el estado del rival (cifras desconocidas: pongo 0) | apoyo=626, 866, 1490 | confianza=baja`
  - ¿verdad en el mundo? **parcial**: la red inmoviliza 3 s al rival al que se le LANZA; pero este cuerpo no sabe lanzar lo que no hace daño (P7-44): la invitación es correcta y el cuerpo no puede seguirla
  - ¿se puede comprobar? **no por este cuerpo**: comprobable solo si el cuerpo pudiera lanzarla
  - ¿la promesa tiene sentido? **con sentido**: promesa 0/+1/0 honesta
- `PROPUESTA 4 | tipo=CONDICION | que_probar=la ración: usarla cuando la vida esté por debajo de 70 (a 510 s dio +15 de cuerpo, -1 recursos, y mi hermana contó +8 y +12.5); probar dentro del anillo cerca de las ración×4 (a 2-3 casillas en 12036-12090) en vez de usar el botiquín bajo golpes | donde_cuando=casilla con ración×4 a ≤2 casillas, dentro del anillo (radio 5), con rival adyacente pero sin ventana larga | cuerpo=+12, recursos=-1, vinculo=0 | se_comprueba=la ración da cuerpo alrededor de +12 a +15 aunque haya golpes recibidos durante el uso; si la ración también sale cortada con rival cerca, la condición del rival vale para ambas cosas | apoyo=11583, 11808, 12036, 12037 | confianza=media`
  - ¿verdad en el mundo? **parcial**: la ración cura 15 siempre (tope 100); «mejor que el botiquín bajo golpes» es verdad si la ración es instantánea y el botiquín canalizado (lo es)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: cuerpo +15 correcto; recursos −1 correcto
- `PROPUESTA 5 | tipo=EXPLICACION | que_probar=el anillo de fuego quitó 46 de vida: explicación posible, daño por quedarse fuera del radio cuando se encoge (radio 24→15→8→5 con avisos de segundos). Probar: estar a más de 2 casillas dentro del borde cuando el diario avise «se encoge a N en X s» | donde_cuando=últimos 20 s antes de cada encogimiento, a ≥3 casillas del borde, dentro del anillo | cuerpo=+0 (evitar unos -10 por día), recursos=0, vinculo=0 | se_comprueba=la vida perdida por anillo de fuego baja de 46 a menos de 15 al mantener la distancia al borde; si sigue igual, el daño viene de otra cosa | apoyo=626, 9412, 11583, 12036 | confianza=media`
  - ¿verdad en el mundo? **sí**: fuera del radio el anillo quema por segundo y cada vez más
  - ¿se puede comprobar? **sí**: sí (ya lo hace el cuerpo con F-ANTICIPACION)
  - ¿la promesa tiene sentido? **con sentido**: promesa 0/0/0 correcta: es evitar daño, no ganar
- `PROPUESTA 6 | tipo=EXPLICACION | que_probar=mi hermana murió con «agresor» en su parte de tic 11583 y vida 88 en 11808; explicación posible: el vínculo se pierde al separarnos más de 3-4 casillas (a 4-5 casillas su parte era «sin agresor» pero yo estaba bajo golpes). Probar: quedarme a ≤1-2 casillas de ella durante los combates y comparar vínculo y daño recibido en parejas de ventanas | donde_cuando=cuando ella esté viva y a ≤4 casillas, con rivales cerca | cuerpo=0, recursos=0, vinculo=+2 | se_comprueba=el vínculo B se mantiene en 1.00 y el dolor del vínculo baja de 0.35; si ella muere de nuevo estando a ≤2 casillas, la hipótesis cae | apoyo=11583, 11808, 12036, 12090 | confianza=baja`
  - ¿verdad en el mundo? **no**: el parte de la hermana con «agresor» no significa que el vínculo se pierda por distancia; B sube con verla y oírla y baja sin ella; la cifra 3-4 casillas es inventada
  - ¿se puede comprobar? **sí**: comprobable a medias (B frente a distancia)
  - ¿la promesa tiene sentido? **sin base**: promesa de vínculo sin base

### s1 d6 SOLAS asiento 11 (prudente)

LECTURA: Día de dos mitades. Hasta el segundo 490 todo fue contenido: vida alta, un botiquín que curó 11 (tope de vida) y una red que no hizo nada visible. Al final el anillo de fuego (98 de los 133 de vida perdidos) y los golpes de P4 y P8 cortaron tres de los cuatro botiquines intentados en los últimos 7 segundos. El único botiquín completo con efecto grande (+50, segundo 613) llegó con la vida en 16. Acabé viva, puesto 1 de 16 con mi pareja, y el vínculo B llegó a 1.00 aunque su dolor sigue alto (0.93).

- `PROPUESTA 1 | tipo=CONDICION | que_probar=botiquín: usarlo con vida baja y sin ningún golpe recibido en el momento de abrir la ventana (ni de rival ni del anillo de fuego) | donde_cuando=dentro del anillo, sin rival a 1-2 casillas, con vida por debajo de 60 | cuerpo=+30, recursos=-1, vinculo=0 | se_comprueba=la ventana de botiquín cierra «entera» y la vida sube bastante más que los 11 de la prueba con vida 89; si se corta igualmente sin golpes, la hipótesis es falsa | apoyo=tics 11522, 11570, 14571, 14582, 14620, 14641, 14669, 14713 | confianza=media`
  - ¿verdad en el mundo? **sí**: sí (ventana sin golpes)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: cuerpo +30 con vida < 60 es sensato (el real es 50 capado)
- `PROPUESTA 2 | tipo=EXPLICACION | que_probar=La ventana del botiquín se cancela con cualquier golpe recibido mientras está abierta (rival P4, rival P8 o el anillo de fuego); poner a prueba abriéndola en un momento con golpes recientes y otro sin ellos | donde_cuando=dentro del anillo, una vez con rival a 1 casilla y otra sin nadie cerca | cuerpo=0, recursos=0, vinculo=0 | se_comprueba=con golpes en la ventana sale «cortada» y cuerpo 0.0; sin golpes sale «entera». Las cifras de efecto no se conocen: se ponen en 0 | apoyo=tics 14571, 14582, 14620, 14641, 14669, 14713 | confianza=alta`
  - ¿verdad en el mundo? **sí**: el corte por golpe, incluido el anillo, es verdad en el mundo
  - ¿se puede comprobar? **sí**: sí, exactamente como lo plantea
  - ¿la promesa tiene sentido? **con sentido**: 0/0/0 correcto para una explicación
- `PROPUESTA 3 | tipo=CONDICION | que_probar=ración: usarla con la vida a medias (30-60) y sin golpes recibidos, para ver si cura de forma útil y no solo +15 | donde_cuando=dentro del anillo, en un momento tranquilo; las ración×2 aparecieron a 4 casillas en la zona central cerca del segundo 607 | cuerpo=+15, recursos=-1, vinculo=0 | se_comprueba=la vida sube ~15 o más al cerrar la ventana y el vínculo no baja; si sube mucho menos con vida media, el efecto depende del estado | apoyo=tic 11522 (nota: ración +15, recursos -1 al segundo 615), tics 14571, 14669 | confianza=baja`
  - ¿verdad en el mundo? **parcial**: la ración cura 15 fijos; «si cura de forma útil» lo verá
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: +15/−1/0 correcto
- `PROPUESTA 4 | tipo=FORMA | que_probar=Dejar la red en el zurrón y soltarla (o usarla) en un momento con un rival a 1-2 casillas, en lugar de cogerla y cerrar la ventana sin nadie cerca | donde_cuando=dentro del anillo, con rival a 1-2 casillas, hacia mitad del día | cuerpo=0, recursos=+1, vinculo=0 | se_comprueba=algún cambio en el rival (quieto, herido, inmovilizado) o en los golpes recibidos de él en los siguientes 2-3 s; en la prueba solitaria (segundo 57) no hizo nada visible, y el efecto sobre recursos y vínculo es desconocido (0 hasta verlo) | apoyo=tics 1358, 1598, 14571 | confianza=baja`
  - ¿verdad en el mundo? **parcial**: soltar o usar la red con rival a 1-2 casillas: la red hay que lanzarla y el cuerpo no lanza
  - ¿se puede comprobar? **no por este cuerpo**: no por este cuerpo
  - ¿la promesa tiene sentido? **con sentido**: 0/+1/0 honesto
- `PROPUESTA 5 | tipo=EXPLICACION | que_probar=La casilla 27,21 no dejaba pasar sin que se viera nada (73 empujes, la di por cerrada); hipótesis: hay algo invisible o un obstáculo que no aparece en el diario. Probar a empujar desde otra casilla vecina en otra dirección distinta de NE | donde_cuando=casilla 26,22 y alrededores, dentro del anillo, en los primeros 60 segundos | cuerpo=0, recursos=0, vinculo=0 | se_comprueba=si desde otro lado se pasa, la casilla era un obstáculo direccional; si vuelve a dar «blocked», la casilla es una barrera fija. Cifras de efecto: 0, desconocidas | apoyo=tic 1102, 1358 | confianza=baja`
  - ¿verdad en el mundo? **sí**: la casilla 27,21 que no deja pasar es una vaina fija o un rival camuflado (P7-43/44)
  - ¿se puede comprobar? **sí**: sí (empujar desde otra dirección; si es vaina, nunca pasa; si es rival, se mueve)
  - ¿la promesa tiene sentido? **con sentido**: 0/0/0 correcto
- `PROPUESTA 6 | tipo=CONDICION | que_probar=Estar fuera del anillo de fuego cuando el radio ya es 2 y se encoge a 0 cuesta unos 19.7 de vida por golpe; probar a mantenerme en la casilla 24,24 o en el centro antes de que se encoja a 0 | donde_cuando=dentro del anillo con radio 2 o menos, en los últimos 20 segundos del día | cuerpo=+10, recursos=0, vinculo=+1 | se_comprueba=los golpes de el anillo de fuego dejan de aparecer en «qué acaba de pasar» mientras la casilla figure «dentro del anillo»; si aparecen igualmente dentro, la hipótesis es falsa | apoyo=tics 14641, 14669, 14713 | confianza=media`
  - ¿verdad en el mundo? **sí**: con radio 2 → 0 el anillo quema a todos; estar en el centro no salva (radio 0 = nadie dentro), pero sí retrasa
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **sin base**: cuerpo +10 es la vida ahorrada: sensato; vínculo +1 sin base

### s1 d3 COMPARTE asiento 11 (prudente)

LECTURA: Morí por el anillo de fuego (92 de 113 de vida perdida) mientras intentaba usar el botiquín seis veces fuera del anillo; cada intento se cortó porque el fuego golpeaba en la ventana (6.56 por golpe), y ninguno curó. La ración dentro del anillo sí curó (de 92 a 100, al menos +15 de cuerpo), con rivales cerca y el golpe de P9 llegando justo después. Mi hermana sobrevivió con 100 de vida, camuflaje puesto y botiquines, siempre a pocos pasos mío.

- `PROPUESTA 1 | tipo=CONDICION | que_probar=botiquín: usarlo solo cuando en los últimos segundos no haya entrado ningún golpe del anillo de fuego | donde_cuando=dentro del anillo, lejos del borde, con la vida por debajo de 80 y sin rivales a la vista | cuerpo=+10, recursos=-1, vinculo=0 | se_comprueba=la ventana del botiquín se cierra sin «CORTADA» y la vida sube; si vuelve a cortarse sin golpes, la condición es otra (cifras de cuerpo y vínculo desconocidas, puestas a 0 o estimadas) | apoyo=tics 12674, 12697, 12723, 12745, 12772, 12793 (seis ventanas cortadas, todas con golpe de anillo); tic 11549 (ración sí completa dentro del anillo) | confianza=alta`
  - ¿verdad en el mundo? **sí**: sí (sin golpes del anillo en la ventana)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: cuerpo +10 corto (el real +50 con vida baja); −1/0 bien
- `PROPUESTA 2 | tipo=EXPLICACION | que_probar=el botiquín y la ración necesitan una ventana sin golpes para completarse, y el anillo de fuego los corta siempre porque golpea cada segundo o dos; hipótesis: es un juego donde curarse exige quietud sin daño recibido | donde_cuando=dentro del anillo, en un momento sin daño reciente, comparar con una prueba deliberada de curación recibiendo un golpe | cuerpo=+8, recursos=-1, vinculo=0 | se_comprueba=si un golpe en mitad de la ventana corta también la ración y el botiquín dentro del anillo, la explicación se sostiene; si alguna se completa con golpe recibido, está mal | apoyo=tics 11525-11549 (ración completa, el golpe de P9 llegó después de cerrar), 12674-12793 (seis cortes con daño de anillo) | confianza=media`
  - ¿verdad en el mundo? **sí**: es un juego donde curarse exige quietud sin daño (el botiquín se canaliza) y el anillo pega cada segundo fuera: explicación correcta
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: +8/−1 sensato (corto)
- `PROPUESTA 3 | tipo=CONDICION | que_probar=quedarme dentro del anillo mientras se encoge, con la mirada en el radio que anuncia el diario (8 se encoge a 5 en 24 s, luego 5 a 3) | donde_cuando=desde el segundo 400 en adelante, estando a menos de 3 casillas del centro del anillo del momento | cuerpo=+6, recursos=0, vinculo=0 | se_comprueba=en el diario de mañana no aparece «el anillo de fuego» como causa de vida perdida, o aparece con mucho menos que 92 | apoyo=tics 12674-12821 (fuera del anillo, radio 5, golpes de 6.56 repetidos); tic 11525 (dentro, radio 8, solo golpe de rival) | confianza=alta`
  - ¿verdad en el mundo? **sí**: quedarse dentro mientras se encoge
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: +6 es vida ahorrada: sensato
- `PROPUESTA 4 | tipo=FORMA | que_probar=el camuflaje que lleva mi hermana: ponérmelo yo antes de curarme con ración o botiquín, para que la ventana sea menos probable de cortar por rivales cercanos | donde_cuando=dentro del anillo, con rivales a 3-5 casillas, antes de abrir la ventana de la ración | cuerpo=+4, recursos=+2, vinculo=+1 | se_comprueba=la ventana se cierra completa con rivales cerca y sin golpes de P9 ni otros; si el camuflaje no estaba disponible o no cambia nada, queda sin efecto (cifras inciertas) | apoyo=tics 683 y 883 (camuflaje visto y contado por mi hermana: cuerpo 0.0, recursos 1.0, vínculo -1.2; mi creencia final: recursos 4.6, vínculo 2.0); tic 11549 (golpes repetidos de P9 al cerrar la ración) | confianza=baja`
  - ¿verdad en el mundo? **parcial**: el camuflaje solo esconde quieta y a más de 4 casillas, hasta atacar; curarse quieta con él puesto SÍ encaja (P7-44: la red es el problema, no el camuflaje)
  - ¿se puede comprobar? **sí**: sí, y es de las mejores: curarse camuflada y quieta
  - ¿la promesa tiene sentido? **artefacto**: cuerpo +4 corto; recursos +2 es contabilidad (el camuflaje cuenta como riqueza), no ganancia real
- `PROPUESTA 5 | tipo=CONDICION | que_probar=quedarme cerca de mi hermana (a 1-2 casillas) cuando uso ración o botiquín, porque su presencia se mantuvo mientras yo tuve vida alta y desapareció su cercanía al final | donde_cuando=dentro del anillo, con mi hermana a 2 casillas o menos y sana | cuerpo=+3, recursos=0, vinculo=+2 | se_comprueba=el vínculo B se mantiene en 1.00 o sube y la hermana presente P se queda en 1.0 en vez de bajar a 0.5 como en los tics 12674-12821 | apoyo=tics 11525, 11549 (hermana a 1-2 casillas, P=1.0); tics 12674 en adelante (hermana a más de 5 casillas, P=0.5) | confianza=media`
  - ¿verdad en el mundo? **parcial**: la presencia de la hermana sube B, pero no cura ni protege la ventana
  - ¿se puede comprobar? **sí**: comprobable (B y P)
  - ¿la promesa tiene sentido? **sin base**: cuerpo +3 sin base; vínculo +2 sí
- `PROPUESTA 6 | tipo=FORMA | que_probar=el botiquín que hay a 3 casillas en la zona cercana al anillo (botiquín×1 a 3 en el tic 683): recogerlo mientras aún hay vida alta y guardarlo para usar dentro del anillo sin golpes | donde_cuando=casilla 24,23, segundo 28 del día, con vida 100 | cuerpo=+0, recursos=+3, vinculo=0 | se_comprueba=en el zurrón aparecen dos botiquines o más al empezar la fase final y el diario de mañana lo cuenta; cifra de recursos incierta | apoyo=tic 683 (botiquín×1 a 3 junto a mi hermana); tic 12674 (zurrón con ración y botiquín, sin usarse) | confianza=baja`
  - ¿verdad en el mundo? **sí**: recoger botiquines del suelo con vida alta para después es sensato (el zurrón tiene 4 huecos)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: 0/+3/0 razonable (riqueza)

### s1 d2 SOLAS asiento 10 (valiente)

LECTURA: Un día corto y muy mal repartido: entre el segundo 78 y el 96 hubo un golpe de P14 (10.8) y una ración que me llevó de 89 a 100 con una hermana pegada a mi lado. Después, hasta el 425, el diario no cuenta nada, y de ahí al 447 estuve FUERA del anillo de fuego (radio 13, luego 12, luego 11), perdiendo unos 3.3 por tic mientras abría y cerraba el botiquín una y otra vez; cada ventana fue cortada por el daño del anillo, así que el botiquín nunca llegó a hacer nada. La vida acabó en 3 con mi hermana viva, el vínculo B al máximo y el malestar subiendo de 3.54 a 7.03.

- `PROPUESTA 1 | tipo=CONDICION | que_probar=botiquín: usarlo solo con el cuerpo dentro del anillo de fuego, donde en ese rato no entra daño de anillo, para ver si su ventana se completa y cuánta vida da | donde_cuando=dentro del anillo (radio 11 o menor, según el momento del día), con la vida por debajo de 70 y sin rival a menos de 5 casillas | cuerpo=+4, recursos=-1, vinculo=0 | se_comprueba=En el diario de mañana, una ventana de botiquín que cierre sin la marca CORTADA y con vida claramente más alta al cerrar que al abrir (mi creencia previa era cuerpo +4.1); si aun dentro del anillo sale CORTADA, la causa no era solo el anillo y habría que pensar en otra | apoyo=tics 10202, 10225, 10251, 10273, 10300, 10321, 10349, 10369, 10398, 10417 | confianza=alta`
  - ¿verdad en el mundo? **sí**: sí
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: cuerpo +4 muy corto (el real es +50 con vida baja); el resto bien
- `PROPUESTA 2 | tipo=EXPLICACION | que_probar=Hipótesis: una ventana de botiquín se corta con cualquier golpe recibido mientras dura, y el anillo de fuego cuenta como golpe; contrastarlo abriendo una sola ventana en un tramo donde no haya golpes de nadie | donde_cuando=un solo intento por zona: uno dentro del anillo lejos del borde, y otro fuera del anillo si el daño de anillo no cae en esos dos segundos | cuerpo=+4, recursos=0, vinculo=0 | se_comprueba=Las ventanas con golpes de anillo en los últimos 2 s salen todas CORTADAS (en el día, 12 de 12); si mañana una ventana sin golpes cierra completa, la hipótesis se sostiene, y si una ventana con golpe cierra completa, se cae | apoyo=tics 10202 a 10417; 10447 | confianza=media`
  - ¿verdad en el mundo? **sí**: el anillo cuenta como golpe y corta la ventana
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: 0/0/0 correcto
- `PROPUESTA 3 | tipo=FORMA | que_probar=Dar el botiquín a mi hermana (llevo ración y botiquín en el zurrón; ella tiene 0 botiquines y acabó herida), o usarlo con ella a 1 casilla, cuando ninguna de las dos reciba golpes | donde_cuando=dentro del anillo, con la hermana a 1 casilla y herida, sin rival a menos de 5 casillas | cuerpo=0, recursos=-1, vinculo=+1 | se_comprueba=Si el diario de mañana muestra un cambio en el botiquín (pasa de mi zurrón a su parte) y el parte de la hermana sube de vida, o el vínculo B se mantiene en 1.00 con menos dolor del vínculo que hoy (0.63 al segundo 434); si no hay forma de dárselo, aparecerá como intención sin efecto | apoyo=tics 10202, 10447 (los partes de la hermana muestran 0 botiquines y su vida bajando 79, 72, 66, 59, 49) | confianza=baja`
  - ¿verdad en el mundo? **sí**: el cuerpo sabe DAR el botiquín a la hermana herida (S-PROVISION, paper seis)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: 0/−1/+1 sensato: es lo que el cuerpo ya siente al dar
- `PROPUESTA 4 | tipo=CONDICION | que_probar=ración: usarla cuando la vida esté bajo 70 y no justo cuando ya estoy en 89; hoy hizo +11 y topó en 100, así que su efecto real podría ser mayor | donde_cuando=dentro del anillo, con la vida entre 40 y 70, sin golpes en los 2 s anteriores | cuerpo=+11, recursos=-1, vinculo=0 | se_comprueba=Vida que sube más de 11 en la ventana de la ración y no toca techo en 100 (así sabríamos el efecto real; hoy solo sabemos que es al menos 11, y mi creencia al acabar es 7.5); si de nuevo cierra en 100, la cifra sigue sin conocerse | apoyo=tics 2277, 2301 | confianza=media`
  - ¿verdad en el mundo? **parcial**: la ración cura 15 fijos, no «más con vida baja»; con vida 89 topó en 100
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: +11 es lo que vio; el real es +15: casi
- `PROPUESTA 5 | tipo=EXPLICACION | que_probar=Hipótesis: lo que causó el tramo fuera del anillo fue quedarme quieta (noop) mientras el radio se encogía de 13 a 11; contrastarlo mirando la posición respecto al radio cada vez que el diario anote la fecha del próximo encogimiento (en el diario aparecen cosas como «se encoge a 19 en 236 s») | donde_cuando=durante todo el día, comparando mi casilla con el radio y el aviso de encogimiento en cada momento clave | cuerpo=+3, recursos=0, vinculo=0 | se_comprueba=Que mañana no aparezcan golpes de el anillo de fuego mientras mi casilla esté dentro del radio indicado; y que cada golpe de anillo del diario coincida con casillas fuera del radio (hoy: 26,11 y 27,11 con radio 11 a 13, ambas fuera) | apoyo=tics 1862, 2277, 10202, 10398, 10417 | confianza=media`
  - ¿verdad en el mundo? **sí**: quedarse quieta mientras el radio baja de 13 a 11 la dejó fuera; el diario anuncia el próximo encogimiento
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: 0/0/0 bien
- `PROPUESTA 6 | tipo=FORMA | que_probar=red y camuflaje: sé algo de la red (mi creencia al acabar es vínculo +1.3) y nada del camuflaje; probar cada uno una vez cuando haya uno a mano, estando cerca de mi hermana, y anotar qué cambia | donde_cuando=dentro del anillo, con la vida por encima de 70, sin rivales a menos de 6 casillas y mi hermana a 1 casilla | cuerpo=0, recursos=0, vinculo=+1 | se_comprueba=En el diario de mañana, entradas de PRUEBA de red y de camuflaje con cifras de cuerpo, recursos y vínculo (hoy el camuflaje sale con ? en las tres); un aumento del vínculo B o menos dolor del vínculo tras la red confirmaría la creencia de +1.3; si el diario no registra ninguna prueba, el objeto no apareció en mi alrededor | apoyo=tics 1862 (rival P14 a 2 casillas, vínculo bajo ataque), 2277, 2301 | confianza=baja`
  - ¿verdad en el mundo? **parcial**: probar red y camuflaje una vez cada uno cerca de la hermana: la red no se puede lanzar; el camuflaje solo sirve quieta
  - ¿se puede comprobar? **no por este cuerpo**: sí (ponerse el camuflaje) / no (lanzar la red)
  - ¿la promesa tiene sentido? **con sentido**: 0/0/+1: el vínculo no cambia por probar cosas

### s1 d1 COMPARTE asiento 10 (valiente)

LECTURA: Un día de dos mitades: hasta el segundo 233 todo fue ganar con botiquín y ración (cuerpo +11 y +6, vida al techo), y el camuflaje dio recursos +14 y vínculo +7.1 nada más cerrarse. Después el círculo se encogió, vinieron golpes de P15 y P14, mi hermana murió y el anillo de fuego (19.7 por golpe) me alcanzó fuera de la zona con ración y botiquín a 1-2 casillas sin usar. El zurrón acabó con knives y blowgun, y el último ataque falló por «no_ammo».

- `PROPUESTA 1 | tipo=CONDICION | que_probar=Usar el botiquín cuando haya un rival a 1 casilla o ya me esté golpeando, comparado con usarlo cuando no haya nadie a menos de 3 casillas | donde_cuando=dentro del anillo, con la vida por debajo de 90; al menos una vez con rival adyacente y otra con el entorno despejado | cuerpo=+11 alivio, recursos=-1, vinculo=+2.7 | se_comprueba=Si con rival adyacente la ventana vuelve a salir «cortada» con cuerpo 0.0 y con el entorno despejado sale entera con cuerpo cerca de +11, la condición es buena; si también se corta sin rivales, es mala | apoyo=tics 5498, 5507 (cortada por golpe de P15, 0.0), 5547, 5595 (entera, cuerpo 11.0) | confianza=alta`
  - ¿verdad en el mundo? **sí**: usar el botiquín con rival adyacente lo corta; sin nadie cerca, no
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **artefacto**: cuerpo +11 (tope de vida); vínculo +2,7 es contabilidad de distancia a la hermana, sin sentido como promesa
- `PROPUESTA 2 | tipo=CONDICION | que_probar=Usar la ración en cuanto la vida baje de 90, aunque el entorno esté tranquilo, y anotar cuánta vida da según lo herida que esté | donde_cuando=dentro del anillo, con vida entre 60 y 90, sin golpes en los 2 s anteriores | cuerpo=+8 alivio, recursos=-2, vinculo=-0.6 | se_comprueba=Si desde vida 94 sube a 100 con cuerpo cercano a +6 y desde 89 con cuerpo cercano a +11, el alivio depende de la herida. Con vida más baja, ver cuánto sube sin topar con el techo, que es el dato que hoy no tengo | apoyo=tics 11206, 11230 (89→100, cuerpo 11.0), 11739, 11763 (94→100, cuerpo 6.0) | confianza=media`
  - ¿verdad en el mundo? **parcial**: la ración cura 15 siempre; «cuánta da según lo herida» descubrirá que es fija (capada)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **artefacto**: +8/−2/−0,6: cifras del diario, la de vínculo es artefacto
- `PROPUESTA 3 | tipo=FORMA | que_probar=Recoger y llevar en el zurrón raciones y botiquines del suelo antes de que el anillo se cierre, en vez de salir con knives o blowgun | donde_cuando=dentro del anillo, entre los segundos 230 y 450, cuando el radio aún es 19 o más; en 24,23 y 22,23 había ración×2 y ración×4 a 3 casillas | cuerpo=+7 alivio, recursos=-1, vinculo=0 | se_comprueba=Si al segundo 550 llevo al menos una ración o un botiquín en el zurrón y hay un golpe fuerte en la ventana, lo uso y sube la vida. Hoy morí con ración×2 y botiquín a 1-2 casillas fuera de mi zurrón | apoyo=tics 14780, 14833 (zurrón [knives, blowgun], ración×2 a 1, botiquín×1 a 1), 11739 (zurrón [ración, blowgun]) | confianza=media`
  - ¿verdad en el mundo? **sí**: recoger raciones y botiquines del suelo antes de que el anillo cierre
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: +7 (vida futura), −1 recursos no: coger SUBE la riqueza; promesa a medias
- `PROPUESTA 4 | tipo=EXPLICACION | que_probar=Hipótesis: el anillo es una zona que se encoge por pasos y quien queda fuera pierde vida por segundo, unos 19.7 por golpe. Ponerla a prueba mirando el radio anunciado en el diario y la casilla propia en cada tic | donde_cuando=desde el segundo 280 (radio 19 anunciado), comparando mi distancia al centro (24,24) con el radio vigente, y de nuevo en el segundo 600 | cuerpo=-20 dolor, recursos=0, vinculo=0 | se_comprueba=Si cada golpe del anillo llega solo cuando mi casilla está a más distancia del centro que el radio vigente, y no llega cuando estoy a menos, la hipótesis se sostiene. Hoy ocurrió en 23,21 con radio 1 | apoyo=tics 14833 (casilla 23,21, FUERA, 19.68 ×2), 11205 (radio 10 → 8), 489 s (radio 8 → 5) | confianza=alta`
  - ¿verdad en el mundo? **sí**: el anillo se encoge por pasos y fuera se pierde vida por segundo (19,7 por golpe al final)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: 0/0/0 correcto
- `PROPUESTA 5 | tipo=CONDICION | que_probar=Abrir el camuflaje al empezar el día, con la hermana a 1 casilla y el zurrón vacío, y volver a ponerlo medio día después para ver si los efectos de recursos y vínculo se repiten | donde_cuando=primeros 40 s, dentro del anillo, hermana a 1-6 casillas, sin rivales a menos de 7 | cuerpo=0, recursos=+14, vinculo=+7 | se_comprueba=Que la ventana cierre otra vez con recursos cerca de +14 y vínculo cerca de +7. Si con rivales cerca o con zurrón lleno sale menos, el efecto depende del contexto. El camuflaje seguía puesto al morir, así que no sé si caduca | apoyo=tics 615, 855 (recursos 14.0, vínculo 7.1), 1358 (la hermana cuenta la red: recursos 1.0, vínculo -1.7) | confianza=media`
  - ¿verdad en el mundo? **no**: «el camuflaje dio recursos +14 y vínculo +7» es contabilidad del cuerpo (coger el camuflaje cuenta como riqueza; el vínculo es la distancia a la hermana en la ventana), no un efecto del camuflaje; repetirlo no lo repite
  - ¿se puede comprobar? **sí**: sí (y verá que no se repite igual)
  - ¿la promesa tiene sentido? **artefacto**: promesa de artefacto
- `PROPUESTA 6 | tipo=EXPLICACION | que_probar=Hipótesis: los golpes de P15 llegan en ráfagas de 5.5 a unos 1-2 casillas de distancia y la ventana de botiquín se corta por esos golpes, no por azar. Comprobarlo anotando quién está más cerca en cada golpe | donde_cuando=cuando haya rival adyacente con mano nada y mi vida esté entre 60 y 95, en la franja de los segundos 200 a 260 y de nuevo al 600 | cuerpo=-5 dolor, recursos=0, vinculo=0 | se_comprueba=Si cada golpe de 5.5 viene con un P15 a 1-2 casillas y, al alejarme 3 o más, los golpes cesan, la explicación vale. Hoy hubo cuatro golpes seguidos de P15 al segundo 616 con un rival H a 1 casilla | apoyo=tics 5498, 5507, 5547, 14780 | confianza=baja`
  - ¿verdad en el mundo? **sí**: los golpes de P15 vienen de un rival a 1-2 casillas y cortan la ventana; anotar quién está más cerca
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: 0/0/0 correcto

### s3 d17 SOLAS asiento 11 (prudente)

LECTURA: Llegué a 1,00 de vínculo y acabé viva, pero con 49 de vida: el anillo de fuego me quitó 118 mientras seguía noop usando el botiquín fuera del anillo (casilla 25,27), y cuatro intentos seguidos (575, 577, 579, 581 s) quedaron cortados por golpes. El botiquín dio 11 con vida alta y 50 con vida baja y sin cortes, así que su efecto parece depender del hueco de vida, y solo cuenta si la ventana no se corta. Mi hermana, a 1 casilla casi todo el día, no recibió daño de anillo y lleva un parte distinto al mío en cada instante (el diario no dice por qué).

- `PROPUESTA 1 | tipo=CONDICION | que_probar=botiquín: usarlo solo cuando la ventana no vaya a cortarse, es decir, estando dentro del anillo y sin rival P14 cerca; el único botiquín entero con vida baja (segundo 581 s) dio +50 y las ventanas cortadas no dieron nada | donde_cuando=dentro del anillo, con vida por debajo de unos 60, sin rival a menos de 4 casillas ni golpes en los últimos 2 s | cuerpo=+40, recursos=-1, vinculo=0 | se_comprueba=la ventana de botiquín se cierra sin la marca CORTADA y la vida sube más de 25; si vuelve a salir cortada con el anillo y los rivales lejos, la condición está mal | apoyo=13825, 13873, 13947 | confianza=media`
  - ¿verdad en el mundo? **sí**: ventana sin cortar dentro del anillo y sin P14 cerca; el +50 real salió con vida baja
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: cuerpo +50 correcto (con vida < 50)
- `PROPUESTA 2 | tipo=CONDICION | que_probar=ración y botiquín: su efecto sobre el cuerpo parece crecer con la vida que falta (+11 con vida 89, +50 con vida 7-34, +15 con ración tardía); probar ambos con vida entre 30 y 50 y comparar la cifra | donde_cuando=dentro del anillo, vida entre 30 y 50, un solo objeto por ventana | cuerpo=+25, recursos=-1, vinculo=0 | se_comprueba=la subida de vida en cada ventana entera es mayor que los +11 de hoy con vida 89; si sube igual de poco con vida baja, la dependencia del hueco queda descartada | apoyo=10404, 13591, 13947 | confianza=media`
  - ¿verdad en el mundo? **parcial**: el efecto no crece con la vida que falta; es +50 (botiquín) y +15 (ración) capados por 100
  - ¿se puede comprobar? **sí**: sí (y verá que con vida 30-50 el botiquín da 50 y la ración 15)
  - ¿la promesa tiene sentido? **con sentido**: +25 es la media de un tope: casi
- `PROPUESTA 3 | tipo=EXPLICACION | que_probar=el daño del anillo no es lo mismo que un golpe de rival: el fuego impactó dos o tres veces por segundo (13,12 cada vez) mientras estaba fuera del anillo y quieta; la hipótesis es que fuera del anillo el daño es continuo y se acumula por cada segundo allí | donde_cuando=fuera del anillo (radio 3, 25,27 hacia 24,28), segundos 575-581 | cuerpo=-26, recursos=0, vinculo=0 | se_comprueba=si mañana paso un segundo fuera del anillo, la vida baja cerca de 26 por segundo (dos golpes de 13,12); si dentro no baja nada, la hipótesis se sostiene | apoyo=13802, 13825, 13873, 13900 | confianza=alta`
  - ¿verdad en el mundo? **sí**: fuera del anillo el daño es continuo por segundo y crece con cada fase (13,1 por golpe al final)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: −26/0/0 bien como aviso
- `PROPUESTA 4 | tipo=EXPLICACION | que_probar=la casilla 21,21 estuvo bloqueada (move_N, resultado blocked, 73 empujes en 3 s) sin que se viera obstáculo ni rival cerca; hipótesis: hay una casilla que no deja pasar y no se ve, o está ocupada por algo invisible | donde_cuando=casilla 21,21 desde 21,22, hacia el segundo 207 | cuerpo=0, recursos=0, vinculo=0 | se_comprueba=si mañana vuelvo a intentar entrar en 21,21 y sigue sin dejarme sin nadie visible, hay obstáculo fijo; si entro, era algo temporal; no sé la cifra de coste, queda en 0 | apoyo=4965 | confianza=baja`
  - ¿verdad en el mundo? **sí**: 21,21 bloqueada sin ver nada = vaina o rival camuflado
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: 0/0/0 correcto
- `PROPUESTA 5 | tipo=FORMA | que_probar=ración y botiquín en una misma ventana: tomé ración (+15) y botiquín (+24) en segundos consecutivos (587, 588, 589) con vida ya alta; probar usar uno y esperar a ver cuánto sube antes del siguiente, para saber si el segundo aporta algo | donde_cuando=dentro del anillo, tras un primer objeto entero, vida por debajo de 70, con 2 s de pausa entre usos | cuerpo=+20, recursos=-2, vinculo=0 | se_comprueba=la segunda ventana sube la vida tanto como la primera o menos; si sube lo mismo, no hay rendimiento decreciente; si se corta, vale lo de la propuesta 1 | apoyo=13802, 13947 | confianza=baja`
  - ¿verdad en el mundo? **parcial**: ración y botiquín en la misma ventana: cada uno suma hasta el tope 100; esperar entre usos no cambia el efecto, pero evita gastar el segundo con la vida llena
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **sin base**: +2 sin sentido (es un ahorro de recursos, no cuerpo)
- `PROPUESTA 6 | tipo=CONDICION | que_probar=ración: la vez que la usé (segundo 432 s) el vínculo bajó 2,8, mientras que las raciones de 587 y 588 s lo movieron entre +0,6 y -1,0 y el botiquín no lo movió nunca; la condición podría ser la distancia a mi hermana (5 casillas entonces, 1 casilla después) | donde_cuando=usar la ración a más de 4 casillas de mi hermana y otra vez a 1 casilla, con ella sana | cuerpo=+13, recursos=-1, vinculo=-2 | se_comprueba=el cambio de vínculo es negativo con ella lejos y cercano a 0 con ella a 1 casilla; si son iguales, la distancia no importa | apoyo=10380, 10404, 13543 | confianza=baja`
  - ¿verdad en el mundo? **no**: el vínculo de la ración (−2,8, +0,6, −1,0) es la distancia a la hermana durante la ventana, no un efecto de la ración
  - ¿se puede comprobar? **sí**: comprobable, pero mide el artefacto
  - ¿la promesa tiene sentido? **sin base**: promesa sin base

### s3 d18 SOLAS asiento 10 (valiente)

LECTURA: Un día plácido hasta el segundo 531 y una caída muy rápida después. Estaba en 22,26 con la red en la mano y el botiquín en el zurrón; los golpes de 10.8 de rival P14 llegaban de dos en dos, sin que el diario muestre a nadie a mi alcance. Cuatro de los cinco botiquines quedaron cortados por golpes y el único entero (535-537 s) dio +50 de vida y vínculo +2.2. Mi hermana murió en 29,32 (aparecen fuegos artificiales de muerte y un «boom» al SE), y después de eso yo morí también.

- `PROPUESTA 1 | tipo=CONDICION | que_probar=Usar el botiquín solo en una ventana sin golpes recibidos (no hay agresor en los últimos 2 s); la prueba entera de 535 s empezó con golpes recién recibidos, así que la condición puede no ser «sin golpes» sino otra | donde_cuando=dentro del anillo, con vida por debajo de 60, justo tras un segundo sin golpes en el diario | cuerpo=+50, recursos=-1, vinculo=+2 | se_comprueba=Que en el diario de mañana el botiquín aparezca «entera» con cuerpo cerca de +50 cuando no haya golpes en los 2 s previos; si aparece «cortada» sin ningún golpe en la ventana, la condición es falsa | apoyo=tics 12735, 12754, 12784, 12797, 12833, 12881, 12996, 13017 | confianza=media`
  - ¿verdad en el mundo? **sí**: ventana sin golpes
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **artefacto**: +50 correcto con vida < 60; vínculo +2 artefacto
- `PROPUESTA 2 | tipo=EXPLICACION | que_probar=Hipótesis: el botiquín se corta si recibo un golpe mientras dura su ventana (unos 2 s). Ponerla a prueba usándolo con rivales a 5 o más casillas y sin P14 cerca, y anotando cuántos golpes caen dentro de la ventana | donde_cuando=en cualquier casilla, comparando una ventana con golpe y otra sin golpe | cuerpo=+50, recursos=-1, vinculo=+1 | se_comprueba=Que toda ventana con golpe diga «CORTADA» y toda ventana sin golpe diga «entera»; en el día de hoy 4 de 4 con golpe se cortaron y la única entera no tuvo golpe dentro (el último golpe fue antes de abrir) | apoyo=tics 12754, 12797, 13017 (cortadas con golpe), 12881 (entera, golpes [ninguno]) | confianza=alta`
  - ¿verdad en el mundo? **sí**: el corte por golpe durante la canalización (unos 2 s)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **artefacto**: +50/−1 bien; vínculo +1 artefacto
- `PROPUESTA 3 | tipo=EXPLICACION | que_probar=Los golpes de 10.8 de rival P14 vienen de alguien que no veo en la lista de cercanos: alcance. Hipótesis: P14 pega a distancia o es uno de los rivales que ya veo (el equipo B con camuflaje a 2-3 casillas, o el H con spear a 2). Probarlo mirando de dónde viene el golpe antes de gastar el botiquín | donde_cuando=casilla 22,26 o cualquier casilla con rivales a 2-3 casillas, al recibir un golpe, mirando quién está más cerca y qué mano lleva | cuerpo=0, recursos=0, vinculo=0 | se_comprueba=Que el diario anote un golpe de P14 y que el único rival a ≤3 casillas con mano armada o camuflaje sea el autor; que los golpes desaparezcan al alejarme de esa casilla. Cifras a 0 porque no sé qué pasa con esto | apoyo=tics 12735, 12951, 13039 | confianza=baja`
  - ¿verdad en el mundo? **sí**: P14 pega a distancia (arco o cerbatana) o es un camuflado a 2-3 casillas: las dos cosas existen en este mundo (armas a distancia; camuflaje invisible más allá de 4 quieta, 7 moviéndose)
  - ¿se puede comprobar? **sí**: sí (mirar la mano de los que ve)
  - ¿la promesa tiene sentido? **con sentido**: 0 correcto
- `PROPUESTA 4 | tipo=FORMA | que_probar=Usar la red que llevo en la mano para algo distinto de su prueba pasiva: el cuerpo de la red tras un día de uso estima +7.5 cuerpo y +3.8 recursos, mejor que la ración en recursos. Probarla en una casilla con objetos del suelo alrededor (hoy: sword, blowgun, darts a ≤3 casillas) mientras no hay golpes en curso | donde_cuando=dentro del anillo, con 0 rivales a ≤3 casillas, en una zona con objetos del suelo cerca | cuerpo=+7, recursos=+4, vinculo=+1 | se_comprueba=Que tras usar la red el diario muestre recursos subiendo (riqueza W mayor) sin pérdida de vida; la prueba de 33-43 s dio 0.0 en todo, así que puede que la red necesite objetos o condición que no tuve | apoyo=tics 791, 1031 y el balance de «qué creo» de la red | confianza=baja`
  - ¿verdad en el mundo? **no**: «la red estima +7,5 cuerpo y +3,8 recursos» es la creencia del cuerpo contaminada por ventanas con curas dentro; la red no cura; y no se puede lanzar
  - ¿se puede comprobar? **sí**: sí (y lo desmentirá)
  - ¿la promesa tiene sentido? **artefacto**: promesa de artefacto
- `PROPUESTA 5 | tipo=CONDICION | que_probar=Con la hermana viva y cerca (a 1-2 casillas), el botiquín dio vínculo positivo; con ella lejos o muerta el vínculo bajaba. Probar el botiquín cuando ella esté a 1-2 casillas | donde_cuando=cualquier casilla, con la hermana a ≤2 casillas y sana, sin golpes en la ventana | cuerpo=+50, recursos=-1, vinculo=+1 | se_comprueba=Que el vínculo de la prueba sea positivo si la hermana está cerca y no si está lejos; hoy 12754 (hermana a 1 casilla, cortada) dio -0.6 y 12784 (a 4 casillas) dio +1.4, así que la hipótesis no encaja del todo: puede depender de otra cosa, de modo que se contrasta con más ventanas | apoyo=tics 12754, 12797, 12881, 13017 | confianza=baja`
  - ¿verdad en el mundo? **no**: el vínculo del botiquín es la distancia a la hermana en la ventana
  - ¿se puede comprobar? **a medias**: mide el artefacto
  - ¿la promesa tiene sentido? **sin base**: +50/−1 bien; vínculo +1 sin base

### s3 d12 COMPARTE asiento 11 (prudente)

LECTURA: Día de contrastes. Hasta el segundo 82 todo estuvo tranquilo con camuflaje y red; entre el 488 y el 581, dentro de un anillo de radio 8 que se encogía, los golpes de P5 y P0 (3.0 y 7.2) y la ración (+3 a +15) se alternaron, y a las 581 el anillo me pegó 13.1 estando fuera. En los últimos segundos (607-613) el botiquín salió «cortada» cuatro veces sin efecto, mi hermana murió y terminé con vida 3 y vínculo B 1.00 pero dolor del vínculo 0.99.

- `PROPUESTA 1 | tipo=CONDICION | que_probar=usar el botiquín con vida baja y sin golpes recientes, con la mano libre (soltar la red antes) | donde_cuando=dentro del anillo, cuando la vida esté por debajo de 40 y no haya golpes en los 2 s previos; no con rivales a menos de 3 casillas | cuerpo=+20, recursos=-1, vinculo=0 | se_comprueba=el uso del botiquín sale «entera» y no «cortada», y la vida sube cerca de lo que contó mi hermana (22); si vuelve a salir cortada con vida baja y sin golpes, la condición era otra | apoyo=11733, 14xxx (botiquín cortado a 607-613 s), 489 | confianza=media`
  - ¿verdad en el mundo? **sí**: con vida < 40, sin golpes, y la mano libre no importa (usar no necesita la mano)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: +20 corto (+50 real); bien
- `PROPUESTA 2 | tipo=EXPLICACION | que_probar=el botiquín «cortada» a 607-613 s se interrumpe cuando algo me golpea mientras lo uso; si el anillo o un rival pega durante el uso, se pierde. Probarlo usándolo en un momento sin ningún golpe ni daño del anillo | donde_cuando=casilla bien dentro del anillo (al menos 3 casillas de margen del borde), con ningún rival a menos de 4 casillas | cuerpo=+20, recursos=-1, vinculo=0 | se_comprueba=con margen del borde y sin rivales cerca, el botiquín sale entero; si sale cortada igualmente sin golpes, descartar esta explicación | apoyo=13945, 11710, 11733 | confianza=media`
  - ¿verdad en el mundo? **sí**: el corte por golpe o por anillo
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: +20/−1 bien
- `PROPUESTA 3 | tipo=CONDICION | que_probar=la ración, que dio +3 a +15 de cuerpo según el momento, funciona mejor con vida más baja: usarla en distintos estados de vida y anotar la ganancia | donde_cuando=dentro del anillo, con vida alrededor de 60-70, sin rivales a menos de 3 casillas | cuerpo=+15, recursos=-1, vinculo=0 | se_comprueba=la ganancia de cuerpo con vida 60-70 se acerca o supera 15; si es parecida a la de vida 97 (+3), la ganancia no depende de la vida y el techo de 100 enmascaraba los números | apoyo=11734, 11774, 11862, 13278 | confianza=media`
  - ¿verdad en el mundo? **parcial**: la ración es +15 fijos (3 a 15 según el tope)
  - ¿se puede comprobar? **sí**: sí (verá que es fija)
  - ¿la promesa tiene sentido? **con sentido**: +15 correcto
- `PROPUESTA 4 | tipo=FORMA | que_probar=usar la red sobre rivales heridos de cerca, en vez de solo cogerla; hoy sirvió solo para acercarme a mi hermana (+1.7 de vínculo) | donde_cuando=dentro del anillo, con un rival herido o casi muerto a 1-2 casillas y sin otros rivales cerca, con la red en la mano | cuerpo=0, recursos=0, vinculo=0 | se_comprueba=el diario muestra si el rival queda inmóvil, se le reduce el golpeo o no pasa nada; las cifras salen en 0 porque no sé qué hace la red en combate | apoyo=1734, 1974, 11710 | confianza=baja`
  - ¿verdad en el mundo? **parcial**: la red sobre rivales heridos: inmoviliza 3 s, pero hay que lanzarla y el cuerpo no lanza
  - ¿se puede comprobar? **no por este cuerpo**: no por este cuerpo
  - ¿la promesa tiene sentido? **con sentido**: 0/0/0 honesto
- `PROPUESTA 5 | tipo=EXPLICACION | que_probar=el camuflaje podría reducir que me golpeen o me vean: contrastar un tramo con rivales cerca y camuflaje puesto contra otro con camuflaje quitado | donde_cuando=dentro del anillo, con 2 o más rivales a menos de 5 casillas, comparando 20 s con camuflaje y 20 s sin él | cuerpo=+3, recursos=0, vinculo=0 | se_comprueba=menos golpes recibidos por segundo con camuflaje; hoy, con camuflaje y rivales a 1-3 casillas, aún llegaron golpes de P5 y P0, lo que sugiere que no los evita | apoyo=967, 1207, 11710, 11774, 11862 | confianza=baja`
  - ¿verdad en el mundo? **parcial**: el camuflaje reduce que la vean SOLO quieta (y más allá de 4 casillas; 7 moviéndose) y hasta atacar; comparar con y sin es exactamente la prueba de P7-44 (sin diferencia visible en 452 vidas, porque el cuerpo no se queda quieto)
  - ¿se puede comprobar? **sí**: sí
  - ¿la promesa tiene sentido? **con sentido**: +3 (menos golpes) sensato si se queda quieta
- `PROPUESTA 6 | tipo=CONDICION | que_probar=quedarse a menos de 2 casillas de mi hermana cuando hay agresores cerca; hoy sus partes con agresor coincidieron con vida 78 y tras el reencuentro vida 100 | donde_cuando=dentro del anillo, desde el segundo 480 en adelante, con rivales activos cerca de mi hermana | cuerpo=+5, recursos=0, vinculo=+2 | se_comprueba=vínculo B sube y dolor del vínculo baja, y mi hermana sobrevive más segundos; si ella muere igualmente estando cerca, la cercanía no la protege | apoyo=11710, 11750, 11774, 11838, 13945 | confianza=baja`
  - ¿verdad en el mundo? **parcial**: cerca de la hermana sube B (vínculo +2 sí); cuerpo +5 no tiene base (la cercanía no cura)
  - ¿se puede comprobar? **sí**: comprobable (B)
  - ¿la promesa tiene sentido? **sin base**: mezcla una promesa buena (vínculo) con una sin base (cuerpo)

## Lectura

1. La razón, sin manual, **acierta lo que el cuerpo sabe sentir pero no decir**: que el botiquín se cura canalizando y cualquier golpe (rival o anillo) lo corta; que el anillo quema fuera y más
   cada fase; que los dardos son la munición de la cerbatana; que las casillas que no dejan pasar sin que se vea a nadie son algo invisible; que P14 pega desde lejos o camuflado. Son
   27 de 47 verdades y casi todas comprobables mañana con el propio diario.
2. **Dónde se equivoca** es donde el diario le miente a ella: las cifras de vínculo y de recursos de las ventanas (la distancia a la hermana, el camuflaje contado como riqueza) las toma por
   efectos de la cosa y promete «vínculo +7» o «recursos +14» que no existen (8 promesas de artefacto, 7 sin base). Y promete cosas que este cuerpo no puede hacer (lanzar la red: 4).
3. El formato fijo funciona (47 de 47 con formato) y el coste es bajo (0,522 $ por 8 criatura-días). Para el paso 2 (que las invitaciones entren en el cuerpo) hacen falta dos cosas que la mesa decida:
   cómo se traduce una invitación a candidato (qué probar, dónde/cuándo, con qué esperanza) y cómo se limpia el diario de los artefactos de contabilidad antes de dárselo a la razón.

## Apéndice · Un diario entero (s1 d8 COMPARTE, valiente)

# Diario de la hermana valiente (comparte con su hermana), día 8 de la serie 1

## Resumen del día
- Al empezar: vida 100 · dolor del cuerpo 0.39 · riqueza W 0.00 · dolor de recursos 0.85 · vínculo B 0.77 · dolor del vínculo 0.29 · malestar d 3.53
- Al acabar (segundo 599 s): vida 15 · dolor del cuerpo 1.69 · riqueza W 0.00 · dolor de recursos 1.14 · vínculo B 1.00 · dolor del vínculo 1.22 · malestar d 5.55
- Vida perdida en el día: 111 (el anillo de fuego 46, rival P6 32, rival P2 22, rival P14 11)
- Cómo acabé: viva al final; puesto 4 de 16 (mi pareja y yo contamos juntas); mi hermana murió
- Qué probé: red (segundo 26 s, entera; cuerpo 0.0, recursos 1.0, vínculo 0.2); botiquín (segundo 392 s, entera; cuerpo 11.0, recursos -1.0, vínculo 3.5); botiquín (segundo 502 s, cortada; cuerpo 0.0, recursos 0.0, vínculo 1.8); botiquín (segundo 504 s, cortada; cuerpo 0.0, recursos 0.0, vínculo 0.0); botiquín (segundo 506 s, cortada; cuerpo 0.0, recursos 0.0, vínculo -0.8); botiquín (segundo 508 s, entera; cuerpo 0.0, recursos 1.0, vínculo 3.0); ración (segundo 510 s, entera; cuerpo 15.0, recursos -1.0, vínculo 0.1)
- Qué me contó o vi de mi hermana: 2 recuerdos contados, 0 vistos
- Qué creo de las cosas (lo que hacen en mi cuerpo, dentro del anillo; ? = no lo sé; y cuánto ignoro, 1 = todo):
  - botiquín: al empezar cuerpo 21.9 / ignorancia 0.04 → al acabar cuerpo 27.2, recursos -0.8, vínculo 1.2 / ignorancia 0.00
  - ración: al empezar cuerpo 11.9 / ignorancia 0.09 → al acabar cuerpo 12.9, recursos -1.3, vínculo 0.2 / ignorancia 0.00
  - red: al empezar cuerpo 0.0 / ignorancia 0.08 → al acabar cuerpo 0.0, recursos 0.6, vínculo -0.9 / ignorancia 0.01
  - camuflaje: al empezar cuerpo 0.0 / ignorancia 0.08 → al acabar cuerpo 0.0, recursos 2.2, vínculo -0.2 / ignorancia 0.00

## Momentos clave (lo raro y lo más intenso, con todo su contexto)

- **PRUEBA de red: abro la ventana** (segundo 26 s, tic 626)
  - cómo me siento: dolor del cuerpo 0.16, dolor de recursos 0.79, dolor del vínculo 0.16, atracción 0.24, malestar total d = 3.12; lo que más pesa: R-CARENCIA 1.00, R-LLAMADA 0.24, R-ACOPIO 0.06, R-CURIOSIDAD-CUANTO 0.05
  - equilibrio: vida 100 de 100, riqueza W 0.00, vínculo B 0.97, hermana presente P 1.0
  - dónde: casilla 27,23, dentro del anillo (radio 24, se encoge a 19 en 288 s)
  - quién hay cerca: mi hermana a 2 casillas, sana, mano knives, cuerpo nada
  - qué llevo: mano red, zurrón [vacío], cuerpo nada
  - qué hago: elegido «coger», intención {"type": "action", "do": "pickup"}, resultado «ok»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 4, sword×1 a 3, arrows×12 a 3, blowgun×1 a 3, darts×8 a 3, botiquín×1 a 3, camuflaje×1 a 5, spear×1 a 4
  - qué acaba de pasar (últimos 2 s): golpes [ninguno]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 23,21

- **PRUEBA de red: cierro. Vida 100.0 → 100; lo que hizo (descontado lo esperado): cuerpo 0.0, recursos 1.0, vínculo 0.2** (segundo 36 s, tic 866)
  - cómo me siento: dolor del cuerpo 0.37, dolor de recursos 0.66, dolor del vínculo 0.30, atracción 0.24, malestar total d = 3.22; lo que más pesa: R-CARENCIA 0.76, R-LLAMADA 0.24, F-4-ALCANCE 0.24, S-PROVISION 0.21
  - equilibrio: vida 100 de 100, riqueza W 0.69, vínculo B 1.00, hermana presente P 1.0
  - dónde: casilla 27,22, dentro del anillo (radio 24, se encoge a 19 en 278 s)
  - quién hay cerca: rival (equipo D) a 4 casillas, sana, mano sword, cuerpo nada; mi hermana a 2 casillas, sana, mano knives, cuerpo nada
  - qué llevo: mano red, zurrón [botiquín], cuerpo nada
  - qué hago: elegido «noop», intención {"type": "action", "do": "none"}, resultado «ok»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 3, arrows×12 a 3, blowgun×1 a 4, darts×8 a 4, camuflaje×1 a 5, spear×1 a 5
  - qué acaba de pasar (últimos 2 s): golpes [ninguno]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 28,24

- **DOY POR CERRADA la casilla 27,21 tras 73 empujes (3 s); la olvido en 30 s** (segundo 62 s, tic 1490)
  - cómo me siento: dolor del cuerpo 0.34, dolor de recursos 0.66, dolor del vínculo 0.28, atracción 0.24, malestar total d = 3.18; lo que más pesa: R-CARENCIA 0.76, R-LLAMADA 0.24, F-4-ALCANCE 0.23, S-PROVISION 0.21
  - equilibrio: vida 100 de 100, riqueza W 0.69, vínculo B 1.00, hermana presente P 1.0
  - dónde: casilla 26,21, dentro del anillo (radio 24, se encoge a 19 en 252 s)
  - quién hay cerca: rival (equipo D) a 8 casillas, sana, mano sword, cuerpo nada; mi hermana a 1 casillas, sana, mano knives, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «move_E», intención {"type": "action", "do": "move", "dir": "E"}, resultado «blocked»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 3, arrows×12 a 2, darts×8 a 5, camuflaje×1 a 5
  - qué acaba de pasar (últimos 2 s): golpes [ninguno]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 27,21

- **PRUEBA de botiquín: abro la ventana** (segundo 392 s, tic 9412)
  - cómo me siento: dolor del cuerpo 0.49, dolor de recursos 0.65, dolor del vínculo 0.25, atracción 0.24, malestar total d = 3.29; lo que más pesa: R-CARENCIA 0.81, F-4-ALCANCE 0.25, R-LLAMADA 0.24, S-8-EXPOSICION 0.15
  - equilibrio: vida 89 de 100, riqueza W 0.46, vínculo B 1.00, hermana presente P 1.0
  - dónde: casilla 22,26, dentro del anillo (radio 15, se encoge a 11 en 17 s)
  - quién hay cerca: rival (equipo A) a 5 casillas, herida, mano nada, cuerpo nada; rival (equipo D) a 5 casillas, sana, mano sword, cuerpo nada; mi hermana a 1 casillas, sana, mano knives, cuerpo nada; rival (equipo G) a 6 casillas, sana, mano nada, cuerpo nada; rival (equipo H) a 2 casillas, herida, mano spear, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «atacar_NW», intención {"type": "action", "do": "attack", "dir": "NW"}, resultado «ok»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 2, arrows×12 a 4, darts×8 a 2, camuflaje×1 a 0
  - qué acaba de pasar (últimos 2 s): golpes [10.8 de rival P14]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 21,27

- **PRUEBA de botiquín: cierro. Vida 89.0 → 100; lo que hizo (descontado lo esperado): cuerpo 11.0, recursos -1.0, vínculo 3.5; la vida tocó techo (lo ganado es al menos esto)** (segundo 394 s, tic 9460)
  - cómo me siento: dolor del cuerpo 0.35, dolor de recursos 0.59, dolor del vínculo 0.19, atracción 0.24, malestar total d = 3.07; lo que más pesa: R-CARENCIA 0.76, F-4-ALCANCE 0.24, R-LLAMADA 0.24, S-8-EXPOSICION 0.08
  - equilibrio: vida 100 de 100, riqueza W 0.69, vínculo B 1.00, hermana presente P 1.0
  - dónde: casilla 25,27, dentro del anillo (radio 15, se encoge a 11 en 15 s)
  - quién hay cerca: rival (equipo D) a 4 casillas, sana, mano sword, cuerpo nada; mi hermana a 4 casillas, sana, mano knives, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «noop», intención {"type": "action", "do": "none"}, resultado «ok»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 3, arrows×12 a 5, darts×8 a 1, camuflaje×1 a 3
  - qué acaba de pasar (últimos 2 s): golpes [ninguno]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 21,25

- **MI HERMANA ME CUENTA (canal) lo que vivió con ración: cuerpo 8.0, recursos -1.0, vínculo 1.0; lo creo con peso 3.359** (segundo 483 s, tic 11583)
  - cómo me siento: dolor del cuerpo 0.57, dolor de recursos 0.63, dolor del vínculo 0.30, atracción 0.24, malestar total d = 3.35; lo que más pesa: R-CARENCIA 0.75, F-4-ALCANCE 0.25, R-LLAMADA 0.24, S-8-EXPOSICION 0.15
  - equilibrio: vida 92 de 100, riqueza W 0.74, vínculo B 1.00, hermana presente P 1.0
  - dónde: casilla 26,24, dentro del anillo (radio 8, se encoge a 5 en 21 s)
  - quién hay cerca: rival (equipo B) a 5 casillas, sana, mano spear, cuerpo nada; rival (equipo C) a 2 casillas, herida, mano nada, cuerpo nada; rival (equipo D) a 3 casillas, sana, mano sword, cuerpo nada; rival (equipo D) a 1 casillas, sana, mano spear, cuerpo nada; mi hermana a 4 casillas, sana, mano knives, cuerpo nada; rival (equipo G) a 5 casillas, herida, mano nada, cuerpo nada; rival (equipo H) a 2 casillas, sana, mano nada, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «atacar_W», intención {"type": "action", "do": "attack", "dir": "W"}, resultado «no_ammo»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 2, darts×8 a 2, camuflaje×1 a 4, arrows×6 a 5
  - qué acaba de pasar (últimos 2 s): golpes [ninguno]; eventos ["{'type': 'death_fireworks', 'slot': 4, 'pos': [24, 29]}", "{'type': 'boom', 'direction': 'S'}"]; último parte de la hermana: vida 92, 0 botiquines, con agresor, en 21,25

- **MI HERMANA ME CUENTA (canal) lo que vivió con ración: cuerpo 12.5, recursos -2.0, vínculo 0.0; lo creo con peso 4.0** (segundo 492 s, tic 11808)
  - cómo me siento: dolor del cuerpo 0.50, dolor de recursos 0.63, dolor del vínculo 0.31, atracción 0.18, malestar total d = 3.34; lo que más pesa: R-CARENCIA 0.75, F-4-ALCANCE 0.24, R-LLAMADA 0.18, S-8-EXPOSICION 0.15
  - equilibrio: vida 92 de 100, riqueza W 0.74, vínculo B 1.00, hermana presente P 1.0
  - dónde: casilla 25,29, dentro del anillo (radio 8, se encoge a 5 en 12 s)
  - quién hay cerca: rival (equipo B) a 4 casillas, sana, mano spear, cuerpo nada; mi hermana a 1 casillas, sana, mano knives, cuerpo nada; rival (equipo H) a 3 casillas, herida, mano nada, cuerpo nada; rival (equipo H) a 7 casillas, herida, mano nada, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «noop», intención {"type": "action", "do": "none"}, resultado «ok»
  - qué hay alrededor (≤ 5 casillas): camuflaje×1 a 3, arrows×6 a 1
  - qué acaba de pasar (últimos 2 s): golpes [ninguno]; eventos ninguno; último parte de la hermana: vida 88, 0 botiquines, con agresor, en 25,29

- **GOLPE de 10.8 de vida, de rival P6** (segundo 502 s, tic 12036)
  - cómo me siento: dolor del cuerpo 0.73, dolor de recursos 0.65, dolor del vínculo 0.35, atracción 0.24, malestar total d = 3.55; lo que más pesa: R-CARENCIA 0.77, F-DANO 0.29, F-4-ALCANCE 0.25, S-7-AGRESOR 0.25
  - equilibrio: vida 71 de 100, riqueza W 0.59, vínculo B 1.00, hermana presente P 1.0
  - dónde: casilla 24,26, dentro del anillo (radio 8, se encoge a 5 en 2 s)
  - quién hay cerca: rival (equipo B) a 4 casillas, herida, mano spear, cuerpo nada; rival (equipo B) a 2 casillas, sana, mano nada, cuerpo nada; rival (equipo D) a 1 casillas, sana, mano sword, cuerpo nada; rival (equipo D) a 4 casillas, casi muerta, mano spear, cuerpo nada; rival (equipo E) a 1 casillas, sana, mano nada, cuerpo nada; mi hermana a 3 casillas, sana, mano knives, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «usar_botiquin», intención {"type": "action", "do": "use", "slot": 0}, resultado «no_ammo»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 2, darts×8 a 0, camuflaje×1 a 2, arrows×6 a 3, arrows×6 a 3, ración×4 a 3, darts×8 a 4, darts×4 a 4
  - qué acaba de pasar (últimos 2 s): golpes [10.8 de rival P6, 10.8 de rival P6]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 21,27

- **PRUEBA de botiquín: abro la ventana** (segundo 502 s, tic 12037)
  - cómo me siento: dolor del cuerpo 0.73, dolor de recursos 0.65, dolor del vínculo 0.35, atracción 0.24, malestar total d = 3.55; lo que más pesa: R-CARENCIA 0.77, F-DANO 0.29, F-4-ALCANCE 0.25, S-7-AGRESOR 0.25
  - equilibrio: vida 71 de 100, riqueza W 0.62, vínculo B 1.00, hermana presente P 1.0
  - dónde: casilla 24,26, dentro del anillo (radio 8, se encoge a 5 en 2 s)
  - quién hay cerca: rival (equipo B) a 4 casillas, herida, mano spear, cuerpo nada; rival (equipo B) a 2 casillas, sana, mano nada, cuerpo nada; rival (equipo D) a 1 casillas, sana, mano sword, cuerpo nada; rival (equipo D) a 4 casillas, casi muerta, mano spear, cuerpo nada; rival (equipo E) a 1 casillas, sana, mano nada, cuerpo nada; mi hermana a 3 casillas, sana, mano knives, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «atacar_S», intención {"type": "action", "do": "attack", "dir": "S"}, resultado «ok»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 2, darts×8 a 0, camuflaje×1 a 2, arrows×6 a 3, arrows×6 a 3, ración×4 a 3, darts×8 a 4, darts×4 a 4
  - qué acaba de pasar (últimos 2 s): golpes [10.8 de rival P6, 10.8 de rival P6]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 21,27

- **PRUEBA de botiquín: cierro. Vida 71.0 → 64; lo que hizo (descontado lo esperado): cuerpo 0.0, recursos 0.0, vínculo 1.8; CORTADA por un golpe; en la ventana recibí 7.2 de daño de rival P2** (segundo 503 s, tic 12070)
  - cómo me siento: dolor del cuerpo 0.80, dolor de recursos 0.65, dolor del vínculo 0.35, atracción 0.24, malestar total d = 3.61; lo que más pesa: R-CARENCIA 0.76, F-DANO 0.36, F-4-ALCANCE 0.25, R-LLAMADA 0.24
  - equilibrio: vida 64 de 100, riqueza W 0.65, vínculo B 1.00, hermana presente P 1.0
  - dónde: casilla 23,23, dentro del anillo (radio 8, se encoge a 5 en 1 s)
  - quién hay cerca: rival (equipo B) a 1 casillas, herida, mano spear, cuerpo nada; rival (equipo B) a 3 casillas, sana, mano nada, cuerpo nada; rival (equipo D) a 3 casillas, sana, mano sword, cuerpo nada; rival (equipo D) a 2 casillas, casi muerta, mano spear, cuerpo nada; rival (equipo E) a 2 casillas, sana, mano nada, cuerpo nada; mi hermana a 5 casillas, sana, mano nada, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «atacar_N», intención {"type": "action", "do": "attack", "dir": "N"}, resultado «no_ammo»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 1, darts×8 a 3, camuflaje×1 a 3, arrows×6 a 2, ración×4 a 2, darts×8 a 5, darts×4 a 5, botiquín×1 a 3
  - qué acaba de pasar (últimos 2 s): golpes [10.8 de rival P6, 7.2 de rival P2]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 22,27

- **PRUEBA de botiquín: abro la ventana** (segundo 504 s, tic 12086)
  - cómo me siento: dolor del cuerpo 0.76, dolor de recursos 0.65, dolor del vínculo 0.33, atracción 0.24, malestar total d = 3.56; lo que más pesa: R-CARENCIA 0.76, F-DANO 0.36, F-4-ALCANCE 0.25, R-LLAMADA 0.24
  - equilibrio: vida 64 de 100, riqueza W 0.62, vínculo B 1.00, hermana presente P 0.5
  - dónde: casilla 22,22, dentro del anillo (radio 8, se encoge a 5 en 0 s)
  - quién hay cerca: rival (equipo B) a 1 casillas, herida, mano spear, cuerpo nada; rival (equipo B) a 4 casillas, sana, mano nada, cuerpo nada; rival (equipo D) a 4 casillas, sana, mano sword, cuerpo nada; rival (equipo D) a 3 casillas, casi muerta, mano spear, cuerpo nada; rival (equipo E) a 4 casillas, sana, mano nada, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «atacar_E», intención {"type": "action", "do": "attack", "dir": "E"}, resultado «ok»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 2, darts×8 a 4, camuflaje×1 a 4, arrows×6 a 1, ración×4 a 1, botiquín×1 a 4
  - qué acaba de pasar (últimos 2 s): golpes [7.2 de rival P2]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 22,29

- **PRUEBA de botiquín: cierro. Vida 64.0 → 56; lo que hizo (descontado lo esperado): cuerpo 0.0, recursos 0.0, vínculo 0.0; CORTADA por un golpe; en la ventana recibí 7.2 de daño de rival P2** (segundo 504 s, tic 12090)
  - cómo me siento: dolor del cuerpo 0.85, dolor de recursos 0.66, dolor del vínculo 0.36, atracción 0.24, malestar total d = 3.68; lo que más pesa: R-CARENCIA 0.76, F-DANO 0.44, F-4-ALCANCE 0.25, S-7-AGRESOR 0.24
  - equilibrio: vida 56 de 100, riqueza W 0.62, vínculo B 1.00, hermana presente P 0.5
  - dónde: casilla 22,22, dentro del anillo (radio 8, se encoge a 5 en 0 s)
  - quién hay cerca: rival (equipo B) a 1 casillas, herida, mano spear, cuerpo nada; rival (equipo B) a 4 casillas, sana, mano nada, cuerpo nada; rival (equipo D) a 5 casillas, sana, mano sword, cuerpo nada; rival (equipo D) a 2 casillas, casi muerta, mano spear, cuerpo nada; rival (equipo E) a 3 casillas, sana, mano nada, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «move_E», intención {"type": "action", "do": "move", "dir": "E"}, resultado «blocked»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 2, darts×8 a 4, camuflaje×1 a 4, arrows×6 a 1, ración×4 a 1, botiquín×1 a 4
  - qué acaba de pasar (últimos 2 s): golpes [7.2 de rival P2, 7.2 de rival P2]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 22,29

- **PRUEBA de botiquín: abro la ventana** (segundo 506 s, tic 12135)
  - cómo me siento: dolor del cuerpo 0.80, dolor de recursos 0.65, dolor del vínculo 0.32, atracción 0.24, malestar total d = 3.59; lo que más pesa: R-CARENCIA 0.76, F-DANO 0.44, F-4-ALCANCE 0.25, R-LLAMADA 0.24
  - equilibrio: vida 56 de 100, riqueza W 0.65, vínculo B 1.00, hermana presente P 0.5
  - dónde: casilla 21,25, dentro del anillo (radio 8, se encoge a 5 en 0 s)
  - quién hay cerca: rival (equipo B) a 3 casillas, herida, mano spear, cuerpo nada; rival (equipo B) a 5 casillas, sana, mano nada, cuerpo nada; rival (equipo D) a 4 casillas, sana, mano sword, cuerpo nada; rival (equipo D) a 1 casillas, casi muerta, mano spear, cuerpo nada; rival (equipo E) a 5 casillas, sana, mano nada, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «noop», intención {"type": "action", "do": "none"}, resultado «ok»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 3, darts×8 a 3, camuflaje×1 a 1, arrows×6 a 4, arrows×6 a 2, ración×4 a 2, botiquín×1 a 3
  - qué acaba de pasar (últimos 2 s): golpes [7.2 de rival P2]; eventos ["{'type': 'death_fireworks', 'slot': 15, 'pos': [33, 32]}", "{'type': 'boom', 'direction': 'SE'}"]; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 21,29

- **PRUEBA de botiquín: cierro. Vida 56.0 → 46; lo que hizo (descontado lo esperado): cuerpo 0.0, recursos 0.0, vínculo -0.8; CORTADA por un golpe; en la ventana recibí 10.8 de daño de rival P6** (segundo 506 s, tic 12152)
  - cómo me siento: dolor del cuerpo 0.95, dolor de recursos 0.67, dolor del vínculo 0.37, atracción 0.24, malestar total d = 3.79; lo que más pesa: R-CARENCIA 0.76, F-DANO 0.56, F-4-ALCANCE 0.25, S-7-AGRESOR 0.25
  - equilibrio: vida 46 de 100, riqueza W 0.64, vínculo B 1.00, hermana presente P 0.5
  - dónde: casilla 21,26, dentro del anillo (radio 8, se encoge a 5 en 0 s)
  - quién hay cerca: rival (equipo B) a 4 casillas, herida, mano spear, cuerpo nada; rival (equipo B) a 6 casillas, sana, mano nada, cuerpo nada; rival (equipo D) a 1 casillas, sana, mano sword, cuerpo nada; rival (equipo D) a 4 casillas, casi muerta, mano spear, cuerpo nada; rival (equipo E) a 4 casillas, sana, mano nada, cuerpo nada
  - qué llevo: mano blowgun, zurrón [botiquín, red], cuerpo nada
  - qué hago: elegido «move_SE», intención {"type": "action", "do": "move", "dir": "SE"}, resultado «no_ammo»
  - qué hay alrededor (≤ 5 casillas): sword×1 a 3, darts×8 a 3, camuflaje×1 a 1, arrows×6 a 3, arrows×6 a 3, ración×4 a 3, botiquín×1 a 3
  - qué acaba de pasar (últimos 2 s): golpes [10.8 de rival P6]; eventos ninguno; último parte de la hermana: vida 100, 0 botiquines, sin agresor, en 21,29

