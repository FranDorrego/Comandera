# README Global – Sistema de Comandera 🍽️📜🖥️

Este proyecto está compuesto por un frontend en Next.js y un backend en Python (FastAPI) que se comunica con una base de datos Microsoft Access. A continuación se detalla cómo configurar y ejecutar el entorno completo en una máquina local. Además, se describe el sistema automatizado de instalación y despliegue.

---

## ✅ Requisitos Generales del Sistema

🔸📦 Tener instalado **Node.js** (el sistema lo descarga e instala globalmente si no está presente o si la versión es antigua).

🔸🐍 Tener instalado **Python 32 bits** (el sistema lo descarga e instala globalmente si no está presente).

🔸📁 Tener una base de datos Access válida (`sifare.mdb`) ubicada en la carpeta del backend (`HostBase/`).

🔸🧩 Tener `Microsoft.Jet.OLEDB.4.0` habilitado (solo funciona con Python de 32 bits).

🔸🛠️ Tener creada una carpeta `venv32/` con entorno virtual de Python dentro de `HostBase` (el sistema la crea automáticamente si no existe).

🔸⚙️ Tener los archivos `run_front.bat` y `run_back.bat` para ejecución rápida.

---

## 🛠️ Sistema de Auto Configuración – Sistema de Comandera

El archivo `main.exe` permite ejecutar y actualizar automáticamente todo el sistema de Comandera con solo hacer doble clic, sin requerir conocimientos técnicos. Ya no se utiliza un instalador externo.

---

## 📁 Estructura de Carpetas

```
📦 Comandera/
├── main.exe                 ← Lanzador principal con interfaz Tkinter
├── HostBase/                ← Backend en Python + base Access
├── frontend/                ← Proyecto Next.js
├── setup/config.json        ← Ruta seleccionada por el usuario
```

---

## 🚦 Flujo de Ejecución del Sistema

🔹 Ejecución de `main.exe`:

* Verifica si existen Python y Node.js:

  * Si no existen, los descarga desde los sitios oficiales e inicia sus instaladores globales.
  * Si existen pero son versiones viejas, también se reinstalan.
  * El usuario debe completar la instalación visual.

* Luego:

  * Crea entorno virtual si no existe.
  * Instala dependencias Python (`pip install`).
  * Instala dependencias Node (`npm install`).
  * Compila frontend (`npm run build`).
  * Lanza frontend y backend como hilos daemon.

---

## 🐍 Python (32 bits) – Instalación y Uso

* Se descarga automáticamente desde python.org si no está presente.
* Instalación visual, el usuario debe completarla.
* Luego se usa para:

  * Crear `venv32/` en `HostBase/`.
  * Instalar dependencias de `requirements.txt`.

✅ Compatible con Access gracias a `pywin32` y `Microsoft.Jet.OLEDB.4.0`.

---

## 🌐 Node.js – Instalación y Uso

* Se descarga automáticamente desde nodejs.org si no está presente o si la versión es más antigua que la requerida.
* Instalación visual, el usuario debe completarla.
* Luego ejecuta:

  ```bash
  npm install
  npm run build
  npm run start
  ```

🧠 Configuración Persistente: `setup/config.json`

🚨 Prevención de errores:

* Detecta puerto 3000 ocupado (Next.js) y lo libera con `taskkill /F`.
* Ejecuta backend y frontend como hilos secundarios daemon (se cierran al salir).

🔁 Auto-Actualización:

* Ejecuta `git reset --hard` y actualiza repositorio.

---

## 📦 Instalación y Ejecución – Frontend (Next.js)

1. Instalar dependencias:

```bash
cd frontend
npm install
```

2. Variables de entorno:
   Crear `.env.local` en `frontend/`:

```
NEXT_PUBLIC_API_BASE=http://localhost:3000
```

3. Ejecutar frontend:

```bash
npm run dev
```

O usar:

```bash
run_front.bat
```

Acceder en: `http://localhost:3000`

---

## 🐍 Instalación y Ejecución – Backend (FastAPI)

1. Crear entorno virtual:

```bash
& 'C:\Path\Python313-32\python.exe' -m venv venv32
```

2. Activar entorno:

```bash
cd HostBase
.\venv32\Scripts\Activate.ps1
```

3. Instalar dependencias:

```bash
pip install fastapi uvicorn pywin32
```

4. Ejecutar servidor backend:

```bash
uvicorn api:app --port 3000 --reload
```

O usar:

```bash
run_back.bat
```

---

## 🗄️ Base de Datos

* Ubicar `sifare.mdb` dentro de `HostBase/`.
* Clave por defecto: `*********`.
* El backend se encarga de abrir/cerrar la conexión.

---

## 🧪 Test rápido de conexión

```bash
curl -X POST http://localhost:3000/api/meseros \
-H "Content-Type: application/json" \
-d '{"query": "SELECT * FROM meseros"}'
```

---

## 📚 Visualización de documentación específica

* `frontend/README.md`: Estructura y estilos del frontend.
* `HostBase/README.md`: Endpoints FastAPI y estructura de la base Access.

---

Con esta estructura clara y modular, podés ejecutar y mantener fácilmente el sistema de comandera completo tanto en frontend como backend. 🚀🧩🍽️
