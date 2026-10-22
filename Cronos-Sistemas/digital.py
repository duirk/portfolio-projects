import sys
import math
import pygame

# --- INICIALIZACIÓN ---
pygame.init()
WIDTH, HEIGHT = 1100, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Framework: Predicción Temporal por Años (Inicio 2026)")
clock = pygame.time.Clock()

# --- COLORES ---
BG_COLOR = (24, 26, 32)
PANEL_BG = (33, 37, 43)
TEXT_COLOR = (220, 224, 230)
ACCENT_BLUE = (61, 139, 255)
ACCENT_RED = (239, 83, 80)
ACCENT_GREEN = (102, 187, 106)
ACCENT_YELLOW = (255, 202, 40)

FONT_TITLE = pygame.font.SysFont("arial", 20, bold=True)
FONT_BODY = pygame.font.SysFont("arial", 13)
FONT_BOLD = pygame.font.SysFont("arial", 13, bold=True)

# --- BASE DE DATOS HISTÓRICA CON AÑOS DE INICIO ---
HISTORICAL_DATASETS = {
    "Era Digital (2026+)": {
        "start_year": 2026,
        "F": 90.0,   # Datos, Redes y Vector Energético actual
        "H": 3.5,    # Complejidad institucional global
        "R": 2.2,    # Inercia institucional
        "Z": 4.8,    # Entropía e intercambio masivo de información
        "M": 3.2,    # Redes descentralizadas
        "desc": "Simulación prospectiva desde el año 2026 con alta volatilidad en red."
    },
    "Roma (Crisis S. III)": {
        "start_year": 235, # Año de inicio de la Crisis del Siglo III
        "F": 12.0,
        "H": 4.2,
        "R": 1.5,
        "Z": 0.8,
        "M": 1.2,
        "desc": "Inicio de la crisis militar e inflación en el Imperio Romano (235 d.C.)."
    },
    "Rev. Industrial (1800)": {
        "start_year": 1800,
        "F": 65.0,
        "H": 2.1,
        "R": 3.8,
        "Z": 2.1,
        "M": 2.5,
        "desc": "Expansión del carbón y la máquina de vapor en el siglo XIX."
    }
}

class PresetButton:
    def __init__(self, x, y, w, h, text, dataset_key, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.dataset_key = dataset_key
        self.callback = callback
        self.selected = False

    def draw(self, surface):
        color = ACCENT_BLUE if self.selected else (50, 60, 75)
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        txt = FONT_BOLD.render(self.text, True, (255, 255, 255))
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback(self.dataset_key)

class TimeSimulation:
    def __init__(self):
        self.current_dataset = "Era Digital (2026+)"
        
        self.buttons = []
        btn_y = 70
        for name in HISTORICAL_DATASETS.keys():
            btn = PresetButton(35, btn_y, 250, 32, name, name, self.load_dataset)
            self.buttons.append(btn)
            btn_y += 42
        
        self.buttons[0].selected = True
        self.load_dataset(self.current_dataset)

    def load_dataset(self, key):
        self.current_dataset = key
        for btn in self.buttons:
            btn.selected = (btn.dataset_key == key)
            
        data = HISTORICAL_DATASETS[key]
        self.start_year = data["start_year"]
        self.F = data["F"]
        self.H = data["H"]
        self.R = data["R"]
        self.Z = data["Z"]
        self.M = data["M"]
        self.desc = data["desc"]
        
        self.reset()

    def reset(self):
        self.elapsed_years = 0.0
        self.collapse_year = None
        self.tension_history = []
        self.stability_history = []
        self.years_history = []
        self.max_points = 250
        self.estado = "ESTABLE"

    def update(self):
        # Avanza 0.2 años por cada fotograma de simulación
        self.elapsed_years += 0.2
        current_year = int(self.start_year + self.elapsed_years)
        
        # Ecuación del framework con dependencia temporal
        coste_burocratico = self.H * math.exp(0.012 * self.elapsed_years)
        tension = (coste_burocratico + (self.Z * self.F * 0.04)) / self.M
        estabilidad = max(0, (self.F * self.R * 0.1) - (tension * 1.1))

        if tension > self.F * 0.25:
            self.estado = "BIFURCACIÓN CAÓTICA (COLAPSO)"
            if self.collapse_year is None:
                self.collapse_year = current_year
        elif tension > self.F * 0.15:
            self.estado = "CRISIS ESTRUCTURAL"
        else:
            self.estado = "Atracción Magnética (ESTABLE)"

        self.tension_history.append(tension)
        self.stability_history.append(estabilidad)
        self.years_history.append(current_year)

        if len(self.tension_history) > self.max_points:
            self.tension_history.pop(0)
            self.stability_history.pop(0)
            self.years_history.pop(0)

    def draw(self, surface):
        # Panel Izquierdo
        panel_rect = pygame.Rect(20, 20, 280, 680)
        pygame.draw.rect(surface, PANEL_BG, panel_rect, border_radius=10)
        
        surface.blit(FONT_TITLE.render("Selección de Escenario", True, TEXT_COLOR), (35, 30))
        for btn in self.buttons:
            btn.draw(surface)

        # Información del Tiempo y Métricas
        y_off = 210
        current_y = int(self.start_year + self.elapsed_years)
        surface.blit(FONT_BOLD.render(f"Año Actual Simulado: {current_y}", True, ACCENT_BLUE), (35, y_off))
        
        y_off += 30
        if self.collapse_year:
            surface.blit(FONT_BOLD.render(f"Colapso estimado: Año {self.collapse_year}", True, ACCENT_RED), (35, y_off))
        else:
            surface.blit(FONT_BOLD.render("Colapso estimado: No proyectado", True, ACCENT_GREEN), (35, y_off))

        y_off += 35
        surface.blit(FONT_BOLD.render("Parámetros del Sistema:", True, ACCENT_YELLOW), (35, y_off))
        metrics = [
            f"F (Energía): {self.F}",
            f"H (Burocracia): {self.H}",
            f"R (Inercia): {self.R}",
            f"Z (Entropía): {self.Z}",
            f"M (Modularidad): {self.M}"
        ]
        for m in metrics:
            y_off += 22
            surface.blit(FONT_BODY.render(m, True, TEXT_COLOR), (35, y_off))

        # Panel Principal
        main_rect = pygame.Rect(320, 20, 760, 680)
        pygame.draw.rect(surface, PANEL_BG, main_rect, border_radius=10)

        # Encabezado de Estado
        status_color = ACCENT_GREEN if "ESTABLE" in self.estado else (ACCENT_YELLOW if "CRISIS" in self.estado else ACCENT_RED)
        surface.blit(FONT_TITLE.render("Estado Sistémico:", True, TEXT_COLOR), (340, 30))
        surface.blit(FONT_TITLE.render(self.estado, True, status_color), (510, 30))
        surface.blit(FONT_BODY.render(f"Contexto: {self.desc}", True, (170, 180, 190)), (340, 60))

        # Gráfico
        graph_rect = pygame.Rect(340, 95, 720, 530)
        pygame.draw.rect(surface, BG_COLOR, graph_rect, border_radius=8)

        # Leyenda
        surface.blit(FONT_BODY.render("— Tensión (dΨ/dt)", True, ACCENT_RED), (360, 110))
        surface.blit(FONT_BODY.render("— Estabilidad", True, ACCENT_BLUE), (510, 110))

        if len(self.tension_history) > 1:
            pts_t, pts_e = [], []
            max_y = max(max(self.tension_history), max(self.stability_history), 10)
            
            for i in range(len(self.tension_history)):
                x = graph_rect.x + (i / self.max_points) * graph_rect.width
                y_t = graph_rect.bottom - (self.tension_history[i] / max_y) * (graph_rect.height - 40) - 10
                y_e = graph_rect.bottom - (self.stability_history[i] / max_y) * (graph_rect.height - 40) - 10
                
                pts_t.append((x, max(graph_rect.top + 10, y_t)))
                pts_e.append((x, max(graph_rect.top + 10, y_e)))

            pygame.draw.lines(surface, ACCENT_RED, False, pts_t, 2)
            pygame.draw.lines(surface, ACCENT_BLUE, False, pts_e, 2)

        # Eje Horizontal (Marcas de Años)
        if len(self.years_history) > 0:
            year_start_txt = str(self.years_history[0])
            year_end_txt = str(self.years_history[-1])
            surface.blit(FONT_BODY.render(f"Eje X: {year_start_txt}", True, TEXT_COLOR), (340, 635))
            surface.blit(FONT_BODY.render(f"Hasta: {year_end_txt}", True, TEXT_COLOR), (980, 635))

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

def main():
    sim = TimeSimulation()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            sim.handle_event(event)

        sim.update()
        screen.fill(BG_COLOR)
        sim.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()