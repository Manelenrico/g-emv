# SPEC — THE PACK, PELDAÑO 1: EL CENSO (solo-observar)
**Sellada en mesa 2026-08-28. Se archiva; reporta md5. Sustrato observable certificado en
`the_pack_hechos_percepcion.md` (md5 5ed678fa577496a4fc8df7cb69f72a57). model.py INTOCABLE
(1e511978c251130e95169ebf8443efa1). Custodia: mesa de temporada. Ejecuta: el vigilante, tras venia.**

## 1. Pregunta única
¿Cuánta individualidad captura la pura contabilidad del otro? Tras una vida, ¿las ocho filas del censo son
DISTINGUIBLES (este es el minero, ese el conquistador, aquel el pasmado) o salen parecidas? Punto cero
declarado: **el pueblo sonámbulo** (los otros como clima).

## 2. Qué se construye
Una TABLA PERSISTENTE por hermano (ag0..ag7), alimentada SOLO de lo observable certificado (28-ago). El
censo **NO toca ninguna decisión**: el animal observa y apunta; su conducta queda IDÉNTICA (regresión
bit-exacta lo garantiza). Incluye la **AUTO-FILA** (el animal como octava entrada, con datos propios).
Todo TRAS FLAG (p.ej. `GEMV_CENSO`); con flag OFF, **bit-exacto**.

## 3. Las cinco columnas (+ regalo)
1. **HERENCIA** (se escribe una vez, ~t10): ¿cogió heart de cuna? ¿cuántos? distancia de nacimiento al hub.
   [directo: `inv:heart` observado temprano + posición inicial vs hub]
2. **TERRITORIO** (acumulado): centroide y radio de sus posiciones observadas; % de ticks visto en mi disco.
   [directo: posición del observado por tick]
3. **OFICIO** (contador de coincidencias — el diseño de la noche creativa): crédito por proximidad a eventos
   económicos (junto a mina + `team_held` sube; junto al hub + depósito). **AMBIGÜEDAD DECLARADA:** si varios
   hermanos están junto al evento, el crédito se reparte o se descarta (a decidir en implementación,
   documentado): la falibilidad del contador es parte de la pregunta, no un bug. [inferido]
4. **DINERO** (directo, tick a tick): hearts que porta, carga, gear. Máximos, medias, y TRANSICIONES
   observadas (lo vi con 3, ahora 2 ⇒ gastó cerca). [directo: `inv:heart`/cargo/gear del observado]
5. **PALABRA** (observada, no interpretada): la `vibe` que declara. Se apunta; no se cree ni se descree.
   Columna sembrada para el futuro examen declaración-vs-conducta. [directo: `vibe`]
- **(+ regalo del corte de mesetas)** % de ticks QUIETO observado (el laborioso vs el pasmado). Barato, entra.

## 4. Restricciones
- El censo solo cuenta lo que el disco alcanza (radio ~6): la tabla es **PARCIAL por construcción**, como la
  de cualquier animal. La **COBERTURA** (% de vida con cada hermano a la vista, por par observador-observado)
  se mide y reporta: es dato, no defecto.
- Sin pregonero firmado (peldaño 2), sin expectativas, sin empatía, sin ley general: SOLO contabilidad.
- model.py intocable; todo tras flag; OFF ⇒ bit-exacto.

## 5. El examen
Vidas de **10.000t** (el mundo de la era, economía viva: ahí hay conducta que contar), **N=3**, BRAZO ÚNICO
(titular con era ON + censo observando). Al final de cada vida, el censo de cada agente se vuelca a log.

## 6. Lectura (criterio simple, sellado)
- **DISTINGUIBLE:** las filas de los 8 hermanos difieren de forma CONSISTENTE entre observadores (el censo que
  ag0 tiene de ag3 se parece al que ag5 tiene de ag3 más que al de ag4); Y los perfiles CASAN con la conducta
  real del replay (el que el censo llama minero ES el que más minó, verificable desde fuera).
- **RUIDO:** filas planas o inconsistentes entre observadores.
- Métrica auxiliar: cobertura por par observador-observado.

## 7. Predicciones (formato simple, los tres, ANTES de correr)
¿Saldrán distinguibles los 8? ¿Cuántos de los 8 perfiles casarán con la conducta real? ¿La cobertura del
disco (radio 6) alcanzará, o deja el censo anémico?

**El vigilante (sellada 2026-08-28, antes de implementar/correr):**
- **¿Distinguibles?** PARCIALMENTE. El peldaño C mostró conducta heterogénea real (unos convierten, otros
  cargan y no entran, unos minan más) → hay individualidad que contar. Pero la era produce muchos «cargan y
  se quedan» que se parecen; apuesto **3-5 de 8 filas claramente distinguibles**, el resto en el racimo
  «pasmado/parecido».
- **¿Cuántos perfiles casan con la conducta real?** Los de columnas DIRECTAS (DINERO, TERRITORIO, PALABRA)
  casarán bien (observación directa); el OFICIO (inferido, ambiguo por co-presencia) casará peor. Apuesto
  **4-6/8 casan en agregado** (el minero pesado y el conquistador se distinguen limpio; los medianos se
  confunden), y el OFICIO será la columna más ruidosa.
- **¿Cobertura?** ADECUADA-PERO-PARCIAL, y BIMODAL: alta cuando el racimo está en el hub (los GIFs del peldaño
  C mostraron conducta hub-céntrica), baja cuando se dispersan a minar/conquistar (extractores/junctions
  lejos, fuera del radio 6). Predigo cobertura mediana **~40-60%** de la vida por par cercano, pero los
  EVENTOS del OFICIO (minar lejos, conquistar lejos) caen fuera del disco de casi todos → **el OFICIO sale
  anémico** aunque TERRITORIO/DINERO/PALABRA no. El censo NO será anémico en general; su punto ciego es el
  oficio a distancia.

**Manel (sellada 2026-08-28):** distinguibles SÍ; **~70% de aciertos (5-6/8** perfiles casando con la
conducta real); cobertura sin apuesta.
**Claude-mesa (sellada 2026-08-28):** distinguibles SÍ **a dos velocidades** (nítidos los de plaza, borrosos
los periféricos); **4-5/8 aciertos**; cobertura mediana **15-30% por par**.

**Careo §7 (completo):** ¿distinguibles? los tres SÍ (vigilante: parcial 3-5; Manel: sí; mesa: sí a dos
velocidades). ¿Aciertos/8? vigilante 4-6, mesa 4-5, **Manel el más optimista 5-6 (~70%)**. Cobertura:
**vigilante 40-60% (racimo domina), mesa 15-30% (dispersión domina)**, Manel sin apuesta — el eje de
desacuerdo es cuánto tiempo pasan los hermanos a la vista. El examen arbitra.

---
**Estado: CORRIDO Y ENTREGADO (2026-08-28). Humo VERDE (regresión censo ON==OFF bit-exacta 3200/3200; enchufe:
vuelca y puebla, consistente entre observadores). Examen N=3 10.000t completo (14250/19548/13917 s; md5 model.py
`1e511978` inicio/fin OK; 9 volcados/vida). Paquete `the_pack_peldano1_paquete.md` (md5 499594218b14…) +
24 censos crudos `the_pack_censos_crudos.md` (2eb37eea…). Implementación en `bronce/gemv_policy_bronce.py`
(flag GEMV_CENSO, observe-only), imagen `cvc-gemv-bronce:era`, runner `bronce/run_pack_censo.sh`, OFICIO 1/k.
DOS BUGS DE FIDELIDAD del censo a aislar (NO tocan la conducta, bit-exacta): carga sobre-leída (~190 vs 10 real)
y auto-conteo de cobertura (residuo >100% para el más visible). SIN LECTURA — distinguible/ruido y careo §7 de
la mesa. model.py INTOCABLE.**
