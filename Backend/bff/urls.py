# bff/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView

urlpatterns = [
    # Endpoint de registro personalizado
    path('auth/register/', UserRegistrationView.as_view(), name='register'),

    # Endpoints de Simple JWT para login y refresco de token
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
