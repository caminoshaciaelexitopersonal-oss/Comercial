 # INFORME DE AUDITORÍA TÉCNICA - MÓDULO AI

**Destinatario:** Liderazgo Técnico
**Auditor:** Jules (Backend Engineer)
**Fecha:** 2024-07-29

## 1. Objetivo y Alcance

Este informe detalla los resultados de una auditoría técnica exhaustiva del módulo `Backend/ai/`, según la Directriz de Auditoría Técnica Total. El objetivo fue verificar, validar y documentar el estado real del código para evaluar su coherencia, diseño, escalabilidad y deuda técnica.

## 2. Resumen Ejecutivo (TL;DR)

El módulo de IA se encuentra en un estado **esquelético y no funcional**.

Existe una **base de diseño sólida y prometedora** en el núcleo de la lógica de negocio (el `AIManager` y la abstracción de proveedores), que demuestra una comprensión clara de la arquitectura deseada (proveedor-agnóstico, basado en capacidades).

Sin embargo, **faltan componentes críticos indispensables** para que el módulo funcione. No hay API (`views.py`), ni modelos de base de datos (`models.py`), y las implementaciones existentes son placeholders (tareas asíncronas) o inseguras (proveedor de IA sin sanitización de salida).

**El módulo, en su estado actual, no puede ser integrado con el frontend. Requiere un desarrollo significativo para ser funcional.**

---

## 3. Mapa Real del Módulo

A continuación se detalla el estado real de cada componente clave, comparando lo esperado (según especificación) con lo encontrado.

| Componente | Estado Esperado (Resumen) | Estado Real | Conclusión |
| --- | --- | --- | --- |
| **Modelos de Datos (`models.py`)** | `AIInteraction` y `ContentAsset` para persistencia. | **Inexistente.** Archivo vacío. | **CRÍTICO** |
| **API Endpoints (`views.py`)** | Endpoints para texto, imagen, video, campañas. | **Inexistente.** Archivo vacío. | **CRÍTICO** |
| **Orquestador (`AIManager`)** | Orquestador por capacidades, proveedor-agnóstico. | **Existe y está bien diseñado.** | **FUNCIONAL (Aislado)** |
| **Abstracción (`AIBaseProvider`)** | Contrato común para todos los proveedores. | **Existe y está excelentemente diseñado.** | **FUNCIONAL** |
| **Proveedores (`GeminiProvider`)** | Implementación funcional y segura. | **Incompleto e Inseguro.** Lógica de imagen es placeholder. **No sanitiza la salida de la IA.** | **ALTO RIESGO** |
| **Tareas Asíncronas (`tasks.py`)** | Lógica funcional para generación de video. | **Placeholder.** Es una simulación con `time.sleep()`. | **NO FUNCIONAL** |
| **Seguridad (Secretos)** | Manejo seguro de claves API. | **Correcto.** Usa variables de entorno. | **OK** |

---

## 4. Lista Priorizada de Problemas

### Nivel CRÍTICO (Bloquean cualquier funcionalidad)

1.  **C-01: Ausencia de Modelos de Datos (`models.py`)**
    *   **Descripción:** No existen los modelos `AIInteraction` ni `ContentAsset`. Esto impide cualquier tipo de persistencia, historial o trazabilidad de las operaciones de IA.
    *   **Impacto:** El requisito fundamental de "Memoria del Sistema" es incumplido.

2.  **C-02: Ausencia de API Endpoints (`views.py`)**
    *   **Descripción:** El archivo de vistas está vacío. No hay ninguna ruta o endpoint expuesto por el módulo.
    *   **Impacto:** El módulo de IA es inalcanzable. No hay forma de que el frontend (o cualquier otro servicio) pueda interactuar con él.

### Nivel ALTO (Riesgo grave de seguridad o inestabilidad)

1.  **H-01: Falta de Sanitización de Salida de la IA (`gemini_provider.py`)**
    *   **Descripción:** El proveedor de Gemini devuelve el texto (`response.text`) directamente de la API sin ninguna limpieza, validación o transformación.
    *   **Impacto:** Una respuesta de IA con Markdown, JSON malformado, o cualquier formato inesperado **romperá el frontend**. Es un riesgo de seguridad y estabilidad inaceptable. **Viola la directriz "La IA nunca se asume correcta por defecto".**

### Nivel MEDIO (Funcionalidad incompleta o mal diseñada)

1.  **M-01: Lógica de Tareas Asíncronas es un Placeholder (`tasks.py`)**
    *   **Descripción:** La tarea `generate_video_task` no contiene lógica real de generación de video; es una simulación.
    *   **Impacto:** La funcionalidad de video es inexistente en la práctica.

2.  **M-02: Generación de Imágenes es un Placeholder (`gemini_provider.py`)**
    *   **Descripción:** El método `generate_image` es una implementación conceptual no funcional.
    *   **Impacto:** La funcionalidad de imagen es inexistente en la práctica.

3.  **M-03: Acoplamiento Arquitectónico en Tareas (`tasks.py`)**
    *   **Descripción:** La tarea asíncrona depende directamente de un modelo de la capa `infrastructure` en lugar de un modelo de dominio propio del módulo `ai`.
    *   **Impacto:** Rompe la separación de capas ideal y crea una dependencia frágil.

### Nivel BAJO (Malas prácticas o mejoras de diseño)

1.  **L-01: Uso de `print()` en lugar de Logging Formal**
    *   **Descripción:** Todo el módulo utiliza `print()` para la salida de información y errores.
    *   **Impacto:** Dificulta el debug en entornos de producción y puede exponer información sensible en logs si no se gestiona correctamente.

2.  **L-02: Hardcode de Proveedores en `AIManager`**
    *   **Descripción:** Para añadir un nuevo proveedor, es necesario modificar el código del `AIManager`.
    *   **Impacto:** Reduce la extensibilidad "plug-and-play" del sistema. Aceptable por ahora, pero a mejorar a futuro.

---

## 5. Recomendaciones Técnicas

El módulo requiere **desarrollo fundamental**, no refactorización. Las acciones deben seguir este orden:

1.  **Construir la Base (Críticos):**
    *   **Acción Inmediata 1:** Implementar los modelos `AIInteraction` y `ContentAsset` en `ai/models.py`, incluyendo la relación con el `Tenant` y las migraciones de base de datos correspondientes.
    *   **Acción Inmediata 2:** Crear los endpoints de la API en `ai/views.py`. Inicialmente, pueden devolver datos mockeados, pero deben existir para establecer el contrato con el frontend.

2.  **Asegurar la Implementación (Alto):**
    *   **Acción Crítica de Seguridad:** Implementar un **servicio de sanitización** robusto. **Ninguna** respuesta de un proveedor de IA debe salir del módulo `ai` sin pasar por este servicio. Debe limpiar Markdown, validar JSON (cuando aplique) y manejar respuestas malformadas.
    *   Integrar la llamada al servicio de sanitización en el `AIManager` antes de devolver cualquier dato.

3.  **Completar la Funcionalidad (Medio):**
    *   Reemplazar la lógica de placeholder en `generate_video_task` y `generate_image` con llamadas reales a las APIs correspondientes.
    *   Integrar la lógica de persistencia: cada vez que el `AIManager` ejecute una tarea, debe crear un registro `AIInteraction` y, si aplica, un `ContentAsset`.

4.  **Mejorar la Calidad (Bajo):**
    *   Reemplazar todos los `print()` con un sistema de logging estructurado.
    *   Planificar a futuro un sistema de registro de proveedores más dinámico para el `AIManager`.

## 6. Conclusión Final

El módulo `ai` es actualmente una **arquitectura conceptual bien definida pero vacía de implementación real**. El trabajo realizado en la capa de servicio (`AIManager`, `AIBaseProvider`) es de buena calidad y debe ser conservado. Sin embargo, se requiere un esfuerzo de desarrollo significativo para construir los cimientos (modelos, vistas) y asegurar la implementación (sanitización, persistencia) antes de que este módulo pueda ser considerado funcional o integrable.
