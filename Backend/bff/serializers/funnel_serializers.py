# bff/serializers/funnel_serializers.py
from rest_framework import serializers
from infrastructure.models import Categoria, Subcategoria, LandingPage, Embudo, Pagina, Bloque

class BloqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloque
        fields = ['id', 'tipo', 'orden', 'config_json']

class PaginaSerializer(serializers.ModelSerializer):
    bloques = BloqueSerializer(many=True, read_only=True)
    class Meta:
        model = Pagina
        fields = ['id', 'tipo', 'orden', 'bloques']

class EmbudoSerializer(serializers.ModelSerializer):
    paginas = PaginaSerializer(many=True, read_only=True)
    class Meta:
        model = Embudo
        fields = ['id', 'nombre', 'orden', 'activo', 'paginas']

class LandingPagePublicSerializer(serializers.ModelSerializer):
    embudo = EmbudoSerializer(read_only=True)
    class Meta:
        model = LandingPage
        fields = ['slug', 'embudo']


class EmbudoCreateSerializer(serializers.Serializer):
    nombre_embudo = serializers.CharField(max_length=255)
    subcategoria_id = serializers.IntegerField()
