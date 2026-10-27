# Flask API - Servidor Local en Docker

Este es un servidor web minimalista desarrollado en **Flask** que se ejecuta de forma aislada dentro de un contenedor de **Docker**, utilizando un entorno virtual (**venv**) de Python para la gestión local de dependencias. 

Actualmente, el proyecto funciona como una estructura base limpia y expone un endpoint de verificación de estado (*Health Check*).

---

## 🚀 Características Básicas

*   **Framework:** Flask (Python).
*   **Entorno local:** Aislado mediante `venv`.
*   **Contenedor:** Dockerizado para producción/desarrollo uniforme.
*   **Puerto:** `8000` (mapeado localmente).

---

## 🛠️ Endpoints Disponibles

Al levantar el servidor, puedes interactuar con las siguientes rutas desde tu navegador o cliente API (como Postman/Insomnia):

| Método | Ruta | Descripción | Respuesta (JSON) |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Ruta raíz de la API | `{"message": "Hola desde mi API"}` |
| `GET` | `/health` | Verificación de estado del servidor | `{"status": "ok"}` |

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado en tu computadora:
*   [Python 3.12+](https://python.org)
*   [Docker](https://docker.com)

---

## 🔧 Levantamiento del Proyecto

### 1. Clonar o acceder al proyecto
Abre tu terminal y colócate en la carpeta raíz del proyecto:
```bash
cd tu-carpeta-del-proyecto
```

### 2. Entorno Virtual Local (Opcional - Para desarrollo local)
Si deseas trabajar en tu código fuera de Docker o ver las sugerencias de tu editor (IDE), inicializa el entorno virtual:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows (CMD/PowerShell):
.\venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# Instalar las librerías necesarias localmente
pip install -r requirements.txt
```

### 3. Construir la Imagen de Docker
Para empaquetar la aplicación con la estructura optimizada multi-etapa, ejecuta:
```bash
docker build -t flask-api-local .
```

### 4. Encender el Contenedor
Corre el contenedor mapeando el puerto `8000` de tu computadora al puerto `8000` interno del contenedor:
```bash
docker run -d -p 8000:8000 --name mi_servidor_flask flask-api-local
```

¡Listo! Abre tu navegador e ingresa a [http://localhost:8000/health](http://localhost:8000/health) para verificar que el JSON responda correctamente.

---

## 🛑 Comandos de Utilidad

Si necesitas gestionar el ciclo de vida del contenedor, utiliza estos comandos básicos:

*   **Verificar si el contenedor está corriendo:**
    ```bash
    docker ps
    ```
*   **Detener el servidor:**
    ```bash
    docker stop mi_servidor_flask
    ```
*   **Volver a encenderlo (si ya existe):**
    ```bash
    docker start mi_servidor_flask
    ```
*   **Eliminar el contenedor para actualizar código:**
    ```bash
    docker rm -f mi_servidor_flask
    ```

---

## 📝 Notas de Personalización
*   Este archivo está listo para ser expandido a medida que agregues lógica de negocio, bases de datos o nuevas variables de entorno.
