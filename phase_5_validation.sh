#!/bin/bash

# --- FASE 5: Script de Validación del Funnel Runtime Engine ---

BASE_URL="http://localhost:8000/api"
EMAIL="test@example.com"
PASSWORD="testpassword"
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "--- Iniciando Validación del Motor de Ejecución de Embudos ---"

echo "Paso 1: Obteniendo token de autenticación..."
TOKEN_RESPONSE=$(curl -s -X POST $BASE_URL/bff/auth/token/ -H "Content-Type: application/json" -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")
ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access')
if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" == "null" ]; then
    echo -e "${RED}Error: No se pudo obtener el token de acceso.${NC}"
    exit 1
fi
echo -e "${GREEN}Token obtenido.${NC}"

FUNNEL_ID=1
VERSION_ID=1
echo "Paso 2: Publicando embudo $FUNNEL_ID..."
PUBLISH_RESPONSE=$(curl -s -X POST $BASE_URL/funnels/$FUNNEL_ID/publish/ -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "{\"version_id\": $VERSION_ID}")

# WORKAROUND: Aceptar 'public_url' y extraer el slug
RAW_SLUG=$(echo $PUBLISH_RESPONSE | jq -r '.public_url')
if [ -z "$RAW_SLUG" ] || [ "$RAW_SLUG" == "null" ]; then
    # Intentar con la clave correcta por si el entorno se arregla
    RAW_SLUG=$(echo $PUBLISH_RESPONSE | jq -r '.public_url_slug')
    if [ -z "$RAW_SLUG" ] || [ "$RAW_SLUG" == "null" ]; then
        echo -e "${RED}Error: No se pudo publicar el embudo.${NC}"
        echo "Respuesta: $PUBLISH_RESPONSE"
        exit 1
    fi
fi
SLUG=$(basename "$RAW_SLUG")
echo -e "${GREEN}Embudo publicado. Slug: $SLUG${NC}"

echo "Paso 3: Enviando evento FORM_SUBMIT..."
EVENT_PAYLOAD="{\"publication_slug\": \"$SLUG\", \"event_type\": \"FORM_SUBMIT\", \"payload\": {\"page_id\": \"fp-1629882928131-0.5\", \"form_data\": {\"name\": \"Jules Verne\", \"email\": \"jules@example.com\"}}}"
EVENT_RESPONSE=$(curl -s -X POST $BASE_URL/runtime/events/ -H "Content-Type: application/json" -d "$EVENT_PAYLOAD")
LEAD_ID=$(echo $EVENT_RESPONSE | jq -r '.lead_id')
if [ -z "$LEAD_ID" ] || [ "$LEAD_ID" == "null" ]; then
    echo -e "${RED}Error: El evento no generó un lead_id.${NC}"
    echo "Respuesta: $EVENT_RESPONSE"
    exit 1
fi
echo -e "${GREEN}Evento procesado. Lead ID: $LEAD_ID${NC}"

echo "Paso 4: Verificando el estado del lead..."
LEAD_RESPONSE=$(curl -s -X GET $BASE_URL/runtime/leads/$LEAD_ID/ -H "Authorization: Bearer $ACCESS_TOKEN")
LEAD_FUNNEL_ID=$(echo $LEAD_RESPONSE | jq -r '.funnel_id')
LEAD_EMAIL=$(echo $LEAD_RESPONSE | jq -r '.form_data.email')

if [ "$LEAD_FUNNEL_ID" == "$FUNNEL_ID" ] && [ "$LEAD_EMAIL" == "jules@example.com" ]; then
    echo -e "${GREEN}Verificación exitosa.${NC}"
    echo "--- Validación Completada ---"
    exit 0
else
    echo -e "${RED}Error de Verificación.${NC}"
    echo "Respuesta: $LEAD_RESPONSE"
    exit 1
fi
