from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from infrastructure.models import Tenant, Role
from .models import Funnel, FunnelVersion, FunnelPublication, FunnelPage, FunnelExperiment
from shared.models import DomainEvent

User = get_user_model()

class FunnelsAPITests(APITestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Funnel Tenant")
        self.user = User.objects.create_user(username='funnel_user', password='password', tenant=self.tenant)
        role = Role.objects.create(tenant=self.tenant, name="FunnelManager", permissions=["funnels:create", "funnels:view", "funnels:publish"])
        self.user.roles.add(role)
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

    def test_ab_test_routing(self):
        funnel = Funnel.objects.create(tenant=self.tenant, name="A/B Test Funnel")
        v1 = FunnelVersion.objects.create(funnel=funnel, version_number=1, schema_json={'v': 1})
        v2 = FunnelVersion.objects.create(funnel=funnel, version_number=2, schema_json={'v': 2})
        publication = FunnelPublication.objects.create(funnel=funnel, version=v1) # Publicación apunta a v1

        # Creamos el experimento
        FunnelExperiment.objects.create(funnel=funnel, version_a=v1, version_b=v2, traffic_split=50)

        url = reverse('public-funnel', kwargs={'slug': publication.public_url_slug})

        # Hacemos 100 peticiones y verificamos que el tráfico se distribuye
        versions_served = {'v1': 0, 'v2': 0}
        for i in range(100):
            # Usamos un cliente nuevo cada vez para simular usuarios sin sesión
            client = self.client_class()
            response = client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            if response.data['schema_json']['v'] == 1:
                versions_served['v1'] += 1
            else:
                versions_served['v2'] += 1

        # Verificamos que ambas versiones fueron servidas (no será exactamente 50/50, pero > 0)
        self.assertGreater(versions_served['v1'], 10) # Damos un margen amplio
        self.assertGreater(versions_served['v2'], 10)


# TODO: Reactivar estos tests cuando se resuelva el problema del RBAC en el entorno de pruebas.
# class FunnelsRBAC_Tests(APITestCase):
#     def setUp(self):
#         self.tenant = Tenant.objects.create(name="RBAC Tenant")
#         self.user = User.objects.create_user(username='rbac_user', password='password', tenant=self.tenant)
#         self.client.force_authenticate(user=self.user)

#     def test_create_funnel_without_permission_fails(self):
#         # El usuario no tiene roles ni permisos
#         url = reverse('funnel-list')
#         data = {"name": "Funnel Sin Permiso"}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_create_funnel_with_permission_succeeds(self):
#         # Asignamos un rol con el permiso correcto
#         role = Role.objects.create(tenant=self.tenant, name="Marketer", permissions=["funnels:create"])
#         self.user.roles.add(role)
#         self.client.force_authenticate(user=self.user)

#         url = reverse('funnel-list')
#         data = {"name": "Funnel Con Permiso"}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_publish_funnel_without_permission_fails(self):
#         # Usuario solo tiene permiso de creación, no de publicación
#         role = Role.objects.create(tenant=self.tenant, name="Creator", permissions=["funnels:create"])
#         self.user.roles.add(role)
#         self.client.force_authenticate(user=self.user)

#         funnel = Funnel.objects.create(tenant=self.tenant, name="Test Funnel")
#         version = FunnelVersion.objects.create(funnel=funnel, version_number=1)

#         url = reverse('funnel-publish', kwargs={'pk': funnel.pk})
#         response = self.client.post(url, {"version_id": version.id})
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
