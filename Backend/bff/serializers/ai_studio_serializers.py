# bff/serializers/ai_studio_serializers.py
from rest_framework import serializers

class GenerateTextSerializer(serializers.Serializer):
    """
    Serializador para validar los datos de entrada para la generación de texto.
    """
    prompt = serializers.CharField(required=True)
    model = serializers.CharField(required=False) # El AIManager podría elegir
    # Otros parámetros como tono, formato, etc. se pueden añadir aquí.

class GenerateImageSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True)
    model = serializers.CharField(required=False)

class GenerateVideoSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True)
