# Forense — ¿sobre qué corrida se midió el censo del peldaño 1?

Fecha: 2026-09-06 · **Solo lectura**: no se ejecutó nada y no se tocó código.
Pregunta: el resultado del censo (peldaño 1 de The Pack en machina_1: *"ag7
minó 84 / ag3 5"*, cobertura 72 % centro / 1 % periferia, N=3 × 10.000 tics)
¿se midió con los ocho agentes iguales (vara, `w_s=1,40`) o con temperamentos
distintos?

## RESPUESTA CORTA

**Con TEMPERAMENTOS DISTINTOS.** Las tres corridas del censo heredan los
flags del banco de temperamentos, incluidos
`GEMV_TEMPERAMENTS=1` y **`GEMV_W_S_BYSLOT=1.90, 1.70, 1.60, 1.40, 1.40,
1.25, 1.15, 1.15`** (más `GEMV_W_F_BYSLOT=1.10, 1.05, 0.90, 1.00, 0.80, 0.75,
0.65, 1.10`). **No era la vara**: los ocho no llevaban `w_s=1,40`; solo los
slots 3 y 4 lo llevaban.

---

## 1 · El acta del cierre y las corridas

- **No existe** un fichero `the_pack_peldano1_acta.md`. El cierre del peldaño
  uno está repartido en:
  - `the_pack_peldano1_spec.md` — la spec sellada en mesa el **2026-08-28**.
  - `the_pack_peldano1_paquete.md` — **el paquete de resultados, "SIN
    VEREDICTO"**, con las tres vidas y las tablas (A) verificación externa,
    (B) cobertura y (C) consistencia. *De aquí salen los dos números de la
    pregunta.*
  - `the_pack_censos_crudos.md` — los **24 censos crudos** (8 observadores ×
    3 vidas, último dump ~t9000).
  - `the_pack_camino.md` — el resumen de estado que declara P1 **CERRADO
    (2026-08-29)** y donde aparece citada la frase *"ag7 minó 84 / ag3 5"*.
- **Las tres corridas** (seeds en el lanzador, ver §2):
  `170534803`, `120290872`, `176280986`, a 10.000 tics cada una.
- **Dónde está "ag7 minó 84 / ag3 5"**: `the_pack_peldano1_paquete.md`, tabla
  (A) de la **VIDA seed 170534803** — columna *REAL minado*: `ag7 = 84`,
  `ag3 = 5`. La cobertura *72 % / 1 %* sale de la tabla (B) de esa misma
  vida (celda obs0→ag1 = 72; celdas obs4→ag3 y obs6→ag7 = 1).
- **Los logs y JSON de esas tres corridas YA NO EXISTEN.** El lanzador escribía
  en `_tmp_gemv/pack_censo_limpio/vida<N>_s<seed>/`, y `_tmp_gemv/` no está en
  el sistema (`find ~` sin resultados para las tres seeds). Lo que sobrevive
  es el volcado de los censos (`the_pack_censos_crudos.md`) y las tablas del
  paquete.

## 2 · El perfil de los ocho — archivo y campo

**Cadena de evidencia (dos ficheros):**

1. **`bronce/run_pack_censo.sh`** — el lanzador exacto del examen del censo
   (cabecera: *"THE PACK, peldaño 1 — EXAMEN DEL CENSO … N=3 vidas a 10.000t,
   BRAZO ÚNICO: titular con era ON + GEMV_CENSO=1"*; `SEEDS=(170534803
   120290872 176280986)`). Su línea de flags **no los escribe: los hereda**:

   ```sh
   BASE=$(grep '^FLAGS=' pregonero/run_bench_temper.sh | sed 's/^FLAGS="//; s/"$//')
   BASE=$(echo "$BASE" | sed "s/GEMV_PREGONERO=1/GEMV_PREGONERO=0/")
   FLAGS="$BASE --secret-env GEMV_BRONCE=on … --secret-env GEMV_CENSO=1"
   ```

   Es decir: **toma tal cual los flags del banco de temperamentos** y solo
   apaga el pregonero y añade los del bronce, la era y el censo.

2. **`pregonero/run_bench_temper.sh`, línea 10** — la variable `FLAGS`
   heredada contiene, entre otros:

   ```
   --secret-env GEMV_TEMPERAMENTS=1
   --secret-env GEMV_W_S_BYSLOT=1.90,1.70,1.60,1.40,1.40,1.25,1.15,1.15
   --secret-env GEMV_W_F_BYSLOT=1.10,1.05,0.90,1.00,0.80,0.75,0.65,1.10
   ```

**Campo exacto que lo verifica**: la variable de entorno
**`GEMV_W_S_BYSLOT`** (y su espejo `GEMV_W_F_BYSLOT`), pasada por
`--secret-env` a las ocho instancias. La mecánica de cómo se aplica está en
`bronce/gemv_policy_bronce.py` (líneas 52-66: `GEMV_W_S`/`GEMV_W_F` fijan
`cfg.w_s_pos` y arrastran `cfg.w_s_ten` con el mismo ratio, sobre un
`ModelConfig` aparte; `DEFAULT_CONFIG` nunca se toca) y la tabla de perfiles
en `temperamentos_spec.md` (líneas 27, 89-110).

**Vale para las tres corridas por igual**: el bucle `for idx in 1 2 3` usa el
mismo `$FLAGS` y la misma imagen (`cvc-gemv-bronce:era`) para las ocho
instancias; **la única diferencia entre agentes es el slot**, que es
precisamente lo que indexa `BYSLOT`.

| slot | w_s | vs vara 1,40 |
|---|---|---|
| 0 | **1,90** | +0,50 |
| 1 | **1,70** | +0,30 |
| 2 | **1,60** | +0,20 |
| 3 | **1,40** | = (control) |
| 4 | **1,40** | = (control) |
| 5 | **1,25** | −0,15 |
| 6 | **1,15** | −0,25 |
| 7 | **1,15** | −0,25 |

> Nota: el rango real es **1,15 – 1,90**, no "1,15 a 1,70" como decía la
> pregunta. El 1,70 es el slot 1; el máximo es el slot 0 con 1,90.

**Lo que NO permite verificarlo**: los censos crudos
(`the_pack_censos_crudos.md`) **no contienen ningún campo de perfil, `w_s` ni
temperamento** — por diseño de la spec (§3: el censo solo apunta lo
observable certificado: herencia, territorio, oficio, dinero, palabra,
quieto%). Buscar `w_s|temper|vara|perfil` en los crudos y en el paquete no
devuelve nada.

## 3 · Las cunas y a qué atribuye el acta la división del trabajo

**¿Eran distintas las cunas?** **Sí, pero poco: dos valores.** El censo
registra la cuna en la columna HERENCIA, campo **`dist_nac_hub`** (y
`heart_cuna`). En la vida `170534803` (leído en `the_pack_censos_crudos.md`,
observador ag0, que ve a los ocho):

| ag | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| `dist_nac_hub` | 3 | 2 | 3 | 2 | 2 | 3 | 2 | 3 |
| `heart_cuna` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Es decir: **ninguno heredó corazón de cuna** y las distancias de nacimiento al
hub son **2 o 3** — distintas entre agentes pero sin relación aparente con el
minado (ag7 = 84 minados nace a 3; ag3 = 5 minados nace a 2; pero ag2 = 44
también nace a 3 y ag1 = 12 nace a 2).

**¿A qué lo atribuye el acta?** **A ninguna de las dos: no lo atribuye.** El
paquete del peldaño uno se declara explícitamente **"SIN VEREDICTO"** (primera
línea) y `the_pack_camino.md` se limita a constatar el hecho —*"ag7 minó 84 /
ag3 5 = división del trabajo real y LEGIBLE"*— **como demostración de que el
censo es legible**, que era la pregunta del peldaño (§1 de la spec:
*"¿las ocho filas del censo son DISTINGUIBLES?"*). No hay en el peldaño uno
ninguna atribución causal a la cuna ni al temperamento.

**Y hay una advertencia previa que va en contra de atribuirlo al
temperamento**, sellada once días antes y que conviene citar en el paper —
`temperamentos_spec.md`, "SELLO DE LA ERA" (2026-08-17), sección **NO-LEY**:

> *"**La división del trabajo NO se sostiene.** corr(w_s, minado): r1 −0,25
> (no el −0,52 de una foto previa), r2 −0,18, **r3 −0,04** (se desvanece);
> Spearman ~0. Quitando al atrapado: r1 −0,18, r3 −0,00 → el poco negativo lo
> empujaba el agente marooned (no mina porque está pinchado), no un gradiente
> w_s→minado."*

y su lección de método, dirigida explícitamente al paper tres:

> *"**Las leyes individuales de UNA corrida son fotos de una semilla.** El
> agregado (N=3) es robusto; los 'rasgos' mecánicos de r1 (trampa, división
> del trabajo) eran contingencia de esa realización."*

## 4 · Qué se puede afirmar y qué no

**Se puede afirmar** (con archivo y campo):

1. Las tres corridas del censo llevaban **temperamentos diversos**
   (`GEMV_TEMPERAMENTS=1`, `GEMV_W_S_BYSLOT=1.90…1.15`), heredados del banco
   de temperamentos vía `bronce/run_pack_censo.sh`. **No eran ocho iguales.**
2. Las **cunas diferían** en `dist_nac_hub` (2 o 3), con `heart_cuna=0` para
   todos.
3. El acta/paquete del peldaño uno **no atribuye** la división del trabajo ni
   a la cuna ni al temperamento: solo la constata como prueba de legibilidad.

**NO se puede afirmar** (y no se rellena):

- **Cuál de los dos factores causa el 84-vs-5**, ni con qué peso. Con los
  logs de las tres corridas borrados (`_tmp_gemv/`), no queda material para
  correlacionar w_s con minado en **estas** vidas. La única correlación
  medida en el proyecto es la de la era anterior (2500 t, otras corridas):
  **−0,25 / −0,18 / −0,04, desvaneciéndose**, y su propio sello la declara
  **NO-LEY**.
- **Si el ag7 de la vida 170534803 era el slot 7** (`w_s=1,15`, el extremo
  bajo) **en el sentido de `BYSLOT`**: el paquete llama "ag" al `agent_id` del
  episodio y el env indexa por slot; **que el índice de agente coincida con el
  índice de slot es plausible pero no está verificado en ningún fichero
  superviviente**. Si el paper quiere decir *"el que más minó era el de menor
  peso social"*, esa identificación hay que verificarla primero — y hoy no
  hay con qué.

## Archivos consultados

| ruta | qué aporta |
|---|---|
| `bronce/run_pack_censo.sh` | **el lanzador del examen**: seeds, N=3, 10.000t, imagen, y la herencia de flags |
| `pregonero/run_bench_temper.sh` (línea 10) | **la línea `FLAGS` heredada**: `GEMV_TEMPERAMENTS=1`, `GEMV_W_S_BYSLOT`, `GEMV_W_F_BYSLOT` |
| `bronce/gemv_policy_bronce.py` (52-66) | cómo `GEMV_W_S` fija `cfg.w_s_pos`/`w_s_ten` sin tocar `DEFAULT_CONFIG` |
| `temperamentos_spec.md` (27, 89-110, 200-215) | tabla de perfiles por slot; **SELLO DE LA ERA**: ganancia agregada CONFIRMADA, división del trabajo **NO-LEY** |
| `the_pack_peldano1_spec.md` | spec sellada 2026-08-28: pregunta, cinco columnas, examen N=3 × 10.000t, brazo único |
| `the_pack_peldano1_paquete.md` | tablas (A)(B)(C) de las tres vidas — origen de "84 / 5" y de "72 % / 1 %" |
| `the_pack_censos_crudos.md` | los 24 censos crudos — `dist_nac_hub`, `heart_cuna`; **sin campo de perfil** |
| `the_pack_camino.md` | P1 CERRADO 2026-08-29; la frase citada; el estado de los peldaños |
| `pregonero/README_censo.md` | custodia de la métrica de minado (`cargo-delta` canónica) y resumen del sello |
| `reunificacion_censo.md` | (contexto, 29-jul) la pila de la era lleva `GEMV_W_S=1.40` horneado — **el BYSLOT es lo que lo sobreescribe** |
| `_tmp_gemv/` | **NO EXISTE**: los logs y `results.json` de las tres corridas no se conservan |
