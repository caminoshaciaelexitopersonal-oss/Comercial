from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.template import Template, Context
from rest_framework.views import APIView
from rest_framework.decorators import action
from ai.services.ai_manager.ai_manager import ai_manager
from ai.services.sanitizers import sanitize_plain_text
from .models import Campaign, SendLog
from .serializers import CampaignSerializer
from .services import validate_social_post
from django.db.models import Count, Q

class CampaignViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Campañas de Marketing.
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Asegurar que los usuarios solo vean las campañas de su tenant
        return Campaign.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        # Asignar el tenant del usuario al crear una nueva campaña
        serializer.save(tenant=self.request.user.tenant)

    @action(detail=True, methods=['post'], url_path='send')
    def send_campaign(self, request, pk=None):
        campaign = self.get_object()

        # Regla crítica: validar que los canales estén activos
        active_channels = campaign.channels.filter(is_active=True).count()
        if active_channels == 0:
            return Response(
                {"error": "La campaña no tiene canales activos o conectados."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Lógica para poner la campaña en la cola de envío
        campaign.status = 'scheduled'
        campaign.save()

        # TODO: Lanzar una tarea asíncrona para procesar el envío

        return Response(
            {"status": f"Campaña '{campaign.name}' programada para envío."},
            status=status.HTTP_200_OK
        )


class EmailRenderView(APIView):
    """
    Renderiza una plantilla de email con un contexto dado.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        template_content = request.data.get('template')
        context_data = request.data.get('context', {})

        if not template_content:
            return Response(
                {"error": "El campo 'template' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            template = Template(template_content)
            context = Context(context_data)
            rendered_html = template.render(context)
            return Response({"rendered_html": rendered_html}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Error al renderizar la plantilla: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class AIRewriteEmailView(APIView):
    """
    Utiliza la IA para reescribir y optimizar el contenido de un email.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        base_text = request.data.get('text')
        if not base_text:
            return Response(
                {"error": "El campo 'text' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # El prompt se puede mejorar para darle más contexto a la IA
        prompt = f"Reescribe el siguiente texto para un email de marketing, optimizando su claridad y poder de conversión:\n\n{base_text}"

        try:
            # Reutilizamos el AIManager y los sanitizers del módulo AI
            raw_text, provider_name = ai_manager.execute_text_generation(prompt=prompt, model='default-text-model')
            sanitized_text = sanitize_plain_text(raw_text)

            # Persistimos la interacción (opcional, pero buena práctica)
            # from infrastructure.models import AIInteraction
            # AIInteraction.objects.create(...)

            return Response({"rewritten_text": sanitized_text}, status=status.HTTP_200_OK)
        except RuntimeError as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response(
                {"error": f"Ocurrió un error inesperado durante la reescritura con IA: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SocialPostPreviewView(APIView):
    """
    Valida y genera una previsualización para una publicación en redes sociales.
    """
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


class MarketingAnalyticsView(APIView):
    """
    Proporciona datos de analítica para el módulo de marketing.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tenant = request.user.tenant

        # Métricas generales
        total_sends = SendLog.objects.filter(variant__channel__campaign__tenant=tenant).count()
        successful_sends = SendLog.objects.filter(variant__channel__campaign__tenant=tenant, status='success').count()
        failed_sends = SendLog.objects.filter(variant__channel__campaign__tenant=tenant, status='failed').count()

        # Métricas por campaña
        campaign_stats = Campaign.objects.filter(tenant=tenant).annotate(
            sends=Count('channels__variants__logs'),
            success=Count('channels__variants__logs', filter=Q(channels__variants__logs__status='success')),
            fails=Count('channels__variants__logs', filter=Q(channels__variants__logs__status='failed'))
        ).values('id', 'name', 'sends', 'success', 'fails')

        overview_data = {
            "total_sends": total_sends,
            "successful_sends": successful_sends,
            "failed_sends": failed_sends,
            "success_rate": (successful_sends / total_sends) * 100 if total_sends > 0 else 0,
        }

        # Separamos la respuesta según el endpoint solicitado
        # Esto es un pequeño truco para usar una sola vista para dos endpoints similares
        if 'campaigns' in request.path:
            return Response(list(campaign_stats), status=status.HTTP_200_OK)

        return Response(overview_data, status=status.HTTP_200_OK)
