# SELLO P7-40 · Último banco antes del campo: la esperanza de clase y el miedo que calla el probar, no el mirar

*10-oct-2026, commit `b7d11da`. Escrito ANTES de calcular nada; commit antes de mirar un solo resultado. Plataforma 0 créditos; consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`.
Cuerpo y congelados sin tocar; solo banco; nada cambia en el campo todavía. Base: **B1 de P7-39** (importancia = |Δ malestar| sin las filas de la curiosidad ni las del acto,
sin contrafactual; neutro como UN recuerdo; curiosidad = ignorancia × importancia esperada; intensidad = 1 + importancia; cadena honesta; enganche por fuera de todas).*

## El diseño (decidido por Manel), con las definiciones fijadas

1. **Esperanza de clase.** El punto de partida de la importancia esperada de una cosa ya no es 1: es la **mediana de la importancia escalar de los recuerdos (sin cortes) de
   las OTRAS cosas conocidas de su clase**; si su clase no tiene nada conocido, la mediana de todo lo conocido (las otras tres cosas); si no se conoce nada (nacimiento), 1.
   Las clases: **consumibles** (botiquín, ración: `nace_P7_23.consumibles`) y **gear** (red, camuflaje: `nace_P7_33.gear`). «Conocida» = con al menos un recuerdo sin corte.
   El punto de partida sigue contando como UN recuerdo: importancia esperada = (p0 + Σ importancias) / (1 + N). Se recalcula en cada lectura (el día y la vida avanzan).
2. **El miedo calla el probar, no el mirar.** En peligro, la curiosidad de clase (la que entra en `R-CURIOSIDAD` y en la llamada de `ir_curioso`) se multiplica por la
   **cautela por distancia** de P7-26 (`nace_P7_23.cautela_de`: 1 sin rivales a 8 casillas o menos; baja linealmente hasta 0 con un rival a 2; 0 fuera del círculo o con la
   vida < 30): atenúa y, cerca, apaga el probar. Pero **lo que se ve en peligro y no se prueba deja un apunte**: cuando una cosa de las cuatro está a la vista
   (`obs.visible.items`), no la lleva, y la cautela es < 1, se abre una **mirada** de 10 s (240 tics; una por cosa a la vez; si en ese tiempo la coge, la mirada se descarta y
   la prueba es la que cuenta); al cerrarse, el apunte guarda la foto emocional del momento (recuerdo_P7_23.foto_de_radio) y la **intensidad de ese momento** = la importancia
   escalar del cambio de malestar filtrado en esa ventana (la misma medida que una prueba). El punto de partida de esa cosa pasa a ser el MAYOR entre el de su clase y la
   intensidad de sus apuntes. Los apuntes no son recuerdos (no entran en la ignorancia ni en la creencia); viajan de un día al siguiente con la cadena (`apuntes_P7_40_<asiento>.json`).
3. Curiosidad = ignorancia × importancia esperada (× cautela en peligro); intensidad = 1 + min(1, S/E) con la importancia filtrada; cadena honesta. Sin más cambios.

## Lo que se mide (lazo abierto: las obs y las pruebas son las del diario; lo que cambia es lo que la réplica decide y lee)

- Cadena: `banco_P7_40.py --cadena` (4 criaturas × 20 días, `filo_P7_40.py` sobre B1) → `P7_40_res/cuaderno_P40_*.json`, `P7_40_cadena.json`. Momentos: `--momentos` (los 71 tics
  de cogida y las 63 aperturas) → `P7_40_momentos.json`. Día a día: `cuaderno_P7_40.py` → `P7_40_cuadernos.json`.
- **I1-I4**: los mismos umbrales que P7-38 (I1 inútil ≤ 0,3 × botiquín; I2 «no hizo nada» ≤ 0,02; I3 lo inútil manda ≤ 40 de 80 cierres y ≤ 4 de los 24 de los días 15-20;
  I4 `coger` lo inútil ≤ 24 de 71).
- **I5 corregido** (motivo: comparar con P7-37 era comparar con una medida contaminada): al día 20, para cada criatura, |creencia − efecto real| del botiquín (dentro, cuerpo,
  sin cortes; efecto real 50, catálogo del mundo) y de la ración (15) no es mayor que en P7-37 por más de 0,10: |c40 − real| ≤ |c37 − real| + 0,10 en las 8 parejas
  (4 criaturas × 2 cosas). Se informa también el I5 antiguo (|c40 − c37| ≤ 0,10 en los 80 cierres).
- **E1 (Al filo del mañana)**: de los apuntes (lo visto en peligro y no probado, con la cosa aún sin recuerdos al abrirse), ≥ 60 % se «prueba antes que otra cosa no probada»:
  en el primer tic de calma (cautela = 1) posterior al apunte, en la misma vida o en la del día siguiente, en que alguna cosa sin recuerdos está a la vista, la clase sin
  recuerdos que más llama (curiosidad) es la del apunte. Un apunte sin ese tic en su día ni en el siguiente cuenta como no cumplido.
- **E2**: pruebas en peligro ≤ 13 de 63: de las 63 aperturas reales de red y camuflaje, las que están en peligro (`peligro_de`, P7-33) Y en las que la réplica con el miedo
  sigue eligiendo el acto que abre la prueba (`coger` en el tic de decisión anterior, o `ponerse_*`) son ≤ 13 (en P7-34 fueron 13 de 63 en peligro, P7-38).
- Se informa: el punto de partida de cada clase por día y criatura; el día en que lo inútil deja de mandar en cada criatura.

## Regla

Último banco antes del campo. Pase o no, el campo va con la mejor versión entre B1 (P7-39) y P7-40 (la que pase más de I1-I5; a igualdad, la que deje lo inútil mandando
menos cierres; a igualdad, B1), sin más bancos sobre lo inútil.

## Añadidos posteriores al sello

(ninguno al escribirlo)

1. (10-oct-2026, al construir, antes de calcular) **Empates en E1.** Al principio de cada vida todo lo no probado llama igual (misma ignorancia, mismo punto de partida); un apunte
   cuya cosa EMPATA en la mayor curiosidad cuenta como cumplido y queda marcado (`empate`); el informe da también la cuenta sin empates.
2. (10-oct-2026, al construir, antes de calcular) **Apuntes de más de un día.** Un apunte pendiente de hace más de un día se resuelve como no cumplido al cargar el día siguiente.
