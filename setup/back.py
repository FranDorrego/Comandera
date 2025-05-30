import os
import subprocess
import urllib.request
import shutil
import getpass

# Parámetros
PYTHON_EXE_URL = "https://www.python.org/ftp/python/3.10.9/python-3.10.9.exe"
PYTHON_INSTALLER_PATH = "python_installer.exe"

# Ruta de instalación esperada de Python 32 bits
USERNAME = getpass.getuser()
PYTHON_INSTALL_DIR = os.path.join("C:\\Users", USERNAME, "AppData", "Local", "Programs", "Python", "Python310-32")
PYTHON_EXE_INSTALLED = os.path.join(PYTHON_INSTALL_DIR, "python.exe")

# Proyecto
HOSTBASE_DIR = "HostBase"
VENV_PATH = os.path.join(HOSTBASE_DIR, "venv32")
REQUIREMENTS = os.path.join(HOSTBASE_DIR, "requirements.txt")
WHEEL_GREENLET_URL = "https://download.lfd.uci.edu/pythonlibs/w4tscw6k/greenlet-3.2.2-cp310-cp310-win32.whl"
WHEEL_LOCAL_PATH = os.path.join(HOSTBASE_DIR, "greenlet.whl")

def ejecutar_instalacion_backend(ruta_mdb, log, log_general):
    try:
        if not os.path.exists(PYTHON_EXE_INSTALLED):
            log_general("🔽 Descargando instalador de Python 32 bits...")
            urllib.request.urlretrieve(PYTHON_EXE_URL, PYTHON_INSTALLER_PATH)

            log_general("📥 Ejecutando instalador de Python...")
            subprocess.Popen([PYTHON_INSTALLER_PATH]).wait()

            if not os.path.exists(PYTHON_EXE_INSTALLED):
                log_general("❌ No se encontró Python 32 bits en la ubicación esperada.")
                log_general("📌 Por favor asegúrese de NO cambiar la ruta de instalación.")
                return
            log_general("✅ Python 32 bits detectado.")

        else:
            log_general("✅ Python 32 bits ya estaba instalado.")

        python_exe = PYTHON_EXE_INSTALLED
        pip_exe = os.path.join(PYTHON_INSTALL_DIR, "Scripts", "pip.exe")

        # Crear entorno virtual
        if not os.path.exists(VENV_PATH):
            log_general("⚙️ Creando entorno virtual...")
            subprocess.check_call([python_exe, "-m", "venv", VENV_PATH])
            log_general("✅ Entorno virtual creado.")
        else:
            log_general("✅ Entorno virtual ya existente.")

        pip_venv = os.path.join(VENV_PATH, "Scripts", "pip.exe")

        # Instalar greenlet manual si está en requirements
        if os.path.exists(REQUIREMENTS) and "greenlet" in open(REQUIREMENTS).read():
            log_general("🔽 Descargando greenlet precompilado...")
            urllib.request.urlretrieve(WHEEL_GREENLET_URL, WHEEL_LOCAL_PATH)
            subprocess.check_call([pip_venv, "install", WHEEL_LOCAL_PATH])
            os.remove(WHEEL_LOCAL_PATH)
            log_general("✅ greenlet instalado.")

        # Instalar resto de dependencias
        if os.path.exists(REQUIREMENTS):
            log_general("📦 Instalando dependencias del backend...")
            subprocess.check_call([pip_venv, "install", "-r", REQUIREMENTS])
            log_general("✅ Dependencias instaladas.")
        else:
            log_general("⚠️ No se encontró requirements.txt")

        # Copiar base de datos
        if ruta_mdb and os.path.exists(ruta_mdb):
            destino = os.path.join(HOSTBASE_DIR, "db.mdb")
            shutil.copy2(ruta_mdb, destino)
            log_general(f"📁 Base de datos copiada a {destino}")

        return True
    
    except Exception as e:
        log_general(f"❌ Error durante instalación del backend: {e}")
