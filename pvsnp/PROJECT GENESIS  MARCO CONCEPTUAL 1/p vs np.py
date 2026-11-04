
import sympy as sp
import math


# ============================================================
# 1. FUNCION DE IGUALDAD
# ============================================================

def equality_function(u, v):
    return int(u == v)


# ============================================================
# 2. MATRIZ DE COMUNICACION
# ============================================================

def communication_matrix(m):
    """
    Construye M[u,v] = 1 si u=v, y 0 en otro caso.
    Dimensiones: 2^m x 2^m.
    """

    N = 2**m

    M = sp.zeros(N, N)

    for u in range(N):
        for v in range(N):
            M[u, v] = equality_function(u, v)

    return M


# ============================================================
# 3. RANGO EXACTO
# ============================================================

def exact_rank(M):
    return M.rank()


# ============================================================
# 4. CIRCUITO BOOLEANO DE IGUALDAD
# ============================================================

def equality_circuit_gate_count(m):
    """
    Base de puertas:
        AND, OR, NOT.

    XOR(a,b) = (a OR b) AND NOT(a AND b)
    Coste: 4 puertas.

    XNOR requiere una NOT adicional.
    Coste: 5 puertas.

    Se combinan los m resultados con m-1 AND.
    """

    xnor_gates = 5 * m
    final_and_gates = m - 1

    return xnor_gates + final_and_gates


# ============================================================
# 5. VERIFICACION DEL RANGO EXPONENCIAL
# ============================================================

def verify_exponential_rank(m):

    M = communication_matrix(m)

    rank = exact_rank(M)

    theoretical_rank = 2**m

    print("\nVARIABLES POR GRUPO:", m)
    print("Dimension matricial:", M.shape)
    print("Rango calculado:", rank)
    print("Rango teorico:", theoretical_rank)

    assert rank == theoretical_rank

    print("Cota exponencial verificada: TRUE")

    return rank


# ============================================================
# 6. COMPARACION CON COMPLEJIDAD DE CIRCUITOS
# ============================================================

def compare_circuit_and_tensor(m):

    tensor_rank = verify_exponential_rank(m)

    circuit_size = equality_circuit_gate_count(m)

    print("\nCOMPLEJIDAD")
    print("Puertas del circuito:", circuit_size)
    print("Rango tensorial:", tensor_rank)

    print(
        "Circuito lineal:",
        circuit_size <= 6*m
    )

    print(
        "Rango exponencial:",
        tensor_rank == 2**m
    )


# ============================================================
# 7. DEMOSTRACION POR APLANAMIENTO
# ============================================================

def flattening_lower_bound(m):

    """
    El tensor de igualdad se aplana separando
    las variables u de las variables v.

    El aplanamiento es la matriz identidad.

    El rango matricial es una cota inferior
    del rango tensorial.
    """

    M = communication_matrix(m)

    matrix_rank = M.rank()

    print("\nAPLANAMIENTO TENSORIAL")
    print("Rango matricial:", matrix_rank)

    print(
        "Cota inferior del rango tensorial:",
        matrix_rank
    )

    return matrix_rank


# ============================================================
# 8. VERIFICACION DE LA DESCOMPOSICION TENSORIAL
# ============================================================

def verify_tensor_decomposition(m):

    """
    EQ_m(u,v) = suma_z [u=z][v=z].

    Cada sumando es un tensor simple:
        producto_i [u_i=z_i][v_i=z_i].

    Hay exactamente 2^m sumandos.

    Junto con la cota inferior del aplanamiento,
    esto demuestra que el rango tensorial es 2^m.
    """

    upper_bound = 2**m
    lower_bound = flattening_lower_bound(m)

    print("\nRANGO TENSORIAL EXACTO")
    print("Cota inferior:", lower_bound)
    print("Cota superior:", upper_bound)

    assert lower_bound == upper_bound

    print("RANGO TENSORIAL =", upper_bound)

    return upper_bound


# ============================================================
# 9. EXPERIMENTO PARA VARIOS TAMAÑOS
# ============================================================

def experiment():

    print("=" * 65)
    print("CIRCUITOS BOOLEANOS Y RANGO TENSORIAL")
    print("=" * 65)

    for m in range(1, 11):

        print("\n" + "-" * 65)

        compare_circuit_and_tensor(m)

        verify_tensor_decomposition(m)

    print("\nEXPERIMENTO COMPLETADO")


# ============================================================
# 10. EJECUCION
# ============================================================

if __name__ == "__main__":

    experiment()
