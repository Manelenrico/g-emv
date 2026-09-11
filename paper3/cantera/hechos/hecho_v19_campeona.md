# Hecho — qué es "8/6/5/1" y cuántas partidas ganó la v19 sola

Fecha: 2026-09-06 · **Solo lectura**: no se ejecutó nada. Los conteos salen de
los `res_*.json` de las tandas de la temporada uno.

---

## 1 · Qué significa "8/6/5/1" — **no son puestos**

**Es el reparto de estadísticas del cuerpo**, el único que el mundo deja
elegir. En `paintball/alma/policy.py:37-38`:

```python
CONSTITUCION = {"intelligence": 8, "athleticism": 6, "speed": 5, "strength": 1}
assert sum(CONSTITUCION.values()) == 20
```

- **intelligence 8** · **athleticism 6** · **speed 5** · **strength 1**
- Suman **20**, que es el presupuesto exacto que el mundo concede
  (`protocol_player.md`: `"stats": {"budget": 20, "min": 1, "max": 10}`); se
  envían una vez en el `allocate_stats` y **son inmutables** el resto de la
  partida.
- El orden en que se escribe (`8/6/5/1`) es **INT/ATH/SPD/STR**, y así aparece
  citado en las actas: `piernas_acta.md:52` ("8/6/5/1 (v19) | 11 tics | 4
  casillas"), `cuesta_campo_acta.md:11` ("cuerpo campeón 8/6/5/1"),
  `ocasion_acta.md:15` ("se restauró la campeona 8/6/5/1").

**No es una lista de puestos por partida.** Los puestos de la v19 van de 1 a
16 y su distribución está abajo (§3).

## 2 · El acta 31 — **existe**

`paintball/debut_acta.md` — *"Acta — LA COSECHA DEL DEBUT"*, del
`PROMPT_31_la_cosecha_del_debut.md`. Lleva una nota de archivo: el encargo
pedía ese nombre pero `debut_acta.md` ya estaba ocupado por el acta anterior,
así que **el nombre del 30 se movió a `debut_certificacion_acta.md`** y el 31
se quedó con `debut_acta.md`. Los dos ficheros existen.

## 3 · ¿Ganó la v19 alguna partida jugando sola? — **SÍ: cinco**

Recuento directo sobre los registros (`placements[slot_v19] == 1`), en las
ocho tandas de la temporada uno donde la v19 jugó **sola** (uuid
`76cdff1a-4652-4748-a720-8e103286489d`):

| | |
|---|---|
| partidas de la v19 pura | **240** |
| **victorias (última en pie)** | **5** |
| tasa | **2,1 %** |

**Las cinco, una a una** (score = 15 de placement + 1 por kill):

| tanda | episodio | score | kills |
|---|---|---|---|
| tempranas | `ereq_42c16dce` | 16 | 1 |
| **piernas** | `ereq_a7fd6f33` | **15** | **0** |
| repesca | `ereq_bbe0f2cd` | 16 | 1 |
| **cuesta** | `ereq_396ae808` | **15** | **0** |
| pila | `ereq_ca74d1b9` | 16 | 1 |

**Dos de las cinco victorias son de quince puntos exactos con cero muertes**:
ganó quedando última en pie **sin matar a nadie**. Las otras tres tienen un
kill (16 puntos) — y por el honor de la casa, ese kill es siempre respuesta a
un agresor, nunca iniciación (0 iniciaciones en toda la serie).

### Distribución completa de puestos de la v19 sola (240 partidas)

| puesto | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| n | **5** | 5 | 8 | 11 | 10 | 16 | 11 | 13 | 10 | 15 | 15 | 20 | 23 | 25 | 29 | 24 |

(top-4 = 29 de 240 = **12,1 %**; mediana en torno al puesto 11.)

## 4 · Reconciliación con el "8 (2,2 %)" del acta 51

`buenas_acta.md` (acta 51, tabla de §B) publica para la *"ànima sola"*:
**357 partidas · 8 victorias · 2,2 %**. Ese número **no es de la v19 pura**:
el universo del 51 (`buenas.py:41-43`, lista `SOLO`) incluye a propósito a
las **variantes del mismo linaje con el cuerpo campeón** — la V6 (v24) de la
tanda `cuesta` y la V7 (v27) de `pila` y `vara`. Recontado hoy con esa misma
definición:

| brazo | partidas | victorias |
|---|---|---|
| **v19 pura** | 240 | **5** |
| variante V6 (cuesta) | 40 | 2 |
| variante V7 (pila) | 40 | 1 |
| variante V7 (vara) | 40 | 1 |
| **total del universo del 51** | **360** | **9 (2,5 %)** |

Las dos cifras difieren un poco de las publicadas (360 vs 357 diarios, 9 vs 8
victorias). **La diferencia se declara, no se maquilla**: el acta 51 filtraba
además por *tener diario legible* (su `diarios_solo()` descarta el episodio si
falta el `.jsonl` del agente, y el 51 documenta la pared del recorte de
cabeza), mientras que este recuento va directo a `res_*.json`, que existe
siempre. Tres diarios ausentes explican los tres episodios de diferencia; la
victoria de más cae en ese grupo. **Para el paper, la cifra que hay que usar
es la de la pregunta —la v19 SOLA— y es 5 de 240 (2,1 %).**

## 5 · Qué se puede afirmar y qué no

**Se puede afirmar:**

- "8/6/5/1" es el cuerpo (INT/ATH/SPD/STR = 8/6/5/1, suma 20, inmutable), no
  una lista de resultados.
- La v19 jugando sola **ganó 5 de 240 partidas** de la temporada uno, y **dos
  de esas victorias fueron sin matar a nadie** (15 puntos exactos).

**No se puede afirmar sin más trabajo:**

- Que esas 240 sean *todas* las partidas que la v19 jugó sola en su historia:
  son las de las ocho tandas que el acta 51 fijó como universo comparable. Si
  hubo v19 en otras tandas fuera de esa lista, no están contadas aquí.
- Nada sobre *cómo* ganó cada una: haría falta abrir sus diarios o replays
  (existen; los ereq están arriba).

## Fuentes

| ruta | qué aporta |
|---|---|
| `paintball/alma/policy.py` (37-38) | **la constitución 8/6/5/1** y su `assert sum == 20` |
| `~/paintball_recon/docs/zero-sum/protocol_player.md` | el presupuesto de 20 y los límites por estadística |
| `paintball/debut_acta.md` | **el acta 31** ("La cosecha del debut") y su nota de archivo |
| `paintball/debut_certificacion_acta.md` | el acta 30, renombrada por la colisión |
| `paintball/buenas.py` (36-43) | el uuid de la v19 y la lista `SOLO` que define el universo |
| `paintball/buenas_acta.md` (§B) | el "8 (2,2 %)" publicado, con su universo de 357 |
| `paintball/runs/{tempranas,ab,piernas,repesca,repliegue,cuesta,pila,vara}/res_*.json` + `episodios.json` | **el recuento de este documento**: 240 partidas, 5 victorias |
| `paintball/piernas_acta.md` (52), `cuesta_campo_acta.md` (11), `ocasion_acta.md` (15) | usos de "8/6/5/1" en las actas, siempre como cuerpo |
