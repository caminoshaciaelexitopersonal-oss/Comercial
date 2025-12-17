from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from shared.permissions import HasPermission
from .models import Funnel, FunnelVersion, FunnelPage, FunnelPublication
from .serializers import FunnelSerializer, FunnelVersionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import random
from django.db import transaction
from rest_framework.views import APIView
from .models import LeadCapture, FunnelEvent
from shared.services import event_dispatcher


class LeadCaptureView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, slug, *args, **kwargs):
        try:
            publication = FunnelPublication.objects.get(public_url_slug=slug, is_active=True)
        except FunnelPublication.DoesNotExist:
            return Response({"error": "Funnel no encontrado."}, status=404)

        form_data = request.data.get('form_data', {})
        page_id = request.data.get('page_id')

        if not page_id:
            return Response({"error": "El campo 'page_id' es requerido."}, status=400)

        lead = LeadCapture.objects.create(
            funnel=publication.funnel,
            version=publication.version,
            page_id=page_id,
            form_data=form_data
        )

        # Emitir el evento de dominio
        event_dispatcher.dispatch(
            'lead.created',
            {
                'lead_id': lead.id,
                'funnel_id': lead.funnel.id,
                'version_id': lead.version.id,
                'tenant_id': lead.funnel.tenant_id,
                'form_data': lead.form_data,
            }
        )

        return Response({"status": "Lead capturado exitosamente."}, status=201)


class FunnelEventView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        funnel_id = request.data.get('funnel_id')
        version_id = request.data.get('version_id')
        event_type = request.data.get('event_type')
        metadata = request.data.get('metadata', {})
        experiment_id = request.data.get('experiment_id')

        if not all([funnel_id, version_id, event_type]):
            return Response({"error": "Los campos 'funnel_id', 'version_id', y 'event_type' son requeridos."}, status=400)

        FunnelEvent.objects.create(
            funnel_id=funnel_id,
            version_id=version_id,
            event_type=event_type,
            metadata_json=metadata,
            experiment_id=experiment_id
        )
        return Response(status=202)


class PublicFunnelView(APIView):
    authentication_classes = [] # Sin autenticación
    permission_classes = []

    def get(self, request, slug, *args, **kwargs):
        try:
            publication = FunnelPublication.objects.select_related(
                'version', 'funnel__experiment__version_a', 'funnel__experiment__version_b'
            ).get(public_url_slug=slug, is_active=True)

            funnel = publication.funnel
            experiment = hasattr(funnel, 'experiment') and funnel.experiment.status == 'active'

            version_to_serve = publication.version
            experiment_id = None

            if experiment:
                # Lógica de A/B Testing
                session_key = f'funnel_experiment_{funnel.id}_version'
                assigned_version_id = request.session.get(session_key)

                experiment_id = funnel.experiment.id

                if assigned_version_id:
                    if assigned_version_id == funnel.experiment.version_a_id:
                        version_to_serve = funnel.experiment.version_a
                    else:
                        version_to_serve = funnel.experiment.version_b
                else:
                    if random.randint(1, 100) <= funnel.experiment.traffic_split:
                        version_to_serve = funnel.experiment.version_a
                    else:
                        version_to_serve = funnel.experiment.version_b
                    request.session[session_key] = version_to_serve.id

            serializer = FunnelVersionSerializer(version_to_serve)
            response_data = serializer.data
            response_data['experiment_id'] = experiment_id

            return Response(response_data)

        except FunnelPublication.DoesNotExist:
            return Response({"error": "Funnel no encontrado o no está publicado."}, status=404)


class FunnelViewSet(viewsets.ModelViewSet):
    queryset = Funnel.objects.all().prefetch_related('versions')
    serializer_class = FunnelSerializer
    permission_classes = [IsAuthenticated] # TEMPORALMENTE DESHABILITADO: HasPermission

    def get_required_permissions(self, action):
        """Devuelve la lista de permisos requeridos para una acción."""
        if action in ['create', 'versions']:
            return ['funnels:create']
        if action == 'publish':
            return ['funnels:publish']
        if action in ['update', 'partial_update', 'destroy']:
            return ['funnels:edit']
        return ['funnels:view']

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        funnel = serializer.save(tenant=self.request.user.tenant)
        # Al crear un funnel, creamos una primera versión vacía
        FunnelVersion.objects.create(funnel=funnel, version_number=1, schema_json={}, is_active=True)

    @action(detail=True, methods=['post'], url_path='versions')
    @transaction.atomic
    def create_version(self, request, pk=None):
        funnel = self.get_object()
        schema_json = request.data.get('schema_json')
        pages_data = request.data.get('pages', [])

        if not schema_json:
            return Response({"error": "El campo 'schema_json' es requerido."}, status=400)

        # Calculamos el nuevo número de versión
        latest_version = funnel.versions.first()
        new_version_number = (latest_version.version_number + 1) if latest_version else 1

        # Creamos la nueva versión
        new_version = FunnelVersion.objects.create(
            funnel=funnel,
            version_number=new_version_number,
            schema_json=schema_json
        )

        # Creamos las páginas asociadas
        for index, page_data in enumerate(pages_data):
            FunnelPage.objects.create(
                funnel_version=new_version,
                page_type=page_data.get('page_type', 'default'),
                page_schema_json=page_data.get('page_schema_json', {}),
                order_index=index
            )

        serializer = FunnelVersionSerializer(new_version)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['post'], url_path='publish')
    @transaction.atomic
    def publish(self, request, pk=None):
        funnel = self.get_object()
        version_id = request.data.get('version_id')

        if not version_id:
            return Response({"error": "El campo 'version_id' es requerido."}, status=400)

        try:
            version_to_publish = funnel.versions.get(id=version_id)
        except FunnelVersion.DoesNotExist:
            return Response({"error": "La versión especificada no existe para este funnel."}, status=404)

        # Desactivar publicaciones anteriores de este funnel
        funnel.publications.update(is_active=False)

        # Crear la nueva publicación
        publication = FunnelPublication.objects.create(
            funnel=funnel,
            version=version_to_publish,
            is_active=True
        )

        # Actualizar el estado del funnel
        funnel.status = 'published'
        funnel.save()

        return Response({
            "status": "Funnel publicado exitosamente.",
            "public_url": f"/f/{publication.public_url_slug}" # URL relativa
        }, status=200)
