# api/serializers.py
from rest_framework import serializers

class GenerateTextSerializer(serializers.Serializer):
    """
    Serializador para validar los datos de entrada para la generación de texto.
    """
    provider = serializers.CharField(required=True)
    model = serializers.CharField(required=True)
    prompt = serializers.CharField(required=True)

class GenerateImageSerializer(serializers.Serializer):
    """
    Serializador para validar los datos de entrada para la generación de imágenes.
    """
    provider = serializers.CharField(required=True)
    model = serializers.CharField(required=True)
    prompt = serializers.CharField(required=True)

class OllamaPullSerializer(serializers.Serializer):
    """
    Serializador para validar la petición de descarga de un modelo de Ollama.
    """
    model_name = serializers.CharField(required=True)
