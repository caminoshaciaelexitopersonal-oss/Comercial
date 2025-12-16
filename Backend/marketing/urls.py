from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CampaignViewSet, EmailRenderView, AIRewriteEmailView,
    SocialPostPreviewView, MarketingAnalyticsView
)

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')

urlpatterns = [
    path('', include(router.urls)),
    path('email/render', EmailRenderView.as_view(), name='email_render'),
    path('email/ai-rewrite', AIRewriteEmailView.as_view(), name='email_ai_rewrite'),
    path('social/preview', SocialPostPreviewView.as_view(), name='social_preview'),
    path('analytics/overview', MarketingAnalyticsView.as_view(), name='analytics_overview'),
    path('analytics/campaigns', MarketingAnalyticsView.as_view(), name='analytics_campaigns'),
]
