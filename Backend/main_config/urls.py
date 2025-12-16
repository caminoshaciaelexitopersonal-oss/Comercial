 
# main_config/urls.py
 
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
 
    path('admin/', admin.site.urls),
 
    path('api/bff/', include('bff.urls')),
    path('api/ai/', include('ai.urls')),
    path('api/marketing/', include('marketing.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/automation/', include('automation.urls')),
    path('api/funnels/', include('funnels.urls')),
]
