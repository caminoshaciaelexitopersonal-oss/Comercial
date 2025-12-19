from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.template import Template, Context
from rest_framework.views import APIView
from rest_framework.decorators import action
from ai.services.ai_manager.ai_manager import ai_manager
from ai.services.sanitizers import sanitize_plain_text
from .models import Campaign
from .serializers import CampaignSerializer
from .services import validate_social_post

class CampaignViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Campañas de Marketing.
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campaign.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

    @action(detail=True, methods=['post'], url_path='send')
    def send_campaign(self, request, pk=None):
        campaign = self.get_object()
        active_channels = campaign.channels.filter(is_active=True).count()
        if active_channels == 0:
            return Response(
                {"error": "La campaña no tiene canales activos o conectados."},
                status=status.HTTP_400_BAD_REQUEST
            )
        campaign.status = 'scheduled'
        campaign.save()
        return Response(
            {"status": f"Campaña '{campaign.name}' programada para envío."},
            status=status.HTTP_200_OK
        )

class EmailRenderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        template_content = request.data.get('template')
        context_data = request.data.get('context', {})
        if not template_content:
            return Response({"error": "El campo 'template' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            template = Template(template_content)
            context = Context(context_data)
            rendered_html = template.render(context)
            return Response({"rendered_html": rendered_html}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al renderizar la plantilla: {e}"}, status=status.HTTP_400_BAD_REQUEST)

class AIRewriteEmailView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        base_text = request.data.get('text')
        if not base_text:
            return Response({"error": "El campo 'text' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        prompt = f"Reescribe el siguiente texto para un email de marketing, optimizando su claridad y poder de conversión:\n\n{base_text}"
        try:
            raw_text, provider_name = ai_manager.execute_text_generation(prompt=prompt, model='default-text-model')
            sanitized_text = sanitize_plain_text(raw_text)
            return Response({"rewritten_text": sanitized_text}, status=status.HTTP_200_OK)
        except RuntimeError as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": f"Ocurrió un error inesperado durante la reescritura con IA: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SocialPostPreviewView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        platform = request.data.get('platform')
        content = request.data.get('content', '')
        if not platform:
            return Response({"error": "El campo 'platform' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        result = validate_social_post(platform, content)
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)
