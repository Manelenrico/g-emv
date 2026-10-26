# P7-49a · Carácter de verdad: el mando de miedo, por fuera (sin copiar ni tocar model.py); identidad y viabilidad local

*12-oct-2026. Solo local, 0 créditos (saldo **228**, dato de Manel 12-oct 06:47); consola 0 $. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`: ni se copia ni se toca; la appraisal congelada
tampoco. Sin sello (P7-49 en espera). Piezas nuevas: `miedo_P7_49.py` = `25926b765096e89116add8dcb3260ddd`, `campo_P7_49.py`, `policy_pareja_P7_49.py`, `Dockerfile.pareja_P7_49`; `banco_P7_49.py` →
`P7_49_identidad.json`; `local49_P7_49.py` → `P7_49_local.json`; `escribe_informe_P7_49a.py` (este informe; ninguna cifra a mano).*

## Sección 1 · Dónde vive el miedo y el mando

`model.py` no tiene miedo: tiene seis fuerzas y una distancia. Lo que llega como f⁻ (nF, nR, nS) lo construye la appraisal congelada sumando filas por `REPARTO`; el miedo y el daño
sentido llegan ya mezclados. Decisión de Manel: el miedo es ANTICIPAR una pérdida que aún no ha ocurrido, en cualquiera de las tres dimensiones. **El mando MIEDO (un solo número)
multiplica la M de esas filas**, enganchado por fuera a `A.filas` después de las piezas del siete (así escala lo que el decisor fotografía en cada candidato). La cautela del probar
lleva el mismo factor: cautela_eff = 1 − MIEDO × (1 − cautela) (MIEDO = 0,5 da la valiente de P7-42, (1 + c) / 2). Pareja: MIEDO_V al asiento par, MIEDO_P al impar.

| anticipa una pérdida (× MIEDO) | motivo |
|---|---|
| F-ANTICIPACION | daño previsto (anillo, hostiles): aún no golpea |
| F-4-ALCANCE | rival con arma al alcance: puede golpear, no ha golpeado |
| F-REENCUENTRO | miedo con memoria: un agresor recordado, armado, que se acerca |
| MIEDO_APRENDIDO | miedo aprendido (paper 4): descuento del futuro sobre el hostil |
| F-HERMANO-AMENAZA | la hermana amenazada: aún no le pegan |
| S-8-EXPOSICION | a la vista / campo abierto: anticipa el ataque |
| S-7-AGRESOR | presión del agresor activo para evitar el siguiente golpe (mesa: dentro) |
| R-ACOPIO | la mochila sin botiquín: anticipa una herida sin cura (mesa: dentro) |
| S-COMPANIA | crece con la distancia a la hermana mientras aún se la localiza: anticipa la separación (aclaración de Manel: la valiente es más independiente) |

| intacta | motivo |
|---|---|
| F-DANO, F-HERMANO-GOLPE, R-HERMANO-FALTA, R-CARENCIA, S-SOLEDAD, S-DANO-PAREJA, S-MUERTE-PAREJA, S-HERIDO, S-PROVISION | pérdida presente (ya ocurre o ya ocurrió) |
| **S-VINCULO, S-VIDA-AJENA** | **decisión de Manel: son el freno a matar, es decir, cuidado, no miedo: la valiente y la prudente cuidan igual** |
| R-LLAMADA; R-CURIOSIDAD, R-CURIOSIDAD-CUANTO | atracción y curiosidad: no son pérdida |

En código: `FILAS_MIEDO = ("F-ANTICIPACION", "F-4-ALCANCE", "F-REENCUENTRO", "MIEDO_APRENDIDO", "F-HERMANO-AMENAZA", "S-8-EXPOSICION", "S-7-AGRESOR", "R-ACOPIO", "S-COMPANIA")`.

## Sección 2 · Identidad con MIEDO = 1 (decisión a decisión)

| vida replicada (lazo abierto, cuaderno real del día anterior) | asiento | decisiones | MIEDO = 1: distintas | 0,5 / 1,5: distintas | 0,7 / 1,3: distintas | p95 ms (MIEDO = 1) |
|---|---:|---:|---:|---:|---:|---:|
| P741_s1_d8_APRENDE_v_44139128 | 10 | 12157 | 0 | 846 | 560 | 5,1 |
| P741_s2_d13_APRENDE_p_44139128 | 11 | 14520 | 0 | 2295 | 677 | 5,9 |
| P741_s3_d17_APRENDE_v_44034399 | 11 | 1552 | 0 | 318 | 121 | 4,7 |

Referencia = la misma composición sin el mando (hermanas solas, sin carácter por paridad: con el mando el carácter es solo el mando). **28229 decisiones en 3 vidas completas, 0 distintas: PASA.**
Con 0,5 / 1,5 y 0,7 / 1,3 las decisiones sí cambian (control del enganche). `model.py` md5 sin cambio.

## Sección 3 · Viabilidad en local (lazo cerrado; hermanas SOLAS para medir solo el carácter)

Tres partidas con nuestra imagen en los 16 asientos (8 parejas valiente/prudente): 1 / 1 (referencia, sin carácter), 0,5 / 1,5 y 0,7 / 1,3. «Quieta» = tics vivos sin haber cambiado de casilla en los últimos 48 tics (2 s; un paso tarda 3-5 tics); «camuflada» = tics con el camuflaje puesto. El mundo local es el de P7-47/48: 16 criaturas nuestras, todas mueren antes del final.

| pareja (MIEDO valiente / prudente) | hermana | MIEDO | vidas | tics (media · mediana) | mueren | quieta (% tics) | camuflada (% tics) | pruebas por vida | ms mediana · p95 máx | % bloqueados |
|---|---|---:|---:|---|---:|---:|---:|---:|---|---:|
| 1,0 / 1,0 | valiente | 1,00 | 8 | 6.177 · 6.528 | 8 | 1,8 | 0,0 | 3,12 | 3,17 · 12,6 | 7,7 |
| 1,0 / 1,0 | prudente | 1,00 | 8 | 6.225 · 7.260 | 8 | 1,6 | 12,3 | 1,50 | 2,82 · 13,8 | 9,9 |
| 0,7 / 1,3 | valiente | 0,70 | 8 | 5.928 · 6.540 | 8 | 5,6 | 0,0 | 1,75 | 3,52 · 12,2 | 6,7 |
| 0,7 / 1,3 | prudente | 1,30 | 8 | 6.351 · 7.296 | 8 | 4,9 | 12,2 | 2,50 | 2,85 · 11,9 | 7,8 |
| 0,5 / 1,5 | valiente | 0,50 | 8 | 6.138 · 7.308 | 8 | 5,0 | 12,2 | 1,00 | 3,38 · 14,6 | 0,9 |
| 0,5 / 1,5 | prudente | 1,50 | 8 | 6.177 · 6.504 | 8 | 3,2 | 0,0 | 1,62 | 2,88 · 12,5 | 4,2 |

Criterio de viabilidad (enunciado): no morir el doble de rápido que MIEDO = 1 (tics medios ≥ la mitad de la referencia: 6.201 tics) y no quedarse quieta la mayor parte del tiempo (< 50 %).
Resultado: 0,7 / 1,3: valiente viable, prudente viable; 0,5 / 1,5: valiente viable, prudente viable.
**Propuesta: MIEDO 0,5 / 1,5 (la pareja más separada en la que las dos siguen viables).** Una partida local por pareja (8 vidas por hermana): la propuesta es para que la
mesa la lleve al sello de P7-49, no un resultado. La «camuflada» al 12 % es en cada partida UNA sola vida que lleva el camuflaje puesto casi entera (m1_1: asiento 13 98 %, m07_13: asiento 7 98 %, m05_15: asiento 12 98 %): no es
un rasgo del miedo. Diferencias entre hermanas en duración, pruebas y quietud: dentro de lo que 8 vidas pueden decir; el mando no las deja ni quietas ni muertas antes.
