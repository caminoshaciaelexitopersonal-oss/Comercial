from django.urls import path
from .views import TextGenerationView

urlpatterns = [
    path('text', TextGenerationView.as_view(), name='ai_text_generation'),
]
