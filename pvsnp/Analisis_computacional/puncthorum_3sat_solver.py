import time
import torch
import random
import numpy as np

def generar_3sat_aleatorio(n_vars, n_clausulas):
    """
    Genera un problema 3-SAT aleatorio con n_vars variables y n_clausulas.
    """
    clausulas = []
    for _ in range(n_clausulas):
        vars_3 = random.sample(range(1, n_vars + 1), 3)
        lit_a = vars_3[0] if random.random() > 0.5 else -vars_3[0]
        lit_b = vars_3[1] if random.random() > 0.5 else -vars_3[1]
        lit_c = vars_3[2] if random.random() > 0.5 else -vars_3[2]
        clausulas.append((lit_a, lit_b, lit_c))
    return clausulas

def resolver_3sat_con_ruido(clausulas, n_vars, lr=0.02, epochs=6000):
    """
    Resuelve 3-SAT a gran escala combinando relajación continua, 
    penalización de binarización e inyección de ruido estocástico.
    """
    v = torch.rand(n_vars, requires_grad=True, dtype=torch.float64)
    optimizer = torch.optim.Adam([v], lr=lr)
    
    for epoch in range(epochs):
        optimizer.zero_grad()
        
        # Annealing para la binarización
        lambda_binarizacion = min(1.0, epoch / (epochs * 0.7)) * 1.5
        
        penalizacion_satisfaccion = 0.0
        for literal_a, literal_b, literal_c in clausulas:
            val_a = v[abs(literal_a) - 1] if literal_a > 0 else (1.0 - v[abs(literal_a) - 1])
            val_b = v[abs(literal_b) - 1] if literal_b > 0 else (1.0 - v[abs(literal_b) - 1])
            val_c = v[abs(literal_c) - 1] if literal_c > 0 else (1.0 - v[abs(literal_c) - 1])
            
            clausula_insatisfecha = (1.0 - val_a) * (1.0 - val_b) * (1.0 - val_c)
            penalizacion_satisfaccion = penalizacion_satisfaccion + clausula_insatisfecha
            
        penalizacion_binaria = torch.sum(v * (1.0 - v))
        costo_total = penalizacion_satisfaccion + (lambda_binarizacion * penalizacion_binaria)
        
        costo_total.backward()
        optimizer.step()
        
        # --- NUEVO: PERTURBACIÓN ESTOCÁSTICA (Inyección de ruido) ---
        # Durante las primeras 60% de las épocas, inyectamos pequeños "kicks" 
        # aleatorios cada 100 épocas para escapar de mínimos locales.
        if epoch < epochs * 0.6 and epoch % 100 == 0:
            with torch.no_grad():
                ruido = torch.randn_like(v) * 0.12 * (1.0 - epoch / (epochs * 0.6))
                v.add_(ruido)
        
        # Mantener en el rango [0, 1]
        with torch.no_grad():
            v.clamp_(0.0, 1.0)
            
    energia_vuelo = float(penalizacion_satisfaccion.item())
    
    # Aterrizaje final
    with torch.no_grad():
        v_discreto = torch.round(v)
        violaciones_suelo = 0
        for literal_a, literal_b, literal_c in clausulas:
            val_a = v_discreto[abs(literal_a) - 1].item() if literal_a > 0 else (1.0 - v_discreto[abs(literal_a) - 1].item())
            val_b = v_discreto[abs(literal_b) - 1].item() if literal_b > 0 else (1.0 - v_discreto[abs(literal_b) - 1].item())
            val_c = v_discreto[abs(literal_c) - 1].item() if literal_c > 0 else (1.0 - v_discreto[abs(literal_c) - 1].item())
            
            if val_a == 0 and val_b == 0 and val_c == 0:
                violaciones_suelo += 1
                
    return v_discreto.numpy(), energia_vuelo, int(violaciones_suelo)

# ================================================================
# EJECUCIÓN PRINCIPAL
# ================================================================

if __name__ == "__main__":
    print("=" * 75)
    print(" LABORATORIO PUNTURUM: 50 VARIABLES CON PERTURBACIÓN ESTOCÁSTICA")
    print("=" * 75)
    
    n_variables = 50
    n_clausulas = 200
    
    clausulas_aleatorias = generar_3sat_aleatorio(n_variables, n_clausulas)
    
    inicio = time.time()
    v_opt, e_vuelo, violaciones_suelo = resolver_3sat_con_ruido(clausulas_aleatorias, n_variables)
    tiempo_total = time.time() - inicio
    
    print(f"Variables analizadas:               {n_variables}")
    print(f"Cláusulas generadas:               {n_clausulas}")
    print(f"Asignación booleana parcial:       {v_opt[:15]}... (mostrando primeras 15)")
    print(f"Energía residual en el aire:       {e_vuelo:.6f}")
    print(f"Cláusulas insatisfechas (Suelo):   {violaciones_suelo}")
    print(f"Tiempo de ejecución:               {tiempo_total:.4f} segundos")
    print("=" * 75)