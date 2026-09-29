# P5-6C · tanda 1 (repetida) — Doce episodios con los arreglos dentro

Con el sí de Manel. **Sin cotejar sellos: eso es al final, sobre las sesenta.**

**Los tres arreglos funcionan en el campo, y dos están probados sin mirar el
código.** El parte va con contenido en **165 de 165 citas (100 %)** y con **cero
interrogantes**; la carrera del hilo no volvió a disparar (**cero reventones**
en 168 evaluaciones, contra 1 de 176); y `/spend` cuadró con la cabecera en los
ocho asientos de F.

**Veinticuatro diarios enteros, ningún freno, 0,736240 $ la tanda.**

**Y aparece la primera relación de verdad de la serie**: el consejero **calla
más cuando el parte le dice que le rechazaron** (36,7 %) que cuando le dice que
le aceptaron (16,7 %), y **no calla nunca** cuando aún no tiene formas juzgadas
(0 %).

> **La tanda anterior no se mezcla.** Está guardada aparte en
> `cantera/paper5/t1_descartada/` y `paintball/runs/descartada_P56C_t1_*`.

---

## Los arreglos

### 1. El parte iba mudo · causa raíz

`forma.curva_H` devuelve por punto de control `tic`, `d`, `vida`, `W` y `pos`,
**y nunca las necesidades**. Sin ellas `_detalle` no podía rellenar «lo que el
cuerpo proyectó» y escribía `?` en todos los partes, en todas las partidas.

**`forma.py` es la regla y no se ha tocado** —md5 `b801876afda071403c5af54a28feff85`,
el mismo de P5-6A—, así que la proyección se repite en `policy_forma.py`
(`_nec_curva`) con el mismo recorrido, solo para apuntar las necesidades.

**Y al arreglarlo salieron dos defectos más, que también van corregidos:**

- **«Lo que el cuerpo sintió de verdad» no se rellenaba nunca.** Ahora se apunta
  al alcanzar cada punto de control (`nec_ahora`).
- **El parte tenía un desfase de índice**: comparaba el tramo *siguiente*
  (`curva[i]` contra `curva[i+1]`). El tramo `i` va del punto `i−1` al `i`, y
  para el primero el punto de partida es el estado del instante en que se juzgó
  (`nec0`).

### 2. La comprobación de campo, que no depende del código

En cada cita se escribe `forma_cita_cuerpo` con el md5 del **cuerpo que sale por
el cable**, sus bytes, si el parte se encontró dentro, su longitud, las primeras
300 letras **sacadas de ese cuerpo** y —lo que lo caza sin mirar el código— el
**número de interrogantes**.

**Tres citas de la partida F de la semilla 20365645, asiento 10:**

```
--- cita 1 · tic 500 · md5 del cuerpo 187ebbf103f5bce03897d0fb9808248b · 29.103 bytes · parte 143 bytes · interrogantes 0 ---
Es tu primera forma en esta partida, o ninguna de las anteriores llego a juzgarse.
Tu confianza esta en 0.30 y el margen que te piden es 0.062.

--- cita 2 · tic 750 · md5 del cuerpo 02c5e0414b1bc69974e50e89aff6f41a · 29.583 bytes · parte 678 bytes · interrogantes 0 ---
Esto es lo que paso con tus formas desde la ultima vez:

- Forma 1 (3 tramos): RECHAZADA por area.
  Tramo 1: dijiste vida 0, manos 0, vinculo - por F-HERMANO-GOLPE;
           el cuerpo proyecto vida 0, manos 0, vinculo 0; ese tramo no llego a vivirse.
  Tramo 2: dijiste vida 0, manos +, vinculo - por R-CAREN...

--- cita 3 · tic 1000 · md5 del cuerpo 1f24eeed55e52a007d529d95405b36e1 · 30.138 bytes · parte 1.134 bytes · interrogantes 0 ---
Esto es lo que paso con tus formas desde la ultima vez:
...
```

El parte **crece** (143 → 678 → 1.134 bytes) según se acumulan formas juzgadas y
el md5 del cuerpo **cambia en cada cita**, que es lo que prueba que no se manda
lo mismo una y otra vez.

**Y en la cita 2 se ve para qué sirve:** el consejero dijo **vínculo `−`** por
`F-HERMANO-GOLPE` y el cuerpo proyectó **vínculo `0`**. Esa es exactamente la
discrepancia que P5-5B midió en banco, y que hasta ahora el consejero no podía
ver.

### 3. La carrera de `_juzga`

`_juzga` recibía la `mem` y los `bloqueos` **vivos**, que el bucle del juego muta
cada tic. Ahora recibe **copias**, como ya hacía la inyección de candidatos.

Humo **(b5)**, nuevo: se muta `mem` y `bloqueos` desde otro hilo mientras se
juzga.

```
humo (b5) OK: con la memoria y los bloqueos mutando en otro hilo, 12 juicios con COPIAS: cero reventones y el veredicto es el mismo que en limpio (`area`)
humo (b5) · contraprueba (informativa, no aseverada): con los objetos VIVOS y la misma mutacion, 0 de 12 juicios revientan
```

**La contraprueba no disparó**, y lo digo tal cual: la carrera es rara —una de
cada 176 en el campo— y el arreglo es **preventivo**, fundado en esa observación
y no en el humo. Lo que sí es prueba es el campo: **cero reventones en 168
evaluaciones**, contra 1 de 176 en la tanda descartada.

### La imagen

`gemv-anima:forma-c1bis`,
**`sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94`**.
Dentro pasan **los dieciséis humos del cuatro** y **los doce de las formas**.

**Nada más ha cambiado**, y se comprueba por md5:

| fichero | md5 | igual que |
|---|---|---|
| `forma.py` | `b801876afda071403c5af54a28feff85` | P5-6A |
| `proyeccion.py` | `bbc42daeaa769c783844997067ef148d` | P5-6A |
| `traductor_forma.py` | `b310bb72884ef5f4e3510ab803cd2776` | P5-5B |
| `instruccion_forma.md` | `02653e4edf04f3bdd9a0ac3deda9aa01` | P5-6A |
| `tabla_ensenada.md` | `9d53807699c4ee2be31d8dd173196de0` | P5-6A |

Misma cadencia (250), mismo tope (25 s), mismo `SPEND_CADA` (10).

---

## La tanda

Semillas **20260916, 20365645, 20470374, 20575103**, los tres brazos con la
misma semilla, una petición por episodio, creadas a las 21:18. **Cola vacía
antes y después.** Políticas: `gemv-p56c2-A:v1` (`f2e75f10…`),
`gemv-p56c2-F:v1` (`aa1de6b6…`), `gemv-p56c2-T:v1` (`98d465dc…`).

### El precio

| brazo | precios | **mediana** |
|---|---|---|
| **A** | 0,034060 · 0,042097 · 0,045621 · 0,068913 | **0,043859 $** |
| **F** | 0,039481 · 0,040851 · 0,043655 · 0,069506 | **0,042253 $** |
| **T** | 0,038733 · 0,072379 · 0,119452 · 0,121492 | **0,095916 $** |
| | | **total 0,736240 $** |

**Ninguno pasa de 0,20 $.** Y la tanda ha salido **un 28 % más barata** que la
descartada (0,736 contra 1,028), con la misma carga: el precio depende de cómo
se solapen los pods, no del brazo.

**Haiku por asiento:** mediana **0,141205 $**, máximo **0,178756 $**, suma
0,846397 $. **Ninguno pasa de 0,50 $.**

**Gasto acumulado: 122,456432 → 123,192672 $**, diferencia 0,736240 $, exacta.

---

## C2 · Las medidas

### Diarios y frenos

**Los veinticuatro enteros**: los veinticuatro traen `final` y en los
veinticuatro `match_ticks` es el último tic vivo más uno. **Ningún freno mordió.
Nada que descartar.** Las vidas van de 321 a 13.728 tics.

### Formas

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **A** | 8 | **0** | 0 | **0** | 0 |
| **F** | 8 | 161 | 168 | **7** | 5 |
| **T** | 8 | 254 | 254 | **6** | 6 |

**Aceptadas por vida:** F `[0,0,0,0,1,1,2,3]` **mediana 0,5** · T
`[0,0,0,0,0,1,1,4]` **mediana 0,0**.

**Edad de la primera aceptada:** F `[759, 1479, 3520, 5122]` mediana **2.499** ·
T `[1769, 3269, 11019]` mediana 3.269.

**Veredictos:**

| | F | T |
|---|---|---|
| rechazada por **área** | 106 | **243** |
| **el consejero calló** | **55** | — |
| rechazada por vida mínima | 0 | 5 |
| **ok** | 7 | 6 |
| **revienta** | **0** | **0** |

Todas las caídas, en los dos brazos, por «en la reevaluación deja de ganar
(área)».

### El consejero, en F

| semilla/asiento | citas | fallos | saltadas | latencia mediana | **callar** | `/spend` cuadra |
|---|---|---|---|---|---|---|
| 20260916/10 | 29 | **0** | 3 | 7.425 ms | 13/29 = 45 % | sí |
| 20260916/11 | 29 | **0** | 3 | 7.288 ms | 12/29 = 41 % | sí |
| 20365645/10 | 34 | **0** | 5 | 7.470 ms | 10/34 = 29 % | sí |
| 20365645/11 | 5 | **0** | 1 | 4.816 ms | 0/5 = 0 % | sí |
| 20470374/10 | 27 | **0** | 5 | 7.066 ms | 16/27 = **59 %** | sí |
| 20470374/11 | 28 | **0** | 3 | 6.303 ms | 3/28 = **11 %** | sí |
| 20575103/10 | 7 | **0** | 1 | 3.876 ms | 1/7 = 14 % | sí |
| 20575103/11 | 2 | **0** | 0 | 4.594 ms | 0/2 = 0 % | sí |

**Cero fallos en 161 llamadas.**

### El parte (las dos medidas nuevas)

**Fracción de citas con parte no vacío: 165 de 165 = 100,0 %.**
**Interrogantes en total: 0.**

**Callar frente a lo que decía el parte en esa cita:**

| lo que le decía el parte | calla | de | **%** |
|---|---|---|---|
| **le rechazaron la anterior** | 54 | 147 | **36,7 %** |
| le aceptaron la anterior | 1 | 6 | **16,7 %** |
| sin formas previas | 0 | 8 | **0,0 %** |

**El consejero calla más cuando le están rechazando.** Es la primera relación
que la serie enseña, y hay que decir tres cosas de ella: la n de «le aceptaron»
es de **seis citas**, el reparto de citas entre los tres casos no es
independiente del momento de la partida, y esto es **una tanda de cinco**. No
se afirma nada todavía.

### La medida principal

| | **F** | **T** |
|---|---|---|
| puntos de control alcanzados | **9** (3 asientos) | **3** (1 asiento) |
| `d` real ≤ proyectada + 0,05 | 4/9 = **44,4 %** | 2/3 = 66,7 % |
| `d` real **por debajo** de la de A en la misma zona | 4/9 = **44,4 %** | 1/1 |
| diferencia (real − A), mediana | **+0,15421** | −1,24518 |

La n sigue siendo minúscula. Lo único reseñable frente a la tanda descartada es
que ahora **hay casos en que la `d` real queda por debajo de la de A** (4 de 9
en F), cuando antes eran 0 de 2 y 0 de 3.

### Confianza, hilo y vida

**Trayectorias de C** (los demás asientos no alcanzaron ningún punto y se
quedaron en 0,30): F/20260916/11 `0,15 → 0,00 → 0,00` · F/20365645/11
`0,40 → 0,50` · F/20470374/10 `0,15 → 0,00 → 0,10 → 0,20`. **El cuerpo no calló
al consejero ni una vez.**

**El hilo** cuadra salvo cuando el hermano muere antes (F/20365645/10 dijo 204 y
oyó 32, porque su hermano murió en el tic 2.004). Ningún mensaje pasó de 120
ASCII.

| brazo | vidas (mediana) | puestos | calma literal |
|---|---|---|---|
| A | **8.170** | 4 · 5 · 13 · 14 · 14 · 15 · 16 · 16 | 0 |
| F | 7.893 | 6 · 14 · 15 · 15 · 15 · 16 · 16 · 16 | 0 |
| T | **8.424** | 4 · 5 · 9 · 14 · 14 · 15 · 16 · 16 | 0 |

### El tiempo por tic, y el precio del arreglo

| asiento | mediana | p95 | **máximo** | en el hilo |
|---|---|---|---|---|
| F/20260916/11 | 1,763 ms | 8,036 | **971,2 ms** | 7.735/7.870 |
| F/20260916/10 | 1,054 ms | 6,559 | **633,2 ms** | 7.868/7.988 |
| F/20365645/10 | 0,545 ms | 3,035 | **582,0 ms** | 9.647/9.749 |

**El arreglo del parte se paga en los máximos.** En la tanda descartada el peor
tic era de 258 ms; ahora hay tres por encima de 580 y uno de **971 ms**. La
causa es que `nec_ahora` y `_detalle` corren **en el bucle del juego**, no en el
hilo: una `appraise` extra al alcanzar cada punto de control y al cerrar cada
forma. Las medianas siguen por debajo de 1,8 ms y el p95 por debajo de 8, así
que no se ha perdido ningún tic —el vigía no disparó en ninguna partida—, pero
**es lo primero que hay que vigilar si la serie sigue**, y se arregla llevando
esas dos llamadas al hilo.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Imagen: `gemv-anima:forma-c1bis`
(`sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94`).
Roster: `roster_lento_v1.json`, md5 `a2293bd16ee94e6d4c2f4683b57c2a09`.
`policy_forma.py` `746a41f1116c0f1d409ee2b91f6fe0ff`, `humo_forma.py` `4aefd120bf739736a3c4719029b7283c`,
`Dockerfile.forma` `b2fdc2145f6199d1e46e85cafb9722e5`.

**PARO AQUÍ.** La tanda 2 espera el sí.
