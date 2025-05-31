import os
import subprocess
import urllib.request
import getpass
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

# ------------------------------
# Configuración
# ------------------------------

PYTHON_EXE_URL = "https://www.python.org/ftp/python/3.10.9/python-3.10.9.exe"
PYTHON_INSTALLER_PATH = "python_installer.exe"

# Rutas dinámicas basadas en main.exe
ROOT_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
HOSTBASE_DIR = os.path.join(ROOT_DIR, "HostBase")
VENV_PATH = os.path.join(HOSTBASE_DIR, "venv32")
REQUIREMENTS = os.path.join(HOSTBASE_DIR, "requirements.txt")

# ------------------------------
# Función principal
# ------------------------------

def ejecutar_instalacion_backend(ruta_mdb, log, log_general):
    try:
        python_exe = None

        # Paso 1: Intentar detectar Python en la ruta típica
        username = getpass.getuser()
        install_dir = os.path.join("C:\\Users", username, "AppData", "Local", "Programs", "Python", "Python310-32")
        possible_path = os.path.join(install_dir, "python.exe")

        if os.path.exists(possible_path):
            python_exe = possible_path
            log_general("✅ Python 32 bits detectado en la ruta predeterminada.")
        else:
            log_general("🔽 Descargando instalador de Python 32 bits...")
            urllib.request.urlretrieve(PYTHON_EXE_URL, os.path.join(ROOT_DIR, PYTHON_INSTALLER_PATH))
            log_general("📥 Ejecutando instalador de Python...")

            subprocess.run([os.path.join(ROOT_DIR, PYTHON_INSTALLER_PATH)], check=False)

            # Verificar si ahora sí está instalado
            if os.path.exists(possible_path):
                python_exe = possible_path
                log_general("✅ Python instalado y detectado correctamente.")
            else:
                # Mostrar UI para seleccionar manualmente
                log_general("❌ Python no encontrado. Requiere selección manual.")

                def seleccionar_manual():
                    archivo = filedialog.askopenfilename(
                        title="Selecciona el ejecutable de Python 32 bits",
                        filetypes=[("Ejecutable", "*.exe")]
                    )
                    if archivo and os.path.exists(archivo):
                        nonlocal python_exe
                        python_exe = archivo
                        top.destroy()
                    else:
                        messagebox.showerror("Error", "Ruta inválida. Se cancela la instalación.")
                        top.destroy()

                top = tk.Toplevel()
                top.title("Seleccionar Python")
                tk.Label(top, text="No se encontró Python 32 bits.\nSelecciona manualmente el ejecutable.").pack(padx=10, pady=10)
                tk.Button(top, text="Seleccionar", command=seleccionar_manual).pack(pady=10)
                top.grab_set()
                top.mainloop()

                if not python_exe:
                    return  # El usuario canceló

        # Paso 2: Crear entorno virtual
        if not os.path.exists(VENV_PATH):
            log_general("⚙️ Creando entorno virtual...")
            subprocess.check_call([python_exe, "-m", "venv", VENV_PATH])
            log_general("✅ Entorno virtual creado.")
        else:
            log_general("✅ Entorno virtual ya existente.")

        # Paso 3: Instalar dependencias
        pip_venv = os.path.join(VENV_PATH, "Scripts", "pip.exe")

        if os.path.exists(pip_venv) and os.path.exists(REQUIREMENTS):
            log_general("📦 Instalando dependencias del backend...")
            subprocess.check_call([pip_venv, "install", "-r", REQUIREMENTS])
            log_general("✅ Dependencias instaladas correctamente.")
        else:
            log_general("⚠️ No se pudo encontrar pip o requirements.txt")

        return True

    except Exception as e:
        log_general(f"❌ Error durante la instalación del backend: {e}")
        return False
