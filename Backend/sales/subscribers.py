import logging
from shared.subscribers import subscribe
from .models import Opportunity
from .services import LeadScoringService

logger = logging.getLogger(__name__)

def handle_lead_created_event(payload: dict):
    logger.info(f"Sales module received lead.created event: {payload}")

    # Crear una nueva Oportunidad a partir del Lead capturado
    try:
        opportunity = Opportunity.objects.create(
            tenant_id=payload['tenant_id'],
            name=f"New Lead from Funnel #{payload['funnel_id']}",
            # Podríamos extraer un valor del form_data si existiera
            value=payload.get('form_data', {}).get('estimated_value', 0)
        )

        # Calcular el score inicial
        LeadScoringService.update_opportunity_score(opportunity)
        logger.info(f"Created Opportunity {opportunity.id} with score {opportunity.lead_score}")

    except Exception as e:
        logger.error(f"Failed to create opportunity from lead.created event: {e}", exc_info=True)


def register_subscribers():
    subscribe('lead.created', handle_lead_created_event)
