# G-EMV — Geometría de Emociones, Motivaciones y Valores

**Arquitectura geométrica de orientación homeostática para agentes**

**Autor:** Manel Enrico · ORCID [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)  
**Licencia:** MIT  
**Preprint:** *(enlace arXiv pendiente de publicación)*

---

## Descripción

G-EMV es un modelo matemático de la orientación motivacional de un agente artificial. La idea central es que todo agente puede describirse mediante tres ejes ortogonales de interés —**F** (físico/corporal), **R** (recursos/material) y **S** (social/relacional)— cada uno con dos fuerzas oponentes: una de aproximación (f⁺) y otra de evitación (f⁻). La diferencia f⁺ − f⁻ define la *posición* del agente en el eje (orientación positiva o negativa) y la suma f⁺ + f⁻ define la *tensión* (intensidad de activación). Esta representación de doble componente captura de forma unificada la direccionalidad y la intensidad de la motivación.

La dinámica del agente es un **descenso de gradiente exacto** sobre una función de distancia homeostática ponderada, que mide cuánto se aleja el estado actual del punto de equilibrio. El modelo incluye dos restricciones fisiológicamente motivadas: un suelo de tensión mínima por eje (TEN_BASAL_MIN = 0.10) y un techo de volumen total de activación (VOL_MAX = 8.0). Un mecanismo de **acoplamiento cruzado** hace que el exceso en un eje amplifique la sensibilidad de los demás, reproduciendo la difusión emocional característica de los estados de alta carga.

El repositorio acompaña al preprint con el código completo, reproducible y autocontenido: el modelo, los experimentos reportados, las pruebas de ablación/robustez y los scripts que generan todas las figuras.

---

## Estructura del repositorio

```
gemv/
│
├── model.py                               ← Núcleo: State, ModelConfig,
│                                             distancia homeostática, DEFAULT_CONFIG
│
├── experiments_atractores.py              ← Atractor global único
├── experiments_firmas_activacion.py       ← Firmas de respuesta en la esfera
├── experiments_dinamica_tension_inmediato.py  ← Ceguera a la oportunidad  (Fig 1)
├── experimentos_niveles_tension.py        ← Óptimo de activación / Yerkes-Dodson  (Fig 2)
├── experimentos_riqueza_orientacion.py    ← Recuperación de riqueza de orientación  (Fig 3)
├── experiments_decentramiento.py          ← Tipología social (Fig 4) + Proactividad  (Fig 5)
├── experiments_descentramiento_optimo.py  ← Descentramiento óptimo según el entorno
├── experiments_anticipacion.py            ← Coste computacional de la anticipación
├── experiments_dinamica_tension.py        ← Exploración dinámica calma vs tensión
├── experiments.py                         ← Exploración preliminar (fenotipos, aburrimiento)
├── experiments_tension.py                 ← Exploración preliminar (tensión independiente)
│
├── robustez_experimentos.py               ← Ablación/robustez: experimentos A y B
├── robustez_exp_CD.py                     ← Ablación/robustez: experimentos C y D
│
├── figures_paper.py                       ← Genera las 5 figuras del paper
├── figure_firmas_activacion.py            ← Genera la figura de la esfera
│
├── figures/                               ← PNGs generados (reproducibles)
│   ├── fig1_ceguera_oportunidad.png
│   ├── fig2_optimo_activacion.png
│   ├── fig3_recuperacion_riqueza.png
│   ├── fig4_tipologia_social.png
│   ├── fig5_proactividad.png
│   ├── exp_firmas_activacion_esfera.png
│   └── ...                               (figuras de exploración)
│
├── attractor_data.json                    ← Resultados: 3000 condiciones → atractor
├── attractor_signatures.json             ← Resultados: 3000 firmas normalizadas
│
├── docs/
│   └── APENDICE_MATEMATICO.md            ← Derivaciones y parámetros exactos (LaTeX)
│
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

## Instalación

Requiere **Python ≥ 3.10**. Las únicas dependencias externas son NumPy y Matplotlib. No se usa scikit-learn: el algoritmo k-means está implementado manualmente (Lloyd's con k-means++ y 15 repeticiones de inicialización).

```bash
# Clonar el repositorio
git clone https://github.com/Manelenrico/geometria-emociones.git
cd geometria-emociones

# Entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## Reproducción de experimentos

Todos los scripts imprimen resultados numéricos en la consola y guardan figuras en `figures/`. Las semillas aleatorias están fijadas en el código para reproducibilidad exacta.

### Modelo: verificación del núcleo

```bash
python model.py
# Imprime parámetros de DEFAULT_CONFIG, constantes y equilibrio teórico
```

### Experimento: atractor global único

```bash
python experiments_atractores.py
# 3000 condiciones iniciales distribuidas por el espacio de estado completo,
# 400 pasos de dinámica sin estímulos externos.
# → attractor_data.json
# Resultado: σ = 4.46×10⁻¹⁶ (un único atractor en pos* ≈ (0.821, 1.601, 0.680))
```

### Experimento: firmas de activación en la esfera

```bash
python experiments_firmas_activacion.py
# 3000 perturbaciones (10% puras, 45% mezclas 2 ejes, 45% mezclas 3 ejes),
# firma = desviación media firmada durante 80 pasos de recuperación, normalizada.
# → attractor_signatures.json
# Resultado: 62.7% de las mezclas dentro de 30° de un polo puro (nulo esférico: 40.2%)

python figure_firmas_activacion.py   # requiere attractor_signatures.json
# → figures/exp_firmas_activacion_esfera.png
```

### Fig 1 — Ceguera a la oportunidad

```bash
python experiments_dinamica_tension_inmediato.py
# Dos agentes con pos_F=0 y ten_F ∈ {2.0, 7.6}; oportunidad δ=1.5 en pF.
# Resultado: Δd_calma = 0.628, Δd_saturado = 0.042  (×15 de diferencia)
```

### Fig 2 — Óptimo de activación (Yerkes-Dodson)

```bash
python experimentos_niveles_tension.py
# Barrido de ten_F ∈ {2.0, 4.0, 6.0, 7.0, 7.5, 7.9}, mismo estímulo δ=1.5.
# Resultado: Δd(ten_F) con pico en ten_F ≈ 6.2 y caída brusca al superar VOL_MAX
```

### Fig 3 — Recuperación de riqueza de orientación

```bash
python experimentos_riqueza_orientacion.py
# Estado inicial: cepellín (exceso de tensión concentrado en F, R y S en basal).
# Resultado: índice de riqueza R sube de 0 a 0.92 en 80 pasos sin estímulo externo
```

### Figs 4 y 5 — Tipología social y Proactividad

```bash
python experiments_decentramiento.py
# Exp A (motor de vida): tres agentes en entorno vacío 10×10, 500 pasos.
#   Resultado: Positivo (95 celdas, proactivo desde paso 1) vs
#              Centrado (68 celdas, reactivo) vs Negativo (81 celdas, declinante)
# Exp B (tipología social): tres fenotipos en grid 20×20 con estímulo social.
#   Resultado: positivo busca y permanece; neutro deambula; negativo evita
```

### Descentramiento óptimo dependiente del entorno

```bash
python experiments_descentramiento_optimo.py
# Entorno plácido vs exigente: ¿qué nivel de descentramiento maximiza la supervivencia?
```

### Coste computacional de la anticipación

```bash
python experiments_anticipacion.py
# Agentes reactivo / medio / profundo (think_cost variable).
# Resultado: curva de supervivencia vs coste de anticipar en dos entornos
```

### Ablación y robustez paramétrica

```bash
python robustez_experimentos.py
# Variación sistemática de η, δ y parámetros del modelo para los experimentos A y B

python robustez_exp_CD.py
# Variación paramétrica para los experimentos C (tipología social) y D (anticipación)
```

### Generar todas las figuras del paper

```bash
# Figuras 1–5 (solo requiere model.py y las dependencias estándar)
python figures_paper.py
# → figures/fig1_ceguera_oportunidad.png
# → figures/fig2_optimo_activacion.png
# → figures/fig3_recuperacion_riqueza.png
# → figures/fig4_tipologia_social.png
# → figures/fig5_proactividad.png
```

---

## Apéndice matemático

`docs/APENDICE_MATEMATICO.md` contiene la derivación completa: definición formal del estado, gradientes exactos de d², calibraciones de parámetros, mecanismo VOL_MAX/TEN_BASAL_MIN y los parámetros exactos de cada experimento.

---

## Cómo citar

Si usas este código o el modelo G-EMV en tu investigación, por favor cita el preprint:

```bibtex
@misc{enrico2025gemv,
  author    = {Enrico, Manel},
  title     = {{G-EMV}: Geometric Architecture for Homeostatic Orientation in Agents},
  year      = {2025},
  publisher = {arXiv},
  note      = {arXiv:XXXX.XXXXX},
  url       = {https://arxiv.org/abs/XXXX.XXXXX}
}
```

*(Sustituir `XXXX.XXXXX` por el identificador de arXiv en el momento de la publicación.)*

---

## Autor

**Manel Enrico**  
ORCID: [0009-0008-1732-6310](https://orcid.org/0009-0008-1732-6310)  
Email: manu.enrico1969@gmail.com

---

## Licencia

MIT License — ver [LICENSE](LICENSE).
