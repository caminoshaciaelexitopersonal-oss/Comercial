from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Workflow
from .serializers import WorkflowDetailSerializer, WorkflowCreateSerializer

class WorkflowViewSet(viewsets.ModelViewSet):
    """
    API para gestionar Workflows de Automatización.
    """
    queryset = Workflow.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return WorkflowCreateSerializer
        return WorkflowDetailSerializer

    def get_queryset(self):
        # Filtrar por tenant del usuario autenticado
        return Workflow.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        # Asignar el tenant al crear
        serializer.save(tenant=self.request.user.tenant)
