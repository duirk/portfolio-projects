
---

```markdown
# 🧪 Laboratorio Punctorum: Hodge Discreto con Matrices de Incidencia

**Laboratorio Punctorum** es un entorno experimental y computacional para la optimización de campos escalares sobre grafos discretos, utilizando los principios del **Cálculo Exterior Discreto (DEC)** y la **Teoría de Hodge**. 

El script modela un sistema físico o de red (como un suelo discretizado con restricciones) donde se busca minimizar la tensión global (energía de Hodge/Dirichlet) bajo un esquema de optimización diferenciable impulsado por PyTorch.

---

## 🚀 Características Principales

* **Cálculo Exterior Discreto (DEC):** Construcción automática de la matriz de coborde / incidencia ($d_0$) y la estrella de Hodge métrica para aristas.
* **Optimización Diferenciable:** Utiliza el motor de autograd y el optimizador Adam de `PyTorch` para explorar el espacio de soluciones de manera eficiente.
* **Control de Estabilidad:** Implementa restricciones de norma (penalización suave) y anclaje de nodos (restricción dura) para evitar colapsos triviales en el sistema.
* **Proyección Discreta:** Conversión final de los campos continuos relajados hacia espacios discretos binarios ($\{0, 1\}$).

---

## 📋 Requisitos del Sistema

Para ejecutar este script, necesitas tener instalado Python junto con las siguientes librerías:

* `torch`
* `numpy`

Puedes instalarlas ejecutando:
```bash
pip install torch numpy

```

---

## ⚙️ Estructura del Código

1. **Construcción de la Red:** Se define el grafo mediante una lista de aristas con pesos métricos $(u, v, w)$ y se genera la matriz de incidencia $d_0$.
2. **Optimización con Restricciones:** Durante 1500 épocas, el sistema minimiza la energía de Hodge junto a una penalización de norma, manteniendo los valores acotados en el rango $[0, 1]$ y fijando el nodo inicial.
3. **Aterrizaje Discreto:** Se redondean los valores finales del campo escalar para obtener el estado binario optimizado.

---

## 🛠️ Uso y Ejecución

Puedes ejecutar el script directamente desde tu terminal:

```bash
python hodge3.py

```

### Ejemplo de Salida Esperada:

```text
===========================================================================
 LABORATORIO PUNTURUM: HODGE DISCRETO CON MATRICES DE INCIDENCIA
===========================================================================

Campo escalar optimizado (Suelo discretizado con restricciones): [1. 1. 1. 1.]
Energía de Hodge residual en el continuo: 0.270460
===========================================================================

```

---


 