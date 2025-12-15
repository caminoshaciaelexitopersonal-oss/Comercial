# api/views/content_studio_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import GenerateTextSerializer, GenerateImageSerializer
from ..services.ai_manager.ai_manager import ai_manager

class GenerateTextView(APIView):
    """
    Vista para generar texto usando un proveedor de IA.
    """
    def post(self, request, *args, **kwargs):
        serializer = GenerateTextSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                provider = ai_manager.get_provider(data['provider'])
                result = provider.generate_text(
                    prompt=data['prompt'],
                    model=data['model']
                )
                return Response({"result": result}, status=status.HTTP_200_OK)
            except (ValueError, RuntimeError) as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenerateImageView(APIView):
    """
    Vista para generar una imagen usando un proveedor de IA.
    """
    def post(self, request, *args, **kwargs):
        serializer = GenerateImageSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                provider = ai_manager.get_provider(data['provider'])
                image_url = provider.generate_image(
                    prompt=data['prompt'],
                    model=data['model']
                )
                if image_url:
                    return Response({"image_url": image_url}, status=status.HTTP_200_OK)
                return Response({"error": "Failed to generate image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except (ValueError, RuntimeError) as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
