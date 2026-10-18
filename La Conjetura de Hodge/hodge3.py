import torch
import numpy as np

def resolver_hodge_dec_modificado(n_nodos, aristas):
    """
    Versión mejorada que utiliza matrices de incidencia (Cálculo Exterior Discreto)
    y evita el colapso trivial mediante una restricción de norma y un nodo anclado.
    """
    print("=" * 75)
    print(" LABORATORIO PUNTURUM: HODGE DISCRETO CON MATRICES DE INCIDENCIA")
    print("=" * 75)
    
    # 1. Construir la matriz de coborde / incidencia (d0) de tamaño [n_aristas, n_nodos]
    n_aristas = len(aristas)
    d0 = torch.zeros((n_aristas, n_nodos), dtype=torch.float64)
    pesos = torch.zeros(n_aristas, dtype=torch.float64)
    
    for idx, (u, v, w) in enumerate(aristas):
        d0[idx, u] = -1.0
        d0[idx, v] = 1.0
        pesos[idx] = w

    # Matriz de Hodge diagonal para las aristas basada en los pesos métricos (*)
    estrella_aristas = torch.diag(pesos)

    # 2. Inicialización del campo escalar f (0-formas)
    # Requerimos requires_grad=True para optimización diferenciable
    f = torch.rand(n_nodos, requires_grad=True, dtype=torch.float64)
    optimizer = torch.optim.Adam([f], lr=0.1)
    
    for epoch in range(1500):
        optimizer.zero_grad()
        
        # Gradiente discreto del campo: df = d0 * f
        df = torch.matmul(d0, f)
        
        # Energía de Dirichlet / Hodge discreta: E(f) = 1/2 * (df)^T * (*) * df
        # Esto mide la tensión o energía acumulada en las aristas de la red
        energia_hodge = 0.5 * torch.dot(df, torch.matmul(estrella_aristas, df))
        
        # Término de penalización para evitar el colapso a cero trivial:
        # Forzamos que la norma del campo se mantenga cerca de un valor de referencia (ej. 2.0)
        penalizacion_norma = (torch.sum(f**2) - 2.0) ** 2
        
        costo = energia_hodge + 1.0 * penalizacion_norma
        
        costo.backward()
        optimizer.step()
        
        with torch.no_grad():
            # Mantener los valores acotados en el rango de relajación [0, 1]
            f.clamp_(0.0, 1.0)
            # Anclar el primer nodo para romper la simetría trivial
            f[0] = 1.0 

    energia_final = float(energia_hodge.item())
    
    # Aterrizaje: Proyección estricta a ciclos enteros {0, 1}
    with torch.no_grad():
        f_discreto = torch.round(f)
        
    return f_discreto.numpy(), energia_final

# ================================================================
# EJECUCIÓN PRINCIPAL
# ================================================================

if __name__ == "__main__":
    # Definimos un grafo de incidencia (malla de 4 nodos)
    # Formato: (nodo_u, nodo_v, peso_metrico_w)
    aristas_ejemplo = [
        (0, 1, 1.2),
        (1, 2, 1.8),
        (2, 3, 1.5),
        (3, 0, 2.0),
        (0, 2, 0.9)
    ]
    n_variables = 4
    
    f_opt, e_hodge = resolver_hodge_dec_modificado(n_variables, aristas_ejemplo)
    
    print(f"\nCampo escalar optimizado (Suelo discretizado con restricciones): {f_opt}")
    print(f"Energía de Hodge residual en el continuo: {e_hodge:.6f}")
    print("=" * 75)