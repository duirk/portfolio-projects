import socket
import os

PUERTO = 5001
CARPETA_DESTINO = '/storage/emulated/0/Download'

# Crear la carpeta de Descargas si no existe
if not os.path.exists(CARPETA_DESTINO):
    os.makedirs(CARPETA_DESTINO, exist_ok=True)

# Configurar el Socket Servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    servidor.bind(('0.0.0.0', PUERTO))
    servidor.listen(5)
    print(f"🟢 [RECEPTOR ANDROID] Escuchando en el puerto {PUERTO}...")
    print(f"📁 Los archivos se guardarán en: {CARPETA_DESTINO}")
except Exception as e:
    print(f"❌ Error al iniciar el puerto {PUERTO}: {e}")
    print("💡 Si dice 'Address already in use', ejecuta: pkill -f python")
    exit(1)

while True:
    conn, addr = servidor.accept()
    print(f"\n📥 Conexión recibida desde {addr[0]}")
    
    try:
        # 1. Recibir cantidad de archivos
        cant_bytes = conn.recv(1024).decode('utf-8', errors='ignore').strip()
        num_archivos = int(cant_bytes)
        conn.sendall(b"OK")
        
        for i in range(num_archivos):
            # 2. Recibir encabezado: "Nombre|Tamaño"
            header = conn.recv(2048).decode('utf-8', errors='ignore').strip()
            nombre_archivo, tamano_str = header.split('|')
            tamano_total = int(tamano_str)
            conn.sendall(b"OK")
            
            ruta_salida = os.path.join(CARPETA_DESTINO, nombre_archivo)
            bytes_recibidos = 0
            
            # 3. Recibir el contenido binario del archivo
            with open(ruta_salida, 'wb') as f:
                while bytes_recibidos < tamano_total:
                    chunk = conn.recv(min(4096, tamano_total - bytes_recibidos))
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_recibidos += len(chunk)
            
            print(f"✅ [{i+1}/{num_archivos}] Archivo guardado: {nombre_archivo}")

            # Force MediaScan para que aparezca de inmediato en la Galería
            os.system(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d "file://{ruta_salida}" > /dev/null 2>&1')

            conn.sendall(b"OK")
            
    except Exception as e:
        print(f"⚠️ Error procesando la transferencia: {e}")
    finally:
        conn.close()