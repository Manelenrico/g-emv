# ACTA — THE PACK, PELDAÑO 3: LAS EXPECTATIVAS (cierre)
**Sellada por la mesa 2026-08-31. Spec: `the_pack_peldano3_spec.md` (md5 2e268c86…). Paquete de datos:
`the_pack_peldano3_paquete.md` (md5 7bb6b5e0…). model.py INTOCABLE (1e511978, sellos inicio/fin verdes).**

## Pregunta del peldaño
¿Nace la fiabilidad cuando cotejar tiene VARA JUSTA (radio ≤2) y MOTIVO económico? ¿Y el pueblo que cuenta con
los demás rinde distinto del sonámbulo? Principio: el censo NO ordena, AFINA valores existentes.

## Qué se construyó (observe/afina, OFF≡bit-exact)
§1 vara justa (radio-2, clase exacta, posición perdonada aw±2). §2(a) factor de ocupación [0.5,1.5] sobre
destinos de trabajo (geografía por territorio del censo; R dom/S menor/F viaje). §2(b) descuento por fuente
(peso = fiabilidad del emisor + triangulación, riding el eff/confianza). §2(c) verificación EMERGENTE (sin
término nuevo). §2(d) auto-fila (self excluido). Flag GEMV_EXPECTATIVAS; radio horneable GEMV_COTEJO_RADIO=2.

## Humo (5 puertas, tras dos correcciones)
1 OFF bit-exact ✅ · 2 ON delta≠0 (857/3200, localizado) ✅ · 3 tres correcciones en log con ejes ✅ ·
4 vara recalibrada ✅ (los 12 del forense absueltos por construcción; agregado 17%→31%) · 5 factores en rango ✅.

## VEREDICTOS SELLADOS (mesa)
- **(A) NACE la fiabilidad, robusta y diferenciada.** Mediana cotejos/emisor **54-131** (bar ≥10, clavado);
  rango de fiabilidad **0.10-0.53**, no degenerada, distingue emisores. El CONOCER-al-otro con vara justa +
  motivo económico produce una columna de reputación real.
- **(C) Rendimiento a la BAJA en 2/3, plano en 1/3, 0 muertes.** Mecanismo: el descuento §2a al **76-82%**
  (seeds densas) **dispersa el núcleo productivo** → el score cae. Confound declarado: lotería del tablón (D=1,
  N=1/celda) ⇒ dirección, no teorema. La paga grande se lee para P5 (mundos adversarios), no para machina amable.
- **(B) La división del trabajo SÍ se afina y el factor es GEOGRÁFICO.** §2a bidireccional respondiendo al
  mundo (denso→descuento; disperso→prima); §2b triangulación colapsa a 0 cuando la manada se dispersa (seed 3).

## CAREO §7 (con nombres)
- **Manel:** acertó (ii) cambio grande y (iv) fenómeno emergente; **refutado en (iii) rendimiento** (predijo
  MUCHO mejor; salió a la baja).
- **Claude-mesa:** **refutado en (ii)** (predijo delta modesto; fue sustancial) **y en (iii)** (predijo igual/
  levemente mejor; bajó).
- **El vigilante:** **mejor calibrado en (iii)** (declaró el riesgo de SCATTER, que se materializó); **refutado
  en su sorpresa (iv)** (predijo 2-ciclo social; la sorpresa real fue la reputación SLOT-ESTABLE).

## FENÓMENO EMERGENTE (no previsto por nadie): REPUTACIÓN SLOT-ESTABLE
ag1/ag4/ag6/ag3 salen fiables y ag0/ag2/ag5/ag7 bajos en las TRES semillas — hay un rasgo de "buen
corresponsal" ligado al slot, no ruido.

## CORTE FAMA × GEOGRAFÍA (encargo de la mesa; `bronce/corte_fama_geografia.py`)
Hipótesis sellada (29-ago): la fama = virtud FILTRADA por circunstancias (zona densa ⇒ más colisiones d≈2 ⇒
menos fama aun siendo veraz). **Resultado: hipótesis de DENSIDAD REFUTADA** — correlación fiabilidad↔densidad
**r = +0.47** (signo OPUESTO al predicho); dist-al-hub r = −0.04 (nada). **Por qué:** la hipótesis era cierta
bajo la vara EXACTA de P2 (densidad × aw±2); la **vara radio-2 de P3 la invierte** — donde abundan features, la
clase anunciada suele caer dentro del radio 2, así que la densidad AYUDA. La vara firmada neutralizó justo la
circunstancia que penalizaba al denso. **Lo que sí filtra (débil, r = −0.36): el ROAMING** — el errante acumula
más DERIVA DE FRAME (linaje H3) → sus anuncios caen >2 celdas → menos fama. Virtud filtrada por circunstancia,
pero la circunstancia es VAGAR, no la densidad. N=8 ⇒ dirección, no significancia. La parte no-geográfica del
ranking apunta al TEMPERAMENTO (corte futuro propuesto, no ejecutado).

## INCIDENTES CON NOMBRE (del humo)
- **H1** — enumeración de la mesa ("minero") corregida a señal real ("trabajador activo": `oficio_dep`/
  `cargo_max`, que el censo SÍ puebla; `oficio_mine≡0` estructural). Geografía conservada. Lección: calibrar el
  criterio a lo que el animal puede saber (misma que la vara del ojo).
- **H2** — bug de borde de ventana (mío): el cotejo se cerraba al entrar la celda por el borde, donde el radio-2
  se sale de lo visible. Cazado por la propia puerta 4. Curado: exigir la vecindad radio-R completa en ventana.
- **H3 (linaje aw)** — deriva de frame entre agentes >2 celdas: techa la vara del honesto en ~31% ("nivel del
  mar" del canal) y filtra la fama por roaming. Fichado, NO abierto; candidato a forense unificado (con el
  truncado del censo P1 y el desvío del anunciante P2).

## DECISIONES / PENDIENTE
- Radio 2 firmado (anclado a aw±2); subirlo sería ajustar el criterio al resultado — NO se toca.
- **P3b (factor suavizado [0.8,1.2], mismas semillas): decisión de Manel PENDIENTE; nada preparado.**
- No se abre P4 antes.

**Estado: PELDAÑO 3 CERRADO. El CONOCER-al-otro NACE (reputación robusta, diferenciada, slot-estable); el
USAR-ese-conocer para reasignar trabajo AFINA el reparto pero cuesta score en machina amable. model.py 1e511978
intacto.**
