**[EN]** This is the independent reproducibility package for Paper 2
(agent code, configs, seeds, raw results, logs, replays). The README
below is in Spanish, the project's working language; the paper's
English version (G-EMV_the_Hive_EN.pdf) is available in this repo. All
figures can be verified against results/ regardless of language:
numbers, hashes and replays need no translation.

---

# Paper 2 — Paquete de reproducibilidad independiente

Código del agente, configuraciones, semillas, resultados crudos y entorno que respaldan las dos cifras
de cabecera del paper: la **vara** (mediana 3.23) y el **banco de temperamentos N=5** (mediana 3.6595).

## 1. Qué contiene cada carpeta
- **`agent/`** — el código exacto del agente (arcilla: Python puro, sin compilar) que corrió las vidas.
  Una subcarpeta por cifra (`vara_survhome/`, `temperamentos_conepoda/`) porque cada una corrió en una
  imagen distinta; ver `agent/AGENT_NOTES.md`. El motor (`motor/model.py`) es idéntico en ambas.
- **`configs/`** — el manifest del mundo (`manifest_e4_s0_t300_2500.json`) + por cifra: los flags
  `--secret-env` del runner (`secret_env_flags.txt`) y el ENV horneado en la imagen (`baked_image_env.txt`).
  La configuración efectiva de una corrida = ENV horneado + flags del runner.
- **`seeds/`** — la semilla de cada cifra (seed 0; la varianza entre réplicas viene del canal
  `pregonero` con `GEMV_PREGONERO=1`, no de la semilla).
- **`results/`** — los `results.json` COMPLETOS de cada réplica (+ su `config.json`).
- **`raw_logs/`** — los logs por-agente (`policy_agent_*.log.gz`, comprimidos con gzip por tamaño; el
  original ~6 MB, el gz ~0.6 MB), los logs del servidor y los `pregonero_*.jsonl`.
- **`replays/`** — la grabación binaria de cada vida empaquetada (`*.replay.gz`), para el visor.
- **`environment_version.txt`** — versiones (coworld, Python, SO, Docker) e image-ids congelados.

## 2. Cómo cotejar las cifras del paper contra estos `results.json`
El score de una vida es el campo **`scores[0]`** de `results.json` (array de 8, uno por slot; en las
corridas all-cogs los 8 son idénticos). La cifra del paper es la **MEDIANA** de las réplicas:
```
python3 - <<'PY'
import json, glob, statistics
for name, patt in [("vara", "results/vara_3.23/r*/results.json"),
                   ("temperamentos N=5", "results/temperamentos_n5_3.6595/r*/results.json")]:
    s = sorted(json.load(open(f))["scores"][0] for f in glob.glob(patt))
    print(f"{name}: N={len(s)} scores={[round(x,4) for x in s]} mediana={statistics.median(s):.4f}")
PY
```
Debe dar: vara mediana ≈ **3.2271** (rango [2.31, 4.11]); temperamentos N=5 mediana ≈ **3.6595**.

> **Nota (dos imágenes):** las dos cifras de cabecera corrieron en dos imágenes Docker que difieren
> solo en andamiaje inerte de velocidad y en la config de temperamento; `motor/model.py` está
> verificado idéntico por md5 en ambas. Detalle en `agent/AGENT_NOTES.md`.

> **Nota (sello N=3 → N=5):** en `temperamentos_n5_3.6595/`, las réplicas **r1–r3** son el sello
> original N=3 y **r4–r5** la ampliación pre-registrada; la mediana **3.6595** coincide en ambos cortes
> (N=3 y N=5), porque r1 es la réplica central en los dos.

## 3. Cómo relanzar una vida
Requiere Docker y la CLI coworld del entorno (ver `environment_version.txt`). Ejemplo para una réplica
de la vara (8 agentes cogs vs clips scriptados, seed 0, 2500 pasos):
```
coworld run-episode configs/manifest_e4_s0_t300_2500.json \
  cvc-gemv-policy:c4-survhome cvc-gemv-policy:c4-survhome cvc-gemv-policy:c4-survhome \
  cvc-gemv-policy:c4-survhome cvc-gemv-policy:c4-survhome cvc-gemv-policy:c4-survhome \
  cvc-gemv-policy:c4-survhome cvc-gemv-policy:c4-survhome \
  --run python --run /app/gemv_policy.py -n 1 -o salida_repro \
  $(sed 's/^/--secret-env /' configs/vara_3.23/secret_env_flags.txt | tr '\n' ' ')
```
Para los temperamentos: usar la imagen `cvc-gemv-policy:c4-cone-poda` y
`configs/temperamentos_n5_3.6595/secret_env_flags.txt` (incluye `GEMV_TEMPERAMENTS=1` + las tablas
`GEMV_W_S_BYSLOT`/`GEMV_W_F_BYSLOT`). El score sale en `salida_repro/results.json` → `scores[0]`.

## 4. AVISO DE COSTE
Cada vida de **2500 ticks** cuesta **~30 horas-máquina** en esta versión SIN compilar (el agente es
Python puro; el árbol de planificación crece hasta el timeout en la vejez). Reproducir una cifra de
cabecera (N=3 o N=5) son varias vidas → días de cómputo. Presupuestar en consecuencia.

## Replays
`replays/` contiene la grabación binaria de cada vida (`<cifra>/rN.replay.gz`). Para visualizar una,
descomprímela y pásala al visor de la CLI coworld junto al manifest:
```
gunzip -k replays/vara_3.23/r1.replay.gz            # → replays/vara_3.23/r1.replay
coworld replay configs/manifest_e4_s0_t300_2500.json replays/vara_3.23/r1.replay
```
(No se incluye un visor HTML autocontenido: la visualización se hace con la CLI coworld del entorno.)

## Verificación del motor
El md5 de `agent/*/motor/model.py` es **1e511978c251130e95169ebf8443efa1**, el mismo declarado en el
paper. Comprobar: `md5sum agent/vara_survhome/motor/model.py`.
