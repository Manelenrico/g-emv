# P7-39 · Último intento sobre lo inútil: la importancia mide solo el efecto del objeto

*10-oct-2026. Banco, coste cero: plataforma 0 créditos (acumulado del siete 710; disponibles el 10-oct, dato de Manel: 496 de 1.000, +71/día); consola 0 USD.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar; nada cambia en el campo. Sello `SELLO_P7_39.md` (commit
`a536ff6`, antes de calcular). Scripts: `efecto_P7_39.py` (= `f36ea927c5c083f597b5baa20b3d48a7`: el filtro de filas), `contrafactual_P7_38.py` (= `88ed3114f4bdbd5d550e18f9dffe5ddf`, con el mando
`GEMV_P7_38_CONTRA` para B1), `banco_P7_39.py` (`--cadena` → `P7_39_cadena.json`, `P7_39_res/cuaderno_B1_*.json`, `cuaderno_B2_*.json`; `--momentos` → `P7_39_momentos.json`),
`cuaderno_P7_39.py` → `P7_39_cuadernos_B1.json`, `_B2.json`, `escribe_informe_P7_39.py` (este informe; ninguna cifra a mano).*

## El sello, de una vez (B1 y B2)

| | criterio | B1 (sin contrafactual) | pasa | B2 (con contrafactual) | pasa |
|---|---|---|---|---|---|
| I1 | inútil ≤ 0,3 × botiquín (medianas, día 20) | 0,0085 frente a 0,0571 (botiquín 0,1903) | sí | 0,0000 frente a 0,0500 (botiquín 0,1667) | sí |
| I2 | «no hizo nada» ≤ 0,02 | 0,0056 (25 de 60 en 0) | sí | 0,0000 (38 de 60 en 0) | sí |
| I3 | lo inútil manda ≤ 40 de 80 y ≤ 20 % en d15-20 | 76 de 80; d15-20 24 de 24 | NO | 76 de 80; d15-20 24 de 24 | NO |
| I4 | `coger` lo inútil ≤ 24 de 71 | 60 de 71 (`ir_curioso` 11) | NO | 62 de 71 (`ir_curioso` 9) | NO |
| I5 | creencia útil ± 0,10 frente a P7-37 | máx 0,451 | NO | máx 0,682 | NO |

B1 pasa 2 de 5; B2 pasa 2 de 5. **Regla de parada**: ni B1 ni B2 pasan I1, I3 e I4 a la vez: no se ajusta más; se declara como hallazgo y el campo va con la mejor de las dos, **B1**
(criterio del sello: la que pase más de los cinco; a igualdad, la que deje lo inútil mandando menos cierres; a igualdad, B1).

## Sección 1 · La importancia sin el acto

Filtro (`efecto_P7_39`): del cambio de malestar salen `R-CURIOSIDAD`, `R-CURIOSIDAD-CUANTO`, `R-ACOPIO`, `R-CARENCIA`, `S-PROVISION` y `R-LLAMADA`. Cadenas honestas:
B1 956803 iguales · 55715 distintas; B2 956852 · 55666 (B2: 249 recuerdos tasados contra referencias, 13 con referencia de cualquier situación, 2 sin referencia).

| cosa | lectura | recuerdos | importancia P7-33 (cuartiles) | importancia nueva (cuartiles) | en 0 |
|---|---|---:|---|---|---:|
| botiquin | B1 | 67 | 0,1229 · 0,1903 · 0,3925 | 0,1229 · 0,1903 · 0,3925 | 0 |
| botiquin | B2 | 67 | 0,1229 · 0,1903 · 0,3925 | 0,0326 · 0,1667 · 0,3626 | 14 |
| racion | B1 | 121 | 0,0533 · 0,0902 · 0,1616 | 0,0533 · 0,0902 · 0,1616 | 0 |
| racion | B2 | 121 | 0,0533 · 0,0902 · 0,1619 | 0,0000 · 0,0000 · 0,1127 | 61 |
| red | B1 | 31 | 0,0000 · 0,0055 · 0,3323 | 0,0000 · 0,0055 · 0,3323 | 14 |
| red | B2 | 31 | 0,0000 · 0,0055 · 0,3323 | 0,0000 · 0,0000 · 0,2870 | 18 |
| camuflaje | B1 | 32 | 0,0000 · 0,0093 · 0,3061 | 0,0000 · 0,0093 · 0,3061 | 11 |
| camuflaje | B2 | 32 | 0,0000 · 0,0093 · 0,3061 | 0,0000 · 0,0000 · 0,2458 | 22 |

«No hizo nada» (red y camuflaje con |efecto cuerpo| ≤ 1): B1 25 de 60 en 0 (mediana 0,0056); B2 38 de 60 (mediana 0,0000). En P7-38 (sin el filtro) eran 24 de 60 (mediana 0,0589).

## Sección 2 · Quién manda, día a día

| criatura | lectura | ignorancia día 20: botiquín · ración · red · camuflaje | importancia esperada día 20: botiquín · ración · red · camuflaje | curiosidad día 20 | la clase que más llama, d1 → d20 | deja de mandar lo inútil el día |
|---|---|---|---|---|---|---|
| s1 a10 | B1 | 0,021 · 0,036 · 0,139 · 0,114 | 0,292 · 0,143 · 0,165 · 0,205 | 0,006 · 0,005 · 0,023 · 0,023 | N N N N C C C C C C C C C C C C C C C C | no llega |
| s1 a10 | B2 | 0,021 · 0,038 · 0,141 · 0,115 | 0,278 · 0,084 · 0,154 · 0,191 | 0,006 · 0,003 · 0,022 · 0,022 | N N N N C C C C C C C C C C C C C C C C | no llega |
| s1 a11 | B1 | 0,034 · 0,052 · 0,159 · 0,201 | 0,332 · 0,143 · 0,304 · 0,155 | 0,011 · 0,007 · 0,049 · 0,031 | N C C C C C C C C N N N N N N N N N N N | no llega |
| s1 a11 | B2 | 0,034 · 0,053 · 0,162 · 0,204 | 0,286 · 0,119 · 0,289 · 0,143 | 0,010 · 0,006 · 0,047 · 0,029 | N C C C C C C C C N N N N N N N N N N N | no llega |
| s2 a10 | B1 | 0,087 · 0,054 · 0,117 · 0,124 | 0,353 · 0,166 · 0,259 · 0,273 | 0,031 · 0,009 · 0,030 · 0,034 | N N N N N N N N C C N N N N C C N N C C | no llega |
| s2 a10 | B2 | 0,089 · 0,056 · 0,118 · 0,128 | 0,319 · 0,134 · 0,247 · 0,231 | 0,028 · 0,008 · 0,029 · 0,030 | N N N N N N N N C C N N N N N C N N N C | no llega |
| s2 a11 | B1 | 0,036 · 0,043 · 0,195 · 0,162 | 0,317 · 0,187 · 0,258 · 0,168 | 0,011 · 0,008 · 0,050 · 0,027 | R R R B C N N C C C C C C C C N N N N N | no llega |
| s2 a11 | B2 | 0,037 · 0,044 · 0,200 · 0,163 | 0,276 · 0,148 · 0,226 · 0,161 | 0,010 · 0,007 · 0,045 · 0,026 | R R R B C N N C C C C C C C C N N N N N | no llega |

(B botiquín, R ración, N red, C camuflaje.) Ignorancia al día 20: lo inútil 0,11-0,20 (B1), 0,12-0,20 (B2); lo útil 0,02-0,09 (B1), 0,02-0,09 (B2).

| criatura | creencia de la ración por día, P7-37 / B1 / B2 (días 1, 5, 10, 15, 20) |
|---|---|
| s1 a10 | d1: 6,0 / 6,0 / 6,0; d5: 5,8 / 5,8 / 5,8; d10: 5,7 / 5,7 / 5,7; d15: 8,4 / 8,4 / 8,3; d20: 11,2 / 11,2 / 11,1 |
| s1 a11 | d1: 3,0 / 3,0 / 3,0; d5: 8,9 / 8,9 / 8,9; d10: 13,1 / 13,1 / 13,1; d15: 13,2 / 13,2 / 13,2; d20: 13,0 / 12,9 / 12,9 |
| s2 a10 | d1: 13,5 / 13,4 / 13,4; d5: 13,8 / 13,8 / 13,7; d10: 13,7 / 13,6 / 13,6; d15: 13,4 / 13,3 / 13,3; d20: 12,9 / 12,9 / 12,9 |
| s2 a11 | d1: — / — / —; d5: 5,6 / 5,6 / 5,3; d10: 6,8 / 6,8 / 6,7; d15: 12,8 / 12,8 / 12,8; d20: 13,8 / 13,8 / 13,7 |

## Sección 3 · Los 71 momentos, en banco

B1: fidelidad 956803 · 55715; `coger` en 60 de 71; en las 63 aperturas, curiosidad mediana red 0,075, camuflaje 0,075, botiquín 0,029, ración 0,012; lo inútil es la clase que más llama en 123 de 134 momentos.
B2: fidelidad 956875 · 55643; `coger` en 62 de 71; curiosidad mediana red 0,075, camuflaje 0,073, botiquín 0,027, ración 0,010; lo inútil manda en 123 de 134.

## Lectura

**Hallazgo (regla de parada disparada).** El filtro hace lo que se le pidió: sin las filas de la curiosidad ni las del acto, la importancia de la red y del camuflaje se
queda en 0,0085 (B1) y 0,0000 (B2) de mediana frente a 0,190 / 0,167 del botiquín (I1 pasa en las dos), y «no hizo nada» vale
0,0056 / 0,0000 (I2 pasa). El cuerpo ya VE que la red no hace nada. Pero lo inútil sigue mandando la curiosidad en 76 de 80 cierres (las dos lecturas) y `coger`
sigue en 60 / 62 de 71, por el **neutro**: con el neutro contando como UN recuerdo de importancia 1 y 6-10 recuerdos de red o camuflaje de importancia ~0, la importancia
esperada de lo inútil el día 20 es 0,155-0,304 (B1; ≈ 1/(1+N)), la del botiquín 0,292-0,353 y la de la ración 0,143-0,187; multiplicadas por la ignorancia
(0,11-0,20 lo inútil frente a 0,02-0,09 lo útil), la curiosidad de la red y el camuflaje el día 20 es 0,023-0,050 y la del botiquín y la ración 0,005-0,031:
lo que nunca importó nada sigue llamando más que lo que cura, porque se ha probado menos veces y el neutro de nacimiento no se gasta. El producto ignorancia × importancia
esperada, con este neutro, no puede dar la vuelta: cuando la importancia de lo inútil es 0, su curiosidad es ignorancia / (1 + N), y la ignorancia de lo inútil (6-10 recuerdos)
siempre será mayor que la de lo útil (16-55 recuerdos). I5 no pasa en ninguna (máx 0,45 / 0,68; mediana de las diferencias 0,046 / 0,068) por la intensidad atada a la importancia, como en P7-38;
la creencia de la ración por día (tabla) se mueve en décimas. Según la regla de parada, no se ajusta más y el campo va con **B1** (2 de 5; a igualdad con la otra, la más simple).

Lo que queda dicho, no decidido: el neutro de importancia 1 es lo único que mantiene viva la curiosidad por lo inútil; una curiosidad que lo gastara con cada prueba sin fruto
(neutro de peso 1/N, o «no hizo nada» como evidencia negativa que resta) cerraría el círculo; es un mecanismo nuevo y no entra en este sello.
