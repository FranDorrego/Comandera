import os
import subprocess
import urllib.request
import getpass
from tkinter import filedialog, messagebox

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
                log_general("📌 Seleccione manualmente el ejecutable de Python...")

                archivo = filedialog.askopenfilename(
                    filetypes=[("Ejecutable", "*.exe")],
                    title="Selecciona el ejecutable de Python 32 bits"
                )

                if archivo and os.path.exists(archivo):
                    python_exe = archivo
                else:
                    messagebox.showerror("Python no encontrado", "No se pudo localizar Python 32 bits. Se cancela la instalación.")
                    return
            else:
                python_exe = PYTHON_EXE_INSTALLED
                log_general("✅ Python 32 bits detectado.")
        else:
            python_exe = PYTHON_EXE_INSTALLED
            log_general("✅ Python 32 bits ya estaba instalado.")

        python_exe = PYTHON_EXE_INSTALLED

        # Crear entorno virtual
        if not os.path.exists(VENV_PATH):
            log_general("⚙️ Creando entorno virtual...")
            subprocess.check_call([python_exe, "-m", "venv", VENV_PATH])
            log_general("✅ Entorno virtual creado.")
        else:
            log_general("✅ Entorno virtual ya existente.")

        pip_venv = os.path.join(VENV_PATH, "Scripts", "pip.exe")

        # Instalar de dependencias
        if os.path.exists(REQUIREMENTS):
            log_general("📦 Instalando dependencias del backend...")
            subprocess.check_call([pip_venv, "install", "-r", REQUIREMENTS])
            log_general("✅ Dependencias instaladas.")
        else:
            log_general("⚠️ No se encontró requirements.txt")

        return True
    
    except Exception as e:
        log_general(f"❌ Error durante instalación del backend: {e}")
