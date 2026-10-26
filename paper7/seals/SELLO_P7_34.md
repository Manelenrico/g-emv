# SELLO P7-34 · El campo de lo inútil

*9-oct-2026, commit `65e7354`. Escrito ANTES de pedir ninguna partida del campo (el freno, días 1-3 de APRENDE de la serie 1, es parte del campo y cuenta en él; se evalúa sobre esas 6 vidas
antes de pedir ninguna más). Coste previsto: hasta 120 partidas en la plataforma; consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Cuerpo y congelados sin
tocar. Archivos `_P7`; una vida por proceso; la memoria viaja solo en el cuaderno.*

## El diseño

- Las piezas de P7-33 tal como quedaron (`descubre_P7`, `pide_P7`, `nace_P7_23`, `nace_P7_29`, `nace_P7_33`; `policy_pareja_P7_33.py`): nace sin saber nada de cuatro cosas
  (botiquín, ración, red, camuflaje); lo que el cuerpo sabía de red y camuflaje borrado (informe P7-33, sección «Lo construido»); probar el camuflaje es ponérselo 10 s y la red
  llevarla 10 s; «no hizo nada» como recuerdo; curiosidad de clase (tener alivia la mitad, probar el resto); el cuánto; oído y ley (`event_warning`: casillas inundadas o en
  tormenta no transitables mientras dure) en los tres brazos; contexto de cada prueba (calma / rival a 4 casillas o menos / fuego / vida < 30).
- **Paso 0 (arreglo, antes del campo)**: el descuadre «N fotos para N+1 candidatos» venía de que la pieza congelada del seis `arreglos_P6_8b._cands` (aplicada por
  `policy_pareja11.run` DESPUÉS de las del siete) esconde `coger` con la mochila llena por fuera del envoltorio del siete, y las fotos se corrían un índice. Arreglo en
  `nace_P7_29.decidir` (la lista de nombres se toma de la lista FINAL de candidatos en el momento de decidir, patrón de `policy_cortex.decidir`); md5 de `nace_P7_29.py`
  tras el arreglo: `f8b85c6f61257b09ae3c1d961382f7e6` (antes: `9f43cd057c0eb6f6e3119b0989bbf233`). Comprobado: la réplica de la vida d1 a10 del humo de P7-33 da 0
  descuadres y 11.130/11.130 decisiones iguales al diario; F2 de P7-33 (cuaderno vacío y cuaderno cargado a mano) idéntica; F1 repetida: todo apagado = A4 (1.007.274 igual · 2 difiere, las dos conocidas) y TECHO con oído y ley
  (1.007.078 igual · 198 difiere, en 6 vidas): las mismas cifras que en P7-33.
- Tres brazos, interruptores de la misma imagen (`Dockerfile.pareja_P7_34` = la de P7-33 con la carpeta de cuadernos de P7-34): **TECHO** (nace sabiendo, con pedir; oído y
  ley), **APRENDE** (nace sin saber las cuatro cosas, cuaderno que viaja de un día al siguiente), **BORRADO** (nace sin saber, cuaderno vaciado cada noche). Pedir corregido y
  lo dado entregado en los tres; ojos compartidos apagados. 20 días; la misma semilla para los tres brazos cada día; dos series con órdenes distintos, una detrás de otra.
- **Semillas nuevas**, declaradas antes de jugar (`semillas_P7_34.json`): 20260916 + k·104729, k = 201 a 220 (las siguientes al humo de P7-33, 198-200); la serie 2 juega
  las mismas 20 en orden inverso. Serie 1: 41311445, 41416174, …, 43301296.
- **Freno**: los días 1 a 3 de APRENDE, serie 1 (`freno_P7_34.py` -> `P7_34_freno.json`). Se sigue si (a) el cuaderno viaja y se lee (registro de arranque con `leido` los
  días 2 y 3 y los recuerdos de arranque son los del cierre del día anterior); (b) en al menos 4 de las 6 vidas la criatura toca alguna de las cuatro cosas; (c) en al menos
  una criatura sube la creencia de alguna cosa útil (botiquín dentro; ración, la mayor de sus situaciones) entre el cierre de un día y el siguiente; (d) ningún error de fotos
  (`P7_error` «fotos para candidatos» = 0 en las 6 vidas). Si algo falla, se para y se dice.
- **Guardas** como en P7-30: latencia (`guarda_latencia_P7_29`: marca la vida si > 1 % de decisiones por encima del tic o > 5 % de pasos listos bloqueados sin cuerpo; para la
  cadena solo por encima del 10 % sobre el tic o del 5 % bloqueados sin cuerpo); disco (parada limpia bajo 5 GB); red (esperar y reintentar); cortes de la plataforma (como
  en P7-27/P7-30: diario rescatado del registro de salida, partida marcada parcial, fuera de puesto, cadena sigue con el cuaderno del corte).

## Definiciones, fijadas antes de medir

- **Las cuatro cosas**: botiquín (`first_aid`), ración (`rations`), red (`net`), camuflaje (`camouflage`). **Útiles**: botiquín y ración. **Inútiles**: red y camuflaje.
- **Contacto** con una cosa: un tic en que sube el número de unidades de esa clase que la criatura lleva (zurrón + mano + cuerpo, leídos del registro de tic del diario);
  **primer contacto**: el primero de la vida. **Coger**: cada subida de unidades (una por unidad); **uso**: cada apertura del canal de uso (registro `P7_nace_uso`,
  como en E6 de P7-30); **soltar**: las bajadas de unidades que sobran una vez descontados los usos (regalos, hacer sitio, muerte).
- **Prueba** de la red o del camuflaje: una huella `P7_huella` de esa cosa (ventana de 10 s desde que entra en el zurrón / se pone; se cierra al acabar la ventana o antes si
  la cosa se va). **Prueba** del botiquín o de la ración: una huella de uso (como en P7-30: firme, «al menos» o corte). **Contexto** de una prueba: el registro
  `P7_33_prueba` de apertura (`peligro`: `rival_a_4`, `fuego`, `vida_menor_30`, `calma`); para el botiquín y la ración, el `peligro` del registro de apertura de su canal
  (`P7_33_prueba` «abre» que escribe `nace_P7_33` para los consumibles). **En calma**: `calma` verdadero (sin rival a 4 casillas o menos, sin fuego, vida en 30 o más).
- **Recuerdo**: cada entrada del cuaderno al cerrar el día (`P7_cuaderno` «fin»); **firme** (ni «al menos» ni corte), **«al menos»**, **corte**; **«no hizo nada»**: un
  recuerdo de la red o del camuflaje cuyo efecto en el cuerpo está entre −1 y +1 (sin daño conocido descontado, la vida no cambió más de un punto en la ventana).
  **Intensidad** de un recuerdo: su campo `intensidad` (`cuaderno_P7`: 1 + min(1, (|imp_cuerpo| + |imp_recursos| + |imp_vínculo|) / 1,5), importancia = cambio del malestar
  por eje durante la prueba). **Creencia** de una cosa: la del cuaderno sin cortes (`CuadernoP29.creencia`), dentro del círculo (la red y el camuflaje se prueban donde se
  está; se toma la situación «dentro»; si una cosa solo tiene recuerdos «fuera», la de fuera); la del botiquín, siempre dentro. **Ignorancia**: `ignorancia` del cuaderno al
  cerrar el día. **Ganas (k)**: el k de cada cosa en el último registro `P7_33_k` del día (`k_ganas` del botiquín, `k_de` de la ración, `k_gear` de la red y del camuflaje).
- **Las 4 criaturas de APRENDE**: asientos 10 y 11 de cada serie (serie 1 a10, s1 a11, s2 a10, s2 a11); cada una lleva su cuaderno los 20 días.
- **Puesto**: `final.placement` (1 el mejor, 16 el peor). **Diferencia de puesto** APRENDE − BORRADO: media de las diferencias emparejadas por serie, día y asiento; su error
  estándar, desviación típica / raíz de n. Días 1-5: 20 parejas; días 16-20: 20 parejas. **Error estándar de la diferencia de dos medias**: raíz de la suma de los dos errores
  estándar al cuadrado (como E8 de P7-30).
- **Marcada**: una vida que no pasa la guarda de latencia; **partida marcada**: la de esa serie, día y brazo (los dos asientos). **Partida con corte**: la que no trae el
  artefacto entero. El sello se evalúa UNA vez al acabar, con dos cuentas: con todas las vidas (quitando solo las partidas con corte de los puestos) y sin las partidas
  marcadas.

## Las reglas

| | regla | pasa si |
|---|---|---|
| I1 | prueba lo inútil | al acabar el día 5, cada una de las 4 criaturas de APRENDE tiene ≥ 1 prueba de la red y ≥ 1 del camuflaje (huellas de los días 1-5) |
| I2 | deja de quererlo | días 11-20, APRENDE: cogidas de red + camuflaje por vida ≤ ¼ de las cogidas de red + camuflaje por vida de TECHO en esos días, y ≤ ¼ de sus propias cogidas de botiquín + ración por vida |
| I3 | lo recuerda débil | APRENDE, cuadernos del día 20 (los 4): la intensidad media de los recuerdos de red y camuflaje < ½ de la intensidad media de los recuerdos de botiquín y ración (sin cortes) |
| I4 | lo olvidado vuelve a parecer nuevo | en ≥ 2 de las 4 criaturas hay una prueba de red o de camuflaje en un día d con ningún contacto con ESA cosa en los días d−5 … d−1 (5 días o más sin tocarla; la prueba del primer contacto de la vida de la criatura no cuenta) |
| I5 | lo útil sigue | la creencia del botiquín dentro (sin cortes) ≥ 30 el día 20 en ≥ 3 de las 4; y en los días 16-20, APRENDE − BORRADO en puesto no es mayor que en los días 1-5 por más de 2 errores estándar (el de la diferencia de las dos medias) |
| I6 | lo curioso en calma | ≥ 80 % de las pruebas de red y camuflaje de APRENDE (los 20 días) se abren en calma |

Sin predicción, solo medida (por día, brazo y criatura, para cada una de las cuatro cosas): contactos, pruebas y su contexto, recuerdos (firmes, «al menos», cortes, «no
hizo nada»), creencia, ignorancia, ganas, cogidas y sueltas; puesto, muerte (tic y causa), latencia (mediana, p95, máximo, fracción sobre el tic, pasos listos bloqueados sin
cuerpo) y agua (avisos oídos, casillas cerradas por la ley, tics bloqueados contra casillas de la ley). Figuras: creencia, ignorancia y ganas de las cuatro cosas por día
(APRENDE, media de las 4 criaturas); cogidas de lo útil frente a lo inútil por día y brazo. GIF de los datos (matplotlib, del diario): una prueba de red o camuflaje en
calma y un uso del botiquín en peligro de la misma criatura.

## Añadidos posteriores al sello

(ninguno al escribirlo)

1. (10-oct-2026, al medir) **Asiento sin artefacto = partida con corte.** Dos vidas de TECHO (s2 d6 a11, s2 d8 a11) no trajeron artefacto ni líneas en el registro de salida;
   `analiza_P7_34` las deja sin diario y `sello_P7_34` toma las partidas con corte también del estado del lanzador (`P7_34_estado.json`, campo `parcial`), no solo de los diarios
   parciales, para que esas dos partidas salgan de los puestos como dice la definición.
2. (10-oct-2026, al medir) **TECHO no tiene canal de uso** (`P7_nace_uso` es de la pieza de nacer sin saber): en la tabla de las cuatro cosas sus usos se dan como «—» y sus
   bajadas de unidades juntas. No cambia ninguna regla (I2 solo usa cogidas).
3. (10-oct-2026, al acabar) La parada dura del lanzador (> 10 % de decisiones sobre el tic: s2 d7 BORRADO a11, 15,98 %) saltó al cerrar la serie 2, con las 120 partidas jugadas y
   bajadas; nada quedó sin jugar ni se reanudó nada. La regla «sin mirar resultados hasta el final» se cumplió: el primer dato leído fue el del freno, el segundo el sello.
