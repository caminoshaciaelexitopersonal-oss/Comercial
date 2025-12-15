# bff/serializers.py
from rest_framework import serializers
from infrastructure.models import User

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
