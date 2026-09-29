# P5-8K — Margen 0,02 para la curiosidad · LA SONDA

**PARO AQUÍ.** Se disparó tu condición de parada por precio, y las cuarenta no
se han lanzado.

---

## El titular

**El cambio hace exactamente lo que el contrafactual prometió, y al hacerlo
destruye todo lo demás.**

| | P5-8I (margen 0,062) | **P5-8K (margen 0,02)** |
|---|---|---|
| **aceptación** | 1,0 % | **42,6 %** (109 de 256) |
| completadas por llegada o alivio | 70 % | **6,4 %** |
| **muertas por veto duro** | 10 % | **93,6 %** |
| lo prometido, **visto durante** | 77,6 % | **2,8 %** |
| lo prometido, **nunca visto** | 17,9 % | **96,3 %** |
| distancia al nacer → al terminar | 5 → 1 | **8 → 7** |

**El contrafactual de P5-8I predijo 45,7 % de aceptación a margen 0,02. Salió
42,6 %.** La predicción era buena. **Lo que no se predijo es qué formas entran.**

**Las que el margen 0,062 dejaba fuera nacen mucho más lejos** —distancia mediana
**8** casillas contra 5— y **un camino largo es un camino que un armado acaba
cubriendo**: 102 de 109 mueren por **veto duro** antes de llegar. El cuerpo las
obedece —**203 de 203 tics con piernas listas, el 100 %**— pero las obedece
camino de un sitio al que no llega.

**Y el compromiso pasó a ser casi siempre contra el cuerpo: 196 de 203
obediencias (96,6 %) fueron contra el criterio del decisor**, cuando en P5-8I
fueron 46 %. Tiene sentido: las formas que ahora pasan son las que el cuerpo
menos quiere.

**De los siete sellos, con esta sonda cumplirían tres y fallarían cuatro.**

---

## La parada, y por qué

**Las dos partidas costaron 0,179818 $ y 0,179138 $, por encima de tu umbral de
0,15.** Paré: no se lanzó la tanda 1.

**La causa es la cola, y se puede comprobar:**

| | cola | juego | vida del pod | precio | **$/minuto** |
|---|---|---|---|---|---|
| P5-8I A/20260916 | 0,5 min | 10,5 | 11,0 min | 0,109143 | **0,00992** |
| **P5-8K A/20260916** | **8,8 min** | 10,3 | 19,1 min | 0,179818 | **0,00941** |
| **P5-8K K/20260916** | **8,8 min** | 10,2 | 19,0 min | 0,179138 | **0,00943** |

**El precio por minuto es el mismo; la cola se multiplicó por diecisiete.** Con
la cola de P5-8I estas partidas habrían costado unos 0,10 $ y no habrían tocado
el umbral. **Aun así el umbral es el umbral, y paré.**

**La otra condición, la aceptación, SÍ pasó:** 42,6 % contra el suelo del 20 %.

---

## Custodia

```
                            al empezar                         al acabar
motor/model.py              1e511978c251130e95169ebf8443efa1   idéntico
paintball/alma/decisor_zs.py
                            8fa03547e3228ef9df4aa94c444f9252   idéntico
paintball/alma/appraisal_zs_v42_exp.py
                            98c13d60167c80cc8334c965be75c640   idéntico
```

### La imagen

| | |
|---|---|
| etiqueta | **`gemv-anima:curforma-k0`** |
| id | `sha256:40ed61adc52b520c1624dbd669bb625ee81b52df694e8bace2869e1fc6afe0c2` |

md5 leídos **dentro**: `policy_forma.py` **`8077ee015f834f47bf4a0f9c1582d2c2`** ·
`curiosidad_forma.py` `4d2ef856a45d1b890b7135036bcd69ef` (**sin tocar, el de
P5-8H**) · `humo_curforma.py` `ff05e6d21c5869f957a8f3aa2735973c` ·
`confianza_viva.py` `6e1e444435914f0b9df287ea37555bbc` (**sin tocar**) ·
`forma.py` `b801876afda071403c5af54a28feff85` (**sin tocar**).

Políticas `gemv-p58k-A:v1` (`6a06a808-…`) y `gemv-p58k-K:v1` (`f89b2f52-…`).

### El cambio, entero

Un método nuevo y cinco líneas tocadas. **Nada más.**

```python
# policy_forma.py:661-670
def _margen_de(self, fv):
    if getattr(fv, "origen", "") == "curiosidad":
        return CVIVA.MARGEN_BASE
    return self.conf.margen()
```

Aplicado en los **dos** sitios donde se juzga (`:697`, `:703`) y en los **dos**
registros de `forma_evaluada` (`:730`, `:1154`), para que el diario guarde el
margen **usado** y no otro. **El 0,02 se importa de
`confianza_viva.MARGEN_BASE`; no hay ninguna constante copiada a mano.**

---

## El humo

```
  (a) APAGADO identico: 200/200 decisiones · 0 registros de curiosidad-forma
  (h) margen por origen: curiosidad 0.0200 · consejero (C=0,30) 0.0620
      curiosidad  ventaja 0.045 contra margen 0.0200 -> 'ok'   (area +0.04500) OK
      curiosidad  ventaja 0.015 contra margen 0.0200 -> 'area' (area +0.01500) OK
      consejero   ventaja 0.045 contra margen 0.0620 -> 'area' (area +0.04500) OK
```

Más los de P5-8H, todos verdes: veto duro discrimina, atasco en pasos, el
compromiso obedece y rompe, completada por alivio. **Corren dentro del build y
lo tumbarían.**

---

## Los siete sellos, con lo que la sonda anticipa

| | sello | la sonda | |
|---|---|---|---|
| **K1** | nuevas/100 tics K/A ≥ 1,5 **y** dentro ≥ 2× fuera | **1,05** y **1,09** | **FALLA** |
| **K2** | cero muertes dentro; puesto no baja de mediana | **0 muertes**; puesto **15 y 16 en los dos brazos** | **cumple** |
| **K3** | cero decisiones con armado a tiro en forma activa | **0** | **cumple** |
| **K4** | completadas ≥ 50 %; veto duro 5-30 % | **6,4 %**; veto duro **93,6 %** | **FALLA, doble** |
| **K5** | daño en 50 tics con forma ≤ base de A en seguro | **1,43 %** contra **0,56 %** | **FALLA** |
| **K6** | < 5 ms mediana; cero tics perdidos | **0,765 y 1,27 ms**; **0 perdidos** | **cumple** |
| **K7** | ≤ 4 $ la serie | a 0,18 $/partida → **~7,2 $** | **FALLARÍA** |

**K4 es el que más duele y es el que explica los otros:** si el 93,6 % de las
formas muere de veto duro, no llega, no descubre (K1) y está más expuesta (K5).

---

## Lo que va sin sello

### Aceptación por asiento

| asiento | nacidas | **aceptadas** | % | W mediana | ventaja mediana |
|---|---|---|---|---|---|
| K/10 | 136 | **5** | 3,7 % | **0,000** | 0,00746 |
| K/11 | 120 | **104** | **86,7 %** | **2,633** | 0,02769 |
| **agregado** | **256** | **109** | **42,6 %** | | |

**La asimetría entre asientos no solo sigue: se ha ensanchado** (3,7 % contra
86,7 %). **Y va en contra de la lectura de riqueza de P5-8E**: aquí el asiento
que acepta el 86,7 % es el **rico** (W = 2,63, el más alto medido en toda la
serie) y el que acepta el 3,7 % es el **pobre** (W = 0). **Es la tercera vez que
W apunta en una dirección distinta.**

### La pista de P5-8J

**No la puedo medir aquí.** La correlación entre ventaja y malestar del cuerpo
pedía la n de toda la serie, y la serie no ha corrido. **Con dos asientos no hay
con qué**, y no voy a publicar un ρ de n = 2.

### El compromiso

| | |
|---|---|
| tics con piernas listas | 203 |
| **obedece** | **203 = 100 %** |
| rompe | **0** — ninguna de las siete causas |
| **contra el criterio del decisor** | **196 = 96,6 % de las obediencias** |
| **coste** | **+13,041 total · +0,0665 por tic** |
| enfriamiento | 1.059 |

**El coste por tic BAJA respecto a P5-8I** (+0,0665 contra +0,174) **y eso no es
bueno**: baja porque las formas que ahora pasan están pegadas al margen, así que
la diferencia con lo que el cuerpo prefería es pequeña. **Se obedece más veces
en contra, pero cada vez cuesta menos, porque lo que se obedece vale menos.**

**Cero rupturas otra vez.** Cuarta sonda seguida. Seis de las siete causas siguen
sin verse nunca en campo.

### Lo prometido contra lo visto

**262 durante (2,8 %) · 81 después (0,9 %) · 8.935 nunca (96,3 %).**

Es **peor que el 76,9 % de «nunca» de P5-8F**, que fue el peor dato de la serie
hasta hoy.

### «Acerca al armado» en inseguro, K contra A

| | K | A |
|---|---|---|
| tics con armado a la vista, entorno inseguro | 4.396 | 2.751 |
| **el paso acerca al armado más cercano** | **10 = 0,23 %** | **22 = 0,80 %** |

**K se acerca al armado MENOS de la mitad que A.** El veto vital y el veto duro
hacen su trabajo: la curiosidad no mete al cuerpo en la boca del lobo. **Es el
dato bueno de esta sonda.**

---

## Lo que no sé, marcado como tal

**No sé si el 93,6 % de veto duro es del margen o de la distancia.** Las dos
cosas se mueven juntas: bajar el margen deja entrar formas más lejanas, y las
lejanas son las que un armado acaba cubriendo. **Separarlo pide medir la tasa de
veto duro por distancia al nacer, y con 109 formas de un solo episodio no me
fío.** Es medible en seco sobre estos diarios y no está en este encargo.

**No sé por qué un asiento acepta el 3,7 % y el otro el 86,7 %.** Con el margen
en 0,062 la asimetría ya estaba; con 0,02 se ha hecho mayor, no menor. **Y la
riqueza vuelve a apuntar al revés.**

**Un fallo mío, cazado antes de publicarlo.** La primera pasada del medidor dio
**todos los tics «inseguro»**, lo cual no puede ser. La causa era mía: construí
el historial de daño entero de antemano, y la condición `t - tt < VENTANA` es
cierta para los tics **futuros** (da negativo), así que el daño del futuro
contaba en el presente. El arnés de P5-7C lo construía incremental. Corregido
con `0 <= t - tt`, salen los tres grados. **Publicar aquel cuadro habría dado un
K5 falso.**

**Y no sé si el precio volverá a 0,10.** La cola fue de 8,8 minutos contra 0,5 en
P5-8I. **El precio por minuto es idéntico**, así que si la cola baja, el precio
baja. **No controlo la cola.**

---

## Propuesta, no ejecución

**No recomiendo lanzar las cuarenta con este margen.** No por el precio —que es
cola y puede pasar— sino porque **la sonda dice que fallarían K1, K4, K5 y K7**,
y K4 por un factor de ocho.

**Lo que la sonda enseña, y es un resultado, no un defecto:** el margen de la
puerta no era solo un filtro de cantidad. **Estaba filtrando distancia.** Con
0,062 pasaban pocas formas pero cercanas, que llegaban; con 0,02 pasan muchas y
lejanas, que no. **El 1 % de P5-8I y el 42,6 % de hoy son dos regímenes
distintos, no el mismo mecanismo con más muestra.**

**Si se quiere n sin perder la llegada, lo que yo mediría antes —en seco y
gratis, sobre estos mismos diarios— es la tasa de veto duro por distancia al
nacer.** Si la caída está toda por encima de cierta distancia, un tope de
distancia daría la n que el margen no puede dar sin romper K4. **No lo he hecho
y no lo propongo como decidido: el margen y la vara son tuyos.**

**Gasto de la sonda: 0,358956 $.** Cola vacía al acabar. Las cuarenta **no se han
lanzado**.

**PARO AQUÍ.**
