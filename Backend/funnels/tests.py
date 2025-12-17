from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from infrastructure.models import Tenant
 
from .models import Funnel, FunnelVersion, FunnelPublication, FunnelPage
from shared.models import DomainEvent
 

User = get_user_model()

class FunnelsAPITests(APITestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Funnel Tenant")
        self.user = User.objects.create_user(email='funnel_user@example.com', password='password', tenant=self.tenant)
        self.client.force_authenticate(user=self.user)

    def test_create_funnel_creates_initial_version(self):
        url = reverse('funnel-list')
        data = {"name": "My First Funnel"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Funnel.objects.count(), 1)
        self.assertEqual(FunnelVersion.objects.count(), 1)

        funnel = Funnel.objects.first()
        version = FunnelVersion.objects.first()
        self.assertEqual(funnel.name, "My First Funnel")
        self.assertEqual(version.funnel, funnel)
        self.assertEqual(version.version_number, 1)

    def test_create_new_version(self):
        funnel = Funnel.objects.create(tenant=self.tenant, name="Version Test Funnel")
        FunnelVersion.objects.create(funnel=funnel, version_number=1)

        url = reverse('funnel-create-version', kwargs={'pk': funnel.pk})
        data = {"schema_json": {"pages": ["page1"]}}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(funnel.versions.count(), 2)
        self.assertEqual(funnel.versions.first().version_number, 2)

    def test_publish_version(self):
        funnel = Funnel.objects.create(tenant=self.tenant, name="Publish Test Funnel")
        version = FunnelVersion.objects.create(funnel=funnel, version_number=1)

        url = reverse('funnel-publish', kwargs={'pk': funnel.pk})
        data = {"version_id": version.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        funnel.refresh_from_db()
        self.assertEqual(funnel.status, 'published')
        self.assertEqual(FunnelPublication.objects.filter(funnel=funnel, is_active=True).count(), 1)
 

    def test_lead_capture_dispatches_event(self):
        funnel = Funnel.objects.create(tenant=self.tenant, name="Event Test Funnel")
        version = FunnelVersion.objects.create(funnel=funnel, version_number=1)
        publication = FunnelPublication.objects.create(funnel=funnel, version=version)
        page = FunnelPage.objects.create(funnel_version=version, order_index=0)

        url = reverse('lead-capture', kwargs={'slug': publication.public_url_slug})
        data = {"page_id": page.id, "form_data": {"email": "test@example.com"}}

        self.assertEqual(DomainEvent.objects.count(), 0)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DomainEvent.objects.count(), 1)

        event = DomainEvent.objects.first()
        self.assertEqual(event.event_type, 'lead.created')
        self.assertEqual(event.payload['form_data']['email'], 'test@example.com')
 
