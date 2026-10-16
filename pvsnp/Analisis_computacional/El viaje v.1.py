import time
import torch
import sympy as sp

def vuelo_y_aterrizaje_punturum(n_vars):
    """
    1. FASE DE VUELO: Navegación continua en el aire con PyTorch.
    2. FASE DE ATERRIZAJE: Proyección discreta al suelo.
    """
    v = torch.rand(n_vars, requires_grad=True, dtype=torch.float64)
    optimizer = torch.optim.Adam([v], lr=0.04)
    
    for _ in range(500):
        optimizer.zero_grad()
        energia_continua = torch.sum(v**2 * (1.0 - v)**2)
        for i in range(n_vars - 1):
            energia_continua = energia_continua + (v[i] * v[i+1] - 0.3)**2
            
        energia_continua.backward()
        optimizer.step()
        
        with torch.no_grad():
            v.clamp_(0.0, 1.0)
            
    energia_vuelo = float(energia_continua.item())
    
    with torch.no_grad():
        v_discreto = torch.round(v)
        energia_suelo = torch.sum(v_discreto**2 * (1.0 - v_discreto)**2)
        for i in range(n_vars - 1):
            energia_suelo = energia_suelo + (v_discreto[i] * v_discreto[i+1] - 0.3)**2
            
    return v.detach().numpy(), energia_vuelo, float(energia_suelo.item())

def extraer_formulas_del_otro_lado(v_optimo):
    """
    3. FASE SIMBÓLICA AL OTRO LADO: Usa SymPy para derivar exactamente 
       las fórmulas algebraicas del estado alcanzado.
    """
    print("\n" + "=" * 75)
    print(" EXTRACCIÓN SIMBÓLICA AL OTRO LADO DEL MURO (SYMPY)")
    print("=" * 75)
    
    # Tomamos una muestra representativa de variables simbólicas del vuelo exitoso
    x1, x2, x3 = sp.symbols('x1 x2 x3')
    
    # Funcional general del sistema al otro lado
    E_simbolica = x1**2 * (1.0 - x1)**2 + x2**2 * (1.0 - x2)**2 + x3**2 * (1.0 - x3)**2 \
                  + (x1 * x2 - 0.3)**2 + (x2 * x3 - 0.3)**2
                  
    # Derivadas analíticas exactas en el espacio continuo del otro lado
    grad_x1 = sp.diff(E_simbolica, x1)
    grad_x2 = sp.diff(E_simbolica, x2)
    
    print(f" Funcional de Energía Analítica (Al otro lado):")
    print(f" E(x1, x2, x3) = {E_simbolica}")
    print(f"\n Gradiente exacto respecto a x1 (dE/dx1):")
    print(f" {grad_x1}")
    print(f"\n Gradiente exacto respecto a x2 (dE/dx2):")
    print(f" {grad_x2}")
    print(f"\n Coordenadas reales alcanzadas por el vuelo (muestra n=5):")
    print(f" v_opt = {v_optimo[:3]}")
    print("=" * 75)

# ================================================================
# EJECUCIÓN PRINCIPAL DEL LABORATORIO PUNTURUM
# ================================================================

if __name__ == "__main__":
    print("=" * 75)
    print(" LABORATORIO PUNTURUM: VUELO, ATERRIZAJE Y FÓRMULAS DEL OTRO LADO")
    print("=" * 75)
    print(f"{'Variables (n)':<15} | {'Energía en el Aire (Vuelo)':<25} | {'Energía al Aterrizar (Suelo)':<25}")
    print("-" * 75)
    
    escalas = [5, 10, 20, 40, 80, 160]
    ultimo_v = None
    
    for n in escalas:
        v_opt, e_vuelo, e_suelo = vuelo_y_aterrizaje_punturum(n)
        if n == 5:
            ultimo_v = v_opt
        print(f"n = {n:<10} | {e_vuelo:<25.6f} | {e_suelo:<25.6f}")
        
    # Una vez cruzado el muro, extraemos las fórmulas exactas del otro lado
    extraer_formulas_del_otro_lado(ultimo_v)