# P7-67 · El campo: la mentira seguible, con el mando de la amenaza · apertura del sello

*Guion sellado `analiza_P7_67.py` (md5 `7bef2e46106bb860c366b0bdb1dba037`, el de la enmienda 1 de `SELLO_P7_67.md`), corrido tal cual sobre el campo terminado. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Este informe lo escribe `escribe_informe_P7_67_campo.py`; ninguna cifra a mano. Lo que no estaba en el sello va marcado «exploratorio, no sellado» o «no sellado: cota del efecto».*

*Nota de lectura: el registro de una llegada lleva la etiqueta del tic t, y la posición que la justifica aparece en el diario en el tic t+1 (el desfase de un tic ya conocido). Los GIF terminan en ese tic t+1.*

## 1. Comprobaciones previas (hechas antes de ver ningún resultado)

- `motor/model.py` y `analiza_P7_67.py` con el md5 de arriba; `SELLO_P7_67.md` sin cambios desde su último commit (enmienda 4).
- Partidas por brazo y nivel: nivel 1 MIENTE 320; nivel 1 CONGELADA 320; nivel 1 HONESTA 320; nivel 2 MIENTE 30; nivel 2 HONESTA 30; nivel 3 MIENTE 30; nivel 3 HONESTA 30; nivel 14 MIENTE 30; nivel 14 HONESTA 30. Total 1140 (diseño: 1140).
- Vidas: 2280 criatura-días leídos, cada una con su diario (el `.art.log` o el `.zip`) y su cuaderno de fin. Llegadas sin oportunidad (anomalías): 0.
- Partidas apartadas por fallo de la plataforma (no cuentan; repetidas con la misma imagen y semilla): 6.

## 2. Partidas marcadas (regla sellada: marcada si cualquiera de las dos hermanas falla la guarda; en la robustez sale entera): 13

- nivel 1 · CONGELADA · serie 1 · día 19 · asiento(s) 11 · bloqueados sin cuerpo 21.1 % > 5 %
- nivel 1 · CONGELADA · serie 3 · día 7 · asiento(s) 10 · bloqueados sin cuerpo 5.9 % > 5 %
- nivel 1 · CONGELADA · serie 5 · día 11 · asiento(s) 10 · decisiones por encima del tic 1.89 % > 1 %
- nivel 1 · HONESTA · serie 6 · día 12 · asiento(s) 11 · bloqueados sin cuerpo 12.2 % > 5 %
- nivel 1 · HONESTA · serie 7 · día 14 · asiento(s) 11 · bloqueados sin cuerpo 8.3 % > 5 %
- nivel 1 · HONESTA · serie 8 · día 3 · asiento(s) 10 · bloqueados sin cuerpo 5.3 % > 5 %
- nivel 1 · HONESTA · serie 13 · día 6 · asiento(s) 11 · bloqueados sin cuerpo 8.6 % > 5 %
- nivel 1 · HONESTA · serie 14 · día 16 · asiento(s) 11 · bloqueados sin cuerpo 5.8 % > 5 %
- nivel 1 · HONESTA · serie 15 · día 1 · asiento(s) 11 · bloqueados sin cuerpo 14.5 % > 5 %
- nivel 1 · HONESTA · serie 16 · día 1 · asiento(s) 11 · bloqueados sin cuerpo 6.3 % > 5 %
- nivel 1 · MIENTE · serie 6 · día 3 · asiento(s) 11 · bloqueados sin cuerpo 5.4 % > 5 %
- nivel 1 · MIENTE · serie 16 · día 10 · asiento(s) 11 · bloqueados sin cuerpo 13.3 % > 5 %
- nivel 14 · MIENTE · serie 6 · día 4 · asiento(s) 11 · decisiones por encima del tic 1.12 % > 1 %

## 3. Las predicciones selladas

| predicción | cuenta | estimación | error estándar | unidades | veredicto |
|---|---|---|---|---|---|
| P1 | cuenta principal | -0,2203 | 0,0135 | 16 | **PASA** |
| P1 | robustez (a): sin las partidas marcadas | -0,2171 | 0,0124 | 16 | **PASA** |
| P1 | robustez (b): la criatura como unidad | -0,2201 | 0,0147 | 32 | **PASA** |
| P2 | cuenta principal | -0,3378 | 0,0362 | 16 + 16 | **PASA** |
| P2 | robustez (a): sin las partidas marcadas | -0,3357 | 0,0356 | 16 + 16 | **PASA** |
| P2 | robustez (b): la criatura como unidad | -0,3378 | 0,0320 | 32 + 32 | **PASA** |
| P3 | cuenta principal | -0,0194 | 0,0172 | 68 | **NO PASA** |
| P3 | robustez (a): sin las partidas marcadas | -0,0254 | 0,0182 | 68 | **NO PASA** |
| P3 | robustez (b): la criatura como unidad | -0,0169 | 0,0163 | 136 | **NO PASA** |
| P3b | cuenta principal | -0,0787 | 0,0331 | 68 | **NO PASA** |
| P3b | robustez (a): sin las partidas marcadas | -0,0784 | 0,0345 | 66 | **NO PASA** |
| P3b | robustez (b): la criatura como unidad | -0,0394 | 0,0154 | 136 | **NO PASA** |

- P1 (MIENTE, media de B − A por pareja): parejas que cumplen el mínimo de 3 días con oportunidad en A y en B: **16**; fuera: 0.
- P2: MIENTE -0,2203 (n 16) − CONGELADA 0,1175 (n 16); parejas de CONGELADA fuera: 0.
- P3 (fracción de llegadas d1-5 sobre ln(rivales), con el brazo como indicadora): 68 parejas; fuera por no tener oportunidad: 0. Por nivel (media ± ee): 1 rivales 0,644 ± 0,040 (n 32); 2 rivales 0,592 ± 0,062 (n 12); 3 rivales 0,635 ± 0,056 (n 12); 14 rivales 0,589 ± 0,040 (n 12).
- P3b (llegadas medias por día d1-5, 0 sin oportunidad): 68 parejas. Por nivel: 1 rivales 1,288 ± 0,081 (n 32); 2 rivales 1,067 ± 0,119 (n 12); 3 rivales 1,133 ± 0,121 (n 12); 14 rivales 1,083 ± 0,067 (n 12).
- Fracción de días con oportunidad, días 1-5 (descriptivo sellado): 1 100,0 % (480 de 480); 14 92,5 % (111 de 120); 2 90,0 % (108 de 120); 3 88,3 % (106 de 120).

## 4. Robustez: ¿cambia algún veredicto entre cuentas?

- P1: no cambia (PASA en las tres cuentas).
- P2: no cambia (PASA en las tres cuentas).
- P3: no cambia (NO PASA en las tres cuentas).
- P3b: no cambia (NO PASA en las tres cuentas).

## 5. Descriptivo

**Sellado:** HONESTA, la confianza día a día, las interrupciones por nivel y las muertes.

- HONESTA (B − A por pareja, como referencia): media 0,0875 ± 0,0196 (n 16; fuera 0).
- Confianza media en recursos al arrancar cada día, nivel 1:

| día | MIENTE | CONGELADA | HONESTA |
|---|---|---|---|
| 1 | 0,500 | 0,500 | 0,500 |
| 2 | 0,458 | 0,500 | 0,519 |
| 3 | 0,360 | 0,500 | 0,585 |
| 4 | 0,341 | 0,500 | 0,602 |
| 5 | 0,271 | 0,500 | 0,642 |
| 6 | 0,229 | 0,500 | 0,740 |
| 7 | 0,202 | 0,500 | 0,818 |
| 8 | 0,200 | 0,500 | 0,817 |
| 9 | 0,200 | 0,500 | 0,801 |
| 10 | 0,188 | 0,500 | 0,814 |
| 11 | 0,188 | 0,500 | 0,813 |
| 12 | 0,188 | 0,500 | 0,869 |
| 13 | 0,181 | 0,500 | 0,908 |
| 14 | 0,181 | 0,500 | 0,824 |
| 15 | 0,161 | 0,500 | 0,876 |
| 16 | 0,161 | 0,500 | 0,913 |
| 17 | 0,159 | 0,500 | 0,939 |
| 18 | 0,159 | 0,500 | 0,826 |
| 19 | 0,157 | 0,500 | 0,822 |
| 20 | 0,157 | 0,500 | 0,838 |

- Interrupciones y llegadas por nivel, días 1-5: 1 rivales: 480 criatura-días, 480 oportunidades, 480 aceptadas, 0 interrumpidas, 318 llegadas; 2 rivales: 120 criatura-días, 108 oportunidades, 113 aceptadas, 14 interrumpidas, 64 llegadas; 3 rivales: 120 criatura-días, 106 oportunidades, 114 aceptadas, 14 interrumpidas, 68 llegadas; 14 rivales: 120 criatura-días, 111 oportunidades, 131 aceptadas, 58 interrumpidas, 65 llegadas.
- Muertes (criatura-días eliminados): n14_HONESTA 51 de 60; n14_MIENTE 47 de 60; n1_CONGELADA 179 de 640; n1_HONESTA 157 de 640; n1_MIENTE 169 de 640; n2_HONESTA 36 de 60; n2_MIENTE 30 de 60; n3_HONESTA 47 de 60; n3_MIENTE 44 de 60.

**Exploratorio, no sellado: por bloque de días, nivel 1.**

| grupo · días | criatura-días | ocasiones | aceptaciones | llegadas | aciertos | fallos | interrumpidas (rival activo a ≤ 3) | no llegó |
|---|---|---|---|---|---|---|---|---|
| MIENTE d1-5 | 160 | 160 | 160 | 73 | 0 | 73 | 0 | 87 |
| MIENTE d6-10 | 160 | 159 | 157 | 16 | 0 | 16 | 0 | 141 |
| MIENTE d11-15 | 160 | 160 | 160 | 15 | 0 | 15 | 0 | 145 |
| MIENTE d16-20 | 160 | 130 | 129 | 2 | 0 | 2 | 0 | 127 |
| CONGELADA d1-5 | 160 | 160 | 160 | 112 | 0 | 112 | 0 | 48 |
| CONGELADA d6-10 | 160 | 159 | 159 | 143 | 0 | 143 | 0 | 16 |
| CONGELADA d11-15 | 160 | 160 | 160 | 153 | 0 | 153 | 0 | 7 |
| CONGELADA d16-20 | 160 | 130 | 130 | 113 | 0 | 113 | 0 | 17 |
| HONESTA d1-5 | 160 | 160 | 160 | 133 | 104 | 29 | 0 | 27 |
| HONESTA d6-10 | 160 | 160 | 160 | 159 | 135 | 24 | 0 | 1 |
| HONESTA d11-15 | 160 | 160 | 160 | 160 | 148 | 12 | 0 | 0 |
| HONESTA d16-20 | 160 | 160 | 160 | 160 | 118 | 42 | 0 | 0 |

## 6. No sellado: cota del efecto (estimación ± 2 errores estándar) de cada predicción que no pasa

- P3, cuenta principal: [-0,0537, 0,0149].
- P3b, cuenta principal: [-0,1449, -0,0126].
- P3, robustez (a): sin las partidas marcadas: [-0,0619, 0,0111].
- P3b, robustez (a): sin las partidas marcadas: [-0,1473, -0,0094].
- P3, robustez (b): la criatura como unidad: [-0,0494, 0,0156].
- P3b, robustez (b): la criatura como unidad: [-0,0701, -0,0086].

## 7. GIF (exploratorio, no sellado; datos crudos, matplotlib; elegidos al azar con random.Random(20261020))

Candidatos: 17 llegadas de MIENTE en los días 11-20 (nivel 1) y 505 llegadas de HONESTA con acierto (nivel 1).

- `P7_67F_gif_miente.gif`: MIENTE, serie 13, día 14, asiento 11, destino (10, 4), de la aceptación (tic 481) a la llegada (tic 569, 88 tics), acierto 0; 46 fotogramas. ![P7_67F_gif_miente.gif](../figuras/P7_67F_gif_miente.gif)
- `P7_67F_gif_honesta.gif`: HONESTA, serie 13, día 4, asiento 11, destino (27, 23), de la aceptación (tic 481) a la llegada (tic 613, 132 tics), acierto 1; 68 fotogramas. ![P7_67F_gif_honesta.gif](../figuras/P7_67F_gif_honesta.gif)

## 8. Exploratorio, no sellado: dos preguntas de Manel (20-oct)

*Guion `explora_P7_67_campo.py` → `P7_67_explora.json`; lee los diarios; no toca nada sellado.*

**8.1. ¿Por qué MIENTE y CONGELADA tienen criatura-días sin oportunidad en los días 16-20 y HONESTA ninguno?**

- Todos son del día 19: 60 criatura-días (MIENTE y CONGELADA a partes iguales). Destino de la mentira ese día: (3, 3). Las 4 criatura-días del día 19 que sí tuvieron oportunidad son todas de la serie 5.
- La invitación se cargó en 60 de 60; el destino es suelo transitable en el mapa fijo en todas (ground 60). `ir_sitio` no se ofreció en ningún tic en 60 de 60.
- Distancia al destino al empezar: ella 10 (30), 15 (30); su hermana 15 (30), 10 (30). La hermana del asiento 11 sale del pedestal (18, 9) exactamente a 15 casillas, el borde de la regla 8-15; tras su primer paso queda a: 16 (30), 11 (30).
- En los tics con elección (más de un candidato; con uno solo, `noop`, el cuerpo no ofrece ningún movimiento), 13486 en total: la hermana fuera de 8-15 en 12911, ella fuera de 8-15 en 12878, sin calma en 0. En cada criatura-día solo hubo **un** tic con elección y todo a la vez: el primer tic vivo.
- Y en el primer tic vivo la invitación no se ofrece nunca, en todo el campo: la primera oferta llega como pronto en el tic 1 (0 ofertas en el tic 0, de 2183 criatura-días con oferta).
- **Lectura descriptiva:** la condición que falló es la distancia 8-15 a las dos hermanas, por la hermana del asiento 11, que empieza a 15 y da su primer paso alejándose. No falló la calma, no faltó una casilla de borde válida ni el destino era inalcanzable. HONESTA no tiene este caso: sus destinos están en el centro.

**8.2. HONESTA: ¿por qué bajan los aciertos en los días 16-20?**

- Aciertos de HONESTA por destino, días 1-20: (27, 23): 131 de 205 (días 1, 3, 4, 10, 13, 17, 20); (21, 24): 151 de 183 (días 2, 7, 8, 9, 18, 19); (24, 23): 223 de 224 (días 5, 6, 11, 12, 14, 15, 16).

| día | destino | llegadas | aciertos | sin botiquín a la vista | botiquines vistos (mediana) | el más cercano al destino (mediana, casillas) | destino dentro de la zona | radio de la zona | tic de llegada (mediana) |
|---|---|---|---|---|---|---|---|---|---|
| 11 | (24, 23) | 32 | 32 | 0 | 2 | 2 | 32 de 32 | 24 | 613 |
| 12 | (24, 23) | 32 | 32 | 0 | 2 | 2 | 32 de 32 | 24 | 613 |
| 13 | (27, 23) | 32 | 20 | 0 | 2 | 2 | 32 de 32 | 24 | 613 |
| 14 | (24, 23) | 32 | 32 | 0 | 2 | 2 | 32 de 32 | 24 | 613 |
| 15 | (24, 23) | 32 | 32 | 0 | 2 | 2 | 32 de 32 | 24 | 613 |
| 16 | (24, 23) | 32 | 32 | 0 | 2 | 2 | 32 de 32 | 24 | 613 |
| 17 | (27, 23) | 32 | 18 | 0 | 2 | 3 | 32 de 32 | 24 | 613 |
| 18 | (21, 24) | 32 | 26 | 0 | 2 | 3 | 32 de 32 | 24 | 624 |
| 19 | (21, 24) | 32 | 28 | 0 | 2 | 3 | 32 de 32 | 24 | 624 |
| 20 | (27, 23) | 32 | 14 | 1 | 2 | 4 | 32 de 32 | 24 | 613 |

- Botiquines en el mapa entero al llegar: **no consta** (el diario solo trae lo que la criatura ve). Lo visible: casi siempre hay botiquines a la vista; lo que cambia es a qué distancia del destino.
- El destino estaba dentro de la zona segura en todas las llegadas: se llega hacia el tic 600, mucho antes de que la zona empiece a cerrarse.
- **Lectura descriptiva:** los aciertos dependen del destino del día. En los días 16-20 tocaron dos veces (27, 23) y dos veces (21, 24), los destinos donde el botiquín más cercano queda más a menudo a más de 3 casillas; el día 16, con (24, 23), acierta 32 de 32.

## 9. Gasto

- **Créditos de la plataforma:** 1146 créditos de experiencia (1140 partidas del campo + 6 reintentos por partidas apartadas). Saldo real: **no consta**; la API de la plataforma no da el saldo (todas las rutas probadas responden 404). Hay que leerlo en la web.
- **Dólares de la consola de Anthropic:** 0 $ (no se llama a la razón).
