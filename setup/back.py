import os
import subprocess
import urllib.request
import zipfile
import shutil

PYTHON_URL = "https://www.python.org/ftp/python/3.10.9/python-3.10.9-embed-win32.zip"
PYTHON_DIR = "Python32"
HOSTBASE_DIR = "HostBase"
REQUIREMENTS = os.path.join(HOSTBASE_DIR, "requirements.txt")

def ejecutar_instalacion_backend(ruta_mdb, log, log_general):
    try:
        # 1. Descargar Python embebido
        if not os.path.exists(PYTHON_DIR):
            log_general("🔽 Descargando Python embebido 32 bits...")
            zip_path = "python_embed.zip"
            urllib.request.urlretrieve(PYTHON_URL, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(PYTHON_DIR)
            os.remove(zip_path)
            log_general("✅ Python embebido instalado en ./Python32")

            # 1b. Modificar _pth para permitir site-packages
            pth_file = [f for f in os.listdir(PYTHON_DIR) if f.endswith("._pth")]
            if pth_file:
                pth_path = os.path.join(PYTHON_DIR, pth_file[0])
                with open(pth_path, "r", encoding="utf-8") as f:
                    contenido = f.read()
                contenido = contenido.replace("#import site", "import site")
                with open(pth_path, "w", encoding="utf-8") as f:
                    f.write(contenido)
                log_general("🧩 Configuración del entorno embebido completada.")
        else:
            log_general("✅ Python ya estaba instalado.")

        python_exe = os.path.abspath(os.path.join(PYTHON_DIR, "python.exe"))

        # 2. Instalar pip (no viene por defecto)
        get_pip = os.path.join(PYTHON_DIR, "get-pip.py")
        urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip)
        log_general("⚙️ Instalando pip...")
        subprocess.check_call([python_exe, get_pip])
        os.remove(get_pip)
        log_general("✅ pip instalado correctamente.")

        # 3. Instalar dependencias globalmente
        if os.path.exists(REQUIREMENTS):
            log_general("📦 Instalando dependencias del backend...")
            subprocess.check_call([python_exe, "-m", "pip", "install", "-r", REQUIREMENTS])
            log_general("✅ Dependencias instaladas.")
        else:
            log_general("⚠️ No se encontró requirements.txt en HostBase.")

        # 4. Copiar la base de datos
        if os.path.exists(ruta_mdb):
            destino = os.path.join(HOSTBASE_DIR, "db.mdb")
            shutil.copy2(ruta_mdb, destino)
            log_general(f"📁 Base de datos copiada a {destino}")

    except Exception as e:
        log_general(f"❌ Error durante instalación del backend: {e}")
