# P5-ARI · punto 7 — Qué llamó con clave propia y qué por el sidecar

Auditoría **en seco**, **coste cero**. Motor, decisor y tabla intocados.
**Solo nombres de variables: en este informe no aparece ni un valor de clave.**

*(Nota: en el repositorio no hay fichero de los puntos 1 a 6 de P5-ARI, así que
este va suelto en `informe_P5ARI_p7.md`. Si existe un P5-ARI en otro sitio,
habría que fundirlos.)*

---

## El titular

**Las tres fechas de la consola casan, y la que no aparece es la que más dice.**

| consola de Anthropic | qué fue | ruta |
|---|---|---|
| **14 y 15-sep** · Haiku 4.5 **y Sonnet 5** | los bancos del **paper cuatro** | **clave propia**, `CLAVE_BANCO_T3` |
| **20-sep** · Haiku 4.5 **y Sonnet 4.5** | **P5-5A y P5-5B** | **clave propia**, `ANTHROPIC_API_KEY` |
| **21 y 22-sep** · **nada** | **P5-6C y todo lo posterior** | **sidecar de Bedrock** |

**La prueba más fuerte del 14-15 no es la fecha, es el modelo: Sonnet 5 SOLO
puede haber ido por clave propia**, porque **el sidecar devuelve 403 para
`us.anthropic.claude-sonnet-5-v1:0`** (`informe_DM2.md §3`, recogido en
`informe_REV2.md` A7). Ese modelo no se puede llamar por la plataforma.

**Y el silencio del 21-22 es exactamente lo que el sidecar produce:** esos días
corrieron P5-6C y la serie entera, con miles de llamadas — pero facturadas por
la plataforma, no contra la cuenta de Anthropic.

---

## Una corrección a la premisa: **S-3 del cuatro NO fue con clave propia**

Me pediste confirmar que S-3 fue con clave propia. **No lo fue: fue por el
sidecar**, y la evidencia es del propio código.

El cuerpo de S-3 es `policy_cortex.py` con `cortex_t5.py`, y la cabecera de
`cortex_t5.py:8-10` lo dice sin rodeos:

> «La llamada va al **SIDECAR de Bedrock** (`docs/BEDROCK.md:8-25`): nunca al
> host real de AWS, nunca firmada, **sin ninguna clave nuestra**.»

Y las variables que usa son las del sidecar (`cortex_t5.py:682-683`):

```
AWS_ENDPOINT_URL_BEDROCK_RUNTIME
BEDROCK_MODEL
```

**El malentendido probable está en `--secret-env`.** `informe_S_CORTEX.md:3` dice
que los tres brazos «se distinguen sólo por `--secret-env`», y eso puede leerse
como que ahí viajaba una clave. **No: `--secret-env` se usó para pasar
interruptores**, como se ve en `forense_censo_temperamentos.md:57`
(`--secret-env GEMV_BRONCE=on --secret-env GEMV_CENSO=1`) y en los propios
brazos de S-CORTEX (`GEMV_CORTEX=0`). **Ningún `--secret-env` del repositorio
lleva un nombre de clave.**

**S-3 sí gastó en modelo** —su informe separa «72,36 $ de plataforma más 5,77 $
de modelo»— **pero ese gasto lo factura la plataforma, no la cuenta de
Anthropic**, y por eso no tiene por qué aparecer en tu consola.

---

## P5-6C por el sidecar: **confirmado**

El brazo F de la familia P5-6 se subió así (`ACTA.md:1111`, y el mismo cuadro en
`informe_P56B.md:40`):

```
GEMV_FORMA=1 · GEMV_HILO_FORMA=1 · GEMV_CONSEJERO_FORMA=1
--use-bedrock
--bedrock-model us.anthropic.claude-haiku-4-5-20251001-v1:0
```

Y el cuerpo que viaja en la imagen, `policy_forma.py:242-243`, lee **solo** las
dos variables del sidecar:

```
AWS_ENDPOINT_URL_BEDROCK_RUNTIME
BEDROCK_MODEL
```

**`policy_forma.py` no nombra ninguna clave propia en ninguna línea.** Lo único
que aparece con el nombre `consejero_forma` (`:251`, `:254`) es la **clave de un
registro del diario**, no un import del script local.

---

## Las dos rutas, separadas

### Ruta A — clave propia, **siempre en local, nunca dentro de una imagen**

| nombre de variable | dónde | quién |
|---|---|---|
| **`CLAVE_BANCO_T3`** | entorno de la máquina | **12 scripts del paper cuatro**: `banco_t3_api.py`, `banco_t4_api.py`, `banco_t5_api.py`, `dolores_ab.py`, `objetivo_ab.py`, `objetivo_ab_ter.py`, `parte_ab.py`, `parte_ab_DC.py`, `parte_ab_DM.py`, `parte_ab_DM2.py`, `profecia.py`, `profecia_bis.py` |
| **`ANTHROPIC_API_KEY`** | `cantera/paper5/.env` | **un solo fichero**: `cantera/paper5/consejero_forma.py` |

**Modelos que nombran estas dos rutas:**

| | modelos |
|---|---|
| `CLAVE_BANCO_T3` (paper 4) | `claude-sonnet-5` (`parte_ab_DM.py:34`), `claude-haiku-4-5` |
| `ANTHROPIC_API_KEY` (paper 5) | `claude-haiku-4-5-20251001` y `claude-sonnet-4-5-20250929` (`consejero_forma.py:29-30`) |

### Ruta B — sidecar de Bedrock, **siempre dentro de una imagen en la plataforma**

| nombre de variable | dónde |
|---|---|
| **`AWS_ENDPOINT_URL_BEDROCK_RUNTIME`** | `cortex_t5.py:682` · `policy_forma.py:242` |
| **`BEDROCK_MODEL`** | `cortex_t5.py:683` · `policy_forma.py:243` |

Se activa al subir la política con `--use-bedrock --bedrock-model …`. **El único
modelo que el sidecar sirve es
`us.anthropic.claude-haiku-4-5-20251001-v1:0`**; devuelve **403** para
`us.anthropic.claude-sonnet-5-v1:0` y `us.anthropic.claude-sonnet-4-6-v1:0`
(`informe_DM2.md §3`).

### La custodia que separa las dos rutas

`Dockerfile.forma:99-112` recorre `/app` entero y **tumba el build** si encuentra
el patrón de una clave de Anthropic:

```
pat = re.compile(rb"sk-ant-[A-Za-z0-9_\-]{10,}")
...
assert not mal, ("CLAVE DENTRO DE LA IMAGEN", mal)
print("custodia OK: ninguna clave sk-ant- en /app")
```

**Ese humo ha pasado en cada build de la serie.** Es prueba positiva de que la
clave propia nunca viajó a la plataforma: si hubiera viajado, no habría imagen.

Y `cantera/paper5/.env` está ignorado por git (`.gitignore:59`, patrón `*.env`),
comprobado con `git check-ignore`. **`git status` no lo ve.**

---

## La conciliación, fecha a fecha

### 14 y 15-sep · Haiku 4.5 **y Sonnet 5** → paper cuatro, clave propia

**Sonnet 5 solo pudo ir por clave propia**, porque el sidecar no lo sirve. Los
bancos que lo llaman son los del paper cuatro con `CLAVE_BANCO_T3`, y su informe
lo dice explícitamente (`informe_REV2.md:192`): «**`claude-sonnet-5`**, llamado
por la API de Anthropic, **no por el sidecar**».

Los experimentos D-M y D-M2 son los que usan Sonnet 5
(`apendice_numeros_p4.md:204-205`); los bancos t3/t4/t5 usan Haiku 4.5.

**Lo que NO puedo fijar: qué banco concreto cayó el 14 y cuál el 15.** Los
informes del paper cuatro no llevan fecha de ejecución, y la cuenta de llamadas
por día no está en el repositorio.

### 20-sep · Haiku 4.5 **y Sonnet 4.5** → P5-5A y P5-5B, clave propia

**Coincidencia exacta de los dos modelos.** `consejero_forma.py:29-30` declara
justo esos dos y ningún otro:

```
MODELOS = {"haiku":  "claude-haiku-4-5-20251001",
           "sonnet": "claude-sonnet-4-5-20250929"}
```

Y el acta fecha P5-5A y P5-5B el **20-sep-2026** (`ACTA.md:872` y `:938`), con
**«600 llamadas + 3 de humo, cero errores»**. **Es la única pareja
Haiku 4.5 + Sonnet 4.5 por clave propia de todo el repositorio.**

### 21 y 22-sep · nada → P5-6C y lo que vino después, por el sidecar

Del 21 al 22 el acta registra **P5-6C tandas 3 a 5, la ampliación entera y toda
la serie 8** — miles de llamadas del brazo F. **Ninguna aparece en tu consola, y
es lo correcto**: van por `--use-bedrock`, las factura la plataforma, y el gasto
se lee por la cabecera `X-Coworld-Spend-Usd` y el `/spend` del sidecar, no por
la cuenta de Anthropic.

**Que la consola esté vacía esos dos días es, de hecho, la confirmación
independiente de que P5-6C fue por sidecar.**

---

## Lo que no sé, marcado como tal

**Las fechas del acta no son consistentes y no me he apoyado en ellas.** Hay
entradas fechadas **23 y 24-sep** (P5-7B, P5-7C, P5-8A, P5-8B, P5-8C)
**intercaladas antes de entradas fechadas 22-sep**. He conciliado por **ruta y
por nombre de modelo**, que sí son verificables en el código, y solo he usado la
fecha del acta donde coincide con la consola (el 20-sep de P5-5A/B).

**No puedo repartir el 14 y el 15 entre bancos concretos**, por lo dicho: los
informes del paper cuatro no llevan fecha de ejecución.

**No he comprobado los importes.** Conciliar el gasto exacto pediría los totales
por día de la consola, que no tengo, y los del acta están en dólares de
plataforma y de modelo mezclados según el informe.

**Y no sé si `CLAVE_BANCO_T3` y `ANTHROPIC_API_KEY` son la misma clave.** Son dos
**nombres de variable** distintos; si detrás hay una sola clave o dos, eso solo
lo sabes tú, y no lo he mirado.

---

## Resumen para el acta

| serie | ruta | variable |
|---|---|---|
| bancos t3/t4/t5, D-C, D-M, D-M2, dolores, objetivo, profecía (paper 4) | **clave propia** | `CLAVE_BANCO_T3` |
| **S-2, S-3, S-CORTEX** (paper 4) | **sidecar** | `AWS_ENDPOINT_URL_BEDROCK_RUNTIME`, `BEDROCK_MODEL` |
| **P5-5A, P5-5B** | **clave propia** | `ANTHROPIC_API_KEY` (de `cantera/paper5/.env`) |
| **P5-6A, P5-6B, P5-6C** (brazo F) | **sidecar** | `AWS_ENDPOINT_URL_BEDROCK_RUNTIME`, `BEDROCK_MODEL` |
| **P5-7, P5-8 entera** | **ninguna**: el consejero va apagado | — |

**Las dos confirmaciones que pediste:**
- **P5-6C por el sidecar: SÍ**, confirmado por la subida de la política y por el
  código del cuerpo.
- **S-3 con clave propia: NO.** S-3 fue por el sidecar; lo dice su propio código
  y la separación de gasto de su informe es de plataforma, no de Anthropic.

**PARO AQUÍ.**
