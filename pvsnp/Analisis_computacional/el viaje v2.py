import time
import torch
import sympy as sp

def resolver_3sat_continuo_y_discreto(clausulas, n_vars):
    """
    Adapta el vuelo continuo para buscar soluciones a un problema NP (3-SAT).
    
    1. VUELO: Las variables viven en [0, 1] (relajación continua).
       La función de costo penaliza las cláusulas no satisfechas.
    2. ATERRIZAJE: Proyección a {0, 1} (booleanos).
    """
    # Inicializamos las variables en el espacio continuo [0, 1]
    v = torch.rand(n_vars, requires_grad=True, dtype=torch.float64)
    optimizer = torch.optim.Adam([v], lr=0.05)
    
    for _ in range(800):
        optimizer.zero_grad()
        
        # Función de penalización para 3-SAT:
        # Cada cláusula es una disyunción (ej: v1 OR not v2 OR v3).
        # En continuo, OR se puede aproximar con productos de negaciones:
        # Si la cláusula es (l1 or l2 or l3), queremos que al menos uno sea True (1).
        # Penalización por cláusula no satisfecha -> producto de (1 - lit) para falsos.
        penalizacion_total = 0.0
        for literal_a, literal_b, literal_c in clausulas:
            # Procesar literal a (si es negativo, su valor de verdad es 1 - v[idx])
            val_a = v[abs(literal_a) - 1] if literal_a > 0 else (1.0 - v[abs(literal_a) - 1])
            val_b = v[abs(literal_b) - 1] if literal_b > 0 else (1.0 - v[abs(literal_b) - 1])
            val_c = v[abs(literal_c) - 1] if literal_c > 0 else (1.0 - v[abs(literal_c) - 1])
            
            # Si todos son falsos (cercanos a 0), el producto es cercano a 1. 
            # Queremos minimizar este producto para forzar que al menos uno sea verdadero.
            clausula_insatisfecha = (1.0 - val_a) * (1.0 - val_b) * (1.0 - val_c)
            penalizacion_total = penalizacion_total + clausula_insatisfecha
            
        penalizacion_total.backward()
        optimizer.step()
        
        with torch.no_grad():
            v.clamp_(0.0, 1.0)
            
    energia_vuelo = float(penalizacion_total.item())
    
    # Aterrizaje: Proyección estricta a booleano {0, 1}
    with torch.no_grad():
        v_discreto = torch.round(v)
        penalizacion_suelo = 0.0
        for literal_a, literal_b, literal_c in clausulas:
            val_a = v_discreto[abs(literal_a) - 1].item() if literal_a > 0 else (1.0 - v_discreto[abs(literal_a) - 1].item())
            val_b = v_discreto[abs(literal_b) - 1].item() if literal_b > 0 else (1.0 - v_discreto[abs(literal_b) - 1].item())
            val_c = v_discreto[abs(literal_c) - 1].item() if literal_c > 0 else (1.0 - v_discreto[abs(literal_c) - 1].item())
            
            if val_a == 0 and val_b == 0 and val_c == 0:
                penalizacion_suelo += 1.0
                
    return v_discreto.numpy(), energia_vuelo, int(penalizacion_suelo)

def analisis_simbolico_np():
    """
    Usa SymPy para demostrar la complejidad algebraica del espacio discreto vs continuo.
    """
    print("\n" + "=" * 75)
    print(" ANÁLISIS SIMBÓLICO: LA BARRERA ENTRE P Y NP")
    print("=" * 75)
    
    x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
    
    # Una cláusula típica de 3-SAT expresada como polinomio continuo
    # (1 - x1) * x2 * (1 - x3) penaliza soluciones no válidas
    clausula_simbolica = (1 - x1) * x2 * (1 - x3)
    
    print(f" Cláusula lógica convertida a paisaje algebraico:")
    print(f" C(x1, x2, x3) = {clausula_simbolica}")
    print(f" Gradiente analítico:")
    print(f" dC/dx1 = {sp.diff(clausula_simbolica, x1)}")
    print("\n Nota: Mientras en el espacio continuo (P) podemos calcular derivadas")
    print(" en tiempo polinómico, el 'aterrizaje' hacia restricciones estrictas")
    print(" booleanas expone la naturaleza exponencial (NP-hard) de los mínimos locales.")
    print("=" * 75)

# ================================================================
# EJECUCIÓN PRINCIPAL
# ================================================================

if __name__ == "__main__":
    print("=" * 75)
    print(" LABORATORIO PUNTURUM ADAPTADO A PROBLEMAS NP (3-SAT)")
    print("=" * 75)
    
    # Definimos un conjunto de cláusulas de prueba (Ej: 4 variables, varias cláusulas)
    # Cada tupla representa (l1, l2, l3). Números positivos = variable, negativos = negación.
    clausulas_ejemplo = [
        (1, 2, -3),
        (-1, 3, 4),
        (-2, -3, -4),
        (1, -2, 4)
    ]
    n_variables = 4
    
    v_opt, e_vuelo, violaciones_suelo = resolver_3sat_continuo_y_discreto(clausulas_ejemplo, n_variables)
    
    print(f"Asignación booleana encontrada (Suelo): {v_opt}")
    print(f"Energía residual en el aire (Vuelo continuo): {e_vuelo:.6f}")
    print(f"Cláusulas insatisfechas tras el aterrizaje: {violaciones_suelo}")
    
    analisis_simbolico_np()