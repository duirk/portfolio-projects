import pygame
import sys
import math
import random

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NASA / TORCHI SYSTEM - REAL QUANTUM & PHYSICS SIMULATION")

# Paleta CRT (Fósforo Verde / Estilo Histórico)
CRT_BG = (8, 12, 18)
CRT_GREEN = (0, 255, 128)
CRT_DIM = (20, 60, 40)
CRT_WHITE = (210, 230, 220)
ACCENT_CYAN = (0, 200, 255)

# Tipografías estilo consola
font_main = pygame.font.SysFont("Courier New", 15, bold=True)
font_title = pygame.font.SysFont("Courier New", 18, bold=True)

# Variables de simulación física real
mission_time = 0.0
dt = 0.05  # Paso de tiempo para la integración numérica

# 1. Péndulo Físico Real (Ecuación diferencial: theta'' + (g/L)*sin(theta) = 0)
theta = math.pi / 4  # Ángulo inicial (45 grados en radianes)
omega = 0.0          # Velocidad angular inicial
g = 9.81             # Aceleración de la gravedad (m/s^2)
length = 2.0         # Longitud del péndulo (m)

# 2. Matriz 3x3 para Álgebra Lineal Real
matrix_3x3 = [[random.randint(-5, 5) for _ in range(3)] for _ in range(3)]

# Variables para la edición interactiva en pantalla (evita que se congele)
entering_matrix = False
input_buffer = ""
feedback_msg = ""

def calcular_traza(mat):
    return mat[0][0] + mat[1][1] + mat[2][2]

def calcular_determinante_3x3(m):
    det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
           m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
           m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    return det

clock = pygame.time.Clock()

while True:
    # --- INTEGRACIÓN FÍSICA REAL (Método de Euler para el Péndulo) ---
    alpha = -(g / length) * math.sin(theta)  # Aceleración angular
    omega += alpha * dt                      # Actualización de velocidad angular
    theta += omega * dt                      # Actualización de posición angular

    mission_time += dt

    # --- FÍSICA CUÁNTICA: Oscilador Armónico Cuántico ---
    h_bar = 1.054571817e-34  # Constante de Planck reducida (J·s)
    omega_cuantico = 1e12    # Frecuencia angular del oscilador
    energias_cuanticas = [h_bar * omega_cuantico * (n + 0.5) for n in range(4)]

    traza_val = calcular_traza(matrix_3x3)
    det_val = calcular_determinante_3x3(matrix_3x3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            if entering_matrix:
                if event.key == pygame.K_RETURN:
                    try:
                        numeros = [int(x) for x in input_buffer.split()]
                        if len(numeros) == 9:
                            matrix_3x3 = [numeros[0:3], numeros[3:6], numeros[6:9]]
                            feedback_msg = "¡Matriz actualizada con éxito!"
                        else:
                            feedback_msg = "Error: Se requieren exactamente 9 números."
                    except ValueError:
                        feedback_msg = "Error: Solo números enteros."
                    input_buffer = ""
                    entering_matrix = False
                elif event.key == pygame.K_BACKSPACE:
                    input_buffer = input_buffer[:-1]
                elif event.key == pygame.K_ESCAPE:
                    entering_matrix = False
                    input_buffer = ""
                    feedback_msg = "Edición cancelada."
                else:
                    if event.unicode.isprintable():
                        input_buffer += event.unicode
            else:
                if event.key == pygame.K_r:  # Reiniciar matriz aleatoriamente
                    matrix_3x3 = [[random.randint(-5, 5) for _ in range(3)] for _ in range(3)]
                    feedback_msg = "Matriz restablecida aleatoriamente."
                elif event.key == pygame.K_e:  # Activar modo de edición en pantalla
                    entering_matrix = True
                    input_buffer = ""
                    feedback_msg = "Escribe 9 números separados por espacios y pulsa ENTER."

    screen.fill(CRT_BG)

    # --- ENCABEZADO DE MISIÓN ---
    title = font_title.render("SISTEMA CIENTÍFICO: SIMULACIÓN FÍSICA Y CUÁNTICA REAL", True, CRT_GREEN)
    screen.blit(title, (30, 20))
    time_lbl = font_main.render(f"MET: {mission_time:6.2f}s | MOTOR FÍSICO: ACTIVO (dt={dt})", True, CRT_WHITE)
    screen.blit(time_lbl, (700, 20))
    pygame.draw.line(screen, CRT_DIM, (30, 50), (WIDTH - 30, 50), 1)

    # --- BLOQUE 1: DINÁMICA CLÁSICA (Péndulo por EDO) ---
    pygame.draw.rect(screen, CRT_DIM, (30, 70, 590, 330), 1)
    t1 = font_title.render(">[ BLOQUE 1: DINÁMICA DE SISTEMAS (PÉNDULO REAL) ]", True, CRT_GREEN)
    screen.blit(t1, (45, 85))

    lines_alg1 = [
        "- Ecuación diferencial: θ'' + (g/L)·sin(θ) = 0",
        f"- Gravedad simulada (g): {g} m/s² | Longitud (L): {length} m",
        f"- Ángulo actual (θ): {math.degrees(theta):.2f}° ({theta:.4f} rad)",
        f"- Velocidad angular (ω): {omega:.4f} rad/s",
        f"- Método numérico: Integración de Euler en tiempo real"
    ]
    for i, l in enumerate(lines_alg1):
        txt = font_main.render(l, True, CRT_WHITE)
        screen.blit(txt, (45, 130 + i * 35))

    # --- BLOQUE 2: ÁLGEBRA LINEAL Y TENSORIAL ---
    pygame.draw.rect(screen, CRT_DIM, (650, 70, 600, 330), 1)
    t2 = font_title.render(">[ BLOQUE 2: ÁLGEBRA LINEAL Y MATRICIAL ]", True, CRT_GREEN)
    screen.blit(t2, (665, 85))

    for r_idx, row in enumerate(matrix_3x3):
        row_str = " | ".join([f"{val:3d}" for val in row])
        mat_txt = font_main.render(f"Matriz [ {row_str} ]", True, ACCENT_CYAN)
        screen.blit(mat_txt, (685, 130 + r_idx * 30))

    lines_alg2 = [
        f"- Traza de la Matriz (Tr): {traza_val}",
        f"- Determinante Real (det M): {det_val}",
        f"- Condición: {'Inversible' if det_val != 0 else 'Singular (Det = 0)'}",
        "  [Presiona 'R' aleatorio | Presiona 'E' para editar matriz]"
    ]
    for i, l in enumerate(lines_alg2):
        txt = font_main.render(l, True, CRT_WHITE)
        screen.blit(txt, (685, 235 + i * 30))

    # Mostrar cuadro de entrada interactiva si se pulsa 'E'
    if entering_matrix:
        prompt_txt = font_main.render(f"> ENTRADA: {input_buffer}_", True, ACCENT_CYAN)
        screen.blit(prompt_txt, (685, 345))

    # --- BLOQUE 3: MECÁNICA CUÁNTICA (Oscilador Armónico) ---
    pygame.draw.rect(screen, CRT_DIM, (30, 420, 1220, 330), 1)
    t3 = font_title.render(">[ BLOQUE 3: MECÁNICA CUÁNTICA - NIVELES DE ENERGÍA ]", True, CRT_GREEN)
    screen.blit(t3, (45, 435))

    q_lines = [
        "Ecuación de Schrödinger (Oscilador Armónico): E_n = ℏ·ω·(n + 1/2)",
        f"Constante de Planck reducida (ℏ): {h_bar:.3e} J·s"
    ]
    for i, ql in enumerate(q_lines):
        txt = font_main.render(ql, True, CRT_WHITE)
        screen.blit(txt, (45, 480 + i * 30))

    # Representación visual de los niveles de energía discretos
    for n, en in enumerate(energias_cuanticas):
        y_pos = 570 + n * 40
        pygame.draw.line(screen, ACCENT_CYAN, (100, y_pos), (700, y_pos), 2)
        lvl_txt = font_main.render(f"Nivel n={n} | E_{n} = {en:.3e} J", True, CRT_WHITE)
        screen.blit(lvl_txt, (720, y_pos - 10))

    # Pie de página dinámico con mensajes de estado
    footer_text = f"ESTADO: {feedback_msg}" if feedback_msg else "ESTADO: SIMULACIÓN CIENTÍFICA MATEMÁTICAMENTE RIGUROSA ACTIVA."
    footer = font_main.render(footer_text, True, CRT_DIM)
    screen.blit(footer, (45, 760))

    pygame.display.flip()
    clock.tick(60)