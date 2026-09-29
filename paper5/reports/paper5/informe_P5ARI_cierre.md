# P5-ARI · cierre — versión del cliente y los seis sin facturar

En seco, **coste cero** (solo lecturas `GET`). Motor, decisor y tabla intocados.

---

## 1 · Versión exacta del cliente `coworld`

**`coworld --version` no existe**: la bandera no está implementada y el CLI
responde con el error de uso. *(Hay un subcomando `next-version`, pero es de
otra cosa — manifiestos.)*

**La versión se lee del paquete instalado:**

```
$ paintball/.venv/bin/pip show coworld
Name: coworld
Version: 0.1.44
Summary: Coworld certification, upload, and runner tooling
Home-page: https://github.com/Metta-AI/coworld
License-Expression: MIT
Location: <repo>/paintball/.venv/lib/python3.12/site-packages
Requires: httpx, jsonschema, kubernetes, packaging, pyarrow, pydantic,
          pyyaml, referencing, requests, rich, softmax-cli, typer, websockets
```

| | |
|---|---|
| **cliente `coworld`** | **0.1.44** |
| **Python** | **3.12.12** |
| **servidor por defecto** | **`https://softmax.com/api`** |
| `coworld.__version__` | **no existe** — el módulo no expone versión |

**Declarado:** la única fuente de la versión es la metadata de pip. **No hay
manera de pedírsela al propio CLI**, y eso es en sí un dato para Ari: un
`--version` ahorraría esta conversación.

---

## 2 · Los seis episodios completados y sin facturar

**Reconsultados hoy, 2026-09-23 a las 04:45:28Z: los seis siguen igual.**
`status: completed`, `cost_usd: null`, **`error: null`** en los seis. Ninguno
falló; ninguno tiene coste.

### La lista, para pegar

```
P5-6C   F/20679832   xreq_98327df9-b33a-417d-8a64-1c876035d635   ereq_90707b08-132b-45df-bf49-68ee0c91351e
P5-6C   F/22564954   xreq_bedb0ab0-acf2-4499-8594-3364c616177e   ereq_26eb8c79-e2f7-4e1b-a3ca-269d90c514b3
P5-6C   F/23402786   xreq_d91be50f-c24e-4d12-a8c4-b119f510da9e   ereq_e956aa43-2fe5-49c1-8508-c8568ae5fb88
P5-7C   A/20889290   xreq_0a56e647-8799-4225-ba18-94489f7aa134   ereq_f3546500-d73a-45c4-b8f0-093bfbc3babf
P5-8I   A/20679832   xreq_cc3e7315-7916-46b6-ac43-71da5a0451bc   ereq_0334be26-b3b1-4553-aa6b-d1d668a370ff
P5-8M   A/21622393   xreq_104822db-7094-44fb-8c55-f79dc8767e21   ereq_d18467e9-6ea5-4de5-a1c6-9a00be9e6912
```

### La misma lista, con cuándo acabaron y cuánto llevan así

| serie | brazo/semilla | acabó (UTC) | lleva sin facturar |
|---|---|---|---|
| **P5-6C** | **F**/20679832 | 2026-09-20 21:54:58Z | **54,8 h** |
| **P5-6C** | **F**/22564954 | 2026-09-21 05:14:28Z | **47,5 h** |
| **P5-6C** | **F**/23402786 | 2026-09-21 06:19:33Z | **46,4 h** |
| **P5-7C** | **A**/20889290 | 2026-09-21 15:30:26Z | **37,3 h** |
| **P5-8I** | **A**/20679832 | 2026-09-22 07:09:00Z | **21,6 h** |
| **P5-8M** | **A**/21622393 | 2026-09-22 15:45:50Z | **13,0 h** |

**El más viejo lleva más de dos días.** No es un retraso de minutos.

### Lo que se puede decir del patrón, y lo que no

**Lo que se ve:**

- **Seis de 200 episodios completados = 3,0 %.**
- **Los tres de P5-6C son del brazo F**, que es el único que llama al modelo por
  el sidecar. **Los tres de P5-7C, P5-8I y P5-8M son del brazo A**, que no llama
  a nadie. **Así que no es cosa del consejero**: pasa con y sin llamadas.
- **Aparecen en cuatro series distintas**, con cuatro imágenes distintas, a lo
  largo de tres días.
- **Ninguno tiene `error`.** El episodio se completó, los diarios se
  descargaron, los datos se usaron. **Lo único que falta es el coste.**

**Lo que NO se puede decir:**

- **No sé si están sin facturar o facturados y no reportados.** Desde fuera solo
  se ve `cost_usd: null`; si el pod se cobró y el campo no se rellenó, o si de
  verdad salieron gratis, **el cliente no lo distingue**.
- **No hay patrón de semilla ni de tanda** que yo vea con seis casos.

**Para el gasto declarado del paper cinco**, estos seis se han contado siempre
como **cero**, que es lo que el servidor dice. Si resultara que sí se
facturaron, **los totales de las series subirían**, y los más afectados serían
los de P5-6C.

---

## Una corrección que conviene que Ari tenga

**En dos informes conté mal este censo.** En `informe_P58I_sonda5.md` escribí
que el de P5-8I era «el **segundo** de la serie», y en `informe_P58M.md` que el
de P5-8M era «el **tercero** del paper cinco». **Los dos están mal: son el
quinto y el sexto.**

**El acta lo tenía bien** —dice «3 sin facturar» en P5-6C y «1» en P5-7C—; **el
que sumó mal fui yo**, contando de memoria en vez de ir al censo. Lo digo aquí
porque la cifra que Ari necesita es **seis**, no tres.

---

## Custodia

```
motor/model.py                          1e511978c251130e95169ebf8443efa1
paintball/alma/decisor_zs.py            8fa03547e3228ef9df4aa94c444f9252
paintball/alma/appraisal_zs_v42_exp.py  98c13d60167c80cc8334c965be75c640
```

Datos en `cantera/paper5/P5ARI_sin_facturar.json`. Los otros dos informes de
P5-ARI: `informe_P5ARI_p1a6.md` y `informe_P5ARI_p7.md`.

**Solo lecturas. Nada creado, nada cancelado. Gasto: cero.**

**PARO AQUÍ.**
