# bff/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views.auth_views import CustomTokenObtainPairView, UserRegistrationView
from .views import (
    CampaignViewSet, CustomerViewSet, FunnelViewSet,
    AssetViewSet, AIInteractionViewSet, GenerateTextView
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
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Nuevas rutas BFF para el Funnel Builder (FASE 4.5)
    path('funnel-builder/', include('bff.urls.funnel_builder_urls')),

    # Endpoints generados por el router
    path('', include(router.urls)),
 
    # Endpoints de la Fase 3 (Content Studio)
    path('content-studio/generate-text/', GenerateTextView.as_view(), name='generate-text'),
]
