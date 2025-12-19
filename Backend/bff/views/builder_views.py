# bff/views/builder_views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from funnels.models import Funnel
from bff.serializers.funnel_serializers import FunnelSerializer
from domain.services import funnel_service
from infrastructure.models import Pagina, Bloque
from bff.serializers.funnel_serializers import PaginaSerializer, BloqueSerializer

class EmbudoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión de Embudos en el constructor.
    Requiere autenticación y opera solo sobre los datos del tenant del usuario.
    """
    serializer_class = FunnelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # La lógica de filtrado por tenant se hará en el servicio de dominio,
        # pero para las listas, podemos filtrar aquí directamente.
        # Asumiendo que Embudo tiene una FK a Tenant.
        # Filtra los embudos para que solo pertenezcan al tenant del usuario.
        user_tenant = self.request.user.tenant
        return Funnel.objects.filter(tenant=user_tenant)

    def retrieve(self, request, *args, **kwargs):
        tenant_id = request.user.tenant.id
        funnel_id = kwargs.get('pk')
        try:
            embudo = funnel_service.get_funnel_for_builder(tenant_id, funnel_id)
            serializer = self.get_serializer(embudo)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = FunnelCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            embudo = funnel_service.create_full_funnel(
                tenant=request.user.tenant,
                subcategoria_id=data['subcategoria_id'],
                nombre_embudo=data['nombre_embudo']
            )
            return Response(FunnelSerializer(embudo).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Acción para publicar una Landing Page asociada a un embudo.
        """
        try:
            funnel_service.publish_funnel(request.user.tenant, pk)
            return Response({"status": "published"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class PaginaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión de Páginas dentro de un Embudo.
    """
    serializer_class = PaginaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra las páginas para que solo pertenezcan a embudos del tenant del usuario.
        user_tenant = self.request.user.tenant
        return Pagina.objects.filter(embudo__landing_page__subcategoria__categoria__tenant=user_tenant)


class BloqueViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión de Bloques dentro de una Página.
    """
    serializer_class = BloqueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra los bloques para que solo pertenezcan a páginas de embudos del tenant del usuario.
        user_tenant = self.request.user.tenant
        return Bloque.objects.filter(pagina__embudo__landing_page__subcategoria__categoria__tenant=user_tenant)
