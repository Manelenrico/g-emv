# SPEC — THE PACK, P3b: CALIBRACIÓN DEL FACTOR §2a (afinar en vez de mandar)
**Sellada por Manel 2026-08-31. Sigue a P3 cerrado (`the_pack_peldano3_acta.md` md5 ab60d8e6…).
model.py INTOCABLE (1e511978). Estructura de P3 INTACTA — un solo cambio de calibración.**

## El cambio (único)
Rango del factor de ocupación §2a: de **[0.5, 1.5]** a **[0.8, 1.2]** (descuento 0.8 / neutro 1.0 / prima 1.2).
Implementado HORNEABLE por flag (GEMV_P3_OCC_LO/HI; fórmula generalizada `HI − (HI−LO)/2·occ`), misma imagen.
Todo lo demás IDÉNTICO: vara radio 2, §2b/§2c iguales, mismas 3 semillas (170534803/120290872/176280986),
10.000t, era+censo+pregonero+expectativas.

## Pregunta sellada única
¿Con el factor que AFINA en vez de MANDAR, desaparece la dispersión del núcleo productivo y el score deja de
bajar (o sube) MANTENIENDO la fiabilidad nacida?

## Humo mínimo
1. Flag OFF: bit-exacto contra la vara. 2. Puerta 5: factores ⊆[0.8,1.2], 0 fuera. 3. Una vida corta: el
descuento sigue BIDIRECCIONAL y GEOGRÁFICO con el rango nuevo.

## Examen
N=3, 10.000t, mismas semillas. Paquete con las MISMAS tablas que P3 (fiabilidad por emisor y por slot, factores
agregados, duplicación de destinos, comparación apareada score/economía/muertes vs P2 Y vs P3). SIN lectura.

## Predicciones (formato simple, antes de encender)
- **Claude-mesa:** la fiabilidad se mantiene (no depende del factor); el score vuelve a nivel de P2 o levemente
  arriba en 2/3; la duplicación evitada baja pero no desaparece. Si se cumple, la lección es que contar-con-el-
  otro paga como AFINADOR, no como reasignador.
- **Manel:** [se añade cuando la dicte]
- **El vigilante (sellada 2026-08-31, antes de tocar código):**
  - **Fiabilidad: se MANTIENE** (observe-only, no depende del factor) — nace igual, ranking slot-estable igual.
    Alta confianza.
  - **Score: recupera hacia P2 en ≥2/3, NO claramente por encima.** El scatter venía del descuento 0.5 (−50%);
    con 0.8 (−20%, 2.5× más suave) la fuerza que saca del núcleo casi desaparece → el score sube hacia P2.
    Pero machina amable no tiene headroom para SUPERAR a P2 — espero flat-a-P2, no mejor.
  - **Riesgo/matiz distintivo: el factor suave puede volverse un SUSURRO casi inerte.** [0.8,1.2] es tan gentil
    que el delta vs P2 podría encogerse hacia cero → "afinador no reasignador" quedaría confirmado, pero al
    precio de que el mecanismo apenas actúa. La duplicación-evitada (eventos de descuento) seguirá igual de
    frecuente en el LOG (§2a dispara con el mismo patrón geográfico), pero su efecto CONDUCTUAL se diluye. La
    paga real de un factor vivo-pero-suave se vería en P5 (adversario), no aquí.

---
**Estado: SELLADA (Manel + Claude-mesa + vigilante). Humo mínimo → examen N=3 tras venia. model.py 1e511978.**
