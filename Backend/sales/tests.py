from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from infrastructure.models import Tenant
from .models import Opportunity, StageHistory

User = get_user_model()

class SalesAPITests(APITestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Sales Tenant")
        self.user = User.objects.create_user(username='sales_user', password='password', tenant=self.tenant)
        self.client.force_authenticate(user=self.user)

        self.opportunity = Opportunity.objects.create(tenant=self.tenant, name="Big Deal", stage="New")

    def test_move_opportunity(self):
        self.assertEqual(StageHistory.objects.count(), 0)
        url = reverse('opportunity-move-opportunity', kwargs={'pk': self.opportunity.pk})
        data = {"stage": "Proposal"}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.opportunity.refresh_from_db()
        self.assertEqual(self.opportunity.stage, "Proposal")

        self.assertEqual(StageHistory.objects.count(), 1)
        history_entry = StageHistory.objects.first()
        self.assertEqual(history_entry.from_stage, "New")
        self.assertEqual(history_entry.to_stage, "Proposal")
        self.assertEqual(history_entry.user, self.user)
