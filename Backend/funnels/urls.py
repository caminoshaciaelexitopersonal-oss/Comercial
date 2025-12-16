from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FunnelViewSet, PublicFunnelView, LeadCaptureView, FunnelEventView

router = DefaultRouter()
router.register(r'', FunnelViewSet, basename='funnel')

urlpatterns = [
    path('', include(router.urls)),
    path('public/<slug:slug>/', PublicFunnelView.as_view(), name='public-funnel'),
    path('public/<slug:slug>/leads/', LeadCaptureView.as_view(), name='lead-capture'),
    path('public/events/', FunnelEventView.as_view(), name='funnel-event'),
]
