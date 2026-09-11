# ACTA — THE PACK, P3b: CALIBRACIÓN DEL FACTOR §2a (cierre)
**Sellada por la mesa 2026-09-01. Spec: `the_pack_peldano3b_spec.md` (md5 21e2982c…). Paquete:
`the_pack_peldano3b_paquete.md` (md5 3d6922f5…). model.py INTOCABLE (1e511978, sellos inicio/fin verdes).**

## El cambio (único, horneable)
Rango del factor de ocupación §2a de [0.5,1.5] → **[0.8,1.2]** (descuento 0.8/neutro 1.0/prima 1.2). Flag
`GEMV_P3_OCC_LO/HI`, fórmula generalizada `HI−(HI−LO)/2·occ` (default 0.5/1.5 reproduce P3 bit-exacto).
Estructura de P3 INTACTA. Humo mínimo verde: OFF bit-exact (3200/3200), puerta 5 (⊆[0.8,1.2], 0 fuera),
bidireccional (0.8/1.0/1.2 presentes).

## Pregunta sellada
¿El factor que AFINA en vez de MANDAR quita la dispersión del núcleo y frena la caída del score, manteniendo
la fiabilidad nacida?

## VEREDICTO SELLADO: SÍ
- **El scatter se frena:** score P3→P3b sube en **3/3** (0.348→0.643, 0.306→0.379, 0.999→1.505).
- **La fiabilidad se mantiene:** ~100 cotejos/emisor (106/103.5/102.5 ≫10), no degenerada, **ranking
  slot-estable IDÉNTICO** a P3 (ag1/ag3/ag4/ag6 altos; ag0/ag2/ag5/ag7 bajos). El factor no la toca (observe-only).
- **En el mundo con holgura el afinador PAGA:** seed 176280986 **+50% vs P2** (0.999→1.505); en los densos,
  cerca de P2 por debajo (0.643 vs 0.801; 0.379 vs 0.442). **0 muertes** en todas.
- **§2a se desplazó hacia PRIMA** (seed1: 76%descuento P3 → 12%descuento/85%prima P3b): el factor gentil no
  fuerza la reasignación agresiva → menos duplicación-evitada, menos scatter.

## LECCIÓN SELLADA
**Contar-con-el-otro paga como AFINADOR, no como reasignador.** El **[0.8,1.2] queda como calibración de
referencia para P4** (el importar).

## CAREO §7 (con nombres)
- **Manel:** acertó la dirección (recuperación); la SUPERACIÓN de P2 salió solo en 1/3 (predijo más).
- **Claude-mesa:** CLAVADO ("vuelve a P2 o levemente arriba"; 1/3 arriba, 2/3 cerca; fiabilidad intacta;
  duplicación-evitada baja pero no desaparece).
- **El vigilante:** mejor en fiabilidad (se mantiene, slot-estable); **refutado en su riesgo estrella** ("susurro
  casi inerte" — NO fue inerte: el score se movió fuerte y seed3 superó P2 +50%); y en "no claramente por
  encima" (seed3 lo refuta).

**Estado: P3b CERRADO. El factor suavizado [0.8,1.2] es la calibración de referencia. model.py 1e511978
intacto. Próximo: P4 (el importar) cuando la mesa lo abra.**
