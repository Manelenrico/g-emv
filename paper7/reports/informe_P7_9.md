# P7-9 · La esperanza, y otra vez el freno

*3-oct-2026. Coste: **créditos de la plataforma** 0,3240 USD en 3 partidas (por día 0,1082, 0,1075, 0,1083); **consola de Anthropic 0 USD**.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; los 202 congelados del cinco y los 32 del seis con su md5; el cuerpo no se toca: todo en
archivos `_P7`. Una vida por proceso; la memoria viaja solo en el cuaderno. Los números de método son los de la mesa.*

## Sección 1 · La esperanza, en el código

Pieza H de `descubre_P7.py` (`esperanza_cuerpo`, `mezcla`, `heal_imaginado`, `k_ganas`). Al imaginar usar el botiquín, la cura imaginada =
(1 − ignorancia) × creencia + ignorancia × esperanza, con esperanza = lo que hacen en el cuerpo los consumibles que el cuerpo conoce, tal como lo
tiene escrito: la media de `heal` del catálogo de los consumibles que no son el botiquín, hoy la ración, **15** (fuente: el registro `catalogo`
de los diarios). En recursos la foto ya pone la unidad gastada (−1) y en vínculo nada. Nunca probado (ignorancia 1): todo esperanza, cura imaginada
15; muy conocido: todo creencia. Ningún peso por la necesidad: de eso se ocupan las filas del cuerpo. La misma mezcla al imaginar tenerlo en el
zurrón: las ganas (R-ACOPIO, la rama "con una sola no basta", el término del botiquín en W y W_TARGET) escalan por k = mezcla sobre la
creencia máxima / cura del catálogo (nunca probado: 15 / 50 = 0,3). La creencia de la situación de ahora; si esa situación no tiene creencia
pero otra sí, la máxima (declarado). El regalo (pieza G, P7-8) sigue mirando solo lo aprendido (`k_creencia`, sin esperanza): con "no sé",
nada que regalar por su valor; queda a la mesa si la esperanza también debe entrar ahí (sección 6). Interruptor `GEMV_P7_ESPERANZA` (1 por
defecto; 0 solo en el banco "antes"). TECHO y apagado no la ven.

Corrección de la causa del corte (P7-8): el canal lo corta el daño recibido, no el movimiento; la regla de no apuntar ventanas sin gasto se
queda.

## Sección 2 · F1: apagado y TECHO reproducen A4

| brazo | tics iguales | distintos | los distintos |
|---|---:|---:|---|
| apagado | 1.007.274 | 2 | A4_21622393/10 t 1832; A4_21622393/10 t 2041 |
| TECHO | 1.007.274 | 2 | A4_21622393/10 t 1832; A4_21622393/10 t 2041 |

Los mismos dos tics de siempre. **F1 pasa** (`P7_9_F1.json`).

## Sección 3 · F2: en banco, sobre los diarios del freno de P7-8

Réplica de los seis diarios del freno de P7-8 (APRENDE serie 1, días 1 a 3, asientos 10 y 11; `banco_P7_9.py`), brazo APRENDE con el cuaderno
vacío (el botiquín desconocido), dos veces: sin esperanza (lo de antes) y con ella. Se registran los tics con un botiquín en el zurrón y la
vida por debajo de 50 (baja) o por encima de 80 (alta), sin el canal abierto. El mundo es el del diario: lo elegido no lo cambia.

| | tics | con el candidato `usar_botiquin` | lo elige | d(usar) − d(mejor), mediana / media | cura imaginada (mediana) |
|---|---:|---:|---:|---|---:|
| antes (sin esperanza), vida < 50 | 132 | 6 | 4 | 0,0000 / 0,1404 | 0,0 |
| antes (sin esperanza), vida > 80 | 41.602 | 7 | 7 | 0,0000 / 0,0000 | 0,0 |
| con esperanza, vida < 50 | 132 | 3 | 3 | 0,0000 / 0,0000 | 15,0 |
| con esperanza, vida > 80 | 41.602 | 6 | 3 | 0,0026 / 0,0044 | 15,0 |

Lectura. Con la vida baja, el candidato de usar casi nunca existe: de los 132 tics, en 129 el cuerpo solo tenía `noop` (el enfriamiento del
mundo tras cada acción; `Bloqueos`, decisor_zs.py:602-606) o el canal estaba abierto (excluidos). **Cuando existe, con esperanza lo usa siempre**
(3 de 3, con la vida a 35, 13 y 6 en el asiento 11 del día 1); antes lo usaba 4 de 6. La cura imaginada pasa de 0 a 15.
Con la vida alta (casi siempre a 100, donde el candidato no existe), con esperanza lo usa 3 de 6 (antes 7 de 7): la esperanza
también da valor al botiquín en el zurrón (k = 0,3), y gastarlo con la vida casi llena empieza a costar (d(usar) − d(mejor) = 0,0026 de mediana).
Lo que la trampa de la mesa predecía (con la vida baja, la imaginación no le ponía efecto a lo desconocido y no lo usaba) se ve en la cura
imaginada (0 → 15) más que en la elección: en el campo de P7-8 el asiento 11 ya intentaba usarlo con la vida baja (7 canales, los 7 cortados
por golpes). Fuente: `P7_9_F2.json`, `P7_9_F2_resumen.json`.

## Sección 4 · F3: el freno otra vez (APRENDE, serie 1, días 1 a 3, las mismas semillas de P7-8)

Imágenes: día 1: gemv-p7-campo:v4 (743d669b…), día 2: gemv-p7-campo:v5 (5e3dbfaf…), día 3: gemv-p7-campo:v6 (3ca47f5a…). Lector `campo_P7_9.py` → `P7_9_campo.json` (un uso = ventana del canal
`channeling first_aid` en el diario crudo; gastado si baja el n a bordo; cortado por daño si se cierra sin gasto en un tic con daño recibido).

| día (semilla) | criatura | vivo · puesto · causa (vida al morir) | coge (cómo) | regala | usos gastados (tic, situación, vida, curada; firme o al menos) | interrumpidos (cortados por daño) | cuaderno leído | al acabar: recuerdos (firmes / al menos), creencia cuerpo dentro, ignorancia |
|---|---|---|---|---:|---|---|---|---|
| 1 (27487217) | 10 | 14.254 · 1 · sobrevive (50) | 6 (por ganas 3, de paso 3) | 0 | 10625 dentro 78 +22 (al menos); 13132 dentro 67 +33 (al menos); 14124 dentro 86 +14 (al menos) | 0 (0) | no (día 1) | 3 (0 / 3), 17,96, 0,222 |
| 1 (27487217) | 11 | 14.088 · 4 · rival (2) | 3 (por ganas 2, de paso 1) | 0 | 11797 dentro 95 +5 (al menos) | 0 (0) | no (día 1) | 1 (0 / 1), 2,62, 0,476 |
| 2 (27591946) | 10 | 12.792 · 4 · anillo (2) | 7 (por ganas 4, de paso 3) | 0 | 1882 dentro 84 +16 (al menos); 10435 dentro 68 +32 (al menos) | 1 (1) | sí (día 2) | 5 (0 / 5), 20,05, 0,148 |
| 2 (27591946) | 11 | 14.184 · 3 · anillo (6) | 1 (por curiosidad 1) | 0 | 1760 dentro 92 +8 (al menos) | 0 (0) | sí (día 2) | 2 (0 / 2), 4,54, 0,311 |
| 3 (27696675) | 10 | 14.304 · 2 · sobrevive (2) | 18 (por ganas 8, por curiosidad 4, de paso 6) | 16 | 12051 dentro 83 +17 (al menos); 12674 fuera 78 +22 (al menos) | 1 (1) | sí (día 3) | 7 (0 / 7), 19,41, 0,111 |
| 3 (27696675) | 11 | 14.256 · 3 · anillo (5) | 10 (por ganas 3, por curiosidad 5, de paso 2) | 8 | 11902 dentro 97 +3 (al menos); 11971 dentro 89 +11 (al menos) | 0 (0) | sí (día 3) | 4 (0 / 4), 5,66, 0,186 |

Al lado, el freno de P7-8 con las mismas semillas y sin esperanza (`P7_8_campo.json`): día 1 asiento 10: usa 0 (interr 0), 0 firmes / 0 al menos, ignorancia –; día 1 asiento 11: usa 0 (interr 7), 0 firmes / 0 al menos, ignorancia –; día 2 asiento 10: usa 1 (interr 1), 0 firmes / 1 al menos, ignorancia 0,471; día 2 asiento 11: usa 1 (interr 0), 0 firmes / 1 al menos, ignorancia 0,465; día 3 asiento 10: usa 1 (interr 0), 0 firmes / 2 al menos, ignorancia 0,278; día 3 asiento 11: usa 0 (interr 0), 0 firmes / 1 al menos, ignorancia 0,477.

**(a) El cuaderno viaja y se lee**: sí, los días 2 y 3, las dos criaturas. **Pasa.**

**(b) Cero regalos con creencia "no sé"**: días 1 y 2, 0 regalos. Día 3, 16 del asiento 10 y 8 del 11, todos con creencia leída (19,4 y 5,7 de
cuerpo; k = 0,39 y 0,11): ninguno con "no sé". **Pasa** tal como está escrito. La cogida que se regala vuelve con fuerza en cuanto hay creencia
(día 3: 24 regalos de 28 cogidas; `soltar_first_aid` dos tics después de coger, con el hermano a la vista, que no lo recoge).

**(c) Al menos un recuerdo firme**: **no, otra vez.** Once usos gastados en tres días (el triple que en P7-8), todos con la vida entre 67 y 97
(67, 68, 78, 78, 83, 84, 86, 89, 92, 95, 97; diez dentro y uno fuera), y los once llenaron la vida hasta 100: once "al menos", cero firmes.
Dos canales cortados por daño (asiento 10, días 2 y 3), ninguno por movimiento. **El freno falla y el campo no sigue.**

**Lo que hizo la esperanza.** Comparado con P7-8 (mismas semillas): 45 cogidas (12 en P7-8), 11 usos gastados (3), 2 interrumpidos (8), y la
ignorancia del asiento 10 al acabar el día 3 en 0,111 (0,278). El cuerpo con esperanza quiere el botiquín desde el primer día (k = 0,3 sin haberlo
probado), lo coge, y lo usa en cuanto le falta vida: imaginando 15 de cura, usarlo con la vida a 85 ya alivia la foto. Y ahí está la trampa
que queda: con la cura real de 50 y el máximo en 100, **todo uso con la vida por encima de 50 toca techo** y queda "al menos"; la creencia de
los "al menos" (19,4 en el asiento 10, tres "al menos" entre 22 y 33 por encima del neutro) sube la cura imaginada (19,3 al usar el día 3), y
con 19 de cura imaginada el cuerpo usa aún antes. Para que un recuerdo sea firme hace falta usar con la vida por debajo de 50, y el cuerpo que
imagina 15 o 19 de cura ya no espera a eso. En seis días de freno (P7-8 y P7-9), cero recuerdos firmes; en los tres humos anteriores, uno (P7-7, día 3,
vida 14). Los P7_uso del día 3 del asiento 10: vida 83, 88 y 78, cura imaginada 19,3, 19,0 y 19,0 (`P7_9_campo.json`, `usos_P7`).

## Sección 5 · F4: créditos

Créditos de la plataforma: 0,3240 USD en 3 partidas enteras (por día 0,1082, 0,1075, 0,1083). Tres subidas de imagen (`gemv-p7-campo`), sin créditos. Consola de Anthropic: 0 USD. Acumulado del siete en la plataforma: P7-5 0,2660 + P7-6 0,1930 + P7-7 0,3265 + P7-8 0,3246 + P7-9 0,3240 = 1,4341 USD.

## Sección 6 · Lo que queda para la mesa

1. **El criterio (c) y el techo.** Con cura 50 y máximo 100, un recuerdo firme exige usar con la vida por debajo de 50; la esperanza (y luego la
   creencia de los "al menos") hace que el cuerpo use antes de llegar ahí. Es el diseño funcionando: imagina cura, le falta vida, se cura. Lo que
   hay que decidir es qué cuenta como "haber aprendido": (i) que los "al menos" cuenten para el freno y el sello (la ignorancia del asiento 10 ya
   es 0,11 y su creencia 19,4, y su conducta es la de un cuerpo que quiere y usa el botiquín); (ii) que el "al menos" se apunte como lo que
   realmente vio: una cota, y que la creencia firme solo pueda venir de usos con hueco (sigue sin llegar); (iii) una regla nueva de método para
   que el cuerpo con vida alta espere (número de la mesa). Si se rehace el sello de P7-8, P1 (ignorancia < 0,3 el día 10) ya lo cumple el freno
   el día 3 en ambas criaturas; P2 a P4 hablan de usos con vida alta y baja y hoy el cuerpo que aprende usa casi solo con vida alta.
2. **La cogida que se regala vuelve con creencia** (día 3: 24 de 28). El regalo mira lo aprendido (k = 0,39) y S-PROVISION (la hermana sin
   venda) lo paga; el hermano no lo recoge. Pregunta abierta de P7-7/P7-8: si la imaginación del regalo debe ver que no lo cogen, o si la
   esperanza debe entrar también en el regalo (hoy no: solo en usar y en las ganas, declarado).
3. **Hacer sitio oscila** (asiento 10: 4 y 7 oscilaciones ración ↔ botiquín los días 1 y 2) aunque el alivio ya no premia soltar: ahora es la
   esperanza (k = 0,3) contra el valor de la ración en W, y cada lado gana en su foto. Mismo remedio pendiente que en P7-7.
4. **Curar bajo fuego**: 2 canales cortados por daño en P7-9 (8 en P7-8). El cuerpo no sabe que un golpe corta el canal.
5. Pendiente para Ari: si el mundo salta un primer objeto que no cabe.

## Archivos

| archivo | qué es |
|---|---|
| `descubre_P7.py` (pieza H) | la esperanza en la imaginación de usar y en las ganas |
| `banco_P7_5.py --f1`, `P7_9_F1.json`; `banco_P7_9.py`, `P7_9_F2.json` | F1 y F2 |
| `lanza_P7_9.py`, `P7_9_estado.json`, `P7_9_res/`, `cuadernos_P7_9/`, `campo_P7_9.py`, `P7_9_campo.json`, `P7_9_diarios_manifiesto.md` | el freno (las mismas semillas de `semillas_P7_8.json`) |
| `escribe_informe_P7_9.py`, `informe_P7_9.md` | este informe |
