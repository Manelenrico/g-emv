# SELLO P7-22 · Recordar por parecido, en banco

*7-oct-2026. Escrito ANTES de calcular ninguna separación, creencia ni repetición de decisiones. Coste cero: sin partidas ni llamadas.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Cuerpo y congelados sin tocar. Archivos nuevos con sufijo `_P7_22`; una vida por proceso.*

## Lo que se fija antes de medir

- **Recuerdos:** `recuerdos_P7_22.py` → `P7_22_recuerdos.json`: 467 canales de botiquín de las 160 vidas de APRENDE (P7-10 y P7-14b), uno por canal,
  completado o cortado; 184 completados. Contexto (dentro/fuera; golpeada en los 48 anteriores), foto emocional al abrir (dolor F, R, S; positivo;
  distancia total), efecto (completado: lo que subió la vida al cerrar, entre 0 y 50; recursos −1; cortado: 0 en todo), intensidad
  = 1 + min(1, efecto_cuerpo / 50) (abierta en el encargo; fijada aquí: un corte pesa 1, una cura entera 2), día de la serie.
- **s** (parecido emocional = exp(−distancia / s)): la mediana de las distancias euclídeas entre todos los pares de aperturas del diario, en el
  vector de 5 (dolor F, R, S, positivo, d): **s = 0,8304** (108.811 pares; `P7_22_fijado.json`, escrito por `banco_P7_22.py --fija`).
- **Parecido de contexto:** 1 si coincide dentro/fuera, 0,25 si no; × 1 si coincide golpeada/no, 0,5 si no. **Olvido:** 0,95 por día. **Neutro:** peso 1, efecto 0.
- **Lo que se recuerda** al abrir en el día d: los recuerdos de los días anteriores de esa criatura (el cuaderno se escribe al acabar el día).
- **Separación:** probabilidad de que una apertura que se completa tenga la creencia más alta que una que se corta (empates, ½); 0,5 = no separa.
- **«Poco / muy dolorido»** (R4): dolor F al abrir por debajo / por encima de la mediana de las aperturas dentro del círculo: **0,9986**.
- **R3:** «cae por debajo del 25 % del catálogo antes del día 10» = el primer día con una apertura fuera cuya creencia C < 12,5 es anterior al 10,
  y desde el día 10 todas las aperturas fuera tienen creencia C < 12,5. Se evalúa en las 4 criaturas de cada campo (2 series × 2 asientos).
- **R4** se mide en P7-14b (días 11 a 20, 40 vidas), donde la réplica del campo es bit-exacta con el cuaderno que leyó cada día; P7-10 jugó con
  una versión anterior de las piezas del siete y no se replica. Solo cambia la cura imaginada al usar (`heal_imaginado`), con
  efecto = (1 − ignorancia_C) × creencia_vivida_C + ignorancia_C × esperanza, ignorancia_C = 1 / (1 + suma de pesos); las ganas quedan como en el campo.
  «Sigue usando» = en el tic en que el campo eligió `usar_botiquin`, con C también lo elige.

## Las reglas

| | regla | pasa si |
|---|---|---|
| R1 | dentro del círculo, la creencia C al abrir predice si el botiquín se completará | separación ≥ 0,65 en los dos campos |
| R2 | C separa mejor que B dentro del círculo | C − B ≥ 0,03 (en los dos campos) |
| R3 | fuera del círculo, la creencia C cae por debajo del 25 % del catálogo antes del día 10 | en las 4 criaturas de cada campo |
| R4 | repetición de decisiones, días 11 a 20, P7-14b | dentro y poco dolorido, sigue usando ≥ 80 %; dentro y muy dolorido, ≥ 50 % |

## md5 de lo sellado

- `recuerdos_P7_22.py`: `fdfa6b71fccc3080221d15509e47b060`
- `banco_P7_22.py`: `d125f2954350557e6ea50eba5c991953`
- `banco_decide_P7_22.py`: `71ec40987425d55b935793f1c2b4fb81`
- `P7_22_recuerdos.json`: `74396f5d7a5205b8b77b3a3aa416027c`
- `P7_22_fijado.json`: `fd382c670253e18e3611d8d5050a07f0`

Commit del sello: `aa6d99517a6b` (gemv-coworld, paintball).
