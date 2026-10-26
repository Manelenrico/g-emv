# P7-17 · El pedido que se cierra al tenerlo (parte A)

*5-oct-2026. Coste: plataforma 0, consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar.
Solo banco: no se ha jugado nada. La parte B (el archivo al T7) está en `cantera/archivo_P7_17.md`.*

## Sección 1 · La regla (decisión de Manel, 5-oct, con la corrección de la mesa)

En pedir corregido (`GEMV_P7_PIDE2`, apagado por defecto; `pide_P7.pide2`):

- **Se abre** cuando la criatura no lleva botiquín, lo quiere (sus propias ganas: la promesa del botiquín mayor que cero), puede llevarlo (un hueco libre, o hacer sitio
  ganaría) y no ve ninguno (si ve uno, va a por él).
- **Se cierra solo** cuando lo tiene en el zurrón, o al morir. Ver uno no cierra un pedido ya abierto; tampoco tener la vida entera, ni dejar de caberle.
- Una criatura sana sin botiquín puede pedir uno de reserva. Se quita el cierre por «vida al máximo» de P7-16.

Las otras dos reglas de P7-16 siguen igual: solo se abre un pedido de lo que se podría coger, y la curiosidad no suma ganas de lo que no cabe.

**F1 sigue pasando** (`P7_17_F1.json`): apagado 1.007.274 tics iguales y 2 distintos; TECHO 1.007.274 y 2 (los dos de siempre).

## Sección 2 · El banco sobre P7-14b

`banco_P7_16.py` con la regla nueva → `P7_17_pedir.json` (el de la regla de P7-16 es `P7_16_pedir.json`). Las 320 vidas de P7-14b, una vida por proceso. La réplica sigue
el diario: dice qué parte habría emitido cada criatura en la vida que vivió. Fidelidad de la elección: pase 1, 4.069.814 tics iguales y 7.368 distintos.

| | ESPERANZA | BORRADO | APRENDE | TECHO | los cuatro |
|---|---:|---:|---:|---:|---:|
| pedidos abiertos en el campo (P7-14b) | 200 | 264 | 310 | 323 | 1.097 |
| pedidos abiertos, regla de P7-16 | 32 | 35 | 36 | 39 | 142 |
| **pedidos abiertos, regla de P7-17** | **101** | **118** | **113** | **104** | **436** |
| … cerrados porque lo lleva | 50 | 83 | 83 | 72 | 288 |
| … abiertos hasta el final de la vida | 51 | 35 | 30 | 32 | 148 |
| … abiertos por hacer sitio (partes) | 0 | 1 | 0 | 2 | 3 |
| partes con pedido en el campo | 2.566 | 3.029 | 1.939 | 1.933 | 9.467 |
| partes con pedido, regla de P7-16 | 755 | 914 | 890 | 934 | 3.493 |
| **partes con pedido, regla de P7-17** | **10.012** (47 % de los partes) | **5.920** (27 % de los partes) | **4.352** (21 % de los partes) | **7.733** (36 % de los partes) | **28.017** (33 % de los partes) |
| pedía en el campo y ahora no | 0 | 410 | 233 | 0 | 643 |
| no pedía en el campo y ahora sí | 7.446 | 3.301 | 2.646 | 5.800 | 19.193 |

**Los regalos** (pase 2: quien regaló oye los partes del hermano con la regla nueva; 1.883 partes cambian). «Siguen» = en el tic del regalo el hermano
estaría pidiendo y la réplica sigue eligiendo regalar.

| | regalos en el campo | siguen, regla de P7-16 | **siguen, regla de P7-17** |
|---|---:|---:|---:|
| APRENDE, los que recogió el hermano | 7 | 5 | **6** |
| APRENDE, los que volvían a quien los dio | 48 | 1 | **15** |
| APRENDE, todos | 56 | 6 | **21** |
| TECHO, los que recogió el hermano | 14 | 1 | **14** |
| TECHO, los que volvían a quien los dio | 23 | 1 | **23** |
| TECHO, todos | 37 | 2 | **37** |
| BORRADO, todos | 2 | 1 | **2** |
| **los cuatro brazos** | **95** | **9** | **60** |
| … de los que siguen, los recogió el hermano en el campo | 21 | 6 | **20** |
| … de los que siguen, volvían a quien los dio | 73 | 3 | **40** |

## Sección 3 · Lo que se lee

- **Los regalos que el hermano recogía se conservan**: 20 de 21 (con la regla de P7-16 quedaban 6). Quitar el cierre por la vida entera devuelve el regalo a un hermano sano sin botiquín.
- **En APRENDE, de los 48 regalos que volvían a quien los dio, 33 no se habrían hecho** y 15 sí. Los que desaparecen son los de un hermano con el zurrón lleno, que ya no pide.
- **En TECHO no cambia nada**: sus 37 regalos se habrían hecho igual, incluidos los 23 que volvían a quien los dio. En esos el hermano tenía hueco y pedía;
  por qué no los cogía no se miró en P7-15 (allí solo se miraron los de APRENDE) y este banco no lo dice.
- **Hay menos pedidos, pero duran mucho más**: se abren 436 (en el campo, 1.097), y los partes con pedido pasan de 9.467 a 28.017, un tercio de todos los partes
  (47 % en ESPERANZA). Un pedido ya solo se cierra al tener el botiquín: 288 de 436 se cierran así y 148 siguen abiertos hasta el final de la vida.
- **Hacer sitio casi nunca abre un pedido** (3 partes en todo el campo): con el zurrón lleno, en la práctica no se pide.
- **Lo que el banco no puede decir**: con el pedido abierto más tiempo, el hermano que tiene botiquines de sobra tendría muchas más ocasiones de regalar que en el campo
  (los partes con pedido se triplican). El banco solo mira los 95 tics en que el campo regaló; cuántos regalos NUEVOS habría, y si quien pide los cogería, solo lo dice un campo.
  Y como siempre: la réplica sigue el diario, y esto es código nuevo, que para jugarse pide sello nuevo.

## Archivos

| archivo | qué es |
|---|---|
| `pide_P7.py` (`pide2`) | la regla nueva, detrás de `GEMV_P7_PIDE2` (apagado por defecto) |
| `banco_P7_16.py` → `P7_17_pedir.json`; `P7_17_F1.json` | el banco con la regla nueva y F1 |
| `informe_P7_17.md` | este informe |
