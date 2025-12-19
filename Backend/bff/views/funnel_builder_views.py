# bff/views/funnel_builder_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from domain.services.funnel_service import get_full_funnel_builder_data, create_new_funnel_version
from bff.serializers.funnel_builder_serializers import FunnelBuilderDataSerializer, FunnelContentSerializer
from funnels.models import Funnel, FunnelVersion, FunnelPublication, LandingPage
from django.db import transaction

class FunnelBuilderDataView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        tenant = request.user.tenant
        funnel_data = get_full_funnel_builder_data(tenant.id)
        serializer = FunnelBuilderDataSerializer(funnel_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FunnelCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request, lp_id, *args, **kwargs):
        tenant = request.user.tenant
        funnel_name = request.data.get('name')
        funnel_schema = request.data.get('schema')
        try:
            landing_page = get_object_or_404(LandingPage, id=lp_id, subcategoria__categoria__cadena__tenant=tenant)
            new_funnel = Funnel.objects.create(tenant=tenant, landing_page=landing_page, name=funnel_name)
            create_new_funnel_version(funnel=new_funnel, schema_json=funnel_schema)
            serializer = FunnelContentSerializer(new_funnel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except LandingPage.DoesNotExist:
            return Response({"error": "LandingPage not found."}, status=status.HTTP_404_NOT_FOUND)

class FunnelSchemaUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, funnel_id, *args, **kwargs):
        tenant = request.user.tenant
        funnel_schema = request.data
        try:
            funnel = get_object_or_404(Funnel, id=funnel_id, tenant=tenant)
            create_new_funnel_version(funnel=funnel, schema_json=funnel_schema)
            return Response({"status": "Funnel version saved successfully."}, status=status.HTTP_200_OK)
        except Funnel.DoesNotExist:
            return Response({"error": "Funnel not found."}, status=status.HTTP_404_NOT_FOUND)

class FunnelPublishView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request, funnel_id, *args, **kwargs):
        tenant = request.user.tenant
        version_id = request.data.get('version_id')
        try:
            funnel = get_object_or_404(Funnel, id=funnel_id, tenant=tenant)
            version_to_publish = get_object_or_404(FunnelVersion, id=version_id, funnel=funnel)
            funnel.publications.update(is_active=False)
            publication = FunnelPublication.objects.create(funnel=funnel, version=version_to_publish, is_active=True)
            funnel.status = 'published'
            funnel.save()
            return Response({"status": "Funnel publicado exitosamente.", "public_url_slug": publication.public_url_slug}, status=status.HTTP_200_OK)
        except (Funnel.DoesNotExist, FunnelVersion.DoesNotExist):
            return Response({"error": "Funnel o versión no encontrada."}, status=status.HTTP_404_NOT_FOUND)
