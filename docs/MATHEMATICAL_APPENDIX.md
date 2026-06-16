# Mathematical Appendix — G-EMV Model

> All numerical values in this appendix are taken directly from the source code (`model.py`, `experiments_dinamica_tension_inmediato.py`, `experiments_decentramiento.py`, `robustez_experimentos.py`, `robustez_exp_CD.py`). The numbers are the literal values in the code, not approximations.

---

## 1. State and derived quantities

### Internal state

The agent's state is a vector of **six independent real variables**, all non-negative:

$$\mathbf{x} = (f^+_F,\; f^-_F,\; f^+_R,\; f^-_R,\; f^+_S,\; f^-_S) \in \mathbb{R}^6_{\geq 0}$$

Implementation: class `State` in `model.py`, fields `pF, nF, pR, nR, pS, nS`. These are the **primitive** quantities of the system — stored directly as independent floats.

### Derived quantities (computed properties)

**Position** and **tension** are derived from the primary forces via `@property`:

$$\text{pos}_a = f^+_a - f^-_a \qquad \text{ten}_a = f^+_a + f^-_a \qquad a \in \{F,\, R,\, S\}$$

> **Key invariant (v2):** Two states can have the same position and different tension. Example: `State(pF=1.0, nF=1.0)` and `State(pF=3.8, nF=3.8)` both have `pos_F = 0`, but `ten_F = 2.0` and `ten_F = 7.6` respectively. This is impossible in the v1 representation where `pF·nF = 0`.

---

## 2. Dynamical update rule

The dynamics are **gradient descent on $d^2$** (not on $d$). The six forces are updated simultaneously.

### Exact gradients

For axis $F$ (and analogously for $R$, $S$ by permuting indices):

$$G^+_F = \frac{\partial d^2}{\partial f^+_F} = 2(w^{\text{pos}}_F + W_F)\,\Delta\text{pos}_F + 2w^{\text{ten}}_F\,\Delta\text{ten}_F + C_F$$

$$G^-_F = \frac{\partial d^2}{\partial f^-_F} = -2(w^{\text{pos}}_F + W_F)\,\Delta\text{pos}_F + 2w^{\text{ten}}_F\,\Delta\text{ten}_F + C_F$$

Auxiliary terms:

$$\Delta\text{pos}_a = \text{pos}_a - \hat{p}_a \qquad \Delta\text{ten}_a = \text{ten}_a - \hat{t}_a$$

$$W_F = \sigma_R\,\text{ten}_R + \sigma_S\,\text{ten}_S \qquad W_R = \sigma_F\,\text{ten}_F + \sigma_S\,\text{ten}_S \qquad W_S = \sigma_F\,\text{ten}_F + \sigma_R\,\text{ten}_R$$

$$C_F = \sigma_F\,(\Delta\text{pos}_R^2 + \Delta\text{pos}_S^2) \qquad C_R = \sigma_R\,(\Delta\text{pos}_F^2 + \Delta\text{pos}_S^2) \qquad C_S = \sigma_S\,(\Delta\text{pos}_F^2 + \Delta\text{pos}_R^2)$$

### Update rule

$$f^+_a(t+1) = \max\!\left(0,\; f^+_a(t) - \eta\, G^+_a\right)$$

$$f^-_a(t+1) = \max\!\left(0,\; f^-_a(t) - \eta\, G^-_a\right)$$

After the update, `State.__post_init__` applies the tension floor and volume ceiling (see §6).

### Dynamical parameters

| Parameter | Symbol | Exact value | Source |
|---|---|---|---|
| Learning rate | $\eta$ | **0.05** | `ETA` in all dynamical files |
| Post-stimulus steps | $N_{\text{post}}$ | **80** | `N_POST` |
| Nominal stimulus magnitude | $\delta$ | **1.5** | `DELTA` |
| Pre-stimulus rest steps | $N_{\text{rest}}$ | **0** (immediate variant) | `N_REPOSO=0` |

> **Numerical stability:** $\eta_{\max} \approx 1/H_{\max} \approx 0.167$ (worst case, R axis with maximum coupling). The value used, $\eta = 0.05$, operates at **30%** of the stability limit.

---

## 3. Exact calibrations

### Position targets (baseline decentering)

| Parameter | Symbol | Value |
|---|---|---|
| `f_pos_target` | $\hat{p}_F$ | **1.0** |
| `r_pos_target` | $\hat{p}_R$ | **2.0** |
| `s_pos_target` | $\hat{p}_S$ | **0.8** |

### Tension targets (optimal arousal)

| Parameter | Symbol | Value |
|---|---|---|
| `f_ten_target` | $\hat{t}_F$ | **0.30** |
| `r_ten_target` | $\hat{t}_R$ | **0.30** |
| `s_ten_target` | $\hat{t}_S$ | **0.15** |

### Position and tension weights per axis

| Axis | Position weight $w^{\text{pos}}_a$ | Tension weight $w^{\text{ten}}_a$ |
|---|---|---|
| F (physical/bodily) | **1.0** | **0.40** |
| R (resources/material) | **1.0** | **0.40** |
| S (social/relational) | **0.70** | **0.25** |

### Coupling sensitivities

| Parameter | Symbol | Value |
|---|---|---|
| `sens_F` | $\sigma_F$ | **0.30** |
| `sens_R` | $\sigma_R$ | **0.15** |
| `sens_S` | $\sigma_S$ | **0.10** |

### Volume limits

| Parameter | Value |
|---|---|
| `TEN_BASAL_MIN` | **0.10** |
| `VOL_MAX` | **8.0** |
| Available surplus above floor (= $\text{VOL\_MAX} - 3 \times \text{TEN\_BASAL\_MIN}$) | **7.70** |

### Domain constants (observables shim)

| Constant | Value | Role |
|---|---|---|
| `HP_EQ` | 75.0 | HP equilibrium point |
| `HP_SCALE` | 25.0 | HP normalisation scale |
| `HP_CAP` | 100.0 | Maximum HP |
| `ENERGY_EQ` | 10.0 | Energy equilibrium point |
| `ENERGY_SCALE` | 5.0 | Energy normalisation scale |
| `ENERGY_CAP` | 20.0 | Maximum energy |
| `S_MAX` | 2.0 | Maximum range of the social field |

---

## 4. Coupling

Exact coupling term implemented in `opponent_distance()` (`model.py`):

$$\text{coupling} = \sigma_F\,\text{ten}_F\,(\Delta\text{pos}_R^2 + \Delta\text{pos}_S^2) + \sigma_R\,\text{ten}_R\,(\Delta\text{pos}_F^2 + \Delta\text{pos}_S^2) + \sigma_S\,\text{ten}_S\,(\Delta\text{pos}_F^2 + \Delta\text{pos}_R^2)$$

where $\Delta\text{pos}_a = \text{pos}_a - \hat{p}_a$.

**Properties:**

- **Bidirectional:** each axis pulls the other two.
- **Uses $\text{ten}_a = f^+_a + f^-_a$:** approach and avoidance forces couple equally; direction is irrelevant for coupling.
- **Zero coupling with no positional deficit:** if $\Delta\text{pos}_a = 0$ for all axes, coupling = 0 regardless of tension.

---

## 5. Homeostatic distance

Exact formula in `opponent_distance()` (`model.py`):

$$d = \sqrt{d_{\text{pos}} + d_{\text{ten}} + \text{coupling}}$$

with:

$$d_{\text{pos}} = w^{\text{pos}}_F\,\Delta\text{pos}_F^2 + w^{\text{pos}}_R\,\Delta\text{pos}_R^2 + w^{\text{pos}}_S\,\Delta\text{pos}_S^2$$

$$d_{\text{ten}} = w^{\text{ten}}_F\,\Delta\text{ten}_F^2 + w^{\text{ten}}_R\,\Delta\text{ten}_R^2 + w^{\text{ten}}_S\,\Delta\text{ten}_S^2$$

> The dynamics minimise $d^2$ (not $d$). The gradients in §2 are exactly the gradients of $d^2$.

---

## 6. Clipping: ceiling and floor

Implemented in `State.__post_init__()` (`model.py`). Two steps in fixed order, applied after each state update.

### Step 1 — TEN\_BASAL\_MIN floor (axis by axis)

```
for each axis a ∈ {F, R, S}:
    ten_a = f⁺_a + f⁻_a
    if ten_a < TEN_BASAL_MIN:
        add = (TEN_BASAL_MIN − ten_a) / 2
        f⁺_a ← f⁺_a + add
        f⁻_a ← f⁻_a + add
```

Preserves $\text{pos}_a$ exactly (the increment `add` is added to both forces and cancels in the difference).

### Step 2 — VOL\_MAX ceiling (scales the surplus, preserves the floor)

```
total = ten_F + ten_R + ten_S
if total > VOL_MAX:
    allowed_surplus = VOL_MAX − 3·TEN_BASAL_MIN    # = 7.70
    exc_a = ten_a − TEN_BASAL_MIN   (for each axis)
    exc_total = exc_F + exc_R + exc_S
    if exc_total > 0:
        scale = allowed_surplus / exc_total
        for each axis a with exc_a > 0:
            new_ten_a = TEN_BASAL_MIN + exc_a · scale
            r = new_ten_a / ten_a
            f⁺_a ← f⁺_a · r
            f⁻_a ← f⁻_a · r
```

**Properties:**

- Axes with `exc_a = 0` (exactly at the minimum floor) are unmodified.
- The ratio $f^+_a / f^-_a$ within each axis is preserved: position $\text{pos}_a$ scales proportionally.
- **Concrete example (TENSE state + OPP stimulus, $\delta = 1.5$):** ten\_F\_req = 9.1, exc\_F = 9.0, scale = 7.70/9.0 = 0.8556, new\_ten\_F = 7.80, pos\_F\_result = 1.286 (instead of the requested 1.5). The stimulus is partially absorbed.

---

## 7. Experimental setup

### Experiments A and B — Opportunity blindness and Yerkes-Dodson

Files: `experiments_dinamica_tension_inmediato.py`, `robustez_experimentos.py`

| Parameter | Value |
|---|---|
| $\eta$ | 0.05 |
| $\delta$ (stimulus) | 1.5 (nominal) |
| $N_{\text{post}}$ | 80 steps |
| $N_{\text{rest}}$ | 0 |
| Seeds (robustness Test 1) | 100 independent Gaussian perturbations |
| Noise on F forces | $\sigma_F = 0.05$ (absolute) |
| Noise on R, S forces | $\sigma_{RS} = 0.01$ (absolute) |
| Generator | `numpy.random.default_rng(0)` |
| CALM state | `State(pF=1.0, nF=1.0, pR=0.05, nR=0.05, pS=0.05, nS=0.05)` |
| TENSE state | `State(pF=3.8, nF=3.8, pR=0.05, nR=0.05, pS=0.05, nS=0.05)` |
| OPPORTUNITY stimulus | `pF += δ` (all other forces unchanged) |
| THREAT stimulus | `nF += δ` (all other forces unchanged) |
| Swept levels (Exp B) | 2.0, 4.0, 6.0, 7.0, 7.5, 7.9 |
| VOL\_MAX ablation (Test 2) | 100.0 (effectively no ceiling) |
| VOL\_MAX calibration range (Test 3) | [7.0, 10.0] |
| $\delta$ calibration range (Test 3) | [0.25, 2.5] |
| $\sigma_F$ calibration range (Test 3) | [0.15, 0.40] |

### Experiment C — Social typology

Files: `experiments_decentramiento.py`, `robustez_exp_CD.py`

| Parameter | Value |
|---|---|
| Grid | 20 × 20 |
| Steps per episode | 300 |
| Social stimulus position | centre (row 10, column 10) |
| Social field | $s(r,c) = 1.5 \cdot \exp\!\left(-d_{\text{Eucl}} / 4.0\right)$ |
| HP (fixed during episode) | 90.0 |
| Energy (fixed during episode) | 15.0 |
| Coupling | disabled ($\sigma_F = \sigma_R = \sigma_S = 0$) for all three phenotypes |
| Proximity threshold (`PROX_THRESH`) | 3.0 cells |
| Seeds Test 1 (robustness) | 100 random initial positions |

**Three-phenotype configurations:**

| Phenotype | `s_pos_target` | `w_s_pos` | `sens` |
|---|---|---|---|
| Positive (seeks bond) | **+1.0** | **0.8** | 0.0 |
| Neutral (indifferent) | **0.0** | **0.0** | 0.0 |
| Negative (avoids) | **−1.0** | **0.8** | 0.0 |

> **Note:** `s_pos_target = 0` with `w_s_pos = 0` produces genuine indifference (s does not enter d). `s_pos_target = 0` with `w_s_pos > 0` produces avoidance because the social field with $s > 0$ deviates from the zero target.

**VOL\_MAX check:** maximum observed tension ≈ 3.1 ≪ VOL\_MAX = 8.0. The ceiling never activates in this experiment.

### Experiment D — Decentering as engine of exploration

Files: `experiments_decentramiento.py`, `robustez_exp_CD.py`

| Parameter | Value |
|---|---|
| Grid | 10 × 10 |
| Steps per episode | 500 |
| Initial position | centre (5, 5) |
| Initial HP | 75.0 (= `HP_EQ`) |
| Initial energy | 10.0 (= `ENERGY_EQ`) |
| `HP_DECAY` (metabolic cost per step) | **0.10** |
| `ENERGY_DECAY` (metabolic cost per step) | **0.05** |
| `MOVE_SCALE` | **3.0** (distance at which prob(move) = 1.0) |
| Movement probability | $\min(1,\; d / 3.0)$ |
| "Early activity" window | first **100** steps |
| Seeds Test 1 (robustness) | 100 stochastic seeds |

**Three-phenotype configurations:**

| Phenotype | `f_pos_target` | `r_pos_target` | `s_pos_target` | `sens` |
|---|---|---|---|---|
| Centered (reactive) | 0.0 | 0.0 | 0.0 | 0.0 |
| Positive (proactive) | **1.0** (default) | **2.0** (default) | **0.8** (default) | default |
| Negative (collapses) | **−1.0** | **−2.0** | **−0.8** | 0.0 |

**VOL\_MAX check:** maximum observed tension ≈ 4.1 ≪ VOL\_MAX = 8.0. The ceiling never activates in this experiment.

---

## 8. Note on the v1 shim

### Experiments using `State(pF, nF, ...)` directly — v2 API (independent forces)

- `experiments_dinamica_tension_inmediato.py`
- `experimentos_niveles_tension.py`
- `experimentos_riqueza_orientacion.py`
- `robustez_experimentos.py`

In these experiments $f^+_a \cdot f^-_a > 0$ at all times (both forces active), which is the v2 independence signature. The opportunity-blindness and Yerkes-Dodson phenomena depend on this independence.

### Experiments using `state_from_observables(hp, energy, s)` — v1 shim

- `experiments_decentramiento.py` (Exp A decentering, Exp B social typology)
- `robustez_exp_CD.py` (Exp C typology, Exp D decentering — via `d_obs`)

The shim implements:

$$f^+_F = \max\!\left(0,\; \frac{hp - \text{HP\_EQ}}{\text{HP\_SCALE}}\right), \qquad f^-_F = \max\!\left(0,\; \frac{\text{HP\_EQ} - hp}{\text{HP\_SCALE}}\right)$$

and analogously for $R$ (energy) and $S$. This forces $f^+_a \cdot f^-_a = 0$ for every axis, so $\text{ten}_a = |\text{pos}_a|$ (regression to v1 behaviour).

**Why this is admissible:** Experiments C and D do not require position/tension separability — their phenomena (social typology, decentering as exploration engine) depend on `s_pos_target` and `f/r/s_pos_target` respectively. The shim is correct for the purpose of those experiments. Experiments that require v2 independence (A and B) use exclusively the direct State API.

**v2 introduction commit:** `434f123`. All opportunity-blindness and Yerkes-Dodson experiments were committed after that commit.
