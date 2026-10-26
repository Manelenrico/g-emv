# P7-49 · Sello y plan del campo del capítulo 4: potencia y coste (NADA lanzado)

*12-oct-2026. Sello `SELLO_P7_49.md` (commit `d73219f`, antes de calcular). Plataforma 0 créditos hoy; saldo 228 (dato de Manel, 12-oct 06:47; no legible por la API; +71 al día). Consola 0 $.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Potencia: `potencia_P7_49.py` → `P7_49_potencia.json` sobre `P7_42_datos.json` (campo P7-45, APRENDE: 12 criaturas, 6 parejas-serie, sin
compartir); `escribe_informe_P7_49.py` (este informe; ninguna cifra a mano).*

## Sección 1 · El sello (resumen; el texto que manda es `SELLO_P7_49.md`)

Brazos COMPARTE / SOLAS, OJOS=1 en los dos; criatura P7-40 + escala (sin habituación); pareja valiente (asiento 10, MIEDO 0,5) / prudente (11, MIEDO 1,5) con `miedo_P7_49`; cuatro
objetos desconocidos; cadena de 20 días; semillas de P7-41 (series 4+: rotación de 5 más por serie). Humo 3 partidas; guarda, equidad y tope como en P7-43e. Predicciones a 3 veces
el ruido: S1 (la hermana que menos prueba por sí misma, decidida en SOLAS, cree más en el botiquín en COMPARTE: área bajo la curva d1-20), S2 (las hermanas de COMPARTE se
parecen más en lo que creen: d11-20, cuatro objetos), S3 (en COMPARTE va menos a red y camuflaje). Vigilancia sin predicción: quién prueba más, contagio de errores, puesto medio.

## Sección 2 · Potencia con el ruido de P7-45

Una observación por serie y brazo. Series necesarias por brazo para que un efecto del 30 % (o del 50 %) de la media sea ≥ 3 errores típicos: n ≥ 18 × sd² / efecto²; coste = 2 brazos
× 20 días × n + 3 de humo.

| predicción | medida | observaciones de P7-45 | media | desviación típica (ruido) | series por brazo para un 30 % (coste) | para un 50 % (coste) | efecto mínimo a 3 ee con 2 · 3 · 5 · 10 series |
|---|---|---:|---:|---:|---|---|---|
| S1 | área bajo la curva de la creencia del botiquín, d1-20 (por criatura) | 12 | 363,4 | 132,3 | 27 (1083 créditos; 13 días de recarga) | 10 (403; 3 días) | 109 · 89 · 69 · 49 % |
| S2 | parecido entre hermanas, d11-20, cuatro objetos (por pareja-serie) | 6 | 2,845 | 1,204 | 36 (1443 créditos; 18 días de recarga) | 13 (523; 5 días) | 127 · 104 · 80 · 57 % |
| S3 | fracción de pruebas a red + camuflaje, las dos juntas (por pareja-serie) | 6 | 0,228 | 0,018 | 2 (83 créditos; 0 días de recarga) | 1 (43; 0 días) | 24 · 20 · 15 · 11 % |

Pruebas por criatura en P7-45 (la hermana que menos prueba, por serie): APRENDE_v s1 a10 73, APRENDE_v s1 a11 64, APRENDE_v s2 a10 61, APRENDE_v s2 a11 72, APRENDE_v s3 a10 74, APRENDE_v s3 a11 67, APRENDE_p s1 a10 72, APRENDE_p s1 a11 60, APRENDE_p s2 a10 69, APRENDE_p s2 a11 80, APRENDE_p s3 a10 87, APRENDE_p s3 a11 81.

## Sección 3 · Lo que cabe y lo que tiene potencia

- Con el saldo de 228 caben hoy hasta **5 series** (203 créditos); 3 series son 123 y 2 series 83.
- Con 3 series (o 5) **solo S3 tiene potencia** (efecto mínimo visible 20 % de la media: un 30 % se ve con 2 series). **S1 y S2 no la tienen**: con 3 series solo se vería un efecto
  del 89 % (S1) o del 104 % (S2) de la media (con 5 series, 69 % y 80 %); un 50 % pide 10 series (S1; 403 créditos, 3 días de recarga) y 13 (S2; 523, 5 días); un 30 %,
  27 y 36 series (1083 y 1443 créditos: 13 y 18 días).
- **Propuesta**: (a) si la mesa quiere jugar ya, **3 series** (123 créditos, caben hoy): S3 con potencia; S1 y S2 solo si el efecto es enorme (≥ 90-100 % de la media), y se declara así en
  el sello antes de jugar. (b) Si lo que importa es S1 (que la que menos prueba aprenda de la otra), esperar y jugar **10 series** (403 créditos, 3 días de recarga desde 228) para un efecto del 50 %.
  Dicho claro: con lo que cabe hoy (5 series como mucho), S1 y S2 no tienen potencia para un 30 % ni para un 50 %.
- El ruido de S1 es grande porque en P7-45 cada criatura llega o no llega a creer en el botiquín (área 157-598); si compartir redujera esa dispersión, la potencia real sería mayor que la
  calculada aquí (el ruido de P7-45 es el de hermanas que no se cuentan nada).
