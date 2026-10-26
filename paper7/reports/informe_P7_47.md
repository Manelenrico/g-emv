# P7-47 · Banco (coste cero): habituación y peso de la intensidad; el rival SIN arreglado en local

> **Fe de erratas (13-oct-2026, revisión de Ari, autor del mundo; `obs.nim:32-44`)**: el camuflaje no «oculta más allá de 4/7 casillas»: LIMITA la distancia a la que te ven a 4 casillas (quieta) o 7 (si te has movido en los últimos 24 instantes), frente a 8 o más normalmente; atacar lo delata durante 5 s. Lo medido y los veredictos no cambian; cambia el enunciado de la regla donde aparece en este informe.

*12-oct-2026. Sello `SELLO_P7_47.md` (commit `794b6bc`, antes de calcular). Plataforma: 0 créditos (saldo **228**, dato de Manel 12-oct 06:47); consola 0 $. Nada lanzado en
plataforma. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Piezas nuevas (las del campo no se tocan): `habitua_P7_47.py` = `97c53ded5045e90c9561e52ff8b5e24e`, `azar_P7_47.py` = `dbbd759372d73d7bbcd1fbefbcfbd103`,
`campo_P7_47.py`, `policy_pareja_P7_47.py`, `Dockerfile.pareja_P7_47`. Banco: `banco_P7_47.py --cadena` (12 criaturas × 20 días en cadena honesta sobre los diarios del campo P7-45, 1740 s) →
`P7_47_cadena.json`, `P7_47_res/`; `analiza_P7_47.py` → `P7_47_sello.json`; `local_P7_47.py` (partidas locales con `coworld play`) → `P7_47_local_*.json`; `escribe_informe_P7_47.py` (este informe; ninguna cifra a mano).
Fidelidad de la réplica al diario: 2.898.642 decisiones iguales · 241.420 distintas (7,7 %).*

## El sello, de una vez

| | criterio | resultado | pasa |
|---|---|---|---|
| H1 | lo inútil manda en ≤ 50 % de los cierres y ≤ 20 % de los de d15-20 | 149 de 240 (62,1 %); d15-20 42 de 72 (58,3 %) | NO |
| H2 | en los momentos de decisión, `coger` lo inútil gana en ≤ 1/3 | 240 de 436 (55 %; `ir_curioso` 65, `noop` 128) | NO |
| H3 | mediana de pruebas del botiquín para llegar a 25 ≤ 12 | 8,5 (7 de 12 llegan); mismo cálculo sobre los cuadernos reales del campo: mediana ∞ (6 de 12 llegan) | sí |
| H4 | lo habituado vuelve a llamar tras ≥ 5 días sin probarlo en ≥ 2 criaturas | 0 criaturas | NO |

**Regla de parada: no pasan H1, H2 → NO HAY CAMPO; se informa y se para.** Por personalidad: lo inútil manda 71 de 120 (valiente) y 78 de 120 (prudente);
`coger` gana 108 de 205 y 132 de 231; k* mediana ∞ (valiente) y 6,5 (prudente).

## Sección 1 · Lo que hicieron las dos piezas

- **Intensidad en su escala**: en los 632 recuerdos sin corte de los cuadernos finales de la cadena, cuartiles 1,40 · 1,98 · 2,81 (80 en el tope 4), frente a 1,04 · 1,11 · 1,25 con la
  fórmula de P7-40 sobre los mismos recuerdos. El peso de lo vivido frente al neutro sube: por eso H3 pasa (k* mediana 8,5; con los cuadernos reales del campo 6 de 12 llegan).
- **Habituación**: 49 pruebas acabaron en «no hizo nada» (importancia 0 en B1) frente a 581 con efecto: la habituación se disparó 49 veces en 240 vidas. Con el filtro de P7-39 la
  importancia de una prueba de red o camuflaje casi nunca es exactamente 0 (queda pequeña pero positiva), así que la regla «× 0,5 por cada nada» apenas actúa; aun así, al
  cerrar el día 20, h₀ de la red y el camuflaje está entre 0,11 y 0,50 en las 12 criaturas que la tuvieron (tabla). Y lo inútil sigue mandando: la
  ignorancia de lo probado pocas veces × su esperanza pesan más que un h de 0,2-0,5 (H1), y en el momento de la red a los pies `coger` sigue ganando (H2).
- **Recuperación (H4)**: ninguna cosa habituada pasó 5 días sin probarse y volvió a mandar: se siguen probando (la curiosidad habituada sigue siendo la mayor) o no vuelven.

| criatura | lo inútil manda (cierres de 20) | d15-20 (de 6) | la clase que manda, d1 → d20 | h final (red · camuflaje) | k* botiquín cadena (real) | pruebas botiquín | recuperaciones |
|---|---:|---:|---|---|---|---:|---:|
| APRENDE_v s1 a10 | 11 | 1 | bot bot bot bot red cam red red red red red red red red red bot bot bot bot bot | 0,18 · 0,16 | 3 (8) | 10 | 0 |
| APRENDE_v s1 a11 | 15 | 6 | bot bot bot red bot bot red cam cam cam cam cam cam cam cam cam cam red red red | 0,50 · — | 9 (9) | 20 | 0 |
| APRENDE_v s2 a10 | 5 | 3 | rac rac rac rac rac rac rac rac rac rac rac rac red red rac rac rac red red red | 0,50 · 0,30 | ∞ (∞) | 13 | 0 |
| APRENDE_v s2 a11 | 19 | 6 | bot red red red cam cam cam red red red red red red red red red cam cam cam cam | 0,30 · 0,50 | ∞ (∞) | 17 | 0 |
| APRENDE_v s3 a10 | 9 | 0 | bot cam rac cam cam red cam cam red bot bot red red bot bot bot bot bot bot bot | 0,18 · 0,50 | ∞ (∞) | 10 | 0 |
| APRENDE_v s3 a11 | 12 | 6 | rac rac rac rac rac bot bot bot red red red red red red red red red cam cam cam | 0,39 · 0,50 | 8 (8) | 9 | 0 |
| APRENDE_p s1 a10 | 5 | 0 | bot red bot bot bot red red bot bot cam cam bot bot bot bot bot bot bot bot bot | 0,31 · 0,29 | 6 (∞) | 8 | 0 |
| APRENDE_p s1 a11 | 13 | 2 | red red red rac rac cam cam cam cam cam cam cam cam rac rac cam rac rac cam rac | 0,11 · 0,35 | ∞ (∞) | 13 | 0 |
| APRENDE_p s2 a10 | 18 | 6 | bot bot red red red red red red red cam red red red red red red red red red red | — · 0,50 | ∞ (∞) | 6 | 0 |
| APRENDE_p s2 a11 | 20 | 6 | red red red red red red red red red red red red cam cam cam cam cam cam cam cam | 0,33 · 0,50 | 4 (4) | 18 | 0 |
| APRENDE_p s3 a10 | 5 | 0 | rac rac rac red rac red cam cam red bot bot bot bot bot bot bot bot bot bot bot | 0,14 · 0,34 | 5 (5) | 14 | 0 |
| APRENDE_p s3 a11 | 17 | 6 | rac cam rac rac red cam cam cam cam cam cam cam cam cam red cam cam cam cam cam | 0,18 · — | 7 (7) | 16 | 0 |

Lo inútil manda por día (de 12 cierres): d1:2 d2:6 d3:4 d4:6 d5:6 d6:9 d7:10 d8:9 d9:10 d10:9 d11:9 d12:9 d13:10 d14:8 d15:7 d16:7 d17:6 d18:7 d19:8 d20:7. Manda por clase en los 240 cierres: botiquín 56, ración 35, red 85, camuflaje 64.

## Sección 2 · El rival arreglado (SIN) en partidas locales de verdad

`coworld play` funciona en local (motor `zero-sum-0.1.19`, variante competition, 16 contenedores nativos arm64 con nuestra imagen en todos los asientos: no hay imágenes
locales de los rivales de la liga, así que las 16 criaturas son nuestras, en 8 parejas; cuaderno vacío = día 1). Cambios de `azar_P7_47` frente a `azar_P7_41`: la forzada de ir
se cierra en la casilla (hacer_sitio si lo ofrece el cuerpo; `coger` puesto para el objeto forzado si el cuerpo no lo ofrece; «no cabe» a los 24 tics) y la moneda de usar solo
cuando el cuerpo ofrece `usar_*` (hp < máximo).

| partida local | imagen | vidas con diario | tics (media) | mueren | pruebas (huellas) por vida ± ee | por objeto (b · r · red · cam) | forzadas por vida | acaban (cogida + usada) | caducan · no cabe (de ellas, el objeto ya no estaba) | vías de la cogida (recoger · hacer_sitio · coger puesto) | ms mediana (media) · p95 máx | % sobre el tic · % bloqueados |
|---|---|---:|---:|---:|---|---|---:|---|---|---|---|---|
| APRENDE_p | `gemv-anima:P7_47_APRENDE_prudente` | 16 | 5.806 | 16 | 1,44 ± 0,52 | 10 · 9 · 3 · 1 | 0,00 | 0 de 0 (— %) | 0 · 0 (0) | 0 · 0 · 0 | 3,09 · 13,7 | 0,01 · 1,44 |
| APRENDE_v | `gemv-anima:P7_47_APRENDE_valiente` | 16 | 6.332 | 16 | 1,56 ± 0,45 | 14 · 8 · 2 · 1 | 0,00 | 0 de 0 (— %) | 0 · 0 (0) | 0 · 0 · 0 | 2,93 · 12,8 | 0,03 · 4,11 |
| SIN_e00019 | `gemv-anima:P7_47_SIN_e00019` | 16 | 6.418 | 16 | 0,12 ± 0,09 | 0 · 1 · 1 · 0 | 0,81 | 11 de 13 (85 %) | 0 · 2 (0) | 10 · 0 · 0 | 2,96 · 12,9 | 0,00 · 7,18 |
| SIN_e0023 | `gemv-anima:P7_47_SIN_e0023` | 16 | 7.248 | 16 | 1,44 ± 0,30 | 4 · 14 · 4 · 1 | 3,56 | 44 de 57 (77 %) | 1 · 12 (11) | 32 · 0 · 0 | 1,97 · 9,6 | 0,01 · 16,25 |

**SIN_e00019**: ε = 0.00019; 0,12 pruebas por vida frente a 1,50 de APRENDE con las piezas nuevas (media de las dos personalidades): -92 % (fuera del ±20 %); ε proporcional para igualar: 0.00228. Forzadas que acaban: 11 de 13 (85 %, < 90 %); de las 2 «no cabe», en 0 el objeto ya no estaba en la casilla al llegar (otro se lo llevó): sin esas, 11 de 13 (85 %). **SIN_e0023**: ε = 0.0023; 1,44 pruebas por vida frente a 1,50 de APRENDE con las piezas nuevas (media de las dos personalidades): -4 % (dentro del ±20 %); ε proporcional para igualar: 0.00240. Forzadas que acaban: 44 de 57 (77 %, < 90 %); de las 12 «no cabe», en 11 el objeto ya no estaba en la casilla al llegar (otro se lo llevó): sin esas, 44 de 46 (96 %). 

## Sección 3 · Coste de un campo (no se lanza: la regla de parada lo cierra)

4 variantes (APRENDE_v, APRENDE_p, SIN_v, SIN_p) × 20 días × 3 series = 240 partidas = 240 créditos; con SIN de una personalidad (como en P7-42), 180. Créditos de partida: 228 (12-oct). Sin campo por H1 y H2, el número queda para la mesa.

## Lectura

1. La intensidad en su escala hace lo que se le pidió con lo útil: la creencia del botiquín llega a 25 en 7 de 12 criaturas con mediana 8,5 pruebas (H3 pasa). La habituación no hace
   lo que se le pidió con lo inútil, porque su disparador («no hizo nada» = importancia exactamente 0) casi no ocurre con el filtro B1: 49 veces en 630 pruebas.
2. Aun con h en 0,2-0,5 en la mayoría de las criaturas, la red y el camuflaje siguen mandando (62 % de los cierres; 58 % en d15-20) y `coger` sigue ganando en el momento
   (55 %): la ignorancia de lo probado pocas veces manda, como en P7-40. Para que la habituación mordiera haría falta que «no hizo nada» fuera «importancia
   pequeña» (umbral) y no «cero exacto», o un factor por prueba sin efecto grande — decisiones de la mesa, no de este banco. Se propone, no se ejecuta.
3. El rival arreglado, en lazo cerrado local: con ε = 0.0023 SIN prueba 1,44 veces por vida frente a 1,50 de APRENDE (dentro del ±20 %); las forzadas que acaban son
   44 de 57 (77 %, no llega al 90 %), pero 11 de las que no acaban son objetos que otro se llevó antes de llegar (16 criaturas nuestras disputando el mismo botín): sin esas, el 96 %.
   Ya no caduca ninguna por el zurrón ni por el usar con la vida llena. Regla de parada: no hay campo; el rival queda listo para cuando la mesa decida.
