# SELLO P7-38 · Importancia contra lo que habría pasado sin la prueba (banco, coste cero)

*10-oct-2026, commit `4e284fc`. Escrito ANTES de calcular nada; commit antes de mirar un solo resultado. Plataforma 0 créditos; consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`.
Cuerpo y congelados sin tocar; solo banco; nada cambia en el campo. Sobre las 4 criaturas de APRENDE de P7-34 (80 cuadernos, 80 vidas) y los mismos momentos de P7-37.*

## La pieza (método, decidido por Manel)

1. **Importancia contrafactual, por dominio** (cuerpo, recursos, vínculo). Para cada prueba (ventana de uso del botiquín o la ración; ventana de 10 s de la red o el
   camuflaje), Δ_prueba = cambio del malestar del dominio en su ventana (`descubre_P7.malestar_ejes` del cierre menos el de la apertura: la importancia de P7-33).
   Δ_esperado = media del cambio del malestar en VENTANAS DE REFERENCIA de la misma duración SIN prueba, de la misma criatura, en situación parecida, usando SOLO su
   pasado hasta ese momento (los días anteriores enteros y el día en curso hasta la apertura; cadena honesta como en P7-37: la réplica del día d escribe lo que lee el día
   d+1). Importancia = |Δ_prueba − Δ_esperado|; si es menor que 1 desviación típica de los Δ de esas ventanas de referencia (por dominio), importancia = 0 («no hizo nada»
   en ese dominio). Si hay menos de 5 ventanas de referencia en la situación parecida, se usan las de cualquier situación de esa criatura y el recuerdo queda marcado
   (`referencia_cualquiera`). Con menos de 5 en total (día 1 al principio), la importancia queda como la de P7-33 y el recuerdo marcado (`sin_referencia`).
   - **Ventana de referencia**: un tramo [u, u+L] de la vida pasada de la criatura, con L la duración de la prueba (en tics), que empieza cada 12 tics (u múltiplo de 12,
     para no contar 14.000 ventanas solapadas por día), dentro de la misma vida, sin ninguna ventana de prueba abierta en ningún tic del tramo. Δ_ref = malestar(u+L) −
     malestar(u) por dominio. El malestar de cada tic se lee de la radiografía del presente (`RADIOGRAFIA.ahora`) de la réplica.
   - **Situación parecida**: la misma terna (dentro/fuera del círculo; golpeada en los últimos 48 tics o no; banda de hambre). El mundo no tiene hambre: la banda de
     hambre es la del dolor de recursos de la foto emocional (`dolor_R`, recuerdo_P7_23.foto_de_radio), en terciles del pasado de la criatura (bajo / medio / alto; con
     menos de 30 tics de pasado, una sola banda). Declarado.
   - La **intensidad** del recuerdo sigue siendo 1 + min(1, S/E) con S la suma de las importancias contrafactuales por dominio y E = 1,5 (cuaderno_P7); la importancia
     de P7-33 se guarda en el recuerdo (`importancia_P33`) y la contrafactual pasa a `importancia`. Lo demás del cuaderno (efecto, creencia, ignorancia, olvido) no cambia.
2. **Importancia esperada de una clase** = media simple de la importancia escalar (min(1, S/E)) de sus recuerdos sin cortes, con el neutro de nacimiento contando como UN
   recuerdo de importancia 1: (1 + Σ imp_i) / (1 + N). Sin olvido ni pesos (el neutro no se apaga; declarado: media simple, no ponderada por intensidad).
3. **Curiosidad de clase** = ignorancia (la de siempre: neutro / (neutro + pesos vividos)) × importancia esperada. Sustituye a `cuaderno.ignorancia(o)` en lo que leen la
   curiosidad de clase (`R-CURIOSIDAD`, nace_P7_29.curiosidad_M) y la llamada de clase (`ir_curioso`, nace_P7_33._cands), como en P7-37; las ganas (k) no cambian.

## Lecturas

- **A**: lo de arriba.
- **A+M** (solo para que Manel decida; no es diseño aprobado): A con la curiosidad atenuada por la cercanía del peligro (la cautela por distancia de P7-26/P7-37:
  `nace_P7_23.cautela_de`, 1 sin rivales a 8 casillas o menos, 0 con un rival a 2, fuera del círculo o con la vida < 30) y la mirada de científico (la forma y la situación
  preferidas, C5 de P7-37) solo entre situaciones sin peligro (dentro del círculo y sin golpe reciente). Se calcula sobre los mismos momentos a partir de las anotaciones
  de A (A × cautela), sin otra réplica.

## Lo que se mide y cómo

- **Cadena**: `banco_P7_38.py --cadena` (molde de P7-37): cada criatura, sus 20 días en cadena con la pieza A (`contrafactual_P7_38.py`, GEMV_P7_38=A); el cuaderno y las
  pistas del pasado (malestar por tic, situación, ventanas) viajan de un día al siguiente en la carpeta de la cadena. Salida: `P7_38_res/cuaderno_A_s<S>_d<D>_<asiento>.json`.
- **Momentos**: `banco_P7_38.py --momentos`: las 80 vidas con el cuaderno A del día anterior, lectura A, en los 71 tics de cogida de red o camuflaje (P7_36_cogidas.json) y las
  63 aperturas de prueba (P7_34_datos.json): qué elige la réplica; curiosidad A de cada clase; cautela; forma y situación preferidas (C5) entre todas y entre las sin peligro.
- **Día a día**: `cuaderno_P7_38.py` sobre los 80 cuadernos A: importancia (mediana) por cosa; «no hizo nada» (recuerdos de red y camuflaje con |efecto en el cuerpo| ≤ 1,
  definición de P7-34) y su importancia; curiosidad A por clase al cierre de cada día; quién manda; creencia de lo útil frente a los cuadernos de P7-37 (`P7_37_res`).

## Criterios (A), fijados antes

| | criterio | pasa si |
|---|---|---|
| I1 | la importancia de lo inútil | mediana de la importancia escalar de los recuerdos de red y camuflaje (cuadernos del día 20, sin cortes) ≤ 0,3 × la mediana de los del botiquín |
| I2 | «no hizo nada» no importa | mediana de la importancia escalar de los recuerdos «no hizo nada» (red y camuflaje con |efecto cuerpo| ≤ 1) ≤ 0,02 |
| I3 | lo inútil deja de mandar | la clase que más llama (curiosidad A) es red o camuflaje en ≤ 40 de los 80 cierres de día, y en ≤ 20 % de los 24 cierres de los días 15-20 (≤ 4) |
| I4 | coge menos | en los 71 momentos de cogida, la réplica con A elige `coger` en ≤ 24 |
| I5 | lo útil se queda | la creencia del botiquín y de la ración (dentro, cuerpo, sin cortes) en cada uno de los 80 cierres no se aparta más de 0,10 de la de los cuadernos de P7-37 |

Se informa también: el día en que cada criatura deja de tener lo inútil como lo que más llama (el primer día a partir del cual ya no manda ningún día más; «no llega» si
manda el día 20); y para A+M, cuántas de las pruebas reales de red y camuflaje (aperturas) y cuántos de los 71 momentos caen en peligro (`peligro_de` de P7-33) y en cuántos
la cautela habría apagado (0) o atenuado (< 1) la curiosidad.

## Añadidos posteriores al sello

(ninguno al escribirlo)

1. (10-oct-2026, al construir, antes de calcular) **Orden de los enganches.** La pieza se engancha por fuera de todas las del siete (envolviendo `nace_P7_33.aplica` en el
   banco), porque las ventanas de la red y el camuflaje se cierran en la pieza de P7-33; enganchada por dentro (como en P7-37) no las vería. Hallado al probar la pieza en
   una vida; P7-37 lleva su fe de erratas (4 recuerdos sin descontar).
2. (10-oct-2026, al construir) Los recuerdos cerrados antes de que la criatura tenga 5 ventanas de referencia (los primeros del día 1) quedan `sin_referencia` con la
   importancia de P7-33, como dice el sello; en el día 1 eso alcanza a las primeras pruebas de la red y el camuflaje, que se abren en los primeros 600-900 tics.
