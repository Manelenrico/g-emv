# El valle, congelado v5 (paper ocho)

*15-nov-2026. Etiqueta `valle-congelado-v5`. La base del ocho tras los arreglos de los prompts 128 a 133 (la cara y la voz de la base, probadas pieza a pieza): lo que juega el experimento v5, con su huella md5. Cambiar cualquiera de estos archivos rompe el sello. Sustituye a `CONGELADO_P8_v4.md` (11-nov-2026, RG61r).*

**La criatura elegida es RG68r** (decisión de Manel, prompt 134): es **M**, la base mínima del prompt 131, con su nombre nuevo. Es RG61r con dos interruptores encendidos, y nada más:
- **«ven, lo necesito» apagado** (`voz_sin_ven_v63`): esa llamada ni se emite ni se oye; las demás de la voz de antes (aquí estoy, aquí hay comida, la bestia) siguen igual;
- **la dormida sin voz** (`dormida_sin_voz_v67`): el mundo no deja salir la voz de una criatura que duerme ese turno.

Por la regla del prompt 133, ninguna pieza nueva del protolenguaje entró en la base (`informe_piezas_por_mundo_v1.md`).

Los md5 salen de `cantera/paper8/congelado_v5/md5_v5.py RG68r`. Comprobaciones (`salida/puerta_experimento_v5.json`):
- RG68r, con el código congelado, sale **idéntico** a su partida de M del taller (bestias que crían 1004, `valle_arreglos_v11/RG67r_M_…`);
- el tonto sale idéntico a su partida del experimento v2 (normal 30001).

Las clases salen de `banco_v7.VARS` (`congelado_v5/comprueba_clases_v5.py`: RG68r es igual a M, y cada compañera es la del v4 con esos mismos dos interruptores).

## El motor (no se toca)

| md5 | archivo |
|---|---|
| `1e511978c251130e95169ebf8443efa1` | `motor/model.py` |

## Las criaturas: RG68r, RG068r, S68, S068, P68 y RG61r (el mismo código, distintos interruptores)

| md5 | archivo |
|---|---|
| `e9869ae14088b3fb0032d8bf52e6b0e3` | `cantera/paper8/cuerpo_valle.py` |
| `7641232a0beddb962bd13d221ccb18c1` | `cantera/paper8/banco_v7.py` |
| `a38769fc437da2dfcb8bd4a326797c08` | `cantera/paper8/banco_cuerpo_valle.py` |
| `d361d60406f02edf060b9c258b4c7b60` | `cantera/paper8/config_cuerpo_valle.json` |
| `c97950bcd253297110b7319f546b9586` | `cantera/paper8/cultura_matorrales_medio.json` |
| `5da90dd00a76a947b32ab1e5d58bb7ea` | `cantera/paper8/cultura_hechos_v40.json` |
| `1958ace14490e2d1ec757572802719a0` | `cantera/paper8/cultura_hechos_v44.json` |
| `fbe005bf57be539849a6370f8dba15fb` | `cantera/paper8/cultura_hechos_v50.json` |
| `885bb75d79402184cd33b8b9742e42e5` | `cantera/paper8/banco_v6.json` |
| `0cfc9573dc4dbea283400dd6c1078221` | `cantera/paper7/cuaderno_P7.py` |
| `1dac5ed0f51b06fcb6b6a5aa31c3e1c5` | `cantera/paper7/descubre_P7.py` |
| `25926b765096e89116add8dcb3260ddd` | `cantera/paper7/miedo_P7_49.py` |
| `f8b85c6f61257b09ae3c1d961382f7e6` | `cantera/paper7/nace_P7_29.py` |
| `0083986bd7d2e51ee0295d6860e9e06a` | `cantera/paper7/nace_P7_23.py` |
| `a56fd98d6148b161a1c07cec9b6ebbfb` | `cantera/paper7/nace_P7_33.py` |
| `519e69e67026c880d49af76bc14eed30` | `cantera/paper7/recuerdo_P7_23.py` |
| `1fefeef2071af1f2adaf9ab116d0254f` | `cantera/paper7/filo_P7_40.py` |
| `b0efef883215d5046cbfc5db220d0f83` | `cantera/paper7/contrafactual_P7_38.py` |
| `4766e5a3b0afdc20b787d0b79da9fe31` | `cantera/paper7/pide_P7.py` |
| `f803f47c8ed0a8eaf3855d7e1dc7d457` | `cantera/paper5/curiosidad.py` |
| `67ba0003234939c349af12be5764a3b0` | `cantera/paper6/parte2.py` |
| `98c13d60167c80cc8334c965be75c640` | `paintball/alma/appraisal_zs_v42_exp.py` |
| `87745903992bdf0b4f5a18d13f9d4f5a` | `paintball/alma/appraisal_zs.py` |
| `8fa03547e3228ef9df4aa94c444f9252` | `paintball/alma/decisor_zs.py` |
| `80dabc2e78c7c36f0708a2d95e22262a` | `paintball/alma/parte.py` |
| `d0a3151d718e6b60d499e258c9dea9b1` | `planificador/planificador_v1.py` |
| `d41d8cd98f00b204e9800998ecf8427e` | `planificador/__init__.py` |

## El tonto y el recolector

| md5 | archivo |
|---|---|
| `01d196c61d500c6105703fa525dc83ec` | `valle/jugadores.py` |
| `3b226323a9896479a6e85f8fba02d2ac` | `valle/banco_base_v5.py` |

## El mundo y su config (con el árbol de fruta dulce y los mandos de estrés; se encienden en la partida)

| md5 | archivo |
|---|---|
| `15846835d8f118350f5bd37700a9244a` | `valle/mundo.py` |
| `603058a7c94f06adfddb030d2cdddcfd` | `valle/config_valle.json` |

## El experimento: lanzador y medidas del cierre (las del informe_cierre_v5)

| md5 | archivo |
|---|---|
| `3c249bccfe6311c12045e5014cab3e1a` | `cantera/paper8/lanzador.py` |
| `9674da51067607ecd745a5a219ba2694` | `cantera/paper8/pasada_v22.py` |
| `a3d0dd51c12e160b32b364094261ea17` | `cantera/paper8/pasada_v18.py` |
| `752255468e30219a7a768bb49eb7e3f5` | `cantera/paper8/taller_v34.py` |
| `679f5cec6ebcd53d7cdbab5b79608d82` | `cantera/paper8/taller_v35.py` |
| `23b7951e60f609c46d839efb09bace03` | `cantera/paper8/taller_v40.py` |
| `45ee3831acc80564fac59b38983fcd1e` | `cantera/paper8/taller_v43.py` |
| `495ab1cfd91f9701b51f1bd8c32b8ef4` | `cantera/paper8/taller_v44.py` |
| `3338628f0ad28f6b1e2bfb0a0bd2a5cc` | `cantera/paper8/taller_v45.py` |
| `d2ff1db9eb58d7c48a42d82c1165f6e3` | `cantera/paper8/taller_v52.py` |
| `93aca9a9b00a793ef6a282bef9dcc6e7` | `cantera/paper8/medida_v3/lanza_medida_v3.py` |
| `7e716ce9792e39d261d0b721ca83fb4b` | `cantera/paper8/medida_v3/rejuega_fotos.py` |
| `070a1f0fc3483d5ed4eb005353ad8a21` | `cantera/paper8/cierre_v5/lanza_cierre_v5.py` |
| `b2cdf8d7e7b326293fcdc68063f0debd` | `cantera/paper8/cierre_v5/tabla_cierre_v5.py` |
| `b1187e44087d1792dfc04abb62f868ab` | `cantera/paper8/cierre_v46.py` |
| `4d450845458a959b5c26480c723dcce5` | `cantera/paper8/cierre_v52.py` |
| `1ccbc12c0c25f31b210f7b1ff62f492d` | `cantera/paper8/diag_v47.py` |
| `82b806dca681a597cba98b672dd8d15b` | `cantera/paper8/diag_robos_v47.py` |
| `2caa5402d72f466be5b36545918c47df` | `cantera/paper8/verdad_noche_v49.py` |
| `f9982cf83cbc6a74de7896873db305a7` | `cantera/paper8/analiza_arbol_v50.py` |
| `63fb708530200dab4418f28a0ddecf86` | `cantera/paper8/analiza_v44.py` |
| `fdc32c3db744f001e69dedf5b9ecc1dd` | `cantera/paper8/cultura_hechos_v40.py` |
| `1f24406b303b81b3a9718ea2afd7c5df` | `cantera/paper8/cultura_hechos_v44.py` |
| `99bf2cf318a08c9e48f4f422b01be142` | `cantera/paper8/cultura_hechos_v50.py` |
| `d43b420727143605745b02f4a8abeaf3` | `cantera/paper8/cultura_valle.py` |
| `4c02ce9a885091d3ffdbfef361ce2e67` | `cantera/paper8/lanza_experimento_v3.py` |
| `3f3211ab756ee0ca7b035677c66725e1` | `cantera/paper8/lanza_experimento_v4.py` |
| `fef43a9835e3f4a0774505aa49a4c8c0` | `cantera/paper8/medida_v4/dormir_v4.py` |
| `b61ba0b3924b63d1227db699bea91c94` | `cantera/paper8/lanza_experimento_v5.py` |
| `ef52cfbc5fa4773110604bbd5de93364` | `cantera/paper8/evalua_experimento_v5.py` |

El mundo ha cambiado desde el v4 solo con interruptores apagados por defecto (los de los prompts 128 a 132: la cara, la voz de la base, la voz pieza a pieza y la dormida sin voz). RG61r, que juega como referencia, va con todos apagados. Cada taller comprobó con su puerta que la clase con los interruptores apagados sale idéntica a la de antes (prompts 128, 130, 131 y 132). El lanzador del experimento v5 (`lanza_experimento_v5.py`) y el evaluador (`evalua_experimento_v5.py`) se sellan con el congelado.

## Qué hace cada clase

**RG68r** (`banco_v7.VARS["RG68r"]`) es RG61r (ver `CONGELADO_P8_v4.md`) con `voz_sin_ven_v63` y `dormida_sin_voz_v67`.

**RG068r, S68, S068 y P68:** RG061r, S61, S061 y P61 del v4, con esos mismos dos interruptores. RG068r decide solo por lo que pierde; S68 y S068 usan el valorador de sumas; P68, el de posición.

**RG61r:** la base del v4, sin cambiar, **como referencia**.

**El tonto y el recolector:** los mismos de los congelados v2 a v4 (`valle/jugadores.py`, sin cambios).

## Los cinco mundos y sus mandos

Igual que en los congelados v2 a v4 (`CONGELADO_P8_v4.md`).

## Los números elegidos

Los mismos del congelado v4. Los dos interruptores de RG68r **no añaden ningún número**.

## Los fallos de saber conocidos (sin arreglar)

Los dieciséis del v4 (`CONGELADO_P8_v4.md`), y además:

17. **El hambre media sube 0,9 sobre 100 frente a RG61r** (con la medida corregida: +0,93 [+0,44, +1,43], prompts 131 y 132). Los días con hambre de más de 60 no suben fuera del ruido. No sabemos por qué; no viene de que vivan más criaturas.
18. **Siguen los bucles de regalos entre hermanas hartas:** dos hermanas sin hambre se pasan la comida turno a turno (en el taller de M, la racha más larga fue de 9; con la alarma, de 13).
19. **Probado y apagado:** la cara, la voz nueva (alarma, petición, contacto), aprender de la cara y el «para». Están en el código, apagados (`cara_v64`, `voz_v64`, `aprender_cara_v64`, `para_v64`, `cara_dar_v65`, `ya_tiene_v67`, `voz_piezas_v68`). Ninguna pieza entró en la base por las reglas fijadas: `informe_arreglos_v9.md`, `informe_dar_v1.md`, `informe_arreglos_v10.md`, `informe_arreglos_v11.md`, `informe_arreglos_v12.md` e `informe_piezas_por_mundo_v1.md`.
20. **Sin «ven, lo necesito», no hay forma de pedir ayuda con la voz.** La hermana solo sabe que la otra está flaca o herida si la ve.

## Lo que se sabe de RG68r (M) antes del experimento

Del taller del prompt 131 (`informe_arreglos_v11.md`; 5 mundos × semillas 1001–1020, frente a RG61r en las mismas semillas):
- **Vive más:** +0,25 [+0,09, +0,42].
- **Es más feliz:** aldea +0,101, peor parada +0,135.
- **Mueren menos de hambre:** −0,24. Los días con hambre de más de 60 bajan −0,014.
- **La mitad de empujones** (−103 por partida) y menos golpes.
- **Duerme más dentro de casa** (+8,5 puntos) y menos noches fuera (7,4 frente a 11,7).
- **Despierta 0,19 veces por noche** (RG61r, 33,7).
- **Sin muertes por golpe;** la racha más larga es de 9.
- **El hambre media sube** +0,8 (+0,93 con la medida corregida).

## Las semillas reservadas para el experimento

**30121–30160** (40 semillas). En el valle no se han usado nunca: ninguna partida del disco las lleva (`congelado_v5/semillas_v5.md`). En el repositorio solo sale la 30121, en el propio lanzador y en el evaluador del v5. Las 30001–30120 son de los experimentos v2, v3 y v4.
