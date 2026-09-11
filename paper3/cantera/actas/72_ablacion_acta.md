# Acta — LA ABLACIÓN DE CAMPO (dos v27-pareja) · **la atribución, con un matiz**

Fecha: 2026-09-05 · Rama `paintball` · Mac mini M4 (arm64)
Prompt: `paintball/PROMPT_72_ablacion_de_campo.md`

## Custodia

- `md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** al empezar y
  al acabar. **Liga en v19: no se tocó.**
- **Nada se construyó**: la imagen `v27-pareja` es el mismo código con los
  doce interruptores en OFF, montada en un **staging** (`/tmp/v27pareja`) para
  no tocar el proyecto vivo. Verificado al cierre: `appraisal_zs.py` del repo
  sigue en **`8a73bb306b4cf3ee`** (la v37 del 71), sin un byte cambiado.
- **Coste**: imagen `gemv-anima:v13` + tanda `xreq_6119d364-…`,
  **`cost_preview` = 20 cr** (≤ tope 25). 40/40 episodios, **80/80 diarios**,
  0 fallos.

---

# EL GATE (antes de gastar) — **VERDE en sus dos mitades**

**1 · ¿Es v27-pareja realmente v27?** Se comparó fila a fila y `State` a
`State` contra el **appraisal v27 histórico** (commit `aeac3f2`, congelado en
`paper3_cantera/codigo/appraisal_zs_v27.py`) sobre 6 escenas (hp 100/60/25 ×
con y sin hermana):

- **diferencias con v27: 0** · **filas sociales vivas: 0** — incluso **con la
  hermana delante y herida**.

**2 · Las fotos de la ánima sola**: bancos 13-28 + s7 corridos con los
interruptores apagados por defecto (como los tendrá la imagen): **12/12 OK**.

Sin este gate verde no se habría gastado un crédito.

## El roster, verificado

Idéntico al del 66 (`runs/xp_manada2_v35.json`) con las gemelas sustituidas
por `gemv-anima:v13`: los 10 UUID explícitos, **sin nuestra campeona**. En los
40 episodios: **0 participantes nuestros fuera de los asientos 10/11**.

---

# LA TABLA (72 ablación vs 66, n=40 y n=40)

| vara | **72 · v27-pareja (social OFF)** | 66 · v35 (social ON) | sello |
|---|---|---|---|
| **P1 defensas por la hermana** | **0** | 104 | **CUMPLE** |
| **P2 dones junto a la hermana** | **1** (en 1 ep) | 98 (en 13 eps) | **NO es 0 → forense** |
| **P3 respuestas propias** | **711** | 918 | **−22,5 %: dentro de ±30 % CUMPLE** |
| **P3 iniciaciones estrictas** | **0** | 0 | **CUMPLE** |
| **P4 distancia mediana entre hermanas** | **4,24** | 3,61 | **CUMPLE** (mayor sin imán) |
| **P6 golpes entre hermanas** | **0** | 0 | **CUMPLE** |
| **P6 ataques elegidos a la hermana** | **0** | 0 | **CUMPLE** |
| P5 score medio de la pareja | 3,12 | 2,65 | sin sello |
| P5 placement mediano | 12,0 | 12,0 | sin sello |
| P5 kills | 10 | 9 | sin sello |
| P5 top-4 del mejor | 8 (20 %) | 5 (12 %) | sin sello |
| P5 "ambas caen" (≥13) | 11 | 11 | sin sello |
| P5 una en pie a 8 | 14 | 12 | sin sello |
| estabilidad (cooldown / congelado) | 0 / 0 | 0 / 0 | — |

---

# EL FORENSE OBLIGADO (P2 = 1, no 0) — **y es un hallazgo**

La regla C exigía forense si P2 no era 0. El don único, entero:

- **Episodio** `ereq_9c3c18ad-f5d1-41a6-ae45-011ac603482e`, **tic 2002**,
  gemela **P11**: elige **`soltar_rations`** (raciones, no botiquín).
- Estado: yo hp 100 en (20,23) · hermana hp **60** en (21,22) · **dist 1,4**.
- **Filas encendidas**: `S-DANO-PAREJA 0,50` · R-CARENCIA 0,67 · F-4-ALCANCE
  0,49 · S-8 0,30 · R-ACOPIO 0,18 · R-LLAMADA 0,21.
- **Candidatos**: solo `noop` y `soltar_rations`.

**Qué significa**: lo movió **S-DANO-PAREJA**, que es una fila de **v19/v27**
—la del PROMPT_11/12, "la medicina junto a la cama"— y el candidato `soltar`
nace con hermana herida a la vista **desde el PROMPT_12**. El encargo listó
para apagar el parte, S-VINCULO, S-HERIDO, S-PROVISION, la manada, la
identidad y F-REENCUENTRO: **S-DANO-PAREJA y S-MUERTE-PAREJA no estaban en la
lista porque no son del paper tres**.

**El matiz para la sección de atribución, dicho con precisión**: la v27 **no
es asocial**. Lleva desde el PROMPT_12 una capa social mínima (el daño y el
duelo de la pareja) y con ella produce **una ración en cuarenta episodios**.
Lo que la comparación demuestra no es "asocial vs social", sino **social
mínima vs social completa** — y el salto es el que se buscaba: **1 → 98
dones** y **0 → 104 defensas**.

# LA LECTURA, APLICADA TAL COMO QUEDÓ SELLADA

- **P1 a 0 y P3 dentro de ±30 %**: se cumplen. **El cuerpo es el mismo**
  (711 vs 918 respuestas por el mismo repertorio; 0 iniciaciones en ambas) y
  **lo social es de las filas**: las defensas por la hermana caen a **cero
  absoluto** sin ellas.
- **P2 no es 0 → forense hecho, hallazgo declarado** (arriba). No se esconde y
  **cambia la frase de la sección 5**: la atribución se enuncia contra la
  línea base correcta (v27 con su social mínima), no contra un cuerpo mudo.
- **P5, en las dos direcciones y con R12 delante**: la ablación puntúa **algo
  mejor** (score 3,12 vs 2,65; top-4 8 vs 5) e **igual** en lo demás
  (placement 12 vs 12, "ambas caen" 11 vs 11). **A n=40 nada de esto es
  señal**: R12 exige ganar el 72 % de los pares y aquí ni siquiera hay pares
  —son dos tandas distintas, no un pareado—. Lo honesto: **lo social no ha
  comprado puntos, y tampoco se demuestra que los cueste.**

# LAS ESCENAS SEÑALADAS (visor hosted)

- **El don único** — `ereq_9c3c18ad` (t2002):
  <https://api.observatory.softmax-research.net/v2/coworlds/replays/static/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/sha256%3Ac96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9/index.html?v=2#replay=https%3A%2F%2Fsoftmax-public.s3.amazonaws.com%2Freplays%2Ffd29a144-14fd-49ce-8f48-05134cf14edd.replay>
- **Episodio de contraste** — `ereq_132cbd1c`:
  <https://api.observatory.softmax-research.net/v2/coworlds/replays/static/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/sha256%3Ac96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9/index.html?v=2#replay=https%3A%2F%2Fsoftmax-public.s3.amazonaws.com%2Freplays%2Feda0b7d3-b88c-4ff3-8a7f-cfe5b6e20494.replay>

# QUÉ QUEDA EN EL REPO

- `runs/ablacion/` — `episodios.json` (con `cost_preview`), 40 `res_*.json`,
  **80 diarios** (los ids completos están en `episodios.json`).
- `runs/xp_ablacion_v27.json` — el cuerpo de la tanda (roster reproducible).
- `gemv-anima:v13` subida (imagen `v27-pareja`). **v37 intacta**; liga v19.
- **Pendiente**: `runs/ablacion/` entera a la cantera del paper tres. La
  cantera está en `chmod a-w`; hay que desbloquear, copiar y volver a
  congelar — se hace cuando lo confirmes.

`md5 motor/model.py` = **`1e511978c251130e95169ebf8443efa1`** también al
cierre.

---

# LECTURA FRÍA

La crítica del paper dos era justa: todas nuestras ablaciones eran de banco, y
un banco prueba que no rompes lo que ya tenías, no que lo nuevo sea la causa
de lo nuevo. Esta tanda va al campo con las mismas dos hermanas, el mismo
mundo y el mismo roster, y con todo lo social apagado. El resultado es tan
limpio como se podía esperar: **las ciento cuatro defensas por la hermana se
convierten en cero**. No en pocas: en cero. Y las respuestas a los golpes
propios se quedan donde estaban —setecientas once contra novecientas
dieciocho, mismo repertorio, mismo cuerpo, cero iniciaciones en las dos—,
que es exactamente lo que hacía falta para poder decir que el cuerpo no
cambió y lo que cambió fueron las filas.

Pero hay un número que no salió como la mesa lo selló, y es el más
interesante del encargo. Se predijo cero dones y salió uno. Al mirarlo de
cerca, la gemela suelta unas raciones junto a su hermana herida a hp sesenta,
y quien la empuja es S-DANO-PAREJA —una fila del encargo doce, de la
temporada de la ánima sola—. Es decir: **la v27 nunca fue asocial**. Llevaba
desde entonces el dolor por la hermana y el gesto de dejarle la medicina al
lado, y con eso da una ración en cuarenta partidas. La comparación honesta,
la que hay que escribir en el paper, no es "cuerpo mudo contra cuerpo
social", sino **social mínima contra social completa**: de una ración a
noventa y ocho dones, y de cero a ciento cuatro defensas.

Queda la moneda, que se reporta como siempre en las dos direcciones: la
ablación puntúa un poco mejor y coloca igual. Con dos tandas sin parear y a
n cuarenta, eso no es una señal ni en un sentido ni en el otro. Lo que sí se
puede afirmar, y es lo que la sección de atribución necesitaba, es que **el
cuidado y la defensa no salen del cuerpo: salen de las filas**, y que sin
ellas la manada no aparece ni una vez.

---

## Reproducción

```bash
cd gemv-coworld
# gate (antes de gastar): v27-pareja == v27 historico, y bancos 13-28 con flags OFF
# tanda: xreq_6119d364…, cuerpo en runs/xp_ablacion_v27.json (roster del 66)
python3 - <<'PY'
import sys; sys.path.insert(0,"paintball")
from manada_campo import carga, honor_dos, golpes_entre
for t in ("ablacion","manada2"):
    f=carga(t); a,b,prop,ch,_=honor_dos(f)
    print(t, "defensas",b, "respuestas",prop, "inic",a, "golpes-hermanas",len(golpes_entre(f)))
PY
```
