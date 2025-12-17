from celery import shared_task
import logging

logger = logging.getLogger(__name__)

from .services.anomaly_detector import FunnelAnomalyDetector

@shared_task
def generate_business_insights():
    logger.info("Starting daily business intelligence analysis...")

    # Ejecutar análisis de funnels
    try:
        FunnelAnomalyDetector.analyze_conversion_rates()
        logger.info("Funnel anomaly detection completed successfully.")
    except Exception as e:
        logger.error(f"Error during funnel anomaly detection: {e}", exc_info=True)

    # Aquí se podrían añadir llamadas a otros analizadores

    logger.info("Business intelligence analysis finished.")
