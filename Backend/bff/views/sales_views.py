# bff/views/sales_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from domain.services import sales_service
import logging

logger = logging.getLogger(__name__)

class OpportunityBFFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        opportunities = sales_service.get_all_opportunities(request.user)

        if not opportunities:
            logger.warning(f"No opportunities found for tenant {request.user.tenant.id}. Returning NO_DATA.")
            return Response({
                "data": [],
                "meta": {
                    "count": 0,
                    "tenant_id": request.user.tenant.id,
                    "reason": "NO_DATA"
                }
            })

        return Response({
            "data": opportunities,
            "meta": {
                "count": len(opportunities),
                "tenant_id": request.user.tenant.id
            }
        })
