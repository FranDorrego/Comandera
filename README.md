# README Global – Sistema de Comandera 🍽️🧾🖥️

Este proyecto está compuesto por un frontend en Next.js y un backend en Python (FastAPI) que se comunica con una base de datos Microsoft Access. A continuación se detalla cómo configurar y ejecutar el entorno completo en una máquina local.

---

## ✅ Requisitos Generales del Sistema

🔹 Tener instalado **Node.js** para el frontend.

🔹 Tener instalado **Python 32 bits** para el backend (necesario para conectarse a Access).

🔹 Tener una base de datos Access válida (`sifare.mdb`) ubicada en la carpeta del backend (`HostBase/`).

🔹 Tener `Microsoft.Jet.OLEDB.4.0` habilitado (solo funciona con Python de 32 bits).

🔹 Tener creada una carpeta `venv32/` con entorno virtual de Python dentro de `HostBase`.

🔹 Tener los archivos `run_front.bat` y `run_back.bat` para ejecución rápida.

---

## 📦 Instalación y Ejecución – Frontend (Next.js)

### 1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2. Variables de entorno

Crear un archivo `.env.local` dentro de `frontend/` con el contenido necesario. Ejemplo:

```
NEXT_PUBLIC_API_BASE=http://localhost:3000
```

### 3. Ejecutar frontend (manualmente o con script)

```bash
npm run dev
```

O usando el archivo:

```bash
run_front.bat
```

Esto iniciará el servidor en:

```
http://localhost:3000
```

---

## 🐍 Instalación y Ejecución – Backend (FastAPI)

### 1. Crear entorno virtual 32 bits (solo una vez)

```bash
& 'C:\Users\franc\AppData\Local\Programs\Python\Python313-32\python.exe' -m venv venv32
```

### 2. Activar entorno

```bash
cd HostBase
.\venv32\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install fastapi uvicorn pywin32
```

### 4. Ejecutar servidor backend (manual o con .bat)

```bash
uvicorn api:app --port 3000 --reload
```

O usar el archivo:

```bash
run_back.bat
```

---

## 🗄️ Base de Datos

Ubicar el archivo `sifare.mdb` dentro de la carpeta del backend (`HostBase/`). La clave de acceso por defecto es `mery46`. No es necesario conectarla previamente, el backend se encarga de abrir y cerrar conexión cuando es necesario.

---

## 🧪 Test rápido de conexión

Puedes probar que la API funcione correctamente con:

```bash
curl -X POST http://localhost:3000/api/meseros -H "Content-Type: application/json" -d '{"query": "SELECT * FROM meseros"}'
```

---

## 📚 Visualización de documentación específica

Este README resume el funcionamiento general. Para más detalle:

🔹 Ver `frontend/README.md`: Detalla estructura, componentes y estilos del frontend.
🔹 Ver `HostBase/README.md`: Explica el backend FastAPI, los endpoints disponibles y la estructura de la base Access.

---

Con esta estructura clara y modular, podés ejecutar y mantener fácilmente el sistema de comandera completo tanto en frontend como backend. 🚀🧩🍽️
