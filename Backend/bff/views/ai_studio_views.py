# bff/views/ai_studio_views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from bff.serializers.ai_studio_serializers import GenerateTextSerializer, GenerateImageSerializer, GenerateVideoSerializer
from domain.services import text_generation_service, image_generation_service, video_generation_service
from infrastructure.models import AsyncTask

class GenerateTextView(APIView):
    """
    Vista del BFF para el Asistente de Redacción (Generación de Texto).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = GenerateTextSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                result = text_generation_service.generate_text_with_memory(
                    user=request.user,
                    prompt=data['prompt'],
                    model=data.get('model', 'default-text-model') # El AIManager elegirá
                )
                return Response({"result": result}, status=status.HTTP_200_OK)
            except RuntimeError as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = GenerateImageSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                asset = image_generation_service.generate_image_with_memory(
                    user=request.user,
                    prompt=data['prompt'],
                    model=data.get('model', 'default-image-model')
                )
                return Response({"asset_id": asset.id, "content_url": asset.content}, status=status.HTTP_201_CREATED)
            except RuntimeError as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateCampaignView(APIView):
    """
    Vista del BFF para el Generador de Campañas Automáticas.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        business_goal = request.data.get('business_goal')
        if not business_goal:
            return Response({"error": "business_goal is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            campaign_json = campaign_generation_service.generate_automatic_campaign(
                user=request.user,
                business_goal=business_goal
            )
            return Response(campaign_json, status=status.HTTP_200_OK)
        except RuntimeError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerateVideoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = GenerateVideoSerializer(data=request.data)
        if serializer.is_valid():
            task = video_generation_service.start_video_generation(
                user=request.user,
                prompt=serializer.validated_data['prompt']
            )
            return Response({"job_id": task.id}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id, *args, **kwargs):
        try:
            task = AsyncTask.objects.get(id=job_id, tenant=request.user.tenant)
            return Response({
                "job_id": task.id,
                "status": task.status,
                "result_url": task.result_url,
                "error_message": task.error_message,
            })
        except AsyncTask.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
