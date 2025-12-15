# bff/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserRegistrationView, CampaignViewSet, CustomerViewSet,
    FunnelViewSet, AssetViewSet, AIInteractionViewSet,
    GenerateTextView
)

# Creamos un router para registrar los ViewSets
router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'funnels', FunnelViewSet, basename='funnel')
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'ai-interactions', AIInteractionViewSet, basename='ai-interaction')

urlpatterns = [
    # Endpoints de registro y autenticación
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Endpoints generados por el router para las entidades de la Fase 2
    path('', include(router.urls)),

    # Endpoints de la Fase 3 (Content Studio)
    path('content-studio/generate-text/', GenerateTextView.as_view(), name='generate-text'),
]
