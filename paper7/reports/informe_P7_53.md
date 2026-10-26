# P7-53 · Banco (coste cero): la revisión de Ari al capítulo 4, sobre los datos de P7-50

*13-oct-2026. Sobre los 240 diarios válidos de P7-50 (nada se juega, nada se toca). `analiza_P7_53.py` → `P7_53_datos.json`; `escribe_informe_P7_53.py` (este informe; ninguna cifra a mano).
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Plataforma 0; consola 0 $.*

## 1 · Doble cuenta: ¿un uso de la hermana llegó como «visto» y además como «contado»?

Fusión por evento: mismo objeto, misma hermana, |tic de su ventana − tic en que lo vi| ≤ 240, el contado del mismo día por el canal o el de la noche siguiente con ese día como origen.

| brazo · hermana | vidas | vistos | contados (canal + noche) | duplicados (visto + contado del mismo uso) | peso extra de la segunda copia | peso total recibido | peso medio por recuerdo |
|---|---:|---:|---:|---:|---:|---:|---:|
| COMPARTE · valiente | 60 | 31 | 171 | 27 | 72,7 | 504,9 | 2,50 |
| COMPARTE · prudente | 60 | 16 | 159 | 16 | 25,1 | 354,8 | 2,03 |
| SOLAS · valiente | 60 | 0 | 0 | 0 | 0,0 | 0,0 | — |
| SOLAS · prudente | 60 | 0 | 0 | 0 | 0,0 | 0,0 | — |

**Sí: 43 de los 47 vistos de COMPARTE llegaron también contados** (canal 43; por objeto: camouflage 43), casi siempre en el MISMO tic (la hermana
cierra su ventana y la cuenta por el canal en el siguiente hueco del parte; yo la vi cerrar). El uso entró dos veces en el cuaderno: la copia vista (peso = su intensidad en mi escala × B) y la
copia contada (peso = la intensidad de ella × B). Peso extra de la segunda copia: 72,7 en las valientes y 25,1 en las prudentes (11,4 % de todo el peso recibido). Es un fallo de
diseño de `hermanas_P7_48` (no se fusiona el visto con el contado): para el siguiente campo, un uso = un recuerdo (fusión por hermana + instante ± ventana, quedándose con el contado,
que trae el efecto medido por ella, y anotando «visto» como confirmación). No se cambia nada a mitad de nada; queda apuntado.

## 2 · Distancia y vínculo

| brazo · hermana | distancia media a la hermana (casillas, las dos vivas) | fracción de tics con la hermana a la vista | roce_B medio | peso medio recibido (intensidad × B) |
|---|---:|---:|---:|---:|
| COMPARTE · valiente | 2,65 | 0,817 | 0,998 | 2,50 |
| COMPARTE · prudente | 2,70 | 0,824 | 0,998 | 2,03 |
| SOLAS · valiente | 2,67 | 0,843 | 0,998 | — |
| SOLAS · prudente | 2,71 | 0,853 | 0,998 | — |

Las parejas van pegadas en los dos brazos (≈ 2,6-2,7 casillas de media, a la vista el 82-85 % de los tics con las dos vivas) y **roce_B está saturado en 1** (0,998-0,998 de media): el peso «intensidad × B»
fue en la práctica la intensidad sola; la confianza según el vínculo no llegó a actuar en este campo (B solo baja sin la hermana, y aquí casi nunca falta). El peso medio recibido es
mayor en la valiente (2,50) que en la prudente (2,03) porque lo que recibe cada una es lo que vivió la OTRA: la prudente prueba más y con más intensidad.

## 3 · S1 releída

| serie | la que menos prueba (en SOLAS: pruebas 10 · 11) | en COMPARTE, recibidos y peso total: valiente (10) · prudente (11) | peso medio: 10 · 11 | distancia media: 10 · 11 | B: 10 · 11 | a la vista: 10 · 11 |
|---|---|---|---|---|---|---|
| 1 | asiento 11 (prudente; 83 · 54) | 73 · 184 frente a 57 · 113 | 2,52 · 1,98 | 2,46 · 2,45 | 0,998 · 0,998 | 0,83 · 0,81 |
| 2 | asiento 11 (prudente; 75 · 66) | 62 · 150 frente a 51 · 120 | 2,42 · 2,36 | 3,17 · 3,27 | 0,997 · 0,998 | 0,77 · 0,80 |
| 3 | asiento 10 (valiente; 69 · 93) | 67 · 170 frente a 67 · 122 | 2,54 · 1,82 | 2,33 · 2,37 | 0,998 · 0,998 | 0,85 · 0,86 |

- **¿La valiente recibió menos peso por estar más lejos?** No: la distancia y la vista son las mismas para las dos (es la misma pareja) y B ≈ 1 en todas; la valiente recibió MÁS peso
  (505 frente a 355 en 60 vidas), porque recibe lo que la prudente vive, y la prudente prueba más.
- **¿Cambia la lectura de «la que menos prueba aprende más»?** Sí, en dos cosas. (i) En las series 1 y 2 la que menos prueba (en SOLAS) es la prudente; en COMPARTE esa misma hermana
  recibió menos peso que su hermana (series 1 y 2: 57 · 113 y 51 · 120 frente a 73 · 184 y 62 · 150), y además probó MÁS por sí misma que en SOLAS (P7-50: 95 y 74 pruebas frente a 54 y 66):
  parte de su área del botiquín en COMPARTE es suya, no recibida. (ii) Como los dos cuadernos convergen (S2: 0,10 de diferencia frente a 4,11), el área de «la que menos prueba» en COMPARTE es
  en realidad el área de la pareja: S1 mide que la pareja que comparte cree más que la que menos prueba de la pareja que no comparte (689 frente a 425, +264 ± 135), no que la más
  callada aprenda de la otra. La lectura honesta: compartir iguala a las dos en lo que la pareja vivió, y la pareja que comparte prueba algo más; con 43 usos contados dos veces
  (11 % del peso), lo recibido pesó algo más de lo que el diseño decía. Los veredictos del sello (S1, S2, S3 no pasan) no cambian.

## 4 · Corrección en los textos: el camuflaje

Revisión de Ari (`obs.nim:32-44`): el camuflaje **limita a 4 casillas (quieta) o 7 (si se ha movido en los últimos 24 instantes) la distancia a la que te ven, frente a 8 o más
normalmente; atacar lo delata 5 s.** Lo que escribí («oculta más allá de 4/7 casillas hasta atacar») se corrige con una fe de erratas fechada al principio de `informe_P7_44.md`,
`informe_P7_47.md` e `informe_P7_52.md` (los informes no se reescriben); las medidas y los veredictos no cambian. La constante [impl] `CAMO_REVELADO_S = 5.0` de la appraisal
congelada coincide con los 5 s de Ari.

## Apuntes para la mesa (no se ejecuta nada)

1. Fusionar visto y contado por evento en `hermanas` (un uso = un recuerdo).
2. B saturado: si la confianza según el vínculo ha de actuar, hace falta que B se mueva (hoy solo baja sin la hermana); medir B en parejas que se separan (ninguna aquí) o cambiar su escala es decisión de la mesa.
3. S1 como está mide a la pareja; si se quiere medir «la callada aprende de la otra», la medida ha de descontar lo que la callada probó por sí misma ese día (p. ej. área atribuible a recibidos: creencia con y sin los recuerdos de origen contado/visto, recalculada del cuaderno).
