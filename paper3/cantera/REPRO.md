# REPRO — reproducibilidad del paper tres

Fecha: 2026-09-05 · `md5 motor/model.py` = `1e511978c251130e95169ebf8443efa1`

## Versiones del alma (con su commit)

| versión | commit | encargo | md5 del appraisal |
|---|---|---|---|
| **v27** | `aeac3f2` | 52 (la sola, antes del parte) | `9a9a4f6e202a17fa581048a953f0a4e7` |
| **v34** | `335ea58` | 63 la manada | `aa234ba0e66b3ef05565273f1af52161` |
| **v35** | `286628f` | 65 alcance y fuego amigo | `4a5f7d2415184ce7692f4c3488202e85` |
| **v36** | `c023c0c` | 68 el nombre del agresor | `3abf6e43f691f5e7234f0903f8bb842e` |
| **v37** | `825e096` | 70-71 miedo con memoria (resellada) | `87745903992bdf0b4f5a18d13f9d4f5a` |

## Tandas de campo

### Tanda 64 · v34 — `xreq_7066af5f-858f-481e-989c-3d109aad3e2d`
- episodios: **40** · cost_preview: `None`
- ids: `e112a979, a423da64, 25a9ef9e, e16f4803, cde813ea, 782f0c5a, 2f34291c, ed1b94c3, 3ef9ccd7, 9a1f188d, 433f6004, feafe3ac, 5285b3e0, 56ea62d4, cf8ef037, ce9eb01b, 508d5d4a, fe0f8ca8, 8a674d69, 32c0326c, 4b9ec6f4, 71f16a3b, 11b827ae, 5e05a52e, b7731595, 6cacbb37, fdb0bdd1, b037b28a, d4de078a, 0e61676b, dfc35a18, 191873b7, 653f64cd, 079c223f, 08440b30, 94010e5e, f2570d5f, e1daaef0, a74ee837, 4367ef5f`
- (ids completos en `runs/manada/episodios.json`)

### Tanda 66 · v35 — `xreq_c2d94f73-7af1-4ac6-8991-2846c024b3e5`
- episodios: **40** · cost_preview: `None`
- ids: `edfce616, 9de73ff8, df2427d4, b915417a, 8be8af47, a62f7c2d, 736990b4, 1f093846, a4afa48e, a22dd3eb, 4b24cc53, 9fab619d, 6f9704f8, 60454bec, 292ee72d, 18dfbd78, 91a500a4, d6b2b089, b4d7ff02, 9869b665, a60c3e48, 0d51e268, 94c76dfa, c49e97f1, 286f1dc1, af1e5567, 350c7c63, 68f15078, 5847a638, 62651a32, f35d9d5a, f9a19099, cd58919c, c6717e24, 77687c93, d294a0b7, 3f9b199e, b71574ae, 4467998b, 7e1d2326`
- (ids completos en `runs/manada2/episodios.json`)

## Roster explícito del 66 (sin nuestra campeona)

| asiento | policy_ref |
|---|---|
| 10 | `gemv-anima:v12` |
| 11 | `gemv-anima:v12` |
| -1 | `6244cdeb-e044-42ff-91e3-a5c716c4338d` |
| -1 | `47f38a1c-9143-4b56-9316-ceabe7c82c6d` |
| -1 | `41f43efa-bbd5-477a-8ed1-1443f2731eb1` |
| -1 | `458ec0b6-fc59-4bda-aff0-68daa7f21b79` |
| -1 | `54ec6fab-6773-46db-bb55-119688182786` |
| -1 | `2b9cfd17-db50-4990-8f99-6c7c13453f61` |
| -1 | `9457da2a-832d-45e5-b918-9209e86f9948` |
| -1 | `dfc40843-b709-4332-85a6-c5bbb653375b` |
| -1 | `3e8097e1-85b8-4731-b7c1-e674f2ccbd10` |
| -1 | `09da1dbc-ac3b-4bb1-9114-4ee615496755` |
| -1 | `6244cdeb-e044-42ff-91e3-a5c716c4338d` |
| -1 | `47f38a1c-9143-4b56-9316-ceabe7c82c6d` |
| -1 | `41f43efa-bbd5-477a-8ed1-1443f2731eb1` |
| -1 | `458ec0b6-fc59-4bda-aff0-68daa7f21b79` |

> Verificado en los 40 episodios: 0 participantes nuestros fuera de 10/11.

## Semillas

- Campos con 'seed' en el detalle de episodio: **ninguno** (la plataforma no los expone en `episodios.json`)

## Replays públicos citados en las actas

- `56_cuidado_acta.md`: `395c6f3f`, `85840773`
- `57_pareja2_acta.md`: `610355a0`, `e783da2b`
- `64_manada_campo_acta.md`: `b481c43e`, `fc91ff56`
- `66_manada2_acta.md`: `3e5751db`, `9b98dc83`

(URL completa del visor en cada acta; patrón del 38: `coworld replay-open <ereq> --hosted`.)

## Diarios crudos (fuente de la verificación fría)

- `paintball/runs/manada/` — **344 MB** · `paintball/runs/manada2/` — **370 MB**
- **No copiados a la cantera** (714 MB): ver `INDICE_CANTERA.md`. La cantera guarda
  `episodios.json`, `res_*.json` y los derivados; los diarios siguen en el proyecto vivo.

## Tanda 72 · ablación — `xreq_6119d364-3c6b-4937-be97-8c5c3a37ec83`

- **imagen**: `gemv-anima:v13` (etiqueta local `gemv-anima:v27pareja`),
  construida desde un **staging** (`/tmp/v27pareja`) para no tocar el repo
  vivo. El appraisal exacto de esa imagen está en la cantera como
  `codigo/appraisal_zs_v27pareja.py` (los doce interruptores en OFF).
- **base histórica del gate**: `codigo/appraisal_zs_v27.py`, commit
  **`aeac3f2`** (encargo 52, la ánima sola antes del parte).
- **roster**: idéntico al del 66 (`runs/xp_ablacion_v27.json`), con las
  gemelas sustituidas por `gemv-anima:v13`. Verificado en los 40 episodios:
  0 participantes nuestros fuera de los asientos 10/11.
- **coste**: `cost_preview` 20 cr (tope 25) · 40/40 episodios · 80/80 diarios.
- **episodios (40)**:

  - `ereq_64194b77-8d47-4f97-b41e-431306710c2b`
  - `ereq_73d3c64d-f3f3-4cc4-9e5c-cce25c033478`
  - `ereq_9aaa8a16-a34e-4708-a016-e658881b82e5`
  - `ereq_d2ff98ea-4edf-40bc-b55a-e7e53eb9699d`
  - `ereq_b410a7fd-0008-4533-a4e6-28d43e72bb31`
  - `ereq_79a5fb75-8c5d-4b69-ad34-20cbd0bae456`
  - `ereq_7dafe136-a077-46ce-8584-3b0c4f26b653`
  - `ereq_d21f61be-26d0-4737-9b56-e1701736ea01`
  - `ereq_57f3ac17-73a6-469f-8b18-b1ea093f4470`
  - `ereq_c615e3de-4a65-4c72-8c39-83d313d371d9`
  - `ereq_e6c7a000-36f3-448b-82dd-7ffbc956ac46`
  - `ereq_4bc1c485-2e5d-4123-aa7e-df64bff2cc3c`
  - `ereq_e5d00939-7c50-427f-846b-e26f38f19bb4`
  - `ereq_619ec82b-0bda-43a1-83b3-47559ae55df8`
  - `ereq_6a4a8bc9-c8ad-42a2-a71c-ddce2bc8ffd7`
  - `ereq_701b3732-3eeb-47a3-8b6d-d65aefecf658`
  - `ereq_42b45729-c10e-4bea-b3bd-881e297f45e6`
  - `ereq_3b200481-ceff-4077-9702-21c58f06410f`
  - `ereq_944eac4d-778b-47c4-bda3-11654fc1e3df`
  - `ereq_2c5ab26c-b5d9-4b2b-ab2b-e465040dbc7d`
  - `ereq_eba164a1-72c4-4f19-99c0-b2659e427705`
  - `ereq_d64c3d2f-8be0-4547-b2d3-8f60dea235d2`
  - `ereq_a6014500-e052-4c06-b2fc-4ffa2754a4e8`
  - `ereq_5e88e288-1e4b-4d92-b1c4-e63cee33dda4`
  - `ereq_5fa4074a-f14f-4f9f-bad3-2a3ba6db69ca`
  - `ereq_ec321e7d-fe50-4131-ba6a-296597ab9227`
  - `ereq_86818005-58ec-44b6-8ae0-9ad1035b6de0`
  - `ereq_132cbd1c-7ef5-4f96-b193-4777f6abc6c4`
  - `ereq_227ccbb5-cd14-4512-b119-5aad37a8c0dd`
  - `ereq_36d775c2-a122-4ecd-a25f-97b1b4339036`
  - `ereq_2ec6bd53-98f2-4e16-ba10-5f1a20664b3d`
  - `ereq_1f9b8275-8a9a-41cc-a38e-0eca6adcd7f8`
  - `ereq_267a13fb-60e9-4fa3-a1b9-b7f3ecf9e396`
  - `ereq_8325c35d-f6de-4481-9008-747cddfefc76`
  - `ereq_9b808828-50c8-4d0e-a17e-21573e36ba32`
  - `ereq_bc50d6e7-27dc-402d-9946-1832ea9313b5`
  - `ereq_9c3c18ad-f5d1-41a6-ae45-011ac603482e`
  - `ereq_5d82be04-6ed6-4c9a-bdb8-197597ec1dc6`
  - `ereq_b4c750e3-7c1f-4c04-8f07-288cefccbc25`
  - `ereq_21d22d51-46f6-4dd3-96d6-ca7dc2e2e00c`

- replays hosted señalados: `fd29a144` (el don único, `ereq_9c3c18ad`) · `eda0b7d3` (contraste, `ereq_132cbd1c`)

## Diarios crudos

- `LOGS_MD5.md` lleva el md5 uno a uno de los **240 diarios** de las tres tandas (manada 64, manada2 66, ablacion 72).
