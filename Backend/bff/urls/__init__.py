# bff/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ..views import builder_views, public_views
from ..views.auth_views import UserRegistrationView # Asumiendo que se ha refactorizado a auth_views

# Router para las vistas privadas del constructor (builder)
builder_router = DefaultRouter()
builder_router.register(r'funnels', builder_views.EmbudoViewSet, basename='funnel')
builder_router.register(r'pages', builder_views.PaginaViewSet, basename='page')
builder_router.register(r'blocks', builder_views.BloqueViewSet, basename='block')

urlpatterns = [
    # --- Autenticación ---
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- API del Estudio de IA ---
    path('ai/', include('bff.urls.ai_urls')),

    # --- API de Ventas ---
    path('sales/', include('bff.urls.sales_urls')),

    # --- API Privada del Constructor ---
    path('builder/', include(builder_router.urls)),

    # --- API Pública (separada, podría ir en otro archivo de URLs a futuro) ---
    # Nota: Este endpoint no debería estar en /api/bff/ sino en /api/public/
    # Por simplicidad en esta fase, lo mantenemos aquí.
    path('public/funnel/<slug:slug>/', public_views.PublicFunnelView.as_view(), name='public-funnel'),
]
