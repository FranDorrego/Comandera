import os
import subprocess
import urllib.request
import zipfile
import shutil

PYTHON_URL = "https://www.python.org/ftp/python/3.10.9/python-3.10.9-embed-win32.zip"
PYTHON_DIR = "Python32"
VENV_DIR = os.path.join("HostBase", "venv32")
REQUIREMENTS = os.path.join("HostBase", "requirements.txt")


def ejecutar_instalacion_backend(ruta_mdb, log, log_general):
    try:
        if not os.path.exists(PYTHON_DIR):
            log_general("🔽 Descargando Python embebido 32 bits...")
            zip_path = "python_embed.zip"
            urllib.request.urlretrieve(PYTHON_URL, zip_path)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(PYTHON_DIR)
            os.remove(zip_path)
            log_general("✅ Python embebido instalado en ./Python32")
        else:
            log_general("✅ Python ya estaba instalado.")

        python_exe = os.path.join(PYTHON_DIR, "python.exe")

        if not os.path.exists(VENV_DIR):
            log_general("⚙️ Creando entorno virtual en HostBase...")
            subprocess.check_call([python_exe, "-m", "venv", VENV_DIR])
            log_general("✅ Entorno virtual creado.")
        else:
            log_general("✅ Entorno virtual ya existente.")

        pip_exe = os.path.join(VENV_DIR, "Scripts", "pip.exe")

        if os.path.exists(REQUIREMENTS):
            log_general("📦 Instalando dependencias del backend...")
            subprocess.check_call([pip_exe, "install", "-r", REQUIREMENTS])
            log_general("✅ Dependencias instaladas.")
        else:
            log_general("⚠️ No se encontró requirements.txt en HostBase.")

        if os.path.exists(ruta_mdb):
            destino = os.path.join("HostBase", "db.mdb")
            shutil.copy2(ruta_mdb, destino)
            log_general(f"📁 Base de datos copiada a {destino}")

    except Exception as e:
        log_general(f"❌ Error durante instalación del backend: {e}")
