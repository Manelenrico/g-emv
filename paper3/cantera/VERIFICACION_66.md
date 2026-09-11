# VERIFICACIÓN FRÍA — recálculo desde los logs, sin usar las actas como fuente

Fecha: 2026-09-05 · Mac mini M4 (arm64) · `md5 motor/model.py` =
`1e511978c251130e95169ebf8443efa1`

**Método**: se usan los MISMOS scripts del vigilante con que se produjeron
los números en su día (`paintball/manada_campo.py`, `paintball/reencuentros.py`).
**No se reescribió ninguna definición**: se importan `honor_dos`,
`golpes_entre`, `puerta` y `reencuentros_de` tal cual.

---

## 1 · Tanda 66 (`runs/manada2`, 40 episodios) — los cuatro de cabecera

```bash
cd gemv-coworld && python3 - <<'EOF'
import sys; sys.path.insert(0,"paintball")
from manada_campo import carga, honor_dos, golpes_entre
filas = carga("manada2")
a,b,prop,ch,det = honor_dos(filas)
g = golpes_entre(filas)
print(len(filas), prop, b, a, len(g), ch)
EOF
```

| número | esperado | **recalculado** | |
|---|---|---|---|
| episodios leídos | 40 | **40** | ✓ |
| respuestas a mi agresor | 918 | **918** | ✓ |
| defensas por la hermana | 104 | **104** | ✓ |
| iniciaciones estrictas | 0 | **0** | ✓ |
| golpes entre hermanas | 0 | **0** | ✓ |
| ataques elegidos contra la hermana | 0 | **0** | ✓ |

**RESULTADO: CUADRA EXACTO.** Ninguna diferencia que reportar.

---

## 2 · Encargo 69 (reencuentros, logs 64+66 = 80 episodios)

```bash
cd gemv-coworld && python3 - <<'EOF'
import sys, collections, statistics as st; sys.path.insert(0,"paintball")
from reencuentros import cargar, puerta, reencuentros_de
eps = cargar("manada") + cargar("manada2")
inc, nsl = puerta(eps)
R = [r for ep in eps for r in reencuentros_de(ep)]
ca = [r for r in R if r["arma"] and r["aprox"]]
print(len(eps), inc, nsl, len(R),
      sum(1 for r in ca if r["primero"]=="el"),
      sum(1 for r in ca if r["primero"]=="nadie"))
EOF
```

| número | esperado | **recalculado** | |
|---|---|---|---|
| episodios | 80 | **80** | ✓ |
| puerta: incoherencias de identidad | 0 | **0** (en 964 asientos-episodio) | ✓ |
| reencuentros | 138 | **138** | ✓ |
| episodios con al menos uno | — | 51 · mediana 1/ep | — |
| caso exacto (arma + aproximación) | n=15 | **15** | ✓ |
| — de esos, él pega primero | 7 | **7** | ✓ |
| — de esos, no pega nadie | 6 | **6** | ✓ |

**RESULTADO: CUADRA EXACTO.** Ninguna diferencia que reportar.

---

## Nota de método

Los dos recálculos se hicieron sobre los **diarios originales** que siguen en
`paintball/runs/manada` y `paintball/runs/manada2` (714 MB, no copiados a la
cantera — ver `INDICE_CANTERA.md`). La cantera guarda los `res_*.json`,
`episodios.json` y los resúmenes derivados; **los diarios crudos son la
fuente y viven fuera**, por tamaño.
