# La Era de los Temperamentos — SPEC PARA CONGELAR (traer a Manel antes del banco)

Fecha: 2026-08-11. `model.py` INTOCABLE (`1e511978`). La vara NO cambia: los temperamentos son
**variante examinada contra ella, nunca sustituta**. `GEMV_SPARSE` encendido de serie.
**El banco N=3 @2500t NO se lanza sin la firma de Manel sobre esta spec.**

> **HALLAZGO QUE OBLIGA A RE-FIRMAR LA TABLA (paso cero, frío):** la vara hornea **`GEMV_W_S=1.40`** — el
> peso social es **el DOBLE del default de model.py (0.70)**. La tabla firmada centra su columna w_s en 0.70
> (el default), NO en la vara (1.40). Consecuencia: la tabla, tal cual, **baja w_s por debajo de la vara en
> los 8 slots** y el "clon de control" (slot3=0.70) **NO reproduce la vara** — la deja a media social. Hay que
> **re-centrar la columna w_s sobre 1.40 antes del banco**. No es un bug del flag: el flag hace lo firmado; la
> TABLA está calibrada contra el centro equivocado.

---

## ✅ FIRMA DE MANEL (2026-08-11) — TABLA CONGELADA + PROTOCOLO

**(1)** Hallazgo w_s=1.40 registrado (acta + memoria). **(2) RE-CENTRADO ADITIVO (+0.70 a toda la columna w_s):**
esta es LA TABLA del banco, congelada:

| slot | 0 | 1 | 2 | 3 (control) | 4 | 5 | 6 | 7 |
|------|---|---|---|---|---|---|---|---|
| **w_s** (=firmada+0.70) | **1.90** | **1.70** | **1.60** | **1.40** | **1.40** | **1.25** | **1.15** | **1.15** |
| **w_f** (=firmada, ya centrada) | 1.10 | 1.05 | 0.90 | 1.00 | 0.80 | 0.75 | 0.65 | 1.10 |

`GEMV_W_S_BYSLOT=1.90,1.70,1.60,1.40,1.40,1.25,1.15,1.15` ·
`GEMV_W_F_BYSLOT=1.10,1.05,0.90,1.00,0.80,0.75,0.65,1.10`. slot3 (control) = w_s 1.40 / w_f 1.00 = **la vara
exacta**. Distancias del diseño firmado preservadas (spread absoluto ±, sólo trasladado a 1.40). La
multiplicativa (×2.0) queda anotada como variante futura (caracteres extremos), no ahora.

**(3) EL CANDADO (previo al banco):** el control re-centrado (1.40/1.00) es hex-idéntico a la vara (verificado
en frío); el gate empírico `gate_temper_lock` (8 slots = control 1.40/1.00, PREG=0 @400t) debe dar
**bit-exact 3200/3200** contra la vara. **Sin ese verde no hay banco.**

**(4) BANCO** (con el candado verde): N=3 @2500t, diverso (tabla de arriba) vs la vara existente
(`tanda_p2500_r1/2/3` = {4.11,2.31,3.23}, mediana 3.23, 0 muertes). Listones L1 (cero muertes, duro) / L2
(economía en rango, duro) / L3 (score [2.0,4.2], orientativo) / división del trabajo OBSERVACIONAL. Predicciones
por perfil CONGELADAS abajo antes del disparo.

**PREDICCIONES CONGELADAS (antes del disparo, contra la vara w_s=1.40):** los perfiles con w_s **por encima**
de 1.40 (slot0=1.90, slot1=1.70, slot2=1.60) → más pegados al grupo/hub, menos distancia, más seguros; slot3=
vara; los de w_s **por debajo** (slot5=1.25, slot6=1.15, slot7=1.15) → más distancia, menos tiempo cerca del
hub, más minado lejano/forage, más riesgo; el eje w_f modula el miedo al cuerpo (slot7 w_f=1.10 alto → vaga
pero vuelve pronto; slot6 w_f=0.65 bajo → el que más arriesga). Hipótesis de la era: rompen el empate exacto
del 100% → desincronizan la navegación; RIESGO conocido (forense 150t): participación pudo bajar 4→2, el banco
@2500t es el juez. Rol casi invariante (E1–E5 en el eje R, no tocado) → la diversidad vive en la navegación.

**(5) Entremeses:** B.3 cerrado (inerte bajo ECON), B.1/B.2 dormidos con nota (banco largo tras temperamentos).
`entremeses_acta.md`.

---

## PASO CERO (Fase A.1) — verificado en frío

- **py_compile:** VERDE en los 4 fuentes tocables horneados (gemv_policy, planificador, transición, appraisal).
- **Custodia (c4-cone-poda ejecuta el fuente declarado):** VERDE en los 4 (md5 casan; el aviso de ruta-muerta
  `/app/coworld_adapter/...` es el baseline c4-survhome `44ad7424`, benigno — el `--run` usa `/app/gemv_policy.py`).
- **OFF (flag=0) ≡ bit-exact contra la vara:** VERDE, empírico. `gate_baseline` vs `gate_baseline2` (misma
  config, dos invocaciones) = **3200/3200 idénticas** ⇒ el harness es determinista cross-invocación Y el flag
  apagado es la vara exacta (el bloque va gateado por `if _TEMPERAMENTS`, no se ejecuta). **Esto es lo que
  pediste ("el flag apagado no contamina"): confirmado.**
- **El "control dentro de un run TEMPERAMENTS=1" NO es la vara** (hallazgo): `gate_temper_ctl` (los 8 con
  byslot=0.70) diverge de la vara desde el step 0 (d_curr 5.9603 vs 5.99051). Forense: **misma posición
  predicha, distinta d ⇒ distinto CONFIG.** Reconstruido bit a bit: la vara usa **w_s=1.40** (d=5.99055) y el
  "control" 0.70 revierte al default de model.py (d=5.96033). El culpable es el `GEMV_W_S=1.40` horneado, que
  `_build_active_cfg(0.70,·)` sobrescribe. **Es calibración de la tabla, no contaminación del OFF.**
- **Convivencia (tabla diversa, no crash):** VERDE — `gate_temper_div` corrió @400t PREG=0 sin crash,
  divergiendo de la vara (los perfiles muerden; conviven con ECON/survhome/SPARSE). *[nota: esa divergencia
  mezcla ahora dos efectos — la diversidad y el des-centrado de w_s; por eso hay que re-centrar primero]*.
- **Bisección que sella la causa:** `gate_temper_zero` (byslot todo-0 → default 0.70) da d **idéntica** a
  `gate_temper_ctl` (byslot 0.70), y ambas divergen de la vara igual (19.84%, mismos steps). ⇒ la divergencia
  es **el valor de w_s (0.70 vs 1.40), no el objeto ni el bloque**. Confirmado analítica y empíricamente.

---

## (a) LA TABLA DE LOS 8 PERFILES — firmada, + la coexistencia con la VARA ACTUAL

**Mecanismo** (gemv_policy `_build_active_cfg`, model.py intocable): cada agente (proceso aparte) toma `w_s` y
`w_f` de su slot en `GEMV_W_S_BYSLOT`/`GEMV_W_F_BYSLOT` y **construye un `ModelConfig` propio** (nunca toca
`DEFAULT_CONFIG`). Fija `w_s_pos` al valor ABSOLUTO del slot y arrastra `w_s_ten` con el mismo ratio. w_s =
eje **SOCIAL**; w_f = eje **FÍSICO/hp**.

**La vara de referencia** (medida, no cableada): `w_s=1.40` (horneado `GEMV_W_S`, ×2 el default 0.70),
`w_f=1.00` (sin `GEMV_W_F` horneado → default). Verificado en las 4 imágenes de la cadena (c4, survhome, cone,
cone-poda) y usado por las corridas de referencia @2500t.

**Tabla firmada (absolutos), centrada en 0.70/1.00 — el problema está en la columna w_s:**

| slot | w_s firmado | vs vara 1.40 | w_f firmado | vs vara 1.00 | arquetipo |
|------|------:|------|------:|------|-----------|
| 0 | 1.20 | −0.20 (por debajo) | 1.10 | +0.10 | EL SOCIAL/gregario |
| 1 | 1.00 | −0.40 | 1.05 | +0.05 | social-cauto |
| 2 | 0.90 | −0.50 | 0.90 | −0.10 | templado |
| 3 | 0.70 | **−0.70 (¡mitad de la vara!)** | 1.00 | 0 (=vara) | "CONTROL" (NO reproduce la vara) |
| 4 | 0.70 | −0.70 | 0.80 | −0.20 | confiado |
| 5 | 0.55 | −0.85 | 0.75 | −0.25 | independiente |
| 6 | 0.45 | −0.95 | 0.65 | −0.35 | EL SCOUT/lobo |
| 7 | 0.45 | −0.95 | 1.10 | +0.10 | EL MIEDOSO |

**La columna w_f está bien centrada** (slot3=1.00=vara; spread simétrico ±0.35). **La columna w_s está toda por
debajo de la vara** (de −0.20 a −0.95): correr la tabla no da "diversidad alrededor de la vara" sino "8 agentes
menos sociales que la vara", y el control no es control. El "codicioso" sigue sin ser expresable (la codicia
vive en w_r, no tocado).

### PROPUESTA de re-centrado (NO aplicada — decide Manel; es decisión de arquitectura)

Re-centrar SÓLO la columna w_s sobre la vara (1.40); w_f se queda como está (ya centrado). Dos transformadas:

- **Multiplicativa (×2.0 = 1.40/0.70): preserva RATIOS.**
  `w_s = 2.40, 2.00, 1.80, 1.40(control), 1.40, 1.10, 0.90, 0.90`. slot0 = 1.71× el control (como la firma).
  *Con:* el extremo alto (2.40) es un peso social fuerte, podría distorsionar el animal ganador.
- **Aditiva (+0.70): preserva el ANCHO ABSOLUTO del spread (±) de la firma.**
  `w_s = 1.90, 1.70, 1.60, 1.40(control), 1.40, 1.25, 1.15, 1.15`. spread ±0.50 alrededor de 1.40, más suave.
  *Recomendada:* menos riesgo de deformar la vara; el control queda exacto (1.40) y la diversidad es simétrica.
- **(alternativa) Preguntar la INTENCIÓN original:** si la tabla se firmó cuando la vara aún era 0.70, sus
  absolutos eran correctos ENTONCES; hoy sólo hay que trasladarlos. Si se firmó con 1.40 ya horneado, habría
  que revisar por qué se eligió centrar en 0.70.

**Recomiendo la ADITIVA** (control exacto = 1.40, spread simétrico y suave). Sea cual sea, el slot3 debe quedar
= 1.40 para ser control de verdad, y entonces `gate_temper_ctl` re-corrido con esa tabla debe dar **bit-exact**
contra la vara (notario del re-centrado).

---

## (b) PREDICCIONES CONGELADAS por perfil (contra la vara w_s=1.40 / w_f=1.00)

De c1c4: la `d` difiere por perfil vía el eje social; el *rol* es casi invariante (E1–E5 viven en el eje R, no
tocado). Predicciones de navegación/reparto espacial, modestas en rol. Con la tabla RE-CENTRADA (control=1.40):

| perfil | w_s vs vara | distancia | tiempo cerca hub | minado lejano | muertes |
|--------|------|----------:|----------:|----------:|--------:|
| más social (slot0) | por encima | más baja | más alto | menos | 0 |
| control (slot3) | = vara | = vara | = vara | = vara | 0 |
| scout (slot6) | por debajo | más alta | más bajo | más/forage | riesgo↑ |
| miedoso (slot7) | w_s bajo, w_f alto | vaga pero vuelve pronto | medio-bajo | medio | 0 |

**Hipótesis de la era:** los temperamentos rompen el empate exacto del 100% entre clones (causa del deadlock del
paso) → desincronizan espacialmente. **Riesgo conocido:** el forense de participación (150t, config vieja)
mostró participación 4→2. El banco @2500t es el examen de si a la larga ayuda o estorba.

---

## (c) LOS LISTONES (escritos antes de mirar)

Referencia = 3 corridas vara @2500t existentes (c4-survhome, PREG=1, machina_1, **w_s=1.40**):
scores **{4.11, 2.31, 3.23}**, mediana **3.23**, rango [2.31, 4.11], **0 muertes**.

- **L1 — SUPERVIVENCIA (duro):** cero muertes, como la vara.
- **L2 — ECONOMÍA (duro):** el hub no colapsa; makes y depósitos en rango de la vara @2500t (leídos de sus logs,
  no cableados).
- **L3 — SCORE (orientación, NO gate):** mediana N=3 en **[2.0, 4.2]**. La diversidad no está obligada a ganar,
  está obligada a VIVIR.
- **DIVISIÓN DEL TRABAJO — OBSERVACIONAL:** mineros distintos, extractores distintos, histograma de rol por
  slot, distancia y tiempo-cerca-del-hub por slot, depósitos/aligns por slot. El corazón del forense.

---

## (d) EL PLAN DEL BANCO (a la firma, con la tabla RE-CENTRADA)

- **Config:** EXACTA de la referencia (run_2500.sh: vara survhome+ECON, **PREGONERO=1**, machina_1, manifest
  `manifest_e4_s0_t300_2500.json`, **w_s=1.40 horneado**) **+ `GEMV_TEMPERAMENTS=1`** con la tabla
  **re-centrada** (`GEMV_W_S_BYSLOT` re-centrada sobre 1.40 — aditiva recomendada; `GEMV_W_F_BYSLOT` = la firmada
  1.10,1.05,0.90,1.00,0.80,0.75,0.65,1.10; columna despensa inerte bajo ECON, se deja caer).
- **Imagen:** c4-cone-poda (= survhome + SPARSE + temperamentos). Control (TEMP=0) NO se re-corre: la referencia
  ya está.
- **N=3 diverso** (varianza del PREG=1). **Coste ~25–27 h.** Chivato de noop 0–60t + PNG 0–60 obligatorios.
- **Gate previo a disparar:** re-correr `gate_temper_ctl` con la tabla re-centrada (slot3=1.40) → debe dar
  **bit-exact** contra la vara. Si no da bit-exact, la tabla sigue mal centrada — NO disparar.

---

## RESUMEN PARA LA FIRMA

1. Paso cero: compila/custodia VERDE; **OFF (flag=0) ≡ bit-exact contra la vara CONFIRMADO empírico** (3200/3200).
2. **HALLAZGO:** la vara hornea **w_s=1.40** (×2 el default); la tabla firmada centra w_s en 0.70 → el control
   no reproduce la vara y los 8 slots quedan por debajo. **Hay que re-centrar w_s sobre 1.40** (recomiendo la
   aditiva; w_f ya está bien). **Decisión de arquitectura: la firmas tú.**
3. Bajo ECON la columna despensa está muerta (se deja caer). El "codicioso" no es expresable (w_r no tocado).
4. Listones L1/L2 duros, L3 orientación [2.0,4.2], división del trabajo observacional. Referencia
   {4.11,2.31,3.23}, mediana 3.23, 0 muertes.
5. Banco N=3 @2500t listo, **con la tabla re-centrada y su gate bit-exact previo; no se dispara sin tu firma**.

---

## NOTA DEL BANCO — r1: LA TRAMPA SOCIAL (2026-08-14, P-2 · censo del baile)

**El extremo hiper-social (w_s=1.70) mostró en r1 una trampa de meseta:** la cuenca de comodidad de casa,
profundizada por el peso, retuvo al agente (slot1) el **91% de su vida en estado insatisfecho**; el mecanismo de
escape (la deriva del 2-ciclo D=1, el "temblor del empate") resultó **insuficiente a ese peso**. Aislado limpio
con el mismo spawn (seed 0): a w_s=1.40 el mismo agente recorre el mapa y trabaja (7 depósitos); a 1.70 queda
pinchado en una caja 16×26 lejos del hub (12 minados / 3 depósitos, motor callado desde t178). **Pendiente de
confirmar consistencia en r2/r3** (si se repite en las 3 vidas = RASGO, el primer coste estable del temperamento;
si no = geografía de la semilla). Coste COLECTIVO neutro (baile ≥15% vida: vara 14.8% vs diverso 15.4%; el
diverso puntúa más, 3.66>3.23): la diversidad **reubica** el bailarín pesado, no añade desperdicio agregado.

**EL TRÍO NO SE SELLA hasta esa comprobación en r2/r3.** La diversidad se reporta **CON su precio**, no como
éxito limpio. Detalle: `forense_censo_baile.md`, memoria `[[trampa-social-y-temblor-escape]]`.

---

## 🏅 SELLO DE LA ERA DE LOS TEMPERAMENTOS (firma de Manel, 2026-08-17)

Banco N=3 completo (encadenado r2→r3 sobre la imagen congelada de r1, image-id `716532439760`).
La comprobación de r2/r3 (censo del baile + división del trabajo) **resuelve el pendiente**.

### ✅ CONFIRMADO — a la spec como ley
**La ganancia agregada de cartera.** Mediana **3.66 vs vara 3.23 (+13.5%)**, **3/3 réplicas por encima de la
vara**, **0 muertes** (8/8 a 2500t en las tres), dispersión [3.61–4.22]. **La diversidad re-centrada no daña
y mejora la cosecha del colectivo.** (El re-centrado sobre el w_s=1.40 REAL de la vara —no el default 0.70—
fue la diferencia frente al no-avance previo.)

### ⚠️ NO-LEY — a la spec con honestidad (observado en r1, NO reproducible)
1. **La trampa social NO es rasgo del hiper-social — es GEOGRAFÍA.** El *plateau-lock* catastrófico (marooned
   ~90% de la vida, insatisfecho) **salta de slot entre corridas**: r1 → slot1 (w_s=1.70); r3 → **slot3
   (w_s=1.40, control)** al 83%. Apareció en **2/3** corridas y **puede atrapar hasta a un w_s bajo**. No es
   consecuencia del peso social alto; es un estancamiento estocástico. (slot1 %confinado: r1 92% / r2 39% / r3 22%.)
2. **La división del trabajo NO se sostiene.** corr(w_s, minado): r1 **−0.25** (no el −0.52 de una foto previa),
   r2 −0.18, **r3 −0.04** (se desvanece); Spearman ~0. Quitando al atrapado: r1 −0.18, r3 −0.00 → el poco
   negativo lo **empujaba el agente marooned** (no mina porque está pinchado), no un gradiente w_s→minado.

### Lección de método (al paper 3)
**Las leyes individuales de UNA corrida son fotos de una semilla.** El agregado (N=3) es robusto; los
"rasgos" mecánicos de r1 (trampa, división del trabajo) eran contingencia de esa realización. Lo que pasa al
paper 3: (a) la **ganancia de cartera**; (b) el **cepo estocástico** (plateau-lock) con su **mecanismo de
escape, el temblor del empate D=1**; (c) esta lección de método.

**LA ERA CIERRA.** Instrumentos del censo en la cantera (`pregonero/censo_{trap,mine,corr}.py`). Custodia de
la métrica de minado: se declara la **cargo-delta calibrada** (reproduce enteros exactos + manada 31 depósitos);
el contador "MIN" del ECON_MOTOR (`forense_participacion.md`, rango 11–116) queda **superseded**. Ver memoria
`[[banco-temperamentos-n3-medido]]` y `[[trampa-social-y-temblor-escape]]`.
