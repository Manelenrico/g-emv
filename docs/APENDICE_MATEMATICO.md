# Apéndice Matemático — Modelo G-EMV

> Todos los valores numéricos de este apéndice están extraídos directamente del código fuente (`model.py`, `experiments_dinamica_tension_inmediato.py`, `experiments_decentramiento.py`, `robustez_experimentos.py`, `robustez_exp_CD.py`). Los números son los valores literales del código, no aproximaciones.

---

## 1. Estado y magnitudes derivadas

### Estado interno

El estado del agente es un vector de **seis variables reales independientes**, todas no negativas:

$$\mathbf{x} = (f^+_F,\; f^-_F,\; f^+_R,\; f^-_R,\; f^+_S,\; f^-_S) \in \mathbb{R}^6_{\geq 0}$$

Implementación: clase `State` en `model.py`, campos `pF, nF, pR, nR, pS, nS`. Son las **primitivas** del sistema — almacenadas directamente como floats independientes.

### Magnitudes derivadas (propiedades calculadas)

**Posición** y **tensión** son derivadas de las fuerzas primarias mediante `@property`:

$$\text{pos}_a = f^+_a - f^-_a \qquad \text{ten}_a = f^+_a + f^-_a \qquad a \in \{F,\, R,\, S\}$$

> **Invariante clave (v2):** Dos estados pueden tener la misma posición y distinta tensión. Ejemplo: `State(pF=1.0, nF=1.0)` y `State(pF=3.8, nF=3.8)` tienen ambos `pos_F = 0`, pero `ten_F = 2.0` y `ten_F = 7.6` respectivamente. Esto es imposible en la representación v1 donde `pF·nF = 0`.

---

## 2. Regla de evolución dinámica

La dinámica es **descenso de gradiente de $d^2$** (no de $d$). Las seis fuerzas se actualizan simultáneamente.

### Gradientes exactos

Para el eje $F$ (y análogos para $R$, $S$ permutando índices):

$$G^+_F = \frac{\partial d^2}{\partial f^+_F} = 2(w^{\text{pos}}_F + W_F)\,\Delta\text{pos}_F + 2w^{\text{ten}}_F\,\Delta\text{ten}_F + C_F$$

$$G^-_F = \frac{\partial d^2}{\partial f^-_F} = -2(w^{\text{pos}}_F + W_F)\,\Delta\text{pos}_F + 2w^{\text{ten}}_F\,\Delta\text{ten}_F + C_F$$

Términos auxiliares:

$$\Delta\text{pos}_a = \text{pos}_a - \hat{p}_a \qquad \Delta\text{ten}_a = \text{ten}_a - \hat{t}_a$$

$$W_F = \sigma_R\,\text{ten}_R + \sigma_S\,\text{ten}_S \qquad W_R = \sigma_F\,\text{ten}_F + \sigma_S\,\text{ten}_S \qquad W_S = \sigma_F\,\text{ten}_F + \sigma_R\,\text{ten}_R$$

$$C_F = \sigma_F\,(\Delta\text{pos}_R^2 + \Delta\text{pos}_S^2) \qquad C_R = \sigma_R\,(\Delta\text{pos}_F^2 + \Delta\text{pos}_S^2) \qquad C_S = \sigma_S\,(\Delta\text{pos}_F^2 + \Delta\text{pos}_R^2)$$

### Regla de actualización

$$f^+_a(t+1) = \max\!\left(0,\; f^+_a(t) - \eta\, G^+_a\right)$$

$$f^-_a(t+1) = \max\!\left(0,\; f^-_a(t) - \eta\, G^-_a\right)$$

Tras la actualización se aplica `State.__post_init__` (basal mínimo + techo VOL\_MAX; véase §6).

### Parámetros de la dinámica

| Parámetro | Símbolo | Valor exacto | Fuente |
|---|---|---|---|
| Learning rate | $\eta$ | **0.05** | `ETA` en todos los archivos dinámicos |
| Pasos post-estímulo | $N_{\text{post}}$ | **80** | `N_POST` |
| Magnitud del estímulo (nominal) | $\delta$ | **1.5** | `DELTA` |
| Pasos de reposo pre-estímulo | $N_{\text{reposo}}$ | **0** (variante inmediata) | `N_REPOSO=0` |

> **Estabilidad numérica:** $\eta_{\max} \approx 1/H_{\max} \approx 0.167$ (peor caso eje R con acoplamiento máximo). El valor usado $\eta = 0.05$ opera al **30 %** del límite de estabilidad.

---

## 3. Calibraciones exactas

### Objetivos de posición (descentramiento basal)

| Parámetro | Símbolo | Valor |
|---|---|---|
| `f_pos_target` | $\hat{p}_F$ | **1.0** |
| `r_pos_target` | $\hat{p}_R$ | **2.0** |
| `s_pos_target` | $\hat{p}_S$ | **0.8** |

### Objetivos de tensión (arousal óptimo)

| Parámetro | Símbolo | Valor |
|---|---|---|
| `f_ten_target` | $\hat{t}_F$ | **0.30** |
| `r_ten_target` | $\hat{t}_R$ | **0.30** |
| `s_ten_target` | $\hat{t}_S$ | **0.15** |

### Pesos de posición y tensión por eje

| Eje | Peso posición $w^{\text{pos}}_a$ | Peso tensión $w^{\text{ten}}_a$ |
|---|---|---|
| F (fuerza vital) | **1.0** | **0.40** |
| R (relaciones) | **1.0** | **0.40** |
| S (sentido) | **0.70** | **0.25** |

### Sensibilidades de acoplamiento

| Parámetro | Símbolo | Valor |
|---|---|---|
| `sens_F` | $\sigma_F$ | **0.30** |
| `sens_R` | $\sigma_R$ | **0.15** |
| `sens_S` | $\sigma_S$ | **0.10** |

### Límites de volumen

| Parámetro | Valor |
|---|---|
| `TEN_BASAL_MIN` | **0.10** |
| `VOL_MAX` | **8.0** |
| Presupuesto disponible sobre basal (= $\text{VOL\_MAX} - 3 \times \text{TEN\_BASAL\_MIN}$) | **7.70** |

### Constantes de dominio (shim de observables)

| Constante | Valor | Rol |
|---|---|---|
| `HP_EQ` | 75.0 | Punto de equilibrio de HP |
| `HP_SCALE` | 25.0 | Escala de normalización HP |
| `HP_CAP` | 100.0 | Máximo HP |
| `ENERGY_EQ` | 10.0 | Punto de equilibrio de energía |
| `ENERGY_SCALE` | 5.0 | Escala de normalización energía |
| `ENERGY_CAP` | 20.0 | Máximo energía |
| `S_MAX` | 2.0 | Rango máximo del campo social |

---

## 4. Acoplamiento

Fórmula exacta del término de acoplamiento implementada en `opponent_distance()` (`model.py`):

$$\text{coupling} = \sigma_F\,\text{ten}_F\,(\Delta\text{pos}_R^2 + \Delta\text{pos}_S^2) + \sigma_R\,\text{ten}_R\,(\Delta\text{pos}_F^2 + \Delta\text{pos}_S^2) + \sigma_S\,\text{ten}_S\,(\Delta\text{pos}_F^2 + \Delta\text{pos}_R^2)$$

con $\Delta\text{pos}_a = \text{pos}_a - \hat{p}_a$.

**Propiedades:**

- **Bidireccional:** cada eje arrastra a los otros dos.
- **Usa $\text{ten}_a = f^+_a + f^-_a$:** oportunidad y amenaza arrastran por igual; la dirección es irrelevante para el acoplamiento.
- **Acoplamiento nulo sin déficit posicional:** si $\Delta\text{pos}_a = 0$ para todos los ejes, coupling = 0 independientemente de la tensión.

---

## 5. Distancia homeostática

Fórmula exacta en `opponent_distance()` (`model.py`):

$$d = \sqrt{d_{\text{pos}} + d_{\text{ten}} + \text{coupling}}$$

con:

$$d_{\text{pos}} = w^{\text{pos}}_F\,\Delta\text{pos}_F^2 + w^{\text{pos}}_R\,\Delta\text{pos}_R^2 + w^{\text{pos}}_S\,\Delta\text{pos}_S^2$$

$$d_{\text{ten}} = w^{\text{ten}}_F\,\Delta\text{ten}_F^2 + w^{\text{ten}}_R\,\Delta\text{ten}_R^2 + w^{\text{ten}}_S\,\Delta\text{ten}_S^2$$

> La dinámica minimiza $d^2$ (no $d$). Los gradientes del §2 son exactamente los gradientes de $d^2$.

---

## 6. Recorte: techo y suelo

Implementado en `State.__post_init__()` (`model.py`). Dos pasos en orden fijo, aplicados tras cada actualización de estado.

### Paso 1 — Suelo TEN\_BASAL\_MIN (eje por eje)

```
para cada eje a ∈ {F, R, S}:
    ten_a = f⁺_a + f⁻_a
    si ten_a < TEN_BASAL_MIN:
        add = (TEN_BASAL_MIN − ten_a) / 2
        f⁺_a ← f⁺_a + add
        f⁻_a ← f⁻_a + add
```

Preserva $\text{pos}_a$ exactamente (el incremento `add` se suma a ambas fuerzas, se cancela en la resta).

### Paso 2 — Techo VOL\_MAX (escala el excedente, preserva el basal)

```
total = ten_F + ten_R + ten_S
si total > VOL_MAX:
    allowed_surplus = VOL_MAX − 3·TEN_BASAL_MIN    # = 7.70
    exc_a = ten_a − TEN_BASAL_MIN   (para cada eje)
    exc_total = exc_F + exc_R + exc_S
    si exc_total > 0:
        scale = allowed_surplus / exc_total
        para cada eje a con exc_a > 0:
            new_ten_a = TEN_BASAL_MIN + exc_a · scale
            r = new_ten_a / ten_a
            f⁺_a ← f⁺_a · r
            f⁻_a ← f⁻_a · r
```

**Propiedades:**

- Los ejes con `exc_a = 0` (exactamente en el mínimo basal) no se modifican.
- La razón $f^+_a / f^-_a$ dentro de cada eje se conserva: la posición $\text{pos}_a$ escala proporcionalmente.
- **Ejemplo concreto (estado TENSO + estímulo OPO, $\delta = 1.5$):** ten\_F\_req = 9.1, exc\_F = 9.0, scale = 7.70/9.0 = 0.8556, new\_ten\_F = 7.80, pos\_F\_resultante = 1.286 (en lugar del 1.5 solicitado). El estímulo queda parcialmente absorbido.

---

## 7. Montaje experimental

### Experimentos A y B — Ceguera a la oportunidad y Yerkes-Dodson

Archivos: `experiments_dinamica_tension_inmediato.py`, `robustez_experimentos.py`

| Parámetro | Valor |
|---|---|
| $\eta$ | 0.05 |
| $\delta$ (estímulo) | 1.5 (nominal) |
| $N_{\text{post}}$ | 80 pasos |
| $N_{\text{reposo}}$ | 0 |
| Semillas (Test 1 robustez) | 100 perturbaciones gaussianas independientes |
| Ruido sobre fuerzas F | $\sigma_F = 0.05$ (absoluto) |
| Ruido sobre fuerzas R, S | $\sigma_{RS} = 0.01$ (absoluto) |
| Generador | `numpy.random.default_rng(0)` |
| Estado CALMA | `State(pF=1.0, nF=1.0, pR=0.05, nR=0.05, pS=0.05, nS=0.05)` |
| Estado TENSO | `State(pF=3.8, nF=3.8, pR=0.05, nR=0.05, pS=0.05, nS=0.05)` |
| Estímulo OPORTUNIDAD | `pF += δ` (las demás fuerzas inalteradas) |
| Estímulo PELIGRO | `nF += δ` (las demás fuerzas inalteradas) |
| Niveles barridos (Exp B) | 2.0, 4.0, 6.0, 7.0, 7.5, 7.9 |
| VOL\_MAX ablación (Test 2) | 100.0 (efectivamente sin techo) |
| Rango calibración VOL\_MAX (Test 3) | [7.0, 10.0] |
| Rango calibración $\delta$ (Test 3) | [0.25, 2.5] |
| Rango calibración $\sigma_F$ (Test 3) | [0.15, 0.40] |

### Experimento C — Tipología social

Archivo: `experiments_decentramiento.py`, `robustez_exp_CD.py`

| Parámetro | Valor |
|---|---|
| Grid | 20 × 20 |
| Pasos por episodio | 300 |
| Posición del estímulo social | centro (fila 10, columna 10) |
| Campo social | $s(r,c) = 1.5 \cdot \exp\!\left(-d_{\text{Eucl}} / 4.0\right)$ |
| HP fijo durante el episodio | 90.0 |
| Energía fija durante el episodio | 15.0 |
| Acoplamiento | desactivado ($\sigma_F = \sigma_R = \sigma_S = 0$) para los tres fenotipos |
| Umbral de proximidad (`PROX_THRESH`) | 3.0 celdas |
| Semillas Test 1 (robustez) | 100 posiciones iniciales aleatorias |

**Configuraciones de los tres fenotipos:**

| Fenotipo | `s_pos_target` | `w_s_pos` | `sens` |
|---|---|---|---|
| Positivo (busca vínculo) | **+1.0** | **0.8** | 0.0 |
| Neutro (indiferente) | **0.0** | **0.0** | 0.0 |
| Negativo (evita) | **−1.0** | **0.8** | 0.0 |

> **Nota:** `s_pos_target = 0` con `w_s_pos = 0` produce indiferencia real (s no entra en d). `s_pos_target = 0` con `w_s_pos > 0` produce evitación porque el campo social con $s > 0$ se desvía del objetivo cero.

**Verificación VOL\_MAX:** tensión máxima observada ≈ 3.1 ≪ VOL\_MAX = 8.0. El techo nunca se activa en este experimento.

### Experimento D — Descentramiento como motor

Archivo: `experiments_decentramiento.py`, `robustez_exp_CD.py`

| Parámetro | Valor |
|---|---|
| Grid | 10 × 10 |
| Pasos por episodio | 500 |
| Posición inicial | centro (5, 5) |
| HP inicial | 75.0 (= `HP_EQ`) |
| Energía inicial | 10.0 (= `ENERGY_EQ`) |
| `HP_DECAY` (coste metabólico por paso) | **0.10** |
| `ENERGY_DECAY` (coste metabólico por paso) | **0.05** |
| `MOVE_SCALE` | **3.0** (distancia donde prob(moverse) = 1.0) |
| Probabilidad de movimiento | $\min(1,\; d / 3.0)$ |
| Ventana "actividad temprana" | primeros **100** pasos |
| Semillas Test 1 (robustez) | 100 semillas estocásticas |

**Configuraciones de los tres fenotipos:**

| Fenotipo | `f_pos_target` | `r_pos_target` | `s_pos_target` | `sens` |
|---|---|---|---|---|
| Centrado (reactivo) | 0.0 | 0.0 | 0.0 | 0.0 |
| Positivo (proactivo) | **1.0** (default) | **2.0** (default) | **0.8** (default) | default |
| Negativo (colapsa) | **−1.0** | **−2.0** | **−0.8** | 0.0 |

**Verificación VOL\_MAX:** tensión máxima observada ≈ 4.1 ≪ VOL\_MAX = 8.0. El techo nunca se activa en este experimento.

---

## 8. Nota sobre el shim v1

### Experimentos que usan `State(pF, nF, ...)` directamente — API v2 (fuerzas independientes)

- `experiments_dinamica_tension.py`
- `experiments_dinamica_tension_inmediato.py`
- `experimentos_niveles_tension.py`
- `experimentos_riqueza_orientacion.py`
- `robustez_experimentos.py`

En estos experimentos $f^+_a \cdot f^-_a > 0$ en todo momento (ambas fuerzas activas), lo que es la firma de la independencia v2. Los fenómenos de ceguera a la oportunidad y Yerkes-Dodson dependen de esta independencia.

### Experimentos que usan `state_from_observables(hp, energy, s)` — shim v1

- `experiments.py` (Exp 1, 2, 3 — fenotipos, aburrimiento, acoplamiento v1)
- `experiments_decentramiento.py` (Exp A descentramiento, Exp B tipología social)
- `robustez_exp_CD.py` (Exp C tipología, Exp D descentramiento — vía `d_obs`)

El shim implementa:

$$f^+_F = \max\!\left(0,\; \frac{hp - \text{HP\_EQ}}{\text{HP\_SCALE}}\right), \qquad f^-_F = \max\!\left(0,\; \frac{\text{HP\_EQ} - hp}{\text{HP\_SCALE}}\right)$$

y análogo para $R$ (energía) y $S$. Esto fuerza $f^+_a \cdot f^-_a = 0$ para todo eje, de modo que $\text{ten}_a = |\text{pos}_a|$ (regresión al comportamiento v1).

**Por qué es admisible:** los experimentos C y D no requieren la separabilidad posición/tensión — sus fenómenos (tipología social, descentramiento como motor) dependen de `s_pos_target` y `f/r/s_pos_target` respectivamente. El shim es correcto para el propósito de esos experimentos. Los experimentos que requieren la independencia v2 (A y B) usan exclusivamente la API de Estado directo.

**Commit de introducción de v2:** `434f123`. Todos los experimentos de ceguera y Yerkes-Dodson fueron comprometidos después de ese commit.
