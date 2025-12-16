# bff/serializers/auth_serializers.py
from rest_framework import serializers
from infrastructure.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tenant_name = serializers.CharField(required=False, allow_blank=True, help_text="Nombre para el nuevo Tenant/Cadena")

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'tenant_name')
