# bff/serializers/funnel_serializers.py
from rest_framework import serializers
from funnels.models import Funnel, FunnelVersion, FunnelPage
from infrastructure.models import Bloque, LandingPage, Pagina

class BloqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloque
        fields = ['id', 'tipo', 'orden', 'config_json']

class PaginaSerializer(serializers.ModelSerializer):
    bloques = BloqueSerializer(many=True, read_only=True)
    class Meta:
        model = Pagina
        fields = ['id', 'tipo', 'orden', 'bloques']

class FunnelPageSerializer(serializers.ModelSerializer):
    bloques = BloqueSerializer(many=True, read_only=True)
    class Meta:
        model = FunnelPage
        fields = ['id', 'page_type', 'order_index', 'bloques']

class FunnelVersionSerializer(serializers.ModelSerializer):
    pages = FunnelPageSerializer(many=True, read_only=True)
    class Meta:
        model = FunnelVersion
        fields = ['id', 'version_number', 'schema_json', 'created_at', 'is_active', 'pages']

class FunnelSerializer(serializers.ModelSerializer):
    versions = FunnelVersionSerializer(many=True, read_only=True)
    class Meta:
        model = Funnel
        fields = ['id', 'name', 'status', 'created_at', 'updated_at', 'versions']

class LandingPagePublicSerializer(serializers.ModelSerializer):
    funnel = FunnelSerializer(read_only=True)
    class Meta:
        model = LandingPage
        fields = ['slug', 'funnel']

class FunnelCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    landing_page_id = serializers.IntegerField()
