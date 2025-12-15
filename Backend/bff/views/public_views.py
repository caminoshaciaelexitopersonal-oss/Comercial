# bff/views/public_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from domain.services import funnel_service
from bff.serializers.funnel_serializers import LandingPagePublicSerializer

class PublicFunnelView(APIView):
    """
    Vista pública para obtener la estructura completa de un embudo por su slug.
    No requiere autenticación.
    """
    def get(self, request, slug, *args, **kwargs):
        try:
            embudo = funnel_service.get_public_funnel_by_slug(slug)
            serializer = LandingPagePublicSerializer(embudo.landing_page)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
