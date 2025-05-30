# Sistema de Comandera con FastAPI y Microsoft Access

Este proyecto permite conectar una base de datos Microsoft Access (`sifare.mdb`) con un servidor local en Python mediante FastAPI. Ideal para sistemas de restaurante, pedidos en red local, y gestión rápida desde una interfaz web.

---

## ⚠️ Requisitos Importantes

* Python 32 bits (**obligatorio**) para usar `Microsoft.Jet.OLEDB.4.0`
* Base de datos Access `.mdb` con clave
* Entorno virtual 32 bits (`venv32`) ya creado dentro de `HostBase`
* Librerías necesarias:

  ```bash
  pip install fastapi uvicorn pywin32
  ```

---

## 🚀 Comandos para levantar el servidor

### 1. Crear entorno virtual (solo si no existe)

```bash
& 'C:\Users\franc\AppData\Local\Programs\Python\Python313-32\python.exe' -m venv venv32
```

### 2. Activar entorno virtual

```bash
.\venv32\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install fastapi uvicorn pywin32
```

### 4. Levantar el servidor

```bash
uvicorn api:app --port 3000 --reload
```

---

## 🌐 Endpoints Disponibles

### 1. `POST /api/{tabla}`

* Ejecuta una consulta SQL (SELECT / INSERT / DELETE / etc)
* Requiere en el `body`:

  ```json
  { "query": "SELECT * FROM meseros" }
  ```
* Devuelve:

  ```json
  {
    "status": "ok",
    "query": "...",
    "res": [...] // Resultado o mensaje
  }
  ```

### 2. `GET /api/base`

* Devuelve estructura completa de la base:

  * Nombre de cada tabla
  * Columnas
  * Ejemplos con 3 filas

### 3. `GET /api/select/{tabla}?limit=50`

* Devuelve registros de una tabla ordenados por `id DESC`
* Soporta parámetro `?limit=50` (default: 100)

---

## 🗂️ Estructura de la Base de Datos

### Tablas principales:

#### `meseros`

* `me_cod`, `me_des`, `me_ide`, `me_tip`, `me_touche`
* Ejemplo:

  ```json
  { "me_cod": "1", "me_des": "SANTIAGO M", "me_ide": "1" }
  ```

#### `mesas`

* `mes_cod`, `mes_nom`, `mes_caj`, `mes_are`, `mes_tip`

#### `productos`

* `pro_cod`, `pro_des`, `pro_val`, `pro_cat`, `pro_inv`, etc.

#### `cocina`

* Tabla de pedidos
* Requiere campos como:

  * `coc_con`, `coc_mes`, `coc_pro`, `coc_obs`, `coc_can`, `coc_val`, `coc_mese`, `coc_hor`, etc.

---

## ✅ Características del Sistema

* La conexión con la base se realiza **solo cuando se hace una consulta**.
* No hay conexión persistente: ¡la base se libera inmediatamente!
* Se puede consumir desde Next.js o cualquier frontend local

---

## 📁 Estructura de carpetas esperada

```
HostBase/
├── api.py               # Archivo principal de FastAPI
├── sifare.mdb           # Base de datos Access protegida
├── venv32/              # Entorno virtual de 32 bits
```

---

## 🧪 Probar consulta de prueba

POST a:

```
http://localhost:3000/api/meseros
```

Body:

```json
{ "query": "SELECT * FROM meseros" }
```

---

## 🔐 Seguridad y Simplicidad

* Se evita bloqueo de archivos
* Compatible con apps en frontend como Next.js
* Rápido para desarrollo en red local o intranet de restaurante

---

Hecho para trabajar con sistemas simples, rápidos y sin dependencias pesadas. ✨
