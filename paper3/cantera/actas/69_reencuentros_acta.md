# Acta — LOS REENCUENTROS (forense puro) · **va al sofá del 70**

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_69_los_reencuentros.md` · **Solo lectura, coste 0**

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. Liga en **v19**. **Ninguna versión nueva, ninguna conducta,
  ninguna silla tocada.**
- Todo sale de los 80 episodios de campo ya pagados (64 + 66, 160 diarios).
- **Testigo ciego aplicado a la vara**: solo cuenta como agresor CIERTO el
  asiento que aparece en el `damage_taken.source` de una de las dos gemelas
  —lo que el parte v2 transmitiría—. No se usan agresiones a terceros que el
  ánima no podría conocer.

---

# A · LA PUERTA: identidad estable — **PASA**

**0 incoherencias de equipo en 964 asientos-episodio**: dentro de un
episodio, el asiento identifica siempre al mismo cuerpo. Todo lo que sigue
tiene sentido.

# B · LA TABLA — **138 reencuentros en 51 de los 80 episodios**

(La tabla fila a fila está en `runs/reencuentros.json`, una entrada por
reencuentro con las once columnas del encargo.)

| resumen | valor |
|---|---|
| reencuentros | **138** (mediana **1** por episodio; 51/80 episodios con al menos uno) |
| como % de las 74 peleas del 68E | **186 %** |
| con **arma visible** | 99 (**72 %**) |
| con **aproximación** medible | 22 (16 %) |
| **arma Y aproximación** (el caso del diseño) | **15 (11 %)** |
| **quién pega primero** | él **56** · nadie 75 · nosotras 7 |
| **desenlaces** | se va/separa **75** · nos daña **58** · lo dañamos 4 · **nos mata 1** |
| **tics de aviso** (t1 → su primer golpe) | mediana **21** · p25 **6** · mín 0 · ≤4 tics: 22 % |
| **gaps** de separación | mín 25 · mediana **110** · máx 3320 · **≤96 tics: 46 %** |

# C · LAS PREDICCIONES SELLADAS

| | predicción | medido | |
|---|---|---|---|
| **P1** | ≤25 % de las peleas y mediana ≤1 | **186 %**, mediana 1 | **FALLA** (por el porcentaje) |
| **P2** | él pega primero ≥60 % con arma+aproximación | **47 %** (7 de 15) | **FALLA** |
| **P3** | mediana de aviso ≥4 tics | **21** (n=59) | **ACIERTA** |
| **P4** | ≥1 de cada 3 es "pegó a la hermana y viene a la otra" | **53 %** (n=138) | **ACIERTA** |

**P1 falla por goleada y en la dirección contraria a la esperada**: la mesa
apostaba a que casi nadie vuelve, y vuelven **casi el doble de veces que
peleas hay**. Los agresores de este mundo no desaparecen: rotan, se van y
regresan — mediana de separación 110 tics.

**P2 falla y es la corrección más importante para el diseño**: en el caso
exacto que la precaución armada querría cubrir —vuelve, con arma, y se
acerca— **él pega primero menos de la mitad de las veces** (7 de 15). En 6 de
esos 15 **no pega nadie**: viene armado, se acerca… y no ataca. Anticiparse
habría golpeado primero a alguien que no iba a golpear en 6 de cada 15 casos.

# D · LA REGLA DE DECISIÓN, APLICADA

Los reencuentros son el **186 %** de las peleas (≥10 %), así que —tal como
quedó sellado— **va al sofá del 70**, con las tres cosas que el sello pide:

## 1 · La tabla (arriba y en JSON)

## 2 · El honor, partido en dos (lo que costaría)

- **Golpes a quien nunca pegó a nadie**: seguiría en **0** por construcción
  (la precaución exige agresor certificado por `source` propio o de la
  hermana).
- **Golpes preventivos a agresor certificado que se acerca armado**: el
  universo son esos **15 reencuentros**. De ellos, **9 acaban dañándonos** y
  **6 acaban en nada** — es decir, **el 40 % de los golpes preventivos caerían
  sobre alguien que no llegó a atacar**. Ese es el precio exacto, con su n.

## 3 · La caducidad, contestada por los gaps

La memoria del testimonio caduca a 96 tics. **El 54 % de los reencuentros
tienen un gap mayor** (mediana 110, máximo 3320). Es decir: **una memoria de
96 tics perdería más de la mitad de los reencuentros**. Si la precaución se
construyera, o la memoria dura **todo el episodio**, o cubre la mitad de los
casos. El dato está, la decisión es de la mesa.

# LO QUE EL FORENSE DESACONSEJA, DICHO CLARO

El aviso mediano es **21 tics** — hay hueco físico de sobra para reaccionar
(P3 acierta). Pero **el 78 % de los reencuentros no acaban con él pegando
primero**, y en el subconjunto armado-y-aproximándose la cifra sigue siendo
**menos de la mitad**. La precaución armada compraría margen en 9 casos de
138 a cambio de golpear primero en 6 que no iban a nada. **Nadie murió por
esperar**: 1 muerte en 138 reencuentros.

# EPISODIOS PARA PEDIR REPLAY (los de reencuentro claro)

- `ereq_2f34291c-90bc-4f2c-875e-3d1ba6b774ec` — **8 reencuentros**
- `ereq_4b24cc53-fdaf-4197-8ea0-e4e8c9d8d2a6` — **8 reencuentros** (incluye
  tres del mismo asiento 8, con arma, y uno con aviso de 11 tics)
- `ereq_6f9704f8-1f25-47d1-a705-184cabbc3dcd` — **8 reencuentros**

# QUÉ QUEDA EN EL REPO

- `reencuentros.py` — el forense (puerta, vara, tabla, P1-P4, regla D).
- `runs/reencuentros.json` — las 138 filas.
- **Nada de conducta, nada de versión.** v36 intacta; liga v19.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

La mesa preguntó si el que pega vuelve, apostando a que casi nunca. Vuelve
ciento treinta y ocho veces en ochenta episodios —casi el doble de veces que
peleas hay— y en la mitad de los episodios al menos una vez. La memoria
tendría de sobra sobre qué actuar: esa parte del diseño está justificada por
el dato.

Lo que el dato no justifica es la conclusión que parecía obvia. En el caso
exacto que la precaución querría cubrir —vuelve, lleva arma, se acerca— él
pega primero **menos de la mitad de las veces**, y en seis de esos quince no
pega nadie: se acerca armado y no ataca. Golpear al verlo venir habría
convertido seis encuentros que terminaron en nada en seis peleas empezadas
por nosotras. Y el margen que tendríamos para esperar es amplísimo:
veintiún tics de mediana desde que lo vemos hasta que golpea, si es que
golpea.

Hay un tercer número que conviene no perder: en el cincuenta y tres por
ciento de los reencuentros, quien lo ve volver no es a quien pegó, sino su
hermana. Ese es exactamente el caso que solo el parte v2 permite conocer —el
nombre viajando entre las dos— y es el que da sentido a hablar de memoria
compartida. La materia prima existe.

Así que el forense entrega tres cosas y ninguna decisión: **vuelven mucho más
de lo previsto, atacan mucho menos de lo previsto, y una memoria de noventa y
seis tics se perdería la mitad de los reencuentros.** Con eso delante, y con
una sola muerte en ciento treinta y ocho reencuentros, el sofá del 70 tiene
lo que necesita para decidir si el animal debe adelantarse — sabiendo que
hoy, esperando, casi nunca le cuesta nada.

---

## Reproducción

```bash
cd gemv-coworld
python3 paintball/reencuentros.py     # puerta, tabla, P1-P4, regla D
```
