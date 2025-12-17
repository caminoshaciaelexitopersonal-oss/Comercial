from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from infrastructure.models import Tenant
from .models import Campaign, CampaignChannel

User = get_user_model()

class MarketingAPITests(APITestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(name="Marketing Tenant")
        self.user = User.objects.create_user(email='mkt_user@example.com', password='password', tenant=self.tenant)
        self.client.force_authenticate(user=self.user)

        self.campaign = Campaign.objects.create(tenant=self.tenant, name="Test Campaign")

    def test_send_campaign_with_no_active_channels(self):
        url = reverse('campaign-send-campaign', kwargs={'pk': self.campaign.pk})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_campaign_with_active_channel(self):
        CampaignChannel.objects.create(campaign=self.campaign, channel_type='email', is_active=True)
        url = reverse('campaign-send-campaign', kwargs={'pk': self.campaign.pk})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.status, 'scheduled')

    def test_render_email_template(self):
        url = reverse('email_render')
        data = {
            "template": "<h1>Hello, {{ name }}!</h1>",
            "context": {"name": "Jules"}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rendered_html'], "<h1>Hello, Jules!</h1>")
