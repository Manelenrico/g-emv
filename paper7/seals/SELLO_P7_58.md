# SELLO P7-58 · Banco (coste cero): curiosidad por el progreso del aprendizaje

*13-oct-2026. Escrito y sellado ANTES de calcular nada (commit antes de mirar). Sin API, sin plataforma; la serie 3 de P7-56 y las piezas de P7-57 no se tocan. `motor/model.py` =
`1e511978c251130e95169ebf8443efa1`. Inspirado en Cowsik et al. 2026, «Self-Play Pretraining with Zero Data» (la señal de aprendizaje es el progreso, no la ignorancia).*

## La pieza (método de la mesa; `progreso_P7_58.py`, GEMV_P7_58=1)

- **Δ de una prueba**: cada recuerdo vivido sin corte de un objeto produce un cambio de creencia Δ_i = creencia del objeto en la situación del recuerdo (vector cuerpo, recursos, vínculo; regla del
  cuerpo: neutro de peso 1, olvido 0,95 por día, «al menos» solo si sube, en cuerpo) con los recuerdos hasta el i incluido − la misma sin él (sin recuerdos previos en esa situación: 0), vistas
  desde el día del recuerdo i. Intensidades en su escala (P7-47/48).
- **Producto bruto de la prueba i** = |Δ_i · m_i|, con m_i = media de los Δ de la ventana = las últimas ⌈n/2⌉ pruebas de ese objeto hasta la i incluida (n = pruebas de ese objeto hasta la i).
  Con una sola prueba la ventana es ella misma y el producto es |Δ_1|².
- **Progreso de la prueba i** = producto bruto / mediana de los productos brutos de TODAS las pruebas de todos los objetos vividos hasta ese momento (la i incluida; cadena honesta). Si esa
  mediana es 0, el denominador es el menor producto positivo hasta entonces (y si no hay ninguno, el progreso es 0).
- **Curiosidad del objeto** = media del progreso de sus últimas ⌈n/2⌉ pruebas. **Lo no probado** conserva la curiosidad de nacimiento, **1** (en su escala: tanto como un paso de aprendizaje
  mediano), hasta su primera prueba.
- Sustituye a ignorancia × importancia esperada en `filo_P7_40.curiosidad` (la cautela del probar sigue multiplicando, como en P7-40). Todo lo demás como P7-47: P7-40 + intensidad en su escala
  (`escala_P7_48`), sin habituación.

## Sobre qué

Los cuadernos y las vidas de APRENDE del campo P7-45: 12 criaturas (3 series × 2 asientos × 2 personalidades) × 20 días = 240 vidas, en cadena honesta (el cuaderno que escribe la réplica
del día d es el que lee el d + 1; lazo abierto), con las mismas definiciones de cierre y momento que P7-47.

## Criterios

| | criterio | pasa si |
|---|---|---|
| H1 | lo inútil (red y camuflaje) manda en ≤ 50 % de los cierres de día, y en ≤ 20 % de los cierres de los días 15-20 | «manda» = la clase con mayor curiosidad (cautela 1) al cerrar el día, entre las cuatro |
| H2 | en los momentos de decisión, coger lo inútil gana en ≤ 1/3 | momentos = tics en que el diario eligió `coger` con red o camuflaje a los pies + aperturas de pruebas de red y camuflaje; gana si la réplica elige `coger` |
| H3 | lo poco frente a lo nada: en los días 10-20, la curiosidad por la ración es mayor que por la red en ≥ 75 % de los cierres donde las dos se han probado al menos 3 veces | pruebas = recuerdos vividos sin corte en el cuaderno al cerrar |

**Regla de parada**: si H1, H2 o H3 no pasan, se informa y se para; queda para después del siete.
Se informa también: curiosidad por objeto y día (media de las 12 criaturas); y **cuándo se apaga la del botiquín** = por criatura, el primer día desde el que la curiosidad del botiquín al
cerrar queda por debajo de 0,5 (la mitad de la de nacimiento) hasta el día 20. Fidelidad de la réplica al diario.

## Añadidos posteriores al sello

(ninguno al escribirlo)
