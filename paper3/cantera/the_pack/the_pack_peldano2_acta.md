# ACTA — THE PACK, PELDAÑO 2: EL CORRESPONSAL (cierre)
**Sellada por la mesa 2026-08-30. Paquete de datos: `the_pack_peldano2_paquete.md` (md5 ea118f21…).
Spec: `the_pack_peldano2_spec.md` (md5 a2a4d66ed6…). model.py INTOCABLE (1e511978). Observe-only estricto.**

## Pregunta del peldaño
¿Nace la columna de FIABILIDAD por emisor del cotejo NATURAL (pasivo) de la vida? Sub-pregunta: ¿los anuncios
firmados hacen legibles a los periféricos (la niebla antes-vs-después)?

## Custodia del examen
N=3 vidas 10.000t nativos, MISMAS 3 semillas de P1 (170534803 / 120290872 / 176280986). Titular: era ON +
censo LIMPIO + **pregonero ON** + corresponsal (firma + fiabilidad, justicia temporal edad=300). Sellos md5
model.py inicio/fin OK (1e511978, intacto). 9 dumps censo+correo por vida. `firma_mala=0`, 0 errores, 0
falsificaciones. Humo previo: 3 puertas verdes (enchufe; bit-exact 3200/3200 con pregonero OFF determinista —
el diff pregonero-ON está confundido por la lotería D=1 del tablón, probado con control que diverge en step 3;
cotejo verificado a mano).

## VEREDICTO (por el criterio sellado, sin estirar)
**NO NACE la fiabilidad por vía PASIVA.** Los cotejos naturales son anecdóticos (2-13 por emisor en las 3
vidas juntas) y los aciertos degeneran a ~0 (fiabilidad 0.000 en casi todos; único no-cero en agregado: ag3
= 0.333, de 1 sola vida / 3 cotejos). El denominador no llega al "puñado no-anécdota" que el spec exigía.

**Causa (medida, NO bug):** los OÍDOS son broadcast (todo el mapa); el OJO solo re-verifica el patch propio
(radio territorial ~3-5, sección A del paquete). El cotejo natural = *footprint pequeño del ojo ∩ anuncios
map-wide* → anecdótico por construcción. Ejemplo: ag0 acumula 200 anuncios oídos pero cotejа 2 celdas en
9000t (la cuenta satura a t≈1000 y no crece). Los pocos aciertos caen por (a) junctions que flipean de dueño
en horizonte largo y (b) ruido de localización en extractores (aw±2, ya fichado).

## HALLAZGO MAYOR DEL PELDAÑO (lectura sellada)
**El broadcast resuelve el CONOCIMIENTO, no la CONFIANZA.** La cobertura efectiva por OÍDOS es **100% en TODOS
los pares obs→emisor, en los 3 mundos**; la niebla de ojo de P1 (pares <15%: 2/24/14 según vida) queda
**rescatada al 100%**; la firma se verifica contra fichero (0 falsificaciones). Los periféricos pasan de
invisibles a plenamente legibles COMO EMISORES. El pueblo **sabe de oídas y no puede comprobar**: la
fiabilidad exigirá DISEÑO ACTIVO (P3).

## CAREO §7 (con nombres)
Los TRES sobre-predijeron el nacimiento de la fiabilidad.
- **Manel — refutado doble:** predijo (ii) "los de la niebla, poco más legibles" → los oídos rindieron MUCHO
  más (legibilidad total); predijo (iii) "fiabilidad pareja" → no fue pareja sino ~0.
- **Claude-mesa — acertó la grieta, erró el nivel:** predijo la duda en "los cotejos de lo LEJANO" (la grieta
  real: el ojo no llega al territorio ajeno), pero predijo el nacimiento al 70% y "alta y pareja".
- **El vigilante — el más cercano en dirección:** predijo (iii) "no lisa, junctions que FLIPEAN fijan el
  techo" (dirección correcta) y enmendó en el humo con el ruido de localización; pero también sobre-estimó el
  nivel (nace ~80%). Acertó además (ii) niebla de oídos casi fuera.

## FORENSE flip-vs-ruido (encargo único de la mesa)
Vida corta con `GEMV_CORRESPONSAL_DBG` (chivato del cotejo, gated OFF por defecto, inerte). Separa por qué
fallan los aciertos-cero: ¿la junction cambió de dueño entre anuncio y cotejo (FLIP), o el extractor colisiona
por localización (RUIDO)?

**Resultado (t2000, mundo censo, 12 cotejos — TABLA CRUDA):**

| recep←emis | celda | anunciado → observado | edad | acierto | clase del fallo |
|---|---|---|---|---|---|
| ag0←ag1 | (-2,0) | junction_gray → junction_gray | 0 | **1** | — (acierto: junction aislada) |
| ag1←ag0 | (-2,0) | junction_gray → junction_gray | 0 | **1** | — (acierto: junction aislada) |
| ag3←ag6 | (15,-1) | extractor_oxygen → extractor_carbon | 0 | 0 | localización (par O/C d≈2) |
| ag6←ag3 | (15,-1) | extractor_carbon → extractor_oxygen | 0 | 0 | localización (par O/C d≈2) |
| ag4←ag1 | (17,-3) | extractor_carbon → extractor_oxygen | 0 | 0 | localización (par O/C d≈2) |
| ag1←ag4 | (17,-3) | extractor_oxygen → extractor_carbon | 1 | 0 | localización (par O/C d≈2) |
| ag1←ag6 | (19,-1) | junction_gray → extractor_oxygen | 34 | 0 | localización (junction/ext d≈2) |
| ag6←ag1 | (19,-1) | extractor_oxygen → junction_gray | 1 | 0 | localización (junction/ext d≈2) |
| ag6←ag5 | (21,-4) | junction_gray → extractor_silicon | 180 | 0 | localización (junction/ext d≈2) |
| ag5←ag6 | (21,-4) | extractor_silicon → junction_gray | 12 | 0 | localización (junction/ext d≈2) |
| ag1←ag7 | (16,9) | junction_gray → extractor_carbon | 189 | 0 | localización (junction/ext d≈2) |
| ag7←ag1 | (16,9) | extractor_carbon → junction_gray | 19 | 0 | localización (junction/ext d≈2) |

**LECTURA DEL FORENSE (corrige la premisa flip-vs-ruido): el reparto es 0 flip / 10 ruido.** NO hay ni un
solo flip de dueño verdadero (cero filas `junction_gray → junction_own/rival`): en esta economía frugal las
junctions apenas se conquistan y se quedan `gray`. Las 10 fallas son TODAS **colisiones de localización**
(`aw±2` sobre features adyacentes a d≈2): 4 pares extractor O/C + 6 colisiones junction/extractor. Los 2
aciertos son la única junction aislada, sin vecino de otro tipo. **Corrección al §7(iii):** el vigilante
predijo que los FLIPS de junction fijarían el techo; el dato lo refuta — el techo lo fija SOLO la localización
(el vigilante acertó "no será liso", erró el mecanismo). La causa raíz del aciertos≈0 es geométrica/perceptiva
(features densamente empaquetadas + `aw±2`), no la dinámica del mundo. Fuente: `GEMV_CORRESPONSAL_DBG`,
`_tmp_gemv/correo_flip_dbg`.

## DECISIONES SELLADAS
- **NO se toca el match.** Aflojar la vara de verdad (exacto → proximidad/familia) sería cambiarla a mitad de
  historia. Si se reconsidera, será en la spec de P3 con sus sellos.
- **NO se abre P3.** Se diseña en la mesa y llegará como spec. El importar (P4) no se abre antes.
- El ruido de localización (aw±2 en escena densa) sigue fichado como textura del canal / forense futuro.

**Estado: PELDAÑO 2 CERRADO. Conocimiento por oídas = LEY (legibilidad total); confianza por cotejo pasivo =
NO-LEY (anecdótica). Próximo: la mesa diseña P3 (el cotejo activo / las expectativas).**
