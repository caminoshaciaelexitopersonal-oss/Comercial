# bff/serializers.py
from rest_framework import serializers
from infrastructure.models import (
    User, Customer, Campaign, Funnel, FunnelPage, Asset, AIInteraction
)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tenant_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'tenant_name')

    def create(self, validated_data):
        # La lógica de creación real estará en el servicio de dominio,
        # este serializador es solo para la validación de datos.
        # No llamamos a User.objects.create_user() aquí directamente.
        return validated_data


# --- Serializers para la Fase 2 ---

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email', 'first_name', 'last_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'goal', 'created_at']
        read_only_fields = ['id', 'created_at']


class FunnelPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunnelPage
        fields = ['id', 'title', 'content_json', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']


class FunnelSerializer(serializers.ModelSerializer):
    pages = FunnelPageSerializer(many=True, read_only=True)

    class Meta:
        model = Funnel
        fields = ['id', 'name', 'campaign', 'pages', 'created_at']
        read_only_fields = ['id', 'created_at']


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'asset_type', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']


class AIInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIInteraction
        fields = ['id', 'user', 'provider', 'prompt', 'result', 'created_at']
        read_only_fields = ['id', 'created_at']
 


# --- Serializers para la Fase 3 ---

class GenerateTextSerializer(serializers.Serializer):
    """
    Serializador para validar los datos de entrada para la generación de texto.
    """
    provider = serializers.CharField(required=True)
    model = serializers.CharField(required=True)
    prompt = serializers.CharField(required=True)
 
