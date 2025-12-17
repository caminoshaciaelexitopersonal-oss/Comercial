import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from funnels.models import Funnel, FunnelEvent
from ..models import Insight
from ai.services.ai_manager.ai_manager import ai_manager

class FunnelAnomalyDetector:
    @classmethod
    def analyze_conversion_rates(cls, days_historical=30, days_current=7, drop_threshold=20.0):
        """
        Analiza las tasas de conversión de los funnels y detecta caídas significativas.
        """
        now = timezone.now()
        historical_start = now - datetime.timedelta(days=days_historical)
        current_start = now - datetime.timedelta(days=days_current)
        historical_end = current_start

        for funnel in Funnel.objects.filter(status='published'):
            # Calcular tasa de conversión histórica (periodo anterior al reciente)
            historical_views = FunnelEvent.objects.filter(funnel=funnel, event_type='page_view', created_at__gte=historical_start, created_at__lt=historical_end).count()
            historical_conversions = FunnelEvent.objects.filter(funnel=funnel, event_type='conversion', created_at__gte=historical_start, created_at__lt=historical_end).count()
            historical_rate = (historical_conversions / historical_views) * 100 if historical_views > 0 else 0

            # Calcular tasa de conversión reciente
            current_views = FunnelEvent.objects.filter(funnel=funnel, event_type='page_view', created_at__gte=current_start).count()
            current_conversions = FunnelEvent.objects.filter(funnel=funnel, event_type='conversion', created_at__gte=current_start).count()
            current_rate = (current_conversions / current_views) * 100 if current_views > 0 else 0

            print(f"DEBUG: Funnel {funnel.name}")
            print(f"DEBUG: Hist. Views: {historical_views}, Hist. Conv: {historical_conversions}, Hist. Rate: {historical_rate}")
            print(f"DEBUG: Curr. Views: {current_views}, Curr. Conv: {current_conversions}, Curr. Rate: {current_rate}")

            if historical_rate > 0 and current_rate < historical_rate:
                percentage_drop = ((historical_rate - current_rate) / historical_rate) * 100
                print(f"DEBUG: Drop detected: {percentage_drop}%")
                if percentage_drop >= drop_threshold:
                    print("DEBUG: Threshold exceeded, creating insight.")
                    cls.create_insight_for_drop(funnel, historical_rate, current_rate, percentage_drop)

    @classmethod
    def create_insight_for_drop(cls, funnel, old_rate, new_rate, drop):
        title = f"Caída de conversión del {drop:.1f}% en el embudo '{funnel.name}'"

        # Generar recomendación con IA
        prompt = f"La tasa de conversión del embudo '{funnel.name}' ha caído un {drop:.1f}%, pasando de {old_rate:.1f}% a {new_rate:.1f}%. Genera una recomendación concisa para un equipo de marketing."
        recommendation, _ = ai_manager.execute_text_generation(prompt=prompt, model='default-text-model')

        Insight.objects.create(
            tenant=funnel.tenant,
            title=title,
            severity='medium',
            recommendation_text=recommendation,
            related_object=funnel
        )
