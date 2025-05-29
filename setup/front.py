import os
import subprocess
import urllib.request
import zipfile
import threading

NODE_URL = "https://nodejs.org/dist/v18.17.1/node-v18.17.1-win-x86.zip"
NODE_DIR = r"Node.js\node-v18.17.1-win-x86"
FRONTEND_DIR = "frontend"


def ejecutar_instalacion_frontend(log, log_general):
    try:
        if not os.path.exists(NODE_DIR):
            log_general("🔽 Descargando Node.js 32 bits...")
            zip_path = "node.zip"
            urllib.request.urlretrieve(NODE_URL, zip_path)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("Node.js")
            os.remove(zip_path)
            log_general("✅ Node.js instalado en ./Node.js")
        else:
            log_general("✅ Node.js ya estaba instalado.")

        npm_cmd = os.path.abspath(os.path.join(f"{NODE_DIR}", "npm.cmd"))

        if not os.path.exists(npm_cmd):
            log_general("⚠️ No se encontró npm.cmd. Verifica la descarga de Node.js.")
            return

        log_general("📦 Instalando dependencias del frontend...")
        log_general("📦 Instalando dependencias del frontend...")
        proceso = subprocess.Popen(["cmd", "/c", npm_cmd, "install"], cwd=os.path.abspath(FRONTEND_DIR), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        def leer_salida():
            for linea in proceso.stdout:
                log_general(linea.strip())

        hilo_log = threading.Thread(target=leer_salida)
        hilo_log.start()
        proceso.wait()
        hilo_log.join()

        log_general("✅ Dependencias del frontend instaladas.")

    except Exception as e:
        log_general(f"❌ Error durante instalación del frontend: {e}")