import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import threading
import json
import os
import subprocess
import shutil
import signal
import time

from back import ejecutar_instalacion_backend, PYTHON_EXE_INSTALLED
from front import ejecutar_instalacion_frontend, existe_node

CONFIG_FILE = "setup/config.json"
PYTHON_DIR = PYTHON_EXE_INSTALLED
BASE_DIR = None


class InstaladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Comandera")
        self.base_path = tk.StringVar()

        self._crear_interfaz()
        self._cargar_config()
        self._verificar_estado_instalacion()
        self.root.protocol("WM_DELETE_WINDOW", self._cerrar_aplicacion)
        try: self.root.iconbitmap("favicon.ico")
        except: pass
        self.CORRER = True


    def _crear_interfaz(self):
        frame_path = tk.Frame(self.root)
        frame_path.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_path, text="📂 Ruta de la Base de Datos:").pack(side="left")
        self.entry_path = tk.Entry(frame_path, textvariable=self.base_path, width=50)
        self.entry_path.pack(side="left", padx=5)
        tk.Button(frame_path, text="Examinar", command=self._seleccionar_archivo).pack(side="left")

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=(0, 10))

        self.btn_iniciar = tk.Button(frame_botones, text="🚀 Iniciar Instalación", command=self._iniciar_instalacion, state="disabled")
        self.btn_iniciar.pack(side="left", padx=5)

        self.btn_start_back = tk.Button(frame_botones, text="▶ Start Back", command=self._start_backend, state="disabled")
        self.btn_start_back.pack(side="left", padx=5)

        self.btn_start_front = tk.Button(frame_botones, text="▶ Start Front", command=self._start_frontend, state="disabled")
        self.btn_start_front.pack(side="left", padx=5)

        self.btn_stop_back = tk.Button(frame_botones, text="⏹ Stop Back", command=self._stop_backend, state="disabled")
        self.btn_stop_back.pack(side="left", padx=5)

        self.btn_stop_front = tk.Button(frame_botones, text="⏹ Stop Front", command=self._stop_frontend, state="disabled")
        self.btn_stop_front.pack(side="left", padx=5)

        # Frame contenedor general
        self.frame_logs = tk.Frame(self.root)
        self.frame_logs.pack(padx=10, pady=10, fill="both", expand=True)

        # Detectar si la instalación ya fue hecha
        python_ok = os.path.exists(PYTHON_DIR)
        node_ok = existe_node()

        if not (python_ok and node_ok):
            # Mostrar consola de instalación (solo si es necesario)
            frame_general = tk.LabelFrame(self.frame_logs, text="Instalación")
            frame_general.pack(fill="both", expand=True, pady=(0, 5))
            self.log_general = scrolledtext.ScrolledText(frame_general, height=10)
            self.log_general.pack(fill="both", expand=True)
        else:
            self.log_general = None  # No se muestra ni se usa

        # Consola Backend
        frame_back = tk.LabelFrame(self.frame_logs, text="Backend")
        frame_back.pack(fill="both", expand=True, pady=(0, 5))
        self.log_back = scrolledtext.ScrolledText(frame_back, height=10)
        self.log_back.pack(fill="both", expand=True)

        # Consola Frontend
        frame_front = tk.LabelFrame(self.frame_logs, text="Frontend")
        frame_front.pack(fill="both", expand=True)
        self.log_front = scrolledtext.ScrolledText(frame_front, height=10)
        self.log_front.pack(fill="both", expand=True)

        self.proc_back = None
        self.proc_front = None

    def _crear_consola(self, parent, titulo):
        frame = tk.LabelFrame(parent, text=titulo)
        frame.pack(side="left", fill="both", expand=True, padx=5)
        consola = scrolledtext.ScrolledText(frame, height=20)
        consola.pack(fill="both", expand=True)
        return consola

    def _seleccionar_archivo(self):
        global BASE_DIR

        archivo = filedialog.askopenfilename(filetypes=[("Base de Datos Access", "*.mdb")])
        if archivo:
            self.base_path.set(archivo)
            BASE_DIR = os.path.dirname(archivo)
            self._guardar_config()
            self._verificar_estado_instalacion()

    def _guardar_config(self):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump({"base_path": self.base_path.get()}, f)

    def _cargar_config(self):
        global BASE_DIR

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.base_path.set(data.get("base_path", ""))
                BASE_DIR = os.path.dirname(self.base_path.get()) if self.base_path.get() else None
    
    def _verificar_estado_instalacion(self):
        python_ok = os.path.exists(PYTHON_DIR)
        node_ok = existe_node()
        base_ok = os.path.exists(self.base_path.get())

        if not (python_ok and node_ok):
            self.btn_iniciar.config(state="normal" if base_ok else "disabled")
            self.btn_start_back.config(state="disabled")
            self.btn_start_front.config(state="disabled")
        else:
            self.btn_iniciar.config(state="disabled")
            self.btn_start_back.config(state="normal")
            self.btn_start_front.config(state="normal")
            self.btn_stop_back.config(state="normal")
            self.btn_stop_front.config(state="normal")

            # Si tiene todo instalado, iniciar backend y frontend automáticamente
            if base_ok:
                self._log(self.log_back, "Iniciando backend automáticamente...")
                self._start_backend()
                self._log(self.log_front, "Iniciando frontend automáticamente...")
                self._start_frontend()

    def _iniciar_instalacion(self):
        self._log(self.log_general, "Iniciando instalación...")
        def instalacion():
            self.btn_iniciar.config(state="disabled")
            self._log(self.log_general, "Instalando backend...")
            
            ejecutar_instalacion_backend(
                self.base_path.get(),
                self._log_callback(self.log_back),
                self._log_callback(self.log_general)
            )
            self._log(self.log_general, "Instalación del backend completada.")
            
            self._log(self.log_general, "Instalando frontend...")
            ejecutar_instalacion_frontend(
                self._log_callback(self.log_front),
                self._log_callback(self.log_general)
            )
            self._log(self.log_general, "Instalación del frontend completada.")
            
            self._verificar_estado_instalacion()
        threading.Thread(target=instalacion, daemon=True).start()

    def _start_backend(self):
        self.btn_start_back.config(state="disabled")
        self._log(self.log_back, "Iniciando servidor backend...")
        self._kill_port(3001)

        from back import VENV_PATH  # Importar BASE_DIR desde el módulo back
        python_exe = os.path.abspath(os.path.join(f"{VENV_PATH}/Scripts/", "python.exe"))

        self.proc_back = subprocess.Popen(
            [python_exe, "-m", "uvicorn", "api:app", "--port", "3001"],
            cwd="HostBase",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        def leer_backend():
            for linea in self.proc_back.stdout:
                self._log(self.log_back, linea.strip())


        self.hilo_back = threading.Thread(target=leer_backend, daemon=True)
        self.hilo_back.start()

    def _start_frontend(self):
        def tarea_frontend():
            self._kill_port(3000)
            self._log(self.log_front, "🏗️ Compilando frontend (next build)...")

            npm_cmd = shutil.which("npm")
            if not npm_cmd:
                print("❌ No se encontró Node.js (npm). ¿Está instalado correctamente?")
            else:
                print(f"✅ npm encontrado en: {npm_cmd}")

            # 0. Instalar dependencias
            self._log(self.log_front, "📦 Instalando dependencias (npm install)...")
            proceso_install = subprocess.Popen(
                [npm_cmd, "install"],
                cwd="frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
            )

            for linea in proceso_install.stdout:
                self._log(self.log_front, f"[install] {linea.strip()}")

            proceso_install.wait()
            self._log(self.log_front, "✅ npm install finalizado.")

            # 1. Compilar
            proceso_build = subprocess.Popen(
                [npm_cmd, "run", "build"],
                cwd="frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
            )

            for linea in proceso_build.stdout:
                self._log(self.log_front, f"[build] {linea.strip()}")

            proceso_build.wait()
            self._log(self.log_front, "✅ Build finalizado. Iniciando servidor de producción...")

            # 2. Iniciar servidor de producción
            self.proc_front = subprocess.Popen(
                [npm_cmd, "run", "start"],
                cwd="frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
            )

            try:
                for linea in self.proc_front.stdout:
                    self._log(self.log_front, f"[serve] {linea.strip()}")
            except Exception as e:
                print(f"Error al leer salida del servidor frontend: {e}")

        # Lanzar todo en hilo aparte
        self.btn_start_front.config(state="disabled")
        self.hilo_front = threading.Thread(target=tarea_frontend, daemon=True)
        self.hilo_front.start()

    def _stop_backend(self):
        self.btn_start_back.config(state="normal")
        self._kill_port(3001)
        if hasattr(self, "proc_back") and self.proc_back and self.proc_back.poll() is None:
            self._log(self.log_back, "🛑 Deteniendo backend...")
            self.proc_back.terminate()
            self.proc_back.wait()
            self._log(self.log_back, "✅ Backend detenido.")

    def _stop_frontend(self):
        self.btn_start_front.config(state="normal")
        self._kill_port(3000)
        if hasattr(self, "proc_front") and self.proc_front and self.proc_front.poll() is None:
            self._log(self.log_front, "🛑 Deteniendo frontend...")
            os.kill(self.proc_front.pid, signal.CTRL_BREAK_EVENT)
            self.proc_front.wait()
            self._log(self.log_front, "✅ Frontend detenido.")

    def _cerrar_aplicacion(self):
        self.CORRER = False
        self._kill_port(3001)
        self._kill_port(3000)
        self._stop_backend()
        self._stop_frontend()
        self.root.destroy()

    def _log(self, consola, texto):
        try:
            consola.insert(tk.END, texto + "\n")
            consola.see(tk.END)
        except Exception as e:
            print(f"Error al escribir en la consola: {e}")

    def _log_callback(self, consola):
        return lambda texto: self._log(consola, texto)

    import subprocess

    def _kill_port(self, puerto=3000):
        try:
            # Verificamos si hay algo usando el puerto (sin abrir ventana)
            output = subprocess.check_output(
                f'netstat -ano | findstr :{puerto}',
                shell=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            lines = output.strip().split('\n')

            procesos_terminados = 0
            for line in lines:
                if 'LISTENING' in line or 'ESTABLISHED' in line:
                    pid = line.strip().split()[-1]
                    subprocess.run(
                        ["taskkill", "/PID", pid, "/F"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    procesos_terminados += 1

            if procesos_terminados > 0:
                self._log(self.log_front, f"✅ Puerto {puerto} liberado. Procesos finalizados: {procesos_terminados}")
            else:
                self._log(self.log_front, f"ℹ️ Puerto {puerto} estaba libre.")

        except subprocess.CalledProcessError:
            self._log(self.log_front, f"ℹ️ Puerto {puerto} está libre. No se realizaron acciones.")
        except Exception as e:
            self._log(self.log_front, f"❌ Error al intentar liberar el puerto {puerto}: {e}")




if __name__ == "__main__":
    root = tk.Tk()
    app = InstaladorApp(root)
    root.mainloop()
