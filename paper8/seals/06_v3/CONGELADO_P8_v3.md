# El valle, congelado v3 (paper ocho)

*9-nov-2026. Etiqueta `valle-congelado-v3`. La base del ocho tras los arreglos de los prompts 103-112: lo que juega el experimento, con su huella md5. Cambiar cualquiera de estos archivos rompe el sello. Sustituye a `CONGELADO_P8_v2.md` (7-nov-2026, RG50r).*

**La criatura elegida es RG58r** (decisión de Manel, tomada antes de ver los resultados del prompt 112): RG60r todavía tenía un bucle de comida, y RG58r no tiene bucles. Apunte obligado: **en bestias que crían, RG58r vive algo menos que RG55r** (−0,62 [−1,19, −0,05] por partida, con 21 semillas emparejadas; `informe_medicina_v1.md`).

Los md5 salen de `cantera/paper8/congelado_v3d/md5_v3d.py RG58r`. RG58r sale idéntico, con el código congelado, a sus partidas del prompt 110 (`congelado_v3d/rg58r_igual.json`).

## El motor (no se toca)

| md5 | archivo |
|---|---|
| `1e511978c251130e95169ebf8443efa1` | `motor/model.py` |

## Las criaturas: RG58r, RG058r, S58, S058 y P58 (el mismo código, distintos interruptores)

| md5 | archivo |
|---|---|
| `0ea3714b7d89330321a1021cc00bee91` | `cantera/paper8/cuerpo_valle.py` |
| `a85da7acadf60ebdf2b0b5aff779add1` | `cantera/paper8/banco_v7.py` |
| `7d880d6f53a90c7dbcb5d452ff9741f8` | `cantera/paper8/banco_cuerpo_valle.py` |
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
| `304f984d6c8cd5ab6ecaad26b08b7c66` | `valle/mundo.py` |
| `603058a7c94f06adfddb030d2cdddcfd` | `valle/config_valle.json` |

Son los mismos que en el congelado v2: el mundo no ha cambiado.

## El experimento: lanzador y medidas del cierre (las del `informe_cierre_v5`)

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

El lanzador del experimento v3 se escribirá con las predicciones selladas, como en el v2, y se sellará con ellas.

## Qué hace cada clase

**RG58r** (`banco_v7.VARS["RG58r"]`) es RG50r (ver `CONGELADO_P8_v2.md`: la regla general con ganancias, el motor del siete, el cuerpo y el mundo, la comida y los sitios, el radar de las suyas, el duelo, la bestia, los robos, las noches y los empates) **con estos cambios:**
- **El gusto de la fruta dulce se aprende** (`dulce_v51`): al comer, el gusto se apunta sea cual sea el origen de la comida.
- **Ir a casa** (`casa_v51`): el destino es un sitio libre de dentro, nunca la puerta. El paso rodea a quien está delante (solo al ir a casa), y nadie se duerme en una puerta, salvo agotada.
- **Dar** (`dar_v52/53/54`, `gesto_comida_v56`):
  - **lo que gana quien da:** el gesto (media comida sencilla del bosque, solo al dar comida) y lo que el regalo hace por la otra (su alivio, solo si lo necesita, y su gusto). Las dos partes van pesadas por lo que vale la otra: su familia (hermana 0,9864; vecina 0,3675) × su radar entero ahora / al nacer, de modo que los robos la bajan y el cuidado la sube;
  - **el alivio de la otra** se apunta como vínculo (0,1 · 0,1 · 0,8);
  - **lo que pierde quien da:** lo de siempre, más lo que le costará al cuerpo quedarse sin su última comida (F-ÚLTIMA-COMIDA, según su hambre) **o sin su última medicina** (F-SIN-MEDICINA, según su herida; `cuesta_medicina_v57`).
- **Devolver no es un gesto** (`devolver_v57`, `devolver_v58`): si lo que voy a darle me lo dio ella hace menos de 40 turnos, o ese mismo turno, a la vez, la foto no lleva ni gesto, ni alivio, ni gusto. Quién me dio qué lo deduzco de mi bolsa y de lo que veo en la de las pegadas.
- **Sin la regla `tope_dar`** (`tope_dar_off`): dar lo último con hambre lo frena la foto, no una orden.
- **En el código, apagados:** `fractal_v51`, `devolver_solo_gesto_v59`, `devolver_necesidad_v60` (las de RG59r y RG60r) e `imagina_v45` (la pieza I).

**RG058r:** RG58r sin ganancias (`rg_ganancias=False`), sin vivir bien (`escala_v6`) ni lo sentido (`sentir`). Decide solo por lo que pierde, con los mismos arreglos; el gesto, que es una ganancia, no entra.

**S58 y S058:** RG58r y RG058r con el valorador de sumas (`sumas_v29`) en vez del motor del siete.

**P58:** RG58r con el valorador de posición (`posicion_v30`).

**El tonto y el recolector:** los mismos del congelado v2 (`valle/jugadores.py`, sin cambios).
- **El tonto:** una hermana trabaja el huerto y la otra busca en el bosque; come con hambre de 40; deja en el almacén lo que le sobra; al anochecer, o si ve la bestia, a casa y a dormir; no da, no empuja, no golpea, no llama.
- **El recolector:** conoce los matorrales; coge, guarda en el almacén y va a la fuente con fruto más cercana (también el árbol dulce); al anochecer, a casa; nunca trabaja el huerto.

## Los cinco mundos y sus mandos

Igual que en el congelado v2. Todos con:
- el mando de la bestia medio: baja de noche la mitad de las veces, al huerto;
- echar y matar a la bestia encendidos (`bestia.pieza_g`);
- **el árbol de fruta dulce encendido** (`arbol_dulce.activo`, que se enciende en la partida): dos sitios a 40–43 pasos de la casa más cercana, cada uno con 2 o 3 apariciones de 3 o 4 días y 20 frutas. Al atardecer la bestia pasa por el árbol.

Las criaturas RG juegan con los sabores (`objetos.sabores`), y el mundo les enseña los empujones vistos y lo que hizo cada cuerpo.

| mundo | qué cambia (`lanzador.mundo_de`) |
|---|---|
| abundancia | las épocas de los matorrales a ×1,3 todo el rato (también el huerto) |
| normal | sin épocas |
| sequía | épocas de 5 días en ciclo: abundancia ×1,3, normal, escasez ×0,7, normal (la escasez, los días 10–14 y 30–34); también el huerto |
| sequía dura | el mismo ciclo ×0,7 (0,91; 0,7; 0,49; 0,7) toda la partida (`estres.sequia_dura`) |
| bestias que crían | la bestia baja también de día (`bestia.de_dia`) y nace otra a los 20 días, hasta dos (`estres.bestias_crian`) |

## Los números elegidos

| número | valor | dónde | de quién |
|---|---|---|---|
| el gesto | media comida sencilla del bosque: 0,5 × (dh(60) − dh(25)) × el peso de la otra; solo al dar comida | `config_cuerpo_valle.json → dar_v53.gesto_parte`; `sabores_v40.hambre_ref` | Manel (prompts 104, 105 y 108) |
| devolver | lo que me dio hace menos de **40** turnos, o ese mismo turno | `dar_v57.devolver_turnos` | Manel (prompts 109 y 110) |
| el hambre supuesta de la otra | **80** si está flaca, **30** si no | `banda_de_la_hermana.flaca_hambre_estimada`; `gusto_v49.no_flaca_hambre_estimada` | el 30, propuesto por mí (prompt 95) |
| el gusto con la tripa llena | **un cuarto**; con mucha hambre, entero (desde 60); en medio, en proporción | `gusto_v49.lleno` | Manel (prompt 95) |
| el reparto de las filas | **0,8 · 0,1 · 0,1** (la tabla del siete); el gesto y el alivio de la otra, 0,1 · 0,1 · 0,8, leído de F-HAMBRE | `appraisal_zs_v42_exp` | el siete; Manel para el gesto y el alivio |
| el peso de la otra | familia: hermana **0,9864**, vecina **0,3675**, × radar entero ahora / al nacer | `radar_v39`; al nacer, `radar_v34` (hermana_vinculo 0,5; vecina 0,25 de la hermana) | los pesos de RG32r (prompt 84); el 0,25, provisional (prompt 79) |
| el gusto del huerto | **media** comida a media hambre | `sabores_v40.parte` | propuesto por mí (prompt 85) |
| el gusto dulce | **el doble** que el del huerto | `arbol_v50.dulce_veces_huerto` | Manel (prompt 96) |
| el dolor del hambre | hasta **el doble** con el hambre al máximo, por encima de 60 | `hambre_dolor.al_maximo` | Manel (prompt 36) |
| el compromiso | se suelta con hambre > **60**, cansancio > **70**, o **3** turnos sin avanzar | `compromiso` | el 60, el umbral de la llamada; el 70 y los 3, propuestos por mí (prompt 22) |

## Los fallos de saber conocidos (sin arreglar)

1. **La foto no llega al árbol y vuelta.** Imagina como mucho 44 pasos (una mirada), y el árbol está a 40–52.
2. **El árbol se recuerda como un matorral:** «hay fruto o no», no cuántas frutas, ni que se va.
3. **La vida de la bestia no se ve:** al imaginar matarla, supone que tiene la vida entera.
4. **Empujar a la bestia:** cuenta a las suyas pegadas como si empujaran con ella.
5. **La bolsa:** su tamaño (6) está escrito en la foto, no es una regla pública.
6. **El hambre de otra:** solo ve si está flaca; le supone 80 o 30. Esos números deciden el alivio y el gusto que imagina al darle. De su vida, solo ve el nivel.
7. **Las costumbres de la hermana** (la pieza I, apagada): la ve más quieta de lo que está.
8. **Los hechos que no conoce:** la cría de las bestias y las épocas. Los del árbol no dicen ni dónde ni cuándo.
9. **Las épocas no se anuncian:** solo ve que hay menos fruto.
10. **Lo que cree de dormir fuera** incluye toda la vida perdida dormida, también la del hambre.
11. **Quedan empujones a quien no lleva nada:** el 2–6 %.
12. **No sabe que de noche dormirá de un tirón:** el mundo cambia lo que elija por dormir, y ella sigue imaginando y eligiendo cosas que no hará.
13. **Llevar comida o medicina no vale nada para el cuerpo en la foto,** salvo al dar la última. Dejarla, perderla en un robo o guardarla solo cuentan en recursos.
14. **El paso solo rodea al ir a casa:** en los demás viajes, quien está delante corta el camino ese turno.
15. **Quién me dio algo, lo deduzco de lo que veo:** de mi bolsa y de las bolsas de las pegadas. Con varias pegadas a la vez, o si no veo su bolsa, me puedo equivocar.

**Arreglados desde el v2:**
- el gusto dulce no se aprendía;
- la puerta (ir a casa llevaba a ella, y una dormida en ella dejaba fuera a la otra);
- el coste para el cuerpo de la última comida y de la última medicina;
- los bucles de dar (devolver lo que me acaban de dar).

## Lo que se sabe de RG58r antes del experimento

- **Sin bucles de dar** en 50 partidas de prueba (10 semillas por mundo): la racha de ida y vuelta más larga es de 5 (comida) y de 2 (medicina). Una herida se cura antes de dar la medicina, salvo que la otra esté peor (`medicina_v1/comprueba_v58.md`).
- **En bestias que crían vive algo menos que RG55r:** −0,62 [−1,19, −0,05] por partida, con 21 semillas emparejadas, por más muertes por la bestia.
  - **No es la medicina:** en las dos clases, el 97 % del tiempo herido no hay medicina a mano, y las curas con medicina son las mismas.
  - **No lo he podido atribuir a nada;** RG59r, con el alivio al devolver, vivía como RG55r, pero tenía bucles (`informe_medicina_v1.md`, `informe_congelado_v3c.md`).

## Las semillas reservadas para el experimento

**30041–30080** (40 semillas). Nunca se han usado: ni en el disco del experimento, ni en el repositorio como semilla (`congelado_v3/semillas_v3.md`, prompt 108). Las 30001–30040 son del experimento v2.
