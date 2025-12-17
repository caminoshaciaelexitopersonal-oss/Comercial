from django.test import TestCase
from django.utils import timezone
import datetime
from infrastructure.models import Tenant
from funnels.models import Funnel, FunnelVersion, FunnelEvent
from .models import Insight
from .services.anomaly_detector import FunnelAnomalyDetector
from unittest.mock import patch

class AnomalyDetectorTests(TestCase):
    @patch('business_intelligence.services.anomaly_detector.ai_manager.execute_text_generation')
    def test_detects_conversion_drop(self, mock_ai_manager):
        mock_ai_manager.return_value = ("Recomendación de prueba", "MockProvider")

        tenant = Tenant.objects.create(name="BI Tenant")
        funnel = Funnel.objects.create(tenant=tenant, name="Test Funnel", status='published')
        version = FunnelVersion.objects.create(funnel=funnel, version_number=1)

        # Simular datos históricos (tasa del 50%)
        for _ in range(10): FunnelEvent.objects.create(funnel=funnel, version=version, event_type='page_view', created_at=timezone.now() - datetime.timedelta(days=15))
        for _ in range(5): FunnelEvent.objects.create(funnel=funnel, version=version, event_type='conversion', created_at=timezone.now() - datetime.timedelta(days=15))

        # Simular datos recientes (tasa del 10%)
        for _ in range(10): FunnelEvent.objects.create(funnel=funnel, version=version, event_type='page_view', created_at=timezone.now() - datetime.timedelta(days=3))
        for _ in range(1): FunnelEvent.objects.create(funnel=funnel, version=version, event_type='conversion', created_at=timezone.now() - datetime.timedelta(days=3))

        self.assertEqual(Insight.objects.count(), 0)
        FunnelAnomalyDetector.analyze_conversion_rates(drop_threshold=50.0)

        self.assertEqual(Insight.objects.count(), 1)
        insight = Insight.objects.first()
        self.assertIn("Caída de conversión", insight.title)
        self.assertEqual(insight.related_object, funnel)
