# Data Contracts

This document defines the JSON data contracts between the frontend and the BFF (Backend For Frontend).

## 1. CRM / Opportunities

### 1.1. List Opportunities

*   **Endpoint:** `GET /api/bff/sales/opportunities/`
*   **Description:** Retrieves the list of all opportunities.
*   **Backend JSON Response:**

```json
[
  {
    "id": 1,
    "name": "Initial CRM Implementation",
    "stage": "proposal",
    "value": "15000.00",
    "last_updated": "2024-01-01T12:00:00Z",
    "company_name": "Example Corp"
  }
]
```

### 1.2. Move Opportunity

*   **Endpoint:** `PUT /api/bff/sales/opportunities/{id}/move/`
*   **Description:** Moves an opportunity to a new stage in the pipeline.
*   **Frontend JSON Request:**

```json
{
  "stage": "negotiation"
}
```

*   **Backend JSON Response:** The full opportunity object, same as the `List Opportunities` response.

---

## 2. Funnel Builder

### 2.1. Create Funnel Version

*   **Endpoint:** `POST /api/bff/funnels/{id}/versions/`
*   **Description:** Creates a new version of a funnel with a new schema.
*   **Frontend JSON Request:**

```json
{
  "schema_json": {
    "pages": [
      {
        "id": "page1",
        "type": "landing",
        "blocks": []
      }
    ]
  },
  "pages": [
    {
      "page_type": "landing",
      "page_schema_json": {}
    }
  ]
}
```

*   **Backend JSON Response:**

```json
{
  "id": 1,
  "version_number": 2,
  "schema_json": {
    "pages": [
      {
        "id": "page1",
        "type": "landing",
        "blocks": []
      }
    ]
  },
  "created_at": "2024-01-01T12:00:00Z",
  "is_active": true
}
```

### 2.2. Publish Funnel

*   **Endpoint:** `POST /api/bff/funnels/{id}/publish/`
*   **Description:** Publishes a specific version of a funnel.
*   **Frontend JSON Request:**

```json
{
  "version_id": 1
}
```

*   **Backend JSON Response:**

```json
{
  "status": "Funnel publicado exitosamente.",
  "public_url": "/f/some-uuid-slug"
}
```

---

## 3. Automation

### 3.1. List Workflows

*   **Endpoint:** `GET /api/bff/automation/workflows/`
*   **Description:** Retrieves the list of all workflows.
*   **Backend JSON Response:**

```json
[
  {
    "id": 1,
    "name": "New Lead Follow-up",
    "trigger_model": "lead",
    "trigger_event": "created",
    "is_active": true,
    "created_at": "2024-01-01T12:00:00Z"
  }
]
```

### 3.2. Create Workflow

*   **Endpoint:** `POST /api/bff/automation/workflows/`
*   **Description:** Creates a new workflow.
*   **Frontend JSON Request:**

```json
{
  "name": "New Lead Follow-up",
  "trigger_model": "lead",
  "trigger_event": "created",
  "is_active": true,
  "actions": [
    {
      "action_type": "send_email",
      "config_json": {
        "template_id": "some-template-id",
        "delay_minutes": 5
      },
      "order": 1
    }
  ]
}
```

*   **Backend JSON Response:** The full workflow object, similar to the `List Workflows` response, but with the `actions` included.
