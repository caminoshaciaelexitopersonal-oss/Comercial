
# bff/serializers/auth_serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from infrastructure.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims here if needed
        token['email'] = user.email
        return token

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tenant_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'tenant_name')
        extra_kwargs = {
            'email': {'required': True}
        }
