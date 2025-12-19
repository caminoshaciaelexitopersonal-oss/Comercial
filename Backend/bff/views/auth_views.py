
# bff/views/auth_views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from bff.serializers.auth_serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from domain.services import auth_service

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view to handle user login using the custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer

class UserRegistrationView(APIView):
    """
    Vista del BFF para el registro de nuevos usuarios y su Tenant/Cadena.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            try:
                user = auth_service.register_user(
                    username=validated_data['username'],
                    password=validated_data['password'],
                    email=validated_data.get('email', ''),
                    tenant_name=validated_data.get('tenant_name')
                )
                return Response(
                    {"message": f"User '{user.username}' registered successfully in tenant '{user.tenant.name}'."},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
