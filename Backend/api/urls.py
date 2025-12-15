# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rutas de gestión
    path('ai/providers/', views.AIProvidersView.as_view(), name='ai-providers'),
    path('ollama/models/', views.OllamaModelsView.as_view(), name='ollama-models'),
    path('ollama/models/pull/', views.OllamaPullView.as_view(), name='ollama-pull'),

    # Rutas del Content Studio
    path('content-studio/generate-text/', views.GenerateTextView.as_view(), name='generate-text'),
    path('content-studio/generate-image/', views.GenerateImageView.as_view(), name='generate-image'),
]
