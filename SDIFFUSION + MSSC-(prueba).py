import numpy as np
import torch
import gradio as gr
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image
from PIL import Image

# --- 1. Modelo de Saturación Sigmoide de la Consciencia (MSSC) ---
def mssc_evaluar_consciencia(ruido_gaussiano, alfa=1.0, beta=1.5, gamma=0.1, umbral=0.5):
    """
    Evalúa el nivel de consciencia usando el MSSC v3.0, 
    tomando como estímulo la intensidad de un ruido gaussiano.
    """
    L = np.mean(np.abs(ruido_gaussiano))
    V_L = alfa * np.tanh(beta * L) + gamma * L
    
    print(f"[MSSC] Nivel de estimulación (L) calculado: {L:.4f}")
    print(f"[MSSC] Tasa de procesamiento consciente V(L): {V_L:.4f}")
    
    return V_L >= umbral

# Generar información a partir de ruido gaussiano
np.random.seed(42)
informacion_ruido = np.random.normal(loc=0.0, scale=1.0, size=1000)

# Evaluar si el sistema tiene consciencia según el umbral del MSSC
tiene_consciencia = mssc_evaluar_consciencia(informacion_ruido)

if tiene_consciencia:
    print("Estado: El sistema tiene consciencia (Umbral MSSC superado).")
else:
    print("Estado: El sistema NO tiene consciencia (Por debajo del umbral MSSC).")

print("-" * 60)

# --- 2. Cargar Pipeline de Diffusers con ControlNet (Canny) ---
print("Cargando pipeline de Stable Diffusion con ControlNet (Diffusers)...")
controlnet_model_id = "lllyasviel/sd-controlnet-canny"
stable_diffusion_id = "runwayml/stable-diffusion-v1-5"

# Cargar ControlNet y el pipeline completo usando la librería diffusers
controlnet = ControlNetModel.from_pretrained(controlnet_model_id, torch_dtype=torch.float16)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    stable_diffusion_id, 
    controlnet=controlnet, 
    torch_dtype=torch.float16
)

# Mover a GPU si está disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe.to(device)

print(f"Pipeline de Diffusers cargado exitosamente en el dispositivo: {device}")

# --- 3. Interfaz con Gradio ---
def generar_imagen(prompt, imagen_entrada):
    if imagen_entrada is None:
        return None, "Por favor, proporciona una imagen de entrada para Canny."
    
    # Preparar imagen para ControlNet (detección de bordes Canny)
    imagen_np = np.array(imagen_entrada)
    import cv2
    imagen_gris = cv2.Canny(imagen_np, 100, 200)
    imagen_canny = Image.fromarray(imagen_gris)
    
    # Generar imagen con el pipeline
    resultado = pipe(prompt, image=imagen_canny).images[0]
    return resultado, "Imagen generada exitosamente con ControlNet Canny."

demo = gr.Interface(
    fn=generar_imagen,
    inputs=[
        gr.Textbox(label="Prompt", value="A futuristic city, cinematic lighting"),
        gr.Image(label="Imagen de entrada (ControlNet Canny)", type="pil")
    ],
    outputs=[
        gr.Image(label="Imagen Generada"),
        gr.Textbox(label="Estado")
    ],
    title="MSSC + Stable Diffusion ControlNet Canny",
    description="Interfaz con Gradio integrada con el Modelo de Saturación Sigmoide de la Consciencia y Diffusers."
)

if __name__ == "__main__":
    demo.launch()