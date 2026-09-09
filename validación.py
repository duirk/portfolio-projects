import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm
import matplotlib.pyplot as plt

# ============================================================
# 1. Definición del sistema (parámetros ajustables)
# ============================================================

n = 3                     # dimensión del espacio (puedes cambiarlo)
m = 2                     # orden del operador de diferencias finitas (m-1 derivadas)
Z = 1.0                   # profundidad máxima de integración
h = 0.1                   # paso para diferencias finitas (solo se usa en la definición formal)

# Estado inicial: matriz X0 compleja aleatoria
X0 = np.random.randn(n, n) + 1j * np.random.randn(n, n)

# Matriz A (generador del flujo exponencial)
A = np.random.randn(n, n) + 1j * np.random.randn(n, n)
# Para estabilidad numérica, forzamos que A tenga autovalores con parte real negativa
# (opcional, pero ayuda a que la integral converja)
A = A - np.eye(n) * 0.5

# Matriz de bifurcación P (proyectores espectrales simulados)
# Construimos P diagonalizable con autovalores aleatorios
D = np.diag(np.random.rand(n) + 1j * np.random.rand(n))
S = np.random.randn(n, n) + 1j * np.random.randn(n, n)
P = S @ D @ np.linalg.inv(S)

# Pesos w_k(z) - función escalar para cada k
def w_k(k, z):
    # Ejemplo: peso exponencial decreciente con k
    return np.exp(-k * z) / (1 + z)

# ============================================================
# 2. Operador de diferencias finitas (orden superior)
# ============================================================

def Delta_h_k(F, k, h):
    """
    Aplica el operador de diferencias finitas de orden k a una función F(z).
    F debe ser una función que devuelva una matriz n x n.
    k: orden de la diferencia (0 = identidad, 1 = primera diferencia, etc.)
    h: paso (se usa solo para escalar, en la práctica se puede omitir)
    """
    if k == 0:
        return F
    # Aproximación de diferencias finitas centradas (para funciones matriciales)
    # Usamos una fórmula simple: (F(z+h) - F(z-h)) / (2h) para k=1, etc.
    # Para k>1 usamos recursión (diferencias sucesivas)
    def diff_k(z):
        if k == 1:
            return (F(z + h) - F(z - h)) / (2 * h)
        else:
            # Aplicamos recursivamente: Delta^k = Delta^(k-1) (Delta^1)
            F1 = lambda t: (F(t + h) - F(t - h)) / (2 * h)
            return Delta_h_k(F1, k-1, h)(z)
    return diff_k

# ============================================================
# 3. Funciones del marco formal
# ============================================================

def flujo_exponencial(z, A, X0):
    """e^{zA} X0"""
    return expm(z * A) @ X0

def camino_bifurcado(k, X0, P):
    """X^(k) = P^k X0 (bifurcación espectral)"""
    return np.linalg.matrix_power(P, k) @ X0

# ============================================================
# 4. Validación numérica de las fórmulas
# ============================================================

print("=" * 60)
print("VALIDACIÓN NUMÉRICA DEL MARCO DE SUCESIÓN MATRICIAL")
print("=" * 60)

# --- 4a. Verificar el estado inicial ---
print("\n[1] Estado inicial X0 (traza):", np.trace(X0))
print("    Norma de X0:", np.linalg.norm(X0))

# --- 4b. Verificar bifurcación espectral ---
print("\n[2] Bifurcación espectral (primeros 3 caminos):")
for k in range(3):
    Xk = camino_bifurcado(k, X0, P)
    print(f"    k={k}: traza = {np.trace(Xk):.4f}, norma = {np.linalg.norm(Xk):.4f}")

# --- 4c. Evaluar el flujo exponencial en z=0 y z=Z ---
print("\n[3] Flujo exponencial e^{zA} X0:")
F0 = flujo_exponencial(0, A, X0)
FZ = flujo_exponencial(Z, A, X0)
print(f"    z=0: traza = {np.trace(F0):.4f}, norma = {np.linalg.norm(F0):.4f}")
print(f"    z=Z: traza = {np.trace(FZ):.4f}, norma = {np.linalg.norm(FZ):.4f}")

# --- 4d. Evaluar diferencias finitas en un punto z=0.5 ---
print("\n[4] Operador de diferencias finitas Δ_h^k en z=0.5:")
z_test = 0.5
for k in range(m):
    # Definimos la función F(z) = e^{zA} X0
    F = lambda z: flujo_exponencial(z, A, X0)
    DeltaF = Delta_h_k(F, k, h)
    val = DeltaF(z_test)
    print(f"    k={k}: traza = {np.trace(val):.4f}, norma = {np.linalg.norm(val):.4f}")

# --- 4e. Evaluar la foliación de planos (subespacios) ---
print("\n[5] Foliación Π_z (rango de la matriz de vectores columna):")
# Construimos la matriz cuyas columnas son Δ_h^j (e^{zA} X0) para j=0..m-1
def construir_plano(z, A, X0, h, m):
    cols = []
    for j in range(m):
        F = lambda t: flujo_exponencial(t, A, X0)
        DeltaF = Delta_h_k(F, j, h)
        col = DeltaF(z).flatten()  # vectorizamos la matriz n x n -> vector n^2
        cols.append(col)
    # Apilamos columnas -> matriz (n^2 x m)
    M = np.column_stack(cols)
    return M

M_plano = construir_plano(z_test, A, X0, h, m)
rango = np.linalg.matrix_rank(M_plano)
print(f"    En z={z_test}, rango de Π_z = {rango} (máximo posible: {m})")
print(f"    Valores singulares de la matriz de planos: {np.linalg.svd(M_plano, compute_uv=False)}")

# --- 4f. Evaluación numérica de la integral S ---
print("\n[6] Evaluación numérica de la integral S = ∫ Σ w_k(z) Tr( Δ_h^k e^{zA} X0 ) dz")

def integrando(z):
    """Suma ponderada de trazas para un z dado"""
    total = 0.0 + 0.0j
    for k in range(m):
        F = lambda t: flujo_exponencial(t, A, X0)
        DeltaF = Delta_h_k(F, k, h)
        val = DeltaF(z)
        traza = np.trace(val)
        peso = w_k(k, z)
        total += peso * traza
    return total

# Integración numérica (parte real e imaginaria por separado)
def integrando_real(z):
    return np.real(integrando(z))

def integrando_imag(z):
    return np.imag(integrando(z))

# Usamos quad de scipy para integrar de 0 a Z
real_int, err_real = quad(integrando_real, 0, Z)
imag_int, err_imag = quad(integrando_imag, 0, Z)

S = real_int + 1j * imag_int
print(f"    S = {S:.6f} + {imag_int:.6f}j")
print(f"    Error estimado (real): {err_real:.2e}, (imag): {err_imag:.2e}")

# ============================================================
# 5. Validación adicional: comparación con caso trivial
# ============================================================

print("\n[7] Validación en caso trivial (A=0, X0=I, m=1):")
# Caso simple para verificar que la integral da algo esperado
A0 = np.zeros((n, n), dtype=complex)
X0I = np.eye(n, dtype=complex)
F0_trivial = lambda z: flujo_exponencial(z, A0, X0I)  # = I siempre
Delta0 = Delta_h_k(F0_trivial, 0, h)  # identidad
def integrando_trivial(z):
    return np.trace(Delta0(z))  # = n
S_trivial, _ = quad(lambda z: np.real(integrando_trivial(z)), 0, Z)
print(f"    Para A=0, X0=I, m=1: S teórica = n*Z = {n*Z}")
print(f"    S calculada = {S_trivial:.6f} (diferencia = {S_trivial - n*Z:.2e})")

# ============================================================
# 6. Gráfico de la función integrando (opcional)
# ============================================================
try:
    z_vals = np.linspace(0, Z, 50)
    integ_vals = [integrando(z) for z in z_vals]
    plt.figure(figsize=(8,5))
    plt.plot(z_vals, np.real(integ_vals), label='Parte real')
    plt.plot(z_vals, np.imag(integ_vals), label='Parte imaginaria')
    plt.xlabel('Profundidad z')
    plt.ylabel('Suma ponderada de trazas')
    plt.title('Evolución del integrando a lo largo de la profundidad')
    plt.legend()
    plt.grid(True)
    plt.show()
except Exception as e:
    print("    (No se pudo mostrar gráfico: requiere matplotlib)")

print("\n" + "=" * 60)
print("VALIDACIÓN COMPLETADA.")