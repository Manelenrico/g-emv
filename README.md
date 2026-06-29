# G-EMV — Geometric Architecture for Homeostatic Orientation in Agents

**Author:** Manel Enrico · ORCID [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)  
**License:** MIT  
**Preprint:** [10.5281/zenodo.20719082](https://doi.org/10.5281/zenodo.20719082)

---

## Description

G-EMV is a mathematical model of the motivational orientation of an artificial agent. The central idea is that any agent can be described by three orthogonal axes of interest — F (physical/bodily), R (resources/material), and S (social/relational) — each with two opponent forces: an approach force (f+) and an avoidance force (f-). The difference f+ - f- defines the agent's *position* on the axis (positive or negative orientation) and the sum f+ + f- defines its *tension* (activation intensity). This two-component representation captures both the directionality and the intensity of motivation in a unified framework.

The agent's dynamics are an exact gradient descent on a weighted homeostatic distance function that measures how far the current state deviates from the equilibrium point. The model includes two physiologically motivated constraints: a per-axis minimum tension floor (TEN_BASAL_MIN = 0.10) and a total activation volume ceiling (VOL_MAX = 8.0). A cross-axis coupling mechanism causes excess tension in one axis to amplify the sensitivity of the other two, reproducing the emotional diffusion characteristic of high-load states.

This repository accompanies the preprint with complete, reproducible, self-contained code: the model core, all reported experiments, ablation and robustness tests, and the scripts that generate every data figure.

---

## Paper figures (v2)

The preprint contains 11 figures. Figures 1, 2, and 5 are illustrations; the remaining eight are generated from the scripts in this repository.

| Fig | Theme | Type | Script |
|-----|-------|------|--------|
| 1 | Six-force sphere | illustration | (none) |
| 2 | Two opponent forces on one axis | illustration | (none) |
| 3 | Displacement by domain (position) | data | `make_figs_EN.py` |
| 4 | Tension by domain | data | `make_figs_EN.py` |
| 5 | Two-limit sphere | illustration | (none) |
| 6 | Negativity bias | data | `make_fig_sesgo_EN.py` |
| 7 | Activation optimum | data | `make_fig_optimo_EN.py` |
| 8 | Saturation blindness | data | `make_fig_ceguera_EN.py` |
| 9 | Orientation richness recovery | data | `make_fig_riqueza_EN.py` |
| 10 | Concentration at poles (histogram) | data | `make_fig_histograma_EN.py` |
| 11 | Cross-modulation | data | `make_fig_acopl_EN.py` |

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
├── experiments_dinamica_tension_inmediato.py ← Saturation blindness experiment
├── experimentos_niveles_tension.py           ← Activation optimum experiment
├── experimentos_riqueza_orientacion.py       ← Orientation richness recovery
├── experiments_decentramiento.py             ← Social typology and proactivity
├── experiments_descentramiento_optimo.py     ← Optimal decentering by environment
├── experiments_anticipacion.py               ← Computational cost of anticipation
│
├── robustez_experimentos.py                  ← Ablation/robustness: experiments A and B
├── robustez_exp_CD.py                        ← Ablation/robustness: experiments C and D
│
├── make_figs_EN.py                           ← Generates Figs 3 and 4
├── make_fig_sesgo_EN.py                      ← Generates Fig 6 (negativity bias)
├── make_fig_optimo_EN.py                     ← Generates Fig 7 (activation optimum)
├── make_fig_ceguera_EN.py                    ← Generates Fig 8 (saturation blindness)
├── make_fig_riqueza_EN.py                    ← Generates Fig 9 (richness recovery)
├── make_fig_histograma_EN.py                 ← Generates Fig 10 (concentration histogram)
├── make_fig_acopl_EN.py                      ← Generates Fig 11 (cross-modulation)
│
├── figures_paper.py                          ← Legacy v1 figure generator (five figures)
├── figure_firmas_activacion.py               ← Sphere figure (requires attractor_signatures.json)
│
├── figures/                                  ← Pre-generated PNGs from the preprint
│   ├── fig01_six_forces_sphere.jpg
│   ├── fig02_two_forces.png
│   ├── fig03_displacement.png
│   ├── fig04_tension.png
│   ├── fig05_two_limits_sphere.jpg
│   ├── fig06_negativity_bias.png
│   ├── fig07_activation_optimum.png
│   ├── fig08_saturation_blindness.png
│   ├── fig09_richness_recovery.png
│   ├── fig10_concentration.png
│   └── fig11_cross_modulation.png
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

Requires Python >= 3.10 (tested on Python 3.12). The only external dependencies are NumPy and Matplotlib. No scikit-learn is used: the k-means algorithm is implemented from scratch (Lloyd's with k-means++ initialisation and 15 restarts).

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
# Prints DEFAULT_CONFIG parameters, constants, and theoretical equilibrium
```

### Single global attractor

```bash
python experiments_atractores.py
# 3000 initial conditions distributed across the full state space,
# 400 steps of dynamics with no external stimuli.
# → attractor_data.json
# Result: sigma = 4.46e-16 (single attractor at pos* = (0.821, 1.601, 0.680))
```

### Activation signatures on the sphere

```bash
python experiments_firmas_activacion.py
# 3000 perturbations (10% pure-pole, 45% two-axis mixes, 45% three-axis mixes),
# signature = mean signed deviation over 80 recovery steps, normalised to unit sphere.
# → attractor_signatures.json
# Result: 62.7% of mixes within 30 degrees of a pure pole (spherical null: 40.2%)
```

### Figs 3 and 4 — Displacement and tension by domain

```bash
python make_figs_EN.py
# Diagram figures illustrating position and tension geometry.
# → figures/fig_esquema_descentramiento_EN.png
# → figures/fig_esquema_tension_EN.png
```

### Fig 6 — Negativity bias

```bash
python make_fig_sesgo_EN.py
# Gradient descent to equilibrium from asymmetric initial states.
# Quantifies the asymmetric approach vs avoidance geometry.
# → figures/fig_sesgo_negatividad_EN.png
```

### Fig 7 — Activation optimum

```bash
python make_fig_optimo_EN.py
# Sweep of ten_F in {2.0, 4.0, 6.0, 7.0, 7.5, 7.9} with stimulus delta = 1.5.
# Result: opportunity sensitivity peaks at ten_F = 6.0, then drops sharply
# as VOL_MAX is approached. This resembles the pattern of an activation optimum
# (moderate tension favours sensitivity; the model does not directly measure
# task performance, so the parallel with Yerkes-Dodson is phenomenological).
# → figures/fig5_optimo_activacion_EN.png
```

### Fig 8 — Saturation blindness

```bash
python make_fig_ceguera_EN.py
# Two agents: calm (ten_F = 2.0) and saturated (ten_F = 7.6).
# Opportunity: delta = +1.5 on pF. Threat: delta = +1.5 on nF.
# Result: delta_d_calm = 0.628, delta_d_saturated = 0.042
#         threat_calm  = 1.381, threat_saturated  = 0.456
# Saturated agent is ~15x less sensitive to opportunity; threat remains detectable.
# → figures/fig6_ceguera_saturacion_EN.png
```

### Fig 9 — Orientation richness recovery

```bash
python make_fig_riqueza_EN.py
# Initial state: zeppelin (all tension concentrated in F; R and S at floor).
# Result: richness index R rises from 0 to ~0.92 in 80 steps with no external stimulus.
# → figures/fig_riqueza_recuperacion_EN.png
```

### Fig 10 — Concentration at poles

```bash
# Requires attractor_signatures.json (generated by experiments_firmas_activacion.py)
python make_fig_histograma_EN.py
# Angular distance to nearest pure pole for 2- and 3-axis mixtures.
# Result: 62.7% within 30 degrees vs 40.2% by chance (enrichment: 1.56x)
# → figures/fig_concentracion_histograma_EN.png
```

### Fig 11 — Cross-modulation

```bash
python make_fig_acopl_EN.py
# Scales the coupling sensitivity coefficients (sens_F, sens_R, sens_S)
# by factors 0.5x, 1.0x, 1.5x, 2.0x to isolate the cross-axis coupling mechanism.
# → figures/fig_acoplamiento_cruzado_EN.png
```

### Additional experiments

```bash
python experiments_decentramiento.py
# Exp A (exploration engine): three agents in an empty 10x10 grid, 500 steps.
#   Positive decentering (95 cells, proactive from step 1) vs
#   Centered (68 cells, reactive) vs Negative (81 cells, declining)
# Exp B (social typology): three phenotypes in a 20x20 grid with a social stimulus.
#   Positive seeks and stays; neutral wanders; negative avoids.

python experiments_descentramiento_optimo.py
# Placid vs demanding environment: what level of decentering maximises survival?

python experiments_anticipacion.py
# Reactive / moderate / deep agents (variable think_cost).
# Result: survival curve vs anticipation cost across two environments
```

### Ablation and parametric robustness

```bash
python robustez_experimentos.py
# Systematic variation of eta, delta, and model parameters for experiments A and B

python robustez_exp_CD.py
# Parametric variation for experiments C (social typology) and D (proactivity)
```

### Generate all paper figures

```bash
# Figs 3 and 4 (position and tension diagrams)
python make_figs_EN.py

# Fig 6 (negativity bias)
python make_fig_sesgo_EN.py

# Fig 7 (activation optimum)
python make_fig_optimo_EN.py

# Fig 8 (saturation blindness)
python make_fig_ceguera_EN.py

# Fig 9 (richness recovery)
python make_fig_riqueza_EN.py

# Fig 10 (concentration histogram; requires attractor_signatures.json)
python make_fig_histograma_EN.py

# Fig 11 (cross-modulation)
python make_fig_acopl_EN.py
```

---

## Mathematical appendix

`docs/MATHEMATICAL_APPENDIX.md` contains the complete derivation: formal state definition, exact gradients of d², parameter calibrations, the VOL_MAX/TEN_BASAL_MIN mechanism, and the exact parameters for each experiment.

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

Manel Enrico  
ORCID: [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)

---

## License

MIT License — see [LICENSE](LICENSE).
