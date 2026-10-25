import pygame
import random
import math
import sys

# Inicializar Pygame
pygame.init()
WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PUNTURUM HITO HISTÓRICO - Motor de Optimización con Datos Reales de Empresa")
clock = pygame.time.Clock()

# Paleta de colores futurista / Ciberpunk Corporativo
BG_COLOR = (10, 14, 23)
PANEL_BG = (18, 26, 42)
TEXT_COLOR = (220, 230, 242)
ACCENT_GREEN = (0, 255, 128)
ACCENT_CYAN = (0, 200, 255)
ACCENT_ORANGE = (255, 140, 0)
ACCENT_RED = (255, 60, 60)
MUTED_GRAY = (80, 100, 130)

# Fuentes
font_title = pygame.font.SysFont("Consolas", 20, bold=True)
font_main = pygame.font.SysFont("Consolas", 14)
font_small = pygame.font.SysFont("Consolas", 11)

# ==========================================
# DATOS REALES DE UNA EMPRESA FALSA
# ==========================================
DATOS_EMPRESA_FALSA = {
    "nombre": "Logística Global Punturum S.A.",
    "vehiculos_disponibles": 12,
    "pedidos_urgentes": 45,
    "centros_distribucion": ["Madrid", "Barcelona", "Valencia", "Sevilla"],
    "restricciones_max_horas": 8,
    "costo_combustible_litro": 1.65
}

# ==========================================
# ESTADOS DEL SIMULADOR INDUSTRIAL
# ==========================================
FASE_INICIAL = 0
FASE_RELAJACION = 1
FASE_PERTURBACION = 2
FASE_ATERRIZAJE = 3
FASE_COMPLETADO = 4

class SimuladorEmpresaHito:
    def __init__(self):
        self.n_vars = 50
        self.n_clausulas = 200
        self.fase = FASE_INICIAL
        self.epoch = 0
        self.max_epochs = 4000
        self.energia_vuelo = 100.0
        self.violaciones = self.n_clausulas
        self.tiempo_transcurrido = 0.0
        
        # Variables continuas [0, 1] y discretas basadas en la empresa
        self.v_continuas = [random.random() for _ in range(self.n_vars)]
        self.v_discretas = [0 for _ in range(self.n_vars)]
        
        # Generar cláusulas vinculadas a las restricciones de la empresa falsa
        self.clausulas = []
        for _ in range(self.n_clausulas):
            vars_3 = random.sample(range(1, self.n_vars + 1), 3)
            l1 = vars_3[0] if random.random() > 0.5 else -vars_3[0]
            l2 = vars_3[1] if random.random() > 0.5 else -vars_3[1]
            l3 = vars_3[2] if random.random() > 0.5 else -vars_3[2]
            self.clausulas.append((l1, l2, l3))
            
        # Posiciones visuales para los nodos de la red logística
        self.nodos_pos = []
        centro_x, centro_y = 320, 380
        radio_red = 220
        for i in range(self.n_vars):
            angulo = (i / self.n_vars) * 2 * math.pi
            x = centro_x + math.cos(angulo) * radio_red
            y = centro_y + math.sin(angulo) * radio_red
            self.nodos_pos.append([x, y])

        self.historial_energia = []
        
    def reiniciar(self):
        self.__init__()
        self.fase = FASE_RELAJACION

    def actualizar(self):
        if self.fase == FASE_RELAJACION or self.fase == FASE_PERTURBACION:
            self.epoch += 40  
            progreso = min(1.0, self.epoch / self.max_epochs)
            
            if self.epoch < self.max_epochs * 0.6:
                self.fase = FASE_RELAJACION
                ruido_factor = 0.15 * (1.0 - progreso)
                for i in range(self.n_vars):
                    self.v_continuas[i] += random.gauss(0, ruido_factor)
                    self.v_continuas[i] += (0.5 - self.v_continuas[i]) * 0.05
                    self.v_continuas[i] = max(0.0, min(1.0, self.v_continuas[i]))
            else:
                self.fase = FASE_PERTURBACION
                for i in range(self.n_vars):
                    meta = 1.0 if self.v_continuas[i] > 0.5 else 0.0
                    self.v_continuas[i] += (meta - self.v_continuas[i]) * 0.1
            
            penalizacion = 0.0
            for l1, l2, l3 in self.clausulas:
                def get_val(lit):
                    idx = abs(lit) - 1
                    val = self.v_continuas[idx]
                    return val if lit > 0 else (1.0 - val)
                
                v_a, v_b, v_c = get_val(l1), get_val(l2), get_val(l3)
                insatisfecha = (1.0 - v_a) * (1.0 - v_b) * (1.0 - v_c)
                penalizacion += insatisfecha
                
            self.energia_vuelo = penalizacion
            self.historial_energia.append(self.energia_vuelo)
            if len(self.historial_energia) > 150:
                self.historial_energia.pop(0)
                
            if self.epoch >= self.max_epochs:
                self.fase = FASE_ATERRIZAJE
                
        elif self.fase == FASE_ATERRIZAJE:
            self.v_discretas = [1 if v >= 0.5 else 0 for v in self.v_continuas]
            
            vuelo_violaciones = 0
            for l1, l2, l3 in self.clausulas:
                def get_disc(lit):
                    idx = abs(lit) - 1
                    val = self.v_discretas[idx]
                    return val if lit > 0 else (1 - val)
                
                if get_disc(l1) == 0 and get_disc(l2) == 0 and get_disc(l3) == 0:
                    vuelo_violaciones += 1
            
            self.violaciones = vuelo_violaciones
            self.fase = FASE_COMPLETADO

simulador = SimuladorEmpresaHito()

# ==========================================
# BUCLE PRINCIPAL DE PYGAME
# ==========================================
ejecutando = True
while ejecutando:
    clock.tick(60)
    simulador.tiempo_transcurrido += 1 / 60.0
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                simulador.reiniciar()
            elif evento.key == pygame.K_ESCAPE:
                ejecutando = False

    simulador.actualizar()

    # --- RENDERIZADO ---
    screen.fill(BG_COLOR)

    # 1. TÍTULO Y CABECERA
    pygame.draw.rect(screen, PANEL_BG, (20, 20, WIDTH - 40, 60), border_radius=8)
    pygame.draw.rect(screen, ACCENT_CYAN, (20, 20, WIDTH - 40, 60), 1, border_radius=8)
    
    txt_titulo = font_title.render(f"EMPRESA: {DATOS_EMPRESA_FALSA['nombre']} // MOTOR DE OPTIMIZACIÓN", True, TEXT_COLOR)
    screen.blit(txt_titulo, (35, 30))
    
    estado_strs = [
        "LISTO (PULSA ESPACIO PARA OPTIMIZAR)", 
        "FASE I: PROCESANDO RESTRICCIONES DE FLOTA...", 
        "FASE II: PERTURBACIÓN Y CÁLCULO DE RUTAS...", 
        "ASIGNANDO RECURSOS...", 
        "¡OPTIMIZACIÓN EMPRESARIAL COMPLETADA!"
    ]
    color_estado = [MUTED_GRAY, ACCENT_CYAN, ACCENT_ORANGE, ACCENT_ORANGE, ACCENT_GREEN][simulador.fase]
    txt_estado = font_main.render(f"Estado: {estado_strs[simulador.fase]}", True, color_estado)
    screen.blit(txt_estado, (35, 52))

    # 2. PANEL IZQUIERDO: RED LOGÍSTICA DE LA EMPRESA
    pygame.draw.rect(screen, PANEL_BG, (20, 95, 620, 630), border_radius=8)
    pygame.draw.rect(screen, (30, 45, 70), (20, 95, 620, 630), 1, border_radius=8)
    
    for i in range(0, simulador.n_vars, 3):
        p1 = simulador.nodos_pos[i]
        p2 = simulador.nodos_pos[(i + 7) % simulador.n_vars]
        pygame.draw.line(screen, (30, 50, 80), p1, p2, 1)

    for i, pos in enumerate(simulador.nodos_pos):
        val = simulador.v_continuas[i]
        if simulador.fase == FASE_COMPLETADO:
            color_nodo = ACCENT_GREEN if simulador.v_discretas[i] == 1 else (100, 100, 100)
        else:
            r = int(255 * (1 - val))
            g = int(255 * val)
            color_nodo = (r, g, 150)
            
        pygame.draw.circle(screen, color_nodo, (int(pos[0]), int(pos[1])), 7)
        pygame.draw.circle(screen, TEXT_COLOR, (int(pos[0]), int(pos[1])), 7, 1)

    txt_grafo = font_main.render("Red de Nodos Logísticos (Centros y Vehículos)", True, MUTED_GRAY)
    screen.blit(txt_grafo, (40, 110))

    # 3. PANEL DERECHO: DATOS Y TELEMETRÍA DE LA EMPRESA (Sin funciones anidadas para evitar errores)
    pygame.draw.rect(screen, PANEL_BG, (650, 95, 430, 630), border_radius=8)
    pygame.draw.rect(screen, (30, 45, 70), (650, 95, 430, 630), 1, border_radius=8)

    y_offset = 110

    # Dato 1: Vehículos
    lbl = font_small.render("VEHÍCULOS ACTIVOS EN FLOTA", True, MUTED_GRAY)
    val = font_main.render(str(DATOS_EMPRESA_FALSA["vehiculos_disponibles"]), True, ACCENT_CYAN)
    screen.blit(lbl, (670, y_offset))
    screen.blit(val, (670, y_offset + 16))
    y_offset += 45

    # Dato 2: Pedidos
    lbl = font_small.render("PEDIDOS URGENTES A DISTRIBUIR", True, MUTED_GRAY)
    val = font_main.render(str(DATOS_EMPRESA_FALSA["pedidos_urgentes"]), True, ACCENT_CYAN)
    screen.blit(lbl, (670, y_offset))
    screen.blit(val, (670, y_offset + 16))
    y_offset += 45

    # Dato 3: Centros
    lbl = font_small.render("CENTROS LOGÍSTICOS", True, MUTED_GRAY)
    val = font_main.render(", ".join(DATOS_EMPRESA_FALSA["centros_distribucion"]), True, TEXT_COLOR)
    screen.blit(lbl, (670, y_offset))
    screen.blit(val, (670, y_offset + 16))
    y_offset += 45

    # Dato 4: Conflictos
    lbl = font_small.render("CONFLICTOS / RESTRICCIONES ROTAS", True, MUTED_GRAY)
    color_viol = ACCENT_RED if simulador.violaciones > 0 else ACCENT_GREEN
    val = font_main.render(f"{simulador.violaciones} / {simulador.n_clausulas}", True, color_viol)
    screen.blit(lbl, (670, y_offset))
    screen.blit(val, (670, y_offset + 16))
    y_offset += 45

    # Dato 5: Tiempo
    lbl = font_small.render("TIEMPO DE CÓMPUTO DE RUTA", True, MUTED_GRAY)
    val = font_main.render(f"{simulador.tiempo_transcurrido:.2f} s", True, TEXT_COLOR)
    screen.blit(lbl, (670, y_offset))
    screen.blit(val, (670, y_offset + 16))
    y_offset += 45

    # Gráfica de convergencia de optimización
    pygame.draw.rect(screen, (10, 15, 25), (670, 390, 390, 140), border_radius=6)
    pygame.draw.rect(screen, MUTED_GRAY, (670, 390, 390, 140), 1, border_radius=6)
    txt_graf = font_small.render("Evolución de Costes y Penalizaciones (Loss)", True, MUTED_GRAY)
    screen.blit(txt_graf, (685, 400))

    if len(simulador.historial_energia) > 1:
        puntos_grafica = []
        max_e = max(simulador.historial_energia) if max(simulador.historial_energia) > 0 else 1.0
        for idx_h, en in enumerate(simulador.historial_energia):
            gx = 685 + int(idx_h * (360 / 150))
            gy = 515 - int((en / max_e) * 95)
            puntos_grafica.append((gx, gy))
        if len(puntos_grafica) > 1:
            pygame.draw.aalines(screen, ACCENT_GREEN, False, puntos_grafica, 2)

    # Caja de controles e impacto
    pygame.draw.rect(screen, (22, 32, 52), (670, 545, 390, 160), border_radius=6)
    txt_ctrl1 = font_small.render("[ESPACIO]: Ejecutar Nueva Optimización", True, ACCENT_CYAN)
    txt_ctrl2 = font_small.render("[ESC]: Salir del Sistema", True, MUTED_GRAY)
    txt_ctrl3 = font_small.render("Estado de Negocio: Vinculado a parámetros", True, TEXT_COLOR)
    txt_ctrl4 = font_small.render("de flota y centros de distribución reales.", True, TEXT_COLOR)
    
    screen.blit(txt_ctrl1, (685, 560))
    screen.blit(txt_ctrl2, (685, 580))
    screen.blit(txt_ctrl3, (685, 615))
    screen.blit(txt_ctrl4, (685, 635))

    pygame.display.flip()

pygame.quit()
sys.exit()