# Prompt 166: qué parte del duelo y de la soledad pusimos nosotros y qué parte sale sola

Para la protagonista RG69r+voz («RG69rvoz»): la clase `cuerpo_vr1.RG69V`, que es `RG69V(VC1, RG69)` sobre `cuerpo_valle.Criatura`, con los interruptores del lanzador del v6 (`lanza_experimento_v6.py:33-35`).

**Dos marcas en todo el informe:**
- **[leído]:** sale del código, con fichero y línea.
- **[contado]:** sale de las partidas selladas del v6 (semillas 30161-30200, los cinco mundos), sin jugar nada.

Abreviaturas: `cv` es `cuerpo_valle.py`, `mundo` es `valle/mundo.py`, `A` es `paintball/alma/appraisal_zs_v42_exp.py` (la tabla congelada del siete, importada) y `config` es `config_cuerpo_valle.json`.

## Resumen

| cosa | ¿escrita por nosotros o sale sola? |
|---|---|
| **Cómo se entera de una muerte** | **Escrita.** Solo si lo ve: la ve morir estando a la vista (5 casillas de día, 3 al anochecer, 2 de noche), o ve el cuerpo, que se queda hasta el final del día siguiente. Ni el mundo ni el lanzador se lo dicen de lejos. No lo nota por dejar de verla ni de oírla. [leído] |
| **Cuánto tarda** | **Sale sola** de dónde está. Por la hermana: el 36 % al morir, el 45 % por el cuerpo (mediana de 73 turnos) y el 19 % no se entera. En los 136 casos de A2, 21 no se enteran. Por una vecina: 7 %, 47 % y 46 %. [contado] |
| **Qué filas forman el duelo y en qué dominios** | **Escrito:** tres filas de pérdida, S-DUELO-CUERPO, S-DUELO-RECURSOS y S-DUELO-VINCULO, una por dominio (prompt 90). [leído] |
| **Su fuerza al empezar** | **Mitad escrita, mitad aprendida.** La parte del cuerpo es un peso de nacimiento escrito: 1,38 por la hermana y 0,51 por una vecina (prompts 83 y 84). Recursos y vínculo salen del radar aprendido: por la hermana, unos 0,0 y 0,81. [leído y contado] |
| **Cómo se apaga** | **Escrito.** Baja hacia un suelo de 0,3 × la fuerza del principio (regla del siete, de Manel); la parte de encima se reduce a la mitad cada 600 turnos por la hermana y cada 300 por una vecina (prompts 8 y 31). Los duelos se suman (prompt 53). Tenerla pegada alivia: lo multiplica por 1 − 0,5 × el vínculo (prompt 31). [leído] |
| **Los 600 turnos frente a los 5 días de A4** | **No se contradicen; es la medida.** A4 mide la mitad del duelo entero, con el suelo dentro: eso lleva 1 084 turnos (2,7 días). Además cuenta los días desde la muerte y usa la media de cada día. La curva pura del código, medida como A4, da también 5 días. [leído y contado] |
| **La soledad** | **La fila es escrita y de siempre** (S-SOLEDAD, del siete), la misma que sube cada vez que las hermanas se separan. No hay ninguna regla para cuando la hermana ha muerto. Que se quede alta **sale sola**: solo ver u oír a la hermana pone a cero su cuenta, y las vecinas la alivian solo en parte, según su vínculo. No hace falta saber que ha muerto. [leído] |
| **Las otras filas de la hermana** | **Escrito:** cuando sabe que ha muerto se apagan, cada una con su condición `not pareja_muerta`: estar lejos de ella, tenerla a la vista, su daño, lo que le falta y la voz. Mientras no lo sabe, siguen calculándose con la casilla donde la vio por última vez. La voz de ir a casa calla en el momento de la muerte, lo sepa o no, porque la lee del mundo. [leído y contado] |
| **Buscar a las vecinas** | **No hay ninguna regla escrita para eso.** La única regla escrita para cuando la hermana ha muerto es que siga oyendo a las vecinas (prompt 31): sin ella, dejaba de oír a nadie. El tirón hacia las vecinas **sale de filas de siempre**, escritas para todas y en todo momento (la soledad, el alivio del duelo, tener cerca a las suyas, las llamadas). El taller del prompt 90 ya midió que lo que más sube el tiempo con vecinas tras la muerte es el duelo grande, porque la compañía lo alivia. [leído] |

## Parte 1. Cómo sabe una criatura que su hermana ha muerto

### Lo leído

**El mundo lo dice solo a quien lo ve.**
- `mundo:613-617`: al morir, la muerte se anuncia en «muertes_vistas» a cada criatura viva que está a la vista en ese momento. «A la vista» es la distancia de Chebyshev ≤ `vista()`.
- `mundo:491-494` y `config_valle.json:601`: la vista depende de la fase: 5 casillas por la mañana y por la tarde, 3 al anochecer y 2 de noche.
- `mundo:614` y `mundo:1156-1158`: el cuerpo queda en su casilla. Quien lo tiene a la vista lo recibe en «cadaveres».
- `mundo:713-715` y `config_valle.json:597`: el cuerpo dura hasta el final del día de la muerte más `cadaver_dias_extra` = 1 día.
- Las criaturas muertas no salen en «criaturas» de la observación.

**La criatura lo apunta al verlo, y nada más** (`cv:695-707`):
- `cv:697-698`: si la hermana sale en «muertes_vistas» o en «cadaveres», `pareja_muerta = True` desde ese turno.
- `cv:699-707` (con `duelo_v19`, encendido): cualquier muerte vista, de la hermana o de una vecina, entra en `muertas` con su turno y su peso. Desde ahí empieza su duelo.
- No hay otro camino.

**Lo que no le dice nada:**
- **Dejar de verla o de oírla** solo hace crecer `sin_compania`, que es la soledad (`cv:713-719`), y baja el vínculo hacia su suelo (`cv:1047-1049`). Nunca pone `pareja_muerta`.
- **El lanzador de la voz** sí lee del mundo si la hermana está muerta, aunque esté lejos: `lanza_vc1.py:27` llena `cuerpo_vc1.ESTADO`. Pero solo lo usa para decidir si la voz de ir a casa puede sonar (`cuerpo_vc1.py:75-79`, `not her[2]`). No toca `pareja_muerta` ni las filas.
- **El lanzador del v6** no pasa a la criatura nada sobre las muertes (`lanza_experimento_v6.py`, buscado).

**Una vecina:** el mismo camino (`cv:699-707`). Su duelo es más corto, con semivida de 300 turnos (`config:228`).

### Lo contado

Programa: `sabe_muerte_166.py`. Salida: `salida/sabe_muerte_166.md` y `.json`. Para cada muerte y cada criatura viva ese turno hay tres cuentas:
- **a, del mundo:** si estaba a la vista al morir, o el primer turno en que tiene el cuerpo a la vista mientras está puesto;
- **b, de sus filas:** el primer turno en que su duelo deja de ser 0. Solo vale para las que no tenían duelo antes, porque el duelo nunca vuelve a 0 por su suelo;
- **c, solo para la hermana:** `S-COMPANIA` solo se calcula mientras no sabe que ha muerto (`cv:1732`). Si sale mayor que 0 después de un turno, todavía no lo sabía.

**Las tres casan:**
- Cuando a y b dicen que se entera, el turno coincide (a 1 turno o menos) en 67 de 67.
- Ninguna hermana tiene `S-COMPANIA` > 0 después del turno en que, según el mundo, lo supo.
- Al principio dos casos parecían contradecirse. Eran un fallo de mi cuenta b: otra criatura había muerto antes y su cuerpo seguía puesto, y el duelo que subía era por ella. Ahora esos casos se apartan como «dudosas».

Muertes en las 200 partidas: 213; parejas (muerta, criatura viva en ese turno): 1236.

#### Tabla 1. Cómo se entera, según la regla del mundo (cuenta a)

| quién muere, para ella | parejas | a la vista al morir | por ver el cuerpo después | no lo ve (ni al morir ni el cuerpo) | turnos hasta ver el cuerpo |
|---|---|---|---|---|---|
| su hermana | 172 | 62 (36,0 %) | 78 (45,3 %) | 32 (18,6 %) | mediana 73 (cuartiles 18–147; máx. 550) |
| una vecina | 1064 | 72 (6,8 %) | 498 (46,8 %) | 494 (46,4 %) | mediana 95 (cuartiles 39–198; máx. 675) |
| su hermana, los 136 casos de A2 | 136 | 51 (37,5 %) | 64 (47,1 %) | 21 (15,4 %) | mediana 74 (cuartiles 19–167; máx. 550) |

#### Tabla 2. Cuándo aparece su duelo en sus filas (cuenta b; solo las que no tenían duelo antes)

| quién muere, para ella | parejas sin duelo antes | sube su duelo | turnos desde la muerte | no sube antes de que acabe o muera | hay otra muerte antes de que suba | sube, pero con el cuerpo de otra anterior aún puesto (dudosa) |
|---|---|---|---|---|---|---|
| su hermana | 113 | 67 (59,3 %) | mediana 15 (cuartiles 1–77; máx. 421) | 8 (7,1 %) | 23 | 15 |
| una vecina | 722 | 217 (30,1 %) | mediana 78 (cuartiles 18–171; máx. 532) | 147 (20,4 %) | 252 | 106 |
| su hermana, los 136 casos de A2 | 89 | 55 (61,8 %) | mediana 15 (cuartiles 1–96; máx. 421) | 4 (4,5 %) | 17 | 13 |

#### Tabla 3. Las dos cuentas juntas (solo la hermana, sin duelo antes)

| según el mundo \ según sus filas | sube | no sube | otra muerte antes | sube, dudosa |
|---|---|---|---|---|
| al_morir | 27 | 0 | 0 | 6 |
| el_cuerpo | 40 | 0 | 11 | 7 |
| no_lo_ve | 0 | 8 | 12 | 2 |

Cuando las dos dicen que se entera: el turno coincide (a 1 turno o menos) en 67 de 67.

Hermanas que no se enteran nunca (no lo ven y su duelo no sube hasta que acaba la partida o mueren): 8: sequia 30170, C1 (muere C2 el turno 7916, día 19, a 10 casillas, noche); sequia 30194, C2 (muere C1 el turno 13217, día 33, a 27 casillas, mañana); sequia_dura 30171, D1 (muere D2 el turno 5050, día 12, a 6 casillas, anochecer); sequia_dura 30196, D1 (muere D2 el turno 5466, día 13, a 8 casillas, anochecer); bestias_crian 30179, C1 (muere C2 el turno 15078, día 37, a 25 casillas, anochecer); bestias_crian 30181, A2 (muere A1 el turno 12310, día 30, a 24 casillas, noche); bestias_crian 30193, A2 (muere A1 el turno 12012, día 30, a 8 casillas, mañana); bestias_crian 30199, B2 (muere B1 el turno 13903, día 34, a 14 casillas, noche).

#### Tabla 3b. La hermana: S-COMPANIA después de la muerte (cuenta c), según la regla del mundo

| según el mundo | parejas | con S-COMPANIA > 0 después de saberlo (contradice) | sin S-COMPANIA > 0 en los últimos 400 turnos que vive | con S-COMPANIA > 0 en los últimos 400 turnos que vive (sigue sin saberlo) |
|---|---|---|---|---|
| al_morir | 62 | 0 | 62 | 0 |
| el_cuerpo | 78 | 0 | 70 | 8 |
| no_lo_ve | 32 | 0 | 4 | 28 |

Las que según el mundo no lo ven pero su duelo sube: sequia_dura 30183, B2 (muere B1 el turno 5187, sube en 5203, a 20 casillas al morir; dudosa); sequia_dura 30196, C2 (muere C1 el turno 5002, sube en 5383, a 28 casillas al morir; dudosa).

#### Tabla 4. A qué distancia estaba la hermana viva cuando murió la otra (Chebyshev), y en qué fase

| fase (vista) | muertes de hermana | a la vista al morir | por el cuerpo | no lo ve | distancia: mediana · máx. |
|---|---|---|---|---|---|
| mañana (5) | 63 | 18 | 36 | 9 | 8 · 27 |
| tarde (5) | 29 | 11 | 13 | 5 | 12 · 28 |
| anochecer (3) | 14 | 2 | 8 | 4 | 10 · 28 |
| noche (2) | 66 | 31 | 21 | 14 | 5 · 26 |

**Cómo leer la tabla 3b.** En «por el cuerpo», 8 hermanas tienen `S-COMPANIA` > 0 en sus últimos 400 turnos de vida. No es una contradicción: se enteran tarde y viven poco después; el «contradice» es 0 en todas.

**Las que no lo ven:**
- 28 de 32 siguen con `S-COMPANIA` > 0 en sus últimos 400 turnos: siguen sin saberlo al final.
- 8 de ellas, sin duelo de antes, lo confirman también con las filas: no se enteran nunca.

## Parte 2. El duelo

### Lo leído

**Las filas.** Son tres filas de pérdida, una por dominio: S-DUELO-CUERPO, S-DUELO-RECURSOS y S-DUELO-VINCULO.
- `cv:1543-1548` (`_pon_duelo3`): reparto puro, (1, 0, 0), (0, 1, 0) y (0, 0, 1).
- El reparto fractal del prompt 103 (`fractal_v51`) está apagado en la protagonista: no está entre sus interruptores (`banco_v7.py:310` y `lanza_experimento_v6.py:33`).
- Se ponen en cada foto (`cv:1657-1660`, con `duelo_v19` y `duelo_v45`).

**La fuerza al empezar** (`cv:703-705` y `cv:1530-1534`, `lo_que_era`). Es lo que la muerta era para ella:
- **cuerpo:** lo aprendido del radar, más `valor_vida` = familia × cuesta(1) (`cv:2043-2052`). Familia es un peso de nacimiento: 0,9864 por la hermana y 0,3675 por una vecina (`config:8`, prompt 84, «los pesos de vínculo que tenía RG32r»). No se aprende (prompt 83, `cv:406-409`: «Hamilton, provisional»);
- **recursos:** lo aprendido del radar (`cv:1813-1816`);
- **vínculo:** lo aprendido del radar.

Las tres se multiplican por el alivio de la compañía (`cv:1325-1334`): pegada (a 1 casilla o menos) a una de las suyas, × (1 − (1 − MEDICINA_ATEN) × su vínculo). MEDICINA_ATEN = 0,5 (`A:333`).

**Cómo se apaga.** `cv:68-70`: duelo(dt) = (DUELO_SUELO + (1 − DUELO_SUELO) × 0,5^(dt / semivida)) × w, contado desde que lo sabe.
- **El suelo:** DUELO_SUELO = 0,3 (`A:335`, «[Manel] nunca baja de 0.3 x B»).
- **La semivida:** 600 turnos por la hermana (`config:12`) y 300 por una vecina (`config:228`); se elige en `cv:1187-1188`.
- **Lo que significa:** la parte por encima del suelo baja a la mitad cada 600 turnos. Lo que «dura» (`cv:1183-1185`, `config:229`) es hasta que esa parte baja al 10 %: 600 × log2(10) ≈ 1 993 turnos, unos 5 días. Después queda el suelo para siempre.
- **Varias muertes:** sus duelos se suman (`cv:1193-1195` y `cv:1541`, con `duelo_suma_v15`).

**De qué prompt viene cada pieza, y su motivo escrito:**
- **El suelo y la forma de la curva** son del siete (PROMPT_12, «sellada por Manel»). Motivo escrito en `A:1118-1121`: «una fuerza constante es invisible para el gradiente; la pendiente devuelve al animal a la vida».
- **Los 600 turnos:** prompt 8 (`constantes_tiempo.md:33`, `:109` y `:118-127`). Manel pidió «que dure unos 5 días = 2000 turnos». Con el suelo, eso es una semivida de unos 600: la parte que se apaga baja al 10 % a los 2 000 turnos.
- **El duelo por una vecina, sus 300 turnos y el alivio de la compañía:** prompt 31 (`cv:277-279` y la nota de `config:228-230`). Motivo escrito: «la tristeza del 24 de octubre, con piezas que ya hay». Los números 300 y 0,1 son propuestos por mí en su momento, y así lo dice la nota.
- **Que los duelos se sumen:** prompt 53 (`cv:322-324`). Motivo escrito: «como el hambre (antes: el mayor)».
- **Las tres filas desde el radar:** prompt 90 (`cv:446-447` e `informe_imaginar_v1.md:77-97`). Lo escrito dice qué es: «lo que pierde cuando muere una de las suyas es lo que era para ella en cuerpo, recursos y vínculo según el radar aprendido, más lo que vale por ser hermana o vecina». No he encontrado otra razón escrita aparte de esa. El informe del 90 ya decía que la mayor parte es el cuerpo, y que ahí casi todo es el peso de nacimiento.

### Lo contado: la fuerza al empezar

Programa: `fuerza_duelo_166.py`. Son las filas apuntadas en el primer turno en que sube, con el alivio de ese turno dentro.

Lo de nacimiento (sin aprender): valor_vida = familia × cuesta(1) = hermana 0.9864 × 1,400 = 1,381; vecina 0.3675 × 1,400 = 0,514 (va a la fila del cuerpo).

| muerta | casos | S-DUELO-CUERPO: mediana (cuartiles) | S-DUELO-RECURSOS | S-DUELO-VINCULO | las tres juntas |
|---|---|---|---|---|---|
| su hermana | 67 | 1,381 (1,381–1,385) | 0,000 (0,000–0,067) | 0,814 (0,780–0,852) | 2,223 (2,166–2,275) |
| una vecina | 217 | 0,514 (0,434–0,514) | 0,000 (0,000–0,049) | 0,115 (0,074–0,158) | 0,638 (0,549–0,707) |

### Por qué A4 dice 5 días y el código dice 600 turnos

**Qué mide A4, exactamente** (`duelo_soledad_v6.py:76-96`; la cifra está en `informe_experimento_v6.md:173-174`):
- el duelo es la suma de las tres filas;
- se toma la media de cada día, solo en sus turnos despierta;
- «antes» es la media de los 5 días antes de la muerte, y el pico es el peor de los 5 días después;
- «a la mitad» es el primer día después del pico cuya media es ≤ antes + 0,5 × (pico − antes);
- esos días se cuentan **desde el día de la muerte**.

**Por qué tarda más** [leído y calculado]:
1. **A4 pide la mitad del duelo entero, no la de la parte que se apaga.** Con el suelo de 0,3, el duelo entero baja a la mitad de su valor inicial cuando 0,3 + 0,7 × 0,5^(dt/600) = 0,5, es decir, a dt = 600 × log2(3,5) ≈ 1 084 turnos: 2,7 días, no 600 turnos.
2. **Cuenta desde la muerte, en días enteros,** y la mitad tiene que caer en la media de un día entero.
3. **El pico es el peor día,** casi siempre el día siguiente a la muerte (mediana 1), cuando ya ha bajado algo.

**La prueba** [contado]. Programa: `duelo_a4_166.py`. Es la curva pura del código (sin compañía, sin otras muertes, w = 1), medida como A4, con el turno real en que se entera y los turnos despierta reales de cada caso:

La regla: la parte del duelo por encima del suelo baja a la mitad cada 600 turnos; el duelo entero (suelo 0.3 incluido) baja a la mitad de su valor al enterarse a los 1084 turnos (2.71 días).

Casos de A2: 136. Se enteran (según el mundo): 115; no lo ven: 21.

| la cuenta de A4, sobre | casos con cifra | «a la mitad»: mediana de días | días: cuartiles |
|---|---|---|---|
| A4 de verdad (las filas apuntadas en el v6) | 109 | 5 | 5–7 |
| la curva pura, con el turno en que se entera (desde la muerte, turnos despierta) | 106 | 5,0 | 5–6 |
| · la misma, sabiéndolo en el turno de la muerte (todos los casos) | 126 | 5,0 | 5–6 |
| · la misma, contando desde el pico | 106 | 4,0 | 4–5 |
| · la misma, con todos los turnos del día | 106 | 6,0 | 5–6 |

Casos con las dos cifras (A4 de verdad y la curva pura): 103; la misma cifra en 48; A4 de verdad más tarde en 37, antes en 18.

Los 21 casos que no lo ven: A4 de verdad dice 4: 3, 5: 1, 7: 2, None: 10, no_sube: 5.

**Lo que dice la tabla:**
- **La curva sola ya da la mediana de 5 días.** La diferencia con los 600 turnos es la medida, no algo que añada el registro.
- **Lo que tarda en enterarse apenas cambia la mediana:** sabiéndolo en el turno de la muerte, también 5.
- **Caso a caso, A4 de verdad y la curva no siempre coinciden.** Sale lo mismo en 48 de 103; A4 de verdad es más tarde en 37 y antes en 18. Eso sale de lo que la curva pura no lleva: el alivio de la compañía y los duelos de otras muertes, que se suman.
- **Un detalle de A4:** su «duelo» suma todos los duelos, no solo el de la hermana. Por eso algunos de los 21 casos que no se enteran tienen cifra en A4.

## Parte 3. La soledad

### Lo leído

**La fila: S-SOLEDAD, una sola.**
- **La fórmula:** `cv:164-166`, (1 − P) × SOLEDAD_TECHO × min(1, sin_compania / 200).
- **Los números:** SOLEDAD_TECHO = 0,5 (`A:322`) y la rampa, 200 turnos (`config:13`).
- **Su reparto:** (0,1, 0,1, 0,8), de Manel (`A:430`).
- **De dónde viene:** es la fila del siete (`A:1092-1097`), traída al valle desde el principio. La rampa de unos 200 turnos, medio día, se fijó en el prompt 8 (`constantes_tiempo.md:110`).

**Qué la enciende.** `sin_compania` (`cv:713-719`):
- vuelve a 0 cuando ve a la hermana, o la ha oído hace 7 turnos o menos (`config:15`);
- si no, sube 1 por turno;
- solo la hermana la pone a 0.

**Qué la alivia.** P (`cv:1727-1731`):
- vale 1 si ve a la hermana, y 0,5 si la ha oído hace poco;
- con las vecinas (prompt 28), P es el mayor de los vínculos de las vecinas que tiene a la vista, que van de 0,1 a 0,5 (`config:211`);
- una vecina a la vista no pone a cero la cuenta; solo la multiplica por (1 − su vínculo).

**Existía antes y aparte de la muerte.** Es la misma fila que sube cada vez que las hermanas se separan más de medio día. En A4, las que conservan a la hermana también la tienen: 0,016 → 0,034 (`duelo_soledad_v6.md:40`).

**No hay ninguna regla escrita para cuando la hermana ha muerto.**
- Tras la muerte nunca vuelve a ver ni a oír a la hermana. Así que `sin_compania` no vuelve a 0 y S-SOLEDAD se queda en 0,5 × (1 − P) para siempre: entre 0,25 y 0,45 con una vecina a la vista, y 0,5 sin ninguna.
- Esto no depende de saber que ha muerto: le pasa igual a la que no se entera.
- A4 lo ve así: la soledad sube a 0,43-0,48 y solo baja a la mitad en 34 de 135 casos (`informe_experimento_v6.md:175`).

**Qué pasa con las otras filas que nombran a la hermana, cuando sabe que ha muerto** (`pareja_muerta`):

| fila | qué hace | tras saberlo | dónde |
|---|---|---|---|
| S-COMPANIA | estar lejos de ella (más de 7 pasos) | no se calcula: 0 | `cv:1732-1738` |
| V-VINCULO | tenerla a la vista | no se calcula | `cv:2277` |
| V-RADAR-… (tenerla cerca) y P-RADAR-… (imaginar perderla) | lo que vale tenerla o perderla | la hermana sale de la lista (las vecinas siguen) | `cv:1958` y `cv:1981` |
| S-DANO-PAREJA (su herida) | verla herida duele, por su vínculo | la parte de la hermana no se calcula (la de las vecinas heridas o de duelo sigue) | `cv:1664-1672`, `cv:1714-1725` |
| R-HERMANO-FALTA y S-PROVISION (lo que le falta) | darle comida o medicina | la parte de la hermana no se calcula | `cv:1664-1685` |
| el alivio del duelo | estar pegada a ella | ya no cuenta | `cv:1328` |
| la voz de ir a casa | imaginarla en casa al final de la foto; sonar para ella | no se oye ni se da | `cuerpo_vc1.py:55` y `:78` |

**La voz de ir a casa calla desde el turno de la muerte, lo sepa o no.** `cuerpo_vc1.py:78` pide la hermana viva según el mundo (`ESTADO`, del lanzador), y una muerta no da voces.

**Mientras no lo sabe, todas siguen como si viviera, con la casilla donde la vio por última vez** (`pareja_pos`). Lo dice el código, y lo confirma la cuenta c de la parte 1: `S-COMPANIA` sigue mayor que cero en 28 de las 32 que no lo ven.

## Parte 4. Buscar a las vecinas

### Lo leído

**No hay ninguna regla escrita que la lleve hacia las vecinas cuando pierde a la hermana.**
- **La única regla escrita para «la hermana ha muerto»** es `oye_sin_hermana` (prompt 31, `cv:276`, `cv:530` y `cv:710`). Con la hermana muerta sigue oyendo y respondiendo a las vecinas. Sin ella, dejaba de oír a nadie. No añade un tirón: quita un corte.
- **El escalón del vínculo con las vecinas no cambia** (`cv:927-929`). El vínculo con cada vecina sube igual que siempre, al verla (1/65 por turno) y al dar o recibir (`cv:1033-1060`).
- **El «plato» S-JUNTAS** (estar con las suyas) está apagado en la protagonista: `dos_platos` no está entre sus interruptores (`cv:285-286` y `cv:1726`).

**El tirón sale de filas de siempre, escritas para todas y en todo momento.** Tras la muerte de la hermana, las vecinas son las únicas que quedan en ellas:
1. **La soledad** (prompt 28, `cv:1727-1730`): solo una vecina a la vista la alivia, según su vínculo. Y tras la muerte la soledad ya no baja de otra forma.
2. **El alivio del duelo** (prompt 31, `cv:1325-1334`, aplicado en `cv:1660`): pegada a una vecina, el duelo × (1 − 0,5 × su vínculo). Con un duelo grande, eso pesa mucho. El taller del prompt 90 lo midió pieza a pieza: el duelo del radar sube el tiempo con vecinas los cinco días siguientes del 24 % al 40 %, «porque la compañía alivia un duelo más grande» (`informe_imaginar_v1.md:158-159`).
3. **Tener cerca a las suyas** (prompts 79 y 81, `cv:1975-1993`): V-RADAR-CUERPO, -RECURSOS y -VINCULO por cada vecina a la vista.
4. **Las llamadas** (prompt 57, `cv:1228-1262`): la foto de una llamada imagina que viene alguien y pone S-SOLEDAD a 0 (`cv:1252`). Con la soledad alta para siempre, llamar a las vecinas sale mejor. En el prompt 165 las llamadas suben unas 30 al día tras la muerte.
5. **La bestia, a suertes entre las que están juntas** (prompt 86, `cv:1741`): estar con otras reparte el peligro.
6. **El otro lado** (prompts 31 y 54, `cv:1300-1317` y `cv:1721-1725`): las vecinas que oyen su sonido de tristeza lo sienten como su herida (S-DANO-PAREJA), por su vínculo, y estar a su lado lo alivia. Así ellas también van hacia ella.

**Ninguna de las seis mira si la hermana ha muerto.** Antes de la muerte pesan menos, porque la hermana también cuenta y es la que más alivia (vínculo de 0,5 a 1).

## Lo que tuve que decidir

- **Lo que se entiende por «se entera»:** que `pareja_muerta` se ponga a True, o que la muerta entre en `muertas` en el caso de una vecina. Es lo único que el código usa.
- **Cuenta a, del mundo:** la casilla de cada criatura es la de su línea en `mundo.jsonl.gz`, y puede ir un turno desfasada de lo que mira el mundo. Por eso la comprobé con las cuentas b y c.
- **Cuenta b:** solo vale para las que no tenían duelo antes. Se aparta si hay otra muerte antes de que suba, o si el cuerpo de otra anterior sigue puesto.
- **La explicación de A4** usa la curva pura (w = 1, sin compañía, sin otras muertes), para aislar la regla.
- **Un error mío, ya corregido:** la primera versión de la cuenta b daba dos casos de «no lo ve pero su duelo sube». Eran por un cuerpo anterior todavía puesto; los he apartado como «dudosas».

## Lo que no se pudo

- **El motivo del prompt 90:** no he encontrado otra razón escrita, aparte de lo que dicen el comentario y el informe. Lo cito tal cual.

## Gasto y procesos

**Gasto:**
- créditos de la plataforma: 0 (no se juega nada);
- dólares de la consola de Anthropic: 0 (ninguna llamada).

**Ficheros nuevos:**
- `sabe_muerte_166.py`, `duelo_a4_166.py` y `fuerza_duelo_166.py`;
- sus salidas en `salida/`;
- este informe.

**Ficheros existentes:** no se ha editado ninguno, y `cantera/paper9` no se ha tocado.
