# bff/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from domain.services.auth_service import register_user

class UserRegistrationView(APIView):
    """
    Vista del BFF para el registro de nuevos usuarios.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            try:
                user = register_user(
                    username=validated_data['username'],
                    password=validated_data['password'],
                    email=validated_data.get('email', ''),
                    tenant_name=validated_data.get('tenant_name')
                )
                # No devolvemos el objeto de usuario completo, solo un mensaje de éxito.
                return Response(
                    {"message": f"User '{user.username}' registered successfully."},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
