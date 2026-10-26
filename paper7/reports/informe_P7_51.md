# P7-51 · Comprobación sin coste: los `rate_limited` del canal en el campo P7-50

*12-oct-2026. Coste 0 (solo lectura de los 240 diarios válidos de P7-50 y los 8 apartados). `rate_P7_51.py` → `P7_51_rate.json`; ninguna cifra a mano. Lo que aporta Ari (zero-sum 0.1.19):
1 mensaje por 24 tics POR CRIATURA, común a todos los canales; un mensaje demasiado pronto se descarta y la observación siguiente trae `action_result` "rate_limited"; bloqueo
inicial de ≈ 480 tics en que se puede hablar (hasta ≈ 20 mensajes por hermana) sin moverse ni recibir golpes.*

## (a) ¿La guarda cuenta los `rate_limited` como pasos bloqueados?

No. `guarda_latencia_P7_29.py` (línea 32) cuenta como bloqueado solo `action_result == "blocked"` en un paso listo (`move_ready_in` = 0) y sin cuerpo en la casilla; el
`bloqueados` que la guarda guardó en el estado coincide con los `blocked` del diario en 240 de 240 vidas. Y además **no hubo ningún `rate_limited` en todo el campo**: 0 en
3.139.426 tics vivos (COMPARTE 1.567.185, SOLAS 1.572.241). Ninguna parada ni la equidad cambian.

`action_result` por brazo (tics vivos): COMPARTE ok 1.243.508, cooldown 300.456, blocked 18.573, no_target 2.548, no_ammo 1.934, inventory_full 166; SOLAS ok 1.253.983, cooldown 291.021, blocked 21.692, no_ammo 2.796, no_target 2.609, inventory_full 140.

## (b) Mensajes descartados por `rate_limited`, por brazo

Ninguno. COMPARTE: 62.744 partes E2 y 302 recuerdos M7 enviados en 120 vidas, 0 descartados; SOLAS: 62.942 partes E2, 0 M7, 0 descartados. Por construcción: el parte
va cada 25 tics (> 24) y el M7 ocupa el hueco de un parte, nunca dos seguidos (`hermanas_P7_48`), así que el límite común de 1 por 24 tics no se toca. M7 enviados dentro del
bloqueo inicial (tic < 480): 0 (el día empieza sin recuerdos nuevos que contar; los de ayer ya fueron de día o de noche). En los 8 diarios apartados tampoco hay `rate_limited`.

## Apunte para el capítulo 5 (no se toca ahora)

Pasar la «noche» al bloqueo inicial: en los ≈ 480 tics antes de moverse, hasta ≈ 20 mensajes por hermana por el canal `team` del mundo (1 por 24 tics), en vez de leer el cuaderno de
la otra en la carpeta. Con el tope actual de 5 recuerdos por noche cabe holgado (5 M7 = 120 tics); el recuerdo viajaría por el mundo, no por el archivo.
