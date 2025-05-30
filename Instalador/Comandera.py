import os
import sys
import ctypes
import subprocess
import shutil
import time
from pathlib import Path

REPO_URL = "git@github.com:FranDorrego/Comandera.git"
CARPETA_REPO = "Comandera"
NOMBRE_SETUP = "main.exe"
NOMBRE_EJECUTABLE = "Comandera.exe"

def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def solicitar_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def tiene_git():
    try:
        subprocess.check_output(["git", "--version"])
        return True
    except:
        return False

def instalar_git():
    url = "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-32-bit.exe"
    path = os.path.abspath("git_installer.exe")
    subprocess.call(["powershell", "-Command", f"Invoke-WebRequest '{url}' -OutFile '{path}'"])
    subprocess.call([path, "/VERYSILENT", "/NORESTART"])
    os.remove(path)

def clonar_o_actualizar_repo():
    os.environ["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no"

    if not os.path.exists(CARPETA_REPO):
        subprocess.check_call(["git", "clone", REPO_URL, CARPETA_REPO])
    else:
        os.chdir(CARPETA_REPO)
        subprocess.call(["git", "fetch", "--all"])
        subprocess.call(["git", "reset", "--hard", "origin/main"])
        os.chdir("..")


def ejecutar_setup():
    ruta_absoluta = os.path.abspath(CARPETA_REPO)
    path_setup = os.path.join(ruta_absoluta, NOMBRE_SETUP)

    if os.path.exists(path_setup):
        print("▶ Ejecutando setup.exe...")
        subprocess.Popen([path_setup], cwd=ruta_absoluta, shell=True)
    else:
        print("❌ No se encontró setup.exe en", path_setup)


def crear_inicio_automatico():
    startup_dir = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    acceso = os.path.join(startup_dir, NOMBRE_EJECUTABLE)

    origen = os.path.abspath(sys.argv[0])
    if not origen.endswith(".exe"):
        print("⚠ Este script debe compilarse a .exe para crear acceso directo de inicio.")
        return

    if not os.path.exists(acceso):
        import pythoncom
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        acceso_lnk = acceso + ".lnk"
        acceso_obj = shell.CreateShortCut(acceso_lnk)
        acceso_obj.Targetpath = origen
        acceso_obj.WorkingDirectory = os.path.dirname(origen)
        acceso_obj.save()

def anclar_barra_tareas():
    powershell = f"""
    $path = "{os.path.abspath(sys.argv[0])}"
    $shell = New-Object -ComObject Shell.Application
    $folder = $shell.Namespace((Split-Path $path))
    $item = $folder.ParseName((Split-Path $path -Leaf))
    $item.InvokeVerb("Pin to Taskbar")
    """
    subprocess.call(["powershell", "-Command", powershell], shell=True)

def main():
    if not es_admin():
        solicitar_admin()
        sys.exit()

    print("✅ Ejecutando como administrador...")

    if not tiene_git():
        print("📦 Git no detectado. Instalando...")
        instalar_git()

    print("📁 Verificando carpeta Comandera...")
    clonar_o_actualizar_repo()

    print("🧷 Agregando a inicio automático...")
    crear_inicio_automatico()

    print("📌 Anclando a barra de tareas...")
    anclar_barra_tareas()

    print("▶ Ejecutando instalador setup.exe...")
    ejecutar_setup()

    print("✅ Todo listo.")

if __name__ == "__main__":
    main()
