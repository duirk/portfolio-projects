import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

def comsol_style_optical_waveguide_simulation():
    """
    Simulación de propagación de campo óptico en guía de onda (2D)
    Estilo COMSOL Multiphysics: Análisis de perfil de índice y modos propagados.
    """
    # ---------------------------------------------------------
    # 1. PARÁMETROS FÍSICOS Y GEOMETRÍA (ESTILO MESH COMSOL)
    # ---------------------------------------------------------
    lambda0 = 1.55e-6          # Longitud de onda (1550 nm)
    k0 = 2 * np.pi / lambda0   # Número de onda en vacío
    
    # Dimensiones del dominio (Micras)
    Lx = 40.0e-6               # Ancho del dominio transversal (x)
    Lz = 500.0e-6              # Distancia de propagación (z)
    core_width = 8.0e-6        # Ancho del núcleo de la fibra
    
    # Índices de refracción y pérdidas reales
    n_core = 1.45              # Índice del núcleo
    n_cladding = 1.445         # Índice del revestimiento
    alpha_loss = 0.2           # Atenuación lineal (dB/km) -> Convertido a m^-1
    alpha_m = (alpha_loss / (10 * np.log10(np.e))) * 1e-3
    
    # Mallado computacional (Grid 2D)
    Nx = 200                   # Nodos transversales
    Nz = 400                   # Nodos longitudinales
    dx = Lx / Nx
    dz = Lz / Nz
    
    x = np.linspace(-Lx/2, Lx/2, Nx)
    z = np.linspace(0, Lz, Nz)
    
    # ---------------------------------------------------------
    # 2. CONSTRUCCIÓN DEL PERFIL DE ÍNDICE DE REFRACCIÓN n(x)
    # ---------------------------------------------------------
    n_profile = np.where(np.abs(x) <= core_width / 2, n_core, n_cladding)
    n_ref = n_cladding          # Índice de referencia para paraxialidad
    
    # ---------------------------------------------------------
    # 3. MÉTODOS DE ELEMENTOS / DIFERENCIAS FINITAS (FD-BPM)
    # ---------------------------------------------------------
    # Operador de derivada segunda espacial d2/dx2 con dtype=complex
    main_diag = -2.0 * np.ones(Nx, dtype=complex)
    off_diag = 1.0 * np.ones(Nx - 1, dtype=complex)
    L_op = diags([off_diag, main_diag, off_diag], [-1, 0, 1], dtype=complex) / (dx**2)
    
    # Construcción del operador de avance Crank-Nicolson (Estabilidad COMSOL)
    k_square_diff = (k0**2) * (n_profile**2 - n_ref**2) - 1j * k0 * n_ref * alpha_m
    
    # Definición de matrices en espacio complejo
    I_mat = diags([np.ones(Nx, dtype=complex)], [0], dtype=complex)
    V_mat = diags([k_square_diff], [0], dtype=complex)
    
    A_mat = I_mat - (1j * dz / (4 * k0 * n_ref)) * (L_op + V_mat)
    B_mat = I_mat + (1j * dz / (4 * k0 * n_ref)) * (L_op + V_mat)
    
    # Matriz para almacenar el campo 2D E(x, z)
    E_field = np.zeros((Nz, Nx), dtype=complex)
    
    # Condición de entrada: Modo Gaussiano fundamental acoplado
    w0 = core_width / 2
    E_field[0, :] = np.exp(-(x**2) / (w0**2))
    
    # Solución iterativa del sistema matricial
    A_csc = A_mat.tocsc()
    for idx_z in range(0, Nz - 1):
        rhs = B_mat.dot(E_field[idx_z, :])
        E_field[idx_z + 1, :] = spsolve(A_csc, rhs)
        
    Intensity = np.abs(E_field)**2

    # ---------------------------------------------------------
    # 4. VISUALIZACIÓN MULTIPHYSICS (COLORMAP ESTILO COMSOL)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Mapa de intensidad de campo eléctrico 2D
    X_mesh, Z_mesh = np.meshgrid(x * 1e6, z * 1e6)
    c = ax.pcolormesh(Z_mesh, X_mesh, Intensity, cmap='magma', shading='auto')
    
    # Líneas que delimitan el núcleo de la fibra
    ax.axhline(y=core_width*1e6/2, color='cyan', linestyle='--', alpha=0.6, label='Límite Núcleo/Revestimiento')
    ax.axhline(y=-core_width*1e6/2, color='cyan', linestyle='--', alpha=0.6)
    
    # Formato y etiquetas académicas
    ax.set_title("COMSOL Multiphysics - Módulo de Óptica Ondulatoria\nPerfil de Propagación del Campo Eléctrico $|E(x,z)|^2$", fontsize=12)
    ax.set_xlabel("Distancia de Propagación z (μm)")
    ax.set_ylabel("Posición Transversal x (μm)")
    
    cbar = fig.colorbar(c, ax=ax)
    cbar.set_label("Intensidad Normalizada |E|^2 (V^2/m^2)")
    
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    comsol_style_optical_waveguide_simulation()