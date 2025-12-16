from django.test import TestCase
from unittest.mock import MagicMock
from .models import DomainEvent
from .subscribers import subscribe, EVENT_SUBSCRIBERS
from .tasks import process_pending_events

class EventProcessorTests(TestCase):
    def tearDown(self):
        # Limpiar suscriptores después de cada test
        EVENT_SUBSCRIBERS.clear()

    def test_event_processor_calls_subscriber(self):
        # Creamos un mock del handler
        mock_handler = MagicMock()
        mock_handler.__name__ = 'mock_handler' # Simular el atributo __name__ para el logging

        # Nos suscribimos al evento
        subscribe('test.event', mock_handler)

        # Creamos un evento pendiente en la BD
        DomainEvent.objects.create(event_type='test.event', payload={'data': 'test'})

        # Ejecutamos la tarea de procesamiento
        process_pending_events()

        # Verificamos que el handler fue llamado con el payload correcto
        mock_handler.assert_called_once_with({'data': 'test'})

        # Verificamos que el evento fue marcado como procesado
        event = DomainEvent.objects.first()
        self.assertEqual(event.status, 'processed')
