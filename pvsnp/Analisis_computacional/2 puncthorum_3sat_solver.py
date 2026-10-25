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

def resolver_3sat_arquitectura_1(clausulas, n_vars, lr=0.02, epochs=4000):
    """
    ARQUITECTURA DEL ALGORITMO I: Relajación continua, annealing, 
    optimización con Adam y perturbación estocástica.
    """
    v = torch.rand(n_vars, requires_grad=True, dtype=torch.float64)
    optimizer = torch.optim.Adam([v], lr=lr)
    
    for epoch in range(epochs):
        optimizer.zero_grad()
        
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
        
        # Perturbación estocástica (Inyección de ruido)
        if epoch < epochs * 0.6 and epoch % 100 == 0:
            with torch.no_grad():
                ruido = torch.randn_like(v) * 0.12 * (1.0 - epoch / (epochs * 0.6))
                v.add_(ruido)
                
        with torch.no_grad():
            v.clamp_(0.0, 1.0)
            
    return v.detach(), float(penalizacion_satisfaccion.item())

def resolver_3sat_arquitectura_2(clausulas, n_vars, v_base, n_variaciones=5):
    """
    ARQUITECTURA DEL ALGORITMO II (Multicapa, Índice de Variaciones y Solución Global):
    Toma la solución base de la Arquitectura I y genera múltiples capas de variaciones
    estocásticas indexadas para explorar vecindarios locales y consolidar la Solución Global.
    """
    print("\n[+] Ejecutando Arquitectura del Algoritmo II (Capas, Variaciones e Índice)...")
    
    mejores_variaciones = []
    
    with torch.no_grad():
        for i in range(n_variaciones):
            # Capa de variación indexada con perturbación direccional
            capa_ruido = torch.randn_like(v_base) * (0.05 * (i + 1))
            v_variante = torch.clamp(v_base + capa_ruido, 0.0, 1.0)
            v_discreto = torch.round(v_variante)
            
            # Evaluar violaciones en el suelo para esta variación
            violaciones = 0
            for literal_a, literal_b, literal_c in clausulas:
                val_a = v_discreto[abs(literal_a) - 1].item() if literal_a > 0 else (1.0 - v_discreto[abs(literal_a) - 1].item())
                val_b = v_discreto[abs(literal_b) - 1].item() if literal_b > 0 else (1.0 - v_discreto[abs(literal_b) - 1].item())
                val_c = v_discreto[abs(literal_c) - 1].item() if literal_c > 0 else (1.0 - v_discreto[abs(literal_c) - 1].item())
                
                if val_a == 0 and val_b == 0 and val_c == 0:
                    violaciones += 1
            
            mejores_variaciones.append({
                "indice": i + 1,
                "vector": v_discreto.numpy(),
                "violaciones": int(violaciones)
            })
            print(f"    -> Capa/Variación #{i+1} indexada | Violaciones detectadas: {violaciones}")

    # Selección de la Solución Global óptima basada en el menor número de violaciones
    solucion_global = min(mejores_variaciones, key=lambda x: x["violaciones"])
    return solucion_global

# ================================================================
# EJECUCIÓN PRINCIPAL CON DOBLE ARQUITECTURA
# ================================================================

if __name__ == "__main__":
    print("=" * 75)
    print(" LABORATORIO PUNTURUM: SISTEMA DE DOBLE ARQUITECTURA 3-SAT")
    print("=" * 75)
    
    n_variables = 50
    n_clausulas = 200
    
    clausulas_aleatorias = generar_3sat_aleatorio(n_variables, n_clausulas)
    
    inicio = time.time()
    
    # Fase 1: Arquitectura I (Relajación, Adam y Perturbación Estocástica)
    v_opt, e_vuelo = resolver_3sat_arquitectura_1(clausulas_aleatorias, n_variables)
    
    # Fase 2: Arquitectura II (Capas, Índice, Variaciones y Solución Global)
    resultado_global = resolver_3sat_arquitectura_2(clausulas_aleatorias, n_variables, v_opt, n_variaciones=6)
    
    tiempo_total = time.time() - inicio
    
    print("\n" + "=" * 75)
    print(" REPORTE DE RESULTADOS - LABORATORIO PUNTURUM")
    print("=" * 75)
    print(f"Variables analizadas:               {n_variables}")
    print(f"Cláusulas generadas:                {n_clausulas}")
    print(f"Energía residual en el aire (Alg. I): {e_vuelo:.6f}")
    print(f"Variación ganadora (Algoritmo II):  Índice #{resultado_global['indice']}")
    print(f"Cláusulas insatisfechas (Suelo):    {resultado_global['violaciones']}")
    print(f"Asignación Global Definitiva:       {resultado_global['vector'][:15]}... (primeras 15)")
    print(f"Tiempo total de ejecución:          {tiempo_total:.4f} segundos")
    print("=" * 75)