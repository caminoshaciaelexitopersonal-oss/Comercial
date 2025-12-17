from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from infrastructure.models import Tenant
from .models import Opportunity, StageHistory
 
from predictions.models import LeadClosenessPrediction
from shared.subscribers import EVENT_SUBSCRIBERS
from .subscribers import handle_lead_created_event
 

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
 


class LeadScoringTests(APITestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Scoring Tenant")

    def tearDown(self):
        EVENT_SUBSCRIBERS.clear()

    def test_lead_created_event_creates_opportunity_with_score(self):
        # Registramos el suscriptor manualmente para el test
        EVENT_SUBSCRIBERS['lead.created'] = [handle_lead_created_event]

        self.assertEqual(Opportunity.objects.count(), 0)

        # Simulamos el payload del evento
        event_payload = {
            'tenant_id': self.tenant.id,
            'funnel_id': 1,
            'form_data': {'estimated_value': 15000}
        }

        # Llamamos al handler directamente
        handle_lead_created_event(event_payload)

        self.assertEqual(Opportunity.objects.count(), 1)
        opportunity = Opportunity.objects.first()
        self.assertEqual(opportunity.lead_score, 50) # Basado en la regla de > 10000
        self.assertEqual(opportunity.priority, 'Medium')

        # Verificar que también se creó la predicción
        self.assertEqual(LeadClosenessPrediction.objects.count(), 1)
        prediction = LeadClosenessPrediction.objects.first()
        self.assertEqual(prediction.opportunity, opportunity)
        self.assertAlmostEqual(prediction.confidence, 0.5) # 50 / 100.0
 
