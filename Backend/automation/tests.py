from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from infrastructure.models import Tenant
from .models import Workflow, Node, Edge

User = get_user_model()

class AutomationAPITests(APITestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Automation Tenant")
        self.user = User.objects.create_user(email='auto_user@example.com', password='password', tenant=self.tenant)
        self.client.force_authenticate(user=self.user)
        self.url = reverse('workflow-list')

    def test_create_workflow_with_nodes_and_edges(self):
        self.assertEqual(Workflow.objects.count(), 0)

        workflow_data = {
            "name": "New Lead Workflow",
            "is_active": True,
            "nodes": [
                {"id": "temp-1", "node_type": "trigger", "config_json": {"type": "lead.created"}},
                {"id": "temp-2", "node_type": "action", "config_json": {"type": "send_email"}}
            ],
            # CORREGIDO: Enviar los IDs temporales en el formato correcto
            "edges": [
                {"source_node": "temp-1", "target_node": "temp-2"}
            ]
        }

        response = self.client.post(self.url, workflow_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workflow.objects.count(), 1)

        workflow = Workflow.objects.first()
        self.assertEqual(workflow.name, "New Lead Workflow")
        self.assertEqual(workflow.tenant, self.tenant)
        self.assertEqual(Node.objects.count(), 2)
        self.assertEqual(Edge.objects.count(), 1)

        trigger_node = Node.objects.get(node_type='trigger')
        action_node = Node.objects.get(node_type='action')
        edge = Edge.objects.first()

        self.assertEqual(edge.source_node, trigger_node)
        self.assertEqual(edge.target_node, action_node)
