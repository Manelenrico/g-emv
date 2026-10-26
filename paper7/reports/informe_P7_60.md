# P7-60 · Banco (coste cero): ¿la regla «lo contado pesa intensidad × vínculo» hace algo?

*13-oct-2026. Propuesta de Ari. Sobre los cuadernos por día de COMPARTE de P7-50 (`P7_50_res`), con la fusión por evento de P7-55. `analiza_P7_60.py` → `P7_60_datos.json`;
`escribe_informe_P7_60.py` (este informe; ninguna cifra a mano). `motor/model.py` intacto. Plataforma 0 créditos; consola 0 $.*

## Qué se hace

La creencia de cada hermana (cuerpo, dentro; la regla del cuerpo de P7-55: sin cortes, neutro de peso 1, «al menos» solo si sube, olvido 0,95 por día) se recalcula con el vínculo B
FIJADO a mano en 1, 0,5 y 0,25 para los recuerdos recibidos (contados: intensidad de la emisora × B; vistos: intensidad sin B × B). Lo vivido queda intacto. Para cada nivel, lo
aprendido de la otra es (a − b) de P7-55: a = creencia con todos los recuerdos deduplicados, b = solo con los vividos (b no depende de B).

**Es lazo abierto**: los recuerdos, las pruebas y las decisiones son los que hubo con el B de verdad; aquí solo cambia el peso al releerlos. Muestra la ESCALA de la regla, no su efecto
sobre la conducta (eso pide un campo con un vínculo que varíe de verdad).

## El vínculo que hubo

En los cuadernos del día 20, los 334 recuerdos recibidos de las seis hermanas llevan B entre 1,00 y 1,00: **el vínculo estuvo saturado en 1 todo el campo**. Por eso la regla no
hizo nada en P7-50, y el recálculo con B = 1 da exactamente lo mismo que con el B registrado (comprobación del banco).

## Lo aprendido de la otra (a − b) al día 20, por nivel de B

| serie · hermana | objeto | b (solo vivido) d20 | a − b: B = 1 · 0,5 · 0,25 | a − b relativo a B = 1: 0,5 · 0,25 | media d1-20 de a − b: B = 1 · 0,5 · 0,25 |
|---|---|---:|---|---|---|
| s1 a10 valiente | botiquin | 24,1 | 16,82 · 13,26 · 9,28 | 79 % · 55 % | 7,20 · 5,23 · 3,40 |
| s1 a10 valiente | racion | 13,3 | 0,99 · 0,70 · 0,44 | 70 % · 44 % | 1,15 · 0,75 · 0,43 |
| s1 a10 valiente | red | 0,0 | 0,00 · 0,00 · 0,00 | — · — | 0,00 · 0,00 · 0,00 |
| s1 a10 valiente | camuflaje | 0,0 | 2,91 · 2,37 · 1,73 | 81 % · 59 % | 0,90 · 0,71 · 0,49 |
| s1 a11 prudente | botiquin | 43,2 | -2,28 · -1,41 · -0,69 | 62 % · 30 % | 4,00 · 3,02 · 1,70 |
| s1 a11 prudente | racion | 14,4 | -0,06 · -0,04 · -0,02 | 60 % · 34 % | 1,17 · 0,90 · 0,61 |
| s1 a11 prudente | red | 0,0 | 0,00 · 0,00 · 0,00 | — · — | 0,00 · 0,00 · 0,00 |
| s1 a11 prudente | camuflaje | 3,6 | -0,72 · -0,40 · -0,21 | 55 % · 29 % | -0,28 · -0,16 · -0,09 |
| s2 a10 valiente | botiquin | 20,4 | 18,86 · 13,26 · 6,55 | 70 % · 35 % | 5,70 · 4,54 · 2,14 |
| s2 a10 valiente | racion | 13,8 | 0,40 · 0,24 · 0,14 | 61 % · 34 % | 0,21 · 0,12 · 0,06 |
| s2 a10 valiente | red | 0,0 | 3,15 · 1,98 · 1,13 | 63 % · 36 % | 0,95 · 0,64 · 0,39 |
| s2 a10 valiente | camuflaje | 0,0 | 0,49 · 0,44 · 0,36 | 90 % · 75 % | 0,37 · 0,31 · 0,24 |
| s2 a11 prudente | botiquin | 34,7 | 4,50 · 2,67 · 1,47 | 59 % · 33 % | 7,25 · 4,89 · 3,14 |
| s2 a11 prudente | racion | 13,1 | 1,04 · 0,74 · 0,47 | 71 % · 45 % | 5,65 · 4,71 · 3,62 |
| s2 a11 prudente | red | 6,8 | -3,80 · -2,63 · -1,63 | 69 % · 43 % | -0,92 · -0,60 · -0,35 |
| s2 a11 prudente | camuflaje | 0,5 | -0,04 · -0,02 · -0,01 | — · — | -0,06 · -0,03 · -0,02 |
| s3 a10 valiente | botiquin | 37,3 | 8,50 · 6,81 · 5,04 | 80 % · 59 % | 6,49 · 4,87 · 3,22 |
| s3 a10 valiente | racion | 10,0 | 1,34 · 0,89 · 0,53 | 66 % · 39 % | 1,76 · 1,18 · 0,76 |
| s3 a10 valiente | red | 0,0 | 0,00 · 0,00 · 0,00 | — · — | 0,00 · 0,00 · 0,00 |
| s3 a10 valiente | camuflaje | 0,0 | 0,00 · 0,00 · 0,00 | — · — | 0,00 · 0,00 · 0,00 |
| s3 a11 prudente | botiquin | 44,9 | 0,87 · 0,35 · 0,18 | 41 % · 21 % | 2,32 · 1,58 · 1,00 |
| s3 a11 prudente | racion | 13,3 | -1,96 · -1,25 · -0,79 | 64 % · 40 % | -0,28 · -0,23 · -0,14 |
| s3 a11 prudente | red | 0,0 | 0,00 · 0,00 · 0,00 | — · — | 0,00 · 0,00 · 0,00 |
| s3 a11 prudente | camuflaje | 0,0 | 0,00 · 0,00 · 0,00 | — · — | 0,00 · 0,00 · 0,00 |

(Relativo solo donde |a − b| a B = 1 es ≥ 0,05.)

## Lectura

- **La regla escala, pero menos que proporcional.** Donde lo recibido movió la creencia (17 casos hermana-objeto), bajar B a la mitad deja de media un 67 % de lo aprendido
  de la otra (entre 41 % y 90 %), y bajarlo a un cuarto deja un 42 % (entre 21 % y 75 %). No es lineal porque la creencia es una media
  ponderada: al bajar el peso de lo recibido, lo vivido y el neutro pesan más en el denominador, y el efecto se reparte; por construcción, donde lo recibido domina el denominador (muchos recibidos, pocos vividos) cae menos.
- **El signo no cambia**: a ningún nivel lo recibido hace creer lo contrario que a B = 1; solo se encoge.
- **En P7-50 la regla no hizo nada** porque B estuvo siempre en 1. Que «intensidad × vínculo» importe para la conducta sigue sin medir: hace falta un campo donde el vínculo varíe de
  verdad (y aquí se ve de qué tamaño sería el efecto sobre la creencia: con B = 0,5, un 33 % menos de lo aprendido de la otra, de media).
