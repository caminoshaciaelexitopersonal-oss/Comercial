# bff/views.py
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserRegistrationSerializer, CampaignSerializer, CustomerSerializer,
 
    FunnelSerializer, AssetSerializer, AIInteractionSerializer,
    GenerateTextSerializer
)
from domain.services import (
    auth_service, campaign_service, content_creation_service,
    customer_service, funnel_service, asset_service
)
 main
from infrastructure.models import (
    Campaign, Customer, Funnel, Asset, AIInteraction
)

class UserRegistrationView(APIView):
    """
    Vista del BFF para el registro de nuevos usuarios.
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
                # No devolvemos el objeto de usuario completo, solo un mensaje de éxito.
                return Response(
                    {"message": f"User '{user.username}' registered successfully."},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CampaignViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el CRUD de Campañas.
    """
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Asegura que los usuarios solo vean las campañas de su propio tenant.
        return Campaign.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        # Asigna automáticamente el tenant del usuario al crear una nueva campaña.
        campaign_service.create_campaign(
            tenant=self.request.user.tenant,
            name=serializer.validated_data['name'],
            goal=serializer.validated_data.get('goal', '')
        )


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el CRUD de Clientes.
    """
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
 
        customer_service.create_customer(
            tenant=self.request.user.tenant,
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', '')
        )
 


class FunnelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el CRUD de Funnels.
    """
    serializer_class = FunnelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Funnel.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
 
        funnel_service.create_funnel(
            tenant=self.request.user.tenant,
            campaign=serializer.validated_data['campaign'],
            name=serializer.validated_data['name']
        )
 


class AssetViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el CRUD de Assets.
    """
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Asset.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
 
        asset_service.create_asset(
            tenant=self.request.user.tenant,
            asset_type=serializer.validated_data['asset_type'],
            content=serializer.validated_data['content']
        )
 


class AIInteractionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar las interacciones de IA (solo lectura).
    """
    serializer_class = AIInteractionSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'head', 'options']  # Solo permitir lectura

    def get_queryset(self):
        return AIInteraction.objects.filter(tenant=self.request.user.tenant)
 


# --- Vistas para la Fase 3 ---

class GenerateTextView(APIView):
    """
    Vista del BFF para la generación de texto con memoria.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = GenerateTextSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                result = content_creation_service.generate_text_with_memory(
                    user=request.user,
                    provider_name=data['provider'],
                    prompt=data['prompt'],
                    model=data['model']
                )
                return Response({"result": result}, status=status.HTTP_200_OK)
            except (ValueError, RuntimeError) as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
