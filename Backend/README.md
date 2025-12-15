# Backend en Django para Plataforma Comercial con IA (Arquitectura por Capas)

Este backend está construido con Python y Django, siguiendo una arquitectura por capas estricta para asegurar la separación de responsabilidades y la escalabilidad, sirviendo a un frontend inmutable.

## 1. Arquitectura y Modelo de Datos

El backend se divide en capas (`bff`, `domain`, `ai`, `infrastructure`, `shared`). El modelo de datos para el Arquitecto de Embudos es el siguiente:

```markdown
- Tenant / Cadena (id, nombre, color_primario, metadata)
  - Categoria (id, tenant_id, nombre)
    - Subcategoria (id, categoria_id, nombre)
      - LandingPage (id, subcategoria_id, slug, estado)
        - Embudo (id, landing_page_id, nombre, orden, activo)
          - Pagina (id, embudo_id, tipo, orden)
            - Bloque (id, pagina_id, tipo, orden, config_json)
```
Los modelos `Embudo`, `Pagina` y `Bloque` tienen **versionado automático** para soportar Undo/Redo.

## 2. Configuración e Instalación
(Instrucciones de `venv`, `pip install`, `.env` y `migrate` se mantienen como antes)

...

## 3. API del Arquitecto de Embudos

### API Pública
---
#### `GET /api/public/funnel/{slug}/`
Obtiene la estructura completa de un embudo publicado. No requiere autenticación.

- **Respuesta Exitosa (200):**
  ```json
  {
    "slug": "mi-landing-page",
    "embudo": {
      "id": 1,
      "nombre": "Embudo Principal",
      "paginas": [
        {
          "id": 1,
          "tipo": "oferta",
          "orden": 0,
          "bloques": [
            {
              "id": 1,
              "tipo": "hero",
              "orden": 0,
              "config_json": { "title": "¡Oferta Especial!" }
            }
          ]
        }
      ]
    }
  }
  ```

### API Privada del Constructor (`/api/builder/`)
---
Requiere autenticación (Bearer Token).

#### Embudos (`/api/builder/funnels/`)
- `GET /`: Lista los embudos del tenant.
- `POST /`: Crea un nuevo embudo y su `LandingPage` asociada.
  - Body: `{"nombre_embudo": "Mi Nuevo Embudo", "subcategoria_id": 1}`
- `GET /{id}/`: Obtiene un embudo.
- `PUT /{id}/`: Actualiza un embudo.
- `DELETE /{id}/`: Elimina un embudo.
- `POST /{id}/publish/`: Publica la landing page asociada.

#### Páginas (`/api/builder/pages/`)
- `GET /`: Lista todas las páginas del tenant.
- `POST /`: Crea una nueva página para un embudo.
  - Body: `{"embudo": 1, "tipo": "oferta", "orden": 1}`
- `GET /{id}/`, `PUT /{id}/`, `DELETE /{id}/`: Gestión estándar.

#### Bloques (`/api/builder/blocks/`)
- `GET /`: Lista todos los bloques del tenant.
- `POST /`: Crea un nuevo bloque para una página.
  - Body: `{"pagina": 1, "tipo": "hero", "orden": 0, "config_json": {"title": "Nuevo Título"}}`
- `GET /{id}/`, `PUT /{id}/`, `DELETE /{id}/`: Gestión estándar.

### API de Autenticación
(Endpoints de `/api/auth/register/`, `/api/auth/token/`, etc. se mantienen como antes)
...
