# domain/services/funnel_service.py
from infrastructure.models import Funnel, Tenant, Campaign

def create_funnel(tenant: Tenant, campaign: Campaign, name: str) -> Funnel:
    """
    Crea un nuevo funnel para un tenant y una campaña específicos.
    """
    funnel = Funnel.objects.create(
        tenant=tenant,
        campaign=campaign,
        name=name
    )
    return funnel
