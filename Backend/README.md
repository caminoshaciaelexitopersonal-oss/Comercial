# Backend en Django para Plataforma Comercial con IA (Arquitectura por Capas)

Este backend está construido con Python y Django, siguiendo una arquitectura por capas estricta para asegurar la separación de responsabilidades y la escalabilidad.

## 1. Arquitectura

El backend se divide en las siguientes capas:

-   **`bff/`**: Backend For Frontend. Actúa como un adaptador que expone APIs específicas para las necesidades del frontend. No contiene lógica de negocio.
-   **`domain/`**: El corazón de la aplicación. Contiene la lógica y las reglas de negocio puras, sin conocimiento de la UI o la base de datos.
-   **`ai/`**: Módulo independiente y agnóstico para interactuar con cualquier proveedor de IA.
-   **`infrastructure/`**: Se encarga de la persistencia de datos (modelos, migraciones) y la comunicación con la base de datos.
-   **`shared/`**: Contiene utilidades, DTOs y excepciones comunes a todas las capas.

## 2. Configuración e Instalación

### Prerrequisitos
- Python 3.12, `pip`, `venv`

### Pasos
1.  **Navegar al Directorio**:
    ```bash
    cd Backend
    ```
2.  **Crear y Activar Entorno Virtual**:
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    ```
3.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configurar Variables de Entorno**:
    Crea un archivo `.env` en el directorio `Backend` y añade las siguientes variables:
    ```env
    # Clave secreta de Django. Puedes generar una con:
    # python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    DJANGO_SECRET_KEY="tu_clave_secreta_aqui"

    # (Opcional) Habilitar modo DEBUG para desarrollo. Por defecto es False.
    DJANGO_DEBUG="True"

    # (Opcional) Claves para proveedores de IA
    GEMINI_API_KEY="tu_clave_de_api_de_gemini"
    OLLAMA_ENDPOINT="http://localhost:11434"
    ```
5.  **Aplicar Migraciones de la Base de Datos**:
    ```bash
    python manage.py migrate
    ```
6.  **Ejecutar el Servidor**:
    ```bash
    python manage.py runserver
    ```
    El servidor estará disponible en `http://127.0.0.1:8000/`.

## 3. API de Autenticación (Fase 1)

Todos los endpoints están prefijados con `/api/bff/`.

### `POST /api/bff/auth/register/`
Registra un nuevo usuario y crea un Tenant asociado a él.

-   **Body:**
    ```json
    {
        "username": "nuevo_usuario",
        "password": "una_contraseña_segura",
        "email": "usuario@ejemplo.com",
        "tenant_name": "Mi Organización"
    }
    ```
-   **Respuesta Exitosa (201):**
    ```json
    {
        "message": "User 'nuevo_usuario' registered successfully."
    }
    ```

### `POST /api/bff/auth/token/`
Autentica a un usuario y devuelve un par de tokens (acceso y refresco).

-   **Body:**
    ```json
    {
        "username": "nuevo_usuario",
        "password": "una_contraseña_segura"
    }
    ```
-   **Respuesta Exitosa (200):**
    ```json
    {
        "access": "ey...",
        "refresh": "ey..."
    }
    ```

### `POST /api/bff/auth/token/refresh/`
Refresca un token de acceso expirado usando un token de refresco.

-   **Body:**
    ```json
    {
        "refresh": "ey..."
    }
    ```
-   **Respuesta Exitosa (200):**
    ```json
    {
        "access": "ey..."
    }
    ```

## 4. API de la Fase 2 (CRUD)

### Campañas (`/api/bff/campaigns/`)

-   **`GET /`**: Lista todas las campañas del tenant del usuario autenticado.
-   **`POST /`**: Crea una nueva campaña.
    -   Body: `{"name": "Mi Nueva Campaña", "goal": "El objetivo."}`
-   **`GET /{id}/`**: Obtiene los detalles de una campaña específica.
-   **`PUT /{id}/`**: Actualiza una campaña.
-   **`DELETE /{id}/`**: Elimina una campaña.
