# FASE 5: Informe Técnico del Motor de Ejecución de Embudos

## 1. Resumen Ejecutivo

Esta fase ha consistido en la creación del "Funnel Runtime Engine", un sistema de backend diseñado para ejecutar los embudos de marketing diseñados en el frontend. El objetivo principal ha sido transformar los diseños visuales en procesos operativos capaces de capturar leads y registrar eventos.

**El objetivo se ha cumplido.** El sistema ahora puede publicar un embudo, procesar un evento de envío de formulario, crear un lead persistente en la base de datos y registrar su estado.

## 2. Diagrama de Flujo del Motor de Ejecución

El motor opera basado en eventos. El siguiente diagrama ilustra el flujo para un evento `FORM_SUBMIT`:

```
[Cliente/Usuario]
      |
      | 1. POST /api/runtime/events/ (con slug, event_type, payload)
      v
[FunnelEventView] (runtime_views.py)
      |
      | 2. Valida el evento
      | 3. Llama a process_event()
      v
[Funnel Runtime Engine] (runtime/engine.py)
      |
      | 4. Busca la `FunnelPublication` activa por slug
      | 5. Determina el tipo de evento (FORM_SUBMIT)
      | 6. Delega a execute_form_submit()
      v
[Executor] (runtime/executor.py)
      |
      | 7. Crea el objeto `Lead` en la BD
      | 8. Crea el objeto `LeadState` inicial
      | 9. Devuelve el lead y su estado
      v
[Funnel Runtime Engine]
      |
      | 10. Crea el `LeadEvent` para auditoría
      | 11. Devuelve el lead_id a la vista
      v
[FunnelEventView]
      |
      | 12. Responde al cliente con un 202 ACCEPTED y el lead_id
      v
[Cliente/Usuario]
```

## 3. Documentación de la API de Runtime

Los siguientes endpoints han sido creados para interactuar con el motor de ejecución.

### Procesar un Evento

-   **Endpoint:** `POST /api/runtime/events/`
-   **Autenticación:** Ninguna (endpoint público).
-   **Descripción:** Punto de entrada principal para todos los eventos de ejecución de un embudo.
-   **Body (JSON):**
    ```json
    {
      "publication_slug": "el-slug-del-embudo-publicado",
      "event_type": "FORM_SUBMIT",
      "payload": {
        "page_id": "id-de-la-pagina-del-schema",
        "form_data": {
          "email": "cliente@example.com",
          "nombre": "Cliente Potencial"
        }
      }
    }
    ```
-   **Respuesta Exitosa (202 ACCEPTED):**
    ```json
    {
      "status": "Event processed successfully.",
      "lead_id": "un-uuid-para-el-lead-creado"
    }
    ```

### Consultar un Lead

-   **Endpoint:** `GET /api/runtime/leads/<uuid:lead_id>/`
-   **Autenticación:** Requerida (Token JWT).
-   **Descripción:** Permite a un usuario interno consultar el estado actual de un lead.
-   **Respuesta Exitosa (200 OK):**
    ```json
    {
      "id": "un-uuid-para-el-lead-creado",
      "funnel_id": 1,
      "form_data": { "email": "cliente@example.com", "nombre": "Cliente Potencial" },
      "created_at": "...",
      "state": {
        "current_page_id": "id-de-la-pagina-del-schema",
        "status": "active",
        "updated_at": "..."
      }
    }
    ```

## 4. Riesgos y Limitaciones Actuales (MVP)

-   **Manejo de Estado Limitado:** El motor actual solo maneja la creación de leads. No tiene lógica para reanudar un flujo o manejar leads existentes que interactúan de nuevo con el embudo.
-   **Falta de Lógica de Transición:** El motor no interpreta el `schema_json` para determinar cuál es la "siguiente página". Simplemente registra el estado en la página donde ocurrió el evento.
-   **Idempotencia no Implementada:** Enviar el mismo evento `FORM_SUBMIT` dos veces creará dos leads idénticos. El sistema no previene duplicados.
-   **Seguridad del Endpoint de Eventos:** Al ser un endpoint público, es vulnerable a envíos de spam. Se requerirán medidas como rate limiting o captchas en el futuro.
-   **Sin Acciones Post-Captura:** El motor crea el lead, pero no ejecuta ninguna acción subsecuente (ej. enviar un email de notificación, añadir a un CRM). Esto está planeado para la Fase 6 (Automatización).

## 5. Conclusión

La Fase 5 ha establecido con éxito la base del motor de ejecución. El sistema ahora puede cerrar el ciclo desde el diseño hasta la captura real de un lead. Las limitaciones actuales son inherentes al enfoque de MVP y proporcionan una hoja de ruta clara para las futuras fases de desarrollo, especialmente la de automatización.
