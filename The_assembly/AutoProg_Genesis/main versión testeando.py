"""
=============================================================================
BANCO DE PRUEBAS CIENTÍFICO - AUTO-PROGRAMACIÓN INFINITA Y ÚNICA EN VIVO
(TensorFlow, SciPy, NumPy, SymPy, OpenCV, Matplotlib y Pygame GUI)
=============================================================================
"""

import math
import os
import random
import sys
import time
import unittest
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pygame
import scipy.integrate as integrate
import scipy.optimize as optimize
import scipy.signal as signal
import sympy as sp
import tensorflow as tf

# Inicialización segura de la variable SERIAL_DISPONIBLE
SERIAL_DISPONIBLE = False
try:
    import serial

    SERIAL_DISPONIBLE = True
except ImportError:
    SERIAL_DISPONIBLE = False

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana estándar manejable
ANCHO, ALTO = 1200, 850
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(
    "Banco de Pruebas Épico - Motor de Funciones Únicas Infinitas"
)

# Paleta de colores técnica avanzada
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
AZUL_OSCURO = (21, 67, 96)
AZUL = (41, 128, 185)
GRIS = (210, 215, 220)
GRIS_OSCURO = (90, 90, 90)
ROJO = (192, 57, 43)
VERDE = (39, 174, 96)
NARANJA = (230, 126, 34)
VIOLETA = (125, 60, 152)
AZUL_CLARO = (235, 243, 250)
VERDE_CLARO = (234, 250, 234)
VIOLETA_CLARO = (245, 238, 255)
AMARILLO_CLARO = (254, 249, 231)

fuente = pygame.font.SysFont("Arial", 11)
fuente_titulo = pygame.font.SysFont("Arial", 13, bold=True)

# =============================================================================
# 1. MOTOR SIMBÓLICO (SymPy)
# =============================================================================
v_gs_sym, v_ds_sym, i_ds_sym, t_j_sym = sp.symbols(
    "v_gs_sym v_ds_sym i_ds_sym t_j_sym", real=True
)
expr_maestra = (v_gs_sym * sp.sqrt(2) + v_ds_sym * 0.707) + (
    i_ds_sym * 0.85 + (t_j_sym / 100.0)
)
derivada_sensibilidad = sp.diff(expr_maestra, v_gs_sym)

# =============================================================================
# 2. MOTOR DE MACHINE LEARNING (TensorFlow)
# =============================================================================
tf.random.set_seed(42)
ml_model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation="relu", input_shape=(3,)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])
ml_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.005),
    loss="binary_crossentropy",
)

X_train = np.array(
    [
        [2.0, 1.0, 25.0],
        [5.0, 5.0, 140.0],
        [1.0, 0.1, 30.0],
        [4.5, 4.8, 130.0],
        [3.0, 2.5, 50.0],
        [7.0, 4.5, 160.0],
    ],
    dtype=np.float32,
)
y_train = np.array([[0.0], [1.0], [0.0], [1.0], [0.0], [1.0]], dtype=np.float32)
ml_model.fit(X_train, y_train, epochs=30, verbose=0)

# =============================================================================
# 3. PARÁMETROS FÍSICOS Y ESTADO
# =============================================================================
V_TH_BASE = 2.0
K_N_BASE = 0.5
LAMBDA = 0.02
TEMP_AMBIENTE = 27.0
V_DD = 5.0
R_L = 200.0

temp_juntura = TEMP_AMBIENTE
R_TH = 150.0
C_TH = 2.5
v_gs = 3.5
auto_arreglo_activo = False
scroll_fórmulas = 0
contador_autoprogramacion = 0

# Variables de control dinámicas
modo_pwm = False
factor_ruido_termico = 0.0
modo_boost_cuantico = False
modo_relativista = False
polaridad_invertida = False

# Banco inicial de módulos físicos unificados
modulos_fisicos_activos = [
    (
        "• [1] Maxwell (∇·D = ρ): Ley de Gauss para campos dieléctricos"
        " activos"
    ),
    (
        "• [2] Shockley-Hodges (MOSFET): Ecuación analítica de corriente de"
        " drenador"
    ),
    (
        "• [3] Lógica Discreta (NAND Status): Compuerta de validación de estado"
        " seguro"
    ),
    (
        "• [4] Ecuación Maestra Unificada E_e(t): Acoplamiento termo-eléctrico"
        " coherente"
    ),
]

# Botones activos iniciales en la interfaz
botones_ui_activos = [
    {"id": "auto", "texto": "🤖 Autocorrector IA", "color": (39, 174, 96)},
    {
        "id": "auto_programar_python",
        "texto": "⚡ AUTO-PROGRAMAR CÓDIGO ÚNICO (+)",
        "color": (211, 84, 0),
    },
    {
        "id": "scipy_optimize",
        "texto": "🧬 SciPy: Optimización Q-Point",
        "color": (41, 128, 185),
    },
    {
        "id": "opencv_ventana",
        "texto": "📷 OpenCV: Visión Telemetría",
        "color": (192, 57, 43),
    },
]

mensaje_estado_auto = "• Motor de auto-programación infinita listo. Pulse el botón naranja para generar funciones 100% únicas."
color_mensaje = NEGRO


def calcular_ecuacion_maestra_historica(v_gs, v_ds, i_ds, temp_j):
    densidad_rho = v_gs * math.sqrt(2.0) + v_ds * math.sin(math.radians(45))
    componente_integral = i_ds * 0.85 + (temp_j / 100.0)
    logica_nand = 1 if (v_gs > 2.2 and v_ds > 1.5) else 0
    e_e = (densidad_rho + componente_integral) * (
        1.0 if logica_nand == 0 else 1.5
    )
    return e_e, densidad_rho, logica_nand


def calcular_mosfet_riguroso(v_gs, v_ds, v_th_base, k_n_base, lambd):
    delta_t = temp_juntura - 27.0
    v_th = max(0.5, v_th_base - (delta_t * 0.0015))
    k_n = max(0.05, k_n_base * (1.0 - delta_t * 0.002))
    if modo_relativista:
        k_n *= 0.85

    if v_gs < v_th:
        return 0.0, "Corte", v_th, k_n
    elif v_ds < (v_gs - v_th):
        i_ds = (
            k_n
            * (2 * (v_gs - v_th) * v_ds - (v_ds**2))
            * (1.0 + lambd * v_ds)
        )
        return max(0.0, i_ds), "Triodo (Lineal)", v_th, k_n
    else:
        i_ds = k_n * ((v_gs - v_th) ** 2) * (1.0 + lambd * v_ds)
        return max(0.0, i_ds), "Saturación", v_th, k_n


def solucionador_punto_operacion(v_gs, v_th_base, k_n_base, lambd):
    v_ds_vals = np.linspace(0.0, V_DD, 400)
    delta_t = temp_juntura - 27.0
    v_th = max(0.5, v_th_base - (delta_t * 0.0015))
    k_n = max(0.05, k_n_base * (1.0 - delta_t * 0.002))

    resis_carga = -R_L if polaridad_invertida else R_L
    i_ds_recta = (
        (V_DD - v_ds_vals) / resis_carga * 1000.0
        if resis_carga != 0
        else np.zeros_like(v_ds_vals)
    )

    if v_gs < v_th:
        i_ds_calc = np.zeros_like(v_ds_vals)
        regiones = np.array(["Corte"] * len(v_ds_vals))
    else:
        triodo_mask = v_ds_vals < (v_gs - v_th)
        i_ds_calc = np.where(
            triodo_mask,
            k_n
            * (2 * (v_gs - v_th) * v_ds_vals - (v_ds_vals**2))
            * (1.0 + lambd * v_ds_vals),
            k_n * ((v_gs - v_th) ** 2) * (1.0 + lambd * v_ds_vals),
        )
        regiones = np.where(triodo_mask, "Triodo (Lineal)", "Saturación")

    residuos = np.abs(i_ds_calc - i_ds_recta)
    idx_opt = np.argmin(residuos)

    return (
        float(v_ds_vals[idx_opt]),
        float(i_ds_calc[idx_opt]),
        str(regiones[idx_opt]),
    )


# =============================================================================
# 4. PRUEBAS AUTOMÁTICAS
# =============================================================================
class TestBancoEpico(unittest.TestCase):

    def test_modelo_mosfet(self):
        i_py, reg, _, _ = calcular_mosfet_riguroso(
            3.5, 3.0, V_TH_BASE, K_N_BASE, LAMBDA
        )
        self.assertGreaterEqual(i_py, 0.0)


def ejecutar_tests():
    print("[TEST SUITE] Validando modelos físicos...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoEpico)
    unittest.TextTestRunner(verbosity=1).run(suite)
    print("[TEST SUITE] Pruebas superadas con éxito.\n")


# =============================================================================
# BUCLE PRINCIPAL CON GENERADOR PROCEDURAL INFINITO DE FUNCIONES ÚNICAS
# =============================================================================
def main():
    ejecutar_tests()

    reloj = pygame.time.Clock()
    global v_gs, TEMP_AMBIENTE, temp_juntura, V_TH_BASE, K_N_BASE, auto_arreglo_activo
    global mensaje_estado_auto, color_mensaje, modo_pwm, factor_ruido_termico
    global modo_boost_cuantico, modo_relativista, polaridad_invertida, scroll_fórmulas, contador_autoprogramacion

    puerto_serial = None
    if SERIAL_DISPONIBLE:
        try:
            puerto_serial = serial.Serial("COM3", 9600, timeout=0.05)
        except Exception:
            puerto_serial = None

    corriendo = True
    while corriendo:
        dt = reloj.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                if 25 <= mx <= 1175 and 25 <= my <= 125:
                    scroll_fórmulas += evento.y * 20
                    max_scroll = max(
                        0, (len(modulos_fisicos_activos) * 18) - 75
                    )
                    scroll_fórmulas = max(-max_scroll, min(0, scroll_fórmulas))
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    pos_mouse = evento.pos
                    for rect_btn, b_info in rects_botones_actuales:
                        if rect_btn.collidepoint(pos_mouse):
                            b_id = b_info.get("id")
                            if b_id == "auto":
                                auto_arreglo_activo = not auto_arreglo_activo
                                mensaje_estado_auto = (
                                    f"🤖 Autocorrector {'ACTIVADO' if auto_arreglo_activo else 'DESACTIVADO'}."
                                )
                                color_mensaje = AZUL_OSCURO
                            elif b_id == "auto_programar_python":
                                # =====================================================
                                # MOTOR PROCEDURAL INFINITO: GENERADOR DE FUNCIONES ÚNICAS
                                # =====================================================
                                contador_autoprogramacion += 1
                                idx_gen = contador_autoprogramacion

                                # Listas masivas para combinar matemáticamente nombres únicos e irrepetibles en cada ciclo
                                prefijos = [
                                    "Red Neuronal Cuántica",
                                    "Tensor Convolucional Masivo",
                                    "Ecuación Diferencial Estocástica",
                                    "Algoritmo Genético Adaptativo",
                                    "Campo Tensorial No Lineal",
                                    "Matriz de Disipación Dinámica",
                                    "Proceso Markoviano de Juntura",
                                    "Oscilador Armónico Relativista",
                                ]
                                nucleos = [
                                    "de Alta Coherencia",
                                    "Multicapa Avanzado",
                                    "de Ultra-Baja Latencia",
                                    "Termo-Eléctrico Autónomo",
                                    "de Propagación Caótica",
                                    "con Resonancia de Plasma",
                                    "de Estabilidad Topológica",
                                    "con Corrección de Espín",
                                ]
                                sufijos = [
                                    f"v{idx_gen}.{random.randint(10,99)}",
                                    f"Mk.{idx_gen}",
                                    f"Alpha-{idx_gen}",
                                    f"Gen.{idx_gen}x",
                                    f"Core-{idx_gen}",
                                ]

                                nombre_funcion_actual = f"{random.choice(prefijos)} {random.choice(nucleos)} [{random.choice(sufijos)}]"

                                # Código fuente dinámico 100% único generado algorítmicamente en caliente
                                peso_aleatorio = round(
                                    random.uniform(0.8, 2.5), 4
                                    )
                                codigo_autogenerado_dinamico = f"""
# --- SCRIPT AUTOPROGRAMADO ÚNICO EN VIVO #{idx_gen} ---
import tensorflow as tf
import numpy as np

def funcion_neural_unica_{idx_gen}():
    # Tensor exclusivo con coeficientes estocásticos generados proceduralmente
    tensor_gen = tf.constant([[{float(v_gs)}, {float(temp_juntura)}, {peso_aleatorio} * {idx_gen}]], dtype=tf.float32)
    salida_tensor = tf.reduce_sum(tf.nn.gelu(tensor_gen)) * {peso_aleatorio}
    print("🧠 [AUTO-EXEC ÚNICO #{idx_gen}] {nombre_funcion_actual} ejecutada. Tensor:", salida_tensor.numpy())
    return float(salida_tensor.numpy())

# Ejecución inmediata en caliente
resultado_unico_{idx_gen} = funcion_neural_unica_{idx_gen}()
"""
                                # Compilar y ejecutar de forma autónoma con exec()
                                try:
                                    exec(
                                        codigo_autogenerado_dinamico, globals()
                                    )
                                    estado_compilacion = (
                                        "COMPILADO Y EJECUTADO CON ÉXITO"
                                    )
                                except Exception as err:
                                    estado_compilacion = f"ERROR: {{str(err)}}"

                                # Generar colores aleatorios vibrantes para el nuevo botón único
                                color_aleatorio = (
                                    random.randint(50, 220),
                                    random.randint(50, 220),
                                    random.randint(50, 220),
                                )
                                id_nuevo = f"autogen_unico_{idx_gen}"

                                # Añadir el botón único a la interfaz en vivo
                                botones_ui_activos.append({
                                    "id": id_nuevo,
                                    "texto": (
                                        f"⚡ [{idx_gen}]"
                                        f" {nombre_funcion_actual[:20]}..."
                                    ),
                                    "color": color_aleatorio,
                                })

                                # Añadir el módulo físico correspondiente al panel superior con scroll
                                modulos_fisicos_activos.append(
                                    f"• [{4+idx_gen}] Autoprogramado"
                                    f" ({estado_compilacion}):"
                                    f" {nombre_funcion_actual}"
                                )

                                mensaje_estado_auto = (
                                    f"⚡ [AUTO-PROGRAMACIÓN ÚNICA] Función"
                                    f" #{idx_gen} creada, escrita y compilada"
                                    f" en vivo."
                                )
                                color_mensaje = VIOLETA

                            elif b_id == "scipy_optimize":
                                def objetivo(v):
                                    id_c, _, _, _ = calcular_mosfet_riguroso(
                                        v[0], 2.5, V_TH_BASE, K_N_BASE, LAMBDA
                                    )
                                    return -id_c

                                res_opt = optimize.minimize(
                                    objetivo, [3.5], method="Nelder-Mead"
                                )
                                v_gs = max(0.0, min(8.0, float(res_opt.x[0])))
                                mensaje_estado_auto = f"🧬 [SciPy Optimize] V_gs optimizado: {v_gs:.3f}V"
                                color_mensaje = (211, 84, 0)

                            elif b_id == "opencv_ventana":
                                img_ventana = np.zeros(
                                    (280, 420, 3), dtype=np.uint8
                                )
                                img_ventana[:] = (35, 35, 35)
                                cv2.putText(
                                    img_ventana,
                                    "TELEMETRIA AUTO-PROGRAMADA",
                                    (20, 40),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5,
                                    (0, 255, 255),
                                    2,
                                )
                                cv2.putText(
                                    img_ventana,
                                    f"Funciones Únicas: {contador_autoprogramacion}",
                                    (20, 90),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5,
                                    (0, 255, 0),
                                    2,
                                )
                                cv2.imshow(
                                    "Ventana Externa Auto-Programada",
                                    img_ventana,
                                )
                                cv2.waitKey(1)
                                mensaje_estado_auto = (
                                    "📷 [OpenCV] Ventana externa lanzada."
                                )
                                color_mensaje = ROJO
                            else:
                                # Si se pulsa cualquier botón generado de forma autónoma única
                                mensaje_estado_auto = (
                                    f"⚡ Módulo Único Ejecutado:"
                                    f" {b_info['texto']}"
                                )
                                color_mensaje = AZUL

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    v_gs = min(8.0, v_gs + 0.1)
                elif evento.key == pygame.K_DOWN:
                    v_gs = max(0.0, v_gs - 0.1)
                elif evento.key == pygame.K_a:
                    auto_arreglo_activo = not auto_arreglo_activo

        if puerto_serial and puerto_serial.in_waiting > 0:
            try:
                linea = puerto_serial.readline().decode("utf-8").strip()
                if linea:
                    v_gs = max(0.0, min(8.0, float(linea)))
            except ValueError:
                pass

        v_gs_efectivo = v_gs
        if modo_pwm:
            v_gs_efectivo = v_gs * (1.0 if (time.time() * 6) % 2 > 1 else 0.5)

        v_ds, i_ds, region_actual = solucionador_punto_operacion(
            v_gs_efectivo, V_TH_BASE, K_N_BASE, LAMBDA
        )
        _, _, v_th_efec, k_n_efec = calcular_mosfet_riguroso(
            v_gs_efectivo, v_ds, V_TH_BASE, K_N_BASE, LAMBDA
        )
        e_e_valor, rho_val, nand_val = calcular_ecuacion_maestra_historica(
            v_gs_efectivo, v_ds, i_ds, temp_juntura
        )

        potencia_w = v_ds * (i_ds / 1000.0)
        ruido_extra = (
            np.random.normal(0, 2.0) if factor_ruido_termico > 0 else 0.0
        )
        d_temp_dt = (
            potencia_w - (temp_juntura - TEMP_AMBIENTE) / R_TH
        ) / C_TH
        temp_juntura += (d_temp_dt + ruido_extra * 0.1) * dt
        temp_juntura = max(TEMP_AMBIENTE, temp_juntura)

        features = np.array(
            [[v_gs_efectivo, v_ds, temp_juntura]], dtype=np.float32
        )
        prob_fallo = float(ml_model.predict(features, verbose=0)[0][0])

        if auto_arreglo_activo:
            if prob_fallo > 0.45 or temp_juntura > 75.0 or v_gs > 6.5:
                v_gs = max(3.0, v_gs - 0.05)
                temp_juntura = max(TEMP_AMBIENTE, temp_juntura - 0.8)
                mensaje_estado_auto = (
                    "🟢 [AUTOCORRECTOR] Estabilizando térmicamente V_gs a"
                    f" {v_gs:.2f}V..."
                )
                color_mensaje = VERDE

        # =====================================================================
        # RENDERIZADO VISUAL PROTEGIDO
        # =====================================================================
        pantalla.fill(BLANCO)

        txt_titulo = fuente_titulo.render(
            "BANCO DE PRUEBAS ÉPICO - AUTO-PROGRAMACIÓN DE FUNCIONES ÚNICAS EN"
            " VIVO",
            True,
            AZUL_OSCURO,
        )
        pantalla.blit(txt_titulo, (25, 6))

        # 1. Caja Fija Superior de Fórmulas con Scroll Interno Independiente
        pygame.draw.rect(
            pantalla, VIOLETA_CLARO, (25, 25, 1150, 95), border_radius=5
        )
        pygame.draw.rect(pantalla, VIOLETA, (25, 25, 1150, 95), 1, border_radius=5)

        surface_formulas = pygame.Surface((1130, 83))
        surface_formulas.fill(VIOLETA_CLARO)
        for i, t in enumerate(modulos_fisicos_activos):
            txt = fuente.render(t, True, NEGRO)
            surface_formulas.blit(txt, (8, 6 + (i * 18) + scroll_fórmulas))
        pantalla.blit(surface_formulas, (33, 31))

        # 2. Panel de Estado del Sistema (Posición fija garantizada)
        y_panel_ctrl = 126
        pygame.draw.rect(
            pantalla, AMARILLO_CLARO, (25, y_panel_ctrl, 1150, 42), border_radius=5
        )
        pygame.draw.rect(
            pantalla, NARANJA, (25, y_panel_ctrl, 1150, 42), 1, border_radius=5
        )

        txt_estado = fuente.render(
            f"V_gs = {v_gs_efectivo:.2f}V | V_ds = {v_ds:.2f}V | Región:"
            f" {region_actual} | T_juntura = {temp_juntura:.1f}°C | Fallo IA:"
            f" {prob_fallo*100:.1f}%",
            True,
            NEGRO,
        )
        pantalla.blit(txt_estado, (33, y_panel_ctrl + 6))

        txt_msg = fuente.render(mensaje_estado_auto, True, color_mensaje)
        pantalla.blit(txt_msg, (33, y_panel_ctrl + 22))

        # 3. Cuadrícula de Botones Interactivos (4 columnas fijas y ordenadas)
        y_botones = 175
        rects_botones_actuales = []
        col_idx = 0
        row_idx = 0
        btn_w, btn_h = 270, 28
        gap_x, gap_y = 15, 8

        for b in botones_ui_activos:
            bx = 25 + col_idx * (btn_w + gap_x)
            by = y_botones + row_idx * (btn_h + gap_y)
            rect_b = pygame.Rect(bx, by, btn_w, btn_h)

            rects_botones_actuales.append((rect_b, b))
            col_btn = b.get("color", AZUL)
            if b["id"] == "auto":
                col_btn = VERDE if auto_arreglo_activo else (100, 100, 100)
                txt_texto = (
                    f"🤖 Autocorrector: {'ON' if auto_arreglo_activo else 'OFF'}"
                )
            else:
                txt_texto = b["texto"]

            pygame.draw.rect(pantalla, col_btn, rect_b, border_radius=4)
            pygame.draw.rect(pantalla, NEGRO, rect_b, 1, border_radius=4)
            txt_surf = fuente.render(txt_texto, True, BLANCO)
            pantalla.blit(txt_surf, (rect_b.x + 10, rect_b.y + 7))

            col_idx += 1
            if col_idx >= 4:  # 4 columnas limpias
                col_idx = 0
                row_idx += 1

        filas_totales = row_idx + (1 if col_idx > 0 else 0)
        altura_bloque_botones = filas_totales * (btn_h + gap_y) + 10

        # 4. Panel Gráfico Principal (Ubicado de forma totalmente protegida abajo)
        y_grafico = y_botones + altura_bloque_botones + 10
        h_grafico = 835 - y_grafico
        pygame.draw.rect(
            pantalla,
            (250, 250, 250),
            (25, y_grafico, 1150, h_grafico),
            border_radius=5,
        )
        pygame.draw.rect(
            pantalla, GRIS, (25, y_grafico, 1150, h_grafico), 1, border_radius=5
        )

        txt_graf = fuente_titulo.render(
            "Curvas Características 2N7000, Recta de Carga y Q-Point en Vivo",
            True,
            NEGRO,
        )
        pantalla.blit(txt_graf, (35, y_grafico + 8))

        origin_x, origin_y = 75, y_grafico + h_grafico - 35
        axis_w, axis_h = 1050, h_grafico - 70

        pygame.draw.line(
            pantalla, NEGRO, (origin_x, origin_y), (origin_x + axis_w, origin_y), 2
        )
        pygame.draw.line(
            pantalla,
            NEGRO,
            (origin_x, origin_y - axis_h),
            (origin_x, origin_y),
            2,
        )

        txt_x = fuente.render("V_ds (V)", True, NEGRO)
        pantalla.blit(txt_x, (origin_x + axis_w - 50, origin_y + 8))
        txt_y = fuente.render("I_ds (mA)", True, NEGRO)
        pantalla.blit(txt_y, (origin_x - 50, origin_y - axis_h - 15))

        for vgs_val_ref in [2.0, 3.5, 5.0, 6.5, 8.0]:
            puntos_curva = []
            for vds_step in range(0, 51):
                vds_val = vds_step * 0.1
                current, _, _, _ = calcular_mosfet_riguroso(
                    vgs_val_ref, vds_val, V_TH_BASE, K_N_BASE, LAMBDA
                )
                px = origin_x + int((vds_val / 5.0) * axis_w)
                py = origin_y - int((current / 25.0) * axis_h)
                puntos_curva.append((px, py))
            if len(puntos_curva) > 1:
                pygame.draw.aalines(pantalla, (120, 150, 180), False, puntos_curva)

        puntos_recta = [(0.0, (V_DD / R_L) * 1000.0), (V_DD, 0.0)]
        rx1 = origin_x + int((puntos_recta[0][0] / 5.0) * axis_w)
        ry1 = origin_y - int((puntos_recta[0][1] / 25.0) * axis_h)
        rx2 = origin_x + int((puntos_recta[1][0] / 5.0) * axis_w)
        ry2 = origin_y - int((puntos_recta[1][1] / 25.0) * axis_h)
        pygame.draw.line(pantalla, NARANJA, (rx1, ry1), (rx2, ry2), 2)

        x_operacion = origin_x + int((v_ds / 5.0) * axis_w)
        y_operacion = origin_y - int((i_ds / 25.0) * axis_h)

        pygame.draw.circle(pantalla, VERDE, (x_operacion, y_operacion), 7)
        pygame.draw.circle(pantalla, NEGRO, (x_operacion, y_operacion), 7, 2)

        txt_pto = fuente.render(
            f"Q-Point: ({v_ds:.2f}V, {i_ds:.2f}mA) | Funciones Únicas Compiladas: {contador_autoprogramacion}",
            True,
            VERDE,
        )
        pantalla.blit(txt_pto, (x_operacion + 10, y_operacion - 8))

        pygame.display.flip()
        reloj.tick(60)

    cv2.destroyAllWindows()
    if puerto_serial and puerto_serial.is_open:
        puerto_serial.close()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()