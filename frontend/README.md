## Introducción al Frontend de Comandera 🎯💻✨

Este proyecto frontend está desarrollado utilizando **Next.js**, un framework de React que permite renderizado híbrido (SSR y SSG), ideal para aplicaciones web modernas. 🧩🚀📘

---

## 📁 Estructura General del Proyecto

### Estructura de Carpetas 📂🗂️📁

🔹 **.next/**: Carpeta generada automáticamente por Next.js que contiene los archivos de build y cache. No debe ser modificada manualmente.

🔹 **components/**: Aquí se ubican todos los componentes reutilizables de la interfaz (botones, modales, tarjetas, etc.). Se divide por responsabilidad o tipo de componente.

🔹 **node\_modules/**: Contiene todas las dependencias instaladas mediante NPM. No se debe editar directamente.

🔹 **pages/**: Esta carpeta es clave en Next.js. Cada archivo representa una ruta (URL) dentro de la aplicación. Por ejemplo:

* `index.js`: pantalla de login.
* `mesas.js`: muestra todas las mesas disponibles.
* `[mesa].js`: genera la vista de un pedido específico.

🔹 **public/**: Archivos estáticos como imágenes, íconos o fuentes. Todo lo que se coloque aquí es accesible desde el navegador.

🔹 **styles/**: Contiene los estilos CSS. Se utiliza CSS Modules para mantener el scope local en cada componente y evitar colisiones de estilos. 🎨🧵📌

---

## 📄 Archivos Principales del Proyecto

🔸 **\_app.js**: Punto de entrada general de la aplicación. Carga los estilos globales y renderiza el componente actual.

🔸 **\_document.js**: Define la estructura HTML base personalizada que Next.js usa en todas las páginas. Se puede modificar aquí el `<head>`, el `<body>`, etc.

🔸 **.env.local**: Variables de entorno locales (como URLs de backend, claves, etc.). Nunca debe subirse al repositorio.

🔸 **jsconfig.json**: Define rutas absolutas de importación, útil para no usar rutas relativas largas.

🔸 **next.config.mjs**: Archivo de configuración de Next.js.

🔸 **package.json / package-lock.json**: Administran las dependencias y scripts del proyecto.

🔸 **README.md**: Documentación inicial del proyecto. 📘📝📂

---

## 🚀 Cómo ejecutar el proyecto localmente 🧪🖥️📊

1. Asegúrate de tener **Node.js** instalado.
2. Abre una terminal en el directorio `frontend/`.
3. Instala las dependencias:

   ```bash
   npm install
   ```
4. Crea un archivo `.env.local` con las variables necesarias.
5. Inicia el servidor de desarrollo:

   ```bash
   npm run dev
   ```
6. Abre el navegador y visita:

   ```
   http://localhost:3000
   ```

---

## ✅ Conclusión

Con esta estructura clara y modular, el desarrollo y mantenimiento del frontend se vuelve mucho más eficiente y escalable. 🧠🔧📈


---
---
---

## Documentación de las Páginas del Usuario 🧑‍🍳📲🖥️

La aplicación está compuesta por tres páginas principales que el usuario (mesero) puede visualizar. A continuación se detalla qué muestra cada una, qué funcionalidades ofrece y cómo se pueden editar sus estilos visuales.

---

## 🏠 Página de Inicio (/index.js)

### ¿Qué ve el usuario?

* Formulario de login con campos para ID del mesero y clave.
* Acceso directo a perfiles previamente guardados en cookies.
* Logo de la aplicación y un mensaje de bienvenida.
* Mensajes de error si las credenciales no son correctas.

### ¿Dónde se editan los estilos?

* Archivo de estilos: `styles/index.module.css`
* Componentes afectados: `.container`, `.card`, `.logo`, `.loginH1`, `.loginp`, `.inputLogin`, `.loginBtn`, `.errorMessage`, `.guards`

---

## 🍽️ Página de Mesas (/mesas.js)

### ¿Qué ve el usuario?

* Nombre del mesero activo.
* Botón para cerrar sesión.
* Listado visual de mesas divididas por rangos (ej: 1-20, 21-40...).
* Estado visual de cada mesa (libre u ocupada), usando íconos e imagenes.
* Campo de búsqueda por número de mesa.
* Botones para filtrar mesas por rango.

### ¿Dónde se editan los estilos?

* Archivo de estilos: `styles/mesas.module.css`
* Clases destacadas: `.container`, `.name`, `.logout`, `.mesash1`, `.buscarBox`, `.inputBuscar`, `.buscarBtn`, `.errorBuscar`, `.filtros`, `.grid`, `.mesa`, `.ocupada`, `.libre`

---

## 📝 Página de Pedido (/pedido/\[mesa].js)

### ¿Qué ve el usuario?

* Nombre del mesero activo y número de mesa.
* Botón para volver a la pantalla de mesas.
* Buscador de productos y categorías.
* Lista de productos con opción para agregar.
* Carrito visible con resumen del pedido.
* Botón para confirmar y enviar el pedido.

### ¿Dónde se editan los estilos?

* Archivo de estilos: `styles/pedido.module.css`
* Clases principales: `.container`, `.name`, `.volver`, `.titulo`

---

## 🌐 Estilos Globales (\_app.js y globals.css)

* El archivo `_app.js` importa `@/styles/globals.css`.
* Aquí se definen estilos universales que aplican a toda la app como fuentes, resets, etc.

---

## 🧱 Estructura HTML Base (\_document.js)

* `_document.js` define la estructura HTML base.
* Elementos como `<Html>`, `<Head>`, `<Main>` y `<NextScript>` se renderizan desde aquí.

---

Con esta estructura clara, cualquier desarrollador puede localizar fácilmente qué página verán los usuarios y cómo adaptar su estilo visual según la necesidad del proyecto. 🎨🛠️📲


---
---
---

## Documentación de la API de Comandera 🍽️🧾📡

La API del proyecto está estructurada dentro de la carpeta `pages/api/`, siguiendo el sistema de rutas de Next.js. A continuación, se describen cada uno de los endpoints disponibles, sus funcionalidades, los métodos que aceptan y cómo se comportan.

---

## 🔐 /api/login.js

Este endpoint permite autenticar a un mesero usando su ID y clave.

* **Método:** POST
* **Body esperado:** `{ idMesero: string, clave: string }`
* **Proceso:**

  * Realiza una consulta SQL al backend de datos (usualmente Access vía proxy API).
  * Si encuentra un match, devuelve los datos del mesero.
* **Respuestas:**

  * `200 OK` con `{ success: true, mesero }`
  * `401 Unauthorized` si las credenciales no son válidas
  * `400 Bad Request` si faltan datos

---

## 📋 /api/mesas/index.js

Devuelve todas las mesas disponibles con su estado actual (`libre` o `en_uso`).

* **Método:** GET (por estructura, aunque internamente hace una consulta POST al backend)
* **Proceso:**

  * Consulta la base de datos por mesas de tipo 'M'.
  * Asigna estado libre o en uso en función de una variable local (`actividadMesas`).
* **Respuesta:** `{ status: 'ok', mesas: [{ numero, estado, tipo }] }`

---

## 🔍 /api/mesas/\[id].js

Busca una mesa específica por su ID.

* **Método:** GET
* **Query:** `id` (en la URL)
* **Respuesta:**

  * `200 OK` con `{ status: 'ok', mesa }`
  * `404 Not Found` si no existe
  * `400 Bad Request` si el ID no es válido

---

## 🛎️ /api/mesas/online.js

Marca una mesa como en uso o libre según la actividad del mesero.

* **Método:** GET
* **Query params:** `mesa`, `user`, `delete`
* **Funcionamiento:**

  * Si `delete` está presente, libera la mesa.
  * Si no, marca la mesa como activa y guarda al mesero responsable.
* **Respuesta:**

  * `200 OK` con estado actualizado o mensaje de liberación

---

## 🥘 /api/pedido/index.js ✅ (ENDPOINT PRINCIPAL)

Este es el núcleo del sistema de pedidos. Se encarga de insertar los productos del pedido en la base de datos y manejar el rollback si algo falla.

* **Método:** POST
* **Body esperado:**

```json
{
  "mesa": "12",
  "mesero": { "me_cod": "123" },
  "items": [
    { "id": "456", "nombre": "Coca Cola", "cantidad": 2, "observacion": "Sin hielo", "total": 6.00 }
  ]
}
```

* **Funcionamiento:**

  1. Construye múltiples queries `INSERT` para cada ítem al sistema de cocina.
  2. Si alguna falla, ejecuta un rollback eliminando los registros del lote (`coc_car` como batch ID).
  3. Si todo va bien, responde con la cantidad total de ítems insertados.
* **Respuestas:**

  * `200 OK` con `{ status: 'ok', cantidad }`
  * `500 Error` con rollback si algo falla

---

## 🧾 /api/pedido/categoria.js

Devuelve la lista de categorías de productos.

* **Método:** GET
* **Respuesta:** `{ status: 'ok', categorias: [{ cod_cat, nom_cat }] }`

---

## 🧃 /api/pedido/productos.js

Devuelve productos aleatorios o filtrados por categoría.

* **Método:** GET
* **Query opcional:** `categoria`
* **Respuesta:** `{ status: 'ok', productos: [...] }`

---

## 🔎 /api/pedido/search.js

Busca productos por nombre.

* **Método:** GET
* **Query param:** `name`
* **Respuesta:** `{ status: 'ok', productos: [...] }`

---

Esta estructura de endpoints permite manejar toda la lógica de login, visualización de mesas, toma de pedidos y monitoreo en tiempo real de forma modular y clara. 🎯📊📱



---
---
---
