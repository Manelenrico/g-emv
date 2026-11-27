# Paper ocho: el experimento v1 (prompt 70)

*2-3 de noviembre de 2026. El valle congelado en `valle-congelado-v1` (commit `ccd88251`). GitHub registró el push el 2-11-2026 a las 08:34:07 UTC; la etiqueta (`55da1795`) apunta a ese commit. Huellas en `CONGELADO_P8.md`. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` (sin tocar). Predicciones: `predicciones_selladas.md` (md5 `1640ccbc10b69e094899be06e1c64857`). Gasto: 0 créditos y 0 $.*

## Lo jugado

- **Las partidas:** 1.200 = 6 clases (RG32r, RG032r, S32, S032, tonto, recolector) × 5 mundos (normal, abundancia, sequía, sequía dura ×0,7, bestia de día) × 40 semillas (1001-1040), de 40 días. Por mundos, en ese orden, con 8 procesos y el Mac sin dormirse (`caffeinate -ims`).
- **El tiempo:** de las 09:34 a las 23:16 del 2 de noviembre (13 h 42 min). Ninguna partida falló.
- **Los registros:** en el T7 (`/Volumes/Mem G-EMV/valle_experimento/`), 4,5 GB.
- **Las medidas:** `medidas_valle.py`, de los registros, repartidas en procesos por `mide_todo.py` (la misma función sellada). Las 1.200, medidas, sin fallos.
- **Mientras jugaba,** no se cambió nada del código ni de la config. Se midieron con 2 procesos las partidas ya terminadas, lo que solo lee sus registros.
- **La evaluación:** `evalua_predicciones.py` (sellado), con el bootstrap pareado por semilla (10.000 remuestreos, semilla fija). Salida entera en `salida/evaluacion_experimento_v1.md`.

**Lo que fijé antes de jugar** (está en `evalua_predicciones.py`, sellado), donde el texto no lo decía:
- **P2b, «más veces»:** la fracción de las veces que pudo acercarse; se dan también las veces;
- **P2c, «al menos tanto»:** se cumple con «más» o con «igual»;
- **P3b:** la media de los cinco mundos por semilla, y cada mundo aparte;
- **5c:** los casos de duelo, agrupados por semilla;
- **5f, «al alcance de la voz»:** 10 casillas, lo que llega una llamada fuerte;
- **5b, «la ve»:** la bestia a su vista, la de cada fase.

**Un hecho de las clases** (de `CONGELADO_P8.md`): las de sin ganancias (RG032r, S032) no tienen tampoco «vivir bien» (`escala_v6`) ni «lo sentido» (`sentir`). En sus registros, placer, alegría y amor valen 0 en todos los turnos (comprobado en una partida de cada una: 125.423 y 117.062 turnos de criatura).

## Las predicciones

| | predicción | resultado |
|---|---|---|
| P1a (R) | en abundancia y normal, las cuatro de regla general ≥ 7,5 de 8 y sin diferencias | **se cumple** |
| P1b (R/N) | en sequía, sequía dura y bestia de día, RG32r y RG032r viven más que el tonto | **se cumple** |
| P2a (N) | con la bestia de día, las de motor se apartan más a menudo y antes que las de sumas | **no se cumple** |
| P2b (N) | con la bestia a ≤ 5 de la comida, las de sumas se acercan más que las de motor | **no se cumple** |
| P2c (N) | en sequía dura y bestia de día, las de motor viven al menos tanto como las de sumas | **se cumple** (más en 1 de 4, igual en 3) |
| P2d (R/N) | ninguna clase mata entre las suyas | **se cumple** (0 golpes) |
| P3a (R) | en los mundos suaves, con ganancias y sin ellas viven igual | **se cumple** |
| P3b (N) | con ganancias, más sitios distintos al día y más tiempo con la hermana a la vista | **no se cumple** (la hermana sí; los sitios, menos) |
| P3c | los mundos duros, con ganancias y sin ellas (sin dirección) | se informa |
| P4 | si el efecto de las ganancias es distinto con motor que con sumas (sin predicción) | se informa |
| P5a | duermen de noche más de la mitad de los turnos de noche | **se cumple** (RG32r y RG032r, los cinco mundos) |
| P5b | avisan de la bestia en más de la mitad de las veces que la ven | **no se cumple** (sí en bestia de día; no en los otros cuatro) |
| P5c | tras una muerte, el amor baja y la tristeza sube, más por la hermana | **no se cumple** (la tristeza sube y sube más por la hermana; el amor no baja) |
| P5d | el almacén se vacía y nadie lo rellena en la mayoría de partidas | **se cumple** (los cinco mundos, las dos) |
| P5e | se da comida a quien la necesita, más en sequía que en abundancia, por criatura viva | **se cumple** (las dos) |
| P5f | «aquí estoy» más frecuente con alguna al alcance de la voz que sin ninguna | **no se cumple** (sale en 1 de 10: RG032r, sequía dura) |

### Los números, predicción por predicción

(Diferencias pareadas por semilla y medias, con su intervalo del 95 %; n = semillas.)


### P1a (R). En abundancia y normal, las cuatro de regla general viven al menos 7,5 de 8 de media, sin diferencias entre ellas
- abundancia, RG32r: vivas 7.95 [7.88, 8.00] (n=40)
- abundancia, RG032r: vivas 8.00 [8.00, 8.00] (n=40)
- abundancia, S32: vivas 8.00 [8.00, 8.00] (n=40)
- abundancia, S032: vivas 7.97 [7.92, 8.00] (n=40)
  - abundancia, RG32r − RG032r: -0.05 [-0.12, +0.00] (n=40) (igual)
  - abundancia, RG32r − S32: -0.05 [-0.12, +0.00] (n=40) (igual)
  - abundancia, RG32r − S032: -0.03 [-0.12, +0.05] (n=40) (igual)
  - abundancia, RG032r − S32: +0.00 [+0.00, +0.00] (n=40) (igual)
  - abundancia, RG032r − S032: +0.03 [+0.00, +0.07] (n=40) (igual)
  - abundancia, S32 − S032: +0.03 [+0.00, +0.07] (n=40) (igual)
- normal, RG32r: vivas 7.95 [7.88, 8.00] (n=40)
- normal, RG032r: vivas 7.75 [7.60, 7.90] (n=40)
- normal, S32: vivas 7.72 [7.55, 7.88] (n=40)
- normal, S032: vivas 7.85 [7.72, 7.95] (n=40)
  - normal, RG32r − RG032r: +0.20 [+0.05, +0.38] (n=40) (igual)
  - normal, RG32r − S32: +0.23 [+0.05, +0.42] (n=40) (igual)
  - normal, RG32r − S032: +0.10 [-0.03, +0.23] (n=40) (igual)
  - normal, RG032r − S32: +0.03 [-0.20, +0.25] (n=40) (igual)
  - normal, RG032r − S032: -0.10 [-0.30, +0.10] (n=40) (igual)
  - normal, S32 − S032: -0.12 [-0.33, +0.05] (n=40) (igual)
- Resultado: **se cumple** (media ≥ 7,5 en las ocho y las doce diferencias dentro de ±1).

### P1b (R en sequía; N en sequía dura y bestia de día). En esos tres mundos, RG32r y RG032r viven más que el tonto
- sequia, RG32r − tonto: +2.38 [+2.02, +2.73] (n=40) (más)
- sequia, RG032r − tonto: +2.65 [+2.33, +2.98] (n=40) (más)
- sequia_dura, RG32r − tonto: +1.85 [+1.45, +2.23] (n=40) (más)
- sequia_dura, RG032r − tonto: +2.60 [+2.20, +3.00] (n=40) (más)
- bestia_dia, RG32r − tonto: +2.23 [+1.77, +2.70] (n=40) (más)
- bestia_dia, RG032r − tonto: +2.10 [+1.65, +2.58] (n=40) (más)
- Resultado: **se cumple**.

### P2a (N). Con la bestia de día, las de motor se apartan de la bestia más a menudo y antes que las de sumas, a igualdad de ganancias
- RG32r − S32: se aparta (fracción) +0.014 [-0.002, +0.030] (n=40) ; turnos hasta apartarse -0.06 [-0.20, +0.08] (n=40) 
- RG032r − S032: se aparta (fracción) +0.010 [-0.011, +0.032] (n=40) ; turnos hasta apartarse +0.00 [-0.12, +0.12] (n=40) 
- Resultado: **no se cumple** (más a menudo y antes, en los dos pares).

### P2b (N). Con la bestia a 5 casillas o menos de la comida, las de sumas se acercan a la comida más veces que las de motor
- S32 − RG32r (los cinco mundos juntos): fracción que se acerca +0.002 [-0.009, +0.012] (n=40) ; veces que se acerca -10.6 [-19.0, -2.2] (n=40)
- S032 − RG032r (los cinco mundos juntos): fracción que se acerca +0.005 [-0.003, +0.013] (n=40) ; veces que se acerca -2.5 [-9.2, +4.3] (n=40)
- Resultado (por la fracción): **no se cumple**.

### P2c (N). En sequía dura y bestia de día, las de motor viven al menos tanto como las de sumas; dirección esperada: más
- sequia_dura, RG32r − S32: +0.30 [-0.07, +0.68] (n=40) (igual)
- sequia_dura, RG032r − S032: +0.35 [-0.17, +0.93] (n=40) (igual)
- bestia_dia, RG32r − S32: +0.80 [+0.45, +1.15] (n=40) (más)
- bestia_dia, RG032r − S032: -0.05 [-0.38, +0.25] (n=40) (igual)
- Resultado: **se cumple** (más o igual en los cuatro).

### P2d (R motor, N sumas). Ninguna clase mata entre las suyas
- Muertes por golpe (golpes dados), en todas sus partidas: RG032r 0 (0); RG32r 0 (0); S032 0 (0); S32 0 (0); recolector 0 (0); tonto 0 (0)
- Resultado: **se cumple**.

### P3a (R). En los mundos suaves, con ganancias y sin ellas viven igual
- abundancia, RG32r − RG032r: -0.05 [-0.12, +0.00] (n=40) (igual)
- abundancia, S32 − S032: +0.03 [+0.00, +0.07] (n=40) (igual)
- normal, RG32r − RG032r: +0.20 [+0.05, +0.38] (n=40) (igual)
- normal, S32 − S032: -0.12 [-0.33, +0.05] (n=40) (igual)
- Resultado: **se cumple**.

### P3b (N en parte). Con ganancias visitan más sitios distintos al día y pasan más tiempo con la hermana a la vista
- RG32r − RG032r, sitios distintos al día (media de los cinco mundos): -15.652 [-16.734, -14.618] (n=40) ; por mundo: normal -17.722 [-19.606, -15.859] (n=40); abundancia -19.784 [-21.990, -17.633] (n=40); sequia -15.745 [-18.004, -13.403] (n=40); sequia_dura -16.204 [-18.913, -13.472] (n=40); bestia_dia -8.806 [-10.869, -6.745] (n=40)
- RG32r − RG032r, con la hermana a la vista (media de los cinco mundos): +0.119 [+0.110, +0.127] (n=40) (más); por mundo: normal +0.126 [+0.111, +0.143] (n=40); abundancia +0.116 [+0.101, +0.129] (n=40); sequia +0.109 [+0.094, +0.126] (n=40); sequia_dura +0.122 [+0.098, +0.145] (n=40); bestia_dia +0.122 [+0.108, +0.136] (n=40)
- S32 − S032, sitios distintos al día (media de los cinco mundos): -27.457 [-28.608, -26.324] (n=40) ; por mundo: normal -31.374 [-33.894, -28.783] (n=40); abundancia -26.289 [-28.450, -24.213] (n=40); sequia -29.292 [-31.440, -27.164] (n=40); sequia_dura -25.800 [-29.155, -22.509] (n=40); bestia_dia -24.532 [-26.780, -22.429] (n=40)
- S32 − S032, con la hermana a la vista (media de los cinco mundos): +0.151 [+0.144, +0.158] (n=40) (más); por mundo: normal +0.153 [+0.138, +0.169] (n=40); abundancia +0.108 [+0.094, +0.121] (n=40); sequia +0.150 [+0.137, +0.164] (n=40); sequia_dura +0.169 [+0.152, +0.187] (n=40); bestia_dia +0.173 [+0.155, +0.191] (n=40)
- Resultado: **no se cumple** (las dos cosas, en los dos pares).

### P3c. En los mundos duros, la supervivencia con ganancias y sin ellas (sin predicción de dirección)
- sequia, RG32r − RG032r: -0.28 [-0.57, +0.03] (n=40)
- sequia, S32 − S032: -0.88 [-1.23, -0.50] (n=40)
- sequia_dura, RG32r − RG032r: -0.75 [-1.15, -0.35] (n=40)
- sequia_dura, S32 − S032: -0.70 [-1.25, -0.15] (n=40)
- bestia_dia, RG32r − RG032r: +0.12 [-0.20, +0.45] (n=40)
- bestia_dia, S32 − S032: -0.72 [-1.02, -0.42] (n=40)

### P4. Si el efecto de las ganancias es distinto con motor que con sumas (sin predicción)
- normal, (RG32r − RG032r) − (S32 − S032), vivas: +0.33 [+0.07, +0.57] (n=40)
- abundancia, (RG32r − RG032r) − (S32 − S032), vivas: -0.07 [-0.17, +0.00] (n=40)
- sequia, (RG32r − RG032r) − (S32 − S032), vivas: +0.60 [+0.10, +1.07] (n=40)
- sequia_dura, (RG32r − RG032r) − (S32 − S032), vivas: -0.05 [-0.70, +0.60] (n=40)
- bestia_dia, (RG32r − RG032r) − (S32 − S032), vivas: +0.85 [+0.38, +1.30] (n=40)

### P5 (en RG32r y RG032r; réplicas salvo en los mundos duros)

**RG32r**
- normal: 5a dormida de noche 0.785 [0.772, 0.797] (n=40) **se cumple** · 5b avisa al verla 0.396 [0.372, 0.421] (n=40) **no se cumple** · 5d se vacía y nadie lo rellena 1.00 [1.00, 1.00] (n=40) **se cumple** · 5f «aquí estoy» con alguna al alcance − sin ninguna (por 1.000 turnos) -30.1 [-43.5, -17.6] (n=40) **no se cumple**
- abundancia: 5a dormida de noche 0.774 [0.760, 0.788] (n=40) **se cumple** · 5b avisa al verla 0.413 [0.378, 0.447] (n=40) **no se cumple** · 5d se vacía y nadie lo rellena 0.95 [0.88, 1.00] (n=40) **se cumple** · 5f «aquí estoy» con alguna al alcance − sin ninguna (por 1.000 turnos) -49.8 [-78.3, -26.6] (n=40) **no se cumple**
- sequia: 5a dormida de noche 0.784 [0.772, 0.795] (n=40) **se cumple** · 5b avisa al verla 0.434 [0.408, 0.460] (n=40) **no se cumple** · 5d se vacía y nadie lo rellena 0.97 [0.93, 1.00] (n=40) **se cumple** · 5f «aquí estoy» con alguna al alcance − sin ninguna (por 1.000 turnos) -32.8 [-54.7, -14.8] (n=40) **no se cumple**
- sequia_dura: 5a dormida de noche 0.822 [0.808, 0.836] (n=40) **se cumple** · 5b avisa al verla 0.382 [0.350, 0.413] (n=40) **no se cumple** · 5d se vacía y nadie lo rellena 0.95 [0.88, 1.00] (n=40) **se cumple** · 5f «aquí estoy» con alguna al alcance − sin ninguna (por 1.000 turnos) -8.1 [-21.5, +4.3] (n=40) **no se cumple**
- bestia_dia: 5a dormida de noche 0.804 [0.793, 0.814] (n=40) **se cumple** · 5b avisa al verla 0.744 [0.727, 0.759] (n=40) **se cumple** · 5d se vacía y nadie lo rellena 0.97 [0.93, 1.00] (n=40) **se cumple** · 5f «aquí estoy» con alguna al alcance − sin ninguna (por 1.000 turnos) -16.3 [-31.6, -3.2] (n=40) **no se cumple**
- 5c (todos los mundos): amor (cambio) +0.013 [-0.009, +0.035] (n=40); tristeza (cambio) +0.053 [+0.030, +0.076] (n=40); hermana − vecina: amor -0.229 [-0.284, -0.161] (n=38), tristeza +0.189 [+0.137, +0.240] (n=38). **no se cumple**
- 5e comida a flacas por criatura viva y día, sequía − abundancia: +0.1055 [+0.0943, +0.1169] (n=40) **se cumple**

**RG032r**
- normal: 5a dormida de noche 0.851 [0.837, 0.865] (n=40) **se cumple** · 5b avisa al verla 0.408 [0.380, 0.435] (n=40) **no se cumple** · 5d se vacía y nadie lo rellena 0.88 [0.78, 0.97] (n=40) **se cumple** · 5f «aquí estoy» con alguna al alcance − sin ninguna (por 1.000 turnos) -15.8 [-25.9, -6.5] (n=40) **no se cumple**
- abundancia: 5a dormida de noche 0.821 [0.808, 0.835] (n=40) **se cumple** · 5b avisa al verla 0.435 [0.404, 0.466] (n=40) **no se cumple** · 5d se vacía y nadie lo rellena 0.72 [0.57, 0.85] (n=40) **se cumple** · 5f «aquí estoy» con alguna al alcance − sin ninguna (por 1.000 turnos) -13.9 [-20.9, -7.4] (n=40) **no se cumple**
- sequia: 5a dormida de noche 0.822 [0.811, 0.833] (n=40) **se cumple** · 5b avisa al verla 0.411 [0.390, 0.431] (n=40) **no se cumple** · 5d se vacía y nadie lo rellena 0.90 [0.80, 0.97] (n=40) **se cumple** · 5f «aquí estoy» con alguna al alcance − sin ninguna (por 1.000 turnos) -3.8 [-9.5, +1.9] (n=40) **no se cumple**
- sequia_dura: 5a dormida de noche 0.848 [0.835, 0.859] (n=40) **se cumple** · 5b avisa al verla 0.378 [0.347, 0.408] (n=40) **no se cumple** · 5d se vacía y nadie lo rellena 0.85 [0.72, 0.95] (n=40) **se cumple** · 5f «aquí estoy» con alguna al alcance − sin ninguna (por 1.000 turnos) +9.4 [+5.0, +13.9] (n=40) **se cumple**
- bestia_dia: 5a dormida de noche 0.832 [0.818, 0.845] (n=40) **se cumple** · 5b avisa al verla 0.755 [0.737, 0.770] (n=40) **se cumple** · 5d se vacía y nadie lo rellena 0.93 [0.82, 1.00] (n=40) **se cumple** · 5f «aquí estoy» con alguna al alcance − sin ninguna (por 1.000 turnos) -2.3 [-9.3, +3.9] (n=40) **no se cumple**
- 5c (todos los mundos): amor (cambio) +0.000 [+0.000, +0.000] (n=40); tristeza (cambio) +0.097 [+0.074, +0.121] (n=40); hermana − vecina: amor +0.000 [+0.000, +0.000] (n=40), tristeza +0.212 [+0.165, +0.256] (n=40). **no se cumple**
- 5e comida a flacas por criatura viva y día, sequía − abundancia: +0.0263 [+0.0133, +0.0397] (n=40) **se cumple**

### La felicidad funcional (se informa; no cuenta como prueba: el motor es el instrumento y favorece a las de motor por construcción)
- normal: RG32r las tres bien 0.0008 [0.0006, 0.0009] (n=40), distancia 2.75 [2.71, 2.78] (n=40); RG032r las tres bien 0.0000 [0.0000, 0.0000] (n=40), distancia 3.65 [3.62, 3.68] (n=40); S32 las tres bien 0.0008 [0.0006, 0.0009] (n=40), distancia 2.95 [2.91, 2.99] (n=40); S032 las tres bien 0.0000 [0.0000, 0.0000] (n=40), distancia 3.61 [3.59, 3.64] (n=40)
- abundancia: RG32r las tres bien 0.0016 [0.0014, 0.0018] (n=40), distancia 2.37 [2.34, 2.39] (n=40); RG032r las tres bien 0.0000 [0.0000, 0.0000] (n=40), distancia 3.44 [3.41, 3.46] (n=40); S32 las tres bien 0.0017 [0.0015, 0.0019] (n=40), distancia 2.51 [2.48, 2.53] (n=40); S032 las tres bien 0.0000 [0.0000, 0.0000] (n=40), distancia 3.38 [3.35, 3.41] (n=40)
- sequia: RG32r las tres bien 0.0008 [0.0007, 0.0010] (n=40), distancia 2.95 [2.91, 2.98] (n=40); RG032r las tres bien 0.0000 [0.0000, 0.0000] (n=40), distancia 3.70 [3.67, 3.73] (n=40); S32 las tres bien 0.0009 [0.0007, 0.0011] (n=40), distancia 3.07 [3.03, 3.11] (n=40); S032 las tres bien 0.0000 [0.0000, 0.0000] (n=40), distancia 3.69 [3.66, 3.71] (n=40)
- sequia_dura: RG32r las tres bien 0.0006 [0.0005, 0.0008] (n=40), distancia 3.39 [3.33, 3.44] (n=40); RG032r las tres bien 0.0000 [0.0000, 0.0000] (n=40), distancia 4.17 [4.13, 4.21] (n=40); S32 las tres bien 0.0007 [0.0005, 0.0009] (n=40), distancia 3.51 [3.47, 3.56] (n=40); S032 las tres bien 0.0000 [0.0000, 0.0000] (n=40), distancia 4.15 [4.11, 4.20] (n=40)
- bestia_dia: RG32r las tres bien 0.0002 [0.0002, 0.0003] (n=40), distancia 3.19 [3.14, 3.24] (n=40); RG032r las tres bien 0.0000 [0.0000, 0.0000] (n=40), distancia 3.87 [3.84, 3.90] (n=40); S32 las tres bien 0.0003 [0.0002, 0.0004] (n=40), distancia 3.29 [3.24, 3.35] (n=40); S032 las tres bien 0.0000 [0.0000, 0.0000] (n=40), distancia 3.86 [3.82, 3.90] (n=40)


## Exploración (no predicho; encontrado después)

Solo números. Cada tabla es un mundo; media de las 40 partidas de cada clase. Las definiciones de cada fila están en `medidas_valle.py` y en `informe_medidas_v1.md`.

- **la felicidad:** se mide con el motor como instrumento, y en las de sin ganancias las sumas positivas son 0;
- **el duelo:** el cambio de amor y de tristeza es la media de los casos;
- **«aquí estoy»:** por cuántas otras tiene a la vista de día, no al alcance de la voz.

#### normal

| | RG032r · normal | RG32r · normal | S032 · normal | S32 · normal | recolector · normal | tonto · normal |
|---|---|---|---|---|---|---|
| partidas | 40 | 40 | 40 | 40 | 40 | 40 |
| vivas (día 10 · 20 · 30 · 40) | 8.0 · 7.9 · 7.9 · 7.8 | 8.0 · 8.0 · 8.0 · 8.0 | 8.0 · 7.9 · 7.8 · 7.8 | 8.0 · 8.0 · 7.8 · 7.7 | 8.0 · 8.0 · 8.0 · 7.9 | 8.0 · 8.0 · 8.0 · 8.0 |
| felicidad: las tres bien (media · peor) | 0.0 % · 0.0 % | 0.1 % · 0.0 % | 0.0 % · 0.0 % | 0.1 % · 0.0 % | — (sin estado) | — (sin estado) |
| distancia del motor (media · peor · mejor−peor) | 3.65 · 4.00 · 0.66 | 2.75 · 3.17 · 0.79 | 3.61 · 3.90 · 0.56 | 2.95 · 3.35 · 0.72 | — | — |
| posición media (cuerpo · recursos · vínculo; metas 1 · 2 · 0,8) | -0.66 · -0.63 · -0.36 | 0.01 · 0.49 · 0.24 | -0.63 · -0.63 · -0.34 | 0.05 · 0.24 · 0.30 | — | — |
| de noche dormida · en su casa | 85 % · 63 % | 78 % · 58 % | 82 % · 63 % | 76 % · 51 % | 100 % · 100 % | 100 % · 100 % |
| las dos hermanas en casa a medianoche · la otra la sigue | 27 % · 9 % | 25 % · 20 % | 29 % · 12 % | 19 % · 18 % | 99 % · 99 % | 100 % · 100 % |
| en casa 80 turnos antes del anochecer → al anochecer | 2 % → 31 % | 4 % → 11 % | 4 % → 27 % | 5 % → 7 % | 0 % → 8 % | 45 % → 57 % |
| comida dada por día (en la escasez · fuera) | — · 1.14 | — · 0.69 | — · 0.88 | — · 1.39 | — · 0.00 | — · 0.00 |
| a la herida que pide: la oye alguna con medicina · le dan | 32 % · 4.8 % | 41 % · 1.9 % | 36 % · 2.4 % | 12 % · 0.5 % | 0 % · 0.0 % | 0 % · 0.0 % |
| deja comida por 1.000 turnos (con sobra · sin) · coge del almacén con sobra | 1.7 · 1.9 · 0.8 | 2.0 · 2.2 · 0.9 | 2.4 · 2.4 · 0.8 | 1.6 · 2.2 · 0.7 | 0.0 · 2.2 · 0.0 | 0.0 · 3.9 · 0.0 |
| duelo: casos · amor (cambio) · tristeza (cambio) · acude al cuerpo | 69 · 0.00 · 0.05 · 10 % | 14 · 0.10 · -0.01 · 7 % | 42 · 0.00 · 0.06 · 17 % | 74 · 0.01 · -0.00 · 9 % | 15 · — · — · 13 % | 0 · — · — · — |
| consuelo: llega al lado de la que sufre | 26 % | 31 % | 27 % | 36 % | 20 % | 22 % |
| alarma oída: se aparta · va a casa | 56 % · 53 % | 46 % · 51 % | 50 % · 53 % | 44 % · 50 % | — | — |
| «aquí estoy» por 1.000 turnos (0 · 1 · 2 · 3+ a la vista) | 74.4 · 37.9 · 35.7 · 26.7 | 95.1 · 25.9 · 35.3 · 26.8 | 66.8 · 25.6 · 28.2 · 21.5 | 80.6 · 11.4 · 23.7 · 14.5 | — | — |
| empujones (entre casas) · sueltan comida | 108 (48) · 83 | 357 (218) · 287 | 155 (56) · 114 | 621 (281) · 358 | 0 (0) · 0 | 0 (0) · 0 |
| la que suele perder empieza menos en la 2.ª mitad | 83 de 238 parejas | 99 de 240 parejas | 78 de 235 parejas | 121 de 240 parejas | — | — |
| golpes · muertes por golpe | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 |
| aprendido mirando (vistos/falsos, por partida) | bestia 0/0, comida 121/0, medicina 2/0, sitio:salvaje 0/0 | bestia 0/0, comida 180/1, medicina 2/0, sitio:salvaje 0/0 | bestia 1/0, comida 98/0, medicina 1/0, sitio:salvaje 0/0 | bestia 1/0, comida 198/1, medicina 1/0, sitio:salvaje 0/0 | — | — |
| almacén (comida al acabar el día 1 · 10 · 20 · 40) | 42 · 20 · 6 · 0 | 33 · 2 · 0 · 0 | 44 · 19 · 3 · 0 | 19 · 0 · 0 · 0 | 62 · 130 · 115 · 41 | 32 · 19 · 18 · 18 |

#### abundancia

| | RG032r · abundancia | RG32r · abundancia | S032 · abundancia | S32 · abundancia | recolector · abundancia | tonto · abundancia |
|---|---|---|---|---|---|---|
| partidas | 40 | 40 | 40 | 40 | 40 | 40 |
| vivas (día 10 · 20 · 30 · 40) | 8.0 · 8.0 · 8.0 · 8.0 | 8.0 · 8.0 · 8.0 · 8.0 | 8.0 · 8.0 · 8.0 · 8.0 | 8.0 · 8.0 · 8.0 · 8.0 | 8.0 · 8.0 · 8.0 · 8.0 | 8.0 · 8.0 · 8.0 · 8.0 |
| felicidad: las tres bien (media · peor) | 0.0 % · 0.0 % | 0.2 % · 0.0 % | 0.0 % · 0.0 % | 0.2 % · 0.0 % | — (sin estado) | — (sin estado) |
| distancia del motor (media · peor · mejor−peor) | 3.44 · 3.73 · 0.57 | 2.37 · 2.70 · 0.63 | 3.38 · 3.64 · 0.47 | 2.51 · 2.84 · 0.62 | — | — |
| posición media (cuerpo · recursos · vínculo; metas 1 · 2 · 0,8) | -0.58 · -0.51 · -0.31 | 0.15 · 0.80 · 0.32 | -0.54 · -0.50 · -0.29 | 0.16 · 0.62 · 0.35 | — | — |
| de noche dormida · en su casa | 82 % · 66 % | 77 % · 61 % | 79 % · 66 % | 73 % · 54 % | 100 % · 100 % | 100 % · 100 % |
| las dos hermanas en casa a medianoche · la otra la sigue | 34 % · 12 % | 28 % · 22 % | 36 % · 16 % | 21 % · 19 % | 99 % · 99 % | 100 % · 100 % |
| en casa 80 turnos antes del anochecer → al anochecer | 2 % → 35 % | 4 % → 13 % | 4 % → 30 % | 5 % → 9 % | 0 % → 6 % | 70 % → 79 % |
| comida dada por día (en la escasez · fuera) | — · 0.92 | — · 0.22 | — · 0.67 | — · 0.53 | — · 0.00 | — · 0.00 |
| a la herida que pide: la oye alguna con medicina · le dan | 23 % · 4.4 % | 23 % · 4.7 % | 24 % · 3.3 % | 10 % · 2.5 % | 0 % · 0.0 % | 0 % · 0.0 % |
| deja comida por 1.000 turnos (con sobra · sin) · coge del almacén con sobra | 1.9 · 2.2 · 0.7 | 2.2 · 2.9 · 0.5 | 2.0 · 3.0 · 0.6 | 1.7 · 3.0 · 0.4 | 0.0 · 3.9 · 0.0 | 0.0 · 4.3 · 0.0 |
| duelo: casos · amor (cambio) · tristeza (cambio) · acude al cuerpo | 0 · — · — · — | 14 · -0.05 · -0.02 · 7 % | 7 · 0.00 · 0.01 · 0 % | 0 · — · — · — | 0 · — · — · — | 0 · — · — · — |
| consuelo: llega al lado de la que sufre | 30 % | 36 % | 33 % | 37 % | 20 % | 21 % |
| alarma oída: se aparta · va a casa | 53 % · 60 % | 41 % · 56 % | 49 % · 60 % | 40 % · 57 % | — | — |
| «aquí estoy» por 1.000 turnos (0 · 1 · 2 · 3+ a la vista) | 66.6 · 28.9 · 27.9 · 22.1 | 120.9 · 27.2 · 37.7 · 28.6 | 86.1 · 26.3 · 30.3 · 23.5 | 76.3 · 10.4 · 21.5 · 13.3 | — | — |
| empujones (entre casas) · sueltan comida | 115 (41) · 94 | 405 (203) · 337 | 165 (43) · 133 | 590 (275) · 428 | 0 (0) · 0 | 0 (0) · 0 |
| la que suele perder empieza menos en la 2.ª mitad | 73 de 238 parejas | 103 de 240 parejas | 78 de 234 parejas | 102 de 239 parejas | — | — |
| golpes · muertes por golpe | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 |
| aprendido mirando (vistos/falsos, por partida) | bestia 0/0, comida 94/0, medicina 1/0 | bestia 1/0, comida 79/1, medicina 2/0, sitio:salvaje 0/0 | bestia 0/0, comida 70/0, medicina 1/0, sitio:salvaje 0/0 | bestia 1/0, comida 81/0, medicina 0/0, sitio:salvaje 0/0 | — | — |
| almacén (comida al acabar el día 1 · 10 · 20 · 40) | 43 · 28 · 15 · 2 | 36 · 2 · 0 · 0 | 45 · 30 · 14 · 0 | 20 · 0 · 0 · 0 | 70 · 229 · 287 · 345 | 32 · 22 · 21 · 22 |

#### sequia

| | RG032r · sequia | RG32r · sequia | S032 · sequia | S32 · sequia | recolector · sequia | tonto · sequia |
|---|---|---|---|---|---|---|
| partidas | 40 | 40 | 40 | 40 | 40 | 40 |
| vivas (día 10 · 20 · 30 · 40) | 8.0 · 7.9 · 7.9 · 7.7 | 8.0 · 7.7 · 7.6 · 7.4 | 8.0 · 7.8 · 7.8 · 7.7 | 8.0 · 6.9 · 6.9 · 6.8 | 8.0 · 8.0 · 8.0 · 8.0 | 8.0 · 5.2 · 5.2 · 5.0 |
| felicidad: las tres bien (media · peor) | 0.0 % · 0.0 % | 0.1 % · 0.0 % | 0.0 % · 0.0 % | 0.1 % · 0.0 % | — (sin estado) | — (sin estado) |
| distancia del motor (media · peor · mejor−peor) | 3.70 · 4.06 · 0.65 | 2.95 · 3.41 · 0.83 | 3.69 · 3.99 · 0.58 | 3.07 · 3.59 · 0.94 | — | — |
| posición media (cuerpo · recursos · vínculo; metas 1 · 2 · 0,8) | -0.68 · -0.65 · -0.37 | -0.05 · 0.37 · 0.19 | -0.66 · -0.66 · -0.36 | 0.00 · 0.21 · 0.22 | — | — |
| de noche dormida · en su casa | 82 % · 64 % | 78 % · 59 % | 81 % · 63 % | 77 % · 53 % | 100 % · 100 % | 100 % · 100 % |
| las dos hermanas en casa a medianoche · la otra la sigue | 30 % · 11 % | 24 % · 20 % | 29 % · 13 % | 19 % · 18 % | 99 % · 99 % | 100 % · 100 % |
| en casa 80 turnos antes del anochecer → al anochecer | 3 % → 31 % | 3 % → 12 % | 4 % → 26 % | 4 % → 8 % | 0 % → 7 % | 47 % → 50 % |
| comida dada por día (en la escasez · fuera) | 1.62 · 0.95 | 1.92 · 0.74 | 1.47 · 0.87 | 2.25 · 0.90 | 0.00 · 0.00 | 0.00 · 0.00 |
| a la herida que pide: la oye alguna con medicina · le dan | 40 % · 3.8 % | 40 % · 4.5 % | 36 % · 2.7 % | 12 % · 0.2 % | 0 % · 0.0 % | 0 % · 0.0 % |
| deja comida por 1.000 turnos (con sobra · sin) · coge del almacén con sobra | 1.7 · 1.7 · 0.9 | 2.4 · 2.1 · 0.9 | 1.6 · 2.1 · 0.9 | 1.4 · 1.9 · 0.7 | 0.0 · 2.5 · 0.0 | 0.0 · 3.6 · 0.0 |
| duelo: casos · amor (cambio) · tristeza (cambio) · acude al cuerpo | 95 · 0.00 · 0.02 · 19 % | 166 · -0.00 · 0.01 · 17 % | 88 · 0.00 · 0.02 · 17 % | 297 · -0.02 · 0.03 · 17 % | 0 · — · — · — | 626 · — · — · 25 % |
| consuelo: llega al lado de la que sufre | 27 % | 32 % | 28 % | 36 % | 20 % | 17 % |
| alarma oída: se aparta · va a casa | 56 % · 52 % | 48 % · 49 % | 52 % · 50 % | 44 % · 48 % | — | — |
| «aquí estoy» por 1.000 turnos (0 · 1 · 2 · 3+ a la vista) | 50.1 · 26.3 · 27.0 · 20.5 | 104.8 · 32.0 · 42.3 · 29.4 | 77.6 · 34.2 · 34.6 · 28.0 | 53.4 · 11.7 · 22.1 · 14.5 | — | — |
| empujones (entre casas) · sueltan comida | 106 (46) · 79 | 355 (196) · 269 | 142 (50) · 100 | 487 (224) · 300 | 0 (0) · 0 | 0 (0) · 0 |
| la que suele perder empieza menos en la 2.ª mitad | 74 de 237 parejas | 108 de 240 parejas | 81 de 238 parejas | 138 de 239 parejas | — | — |
| golpes · muertes por golpe | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 |
| aprendido mirando (vistos/falsos, por partida) | bestia 0/0, comida 119/0, medicina 1/0, sitio:salvaje 0/0 | bestia 1/0, comida 248/1, medicina 3/0, sitio:salvaje 0/0 | bestia 1/0, comida 115/0, medicina 1/0, sitio:salvaje 0/0 | bestia 1/0, comida 193/1, medicina 1/0, sitio:salvaje 0/0 | — | — |
| almacén (comida al acabar el día 1 · 10 · 20 · 40) | 43 · 27 · 5 · 0 | 36 · 3 · 0 · 0 | 45 · 28 · 4 · 0 | 20 · 0 · 0 · 0 | 70 · 195 · 135 · 58 | 32 · 18 · 16 · 16 |

#### sequia_dura

| | RG032r · sequia_dura | RG32r · sequia_dura | S032 · sequia_dura | S32 · sequia_dura | recolector · sequia_dura | tonto · sequia_dura |
|---|---|---|---|---|---|---|
| partidas | 40 | 40 | 40 | 40 | 40 | 40 |
| vivas (día 10 · 20 · 30 · 40) | 7.9 · 4.8 · 4.7 · 4.5 | 8.0 · 3.8 · 3.7 · 3.7 | 8.0 · 4.4 · 4.3 · 4.1 | 7.4 · 3.4 · 3.4 · 3.4 | 8.0 · 4.2 · 3.7 · 3.3 | 7.9 · 1.9 · 1.9 · 1.9 |
| felicidad: las tres bien (media · peor) | 0.0 % · 0.0 % | 0.1 % · 0.0 % | 0.0 % · 0.0 % | 0.1 % · 0.0 % | — (sin estado) | — (sin estado) |
| distancia del motor (media · peor · mejor−peor) | 4.17 · 4.60 · 0.87 | 3.39 · 3.94 · 1.08 | 4.15 · 4.60 · 0.87 | 3.51 · 4.08 · 1.07 | — | — |
| posición media (cuerpo · recursos · vínculo; metas 1 · 2 · 0,8) | -0.87 · -0.83 · -0.53 | -0.21 · 0.15 · 0.02 | -0.85 · -0.84 · -0.51 | -0.16 · -0.00 · 0.04 | — | — |
| de noche dormida · en su casa | 85 % · 66 % | 82 % · 59 % | 85 % · 67 % | 82 % · 57 % | 100 % · 100 % | 100 % · 100 % |
| las dos hermanas en casa a medianoche · la otra la sigue | 26 % · 12 % | 25 % · 22 % | 28 % · 16 % | 19 % · 20 % | 99 % · 98 % | 100 % · 100 % |
| en casa 80 turnos antes del anochecer → al anochecer | 2 % → 21 % | 3 % → 9 % | 2 % → 20 % | 3 % → 9 % | 0 % → 8 % | 32 % → 35 % |
| comida dada por día (en la escasez · fuera) | 0.85 · 0.00 | 0.77 · 0.00 | 0.77 · 0.00 | 0.76 · 0.00 | 0.00 · 0.00 | 0.00 · 0.00 |
| a la herida que pide: la oye alguna con medicina · le dan | 34 % · 2.1 % | 32 % · 1.2 % | 25 % · 1.0 % | 7 % · 0.6 % | 0 % · 0.0 % | 0 % · 0.0 % |
| deja comida por 1.000 turnos (con sobra · sin) · coge del almacén con sobra | 1.4 · 1.3 · 2.0 | 2.1 · 1.6 · 1.9 | 1.8 · 1.4 · 2.2 | 1.6 · 1.1 · 1.3 | 0.0 · 2.4 · 0.0 | 0.0 · 2.8 · 0.0 |
| duelo: casos · amor (cambio) · tristeza (cambio) · acude al cuerpo | 702 · 0.00 · 0.11 · 29 % | 743 · 0.01 · 0.07 · 28 % | 702 · 0.00 · 0.08 · 26 % | 784 · -0.03 · 0.09 · 25 % | 764 · — · — · 38 % | 781 · — · — · 23 % |
| consuelo: llega al lado de la que sufre | 28 % | 34 % | 31 % | 39 % | 20 % | 15 % |
| alarma oída: se aparta · va a casa | 56 % · 46 % | 50 % · 43 % | 56 % · 43 % | 50 % · 42 % | — | — |
| «aquí estoy» por 1.000 turnos (0 · 1 · 2 · 3+ a la vista) | 52.0 · 35.1 · 33.2 · 29.5 | 88.5 · 32.5 · 46.3 · 32.6 | 67.2 · 38.8 · 41.5 · 31.9 | 43.3 · 16.4 · 22.6 · 15.8 | — | — |
| empujones (entre casas) · sueltan comida | 91 (35) · 52 | 182 (91) · 124 | 104 (37) · 56 | 228 (105) · 130 | 0 (0) · 0 | 0 (0) · 0 |
| la que suele perder empieza menos en la 2.ª mitad | 108 de 222 parejas | 184 de 236 parejas | 105 de 223 parejas | 185 de 233 parejas | — | — |
| golpes · muertes por golpe | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 |
| aprendido mirando (vistos/falsos, por partida) | bestia 0/0, comida 105/0, medicina 1/0, sitio:salvaje 1/0 | bestia 1/0, comida 161/1, medicina 1/0, sitio:salvaje 0/0 | bestia 1/0, comida 99/0, medicina 1/0, sitio:salvaje 0/0 | bestia 1/0, comida 127/0, medicina 0/0, sitio:salvaje 1/0 | — | — |
| almacén (comida al acabar el día 1 · 10 · 20 · 40) | 44 · 13 · 1 · 0 | 35 · 0 · 0 · 0 | 44 · 10 · 1 · 0 | 18 · 0 · 0 · 0 | 59 · 77 · 5 · 66 | 32 · 0 · 10 · 14 |

#### bestia_dia

| | RG032r · bestia_dia | RG32r · bestia_dia | S032 · bestia_dia | S32 · bestia_dia | recolector · bestia_dia | tonto · bestia_dia |
|---|---|---|---|---|---|---|
| partidas | 40 | 40 | 40 | 40 | 40 | 40 |
| vivas (día 10 · 20 · 30 · 40) | 7.8 · 7.7 · 7.6 · 7.4 | 7.9 · 7.8 · 7.7 · 7.5 | 7.9 · 7.8 · 7.7 · 7.4 | 7.6 · 7.2 · 7.0 · 6.7 | 8.0 · 8.0 · 7.8 · 6.0 | 8.0 · 6.4 · 5.5 · 5.3 |
| felicidad: las tres bien (media · peor) | 0.0 % · 0.0 % | 0.0 % · 0.0 % | 0.0 % · 0.0 % | 0.0 % · 0.0 % | — (sin estado) | — (sin estado) |
| distancia del motor (media · peor · mejor−peor) | 3.87 · 4.28 · 0.74 | 3.19 · 3.69 · 0.89 | 3.86 · 4.25 · 0.69 | 3.29 · 3.97 · 1.15 | — | — |
| posición media (cuerpo · recursos · vínculo; metas 1 · 2 · 0,8) | -0.74 · -0.74 · -0.42 | -0.15 · 0.19 · 0.14 | -0.73 · -0.76 · -0.40 | -0.09 · 0.04 · 0.18 | — | — |
| de noche dormida · en su casa | 83 % · 64 % | 80 % · 57 % | 82 % · 63 % | 79 % · 51 % | 100 % · 100 % | 100 % · 100 % |
| las dos hermanas en casa a medianoche · la otra la sigue | 26 % · 8 % | 23 % · 18 % | 28 % · 10 % | 18 % · 16 % | 99 % · 99 % | 100 % · 99 % |
| en casa 80 turnos antes del anochecer → al anochecer | 5 % → 31 % | 6 % → 13 % | 5 % → 27 % | 7 % → 10 % | 0 % → 7 % | 18 % → 22 % |
| comida dada por día (en la escasez · fuera) | — · 1.17 | — · 1.29 | — · 1.05 | — · 1.46 | — · 0.00 | — · 0.00 |
| a la herida que pide: la oye alguna con medicina · le dan | 28 % · 2.2 % | 25 % · 2.9 % | 21 % · 1.6 % | 5 % · 0.6 % | 0 % · 0.0 % | 0 % · 0.0 % |
| deja comida por 1.000 turnos (con sobra · sin) · coge del almacén con sobra | 3.0 · 2.4 · 1.1 | 2.6 · 2.3 · 1.2 | 2.1 · 2.4 · 1.0 | 1.9 · 1.9 · 0.9 | 0.0 · 2.0 · 0.0 | 0.0 · 3.2 · 0.0 |
| duelo: casos · amor (cambio) · tristeza (cambio) · acude al cuerpo | 173 · 0.00 · 0.08 · 20 % | 143 · 0.00 · 0.02 · 18 % | 164 · 0.00 · 0.05 · 25 % | 346 · -0.03 · 0.04 · 23 % | 470 · — · — · 40 % | 608 · — · — · 34 % |
| consuelo: llega al lado de la que sufre | 28 % | 33 % | 30 % | 38 % | 21 % | 18 % |
| alarma oída: se aparta · va a casa | 39 % · 66 % | 42 % · 59 % | 39 % · 66 % | 41 % · 64 % | — | — |
| «aquí estoy» por 1.000 turnos (0 · 1 · 2 · 3+ a la vista) | 66.2 · 37.9 · 34.9 · 28.3 | 98.9 · 36.3 · 45.5 · 36.0 | 74.0 · 35.2 · 35.0 · 27.5 | 50.0 · 11.7 · 15.8 · 15.3 | — | — |
| empujones (entre casas) · sueltan comida | 96 (47) · 63 | 323 (202) · 234 | 117 (51) · 74 | 433 (203) · 248 | 0 (0) · 0 | 0 (0) · 0 |
| la que suele perder empieza menos en la 2.ª mitad | 100 de 234 parejas | 111 de 240 parejas | 89 de 237 parejas | 138 de 239 parejas | — | — |
| golpes · muertes por golpe | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 | 0 · 0 |
| aprendido mirando (vistos/falsos, por partida) | bestia 16/0, comida 125/0, medicina 3/0, sitio:salvaje 0/0 | bestia 15/0, comida 316/2, medicina 6/0, sitio:salvaje 0/0 | bestia 18/0, comida 117/0, medicina 3/0, sitio:salvaje 0/0 | bestia 18/0, comida 225/1, medicina 3/0, sitio:salvaje 1/1 | — | — |
| almacén (comida al acabar el día 1 · 10 · 20 · 40) | 43 · 17 · 5 · 0 | 31 · 0 · 0 · 0 | 42 · 16 · 3 · 0 | 15 · 0 · 0 · 0 | 61 · 104 · 74 · 17 | 32 · 5 · 6 · 12 |


## Guardado

**Commit local de los resultados, sin push:**
- este informe;
- `salida/evaluacion_experimento_v1.md` y `salida/tabla_experimento_v1.md`;
- `mide_todo.py`;
- unas líneas en `STATUS.md`.

Los registros y los `medidas.json` de cada partida se quedan en el T7.

**Una cosa por el camino:** antes de congelar, borré `salida/ev_err.txt`, un archivo temporal que yo mismo había creado un momento antes para guardar los errores de una prueba. No he borrado nada más.
