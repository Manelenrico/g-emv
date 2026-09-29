# P5-6A — La política con formas, en vivo: construcción y humo

Sin partidas, coste cero, nada a la plataforma. Motor, decisor y tabla
intactos. **`policy_cortex.py` tampoco se ha tocado**, y no por promesa: la
política nueva **hereda de su `Alma`**, así que con los interruptores apagados
la decisión recorre exactamente el mismo código.

**Los ocho humos de A6 pasan, más tres añadidos, y los dieciséis del cuatro
siguen pasando dentro de la imagen.** Con todo apagado, la política con formas
decide **lo mismo que la del cuatro en 200 de 200 tics (100,00 %)**.

**Y encontré un fallo en el código que ya voló, que hay que decir antes de
nada.**

---

## El fallo del cuatro: la regla de los empates no corría

`policy_cortex.py:493-497`, literal:

```python
        if caja["nuevos"]:
            _cds = {k: v["d"] for k, v in radio["candidatos"].items()}
            _iny = set(caja["nuevos"])
            _prop = {k: v for k, v in _cds.items() if k not in _iny}
            _mj = min(_prop, key=_prop.get)
            if radio["elegido"] in _iny and not (_cds[radio["elegido"]]
                                                 < _prop[_mj] - 1e-9):
```

`caja["nuevos"]` guarda **IDs de propuesta** (enteros: `_k["nuevos"].append(v["id"])`),
y `radio["elegido"]` es un **nombre de candidato** (cadena). `cadena in
set_de_enteros` es **siempre falso**, así que `self.cx_empate` nunca se pone a
True y **la re-decisión que le devuelve el empate al cuerpo nunca se ejecuta**.
Veinte líneas más abajo, en `:521`, el mismo fichero lo hace **bien**
(`inyectados = {caja["de"][i] for i in caja["nuevos"]}`), lo que confirma que
era el mapeo que faltaba arriba.

**Medido en los 160 diarios de S2_B y S2_C**, no deducido:

```
ultimo cortex_resumen de cada diario (160):
   victorias_total 1908
   empates_al_cuerpo=0 160
```

Y recorriendo los `cortex_tic` con victoria y comparando la `d` de la propuesta
con la del mejor candidato propio:

```
  victorias con cortex_tic: 1908
  gano ESTRICTA: 1904
  EMPATE (deberia haber ido al cuerpo): 4

  empates emitidos como victoria: 4 de 1908 = 0.21%
   ejemplo: ('ereq_d7022d13-0b61-4ff', 1192, '_CX_ir_21_26', 3.6987, 3.6987)
   ejemplo: ('ereq_445169ca-8c36-4be', 1603, '_CX_ir_23_25', 3.92117, 3.92117)
```

**Consecuencia real: cuatro tics de 1.908 victorias, el 0,21 %.** Las cifras
del paper cuatro no se mueven. Lo que sí hay que corregir es la afirmación: la
regla «los empates son del cuerpo» **estaba escrita y no corría**.

**Por qué el humo del cuatro no lo cazó.** `humo_cortex.viii_empates` prueba
`D.decide` con su propia inyección y comprueba que un clon de `noop` no gana
por `d` estricta — eso es cierto y sigue siéndolo, pero es una propiedad **del
decisor**, no de la regla de la política. Nadie probó `Alma.decidir`.

Aquí la regla se escribe bien y **el humo (b2) la prueba donde vive**.

---

## A1 · La forma en vivo

### Lo que entra y cómo

| pieza | qué hace |
|---|---|
| **la cita** | cada `GEMV_FORMA_CADA` (100) tics, si el cuerpo no ha callado al consejero |
| **la instrucción** | la de P5-5B (B1) **más la tabla enseñada** (página nueva, abajo) |
| **el traductor** | `traductor_forma.py`, el mismo del banco |
| **la regla** | `forma.curva_H` + `forma.mejor_propia_H` + `forma.juzga_margen`, **sin tocar una línea** |
| **cuándo se juzga** | al proponerla, **al llegar a un punto de control y cada 25 tics** |
| **cómo compite** | el primer tramo entra en `D.candidatos` envolviéndolo desde fuera; la **ventaja del área** se aplica fuera, `d_ajustada = d − max(0, ventaja)`, igual que `banco_forma3.compite` |
| **cuándo se cae** | deja de ganar en una reevaluación · la vida real baja de la proyectada menos 10 · el destino deja de ser alcanzable |

**Una decisión de diseño que declaro.** `D.decide` ordena por `d` cruda y no
sabe de ventajas. Para no tocar el decisor, la ventaja se aplica **después**,
como en el banco: si la forma gana con ella, su acción se arma llamando a
`decisor_zs._a_json`, que es leer la API del decisor, no modificarla. Al
cambiar de candidato se deshacen las dos escrituras de memoria del epílogo de
`decide` (`cedidos` y `ultimo_ataque`); **el primer tramo de una forma es
siempre un `ir`, que no escribe ninguna de las dos**.

### El tiempo, y el hilo

Cada tic escribe un registro `tiempo_tic` con los milisegundos de la decisión y
los de la última evaluación de forma. **Si evaluar una forma pasa de 20 ms, la
política enciende `evalua_en_hilo`** y a partir de ahí las evaluaciones se
encargan al hilo (`EvaluadorHilo`), no al bucle del juego; el bucle las recoge
cuando vuelven, y queda anotado en `hilo_forma`.

### La tabla enseñada (página nueva)

`cantera/paper5/tabla_ensenada.md`. Nace de lo que P5-5B midió: el renglón que
el consejero nombra como causa solo cambia de verdad el 7,53 % de las veces, y
en las manos acierta **por debajo del azar**. La página dice, en una frase cada
uno, los cuatro sitios donde la tabla engaña:

- **`R-CARENCIA` solo baja con el arma EN LA MANO** (ni yendo a por ella, ni en
  la mochila);
- **`R-LLAMADA` SUBE al acercarte y se APAGA al coger** — es la única apetitiva;
- **`F-DANO` es la vida que falta**, nada más: un tramo que solo te mueve no lo
  cambia;
- **`S-8-EXPOSICION` depende de quién te ve**, no de adónde vas.

Y dos avisos más que salen del banco: los renglones del hermano **no empiezan
por S** (`F-HERMANO-GOLPE`, `F-HERMANO-AMENAZA`, `R-HERMANO-FALTA`), que fue el
error más repetido; y `S-COMPANIA` está callado y se nombró 167 veces.

---

## A2 · El hermano cuenta su forma

`paintball/alma/hilo_forma.py`. El mundo deja **120 ASCII imprimibles** y uno
cada 24 tics. Formato, versión 1:

```
GF1|<x.y.intención.tic>;<...>|<hp>,<W>,<herido>
```

con la intención en una letra (`i` ir · `c` coger · `u` usar · `e` esperar) y
`-.-` cuando el tramo es quedarse. **El peor caso medido son 61 caracteres** con
cuatro tramos y el estado entero.

**Una decisión que declaro:** el canal `team` ya lo usaba el parte de estado del
cuatro, cada 48 tics, y el mundo solo deja un mensaje cada 24. Así que **no se
mandan los dos**: con `GEMV_HILO_FORMA=1` el mensaje del hilo **es** la forma, y
se consigue envolviendo `parte.emite` desde fuera — `parte.py` no se toca,
igual que todo lo demás. Al aceptar una forma se fuerza la emisión siguiente.

Al recibir, las filas del hermano se evalúan en los puntos de control con su
forma contada; si hace más de **150 tics** que no cuenta nada, con su último
estado.

---

## A3 · La confianza por resultados

`paintball/alma/confianza_viva.py`. Distinta de la de P5-4: allí se comprobaba
lo **dicho** sobre los rivales; aquí lo **prometido** por la forma.

| | |
|---|---|
| C empieza en | **0,30** |
| acierto (`d_real ≤ d_proyectada + 0,05`) | **+0,10** |
| fallo | **−0,15** |
| margen de la puerta | **0,02 + 0,06 × (1 − C)** |
| el cuerpo calla al consejero | si **C = 0** y van **5** formas aceptadas que acabaron mal, **500 tics** |

Con C = 1 el margen es el 0,02 de P5-3H; con C = 0 es 0,08, **cuatro veces más
duro**. Confiar poco es pedir más ventaja. Cada cambio de C va al diario con la
forma y el punto de control que lo causó.

---

## A4 · El parte de la forma

En cada cita el consejero recibe, por tramo, **lo que él dijo que sentiría el
cuerpo** (los tres signos y el renglón), **lo que el cuerpo proyectó** y **lo
que el cuerpo sintió de verdad** si el tramo se vivió; más el registro de
aceptadas y rechazadas con su causa, y el valor de C. Cada parte se guarda en el
diario con la clave `parte`. Ejemplo real del humo (e):

```
Esto es lo que paso con tus formas desde la ultima vez:

- Forma 1 (2 tramos): ACEPTADA y luego caida.
  Se cayo porque la vida real 60 esta por debajo de la proyectada 90 menos 10.
  Tramo 1: dijiste vida +, manos 0, vinculo - por R-CARENCIA; el cuerpo proyecto vida -, manos 0, vinculo 0; y de verdad sintio vida -, manos -, vinculo 0.
```

---

## A5 · Formas al azar (brazo T)

`paintball/alma/formas_azar.py`. El control tiene que parecerse a lo que
controla, así que el número de tramos y las distancias **se sortean de la
distribución empírica medida** en las 334 formas traducidas de FORMAS/Haiku de
P5-5B, no de una inventada:

| tramos por forma | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **medido** | 14,07 % | 32,34 % | 38,02 % | 15,57 % |

**El 39,7 % de los tramos son «quedarse»**; las distancias van sobre todo de 1 a
6 casillas. La intención es `ir`, y `coger` si el destino tiene objeto. Pasa por
**la misma puerta y la misma confianza** (C se actualiza aunque no haya
consejero). Guardado en `P56A_distribucion_azar.json`.

---

## A6 · El humo, entero, con salida cruda

```
$ GEMV_CORTEX=0 python3 -u paintball/alma/humo_forma.py
humo (a) OK: con todo apagado, 200/200 tics con la MISMA decision que la politica del cuatro (100,00 %)
humo (b1) OK: el primer tramo entra como `_FM_ir_14_13` con ventaja 0.25
humo (b1) OK: elegido `ir_centro`, mejor `ir_centro` (d 3.52958); la forma quedo en d 3.73850
humo (b1) OK: GANA CUANDO DEBE — tic 241, forma `_FM_ir_14_13`: d 3.73850 menos ventaja 0.60 = 3.13850, contra 3.52958 del mejor propio; se lleva el tic y emite {"dir": "E", "do": "move", "type": "action"}
humo (b2) OK: se cae por la vida — la vida real 80 esta por debajo de la proyectada 100 menos 10
humo (b3) OK: se cae por el destino — el destino (14, 13) ya no es alcanzable
humo (b4) OK: con las piernas enfriando (10 tics) el cuerpo VETA la forma y no llega a la mesa
humo (b2) OK: en 25 tics ninguna forma se lleva el tic por empate; la regla que en policy_cortex.py no corre, aqui si
humo (c) OK:  61 ASCII, ida y vuelta identica · GF1|23.20.i.4312;-.-.u.4360;24.24.c.4470;-.-.e.4500|87,2.50,1
humo (c) OK:  15 ASCII, ida y vuelta identica · GF1||100,0.00,0
humo (c) OK:  24 ASCII, ida y vuelta identica · GF1|0.0.i.18240|1,3.52,1
humo (c) OK: la basura no decodifica
humo (d) OK: C 0,30 -> 0,40 (acierto) -> 0,25 (fallo); margen 0.0650
humo (d) OK: con C=0 y cinco formas malas el cuerpo calla al consejero 500 tics, y luego vuelve
humo (e) OK: el parte dice lo dicho, lo proyectado y lo sentido:
    Esto es lo que paso con tus formas desde la ultima vez:

    - Forma 1 (2 tramos): ACEPTADA y luego caida.
      Se cayo porque la vida real 60 esta por debajo de la proyectada 90 menos 10.
      Tramo 1: dijiste vida +, manos 0, vinculo - por R-CARENCIA; el cuerpo proyecto vida -, manos 0, vinculo 0; y de verdad sintio vida -, manos -, vinculo 0.

humo (e) OK: el parte viajo por el cable (503 bytes) y el manual va cacheado
humo (f) OK: 60 formas al azar, 0 destinos inalcanzables, tramos {1: 7, 2: 23, 3: 22, 4: 8}
humo (g) OK: el freno de llamadas muerde en 200 y calla al consejero
humo (g) OK: el freno de gasto muerde en 1.00 $
humo (g) OK: sin la cabecera X-Coworld-Spend-Usd el freno AVISA de que va ciego: «el freno de gasto NO protege; solo queda el de 200 llamadas»
humo (h) OK: artefacto subido UNA vez (748 bytes de zip, entrada `policy_agent_10.log`) con los ocho registros nuevos: forma_propuesta, forma_evaluada, forma_aceptada, forma_caida, confianza, parte, hilo_forma, tiempo_tic
HUMO DE FORMAS COMPLETO
```

**Qué prueba cada uno, y qué no.**

- **(a)** es la garantía más fuerte del encargo y **no depende de la suerte**:
  con `GEMV_FORMA=0`, `AlmaForma.decidir` hace `return super().decidir(obs)`,
  o sea es *literalmente* el código del cuatro. Las 200 decisiones se comparan
  serializadas contra una `PC.Alma` corriendo los mismos tics.
- **(b1)** tuvo que buscar un tic con **las piernas libres**: si están
  enfriando, el cuerpo veta la receta de `ir` y la forma no llega a la mesa —
  lo cual es correcto y se prueba aparte en **(b4)**.
- **(b1) «gana cuando debe»** es con la **ventaja del área**, como en el banco:
  una forma nunca bate al cuerpo por `d` cruda cuando su destino es una casilla
  contigua, porque eso es lo mismo que un `paso_*` que el cuerpo ya ofrece.
- **(g)** prueba los tres frenos, incluido el **ciego**: con un sidecar que no
  manda `X-Coworld-Spend-Usd`, el aviso salta.
- **(h)** escribe los ocho registros nuevos y comprueba que **están dentro del
  zip** que sube el relé, y que la subida se hace **una sola vez**.

**Un fallo mío, encontrado por el propio humo y arreglado.** La primera versión
de `_recarga` borraba el módulo de `sys.modules` para reimportarlo con otros
interruptores, pero `from alma import policy_forma` **devuelve el atributo del
paquete si existe**, sin reimportar: la prueba (b) corría con los interruptores
de la (a) y fallaba. Se arregla borrando también el atributo del paquete e
importando por `importlib`, y ahora `_recarga` **verifica** que los
interruptores quedaron como se pidieron.

---

## A7 · La imagen

```
$ docker build --platform linux/amd64 -f paintball/alma/Dockerfile.forma -t gemv-anima:forma .
$ docker image inspect gemv-anima:forma --format '{{.Id}}'
sha256:dd037e166ac0f8e0615743d8873de680ef23327be2bc1e95ca8a6e1beca7359e
```

Y los dos humos, corridos **dentro de la imagen**:



Y los dos humos, corridos **dentro de la imagen**:

```
$ docker run --rm --platform linux/amd64 -e GEMV_CORTEX=0 gemv-anima:forma \
      python -u /app/alma/humo_cortex.py
  ... (los dieciseis) ...
  HUMO S-2 COMPLETO

$ docker run --rm --platform linux/amd64 -e GEMV_CORTEX=0 gemv-anima:forma \
      python -u /app/alma/humo_forma.py
  ... (los ocho) ...
  HUMO DE FORMAS COMPLETO
```

El build **tumba la imagen** si falla cualquiera de estas capas: el md5 del
motor, **los md5 del decisor y de la tabla** (custodia nueva de este encargo),
la importación del alma, v40 apagada, la sonda de red, la instrucción y la
tabla enseñada dentro con su md5, la custodia anti-clave, **los dieciséis humos
del cuatro** y **los ocho de las formas**.

Las piezas del cinco (`forma.py`, `proyeccion.py`, `traductor_forma.py`,
`alcance_g.py`, la instrucción, la tabla y la distribución del azar) viajan a
`/app/alma/` **desde `cantera/paper5/`**: son las mismas que usaron los bancos,
y así no hay una copia divergente en el repo.

**La imagen viene APAGADA**: `GEMV_FORMA=0`, `GEMV_HILO_FORMA=0`,
`GEMV_CONSEJERO_FORMA=0`, `GEMV_FORMAS_AZAR=0`. Tal cual, juega el cuatro.

**NO se ha subido ni lanzado nada.**

---

## Los interruptores, crudo y efectivo

Como manda la regla del cuatro, el primer registro del diario lleva los dos:

```json
{"k": "arranque", "entorno_forma": {
  "crudo": {"GEMV_FORMA": null, "GEMV_HILO_FORMA": null,
            "GEMV_CONSEJERO_FORMA": null, "GEMV_FORMAS_AZAR": null,
            "GEMV_FORMAS_AZAR_SEMILLA": null, "GEMV_FORMA_CADA": null},
  "efectivo": {"FORMA": false, "HILO": false, "CONSEJERO": false,
               "AZAR": false, "AZAR_SEMILLA": 20260920, "CITA_CADA": 100,
               "MS_AL_HILO": 20.0, "TOPE_LLAMADAS": 200,
               "TOPE_GASTO_USD": 1.0, "CADA_REEVALUA": 25, "C0": 0.3,
               "SUBE": 0.1, "BAJA": 0.15, "MARGEN_BASE": 0.02,
               "MARGEN_RANGO": 0.06},
  "instruccion_md5": "401510e7ba6fd329ab0a2937818d954f",
  "tabla_md5": "a5bdb5cecd2cda3c9c5819e6764501f5"}}
```

**El freno de llamadas sube a 200** porque el mundo lento da hasta 182 citas a
una cada 100 tics; el de gasto se queda en **1,00 $**, como el cuatro.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

**Lo que el encargo pide:**

| fichero | md5 |
|---|---|
| `paintball/alma/policy_forma.py` | `d4f5e5a7394ddc5d3864c1ebd7e9b2c9` |
| `cantera/paper5/forma.py` | `b801876afda071403c5af54a28feff85` |
| `cantera/paper5/traductor_forma.py` | `b310bb72884ef5f4e3510ab803cd2776` |
| `cantera/paper5/proyeccion.py` | `bbc42daeaa769c783844997067ef148d` |
| `cantera/paper5/instruccion_forma.md` | `02653e4edf04f3bdd9a0ac3deda9aa01` |
| `cantera/paper5/tabla_ensenada.md` | `9d53807699c4ee2be31d8dd173196de0` |

*(La política hashea el texto **ya recortado**, que es lo que va al prompt:
`401510e7…` la instrucción y `a5bdb5ce…` la tabla. Los dos números son del
mismo contenido; el de arriba es el del fichero.)*

**Lo nuevo de apoyo:**

| fichero | md5 |
|---|---|
| `paintball/alma/forma_viva.py` | `7183091a30a46818178e2f3e281ab562` |
| `paintball/alma/confianza_viva.py` | `6e1e444435914f0b9df287ea37555bbc` |
| `paintball/alma/hilo_forma.py` | `aeea06ae4eb5b704e94fe845a5a5e5aa` |
| `paintball/alma/formas_azar.py` | `eefb5534e9533c8b742f7feb96239588` |
| `paintball/alma/humo_forma.py` | `65f0bb4d1fa6f40ba2111b7a749dc62d` |
| `paintball/alma/Dockerfile.forma` | `8259315fd214e200a5b5a0bc7ee24edf` |
| `cantera/paper5/alcance_g.py` | `bf62b03587506064311c122fd0e09102` |

**Lo que NO se ha tocado, comprobado por md5:**

| fichero | md5 | igual que |
|---|---|---|
| `paintball/alma/policy_cortex.py` | `6997b00c266f23d6037cc1a018f60a76` | el de S-3 del encargo |
| `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` | P5-3H |
| `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` | P5-3H |
| `paintball/alma/humo_cortex.py` | `302e7d691c17c719d4343ea92a943d90` | `informe_S2.md:415` |

**PARO AQUÍ.** Lo siguiente (P5-6B) son tres partidas, una por brazo, con precio
y humo en el campo, y necesita el sí de Manel.
