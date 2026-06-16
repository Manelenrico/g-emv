# G-EMV — Geometric Architecture for Homeostatic Orientation in Agents

**Author:** Manel Enrico · ORCID [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)  
**License:** MIT  
**Preprint:** [10.5281/zenodo.20719082](https://doi.org/10.5281/zenodo.20719082)

---

## Description

G-EMV is a mathematical model of the motivational orientation of an artificial agent. The central idea is that any agent can be described by three orthogonal axes of interest — **F** (physical/bodily), **R** (resources/material), and **S** (social/relational) — each with two opponent forces: an approach force (f⁺) and an avoidance force (f⁻). The difference f⁺ − f⁻ defines the agent's *position* on the axis (positive or negative orientation) and the sum f⁺ + f⁻ defines its *tension* (activation intensity). This two-component representation captures both the directionality and the intensity of motivation in a unified framework.

The agent's dynamics are an **exact gradient descent** on a weighted homeostatic distance function that measures how far the current state deviates from the equilibrium point. The model includes two physiologically motivated constraints: a per-axis minimum tension floor (TEN_BASAL_MIN = 0.10) and a total activation volume ceiling (VOL_MAX = 8.0). A **cross-axis coupling** mechanism causes excess tension in one axis to amplify the sensitivity of the other two, reproducing the emotional diffusion characteristic of high-load states.

This repository accompanies the preprint with complete, reproducible, self-contained code: the model core, all reported experiments, ablation and robustness tests, and the scripts that generate every figure.

---

## Repository structure

```
g-emv/
│
├── model.py                                  ← Core: State, ModelConfig,
│                                               homeostatic distance, DEFAULT_CONFIG
│
├── experiments_atractores.py                 ← Single global attractor
├── experiments_firmas_activacion.py          ← Response signatures on the sphere
├── experiments_dinamica_tension_inmediato.py ← Opportunity blindness  (Fig 1)
├── experimentos_niveles_tension.py           ← Activation optimum / Yerkes-Dodson  (Fig 2)
├── experimentos_riqueza_orientacion.py       ← Orientation richness recovery  (Fig 3)
├── experiments_decentramiento.py             ← Social typology (Fig 4) + Proactivity (Fig 5)
├── experiments_descentramiento_optimo.py     ← Optimal decentering by environment
├── experiments_anticipacion.py              ← Computational cost of anticipation
│
├── robustez_experimentos.py                  ← Ablation/robustness: experiments A and B
├── robustez_exp_CD.py                        ← Ablation/robustness: experiments C and D
│
├── figures_paper.py                          ← Generates all five paper figures
├── figure_firmas_activacion.py              ← Generates the sphere figure
│
├── figures/                                  ← Pre-generated PNGs (reproducible)
│   ├── fig1_opportunity_blindness.png
│   ├── fig2_activation_optimum.png
│   ├── fig3_richness_recovery.png
│   ├── fig4_social_typology.png
│   ├── fig5_proactivity.png
│   └── exp_activation_signatures_sphere.png
│
├── attractor_data.json                       ← Results: 3000 conditions → attractor
├── attractor_signatures.json                 ← Results: 3000 normalised signatures
│
├── docs/
│   └── MATHEMATICAL_APPENDIX.md             ← Full derivations and exact parameters
│
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

## Installation

Requires **Python ≥ 3.10**. The only external dependencies are NumPy and Matplotlib. No scikit-learn is used: the k-means algorithm is implemented from scratch (Lloyd's with k-means++ initialisation and 15 restarts).

```bash
# Clone the repository
git clone https://github.com/Manelenrico/g-emv.git
cd g-emv

# Virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Reproducing the experiments

All scripts print numerical results to the console and save figures to `figures/`. Random seeds are fixed in the code for exact reproducibility.

### Model: core verification

```bash
python model.py
# Prints DEFAULT_CONFIG parameters, constants and theoretical equilibrium
```

### Single global attractor

```bash
python experiments_atractores.py
# 3000 initial conditions distributed across the full state space,
# 400 steps of dynamics with no external stimuli.
# → attractor_data.json
# Result: σ = 4.46×10⁻¹⁶ (single attractor at pos* ≈ (0.821, 1.601, 0.680))
```

### Activation signatures on the sphere

```bash
python experiments_firmas_activacion.py
# 3000 perturbations (10% pure-pole, 45% two-axis mixes, 45% three-axis mixes),
# signature = mean signed deviation over 80 recovery steps, normalised to unit sphere.
# → attractor_signatures.json
# Result: 62.7% of mixes within 30° of a pure pole (spherical null: 40.2%)

python figure_firmas_activacion.py   # requires attractor_signatures.json
# → figures/exp_firmas_activacion_esfera.png
```

### Fig 1 — Opportunity blindness

```bash
python experiments_dinamica_tension_inmediato.py
# Two agents with pos_F = 0 and ten_F ∈ {2.0, 7.6}; opportunity δ = 1.5 on pF.
# Result: Δd_calm = 0.628, Δd_saturated = 0.042  (×15 difference)
```

### Fig 2 — Activation optimum (Yerkes-Dodson)

```bash
python experimentos_niveles_tension.py
# Sweep of ten_F ∈ {2.0, 4.0, 6.0, 7.0, 7.5, 7.9}, same stimulus δ = 1.5.
# Result: Δd(ten_F) peaks at ten_F ≈ 6.2 with sharp drop beyond VOL_MAX
```

### Fig 3 — Orientation richness recovery

```bash
python experimentos_riqueza_orientacion.py
# Initial state: zeppelin (all tension concentrated in F, R and S at floor).
# Result: richness index R rises from 0 to 0.92 in 80 steps with no external stimulus
```

### Figs 4 and 5 — Social typology and Proactivity

```bash
python experiments_decentramiento.py
# Exp A (exploration engine): three agents in an empty 10×10 grid, 500 steps.
#   Result: Positive (95 cells, proactive from step 1) vs
#           Centered (68 cells, reactive) vs Negative (81 cells, declining)
# Exp B (social typology): three phenotypes in a 20×20 grid with a social stimulus.
#   Result: positive seeks and stays; neutral wanders; negative avoids
```

### Optimal decentering by environment

```bash
python experiments_descentramiento_optimo.py
# Placid vs demanding environment: what level of decentering maximises survival?
```

### Computational cost of anticipation

```bash
python experiments_anticipacion.py
# Reactive / moderate / deep agents (variable think_cost).
# Result: survival curve vs anticipation cost across two environments
```

### Ablation and parametric robustness

```bash
python robustez_experimentos.py
# Systematic variation of η, δ and model parameters for experiments A and B

python robustez_exp_CD.py
# Parametric variation for experiments C (social typology) and D (anticipation)
```

### Generate all paper figures

```bash
# Figures 1–5 (requires only model.py and standard dependencies)
python figures_paper.py
# → figures/fig1_opportunity_blindness.png
# → figures/fig2_activation_optimum.png
# → figures/fig3_richness_recovery.png
# → figures/fig4_social_typology.png
# → figures/fig5_proactivity.png

# Sphere figure (requires attractor_signatures.json)
python figure_firmas_activacion.py
# → figures/exp_activation_signatures_sphere.png
```

---

## Mathematical appendix

`docs/MATHEMATICAL_APPENDIX.md` contains the complete derivation: formal state definition, exact gradients of d², parameter calibrations, VOL_MAX/TEN_BASAL_MIN mechanism, and the exact parameters for each experiment.

---

## How to cite

If you use this code or the G-EMV model in your research, please cite the preprint:

```bibtex
@misc{enrico2026gemv,
  author    = {Enrico, Manel},
  title     = {{G-EMV}: Geometric Architecture for Homeostatic Orientation in Agents},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20719082},
  url       = {https://doi.org/10.5281/zenodo.20719082}
}
```

---

## Author

**Manel Enrico**  
ORCID: [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)

---

## License

MIT License — see [LICENSE](LICENSE).
