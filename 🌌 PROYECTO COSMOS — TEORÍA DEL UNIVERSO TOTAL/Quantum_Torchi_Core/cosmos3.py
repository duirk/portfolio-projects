import pygame
import sys
import math
import random

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NASA / TORCHI SYSTEM - HISTORICAL QUANTUM INTERFACE ")

# Paleta de colores CRT (Fósforo Verde / Estilo Histórico)
CRT_BG = (8, 12, 18)
CRT_GREEN = (0, 255, 128)
CRT_DIM = (20, 60, 40)
CRT_WHITE = (210, 230, 220)
ACCENT_CYAN = (0, 200, 255)

# Tipografías estilo consola
font_main = pygame.font.SysFont("Courier New", 15, bold=True)
font_title = pygame.font.SysFont("Courier New", 18, bold=True)

# Variables de estado
mission_time = 0
matrix_3x3 = [[random.randint(1, 9) for _ in range(3)] for _ in range(3)]
pendulum_angle = 0.0

clock = pygame.time.Clock()

def calcular_traza(mat):
    return mat[0][0] + mat[1][1] + mat[2][2]

while True:
    mission_time += 0.05
    pendulum_angle = math.sin(mission_time) * 45.0

    # Cálculos matemáticos reales para mostrar en pantalla
    derivada_val = math.cos(mission_time)
    integral_val = -math.cos(mission_time)
    traza_afin = calcular_traza(matrix_3x3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reiniciar aleatoriamente
                matrix_3x3 = [[random.randint(1, 9) for _ in range(3)] for _ in range(3)]
            elif event.key == pygame.K_e:  # Modificar matriz manualmente por consola
                print("\n--- CONFIGURACIÓN MANUAL DE MATRIZ 3x3 ---")
                try:
                    entrada = input("Introduce 9 números separados por espacios: ")
                    numeros = [int(x) for x in entrada.split()]
                    if len(numeros) == 9:
                        matrix_3x3 = [
                            numeros[0:3],
                            numeros[3:6],
                            numeros[6:9]
                        ]
                        print("¡Matriz actualizada con éxito!\n")
                    else:
                        print("Error: Debes introducir exactamente 9 números. Se mantiene la matriz anterior.\n")
                except ValueError:
                    print("Error: Entrada inválida. Usa solo números enteros.\n")

    screen.fill(CRT_BG)

    # --- ENCABEZADO DE MISIÓN ---
    title = font_title.render("SISTEMA ESPACIAL: INTERFACE TORCHI / ESPACIO ", True, CRT_GREEN)
    screen.blit(title, (30, 20))
    time_lbl = font_main.render(f"MET: {int(mission_time*20):06d}s | PLANCK / CUÁNTICO: ACTIVO", True, CRT_WHITE)
    screen.blit(time_lbl, (750, 20))
    pygame.draw.line(screen, CRT_DIM, (30, 50), (WIDTH - 30, 50), 1)

    # --- BLOQUE 1: ALGORITMO 1 (Distancias, Medidas, Péndulo y Fórmulas Globales) ---
    pygame.draw.rect(screen, CRT_DIM, (30, 70, 590, 330), 1)
    t1 = font_title.render(">[ ALGORITMO 1: DISTANCIAS Y MEDIDAS ]", True, CRT_GREEN)
    screen.blit(t1, (45, 85))

    lines_alg1 = [
        "- Funciones globales y modificación a tiempo real",
        f"- Distancias & Varia Medidas: {50 + math.sin(mission_time)*10:.2f} m",
        f"- Péndulo a tiempo real: {pendulum_angle:.2f}°",
        "- Constante de Planck / Fórmulas Cuánticas: 6.626e-34 J·s",
        "- Interfaz Torchi / Módulo Espacial sincronizada"
    ]
    for i, l in enumerate(lines_alg1):
        txt = font_main.render(l, True, CRT_WHITE)
        screen.blit(txt, (45, 130 + i * 35))

    # --- BLOQUE 2: ALGORITMO 2 (Sistema 3x3, Derivadas, Planos Afín, Conectividad) ---
    pygame.draw.rect(screen, CRT_DIM, (650, 70, 600, 330), 1)
    t2 = font_title.render(">[ ALGORITMO 2: SISTEMA 3x3 & AFÍN ]", True, CRT_GREEN)
    screen.blit(t2, (665, 85))

    # Renderizado de la Matriz 3x3
    for r_idx, row in enumerate(matrix_3x3):
        row_str = " | ".join([f"{val:2d}" for val in row])
        mat_txt = font_main.render(f"Matriz [ {row_str} ]", True, ACCENT_CYAN)
        screen.blit(mat_txt, (685, 130 + r_idx * 30))

    lines_alg2 = [
        f"- Op. Diferencial Temporal (d/dt): {derivada_val:.3f} | Integral: {integral_val:.3f}",
        f"- Morfismo Espacio-Afín (Traza Tensorial): {traza_afin}",
        "- Conectividad Neuronal / Red: Estable",
        "  [Presiona 'R' aleatorio | Presiona 'E' para editar matriz]"
    ]
    for i, l in enumerate(lines_alg2):
        txt = font_main.render(l, True, CRT_WHITE)
        screen.blit(txt, (685, 235 + i * 30))

    # --- BLOQUE 3: HOMEOMORFISMO, ESFERONES Y PARÁBOLAS ---
    pygame.draw.rect(screen, CRT_DIM, (30, 420, 1220, 330), 1)
    t3 = font_title.render(">[ HOMEOMORFISMO, ESFERONES Y PARÁBOLAS ESPACIALES ]", True, CRT_GREEN)
    screen.blit(t3, (45, 435))

    # Trazado de ondas / parábolas dinámicas
    points = []
    for x in range(60, 1220, 4):
        nx = (x - 60) * 0.02
        y = 590 + int(math.sin(nx + mission_time) * 50 * math.cos(mission_time * 0.5))
        points.append((x, y))
    if len(points) > 1:
        pygame.draw.lines(screen, ACCENT_CYAN, False, points, 2)

    # Esferones animados en el espacio de trabajo
    for k in range(4):
        sx = 220 + k * 280
        sy = 650 + int(math.sin(mission_time + k) * 30)
        pygame.draw.circle(screen, CRT_GREEN, (sx, sy), 15, 2)

    footer = font_main.render("ESTADO: NÚCLEO ESPACIAL ESTABLE. [100% CONFIGURACIÓN HISTÓRICA]", True, CRT_DIM)
    screen.blit(footer, (45, 760))

    pygame.display.flip()
    clock.tick(60)