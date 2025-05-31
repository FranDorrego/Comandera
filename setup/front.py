import os
import subprocess
import urllib.request
import threading
import tempfile

NODE_VERSION_OBJETIVO = (22, 16, 0)
NODE_URL = "https://nodejs.org/dist/v22.16.0/node-v22.16.0-x64.msi"

FRONTEND_DIR = "frontend"


def obtener_version_node():
    try:
        output = subprocess.check_output(["node", "--version"], text=True).strip()
        version_str = output.lstrip("v")  # Quita la 'v'
        return tuple(map(int, version_str.split(".")))  # Ej: (22, 16, 0)
    except Exception:
        return None


def instalar_node_msi(log):
    try:
        log("🔽 Descargando instalador de Node.js v22.16.0...")

        temp_dir = tempfile.gettempdir()
        path_msi = os.path.join(temp_dir, "node-installer.msi")

        urllib.request.urlretrieve(NODE_URL, path_msi)
        log("📦 Instalador descargado. Abriendo...")

        # Ejecutar el MSI con interfaz para el usuario
        subprocess.Popen(["msiexec", "/i", path_msi]).wait()
        log("➡️ Sigue los pasos del instalador de Node.js.")
    except Exception as e:
        log(f"❌ Error al descargar o ejecutar Node.js: {e}")


def ejecutar_instalacion_frontend(log, log_general):
    try:
        version_actual = obtener_version_node()
        if not version_actual or version_actual < NODE_VERSION_OBJETIVO:
            log_general(f"⚠️ Node.js no encontrado o versión desactualizada ({version_actual}). Instalando...")
            instalar_node_msi(log_general)
  
        version_actual = obtener_version_node()
        if not version_actual or version_actual < NODE_VERSION_OBJETIVO:
            log_general("❌ Node.js no instalado o versión insuficiente. Instalación cancelada.")
            return False
        
        log_general(f"✅ Node.js detectado. Versión actual: {version_actual}")
        return True
    except Exception as e:
        log_general(f"❌ Error durante instalación del frontend: {e}", f"npm install cwd= {os.path.abspath(FRONTEND_DIR)}")


def existe_node():
    version_actual = obtener_version_node()

    if not version_actual or version_actual < NODE_VERSION_OBJETIVO:
        return False
    return True