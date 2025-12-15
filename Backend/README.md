# Backend en Django para Plataforma Comercial con IA

Este backend está construido con Python y Django para servir como una capa de servicio de IA robusta y modular. Gestiona múltiples proveedores de IA y expone una API RESTful para el frontend.

## Arquitectura

-   **`main_config/`**: El proyecto principal de Django.
-   **`api/`**: La app de Django que contiene toda la lógica de la API.
    -   **`components/`**: Lógica de negocio específica por módulo.
    -   **`services/ai_manager/`**: El núcleo del sistema de IA, con un gestor y proveedores intercambiables.
    -   **`views/`**: Vistas de Django REST Framework que manejan las peticiones HTTP.
    -   **`serializers.py`**: Serializadores para la validación y formato de datos de la API.
    -   **`urls.py`**: Definiciones de las rutas de la API.

## 1. Primeros Pasos

### Prerrequisitos

-   Python 3.12
-   `pip` y `venv`
-   Un servidor [Ollama](https://ollama.com/) corriendo (para la funcionalidad de Ollama).

### Instalación

1.  Navega a la carpeta `Backend`:
    ```bash
    cd Backend
    ```

2.  Crea y activa un entorno virtual de Python:
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    ```

3.  Instala las dependencias desde el archivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## 2. Configuración

1.  Crea un archivo llamado `.env` en la raíz de la carpeta `Backend`.

2.  Añade las siguientes variables de entorno:

    ```env
    # Clave secreta de Django. Puedes generar una nueva con `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
    DJANGO_SECRET_KEY="tu_clave_secreta_aqui"

    # Clave de API para Google Gemini
    GEMINI_API_KEY="tu_clave_de_api_de_gemini"

    # Endpoint para tu servidor local de Ollama
    OLLAMA_ENDPOINT="http://localhost:11434"
    ```
    El `AIManager` solo inicializará los proveedores para los que se proporcionen las credenciales.

## 3. Ejecutar el Servidor

1.  Aplica las migraciones de Django (necesario la primera vez):
    ```bash
    python manage.py migrate
    ```

2.  Inicia el servidor de desarrollo de Django:
    ```bash
    python manage.py runserver
    ```
    El servidor se iniciará en `http://127.0.0.1:8000/`.

## 4. Referencia de la API

Todos los endpoints están prefijados con `/api/`.

### Gestión de IA y Ollama

---

#### `GET /api/ai/providers/`
Obtiene la lista de los proveedores de IA disponibles.
-   **Respuesta Exitosa (200):** `["gemini", "ollama"]`

#### `GET /api/ollama/models/`
Lista los modelos descargados en el servidor de Ollama.
-   **Respuesta Exitosa (200):** `[{"name": "llama3:latest", ...}]`

#### `POST /api/ollama/models/pull/`
Inicia la descarga de un nuevo modelo en Ollama.
-   **Body:** `{"model_name": "phi3"}`
-   **Respuesta Exitosa (202):** `{"status": "Model pull for 'phi3' initiated."}`

### Content Studio

---

#### `POST /api/content-studio/generate-text/`
Genera texto con un proveedor de IA.
-   **Body:**
    ```json
    {
        "provider": "gemini",
        "model": "gemini-1.5-flash",
        "prompt": "Escribe un eslogan para una cafetería."
    }
    ```
-   **Respuesta Exitosa (200):** `{"result": "El mejor café para tus mañanas."}`

#### `POST /api/content-studio/generate-image/`
Genera una imagen con un proveedor de IA.
-   **Body:**
    ```json
    {
        "provider": "gemini",
        "model": "imagen-4.0",
        "prompt": "Un gato en una nave espacial."
    }
    ```
-   **Respuesta Exitosa (200):** `{"image_url": "data:image/jpeg;base64,..."}`
