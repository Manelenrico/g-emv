# SELLO P7-10 · el primer campo del siete, con la esperanza

*3-oct-2026, antes de pedir ninguna partida. Sustituye al sello de P7-8 (`SELLO_P7_8.md`), retirado por la mesa. El commit que añade este archivo es el commit del sello; su hash se apunta en `P7_10_estado.json` (`commit_sello`) y en el informe.*

## Lo que se juega

Cuatro brazos (SUELO, BORRADO, APRENDE, TECHO; `descubre_P7.py`, interruptores en la cabecera; con la esperanza, pieza H, el regalo que mira lo aprendido, pieza G, y el desempate sin hacer sitio, pieza I) × 20 días × 2 series = 160 partidas enteras, roster lento v2, mundo 0.1.19, liga de siempre, la misma semilla para los cuatro brazos cada día.
Semillas (`semillas_P7_10.json`, sucesión 20260916 + k·104729, k = 89..108, ninguna usada): serie 1 = [29581797, 29686526, 29791255, 29895984, 30000713, 30105442, 30210171, 30314900, 30419629, 30524358, 30629087, 30733816, 30838545, 30943274, 31048003, 31152732, 31257461, 31362190, 31466919, 31571648]; serie 2 = las mismas en orden inverso.
Cada criatura (asientos 10 y 11) lleva su cuaderno; en APRENDE viaja horneado en la imagen del día siguiente de su serie; BORRADO no lo lee; SUELO y TECHO no lo tienen. Imagen `Dockerfile.pareja_P7_8` (ARG BRAZO, CUAD); lanzador `lanza_P7_10.py`; lector `campo_P7_10.py`.
FRENO (corregido): primero APRENDE serie 1 días 1-3; se sigue solo si (a) el cuaderno viaja y se lee los días 2 y 3, (b) cero regalos de botiquines con creencia "no sé", (c) en al menos una criatura la creencia del botiquín sube y la ignorancia baja entre el fin del día 1 y el fin del día 3.

## Los archivos sellados (md5)

| archivo | md5 |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` |
| `cantera/paper7/cuaderno_P7.py` | `c452a30be823af157193e8705f5c3ef1` |
| `cantera/paper7/descubre_P7.py` | `76c0222dcd806cfb0747a9c70c38fe61` |
| `cantera/paper7/policy_pareja_P7.py` | `6eb8202a636e5de20ae8df794eb326a8` |
| `cantera/paper7/Dockerfile.pareja_P7_8` | `b4f554c8517e826ec4bf74d71586f5dd` |
| `cantera/paper7/lanza_P7_10.py` | `645d335007138d9db912238f5b722151` |
| `cantera/paper7/campo_P7_10.py` | `4b58f1d66e584b43962eeae4fbc4037d` |
| `cantera/paper7/semillas_P7_10.json` | `25eb92133e8c204269b2c55b0f751e6c` |
| `cantera/paper7/banco_P7_10.py` | `e10696b435c20d333a74b98378dc848e` |
| `cantera/paper6/policy_pareja11.py` | `e7136f856e6c09dd033bb4658cd135ea` |
| `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` |
| `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` |
| `planificador/planificador_v1.py` | `d0a3151d718e6b60d499e258c9dea9b1` |

## Las predicciones (de la mesa), con su medida

Un USO = ventana del canal `channeling first_aid` en el diario crudo que acaba con el botiquín gastado (baja el n a bordo); su vida es la del tic en que se abre; dentro/fuera por `zona` en ese tic. Igual para los cuatro brazos. Una CRIATURA de APRENDE = (serie, asiento): 4. Los días son los de cada serie por orden de juego. Creencia = `creencia` del cuaderno de fin (dominio cuerpo, situación dentro). Vida al morir = hp del último tic de la vida; puesto = `placement`.

- **P1. Aprende a esperar.** En APRENDE, la mediana de la vida al usar un botiquín en los días 16-20 es menor que en los días 1-5, en al menos 3 de las 4 criaturas (medianas sobre los usos gastados de esa criatura en esos días; una criatura sin usos en alguno de los dos tramos no cuenta a favor).
- **P2. Lo hace por lo que recuerda.** Días 11-20: la mediana de la vida al usar (todos los usos gastados del brazo) es menor en APRENDE que en BORRADO.
- **P3. La creencia sube.** Creencia del botiquín dentro del círculo al fin del día 20 mayor que al fin del día 5, en al menos 3 de las 4 criaturas de APRENDE ("no sé" cuenta como 0).
- **P4. Pero se queda corta.** Creencia final (fin del día 20, dentro) por debajo de 40 en al menos 3 de las 4 criaturas de APRENDE.
- **P5.** SUELO casi no usa botiquines (≤ 0,1 usos gastados por vida sobre sus 80 vidas); y TECHO usa con la vida más baja que APRENDE en los días 1-5 (mediana de la vida al usar, todos los usos del brazo en esos días).
- **P6.** Vida al morir y puesto: para cada par de brazos, emparejando por (serie, día, asiento), |d̄| ≤ 2·se (n = 80 pares) en las dos medidas.

Ningún número se ha calculado antes de jugar. `motor/model.py` intocable; el cuerpo congelado no se toca (los md5 de `decisor_zs.py` y `appraisal_zs_v42_exp.py` son los de `CONGELADO_P6.md`; `planificador_v1.py` el de `CONGELADO.md`).

## Apéndice (3-oct-2026, 22:30, tras el freno y antes de las 157 partidas restantes)

El freno (APRENDE serie 1, días 1-3) pasó: (a) el cuaderno viaja y se lee; (b) 0 regalos con "no sé" (día 3: 2 con creencia 26,4); (c) el asiento 10
pasa de "no sé" a creencia 29,3 e ignorancia 0,223. Al leerlo se vio un fallo de fontanería: con el canal abierto, el cuerpo regaló al hermano la
pila de botiquines (`soltar_first_aid` en los tics 10.051 y 10.335 del día 3, asiento 11); el canal siguió sin botiquín, la vida no subió y la ventana
lo apuntó como "cura 0, firme" dos veces. Arreglo, solo en `descubre_P7.ventana`: una ventana en la que el cuerpo elige regalar el botiquín queda
anulada (`regalado`), no se apunta. El cuaderno del día 3 del asiento 11 se rehízo desde las huellas con esa regla (`limpia_cuaderno_P7_7.py` →
`P7_10_res/cuaderno_s1_d3_APRENDE_11_limpio.json`: 7 recuerdos, 1 firme) y es el que viaja al día 4; el del asiento 10 no cambia. Las predicciones
no cambian. Los md5 nuevos:

| archivo | md5 |
|---|---|
| `cantera/paper7/descubre_P7.py` | `9f9080eed55968e5869597ef0c7c7b41` |
| `cantera/paper7/campo_P7_10.py` | `2f4e87140ecd8b589a225ac1e5672635` |
| `cantera/paper7/limpia_cuaderno_P7_7.py` | `754fae58ad6af07066f96f71b465d526` |
