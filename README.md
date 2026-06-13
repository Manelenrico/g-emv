# Geometría de las Emociones: Un Modelo de Fuerzas Oponentes

**Autor:** Manel Enrico  
**Estado:** borrador de trabajo — privado

## Idea central

Cada eje emocional (Físico, Material/Recursos, Social) tiene dos fuerzas
oponentes: f⁺ (placer/aproximación) y f⁻ (displacer/evitación).

- **Posición** en el eje = f⁺ − f⁻
- **Tensión** (intensidad) = f⁺ + f⁻
- **Emoción** = colapso cuando el equilibrio de tensiones se rompe
- **Acoplamiento asimétrico**: lo físico pesa más sobre los otros ejes

## Estructura del repositorio

```
model.py        — núcleo matemático (fuerzas oponentes, distancia homeostática)
experiments.py  — experimentos: fenotipos explorador/apático, aburrimiento, curiosidad
figures/        — salidas gráficas generadas por experiments.py
README.md       — este archivo
```

## Entorno

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy matplotlib
```
