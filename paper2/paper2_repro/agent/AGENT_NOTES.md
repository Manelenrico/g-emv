# agent/ — snapshot del código ARCILLA (una versión por cifra de cabecera)

Las dos cifras de cabecera del paper corrieron en DOS imágenes de agente distintas (ambas "arcilla":
Python puro, sin compilar). Se incluye el código EXACTO de cada una, en su subcarpeta:

- `vara_survhome/`        — código que corrió la **vara** (mediana 3.23). Imagen `cvc-gemv-policy:c4-survhome`.
- `temperamentos_conepoda/` — código que corrió los **temperamentos N=5** (mediana 3.6595). Imagen
  `cvc-gemv-policy:c4-cone-poda`, image-id **716532439760** (congelada).

## Qué contiene cada snapshot (paquetes vivos del agente)
`motor/` (oráculo `model.py` + `__init__`), `appraisal/`, `planificador/` (árbol/compromisos),
`memoria/` (tablón/memoria episódica), `coworld_adapter/gemv_policy.py` (la política ejecutada),
`cortex/`, `gemv_policy.py` (entrypoint), `coworld_reference_player.py`. **NO se incluye:** el bronce
(porte compilado posterior), binarios `.so`, ni `__pycache__`.

## El oráculo del motor es idéntico y verificable
`motor/model.py` en AMBOS snapshots tiene md5 **1e511978c251130e95169ebf8443efa1** (el declarado en el
paper). El motor no cambió entre las dos cifras.

## Diferencias entre las dos versiones (honestidad de auditoría)
Comparadas fichero a fichero, difieren SOLO en el andamiaje de datos añadido después de la vara
(optimizaciones de velocidad, inertes bajo los flags de estas corridas):
- `planificador/planificador_v1.py`: cone-poda añade parámetros de poda del cono (`cone_prune`/
  `cone_dryrun`), que quedan a None (inertes) en estas corridas.
- `appraisal/appraisal_v1.py`: cone-poda añade lecturas array/sparse (bit-exactas al scan; OFF o
  resultado idéntico bajo estos flags).
- `coworld_adapter/gemv_policy.py`: la orquestación de esas optimizaciones.
- IDÉNTICOS: `motor/model.py`, `appraisal/appraisal_shelf.py`, `memoria/memoria_v2.py`.
La diferencia de CONFIGURACIÓN entre cifras es el temperamento: la vara corre los 8 agentes con
`GEMV_W_S=1.40` (ENV horneado, sin tabla por-slot); los temperamentos activan `GEMV_TEMPERAMENTS=1`
con `GEMV_W_S_BYSLOT`/`GEMV_W_F_BYSLOT` (ver configs/).
