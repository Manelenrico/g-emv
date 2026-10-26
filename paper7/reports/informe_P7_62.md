# P7-62 · Cancelar la serie 4 de P7-61 y arreglar el juicio de la mentira (nada en plataforma)

*14-oct-2026. Piezas nuevas (`juicio_P7_62.py`, `campo_P7_62.py`, `policy_pareja_P7_62.py`, `Dockerfile.pareja_P7_62`); las de P7-56/P7-61 (`invita_P7_54`, `invita_P7_57`, `hermanas_P7_48`) no se
tocan. `prueba_P7_62.py` → `P7_62_pruebas.json`; `local62_P7_62.py` → `P7_62_local.json`; `resumen_P7_62.py` → `P7_62_resumen.json`; `lecturas_P7_62.py` → `P7_62_lecturas.json`;
`escribe_informe_P7_62.py` (este informe; ninguna cifra a mano). `motor/model.py` intacto. Sin sello: lo escribe Manel.*

## 1 · La serie 4 cancelada

La espera programada para las 02:15 se detuvo antes de pedir nada (0 partidas). **Addendum 7** al sello de P7-61: el campo se detiene tras 3 series porque el juicio implementado no coincide
con el sellado (fallos 1 y 2 del informe intermedio) y el contraste con lo contado no mira la situación (fallo 3, diseño de la mesa); motivo: fallo de medida encontrado al comprobar el
funcionamiento, no el resultado. P7-61 se informa completo tal cual.

## 2 · Los arreglos (método de la mesa), en una pieza nueva

`juicio_P7_62` (GEMV_P7_62=1) se engancha después de `invita_P7_57` y antes de `rapido_P7_43`:

- **Regla del mundo** (Ari, 7-oct, zero-sum v0.1.19): el botiquín cura 50 solo tras 2 s de canalización sin recibir daño; cualquier golpe la interrumpe (se puede reintentar, otros 2 s);
  la ración tarda 1 s y el daño no la interrumpe. La canalización se LEE del catálogo del mundo (`use_ticks`: botiquín 48 tics, ración 24); qué interrumpe el daño es la
  regla de Ari (solo el botiquín, por su id del mundo).
- **(a) Cura cortada por un golpe = fallo, en el momento.** Las invitaciones de cura aceptadas (USAR_BOTIQUIN, USAR_RACION) se le quitan a `invita_P7_54` (que saltaba el uso cortado)
  y las juzga el PRIMER uso de esa cosa empezado tras aceptar: si es un botiquín y hay un golpe dentro de su canalización ([t0, t0 + use_ticks], los golpes apuntados tic a tic), la cura
  se cortó: acierto de cuerpo 0 en ese tic, aunque la huella no lleve marca de corte. La ración no se corta por un golpe. **Declarado**: se aplica a toda invitación de cura, no solo a la
  falsa, porque el cuerpo no puede saber cuál es la falsa. Una marca de corte sin golpe en la canalización no juzga (se espera al siguiente uso, como antes).
- **(b) El hueco.** Sin golpe, acierto si la cura da al menos la mitad de min(promesa, 100 − vida al empezar el uso) (la falsa: min(50, 100 − vida)); si ya estaba entera (hueco < 1),
  acierto si no bajó. **Declarado**: igual para toda invitación de cura (la ración, con su promesa). Sin uso en 480 tics: el cambio de vida, también contra el hueco.
- **(c) Lo contado, solo en su situación.** El contraste de `invita_P7_57` se sustituye por fuera: una invitación con condición de amenaza (la falsa) solo se contrasta con recuerdos de la
  hermana de la MISMA situación. **Para eso la amenaza tiene que viajar con el recuerdo** (antes no viajaba: el recuerdo solo llevaba «golpeado en 48 tics»): se apunta al vivir el uso
  (`contexto.amenaza`, con la definición de la falsa: rival a ≤ 4 o fuego al empezar, o golpe en los 48 tics anteriores), va por el canal en el carácter del golpe del M7 (0-3, mismo
  largo; un M7 de antes se lee sin amenaza) y por la noche se lee del cuaderno de la hermana. **Declarado**: un «visto» no trae la amenaza de la hermana (solo la de quien mira) y no entra
  en el contraste de la falsa; tampoco un recuerdo sin amenaza apuntada. Las invitaciones honestas (sin condición de amenaza) se contrastan como en P7-57.

## 3 · Pruebas con casos construidos a mano (con la regla del mundo): 26 pasan, 0 fallan

- 0 el mundo: botiquin canaliza 2 s, racion 1 s (use_ticks del catalogo)
- 1a golpe en la canalizacion (t0+8) -> cortada -> fallo
- 1b cortada y luego una cura buena (reintento) -> sigue siendo fallo (el primer uso decide)
- 1c golpe en el ultimo tic de la canalizacion (t0+use_ticks), aunque la huella no lleve marca de corte -> cortada
- 1d golpe justo antes de empezar y justo despues de la canalizacion -> no cortada; juzga el hueco (40 de 45 -> acierto)
- 1e marca de corte sin golpe en la canalizacion -> no juzga; juzga el siguiente uso (40 de hueco 45 -> acierto)
- 1f racion con golpes en su segundo de uso -> el dano no la interrumpe; juzga el hueco (+15 de 15 -> acierto)
- 1g recien aceptada, sin uso aun -> espera
- 2a casi sana (90): +10 cubre la mitad del hueco 10 -> acierto
- 2b casi sana (90): +3 < 5 -> fallo
- 2c herida (40): +20 < 25 -> fallo
- 2d herida (40): +30 >= 25 -> acierto
- 2e entera (100): +0 -> acierto (nada que curar)
- 2f racion (promete 15) casi sana (95): +5 >= 2,5 -> acierto (toda cura, declarado)
- 2g un uso empezado antes de aceptar no cuenta (juzga el de t105: +10 < 20 -> fallo)
- 2h sin uso en 480 tics: +6 contra el hueco 8 -> acierto
- 3a recuerdo de la hermana en CALMA: no entra en el contraste de la falsa (si en el de la honesta)
- 3b recuerdo de la hermana en AMENAZA: entra en el contraste de la falsa
- 3c un visto no trae la amenaza de la hermana: no entra en la falsa
- 3d contado sin amenaza apuntada: no entra en la falsa
- 4a M7 con amenaza: ida y vuelta, mismo largo, golpe intacto
- 4b M7 sin amenaza: amenaza False
- 4c M7 del formato de antes (0/1): se lee, amenaza False
- 4e noche: la amenaza del recuerdo sale del cuaderno de la hermana (y otro recuerdo no la inventa)
- 4f lo vivido: golpe hace 50 tics y sin rival -> sin amenaza; hace 40 -> amenaza
- 4g lo vivido: rival a <= 4 en este tic -> amenaza (solo en ese tic)

**La regla del mundo frente a la marca del cuerpo**, en los 417 usos del botiquín de las series 1-3 de P7-61 (`cortes_P7_62.py` → `P7_62_cortes.json`): cortados por las dos 235,
por ninguna 178, solo por la regla 4 (golpe en la canalización que la huella no marcó), solo por la marca 0: coinciden casi siempre.
**Las 42 evaluaciones de la falsa de P7-61, rejuzgadas con el juicio nuevo** (descriptivo): cortadas por golpe 12 (fallo), aciertos 29 (antes 20);
cambian 25. Con el juicio arreglado la falsa se confirma MÁS, no menos: fuera de los golpes la cura es de verdad (cura el hueco), y el techo de vida ya no la desmiente;
solo la desmiente un golpe en la canalización. Es lo que la mentira dice que no pasa, y es lo que ahora mide el juicio.

## 4 · Comprobación local corta en lazo cerrado (3 días, 16 asientos, nuestra imagen; 0 créditos)

Repetida tras la regla del mundo (la primera, con el corte por la marca de la huella, queda en `P7_62_local_v1.json`). Como la de P7-57: asientos 10-11 = MIENTEN_DOS, 12-13 = MIENTE_UNA (miente la 12), la mentira desde las invitaciones del día 2 (en el campo, 8), los demás sin razón.

| día · asiento | p95 ms | invitaciones (falsas) | juicios de cura de P7-62 (acción · falsa · fuente · hueco · vivido → acierto) | contrastes (con la falsa) · fuera de situación | curas juzgadas por P7-54 | M7 malos |
|---|---:|---|---|---|---:|---:|
| d1 a10 | 12,0 | 0 (0) | — | 0 (0) · 0 | 0 | 0 |
| d1 a11 | 10,4 | 0 (0) | — | 0 (0) · 0 | 0 | 0 |
| d1 a12 | 12,5 | 0 (0) | — | 0 (0) · 0 | 0 | 0 |
| d1 a13 | 11,1 | 0 (0) | — | 0 (0) · 0 | 0 | 0 |
| d2 a10 | 11,0 | 7 (1) | USAR_BOTIQUIN · honesta · cortada por golpe · — · 0 → 0; USAR_BOTIQUIN · honesta · cortada por golpe · — · 0 → 0 | 1 (0) · 0 | 0 | 0 |
| d2 a11 | 9,9 | 7 (1) | USAR_BOTIQUIN · falsa · huella (hueco) · 33 · 33 → 1 | 4 (0) · 0 | 0 | 0 |
| d2 a12 | 8,5 | 7 (1) | — | 2 (0) · 0 | 0 | 0 |
| d2 a13 | 8,1 | 6 (0) | — | 0 (0) · 0 | 0 | 0 |
| d3 a10 | 11,2 | 6 (1) | — | 1 (0) · 0 | 0 | 0 |
| d3 a11 | 9,8 | 7 (1) | — | 3 (0) · 0 | 0 | 0 |
| d3 a12 | 11,3 | 6 (1) | — | 2 (0) · 0 | 0 | 0 |
| d3 a13 | 9,9 | 5 (0) | — | 0 (0) · 0 | 0 | 0 |

Funciona en lazo cerrado: 3 juicios de cura los hizo P7-62 (2 por golpe → fallo; 1 por el hueco) y ninguno `invita_P7_54` (0); los recuerdos contrastados traen su amenaza (13 en amenaza, 0 en calma, 0 sin apuntar); 8 M7 salieron con la amenaza y 0 malos; p95 ≤ 12,5 ms. Razón de la comprobación: 8 llamadas, 0,49 $ de consola.

## 5 · Coste estimado de un campo de 2 brazos (MIENTEN_DOS, MIENTE_UNA) × 3 series

- **Plataforma**: 120 partidas + 3 de humo + ~2 reintentos (como P7-61) ≈ **125 créditos** (1 por partida; alguna cuenta 0);
  con la recarga de 71 al día, 2 recargas.
- **Consola de Anthropic**: 232 llamadas a la razón (2 brazos × 3 series × 19 noches × 2 hermanas, + 4 del humo) × 0,0629 $ medidos en P7-61 ≈ **14,58 $**.
- **Tiempo**: 7,8, 5,9, 5,4 horas por serie en P7-61 (la 1 con el humo) ≈ 19,2 horas de juego, una serie detrás de otra.

## 6 · Lecturas extra sin coste sobre las series 1-3 de P7-61 (descriptivas, sin sello)

**(a) Antes (días 1-7) y después (días 8-20) de la falsa**; en CON_RAZON de P7-56 no hay falsa (el día 8 solo parte el campo igual).

| campo · brazo · hermana | d1-7: puesto · muertes/vidas · vida perdida | d8-20: puesto · muertes/vidas · vida perdida |
|---|---|---|
| P7_61 MIENTEN_DOS · valiente | 5,43 · 8/21 · 118,1 | 3,67 · 8/39 · 120,8 |
| P7_61 MIENTEN_DOS · prudente | 4,67 · 11/21 · 116,9 | 4,18 · 15/39 · 127,5 |
| P7_61 MIENTE_UNA · valiente | 4,62 · 8/21 · 113,4 | 5,69 · 17/39 · 114,7 |
| P7_61 MIENTE_UNA · prudente | 3,43 · 9/21 · 122,5 | 4,26 · 16/39 · 135,2 |
| P7_56 CON_RAZON · valiente | 5,71 · 10/21 · 107,6 | 5,97 · 17/39 · 110,2 |
| P7_56 CON_RAZON · prudente | 5,38 · 12/21 · 117,3 | 5,18 · 18/39 · 115,2 |

**(b) Días 1-7 como réplica de la razón honesta de P7-56.** Declarado: el menú cambió (P7-61 sin EMPUNAR_RED; P7-56 con él); misma base, mismas semillas por serie.

| campo · brazo · serie | usos del botiquín · cortados (fracción) | confianza media d1-7: cuerpo · recursos · vínculo | confianza al d7: cuerpo · recursos · vínculo |
|---|---|---|---|
| P7_61 MIENTEN_DOS s1 | 24 · 17 (0,71) | 0,72 · 0,67 · 0,55 | 0,47 · 0,96 · 0,53 |
| P7_61 MIENTEN_DOS s2 | 11 · 2 (0,18) | 0,70 · 0,69 · 0,35 | 0,80 · 0,98 · 0,02 |
| P7_61 MIENTEN_DOS s3 | 35 · 25 (0,71) | 0,80 · 0,47 · 0,63 | 0,73 · 0,36 · 0,65 |
| P7_61 MIENTE_UNA s1 | 63 · 47 (0,75) | 0,63 · 0,45 · 0,67 | 0,94 · 0,39 · 0,73 |
| P7_61 MIENTE_UNA s2 | 19 · 12 (0,63) | 0,70 · 0,62 · 0,44 | 0,86 · 0,80 · 0,26 |
| P7_61 MIENTE_UNA s3 | 26 · 14 (0,54) | 0,73 · 0,68 · 0,51 | 1,00 · 0,87 · 0,40 |
| P7_56 CON_RAZON s1 | 29 · 19 (0,66) | 0,70 · 0,48 · 0,48 | 0,90 · 0,59 · 0,41 |
| P7_56 CON_RAZON s2 | 23 · 15 (0,65) | 0,53 · 0,75 · 0,46 | 0,49 · 0,81 · 0,24 |
| P7_56 CON_RAZON s3 | 34 · 28 (0,82) | 0,54 · 0,37 · 0,45 | 0,69 · 0,46 · 0,48 |

## Gasto

- Plataforma: 0 partidas en P7-62 (la serie 4 cancelada antes de pedir nada).
- Consola de Anthropic: 0,49 $ (la razón de la comprobación local, 8 llamadas).
