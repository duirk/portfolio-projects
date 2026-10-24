
```markdown
# 🌀 Teletransporte MP4 (PC ➔ Android/PC)

Aplicación en Python que envía vídeos MP4 a Android por Wi-Fi mediante **Sockets TCP** y los guarda en `/Descargas`. Incluye interfaz en **Gradio** y animación dinámicas en **Pillow**.

---

## 🛠️ Instalación

```bash
pip install gradio pillow

```

---

## 🚀 Uso Rápido

1. **Android:** Ejecuta `python receptor.py` en Termux y copia tu IP. O EJECUTNADO RECEPTOR EN PYANDROID
2. **PC:** Ejecuta `python app.py` y abre `http://localhost:8080`.
3. Sube los archivos `.mp4`, ingresa la IP de Android y pulsa **"🚀 Teletransportar"**.

---

## ⚙️ ¿Cómo funciona la transferencia binaria?

1. **Lectura Binaria (`'rb'`):** Lee el archivo `.mp4` byte por byte directamente desde el disco duro, ignorando el formato de texto.
2. **Bloques de 4 KB (`chunks`):** Divide el vídeo en fragmentos de `4096 bytes` para enviarlos secuencialmente sin saturar la memoria RAM.
3. **Flujo por Sockets (TCP/Puerto 5000):** Envía primero la cabecera (`Nombre|Tamaño`), espera un mensaje de confirmación (`ACK`) y transmite la ráfaga de datos binarios por Wi-Fi.
4. **Sincronización:** El móvil confirma cada archivo recibido antes de procesar el siguiente.

```

```
