# bff/urls/sales_urls.py
from django.urls import path
from bff.views.sales_views import OpportunityBFFView

urlpatterns = [
    path('opportunities/', OpportunityBFFView.as_view(), name='bff-opportunities'),
]
