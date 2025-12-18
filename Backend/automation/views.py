from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Workflow, AgentPersona
from .serializers import WorkflowDetailSerializer, WorkflowCreateSerializer, AgentPersonaSerializer

class AgentPersonaViewSet(viewsets.ModelViewSet):
    queryset = AgentPersona.objects.all()
    serializer_class = AgentPersonaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return WorkflowCreateSerializer
        return WorkflowDetailSerializer

    def get_queryset(self):
        return Workflow.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)
