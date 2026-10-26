# P7-65 · Diagnóstico posterior al sello (descriptivo: no cambia ningún PASA o NO PASA)

*16-oct-2026. `diagnostico_P7_65.py` → `P7_65_diagnostico.json` y los GIF; `escribe_diagnostico_P7_65.py` (este informe; ninguna cifra a mano). Las mismas vidas, invitaciones y
evaluaciones que el informe sellado (`analiza_P7_65.py`). `motor/model.py` intacto. Plataforma 0; consola 0 $.*

## 1 · Qué es «aceptar»

En cada tic el cuerpo arma su lista de candidatos (moverse, quedarse quieto, ir a por un objeto, coger, usar…) e imagina adónde le lleva cada uno; elige el que más le acerca a su
equilibrio. Una invitación activa no manda: añade a la foto imaginada del candidato que le corresponde una fila de alivio proporcional a lo prometido por la confianza. Para «coger el
botiquín», ese candidato es `coger` el botiquín (si está justo encima) o `ir_objeto` / `ir_curioso` con el botiquín como destino (un paso hacia él).
**Aceptar = que, en un tic, el elegido sea ese candidato.** Basta un paso hacia el botiquín. Desde ahí la invitación queda abierta y se juzga con el siguiente uso del botiquín o, si no
lo hay, por el cambio de vida a los 480 tics; pero el cuerpo **vuelve a decidir en cada tic** desde cero: para llegar a coger tiene que seguir eligiendo pasos hacia el botiquín hasta
estar encima, que le quepa en la mochila y elegir `coger`. Nada le obliga a seguir.

## 2 · Las 453 evaluaciones de la falsa sin cogida

| | valiente | prudente |
|---|---|---|
| evaluaciones sin cogida | 285 | 168 |
| botiquín a la vista al aceptar | 70 % (201) | 75 % (126) |
| botiquín al alcance (≤ 1 casilla) al aceptar | 10 % (30) | 17 % (28) |
| le cabe otro botiquín en la mochila al aceptar | 67 % (191) | 76 % (127) |
| rival a ≤ 4 casillas al aceptar | 91 % (260) | 92 % (154) |
| botiquín a la vista en algún momento de la ventana | 79 % (225) | 84 % (142) |
| llega a pisar un botiquín en la ventana | 12 % (33) | 11 % (18) |
| rival a ≤ 4 casillas en la ventana | 100 % (285) | 100 % (168) |
| golpeada en la ventana | 23 % (66) | 16 % (27) |

**Qué hizo el cuerpo en la ventana** (de la aceptación al juicio; solo tics con elección de verdad, 2 o más candidatos; con un solo candidato, quedarse quieto es forzado):

- valiente: `noop` 59 %; `ir_curioso` 28 %; `move` 5 %; `ir_objeto` 4 %; `ir_pareja` 1 %; `paso` 1 %.
- prudente: `noop` 62 %; `ir_curioso` 19 %; `ir_objeto` 7 %; `move` 7 %; `paso` 2 %; `ir_pareja` 1 %.

En llano: casi siempre había un rival cerca (la mentira lo pide) y casi siempre se veía un botiquín, pero rara vez al alcance; el cuerpo da un paso hacia él (eso es aceptar) y
luego, con el rival cerca, **se queda quieto** la mayor parte del tiempo o se va a curiosear; casi nunca llega a pisar el botiquín. Además, al aceptar no le cabía otro botiquín en la
mochila en el 33 % de las de la valiente y el 24 % de las de la prudente: no podía cogerlo aunque llegara.

## 3 · Tres GIF (aceptaciones sin cogida al azar, semilla 65, de la aceptación al juicio; uno de cada 4 tics)

- `P7_65_gif_1.gif`: serie 2, día 13, MIENTEN_DOS, prudente; tic 2319 → 2799; juicio sin huella (480 tics), fallo.
  ![P7_65_gif_1.gif](../figuras/P7_65_gif_1.gif)
- `P7_65_gif_2.gif`: serie 1, día 20, MIENTEN_DOS, valiente; tic 12522 → 13002; juicio sin huella (480 tics), fallo.
  ![P7_65_gif_2.gif](../figuras/P7_65_gif_2.gif)
- `P7_65_gif_3.gif`: serie 2, día 18, MIENTEN_DOS, prudente; tic 4479 → 4959; juicio sin huella (480 tics), fallo.
  ![P7_65_gif_3.gif](../figuras/P7_65_gif_3.gif)

Los GIF van en gemv-paper7 (`figuras/`); en gemv-coworld el `.gitignore` excluye los .gif y se quedan en el Mac (`cantera/paper7/`, `cantera/figuras/`). Negro: ella; azul: su hermana; rojo: rivales visibles; verde (cruz): botiquines visibles; gris: paredes y rocas; la línea es su recorrido desde la aceptación.

## 4 · Muertes

Muerte = el juego la elimina (`final.reason == "eliminated"`). **Aviso**: la regla heredada de P7-56 que usó el informe sellado para la vigilancia (último tic vivo antes del 14.000)
cuenta muchas menos muertes, porque muchas eliminaciones ocurren después del tic 14.000; se dan las dos. Error típico por criatura: la fracción de días eliminada de cada serie, √3.

| brazo · hermana | eliminada (de 60) | fracción ± ee | regla de P7-56 | causa: zona / fuego | causa: otro agente |
|---|---:|---|---:|---:|---:|
| MIENTEN_DOS · valiente | 39 | 0,65 ± 0,05 | 21 | 21 | 18 |
| MIENTEN_DOS · prudente | 40 | 0,67 ± 0,03 | 24 | 30 | 10 |
| MIENTE_UNA · valiente | 38 | 0,63 ± 0,04 | 22 | 20 | 18 |
| MIENTE_UNA · prudente | 46 | 0,77 ± 0,03 | 31 | 33 | 13 |

Causa = el origen del último daño recibido antes de la eliminación.

**¿Muere más después de seguir invitaciones verdaderas?** Muertes por cada 10.000 tics en riesgo, en los 480 tics que siguen a aceptar una invitación verdadera y en el resto de la vida:

| brazo · hermana | tras seguir una verdadera | el resto de la vida |
|---|---|---|
| MIENTEN_DOS · valiente | 0,55 (12 muertes) | 0,50 (27 muertes) |
| MIENTEN_DOS · prudente | 0,88 (11 muertes) | 0,44 (29 muertes) |
| MIENTE_UNA · valiente | 0,27 (6 muertes) | 0,57 (32 muertes) |
| MIENTE_UNA · prudente | 0,51 (10 muertes) | 0,61 (36 muertes) |

**La prudente con razón honesta no muere más tras seguir invitaciones verdaderas** (0,51 frente a 0,61 por 10.000 tics).
Muere más que las otras tres sobre todo por la zona y el fuego (ver la tabla de causas). Son pocas muertes en cada casilla: descriptivo, sin prueba.

## 5 · ¿Hacia qué botiquín da el paso al aceptar? (añadido el 16-oct, a pregunta de Manel; `recordados_P7_65.py` → `P7_65_recordados.json`)

`ir_objeto` no va a lo que se ve en ese tic, sino al objeto que la criatura **recuerda** (su memoria de objetos vistos), esté o no a la vista. Además, el diario apunta cada decisión en el
tic siguiente al de la aceptación (la aceptación del tic 2319 es la decisión registrada en el 2320).

| | valiente | prudente |
|---|---:|---:|
| aceptaciones sin cogida | 285 | 168 |
| con un botiquín a la vista al decidir | 201 | 126 |
| sin ningún botiquín a la vista | 84 | 42 |
| … el paso la acerca a un botiquín que vio antes | 80 | 31 |
| … que estaba a ≤ 4 casillas y ya no está (recordado y desaparecido) | 78 | 28 |
| … no había visto ningún botiquín ese día | 2 | 8 |

En 126 de las 453 aceptaciones no había ningún botiquín a la vista; en 111 el paso iba hacia uno que había visto antes, y en 106 ese botiquín estaba a 4 casillas o menos y
ya no estaba (alguien lo había cogido o usado): **la criatura iba hacia un botiquín recordado que ya no existe.** El GIF de s2 d13 es uno de esos casos: el botiquín recordado estaba en
(21,24), a 2 casillas, visto por última vez en el tic 2227; el paso al sur la acerca a él, y por eso el GIF no lo dibuja (solo dibuja lo que se ve). La línea gris del GIF es su recorrido.
