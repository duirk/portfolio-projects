# Marco Computacional Integrado para el Diseño y Optimización de Aleaciones Metálicas Complejas

**Autor:** Nadal Ferrá - Investigador Independiente  
**Fecha:** 26/09/2026

# Alloy Design Framework

Framework de Machine Learning integrado para el diseño y optimización de aleaciones ternarias (Fe-Ti-Al), combinando física de materiales y optimización matemática.

## ¿Qué tiene de diferente respecto a otros enfoques?

* **Física informada (*Informed ML*):** No es una red neuronal ciega; integra los criterios termodinámicos y cristalográficos de **Hume-Rothery** mediante una matriz de compatibilidad ($T$) basada en radios atómicos y electronegatividades para filtrar composiciones inviables.
* **Diseño Inverso:** En lugar de probar composiciones al azar para ver qué propiedades resultan, utiliza optimización matemática restringida (SLSQP) para encontrar la receta química exacta que cumple con los objetivos de resistencia y ductilidad.
* **Validación cruzada robusta y comparativa:** Evalúa y compara directamente el rendimiento de modelos avanzados (MLP, Random Forest) frente a líneas base tradicionales (Ridge) utilizando métricas reales (MAE, RMSE, $R^2$).

## Características principales

* Generación y validación de matrices de compatibilidad atómica.
* Modelado predictivo mediante redes neuronales (MLPRegressor).
* Optimización multiobjetivo de composiciones en el espacio ternario.
* Generación automática de mapas ternarios de calor y gráficos de validación.
---

## 🚀 Requisitos e Instalación

Para ejecutar este script, asegúrate de tener instalado Python 3.x junto con las siguientes bibliotecas científicas:

```bash
pip install numpy scikit-learn matplotlib
