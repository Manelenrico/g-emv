# SELLO P7-8 · el primer campo del siete

*3-oct-2026, antes de pedir ninguna partida. El commit que añade este archivo es el commit del sello; su hash se apunta en `P7_8_estado.json` (`commit_sello`) y en el informe.*

## Lo que se juega

Cuatro brazos (SUELO, BORRADO, APRENDE, TECHO; `descubre_P7.py`, interruptores en la cabecera) × 20 días × 2 series = 160 partidas enteras, roster lento v2, mundo 0.1.19, liga de siempre, emparejadas por semilla.
Semillas (`semillas_P7_8.json`, sucesión 20260916 + k·104729, k = 69..88, ninguna usada): serie 1 = [27487217, 27591946, 27696675, 27801404, 27906133, 28010862, 28115591, 28220320, 28325049, 28429778, 28534507, 28639236, 28743965, 28848694, 28953423, 29058152, 29162881, 29267610, 29372339, 29477068]; serie 2 = las mismas en orden inverso.
Cada criatura (asientos 10 y 11) lleva su cuaderno; en APRENDE viaja horneado en la imagen del día siguiente de su serie; BORRADO no lo lee; SUELO y TECHO no lo tienen.
FRENO: primero APRENDE serie 1 días 1-3; se sigue solo si (a) el cuaderno viaja y se lee los días 2 y 3, (b) cero regalos de botiquines con creencia "no sé", (c) al menos un recuerdo firme del botiquín.

## Los archivos sellados (md5)

| archivo | md5 |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` |
| `cantera/paper7/cuaderno_P7.py` | `c452a30be823af157193e8705f5c3ef1` |
| `cantera/paper7/descubre_P7.py` | `ff3bb96aa384ed9831630c0dbf7b05a4` |
| `cantera/paper7/policy_pareja_P7.py` | `6eb8202a636e5de20ae8df794eb326a8` |
| `cantera/paper7/Dockerfile.pareja_P7_8` | `b4f554c8517e826ec4bf74d71586f5dd` |
| `cantera/paper7/lanza_P7_8.py` | `a821a6006eecda9de578bc6031b2ca8a` |
| `cantera/paper7/campo_P7_8.py` | `a6553d0e162b57aa4896eaf131045210` |
| `cantera/paper7/semillas_P7_8.json` | `ff6c2fb5754cf0bab67e72cda145ca6e` |
| `cantera/paper7/banco_P7_8.py` | `a25ff85edcbf56347135013f0b245c34` |
| `cantera/paper6/policy_pareja11.py` | `e7136f856e6c09dd033bb4658cd135ea` |
| `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` |
| `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` |

## Las predicciones (de la mesa), con su medida

Un USO = ventana del canal `channeling first_aid` en el diario crudo que acaba con el botiquín gastado (baja el n a bordo); su vida es la del tic en que se abre; dentro/fuera por `zona` en ese tic. Por vida = por (serie, día, asiento). Días 11 a 20 = los días 11 a 20 de cada serie (por orden de juego). Igual para los cuatro brazos (`campo_P7_8.py`).

- **P1.** En APRENDE, la ignorancia del botiquín al acabar el día 10 (cuaderno de fin, `ignorancia`) está por debajo de 0,3 en al menos 3 de las 4 criaturas (2 series × 2 asientos).
- **P2.** Usos con la vida a 80 o más, media por vida, días 11 a 20: APRENDE < BORRADO / 2.
- **P3.** Usos con la vida por debajo de 50, media por vida, días 11 a 20: APRENDE ≥ TECHO / 2; SUELO casi cero (≤ 0,1 por vida).
- **P4.** Proporción de usos fuera del círculo (sobre todos los usos del brazo), días 11 a 20: APRENDE < TECHO.
- **P5.** Vida al morir (hp del último tic de la vida) y puesto: para cada par de brazos, emparejando por (serie, día, asiento), la media de las diferencias está dentro de ±2 errores típicos (|d̄| ≤ 2·se, n = 80 pares) en las dos medidas: ningún brazo se separa más allá del ruido entre semillas.

Ningún número se ha calculado antes de jugar. `motor/model.py` intocable; el cuerpo congelado no se toca (los md5 de `decisor_zs.py` y `appraisal_zs_v42_exp.py` son los de `CONGELADO_P6.md`).
