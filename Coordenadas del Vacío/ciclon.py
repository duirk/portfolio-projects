import math
import random
import sys
import pygame

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "Simulador de Dinámica de Oscilones y Campo Vectorial"
)

# Colores (Estética científica / Neón oscuro)
BG_COLOR = (10, 15, 25)
GRID_COLOR = (25, 35, 50)
VECTOR_COLOR = (70, 130, 180, 100)
TEXT_COLOR = (220, 230, 240)
ACCENT_COLOR = (0, 255, 200)
OSCILON_COLOR = (255, 100, 150)
SCAN_COLOR = (255, 220, 0)

clock = pygame.time.Clock()


class Oscilon:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.radius = 40
    self.phase = random.uniform(0, 2 * math.pi)

  def update(self):
    # Simula la oscilación interna del campo (frecuencia propia)
    self.phase += 0.05


# Inicializar el campo de oscilones (puntos de interés dinámico)
oscilones = [
    Oscilon(random.randint(200, WIDTH - 200), random.randint(150, HEIGHT - 150))
    for _ in range(3)
]

# Partícula exploradora (Buscador regido por gradientes y métricas de distancia)
explorer_x = 100
explorer_y = HEIGHT // 2
target_index = 0
speed = 3.5

font = pygame.font.SysFont("Courier New", 16)
font_bold = pygame.font.SysFont("Courier New", 18, bold=True)

running = True
while running:
  screen.fill(BG_COLOR)

  # Eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      # Añadir un nuevo oscilón donde hagas clic
      mx, my = pygame.mouse.get_pos()
      oscilones.append(Oscilon(mx, my))

  # 1. Dibujar la cuadrícula y campo vectorial (Mapas Vectoriales y Planos Afines)
  grid_size = 40
  for x in range(0, WIDTH, grid_size):
    for y in range(0, HEIGHT, grid_size):
      pygame.draw.circle(screen, GRID_COLOR, (x, y), 2)

      # Calcular vector de influencia hacia el oscilón más cercano (Gradiente)
      # Simula ds^2 = g_ij dx^i dx^j afectando el espacio local
      closest_osc = min(
          oscilones, key=lambda o: math.hypot(o.x - x, o.y - y)
      )
      dx = closest_osc.x - x
      dy = closest_osc.y - y
      dist = math.hypot(dx, dy) + 1e-5

      # Longitud y dirección del vector normalizado
      v_len = min(15, 800 / dist)
      end_x = x + (dx / dist) * v_len
      end_y = y + (dy / dist) * v_len

      pygame.draw.line(screen, (30, 50, 75), (x, y), (end_x, end_y), 1)

  # 2. Actualizar y dibujar Oscilones (Sistemas dinámicos en espiral)
  for i, osc in enumerate(oscilones):
    osc.update()
    # Dibujar ondas concéntricas dinámicas (espirales del póster)
    for r_offset in range(0, 4):
      r = (
          int(osc.radius + r_offset * 12 + math.sin(osc.phase + r_offset) * 8)
          % 80
      )
      alpha = max(0, 255 - r * 3)
      surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
      pygame.draw.circle(surf, (*OSCILON_COLOR, max(30, alpha)), (r, r), r, 1)
      screen.blit(surf, (osc.x - r, osc.y - r))

    # Centro del oscilón
    pygame.draw.circle(
        screen, ACCENT_COLOR, (int(osc.x), int(osc.y)), 5
    )  # Nodo central q

  # 3. Lógica del Explorador (Búsqueda basada en Distancia Euclidiana y Métrica)
  if oscilones:
    target = oscilones[target_index]
    dx = target.x - explorer_x
    dy = target.y - explorer_y
    dist_to_target = math.hypot(dx, dy)

    if dist_to_target > speed:
      explorer_x += (dx / dist_to_target) * speed
      explorer_y += (dy / dist_to_target) * speed
    else:
      # Cambiar al siguiente objetivo al alcanzarlo (barrido del campo)
      target_index = (target_index + 1) % len(oscilones)

  # Dibujar trayectoria de rastreo del explorador
  pygame.draw.circle(
      screen, SCAN_COLOR, (int(explorer_x), int(explorer_y)), 7
  )
  pygame.draw.circle(
      screen, (255, 255, 255), (int(explorer_x), int(explorer_y)), 3
  )

  # 4. Panel de Información Teórica en Pantalla (HUD al estilo del póster)
  title_surf = font_bold.render(
      "SISTEMA DINÁMICO: BÚSQUEDA DE OSCILONES", True, TEXT_COLOR
  )
  screen.blit(title_surf, (20, 20))

  metrics_text = [
      f"Variables Activas -> C: Campo Dinámico | P: Profundidad ({len(oscilones)} nodos) | D: 2D Métrica",
      f"Métrica Espaciotemporal ds² = g_ij dx^i dx^j: Activa",
      "Controles: Clic izquierdo para generar un nuevo oscilón en el espacio.",
  ]

  for idx, txt in enumerate(metrics_text):
    t_surf = font.render(txt, True, (150, 180, 210))
    screen.blit(t_surf, (20, 50 + idx * 22))

  pygame.display.flip()
  clock.tick(60)

pygame.quit()
sys.exit()