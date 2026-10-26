# SELLO P7-14b · el segundo campo del siete, con pedir, otra vez desde el día 1

*4-oct-2026, antes de pedir ninguna partida. Es el sello de P7-14 (`SELLO_P7_14.md`, commit 045b28f) con las mismas cinco preguntas, las mismas
medidas y el mismo freno, palabra por palabra, y tres cambios declarados: (1) el arreglo de la mesa tras el freno de P7-14: **en un empate no se da
ni se suelta nada** (`descubre_P7.desempate_sin_sitio` vale ahora para `soltar_*` además de `hacer_sitio_*`; mismo criterio de empate, ningún número
nuevo); (2) semillas nuevas, k = 132..151; (3) los nombres de los archivos (`P7_14b`). **Las 3 partidas del freno de P7-14 no cuentan para nada.**
El commit que añade este archivo es el commit del sello; su hash se apunta en `P7_14b_estado.json` y en el informe. Ningún número de este campo
se ha calculado antes de jugar.*

## Lo que se juega

Cuatro brazos, **ESPERANZA**, **BORRADO**, **APRENDE** y **TECHO**, los cuatro con pedir (pieza J, `pide_P7.py`, `GEMV_P7_PIDE=1`, solo el botiquín),
con el arreglo de P7-14 (la ignorancia descuenta una sola vez en las ganas) y con el de P7-14b (en un empate no se da ni se suelta nada).
**Ojos compartidos apagados** (`GEMV_OJOS=0`, parte E1 cada 48 tics), por decisión de Manel para todo el capítulo 3. × 20 días × 2 series = 160
partidas enteras, roster lento v2, mundo 0.1.19, liga de siempre; la misma semilla para los cuatro brazos cada día.
Semillas (`semillas_P7_14b.json`, sucesión 20260916 + k·104729, k = 132..151, ninguna usada): serie 1 = [34085144, 34189873, 34294602, 34399331, 34504060, 34608789, 34713518, 34818247, 34922976, 35027705, 35132434, 35237163, 35341892, 35446621, 35551350, 35656079, 35760808, 35865537, 35970266, 36074995]; serie 2 = las mismas en orden inverso.
Cada criatura (asientos 10 y 11) lleva su cuaderno; en APRENDE viaja horneado en la imagen del día siguiente de su serie; BORRADO no lo lee;
ESPERANZA y TECHO no lo tienen. Imagen `Dockerfile.pareja_P7_13` (ARG BRAZO, CUAD); las cuatro imágenes se hornean con el código de este sello.
Lanzador `lanza_P7_14b.py` (guarda de disco en 5 GB, limpieza de Docker tras cada horneado, espera de red); lectores `campo_P7_14b.py` y
`analiza_P7_14b.py`; evaluador `sello_P7_14b.py`; freno `freno_P7_14b.py`.

**FRENO:** primero APRENDE, serie 1, días 1 a 3. Se sigue solo si (a) el cuaderno viaja y se lee los días 2 y 3; (b) hay pedidos (al menos uno
abierto) y ningún regalo sin pedido; (c) en al menos una criatura la creencia del botiquín sube y la ignorancia baja entre el fin del día 1 y el
fin del día 3. Si algo falla, el campo para. Del freno solo se miran esas tres condiciones.

## Los archivos sellados (md5)

| archivo | md5 |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` |
| `cantera/paper7/cuaderno_P7.py` | `f4c6a9dae0af4831cfa930da18b74376` |
| `cantera/paper7/descubre_P7.py` | `5d6de90e491be8d8c6618263023a6534` |
| `cantera/paper7/pide_P7.py` | `4bc2ae5d3934a1be61944fa37d90b976` |
| `cantera/paper7/policy_pareja_P7_13.py` | `cbcf43ac1a67a78ee317e207c227f5c7` |
| `cantera/paper7/Dockerfile.pareja_P7_13` | `a7f97e4bedebf05499b1160a1d890105` |
| `cantera/paper7/lanza_P7_14b.py` | `04af05dee256157bae9515eeecf0d72f` |
| `cantera/paper7/campo_P7_14b.py` | `1f25698d4032b4064d977fedf680c5db` |
| `cantera/paper7/analiza_P7_14b.py` | `d6f870231b61ebec200fcec983369da8` |
| `cantera/paper7/analiza_P7_11.py` | `5ccc1bc0bef563e380691f1866c39c05` |
| `cantera/paper7/sello_P7_14b.py` | `20261bd1cdb3deee2ebd6c8b405b72a4` |
| `cantera/paper7/freno_P7_14b.py` | `c1870e9907f7925f6f8badf88a510d8a` |
| `cantera/paper7/semillas_P7_14b.json` | `968117a6bc88b5e6b1aa72c9876a9cbf` |
| `cantera/paper7/banco_P7_13.py` | `0e31cf5b9e5f7fe486036928a66f45f5` |
| `cantera/paper7/banco_P7_14b.py` | `b09c0d9f4f2b5cafbd6558f5cd82c9ee` |
| `cantera/paper6/policy_pareja11.py` | `e7136f856e6c09dd033bb4658cd135ea` |
| `paintball/alma/parte.py` | `80dabc2e78c7c36f0708a2d95e22262a` |
| `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` |
| `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` |
| `planificador/planificador_v1.py` | `d0a3151d718e6b60d499e258c9dea9b1` |

## Las preguntas (de la mesa), con su medida

Definiciones, iguales para los cuatro brazos. Un USO = ventana del canal `channeling first_aid` que acaba con el botiquín gastado; su vida es la del
tic en que se abre (`campo_P7_14b.py`, la de P7-10). Un REGALO = `soltar_first_aid` elegido y ejecutado (baja el número de botiquines a bordo).
VUELTO A COGER = la primera recogida en esa casilla después de soltarlo es de quien lo soltó (`analiza_P7_11.py`, destino «lo recoge el mismo»).
YENDO A POR BOTIQUINES = tics con ese candidato en curso (`analiza_P7_11.py`), como parte de los tics vivos de la vida. CREENCIA = la del cuaderno
de fin (cuerpo, dentro del círculo, con el recuerdo neutro, como en P7-10; «no sé» cuenta 0). Vida al morir = hp del último tic; puesto =
`placement`. Una CRIATURA de APRENDE = (serie, asiento): 4. PEDIDO ABIERTO = un parte con pedido tras uno sin él; CERRADO = un parte sin pedido
tras uno con él; se cerró PORQUE SE LO DIERON si entre el parte anterior y el del cierre el hermano ejecutó un regalo de botiquín (`analiza_P7_14b.py`).

- **Q1 (principal). Con pedir, APRENDE ya no acaba peor que BORRADO.** Emparejando por (serie, día, asiento), n = 80 pares: |d̄| ≤ 2·se en el puesto
  y en la vida al morir (las dos).
- **Q2. El círculo se rompe.** Regalos por vida de APRENDE ≤ la cuarta parte de los de P7-10 (171 en 80 vidas: tope 0,534 por vida); y botiquines
  vueltos a coger por quien los regaló, por vida, ≤ la décima parte (93 en 80 vidas: tope 0,116 por vida). Las dos. Las referencias se leen de `P7_11_vidas.json`.
- **Q3.** Días 11 a 20: la parte de la vida yendo a por botiquines, media por vida, de APRENDE no es mayor que la de BORRADO.
- **Q4. Se repite P7-10.** La creencia al fin del día 20 es mayor que al fin del día 5 en las 4 criaturas de APRENDE; y en los días 11 a 20 la
  mediana de la vida al usar (todos los usos del brazo) es menor en APRENDE que en BORRADO. Las dos.
- **Q5.** De los pedidos cerrados (los cuatro brazos juntos), menos de la quinta parte se cierran porque se lo dieron.

El sello se evalúa una sola vez, al final, con `sello_P7_14b.py`. Mientras se juega no se miran resultados de los brazos.
`motor/model.py` intocable; el cuerpo congelado no se toca.
