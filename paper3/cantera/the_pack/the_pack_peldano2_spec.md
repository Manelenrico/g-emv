# SPEC — THE PACK, PELDAÑO 2: EL CORRESPONSAL (el pregonero firmado)
**Sellada en mesa 2026-08-29 (P-16). Archivada por el vigilante. Terreno certificado en
`the_pack_peldano2_hechos_canal.md` (md5 472ec68ddc…). model.py INTOCABLE (1e511978).**

## Pregunta única
¿Nace la columna de fiabilidad? El cotejo NATURAL de la vida (sin buscar cotejos a propósito), ¿produce
suficientes casos para que la fiabilidad POR EMISOR sea un número y no anécdota? Sub-pregunta del censo:
¿los anuncios firmados hacen legibles a los periféricos (la niebla antes-vs-después)?

## Terreno certificado
El pregonero es tablón propio (fichero compartido), no el canal del motor. El emisor YA viaja (`slot`) y el
consumidor lo ignora: firma inerte. Formato nuestro, ampliable, sin cooldown. Se hace load-bearing sin tocar
motor ni formato.

## Qué se construye (mínimo firmado por Manel)
1. El consumidor LEE el `slot` y VERIFICA firma-contra-fichero (cierra la falsificabilidad del mount).
2. Cada anuncio consumido se apunta en la fila del EMISOR del censo: "ag3 anunció <clase> en <pos>, tick T".
   El censo gana OÍDOS.
3. Columna FIABILIDAD por emisor: cuando el ojo propio llega después al lugar anunciado, coteja. Razón:
   aciertos / cotejos válidos.
4. JUSTICIA TEMPORAL (Manel, 29-ago): el cotejo pesa por la EDAD del anuncio al cotejar. Bajo umbral
   (flag horneable): cuenta entero. Sobre umbral: NO atribuible al emisor (aparte; el fallo es del tiempo).
NO se amplía lo anunciable. NO se toca la decisión: observe-only estricto (la fiabilidad se apunta, no se
usa — usarla = P3). Regresión bit-exacta obligada.

## Punto cero declarado
Todos veraces (primera mano + anti-eco): se espera fiabilidad alta y pareja. NO es examen fallido: es la VARA
del corresponsal honesto, contra la que se medirá la divergencia con rivales/ruido/engaño.

## El examen
N=3, 10.000t, era ON, censo limpio + corresponsal. MISMAS 3 semillas de P1 (niebla antes-vs-después
apareada). Volcados: censo completo (+ columnas nuevas: anuncios-por-emisor, fiabilidad, cotejos
válidos/no-atribuibles) + matriz de cobertura EFECTIVA (ojo+oídos) vs la de solo-ojo de P1.

## Lectura (criterio simple)
- NACE: mediana de cotejos válidos por par emisor-receptor con denominador ≥ un puñado (no anécdota), y la
  cobertura efectiva de los pares en niebla (los <15% de P1) sube claramente.
- NO NACE: cotejos anecdóticos o niebla igual → la fiabilidad necesitaría diseño activo (decisión de mesa).

## Predicciones (§7)
**El vigilante (sellada 2026-08-29, antes de tocar código):**
- (i) **¿Nace? SÍ (~80%).** Cotejos válidos DE SOBRA para los pares del racimo del hub (denominador grande:
  el ojo pasa mucho por la plaza); FINOS para los pares periféricos-COMO-cotejados (rara vez mi ojo llega a
  su territorio a tiempo). La columna es un NÚMERO en agregado, no anécdota; pero desigual por par.
- (ii) **Legibilidad periféricos: asimétrica.** La niebla de OÍDOS casi desaparece — el tablón es BROADCAST
  (todos leen a todos) ⇒ los emisores periféricos pasan de <15% (P1, solo-ojo) a **~near-full como
  emisores-oídos**. Pero como COTEJADOS sube poco (denominador fino). Predigo: cobertura efectiva de los
  pares-niebla ≈ 90-100% en la dimensión EMISOR, aún fina en la dimensión COTEJO.
- (iii) **Alta pero NO perfectamente pareja — y la sorpresa la pone el MUNDO, no el mentiroso.** Honestidad
  universal ⇒ fiabilidad alta, PERO el mundo es dinámico: las JUNCTIONS cambian de dueño entre anuncio y
  cotejo (gray→nuestra/rival por conquista) → "fallos" que son del TIEMPO, no del emisor. Predigo
  **extractores ~100%** (estáticos) y **junctions más bajas** (flips DENTRO del umbral). La justicia temporal
  mitiga la staleness pero no los flips intra-umbral. La vara del honesto no será un 100% liso: su techo lo
  fija la dinámica de las junctions.

**Claude-mesa (sellada 2026-08-29):** (i) nace 70%, con duda en los cotejos de lo lejano; (ii) periféricos
legibles como EMISORES (niebla de oídos casi fuera), poco como cotejados; (iii) alta y pareja, con los
periféricos como corresponsales MÁS valiosos.
**Manel:** (se añade cuando la dicte).

---
**Estado: SELLADA (vigilante + mesa; Manel pendiente). Implementación mínima observe-only + humo (regresión
bit-exacta + enchufe de columnas + cotejo verificado a mano) → examen N=3 mismas semillas de P1, tras §7
completo y venia. SIN LECTURA (de la mesa).**
