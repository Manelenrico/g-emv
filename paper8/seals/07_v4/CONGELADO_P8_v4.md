# El valle, congelado v4 (paper ocho)

*11-nov-2026. Etiqueta `valle-congelado-v4`. La base del ocho tras los arreglos de los prompts 115 y 116 («que robar deje huella en el vínculo»): lo que juega el experimento v4, con su huella md5. Cambiar cualquiera de estos archivos rompe el sello. Sustituye a `CONGELADO_P8_v3.md` (9-nov-2026, RG58r).*

**La criatura elegida es RG61r** (decisión de Manel, prompt 117). Cumplía la regla fijada antes del taller: ninguna muerte por golpe, ningún bucle nuevo de más de 10 y no vive peor que RG58r fuera del ruido (`informe_arreglos_v8.md`).

Los md5 salen de `cantera/paper8/congelado_v4/md5_v4.py RG61r`. Comprobaciones:
- RG58r, con el código congelado y los interruptores nuevos apagados, sale idéntico al congelado v3 (`arreglos_v8/puerta_v13b.json`).
- RG61r sale idéntico a su partida del taller (`salida/puerta_experimento_v4.json`).

Los tres interruptores nuevos (`robo_regalo_v61`, `robo_trato_v61`, `quitar_espejo_v61`) están en `cuerpo_valle.py`, apagados por defecto. Las clases que los encienden están en `banco_v7.py`.

## El motor (no se toca)

| md5 | archivo |
|---|---|
| `1e511978c251130e95169ebf8443efa1` | `motor/model.py` |

## Las criaturas: RG61r, RG061r, S61, S061 y P61 (el mismo código, distintos interruptores)

| md5 | archivo |
|---|---|
| `760bc2af4b70c8f4a559aed0ae807af7` | `cantera/paper8/cuerpo_valle.py` |
| `a2087f1e969b9295b02cf24dd021266d` | `cantera/paper8/banco_v7.py` |
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

El mundo y su config son los mismos que en los congelados v2 y v3: el mundo no ha cambiado. El lanzador del experimento v4 (`lanza_experimento_v4.py`) y la medida de dormir arreglada (`medida_v4/dormir_v4.py`) se sellan con el congelado.

## Qué hace cada clase

**RG61r** (`banco_v7.VARS["RG61r"]`) es RG58r (ver `CONGELADO_P8_v3.md`) **con estos tres cambios** (prompts 115 y 116):
- **Ganar un empujón nunca es un regalo** (`robo_regalo_v61`): si la criatura acaba de ganar un empujón contra la otra (empujara ella o la empujaran a ella; al robar o al recuperar), su bolsa crecida no se apunta como un regalo de la otra. Un regalo es solo lo que la otra da con la acción de dar.
- **El robo baja el trato de la ladrona** (`robo_trato_v61`): en la mirada en que le roban comida, el apunte del trato de la ladrona baja un cuarto, lo mismo que sube con un regalo: min(1, tiempo a la vista + ¼ × (cuidados − robos)). Las que lo ven restan ese cuarto multiplicado por su vínculo con la robada, la proporción con la que ya aprenden un robo visto. Se recupera con el trato de las miradas siguientes; no hay nada para el perdón.
- **Quitar comida cuenta la falta que deja en el vínculo** (`quitar_espejo_v61`): el espejo de dar que ya había (R-HERMANO-FALTA, en recursos, con peso familia) pasa a una fila de vínculo, S-QUITAR. Lleva el reparto de G-ALIVIO (0,1 · 0,1 · 0,8) y el peso del alivio al dar: peso_dar × lo que le baja el hambre la comida quitada × lo aprendido de dar. La condición es la de antes: que la otra se vea flaca, herida o de duelo. S-DANAR se queda como estaba.

**RG061r:** RG61r sin ganancias (`rg_ganancias=False`), sin vivir bien (`escala_v6`) ni lo sentido (`sentir`), con los mismos tres cambios. Decide solo por lo que pierde.

**S61 y S061:** RG61r y RG061r con el valorador de sumas (`sumas_v29`) en vez del motor del siete.

**P61:** RG61r con el valorador de posición (`posicion_v30`).

**El tonto y el recolector:** los mismos de los congelados v2 y v3 (`valle/jugadores.py`, sin cambios).
- **El tonto:** una hermana trabaja el huerto y la otra busca en el bosque; come con hambre de 40; deja en el almacén lo que le sobra; al anochecer, o si ve la bestia, a casa y a dormir; no da, no empuja, no golpea, no llama.
- **El recolector:** conoce los matorrales; coge, guarda en el almacén y va a la fuente con fruto más cercana (también el árbol dulce); al anochecer, a casa; nunca trabaja el huerto.

## Los cinco mundos y sus mandos

Igual que en los congelados v2 y v3 (`CONGELADO_P8_v3.md`): el mando de la bestia medio, echar y matar a la bestia encendidos, el árbol de fruta dulce encendido. Las criaturas RG juegan con los sabores.

| mundo | qué cambia (`lanzador.mundo_de`) |
|---|---|
| abundancia | las épocas de los matorrales a ×1,3 todo el rato (también el huerto) |
| normal | sin épocas |
| sequía | épocas de 5 días en ciclo: abundancia ×1,3, normal, escasez ×0,7, normal (la escasez, los días 10–14 y 30–34); también el huerto |
| sequía dura | el mismo ciclo ×0,7 (0,91; 0,7; 0,49; 0,7) toda la partida (`estres.sequia_dura`) |
| bestias que crían | la bestia baja también de día (`bestia.de_dia`) y nace otra a los 20 días, hasta dos (`estres.bestias_crian`) |

## Los números elegidos

Los mismos del congelado v3. Los tres cambios de RG61r **no añaden ningún número**: el cuarto del robo es el del regalo; las testigos usan el peso con el que ya aprenden un robo visto; S-QUITAR usa el reparto de G-ALIVIO y el peso de dar.

| número | valor | dónde | de quién |
|---|---|---|---|
| el gesto | media comida sencilla del bosque: 0,5 × (dh(60) − dh(25)) × el peso de la otra; solo al dar comida | `config_cuerpo_valle.json → dar_v53.gesto_parte`; `sabores_v40.hambre_ref` | Manel (prompts 104, 105 y 108) |
| devolver | lo que me dio hace menos de **40** turnos, o ese mismo turno | `dar_v57.devolver_turnos` | Manel (prompts 109 y 110) |
| el hambre supuesta de la otra | **80** si está flaca, **30** si no | `banda_de_la_hermana.flaca_hambre_estimada`; `gusto_v49.no_flaca_hambre_estimada` | el 30, propuesto por mí (prompt 95) |
| el gusto con la tripa llena | **un cuarto**; con mucha hambre, entero (desde 60); en medio, en proporción | `gusto_v49.lleno` | Manel (prompt 95) |
| el reparto de las filas | **0,8 · 0,1 · 0,1** (la tabla del siete); el gesto, el alivio de la otra y S-QUITAR, 0,1 · 0,1 · 0,8, leído de F-HAMBRE | `appraisal_zs_v42_exp` | el siete; Manel para el gesto, el alivio y S-QUITAR |
| el peso de la otra | familia: hermana **0,9864**, vecina **0,3675**, × radar entero ahora / al nacer | `radar_v39`; al nacer, `radar_v34` (hermana_vinculo 0,5; vecina 0,25 de la hermana) | los pesos de RG32r (prompt 84); el 0,25, provisional (prompt 79) |
| el trato del radar | cada mirada (**44** turnos): la parte a la vista + **¼** por cada cuidado (y, en RG61r, − ¼ por cada robo) | `config_cuerpo_valle.json → mirada`; `cuerpo_valle._rad_vive` | el cuarto, del prompt 79; el robo, Manel (prompt 115) |
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
15. **Quién me dio algo, lo deduzco de lo que veo:** de mi bolsa y de las bolsas de las pegadas. Con varias pegadas a la vez, o si no veo su bolsa, me puedo equivocar. (Los empujones ganados ya no cuentan como regalo.)
16. **Se roba entre criaturas sin hambre,** con entre 133 y 256 empujones por partida según el mundo (taller del prompt 116). La marca del robo en el vínculo (un cuarto menos en el trato) pesa menos que el tiempo a la vista: la ladrona todavía sube en el radar de la robada, aunque la mitad que antes.

**Arreglados desde el v3:**
- ganar un empujón se apuntaba como un regalo de la perdedora, unos 152 apuntes falsos por partida;
- el robo no dejaba ninguna marca en el trato;
- el espejo de dar al quitar comida estaba en recursos y con otro peso.

## Lo que se sabe de RG61r antes del experimento

Del taller de los prompts 115 y 116 (`informe_arreglos_v8.md`; 5 mundos × semillas 1001–1010, frente a RG58r en las mismas semillas):
- RG58r con el código nuevo y los interruptores apagados sale **idéntico** al congelado v3 (dos puertas).
- **Sin muertes por golpe;** la racha de ida y vuelta más larga es de 3.
- **Vive como RG58r:** +0,06 [−0,22, +0,34].
- **Desaparecen unos 152 apuntes de regalo falsos por partida.**
- **La ladrona sube la mitad** en el radar de la robada.
- **Los empujones no bajan.**

## Las semillas reservadas para el experimento

**30081–30120** (40 semillas). En el valle no se han usado nunca: ninguna partida del disco las lleva (`congelado_v4/semillas_v4.md`). En el repositorio salen tres números con forma de semilla:
- 30081, en el propio lanzador v4;
- 30092, en un fichero de `paintball/runs`;
- 30105, en los resultados del siete (`paper7/P7_10`).

Las dos últimas son de otros mundos, no del valle. Las 30001–30040 son del experimento v2 y las 30041–30080 del v3.
