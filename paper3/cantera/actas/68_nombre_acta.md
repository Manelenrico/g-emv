# Acta — EL NOMBRE DEL AGRESOR (v36) · BANCO VERDE

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_68_el_nombre_del_agresor.md` · Banco + forense,
**coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**.
- **v36 = v35 + parte v2 + certificación por identidad** (`parte.py
  562b90d5…`, `appraisal_zs.py 160e53a2…`). Interruptor `IDENTIDAD_ON`
  (False = v35 bit a bit).
- C y E salen de los diarios ya pagados del 64 y 66. **Ninguna imagen,
  ningún submit.**

---

# A · EL PARTE v2

```
E1 P<slot> t<tick> x,y h<hp> v<0|1> b<n> a<0|1>[ s<asiento>][ ax,ay]
```

El **asiento** del agresor va SIEMPRE que hay agresor: la hermana lo conoce
con **certeza total** —se lo dice su propio `damage_taken.source`— aunque ya
no lo vea. La posición sigue viajando solo si lo tiene a la vista. **39
caracteres** en el peor caso medido, ASCII limpio, cadencia 48 ≥ 24 (jamás
`rate_limited`), y **compatible hacia atrás**: un parte v1 (sin asiento) se
parsea igual y cae al respaldo por posición. La basura con marca válida se
rechaza.

# B · LA CERTIFICACIÓN POR IDENTIDAD

Agresor de mi hermana = **el asiento que dice su parte fresco, si ese asiento
está visible ahora — donde esté**. La posición queda de respaldo (partes v1).
Caducidad igual (96 tics / `a=0`). **El nombre identifica; no persigue**: sin
verlo, no hay candidato; y C1 sigue: si el parte nombrara a la propia
hermana, se descarta.

# C · LA VARA DE OCASIÓN, REESCRITA (el agresor VISIBLE AHORA)

| tanda | vara vieja (posición del parte) | **vara nueva (visible ahora)** |
|---|---|---|
| **64** (v34) | 5/8 = 62 % | **7/9 = 78 %** |
| **66** (v35) | 6/12 = 50 % | **12/13 = 92 %** |
| **acumulado** | — | **19/22 = 86 %** |

El 67 dijo que 62 % y 50 % eran **cotas inferiores**; medido con la posición
real y visible del cazador, **la manada defiende el 86 % de las veces que
puede**. La diferencia no era conducta: era la vara, que preguntaba por una
foto de hasta 96 tics.

# D · LAS PRUEBAS (`alma/verifica_68.py`, VERDE)

| prueba | sello | resultado |
|---|---|---|
| **A formato** | sellado | **VERDE** — 39 chars, ASCII limpio, eco parseado, v1 compatible, basura rechazada, cadencia ≥24 |
| **P1 LAS SEIS** | sellado | **VERDE — cambian 3 de 6**: las tres en que el cazador era visible y a alcance (el parte traía su posición vieja: la certificación por posición no encontraba a nadie, la de identidad sí). Las otras tres **siguen sin candidato**: una porque no lo veía, dos porque estaba realmente a 2 con espada. **No se inventa nada** |
| **P2 NO PERSIGUE** | sellado | **VERDE** — nombre certificado pero fuera de vista, o visible a 6 con espada: **0 candidatos** y misma decisión que v35 |
| **P3 CANDADOS + HONOR** | sellado | **VERDE** — C1 (parte que nombra a la hermana → 0 candidatos), C2 (sin `a=1` → byte-idéntica a v35), C4 (parte v2 caducado → 0 candidatos), **fuego amigo del 65 intacto** (con ella en la línea el candidato existe y no se elige) |
| **P4 SILENCIOS** | sellado | **VERDE** — sin hermana: byte-idéntica a **v27**; en calma: byte-idéntica a **v32** |
| **honor (a)** | gate | **0 iniciaciones-estrictas**, 0 ataques contra la hermana (25 decisiones) |
| **P5 REGRESIÓN** | — | **VERDE** — bancos 13-67: **30/30**; humo 3/3 (hash de siempre); determinismo 3/3 |

# E · EL FORENSE DE LOS DESENLACES (66 · para el sofá del dial, ANTES de tocarlo)

74 ventanas de respuesta (propias y por la hermana), seguidas 240 tics:

| desenlace | n | % | golpes (mediana) | hp final |
|---|---|---|---|---|
| **el agresor SE VA** | 34 | **46 %** | 4 | 46 |
| el agresor DESAPARECE de nuestra vista | 33 | 45 % | 4 | 10 |
| nos alejamos nosotras | 5 | 7 % | 2 | 80 |
| sigue el acoso | 2 | 3 % | 15 | 28 |
| **MORIMOS** | **0** | **0 %** | — | — |

**Corrección honesta de la vara** (medida, no estimada): mi etiqueta
"el agresor MUERE" contaba *dejar de verlo para siempre*, y **el mundo solo
nos apunta 7 kills en los 80 diarios de la tanda**. Así que de esas 33, **a lo
sumo 7 son muertes nuestras**; el resto son cuerpos que se fueron y no
volvieron a nuestra vista. Se dice así.

## La pregunta del sofá (sin sello)

- **La persistencia ya basta**: en el **53 %** de las peleas el agresor se va
  o nos separamos, con **4 golpes de mediana**.
- **El dial de matar no tiene caso demostrado**: **0 % de las ventanas acaban
  matándonos**, y solo el 3 % siguen en acoso. Nadie nos mató por no rematar.
- **Las 12 respuestas por la hermana** acaban: 7 el agresor se va · 3
  desaparece · 2 nos alejamos. **Ninguna acaba mal.**

# INCÓGNITAS CON MÉTODO

1. **El asiento en el campo**: v36 no ha jugado. Las tres fotos recuperadas
   son de banco sobre geometrías reales; el campo dirá cuántas ocasiones
   añade de verdad (la vara nueva ya está escrita para medirlo).
2. **Los 7 kills**: quién y en qué desenlace. Recomputable de los diarios sin
   gastar; interesa para saber si matamos defendiendo o defendiéndonos.
3. **El 3 % de acoso persistente** (2 ventanas, 15 golpes de mediana): son
   las únicas donde un dial cambiaría algo. Dos casos no son una política.

# QUÉ QUEDA EN EL REPO

- `alma/parte.py` (`562b90d5…`) — parte v2 con asiento, compatible atrás.
- `alma/appraisal_zs.py` (`160e53a2…`) — certificación por identidad +
  `IDENTIDAD_ON`.
- `alma/verifica_68.py` **nuevo** (`d1856306…`) · `desenlaces.py` **nuevo**
  (`2eade969…`, C+E sobre diarios pagados).
- Alma efectiva de taller: **v36**. Liga: v19.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

El 67 dejó tres fallos que parecían tres problemas distintos —un parte viejo,
un cazador que se había movido una casilla, una certificación que no
encontraba a quién apuntar— y resultaron ser el mismo: **preguntábamos dónde
en vez de preguntar quién**. La hermana siempre supo el nombre del que la
golpeaba; el mundo se lo dice en cada golpe con total certeza. Solo había que
dejarla decirlo: tres caracteres más en el parte.

Con el nombre, la manada defiende el ochenta y seis por ciento de las veces
que puede —no el cincuenta ni el sesenta y dos que las varas viejas
apuntaban—, y tres de las seis fotos que el 66 marcó como "pudo y no quiso"
recuperan el gesto. Las otras tres siguen quietas, y eso también es correcto:
en una no veía al cazador y en dos estaba de verdad a dos casillas con una
espada que llega a una. **Nombrar no es perseguir**: sin verlo, no hay
candidato, y el banco lo verifica en las dos direcciones.

Y el forense de las setenta y cuatro peleas trae la respuesta que el sofá
necesitaba antes de discutir ningún dial de rematar: **en ninguna nos
mataron**. En casi la mitad el agresor se marchó tras cuatro golpes —la
persistencia ya basta— y el mundo nos apunta siete muertes en ochenta
diarios, casi todas indistinguibles de "se fue y no volvió". Si alguna vez se
discute enseñar al animal a rematar, que se discuta sabiendo esto: nadie lo
ha matado por no hacerlo.

---

## Reproducción

```bash
cd gemv-coworld
PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_68   # A+D
python3 paintball/desenlaces.py                                         # C+E
for n in 13 14 15 16 17 18 21 22 23 24 28 33 35 37 39 41 43 46 47 48 s7 53 54 56 59 61 62 63 65; do
  PYTHONPATH=.:paintball paintball/.venv/bin/python -m alma.verifica_$n; done  # 30/30
```
