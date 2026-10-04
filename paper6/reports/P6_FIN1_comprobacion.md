# P6-FIN1 · Comprobación final de números y figuras del paper seis

*2-oct-2026. Coste cero. Borrador comprobado: `cantera/paper6/paper6_ES_borrador_v1.md` (386 líneas). Cada valor se ha leído en su
informe; «P6-N:l» = `cantera/paper6/informe_P6_N.md`, línea l. Marcas: **≠** no coincide o la fuente es otra; **~** coincide con
matiz; sin marca, coincide. El borrador no se ha tocado.*

## 0 · Las discrepancias, primero

1. **Apéndice §5, «2.120 de 2.253 (84 %)»** → **≠**. La fuente dice **2.120 de los 2.536 rechazos por área (84 %)**; 2.253 es otra cuenta
   de la misma fila de la tabla (los rechazos con último punto de control). P6-15:23-24, 53.
2. **Texto §2, «catorce criaturas, siete parejas»** → **≠**. Son **dieciséis criaturas, ocho parejas**: catorce asientos rivales más la
   pareja (P6-1:378 «los catorce asientos rivales»; el `static_map` del diario tiene 16 pedestales de salida; `STATUS.md`:7 «16 agents in 8 teams»).
3. **Apéndice §4, «0 tics: 79 %; más de 100 tics: 49 %» y texto «entre las que entraban… más de cuatro segundos ardiendo, la mitad»** → **~**.
   El informe da rangos por brazo (0 tics: 79-86 %; > 100: 29-49 %; P6-17:139, 261). Los valores agregados 79 % (15 de 19) y 49 % (35 de 72)
   salen de `P6_17_final.json` **contando todas las vidas vivas en el aviso, también las 18 que nunca entran**. Solo entre las que entran:
   15 de 19 (79 %), 9 de 11 y **35 de 57 (61 %)**. La frase del texto («entre las que entraban… la mitad») no cuadra con «la mitad».
4. **Apéndice §4, «diecinueve con una casilla segura al alcance … (P6-16)»** → **~**. El 19 de 22 es «llegaba a salvo saliendo en el primer
   golpe», P6-13:123. La salvedad atribuida a P6-16 («alcanzables, no necesariamente sobrevivibles») **no la he encontrado en P6-16**.
5. **Apéndice §4, «ni una vuelta en sesenta partidas | 0 en 60»** → **≠ no encontrado**. P6-17 dice que «salir y volver» tiene margen
   aritmético en 30 de 62 muertes y lo clasifica como «aritmético, no medido» (P6-17:31, 280); no he encontrado la cuenta «0 en 60».
6. **Texto §6, «en el campo tardaba unos cuatro segundos de media»** → **~**: 94 tics es la **mediana** (p95 140), P6-27:109.
7. **Apéndice §3, «diecinueve de veinte juntas al cierre | informe_P6_11, informe_P6_12»** → **~**: está en P6-11:196; en P6-12 no lo veo escrito.
8. **Apéndice §3, «22 de 40 vidas | informe_P6_12»** → **~**: la medida es de P6-11:161, 172 (A4: 22 muertes por anillo en 40 vidas); P6-12:68 solo la repite.
9. **Apéndice §4, «mediana 2 pasos, 22 tics»** → **~**: el informe da 2 pasos de mediana (P6-13:241); los 22 tics son 2 × 11 (regla
   «pasos × 11», P6-13:221), no están escritos como tales.
10. **Apéndice §5, «mejora en 24, empeora en 13»** → coincide, con nota: P6-24:99 lo escribe como «13/24» (gana/pierde de la diferencia
    A7h − A4: 13 semillas en que A7h arde más, 24 en que arde menos).
11. **Texto §4, «de sesenta y cinco veces… solo se quedó en dos. En las otras sesenta y tres»** → coincide con P6-17:151-152 (2 de 65; 63
    salen), aunque el propio informe habla en §0 de «63 planes que llegaron dentro» y en §3 de «65 planes cumplidos» (P6-17:24, 145).

Todo lo demás coincide con su fuente (tablas abajo).

## 1 · El apéndice, fila a fila

### Sección 3

| en el apéndice | fuente | ¿coincide? |
|---|---|---|
| un parte cada 48 tics | P6-2:35 (48 tics en 5.323 de 5.323 huecos) | sí |
| mediana 2; 91,8 % a 4 o menos | P6-2:183, 186 | sí |
| una cuarta parte solo suyo; 47-59 % | P6-2:200-201, 209-210 (21,1 / 25,5 %, «la cuarta parte»); 204-205 (47,2 / 58,6 %) | sí |
| 6 de 7 campos; todas las vías exigen ver | P6-2:69-80; P6-3:25-26 | sí |
| 2.281 a 8.085 (5.600), hermano 10 | P6-2:241, 245-247 | sí |
| canal al 13,3 % (siete veces y media) | P6-2:163-165 | sí |
| E2 cada 25 tics | P6-3:90, 104 | sí |
| 687: 458 / 224 / 5 / 0 | P6-4:119-127, 149-150 | sí |
| 0 de 18.315 partes | P6-5:371-373 | sí |
| −1.301,8; 6 de 20; p 0,115 | P6-6:245, 256-258 | sí |
| S-8 −57,4 % | P6-6:235, 251 | sí |
| 79,1 → 59,9 % | P6-7:25-26, 210 | sí |
| escapadas 3 → 19 | P6-7:27, 215 | sí |
| 9,5 contra 1 casillas | P6-7:47-48, 153 | sí |
| 154 / 144 / 173 tics; 13-16 casillas | P6-9:58, 208 | sí |
| 1 de 46 (A1), 2 de 44 (A2) | P6-9:107 | sí |
| D0 = 7 (mitad de 154 / 11) | P6-10:27-33 (154 → 77 tics; 11 por casilla; 7,00) | sí |
| 78,9 %; 0 % | P6-10:151, 165 | sí |
| 30 → 1 | P6-10:152, 167 | sí |
| +1.668, 14 de 20 | P6-10:153, 191 | sí |
| +452, 11 de 20, p 0,82 | P6-10:153, 192-193 (0,824) | sí |
| 19 de 19 | P6-10:154, 174 | sí |
| 3,0 contra 16,2 | P6-11:22-24 | sí |
| A3 6, A0 2; A4 2 | P6-10:200; P6-11:157, 172 | sí |
| 3,95 → 2,88 (A0 3,20) | P6-11:160, 181 | sí |
| 19/20 juntas al cierre | P6-11:196 (P6-12: no localizado) | ~ |
| 22 de 40 vidas | P6-11:161, 172 (P6-12:68 lo repite) | ~ |

### Sección 4

| en el apéndice | fuente | ¿coincide? |
|---|---|---|
| 7 fases; centro (24, 24) | P6-13:21-29, 32-47 | sí |
| sorpresa F-ANTICIPACION 0,0017 contra S-8 0,043 | P6-13:175-176 (medias 0,00166 / 0,04329) | sí |
| 16 de 22 | P6-13:88 | sí |
| 22 de 22; mediana 2 pasos; 22 tics; 966 tics | P6-13:241 (2 pasos, 966); 119 (966 / 7); 22 tics = 2 × 11 (P6-13:221) | ~ |
| 12; 8; hermano 1; otra 1 | P6-13:131-136 | sí |
| techos 0,30 contra 0,167 | P6-13:156, 184 | sí |
| 19 de 22 (salvedad P6-16) | P6-13:123; la salvedad no está en P6-16 | ~ |
| fuego 0,33 por tic; 300 tics con 100 de vida | P6-17:179 | sí |
| 30 de 62; 0 en 60 | P6-17:31, 280 (30 de 62); «0 en 60» no encontrado | ≠ |
| 57 contra 53 % | P6-17:24, 136 | sí |
| 40 % y 3 %; 1 % y 18 %; 325 golpes | P6-17:29-30, 185, 230, 233 | sí |
| 167 de 225 | P6-17:30-31, 235, 237 | sí |
| 0 de 28 (0/18; 0/10) | P6-17:22-23, 89, 123, 134 | sí |
| 63-83 % | P6-17:23, 135 | sí |
| 0 tics: 79 %; > 100: 49 % | P6-17:139, 261 (rangos por brazo 79-86 / 29-49); agregado sobre todas las vidas en `P6_17_final.json` | ~ (ver 0.3) |
| 2 de 65; 11-12 tics | P6-17:151-152 | sí |
| ~10 supervivientes detectables | P6-17:20, 46 | sí |

### Sección 5

| en el apéndice | fuente | ¿coincide? |
|---|---|---|
| 27 de 3.849 (0,7 %) | P6-14:22-23 | sí |
| 3 de 19 | P6-14:21-22, 145 | sí |
| 2.120 de 2.253 (84 %); +31 | P6-15:23-24, 53 (**2.120 de 2.536**); 56 (+31,0) | **≠** |
| 17 de 19 (techo 18) | P6-15:27-30 | sí |
| 129 contra 3 | P6-16:22 | sí |
| 48 de 63 (76 %) | P6-18:16 | sí |
| 1.054; 2 de 74 | P6-18:20-21 | sí |
| P(golpe) 0,0002 (arco) a 0,0206 (espada); anillo 77 % | P6-19:48-52, 20 | sí |
| 40,8 % (A5h), 40,5 % (A6); A4 0 % | P6-21:134 | sí |
| 12-73 ms contra 41,7; proceso aparte | P6-22:30-32 | sí |
| 0,28 / 0,36 % (P6-23); 0,02 / 0,11 % (P6-24) | P6-23:92; P6-24:72 | sí |
| 5,5-17 % en brazos con puerta; conclusiones sostenidas | P6-22:21-22; informe_P5_LAG:23-24 | sí |
| −57,6; 24/13; p unilateral 0,007; IC95 [−100,9, −15,3] | P6-24:99 (escrito «13/24») | sí |
| 46,0 contra 35,6 % | P6-24:70 | sí |
| 19 de 70; 6 de 58 | P6-24:22, 80; P6-23:23 | sí |

### Secciones 6 y 7

| en el apéndice | fuente | ¿coincide? |
|---|---|---|
| 51,0 / 51,3 / 54,6 % | P6-25:68 | sí |
| 172-174 de 200; p 0,57 y 0,85 | P6-25:75, 87 | sí |
| 3,7 s y 8,1 s (90 y 195 tics) | P6-25:23 (tics = s × 24, derivado) | sí |
| 51,8 / 41,0 % | P6-25:103 | sí |
| intraducibles 1,5 / 7,5 % | P6-25:66 | sí |
| 2.º 8,1 / 14,3 %; 3.º 0 / 4,2 % | P6-25:122-123 | sí |
| 22,6 / 15,7 % | P6-26:21-22, 42-43 | sí |
| 82,5 / 100 %; 20,0 / 17,5 % | P6-25:141, 143 | sí |
| 75 de 92; 11 partidas | P6-27:115 (11 de 38 partidas) | sí |
| A4 232,3, A7h 174,7, A8 220,4; −9,9 (p 0,35, IC); +43,1 (p 0,08) | P6-27:100-102 | sí |
| 94 tics (serie), 113 (humo) | P6-27:109; P6-26:25, 107 | sí |
| 59 de 109 | P6-27:111 | sí |
| 33,5 contra 36,7 %; 251; p 0,28 | P6-28:19-20, 49-50 | sí |
| mediana 2, p90 7 | P6-28:55 | sí |
| 75,5 / 73,6 %; +0,08 / +0,12 | P6-27:116, 130 | sí |
| 83,9 / 82,4 % | P6-29:14-15 | sí |
| 92 %; 76 % | P6-29:66-67 (75,9 %) | sí |
| 0,154 contra 0,065 | P6-29:59, 67-68 | sí |
| mediana 0,28 / 0,27, p90 17 / 3,9, máx 102 | P6-29:61 | sí |
| 20,0 contra 0,18 | P6-29:17 | sí |
| 132 por reevaluación, 76 por la vida | P6-29:77, 87 | sí |
| media +42 / +15, mediana 0; Spearman −0,07 / +0,18 | P6-29:97-98, 104 | sí |
| 200 tics; 99,7 % (A4 98,8 %) | P6-29:20-21, 111 | sí |

## 2 · Frases del texto con cifra que no están en el apéndice

Comprobadas con el reloj del mundo (24 instantes por segundo, 11 instantes por casilla) y con su informe:

| frase | cuenta | ¿cuadra? |
|---|---|---|
| §2 «veinticuatro veces por segundo»; «cada dos segundos» (parte) | 24 tics/s; 48 tics = 2,0 s | sí |
| §2 «catorce criaturas, siete parejas» | 14 asientos rivales + la pareja = 16, 8 parejas (P6-1:378) | **≠** |
| §2 «partidas el doble de largas» | 18.240 frente a 9.120 tics (informe_P5ARI3) | sí |
| §3 «veinte vidas de parejas» | 20 diarios de P6-1 (P6-2:34; P6-3:218) | sí |
| §3 «unos cuatro minutos sin una ración» | 8.085 − 2.281 = 5.804 tics = 4,0 min | sí |
| §3 «cabía siete veces y media» | 100 / 13,3 = 7,5 | sí |
| §3 «cada segundo en lugar de cada dos» | 25 tics = 1,04 s | sí |
| §3 «casi setecientos golpes, dos de cada tres del anillo» | 687; 458 / 687 = 67 % | sí |
| §3 «casi un minuto menos por vida» | 1.301,8 / 24 = 54 s | sí |
| §3 «seis o siete segundos»; «trece y dieciséis casillas»; «media pelea… unas siete casillas» | 144-173 tics = 6,0-7,2 s; 13-16; 77 / 11 = 7 | sí |
| §3 «casi un minuto y diez segundos más» | 1.668 / 24 = 69,5 s | sí |
| §3 «un sexto de una espada» | 3,0 / 16,2 = 0,19; el informe lo dice así (P6-11:32) | sí |
| §3 «más de la mitad mueren quemadas» | 22 / 40 = 55 % | sí |
| §4 «un segundo de camino»; «unos cuarenta segundos de margen» | 22 tics = 0,9 s; 966 / 24 = 40 s | sí |
| §4 «dentro de treinta segundos aquí no se podrá estar» | fase 5: del aviso (11.856) al cierre (12.636), 780 tics = 32,5 s | sí |
| §4 «casi el doble» | 0,30 / 0,167 = 1,8 | sí |
| §4 «unos doce segundos fuera con toda la vida» | 300 / 24 = 12,5 s | sí |
| §4 «en sesenta partidas ni una sola criatura salió y volvió a entrar» | 60 partidas sí (P6-17:3); la cuenta «ninguna volvió» no encontrada | **≠** |
| §4 «entre seis y ocho de cada diez»; «ocho de cada diez»; «más de cuatro segundos, la mitad» | 63-83 %; 79 % (todas las vidas); > 100 tics = 4,2 s, 49 % todas / 61 % las que entran | ~ (ver 0.3) |
| §4 «al cabo de medio segundo» | 11-12 tics = 0,5 s | sí |
| §5 «menos de uno de cada cien»; «ocho de cada diez rechazos»; «unas cuarenta veces más» | 0,7 %; 84 %; 129 / 3 = 43 | sí |
| §5 «tres de cada cuatro… prefería quedarse»; «más de mil pasos»; «dos de setenta y cuatro» | 76 %; 1.054; 2 / 74 | sí |
| §5 «tres de cada cuatro puntos de daño, el anillo» | 77 % | sí |
| §5 «cuatro de cada diez pasos»; «menos de uno de cada doscientos» | 40,8 / 40,5 %; 0,28 / 0,36 % < 0,5 % | sí |
| §5 «unos cincuenta y ocho instantes… dos segundos y medio menos de fuego» | 57,6 / 24 = 2,4 s | sí |
| §5 «menos de uno entre cien»; «más de uno de cada cuatro» | p 0,007; 19 / 70 = 27 % | sí |
| §6 «unos cuatro segundos… más de ocho»; «entre noventa y doscientos instantes» | 3,7 s = 89 tics; 8,1 s = 194 | sí |
| §6 «la mitad; cuatro de cada diez»; «tarda la mitad» | 51,8 / 41,0 %; 3,7 contra 8,1 s | sí |
| §6 «en ocho de cada diez no había ninguno» | 100 − 22,6 = 77 %; 100 − 15,7 = 84 % | sí |
| §6 «una vez de cada cinco»; «ocho de cada diez envíos»; «once partidas» | 20,0 / 17,5 %; 75 / 92 = 82 %; 11 | sí |
| §6 «unos cuatro segundos de media» (campo) | 94 tics = 3,9 s, pero es la **mediana** (P6-27:109) | ~ |
| §6 «más de la mitad se rechazaron al llegar»; «dentro de cuatro segundos» (adelanto) | 54 %; Δ = 94 tics = 3,9 s | sí |
| §6 «un par de casillas»; «tres de cada cuatro» | mediana 2; 75,5 / 73,6 % | sí |
| §7 «ocho de cada diez instantes»; «nueve de cada diez… tres de cada cuatro» | 83,9 / 82,4; 92; 75,9 % | sí |
| §7 «más del doble»; «cientos de veces lo que el plan típico»; «unas cien veces más» | 0,154 / 0,065 = 2,4; 102 / 0,28 = 364; 20,0 / 0,18 = 111 | sí |
| §7 «los ocho segundos siguientes» | 200 tics = 8,3 s | sí |
| §9 «menos de uno de cada doscientos» | 0,28 / 0,36 % | sí |

Fuera del alcance de los informes del seis: §1 «la vida duraba dos minutos» (paper cuatro) y «en cien partidas» (paper cinco, P5-6C).

## 3 · La deformación, tal como la calcula el código (`mide_P6_29.py`)

La definición propuesta («en cada instante con plan vivo, malestar imaginado con la acción del plan menos malestar imaginado con la acción
que el cuerpo habría elegido solo, en la unidad del malestar; la acumulada es la suma durante el plan») es correcta en lo esencial. Cuatro
precisiones del código:

1. **Qué instantes cuentan.** Solo los tics con plan vivo (de la aceptación al fin del plan) **y con las piernas listas** (`move_ready_in` 0),
   `mide_P6_29.py:273`. Los tics de enfriamiento no entran en la acumulada principal (hay una variante «todos los tics», `defo_todos`, línea 290).
2. **El malestar.** Es la d del decisor: la distancia al equilibrio (`opponent_distance` del motor) del estado imaginado para cada candidato,
   la misma que el cuerpo usa para elegir. Las dos d salen de **la misma imaginación**, la réplica en seco de ese tic (`_dec29`, líneas 85-110),
   no del diario.
3. **La acción del plan.** Si el compromiso anduvo el plan (`obedece`), la d del candidato `_FM_ir` = la receta «ir al destino del plan», añadida
   a los candidatos del cuerpo en esa misma decisión (línea 94-99); si lo sujetó o lo retuvo (`sujeta` / `retenido`), la d de **quedarse quieto**
   (`noop`, línea 267). **La acción propia** es la de menor d entre los candidatos del cuerpo (`min`, línea 262), que es la que el decisor elige.
4. **Cuándo vale cero.** Si lo ejecutado coincide con lo propio, δ = 0 (línea 271); los instantes con δ < 0 (el paso del plan imaginado mejor
   que el mejor propio: 37 en A7h, 8 en A8) entran con su signo. La acumulada del plan es la suma de δ sobre sus instantes con piernas listas (línea 282).

Frase corregida: «en cada instante con un plan vivo y las piernas listas, el malestar que el cuerpo imagina para la acción del plan (ir hacia
su destino, o quedarse quieto cuando el compromiso lo sujeta) menos el que imagina para la acción que habría elegido solo, las dos
imaginadas en ese mismo instante y en la unidad de su malestar; cero cuando coinciden; la acumulada es la suma de esas restas a lo largo del plan.»

## 4 · El «22,6 / 15,7 %» (P6-26)

Banco de P6-26 sobre las 200 escenas del anillo de P6-25. Para cada razonador, se toman **las escenas en que la puerta6 rechazó su plan**
(Haiku: 93 escenas; Sonnet: 83; P6-26:42) y en cada una se prueban todos los planes de «ir y quedarse» posibles (~49 destinos). **22,6 % = 21 de
las 93 escenas rechazadas de Haiku** tienen al menos un plan que pasa; **15,7 % = 13 de las 83 de Sonnet** (P6-26:43). Son porcentajes de
escenas (no de planes) y cada cifra va con el consejero cuyo rechazo define el conjunto. Donde existe un plan que pasa, el del oráculo ya
era uno (12 de 12 y 7 de 7, P6-26:44, 55).

## 5 · Las cinco figuras (`cantera/paper6/figuras/`, 300 ppp; guion `figuras_P6_FIN1.py`; cifras dibujadas en `figuras_P6_FIN1.json`)

| figura | de qué datos sale | qué enseña |
|---|---|---|
| `fig1_es.png` | `P6_7_pareja.json` (A0, A1), `P6_8_pareja.json` (A2), `P6_10_pareja.json` (A3): recuento de tics a ≤ 3 casillas sobre tics con los dos vivos; `P6_7_largas_A0/A1`, `P6_8_largas_A2`, `P6_10_largas_A3.json`: escapadas ≥ 200 tics | a: 79,1 / 59,9 / 48,6 / 78,9 %; b: 3 / 19 / 30 / 1 |
| `fig2_es.png` | `P6_17_final.json`, `anatomia` de la fase 5 (105 vidas vivas en el aviso; A4, A5v, A5h) | a: sobreviven según entren: 0/18, 27/40, 22/35, 10/12; b: según arder, todas las vidas: 15/19, 9/14, 35/72 (solo las que entran: 15/19, 9/11, 35/57) |
| `fig3_es.png` | el diario de la vida del GIF de P6-23 (`P623_t2_A7h_20784561`, asiento 11) y el de su hermano: cuatro instantes (12.609 aceptación, 12.640, 12.760, 12.990) | plan 3 aceptado en el 12.609 hacia (23,28), la criatura dentro del círculo (0 tics ardiendo) hasta que la puerta lo suelta en la reevaluación en el 12.870; aviso 6 en el 12.996 |
| `fig4_es.png` | `P6_24_campo_40.json` (A4, A7h) y `P6_27_campo.json` (A8): tics ardiendo 5-7 por vida viva en el aviso 5 (74 / 77 / 66 vidas) y diferencias por semilla | medianas 233,5 / 146 / 231,5; A7h − A4 media −57,6 (24 mejora, 13 empeora, n 37); A8 − A4 −9,9 (19 / 15, n 34): iguales a lo publicado |
| `fig5_es.png` | `P6_29_planes.json`: plan 13 de `P623_t2_A7h_20994019`, asiento 10 (184 instantes distintos) | a: Δ acumulada hasta 102; b: en los 184 el cuerpo quería ir a por algo; se quedó en 183 y anduvo el plan en 1 |

Estilo: blanco y negro con un solo rojo (#B22222), rótulos en español, pie con la fuente. Nota de la fig. 3: el pie de figura del
borrador dice «se queda hasta el final de la fase»; en esta vida el plan lo soltó la puerta en el 12.870 (126 tics antes del aviso 6) con
el cuerpo dentro, y el cuerpo siguió dentro; el ejemplo publicado de plan cumplido hasta su último tic es el de la fig. 5 (plan 13, 20994019).
