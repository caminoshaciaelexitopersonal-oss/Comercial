# Backend para Plataforma Comercial con IA

Este backend está diseñado para servir como una capa de servicio robusta y segura para la plataforma comercial, gestionando múltiples proveedores de Inteligencia Artificial y exponiendo una API modular para interactuar con el frontend.

## Arquitectura

El backend sigue una arquitectura modular para reflejar la estructura de componentes del frontend.

-   **`src/components`**: Contiene la lógica de negocio y las rutas de API específicas para cada módulo funcional de la plataforma (ej. `contentStudio`).
-   **`src/core/ai`**: Es el corazón del sistema de IA.
    -   **`AIManager.ts`**: Un gestor central que inicializa y proporciona acceso a los diferentes proveedores de IA.
    -   **`IAiProvider.ts`**: Una interfaz que define un contrato estándar para todos los proveedores de IA, garantizando que se puedan intercambiar fácilmente.
    -   **`providers/`**: Contiene las implementaciones concretas para cada servicio de IA (Gemini, Ollama, etc.).
-   **`src/config`**: Centraliza la configuración de la aplicación, como las claves de API.
-   **`src/services`**: Contiene servicios para interactuar con APIs externas, como `OllamaService`.
-   **`src/routes`**: Define las rutas de la API que no pertenecen a un componente específico.

## 1. Primeros Pasos

### Prerrequisitos

-   [Node.js](https://nodejs.org/) (versión 16 o superior)
-   Un servidor [Ollama](https://ollama.com/) corriendo (si se desea usar esta funcionalidad).

### Instalación

1.  Navega a la carpeta `Backend`:
    ```bash
    cd Backend
    ```
2.  Instala las dependencias:
    ```bash
    npm install
    ```

## 2. Configuración

El backend gestiona todas las claves de API y configuraciones a través de variables de entorno.

1.  Crea un archivo llamado `.env` en la raíz de la carpeta `Backend`.

2.  Añade las siguientes variables al archivo `.env`, rellenando los valores según sea necesario:

    ```env
    # Puerto en el que correrá el servidor del backend
    PORT=3001

    # Clave de API para Google Gemini
    GEMINI_API_KEY=tu_clave_de_api_de_gemini

    # (Opcional) Clave de API para OpenAI
    # OPENAI_API_KEY=tu_clave_de_api_de_openai

    # (Opcional) Endpoint para tu servidor local de Ollama
    # Si no se especifica, se usará http://localhost:11434 por defecto
    OLLAMA_ENDPOINT=http://localhost:11434
    ```

    **Importante:** El backend solo habilitará los proveedores de IA para los que se haya proporcionado una clave de API o un endpoint válido.

## 3. Ejecutar el Servidor

-   **Para desarrollo (con recarga automática):**
    ```bash
    npm run dev
    ```
    El servidor se iniciará en el puerto especificado en el archivo `.env` (o en el 3001 por defecto).

-   **Para producción:**
    ```bash
    # 1. Compilar el código TypeScript a JavaScript
    npm run build

    # 2. Iniciar el servidor desde los archivos compilados en la carpeta /dist
    npm start
    ```

## 4. Referencia de la API

### Gestión de IA

---

#### `GET /api/ai/providers`

Obtiene una lista de los proveedores de IA que han sido inicializados con éxito en el backend.

-   **Respuesta Exitosa (200):**
    ```json
    ["gemini", "ollama"]
    ```

### Content Studio

---

#### `POST /api/content-studio/generate-text`

Genera texto utilizando el proveedor de IA especificado.

-   **Body (JSON):**
    ```json
    {
      "provider": "gemini", // o "ollama"
      "params": {
        "model": "gemini-1.5-flash", // o "llama3" para ollama
        "prompt": "Escribe un eslogan para una nueva marca de café."
      }
    }
    ```
-   **Respuesta Exitosa (200):**
    ```json
    {
      "result": "Café 'Amanecer': Tu día empieza aquí."
    }
    ```

#### `POST /api/content-studio/generate-image`

Genera una imagen. (Nota: La implementación es conceptual y depende del modelo).

-   **Body (JSON):**
    ```json
    {
      "provider": "gemini",
      "params": {
        "model": "imagen-4.0-generate-001",
        "prompt": "Un astronauta en un caballo en la luna, estilo fotorrealista."
      }
    }
    ```
-   **Respuesta Exitosa (200):**
    ```json
    {
      "imageUrl": "data:image/jpeg;base64,..."
    }
    ```

### Gestión de Ollama

---

#### `GET /api/ollama/models`

Obtiene la lista de modelos que están descargados en el servidor de Ollama.

-   **Respuesta Exitosa (200):**
    ```json
    [
      {
        "name": "llama3:latest",
        "modified_at": "2024-05-15T14:00:00Z",
        "size": 4700000000
      }
    ]
    ```

#### `POST /api/ollama/models/pull`

Inicia la descarga (pull) de un nuevo modelo en el servidor de Ollama. La operación es asíncrona.

-   **Body (JSON):**
    ```json
    {
      "modelName": "phi3"
    }
    ```
-   **Respuesta Exitosa (202 Accepted):**
    ```json
    {
      "status": "Model pull for 'phi3' initiated."
    }
    ```

## Extensibilidad

Para añadir un nuevo proveedor de IA:
1.  Crea una nueva clase en `src/core/ai/providers/` que implemente la interfaz `IAiProvider`.
2.  Añade su configuración en `src/config/ai-config.ts`.
3.  Importa e inicializa el nuevo proveedor en el `AIManager.ts`.
