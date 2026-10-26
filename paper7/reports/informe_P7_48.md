# P7-48 · Capítulo 4, construcción (sin sello): las hermanas que se cuentan lo aprendido, comprobadas en local

*12-oct-2026. Solo local (`coworld play` en el Mac): plataforma 0 créditos (saldo **228**, dato de Manel 12-oct 06:47); consola 0 $. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`,
no se lee ni se escribe. Piezas nuevas (las del campo intactas): `escala_P7_48.py` = `adcdd40ba2b046b5df03964c1cb56f83` (la intensidad en su escala, SIN habituación), `hermanas_P7_48.py` = `f75c4060afe5a681ccaa9dff65461d24`,
`campo_P7_48.py`, `policy_pareja_P7_48.py`, `Dockerfile.pareja_P7_48` (ARG HERMANAS = comparte | solas; GEMV_OJOS=1 en los dos). Comprobación: `local48_P7_48.py` → `P7_48_local.json`
(partidas en `_P7_48_local/`, cuadernos encadenados en `cuadernos_P7_48/`); `escribe_informe_P7_48.py` (este informe; ninguna cifra a mano).*

## Sección 1 · Lo que permite el juego (medido) y lo construido

- **Canal**: `talk` con `broadcast`, **`team` (privado de la pareja)** y `dm`; 1 mensaje por 24 tics (`rate_limited` si no), 120 caracteres ASCII, latencia 2 tics, sin límite de distancia,
  solo entre vivas. Con los ojos compartidos el parte E2 ocupa un hueco cada 25 tics: el recuerdo va EN LUGAR de un parte, nunca dos seguidos (el parte no se pierde más de 25 tics).
  No hay noche en el juego: la noche es entre partidas, con los cuadernos de las dos en la misma carpeta.
- **Lo que ve una de la otra**: por la vista `pos`, `hp_band`, `hand`, `body`, `netted`, `poisoned`, `channeling`; por el parte E2 (cada 25 tics) hp exacto, botiquines a bordo, agresor,
  rivales y recursos que ella ve. El vínculo = `mem.roce_B` (0-1, appraisal congelado). Nada de esto toca `model.py`.
- **Pareja** (Manel): una valiente (asiento par) y una prudente (impar); carácter como en P7-42, solo en la cautela del probar (`filo_P7_40.MIEDO`; `model.py` no expone el miedo del
  cuerpo, así que «la mitad del miedo del cuerpo» no es alcanzable sin tocarlo: se declara). Igual en los dos brazos.
- **Recuerdo entero**: efecto por dominio, importancia, contexto (dentro/fuera, golpeado), foto emocional (dolor F/R/S, positivo, d), últimas 4 acciones, día, tic, `al_menos`.
  Marca `origen` = vivido / visto / contado, `via` = canal | noche, `de`, `B`. **Peso recibido = intensidad (en su escala) × B** (B ≤ 1: nunca más que el vivido).
- **Mensaje M7** (90-95 caracteres): `M7 P<asiento> d<día> t<tic> <objeto><situación><golpeado> e<c>,<r>,<v> i<c>,<r>,<v> f<F>,<R>,<S>,<pos>,<d> a<acciones> n<intensidad> m<al_menos>`;
  parser estricto (regex); lo que no cuadra se cuenta como malo.
- **Mirando**: vigilia al ver en el parte un botiquín menos o el camuflaje puesto; ventana = parte anterior + 4 partes; efecto = hp máximo − hp anterior; descartes: agresor en la
  ventana, daño (hp baja entre partes), la hermana calla, el botiquín acabó en mi zurrón (regalo), o la vida llena (soltar/dar, no usar). Importancia = |Δ malestar propio| en la
  ventana; foto y situación propias; acciones = lo que hacía la hermana (mano, cuerpo, channeling, distancia).
- **Noche** (Manel, cambio 1): como mucho los 5 vividos MÁS INTENSOS de ayer de la hermana que no llegaron de día, con el B del cierre de ayer.

## Sección 2 · La comprobación local (lazo cerrado, partidas de verdad)

Cada brazo, una cadena de 3 días con nuestra imagen en los 16 asientos (8 parejas valiente/prudente; no hay imágenes de los rivales: todas las vidas son nuestras y todas mueren
antes del final); el día d+1 se hornea con los cuadernos que las 16 escribieron el día d.

| partida | vidas | tics (media) | mueren | pruebas por vida | recuerdos por vida: vividos · vistos · contados canal · contados noche | vistos descartados (motivos) | mensajes M7 enviados · malos | pesos = intensidad × B: bien · mal | ms mediana (media) · p95 máx | % sobre el tic (media) · % bloqueados |
|---|---:|---:|---:|---:|---|---|---|---|---|---|
| comparte_d1 | 16 | 6.196 | 16 | 1,44 | 1,38 · 0,06 · 0,69 · 0,00 | 0 (—) | 11 · 0 | 12 · 0 | 3,36 · 12,2 | 0,020 · 5,85 |
| comparte_d2 | 16 | 6.668 | 16 | 2,31 | 2,31 · 0,06 · 1,19 · 0,06 | 0 (—) | 19 · 0 | 21 · 0 | 3,00 · 11,6 | 0,002 · 10,41 |
| comparte_d3 | 16 | 6.490 | 16 | 2,00 | 1,94 · 0,06 · 1,12 · 0,19 | 0 (—) | 18 · 0 | 22 · 0 | 2,90 · 12,5 | 0,002 · 5,69 |
| solas_d1 | 16 | 5.652 | 16 | 2,12 | 2,06 · 0,00 · 0,00 · 0,00 | 0 (—) | 0 · 0 | 0 · 0 | 3,61 · 12,8 | 0,011 · 3,58 |
| solas_d2 | 16 | 6.064 | 16 | 1,44 | 1,38 · 0,00 · 0,00 · 0,00 | 0 (—) | 0 · 0 | 0 · 0 | 3,50 · 13,7 | 0,005 · 2,46 |
| solas_d3 | 16 | 6.406 | 16 | 1,81 | 1,81 · 0,00 · 0,00 · 0,00 | 0 (—) | 0 · 0 | 0 · 0 | 3,34 · 12,2 | 0,005 · 6,84 |

| brazo · hermana | vidas | tics (media) | pruebas por vida | vividos · vistos · canal · noche (por vida) | mensajes por vida | vistos descartados |
|---|---:|---:|---:|---|---:|---:|
| comparte · prudente | 24 | 6.646 | 1,96 | 1,88 · 0,00 · 0,75 · 0,04 | 1,25 | 0 |
| comparte · valiente | 24 | 6.257 | 1,88 | 1,88 · 0,12 · 1,25 · 0,12 | 0,75 | 0 |
| solas · prudente | 24 | 6.144 | 2,25 | 2,25 · 0,00 · 0,00 · 0,00 | 0,00 | 0 |
| solas · valiente | 24 | 5.938 | 1,33 | 1,25 · 0,00 · 0,00 · 0,00 | 0,00 | 0 |

- **Llegan y pesan como se dice**: 55 recuerdos recibidos (vistos y contados) con peso = intensidad × B exacto; 0 con peso distinto. La noche entrega comparte_d1: 0, comparte_d2: 1, comparte_d3: 3, solas_d1: 0, solas_d2: 0, solas_d3: 0
  recuerdos (en el día 1 no hay ayer; en `solas` la noche está apagada).
- **Latencia**: p95 local ≤ 8 ms en todas las partidas: NO (máximo del p95 por vida 13,7 ms; medianas 2,90-3,61 ms); 0 % sobre el tic: NO (máximo 0,020 %).
  Referencia sin las piezas de P7-48, mismas partidas locales de P7-47 (16 contenedores en el mismo Mac): p95 máximo APRENDE_p 13,7, APRENDE_v 12,8 ms, sobre el tic 0,013, 0,033 %:
  la cola de latencia es la del montaje local (16 políticas y el motor en una máquina), no de las piezas; en plataforma el campo P7-45 dio p95 2-20 ms con cachés.

## Lectura (construcción; sin sello)

Las tres vías funcionan en lazo cerrado: el canal manda recuerdos enteros en los huecos del parte sin perder ninguno por formato, el mirar apunta usos de la hermana con sus descartes
contados, y la noche entrega como mucho 5 por hermana con el B del cierre. Los pesos son intensidad × B sin excepción. La latencia local NO cumple el p95 ≤ 8 ms ni el 0 % sobre el tic, pero con los mismos números que las partidas locales sin estas piezas (P7-47): es el montaje de 16 políticas en un Mac, no la construcción; se mide de verdad en plataforma. El mundo local (16 criaturas nuestras, vidas cortas) da pocas
pruebas por vida; medir si compartir cambia lo aprendido pide un campo en la plataforma, con sello: queda para la mesa.
