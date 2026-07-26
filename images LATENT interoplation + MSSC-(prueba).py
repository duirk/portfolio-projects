import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import gradio as gr

# --- 1. Directorios de Salida ---
input_dir = "imagenes_subidas"
output_dir = "mssc_output_arte"
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# --- 2. Modelo de Saturación Sigmoide de la Consciencia (MSSC) ---
def mssc_evaluar_consciencia(ruido_gaussiano, alfa=1.0, beta=1.5, gamma=0.1, umbral=0.5):
    """
    Evalúa el nivel de consciencia usando el MSSC v3.0, 
    tomando como estímulo la intensidad del brillo/color extraído de un frame.
    """
    L = np.mean(np.abs(ruido_gaussiano))
    V_L = alfa * np.tanh(beta * L) + gamma * L
    return V_L, V_L >= umbral

# --- 3. Generador de Estilo Difusorio Invertido Único por Imagen ---
def generar_arte_difusorio_unico(frame_rgb, indice_imagen, total_imagenes):
    """
    Aplica una inversión difusoria y transformación geométrica/estilística 
    única y diferente para cada imagen fuente subida.
    """
    img_float = frame_rgb.astype(np.float32) / 255.0
    h, w, _ = img_float.shape
    
    # Semilla única basada en el índice de la imagen para garantizar variación absoluta
    np.random.seed(100 + indice_imagen)
    
    # Variaciones paramétricas únicas por cada imagen subida
    escala_ruido = 0.2 + (indice_imagen % 3) * 0.15
    frecuencia_color = (indice_imagen % 2) + 1
    
    # Generar ruido difusorio único
    ruido_fase = np.random.normal(loc=0.0, scale=escala_ruido, size=(h, w, 3))
    
    # Transformación cromática y de difusión exclusiva para esta imagen
    arte_generado = img_float * 0.7 + ruido_fase * 0.3
    arte_generado[:, :, 0] = np.roll(arte_generado[:, :, 0], shift=indice_imagen * 5, axis=1)
    
    # Extracción de bordes estéticos con Canny
    gray = cv2.cvtColor((np.clip(arte_generado, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 40 + (indice_imagen * 10) % 50, 150).astype(np.float32) / 255.0
    edges_3ch = np.stack([edges, edges, edges], axis=-1)
    
    arte_final = np.clip(arte_generado + edges_3ch * 0.35, 0.0, 1.0)
    return arte_final

# --- 4. Interpolación de Movimiento Fluido entre Imágenes Diferentes ---
def interpolar_secuencia_imagenes(lista_rutas, frames_por_transicion=15):
    """
    Toma las imágenes subidas, procesa un arte único para cada una y 
    genera una secuencia animada con movimiento interpolado entre ellas.
    """
    imagenes_procesadas = []
    
    for idx, ruta in enumerate(lista_rutas):
        img = cv2.imread(ruta)
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_rgb = cv2.resize(img_rgb, (256, 256))
            
            # Generar la imagen de arte única y diferente para esta fuente
            arte_unico = generar_arte_difusorio_unico(img_rgb, idx, len(lista_rutas))
            imagenes_procesadas.append((arte_unico * 255).astype(np.float32))

    if not imagenes_procesadas:
        return []

    if len(imagenes_procesadas) == 1:
        return [imagenes_procesadas[0].astype(np.uint8)] * 30

    secuencia_interpolada = []
    
    # Morphing y transición de movimiento fluido entre las piezas de arte únicas
    for i in range(len(imagenes_procesadas) - 1):
        img_actual = imagenes_procesadas[i]
        img_siguiente = imagenes_procesadas[i + 1]
        
        for t in range(frames_por_transicion):
            alpha = t / float(frames_por_transicion)
            frame_intermedio = (1.0 - alpha) * img_actual + alpha * img_siguiente
            secuencia_interpolada.append(np.clip(frame_intermedio, 0, 255).astype(np.uint8))

    secuencia_interpolada.append(imagenes_procesadas[-1].astype(np.uint8))
    return secuencia_interpolada

# --- 5. Función Principal de Procesamiento ---
def procesar_imagenes_con_movimiento(lista_imagenes):
    if not lista_imagenes:
        return None, []

    rutas_archivos = [img.name if hasattr(img, 'name') else img for img in lista_imagenes]
    
    frames_video = interpolar_secuencia_imagenes(rutas_archivos, frames_por_transicion=20)
    
    if not frames_video:
        return None, []

    frames_totales = len(frames_video)

    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
    fig.patch.set_facecolor('#05050a')

    COLOR_TEXT = '#e0e0e0'
    L_vals = np.linspace(0, 3, 100)
    V_vals = 1.0 * np.tanh(1.5 * L_vals) + 0.1 * L_vals

    rutas_png = []

    def actualizar(i):
        ax1.clear()
        ax2.clear()
        
        frame_arte = frames_video[i].astype(np.float32) / 255.0
        estimulo_visual = frame_arte
        nivel_consciencia, es_consciente = mssc_evaluar_consciencia(estimulo_visual)
        
        # --- Subplot 1: Arte Único en Movimiento ---
        ax1.set_facecolor('#0d1117')
        ax1.imshow(frame_arte)
        ax1.set_title(f"Arte Difusorio Único [Frame Dinámico {i+1}/{frames_totales}]", color=COLOR_TEXT, fontsize=11, fontweight='bold')
        ax1.axis('off')
        
        # --- Subplot 2: Evaluación MSSC Dinámica ---
        ax2.set_facecolor('#0d1117')
        ax2.plot(L_vals, V_vals, color='#8b949e', linestyle='--', label='Curva Base MSSC')
        ax2.axhline(y=0.5, color='#ff7b72', linestyle=':', label='Umbral Crítico ($\theta=0.5$)')
        
        L_actual = np.mean(np.abs(estimulo_visual))
        color_punto = '#3fb950' if es_consciente else '#f85149'
        ax2.scatter([L_actual], [nivel_consciencia], color=color_punto, s=140, zorder=5)
        
        estado_texto = "ESTADO: CONSCIENTE (ARTE ACTIVO)" if es_consciente else "ESTADO: SUB-CONSCIENTE (LATENTE)"
        ax2.set_title(f"{estado_texto} | V(L): {nivel_consciencia:.3f}", color=color_punto, fontsize=11, fontweight='bold')
        
        ax2.set_xlim(0, 3)
        ax2.set_ylim(0, 3.5)
        ax2.set_xlabel("Intensidad de Estímulo Difusorio (L)", color=COLOR_TEXT)
        ax2.set_ylabel("Nivel de Consciencia V(L)", color=COLOR_TEXT)
        ax2.grid(True, color='#21262d', linestyle='-', alpha=0.4)
        ax2.tick_params(colors=COLOR_TEXT)
        ax2.legend(loc='upper left', facecolor='#161b22', edgecolor='#30363d', labelcolor='#ffffff', fontsize=9)
        
        plt.tight_layout()
        
        nombre_png = os.path.join(output_dir, f"arte_unico_{i:03d}.png")
        plt.savefig(nombre_png, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
        rutas_png.append(nombre_png)

    for f in range(frames_totales):
        actualizar(f)
    
    animacion = animation.FuncAnimation(fig, actualizar, frames=frames_totales, interval=50)
    ruta_mp4_salida = os.path.join(output_dir, "mssc_arte_unico_resultado.mp4")
    
    try:
        animacion.save(ruta_mp4_salida, writer='ffmpeg', fps=20, dpi=150)
    except Exception as e:
        print(f"Nota sobre FFmpeg: {e}")
        ruta_mp4_salida = None

    plt.close(fig)
    return ruta_mp4_salida, rutas_png

# --- 6. Interfaz Gráfica con Gradio ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌀 Generador  Movimiento Dinámico con MSSC")
    gr.Markdown("Sube **varias imágenes**. El sistema transformará cada una en una pieza de arte difusorio **completamente diferente y única**, interpolando un movimiento fluido entre ellas y evaluando su consciencia visual.")
    
    with gr.Row():
        with gr.Column():
            input_images = gr.File(label="Sube tus imágenes base (varias)", file_count="multiple", file_types=["image"])
            btn_procesar = gr.Button("Generar  Movimiento", variant="primary")
            
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🎬 Video Animado Resultado (MP4)")
            output_video = gr.Video(label="Secuencia Animada Final")
            
        with gr.Column():
            gr.Markdown("### 🖼️ Galería de Frames Generados en PNG")
            output_gallery = gr.Gallery(label="Frames Procesados", columns=3, height="auto")

    btn_procesar.click(
        fn=procesar_imagenes_con_movimiento,
        inputs=[input_images],
        outputs=[output_video, output_gallery]
    )

if __name__ == "__main__":
    demo.launch()