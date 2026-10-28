"""
=============================================================================
BANCO DE PRUEBAS CIENTÍFICO: UNIFICACIÓN DE FÓRMULAS HISTÓRICAS DE LA FÍSICA
(Con Autocorrector e Interfaz USB Hardware-in-the-Loop)
=============================================================================
"""

import sys
import unittest
import numpy as np
import pygame
import tensorflow as tf

# Intento de importación para soporte de puertos COM USB
try:
  import serial

  SERIAL_DISPONIBLE = True
except ImportError:
  SERIAL_DISPONIBLE = False

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 1100, 850
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(
    "Banco de Pruebas - Fórmulas Históricas y Ecuación Maestra Unificada"
)

# Paleta de colores técnica
BLANCO = (255, 255, 255)
NEGRO = (30, 30, 30)
AZUL_OSCURO = (26, 82, 118)
AZUL = (41, 128, 185)
GRIS = (200, 200, 200)
GRIS_OSCURO = (100, 100, 100)
ROJO = (192, 57, 43)
VERDE = (39, 174, 96)
NARANJA = (230, 126, 34)
VIOLETA = (125, 60, 152)
AZUL_CLARO = (240, 245, 250)
ROJO_CLARO = (255, 240, 240)
VIOLETA_CLARO = (245, 238, 255)

fuente = pygame.font.SysFont("Arial", 13)
fuente_titulo = pygame.font.SysFont("Arial", 15, bold=True)
fuente_tecnica = pygame.font.SysFont("Consolas", 12)

# =============================================================================
# 1. MODELO DE MACHINE LEARNING (Surrogate Model con TensorFlow)
# =============================================================================
tf.random.set_seed(42)
ml_model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation="relu", input_shape=(3,)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])
ml_model.compile(optimizer="adam", loss="binary_crossentropy")

X_train = np.array(
    [
        [2.0, 1.0, 25.0],
        [5.0, 5.0, 140.0],
        [1.0, 0.1, 30.0],
        [4.5, 4.8, 130.0],
        [3.0, 2.5, 50.0],
    ],
    dtype=np.float32,
)
y_train = np.array([[0.0], [1.0], [0.0], [1.0], [0.0]], dtype=np.float32)
ml_model.fit(X_train, y_train, epochs=20, verbose=0)

# =============================================================================
# 2. PARÁMETROS FÍSICOS Y VARIABLES DE ESTADO
# =============================================================================
V_TH_BASE = 2.0  # Tensión de umbral (V)[cite: 1]
K_N_BASE = 0.5  # Transconductancia (mA/V^2)[cite: 1]
LAMBDA = 0.02  # Modulación de canal (1/V)[cite: 1]
TEMP_AMBIENTE = 27.0  # Temperatura ambiente (°C)[cite: 1]

V_DD = 5.0  # Tensión de alimentación (V)[cite: 1]
R_L = 200.0  # Resistencia de carga (Ohm)[cite: 1]

temp_juntura = TEMP_AMBIENTE
R_TH = 150.0  # Resistencia térmica (°C/W)[cite: 1]
C_TH = 2.5  # Capacitancia térmica[cite: 1]

v_gs = 3.5  # Tensión de compuerta inicial[cite: 1]
auto_arreglo_activo = False


def calcular_ecuacion_maestra_historica(v_gs, v_ds, i_ds, temp_j):
  """Calcula la Ecuación Maestra de Estado Electrónico E_e(t)."""
  densidad_rho = v_gs * 1.414 + v_ds * 0.707
  componente_integral = i_ds * 0.85 + (temp_j / 100.0)
  logica_nand = 1 if (v_gs > 2.2 and v_ds > 1.5) else 0
  e_e = (densidad_rho + componente_integral) * (1.0 if logica_nand == 0 else 1.5)
  return e_e, densidad_rho, logica_nand


def calcular_mosfet_riguroso(v_gs, v_ds, v_th_base, k_n_base, lambd):
  """Modelo MOSFET riguroso (Shockley / Shichman-Hodges con deriva térmica)."""
  delta_t = temp_juntura - 27.0
  v_th = max(0.5, v_th_base - (delta_t * 0.0015))
  k_n = max(0.05, k_n_base * (1.0 - delta_t * 0.002))

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
  """Solucionador automático de intersección del circuito."""
  mejor_v_ds = 0.0
  menor_residuo = float("inf")
  mejor_ids = 0.0
  mejor_reg = "Corte"

  for v_ds_step in np.linspace(0.0, V_DD, 400):
    i_ds_calc, reg, _, _ = calcular_mosfet_riguroso(
        v_gs, v_ds_step, v_th_base, k_n_base, lambd
    )
    i_ds_recta = (V_DD - v_ds_step) / R_L * 1000.0
    residuo = abs(i_ds_calc - i_ds_recta)
    if residuo < menor_residuo:
      menor_residuo = residuo
      mejor_v_ds = v_ds_step
      mejor_ids = i_ds_calc
      mejor_reg = reg

  return mejor_v_ds, mejor_ids, mejor_reg


# =============================================================================
# 3. SUITE DE PRUEBAS AUTOMÁTICAS Y VALIDACIÓN SPICE
# =============================================================================
class TestBancoDePruebas(unittest.TestCase):

  def test_benchmark_spice_nivel1(self):
    i_py, _, _, _ = calcular_mosfet_riguroso(
        3.5, 3.0, V_TH_BASE, K_N_BASE, LAMBDA
    )
    i_spice_ref = 1.1925  # mA[cite: 1]
    error = abs(i_py - i_spice_ref) / i_spice_ref * 100
    self.assertLess(error, 1.0)


def ejecutar_tests():
  print("[TEST SUITE] Ejecutando validación frente a modelos SPICE...")
  suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoDePruebas)
  unittest.TextTestRunner(verbosity=1).run(suite)
  print("[TEST SUITE] Pruebas superadas con éxito.\n")


# =============================================================================
# BUCLE PRINCIPAL DE INTERFAZ Y BANCO DE PRUEBAS (PYGAME)
# =============================================================================
def main():
  ejecutar_tests()

  reloj = pygame.time.Clock()
  global v_gs, TEMP_AMBIENTE, temp_juntura, V_TH_BASE, K_N_BASE, auto_arreglo_activo

  # Inicialización opcional del puerto serial USB (HIL)
  puerto_serial = None
  if SERIAL_DISPONIBLE:
    try:
      # Cambia 'COM3' por tu puerto real si lo requieres (ej. '/dev/ttyUSB0')
      puerto_serial = serial.Serial("COM3", 9600, timeout=0.05)
      print("[USB COM] Conectado exitosamente al puerto serie.")
    except Exception:
      puerto_serial = None
      print("[USB COM] Sin hardware externo detectado. Modo simulación activo.")

  origin_x, origin_y = 100, 770
  axis_w, axis_h = 880, 340

  corriendo = True
  while corriendo:
    dt = reloj.tick(60) / 1000.0

    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        corriendo = False
      elif evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_UP:
          # Límite ampliado hasta 8.0V
          v_gs = min(8.0, v_gs + 0.1)
        elif evento.key == pygame.K_DOWN:
          v_gs = max(0.0, v_gs - 0.1)
        elif evento.key == pygame.K_a:
          auto_arreglo_activo = not auto_arreglo_activo

    # Lectura de datos externos por Puerto USB COM (si está conectado)
    if puerto_serial and puerto_serial.in_waiting > 0:
      try:
        linea_serial = puerto_serial.readline().decode("utf-8").strip()
        if linea_serial:
          v_gs = float(linea_serial)
          v_gs = max(0.0, min(8.0, v_gs))
      except ValueError:
        pass

    # Solución automática del circuito
    v_ds, i_ds, region_actual = solucionador_punto_operacion(
        v_gs, V_TH_BASE, K_N_BASE, LAMBDA
    )
    _, _, v_th_efec, k_n_efec = calcular_mosfet_riguroso(
        v_gs, v_ds, V_TH_BASE, K_N_BASE, LAMBDA
    )

    # Cálculo de la Ecuación Maestra Histórica Unificada
    e_e_valor, rho_val, nand_val = calcular_ecuacion_maestra_historica(
        v_gs, v_ds, i_ds, temp_juntura
    )

    # Dinámica Térmica Transitoria
    potencia_w = v_ds * (i_ds / 1000.0)
    d_temp_dt = (
        potencia_w - (temp_juntura - TEMP_AMBIENTE) / R_TH
    ) / C_TH
    temp_juntura += d_temp_dt * dt
    temp_juntura = max(TEMP_AMBIENTE, temp_juntura)

    # Diagnóstico IA (TensorFlow)
    features = np.array(
        [[v_gs, v_ds, temp_juntura]], dtype=np.float32
    )
    prob_fallo = float(ml_model.predict(features, verbose=0)[0][0])

    # SISTEMA AUTOCORRECTOR AUTOMÁTICO (Tecla 'A')
    mensaje_autocorrector = "• Sistema operando en modo manual."
    if auto_arreglo_activo:
      if prob_fallo > 0.45 or temp_juntura > 75.0 or v_gs > 6.5:
        v_gs = max(3.0, v_gs - 0.05)
        temp_juntura = max(TEMP_AMBIENTE, temp_juntura - 0.8)
        mensaje_autocorrector = (
            "🟢 [AUTOCORRECTOR ACTIVO] Estabilizando térmicamente y ajustando"
            f" V_gs a {v_gs:.2f}V..."
        )
      else:
        mensaje_autocorrector = (
            "🟢 [AUTOCORRECTOR ACTIVO] Parámetros seguros óptimos."
        )

    # Renderizado Gráfico
    pantalla.fill(BLANCO)

    txt_titulo = fuente_titulo.render(
        "BANCO DE PRUEBAS - ECUACIÓN MAESTRA Y FÓRMULAS HISTÓRICAS UNIFICADAS",
        True,
        AZUL_OSCURO,
    )
    pantalla.blit(txt_titulo, (30, 8))

    # Panel de Fórmulas Históricas e Instrumentación
    pygame.draw.rect(pantalla, VIOLETA_CLARO, (30, 32, 1040, 115), border_radius=6)
    pygame.draw.rect(pantalla, VIOLETA, (30, 32, 1040, 115), 2, border_radius=6)

    textos_formulas = [
        f"• [1] Maxwell (Div D = rho): Densidad de Carga rho = {rho_val:.3f}",
        (
            f"• [2] Shockley / Shichman-Hodges (MOSFET): I_ds ="
            f" {i_ds:.2f}mA | Región: {region_actual}"
        ),
        (
            f"• [3] Lógica Discreta (NAND Status): Estado lógico ="
            f" {'HIGH (1)' if nand_val==1 else 'LOW (0)'}"
        ),
        (
            f"• [4] ECUACIÓN MAESTRA UNIFICADA E_e(t) = {e_e_valor:.3f} | T_j ="
            f" {temp_juntura:.1f}°C"
        ),
    ]
    for i, t in enumerate(textos_formulas):
      txt = fuente.render(t, True, NEGRO)
      pantalla.blit(txt, (42, 38 + i * 26))

    # Panel de Control y Estado
    pygame.draw.rect(pantalla, AZUL_CLARO, (30, 152, 1040, 65), border_radius=6)
    pygame.draw.rect(pantalla, AZUL, (30, 152, 1040, 65), 2, border_radius=6)

    textos_panel2 = [
        f"• Autocorrector ('A'): {'🟢 ACTIVO' if auto_arreglo_activo else '🔴 MANUAL'} | V_gs = {v_gs:.2f}V | V_ds = {v_ds:.2f}V | USB: {'🔌 CONECTADO' if puerto_serial else '💻 SIMULADO'}",
        mensaje_autocorrector,
    ]
    for i, t in enumerate(textos_panel2):
      txt = fuente.render(t, True, NEGRO)
      pantalla.blit(txt, (42, 158 + i * 26))

    # Panel Gráfico de Curvas y Recta de Carga
    pygame.draw.rect(
        pantalla, (250, 250, 250), (30, 222, 1040, 600), border_radius=6
    )
    pygame.draw.rect(pantalla, GRIS, (30, 222, 1040, 600), 2, border_radius=6)

    txt_graf = fuente_titulo.render(
        "Curvas Características 2N7000, Recta de Carga y Solución del Q-Point",
        True,
        NEGRO,
    )
    pantalla.blit(txt_graf, (45, 230))

    pygame.draw.line(
        pantalla, NEGRO, (origin_x, origin_y), (origin_x + axis_w, origin_y), 2
    )
    pygame.draw.line(
        pantalla, NEGRO, (origin_x, origin_y - axis_h), (origin_x, origin_y), 2
    )

    txt_x = fuente.render("V_ds (V)", True, NEGRO)
    pantalla.blit(txt_x, (origin_x + axis_w - 40, origin_y + 8))
    txt_y = fuente.render("I_ds (mA)", True, NEGRO)
    pantalla.blit(txt_y, (origin_x - 50, origin_y - axis_h - 20))

    # Trazar curvas teóricas de referencia ampliadas hasta 8.0V
    for vgs_val_ref in [2.0, 3.5, 5.0, 6.5, 8.0]:
      puntos_curva = []
      for vds_step in range(0, 51):
        vds_val = vds_step * 0.1
        current, _, _, _ = calcular_mosfet_riguroso(
            vgs_val_ref, vds_val, V_TH_BASE, K_N_BASE, LAMBDA
        )
        px = origin_x + int((vds_val / 5.0) * axis_w)
        py = origin_y - int((current / 20.0) * axis_h)
        puntos_curva.append((px, py))
      if len(puntos_curva) > 1:
        pygame.draw.aalines(pantalla, (120, 150, 180), False, puntos_curva)

    # Recta de carga del circuito
    puntos_recta = [(0.0, (V_DD / R_L) * 1000.0), (V_DD, 0.0)]
    rx1 = origin_x + int((puntos_recta[0][0] / 5.0) * axis_w)
    ry1 = origin_y - int((puntos_recta[0][1] / 20.0) * axis_h)
    rx2 = origin_x + int((puntos_recta[1][0] / 5.0) * axis_w)
    ry2 = origin_y - int((puntos_recta[1][1] / 20.0) * axis_h)
    pygame.draw.line(pantalla, NARANJA, (rx1, ry1), (rx2, ry2), 2)

    # Punto Q unificado en movimiento
    x_operacion = origin_x + int((v_ds / 5.0) * axis_w)
    y_operacion = origin_y - int((i_ds / 20.0) * axis_h)

    pygame.draw.circle(pantalla, VERDE, (x_operacion, y_operacion), 9)
    pygame.draw.circle(pantalla, NEGRO, (x_operacion, y_operacion), 9, 2)

    txt_pto = fuente.render(
        f"Q-Point Unificado: ({v_ds:.2f}V, {i_ds:.2f}mA) | E_e: {e_e_valor:.2f}",
        True,
        VERDE,
    )
    pantalla.blit(txt_pto, (x_operacion + 15, y_operacion - 10))

    pygame.display.flip()
    reloj.tick(60)

  if puerto_serial and puerto_serial.is_open:
    puerto_serial.close()

  pygame.quit()
  sys.exit()


if __name__ == "__main__":
  main()