# bff/urls/funnel_builder_urls.py
from django.urls import path
from bff.views.funnel_builder_views import (
    FunnelBuilderDataView,
    FunnelCreateView,
    FunnelSchemaUpdateView,
    FunnelPublishView,
)

urlpatterns = [
    path('funnel-editor-data/', FunnelBuilderDataView.as_view(), name='bff-funnel-editor-data'),
    path('landing-pages/<int:lp_id>/funnels/', FunnelCreateView.as_view(), name='bff-funnel-create'),
    path('funnels/<int:funnel_id>/', FunnelSchemaUpdateView.as_view(), name='bff-funnel-schema-update'),
    path('funnels/<int:funnel_id>/publish/', FunnelPublishView.as_view(), name='bff-funnel-publish'),
]
