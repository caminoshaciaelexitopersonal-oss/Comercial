from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from infrastructure.models import Tenant, AIInteraction

User = get_user_model()

class AITextGenerationTests(APITestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test Tenant")
        # Creamos un segundo tenant para asegurar que no hay ambigüedad
        self.other_tenant = Tenant.objects.create(name="Other Tenant")

        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            tenant=self.tenant
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('ai_text_generation')

    def test_text_generation_success(self):
        """
        Verifica que el endpoint de generación de texto funciona correctamente
        con una solicitud válida.
        """
        data = {'prompt': 'Hola mundo'}

        # Mockeamos el AIManager para no hacer una llamada real a la IA
        from .services.ai_manager.ai_manager import ai_manager
        import unittest.mock as mock

        mock_return_value = ("  Respuesta de prueba.  ", "MockedProvider")
        with mock.patch.object(ai_manager, 'execute_text_generation', return_value=mock_return_value) as mock_execute:
            response = self.client.post(self.url, data, format='json')

            # 1. Verificar que la respuesta de la API es correcta
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('generated_text', response.data)
            self.assertEqual(response.data['generated_text'], "Respuesta de prueba.") # Verifica la sanitización

            # 2. Verificar que se llamó al AIManager
            mock_execute.assert_called_once_with(prompt='Hola mundo', model='default-text-model')

            # 3. Verificar que la interacción se guardó en la BD
            self.assertEqual(AIInteraction.objects.count(), 1)
            interaction = AIInteraction.objects.first()
            self.assertEqual(interaction.user, self.user)
            self.assertEqual(interaction.tenant, self.tenant) # Esta aserción es clave
            self.assertNotEqual(interaction.tenant, self.other_tenant) # Aserción adicional
            self.assertEqual(interaction.prompt_original, 'Hola mundo')
            self.assertEqual(interaction.resultado, "Respuesta de prueba.")
            self.assertEqual(interaction.proveedor_usado, "MockedProvider")

    def test_text_generation_no_prompt(self):
        """
        Verifica que el endpoint devuelve un error 400 si no se proporciona un prompt.
        """
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(AIInteraction.objects.count(), 0)

    def test_text_generation_no_provider(self):
        """
        Verifica que el endpoint devuelve un error 503 si el AIManager no encuentra un proveedor.
        """
        data = {'prompt': 'Prueba sin proveedor'}

        from .services.ai_manager.ai_manager import ai_manager
        import unittest.mock as mock

        with mock.patch.object(ai_manager, 'execute_text_generation', side_effect=RuntimeError("No provider available")):
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
            self.assertEqual(AIInteraction.objects.count(), 0)
