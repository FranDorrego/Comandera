import os
import sys
import ctypes
import subprocess
import shutil

REPO_URL = "git@github.com:FranDorrego/Comandera.git"
CARPETA = "Comandera"
ARCHIVO_INTERNO = "main.exe"
ACCESO_DIRECTO = "Comandera.exe"

CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW

import stat

def forzar_borrado(func, path, exc_info):
    # Intenta dar permisos de escritura y volver a borrar
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass


def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def solicitar_admin():
    if getattr(sys, 'frozen', False):
        # Si está compilado como .exe
        path = sys.executable
    else:
        # Si se está ejecutando como .py
        path = sys.executable
        script = os.path.abspath(__file__)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", path, f'"{script}"', None, 0)
        sys.exit()

    # Relanza el propio ejecutable con permisos de admin
    ctypes.windll.shell32.ShellExecuteW(None, "runas", path, "", None, 0)
    sys.exit()


def tiene_git():
    try:
        subprocess.check_output(["git", "--version"], creationflags=CREATE_NO_WINDOW)
        return True
    except:
        return False


def instalar_git():
    url = "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-32-bit.exe"
    path = os.path.abspath("git_installer.exe")
    subprocess.call(["powershell", "-Command", f"Invoke-WebRequest '{url}' -OutFile '{path}'"],
                    creationflags=CREATE_NO_WINDOW)
    subprocess.call([path, "/VERYSILENT", "/NORESTART"], creationflags=CREATE_NO_WINDOW)
    os.remove(path)


def clonar_o_actualizar_repo_en_escritorio():
    escritorio = os.path.join(os.environ["USERPROFILE"], "Desktop")
    destino = os.path.join(escritorio, CARPETA)

    os.environ["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no"

    if not os.path.exists(destino):
        os.chdir(escritorio)
        subprocess.check_call(["git", "clone", REPO_URL, CARPETA], creationflags=CREATE_NO_WINDOW)
    else:
        try:
            os.chdir(destino)
            subprocess.check_call(["git", "fetch", "--all"], creationflags=CREATE_NO_WINDOW)
            subprocess.check_call(["git", "reset", "--hard", "origin/main"], creationflags=CREATE_NO_WINDOW)
        except Exception:
            os.chdir(escritorio)
            shutil.rmtree(destino, onerror=forzar_borrado)
            subprocess.check_call(["git", "clone", REPO_URL, CARPETA], creationflags=CREATE_NO_WINDOW)

    return os.path.join(destino, ARCHIVO_INTERNO)


def crear_acceso_directo(origen_main_exe):
    try:
        import pythoncom
        from win32com.client import Dispatch

        pythoncom.CoInitialize()  # ¡esto es clave en entorno oculto!

        escritorio = os.path.join(os.environ["USERPROFILE"], "Desktop")
        acceso_lnk = os.path.join(escritorio, ACCESO_DIRECTO)

        shell = Dispatch("WScript.Shell")
        acceso = shell.CreateShortCut(acceso_lnk + ".lnk")
        acceso.Targetpath = origen_main_exe
        acceso.WorkingDirectory = os.path.dirname(origen_main_exe)
        acceso.IconLocation = origen_main_exe
        acceso.save()

    except Exception as e:
        # Log interno si necesitás debug
        with open(os.path.join(escritorio, "comandera_error.log"), "a") as f:
            f.write(f"Error creando acceso directo: {e}\n")


def main():
    if not tiene_git():
        instalar_git()

    path_main = clonar_o_actualizar_repo_en_escritorio()
    crear_acceso_directo(path_main)

    subprocess.Popen([path_main],
                     cwd=os.path.dirname(path_main),
                     shell=True,
                     creationflags=CREATE_NO_WINDOW)


if __name__ == "__main__":
    if not es_admin():
        solicitar_admin()
    else:
        main()
