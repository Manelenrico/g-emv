# SELLO P7-39 · Último intento sobre lo inútil: la importancia mide solo el efecto del objeto (banco, coste cero)

*10-oct-2026, commit `a536ff6`. Escrito ANTES de calcular nada; commit antes de mirar un solo resultado. Plataforma 0 créditos; consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`.
Cuerpo y congelados sin tocar; solo banco; nada cambia en el campo. Sobre las 4 criaturas de APRENDE de P7-34 (80 cuadernos, 80 vidas) y los mismos momentos de P7-37/38.*

## Hallazgo que lo motiva (P7-38)

El fondo en 10 s de calma casi no se mueve; lo que se mueve en la prueba es la propia prueba, sobre todo el alivio de la curiosidad (`R-CURIOSIDAD`, 80 % en recursos), que
se apunta como efecto del objeto. Es un círculo.

## La pieza (método, decidido por Manel)

La importancia de una prueba mide SOLO el efecto del objeto. Del cambio de malestar por dominio entre abrir y cerrar la ventana (`descubre_P7.malestar_ejes`) se excluyen:
- las filas de la curiosidad: `R-CURIOSIDAD` y `R-CURIOSIDAD-CUANTO` (nace_P7_29);
- el acto de coger/llevar/caminar hasta él: las filas que leen el propio zurrón o tiran hacia el recurso, `R-ACOPIO`, `R-CARENCIA`, `S-PROVISION` (leen las unidades a bordo y
  cambian al coger, al llevar y al gastar) y `R-LLAMADA` (la fila apetitiva que tira hacia el recurso: caminar hasta él). Lista declarada aquí; el camino hasta el objeto
  anterior a la apertura de la ventana no entra en ninguna ventana (la ventana se abre cuando el objeto ya está a bordo o puesto).
El filtro se aplica en `descubre_P7.malestar_ejes` desde el banco (`efecto_P7_39.py`, GEMV_P7_39=1): lo ven la apertura y el cierre de las ventanas del botiquín, la ración
(nace_P7_23), la red y el camuflaje (nace_P7_33), y las pistas del contrafactual. Lo demás del cuerpo y de las piezas no cambia.

Dos lecturas:
- **B1**: sin contrafactual: importancia = |Δ malestar filtrado| por dominio (la ventana como en P7-37; enganche por fuera de todas las piezas, como en P7-38).
- **B2**: con el contrafactual de P7-38 (ventanas de referencia sin prueba, misma criatura y situación, solo el pasado; 0 si < 1 desviación típica), con el malestar filtrado
  también en las pistas.
Todo lo demás IGUAL que P7-38: importancia esperada = (1 + Σ importancias escalares) / (1 + N) con el neutro como UN recuerdo de importancia 1; curiosidad de clase = ignorancia
× importancia esperada (sustituye a `ignorancia` en `R-CURIOSIDAD` y en la llamada de clase); intensidad = 1 + min(1, S/E) con la importancia nueva; cadena honesta (cada
criatura sus 20 días; cuaderno y pistas viajan). Bancos: `banco_P7_39.py --cadena` (B1 y B2) → `P7_39_res/cuaderno_B1_*.json`, `cuaderno_B2_*.json`; `--momentos` (B1 y
B2) → `P7_39_momentos.json`; `cuaderno_P7_39.py` → `P7_39_cuadernos.json`.

## Criterios: los mismos cinco de P7-38, sin cambiar umbrales (para B1 y para B2)

| | criterio | pasa si |
|---|---|---|
| I1 | la importancia de lo inútil | mediana de la importancia escalar de los recuerdos de red y camuflaje (cuadernos del día 20, sin cortes) ≤ 0,3 × la mediana de los del botiquín |
| I2 | «no hizo nada» no importa | mediana de la importancia escalar de los recuerdos «no hizo nada» (red y camuflaje con |efecto cuerpo| ≤ 1) ≤ 0,02 |
| I3 | lo inútil deja de mandar | la clase que más llama es red o camuflaje en ≤ 40 de los 80 cierres de día, y en ≤ 20 % de los 24 cierres de los días 15-20 (≤ 4) |
| I4 | coge menos | en los 71 momentos de cogida, la réplica elige `coger` en ≤ 24 |
| I5 | lo útil se queda | la creencia del botiquín y de la ración (dentro, cuerpo, sin cortes) en cada uno de los 80 cierres no se aparta más de 0,10 de la de los cuadernos de P7-37 |

Se informa además: la ignorancia de lo inútil y de lo útil al día 20; el día en que lo inútil deja de mandar en cada criatura (el primer día a partir del cual ya no manda
ningún día más; «no llega» si manda el día 20); la creencia de la ración por día en B1 y B2 (frente a P7-37).

## Regla de parada (Manel)

Si ni B1 ni B2 pasan I1, I3 e I4, no se ajusta más: se declara como hallazgo y el campo va con la mejor de las dos (la que pase más criterios de los cinco; a igualdad, la
que deje lo inútil mandando menos cierres de día; a igualdad, B1 por ser la más simple).

## Añadidos posteriores al sello

(ninguno al escribirlo)
