# PAQUETE — THE PACK peldaño 1 (el censo). SIN VEREDICTO.

3 vidas × 8 observadores = 24 censos (último dump ~t9000). Verificación externa vs replay, cobertura, consistencia. La lectura (distinguible/ruido) y el careo §7 son de la mesa.

## VIDA seed 170534803 (censo a t9000; conducta real del replay a t9000)

### (A) Verificación externa — REAL (replay, verdad) vs CENSO-consenso (censo LIMPIO, fix de fidelidad)
Todas las columnas del censo ya fiables (misatribución por agent_id-truncado corregida). CENSO heart_max
casa exacto con REAL; carga/oficio-depósito ahora comparables con el minado/depósito real.
| ag | REAL minado | REAL depós | REAL heart_max | REAL quieto% | CENSO cargo_max | CENSO ofi_dep | CENSO ofi_min | CENSO heart_max | CENSO radio | #obs |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 67 | 67 | 2 | 72.5 | 10.0 | 3.83 | 0.0 | 2.0 | 3.98 | 8 |
| 1 | 12 | 12 | 1 | 77.2 | 4.0 | 4.42 | 0.0 | 1.0 | 4.45 | 8 |
| 2 | 44 | 40 | 1 | 11.6 | 20.0 | 6.54 | 0.0 | 1.0 | 5.37 | 8 |
| 3 | 5 | 5 | 2 | 50.6 | 2.0 | 3.42 | 0.0 | 2.0 | 6.01 | 8 |
| 4 | 39 | 35 | 1 | 61.1 | 10.0 | 2.62 | 0.0 | 1.0 | 5.24 | 8 |
| 5 | 35 | 31 | 0 | 38.8 | 10.0 | 7.88 | 0.0 | 0.0 | 4.81 | 8 |
| 6 | 8 | 4 | 1 | 22.8 | 4.0 | 0.0 | 0.0 | 1.0 | 5.46 | 8 |
| 7 | 84 | 84 | 2 | 43.2 | 20.0 | 3.42 | 0.0 | 2.0 | 5.28 | 8 |

### (B) Cobertura observador→observado (% de observaciones con el hermano a la vista; auto-fila=100)
| obs\ado | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| **0** | 100 | 72 | 18 | 12 | 45 | 61 | 10 | 35 |
| **1** | 72 | 100 | 17 | 11 | 47 | 43 | 15 | 35 |
| **2** | 18 | 17 | 100 | 21 | 11 | 20 | 2 | 50 |
| **3** | 12 | 11 | 21 | 100 | 1 | 11 | 2 | 32 |
| **4** | 45 | 47 | 11 | 1 | 100 | 80 | 47 | 4 |
| **5** | 61 | 43 | 20 | 11 | 80 | 100 | 29 | 17 |
| **6** | 10 | 15 | 2 | 2 | 47 | 29 | 100 | 1 |
| **7** | 35 | 35 | 50 | 32 | 4 | 17 | 1 | 100 |

### (C) Consistencia entre observadores — quieto% de cada hermano (min–max entre observadores)
| observado | quieto% por obs (min–max) | radio (min–max) |
|---|---|---|
| 0 | 26.7–80.3 (8 obs) | 2.76–5.16 |
| 1 | 63.2–88.9 (8 obs) | 3.10–5.29 |
| 2 | 11.6–50.2 (8 obs) | 3.95–9.39 |
| 3 | 14.9–56.2 (8 obs) | 2.33–9.92 |
| 4 | 23.7–82.4 (8 obs) | 3.85–6.73 |
| 5 | 17.5–43.7 (8 obs) | 4.26–7.50 |
| 6 | 10.8–68.0 (8 obs) | 3.64–10.43 |
| 7 | 17.9–82.5 (8 obs) | 2.79–9.05 |

## VIDA seed 120290872 (censo a t9000; conducta real del replay a t9000)

### (A) Verificación externa — REAL (replay, verdad) vs CENSO-consenso (censo LIMPIO, fix de fidelidad)
Todas las columnas del censo ya fiables (misatribución por agent_id-truncado corregida). CENSO heart_max
casa exacto con REAL; carga/oficio-depósito ahora comparables con el minado/depósito real.
| ag | REAL minado | REAL depós | REAL heart_max | REAL quieto% | CENSO cargo_max | CENSO ofi_dep | CENSO ofi_min | CENSO heart_max | CENSO radio | #obs |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 10 | 10 | 2 | 43.6 | 4.0 | 2.58 | 0.0 | 2.0 | 8.49 | 8 |
| 1 | 15 | 13 | 0 | 69.9 | 4.0 | 6.5 | 0.0 | 0.0 | 7.5 | 8 |
| 2 | 41 | 37 | 0 | 71.4 | 10.0 | 6.67 | 0.0 | 0.0 | 8.55 | 8 |
| 3 | 10 | 6 | 1 | 22.6 | 4.0 | 3.75 | 0.0 | 1.0 | 9.94 | 8 |
| 4 | 10 | 6 | 1 | 12.8 | 4.0 | 3.92 | 0.0 | 1.0 | 8.41 | 8 |
| 5 | 97 | 57 | 0 | 29.4 | 40.0 | 5.5 | 0.0 | 0.0 | 11.23 | 8 |
| 6 | 10 | 6 | 4 | 18.4 | 4.0 | 2.75 | 0.0 | 4.0 | 8.05 | 8 |
| 7 | 15 | 11 | 1 | 29.5 | 4.0 | 3.5 | 0.0 | 1.0 | 10.09 | 8 |

### (B) Cobertura observador→observado (% de observaciones con el hermano a la vista; auto-fila=100)
| obs\ado | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| **0** | 100 | 20 | 14 | 17 | 33 | 32 | 14 | 28 |
| **1** | 20 | 100 | 78 | 33 | 8 | 27 | 22 | 21 |
| **2** | 14 | 78 | 100 | 25 | 8 | 38 | 25 | 40 |
| **3** | 17 | 33 | 25 | 100 | 45 | 56 | 29 | 37 |
| **4** | 33 | 8 | 8 | 45 | 100 | 69 | 7 | 42 |
| **5** | 32 | 27 | 38 | 56 | 69 | 100 | 23 | 67 |
| **6** | 14 | 22 | 25 | 29 | 7 | 23 | 100 | 24 |
| **7** | 28 | 21 | 40 | 37 | 42 | 67 | 24 | 100 |

### (C) Consistencia entre observadores — quieto% de cada hermano (min–max entre observadores)
| observado | quieto% por obs (min–max) | radio (min–max) |
|---|---|---|
| 0 | 33.4–62.8 (8 obs) | 6.10–10.43 |
| 1 | 43.8–77.4 (8 obs) | 5.08–9.83 |
| 2 | 36.6–74.9 (8 obs) | 6.97–10.55 |
| 3 | 20.3–63.5 (8 obs) | 6.74–14.24 |
| 4 | 12.8–47.8 (8 obs) | 5.90–10.20 |
| 5 | 19.4–52.1 (8 obs) | 7.42–13.04 |
| 6 | 18.4–58.0 (8 obs) | 6.68–10.73 |
| 7 | 25.7–57.2 (8 obs) | 7.05–12.58 |

## VIDA seed 176280986 (censo a t9000; conducta real del replay a t9000)

### (A) Verificación externa — REAL (replay, verdad) vs CENSO-consenso (censo LIMPIO, fix de fidelidad)
Todas las columnas del censo ya fiables (misatribución por agent_id-truncado corregida). CENSO heart_max
casa exacto con REAL; carga/oficio-depósito ahora comparables con el minado/depósito real.
| ag | REAL minado | REAL depós | REAL heart_max | REAL quieto% | CENSO cargo_max | CENSO ofi_dep | CENSO ofi_min | CENSO heart_max | CENSO radio | #obs |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 71 | 67 | 2 | 48.3 | 40.0 | 4.54 | 0.0 | 2.0 | 9.86 | 8 |
| 1 | 33 | 29 | 1 | 47.3 | 4.0 | 6.0 | 0.0 | 1.0 | 10.02 | 8 |
| 2 | 31 | 27 | 2 | 57.9 | 10.0 | 9.88 | 0.0 | 2.0 | 8.77 | 8 |
| 3 | 17 | 13 | 2 | 62.9 | 4.0 | 4.96 | 0.0 | 2.0 | 8.18 | 8 |
| 4 | 12 | 11 | 0 | 30.5 | 3.0 | 3.75 | 0.0 | 0.0 | 5.0 | 8 |
| 5 | 35 | 31 | 0 | 54.8 | 4.0 | 6.46 | 0.0 | 0.0 | 9.59 | 8 |
| 6 | 57 | 17 | 1 | 35.4 | 40.0 | 6.33 | 0.0 | 1.0 | 8.01 | 8 |
| 7 | 31 | 31 | 1 | 38.3 | 4.0 | 5.58 | 0.0 | 1.0 | 9.97 | 8 |

### (B) Cobertura observador→observado (% de observaciones con el hermano a la vista; auto-fila=100)
| obs\ado | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| **0** | 100 | 48 | 45 | 22 | 21 | 36 | 38 | 35 |
| **1** | 48 | 100 | 55 | 33 | 16 | 42 | 38 | 31 |
| **2** | 45 | 55 | 100 | 31 | 20 | 42 | 38 | 30 |
| **3** | 22 | 33 | 31 | 100 | 13 | 41 | 32 | 35 |
| **4** | 21 | 16 | 20 | 13 | 100 | 16 | 22 | 21 |
| **5** | 36 | 42 | 42 | 41 | 16 | 100 | 32 | 23 |
| **6** | 38 | 38 | 38 | 32 | 22 | 32 | 100 | 42 |
| **7** | 35 | 31 | 30 | 35 | 21 | 23 | 42 | 100 |

### (C) Consistencia entre observadores — quieto% de cada hermano (min–max entre observadores)
| observado | quieto% por obs (min–max) | radio (min–max) |
|---|---|---|
| 0 | 43.4–74.1 (8 obs) | 6.10–11.52 |
| 1 | 40.7–75.9 (8 obs) | 4.81–11.49 |
| 2 | 44.0–67.8 (8 obs) | 4.43–10.19 |
| 3 | 52.2–75.6 (8 obs) | 4.46–10.57 |
| 4 | 30.5–85.6 (8 obs) | 4.45–7.72 |
| 5 | 42.6–69.2 (8 obs) | 4.64–11.46 |
| 6 | 14.0–67.1 (8 obs) | 3.59–10.47 |
| 7 | 37.3–80.6 (8 obs) | 3.80–11.89 |

**SIN VEREDICTO.** La lectura (¿distinguibles los 8? ¿cuántos casan? ¿cobertura suficiente?) y el careo con las predicciones §7 (vigilante/Manel/mesa) son de la mesa. Los 24 censos crudos: `the_pack_censos_crudos.md`.

## Comparación SUCIO vs LIMPIO (material de método — mismas 3 semillas, conducta idéntica)
El censo es observe-only (regresión bit-exacta): la conducta y el score de la re-corrida limpia son IDÉNTICOS
a los del sucio (mismas semillas). Lo único que cambia es la FIDELIDAD del censo. Root cause único: la obs se
trunca (~500 tokens) y a algunos hermanos se les cae el token `agent_id`; `get_scalar` devolvía 0 por defecto
→ misatribución a ag0. Fix: contar solo equipo-propio con `agent_id` legible.
| métrica (vida 1, seed 170534803) | SUCIO | LIMPIO | verdad (replay) |
|---|---|---|---|
| ag0 cargo_max (consenso) | ~190 (imposible) | 10 | 10 (máx instant.) |
| cobertura obs1→ag0 | 144% (inflada) | 72% | — |
| cobertura obs0→ag0 (self) | 145% | 100% | — |
| ag0 heart_max | 2 | 2 | 2 |
Efecto: carga y oficio pasan de EXCLUIDAS (asterisco) a FIABLES; la cobertura deja de inflar. El asterisco de
la lectura queda LEVANTADO. (Sucio preservado: `the_pack_peldano1_paquete_SUCIO.md` md5 499594218b14…).
