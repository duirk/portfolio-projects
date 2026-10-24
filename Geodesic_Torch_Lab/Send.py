import gradio as gr
from PIL import Image, ImageDraw
import math
import socket
import os

PUERTO_ANDROID = 5000

# ==========================================
# 1. GENERADOR DE ANIMACIÓN DEL PORTAL (GIF)
# ==========================================
def crear_portal(draw, centro, radio, color, angulo):
    x_c, y_c = centro
    draw.ellipse([x_c - radio, y_c - radio, x_c + radio, y_c + radio], outline=color, width=4)
    num_particulas = 8
    for i in range(num_particulas):
        a = angulo + (i * (2 * math.pi / num_particulas))
        px = x_c + int(math.cos(a) * (radio - 5))
        py = y_c + int(math.sin(a) * (radio - 5))
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=color)

def generar_gif_teletransporte(ip_a, ip_b, total_archivos):
    ANCHO, ALTO = 800, 400
    pos_A, pos_B = (200, 220), (600, 220)
    frames = []
    total_frames = 30
    
    for i in range(total_frames):
        lienzo = Image.new("RGBA", (ANCHO, ALTO), (15, 15, 25, 255))
        draw = ImageDraw.Draw(lienzo)
        angulo = (i / total_frames) * 4 * math.pi
        
        crear_portal(draw, pos_A, 60, (0, 180, 255, 255), angulo)
        crear_portal(draw, pos_B, 60, (50, 255, 100, 255), -angulo)
        
        draw.text((pos_A[0] - 50, pos_A[1] - 90), f"Origen (PC):\n{ip_a}", fill=(0, 180, 255))
        draw.text((pos_B[0] - 50, pos_B[1] - 90), f"Destino (Android):\n{ip_b}", fill=(50, 255, 100))
        draw.text((ANCHO // 2 - 80, 30), f"🎥 Teletransportando {total_archivos} MP4(s)", fill=(255, 220, 0))

        for px in range(pos_A[0], pos_B[0], 25):
            draw.ellipse([px, pos_A[1] - 2, px + 4, pos_A[1] + 2], fill=(80, 80, 100))

        frames.append(lienzo.convert("RGB"))

    gif_path = "teletransporte_mp4.gif"
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=60, loop=0)
    return gif_path

# ==========================================
# 2. LÓGICA DE ENVÍO DE MÚLTIPLES ARCHIVOS
# ==========================================
def teletransportar_videos(archivos, ip_origen, ip_destino):
    if not archivos:
        return None, "⚠️ Por favor selecciona al menos un archivo MP4."

    ip_a = ip_origen.strip() if ip_origen.strip() else "192.168.1.36"
    ip_b = ip_destino.strip()

    if not ip_b:
        return None, "⚠️ Ingresa la IP de tu teléfono Android."

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.settimeout(15.0)  # Tiempo de espera extendido para videos grandes
        cliente.connect((ip_b, PUERTO_ANDROID))
        
        # 1. Enviar cantidad de archivos
        cliente.sendall(f"{len(archivos)}".encode('utf-8'))
        cliente.recv(1024) # Esperar confirmación (OK)
        
        # 2. Enviar cada archivo MP4
        for archivo in archivos:
            ruta_filepath = archivo.name
            nombre = os.path.basename(ruta_filepath)
            tamano = os.path.getsize(ruta_filepath)
            
            # Enviar cabecera (Nombre|Tamaño)
            cliente.sendall(f"{nombre}|{tamano}".encode('utf-8'))
            cliente.recv(1024)
            
            # Enviar contenido binario
            with open(ruta_filepath, 'rb') as f:
                while chunk := f.read(4096):
                    cliente.sendall(chunk)
            
            cliente.recv(1024) # Esperar confirmación
            
        cliente.close()
    except socket.timeout:
        return None, f"❌ Tiempo agotado al conectar con {ip_b}:5000."
    except ConnectionRefusedError:
        return None, f"❌ Conexión rechazada. Ejecuta 'python receptor.py' en Termux."
    except Exception as e:
        return None, f"❌ Error de transferencia: {e}"

    # Generar GIF de confirmación
    gif_path = generar_gif_teletransporte(ip_a, ip_b, len(archivos))
    return gif_path, f"✅ ¡ÉXITO! Se teletransportaron {len(archivos)} video(s) MP4 a la carpeta Descargas de tu Android."

# ==========================================
# 3. INTERFAZ GRÁFICA EN GRADIO
# ==========================================
with gr.Blocks(title="Teletransporte Multi-MP4") as demo:
    gr.Markdown("# 🌀 Portal de Teletransporte Múltiple de Videos MP4")
    
    with gr.Row():
        with gr.Column():
            input_files = gr.File(
                label="Selecciona o arrastra tus archivos MP4", 
                file_count="multiple", 
                file_types=[".mp4"]
            )
            ip_origen = gr.Textbox(label="IP Origen (PC)", value="192.168.1.36")
            ip_destino = gr.Textbox(label="IP Destino (Android)", placeholder="Ej: 192.168.1.15")
            btn = gr.Button("🚀 Teletransportar Videos MP4", variant="primary")
            
        with gr.Column():
            output_gif = gr.Image(label="Animación del Portal")
            output_status = gr.Textbox(label="Estado del Envío", interactive=False)
        
    btn.click(
        fn=teletransportar_videos, 
        inputs=[input_files, ip_origen, ip_destino], 
        outputs=[output_gif, output_status]
    )

if __name__ == "__main__":
    demo.launch(server_port=8080)