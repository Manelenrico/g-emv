# P5-ARI · puntos 1 a 6 — los hechos de plataforma, para Ari

Reconstrucción **en seco**, **coste cero**. Motor, decisor y tabla intocados.

**Aviso de método, antes de nada.** No tengo el enunciado original de P5-ARI: en
el repositorio solo estaba el punto 7. He trabajado con tu lista abreviada, que
son **cinco temas para seis puntos**, así que **el punto que falta no lo he
inventado**: va señalado al final como hueco.

---

## 1 · Las horas exactas del parón, en UTC

**La plataforma dejó de programar trabajos durante 6 horas y 30 minutos, el 21
de septiembre de 2026.**

| | UTC |
|---|---|
| última petición que la plataforma **sí** programó | **2026-09-21 06:44:29Z** (`T/23926431`) |
| **primera petición que se quedó sin programar** | **2026-09-21 07:10:16Z** (`F/24031160`) |
| segunda, un segundo después | 2026-09-21 07:10:18Z (`T/24240618`) |
| **primera petición que volvió a arrancar** | **2026-09-21 13:40:43Z** (`F/24135889`), en cola 7,1 min |
| serie cerrada | **2026-09-21 14:19:15Z** |

**Duración del parón: de 07:10:16Z a 13:40:43Z = 6 h 30 min 27 s.**

*(El acta dice que la sonda de recuperación «arrancó a los 8 min»; los registros
dan **7,1 y 7,0 minutos**. La diferencia es de redondeo al informar, no de
dato.)*

### Cómo se cerró, sin intervención

`ciclo_P56C.py` quedó corriendo con las reglas que fijaste: cola vacía delante
de cada intento, sonda de dos episodios, **quince minutos para arrancar o
cancelación automática**, una hora de espera entre intentos, y los cuatro
restantes solo si la sonda costaba menos de 0,20 $ por episodio. Topes duros:
**nunca más de 6 episodios en toda su vida**.

**Cuatro sondas fueron canceladas antes de la buena, todas en `submitted` y
todas a coste cero comprobado.** La quinta arrancó y disparó el resto.

---

## 2 · Los episodios afectados — **son seis, no siete**

**No encuentro siete. Encuentro seis, y los doy con nombre y hora.** Si tu
séptimo sale de otro sitio, dímelo y lo busco.

| episodio | creada (final) | arranca | acaba | cola | precio |
|---|---|---|---|---|---|
| **F/24135889** | 13:40:43Z | 13:47:51Z | 13:56:17Z | 7,1 min | 0,074053 $ |
| **T/24135889** | 13:40:44Z | 13:47:45Z | 13:57:10Z | 7,0 min | 0,078709 $ |
| **T/24031160** | 13:57:54Z | 13:58:54Z | 14:08:37Z | 1,0 min | 0,107240 $ |
| **F/24240618** | 13:57:54Z | 14:09:35Z | 14:19:15Z | 11,7 min | 0,042024 $ |
| **F/24345347** | 13:57:55Z | 13:59:18Z | 14:09:43Z | 1,4 min | 0,055940 $ |
| **T/24345347** | 13:57:55Z | 13:59:13Z | 14:08:19Z | 1,3 min | 0,052699 $ |

**Los dos primeros son la sonda; los cuatro siguientes, el resto que la sonda
autorizó.** Las horas de creación que aparecen son las **finales**: las
peticiones originales de las 07:10Z fueron canceladas y vueltas a crear.

**Lo que estos seis demuestran, y es el dato que importa:** sus precios
—0,042 a 0,107 $— son **normales**. Los 0,78 $ y 0,21 $ que se habían visto
durante el parón **eran cola cobrada, no episodios caros**. El pod se factura
por minuto de vida, cola incluida.

### Las tres lecturas posibles de un «séptimo», por si alguna es la tuya

- **el episodio sin facturar de la tanda 2** (`ereq_90707b08`, F/20679832), que
  se reconsultó siete horas después y seguía con `cost_usd: null`;
- **las sondas canceladas**: fueron **cuatro**, de dos episodios cada una, todas
  a coste cero;
- **los rivales del roster**: son **siete** políticas distintas en los dieciséis
  puestos.

**Ninguna de las tres da «siete episodios» y no voy a forzar la que encaje.**

---

## 3 · La carga del 422, tachada

**Ocurrió en la primerísima experience request del proyecto, antes de gastar un
céntimo.** Está en `paintball/aliento_acta.md:118-135`.

El cuerpo JSON fue **rechazado con 422**, y un 422 **no crea nada y no cuesta
nada** — verificado en su momento contra el listado, que devolvió `entries: []`.

**La carga tachada, campo por campo:**

| ~~lo que se envió~~ | lo documentado en el `COOKBOOK.md` |
|---|---|
| ~~`roster: [{policy_ref}]`~~ | `roster: [{"player": {…}, "slot": 0}]` |
| ~~`policy_ref: "gemv-anima:v1"`~~ | `policy_ref` es un **UUID**, no una etiqueta |
| ~~`target.league_id`~~ | un `target` con **`league_name`** |

Quedaban además `private` y el rotate-seats, **cuyos nombres no aparecían en
ninguna documentación alcanzable**.

**La decisión que se tomó entonces, y que conviene que Ari conozca:** se podía
seguir a ciegas, porque **cada rechazo es gratis** — pero **un cuerpo aceptado y
equivocado sí gasta**, y gastaría en una configuración que no era la que se
quería medir. **Así que se paró y se pidió la petición a la mesa** en vez de
adivinar.

---

## 4 · El reintento del artefacto

**Un asiento jugó, puntuó, y la plataforma no produjo su diario.**

| | |
|---|---|
| episodio | **`K/20784561`, asiento 10** (P5-8M, tanda 2) |
| estado del episodio | **`completed`** |
| coste | **0,097807 $** — facturado con normalidad |
| el asiento | **tiene puntuación**: posición 10, score 1,0 |
| respuesta del servidor al pedir el artefacto | **`Agent 10 has no artifact. Available agent indices: 11`** |

**Se reintentó la descarga y el artefacto no existe.** No es un fallo de la
descarga ni del reintento: **el artefacto no se generó**. El asiento hermano
(11) del mismo episodio sí lo tiene.

**Consecuencia declarada en el informe de la serie:** P5-8M se cerró con **79
asientos de 80**, y la semilla 20784561 cuenta con **un solo asiento de K** en
todas las tablas.

**Es el único caso de todo el paper cinco:** 200 episodios de P5-6C, 40 de
P5-7C y 40 de P5-8M, y **un solo artefacto que no llegó a existir**.

---

## 5 · El bloque del patrocinador de `lento_v0`

**El hallazgo fue que el objeto `sponsor` hay que mandarlo ENTERO.** Está en
`ACTA.md:155-166`, y resolvió la duda que quedaba abierta de A2.

El bloque, tal como viaja hoy en `roster_lento_v1.json` dentro de
`game_config_overrides`:

```
sponsor = {
    "live": false,
    "budget_per_team": 600,
    "shop_opens_tick": 1680,
    "scripted_gifts": [ … 16 regalos … ]
}
```

**Los dieciséis regalos, con su estructura:** cada uno lleva `team`, `tick`,
`item_id` y `recipient_slot`. Dos por equipo y ocho equipos: **raciones** hacia
el tic ~2.000 y **botiquín** hacia el ~4.600, escalonados 24 tics entre equipos.
Nuestros asientos son el **10 y el 11**, del equipo F.

| lo que se aprendió | |
|---|---|
| mandando el `sponsor` **entero** | los **dieciséis** regalos sobreviven y el presupuesto sube a **600** |
| mandando solo parte | se perdían |

**Y el resto de `game_config_overrides` de `lento_v0`, para que Ari lo tenga
completo:** `max_ticks`, `freeze_ticks`, `stat_budget`, `zone` (con su
`schedule` de siete filas: 7296/7536/8076 hasta 14136/14376/14916), `sponsor`,
y `seed`, que es lo único que cambia entre partidas. **`league_mode` es
`solo`.**

---

## 6 · El punto que falta

**Tu lista tiene cinco temas y los puntos son seis. No sé cuál es el sexto y no
lo invento.**

Candidatos que aparecen en el acta y que encajarían con una auditoría de
plataforma, por si alguno es:

- **el `/spend` que da más que la cabecera** (`ACTA.md:1269`): «siete de
  `/spend`… y `/spend` da más que la cabecera»;
- **el 1.166 → 1.173: «siete, no ocho»** (`ACTA.md:1778` y `:1898`), que aparece
  dos veces en las ampliaciones;
- **el freno de gasto ciego**: sin la cabecera `X-Coworld-Spend-Usd` el freno
  **avisa de que va ciego** en vez de callarse.

**Dime cuál y lo escribo.**

---

## Una corrección que sale de esta auditoría

**Conté mal los episodios sin facturar, dos veces.**

En `informe_P58I_sonda5.md` escribí que el de P5-8I era «el **segundo** de la
serie», y en `informe_P58M.md` que el de P5-8M era «el **tercero** del paper
cinco». **Los dos números están mal.**

**El censo real de todo el paper cinco son SEIS:**

| serie | episodio |
|---|---|
| P5-6C | `F/20679832` · `F/22564954` · `F/23402786` |
| P5-7C | `A/20889290` |
| P5-8I | `A/20679832` |
| P5-8M | `A/21622393` |

**Seis de 200 episodios completados = 3,0 %.** El acta lo tenía bien —dice «3 sin
facturar» en P5-6C y «1 sin facturar» en P5-7C—; **el que sumó mal fui yo al
escribir los informes posteriores**, porque conté solo los que recordaba en vez
de ir al censo.

**Para Ari esto importa**, porque es la cifra que hay que darle: **seis episodios
completados con `cost_usd: null`**, ninguno con error, y uno de ellos
reconsultado siete horas más tarde sin cambio.

---

## Lo que no sé, marcado como tal

**No encuentro el séptimo episodio.** Doy seis con nombre y hora, y las tres
lecturas posibles de un séptimo.

**No sé cuál es el sexto punto de tu lista.**

**No he conciliado los importes con la consola.** Eso es el punto 7, que ya está
escrito en `informe_P5ARI_p7.md`, y allí digo lo mismo: los totales por día no
los tengo.

**Y las fechas del propio acta no son consistentes** —hay entradas de 23 y
24-sep intercaladas antes de otras de 22-sep—, así que **todas las horas de este
informe salen de los registros de los episodios, no del acta**. Son las que la
plataforma escribió.

---

`cantera/paper5/informe_P5ARI_p7.md` tiene el punto 7. **Gasto: cero.**

**PARO AQUÍ.**
