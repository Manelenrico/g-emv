# P5-8C — Por qué muere la forma de curiosidad al primer examen

En seco, **coste cero**, sin imagen y sin plataforma. Motor, decisor y tabla
intocados (`1e511978c251130e95169ebf8443efa1` al empezar y al acabar).

---

## El titular

**El examen cae a un tercio del camino, y ése es el hecho duro de la sección.**

Con velocidad 5 el cuerpo tarda **11 tics por casilla** (`mundo.coste_movimiento
= max(1, 16 − speed)`, leído del mundo, no cableado). Un trayecto de 6 casillas
son **66 tics**. El primer examen cae a los **25**.

**Las 23 formas medidas, sin una sola excepción, tardan más de 25 tics en
llegar.** Llegada mediana: **66 tics en el lento**, 55 en S-2. Se las examina
cuando llevan andado un tercio.

**Y las dos hipótesis que yo traía de P5-8B bis se caen las dos:**

- **No es el decaimiento.** La ventaja al tic 25 es **+0,06958**, prácticamente
  la misma que al nacer (**+0,06945**). No decae en veinticinco tics.
- **No es el margen, o no solo.** Con el margen actual **sobrevive el 73 %** al
  examen del tic 25 en esta medida.

**Pero hay un límite del método que manda sobre todo lo anterior, y va aquí
arriba: en seco el cuerpo nunca sigue la forma.** Por eso la ventaja se
mantiene alta a los 25 tics — el cuerpo sigue tan lejos de la frontera como al
principio. **Esta medida no reproduce la muerte en vivo, y por tanto no puede
explicarla del todo.** Lo digo antes que los números.

---

## El sello, cotejado

> Con R1 más R2 sobrevive al primer examen al menos el 50 % de las aceptadas; si
> con las cuatro reglas juntas sigue muriendo más del 80 %, entonces sí es un
> resultado y no un defecto.

| | **lento** | **S-2** |
|---|---|---|
| **R1 + R2** | **9/11 = 82 %** | **3/12 = 25 %** |
| las cuatro juntas | 7/11 = 64 % | 0/12 = 0 % |

**En el lento —el mundo objetivo— el sello CUMPLE: 82 %, muy por encima del
50 %.** Y con las cuatro juntas sobrevive el 64 %, así que **no se dispara la
cláusula del «resultado»**: no puede decirse que la curiosidad como forma no
sobreviva a una puerta honesta.

**En S-2 pasa lo contrario**, y es informativo: R1+R2 da 25 % y las cuatro
juntas **0 %**. En un mundo con cazadores la forma no llega.

---

## Tabla de cuatro reglas por cuatro contadores

Supervivencia al **primer examen** de las formas aceptadas:

| | R0 actual | R1 margen 0,02 | R2 horizonte | R3 exp=1 | **R1+R2** | las 4 |
|---|---|---|---|---|---|---|
| **lento** (n=11) | 8/11 = **73 %** | 9/11 = 82 % | 7/11 = 64 % | **0/11 = 0 %** | **9/11 = 82 %** | 7/11 = 64 % |
| **S-2** (n=12) | 10/12 = **83 %** | 12/12 = 100 % | **0/12 = 0 %** | **0/12 = 0 %** | 3/12 = 25 % | 0/12 = 0 % |

### La ventaja en los tres instantes

| | tic 0 | **tic 25** | **llegada** | tic 25 con exp=1 |
|---|---|---|---|---|
| **lento** | +0,06945 | **+0,06958** | **+0,07562** | +0,03232 |
| **S-2** | +0,06910 | +0,06403 | **+0,00000** | +0,02380 |

(medianas; margen actual **0,062**, margen base **0,02**)

**R3 mata todo, en los dos mundos.** Bajar el exponente de 3 a 1 hunde la
ventaja de ~0,070 a ~0,032, por debajo del margen. **Era una regla para separar
causas, no una propuesta**, y confirma que **el exponente cúbico de `R-LLAMADA`
es lo que hace que la forma tenga ventaja en absoluto.**

**En S-2, R2 mata todo.** A la llegada la ventaja mediana es **+0,00000**: en un
mundo con cazadores, cuando el cuerpo habría llegado, la forma ya no vale nada.
En el lento ocurre lo contrario: a la llegada la ventaja es **mayor** que al
nacer (+0,0756 contra +0,0694).

### El tiempo de llegada, que es el hecho nuevo

| | trayectos | **paso** | **llegada proyectada** | trayectos que duran más de 25 tics |
|---|---|---|---|---|
| **lento** | 3 a 8 casillas | 11 tics/casilla | **mediana 66** (33-88) | **11 de 11** |
| **S-2** | 5 a 7 casillas | 11 tics/casilla | **mediana 55** (55-77) | **12 de 12** |

---

## (4) Con R1 y R2 juntas: ¿se cobra el alivio prometido?

**En el lento, 9 de 11 formas se completarían. Y en las nueve la ignorancia
global proyectada baja de verdad: 9 de 9.**

**Bajada mediana: 0,05252 — 121 casillas de 2.304.** No es un alivio nominal:
es un quinto más de arena vista por forma completada.

Es el dato más favorable de toda la sección, y también el más frágil: son nueve
formas.

---

## Lo que no sé, marcado como tal

**Lo más importante: esta medida no reproduce la muerte en vivo.** En seco el
cuerpo no sigue la forma, así que a los 25 tics sigue lejos de la frontera y la
ventaja se mantiene. En vivo el cuerpo **sí** avanza, la ignorancia baja y el
alivio que queda es menor. **La sospecha razonable es que ésa sea la causa real
de la muerte al primer examen** — pero **no está medido aquí y no lo afirmo**.
Medirlo pide seguir la forma, y seguir la forma es el campo.

**La n es pequeña: 11 y 12 formas.** Salen de un muestreo cada 200 tics con tope
de doce por asiento, y del filtro de que la ventaja al nacer supere el margen
actual. Los porcentajes de la tabla se apoyan en denominadores de once y doce:
**un caso vale nueve puntos porcentuales.**

**No sé por qué el lento y S-2 se comportan al revés en R2.** En el lento la
ventaja crece hasta la llegada; en S-2 se anula. Lo más probable es que en S-2 el
mundo cambie mucho en 55 tics —cazadores que aparecen— y en el lento no, pero no
lo he medido.

**R3 no es una propuesta de diseño** y no la trato como tal. Solo sirve para
decir que el exponente cúbico es lo que sostiene la ventaja.

---

## Propuesta, no ejecución

**El sello cumple en el mundo objetivo, así que la lectura de «resultado, no
defecto» queda descartada**: la curiosidad como forma **sí** sobrevive a una
puerta honesta si el examen no cae antes de que se pueda llegar.

Lo que los datos apoyan, por orden de evidencia:

1. **R2 es el arreglo con más fundamento**: el primer examen no debería caer
   antes de la llegada proyectada. **11 de 11 formas se examinan a un tercio del
   camino**, y eso es un hecho del reloj del mundo, no una opinión.
2. **R1 ayuda poco por sí sola** (73 % → 82 %) y toca la puerta, que es lo que
   da valor a todo lo demás. **No la recomendaría sin R2.**
3. **R3, descartada**: hunde la ventaja en los dos mundos.

Y una reserva: **en S-2 nada de esto funciona.** Si la serie de cuarenta va al
lento sin cazadores, bien; si alguna vez va a un mundo con ellos, esta medida
dice que la forma no llegará.

**No he cambiado nada.** Decidir es de la mesa.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1     (idéntico al empezar y al acabar)
paintball/alma/decisor_zs.py         8fa03547e3228ef9df4aa94c444f9252
paintball/alma/appraisal_zs_v42_exp.py
                                     98c13d60167c80cc8334c965be75c640
```

`cantera/paper5/mide_P58C.py` · datos `P58C_lento.json`, `P58C_s2.json`.
**Gasto: cero.** Ninguna imagen, ninguna sonda, ningún episodio.

**PARO AQUÍ.**
