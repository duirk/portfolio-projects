import numpy as np
import matplotlib.pyplot as plt

def simulate_optical_soliton_perfect():
    # ---------------------------------------------------------
    # 1. PARÁMETROS FÍSICOS Y CONFIGURACIÓN DEL CANAL (DSF/PCF)
    # ---------------------------------------------------------
    L = 20.0            # Distancia de propagación (km)
    num_steps = 2000    # Pasos de integración espacial
    dz = L / num_steps
    
    N_pts = 4096        # Puntos de la rejilla (alta resolución)
    T_window = 800.0    # Ventana temporal (ps)
    dt = T_window / N_pts
    t = np.linspace(-T_window/2, T_window/2, N_pts)
    
    # Parámetros ópticos ajustados (Fibra de Dispersión Desplazada)
    beta2 = -2.0        # Dispersión anómala moderada (ps^2/km)
    gamma = 2.0         # Coeficiente no lineal Kerr (1/(W*km))
    alpha = 0.0         # Canal compensado sin pérdidas
    
    # ---------------------------------------------------------
    # 2. CONDICIÓN INICIAL DE SOLITÓN FUNDAMENTAL (N = 1)
    # ---------------------------------------------------------
    T0 = 10.0           # Ancho del pulso (ps)
    
    # Potencia pico exacta para el equilibrio entre GVD y Kerr
    P0 = np.abs(beta2) / (gamma * (T0**2))  # P0 = 0.01 W
    
    # Envolvente inicial del campo complejo A(z=0, t)
    A = np.sqrt(P0) / np.cosh(t / T0) + 0.0j  
    
    # Frecuencias angulares
    omega = 2 * np.pi * np.fft.fftfreq(N_pts, d=dt)
    
    # Operador lineal (Dispersión + Pérdidas)
    D_op = np.exp((-1j * (beta2 / 2) * (omega**2) - (alpha / 2)) * (dz / 2))
    
    # Matrices para almacenar la evolución
    intensity_history = np.zeros((num_steps + 1, N_pts))
    intensity_history[0, :] = np.abs(A)**2
    energy_history = np.zeros(num_steps + 1)
    energy_history[0] = np.trapz(np.abs(A)**2, t)

    # ---------------------------------------------------------
    # 3. ALGORITMO SPLIT-STEP FOURIER (SSFM)
    # ---------------------------------------------------------
    A_current = A.copy()
    
    for step in range(1, num_steps + 1):
        # Medio paso lineal
        A_f = np.fft.fft(A_current)
        A_f = A_f * D_op
        A_current = np.fft.ifft(A_f)
        
        # Paso completo no lineal
        N_op = np.exp(1j * gamma * (np.abs(A_current)**2) * dz)
        A_current = A_current * N_op
        
        # Medio paso lineal final
        A_f = np.fft.fft(A_current)
        A_f = A_f * D_op
        A_current = np.fft.ifft(A_f)
        
        # Registrar métricas
        intensity_history[step, :] = np.abs(A_current)**2
        energy_history[step] = np.trapz(np.abs(A_current)**2, t)

    # ---------------------------------------------------------
    # 4. EVALUACIÓN DE ESTABILIDAD REAL
    # ---------------------------------------------------------
    I_in = intensity_history[0, :]
    I_out = intensity_history[-1, :]
    
    correlation = np.corrcoef(I_in, I_out)[0, 1]
    energy_retention = energy_history[-1] / energy_history[0]
    
    print("=" * 60)
    print("REPORTE DE ESTABILIDAD DEL CAMPO ÓPTICO CONTINUO")
    print("=" * 60)
    print(f"Energía Inicial:          {energy_history[0]:.6f} W*ps")
    print(f"Energía Final:            {energy_history[-1]:.6f} W*ps")
    print(f"Retención de Energía:     {energy_retention * 100:.2f}%")
    print(f"Fidelidad de Forma (0-1): {correlation:.6f}")
    
    if correlation > 0.98 and 0.95 <= energy_retention <= 1.05:
        print("\nResultado: ESTABLE REAL [OK]")
        print("El solitón propagó manteniendo su forma e intensidad intactas.")
    else:
        print("\nResultado: INESTABLE / DEFORMADO [ERROR]")
        print("La señal sufrió dispersión, rotura o pérdidas severas.")
    print("=" * 60)

    # ---------------------------------------------------------
    # 5. VISUALIZACIÓN GRÁFICA
    # ---------------------------------------------------------
    z_vals = np.linspace(0, L, num_steps + 1)
    T_mesh, Z_mesh = np.meshgrid(t, z_vals)

    plt.figure(figsize=(12, 5))

    # Gráfica 1: Canal 2D constante
    plt.subplot(1, 2, 1)
    plt.pcolormesh(T_mesh, Z_mesh, intensity_history, shading='auto', cmap='viridis')
    plt.xlim(-100, 100)
    plt.title("Evolución del Campo Óptico A(z,t)")
    plt.xlabel("Tiempo retardado t (ps)")
    plt.ylabel("Distancia de propagación z (km)")
    plt.colorbar(label="Intensidad |A|^2 (W)")

    # Gráfica 2: Perfil Entrante vs Saliente (Superposición exacta)
    plt.subplot(1, 2, 2)
    plt.plot(t, I_in, 'b--', linewidth=2, label="Perfil Entrante (z=0 km)")
    plt.plot(t, I_out, 'r-', linewidth=1.5, label=f"Perfil Saliente (z={L} km)")
    plt.xlim(-100, 100)
    plt.title("Estabilidad del Perfil de Intensidad")
    plt.xlabel("Tiempo retardado t (ps)")
    plt.ylabel("Intensidad (W)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    simulate_optical_soliton_perfect()