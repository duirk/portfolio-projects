import pygame
import random
import math
import sys

# Inicializar Pygame
pygame.init()
WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PUNTURUM  - Motor Financiero y Gráfica Contable")
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
INPUT_BG = (28, 38, 58)
INPUT_ACTIVE = (40, 60, 95)

# Fuentes
font_title = pygame.font.SysFont("Consolas", 20, bold=True)
font_main = pygame.font.SysFont("Consolas", 14)
font_small = pygame.font.SysFont("Consolas", 11)

# ==========================================
# ESTADOS DE LA APLICACIÓN
# ==========================================
ESTADO_CONFIGURACION = 0
ESTADO_SIMULACION = 1
estado_actual = ESTADO_CONFIGURACION

# Subvistas en simulación
VISTA_LOGISTICA = 0
VISTA_FINANCIERA = 1
vista_actual = VISTA_LOGISTICA

# Campos iniciales ampliados con datos contables y logísticos
config_campos = [
    {"label": "Empresa", "valor": "Logística Global Punturum S.A."},
    {"label": "Vehículos", "valor": "12"},
    {"label": "Pedidos Urgentes", "valor": "45"},
    {"label": "Centros", "valor": "Madrid, Barcelona, Valencia, Sevilla"},
    {"label": "Activo Corriente", "valor": "71180"},
    {"label": "Activo No Corriente", "valor": "273500"},
    {"label": "Pasivo Corriente", "valor": "41100"},
    {"label": "Pasivo No Corriente", "valor": "205000"},
    {"label": "Capital Social", "valor": "50000"},
    {"label": "Utilidades Acumuladas", "valor": "48580"}
]

focus_idx = 0
focus_part = "valor"
DATOS_EMPRESA_PROCESADOS = {}

# ==========================================
# SIMULADOR INDUSTRIAL Y FINANCIERO
# ==========================================
FASE_INICIAL = 0
FASE_RELAJACION = 1
FASE_PERTURBACION = 2
FASE_ATERRIZAJE = 3
FASE_COMPLETADO = 4

class SimuladorEmpresaHito:
    def __init__(self, datos):
        self.datos = datos
        
        total_vehiculos = 0
        for k, v in datos.items():
            if isinstance(v, (int, float)) and any(palabra in k.lower() for palabra in ["vehículo", "moto", "furgoneta", "camión", "flota"]):
                total_vehiculos += int(v)
        
        if total_vehiculos == 0:
            total_vehiculos = 10

        pedidos = datos.get("Pedidos Urgentes", datos.get("Pedidos", 30))
        if not isinstance(pedidos, (int, float)):
            pedidos = 30

        centros = datos.get("Centros", ["Central"])
        num_centros = len(centros) if isinstance(centros, list) else 1

        self.n_vars = max(20, min(100, int(total_vehiculos * num_centros)))
        self.n_clausulas = max(50, int(pedidos * 3))
        
        self.fase = FASE_INICIAL
        self.epoch = 0
        self.max_epochs = 4000
        self.energia_vuelo = 100.0
        self.violaciones = self.n_clausulas
        self.tiempo_transcurrido = 0.0
        
        self.v_continuas = [random.random() for _ in range(self.n_vars)]
        self.v_discretas = [0 for _ in range(self.n_vars)]
        
        # Extracción segura de valores financieros para el Balance General
        self.act_corr = float(datos.get("Activo Corriente", 71180))
        self.act_no_corr = float(datos.get("Activo No Corriente", 273500))
        self.pas_corr = float(datos.get("Pasivo Corriente", 41100))
        self.pas_no_corr = float(datos.get("Pasivo No Corriente", 205000))
        self.cap_social = float(datos.get("Capital Social", 50000))
        self.util_acum = float(datos.get("Utilidades Acumuladas", 48580))
        
        # Cálculos Financieros Clave
        self.total_activo = self.act_corr + self.act_no_corr
        self.total_pasivo = self.pas_corr + self.pas_no_corr
        self.patrimonio_neto = self.cap_social + self.util_acum
        self.capital_corriente = self.act_corr - self.pas_corr  # Fondo de Maniobra
        
        # Ratios Financieros
        self.razon_circulante = self.act_corr / self.pas_corr if self.pas_corr > 0 else 0.0
        self.endeudamiento = (self.total_pasivo / self.total_activo) * 100 if self.total_activo > 0 else 0.0

        # Generar cláusulas de optimización
        self.clausulas = []
        for _ in range(self.n_clausulas):
            vars_3 = random.sample(range(1, self.n_vars + 1), min(3, self.n_vars))
            while len(vars_3) < 3:
                vars_3.append(vars_3[0])
            l1 = vars_3[0] if random.random() > 0.5 else -vars_3[0]
            l2 = vars_3[1] if random.random() > 0.5 else -vars_3[1]
            l3 = vars_3[2] if random.random() > 0.5 else -vars_3[2]
            self.clausulas.append((l1, l2, l3))
            
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
        self.__init__(self.datos)
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
            
            vuelo_violaciones_count = 0
            for l1, l2, l3 in self.clausulas:
                def get_disc(lit):
                    idx = abs(lit) - 1
                    val = self.v_discretas[idx]
                    return val if lit > 0 else (1 - val)
                
                if get_disc(l1) == 0 and get_disc(l2) == 0 and get_disc(l3) == 0:
                    vuelo_violaciones_count += 1
            
            self.violaciones = vuelo_violaciones_count
            self.fase = FASE_COMPLETADO

simulador = None

# ==========================================
# BUCLE PRINCIPAL DE LA APLICACIÓN
# ==========================================
ejecutando = True
while ejecutando:
    clock.tick(60)
    
    btn_add_rect = pygame.Rect(WIDTH//2 - 300, 550, 180, 36)
    btn_start_rect = pygame.Rect(WIDTH//2 - 100, 550, 400, 36)
    
    rects_campos = []
    if estado_actual == ESTADO_CONFIGURACION:
        y_pos_temp = 150
        for i, campo in enumerate(config_campos):
            if y_pos_temp > 520:
                break
            box_label = pygame.Rect(WIDTH//2 - 370, y_pos_temp, 220, 30)
            box_val = pygame.Rect(WIDTH//2 - 140, y_pos_temp, 390, 30)
            btn_del = pygame.Rect(WIDTH//2 + 260, y_pos_temp, 30, 30)
            rects_campos.append((box_label, box_val, btn_del))
            y_pos_temp += 38

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_actual == ESTADO_CONFIGURACION:
                pos_m = evento.pos
                if btn_add_rect.collidepoint(pos_m):
                    config_campos.append({"label": "Nueva Cuenta", "valor": "0"})
                    focus_idx = len(config_campos) - 1
                    focus_part = "label"
                elif btn_start_rect.collidepoint(pos_m):
                    DATOS_EMPRESA_PROCESADOS = {}
                    for c in config_campos:
                        k = c["label"].strip()
                        v = c["valor"].strip()
                        if v.replace('.', '', 1).isdigit():
                            DATOS_EMPRESA_PROCESADOS[k] = float(v) if '.' in v else int(v)
                        elif "," in v:
                            DATOS_EMPRESA_PROCESADOS[k] = [x.strip() for x in v.split(",")]
                        else:
                            DATOS_EMPRESA_PROCESADOS[k] = v
                                
                    simulador = SimuladorEmpresaHito(DATOS_EMPRESA_PROCESADOS)
                    estado_actual = ESTADO_SIMULACION
                else:
                    for i, (r_label, r_val, r_del) in enumerate(rects_campos):
                        if r_del.collidepoint(pos_m) and len(config_campos) > 1:
                            config_campos.pop(i)
                            focus_idx = max(0, i - 1)
                            break
                        elif r_label.collidepoint(pos_m):
                            focus_idx = i
                            focus_part = "label"
                            break
                        elif r_val.collidepoint(pos_m):
                            focus_idx = i
                            focus_part = "valor"
                            break

        elif evento.type == pygame.KEYDOWN:
            if estado_actual == ESTADO_CONFIGURACION:
                if evento.key == pygame.K_TAB:
                    if focus_part == "label":
                        focus_part = "valor"
                    else:
                        focus_part = "label"
                        focus_idx = (focus_idx + 1) % len(config_campos)
                elif evento.key == pygame.K_RETURN:
                    DATOS_EMPRESA_PROCESADOS = {}
                    for c in config_campos:
                        k = c["label"].strip()
                        v = c["valor"].strip()
                        if v.replace('.', '', 1).isdigit():
                            DATOS_EMPRESA_PROCESADOS[k] = float(v) if '.' in v else int(v)
                        elif "," in v:
                            DATOS_EMPRESA_PROCESADOS[k] = [x.strip() for x in v.split(",")]
                        else:
                            DATOS_EMPRESA_PROCESADOS[k] = v
                                
                    simulador = SimuladorEmpresaHito(DATOS_EMPRESA_PROCESADOS)
                    estado_actual = ESTADO_SIMULACION
                elif evento.key == pygame.K_BACKSPACE:
                    if focus_part == "label" and len(config_campos[focus_idx]["label"]) > 0:
                        config_campos[focus_idx]["label"] = config_campos[focus_idx]["label"][:-1]
                    elif focus_part == "valor" and len(config_campos[focus_idx]["valor"]) > 0:
                        config_campos[focus_idx]["valor"] = config_campos[focus_idx]["valor"][:-1]
                else:
                    if evento.unicode.isprintable() and len(evento.unicode) > 0:
                        if focus_part == "label":
                            config_campos[focus_idx]["label"] += evento.unicode
                        else:
                            config_campos[focus_idx]["valor"] += evento.unicode
                            
            elif estado_actual == ESTADO_SIMULACION:
                if evento.key == pygame.K_SPACE:
                    simulador.reiniciar()
                elif evento.key == pygame.K_f:
                    vista_actual = VISTA_FINANCIERA if vista_actual == VISTA_LOGISTICA else VISTA_LOGISTICA
                elif evento.key == pygame.K_ESCAPE:
                    ejecutando = False

    # --- RENDERIZADO VISUAL ---
    screen.fill(BG_COLOR)

    if estado_actual == ESTADO_CONFIGURACION:
        pygame.draw.rect(screen, PANEL_BG, (WIDTH//2 - 410, 50, 820, 640), border_radius=12)
        pygame.draw.rect(screen, ACCENT_CYAN, (WIDTH//2 - 410, 50, 820, 640), 2, border_radius=12)
        
        txt_t = font_title.render("CONFIGURADOR DE DATOS EMPRESARIALES Y CONTABLES", True, TEXT_COLOR)
        screen.blit(txt_t, (WIDTH//2 - txt_t.get_width()//2, 70))
        
        txt_sub = font_main.render("Personaliza las variables de flota, operaciones y contabilidad general:", True, MUTED_GRAY)
        screen.blit(txt_sub, (WIDTH//2 - txt_sub.get_width()//2, 100))
        
        y_pos = 150
        for i, campo in enumerate(config_campos):
            if y_pos > 520:
                break
                
            is_active_l = (focus_idx == i and focus_part == "label")
            is_active_v = (focus_idx == i and focus_part == "valor")
            
            box_label, box_val, btn_del = rects_campos[i]
            
            pygame.draw.rect(screen, INPUT_ACTIVE if is_active_l else INPUT_BG, box_label, border_radius=4)
            pygame.draw.rect(screen, ACCENT_GREEN if is_active_l else MUTED_GRAY, box_label, 1, border_radius=4)
            txt_l = font_main.render(campo["label"], True, TEXT_COLOR)
            screen.blit(txt_l, (box_label.x + 8, box_label.y + 6))
            
            pygame.draw.rect(screen, INPUT_ACTIVE if is_active_v else INPUT_BG, box_val, border_radius=4)
            pygame.draw.rect(screen, ACCENT_CYAN if is_active_v else MUTED_GRAY, box_val, 1, border_radius=4)
            val_str = ", ".join(campo["valor"]) if isinstance(campo["valor"], list) else str(campo["valor"])
            txt_v = font_main.render(val_str, True, TEXT_COLOR)
            screen.blit(txt_v, (box_val.x + 8, box_val.y + 6))
            
            pygame.draw.rect(screen, (80, 30, 30), btn_del, border_radius=4)
            txt_x = font_main.render("X", True, ACCENT_RED)
            screen.blit(txt_x, (btn_del.centerx - txt_x.get_width()//2, btn_del.centery - txt_x.get_height()//2))
            
            y_pos += 38
            
        pygame.draw.rect(screen, (30, 50, 80), btn_add_rect, border_radius=6)
        txt_add = font_main.render("+ Añadir Dato", True, ACCENT_CYAN)
        screen.blit(txt_add, (btn_add_rect.centerx - txt_add.get_width()//2, btn_add_rect.centery - txt_add.get_height()//2))
        
        pygame.draw.rect(screen, ACCENT_GREEN, btn_start_rect, border_radius=6)
        txt_start = font_main.render("INICIAR SIMULACIÓN Y BALANCE GENERAL", True, (10, 14, 23))
        screen.blit(txt_start, (btn_start_rect.centerx - txt_start.get_width()//2, btn_start_rect.centery - txt_start.get_height()//2))
        
        txt_hint = font_small.render("[Clic]: Editar  |  [TAB]: Cambiar campo  |  [ENTER]: Iniciar motor", True, MUTED_GRAY)
        screen.blit(txt_hint, (WIDTH//2 - txt_hint.get_width()//2, 650))

    elif estado_actual == ESTADO_SIMULACION:
        simulador.tiempo_transcurrido += 1 / 60.0
        simulador.actualizar()

        nombre_empresa_act = "Empresa"
        for k, v in DATOS_EMPRESA_PROCESADOS.items():
            if "empresa" in k.lower():
                nombre_empresa_act = str(v)
                break

        # Cabecera superior
        pygame.draw.rect(screen, PANEL_BG, (20, 20, WIDTH - 40, 60), border_radius=8)
        pygame.draw.rect(screen, ACCENT_CYAN, (20, 20, WIDTH - 40, 60), 1, border_radius=8)
        
        txt_titulo = font_title.render(f"EMPRESA: {nombre_empresa_act} // [F]: Alternar Vista Financiera", True, TEXT_COLOR)
        screen.blit(txt_titulo, (35, 30))
        
        estado_strs = [
            "LISTO (PULSA ESPACIO PARA OPTIMIZAR)", 
            "FASE I: PROCESANDO RESTRICCIONES DE FLOTA...", 
            "FASE II: PERTURBACIÓN Y CÁLCULO DE RUTAS...", 
            "ASIGNANDO RECURSOS...", 
            "¡OPTIMIZACIÓN Y BALANCE COMPLETADOS!"
        ]
        color_estado = [MUTED_GRAY, ACCENT_CYAN, ACCENT_ORANGE, ACCENT_ORANGE, ACCENT_GREEN][simulador.fase]
        txt_estado = font_main.render(f"Estado: {estado_strs[simulador.fase]}", True, color_estado)
        screen.blit(txt_estado, (35, 52))

        if vista_actual == VISTA_LOGISTICA:
            # Panel izquierdo: Red de nodos logística
            pygame.draw.rect(screen, PANEL_BG, (20, 95, 620, 630), border_radius=8)
            pygame.draw.rect(screen, (30, 45, 70), (20, 95, 620, 630), 1, border_radius=8)
            
            for i in range(0, simulador.n_vars, max(1, simulador.n_vars // 15)):
                p1 = simulador.nodos_pos[i]
                p2 = simulador.nodos_pos[(i + 3) % simulador.n_vars]
                pygame.draw.line(screen, (30, 50, 80), p1, p2, 1)

            for i, pos in enumerate(simulador.nodos_pos):
                val = simulador.v_continuas[i]
                if simulador.fase == FASE_COMPLETADO:
                    color_nodo = ACCENT_GREEN if simulador.v_discretas[i] == 1 else (100, 100, 100)
                else:
                    r = int(255 * (1 - val))
                    g = int(255 * val)
                    color_nodo = (r, g, 150)
                    
                pygame.draw.circle(screen, color_nodo, (int(pos[0]), int(pos[1])), 6)
                pygame.draw.circle(screen, TEXT_COLOR, (int(pos[0]), int(pos[1])), 6, 1)

            txt_grafo = font_main.render(f"Red Logística Dinámica (Variables: {simulador.n_vars})", True, MUTED_GRAY)
            screen.blit(txt_grafo, (40, 110))

        else:
            # Vista Financiera y Gráfica Contable Estructural
            pygame.draw.rect(screen, PANEL_BG, (20, 95, 620, 630), border_radius=8)
            pygame.draw.rect(screen, ACCENT_CYAN, (20, 95, 620, 630), 1, border_radius=8)
            
            txt_b_title = font_title.render("ESTRUCTURA CONTABLE Y GRÁFICA PATRIMONIAL", True, ACCENT_CYAN)
            screen.blit(txt_b_title, (40, 115))

            # --- GRÁFICA DE BARRAS APILADAS (Activo vs Pasivo + Patrimonio) ---
            pygame.draw.rect(screen, (12, 18, 30), (40, 155, 580, 180), border_radius=6)
            pygame.draw.rect(screen, MUTED_GRAY, (40, 155, 580, 180), 1, border_radius=6)
            txt_g_title = font_small.render("Gráfica: Ecuación Patrimonial (Activo = Pasivo + Patrimonio)", True, MUTED_GRAY)
            screen.blit(txt_g_title, (55, 165))

            max_val_grafica = max(simulador.total_activo, simulador.total_pasivo + simulador.patrimonio_neto)
            if max_val_grafica == 0: 
                max_val_grafica = 1.0

            # Barra 1: Total Activo
            w_activo = int((simulador.total_activo / max_val_grafica) * 380)
            pygame.draw.rect(screen, ACCENT_CYAN, (140, 205, max(5, w_activo), 24), border_radius=4)
            txt_a_bar = font_small.render(f"ACTIVO: {simulador.total_activo:,.0f}", True, TEXT_COLOR)
            screen.blit(txt_a_bar, (55, 209))

            # Barra 2: Pasivo Total + Patrimonio Neto (Apilados)
            w_pasivo = int((simulador.total_pasivo / max_val_grafica) * 380)
            w_pat = int((simulador.patrimonio_neto / max_val_grafica) * 380)
            
            pygame.draw.rect(screen, ACCENT_RED, (140, 255, max(5, w_pasivo), 24), border_radius=4)
            pygame.draw.rect(screen, ACCENT_GREEN, (140 + w_pasivo, 255, max(5, w_pat), 24), border_radius=4)
            
            txt_p_bar = font_small.render(f"PASIVO: {simulador.total_pasivo:,.0f}", True, TEXT_COLOR)
            screen.blit(txt_p_bar, (55, 259))
            
            txt_net_bar = font_small.render(f"PATRIMONIO: {simulador.patrimonio_neto:,.0f}", True, TEXT_COLOR)
            screen.blit(txt_net_bar, (55, 290))

            # --- GRÁFICA DE CAPITAL CORRIENTE (Fondo de Maniobra) ---
            pygame.draw.rect(screen, (12, 18, 30), (40, 350, 580, 150), border_radius=6)
            pygame.draw.rect(screen, MUTED_GRAY, (40, 350, 580, 150), 1, border_radius=6)
            txt_cc_title = font_small.render("Gráfica: Capital Corriente = Activo Corriente - Pasivo Corriente", True, MUTED_GRAY)
            screen.blit(txt_cc_title, (55, 360))

            max_cc_base = max(simulador.act_corr, simulador.pas_corr) if max(simulador.act_corr, simulador.pas_corr) > 0 else 1.0
            w_ac = int((simulador.act_corr / max_cc_base) * 360)
            w_pc = int((simulador.pas_corr / max_cc_base) * 360)

            pygame.draw.rect(screen, ACCENT_CYAN, (160, 395, max(5, w_ac), 18), border_radius=3)
            txt_ac_lbl = font_small.render(f"Act.Corr: {simulador.act_corr:,.0f}", True, TEXT_COLOR)
            screen.blit(txt_ac_lbl, (55, 395))

            pygame.draw.rect(screen, ACCENT_ORANGE, (160, 430, max(5, w_pc), 18), border_radius=3)
            txt_pc_lbl = font_small.render(f"Pas.Corr: {simulador.pas_corr:,.0f}", True, TEXT_COLOR)
            screen.blit(txt_pc_lbl, (55, 430))

            txt_res_cc = font_main.render(f"Capital Corriente (Fondo Maniobra): {simulador.capital_corriente:,.2f}", True, ACCENT_GREEN)
            screen.blit(txt_res_cc, (55, 465))

            # Resumen textual inferior de composición del Patrimonio Neto
            txt_comp = font_small.render(f"Composición Pat. Neto -> Capital Social ({simulador.cap_social:,.0f}) + Utilidades ({simulador.util_acum:,.0f})", True, MUTED_GRAY)
            screen.blit(txt_comp, (40, 515))

        # Panel derecho: Telemetría y Métricas Financieras Clave
        pygame.draw.rect(screen, PANEL_BG, (650, 95, 430, 630), border_radius=8)
        pygame.draw.rect(screen, (30, 45, 70), (650, 95, 430, 630), 1, border_radius=8)

        y_offset = 110
        lbl_fin_res = font_title.render("INDICADORES FINANCIEROS CLAVE", True, ACCENT_GREEN)
        screen.blit(lbl_fin_res, (670, y_offset))
        y_offset += 35

        metrics = [
            ("CAPITAL CORRIENTE (Fondo Maniobra)", f"{simulador.capital_corriente:,.2f}"),
            ("PATRIMONIO NETO (Activo - Pasivo)", f"{simulador.patrimonio_neto:,.2f}"),
            ("RAZÓN CIRCULANTE (Liquidez)", f"{simulador.razon_circulante:.2f}x"),
            ("NIVEL DE ENDEUDAMIENTO", f"{simulador.endeudamiento:.1f}%")
        ]

        for m_lbl, m_val in metrics:
            l = font_small.render(m_lbl, True, MUTED_GRAY)
            v = font_main.render(m_val, True, ACCENT_CYAN)
            screen.blit(l, (670, y_offset))
            screen.blit(v, (670, y_offset + 16))
            y_offset += 45

        lbl_conf = font_small.render("CONFLICTOS / RESTRICCIONES ROTAS", True, MUTED_GRAY)
        color_viol = ACCENT_RED if simulador.violaciones > 0 else ACCENT_GREEN
        val_conf = font_main.render(f"{simulador.violaciones} / {simulador.n_clausulas}", True, color_viol)
        screen.blit(lbl_conf, (670, y_offset))
        screen.blit(val_conf, (670, y_offset + 16))
        y_offset += 45

        # Gráfica de convergencia de optimización
        pygame.draw.rect(screen, (10, 15, 25), (670, 435, 390, 115), border_radius=6)
        pygame.draw.rect(screen, MUTED_GRAY, (670, 435, 390, 115), 1, border_radius=6)
        txt_graf = font_small.render("Evolución de Costes (Loss de Optimización)", True, MUTED_GRAY)
        screen.blit(txt_graf, (685, 443))

        if len(simulador.historial_energia) > 1:
            puntos_grafica = []
            max_e = max(simulador.historial_energia) if max(simulador.historial_energia) > 0 else 1.0
            for idx_h, en in enumerate(simulador.historial_energia):
                gx = 685 + int(idx_h * (360 / 150))
                gy = 530 - int((en / max_e) * 65)
                puntos_grafica.append((gx, gy))
            if len(puntos_grafica) > 1:
                pygame.draw.aalines(screen, ACCENT_GREEN, False, puntos_grafica, 2)

        pygame.draw.rect(screen, (22, 32, 52), (670, 560, 390, 145), border_radius=6)
        txt_ctrl1 = font_small.render("[ESPACIO]: Reiniciar / Reoptimizar", True, ACCENT_CYAN)
        txt_ctrl2 = font_small.render("[F]: Cambiar Vista (Logística / Gráfica Contable)", True, ACCENT_ORANGE)
        txt_ctrl3 = font_small.render("[ESC]: Salir del Sistema", True, MUTED_GRAY)
        txt_ctrl4 = font_small.render("Gráficas estructurales de balance integradas.", True, TEXT_COLOR)
        
        screen.blit(txt_ctrl1, (685, 575))
        screen.blit(txt_ctrl2, (685, 595))
        screen.blit(txt_ctrl3, (685, 615))
        screen.blit(txt_ctrl4, (685, 650))

    pygame.display.flip()

pygame.quit()
sys.exit()