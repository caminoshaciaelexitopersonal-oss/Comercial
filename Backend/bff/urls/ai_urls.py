# bff/urls/ai_urls.py
from django.urls import path
from bff.views import ai_studio_views

urlpatterns = [
    path('text/', ai_studio_views.GenerateTextView.as_view(), name='ai-generate-text'),
    path('campaign/', ai_studio_views.GenerateCampaignView.as_view(), name='ai-generate-campaign'),
    path('image/', ai_studio_views.GenerateImageView.as_view(), name='ai-generate-image'),
    path('video/', ai_studio_views.GenerateVideoView.as_view(), name='ai-generate-video'),
    path('video/status/<int:job_id>/', ai_studio_views.VideoStatusView.as_view(), name='ai-video-status'),
]
