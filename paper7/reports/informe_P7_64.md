# P7-64 · Banco (coste cero): ¿dónde tiene agarre la razón?

*14-oct-2026. Sobre todas las invitaciones de P7-56 (CON_RAZON) y de las series 1-3 de P7-61 (días 1-7, días 8-20 honestas, y la falsa aparte): 1587 oportunidades.
`banco_P7_64.py` → `P7_64_banco.json` (y `P7_64_filas.json`, una fila por oportunidad); `escribe_informe_P7_64.py` (este informe; ninguna cifra a mano). `motor/model.py` intacto.*

**Definiciones.** Oportunidad = una invitación cargada en una vida-día que se activó al menos una vez; aceptada = al menos un `P7_54_aceptada` suyo. El momento = su primer tic activa (el único
que se registra): vida en tramos; amenaza = rival a ≤ 4 casillas, golpe en los 48 tics anteriores o calma=PELIGRO con vida ≥ 30; peso de la alternativa = d(candidato invitado) − d(elegido)
en la radiografía de ese tic (el cuerpo elige el menor d; 0 = el invitado era el elegido), medible solo para acciones con candidato de nombre único (para COGER_* no: «sin medida»).
**Límite declarado**: casi todas las invitaciones se activan por primera vez al empezar el día, con la vida llena; el momento de la primera activación dice poco de la urgencia en la que
luego se acepta o no.

## 1 · Aceptación por oportunidad, por acción del menú

| acción | P7-56 | P7-61 d1-7 | P7-61 d8-20 | honestas, todo | P7-61 falsa |
|---|---|---|---|---|---|
| ACERCARSE_HERMANA | 72 % de 85 | 82 % de 55 | 76 % de 127 | 76 % de 267 | — |
| COGER_BOTIQUIN | 74 % de 74 | 80 % de 46 | 84 % de 119 | 80 % de 239 | — |
| COGER_CAMUFLAJE | 86 % de 7 | 100 % de 1 | 80 % de 5 | 85 % de 13 | — |
| COGER_RACION | 71 % de 49 | 60 % de 30 | 76 % de 54 | 71 % de 133 | — |
| COGER_RED | 57 % de 7 | 67 % de 3 | 29 % de 7 | 47 % de 17 | — |
| DAR_BOTIQUIN_HERMANA | 4 % de 28 | 0 % de 22 | 3 % de 36 | 2 % de 86 | — |
| EMPUNAR_RED | 0 % de 16 | — | — | 0 % de 16 | — |
| PONERSE_CAMUFLAJE | 0 % de 34 | 0 % de 23 | 0 % de 54 | 0 % de 111 | — |
| QUEDARSE_QUIETA | 57 % de 30 | 47 % de 17 | 70 % de 47 | 62 % de 94 | — |
| USAR_BOTIQUIN | 13 % de 86 | 18 % de 63 | 15 % de 131 | 15 % de 280 | 32 % de 117 |
| USAR_RACION | 7 % de 68 | 7 % de 44 | 10 % de 102 | 8 % de 214 | — |

Agarre alto (≥ 60 % en todas las honestas): ACERCARSE_HERMANA, COGER_BOTIQUIN, COGER_RACION, QUEDARSE_QUIETA. Agarre casi nulo: usar el botiquín o la ración (7 %-18 %), dar el botiquín a la hermana,
ponerse el camuflaje, empuñar la red. **La razón mueve al cuerpo a ir y a coger, no a gastar**: lo que se gasta (usar, dar) lo decide el cuerpo por su cuenta.

## 2 · La misma fracción según el momento (honestas, todo)

| | <30 | 30-60 | 60-90 | >=90 |
|---|---|---|---|---|
| vida al activarse | 7 % de 30 | 18 % de 34 | 10 % de 86 | 46 % de 1320 |

| | amenaza | sin amenaza |
|---|---|---|
| todas las honestas | 41 % de 751 | 45 % de 719 |
| USAR_BOTIQUIN | 20 % de 182 | 5 % de 98 |
| USAR_RACION | 15 % de 91 | 3 % de 123 |
| QUEDARSE_QUIETA | 46 % de 54 | 82 % de 40 |
| ACERCARSE_HERMANA | 76 % de 163 | 76 % de 104 |
| COGER_BOTIQUIN | 80 % de 93 | 81 % de 146 |

| peso de la alternativa elegida | 0 (elegida) | (0, 0,02] | (0,02, 0,1] | > 0,1 | sin medida |
|---|---|---|---|---|---|
| honestas | 61 % de 61 | 50 % de 14 | 76 % de 118 | 56 % de 126 | 37 % de 1151 |

La amenaza sube el agarre de usar el botiquín o la ración y baja el de quedarse quieta; la vida y el peso de la alternativa, medidos en la primera activación, apenas separan (límite de
arriba). La falsa de P7-61 (botiquín en amenaza) tuvo 32 % de agarre, frente a 15 % de las honestas de usar el botiquín.

## 3 · Las invitaciones con más agarre y dónde

| acción · calma · anillo · hermana | oportunidades | aceptación | activación por carga | evaluaciones por oportunidad | vida media al activarse | en amenaza |
|---|---:|---:|---:|---:|---:|---:|
| QUEDARSE_QUIETA · CALMA · DENTRO · CERCA | 28 | 93 % | 82 % | 12,79 | 99,1 | 11 % |
| COGER_BOTIQUIN · CALMA · DENTRO · CUALQUIERA | 57 | 90 % | 97 % | 6,61 | 100,0 | 23 % |
| ACERCARSE_HERMANA · CUALQUIERA · DENTRO · LEJOS | 27 | 89 % | 100 % | 6,59 | 97,9 | 22 % |
| COGER_BOTIQUIN · CUALQUIERA · DENTRO · CUALQUIERA | 18 | 89 % | 100 % | 10,06 | 100,0 | 11 % |
| ACERCARSE_HERMANA · PELIGRO · CUALQUIERA · LEJOS | 44 | 84 % | 100 % | 2,82 | 99,6 | 100 % |
| ACERCARSE_HERMANA · CUALQUIERA · CUALQUIERA · LEJOS | 17 | 82 % | 100 % | 5,94 | 100,0 | 24 % |
| COGER_RACION · CALMA · DENTRO · CUALQUIERA | 42 | 79 % | 98 % | 3,05 | 100,0 | 17 % |
| ACERCARSE_HERMANA · PELIGRO · DENTRO · LEJOS | 81 | 78 % | 98 % | 2,69 | 99,9 | 100 % |
| COGER_BOTIQUIN · CALMA · DENTRO · CERCA | 100 | 77 % | 99 % | 5,48 | 99,4 | 30 % |
| ACERCARSE_HERMANA · CALMA · DENTRO · LEJOS | 69 | 74 % | 100 % | 3,43 | 100,0 | 19 % |
| COGER_BOTIQUIN · PELIGRO · DENTRO · CERCA | 28 | 68 % | 88 % | 3,96 | 98,9 | 100 % |
| COGER_RACION · CALMA · DENTRO · CERCA | 55 | 64 % | 96 % | 2,62 | 100,0 | 34 % |

**Evaluaciones esperadas por serie** si la mentira se carga cada noche en las 3 hermanas que mienten (2 de MIENTEN_DOS + la valiente de MIENTE_UNA) de los días 8-20 = 39 vidas-día ×
activación por carga × evaluaciones por oportunidad (estimadas de las honestas con la misma acción y situación; las evaluaciones por oportunidad cuentan las aceptaciones repetidas del día):

| candidata | cargadas | activación | aceptación | evaluaciones / oportunidad | **evaluaciones por serie** |
|---|---:|---:|---:|---:|---:|
| ACERCARSE_HERMANA con peligro (calma=PELIGRO) | 168 | 81 % | 74 % | 2,51 | **79,4** |
| QUEDARSE_QUIETA con peligro (calma=PELIGRO) | 145 | 34 % | 45 % | 8,45 | **111,4** |
| QUEDARSE_QUIETA (cualquier situacion) | 219 | 43 % | 62 % | 9,96 | **166,7** |
| COGER_BOTIQUIN (cualquier situacion) | 261 | 92 % | 80 % | 5,92 | **211,3** |
| COGER_BOTIQUIN con peligro (calma=PELIGRO) | 64 | 70 % | 73 % | 3,33 | **91,4** |
| USAR_RACION (referencia: la falsa de P7-63) | 286 | 75 % | 8 % | 0,16 | **4,6** |

La referencia lo confirma: una falsa sobre usar la ración se evaluaría unas 4,6 veces por serie (en local: 1 de 18 vidas-día). 

**Candidatas a mentira dañina y comprobable** (propuesta para la mesa; ninguna decidida):

1. **«Acércate a tu hermana cuando hay peligro: estar juntas te cura (+20 de vida)»** — ACERCARSE_HERMANA, calma=PELIGRO, cuerpo +20. Agarre 74 %, unas
   **79 evaluaciones por serie**. Dañina: lleva al cuerpo a moverse expuesto en peligro. Comprobable: el juicio de P7-54 mira el cambio de vida en 240 tics;
   en peligro casi nunca sube 10 o más (la mitad de lo prometido). Ojo: acercarse no tiene «cosa», así que no hay contraste con lo contado por la hermana (solo lo vivido).
2. **«Quédate quieta cuando hay peligro: así no te ven (+15 de vida)»** — QUEDARSE_QUIETA, calma=PELIGRO, cuerpo +15. Agarre 45 % (menor en amenaza), unas
   **111 evaluaciones por serie** (se acepta muchas veces al día). Dañina: quieta y con rival cerca, recibe golpes. Comprobable: 240 tics de vida.
3. **«Coge el botiquín aunque haya un rival cerca: al cogerlo ya cura (+30)»** — COGER_BOTIQUIN, calma=PELIGRO, cuerpo +30. Agarre 73 %, unas
   **91 evaluaciones por serie**. Dañina: ir a por el botiquín junto al rival. Comprobable: coger da 0 en el cuerpo (la huella de coger), siempre falla;
   tiene «cosa» (el botiquín), así que entra el contraste con lo contado (en la misma situación, con la amenaza que ya viaja desde P7-62).

Las tres alcanzarían las 48 evaluaciones en la primera serie. Advertencias: son estimaciones sobre las honestas (la falsa se cargaría cada noche y su texto puede cambiar el agarre);
las de acercarse y quedarse quieta se juzgan por la ventana de 240 tics de P7-54 (cualquier cosa que pase en esos 240 tics cuenta), no por una huella.

## El humo de P7-63 (datos guardados, fuera de resultados)

Las 3 partidas del humo se completaron (s1 d1 MIENTEN_DOS, s1 d1 MIENTE_UNA, s1 d2 MIENTEN_DOS); diarios `P763_*`, estado `P7_63_estado.json`. El humo **no pasó**: p95 máximo 24,95 ms ≥ 20 (la guarda dura no saltó). El campo ya estaba en pausa (addendum 1 del sello de P7-63).

## Gasto

- Plataforma: el humo de P7-63, 3 partidas (créditos: hasta 3). P7-64: 0.
- Consola de Anthropic: la razón del humo de P7-63, 0,11 $. P7-64: 0 $.
