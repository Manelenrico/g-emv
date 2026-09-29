# P5-7A — La curiosidad por el terreno, en seco

En seco, **coste cero**, nada a la plataforma. Motor, decisor y tabla intocados.

---

## El titular

**La curiosidad local no alcanza la ignorancia que de verdad persiste; la
llamada de la frontera sí.**

En una vida entera el cuerpo ve **una cuarta parte de la arena** y su ignorancia
global baja **seis puntos de principio a fin**. Pero el renglón de A3 mide la
ignorancia **a radio 6 descontando lo que vería al llegar**, y con vista 9 eso es
casi siempre cero: mide un hueco que ya está tapado. La variante de frontera —la
misma caída de `R-LLAMADA` aplicada a la distancia hasta lo no visto— **dispara
el doble de veces, cambia el doble de decisiones y revela 16 veces más casillas**.

**El veto vital aguanta en las dos variantes y en los dos mundos: cero cambios
con un armado a tiro, en 2.986 decisiones muestreadas.** La balanza funciona: en
entorno inseguro los cambios caen a 0,08 % (local) y 0,48 % (frontera), y sin
balanza suben a 1,21 % y 5,39 %.

**De los seis sellos, K1 falla en S-2 y K4 falla en los dos mundos y las dos
variantes.** El resto depende de la variante, y ahí está el resultado.

---

## Lo que hubo que construir, y una declaración que cambia A1

**El mundo no publica qué casillas ves.** El registro del tic aplana la
observación en `ve_agentes` / `ve_items` / `ve_bushes` / `ve_proyectiles`
(`paintball/alma/policy.py:174-182`); no hay lista de casillas ni de tiles. La
visibilidad es **derivada**: radio `mundo.radio_vision(INT)` — 9 aquí,
`5 + (8+1)//2`, `mundo.py:256-264` — más `mundo.linea_de_vista`, que cortan
muros, rocas y fortaleza.

Así que **la ignorancia no se lee: se reconstruye**, casilla a casilla, con las
reglas del mundo y la posición del diario. Es un dato calculado, no observado, y
toda A1 hay que leerla con eso delante. El denominador son **las 2.304 casillas
del mapa**, muros incluidos: un muro se ve aunque no se pise.

### La puerta de entrada

El renglón se instala **fuera**, con el patrón exacto del piso de P5-3E
(`forma.py:444-461`): se repite el reparto de `A.REPARTO` / `A.APETITIVAS` y se
rehace el `State`. `D.A` se sustituye por un proxy que **delega todo en v42** por
`__getattr__` —el decisor usa `A.` para veinte cosas más que `appraise`— y
reimplanta solo el montaje.

```
PUERTA (renglon apagado, proxy instalado): 5.555/5.555 = 100,00 %
```

Bit a bit la `d` de siempre. Sin eso, nada de lo que sigue valdría.

---

## A1 · La ignorancia, como número

| | **S-2** (40 asientos, 112.865 tics) | **lento** (6 asientos, 37.750 tics) |
|---|---|---|
| global, mediana | **0,7283** | **0,7101** |
| global, min-max | 0,6233 – 0,8963 | 0,6662 – 0,8941 |
| local (r=6), mediana | 0,0088 | 0,0000 |
| local (r=6), media | 0,0247 | 0,0103 |
| tics con local > 0 | **63,85 %** | 42,20 % |
| novedad (100 tics), mediana | 0,0 | 0,0 |
| novedad, máximo | 426 | 418 |
| casillas vistas, mediana | **616,5** de 2.304 | **647,5** de 2.304 |

**Por tramo de vida** (mediana de global · local · novedad):

| tramo | S-2 | lento |
|---|---|---|
| 1 | 0,7730 · 0,0088 · 0,0 | 0,7257 · 0,0000 · 0,0 |
| 2 | 0,7418 · 0,0177 · 0,0 | 0,7188 · 0,0000 · 0,0 |
| 3 | 0,7235 · 0,0088 · 0,0 | 0,7109 · 0,0000 · 0,0 |
| 4 | **0,7101** · 0,0000 · 0,0 | **0,6979** · 0,0000 · 0,0 |

**Tres hechos que mandan sobre todo lo demás:**

1. **El cuerpo ve una cuarta parte de la arena en toda su vida** y se queda ahí.
2. **La ignorancia global baja seis puntos de principio a fin** (0,773 → 0,710 en
   S-2). No explora: se mueve por lo conocido.
3. **La novedad mediana es cero en los cuatro tramos y en los dos mundos.** En el
   tic mediano no se descubre nada nuevo. Los máximos de 426 y 418 son el primer
   barrido al nacer.

**Y la ignorancia local es casi siempre cero.** Ese es el diagnóstico que
explica A4: lo que el cuerpo no sabe **no está a radio 6, está lejos**.

---

## A2 · La amenaza, graduada

### La fórmula, declarada

```
amenaza = 1 − (1 − a_armados)(1 − a_daño)(1 − a_anillo)
```

Tres términos en [0,1] combinados como **«al menos uno»**, y no como suma con
pesos, por dos razones: no puede pasarse de 1 sin recortes artificiales, y dos
peligros distintos se acumulan sin que uno tape al otro. **Da exactamente 0 sin
armados a la vista, sin daño reciente y sin anillo**, que es la condición pedida.

- **`a_armados`**: por cada rival armado a distancia Chebyshev `d` con alcance
  `rg` **leído del catálogo del mundo**, vale 1 si `d ≤ rg` (a tiro) y cae
  linealmente hasta 0 en el radio de visión propio. Se combinan igual, «al menos
  uno».
- **`a_daño`**: daño recibido en los últimos 100 tics / **25**, con techo 1. El
  25 es el único número elegido a mano y va declarado como `[impl]`.
- **`a_anillo`**: 1 si la casilla ya arde; si no, sube al acercarse el momento de
  arder, con **el mismo horizonte que `F-ANTICIPACION`** (`A.ANT_HORIZONTE_S`,
  importado, no copiado).

### El reparto

| grado | **S-2** | **lento** |
|---|---|---|
| seguro (< 0,2) | 36.766 / 112.865 = **32,58 %** | 18.200 / 37.750 = **48,21 %** |
| neutro | 14.103 = 12,50 % | 2.503 = 6,63 % |
| inseguro (> 0,6) | 61.996 = **54,93 %** | 17.047 = **45,16 %** |
| amenaza mediana | **0,6875** | **0,3750** |
| tics con armados > 0 | 59,74 % | 49,41 % |
| tics con daño > 0 | 17,65 % | 5,36 % |
| tics con anillo > 0 | 10,79 % | 5,64 % |

**El lento es medio mundo más seguro que S-2**, que es la dirección que el sello
esperaba. Pero las magnitudes no son las del sello, y hay que decirlo.

### Contra la «calma de amenaza» de P5-1

P5-1 midió **18 %** de calma en el lento; aquí el entorno seguro sale **48,21 %**.
**No son la misma medida y no deberían coincidir:** la calma de P5-1 es binaria y
estricta —ningún armado a la vista **y** todas las filas por debajo de un
umbral—, mientras que esto es una amenaza graduada con corte en 0,2, que admite
un armado lejano o un rastro de daño viejo. Que mi número sea 2,7 veces mayor es
consecuencia del corte, no una contradicción. **Con el corte en 0,05 el «seguro»
del lento bajaría a la banda de P5-1**; no lo muevo porque los umbrales venían
dados en el encargo.

---

## A3 · Los dos renglones

Los dos son **dolor** (no apetitivos), en el dominio **R**, con reparto
**(0,1 / 0,8 / 0,1)** — el de `R-ACOPIO` y `R-LLAMADA`, los R-dominantes ya
existentes. No se inventa un reparto nuevo y ninguno queda a cero, como manda la
tabla.

**`R-CURIOSIDAD-TERRENO` (local, A3)**
`valor = k × ignorancia_local_proyectada × (1 − amenaza)`, donde la proyectada es
lo no visto dentro del radio 6 desde la casilla de llegada **descontando lo que
vería al llegar**.

**`R-CURIOSIDAD-FRONTERA` (el añadido)**
`valor = k × ignorancia_global × (1 − amenaza) × (1 − g(d))`, con `d` la
distancia por el mapa de la casilla de llegada a la casilla no vista pisable más
cercana, y `g` **la misma caída de `R-LLAMADA`**:

```python
# appraisal_zs_v42_exp.py:1085
v = niv * max(0.0, 1.0 - math.dist(pos, p) / BOTIN_DIST_REF) ** BOTIN_EXP
```
con `BOTIN_DIST_REF = 24.0` (`:134`) y `BOTIN_EXP = 3`, descuento cúbico
(`:135`), **importadas, no copiadas**.

### Una ambigüedad del encargo, resuelta y señalada

El encargo escribe **`× g(distancia)`**, pero `g` vale **1 pegado a lo no visto**
y 0 lejos. Como el renglón es **dolor**, multiplicar por `g` haría **doler más
cuanto más cerca de la frontera** y **no doler nada con la frontera lejos** — lo
contrario de la intención que el propio encargo declara («acercarse a la frontera
alivia y alejarse duele») y de cómo funciona el renglón local, donde el dolor es
la ignorancia **no aliviada**.

**Implemento `× (1 − g(d))`.** Queda señalado en el código y aquí; volver a la
lectura literal es quitar el `1.0 -` de una línea.

### El coste de la frontera: un BFS por tic, no por candidato

La distancia a lo no visto se resuelve con **un BFS multi-fuente sobre las 2.304
casillas**, con las no vistas y pisables como fuentes y expansión en las 8
direcciones del decisor. **Uno por tic muestreado sirve a los cuatro k y a todos
los candidatos**, así que no hace falta precalcular por posición.

**Coste medido: mediana 1,850 ms, máximo 21,957 ms.**

---

## A4 y A5 · Las dos variantes, lado a lado

**Muestreo declarado:** el ojo mira en cada tic vivo, pero se **decide** cada 50
tics desde el 300 — las constantes del arnés de P5-2. Decidir en los 150.000 tics
vivos por cada una de las nueve configuraciones serían horas. Las fracciones son
**estimaciones de muestra, no censos**.

### S-2 (40 asientos · 2.230 decisiones muestreadas)

| medida, k = 0,2 con balanza | **LOCAL** | **FRONTERA** |
|---|---|---|
| se enciende (M > 0), % de tics | 41,30 % | **63,27 %** |
| M máximo | 0,07080 | 0,11561 |
| **(a) decisiones que cambian** | **0,90 %** | **1,70 %** |
| en entorno seguro | 2,14 % | **3,42 %** |
| en entorno neutro | 1,40 % | 2,80 % |
| **en entorno inseguro** | **0,08 %** | **0,48 %** |
| (c) voz propia, R-CARENCIA ≥ 0,25 | 0,97 % | **1,65 %** |
| **(d) veto: armado a tiro** | **0** | **0** |
| (d) veto: vida < 30 | 3 | 3 |
| (e) derroche: acerca a un armado | 10,00 % | 10,53 % |
| (e) derroche: mete en el anillo | 45,00 % | 57,89 % |
| **(b) razón proyectado/real** | 3,48x | **16,08x** |

### Mundo lento (6 asientos · 756 decisiones muestreadas)

| medida, k = 0,2 con balanza | **LOCAL** | **FRONTERA** |
|---|---|---|
| se enciende (M > 0), % de tics | 36,77 % | **60,32 %** |
| M máximo | 0,06549 | 0,11275 |
| **(a) decisiones que cambian** | **0,53 %** | **3,84 %** |
| en entorno seguro | 1,09 % | **7,10 %** |
| en entorno neutro | 0,00 % | 6,00 % |
| **en entorno inseguro** | **0,00 %** | **0,00 %** |
| (c) voz propia, R-CARENCIA ≥ 0,25 | 0,53 % | **3,84 %** |
| **(d) veto: armado a tiro** | **0** | **0** |
| (d) veto: vida < 30 | 0 | 1 |
| (e) derroche: acerca a un armado | 0,00 % | 0,00 % |
| (e) derroche: mete en el anillo | 25,00 % | 31,03 % |
| **(b) razón proyectado/real** | 0,24x | **66,68x** |

### A5 · Lo que hace la balanza sola

Sin el factor `(1 − amenaza)`, k = 0,2, cambios en **entorno inseguro**:

| | con balanza | **sin balanza** |
|---|---|---|
| S-2 · local | 0,08 % | **1,21 %** |
| S-2 · frontera | 0,48 % | **5,39 %** |
| lento · local | 0,00 % | 2,35 % |
| lento · frontera | 0,00 % | 5,88 % |

**La balanza es lo que mantiene el veto.** Quitarla multiplica los cambios en
entorno inseguro por 15 en S-2 y por 11 en la frontera. Es el resultado más
limpio del encargo: **el mecanismo de subordinación a la amenaza funciona, y se
puede medir apagándolo.**

### (b), con su confuso declarado

La columna «real» son las casillas nuevas que el diario vio en los 100 tics
siguientes; la columna «proyectado» son las que el candidato nuevo **habría**
revelado al llegar. **No es una comparación entre dos futuros: el diario no
siguió ese camino.** Es lo que el candidato prometía contra lo que de hecho pasó
por otra ruta. La razón de 16x y 66x dice que **los candidatos que la curiosidad
elige apuntan a terreno mucho más virgen que el que el cuerpo pisó**, no que
habría visto 16 veces más.

---

## A6 · Coste por decisión

| | S-2 | lento |
|---|---|---|
| decisión **sin** renglón | mediana **12,676 ms** · máx 39,954 | 11,200 · máx 33,628 |
| decisión **con local** (k=0,2) | 12,558 · máx 39,475 | 11,231 · máx 33,508 |
| decisión **con frontera** (k=0,2) | 12,541 · máx 39,605 | 11,183 · máx 33,144 |
| **sobrecoste del renglón** | **−0,118 / −0,135 ms** | +0,031 / −0,017 ms |
| **BFS de la frontera** (1 por tic) | **1,850 ms** · máx 21,957 | 1,845 · máx 6,188 |

**El renglón es gratis**: el sobrecoste sale negativo, o sea por debajo del ruido
de medida. Lo único que cuesta es el BFS, **1,85 ms una vez por tic**, y ya está
amortizado entre los cuatro k y todos los candidatos.

---

## Cotejo de las predicciones selladas (mesa, 22-sep-2026)

| | sello | contador | veredicto |
|---|---|---|---|
| **K1** | lento > 10 % seguro; S-2 < 5 % | lento **48,21 %** ✔ · S-2 **32,58 %** ✘ | **FALLA en S-2** |
| **K2 local** | seguro > 3 %, inseguro < 0,3 %, sin balanza inseguro > 1 % | S-2: 2,14 / 0,08 / 1,21 · lento: 1,09 / 0,00 / 2,35 | **FALLA (por el «seguro»)** |
| **K2 frontera** | ídem | S-2: 3,42 / 0,48 / 5,39 · lento: **7,10 / 0,00 / 5,88** | **FALLA en S-2 · CUMPLE en el lento** |
| **K3 local** | voz propia > 1 % | S-2 **0,97 %** · lento 0,53 % | **FALLA** (pero > 0,2 %) |
| **K3 frontera** | ídem | S-2 **1,65 %** · lento **3,84 %** | **CUMPLE en los dos** |
| **K4** | derroche > 1 % con k=0,4 y **ninguno** con k=0,1 | k=0,4 sí (5,9-20 %), pero **k=0,1 no da cero**: S-2 local 1, frontera 3 | **FALLA en los dos** |
| **K5 local** | ≥ 2x | S-2 **3,48x** ✔ · lento **0,24x** ✘ | **CUMPLE en S-2, falla en el lento** |
| **K5 frontera** | ídem | S-2 **16,08x** · lento **66,68x** | **CUMPLE en los dos** |
| **K6** | coste por decisión < 3 ms | renglón **≈ 0 ms** ✔ · BFS **1,85 ms** ✔ · decisión entera **12,5 ms** ✘ | **depende de la lectura** |

### Lo que hay que leer de este cotejo

**K1 falla en S-2 por mi fórmula, no por el mundo.** El 32,58 % de «seguro»
viene del corte en 0,2 sobre una amenaza graduada; con un corte más estricto
caería. La **dirección** sellada —el lento más seguro que S-2— **se cumple**:
48,21 % contra 32,58 %.

**K3 es el sello que el encargo marcó como decisivo** («si es menor del 0,2 %, la
opción A se reexamina con datos»). El renglón local da **0,97 % en S-2 y 0,53 %
en el lento**: falla el umbral del 1 % por poco, pero **está muy por encima del
0,2 %**, así que **la opción A —recurso dentro de R— no se reexamina**. La voz
epistémica **no se apaga por la subordinación a R**, que era la condición de
examen de agosto. Y con la frontera cumple holgadamente: 1,65 % y 3,84 %.

**K4 falla por su segunda cláusula, no por la primera.** Con k = 0,4 el derroche
aparece como se esperaba (5,94 % y 20 %), pero **con k = 0,1 no es cero**: quedan
1 caso en S-2 local y 3 en frontera. El derroche no desaparece bajando la
ganancia: **es más barato de lo que el sello suponía**.

**K6 tiene la misma ambigüedad que S8 en P5-6C:** «coste por decisión» puede ser
lo que el renglón añade (≈ 0 ms, cumple), lo que cuesta su maquinaria (1,85 ms,
cumple) o la decisión entera (12,5 ms, falla — pero **ya fallaba sin renglón**,
porque la decisión base cuesta 12,676 ms). **Doy los tres y no elijo.**

---

## A7 · La figura

`cantera/paper5/figG/A7_P5_C2_a10.png` — la vida más larga del mundo lento
(13.440 tics), con la ignorancia global, la amenaza graduada (cruda en tenue y su
mediana móvil de 100 tics, porque entra y sale de golpe cuando un armado aparece
y desaparece de la vista) y los tics en que cada variante habría cambiado la
decisión.

**La figura es el argumento del informe en una imagen.** Entre los tics 2.400 y
8.000 la amenaza es cero y **la ignorancia global no se mueve: se queda clavada
en 0,727 durante seis mil tics**. El cuerpo no explora aunque esté completamente
seguro. En ese tramo **el renglón local no dispara ni una vez** —a radio 6 ya
está todo visto— y **la frontera dispara repetidamente**. Local: 1 cambio en toda
la vida. Frontera: 13.

---

## Un fallo mío, y cómo se encontró

**La primera pasada dio cero cambios en las cuatro configuraciones y en los dos
mundos.** No era el renglón: **no llamé a `C.instala()` en el medidor**, así que
`D.A` seguía siendo v42 y el renglón nunca entró en la decisión.

Lo encontré porque, al ver el cero, añadí contadores dentro del proxy que
distinguen **«el renglón no se enciende nunca»** de **«se enciende y no voltea
nada»** — candidatos valorados, cuántos con M > 0, M máximo. Sin ellos habría
publicado un cero que parecía un resultado. Esos contadores se quedan en el
código y son la primera línea de cada bloque de A4.

---

## Propuesta, no ejecución

Los datos dicen que **la curiosidad definida a radio local mide el hueco
equivocado**. La variante de frontera está construida y medida, y cumple K3 y K5
en los dos mundos. **Lo propongo, no lo decido**: si la mesa quiere una sola
curiosidad, los números favorecen la frontera; si quiere las dos, conviven sin
tocarse porque son dos renglones distintos del mismo dominio.

Queda sin resolver **K4**: el derroche no se apaga con k = 0,1. Si importa que a
ganancia baja no haya ni un caso, hace falta algo más que bajar k — un veto
explícito por proximidad a un armado, que **no está en el encargo y no he
añadido**.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

| fichero | md5 |
|---|---|
| `cantera/paper5/curiosidad.py` | `fc77bea7aeef7db16a08590c20854936` |
| `cantera/paper5/mide_P57A.py` | `8374fb65babeec4e4b880d27558f2e87` |
| `cantera/paper5/analiza_P57A.py` | `ff2e2462fa887f31661021c9e2a43d9b` |
| `cantera/paper5/fig_P57A.py` | `9dc46ed07ba3e21907943bdb70e98fd3` |
| `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` |
| `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` |

Datos: `P57A_s2.json`, `P57A_lento.json`, `P57A_progreso.log`.
Figura: `figG/A7_P5_C2_a10.png`.

**PARO AQUÍ.**
