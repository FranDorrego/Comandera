# 📦 Instalador del Sistema de Comandera – README\_install.md

Este documento explica cómo funciona el archivo `main.py` (incluido en `main.exe`), qué componentes instala automáticamente, y cómo realizar manualmente la instalación en caso de que falle algún paso del proceso automatizado.

---

## ✅ Requisitos del Sistema

Antes de ejecutar el instalador, asegurate de contar con lo siguiente:

* ✅ Windows 10 o superior (64 bits)
* ✅ Conexión a internet (para descargar Python, Node.js y Git si es necesario)
* ✅ Microsoft Access o Driver `Microsoft.Jet.OLEDB.4.0` (incluido por defecto en Windows de 32 bits)

---

## 🚀 ¿Qué hace `main.exe`?

Cuando ejecutás `main.exe`, el instalador realiza lo siguiente:

### 1. **Instala Python 32 bits** (si no está instalado):

* Descarga `python-3.10.9.exe` de [python.org](https://www.python.org/ftp/python/3.10.9/)
* Ejecuta el instalador y espera a que finalice
* Si no lo encuentra automáticamente, te pide seleccionar manualmente el ejecutable

### 2. **Crea un entorno virtual en `HostBase/venv32`**

* Usa el Python detectado para crear el entorno
* Instala las dependencias del backend desde `HostBase/requirements.txt`

### 3. **Instala Node.js v22.16.0** (si no está instalado o es muy viejo):

* Descarga el instalador MSI desde [nodejs.org](https://nodejs.org/dist/v22.16.0/)
* Ejecuta el instalador con asistente gráfico

### 4. **Instala dependencias del frontend (`npm install`)**

* Usa `npm` para instalar paquetes en la carpeta `frontend`

### 5. **Compila e inicia automáticamente el frontend y backend**

---

## 🛠 Instalación manual (por si algo falla)

Si la instalación automática falla, podés hacer lo siguiente:

### 1. Instalar Python 32 bits manualmente

* Descargar desde: [https://www.python.org/ftp/python/3.10.9/python-3.10.9.exe](https://www.python.org/ftp/python/3.10.9/python-3.10.9.exe)
* Durante la instalación:

  * Activar la opción "Add to PATH"
  * Elegir instalación para todos los usuarios

### 2. Crear entorno virtual manualmente

```bash
cd HostBase
"C:\Ruta\a\python.exe" -m venv venv32
venv32\Scripts\pip install -r requirements.txt
```

### 3. Instalar Node.js manualmente

* Descargar desde: [https://nodejs.org/dist/v22.16.0/node-v22.16.0-x64.msi](https://nodejs.org/dist/v22.16.0/node-v22.16.0-x64.msi)
* Seguir pasos del instalador

### 4. Instalar frontend manualmente

```bash
cd frontend
npm install
npm run build
```

---

## ⚙️ Ejecutar manualmente el sistema

### Iniciar el backend

```bash
cd HostBase
venv32\Scripts\python.exe -m uvicorn api:app --port 3001
```

### Iniciar el frontend

```bash
cd frontend
npm run start
```

---

## 🧠 Solución de problemas comunes

| Problema                     | Solución                                                                                       |
| ---------------------------- | ---------------------------------------------------------------------------------------------- |
| No se detecta Python         | Verificá que sea de 32 bits y esté correctamente instalado                                     |
| Error en Node.js             | Asegurate de reiniciar la PC después de instalar Node                                          |
| `sifare.mdb` no se encuentra | Asegurate de haber elegido correctamente el archivo al inicio                                  |
| Puertos ocupados             | El sistema usa los puertos **3000** (frontend) y **3001** (backend). Cerrá procesos anteriores |

---

Este sistema fue desarrollado como solución de instalación automática de una comandera local para sistemas con Microsoft Access, Node.js y FastAPI.

---

Cualquier duda o soporte técnico, escribí a: **[FrancoDorrego@gmail.com](mailto:francodorrego@gmail.com)**
