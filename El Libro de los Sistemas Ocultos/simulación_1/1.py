import numpy as np
import networkx as nx
from scipy.integrate import quad
import matplotlib.pyplot as plt

# ==========================================
# 1. CONSTRUCCIÓN MATRICIAL DE LA RED COMPLEJA
# ==========================================
np.random.seed(42)
nodos = 40
G = nx.erdos_renyi_graph(n=nodos, p=0.3, seed=42)

# Asignar pesos aleatorios a las aristas
for u, v in G.edges():
    G[u][v]['weight'] = np.random.uniform(0.1, 1.0)

# Obtener la Matriz de Adyacencia (W) y la Matriz Laplaciana (L = D - W)
W = nx.adjacency_matrix(G, weight='weight').toarray()
L = nx.laplacian_matrix(G, weight='weight').toarray()

print("--- ANÁLISIS MATRICIAL Y FUNCIONAL AVANZADO ---")
print(f"Dimensión de la Matriz Laplaciana (L): {L.shape}")

# ==========================================
# 2. INTEGRACIÓN NUMÉRICA DE CAMPOS FUNCIONALES
# ==========================================
# Simulamos el "Mapeo a Campos Funcionales" del póster integrando 
# una densidad de energía continua f(x) sobre un dominio continuo [0, 1] 
# influenciada por las propiedades espectrales del grafo.

def densidad_energia_continua(x, autovalor_laminrar):
    # Función de onda o campo funcional continuo modelado con integrales
    return np.exp(-x) * np.cos(autovalor_laminrar * np.pi * x) ** 2

# Calculamos la integral numérica de la energía para un campo asociado al grafo
autovalores, autovectores = np.linalg.eigh(L)
# Usamos el segundo autovalor no nulo (Fiedler value) para parametrizar la integral
lambda_fiedler = autovalores[1] 

energia_integral, _ = quad(densidad_energia_continua, 0, 1, args=(lambda_fiedler,))
print(f"Valor del Funcional Integrado (Campo Continuo): {energia_integral:.6f}")

# ==========================================
# 3. OPTIMIZACIÓN MATRICIAL EXACTA 
# ==========================================
# En lugar de aleatoriedad, usamos el autovector asociado al segundo 
# autovalor más pequeño de la matriz Laplaciana (Vector de Fiedler)
vector_fiedler = autovectores[:, 1]

# Particionamiento óptimo basado en el signo del Vector de Fiedler
f_spectral = {i: 1 if vector_fiedler[i] >= 0 else -1 for i in range(nodos)}

# Cálculo matricial del Funcional de Energía: E(f) = f^T * L * f
f_vector = np.array([f_spectral[i] for i in range(nodos)])
energia_matricial = np.dot(f_vector.T, np.dot(L, f_vector))

print(f"Energía Matricial Minimizada por Espectroscopia: {energia_matricial:.4f}")
print("Conclusión: Las matrices y el cálculo integral proporcionan una solución determinista.")

# ==========================================
# 4. VISUALIZACIÓN CIENTÍFICA
# ==========================================
plt.figure(figsize=(9, 6))
pos = nx.spring_layout(G, seed=42)

# Colorear nodos según la partición matricial exacta
colores_nodos = ['#ff6b6b' if f_spectral[node] == 1 else '#4dabf7' for node in G.nodes()]

nx.draw(G, pos, node_color=colores_nodos, with_labels=False, node_size=200)
plt.title(f"Partición Espectral de Grafos vía Matrices Laplacianas\nEnergía Matricial E(f) = {energia_matricial:.2f} | Integral Funcional = {energia_integral:.4f}", fontsize=11)
plt.tight_layout()
plt.show()