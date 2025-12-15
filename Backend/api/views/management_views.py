# api/views/management_views.py
import requests
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import OllamaPullSerializer
from ..services.ai_manager.ai_manager import ai_manager

class AIProvidersView(APIView):
    """
    Vista para obtener la lista de proveedores de IA disponibles.
    """
    def get(self, request, *args, **kwargs):
        providers = ai_manager.get_available_providers()
        return Response(providers, status=status.HTTP_200_OK)

class OllamaModelsView(APIView):
    """
    Vista para listar los modelos de Ollama locales.
    """
    def get(self, request, *args, **kwargs):
        ollama_endpoint = os.getenv("OLLAMA_ENDPOINT")
        if not ollama_endpoint:
            return Response({"error": "Ollama endpoint is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            response = requests.get(f"{ollama_endpoint}/api/tags")
            response.raise_for_status()
            return Response(response.json().get("models", []), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Could not fetch models from Ollama: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OllamaPullView(APIView):
    """
    Vista para iniciar la descarga de un modelo de Ollama.
    """
    def post(self, request, *args, **kwargs):
        serializer = OllamaPullSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        model_name = serializer.validated_data['model_name']
        ollama_endpoint = os.getenv("OLLAMA_ENDPOINT")
        if not ollama_endpoint:
            return Response({"error": "Ollama endpoint is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            # La petición de pull puede tardar, pero la API de Ollama responde con un stream.
            # Aquí, no manejamos el stream para no bloquear la petición.
            # Devolvemos una respuesta inmediata.
            requests.post(f"{ollama_endpoint}/api/pull", json={"name": model_name, "stream": False}, timeout=1)
        except requests.exceptions.ReadTimeout:
            # Ignoramos el timeout ya que la descarga continúa en segundo plano en Ollama.
            pass
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to initiate pull for model '{model_name}': {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": f"Model pull for '{model_name}' initiated."}, status=status.HTTP_202_ACCEPTED)
