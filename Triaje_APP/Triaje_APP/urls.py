from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('triaje.urls')),
    path('', include('dea_finder.urls')),
    path('', include('clinic_finder.urls')),
]
